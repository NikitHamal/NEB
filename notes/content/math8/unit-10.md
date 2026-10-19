---
subject: Mathematics
grade: 8
unit: 10
title: Algebraic Expressions
hours: 0
area: Compulsory Mathematics
---

An algebraic expression is arithmetic with letters in it, and factorising is the
art of writing it as a product instead of a sum. That single change is what
makes it possible to cancel, to solve and to see structure. This chapter
reviews the vocabulary, then works through the highest common factor and the
lowest common multiple of expressions, factorisation by taking out a common
factor and by grouping, and the three standard identities that every later
chapter depends on.

::: key What this chapter asks of you
You should be able to name the terms, coefficient and degree of an expression,
find the HCF and LCM of two or more expressions, factorise by taking out a
common factor and by grouping, and use the identities
$(a\pm b)^2$, $a^2-b^2$ in both directions.
:::

## 10.1 Terms, coefficients and like terms

An **algebraic expression** is a combination of constants and variables joined
by $+$, $-$ and $\times$. In $5x^2-3x+7$:

- the **terms** are $5x^2$, $-3x$ and $7$;
- the **coefficient** of $x^2$ is 5 and of $x$ is $-3$;
- the **constant term** is 7;
- the **degree** of the expression is 2, the highest power of the variable.

**Like terms** have the same variable raised to the same power and can be added
or subtracted: $5x^2+3x^2=8x^2$, but $5x^2+3x$ cannot be combined.

::: caution $-3x$ is a term with a minus sign
When you collect like terms in $7x-3x+2x$, the answer is $6x$, not $12x$. The
sign belongs to the term that follows it. Writing each term with its sign
before collecting removes an entire family of mistakes.
:::

## 10.2 Highest common factor of expressions

The **HCF** of two or more expressions is the product of every factor common to
all of them, each taken to its **lowest** power.

**Method.** Factorise each expression completely, write the common factors with
their smallest indices, and multiply.

::: example HCF of two expressions
**Problem.** Find the HCF of $12x^3y^2$ and $18x^2y^4$.

**Solution.** Factorise each:

$$12x^3y^2=2^2\times3\times x^3y^2,\qquad
18x^2y^4=2\times3^2\times x^2y^4$$

Common to both: one 2, one 3, $x^2$ and $y^2$.

$$\text{HCF}=2\times3\times x^2\times y^2=6x^2y^2$$

**Check.** $\frac{12x^3y^2}{6x^2y^2}=2x$ ✓ and
$\frac{18x^2y^4}{6x^2y^2}=3y^2$ ✓ — both quotients are whole expressions, as
they must be for a common factor.
:::

::: example HCF of three expressions
**Problem.** Find the HCF of $8a^2b$, $12ab^2$ and $20a^2b^2$.

**Solution.** Numbers: HCF of 8, 12 and 20 is 4. For $a$: the smallest power is
$a^1$. For $b$: the smallest power is $b^1$.

$$\text{HCF}=4ab$$

**Check.** Dividing each by $4ab$ gives $2a$, $3b$ and $5ab$ ✓, none of which
has a further common factor.
:::

## 10.3 Lowest common multiple of expressions

The **LCM** is the product of every factor that appears in **any** of the
expressions, each taken to its **highest** power.

$$\text{HCF}\times\text{LCM}=\text{product of the two expressions}\quad
\text{(for two expressions)}$$

::: example LCM of two expressions
**Problem.** Find the LCM of $6x^2y$ and $9xy^3$.

**Solution.** Numbers: LCM of 6 and 9 is 18. For $x$: highest power $x^2$. For
$y$: highest power $y^3$.

$$\text{LCM}=18x^2y^3$$

**Check.** Using the product rule (here the product is
$6x^2y\times9xy^3=54x^3y^4$):
$\text{LCM}=\frac{54x^3y^4}{3xy}=18x^2y^3$ ✓, agreeing with the direct answer.
:::

::: example HCF and LCM together
**Problem.** For $4a^3b^2$ and $10a^2b^3$, find both the HCF and the LCM, and
verify that $\text{HCF}\times\text{LCM}$ equals the product of the two
expressions.

**Solution.** HCF: numbers 2, $a^2$, $b^2$, so $\text{HCF}=2a^2b^2$.

LCM: numbers 20, $a^3$, $b^3$, so $\text{LCM}=20a^3b^3$.

$$\text{HCF}\times\text{LCM}=2a^2b^2\times20a^3b^3=40a^5b^5$$

Product of the expressions:
$4a^3b^2\times10a^2b^3=40a^5b^5$. They agree ✓.
:::

## 10.4 Factorisation by taking out a common factor

The first thing to look for in any expression is a factor common to every term.
The distributive law then works backwards:

$$ab+ac=a(b+c)$$

::: example Factorising a binomial
**Problem.** Factorise $4x^3-8x^2$.

**Solution.** The HCF of the two terms is $4x^2$, so

$$4x^3-8x^2=4x^2(x-2)$$

**Check.** Expanding: $4x^2\times x-4x^2\times2=4x^3-8x^2$ ✓. Always expand your
answer back — it takes ten seconds and it is the only complete check in
factorising.
:::

::: example A common binomial factor
**Problem.** Factorise $3a(x+y)+5b(x+y)$.

**Solution.** The whole bracket $(x+y)$ is common:

$$3a(x+y)+5b(x+y)=(x+y)(3a+5b)$$

**Answer.** $(x+y)(3a+5b)$.
:::

## 10.5 Factorisation by grouping

When there is no common factor to all four terms, group them in pairs, take a
common factor out of each pair, and hope for a common bracket.

::: example Factorising four terms by grouping
**Problem.** Factorise $6x^2+9x+4x+6$.

**Solution.** Group the first two and the last two:

$$6x^2+9x+4x+6=3x(2x+3)+2(2x+3)$$

Now $(2x+3)$ is common:

$$=(2x+3)(3x+2)$$

**Answer.** $(2x+3)(3x+2)$.

**Check.** Expanding: $6x^2+4x+9x+6=6x^2+13x+6$ ✓, which is the original.
:::

::: example Grouping with a sign change
**Problem.** Factorise $a^2-ab+ac-bc$.

**Solution.** Group as $(a^2-ab)+(ac-bc)$:

$$=a(a-b)+c(a-b)=(a-b)(a+c)$$

**Answer.** $(a-b)(a+c)$.

**Check.** Expanding: $a^2+ac-ab-bc$ ✓.

**Note.** If the second group had been written as $(ac-bc)=c(a-b)$, the brackets
matched. If they come out matching with opposite signs, take the minus sign out
of the whole group, which reverses both terms inside it.
:::

::: caution The sign that reverses a bracket
From $x^2-5x-3x+15$ the grouping gives $x(x-5)-3(x-5)$, not
$x(x-5)+3(x-5)$. Factorising $-3x+15$ as $-3(x-5)$ is correct; as $+3(x-5)$ it
is not, because $3(x-5)=3x-15$. When the last two terms have a minus before the
third, put the minus outside the bracket.
:::

## 10.6 The standard identities

The three identities below are used in both directions: to expand a product, and
to factorise a sum.

| Identity | Expanded form |
|---|---|
| $(a+b)^2$ | $a^2+2ab+b^2$ |
| $(a-b)^2$ | $a^2-2ab+b^2$ |
| $(a+b)(a-b)$ | $a^2-b^2$ |

::: example The difference of two squares
**Problem.** Factorise $9x^2-16y^2$.

**Solution.** Both terms are perfect squares: $9x^2=(3x)^2$ and
$16y^2=(4y)^2$. Using $a^2-b^2=(a+b)(a-b)$,

$$9x^2-16y^2=(3x+4y)(3x-4y)$$

**Answer.** $(3x+4y)(3x-4y)$.

**Check.** Expanding: $9x^2-12xy+12xy-16y^2=9x^2-16y^2$ ✓.
:::

::: example Squaring a binomial
**Problem.** Expand $(2x+5)^2$.

**Solution.** With $a=2x$ and $b=5$:

$$(2x+5)^2=(2x)^2+2(2x)(5)+5^2=4x^2+20x+25$$

**Answer.** $4x^2+20x+25$.

**Check.** Put $x=1$: the original is $7^2=49$, and the answer is
$4+20+25=49$ ✓.
:::

::: example Using an identity to evaluate a number
**Problem.** Evaluate $103\times97$ and $102^2$ without a calculator.

**Solution.** Write each as an identity.

$$103\times97=(100+3)(100-3)=100^2-3^2=10\,000-9=9991$$

$$102^2=(100+2)^2=10\,000+400+4=10\,404$$

**Check.** $103\times97=9991$ ✓ and $102\times102=10\,404$ ✓.
:::

::: example Factorising with a common factor first
**Problem.** Factorise $2x^3-8x$ completely.

**Solution.** Take out the common factor 2 first, then recognise a difference of
two squares:

$$2x^3-8x=2x(x^2-4)=2x(x+2)(x-2)$$

**Answer.** $2x(x+2)(x-2)$.

**Check.** Expanding: $2x(x^2-4)=2x^3-8x$ ✓. Notice that "completely" is not
satisfied by $2x(x^2-4)$; the bracket still factorises.
:::

### 10.6.1 Perfect squares and the blank term

An expression $a^2\pm2ab+b^2$ is a **perfect square**. To decide what must go
in a blank, compare with $a^2+2ab+b^2$:

- the middle term is $2\times\sqrt{\text{first}}\times\sqrt{\text{last}}$;
- the last term is $\left(\frac{\text{middle}}{2\sqrt{\text{first}}}\right)^2$.

::: example Completing a perfect square
**Problem.** Fill the blank so that each is a perfect square:
(a) $x^2+\ \dots\ +16$ (b) $9a^2-\ \dots\ +49b^2$ (c) $p^2+\ \dots\ +\frac{1}{p^2}$.

**Solution.**
(a) $x^2+16=x^2+4^2$, so the middle term is $2\times x\times4=8x$:
$x^2+8x+16=(x+4)^2$.

(b) $9a^2=(3a)^2$, $49b^2=(7b)^2$, so the middle term is
$2\times3a\times7b=42ab$: $9a^2-42ab+49b^2=(3a-7b)^2$.

(c) Middle term $=2\times p\times\frac1p=2$: $p^2+2+\frac{1}{p^2}=\left(p+\frac1p\right)^2$.
:::

::: example Factorising perfect squares
**Problem.** Factorise (a) $4x^2+12x+9$ (b) $36a^2-48ab+16b^2$.

**Solution.**
(a) $4x^2+12x+9=(2x)^2+2\times2x\times3+3^2=(2x+3)^2$.

(b) $36a^2-48ab+16b^2=(6a)^2-2\times6a\times4b+(4b)^2=(6a-4b)^2$

$=[2(3a-2b)]^2=4(3a-2b)^2$.
:::

::: example Perfect square, then difference of squares
**Problem.** Factorise $16x^2+40x+25-y^2$.

**Solution.** The first three terms form a perfect square:

$16x^2+40x+25=(4x)^2+2\times4x\times5+5^2=(4x+5)^2$.

So the expression is $(4x+5)^2-y^2=(4x+5+y)(4x+5-y)$.
:::

## 10.8 Factorising $x^2+bx+c$

Expanding $(x+p)(x+q)=x^2+(p+q)x+pq$. So to factorise $x^2+bx+c$ we look for
two numbers $p$ and $q$ with

$$p\times q=c\quad\text{and}\quad p+q=b$$

then split the middle term and group.

| Sign of $c$ | What to look for | Signs of the two numbers |
|---|---|---|
| $c$ positive | product $c$, **sum** $b$ | both the same sign as $b$ |
| $c$ negative | product $c$, **difference** $|b|$ | opposite signs; the bigger one takes the sign of $b$ |

::: example When the constant term is positive
**Problem.** Factorise (a) $x^2+5x+6$ (b) $x^2-6x+5$.

**Solution.**
(a) Product 6, sum 5: the numbers are 2 and 3.
$x^2+5x+6=x^2+3x+2x+6=x(x+3)+2(x+3)=(x+3)(x+2)$.

(b) Product 5, sum $-6$: the numbers are $-1$ and $-5$.
$x^2-6x+5=x^2-5x-x+5=x(x-5)-1(x-5)=(x-5)(x-1)$.

**Check (b).** $(x-5)(x-1)=x^2-x-5x+5=x^2-6x+5$ ✓.
:::

::: example When the constant term is negative
**Problem.** Factorise (a) $x^2+5x-6$ (b) $x^2-6x-16$.

**Solution.**
(a) Product $-6$, so the numbers have opposite signs and **difference** 5:
6 and 1, with the bigger one positive: $+6$ and $-1$.
$x^2+5x-6=x^2+6x-x-6=x(x+6)-1(x+6)=(x+6)(x-1)$.

(b) Product $-16$, difference 6: 8 and 2, bigger one negative: $-8$ and $+2$.
$x^2-6x-16=x^2-8x+2x-16=x(x-8)+2(x-8)=(x-8)(x+2)$.

**Check (b).** $(x-8)(x+2)=x^2+2x-8x-16=x^2-6x-16$ ✓.
:::

::: caution Split the middle term with the right signs
For $x^2-6x-16$, the pair $+8,-2$ also has product $-16$, but its sum is $+6$,
not $-6$. Always check the **sum** of the pair against the middle coefficient,
sign included.
:::

## 10.9 HCF and LCM of expressions that need factorising

When the expressions are not single terms, **factorise each one completely
first**. Then

- HCF $=$ product of the common factors;
- LCM $=$ common factors $\times$ the remaining factors.

::: example HCF of three trinomials
**Problem.** Find the HCF of $x^2+6x+8$, $x^2-4$ and $x^2+4x+4$.

**Solution.**
First $=x^2+4x+2x+8=x(x+4)+2(x+4)=(x+2)(x+4)$.
Second $=x^2-2^2=(x+2)(x-2)$.
Third $=x^2+2\cdot x\cdot2+2^2=(x+2)^2=(x+2)(x+2)$.

The only factor common to all three is $(x+2)$, so **HCF $=x+2$**.
:::

::: example LCM of two polynomials
**Problem.** Find the LCM of $3x^3-15x^2$ and $2x^3-50x$.

**Solution.**
First $=3x^2(x-5)=3\times x\times x\times(x-5)$.
Second $=2x(x^2-25)=2\times x\times(x+5)(x-5)$.

Common factors: $x(x-5)$. Remaining factors: $3\times x$ from the first and
$2\times(x+5)$ from the second.

LCM $=x(x-5)\times3x\times2(x+5)=6x^2(x-5)(x+5)$.
:::

::: example LCM using a trinomial
**Problem.** Find the LCM of $x^2+x-20$ and $x^2-25$.

**Solution.**
First $=x^2+5x-4x-20=x(x+5)-4(x+5)=(x+5)(x-4)$.
Second $=(x+5)(x-5)$.

Common factor $(x+5)$; remaining factors $(x-4)$ and $(x-5)$.
**LCM $=(x+5)(x-4)(x-5)$.**
:::

## 10.7 The three identities as areas

```figure caption="The identity (a + b)² = a² + 2ab + b² seen as a square. The big square of side (a + b) is made of two squares and two equal rectangles."
fig, ax = plt.subplots(figsize=(4.2, 3.5))
A, B = 0.46, 0.28
x0, y0 = 0.1, 0.1
ax.add_patch(matplotlib.patches.Rectangle((x0, y0 + B), A, A,
             facecolor=SERIES[0], alpha=0.8, edgecolor="white", linewidth=1.4))
ax.add_patch(matplotlib.patches.Rectangle((x0 + A, y0 + B), B, A,
             facecolor=SERIES[2], alpha=0.8, edgecolor="white", linewidth=1.4))
ax.add_patch(matplotlib.patches.Rectangle((x0, y0), A, B,
             facecolor=SERIES[2], alpha=0.8, edgecolor="white", linewidth=1.4))
ax.add_patch(matplotlib.patches.Rectangle((x0 + A, y0), B, B,
             facecolor=SERIES[3], alpha=0.8, edgecolor="white", linewidth=1.4))
ax.text(x0 + A / 2, y0 + B + A / 2, "$a^2$", ha="center", va="center",
        color="white", fontsize=12)
ax.text(x0 + A + B / 2, y0 + B + A / 2, "$ab$", ha="center", va="center",
        color="white", fontsize=10)
ax.text(x0 + A / 2, y0 + B / 2, "$ab$", ha="center", va="center",
        color="white", fontsize=10)
ax.text(x0 + A + B / 2, y0 + B / 2, "$b^2$", ha="center", va="center",
        color="white", fontsize=10)
ax.text(x0 + A / 2, y0 + A + B + 0.03, "$a$", ha="center", color=INK,
        fontsize=10)
ax.text(x0 + A + B / 2, y0 + A + B + 0.03, "$b$", ha="center", color=INK,
        fontsize=10)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
```

| Identity | Expanded form | Used for |
|---|---|---|
| $(a+b)^2$ | $a^2 + 2ab + b^2$ | squaring a sum, mental arithmetic ($102^2$) |
| $(a-b)^2$ | $a^2 - 2ab + b^2$ | squaring a difference ($98^2$) |
| $a^2 - b^2$ | $(a+b)(a-b)$ | factorising, quick products ($53 \times 47$) |

::: example Identities as a shortcut
**Question.** Evaluate without a calculator: (i) $103^2$ (ii) $97^2$
(iii) $56 \times 44$.

**Answer.**
(i) $(100+3)^2 = 10000 + 600 + 9 = \textbf{10609}$.
(ii) $(100-3)^2 = 10000 - 600 + 9 = \textbf{9409}$.
(iii) $(50+6)(50-6) = 2500 - 36 = \textbf{2464}$.
:::

::: example Factorising in two steps
**Question.** Factorise $2x^2 - 18$.

**Answer.** Take out the common factor first: $2(x^2 - 9)$.
Now use the difference of two squares: $2(x+3)(x-3)$.
**Note:** always look for the common factor before reaching for an identity.
:::

::: note Activity — the algebra tile wall
Cut squares of side $a$, squares of side $b$ and rectangles $a \times b$ from
card (take $a = 6$ cm, $b = 4$ cm). Arrange them to build a square of side
$(a+b)$ and count what you used: one $a^2$, two $ab$, one $b^2$. Then try to
build $(a+b)^2$ using only $a^2$ and $b^2$ — you cannot, and that is the proof
that $(a+b)^2 \neq a^2 + b^2$.
:::

## Chapter summary

- Terms, coefficient, constant and degree describe the parts of an expression;
  only like terms can be combined.
- $\text{HCF}$: every factor common to all the expressions, to its **lowest**
  power.
- $\text{LCM}$: every factor appearing in any expression, to its **highest**
  power.
- For two expressions, $\text{HCF}\times\text{LCM}=$ product of the expressions.
- $ab+ac=a(b+c)$; group four terms in pairs when no single factor is common to
  all of them.
- The standard identities in both directions: $(a\pm b)^2=a^2\pm2ab+b^2$ and
  $(a+b)(a-b)=a^2-b^2$.
- $x^2+bx+c$: find two numbers with product $c$ and sum $b$, split the middle
  term and group.
- For HCF and LCM of polynomials, factorise each expression completely first.
- Factorise completely: take out the common factor first, then look for an
  identity, then check by expanding.

## Practice questions

**Group A — Objective (1 mark each)**

1. The coefficient of $x$ in $7x^2-4x+3$ is <span class="marks">[1]</span>
   (a) 7 (b) $-4$ (c) 3 (d) 4
2. The HCF of $6x^2$ and $9x^3$ is <span class="marks">[1]</span>
   (a) $3x^2$ (b) $3x^3$ (c) $18x^3$ (d) $54x^5$
3. The LCM of $4a$ and $6a^2$ is <span class="marks">[1]</span>
   (a) $2a$ (b) $12a^2$ (c) $24a^3$ (d) $6a$
4. $x^2-9$ factorised is <span class="marks">[1]</span>
   (a) $(x-3)^2$ (b) $(x+3)^2$ (c) $(x+3)(x-3)$ (d) $x(x-9)$
5. $(a+3)^2$ equals <span class="marks">[1]</span>
   (a) $a^2+9$ (b) $a^2+6a+9$ (c) $a^2+3a+9$ (d) $a^2-6a+9$
6. $4x^3-8x^2$ factorised is <span class="marks">[1]</span>
   (a) $4x^2(x-2)$ (b) $4x(x^2-2)$ (c) $2x(2x^2-4)$ (d) $8x^2(x-1)$

::: note Answers to Group A
**1.** (b) — the term is $-4x$.
**2.** (a) — common numbers 3, and the lower power $x^2$.
**3.** (b) — LCM of 4 and 6 is 12, and the higher power is $a^2$.
**4.** (c) — a difference of two squares.
**5.** (b) — $a^2+2(a)(3)+3^2$.
**6.** (a) — the HCF of the two terms is $4x^2$.
:::

**Group B — Short answer (2 marks each)**

1. Find the HCF of $8a^2b$ and $12ab^2$. <span class="marks">[2]</span>
2. Find the LCM of $5x^3y$ and $10xy^2$. <span class="marks">[2]</span>
3. Factorise $a^2+ab+ac+bc$. <span class="marks">[2]</span>
4. Factorise $25m^2-49n^2$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $4ab$.
**2.** $10x^3y^2$.
**3.** $a(a+b)+c(a+b)=(a+b)(a+c)$.
**4.** $(5m)^2-(7n)^2=(5m+7n)(5m-7n)$.
:::

**Group C — Long answer (4 marks each)**

1. Factorise $x^2+7x+12$ by finding two numbers whose product is 12 and whose
   sum is 7, and check by expanding. <span class="marks">[4]</span>
2. If the HCF of two expressions is $3x^2y$ and their LCM is $18x^3y^2$, and one
   of the expressions is $6x^2y^2$, find the other expression.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** The two numbers are 3 and 4, because $3\times4=12$ and $3+4=7$. So
$$x^2+7x+12=(x+3)(x+4)$$
**Check by expanding:**
$x^2+4x+3x+12=x^2+7x+12$ ✓.
**Why it works.** Expanding $(x+p)(x+q)$ gives $x^2+(p+q)x+pq$, so the sum of the
two numbers must be the coefficient of $x$ and their product the constant term.
A quick mental test on the factors of 12 — $1\times12$, $2\times6$, $3\times4$ —
immediately gives the pair whose sum is 7.
**2.** For two expressions,
$\text{HCF}\times\text{LCM}=\text{product of the two expressions}$. So

$$\text{product}=3x^2y\times18x^3y^2=54x^5y^3$$

The known expression is $6x^2y^2$, so the other is

$$\frac{54x^5y^3}{6x^2y^2}=9x^3y$$

**Check.** HCF of $6x^2y^2$ and $9x^3y$: numbers—3; $x$—$x^2$; $y$—$y$; so
$3x^2y$ ✓. LCM: numbers—18; $x$—$x^3$; $y$—$y^2$; so $18x^3y^2$ ✓.
:::

**Extra practice**

**Group B (2 marks)**

**11.** Expand $(3x - 5)^2$.
**12.** Evaluate $104 \times 96$ using an identity.

**Group C (4 marks)**

**13.** Factorise completely: (i) $3x^2 - 27$ (ii) $x^2 + 10x + 25$ (iii) $4a^2-9b^2$
    (iii) $4a^2 - 9b^2$.

**14.** Factorise: (i) $x^2-x-20$ (ii) $9r^2+60r+100$ (iii) $a^2-12a+36-b^2$.
**15.** Find the HCF and the LCM of $x^2-y^2$ and $xy-y^2$.

::: note Extra practice — answers
**11.** $9x^2 - 30x + 25$.
**12.** $(100+4)(100-4) = 10000 - 16 = 9984$.
**13.** (i) $3(x^2-9) = 3(x+3)(x-3)$. (ii) $(x+5)^2$.
(iii) $(2a+3b)(2a-3b)$.
**14.** (i) product $-20$, sum $-1$: $-5$ and $4$, so $(x-5)(x+4)$. (ii) $(3r)^2+2\cdot3r\cdot10+10^2=(3r+10)^2$. (iii) $(a-6)^2-b^2=(a-6+b)(a-6-b)$.
**15.** $x^2-y^2=(x+y)(x-y)$ and $xy-y^2=y(x-y)$. HCF $=x-y$; LCM $=y(x+y)(x-y)$.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** $(x-4)^2$ expands to
   (a) $x^2-16$ (b) $x^2-8x+16$ (c) $x^2+8x+16$ (d) $x^2-4x+16$
**2.** $x^2-49$ factorises as
   (a) $(x-7)^2$ (b) $(x+7)(x-7)$ (c) $(x+49)(x-1)$ (d) $(x+7)^2$
**3.** $101^2$ by an identity is
   (a) 10201 (b) 10001 (c) 11201 (d) 10101
**4.** $x^2+9x+20$ factorises as
   (a) $(x+4)(x+5)$ (b) $(x+2)(x+10)$ (c) $(x+1)(x+20)$ (d) $(x+3)(x+6)$
**5.** $3x^2-12$ factorises completely as
   (a) $3(x^2-4)$ (b) $3(x+2)(x-2)$ (c) $(3x+6)(x-2)$ (d) $3(x-2)^2$

::: note Objective practice — answers
**1.** (b) — $(a-b)^2=a^2-2ab+b^2$. **2.** (b) — difference of two squares. **3.** (a) — $(100+1)^2=10000+200+1$. **4.** (a) — $4+5=9$, $4\times5=20$. **5.** (b) — common factor first, then the identity.
:::

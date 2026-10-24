---
subject: Optional Mathematics
grade: 8
unit: 2
title: Polynomials
hours: 0
---

The cost of $x$ exercise books at Rs 45 each plus a bag at Rs 600 is $45x+600$ rupees. The area of a square floor of side $x$ metres with a 1-metre border around it is $(x+2)^2=x^2+4x+4$ square metres. Expressions like these, built from a variable with whole-number powers, are called **polynomials**. They are the everyday language of algebra: formulas for cost, area, volume, distance and profit are polynomials. In this chapter you will learn to recognise a polynomial, describe it by its degree and its number of terms, write it in standard form, decide when two polynomials are equal, and add, subtract and multiply polynomials.

::: key What your examination asks from this chapter
Expect: (i) say whether an expression is a polynomial, **with a reason**; (ii) find the **degree**, the **leading coefficient** and the **constant term**, and write a polynomial in **standard form**; (iii) name a polynomial by its degree (linear, quadratic, cubic) and by its number of terms (monomial, binomial, trinomial); (iv) find unknown coefficients from **equal polynomials**; (v) add and subtract polynomials, including "what must be added to …"; (vi) multiply polynomials and state the degree of the product; (vii) find the value $f(a)$ of a polynomial function.
:::

## 2.1 Polynomial expressions and polynomial functions; classification by degree and by number of terms

### Terms, coefficients and constants

In the expression $5x^3-2x^2+7x-4$ there are four **terms**: $5x^3$, $-2x^2$, $7x$ and $-4$. The number multiplying a power of $x$ is its **coefficient**: the coefficient of $x^3$ is 5, of $x^2$ is $-2$, and of $x$ is 7. A term with no variable, here $-4$, is the **constant term**. The sign in front of a term belongs to that term.

::: definition Polynomial
A **polynomial** in $x$ is an algebraic expression in which every term is a number, or a number multiplied by a **whole-number power** of $x$ (the powers $x^0, x^1, x^2, x^3, \ldots$). In general it has the form
$$ a_nx^n+a_{n-1}x^{n-1}+\cdots+a_2x^2+a_1x+a_0 $$
where $n$ is a whole number and the coefficients $a_n, \ldots, a_0$ are real numbers.
:::

The coefficients may be fractions, negative numbers or even surds such as $\sqrt{2}$. What is **not allowed** is a variable with a negative power, a fractional power, a variable inside a root, or a variable in a denominator.

| Expression | Polynomial? | Reason |
|---|---|---|
| $4x^2-3x+1$ | yes | powers 2, 1, 0 are whole numbers |
| $\frac{1}{3}x^2-\sqrt{5}\,x$ | yes | the coefficients may be any real numbers |
| $7$ | yes | a constant is $7x^0$ |
| $x^2y+3xy^2-y$ | yes | a polynomial in two variables |
| $2x^3+\frac{5}{x}$ | no | $\frac{5}{x}=5x^{-1}$ has a negative power |
| $\sqrt{x}+2$ | no | $\sqrt{x}=x^{\frac{1}{2}}$ has a fractional power |
| $\frac{1}{x+1}$ | no | the variable is in the denominator |

### Where polynomials come from

Polynomials are not invented for examinations; they appear the moment a quantity is worked out from another by adding and multiplying. The degree tells you how fast the quantity grows.

| Situation | Formula | Kind |
|---|---|---|
| Cost of $x$ copies at Rs 45 and a bag at Rs 600 | $45x+600$ | linear |
| Area of a square floor of side $x$ m with a 1 m border | $(x+2)^2=x^2+4x+4$ | quadratic |
| Distance in metres a stone falls in $t$ seconds (roughly) | $5t^2$ | quadratic monomial |
| Volume of an open box made from a $10	imes8$ cm card by cutting squares of side $x$ cm from the corners | $x(10-2x)(8-2x)=4x^3-36x^2+80x$ | cubic |

In the box, if $x=1$ the volume is $1	imes8	imes6=48$ cm³, and the polynomial gives $4-36+80=48$ as well. A formula and its polynomial form must always agree.

### Polynomial functions

When a polynomial is used as the rule of a function, we call it a **polynomial function** and write, for example, $f(x)=2x^3-x^2+3$. Putting a number in place of $x$ gives the **value** of the polynomial at that number.

::: example Value of a polynomial function
**Problem.** If $f(x)=2x^3-x^2+3$, find $f(2)$, $f(0)$ and $f(-1)$.

**Solution.** Replace $x$ by the given number everywhere, using brackets for negative numbers.
$$ f(2)=2(2)^3-(2)^2+3=16-4+3=15 $$
$$ f(0)=0-0+3=3,\qquad f(-1)=2(-1)^3-(-1)^2+3=-2-1+3=0 $$
Since $f(-1)=0$, we say that $-1$ is a **zero** of the polynomial.
:::

### Classification by degree and by number of terms

The **degree** of a polynomial in one variable is the **highest power** of the variable that appears (with a non-zero coefficient). Polynomials are named by their degree and, separately, by how many terms they have.

| Degree | Name | Example |
|---|---|---|
| 0 | constant polynomial | $9$ |
| 1 | linear polynomial | $5x-3$ |
| 2 | quadratic polynomial | $x^2-4x+4$ |
| 3 | cubic polynomial | $7x^3$ |
| 4 | biquadratic (quartic) polynomial | $x^4-x^2+2x-1$ |

| Number of terms | Name | Example |
|---|---|---|
| 1 | monomial | $-6x^2$, $\ 3xy$, $\ 9$ |
| 2 | binomial | $x^3-8$, $\ 2x+5$ |
| 3 | trinomial | $x^2+5x+6$ |
| 4 or more | polynomial (multinomial) | $x^3-2x^2+x-4$ |

So $x^2-4x+4$ is a **quadratic trinomial** and $x^3-8$ is a **cubic binomial**. Both names are needed to describe a polynomial fully.

```figure caption="Graphs of polynomial functions of degree 0, 1, 2 and 3. A constant gives a horizontal line, a linear polynomial a slanting line, a quadratic one bend (a parabola) and a cubic up to two bends."
fig, axs = plt.subplots(2, 2, figsize=(5.0, 3.6))
x = np.linspace(-2.4, 2.4, 300)
data = [(np.full_like(x, 2.0), 'degree 0 : f(x) = 2'), (x + 1, 'degree 1 : f(x) = x + 1'),
        (x**2 - 2, 'degree 2 : f(x) = x² − 2'), (x**3 - 3*x, 'degree 3 : f(x) = x³ − 3x')]
for ax, (y, title) in zip(axs.flat, data):
    ax.plot(x, y, color=ACCENT, lw=1.8)
    ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-3.5, 3.5)
    ax.set_xticks([-2, -1, 1, 2]); ax.set_yticks([-2, 2])
    ax.tick_params(labelsize=7.5, length=0)
    ax.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(title, fontsize=8.5, pad=3)
fig.tight_layout(pad=0.4)
```

::: example Naming polynomials
**Problem.** Name each polynomial by its degree and by its number of terms: (i) $5x-3$ (ii) $7x^3$ (iii) $x^2-4x+4$ (iv) $9$ (v) $x^4-x^2+2x-1$.

**Solution.**

| Polynomial | Degree | By degree | Terms | By terms |
|---|---|---|---|---|
| $5x-3$ | 1 | linear | 2 | binomial |
| $7x^3$ | 3 | cubic | 1 | monomial |
| $x^2-4x+4$ | 2 | quadratic | 3 | trinomial |
| $9$ | 0 | constant | 1 | monomial |
| $x^4-x^2+2x-1$ | 4 | biquadratic | 4 | polynomial |
:::

## 2.2 Degree of a polynomial, standard form and equal polynomials

### Degree when there is more than one variable

The **degree of a term** is the **sum of the powers** of all the variables in it. The degree of the polynomial is the largest degree among its terms.

| Term | Powers | Degree of the term |
|---|---|---|
| $3x^2y^3$ | $2+3$ | 5 |
| $-4xy$ | $1+1$ | 2 |
| $6x^4$ | 4 | 4 |
| $7$ | none | 0 |

::: example Degree of a polynomial in two variables
**Problem.** Find the degree of $x^2y+3xy^3-5x^2+8$.

**Solution.** Degrees of the terms: $x^2y\to2+1=3$; $3xy^3\to1+3=4$; $-5x^2\to2$; $8\to0$. The highest is 4, so the polynomial has **degree 4**.
:::

### Simplify before you state the degree

Like terms may hide the true degree. In $3x^3+2x-3x^3+5$ the two cubic terms cancel, leaving $2x+5$, which is **linear**. In the same way $(x+1)^2-x^2=x^2+2x+1-x^2=2x+1$ has degree 1, although a square appears in it. Always collect like terms first, then read the highest power that is left.

::: caution The degree is not the number of terms, nor the biggest coefficient
$x^2y+3xy^3-5x^2+8$ has 4 terms and degree 4, but $2x^5+100$ has 2 terms and degree 5. The coefficient 100 does not affect the degree at all. Look only at the powers of the variables. The polynomial $0$ (every coefficient zero) is called the **zero polynomial**; it has no degree.
:::

### Standard form

A polynomial is in **standard form** when its terms are written in **descending order of powers** (some books also accept ascending order). The first term in standard form is the **leading term**, and its coefficient is the **leading coefficient**.

::: example Writing in standard form
**Problem.** Write $3+2x-5x^2+x^3$ and $4x-7+2x^4-x^2$ in standard form, and give the degree, leading coefficient and constant term of each.

**Solution.**

| Standard form | Degree | Leading coefficient | Constant term |
|---|---|---|---|
| $x^3-5x^2+2x+3$ | 3 | 1 | 3 |
| $2x^4-x^2+4x-7$ | 4 | 2 | $-7$ |

The second polynomial has no $x^3$ term. In standard form we may show the gap as $2x^4+0x^3-x^2+4x-7$. This is useful when we add or multiply in columns.
:::

### Equal polynomials

::: definition Equal polynomials
Two polynomials in $x$ are **equal** when they have the same degree and the **coefficients of like powers are equal**. For example,
$$ ax^2+bx+c=px^2+qx+r \quad\Longleftrightarrow\quad a=p,\ b=q,\ c=r $$
:::

This is the polynomial version of equal ordered pairs: compare the coefficient of $x^2$ with the coefficient of $x^2$, the coefficient of $x$ with the coefficient of $x$, and the constants with each other.

::: example Unknown coefficients
**Problem.** If $(a-1)x^3+4x^2+(b+2)x+c=2x^3+4x^2-x+5$, find $a$, $b$ and $c$.

**Solution.** Compare coefficients of like powers.

$x^3$: $a-1=2$, so $a=3$.

$x^2$: $4=4$ (already equal).

$x$: $b+2=-1$, so $b=-3$.

Constant: $c=5$.
:::

::: example Equal polynomials giving two equations
**Problem.** Find $a$ and $b$ if $(a+b)x^2+(a-b)x+6=7x^2+3x+6$.

**Solution.** Coefficients of $x^2$: $a+b=7$. Coefficients of $x$: $a-b=3$. Adding the two equations, $2a=10$, so $a=5$, and then $b=7-5=2$.

**Check.** $(5+2)x^2+(5-2)x+6=7x^2+3x+6$. ✓
:::

## 2.3 Addition and subtraction of polynomials

Terms with the **same variable and the same power** are **like terms**: $3x^2$ and $-5x^2$ are like terms, but $3x^2$ and $3x$ are not. We can add or subtract only like terms, by adding or subtracting their coefficients:
$$ 3x^2+(-5x^2)=-2x^2, \qquad\text{but}\qquad 3x^2+3x \text{ cannot be combined.} $$

### Two methods of adding

**Horizontal method.** Write the polynomials side by side, group like terms and combine them.

**Vertical (column) method.** Write each polynomial in standard form, one below the other, with like terms in the same column. Leave a gap (or write 0) for a missing power. Then add each column.

::: example Adding by both methods
**Problem.** Add $3x^3-2x^2+5x-7$ and $x^3+4x^2-6$.

**Solution.** **Horizontal:**
$$ (3x^3+x^3)+(-2x^2+4x^2)+5x+(-7-6)=4x^3+2x^2+5x-13 $$
**Vertical:**

| | $x^3$ | $x^2$ | $x$ | constant |
|---|---|---|---|---|
| first | $3x^3$ | $-2x^2$ | $+5x$ | $-7$ |
| second | $x^3$ | $+4x^2$ | $+0x$ | $-6$ |
| sum | $4x^3$ | $+2x^2$ | $+5x$ | $-13$ |

Both methods give $4x^3+2x^2+5x-13$.
:::

Algebra tiles make addition visible. A large square stands for $x^2$, a long strip for $x$ and a small square for $1$; a red tile stands for a negative term. A positive strip and a negative strip together make nothing: they are a **zero pair**.

```figure caption="Adding $(2x^2+3x+1)+(x^2-2x+2)$ with algebra tiles. Like tiles are collected; each positive strip next to a negative strip is a zero pair and is removed. What is left is $3x^2+x+3$."
fig, ax = plt.subplots(figsize=(5.0, 3.3))
ax.set_xlim(0, 11.0); ax.set_ylim(-0.9, 5.7); ax.axis('off')
FC = {'x2': '#cfe3f6', 'x': '#d5efdf', '1': '#f7e7c4'}
EC = {'x2': ACCENT, 'x': SERIES[2], '1': SERIES[3]}
SZ = {'x2': (1.0, 1.0), 'x': (0.34, 1.0), '1': (0.34, 0.34)}
LB = {'x2': 'x²', 'x': 'x', '1': '1'}
def tile(x, y, kind, neg=False, struck=False):
    w, h = SZ[kind]
    ax.add_patch(Rectangle((x, y), w, h, fc=('#f6d2d0' if neg else FC[kind]), ec=(SERIES[1] if neg else EC[kind]), lw=1.1))
    ax.text(x + w/2, y + h/2, ('−' if neg else '') + LB[kind], ha='center', va='center', fontsize=(9 if kind == 'x2' else 7.5))
    if struck:
        ax.plot([x, x + w], [y, y + h], color=MUTED, lw=0.9)
    return x + w + 0.12
rows = [(4.4, '2x² + 3x + 1', [('x2', 0), ('x2', 0), ('x', 0), ('x', 0), ('x', 0), ('1', 0)]),
        (2.8, 'x² − 2x + 2', [('x2', 0), ('x', 1), ('x', 1), ('1', 0), ('1', 0)])]
for y, lab, tiles in rows:
    ax.text(0.0, y + 0.5, lab, fontsize=9, va='center')
    x = 2.6
    for kind, neg in tiles:
        x = tile(x, y, kind, bool(neg))
ax.plot([0, 10.9], [2.45, 2.45], color=GRID, lw=1.0)
y = 1.0
ax.text(0.0, y + 0.5, 'sum', fontsize=9, va='center')
x = 2.6
for k in range(3):
    x = tile(x, y, 'x2')
x = tile(x, y, 'x') + 0.15
pairs = []
for k in range(2):
    x0 = x
    x = tile(x, y, 'x', struck=True)
    x = tile(x, y, 'x', neg=True, struck=True)
    pairs.append((x0, x - 0.12))
    x += 0.35
for k in range(3):
    x = tile(x, y, '1')
for x0, x1 in pairs:
    ax.plot([x0, x0, x1, x1], [0.85, 0.7, 0.7, 0.85], color=MUTED, lw=0.9)
    ax.text((x0 + x1)/2, 0.32, '= 0', ha='center', fontsize=8, color=MUTED)
ax.text(0.0, -0.55, 'each bracket is a zero pair, x + (−x) = 0;  left over:  3x² + x + 3', fontsize=9, color=INK)
```

### Subtraction

To subtract a polynomial, **change the sign of every one of its terms** and then add. This works because subtracting a term is the same as adding its negative.

::: example Subtracting one polynomial from another
**Problem.** Subtract $2x^2-5x+3$ from $5x^2+x-4$.

**Solution.** "Subtract A from B" means $B-A$:
$$ (5x^2+x-4)-(2x^2-5x+3)=5x^2+x-4-2x^2+5x-3 $$
$$ =(5x^2-2x^2)+(x+5x)+(-4-3)=3x^2+6x-7 $$
:::

::: caution A minus sign in front of a bracket changes every sign inside
$-(2x^2-5x+3)=-2x^2+5x-3$. Changing only the first sign, to get $-2x^2-5x+3$, is the most common mistake in this chapter. Also read the order carefully: "subtract $A$ from $B$" is $B-A$, not $A-B$.
:::

::: example Three polynomials at once
**Problem.** If $f(x)=2x^3-x+4$, $g(x)=x^3+3x^2-2x-1$ and $h(x)=-x^2+5$, find $f(x)+g(x)-h(x)$.

**Solution.**
$$ f+g-h=(2x^3-x+4)+(x^3+3x^2-2x-1)-(-x^2+5) $$
$$ =2x^3-x+4+x^3+3x^2-2x-1+x^2-5 $$
$$ =3x^3+4x^2-3x-2 $$
**Check at $x=1$.** $f(1)=5$, $g(1)=1$, $h(1)=4$, so $f+g-h=5+1-4=2$; and $3+4-3-2=2$. ✓
:::

::: example What must be added?
**Problem.** What must be added to $x^3-2x^2+3$ to get $2x^3+x-1$?

**Solution.** The missing polynomial is the **target minus the given one**:
$$ (2x^3+x-1)-(x^3-2x^2+3)=2x^3+x-1-x^3+2x^2-3=x^3+2x^2+x-4 $$
**Check.** $(x^3-2x^2+3)+(x^3+2x^2+x-4)=2x^3+x-1$. ✓
:::

::: example Perimeter as a polynomial
**Problem.** The sides of a triangle are $(x^2+2x)$ cm, $(2x^2-x+1)$ cm and $(3x+2)$ cm. Find its perimeter, and its value when $x=2$.

**Solution.** Perimeter $=(x^2+2x)+(2x^2-x+1)+(3x+2)=3x^2+4x+3$ cm.

When $x=2$: $3(4)+4(2)+3=12+8+3=23$ cm. The sides are then 8 cm, 7 cm and 8 cm, which add to 23 cm. ✓
:::

When two polynomials are added, the degree of the sum is never more than the larger degree, and it can be less if the leading terms cancel: $(x^2+3x)+(-x^2+2)=3x+2$ has degree 1.

### Properties of addition

Because polynomials are added by adding numbers (their coefficients), they obey the same laws as numbers. For any polynomials $p(x)$, $q(x)$ and $r(x)$:

| Property | Statement |
|---|---|
| Closure | $p(x)+q(x)$ is again a polynomial |
| Commutative | $p(x)+q(x)=q(x)+p(x)$ |
| Associative | $[p(x)+q(x)]+r(x)=p(x)+[q(x)+r(x)]$ |
| Identity | $p(x)+0=p(x)$; the zero polynomial changes nothing |
| Inverse | $p(x)+[-p(x)]=0$, where $-p(x)$ has every sign changed |

The inverse property is the reason subtraction works by changing signs: subtracting $q(x)$ is adding its inverse $-q(x)$.

::: example Profit as the difference of two polynomials
**Problem.** A momo stall in Pokhara sells a plate for Rs 150. Its daily cost is Rs 60 per plate for ingredients plus Rs 1,200 for rent and gas. Write the revenue, the cost and the profit for $x$ plates as polynomials, and find the profit on a day when 50 plates are sold.

**Solution.** Revenue $R(x)=150x$ and cost $C(x)=60x+1200$. Profit is revenue minus cost:
$$ P(x)=R(x)-C(x)=150x-(60x+1200)=90x-1200 $$
For 50 plates: $P(50)=90	imes50-1200=4500-1200=$ Rs 3,300.

The stall makes a profit only when $90x>1200$, that is when $x>13.3$; it must sell **at least 14 plates** a day to cover its costs.
:::

## 2.4 Multiplication of polynomials

Multiplication uses two tools you already know: the **laws of indices** ($x^m\times x^n=x^{m+n}$) and the **distributive law** ($a(b+c)=ab+ac$).

### Monomial times monomial, and monomial times polynomial

Multiply the coefficients and add the powers of each variable:
$$ (3x^2)(-4x^3)=-12x^5, \qquad (2x^2y)(5xy^3)=10x^3y^4 $$
To multiply a polynomial by a monomial, multiply **every term** by the monomial:
$$ 2x(3x^2-4x+5)=6x^3-8x^2+10x $$

### Binomial times binomial

Each term of the first bracket multiplies each term of the second, giving four products. The area of a rectangle shows why.

```figure caption="The area model for $(x+3)(x+2)$. The rectangle of sides $x+3$ and $x+2$ splits into four parts, $x^2$, $3x$, $2x$ and $6$, so $(x+3)(x+2)=x^2+5x+6$."
fig, ax = plt.subplots(figsize=(4.6, 3.2))
X, A, B = 3.0, 1.5, 1.0
parts = [((0, B), X, X, 'x²', '#cfe3f6'), ((X, B), A, X, '3x', '#d5efdf'),
         ((0, 0), X, B, '2x', '#d5efdf'), ((X, 0), A, B, '6', '#f7e7c4')]
for (x0, y0), w, h, lab, c in parts:
    ax.add_patch(Rectangle((x0, y0), w, h, fc=c, ec=INK, lw=1.1))
    ax.text(x0 + w/2, y0 + h/2, lab, ha='center', va='center', fontsize=12)
ax.text(X/2, X + B + 0.22, 'x', ha='center', fontsize=10.5)
ax.text(X + A/2, X + B + 0.22, '3', ha='center', fontsize=10.5)
ax.text(-0.25, B + X/2, 'x', ha='center', va='center', fontsize=10.5)
ax.text(-0.25, B/2, '2', ha='center', va='center', fontsize=10.5)
ax.annotate('', xy=(X + A, X + B + 0.65), xytext=(0, X + B + 0.65), arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9))
ax.text((X + A)/2, X + B + 0.8, 'x + 3', ha='center', fontsize=9, color=MUTED)
ax.annotate('', xy=(-0.7, X + B), xytext=(-0.7, 0), arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9))
ax.text(-0.85, (X + B)/2, 'x + 2', ha='right', va='center', fontsize=9, color=MUTED, rotation=90)
ax.text((X + A)/2, -0.45, 'area = x² + 3x + 2x + 6 = x² + 5x + 6', ha='center', fontsize=9.5, color=INK)
ax.set_xlim(-1.4, X + A + 0.4); ax.set_ylim(-0.8, X + B + 1.2)
ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Two binomials
**Problem.** Multiply (i) $(x+3)(x+2)$ (ii) $(2x+3)(x-5)$.

**Solution.** (i) $(x+3)(x+2)=x\cdot x+x\cdot2+3\cdot x+3\cdot2=x^2+2x+3x+6=x^2+5x+6$.

(ii) $(2x+3)(x-5)=2x^2-10x+3x-15=2x^2-7x-15$.

**Check (ii) at $x=1$.** Left: $(5)(-4)=-20$. Right: $2-7-15=-20$. ✓
:::

### Polynomial times polynomial

Multiply every term of the first polynomial by every term of the second, then collect like terms. If the first has 3 terms and the second has 2, there are $3\times2=6$ products before collecting. A grid keeps them in order.

```figure caption="The grid (box) method for $(2x^2-x+3)(x+4)$. Each cell is the product of its row and column headings. Cells of the same colour are like terms: $8x^2-x^2=7x^2$ and $3x-4x=-x$. The product is $2x^3+7x^2-x+12$."
fig, ax = plt.subplots(figsize=(4.8, 2.7))
cols = ['2x²', '− x', '+ 3']; rows = ['x', '+ 4']
cells = [['2x³', '− x²', '+ 3x'], ['+ 8x²', '− 4x', '+ 12']]
tint = {'2x³': '#eeeeee', '− x²': '#cfe3f6', '+ 8x²': '#cfe3f6', '+ 3x': '#d5efdf', '− 4x': '#d5efdf', '+ 12': '#f7e7c4'}
w, h = 1.3, 0.8
for j, c in enumerate(cols):
    ax.text(1.0 + j*w + w/2, 2*h + 0.28, c, ha='center', va='center', fontsize=10.5, color=ACCENT)
for i, r in enumerate(rows):
    ax.text(0.55, (1 - i)*h + h/2, r, ha='center', va='center', fontsize=10.5, color=SERIES[1])
for i in range(2):
    for j in range(3):
        v = cells[i][j]
        ax.add_patch(Rectangle((1.0 + j*w, (1 - i)*h), w, h, fc=tint[v], ec=INK, lw=1.0))
        ax.text(1.0 + j*w + w/2, (1 - i)*h + h/2, v, ha='center', va='center', fontsize=10.5)
ax.text(5.15, 1.15, 'collect like terms:', fontsize=8.5, color=MUTED)
ax.text(5.15, 0.65, '2x³ + 7x² − x + 12', fontsize=10, color=INK)
ax.set_xlim(0, 7.8); ax.set_ylim(-0.15, 2.25); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example A trinomial times a binomial
**Problem.** Find the product $(x^2+2x-1)(x-3)$ and state its degree.

**Solution.** Multiply each term of the first bracket by $x$ and then by $-3$:
$$ (x^2+2x-1)(x-3)=x^3+2x^2-x-3x^2-6x+3 $$
$$ =x^3-x^2-7x+3 $$
The product has **degree 3**. A degree-2 polynomial times a degree-1 polynomial gives degree $2+1=3$.

**Check at $x=2$.** Left: $(4+4-1)(2-3)=7\times(-1)=-7$. Right: $8-4-14+3=-7$. ✓
:::

### The column method, and why it works

Polynomials can also be multiplied in columns, exactly like long multiplication of numbers. Write the longer polynomial on top, multiply it by each term of the lower one on a separate line, keep like powers in the same column, and add.

| | $x^3$ | $x^2$ | $x$ | constant |
|---|---|---|---|---|
| top | | $x^2$ | $+2x$ | $+1$ |
| bottom | | | $x$ | $+3$ |
| $	imes3$ | | $3x^2$ | $+6x$ | $+3$ |
| $	imes x$ | $x^3$ | $+2x^2$ | $+x$ | |
| product | $x^3$ | $+5x^2$ | $+7x$ | $+3$ |

So $(x^2+2x+1)(x+3)=x^3+5x^2+7x+3$. Now put $x=10$: the top becomes 121, the bottom 13, and the product $1000+500+70+3=1573$. Indeed $121	imes13=1573$. Multiplying polynomials **is** long multiplication; the only difference is that the columns never carry, because $x$ is not fixed at 10.

::: key Degree of a product
If $f(x)$ has degree $m$ and $g(x)$ has degree $n$, then $f(x)\cdot g(x)$ has degree $m+n$, because the leading terms multiply to give the highest power: $x^m\cdot x^n=x^{m+n}$.
:::

::: example Products that collapse
**Problem.** Find (i) $(x+2)(x^2-2x+4)$ and (ii) $(x^2-3)(x^2+2x-1)$.

**Solution.** (i)
$$ (x+2)(x^2-2x+4)=x^3-2x^2+4x+2x^2-4x+8=x^3+8 $$
Four of the six products cancel in pairs. This is the pattern $(a+b)(a^2-ab+b^2)=a^3+b^3$.

(ii)
$$ (x^2-3)(x^2+2x-1)=x^4+2x^3-x^2-3x^2-6x+3=x^4+2x^3-4x^2-6x+3 $$
The degree is $2+2=4$.
:::

### Special products

These products occur so often that they are worth remembering.

| Identity | Example |
|---|---|
| $(a+b)^2=a^2+2ab+b^2$ | $(x+5)^2=x^2+10x+25$ |
| $(a-b)^2=a^2-2ab+b^2$ | $(2x-3)^2=4x^2-12x+9$ |
| $(a+b)(a-b)=a^2-b^2$ | $(x+4)(x-4)=x^2-16$ |
| $(x+a)(x+b)=x^2+(a+b)x+ab$ | $(x+3)(x-7)=x^2-4x-21$ |

::: caution The square of a sum is not the sum of the squares
$(x+3)^2$ is $(x+3)(x+3)=x^2+6x+9$, not $x^2+9$. The middle term $2ab$ is the part students forget. Put $x=1$ to see it: $(1+3)^2=16$, but $1+9=10$.
:::

::: example Area of a rectangle as a polynomial
**Problem.** A rectangular plot is $(3x+2)$ m long and $(2x-1)$ m wide. Find its area as a polynomial, and the area when $x=3$.

**Solution.** Area $=(3x+2)(2x-1)=6x^2-3x+4x-2=6x^2+x-2$ square metres.

When $x=3$: $6(9)+3-2=55$ m². Directly, the sides are $11$ m and $5$ m, and $11\times5=55$ m². ✓
:::

::: tip Check every answer with a number
After adding, subtracting or multiplying, put a small number such as $x=1$ or $x=2$ into the question and into your answer. If the two values are different, there is a mistake. The check takes thirty seconds and catches almost every sign error.
:::

::: note Activity — make your own algebra tiles
Cut tiles from card: large squares for $x^2$, long strips for $x$ (as long as the side of the square) and small squares for 1. Colour the back of each tile red for negative terms. (1) Show $(2x^2+3x+1)+(x^2-2x+2)$ and remove zero pairs. (2) Build a rectangle with sides $x+3$ and $x+2$ from one $x^2$ tile, five strips and six small squares, and read off $(x+3)(x+2)=x^2+5x+6$. (3) Try to build a rectangle from one $x^2$ tile, four strips and three small squares. What two sides does it have?
:::

## Chapter summary

- A **polynomial** has only whole-number powers of its variables; negative or fractional powers, roots of the variable and variables in a denominator are not allowed.
- **Degree** = highest power of the variable (for several variables, the highest sum of powers in a term); a non-zero constant has degree 0.
- By degree: constant (0), linear (1), quadratic (2), cubic (3), biquadratic (4). By terms: monomial, binomial, trinomial, polynomial.
- **Standard form**: descending powers; the first coefficient is the **leading coefficient**.
- **Equal polynomials** have equal coefficients of like powers: compare $x^2$ with $x^2$, $x$ with $x$, constant with constant.
- Add or subtract only **like terms**; to subtract, change the sign of **every** term being subtracted.
- Multiply every term by every term; the degree of a product is the sum of the degrees.
- $(a\pm b)^2=a^2\pm2ab+b^2$, $(a+b)(a-b)=a^2-b^2$; check any answer by substituting a number.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these is a polynomial? <span class="marks">[1]</span>
   (a) $x+\frac{1}{x}$ (b) $\sqrt{x}+3$ (c) $2x^2-3x+1$ (d) $x^{-2}+5$
2. The degree of $4x^3-7x^5+2x-9$ is <span class="marks">[1]</span>
   (a) 3 (b) 5 (c) 4 (d) 9
3. A polynomial of degree 2 is called <span class="marks">[1]</span>
   (a) linear (b) quadratic (c) cubic (d) biquadratic
4. The polynomial $x^3-8$ is a <span class="marks">[1]</span>
   (a) monomial (b) binomial (c) trinomial (d) quadratic
5. The degree of the term $5x^2y^3$ is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 5 (d) 6
6. The constant term of $3x^3-2x+7$ is <span class="marks">[1]</span>
   (a) 3 (b) $-2$ (c) 7 (d) 0
7. If $f(x)=x^2-2x+3$, then $f(2)$ is <span class="marks">[1]</span>
   (a) 3 (b) 11 (c) 0 (d) 5
8. If $ax^2+5x+1=3x^2+bx+1$, then $a+b$ is <span class="marks">[1]</span>
   (a) 8 (b) 2 (c) 15 (d) 6
9. $(3x^2+2x)+(x^2-5x)$ equals <span class="marks">[1]</span>
   (a) $4x^2-3x$ (b) $4x^2+7x$ (c) $3x^2-3x$ (d) $4x^4-3x^2$
10. $(5x-3)-(2x-7)$ equals <span class="marks">[1]</span>
    (a) $3x-10$ (b) $3x+4$ (c) $7x+4$ (d) $3x-4$
11. $(x+4)(x-4)$ equals <span class="marks">[1]</span>
    (a) $x^2+16$ (b) $x^2-8x-16$ (c) $x^2-16$ (d) $x^2+8x-16$
12. If $f(x)$ has degree 3 and $g(x)$ has degree 2, the degree of $f(x)\cdot g(x)$ is <span class="marks">[1]</span>
    (a) 5 (b) 6 (c) 3 (d) 1

::: note Answers to Group A
**1.** (c) — the others contain $x^{-1}$, $x^{\frac{1}{2}}$ or $x^{-2}$.
**2.** (b) — the highest power is $x^5$.
**3.** (b) — degree 2 is quadratic.
**4.** (b) — two terms, $x^3$ and $-8$.
**5.** (c) — $2+3=5$.
**6.** (c) — the term without $x$ is 7.
**7.** (a) — $4-4+3=3$.
**8.** (a) — $a=3$ and $b=5$, so $a+b=8$.
**9.** (a) — $3x^2+x^2=4x^2$ and $2x-5x=-3x$.
**10.** (b) — $5x-3-2x+7=3x+4$.
**11.** (c) — $(a+b)(a-b)=a^2-b^2$.
**12.** (a) — degrees add: $3+2=5$.
:::

**Group B — Short answer (2 marks each)**

1. Write $7-3x^2+5x^4-x$ in standard form and state its degree and leading coefficient. <span class="marks">[2]</span>
2. State, with a reason, whether each is a polynomial: (i) $3x^2-\sqrt{2}\,x+1$ (ii) $2x+\frac{3}{x}$. <span class="marks">[2]</span>
3. If $f(x)=2x^3-3x+1$, find $f(-1)$ and $f(2)$. <span class="marks">[2]</span>
4. Find $a$ and $b$ if $(a+2)x^2+3x-4=5x^2+(b-1)x-4$. <span class="marks">[2]</span>
5. Add $4x^3-2x^2+x-5$ and $-x^3+5x^2-3x+2$. <span class="marks">[2]</span>
6. Subtract $3x^2-4x+1$ from $x^2+2x-6$. <span class="marks">[2]</span>
7. Multiply $(3x-2)(2x+5)$. <span class="marks">[2]</span>
8. Multiply $(-2x^2y)(3xy^2-4y)$. <span class="marks">[2]</span>
9. Find the degree of $x^3y^2-4x^4+2xy$. <span class="marks">[2]</span>
10. What must be subtracted from $5x^2-3x+2$ to get $2x^2+x-1$? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $5x^4-3x^2-x+7$; degree 4; leading coefficient 5.
**2.** (i) Yes: the powers of $x$ are 2, 1 and 0; the coefficient $\sqrt{2}$ is allowed. (ii) No: $\frac{3}{x}=3x^{-1}$ has a negative power of $x$.
**3.** $f(-1)=2(-1)-3(-1)+1=-2+3+1=2$; $f(2)=16-6+1=11$.
**4.** $x^2$: $a+2=5$, so $a=3$. $x$: $3=b-1$, so $b=4$.
**5.** $(4-1)x^3+(-2+5)x^2+(1-3)x+(-5+2)=3x^3+3x^2-2x-3$.
**6.** $(x^2+2x-6)-(3x^2-4x+1)=x^2+2x-6-3x^2+4x-1=-2x^2+6x-7$.
**7.** $6x^2+15x-4x-10=6x^2+11x-10$.
**8.** $(-2x^2y)(3xy^2)+(-2x^2y)(-4y)=-6x^3y^3+8x^2y^2$.
**9.** Term degrees: $x^3y^2\to5$, $-4x^4\to4$, $2xy\to2$. The degree is **5**.
**10.** $(5x^2-3x+2)-(2x^2+x-1)=3x^2-4x+3$. Check: $(5x^2-3x+2)-(3x^2-4x+3)=2x^2+x-1$ ✓.
:::

**Group C — Long answer (4 marks each)**

1. If $f(x)=2x^3-5x^2+3$, $g(x)=x^3+2x-4$ and $h(x)=-3x^2+x+1$, find (i) $f(x)+g(x)-h(x)$ (ii) $f(x)-2g(x)$. <span class="marks">[4]</span>
2. Multiply $(x^2-3x+2)(2x-1)$, state the degree of the product, and verify your answer by putting $x=3$. <span class="marks">[4]</span>
3. Find $p$, $q$ and $r$ if $(p+q)x^2+(p-q)x+(r-1)=8x^2+2x+4$. Write the polynomial and find its value at $x=-1$. <span class="marks">[4]</span>
4. A rectangular garden is $(2x+5)$ m long and $(x+3)$ m wide. (i) Find its area and its perimeter as polynomials. (ii) Find the area and the perimeter when $x=4$. <span class="marks">[4]</span>
5. Show that $(x+2)(x^2-2x+4)-(x-2)(x^2+2x+4)=16$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) $f+g-h=2x^3-5x^2+3+x^3+2x-4+3x^2-x-1=3x^3-2x^2+x-2$. (ii) $2g(x)=2x^3+4x-8$, so $f-2g=2x^3-5x^2+3-2x^3-4x+8=-5x^2-4x+11$. Check (i) at $x=1$: $f(1)=0$, $g(1)=-1$, $h(1)=-1$, so $0-1+1=0$; and $3-2+1-2=0$ ✓.
**2.** $(x^2-3x+2)(2x-1)=2x^3-x^2-6x^2+3x+4x-2=2x^3-7x^2+7x-2$; degree $2+1=3$. At $x=3$: left $=(9-9+2)(6-1)=2\times5=10$; right $=54-63+21-2=10$ ✓.
**3.** $x^2$: $p+q=8$; $x$: $p-q=2$. Adding, $2p=10$, so $p=5$ and $q=3$. Constant: $r-1=4$, so $r=5$. The polynomial is $8x^2+2x+4$, and at $x=-1$ its value is $8-2+4=10$.
**4.** (i) Area $=(2x+5)(x+3)=2x^2+6x+5x+15=2x^2+11x+15$ m². Perimeter $=2[(2x+5)+(x+3)]=2(3x+8)=6x+16$ m. (ii) At $x=4$: area $=32+44+15=91$ m² and perimeter $=24+16=40$ m. Check: the sides are 13 m and 7 m; $13\times7=91$ ✓ and $2(13+7)=40$ ✓.
**5.** $(x+2)(x^2-2x+4)=x^3-2x^2+4x+2x^2-4x+8=x^3+8$. $(x-2)(x^2+2x+4)=x^3+2x^2+4x-2x^2-4x-8=x^3-8$. The difference is $(x^3+8)-(x^3-8)=16$, whatever the value of $x$.
:::

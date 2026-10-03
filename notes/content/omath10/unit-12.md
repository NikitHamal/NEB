---
subject: Optional Mathematics
grade: 10
unit: 12
title: Functions and Polynomials
hours: 0
area: Units
---

A vending machine gives exactly one drink for each button you press. A shop gives exactly one price for each item. The area of a square is fixed once its side is known. In each case, one quantity **determines** another in a definite way. Mathematics calls such a rule a **function**. Functions are the language in which the rest of mathematics is written, and the polynomial functions, built only from additions and multiplications of $x$, are the simplest and most useful family. This chapter first studies relations and functions, their domain and range, composite and inverse functions and their graphs, and then turns to polynomials: how to divide them, how to find the remainder without dividing, and how to use the **factor theorem** to break a polynomial into factors and find its zeros.

::: key What the SEE asks from this chapter
Expect 3 to 6 marks. Common types: (i) find the domain and range of a relation or function; (ii) find $f(a)$ or solve $f(x)=k$; (iii) find $f\circ g$ and $g\circ f$; (iv) find the inverse $f^{-1}(x)$; (v) find the remainder using the remainder theorem; (vi) show that $x-a$ is a factor and factorise a cubic; (vii) find an unknown constant so that a given binomial is a factor. Show the rule, the substitution and the check.
:::

## 12.1 Relations

A **relation** from a set $A$ to a set $B$ is any set of ordered pairs $(x,y)$ with $x\in A$ and $y\in B$. We say $x$ is **related** to $y$. For example, let $A=\{1,2,3\}$ and $B=\{2,3,4,5\}$ and let the relation be "$y$ is one more than $x$". The ordered pairs are

$$ R=\{(1,2),\ (2,3),\ (3,4)\}. $$

::: definition Domain and range of a relation
The set of all first components of the ordered pairs is the **domain**. The set of all second components is the **range**. The whole set $B$ into which the pairs may fall is the **codomain**.
:::

For the relation $R$ above the domain is $\{1,2,3\}$, the range is $\{2,3,4\}$ and the codomain is $\{2,3,4,5\}$. Notice that 5 belongs to the codomain but not to the range, because nobody in $A$ is sent to 5. The range is always a subset of the codomain.

::: example Domain and range from ordered pairs
**Problem.** Write the relation $R=\{(x,y): y=2x-1,\ x\in\{1,2,3,4\}\}$ as a set of ordered pairs and state its domain and range.

**Solution.** For $x=1,2,3,4$ we get $y=1,3,5,7$. So

$$ R=\{(1,1),\ (2,3),\ (3,5),\ (4,7)\}. $$

Domain $=\{1,2,3,4\}$ and range $=\{1,3,5,7\}$.
:::

::: example A relation that is not a function
**Problem.** Let $S=\{(1,2),(1,3),(2,4),(3,4)\}$. State its domain and range. Does every element of the domain have only one image?

**Solution.** The domain is $\{1,2,3\}$ and the range is $\{2,3,4\}$. The element 1 has **two** images, 2 and 3, so $S$ is a relation but not a function (see the next section).
:::

## 12.2 Functions

::: definition Function
A relation from $A$ to $B$ is a **function** if **every element of $A$ is related to exactly one element of $B$**. We write $f:A\to B$ and $y=f(x)$, read "$y$ equals $f$ of $x$". Here $x$ is the **independent variable** (input) and $y=f(x)$ is the **image** of $x$ (output).
:::

Two conditions must both hold: no element of the domain is left without an image, and no element has two images. Different elements may share the same image, as in $\{(1,4),(2,4),(3,5)\}$, which is a function.

```figure caption="A function as an arrow diagram. Every element of $A$ sends exactly one arrow to $B$ (left). In the relation on the right, the element $1$ sends two arrows, so it is not a function."
fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.6))
def draw(ax, left, right, arrows, title):
    for i, v in enumerate(left):
        ax.text(0.2, 3 - i, str(v), ha='center', va='center', fontsize=9, color=ACCENT)
    for i, v in enumerate(right):
        ax.text(1.8, 3 - i, str(v), ha='center', va='center', fontsize=9, color=SERIES[1])
    for a, b in arrows:
        ax.annotate('', xy=(1.65, 3 - right.index(b)), xytext=(0.35, 3 - left.index(a)),
                    arrowprops=dict(arrowstyle='->', color='#444', lw=0.9))
    ax.set_xlim(-0.1, 2.1); ax.set_ylim(-0.6, 3.6); ax.axis('off')
    ax.set_title(title, fontsize=8.5)
draw(axs[0], [1, 2, 3], [4, 5, 6, 7], [(1, 4), (2, 4), (3, 6)], 'function')
draw(axs[1], [1, 2, 3], [4, 5, 6, 7], [(1, 4), (1, 5), (2, 6)], 'not a function')
fig.tight_layout(pad=0.4)
```

### The vertical line test

When a relation is drawn as a graph, every vertical line meets the graph of a function **at most once** (a vertical line through an element of the domain meets it exactly once). If some vertical line cuts the graph twice, one $x$ has two images and the graph is not that of a function. The parabola $y=x^2$ passes the test; the sideways parabola $x=y^2$ fails it.

### Finding values of a function

::: example Value of a function
**Problem.** If $f(x)=2x+3$, find $f(4)$, $f(-1)$ and the value of $x$ for which $f(x)=15$.

**Solution.** $f(4)=2\times 4+3=11$ and $f(-1)=2\times(-1)+3=1$.

For $f(x)=15$: $2x+3=15$, so $2x=12$ and $x=6$.
:::

::: example A quadratic function
**Problem.** If $f(x)=x^2-3x+2$, find $f(3)$, $f(-2)$ and the values of $x$ for which $f(x)=0$.

**Solution.** $f(3)=9-9+2=2$ and $f(-2)=4+6+2=12$.

$f(x)=0$ gives $x^2-3x+2=0$, so $(x-1)(x-2)=0$ and $x=1$ or $x=2$.
:::

::: example Substituting an expression
**Problem.** If $f(x)=3x-5$, find $f(a+2)$ and show that $f(a+2)-f(a)=6$.

**Solution.** $f(a+2)=3(a+2)-5=3a+1$. Also $f(a)=3a-5$. So $f(a+2)-f(a)=(3a+1)-(3a-5)=6$.
:::

::: example Finding the rule from two values
**Problem.** A linear function $f(x)=ax+b$ has $f(1)=5$ and $f(3)=11$. Find $f(x)$ and $f(10)$.

**Solution.** $a+b=5$ and $3a+b=11$. Subtracting, $2a=6$, so $a=3$ and $b=2$. Hence $f(x)=3x+2$ and $f(10)=32$.
:::

## 12.3 Domain and range of a function

The **domain** of $f$ is the set of all inputs for which the rule makes sense; the **range** is the set of all outputs actually produced. If the domain is not stated, it is the largest set of real numbers for which $f(x)$ is defined. Two things can go wrong: **dividing by zero** and taking the **square root of a negative number**.

::: key Finding the natural domain
- For $\frac{1}{g(x)}$, exclude every $x$ with $g(x)=0$.
- For $\sqrt{g(x)}$, require $g(x)\geq 0$.
- A polynomial is defined for every real $x$, so its domain is $\mathbb{R}$.
:::

::: example Domain of simple functions
**Problem.** Find the domain of (i) $f(x)=\frac{1}{x-3}$, (ii) $g(x)=\sqrt{x-2}$, (iii) $h(x)=\frac{x}{x^2-9}$.

**Solution.** (i) $x-3\neq 0$, so the domain is all real numbers except 3, written $\{x\in\mathbb{R}: x\neq 3\}$.

(ii) We need $x-2\geq 0$, so the domain is $\{x\in\mathbb{R}: x\geq 2\}$.

(iii) $x^2-9\neq 0$ means $x\neq 3$ and $x\neq -3$. The domain is $\mathbb{R}$ without $\{3,-3\}$.
:::

::: example Range from a table of values
**Problem.** Let $f(x)=x^2+1$ with domain $\{-2,-1,0,1,2\}$. Find the range.

**Solution.** $f(-2)=5$, $f(-1)=2$, $f(0)=1$, $f(1)=2$, $f(2)=5$. The range is $\{1,2,5\}$. Two inputs share each of the images 2 and 5, which is allowed.
:::

::: example Domain and range of a square-root function
**Problem.** Find the domain and range of $f(x)=\sqrt{x-2}$.

**Solution.** Domain: $x\geq 2$. As $x$ takes values from 2 upwards, $x-2$ takes all values from 0 upwards, and its square root also takes all values from 0 upwards. So the range is $\{y: y\geq 0\}$.
:::

### Reading domain and range from a graph

The domain is the set of $x$-values covered by the graph, read **along the $x$-axis**; the range is the set of $y$-values covered, read **along the $y$-axis**. For a linear function $f(x)=mx+c$ both are all real numbers. For a quadratic $f(x)=ax^2+bx+c$ the domain is all real numbers, but the range stops at the **vertex**: it is $y\geq y_{\min}$ if $a>0$ and $y\leq y_{\max}$ if $a<0$. The vertex of $y=ax^2+bx+c$ lies at $x=-\frac{b}{2a}$.

::: example Domain and range of a quadratic
**Problem.** For $f(x)=x^2-4x+3$ find the zeros, the vertex, and the range. Draw the graph.

**Solution.** $x^2-4x+3=(x-1)(x-3)$, so the zeros are $x=1$ and $x=3$. The vertex is at $x=-\frac{-4}{2}=2$, and $f(2)=4-8+3=-1$, so it is $(2,-1)$. Since the coefficient of $x^2$ is positive, the parabola opens upwards and the lowest value is $-1$. The domain is all real numbers and the range is $\{y: y\geq -1\}$.

Table: $x=0,1,2,3,4$ give $f(x)=3,0,-1,0,3$.
:::

```figure caption="The graph of $f(x)=x^2-4x+3$. The vertex is $(2,-1)$, so the range is $y\geq -1$. The parabola crosses the $x$-axis at $x=1$ and $x=3$. Every vertical line meets it once, so it is a function; but a horizontal line such as $y=3$ meets it twice, so it is not one-one."
x = np.linspace(-0.4, 4.4, 100)
y = x**2 - 4*x + 3
fig, ax = plt.subplots(figsize=(4.4, 3.0))
ax.plot(x, y, color=ACCENT, lw=1.5)
ax.plot([1, 3], [0, 0], 'o', color=SERIES[1], ms=5)
ax.plot([2], [-1], 's', color='#222', ms=4.5)
ax.text(2.1, -1.35, 'vertex (2, -1)', fontsize=8)
ax.axhline(3, color='#999', lw=0.8, ls='--')
ax.text(-0.3, 3.25, 'y = 3', fontsize=8, color='#666')
ax.axhline(0, color='#333', lw=0.6)
ax.set_xlim(-0.5, 4.5); ax.set_ylim(-2, 5.5)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('f(x)', fontsize=8.5)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Domain with a root and a fraction
**Problem.** Find the domain of $f(x)=\frac{\sqrt{x+3}}{x-1}$.

**Solution.** The root needs $x+3\geq 0$, that is $x\geq -3$. The denominator needs $x\neq 1$. So the domain is $\{x: x\geq -3,\ x\neq 1\}$.
:::

::: example A function in daily life
**Problem.** The temperature in degrees Fahrenheit is $F=f(C)=\frac{9}{5}C+32$ where $C$ is the temperature in degrees Celsius. Find $f(37)$, find the inverse function, and use it to convert $212^\circ$F.

**Solution.** $f(37)=\frac{9}{5}\times 37+32=66.6+32=98.6$, so $37^\circ$C is $98.6^\circ$F.

Put $F=\frac{9}{5}C+32$. Then $\frac{9}{5}C=F-32$ and $C=\frac{5}{9}(F-32)$. So $f^{-1}(F)=\frac{5(F-32)}{9}$ and $f^{-1}(212)=\frac{5\times 180}{9}=100$. Water boils at $100^\circ$C.
:::
### Kinds of function

| Kind | Meaning | Example |
| --- | --- | --- |
| One-one (injective) | different inputs give different outputs | $f(x)=2x+1$ |
| Many-one | some different inputs share an output | $f(x)=x^2$ |
| Onto (surjective) | range equals codomain | $f(x)=x+3$ on $\mathbb{R}\to\mathbb{R}$ |
| Constant | every input has the same output | $f(x)=4$ |
| Identity | output equals input | $I(x)=x$ |

A function that is both one-one and onto is called a **one-one correspondence** (bijection). Only such functions have an inverse, as we see in Section 12.5. To test whether a graph is one-one use the **horizontal line test**: no horizontal line may cut the graph more than once.

::: example Is it one-one?
**Problem.** Are $f(x)=3x-1$ and $g(x)=x^2$ (on $\mathbb{R}$) one-one?

**Solution.** Suppose $f(a)=f(b)$. Then $3a-1=3b-1$, so $a=b$: $f$ is one-one. But $g(2)=4=g(-2)$ with $2\neq -2$, so $g$ is many-one.
:::

## 12.4 Composite functions

If a machine $g$ turns $x$ into $g(x)$ and a second machine $f$ then acts on that result, the two machines together form one new function.

::: definition Composite function
For functions $g:A\to B$ and $f:B\to C$ the **composite function** $f\circ g:A\to C$ is defined by
$$ (f\circ g)(x)=f\big(g(x)\big). $$
First apply $g$, then apply $f$ to the result.
:::

Read $f\circ g$ as "$f$ of $g$" or "$f$ after $g$". The function nearest to $x$ acts first.

::: example Composite of two functions
**Problem.** If $f(x)=2x+1$ and $g(x)=x^2$, find $f\circ g$, $g\circ f$, and the values $(f\circ g)(3)$ and $(g\circ f)(3)$.

**Solution.** $(f\circ g)(x)=f(x^2)=2x^2+1$.

$(g\circ f)(x)=g(2x+1)=(2x+1)^2=4x^2+4x+1$.

$(f\circ g)(3)=2\times 9+1=19$ and $(g\circ f)(3)=7^2=49$. The two answers differ, so in general $f\circ g\neq g\circ f$: **composition is not commutative**.
:::

::: caution Common mistakes
- Mixing the order: $f\circ g$ means $g$ first, then $f$.
- Writing $f(g(x))=f(x)\cdot g(x)$. A composite is a substitution, not a product.
- Forgetting to expand $(2x+1)^2$ as $4x^2+4x+1$.
:::

::: example When are two composites equal?
**Problem.** For $f(x)=x+1$ and $g(x)=x^2-2x$, find the value of $x$ for which $(f\circ g)(x)=(g\circ f)(x)$.

**Solution.** $(f\circ g)(x)=x^2-2x+1$. $(g\circ f)(x)=(x+1)^2-2(x+1)=x^2+2x+1-2x-2=x^2-1$.

Equating, $x^2-2x+1=x^2-1$, so $-2x=-2$ and $x=1$. Check: both sides equal 0 when $x=1$.
:::

::: example Finding a function from a composite
**Problem.** If $g(x)=x-4$ and $(f\circ g)(x)=2x-5$, find $f(x)$.

**Solution.** Let $t=g(x)=x-4$, so $x=t+4$. Then $f(t)=2(t+4)-5=2t+3$. Hence $f(x)=2x+3$. Check: $f(g(x))=2(x-4)+3=2x-5$. ✓
:::

::: example Composite with a value
**Problem.** If $f(x)=3x-2$ and $g(x)=x^2+1$, find $(f\circ g)(2)$ and $(g\circ f)(2)$.

**Solution.** $g(2)=5$, so $(f\circ g)(2)=f(5)=13$. $f(2)=4$, so $(g\circ f)(2)=g(4)=17$.
:::

## 12.5 Inverse functions and their graphs

If $f$ turns $x$ into $y$, the **inverse function** $f^{-1}$ turns $y$ back into $x$. It undoes $f$.

::: definition Inverse function
If $f:A\to B$ is a one-one correspondence, the **inverse** $f^{-1}:B\to A$ is the function with
$$ f^{-1}(y)=x\iff f(x)=y, $$
so that $f\big(f^{-1}(x)\big)=x$ and $f^{-1}\big(f(x)\big)=x$. Note that $f^{-1}(x)$ does **not** mean $\frac{1}{f(x)}$.
:::

::: key Finding the inverse
1. Write $y=f(x)$.
2. Solve the equation for $x$ in terms of $y$.
3. Interchange the letters $x$ and $y$. The result is $y=f^{-1}(x)$.
4. Check that $f(f^{-1}(x))=x$.
:::

::: example Inverse of a linear function
**Problem.** Find the inverse of $f(x)=3x-5$ and evaluate $f^{-1}(7)$.

**Solution.** Put $y=3x-5$. Then $3x=y+5$ and $x=\frac{y+5}{3}$. Interchanging, $f^{-1}(x)=\frac{x+5}{3}$.

$f^{-1}(7)=\frac{12}{3}=4$. Check: $f(4)=12-5=7$. ✓
:::

::: example Inverse of a fractional function
**Problem.** Find the inverse of $f(x)=\frac{2x+1}{x-3}$, $x\neq 3$.

**Solution.** Put $y=\frac{2x+1}{x-3}$. Then $y(x-3)=2x+1$, so $xy-3y=2x+1$ and $x(y-2)=3y+1$. Hence $x=\frac{3y+1}{y-2}$ and

$$ f^{-1}(x)=\frac{3x+1}{x-2},\quad x\neq 2. $$

Check with $x=4$: $f(4)=\frac{9}{1}=9$ and $f^{-1}(9)=\frac{28}{7}=4$. ✓
:::

::: example Inverse of a function with a given value
**Problem.** If $f(x)=\frac{x-4}{5}$, find $f^{-1}(x)$ and solve $f^{-1}(x)=14$.

**Solution.** $y=\frac{x-4}{5}$ gives $x=5y+4$, so $f^{-1}(x)=5x+4$. Then $5x+4=14$ gives $x=2$.
:::

### Graph of the inverse

The point $(a,b)$ lies on the graph of $f$ exactly when $(b,a)$ lies on the graph of $f^{-1}$. Swapping the coordinates reflects a point in the line $y=x$. Therefore **the graph of $f^{-1}$ is the mirror image of the graph of $f$ in the line $y=x$.**

```figure caption="The graph of $f(x)=2x-1$ and its inverse $f^{-1}(x)=\\frac{x+1}{2}$ are mirror images in the line $y=x$. The point $(3,5)$ on $f$ matches $(5,3)$ on $f^{-1}$."
x = np.linspace(-2, 4, 50)
fig, ax = plt.subplots(figsize=(4.2, 3.6))
ax.plot(x, 2*x - 1, color=ACCENT, lw=1.4, label='f(x) = 2x - 1')
ax.plot(x, (x + 1)/2, color=SERIES[1], lw=1.4, label='inverse')
ax.plot(x, x, color='#888', lw=0.9, ls='--')
ax.plot([3, 5], [5, 3], 'ko', ms=3.5)
ax.text(3.1, 5.1, '(3, 5)', fontsize=8)
ax.text(5.05, 2.6, '(5, 3)', fontsize=8)
ax.text(4.2, 4.5, 'y = x', fontsize=8, color='#666')
ax.set_xlim(-2, 6.5); ax.set_ylim(-2, 6.5); ax.set_aspect('equal')
ax.axhline(0, color='#333', lw=0.6); ax.axvline(0, color='#333', lw=0.6)
ax.legend(fontsize=7.5, loc='upper left', frameon=False)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
fig.tight_layout(pad=0.4)
```

::: example A point on the inverse
**Problem.** The point $(2,7)$ lies on the graph of $f(x)=x^2+3$ (for $x\geq 0$). Write a point that lies on $f^{-1}$ and find $f^{-1}(12)$.

**Solution.** Swapping the coordinates, $(7,2)$ lies on $f^{-1}$. For $f^{-1}(12)$ solve $f(x)=12$: $x^2+3=12$, $x^2=9$, and $x=3$ (taking $x\geq 0$). So $f^{-1}(12)=3$.
:::

## 12.6 Polynomials

::: definition Polynomial
An expression of the form
$$ p(x)=a_nx^n+a_{n-1}x^{n-1}+\cdots+a_1x+a_0 $$
where $n$ is a non-negative integer and $a_n\neq 0$, is a **polynomial in $x$ of degree $n$**. The numbers $a_i$ are the **coefficients**, $a_n$ is the **leading coefficient** and $a_0$ the **constant term**.
:::

So $3x^4-2x^2+7$ has degree 4, $5x-1$ has degree 1 (linear), $x^2-9$ has degree 2 (quadratic), $x^3+x$ has degree 3 (cubic) and $6$ has degree 0. Expressions like $x^{-1}+2$ or $\sqrt{x}+1$ are **not** polynomials, because the powers are not whole numbers. A polynomial is written in **standard form** when its terms run from the highest power to the lowest.

When polynomials are added, subtracted or multiplied, the degree of a product is the **sum** of the degrees of the factors. When one polynomial is divided by another, we use the **division algorithm**.

::: key Division algorithm
If $p(x)$ is divided by a non-zero polynomial $d(x)$, there are unique polynomials, the **quotient** $q(x)$ and the **remainder** $r(x)$, such that
$$ p(x)=d(x)\,q(x)+r(x), $$
where $r(x)=0$ or the degree of $r(x)$ is less than the degree of $d(x)$.
:::

::: example Long division of polynomials
**Problem.** Divide $p(x)=x^3-2x^2+3x-5$ by $x-2$.

**Solution.** $x^3\div x=x^2$; subtract $x^2(x-2)=x^3-2x^2$, leaving $0x^2+3x-5$. Next, $0\div x=0$, leaving $3x-5$. Then $3x\div x=3$; subtract $3(x-2)=3x-6$, leaving $1$.

So the quotient is $x^2+3$ and the remainder is 1:

$$ x^3-2x^2+3x-5=(x-2)(x^2+3)+1. $$

Check by expanding: $(x-2)(x^2+3)=x^3+3x-2x^2-6$; adding 1 gives $x^3-2x^2+3x-5$. ✓
:::

## 12.7 The remainder theorem

Long division takes time. When we need only the remainder, there is a shortcut. Divide $p(x)$ by $x-a$. The remainder is a constant $R$, and $p(x)=(x-a)q(x)+R$. Put $x=a$: the term $(x-a)q(x)$ vanishes, so $p(a)=R$.

::: key Remainder theorem
When a polynomial $p(x)$ is divided by $x-a$, the remainder is $p(a)$. When it is divided by $ax+b$ (with $a\neq 0$), the remainder is $p\left(-\frac{b}{a}\right)$.
:::

::: tip The examiner is looking for
(1) the root of the divisor found first ($x-2$ gives $x=2$), (2) substitution into $p(x)$, (3) correct arithmetic with negative numbers, (4) a clear statement "the remainder is …".
:::

::: example Remainder by substitution
**Problem.** Find the remainder when $p(x)=x^3-2x^2+3x-5$ is divided by (i) $x-2$, (ii) $x+1$, (iii) $2x+1$.

**Solution.** (i) $p(2)=8-8+6-5=1$. This agrees with the long division above.

(ii) $x+1=x-(-1)$, so the remainder is $p(-1)=-1-2-3-5=-11$.

(iii) $2x+1=0$ gives $x=-\frac{1}{2}$. $p\left(-\frac{1}{2}\right)=-\frac{1}{8}-\frac{1}{2}-\frac{3}{2}-5=-\frac{57}{8}$.
:::

::: example Finding an unknown from the remainder
**Problem.** When $p(x)=x^3+kx^2-3x+2$ is divided by $x-2$ the remainder is 12. Find $k$.

**Solution.** $p(2)=8+4k-6+2=4k+4$. Setting $4k+4=12$ gives $k=2$.
:::

::: example Two remainders
**Problem.** The polynomial $p(x)=x^3+ax+b$ leaves remainder 4 when divided by $x-1$ and is exactly divisible by $x+1$. Find $a$ and $b$.

**Solution.** $p(1)=1+a+b=4$ so $a+b=3$. $p(-1)=-1-a+b=0$ so $b-a=1$. Adding, $2b=4$, $b=2$, and $a=1$. So $p(x)=x^3+x+2$.
:::

## 12.8 The factor theorem

If the remainder on dividing $p(x)$ by $x-a$ is zero, then $x-a$ divides $p(x)$ exactly, that is, $x-a$ is a **factor**. The remainder theorem says that the remainder is $p(a)$, so we get the factor theorem at once.

::: key Factor theorem
$x-a$ is a factor of $p(x)$ **if and only if** $p(a)=0$. In that case $a$ is called a **zero** (or root) of $p(x)$.
:::

::: example Testing a factor
**Problem.** Show that $x-1$ is a factor of $p(x)=x^3-3x^2+4x-2$ and find the other factor.

**Solution.** $p(1)=1-3+4-2=0$, so $x-1$ is a factor. Dividing,

$$ x^3-3x^2+4x-2=(x-1)(x^2-2x+2). $$

The quadratic factor $x^2-2x+2$ has discriminant $4-8=-4<0$, so it does not factor further over the real numbers.
:::

::: example Finding a constant so that a binomial is a factor
**Problem.** For what value of $k$ is $x-3$ a factor of $x^2-5x+k$?

**Solution.** We need $p(3)=0$: $9-15+k=0$, so $k=6$. Then $x^2-5x+6=(x-2)(x-3)$.
:::

::: example Two factors given
**Problem.** The polynomial $p(x)=x^3+ax^2+bx-6$ has $x-1$ and $x+2$ as factors. Find $a$ and $b$ and the third factor.

**Solution.** $p(1)=1+a+b-6=0$ gives $a+b=5$. $p(-2)=-8+4a-2b-6=0$ gives $2a-b=7$. Adding, $3a=12$, $a=4$, and $b=1$. So $p(x)=x^3+4x^2+x-6$.

Product of the zeros: for a monic cubic the product of the three zeros is $-(-6)=6$. The known zeros are $1$ and $-2$, so the third is $\frac{6}{1\times(-2)}=-3$, and the factor is $x+3$. Hence

$$ x^3+4x^2+x-6=(x-1)(x+2)(x+3). $$
:::

## 12.9 Synthetic division

Dividing by $x-a$ can be done quickly using only the coefficients. This is **synthetic division**.

::: key Method of synthetic division by $x-a$
1. Write the coefficients of $p(x)$ in order (put 0 for any missing power).
2. Bring down the first coefficient.
3. Multiply it by $a$, write the product under the next coefficient and add.
4. Repeat across the row. The last number is the **remainder**; the others are the coefficients of the **quotient**, whose degree is one less than $p(x)$.
:::

::: example Synthetic division
**Problem.** Divide $p(x)=2x^3-5x^2+x+6$ by $x-2$.

**Solution.** Here $a=2$ and the coefficients are $2,\ -5,\ 1,\ 6$.

Bring down 2. Then $2\times 2=4$ and $-5+4=-1$. Next $-1\times 2=-2$ and $1-2=-1$. Next $-1\times 2=-2$ and $6-2=4$.

The row is $2,\ -1,\ -1,\ \mid\ 4$. So the quotient is $2x^2-x-1$ and the remainder is 4. Check: $p(2)=16-20+2+6=4$. ✓
:::

::: example Synthetic division with a missing term
**Problem.** Divide $x^3-7x+6$ by $x-1$.

**Solution.** The $x^2$ term is missing, so the coefficients are $1,\ 0,\ -7,\ 6$ with $a=1$. Bring down 1; $0+1=1$; $-7+1=-6$; $6-6=0$.

The quotient is $x^2+x-6$ and the remainder is 0, so $x-1$ is a factor. Further, $x^2+x-6=(x+3)(x-2)$, so

$$ x^3-7x+6=(x-1)(x-2)(x+3). $$
:::

## 12.10 Zeros of a polynomial and factorisation

To factorise a polynomial of degree 3 or more, we look for a zero by trial, use the factor theorem, divide, and repeat with the quotient.

::: key Finding rational zeros by trial
If a polynomial with whole-number coefficients has a rational zero $\frac{m}{n}$ in lowest terms, then $m$ divides the constant term and $n$ divides the leading coefficient. For a monic polynomial, test the factors of the constant term: $\pm1, \pm2, \ldots$
:::

::: example Factorising a cubic
**Problem.** Factorise $p(x)=x^3-6x^2+11x-6$.

**Solution.** The constant term is $-6$; try its factors. $p(1)=1-6+11-6=0$, so $x-1$ is a factor. Synthetic division with $a=1$: coefficients $1,\ -6,\ 11,\ -6$ give $1,\ -5,\ 6,\ \mid\ 0$. So

$$ p(x)=(x-1)(x^2-5x+6)=(x-1)(x-2)(x-3). $$

The zeros are 1, 2 and 3.
:::

```figure caption="The graph of $p(x)=x^3-6x^2+11x-6$ crosses the $x$-axis at its three zeros $x=1,2,3$."
x = np.linspace(0.2, 3.8, 200)
y = x**3 - 6*x**2 + 11*x - 6
fig, ax = plt.subplots(figsize=(4.4, 2.8))
ax.plot(x, y, color=ACCENT, lw=1.5)
ax.plot([1, 2, 3], [0, 0, 0], 'o', color=SERIES[1], ms=5)
for z in (1, 2, 3):
    ax.text(z, -0.45, 'x = %d' % z, ha='center', fontsize=8)
ax.axhline(0, color='#333', lw=0.7)
ax.set_xlim(0, 4); ax.set_ylim(-1.6, 1.6)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('p(x)', fontsize=8.5)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example A cubic with a fractional zero
**Problem.** Solve $2x^3-3x^2-11x+6=0$.

**Solution.** Let $p(x)=2x^3-3x^2-11x+6$. Try $x=3$: $54-27-33+6=0$. So $x-3$ is a factor. Synthetic division with $a=3$ on $2,\ -3,\ -11,\ 6$ gives $2,\ 3,\ -2,\ \mid\ 0$, so the quotient is $2x^2+3x-2=(2x-1)(x+2)$.

Hence $p(x)=(x-3)(2x-1)(x+2)$ and the zeros are $x=3,\ \frac{1}{2},\ -2$.
:::

::: example Factorising by finding a negative zero
**Problem.** Factorise $x^3+2x^2-5x-6$.

**Solution.** $p(1)=1+2-5-6=-8\neq0$. $p(-1)=-1+2+5-6=0$, so $x+1$ is a factor. Synthetic division with $a=-1$ on $1,\ 2,\ -5,\ -6$: $1,\ 1,\ -6,\ \mid\ 0$. The quotient is $x^2+x-6=(x+3)(x-2)$, so

$$ x^3+2x^2-5x-6=(x+1)(x-2)(x+3). $$
:::

::: caution Common mistakes
- Using $p(a)$ for the divisor $x+a$. The divisor $x+a$ needs $p(-a)$.
- Forgetting a zero coefficient for a missing power in synthetic division.
- Dividing by $2x-1$ with $a=1$. For $2x-1$ use the zero $\frac{1}{2}$ and then divide the quotient by 2.
- Stopping after finding one zero; always factorise the quotient as far as possible.
:::

## 12.11 Zeros and coefficients

For a quadratic $x^2+bx+c$ with zeros $\alpha,\beta$ we know $\alpha+\beta=-b$ and $\alpha\beta=c$. The same idea works for a cubic.

::: key Zeros of a monic cubic
If $x^3+ax^2+bx+c$ has zeros $\alpha,\beta,\gamma$, then
$$ x^3+ax^2+bx+c=(x-\alpha)(x-\beta)(x-\gamma), $$
and comparing coefficients,
$$ \alpha+\beta+\gamma=-a,\qquad \alpha\beta+\beta\gamma+\gamma\alpha=b,\qquad \alpha\beta\gamma=-c. $$
:::

::: example Checking with known zeros
**Problem.** The zeros of $x^3-6x^2+11x-6$ are $1,2,3$. Verify the three relations.

**Solution.** Here $a=-6$, $b=11$, $c=-6$. Sum of zeros $=1+2+3=6=-a$. Sum of products in pairs $=2+3+6=11=b$. Product $=6=-c$. ✓
:::

::: example Building a polynomial from its zeros
**Problem.** Find the monic cubic polynomial whose zeros are $2,\ -1,\ 3$.

**Solution.** $p(x)=(x-2)(x+1)(x-3)$. First $(x-2)(x+1)=x^2-x-2$. Then $(x^2-x-2)(x-3)=x^3-3x^2-x^2+3x-2x+6=x^3-4x^2+x+6$.

Check with the relations: sum $=2-1+3=4=-(-4)$ ✓; pair sums $2(-1)+(-1)(3)+3(2)=-2-3+6=1=b$ ✓; product $=-6=-c$ ✓.
:::

::: example Equal polynomials
**Problem.** If $(x+2)(x^2+ax+b)=x^3+5x^2+8x+4$ for all $x$, find $a$ and $b$.

**Solution.** The left side expands to $x^3+(a+2)x^2+(b+2a)x+2b$. Equal polynomials have equal coefficients: $a+2=5$ gives $a=3$; $2b=4$ gives $b=2$; check $b+2a=2+6=8$ ✓.
:::

## 12.12 Exercises of the SEE type

### Method for any question

1. **Function questions:** substitute carefully, putting brackets around the replaced value, especially for negatives: $f(-2)$ for $x^2-3x$ is $(-2)^2-3(-2)=4+6=10$, not $-4-6$.
2. **Domain:** check each denominator and each square root separately, then combine the conditions.
3. **Composite:** write the inner function first, replace $x$ in the outer function by the whole inner expression, then simplify. Decide the order from the symbol: in $f\circ g$ the function $g$ acts first.
4. **Inverse:** $y=f(x)$, solve for $x$, interchange the letters, and finish with a numerical check such as $f(4)=9$ and $f^{-1}(9)=4$.
5. **Remainder and factor:** write the zero of the divisor, substitute into $p(x)$, and state the conclusion in words. Remainder zero means a factor.
6. **Factorising a cubic:** test $\pm1,\pm2,\pm3,\ldots$ (factors of the constant term), divide synthetically, then factorise the quadratic; list **all** the factors in the final answer.
7. **Unknown constants:** form one equation for each condition, solve, and substitute back to check.

A good habit is to finish every polynomial question with a quick numerical check: put a convenient value such as $x=0$ or $x=1$ into the original polynomial and into the factorised form. If the two values differ, there is an error somewhere in the working, and finding it takes seconds instead of a lost mark.

::: example Combined function question
**Problem.** If $f(x)=2x-3$ and $g(x)=x+4$, find $(f\circ g)(x)$, $(g\circ f)(x)$ and $f^{-1}(x)$. Then show that $(f\circ g)(x)\neq(g\circ f)(x)$.

**Solution.** $(f\circ g)(x)=2(x+4)-3=2x+5$. $(g\circ f)(x)=(2x-3)+4=2x+1$. These differ for every $x$.

For $f^{-1}$: $y=2x-3$ gives $x=\frac{y+3}{2}$, so $f^{-1}(x)=\frac{x+3}{2}$.
:::

::: example Remainder and factor together
**Problem.** When $x^3-ax^2+6x-8$ is divided by $x-2$ the remainder is 0. Find $a$, and factorise the polynomial completely.

**Solution.** $p(2)=8-4a+12-8=12-4a=0$, so $a=3$. Now $p(x)=x^3-3x^2+6x-8$. Synthetic division with $a=2$ on $1,\ -3,\ 6,\ -8$ gives $1,\ -1,\ 4,\ \mid\ 0$, so $p(x)=(x-2)(x^2-x+4)$. The discriminant of $x^2-x+4$ is $1-16=-15<0$, so this is as far as it factorises over the real numbers.
:::

::: example Equal remainders
**Problem.** $p(x)=x^2+kx-5$ leaves the same remainder when divided by $x-1$ and by $x+2$. Find $k$.

**Solution.** $p(1)=k-4$ and $p(-2)=4-2k-5=-2k-1$. Equating, $k-4=-2k-1$, so $3k=3$ and $k=1$. The common remainder is $-3$.
:::

::: example Zeros and the unknown coefficient
**Problem.** One zero of $x^3-4x^2+kx+6$ is 3. Find $k$ and the other zeros.

**Solution.** $p(3)=27-36+3k+6=3k-3=0$, so $k=1$. Now $p(x)=x^3-4x^2+x+6$. Synthetic division with $a=3$ on $1,\ -4,\ 1,\ 6$ gives $1,\ -1,\ -2,\ \mid\ 0$, so $p(x)=(x-3)(x^2-x-2)=(x-3)(x-2)(x+1)$. The zeros are $3,\ 2,\ -1$.
:::

::: example Composite values
**Problem.** If $f(x)=x^2+1$ and $g(x)=2x-3$, find $(f\circ g)(x)$ and $(g\circ f)(x)$, and the values at $x=2$.

**Solution.** $(f\circ g)(x)=(2x-3)^2+1=4x^2-12x+10$. $(g\circ f)(x)=2(x^2+1)-3=2x^2-1$.

At $x=2$: $(f\circ g)(2)=16-24+10=2$; direct check: $g(2)=1$, $f(1)=2$ ✓. $(g\circ f)(2)=8-1=7$; direct check: $f(2)=5$, $g(5)=7$ ✓.
:::

::: example Remainder by a linear divisor
**Problem.** Find the remainder when $p(x)=2x^3-3x^2+x-4$ is divided by (i) $x+1$, (ii) $2x-1$.

**Solution.** (i) $p(-1)=-2-3-1-4=-10$. (ii) The zero of $2x-1$ is $\frac{1}{2}$: $p\left(\frac{1}{2}\right)=\frac{2}{8}-\frac{3}{4}+\frac{1}{2}-4=\frac{1}{4}-\frac{3}{4}+\frac{2}{4}-4=-4$.
:::

::: example Finding $k$ and solving
**Problem.** The binomial $x+2$ is a factor of $x^3+kx^2-4x-12$. Find $k$ and all the zeros.

**Solution.** $p(-2)=-8+4k+8-12=4k-12=0$, so $k=3$. Then $p(x)=x^3+3x^2-4x-12=x^2(x+3)-4(x+3)=(x+3)(x^2-4)=(x+3)(x-2)(x+2)$. The zeros are $-3,\ 2,\ -2$.
:::

::: example An inverse with a restricted domain
**Problem.** Let $f(x)=x^2+2$ with domain $x\geq 0$. Find $f^{-1}(x)$, its domain, and $f^{-1}(11)$.

**Solution.** $y=x^2+2$ gives $x^2=y-2$ and, because $x\geq 0$, $x=\sqrt{y-2}$. So $f^{-1}(x)=\sqrt{x-2}$ with domain $x\geq 2$ (the range of $f$). $f^{-1}(11)=\sqrt{9}=3$. Check: $f(3)=11$ ✓.
:::

::: example A cost function and its inverse
**Problem.** A printer charges Rs $c=500+12n$ to print $n$ copies of a booklet. Find the inverse function and the number of copies for Rs 2,300.

**Solution.** $c=500+12n$ gives $n=\frac{c-500}{12}$. For $c=2300$: $n=\frac{1800}{12}=150$ copies.
:::

::: example Where a function meets its inverse
**Problem.** For $f(x)=3x-2$ find the value of $x$ for which $f(x)=f^{-1}(x)$.

**Solution.** $f^{-1}(x)=\frac{x+2}{3}$. Setting $3x-2=\frac{x+2}{3}$ gives $9x-6=x+2$, so $8x=8$ and $x=1$. This lies on the line $y=x$, as the mirror-image property predicts: $f(1)=1$.
:::

## Chapter summary

- **Relation:** a set of ordered pairs; domain = first components, range = second components.
- **Function:** every element of the domain has exactly one image. Vertical line test; horizontal line test for one-one.
- **Domain:** exclude zero denominators; keep square-root arguments $\geq 0$.
- **Composite:** $(f\circ g)(x)=f(g(x))$; in general $f\circ g\neq g\circ f$.
- **Inverse:** solve $y=f(x)$ for $x$, then swap letters; the graph of $f^{-1}$ is the mirror image of that of $f$ in $y=x$.
- **Polynomial:** degree $n$, standard form; $p(x)=d(x)q(x)+r(x)$.
- **Remainder theorem:** remainder on division by $x-a$ is $p(a)$.
- **Factor theorem:** $x-a$ is a factor iff $p(a)=0$.
- **Synthetic division** gives quotient and remainder from the coefficients; factorise cubics by finding one zero, dividing, and factorising the quadratic.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. If $f(x)=3x-4$, then $f(5)$ is <span class="marks">[1]</span>
   (a) 9 (b) 11 (c) 19 (d) $-1$
2. The domain of $f(x)=\frac{1}{x-5}$ is <span class="marks">[1]</span>
   (a) all real numbers (b) $x>5$ (c) all real numbers except 5 (d) all real numbers except $-5$
3. If $f(x)=x+2$ and $g(x)=x^2$, then $(g\circ f)(1)$ is <span class="marks">[1]</span>
   (a) 3 (b) 5 (c) 9 (d) 27
4. If $f(x)=2x+6$, then $f^{-1}(4)$ is <span class="marks">[1]</span>
   (a) 14 (b) $-1$ (c) 1 (d) $-5$
5. The remainder when $x^2+x+1$ is divided by $x-1$ is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 3 (d) $-1$
6. $x-3$ is a factor of $x^2-5x+k$ when $k$ equals <span class="marks">[1]</span>
   (a) 6 (b) $-6$ (c) 2 (d) 15
7. The degree of $(x^2+1)(x^3-x)$ is <span class="marks">[1]</span>
   (a) 6 (b) 5 (c) 3 (d) 2

::: note Answers to Group A
**1.** (b) — $f(5)=15-4=11$.
**2.** (c) — $x-5\neq0$.
**3.** (c) — $f(1)=3$ and $g(3)=9$.
**4.** (b) — $f^{-1}(x)=\frac{x-6}{2}$, so $f^{-1}(4)=-1$.
**5.** (c) — $p(1)=1+1+1=3$.
**6.** (a) — $9-15+k=0$, so $k=6$.
**7.** (b) — the degrees add: $2+3=5$.
:::

**Group B — Short answer (2 marks each)**

1. Find the range of $f(x)=x^2-1$ with domain $\{-2,-1,0,1,2\}$. <span class="marks">[2]</span>
2. If $f(x)=x^2-2x$, find $f(3)+f(-1)$. <span class="marks">[2]</span>
3. If $f(x)=2x+3$ and $g(x)=x-4$, find $(f\circ g)(x)$ and $(g\circ f)(x)$. <span class="marks">[2]</span>
4. Find the inverse of $f(x)=5x+4$. <span class="marks">[2]</span>
5. Find the remainder when $x^3+2x^2-x+4$ is divided by $x+2$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $f(-2)=3$, $f(-1)=0$, $f(0)=-1$, $f(1)=0$, $f(2)=3$. The range is $\{-1,0,3\}$.
**2.** $f(3)=9-6=3$ and $f(-1)=1+2=3$. The sum is 6.
**3.** $(f\circ g)(x)=2(x-4)+3=2x-5$ and $(g\circ f)(x)=(2x+3)-4=2x-1$.
**4.** $y=5x+4$, $x=\frac{y-4}{5}$, so $f^{-1}(x)=\frac{x-4}{5}$.
**5.** $p(-2)=-8+8+2+4=6$.
:::

**Group C — Short answer (3 marks each)**

1. A linear function $f(x)=ax+b$ has $f(1)=5$ and $f(3)=11$. Find $a$, $b$ and $f(10)$. <span class="marks">[3]</span>
2. Show that $x-1$ is a factor of $x^3-3x^2+4x-2$ and find the quotient. <span class="marks">[3]</span>
3. When $x^3+kx^2-3x+2$ is divided by $x-2$ the remainder is 12. Find $k$. <span class="marks">[3]</span>
4. Find the inverse of $f(x)=\frac{x+1}{x-2}$. <span class="marks">[3]</span>
5. Use synthetic division to divide $2x^3-5x^2+x+6$ by $x-2$. State the quotient and the remainder. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $a+b=5$ and $3a+b=11$, so $a=3$, $b=2$, $f(x)=3x+2$ and $f(10)=32$.
**2.** $p(1)=1-3+4-2=0$, so $x-1$ is a factor. The quotient is $x^2-2x+2$.
**3.** $p(2)=8+4k-6+2=4k+4=12$, so $k=2$.
**4.** $y(x-2)=x+1$, $x(y-1)=2y+1$, so $f^{-1}(x)=\frac{2x+1}{x-1}$.
**5.** Coefficients $2,-5,1,6$ with $a=2$ give $2,-1,-1,\mid 4$. Quotient $2x^2-x-1$, remainder 4.
:::

**Group D — Long answer (4 marks each)**

1. Factorise $x^3-7x+6$ completely. <span class="marks">[4]</span>
2. The polynomial $x^3+ax^2+bx-6$ has $x-1$ and $x+2$ as factors. Find $a$ and $b$ and factorise it. <span class="marks">[4]</span>
3. If $f(x)=x+1$ and $g(x)=x^2-2x$, find $x$ so that $(f\circ g)(x)=(g\circ f)(x)$. <span class="marks">[4]</span>
4. The polynomial $x^3+ax+b$ leaves remainder 4 on division by $x-1$ and is exactly divisible by $x+1$. Find $a$ and $b$. <span class="marks">[4]</span>
5. Solve $2x^3-3x^2-11x+6=0$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $p(1)=1-7+6=0$. Dividing by $x-1$ gives $x^2+x-6=(x+3)(x-2)$. So $x^3-7x+6=(x-1)(x-2)(x+3)$.
**2.** $1+a+b-6=0$ gives $a+b=5$; $-8+4a-2b-6=0$ gives $2a-b=7$. So $a=4$, $b=1$ and $x^3+4x^2+x-6=(x-1)(x+2)(x+3)$.
**3.** $(f\circ g)(x)=x^2-2x+1$ and $(g\circ f)(x)=(x+1)^2-2(x+1)=x^2-1$. Equating gives $-2x+1=-1$, so $x=1$.
**4.** $1+a+b=4$ and $-1-a+b=0$. Adding, $2b=4$, $b=2$, $a=1$.
**5.** $p(3)=54-27-33+6=0$. Dividing by $x-3$ gives $2x^2+3x-2=(2x-1)(x+2)$. So $x=3,\ \frac{1}{2},\ -2$.
:::

---
subject: Mathematics
grade: 10
unit: 11
title: Algebraic Fraction
hours: 0
area: Compulsory Mathematics
---

A fraction such as $\frac{3}{4}$ has numbers on the top and bottom. An **algebraic fraction** has algebraic expressions there, for example $\frac{x^2-9}{x^2+5x+6}$. We add, subtract, multiply, divide and simplify algebraic fractions by exactly the same rules as ordinary fractions; the only new skill is **factorisation**, because we can cancel only *factors*, never terms. Algebraic fractions appear in formulae for speed, work and electricity, and in the SEE they give a dependable 3- or 4-mark question on simplification.

::: key What the SEE asks from this chapter
Expect: (i) reduce a fraction to its **lowest terms** by factorising; (ii) **add or subtract** two or three fractions with different denominators using the LCM; (iii) **multiply or divide** fractions and simplify to a single expression; (iv) a "simplify" or "prove" question combining all of these, often ending in a surprisingly simple answer like 1 or $x+1$. Factorise first, cancel second, and write every step.
:::

## 11.1 Algebraic Fraction: concepts, formulas and worked problems

### Factorisation toolkit

Everything in this chapter rests on these factorisations. Learn them until you can see them at a glance.

::: key Factorisation formulas
$$ a^2-b^2=(a+b)(a-b) $$
$$ a^2+2ab+b^2=(a+b)^2 \qquad a^2-2ab+b^2=(a-b)^2 $$
$$ a^3+b^3=(a+b)(a^2-ab+b^2) $$
$$ a^3-b^3=(a-b)(a^2+ab+b^2) $$

| Type | Method | Example |
|---|---|---|
| Common factor | take out the HCF | $6x^2+9x=3x(2x+3)$ |
| Difference of squares | $a^2-b^2$ | $x^2-25=(x+5)(x-5)$ |
| Trinomial $x^2+px+q$ | two numbers with sum $p$, product $q$ | $x^2+5x+6=(x+2)(x+3)$ |
| Trinomial $ax^2+bx+c$ | split the middle term | $2x^2+7x+3=(2x+1)(x+3)$ |
| Grouping | pair the terms | $ax+ay+bx+by=(a+b)(x+y)$ |
| Sum / difference of cubes | the two formulas above | $x^3-8=(x-2)(x^2+2x+4)$ |
:::

```figure caption="Area model of a² − b². Remove the b × b square from the a × a square and re-arrange the rest into a rectangle (a + b) long and (a − b) wide."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.5), gridspec_kw={'width_ratios':[1, 1.35]})
a, b = 3.0, 1.2
ax1.add_patch(Rectangle((0, 0), a, a, fc='#dbeafe', ec=INK, lw=1.1))
ax1.add_patch(Rectangle((a-b, a-b), b, b, fc='white', ec=INK, lw=1.1, hatch='//'))
ax1.text(a/2, a/2 - 0.3, 'a² − b²', ha='center', fontsize=9)
ax1.text(a - b/2, a - b/2, 'b²', ha='center', va='center', fontsize=8)
ax1.text(a/2, -0.3, 'a', ha='center', va='top', fontsize=8.5)
ax1.text(-0.12, a/2, 'a', ha='right', va='center', fontsize=8.5)
ax1.set_xlim(-0.6, a + 0.3); ax1.set_ylim(-0.8, a + 0.3); ax1.set_aspect('equal'); ax1.axis('off')
ax2.add_patch(Rectangle((0, 0), a + b, a - b, fc='#dcfce7', ec=INK, lw=1.1))
ax2.plot([a, a], [0, a - b], color=INK, lw=0.8, ls='--')
ax2.text((a + b)/2, (a - b)/2, '(a + b)(a − b)', ha='center', va='center', fontsize=9)
ax2.text((a + b)/2, -0.3, 'a + b', ha='center', va='top', fontsize=8.5)
ax2.text(-0.12, (a - b)/2, 'a − b', ha='right', va='center', fontsize=8.5)
ax2.set_xlim(-1.2, a + b + 0.3); ax2.set_ylim(-0.8, a + 0.3); ax2.set_aspect('equal'); ax2.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Factorising before simplifying
**Problem.** Factorise (a) $x^2-7x+12$, (b) $3x^2-x-2$, (c) $a^3+27$.

**Solution.**
(a) We need two numbers with product $12$ and sum $-7$: $-3$ and $-4$. So $x^2-7x+12=(x-3)(x-4)$.

(b) $3\times(-2)=-6$; split $-x$ as $-3x+2x$: $3x^2-3x+2x-2=3x(x-1)+2(x-1)=(x-1)(3x+2)$.

(c) $a^3+27=a^3+3^3=(a+3)(a^2-3a+9)$.
:::

### Reducing to lowest terms

::: key Cancelling rule
$$ \frac{p\times r}{q\times r}=\frac{p}{q}\qquad (r\ne 0) $$
You may cancel only a **common factor** of the whole numerator and the whole denominator. Never cancel a term that is added or subtracted: $\frac{x+3}{x+5}$ is already in lowest terms, and it is **not** $\frac{3}{5}$.
:::

::: example Reduce to lowest terms
**Problem.** Simplify $\frac{x^2-9}{x^2+5x+6}$.

**Solution.** Factorise both parts: $x^2-9=(x+3)(x-3)$ and $x^2+5x+6=(x+2)(x+3)$. Then

$$ \frac{(x+3)(x-3)}{(x+2)(x+3)}=\frac{x-3}{x+2} $$

**Check with $x=1$.** Original: $\frac{1-9}{1+5+6}=\frac{-8}{12}=-\frac{2}{3}$. Answer: $\frac{1-3}{1+2}=-\frac{2}{3}$. ✓
:::

::: example Reduce with a trinomial
**Problem.** Simplify $\frac{a^2-a-6}{a^2-9}$.

**Solution.** $a^2-a-6=(a-3)(a+2)$ and $a^2-9=(a-3)(a+3)$. Cancel $(a-3)$:

$$ \frac{a^2-a-6}{a^2-9}=\frac{a+2}{a+3} $$
:::

::: example Reduce with cubes
**Problem.** Simplify $\frac{x^3-8}{x^2-4}$.

**Solution.** $x^3-8=(x-2)(x^2+2x+4)$ and $x^2-4=(x-2)(x+2)$. So the fraction is $\frac{x^2+2x+4}{x+2}$.
:::

::: caution Common mistakes
- Cancelling terms: $\frac{x+3}{x+5}\ne\frac{3}{5}$ and $\frac{x^2+4}{x+4}\ne x$.
- Forgetting a bracket when subtracting a fraction: $\frac{1}{a}-\frac{b-c}{a}=\frac{1-(b-c)}{a}$, not $\frac{1-b-c}{a}$.
- Cancelling before factorising — if you cannot see a common factor, factorise first.
- Writing "$=0$" when numerators cancel: $\frac{x}{x}=1$, not 0.
:::

### HCF and LCM of expressions

To add fractions you need a common denominator, and the best one is the **lowest common multiple (LCM)** of the denominators. As in Chapter 8, factorise first. The **HCF** takes each common factor with its **smallest** power; the **LCM** takes every factor that appears, with its **largest** power.

| Expressions | Factorised | HCF | LCM |
|---|---|---|---|
| $x^2-4$ and $x^2+4x+4$ | $(x-2)(x+2)$ and $(x+2)^2$ | $x+2$ | $(x-2)(x+2)^2$ |
| $x^2-x-6$ and $x^2-9$ | $(x-3)(x+2)$ and $(x-3)(x+3)$ | $x-3$ | $(x-3)(x+2)(x+3)$ |
| $6x^2y$ and $9xy^2$ | $2\cdot3\cdot x^2y$ and $3^2\cdot xy^2$ | $3xy$ | $18x^2y^2$ |

::: example LCM before adding
**Problem.** Add $\frac{1}{x^2-4}+\frac{1}{x^2+4x+4}$.

**Solution.** From the table the LCM is $(x-2)(x+2)^2$. Multiply the first fraction's top and bottom by $(x+2)$ and the second's by $(x-2)$:

$$ \frac{(x+2)+(x-2)}{(x-2)(x+2)^2}=\frac{2x}{(x-2)(x+2)^2} $$

**Check with $x=3$.** $\frac{1}{5}+\frac{1}{25}=\frac{6}{25}$, and the answer gives $\frac{6}{1\times25}=\frac{6}{25}$ ✓.
:::

### Multiplication and division

::: key Rules
$$ \frac{p}{q}\times\frac{r}{s}=\frac{pr}{qs}\qquad \frac{p}{q}\div\frac{r}{s}=\frac{p}{q}\times\frac{s}{r}=\frac{ps}{qr} $$
To divide, **invert the second fraction and multiply**. Factorise everything and cancel before multiplying out.
:::

::: example Multiplying
**Problem.** Simplify $\frac{x^2-5x+6}{x^2-4}\times\frac{x+2}{x-3}$.

**Solution.** $x^2-5x+6=(x-2)(x-3)$ and $x^2-4=(x-2)(x+2)$. Thus

$$ \frac{(x-2)(x-3)}{(x-2)(x+2)}\times\frac{x+2}{x-3}=1 $$

Every factor cancels, leaving 1.
:::

::: example Dividing
**Problem.** Simplify $\frac{a^2-b^2}{a^2+2ab+b^2}\div\frac{a-b}{a+b}$.

**Solution.** Factorise: $\frac{(a+b)(a-b)}{(a+b)^2}\times\frac{a+b}{a-b}$. The factors $(a+b)$ and $(a-b)$ cancel completely:

$$ \frac{(a+b)(a-b)(a+b)}{(a+b)(a+b)(a-b)}=1 $$
:::

::: example Three fractions
**Problem.** Simplify $\frac{x^2+3x+2}{x^2+x-2}\times\frac{x^2-1}{x^2+2x}$.

**Solution.** $x^2+3x+2=(x+1)(x+2)$, $x^2+x-2=(x+2)(x-1)$, $x^2-1=(x+1)(x-1)$, $x^2+2x=x(x+2)$. So

$$ \frac{(x+1)(x+2)}{(x+2)(x-1)}\times\frac{(x+1)(x-1)}{x(x+2)} $$

Cancel $(x+2)$ once and $(x-1)$ once:

$$ \frac{(x+1)(x+1)}{x(x+2)}=\frac{(x+1)^2}{x(x+2)} $$
:::

### Addition and subtraction

::: key Steps for $\frac{p}{q}\pm\frac{r}{s}$
1. Factorise every denominator.
2. Find the **LCM** of the denominators: each different factor once, with its highest power.
3. Rewrite each fraction with the LCM as denominator (multiply top and bottom by the missing factors).
4. Add or subtract the numerators — **put brackets round numerators** that are subtracted.
5. Simplify the numerator; factorise and cancel if possible.
:::

::: example Same denominator
**Problem.** Simplify $\frac{x}{x^2-y^2}-\frac{y}{x^2-y^2}$.

**Solution.** The denominators are equal, so $\frac{x-y}{x^2-y^2}=\frac{x-y}{(x-y)(x+y)}=\frac{1}{x+y}$.
:::

::: example Different denominators
**Problem.** Simplify $\frac{1}{x-1}+\frac{1}{x+1}$.

**Solution.** The LCM is $(x-1)(x+1)$.

$$ \frac{(x+1)+(x-1)}{(x-1)(x+1)}=\frac{2x}{x^2-1} $$
:::

::: example Subtraction
**Problem.** Simplify $\frac{x}{x-2}-\frac{2}{x+2}$.

**Solution.** LCM $=(x-2)(x+2)$.

$$ \frac{x(x+2)-2(x-2)}{(x-2)(x+2)}=\frac{x^2+2x-2x+4}{x^2-4}=\frac{x^2+4}{x^2-4} $$

The numerator $x^2+4$ does not factorise, so this is the final answer.
:::

::: example Three fractions
**Problem.** Simplify $\frac{2}{x^2-1}+\frac{1}{x+1}-\frac{1}{x-1}$.

**Solution.** $x^2-1=(x+1)(x-1)$, so the LCM is $(x+1)(x-1)$:

$$ \frac{2+(x-1)-(x+1)}{(x+1)(x-1)}=\frac{2+x-1-x-1}{(x+1)(x-1)}=\frac{0}{x^2-1}=0 $$
:::

::: example Subtraction with a bracket trap
**Problem.** Simplify $\frac{1}{x-2}-\frac{1}{x-1}-\frac{1}{(x-1)(x-2)}$.

**Solution.** The LCM is $(x-1)(x-2)$.

$$ \frac{(x-1)-(x-2)-1}{(x-1)(x-2)}=\frac{x-1-x+2-1}{(x-1)(x-2)}=\frac{0}{(x-1)(x-2)}=0 $$
:::

::: example Unlike denominators with a pair
**Problem.** Simplify $\frac{x+2}{x-2}-\frac{x-2}{x+2}$.

**Solution.** LCM $=(x-2)(x+2)$. Numerator: $(x+2)^2-(x-2)^2=(x^2+4x+4)-(x^2-4x+4)=8x$.

$$ \frac{8x}{x^2-4} $$
:::

### Fractions inside fractions

::: example Complex fraction
**Problem.** Simplify $\frac{x^2-\frac{1}{x^2}}{x-\frac{1}{x}}$.

**Solution.** Put $p=x$ and $q=\frac{1}{x}$. Then the numerator is $p^2-q^2$ and the denominator is $p-q$. Therefore

$$ \frac{p^2-q^2}{p-q}=p+q=x+\frac{1}{x}=\frac{x^2+1}{x} $$
:::

::: example Continued fraction
**Problem.** Simplify $\frac{1}{1-\frac{1}{1+\frac{1}{x}}}$.

**Solution.** Work from the inside out.

- $1+\frac{1}{x}=\frac{x+1}{x}$, so its reciprocal is $\frac{x}{x+1}$.
- $1-\frac{x}{x+1}=\frac{(x+1)-x}{x+1}=\frac{1}{x+1}$.
- The reciprocal of $\frac{1}{x+1}$ is $x+1$.

The answer is $x+1$.
:::

::: example Sum of squares
**Problem.** Simplify $\left(x+\frac{1}{x}\right)^2-\left(x-\frac{1}{x}\right)^2$.

**Solution.** Use $a^2-b^2=(a+b)(a-b)$: here $a+b=2x$ and $a-b=\frac{2}{x}$. The product is $2x\times\frac{2}{x}=4$.
:::

```figure caption="A route map for any algebraic-fraction question: factorise first, then decide whether to cancel (× and ÷) or find the LCM (+ and −)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.6))
def box(x, y, w, h, t, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc=fc, ec=INK, lw=1.0))
    ax.text(x + w/2, y + h/2, t, ha='center', va='center', fontsize=8)
box(3.5, 3.9, 3.0, 0.8, 'Factorise every numerator\nand denominator', '#dbeafe')
box(0.2, 2.2, 3.4, 0.9, 'Multiply or divide?\n(invert the 2nd for ÷)', '#fef9c3')
box(6.4, 2.2, 3.4, 0.9, 'Add or subtract?\nFind the LCM first', '#fef9c3')
box(0.2, 0.6, 3.4, 0.9, 'Cancel common factors,\nthen multiply across', '#dcfce7')
box(6.4, 0.6, 3.4, 0.9, 'Combine numerators\n(use brackets), then\nfactorise and cancel', '#dcfce7')
for (x1, y1, x2, y2) in [(4.6, 3.9, 2.4, 3.1), (5.4, 3.9, 7.6, 3.1), (1.9, 2.2, 1.9, 1.5), (8.1, 2.2, 8.1, 1.5)]:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color=INK, lw=1.0))
ax.set_xlim(0, 10); ax.set_ylim(0.2, 5.0); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: tip Restrictions
A fraction is undefined when its denominator is 0. In $\frac{x-3}{x+2}$ we need $x\ne-2$. In the SEE you are rarely asked to state this, but you must never put a value in that makes a denominator zero when you check an answer.
:::

### Equations with algebraic fractions

::: key Solving a fractional equation
Multiply **every term** by the LCM of the denominators to clear the fractions, solve the resulting equation, and **reject** any answer that makes a denominator zero.
:::

::: example Solve
**Problem.** Solve $\frac{1}{x-1}+\frac{1}{x+1}=\frac{4}{3}$.

**Solution.** The left side is $\frac{2x}{x^2-1}$ (done above). Then

$$ \frac{2x}{x^2-1}=\frac{4}{3} \;\Rightarrow\; 6x=4x^2-4 \;\Rightarrow\; 2x^2-3x-2=0 $$

Factorise: $(2x+1)(x-2)=0$, so $x=-\frac{1}{2}$ or $x=2$. Neither makes a denominator zero, so both are valid.

**Check $x=2$.** $\frac{1}{1}+\frac{1}{3}=\frac{4}{3}$. ✓
:::

::: example Solve with a fraction on each side
**Problem.** Solve $\frac{3}{x-1}-\frac{2}{x+1}=1$.

**Solution.** Multiply by $(x-1)(x+1)$:

$$ 3(x+1)-2(x-1)=(x-1)(x+1) \;\Rightarrow\; x+5=x^2-1 $$

So $x^2-x-6=0$, $(x-3)(x+2)=0$ and $x=3$ or $x=-2$.
:::

### More patterns to practise

::: example Trinomials on both sides
**Problem.** Simplify $\frac{x^2+x-12}{x^2-16}$.

**Solution.** $x^2+x-12=(x+4)(x-3)$ and $x^2-16=(x+4)(x-4)$. Cancel $(x+4)$:

$$ \frac{x^2+x-12}{x^2-16}=\frac{x-3}{x-4} $$

**Check with $x=5$.** Original: $\frac{25+5-12}{25-16}=\frac{18}{9}=2$. Answer: $\frac{5-3}{5-4}=2$. ✓
:::

::: example Splitting the middle term
**Problem.** Simplify $\frac{2x^2+5x-3}{2x^2-5x+2}$.

**Solution.** For the top, $2\times(-3)=-6$ and $5=6-1$: $2x^2+6x-x-3=2x(x+3)-1(x+3)=(2x-1)(x+3)$. For the bottom, $2\times2=4$ and $-5=-4-1$: $2x^2-4x-x+2=2x(x-2)-1(x-2)=(2x-1)(x-2)$. Cancel $(2x-1)$:

$$ \frac{x+3}{x-2} $$
:::

::: example A perfect square over a difference of squares
**Problem.** Simplify $\frac{a^2-4a+4}{a^2-4}\times\frac{a+2}{a-2}$.

**Solution.** $a^2-4a+4=(a-2)^2$ and $a^2-4=(a-2)(a+2)$. So

$$ \frac{(a-2)^2}{(a-2)(a+2)}\times\frac{a+2}{a-2}=\frac{(a-2)^2(a+2)}{(a-2)^2(a+2)}=1 $$
:::

::: example Two fractions, one hidden factor
**Problem.** Simplify $\frac{x}{x-3}-\frac{x+3}{x^2-9}$.

**Solution.** $x^2-9=(x-3)(x+3)$, so the second fraction reduces first: $\frac{x+3}{(x-3)(x+3)}=\frac{1}{x-3}$. Now the denominators are equal:

$$ \frac{x}{x-3}-\frac{1}{x-3}=\frac{x-1}{x-3} $$

Always look for a fraction that can be reduced before you find the LCM; it saves work.
:::

::: example Three terms with $x^2-9$
**Problem.** Simplify $\frac{1}{x-3}+\frac{1}{x+3}+\frac{6}{x^2-9}$.

**Solution.** LCM $=(x-3)(x+3)$.

$$ \frac{(x+3)+(x-3)+6}{(x-3)(x+3)}=\frac{2x+6}{(x-3)(x+3)}=\frac{2(x+3)}{(x-3)(x+3)}=\frac{2}{x-3} $$
:::

::: example A division with a common factor
**Problem.** Simplify $\frac{x^2-9}{x^2-4x+3}\div\frac{x+3}{x-1}$.

**Solution.** $x^2-4x+3=(x-1)(x-3)$ and $x^2-9=(x-3)(x+3)$. Invert the divisor:

$$ \frac{(x-3)(x+3)}{(x-1)(x-3)}\times\frac{x-1}{x+3}=1 $$
:::

::: example Same denominator, difference of squares on top
**Problem.** Simplify $\frac{x^2}{x-y}-\frac{y^2}{x-y}$.

**Solution.** $\frac{x^2-y^2}{x-y}=\frac{(x-y)(x+y)}{x-y}=x+y$.
:::

::: example Cubes
**Problem.** Simplify $\frac{a^3-b^3}{a^2-b^2}\times\frac{a+b}{a^2+ab+b^2}$.

**Solution.** $a^3-b^3=(a-b)(a^2+ab+b^2)$ and $a^2-b^2=(a-b)(a+b)$. Hence

$$ \frac{(a-b)(a^2+ab+b^2)}{(a-b)(a+b)}\times\frac{a+b}{a^2+ab+b^2}=1 $$
:::

::: example Fractions inside
**Problem.** Simplify $\frac{\frac{1}{x}-\frac{1}{y}}{\frac{1}{x^2}-\frac{1}{y^2}}$.

**Solution.** The numerator is $\frac{y-x}{xy}$. The denominator is $\frac{y^2-x^2}{x^2y^2}=\frac{(y-x)(y+x)}{x^2y^2}$. Dividing,

$$ \frac{y-x}{xy}\times\frac{x^2y^2}{(y-x)(y+x)}=\frac{xy}{x+y} $$
:::

::: example An equation that gives two roots
**Problem.** Solve $\frac{x}{x-2}+\frac{x-2}{x}=\frac{5}{2}$.

**Solution.** Multiply by $2x(x-2)$: $2x^2+2(x-2)^2=5x(x-2)$. Expand: $2x^2+2x^2-8x+8=5x^2-10x$, so $x^2-2x-8=0$ and $(x-4)(x+2)=0$. Hence $x=4$ or $x=-2$.

**Check $x=4$.** $\frac{4}{2}+\frac{2}{4}=2.5$ ✓. **Check $x=-2$.** $\frac{-2}{-4}+\frac{-4}{-2}=0.5+2=2.5$ ✓.
:::

::: example Equation with shifted numerators
**Problem.** Solve $\frac{x-2}{x-3}+\frac{x-4}{x-5}=\frac{10}{3}$.

**Solution.** Multiply by $3(x-3)(x-5)$: $3(x-2)(x-5)+3(x-4)(x-3)=10(x-3)(x-5)$. Expanding, $3(x^2-7x+10)+3(x^2-7x+12)=10(x^2-8x+15)$, i.e. $6x^2-42x+66=10x^2-80x+150$, which gives $4x^2-38x+84=0$ or $2x^2-19x+42=0$. Then $(2x-7)(x-6)=0$ and $x=\frac{7}{2}$ or $x=6$.
:::

## 11.2 Exercises of the SEE type

### Method for any question

1. **Factorise** each numerator and denominator completely.
2. For $\times,\div$: invert the divisor, cancel common factors, multiply what remains.
3. For $+,-$: LCM of denominators, bracket every numerator being subtracted.
4. Check by substituting a small number (such as $x=2$ or $x=3$) in the question and the answer. They must agree.
5. Present the answer in lowest terms.

::: example SEE type: simplify
**Problem.** Simplify $\frac{a}{a-b}-\frac{b}{a+b}-\frac{2ab}{a^2-b^2}$.

**Solution.** LCM $=(a-b)(a+b)=a^2-b^2$.

$$ \frac{a(a+b)-b(a-b)-2ab}{a^2-b^2}=\frac{a^2+ab-ab+b^2-2ab}{a^2-b^2}=\frac{a^2-2ab+b^2}{a^2-b^2} $$

The numerator is $(a-b)^2$, so the expression equals $\frac{(a-b)^2}{(a-b)(a+b)}=\frac{a-b}{a+b}$.
:::

::: example SEE type: combine three fractions
**Problem.** Simplify $\frac{1}{x+1}+\frac{2}{x+2}-\frac{3}{x+3}$.

**Solution.** The LCM is $(x+1)(x+2)(x+3)$. The numerator is

$$ (x+2)(x+3)+2(x+1)(x+3)-3(x+1)(x+2) $$

Expand each part: $x^2+5x+6$, $2x^2+8x+6$ and $3x^2+9x+6$. So the numerator is $(x^2+2x^2-3x^2)+(5x+8x-9x)+(6+6-6)$, which equals $4x+6$. Hence

$$ \frac{4x+6}{(x+1)(x+2)(x+3)}=\frac{2(2x+3)}{(x+1)(x+2)(x+3)} $$

**Check with $x=1$.** Left: $\frac{1}{2}+\frac{2}{3}-\frac{3}{4}=\frac{5}{12}$. Right: $\frac{2\times5}{2\times3\times4}=\frac{5}{12}$. ✓
:::

::: example SEE type: show that
**Problem.** Show that $\frac{x^2+3x+2}{x+1}+\frac{x^2-x-6}{x-3}=2(x+2)$.

**Solution.** $x^2+3x+2=(x+1)(x+2)$, so the first fraction is $x+2$. $x^2-x-6=(x-3)(x+2)$, so the second fraction is $x+2$. The sum is $(x+2)+(x+2)=2(x+2)$. Proved.
:::

::: example SEE type: area of a rectangle
**Problem.** A rectangle has area $x^2+7x+12$ and length $x+4$. Find its breadth, and the ratio of the breadth to the length.

**Solution.** Breadth $=\frac{\text{area}}{\text{length}}=\frac{x^2+7x+12}{x+4}=\frac{(x+3)(x+4)}{x+4}=x+3$. The ratio is $\frac{x+3}{x+4}$.
:::

## Chapter summary

- Factorisation formulas: $a^2-b^2=(a+b)(a-b)$; $(a\pm b)^2$; $a^3\pm b^3=(a\pm b)(a^2\mp ab+b^2)$; trinomials by sum and product or by splitting the middle term.
- Cancel only **factors**, never added terms.
- $\frac{p}{q}\times\frac{r}{s}=\frac{pr}{qs}$; $\frac{p}{q}\div\frac{r}{s}=\frac{p}{q}\times\frac{s}{r}$.
- To add or subtract: factorise the denominators, take the LCM, rewrite, combine numerators with brackets, simplify.
- Complex fractions: simplify the inside first; $x^2-\frac{1}{x^2}=\left(x+\frac{1}{x}\right)\left(x-\frac{1}{x}\right)$.
- Fractional equations: multiply by the LCM; reject roots that zero a denominator.
- Always check with a small number such as $x=2$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Factorise $x^2-16$. <span class="marks">[1]</span>
   (a) $(x-4)^2$ (b) $(x+4)(x-4)$ (c) $(x+8)(x-2)$ (d) $x(x-16)$
2. $\frac{x^2-1}{x-1}$ in its simplest form is <span class="marks">[1]</span>
   (a) $x+1$ (b) $x-1$ (c) $x$ (d) $1$
3. The LCM of $x-2$ and $x^2-4$ is <span class="marks">[1]</span>
   (a) $x-2$ (b) $x+2$ (c) $x^2-4$ (d) $(x-2)(x^2-4)$
4. $\frac{3}{x}+\frac{2}{x}=$ <span class="marks">[1]</span>
   (a) $\frac{5}{2x}$ (b) $\frac{5}{x}$ (c) $\frac{6}{x}$ (d) $\frac{5}{x^2}$
5. $\frac{a}{b}\div\frac{c}{d}=$ <span class="marks">[1]</span>
   (a) $\frac{ac}{bd}$ (b) $\frac{ad}{bc}$ (c) $\frac{bc}{ad}$ (d) $\frac{ab}{cd}$

::: note Answers to Group A
**1.** (b) — difference of squares.
**2.** (a) — $\frac{(x+1)(x-1)}{x-1}=x+1$.
**3.** (c) — $x^2-4=(x-2)(x+2)$ already contains $x-2$.
**4.** (b) — same denominator, add numerators.
**5.** (b) — invert the divisor.
:::

**Group B — Short answer (2 marks each)**

1. Factorise $x^2+5x+6$. <span class="marks">[2]</span>
2. Simplify $\frac{x^2-9}{x^2+6x+9}$. <span class="marks">[2]</span>
3. Simplify $\frac{x}{x+1}+\frac{1}{x+1}$. <span class="marks">[2]</span>
4. Simplify $\frac{x+2}{x-3}\times\frac{x-3}{x^2-4}$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $(x+2)(x+3)$.
**2.** $\frac{(x+3)(x-3)}{(x+3)^2}=\frac{x-3}{x+3}$.
**3.** $\frac{x+1}{x+1}=1$.
**4.** $\frac{x+2}{x-3}\times\frac{x-3}{(x-2)(x+2)}=\frac{1}{x-2}$.
:::

**Group C — Short answer (3 marks each)**

1. Simplify $\frac{1}{x-1}+\frac{1}{x+1}$. <span class="marks">[3]</span>
2. Simplify $\frac{x^2-5x+6}{x^2-4}\div\frac{x-3}{x+2}$. <span class="marks">[3]</span>
3. Simplify $\frac{x}{x-2}-\frac{2}{x+2}$. <span class="marks">[3]</span>
4. Simplify $\left(x+\frac{1}{x}\right)^2-\left(x-\frac{1}{x}\right)^2$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\frac{2x}{x^2-1}$.
**2.** $\frac{(x-2)(x-3)}{(x-2)(x+2)}\times\frac{x+2}{x-3}=1$.
**3.** $\frac{x^2+4}{x^2-4}$.
**4.** $4$.
:::

**Group D — Long answer (4 marks each)**

1. Simplify $\frac{a}{a-b}-\frac{b}{a+b}-\frac{2ab}{a^2-b^2}$. <span class="marks">[4]</span>
2. Simplify $\frac{x^2+3x+2}{x^2+x-2}\times\frac{x^2-1}{x^2+2x}$. <span class="marks">[4]</span>
3. Simplify $\frac{1}{1-\frac{1}{1+\frac{1}{x}}}$. <span class="marks">[4]</span>
4. Solve $\frac{3}{x-1}-\frac{2}{x+1}=1$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $\frac{a-b}{a+b}$.
**2.** $\frac{(x+1)^2}{x(x+2)}$.
**3.** $x+1$.
**4.** $x=3$ or $x=-2$.
:::

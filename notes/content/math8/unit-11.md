---
subject: Mathematics
grade: 8
unit: 11
title: Algebraic Fraction
hours: 0
area: Compulsory Mathematics
---

An algebraic fraction is a fraction whose top, bottom or both contain letters.
Everything you already do with number fractions — cancelling, taking a common
denominator, multiplying and dividing — works in exactly the same way, with one
extra step in front: **factorise first**. Nothing can be cancelled until the top
and bottom are written as products, because cancelling is division and division
only removes whole factors.

::: key What this chapter asks of you
You should be able to reduce an algebraic fraction to its lowest terms, add and
subtract algebraic fractions by finding the LCM of the denominators, multiply
and divide them, and solve a simple equation that contains fractions.
:::

## 11.1 Reducing a fraction to its lowest terms

**Method.** Factorise the numerator and the denominator completely, cancel the
common factors, and write what is left.

$$\frac{a\times c}{b\times c}=\frac ab\qquad(c\ne0)$$

::: example Reducing with monomials
**Problem.** Simplify $\frac{12x^3y^2}{18x^2y^4}$.

**Solution.** Divide the numbers by their HCF 6, and subtract indices on the
letters:

$$\frac{12}{18}=\frac23,\qquad \frac{x^3}{x^2}=x,\qquad
\frac{y^2}{y^4}=\frac{1}{y^2}$$

$$\frac{12x^3y^2}{18x^2y^4}=\frac{2x}{3y^2}$$

**Answer.** $\frac{2x}{3y^2}$.

**Check.** Put $x=2$, $y=1$: the original is
$\frac{12\times8}{18\times4}=\frac{96}{72}=\frac43$, and the answer is
$\frac{2\times2}{3}=\frac43$ ✓.
:::

::: example Reducing after factorising
**Problem.** Simplify $\frac{x^2-9}{x^2+6x+9}$.

**Solution.** Factorise both parts:

$$x^2-9=(x+3)(x-3),\qquad x^2+6x+9=(x+3)^2$$

$$\frac{x^2-9}{x^2+6x+9}=\frac{(x+3)(x-3)}{(x+3)(x+3)}=\frac{x-3}{x+3}$$

**Answer.** $\frac{x-3}{x+3}$, with $x\ne-3$.

**Check.** Put $x=0$: the original is $\frac{-9}{9}=-1$, and the answer is
$\frac{-3}{3}=-1$ ✓.
:::

::: caution Factorise before you cancel
You may **not** cancel the $x^2$ in $\frac{x^2+4}{x^2+9}$ to get $\frac49$. The
$x^2$ is not a factor of either top or bottom; it is only one of two terms. Only
terms multiplied together can be cancelled. Write both parts as products first,
then cancel.
:::

## 11.2 Adding and subtracting algebraic fractions

**Method.**

1. Factorise every denominator.
2. Find the LCM of the denominators — this is the common denominator.
3. Rewrite each fraction with that denominator, multiplying top and bottom by
   whatever is missing.
4. Add or subtract the numerators.
5. Simplify, and factorise and cancel if possible.

::: example Adding with unlike denominators
**Problem.** Simplify $\frac{3}{x}+\frac{5}{y}$.

**Solution.** The LCM of $x$ and $y$ is $xy$.

$$\frac{3}{x}=\frac{3y}{xy},\qquad \frac{5}{y}=\frac{5x}{xy}$$

$$\frac{3}{x}+\frac{5}{y}=\frac{3y+5x}{xy}$$

**Answer.** $\frac{3y+5x}{xy}$.

**Check.** Put $x=1$, $y=1$: the original is $3+5=8$, and the answer is
$\frac{3+5}{1}=8$ ✓.
:::

::: example Subtracting with an algebraic LCM
**Problem.** Simplify $\frac{2}{x-1}-\frac{1}{x+1}$.

**Solution.** The LCM of $(x-1)$ and $(x+1)$ is their product, $(x-1)(x+1)$.

$$\frac{2}{x-1}=\frac{2(x+1)}{(x-1)(x+1)},\qquad
\frac{1}{x+1}=\frac{x-1}{(x-1)(x+1)}$$

Subtracting the numerators:

$$\frac{2(x+1)-(x-1)}{(x-1)(x+1)}=\frac{2x+2-x+1}{(x-1)(x+1)}
=\frac{x+3}{x^2-1}$$

**Answer.** $\frac{x+3}{x^2-1}$.

**Check.** Put $x=2$: the original is $\frac21-\frac13=\frac53$, and the answer
is $\frac{5}{4-1}=\frac53$ ✓.
:::

::: caution The bracket that must be kept
In $\frac{2}{x-1}-\frac{1}{x+1}$ the second numerator is $(x-1)$, and the sign in
front of it is a minus. The numerator therefore becomes
$2(x+1)\mathbf{-}(x-1)=2x+2-x+1=x+3$, **not** $2x+2-x-1=x+1$. Whenever a
fraction is subtracted, put the numerator in brackets before you subtract it.
:::

::: example Three denominators
**Problem.** Simplify $\frac{1}{x}+\frac{1}{2x}+\frac{1}{3x}$.

**Solution.** The LCM of $x$, $2x$ and $3x$ is $6x$. Rewrite each:

$$\frac{6}{6x}+\frac{3}{6x}+\frac{2}{6x}=\frac{11}{6x}$$

**Answer.** $\frac{11}{6x}$.

**Check.** Put $x=1$: $1+\frac12+\frac13=\frac{11}{6}$ ✓.
:::

::: example With a factorisable denominator
**Problem.** Simplify $\frac{1}{x^2-4}+\frac{1}{x+2}$.

**Solution.** Factorise the first denominator:
$x^2-4=(x-2)(x+2)$. The LCM is $(x-2)(x+2)$.

$$\frac{1}{(x-2)(x+2)}+\frac{x-2}{(x-2)(x+2)}
=\frac{1+x-2}{(x-2)(x+2)}=\frac{x-1}{x^2-4}$$

**Answer.** $\frac{x-1}{x^2-4}$.

**Check.** Put $x=3$: the original is $\frac15+\frac15=\frac25$, and the answer
is $\frac{2}{9-4}=\frac25$ ✓.
:::

## 11.3 Multiplying and dividing

Multiplication is the easiest operation: multiply the numerators, multiply the
denominators, then cancel.

Division: turn the second fraction upside down and multiply.

$$\frac ab\times\frac cd=\frac{ac}{bd},\qquad
\frac ab\div\frac cd=\frac ab\times\frac dc=\frac{ad}{bc}$$

::: example Multiplication
**Problem.** Simplify $\frac{x^2-4}{x+3}\times\frac{x+3}{x-2}$.

**Solution.** Factorise the difference of squares:
$x^2-4=(x-2)(x+2)$. Then

$$\frac{(x-2)(x+2)}{x+3}\times\frac{x+3}{x-2}=\frac{(x+2)}{1}=x+2$$

after cancelling $(x-2)$ and $(x+3)$.

**Answer.** $x+2$.

**Check.** Put $x=4$: the original is $\frac{12}{7}\times\frac{7}{2}=6$, and the
answer is $6$ ✓.
:::

::: example Division
**Problem.** Simplify $\frac{a^2-b^2}{a+b}\div\frac{a-b}{a}$.

**Solution.** Invert and multiply, having factorised
$a^2-b^2=(a+b)(a-b)$:

$$\frac{(a+b)(a-b)}{a+b}\times\frac{a}{a-b}
=\frac{(a-b)}{1}\times\frac{a}{(a-b)}=a$$

**Answer.** $a$.

**Check.** Put $a=3$, $b=1$: the original is $\frac{8}{4}\div\frac{2}{3}
=2\times\frac32=3$, and the answer is $a=3$ ✓.
:::

## 11.4 Equations containing fractions

Clear the denominators by multiplying every term by the LCM, then solve the
resulting simple equation.

::: example Solving a fractional equation
**Problem.** Solve $\frac{x}{2}+\frac{x}{3}=5$.

**Solution.** The LCM of 2 and 3 is 6. Multiply every term by 6:

$$6\times\frac{x}{2}+6\times\frac{x}{3}=6\times5$$

$$3x+2x=30\;\Longrightarrow\;5x=30\;\Longrightarrow\;x=6$$

**Answer.** $x=6$.

**Check.** $\frac62+\frac63=3+2=5$ ✓.
:::

::: example An equation with the unknown in a denominator
**Problem.** Solve $\frac{3}{x}=\frac{5}{x+2}$.

**Solution.** Cross-multiplying removes both denominators:

$$3(x+2)=5x\;\Longrightarrow\;3x+6=5x\;\Longrightarrow\;6=2x
\;\Longrightarrow\;x=3$$

**Answer.** $x=3$.

**Check.** $\frac33=1$ and $\frac{5}{5}=1$ ✓.

**Note.** Always state the values the variable may not take:
here $x\ne0$ and $x\ne-2$, and $x=3$ is allowed.
:::

::: tip The two-line check on every fraction sum
Put a convenient number — 1, 2 or 3 — into the original expression and into your
answer and see whether they agree. It takes fifteen seconds and it catches the
sign errors, the mis-copied terms and the wrong LCM, which is where nearly all
the marks in this chapter are lost.
:::

## 11.5 Why factorising comes first

An algebraic fraction is simplified by **factorising and cancelling common
factors** — never by cancelling across a plus or minus sign.

```figure caption="The three steps of simplifying an algebraic fraction. Skipping step 1 is what produces the classic wrong cancellation."
fig, ax = flow([("Factorise", "numerator"), ("Factorise", "denominator"),
                ("Cancel", "common factors"), ("State", "excluded values")],
               note="skipping step 1 is what produces the wrong cancellation")
```

::: caution The cancellation that is never allowed
$\frac{x+3}{x}$ does **not** simplify to $3$. You may cancel only a factor of
the *whole* numerator against a factor of the *whole* denominator. Since $x+3$
is a sum, not a product, nothing cancels.
:::

::: example Simplify and state the excluded values
**Question.** Simplify $\dfrac{x^2 - 4}{x^2 + 5x + 6}$ and state the values of
$x$ for which it is undefined.

**Answer.** Numerator $= (x+2)(x-2)$. Denominator $= (x+2)(x+3)$.
Cancelling $(x+2)$: $\dfrac{x-2}{x+3}$.
The original denominator is zero at $x = -2$ and $x = -3$, so the expression is
**undefined at $x = -2$ and $x = -3$**.
:::

::: example Adding two algebraic fractions
**Question.** Simplify $\dfrac{2}{x-1} + \dfrac{3}{x+2}$.

**Answer.** LCM of the denominators is $(x-1)(x+2)$.
$$\frac{2(x+2) + 3(x-1)}{(x-1)(x+2)} = \frac{2x + 4 + 3x - 3}{(x-1)(x+2)}
= \frac{5x + 1}{(x-1)(x+2)}$$
:::

::: note Activity — spot the error
Each line below contains one mistake. Working in pairs, find it and write the
correct simplification.
(i) $\frac{x+5}{5} = x$ &nbsp;&nbsp; (ii) $\frac{x^2-9}{x-3} = x-3$ &nbsp;&nbsp;
(iii) $\frac{2x}{2x+4} = \frac{1}{4}$ &nbsp;&nbsp;
(iv) $\frac{1}{x} + \frac{1}{y} = \frac{1}{x+y}$
:::

## Chapter summary

- Factorise the top and bottom before cancelling anything; only factors cancel.
- The LCM of the denominators is the common denominator; multiply top and bottom
  by whatever each fraction is missing.
- When subtracting, put the second numerator in brackets and distribute the
  minus sign.
- Multiply fractions straight across; divide by inverting the second fraction.
- Solve a fractional equation by multiplying every term by the LCM, and state
  the values the variable may not take.
- Check every answer numerically in the original expression.

## Practice questions

**Group A — Objective (1 mark each)**

1. $\frac{6x^2}{3x}$ in its lowest terms is <span class="marks">[1]</span>
   (a) $2x$ (b) $2x^2$ (c) $3x$ (d) $18x^3$
2. $\frac{1}{x}+\frac{1}{y}$ equals <span class="marks">[1]</span>
   (a) $\frac{2}{x+y}$ (b) $\frac{x+y}{xy}$ (c) $\frac{1}{xy}$ (d) $\frac{xy}{x+y}$
3. $\frac{x^2-1}{x-1}$ simplifies to <span class="marks">[1]</span>
   (a) $x-1$ (b) $x+1$ (c) $x^2$ (d) 1
4. $\frac ab\div\frac cd$ equals <span class="marks">[1]</span>
   (a) $\frac{ac}{bd}$ (b) $\frac{ad}{bc}$ (c) $\frac{ab}{cd}$ (d) $\frac{bd}{ac}$
5. In $\frac{x^2+4}{x^2+9}$ you may cancel
   <span class="marks">[1]</span>
   (a) $x^2$ (b) 4 and 9 (c) nothing (d) $x^4$
6. If $\frac{x}{3}=4$, then $x$ is <span class="marks">[1]</span>
   (a) 7 (b) 12 (c) $\frac43$ (d) 1

::: note Answers to Group A
**1.** (a) — divide numbers and subtract indices.
**2.** (b) — the common denominator is $xy$.
**3.** (b) — $x^2-1=(x+1)(x-1)$.
**4.** (b) — invert and multiply.
**5.** (c) — the $x^2$ terms are not factors.
**6.** (b) — multiply both sides by 3.
:::

**Group B — Short answer (2 marks each)**

1. Simplify $\frac{15a^3b^2}{25a^2b^4}$. <span class="marks">[2]</span>
2. Simplify $\frac{2}{x}+\frac{3}{2x}$. <span class="marks">[2]</span>
3. Simplify $\frac{x^2-16}{x+4}$. <span class="marks">[2]</span>
4. Solve $\frac{x}{4}+\frac{x}{6}=5$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\frac{3a}{5b^2}$.
**2.** $\frac{4}{2x}+\frac{3}{2x}=\frac{7}{2x}$.
**3.** $\frac{(x+4)(x-4)}{x+4}=x-4$.
**4.** Multiply by 12: $3x+2x=60$, so $5x=60$ and $x=12$.
:::

**Group C — Long answer (4 marks each)**

1. Simplify $\frac{3}{x-2}-\frac{2}{x+1}$, giving the answer as a single
   fraction, and check with $x=3$. <span class="marks">[4]</span>
2. Simplify $\frac{x^2-9}{x^2+5x+6}\times\frac{x+2}{x-3}$ and state the values
   of $x$ for which the expression is not defined.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** The LCM of $(x-2)$ and $(x+1)$ is $(x-2)(x+1)$.

$$\frac{3(x+1)-2(x-2)}{(x-2)(x+1)}
=\frac{3x+3-2x+4}{(x-2)(x+1)}=\frac{x+7}{x^2-x-2}$$

**Check with $x=3$:** the original is $\frac31-\frac{2}{4}=3-0.5=2.5$, and the
answer is $\frac{10}{9-3-2}=\frac{10}{4}=2.5$ ✓. Note the brackets around
$2(x-2)$: without them the numerator would be $3x+3-2x-4=x-1$, which is wrong.
**2.** Factorise everything first:
$x^2-9=(x-3)(x+3)$ and $x^2+5x+6=(x+2)(x+3)$. So

$$\frac{(x-3)(x+3)}{(x+2)(x+3)}\times\frac{x+2}{x-3}
=\frac{(x-3)(x+3)(x+2)}{(x+2)(x+3)(x-3)}=1$$

**Answer.** 1. **Not defined when** the original denominators vanish:
$x\ne-2$, $x\ne-3$ and $x\ne3$. At every other value the expression equals 1,
which is consistent: the numerator and denominator are the same product written
in a different order.
:::

**Extra practice**

**Group B (2 marks)**

**11.** Simplify: $\dfrac{x^2 - 16}{x + 4}$.
**12.** Simplify: $\dfrac{3a}{4} - \dfrac{a}{6}$.

**Group C (4 marks)**

**13.** Simplify $\dfrac{x^2 + 7x + 12}{x^2 - 9}$ and state where it is undefined.

::: note Extra practice — answers
**11.** $\frac{(x+4)(x-4)}{x+4} = x - 4$ (for $x \neq -4$).
**12.** LCM 12: $\frac{9a - 2a}{12} = \frac{7a}{12}$.
**13.** Numerator $= (x+3)(x+4)$; denominator $= (x+3)(x-3)$.
Cancelling: $\frac{x+4}{x-3}$. Undefined at $x = 3$ and $x = -3$.
**Answers to the spot-the-error activity.** (i) $\frac{x+5}{5}$ does not
simplify — 5 is not a factor of $x+5$. (ii) $\frac{(x+3)(x-3)}{x-3} = x+3$.
(iii) $\frac{2x}{2(x+2)} = \frac{x}{x+2}$. (iv) $\frac{1}{x}+\frac{1}{y} =
\frac{x+y}{xy}$.
:::

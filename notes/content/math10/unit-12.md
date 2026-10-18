---
subject: Mathematics
grade: 10
unit: 12
title: Equations
hours: 0
area: Compulsory Mathematics
---

An **equation** is a statement that two expressions are equal; to **solve** it is to find the value of the unknown that makes the statement true. Shopkeepers, engineers and farmers all meet problems of the form "two numbers together make 9 and multiply to 20". This chapter covers two families you need for the SEE: **pairs of linear equations** in two unknowns (solved by substitution, elimination or by a graph) and **quadratic equations** in one unknown (solved by factorisation, completing the square or the quadratic formula). Then we use both to solve word problems about numbers, ages, money, rectangles, triangles and speed.

::: key What the SEE asks from this chapter
Expect: (i) solve a pair of linear equations, sometimes with fractions; (ii) a **word problem** that you must first turn into equations; (iii) solve a **quadratic** by factorising or by the formula; (iv) a word problem on area, consecutive numbers, right triangles or speed that leads to a quadratic, where one root is rejected. Every solution should show: *let*, *form the equation*, *solve*, *check*, *answer in a sentence*.
:::

```photo id="math10/balance" caption="A two-pan balance. Solving an equation is precisely this: whatever you do to one side you must also do to the other, so that the two remain equal." width="84"
```

## 12.1 Equations: concepts, formulas and worked problems

### Pairs of linear equations

A linear equation in two unknowns, such as $2x+3y=12$, has infinitely many solutions $(x,y)$: each is a point on a straight line. Two such equations have, in general, **exactly one common solution** — the point where the two lines meet.

```figure caption="The solution of 2x + 3y = 12 and x − y = 1 is the point where the two lines cross: (3, 2)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.2))
x = np.linspace(-1, 7, 100)
ax.plot(x, (12 - 2*x)/3, color=ACCENT, lw=1.6, label='2x + 3y = 12')
ax.plot(x, x - 1, color='#dc2626', lw=1.6, label='x − y = 1')
ax.plot([3], [2], 'o', color=INK, ms=5)
ax.annotate('(3, 2)', xy=(3, 2), xytext=(3.6, 3.3), fontsize=9, arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.set_xlim(-1, 7); ax.set_ylim(-2, 6)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('y', fontsize=8.5)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
ax.legend(fontsize=8, frameon=False, loc='upper right')
fig.tight_layout(pad=0.4)
```

::: key Methods
| Method | Idea | Best when |
|---|---|---|
| Substitution | express one unknown from one equation and put it in the other | one equation has $x=\dots$ or a coefficient 1 |
| Elimination | multiply to make a coefficient equal, then add or subtract | both equations are in the form $ax+by=c$ |
| Graph | draw both lines; read the crossing point | a picture is requested |

After finding one unknown, substitute back to find the other, then **check in both equations**.
:::

::: example Substitution
**Problem.** Solve $2x+3y=12$ and $x-y=1$.

**Solution.** From the second equation, $x=y+1$. Substitute into the first:

$$ 2(y+1)+3y=12 \;\Rightarrow\; 5y=10 \;\Rightarrow\; y=2 $$

Then $x=y+1=3$. **Check.** $2(3)+3(2)=12$ ✓ and $3-2=1$ ✓. So $x=3,\ y=2$.
:::

::: example Elimination
**Problem.** Solve $3x-2y=5$ and $4x+3y=18$.

**Solution.** Make the $y$-coefficients equal in size: multiply the first by 3 and the second by 2.

$$ 9x-6y=15 \qquad 8x+6y=36 $$

Add: $17x=51$, so $x=3$. Put $x=3$ in the first equation: $9-2y=5$, so $y=2$. **Check.** $4(3)+3(2)=18$ ✓.
:::

::: example Equations with fractions
**Problem.** Solve $\frac{x}{2}+\frac{y}{3}=4$ and $\frac{x}{6}+\frac{y}{3}=2$.

**Solution.** Subtract the second from the first so that $y$ disappears:

$$ \frac{x}{2}-\frac{x}{6}=2 \;\Rightarrow\; \frac{3x-x}{6}=2 \;\Rightarrow\; \frac{x}{3}=2 \;\Rightarrow\; x=6 $$

From the first equation, $3+\frac{y}{3}=4$, so $y=3$. **Check.** $\frac{6}{6}+\frac{3}{3}=2$ ✓.
:::

::: caution Common mistakes
- Changing only one side when multiplying an equation: multiply **every** term on both sides.
- Sign errors when subtracting equations — if in doubt, change the signs of the whole second equation and add.
- Forgetting to find the second unknown. A pair of equations needs *two* values.
- Not checking in **both** original equations.
:::

### Word problems leading to linear equations

Choose letters for the two things you want to find, translate each sentence into an equation, solve, and reply in words.

::: example Cost of pens and copies
**Problem.** Three pens and two copies cost Rs 70; two pens and three copies cost Rs 80. Find the price of one pen and of one copy.

**Solution.** Let a pen cost Rs $p$ and a copy Rs $c$.

$$ 3p+2c=70 \qquad 2p+3c=80 $$

Multiply the first by 3 and the second by 2: $9p+6c=210$ and $4p+6c=160$. Subtract: $5p=50$, so $p=10$. Then $30+2c=70$ gives $c=20$.

A pen costs Rs 10 and a copy costs Rs 20. **Check.** $2(10)+3(20)=80$ ✓.
:::

::: example Ages
**Problem.** The sum of the ages of a father and his son is 50 years. Five years ago the father was nine times as old as the son. Find their present ages.

**Solution.** Let the father be $F$ and the son $S$. Then $F+S=50$ and $F-5=9(S-5)$, i.e. $F=9S-40$. Substitute:

$$ (9S-40)+S=50 \;\Rightarrow\; 10S=90 \;\Rightarrow\; S=9 $$

So $F=41$. **Check.** Five years ago: $36$ and $4$; $36=9\times4$ ✓. The father is 41 and the son is 9.
:::

::: example Digits
**Problem.** The sum of the digits of a two-digit number is 9. If the digits are reversed, the number increases by 27. Find the number.

**Solution.** Let the tens digit be $x$ and the units digit $y$; the number is $10x+y$. Then $x+y=9$. The reversed number is $10y+x$, so

$$ (10y+x)-(10x+y)=27 \;\Rightarrow\; 9y-9x=27 \;\Rightarrow\; y-x=3 $$

Adding to $x+y=9$: $2y=12$, $y=6$, $x=3$. The number is **36** (reversed: 63, and $63-36=27$ ✓).
:::

### Quadratic equations

A **quadratic equation** has the standard form

$$ ax^2+bx+c=0,\qquad a\neq0 $$

A number that satisfies it is a **root**. A quadratic has at most two real roots.

::: key Zero product rule
If $p\times q=0$ then $p=0$ or $q=0$.

So after moving everything to one side and factorising, set each bracket equal to 0. The right-hand side **must be 0** before you factorise.
:::

### Solving by factorisation

::: example Simple quadratic
**Problem.** Solve $x^2-5x+6=0$.

**Solution.** Two numbers with product $6$ and sum $-5$ are $-2$ and $-3$. So $(x-2)(x-3)=0$, giving $x=2$ or $x=3$.
:::

::: example Leading coefficient not 1
**Problem.** Solve $2x^2-7x+3=0$.

**Solution.** $2\times3=6$; split $-7x$ as $-6x-x$:

$$ 2x^2-6x-x+3=2x(x-3)-1(x-3)=(x-3)(2x-1)=0 $$

So $x=3$ or $x=\frac{1}{2}$.
:::

::: example Bring to standard form first
**Problem.** Solve $x(x+7)=60$.

**Solution.** Expand and move all terms to the left: $x^2+7x-60=0$. Two numbers with product $-60$ and sum $7$ are $12$ and $-5$:

$$ (x+12)(x-5)=0 \;\Rightarrow\; x=-12 \text{ or } x=5 $$
:::

::: example A common factor
**Problem.** Solve $3x^2=12x$.

**Solution.** $3x^2-12x=0$, so $3x(x-4)=0$ and $x=0$ or $x=4$. (Never divide both sides by $x$; you would lose the root $x=0$.)
:::

### Completing the square and the quadratic formula

When the quadratic does not factorise neatly we use a formula that works for every quadratic.

::: derivation The quadratic formula
We turn $ax^2+bx+c=0$ into a perfect square on the left, then take square roots.

**Step 1 — divide by $a$.**

$$ x^2+\frac{b}{a}x+\frac{c}{a}=0 $$

**Step 2 — move the constant and add $\left(\frac{b}{2a}\right)^2$ to both sides.**

$$ x^2+\frac{b}{a}x+\frac{b^2}{4a^2}=\frac{b^2}{4a^2}-\frac{c}{a} $$

**Step 3 — left side is a perfect square; combine the right side.**

$$ \left(x+\frac{b}{2a}\right)^2=\frac{b^2-4ac}{4a^2} $$

**Step 4 — take square roots.**

$$ x+\frac{b}{2a}=\pm\frac{\sqrt{b^2-4ac}}{2a} $$

**Result.**

$$ x=\frac{-b\pm\sqrt{b^2-4ac}}{2a} $$

**What it means.** $D=b^2-4ac$ is the **discriminant**. If $D>0$ there are two real roots; if $D=0$ there is one repeated root; if $D<0$ there is no real root.
:::

```figure caption="y = x² − 5x + 6 meets the x-axis at x = 2 and x = 3 — the roots of the equation x² − 5x + 6 = 0."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.0))
x = np.linspace(0.2, 4.8, 200)
ax.plot(x, x**2 - 5*x + 6, color=ACCENT, lw=1.8)
ax.plot([2, 3], [0, 0], 'o', color='#dc2626', ms=5)
ax.text(1.7, 0.45, 'x = 2', fontsize=8.5, color='#dc2626', ha='center')
ax.text(3.3, 0.45, 'x = 3', fontsize=8.5, color='#dc2626', ha='center')
ax.plot([2.5], [-0.25], 'o', color=INK, ms=3.5)
ax.text(2.55, -0.65, 'lowest point (2.5, −0.25)', fontsize=8, ha='center')
ax.axhline(0, color=INK, lw=0.8)
ax.set_xlim(0.2, 4.8); ax.set_ylim(-1.1, 5)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('y', fontsize=8.5)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
fig.tight_layout(pad=0.4)
```

::: example Completing the square
**Problem.** Solve $x^2-4x+1=0$ by completing the square.

**Solution.** Move the constant: $x^2-4x=-1$. Add $\left(\frac{4}{2}\right)^2=4$ to both sides:

$$ x^2-4x+4=3 \;\Rightarrow\; (x-2)^2=3 \;\Rightarrow\; x-2=\pm\sqrt{3} $$

So $x=2+\sqrt{3}$ or $x=2-\sqrt{3}$.
:::

::: example Using the formula
**Problem.** Solve $2x^2+3x-1=0$.

**Solution.** $a=2,\ b=3,\ c=-1$. The discriminant is $b^2-4ac=9+8=17$.

$$ x=\frac{-3\pm\sqrt{17}}{4} $$

Numerically $x\approx0.78$ or $x\approx-1.78$.
:::

::: example Roots of a quadratic that factorises
**Problem.** Solve $3x^2-x-2=0$ using the formula.

**Solution.** $a=3,\ b=-1,\ c=-2$. $D=1+24=25$.

$$ x=\frac{1\pm5}{6}\;\Rightarrow\; x=1 \text{ or } x=-\frac{2}{3} $$
:::

::: example No real roots
**Problem.** Does $x^2+2x+5=0$ have real roots?

**Solution.** $D=b^2-4ac=4-20=-16<0$, so there is no real root.
:::

### Equations that reduce to quadratics

::: example Fraction equation
**Problem.** Solve $x+\frac{1}{x}=\frac{10}{3}$.

**Solution.** Multiply every term by $3x$: $3x^2+3=10x$, so $3x^2-10x+3=0$. Then $(3x-1)(x-3)=0$ and $x=\frac{1}{3}$ or $x=3$.
:::

::: example A square root
**Problem.** Solve $\sqrt{x+6}=x$.

**Solution.** Square both sides: $x+6=x^2$, so $x^2-x-6=0$, $(x-3)(x+2)=0$, giving $x=3$ or $x=-2$. Check each in the original equation: $x=3$: $\sqrt{9}=3$ ✓. $x=-2$: $\sqrt{4}=2\ne-2$, so $-2$ is **rejected**. Answer: $x=3$.
:::

::: example Quadratic in $x^2$
**Problem.** Solve $x^4-13x^2+36=0$.

**Solution.** Let $y=x^2$: $y^2-13y+36=0$, $(y-4)(y-9)=0$, so $y=4$ or $9$. Therefore $x=\pm2$ or $x=\pm3$.
:::

### Word problems leading to quadratics

::: example Consecutive numbers
**Problem.** The product of two consecutive positive integers is 156. Find them.

**Solution.** Let the numbers be $x$ and $x+1$: $x(x+1)=156$, so $x^2+x-156=0$. Factorise: $(x+13)(x-12)=0$, so $x=12$ (the root $-13$ is not positive). The numbers are 12 and 13.
:::

::: example Rectangle
**Problem.** The length of a rectangle is 7 m more than its breadth, and its area is 60 m². Find its dimensions.

**Solution.** Let the breadth be $x$ m. Then $x(x+7)=60$, so $x^2+7x-60=0$ and $(x+12)(x-5)=0$. A length cannot be negative, so $x=5$. The rectangle is 5 m by 12 m.
:::

::: example Right-angled triangle
**Problem.** The hypotenuse of a right-angled triangle is 13 cm and one side is 7 cm longer than the other. Find the sides.

**Solution.** Let the shorter side be $x$. By Pythagoras, $x^2+(x+7)^2=13^2$:

$$ 2x^2+14x+49=169 \;\Rightarrow\; x^2+7x-60=0 \;\Rightarrow\; (x+12)(x-5)=0 $$

So $x=5$ and the other side is 12 cm. (Check: $25+144=169$ ✓.)
:::

::: example Speed and time
**Problem.** A train travels 120 km at a steady speed. If its speed were 10 km/h more, the journey would take 1 hour less. Find its speed.

**Solution.** Let the speed be $x$ km/h. Time $=\frac{\text{distance}}{\text{speed}}$, so

$$ \frac{120}{x}-\frac{120}{x+10}=1 $$

Multiply by $x(x+10)$: $120(x+10)-120x=x(x+10)$, i.e. $1200=x^2+10x$. Then $x^2+10x-1200=0$, $(x+40)(x-30)=0$. Speed cannot be negative, so $x=30$ km/h.
:::

::: example Sum and product of two numbers
**Problem.** Two numbers add up to 9 and their product is 20. Find them.

**Solution.** Let one number be $x$; the other is $9-x$. Then $x(9-x)=20$, so $x^2-9x+20=0$, $(x-4)(x-5)=0$. The numbers are 4 and 5.
:::

::: example A pair with one quadratic equation
**Problem.** Solve $2x+y=7$ and $x^2+y=10$.

**Solution.** From the first, $y=7-2x$. Substitute into the second: $x^2+7-2x=10$, so $x^2-2x-3=0$, $(x-3)(x+1)=0$. If $x=3$, $y=1$; if $x=-1$, $y=9$. Solutions: $(3,1)$ and $(-1,9)$.
:::

## 12.2 Exercises of the SEE type

### Method for any question

1. Read twice; underline what is asked. Write "Let …".
2. Translate each sentence to an equation. Two unknowns need two equations.
3. Solve: linear — elimination or substitution; quadratic — factorise, else use the formula.
4. **Reject** roots that are impossible (negative length, age, speed).
5. Check in the words of the problem and answer in a sentence with units.

::: example SEE type: ages with a quadratic
**Problem.** The product of the ages of a boy and his sister is 80. The boy is 2 years older than his sister. Find their ages.

**Solution.** Let the sister's age be $x$. Then $x(x+2)=80$, $x^2+2x-80=0$, $(x+10)(x-8)=0$. So $x=8$; the sister is 8 and the boy is 10.
:::

::: example SEE type: fixing the price
**Problem.** A shopkeeper sold 5 kg of rice and 3 kg of lentils for Rs 1,050 and 3 kg of rice and 5 kg of lentils for Rs 1,150. Find the price per kg of each.

**Solution.** Let rice cost Rs $r$ per kg and lentils Rs $l$ per kg: $5r+3l=1050$ and $3r+5l=1150$. Add: $8r+8l=2200$, so $r+l=275$. Subtract: $2r-2l=-100$, so $r-l=-50$. Hence $r=112.5$ and $l=162.5$.

Rice costs Rs 112.50 and lentils Rs 162.50 per kg. **Check.** $5(112.5)+3(162.5)=562.5+487.5=1050$ ✓.
:::

## Chapter summary

- A pair of linear equations: solve by substitution, elimination or graph; check in both.
- Word problems: choose letters, form equations, solve, answer in words.
- Quadratic standard form $ax^2+bx+c=0$; zero product rule after factorising.
- Completing the square: add $\left(\frac{b}{2a}\right)^2$ to both sides.
- Quadratic formula $x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$; discriminant $D=b^2-4ac$: $D>0$ two roots, $D=0$ one root, $D<0$ no real root.
- Reject answers that are impossible in the context.
- When squaring an equation containing a square root, check every root in the original.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The solution of $x+y=5$ and $x-y=1$ is <span class="marks">[1]</span>
   (a) (2, 3) (b) (3, 2) (c) (4, 1) (d) (1, 4)
2. The roots of $x^2-9=0$ are <span class="marks">[1]</span>
   (a) 9 only (b) 3 only (c) $\pm3$ (d) $\pm9$
3. For $x^2+4x+4=0$ the discriminant is <span class="marks">[1]</span>
   (a) 0 (b) 4 (c) 16 (d) $-16$
4. The quadratic formula is <span class="marks">[1]</span>
   (a) $\frac{-b\pm\sqrt{b^2+4ac}}{2a}$ (b) $\frac{-b\pm\sqrt{b^2-4ac}}{2a}$ (c) $\frac{b\pm\sqrt{b^2-4ac}}{2a}$ (d) $\frac{-b\pm\sqrt{b^2-4ac}}{a}$
5. How many real roots does $x^2+1=0$ have? <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) 4

::: note Answers to Group A
**1.** (b) — adding gives $2x=6$.
**2.** (c) — $x^2=9$.
**3.** (a) — $16-16=0$.
**4.** (b).
**5.** (a) — $D=-4<0$.
:::

**Group B — Short answer (2 marks each)**

1. Solve $x+y=7$ and $x-y=3$. <span class="marks">[2]</span>
2. Solve $x^2-5x+6=0$. <span class="marks">[2]</span>
3. Find the discriminant of $2x^2-3x+5=0$ and state whether it has real roots. <span class="marks">[2]</span>
4. Two numbers add to 15 and differ by 3. Find them. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $2x=10$, $x=5$, $y=2$.
**2.** $(x-2)(x-3)=0$, $x=2,3$.
**3.** $D=9-40=-31<0$: no real roots.
**4.** $x+y=15$, $x-y=3$ gives $x=9$, $y=6$.
:::

**Group C — Short answer (3 marks each)**

1. Solve $3x-2y=5$ and $4x+3y=18$. <span class="marks">[3]</span>
2. Solve $2x^2-7x+3=0$. <span class="marks">[3]</span>
3. Solve $x^2-4x+1=0$ using the quadratic formula. <span class="marks">[3]</span>
4. The sum of two numbers is 9 and their product is 20. Find the numbers. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $x=3,\ y=2$.
**2.** $(x-3)(2x-1)=0$: $x=3$ or $\frac{1}{2}$.
**3.** $D=16-4=12$, $x=\frac{4\pm2\sqrt{3}}{2}=2\pm\sqrt{3}$.
**4.** $x(9-x)=20$ gives $x^2-9x+20=0$: numbers 4 and 5.
:::

**Group D — Long answer (4 marks each)**

1. The length of a rectangle is 7 m more than its breadth and its area is 60 m². Find its perimeter. <span class="marks">[4]</span>
2. A train covers 120 km at speed $x$ km/h. At $(x+10)$ km/h it would take 1 hour less. Find $x$. <span class="marks">[4]</span>
3. The sum of the digits of a two-digit number is 9; reversing the digits adds 27 to the number. Find the number. <span class="marks">[4]</span>
4. The hypotenuse of a right-angled triangle is 13 cm; one side is 7 cm longer than the other. Find its area. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Breadth 5 m, length 12 m; perimeter $2(5+12)=34$ m.
**2.** $x^2+10x-1200=0$, $x=30$ km/h.
**3.** 36.
**4.** Sides 5 cm and 12 cm; area $\frac{1}{2}\times5\times12=30\text{ cm}^2$.
:::

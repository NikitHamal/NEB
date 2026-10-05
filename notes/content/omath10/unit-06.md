---
subject: Optional Mathematics
grade: 10
unit: 6
title: Angle between Two Lines and Pair of Straight Lines
hours: 0
area: Units
---

Roads cross, rafters meet, and the two edges of a ramp make an angle with the ground. In coordinate geometry we describe every such line by an equation, and the angle between two lines can be found from their **slopes** alone, with no protractor. This chapter first derives the formula for the angle between two lines and the conditions for lines to be parallel or perpendicular. It then shows how two lines through the origin can be written as **one** equation, and how to read the angle between them straight from the coefficients of that equation.

::: key What the SEE asks from this chapter
Expect (i) the angle between two given lines, or the slope of a line that makes a given angle with another line; (ii) the value of $k$ that makes two lines parallel or perpendicular; (iii) the combined equation of two given lines through the origin, or the two lines hidden in an equation like $2x^2+7xy+3y^2=0$; (iv) the angle between the pair, or the condition that the pair is perpendicular ($a+b=0$) or coincident ($h^2=ab$). Everything in the chapter depends on one fact: **slope $=\tan$ of the inclination**.
:::

```photo id="omath10/railway-vanishing" caption="Rails meeting at a vanishing point. Any two non-parallel straight lines meet at an angle, and the tangent of that angle is fixed by their gradients." width="64"
```

## 6.1 Angle between two straight lines

### Slope and inclination: a quick review

The **inclination** $\theta$ of a line is the angle it makes with the positive direction of the $x$-axis, measured anticlockwise ($0^\circ\le\theta<180^\circ$). Its **slope** is

$$ m=\tan\theta $$

| Line | Slope formula |
|---|---|
| Through $(x_1,y_1)$ and $(x_2,y_2)$ | $m=\dfrac{y_2-y_1}{x_2-x_1}$ |
| $y=mx+c$ | $m$ (the coefficient of $x$) |
| $ax+by+c=0$ | $m=-\dfrac{a}{b}$ |
| Parallel to the $x$-axis | $m=0$ |
| Parallel to the $y$-axis | slope undefined ($\theta=90^\circ$) |

### The angle between two lines

::: derivation Angle between two lines in terms of their slopes
We want the angle $\theta$ between two lines whose slopes $m_1$ and $m_2$ we know.

**Setting up.** Let the two lines meet at a point and have inclinations $\theta_1$ and $\theta_2$, with $\theta_1>\theta_2$. So $m_1=\tan\theta_1$ and $m_2=\tan\theta_2$. Let $\theta$ be the angle between them.

**Step 1 — relate the angles.** The inclination $\theta_1$ is an exterior angle of the triangle formed by the two lines and the $x$-axis. An exterior angle equals the sum of the two opposite interior angles, so

$$ \theta_1=\theta_2+\theta \quad\Longrightarrow\quad \theta=\theta_1-\theta_2 $$

**Step 2 — take tangents.** Use the formula for $\tan(A-B)$:

$$ \tan\theta=\tan(\theta_1-\theta_2)=\frac{\tan\theta_1-\tan\theta_2}{1+\tan\theta_1\tan\theta_2}=\frac{m_1-m_2}{1+m_1m_2} $$

**Step 3 — the second angle.** The two lines make two angles, $\theta$ and $180^\circ-\theta$, and $\tan(180^\circ-\theta)=-\tan\theta$. So the other angle has the tangent $-\dfrac{m_1-m_2}{1+m_1m_2}$.

**Result.**

$$ \tan\theta=\pm\frac{m_1-m_2}{1+m_1m_2} $$

**What it means.** The plus sign gives one of the two angles and the minus sign gives the other. If the value of $\dfrac{m_1-m_2}{1+m_1m_2}$ is positive the angle is acute; if it is negative the angle is obtuse. Taking the positive value always gives the **acute** angle between the lines.
:::

```figure caption="Two lines with inclinations $\theta_1$ and $\theta_2$. The angle between them is $\theta=\theta_1-\theta_2$, because $\theta_1$ is an exterior angle of the shaded triangle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.9))
t1, t2 = np.radians(62), np.radians(20)
x0 = 1.0
px = x0*np.tan(t1)/(np.tan(t1)-np.tan(t2))
py = np.tan(t2)*px
ax.annotate('', xy=(5.4, 0), xytext=(-0.6, 0), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.9))
ax.fill([0, x0, px], [0, 0, py], color='#dbeafe', zorder=0)
ax.plot([0, 4.6], [0, 4.6*np.tan(t2)], color=ACCENT, lw=1.6)
ax.plot([x0-0.6/np.tan(t1), px+0.9], [-0.6, py+0.9*np.tan(t1)], color=SERIES[1], lw=1.6)
ax.plot([px], [py], 'o', color=INK, ms=3.5)
th = np.linspace(0, t2, 30)
ax.plot(0.9*np.cos(th), 0.9*np.sin(th), color=INK, lw=0.8)
ax.text(1.0, 0.09, r'$\theta_2$', fontsize=9)
th = np.linspace(0, t1, 40)
ax.plot(x0+0.6*np.cos(th), 0.6*np.sin(th), color=INK, lw=0.8)
ax.text(x0+0.68, 0.38, r'$\theta_1$', fontsize=9)
th = np.linspace(t2, t1, 30)
ax.plot(px+0.6*np.cos(th), py+0.6*np.sin(th), color=INK, lw=0.8)
ax.text(px+0.55, py+0.2, r'$\theta$', fontsize=9)
ax.text(4.7, 4.6*np.tan(t2), r'$m_2=\tan\theta_2$', fontsize=8.5, color=ACCENT, va='center')
ax.text(px+0.55, py+0.9*np.tan(t1)+0.25, r'$m_1=\tan\theta_1$', fontsize=8.5, color=SERIES[1])
ax.set_xlim(-0.8, 6.6); ax.set_ylim(-0.7, 3.6); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: key Angle between two lines
For slopes $m_1$ and $m_2$:

$$ \tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right| \qquad\text{(acute angle)} $$

For lines $a_1x+b_1y+c_1=0$ and $a_2x+b_2y+c_2=0$ the slopes are $-\dfrac{a_1}{b_1}$ and $-\dfrac{a_2}{b_2}$, which gives

$$ \tan\theta=\left|\frac{a_1b_2-a_2b_1}{a_1a_2+b_1b_2}\right| $$

| Condition | In slopes | In coefficients |
|---|---|---|
| **Parallel** ($\theta=0^\circ$) | $m_1=m_2$ | $\dfrac{a_1}{a_2}=\dfrac{b_1}{b_2}$ |
| **Perpendicular** ($\theta=90^\circ$) | $m_1m_2=-1$ | $a_1a_2+b_1b_2=0$ |
:::

Why does perpendicularity give $m_1m_2=-1$? When the lines are at $90^\circ$, $\tan\theta$ is undefined, so the denominator $1+m_1m_2$ must be $0$. Hence $m_1m_2=-1$. If $m_1=m_2$ the numerator is $0$, so $\tan\theta=0$ and the lines are parallel (or the same line).

::: caution A vertical line has no slope
If one line is vertical (say $x=3$) its slope does not exist, so the formula cannot be used. A line perpendicular to it is horizontal ($y=\text{constant}$) and the angle with any other line is found from its inclination directly. Also, never forget the **modulus** when the question says "the acute angle": a negative answer for $\tan\theta$ means you found the obtuse angle.
:::

::: example Angle between two lines given by slopes
**Problem.** Find the angle between the lines $y=2x+3$ and $y=\dfrac13x-5$.

**Solution.** Here $m_1=2$ and $m_2=\dfrac13$.

$$ \tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|=\left|\frac{2-\frac13}{1+2\times\frac13}\right|=\frac{\frac53}{\frac53}=1 $$

So $\theta=45^\circ$. The angle between the lines is $45^\circ$.
:::

::: example Acute and obtuse angles from the general form
**Problem.** Find the acute and the obtuse angle between $2x+y-3=0$ and $x-3y+1=0$.

**Solution.** For $2x+y-3=0$: $a_1=2,\ b_1=1$, so $m_1=-2$.
For $x-3y+1=0$: $a_2=1,\ b_2=-3$, so $m_2=\dfrac13$.

$$ \tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|=\left|\frac{-2-\frac13}{1-\frac23}\right|=\left|\frac{-\frac73}{\frac13}\right|=7 $$

So the acute angle is $\theta=\tan^{-1}7\approx 81.87^\circ$, and the obtuse angle is $180^\circ-81.87^\circ\approx 98.13^\circ$.
:::

```figure caption="The lines $2x+y-3=0$ and $x-3y+1=0$ meet at $\left(\frac{8}{7},\frac{5}{7}\right)$. They make an acute angle of about $81.9^\circ$ and an obtuse angle of about $98.1^\circ$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.2))
x = np.linspace(-1.5, 3.5, 100)
ax.plot(x, 3-2*x, color=ACCENT, lw=1.6, label='2x + y − 3 = 0')
ax.plot(x, (x+1)/3, color=SERIES[1], lw=1.6, label='x − 3y + 1 = 0')
ax.plot([8/7], [5/7], 'o', color=INK, ms=4)
ax.text(1.3, 0.5, '(8/7, 5/7)', fontsize=8.5)
ax.annotate('acute\n81.9°', xy=(1.7, 1.3), fontsize=8.5, color=INK)
ax.annotate('obtuse\n98.1°', xy=(-0.5, 0.3), fontsize=8.5, color=INK, ha='center')
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-1.5, 3.5); ax.set_ylim(-1.2, 3.6); ax.set_aspect('equal')
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
ax.legend(fontsize=8, loc='upper right', frameon=False)
fig.tight_layout(pad=0.4)
```

::: example Angle of a triangle from coordinates
**Problem.** Find the angle at $A$ of the triangle with vertices $A(1,1)$, $B(5,1)$ and $C(3,5)$.

**Solution.** Slope of $AB=\dfrac{1-1}{5-1}=0$. Slope of $AC=\dfrac{5-1}{3-1}=2$.

$$ \tan A=\left|\frac{2-0}{1+2\times0}\right|=2 \quad\Longrightarrow\quad A=\tan^{-1}2\approx 63.43^\circ $$

By symmetry $B\approx63.43^\circ$ too, so $C\approx 180^\circ-2\times63.43^\circ\approx 53.13^\circ$.
:::

::: example Parallel and perpendicular lines
**Problem.** (a) Find $k$ so that $3x+ky=5$ is perpendicular to $2x-5y+1=0$. (b) Find $k$ so that it is parallel to it. (c) Find the line through $(2,3)$ perpendicular to $3x-4y+5=0$.

**Solution.** (a) Perpendicular: $a_1a_2+b_1b_2=0$, so $3\times2+k\times(-5)=0$, giving $k=\dfrac65$.

(b) Parallel: $\dfrac{a_1}{a_2}=\dfrac{b_1}{b_2}$, so $\dfrac32=\dfrac{k}{-5}$, giving $k=-\dfrac{15}{2}$.

(c) The slope of $3x-4y+5=0$ is $\dfrac34$. A perpendicular line has slope $-\dfrac43$. Its equation through $(2,3)$ is

$$ y-3=-\frac43(x-2) \;\Rightarrow\; 3y-9=-4x+8 \;\Rightarrow\; 4x+3y-17=0 $$

Check: $4(2)+3(3)-17=0$. ✓
:::

::: example A line at a given angle to another line
**Problem.** Find the equations of the two lines through $(1,2)$ that make an angle of $45^\circ$ with the line $x-2y+3=0$.

**Solution.** The given line has slope $\dfrac12$. Let the required slope be $m$. Then $\tan45^\circ=1$, so

$$ \left|\frac{m-\frac12}{1+\frac{m}{2}}\right|=1 $$

*Case 1:* $m-\dfrac12=1+\dfrac m2$, so $\dfrac m2=\dfrac32$ and $m=3$. Line: $y-2=3(x-1)$, i.e. $3x-y-1=0$.

*Case 2:* $m-\dfrac12=-1-\dfrac m2$, so $\dfrac{3m}{2}=-\dfrac12$ and $m=-\dfrac13$. Line: $y-2=-\dfrac13(x-1)$, i.e. $x+3y-7=0$.

The two lines are $3x-y-1=0$ and $x+3y-7=0$. (They are perpendicular, since $3\times(-\frac13)=-1$: of course, because they lie $45^\circ$ on either side of the given line.)
:::

::: tip Setting out the angle question
(1) Write each slope, converting $ax+by+c=0$ to $m=-a/b$. (2) Write the formula with its modulus. (3) Substitute, simplifying numerator and denominator separately. (4) Give the angle in degrees, noting acute or obtuse if asked. Marks go to the slopes, the formula and the final angle.
:::

## 6.2 Pair of straight lines through the origin

### A homogeneous equation of the second degree

Take two lines through the origin, $y-2x=0$ and $y-3x=0$. Multiply the left sides:

$$ (y-2x)(y-3x)=y^2-5xy+6x^2=0 $$

A point lies on this curve if it lies on **either** line, so this one equation stands for both lines. Every term has degree $2$ in $x$ and $y$ together ($x^2$, $xy$, $y^2$) and there is no constant or first-degree term. Such an equation is called a **homogeneous equation of the second degree**. Its standard form is

$$ ax^2+2hxy+by^2=0 $$

::: definition Homogeneous equation of second degree
An equation in $x$ and $y$ in which every term is of degree two, $ax^2+2hxy+by^2=0$, represents a **pair of straight lines passing through the origin** (real and distinct, real and coincident, or imaginary, depending on $h^2-ab$).
:::

::: derivation Why $ax^2+2hxy+by^2=0$ is a pair of lines through the origin
**Step 1 — divide by $x^2$.** For $x\neq0$ put $m=\dfrac yx$, the slope of the line joining the origin to the point $(x,y)$:

$$ b\,m^2+2h\,m+a=0 $$

**Step 2 — solve the quadratic.** This quadratic in $m$ has two roots $m_1$ and $m_2$. So every point of the curve satisfies $\dfrac yx=m_1$ or $\dfrac yx=m_2$, that is, $y=m_1x$ or $y=m_2x$.

**Step 3 — sum and product of roots.**

$$ m_1+m_2=-\frac{2h}{b}, \qquad m_1m_2=\frac ab $$

**Result.** The equation represents the two lines $y=m_1x$ and $y=m_2x$ through the origin.

**What it means.** The roots are real and different when $h^2-ab>0$ (two lines), real and equal when $h^2=ab$ (one line, counted twice) and non-real when $h^2<ab$ (only the origin satisfies it).
:::

### Finding the combined equation

To write one equation for two lines through the origin, **multiply** their equations (each written as $\text{expression}=0$).

::: example Combined equation from two lines
**Problem.** Find the combined equation of the lines $2x-y=0$ and $x+3y=0$.

**Solution.**

$$ (2x-y)(x+3y)=2x^2+6xy-xy-3y^2=2x^2+5xy-3y^2 $$

The combined equation is $2x^2+5xy-3y^2=0$.
:::

::: example Combined equation from slopes
**Problem.** Find the equation of the pair of lines through the origin with slopes $2$ and $-3$.

**Solution.** The lines are $y=2x$ and $y=-3x$, i.e. $y-2x=0$ and $y+3x=0$.

$$ (y-2x)(y+3x)=y^2+3xy-2xy-6x^2=y^2+xy-6x^2 $$

The pair is $6x^2-xy-y^2=0$.
:::

### Separating a pair into its two lines

To split $ax^2+2hxy+by^2=0$ into two lines, **factorise** the left side into two linear factors and equate each to zero. If it does not factorise by inspection, solve $bm^2+2hm+a=0$ and use $y=mx$.

::: example Separating the lines
**Problem.** Find the separate equations of the lines given by $6x^2-5xy-6y^2=0$.

**Solution.** Factorise: $6x^2-5xy-6y^2=(2x-3y)(3x+2y)$. Check: $6x^2+4xy-9xy-6y^2$. ✓

So the lines are $2x-3y=0$ and $3x+2y=0$, with slopes $\dfrac23$ and $-\dfrac32$. Their product is $-1$, so the lines are perpendicular.
:::

```figure caption="The pair $6x^2-5xy-6y^2=0$ is the two perpendicular lines $2x-3y=0$ and $3x+2y=0$ through the origin."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2, 3.4))
x = np.linspace(-3, 3, 50)
ax.plot(x, 2*x/3, color=ACCENT, lw=1.6)
ax.plot(x, -3*x/2, color=SERIES[1], lw=1.6)
ax.text(2.2, 1.6, '2x − 3y = 0', color=ACCENT, fontsize=8.5)
ax.text(-3.0, 3.9, '3x + 2y = 0', color=SERIES[1], fontsize=8.5)
ax.plot([0], [0], 'o', color=INK, ms=4)
ax.plot([0.35, 0.35, 0], [0, 0.45, 0.45], color=INK, lw=0.6)
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-3.2, 3.4); ax.set_ylim(-3.2, 4.2); ax.set_aspect('equal')
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example A condition for coincident lines
**Problem.** For what values of $k$ does $x^2+kxy+4y^2=0$ represent two coincident lines?

**Solution.** Compare with $ax^2+2hxy+by^2=0$: $a=1$, $2h=k$ so $h=\dfrac k2$, and $b=4$. Coincident lines need $h^2=ab$:

$$ \frac{k^2}{4}=1\times4 \Rightarrow k^2=16 \Rightarrow k=\pm4 $$

For $k=4$: $x^2+4xy+4y^2=(x+2y)^2=0$, the single line $x+2y=0$ taken twice.
:::

::: caution The "2" in $2h$
In $ax^2+2hxy+by^2$ the middle coefficient is $2h$, not $h$. In $3x^2+8xy-5y^2$ we have $2h=8$, so $h=4$. Using $h=8$ is the most common slip in this chapter and ruins every later formula.
:::

## 6.3 Angle between the pair of lines

::: derivation Angle between the lines of $ax^2+2hxy+by^2=0$
**Setting up.** The lines are $y=m_1x$ and $y=m_2x$, with $m_1+m_2=-\dfrac{2h}{b}$ and $m_1m_2=\dfrac ab$.

**Step 1 — difference of slopes.**

$$ (m_1-m_2)^2=(m_1+m_2)^2-4m_1m_2=\frac{4h^2}{b^2}-\frac{4a}{b}=\frac{4(h^2-ab)}{b^2} $$

so $m_1-m_2=\pm\dfrac{2\sqrt{h^2-ab}}{b}$.

**Step 2 — the denominator.** $1+m_1m_2=1+\dfrac ab=\dfrac{a+b}{b}$.

**Step 3 — substitute into the angle formula.**

$$ \tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|=\left|\frac{2\sqrt{h^2-ab}/b}{(a+b)/b}\right| $$

**Result.**

$$ \tan\theta=\left|\frac{2\sqrt{h^2-ab}}{a+b}\right| $$

**What it means.** The angle depends only on $a$, $h$ and $b$, so the lines never have to be separated. If $a+b=0$ the denominator is zero and $\theta=90^\circ$. If $h^2=ab$ the numerator is zero and $\theta=0^\circ$.
:::

::: key Pair of lines through the origin
For $ax^2+2hxy+by^2=0$:

$$ \tan\theta=\left|\frac{2\sqrt{h^2-ab}}{a+b}\right| $$

| Condition | Meaning |
|---|---|
| $h^2>ab$ | two distinct real lines |
| $a+b=0$ | the lines are **perpendicular** |
| $h^2=ab$ | the lines are **coincident** (parallel and joined) |
| $h^2<ab$ | no real lines |
:::

::: example Angle between a pair (clean answer)
**Problem.** Find the angle between the lines given by $2x^2+7xy+3y^2=0$.

**Solution.** $a=2$, $2h=7$ so $h=\dfrac72$, $b=3$.

$$ h^2-ab=\frac{49}{4}-6=\frac{25}{4}, \qquad \sqrt{h^2-ab}=\frac52 $$

$$ \tan\theta=\left|\frac{2\times\frac52}{2+3}\right|=\frac55=1 \quad\Rightarrow\quad \theta=45^\circ $$

Check by factorising: $2x^2+7xy+3y^2=(2x+y)(x+3y)$, slopes $-2$ and $-\dfrac13$, and $\dfrac{-2+\frac13}{1+\frac23}=\dfrac{-5/3}{5/3}=-1$, so again $45^\circ$. ✓
:::

::: example Angle between a pair with surds
**Problem.** Find the angle between the lines $\sqrt{3}\,x^2-4xy+\sqrt{3}\,y^2=0$.

**Solution.** $a=\sqrt{3}$, $2h=-4$ so $h=-2$, $b=\sqrt{3}$.

$$ h^2-ab=4-3=1 \quad\Rightarrow\quad \tan\theta=\left|\frac{2\times1}{\sqrt{3}+\sqrt{3}}\right|=\frac{2}{2\sqrt{3}}=\frac{1}{\sqrt{3}} $$

So $\theta=30^\circ$.
:::

::: example Condition of perpendicular lines
**Problem.** Find $k$ if the lines given by $3x^2+4xy+ky^2=0$ are perpendicular to each other.

**Solution.** Perpendicular lines need $a+b=0$: $3+k=0$, so $k=-3$.

Check: $3x^2+4xy-3y^2=0$ has $h=2$, $h^2-ab=4+9=13>0$, so the lines are real and distinct. ✓
:::

::: example Lines perpendicular to a given pair
**Problem.** Find the equation of the pair of lines through the origin perpendicular to the pair $x^2-5xy+6y^2=0$.

**Solution.** Factorise: $x^2-5xy+6y^2=(x-2y)(x-3y)$, so the given lines are $x-2y=0$ (slope $\frac12$) and $x-3y=0$ (slope $\frac13$).

Perpendicular slopes are $-2$ and $-3$. The lines through the origin are $y=-2x$ and $y=-3x$, i.e. $2x+y=0$ and $3x+y=0$.

$$ (2x+y)(3x+y)=6x^2+5xy+y^2=0 $$

**Shortcut.** To get the perpendicular pair, interchange the coefficients of $x^2$ and $y^2$ and change the sign of the $xy$ term: $x^2-5xy+6y^2\to 6x^2+5xy+y^2$.
:::

::: tip The examiner is looking for
Writing $a$, $2h$ and $b$ explicitly (marks); computing $h^2-ab$ separately; the formula with the modulus and the factor $2$ in the numerator; and a final angle in degrees. For "show that the lines are perpendicular" it is enough to show $a+b=0$.
:::

## 6.4 Exercises of the SEE type

### Method for any question

1. Pick the right case: two separate lines (use slopes) or one homogeneous equation (use $a$, $h$, $b$).
2. For two lines, find $m_1$ and $m_2$; for one equation, read $a$, $2h$ and $b$ carefully.
3. Use the formula with the modulus; simplify the numerator and denominator separately.
4. For conditions on $k$: parallel $\Rightarrow m_1=m_2$; perpendicular $\Rightarrow m_1m_2=-1$ or $a+b=0$; coincident $\Rightarrow h^2=ab$.
5. State the final angle in degrees or the final equation in simplest form.

### Two more SEE-type questions

::: example A pair of lines from their inclinations
**Problem.** Two lines through the origin make angles of $60^\circ$ and $120^\circ$ with the positive $x$-axis. Find their combined equation and check the angle between them.

**Solution.** Slopes: $\tan60^\circ=\sqrt{3}$ and $\tan120^\circ=-\sqrt{3}$. Lines: $y-\sqrt{3}\,x=0$ and $y+\sqrt{3}\,x=0$.

$$ (y-\sqrt{3}\,x)(y+\sqrt{3}\,x)=y^2-3x^2 \quad\Rightarrow\quad 3x^2-y^2=0 $$

Here $a=3$, $h=0$, $b=-1$, so $\tan\theta=\left|\dfrac{2\sqrt{0+3}}{3-1}\right|=\sqrt{3}$ and $\theta=60^\circ$. ✓
:::

::: example Finding $k$ from a given angle
**Problem.** Find $k$ if the angle between the lines $x^2+kxy+y^2=0$ is $45^\circ$.

**Solution.** $a=1$, $h=\dfrac k2$, $b=1$, and $\tan45^\circ=1$:

$$ 1=\left|\frac{2\sqrt{\frac{k^2}{4}-1}}{2}\right| \Rightarrow \frac{k^2}{4}-1=1 \Rightarrow k^2=8 \Rightarrow k=\pm2\sqrt{2} $$
:::

## Chapter summary

- Slope $m=\tan\theta$; for $ax+by+c=0$, $m=-\dfrac ab$.
- Angle between lines of slopes $m_1,m_2$: $\tan\theta=\left|\dfrac{m_1-m_2}{1+m_1m_2}\right|$.
- For $a_1x+b_1y+c_1=0$ and $a_2x+b_2y+c_2=0$: $\tan\theta=\left|\dfrac{a_1b_2-a_2b_1}{a_1a_2+b_1b_2}\right|$.
- Parallel: $m_1=m_2$. Perpendicular: $m_1m_2=-1$, i.e. $a_1a_2+b_1b_2=0$.
- The combined equation of two lines through the origin is the product of their equations; it is $ax^2+2hxy+by^2=0$.
- Lines $y=m_1x$, $y=m_2x$ from it: $m_1+m_2=-\dfrac{2h}{b}$, $m_1m_2=\dfrac ab$.
- Angle between the pair: $\tan\theta=\left|\dfrac{2\sqrt{h^2-ab}}{a+b}\right|$.
- Perpendicular if $a+b=0$; coincident if $h^2=ab$; real and distinct if $h^2>ab$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The slope of the line $3x-4y+7=0$ is <span class="marks">[1]</span>
   (a) $-\frac34$ (b) $\frac34$ (c) $\frac43$ (d) $-\frac43$
2. Two lines of slopes $m_1$ and $m_2$ are perpendicular if <span class="marks">[1]</span>
   (a) $m_1=m_2$ (b) $m_1+m_2=0$ (c) $m_1m_2=-1$ (d) $m_1m_2=1$
3. The equation $ax^2+2hxy+by^2=0$ represents two perpendicular lines if <span class="marks">[1]</span>
   (a) $h=0$ (b) $a+b=0$ (c) $h^2=ab$ (d) $a=b$
4. The combined equation of $x-y=0$ and $x+y=0$ is <span class="marks">[1]</span>
   (a) $x^2+y^2=0$ (b) $x^2-y^2=0$ (c) $xy=0$ (d) $x^2-2xy+y^2=0$
5. The lines given by $4x^2+12xy+9y^2=0$ are <span class="marks">[1]</span>
   (a) perpendicular (b) coincident (c) distinct and not perpendicular (d) imaginary

::: note Answers to Group A
**1.** (b) — $m=-\frac ab=-\frac{3}{-4}=\frac34$.
**2.** (c) — the denominator $1+m_1m_2$ must be zero.
**3.** (b) — $a+b=0$ makes the denominator of the angle formula zero.
**4.** (b) — $(x-y)(x+y)=x^2-y^2$.
**5.** (b) — $4x^2+12xy+9y^2=(2x+3y)^2$; also $h=6$, $h^2=36=ab$.
:::

**Group B — Short answer (2 marks each)**

1. Find the angle between the lines of slopes $\sqrt{3}$ and $0$. <span class="marks">[2]</span>
2. Find $k$ so that the lines $2x+3y=7$ and $kx-6y=1$ are parallel. <span class="marks">[2]</span>
3. Find the combined equation of the lines $x-2y=0$ and $2x+y=0$. <span class="marks">[2]</span>
4. Find the separate lines given by $x^2-y^2=0$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\tan\theta=\left|\dfrac{\sqrt{3}-0}{1+0}\right|=\sqrt{3}$, so $\theta=60^\circ$.
**2.** Parallel: $\dfrac{2}{k}=\dfrac{3}{-6}$, so $3k=-12$ and $k=-4$.
**3.** $(x-2y)(2x+y)=2x^2+xy-4xy-2y^2=2x^2-3xy-2y^2=0$.
**4.** $(x-y)(x+y)=0$: the lines are $x-y=0$ and $x+y=0$.
:::

**Group C — Short answer (3 marks each)**

1. Find the acute angle between $x+2y-5=0$ and $3x-y+4=0$. <span class="marks">[3]</span>
2. Find the angle between the lines given by $x^2-4xy+y^2=0$. <span class="marks">[3]</span>
3. Find the value of $k$ if the lines $kx^2+5xy-3y^2=0$ are perpendicular. <span class="marks">[3]</span>
4. Find the equation of the line through $(1,-2)$ perpendicular to the line $2x+3y=6$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $m_1=-\frac12$, $m_2=3$. $\tan\theta=\left|\dfrac{-\frac12-3}{1-\frac32}\right|=\left|\dfrac{-\frac72}{-\frac12}\right|=7$, so $\theta=\tan^{-1}7\approx81.87^\circ$.
**2.** $a=1$, $h=-2$, $b=1$. $\tan\theta=\left|\dfrac{2\sqrt{4-1}}{2}\right|=\sqrt{3}$, so $\theta=60^\circ$.
**3.** Perpendicular needs $a+b=0$: $k-3=0$, so $k=3$.
**4.** Slope of $2x+3y=6$ is $-\frac23$; perpendicular slope $\frac32$. $y+2=\frac32(x-1)\Rightarrow 2y+4=3x-3\Rightarrow 3x-2y-7=0$. Check $(1,-2)$: $3+4-7=0$. ✓
:::

**Group D — Long answer (4 marks each)**

1. Find the equations of the two lines through $(2,1)$ that make an angle of $45^\circ$ with the line $3x-y+2=0$. <span class="marks">[4]</span>
2. Show that the lines $3x^2+8xy-3y^2=0$ are perpendicular, and find the separate equations of the lines. <span class="marks">[4]</span>
3. Find the pair of lines through the origin perpendicular to $2x^2+5xy+3y^2=0$. <span class="marks">[4]</span>
4. The vertices of a triangle are $P(0,0)$, $Q(4,0)$ and $R(4,3)$. Find the angle at $P$ and verify that the angles of the triangle add up to $180^\circ$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Slope of the given line $=3$. $\left|\dfrac{m-3}{1+3m}\right|=1$. Case 1: $m-3=1+3m\Rightarrow m=-2$; line $y-1=-2(x-2)$, i.e. $2x+y-5=0$. Case 2: $m-3=-1-3m\Rightarrow4m=2\Rightarrow m=\frac12$; line $y-1=\frac12(x-2)$, i.e. $x-2y=0$. Lines: $2x+y-5=0$ and $x-2y=0$.
**2.** $a=3$, $b=-3$, so $a+b=0$: the lines are perpendicular. Factorise: $3x^2+8xy-3y^2=(3x-y)(x+3y)$ (check: $3x^2+9xy-xy-3y^2$ ✓). Lines: $3x-y=0$ and $x+3y=0$; slopes $3$ and $-\frac13$, product $-1$. ✓
**3.** $2x^2+5xy+3y^2=(2x+3y)(x+y)$: slopes $-\frac23$ and $-1$. Perpendicular slopes: $\frac32$ and $1$. Lines: $3x-2y=0$ and $x-y=0$. Combined: $(3x-2y)(x-y)=3x^2-5xy+2y^2=0$. (Shortcut check: swap $a,b$ and flip the sign of $xy$.)
**4.** Slope of $PQ=0$, slope of $PR=\frac34$. $\tan P=\frac34$, $P\approx36.87^\circ$. $Q=90^\circ$ (since $PQ$ is horizontal and $QR$ vertical). $R=180^\circ-90^\circ-36.87^\circ=53.13^\circ$; check with slopes of $RP$ ($\frac34$) and $RQ$ (vertical, inclination $90^\circ$): inclination of $RP$ is $36.87^\circ$, so $R=90^\circ-36.87^\circ=53.13^\circ$. ✓ Sum: $36.87+90+53.13=180^\circ$.
:::


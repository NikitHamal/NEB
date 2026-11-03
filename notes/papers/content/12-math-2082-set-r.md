---
file: NEBians-Past-Paper-Grade-12-Mathematics-2082-Set-R.pdf
subject: Mathematics
grade: 12
year_bs: 2082
year_ad: 2025
stream: Set 'R'
code: 0081 (New course) Set 'R'
time: 3 hrs
marks: 75
students: For the students whose first two digits of registration number start from 80 (partial) and 81 (regular)
category: Board Exam
---
## Group 'A'
<small>Multiple choice questions · rewrite the correct option of each question in your answer sheet · [11×1=11]</small>

@mcq 1
Which one is the relation between permutation and combination of $n$ things taken $r$ things at a time?
@opts-col $C(n,r) = r!\times P(n,r)$ | $C(n,r)\times r! = P(n,r)$ | $C(n,r)\times r = P(n,r)$ | $C(n,r) = P(n,r)\times r$

@mcq 2
If the system of equations $p_1x + q_1y = r_1$ and $p_2x + q_2y = r_2$, what is the value of $y$?

```figure caption="Options for question 2: each option is a ratio of two second-order determinants."
fig, ax = plt.subplots(figsize=(4.8,2.9))
def det(cx, cy, e):
    for r in range(2):
        for c in range(2):
            ax.text(cx-0.27+c*0.54, cy+0.18-r*0.36, '$%s$' % e[r][c], ha='center', va='center', fontsize=9)
    for dx in (-0.5, 0.5): ax.plot([cx+dx]*2, [cy-0.4, cy+0.4], color=INK, lw=1)
def frac(ox, oy, label, top, bot):
    ax.text(ox, oy, label, fontsize=9, va='center', ha='right', fontweight='bold', color=ACCENT)
    det(ox+0.8, oy+0.55, top); ax.plot([ox+0.15, ox+1.45], [oy, oy], color=INK, lw=1.3); det(ox+0.8, oy-0.55, bot)
frac(0.4, 2.0, 'A', [['p_1','r_1'],['p_2','r_2']], [['p_1','q_1'],['p_2','q_2']])
frac(3.4, 2.0, 'B', [['p_1','q_1'],['p_2','q_2']], [['r_1','q_1'],['r_2','q_2']])
frac(0.4, 0.0, 'C', [['r_1','q_1'],['r_2','q_2']], [['p_1','q_1'],['p_2','q_2']])
frac(3.4, 0.0, 'D', [['r_1','p_1'],['r_2','p_2']], [['p_1','q_1'],['p_2','q_2']])
ax.set_xlim(-0.2, 5.4); ax.set_ylim(-1.0, 3.0); ax.set_aspect('equal'); ax.axis('off')
```

@mcq 3
Which one of the following is the value of $\sec\dfrac{B}{2}$?
@opts $\sqrt{\dfrac{ca}{s-b}}$ | $\sqrt{\dfrac{bc}{s(s-a)}}$ | $\sqrt{\dfrac{bc}{s(s-c)}}$ | $\sqrt{\dfrac{ca}{s(s-b)}}$

@mcq 4
In which condition will the line $y = mx + c$ be tangent to the circle $x^2 + y^2 = a^2$?
@opts $a = c\sqrt{1+m^2}$ | $a = \pm c\sqrt{1+m^2}$ | $c = \pm a\sqrt{1+m^2}$ | $c = a\sqrt{1+m^2}$

@mcq 5
What is $\vec a\times\vec b$ if $\vec a = (0,0,1)$ and $\vec b = (0,1,0)$?
@opts $(-1,0,0)$ | $(1,0,0)$ | $(0,1,0)$ | $(0,0,-1)$

@mcq 6
If $P(A) = \dfrac13$, $P(B) = \dfrac23$ and $P(A\cap B) = \dfrac15$, which one of the following is $P(B/A)$?
@opts $\dfrac{3}{5}$ | $\dfrac25$ | $\dfrac{2}{15}$ | $\dfrac{1}{15}$

@mcq 7
Which one of the following is the slope of the normal to the curve $y = 3x^2 - x$ at $(-1, 1)$?
@opts $-7$ | $-5$ | $\dfrac{1}{7}$ | $\dfrac15$

@mcq 8
What is the integral of $\displaystyle\int\dfrac{dx}{9x^2+1}$?
@opts-col $\dfrac{1}{3}\tan^{-1}(3x) + C$ | $\dfrac{1}{27}\tan^{-1}(3x) + C$ | $\dfrac{1}{27}\tan^{-1}\left(\dfrac{x}{3}\right) + C$ | $\dfrac{1}{27}\tan^{-1}\left(\dfrac{3}{x}\right) + C$

@mcq 9
Which one of the following is the homogeneous differential equation?
@opts-col $\dfrac{dy}{dx} = \dfrac{x^2+y^2}{x+y}$ | $\dfrac{dy}{dx} = \dfrac{x^2+y^2}{x-y}$ | $\dfrac{dy}{dx} = \dfrac{x^2+y^2}{x^2-y^2}$ | $\dfrac{dy}{dx} = \dfrac{x+y}{x^2+y^2}$

@mcq 10
Which is the integrating factor of the linear differential equation $\cos^2x\,\dfrac{dy}{dx} = 1 - y$?
@opts $\tan x$ | $e^{\tan x}$ | $e^{\sec^2x}$ | $\sec^2x$

@mcq 11
Two simultaneous equations are given as $3x + 4y = 13$ and $x - 2y = 1$. What is the equation after eliminating $x$?
@opts $10y = 10$ | $10y = 16$ | $y = 10$ | $2y = 10$
@or
What is the maximum height attained by a particle in projectile motion if the initial velocity and angle of inclination are 40 m/s and $30^{\circ}$? ($g = 10\ \text{m s}^{-2}$)
@opts 20 m | 40 m | 80 m | 160 m

## Group 'B'
<small>Short answer questions · [8×5=40]</small>

@q 12
(a) Write the expansion of $\log_e(1-x)$; $|x|<1$. [[1]]
(b) Write the total number of permutations of a set having $n$ elements. [[1]]
(c) State De Moivre's theorem. [[1]]
(d) Write the sum of cubes of the first $n$ natural numbers. [[1]]
(e) Write the augmented matrix of the system of equations $3x + 2y - 1 = 0$ and $4x + y = 3$. [[1]]

@q 13
(a) A committee is to be chosen from $a$ boys and 6 girls and is to consist of 2 boys and 3 girls. If 120 committees are formed, what is the number of boys represented by $a$? [[2]]
(b) The square roots of a complex number are $(\sqrt{3} + i)$ and $(-\sqrt{3} - i)$. Write the complex number in polar form. [[3]]

@q 14
(a) In any triangle PQR, if $p\sin^2\dfrac{R}{2} + r\sin^2\dfrac{P}{2} = \dfrac{q}{2}$, prove that the sides are in A.P. [[3]]
(b) If $\vec a = 4\hat i - 3\hat j + 2\hat k$ and $\vec b = 3\hat i - 2\hat j + 4\hat k$ are two vectors, find the projection of $\vec b$ on $\vec a$. [[2]]

@q 15
(a) Find the eccentricity of the conic $3x^2 - 4y^2 - 6x = 0$. [[2]]
(b) Find the eccentricity of the ellipse whose major axis is four times its minor axis and which passes through the point $(4, 2)$. [[3]]

@q 16
Consider the following data for supply ($X$) and the price ($Y$) of a commodity for the last six years.

| Year in B.S. | 2075 | 2076 | 2077 | 2078 | 2079 | 2080 |
|---|---|---|---|---|---|---|
| X | 45 | 50 | 56 | 62 | 65 | 70 |
| Y | 65 | 70 | 75 | 80 | 90 | 100 |

(a) Find the correlation coefficient between $X$ and $Y$. [[2]]
(b) Calculate the supply when the price of the commodity is Rs. 150. [[3]]

@q 17
(a) Write the derivative of $\text{cosech}^{-1}(x)$. [[1]]
(b) Define L'Hospital's rule. [[1]]
(c) Write the condition where the curve $y = f(x)$ has a tangent parallel to the y-axis. [[1]]
(d) Write the integral of $\displaystyle\int\dfrac{1}{x^2-a^2}\,dx$. [[1]]
(e) Write the standard form of a first order linear differential equation. [[1]]

@q 18
(a) Find the derivative of $\coth^{-1}(\sin2x)$. [[2]]
(b) Integrate: $\displaystyle\int\dfrac{dx}{x^3 - x^2 - 2x}$. [[3]]

@q 19
Using the simplex method, maximize $P(x,y) = 10x + 3y$ subject to the constraints $6x + 7y \le 42$, $x + 3y \le 42$, $x + 3y \le 9$, $x \ge 0$, $y \ge 0$. [[5]]
@or
Two forces $A$ and $B$ acting parallel to the length and base of an inclined plane respectively would each of them singly support a weight $R$ on the plane. Prove that $\dfrac{1}{A^2} = \dfrac{1}{B^2} + \dfrac{1}{R^2}$. [[5]]

## Group 'C'
<small>Long answer questions · [3×8=24]</small>

@q 20
(a) If the middle term in the expansion of $\left(\dfrac{a}{2} + 2\right)^8$ is 1120, find the value of $a$. [[2]]
(b) Using mathematical induction, prove that $1 + 7 + 13 + 19 + \dots + (6n-5) = n(3n-2)$. [[3]]
(c) Solve the following linear equations by using the matrix method: $7x - 2y = 18$, $3x + 7z = 33$, $x + y + z = 12$. [[3]]

@q 21
(a) The scalar product of two vectors and the cross product of two vectors are interrelated. Explain. [[3]]
(b) If the cosines of two angles of a triangle are proportional to the opposite sides, show that it is an isosceles triangle. [[2]]
(c) Establish the condition that the line $ax + by + c = 0$ may be normal to the parabola $x^2 = 4ay$. [[3]]

@q 22
(a) Find the rate of change of volume of a sphere with respect to its surface area when the radius is 7 cm. [[2]]
(b) Integrate: $\displaystyle\int\dfrac{dx}{5 - 3\cos x}$. [[3]]
(c) Solve: $(1+x^2)\,dy - (1+y^2)\,dx = 0$. [[3]]

<!-- SOLUTIONS -->
### Group A — answer key

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ans | B | A | D | C | A | A | C | A | C | B | A |

**1. B.** $P(n,r) = \dfrac{n!}{(n-r)!}$ and $C(n,r) = \dfrac{n!}{r!(n-r)!}$, so $C(n,r)\times r! = P(n,r)$.

**2. A.** By Cramer's rule $y = \dfrac{D_y}{D}$, with $D_y = p_1r_2 - p_2r_1$ (the determinant with rows $(p_1, r_1)$, $(p_2, r_2)$) and $D = p_1q_2 - p_2q_1$ (rows $(p_1, q_1)$, $(p_2, q_2)$): the numerator is the determinant of the coefficients with the $y$-column replaced by the constants.

**3. D.** $\cos\dfrac{B}{2} = \sqrt{\dfrac{s(s-b)}{ca}}$, so $\sec\dfrac{B}{2} = \sqrt{\dfrac{ca}{s(s-b)}}$.

**4. C.** The distance from the centre to the line $mx - y + c = 0$ must equal the radius: $\dfrac{|c|}{\sqrt{1+m^2}} = a$, so $c = \pm a\sqrt{1+m^2}$.

**5. A.** $\hat k\times\hat j = -\hat i$, so $\vec a\times\vec b = (-1,0,0)$.

**6. A.** $P(B/A) = \dfrac{P(A\cap B)}{P(A)} = \dfrac{1/5}{1/3} = \dfrac{3}{5}$.

**7. C.** $\dfrac{dy}{dx} = 6x - 1 = -7$ at $x=-1$; slope of the normal $= -\dfrac{1}{-7} = \dfrac{1}{7}$.

**8. A.** $\displaystyle\int\dfrac{dx}{(3x)^2+1} = \dfrac{1}{3}\tan^{-1}(3x) + C$.

**9. C.** A first-order equation $\dfrac{dy}{dx} = f(x,y)$ is homogeneous when $f$ is homogeneous of degree 0. In (C) numerator and denominator are both of degree 2, so $f(\lambda x,\lambda y) = f(x,y)$. The others mix degrees.

**10. B.** Dividing by $\cos^2x$: $\dfrac{dy}{dx} + y\sec^2x = \sec^2x$. $\text{I.F.} = e^{\int\sec^2x\,dx} = e^{\tan x}$.

**11. A.** Multiply $x - 2y = 1$ by 3: $3x - 6y = 3$. Subtract from $3x + 4y = 13$: $10y = 10$.
**Or: A.** $H = \dfrac{u^2\sin^2\theta}{2g} = \dfrac{1600\times\frac14}{20} = 20$ m.

### Group B

@s 12
**(a)** $\log_e(1-x) = -\left(x + \dfrac{x^2}{2} + \dfrac{x^3}{3} + \dfrac{x^4}{4} + \dots\right)$, for $|x|<1$.
**(b)** $n!$ (all $n$ elements taken at a time).
**(c)** For any real $\theta$ and integer $n$: $(\cos\theta + i\sin\theta)^n = \cos n\theta + i\sin n\theta$.
**(d)** $1^3 + 2^3 + \dots + n^3 = \left[\dfrac{n(n+1)}{2}\right]^2$.
**(e)** The system is $3x + 2y = 1$, $4x + y = 3$. Augmented matrix, rows $[\,3\ \ 2\ |\ 1\,]$ and $[\,4\ \ 1\ |\ 3\,]$:

| x | y | constant |
|---|---|---|
| 3 | 2 | 1 |
| 4 | 1 | 3 |


@s 13
**(a)** $C(a,2)\times C(6,3) = 120$, with $C(6,3) = 20$, so $C(a,2) = 6$, i.e. $\dfrac{a(a-1)}{2} = 6$, $a^2 - a - 12 = 0$, $(a-4)(a+3) = 0$. Since $a>0$, $a = 4$.

**(b)** The complex number is the square of a square root: $z = (\sqrt{3} + i)^2 = 3 + 2\sqrt{3}\,i + i^2 = 2 + 2\sqrt{3}\,i$. Then $r = \sqrt{4+12} = 4$, $\tan\theta = \dfrac{2\sqrt{3}}{2} = \sqrt{3}$, and $z$ lies in the first quadrant, so $\theta = \dfrac{\pi}{3}$.
$$z = 4\left(\cos\frac{\pi}{3} + i\sin\frac{\pi}{3}\right).$$

@s 14
**(a)** Use $\sin^2\dfrac{\theta}{2} = \dfrac{1-\cos\theta}{2}$:
$$\frac{p}{2}(1-\cos R) + \frac{r}{2}(1-\cos P) = \frac{q}{2}\ \Rightarrow\ p + r - (p\cos R + r\cos P) = q.$$
The projection formula for $\triangle$PQR gives $q = p\cos R + r\cos P$. Hence $p + r - q = q$, i.e. $p + r = 2q$, so $p, q, r$ are in A.P.

**(b)** $\vec a\cdot\vec b = 4(3) + (-3)(-2) + 2(4) = 12 + 6 + 8 = 26$, $|\vec a| = \sqrt{16+9+4} = \sqrt{29}$. Projection of $\vec b$ on $\vec a$ $= \dfrac{\vec a\cdot\vec b}{|\vec a|} = \dfrac{26}{\sqrt{29}} \approx 4.83$.

@s 15
**(a)** $3x^2 - 6x - 4y^2 = 0\Rightarrow 3(x-1)^2 - 4y^2 = 3\Rightarrow \dfrac{(x-1)^2}{1} - \dfrac{y^2}{3/4} = 1$. This is a hyperbola with $a^2 = 1$, $b^2 = \dfrac{3}{4}$:
$$e = \sqrt{1 + \frac{b^2}{a^2}} = \sqrt{1 + \frac{3}{4}} = \frac{\sqrt{7}}{2}.$$

**(b)** Let the ellipse be $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1$ with $2a = 4(2b)$, so $a = 4b$ and $a^2 = 16b^2$. Through $(4,2)$: $\dfrac{16}{16b^2} + \dfrac{4}{b^2} = 1\Rightarrow\dfrac{5}{b^2} = 1\Rightarrow b^2 = 5$, $a^2 = 80$.
$$e = \sqrt{1 - \frac{b^2}{a^2}} = \sqrt{1 - \frac{1}{16}} = \frac{\sqrt{15}}{4}.$$
(If the major axis were along the y-axis the same value of $e$ results.)

@s 16
$n = 6$, $\bar X = \dfrac{348}{6} = 58$, $\bar Y = \dfrac{480}{6} = 80$. With $x = X - 58$ and $y = Y - 80$:

| X | Y | x | y | x² | y² | xy |
|---|---|---|---|---|---|---|
| 45 | 65 | −13 | −15 | 169 | 225 | 195 |
| 50 | 70 | −8 | −10 | 64 | 100 | 80 |
| 56 | 75 | −2 | −5 | 4 | 25 | 10 |
| 62 | 80 | 4 | 0 | 16 | 0 | 0 |
| 65 | 90 | 7 | 10 | 49 | 100 | 70 |
| 70 | 100 | 12 | 20 | 144 | 400 | 240 |
| Σ | | 0 | 0 | 446 | 850 | 595 |

**(a)** $r = \dfrac{\sum xy}{\sqrt{\sum x^2\sum y^2}} = \dfrac{595}{\sqrt{446\times850}} = \dfrac{595}{615.7} \approx 0.966$.
**(b)** To estimate supply from price, use the regression line of $X$ on $Y$: $b_{xy} = \dfrac{\sum xy}{\sum y^2} = \dfrac{595}{850} = 0.7$.
$$X - 58 = 0.7\,(Y - 80).$$
For $Y = 150$: $X = 58 + 0.7\times70 = 107$ units.

@s 17
**(a)** $\dfrac{d}{dx}\text{cosech}^{-1}x = -\dfrac{1}{|x|\sqrt{1+x^2}}$ (for $x>0$: $-\dfrac{1}{x\sqrt{1+x^2}}$).
**(b)** If $f(x)$ and $g(x)$ both tend to 0 (or both to $\infty$) as $x\to a$, then $\displaystyle\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)}$, provided the second limit exists.
**(c)** $\dfrac{dy}{dx}\to\infty$, equivalently $\dfrac{dx}{dy} = 0$.
**(d)** $\displaystyle\int\frac{dx}{x^2-a^2} = \frac{1}{2a}\ln\left|\frac{x-a}{x+a}\right| + C$.
**(e)** $\dfrac{dy}{dx} + Py = Q$, where $P$ and $Q$ are functions of $x$ only (or constants).

@s 18
**(a)** $y = \coth^{-1}(\sin2x)$: using $\dfrac{d}{dx}\coth^{-1}u = \dfrac{1}{1-u^2}\dfrac{du}{dx}$,
$$\frac{dy}{dx} = \frac{2\cos2x}{1-\sin^22x} = \frac{2\cos2x}{\cos^22x} = 2\sec2x.$$

**(b)** $x^3 - x^2 - 2x = x(x-2)(x+1)$. Let $\dfrac{1}{x(x-2)(x+1)} = \dfrac{A}{x} + \dfrac{B}{x-2} + \dfrac{C}{x+1}$. Then $A = \dfrac{1}{(-2)(1)} = -\dfrac{1}{2}$, $B = \dfrac{1}{2\cdot3} = \dfrac16$, $C = \dfrac{1}{(-1)(-3)} = \dfrac13$.
$$\int\frac{dx}{x^3-x^2-2x} = -\frac12\ln|x| + \frac16\ln|x-2| + \frac13\ln|x+1| + C.$$

@s 19
The constraint $x + 3y \le 42$ is implied by $x + 3y \le 9$. Add slack variables $s_1, s_2, s_3$: $6x + 7y + s_1 = 42$, $x + 3y + s_2 = 42$, $x + 3y + s_3 = 9$, $P - 10x - 3y = 0$.

| Basis | x | y | s₁ | s₂ | s₃ | P | RHS |
|---|---|---|---|---|---|---|---|
| s₁ | 6 | 7 | 1 | 0 | 0 | 0 | 42 |
| s₂ | 1 | 3 | 0 | 1 | 0 | 0 | 42 |
| s₃ | 1 | 3 | 0 | 0 | 1 | 0 | 9 |
| P | −10 | −3 | 0 | 0 | 0 | 1 | 0 |

The most negative entry is −10 (column $x$). Ratios: $42/6 = 7$, $42/1 = 42$, $9/1 = 9$; the pivot row is $s_1$. After $R_1\to R_1/6$ and clearing column $x$:

| Basis | x | y | s₁ | s₂ | s₃ | P | RHS |
|---|---|---|---|---|---|---|---|
| x | 1 | 7/6 | 1/6 | 0 | 0 | 0 | 7 |
| s₂ | 0 | 11/6 | −1/6 | 1 | 0 | 0 | 35 |
| s₃ | 0 | 11/6 | −1/6 | 0 | 1 | 0 | 2 |
| P | 0 | 26/3 | 5/3 | 0 | 0 | 1 | 70 |

No negative entry remains in the objective row, so the solution is optimal: $x = 7$, $y = 0$, **maximum $P = 70$**.

**Or.** Let the plane be inclined at angle $\alpha$ and the weight be $R$.
*Force $A$ parallel to the plane:* resolving along the plane, $A = R\sin\alpha$.
*Force $B$ horizontal (parallel to the base):* resolving along the plane, $B\cos\alpha = R\sin\alpha$, so $B = R\tan\alpha$.
Then
$$\frac{1}{B^2} + \frac{1}{R^2} = \frac{\cos^2\alpha}{R^2\sin^2\alpha} + \frac{1}{R^2} = \frac{\cos^2\alpha + \sin^2\alpha}{R^2\sin^2\alpha} = \frac{1}{R^2\sin^2\alpha} = \frac{1}{A^2}.$$

### Group C

@s 20
**(a)** For $n = 8$ there are 9 terms; the middle term is $T_5 = {}^8C_4\left(\dfrac{a}{2}\right)^4(2)^4 = 70\times\dfrac{a^4}{16}\times16 = 70a^4$. Setting $70a^4 = 1120$ gives $a^4 = 16$, so $a = \pm2$.

**(b)** Let $P(n)$: $1 + 7 + 13 + \dots + (6n-5) = n(3n-2)$.
*Basis:* $n = 1$: LHS $= 1$, RHS $= 1(3-2) = 1$. True.
*Step:* assume $P(k)$: $1 + 7 + \dots + (6k-5) = k(3k-2)$. Adding the next term $6(k+1) - 5 = 6k+1$:
$$k(3k-2) + 6k + 1 = 3k^2 + 4k + 1 = (k+1)(3k+1) = (k+1)\big(3(k+1) - 2\big),$$
which is $P(k+1)$. By induction $P(n)$ is true for all natural numbers $n$.

**(c)** In matrix form $AX = B$, where $A$ has rows $(7, -2, 0)$, $(3, 0, 7)$, $(1, 1, 1)$, $X = (x, y, z)^T$ and $B = (18, 33, 12)^T$.
$|A| = 7(0-7) + 2(3-7) + 0 = -49 - 8 = -57 \ne 0$, so $X = A^{-1}B = \dfrac{\text{adj}A}{|A|}B$. The cofactors give $\text{adj}A$ with rows $(-7, 2, -14)$, $(4, 7, -49)$, $(3, -9, 6)$. Multiplying row by row with $B$:
$$x = \frac{-7(18) + 2(33) - 14(12)}{-57} = \frac{-228}{-57} = 4,\qquad y = \frac{4(18) + 7(33) - 49(12)}{-57} = \frac{-285}{-57} = 5,$$
$$z = \frac{3(18) - 9(33) + 6(12)}{-57} = \frac{-171}{-57} = 3.$$
$x = 4$, $y = 5$, $z = 3$. Check: $7(4) - 2(5) = 18$; $3(4) + 7(3) = 33$; $4 + 5 + 3 = 12$.

@s 21
**(a)** For two vectors with angle $\theta$ between them: scalar product $\vec a\cdot\vec b = |\vec a||\vec b|\cos\theta$ and cross product $|\vec a\times\vec b| = |\vec a||\vec b|\sin\theta$. Both are built from the same magnitudes and the same angle, so they determine each other:
$$(\vec a\cdot\vec b)^2 + |\vec a\times\vec b|^2 = |\vec a|^2|\vec b|^2(\cos^2\theta + \sin^2\theta) = |\vec a|^2|\vec b|^2,\qquad \tan\theta = \frac{|\vec a\times\vec b|}{\vec a\cdot\vec b}.$$
Also, $\vec a\cdot\vec b = 0$ when the vectors are perpendicular (then $|\vec a\times\vec b|$ is maximum), and $\vec a\times\vec b = \vec 0$ when they are parallel (then $|\vec a\cdot\vec b|$ is maximum).

**(b)** Given $\cos A : \cos B = a : b$, i.e. $\dfrac{\cos A}{a} = \dfrac{\cos B}{b}$. By the sine rule $a = 2R\sin A$, $b = 2R\sin B$:
$$\frac{\cos A}{\sin A} = \frac{\cos B}{\sin B}\ \Rightarrow\ \cot A = \cot B\ \Rightarrow\ A = B,$$
since $0<A,B<\pi$. Hence $a = b$ and the triangle is isosceles.

**(c)** (To avoid using $a$ twice, let the line be $Lx + My + N = 0$ and the parabola $x^2 = 4ay$.) A point on the parabola is $(2at, at^2)$. $\dfrac{dy}{dx} = \dfrac{x}{2a} = t$ there, so the normal has slope $-\dfrac{1}{t}$:
$$y - at^2 = -\frac{1}{t}(x - 2at)\ \Rightarrow\ x + ty = 2at + at^3.$$
For this to be the line $x + \dfrac{M}{L}y + \dfrac{N}{L} = 0$ we need $t = \dfrac{M}{L}$ and $\dfrac{N}{L} = -(2at + at^3)$. Substituting $t = M/L$:
$$\frac{N}{L} = -a\frac{M}{L}\left(2 + \frac{M^2}{L^2}\right)\ \Rightarrow\ NL^2 + aM(2L^2 + M^2) = 0$$
which is the required condition. (Check: for $x^2 = 4y$, the normal at $t=1$ is $x + y - 3 = 0$; $L=M=1$, $N=-3$, $a=1$ gives $-3 + 3 = 0$.)

@s 22
**(a)** $V = \tfrac{4}{3}\pi r^3$ and $S = 4\pi r^2$, so $\dfrac{dV}{dS} = \dfrac{dV/dr}{dS/dr} = \dfrac{4\pi r^2}{8\pi r} = \dfrac{r}{2}$. At $r = 7$ cm: $\dfrac{dV}{dS} = 3.5$ cm (i.e. cm³ per cm²).

**(b)** Put $t = \tan\dfrac{x}{2}$, so $\cos x = \dfrac{1-t^2}{1+t^2}$ and $dx = \dfrac{2\,dt}{1+t^2}$. Then $5 - 3\cos x = \dfrac{5(1+t^2) - 3(1-t^2)}{1+t^2} = \dfrac{2 + 8t^2}{1+t^2}$.
$$\int\frac{dx}{5-3\cos x} = \int\frac{2\,dt}{2+8t^2} = \int\frac{dt}{1+4t^2} = \frac12\tan^{-1}(2t) + C = \frac12\tan^{-1}\!\left(2\tan\frac{x}{2}\right) + C.$$

**(c)** Separate the variables: $\dfrac{dy}{1+y^2} = \dfrac{dx}{1+x^2}$. Integrating, $\tan^{-1}y = \tan^{-1}x + C$, i.e. $\dfrac{y - x}{1 + xy} = k$ (a constant), or $y - x = k(1 + xy)$.

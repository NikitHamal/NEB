---
subject: Mathematics I
grade: BCA Semester 1
unit: 1
title: Functions and Graphs
area: BCA 104 · Mathematics I · Unit 1
---

Calculus is the mathematics of change, and its objects are **functions**. Everything in later units (limits, derivatives, integrals, differential equations) is something we *do to a function*, so this unit makes sure you can read, build and combine functions fluently.

::: key What this unit gives you
- Function, domain, range; how to find them from a formula.
- The standard families: polynomial, rational, power, exponential, logarithmic, trigonometric, absolute value, piecewise.
- Even/odd, one-to-one, composition and inverse functions.
- Graph transformations, and the exponent, logarithm and trigonometric facts used throughout the course.
:::

## 1.1 Functions, domain and range

A **function** f from a set A to a set B assigns to every x in A exactly one y = f(x) in B. A is the **domain**; the set of values actually produced is the **range**. A curve is the graph of a function exactly when every vertical line meets it at most once (**vertical line test**).

**Finding the domain.** Start from ℝ and remove values that break the formula:

- division by zero (denominator = 0);
- even roots of negative numbers (radicand < 0);
- logarithm of a non-positive number (argument ≤ 0).

::: example Worked example: domains
**(a)** f(x) = √(x − 2) / (x − 5). Need x − 2 ≥ 0 and x ≠ 5. Domain = [2, 5) ∪ (5, ∞).
**(b)** g(x) = ln(4 − x²). Need 4 − x² > 0, so −2 < x < 2. Domain = (−2, 2).
**(c)** h(x) = 1/√(x² − 3x + 2). Need x² − 3x + 2 > 0, i.e. (x − 1)(x − 2) > 0, so x < 1 or x > 2. Domain = (−∞, 1) ∪ (2, ∞).
:::

**Finding the range.** Complete the square, use known ranges, or solve y = f(x) for x and see which y give a real x.

::: example Worked example: range
f(x) = x² − 4x + 5 = (x − 2)² + 1. Since (x − 2)² ≥ 0, f(x) ≥ 1, and 1 is reached at x = 2. Range = [1, ∞).
:::

## 1.2 Standard families of functions

| Family | Form | Notes |
|---|---|---|
| Linear | f(x) = mx + c | slope m, intercept c |
| Quadratic | ax² + bx + c | parabola, vertex at x = −b/(2a) |
| Polynomial | aₙxⁿ + … + a₀ | domain ℝ; degree n gives at most n roots |
| Rational | P(x)/Q(x) | undefined where Q = 0 (vertical asymptotes or holes) |
| Power / root | xᵃ, ⁿ√x | √x needs x ≥ 0 |
| Exponential | aˣ (a > 0, a ≠ 1) | range (0, ∞); growth if a > 1, decay if 0 < a < 1 |
| Logarithmic | logₐ x | inverse of aˣ; domain (0, ∞) |
| Trigonometric | sin, cos, tan … | periodic |
| Absolute value | \|x\| | = x if x ≥ 0, −x if x < 0 |
| Piecewise | different formulas on different intervals | check the join points |
| Floor / step | ⌊x⌋ | greatest integer ≤ x |

**Exponent laws** (a, b > 0): aᵐ·aⁿ = aᵐ⁺ⁿ; aᵐ / aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ; (ab)ⁿ = aⁿbⁿ; a⁰ = 1; a⁻ⁿ = 1/aⁿ; a^(1/n) = ⁿ√a.

**Logarithm laws.** logₐ(xy) = logₐ x + logₐ y; logₐ(x/y) = logₐ x − logₐ y; logₐ(xᵖ) = p logₐ x; change of base logₐ x = ln x / ln a; logₐ a = 1; logₐ 1 = 0. **e** ≈ 2.71828 is the base of the natural logarithm ln.

**Trigonometric facts used in calculus.** sin²θ + cos²θ = 1; 1 + tan²θ = sec²θ; sin 2θ = 2 sin θ cos θ; cos 2θ = cos²θ − sin²θ = 1 − 2 sin²θ = 2 cos²θ − 1; sin(A ± B) = sin A cos B ± cos A sin B; cos(A ± B) = cos A cos B ∓ sin A sin B. Angles in calculus are always in **radians** (π rad = 180°).

| θ | 0 | π/6 | π/4 | π/3 | π/2 |
|---|---|---|---|---|---|
| sin θ | 0 | 1/2 | √2/2 | √3/2 | 1 |
| cos θ | 1 | √3/2 | √2/2 | 1/2 | 0 |
| tan θ | 0 | 1/√3 | 1 | √3 | undefined |

```svgfig label="1.1" caption="A gallery of the standard functions. Learn the shape of each one: the rest of calculus is read off these graphs. Dashed lines mark asymptotes (a curve that is approached but never reached)."
import math
f = Fig(780, 330)
cells = [("y = x²", lambda x: x*x, (-2.2, 2.2), (-1, 4.5), "even, range [0, ∞)"), ("y = x³", lambda x: x**3, (-2, 2), (-4, 4), "odd, range all reals"),
         ("y = 1/x", lambda x: 1/x, (-3, 3), (-3, 3), "odd, x ≠ 0, two branches"), ("y = √x", lambda x: math.sqrt(x), (-0.5, 4.5), (-1, 3), "x ≥ 0, range [0, ∞)"),
         ("y = eˣ  and  y = ln x", None, (-2, 4), (-2, 4), "inverse pair"), ("y = sin x", lambda x: math.sin(x), (-4.2, 4.2), (-1.6, 1.6), "odd, period 2π")]
for i, (t, fn, xr, yr, note) in enumerate(cells):
    cx, cy = 10 + (i % 3) * 258, 8 + (i // 3) * 162
    f.box(cx, cy, 246, 152, "", fill=SOFT, stroke="#cbd5e1")
    ax = Axes(f, cx + 14, cy + 26, 218, 100, xr, yr)
    ax.axes("", "")
    f.text(cx + 123, cy + 18, t, size=11.5, color=NAVY, bold=True)
    f.text(cx + 123, cy + 146, note, size=9.5, color=TEAL)
    if fn: ax.curve(fn, color=NAVY, sw=2.2)
    if i == 2: ax.vline(0, color=RED); ax.hline(0, color=RED)
    if i == 4:
        ax.curve(math.exp, color=NAVY, sw=2.2); ax.curve(math.log, 0.001, 4, color=TEAL, sw=2.2)
        ax.curve(lambda x: x, color=AMBER, dash=True, sw=1.2)
    if i == 0: ax.pt(0, 0, "", r=3)
```

```photogrid label="1.1" cols="3" ratio="1.2" caption="Functions you can photograph. (a) A parabolic satellite dish: its cross-section is y = ax², which sends every incoming ray to one focus. (b) The Gateway Arch in St Louis follows a hyperbolic cosine (catenary) curve, not a parabola. (c) A sine wave on an oscilloscope: the voltage of an AC supply is V = V₀ sin(ωt)."
@ photo id="bca104/dish" cap="Parabolic dish: y = ax²"
fit 1.2
focus 0.5 0.45
call 0.50 0.93 0.50 0.62 "Parabolic dish"
@ photo id="bca104/arch" cap="Gateway Arch: y = A − B cosh(kx)"
fit 1.2
focus 0.5 0.45
call 0.50 0.93 0.50 0.70 "Catenary curve"
@ photo id="bca103/scope" cap="Oscilloscope trace: y = sin x"
fit 1.2
call 0.30 0.93 0.30 0.70 "Sine wave"
```

## 1.3 Even, odd and one-to-one functions

- **Even**: f(−x) = f(x); graph symmetric about the y-axis (x², cos x, |x|).
- **Odd**: f(−x) = −f(x); symmetric about the origin (x³, sin x, tan x).
- Most functions are neither. Sums of even functions are even; product of two odd functions is even.

::: example Worked example: classify
f(x) = x³ − x: f(−x) = −x³ + x = −f(x), so **odd**. g(x) = x⁴ + cos x: g(−x) = x⁴ + cos x = g(x), so **even**. h(x) = x² + x: h(−x) = x² − x, which is neither h(x) nor −h(x), so **neither**.
:::

A function is **one-to-one** (injective) if different inputs give different outputs; the **horizontal line test** checks it on a graph. Only one-to-one functions have inverses. x² is not one-to-one on ℝ but is on [0, ∞).

## 1.4 Composition and inverse

The **composite** (f∘g)(x) = f(g(x)): apply g first. In general f∘g ≠ g∘f. The domain of f∘g is those x in the domain of g for which g(x) is in the domain of f.

::: example Worked example: composition
f(x) = 2x + 3, g(x) = x². Then (f∘g)(x) = 2x² + 3, and (g∘f)(x) = (2x + 3)². At x = 1: f∘g = 5 but g∘f = 25.
:::

The **inverse** f⁻¹ undoes f: f⁻¹(f(x)) = x. To find it: write y = f(x), solve for x, swap the names. The graph of f⁻¹ is the mirror image of f's graph in the line y = x; domain and range swap.

::: example Worked example: inverse of a rational function
f(x) = (3x − 1)/(x + 2). Put y = (3x − 1)/(x + 2), so y(x + 2) = 3x − 1, giving xy + 2y = 3x − 1, so x(y − 3) = −1 − 2y, hence x = (2y + 1)/(3 − y). Therefore **f⁻¹(x) = (2x + 1)/(3 − x)**. Check: f(0) = −1/2 and f⁻¹(−1/2) = (−1 + 1)/(3.5) = 0. ✓
:::

The logarithm is the inverse of the exponential: y = aˣ ⇔ x = logₐ y.

```svgfig label="1.2" caption="An inverse function is the mirror image of the original in the line y = x. Here f(x) = eˣ (navy) and f⁻¹(x) = ln x (teal). The point (1, e) on f becomes (e, 1) on f⁻¹."
import math
f = Fig(480, 300)
ax = Axes(f, 40, 14, 400, 270, (-2, 4.2), (-2, 4.2))
ax.grid(1, 1).axes()
ax.curve(math.exp, color=NAVY, sw=2.4)
ax.curve(math.log, 0.0001, 4.2, color=TEAL, sw=2.4)
ax.curve(lambda x: x, color=AMBER, dash=True, sw=1.4)
ax.pt(1, math.e, "(1, e)", color=NAVY, dx=8, dy=-6)
ax.pt(math.e, 1, "(e, 1)", color=TEAL, dx=8, dy=14)
ax.tag(2.3, 0.4, "", color=SLATE)
f.text(ax.X(1.35), ax.Y(3.8), "y = eˣ", size=12, color=NAVY, bold=True, anchor="start")
f.text(ax.X(3.0), ax.Y(0.2), "y = ln x", size=12, color=TEAL, bold=True, anchor="start")
f.text(ax.X(3.3), ax.Y(3.55), "y = x", size=11, color=AMBER, bold=True, anchor="start")
```

## 1.5 Graph transformations

From the graph of y = f(x):

| Change | Effect |
|---|---|
| y = f(x) + k | shift up k (down if k < 0) |
| y = f(x − h) | shift right h (left if h < 0) |
| y = −f(x) | reflect in the x-axis |
| y = f(−x) | reflect in the y-axis |
| y = a·f(x), a > 1 | stretch vertically by a |
| y = f(bx), b > 1 | compress horizontally by b |
| y = \|f(x)\| | reflect the part below the x-axis upward |

Example: y = (x − 3)² + 2 is the parabola y = x² moved 3 right and 2 up, with vertex (3, 2).

**Piecewise and absolute-value functions.** |x − 2| = x − 2 for x ≥ 2 and 2 − x for x < 2. Solving |x − 2| < 3 means −3 < x − 2 < 3, so −1 < x < 5. Solving |x − 2| ≥ 3 gives x ≤ −1 or x ≥ 5.

```svgfig label="1.3" caption="Transformations of the parabola y = x². (a) Shifting: y = (x − 3)² + 2 is the same shape moved 3 right and 2 up, so the vertex moves from (0, 0) to (3, 2). (b) Stretch and reflection: y = 2x² is narrower, y = −x² opens downward."
f = Fig(780, 270)
f.text(195, 18, "(a) shift: y = (x − 3)² + 2", size=11.5, color=NAVY, bold=True)
a = Axes(f, 30, 28, 330, 225, (-3, 6), (-1, 8)); a.grid(1, 1).axes()
a.curve(lambda x: x*x, color=SLATE, sw=1.6, dash=True); a.curve(lambda x: (x-3)**2 + 2, color=NAVY, sw=2.4)
a.pt(0, 0, "(0, 0)", color=SLATE, dx=-6, dy=14, anchor="end"); a.pt(3, 2, "vertex (3, 2)", color=RED, dx=10, dy=18)
f.arrow([(a.X(0.3), a.Y(0.4)), (a.X(2.7), a.Y(1.7))], color=TEAL, sw=1.6)
f.text(585, 18, "(b) stretch and reflect", size=11.5, color=NAVY, bold=True)
b = Axes(f, 410, 28, 350, 225, (-3, 3), (-5, 5)); b.grid(1, 1).axes()
b.curve(lambda x: x*x, color=SLATE, sw=1.6, dash=True)
b.curve(lambda x: 2*x*x, color=NAVY, sw=2.4); b.curve(lambda x: -x*x, color=RED, sw=2.4)
f.text(b.X(0.55), b.Y(4.6), "y = 2x²", size=11, color=NAVY, bold=True, anchor="start")
f.text(b.X(0.9), b.Y(-3.6), "y = −x²", size=11, color=RED, bold=True, anchor="start")
f.text(b.X(-2.9), b.Y(3.6), "y = x² (dashed)", size=10, color=SLATE, anchor="start")
```

## 1.6 Eight ways functions are used in computing

1. **Input-output rules in programs.** A C function `float vat(float price)` is a mathematical function: one input gives exactly one output. When the same input could give two outputs the program becomes unpredictable. Thinking in functions makes code easy to test. A shopkeeper's billing program in Pokhara is a chain of such functions.
2. **Mobile data and mobile top-up.** The cost of a data pack as a function of megabytes is a piecewise function: a fixed price per pack and extra charges beyond it. NTC and Ncell use such step functions in their tariffs. Reading the graph tells a customer which pack is cheapest for his usage. The taxi fare in Practice 10 is the same idea.
3. **Hash functions.** A hash maps any input to a fixed-size number, for example a student roll number to a table slot. It is a function (same input, same output) but not one-to-one, so collisions occur. This is the basis of fast database indexes and password storage.
4. **Graphics and screens.** Every pixel on a screen is placed with coordinates, and shifting, scaling and reflecting a picture uses exactly the transformations of Section 1.5. A phone zooming into a photo is applying y = f(bx). Game engines apply these transformations millions of times per second.
5. **Signals and sound.** Music, radio and AC electricity are sine-type functions of time, as the oscilloscope in Plate 1.1 shows. Changing the amplitude is a vertical stretch and changing the frequency is a horizontal compression. FM radio stations in Kathmandu differ only in the carrier frequency.
6. **Growth and decay.** Money in a savings account at 8% interest grows as 100000 × 1.08ᵗ, an exponential function. Bacteria and the spread of a rumour on social media follow similar curves. The inverse function, the logarithm, tells us how many years are needed to double the money.
7. **Algorithm analysis.** The running time of a program is a function of the input size n, such as n, n² or log n. Comparing the graphs shows why a log n search in a sorted list beats an n search for a million records. Computer scientists compare programs by comparing function growth.
8. **Encoding and decoding.** Encryption is an invertible function: a message goes in and a cipher comes out, and the inverse function recovers the message. Only a one-to-one function can be reversed. This is why Section 1.3 matters for the security of ConnectIPS and Fonepay payments.

## Formula and fact sheet

- Domain restrictions: denominators ≠ 0, even-root radicands ≥ 0, log arguments > 0.
- Even: f(−x) = f(x). Odd: f(−x) = −f(x).
- (f∘g)(x) = f(g(x)). Inverse: swap x and y, solve; graph reflects in y = x.
- log(xy) = log x + log y; log(xᵖ) = p log x; logₐ x = ln x / ln a.
- sin²θ + cos²θ = 1; sin 2θ = 2 sin θ cos θ; cos 2θ = 1 − 2 sin²θ.
- |x| < a ⇔ −a < x < a; |x| > a ⇔ x < −a or x > a.

## Chapter summary

- A function pairs each input with exactly one output; domain and range come from restrictions of the formula.
- Even and odd symmetry, composition and inverses are the algebra of functions.
- Transformations shift, stretch and reflect graphs; knowing them saves plotting.
- Exponent, logarithm and trigonometric rules are the toolkit used in every later unit.

## Practice

1. Find the domain of (a) f(x) = √(6 − x − x²), (b) g(x) = ln(x² − 5x + 6), (c) h(x) = (x + 1)/(x² − 4).
2. Find the range of f(x) = 3 − 2x² and of g(x) = 2ˣ + 1.
3. If f(x) = x² + 1 and g(x) = 1/(x − 1), find f∘g, g∘f and their domains.
4. Show that f(x) = (2x + 1)/(x − 3) is one-to-one and find f⁻¹.
5. Classify as even, odd or neither: (a) x sin x, (b) x² + sin x, (c) (eˣ − e⁻ˣ)/2.
6. Solve |2x − 3| ≤ 5.
7. Sketch y = |x² − 4| by describing the transformation.
8. Simplify log₂ 40 − log₂ 5 + 2 log₂ 3.
9. If f(x + 1) = x² + 3x + 2 find f(x).
10. A taxi charges Rs 60 for the first km and Rs 40 for each further km (or part). Write the fare as a piecewise function of distance d and evaluate f(3.5).

::: note Answers and worked solutions
**1.** (a) 6 − x − x² ≥ 0 ⇔ x² + x − 6 ≤ 0 ⇔ (x + 3)(x − 2) ≤ 0, so **[−3, 2]**. (b) x² − 5x + 6 = (x − 2)(x − 3) > 0, so **x < 2 or x > 3**. (c) x² ≠ 4, so **all reals except ±2**.
**2.** f(x) = 3 − 2x² ≤ 3, maximum 3 at x = 0: **(−∞, 3]**. g: 2ˣ > 0, so g > 1: **(1, ∞)**.
**3.** (f∘g)(x) = 1/(x − 1)² + 1, domain x ≠ 1. (g∘f)(x) = 1/(x² + 1 − 1) = 1/x², domain x ≠ 0.
**4.** If (2a + 1)/(a − 3) = (2b + 1)/(b − 3), cross-multiplying gives 2ab − 6a + b − 3 = 2ab − 6b + a − 3, so 7b = 7a, hence a = b. Inverse: y(x − 3) = 2x + 1 ⇒ x(y − 2) = 3y + 1 ⇒ **f⁻¹(x) = (3x + 1)/(x − 2)**.
**5.** (a) x sin x is odd × odd = **even**. (b) x² is even, sin x is odd, so **neither**. (c) **odd** (this is sinh x).
**6.** −5 ≤ 2x − 3 ≤ 5 ⇒ −2 ≤ 2x ≤ 8 ⇒ **−1 ≤ x ≤ 4**.
**7.** Draw the parabola y = x² − 4 (vertex (0, −4), roots ±2), then reflect the part between x = −2 and 2 (below the axis) upward: a "W" with a peak (0, 4).
**8.** log₂(40/5) + log₂ 9 = log₂ 8 + log₂ 9 = 3 + log₂ 9 = **log₂ 72 ≈ 6.17**.
**9.** Put t = x + 1: f(t) = (t − 1)² + 3(t − 1) + 2 = t² + t. So **f(x) = x² + x**.
**10.** f(d) = 60 for 0 < d ≤ 1, and f(d) = 60 + 40·⌈d − 1⌉ for d > 1. f(3.5) = 60 + 40 × ⌈2.5⌉ = 60 + 120 = **Rs 180**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Define even and odd functions. Test f(x) = x³ − x, g(x) = x² + x and h(x) = x² cos x, and state what the symmetry of each graph is.**

A function f is **even** if f(−x) = f(x) for every x in its domain, and **odd** if f(−x) = −f(x). The test is to replace x by −x, simplify, and compare with f(x) and with −f(x). Both definitions need the domain to be symmetric about 0 (if 3 is in the domain, so is −3).

1. **f(x) = x³ − x.** f(−x) = (−x)³ − (−x) = −x³ + x = −(x³ − x) = −f(x). So f is **odd**. Its graph is symmetric about the origin: rotating it by 180° leaves it unchanged.
2. **g(x) = x² + x.** g(−x) = x² − x. This is neither g(x) nor −g(x), so g is **neither** even nor odd. The parabola is symmetric about the line x = −½, not about the y-axis.
3. **h(x) = x² cos x.** h(−x) = (−x)² cos(−x) = x² cos x = h(x). So h is **even** (even × even = even). Its graph is the mirror image in the y-axis.

| Type | Test | Graph symmetry | Examples |
|---|---|---|---|
| Even | f(−x) = f(x) | about the y-axis | x², \|x\|, cos x |
| Odd | f(−x) = −f(x) | about the origin | x³, sin x, 1/x |

**Use.** Symmetry halves the work: to plot an even or odd function we draw it for x ≥ 0 and complete the rest by reflection. In integration, an odd function over [−a, a] always gives 0.

**Q (5 marks). Find the domain and range of f(x) = √(9 − x²) and g(x) = ln(x − 1), and sketch the shape of each in words.**

The **domain** is the set of inputs for which the formula makes sense, and the **range** is the set of outputs obtained. Three restrictions control almost every exam question: the denominator cannot be 0, an even root needs a non-negative radicand, and a logarithm needs a positive argument.

1. **f(x) = √(9 − x²).** We need 9 − x² ≥ 0, that is x² ≤ 9, so −3 ≤ x ≤ 3. The domain is **[−3, 3]**. Inside, 9 − x² runs from 0 up to 9, so its square root runs from 0 up to 3. The range is **[0, 3]**. The graph is the upper half of the circle x² + y² = 9, a semicircle of radius 3.
2. **g(x) = ln(x − 1).** We need x − 1 > 0, so x > 1. The domain is **(1, ∞)**. As x → 1⁺ the value goes to −∞ and as x → ∞ it increases without bound, so the range is **all real numbers**. The graph is the curve y = ln x moved 1 unit to the right (Section 1.5); the line x = 1 is a vertical asymptote.

**Check.** Take x = 5 in g: ln 4 ≈ 1.386, a valid output. Take x = 4 in f: 9 − 16 < 0, so 4 is not in the domain.

**Q (10 marks). What is a function? Explain domain and range, the standard families of functions with their graphs, composition and inverse functions, and the rules for transforming graphs.**

**Introduction.** A **function** f from a set A to a set B is a rule that assigns to each element x of A exactly one element f(x) of B. The set A is the **domain**, and the set of values actually produced is the **range**. A graph represents a function only if every vertical line cuts it at most once (the vertical line test). Calculus studies how such rules change, so this chapter is its alphabet.

**Domain and range.** Domain restrictions come from three rules: no division by zero, no even root of a negative number, and only positive arguments in a logarithm. For example the domain of ln(x² − 5x + 6) is x < 2 or x > 3 (Practice 1).

**Standard families (Figure 1.1).**

| Family | Example | Domain | Range | Key feature |
|---|---|---|---|---|
| Polynomial | x², x³ | all reals | [0, ∞) for x²; all reals for x³ | smooth, no breaks |
| Rational | 1/x | x ≠ 0 | y ≠ 0 | vertical and horizontal asymptotes |
| Root | √x | x ≥ 0 | [0, ∞) | starts at origin, rises slowly |
| Exponential | eˣ | all reals | (0, ∞) | always positive, grows fast |
| Logarithm | ln x | x > 0 | all reals | inverse of eˣ |
| Trigonometric | sin x | all reals | [−1, 1] | periodic, period 2π |

**Even and odd functions.** An even function has f(−x) = f(x) (symmetric about the y-axis, like x²); an odd function has f(−x) = −f(x) (symmetric about the origin, like x³ and sin x).

**Composition and inverse.** The composition (f∘g)(x) = f(g(x)) applies g first and then f; in general f∘g ≠ g∘f. A one-to-one function has an **inverse** f⁻¹ found by swapping x and y and solving; its graph is the reflection of f in the line y = x (Figure 1.2). Only one-to-one functions can be inverted, which is why x² is restricted to x ≥ 0 before taking √.

**Transformations (Figure 1.3).** From y = f(x): f(x) + k shifts up, f(x − h) shifts right, −f(x) reflects in the x-axis, f(−x) reflects in the y-axis, a·f(x) stretches vertically and f(bx) compresses horizontally. For example y = (x − 3)² + 2 is y = x² moved 3 right and 2 up, with vertex (3, 2).

**Applications.** Dish antennas use the parabola, loans use the exponential, and sound uses the sine (Plate 1.1).

**Conclusion.** Every later idea (limit, derivative, integral) is applied to these functions. A student who can name the family, find the domain and range, and sketch the graph by transformation has done most of the work of a calculus problem.

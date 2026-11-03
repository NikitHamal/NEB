---
subject: Mathematics I
grade: BCA Semester 1
unit: 5
title: Integration
area: BCA 104 · Mathematics I · Unit 5
---

Integration reverses differentiation and also adds up infinitely many infinitesimal pieces. With it we compute areas, volumes, total change, averages and, in the next unit, solve differential equations.

::: key What this unit gives you
- Antiderivatives, the table of standard integrals, and the substitution, parts and partial-fraction methods.
- The definite integral, the Fundamental Theorem of Calculus, and its properties.
- Area between curves, volume of revolution, average value, and improper integrals.
:::

## 5.1 Indefinite integrals

F is an **antiderivative** of f if F′ = f. The family of all antiderivatives is the **indefinite integral** ∫ f(x) dx = F(x) + C, where C is an arbitrary constant.

| f(x) | ∫ f dx | f(x) | ∫ f dx |
|---|---|---|---|
| xⁿ (n ≠ −1) | xⁿ⁺¹/(n + 1) | 1/x | ln\|x\| |
| eˣ | eˣ | aˣ | aˣ/ln a |
| sin x | −cos x | cos x | sin x |
| sec²x | tan x | cosec²x | −cot x |
| sec x tan x | sec x | 1/(1 + x²) | tan⁻¹x |
| 1/√(1 − x²) | sin⁻¹x | tan x | ln\|sec x\| |
| 1/√(x² + a²) | ln\|x + √(x² + a²)\| | 1/(x² − a²) | (1/2a) ln\|(x − a)/(x + a)\| |

Linearity: ∫ (af + bg) = a∫ f + b∫ g. Always check an answer by differentiating it.

::: example Worked example
∫ (3x² + 2x + 1) dx = x³ + x² + x + C.
∫ (√x + 1/x²) dx = (2/3)x^{3/2} − 1/x + C.
∫ sin²x dx = ∫ (1 − cos 2x)/2 dx = x/2 − (sin 2x)/4 + C.
:::

```photogrid label="5.1" cols="3" ratio="1.2" caption="Integration in history and in Nepal. (a) Archimedes of Syracuse (c. 287-212 BC) found areas and volumes by the method of exhaustion, the ancestor of the integral. (b) Bernhard Riemann (1826-1866) gave the definition by sums that we use today. (c) The reservoir wall of the Kaligandaki A hydropower station in Syangja: the force of water on the wall is an integral of pressure over depth."
@ photo id="bca104/archimedes" cap="Archimedes (painting by D. Fetti, 1620)"
fit 1.2
focus 0.5 0.7
@ photo id="bca104/riemann" cap="Bernhard Riemann"
fit 1.2
focus 0.5 0.72
@ photo id="bca104/kgdam" cap="Kaligandaki A dam, Syangja"
fit 1.2
call 0.5 0.93 0.5 0.6 "F = ∫ ρ g h w dh"
```

## 5.2 Integration by substitution

If an integral has the form ∫ f(g(x)) g′(x) dx, put u = g(x), du = g′(x) dx, and integrate in u.

::: example Worked example
**(a)** ∫ 2x e^{x²} dx: u = x², du = 2x dx, so ∫ eᵘ du = e^{x²} + C.
**(b)** ∫ x/(x² + 1) dx: u = x² + 1, du = 2x dx, so ½ ∫ du/u = **½ ln(x² + 1) + C**.
**(c)** ∫ tan x dx = ∫ sin x/cos x dx: u = cos x, du = −sin x dx, so −ln|cos x| + C = ln|sec x| + C.
**(d)** ∫ cos³x dx = ∫ (1 − sin²x) cos x dx: u = sin x, so sin x − sin³x/3 + C.
**(e)** ∫ 1/(x ln x) dx: u = ln x, so ln|ln x| + C.
**(f)** ∫ (2x + 3)⁵ dx = (2x + 3)⁶/12 + C.
:::

## 5.3 Integration by parts

From (uv)′ = u′v + uv′: **∫ u dv = uv − ∫ v du**. Choose u in the order **LIATE** (Logarithmic, Inverse trig, Algebraic, Trig, Exponential): the first type that appears becomes u.

::: example Worked example
**(a)** ∫ x eˣ dx: u = x, dv = eˣ dx ⇒ x eˣ − ∫ eˣ dx = **(x − 1)eˣ + C**.
**(b)** ∫ x² ln x dx: u = ln x, dv = x² dx ⇒ (x³/3) ln x − ∫ x²/3 dx = **(x³/3) ln x − x³/9 + C**.
**(c)** ∫ ln x dx: u = ln x, dv = dx ⇒ x ln x − x + C.
**(d)** ∫ x sin x dx = −x cos x + sin x + C.
**(e)** ∫ eˣ sin x dx = I. By parts twice, I = eˣ sin x − eˣ cos x − I, so **I = eˣ(sin x − cos x)/2 + C**.
**(f)** ∫ tan⁻¹x dx = x tan⁻¹x − ½ ln(1 + x²) + C.
:::

## 5.4 Partial fractions

A proper rational function P(x)/Q(x) (degree P < degree Q) is split into simpler fractions by factors of Q: a linear factor (x − a) gives A/(x − a); a repeated factor (x − a)² gives A/(x − a) + B/(x − a)²; an irreducible quadratic gives (Ax + B)/(x² + px + q). If the degree of P ≥ degree of Q, divide first.

::: example Worked example
**(a)** 1/((x − 1)(x + 2)) = A/(x − 1) + B/(x + 2). Then 1 = A(x + 2) + B(x − 1); x = 1 gives A = 1/3; x = −2 gives B = −1/3. So ∫ = ⅓ ln|x − 1| − ⅓ ln|x + 2| = **⅓ ln|(x − 1)/(x + 2)| + C**.
**(b)** (3x + 5)/((x + 1)²) = 3/(x + 1) + 2/(x + 1)². ∫ = 3 ln|x + 1| − 2/(x + 1) + C.
**(c)** ∫ (x² + 1)/(x − 1) dx: divide, x² + 1 = (x − 1)(x + 1) + 2, so ∫ (x + 1 + 2/(x − 1)) dx = x²/2 + x + 2 ln|x − 1| + C.
:::

## 5.5 The definite integral and the Fundamental Theorem

The **definite integral** ∫ₐᵇ f(x) dx is the limit of Riemann sums Σ f(xᵢ) Δx, the signed area between the graph and the x-axis from a to b. The **Fundamental Theorem of Calculus** connects it to antiderivatives:

- **Part 1**: if F(x) = ∫ₐˣ f(t) dt then F′(x) = f(x).
- **Part 2**: **∫ₐᵇ f(x) dx = F(b) − F(a)** for any antiderivative F.

**Properties.** ∫ₐᵇ f = −∫ᵇₐ f; ∫ₐᵃ f = 0; ∫ₐᵇ f = ∫ₐᶜ f + ∫ᶜᵇ f; ∫ₐᵇ f(x) dx = ∫ₐᵇ f(a + b − x) dx; for even f, ∫₋ₐᵃ f = 2∫₀ᵃ f; for odd f, ∫₋ₐᵃ f = 0. When substituting in a definite integral, change the limits too.

::: example Worked example
**(a)** ∫₀^π sin x dx = [−cos x]₀^π = 1 + 1 = **2**.
**(b)** ∫₁² dx/x = ln 2 − ln 1 = **ln 2 ≈ 0.693**.
**(c)** ∫₀¹ 2x e^{x²} dx: u = x², limits 0 → 1: ∫₀¹ eᵘ du = **e − 1 ≈ 1.718**.
**(d)** ∫₀^{π/2} sin³x dx = ∫₀^{π/2} (1 − cos²x) sin x dx, u = cos x: ∫₀¹ (1 − u²) du = 1 − 1/3 = **2/3**.
**(e)** ∫₋₁¹ x³ dx = **0** (odd function).
**(f)** ∫₀¹ x eˣ dx = [(x − 1)eˣ]₀¹ = 0 − (−1) = **1**.
:::

```svgfig label="5.1" caption="Riemann sums for the area under f(x) = x² on [0, 2]. (a) Four left rectangles under-estimate (1.75). (b) Four right rectangles over-estimate (3.75). (c) Twenty mid-point rectangles are almost exact. As n → ∞ every version tends to the definite integral ∫₀² x² dx = 8/3 ≈ 2.6667."
f = Fig(780, 250)
fx = lambda x: x * x
mid = sum(fx(0.05 + 0.1 * k) * 0.1 for k in range(20))
for i, (mode, n, t, val) in enumerate([("left", 4, "(a) left sum, n = 4", "1.75"), ("right", 4, "(b) right sum, n = 4", "3.75"), ("mid", 20, "(c) mid-point sum, n = 20", f"{mid:.4f}")]):
    cx = 8 + i * 258
    f.box(cx, 4, 246, 242, "", fill=SOFT, stroke="#cbd5e1")
    f.text(cx + 123, 22, t, size=11, color=NAVY, bold=True)
    a = Axes(f, cx + 22, 34, 208, 150, (-0.2, 2.3), (-0.3, 4.6)); a.grid(1, 1, size=8.5)
    a.bars(fx, 0, 2, n, mode=mode); a.curve(fx, 0, 2.3, color=NAVY, sw=2.4); a.axes("", "")
    f.text(cx + 123, 214, "sum ≈ " + val, size=12, color=TEAL if i == 2 else AMBER, bold=True); f.text(cx + 123, 235, "exact value 8/3 = 2.6667", size=9.5, color=SLATE)
```

## 5.6 Applications

**Area between curves.** If f ≥ g on [a, b]: A = ∫ₐᵇ [f(x) − g(x)] dx. If the curves cross, split at the intersections.

**Volume of revolution** about the x-axis (disc method): V = π ∫ₐᵇ [f(x)]² dx; with a hole (washer): V = π ∫ (R² − r²) dx. About the y-axis (shell method): V = 2π ∫ x f(x) dx.

**Average value** of f on [a, b]: (1/(b − a)) ∫ₐᵇ f dx. **Arc length**: L = ∫ₐᵇ √(1 + (f′)²) dx. **Total change**: ∫ of a rate gives the net change (distance = ∫ speed dt).

::: example Worked example
**Area** between y = x and y = x²: intersections x = 0, 1; A = ∫₀¹ (x − x²) dx = ½ − ⅓ = **1/6**.
**Area** under y = sin x from 0 to π: **2**.
**Volume** of y = x² about the x-axis from 0 to 1: V = π ∫₀¹ x⁴ dx = **π/5**. For y = √x on [0, 4]: V = π ∫₀⁴ x dx = **8π**.
**Average value** of f(x) = x² on [0, 3]: (1/3)(27/3) = **3**.
**Net displacement** for velocity v(t) = 3t² − 6t + 2 from t = 0 to 2: [t³ − 3t² + 2t]₀² = 8 − 12 + 4 = **0** (the body returns to its start; the *distance* travelled is ∫|v| dt, which is larger).
:::

```svgfig label="5.2" caption="Two applications of the definite integral. (a) The area between y = x and y = x² on [0, 1] is ∫₀¹ (x − x²) dx = 1/2 − 1/3 = 1/6. (b) Rotating y = √x about the x-axis for 0 ≤ x ≤ 4 sweeps out a solid made of thin discs of radius √x, so V = π∫₀⁴ x dx = 8π ≈ 25.13 cubic units."
f = Fig(780, 270)
f.box(8, 4, 330, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(173, 22, "(a) area between two curves", size=11, color=NAVY, bold=True)
a = Axes(f, 40, 36, 270, 190, (-0.1, 1.2), (-0.1, 1.2)); a.grid(0.5, 0.5, size=8.5)
a.area(lambda x: x, 0, 1, fn2=lambda x: x * x, fill="#99f6e4"); a.axes()
a.curve(lambda x: x, color=NAVY, sw=2.4); a.curve(lambda x: x * x, color=RED, sw=2.4)
f.text(a.X(0.7), a.Y(0.9), "y = x", size=11, color=NAVY, bold=True, anchor="start"); f.text(a.X(0.78), a.Y(0.4), "y = x²", size=11, color=RED, bold=True, anchor="start"); f.text(173, 250, "area = 1/6 ≈ 0.1667", size=11, color=TEAL, bold=True)
f.box(346, 4, 426, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(559, 22, "(b) solid of revolution about the x-axis", size=11, color=NAVY, bold=True)
b = Axes(f, 370, 36, 380, 190, (-0.4, 4.6), (-2.4, 2.4)); b.area(lambda x: math.sqrt(x), 0, 4, fn2=lambda x: -math.sqrt(x), fill="#bfdbfe", opacity=0.6)
for xv in (1, 2, 3, 4):
    f.raw(f'<ellipse cx="{b.X(xv)}" cy="{b.Y(0)}" rx="6" ry="{round(b.Y(0) - b.Y(math.sqrt(xv)), 2)}" fill="none" stroke="{TEAL}" stroke-width="1.3"/>')
b.axes(); b.curve(math.sqrt, 0, 4, color=NAVY, sw=2.4); b.curve(lambda x: -math.sqrt(x), 0, 4, color=NAVY, sw=1.6, dash=True)
f.text(b.X(1.0), b.Y(1.9), "y = √x, rotated", size=11, color=NAVY, bold=True, anchor="start"); f.text(559, 250, "V = π ∫₀⁴ x dx = 8π ≈ 25.13", size=11, color=TEAL, bold=True)
```

## 5.7 Improper integrals

An integral with an infinite limit or an infinite integrand is defined as a limit.

::: example Worked example
**(a)** ∫₁^∞ x⁻² dx = lim (b→∞) [−1/x]₁ᵇ = 1 − 0 = **1** (converges).
**(b)** ∫₁^∞ 1/x dx = lim ln b = ∞ (**diverges**).
**(c)** ∫₀¹ x^{−1/2} dx = lim (a→0⁺) [2√x]ₐ¹ = **2** (converges).
**(d)** ∫₀^∞ e^{−x} dx = **1**.
**Rule:** ∫₁^∞ x^{−p} dx converges iff p > 1; ∫₀¹ x^{−p} dx converges iff p < 1.
:::

```svgfig label="5.3" caption="Improper integrals over an infinite interval. (a) The area under y = 1/x² from 1 to infinity is finite: ∫₁^b dx/x² = 1 − 1/b → 1. (b) The area under y = 1/x is infinite: ∫₁^b dx/x = ln b → ∞. Both curves tend to 0, yet only the first area is finite."
f = Fig(780, 240)
for i, (fn, t, s, c) in enumerate([(lambda x: 1 / (x * x), "(a) y = 1/x²", "converges: area = 1", TEAL), (lambda x: 1 / x, "(b) y = 1/x", "diverges: area = ∞", RED)]):
    cx = 8 + i * 388
    f.box(cx, 4, 376, 232, "", fill=SOFT, stroke="#cbd5e1"); f.text(cx + 188, 22, t, size=11.5, color=NAVY, bold=True)
    a = Axes(f, cx + 36, 34, 320, 150, (0, 6.5), (0, 1.2)); a.grid(1, 0.5, size=8.5)
    a.area(fn, 1, 6.5, fill="#99f6e4" if i == 0 else "#fecaca"); a.axes(); a.curve(fn, 1, 6.5, color=NAVY, sw=2.4); a.vline(1, 0, 1.2, color=AMBER)
    f.text(cx + 188, 222, s, size=11.5, color=c, bold=True)
```

## 5.8 Eight uses of integration

1. **Area of irregular land.** The area under a curve is a definite integral, so surveyors and map software can find the area of a plot with a curved boundary. In Nepal land is measured in ropani and kattha, and the same idea converts a measured outline into area. A smaller strip width gives a more exact answer (Figure 5.1).
2. **Volume of tanks and solids.** Cutting a solid into thin discs and adding them gives volume (Figure 5.2b). Water tank, bottle and dam designers use it to know how much each shape holds. The reservoir of a hydropower plant is estimated this way.
3. **Distance from speed.** If the speed v(t) of a bus is known, the distance travelled is ∫v dt. A GPS tracker adds many small distances to give the trip length. This is the reverse of differentiation: position is the integral of speed.
4. **Work, force and pressure.** The pressure on a dam wall increases with depth, so the total force is an integral of pressure over the wall (Plate 5.1c). Engineers of the Kaligandaki and Marsyangdi plants need this to make the wall strong enough. A constant-force formula alone would be wrong.
5. **Probability and statistics.** For a continuous variable, the probability that a value lies between a and b is the area under its density curve. The normal curve of exam marks is integrated to find how many students score above 60. Tribhuvan University result analysis is built on such areas.
6. **Electricity and signals.** The charge stored in a capacitor is the integral of the current, and the energy used by a house is the integral of power over time. Nepal Electricity Authority meters add power over hours in the same way. Digital signal processing also integrates signals to find their average and energy.
7. **Computer graphics and numerical methods.** Computers cannot do symbolic integration for every function, so they use Riemann-type sums such as the trapezoidal and Simpson's rules. These give an accurate area with a fast loop. Games and simulations use them for physics.
8. **Average value and economics.** The average value of a function on [a, b] is (1/(b − a))∫f dx. An economist finds the average daily electricity demand or the total revenue from a marginal revenue curve. The consumer surplus in a market is also an area between two curves.

## Formula and fact sheet

- ∫ xⁿ dx = xⁿ⁺¹/(n + 1); ∫ dx/x = ln|x|; ∫ eˣ = eˣ; ∫ sin = −cos; ∫ cos = sin.
- Substitution: u = g(x). Parts: ∫u dv = uv − ∫v du, LIATE.
- FTC: ∫ₐᵇ f = F(b) − F(a). Even: 2∫₀ᵃ; odd: 0.
- Area = ∫ (top − bottom). Disc volume = π∫ f². Average = (1/(b − a))∫ f.
- Improper: ∫₁^∞ x^{−p} converges for p > 1.

## Chapter summary

- Integration is reverse differentiation; always add C for indefinite integrals and verify by differentiating.
- Substitution undoes the chain rule, parts undoes the product rule, partial fractions handle rational functions.
- The Fundamental Theorem lets us compute definite integrals from antiderivatives.
- Areas, volumes, averages and total change are all definite integrals; improper integrals are limits.

## Practice

1. Evaluate (a) ∫ (4x³ − 3/x + eˣ) dx, (b) ∫ (x² + 1)² dx, (c) ∫ cos²x dx.
2. Evaluate by substitution (a) ∫ x√(x² + 4) dx, (b) ∫ e^{3x + 1} dx, (c) ∫ sin x cos⁴x dx.
3. Evaluate by parts (a) ∫ x cos x dx, (b) ∫ x e^{2x} dx, (c) ∫ x ln x dx.
4. Evaluate ∫ (2x + 3)/((x − 1)(x + 2)) dx.
5. Evaluate (a) ∫₀² (3x² − 2x) dx, (b) ∫₀^{π/4} sec²x dx, (c) ∫₁^e (ln x)/x dx.
6. Find the area enclosed by y = x² and y = 4x − x².
7. Find the volume generated by revolving y = x² about the x-axis between x = 1 and x = 2.
8. Find the average value of sin x on [0, π].
9. Does ∫₁^∞ 1/√x dx converge? Does ∫₁^∞ 1/x^{3/2} dx?
10. If F(x) = ∫₀ˣ t e^{t} dt find F′(x) and F(1).

::: note Answers and worked solutions
**1.** (a) x⁴ − 3 ln|x| + eˣ + C. (b) x⁵/5 + 2x³/3 + x + C. (c) x/2 + (sin 2x)/4 + C.
**2.** (a) u = x² + 4: ⅓(x² + 4)^{3/2} + C. (b) ⅓ e^{3x + 1} + C. (c) u = cos x: −cos⁵x/5 + C.
**3.** (a) x sin x + cos x + C. (b) (x/2)e^{2x} − e^{2x}/4 + C. (c) (x²/2) ln x − x²/4 + C.
**4.** (2x + 3)/((x − 1)(x + 2)) = A/(x − 1) + B/(x + 2): A = 5/3, B = 1/3. ∫ = **(5/3) ln|x − 1| + (1/3) ln|x + 2| + C**.
**5.** (a) [x³ − x²]₀² = 8 − 4 = **4**. (b) tan(π/4) − 0 = **1**. (c) [ (ln x)²/2 ]₁^e = **1/2**.
**6.** Intersections: x² = 4x − x² ⇒ x = 0, 2. A = ∫₀² (4x − 2x²) dx = [2x² − 2x³/3]₀² = 8 − 16/3 = **8/3**.
**7.** V = π ∫₁² x⁴ dx = π (32 − 1)/5 = **31π/5 ≈ 19.48**.
**8.** (1/π)[−cos x]₀^π = 2/π ≈ **0.637**.
**9.** ∫₁^∞ x^{−1/2} diverges (p = 1/2 ≤ 1). ∫₁^∞ x^{−3/2} = [−2x^{−1/2}]₁^∞ = **2**, converges.
**10.** F′(x) = x eˣ. F(1) = ∫₀¹ t eᵗ dt = [(t − 1)eᵗ]₀¹ = **1**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Evaluate ∫ x eˣ dx by parts and hence find ∫₀¹ x eˣ dx.**

**Integration by parts** comes from the product rule: ∫u dv = uv − ∫v du. The skill is to choose u so that du is simpler than u. The order of preference is *LIATE*: Logarithmic, Inverse trigonometric, Algebraic, Trigonometric, Exponential.

1. In x eˣ the algebraic factor x comes before the exponential, so let u = x and dv = eˣ dx.
2. Then du = dx and v = eˣ.
3. Apply the formula: ∫ x eˣ dx = x eˣ − ∫ eˣ dx.
4. The remaining integral is eˣ, so ∫ x eˣ dx = x eˣ − eˣ + C = **(x − 1)eˣ + C**.
5. Check by differentiating: d/dx[(x − 1)eˣ] = eˣ + (x − 1)eˣ = x eˣ ✓.

For the definite integral use the Fundamental Theorem: ∫₀¹ x eˣ dx = [(x − 1)eˣ]₀¹ = (0)(e) − (−1)(1) = **1**. The area under the curve y = x eˣ between x = 0 and x = 1 is exactly one square unit.

**Q (5 marks). Find the area between y = x and y = x² and the volume generated when the curve y = √x, 0 ≤ x ≤ 4, is rotated about the x-axis.**

*Area (Figure 5.2a).* The curves meet where x = x², that is x = 0 and x = 1. Between them the line is above the parabola (at x = 0.5: 0.5 > 0.25). The area is the integral of (upper − lower): ∫₀¹ (x − x²) dx = [x²/2 − x³/3]₀¹ = 1/2 − 1/3 = **1/6 square unit**.

*Volume (Figure 5.2b).* A thin slice at position x is a disc of radius y = √x and thickness dx, so its volume is πy² dx = πx dx. Adding all slices from 0 to 4:

V = π ∫₀⁴ x dx = π [x²/2]₀⁴ = π × 8 = **8π ≈ 25.13 cubic units**.

*Remark.* The disc formula is V = π∫ y² dx. If the region lies between two curves a washer (a disc with a hole) is used: V = π∫ (R² − r²) dx. Always sketch the region first and write which curve is on top.

**Q (10 marks). Define the definite integral through Riemann sums. State the Fundamental Theorem of Calculus. Explain the methods of integration (substitution, parts, partial fractions) with an example of each, and explain improper integrals.**

**Introduction.** Integration reverses differentiation and also measures accumulated quantities such as area, distance and volume. The **indefinite integral** ∫f dx is the family of antiderivatives F(x) + C, and the **definite integral** ∫ₐᵇ f dx is a number, the signed area under the curve.

**Riemann sums (Figure 5.1).** Divide [a, b] into n strips of width Δx = (b − a)/n, build a rectangle of height f(xᵢ) on each, and add: Σ f(xᵢ)Δx. The definite integral is the limit of this sum as n → ∞. For f = x² on [0, 2] the sums are 1.75 (left, n = 4), 3.75 (right, n = 4) and tend to **8/3**.

**Fundamental Theorem of Calculus.** (1) If F(x) = ∫ₐˣ f(t) dt then F′(x) = f(x). (2) If G′ = f then ∫ₐᵇ f dx = G(b) − G(a). Example: ∫₀² x² dx = [x³/3]₀² = 8/3 ✓.

**Methods of integration.**

| Method | When used | Example | Result |
|---|---|---|---|
| Substitution | a function and its derivative appear | ∫ 2x cos(x²) dx, u = x² | sin(x²) + C |
| By parts | product of different types | ∫ x eˣ dx, u = x | (x − 1)eˣ + C |
| Partial fractions | rational function with factorable denominator | ∫ (3x + 5)/((x + 1)(x + 2)) dx | 2 ln\|x + 1\| + ln\|x + 2\| + C |

For the last example write (3x + 5)/((x + 1)(x + 2)) = A/(x + 1) + B/(x + 2). Then 3x + 5 = A(x + 2) + B(x + 1); putting x = −1 gives A = 2 and x = −2 gives B = 1.

**Applications (Figure 5.2).** Area between curves is ∫(upper − lower)dx, volume of revolution is π∫y² dx, and average value is (1/(b − a))∫f dx.

**Improper integrals (Figure 5.3).** An integral with an infinite limit is defined by a limit: ∫₁^∞ dx/x² = lim (b→∞) (1 − 1/b) = **1** (converges), but ∫₁^∞ dx/x = lim ln b = ∞ (diverges). The p-test: ∫₁^∞ dx/xᵖ converges if and only if p > 1.

**Conclusion.** Integration accumulates small pieces into a total. The Fundamental Theorem makes it practical by connecting it with antiderivatives, and the three methods cover most examination problems.

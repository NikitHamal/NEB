---
subject: Computer Graphics and Animation
grade: BCA Semester 6
unit: 4
title: Clipping
hours: 6
area: BCA 351 · Computer Graphics and Animation · Unit 4
---

A map of Nepal drawn into a small window on a phone must not spill over onto the rest of the screen, and drawing millions of triangles that are far outside the picture would waste time. **Clipping** removes the parts of primitives that lie outside a clip region (normally a rectangular window), and it is among the first things a renderer does, because discarding early saves all later work. This unit covers line clipping by the Cohen–Sutherland and Liang–Barsky algorithms and polygon clipping by Sutherland–Hodgman, with a numeric trace for each. The traces were computed by two independent implementations (the two line clippers must agree on every line) and the clipped polygon's area was checked against a fine-grid integration.

::: key What this unit gives you
- Point clipping and the idea of trivial accept and trivial reject.
- Cohen–Sutherland outcodes, the accept/reject tests and intersection formulas.
- Liang–Barsky parametric clipping with p and q.
- Sutherland–Hodgman polygon clipping, its four cases, and its limitation.
:::

## 4.1 The clipping problem

A point (x, y) is inside the window with corners (x_min, y_min) and (x_max, y_max) if x_min ≤ x ≤ x_max and y_min ≤ y ≤ y_max. A line is **inside** if both endpoints are, **outside** if both are beyond the *same* boundary, and otherwise it **crosses** a boundary and must be cut. Computing intersections for every line is expensive, so the good algorithms try to *accept or reject cheaply* first. Clipping can be applied to world coordinates before the viewport transform (the usual order in this book) or to the screen after it (**scissoring**).

For the examples the window is **(10, 10) to (50, 40)**: x from 10 to 50 and y from 10 to 40.

## 4.2 The Cohen–Sutherland line-clipping algorithm

**Outcodes.** Divide the plane into nine regions by extending the window edges. Give each endpoint a 4-bit **outcode** with bits (from the most significant) **top, bottom, right, left**: bit 1 is set if y > y_max (top), bit 2 if y < y_min (bottom), bit 3 if x > x_max (right) and bit 4 if x < x_min (left). A point inside has code 0000.

**Tests on a line with endpoint codes c₁ and c₂:**

1. If **c₁ OR c₂ = 0000**: both endpoints are inside, **trivially accept**.
2. If **c₁ AND c₂ ≠ 0000**: both are on the outer side of the same boundary, **trivially reject**.
3. Otherwise pick an endpoint with a non-zero code, find where the line meets *one* boundary that endpoint violates, replace the endpoint with the intersection, recompute its code and repeat.

**Intersection formulas** for the line through (x₁, y₁) and (x₂, y₂) with slope m = (y₂ − y₁)/(x₂ − x₁): with the **top or bottom** boundary y = y_edge: x = x₁ + (y_edge − y₁)/m; with the **left or right** boundary x = x_edge: y = y₁ + m(x_edge − x₁).

::: example Four lines against the window
| Line | P1 | Code 1 | P2 | Code 2 | AND | Result |
|---|---|---|---|---|---|---|
| AB | (5, 20) | 0001 | (30, 45) | 1000 | 0001 AND 1000 = 0000 | clip P1 -> (10.00, 25.00); clip P2 -> (25.00, 40.00); accept |
| CD | (20, 15) | 0000 | (40, 35) | 0000 | 0000 AND 0000 = 0000 | accept |
| EF | (0, 0) | 0101 | (5, 50) | 1001 | 0101 AND 1001 = 0001 | reject |
| GH | (0, 25) | 0001 | (60, 5) | 0110 | 0001 AND 0110 = 0000 | clip P1 -> (10.00, 21.67); clip P2 -> (45.00, 10.00); accept |

For **AB**, P1 = (5, 20) is left of the window (code 0001) and P2 = (30, 45) is above (1000). The AND is 0000 and the OR is non-zero, so clipping is needed. Clipping P1 against the left edge x = 10 gives y = 20 + (45 − 20)/(30 − 5) × (10 − 5) = **25**, so P1 becomes (10, 25). Clipping P2 against the top edge y = 40 gives x = 30 − (45 − 40)/1 = **25**, so P2 becomes (25, 40). The visible part is **(10.00, 25.00) to (25.00, 40.00)**, and after the cuts both codes are 0000 (accept). Line **EF** has codes 0101 and 1001 with AND = 0001 (both left of the window): rejected without computing anything. Line **GH** needs two cuts and ends as **(10.00, 21.67) to (45.00, 10.00)**.
:::

A short program computing outcodes (the checker uses the same rule):

```python
def outcode(x, y, xmin=10, ymin=10, xmax=50, ymax=40):
    code = 0
    if y > ymax: code |= 8
    if y < ymin: code |= 4
    if x > xmax: code |= 2
    if x < xmin: code |= 1
    return code

for p in [(5, 20), (30, 45), (20, 15), (0, 0), (60, 5)]:
    print(p, format(outcode(*p), "04b"))
```
```output
(5, 20) 0001
(30, 45) 1000
(20, 15) 0000
(0, 0) 0101
(60, 5) 0110
```
The loop runs at most four times for one line (at most one cut per boundary). The algorithm is efficient when most lines are trivially accepted or rejected (a large window or a tiny one), but can compute unnecessary intersections for lines that miss a corner of the window.

## 4.3 The Liang–Barsky algorithm

Liang and Barsky write the line **parametrically**: x = x₁ + t·Δx, y = y₁ + t·Δy, with t from 0 to 1 and Δx = x₂ − x₁, Δy = y₂ − y₁. The point is inside if for every boundary k: **pₖ · t ≤ qₖ**, where

| k | Boundary | pₖ | qₖ |
|---|---|---|---|
| 1 | left | −Δx | x₁ − x_min |
| 2 | right | Δx | x_max − x₁ |
| 3 | bottom | −Δy | y₁ − y_min |
| 4 | top | Δy | y_max − y₁ |

- If **pₖ = 0** the line is parallel to that boundary; if also qₖ < 0 it is outside, so reject.
- If **pₖ < 0** the line goes from outside to inside at that boundary (*entering*) and rₖ = qₖ/pₖ is a candidate for the lower limit t₀ = max(0, all entering rₖ).
- If **pₖ > 0** the line goes from inside to outside (*leaving*): rₖ is a candidate for the upper limit t₁ = min(1, all leaving rₖ).
- If t₀ > t₁ the line is outside; otherwise the clipped segment runs from t₀ to t₁.

::: example Liang–Barsky on line GH, (0, 25) to (60, 5)
Δx = 60, Δy = −20.

| k | Boundary | p_k | q_k | r = q/p |
|---|---|---|---|---|
| 1 | left | -60 | -10 | 0.1667 |
| 2 | right | 60 | 50 | 0.8333 |
| 3 | bottom | 20 | 15 | 0.7500 |
| 4 | top | -20 | 15 | -0.7500 |

The entering boundaries (those with p_k < 0) give t₀ = max(0, ...) = **0.1667** and those with p_k > 0 give t₁ = min(1, ...) = **0.7500**. The endpoints are (0 + 60·t₀, 25 − 20·t₀) and (0 + 60·t₁, 25 − 20·t₁), which is **(10.00, 21.67) to (45.00, 10.00)**, exactly the Cohen–Sutherland result. Note that Liang–Barsky computes **at most two intersections** (t₀ and t₁) and decides acceptance before computing the coordinates, which is why it is faster for lines that cross many boundaries.
:::

| | Cohen–Sutherland | Liang–Barsky |
|---|---|---|
| Idea | Region codes, repeated cutting | Parametric inequalities pt ≤ q |
| Intersections computed | Up to four, one at a time | At most two, at the end |
| Best case | Many trivial accepts/rejects | Any |
| Extension to 3D | Yes (six-bit codes) | Yes, easily |

## 4.4 Polygon clipping: Sutherland–Hodgman

Clipping a polygon is not the same as clipping its edges: the result must be a closed polygon, with new edges along the window boundary. The **Sutherland–Hodgman** algorithm clips the polygon against **one boundary at a time** (left, right, bottom, top), feeding each stage's output vertex list to the next. For each edge from the current vertex *c* to the next vertex *n*, with respect to the clip boundary:

1. **in → in:** output *n*.
2. **in → out:** output the *intersection*.
3. **out → out:** output nothing.
4. **out → in:** output the *intersection*, then *n*.

::: example Clipping a triangle
The triangle (0, 20), (40, 55), (60, 15) against the same window gives **6 vertices**:

| # | Vertex |
|---|---|
| 1 | (50.00, 15.83) |
| 2 | (10.00, 19.17) |
| 3 | (10.00, 28.75) |
| 4 | (22.86, 40.00) |
| 5 | (47.50, 40.00) |
| 6 | (50.00, 35.00) |

The triangle's area is 1150.0 square units; the clipped polygon's area (shoelace formula) is **821.43**, and a fine-grid numerical integration of the region inside both the triangle and the window agrees to within 0.5. Three vertices became six: each clip can add vertices.
:::

**Limitation.** For a *concave* polygon the algorithm can produce extra edges that run along the boundary connecting separate pieces (a degenerate overlap that looks fine when filled but is not a true polygon). The **Weiler–Atherton** algorithm handles concave polygons and concave windows by tracing the boundaries and producing separate polygons; **Cyrus–Beck** extends parametric clipping to any convex window. **Text and curves** are clipped at the level of whole characters, strings or by clipping their approximating lines. In 3D the same ideas clip against a view volume (Unit 5), done in hardware after projection.

## Chapter summary

- Clipping discards geometry outside the window; efficient algorithms accept or reject trivially before computing intersections.
- Cohen–Sutherland: a 4-bit outcode per endpoint; OR = 0 accepts, AND ≠ 0 rejects; otherwise cut at one boundary and repeat.
- Liang–Barsky: pₖt ≤ qₖ; t₀ = max of entering r, t₁ = min of leaving r; at most two intersections.
- Sutherland–Hodgman clips a polygon against each boundary in turn with four in/out cases; concave polygons need Weiler–Atherton.

## Practice

1. Write the Cohen–Sutherland outcode for (5, 60) against the window (10, 10)–(50, 40).
2. For which pairs of outcodes is a line trivially rejected?
3. Clip the line (0, 0) to (60, 30) against the window (10, 10)–(50, 40) by Cohen–Sutherland (give the final endpoints).
4. Compute p and q for the left boundary of the line (5, 20)–(30, 45).
5. In Liang–Barsky, what does pₖ = 0 and qₖ < 0 mean?
6. Why is Liang–Barsky often faster than Cohen–Sutherland?
7. List the four cases of Sutherland–Hodgman.
8. Why might Sutherland–Hodgman produce wrong results for a concave polygon?
9. How many clipping stages does Sutherland–Hodgman use for a rectangular window?
10. Give one situation where trivial rejection saves most of the work.

::: note Answers and worked solutions
**1.** x = 5 < 10 (left), y = 60 > 40 (top): code **1001** (top, bottom, right, left = 1, 0, 0, 1).
**2.** When the AND of the two codes is non-zero (both endpoints beyond the same boundary).
**3.** (0, 0) has code 0101 (bottom, left). The slope is 0.5; clipping against the bottom edge y = 10 gives x = 10/0.5 = 20, point (20, 10). Its code is 0000. P2 = (60, 30) has code 0010 (right); clip at x = 50: y = 0.5 × 50 = 25, point (50, 25). Result **(20, 10) to (50, 25)**.
**4.** Δx = 25; p₁ = −Δx = −25; q₁ = x₁ − x_min = 5 − 10 = −5; r₁ = q/p = 0.2.
**5.** The line is parallel to that boundary and lies outside it, so it is rejected.
**6.** It decides acceptance from parameters and computes at most two intersections, instead of repeated cut-and-recode steps.
**7.** in→in (output n); in→out (output intersection); out→out (nothing); out→in (output intersection and n).
**8.** The algorithm outputs one vertex list, so separate pieces are joined by extra boundary edges.
**9.** Four: left, right, bottom, top.
**10.** Large scenes with a small window, where nearly all objects lie wholly outside.
:::

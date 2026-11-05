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

## 4.5 Seeing the ideas: region codes, parameters and polygon clipping

Clipping is arithmetic on rectangles and lines, so the useful pictures are diagrams with real numbers. All three figures use one window, x from 20 to 100 and y from 20 to 80, and the same line from A(10, 30) to B(110, 70). No photograph is used in this unit because the topic is pure geometry.

```svgfig label="4.1" caption="Cohen-Sutherland region codes (bits TOP, BOTTOM, RIGHT, LEFT) around the window x 20-100, y 20-80. The line A(10,30) to B(110,70) has codes 0001 and 0010: neither is 0000 and the AND is 0000, so it is neither trivially accepted nor rejected. Clipping at x = 20 gives (20, 34) and at x = 100 gives (100, 66)."
f = Fig(580, 214)
X = lambda v: 60 + v * 3.2; Y = lambda v: 200 - v * 2.3
cols = [20, 100]; rows = [20, 80]
xs = [0, 20, 100, 120]; ys = [0, 20, 80, 100]
codes = {(0, 2): "1001", (1, 2): "1000", (2, 2): "1010", (0, 1): "0001", (1, 1): "0000", (2, 1): "0010", (0, 0): "0101", (1, 0): "0100", (2, 0): "0110"}
for (i, j), c in codes.items():
    x0, x1 = xs[i], xs[i + 1]; y0, y1 = ys[j], ys[j + 1]
    f.box(X(x0), Y(y1), X(x1) - X(x0), Y(y0) - Y(y1), c, fill=MINT if c == "0000" else "#f8fafc", stroke="#94a3b8", size=11, bold=True, r=0, sw=1)
f.box(X(20), Y(80), X(100) - X(20), Y(20) - Y(80), "", fill="none", stroke=TEAL, r=0, sw=2.6)
f.line(X(10), Y(30), X(110), Y(70), color=RED, sw=1.4, dash=True)
f.line(X(20), Y(34), X(100), Y(66), color=RED, sw=3)
f.circle(X(10), Y(30), 4, fill=RED, stroke=RED); f.circle(X(110), Y(70), 4, fill=RED, stroke=RED)
f.text(X(10) - 8, Y(30) + 14, "A 0001", size=9.6, color=RED, bold=True); f.text(X(110) + 4, Y(70) - 8, "B 0010", size=9.6, color=RED, bold=True)
f.box(452, 20, 124, 170, "Trivial tests\naccept: both\ncodes 0000\nreject: AND of\ncodes not 0000\nelse: clip at an\nedge, repeat\n\nA: left edge\n-> (20, 34)\nB: right edge\n-> (100, 66)", fill=SAND, stroke=AMBER, size=9.6, bold=True)
```

```svgfig label="4.2" caption="Liang-Barsky for the same line. The parameter u runs from 0 at A to 1 at B. Entering the window at the left edge at u = 0.1 and leaving at the right edge at u = 0.9; the bottom and top edges give -0.25 and 1.25, outside [0, 1], so they do not limit the line. The visible part is u = 0.1 to 0.9: (20, 34) to (100, 66)."
f = Fig(580, 176)
U = lambda u: 40 + u * 500
f.line(U(0), 70, U(1), 70, color=SLATE, sw=1.4)
f.box(U(0.1), 56, U(0.9) - U(0.1), 28, "", fill=MINT, stroke=TEAL, sw=2)
for u, lab, col in [(0, "u = 0  A", SLATE), (0.1, "u1 = 0.1", TEAL), (0.9, "u2 = 0.9", TEAL), (1, "u = 1  B", SLATE)]:
    f.circle(U(u), 70, 4, fill=col, stroke=col); f.text(U(u), 100 if u in (0, 1) else 46, lab, size=10, color=col, bold=True)
f.text(U(0.0), 122, "-0.25 (bottom, entering)", size=9.4, color=AMBER, bold=True, anchor="start")
f.text(U(1.0), 122, "1.25 (top, leaving)", size=9.4, color=AMBER, bold=True, anchor="end")
f.box(40, 136, 500, 34, "p = [-100, 100, -40, 40],  q = [-10, 90, 10, 50]:  u1 = max(0, 0.1, -0.25) = 0.1,  u2 = min(1, 0.9, 1.25) = 0.9", fill="#f8fafc", stroke=SLATE, size=10, bold=True)
```

```svgfig label="4.3" caption="Sutherland-Hodgman polygon clipping against the window x 20-100, y 20-80. The quadrilateral (10,40), (60,10), (110,50), (60,90) (left, dashed) has all four corners outside the window or on its edge; clipping against the four edges in turn gives an eight-sided polygon with vertices (50,80), (20,50), (20,34), (43.33,20), (72.5,20), (100,42), (100,58), (72.5,80) (right, filled)."
f = Fig(580, 214)
def pan(ox, poly, fill, st, dash, title):
    X = lambda v: ox + 20 + v * 2.2; Y = lambda v: 198 - v * 2.0
    f.box(X(20), Y(80), X(100) - X(20), Y(20) - Y(80), "", fill="#f8fafc", stroke=TEAL, r=0, sw=2)
    pts = [(X(x), Y(y)) for x, y in poly]
    if dash:
        f.arrow(pts + [pts[0]], color=st, sw=1.8, dash=True)
    else:
        f.poly(pts, fill=fill, stroke=st, sw=2.2)
    f.text(X(60), 208, title, size=10, color=st, bold=True)
pan(6, [(10, 40), (60, 10), (110, 50), (60, 90)], "none", SLATE, True, "input polygon (4 vertices)")
pan(296, [(50, 80), (20, 50), (20, 34), (43.33, 20), (72.5, 20), (100, 42), (100, 58), (72.5, 80)], MINT, TEAL, False, "clipped polygon (8 vertices)")
```

### 4.5.1 Eight uses of clipping in graphics systems

1. **Showing only the visible part of a scene.** A game or map draws only what lies inside the screen. Everything else is discarded early, so no time is wasted on it. This keeps the frame rate high.
2. **Zooming and panning in maps.** When a user zooms into Kathmandu, roads outside the window must not be drawn on the rest of the page. Clipping cuts each road at the edge of the map view. Map apps such as Pathao do this for every frame.
3. **Windowed user interfaces.** A window on a desktop clips its contents to its own rectangle so text does not spill onto neighbouring windows. Overlapping windows depend on correct clipping. Scrolling a list also relies on it.
4. **Printing and exporting.** A drawing larger than the paper is clipped to the page area. Only the part inside the printable region is sent. This avoids wasted ink and errors.
5. **Speeding up the pipeline.** Triangles wholly outside the view are rejected before shading, saving the most expensive work. GPUs clip in hardware and use trivial reject tests of the Cohen-Sutherland type. Early rejection is the cheapest optimisation.
6. **Windows into CAD models.** An engineer inspecting one bay of a building plan shows only that region. Clipping lets the screen show a detail without redrawing the whole model. Large drawings stay responsive.
7. **Cutting parts of images.** Cropping a photo to a rectangle is clipping; a mask in the shape of a polygon uses polygon clipping. Photo editors and ID-card makers use this for passport-size pictures.
8. **Collision and selection tests.** Selecting objects with a rubber-band rectangle is a clipping test of each object against the rectangle. The same rejection codes decide quickly which objects are inside. Touch interfaces use this idea.

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


## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the Cohen-Sutherland line clipping algorithm. Clip the line A(10, 30) to B(110, 70) against the window x 20-100, y 20-80.**

*Introduction.* The algorithm gives each end point a 4-bit region code and uses the codes to accept, reject or clip a line quickly (section 4.2, Figure 4.1).

1. **Region codes.** Bits are TOP (y > ymax), BOTTOM (y < ymin), RIGHT (x > xmax) and LEFT (x < xmin); a point inside has code 0000.
2. **Trivial accept.** If both codes are 0000, draw the whole line.
3. **Trivial reject.** If the bitwise AND of the codes is not 0000, both ends lie on the same outside side; discard the line.
4. **Clip.** Otherwise pick an end point outside, intersect the line with the window edge indicated by a set bit, replace the end point and repeat.

*Worked example.* The slope is (70 - 30) / (110 - 10) = 0.4. Code of A: x = 10 < 20, so LEFT: **0001**. Code of B: x = 110 > 100, so RIGHT: **0010**. Neither is 0000 and the AND is 0000, so clip. A against x = 20: y = 30 + 0.4 x 10 = **34**, point (20, 34), code 0000. B against x = 100: y = 30 + 0.4 x 90 = **66**, point (100, 66), code 0000. Both codes are now 0000, so draw the line from (20, 34) to (100, 66).

| Step | Point | Code |
|---|---|---|
| Start A | (10, 30) | 0001 |
| Start B | (110, 70) | 0010 |
| Clip A at left | (20, 34) | 0000 |
| Clip B at right | (100, 66) | 0000 |

*Conclusion.* Region codes make the common accept and reject cases very cheap; only lines that cross the window need arithmetic.

**Q2 (5 marks). Use the Liang-Barsky algorithm to clip the same line. Show the p and q values and the parameters.**

*Introduction.* Liang-Barsky writes the line as x = x1 + u dx, y = y1 + u dy with 0 <= u <= 1 and clips against each edge using four inequalities u p_k <= q_k (section 4.3, Figure 4.2).

*Values.* dx = 100 and dy = 40. For left, right, bottom and top: p = [-dx, dx, -dy, dy] = [-100, 100, -40, 40] and q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1] = [-10, 90, 10, 50].

*Parameters.* If p < 0 the line enters across that edge at u = q / p; if p > 0 it leaves at u = q / p.

| Edge | p | q | q / p | Role |
|---|---|---|---|---|
| Left | -100 | -10 | 0.10 | enter |
| Right | 100 | 90 | 0.90 | leave |
| Bottom | -40 | 10 | -0.25 | enter |
| Top | 40 | 50 | 1.25 | leave |

u1 = max(0, 0.10, -0.25) = **0.1**; u2 = min(1, 0.90, 1.25) = **0.9**. Since u1 < u2 the line is visible. New end points: u = 0.1 gives (10 + 10, 30 + 4) = **(20, 34)**; u = 0.9 gives (10 + 90, 30 + 36) = **(100, 66)**, the same result as Cohen-Sutherland.

*Conclusion.* Liang-Barsky needs only four divisions and no repeated intersections, so it is faster than Cohen-Sutherland for lines that need clipping.

**Q3 (10 marks). Explain Sutherland-Hodgman polygon clipping with the four cases. Clip the polygon (10, 40), (60, 10), (110, 50), (60, 90) against the window x 20-100, y 20-80.**

*Introduction.* Clipping a polygon is not the same as clipping its edges one by one, because the result must again be a closed polygon. Sutherland-Hodgman clips the whole polygon against one window edge at a time and passes the result to the next edge (section 4.4, Figure 4.3).

*The four cases.* For each polygon edge from vertex a to vertex b, relative to one clipping edge:
1. both inside: output b;
2. a inside, b outside: output the intersection;
3. both outside: output nothing;
4. a outside, b inside: output the intersection and then b.

*Procedure.* Clip against left, right, bottom and top in turn; the output list of one edge is the input of the next. Intersections use the line equation; the inside test is a comparison with the edge.

*Worked example.* The window is x 20-100, y 20-80.

| Clip edge | Output vertices | Count |
|---|---|---|
| left x = 20 | (20, 50), (20, 34), (60, 10), (110, 50), (60, 90) | 5 |
| right x = 100 | (20, 50), (20, 34), (60, 10), (100, 42), (100, 58), (60, 90) | 6 |
| bottom y = 20 | (20, 50), (20, 34), (43.33, 20), (72.5, 20), (100, 42), (100, 58), (60, 90) | 7 |
| top y = 80 | (50, 80), (20, 50), (20, 34), (43.33, 20), (72.5, 20), (100, 42), (100, 58), (72.5, 80) | 8 |

The final polygon has eight vertices: **(50, 80), (20, 50), (20, 34), (43.33, 20), (72.5, 20), (100, 42), (100, 58), (72.5, 80)**. Every vertex lies on or inside the window, and the four clipped corners of the original have been replaced by edges along the window boundary.

*Limitation.* For a concave polygon the algorithm can produce extra edges along the window boundary joining separate pieces; these show as degenerate lines and are removed or avoided by other algorithms such as Weiler-Atherton.

| Algorithm | Clips | Idea |
|---|---|---|
| Cohen-Sutherland | Lines | Region codes |
| Liang-Barsky | Lines | Parametric inequalities |
| Sutherland-Hodgman | Polygons | One edge at a time |

*Conclusion.* Polygon clipping is performed edge by edge, so the vertex count can change (here from 4 to 8); the result is a closed polygon inside the window.

---
subject: Applied Economics
grade: BCA Semester 3
unit: 4
title: Cost and Revenue Curves
hours: 6
area: BCA 206 · Applied Economics · Unit 4
---

A firm's decisions depend on what it **costs** to produce and what it **earns**. This unit builds the cost and revenue curves that Unit 5 uses to find the profit-maximising output in each market structure.

::: key What this unit gives you
- Concepts of cost: actual, opportunity, implicit, explicit, accounting and economic.
- Short-run and long-run cost curves (total, average, marginal) and their relations.
- Revenue under perfect and imperfect competition and the AR–MR relation; a worked table.
:::

## 4.1 Concepts of cost

| Concept | Meaning |
|---|---|
| **Actual (money) cost** | the money actually spent on inputs |
| **Opportunity cost** | the value of the best alternative use of a resource |
| **Explicit cost** | payments to outsiders (wages, rent, raw materials, electricity) |
| **Implicit cost** | the opportunity cost of the owner's own resources (own capital, own time, own building) |
| **Accounting cost** | explicit costs only |
| **Economic cost** | explicit + implicit costs (including **normal profit**) |

Accounting profit = revenue − explicit costs; **economic profit** = revenue − (explicit + implicit costs). A shop-owner earning NPR 500,000 revenue with NPR 350,000 explicit costs has accounting profit 150,000; if she could have earned a 100,000 salary elsewhere and her capital could earn 30,000, economic profit is 150,000 − 130,000 = **20,000**. Zero economic profit means normal profit: the owner just covers all opportunity costs and stays in business.

## 4.2 Short-run cost curves

In the **short run** at least one input (plant, machinery) is **fixed**; in the **long run** all are variable. Costs: **Total fixed cost (TFC)** does not change with output (rent, interest); **total variable cost (TVC)** rises with output (materials, wages); **TC = TFC + TVC**. Per unit: **AFC = TFC/Q** (falls continuously, a rectangular hyperbola), **AVC = TVC/Q**, **AC (ATC) = TC/Q = AFC + AVC**, and **marginal cost MC = ΔTC/ΔQ = ΔTVC/ΔQ**, the extra cost of one more unit.

The shapes follow the **law of variable proportions** (diminishing returns): at first extra workers raise output a lot (MC falls), then crowding sets in (MC rises). So **AVC, AC and MC are U-shaped**, and **MC cuts AVC and AC at their minimum points** (marginal below average pulls the average down; above, pulls it up).

::: example Worked example: a cost schedule (TFC = 100)
| Q | TVC | TC | MC | AFC | AVC | AC |
|---|---|---|---|---|---|---|
| 0 | 0 | 100 | | | | |
| 1 | 50 | 150 | 50 | 100.0 | 50 | 150.0 |
| 2 | 90 | 190 | 40 | 50.0 | 45 | 95.0 |
| 3 | 120 | 220 | 30 | 33.3 | 40 | 73.3 |
| 4 | 160 | 260 | 40 | 25.0 | 40 | 65.0 |
| 5 | 220 | 320 | 60 | 20.0 | 44 | 64.0 |
| 6 | 300 | 400 | 80 | 16.7 | 50 | 66.7 |

MC falls to 30 at Q = 3 then rises. AVC is minimum (40) at Q = 3–4 where MC = 40 crosses it; AC is minimum (64) at Q = 5, where MC (60 → 80) crosses it. AFC falls throughout, which is why AC and AVC converge as output rises.
:::

## 4.3 Long-run cost curves

In the long run the firm can choose any plant size. The **long-run average cost (LAC)** curve is the **envelope** of the short-run AC curves (SAC₁, SAC₂, SAC₃ …): for each output it shows the lowest achievable average cost when the plant can be chosen. It is also **U-shaped**, but flatter, for reasons of **scale**: **economies of scale** (specialisation, bulk buying, spreading overhead, better technology) make LAC fall; at the **minimum efficient scale** it is flat (constant returns); **diseconomies of scale** (management and coordination problems) make it rise. **Long-run marginal cost (LMC)** cuts LAC at its minimum. At the minimum of LAC the firm's plant is operated at the minimum of its SAC (the optimal scale), and **SMC = LMC**; on the falling part of LAC the SAC touches it to the left of SAC's own minimum, on the rising part to the right.

**Relationship:** SAC ≥ LAC everywhere, with equality only at the one output where the plant is optimal; LAC is the envelope; LMC is not an envelope but passes through the points where SMC = LMC.

## 4.4 Concept of revenue

**Total revenue TR = P × Q**; **average revenue AR = TR/Q = P** (so the AR curve is the demand curve); **marginal revenue MR = ΔTR/ΔQ**, the extra revenue from one more unit.

**Perfect competition:** the firm is a **price-taker**; each extra unit sells at the market price, so **AR = MR = P**: a **horizontal** line; TR is a straight line from the origin.

**Imperfect competition (monopoly, monopolistic competition, oligopoly):** the firm faces a downward-sloping demand curve (it must cut price to sell more), so **MR < AR** and MR lies below AR. TR rises, reaches a maximum where **MR = 0** (the elasticity = 1 point), then falls. For a linear demand AR = a − bQ: TR = aQ − bQ², **MR = a − 2bQ**, i.e. MR has the same intercept as AR and **twice the slope**, cutting the quantity axis at half the distance.

**AR–MR–elasticity relation: MR = AR × (1 − 1/|e|)** (so MR > 0 when demand is elastic, MR = 0 when |e| = 1, MR < 0 when inelastic: a monopolist never operates on the inelastic part).

::: example Worked example: revenue with AR = 100 − Q
TR = 100Q − Q²; MR = 100 − 2Q. At Q = 20: P = 80, TR = 1,600, MR = 60. At Q = 30: P = 70, TR = 2,100, MR = 40; check via elasticity: |e| = (1) × 70/30 = 2.33, MR = 70 × (1 − 1/2.33) = **40** ✓. TR is maximum at Q = 50 (MR = 0, P = 50, TR = 2,500), where |e| = 50/50 = 1.
**Perfect competition at P = 60:** AR = MR = 60 for every Q; TR(5) = 300.
:::

**Excel exercise:** build the schedule in columns Q, TVC, then `=TVC+100` for TC, `=C3-C2` for MC, `=C3/A3` for AC; chart AC and MC on one graph to see MC cut AC at its minimum, and `=P*Q`, `=TR3-TR2` for revenue.

## 4.5 Seeing costs and revenues: schedules, the long-run envelope and the MR line

```svgfig label="4.1" caption="The cost schedule with TFC = 100. (a) Total costs: TFC is flat, TVC rises, TC = TFC + TVC lies 100 above TVC. (b) Unit costs: AFC falls throughout; AVC and AC are U-shaped; MC cuts AVC at its minimum (Q = 3 to 4, 40) and AC at its minimum (Q = 5, 64)."
f = Fig(580, 262)
a = Axes(f, 42, 14, 225, 190, (0, 6.5), (0, 420))
a.grid(1, 100).axes("Output Q", "Total cost")
def line(ax, xs, ys, col, dash=False):
    p = " ".join(f"{ax.X(x)},{ax.Y(y)}" for x, y in zip(xs, ys))
    f.raw(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="2.3" stroke-linejoin="round"{" stroke-dasharray=\"6 4\"" if dash else ""}/>')
    for x, y in zip(xs, ys): ax.pt(x, y, "", r=2.6, color=col)
Q = [0, 1, 2, 3, 4, 5, 6]
line(a, Q, [100] * 7, SLATE, True); line(a, Q, [0, 50, 90, 120, 160, 220, 300], AMBER); line(a, Q, [100, 150, 190, 220, 260, 320, 400], NAVY)
a.tag(5.4, 372, "TC", size=11, color=NAVY, bold=True); a.tag(5.3, 262, "TVC", size=11, color=AMBER, bold=True); a.tag(5.6, 118, "TFC", size=11, color=SLATE, bold=True)
b = Axes(f, 335, 14, 225, 190, (0, 6.5), (0, 160))
b.grid(1, 40).axes("Output Q", "Cost per unit")
Q1 = [1, 2, 3, 4, 5, 6]
line(b, Q1, [100, 50, 33.3, 25, 20, 16.7], SLATE, True); line(b, Q1, [50, 45, 40, 40, 44, 50], TEAL); line(b, Q1, [150, 95, 73.3, 65, 64, 66.7], NAVY); line(b, Q1, [50, 40, 30, 40, 60, 80], RED)
b.tag(1.3, 148, "AC", size=11, color=NAVY, bold=True); b.tag(1.6, 108, "AFC", size=11, color=SLATE, bold=True); b.tag(6.1, 86, "MC", size=11, color=RED, bold=True); b.tag(6.2, 38, "AVC", size=11, color=TEAL, bold=True)
b.pt(5, 64, "min AC = 64", dx=-6, dy=-16, anchor="middle", color=NAVY)
f.text(155, 250, "(a) total cost curves", size=11, color=SLATE, italic=True); f.text(448, 250, "(b) unit cost curves", size=11, color=SLATE, italic=True)
```

```svgfig label="4.2" caption="Long-run average cost as the envelope of short-run average cost curves. Each thin curve is the SAC of one plant size and touches the thick LAC at a single output. LAC falls through economies of scale, is flat near the minimum efficient scale, and rises through diseconomies of scale."
f = Fig(580, 250)
a = Axes(f, 50, 14, 360, 190, (0, 90), (0, 110))
a.grid(15, 20).axes("Output", "Cost per unit")
lac = lambda q: 50 + 0.012 * (q - 45) ** 2
for m in [8, 22, 38, 55, 70, 84]:
    s = 0.024 * (m - 45)
    a.curve(lambda q, m=m, s=s: lac(m) + s * (q - m) + 0.03 * (q - m) ** 2, max(m - 22, 0), min(m + 22, 90), color=TEAL, sw=1.3)
a.curve(lac, 0, 90, color=NAVY, sw=3)
a.tag(78, 86, "LAC", size=12, color=NAVY, bold=True); a.tag(7, 36, "SAC", size=10.5, color=TEAL, bold=True)
a.vline(45, 0, 50, color=AMBER); a.pt(45, 50, "minimum efficient scale", dx=10, dy=34, anchor="start")
f.box(430, 30, 140, 44, "Economies of scale:\nLAC falls", fill=MINT, stroke=TEAL, size=10.5)
f.box(430, 88, 140, 44, "Constant returns:\nLAC flat", fill=SAND, stroke=AMBER, size=10.5)
f.box(430, 146, 140, 44, "Diseconomies:\nLAC rises", fill=ROSE, stroke=RED, size=10.5)
```

```svgfig label="4.3" caption="Revenue curves. (a) A price-taking firm has AR = MR = P, a horizontal line. (b) With AR = 60 − Q the firm has MR = 60 − 2Q, below AR and cutting the axis at half the distance. (c) TR = 60Q − Q² peaks at Q = 30 (TR = 900), exactly where MR = 0."
f = Fig(580, 240)
a = Axes(f, 36, 14, 150, 160, (0, 60), (0, 70)); a.grid(20, 20).axes("Q", "P")
a.hline(40, 0, 60, color=NAVY, dash=False, sw=2.4); a.tag(50, 46, "AR = MR = P", size=10, color=NAVY, bold=True)
b = Axes(f, 226, 14, 150, 160, (0, 65), (-10, 70)); b.grid(20, 20).axes("Q", "P")
b.curve(lambda q: 60 - q, 0, 60, color=NAVY); b.curve(lambda q: 60 - 2 * q, 0, 35, color=RED)
b.tag(52, 12, "AR", size=11, color=NAVY, bold=True); b.tag(42, -4, "MR", size=11, color=RED, bold=True); b.vline(30, -10, 0, color=AMBER)
c = Axes(f, 416, 14, 150, 160, (0, 65), (0, 1000)); c.grid(20, 250).axes("Q", "TR")
c.curve(lambda q: 60 * q - q * q, 0, 60, color=TEAL); c.vline(30, 0, 900, color=AMBER); c.pt(30, 900, "TR max 900", dx=-6, dy=-8, anchor="middle")
f.text(111, 214, "(a) perfect competition", size=10.5, color=SLATE, italic=True); f.text(301, 214, "(b) AR and MR", size=10.5, color=SLATE, italic=True); f.text(491, 214, "(c) total revenue", size=10.5, color=SLATE, italic=True)
```

```photogrid label="4.1" cols="2" ratio="1.1" caption="Economies of scale: spreading fixed cost. (a) The Ford assembly line at Trafford Park, Manchester, 1923. Ford's moving assembly line, introduced in 1913-1914, cut the time to assemble a chassis from about 12 hours 8 minutes to 1 hour 33 minutes, roughly 7.8 times faster, which let Ford lower his price. (b) A small illustrative workshop with fixed cost Rs 2,000,000 a month and variable cost Rs 20,000 a unit has average cost AC = 2,000,000 / Q + 20,000. At 10 units AC is Rs 220,000; at 50 units 60,000; at 100 units 40,000; at 500 units 24,000; at 1,000 units 22,000. Average cost can never fall below the variable cost of Rs 20,000, but it falls steeply at first because each extra unit shares the fixed cost with more units. This is why large producers such as cement plants and telecom companies can sell cheaper per unit."
@ photo id="bcaeco/fordline" cap="Ford assembly line, Manchester, 1923"
fit 1.1
focus 0.5 0.5
@ svg cap="Average cost against output, in thousand rupees"
F_, v = 2000000, 20000
Q = [10, 50, 100, 500, 1000]
ac = [F_ / q + v for q in Q]
assert ac == [220000, 60000, 40000, 24000, 22000] and round(728 / 93, 1) == 7.8
f = Fig(300, 240)
f.text(150, 14, "AC = 2,000,000 / Q + 20,000", size=10.5, color=NAVY, bold=True)
base, sc = 170, 120 / 220000
for i, (q, a) in enumerate(zip(Q, ac)):
    x = 18 + i * 54; h = a * sc
    f.box(x, base - h, 40, h, "", fill=BLUE if i < 4 else TEAL, stroke=NAVY, r=0, sw=1)
    f.text(x + 20, base - h - 8, f"{int(a) // 1000}k", size=10.5, color=NAVY, bold=True)
    f.text(x + 20, base + 14, str(q), size=10.5, color=SLATE)
f.line(10, base, 292, base, color=SLATE, sw=1.2)
f.line(10, base - v * sc, 292, base - v * sc, color=RED, sw=1.4, dash=True)
f.text(150, base + 32, "units per month (Q); dashed = floor 20k", size=10.5, color=SLATE)
f.text(150, 228, "10 units -> 1,000 units: AC falls 10 times", size=10.5, color=TEAL, bold=True)
```

```photogrid label="4.2" cols="2" ratio="1.1" caption="Break-even at a tea stall. (a) A street tea-and-snack stall. (b) Illustrative daily figures: fixed cost Rs 1,500 (rent, licence, one helper), variable cost Rs 12 a cup, price Rs 25 a cup, so AR = MR = 25 for this price-taking seller. Total revenue is TR = 25Q and total cost TC = 1,500 + 12Q. Break-even is where they meet: Q = 1,500 / (25 - 12) = 115.4, so the stall must sell 116 cups to avoid a loss. At 100 cups the stall loses 13 x 100 - 1,500 = Rs 200; at 200 cups it earns Rs 1,100. Each cup beyond break-even adds the contribution of Rs 13, and the margin of safety at 200 cups is (200 - 115.4) / 200 = 42 per cent."
@ photo id="bcaeco/stall" cap="Tea and sel roti, a street stall"
fit 1.1
focus 0.5 0.5
@ svg cap="TR and TC lines, break-even at 116 cups"
P_, V_, F_ = 25, 12, 1500
be = F_ / (P_ - V_)
assert round(be, 1) == 115.4 and -200 == (P_ - V_) * 100 - F_ and (P_ - V_) * 200 - F_ == 1100
assert round((200 - be) / 200 * 100) == 42
f = Fig(300, 240)
ax = Axes(f, 52, 42, 232, 134, (0, 250), (0, 6000))
ax.grid(50, 1000, size=10.5).axes("cups per day (Q)", "rupees")
ax.curve(lambda q: P_ * q, 0, 240, color=TEAL, label="TR", lx=ax.X(214), ly=ax.Y(5900))
ax.curve(lambda q: F_ + V_ * q, 0, 250, color=RED, label="TC", lx=ax.X(236), ly=ax.Y(4000))
ax.hline(F_, 0, 40, color=AMBER)
ax.pt(be, P_ * be, "break-even", color=NAVY, dx=8, dy=14)
ax.vline(be, 0, P_ * be, color=NAVY)
f.text(150, 14, "TR = 25Q   TC = 1,500 + 12Q", size=10.5, color=NAVY, bold=True)
f.text(150, 206, "break-even 115.4 -> 116 cups a day", size=10.5, color=NAVY, bold=True)
f.text(150, 226, "100 cups: -Rs 200;  200 cups: +Rs 1,100", size=10.5, color=TEAL, bold=True)
```

## 4.6 The production behind the cost curves: returns to scale and cost minimisation

The cost curves of sections 4.1 to 4.3 come from **how inputs turn into output**. This section links the two with a worked production function.

### Short run: diminishing returns make MC rise

In the short run at least one input is fixed. Suppose a workshop has **K = 100** machines (fixed) and hires labour L, with output Q = √(K × L) = 10√L. Labour costs w = Rs 100 per unit and each machine costs r = Rs 400.

::: example Worked example: from production to cost
Output needs L = Q²/100 units of labour (square both sides of Q = 10√L).
**Fixed cost** = 400 × 100 = **40,000**. **Variable cost** = 100 × L = 100 × Q²/100 = **Q²**. So **TC = 40,000 + Q²**.
**MC** = 2Q (rising), **AVC** = Q, **AFC** = 40,000/Q, **AC** = Q + 40,000/Q.
**Minimum AC:** set AC = MC: Q + 40,000/Q = 2Q gives Q² = 40,000, so **Q = 200** and AC = **400**. This is the bottom of the U that section 4.2 describes, and MC cuts AC there.
Why MC rises: the **marginal product of labour** MPL = dQ/dL = 5/√L falls as more labour is added to the same machines (diminishing returns), and MC = w / MPL. A smaller MPL means a larger MC.
:::

### Long run: isoquant, isocost and the cheapest input mix

In the long run both inputs vary. An **isoquant** joins all combinations of labour and capital that give the same output. Its slope is the **marginal rate of technical substitution (MRTS = MPL / MPK)**. An **isocost line** joins all combinations that cost the same total: wL + rK = C, with slope −w/r. The cost-minimising mix is where an isocost line **just touches** the isoquant, so **MRTS = w / r**, or equivalently **MPL / w = MPK / r**: the last rupee spent on each input gives the same extra output (the producer's version of the equal-marginal-utility rule in section 3.1).

::: example Worked example: the cheapest way to make 100 units
Q = √(KL) = 100 means KL = 10,000. With w = 100 and r = 400, the isocost line is 100L + 400K = C.
MPL = ½√(K/L), MPK = ½√(L/K), so MRTS = K/L. Setting K/L = w/r = 100/400 = 0.25 gives **L = 4K**.
Then KL = 4K² = 10,000, so **K = 50, L = 200**, and the minimum cost is 100 × 200 + 400 × 50 = **Rs 40,000**, so AC = 400.
**Link to the short run:** with the plant fixed at K = 100 the firm would use L = 100 hours for Q = 100 and pay 50,000, which is more. The plant of 100 machines is the cheapest one only for Q = 200 (there K = 100, L = 400, cost 80,000 on both counts), which is why the short-run AC bottom (Q = 200, AC = 400) touches the long-run curve at that output. Because this function has constant returns to scale, LAC = 400 at every output.
**If wages rise to 200:** K/L = 0.5, so L = 2K and 2K² = 10,000, K = 70.7, L = 141.4, cost = 200 × 141.4 + 400 × 70.7 = **Rs 56,569**. The firm substitutes machines for labour.
:::

```svgfig label="4.4" caption="Cost minimisation for Q = 100 with w = 100, r = 400. The curve is the isoquant KL = 10,000. The isocost line for Rs 40,000 touches it at L = 200, K = 50 (the cheapest mix). Rs 30,000 cannot reach the isoquant; Rs 50,000 cuts it twice, so some cheaper mix exists."
f = Fig(580, 262)
a = Axes(f, 48, 14, 300, 200, (0, 400), (0, 120))
a.grid(100, 20).axes("Labour L", "Capital K")
a.curve(lambda L: 10000 / L if L > 0 else 999, 80, 400, color=NAVY, sw=2.6, label="Q = 100", lx=a.X(300), ly=a.Y(46))
a.curve(lambda L: 75 - L / 4, 0, 300, color=SLATE, dash=True, label="30,000", lx=a.X(20), ly=a.Y(66))
a.curve(lambda L: 100 - L / 4, 0, 400, color=RED, sw=2.4, label="40,000", lx=a.X(40), ly=a.Y(94))
a.curve(lambda L: 125 - L / 4, 0, 400, color=SLATE, dash=True, label="50,000", lx=a.X(60), ly=a.Y(116))
a.hline(50, 0, 200, color=AMBER); a.vline(200, 0, 50, color=AMBER)
a.pt(200, 50, "", r=5, color=RED)
f.box(372, 24, 198, 56, "Tangency: MRTS = w/r\nK/L = 100/400 = 0.25", fill=BLUE, stroke=NAVY, size=10.5)
f.box(372, 94, 198, 56, "L = 200, K = 50\ncost = 20,000 + 20,000", fill=MINT, stroke=TEAL, size=10.5)
f.box(372, 164, 198, 56, "Wage to 200: L = 141,\nK = 71, cost 56,569", fill=SAND, stroke=AMBER, size=10.5)
```

### Returns to scale

**Returns to scale** ask what happens to output when **all** inputs are multiplied by the same factor. This is the long-run basis of the LAC curve in section 4.3.

| Production function | Double K and L → output × | Type | LAC |
|---|---|---|---|
| Q = K^0.6 L^0.6 | 2^1.2 = 2.30 | increasing returns | falls |
| Q = K^0.5 L^0.5 | 2^1.0 = 2.00 | constant returns | flat |
| Q = K^0.4 L^0.4 | 2^0.8 = 1.74 | decreasing returns | rises |

Increasing returns arise from specialisation, bulk buying and spreading of overhead (software has an extreme case: the second copy costs almost nothing). Decreasing returns appear when coordination becomes hard. **Do not confuse** returns to scale (all inputs change, long run) with **diminishing marginal returns** (one input changes, short run): a production function can have constant returns to scale and still show diminishing returns to labour.

**Practice:** (i) For Q = √(KL) with w = 50 and r = 200, find the cheapest way to produce 400 units. (ii) What does MRTS > w/r tell the firm to do?

## 4.7 Eight uses of cost and revenue analysis

1. **Deciding the price of a product.** A firm must cover its average cost, so it never sells below the minimum of the AC curve for long. A Kathmandu printing press adds a margin to the unit cost of each job. Without knowing the cost curve the price would be a guess.
2. **Choosing how much to produce.** Output should rise as long as marginal revenue is above marginal cost. A bakery in Pokhara bakes extra batches only while the extra income covers the extra flour, gas and labour. This simple rule is the base of all profit decisions.
3. **Deciding to shut down or to continue.** In the short run fixed costs are sunk, so a firm keeps working if the price covers AVC even when it loses on AC. A hotel in the off-season may stay open on these grounds. If price falls below AVC, closing is the better choice.
4. **Planning plant size and expansion.** The long-run cost curve shows which factory size gives the lowest unit cost. A cement plant in Hetauda gains from economies of scale, while a very large unit may suffer from poor management. Banks study these curves before lending for expansion.
5. **Understanding economies of scale in technology.** Software has a high fixed cost to build and almost zero marginal cost per user. The average cost per user therefore falls steadily as the user base grows. This is why apps such as eSewa and Foodmandu fight to gain users quickly.
6. **Separating accounting and economic profit.** An owner who counts only cash costs may feel rich while earning less than a salary elsewhere. Economic profit includes the opportunity cost of own time and capital. A small shopkeeper uses it to decide whether the shop is worth running.
7. **Understanding pricing power.** A firm with a falling AR curve knows that MR is lower than price, so each extra unit sold earns less than the price shown. This is the basis of limited output and higher prices in monopolies. It also explains discounts that are offered only to some groups.
8. **Controlling and budgeting costs.** Splitting costs into fixed and variable lets a manager forecast the bill at any output. A college planning more students knows that rent stays the same but staff and electricity rise. Break-even analysis follows directly from TC and TR.

## Formula and fact sheet

- TC = TFC + TVC; AFC = TFC/Q; AVC = TVC/Q; AC = AFC + AVC; MC = ΔTC/ΔQ.
- MC cuts AVC and AC at their minima; AFC always falls.
- LAC is the envelope of SAC; economies then diseconomies of scale.
- TR = PQ; AR = P; MR = ΔTR/ΔQ. Perfect competition: AR = MR = P. Otherwise MR < AR; linear: MR has twice the slope.
- MR = AR(1 − 1/|e|); TR maximum where MR = 0.
- Production: MC = w/MPL; cost minimum where MRTS = w/r; returns to scale: all inputs × λ → output × λᵏ (k > 1 increasing, k = 1 constant, k < 1 decreasing).

## Chapter summary

- Economic cost includes implicit costs, so economic profit is lower than accounting profit; normal profit is a cost.
- Short-run cost curves are U-shaped because of diminishing returns; long-run curves are envelopes shaped by scale economies.
- Revenue curves are horizontal under perfect competition and downward-sloping with MR below AR otherwise.

## Practice

1. Differentiate explicit and implicit, accounting and economic cost.
2. Given TFC = 60 and TVC = 20, 36, 48, 64, 90 for Q = 1–5, compute MC, AVC and AC.
3. Why does MC cut AC at its minimum?
4. Derive MR for AR = 60 − 2Q; at what output is TR maximum?
5. Explain the long-run average cost curve and economies of scale.
6. Why is MR below AR for a monopolist but equal to it in perfect competition?
7. A firm has revenue 800, explicit costs 500, and implicit costs 350. Find accounting and economic profit.
8. For Q = √(KL) with w = 50 and r = 200, find the cheapest way to produce 400 units.
9. What does MRTS > w/r tell a firm?

::: note Answers and worked solutions
**1.** Explicit: paid to outsiders. Implicit: opportunity cost of owner's resources. Accounting cost = explicit; economic cost = explicit + implicit.
**2.** TC = 80, 96, 108, 124, 150. MC = 20, 16, 12, 16, 26. AVC = 20, 18, 16, 16, 18. AC = 80, 48, 36, 31, 30.
**3.** If the marginal cost is below the average, adding that unit lowers the average; if above, it raises it; so MC crosses AC where AC stops falling, at its minimum.
**4.** TR = 60Q − 2Q²; MR = 60 − 4Q. TR is maximum where MR = 0: Q = **15** (P = 30, TR = 450).
**5.** LAC is the envelope of short-run AC curves: the lowest cost of each output when the plant size can be chosen. It falls with economies of scale, is flat at the minimum efficient scale and rises with diseconomies of scale.
**6.** To sell one more unit a monopolist must lower the price on **all** units, so the extra revenue is less than the price; a price-taker sells every unit at the same fixed price, so MR = P.
**7.** Accounting profit = 800 − 500 = **300**; economic profit = 800 − 850 = **−50** (a loss compared with the best alternative).
**8.** MRTS = K/L = w/r = 0.25 so L = 4K; KL = 4K² = 160,000 gives **K = 200, L = 800**; cost = 50 × 800 + 200 × 200 = **Rs 80,000**.
**9.** MPL/MPK exceeds w/r, so labour gives more extra output per rupee than capital: use more labour and less capital until MPL/w = MPK/r.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distinguish between explicit and implicit costs, and between accounting profit and economic profit, with a numerical example.**

*Introduction.* To a business owner a cost is more than the cash paid out. Economists count every resource at what it could have earned elsewhere, its **opportunity cost**.

*Explicit and implicit cost.*

| Point | Explicit cost | Implicit cost |
|---|---|---|
| Meaning | payments to outsiders for inputs | opportunity cost of the owner's own resources |
| Examples | wages, rent, raw material, electricity | own capital, own time, own building |
| Recorded in books | yes | no |
| Used in | accounting cost | economic cost (explicit + implicit) |

*Profit.* **Accounting profit** = revenue − explicit costs. **Economic profit** = revenue − (explicit + implicit costs). The implicit costs include **normal profit**, the minimum reward that keeps the owner in the business.

*Example.* A shop earns revenue NPR 500,000 and pays explicit costs of 350,000. Accounting profit is 150,000. The owner could earn a 100,000 salary elsewhere and her capital could earn 30,000, so implicit cost is 130,000. Economic profit = 150,000 − 130,000 = **20,000**. Zero economic profit would mean exactly normal profit.

*Conclusion.* A business that shows an accounting profit may still be a poor choice if the owner's best alternative pays more.

**Q2 (5 marks). Explain total, average and marginal revenue. Show how AR and MR are related in perfect competition and under imperfect competition.**

*Introduction.* **Total revenue** TR = P × Q is the money received from sales. **Average revenue** AR = TR/Q = P, so the AR curve is the demand curve. **Marginal revenue** MR = ΔTR/ΔQ is the extra revenue from selling one more unit (Figure 4.3).

*Perfect competition.* The firm is a **price-taker**. Every unit sells at the market price, so **AR = MR = P** and both are one horizontal line. TR is a straight line through the origin.

*Imperfect competition.* The firm faces a downward-sloping demand curve and must cut the price to sell more. Therefore **MR < AR**. For AR = a − bQ, TR = aQ − bQ² and **MR = a − 2bQ**: the same intercept and twice the slope, so MR cuts the quantity axis at half the distance.

*Numerical illustration.* For AR = 60 − Q, MR = 60 − 2Q. At Q = 20, AR = 40 but MR = 20. TR = 60Q − Q² rises until MR = 0 at Q = 30, where TR = 900, and falls after that. At that point elasticity is exactly 1.

*Conclusion.* The price taker sees MR equal to price; every other firm sees MR below price, which is the root of monopoly power.

**Q3 (10 marks). Explain the short-run cost curves and their relationships using a schedule. How is the long-run average cost curve derived, and why is it U-shaped?**

*Introduction.* In the **short run** some input, such as plant, is fixed; in the **long run** all inputs can change. Costs are therefore divided into fixed and variable parts.

*Cost concepts.* TFC does not change with output; TVC rises with output; **TC = TFC + TVC**. Per unit: AFC = TFC/Q, AVC = TVC/Q, **AC = AFC + AVC**, and **MC = ΔTC/ΔQ**.

*Schedule and curves (Figure 4.1), TFC = 100.*

| Q | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| TC | 150 | 190 | 220 | 260 | 320 | 400 |
| MC | 50 | 40 | 30 | 40 | 60 | 80 |
| AVC | 50 | 45 | 40 | 40 | 44 | 50 |
| AC | 150 | 95 | 73.3 | 65 | 64 | 66.7 |

*Relationships.*

1. **AFC** falls throughout (a rectangular hyperbola), so AC and AVC come closer as output grows.
2. **AVC, AC and MC are U-shaped** because of the law of variable proportions: at first extra workers raise output a lot and MC falls; later crowding makes MC rise.
3. **MC cuts AVC and AC at their minimum points.** Here AVC is minimum (40) at Q = 3 to 4 and AC is minimum (64) at Q = 5. When MC is below the average, the average falls; when above, it rises.

*Long-run curve (Figure 4.2).* In the long run the firm may pick any plant size. Each plant has its own SAC curve. For any output the firm chooses the plant with the lowest cost, so **LAC is the lower envelope of the SAC curves**, touching each at one output. LMC cuts LAC at its minimum.

*Why U-shaped.* Falling LAC comes from **economies of scale**: specialisation, bulk buying, spreading overhead and better technology. The flat part near the minimum efficient scale shows constant returns. Rising LAC comes from **diseconomies of scale**: coordination, communication and management problems.

| Feature | Short-run AC | Long-run AC |
|---|---|---|
| Fixed input | at least one | none |
| Shape cause | variable proportions | scale of operations |
| Curve | U, steeper | U, flatter envelope |

*Conclusion.* Short-run curves guide daily output decisions; the long-run curve guides the choice of plant size.

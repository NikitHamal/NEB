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

## Formula and fact sheet

- TC = TFC + TVC; AFC = TFC/Q; AVC = TVC/Q; AC = AFC + AVC; MC = ΔTC/ΔQ.
- MC cuts AVC and AC at their minima; AFC always falls.
- LAC is the envelope of SAC; economies then diseconomies of scale.
- TR = PQ; AR = P; MR = ΔTR/ΔQ. Perfect competition: AR = MR = P. Otherwise MR < AR; linear: MR has twice the slope.
- MR = AR(1 − 1/|e|); TR maximum where MR = 0.

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

::: note Answers and worked solutions
**1.** Explicit: paid to outsiders. Implicit: opportunity cost of owner's resources. Accounting cost = explicit; economic cost = explicit + implicit.
**2.** TC = 80, 96, 108, 124, 150. MC = 20, 16, 12, 16, 26. AVC = 20, 18, 16, 16, 18. AC = 80, 48, 36, 31, 30.
**3.** If the marginal cost is below the average, adding that unit lowers the average; if above, it raises it; so MC crosses AC where AC stops falling, at its minimum.
**4.** TR = 60Q − 2Q²; MR = 60 − 4Q. TR is maximum where MR = 0: Q = **15** (P = 30, TR = 450).
**5.** LAC is the envelope of short-run AC curves: the lowest cost of each output when the plant size can be chosen. It falls with economies of scale, is flat at the minimum efficient scale and rises with diseconomies of scale.
**6.** To sell one more unit a monopolist must lower the price on **all** units, so the extra revenue is less than the price; a price-taker sells every unit at the same fixed price, so MR = P.
**7.** Accounting profit = 800 − 500 = **300**; economic profit = 800 − 850 = **−50** (a loss compared with the best alternative).
:::

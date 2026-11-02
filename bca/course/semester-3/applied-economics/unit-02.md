---
subject: Applied Economics
grade: BCA Semester 3
unit: 2
title: Elasticity of Demand and Supply
hours: 6
area: BCA 206 · Applied Economics · Unit 2
---

The law of demand says quantity falls when price rises; **elasticity** says *by how much*. A firm deciding whether to cut a price, a government deciding which good to tax, and a cloud provider changing a subscription fee all need it.

::: key What this unit gives you
- Price, income and cross elasticity of demand: concept and types.
- Measurement by the total outlay method, the point method and the arc (midpoint) method.
- Uses of elasticity; elasticity of supply; how to compute in Excel.
:::

## 2.1 Price elasticity of demand

**Price elasticity of demand (e_d)** = percentage change in quantity demanded ÷ percentage change in price. Because price and quantity move in opposite directions e_d is negative; we usually quote the absolute value |e_d|.

| Type | |e_d| | Meaning | Example |
|---|---|---|---|
| **Perfectly inelastic** | 0 | quantity does not change | life-saving drug (vertical demand) |
| **Inelastic** | 0 < |e| < 1 | quantity changes proportionally less than price | salt, electricity, petrol in the short run |
| **Unitary elastic** | = 1 | proportional change | |
| **Elastic** | > 1 | proportionally more | luxuries, restaurant meals, branded goods with substitutes |
| **Perfectly elastic** | ∞ | any price rise loses all sales (horizontal demand) | one farmer's wheat in a perfect market |

**Determinants:** availability and closeness of **substitutes** (more substitutes → more elastic); **necessity versus luxury**; **share of income** spent (matchboxes vs cars); **time period** (longer → more elastic); **definition of the market** (demand for "food" is inelastic, for "one brand of noodles" elastic); habit.

### Measurement 1: Total outlay (expenditure) method

Compare total expenditure TE = P × Q before and after a price change.

| Price change | Total outlay rises | Total outlay unchanged | Total outlay falls |
|---|---|---|---|
| **Price falls** | **elastic** (|e| > 1) | unitary (|e| = 1) | **inelastic** (|e| < 1) |
| **Price rises** | **inelastic** | unitary | **elastic** |

In words: if price and total outlay move in **opposite** directions, demand is **elastic**; in the **same** direction, **inelastic**; if outlay is unchanged, **unitary**.

::: example Worked example: total outlay
A price falls from NPR 10 to 8 and the quantity rises from 100 to 130. TE: 10 × 100 = **1,000** → 8 × 130 = **1,040**. Price fell and outlay rose (opposite directions): demand is **elastic** (|e| > 1). If instead the quantity had risen only to 110, TE = 880 < 1,000 and demand would be inelastic.
:::

### Measurement 2: Point method

At one point on the demand curve, **e = (dQ/dP) × (P/Q)** = (1/slope) × P/Q. For linear demand it varies along the curve: elastic at high prices, unit elastic at the midpoint, inelastic at low prices.

::: example Worked example: Q = 100 − 2P
dQ/dP = −2. At P = 20, Q = 60: e = −2 × 20/60 = **−0.667** (inelastic). At P = 25, Q = 50: e = −2 × 25/50 = **−1.0** (unit elastic, the midpoint of the line, where total revenue is maximum: 25 × 50 = 1,250). At P = 30, Q = 40: e = −2 × 30/40 = **−1.5** (elastic). Geometric form: e = lower segment ÷ upper segment of the demand line at that point.
:::

### Measurement 3: Arc (midpoint) method

For a discrete change use the averages so that the answer does not depend on the direction: **e = (ΔQ/Q̄) ÷ (ΔP/P̄)**, with Q̄ and P̄ the midpoints. For the example above: ΔQ = 30, Q̄ = 115 → 26.09%; ΔP = −2, P̄ = 9 → −22.22%; **e = −1.174** (elastic, agrees with the outlay test).

## 2.2 Income and cross elasticity of demand

**Income elasticity e_y = %ΔQ ÷ %ΔIncome.** Positive for **normal goods** (>1 luxury, 0–1 necessity); **negative** for **inferior goods** (instant noodles, public transport as income rises). Used to forecast demand as the economy grows and to decide which industries expand.

::: example Worked example
Income rises from NPR 20,000 to 24,000 a month and a student's monthly purchases of books rise from 50 to 56: %ΔQ = 6/53 = 11.32%; %ΔIncome = 4,000/22,000 = 18.18%; **e_y = 0.623**: books are a normal **necessity** (0 < e_y < 1).
:::

**Cross elasticity e_xy = %ΔQ_x ÷ %ΔP_y.** **Positive** for **substitutes** (tea and coffee), **negative** for **complements** (cars and petrol, printers and ink), zero for unrelated goods. Firms use it to see competition and to price product lines.

::: example Worked example
The price of tea rises from 10 to 12 and the quantity of coffee demanded rises from 80 to 88: %ΔQ = 8/84 = 9.52%; %ΔP = 2/11 = 18.18%; **e_xy = +0.524**: tea and coffee are **substitutes**.
:::

## 2.3 Uses of elasticity

- **Business pricing:** if demand is **elastic**, a price *cut* raises revenue; if **inelastic**, a price *rise* raises revenue. A software seller with many competitors (elastic) cuts price to grow; a monopoly utility (inelastic) can raise price.
- **Taxation:** governments tax **inelastic** goods (fuel, tobacco) for stable revenue; the tax burden falls more on the side with the **less elastic** curve.
- **Agriculture:** a bumper harvest can **lower** farmers' income because food demand is inelastic (price falls proportionally more than quantity rises).
- **International trade:** devaluation helps the trade balance only if import and export demands are sufficiently elastic (Marshall–Lerner condition: sum of elasticities > 1).
- **Planning:** income elasticity guides forecasts and investment; cross elasticity guides competition policy.

## 2.4 Elasticity of supply

**e_s = %ΔQ_s ÷ %ΔP**, positive. Determinants: **time** (supply is more elastic in the long run), availability of inputs and spare capacity, storability, flexibility of production. Perfectly inelastic supply is vertical (land, a concert hall's seats); perfectly elastic is horizontal.

::: example Worked example: supply and the numerical exercise in Excel
Price rises from 50 to 60 and the quantity supplied from 200 to 260: midpoint %ΔQ = 60/230 = 26.09%; %ΔP = 10/55 = 18.18%; **e_s = 1.435** (elastic).
**In Excel:** put prices in B2:B3 and quantities in C2:C3; the midpoint elasticity is `=((C3-C2)/AVERAGE(C2:C3))/((B3-B2)/AVERAGE(B2:B3))`; the point elasticity at P = 20 for Q = 100 − 2P is `=-2*20/(100-2*20)`; the total outlay is `=B2*C2` and `=B3*C3`.
:::

## Formula and fact sheet

- e_d = %ΔQ/%ΔP; point: (dQ/dP)(P/Q); arc: (ΔQ/Q̄)/(ΔP/P̄).
- Total outlay: price and outlay opposite directions → elastic; same → inelastic; unchanged → unitary.
- Linear demand: elastic above the midpoint, e = 1 at the midpoint, inelastic below.
- e_y > 0 normal (>1 luxury), < 0 inferior. e_xy > 0 substitutes, < 0 complements.
- Supply elasticity grows with time.

## Chapter summary

- Elasticity measures responsiveness; price elasticity is classified from perfectly inelastic to perfectly elastic and depends on substitutes, necessity, income share and time.
- Total outlay, point and arc methods measure it; income and cross elasticities classify goods and relationships.
- Elasticity guides pricing, taxation and policy.

## Practice

1. A price rises from 20 to 25 and the quantity demanded falls from 200 to 150. Find the arc elasticity and classify demand. Check with the total outlay method.
2. For Q = 80 − 4P find the point elasticity at P = 5 and P = 15, and the price of unit elasticity.
3. Income rises 10% and the demand for a good falls 4%. Find e_y and classify the good.
4. The price of petrol rises 20% and the demand for cars falls 6%. Find e_xy and the relationship.
5. Explain why a bumper crop may reduce farmers' income.
6. List four determinants of price elasticity of demand.
7. Price rises from 100 to 110 and Q_s from 500 to 560. Find e_s (midpoint).

::: note Answers and worked solutions
**1.** ΔQ = −50, Q̄ = 175 → −28.57%; ΔP = 5, P̄ = 22.5 → 22.22%; e = **−1.286** → elastic. TE: 20 × 200 = 4,000 → 25 × 150 = 3,750: price up, outlay down (opposite) → elastic ✓.
**2.** dQ/dP = −4. At P = 5, Q = 60: e = −4 × 5/60 = **−0.333**. At P = 15, Q = 20: e = −4 × 15/20 = **−3**. Unit elasticity: −4P/(80 − 4P) = −1 → 4P = 80 − 4P → **P = 10**.
**3.** e_y = −4/10 = **−0.4**: inferior good.
**4.** e_xy = −6/20 = **−0.3**: complements.
**5.** Demand for food is inelastic, so the price falls proportionally more than output rises and total revenue falls.
**6.** Substitutes, necessity vs luxury, share of income, time period (also market definition).
**7.** ΔQ = 60, Q̄ = 530 → 11.32%; ΔP = 10, P̄ = 105 → 9.52%; **e_s = 1.19**.
:::

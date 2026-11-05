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

## 2.5 Seeing elasticity: five cases, the demand line and the bumper harvest

```svgfig label="2.1" caption="The five cases of price elasticity of demand. The flatter the curve, the more sensitive buyers are to price; the steeper, the less. Unit elasticity is a rectangular hyperbola (price × quantity constant)."
f = Fig(580, 175)
names = [("Perfectly inelastic", "e = 0"), ("Inelastic", "0 < e < 1"), ("Unit elastic", "e = 1"), ("Elastic", "1 < e < ∞"), ("Perfectly elastic", "e = ∞")]
for i, (n, e) in enumerate(names):
    a = Axes(f, 26 + i * 114, 10, 90, 100, (0, 10), (0, 10))
    a.axes("Q", "P")
    f.text(71 + i * 114, 140, n, size=10.5, color=NAVY, bold=True); f.text(71 + i * 114, 157, e, size=11, color=TEAL, bold=True)
    if i == 0: a.vline(5, 0, 10, color=NAVY, dash=False, sw=2.4)
    if i == 1: f.line(a.X(3.5), a.Y(9), a.X(6), a.Y(1.5), color=NAVY, sw=2.4)
    if i == 2: a.curve(lambda q: 16 / q, 1.6, 10, color=NAVY)
    if i == 3: f.line(a.X(1), a.Y(7), a.X(9), a.Y(3), color=NAVY, sw=2.4)
    if i == 4: a.hline(5, 0, 10, color=NAVY, dash=False, sw=2.4)
```

```svgfig label="2.2" caption="Linear demand Q = 100 − 2P. (a) Elasticity falls along the line: 1.5 at P = 30 (elastic), 1.0 at the midpoint P = 25, 0.667 at P = 20 (inelastic). (b) Total revenue P × Q rises while demand is elastic, peaks at 1,250 where e = 1, then falls."
f = Fig(580, 245)
a = Axes(f, 42, 14, 225, 175, (0, 100), (0, 50))
a.grid(20, 10).axes("Quantity", "Price")
a.curve(lambda q: 50 - q / 2, 0, 100, color=NAVY)
a.area(lambda q: 50 - q / 2, 0, 50, fill="#fde68a", opacity=0.35)
a.pt(40, 30, "e = 1.5", dx=8, dy=-6, color=RED); a.pt(50, 25, "e = 1", dx=8, dy=-6, color=TEAL); a.pt(60, 20, "e = 0.667", dx=8, dy=-6, color=AMBER)
a.tag(14, 14, "elastic zone", size=10.5, color=RED, bold=True); a.tag(86, 20, "inelastic", size=10.5, color=AMBER, bold=True)
b = Axes(f, 335, 14, 225, 175, (0, 100), (0, 1400))
b.grid(20, 400).axes("Quantity", "Total revenue")
b.curve(lambda q: q * (100 - q) / 2, 0, 100, color=TEAL)
b.vline(50, 0, 1250, color=AMBER); b.pt(50, 1250, "max 1,250", dx=-8, dy=-8, anchor="end")
b.tag(20, 300, "e > 1", size=10.5, color=RED, bold=True); b.tag(82, 300, "e < 1", size=10.5, color=AMBER, bold=True)
f.text(155, 232, "(a) demand line and elasticity zones", size=11, color=SLATE, italic=True)
f.text(448, 232, "(b) total revenue peaks where e = 1", size=11, color=SLATE, italic=True)
```

```photogrid label="2.1" cols="2" ratio="1.0" caption="Why a bumper harvest can hurt farmers. (a) Spices and staple foods at Asan have few close substitutes, so demand is steep (inelastic). (b) With demand P = 60 − 0.4Q, a good harvest moves supply from S1 to S2: price falls from 16 to 8 while quantity rises only from 110 to 130, so revenue drops from 1,760 to 1,040."
@ photo id="bca206/spice" cap="Spice stalls, Asan Bazaar, Kathmandu"
fit 1.0
focus 0.5 0.45
@ svg cap="Inelastic demand and a supply increase"
f = Fig(300, 300)
a = Axes(f, 40, 12, 245, 220, (0, 150), (0, 60))
a.grid(50, 20, size=10.5).axes("Q", "P")
a.curve(lambda q: 60 - 0.4 * q, 0, 150, color=NAVY)
a.curve(lambda q: 0.1 * q + 5, 0, 150, color=TEAL); a.curve(lambda q: 0.1 * q - 5, 50, 150, color=AMBER, dash=True)
a.pt(110, 16, "", color=TEAL); a.pt(130, 8, "", color=RED)
f.text(180, 262, "S1 → S2 (dashed)", size=12, color=AMBER, bold=True)
f.text(150, 282, "revenue 1,760 → 1,040", size=12.5, color=RED, bold=True)
```

```photogrid label="2.2" cols="2" ratio="1.0" caption="Income elasticity and Engel's law. (a) Ernst Engel (1821-1896), the Saxon statistician who showed in 1857 that the share of income spent on food falls as income rises. (b) Illustrative monthly figures for a household (invented to show the pattern): income in thousand rupees 20, 40, 60, 80, 100 and food spending 12, 18, 22, 25, 27. By the midpoint formula the income elasticity between 20 and 40 is (6 / 15) / (20 / 30) = 0.60 and between 80 and 100 it is (2 / 26) / (20 / 90) = 0.35. Both are below 1, so food is a necessity: spending rises, but more slowly than income, and the food share falls from 60 per cent to 27 per cent. A good with income elasticity above 1 (a mobile phone plan, eating out) would show a share that rises with income."
@ photo id="bcaeco/engel" cap="Ernst Engel (1821-1896)"
fit 1.0
focus 0.5 0.3
@ svg cap="Engel curve for food (illustrative household)"
inc = [20, 40, 60, 80, 100]; food = [12, 18, 22, 25, 27]
def arc(i):
    q0, q1, y0, y1 = food[i], food[i + 1], inc[i], inc[i + 1]
    return ((q1 - q0) / ((q0 + q1) / 2)) / ((y1 - y0) / ((y0 + y1) / 2))
e = [arc(i) for i in range(4)]
assert [round(x, 2) for x in e] == [0.6, 0.5, 0.45, 0.35] and all(x < 1 for x in e)
assert [round(100 * q / y) for q, y in zip(food, inc)] == [60, 45, 37, 31, 27]
f = Fig(300, 240)
ax = Axes(f, 44, 42, 240, 134, (0, 110), (0, 30))
ax.grid(20, 10, size=10.5).axes("income (thousand Rs)", "food (thousand Rs)")
for i in range(4):
    f.line(ax.X(inc[i]), ax.Y(food[i]), ax.X(inc[i + 1]), ax.Y(food[i + 1]), color=NAVY, sw=2.2)
for y, q in zip(inc, food):
    ax.pt(y, q, "", color=RED, r=4)
f.text(150, 14, "Engel curve for food flattens as income rises", size=10.5, color=NAVY, bold=True)
f.text(150, 206, "income elasticity 0.60, 0.50, 0.45, 0.35", size=10.5, color=TEAL, bold=True)
f.text(150, 226, "food share of income 60% -> 27%", size=10.5, color=RED, bold=True)
```

```photogrid label="2.3" cols="2" ratio="1.0" caption="Who really pays a fuel tax? (a) A 1952 petrol pump: fuel is the classic good to tax because demand is inelastic. (b) Linear model with demand Q = 300 - 2P and supply Q = 4P (price in rupees per litre, quantity in thousand litres; invented numbers). Before tax the market clears at P = 50 and Q = 200. At that point the elasticity of demand is 2 x 50 / 200 = 0.5 and that of supply is 4 x 50 / 200 = 1.0. A tax of Rs 12 per litre shifts the supply curve up by 12; the new equilibrium is P = 58, Q = 184. Buyers pay 8 more and sellers keep 4 less, so buyers bear 8 / 12 = 2/3 of the tax, exactly Es / (Es + Ed) = 1 / 1.5. The government collects 12 x 184 = 2,208 thousand rupees. The less elastic side carries the larger share."
@ photo id="bcaeco/petrol" cap="A petrol pump of 1952"
fit 1.0
focus 0.5 0.4
@ svg cap="A Rs 12 tax: buyers carry 2/3"
Ed, Es = 2 * 50 / 200, 4 * 50 / 200
assert (Ed, Es) == (0.5, 1.0)
pn = (300 + 48) / 6; qn = 300 - 2 * pn
assert (qn, pn) == (184, 58) and 4 * (pn - 12) == qn
buyer = pn - 50; seller = 50 - (pn - 12)
assert (buyer, seller) == (8, 4) and abs(buyer / 12 - Es / (Es + Ed)) < 1e-9 and 12 * qn == 2208
f = Fig(300, 240)
ax = Axes(f, 48, 42, 236, 134, (150, 230), (30, 80))
ax.grid(20, 10, size=10.5).axes("quantity (thousand L)", "price (Rs/L)")
ax.curve(lambda q: (300 - q) / 2, 150, 230, color=BLUE, label="D", lx=ax.X(222), ly=ax.Y(36))
ax.curve(lambda q: q / 4, 150, 230, color=TEAL, label="S", lx=ax.X(224), ly=ax.Y(57))
ax.curve(lambda q: q / 4 + 12, 150, 218, color=RED, dash=True, label="S + tax", lx=ax.X(206), ly=ax.Y(70))
ax.pt(200, 50, "", color=NAVY); ax.pt(184, 58, "", color=RED)
ax.hline(58, 150, 184, color=RED); ax.hline(50, 150, 200, color=NAVY); ax.hline(46, 150, 184, color=AMBER)
ax.vline(184, 30, 58, color=RED)
f.text(150, 14, "price 50 -> buyers pay 58, sellers keep 46", size=10.5, color=NAVY, bold=True)
f.text(150, 206, "buyers +8, sellers -4: buyers bear 2/3", size=10.5, color=RED, bold=True)
f.text(150, 226, "Ed 0.5 (steeper) < Es 1.0, revenue 2,208", size=10.5, color=TEAL, bold=True)
```

## 2.6 Eight uses of elasticity in business, government and Nepal

1. **Setting the price of a product.** If demand is elastic, a small price cut brings a large rise in sales, so total revenue grows. A Nepali mobile-data company with many rivals therefore offers cheap packs to win users. If demand is inelastic, a price cut only loses revenue, so a seller of an essential item keeps the price firm.
2. **Choosing which goods to tax.** Governments prefer to tax goods with inelastic demand, such as fuel, cigarettes and alcohol, because buyers keep buying and the revenue is steady. Nepal's excise duties follow this logic. Heavy taxes on an elastic luxury would simply push buyers to stop or to smuggle.
3. **Sharing the burden of a tax.** The side of the market with the less elastic curve pays the larger part of a tax. When demand for petrol is inelastic, nearly all of a new tax passes to the motorist. Knowing this lets a student predict who will really pay, whatever the law says.
4. **Understanding the farmers' paradox.** Food has inelastic demand, so a bumper harvest lowers the price by more than it raises the quantity sold. The farmers of the Terai may earn less from a record rice crop than from an average one. This is why support prices and storage are discussed every season.
5. **Exchange rate and trade policy.** A weaker currency makes exports cheaper and imports dearer, but the trade balance improves only if demand elasticities are high enough (Marshall-Lerner: the sum is above 1). Nepal's imports of fuel and medicine are inelastic, so a depreciation helps little. The rule explains why trade policy needs more than a change in the rate.
6. **Forecasting demand as incomes grow.** Income elasticity shows how fast demand rises when incomes rise. Luxuries, such as smartphones and air travel, grow faster than income, while inferior goods, such as cheap noodles, fall. Banks and telecom firms use this to decide where to expand.
7. **Reading competition between products.** Cross elasticity is large and positive for close substitutes, such as two mobile-wallet apps. A firm that sees this knows a price rise will send customers to its rival. For complements, such as printers and ink, a fall in one price raises sales of the other.
8. **Timing and planning supply.** Supply is more elastic over a longer period because factories, farms and servers can be expanded. A hydropower plant cannot respond to a price signal this year, but it can in ten years. Planners use the idea to decide whether a shortage is temporary or needs investment.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the total outlay method of measuring price elasticity of demand. A price falls from NPR 10 to 8 and quantity rises from 100 to 130; what do you conclude?**

*Introduction.* **Price elasticity of demand** measures how strongly the quantity demanded responds to a change in price. The **total outlay (expenditure) method**, due to Marshall, finds it without any formula by comparing what buyers spend, TE = P × Q, before and after the price change.

*Rule.*

| Price change | Outlay rises | Outlay unchanged | Outlay falls |
|---|---|---|---|
| Price falls | elastic (e > 1) | unitary (e = 1) | inelastic (e < 1) |
| Price rises | inelastic | unitary | elastic |

In words: if price and outlay move in **opposite** directions the demand is **elastic**; in the **same** direction, **inelastic**; if outlay does not change, **unitary**.

*Numerical case.* Before: TE = 10 × 100 = 1,000. After: TE = 8 × 130 = 1,040. Price fell and outlay rose, which is the opposite direction, so demand is **elastic**. A cross-check by the midpoint formula gives %ΔQ = 30/115 = 26.09% and %ΔP = −2/9 = −22.22%, so e = −1.174, which agrees (Figure 2.2b shows the same idea: revenue rises while e > 1).

*Merit and limit.* The method is simple and needs no calculus, but it gives only the class of elasticity, not its numerical value.

*Conclusion.* Outlay rose after the price fell, so demand is elastic and the seller gains by the cut.

**Q2 (5 marks). Define income elasticity and cross elasticity of demand. Show how they classify goods, with a numerical example of each.**

*Introduction.* Price is not the only determinant of demand. **Income elasticity** and **cross elasticity** measure the response of quantity to income and to another good's price.

*Income elasticity* e_y = %ΔQ ÷ %ΔIncome.

1. e_y > 1: **luxury** (smartphones, air travel); demand rises faster than income.
2. 0 < e_y < 1: **necessity** (books, rice); demand rises more slowly.
3. e_y < 0: **inferior** good (cheap noodles); demand falls as income rises.

*Example.* Income rises from NPR 20,000 to 24,000 and book purchases from 50 to 56. %ΔQ = 6/53 = 11.32% and %ΔIncome = 4,000/22,000 = 18.18%, so e_y = **0.623**, a necessity.

*Cross elasticity* e_xy = %ΔQ_x ÷ %ΔP_y.

1. e_xy > 0: **substitutes** (tea and coffee).
2. e_xy < 0: **complements** (printers and ink).
3. e_xy = 0: unrelated goods.

*Example.* The price of tea rises from 10 to 12 and coffee sales rise from 80 to 88. %ΔQ = 8/84 = 9.52% and %ΔP = 2/11 = 18.18%, so e_xy = **+0.524**: substitutes.

*Conclusion.* Firms use e_y to forecast growth of demand and e_xy to measure rivalry and set the prices of related products.

**Q3 (10 marks). Define price elasticity of demand. Explain its types and determinants, describe the three methods of measuring it, and discuss its practical uses.**

*Introduction.* **Price elasticity of demand** is the percentage change in quantity demanded divided by the percentage change in price. Since price and quantity move in opposite directions the value is negative, and we usually quote its absolute value |e|.

*Types (Figure 2.1).* (1) **Perfectly inelastic**, e = 0: vertical curve, as for a life-saving drug. (2) **Inelastic**, 0 < e < 1: steep curve, as for salt or electricity. (3) **Unitary**, e = 1: a rectangular hyperbola with constant outlay. (4) **Elastic**, e > 1: flat curve, as for restaurant meals or a branded phone with many rivals. (5) **Perfectly elastic**, e = ∞: horizontal curve, as for one wheat farmer in a perfect market.

*Determinants.* Number and closeness of **substitutes**; necessity or luxury; **share of income** spent; **time period** (longer means more elastic); breadth of the market definition; and habit.

*Measurement.*

1. **Total outlay method:** compare P × Q before and after (Q1). Opposite movement means elastic.
2. **Point method:** e = (dQ/dP) × (P/Q). For Q = 100 − 2P, dQ/dP = −2, so e = −2 × 30/40 = **−1.5** at P = 30 (elastic), **−1** at P = 25 (midpoint, revenue 1,250 is maximum) and **−0.667** at P = 20 (inelastic); see Figure 2.2.
3. **Arc method:** e = (ΔQ/Q̄) ÷ (ΔP/P̄), for example −1.174 for the move from (10, 100) to (8, 130).

*Uses.* (1) **Pricing:** cut price if demand is elastic, raise it if inelastic. (2) **Taxation:** tax inelastic goods such as fuel for steady revenue. (3) **Agriculture:** a bumper harvest lowers farm income because food demand is inelastic (Plate 2.1). (4) **Trade:** devaluation helps only if elasticities sum to more than 1. (5) **Planning:** income and cross elasticities guide investment and competition policy.

| Elasticity | Price rise by 10% | Revenue effect | Best seller action |
|---|---|---|---|
| e = 2 (elastic) | quantity falls 20% | revenue falls | cut price |
| e = 1 | quantity falls 10% | unchanged | hold price |
| e = 0.5 (inelastic) | quantity falls 5% | revenue rises | raise price |

*Conclusion.* Elasticity turns the shape of the demand curve into a number that managers and governments can act on.

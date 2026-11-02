---
subject: Financial Accounting
grade: BCA Semester 7
unit: 5
title: Depreciation and Inventory Valuation
hours: 7
area: BCA 403 · Financial Accounting · Unit 5
---

A delivery van bought for Rs 6,00,000 does not stay worth that amount; it is used up, worn out and eventually sold for scrap. **Depreciation** spreads the cost of such an asset over the years that benefit from it, which is the matching concept in action. The other great judgement in measuring profit is the value placed on unsold goods at year end: **inventory valuation**. Both change profit without moving any cash, and both are choices governed by standards.

::: key What this unit gives you
- The meaning, causes and accounting entries of depreciation.
- Straight-line (SLM) and written-down-value (WDV) schedules, and why they differ.
- Profit or loss on disposal of an asset.
- Inventory valuation by FIFO and weighted average, and the lower of cost and net realisable value.
:::

## 5.1 What depreciation is

**Depreciation** is the systematic allocation of the **depreciable amount** of a tangible asset (cost less estimated residual or *salvage* value) over its **useful life**. Causes include wear and tear, obsolescence, passage of time and depletion. It is **not** a way of setting aside cash and does not measure the asset's market value: it is an allocation of cost. The standard that governs this (IAS 16, adopted in Nepal as the NFRS for property, plant and equipment) requires that the method reflect the pattern in which the asset's benefits are consumed and that the life and residual value be reviewed at least annually.

## 5.2 Methods

**Straight-line method (SLM):** an equal charge each year.

Annual depreciation = (Cost − Residual value) ÷ Useful life.

**Written-down-value method (WDV, also reducing-balance):** a fixed *percentage* of the opening book value each year, so the charge is highest at the start. It suits assets whose usefulness or repair cost pattern is front-loaded, and it never reaches exactly zero.

Nepal's Income Tax Act 2058 does not use the accounting method for tax: it groups assets into **depreciation pools** (blocks) and allows a declining-balance rate per block, for example about 5% for buildings, 25% for computers, furniture and office equipment, 20% for vehicles and construction equipment, and 15% for other assets (verify against the current schedule). Accounting depreciation per NFRS and tax depreciation per the Act therefore differ, and the difference is carried into a tax computation.

::: example SLM versus WDV
A van costs Rs 6,00,000 with residual value Rs 60,000 and a five-year life. SLM depreciation is (600,000 − 60,000) ÷ 5 = Rs 108,000 each year. Under WDV at 25%, year 1 charges Rs 150,000 and year 2 charges 25% of 4,50,000, which is Rs 112,500.
:::

```python
from decimal import Decimal as D, ROUND_HALF_UP
cost, salvage, life = 600000, 60000, 5
slm = (cost - salvage) // life
print(f"SLM annual charge: {slm}")
book = D(cost)
for year in range(1, life + 1):
    dep = (book * D("0.25")).quantize(D("0.01"), ROUND_HALF_UP)
    book -= dep
    print(f"year {year}: WDV charge {dep}, closing {book}")
print(f"year {life} closing WDV: {book}")
```
```output
SLM annual charge: 108000
year 1: WDV charge 150000.00, closing 450000.00
year 2: WDV charge 112500.00, closing 337500.00
year 3: WDV charge 84375.00, closing 253125.00
year 4: WDV charge 63281.25, closing 189843.75
year 5: WDV charge 47460.94, closing 142382.81
year 5 closing WDV: 142382.81
```
After five years SLM leaves the van at its residual value of Rs 60,000, while WDV at 25% leaves a book value of Rs 142,382.81. The WDV total charge is smaller in the later years and larger in the early years, so profit is lower early and higher later than under SLM.

## 5.3 Accounting entries

**Direct method:** the asset account is credited each year: *Dr Depreciation Expense, Cr Asset*. **Provision method:** the asset stays at cost and the credit goes to an **Accumulated Depreciation** account: *Dr Depreciation Expense, Cr Accumulated Depreciation*. The balance sheet then shows cost, less accumulated depreciation, equals book value (carrying amount). NFRS presentations use the provision method. Depreciation Expense is closed to the Profit and Loss Account at year end.

::: caution
Land is not depreciated (it has an unlimited life), though buildings on it are. A common error is to depreciate the land and building at one combined rate.
:::

## 5.4 Disposal of an asset

When an asset is sold, compute its **book value** at the date of sale and compare it with the sale proceeds. If proceeds exceed book value, there is a **gain**; otherwise a **loss**. The gain or loss goes to the Profit and Loss Account. The entries use an *Asset Disposal Account*:

1. Transfer the asset's cost: Dr Disposal, Cr Asset.
2. Transfer its accumulated depreciation: Dr Accumulated Depreciation, Cr Disposal.
3. Record the proceeds: Dr Cash or Bank, Cr Disposal.
4. The balancing figure on the disposal account is the gain (credit) or loss (debit), transferred to Profit and Loss.

Depreciation is charged up to the date of sale; a part-year charge is made pro rata by months unless the firm's policy says otherwise.

```python
cost, annual, years_used, proceeds = 600000, 108000, 3, 300000
accumulated = annual * years_used
book_value = cost - accumulated
result = proceeds - book_value
print(f"{'gain' if result >= 0 else 'loss'} on disposal: {abs(result)}")
```
```output
gain on disposal: 24000
```
After three years under SLM the accumulated depreciation is Rs 3,24,000 and the book value Rs 276,000. A sale at Rs 3,00,000 produces a **gain of Rs 24,000**.

## 5.5 Inventory valuation

Closing inventory is deducted from the goods available for sale to find the cost of goods sold (COGS), so any change in its valuation moves profit by the same amount. NFRS (IAS 2) requires inventory at the **lower of cost and net realisable value (NRV)**, where NRV is the estimated selling price less the costs to complete and sell. **LIFO is not permitted**; the allowed cost formulas are **FIFO** and **weighted average**, or specific identification for unique items.

- **FIFO (first in, first out):** the oldest purchases are assumed sold first, so closing inventory consists of the *latest* purchases. In rising prices it gives a lower COGS and a higher profit.
- **Weighted average cost:** each unit carries the average cost of all units available.

::: example FIFO versus weighted average
Purchases: 100 units at Rs 50, 200 units at Rs 55, 150 units at Rs 60 (total 450 units costing Rs 25,000). The business sells 280 units at Rs 80 (revenue Rs 22,400).
:::

```python
from fractions import Fraction
lots = [(100, 50), (200, 55), (150, 60)]
sold = 280
need, cogs = sold, 0
left = []
for qty, price in lots:
    take = min(qty, need)
    cogs += take * price
    need -= take
    if qty > take:
        left.append((qty - take, price))
closing = sum(q * p for q, p in left)
print(f"FIFO: COGS {cogs} closing {closing}")
total_cost = sum(q * p for q, p in lots)
units = sum(q for q, _ in lots)
w_cogs = Fraction(total_cost, units) * sold
print(f"Weighted average: COGS {float(w_cogs):.2f} closing {float(total_cost - w_cogs):.2f}")
```
```output
FIFO: COGS 14900 closing 10100
Weighted average: COGS 15555.56 closing 9444.44
```
FIFO gives COGS of Rs 14,900 and closing inventory of Rs 10,100, so gross profit is 22,400 − 14,900 = Rs 7,500. The weighted average cost per unit is Rs 55.56, giving COGS Rs 15,555.56, closing inventory Rs 9,444.44 and gross profit Rs 6,844.44. In both cases COGS plus closing stock equals Rs 25,000, the goods available.

The choice therefore changes reported profit by Rs 655.56 on the same physical transactions. A firm must apply the chosen method **consistently** and disclose it; switching merely to improve profit violates the consistency concept.

## 5.6 Periodic and perpetual systems

In the **periodic** system, purchases are debited to a Purchases account and inventory is determined by a physical count at period end. The **perpetual** system updates inventory after every purchase and sale, so the Inventory account is always current and COGS is recorded at each sale. The figures above are for a periodic weighted average, because a *perpetual* average would recompute the average after each receipt and give a slightly different COGS when sales and purchases interleave.

## 5.7 Summary and exercises

Depreciation allocates cost over useful life by SLM or WDV; disposal compares proceeds with book value; inventory is measured at the lower of cost and NRV using FIFO or weighted average, and the method moves profit.

1. Define depreciation and list four causes.
2. A machine costs Rs 4,50,000, residual value Rs 30,000, life 7 years. Prepare the SLM schedule and compute the WDV charge in year 2 at 20%.
3. Journalise depreciation under the direct and provision methods.
4. An asset costing Rs 2,00,000 with Rs 1,20,000 accumulated depreciation is sold for Rs 95,000. Prepare the disposal account.
5. Explain why LIFO is not allowed under NFRS.
6. Using the lots in this unit, compute COGS if 400 units are sold under FIFO.

---
subject: Financial Accounting
grade: BCA Semester 7
unit: 6
title: Final Accounts with Year-End Adjustments
hours: 8
area: BCA 403 · Financial Accounting · Unit 6
---

At the end of the fiscal year, the ledger holds hundreds of balances, but the owner wants three answers: *what was the gross margin on goods, what was the net profit, and what does the business own and owe?* The **final accounts** answer them: the **Trading Account**, the **Profit and Loss Account** and the **Balance Sheet**. Before they can be prepared, the trial balance must be corrected for the **adjustments** that accrual accounting demands.

::: key What this unit gives you
- The structure of the Trading Account, Profit and Loss Account and Balance Sheet.
- Year-end adjustments: closing stock, outstanding and prepaid items, accrued income, depreciation, bad debts and provisions, drawings.
- A complete worked set of final accounts, checked by a program, and the extension to a company.
- How these map to the NFRS statements.
:::

## 6.1 Trading Account

The **Trading Account** shows the gross result of buying and selling goods:

- **Debit side:** opening stock, purchases less purchases returns, direct expenses (carriage inwards, wages, freight, import duty).
- **Credit side:** net sales (sales less sales returns) and closing stock.

Cost of goods sold = opening stock + net purchases + direct expenses − closing stock. **Gross profit = net sales − cost of goods sold.** A gross loss arises if the balance is the other way.

## 6.2 Profit and Loss Account

The **Profit and Loss Account** starts with the gross profit and subtracts *indirect* (operating) expenses: salaries, rent, depreciation, bad debts, interest, advertising. It adds other incomes (interest and commission received). The result is **net profit**, which is transferred to the owner's capital account. Items are included on an accrual basis for the period only.

## 6.3 Balance Sheet

The **Balance Sheet** is a *statement of position at a date*, not an account. Assets are listed (in the Nepali tradition, often in order of liquidity or permanence) on one side, liabilities and capital on the other. Classification: **non-current assets** (fixed), **current assets** (cash, debtors, stock, prepaid), **non-current liabilities** (long-term loans), **current liabilities** (creditors, outstanding expenses, bank overdraft), and **equity**.

## 6.4 Year-end adjustments

Adjustments are not in the trial balance, so each affects **two places** in the final accounts, the income statement and the balance sheet.

| Adjustment | Income statement | Balance sheet |
|---|---|---|
| Closing stock | Credit of Trading Account (reduces COGS) | Current asset |
| Outstanding expense | Added to the expense | Current liability |
| Prepaid expense | Deducted from the expense | Current asset |
| Accrued income | Added to the income | Current asset |
| Income received in advance | Deducted from income | Current liability |
| Depreciation | Expense | Deducted from the asset |
| Bad debts written off | Expense | Deducted from debtors |
| Provision for doubtful debts | Expense (change in the provision) | Deducted from debtors |
| Drawings of goods | Deducted from purchases | Deducted from capital |

::: caution
The **double effect** is the key. If you add an outstanding salary to the expense but forget to show the liability on the balance sheet, the balance sheet will not balance. The balancing check is a built-in test for forgotten adjustments.
:::

## 6.5 A complete worked example

The trial balance of a trader (in rupees) at 31 Ashad is processed with these adjustments: closing stock Rs 70,000; salaries outstanding Rs 10,000; rent prepaid Rs 5,000; depreciation of furniture Rs 25,000; and a provision for doubtful debts of 2% on debtors. The program lists the trial balance, asserts that it agrees, applies the adjustments and builds the three statements.

```python
dr = {"Opening stock": 40000, "Purchases": 600000, "Sales returns": 20000, "Carriage inwards": 5000,
      "Wages": 30000, "Salaries": 110000, "Rent": 60000, "Furniture (cost)": 300000,
      "Bad debts": 8000, "Debtors": 200000, "Drawings": 30000, "Cash and bank": 223000}
cr = {"Capital": 500000, "Sales": 1000000, "Purchases returns": 10000,
      "Creditors": 110000, "Interest income": 6000}
assert sum(dr.values()) == sum(cr.values())
closing_stock, out_sal, pre_rent, dep = 70000, 10000, 5000, 25000
prov = dr["Debtors"] * 2 // 100

net_sales = cr["Sales"] - dr["Sales returns"]
cogs = (dr["Opening stock"] + dr["Purchases"] - cr["Purchases returns"]
        + dr["Carriage inwards"] + dr["Wages"] - closing_stock)
gross = net_sales - cogs
print(f"gross profit: {gross}")
expenses = (dr["Salaries"] + out_sal) + (dr["Rent"] - pre_rent) + dep + dr["Bad debts"] + prov
net = gross + cr["Interest income"] - expenses
print(f"net profit: {net}")

equity = cr["Capital"] + net - dr["Drawings"]
assets = (dr["Furniture (cost)"] - dep) + closing_stock + (dr["Debtors"] - prov) + pre_rent + dr["Cash and bank"]
liabilities = cr["Creditors"] + out_sal
print(f"balance sheet total: {assets} = {equity + liabilities}")
assert assets == equity + liabilities

tax = net * 25 // 100
print(f"company: tax {tax}, profit after tax {net - tax}")
```
```output
gross profit: 385000
net profit: 179000
balance sheet total: 769000 = 769000
company: tax 44750, profit after tax 134250
```
Cost of goods sold is Rs 595,000 and the gross profit is Rs 385,000. Operating expenses total Rs 212,000 (salaries 1,20,000, rent 55,000, depreciation 25,000, bad debts 8,000 and the 4,000 provision), and after adding interest income of Rs 6,000 the net profit is Rs 179,000. Closing capital is 5,00,000 + 1,79,000 − 30,000 = Rs 649,000.

The balance sheet then reads:

| Liabilities and equity | Rs | Assets | Rs |
|---|---|---|---|
| Capital (closing) | 6,49,000 | Furniture 3,00,000 − 25,000 | 2,75,000 |
| Creditors | 1,10,000 | Closing stock | 70,000 |
| Salaries outstanding | 10,000 | Debtors 2,00,000 − provision 4,000 | 1,96,000 |
| | | Prepaid rent | 5,000 |
| | | Cash and bank | 2,23,000 |
| **Total** | **769,000** | **Total** | **769,000** |

::: note
Each adjustment is entered **twice** in the working papers, once for the income statement and once for the balance sheet. A "ten-column worksheet" (trial balance, adjustments, adjusted trial balance, income statement, balance sheet) is the professional way to organise this and makes omissions visible.
:::

## 6.6 Provision for doubtful debts

Bad debts actually written off are an expense. A **provision** estimates those still hidden in debtors. The provision is created at year end as a percentage of *good* debtors (after specific bad debts have been written off). Only the **change** in the provision is charged each year: a first-time provision of Rs 4,000 is a full expense, whereas raising it to Rs 5,500 next year charges Rs 1,500 and lowering it credits the difference to Profit and Loss. NFRS 9 (IFRS 9) goes further with *expected credit losses*, but the same logic of a charge and an offsetting contra-asset holds.

## 6.7 Final accounts of a company

A company's accounts differ in capital structure and distribution. Under the Companies Act 2063:

- **Share capital** (authorised, issued, paid-up), **share premium**, **reserves** and **retained earnings** replace the sole trader's capital.
- Profit before tax is reduced by **income tax**, taken here at the general corporate rate of 25% (banks and certain sectors carry different rates). The program shows tax of Rs 44,750 on a profit of 1,79,000, leaving **profit after tax of Rs 134,250**.
- Part of the after-tax profit may be distributed as dividend (cash or **bonus shares**), and statutory reserves may be required for some sectors. The rest is retained.
- Drawings do not exist; the owners are paid through dividends, and directors' pay is an expense.

Under NFRS the statements are renamed: *Statement of Financial Position*, *Statement of Profit or Loss and Other Comprehensive Income*, *Statement of Changes in Equity* and *Statement of Cash Flows*, with notes on policies. The numbers computed here fit those headings directly.

## 6.8 Manufacturing account

A business that **makes** what it sells prepares a **manufacturing account** before the trading account. It finds the **cost of goods manufactured** (cost of production), which then takes the place of purchases in the trading account.

| Line | Contents |
|---|---|
| Direct materials consumed | Opening raw materials + purchases (+ carriage in) - closing raw materials |
| Direct labour (wages) | Wages of workers who make the product |
| Direct expenses | Royalty on production, hire of a special machine |
| **Prime cost** | Materials + labour + direct expenses |
| Factory overheads | Factory rent, power, depreciation of machinery, indirect wages, supervision |
| Work in progress | Add opening, deduct closing (partly finished goods) |
| **Cost of goods manufactured** | Prime cost + factory overheads + opening WIP - closing WIP |

Example (Rs): opening raw material 40,000, purchases 3,60,000, closing raw material 50,000, direct wages 1,20,000, factory overheads 80,000, opening WIP 20,000, closing WIP 30,000. Materials consumed = 40,000 + 3,60,000 - 50,000 = 3,50,000. Prime cost = 3,50,000 + 1,20,000 = 4,70,000. Cost of goods manufactured = 4,70,000 + 80,000 + 20,000 - 30,000 = **5,40,000**. In the trading account this figure is added to the opening inventory of finished goods and the closing finished-goods inventory is deducted to give cost of goods sold.

```python
mat = 40000 + 360000 - 50000
prime = mat + 120000
com = prime + 80000 + 20000 - 30000
print("materials consumed", mat, "| prime cost", prime, "| cost of goods manufactured", com)
```
```output
materials consumed 350000 | prime cost 470000 | cost of goods manufactured 540000
```
## 6.9 Seeing the ideas: from sales to net profit, the balance sheet and the five adjustments

The three figures below redraw the worked example of 6.5 so that every rupee can be followed from sales to the balance sheet.

```svgfig label="6.1" caption="How Rs 9,80,000 of net sales become a net profit of Rs 1,79,000 in the worked example of 6.5. Red bars are costs deducted; green bars are the subtotals gross profit (3,85,000) and net profit (1,79,000)."
f = Fig(580, 262)
k = 190 / 980000
base = 224
def bar(x, lo, hi, fl, st, top, bot):
    f.box(x, base - hi * k, 62, max((hi - lo) * k, 3), "", fill=fl, stroke=st)
    f.text(x + 31, base - hi * k - 8, top, size=10.5, color=st, bold=True)
    f.text(x + 31, base + 16, bot, size=10, color=SLATE)
f.line(10, base, 570, base, color=SLATE, sw=1.4)
bar(14, 0, 980000, BLUE, NAVY, "9,80,000", "Net sales")
bar(104, 385000, 980000, ROSE, RED, "-5,95,000", "Cost of\ngoods sold")
bar(194, 0, 385000, MINT, TEAL, "3,85,000", "Gross\nprofit")
bar(284, 173000, 385000, ROSE, RED, "-2,12,000", "Expenses")
bar(374, 173000, 179000, MINT, TEAL, "+6,000", "Interest\nincome")
bar(464, 0, 179000, MINT, TEAL, "1,79,000", "Net\nprofit")
for x0, x1, y in [(76, 104, 980000), (166, 194, 385000), (256, 284, 385000), (346, 374, 173000), (436, 464, 179000)]:
    f.line(x0, base - y * k, x1, base - y * k, color=SLATE, dash=True)
```

```svgfig label="6.2" caption="The balance sheet of 6.5 drawn to scale: assets of Rs 7,69,000 on the left equal capital 6,49,000 + creditors 1,10,000 + outstanding salaries 10,000 on the right. The closing capital is the opening 5,00,000 plus net profit 1,79,000 less drawings 30,000."
f = Fig(580, 262)
k = 220 / 769000
def stack(x, segs, w=150):
    y = 238
    for lab, v, fl, st in segs:
        h = v * k; y -= h
        f.box(x, y, w, h, lab if h >= 16 else "", fill=fl, stroke=st, size=10.5)
stack(40, [("Cash and bank 2,23,000", 223000, MINT, TEAL), ("Prepaid", 5000, SAND, AMBER), ("Debtors (net) 1,96,000", 196000, BLUE, NAVY), ("Stock 70,000", 70000, SAND, AMBER), ("Furniture (net) 2,75,000", 275000, ROSE, RED)])
stack(260, [("Capital 6,49,000", 649000, BLUE, NAVY), ("Creditors 1,10,000", 110000, ROSE, RED), ("", 10000, SAND, AMBER)])
f.text(115, 254, "Assets 7,69,000", size=11.5, color=NAVY, bold=True)
f.text(335, 254, "Equity + liabilities 7,69,000", size=11.5, color=NAVY, bold=True)

f.box(430, 20, 140, 70, "Capital =\n5,00,000 + 1,79,000\n- 30,000 = 6,49,000", fill=MINT, stroke=TEAL, size=10.5)
f.box(430, 104, 140, 50, "Small slivers:\nprepaid rent 5,000,\nsalaries due 10,000", fill=SAND, stroke=AMBER, size=10.5)
```

```svgfig label="6.3" caption="Every year-end adjustment is entered twice: once in the income statement and once in the balance sheet. That is why the balance sheet still balances after profit changes."
f = Fig(580, 232)
H = [("Adjustment", 8, 150), ("Income statement", 168, 190), ("Balance sheet", 366, 206)]
for t, x, w in H: f.box(x, 6, w, 26, t, fill=NAVY, color="#ffffff", bold=True, size=11.5)
R = [("Closing stock 70,000", "credit in trading: COGS falls", "current asset 70,000"), ("Salaries due 10,000", "expense rises to 1,20,000", "liability: outstanding 10,000"), ("Rent prepaid 5,000", "expense falls to 55,000", "current asset: prepaid 5,000"), ("Depreciation 25,000", "expense 25,000", "furniture 3,00,000 - 25,000"), ("Provision 2% = 4,000", "expense 4,000", "debtors 2,00,000 - 4,000")]
for i, (a, b, c) in enumerate(R):
    y = 40 + i * 38
    f.box(8, y, 150, 32, a, fill=SAND, stroke=AMBER, size=10.5)
    f.box(168, y, 190, 32, b, fill=MINT, stroke=TEAL, size=10.5)
    f.box(366, y, 206, 32, c, fill=BLUE, stroke=NAVY, size=10.5)
    f.arrow([(158, y + 16), (168, y + 16)], color=SLATE); f.arrow([(358, y + 16), (366, y + 16)], color=SLATE)
```

### 6.9.1 Eight checks before finalising the accounts

1. **Agree the trial balance first.** The totals must match before any adjustment starts. If they do not, find the error or place a labelled suspense balance. Final accounts built on a wrong trial balance are wrong from the start.
2. **Count the closing stock.** A physical count at the year end, valued at the lower of cost and net realisable value, gives the closing figure. In the example 70,000 of stock cut the cost of goods sold. A missed shelf changes profit.
3. **Accrue what is owed.** Expenses incurred but unpaid, like salaries due of Rs 10,000, belong to this year. Adding them lowers profit and creates a liability. Forgetting them overstates profit and understates debts.
4. **Defer what is prepaid.** Rent of Rs 5,000 paid for the next period is an asset today, not an expense. Deduct it from the rent expense and show it in the balance sheet. A shop that pays a year's rent in Shrawan shows only the used part.
5. **Charge depreciation.** Write down fixed assets by the policy method, here Rs 25,000 on furniture. This shows an honest book value. Skipping it inflates both profit and assets.
6. **Make the provision for doubtful debts.** Estimate the part of debtors that may not pay, here 2% of 2,00,000 or Rs 4,000, and charge it. Only the change in the provision goes to profit next year. This follows prudence.
7. **Separate capital from revenue items.** The purchase of furniture is capital and goes to the balance sheet, while carriage inwards is a cost of goods. Misplacing them shifts profit and hides assets. Check any large item again.
8. **Prove the balance sheet.** After all adjustments, assets must equal equity plus liabilities (7,69,000 each). Then compare ratios with last year to spot odd movements. A statement that balances and looks reasonable is ready for the auditor.

```photogrid label="6.1" cols="2" ratio="1.1" caption="From sales to net profit. (a) A Kathmandu shopkeeper at work; every shop must show the owner what is left after costs. (b) Illustrative year: sales Rs 5,00,000; opening stock 60,000; purchases 3,20,000; closing stock 80,000. Cost of goods sold = 60,000 + 3,20,000 - 80,000 = Rs 3,00,000, so gross profit is 5,00,000 - 3,00,000 = Rs 2,00,000, a gross margin of 40%. Expenses of salaries 70,000, rent 36,000 and depreciation 14,000 total Rs 1,20,000, leaving a net profit of Rs 80,000, a net margin of 16%. The Trading Account stops at gross profit; the Profit and Loss Account carries on to net profit; the balance sheet then shows where the money sits."
@ photo id="bcafa/shop" cap="A shop in Kathmandu"
fit 1.1
focus 0.5 0.5
@ svg cap="Waterfall from sales to net profit (thousand rupees)"
sales, ops, pur, cls = 500000, 60000, 320000, 80000
cogs = ops + pur - cls; gp = sales - cogs; exp = 70000 + 36000 + 14000; npf = gp - exp
assert (cogs, gp, exp, npf) == (300000, 200000, 120000, 80000) and gp / sales == 0.4 and npf / sales == 0.16
rows = [("Sales", 0, sales, "#1d6fb8"), ("Cost of goods sold", gp, sales, "#b91c1c"), ("Gross profit", 0, gp, "#0f766e"), ("Expenses", npf, gp, "#b91c1c"), ("Net profit", 0, npf, "#0f766e")]
f = Fig(300, 240)
f.text(150, 14, "Trading and Profit and Loss account", size=10.5, color=NAVY, bold=True)
x0, sc = 118, 150 / 500.0
for i, (lab, lo, hi, col) in enumerate(rows):
    y = 26 + i * 30
    f.text(112, y + 10, lab, size=10.5, color=NAVY, anchor="end", vmid=True)
    f.box(x0 + lo / 1000 * sc, y, (hi - lo) / 1000 * sc, 20, "", fill=col, stroke=col, r=0)
    v = hi - lo
    f.text(x0 + hi / 1000 * sc + 4, y + 10, f"{v / 1000:.0f}", size=10.5, color=col, anchor="start", bold=True, vmid=True)
f.text(150, 188, "COGS = 60 + 320 - 80 = 300", size=10.5, color=SLATE)
f.text(150, 206, "gross margin 40%, net margin 16%", size=10.5, color=TEAL, bold=True)
f.text(150, 224, "expenses 70 + 36 + 14 = 120", size=10.5, color=NAVY)
```

```photogrid label="6.2" cols="2" ratio="1.1" caption="Year-end adjustments always keep the balance sheet in balance. (a) A balance scale: both pans must weigh the same. (b) Four adjustments and their effect on assets (A), liabilities (L) and profit (P): accrued wages of Rs 5,000 raise a liability and cut profit; prepaid insurance of Rs 3,000 raises an asset and lifts profit; depreciation of Rs 14,000 cuts an asset and profit; a provision for doubtful debts of 2% on debtors of Rs 1,00,000 cuts an asset (debtors) by Rs 2,000 and profit by the same. Each line obeys change in A = change in L + change in P. Together assets fall by Rs 13,000, liabilities rise by Rs 5,000 and profit falls by Rs 18,000, and -13,000 = 5,000 - 18,000. A profit of Rs 1,04,000 before adjustments becomes Rs 86,000 after them."
@ photo id="bcafa/scale" cap="A balance scale: both pans equal"
fit 1.1
focus 0.5 0.5
@ svg cap="Effect of each adjustment (rupees)"
adj = [("Accrued wages", 0, 5000, -5000), ("Prepaid insur.", 3000, 0, 3000), ("Depreciation", -14000, 0, -14000), ("Bad-debt prov.", -round(0.02 * 100000), 0, -2000)]
assert all(a == l + p for _, a, l, p in adj)
tA, tL, tP = (sum(r[k] for r in adj) for k in (1, 2, 3))
assert (tA, tL, tP) == (-13000, 5000, -18000) and tA == tL + tP and 104000 + tP == 86000
f = Fig(300, 240)
f.text(150, 14, "change in assets = liabilities + profit", size=10.5, color=NAVY, bold=True)
f.text(142, 34, "A", size=10.5, color=NAVY, bold=True); f.text(200, 34, "L", size=10.5, color=NAVY, bold=True); f.text(262, 34, "P", size=10.5, color=NAVY, bold=True)
def fm(v): return f"{v:+,}" if v else "0"
rows = adj + [("Total", tA, tL, tP)]
for i, (lab, a, l, p) in enumerate(rows):
    y = 48 + i * 30
    tot = i == len(rows) - 1
    if tot: f.line(8, y - 8, 292, y - 8, color=SLATE, sw=1.2)
    f.text(8, y + 8, lab, size=10.5, color=NAVY, anchor="start", bold=True, vmid=True)
    for x, v in ((160, a), (216, l), (280, p)):
        f.text(x, y + 8, fm(v), size=10.5, color="#b91c1c" if v < 0 else ("#0f766e" if v > 0 else SLATE), anchor="end", bold=True, vmid=True)
f.text(150, 214, "every row: A = L + P  (checked in code)", size=10.5, color=TEAL, bold=True)
f.text(150, 230, "profit 1,04,000 -> 86,000", size=10.5, color=RED, bold=True)
```

## 6.10 Summary and exercises

The Trading Account measures gross profit, the Profit and Loss Account measures net profit after operating items and the Balance Sheet reports position; every year-end adjustment has a double effect, and a balancing balance sheet confirms that none was forgotten.

1. Define gross profit, net profit and operating expenses, and state which side of the Trading Account takes closing stock.
2. List the adjustment entries for outstanding wages, prepaid insurance and accrued interest.
3. A debtor balance of Rs 3,00,000 has Rs 10,000 of bad debts to write off, then a 5% provision. Compute the provision and show the balance sheet presentation.
4. Rerun the program with closing stock of Rs 50,000. By how much do gross profit, net profit and capital change?
5. Explain why net profit increases the owner's capital while drawings reduce it.
6. For a company with profit before tax of Rs 8,00,000, compute tax at 25% and the retained profit after a 20% cash dividend on the after-tax profit.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Prepare a trading account and find the gross profit from: opening stock 40,000; purchases 6,00,000; purchases returns 10,000; carriage inwards 5,000; wages 30,000; sales 10,00,000; sales returns 20,000; closing stock 70,000.**

*Purpose.* The trading account shows the gross profit or loss of buying and selling goods; it contains direct costs only.

| Dr | Rs | Cr | Rs |
|---|---|---|---|
| To Opening stock | 40,000 | By Sales | 10,00,000 |
| To Purchases | 6,00,000 | Less returns | (20,000) |
| Less returns | (10,000) | Net sales | 9,80,000 |
| To Carriage inwards | 5,000 | By Closing stock | 70,000 |
| To Wages | 30,000 | | |
| To Gross profit c/d | 3,85,000 | | |
| | 10,50,000 | | 10,50,000 |

Cost of goods sold = 40,000 + 5,90,000 + 5,000 + 30,000 − 70,000 = **Rs 5,95,000**; gross profit = 9,80,000 − 5,95,000 = **Rs 3,85,000** (Figure 6.1). Gross margin = 3,85,000 ÷ 9,80,000 = 39.29%. *Conclusion:* the trading account measures the trader's gross margin before running costs.

**Q2 (5 marks). Explain the year-end adjustments with entries for: salaries outstanding 10,000; rent prepaid 5,000; depreciation 25,000; provision for doubtful debts 2% on debtors of 2,00,000.**

*Principle.* Under the accrual concept, income and expense belong to the period in which they arise. Each adjustment is entered twice, in the income statement and in the balance sheet (Figure 6.3).

| Adjustment | Journal entry | P&L effect | Balance sheet |
|---|---|---|---|
| Salaries due | Dr Salaries 10,000, Cr Outstanding salaries 10,000 | expense rises | current liability |
| Rent prepaid | Dr Prepaid rent 5,000, Cr Rent 5,000 | expense falls | current asset |
| Depreciation | Dr Depreciation 25,000, Cr Furniture 25,000 | expense 25,000 | asset reduced |
| Provision | Dr P&L 4,000, Cr Provision 4,000 | expense 4,000 | debtors shown net 1,96,000 |

Net effect on profit: −10,000 + 5,000 − 25,000 − 4,000 = −34,000 (plus the stock effect in trading). *Conclusion:* adjustments give a true profit and a true position.

**Q3 (10 marks). Explain the final accounts of a trader and of a company. Using the worked example, prepare the income statement and balance sheet.**

*Introduction.* **Final accounts** are the trading account, profit and loss account and balance sheet prepared at the year end after adjustments. They answer two questions: what was the profit, and what is owned and owed.

*Trading and profit and loss account (Figure 6.1).*

| Item | Rs |
|---|---|
| Net sales (10,00,000 − 20,000) | 9,80,000 |
| Cost of goods sold | (5,95,000) |
| **Gross profit** | **3,85,000** |
| Add interest income | 6,000 |
| Salaries (1,10,000 + 10,000) | (1,20,000) |
| Rent (60,000 − 5,000) | (55,000) |
| Depreciation | (25,000) |
| Bad debts | (8,000) |
| Provision for doubtful debts | (4,000) |
| **Net profit** | **1,79,000** |

*Balance sheet (Figure 6.2).*

| Equity and liabilities | Rs | Assets | Rs |
|---|---|---|---|
| Capital 5,00,000 + 1,79,000 − 30,000 | 6,49,000 | Furniture (3,00,000 − 25,000) | 2,75,000 |
| Creditors | 1,10,000 | Closing stock | 70,000 |
| Salaries outstanding | 10,000 | Debtors (2,00,000 − 4,000) | 1,96,000 |
| | | Prepaid rent | 5,000 |
| | | Cash and bank | 2,23,000 |
| **Total** | **7,69,000** | **Total** | **7,69,000** |

*Company accounts.* A company has share capital, reserves and retained earnings in place of capital and drawings. Income tax at 25% on Rs 1,79,000 is Rs 44,750, leaving **profit after tax of Rs 1,34,250**, from which dividends or bonus shares may be paid. Under NFRS the statements are titled Statement of Financial Position, Statement of Profit or Loss and Other Comprehensive Income, Statement of Changes in Equity and Statement of Cash Flows. The Companies Act 2063 requires audited statements.

*Comparison.*

| Point | Trader | Company |
|---|---|---|
| Owner's claim | capital and drawings | share capital, reserves, retained earnings |
| Tax | on owner's income | corporate tax on profit |
| Distribution | drawings | dividend or bonus shares |
| Statements | trading, P&L, balance sheet | NFRS four statements plus notes |
| Audit | optional by size | compulsory |

*Conclusion.* The final accounts tie all the earlier work together: adjusted balances become profit and position, and the balance sheet total (Rs 7,69,000) proves the process.

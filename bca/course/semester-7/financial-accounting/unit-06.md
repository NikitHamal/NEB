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

## 6.8 Summary and exercises

The Trading Account measures gross profit, the Profit and Loss Account measures net profit after operating items and the Balance Sheet reports position; every year-end adjustment has a double effect, and a balancing balance sheet confirms that none was forgotten.

1. Define gross profit, net profit and operating expenses, and state which side of the Trading Account takes closing stock.
2. List the adjustment entries for outstanding wages, prepaid insurance and accrued interest.
3. A debtor balance of Rs 3,00,000 has Rs 10,000 of bad debts to write off, then a 5% provision. Compute the provision and show the balance sheet presentation.
4. Rerun the program with closing stock of Rs 50,000. By how much do gross profit, net profit and capital change?
5. Explain why net profit increases the owner's capital while drawings reduce it.
6. For a company with profit before tax of Rs 8,00,000, compute tax at 25% and the retained profit after a 20% cash dividend on the after-tax profit.

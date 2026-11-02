---
subject: Financial Accounting
grade: BCA Semester 7
unit: 7
title: Ratio Analysis and a Computerised Ledger in SQLite
hours: 6
area: BCA 403 · Financial Accounting · Unit 7
---

Final accounts report numbers; **ratio analysis** gives them meaning. A profit of Rs 1,79,000 means little until it is compared with sales, with the capital invested and with last year's result. Ratios convert statement figures into comparable percentages and multiples so that a bank officer, an investor or a manager can judge liquidity, solvency, profitability and efficiency. In the second half of this unit, the same double-entry rules are implemented as a small relational ledger, which is how every accounting package works internally.

::: key What this unit gives you
- The four families of ratio: liquidity, solvency, profitability and turnover (activity).
- The DuPont identity: ROE = net margin × asset turnover × equity multiplier.
- All ratios computed from the Unit 6 statements and cross-checked.
- A SQLite double-entry ledger with constraints and a trial-balance query.
:::

## 7.1 Why ratios, and their limits

Ratios allow comparison over time (trend analysis), across firms (peer comparison) and against a standard (budget or industry benchmark). **Common-size statements** express every line as a percentage of sales (income statement) or total assets (balance sheet). Their limits matter: ratios use historical costs, depend on accounting policies (FIFO vs average changes inventory and profit), may be window-dressed at year end, and mean little without context such as seasonality and industry.

## 7.2 Data used

All ratios below use the Unit 6 trader: net sales Rs 9,80,000; cost of goods sold Rs 5,95,000; gross profit Rs 3,85,000; net profit Rs 1,79,000; current assets (stock 70,000, debtors net 1,96,000, prepaid 5,000, cash 2,23,000) Rs 4,94,000; current liabilities (creditors 1,10,000 and outstanding salaries 10,000) Rs 1,20,000; total assets Rs 7,69,000; closing equity Rs 6,49,000; average stock (40,000 + 70,000) ÷ 2 = Rs 55,000; debtors Rs 2,00,000.

## 7.3 Liquidity ratios

**Current ratio** = current assets ÷ current liabilities, the ability to meet short-term obligations. A traditional benchmark of 2:1 is a rule of thumb, not a law.

**Quick (acid-test) ratio** = (current assets − stock − prepaid) ÷ current liabilities, which excludes the least liquid items. Here quick assets are debtors and cash, Rs 4,19,000, so the quick ratio is 419,000 ÷ 120,000.

## 7.4 Solvency (leverage) ratios

**Debt-to-equity** = total outside liabilities ÷ equity: how much of the financing comes from creditors per rupee of owners' funds. **Interest coverage** = profit before interest and tax ÷ interest expense: how many times the earnings cover the interest. **Equity multiplier** = total assets ÷ equity, used in DuPont. A low ratio signals safety but may also indicate under-use of cheap borrowing.

## 7.5 Profitability ratios

- **Gross profit margin** = gross profit ÷ net sales.
- **Net profit margin** = net profit ÷ net sales.
- **Return on assets (ROA)** = net profit ÷ total assets.
- **Return on equity (ROE)** = net profit ÷ equity.
- For a company: **earnings per share (EPS)** = profit after tax ÷ shares outstanding, and **price/earnings (P/E)** = market price ÷ EPS.

## 7.6 Turnover (activity) ratios

**Inventory turnover** = COGS ÷ average inventory, and *inventory days* = 365 ÷ turnover. **Debtor days** = debtors ÷ credit sales × 365, the average collection period. **Creditor days** = creditors ÷ credit purchases × 365. **Asset turnover** = net sales ÷ total assets. The **cash conversion cycle** = inventory days + debtor days − creditor days, the time cash stays locked in operations.

```python
net_sales, cogs, gross, net_profit = 980000, 595000, 385000, 179000
current_assets, quick_assets, current_liab = 494000, 419000, 120000
equity, total_assets, avg_stock = 649000, 769000, 55000
print(f"current ratio {current_assets / current_liab:.2f}, quick ratio {quick_assets / current_liab:.2f}")
print(f"debt to equity {current_liab / equity:.2f}")
print(f"gross margin {gross / net_sales * 100:.2f}%, net margin {net_profit / net_sales * 100:.2f}%")
nm, at, em = net_profit / net_sales, net_sales / total_assets, total_assets / equity
roe = nm * at * em
print(f"ROE {roe * 100:.2f}% = {nm:.4f} x {at:.4f} x {em:.4f}")
turns = cogs / avg_stock
print(f"inventory turnover {turns:.2f} times, {365 / turns:.1f} days")
print(f"debtor days {200000 / net_sales * 365:.1f}")
```
```output
current ratio 4.12, quick ratio 3.49
debt to equity 0.18
gross margin 39.29%, net margin 18.27%
ROE 27.58% = 0.1827 x 1.2744 x 1.1849
inventory turnover 10.82 times, 33.7 days
debtor days 74.5
```
The current ratio of 4.12 and quick ratio of 3.49 show very comfortable liquidity, perhaps too much idle cash (Rs 2,23,000, or 29% of assets). Debt-to-equity of 0.18 means creditors fund only about 18 paisa for every rupee of equity. Gross margin is 39.29% and net margin 18.27%. Stock is turned over 10.82 times a year (about 33.7 days), but debtors take 74.5 days to pay, which is slow relative to stock days and is the first place to look to release cash.

## 7.7 The DuPont identity

Return on equity can be decomposed:

::: key DuPont identity
**ROE = Net margin × Asset turnover × Equity multiplier**, that is (NP ÷ Sales) × (Sales ÷ Assets) × (Assets ÷ Equity). The sales and asset terms cancel algebraically, leaving NP ÷ Equity.
:::

The product above gives ROE of 27.58%. ROA is 23.28% and asset turnover 1.2744. DuPont tells *why* ROE is what it is: through high margins (pricing power), through fast asset use (efficiency) or through leverage (financial risk). Two firms with the same ROE may have very different risk profiles.

::: example Reading a DuPont result
A supermarket may show net margin of 3%, asset turnover of 4 and an equity multiplier of 2.5: ROE = 0.03 × 4 × 2.5 = 30%. A jeweller may reach the same 30% with margin 15%, turnover 0.8 and multiplier 2.5. The first competes on volume, the second on margin.
:::

## 7.8 A computerised double-entry ledger

Accounting software such as the packages commonly used by Nepali businesses (and the VAT billing systems that the Inland Revenue Department expects registered taxpayers to use) is a database underneath. The design keeps the three ideas of double entry:

1. **Chart of accounts:** a table of account names and their kinds.
2. **Entry and lines:** one header per transaction and two or more lines, each with a debit or a credit amount.
3. **Constraints:** an amount cannot be negative, a line is either a debit or a credit, and the sum of debits equals the sum of credits for each entry.

SQLite can enforce the first two with `CHECK` constraints and foreign keys; the third is checked with an aggregate query (or by posting the whole entry in one transaction after validating it in application code). The program loads the six entries of Unit 2 and produces the trial balance with SQL.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = ON")
con.executescript("""
CREATE TABLE account(name TEXT PRIMARY KEY,
  kind TEXT NOT NULL CHECK(kind IN ('asset','liability','equity','income','expense')));
CREATE TABLE entry(id INTEGER PRIMARY KEY, narration TEXT NOT NULL);
CREATE TABLE line(entry_id INTEGER NOT NULL REFERENCES entry(id),
  account TEXT NOT NULL REFERENCES account(name),
  debit INTEGER NOT NULL DEFAULT 0, credit INTEGER NOT NULL DEFAULT 0,
  CHECK(debit >= 0 AND credit >= 0 AND (debit = 0 OR credit = 0)));
""")
kinds = {"Cash": "asset", "Debtors": "asset", "VAT Input": "asset", "Purchases": "expense", "Rent": "expense",
         "Capital": "equity", "Creditors (Himal)": "liability", "Sales": "income",
         "VAT Output": "liability", "TDS Payable": "liability"}
con.executemany("INSERT INTO account VALUES (?, ?)", kinds.items())
entries = [
    ("capital", [("Cash", 500000, 0), ("Capital", 0, 500000)]),
    ("purchase", [("Purchases", 100000, 0), ("VAT Input", 13000, 0), ("Creditors (Himal)", 0, 113000)]),
    ("sale", [("Debtors", 226000, 0), ("Sales", 0, 200000), ("VAT Output", 0, 26000)]),
    ("rent", [("Rent", 50000, 0), ("TDS Payable", 0, 5000), ("Cash", 0, 45000)]),
    ("receipt", [("Cash", 150000, 0), ("Debtors", 0, 150000)]),
    ("payment", [("Creditors (Himal)", 113000, 0), ("Cash", 0, 113000)]),
]
for i, (narr, lines) in enumerate(entries, 1):
    con.execute("INSERT INTO entry VALUES (?, ?)", (i, narr))
    con.executemany("INSERT INTO line VALUES (?, ?, ?, ?)", [(i, a, d, c) for a, d, c in lines])
bad = con.execute("SELECT entry_id FROM line GROUP BY entry_id HAVING SUM(debit) <> SUM(credit)").fetchall()
rows = con.execute("SELECT account, SUM(debit) - SUM(credit) FROM line GROUP BY account").fetchall()
debits = sum(b for _, b in rows if b > 0)
credits = -sum(b for _, b in rows if b < 0)
print(f"sqlite trial balance: debits={debits} credits={credits} balanced={debits == credits and not bad}")
try:
    con.execute("INSERT INTO line VALUES (1, 'Cash', -5, 0)")
except sqlite3.IntegrityError:
    print("negative amount rejected by CHECK")
```
```output
sqlite trial balance: debits=731000 credits=731000 balanced=True
negative amount rejected by CHECK
```
The output shows the trial balance agreeing at Rs 731,000, the same total as the manual ledger of Unit 2. The final lines show a database constraint refusing an impossible line. A production system adds immutability (corrections made by reversing entries, never by editing), a user and timestamp on each entry for the **audit trail**, period locking after the books are closed, and controls that stop one person from both entering and approving a payment.

::: caution
A balanced ledger is not a correct ledger. The software prevents arithmetic errors, not errors of principle or commission: posting a sale to the wrong customer still balances. Controls and review remain human responsibilities.
:::

## 7.9 Summary and exercises

Ratios turn statements into evidence about liquidity, solvency, profitability and efficiency; DuPont explains return on equity as margin, turnover and leverage; and a computerised ledger is the same double-entry discipline expressed as tables and constraints.

1. Compute current and quick ratios if current assets are Rs 6,00,000 (stock 2,40,000) and current liabilities Rs 3,00,000. Comment.
2. Given net sales Rs 12,00,000, net profit Rs 1,50,000, total assets Rs 10,00,000 and equity Rs 6,00,000, compute ROE through DuPont.
3. Define debtor days and explain what a rise from 45 to 74 days implies for cash flow.
4. Why can two firms with identical ROE have different risk?
5. Extend the SQLite schema with a date column and write a query for the balance of Cash at the end of a given month.
6. Explain why an accounting system should correct errors by reversing entries rather than by editing history.

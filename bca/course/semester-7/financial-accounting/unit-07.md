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

## 7.9 Seeing the ideas: the ratio dashboard, the DuPont tree and the database ledger

```photogrid label="7.1" cols="2" ratio="1.0" caption="(a) Source code on a screen: a modern ledger is a program with a rule built in, that every entry must balance. (b) The three-table design of the unit's SQLite ledger: an account has a kind, an entry has a narration, and each line belongs to one entry and one account with a debit or a credit, never both."
@ photo id="bca306/code" cap="Code on a screen"
fit 1.0
focus 0.5 0.5
@ svg cap="Ledger tables"
f = Fig(300, 300)
f.box(10, 10, 130, 90, "account\nname (PK)\nkind: asset,\nliability, equity,\nincome, expense", fill=MINT, stroke=TEAL, size=12.5)
f.box(160, 10, 130, 90, "entry\nid (PK)\nnarration", fill=BLUE, stroke=NAVY, size=12.5)
f.box(60, 160, 180, 100, "line\nentry_id (FK)\naccount (FK)\ndebit, credit\nCHECK one side is 0", fill=SAND, stroke=AMBER, size=12.5)
f.arrow([(75, 160), (75, 100)], color=SLATE, label="many", lpos=(100, 132), lsize=12)
f.arrow([(225, 160), (225, 100)], color=SLATE, label="many", lpos=(250, 132), lsize=12)
f.text(150, 284, "debits = credits is checked per entry", size=12.5, color=TEAL, italic=True)
```

```svgfig label="7.1" caption="A ratio dashboard for the worked trader of Unit 6: liquidity, solvency, profitability and activity. Each tile gives the formula and the value, and a comment on what it says about the business."
f = Fig(580, 262)
T = [("LIQUIDITY", "Current ratio\nCA / CL = 4.94 / 1.20 lakh", "= 4.12", "Quick ratio = 3.49", MINT, TEAL), ("SOLVENCY", "Debt / equity\n1.20 / 6.49 lakh", "= 0.18", "creditors fund little", BLUE, NAVY), ("PROFITABILITY", "Gross margin 39.29%\nNet margin 18.27%", "ROE 27.58%", "return on owner's money", SAND, AMBER), ("ACTIVITY", "Inventory turnover\nDebtor days", "10.82 times\n74.5 days", "stock 33.7 days", ROSE, RED)]
for i, (h, a, v, c, fl, st) in enumerate(T):
    x = 8 + (i % 2) * 288; y = 8 + (i // 2) * 124
    f.box(x, y, 276, 116, "", fill=fl, stroke=st)
    f.text(x + 138, y + 18, h, size=12.5, color=st, bold=True)
    f.text(x + 138, y + 50, a, size=11, color=SLATE)
    f.text(x + 138, y + 84, v, size=14, color=NAVY, bold=True)
    f.text(x + 138, y + 106, c, size=10.5, color=st, italic=True)
```

```svgfig label="7.2" caption="The DuPont tree. Return on equity is the product of three simple ratios, so a low ROE can be traced to margin, turnover or borrowing: 0.1827 x 1.2744 x 1.1849 = 0.2758."
f = Fig(580, 214)
f.box(190, 8, 200, 40, "ROE = 27.58%", fill=NAVY, color="#ffffff", bold=True, size=14)
for x, t, v, fl, st in [(24, "Net margin\nprofit / sales", "18.27%", MINT, TEAL), (210, "Asset turnover\nsales / assets", "1.2744", BLUE, NAVY), (396, "Leverage\nassets / equity", "1.1849", SAND, AMBER)]:
    f.arrow([(290, 48), (x + 80, 80)], color=SLATE)
    f.box(x, 80, 160, 50, t, fill=fl, stroke=st, size=11.5)
    f.box(x + 40, 140, 80, 30, v, fill="#ffffff", stroke=st, bold=True, size=13)
f.text(204, 156, "x", size=18, color=SLATE, bold=True); f.text(390, 156, "x", size=18, color=SLATE, bold=True)
f.text(290, 198, "profit per rupee of sales  x  sales per rupee of assets  x  assets per rupee of owner's money", size=10.5, color=SLATE, italic=True)
```

### 7.9.1 Eight uses of ratio analysis and computerised accounting

1. **Banks judge repayment ability.** A current ratio of 4.12 and a debt-to-equity of 0.18 tell a lender that the firm can pay its short debts and borrows little. These are the first numbers a credit officer reads. A weak ratio can lead to a smaller loan.
2. **Owners see where profit is made.** Gross margin of 39.29% and net margin of 18.27% show how much of each rupee of sales is kept. A fall in gross margin points at buying cost or pricing, while a fall in net margin points at running costs. The owner knows where to act.
3. **Managers control working capital.** Inventory turnover of 10.82 times and debtor days of 74.5 show how fast stock sells and money is collected. Debtor days of 74.5 are long, so collection needs attention. Faster collection frees cash without any new sales.
4. **Investors compare firms.** ROE and earnings per share let an investor compare a bank with a hydropower company on the same scale. Ratios remove the effect of size. They must still be compared within one industry.
5. **DuPont explains return.** Splitting ROE into margin, turnover and leverage shows whether a high return comes from skill or from risky borrowing. A firm can raise ROE by borrowing, but the risk also rises. This is a diagnostic, not a target.
6. **Trends reveal problems early.** One year's ratio means little; five years show direction. A current ratio sliding from 3 to 1.2 warns of a cash squeeze. Trend lines are the early-warning system for trouble.
7. **Software enforces double entry.** A database ledger can reject any entry where debits and credits differ, as the SQLite schema does with its CHECK rule. The trial balance then always agrees, here at Rs 7,31,000. Errors of principle and commission still need people.
8. **Computerised books save time and give audit trails.** A system such as a Nepali tax-compliant billing package posts a sale to Sales, VAT Output and Debtors at once and keeps a log of who did what. Reports come at a click. The business gains speed, but only if the first entry is correct.

```photogrid label="7.2" cols="2" ratio="1.2" caption="How long money is stuck in the business. (a) A well-stocked shelf looks like wealth, but every packet on it is cash already spent that has not yet come back. (b) For an invented general store with yearly sales of Rs 24 million, cost of goods of Rs 18 million, stock of Rs 3 million, receivables of Rs 2 million and payables of Rs 1.5 million, stock stays 60.8 days (DIO), customers take 30.4 days to pay (DSO) and the shop takes 30.4 days to pay its suppliers (DPO). The cash conversion cycle is DIO + DSO - DPO = 60.8 days. Collecting from customers 10 days faster would free Rs 657,534 of cash without a single extra sale, which is why a ratio table is a management tool and not only a school exercise. All figures are invented for the exercise."
@ photo id="bcafa/shelf" cap="Stock on the shelf is money that cannot be spent"
fit 1.2
focus 0.5 0.5
@ svg cap="Cash conversion cycle of a general store"
sales, cogs = 24000000, 18000000
inv, rec, pay = 3000000, 2000000, 1500000
dio = inv / cogs * 365
dso = rec / sales * 365
dpo = pay / cogs * 365
ccc = dio + dso - dpo
free = sales / 365 * 10
assert round(ccc, 1) == 60.8 and round(free) == 657534
facts = dict(dio=round(dio, 1), dso=round(dso, 1), dpo=round(dpo, 1), ccc=round(ccc, 1), free=format(round(free), ","))
f = Fig(300, 236)
f.text(150, 12, "days a rupee is tied up (invented store)", size=10.5, color=NAVY, bold=True)
sc = 2.0
f.text(6, 38, "inventory", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(96, 28, dio * sc, 20, "%.1f days" % dio, fill=BLUE, stroke=NAVY, size=10.5, r=3, sw=1)
f.text(6, 68, "receivables", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(96 + dio * sc, 58, dso * sc, 20, "%.1f" % dso, fill="#fde68a", stroke=AMBER, size=10.5, r=3, sw=1)
f.text(6, 98, "payables", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(96, 88, dpo * sc, 20, "%.1f days" % dpo, fill="#bbf7d0", stroke=TEAL, size=10.5, r=3, sw=1)
f.line(96, 120, 96 + ccc * sc, 120, color=RED, sw=3)
f.text(96 + ccc * sc / 2, 136, "cash cycle = %.1f days" % ccc, size=10.5, color=RED, bold=True)
f.text(150, 160, "CCC = DIO + DSO - DPO", size=10.5, color=NAVY, bold=True)
f.text(150, 182, "collect 10 days faster:", size=10.5, color=NAVY, bold=True)
f.text(150, 200, "Rs %s freed" % format(round(free), ","), size=12, color=TEAL, bold=True)
f.text(150, 222, "(sales Rs 24 million a year, assumed)", size=10.5, color=SLATE)
```

## 7.10 Summary and exercises

Ratios turn statements into evidence about liquidity, solvency, profitability and efficiency; DuPont explains return on equity as margin, turnover and leverage; and a computerised ledger is the same double-entry discipline expressed as tables and constraints.

1. Compute current and quick ratios if current assets are Rs 6,00,000 (stock 2,40,000) and current liabilities Rs 3,00,000. Comment.
2. Given net sales Rs 12,00,000, net profit Rs 1,50,000, total assets Rs 10,00,000 and equity Rs 6,00,000, compute ROE through DuPont.
3. Define debtor days and explain what a rise from 45 to 74 days implies for cash flow.
4. Why can two firms with identical ROE have different risk?
5. Extend the SQLite schema with a date column and write a query for the balance of Cash at the end of a given month.
6. Explain why an accounting system should correct errors by reversing entries rather than by editing history.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Current assets are Rs 6,00,000 (stock 2,40,000) and current liabilities Rs 3,00,000. Compute the current and quick ratios and comment.**

*Formulae.* Current ratio = current assets ÷ current liabilities. Quick (acid-test) ratio = (current assets − stock) ÷ current liabilities.

*Working.* Current ratio = 6,00,000 ÷ 3,00,000 = **2.0 : 1**. Quick assets = 6,00,000 − 2,40,000 = 3,60,000, so quick ratio = 3,60,000 ÷ 3,00,000 = **1.2 : 1**.

*Comment.* The usual norms are 2 : 1 and 1 : 1. Both are met, so the firm can pay short-term debts even without selling its stock. A very high ratio, such as the 4.12 of the worked trader, would suggest idle cash. The quick ratio is a harsher test because stock may be slow to sell. *Conclusion:* liquidity is satisfactory, and the figures should be compared with the industry and with past years.

**Q2 (5 marks). Explain the DuPont identity with the worked example.**

*Identity.* Return on equity = net margin × asset turnover × financial leverage, that is (profit ÷ sales) × (sales ÷ assets) × (assets ÷ equity) (Figure 7.2).

*Worked trader.* Net profit 1,79,000; sales 9,80,000; assets 7,69,000; equity 6,49,000.

| Factor | Working | Value |
|---|---|---|
| Net margin | 1,79,000 ÷ 9,80,000 | 18.27% |
| Asset turnover | 9,80,000 ÷ 7,69,000 | 1.2744 |
| Leverage | 7,69,000 ÷ 6,49,000 | 1.1849 |
| **ROE** | 0.1827 × 1.2744 × 1.1849 | **27.58%** |

*Use.* A firm can raise ROE by improving margin (price, cost control), turnover (using assets harder) or leverage (borrowing). The third raises risk. Here the return comes mainly from margin and turnover, with very little borrowing (debt-to-equity 0.18). *Conclusion:* DuPont shows why ROE is high or low, not only how much it is.

**Q3 (10 marks). Classify financial ratios and explain each class with the worked trader. State the limitations of ratio analysis. How does a computerised ledger enforce double entry?**

*Introduction.* **Ratio analysis** turns the figures of financial statements into relationships that show liquidity, solvency, profitability and efficiency. It is used by owners, lenders and investors (Figure 7.1).

*Classes with the worked trader (balance sheet total Rs 7,69,000).*

| Class | Ratio | Formula | Value | Meaning |
|---|---|---|---|---|
| Liquidity | Current | CA ÷ CL = 4,94,000 ÷ 1,20,000 | 4.12 | very comfortable, perhaps idle cash |
| Liquidity | Quick | (CA − stock − prepaid) ÷ CL | 3.49 | strong |
| Solvency | Debt to equity | liabilities ÷ equity = 1,20,000 ÷ 6,49,000 | 0.18 | little borrowing |
| Profitability | Gross margin | 3,85,000 ÷ 9,80,000 | 39.29% | healthy |
| Profitability | Net margin | 1,79,000 ÷ 9,80,000 | 18.27% | healthy |
| Profitability | ROE | profit ÷ equity | 27.58% | high |
| Activity | Inventory turnover | COGS ÷ stock = 5,95,000 ÷ 55,000 average | 10.82 times (33.7 days) | stock moves quickly |
| Activity | Debtor days | debtors ÷ sales × 365 | 74.5 days | slow collection |

*Limitations.* (1) Ratios are based on historical cost, so inflation distorts them. (2) Accounting policies (FIFO versus average, depreciation method) change the figures. (3) A year-end balance sheet may not represent the whole year, for example seasonal stock. (4) Ratios compare numbers, not quality such as management or customer loyalty. (5) They are useful only against benchmarks: past years, competitors and the industry. (6) Window dressing can improve ratios on one date.

*Computerised ledger.* The unit's database has three tables: account (name and kind), entry (narration) and line (entry, account, debit, credit). A CHECK rule rejects a negative amount or a line with both a debit and a credit. Each entry is verified to have equal total debits and credits before saving, so the trial balance always agrees (Rs 7,31,000 in the example, as in the manual ledger of Unit 2). Reports are queries. The log of who posted what gives an audit trail.

*Caution.* A balanced ledger is not a correct ledger. Posting a sale to the wrong customer still balances. Controls, review and reconciliation (Unit 4) are still needed.

*Comparison of manual and computerised ledgers.*

| Point | Manual | Computerised |
|---|---|---|
| Arithmetic errors | possible | prevented by rules |
| Speed of reports | slow | immediate |
| Audit trail | handwriting | automatic log |
| Errors of principle | possible | still possible |
| Cost | stationery | software and training |

*Conclusion.* Ratios turn statements into evidence, DuPont explains return, and software makes the arithmetic of the books reliable, while correct judgement still has to come from the accountant.

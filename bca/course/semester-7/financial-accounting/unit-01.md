---
subject: Financial Accounting
grade: BCA Semester 7
unit: 1
title: Conceptual Framework of Accounting, GAAP, NFRS and the Accounting Equation
hours: 5
area: BCA 403 · Financial Accounting · Unit 1
---

A momo shop in Baneshwor sells a few hundred plates a day. By Friday the owner cannot say whether the week made a profit, how much she owes the flour supplier, or whether the cash in the drawer is hers or the business's. **Accounting** is the discipline that answers those questions in a standard, auditable way: it identifies, measures, records and communicates economic information so that owners, lenders, the Inland Revenue Department and investors can decide. This unit builds the vocabulary and the single equation on which every later unit rests.

::: key What this unit gives you
- What accounting is, who uses its output, and the difference between book-keeping and accounting.
- The accounting principles and concepts (GAAP), and how Nepal's NFRS, based on IFRS, sits on top of them.
- The accounting equation A = L + E and how each transaction keeps it balanced.
- The double-entry principle: every transaction has two equal and opposite effects.
:::

## 1.1 Accounting, book-keeping and users

**Book-keeping** is the mechanical recording of transactions. **Accounting** goes further: it classifies, summarises, interprets and reports. The process runs in a cycle: *transaction → source document → journal → ledger → trial balance → adjustments → financial statements → closing*.

Users of accounting information fall into two groups. *Internal users* are owners and managers who need detail for control. *External users* are lenders, suppliers, employees, tax authorities, regulators and prospective investors who need general-purpose statements. The Nepal Rastra Bank, for example, relies on audited statements when licensing and supervising a commercial bank, and the Inland Revenue Department assesses income tax on profit that must be traceable to books.

## 1.2 Branches and the nature of business transactions

Financial accounting reports to outsiders; **cost accounting** measures the cost of products and services; **management accounting** supports internal decisions. Only transactions that can be **measured in money** and that change a business's resources or obligations are recorded. Hiring a brilliant chef is not recorded, but paying her salary is.

::: note
A transaction is *external* when it involves another party (buying goods, paying rent) and *internal* when it only moves value inside the business (using stock for the owner's personal use is treated as drawings, which is external to the business entity).
:::

## 1.3 Accounting concepts and GAAP

**Generally Accepted Accounting Principles (GAAP)** are the rules and conventions that make statements comparable. The core concepts are these.

1. **Business entity.** The business is separate from its owner. The owner's money in the till is the business's money only when invested; withdrawals are *drawings*.
2. **Money measurement.** Only monetary facts are recorded.
3. **Going concern.** Statements assume the entity will continue, so assets are not valued at fire-sale prices.
4. **Cost concept.** Assets are recorded at historical cost; a plot bought at Rs 8,00,000 stays at that figure even if the market moves (revaluation is allowed only where a standard permits it).
5. **Accounting period.** Profit is measured over a fixed period. Nepal's fiscal year runs from Shrawan 1 to Ashad end (mid-July to mid-July).
6. **Dual aspect.** Each transaction affects two accounts, which gives the accounting equation.
7. **Revenue recognition and matching.** Revenue is recognised when earned, not when cash arrives; expenses are matched to the revenue they helped earn (accrual basis).
8. **Conservatism and consistency.** Anticipate no profit but provide for all probable losses; apply the same methods year after year.
9. **Materiality and full disclosure.** Trivial items need not be reported separately, while anything that could change a user's decision must be disclosed.

::: caution
Cash-basis and accrual-basis profit differ. A shop that delivers goods in Chaitra and is paid in Baisakh has earned the revenue in the Chaitra year. Beginners who record revenue only on cash receipt misstate both years.
:::

## 1.4 Accounting standards, NFRS and IFRS in Nepal

Standards turn broad principles into detailed rules. The International Accounting Standards Board issues **IFRS**. Nepal's **Accounting Standards Board (ASB)**, formed under the Nepal Chartered Accountants Act, develops the **Nepal Financial Reporting Standards (NFRS)**, which are adopted from IFRS. The Institute of Chartered Accountants of Nepal (ICAN) is the professional body. NFRS applies in full to public-interest entities such as banks, insurers and listed companies, while a simplified version (NFRS for SMEs) exists for smaller entities; check the current notice from the ASB for the exact scope and dates, because they have been revised.

Practical consequences you will meet in this course:

- Financial statements are titled *Statement of Financial Position*, *Statement of Profit or Loss and Other Comprehensive Income*, *Statement of Changes in Equity* and *Statement of Cash Flows*, with notes. The classic *Balance Sheet* and *Profit and Loss Account* in this book are the same ideas in older vocabulary.
- Nepal's Companies Act 2063 requires a company to keep books, prepare annual accounts and have them audited.
- Tax rules are separate from accounting rules: the Income Tax Act 2058 decides the taxable profit, and the difference is reconciled in a tax computation.

## 1.5 The accounting equation

At every instant a business's resources are financed by someone. **Assets** are resources controlled by the business that are expected to bring future benefits (cash, stock, furniture). **Liabilities** are obligations to outsiders (creditors, loans). **Equity** (capital, owner's equity) is what remains for the owner:

::: key The accounting equation
**Assets = Liabilities + Equity**, or equivalently **Equity = Assets − Liabilities**. Equity increases with capital introduced and profit, and decreases with drawings and loss.
:::

Every transaction changes at least two items, in a way that leaves both sides equal. The program below tracks six transactions of a small trading business: the owner invests Rs 5,00,000 cash; furniture is bought for Rs 1,20,000 cash; goods worth Rs 80,000 are bought on credit; goods costing Rs 40,000 are sold for Rs 60,000 cash; rent of Rs 10,000 is paid; and Rs 50,000 is paid to the creditor. Each row lists the effect on assets (ΔA), liabilities (ΔL) and equity (ΔE).

```python
txns = [
    ("owner invests cash",            +500000,       0, +500000),
    ("furniture bought for cash",           0,       0,       0),
    ("goods bought on credit",         +80000,  +80000,       0),
    ("goods cost 40000 sold for 60000", +20000,       0,  +20000),
    ("rent paid in cash",              -10000,       0,  -10000),
    ("creditor paid in cash",          -50000,  -50000,       0),
]
A = L = E = 0
for i, (what, dA, dL, dE) in enumerate(txns, 1):
    A += dA; L += dL; E += dE
    assert A == L + E, what
    print(f"step {i}: A={A} L={L} E={E}")
```
```output
step 1: A=500000 L=0 E=500000
step 2: A=500000 L=0 E=500000
step 3: A=580000 L=80000 E=500000
step 4: A=600000 L=80000 E=520000
step 5: A=590000 L=80000 E=510000
step 6: A=540000 L=30000 E=510000
```
The furniture purchase changes the *composition* of assets (cash down, furniture up) but not the total, so all three deltas are zero. After step 6 assets are Rs 540,000, liabilities Rs 30,000 and equity Rs 510,000, so 540,000 = 30,000 + 510,000 holds. The assertion inside the loop is a miniature *integrity check*: if any entry broke the equation, the program would stop.

::: example Worked example
A business has assets of Rs 9,00,000 and liabilities of Rs 3,50,000. The owner's equity is 9,00,000 − 3,50,000 = Rs 550,000. If the owner now withdraws Rs 50,000 cash for personal use, assets fall to 8,50,000 and equity to 5,00,000, and the equation still balances.
:::

## 1.6 Double-entry principle and account types

Under **double entry**, every transaction has a *debit* aspect and a *credit* aspect of equal amount. **Debit** means the left side of an account and **credit** the right side; neither word means "good" or "bad". The effect depends on account type:

| Account type | Increases with | Decreases with | Normal balance |
|---|---|---|---|
| Asset | Debit | Credit | Debit |
| Expense / loss | Debit | Credit | Debit |
| Liability | Credit | Debit | Credit |
| Equity / capital | Credit | Debit | Credit |
| Income / gain | Credit | Debit | Credit |

The memory aid is that the equation's left side (assets) and expenses, which reduce equity, are debit-natured, while the right side and income, which raise equity, are credit-natured. Double entry is powerful because it is self-checking: the total of all debit balances must equal the total of all credit balances (the trial balance of Unit 3). It cannot, however, detect an error that is made on both sides equally.

## 1.7 Summary and exercises

Accounting turns economic events into reliable reports under a shared body of principles; Nepal anchors those principles in NFRS; and the equation A = L + E together with double entry makes the records self-balancing.

1. Distinguish book-keeping from accounting, and list four external users of financial statements.
2. State any five accounting concepts and give one Nepali business example of each.
3. Explain why the cost concept and the going-concern concept can conflict with a market-value view of assets.
4. A trader starts with Rs 2,00,000 cash, buys stock on credit for Rs 50,000 and pays rent of Rs 8,000. Show the equation after each step.
5. Why is a debit not always an increase? Illustrate with a liability account.
6. Differentiate NFRS from the Income Tax Act as a source of rules for profit measurement.

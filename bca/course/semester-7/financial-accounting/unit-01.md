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

## 1.7 Qualitative characteristics and accounting policies

**Qualitative characteristics** are the qualities that make financial information useful. The IASB framework that NFRS follows names two **fundamental** characteristics and four **enhancing** ones.

| Type | Characteristic | Meaning |
|---|---|---|
| Fundamental | **Relevance** | Information can change a decision: it has predictive or confirmatory value and is material. |
| Fundamental | **Faithful representation** | Complete, neutral and free from error; it shows what it claims to show. |
| Enhancing | Comparability | Users can compare one period or one firm with another. |
| Enhancing | Verifiability | Independent people would agree that it is faithful. |
| Enhancing | Timeliness | Available in time to influence a decision. |
| Enhancing | Understandability | Clear and concise for a user with reasonable knowledge. |

**Fundamental accounting assumptions** are two: the **accrual basis** (effects of transactions are recorded when they occur, not when cash moves) and the **going concern** assumption (the business will continue for the foreseeable future, so assets are not valued as if it were closing down).

**Accounting policies** are the specific principles, bases and practices a business applies in preparing its statements: the depreciation method, the inventory formula (FIFO or weighted average), how revenue is recognised, how doubtful debts are provided for. **Selection:** the policy should give relevant and faithful information and be applied consistently; where an NFRS applies to an item, it must be followed. **Change:** a policy may be changed only if the standard requires it or the change gives more reliable and relevant information; the effect is applied **retrospectively** (as if the new policy had always been used) and the change and its effect are **disclosed** in the notes. A change of an *estimate* (for example a new useful life) is different: it is applied from now on, not backdated.

Example: a shop switched from FIFO to weighted-average inventory. It must restate the opening inventory and the previous year's profit as if weighted average had always been used, and disclose both figures.

## 1.8 Seeing the ideas: records, equation and cycle

```photogrid label="1.1" cols="3" ratio="1.0" caption="Three generations of the accounting record. (a) A handwritten merchant ledger of 1855: every customer has a debit entry with date, particulars and amount, exactly the discipline of double entry. (b) An antique mechanical cash register: it records each sale at the moment it happens, the source of the day's cash-book total. (c) A bank cheque of 1909: a source document that proves a payment and starts a journal entry."
@ photo id="bca403/ledger2" cap="Merchant ledger, 1855"
fit 1.0
focus 0.5 0.3
@ photo id="bca403/register" cap="Mechanical cash register"
fit 1.0
focus 0.5 0.55
@ photo id="bca403/cheque" cap="Bank cheque, 1909"
fit 1.0
focus 0.4 0.5
```

```svgfig label="1.1" caption="The accounting equation stays balanced through three transactions. (1) The owner starts with Rs 5,00,000 cash. (2) Furniture of Rs 1,00,000 is bought for cash: one asset replaces another. (3) Stock of Rs 60,000 is bought on credit: assets and liabilities both rise by 60,000. Total assets always equal liabilities plus capital."
f = Fig(580, 262)
k = 0.00025
def stack(x, segs, w=70):
    y = 206
    for lab, v, fl, st in segs:
        h = v * k
        y -= h
        f.box(x, y, w, h, lab, fill=fl, stroke=st, size=9)
P = [("(1) Start", [("Cash 5,00,000", 500000, MINT, TEAL)], [("Capital 5,00,000", 500000, BLUE, NAVY)]), ("(2) Buy furniture", [("Furniture 1,00,000", 100000, SAND, AMBER), ("Cash 4,00,000", 400000, MINT, TEAL)], [("Capital 5,00,000", 500000, BLUE, NAVY)]), ("(3) Stock on credit", [("Stock 60,000", 60000, ROSE, RED), ("Furniture 1,00,000", 100000, SAND, AMBER), ("Cash 4,00,000", 400000, MINT, TEAL)], [("Creditors 60,000", 60000, ROSE, RED), ("Capital 5,00,000", 500000, BLUE, NAVY)])]
for i, (t, L, R) in enumerate(P):
    x0 = 12 + i * 192
    stack(x0, L); stack(x0 + 90, R)
    f.text(x0 + 80, 18, t, size=11.5, color=NAVY, bold=True)
    
    f.text(x0 + 35, 222, "Assets", size=10.5, color=SLATE, bold=True)
    f.text(x0 + 125, 222, "Liabilities + Capital", size=10, color=SLATE, bold=True)
    tot = sum(v for _, v, _, _ in L)
    f.text(x0 + 80, 244, "Rs {:,} = Rs {:,}".format(tot, tot), size=10.5, color=TEAL, bold=True)
```

```svgfig label="1.2" caption="The accounting cycle. A transaction is recognised from a source document, journalised, posted to the ledger and summarised in a trial balance; adjustments and closing entries lead to the final accounts, and the next year opens with the closing balances."
f = Fig(580, 168)
S = [("Source\ndocument", MINT, TEAL), ("Journal", BLUE, NAVY), ("Ledger", BLUE, NAVY), ("Trial\nbalance", SAND, AMBER), ("Adjust-\nments", SAND, AMBER), ("Final\naccounts", ROSE, RED)]
for i, (t, fl, st) in enumerate(S):
    x = 8 + i * 96
    f.box(x, 18, 80, 46, t, fill=fl, stroke=st, bold=True, size=11)
    if i < 5: f.arrow([(x + 80, 41), (x + 96, 41)])
f.text(48, 80, "bill, cheque,\nvoucher", size=10, color=SLATE)
f.text(144, 80, "first record,\ndate order", size=10, color=SLATE)
f.text(240, 80, "grouped by\naccount", size=10, color=SLATE)
f.text(336, 80, "checks debits\n= credits", size=10, color=SLATE)
f.text(432, 80, "accruals,\ndepreciation", size=10, color=SLATE)
f.text(528, 80, "profit and\nposition", size=10, color=SLATE)
f.arrow([(528, 106), (528, 140), (48, 140), (48, 108)], color=RED, dash=True, label="closing balances become next year's opening balances", lpos=(290, 156))
```

### 1.8.1 Eight uses of accounting information

1. **Owners judge performance.** The profit and loss account shows whether the business earned a surplus after all costs. A shopkeeper in Pokhara who sees a fall in net profit can look for the cause in sales or expenses. Without records, the owner only guesses.
2. **Banks decide on loans.** A bank asks for balance sheets and cash flows before lending, and uses them to judge repayment ability. A small manufacturer who can show three years of clear accounts is far more likely to get a working-capital loan. Poor records usually mean a refusal or a higher interest rate.
3. **Tax is calculated correctly.** The Inland Revenue Department needs sales, purchases, VAT and income to be reported accurately. A business with a PAN must keep proper books, issue bills and file returns on time. Clean records reduce penalties and disputes.
4. **Investors compare companies.** Shareholders of listed companies read published statements, earnings per share and ratios to compare firms. They decide whether to buy, hold or sell on the Nepal Stock Exchange. Reliable accounts are the base of the capital market.
5. **Managers plan and control.** Budgets are compared with actual figures to see where costs rise. A college finance office can see which department overspent and act in time. Accounting is the control panel of management.
6. **Creditors check safety.** Suppliers who sell on credit want to know if they will be paid. They look at the liquidity position and the payment history. A firm that pays on time earns better credit terms.
7. **Regulators supervise.** The Nepal Rastra Bank, the Securities Board and the Office of the Company Registrar require standard statements from the entities they supervise. Uniform rules such as NFRS make the figures comparable. This protects the public and the economy.
8. **Law and audit are satisfied.** The Companies Act and tax law require books to be kept, and auditors check them. Records also give evidence in a dispute, for example when a customer denies a payment. Honest accounts protect the business as much as they bind it.

## 1.9 Summary and exercises

Accounting turns economic events into reliable reports under a shared body of principles; Nepal anchors those principles in NFRS; and the equation A = L + E together with double entry makes the records self-balancing.

1. Distinguish book-keeping from accounting, and list four external users of financial statements.
2. State any five accounting concepts and give one Nepali business example of each.
3. Explain why the cost concept and the going-concern concept can conflict with a market-value view of assets.
4. A trader starts with Rs 2,00,000 cash, buys stock on credit for Rs 50,000 and pays rent of Rs 8,000. Show the equation after each step.
5. Why is a debit not always an increase? Illustrate with a liability account.
6. Differentiate NFRS from the Income Tax Act as a source of rules for profit measurement.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). State and explain the accounting equation. Show its effect through the transactions of a trader.**

*Equation.* **Assets = Liabilities + Capital (owner's equity).** Assets are resources owned (cash, stock, furniture); liabilities are amounts owed to outsiders; capital is the owner's claim. The equation holds after every transaction because each transaction has two equal sides (Figure 1.1).

*Illustration.* A trader starts with Rs 2,00,000 cash, buys stock on credit for Rs 50,000 and pays rent of Rs 8,000.

| Step | Cash | Stock | = | Creditors | + | Capital |
|---|---|---|---|---|---|---|
| 1. Start business | 2,00,000 | | = | | | 2,00,000 |
| 2. Stock on credit | 2,00,000 | 50,000 | = | 50,000 | | 2,00,000 |
| 3. Pay rent 8,000 | 1,92,000 | 50,000 | = | 50,000 | | 1,92,000 |

In step 3 an expense reduces cash and also reduces capital (profit is part of capital), so both sides fall by 8,000 and total assets Rs 2,42,000 still equal Rs 50,000 + Rs 1,92,000. *Conclusion:* the equation is the basis of double entry and of the balance sheet.

**Q2 (5 marks). Explain any five accounting concepts with a Nepali business example of each.**

1. **Business entity.** The business is separate from its owner. When a shopkeeper in Butwal takes Rs 5,000 for a family wedding, it is recorded as drawings, not as an expense.
2. **Going concern.** The business is assumed to continue, so a delivery van is shown at cost less depreciation, not at its forced-sale price.
3. **Money measurement.** Only items that can be measured in money are recorded. A loyal customer base is valuable but does not appear in the books, while Rs 1,20,000 of stock does.
4. **Cost concept.** Assets are recorded at purchase cost. Land bought for Rs 30 lakh stays at that figure even if its market value rises to Rs 60 lakh.
5. **Accrual (matching).** Revenue and expenses belong to the period in which they are earned or incurred, not when cash moves. Rent for Falgun that is paid in Chaitra is still an expense of Falgun.

*Others:* dual aspect, realisation, periodicity, consistency, prudence and materiality. *Conclusion:* the concepts make accounts comparable and reliable.

**Q3 (10 marks). Define accounting. Explain its objectives, users and branches. Distinguish book-keeping from accounting, and state the role of accounting standards (NFRS) in Nepal.**

*Introduction.* **Accounting** is the process of identifying, measuring, recording, classifying, summarising and communicating the financial information of an entity so that users can make informed decisions. It is often called the language of business.

*Objectives.* (1) Keep systematic records. (2) Find the profit or loss. (3) Show the financial position. (4) Provide information to users. (5) Help in tax and legal compliance. (6) Support planning and control.

*Users.* Internal users are owners and managers. External users are banks, suppliers, investors, employees, the Inland Revenue Department, regulators and the public (Section 1.8.1 lists eight uses).

*Branches.* **Financial accounting** records transactions and prepares statements for outsiders; **cost accounting** finds the cost of products and services; **management accounting** supplies analysis for internal decisions.

*Book-keeping versus accounting.*

| Basis | Book-keeping | Accounting |
|---|---|---|
| Scope | recording only | recording, classifying, summarising, interpreting |
| Stage | first stage | continues after book-keeping |
| Skill | routine, clerical | analytical, judgement |
| Output | journal and ledger | final accounts and analysis |
| Decision use | none by itself | direct basis for decisions |

*The cycle (Figure 1.2).* A source document leads to the journal, then the ledger, the trial balance, adjustments and the final accounts.

*Standards.* Accounting standards fix how items are recognised, measured and disclosed so statements are comparable. In Nepal the Accounting Standards Board issues Nepal Financial Reporting Standards (NFRS), which follow the international IFRS; small entities may use a simplified standard. Tax law, such as the Income Tax Act, has its own rules for taxable profit, so accounting profit and taxable profit can differ.

*Conclusion.* Accounting converts raw transactions into reliable information, standards and concepts keep it consistent, and its value is measured by the quality of the decisions that users take from it.

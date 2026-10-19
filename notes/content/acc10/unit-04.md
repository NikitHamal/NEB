---
subject: Accountancy
grade: 10
unit: 4
title: Business Accounting (व्यावसायिक लेखा)
hours: 5
area: Business Accounting
---

Every business, however small, has to answer four questions: how much did I earn, how much do I owe, how much is owed to me, and is my business worth more than it was last year? **Accounting** is the system that produces those answers. This unit introduces what accounting is and what it is for, the difference between financial, cost and management accounting, the rules — the **accounting standards** — that keep every business's answers comparable, the **Nepal Accounting Standards** that apply in our country, and the **chart of accounts**, the numbered list of account heads that an office uses to record a transaction in the right place.

::: key What the examiner tests here
Group A asks meanings: "Why do business organisations use accounting?", "What is an accounting standard?", "What is a chart of accounts?". Group B asks for the objectives and importance of financial accounting, and for the users of accounting information. Learn the **accounting equation** and the **rules of debit and credit**, because they are used again in units 6, 7 and 8 and they are the only way to get a numerical question right.
:::

## 4.1 Accounting: meaning, objectives and types

**Accounting** is the process of **identifying** economic events, **measuring** them in money, **recording** them in the books, **classifying** and **summarising** them, and then **communicating** the result to the people who have to take decisions.

The same idea is usually written in six steps, and this is the **accounting cycle**:

```figure caption="The accounting cycle. Every step feeds the next, and the last step produces the statements from which the next year's work begins."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,2.9))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,7)
steps=["Record in journal","Post to ledger","Balance and trial balance","Adjust and rectify","Final accounts","Communicate"]
for i,s in enumerate(steps):
    y = 6.0 - i*1.05
    ax.add_patch(FancyBboxPatch((0.4,y-0.4),6.2,0.8,boxstyle="round,pad=0.04",fc="#eaf1ff",ec=ACCENT,lw=1.0))
    ax.text(3.5,y,s,ha='center',va='center',fontsize=7.6,color=INK)
    if i < len(steps)-1:
        ax.add_patch(FancyArrowPatch((3.5,y-0.42),(3.5,y-1.05+0.42),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.0))
ax.add_patch(FancyBboxPatch((7.0,2.4),2.6,2.4,boxstyle="round,pad=0.06",fc="#fdf3f3",ec=SERIES[1],lw=1.2))
ax.text(8.3,3.6,"Statements\nused by\nowners, banks,\ngovernment",ha='center',va='center',fontsize=7,color=INK)
ax.add_patch(FancyArrowPatch((6.7,3.0),(6.95,3.4),arrowstyle="-|>",mutation_scale=9,color=MUTED,lw=1.0))
```

**Six steps in words.** First a transaction happens and is **identified** as one that changes the financial position — buying goods, selling goods, paying a bill, receiving cash. It is **measured** in rupees. It is **recorded** in the journal with a narration and a voucher. It is **posted** to the ledger accounts it affects, and all the ledger balances are collected in the **trial balance**. Adjustments and the rectification of errors are made. Finally the **final accounts** — trading account, profit and loss account and balance sheet — are prepared, and the result is **communicated** to the owners and to the people outside who need it.

**Types of accounting.**

| Type | Records | Main purpose | Main users |
|---|---|---|---|
| Financial accounting | Transactions with outsiders, in money, for a period | To show profit or loss and the financial position | Owners, banks, tax office, investors |
| Cost accounting | The cost of producing each product or service | To find the cost per unit and control cost | Management, factory heads |
| Management accounting | Any information, financial or non-financial, that is useful | To help managers plan, decide and control | Management only |

**Book-keeping, accounting and accountancy.** *Book-keeping* is only the recording part — writing up the journal and the ledger. *Accounting* includes summarising, analysing and interpreting the recorded figures. *Accountancy* is the whole body of knowledge, including the principles and rules on which accounting is built. So book-keeping is the smallest of the three and accountancy the largest.

**The accounting equation.** Every transaction keeps this true:

$$Assets = Liabilities + Capital$$

Assets are what the business owns; liabilities are what it owes to outsiders; capital is the owner's claim — what is left after outsiders have been paid. A transaction always changes at least two things in such a way that the equation still balances, which is why the system is called **double entry**.

**Rules of debit and credit.**

| Type of account | Debit (Dr.) | Credit (Cr.) |
|---|---|---|
| Asset | Increase | Decrease |
| Liability | Decrease | Increase |
| Capital | Decrease | Increase |
| Expense or loss | Increase | Decrease |
| Income or gain | Decrease | Increase |

::: example Does the equation still balance?
**Problem.** A trader starts a business with Rs. 5,00,000 of his own money. He takes a bank loan of Rs. 2,00,000. He buys furniture for Rs. 1,50,000 in cash and goods for resale for Rs. 3,00,000 on credit. Show the accounting equation after each transaction.

**Solution.**
Step 1 — Cash Rs. 5,00,000 = Capital Rs. 5,00,000: $5{,}00{,}000 = 0 + 5{,}00{,}000$.
Step 2 — Add loan: cash becomes $5{,}00{,}000 + 2{,}00{,}000 = Rs.\ 7{,}00{,}000$; liabilities Rs. 2,00,000. $7{,}00{,}000 = 2{,}00{,}000 + 5{,}00{,}000$. ✔
Step 3 — Buy furniture for cash: cash $= 7{,}00{,}000 - 1{,}50{,}000 = Rs.\ 5{,}50{,}000$; furniture Rs. 1,50{,}000. Total assets $= 5{,}50{,}000 + 1{,}50{,}000 = Rs.\ 7{,}00{,}000$. $7{,}00{,}000 = 2{,}00{,}000 + 5{,}00{,}000$. ✔
Step 4 — Buy goods on credit: stock Rs. 3,00,000, creditors Rs. 3,00,000. Total assets $= 5{,}50{,}000 + 1{,}50{,}000 + 3{,}00{,}000 = Rs.\ 10{,}00{,}000$; right side $= (2{,}00{,}000 + 3{,}00{,}000) + 5{,}00{,}000 = Rs.\ 10{,}00{,}000$. Balanced.

**Answer.** After all four transactions: assets Rs. 10,00,000, liabilities Rs. 5,00,000, capital Rs. 5,00,000. The equation holds after every single transaction.
:::

## 4.2 Objectives and importance of financial accounting

**Objectives.**

1. To keep a **systematic record** of every business transaction, with evidence.
2. To find out the **profit or loss** of a period by matching the income of the period against the expenses of the same period.
3. To show the **financial position** — what the business owns and owes — on a given date.
4. To give the owner the information he needs to **control** the business: which product earns, which expense is rising, which customer does not pay.
5. To supply the **evidence** required by the tax office, the auditor and the courts.
6. To **communicate** the result to the parties outside the business who have a right to know it.

**Importance.** For the **owner**, accounts show whether the capital is safe and growing. For **management**, they are the basis of every decision — pricing, purchase, expansion, borrowing. For **creditors and banks**, they decide whether credit can be given and on what terms. For the **government**, they are the base of income tax and VAT assessment. For **investors**, they are the reason to buy or sell a share. For **employees**, they are evidence in a wage or bonus dispute. And for the business itself, kept properly, they are the **memory** of the business and the proof of its good name.

**Users of accounting information.**

| Internal users | What they want |
|---|---|
| Owners / shareholders | Profit, the value of their investment, dividend |
| Management | Cost, profit by product, cash position, budgets |
| Employees | Wages, bonus, job security, the health of the firm |

| External users | What they want |
|---|---|
| Banks and lenders | Ability to repay; security |
| Suppliers and creditors | Ability to pay within the credit period |
| Government and tax authority | Income tax, VAT, correctness of returns |
| Investors and the stock exchange | Earnings, growth, risk |
| Auditors | Evidence for the audit report |
| Consumers and the public | Fair price, continuity of supply |

```photo id="acc10/ledger" caption="A bound ledger of 1828. A ledger is still the heart of the system: one account per head, one page per account, debit on the left and credit on the right." width="72"
```

## 4.3 Accounting standards

An **accounting standard** (लेखामान) is a written rule, issued by an authorised professional body, that says how a particular transaction or event must be recognised, measured, presented and disclosed in the financial statements.

Without standards, two businesses of the same size and in the same trade could report completely different profits simply because one values closing stock one way and the other another. A bank reading both could not compare them. Standards cure exactly that problem: they make the statements of different businesses **comparable**, keep them **consistent** from year to year, make them **reliable** — a statement prepared under standards can be trusted by a lender who has never visited the business — and give the auditor an objective yardstick instead of his own opinion.

**Qualitative characteristics** that standards exist to protect: *understandability*, *relevance*, *reliability* and *comparability*.

## 4.4 Nepal Accounting Standards

Accounting in Nepal is regulated by the **Institute of Chartered Accountants of Nepal (ICAN)**, which issues the standards through its **Accounting Standards Board (ASB)**. The framework in force is:

- **Nepal Financial Reporting Standards (NFRS)** — the full set, based on International Financial Reporting Standards, mandatory for listed companies and large public-interest entities.
- **NFRS for SMEs** — a reduced set for small and medium-sized entities that are not public-interest entities.
- **Nepal Accounting Standards (NAS)** — the older set, retained for entities that are not required to apply NFRS.

**Some standards a student should be able to name.**

| Standard | It deals with |
|---|---|
| NAS 1 / NFRS presentation | Presentation of financial statements |
| NAS 2 | Inventories — valuation at the lower of cost and net realisable value |
| NAS 7 | Statement of cash flows |
| NAS 16 | Property, plant and equipment — cost, depreciation, revaluation |
| NAS 18 | Revenue recognition |
| NAS 19 | Provision for employee benefits (retirement benefits) |

Two institutions enforce the result: the **Office of the Auditor General** audits government bodies, and the **Inland Revenue Department** uses the accounts for tax assessment. For a Grade 10 answer it is enough to say that standards are issued by ICAN through its Accounting Standards Board, that Nepal follows NFRS and NFRS for SMEs, and that the purpose of every one of them is comparability, consistency and reliability.

## 4.5 Chart of accounts

A **chart of accounts (खातासूची)** is the complete, organised and numbered list of all the account heads a business — or a government office — uses to record its transactions.

Look inside any office and you find the same problem: one clerk writes "stationery", another writes "office materials", a third writes "printing". At the end of the year the three amounts cannot be added and the report is useless. A chart of accounts fixes one name and one **code** for each head, and every clerk must use that code. The code makes the accounts easy to sort, easy to total and, in a computerised system, easy to search.

A chart of accounts is normally built in this order: the **five main groups** first — assets, liabilities, capital, income and expenses — then the sub-groups, then the individual accounts. The numbering is usually hierarchical: 1 for assets, 2 for liabilities, 3 for capital, 4 for income and 5 for expenses, with further digits for sub-groups.

```figure caption="The structure of a chart of accounts. The first digit fixes the main group, so any code can be read at a glance."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
groups=[("1","Assets","1000 Cash, 1100 Debtors, 1200 Furniture, 1300 Stock"),
        ("2","Liabilities","2000 Creditors, 2100 Bank loan, 2200 Outstanding salary"),
        ("3","Capital","3000 Capital, 3100 Drawings, 3200 Retained earnings"),
        ("4","Income","4000 Sales, 4100 Commission received, 4200 Rent received"),
        ("5","Expenses","5000 Purchase, 5100 Salary, 5200 Rent, 5300 Carriage")]
for i,(d,name,ex) in enumerate(groups):
    y = 8.6 - i*1.75
    ax.add_patch(FancyBboxPatch((0.3,y-0.6),1.0,1.2,boxstyle="round,pad=0.03",fc="#eaf1ff",ec=ACCENT,lw=1.1))
    ax.text(0.8,y, d, ha='center',va='center',fontsize=9,color=ACCENT,weight='bold')
    ax.text(1.6,y+0.24,name,ha='left',va='center',fontsize=7.8,color=INK,weight='bold')
    ax.text(1.6,y-0.30,ex,ha='left',va='center',fontsize=6.4,color=MUTED)
```

**The same idea in government accounting.** A Nepali government office does not invent its own codes. It uses the uniform **chart of accounts** prescribed by the Financial Comptroller General Office, in which every budget head, revenue head and expenditure head has a fixed code (for example 21111 for remuneration). Because the code is the same in every district, the whole country's accounts can be added up — which is exactly what the chart of accounts is for.

::: example Give the head and the code
**Problem.** Name the main group and suggest a suitable code for each of the following, using the scheme in the figure: (a) cash in hand, (b) a loan taken from Rastriya Banijya Bank, (c) salary paid to staff, (d) commission received, (e) goods bought for resale, (f) amount owed to a supplier.

**Solution.**
Step 1 — Decide, in each case, whether the item is something the business owns (asset), owes (liability), the owner's claim (capital), money coming in (income) or money going out (expense).
Step 2 — (a) cash in hand — the business owns it — **asset, 1000**.
Step 3 — (b) bank loan — the business owes it — **liability, 2100**.
Step 4 — (c) salary paid — an expense of running the business — **expense, 5100**.
Step 5 — (d) commission received — income — **income, 4100**.
Step 6 — (e) goods bought for resale — these are stock, which the business owns — **asset (stock), 1300**; and at the moment of purchase the same transaction is a **purchase, expense group 5000** when the periodic system is used.
Step 7 — (f) amount owed to a supplier — **liability, 2000 (creditors)**.

**Answer.** (a) asset 1000, (b) liability 2100, (c) expense 5100, (d) income 4100, (e) stock 1300 / purchase 5000, (f) liability 2000.
**What it means.** The five groups are decided by asking one question: does the item make the business richer (asset or income) or poorer (liability, capital withdrawal or expense)? The code simply files the answer.
:::

::: example Journal entry to the ledger head
**Problem.** A firm bought office furniture for Rs. 60,000, paying Rs. 20,000 in cash and agreeing to pay the balance next month. Which accounts are affected and which is debited and which is credited?

**Solution.**
Step 1 — Identify the accounts: furniture (asset), cash (asset), creditor (liability).
Step 2 — Furniture increases: an asset increasing is **debited** → Furniture A/c Dr. Rs. 60,000.
Step 3 — Cash decreases: an asset decreasing is **credited** → Cash A/c Cr. Rs. 20,000.
Step 4 — Creditors increase: a liability increasing is **credited** → Creditor A/c Cr. Rs. 40,000.
Step 5 — Check the equation: assets rise by $60{,}000 - 20{,}000 = 40{,}000$, liabilities rise by Rs. 40,000. Balanced.

**Answer.**
Furniture A/c Dr. 60,000
To Cash A/c 20,000
To Creditor A/c 40,000
(Being furniture purchased for cash and on credit.)
:::

::: caution The common mistake
Students write "cash account is debited because cash came in" without looking at the transaction. Cash is an **asset**: it is debited when it *increases* (money received) and credited when it *decreases* (money paid). Always name the type of account first, then apply the rule for that type. And never write a journal entry without a narration — the examiner awards a mark for it.
:::

## Chapter summary

- **Accounting** identifies, measures, records, classifies, summarises and communicates economic information. The **accounting cycle** runs: record in the journal, post to the ledger, take a trial balance, adjust and rectify, prepare the final accounts, communicate.
- **Financial accounting** records transactions with outsiders and reports profit or loss and financial position; **cost accounting** finds the cost per unit; **management accounting** supplies whatever information managers need. **Book-keeping** is only the recording stage; **accountancy** is the whole body of knowledge.
- The **accounting equation** is $Assets = Liabilities + Capital$; every transaction keeps it true, which is what double entry means.
- **Rules of debit and credit**: assets and expenses increase on the debit side; liabilities, capital and income increase on the credit side.
- **Objectives of financial accounting**: systematic record, profit or loss, financial position, control, evidence for tax and audit, communication. Its users are internal (owners, management, employees) and external (banks, creditors, government, investors, auditors, public).
- An **accounting standard** is a written rule on how to recognise, measure, present and disclose transactions; it makes statements **comparable, consistent and reliable**.
- In Nepal standards are issued by **ICAN** through its **Accounting Standards Board**: **NFRS** for listed and large entities, **NFRS for SMEs** for smaller ones, and the older **NAS** for the rest.
- A **chart of accounts** is the numbered list of all account heads, arranged in the five groups — assets, liabilities, capital, income and expenses. It gives every head one name and one code.
- A Nepali **government office** uses the uniform chart of accounts prescribed by the Financial Comptroller General Office, so that the accounts of every office can be added up.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. Define accounting in one sentence. <span class="marks">[1]</span>
2. Write the accounting equation. <span class="marks">[1]</span>
3. Name any two types of accounting. <span class="marks">[1]</span>
4. Which asset is increased by a debit? <span class="marks">[1]</span>
5. Why do business organisations use accounting? Give any two reasons. <span class="marks">[1]</span>
6. What is an accounting standard? <span class="marks">[1]</span>
7. Name the body that issues accounting standards in Nepal. <span class="marks">[1]</span>
8. Write the full form of NFRS. <span class="marks">[1]</span>
9. What is a chart of accounts? <span class="marks">[1]</span>
10. Write any two external users of accounting information. <span class="marks">[1]</span>
11. On which side is an increase in a liability recorded? <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Accounting is the process of identifying, measuring, recording, classifying, summarising and communicating economic information to the users who need it.
**2.** $Assets = Liabilities + Capital$.
**3.** Any two of: financial accounting, cost accounting, management accounting.
**4.** An asset is increased by a debit (e.g. furniture, cash, stock).
**5.** Any two of: to keep a systematic record, to find profit or loss, to show the financial position, to control the business, to satisfy the tax office and the auditor, to take decisions.
**6.** An accounting standard is a written rule, issued by an authorised professional body, prescribing how a transaction or event must be recognised, measured, presented and disclosed in the financial statements.
**7.** The Institute of Chartered Accountants of Nepal (ICAN), through its Accounting Standards Board.
**8.** Nepal Financial Reporting Standards.
**9.** A chart of accounts is the complete, organised and numbered list of all the account heads used to record transactions, grouped into assets, liabilities, capital, income and expenses.
**10.** Any two of: banks and lenders, suppliers and creditors, the government and the tax authority, investors, auditors, consumers and the public.
**11.** The credit side — a liability increases on the credit side.
:::

**Group B — Short answer (5 marks each)**

1. Why do business organisations use accounting? Explain any five reasons. <span class="marks">[5]</span>
2. Explain the objectives of financial accounting. <span class="marks">[5]</span>
3. Who are the users of accounting information? Explain any five of them and what each wants. <span class="marks">[5]</span>
4. What is an accounting standard? Explain its importance and name any three standards used in Nepal. <span class="marks">[5]</span>
5. What is a chart of accounts? Explain its structure and importance in an office. <span class="marks">[5]</span>
6. Distinguish between book-keeping, accounting and accountancy. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** (i) To keep a systematic, evidence-based record of every transaction. (ii) To find the profit or loss of a period. (iii) To show the financial position on a date. (iv) To give the owner information for control and decision. (v) To satisfy the tax office, the auditor and the courts. (Also: to attract investors and lenders, to value the business on sale.)
**2.** Systematic record; ascertainment of profit or loss by matching income with the expenses of the same period; presentation of the financial position; supply of information for control; provision of evidence for tax, audit and legal purposes; communication of the result to the interested parties.
**3.** Owners/shareholders want profit and the value of their investment; management wants cost, product-wise profit and the cash position for decisions; employees want wages, bonus and job security; banks and lenders want the ability to repay and the security available; suppliers and creditors want the ability to pay within the credit period; the government and tax authority want income tax and VAT correctly assessed; investors want earnings and risk; auditors want evidence for their report; the public wants a fair price and continuity of supply. (Any five with what each wants.)
**4.** A standard is a written rule on recognition, measurement, presentation and disclosure. Importance: comparability between businesses, consistency from year to year, reliability so that a lender may trust a statement without visiting the business, and an objective yardstick for the auditor. Standards in Nepal: NFRS, NFRS for SMEs and NAS; examples NAS 2 (inventories), NAS 16 (property, plant and equipment), NAS 18 (revenue).
**5.** A chart of accounts is the numbered list of all account heads. Structure: five main groups — assets (1), liabilities (2), capital (3), income (4) and expenses (5) — then sub-groups, then individual accounts, the code being hierarchical so that the first digit tells the group. Importance: one name and one code for every head, so that different clerks record similar items alike; easy sorting and totalling; makes computerised accounting possible; and in government, a uniform chart of accounts lets the accounts of every office be consolidated.
**6.** Book-keeping is only the recording stage — writing the journal, posting to the ledger, balancing the accounts; it is routine and clerical. Accounting goes further: it summarises, analyses and interprets the recorded data and prepares the final accounts. Accountancy is the whole body of knowledge, including the principles, standards and rules on which accounting is based. Book-keeping is a part of accounting, and accounting is a part of accountancy.
:::

**Group C — Long answer (8 marks each)**

1. What is accounting? Explain the steps of the accounting cycle and state the rules of debit and credit with the accounting equation. <span class="marks">[8]</span>
2. What is an accounting standard? Explain the accounting standards in force in Nepal and their importance to a business and to a bank that is considering a loan. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Definition (1).* Accounting is the process of identifying, measuring, recording, classifying, summarising and communicating economic information so that users can take decisions.
*Accounting cycle (4).* (i) Identify and measure the transaction in money. (ii) Record it in the journal with a narration and a voucher. (iii) Post to the ledger accounts. (iv) Balance the accounts and prepare the trial balance. (v) Make adjustments and rectify errors. (vi) Prepare the trading and profit and loss account and the balance sheet. (vii) Communicate the result to the users. Explain each step in one sentence and say that the cycle repeats every year.
*Equation and rules (3).* $Assets = Liabilities + Capital$; every transaction keeps it true. Assets and expenses increase on the debit side and decrease on the credit side; liabilities, capital and income increase on the credit side and decrease on the debit side.
**2.** *Definition (1).* A written rule issued by an authorised professional body prescribing how transactions must be recognised, measured, presented and disclosed.
*Standards in Nepal (3).* Issued by the Institute of Chartered Accountants of Nepal through its Accounting Standards Board: NFRS for listed companies and large public-interest entities; NFRS for SMEs for smaller entities; NAS for the rest. Give examples such as NAS 2 (inventories), NAS 16 (property, plant and equipment), NAS 18 (revenue) and NAS 7 (cash flows).
*Importance (4).* Comparability — two businesses in the same trade can be compared; consistency — the same basis year after year; reliability — a lender can trust a statement prepared under standards without inspecting the books; auditability — the auditor has an objective yardstick. For a bank considering a loan, standards mean that the profit, the assets and the liabilities it reads have been measured by rules it knows, so it can assess the borrower's ability to repay and the security honestly and quickly, and can compare the borrower with others. (Marks are given for the definition, the Nepali framework and the explanation of importance.)
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** What is total assets after those transactions?

**2.** Does a cash purchase of furniture immediately reduce capital by the full purchase price?

**3.** Is the owner and the business treated as one accounting entity?

::: note Reasoned key
**1.** Cash 40,000 + furniture 10,000 + goods 8,000 = Rs. 58,000. Liabilities 8,000 + capital 50,000 also equals 58,000.

**2.** No. One asset, cash, is exchanged for another, furniture. Later depreciation may affect profit and capital.

**3.** No. The business entity concept separates business transactions from the owner's personal transactions.

:::

::: tip Investigation — Check the accounting equation
Start a fictional shop with cash capital of Rs. 50,000. Buy furniture for Rs. 10,000 cash and goods for Rs. 8,000 on credit. Make a table showing assets, liabilities and capital after each transaction.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::

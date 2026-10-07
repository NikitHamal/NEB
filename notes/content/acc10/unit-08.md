---
subject: Accountancy (कार्यालय सञ्चालन तथा लेखा)
grade: 10
unit: 8
title: System of Government Accounting in Nepal (नेपालको सरकारी लेखा प्रणाली)
hours: 7
area: Government Accounting of Nepal
---

A shopkeeper's accounts answer to the owner. A government office's accounts answer to the **people who pay the taxes** — which is why government accounting is built differently. Every rupee must be traceable from the budget passed by Parliament to the bill paid in a village office, and every office must use the same forms, the same codes and the same rules, or the national accounts cannot be added up. This unit explains what government accounting is, the bases on which Nepal's system rests, how it differs from commercial accounting, how the three tiers of government and the two levels of office keep their accounts, and the two words every student must be able to define — the **consolidated fund** and the **single account fund**.

::: key What the examiner tests here
Group A asks short definitions — "What is government accounting?", "Write any two bases of government accounting in Nepal", "What is a consolidated fund?", "What is central level accounting?". Group B asks the differences between commercial and government accounting, or the main bases, or the accounting of the three tiers of government. Learn the bases as a numbered list of five and the differences as a table.
:::

## 8.1 Government accounting: introduction and features

**Government accounting (सरकारी लेखा प्रणाली)** is the system by which a government records, classifies, summarises and reports the **revenue it collects** and the **expenditure it incurs**, and shows the **financial position** of the government, in order to make the government answerable to the legislature and to the people for the money entrusted to it.

In Nepal the system is governed by the **Financial Procedures and Fiscal Responsibility Act, 2076** and its Rules, 2077, and it is operated by the **Financial Comptroller General Office (महालेखा नियन्त्रक कार्यालय, FCGO)** through the Treasury and Comptroller Offices in the districts.

**Main features.**

1. **It follows the budget.** Every rupee of expenditure must fall under an approved budget head. A payment outside the budget head is illegal, however good the cause.
2. **It is fund-based.** Money is held and accounted for in prescribed funds — the consolidated fund and the other funds — and the source of the money decides where it may be spent.
3. **It is uniform.** Every office uses the same forms, the same codes and the same chart of accounts, so the accounts of a village office and of a ministry can be added together.
4. **It is cash-based.** A transaction is recorded when cash is actually received or paid.
5. **It is double-entry and computerised.** Entries follow the double-entry rules, and today most of them are made in the government's computerised systems — PAMS, LMBIS, TSA and SuTRA — rather than in bound registers.
6. **It is audited from outside.** The accounts are audited by the **Office of the Auditor General** and reported to Parliament through the Public Accounts Committee.
7. **It is public.** The annual financial statements of the government are published, and any citizen may see them.

```figure caption="How public money moves and who watches it. Revenue is deposited into the consolidated fund, released under an appropriation, spent by an office against a budget head, and audited from outside."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
boxes=[(0.3,8.0,3.0,1.3,"Tax and non-tax\nrevenue collected"),
       (3.6,8.0,3.0,1.3,"CONSOLIDATED\nFUND"),
       (6.9,8.0,2.8,1.3,"Appropriation\nAct of Parliament"),
       (6.9,4.6,2.8,1.4,"Budget release to\nthe office and head"),
       (3.6,4.6,3.0,1.4,"Expenditure recorded\nin the bank cash book"),
       (0.3,4.6,3.0,1.4,"Statement of\nexpenditure to the\nTreasury Office")]
for x,y,w,h,t in boxes:
    col = "#eaf1ff" if "FUND" in t or "Expenditure" in t else "#f6f8fc"
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.06",fc=col,ec=ACCENT,lw=1.1))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=6.4,color=INK)
ax.add_patch(FancyArrowPatch((3.35,8.65),(3.55,8.65),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((6.65,8.65),(6.85,8.65),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((8.3,7.95),(8.3,6.05),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((6.85,5.3),(6.65,5.3),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((3.55,5.3),(3.35,5.3),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.1))
ax.add_patch(FancyBboxPatch((3.6,1.6),6.1,1.9,boxstyle="round,pad=0.06",fc="#fdf3f3",ec=SERIES[1],lw=1.2))
ax.text(6.65,2.55,"Office of the Auditor General\nand the Public Accounts Committee",ha='center',va='center',fontsize=6.8,color=INK)
ax.add_patch(FancyArrowPatch((1.8,4.5),(3.9,3.6),arrowstyle="-|>",mutation_scale=9,color=MUTED,lw=1.0,connectionstyle="arc3,rad=-0.2"))
ax.text(1.6,2.5,"audit\nreport",ha='center',fontsize=6.2,color=MUTED)
```

## 8.2 Main bases of government accounting in Nepal

| Base | What it means in practice |
|---|---|
| **Legal basis** | The Financial Procedures and Fiscal Responsibility Act, 2076 and the Rules, 2077, the annual Appropriation Act and the Finance Act fix what must be recorded and how |
| **Cash basis** | Revenue is recorded when received and expenditure when paid; there are no accruals and no debtors and creditors of the ordinary kind |
| **Double-entry system** | Every transaction has two sides; the government maintains the general ledger, the budget ledger and the personal ledgers |
| **Fund basis** | All revenue goes into the consolidated fund; expenditure is met from it only under an appropriation, and other funds (contingency, reserve, deposit) have their own rules |
| **Uniformity of forms and chart of accounts** | The prescribed forms (the म.ले.प.फा. series) and the uniform code carve every revenue head and every expense head in the same way in every office |
| **Budget classification** | Expenditure is classified by ministry, office and economic head (remuneration, allowance, goods and services, capital), so budget and actual can be compared line by line |
| **Two levels of accounting** | Central level transactions are accounted for at the FCGO; operating level transactions are accounted for in the office itself |
| **Banking arrangement** | Government money is kept in the Nepal Rastra Bank and in commercial banks under agreement, and payments are made by cheque or by electronic transfer, not in cash |
| **External audit** | Every office's accounts and stores are audited by the Office of the Auditor General |

## 8.3 Similarities and differences between commercial and government accounting

They are similar in that both use the double-entry principle, both rest on documentary evidence, both prepare statements at the end of the period, and both are audited. Everything else is different.

| Point | Commercial accounting | Government accounting |
|---|---|---|
| **Main objective** | To find profit or loss and the financial position of a private business | To show accountability for public money and to ensure it was spent as approved |
| **Basis** | Usually accrual — income earned and expenses incurred | Cash — receipts and payments as they happen |
| **Ownership** | Owners or shareholders, who take the profit | The public; no owner's capital and no drawings |
| **Budget** | A plan, used as a guide | A law; spending outside it is irregular |
| **Funds** | One general fund of the business | Several funds — consolidated fund, contingency fund and others — each with its own rules |
| **Accounts kept** | Journal, ledger, trading and profit and loss account, balance sheet | General ledger, budget ledger, personal and advance ledgers, bank cash book, statements of revenue and expenditure, statement of financial position |
| **Main statements** | Trading account, profit and loss account, balance sheet | Statement of revenue, statement of expenditure, statement of financial position, statement of the consolidated fund |
| **Measuring performance** | Profit | Economy, efficiency, effectiveness and compliance with the law |
| **Audit** | By a chartered accountant or an auditor appointed by the owners | By the Office of the Auditor General, reporting to Parliament |
| **Rules** | Accounting standards and company law | Financial procedures law, appropriation and finance acts, and the prescribed forms |

```photo id="acc10/singha-durbar" caption="Singha Durbar, the seat of many ministries. Every ministry's revenue and expenditure runs through the same government accounting system and the same chart of accounts." width="86"
```

## 8.4 Accounting of the federal, provincial and local levels

Nepal is a **federal democratic republic** with three tiers of government, and each tier has its own budget, its own accounts and its own audit.

| Tier | Who keeps the accounts | How revenue and expenditure are recorded |
|---|---|---|
| **Federal (सङ्घ)** | The ministries and departments and their offices, through the FCGO and the Treasury and Comptroller Offices | Federal taxes and non-tax revenue go into the consolidated fund of the federation; federal expenditure is met under the appropriation act |
| **Provincial (प्रदेश)** | The provincial ministries and offices, through the Provincial Treasury and Comptroller Offices | Provincial taxes and the money received from the federal divisible fund go into the provincial consolidated fund |
| **Local (स्थानीय)** | Municipalities, rural municipalities and ward offices, through the Local Treasury and Comptroller Offices | Local taxes, service fees and grants go into the local consolidated fund; the local assembly appropriates the expenditure |

The three tiers are linked by the **divisible fund** — the pool of federal revenue shared with the provinces and local levels under the recommendation of the **National Natural Resources and Fiscal Commission** — and by the **grant system**. Each tier's accounts are audited by the Office of the Auditor General and reported to its own assembly.

## 8.5 Central level and operating level accounting

Government transactions are recorded at two levels.

**Central level accounting (केन्द्रीय तहको लेखा).** Transactions that relate to the **centre** — payments made at the ministry or the department itself, or expenditure that a central office books on behalf of the whole country, such as a lump-sum transfer to a province — are accounted for centrally, at the Financial Comptroller General Office and the central Treasury and Comptroller Office. The office concerned uses **central level accounting**.

**Operating level accounting (कार्यसञ्चालन तहको लेखा).** Transactions of a **district or local office** — paying a salary, buying stationery, issuing an advance to a section officer — are accounted for in the office itself, using the **bank cash book** and the prescribed vouchers. Every month the office sends its statement of expenditure and its bank reconciliation to the Treasury and Comptroller Office, which consolidates it.

The difference matters because the two levels use different records: the central level transactions come into the general ledger directly, while the operating level's figures reach it only through the monthly statement of expenditure. If a district office fails to send its statement, the national accounts are incomplete — which is exactly why the monthly reporting deadlines are enforced.

## 8.6 Chart of accounts and its use in government accounting

The **chart of accounts (खातासूची)** is the uniform, coded list of every revenue head, every expenditure head, every fund and every asset that a government office may use. In Nepal it is prescribed by the FCGO, and it is the same in every district.

Its structure follows the **budget classification**. Expenditure is carved first by **ministry and office** (the organisational classification) and then by **economic head**:

| Code (example) | Head | What it covers |
|---|---|---|
| 21111 | Remuneration (पारिश्रमिक) | Salary of staff |
| 21112 | Allowances (भत्ता) | Dearness, house rent, other allowances |
| 21121 | Office materials (कार्यालय मसलन्द) | Stationery, printing |
| 22111 | Uniform (ड्रेस) | Uniform for staff |
| 22311 | Travelling expenses (भ्रमण खर्च) | Travel on duty |
| 22711 | Miscellaneous expenses (विविध खर्च) | Other running costs |
| 31111 | Machinery and equipment (मेसिनरी तथा उपकरण) | Capital purchase of equipment |
| 31121 | Furniture and fixtures | Capital purchase of furniture |

**Why it matters.** A code makes a payment checkable before it is made: the office can see instantly whether the budget head has money left, and the auditor can see instantly whether the head was the right one. And because the code is the same everywhere, every office's figures can be added into one national statement.

## 8.7 Determination and use of government accounting formats

A **format (फाराम)** is the printed form on which a particular government transaction or record must be written. The forms are prescribed centrally, and every office must use the prescribed one: an entry made on a plain sheet has no standing in an audit.

The formats are known by the series number **म.ले.प.फा.नं.** and each carries its own purpose. The ones a Grade 10 student must be able to name are:

| Format | Used for |
|---|---|
| Vouchers (भौचर) | Recording one transaction: the निकासा भौचर for a payment, the आम्दानी भौचर for a receipt, the **गोश्वारा भौचर** for a transfer between heads or accounts |
| **Bank cash book (म.ले.प.फा.नं. २०९)** | The office's combined record of cash and bank receipts and payments, kept month by month |
| General ledger and budget ledger (म.ले.प.फा.नं. २०७ and similar) | The office's accounts by budget head, showing appropriation, release and expenditure |
| Advance (पेस्की) register | Advances paid to staff, and their clearance |
| Statement of expenditure (खर्चको फाँटबारी) | The monthly return sent to the Treasury and Comptroller Office |
| Revenue statement (राजस्वको फाँटबारी) | The monthly return of revenue collected |
| Store ledger (जिन्सी खाता) | Goods received and issued |

The forms exist because government accounting has to be **checked by people who were not there**. A voucher that names the budget head, the payee, the purpose, the amount and the authority lets a distant auditor reconstruct the transaction years later.

## 8.8 Areas of Nepal's government accounting

| Area | What it records |
|---|---|
| **Revenue accounting** | Taxes and non-tax revenue collected, deposited into the consolidated fund and reported |
| **Expenditure (appropriation) accounting** | Payments made under each budget head, advances paid and cleared, the bank cash book and the statement of expenditure |
| **Store (jinsi) accounting** | Goods bought, stored and issued; the store ledger and the bin card |
| **Fund accounting** | The consolidated fund, the divisible fund, the contingency fund and other funds, and the retention account |
| **Deposit and retention accounting** | Money held on behalf of others — retention from contractors, provident fund, income tax deducted |
| **Loan and grant accounting** | Foreign and domestic loans received, and grants-in-aid to and from other levels of government |
| **Asset and liability accounting** | Government property and the government's liabilities, maintained to complete the statement of financial position |

## 8.9 Single account fund and consolidated fund

These two terms look alike and are constantly confused. They are not the same thing.

**Consolidated fund (सञ्चित कोष).** The consolidated fund is the government's **main account**. All revenue — taxes, fees, loans, grants — must be deposited into it, and no money may be withdrawn from it except under an **appropriation made by law** (the Appropriation Act passed by Parliament or by the provincial or local assembly). It is the account that gives the legislature its real power over the executive: the government can collect, but it cannot spend, without a vote.

**Single account fund (एकल कोष खाता).** The single account fund is the arrangement under which a government office keeps **one bank account** — a single treasury account — for its transactions, instead of several accounts for different purposes. All its receipts are deposited into that account and all its payments are made from it, and the office records them in the **bank cash book**. The single account fund replaced the old practice of a separate account for each scheme; it makes the government's cash position visible at any moment, stops money lying idle in many accounts and makes reconciliation easy.

::: example Consolidated fund and single account fund
**Problem.** State, with a reason, which of the following is a matter of the **consolidated fund** and which of the **single account fund**.
(a) A district office maintains one bank account at Rastriya Banijya Bank and pays every bill from it.
(b) Parliament passes the Appropriation Act authorising the government to spend Rs. 1,700 billion.
(c) A municipality deposits the house tax it collects into its main account at the Nepal Bank.
(d) The Treasury and Comptroller Office releases a month's budget to a district office, which is credited to its operating account.
(e) No payment may be made from the government's main account for a purpose for which no appropriation was passed.

**Solution.**
Step 1 — Ask whether the point is about **authority to spend from the main fund** (consolidated fund) or about **how an office keeps its operating bank account** (single account fund).
Step 2 — (a) One operating bank account for all transactions → **single account fund**.
Step 3 — (b) The authority to spend, given by the legislature → **consolidated fund**.
Step 4 — (c) Revenue deposited into the main fund of the local level → **consolidated fund**.
Step 5 — (d) Budget released into the operating account of the office → **single account fund** arrangement.
Step 6 — (e) The rule that nothing may be spent without an appropriation → **consolidated fund**.

**Answer.** (a) and (d) single account fund; (b), (c) and (e) consolidated fund.
:::

::: example Similarities and differences
**Problem.** A bank asks a newly appointed accountant of a district office why the office's accounts do not show the office's "profit". Explain, giving four differences between commercial accounting and government accounting.

**Solution.**
Step 1 — The objective is different. A business exists to earn profit for its owners; a government office exists to deliver services under an approved budget. There is no profit to measure, so there is no profit and loss account.
Step 2 — The basis is different. A commercial firm generally follows the accrual basis; the government follows the cash basis, recording a receipt when money is received and a payment when money is paid.
Step 3 — The drive is different. A business is guided by a budget but may depart from it; a government office may not spend one rupee outside its budget head, because the budget is a law and not a plan.
Step 4 — The accountability is different. The owners of a business may read its accounts if they wish; the accounts of a government office are audited by the Office of the Auditor General and laid before Parliament and the public.

**Answer.** The four differences are objective (accountability, not profit), basis (cash, not accrual), the standing of the budget (law, not plan) and accountability (public audit, not private audit).
:::

::: example Choosing the budget head
**Problem.** A district office has to record the following payments. Choose the most suitable budget head from the chart of accounts and give its code: (a) the monthly salary of a section officer; (b) a new computer for the account section; (c) a steel almirah for the record room; (d) the travelling allowance of a staff member sent to a training in Pokhara; (e) the purchase of paper, ink and registers.

**Solution.**
Step 1 — Decide first whether the payment is **recurrent** (running the office) or **capital** (acquiring an asset). Salaries, allowances, travel and stationery are recurrent; a computer and an almirah are capital.
Step 2 — (a) Salary of staff is remuneration → **21111, Remuneration**.
Step 3 — (b) A computer is a machine → **31111, Machinery and equipment**.
Step 4 — (c) A steel almirah is furniture → **31121, Furniture and fixtures**.
Step 5 — (d) Travel on duty → **22311, Travelling expenses**.
Step 6 — (e) Paper, ink and registers are consumables → **21121, Office materials**.

**Answer.** (a) 21111, (b) 31111, (c) 31121, (d) 22311, (e) 21121.
**What it means.** The code is not decoration. Booking a computer to office materials would hide a capital purchase inside a running expense, and the auditor would report it as an irregular charge.
:::

::: caution The common mistake
"Cabinet decides to spend Rs. 5 crore from the consolidated fund, so the payment is valid" is wrong. Money may be withdrawn from the consolidated fund **only under an appropriation made by law**. A decision of the Cabinet, a minister or a secretary is not enough; without an appropriation the payment is irregular, and the Auditor General will report it.
:::

## Chapter summary

- **Government accounting** is the system by which a government records, classifies, summarises and reports its revenue, expenditure and financial position, in order to be accountable to the legislature and the people. In Nepal it is governed by the **Financial Procedures and Fiscal Responsibility Act, 2076** and its Rules, 2077, and operated by the **Financial Comptroller General Office**.
- Its **bases** are: the legal basis, the **cash basis**, the **double-entry system**, the **fund basis**, **uniformity of forms and chart of accounts**, **budget classification**, the **two levels of accounting**, the **banking arrangement**, and **external audit**.
- **Commercial and government accounting** both use double entry and documentary evidence, but they differ in **objective** (profit against accountability), **basis** (accrual against cash), **ownership**, the **standing of the budget** (plan against law), **funds**, the **statements** prepared, **performance measurement** and **audit**.
- Nepal has **three tiers** — federal, provincial and local — each with its own consolidated fund, budget and audit, linked by the divisible fund and the grant system.
- **Central level accounting** records the transactions of the centre at the FCGO; **operating level accounting** records a district or local office's transactions in the office itself, through the bank cash book, reported monthly by the statement of expenditure.
- The **chart of accounts** is the uniform coded list of revenue, expenditure, fund and asset heads, following the budget classification (for example 21111 remuneration, 22111 uniform, 22311 travelling expenses). It makes a payment checkable in advance and the national accounts addable.
- Government **formats** (the म.ले.प.फा. series) are prescribed centrally: the vouchers (निकासा, आम्दानी, गोश्वारा), the **bank cash book (No. 209)**, the ledgers, the advance register, the statement of expenditure and the revenue statement.
- The **areas** of government accounting are revenue, expenditure, store (jinsi), fund, deposit and retention, loan and grant, and asset and liability accounting.
- The **consolidated fund** is the government's main account: all revenue is deposited into it and nothing may be withdrawn except under an appropriation made by law. The **single account fund** is the one bank account an office keeps for all its receipts and payments, recorded in the bank cash book.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is government accounting? <span class="marks">[1]</span>
2. Write any two bases of government accounting in Nepal. <span class="marks">[1]</span>
3. Which basis of accounting does the government of Nepal follow? <span class="marks">[1]</span>
4. Which office manages government accounting in Nepal? <span class="marks">[1]</span>
5. What is a consolidated fund? <span class="marks">[1]</span>
6. Write any two government offices that use central level accounting. <span class="marks">[1]</span>
7. What is operating level accounting? <span class="marks">[1]</span>
8. What is a chart of accounts? <span class="marks">[1]</span>
9. Write any two areas of government accounting. <span class="marks">[1]</span>
10. Write any two differences between commercial and government accounting. <span class="marks">[1]</span>
11. Name the apex auditing body that audits government accounts in Nepal. <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Government accounting is the system by which a government records, classifies, summarises and reports its revenue and expenditure and its financial position, in order to be accountable to the legislature and the public for public money.
**2.** Any two of: legal basis, cash basis, double-entry system, fund basis, uniformity of forms and chart of accounts, budget classification, two levels of accounting, banking arrangement, external audit.
**3.** The cash basis.
**4.** The Financial Comptroller General Office (महालेखा नियन्त्रक कार्यालय).
**5.** The consolidated fund is the government's main account, into which all revenue must be deposited and from which no money may be withdrawn except under an appropriation made by law.
**6.** Any two of: the Ministry of Finance, the Office of the Auditor General, a ministry or department at the centre, the Financial Comptroller General Office.
**7.** Operating level accounting is the accounting of the transactions of a district or local office, kept in the office itself in the bank cash book and reported monthly through the statement of expenditure.
**8.** The chart of accounts is the uniform, coded list of every revenue head, expenditure head, fund and asset that a government office may use, prescribed by the Financial Comptroller General Office.
**9.** Any two of: revenue accounting, expenditure accounting, store (jinsi) accounting, fund accounting, deposit and retention accounting, loan and grant accounting, asset and liability accounting.
**10.** Any two of: objective (profit against accountability); basis (accrual against cash); budget (plan against law); ownership (private owners against the public); audit (private auditor against the Auditor General).
**11.** The Office of the Auditor General.
:::

**Group B — Short answer (5 marks each)**

1. What is government accounting? Explain any five bases of government accounting in Nepal. <span class="marks">[5]</span>
2. Explain any five differences between commercial accounting and government accounting. <span class="marks">[5]</span>
3. Explain the accounting of the federal, provincial and local levels in Nepal. <span class="marks">[5]</span>
4. What is the chart of accounts? Explain its structure and importance in government accounting. <span class="marks">[5]</span>
5. What is a consolidated fund? Explain the provisions for its operation. <span class="marks">[5]</span>
6. Distinguish between central level accounting and operating level accounting. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definition as in Group A answer 1. Bases: (i) *legal basis* — the Financial Procedures and Fiscal Responsibility Act 2076 and the Rules 2077; (ii) *cash basis* — receipts and payments recorded when they happen; (iii) *double-entry* — general, budget and personal ledgers; (iv) *fund basis* — every receipt and payment belongs to a fund; (v) *uniformity* — the same forms and chart of accounts in every office. (Also: budget classification, two levels, banking arrangement, external audit.)
**2.** Objective — profit against accountability; basis — accrual against cash; ownership — private against public; budget — a plan against a law; funds — one general fund against several prescribed funds; statements — trading, profit and loss account and balance sheet against statements of revenue, expenditure and financial position; performance — profit against economy, efficiency and compliance; audit — a private auditor against the Office of the Auditor General. (Any five explained.)
**3.** The federation keeps its accounts through the ministries, departments and the FCGO; its revenue goes into the federal consolidated fund and its expenditure is met under the federal appropriation act. The provinces keep their accounts through the provincial ministries and the Provincial Treasury and Comptroller Offices; provincial revenue and the divisible fund money go into the provincial consolidated fund. The local levels (municipalities, rural municipalities, wards) keep their accounts through the Local Treasury and Comptroller Offices; their own taxes, fees and grants go into the local consolidated fund and the local assembly appropriates the expenditure. The three are linked by the divisible fund and the grant system, and each tier's accounts are audited by the Office of the Auditor General.
**4.** The chart of accounts is the uniform coded list of all revenue heads, expenditure heads, funds and assets. Its structure follows the budget classification: first the organisational classification (ministry, office) and then the economic classification (remuneration 21111, allowance 21112, office materials 21121, uniform 22111, travelling expenses 22311, machinery 31111, furniture 31121). Importance: payments can be checked against the balance in the head before they are made; the auditor sees at once whether the right head was used; and because the codes are the same everywhere, the accounts of all offices can be consolidated into the national statement.
**5.** The consolidated fund is the government's main account. All revenue — taxes, fees, loans and grants — must be deposited into it, and no money may be withdrawn from it except under an appropriation made by law. Provisions for its operation: all government receipts are credited to it; expenditure requires an appropriation act passed by the legislature; the money may be used only for the purposes approved; emergency expenditure is met from the contingency fund and later regularised by the legislature; the fund is managed by the Ministry of Finance and accounted for by the FCGO; and no payment may be made from it without the authority of the prescribed officer.
**6.** Central level accounting records transactions of the centre — payments made at the ministry or department, or expenditure booked centrally for the whole country — and is kept at the Financial Comptroller General Office and the central Treasury and Comptroller Office. Operating level accounting records the transactions of a district or local office — a salary paid, an advance issued, stationery bought — in the office itself, using the bank cash book and the prescribed vouchers, and is reported monthly to the Treasury and Comptroller Office through the statement of expenditure. The central level figures enter the general ledger directly; the operating level figures enter it only through the monthly return.
:::

**Group C — Long answer (8 marks each)**

1. What is government accounting? Explain the main bases of government accounting in Nepal and the differences between commercial and government accounting. <span class="marks">[8]</span>
2. What is the consolidated fund? Explain the provisions for its operation and distinguish it from the single account fund. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Definition (1).* As in Group A answer 1.
*Bases (4).* Legal basis, cash basis, double-entry system, fund basis, uniformity of forms and chart of accounts, budget classification, two levels of accounting, banking arrangement, external audit — explain any five or six in a sentence each.
*Differences (3).* Objective, basis, ownership, standing of the budget, funds, statements prepared, performance measurement, audit. Give them as a table with a short explanation of each row.
**2.** *Consolidated fund (2).* The government's main account: all revenue is deposited into it and nothing may be withdrawn from it except under an appropriation made by law.
*Provisions for its operation (3).* All government receipts credited to it; expenditure only under an appropriation act; use only for the approved purposes; emergency expenditure from the contingency fund, later regularised; managed by the Ministry of Finance and accounted by the FCGO; payment only by the officer authorised to draw.
*Difference from the single account fund (3).* The consolidated fund is about **authority and ownership** — it is the government's main fund and its use is controlled by the legislature. The single account fund is about **the mechanics of day-to-day banking** — each office keeps one operating bank account for all its receipts and payments, recorded in the bank cash book, which replaced the practice of several accounts for several schemes. A payment from the single account fund of an office is valid only if it falls within an appropriation from the consolidated fund.
:::

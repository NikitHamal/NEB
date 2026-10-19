---
subject: Accountancy
grade: 10
title: Agencies Involved in Government Accounting (नेपालको सरकारी लेखा प्रणालीमा संलग्न विभिन्न निकायहरू)
unit: 14
hours: 4
area: Government Accounting of Nepal
---

A budget is not executed by one office. It is prepared by one body, voted by another, released by a third, spent by thousands, accounted for by a fourth, audited by a fifth and examined by a sixth. This unit names the six, says what each does, and explains how the government's money reaches a district office through the banking arrangement.

::: key What the examiner tests here
Group A asks: "Which office prepares the national budget?", "What is the role of the Financial Comptroller General Office?", "Write any two functions of the Ministry of Finance", "What is the role of the DTCO?". Group B asks for the agencies involved in government accounting and their functions, or the banking arrangement of government offices. The safest answer format is a table: agency on the left, function on the right.
:::

## 14.1 Introduction: the agencies of the government accounting system

Government accounting is a chain of accountability, and every link in it is an institution with a defined job. One body decides how much may be spent, another makes the money available, another spends it, another records it, another audits it, and the last one is the people's own representative assembly, which asks what happened to the money it voted.

| Agency | Its place in the system |
|---|---|
| Ministry of Finance | Prepares the budget and manages the consolidated fund |
| National Planning Commission | Sets the plan and the priorities the budget must serve |
| Financial Comptroller General Office | Controls the release of money and keeps the central accounts |
| Treasury and Comptroller Offices | Make the payments and keep the operating level accounts |
| Spending offices (ministries, departments, districts, local levels) | Incur expenditure and keep the primary records |
| Office of the Auditor General | Audits the accounts and reports |
| Public Accounts Committee | Examines the audit report on behalf of Parliament |
| Nepal Rastra Bank | Banker to the government; keeps the government's accounts |

## 14.2 Ministry of Finance, Financial Comptroller General Office, National Planning Commission

**Ministry of Finance (अर्थ मन्त्रालय)** is the ministry that manages the government's money. Its functions are: to prepare the **budget** and the annual financial statement for the government; to frame **revenue and tax policy** and the fiscal policy of the country; to manage the **consolidated fund**, the contingency fund and government borrowing; to arrange **internal and external loans and grants**; to control and monitor **public expenditure**; to fix the terms of government borrowing and of the foreign exchange rate policy in consultation with Nepal Rastra Bank; and to represent the government in financial negotiations with foreign lenders and donors. It also lays the **Annual Report of the Financial Comptroller General Office** before the legislature.

**Financial Comptroller General Office (महालेखा नियन्त्रक कार्यालय, FCGO)** is the office under the Ministry of Finance that actually runs the government accounting system. Its functions are: to **release** the budget to the spending offices against the appropriation; to keep the **central accounts** of the government; to supervise and guide the Treasury and Comptroller Offices; to consolidate the accounts of every office and prepare the **annual financial statement** and the monthly and annual reports; to maintain the **uniform chart of accounts and the prescribed formats**; and to operate the computerised systems (**FMIS, CGAS, TSA, SUTRA**). It is, in short, the accountant of the whole government.

**National Planning Commission (राष्ट्रिय योजना आयोग)** prepares the country's **periodic development plan**, decides the **priorities** and the sectoral ceilings within which the budget is made, appraises and approves large development projects, and recommends the **resource envelope** for the plan period. It supplies the Medium-Term Expenditure Framework which the Ministry of Finance uses to build each year's budget. Without it, the budget would be a list of requests with no plan behind it.

```photo id="acc10/finance-ministry" caption="The Ministry of Finance, Kathmandu. It prepares the budget, manages the consolidated fund and answers to Parliament for the government's finances." width="80"
```

## 14.3 Treasury and Comptroller Offices

The **Treasury and Comptroller Offices (कोष तथा लेखा नियन्त्रक कार्यालय)** are the local arms of the Financial Comptroller General Office and the government's paymaster. They exist at the central level, in each province and in each district, where the district office is known as the **DTCO** and the provincial one as the **PTCO**.

**Functions.**

1. To **receive the budget release** from the FCGO and pass it on to the offices within its jurisdiction.
2. To **make the payments** of the offices on the basis of the payment orders passed to it — by cheque or by electronic transfer from the government's account.
3. To keep the **operating level accounts** for the offices in its area, and to consolidate the monthly statements of expenditure that the offices send.
4. To **control expenditure against the release**, and to refuse payment where the head has no balance or the payment order is defective.
5. To operate the **single account fund (TSA)** in the district, so that all government payments in the district come out of one account.
6. To make the **bank reconciliation** with the Nepal Rastra Bank and the commercial banks, and to report the district's financial position to the FCGO.
7. To keep the accounts of **revenue deposits** made by the offices and forward them to the consolidated fund.
8. To provide the figures on which the FCGO's consolidated statements are built.

A district office therefore does not pay anybody by itself. It passes a payment order to the DTCO; the DTCO checks the head, the release and the authority, and pays. That separation is deliberate: the office that decides to spend does not hold the money.

```figure caption="Who does what in the expenditure chain. The spending office decides and records; the Treasury and Comptroller Office pays; the Financial Comptroller General Office consolidates and reports; the Auditor General checks."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,2.9))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,8)
rows=[(6.4,"Ministry of Finance — budget and the consolidated fund","#eaf1ff",ACCENT),
      (4.9,"FCGO — release, central accounts, consolidation","#eef3ff",ACCENT),
      (3.4,"Treasury and Comptroller Office — pays and keeps operating accounts","#f6f8fc",MUTED),
      (1.9,"Spending office — incurs expenditure, keeps primary records","#f6f8fc",MUTED),
      (0.4,"Office of the Auditor General — audits and reports","#fdf3f3",SERIES[1])]
for y,t,c,ec in rows:
    ax.add_patch(FancyBboxPatch((0.4,y),9.2,1.15,boxstyle="round,pad=0.05",fc=c,ec=ec,lw=1.1))
    ax.text(5.0,y+0.575,t,ha='center',va='center',fontsize=6.4,color=INK)
for y in (6.25,4.75,3.25,1.75):
    ax.add_patch(FancyArrowPatch((5.0,y),(5.0,y-0.15),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.0))
```

## 14.4 Office of the Auditor General, Public Accounts Committee, Nepal Rastra Bank

**Office of the Auditor General (महालेखापरीक्षकको कार्यालय)** is the constitutional audit body described in unit 13. In this unit its place in the chain matters: it is the one agency that is deliberately placed **outside** the spending line, so that it can examine it. It audits the accounts of the federation, the provinces, the local levels, the constitutional bodies, the courts, government corporations and foreign aid, and reports to the President, who lays the report before Parliament.

**Public Accounts Committee (सार्वजनिक लेखा समिति)** is a committee of the legislature. Its function is to examine the audit report, to call the Secretary of the ministry or the head of the office concerned and ask him to explain each observation, to take evidence from the Auditor General's office, to direct the recovery of money or the correction of a system, and to report to the House. It is the committee that turns an audit observation into an action — and therefore the body that makes the Auditor General's independence worth having.

**Nepal Rastra Bank** is the **banker to the government**. It keeps the accounts of the government and of the government offices, receives government revenue and makes government payments through the Treasury and Comptroller Offices, holds the government's foreign exchange and manages the issue of treasury bills and bonds by which the government borrows from the market. Under the banking arrangement of government offices, every office's money is kept in the Nepal Rastra Bank or in a commercial bank with which the government has an agreement, and no office keeps a private bank account of its own.

## 14.5 Banking arrangement of government offices

The **banking arrangement (बैंकिङ व्यवस्थापन)** is the set of rules that govern how government money is kept in the bank and how it is paid out.

1. **One designated account.** Under the **single account fund (Treasury Single Account, TSA)**, an office keeps one account for its transactions, and it is opened only with the bank named by the Financial Comptroller General Office — ordinarily the Nepal Rastra Bank at district level, or a commercial bank under an agreement.
2. **Release credited to the account.** The budget release passed by the Treasury and Comptroller Office is credited directly to the office's account.
3. **Payment by cheque or electronic transfer.** The office passes a payment order to the Treasury and Comptroller Office, which issues the cheque or makes the transfer. Payment is not made in cash except for petty expenses expressly allowed.
4. **Revenue deposited, never spent.** Revenue is deposited into the government account the same day, and the office may not pay an expense out of it.
5. **Daily and monthly records.** Every receipt and payment is entered in the **bank cash book (म.ले.प.फा.नं. २०९)**; the office reconciles the bank every month and sends the bank reconciliation with the monthly statement of expenditure.
6. **No overdraft, no idle balances.** The account may not be overdrawn, and money that is not needed is not left lying in an office account, because the single account sweeps it to the centre.
7. **Cheque custody and control.** Cheque books are kept under lock, cheques are signed only by the officer authorised to sign them, and an unused or spoilt cheque is accounted for.

**Why the arrangement matters.** Three things are achieved by it. The government knows at any moment **how much cash it has**, because the money is not scattered over thousands of private accounts. **Expenditure cannot escape the budget**, because the office cannot pay out of money it has collected. And **reconciliation is possible**, because there is one account per office and one set of records against one passbook.

::: example Which agency?
**Problem.** Name the agency responsible in each case, and say in one line what the agency is doing. (a) Preparing the annual budget of the Government of Nepal. (b) Releasing the quarterly budget to a district office. (c) Paying the salary of a district office's staff. (d) Auditing the accounts of a municipality. (e) Asking the Secretary of a ministry why a contract was given at an unusually high price, on the basis of the audit report. (f) Keeping the bank account of the government and issuing treasury bills.

**Solution.**
Step 1 — (a) The budget is prepared by the **Ministry of Finance**, using the plan and the ceilings set by the National Planning Commission.
Step 2 — (b) The release is made by the **Financial Comptroller General Office**, through the Treasury and Comptroller Office.
Step 3 — (c) The payment is made by the **Treasury and Comptroller Office** (the DTCO) on the office's payment order — not by the spending office itself.
Step 4 — (d) The audit is by the **Office of the Auditor General**, which audits the local levels as well as the federation and the provinces.
Step 5 — (e) The **Public Accounts Committee** of the legislature examines the audit report and calls the official to explain.
Step 6 — (f) **Nepal Rastra Bank**, which is the banker to the government and manages government borrowing.

**Answer.** (a) Ministry of Finance, (b) FCGO, (c) DTCO, (d) Office of the Auditor General, (e) Public Accounts Committee, (f) Nepal Rastra Bank.
**What it means.** Every agency in the chain exists to make it impossible for one office to both spend public money and be the only witness to how it was spent.
:::

::: example The banking arrangement in practice
**Problem.** A newly appointed accountant of a district office proposes to open a separate account in a nearby commercial bank for a project fund, "so that the project money is separate and easy to use". Advise him.

**Solution.**
Step 1 — State the rule. A government office may open its account only in the bank named by the FCGO, and under the single account fund it keeps **one** account for its transactions.
Step 2 — Applying the rule, the proposal is **not allowed**. Opening a private account would take government money outside the treasury single account, make the government's cash position unknown, and allow expenditure to escape the release and the budget.
Step 3 — The legitimate need — to see the project's money separately — is met **inside** the system, in two ways: by opening a separate **budget head** for the project with its own code and its own ledger account, and by marking the project fund separately in the office's accounts and monthly statements.
Step 4 — What he should do: apply to the FCGO through the Treasury and Comptroller Office for a separate bank account if the rules permit it, or simply use a distinct budget head and a distinct ledger account within the existing account.

**Answer.** Not allowed as proposed. Use a separate budget head and ledger account within the office's existing government account.
**What it means.** Separation of money for accounting purposes is done with **heads and ledgers**, not with private bank accounts. The single bank account is precisely what makes the government's cash position knowable.
:::

::: example Functions of the FCGO
**Problem.** A district office has submitted its monthly statement of expenditure and its bank reconciliation to the Treasury and Comptroller Office. State four things the Financial Comptroller General Office will do with that information, and explain why the district office cannot simply keep the figures to itself.

**Solution.**
Step 1 — The DTCO consolidates the district's statement with those of the other offices in its area and forwards it to the FCGO.
Step 2 — The **FCGO records it in the central accounts**, so that the national account of expenditure under each budget head includes the district's figures.
Step 3 — The **FCGO compares expenditure with the release** and sanctions further releases for the coming months; an office spending faster than expected is asked why, and one that is not spending at all may lose part of its allocation.
Step 4 — The **FCGO consolidates all the offices' figures into the government's annual financial statement**, which is audited by the Office of the Auditor General and laid before Parliament.
Step 5 — The **FCGO supervises the office's accounting** — it checks that the prescribed formats, codes and rules were used, and it maintains the chart of accounts and the formats that the district office works with.
Step 6 — Why the office cannot keep the figures to itself: the district office's money is not its own but the government's, voted by Parliament for the whole country; until the district's figures are consolidated the national accounts are incomplete, further releases cannot be justified, and the legislature cannot see how its money was spent.

**Answer.** Consolidation and central accounting; comparison of expenditure with release and the sanction of further releases; consolidation into the annual financial statement for audit and Parliament; and supervision of the prescribed formats, codes and systems.
**What it means.** Operating level accounting in the office is only half the system. The figures have to travel upwards, or the nation's accounts would be a sum of fragments and the legislature would be voting money blind.
:::

::: caution The common mistake
Students write "the Ministry of Finance releases the budget to the office". The budget is **voted** by Parliament, **prepared** by the Ministry of Finance, but **released** by the Financial Comptroller General Office through the Treasury and Comptroller Offices. Another frequent error is to say that a district office "pays" its staff: it passes a **payment order**, and the **DTCO** pays.
:::

## Chapter summary

- Government accounting is a chain of accountability, and each link is an institution: the **Ministry of Finance**, the **National Planning Commission**, the **Financial Comptroller General Office**, the **Treasury and Comptroller Offices**, the spending offices, the **Office of the Auditor General**, the **Public Accounts Committee** and **Nepal Rastra Bank**.
- The **Ministry of Finance** prepares the budget and the annual financial statement, frames revenue and fiscal policy, manages the consolidated fund and the contingency fund, arranges loans and grants, controls public expenditure and lays the FCGO's annual report before the legislature.
- The **Financial Comptroller General Office** releases the budget, keeps the central accounts, supervises the Treasury and Comptroller Offices, consolidates the accounts, maintains the chart of accounts and the formats and runs the computerised systems. It is the accountant of the whole government.
- The **National Planning Commission** prepares the periodic plan, sets priorities and sectoral ceilings, appraises large projects and provides the resource envelope for the budget.
- The **Treasury and Comptroller Offices** (DTCO at district level, PTCO at provincial level) receive the release, make payments on the offices' payment orders, keep the operating level accounts, control expenditure against the release, operate the single account fund and report to the FCGO.
- The **Office of the Auditor General** audits the accounts of the federation, the provinces, the local levels, the constitutional bodies, the courts, government corporations and foreign aid, and reports to the President and thence to Parliament.
- The **Public Accounts Committee** examines the audit report, calls the officials concerned to explain, directs recovery or correction and reports to the House. It is what turns an observation into an action.
- **Nepal Rastra Bank** is the banker to the government: it keeps the government's accounts, receives revenue, makes payments through the Treasury offices and manages government borrowing.
- Under the **banking arrangement**, each office keeps one designated account under the single account fund; the release is credited to it; payments are made by cheque or electronic transfer on a payment order from the Treasury and Comptroller Office; revenue is deposited and never spent; the bank cash book is written daily and reconciled monthly; the account may not be overdrawn and no private accounts are allowed. The arrangement makes the government's cash position knowable, keeps expenditure inside the budget and makes reconciliation possible.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. Which office prepares the annual budget of the Government of Nepal? <span class="marks">[1]</span>
2. Write any two functions of the Ministry of Finance. <span class="marks">[1]</span>
3. What is the role of the Financial Comptroller General Office? <span class="marks">[1]</span>
4. What is the full form of FCGO? <span class="marks">[1]</span>
5. What is a DTCO and what does it do? <span class="marks">[1]</span>
6. Which office releases the budget to a spending office? <span class="marks">[1]</span>
7. Who is the banker to the Government of Nepal? <span class="marks">[1]</span>
8. What is the function of the National Planning Commission? <span class="marks">[1]</span>
9. Name the two names of government offices that use central level accounting. <span class="marks">[1]</span>
10. What is the single account fund? <span class="marks">[1]</span>
11. Name the parliamentary committee that examines the audit report. <span class="marks">[1]</span>

::: note Answers to Group A
**1.** The Ministry of Finance.
**2.** Any two of: preparing the budget; framing revenue and fiscal policy; managing the consolidated fund; arranging loans and grants; controlling public expenditure; fixing the terms of government borrowing.
**3.** The Financial Comptroller General Office releases the budget, keeps the central accounts, supervises the Treasury and Comptroller Offices, consolidates the accounts of all offices, maintains the chart of accounts and the formats, and operates the computerised accounting systems.
**4.** Financial Comptroller General Office (महालेखा नियन्त्रक कार्यालय).
**5.** The District Treasury and Comptroller Office; it receives the budget release and makes the payments of the government offices in the district on their payment orders, and keeps the operating level accounts.
**6.** The Financial Comptroller General Office, through the Treasury and Comptroller Office.
**7.** Nepal Rastra Bank.
**8.** It prepares the country's periodic development plan, sets the priorities and sectoral ceilings for the budget, appraises large projects and recommends the resource envelope.
**9.** The Ministry of Finance and the Office of the Auditor General (also acceptable: a ministry or department at the centre, and the FCGO).
**10.** The arrangement under which a government office keeps one designated bank account for all its receipts and payments, recorded in the bank cash book, under the Treasury Single Account.
**11.** The Public Accounts Committee (सार्वजनिक लेखा समिति).
:::

**Group B — Short answer (5 marks each)**

1. Name the agencies involved in the government accounting system of Nepal and explain the functions of any four. <span class="marks">[5]</span>
2. Explain the functions of the Ministry of Finance. <span class="marks">[5]</span>
3. What is the Financial Comptroller General Office? Explain its functions. <span class="marks">[5]</span>
4. Explain the functions of the Treasury and Comptroller Offices. <span class="marks">[5]</span>
5. Explain the banking arrangement of government offices. <span class="marks">[5]</span>
6. Explain the role of the Public Accounts Committee and of Nepal Rastra Bank in the government accounting system. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Agencies: Ministry of Finance, National Planning Commission, Financial Comptroller General Office, Treasury and Comptroller Offices, the spending offices, the Office of the Auditor General, the Public Accounts Committee and Nepal Rastra Bank. Explain any four: Ministry of Finance — budget, fiscal policy, consolidated fund, loans and grants, expenditure control; FCGO — release, central accounts, consolidation, formats and systems; DTCO — payments, operating level accounts, single account fund, reporting; Office of the Auditor General — audit of all government accounts and stores and report to the President and Parliament.
**2.** Preparing the budget and the annual financial statement; framing revenue and tax policy and fiscal policy; managing the consolidated fund and the contingency fund; arranging internal and external loans, grants and foreign aid; controlling and monitoring public expenditure; fixing the terms of government borrowing and advising on the exchange rate policy with Nepal Rastra Bank; laying the annual report of the FCGO before the legislature; and representing the government in financial negotiations.
**3.** The FCGO is the office under the Ministry of Finance that runs the government accounting system. Functions: releasing the budget to spending offices against the appropriation; keeping the central accounts; supervising and guiding the Treasury and Comptroller Offices; consolidating the accounts of all offices and preparing the annual financial statement and the periodical reports; maintaining the uniform chart of accounts and the prescribed formats; and operating the computerised systems (FMIS, CGAS, TSA, SUTRA).
**4.** Receiving the budget release from the FCGO and passing it to the offices in its jurisdiction; making payments on the offices' payment orders by cheque or electronic transfer; keeping the operating level accounts and consolidating the monthly statements of expenditure; controlling expenditure against the release and refusing defective payment orders; operating the single account fund in the district; making the bank reconciliation and reporting the financial position to the FCGO; and receiving and forwarding revenue deposits to the consolidated fund.
**5.** One designated bank account per office under the single account fund (TSA), opened with the bank named by the FCGO (Nepal Rastra Bank or a commercial bank under agreement); the release credited directly to the account; payment by cheque or electronic transfer on a payment order, not in cash except for allowed petty expenses; revenue deposited the same day and never spent; every entry in the bank cash book and a monthly bank reconciliation sent with the statement of expenditure; no overdraft and no idle balances; and strict custody and control of cheque books. The arrangement makes the government's cash position known at any time, keeps expenditure within the budget and makes reconciliation possible.
**6.** The *Public Accounts Committee* is a committee of the legislature that examines the report of the Auditor General, calls the Secretary or head of the office concerned to explain each observation, takes evidence, directs the recovery of money or the correction of the system and reports to the House — it turns an audit observation into an action. *Nepal Rastra Bank* is the banker to the government: it keeps the government's and the offices' accounts, receives government revenue and makes payments through the Treasury and Comptroller Offices, holds the foreign exchange reserves and manages the issue of treasury bills and bonds by which the government borrows. Both sit outside the spending chain, which is why they can hold it to account and serve it at the same time.
:::

**Group C — Long answer (8 marks each)**

1. Explain the agencies involved in the government accounting system of Nepal and their functions, and describe the banking arrangement of government offices.
2. Explain the government accounting system of Nepal from the preparation of the budget to the settlement of the audit report, naming the agency responsible at each stage. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *The agencies (4).* Ministry of Finance (budget, fiscal policy, consolidated fund, loans and grants, expenditure control); National Planning Commission (plan, priorities, ceilings, project appraisal); FCGO (release, central accounts, consolidation, chart of accounts, computerised systems); Treasury and Comptroller Offices (payments, operating level accounts, single account fund, reporting); the spending offices (incur expenditure and keep primary records); Office of the Auditor General (audit); Public Accounts Committee (examination of the report and action); Nepal Rastra Bank (banker to the government). Give the function of each in a sentence or two.
*Banking arrangement (4).* One designated account under the single account fund; the release credited to it; payment by cheque or electronic transfer on a payment order by the Treasury and Comptroller Office; revenue deposited the same day and never spent; daily entry in the bank cash book and monthly reconciliation; no overdraft, no idle balance, no private account; cheque custody and control. Then state the three results: the cash position is known, expenditure cannot escape the budget and reconciliation is possible.
**2.** *Budget preparation (1).* The National Planning Commission sets the plan, the priorities and the sectoral ceilings; the Ministry of Finance prepares the budget and the annual financial statement, with the line ministries feeding their proposals through the LMBIS.
*Authorisation (1).* The budget is presented to Parliament, discussed and passed as the Appropriation Act and the Finance Act; without these, nothing may be spent or collected.
*Release (1).* The FCGO releases money to the spending offices through the Treasury and Comptroller Offices, and the release is credited to the office's account under the single account fund.
*Execution (2).* The spending office spends against a budget head; it passes a payment order to the Treasury and Comptroller Office, which pays by cheque or transfer; the office enters the payment in the bank cash book and sends the monthly statement of expenditure; revenue collected is deposited into the consolidated fund the same day.
*Accounting and reporting (1).* The FCGO consolidates the accounts of every office into the government's annual financial statement, using the uniform chart of accounts and the FMIS, CGAS, TSA and SUTRA systems.
*Audit and settlement (2).* The Office of the Auditor General audits the accounts and the stores, reports to the President, who lays the report before Parliament; the Public Accounts Committee examines the report, calls the officials concerned to explain, and directs the recovery of money or the correction of the system; each observation is settled by producing the asset, the money or the authority, or by recovery from the person responsible.
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** Which constitutional institution performs Nepal's external public audit?

**2.** Is external audit identical to day-to-day bookkeeping?

**3.** Why consolidate financial reports?

::: note Reasoned key
**1.** The Office of the Auditor General, within its constitutional and legal mandate.

**2.** No. Bookkeeping records transactions; external audit independently examines the accounts and their supporting evidence.

**3.** To present an overall view while retaining the underlying office-level evidence and responsibility.

:::

::: tip Investigation — Map institutions to responsibilities
Create a responsibility map distinguishing an office's transaction recording, financial administration and reporting, internal review, and the Auditor General's external audit. Explain why keeping these roles distinct matters for accountability.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::

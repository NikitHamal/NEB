---
subject: Accountancy
grade: 10
title: Accounting of Government Expenditure (सरकारी खर्चको लेखा)
unit: 10
hours: 12
area: Government Accounting of Nepal
---

This is the working chapter of government accounting. It is how a district office actually spends its budget: the appropriation voted by Parliament and released month by month, the **payment order** issued against a budget head, the cheque drawn on the office's account at the bank, the **bank cash book** in which every receipt and payment is written, the monthly **statement of expenditure** sent to the Treasury and Comptroller Office, and the **vouchers** that an auditor will read years later. Everything here is format work, and every format has a rule.

::: key What the examiner tests here
Group B and Group C both carry numerical questions from this unit, and they are among the most predictable in the paper: a set of government transactions from which you must prepare the **bank cash book (A.G.F. No. 209)**, or a table of appropriation and expenditure from which you must prepare the **statement of expenditure**, or a set of transactions for which you must pass the **journal vouchers**. Learn the columns of each format and the direction of each entry — budget release and revenue are debits, expenditure and advances are credits.
:::

## 10.1 Expenditure and appropriation accounting: introduction

**Expenditure accounting (सरकारी खर्चको लेखा)**, also called **appropriation accounting (विनियोजन लेखा)**, is the branch of government accounting that records the **money a government office spends** against the budget head approved for it, the **advances** it gives and recovers, the **deductions** it holds on behalf of others, and the **bank balance** it holds at any moment.

Its guiding principle is different from a businessman's. A businessman asks *is this expense profitable?* A government office asks *is this expense **authorised**, and is there enough money left in the head?* Three words run through the whole unit:

- **Appropriation (विनियोजन)** — the amount the legislature has voted for a head for the year.
- **Release (निकासा)** — the part of the appropriation actually made available to the office, usually month by month or quarter by quarter.
- **Expenditure (खर्च)** — what has actually been spent against the head.

$$Available\ balance = Appropriation - Expenditure\ to\ date - Uncleared\ advances$$

An expenditure is **regular** only if it satisfies all of these: it falls within the approved budget head; it is incurred for the purpose for which the head exists; it is supported by evidence; it is sanctioned by the officer authorised to sanction it; the goods or services have actually been received; and it is recorded in the prescribed forms.

## 10.2 Codes used in expenditure accounting

Expenditure is coded in the same uniform chart of accounts as revenue. The code has two parts.

**The organisational classification** tells *who* is spending — the ministry, the department, the office and its office code. This is how the accounts show which office spent the money.

**The economic classification** tells *what* the money was spent on. The first digit of the economic code separates **recurrent** from **capital** expenditure:

| First digit | Meaning | Examples |
|---|---|---|
| **2** | Recurrent expenditure (चालु खर्च) — running the office | 21111 remuneration, 21112 allowances, 21121 office materials, 22111 uniform, 22311 travelling expenses, 22612 fuel, 22711 miscellaneous |
| **3** | Capital expenditure (पुँजीगत खर्च) — acquiring an asset | 31111 machinery and equipment, 31121 furniture and fixtures, 31131 vehicles, 31141 buildings and structures |

So the code **21111** read from left to right says: recurrent expenditure (2), of the personnel group (1), on remuneration (111). A clerk who books a computer to 21121 instead of 31111 has hidden a capital purchase inside a running expense, and the office's asset records will be wrong for years.

## 10.3 Formats used in expenditure accounting and reporting

| Format | What it records |
|---|---|
| **Payment order (भुक्तानी आदेश)** | The office's authority to pay a stated amount to a stated person against a stated budget head, passed to the Treasury and Comptroller Office |
| **Vouchers (भौचर)** | The individual entries: the **गोश्वारा भौचर** for a transfer or journal entry, the **निकासा भौचर** for a payment, the **आम्दानी भौचर** for a receipt |
| **Advance (पेस्की) register** | Advances paid to staff or suppliers, and their clearance |
| **Bank cash book (म.ले.प.फा.नं. २०९)** | The office's combined cash-and-bank record, written month by month |
| **Budget ledger / expenditure ledger** | The head-wise account showing appropriation, release and expenditure |
| **Statement of expenditure (खर्चको फाँटबारी)** | The monthly return to the Treasury and Comptroller Office |
| **Deposit and retention ledgers** | Money held on behalf of others — provident fund, income tax deducted, retention from contractors |

The purpose of the formats is the same as everywhere in government accounting: to let somebody who was not there reconstruct the transaction. A payment whose voucher does not name the head, the payee, the purpose and the authority cannot be audited, and an unauditable payment is treated as an irregular payment.

```figure caption="The route of an expenditure. Nothing is paid until each step is complete, and the bank cash book entry is made only after the money has actually moved."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
steps=["1 Appropriation voted\nby the legislature","2 Budget released\nby the Treasury Office",
       "3 Goods or services\nreceived and bill passed","4 Payment order\nissued to the DTCO",
       "5 DTCO pays; entry in the\nbank cash book (No. 209)","6 Statement of expenditure\nsent monthly"]
for i,s in enumerate(steps):
    y = 9.0 - i*1.5
    col = "#eaf1ff" if i < 3 else "#f6f8fc"
    ax.add_patch(FancyBboxPatch((0.4,y-0.55),6.6,1.1,boxstyle="round,pad=0.04",fc=col,ec=ACCENT if i<3 else MUTED,lw=1.0))
    ax.text(3.7,y,s,ha='center',va='center',fontsize=6.8,color=INK)
    if i < len(steps)-1:
        ax.add_patch(FancyArrowPatch((3.7,y-0.57),(3.7,y-1.5+0.57),arrowstyle="-|>",mutation_scale=9,color=INK,lw=1.0))
ax.add_patch(FancyBboxPatch((7.4,4.0),2.3,4.4,boxstyle="round,pad=0.06",fc="#fdf3f3",ec=SERIES[1],lw=1.1))
ax.text(8.55,6.2,"Office of the\nAuditor General\nmay test any\nstep, years later",ha='center',va='center',fontsize=6.4,color=INK)
```

```photo id="acc10/cheque-issued" caption="A bank cheque. In a government office the cheque is not written by the clerk: the payment order goes to the Treasury and Comptroller Office, which issues the cheque and releases the money." width="80"
```

## 10.4 Payment order, advance payment and clearance

A **payment order (भुक्तानी आदेश)** is the document by which a government office authorises a payment. It names the budget head, the payee, the amount, the purpose and the sanction, and it is passed to the **Treasury and Comptroller Office (कोष तथा लेखा नियन्त्रक कार्यालय, DTCO at district level)** which makes the payment by cheque or electronic transfer.

**Kinds of payment.** *Recurrent* payments (salary, allowance, stationery, travel) are for running the office; *capital* payments (machinery, furniture, vehicles, buildings) create an asset. *Revenue* payments are made from the consolidated fund against an appropriation; *deposit* payments are made out of money the office is merely holding — provident fund, tax deducted at source, retention withheld from a contractor — and are not expenditure at all.

A **payment order** is of two kinds in practice:

| Kind | When it is used |
|---|---|
| **Final payment** | The bill has been received and checked and the supplier or employee is paid in full |
| **Advance (पेस्की) payment** | Money is needed before the bill can be produced — for travel on duty, or for a purchase to be made by an officer |

**Advance and its clearance.** An advance is a debt of the officer to the government, not an expenditure. It must be cleared, as a rule within the same financial year (Nepali practice allows about a month, and certainly before the year is closed):

1. The advance is paid by payment order and entered in the **advance register** and in the bank cash book.
2. When the work is done, the officer submits the **bill** with the vouchers and the unused balance, if any.
3. If the bill is **equal to** the advance, the advance account is cleared against the expenditure head.
4. If the bill is **larger** than the advance, the excess is paid by a further payment order.
5. If the bill is **smaller**, the unspent cash is refunded and credited back.

$$Uncleared\ advance = Advance\ paid - Advance\ cleared$$

An uncleared advance at the end of the year is deducted from the available balance of the head, because the money is already committed.

::: example Advance payment and clearance — journal vouchers
**Problem.** Pass the journal vouchers for the following transactions of a District Education Office.
(a) A payment order of Rs. 60,000 was issued against budget head 31111 for the purchase of a computer.
(b) An advance of Rs. 80,000 was given to Section Officer Mr. Rana against budget head 31121 for the purchase of furniture for the office.
(c) Mr. Rana cleared his furniture advance by submitting a bill of Rs. 95,000 for furniture purchased out of his own arrangement.
(d) Provident fund of Rs. 30,000 and income tax of Rs. 5,000 deducted from the salary of Shrawan were deposited into the concerned office.

**Solution.**
Step 1 — (a) The government has incurred capital expenditure and the DTCO will pay. Debit the expenditure head, credit the DTCO.
*31111 Machinery and equipment (computer) A/c Dr. 60,000*
*To DTCO A/c 60,000*
(Being a payment order issued for the purchase of a computer.)
Step 2 — (b) An advance is not an expense; it is a debt recoverable from the officer.
*Furniture advance (Mr. Rana) A/c Dr. 80,000*
*To DTCO A/c 80,000*
(Being an advance issued for the purchase of furniture.)
Step 3 — (c) The advance is cleared, the asset is recognised at the full bill value, and the excess is a further charge on the same head.
*31121 Furniture and fixtures A/c Dr. 95,000*
*To Furniture advance (Mr. Rana) A/c 80,000*
*To DTCO A/c 15,000*
(Being the furniture advance cleared on a bill of Rs. 95,000, the excess of Rs. 15,000 being payable.)
Step 4 — (d) The deductions were never the office's money; they were held on behalf of others and are now paid over.
*Provident fund payable A/c Dr. 30,000*
*Income tax payable A/c Dr. 5,000*
*To Bank A/c 35,000*
(Being the amount deducted from salary deposited into the concerned office.)

**Answer.** The four vouchers above.
**What it means.** An advance and an expenditure are different things. Booking an advance as an expenditure inflates the year's spending and hides a recoverable debt — and it is exactly the kind of thing the Auditor General looks for at the year end.
:::

## 10.5 Bank cash book (A.G.F. No. 209) and its preparation

The **bank cash book**, prescribed as **म.ले.प.फा.नं. २०९**, is the office's combined record of its bank account. It is the single most important book of an operating level office, because it shows both the money received and the money paid, month by month, with a running balance.

**The columns.** The prescribed form carries the **date**, the **voucher number**, the **particulars of the transaction**, a **debit** column for money received, a **credit** column for money paid, and a **balance** column.

**What goes on each side.**

| Debit (receipts) | Credit (payments) |
|---|---|
| Budget release received from the Treasury and Comptroller Office | Expenditure paid (salary, office materials, travel, capital goods) |
| Revenue collected and deposited | Advances paid to staff or suppliers |
| Retention money and deductions received | Retention money and deductions refunded or paid over |
| Refund of an unspent advance | Money transferred to another head or office |
| Amount transferred in from another head | Balance carried down |

**How to prepare it.**

1. Write the opening balance brought forward from the previous month.
2. Enter every receipt on the debit side and every payment on the credit side, in date order, with the voucher number.
3. Carry the running balance after every entry.
4. Total both columns and write the closing balance on the credit side (if it is a debit balance) so that the two columns agree.
5. Prepare the bank reconciliation with the passbook and send the statement of expenditure with a copy of the bank cash book.

::: example Bank cash book for the month of Shrawan
**Problem.** The following transactions took place in the bank account of a District Coordination Unit during the month of Shrawan. There was no opening balance. Prepare the bank cash book (A.G.F. No. 209).
i. 2082/04/03 — Budget release received from the Treasury and Comptroller Office Rs. 5,00,000.
ii. 2082/04/08 — Payment order issued against 22311 office materials for Rs. 80,000.
iii. 2082/04/14 — Advance of Rs. 50,000 given to a section officer against 31121 for furniture.
iv. 2082/04/25 — Salary payment order issued for the month of Shrawan, total salary Rs. 2,00,000, after deducting provident fund Rs. 30,000 and income tax Rs. 5,000.
v. 2082/04/26 — The provident fund and income tax deducted were deposited into the concerned office.

**Solution.**
Step 1 — The budget release is money received: **debit Rs. 5,00,000**; balance Rs. 5,00,000.
Step 2 — The office materials payment is money paid: **credit Rs. 80,000**; balance Rs. 4,20,000.
Step 3 — The advance is money paid (and recoverable): **credit Rs. 50,000**; balance Rs. 3,70,000.
Step 4 — The salary: the full salary is Rs. 2,00,000, of which Rs. 30,000 + Rs. 5,000 = Rs. 35,000 is deducted and only the **net Rs. 1,65,000** is paid out. **Credit Rs. 1,65,000**; balance Rs. 2,05,000.
Step 5 — The deductions, when deposited, leave the office's account: **credit Rs. 35,000**; balance Rs. 1,70,000.
Step 6 — Total both sides and carry the closing balance.

*Bank cash book (म.ले.प.फा.नं. २०९) — month of Shrawan, 2082*

| Date | Voucher no. | Particulars | Debit (Rs.) | Credit (Rs.) | Balance (Rs.) |
|---|---|---|---|---|---|
| 04/03 | 1 | Budget release received from the DTCO | 5,00,000 | | 5,00,000 |
| 04/08 | 2 | Payment order — 22311 office materials | | 80,000 | 4,20,000 |
| 04/14 | 3 | Advance to section officer — 31121 furniture | | 50,000 | 3,70,000 |
| 04/25 | 4 | Salary of Shrawan, net of provident fund Rs. 30,000 and income tax Rs. 5,000 | | 1,65,000 | 2,05,000 |
| 04/26 | 5 | Provident fund Rs. 30,000 and income tax Rs. 5,000 deposited | | 35,000 | 1,70,000 |
| 04/30 | | Balance c/d | | 1,70,000 | — |
| | | **Total** | **5,00,000** | **5,00,000** | |

**Answer.** Total receipts Rs. 5,00,000; total payments Rs. 3,30,000; closing balance Rs. 1,70,000 (debit), subject to reconciliation with the passbook.
**What it means.** The office has spent only Rs. 1,65,000 of cash on salary, but Rs. 2,00,000 of the head has been committed. The bank cash book is a record of money, not of appropriation — which is why the statement of expenditure is needed as well.
:::

## 10.6 Statement of expenditure and its preparation

The **statement of expenditure (खर्चको फाँटबारी)** is the monthly return in which every government office reports to the Treasury and Comptroller Office what it has received and what it has spent, head by head, and how much of its appropriation remains available.

**The columns.**

| Column | What it shows |
|---|---|
| Budget head number | The code of the head |
| Budget head (description) | The name of the head |
| Annual appropriation | The amount voted for the year |
| Total expenditure up to the month | Cumulative expenditure of the year |
| Expenditure of the current month | This month's spending |
| Uncleared advance | Advances still to be cleared |
| Available balance | Appropriation − expenditure − uncleared advance |

The statement is short but it is the single most important operating document of the office, because the Treasury and Comptroller Office releases further money on the strength of it. A wrong figure either starves the office of funds or leaves money unspent that should have gone to another office.

::: example Statement of expenditure
**Problem.** The following particulars relate to the District Police Office, Sindhuli, for the month of Poush 2080. Prepare the statement of expenditure and show the available balance.

| Budget head no. | Budget head | Annual appropriation (Rs.) | Expenditure up to Magh (Rs.) | Expenditure of Poush (Rs.) |
|---|---|---|---|---|
| 21111 | Remuneration | 4,20,000 | 1,50,000 | 28,000 |
| 22111 | Uniform | 45,000 | 7,500 | 1,500 |
| 22311 | Office materials | 20,000 | 9,000 | 1,800 |
| 22612 | Travelling expenses | 75,000 | 30,000 | 6,000 |
| 22711 | Miscellaneous expenses | 36,000 | 11,000 | 2,200 |

An uncleared advance of Rs. 4,000 for fuel is outstanding.

**Solution.**
Step 1 — Total the annual appropriation: $4{,}20{,}000 + 45{,}000 + 20{,}000 + 75{,}000 + 36{,}000 = Rs.\ 5{,}96{,}000$.
Step 2 — Total the expenditure up to Magh: $1{,}50{,}000 + 7{,}500 + 9{,}000 + 30{,}000 + 11{,}000 = Rs.\ 2{,}07{,}500$.
Step 3 — Total the expenditure of Poush: $28{,}000 + 1{,}500 + 1{,}800 + 6{,}000 + 2{,}200 = Rs.\ 39{,}500$.
Step 4 — Available balance $= 5{,}96{,}000 - 2{,}07{,}500 - 4{,}000 = Rs.\ 3{,}84{,}500$.

*Statement of expenditure — District Police Office, Sindhuli, Poush 2080*

| Head no. | Head | Annual appropriation (Rs.) | Expenditure up to Magh (Rs.) | Expenditure of Poush (Rs.) | Uncleared advance (Rs.) | Available balance (Rs.) |
|---|---|---|---|---|---|---|
| 21111 | Remuneration | 4,20,000 | 1,50,000 | 28,000 | — | 2,70,000 |
| 22111 | Uniform | 45,000 | 7,500 | 1,500 | — | 37,500 |
| 22311 | Office materials | 20,000 | 9,000 | 1,800 | — | 11,000 |
| 22612 | Travelling expenses | 75,000 | 30,000 | 6,000 | 4,000 | 41,000 |
| 22711 | Miscellaneous | 36,000 | 11,000 | 2,200 | — | 25,000 |
| | **Total** | **5,96,000** | **2,07,500** | **39,500** | **4,000** | **3,84,500** |

**Answer.** Total appropriation Rs. 5,96,000; expenditure to date Rs. 2,07,500; Poush expenditure Rs. 39,500; uncleared advance Rs. 4,000; available balance Rs. 3,84,500.
**What it means.** The uncleared advance is money already committed. If it were ignored, the office would think it had Rs. 3,88,500 available and would overdraw the head by Rs. 4,000.
:::

## 10.7 Budget release, budget transfer and re-appropriation

Money does not arrive all at once. The appropriation is voted for the year; the money is **released** to the office in instalments.

**Budget release (बजेट निकासा).** A release is the amount made available to an office against its appropriation, usually month by month or quarter by quarter, and it is credited to the office's account. The office may not spend more than what has been released, even if the annual appropriation is larger. The release is recorded by a **निकासा भौचर** and entered as a debit in the bank cash book.

**Budget transfer (बजेटान्तर).** A transfer moves budget from one head to another, or from one office to another, **within the same office** or between offices of the same level, with the approval of the prescribed authority. It is used when one head is short and another has more than it will use.

**Re-appropriation.** Re-appropriation is the transfer of savings from one head to another **within the same office's budget**, usually with the approval of the ministry or the higher office, and subject to the limits laid down in the Financial Procedures Rules. Amounts may not be re-appropriated out of certain protected heads, such as remuneration and the foreign loan service, and a re-appropriation may not be used to create a **new** item of expenditure that the legislature never approved.

```figure caption="Types of budget movement. A release makes money available; a transfer and a re-appropriation move it between heads; none of them increases the total the legislature voted."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,2.5))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6)
ax.add_patch(FancyBboxPatch((3.4,4.3),3.2,1.2,boxstyle="round,pad=0.05",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(5.0,4.9,"Annual appropriation\nvoted by the legislature",ha='center',va='center',fontsize=6.8,color=INK)
ax.add_patch(FancyArrowPatch((3.3,4.6),(1.9,3.2),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((5.0,4.25),(5.0,3.2),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((6.7,4.6),(8.1,3.2),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.1))
for x,t,c in ((0.3,"Release\n(बजेट निकासा)\nmoney made available",ACCENT),
              (3.6,"Transfer\n(बजेटान्तर)\nbetween offices",MUTED),
              (6.9,"Re-appropriation\nbetween heads of the\nsame office",SERIES[1])):
    ax.add_patch(FancyBboxPatch((x,1.4),2.8,1.7,boxstyle="round,pad=0.05",fc="#f6f8fc",ec=c,lw=1.0))
    ax.text(x+1.4,2.25,t,ha='center',va='center',fontsize=5.9,color=INK)
ax.text(5.0,0.6,"None of the three increases the total the legislature voted",ha='center',fontsize=6.2,color=MUTED)
```

## 10.8 Journal vouchers for government transactions

A **journal voucher (भौचर)** is the document on which a single government transaction is recorded, in the double-entry form. Government offices use a small family of vouchers, and a student must be able to tell them apart.

| Voucher | Used for |
|---|---|
| **गोश्वारा भौचर (transfer journal voucher)** | A transfer between heads or accounts where no money leaves the office — clearing an advance, transferring between budget heads, adjusting a deposit |
| **निकासा भौचर (payment voucher)** | A payment: salary, goods, works, an advance, a refund of a deposit |
| **आम्दानी भौचर (revenue voucher)** | A receipt: revenue collected, a budget release, a deposit received |
| **प्रतिभूति/धरौटी भौचर (retention voucher)** | Money withheld from a contractor and its later release or forfeiture |

**The rules for writing a government journal voucher.**

1. Write the date, the voucher number and the office's code.
2. Name the **budget head number and the head** for every entry — a voucher without a head is not acceptable.
3. Use the double-entry form in full: the account debited first, then "To" the account credited, and a short narration in brackets beginning "Being ...".
4. Attach the evidence — the bill, the receipt, the measurement book entry, the sanction order.
5. Get the signature of the officer authorised to pass the payment, and of the person who checked it.
6. Enter the voucher in the bank cash book and in the head-wise ledger on the same day.

::: example Government journal vouchers
**Problem.** Pass the journal vouchers for the following transactions of a District Administration Office.
(a) Budget release of Rs. 8,00,000 received from the DTCO against the annual appropriation.
(b) A payment order of Rs. 1,20,000 issued against 21111 remuneration for the salary of the month, after deducting provident fund Rs. 18,000 and income tax Rs. 2,000.
(c) Furniture purchased for Rs. 90,000 against 31121, the supplier paid by payment order.
(d) The provident fund and income tax deducted were deposited into the concerned office.

**Solution.**
Step 1 — (a) Money received against the appropriation is a debit to the bank and a credit to the release account.
*Bank A/c Dr. 8,00,000*
*To Budget release A/c 8,00,000*
(Being the budget release received from the DTCO for the year.)
Step 2 — (b) Salary totals Rs. 1,20,000 + 18,000 + 2,000 = Rs. 1,40,000; only Rs. 1,20,000 is paid in cash.
*21111 Remuneration A/c Dr. 1,40,000*
*To Provident fund payable A/c 18,000*
*To Income tax payable A/c 2,000*
*To DTCO A/c 1,20,000*
(Being the salary payment order issued for the month after the prescribed deductions.)
Step 3 — (c) Capital expenditure creating an asset.
*31121 Furniture and fixtures A/c Dr. 90,000*
*To DTCO A/c 90,000*
(Being a payment order issued for the purchase of furniture.)
Step 4 — (d) The deductions are paid over; they were never the office's money.
*Provident fund payable A/c Dr. 18,000*
*Income tax payable A/c Dr. 2,000*
*To Bank A/c 20,000*
(Being the deductions deposited into the concerned office.)

**Answer.** The four vouchers above. Note that only (a) and (d) touch the bank account; (b) and (c) touch the DTCO account, because the Treasury and Comptroller Office makes the actual payment.
:::

::: caution The common mistakes
Three mistakes cost most of the marks in this unit. First, **recording the gross salary as a bank payment** — only the net amount leaves the bank, because the deductions are still held by the office. Second, **treating a release as revenue** — a budget release is not government income, it is the office's own appropriation being made available; the money is debited to the bank and credited to the release account, never to a revenue head. Third, **forgetting the uncleared advance** in the statement of expenditure, which overstates the available balance and leads the office to overspend.
:::

## Chapter summary

- **Expenditure (appropriation) accounting** records what an office spends against its approved budget head, the advances it gives and recovers, the deductions it holds and its bank balance.
- An expenditure is **regular** only when it is within the approved head, for the approved purpose, supported by evidence, sanctioned by the authorised officer, actually incurred and recorded in the prescribed formats.
- The key terms are **appropriation** (what the legislature voted), **release** (what has been made available) and **expenditure** (what has been spent). $Available\ balance = Appropriation - Expenditure - Uncleared\ advances$.
- **Expenditure codes** follow the uniform chart of accounts: the organisational classification says who spends; the economic classification says what, with **2** for recurrent (21111 remuneration, 22111 uniform, 22311 office materials, 22612 fuel, 22711 miscellaneous) and **3** for capital (31111 machinery, 31121 furniture, 31131 vehicles).
- The **formats** are the payment order, the vouchers (गोश्वारा, निकासा, आम्दानी, धरौटी), the advance register, the **bank cash book (No. 209)**, the head-wise ledger, the **statement of expenditure** and the deposit and retention ledgers.
- A **payment order** authorises the Treasury and Comptroller Office to pay. A payment is either **final** or an **advance**; an advance is a recoverable debt, cleared on the bill, and an uncleared advance is deducted from the available balance.
- The **bank cash book (A.G.F. No. 209)** shows the date, voucher number, particulars, debit (receipts), credit (payments) and the running balance. Budget release, revenue and refunds are debits; expenditure, advances and payments over of deductions are credits.
- The **statement of expenditure** reports, head by head, the annual appropriation, the cumulative and monthly expenditure, the uncleared advance and the available balance. It is the document on which further releases are made.
- **Budget release** makes money available; **budget transfer** moves budget between offices; **re-appropriation** moves savings between heads of the same office. None of them increases the total the legislature voted, and protected heads may not be raided.
- **Journal vouchers** in government accounting always name the budget head, follow the double-entry form with a narration, carry the evidence, and are signed by the authorised officer. The **गोश्वारा भौचर** records a transfer where no money moves.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is expenditure accounting? <span class="marks">[1]</span>
2. What is appropriation? <span class="marks">[1]</span>
3. What is a budget release? <span class="marks">[1]</span>
4. Write the code for office materials and for furniture. <span class="marks">[1]</span>
5. What is a payment order? <span class="marks">[1]</span>
6. What is an advance? <span class="marks">[1]</span>
7. What is a गोश्वारा भौचर? <span class="marks">[1]</span>
8. What is the number of the bank cash book format? <span class="marks">[1]</span>
9. Write any two items entered on the debit side of the bank cash book. <span class="marks">[1]</span>
10. What is a statement of expenditure? <span class="marks">[1]</span>
11. How is the available balance of a budget head found? <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Expenditure accounting is the branch of government accounting that records a government office's spending against its approved budget heads, its advances and their clearance, the deductions it holds and its bank balance.
**2.** Appropriation is the amount voted by the legislature for a particular budget head for the financial year.
**3.** A budget release is the amount of the appropriation actually made available to the office by the Treasury and Comptroller Office, usually month by month or quarter by quarter.
**4.** Office materials 22311; furniture and fixtures 31121.
**5.** A payment order is the document by which a government office authorises the Treasury and Comptroller Office to pay a stated amount to a stated person against a stated budget head.
**6.** An advance (पेस्की) is money paid to an officer or supplier before the bill is produced; it is a recoverable debt of that person to the government, not an expenditure.
**7.** The गोश्वारा भौचर is the transfer journal voucher used where no money leaves the office — clearing an advance, transferring between heads, or adjusting a deposit.
**8.** म.ले.प.फा.नं. २०९ (A.G.F. No. 209).
**9.** Any two of: budget release received, revenue deposited, retention and deductions received, refund of an unspent advance, amount transferred in.
**10.** The statement of expenditure is the monthly return sent to the Treasury and Comptroller Office showing head by head the annual appropriation, the expenditure to date, the expenditure of the month, the uncleared advances and the available balance.
**11.** Available balance = annual appropriation − total expenditure to date − uncleared advances.
:::

**Group B — Short answer (5 marks each)**

1. What is expenditure accounting? Explain the codes used in expenditure accounting. <span class="marks">[5]</span>
2. Explain the formats used in expenditure accounting and reporting. <span class="marks">[5]</span>
3. What is a payment order? Explain the kinds of payment and the procedure for clearing an advance. <span class="marks">[5]</span>
4. Prepare the bank cash book for the month of Bhadra from the following transactions of a District Coordination Unit (no opening balance). 04/02 budget release received Rs. 4,00,000; 04/06 payment order for office materials Rs. 60,000; 04/12 advance to a section officer for furniture Rs. 40,000; 04/25 salary payment order for Rs. 1,60,000 after deducting provident fund Rs. 24,000 and income tax Rs. 4,000; 04/28 the deductions deposited. <span class="marks">[5]</span>
5. Explain budget release, budget transfer and re-appropriation. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definition as in Group A answer 1. Codes: expenditure is coded in the uniform chart of accounts, in two parts — the organisational classification (ministry, department, office) and the economic classification. In the economic code the first digit separates **2 recurrent** from **3 capital**; the remaining digits identify the group and the head — 21111 remuneration, 21112 allowances, 21121 office materials, 22111 uniform, 22311 travelling expenses, 22612 fuel, 22711 miscellaneous; 31111 machinery and equipment, 31121 furniture and fixtures, 31131 vehicles. Explain that a wrong code conceals a capital purchase among running expenses.
**2.** Payment order — the authority to pay; vouchers — गोश्वारा भौचर for a transfer, निकासा भौचर for a payment, आम्दानी भौचर for a receipt, धरौटी भौचर for retention; advance register — advances and their clearance; bank cash book (No. 209) — the office's cash and bank record; head-wise ledger — appropriation, release and expenditure by head; statement of expenditure — the monthly return; deposit and retention ledgers — money held for others. Explain the purpose of each: to let a person who was not present reconstruct the transaction, and so to make it auditable.
**3.** A payment order is the document by which the office authorises the Treasury and Comptroller Office to pay a stated amount to a stated person against a stated head, naming the purpose and the sanction. Kinds of payment: **final** (bill received and checked) and **advance** (money needed before the bill). Procedure for clearing an advance: the advance is paid by payment order and entered in the advance register and bank cash book; the officer later submits the bill with vouchers and any unspent balance; if the bill equals the advance the advance is cleared against the expenditure head; if the bill is larger the excess is paid by a further payment order; if it is smaller the unspent cash is refunded; and any advance left uncleared at the year end is deducted from the available balance.
**4.**

| Date | Voucher no. | Particulars | Debit (Rs.) | Credit (Rs.) | Balance (Rs.) |
|---|---|---|---|---|---|
| 04/02 | 1 | Budget release received from the DTCO | 4,00,000 | | 4,00,000 |
| 04/06 | 2 | Payment order — 22311 office materials | | 60,000 | 3,40,000 |
| 04/12 | 3 | Advance to section officer — 31121 furniture | | 40,000 | 3,00,000 |
| 04/25 | 4 | Salary of Bhadra, net of provident fund Rs. 24,000 and income tax Rs. 4,000 | | 1,32,000 | 1,68,000 |
| 04/28 | 5 | Provident fund and income tax deposited | | 28,000 | 1,40,000 |
| 04/30 | | Balance c/d | | 1,40,000 | — |
| | | **Total** | **4,00,000** | **4,00,000** | |

**5.** A **budget release** makes part of the appropriation available to the office, month by month or quarter by quarter; it is recorded by a निकासा भौचर and credited to the office's account, and the office may not spend more than the release. A **budget transfer** moves budget from one head to another or from one office to another with the approval of the prescribed authority. **Re-appropriation** moves savings from one head to another within the same office's budget, subject to the limits in the Financial Procedures Rules; amounts may not be taken out of protected heads such as remuneration, and re-appropriation may not be used to create a new item of expenditure that the legislature never approved.
:::

**Group C — Long answer (8 marks each)**

1. What is a bank cash book? Explain its columns and the rules for its preparation, and state which items are entered on the debit side and which on the credit side. <span class="marks">[8]</span>
2. The following transactions relate to the District Administration Office, Rasuwa. Prepare the bank cash book for the month of Ashoj (no opening balance). 2082/06/01 payment order issued for house rent Rs. 10,000; 06/05 advance given to Mr. Rai for the purchase of office furniture Rs. 50,000; 06/12 budget release received from the DTCO Rs. 3,00,000; 06/15 Mr. Rai's advance cleared on a furniture bill of Rs. 58,000, the excess paid by payment order; 06/22 salary payment order for the month issued after deducting provident fund Rs. 20,000 and income tax Rs. 3,000 out of a total salary of Rs. 1,80,000; 06/28 the deductions deposited into the concerned office. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Meaning (2).* The bank cash book, म.ले.प.फा.नं. २०९, is the operating level office's combined record of its bank account, showing all money received and paid with a running balance; it is the principal book of an office that uses operating level accounting.
*Columns (2).* Date; voucher number; particulars of the transaction; debit (money received); credit (money paid); balance.
*Debit side (2).* Budget release received, revenue deposited, retention and deductions received, refund of an unspent advance, amount transferred in from another head.
*Credit side (2).* Expenditure paid, advances paid, retention and deductions paid over or refunded, amounts transferred out, and the closing balance carried down. Add the rules: enter in date order with the voucher number; carry a running balance; total both sides; reconcile with the passbook every month and send a copy with the monthly statement of expenditure.
**2.**

| Date | Voucher no. | Particulars | Debit (Rs.) | Credit (Rs.) | Balance (Rs.) |
|---|---|---|---|---|---|
| 06/01 | 1 | Payment order — house rent | | 10,000 | (10,000) |
| 06/05 | 2 | Advance to Mr. Rai — furniture | | 50,000 | (60,000) |
| 06/12 | 3 | Budget release received from the DTCO | 3,00,000 | | 2,40,000 |
| 06/15 | 4 | Excess of the furniture bill over the advance paid (58,000 − 50,000) | | 8,000 | 2,32,000 |
| 06/22 | 5 | Salary of Ashoj, net of provident fund Rs. 20,000 and income tax Rs. 3,000 | | 1,57,000 | 75,000 |
| 06/28 | 6 | Provident fund and income tax deposited | | 23,000 | 52,000 |
| 06/30 | | Balance c/d | | 52,000 | — |
| | | **Total** | **3,00,000** | **3,00,000** | |

Note: the advance of Rs. 50,000 is *not* an expenditure; when the bill of Rs. 58,000 is received the advance is cleared and only the excess of Rs. 8,000 is a fresh payment. The furniture head (31121) finally carries Rs. 58,000 of expenditure. Closing balance Rs. 52,000 (debit), subject to reconciliation with the passbook.
:::

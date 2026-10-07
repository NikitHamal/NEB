---
subject: Accountancy (कार्यालय सञ्चालन तथा लेखा)
grade: 10
title: Bank Reconciliation Statement (बैंक हिसाब मिलान)
unit: 5
hours: 5
area: Business Accounting
---

A trader keeps a **cash book** with a bank column. The bank keeps its own record of the same account, and sends the trader a **passbook** or a bank statement. In theory the two balances should be identical, because they are two records of one account. In practice they hardly ever are, and the reason is almost never a mistake — it is **time**. A cheque written today may reach the bank five days later. This unit explains why the two balances differ, how to write the **bank reconciliation statement** that explains the difference, and how to adjust the cash book when the bank has done something the trader has not yet recorded.

::: key What the examiner tests here
This unit carries a numerical question in almost every paper. Either Group B gives you a cash book balance and four or five discrepancies and asks for a bank reconciliation statement, or Group C gives you the same and asks for a statement plus an adjusted cash book. The marks are awarded for the **correct starting balance**, the **correct treatment of each item** and the **arithmetic**. Learn the table format; do not write a paragraph.
:::

## 5.1 Bank reconciliation statement: meaning, need and causes of difference

A **bank reconciliation statement (बैंक हिसाब मिलान विवरण)** is a statement prepared on a particular date to explain the difference between the balance of the bank column of the **cash book** and the balance shown by the **passbook** (or bank statement) for the same account, and to make the two agree.

The two records are the same account seen from two sides.

| Cash book (bank column) | Passbook |
|---|---|
| Kept by the trader | Kept by the bank |
| The trader's own record of what he has paid in and drawn out | The bank's record of what has actually been credited and debited |
| Written when the trader issues or receives a cheque | Written when the cheque actually reaches and is cleared by the bank |
| A **debit** balance means money in the bank (an asset) | A **credit** balance means money in the bank |
| A **credit** balance means an overdraft | A **debit** balance means an overdraft |

Note the trap: a debit balance in the cash book is a credit balance in the passbook. The two books record the same transaction on opposite sides, so their balances are mirror images.

```photo id="acc10/passbook" caption="A bank passbook. Every entry here was made by the bank, not by the account holder — which is exactly why the passbook and the cash book can disagree on any given day." width="66"
```

**Need for a bank reconciliation statement.**

1. To check the accuracy of both records and to find errors made by the trader **or by the bank**.
2. To find out the **real balance** available and hence how much can safely be drawn.
3. To detect dishonoured cheques, unauthorised or forgotten charges, and direct deposits that the trader has missed.
4. To find out the true bank balance for the balance sheet when the final accounts are prepared.
5. To discourage fraud: a cashier who has misappropriated money usually tries to hide it in the bank balance. Reconciliation finds it.
6. It is required by auditors, and by the bank itself before sanctioning further credit.

**Causes of difference.** Every cause falls into one of three classes.

```figure caption="Why the two balances diverge. The trader records a cheque the day he issues it; the bank records it the day it is presented. Everything between those two days is a timing difference."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.text(2.5,9.2,"Trader's cash book",ha='center',fontsize=8,color=ACCENT,weight='bold')
ax.text(7.5,9.2,"Bank's passbook",ha='center',fontsize=8,color=SERIES[1],weight='bold')
cb=["Cheque issued,\nentered at once","Cheque deposited,\nentered at once","Bank charges,\nnot yet known"]
pb=["Cheque presented\nsome days later","Cheque collected\nsome days later","Charges debited\nimmediately"]
for i,(a,b) in enumerate(zip(cb,pb)):
    y = 7.4 - i*2.3
    ax.add_patch(FancyBboxPatch((0.3,y-0.75),4.0,1.5,boxstyle="round,pad=0.05",fc="#eaf1ff",ec=ACCENT,lw=1.0))
    ax.text(2.3,y,a,ha='center',va='center',fontsize=6.8,color=INK)
    ax.add_patch(FancyBboxPatch((5.7,y-0.75),4.0,1.5,boxstyle="round,pad=0.05",fc="#fdf3f3",ec=SERIES[1],lw=1.0))
    ax.text(7.7,y,b,ha='center',va='center',fontsize=6.8,color=INK)
    ax.add_patch(FancyArrowPatch((4.35,y),(5.65,y),arrowstyle="-|>",mutation_scale=9,color=MUTED,lw=1.0,connectionstyle="arc3,rad=0.12"))
```

**Causes, classified.**

| Class | Examples | Effect on the difference |
|---|---|---|
| **Cheques issued but not yet presented for payment** | A cheque given to a supplier on 25 Chaitra is presented on 2 Baisakh | Cash book balance is lower than the passbook balance |
| **Cheques deposited but not yet collected or credited** | A cheque paid in on 28 Chaitra is cleared on 3 Baisakh | Cash book balance is higher than the passbook balance |
| **Items recorded by the bank only** | Bank charges and commission, interest on overdraft, interest allowed on the deposit, dividend or interest collected by the bank, a customer's direct deposit, standing instructions paid by the bank such as insurance premium or loan instalment, dishonour of a cheque deposited | Depends on whether the item increased or decreased the bank balance |
| **Errors** | A wrong amount posted in the cash book, a wrong total, a transposition, a cheque entered twice, an amount credited to the wrong account by the bank | Depends on the error |
| **Adjusted cash book** | Items that appear only in the passbook are first brought into the cash book | Then a fresh reconciliation is drawn up for timing differences only |

## 5.2 Effect of transactions on the cash book and on the passbook

Before writing a statement, work out for each item what it did to each record.

| Item | Effect on cash book (bank column) | Effect on passbook |
|---|---|---|
| Cheque issued | Decreases (credited) | No effect until presented |
| Cheque issued and presented | Decreases | Decreases |
| Cheque deposited | Increases (debited) | No effect until collected |
| Cheque deposited and collected | Increases | Increases |
| Bank charges, commission | No effect | Decreases |
| Interest allowed by bank | No effect | Increases |
| Interest on overdraft charged | No effect | Decreases |
| Customer deposits directly into the bank | No effect | Increases |
| Standing instruction paid by bank | No effect | Decreases |
| Cheque deposited but dishonoured | No effect (until known) | Decreases |

::: caution Direction, not memory
Do not try to memorise a list of "add" and "less". Ask one question each time: *does this item make the bank's record higher or lower than the trader's?* A cheque issued but not presented means the trader has already reduced his book while the bank has not — so the bank's balance is **higher**, and when you start from the cash book balance you **add** it.
:::

## 5.3 Preparing a bank reconciliation statement from the cash book balance

**Format.** The usual form starts with the cash book balance and works towards the passbook balance.

| Particulars | Amount (Rs.) | Amount (Rs.) |
|---|---|---|
| Balance as per cash book (Dr) | | xxx |
| **Add:** cheques issued but not presented for payment | xx | |
| **Add:** interest allowed or collected by the bank, not entered in the cash book | xx | |
| **Add:** amount deposited directly by a customer into the bank | xx | |
| **Add:** any wrong credit given by the bank in the passbook | xx | |
| | | xxx |
| **Less:** cheques deposited but not yet collected by the bank | xx | |
| **Less:** bank charges, commission or interest on overdraft not entered in the cash book | xx | |
| **Less:** a cheque deposited and later dishonoured | xx | |
| **Less:** standing instructions paid by the bank | xx | |
| **Less:** any wrong debit made by the bank in the passbook | xx | |
| **Balance as per passbook (Cr)** | | **xxx** |

If the cash book shows an **overdraft** (a credit balance in the bank column), the statement starts from that overdraft and the additions and deductions are **reversed**.

::: example From the cash book balance
**Problem.** From the following particulars of a trader as on 30 Chaitra, prepare a bank reconciliation statement.

i. Cash book showed a bank balance of Rs. 50,000 (debit).
ii. A cheque of Rs. 12,000 was issued but not presented for payment.
iii. A cheque of Rs. 8,000 was deposited but not collected by the bank.
iv. Bank charges of Rs. 1,500 were debited only in the passbook.
v. Interest on investment of Rs. 6,000 was collected by the bank and appears only in the passbook.
vi. A customer directly deposited Rs. 9,000 into the bank, not recorded in the cash book.

**Solution.**
Step 1 — Start with the cash book balance: Rs. 50,000.
Step 2 — Cheque issued but not presented (ii): the trader has already reduced his book, the bank has not, so the bank's balance is higher → **add Rs. 12,000**.
Step 3 — Interest collected by the bank (v): this increases the bank balance and is missing from the cash book → **add Rs. 6,000**.
Step 4 — Customer's direct deposit (vi): same reasoning → **add Rs. 9,000**.
Step 5 — Cheque deposited but not collected (iii): the trader has already increased his book, the bank has not → **less Rs. 8,000**.
Step 6 — Bank charges (iv): the bank has reduced the balance, the trader does not know → **less Rs. 1,500**.
Step 7 — Total the two sides.

| Particulars | Amount (Rs.) | Amount (Rs.) |
|---|---|---|
| Balance as per cash book | | 50,000 |
| Add: cheque issued but not presented | 12,000 | |
| Add: interest on investment collected by the bank | 6,000 | |
| Add: amount deposited directly by a customer | 9,000 | 27,000 |
| | | 77,000 |
| Less: cheque deposited but not collected | 8,000 | |
| Less: bank charges debited by the bank | 1,500 | 9,500 |
| **Balance as per passbook** | | **67,500** |

**Answer.** Balance as per passbook Rs. 67,500.
:::

## 5.4 Preparing a bank reconciliation statement from the passbook balance

When the question gives the **passbook** balance, the statement is written the other way round: start with the passbook balance and work towards the cash book balance. The same items appear, with their treatment reversed.

| Particulars | Amount (Rs.) |
|---|---|
| Balance as per passbook (Cr) | xxx |
| **Add:** cheques deposited but not yet collected by the bank | xx |
| **Add:** bank charges, commission, interest on overdraft | xx |
| **Add:** standing instructions paid by the bank | xx |
| **Less:** cheques issued but not yet presented for payment | xx |
| **Less:** interest or dividend collected by the bank | xx |
| **Less:** amount deposited directly by a customer | xx |
| **Balance as per cash book (Dr)** | **xxx** |

**Overdraft.** If either balance is an overdraft, write the heading as "Balance as per cash book (Cr) — overdraft" and remember that all the adjustments now move in the opposite direction from the normal case. The safest method is to reason out each item's effect rather than to memorise.

::: example From the passbook balance
**Problem.** On 31 Ashad the passbook of a firm showed a credit balance of Rs. 40,000. Prepare a bank reconciliation statement from the following.
i. Cheques issued but not presented for payment: Rs. 15,000.
ii. Cheques deposited but not collected: Rs. 7,000.
iii. Bank charges not entered in the cash book: Rs. 500.
iv. Interest allowed by the bank: Rs. 2,500.

**Solution.**
Step 1 — Start with the passbook balance Rs. 40,000.
Step 2 — Cheques deposited but not collected (ii): the trader has already added them in his book, the bank has not credited them, so the **cash book balance is higher** by Rs. 7,000 → add.
Step 3 — Bank charges (iii): the bank has reduced the passbook, the trader's book still shows the higher figure → the cash book balance is higher by Rs. 500 → add.
Step 4 — Cheques issued but not presented (i): the trader has reduced his book, the bank has not → the **cash book balance is lower** by Rs. 15,000 → less.
Step 5 — Interest allowed (iv): the bank has added it, the trader has not → the cash book balance is lower by Rs. 2,500 → less.
Step 6 — Total.

| Particulars | Amount (Rs.) | Amount (Rs.) |
|---|---|---|
| Balance as per passbook | | 40,000 |
| Add: cheques deposited but not collected | 7,000 | |
| Add: bank charges not entered in the cash book | 500 | 7,500 |
| | | 47,500 |
| Less: cheques issued but not presented | 15,000 | |
| Less: interest allowed by the bank | 2,500 | 17,500 |
| **Balance as per cash book** | | **30,000** |

**Answer.** Balance as per cash book Rs. 30,000 (debit).
:::

## 5.5 Adjusted cash book method

The bank reconciliation statement explains a difference, but it does not correct the trader's books. So long as the bank charges, the interest and the direct deposits are missing from the cash book, the trader's balance is wrong. The **adjusted cash book method** first brings all those items into the cash book and then prepares a short reconciliation for the timing differences that remain.

**Step 1 — Adjust the cash book.** Enter in the bank column of the cash book every item that appears **only in the passbook**:

| Add (increase the balance) | Less (reduce the balance) |
|---|---|
| Interest allowed by the bank | Bank charges, commission, incidental charges |
| Dividend or interest collected by the bank | Interest on overdraft |
| Direct deposit by a customer | Standing instructions paid by the bank |
| Amount wrongly debited by the bank, now corrected | Cheque deposited and later dishonoured |

**Step 2 — Find the adjusted balance** (old balance ± the above).

**Step 3 — Prepare the reconciliation** from the adjusted cash book balance to the passbook balance, using only the items that cause a **time difference**: cheques issued but not presented (add) and cheques deposited but not collected (less), plus any uncorrected error.

::: example Adjusted cash book and a short statement
**Problem.** The cash book of Sita Traders showed a bank balance of Rs. 36,000 on 31 Chaitra. On comparing it with the passbook the following were found.
i. Bank charges Rs. 400 and interest on overdraft Rs. 1,100 had been debited by the bank only.
ii. A customer had deposited Rs. 5,000 directly into the bank.
iii. A cheque of Rs. 3,000 deposited earlier had been dishonoured.
iv. Cheques of Rs. 14,000 issued were not presented for payment; cheques of Rs. 6,000 deposited were not yet collected.
Prepare the adjusted cash book and the bank reconciliation statement.

**Solution.**
Step 1 — Identify the items that appear only in the passbook: (i), (ii) and (iii). These adjust the cash book.
Step 2 — Identify the items that are timing differences: (iv). These stay in the reconciliation.

*Adjusted cash book (bank column)*

| Particulars | Amount (Rs.) | Particulars | Amount (Rs.) |
|---|---|---|---|
| To Balance b/d | 36,000 | By Bank charges | 400 |
| To Customer's direct deposit | 5,000 | By Interest on overdraft | 1,100 |
| | | By Cheque dishonoured | 3,000 |
| | | By Balance c/d (adjusted) | 36,500 |
| **Total** | **41,000** | **Total** | **41,000** |

Step 3 — Adjusted cash book balance $= 41{,}000 - 4{,}500 = Rs.\ 36{,}500$.
Step 4 — Prepare the reconciliation from Rs. 36,500.

*Bank reconciliation statement as on 31 Chaitra*

| Particulars | Amount (Rs.) | Amount (Rs.) |
|---|---|---|
| Balance as per adjusted cash book | | 36,500 |
| Add: cheques issued but not presented | | 14,000 |
| | | 50,500 |
| Less: cheques deposited but not collected | | 6,000 |
| **Balance as per passbook** | | **44,500** |

**Answer.** Adjusted cash book balance Rs. 36,500; balance as per passbook Rs. 44,500.
**What it means.** Only the two timing items now separate the books. Every genuine difference — the charges, the interest, the direct deposit and the dishonoured cheque — has been brought into the trader's own record, so the cash book now shows what the bank balance really is.
:::

## Chapter summary

- A **bank reconciliation statement** explains, on a given date, the difference between the bank column of the **cash book** and the **passbook**, and makes the two agree.
- The cash book is the trader's record, written when a cheque is issued or received; the passbook is the bank's record, written when the cheque actually reaches the bank. A **debit** balance in the cash book is a **credit** balance in the passbook.
- Its **need**: to check accuracy, to find the true bank balance, to detect dishonoured cheques and unauthorised charges, to prepare the balance sheet, to prevent fraud and to satisfy the auditor.
- **Causes of difference**: cheques issued but not presented; cheques deposited but not collected; items recorded by the bank only (bank charges, interest, collection of dividends, direct deposits, standing instructions, dishonoured cheques); and errors in either book.
- Working from the **cash book** balance: **add** cheques issued but not presented, interest and dividends collected by the bank, direct deposits and wrong credits by the bank; **less** cheques deposited but not collected, bank charges and interest on overdraft, dishonoured cheques, standing instructions and wrong debits by the bank.
- Working from the **passbook** balance reverses every item. Where either balance is an **overdraft**, reason out each item instead of using the list.
- In the **adjusted cash book method**, items appearing only in the passbook are first entered in the cash book to find an adjusted balance; then the reconciliation is drawn using only the timing differences — cheques issued but not presented (add) and cheques deposited but not collected (less) — and any uncorrected error.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is a bank reconciliation statement? <span class="marks">[1]</span>
2. Write any two causes of the difference between the cash book and the passbook. <span class="marks">[1]</span>
3. What does a debit balance in the cash book (bank column) mean? <span class="marks">[1]</span>
4. If the cash book shows an overdraft, what kind of balance does the passbook show? <span class="marks">[1]</span>
5. A cheque of Rs. 5,000 issued on 28 Chaitra is presented on 4 Baisakh. In which book is it recorded on 31 Chaitra? <span class="marks">[1]</span>
6. Where is interest allowed by the bank recorded? <span class="marks">[1]</span>
7. Write any two items that are recorded by the bank only. <span class="marks">[1]</span>
8. A cheque deposited was dishonoured. Which book shows it first? <span class="marks">[1]</span>
9. When cheques are issued but not presented, is the passbook balance higher or lower than the cash book balance? <span class="marks">[1]</span>
10. What is meant by the adjusted cash book? <span class="marks">[1]</span>
11. Name the statement prepared to bring the cash book and the passbook into agreement. <span class="marks">[1]</span>

::: note Answers to Group A
**1.** A statement prepared on a particular date to explain and reconcile the difference between the balance shown by the bank column of the cash book and the balance shown by the passbook.
**2.** Any two of: cheques issued but not presented, cheques deposited but not collected, bank charges, interest allowed or charged by the bank, direct deposit by a customer, standing instructions, dishonoured cheque, errors.
**3.** A debit balance in the cash book (bank column) means money is lying in the bank — a favourable balance.
**4.** A debit balance — an overdraft in the cash book is a debit balance in the passbook.
**5.** Only in the cash book; the bank will record it when the cheque is presented in Baisakh.
**6.** Only in the passbook, until the trader enters it in the cash book or it is adjusted.
**7.** Any two of: bank charges and commission, interest allowed or charged, dividend collected, direct deposit by a customer, standing instructions, dishonour of a cheque.
**8.** The passbook shows it first; the trader learns of it afterwards.
**9.** Higher — the trader has already reduced his cash book, the bank has not.
**10.** The cash book after all items that appear only in the passbook have been entered in it, so that the remaining difference is only a matter of time.
**11.** The bank reconciliation statement.
:::

**Group B — Short answer (5 marks each)**

1. What is a bank reconciliation statement? Explain any four causes of the difference between the cash book and the passbook. <span class="marks">[5]</span>
2. The cash book of a firm showed a bank balance of Rs. 65,000 on 30 Chaitra. Cheques issued but not presented Rs. 12,000; cheques deposited but not collected Rs. 8,000; bank charges Rs. 1,500; interest on investment collected by the bank Rs. 6,000; a customer deposited Rs. 9,000 directly into the bank. Prepare the bank reconciliation statement. <span class="marks">[5]</span>
3. The passbook of a trader showed a credit balance of Rs. 55,000 on 31 Ashad. Cheques issued but not presented Rs. 20,000; cheques deposited but not collected Rs. 9,000; bank charges Rs. 800; interest allowed by the bank Rs. 3,800. Prepare the bank reconciliation statement. <span class="marks">[5]</span>
4. Explain the effect on the cash book and on the passbook of: (a) a cheque issued, (b) a cheque deposited, (c) bank charges, (d) a direct deposit by a customer, (e) a dishonest dishonour of a cheque deposited. <span class="marks">[5]</span>
5. Why is a bank reconciliation statement prepared? Explain any five reasons. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definition as in Group A answer 1. Causes: (i) cheques issued but not yet presented for payment — the cash book balance is lower; (ii) cheques deposited but not yet collected — the cash book balance is higher; (iii) bank charges, commission and interest on overdraft debited by the bank only; (iv) interest, dividend and direct deposits credited by the bank only; (iv) standing instructions paid by the bank; (v) dishonour of a cheque deposited; (vi) errors in either book. (Any four explained.)
**2.**

| Particulars | Rs. | Rs. |
|---|---|---|
| Balance as per cash book | | 65,000 |
| Add: cheque issued but not presented | 12,000 | |
| Add: interest on investment collected by bank | 6,000 | |
| Add: direct deposit by a customer | 9,000 | 27,000 |
| | | 92,000 |
| Less: cheque deposited but not collected | 8,000 | |
| Less: bank charges | 1,500 | 9,500 |
| **Balance as per passbook** | | **82,500** |

**3.**

| Particulars | Rs. | Rs. |
|---|---|---|
| Balance as per passbook | | 55,000 |
| Add: cheques deposited but not collected | 9,000 | |
| Add: bank charges | 800 | 9,800 |
| | | 64,800 |
| Less: cheques issued but not presented | 20,000 | |
| Less: interest allowed by the bank | 3,800 | 23,800 |
| **Balance as per cash book** | | **41,000** |

**4.** (a) Cheque issued — cash book decreases at once; the passbook is unaffected until the cheque is presented. (b) Cheque deposited — cash book increases at once; the passbook is unaffected until the cheque is collected. (c) Bank charges — no effect on the cash book until known; the passbook decreases at once. (d) Direct deposit by a customer — no effect on the cash book until known; the passbook increases at once. (e) Cheque deposited dishonoured — the passbook decreases when the bank returns it; the cash book must then be corrected. (Note: the phrase in the question is a typo for "dishonour".)
**5.** (i) To check the accuracy of both records and to trace errors of the trader or of the bank. (ii) To find the real bank balance available for drawing and for the balance sheet. (iii) To detect dishonoured cheques, bank charges and direct deposits that the trader has missed. (iv) To prevent and detect fraud by a cashier. (v) Because it is required by the auditor and by the bank before granting further credit.
:::

**Group C — Long answer (8 marks each)**

1. What is a bank reconciliation statement? Explain its need and the causes which make the cash book and the passbook differ, and show the usual format starting from the cash book balance. <span class="marks">[8]</span>
2. On 31 Chaitra the cash book of Himal Traders showed a bank balance of Rs. 42,000. On comparing it with the passbook the following were found. (a) Cheques of Rs. 18,000 issued had not been presented. (b) Cheques of Rs. 9,000 deposited had not been collected. (c) Bank charges Rs. 600 and interest on overdraft Rs. 900 had been debited by the bank only. (d) A customer had deposited Rs. 7,500 directly into the bank. (e) A cheque of Rs. 4,000 deposited earlier was dishonoured. Prepare the adjusted cash book and the bank reconciliation statement. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Definition (1).* As in Group A answer 1.
*Need (3).* Accuracy check on both books; finding the true bank balance; detecting dishonoured cheques, missed charges and direct deposits; preparing the balance sheet; preventing fraud; satisfying the auditor and the bank.
*Causes (2).* Timing: cheques issued but not presented, cheques deposited but not collected. Bank-only entries: bank charges and commission, interest allowed or charged, dividend or interest collected, direct deposits, standing instructions, dishonoured cheques. Errors: in the cash book or in the passbook.
*Format (2).* Start with the cash book balance; add cheques issued but not presented, interest collected by the bank, direct deposits and wrong credits by the bank; less cheques deposited but not collected, bank charges and interest on overdraft, dishonoured cheques, standing instructions and wrong debits by the bank; arrive at the passbook balance. Show the table.
**2.**
*Adjusted cash book*

| Particulars | Rs. | Particulars | Rs. |
|---|---|---|---|
| To Balance b/d | 42,000 | By Bank charges | 600 |
| To Customer's direct deposit | 7,500 | By Interest on overdraft | 900 |
| | | By Cheque dishonoured | 4,000 |
| | | By Balance c/d (adjusted) | 44,000 |
| **Total** | **49,500** | **Total** | **49,500** |

Adjusted balance $= 49{,}500 - 5{,}500 = Rs.\ 44{,}000$.
*Bank reconciliation statement as on 31 Chaitra*

| Particulars | Rs. | Rs. |
|---|---|---|
| Balance as per adjusted cash book | | 44,000 |
| Add: cheques issued but not presented | | 18,000 |
| | | 62,000 |
| Less: cheques deposited but not collected | | 9,000 |
| **Balance as per passbook** | | **53,000** |
:::

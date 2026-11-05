---
subject: Financial Accounting
grade: BCA Semester 7
unit: 4
title: Bank Reconciliation Statement
hours: 6
area: BCA 403 · Financial Accounting · Unit 4
---

On the last day of Ashad a shop's cash book shows a bank balance of Rs 45,200, but the statement from the bank (the **pass book**) says Rs 52,550. Nobody has made a mistake with the money; the two records describe the same account from two sides and are written at different moments. The **Bank Reconciliation Statement (BRS)** explains the difference item by item. It is a control: an account that cannot be reconciled hides errors, delays or fraud.

::: key What this unit gives you
- Why the cash book (bank column) and the pass book differ.
- Which differences need a cash book entry and which are only timing differences.
- Three standard layouts: starting from the cash book, from the pass book, and with an overdraft.
- A program that adjusts the cash book and proves both balances meet.
:::

## 4.1 Cash book versus pass book

The **cash book** is the business's own record. The **pass book** (bank statement) is the bank's record of the same account, in the bank's own view: a *deposit* in the cash book is a debit, but the bank, which owes the money to the customer, shows it as a **credit**. The roles of debit and credit are therefore reversed between the two books. This reversal is a common source of confusion; remember that a favourable balance is a debit in the cash book but a credit in the pass book.

## 4.2 Causes of difference

**A. Timing differences** (the business has recorded the item and the bank has not yet; **no cash book entry is needed**):

1. **Cheques issued but not yet presented** for payment: the cash book is already reduced, the bank balance is not.
2. **Cheques deposited but not yet cleared/credited**: the cash book is already increased, the pass book is not.

**B. Items the bank has recorded but the business has not yet; each needs a correcting entry in the cash book:**

3. **Bank charges and commission**, debited by the bank.
4. **Interest credited** on a savings or fixed account.
5. **Direct deposits** by customers (for example by connectIPS, bank transfer or standing instruction) that appear first on the statement.
6. **Direct payments** by the bank on the customer's behalf: insurance premium, loan instalment, electricity bill by standing order.
7. **Dishonoured (bounced) cheques**: a customer cheque the cash book showed as received is returned unpaid.
8. **Errors** in the cash book (wrong amount, wrong side) found during checking.

::: caution
Do not adjust the cash book for items in group A. A cheque that is merely *unpresented* has already been correctly recorded; adding it again would double-count it. Group A items appear **only** in the reconciliation statement.
:::

## 4.3 Preparing the BRS: step by step

1. Compare the cash book bank column with the pass book entry by entry; tick the matches.
2. List the *unticked* items on each side.
3. Update the cash book for every group B item; this gives the **adjusted cash book balance**.
4. Reconcile the pass book balance to the adjusted cash book balance using group A items only.

The two directions of the reconciliation formula, for a **favourable (debit)** cash book balance, are:

| To go from | Add | Subtract |
|---|---|---|
| Adjusted cash book → pass book | Cheques issued but not presented | Cheques deposited but not credited |
| Pass book → adjusted cash book | Cheques deposited but not credited | Cheques issued but not presented |

With an **overdraft**, signs reverse because the balance is credit-natured: cheques issued not presented *reduce* the overdraft shown in the pass book.

## 4.4 Worked schedule

::: example A full reconciliation
The unadjusted cash book balance (debit) is Rs 45,200. The pass book shows Rs 52,550. Comparison reveals:

- Cheques issued, not yet presented: Rs 12,000
- Cheques deposited, not yet credited: Rs 8,500
- Bank charges not in the cash book: Rs 350
- Interest credited by the bank: Rs 1,200
- Direct deposit by a customer: Rs 6,000
- Customer cheque dishonoured: Rs 3,000
:::

Step 3: the cash book is corrected for group B items. Bank charges and the dishonoured cheque reduce it; interest and the direct deposit increase it:

45,200 − 350 + 1,200 + 6,000 − 3,000 = **Rs 49,050**

Step 4: starting from the pass book balance Rs 52,550, subtract the cheques issued but not presented (they have not yet left the bank) and add the cheques deposited but not credited (they have not yet reached the bank). The result must equal the adjusted cash book balance. The program carries out both steps.

```python
cash_book = 45200
adjustments = {"bank charges": -350, "interest credited": +1200,
               "direct deposit": +6000, "dishonoured cheque": -3000}
adjusted = cash_book + sum(adjustments.values())
print(f"adjusted cash book balance: {adjusted}")

pass_book = 52550
unpresented, uncleared = 12000, 8500
reconciled = pass_book - unpresented + uncleared
print(f"reconciled bank balance: {reconciled}")
assert adjusted == reconciled
```
```output
adjusted cash book balance: 49050
reconciled bank balance: 49050
```
The two printed lines agree, so every difference has been explained. Notice that the unpresented cheque and the uncleared deposit never changed the adjusted figure: they only bridge the pass book to it.

## 4.5 Journal entries after the BRS

The corrections are posted to the cash book and ledger as ordinary entries:

| Item | Entry |
|---|---|
| Bank charges Rs 350 | Dr Bank Charges 350, Cr Bank 350 |
| Interest Rs 1,200 | Dr Bank 1,200, Cr Interest Income 1,200 |
| Direct deposit Rs 6,000 | Dr Bank 6,000, Cr Debtors 6,000 |
| Dishonoured cheque Rs 3,000 | Dr Debtors 3,000, Cr Bank 3,000 |

The debtor's account is **re-debited** on dishonour because the customer again owes the money. Once these entries are made, the Bank account in the ledger shows Rs 49,050, the figure that appears on the balance sheet.

## 4.6 Stale cheques and good practice

A cheque not presented within its validity period (usually six months in Nepal's banking practice; check the bank's rule) is **stale**. The business reverses the original payment entry (Dr Bank, Cr the payee) and issues a replacement if the payee still has a claim. Good practice: reconcile at least monthly, by someone other than the person who writes cheques, investigate any item outstanding for more than a few weeks, and keep a signed copy of each statement.

::: note
An unreconciled difference is not "rounding". Treat any residue as an error to be found, using the same tools as in Unit 3: check transpositions (multiple of 9), a double-sided posting error (twice the amount) and omitted entries.
:::

## 4.7 Seeing the ideas: the cheque, the two balances and the bridge between them

```photogrid label="4.1" cols="2" ratio="1.0" caption="(a) A bank cheque of 1909: the cheque is the usual cause of a cash-book and pass-book difference, because the day it is written is not the day the bank pays it. (b) The anatomy of a modern cheque; each labelled field is what the bank checks before it pays and the firm records in the cash book."
@ photo id="bca403/cheque" cap="Bank cheque, 1909"
fit 1.0
focus 0.35 0.5
@ svg cap="Cheque anatomy"
f = Fig(300, 300)
f.box(8, 20, 284, 190, "", fill="#ffffff", stroke=NAVY)
L = [("Date (BS or AD)", 28, 150, 28, MINT, TEAL), ("Pay: payee name", 62, 270, 26, BLUE, NAVY), ("Amount in words", 94, 270, 26, BLUE, NAVY), ("A/C Payee crossing", 126, 160, 26, SAND, AMBER), ("Rs figures", 126, 104, 26, SAND, AMBER), ("Signature", 164, 140, 28, ROSE, RED), ("Cheque no.", 164, 124, 28, MINT, TEAL)]
f.box(18, 28, 150, 26, "Date (BS or AD)", fill=MINT, stroke=TEAL, size=12.5)
f.box(18, 60, 264, 26, "Payee name", fill=BLUE, stroke=NAVY, size=12.5)
f.box(18, 92, 264, 26, "Amount in words", fill=BLUE, stroke=NAVY, size=12.5)
f.box(18, 124, 150, 26, "A/C Payee crossing", fill=SAND, stroke=AMBER, size=12.5)
f.box(178, 124, 104, 26, "Rs figures", fill=SAND, stroke=AMBER, size=12.5)
f.box(18, 164, 124, 36, "Cheque no. + bank code", fill=MINT, stroke=TEAL, size=12.5)
f.box(152, 164, 130, 36, "Signature of drawer", fill=ROSE, stroke=RED, size=12.5)
f.text(150, 238, "Words and figures must agree;", size=12.5, color=SLATE, italic=True)
f.text(150, 258, "an altered cheque is refused.", size=12.5, color=SLATE, italic=True)
```

```svgfig label="4.1" caption="The bridge between the two balances of the worked schedule. Left: the cash book is corrected for four items the bank already knew (net +3,850), giving 49,050. Right: the pass book is corrected for timing (12,000 not yet presented, 8,500 not yet credited), giving the same 49,050."
f = Fig(580, 262)
f.text(150, 16, "Cash book route", size=12.5, color=NAVY, bold=True)
C = [("Cash book (unadjusted)", "45,200", BLUE, NAVY), ("- Bank charges", "-350", ROSE, RED), ("+ Interest credited", "+1,200", MINT, TEAL), ("+ Direct deposit", "+6,000", MINT, TEAL), ("- Dishonoured cheque", "-3,000", ROSE, RED), ("Adjusted cash book", "49,050", SAND, AMBER)]
for i, (t, v, fl, st) in enumerate(C):
    y = 26 + i * 36
    f.box(10, y, 190, 30, "", fill=fl, stroke=st)
    f.text(18, y + 15, t, size=11, color=NAVY, anchor="start", vmid=True, bold=(i in (0, 5)))
    f.text(192, y + 15, v, size=11, color=st, anchor="end", vmid=True, bold=True)
f.text(430, 16, "Pass book route", size=12.5, color=NAVY, bold=True)
D = [("Pass book balance", "52,550", BLUE, NAVY), ("- Cheques issued, not presented", "-12,000", ROSE, RED), ("+ Deposits not yet credited", "+8,500", MINT, TEAL), ("Reconciled bank balance", "49,050", SAND, AMBER)]
for i, (t, v, fl, st) in enumerate(D):
    y = 26 + i * 36 if i < 3 else 26 + 5 * 36
    f.box(300, y, 270, 30, "", fill=fl, stroke=st)
    f.text(308, y + 15, t, size=11, color=NAVY, anchor="start", vmid=True, bold=(i in (0, 3)))
    f.text(562, y + 15, v, size=11, color=st, anchor="end", vmid=True, bold=True)
f.arrow([(200, 224), (300, 224)], color=TEAL, sw=2, both=True, label="agree", lpos=(250, 214))
```

```svgfig label="4.2" caption="Sorting the six differences of the schedule. Timing items need no entry because the bank will catch up; items the bank knew first must be entered in the cash book."
f = Fig(580, 196)
f.box(190, 8, 200, 32, "Difference found", fill=NAVY, color="#ffffff", bold=True, size=12)
f.arrow([(250, 40), (150, 66)], color=SLATE); f.arrow([(330, 40), (430, 66)], color=SLATE)
f.box(30, 66, 240, 34, "Timing: bank will catch up", fill=SAND, stroke=AMBER, bold=True, size=11.5)
f.box(310, 66, 240, 34, "Bank knew first: not in cash book", fill=MINT, stroke=TEAL, bold=True, size=11.5)
f.box(30, 116, 240, 60, "Cheques issued, not presented 12,000\nDeposits not credited 8,500\n-> bridge only, no journal entry", fill="#ffffff", stroke=AMBER, size=11)
f.box(310, 116, 240, 60, "Bank charges 350, interest 1,200\nDirect deposit 6,000, dishonour 3,000\n-> correct the cash book by entries", fill="#ffffff", stroke=TEAL, size=11)
```

### 4.7.1 Eight benefits of preparing a bank reconciliation every month

1. **It finds mistakes by the firm.** A cheque entered as Rs 5,600 instead of Rs 6,500 appears as a difference. The bank's record is an independent check on the cash book. Correcting it early keeps the balance trustworthy.
2. **It finds mistakes by the bank.** Banks also make errors, such as posting a deposit to another account. A monthly comparison catches it while the paper trail is fresh. Complaints made late are harder to prove.
3. **It exposes fraud.** A forged or altered cheque, or a clerk who takes cash and delays the deposit, shows up as an unexplained difference. Regular reconciliation by someone who does not handle cash is a core control. Many small Nepali firms have been caught this way.
4. **It records unrecorded items.** Bank charges, interest and direct credits through ConnectIPS or Fonepay may be unknown until the statement arrives. The reconciliation tells the accountant to enter them. Without it, profit is wrong.
5. **It shows true available cash.** The cash book may show Rs 49,050 while the pass book shows Rs 52,550. Knowing the cheques still to clear helps decide what can be spent. This avoids dishonour for lack of funds.
6. **It tracks dishonoured cheques.** A customer cheque returned unpaid must be debited back to the customer. The reconciliation reminds the firm to chase payment. Delay lets a bad debt grow.
7. **It supports audit.** An auditor asks for the reconciliation at the year end and compares it with the statement. A clean, signed schedule shortens the audit. A missing one raises doubts about all the cash records.
8. **It follows up stale cheques.** A cheque unpresented for six months may be out of date. The schedule lists it so it can be cancelled and reissued. Old cheques that stay on the list distort the picture.

```photogrid label="4.2" cols="2" ratio="1.0" caption="The bridge between two balances. (a) A bank counter: the bank's pass book and the firm's cash book describe the same money from two sides, so they differ for timing reasons. (b) The cash book shows Rs 50,000. It has not yet recorded a customer's direct deposit of Rs 5,000 or bank charges of Rs 500, so the adjusted cash book balance is 50,000 + 5,000 - 500 = Rs 54,500. The bank has not yet paid cheques of Rs 12,000 that the firm issued, and has not yet credited cheques of Rs 8,000 that the firm deposited. Starting from the adjusted cash book, the pass book balance is 54,500 + 12,000 - 8,000 = Rs 58,500, and every rupee of the difference is explained. Only the first two items need a journal entry in the firm's books; the other two correct themselves when the bank clears the cheques."
@ photo id="bcafa/teller" cap="A bank counter"
fit 1.0
focus 0.5 0.5
@ svg cap="From cash book to pass book, in rupees"
cb, dep, chg, unp, unc = 50000, 5000, 500, 12000, 8000
adj = cb + dep - chg; pb = adj + unp - unc
assert adj == 54500 and pb == 58500
steps = [("cash book", cb, 0, True), ("+ direct deposit", dep, 1, False), ("- bank charges", -chg, 1, False), ("+ unpresented chq", unp, 1, False), ("- uncredited dep.", -unc, 1, False), ("pass book", pb, 0, True)]
f = Fig(300, 240)
f.text(150, 14, "waterfall (thousand rupees)", size=10.5, color=NAVY, bold=True)
x0, sc = 112, 140 / 60.0
run = 0; y = 24
for lab, v, rel, tot in steps:
    if tot:
        a, b = 0, v; run = v
    else:
        a, b = run, run + v; run = b
    lo, hi = min(a, b), max(a, b)
    col = "#1d6fb8" if tot else ("#0f766e" if v > 0 else "#b91c1c")
    f.text(106, y + 9, lab, size=10, color=NAVY, anchor="end", vmid=True)
    f.box(x0 + lo / 1000 * sc, y, max((hi - lo) / 1000 * sc, 2), 18, "", fill=col, stroke=col, r=0)
    f.text(x0 + hi / 1000 * sc + 4, y + 9, f"{v / 1000:+.1f}" if not tot else f"{v / 1000:.1f}", size=10.5, color=col, anchor="start", bold=True, vmid=True)
    y += 28
f.text(150, 206, "adjusted cash book 54.5", size=10.5, color=SLATE)
f.text(150, 224, "54.5 + 12 - 8 = 58.5, nothing left over", size=10.5, color=TEAL, bold=True)
```

## 4.8 Summary and exercises

The BRS bridges the cash book and the pass book. Timing items stay out of the books and appear only in the statement; bank-originated items force correcting entries and produce the adjusted cash book balance, which then reconciles to the pass book.

1. List four timing differences and four differences that need a cash book entry.
2. The cash book shows a bank balance of Rs 30,000. Cheques issued not presented total Rs 5,000, cheques deposited not credited Rs 2,500, interest credited Rs 400 and charges Rs 150 are unrecorded. Find the pass book balance.
3. Starting from an overdraft in the pass book of Rs 18,000, cheques issued not presented Rs 6,000 and deposits not credited Rs 4,000, find the overdraft in the cash book.
4. Explain why debit and credit are reversed in a bank statement.
5. A customer cheque of Rs 7,500 is dishonoured. Give the entry in the business's books.
6. Why is it a control weakness if the same person writes cheques and prepares the BRS?

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Why do the cash book and the pass book differ? List the causes.**

*Introduction.* The cash book is the firm's record of its bank account; the pass book (bank statement) is the bank's record. They seldom agree on the same date, though both describe one account.

*Causes (Figure 4.2).*

1. **Cheques issued but not yet presented**: the firm has credited the cash book, but the bank has not yet paid.
2. **Cheques deposited but not yet credited** (uncleared): the firm has debited it, but the bank is still collecting.
3. **Bank charges and interest** entered by the bank and not yet by the firm.
4. **Direct deposits** by customers (for example by ConnectIPS) that the firm has not seen.
5. **Dishonoured cheques**: the bank has debited the account back.
6. **Standing orders and direct debits**, such as insurance.
7. **Errors** in either book.

Items 1 and 2 are timing differences; 3 to 6 need entries in the cash book. *Conclusion:* a bank reconciliation statement explains every difference.

**Q2 (5 marks). The unadjusted cash book shows Rs 45,200 and the pass book Rs 52,550. Cheques issued not presented Rs 12,000; deposited not credited 8,500; bank charges 350; interest credited 1,200; direct deposit 6,000; customer cheque dishonoured 3,000. Prepare the reconciliation.**

*Step 1: correct the cash book (Figure 4.1).*

| Item | Rs |
|---|---|
| Cash book balance (Dr) | 45,200 |
| Less bank charges | (350) |
| Add interest credited | 1,200 |
| Add direct deposit | 6,000 |
| Less dishonoured cheque | (3,000) |
| **Adjusted cash book** | **49,050** |

*Step 2: bridge from the pass book.* 52,550 − 12,000 + 8,500 = **49,050**.

The two results agree, so every difference is explained. *Entries:* Dr Bank charges 350, Cr Bank 350; Dr Bank 1,200, Cr Interest income 1,200; Dr Bank 6,000, Cr Debtors 6,000; Dr Debtors 3,000, Cr Bank 3,000. *Conclusion:* the unpresented cheque and the uncleared deposit never alter the adjusted figure; they only link the two books.

**Q3 (10 marks). Define a bank reconciliation statement. Explain its purpose, the steps of preparation and the journal entries that follow, using the figures of the schedule above.**

*Introduction.* A **bank reconciliation statement (BRS)** lists the items that explain the difference between the cash book bank balance and the pass book balance on a date. It is not a ledger account; it is a working schedule.

*Purposes.* To detect errors and fraud, to find unrecorded items, to show true available funds, to follow dishonoured and stale cheques, and to support audit.

*Steps.*

1. Tick the cash book against the pass book item by item.
2. List the unticked items on each side.
3. Separate timing items from items needing entry.
4. Correct the cash book for the items the bank knew first, giving the adjusted balance.
5. Start from the pass book balance and add or subtract the timing items.
6. Compare the two results; they must agree.
7. Post journal entries for the cash-book corrections.
8. Investigate anything still unexplained and file the signed statement.

*Statement (Figure 4.1).*

| Particulars | Rs |
|---|---|
| Balance as per pass book | 52,550 |
| Less cheques issued, not presented | (12,000) |
| Add cheques deposited, not credited | 8,500 |
| **Balance as per adjusted cash book** | **49,050** |

*Journal entries.*

| Dr | Cr | Rs |
|---|---|---|
| Bank charges | Bank | 350 |
| Bank | Interest income | 1,200 |
| Bank | Debtors (customer) | 6,000 |
| Debtors (customer) | Bank | 3,000 |

*Comparison of the two books.*

| Point | Cash book | Pass book |
|---|---|---|
| Kept by | the firm | the bank |
| Viewpoint | firm's asset (Dr balance) | bank's liability to the customer |
| Receipts | debit side | credit side |
| Payments | credit side | debit side |
| Overdraft | credit balance | debit balance |

*Good practice.* Reconcile monthly, by a person who does not handle cash, and follow up cheques older than six months.

*Conclusion.* Because the bank holds an independent record, reconciliation is the cheapest control over a firm's cash. A schedule that ends with equal figures (Rs 49,050) shows that each difference is understood.

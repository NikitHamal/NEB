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

## 4.7 Summary and exercises

The BRS bridges the cash book and the pass book. Timing items stay out of the books and appear only in the statement; bank-originated items force correcting entries and produce the adjusted cash book balance, which then reconciles to the pass book.

1. List four timing differences and four differences that need a cash book entry.
2. The cash book shows a bank balance of Rs 30,000. Cheques issued not presented total Rs 5,000, cheques deposited not credited Rs 2,500, interest credited Rs 400 and charges Rs 150 are unrecorded. Find the pass book balance.
3. Starting from an overdraft in the pass book of Rs 18,000, cheques issued not presented Rs 6,000 and deposits not credited Rs 4,000, find the overdraft in the cash book.
4. Explain why debit and credit are reversed in a bank statement.
5. A customer cheque of Rs 7,500 is dishonoured. Give the entry in the business's books.
6. Why is it a control weakness if the same person writes cheques and prepares the BRS?

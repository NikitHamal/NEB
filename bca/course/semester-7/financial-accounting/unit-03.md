---
subject: Financial Accounting
grade: BCA Semester 7
unit: 3
title: Subsidiary Books, Trial Balance and Error Rectification
hours: 6
area: BCA 403 · Financial Accounting · Unit 3
---

A wholesaler in Birgunj may issue two hundred invoices a day. Journalising each one individually, with a narration, would bury the accountant. The remedy is to divide the journal into **subsidiary books** (also called books of original entry or special journals), one per kind of repetitive transaction, and to post only their *totals* to the ledger. After posting, a **trial balance** checks the arithmetic of double entry, and a **suspense account** parks any unexplained difference until the errors are found.

::: key What this unit gives you
- The subsidiary books: purchases, sales, returns and cash books (single, double and triple column).
- Contra entries and discounts: trade vs cash discount.
- Preparing a trial balance, what it proves and what it cannot detect.
- Locating and rectifying errors, with a suspense account where needed.
:::

## 3.1 Purchases, sales and returns books

- **Purchases book** records credit purchases of goods for resale. **Sales book** records credit sales. Cash purchases and sales go to the cash book, and purchases of assets (not for resale) go to the journal proper.
- **Purchases returns (returns outward)** and **sales returns (returns inward)** books record goods sent back, supported by debit notes and credit notes respectively.
- A **trade discount** is a reduction from the list price given at the time of sale; it is *not recorded* in the books, only the net invoice amount is. A **cash discount** is an incentive for prompt payment; it *is* recorded, as *discount allowed* (an expense, on sales) or *discount received* (an income, on purchases).

VAT is shown in a separate column. The program below builds a two-invoice sales book: list prices Rs 50,000 and Rs 30,000, a 10% trade discount, and 13% VAT on the discounted value.

```python
invoices = [50000, 30000]
net = sum(p * 90 // 100 for p in invoices)
vat = net * 13 // 100
print(f"sales book: net {net}, VAT {vat}, gross {net + vat}")
```
```output
sales book: net 72000, VAT 9360, gross 81360
```
Net sales are Rs 72,000, VAT is Rs 9,360 and the debtors' total is Rs 81,360. Posting is by totals: Dr Debtors (per customer, from each invoice), Cr Sales for the net total, Cr VAT Output for the VAT total.

## 3.2 Cash books

The **cash book** is both a journal and a ledger: it records every cash and bank transaction in date order, and it *is* the Cash and Bank account, so it is not separately posted to a cash ledger account.

- **Single column:** cash only.
- **Double column:** cash and bank columns.
- **Triple column:** cash, bank and a **discount** column on each side. The discount-allowed total on the debit side and the discount-received total on the credit side are *not* balanced like cash and bank; they are posted to the Discount Allowed and Discount Received accounts at period end.

A **contra entry** is a transaction entirely between cash and bank (depositing cash, withdrawing cash). It appears on both sides of the cash book, once in each column, and needs no ledger posting. The letter C in the folio column marks it.

::: example A triple-column cash book
Opening balances: cash Rs 20,000, bank Rs 80,000. Transactions: (1) received Rs 15,000 cash from customer X, allowing Rs 500 discount; (2) deposited Rs 10,000 cash in the bank (contra); (3) paid supplier Y Rs 24,000 by cheque, receiving Rs 1,000 discount; (4) cash sales of Rs 30,000; (5) withdrew Rs 5,000 from the bank for office use (contra); (6) paid Rs 4,000 cash expenses.
:::

```python
dr = [("Balance b/d", 20000, 80000, 0), ("X (debtor)", 15000, 0, 500),
      ("Cash (contra)", 0, 10000, 0), ("Cash sales", 30000, 0, 0), ("Bank (contra)", 5000, 0, 0)]
cr = [("Bank (contra)", 10000, 0, 0), ("Y (creditor)", 0, 24000, 1000),
      ("Expenses", 4000, 0, 0), ("Cash (contra)", 0, 5000, 0)]
cash = sum(r[1] for r in dr) - sum(r[1] for r in cr)
bank = sum(r[2] for r in dr) - sum(r[2] for r in cr)
print(f"closing cash {cash}, closing bank {bank}")
```
```output
closing cash 56000, closing bank 61000
```
The cash column balances at Rs 56,000 and the bank column at Rs 61,000. Each contra entry appears in both lists: moving Rs 10,000 from cash to bank lowers the cash balance and raises the bank balance by the same amount, so the combined total of cash and bank is unchanged by contra entries.

::: caution
A **bank overdraft** is a *credit* balance in the bank column. Do not subtract it from a debit total as a "negative asset" without labelling it: on the balance sheet it appears as a current liability.
:::

## 3.3 Petty cash and the imprest system

Small expenses are met from a **petty cash book** under the **imprest system**: the petty cashier receives a fixed float (say Rs 5,000), pays small expenses against vouchers, and at period end is *reimbursed* the exact amount spent so that the float is restored. The analytical columns (postage, travel, refreshments) are totalled and posted to the matching expense accounts.

## 3.4 The trial balance

A **trial balance** lists every ledger balance, debit balances in one column and credit balances in the other, at a given date. Its totals must agree, because every transaction was recorded with equal debits and credits.

::: key What a trial balance proves
Agreement of the totals shows that the *arithmetic* of double entry is intact. It does **not** prove the books are correct: several errors leave the totals equal.
:::

Errors **not** revealed by the trial balance:

1. **Error of omission:** a transaction not recorded at all.
2. **Error of commission:** the right amount posted to the wrong account of the same class (a sale to Ram credited to Shyam).
3. **Error of principle:** wrong class of account (buying furniture debited to purchases).
4. **Compensating errors:** two errors of equal amount in opposite directions.
5. **Complete reversal:** debit and credit swapped.
6. **Error of original entry:** the wrong amount recorded on both sides.

Errors that **do** make the totals differ include: a one-sided posting, posting a different amount to each side, a transposition (5,400 written as 4,500), wrong addition of an account and balance carried wrongly.

## 3.5 Locating errors and the suspense account

A difference exactly divisible by **9** often signals a *transposition* or *slide* error: swapping two adjacent digits changes a number by a multiple of 9. A difference equal to twice an amount hints that an item was posted to the wrong side. If the error cannot be found immediately, the books are closed with the difference placed in a **suspense account** (credit if the debit side is heavier, debit if the credit side is heavier), and it is cleared when the error is found.

::: example Transposition and suspense
A credit sale to a debtor was Rs 5,400. The debtor was debited correctly with 5,400, but Sales was credited with 4,500. The trial balance showed debits of Rs 8,42,500 and credits of Rs 8,41,600.
:::

```python
debits = {"Cash": 56000, "Bank": 61000, "Debtors": 305400, "Purchases": 300000, "Rent": 60000, "Salaries": 60100}
credits = {"Capital": 400000, "Creditors": 150000, "Sales": 291600}
diff = sum(debits.values()) - sum(credits.values())
print(f"difference {diff}, divisible by 9: {diff % 9 == 0}")
susp_cr, susp_dr = diff, 0          # credit suspense balances the books
susp_dr += 900                      # rectification: Dr Suspense 900, Cr Sales 900
print(f"suspense after rectification: {susp_cr - susp_dr}")
```
```output
difference 900, divisible by 9: True
suspense after rectification: 0
```
The difference is Rs 900 (exactly 100 × 9) and the entry **Dr Suspense 900, Cr Sales 900** clears it, restoring Sales to its true figure and returning the suspense balance to zero.

## 3.6 Rectification principles

Rectify in the **period the error is found**:

- Errors that affected the trial balance go through the suspense account. Errors that did not are corrected by a journal entry directly between the accounts concerned.
- *Commission* (sale to Ram credited to Shyam): Dr Shyam, Cr Ram. *Principle* (furniture debited to Purchases, Rs 20,000): Dr Furniture 20,000, Cr Purchases 20,000. *Omission:* record the transaction now. *Complete reversal:* debit and credit the amount twice the original.
- If an error affected profit, adjust profit as well; corrected profit equals reported profit plus or minus the effect of each error, keeping a clear statement of corrected profit.

## 3.7 Summary and exercises

Subsidiary books keep detail manageable, the triple-column cash book handles cash, bank and discounts together, and the trial balance and suspense account give a first, imperfect line of defence against error.

1. Distinguish trade discount from cash discount, with the entry for each.
2. Record in a triple-column cash book: opening cash Rs 12,000 and bank Rs 40,000; deposit of Rs 6,000 cash; cheque received of Rs 9,000 from a debtor, discount Rs 300.
3. State six errors that the trial balance cannot reveal, with one example each.
4. A trial balance disagrees by Rs 1,260 (credits larger). Show why a transposition is plausible and prepare the suspense entry.
5. Furniture costing Rs 30,000 was debited to Purchases. Journalise the correction.
6. Explain why a bank overdraft is a liability even though it is a bank-column balance.

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

## 3.7 Seeing the ideas: books of prime entry, the three-column cash book and the hunt for a difference

```photogrid label="3.1" cols="2" ratio="1.0" caption="(a) A bound account book: before computers a business kept separate books for purchases, sales and cash, and the clerk who posted them kept the whole trade readable. (b) The ruled layout of a three-column cash book: cash, bank and discount are three columns on each side, so one page carries the day's money in and out."
@ photo id="bca403/ledger" cap="Bound account book"
fit 1.0
focus 0.5 0.5
@ svg cap="Three-column cash book"
f = Fig(300, 300)
f.box(8, 8, 284, 30, "Dr  CASH BOOK  Cr", fill=NAVY, color="#ffffff", bold=True, size=13)
f.line(150, 38, 150, 250, color=SLATE, sw=2)
H = [("Disc", 8, 36), ("Cash", 44, 50), ("Bank", 94, 50)]
for t, x, w in H:
    f.box(x, 44, w, 22, t, fill=SAND, stroke=AMBER, size=12.5, bold=True)
    f.box(x + 142, 44, w, 22, t, fill=SAND, stroke=AMBER, size=12.5, bold=True)
rows = [("Balance b/d", "10,000", "40,000", "Bank (contra)", "6,000", ""), ("Cash (contra)", "", "6,000", "Supplier", "", "9,800"), ("Customer", "", "12,000", "Balance c/d", "4,000", "48,200")]
for i, r in enumerate(rows):
    y = 90 + i * 50
    f.text(12, y, r[0], size=12.5, color=NAVY, bold=True, anchor="start")
    f.text(12, y + 20, r[1] + "  " + r[2], size=12.5, color=SLATE, anchor="start")
    f.text(154, y, r[3], size=12.5, color=RED, bold=True, anchor="start")
    f.text(154, y + 20, r[4] + "  " + r[5], size=12.5, color=SLATE, anchor="start")
f.text(150, 276, "contra = cash and bank on both sides", size=12.5, color=TEAL, italic=True)
```

```svgfig label="3.1" caption="Where each transaction is first recorded. High-volume transactions go to subsidiary books, which are totalled and posted to the ledger once a period; the journal proper takes whatever is left (opening entries, adjustments, rectifications)."
f = Fig(580, 214)
f.box(8, 90, 120, 46, "Transaction\n+ document", fill=MINT, stroke=TEAL, bold=True, size=11.5)
B = [("Purchases book", 8), ("Sales book", 52), ("Returns books", 96), ("Cash book", 140), ("Journal proper", 184)]
for t, y in B:
    f.box(210, y - 6, 140, 30, t, fill=BLUE if y < 184 else SAND, stroke=NAVY if y < 184 else AMBER, size=11)
    f.arrow([(128, 113), (210, y + 9)], color=SLATE)
    f.arrow([(350, y + 9), (420, 113)], color=SLATE)
f.box(420, 88, 150, 50, "General ledger\n(accounts)", fill=ROSE, stroke=RED, bold=True, size=12)
```

```svgfig label="3.2" caption="The transposition hunt of 3.5. Sales should be credited 5,400 but 4,500 was posted. Debits exceed credits by 900, which is divisible by 9, the signature of swapped adjacent digits. A suspense credit of 900 balances the books until the error is found and cleared."
f = Fig(580, 200)
f.box(14, 14, 168, 44, "Debtor debited 5,400\n(correct)", fill=MINT, stroke=TEAL, size=11.5)
f.box(14, 74, 168, 44, "Sales credited 4,500\n(digits swapped)", fill=ROSE, stroke=RED, size=11.5)
f.arrow([(182, 36), (214, 80)], color=SLATE); f.arrow([(182, 96), (214, 90)], color=SLATE)
f.box(214, 56, 150, 54, "Trial balance\nDr 8,42,500\nCr 8,41,600", fill=SAND, stroke=AMBER, size=11.5)
f.arrow([(364, 83), (394, 83)], color=SLATE)
f.box(394, 40, 176, 86, "Difference 900\n900 / 9 = 100\nso suspect a\ntransposition", fill=BLUE, stroke=NAVY, size=11.5)
f.box(14, 146, 270, 40, "Temporary: Cr Suspense 900", fill="#ffffff", stroke=AMBER, size=11.5, bold=True)
f.box(300, 146, 270, 40, "Rectify: Dr Suspense 900, Cr Sales 900", fill="#ffffff", stroke=TEAL, size=11.5, bold=True)
f.arrow([(284, 166), (300, 166)], color=SLATE)
```

### 3.7.1 Eight good habits of cash-book and trial-balance work

1. **Record cash and bank daily.** The cash book is both a book of original entry and a ledger, so it should be written on the day of each transaction. A shop that records weekly forgets small payments. Daily entries also make theft easy to notice.
2. **Count the cash each evening.** Compare the cash book balance with the cash in the drawer and note any difference. A shortage of Rs 50 found today is easy to trace, but one found next month is not. This is the oldest and cheapest control.
3. **Use the imprest system for petty cash.** Give the cashier a fixed float, say Rs 5,000, and refill it by the exact amount spent. Each expense needs a voucher. The reimbursement cheque then equals the vouchers, which keeps small spending honest.
4. **Show contra entries on both sides.** When Rs 6,000 cash is deposited into the bank, it appears on the debit side in the bank column and on the credit side in the cash column. Writing it on one side only is a common mistake. Mark such lines with the letter C.
5. **Keep discounts in their own column.** Cash discount allowed to customers and received from suppliers are separate nominal accounts. The totals of the discount columns are posted at the period end. Netting them into the cash amount hides the cost of early payment.
6. **Total the subsidiary books before posting.** Add the purchases, sales and returns books at the month end, check the totals and post only the totals. One posting instead of many reduces the chance of an error. Nepali shops that issue hundreds of VAT bills a month save hours this way.
7. **Divide a difference by 9.** If the trial balance is out by an amount divisible by 9, look for a transposition or a slide first. If it equals twice an amount, look for an item posted to the wrong side. A systematic search is faster than rechecking every page.
8. **Never force the trial balance.** Putting a difference into a suspense account is allowed only as a clearly labelled temporary step. Find the error and rectify it by a proper entry. A forced balance hides a real fault and misleads whoever reads the statements.

```photogrid label="3.2" cols="2" ratio="1.0" caption="Why the difference in a trial balance is a clue. (a) An adding machine: the totals of a trial balance are only as good as the figures entered. (b) A small business has debit balances Cash 45,000, Debtors 30,000, Stock 25,000, Purchases 20,000 and Rent 7,500, total Rs 1,27,500, and credit balances Capital 80,000, Creditors 22,000 and Sales 25,500, total Rs 1,27,500. If the Sales balance is copied as 25,050 (the digits 5 and 0 swapped), the credit total becomes 1,27,050 and the trial balance disagrees by Rs 450. A difference that divides exactly by 9 (450 / 9 = 50) is the signature of a transposition, so the accountant checks swapped digits first. The difference is parked in a Suspense Account (credit 450) until the error is found and rectified. A trial balance that agrees does not prove the books are right: errors of omission, compensating errors and errors of principle do not disturb the totals."
@ photo id="bcafa/adder" cap="A mechanical adding machine"
fit 1.0
focus 0.5 0.5
@ svg cap="Debit and credit totals with the 450 gap"
dr = {"Cash": 45000, "Debtors": 30000, "Stock": 25000, "Purchases": 20000, "Rent": 7500}
cr_ok = {"Capital": 80000, "Creditors": 22000, "Sales": 25500}
cr_bad = dict(cr_ok, Sales=25050)
D = sum(dr.values()); C0 = sum(cr_ok.values()); C1 = sum(cr_bad.values())
assert (D, C0, C1) == (127500, 127500, 127050) and D - C1 == 450 and 450 % 9 == 0 and 450 // 9 == 50
assert [d % 9 == 0 for d in (450, 100, 27, 90)] == [True, False, True, True]
f = Fig(300, 240)
f.text(150, 14, "trial balance totals (rupees)", size=10.5, color=NAVY, bold=True)
for i, (lab, v, col) in enumerate([("Debit", D, "#1d6fb8"), ("Credit, correct", C0, "#0f766e"), ("Credit, as copied", C1, "#b91c1c")]):
    y = 28 + i * 40
    f.text(10, y + 6, lab, size=10.5, color=NAVY, anchor="start", bold=True)
    w = 180 * v / D
    f.box(10, y + 14, w, 16, "", fill=col, stroke=col, r=0)
    f.text(14, y + 22, f"{v:,}", size=10.5, color="#ffffff", anchor="start", bold=True, vmid=True)
f.box(10, 152, 280, 76, "", fill="#f1f5f9", stroke=SLATE, r=6, sw=1)
f.text(150, 170, "difference 1,27,500 - 1,27,050 = 450", size=10.5, color=RED, bold=True)
f.text(150, 188, "450 / 9 = 50 exactly: swapped digits?", size=10.5, color=NAVY, bold=True)
f.text(150, 206, "tests: 450 yes, 100 no, 27 yes, 90 yes", size=10.5, color=SLATE)
f.text(150, 222, "park 450 Cr in Suspense", size=10.5, color=TEAL, bold=True)
```

## 3.8 Summary and exercises

Subsidiary books keep detail manageable, the triple-column cash book handles cash, bank and discounts together, and the trial balance and suspense account give a first, imperfect line of defence against error.

1. Distinguish trade discount from cash discount, with the entry for each.
2. Record in a triple-column cash book: opening cash Rs 12,000 and bank Rs 40,000; deposit of Rs 6,000 cash; cheque received of Rs 9,000 from a debtor, discount Rs 300.
3. State six errors that the trial balance cannot reveal, with one example each.
4. A trial balance disagrees by Rs 1,260 (credits larger). Show why a transposition is plausible and prepare the suspense entry.
5. Furniture costing Rs 30,000 was debited to Purchases. Journalise the correction.
6. Explain why a bank overdraft is a liability even though it is a bank-column balance.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). List the errors that a trial balance does not reveal, with an example of each.**

*Introduction.* A trial balance tests only the arithmetic of double entry. If the totals agree, it does **not** prove the books are correct, because some errors leave debits equal to credits.

| Error | Meaning | Example |
|---|---|---|
| Omission | transaction not recorded at all | a credit sale of Rs 4,000 never entered |
| Commission | right amount, wrong account of the same class | sale to Ram credited to Shyam |
| Principle | wrong class of account | furniture debited to Purchases |
| Compensating | two errors of equal amount that cancel | Sales over-added by 500 and Rent over-added by 500 |
| Complete reversal | debit and credit swapped | cash received debited to Cash as credit |
| Original entry | wrong amount on both sides | Rs 1,500 recorded as 1,050 in the journal |

*Errors that do show up:* a one-sided posting, different amounts on the two sides, a transposition in one posting and wrong addition of an account. *Conclusion:* agreement of the trial balance is necessary but not sufficient evidence of correct books.

**Q2 (5 marks). Prepare a three-column cash book from: opening cash Rs 10,000 and bank Rs 40,000; deposited cash in bank 6,000; received a cheque from a customer 12,000 and banked it; paid a supplier by cheque 9,800 after discount 200.**

*Method.* Cash receipts and the bank column are on the debit side, payments on the credit side; the discount column records discount allowed (debit) and discount received (credit). The deposit is a **contra** entry.

| Dr | Disc | Cash | Bank | Cr | Disc | Cash | Bank |
|---|---|---|---|---|---|---|---|
| Balance b/d | | 10,000 | 40,000 | Bank (C) | | 6,000 | |
| Cash (C) | | | 6,000 | Supplier | 200 | | 9,800 |
| Customer | | | 12,000 | Balance c/d | | 4,000 | 48,200 |
| | | 10,000 | 58,000 | | 200 | 10,000 | 58,000 |

Check: cash 10,000 − 6,000 = 4,000; bank 40,000 + 6,000 + 12,000 − 9,800 = 48,200. The discount received of 200 is posted to the Discount Received account (a gain). *Conclusion:* the cash book serves as journal and ledger together, and its two balances must equal the cash in hand and the bank's own figure after reconciliation.

**Q3 (10 marks). Explain the trial balance, its limits and the methods of locating errors. A trial balance shows debits of Rs 8,42,500 and credits of Rs 8,41,600. Find the cause and show the suspense account entries.**

*Introduction.* The **trial balance** lists every ledger balance in a debit and a credit column on a date. Its totals must agree because every entry has equal debits and credits (Figure 3.2).

*Limits.* It does not reveal errors of omission, commission, principle, compensating errors, complete reversal or errors of original entry (Q1).

*Method of locating a difference.*

1. Recheck the addition of the trial balance.
2. Find the difference and halve it: a difference of twice an amount suggests an item posted to the wrong side.
3. Check whether the difference is divisible by 9: a transposition (5,400 written as 4,500) or a slide changes a number by a multiple of 9.
4. Look for an item equal to the difference that was left out of the trial balance.
5. Recheck the postings and balances of the ledger accounts; then the subsidiary books and their totals.
6. If the error is still not found by the deadline, place the difference in a **suspense account** and continue.

*Application.* Difference = 8,42,500 − 8,41,600 = **Rs 900**. 900 ÷ 9 = 100, so a transposition is likely. A search finds that a credit sale of Rs 5,400 was debited to the debtor correctly but credited to Sales as 4,500.

*Entries.*

| Step | Entry | Effect |
|---|---|---|
| 1. To agree the trial balance | Cr Suspense 900 | credits become 8,42,500 |
| 2. Rectification | Dr Suspense 900, Cr Sales 900 | Sales is now 2,92,500 and suspense is nil |

*Comparison of error treatment.*

| Error type | Trial balance shows? | Correction |
|---|---|---|
| One-sided posting | yes | find and post the other side |
| Transposition | yes | Dr/Cr Suspense and the correct account |
| Commission | no | transfer between the two accounts |
| Principle | no | transfer from wrong to right class |

*Conclusion.* A trial balance is a first check, not a certificate. A systematic search, the divisible-by-9 test and a clearly labelled suspense account locate errors while the books stay in order, and every suspense balance must be cleared to zero before the final accounts.

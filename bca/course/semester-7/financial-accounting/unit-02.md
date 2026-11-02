---
subject: Financial Accounting
grade: BCA Semester 7
unit: 2
title: "Recording Transactions: Journal, VAT and TDS Entries, Ledger and T-Accounts"
hours: 7
area: BCA 403 · Financial Accounting · Unit 2
---

Every sale, purchase and payment leaves a trail: an invoice, a cheque stub, a bank voucher. Accounting turns each such **source document** into a *journal entry* (the first record, in date order) and then *posts* it to the **ledger** (the second record, grouped by account). In Nepal, that trail also carries two statutory layers that students must handle correctly from day one: **Value Added Tax (VAT) at 13%** and **Tax Deducted at Source (TDS)**.

::: key What this unit gives you
- The two systems for deciding what to debit and credit: traditional (golden) rules and the modern (accounting-equation) rule.
- How to journalise purchases and sales with VAT, and a payment of rent with TDS.
- How to post to ledger accounts, draw T-accounts and balance them.
- A small program that proves a set of entries is balanced and produces the account balances.
:::

## 2.1 Source documents and the journal

Documents come first: purchase invoice, sales invoice, debit note, credit note, receipt, cheque, bank deposit slip and payment voucher. Nepal's VAT rules require a tax invoice carrying the seller's PAN and the VAT charged separately. The **journal** records, for each transaction: date, the account(s) debited, the account(s) credited, amounts and a one-line **narration**. A transaction touching more than two accounts gives a *compound entry*.

## 2.2 Rules of debit and credit

Two equivalent rule sets are taught.

**Traditional (golden) rules**

| Account class | Rule |
|---|---|
| Personal | Debit the receiver, credit the giver |
| Real (assets) | Debit what comes in, credit what goes out |
| Nominal (income and expense) | Debit all expenses and losses, credit all incomes and gains |

**Modern rules (equation based)** follow from the table in Unit 1: debit increases in assets and expenses; credit increases in liabilities, equity and income.

::: example Which rule gives which entry?
*Goods bought for cash.* Under golden rules, goods are a real account (what comes in is debited), cash is real (what goes out is credited): **Dr Purchases, Cr Cash**. Under modern rules, purchases is an expense-type account (debit) and cash falls (credit). Both give the same entry; use whichever you can apply without error.
:::

## 2.3 VAT in the books

In Nepal, VAT is charged at a standard **13%** on taxable supplies. A VAT-registered business keeps two accounts: **VAT Input** (an asset, tax paid on purchases) and **VAT Output** (a liability, tax collected on sales). Each month the *net VAT* is the difference, and the business pays it to the Inland Revenue Department; if input exceeds output the excess is carried forward as a credit. VAT is **not** an expense or income of the business: it is collected on behalf of the government.

::: example Purchase and sale with VAT
*Purchase on credit from Himal Traders*, Rs 1,00,000 plus 13% VAT:

Dr Purchases 1,00,000; Dr VAT Input 13,000; Cr Himal Traders (creditor) 113,000.

*Sale on credit to a customer*, Rs 2,00,000 plus 13% VAT: Dr Debtors 2,26,000; Cr Sales 2,00,000; Cr VAT Output 26,000.

Net VAT payable is 26,000 − 13,000 = Rs 13,000.
:::

## 2.4 TDS entries

Under the Income Tax Act 2058, a payer of certain amounts (rent, service fees, interest, dividends and others) must deduct tax at a prescribed rate and deposit it with the Inland Revenue Department. The payee receives the net sum and claims the deducted tax as an advance against their own income tax. As a teaching figure this unit uses **10% on rent**; rates differ by payment type and are revised in each Finance Act, so confirm the current rate before applying it to a real case.

::: example Rent with TDS
The business pays monthly rent of Rs 50,000 and deducts 10% TDS (Rs 5,000), paying the landlord Rs 45,000 net:

Dr Rent Expense 50,000; Cr TDS Payable 5,000; Cr Cash 45,000.

When the TDS is later deposited: Dr TDS Payable 5,000; Cr Cash 5,000.
:::

## 2.5 Ledger posting and T-accounts

The **ledger** is the book of accounts. Each account is shown as a **T-account**: debits on the left, credits on the right.

```
        Cash Account
   Dr                    Cr
 Capital   500,000   Rent (net)     45,000
 Debtors   150,000   Himal Traders 113,000
```

Posting means copying each journal line into the named account with a cross-reference. To **balance** an account, total both sides, find the difference, and carry it down on the smaller side as the balance brought down (b/d). A debit balance is shown when debits exceed credits.

::: caution
Posting the amount to the correct account but on the **wrong side** (debit instead of credit) is a classic slip. It makes the trial balance differ by *twice* the amount, which is itself a diagnostic clue (Unit 3).
:::

## 2.6 A journal and ledger engine in Python

The program below holds six transactions as journal entries: capital Rs 5,00,000 in cash; the credit purchase with VAT; the credit sale with VAT; the rent payment with TDS; Rs 1,50,000 received from the debtor; and the creditor paid Rs 1,13,000. It refuses to accept an unbalanced entry, posts every line to ledger accounts, and prints the closing balances and the trial totals.

```python
entries = [
    ("capital introduced", [("Cash", 500000, 0), ("Capital", 0, 500000)]),
    ("credit purchase with VAT", [("Purchases", 100000, 0), ("VAT Input", 13000, 0), ("Creditors (Himal)", 0, 113000)]),
    ("credit sale with VAT", [("Debtors", 226000, 0), ("Sales", 0, 200000), ("VAT Output", 0, 26000)]),
    ("rent with 10% TDS", [("Rent", 50000, 0), ("TDS Payable", 0, 5000), ("Cash", 0, 45000)]),
    ("received from debtor", [("Cash", 150000, 0), ("Debtors", 0, 150000)]),
    ("paid creditor", [("Creditors (Himal)", 113000, 0), ("Cash", 0, 113000)]),
]
ledger = {}
for narr, lines in entries:
    assert sum(d for _, d, _ in lines) == sum(c for _, _, c in lines), narr
    for acct, dr, cr in lines:
        side = ledger.setdefault(acct, [0, 0])
        side[0] += dr; side[1] += cr
tot_dr = tot_cr = 0
for acct, (dr, cr) in sorted(ledger.items()):
    net = dr - cr
    kind = "Dr" if net > 0 else "Cr" if net < 0 else "nil"
    print(f"{acct}: {kind} {abs(net)}")
    tot_dr += max(net, 0); tot_cr += max(-net, 0)
print(f"total debits {tot_dr}, total credits {tot_cr}")
```
```output
Capital: Cr 500000
Cash: Dr 492000
Creditors (Himal): nil 0
Debtors: Dr 76000
Purchases: Dr 100000
Rent: Dr 50000
Sales: Cr 200000
TDS Payable: Cr 5000
VAT Input: Dr 13000
VAT Output: Cr 26000
total debits 731000, total credits 731000
```
The Cash account closes with a debit balance of Rs 492,000 (500,000 − 45,000 + 150,000 − 113,000) and Debtors with Rs 76,000. The creditor shows *nil* because the invoice was settled. The final line is the **trial balance** idea in miniature: Rs 731,000 on each side. Notice the `assert`: each entry is validated before it is posted, so an unbalanced entry can never reach the ledger.

## 2.7 Opening, closing and compound entries

At the start of a period, an **opening entry** records existing assets and liabilities, with capital as the balancing figure. At period end, **closing entries** transfer nominal-account balances to the Trading and Profit and Loss accounts (Unit 6). A **compound entry** such as the rent entry above debits or credits more than one account but keeps total debits equal to total credits.

::: note
Journal proper is not the only first record. Subsidiary books (Unit 3) take the high-volume transactions; the journal proper handles opening entries, adjustments, rectifications and non-routine items.
:::

## 2.8 Summary and exercises

Journalising converts documents into balanced debit and credit lines; VAT is a pass-through liability and input asset, TDS is a liability to the tax office, and the ledger accumulates each account's movements until it can be balanced.

1. Journalise: purchased furniture for Rs 40,000 plus 13% VAT on credit; sold goods for Rs 60,000 plus 13% VAT in cash.
2. Rent of Rs 80,000 is paid with 10% TDS. Give the entries for payment and later deposit.
3. Differentiate VAT Input and VAT Output; compute the VAT payable when output is 1,95,000 and input is 2,10,000.
4. Rule off and balance a Cash account with debits of 3,20,000 and credits of 2,75,000.
5. State the golden rule applied to each side of the entry "Paid salary Rs 25,000 by cheque".
6. Modify the Python program to reject an entry that debits and credits the same account.

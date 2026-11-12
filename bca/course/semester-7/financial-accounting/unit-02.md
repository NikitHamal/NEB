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

## 2.8 Seeing the ideas: debit and credit, the VAT invoice and the cash T-account

```photogrid label="2.1" cols="2" ratio="1.0" caption="(a) A Nepalese five-rupee note from the Nepal Rastra Bank: the money measurement concept records only what can be stated in rupees like this. (b) The anatomy of a VAT tax invoice, the source document from which the journal entry is written; every labelled field becomes a line in the books."
@ photo id="bca403/note" cap="Old Nepal Rastra Bank note"
fit 1.0
focus 0.4 0.5
@ svg cap="Tax invoice anatomy"
f = Fig(300, 300)
f.box(10, 8, 280, 284, "", fill="#ffffff", stroke=NAVY)
f.text(150, 28, "TAX INVOICE", size=14, color=NAVY, bold=True)
R = [("Seller name + PAN", 48, MINT, TEAL), ("Invoice no. + date (BS)", 80, BLUE, NAVY), ("Buyer name + PAN", 112, BLUE, NAVY), ("Goods, qty, rate", 144, SAND, AMBER), ("Taxable amount 1,00,000", 176, SAND, AMBER), ("VAT 13% = 13,000", 208, ROSE, RED), ("Total 1,13,000 in words", 240, MINT, TEAL)]
for t, y, fl, st in R:
    f.box(22, y, 256, 26, t, fill=fl, stroke=st, size=12.5)
f.text(150, 282, "debit Purchases 1,00,000 and VAT Input 13,000", size=11, color=SLATE, italic=True)
```

```svgfig label="2.1" caption="Which side increases which account. Assets and expenses increase on the debit (left) side; liabilities, capital and income increase on the credit (right) side. The accounting equation is the reason: the left side of the equation is the debit side."
f = Fig(580, 214)
T = [(10, "Assets", "Dr increases", "Cr decreases", MINT, TEAL), (126, "Expenses", "Dr increases", "Cr decreases", SAND, AMBER), (242, "Liabilities", "Cr increases", "Dr decreases", ROSE, RED), (358, "Capital", "Cr increases", "Dr decreases", BLUE, NAVY), (474, "Income", "Cr increases", "Dr decreases", MINT, TEAL)]
for x, n, a, b, fl, st in T:
    f.box(x, 12, 96, 28, n, fill=fl, stroke=st, bold=True, size=12)
    f.line(x + 48, 46, x + 48, 120, color=st, sw=2)
    f.line(x, 46, x + 96, 46, color=st, sw=2)
    f.text(x + 24, 60, "Dr", size=11, color=NAVY, bold=True)
    f.text(x + 72, 60, "Cr", size=11, color=NAVY, bold=True)
    inc_dr = a.startswith("Dr")
    f.box(x + (2 if inc_dr else 50), 70, 44, 22, "+", fill=MINT, stroke=TEAL, bold=True, size=14)
    f.box(x + (50 if inc_dr else 2), 70, 44, 22, "-", fill=ROSE, stroke=RED, bold=True, size=14)
    f.text(x + 48, 140, a, size=10.5, color=TEAL, bold=True)
    f.text(x + 48, 156, b, size=10.5, color=RED)
f.box(10, 176, 336, 28, "Left of equation = DEBIT side:  Assets", fill="#ffffff", stroke=SLATE, size=11)
f.box(358, 176, 212, 28, "Right = CREDIT side: L + Capital", fill="#ffffff", stroke=SLATE, size=11)
```

```svgfig label="2.2" caption="The Cash T-account of the Python engine in 2.6. Debits (receipts) of 6,50,000 minus credits (payments) of 1,58,000 leave a debit balance of Rs 4,92,000, which is carried down."
f = Fig(580, 200)
f.text(290, 16, "Cash account", size=13, color=NAVY, bold=True)
f.line(60, 26, 520, 26, color=SLATE, sw=2); f.line(290, 26, 290, 170, color=SLATE, sw=2)
f.text(175, 42, "Dr (receipts)", size=11, color=TEAL, bold=True); f.text(405, 42, "Cr (payments)", size=11, color=RED, bold=True)
for y, a, b in [(66, "Capital introduced", "5,00,000"), (92, "Received from debtor", "1,50,000")]:
    f.text(70, y, a, size=11, color=SLATE, anchor="start"); f.text(280, y, b, size=11, color=SLATE, anchor="end")
for y, a, b in [(66, "Rent (net of TDS 5,000)", "45,000"), (92, "Paid creditor (Himal)", "1,13,000"), (118, "Balance c/d", "4,92,000")]:
    f.text(300, y, a, size=11, color=SLATE, anchor="start"); f.text(510, y, b, size=11, color=RED if y == 118 else SLATE, anchor="end", bold=(y == 118))
f.line(60, 134, 520, 134, color=SLATE); f.text(280, 154, "6,50,000", size=12, color=NAVY, bold=True, anchor="end"); f.text(510, 154, "6,50,000", size=12, color=NAVY, bold=True, anchor="end")
f.text(290, 188, "Dr 6,50,000 = Cr 45,000 + 1,13,000 + 4,92,000", size=10.5, color=SLATE, italic=True)
```

### 2.8.1 Eight controls for correct journal and ledger work

1. **Start from a source document.** Every entry must be backed by an invoice, cheque, receipt or voucher. A payment with no bill cannot be defended to an auditor or to the tax office. Filing the document number in the narration makes later checking quick.
2. **Write the entry in date order.** The journal is the book of original entry, so the order of events is kept. Back-dating or skipping lines makes errors hard to find. A Nepali business should record both the BS and AD dates when its software allows.
3. **Check that debits equal credits.** Before saving an entry, add each side. The Python engine rejects an unbalanced entry by an assertion, and a good accounting package does the same. This single check removes most arithmetic mistakes.
4. **Use the right account class.** A purchase of a computer is an asset, not an expense, while its monthly internet bill is an expense. Wrong classification changes profit and tax. Keep a chart of accounts with codes and use it every time.
5. **Record VAT separately.** Show VAT Input and VAT Output in their own accounts, as in the 13% example. At the month end the difference is the VAT payable or refundable. Mixing VAT into the purchase price hides what is claimable.
6. **Deduct and record TDS.** When rent is paid, the payer deducts tax at source and credits TDS Payable, then deposits it with the revenue office. Forgetting this creates a penalty. The entry in this unit shows rent 50,000, TDS 5,000 and cash 45,000.
7. **Post promptly and tick the posting.** Posting to the ledger should follow the journal at once, with the folio number noted. A trial balance taken after complete posting will show any slip. Late posting is how entries get lost.
8. **Review balances regularly.** Compare the cash balance with the physical cash and the bank balance with the statement. A debtor balance that does not move for months needs follow-up. Regular review turns the ledger from a record into a control.

```photogrid label="2.2" cols="2" ratio="1.0" caption="A month of VAT in two accounts. (a) A cash register: every taxable sale prints the 13 per cent VAT collected for the Inland Revenue Department. (b) A shop makes taxable sales of Rs 8,00,000 in a month and buys goods for Rs 5,00,000, both before VAT. VAT Output (a liability) is 13% of 8,00,000 = Rs 1,04,000 and VAT Input (an asset) is 13% of 5,00,000 = Rs 65,000. The two accounts are set against each other, so the net VAT payable is 1,04,000 - 65,000 = Rs 39,000, which is exactly 13% of the value added (8,00,000 - 5,00,000 = 3,00,000). A single item priced Rs 1,000 is sold for Rs 1,130. The shop is only the collector of VAT: the burden lies on the final consumer, and the shop keeps nothing but must file the return and pay the net amount on time."
@ photo id="bcafa/register" cap="A cash register that prints the VAT"
fit 1.0
focus 0.5 0.5
@ svg cap="VAT Input, VAT Output and the net payable"
sales, purch, rate = 800000, 500000, 0.13
out = round(sales * rate); inn = round(purch * rate); net = out - inn
assert (out, inn, net) == (104000, 65000, 39000) and net == round((sales - purch) * rate) and round(1000 * 1.13) == 1130
f = Fig(300, 240)
f.text(150, 14, "monthly VAT (rupees)", size=10.5, color=NAVY, bold=True)
mx = 104000
for i, (lab, v, col) in enumerate([("VAT Output (Cr)", out, "#b91c1c"), ("VAT Input (Dr)", inn, "#1d6fb8"), ("Net payable", net, "#0f766e")]):
    y = 28 + i * 40
    f.text(10, y + 6, lab, size=10.5, color=NAVY, anchor="start", bold=True)
    w = 170 * v / mx
    f.box(10, y + 14, w, 16, "", fill=col, stroke=col, r=0)
    f.text(10 + w + 5, y + 22, f"{v:,}", size=10.5, color=col, anchor="start", bold=True, vmid=True)
f.line(10, 154, 290, 154, color=SLATE, sw=1)
f.text(150, 172, "13% of 8,00,000 = 1,04,000", size=10.5, color=SLATE)
f.text(150, 190, "13% of 5,00,000 =   65,000", size=10.5, color=SLATE)
f.text(150, 210, "net = 13% of value added 3,00,000", size=10.5, color=TEAL, bold=True)
f.text(150, 228, "Rs 1,000 item sells at Rs 1,130", size=10.5, color=NAVY)
```

## 2.9 Summary and exercises

Journalising converts documents into balanced debit and credit lines; VAT is a pass-through liability and input asset, TDS is a liability to the tax office, and the ledger accumulates each account's movements until it can be balanced.

1. Journalise: purchased furniture for Rs 40,000 plus 13% VAT on credit; sold goods for Rs 60,000 plus 13% VAT in cash.
2. Rent of Rs 80,000 is paid with 10% TDS. Give the entries for payment and later deposit.
3. Differentiate VAT Input and VAT Output; compute the VAT payable when output is 1,95,000 and input is 2,10,000.
4. Rule off and balance a Cash account with debits of 3,20,000 and credits of 2,75,000.
5. State the golden rule applied to each side of the entry "Paid salary Rs 25,000 by cheque".
6. Modify the Python program to reject an entry that debits and credits the same account.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). State the rules of debit and credit. Journalise: (a) capital introduced Rs 5,00,000 in cash; (b) goods bought on credit from Himal for Rs 1,00,000 plus 13% VAT.**

*Rules.* Traditional: *personal* account, debit the receiver and credit the giver; *real* account, debit what comes in and credit what goes out; *nominal* account, debit expenses and losses and credit incomes and gains. Modern: debit increases assets and expenses, credit increases liabilities, capital and income (Figure 2.1).

| Entry | Account | Dr (Rs) | Cr (Rs) |
|---|---|---|---|
| (a) | Cash A/c (asset comes in) | 5,00,000 | |
| | Capital A/c (owner is the giver) | | 5,00,000 |
| (b) | Purchases A/c (expense) | 1,00,000 | |
| | VAT Input A/c (asset: claimable) | 13,000 | |
| | Creditors, Himal (liability) | | 1,13,000 |

In both entries total debits equal total credits (5,00,000 and 1,13,000). *Narration* such as "being goods purchased on credit, invoice no. 41" is added under each entry. *Conclusion:* a correct entry always has equal debits and credits.

**Q2 (5 marks). Explain the accounting of VAT with an example. What is the VAT payable?**

*Principle.* VAT is a tax on value added that is collected at each stage and passed on. A registered business charges **output VAT** on sales and may deduct **input VAT** paid on purchases, so it pays only the difference to the Inland Revenue Department. The standard rate used here is 13%.

*Example (the book's data).* Purchases Rs 1,00,000 + VAT 13,000; sales Rs 2,00,000 + VAT 26,000.

| Item | Amount (Rs) |
|---|---|
| Output VAT on sales (13% × 2,00,000) | 26,000 |
| Less input VAT on purchases (13% × 1,00,000) | 13,000 |
| **VAT payable** | **13,000** |

*Entries.* Purchase: Dr Purchases 1,00,000, Dr VAT Input 13,000, Cr Creditors 1,13,000. Sale: Dr Debtors 2,26,000, Cr Sales 2,00,000, Cr VAT Output 26,000. At the month end: Dr VAT Output 26,000, Cr VAT Input 13,000, Cr VAT Payable 13,000. VAT is a liability to the government, not the business's income. *Conclusion:* separate VAT accounts keep the sales and purchases figures clean and the payment correct.

**Q3 (10 marks). Explain journal, ledger posting and the trial balance. Using the six transactions of the book's engine, show the Cash account and the trial balance.**

*Introduction.* The **journal** is the book of original entry in which each transaction is recorded in date order with debit and credit. The **ledger** groups the same entries by account. The **trial balance** lists all ledger balances to test that total debits equal total credits (Figure 2.2).

*Transactions.* (1) capital Rs 5,00,000 in cash; (2) credit purchase 1,00,000 + VAT 13,000; (3) credit sale 2,00,000 + VAT 26,000; (4) rent 50,000 with 10% TDS; (5) received 1,50,000 from a debtor; (6) paid creditor 1,13,000.

*Posting.* Each debit line is posted to the debit side of its account and each credit to the credit side, with a folio reference. *Cash account:* debit 5,00,000 + 1,50,000 = 6,50,000; credit 45,000 + 1,13,000 = 1,58,000; balance **Rs 4,92,000 Dr**.

*Trial balance.*

| Account | Dr (Rs) | Cr (Rs) |
|---|---|---|
| Cash | 4,92,000 | |
| Debtors | 76,000 | |
| Purchases | 1,00,000 | |
| Rent | 50,000 | |
| VAT Input | 13,000 | |
| Capital | | 5,00,000 |
| Sales | | 2,00,000 |
| TDS Payable | | 5,000 |
| VAT Output | | 26,000 |
| **Total** | **7,31,000** | **7,31,000** |

The Creditors (Himal) account shows nil, so it is absent.

*Limits of the trial balance.* Agreement proves arithmetic accuracy only. It does not detect omission of a whole transaction, an error of principle (wrong class), compensating errors or an entry posted to a wrong account of the same side.

*Comparison.*

| Point | Journal | Ledger | Trial balance |
|---|---|---|---|
| Nature | book of original entry | book of final entry | statement, not a book |
| Order | by date | by account | by account list |
| Purpose | record | classify | test accuracy |

*Conclusion.* The journal captures, the ledger classifies and the trial balance verifies. When the totals agree (Rs 7,31,000), the books are ready for adjustments and final accounts.

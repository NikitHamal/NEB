---
subject: Accountancy
grade: 10
unit: 6
title: Accounting Errors (लेखात्मक गल्तीहरू)
hours: 5
area: Business Accounting
---

Nobody keeps a perfect set of books. A figure is copied wrongly, a posting is made to the wrong side, a capital expense is treated as a revenue expense, or a whole transaction is left out. Some of these mistakes make the trial balance disagree and shout for attention; others are silent and can survive for years. This unit classifies errors, shows which of them the **trial balance** can catch, explains how each one is corrected — before the trial balance and after it — and introduces the **suspense account**, the temporary account that holds the difference until the mistake is found.

::: key What the examiner tests here
Group B or Group C always gives you a list of errors and asks for **rectifying entries**, and asks in the margin whether the trial balance will agree or not. The trick is to decide, for each error, whether it is **one-sided** (affects only one account — the trial balance will not agree, so a suspense account is needed) or **two-sided** (affects two accounts in a way that cancels out — the trial balance agrees, so no suspense is needed). Get that decision right and the entry writes itself.
:::

## 6.1 Accounting errors: meaning and causes

An **accounting error (लेखात्मक गल्ती)** is a mistake made in recording, posting, casting, carrying forward or summarising a transaction, or in applying an accounting principle, which makes the books wrong.

**Causes.** Errors are made because the work is done by human beings under time pressure. The commonest causes are:

- **Carelessness** — a wrong figure copied from a voucher, a figure written in the wrong column.
- **Ignorance of principle** — treating the purchase of a machine as a purchase of goods, or a repair of a building as an addition to the building.
- **Wrong classification** — posting a payment to wages instead of to salary.
- **Wrong side** — a debit posted as a credit.
- **Omission** — a transaction not entered at all, or entered in the journal but never posted.
- **Compensating mistakes** — two errors of the same amount on opposite sides which cancel each other.
- **Faulty arithmetic** — adding a column wrongly (a *casting* error) or carrying a wrong balance forward.
- **Wrong account of the same class** — debiting Ram instead of Shyam (both are debtors).

## 6.2 Types of errors

```figure caption="The classification of accounting errors. The right-hand branch is the dangerous one: these errors leave the trial balance perfectly in agreement while the books are still wrong."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.1))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.add_patch(FancyBboxPatch((3.6,8.5),2.8,1.1,boxstyle="round,pad=0.05",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(5.0,9.05,"ERRORS",ha='center',va='center',fontsize=8.6,color=INK,weight='bold')
ax.add_patch(FancyArrowPatch((4.4,8.45),(2.6,7.15),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((5.6,8.45),(7.4,7.15),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.1))
ax.add_patch(FancyBboxPatch((0.2,5.6),4.4,1.5,boxstyle="round,pad=0.05",fc="#f6f8fc",ec=MUTED,lw=1.1))
ax.text(2.4,6.35,"Affect the trial balance\n(one-sided errors)",ha='center',va='center',fontsize=7,color=INK)
ax.add_patch(FancyBboxPatch((5.4,5.6),4.4,1.5,boxstyle="round,pad=0.05",fc="#fdf3f3",ec=SERIES[1],lw=1.1))
ax.text(7.6,6.35,"Do not affect the trial balance\n(two-sided errors)",ha='center',va='center',fontsize=7,color=INK)
ax.text(2.4,3.3,"• Error of partial omission\n• Posting to the wrong side\n• Wrong amount posted\n• Error of casting or balancing\n• Posting only one aspect",
        ha='center',va='center',fontsize=6.5,color=INK)
ax.text(7.6,3.3,"• Error of principle\n• Complete omission\n• Compensating errors\n• Wrong account of the same class\n• Recording the same transaction twice",
        ha='center',va='center',fontsize=6.5,color=INK)
```

**Errors of principle.** A mistake in applying an accounting rule, usually by putting a **capital expenditure** among the revenue expenses or the other way round. Example: wages paid for installing a new machine are debited to the wages account instead of being added to the cost of the machine. Such an error **does not** affect the trial balance (both sides receive the same amount, only under the wrong heads), but it makes both the profit and the asset figure wrong.

**Errors of omission.** The transaction is left out altogether. If it is *completely omitted* — nothing written anywhere — the trial balance still agrees, because neither side has been entered. If it is *partially omitted* — entered in the journal but posted to only one account — the trial balance will not agree.

**Errors of commission.** The transaction is recorded, but wrongly: the wrong amount is entered, or the right amount is posted to the wrong account, or posted to the wrong side, or the total of a book is cast wrongly, or a balance is carried forward wrongly.

**Compensating errors.** Two or more errors, each of the same amount, on opposite sides, which cancel each other. Example: wages overcast by Rs. 1,000 (debit side too high by Rs. 1,000) and sales undercast by Rs. 1,000 (credit side too low by Rs. 1,000). The trial balance agrees and neither error is visible.

```photo id="acc10/adding-machine" caption="A mechanical adding machine of the kind used to cast ledger columns before computers. A single wrong casting left a difference that the trial balance carried for months." width="66"
```

## 6.3 Detection of errors through the trial balance

A **trial balance** is a statement of the debit and credit balances of all the ledger accounts, prepared to test the arithmetical accuracy of the books. If the total of the debit column does not equal the total of the credit column, an error has certainly been made — a **one-sided** error.

| Error | Effect on the trial balance |
|---|---|
| An amount posted to the wrong side of an account | Difference of twice the amount |
| An amount posted to only one account (partial omission) | Difference of the full amount |
| A wrong amount posted, where the correct amount was journalised | Difference of the difference of the two amounts |
| A book overcast or undercast, or a balance carried forward wrongly | Difference of the amount of the error |
| A transaction entered twice in one account only | Difference of the amount |

**What the trial balance cannot detect.** The trial balance tests only that the debits equal the credits. It cannot see an error of **principle**, a **complete omission**, a **compensating error**, a **wrong account of the same class**, or a transaction **entered twice in both accounts**. These leave the trial balance agreeing while the books are still wrong. That is why the trial balance is a proof of *arithmetical* accuracy only, and never a proof that the accounts are correct.

When the trial balance disagrees, the difference is put in a **suspense account** so that the work can continue, and it is hunted down afterwards by checking the books, the journal, the postings, the casts and the balances.

## 6.4 Rectification of errors

How an error is corrected depends on **when** it is discovered.

**Before the trial balance is prepared.** The books are still open, so the correction is made by an ordinary journal entry that puts the amounts where they should have been. No suspense account is needed.

- *Two accounts affected* — write a journal entry debiting the account that should have been debited and crediting the account that should have been credited.
- *Error of principle* — reverse the wrong entry and pass the correct one.
- *One-sided error* — correct the wrong account with a journal entry; the other side of the entry goes to the **suspense account** if the trial balance has already been drawn.

**After the trial balance is prepared.** The same errors are corrected by journal entries, but with one important difference: for a **one-sided error** the corresponding side of the correcting entry is taken to the **suspense account**, because the trial balance has already been balanced by putting the difference there.

**The ordinary corrections.**

| Error | Correction |
|---|---|
| An expense debited to the wrong expense account (e.g. salary to rent) | Debit the correct expense, credit the wrong one |
| A purchase of machinery debited to the purchases account | Debit machinery, credit purchases; and if depreciation was charged, reverse it too |
| A sale to Ram debited to Shyam | Debit Ram, credit Shyam |
| A sale of Rs. 5,000 entered in the sales book as Rs. 500 | Debit the customer by Rs. 4,500, credit sales by Rs. 4,500 |
| A purchase of Rs. 2,000 posted to the credit of the purchase account instead of the debit | Debit purchases twice Rs. 2,000 and credit suspense Rs. 4,000 |
| A cash sale of Rs. 3,000 completely omitted | Debit cash, credit sales by Rs. 3,000 |
| Wages for installing machinery debited to wages | Debit machinery, credit wages; and reduce the wages already closed if the accounts have been closed |

::: example Errors before the trial balance
**Problem.** The following errors were found before the trial balance was prepared. Pass the rectifying entries.
i. Salary of Rs. 20,000 paid was wrongly debited to the rent account.
ii. A sale of goods of Rs. 15,000 to Mohan was debited to Sohan's account.
iii. Purchase of furniture of Rs. 40,000 was debited to the purchases account.
iv. A cash sale of Rs. 5,000 was completely omitted from the books.

**Solution.**
Step 1 — (i) Two accounts, both expense accounts: salary should have been debited and rent should not have been. *Salary A/c Dr. 20,000; To Rent A/c 20,000.*
Step 2 — (ii) Two debtors, same class: Mohan's account should have been debited. *Mohan A/c Dr. 15,000; To Sohan A/c 15,000.*
Step 3 — (iii) This is an error of **principle** — a capital expenditure treated as revenue. *Furniture A/c Dr. 40,000; To Purchases A/c 40,000.*
Step 4 — (iv) A complete omission: nothing at all was written. *Cash A/c Dr. 5,000; To Sales A/c 5,000.*
Step 5 — State the effect on the trial balance: (i) and (ii) are two-sided errors — the trial balance agreed and still agrees. (iii) is a two-sided error of principle — the trial balance agreed; but profit is understated by Rs. 40,000 and furniture is understated. (iv) is a complete omission — the trial balance agreed, and it still agrees after rectification.

**Answer.** The four entries above. No suspense account is needed because the trial balance has not yet been prepared.
:::

::: example One-sided errors after the trial balance
**Problem.** After preparing the trial balance, the following errors were discovered. Pass the rectifying entries and show the suspense account.
i. The purchases book was undercast by Rs. 5,000.
ii. Sales of Rs. 8,000 to Kamal were posted to Kamal's account as Rs. 800.
iii. A cash purchase of Rs. 3,000 was posted to the debit of the purchase account as Rs. 300 while the cash account was correctly posted.

**Solution.**
Step 1 — (i) The purchases book was undercast: the debit side of the ledger is short by Rs. 5,000. The trial balance was short on the debit side, so the difference sits in the credit of the suspense account. *Purchases A/c Dr. 5,000; To Suspense A/c 5,000.*
Step 2 — (ii) Kamal's account was debited Rs. 800 instead of Rs. 8,000, so the debit is short by Rs. 7,200. *Kamal A/c Dr. 7,200; To Suspense A/c 7,200.*
Step 3 — (iii) The purchase account was debited with Rs. 300 instead of Rs. 3,000 — short by Rs. 2,700 on the debit side. *Purchases A/c Dr. 2,700; To Suspense A/c 2,700.*
Step 4 — Total the suspense account: three credits of Rs. 5,000, Rs. 7,200 and Rs. 2,700 = Rs. 14,900. This is exactly the difference that the trial balance showed.

*Suspense account*

| Date | Particulars | Rs. | Date | Particulars | Rs. |
|---|---|---|---|---|---|
| | To Balance b/d (if any) | — | | By Purchases A/c (undercast) | 5,000 |
| | | | | By Kamal A/c (short posting) | 7,200 |
| | | | | By Purchases A/c (short posting) | 2,700 |
| | **Total** | **14,900** | | **Total** | **14,900** |

**Answer.** The debit side of the trial balance was short by Rs. 14,900, which was sitting in the credit of the suspense account. The three entries above clear it.
:::

::: example Which errors make the trial balance disagree?
**Problem.** State, with a reason, whether the trial balance will agree in each of the following cases, and name the kind of error.
(a) A credit sale of Rs. 20,000 to Gita was not entered anywhere.
(b) The purchases returns book was overcast by Rs. 2,000.
(c) A purchase from Bimal of Rs. 6,000 was posted to his account as Rs. 6,600.
(d) Wages paid for the erection of a machine of Rs. 15,000 were debited to the wages account.
(e) A payment of Rs. 4,000 to a creditor was posted to the creditor's account twice on the debit side while cash was posted once.
(f) The carriage inward account was undercast by Rs. 3,000 and the carriage outward account was undercast by Rs. 3,000.

**Solution.**
Step 1 — (a) Nothing was written on either side, so both sides of the trial balance keep the same totals. **Agrees** — complete omission.
Step 2 — (b) The returns book total is used for postings on one side only, so one side becomes short by Rs. 2,000. **Does not agree** — one-sided casting error; suspense account needed.
Step 3 — (c) The journal and the debit to purchases are right; only the creditor's account is wrong, by Rs. 600 on the credit side. **Does not agree** — one-sided error; suspense account needed.
Step 4 — (d) The entry is complete and balanced; only the head is wrong. **Agrees** — error of principle; but profit and the asset figure are both wrong.
Step 5 — (e) The creditor's account has been debited Rs. 8,000 while cash was credited Rs. 4,000, so one side is short by Rs. 4,000. **Does not agree** — one-sided error; suspense account needed.
Step 6 — (f) Both errors are Rs. 3,000 on the same side (debit), so they add up: the debit side is short by Rs. 6,000. **Does not agree** — two one-sided errors, not a compensating pair.

**Answer.** Agrees: (a) and (d). Does not agree: (b) Rs. 2,000, (c) Rs. 600, (e) Rs. 4,000, (f) Rs. 6,000.
**What it means.** The test is not the size of the error but **how many sides of the trial balance it disturbs**. If it disturbs one side only, the trial balance will not agree and a suspense account is opened.
:::

## 6.5 Suspense account

A **suspense account (उज्राती खाता)** is a temporary account opened to hold the difference in the trial balance so that the trial balance can be made to agree and the books can be closed and the final accounts prepared while the mistake is still being traced.

**Why it is used.** When a trial balance does not agree, the accountant cannot stop work. By putting the difference in the suspense account he can carry on. The account is a holding place, never a permanent one: it must be cleared to nil as soon as every error is found.

**How it works.**

- If the **debit** column of the trial balance is short, the suspense account is **credited** with the difference.
- If the **credit** column is short, the suspense account is **debited** with the difference.
- Each one-sided error is then corrected with an entry whose other side is the suspense account, so the suspense balance falls.
- When every error has been found and corrected, the suspense account closes at nil. If a balance remains, one or more errors are still hidden.

**Where its balance is shown.** Until it is cleared, a credit balance of the suspense account is shown on the **liabilities** side of the balance sheet and a debit balance on the **assets** side. That is one more reason to clear it quickly.

::: caution The common mistake
Students pass a perfect rectifying entry and then forget to say whether the trial balance **will agree**. For each error, ask: *has the same amount been taken out of one account and put into another on the same side, or has a whole side been left short?*
- Wrong account, same class (Ram for Shyam) — **two-sided**, trial balance agrees.
- Wrong expense instead of another expense — **two-sided**, agrees.
- Capital expense in a revenue account — **two-sided (error of principle)**, agrees.
- Complete omission — **two-sided**, agrees.
- A book undercast, a single posting short, a wrong side — **one-sided**, does not agree, suspense account needed.
:::

::: memory The unit in one list
**Errors that the trial balance catches** = one-sided: casting, balancing, half a posting, wrong side, wrong amount posted once. **Errors it never catches** = two-sided: principle, complete omission, compensating, wrong account of the same class, double entry. **Correction before trial balance** = plain journal entry. **Correction after trial balance** = journal entry with the suspense account on the other side for one-sided errors.
:::

## Chapter summary

- An **accounting error** is a mistake in recording, posting, casting, carrying forward or summarising a transaction, or in applying an accounting principle.
- Its causes are carelessness, ignorance of principle, wrong classification, wrong side, omission, compensating mistakes, faulty arithmetic and the wrong account of the same class.
- **Types**: errors of **principle** (capital expenditure treated as revenue or the reverse); errors of **omission** (complete or partial); errors of **commission** (wrong amount, wrong account, wrong side, wrong casting or balancing); and **compensating** errors.
- The **trial balance** tests only that total debits equal total credits. It detects **one-sided** errors — casting errors, wrong side, wrong amount posted once, partial omission, a balance carried forward wrongly.
- It **cannot** detect errors of principle, complete omission, compensating errors, a wrong account of the same class, or the same transaction entered twice in both accounts. A trial balance proves arithmetical accuracy, not correctness.
- **Rectification before the trial balance** is by an ordinary journal entry putting the amounts where they belong. An error of principle is corrected by reversing the wrong entry and passing the correct one.
- **Rectification after the trial balance** is by a journal entry in which the other side of a **one-sided** error goes to the suspense account; two-sided errors are corrected exactly as before.
- A **suspense account** is a temporary account holding the difference in the trial balance. The short side of the trial balance is the side on which the suspense account is entered. It must be cleared to nil; until then a credit balance appears on the liabilities side and a debit balance on the assets side of the balance sheet.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is an accounting error? <span class="marks">[1]</span>
2. Write any two causes of accounting errors. <span class="marks">[1]</span>
3. What is an error of principle? Give one example. <span class="marks">[1]</span>
4. What is a compensating error? <span class="marks">[1]</span>
5. Which errors are detected by the trial balance? <span class="marks">[1]</span>
6. Which errors are not detected by the trial balance? <span class="marks">[1]</span>
7. What is a suspense account? <span class="marks">[1]</span>
8. If the debit column of the trial balance is short, on which side is the suspense account opened? <span class="marks">[1]</span>
9. A purchase of machinery was debited to the purchases account. What kind of error is this? <span class="marks">[1]</span>
10. Where is a debit balance of the suspense account shown in the balance sheet? <span class="marks">[1]</span>
11. A sale of Rs. 5,000 to Ram was debited to Shyam. Will the trial balance agree? <span class="marks">[1]</span>

::: note Answers to Group A
**1.** An accounting error is a mistake made in recording, posting, casting, carrying forward or summarising a transaction, or in applying an accounting principle.
**2.** Any two of: carelessness, ignorance of accounting principle, wrong classification, posting to the wrong side, omission, compensating mistake, faulty arithmetic.
**3.** An error of principle is a mistake in applying an accounting rule, such as treating a capital expenditure as a revenue expense. Example: wages paid for installing a machine debited to the wages account instead of being added to the machine's cost.
**4.** A compensating error is one of two or more errors, each of the same amount and on opposite sides, which cancel each other so that the trial balance still agrees.
**5.** One-sided errors: casting or balancing errors, posting to the wrong side, a wrong amount posted in one account only, partial omission.
**6.** Two-sided errors: errors of principle, complete omission, compensating errors, wrong account of the same class, a transaction entered twice in both accounts.
**7.** A suspense account is a temporary account opened to hold the difference in the trial balance until the errors causing it are found and corrected.
**8.** On the **credit** side — the suspense account is credited when the debit column is short.
**9.** An error of principle. (It is also an error of commission in classification, but the accepted answer is error of principle.)
**10.** On the assets side.
**11.** Yes — both are debtors, so the total of the debit column is unchanged.
:::

**Group B — Short answer (5 marks each)**

1. What are accounting errors? Explain any five causes of accounting errors. <span class="marks">[5]</span>
2. Explain the types of accounting errors with suitable examples. <span class="marks">[5]</span>
3. Which errors are detected by the trial balance and which are not? Explain with examples. <span class="marks">[5]</span>
4. Rectify the following errors before the preparation of the trial balance. (a) Rent paid Rs. 6,000 was debited to the wages account. (b) A sale of Rs. 9,000 to Hari was posted to Gopal's account. (c) Purchase of a computer of Rs. 50,000 was debited to the purchases account. (d) A credit purchase of Rs. 4,000 from Shyam was completely omitted. <span class="marks">[5]</span>
5. Rectify the following errors found after the preparation of the trial balance and show the suspense account. (a) The sales book was undercast by Rs. 3,000. (b) A purchase of Rs. 6,000 from Ram was posted to his account as Rs. 600. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** An accounting error is a mistake in recording, posting, casting, carrying forward or summarising a transaction or in applying a principle. Causes: carelessness (wrong figure or column); ignorance of principle (capital expenditure in a revenue account); wrong classification (salary posted to rent); wrong side (a debit posted as a credit); omission (a transaction not entered or not posted); compensating errors; faulty arithmetic in a book or a balance.
**2.** *Error of principle* — treating capital expenditure as revenue (wages for installing machinery debited to wages). *Error of omission* — complete omission (a sale not entered anywhere) or partial omission (entered in the journal but not posted). *Error of commission* — wrong amount, wrong account, wrong side, wrong casting, wrong balance carried forward. *Compensating error* — wages overcast by Rs. 1,000 and sales undercast by Rs. 1,000.
**3.** *Detected:* one-sided errors — a book overcast or undercast, an amount posted to the wrong side, an amount posted to only one account, a wrong amount posted in one account while the journal is correct. These change one side of the trial balance only. *Not detected:* two-sided errors — errors of principle, complete omission, compensating errors, a wrong account of the same class and a transaction entered twice in both accounts. These change both sides equally or not at all, so the trial balance still agrees.
**4.** (a) *Rent A/c Dr. 6,000; To Wages A/c 6,000* — two-sided, trial balance agreed. (b) *Hari A/c Dr. 9,000; To Gopal A/c 9,000* — two-sided, agreed. (c) *Computer A/c Dr. 50,000; To Purchases A/c 50,000* — error of principle, two-sided, agreed. (d) *Purchases A/c Dr. 4,000; To Shyam A/c 4,000* — complete omission, two-sided, agreed.
**5.** (a) The debit side is short by Rs. 3,000, so the suspense account was credited: *Sales A/c Dr. 3,000; To Suspense A/c 3,000*. (b) Ram's account was credited Rs. 600 instead of Rs. 6,000 — the credit side is short by Rs. 5,400: *Suspense A/c Dr. 5,400; To Ram A/c 5,400*. (Because a credit posting of a purchase was short, the credit side of the trial balance was short, so the suspense account was **debited** with the difference.) Total of the suspense account: Rs. 5,400 (Dr.) against Rs. 3,000 (Cr.), leaving Rs. 2,400 on the debit side until the remaining errors are found.
:::

**Group C — Long answer (8 marks each)**

1. What is an accounting error? Explain the types of errors and state which of them are detected by the trial balance and which are not. <span class="marks">[8]</span>
2. The following errors were located after the preparation of the trial balance. (a) Salary paid Rs. 20,000 was wrongly debited to the house rent account. (b) The sales book was overcast by Rs. 5,000. (c) A purchase of furniture of Rs. 30,000 was debited to the purchases account. (d) A sale of Rs. 7,000 to Bina was posted to Bina's account as Rs. 700. Pass the rectifying entries and prepare the suspense account. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Definition (1).* As in Group B answer 1.
*Types (4).* Errors of principle (capital expenditure treated as revenue, or the reverse) — two-sided. Errors of omission — complete omission (nothing recorded) and partial omission (recorded but posted once) — the first two-sided, the second one-sided. Errors of commission — wrong amount, wrong account, wrong side, wrong casting, wrong balance carried forward. Compensating errors — two errors of the same amount on opposite sides. Explain each with an example.
*Detected/not detected (3).* The trial balance detects only one-sided errors: casting and balancing errors, posting to the wrong side, a wrong amount posted in one account, partial omission. It cannot detect errors of principle, complete omission, compensating errors, the wrong account of the same class or a double recording. Hence a trial balance proves arithmetical accuracy only.
**2.**
(a) *Salary A/c Dr. 20,000; To House Rent A/c 20,000.* Two-sided — the trial balance agreed, no suspense needed.
(b) The sales book was overcast by Rs. 5,000: the credit side is too high, so the trial balance was short on the debit side and the suspense account was **credited**. *Sales A/c Dr. 5,000; To Suspense A/c 5,000.*
(c) *Furniture A/c Dr. 30,000; To Purchases A/c 30,000.* Error of principle — two-sided, no suspense.
(d) Bina's account was debited Rs. 700 instead of Rs. 7,000 — the debit side is short by Rs. 6,300. *Bina A/c Dr. 6,300; To Suspense A/c 6,300.*

*Suspense account*

| Particulars | Rs. | Particulars | Rs. |
|---|---|---|---|
| To Balance b/d (debit difference, if any) | — | By Sales A/c (overcast) | 5,000 |
| | | By Bina A/c (short posting) | 6,300 |
| **Total** | **11,300** | **Total** | **11,300** |

The debit column of the trial balance was short by Rs. 11,300, which was carried in the credit of the suspense account and is now cleared.
:::

---
subject: Accountancy
grade: 10
unit: 7
title: Final Account (अन्तिम खाता)
hours: 10
area: Final Accounts
---

At the end of the year every trader has to answer two questions with figures: **how much did I earn?** and **what do I own and owe today?** The **final accounts** answer them. They are the trading account, the profit and loss account and the balance sheet, and they are prepared from the trial balance after the **adjustments** for everything that happened but has not yet been written down — stock still unsold, a salary still unpaid, rent paid in advance, depreciation on the furniture. This is the largest and most examined unit of the paper, and everything in it rests on one rule: **every adjustment has two effects, one in the trading or profit and loss account and one in the balance sheet**.

::: key What the examiner tests here
Group C almost always carries a final-accounts numerical: a trial balance with three or four additional informations, and you must prepare the trading account, the profit and loss account and the balance sheet. Group B asks for the meaning and objectives of final accounts, the components of financial statements, or the treatment of a particular adjustment. Marks are lost most often for a **forgotten second effect** of an adjustment; check every adjustment twice before you turn the page.
:::

## 7.1 Final accounts: meaning and objectives

**Final accounts (अन्तिम खाता)** are the statements prepared at the end of an accounting period from the trial balance, after all adjustments, in order to show the **profit or loss** of the period and the **financial position** of the business on the last day of the period.

They are also called the **financial statements**. The trading account and the profit and loss account together are the *income statement*; the balance sheet is the *statement of financial position*. (A modern set of statements adds the statement of cash flows and the notes.)

**Objectives.**

1. To find the **gross profit or gross loss** earned on buying and selling (or manufacturing and selling) during the period.
2. To find the **net profit or net loss** after all indirect expenses and other incomes have been brought in.
3. To show the **financial position** — the assets, the liabilities and the capital — on the closing date.
4. To make the year's figures **comparable** with previous years and with similar businesses.
5. To give the **basis for the tax return**, for the auditor and for a loan application.
6. To supply the owner with the information needed for decisions — what to buy, what to drop, what to expand.

## 7.2 Components of final accounts

```figure caption="The three statements and what each one shows. The gross profit is carried down into the profit and loss account, and the net profit is carried into the balance sheet."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.2))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.add_patch(FancyBboxPatch((0.3,7.4),4.4,2.1,boxstyle="round,pad=0.07",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(2.5,8.75,"TRADING ACCOUNT",ha='center',fontsize=8,color=INK,weight='bold')
ax.text(2.5,7.95,"Sales less cost of goods sold\n= GROSS PROFIT",ha='center',va='center',fontsize=6.8,color=INK)
ax.add_patch(FancyBboxPatch((0.3,4.2),4.4,2.2,boxstyle="round,pad=0.07",fc="#eef3ff",ec=ACCENT,lw=1.2))
ax.text(2.5,5.65,"PROFIT AND LOSS ACCOUNT",ha='center',fontsize=7.6,color=INK,weight='bold')
ax.text(2.5,4.8,"Gross profit plus other income\nless indirect expenses\n= NET PROFIT",ha='center',va='center',fontsize=6.8,color=INK)
ax.add_patch(FancyBboxPatch((5.3,4.2),4.4,5.3,boxstyle="round,pad=0.07",fc="#fdf3f3",ec=SERIES[1],lw=1.2))
ax.text(7.5,8.75,"BALANCE SHEET",ha='center',fontsize=8,color=INK,weight='bold')
ax.text(7.5,6.6,"Liabilities\nCapital (with net profit added)\nLong-term loans\nCurrent liabilities\nand provisions",
        ha='center',va='center',fontsize=6.6,color=INK)
ax.text(7.5,4.75,"Assets\nFixed assets (less depreciation)\nInvestments\nCurrent assets\nand prepayments",ha='center',va='center',fontsize=6.6,color=INK)
ax.add_patch(FancyArrowPatch((2.5,7.35),(2.5,6.5),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.2))
ax.add_patch(FancyArrowPatch((4.8,4.8),(5.25,5.6),arrowstyle="-|>",mutation_scale=10,color=SERIES[1],lw=1.2))
ax.text(2.5,3.1,"Prepared FOR the year:\nflows of income and expense",ha='center',fontsize=6.4,color=MUTED)
ax.text(7.5,3.1,"Prepared ON the closing date:\nbalances of assets and liabilities",ha='center',fontsize=6.4,color=MUTED)
```

**Trading account.** It deals with the goods bought and sold. On the debit side go the **opening stock, purchases, purchases returns adjusted, and all direct expenses** — carriage inward, freight, wages, wages and salaries of factory staff, fuel, power, factory rent, customs duty and clearing charges. On the credit side go **sales less sales returns, and the closing stock**. The balance is the **gross profit** (or gross loss).

$$Gross\ profit = Sales - Cost\ of\ goods\ sold$$
$$Cost\ of\ goods\ sold = Opening\ stock + Purchases + Direct\ expenses - Closing\ stock$$

**Profit and loss account.** It starts with the gross profit and deals with everything else. On the debit side go all **indirect expenses** — office salaries, rent, rates and taxes, printing and stationery, postage, telephone, insurance, depreciation, bank charges, interest on loan, discount allowed, carriage outward, advertisement, bad debts. On the credit side go **other incomes** — commission received, rent received, discount received, interest received, profit on sale of an asset. The balance is the **net profit** (or net loss).

$$Net\ profit = Gross\ profit + Other\ income - Indirect\ expenses$$

**Balance sheet.** A statement of the **assets, liabilities and capital** as they stand on the closing date. It is not an account — it has no debit or credit side in the accounting sense — and it is a *statement*, not a summary of movements.

$$Assets = Liabilities + Capital$$

**Treatment of a few balances.** Drawings are deducted from capital; the net profit is *added* to capital (a net loss is deducted); the balance of the capital account is the closing capital.

```photo id="acc10/cash-book" caption="A ruled cash book. The final accounts are built from books exactly like this one — which is why every figure in them must first be traced back to its page." width="62"
```

## 7.3 Adjustments in financial statements

An **adjustment** is the entry made at the end of the year to bring into the accounts something that has happened but has not yet been recorded, or has been recorded in a way that must now be corrected. Adjustments are needed because of the **accrual basis**: income is recognised when it is earned, not when it is received, and expense when it is incurred, not when it is paid.

**The golden rule of adjustments.** Every adjustment has **two effects**: one in the **trading or profit and loss account** and one in the **balance sheet** (or in both statements). If you have written only one of them, the balance sheet will not tally.

| Adjustment | Effect in trading / profit and loss account | Effect in balance sheet |
|---|---|---|
| Closing stock | Credited to the trading account | Shown as a current asset |
| Outstanding (accrued) expense, e.g. salary unpaid | Added to that expense on the debit side | Shown as a current liability |
| Prepaid (unexpired) expense | Deducted from that expense on the debit side | Shown as a current asset |
| Accrued income, e.g. commission earned but not received | Added to that income on the credit side | Shown as a current asset |
| Income received in advance | Deducted from that income on the credit side | Shown as a current liability |
| Depreciation on a fixed asset | Debited to the profit and loss account | Deducted from the asset |
| Interest on capital | Debited to the profit and loss account | Added to capital |
| Interest on drawings | Credited to the profit and loss account | Deducted from capital |
| Goods taken by the owner for private use | Credited to purchases (or to trading account) | Deducted from capital as drawings |
| Goods distributed as free samples | Debited to advertisement | Deducted from purchases (or from closing stock) |
| Bad debts, and provision for doubtful debts | Debited to the profit and loss account | Deducted from debtors |
| Manager's commission on net profit | Debited to the profit and loss account | Shown as an outstanding liability |
| Loss of stock by fire, not insured | Debited to the profit and loss account | Stock reduced |

::: caution The common mistake
The single most expensive mistake in this unit is writing the first effect of an adjustment and forgetting the second. **Closing stock** is credited to the trading account *and* shown as an asset — miss the asset and the balance sheet is short by the whole stock figure. **Outstanding salary** is added to salary *and* shown as a liability. Before totalling, go down your list of adjustments and tick two effects for every one of them.
:::

```figure caption="Why an adjustment is never a single entry. One effect lands in a revenue statement and the other in the balance sheet, and both are needed or the balance sheet will not tally."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,2.6))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6)
ax.add_patch(FancyBboxPatch((3.6,2.4),2.8,1.3,boxstyle="round,pad=0.06",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(5.0,3.05,"ADJUSTMENT\ne.g. closing stock",ha='center',va='center',fontsize=7.4,color=INK,weight='bold')
ax.add_patch(FancyArrowPatch((4.3,3.75),(2.3,4.75),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.1))
ax.add_patch(FancyArrowPatch((5.7,3.75),(7.7,4.75),arrowstyle="-|>",mutation_scale=10,color=SERIES[1],lw=1.1))
ax.add_patch(FancyBboxPatch((0.2,4.6),4.1,1.2,boxstyle="round,pad=0.05",fc="#f6f8fc",ec=MUTED,lw=1.0))
ax.text(2.25,5.2,"Effect 1\nTrading / profit and loss account",ha='center',va='center',fontsize=6.8,color=INK)
ax.add_patch(FancyBboxPatch((5.7,4.6),4.1,1.2,boxstyle="round,pad=0.05",fc="#fdf3f3",ec=SERIES[1],lw=1.0))
ax.text(7.75,5.2,"Effect 2\nBalance sheet",ha='center',va='center',fontsize=6.8,color=INK)
ax.text(5.0,1.4,"Write one effect only and the balance sheet will not tally",ha='center',fontsize=6.6,color=MUTED)
```

## 7.4 Steps in preparing final accounts

1. **Complete the trial balance.** Total the debit and credit columns; find and correct any difference before starting.
2. **Adjust the closing entries for the trading account.** Bring in the closing stock, the returns, the direct expenses.
3. **Prepare the trading account** and find the gross profit or gross loss.
4. **Prepare the profit and loss account**, carrying the gross profit in and dealing with the indirect expenses and other incomes, applying every remaining adjustment. Find the net profit or net loss.
5. **Add the net profit to capital** (or deduct the net loss) and deduct the drawings.
6. **Prepare the balance sheet** in the usual order, taking the adjusted values of the assets and putting in every outstanding, prepaid and accrued item.
7. **Check that the two sides agree.** If they do not, look again at your adjustments — the difference is nearly always an adjustment whose second effect is missing.

**Order of presentation.** In a Nepali school answer the **trading and profit and loss account** is written with the debit side on the left and the credit side on the right, and the **balance sheet** is written with **liabilities on the left and assets on the right**.

## 7.5 Preparation of accounting notes

**Accounting notes (लेखा टिप्पणी)** are the short explanations attached to the financial statements, in which each item in the statements is described, the accounting policy applied to it is stated, and any figure that a reader could misinterpret is explained.

Under Nepal's accounting standards the notes are not optional — the statements are incomplete without them. Their purposes are: to **explain** the policies used (how stock is valued, how depreciation is charged, how foreign currency is translated); to **break down** a large figure into its parts (what is inside "other expenses"); to **disclose** matters that do not appear in the numbers at all, such as a pending court case, a contingent liability, or a guarantee given for another company; and to **reconcile** the figures in the statements with the underlying accounts.

For a Grade 10 answer, mention that notes state the **accounting policies**, explain **each item in the statements** in the order in which it appears, disclose **contingent liabilities and events after the balance sheet date**, and give the **supporting schedules** of fixed assets, debtors, creditors and loans. Notes make the statements understandable, comparable and honest.

::: example Full final accounts from a trial balance
**Problem.** The following is the trial balance of Surya Traders as on 31 Ashad 2082.

| Particulars | Debit (Rs.) | Credit (Rs.) |
|---|---|---|
| Opening stock | 40,000 | |
| Purchases | 2,00,000 | |
| Carriage inward | 10,000 | |
| Wages | 30,000 | |
| Salaries | 25,000 | |
| Rent | 15,000 | |
| Furniture | 60,000 | |
| Debtors | 45,000 | |
| Bank | 35,000 | |
| Cash | 5,000 | |
| Capital | | 1,20,000 |
| Sales | | 2,90,000 |
| Creditors | | 35,000 |
| Commission received | | 20,000 |
| **Total** | **4,65,000** | **4,65,000** |

Additional information: (i) closing stock Rs. 55,000; (ii) outstanding salary Rs. 5,000; (iii) prepaid rent Rs. 3,000; (iv) depreciation on furniture 10 per cent.

**Solution.**
Step 1 — *Trading account.* Debit: opening stock, purchases, carriage inward, wages, and gross profit c/d. Credit: sales and closing stock.
Cost of goods sold $= 40{,}000 + 2{,}00{,}000 + 10{,}000 + 30{,}000 - 55{,}000 = Rs.\ 2{,}25{,}000$; gross profit $= 2{,}90{,}000 - 2{,}25{,}000 = Rs.\ 65{,}000$.

*Trading account for the year ended 31 Ashad 2082*

| Particulars | Rs. | Particulars | Rs. |
|---|---|---|---|
| To Opening stock | 40,000 | By Sales | 2,90,000 |
| To Purchases | 2,00,000 | By Closing stock | 55,000 |
| To Carriage inward | 10,000 | | |
| To Wages | 30,000 | | |
| To Gross profit c/d | 65,000 | | |
| **Total** | **3,45,000** | **Total** | **3,45,000** |

Step 2 — *Profit and loss account.* Salary becomes $25{,}000 + 5{,}000 = Rs.\ 30{,}000$; rent becomes $15{,}000 - 3{,}000 = Rs.\ 12{,}000$; depreciation $= 10\% \times 60{,}000 = Rs.\ 6{,}000$.

*Profit and loss account for the year ended 31 Ashad 2082*

| Particulars | Rs. | Particulars | Rs. |
|---|---|---|---|
| To Salaries | 25,000 | By Gross profit b/d | 65,000 |
| To Add: outstanding salary | 5,000 | By Commission received | 20,000 |
| | 30,000 | | |
| To Rent | 15,000 | | |
| To Less: prepaid rent | 3,000 | | |
| | 12,000 | | |
| To Depreciation on furniture | 6,000 | | |
| To Net profit (transferred to capital) | 37,000 | | |
| **Total** | **85,000** | **Total** | **85,000** |

Step 3 — *Balance sheet.* Capital $= 1{,}20{,}000 + 37{,}000 = Rs.\ 1{,}57{,}000$; furniture $= 60{,}000 - 6{,}000 = Rs.\ 54{,}000$.

*Balance sheet as on 31 Ashad 2082*

| Liabilities | Rs. | Assets | Rs. |
|---|---|---|---|
| Capital | 1,20,000 | Furniture | 60,000 |
| Add: Net profit | 37,000 | Less: Depreciation | 6,000 |
| | 1,57,000 | | 54,000 |
| Creditors | 35,000 | Closing stock | 55,000 |
| Outstanding salary | 5,000 | Debtors | 45,000 |
| | | Bank | 35,000 |
| | | Cash | 5,000 |
| | | Prepaid rent | 3,000 |
| **Total** | **1,97,000** | **Total** | **1,97,000** |

**Answer.** Gross profit Rs. 65,000; net profit Rs. 37,000; balance sheet total Rs. 1,97,000.
:::

::: example Find the missing figures
**Problem.** From the following, compute the gross profit, the net profit and the closing capital.
Opening stock Rs. 30,000; purchases Rs. 1,80,000; carriage inward Rs. 8,000; wages Rs. 22,000; closing stock Rs. 40,000; sales Rs. 2,60,000; office salary Rs. 20,000; rent Rs. 10,000; advertisement Rs. 6,000; commission received Rs. 12,000; opening capital Rs. 90,000; drawings Rs. 15,000.

**Solution.**
Step 1 — Cost of goods sold $= 30{,}000 + 1{,}80{,}000 + 8{,}000 + 22{,}000 - 40{,}000 = Rs.\ 2{,}00{,}000$.
Step 2 — Gross profit $= 2{,}60{,}000 - 2{,}00{,}000 = Rs.\ 60{,}000$.
Step 3 — Total indirect expenses $= 20{,}000 + 10{,}000 + 6{,}000 = Rs.\ 36{,}000$.
Step 4 — Net profit $= 60{,}000 + 12{,}000 - 36{,}000 = Rs.\ 36{,}000$.
Step 5 — Closing capital $= 90{,}000 + 36{,}000 - 15{,}000 = Rs.\ 1{,}11{,}000$.

**Answer.** Gross profit Rs. 60,000; net profit Rs. 36,000; closing capital Rs. 1,11,000.
:::

::: example The two effects of each adjustment
**Problem.** State the two effects of each of the following adjustments: (a) closing stock Rs. 25,000; (b) outstanding wages Rs. 4,000; (c) insurance prepaid Rs. 2,000; (d) depreciation on machinery Rs. 9,000; (e) goods worth Rs. 3,000 taken by the proprietor for personal use.

**Solution.**
Step 1 — (a) Credited in the trading account (credit side) and shown as a current asset in the balance sheet.
Step 2 — (b) Added to wages on the debit side of the trading account and shown as a current liability in the balance sheet.
Step 3 — (c) Deducted from insurance on the debit side of the profit and loss account and shown as a current asset (prepaid insurance) in the balance sheet.
Step 4 — (d) Debited to the profit and loss account and deducted from machinery in the balance sheet.
Step 5 — (e) Credited to the purchases account (which reduces the cost of goods sold) and deducted from capital as drawings in the balance sheet.

**Answer.** As above. Notice that in each case one effect is in a revenue statement and the other in the balance sheet.
**What it means.** An adjustment is never a single entry. If only one effect is written, the profit will be right and the balance sheet wrong, or the reverse — and the balance sheet will not tally.
:::

::: memory The unit in one list
**Gross profit** = Sales − (Opening stock + Purchases + Direct expenses − Closing stock). **Net profit** = Gross profit + Other income − Indirect expenses. **Balance sheet** = Assets = Liabilities + Capital. **Every adjustment has two effects.** Deduct **drawings** from capital and **add net profit** to capital. Balance sheet order: **liabilities left, assets right**.
:::

## Chapter summary

- **Final accounts** are prepared at the end of the year from the trial balance, after adjustments, to show the profit or loss of the period and the financial position on the closing date. They are also called the financial statements.
- Their **objectives** are to find gross profit, to find net profit, to show the financial position, to allow comparison, to provide the basis for tax and audit, and to supply the owner with information for decisions.
- The **trading account** deals with goods: opening stock, purchases and direct expenses on the debit side; sales and closing stock on the credit side; the balance is the gross profit.
- $Gross\ profit = Sales - Cost\ of\ goods\ sold$ and $Cost\ of\ goods\ sold = Opening\ stock + Purchases + Direct\ expenses - Closing\ stock$.
- The **profit and loss account** starts with the gross profit and adds other incomes and deducts indirect expenses; the balance is the net profit.
- The **balance sheet** is a statement, not an account, of assets, liabilities and capital on the closing date: $Assets = Liabilities + Capital$.
- An **adjustment** brings in an item that is earned or incurred but not yet recorded. **Every adjustment has two effects** — one in the trading or profit and loss account and one in the balance sheet.
- The treatment of the common adjustments: closing stock (credit trading, asset), outstanding expense (add to expense, liability), prepaid expense (less from expense, asset), accrued income (add to income, asset), income in advance (less from income, liability), depreciation (debit profit and loss, deduct from asset), interest on capital (debit profit and loss, add to capital), interest on drawings (credit profit and loss, deduct from capital), goods taken by the owner (credit purchases, deduct from capital), provision for doubtful debts (debit profit and loss, deduct from debtors), manager's commission (debit profit and loss, liability).
- **Steps**: complete the trial balance; prepare the trading account; prepare the profit and loss account; carry the net profit to capital and deduct drawings; prepare the balance sheet; check that the two sides agree.
- **Accounting notes** explain the policies used, break down large figures, disclose contingent liabilities and events after the balance sheet date, and reconcile the statements with the accounts. The statements are incomplete without them.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What are final accounts? <span class="marks">[1]</span>
2. Write any two objectives of preparing final accounts. <span class="marks">[1]</span>
3. Write the formula for the cost of goods sold. <span class="marks">[1]</span>
4. How is outstanding salary treated in the final accounts? <span class="marks">[1]</span>
5. What is the treatment of prepaid rent? <span class="marks">[1]</span>
6. Where does the closing stock appear? <span class="marks">[1]</span>
7. What is depreciation? <span class="marks">[1]</span>
8. Where is the net profit shown in the balance sheet? <span class="marks">[1]</span>
9. How are drawings treated in the balance sheet? <span class="marks">[1]</span>
10. What is a provision for doubtful debts? <span class="marks">[1]</span>
11. What are accounting notes? <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Final accounts are the statements prepared at the end of an accounting period, after adjustments, to show the profit or loss of the period and the financial position on the closing date. They comprise the trading account, the profit and loss account and the balance sheet.
**2.** Any two of: to find the gross profit, to find the net profit, to show the financial position, to allow comparison with past years, to provide the basis for tax and audit, to help the owner decide.
**3.** $Cost\ of\ goods\ sold = Opening\ stock + Purchases + Direct\ expenses - Closing\ stock$.
**4.** Added to the salary on the debit side of the profit and loss account and shown as a current liability in the balance sheet.
**5.** Deducted from rent on the debit side of the profit and loss account and shown as a current asset in the balance sheet.
**6.** Credited in the trading account on the credit side and shown as a current asset in the balance sheet.
**7.** Depreciation is the fall in the value of a fixed asset caused by use, wear and tear, or the passage of time; it is charged as an expense every year.
**8.** Added to the capital on the liabilities side.
**9.** Deducted from the capital on the liabilities side.
**10.** A provision for doubtful debts is an amount set aside out of profit to cover the debts that are expected not to be recovered; it is debited to the profit and loss account and deducted from debtors.
**11.** Accounting notes are the explanations attached to the financial statements stating the accounting policies used, describing each item, and disclosing contingent liabilities and other matters that the figures alone do not show.
:::

**Group B — Short answer (5 marks each)**

1. What are final accounts? Explain their objectives. <span class="marks">[5]</span>
2. Explain the components of the financial statements prepared by a trading concern. <span class="marks">[5]</span>
3. Explain the effect of any five adjustments on the trading account, the profit and loss account and the balance sheet. <span class="marks">[5]</span>
4. From the following, compute the gross profit and the net profit. Opening stock Rs. 25,000; purchases Rs. 1,50,000; carriage inward Rs. 5,000; purchases returns Rs. 5,000; wages Rs. 20,000; sales Rs. 2,20,000; sales returns Rs. 10,000; closing stock Rs. 35,000; salary Rs. 18,000; rent Rs. 12,000; discount received Rs. 4,000. <span class="marks">[5]</span>
5. Why are accounting notes prepared with the financial statements? Explain any five points disclosed in them. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definition as in Group A answer 1. Objectives: to ascertain the gross profit or loss on trading; to ascertain the net profit or loss for the period; to show the financial position on the closing date; to make the results comparable with those of previous periods and of other businesses; to provide the basis for tax assessment, audit and loan applications; to help the owner and the management take decisions. (Any five explained.)
**2.** The trading account shows the gross result of buying and selling: opening stock, purchases, direct expenses and gross profit on the debit side; sales and closing stock on the credit side. The profit and loss account shows the net result: the gross profit and other income on the credit side; indirect expenses such as office salary, rent, depreciation and interest on the debit side. The balance sheet is a statement of assets, liabilities and capital on the closing date, with the net profit added to capital and drawings deducted. Explain each with one example of an item that belongs in it.
**3.** Example items: closing stock — credited to trading, current asset; outstanding salary — added to salary in profit and loss, current liability; depreciation — debited to profit and loss, deducted from the asset; prepaid insurance — deducted from insurance, current asset; interest on capital — debited to profit and loss, added to capital; goods taken by the proprietor — credited to purchases, deducted from capital as drawings. (Any five, each with both effects.)
**4.** Net sales $= 2{,}20{,}000 - 10{,}000 = Rs.\ 2{,}10{,}000$. Net purchases $= 1{,}50{,}000 - 5{,}000 = Rs.\ 1{,}45{,}000$. Cost of goods sold $= 25{,}000 + 1{,}45{,}000 + 5{,}000 + 20{,}000 - 35{,}000 = Rs.\ 1{,}60{,}000$. Gross profit $= 2{,}10{,}000 - 1{,}60{,}000 = Rs.\ 50{,}000$. Indirect expenses $= 18{,}000 + 12{,}000 = Rs.\ 30{,}000$. Net profit $= 50{,}000 + 4{,}000 - 30{,}000 = Rs.\ 24{,}000$.
**5.** Notes are prepared because the statements alone do not tell a reader which policies were applied, what a composite figure contains, or what obligations exist that do not appear as liabilities. They state the accounting policies (valuation of stock, method of depreciation); break down large items such as other expenses, debtors and creditors; give schedules of fixed assets, loans and investments; disclose contingent liabilities such as a pending court case or a guarantee given for another firm; disclose events after the balance sheet date; and reconcile the figures in the statements with the accounts.
:::

**Group C — Long answer (8 marks each)**

1. What are final accounts? Explain the steps in their preparation and the treatment of any five adjustments. <span class="marks">[8]</span>
2. The following is the trial balance of Himal Traders on 31 Chaitra 2082.

| Particulars | Debit (Rs.) | Credit (Rs.) |
|---|---|---|
| Opening stock | 50,000 | |
| Purchases | 3,00,000 | |
| Carriage inward | 10,000 | |
| Wages | 40,000 | |
| Salaries | 30,000 | |
| Rent | 18,000 | |
| Machinery | 80,000 | |
| Debtors | 60,000 | |
| Bank | 40,000 | |
| Cash | 6,000 | |
| Capital | | 1,50,000 |
| Sales | | 4,20,000 |
| Creditors | | 40,000 |
| Discount received | | 4,000 |
| **Total** | **6,14,000** | **6,14,000** |

Additional information: (i) closing stock Rs. 65,000; (ii) outstanding salary Rs. 6,000; (iii) prepaid rent Rs. 2,000; (iv) depreciation on machinery at 10 per cent. Prepare the trading account, the profit and loss account and the balance sheet. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Definition (1).* As in Group A answer 1.
*Steps (3).* Complete and agree the trial balance; bring in the closing entries for the trading account; prepare the trading account and find the gross profit; prepare the profit and loss account applying every remaining adjustment and find the net profit; add the net profit to capital and deduct drawings; prepare the balance sheet with the adjusted asset values and every outstanding, prepaid and accrued item; check that the two sides agree.
*Adjustments (4).* Explain any five from: closing stock, outstanding expense, prepaid expense, accrued income, income in advance, depreciation, interest on capital, interest on drawings, goods taken by the proprietor, provision for doubtful debts, manager's commission. Each must be shown with **both** its effects, and the answer should say plainly that every adjustment has two effects.
**2.**
*Trading account for the year ended 31 Chaitra 2082*

| Particulars | Rs. | Particulars | Rs. |
|---|---|---|---|
| To Opening stock | 50,000 | By Sales | 4,20,000 |
| To Purchases | 3,00,000 | By Closing stock | 65,000 |
| To Carriage inward | 10,000 | | |
| To Wages | 40,000 | | |
| To Gross profit c/d | 85,000 | | |
| **Total** | **4,85,000** | **Total** | **4,85,000** |

Check: COGS $= 50{,}000 + 3{,}00{,}000 + 10{,}000 + 40{,}000 - 65{,}000 = Rs.\ 3{,}35{,}000$; gross profit $= 4{,}20{,}000 - 3{,}35{,}000 = Rs.\ 85{,}000$.

*Profit and loss account for the year ended 31 Chaitra 2082*

| Particulars | Rs. | Particulars | Rs. |
|---|---|---|---|
| To Salaries | 30,000 | By Gross profit b/d | 85,000 |
| To Add: outstanding | 6,000 | By Discount received | 4,000 |
| | 36,000 | | |
| To Rent | 18,000 | | |
| To Less: prepaid | 2,000 | | |
| | 16,000 | | |
| To Depreciation on machinery | 8,000 | | |
| To Net profit | 29,000 | | |
| **Total** | **89,000** | **Total** | **89,000** |

*Balance sheet as on 31 Chaitra 2082*

| Liabilities | Rs. | Assets | Rs. |
|---|---|---|---|
| Capital | 1,50,000 | Machinery | 80,000 |
| Add: Net profit | 29,000 | Less: Depreciation | 8,000 |
| | 1,79,000 | | 72,000 |
| Creditors | 40,000 | Closing stock | 65,000 |
| Outstanding salary | 6,000 | Debtors | 60,000 |
| | | Bank | 40,000 |
| | | Cash | 6,000 |
| | | Prepaid rent | 2,000 |
| **Total** | **2,25,000** | **Total** | **2,25,000** |

Gross profit Rs. 85,000; net profit Rs. 29,000; balance sheet total Rs. 2,25,000.
:::

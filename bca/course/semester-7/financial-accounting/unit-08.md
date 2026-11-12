---
subject: Financial Accounting
grade: BCA Semester 7
unit: 8
title: Introduction to Company Accounts
hours: 9
area: BCA 403 · Financial Accounting · Unit 8
---

The TU syllabus ends with **company accounts**: what a company is, its types and salient features, the financial statements it prepares, **share capital** and its kinds, **debentures** and their kinds, the difference between shares and debentures, the **issue** of shares and debentures, and the **redemption of preference shares**. Until now the book dealt with a sole proprietor, whose capital is one number. A company's capital is split into thousands of small units owned by different people, and every one of them must be accounted for.

::: key What this unit gives you
- Meaning, features and types of company, with the Nepal position (Companies Act, 2063).
- The five meanings of "capital": authorised, issued, subscribed, called-up, paid-up.
- Equity and preference shares, debentures, and the table that separates shares from debentures.
- Journal entries for the **issue of shares** (application, allotment, calls, premium, over-subscription, calls in arrears), **forfeiture and re-issue**.
- Journal entries for **debentures** issued at par, discount or premium and redeemable at par or premium.
- **Redemption of preference shares** with the capital redemption reserve.
:::

## 8.1 What a company is

A **company** is an artificial legal person created by registration under the Companies Act. The law treats it as separate from the people who own it. That one idea produces the features below.

| Feature | Meaning |
|---|---|
| Separate legal entity | The company owns property, signs contracts and sues or is sued in its own name. The owners are not the company. |
| Limited liability | A shareholder can lose only the unpaid amount on his or her shares, not personal property. |
| Perpetual succession | Death or exit of a member does not end the company; it ends only by legal winding up. |
| Transferable shares | A member can sell shares (freely in a public company; with limits in a private one). |
| Common seal and registered name | The company acts through its board; its registered name carries *Limited* or *Ltd.*, *Pvt. Ltd.* |
| Separation of ownership and management | Shareholders own; directors elected by them manage. |

**Types of company in Nepal.** The Companies Act, 2063 (2006) recognises mainly **private** and **public** companies, and a company may be limited by shares or by guarantee, or be unlimited. As commonly taught: a **private** company has a restricted right to transfer shares, may be formed with one or more persons, and cannot invite the public to subscribe (the usual maximum is 101 shareholders); a **public** company may invite the public to buy its shares and debentures, needs more founders (the Act's minimum is seven) and must follow stricter disclosure rules. A public company that gets its shares traded on Nepal Stock Exchange (NEPSE) is **listed**, and its public issues are approved by the **Securities Board of Nepal (SEBON)**. Banks, insurance companies and hydropower companies you see on NEPSE are examples. Check the current Act and its amendments for thresholds: the principle matters more than the number in an exam.

::: note Nepal practice
Shares of listed companies in Nepal normally have a face (par) value of **Rs 100**; the IPO price is often the par value, and companies may issue shares at a premium after earning a track record. The worked examples in this unit use Rs 100 shares for that reason.
:::

## 8.2 Financial statements of a company

A company cannot use the simple "capital plus profit" balance sheet. Under **NFRS** (Nepal's version of IFRS) a complete set of statements has five parts.

1. **Statement of financial position** (balance sheet): assets, liabilities and **equity** (share capital, reserves, retained earnings) on a stated date.
2. **Statement of profit or loss and other comprehensive income.**
3. **Statement of changes in equity.**
4. **Statement of cash flows.**
5. **Notes**, including the accounting policies.

The equity side of the balance sheet is where companies differ most from sole traders:

| Equity item | What it holds |
|---|---|
| Share capital | Nominal value of shares issued and paid |
| Securities (share) premium | Amount received above the nominal value |
| General and other reserves | Profits kept back deliberately |
| Capital reserve | Gains that cannot be paid as dividend (for example profit on re-issue of forfeited shares) |
| Retained earnings | Undistributed profit of this and earlier years |

The adjustments of Unit 6 (depreciation, accruals, bad debts) apply to a company unchanged; what is new is **how its capital is raised and shown**, and that is the subject of the rest of this unit.

## 8.3 Share capital and its kinds

A company's capital is divided into **shares**, each with a **nominal (face) value**. The word "capital" has several layers (Figure 8.1).

| Term | Meaning | Example (Rs 100 shares) |
|---|---|---|
| **Authorised** (registered) capital | The maximum the company may issue, stated in its memorandum | 50,000 shares = Rs 50,00,000 |
| **Issued** capital | The part actually offered to the public or allotted | 40,000 shares = Rs 40,00,000 |
| **Subscribed** capital | The part of the issued capital that investors have applied for and been allotted | 38,000 shares = Rs 38,00,000 |
| **Called-up** capital | The part of the nominal value that the company has demanded so far | Rs 70 per share called = Rs 26,60,000 |
| **Paid-up** capital | The part of the called-up capital actually received | Rs 26,00,000 if Rs 60,000 is unpaid |
| **Uncalled** capital | Subscribed capital not yet demanded | Rs 30 per share x 38,000 = Rs 11,40,000 |
| **Calls in arrears** | Called amount not yet paid by members | Rs 60,000 above |

```svgfig label="8.1" caption="The layers of share capital, drawn as nested boxes with the figures of the table above (Rs lakh). Each inner box is a part of the box around it: authorised 50.0, issued 40.0, subscribed 38.0, called-up 26.6, paid-up 26.0. Calls in arrears are called-up minus paid-up."
f = Fig(600, 250)
f.box(20, 14, 560, 222, "", fill="#eff6ff", stroke=NAVY)
f.text(300, 30, "Authorised capital  Rs 50.0 lakh", size=11, color=NAVY, bold=True)
f.box(50, 44, 500, 180, "", fill=BLUE, stroke=NAVY)
f.text(300, 60, "Issued capital  Rs 40.0 lakh", size=11, color=NAVY, bold=True)
f.box(80, 74, 440, 138, "", fill="#bbf7d0", stroke=TEAL)
f.text(300, 90, "Subscribed capital  Rs 38.0 lakh", size=11, color=NAVY, bold=True)
f.box(110, 104, 380, 96, "", fill="#fde68a", stroke=AMBER)
f.text(300, 120, "Called-up capital  Rs 26.6 lakh", size=11, color=NAVY, bold=True)
f.box(140, 134, 320, 56, "Paid-up capital  Rs 26.0 lakh", fill="#ffffff", stroke=NAVY, color=NAVY, size=11, bold=True)
f.text(300, 202, "arrears Rs 0.6 lakh sit between paid-up and called-up", size=10, color=NAVY)
```

**Kinds of shares.**

1. **Equity (ordinary) shares.** Owners get dividend only if there is profit and the board declares it, after preference shareholders; they vote and bear the main risk, and they share the surplus when the company wins.
2. **Preference shares.** They have a **preferential right** to a fixed rate of dividend and to repayment of capital on winding up. Types: **cumulative** (unpaid dividend carries forward), **non-cumulative**, **participating** (share extra profit), **redeemable** (to be repaid on a date), **convertible** (may be converted into equity).

| Point | Equity share | Preference share |
|---|---|---|
| Dividend | Variable, from profit left | Fixed rate, paid first |
| Voting | Full | Usually none (only on their own rights) |
| Repayment on winding up | After everyone else | Before equity |
| Risk and reward | Highest | Lower |
| Redeemable? | No (permanent capital) | Yes, if so issued |

## 8.4 Debentures and the difference from shares

A **debenture** is a written acknowledgement of a **loan** to the company, issued under its seal, carrying a fixed rate of **interest** and usually repayable on a stated date. A debenture holder is a **creditor**; a shareholder is an **owner**.

**Kinds of debenture.** *Secured* (mortgage, a charge on assets) and *unsecured* (naked); *redeemable* (repaid at a date) and *irredeemable* (repaid only on winding up); *convertible* (may become shares) and *non-convertible*; *registered* (holder's name is on the company's register) and *bearer* (transferable by delivery).

| Basis | Shares | Debentures |
|---|---|---|
| Status of holder | Owner (member) | Creditor (lender) |
| Return | Dividend, from profit, varies | Interest, fixed, due whether or not there is profit |
| Voting | Yes (equity) | No |
| Repayment | Not repaid during life (equity) | Repaid on maturity |
| Security | None | Often secured on assets |
| Effect on tax | Dividend is not a cost before tax | Interest is an expense and reduces taxable profit |
| Risk to holder | Higher | Lower |
| Appears in balance sheet under | Equity | Non-current (or current) liabilities |

## 8.5 Issue of shares: the journal entries

Shares are usually issued in **instalments**: an amount with the **application**, a further amount on **allotment** (when shares are assigned to applicants), and later **calls** (first call, final call). The premium, if any, is usually asked on allotment. A separate **personal-looking account** is opened for each stage, and money received is first debited to Bank.

**Standard entries (per stage).**

| Event | Debit | Credit |
|---|---|---|
| Application money received | Bank | Share Application A/c |
| Shares allotted | Share Application A/c | Share Capital A/c (and refund or transfer of excess) |
| Allotment money due | Share Allotment A/c | Share Capital A/c (and Securities Premium A/c) |
| Allotment money received | Bank | Share Allotment A/c |
| Call due | Share Call A/c | Share Capital A/c |
| Call received | Bank (and Calls in Arrears A/c for unpaid) | Share Call A/c |

### Worked example 8.1: over-subscription with pro rata allotment

*Narayani Hydro Ltd* issues **10,000 equity shares of Rs 100 each at a premium of Rs 20**. Payable: Rs 30 on application, Rs 50 on allotment (including the premium of Rs 20) and Rs 40 on the first and final call. Applications are received for **12,000 shares**. The directors allot 10,000 shares **pro rata** (10 shares for every 12 applied) and adjust the excess application money against the allotment. All money is received.

*Reasoning.* Application money received = 12,000 x 30 = Rs 3,60,000. Money for the 10,000 shares allotted = 10,000 x 30 = Rs 3,00,000 goes to share capital; the excess of Rs 60,000 (for the 2,000 shares not allotted) is **not** refunded here but adjusted towards allotment. Allotment due = 10,000 x 50 = Rs 5,00,000, so cash needed on allotment = 5,00,000 - 60,000 = Rs 4,40,000. The call is 10,000 x 40 = Rs 4,00,000. Total received = 3,60,000 + 4,40,000 + 4,00,000 = Rs 12,00,000 = 10,000 x (100 + 20).

| No. | Particulars | Dr (Rs) | Cr (Rs) |
|---|---|---|---|
| 1 | Bank A/c | 3,60,000 | |
| | To Share Application A/c (12,000 x 30) | | 3,60,000 |
| 2 | Share Application A/c | 3,60,000 | |
| | To Share Capital A/c (10,000 x 30) | | 3,00,000 |
| | To Share Allotment A/c (excess adjusted) | | 60,000 |
| 3 | Share Allotment A/c (10,000 x 50) | 5,00,000 | |
| | To Share Capital A/c (10,000 x 30) | | 3,00,000 |
| | To Securities Premium A/c (10,000 x 20) | | 2,00,000 |
| 4 | Bank A/c | 4,40,000 | |
| | To Share Allotment A/c (5,00,000 - 60,000) | | 4,40,000 |
| 5 | Share First and Final Call A/c (10,000 x 40) | 4,00,000 | |
| | To Share Capital A/c | | 4,00,000 |
| 6 | Bank A/c | 4,00,000 | |
| | To Share First and Final Call A/c | | 4,00,000 |

Note that the allotment amount of Rs 50 is Rs 30 of capital plus the Rs 20 premium; students lose marks by crediting the whole 5,00,000 to share capital. After the six entries: **Share Capital = 3,00,000 + 3,00,000 + 4,00,000 = Rs 10,00,000 (10,000 x 100)** and **Securities Premium = Rs 2,00,000**, and all personal accounts are closed to nil.

If the shares had been **under-subscribed** (fewer applications than shares offered), the company allots only what it receives, or the issue fails if the **minimum subscription** the law requires is not reached and all money is refunded.

### Calls in arrears and calls in advance

If a shareholder does not pay a call on time, the unpaid amount is debited to **Calls in Arrears A/c** (and Bank is debited only with what was received). Money paid before it is called is **Calls in Advance A/c**, a liability that the company clears when the call is made. Calls in arrears are shown as a **deduction from called-up capital** in the balance sheet.

### Worked example 8.2: forfeiture and re-issue

*Himal Foods Ltd* has Rs 100 shares payable Rs 25 on application, Rs 35 on allotment and Rs 40 on the call. Mr Karki holds **100 shares**, paid application and allotment, but **does not pay the call** of Rs 40. After due notice the directors **forfeit** his shares. Later they re-issue all 100 forfeited shares as **fully paid at Rs 85 per share**.

*Forfeiture.* Called-up amount for 100 shares = 100 x 100 = Rs 10,000; unpaid = 100 x 40 = Rs 4,000 (calls in arrears); received = 100 x 60 = Rs 6,000, which is kept by the company.

| No. | Particulars | Dr (Rs) | Cr (Rs) |
|---|---|---|---|
| 1 | Share Capital A/c (100 x 100) | 10,000 | |
| | To Calls in Arrears A/c | | 4,000 |
| | To Share Forfeiture A/c | | 6,000 |
| 2 | Bank A/c (100 x 85) | 8,500 | |
| | Share Forfeiture A/c (discount allowed) | 1,500 | |
| | To Share Capital A/c (fully paid) | | 10,000 |
| 3 | Share Forfeiture A/c (6,000 - 1,500) | 4,500 | |
| | To Capital Reserve A/c | | 4,500 |

The discount on re-issue (Rs 15 per share) may not exceed the amount forfeited (Rs 60 per share); here 1,500 is well within 6,000. The remaining credit balance of the forfeiture account, **Rs 4,500, is a capital profit** and is transferred to **Capital Reserve**, not to profit and loss.

## 8.6 Issue of debentures

Debentures can be issued **at par** (at face value), **at a discount** (below face value) or **at a premium** (above it), and be **redeemable at par or at a premium**. The accounting idea is simple: the company records its **liability** at the amount it will have to repay and treats any shortfall between that and the cash received as a **loss (cost) of raising the loan**, written off over the life of the debentures.

| Issued at | Redeemable at | Bank Dr | Debentures Cr | Other entries |
|---|---|---|---|---|
| Par | Par | Face value | Face value | none |
| Par | Premium | Face value | Face value | Loss on issue Dr; Premium payable on redemption Cr |
| Discount | Par | Less than face value | Face value | Discount (loss) on issue Dr |
| Discount | Premium | Less than face value | Face value | Loss on issue Dr (discount + premium); Premium payable Cr |
| Premium | Par | More than face value | Face value | Securities Premium Cr (a capital gain) |

### Worked example 8.3: issue at a discount, redeemable at a premium

*Sundar Cement Ltd* issues **1,000 10% debentures of Rs 100 each** at a **5% discount**, redeemable after five years at a **10% premium**.

*Reasoning.* Cash received = 1,000 x 95 = Rs 95,000. Liability at redemption = 1,000 x (100 + 10) = Rs 1,10,000 (the face value Rs 1,00,000 plus the premium of Rs 10,000). The company therefore carries a **loss on issue** of 1,10,000 - 95,000 = Rs 15,000, made of the discount Rs 5,000 and the premium Rs 10,000.

| Particulars | Dr (Rs) | Cr (Rs) |
|---|---|---|
| Bank A/c | 95,000 | |
| Loss on Issue of Debentures A/c | 15,000 | |
| To 10% Debentures A/c | | 1,00,000 |
| To Premium Payable on Redemption A/c | | 10,000 |

Each year, interest at 10% on Rs 1,00,000 = Rs 10,000 is charged to profit and loss (the debenture interest is an expense, and tax on it is deducted at source where the law requires, the TDS entry of Unit 2), and one-fifth of the loss on issue (Rs 3,000) is written off. At the end of year 5 the liability of Rs 1,10,000 is paid.

::: caution Common mistakes
Crediting the premium payable on redemption to Securities Premium is wrong: it is a **liability** until redemption. Treating the loss on issue as a fictitious asset that never goes away is also wrong; it must be written off over the term (usually from profit or securities premium).
:::

## 8.7 Redemption of preference shares

**Redemption** means repaying redeemable preference shares. Because it returns capital to some owners, the law protects creditors: shares may be redeemed only if they are **fully paid** and, as commonly taught in Nepal and under IFRS-style practice, only out of (a) **profits that would otherwise be distributable as dividend** or (b) the **proceeds of a fresh issue** of shares made for the purpose. To keep the total capital cushion intact, when profits are used the company transfers an amount equal to the **nominal value redeemed out of profits** to a **Capital Redemption Reserve (CRR)**, which cannot be paid out as dividend. Any **premium on redemption** is charged to securities premium or, if that is not enough, to profit and loss.

**Steps.**

1. Issue new shares (if any) to raise cash: Bank Dr, Share Capital Cr.
2. Redeem: Preference Share Capital Dr, Premium on Redemption Dr; to Preference Shareholders Cr.
3. Charge the premium to Securities Premium or Profit and Loss.
4. Transfer to CRR the nominal value redeemed minus the fresh issue (the part met from profits), debiting General Reserve or Profit and Loss.
5. Pay the shareholders: Preference Shareholders Dr, Bank Cr.

### Worked example 8.4

*Terai Textiles Ltd* has **5,000 redeemable 8% preference shares of Rs 100** (Rs 5,00,000) to be redeemed at a **10% premium**. To help the payment it issues **2,000 equity shares of Rs 100 at par** (Rs 2,00,000, all received). It has General Reserve Rs 3,00,000 and Profit and Loss credit balance Rs 1,00,000; it has no securities premium.

*Reasoning.* Amount to pay = 5,000 x 110 = Rs 5,50,000; premium = Rs 50,000. The part of the nominal value met from profits = 5,00,000 - 2,00,000 = **Rs 3,00,000**, so CRR = Rs 3,00,000 from the General Reserve. The premium of Rs 50,000 is charged to Profit and Loss (balance 1,00,000, enough). Total profits used = 3,00,000 + 50,000 = 3,50,000, which does not exceed the 4,00,000 available. The bank must supply the other 5,50,000 - 2,00,000 = Rs 3,50,000 from its existing balance.

| No. | Particulars | Dr (Rs) | Cr (Rs) |
|---|---|---|---|
| 1 | Bank A/c | 2,00,000 | |
| | To Equity Share Capital A/c | | 2,00,000 |
| 2 | 8% Preference Share Capital A/c | 5,00,000 | |
| | Premium on Redemption of Preference Shares A/c | 50,000 | |
| | To Preference Shareholders A/c | | 5,50,000 |
| 3 | Profit and Loss A/c | 50,000 | |
| | To Premium on Redemption of Preference Shares A/c | | 50,000 |
| 4 | General Reserve A/c | 3,00,000 | |
| | To Capital Redemption Reserve A/c | | 3,00,000 |
| 5 | Preference Shareholders A/c | 5,50,000 | |
| | To Bank A/c | | 5,50,000 |

After these entries the preference capital is gone, equity capital is higher by Rs 2,00,000, CRR is Rs 3,00,000, General Reserve is nil, Profit and Loss is Rs 50,000 and cash is lower by Rs 3,50,000. Total equity changed by +2,00,000 (new shares) - 5,00,000 (preference) + 3,00,000 (CRR) - 3,00,000 (General Reserve) - 50,000 (P and L) = -3,50,000 *as a group*, equal to the net cash that left. Check in Python:

```python
# Worked examples 8.1 to 8.4: independent check of every figure
app, cap = 12000 * 30, 10000 * 30
allot_cash = 10000 * 50 - (app - cap)
call = 10000 * 40
assert app + allot_cash + call == 10000 * (100 + 20)
print("8.1 total received:", app + allot_cash + call, "| capital", 10000 * 100, "| premium", 10000 * 20)

capital_called, arrears = 100 * 100, 100 * 40
forfeit = capital_called - arrears
discount = 100 * (100 - 85)
print("8.2 forfeited:", forfeit, "| capital reserve:", forfeit - discount)

cash, liability = 1000 * 95, 1000 * 110
print("8.3 loss on issue:", liability - cash, "| yearly write-off:", (liability - cash) // 5)

pay, fresh = 5000 * 110, 2000 * 100
crr, prem = 5000 * 100 - fresh, 5000 * 10
print("8.4 pay:", pay, "| CRR:", crr, "| profits used:", crr + prem, "| cash from bank:", pay - fresh)
```
```output
8.1 total received: 1200000 | capital 1000000 | premium 200000
8.2 forfeited: 6000 | capital reserve: 4500
8.3 loss on issue: 15000 | yearly write-off: 3000
8.4 pay: 550000 | CRR: 300000 | profits used: 350000 | cash from bank: 350000
```
## 8.8 Seeing the ideas: where each item sits in the balance sheet

```svgfig label="8.2" caption="Equity and liabilities of a company after Worked Example 8.1 and 8.3: shares sit in equity (owners), debentures sit in liabilities (lenders), and securities premium is part of equity. Figures in Rs lakh (illustrative combined company)."
f = Fig(600, 230)
f.text(150, 18, "Equity", size=12, color=NAVY, bold=True)
f.box(40, 30, 220, 44, "Share capital  10.00", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(40, 80, 220, 34, "Securities premium  2.00", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(40, 120, 220, 34, "Capital reserve  0.045", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(40, 160, 220, 34, "Retained earnings", fill="#ffffff", stroke=NAVY, color=NAVY, size=11, bold=True)
f.text(450, 18, "Liabilities", size=12, color=NAVY, bold=True)
f.box(340, 30, 220, 44, "10% debentures  1.00", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(340, 80, 220, 34, "Premium payable  0.10", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(340, 120, 220, 34, "Trade payables", fill="#ffffff", stroke=NAVY, color=NAVY, size=11, bold=True)
f.text(150, 214, "owners: dividend, vote, last claim", size=10, color=NAVY)
f.text(450, 214, "lenders: interest, no vote, repaid first", size=10, color=NAVY)
```

## Formula and fact sheet

- Company = separate legal entity, limited liability, perpetual succession, transferable shares.
- Authorised ≥ Issued ≥ Subscribed ≥ Called-up ≥ Paid-up; calls in arrears = called-up - paid-up.
- Share entries: Bank → Application → Capital; excess application money adjusted to allotment; **premium is credited to Securities Premium, never to Share Capital**.
- Forfeiture: Share Capital Dr (called-up) | Calls in Arrears Cr | Share Forfeiture Cr (amount received). Re-issue discount ≤ forfeited amount; balance of forfeiture → Capital Reserve.
- Debentures: record the **redemption amount** as liability; loss on issue = redemption amount - cash received; interest is an expense (profit and loss), dividend is an appropriation.
- Redeem preference shares only if fully paid, out of distributable profits or fresh issue; CRR = nominal redeemed - fresh issue; premium on redemption from securities premium or profit and loss.

## Chapter summary

- A company is a separate legal person whose capital is split into shares; limited liability and perpetual succession follow.
- Share capital has five layers from authorised to paid-up; equity shares carry risk and vote, preference shares carry a fixed preferential dividend.
- Shares give ownership and a dividend; debentures are loans carrying interest and sit in liabilities.
- Share issues pass through application, allotment and call accounts, with premium to Securities Premium and excess application money adjusted; unpaid calls become arrears and may lead to forfeiture and re-issue.
- Debenture issues record the liability at the redemption amount and write the loss on issue off over the term.
- Preference shares are redeemed from profits or a fresh issue, and a capital redemption reserve protects creditors.

## Practice

1. Define a company and list its salient features.
2. Differentiate between a private and a public company.
3. Explain authorised, issued, subscribed, called-up and paid-up capital with an example.
4. Distinguish equity shares from preference shares, and shares from debentures.
5. A company issues 4,000 shares of Rs 100 at par, payable Rs 30 on application, Rs 30 on allotment and Rs 40 on call, all received. Give the journal and the total share capital.
6. Applications for 9,000 shares are received against an offer of 6,000 shares of Rs 100 at Rs 10 premium, application Rs 25, allotment Rs 45 (with premium), call Rs 40. Allot pro rata and find the excess adjusted and the cash needed on allotment.
7. 100 shares of Rs 100 on which Rs 60 was received are forfeited and re-issued at Rs 70 as fully paid. Find the loss on re-issue and the capital reserve.
8. 500 debentures of Rs 100 are issued at a 10% premium, redeemable at par. Journalise.
9. What conditions govern the redemption of preference shares and why is a CRR created?
10. Why is a premium on redemption of debentures a liability and not a gain?

::: note Answers and worked solutions
**1.** A voluntary association registered under the Companies Act, an artificial legal person with limited liability, perpetual succession, a common name and transferable shares.
**2.** A private company limits transfer of shares, may have as few as one member and a ceiling on members, and cannot invite the public; a public company can invite the public, needs more founders and publishes more.
**3.** Authorised is the maximum allowed (Rs 50 lakh), issued is what is offered (Rs 40 lakh), subscribed is what is taken up (Rs 38 lakh), called-up is the part demanded, paid-up is what has actually come in.
**4.** Equity: variable dividend, votes, last claim, no redemption; preference: fixed dividend, no vote, preferential claim, may be redeemable. Shares: ownership and dividend; debentures: loan and interest (see the table in 8.4).
**5.** Application: Bank Dr 1,20,000 Cr Share Application; Share Application Dr 1,20,000 Cr Share Capital 1,20,000. Allotment: Share Allotment Dr 1,20,000 Cr Share Capital 1,20,000; Bank Dr 1,20,000 Cr Share Allotment. Call: Share Call Dr 1,60,000 Cr Share Capital 1,60,000; Bank Dr 1,60,000 Cr Call. Total share capital = 4,00,000.
**6.** Application money = 9,000 x 25 = 2,25,000; for 6,000 shares = 1,50,000; excess = 75,000. Allotment due = 6,000 x 45 = 2,70,000 (capital 6,000 x 35 = 2,10,000 and premium 6,000 x 10 = 60,000); cash needed = 2,70,000 - 75,000 = 1,95,000. Pro rata ratio is 2 shares for every 3 applied.
**7.** Received Rs 6,000. Re-issue at Rs 70: discount = 100 x 30 = 3,000. Forfeiture account: credit 6,000, debit 3,000, balance 3,000 transferred to capital reserve.
**8.** Bank Dr 55,000; To 10% Debentures 50,000; To Securities Premium 5,000 (premium on issue is a capital gain because redemption is at par).
**9.** Only fully paid shares; only from distributable profits or a fresh issue; a CRR equal to the nominal value redeemed from profits is created so that creditors' cushion does not shrink and the amount cannot be paid as dividend.
**10.** Because at redemption the company must pay it to the holder; it is part of what the company owes from the day the debentures are issued.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distinguish between shares and debentures.**

*Introduction.* Both are ways to raise long-term funds, but a share is a unit of ownership and a debenture is a loan.

1. **Status.** A shareholder is an owner; a debenture holder is a creditor.
2. **Return.** Dividend on shares depends on profit and the board's decision; interest on debentures is fixed and must be paid.
3. **Voting.** Equity shareholders vote; debenture holders do not.
4. **Repayment.** Equity shares are not repaid in the life of the company; debentures are repaid on maturity.
5. **Security and risk.** Debentures are often secured on assets and carry lower risk; shares carry the highest risk and reward.
6. **Tax and presentation.** Interest is an expense; dividend is an appropriation of profit. Shares appear under equity, debentures under liabilities.

**Q2 (10 marks). Explain the different kinds of share capital. Journalise the issue of 10,000 shares of Rs 100 at a premium of Rs 20 payable Rs 30 on application, Rs 50 on allotment (including premium) and Rs 40 on call, if 12,000 shares are applied for and allotted pro rata.**

*Part A: kinds of capital* (Section 8.3, Figure 8.1): authorised, issued, subscribed, called-up, paid-up, uncalled, calls in arrears, each with a one-line meaning.

*Part B: journal.* Use the six entries of Worked Example 8.1 with figures: Bank 3,60,000; Application to Capital 3,00,000 and to Allotment 60,000; Allotment due 5,00,000 split 3,00,000 capital and 2,00,000 premium; Bank 4,40,000; Call 4,00,000 due and received. Final balances: Share Capital Rs 10,00,000, Securities Premium Rs 2,00,000.

**Q3 (5 marks). What is forfeiture of shares? Show its entries and the treatment of the balance after re-issue.**

When a shareholder fails to pay a call after notice, the directors may cancel the shares and keep the money already paid. Entry: Share Capital Dr (called-up amount); Calls in Arrears Cr (unpaid); Share Forfeiture Cr (amount received). On re-issue the cash received is debited together with any discount (which may not exceed the forfeited amount) and Share Capital is credited at the full called-up value. The balance remaining in Share Forfeiture after the discount is a capital profit, so it is transferred to Capital Reserve.

**Q4 (5 marks). Explain how preference shares are redeemed.**

Conditions: shares must be redeemable and fully paid; money must come from distributable profits or from a fresh issue of shares. A Capital Redemption Reserve equal to the nominal value redeemed out of profits is created. Premium on redemption is written off against securities premium or profit and loss. Entries: Bank/Share Capital for the fresh issue; Preference Capital and Premium to Preference Shareholders; General Reserve/P and L to CRR; Preference Shareholders to Bank (Worked Example 8.4).

---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 5
title: e-Business, e-Commerce and Digital Payments in Nepal
hours: 8
area: BCA 304 · MIS and e-Business · Unit 5
---

You can order a pair of shoes on a phone in Pokhara, pay with a QR code from a bank account in Biratnagar, and have the shoes delivered in a few days. Three networks cooperated: a marketplace that matched you with a seller, a payment system that moved money between two banks that have never spoken to each other directly, and a logistics network. This unit separates the business ideas (e-business models, revenue models, metrics) from the plumbing (how Nepal's retail payments are cleared and settled), and then shows how to count, in rupees, whether an online business is healthy.

::: key What this unit gives you
- e-business versus e-commerce; B2B, B2C, C2C, B2G/G2C, and m-commerce models and revenue models.
- Funnel, conversion, CAC and customer lifetime value calculations.
- Nepal's digital payment architecture: the central bank's role, switches, ConnectIPS, QR payments, wallets and licensing; clearing and multilateral netting with numbers.
:::

## 5.1 e-Business and e-Commerce

**e-Business** is the use of the Internet and related technologies to run *all* the processes of a business: buying, selling, serving customers, collaborating with partners, and internal operations (ERP, e-learning, e-recruitment). **e-Commerce** is the narrower part concerned with *buying and selling* goods and services and the payments that go with them. e-Commerce has stages: pre-sale (search, comparison), the order and payment, delivery, and after-sales service. Benefits: global reach at low cost, 24-hour service, lower transaction and inventory cost, personalisation, and easy measurement. Limits in Nepal: uneven connectivity, trust and fraud worries, cash-on-delivery habit, address and logistics challenges, and thin card penetration.

| Model | Parties | Example | Typical revenue |
|---|---|---|---|
| **B2C** (business to consumer) | Firm sells to individuals | Online shop, ticketing, food delivery | Product margin, delivery fees |
| **B2B** (business to business) | Firm sells to firm | Wholesale portal, e-procurement | Per-order margin, subscription |
| **C2C** (consumer to consumer) | Individuals via a platform | Second-hand marketplace (Hamrobazar-type classifieds) | Listing fees, advertising, commission |
| **B2G / G2C / G2B** | Business or citizen with government | Online tax filing, bill payment, Nagarik App services | Service charges (or none) |
| **P2P / social commerce** | Users trade through social platforms | Facebook shops, live selling | Often none; platform ads |
| **m-commerce** | Any of the above on a mobile phone | Wallet shopping, app ordering | As above |

**Revenue models:** direct sales, *commission* on transactions, *subscription*, *advertising*, *listing or membership fees*, *freemium*, *affiliate* links, and *data/analytics* services. A **marketplace** earns commission but owns no stock; an **inventory model** takes the stock risk; a **dropshipper** orders from the supplier after the customer pays.

## 5.2 The online customer funnel and unit economics

An online business is managed as a **funnel**: visitors, then add-to-cart, then checkout, then payment. **Conversion rate** = orders ÷ visitors. Suppose 100,000 visitors in a month with step rates 5%, 40% and 70%:

| Funnel stage | Users | Step rate |
|---|---|---|
| Visitors | 100000 |  |
| Add to cart | 5,000 | 5% |
| Start checkout | 2,000 | 40% |
| Complete payment | 1,400 | 70% |

The overall conversion is **1.40%**, giving **1,400 orders**. Improving the weakest step is cheapest: raising checkout completion from 70% to 80% adds 200 orders without any extra advertising.

**Customer acquisition cost (CAC)** = marketing spend ÷ new customers. With Rs 1,50,000 of advertising and 1,400 orders, CAC = **Rs 107.14**. If the average order value is Rs 2,400 with 22% gross margin, **gross profit per order** is Rs **528**, so the first order already covers its acquisition cost with Rs 420.86 left over. **Customer lifetime value (LTV)** = gross profit per order × orders per year ÷ annual churn. With 3 orders a year and 25% churn (expected life 4 years), LTV = 528 × 3 / 0.25 = **Rs 6,336**, and LTV/CAC = **59.1**. A ratio above 3 is generally healthy; this one is implausibly high, which tells the analyst that the sample is too small or that the CAC ignores returns, delivery cost and discounts. *The usefulness of the metric is in knowing which assumption to challenge.*

## 5.3 The payment problem

Buying online needs a way for money to move between the buyer's account and the seller's. In cash-based economies this is the hardest part of e-commerce. Payment instruments: **cards** (debit, credit), **bank transfer** (account to account), **mobile wallets** (stored value), **QR payments**, **cash on delivery (COD)**, and (in some countries) **mobile money** accounts at telecoms. Every electronic payment passes through three stages: **authorisation** (is the payer allowed and funded?), **clearing** (exchanging the payment instructions among banks) and **settlement** (the actual movement of funds between the banks' accounts at the central bank).

## 5.4 Nepal's payment architecture

*Specific limits, fees and product names change often; consult the current Nepal Rastra Bank (NRB) circulars and the operators' websites before relying on them.*

### The regulator and the law

The **Nepal Rastra Bank**, the central bank, regulates and oversees payments under the **Payment and Settlement Act, 2075 (2019)** and its by-laws. NRB issues licences and sets rules for risk, customer protection and interoperability. Two licence families matter in this unit: a **Payment System Operator (PSO)** runs a payment *system* (a switch, a clearing house, or a QR network connecting many institutions); a **Payment Service Provider (PSP)** offers payment *services* to customers, such as a mobile wallet or a prepaid card. Banks and financial institutions, licensed by NRB, issue accounts and cards. The settlement of final balances happens in the banks' accounts held at NRB, which is why central-bank money is the "settlement asset".

### The main infrastructure pieces

| Component | Operator and role |
|---|---|
| **Nepal Clearing House Limited (NCHL)** | A PSO owned by banks and institutions. Runs the **National Payment Interface (NPI)** for interoperable transfers, **ConnectIPS** (account-to-account credit transfers for bills, remittance, salaries and e-commerce, in which the customer authorises a debit from their bank account in a bank-neutral web or mobile flow), and cheque clearing (ECC); also **NepalPay QR**, a QR scheme |
| **Fonepay** | A PSO that operates a switch connecting banks' accounts and cards with merchants' **Fonepay QR** codes and ATM/POS networks; most merchants display one |
| **Wallets (PSPs)** such as eSewa, Khalti, IME Pay | Hold the user's stored value; pay merchants, bills and top-ups; the user loads money from a bank account (often through ConnectIPS) |
| **Card networks and bank switches** | Domestic cards processed by bank switches; international cards connect through global networks |
| **Banks and NRB** | Hold customer accounts and, for final settlement, the banks' accounts at NRB |

Operationally, the flow of a QR payment is: (1) the merchant displays a static or dynamic QR code with an identifier; (2) the customer scans it in a bank or wallet app; (3) the app sends an authorisation request through the switch to the customer's bank or wallet; (4) the debit is made and the merchant's bank or wallet is notified; (5) the switch records the obligation and (6) *net* positions between institutions are settled periodically at the central bank. Wallet balances are backed by funds that the PSP must hold in a **settlement or escrow account at a bank**; the customer's wallet balance is a claim on that bank-held pool. Customers' eKYC (identity verification) and limits per transaction and per month are set by NRB's rules.

### Clearing by multilateral netting: a worked example

If every payment between banks were settled one by one, the volume of settlement transfers would be huge. Switches therefore **net** obligations: each bank pays or receives only the *net* of everything it owes and is owed. Below is an invented day's obligations among four banks (rupees in crore; row = payer, column = receiver):

| From \ To | A | B | C | D | Total sent |
|---|---|---|---|---|---|
| A | 0 | 120 | 80 | 60 | 260 |
| B | 90 | 0 | 50 | 100 | 240 |
| C | 110 | 70 | 0 | 40 | 220 |
| D | 30 | 130 | 90 | 0 | 250 |
| **Total received** | 230 | 320 | 220 | 200 | 970 |

Each bank's net position is received minus sent. The positions always sum to zero (money is only moved, never created).

| Bank | Sent | Received | Net position | Settles |
|---|---|---|---|---|
| A | 260 | 230 | -30 | pays |
| B | 240 | 320 | +80 | receives |
| C | 220 | 220 | +0 | — |
| D | 250 | 200 | -50 | pays |

Gross obligations total **970** crore, but only **80** crore must actually move (the sum of the positive net positions): a saving of **91.8%**. Netting only between pairs (bilateral) would still require 190 crore of transfers, so multilateral netting through a central switch is more efficient. The risk side: a bank that cannot pay its net debit on settlement breaks the whole cycle, so participants pre-fund collateral or have limits ("settlement risk").

### Why it matters for an e-business

A merchant choosing payment options is choosing fees, settlement time (T+0, T+1), refund process, chargeback or dispute handling, and the risk of fraud. Typical integration: the merchant's website redirects the buyer to a **payment gateway** (a PSP such as a wallet or the bank's page), the gateway returns a **success/failure callback**, and the merchant's server **verifies** the transaction by calling the gateway's lookup API before delivering the goods (never trust the browser redirect alone). Unit 6 covers the controls around this.

## 5.5 Building and running an e-business

An online business needs: a **platform** (own site with a CMS or shop framework, or a marketplace seller account), a **catalogue**, a **payment gateway**, **logistics** (own riders or courier partners, with Nepal-specific issues such as incomplete street addresses and COD returns), **customer service**, **analytics** (funnel, abandoned carts) and **legal compliance** (company registration, VAT, consumer protection, the Electronic Transactions Act 2063). Typical pitfalls: underestimating delivery and returns costs, running promotions that destroy margin, and ignoring mobile-first design when most users arrive by phone.

## Chapter summary

- e-Business covers all online business processes; e-commerce is online trade; models include B2C, B2B, C2C, G2C and m-commerce with revenue by margin, commission, subscription or advertising.
- Funnel metrics, CAC and LTV tell whether growth is profitable; sanity-check the assumptions.
- A payment passes through authorisation, clearing and settlement; NRB licenses PSOs and PSPs under the Payment and Settlement Act 2075.
- NCHL (NPI, ConnectIPS), Fonepay (switch and QR), wallets and banks form the retail payment network; multilateral netting reduces settlement transfers.
- Always verify payment status server-side with the gateway before fulfilment.

## Practice

1. Differentiate e-business from e-commerce.
2. Classify: (a) buying a train-style ticket online, (b) a wholesaler's ordering portal for shops, (c) selling a used phone on a classifieds site, (d) paying electricity bills online.
3. For 80,000 visitors with rates 4%, 50% and 80%, compute the number of orders and the conversion rate.
4. CAC is Rs 200 and LTV Rs 900. What is LTV/CAC? Is it healthy?
5. Explain authorisation, clearing and settlement.
6. What is the difference between a PSO and a PSP? Give one example of each from this chapter.
7. In the netting example, which banks pay, which receive, and how much moves?
8. Why must a merchant verify payment server-side?
9. Why does a wallet need an escrow or settlement account at a bank?
10. List four risks specific to selling online in Nepal.

::: note Answers and worked solutions
**1.** e-business: all business processes online (including internal ones). e-commerce: buying and selling online.
**2.** (a) B2C; (b) B2B; (c) C2C; (d) G2C/B2G (citizen-to-government payment) or B2C if the utility is a company.
**3.** 80,000 × 0.04 = 3,200; × 0.5 = 1,600; × 0.8 = **1,280 orders**; conversion 1,280/80,000 = **1.6%**.
**4.** 900 / 200 = 4.5, above the common threshold of 3: healthy, subject to the assumptions behind LTV.
**5.** Authorisation: check the payer and funds. Clearing: exchange and reconcile payment instructions between institutions. Settlement: move final funds between banks' accounts at the central bank.
**6.** PSO operates a payment system (NCHL, Fonepay); PSP offers customer-facing services such as a wallet (eSewa, Khalti).
**7.** Net positions (crore): see the table; positive banks receive and negative banks pay, and the total moved is 80 crore.
**8.** A browser redirect can be forged or interrupted; only a server-to-server lookup proves the payment really succeeded.
**9.** Wallet balances are claims on real money; the escrow account protects customers' funds from the PSP's own creditors and risks.
**10.** Fraud and chargebacks, COD return costs, address and delivery problems, connectivity limits and low trust in online payments.
:::

---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 7
title: e-Business, e-Commerce and Digital Payments in Nepal
hours: 8
area: BCA 304 · MIS and e-Business · Unit 7
---

You can order a pair of shoes on a phone in Pokhara, pay with a QR code from a bank account in Biratnagar, and have the shoes delivered in a few days. Three networks cooperated: a marketplace that matched you with a seller, a payment system that moved money between two banks that have never spoken to each other directly, and a logistics network. This unit separates the business ideas (e-business models, revenue models, metrics) from the plumbing (how Nepal's retail payments are cleared and settled), and then shows how to count, in rupees, whether an online business is healthy.

::: key What this unit gives you
- e-business versus e-commerce; B2B, B2C, C2C, B2G/G2C, and m-commerce models and revenue models.
- Funnel, conversion, CAC and customer lifetime value calculations.
- Nepal's digital payment architecture: the central bank's role, switches, ConnectIPS, QR payments, wallets and licensing; clearing and multilateral netting with numbers.
:::

## 7.1 e-Business and e-Commerce

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

## 7.2 The online customer funnel and unit economics

An online business is managed as a **funnel**: visitors, then add-to-cart, then checkout, then payment. **Conversion rate** = orders ÷ visitors. Suppose 100,000 visitors in a month with step rates 5%, 40% and 70%:

| Funnel stage | Users | Step rate |
|---|---|---|
| Visitors | 100000 |  |
| Add to cart | 5,000 | 5% |
| Start checkout | 2,000 | 40% |
| Complete payment | 1,400 | 70% |

The overall conversion is **1.40%**, giving **1,400 orders**. Improving the weakest step is cheapest: raising checkout completion from 70% to 80% adds 200 orders without any extra advertising.

**Customer acquisition cost (CAC)** = marketing spend ÷ new customers. With Rs 1,50,000 of advertising and 1,400 orders, CAC = **Rs 107.14**. If the average order value is Rs 2,400 with 22% gross margin, **gross profit per order** is Rs **528**, so the first order already covers its acquisition cost with Rs 420.86 left over. **Customer lifetime value (LTV)** = gross profit per order × orders per year ÷ annual churn. With 3 orders a year and 25% churn (expected life 4 years), LTV = 528 × 3 / 0.25 = **Rs 6,336**, and LTV/CAC = **59.1**. A ratio above 3 is generally healthy; this one is implausibly high, which tells the analyst that the sample is too small or that the CAC ignores returns, delivery cost and discounts. *The usefulness of the metric is in knowing which assumption to challenge.*

## 7.3 The payment problem

Buying online needs a way for money to move between the buyer's account and the seller's. In cash-based economies this is the hardest part of e-commerce. Payment instruments: **cards** (debit, credit), **bank transfer** (account to account), **mobile wallets** (stored value), **QR payments**, **cash on delivery (COD)**, and (in some countries) **mobile money** accounts at telecoms. Every electronic payment passes through three stages: **authorisation** (is the payer allowed and funded?), **clearing** (exchanging the payment instructions among banks) and **settlement** (the actual movement of funds between the banks' accounts at the central bank).

## 7.4 Nepal's payment architecture

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

A merchant choosing payment options is choosing fees, settlement time (T+0, T+1), refund process, chargeback or dispute handling, and the risk of fraud. Typical integration: the merchant's website redirects the buyer to a **payment gateway** (a PSP such as a wallet or the bank's page), the gateway returns a **success/failure callback**, and the merchant's server **verifies** the transaction by calling the gateway's lookup API before delivering the goods (never trust the browser redirect alone). Unit 8 covers the controls around this.

## 7.5 Building and running an e-business

An online business needs: a **platform** (own site with a CMS or shop framework, or a marketplace seller account), a **catalogue**, a **payment gateway**, **logistics** (own riders or courier partners, with Nepal-specific issues such as incomplete street addresses and COD returns), **customer service**, **analytics** (funnel, abandoned carts) and **legal compliance** (company registration, VAT, consumer protection, the Electronic Transactions Act 2063). Typical pitfalls: underestimating delivery and returns costs, running promotions that destroy margin, and ignoring mobile-first design when most users arrive by phone.

## 7.6 Online payment cards and how a card payment is processed

Cards remain the most common electronic payment instrument worldwide. Five kinds are named in the syllabus.

| Card | How it pays | Key features |
|---|---|---|
| **Credit card** | The issuing bank lends the money; the holder repays later | Credit limit, monthly statement, interest on unpaid balance, rewards, chargeback rights |
| **Charge card** | Like credit, but the full balance is due every month | No pre-set limit in some schemes, no revolving interest, annual fee |
| **Debit card** | Money leaves the holder's bank account at once | No credit, PIN or OTP needed, limited by balance |
| **Prepaid or stored-value card** | Holder loads money first | Useful for students and gifts; no bank account needed |
| **Smart card** | Any card with an embedded microprocessor chip (EMV) | Stores keys, creates a one-time code per transaction, resists cloning, supports contactless tap |

### The four-party model

A card payment involves five roles: the **cardholder**, the **merchant**, the **issuer** (the cardholder's bank), the **acquirer** (the merchant's bank or processor) and the **card network** (Visa, Mastercard, UnionPay or a domestic switch) that connects issuers and acquirers. A **payment gateway** sits between the merchant's site and the acquirer and encrypts the card data.

```svgfig label="7.1" caption="The card payment cycle. (1) The cardholder pays on the merchant's checkout, which passes the card data to the payment gateway. (2) The gateway sends an authorisation request to the acquirer, which (3) forwards it through the card network to the issuer. (4) The issuer checks funds and fraud signals and approves or declines; the answer returns along the same path. Later, clearing and settlement move the money: the issuer pays the acquirer less the interchange fee, and the acquirer pays the merchant less its own fee."
f = Fig(580, 190)
nodes = [("Customer", 10, MINT, TEAL), ("Merchant\n+ gateway", 130, BLUE, NAVY), ("Acquirer", 250, SAND, AMBER), ("Card\nnetwork", 370, SOFT, SLATE), ("Issuer", 490, ROSE, RED)]
for n, x, fl, c in nodes:
    f.box(x, 40, 80, 56, n, fill=fl, stroke=c, size=11, bold=True, color=c, r=6)
for i in range(4):
    f.arrow([(nodes[i][1] + 80, 58), (nodes[i + 1][1], 58)], color=SLATE)
    f.arrow([(nodes[i + 1][1], 80), (nodes[i][1] + 80, 80)], color=TEAL)
f.text(290, 20, "Authorisation: request goes right, approval or decline comes back", size=11, color=NAVY, bold=True)
f.arrow([(530, 140), (50, 140)], color=AMBER)
f.text(290, 124, "Settlement: money flows back, reduced by a fee at each step", size=11, color=AMBER, bold=True)
f.text(290, 168, "Rs 10,000 order: merchant receives about Rs 9,780", size=10.5, color=SLATE, bold=True)
```

### Processing a card payment online, step by step

1. The customer chooses a card at checkout. The merchant's page hands the customer to the **gateway's hosted page** (or loads its secure form), so card numbers do not touch the merchant's server.
2. The customer enters the card number (PAN), expiry and security code and, for strong customer authentication, passes **3-D Secure**, usually a one-time password from the issuer.
3. The gateway sends an **authorisation request** to the acquirer. The acquirer passes it through the network to the issuer.
4. The issuer checks the account, the limit and its fraud rules and returns **approved** or **declined** with a reason code. The amount is put on hold.
5. The merchant sees the result, shows a receipt and ships the goods.
6. In **capture** and **clearing**, the merchant's approved transactions are sent to the acquirer in a batch, usually daily.
7. In **settlement** the money moves: the issuer pays the acquirer, which pays the merchant after deducting the **merchant discount rate (MDR)**. The cardholder is billed (credit) or debited (debit).

::: example Where does the fee go?
Illustrative rates (real rates differ by country, card type and contract). On a Rs 10,000 order the interchange fee to the issuer is 1.5 percent = Rs 150, the network fee 0.1 percent = Rs 10 and the acquirer's margin 0.6 percent = Rs 60. The merchant pays a total MDR of 2.2 percent = **Rs 220** and receives 10,000 − 220 = **Rs 9,780**.
:::

**Risks and protections.** Online card payments are *card-not-present* transactions, so fraud is a larger share. Controls: 3-D Secure, tokenisation (the real number is replaced by a token), address and security-code checks, velocity rules (too many attempts) and monitoring by the gateway. A customer may dispute a transaction, creating a **chargeback**; the merchant loses the amount and pays a fee unless it can prove delivery. Merchants must follow **PCI DSS**, the card industry's security standard: never store the security code, encrypt card data, restrict access and test regularly. Using a hosted gateway page removes most of this burden.

## 7.7 e-Micropayments, e-checks and the ACH network

### e-Micropayments

A **micropayment** is a very small online payment, from a few rupees to about Rs 500 (roughly ten US dollars). Examples are paying per news article, a song, a mobile game item, a ride unlock or a data top-up. Card fees have a fixed part, so a Rs 10 card payment would lose most of its value to fees. The solutions are **aggregation** (collect many small charges and bill once), **prepaid balances** and wallets, **carrier billing** (the charge is added to the mobile bill) and **in-app purchases** through an app store. Micropayments need very low cost per transaction, speed and simplicity, and they must still be secure.

### e-Checks and their online processing

An **electronic cheque (e-check)** is the electronic version of a paper cheque: the payer authorises the transfer of money from a bank account by giving the account details (or by a digitally signed order), and the payment is cleared between banks. It is cheaper than cards and suits recurring and high-value payments such as insurance premiums, rent and business-to-business invoices. Processing:

1. The customer selects "pay by e-check" and supplies bank and account details with authorisation.
2. The merchant (or its processor) validates the details and sends the payment instruction to its bank.
3. The bank places the item in a clearing batch. The **clearing house** sends it to the payer's bank.
4. The payer's bank checks funds and either honours or returns the item.
5. Funds are credited to the merchant after settlement, normally one or two days later.

In Nepal, NCHL runs electronic cheque clearing (ECC) between banks and the connectIPS system for direct account-to-account transfers.

### The Automated Clearing House (ACH) network

An **ACH** is an electronic network that processes bank-to-bank transfers in **batches**. It handles payroll, bill payment, government payments, subscriptions and e-checks at low cost. Two directions exist: an **ACH credit** *pushes* money from the payer's bank to the payee (salary), and an **ACH debit** *pulls* money from the payer's account with permission (utility bill). The path is: originator (company) to its bank, to the ACH operator, to the receiving bank, to the account holder. Settlement is by net position between banks, as in the netting example of section 7.4. Compared with cards, ACH is cheaper and has no interchange fee, but is slower (batch cycles) and the paying side has less protection.

## 7.8 Mobile payments, digital wallets and international payments

A **mobile payment** is a payment started, authorised or completed with a mobile device. A **digital wallet** is an app or account that stores payment credentials or value and pays from them.

| Method | How it works | Example in use |
|---|---|---|
| SMS or USSD | Payment by text or a short code on any phone | Early mobile banking, balance and top-up |
| App wallet (stored value) | The user loads money, then pays merchants and bills from the balance | eSewa, Khalti, IME Pay and bank wallets |
| QR payment | Customer scans the merchant's code (static) or the merchant scans a one-time code (dynamic) | Fonepay and NepalPay QR in shops |
| NFC tap | The phone sends a **token** to the terminal by short-range radio | Google Pay and Apple Pay in countries with contactless terminals |
| Carrier billing | The charge is added to the phone bill or deducted from airtime | Subscriptions, ringtones, small digital goods |

**Participants:** the consumer, the merchant, the **wallet or payment service provider**, the banks, the mobile network operator, the interoperability network (for example NCHL or Fonepay) and the regulator (Nepal Rastra Bank).

**Issues:** security (SIM swap, lost phones, fake apps, phishing for OTPs); **interoperability** (can a wallet pay a bank account and another wallet?); **KYC and anti-money-laundering** rules and transaction limits; fees; reliability of networks in remote areas; consumer trust and digital literacy; and dispute handling.

### International payments

Paying across borders is slower and costlier than paying at home. A bank transfer goes through **correspondent banks** over the SWIFT messaging network, each step adding a fee and a delay, and currency conversion adds a margin. Other routes are **remittance companies** (cash or account payout, widely used for money sent home by Nepali workers abroad), international **card payments** (the merchant receives foreign currency converted by the acquirer) and, where permitted, wallet links between countries. Foreign exchange limits and documentation are set by NRB, so an exporter must follow the rules for receiving payment. Cross-border QR links between national systems (for example with India's UPI) are being introduced; check the current status before quoting them.

## 7.9 Emerging payment systems: virtual currency and cryptocurrency

A **virtual currency** is a digital unit of value that is not issued by a central bank. Closed examples are game gold, airline miles and loyalty points: they can be spent only inside one ecosystem. A **cryptocurrency** is a virtual currency that uses cryptography and a **distributed ledger** (a blockchain) so that no single authority keeps the records. Bitcoin (2009, by the pseudonymous Satoshi Nakamoto) was the first; Ethereum and many others followed, and **stablecoins** try to keep a fixed value against a currency.

**How a transaction works.** The sender signs a transfer with a private key; the network broadcasts it; **miners** or **validators** collect transactions into a block, check the signatures and add the block to the chain; after enough confirmations (about 10 minutes per block for Bitcoin) the payment is final and cannot be reversed. Wallets hold keys, not coins.

| Advantages | Problems |
|---|---|
| No bank intermediary, works across borders, open all hours | Price **volatility** makes it unsuitable as a store of value for a shop |
| Low fees for large international transfers | Irreversible payments and no chargeback protection |
| Transparent public ledger | Scams, theft of keys, exchange failures |
| Programmable payments (smart contracts) | Energy use in proof-of-work systems, legal and tax uncertainty |

**Legal position in Nepal.** Nepal Rastra Bank has declared cryptocurrency dealings illegal (a notice in 2017, repeated in later directives), so a Nepali business cannot lawfully accept or promote them as payment. Students should know the technology and the regulatory risk. Some central banks are developing **central bank digital currencies (CBDC)**, a digital form of the national currency issued by the central bank; this is different from private cryptocurrency.

## 7.10 Case study: emerging trends in online payments in Nepal

The table follows the main shifts. Dates and names change quickly; treat it as a structured overview of general knowledge and verify details with current NRB and operator publications.

| Trend | What changed | Effect on e-business |
|---|---|---|
| From cash to wallets | App wallets such as eSewa and Khalti let people pay bills, top up and shop without a card | A shop can take payment without a bank card |
| Bank-to-bank transfers | connectIPS and mobile banking enable direct account payments | Lower fees than cards for larger orders |
| QR everywhere | Fonepay and NepalPay QR are accepted in shops and by street vendors | Bridges physical and online retail |
| Interoperability | Wallets, banks and QR networks connect through national switches | Customers pay from any account to any merchant |
| Regulation and licensing | The Payment and Settlement Act 2075 and NRB licences for payment system operators and providers | Safer services, compliance needed for merchants |
| Cards and chips | EMV chip cards, 3-D Secure and domestic card switches | Fewer cloned cards, safer online card use |
| Cash on delivery decline | COD is still common but wallets and QR are rising | Fewer returns and cash handling costs |

**Challenges:** limited internet and smartphone access outside cities, trust and fear of fraud, fees and limits, digital literacy, cybersecurity incidents and the need for a clear dispute process. **Opportunities:** a young population, remittance flows that can be directed to digital channels, tourism payments and integration with government services.

Questions to prepare for the exam: explain two trends and their effect on online shops; list two risks and two controls for mobile wallets; contrast a card payment with an ACH debit in cost, speed and protection.

## 7.11 Seeing e-business: funnels, unit economics and netting

An online business lives on small percentages and thin margins, and Nepal's payment system relies on netting. The plate shows the regulator's home and the funnel of a typical shop, and the figures show the unit economics and the settlement arithmetic.

```photogrid label="7.1" cols="2" ratio="1.2" caption="(a) The head office of Nepal Rastra Bank in Kathmandu. The central bank licenses payment service providers and payment system operators and supervises settlement, so every wallet and card scheme in Nepal ultimately operates under its rules. (b) The funnel of the online shop in section 7.2: of 100,000 visitors only 5,000 add to cart, 2,000 start checkout and 1,400 pay, an overall conversion of 1.40 percent."
@ photo id="bca304/nrb" cap="Nepal Rastra Bank, Kathmandu"
fit 1.2
focus 0.5 0.5
@ svg cap="Funnel of 100,000 visitors"
f = Fig(330, 275)
st = [("Visitors", 100000, 300, NAVY, BLUE), ("Add to cart", 5000, 5, TEAL, MINT), ("Checkout", 2000, 2, AMBER, SAND), ("Paid", 1400, 1, RED, ROSE)]
rows = [("Visitors  100,000", 300, BLUE, NAVY), ("Add to cart  5,000  (5%)", 220, MINT, TEAL), ("Checkout  2,000  (40%)", 150, SAND, AMBER), ("Paid  1,400  (70%)", 100, ROSE, RED)]
for i, (t, w, fl, c) in enumerate(rows):
    y = 14 + i * 56
    f.box(165 - w / 2, y, w, 40, "", fill=fl, stroke=c)
    f.text(165, y + 20, t, size=11.5, color=c, bold=True) if w >= 150 else f.text(165, y + 20, t, size=10.5, color=c, bold=True)
f.text(165, 250, "Overall conversion 1.40%", size=12, color=NAVY, bold=True)
f.text(165, 268, "Checkout 70% -> 80% adds 200 orders", size=10.5, color=SLATE, bold=True)
```

```svgfig label="7.2" caption="Unit economics of one order. Advertising of Rs 1,50,000 brought 1,400 customers, so the customer acquisition cost is 150,000 / 1,400 = Rs 107.14. An average order of Rs 2,400 at a 22 percent gross margin gives a gross profit of 2,400 x 0.22 = Rs 528 per order. After paying for acquisition Rs 528 - 107.14 = Rs 420.86 is left on the first order. A shop where the CAC exceeds the profit per order loses money on every new customer and survives only if customers return."
f = Fig(580, 150)
f.box(10, 20, 528 * 0.9, 34, "Gross profit per order  Rs 528", fill=MINT, stroke=TEAL, color=TEAL, size=11, bold=True, r=3)
f.box(10, 66, 107.14 * 0.9, 34, "", fill=ROSE, stroke=RED, r=3)
f.text(10 + 107.14 * 0.9 + 8, 83, "CAC  Rs 107.14", size=11, color=RED, bold=True, anchor="start")
f.box(10 + 107.14 * 0.9, 66, 420.86 * 0.9, 34, "Left over  Rs 420.86", fill=SAND, stroke=AMBER, color=AMBER, size=11, bold=True, r=3) if False else None
f.box(10 + 107.14 * 0.9 + 150, 66, 420.86 * 0.9 - 150, 34, "left  Rs 420.86", fill=SAND, stroke=AMBER, color=AMBER, size=11, bold=True, r=3)
f.text(290, 126, "Order value Rs 2,400 x margin 22% = Rs 528;  Rs 528 - Rs 107.14 = Rs 420.86", size=10.5, color=NAVY, bold=True)
```

```svgfig label="7.3" caption="Multilateral netting, the worked example of section 7.4. Gross obligations among four banks total Rs 970 crore. Net positions are A -30, B +80, C 0, D -50 (received minus sent). Only A pays 30 and D pays 50, both to B, so Rs 80 crore moves in settlement instead of 970: a saving of 91.8 percent. Settling pair by pair (bilateral netting) would still need Rs 190 crore of transfers. The positions always sum to zero because money is only moved, never created."
f = Fig(580, 200)
pos = {"A": (60, 100), "B": (290, 40), "C": (290, 170), "D": (520, 100)}
net = {"A": "-30 pays", "B": "+80 receives", "C": "0", "D": "-50 pays"}
for k, (x, y) in pos.items():
    f.circle(x, y, 26, fill=BLUE if k != "B" else MINT, stroke=NAVY if k != "B" else TEAL, label=k, size=13)
    f.text(x, y + 42 if k != "B" else y - 38, net[k], size=10.5, color=RED if k in "AD" else TEAL, bold=True)
f.arrow([(86, 90), (264, 46)], color=RED, label="30", lpos=(170, 56))
f.arrow([(494, 90), (316, 46)], color=RED, label="50", lpos=(410, 56))
f.text(290, 118, "Settlement: 30 + 50 = 80 crore", size=11, color=NAVY, bold=True)
f.text(290, 136, "instead of 970 crore gross (91.8% less)", size=10.5, color=SLATE, bold=True)
```

```svgfig label="7.4" caption="The path of a QR payment in a generic wallet and switch architecture. (1) The customer scans the merchant's QR code with a wallet or bank app. (2) The app sends the payment request to the payment service provider or switch. (3) The switch checks the customer's bank and the balance. (4) The customer's bank approves and debits the account. (5) The switch tells the merchant's bank, which credits the merchant. (6) Both apps show a confirmation within seconds. Final interbank settlement happens later by netting through the central bank, so the customer sees an instant payment while the banks settle in batches."
f = Fig(580, 190)
b = [("Customer\napp", 8, MINT, TEAL), ("Switch /\nPSP", 130, SAND, AMBER), ("Customer's\nbank", 252, BLUE, NAVY), ("Merchant's\nbank", 374, BLUE, NAVY), ("Merchant", 496, MINT, TEAL)]
for t, x, fl, c in b:
    f.box(x, 40, 76, 50, t, fill=fl, stroke=c, size=10, bold=True)
f.arrow([(84, 55), (130, 55)], color=SLATE); f.text(107, 44, "1-2", size=9.5, color=SLATE, bold=True)
f.arrow([(206, 55), (252, 55)], color=SLATE); f.text(229, 44, "3", size=9.5, color=SLATE, bold=True)
f.arrow([(252, 78), (206, 78)], color=TEAL); f.text(229, 100, "4", size=9.5, color=TEAL, bold=True)
f.arrow([(206, 66), (374, 30), (450, 30)], color=SLATE) if False else None
f.arrow([(168, 40), (168, 18), (412, 18), (412, 40)], color=SLATE); f.text(290, 12, "5 credit instruction", size=9.5, color=SLATE, bold=True)
f.arrow([(450, 65), (496, 65)], color=SLATE)
f.box(130, 130, 320, 40, "Later: netted settlement through the central bank", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(535, 110, "6 confirmation", size=9.5, color=TEAL, bold=True)
```

```photogrid label="7.4" cols="2" ratio="1.27" caption="A payment gateway must reject mistyped card numbers instantly, without sending them to the bank. (a) A card terminal at a shop counter reads the number from the chip or stripe. (b) The Luhn algorithm, used on bank card numbers, doubles every second digit from the right, subtracts 9 from any result above 9, and adds all digits. The test card 4111 1111 1111 1111 gives a sum of 30, a multiple of 10, so it passes, while changing only the last digit gives 31 and fails. Brute force over all 144 single-digit mistakes shows that every one is caught. The check protects against typing errors, not against fraud, so authentication and OTP are still required."
@ photo id="bca304/cardterm" cap="A card payment terminal (point of sale)"
fit 1.27
focus 0.5 0.5
@ svg cap="Luhn check on a 16-digit card number"
def luhn_total(num):
    s = 0
    for k, ch in enumerate(reversed(num)):
        d = int(ch)
        if k % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return s
good = "4111111111111111"
bad = "4111111111111112"
tg, tb = luhn_total(good), luhn_total(bad)
assert tg % 10 == 0 and tb % 10 != 0
caught = 0; tried = 0
for pos in range(16):
    for d in "0123456789":
        if d != good[pos]:
            tried += 1
            n = good[:pos] + d + good[pos + 1:]
            caught += luhn_total(n) % 10 != 0
assert caught == tried == 144
f = Fig(300, 236)
f.text(150, 14, "Luhn check digit: 4111 1111 1111 1111", size=10.5, color=NAVY, bold=True)
dbl = []
for i, ch in enumerate(good):
    k = 15 - i
    d = int(ch) * (2 if k % 2 == 1 else 1)
    dbl.append(d - 9 if d > 9 else d)
f.text(6, 34, "digits", size=9, anchor="start")
f.text(6, 74, "after Luhn", size=9, anchor="start")
for i, ch in enumerate(good):
    x = 14 + i * 17
    f.box(x, 40, 15, 20, ch, fill=BLUE, stroke=NAVY, size=10, bold=True, r=2)
    hl = (15 - i) % 2 == 1
    f.box(x, 80, 15, 20, str(dbl[i]), fill=("#fee2e2" if hl else SOFT), stroke=(RED if hl else SLATE), color=(RED if hl else SLATE), size=10, bold=True, r=2)
f.text(150, 118, "every 2nd digit from the right is doubled", size=9.5, color=RED)
f.text(150, 140, "sum = %d, and %d mod 10 = 0: accepted" % (tg, tg), size=10.5, color=TEAL, bold=True)
f.text(150, 160, "change last digit to 2: sum = %d, rejected" % tb, size=10.5, color=RED, bold=True)
f.text(150, 188, "all %d single-digit errors detected" % tried, size=10.5, color=NAVY, bold=True)
f.text(150, 204, "(16 positions x 9 wrong digits)", size=9.5)
f.text(150, 222, "a typing slip is caught before the bank is called", size=9.5, color=SLATE)
facts = dict(tg=tg, tb=tb, tried=tried)
```

### 7.11.1 Eight advantages of e-business for Nepali firms

1. **Wider market.** An online shop is open to customers across Nepal and abroad, not only to those who pass the building. A Bhaktapur handicraft seller can sell to tourists who returned home. The market grows without new shops.
2. **Lower operating cost.** There is no need for prime shop space or many counter staff, and orders are processed by software. A small firm can start with a laptop and a phone. Savings can be passed on as lower prices.
3. **Open all day.** Customers order at midnight or on a holiday. Migrant workers abroad send gifts and recharge at their own time zone. Sales no longer stop when the shutter closes.
4. **Faster transactions.** Payment by wallet, ConnectIPS or QR completes in seconds and creates a digital record. Cash handling, queues and counting errors fall. A utility company that accepts online payment collects bills faster.
5. **Better customer data.** Each visit and order produces data on what people want. The shop can personalise offers and measure funnel steps as in Figure 7.2. Decisions are based on evidence, not guesses.
6. **Direct relationship.** Producers can sell directly to buyers, cutting layers of middlemen. A farmer cooperative can list vegetables and take orders from restaurants. The producer earns more and the buyer pays less.
7. **Easy scaling.** A system built for 100 orders a day can be upgraded to handle 10,000 with more servers. Cloud services are rented by use. A festival-season rush does not require permanent staff.
8. **Better service and tracking.** Customers see order status, receipts and delivery tracking, and can complain by chat. Fast replies create trust. Reliable service is the main reason people return to an online shop.

## Chapter summary

- e-Business covers all online business processes; e-commerce is online trade; models include B2C, B2B, C2C, G2C and m-commerce with revenue by margin, commission, subscription or advertising.
- Funnel metrics, CAC and LTV tell whether growth is profitable; sanity-check the assumptions.
- A payment passes through authorisation, clearing and settlement; NRB licenses PSOs and PSPs under the Payment and Settlement Act 2075.
- NCHL (NPI, ConnectIPS), Fonepay (switch and QR), wallets and banks form the retail payment network; multilateral netting reduces settlement transfers.
- Always verify payment status server-side with the gateway before fulfilment.
- Cards (credit, charge, debit, prepaid, smart) are processed through issuer, acquirer and network; the merchant receives the amount less interchange, network and acquirer fees, and 3-D Secure, tokenisation and PCI DSS reduce card fraud.
- Micropayments need aggregation or wallets; e-checks and the ACH network clear bank-to-bank in cheap batches; wallets, QR and NFC dominate mobile payment, with SIM-swap and interoperability as the main issues.
- Cryptocurrency is volatile, irreversible and not lawful as payment in Nepal; Nepal's payment trends are wallets, QR, bank transfers and interoperability.

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
11. Differentiate credit, charge and debit cards. What makes a smart card more secure?
12. A Rs 25,000 card order carries interchange 1.5 percent, network 0.1 percent and acquirer 0.6 percent. What does the merchant receive?
13. Differentiate an ACH credit from an ACH debit with one example each.
14. Why are micropayments hard to handle by card? Give two solutions.
15. Compare virtual currency and cryptocurrency and state the legal position in Nepal.

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
**11.** Credit: the bank lends, the holder repays later with interest. Charge: full balance due monthly. Debit: pays at once from the account. A smart card holds a chip that creates a one-time code for each transaction and resists cloning.
**12.** MDR = 2.2 percent; fee = 25,000 × 0.022 = Rs 550; merchant receives **Rs 24,450**.
**13.** Credit pushes money to the payee (salary payment). Debit pulls money from the payer's account with permission (monthly utility bill).
**14.** The fixed part of the card fee is large relative to a tiny amount. Solutions: aggregate many small charges into one bill; use prepaid wallets or carrier billing.
**15.** Virtual currency is any digital unit not issued by a central bank (game coins); cryptocurrency uses cryptography and a blockchain. NRB has declared crypto dealings illegal, so Nepali merchants cannot accept it.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). An online shop gets 100,000 visitors; 5 percent add to cart, 40 percent of those start checkout and 70 percent of those pay. Advertising cost is Rs 1,50,000 and the average order is Rs 2,400 with 22 percent gross margin. Find conversion, CAC and profit per order.**

*Introduction.* An online business is managed with funnel and unit-economics measures (section 7.2, Figure 7.2).

1. **Funnel.** 100,000 x 0.05 = 5,000 add to cart; 5,000 x 0.40 = 2,000 start checkout; 2,000 x 0.70 = **1,400** orders.
2. **Conversion rate.** Orders / visitors = 1,400 / 100,000 = **1.40 percent**.
3. **CAC.** Marketing spend / new customers = 1,50,000 / 1,400 = **Rs 107.14**.
4. **Gross profit per order.** 2,400 x 0.22 = **Rs 528**.
5. **First-order result.** 528 - 107.14 = **Rs 420.86** left after acquisition.
6. **Improvement.** Raising checkout completion from 70 to 80 percent gives 2,000 x 0.80 = 1,600 orders, 200 more, without extra advertising.

| Stage | Users | Step rate |
|---|---|---|
| Visitors | 100,000 | |
| Add to cart | 5,000 | 5% |
| Checkout | 2,000 | 40% |
| Paid | 1,400 | 70% |

*Conclusion.* The shop makes a positive profit on the first order; improving the weakest funnel step is the cheapest growth.

**Q2 (5 marks). Explain multilateral netting with the four-bank example (net positions A -30, B +80, C 0, D -50) and state its advantage.**

*Introduction.* Banks owe each other many payments during a day; netting reduces them to one net settlement per bank (section 7.4, Figure 7.3).

1. **Gross obligations.** Each bank sends payments to the others; in the example the total is Rs 970 crore.
2. **Net position.** For each bank, received minus sent: A 230 - 260 = -30; B 320 - 240 = +80; C 220 - 220 = 0; D 200 - 250 = -50.
3. **Check.** -30 + 80 + 0 - 50 = 0, because money is moved and not created.
4. **Settlement.** Banks with negative positions pay the central bank or settlement agent: A pays 30 and D pays 50; B receives 80.
5. **Saving.** Only Rs 80 crore moves instead of 970, a saving of 91.8 percent; bilateral netting would still need 190 crore.
6. **Risk.** The liquidity needed is much smaller, but a bank that cannot pay its net amount affects all, so limits and collateral are used.

*Conclusion.* Multilateral netting through a central switch minimises transfers and liquidity and is the basis of retail payment clearing.

**Q3 (10 marks). Define e-business and e-commerce. Explain the business models, the payment system architecture in Nepal and the security and legal issues of e-commerce.**

*Introduction.* E-business is the use of the Internet and information systems to run all business activities, such as buying, selling, producing and serving customers. E-commerce is the part that deals with buying and selling online. For Nepal the topic joins technology, payment regulation and law (sections 5.1 to 5.5, Figures 5.1 to 5.3).

1. **E-business versus e-commerce.** E-commerce is the transaction part (online shop); e-business also covers internal processes (ERP), supply chain and customer service.
2. **Business models.** B2C (Daraz to consumers), B2B (wholesaler to retailer), C2C (marketplace between individuals), G2C (government to citizens, as in the Nagarik App) and G2B (tax and customs portals).
3. **Revenue models.** Sales margin, commission, advertising, subscription and transaction fees.
4. **Payment methods.** Cash on delivery, cards, wallets, bank transfer through ConnectIPS and QR payments.
5. **Architecture.** The customer's app, a payment service provider or switch, the banks and the central bank. The switch routes and authorises instantly; the final settlement is netted and done through the central bank.
6. **Regulation.** Nepal Rastra Bank licenses payment service providers and operators under the Payment and Settlement Act, 2075 (2019); the Electronic Transactions Act, 2063 (2008) gives legal validity to electronic records and signatures.
7. **Security.** HTTPS with TLS, strong authentication (MFA), tokenisation of card data, fraud monitoring and secure storage of passwords as salted slow hashes.
8. **Challenges.** Trust, last-mile delivery, address problems, low digital literacy, internet access and refund handling.

| Model | Seller | Buyer | Nepali example |
|---|---|---|---|
| B2C | Business | Consumer | Online shop |
| B2B | Business | Business | Wholesale portal |
| C2C | Consumer | Consumer | Classified marketplace |
| G2C | Government | Citizen | Nagarik App |

*Conclusion.* E-business extends the firm across the Internet. It succeeds when a sound business model, an efficient payment path, regulation and security work together, so that customers trust paying online.

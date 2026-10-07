---
subject: Accountancy
grade: 10
unit: 2
title: Bank, Insurance and Financial Institutions (बैंक, बीमा तथा वित्तीय संस्थाहरू)
hours: 10
area: Financial Institutions
---

Money does not sit still. Households save, businesses borrow, the government collects and spends, and somebody has to move money from the people who have a surplus to the people who need it. That somebody is the **financial institution**. This unit introduces the whole family — the central bank at the top, commercial banks, development banks, finance companies and microfinance institutions below it, and the non-bank members such as insurance companies, provident funds, the Citizen Investment Trust and financial cooperatives beside it. It then explains the instruments a bank uses (cheque, draft, card) and finishes with the three markets in which money and securities are traded.

::: key What the examiner tests here
The very commonest Group A questions in the whole paper come from this unit: "When was Nepal Rastra Bank established?", "What is a central bank?", "Write any two functions of a commercial bank", "What is insurance?", "What is a money market?". Group B regularly asks for five functions of a financial institution or of a central bank, and Group C has asked "Introduce the financial institution and describe any five of its functions." Learn the functions as lists of five, with one line of explanation for each.
:::

## 2.1 Financial institutions: meaning and types

A **financial institution** (वित्तीय संस्था) is an institution whose main business is to collect money from those who have it and to lend or invest it in those who need it, and to provide the financial services — payments, deposits, insurance, foreign exchange — that a modern economy needs.

Financial institutions exist because of three facts about money. First, savers and borrowers are **different people** who rarely meet. Second, they want **different maturities** — a household wants to be able to withdraw its savings at a month's notice, while a factory wants a loan for ten years. Third, there is **risk**: the saver does not know whether the borrower will repay. A financial institution stands in the middle, pooling small savings into large loans, matching short maturity with long, and carrying a risk that a single saver could not.

**Types.** Financial institutions are divided into two great families.

```figure caption="The family of financial institutions in Nepal. The institutions inside the outer box create credit; those outside it move and protect money without creating deposits."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.3))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.add_patch(FancyBboxPatch((0.2,3.6),9.6,6.2,boxstyle="round,pad=0.1",fc="#f7f9fc",ec=ACCENT,lw=1.3))
ax.text(5.0,9.25,"BANKING FINANCIAL INSTITUTIONS",ha='center',fontsize=8,color=ACCENT,weight='bold')
ax.add_patch(FancyBboxPatch((3.4,7.5),3.2,1.15,boxstyle="round,pad=0.06",fc="#eaf1ff",ec=ACCENT,lw=1.1))
ax.text(5.0,8.08,"Central bank\n(NRB)",ha='center',va='center',fontsize=7.2,color=INK)
for x,t in ((0.8,"Commercial\nbanks"),(3.5,"Development\nbanks"),(6.2,"Finance\ncompanies"),(8.6,"Micro-\nfinance")):
    w = 2.1 if x<8 else 1.3
    ax.add_patch(FancyBboxPatch((x,5.2),w,1.2,boxstyle="round,pad=0.05",fc="#eef3ff",ec=MUTED,lw=1.0))
    ax.text(x+w/2,5.8,t,ha='center',va='center',fontsize=6.6,color=INK)
ax.add_patch(FancyBboxPatch((0.2,0.4),9.6,2.6,boxstyle="round,pad=0.1",fc="#fdf3f3",ec=SERIES[1],lw=1.3))
ax.text(5.0,2.55,"NON-BANKING FINANCIAL INSTITUTIONS",ha='center',fontsize=8,color=SERIES[1],weight='bold')
ax.text(5.0,1.45,"Insurance companies · Provident fund · Citizen Investment Trust\nMutual funds · Financial cooperatives · Hire-purchase companies",
        ha='center',va='center',fontsize=6.8,color=INK)
```

**Banking institutions** accept deposits from the public and are allowed to create credit: the central bank, commercial banks, development banks, finance companies and microfinance institutions. **Non-banking financial institutions** also collect money from the public, but they do not create deposits and cannot issue cheques against them: insurance companies, the Employees' Provident Fund, the Citizen Investment Trust, mutual funds and financial cooperatives.

## 2.2 Banking financial institutions

A **bank** is a financial institution that accepts deposits from the public, lends money, and provides payment services. Its special power is **credit creation**: when it lends, it does not hand over notes from a vault — it credits the borrower's account, and that new deposit becomes money in circulation.

A bank earns its income from the **spread** — the difference between the interest it pays on deposits and the interest it charges on loans — and from fees and commissions on the services it renders. A bank must always keep a part of its deposits as a **reserve** so that depositors who want cash can be paid. Nepal Rastra Bank fixes the cash reserve ratio and the statutory liquidity ratio for banks in Nepal.

## 2.3 Central bank: introduction and functions

A **central bank** is the apex financial institution of a country. It does not deal with the general public; it deals with the government and with the other banks. Its job is to keep the value of the currency stable and the financial system sound. In Nepal the central bank is **Nepal Rastra Bank (NRB)**, established on **26 April 1956 A.D. (13 Baisakh 2013 B.S.)** under the Nepal Rastra Bank Act. Its head office is in Baluwatar, Kathmandu, and it works through its provincial offices.

```photo id="acc10/nrb-pokhara" caption="The Nepal Rastra Bank office in Pokhara. NRB is the only institution in Nepal that may issue currency notes and coins." width="80"
```

**Functions of a central bank.**

1. **Currency issue.** It alone has the right to issue notes and coins. This gives it control over the supply of money in the country.
2. **Banker to the government.** It keeps the accounts of the government, receives revenue, makes payments on the government's behalf, and manages public debt by selling treasury bills and bonds.
3. **Banker's bank.** Every commercial bank keeps an account with the central bank. It settles the inter-bank claims of the banks among themselves and holds their reserves.
4. **Lender of last resort.** When a sound bank is temporarily short of cash and no other bank will lend to it, the central bank lends. This prevents a small shortage from becoming a panic.
5. **Monetary policy.** It controls the supply of money and the cost of credit — through the bank rate, the cash reserve ratio, open market operations and moral suasion — in order to control inflation and support growth.
6. **Foreign exchange management.** It holds the country's foreign exchange reserves, fixes and defends the exchange rate policy, and issues licences to buy and sell foreign currency.
7. **Regulation and supervision.** It licenses banks and financial institutions, inspects them, and takes action if they are unsound, so that depositors' money is safe.
8. **Clearing house.** It runs the clearing system through which cheques drawn on different banks are settled.
9. **Promotion of the financial sector.** It encourages banking in areas and sectors that private banks neglect, for example through directed lending to agriculture and small enterprises.

```photo id="acc10/nrb-janakpur" caption="A Nepal Rastra Bank branch. Provincial offices carry out currency distribution, government banking and supervision away from Kathmandu." width="80"
```

::: memory The central bank in one sentence
The central bank is the **government's bank, the bankers' bank, the only note issuer, the lender of last resort, the supervisor of banks and the manager of the country's foreign exchange**.
:::

## 2.4 Commercial banks: introduction and functions

A **commercial bank** is a financial institution that accepts deposits from the public and lends money to trade, industry, agriculture and individuals with the object of earning profit. **Nepal Bank Limited**, established in **1994 B.S. (1937 A.D.)**, was the first bank of Nepal; **Rastriya Banijya Bank** (2022 B.S.) was the first fully government-owned commercial bank. Today dozens of commercial banks operate through thousands of branches across the country.

**Functions.**

**Primary functions.**

1. **Accepting deposits** — savings deposits, current (demand) deposits, fixed (time) deposits and recurring deposits. The current account is the only one on which a cheque may be drawn.
2. **Advancing loans and advances** — cash credit, overdraft, demand loan, term loan, bill discounting and hire purchase. Interest is the price of the loan.
3. **Credit creation** — by lending, a bank turns one deposit into several deposits across the banking system, subject to the reserve ratio.

**Secondary (agency) functions.** Collecting cheques, bills and drafts on behalf of customers; making payments such as standing instructions, insurance premiums and utility bills; buying and selling securities on the customer's instruction; acting as a trustee or executor; and keeping valuables in safe custody.

**General utility functions.**

4. **Payment services** — issuing cheques, drafts, pay orders and traveller's cheques and running ATMs, debit and credit cards, mobile banking and internet banking.
5. **Remittance** — transferring money from one place to another, including foreign remittance from Nepali workers abroad.
6. **Foreign exchange business** — buying and selling foreign currency, issuing letters of credit for imports, and handling export documents.
7. **Advisory and agency services** — advising on investment, helping small businesses with project reports, and acting as a referee when a customer gives a guarantee.
8. **Social banking** — under NRB's directives, banks must lend a fixed share of their loans to agriculture, energy, tourism, small and medium enterprises and deprived sectors.

::: example How much money can a bank create?
**Problem.** A commercial bank receives a new deposit of Rs. 50,000. The cash reserve ratio fixed by Nepal Rastra Bank is 10 per cent, and the bank lends out everything it is allowed to. Find (a) the amount of the first loan, (b) the total deposits the banking system can create from this deposit, and (c) the credit multiplier.

**Solution.**
Step 1 — The bank must keep 10 % of Rs. 50,000 as reserve: $0.10 \times 50{,}000 = Rs.\ 5{,}000$.
Step 2 — It may lend the rest: $50{,}000 - 5{,}000 = Rs.\ 45{,}000$. That is the first loan, and once it is spent and re-deposited it becomes a new deposit.
Step 3 — The same process repeats with each new deposit, so the total deposits are the original deposit times the multiplier.
Step 4 — Credit multiplier $= \frac{1}{\text{cash reserve ratio}} = \frac{1}{0.10} = 10$.
Step 5 — Total deposits $= 50{,}000 \times 10 = Rs.\ 5{,}00{,}000$.

**Answer.** First loan Rs. 45,000; total deposits Rs. 5,00,000; multiplier 10.
**What it means.** One rupee of new reserve supports ten rupees of deposits. If NRB raised the reserve ratio to 12.5 per cent, the same Rs. 50,000 would support only Rs. 4,00,000 — which is exactly how a central bank squeezes credit out of the system.
:::

## 2.5 Development banks, finance companies and microfinance institutions

Not every customer a factory, a shop and a street vendor wants the same kind of bank. Nepal therefore licenses four classes of institution, each with its own permitted business.

| Institution | Main business | Typical customer |
|---|---|---|
| Commercial bank | All banking business; demand deposits and cheques; foreign exchange | Firms, government, salaried people, all sectors |
| Development bank | Medium and long-term credit for industry, agriculture, infrastructure and tourism | Projects and productive enterprises |
| Finance company | Hire purchase, lease, housing and consumer credit; fixed deposits | Households buying vehicles, appliances, houses |
| Microfinance institution | Small loans to poor households, often to groups; compulsory small savings | Low-income families, women's groups, rural entrepreneurs |

**Development banks** were created to fill the gap left by commercial banks, which prefer short-term, low-risk lending. Development banks supply the *term finance* a project needs and often provide technical help as well. The Agricultural Development Bank (2024 B.S.) is the oldest example.

**Finance companies** lend against the security of the asset being bought and are important in vehicle and housing finance. They may accept fixed deposits but not current deposits, and so they cannot offer a cheque account.

**Microfinance institutions** lend very small amounts without the usual collateral. The technique is **group lending**: the members of a group guarantee one another's loans, so the bank's risk is spread over people who know each other, and repayment rates stay high. Microfinance is how banking reaches the person who has never been inside a bank's door.

## 2.6 Non-banking financial institutions; insurance

**Non-banking financial institutions (गैरबैंकिङ वित्तीय संस्था)** are institutions that collect money from the public and provide financial services, but do not accept demand deposits and cannot create credit. The main ones in Nepal are insurance companies, the Employees' Provident Fund, the Citizen Investment Trust, mutual funds, deposit-and-credit guarantee institutions and hire-purchase companies.

**Insurance** is a contract in which one party (the insurer) agrees, in return for a payment called the **premium**, to pay a sum of money to the other party (the insured) if a stated event happens — a fire, an accident, a death, a loss of goods in transit.

Insurance works on the principle of **pooling of risk**. Many people each pay a small premium into a common fund; the few who actually suffer a loss are paid from that fund. So the loss of an unlucky individual is spread over the whole group. For this to work, three conditions must hold: the risk must be **shared among many** similar exposures, the loss must be **capable of being estimated** in money, and the insured must have an **insurable interest** — they must gain by the safety and lose by the destruction of the thing insured.

**Kinds of insurance.** *Life insurance* insures a human life; the event insured is certain (death) but its time is not, so a life policy combines protection with saving. Its forms include whole-life, endowment, money-back and term policies. *Non-life (general) insurance* insures property and liability: fire, marine, motor, health, accident, crop and livestock insurance. In Nepal, **Beema Samiti (the Insurance Board)** regulates insurance, and the **Rastriya Beema Sansthan** and many private companies are the insurers.

```photo id="acc10/insurance-policy" caption="An insurance policy document. The policy states the insurer, the insured, the risk covered, the period and the premium — the five things you must always check before signing." width="66"
```

::: example Is there an insurable interest?
**Problem.** Decide, giving a reason, whether each of the following can take out a valid insurance policy: (a) a shopkeeper insuring his own stock against fire; (b) a man insuring his neighbour's house against fire; (c) a bank insuring the building it has lent money against; (d) a trader insuring a consignment of goods he has already sold and delivered.

**Solution.**
Step 1 — State the test. Insurance requires an **insurable interest**: the person must gain by the safety of the thing insured and lose by its destruction.
Step 2 — Apply the test to each.
(a) The shopkeeper owns the stock, so he loses if it burns — **valid**.
(b) The neighbour loses nothing if the house burns — **not valid**; this would be a wager, not insurance.
(c) The bank has lent money on the building, so its security is at risk — **valid**, to the extent of its interest.
(d) The goods are already sold and delivered; the trader loses nothing — **not valid**.

**Answer.** (a) valid, (b) invalid, (c) valid, (d) invalid.
**What it means.** Insurance restores a loss, it never creates a profit. That is why the insured can never recover more than the actual loss — the principle of indemnity.
:::

## 2.7 Financial cooperatives and banking instruments

A **financial cooperative** (वित्तीय सहकारी संस्था) is a member-owned institution that collects savings from its members and lends to them. Its members are at once its owners and its customers, and any surplus is returned to members rather than paid to outside shareholders. Cooperatives reach villages and occupational groups that banks find expensive to serve, but because they are many and small, supervision is a real problem — which is why Nepal now regulates them under the Cooperative Act and the local levels.

**Banking instruments (बैंकिङ उपकरणहरू)** are the documents and devices through which a bank moves money and gives its customer access to it.

| Instrument | What it is | Where it is used |
|---|---|---|
| Cheque | A written order on a bank to pay a stated sum from the drawer's account to the payee | Everyday payments; only against a current account |
| Bank draft / demand draft | The bank's own order to pay, sold to the customer for the amount plus commission | Payments to a person or place where the payer has no account |
| Pay order | A bank's undertaking to pay a fixed amount to a named person on presentation | Fees, taxes, tenders, where a personal cheque is not accepted |
| Traveller's cheque | A pre-printed instrument signed twice, for carrying money safely abroad | Foreign travel (now largely replaced by cards) |
| Letter of credit | A bank's promise to pay an exporter when the shipping documents are presented | Import and export trade |
| Debit card / ATM card | A card that authorises the bank to debit the customer's own account | Cash withdrawal and purchases |
| Credit card | A card on which the holder borrows from the issuing bank up to a limit | Purchases, with interest if not paid by the due date |
| Mobile and internet banking | Payment instructions given through a phone or a website | Bills, transfers, balance enquiry |

**Kinds of cheque.** An **open (bearer) cheque** is one that the bank will pay in cash across the counter, either to the person named or to anyone who presents it if it says "or bearer". An **order cheque** is payable only to the payee, who must be identified. A **crossed cheque** carries two parallel lines across its face and must be paid into a bank account, never in cash; crossing is therefore a safety device, and the crossing may be *general* (any bank) or *special* ("account payee" or a named bank only).

```photo id="acc10/cheque" caption="A cheque form. The drawer's name and account, the payee, the amount in words and figures, the date and the signature — a cheque without any one of these is returned unpaid." width="82"
```

## 2.8 Remittance; money market, capital market and commodity market

**Remittance (विप्रेषण)** is money sent by a person working in one place to a person in another, usually across a border. For Nepal it is not a small matter: a very large share of national income comes from the money that migrant workers send home. That money supports household consumption, education, health and house building, and it is one of the biggest sources of foreign exchange for the country. Remittance reaches Nepal through banks, through licensed remittance companies and through informal channels called *hundi*. The formal channels are safer, cheaper and traceable; hundi is illegal because it escapes the country's foreign-exchange records, but it survives because it is fast and, in remote places, the only channel.

A **market** is a place, physical or electronic, where buyers and sellers meet. The financial world has three markets, and the difference between them lies in *what* is traded and *how long* it lasts.

| Market | What is traded | Maturity | Institutions in Nepal |
|---|---|---|---|
| Money market | Short-term funds and securities — treasury bills, inter-bank (call) money, commercial bills, certificates of deposit | Up to one year | Nepal Rastra Bank, commercial banks, finance companies |
| Capital market | Long-term securities — ordinary shares, preference shares, debentures, government bonds | More than one year | Nepal Stock Exchange, Securities Board of Nepal, merchant banks, mutual funds |
| Commodity market | Actual goods — gold, silver, petroleum, agricultural produce | Depends on the commodity | Bullion dealers, commodity exchanges, agricultural markets |

The **money market** is the market of the *banks themselves*: when a bank has surplus cash for a day or a week, it lends it to another bank that is short. The **capital market** is where firms raise the long-term capital they need to build factories, and where savers put their savings into shares and debentures; in Nepal it is regulated by the **Securities Board of Nepal (SEBON)** and traded on the **Nepal Stock Exchange (NEPSE)**. The **commodity market** deals in the goods themselves, and in Nepal it is dominated by gold and silver trading and by agricultural produce.

::: example Which market, and how much does the family get?
**Problem.** (a) A commercial bank has Rs. 2 crore of surplus cash that it can lend for seven days. In which market will it lend? (b) A hydro company needs Rs. 5 crore for ten years to build a plant. From which market will it raise the money? (c) A migrant worker in Qatar sends Rs. 1,20,000 home. The bank charges a service fee of Rs. 500 and the exchange rate is Rs. 160 to one riyal. How many riyals did he send?

**Solution.**
Step 1 — (a) Seven days is under one year, so this is a **money market** transaction — an inter-bank (call money) loan.
Step 2 — (b) Ten years is over one year, so the company raises it from the **capital market** — shares, debentures or a long-term loan.
Step 3 — (c) The amount the family receives plus the fee is what was sent in rupees: $1{,}20{,}000 + 500 = Rs.\ 1{,}20{,}500$.
Step 4 — Convert at the given rate: $1{,}20{,}500 \div 160 = 753.125$ riyals.

**Answer.** (a) money market; (b) capital market; (c) 753.125 riyals.
**What it means.** Maturity decides the market; and every remittance has a price — the service fee and the exchange rate together decide what actually reaches the family.
:::

::: caution The two mistakes in this unit
First, students write "commercial bank" when the question asks for the **central bank**, or list "accepting deposits" as a function of the central bank — the central bank does not accept deposits from the public. Second, the words *money market* and *capital market* are used as if they were interchangeable. The test is **maturity**: up to one year is the money market, more than one year is the capital market.
:::

## Chapter summary

- A **financial institution** collects money from savers and lends or invests it for borrowers, matching different maturities and carrying risk. It is either **banking** (central bank, commercial banks, development banks, finance companies, microfinance institutions) or **non-banking** (insurance, provident fund, CIT, mutual funds, cooperatives).
- A **bank** accepts deposits, lends, and provides payment services, and it **creates credit** when it lends. Its income is the spread between deposit and lending rates plus fees.
- A **central bank** is the apex institution. **Nepal Rastra Bank** was established on 26 April 1956 A.D. (2013 B.S.).
- The central bank **issues currency, acts as banker to the government and to the banks, is the lender of last resort, makes monetary policy, manages foreign exchange, supervises the banks and financial institutions, runs the clearing house** and promotes the financial sector.
- A **commercial bank's** primary functions are accepting deposits (savings, current, fixed, recurring), advancing loans (cash credit, overdraft, demand loan, term loan, bill discounting) and credit creation. Its agency and general utility functions include collection and payment, safe custody, drafts and pay orders, cards, mobile banking, remittance and foreign exchange.
- **Development banks** give medium and long-term project finance; **finance companies** do hire purchase, lease, housing and consumer credit; **microfinance institutions** lend small amounts to groups of poor households.
- **Insurance** is a contract under which the insurer pays on a stated event in return for a premium. It works by **pooling risk**. Life insurance covers human life; non-life covers fire, marine, motor, health, accident, crop and livestock. **Beema Samiti** is the regulator.
- A **financial cooperative** is member-owned and lends to its members; **banking instruments** are the cheque, draft, pay order, traveller's cheque, letter of credit, debit card, credit card and mobile/internet banking.
- A **cheque** may be open (bearer), order or **crossed**; crossing means it can only be credited to an account and is the ordinary safety device.
- **Remittance** is money sent home by migrant workers; it is one of Nepal's largest sources of foreign exchange. Formal channels are safer and legal; *hundi* is illegal.
- The **money market** trades funds and securities of up to one year (treasury bills, call money); the **capital market** trades long-term securities (shares, debentures, bonds) on NEPSE under SEBON; the **commodity market** trades goods such as gold, silver and agricultural produce.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is a financial institution? <span class="marks">[1]</span>
2. When was Nepal Rastra Bank established? <span class="marks">[1]</span>
3. Write any two functions of a central bank. <span class="marks">[1]</span>
4. Name the first bank of Nepal and the year it was established. <span class="marks">[1]</span>
5. What is credit creation? <span class="marks">[1]</span>
6. Write any two functions of a commercial bank. <span class="marks">[1]</span>
7. What is a development bank? <span class="marks">[1]</span>
8. What is insurance? <span class="marks">[1]</span>
9. Write any two kinds of non-life insurance. <span class="marks">[1]</span>
10. What is meant by crossing a cheque? <span class="marks">[1]</span>
11. Distinguish between the money market and the capital market in one line. <span class="marks">[1]</span>

::: note Answers to Group A
**1.** A financial institution is an institution whose main business is to collect money from savers and lend or invest it for those who need it, providing financial services such as deposits, loans, payments, insurance and foreign exchange.
**2.** 26 April 1956 A.D. (13 Baisakh 2013 B.S.).
**3.** Any two of: issuing currency, banker to the government, banker's bank, lender of last resort, monetary policy, foreign exchange management, regulation and supervision of banks, clearing house, promoting the financial sector.
**4.** Nepal Bank Limited, 1994 B.S. (1937 A.D.).
**5.** Credit creation is the power of a bank to expand the money supply by lending: a loan is credited to the borrower's account and becomes a new deposit, which supports further lending.
**6.** Any two of: accepting deposits, advancing loans, credit creation, collecting and paying on the customer's behalf, issuing drafts and pay orders, card and mobile banking, remittance, foreign exchange business.
**7.** A development bank is a banking institution that provides medium and long-term credit for the development of industry, agriculture, infrastructure and tourism, filling the gap left by the short-term lending of commercial banks.
**8.** Insurance is a contract in which the insurer, in return for a premium, agrees to pay a stated sum to the insured if a stated event (fire, accident, death, loss of goods) happens.
**9.** Any two of: fire, marine, motor, health, accident, crop and livestock insurance.
**10.** Crossing is drawing two parallel lines across the face of a cheque, which directs the bank to pay it only into a bank account and never in cash.
**11.** The money market deals in short-term funds and securities of up to one year; the capital market deals in long-term securities of more than one year.
:::

**Group B — Short answer (5 marks each)**

1. Introduce the financial institutions of Nepal and describe any five functions of them. <span class="marks">[5]</span>
2. What is a central bank? Explain any five functions of a central bank. <span class="marks">[5]</span>
3. Explain any five functions of a commercial bank. <span class="marks">[5]</span>
4. Distinguish between banking and non-banking financial institutions with suitable examples. <span class="marks">[5]</span>
5. What is insurance? Explain the principle on which insurance works and describe any three kinds of insurance. <span class="marks">[5]</span>
6. Describe any five banking instruments used in Nepal. <span class="marks">[5]</span>
7. What is remittance? Explain its importance for the economy of Nepal. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Financial institutions are institutions that collect savings and lend or invest them, and provide financial services. Five functions: (i) *mobilising savings* — collecting small savings into large funds; (ii) *lending* — supplying working and fixed capital to trade and industry; (iii) *payment services* — cheques, drafts, cards, electronic transfer; (iv) *maturity transformation* — accepting short-term deposits and making long-term loans; (v) *risk bearing and insurance* — carrying default risk and pooling the risk of loss. (Also acceptable: foreign exchange, remittance, credit creation, financial advice, support to the government.)
**2.** A central bank is the apex financial institution of a country, dealing with the government and the banks rather than the public; in Nepal, Nepal Rastra Bank (26 April 1956 A.D., 2013 B.S.). Five functions: currency issue; banker to the government; banker's bank and clearing house; lender of last resort; monetary policy. (Also foreign exchange management, supervision of banks, promotion of the financial sector.)
**3.** (i) Accepting deposits — savings, current (cheque account), fixed and recurring. (ii) Advancing loans — cash credit, overdraft, demand loan, term loan, bill discounting. (iii) Credit creation. (iv) Agency services — collecting cheques and bills, paying bills and premiums, buying and selling securities, safe custody. (v) General utility services — drafts, pay orders, cards, mobile and internet banking, remittance and foreign exchange business.
**4.** *Banking* institutions accept demand deposits, operate cheque accounts and create credit: central bank, commercial banks, development banks, finance companies, microfinance institutions. *Non-banking* institutions collect public money and render financial services but do not accept demand deposits and cannot create credit: insurance companies, Employees' Provident Fund, Citizen Investment Trust, mutual funds and financial cooperatives. Give one example of each.
**5.** Insurance is a contract under which the insurer pays the insured on the happening of a stated event in return for a premium. It works on the **pooling of risk**: many pay a small premium into one fund from which the few who suffer a loss are paid, so the loss of an individual is spread over the group. Conditions: many similar exposures, a loss capable of being estimated in money, and an insurable interest. Any three kinds: life (whole life, endowment, money-back, term), fire, marine, motor, health, accident, crop or livestock insurance.
**6.** Cheque (open, order or crossed — a written order on the bank; only against a current account); bank draft (the bank's own order to pay, used where the payer has no account); pay order (the bank undertakes to pay a fixed amount to a named person, used for taxes and tenders); letter of credit (the bank promises to pay the exporter against shipping documents); debit and credit cards (access to one's own account; a short-term borrowing limit); mobile and internet banking (payment instructions from a phone or a website, used for bills and transfers). (Any five, each explained.)
**7.** Remittance is money sent by a person working away from home, usually abroad, to a person at home. For Nepal it matters because (i) it is one of the largest single sources of foreign exchange; (ii) it sustains household consumption, education, health and house construction; (iii) it reduces pressure on the balance of payments because it does not have to be repaid; (iv) it creates the savings that bank deposits and cooperatives are built from; (v) it employs a large number of people in the transfer business. Its risks are dependence on foreign labour markets and the loss to *hundi*, the illegal informal channel.
:::

**Group C — Long answer (8 marks each)**

1. Introduce the financial institutions of Nepal. Describe any five functions of a financial institution. <span class="marks">[8]</span>
2. What is a bank? Explain the primary functions of a commercial bank and show, with a suitable example, how a commercial bank creates credit. <span class="marks">[8]</span>
3. What is insurance? Explain the principle of insurance and compare life insurance with non-life insurance. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Introduction (3).* A financial institution is an institution that collects money from savers and lends or invests it for those who need it, and provides financial services such as deposits, loans, payments, insurance and foreign exchange. Nepal's institutions are of two families. Banking: Nepal Rastra Bank (2013 B.S., 1956 A.D.), commercial banks (Nepal Bank Limited, 1994 B.S., the first), development banks (Agricultural Development Bank, 2024 B.S.), finance companies and microfinance institutions. Non-banking: insurance companies regulated by Beema Samiti, Employees' Provident Fund, Citizen Investment Trust, mutual funds and financial cooperatives.
*Five functions (5).* (i) Mobilising savings. (ii) Supplying credit to trade, industry, agriculture and households. (iii) Providing the payment system — cheques, drafts, cards, electronic transfer and clearing. (iv) Transforming maturity — short-term deposits into long-term loans. (v) Bearing and pooling risk. (Alternatives: foreign exchange, remittance, financial advice, government banking, credit creation.)
**2.** *Definition (2).* A bank is a financial institution that accepts deposits from the public, lends money and provides payment services, aiming at profit.
*Primary functions (4).* (i) Accepting deposits — savings, current, fixed, recurring; only the current account carries a cheque. (ii) Advancing loans — cash credit, overdraft, demand loan, term loan, bill discounting, hire purchase. (iii) Credit creation. (Also agency and general utility functions may be given briefly.)
*Credit creation (2).* Suppose a bank receives a deposit of Rs. 10,000 and the cash reserve ratio is 10 per cent. It keeps Rs. 1,000 and lends Rs. 9,000. The borrower spends it, the receiver deposits it in a bank, which keeps Rs. 900 and lends Rs. 8,100, and so on. The total deposits created are $10{,}000 \times \frac{1}{0.10} = Rs.\ 1{,}00{,}000$ — ten times the original deposit. The multiplier is $\frac{1}{\text{reserve ratio}}$.
**3.** *Definition (1).* Insurance is a contract in which the insurer, in return for a premium, agrees to pay a stated sum to the insured on the happening of a stated event.
*Principle (3).* Pooling of risk — many persons exposed to a similar risk each contribute a small premium to a common fund, and the few who actually suffer a loss are compensated from that fund, so the loss of one is shared by all. Three conditions are needed: a large number of similar exposures, a loss that can be measured in money, and an insurable interest.
*Comparison (4).* Life insurance insures a human life: the event (death) is certain but its time is not, the policy is usually long-term, it has a savings element and a surrender value, and the sum assured is fixed in advance. Non-life insurance insures property or liability: the event is uncertain, the policy is usually for one year and renewable, there is no savings element and no surrender value, and the compensation is limited to the actual loss. Examples: endowment and whole-life policies on the life side; fire, marine, motor, health, crop and livestock policies on the non-life side.
:::

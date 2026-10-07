---
subject: Economics
grade: 10
unit: 3
title: Macroeconomics (समष्टि अर्थशास्त्र)
hours: 12
area: Macroeconomics
---

Microeconomics adds up millions of individual decisions; macroeconomics looks at the totals. Two sets of totals dominate this unit. The first is the **government's own finances** — what it collects, what it spends, what it borrows and whether the year ends in surplus or deficit — which is the subject of **public finance**. The second is the country's dealings with the rest of the world — what it sells abroad, what it buys, how the two compare and how the gap is paid for — which is the subject of **international trade** and the **balance of payments**. Both matter enormously to Nepal, whose government spends more than it earns and whose imports are several times its exports.

::: key What the examiner tests here
Group A asks: "What is public finance?", "What is a budget?", "Distinguish between the balance of trade and the balance of payments", "What is the terms of trade?", "What is devaluation?". Group B asks for the sources of public revenue and the kinds of public expenditure, the difference between direct and indirect tax, the merits of free trade, or the features of Nepal's foreign trade. Learn the definitions in one line each, and be ready to compute a budget deficit, the terms of trade, or the balance of payments from a table.
:::

## 3.1 Government finance: public revenue, public expenditure and public debt

**Public finance (सार्वजनिक वित्त)** is the branch of economics that studies the **income and expenditure of the government** and the way it manages them — the sources from which the government raises money, the purposes for which it spends it, the debt it incurs, and the effect of all of this on the economy. Unlike a private household, the government does not aim at profit: its aim is to provide public goods and services and to influence the economy for the general good.

**Public revenue.** The income the government raises is of two kinds.

| Source | What it is | Examples |
|---|---|---|
| **Tax revenue** | Compulsory payments, with no direct return to the payer | Income tax, VAT, excise duty, customs duty, land and house tax, vehicle tax |
| **Non-tax revenue** | Income from services, property, penalties and other sources | Fees and charges, fines, registration fees, royalties, dividends from public enterprises, interest, rent of government property, foreign grants |
| **Capital receipts** | Money raised by borrowing or by selling assets | Internal loans, treasury bills and bonds, foreign loans, principal repaid by borrowers |

**Public expenditure.** Government spending is classified in two ways.

| Classification | Kinds |
|---|---|
| By nature | **Recurrent expenditure** — running the government: salaries, allowances, goods and services, interest on debt. **Capital expenditure** — building assets: roads, bridges, irrigation, buildings, machinery |
| By purpose | **Developmental expenditure** — education, health, agriculture, infrastructure. **Non-developmental expenditure** — defence, general administration, debt service |

**Causes of the growth of public expenditure.** Growth of population and of the demand for services; the rising cost of defence and internal security; the state's growing role in education, health and social security; the cost of economic development — Nepal's capital budget is almost entirely a development budget; the growth of public debt and the interest on it; inflation, which raises the money cost of everything the government buys; and the growing complexity of regulation.

**Public debt.** When revenue falls short of expenditure, the government borrows, and the accumulated borrowing is the **public debt**.

| Kind | Where it comes from | Notes |
|---|---|---|
| **Internal debt** | Borrowing inside the country — treasury bills, development bonds, loans from Nepal Rastra Bank and from the public | Repaid in rupees; it is a transfer from one set of citizens to another, but it can still crowd out private borrowing |
| **External debt** | Borrowing from foreign governments and international bodies — the World Bank, the Asian Development Bank, the IMF, friendly countries | Repaid in foreign currency, so it adds to the demand for foreign exchange; often carries conditions and concessional terms |

**Public debt is a burden** because it must be serviced: interest has to be paid every year and the principal repaid, and both come out of future revenue, so they compete with schools and hospitals. It can also be a **blessing**, because it lets the government build a road or a power plant now and pay for it over the years during which it yields benefits, and it brings in foreign exchange and technology with an external loan. The rule of prudence is simple: **borrow for capital expenditure, not to meet a salary bill.**

## 3.2 Tax, the budget and fiscal policy

**Tax** is a compulsory contribution imposed by the government on persons, goods, services and transactions to meet public expenditure, without a direct and proportionate return to the payer.

**Direct and indirect tax.**

| Point | Direct tax | Indirect tax |
|---|---|---|
| Burden | Borne by the person legally liable; cannot be shifted | Shifted to the final consumer |
| Levied on | Income, profit, property | Goods, services, transactions |
| Examples | Income tax, house and land tax, capital gains tax, vehicle tax | VAT, excise duty, customs duty, entertainment tax |
| Effect on prices | Does not directly raise prices | Raises the price of the goods |
| Equity | Usually progressive — the rich pay proportionately more | Regressive in effect — the same rate weighs more on the poor |
| Administration | Collected directly from the taxpayer, and can be evaded by concealment | Collected at the point of sale, and harder to evade |
| Coverage | Reaches only those within the tax net | Reaches almost everybody who buys |

**The budget.** The **budget (बजेट)** is the government's annual statement of its estimated revenue and its proposed expenditure for the coming financial year, presented to the legislature and, once approved, authorising the government to collect and to spend.

**Kinds of budget.**

- **Balanced budget** — estimated revenue equals proposed expenditure. It is prudent, but it may be the wrong policy in a depression, when extra spending is needed.
- **Surplus budget** — revenue exceeds expenditure. It is used to control inflation, to retire debt, and to build up reserves.
- **Deficit budget** — expenditure exceeds revenue. It is used to fight a depression and unemployment, and to finance development; but a deficit continued year after year causes inflation, rising debt and a loss of confidence.

$$Budget\ deficit = Public\ expenditure - Public\ revenue$$

**Fiscal policy** is the government's policy on **taxation, public expenditure and public borrowing**, used deliberately to influence the level of income, employment and prices in the economy.

- **Expansionary fiscal policy** — lower taxes, higher spending, more borrowing — used to raise demand, output and employment in a slump. It risks inflation and a larger deficit.
- **Contractionary fiscal policy** — higher taxes, lower spending, less borrowing — used to reduce demand and check inflation. It risks unemployment.
- **Automatic stabilisers** — progressive income tax and unemployment benefits work against the cycle without anyone deciding anything: in a boom, tax receipts rise and spending on benefits falls, cooling the economy; in a slump the reverse happens.

```figure caption="The budget balance and what it is for. A deficit is an instrument, not an accident — but only when it finances capital spending that will earn its keep."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.6))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6)
for x,name,desc,c,ec in ((0.2,"BALANCED","Revenue = Expenditure\\n\\nno borrowing needed;\\nthe prudent case",
                          "#eaf1ff",ACCENT),
                         (3.4,"SURPLUS","Revenue > Expenditure\\n\\nchecks inflation,\\nrepays debt",
                          "#f6f8fc",MUTED),
                         (6.6,"DEFICIT","Expenditure > Revenue\\n\\nfights a slump, finances\\ndevelopment; risks inflation",
                          "#fdf3f3",SERIES[1])):
    ax.add_patch(FancyBboxPatch((x,1.0),3.1,3.9,boxstyle="round,pad=0.07",fc=c,ec=ec,lw=1.2))
    ax.text(x+1.55,4.4,name,ha='center',fontsize=8,color=INK,weight='bold')
    ax.text(x+1.55,2.7,desc,ha='center',va='center',fontsize=6.2,color=INK)
ax.text(5.0,0.35,"Deficit = Expenditure − Revenue",ha='center',fontsize=6.8,color=INK)
```

::: example The budget figures
**Problem.** In a financial year the Government of Nepal estimated revenue of Rs. 11,00,000 million and expenditure of Rs. 14,00,000 million. Of the revenue, Rs. 9,50,000 million was tax revenue. Of the expenditure, Rs. 5,00,000 million was recurrent and Rs. 9,00,000 million capital. Find (a) the budget deficit, (b) the share of tax in the revenue, (c) the deficit as a percentage of expenditure, and (d) the amount that must be raised by borrowing.

**Solution.**
Step 1 — $Budget\ deficit = Expenditure - Revenue = 14{,}00{,}000 - 11{,}00{,}000 = Rs.\ 3{,}00{,}000$ million.
Step 2 — $Share\ of\ tax\ revenue = \frac{9{,}50{,}000}{11{,}00{,}000} \times 100 = 86.36\%$.
Step 3 — $Deficit\ as\ a\ share\ of\ expenditure = \frac{3{,}00{,}000}{14{,}00{,}000} \times 100 = 21.4\%$.
Step 4 — The deficit must be financed by **borrowing** — internal loans and treasury bills, and foreign loans and grants. So the government must borrow Rs. 3,00,000 million.
Step 5 — Note the composition: the capital expenditure is Rs. 9,00,000 million, which is larger than the deficit, so the borrowing is more than covered by the development spending. That is the **right use** of a deficit.

**Answer.** Deficit Rs. 3,00,000 million; tax 86.36 % of revenue; deficit 21.4 % of expenditure; borrowing of Rs. 3,00,000 million.
**What it means.** A deficit is not automatically bad. What matters is what the borrowed money buys. A deficit that finances a motorable road or a hydropower plant is an investment; one that pays salaries is consumption at the expense of next year's taxpayers.
:::

```photo id="eco10/containers" caption="Container ships at a port. A landlocked country such as Nepal pays for every tonne it trades twice over — once for the goods and once for the transit." width="82"
```

## 3.3 International trade

**International trade** is the exchange of goods and services between one country and another. It exists because **no country can produce everything it needs efficiently**. Climate, natural resources, the skill of the labour force, capital and technology differ from country to country, so each country gains by specialising in what it produces relatively best and trading for the rest. The gains from trade are a **larger total output**, lower prices, a wider variety of goods, the transfer of technology and the stimulus of competition.

**Absolute advantage.** Adam Smith argued that a country should export the goods it can produce with **less labour and other resources** than its trading partner, and import those in which it uses more. A country that is absolutely better at everything, however, still gains from trade — which is Ricardo's contribution.

**Comparative advantage.** David Ricardo showed that trade is beneficial even when one country is absolutely more efficient in **both** goods, so long as the **relative** efficiencies differ. A country should specialise in the good in which its disadvantage is smallest (or its advantage largest) — that is, in the good with the lower **opportunity cost** — and buy the other.

Consider two countries, each with 100 units of labour, producing cloth and rice:

| | Cloth (units) | Rice (units) |
|---|---|---|
| **Nepal** | 40 | 80 |
| **India** | 60 | 100 |

Nepal is worse at both, so it has no absolute advantage. But look at opportunity cost. In Nepal, making one unit of cloth costs 2 units of rice ($80 \div 40$); in India it costs 1.67 units of rice ($100 \div 60$). India is relatively more efficient in cloth, and Nepal relatively less inefficient in rice. So India should specialise in cloth and Nepal in rice, and both are better off after trade.

**The terms of trade.** The **terms of trade** measure the rate at which a country's exports exchange for its imports.

$$Terms\ of\ trade = \frac{Index\ of\ export\ prices}{Index\ of\ import\ prices} \times 100$$

If the ratio is above 100 the terms of trade are favourable — a given quantity of exports buys more imports. If it falls below 100 they are unfavourable, and the country must export more to pay for the same imports.

**Free trade and protection.** **Free trade** is trade without barriers. Its advantages are the full international division of labour, lower prices for consumers, a wider choice of goods, larger markets for producers, and competition that forces efficiency. **Protection** is the policy of restricting imports to shelter domestic producers, by a **tariff** (a tax on the import), a **quota** (a limit on the quantity), an **embargo** (a ban), a **subsidy** to domestic producers, or administrative rules that make importing difficult.

The case for protection is that a **new ("infant") industry** cannot survive against established foreign competitors and needs time to grow; that a country should not depend on foreigners for **essential goods**, especially in war; that it should diversify away from a few primary exports; that tariff revenue is easy to collect; and that protecting domestic industry protects domestic employment. The case against is that protection raises prices for consumers, shelters inefficiency, invites retaliation from trading partners, and makes the protected industry lazy — and that the infant may never grow up.

## 3.4 Balance of trade, balance of payments, exchange rate and Nepal's trade policy

**Balance of trade (व्यापार सन्तुलन)** is the difference between the value of a country's **exports of goods** and the value of its **imports of goods** in a year.

$$Balance\ of\ trade = Value\ of\ exports - Value\ of\ imports$$

- If exports exceed imports, the balance of trade is **favourable** (a trade surplus).
- If imports exceed exports, it is **unfavourable** (a trade deficit).

**Balance of payments (भुक्तानी सन्तुलन)** is the **complete record of all** a country's economic transactions with the rest of the world in a year — not only goods, but services, income, transfers and capital movements.

| The balance of payments | |
|---|---|
| **Current account** | **Goods** (visible trade: exports minus imports = the balance of trade); **services** (invisible trade: tourism, transport, insurance); **income** (interest, dividend, profit); **transfers** (remittance, grants) |
| **Capital account** | Foreign loans and their repayment, foreign direct investment, portfolio investment, changes in reserves |
| **Errors and omissions** | The figure that reconciles the two |
| **Overall balance** | Should be financed by a change in the foreign exchange reserves |

**Balance of trade versus balance of payments.** The balance of trade covers **goods only** and is one part of the current account. The balance of payments covers **every** transaction — goods, services, income, transfers and capital — and always balances in the accounting sense, because the difference is settled by a movement in the reserves or by borrowing. A country such as Nepal can have a large **trade deficit** and still have a **manageable overall balance of payments**, because **remittance** earned by migrant workers is so large that it pays for much of the import bill.

**Exchange rate.** The **exchange rate** is the price of one country's currency in terms of another's — for example Rs. 133 for one US dollar. A **fixed** rate is pegged by the central bank; a **floating** rate is set by demand and supply in the market; Nepal's rupee is **pegged to the Indian rupee** at a fixed rate, with the rate against other currencies moving with the Indian rupee.

**Depreciation and devaluation.** **Depreciation** is a fall in a currency's value under a floating rate; **devaluation** is a deliberate official reduction of a fixed rate. Both make exports cheaper to foreigners and imports dearer at home, so they should improve the trade balance — but they also raise the price of imported fuel, machinery and medicine, and so cause inflation, and they make foreign debt repayment dearer.

```photo id="eco10/hydropower" caption="The Chilime hydropower project. Electricity has become one of the few exports in which Nepal has a genuine comparative advantage — and in the wet season it is sold to India and, through India, to Bangladesh." width="82"
```

**Nepal's foreign trade: features and problems.** Nepal's trade has four standing features. It is **heavily concentrated on India**, which takes about two-thirds of Nepal's exports and supplies about two-thirds of its imports; the **trade deficit is chronic and large**, with imports several times exports; **exports are dominated by a few primary and semi-processed goods** — readymade garments, woollen carpets, pashmina, tea, cardamom, lentils, jute goods, and electricity exports in the wet season — while **imports are dominated by manufactured goods, petroleum products, machinery, vehicles, medicines and food**; and the economy is a **transit-dependent** one, landlocked, relying on Indian ports and roads for its third-country trade.

**Trade policy.** Nepal's trade policy has moved through import substitution in the 1960s and 1970s, export promotion from the 1980s, and liberalisation since the mid-1980s and especially after joining the WTO in 2004. The measures now in use are: export promotion through concessional credit, duty drawbacks and cash incentives; trade facilitation through one-stop service at the border, electronic customs and improved transit agreements; diversification of markets and products beyond India, including electricity trade with Bangladesh and India; and quality and standard compliance so that Nepali goods can enter foreign markets.

::: example Comparative advantage and the terms of trade
**Problem.** (a) With the labour figures of the table above (Nepal: 40 cloth or 80 rice; India: 60 cloth or 100 rice, each with 100 units of labour), work out the opportunity cost of one unit of cloth in each country and say in which good each country should specialise. (b) In a certain year a country's index of export prices was 150 and its index of import prices was 125 (base year 2015 = 100). Find the terms of trade and say whether they are favourable.

**Solution.**
Step 1 — (a) Opportunity cost of 1 unit of cloth in Nepal $= \frac{80}{40} = 2$ units of rice.
Step 2 — Opportunity cost of 1 unit of cloth in India $= \frac{100}{60} = 1.67$ units of rice.
Step 3 — India gives up less rice to make a unit of cloth, so India has a comparative advantage in cloth. Nepal's comparative advantage is in rice, since it gives up only $40/80 = 0.5$ units of cloth for a unit of rice, against India's $60/100 = 0.6$.
Step 4 — (b) $Terms\ of\ trade = \frac{150}{125} \times 100 = 120$.
Step 5 — Since 120 is above 100, the terms of trade are **favourable**: the same quantity of exports now buys 20 per cent more imports than in the base year.

**Answer.** (a) India specialises in cloth (opportunity cost 1.67 rice against Nepal's 2) and Nepal in rice (opportunity cost 0.5 cloth against India's 0.6). (b) Terms of trade = 120, favourable.
**What it means.** Even a country that is worse at everything gains from trade, provided it specialises where its relative disadvantage is smallest. And a country watches its terms of trade as closely as its exchange rate, because a fall from 120 to 90 means it must export a third more to buy the same imports.
:::

::: example The balance of payments
**Problem.** From the following figures of a country for a year (in Rs. billion), find the balance of trade, the current account balance and the overall balance of payments. Merchandise exports 1,200; merchandise imports 4,000; tourism and other services earned 800; services paid abroad 400; interest and dividend paid abroad 300; remittance and grants received 5,200; foreign loans received 900; foreign loans repaid 200; foreign direct investment 300; change in reserves 3,500.

**Solution.**
Step 1 — $Balance\ of\ trade = 1{,}200 - 4{,}000 = -2{,}800$, a **trade deficit** of Rs. 2,800 billion.
Step 2 — Current account: goods −2,800; services $+800 - 400 = +400$; income $-300$; transfers $+5{,}200$.
Step 3 — Current account total $= -2{,}800 + 400 - 300 + 5{,}200 = +2{,}500$ billion — a current account **surplus**.
Step 4 — Capital account: loans received +900, loans repaid −200, FDI +300 = $+1{,}000$ billion.
Step 5 — Overall balance $= 2{,}500 + 1{,}000 = +3{,}500$ billion, which matches the increase in reserves of Rs. 3,500 billion.

**Answer.** Balance of trade −2,800; current account +2,500; overall balance +3,500 billion, reflected in the rise in reserves.
**What it means.** This is the Nepali pattern exactly: a very large trade deficit, turned into a current account surplus by remittance, with the surplus added to the foreign exchange reserves. It shows why remittance is not a small matter in Nepal's macroeconomy — without it the arithmetic would not close.
:::

```figure caption="The balance of payments at a glance. The trade deficit sits inside the current account, where remittance usually rescues it; the capital account finances whatever is left."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,2.9))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.add_patch(FancyBboxPatch((0.3,5.4),4.4,4.2,boxstyle="round,pad=0.08",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(2.5,9.0,"CURRENT ACCOUNT",ha='center',fontsize=7.6,color=INK,weight='bold')
ax.text(2.5,7.1,"Goods (visible trade)\n= balance of trade\n\nServices (invisible trade)\n\nIncome\n\nTransfers: remittance, grants",
        ha='center',va='center',fontsize=6.0,color=INK)
ax.add_patch(FancyBboxPatch((5.3,5.4),4.4,4.2,boxstyle="round,pad=0.08",fc="#fdf3f3",ec=SERIES[1],lw=1.2))
ax.text(7.5,9.0,"CAPITAL ACCOUNT",ha='center',fontsize=7.6,color=INK,weight='bold')
ax.text(7.5,7.1,"Foreign loans received\nand repaid\n\nForeign direct investment\n\nPortfolio investment\n\nChange in reserves",
        ha='center',va='center',fontsize=6.0,color=INK)
ax.add_patch(FancyBboxPatch((1.0,2.4),8.0,2.2,boxstyle="round,pad=0.07",fc="#f6f8fc",ec=MUTED,lw=1.1))
ax.text(5.0,3.5,"In Nepal the current account usually closes with a small surplus, because\nremittance of about a quarter of GDP more than covers a trade deficit\nseveral times the size of merchandise exports.",
        ha='center',va='center',fontsize=6.2,color=INK)
ax.text(5.0,1.0,"Both accounts are parts of one balance of payments; the overall balance is met by the change in reserves",
        ha='center',fontsize=6.0,color=MUTED)
```

::: caution The common mistakes
Four errors are made repeatedly. First, **the balance of trade is not the balance of payments**: the first covers goods only, the second covers everything. Second, a **budget deficit is not always a bad thing** — a deficit that finances capital expenditure is investment, though one that pays salaries year after year is not. Third, **devaluation does not automatically cure a trade deficit**; it makes imports dearer, causes inflation and raises the cost of servicing foreign debt, and it works only if the country has goods to sell that foreigners will buy more of. Fourth, **comparative advantage, not absolute advantage, is the basis of gainful trade** — a country that is worse at everything still gains by specialising where its relative disadvantage is smallest.
:::

## Chapter summary

- **Public finance** studies the government's income, expenditure and debt. **Public revenue** is tax revenue, non-tax revenue and capital receipts (borrowing).
- **Public expenditure** is recurrent or capital, and developmental or non-developmental. It grows because of population, defence, social services, development, debt service, inflation and regulation.
- **Public debt** is internal (borrowed inside the country) or external (borrowed abroad). It is a burden because it must be serviced from future revenue; it is useful when it finances capital expenditure and brings in foreign exchange and technology. Borrow for capital, not for salaries.
- **Tax** is a compulsory contribution. **Direct tax** is borne by the person legally liable and cannot be shifted (income tax, house and land tax); **indirect tax** is shifted to the consumer (VAT, excise, customs) and, being the same rate for rich and poor, weighs more heavily on the poor.
- The **budget** is the government's annual statement of estimated revenue and proposed expenditure. It may be **balanced**, in **surplus** (used to check inflation and repay debt) or in **deficit** (used to fight a slump and finance development, at the risk of inflation and growing debt). $Budget\ deficit = Expenditure - Revenue$.
- **Fiscal policy** uses taxation, public expenditure and borrowing to influence income, employment and prices. It may be expansionary or contractionary, and it works partly through **automatic stabilisers** such as progressive tax and unemployment benefits.
- **International trade** arises because no country can produce everything efficiently. **Absolute advantage** (Smith) is producing with fewer resources; **comparative advantage** (Ricardo) is producing at the lower opportunity cost, and it explains why a country worse at everything still gains from trade.
- The **terms of trade** $= \frac{Index\ of\ export\ prices}{Index\ of\ import\ prices} \times 100$; above 100 they are favourable.
- **Free trade** gives the international division of labour, lower prices, wider choice and competition. **Protection** — tariffs, quotas, embargoes, subsidies and administrative barriers — shelters infant industries and essential goods but raises consumer prices, shelters inefficiency and invites retaliation.
- **Balance of trade** is exports of goods minus imports of goods. **Balance of payments** records **all** transactions: the current account (goods, services, income, transfers) and the capital account (loans, repayment, investment, reserves). A country can have a large trade deficit and still have a manageable overall balance because of remittance.
- The **exchange rate** is the price of one currency in another. It is fixed or floating; Nepal's rupee is pegged to the Indian rupee. **Devaluation** (a deliberate cut in a fixed rate) and **depreciation** (a market fall) make exports cheaper and imports dearer, improving the trade balance at the cost of inflation and dearer debt service.
- **Nepal's foreign trade** is concentrated on India, runs a chronic and large deficit, exports a few primary and semi-processed goods and imports manufactures, fuel, machinery and medicine, and is transit-dependent and landlocked. Its policy has moved from import substitution to export promotion, liberalisation, trade facilitation and market diversification.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is public finance? <span class="marks">[1]</span>
2. Write any two sources of non-tax revenue. <span class="marks">[1]</span>
3. What is public debt? <span class="marks">[1]</span>
4. What is a budget? <span class="marks">[1]</span>
5. What is a deficit budget? <span class="marks">[1]</span>
6. What is fiscal policy? <span class="marks">[1]</span>
7. Distinguish between direct and indirect tax in one line. <span class="marks">[1]</span>
8. What is absolute advantage? <span class="marks">[1]</span>
9. What is comparative advantage? <span class="marks">[1]</span>
10. What is the terms of trade? <span class="marks">[1]</span>
11. What is the balance of trade? <span class="marks">[1]</span>
12. What is the balance of payments? <span class="marks">[1]</span>
13. Write any two features of Nepal's foreign trade. <span class="marks">[1]</span>
14. What is devaluation? <span class="marks">[1]</span>
15. Write any two measures of protection. <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Public finance is the branch of economics that studies the income and expenditure of the government, its borrowing, and the effect of these on the economy.
**2.** Any two of: fees and charges, fines, registration fees, royalties, dividends from public enterprises, interest and rent, foreign grants.
**3.** Public debt is the total amount the government has borrowed and not yet repaid, whether internally or from abroad.
**4.** The budget is the government's annual statement of its estimated revenue and proposed expenditure for the coming financial year, presented to the legislature and authorising collection and spending once approved.
**5.** A deficit budget is one in which the estimated expenditure exceeds the estimated revenue.
**6.** Fiscal policy is the government's policy on taxation, public expenditure and public borrowing, used deliberately to influence income, employment and prices in the economy.
**7.** A direct tax is borne by the person on whom it is legally imposed and cannot be shifted; an indirect tax is imposed on one person but shifted to another, ultimately the final consumer.
**8.** Absolute advantage is the ability of a country to produce a good with fewer resources than another country.
**9.** Comparative advantage is the ability of a country to produce a good at a lower opportunity cost than another country; it is the basis of gainful trade.
**10.** The terms of trade are the ratio of the index of a country's export prices to the index of its import prices, multiplied by 100.
**11.** The balance of trade is the difference between the value of a country's exports of goods and its imports of goods in a year.
**12.** The balance of payments is the complete record of all a country's economic transactions with the rest of the world in a year, covering goods, services, income, transfers and capital movements.
**13.** Any two of: heavy concentration on India; a chronic and large trade deficit; exports dominated by a few primary and semi-processed goods; imports dominated by manufactures, fuel and machinery; landlocked and transit-dependent.
**14.** Devaluation is a deliberate official reduction in the value of a country's currency in terms of foreign currencies under a fixed exchange rate.
**15.** Any two of: tariff (customs duty), quota, embargo, subsidy to domestic producers, administrative barriers.
:::

**Group B — Short answer (5 marks each)**

1. What is public finance? Explain the sources of public revenue and the kinds of public expenditure. <span class="marks">[5]</span>
2. What is public debt? Explain its kinds and state whether public debt is a burden or a blessing. <span class="marks">[5]</span>
3. What is a budget? Explain the balanced, surplus and deficit budgets and when each is appropriate. <span class="marks">[5]</span>
4. Distinguish between direct tax and indirect tax with examples, and state the merits of each. <span class="marks">[5]</span>
5. Explain the theory of comparative advantage with an example and state the gains from international trade. <span class="marks">[5]</span>
6. Distinguish between the balance of trade and the balance of payments. <span class="marks">[5]</span>
7. Explain the features and problems of Nepal's foreign trade and state the measures of Nepal's trade policy. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definition as in Group A answer 1. Revenue: tax revenue (income tax, VAT, excise, customs, land and house tax); non-tax revenue (fees, fines, registration fees, royalties, dividends, interest, rent, foreign grants); and capital receipts (internal and external borrowing). Expenditure: by nature, recurrent (salaries, goods and services, interest) and capital (roads, buildings, machinery); by purpose, developmental (education, health, agriculture, infrastructure) and non-developmental (defence, general administration, debt service). Explain each with one example.
**2.** Definition as in Group A answer 3. Kinds: internal debt — treasury bills, development bonds, loans from the central bank and the public, repaid in rupees; external debt — loans from foreign governments and international bodies such as the World Bank, the ADB and the IMF, repaid in foreign currency. It is a burden because interest and repayment must come out of future revenue and so compete with other spending; and external debt must be repaid in foreign exchange. It is a blessing because it allows a capital project to be paid for over the years in which it yields benefits, and an external loan brings foreign exchange and technology. The prudent rule is to borrow for capital expenditure, not to meet recurrent expenses.
**3.** Definition as in Group A answer 4. Balanced budget — revenue equals expenditure; prudent and non-inflationary, appropriate in normal times. Surplus budget — revenue exceeds expenditure; used to check inflation by withdrawing purchasing power, to retire debt and to build reserves. Deficit budget — expenditure exceeds revenue; used to raise demand, output and employment in a slump and to finance development, but continued year after year it causes inflation, a growing debt and a loss of confidence. $Deficit = Expenditure - Revenue$.
**4.** Direct tax: levied on income, profit or property; borne by the person legally liable and not shiftable; progressive; collected directly; can be evaded by concealment; examples income tax, house and land tax, capital gains tax. Indirect tax: levied on goods, services and transactions; shifted to the final consumer; raises the price; regressive in effect; hard to evade because it is collected at the point of sale; examples VAT, excise, customs. Merits of direct tax: equity, certainty, and it redistributes income. Merits of indirect tax: wide coverage, convenient to collect, difficult to evade, and it can be used to discourage harmful goods.
**5.** Comparative advantage (Ricardo): a country should specialise in the good in which its opportunity cost is lower and trade for the other, even if it is absolutely less efficient in both. Example: with 100 units of labour Nepal can produce 40 cloth or 80 rice, India 60 cloth or 100 rice. The opportunity cost of one cloth is 2 rice in Nepal and 1.67 in India, so India specialises in cloth and Nepal in rice; both gain. Gains from trade: larger total output through the international division of labour; lower prices; a wider variety of goods; transfer of technology and skills; competition that raises efficiency; and larger markets for producers.
**6.** *Balance of trade*: covers **goods only** — merchandise exports minus merchandise imports; it is the visible part of the current account; a deficit means imports of goods exceed exports. *Balance of payments*: covers **every** transaction with the rest of the world — goods, services, income, transfers and capital movements; it is a complete account and always balances in the accounting sense, the difference being settled by a change in reserves or by borrowing. Nepal routinely has a large trade deficit but a manageable overall balance of payments because of remittance.
**7.** Features: heavy concentration on India for both exports and imports; a chronic and large trade deficit, with imports several times exports; exports dominated by a few primary and semi-processed goods — garments, carpets, pashmina, tea, cardamom, lentils and seasonal electricity; imports dominated by manufactures, petroleum, machinery, vehicles and medicine; and landlocked and transit-dependent, relying on Indian ports and roads. Problems: the deficit drains foreign exchange; dependence on a single market; low value addition and low quality compliance; poor infrastructure and high transit cost. Policy: export promotion through concessional credit, duty drawback and cash incentives; trade facilitation through one-stop border service and electronic customs; market and product diversification, including electricity trade; and quality and standard compliance.
:::

**Group C — Long answer (8 marks each)**

1. What is public finance? Explain the sources of public revenue, the kinds of public expenditure and the causes of the growth of public expenditure, and state the merits and demerits of public debt. <span class="marks">[8]</span>
2. Explain the theory of comparative advantage and the gains from international trade, and distinguish between the balance of trade and the balance of payments with the help of the Nepali case. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Definition (1).* As in Group A answer 1.
*Public revenue (2).* Tax revenue — direct (income tax, house and land tax, capital gains tax, vehicle tax) and indirect (VAT, excise, customs); non-tax revenue — fees, fines, registration fees, royalties, dividends, interest, rent and foreign grants; capital receipts — internal and external borrowing.
*Public expenditure (2).* Recurrent and capital; developmental and non-developmental; with examples.
*Causes of growth (1.5).* Population growth and rising demand for services; defence and internal security; the state's growing role in education, health and social security; the cost of development; the growth and servicing of public debt; inflation; and growing regulation.
*Public debt (1.5).* Kinds internal and external; burden — servicing from future revenue, foreign exchange needed for external debt; blessing — capital projects paid for over their useful life, foreign exchange and technology with an external loan; the prudent rule is to borrow for capital, not recurrent, expenditure.
**2.** *Comparative advantage (3).* Ricardo's theory: trade benefits a country even when it is absolutely less efficient in both goods, provided the relative efficiencies differ. A country should specialise where its opportunity cost is lower. Give the numerical illustration with Nepal and India; compute the opportunity cost of cloth in each and show the specialisation that follows. Contrast it with Adam Smith's absolute advantage.
*Gains from trade (2).* Larger total output from the international division of labour; lower prices; wider choice; transfer of technology and skills; competition; larger markets; and the possibility of earning the foreign exchange needed for imports of capital goods.
*Balance of trade and balance of payments (3).* Balance of trade = merchandise exports − merchandise imports (goods only) and is the visible part of the current account; balance of payments = the complete record of all transactions — goods, services, income, transfers and capital — and always balances through a change in reserves or borrowing. Nepali case: a large and chronic trade deficit, a very large remittance inflow in the transfers of the current account, and therefore a manageable overall balance of payments; imports several times exports; heavy dependence on India; a landlocked, transit-dependent economy.
:::

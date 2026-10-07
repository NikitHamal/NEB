---
subject: Economics
grade: 10
unit: 1
title: Basic Concepts of Economics and Allocation of Resources (अर्थशास्त्रको आधारभूत अवधारणा र साधनको बाँडफाँट)
hours: 12
area: Basic Concepts
---

Economics begins with a simple but uncomfortable fact: people want more than there is. A family wants a house, a scooter, good schooling for two children and a secure old age, but its income will not stretch to all of them at once — so it chooses. A country faces the same problem on a larger scale, with farmland, labour, machines and money that are never enough for everything its people want. This unit sets out the ideas that follow from that fact — **scarcity, choice, opportunity cost and the allocation of resources** — describes the three kinds of economy that have been built to answer the same questions, and introduces the **macroeconomic variables** and the **circular flow of income** that the rest of the book uses.

::: key What the examiner tests here
Group A of the SEE paper opens from this unit almost every year: "Define an economy", "What is opportunity cost?", "Write any two features of a capitalist economy", "What is a mixed economy?", "Write any two macroeconomic variables". Group B asks for the features and merits of a capitalist or mixed economy, or for the three central problems of an economy, or for the circular flow of income. Learn the definitions exactly, and learn the features as numbered lists of five.
:::

## 1.1 Economy: meaning, types and features

An **economy (अर्थव्यवस्था)** is the organised system by which the people of a country produce goods and services, distribute them among themselves and consume them, in order to satisfy their wants with the limited resources available.

An economy has to answer three questions, and the way it answers them decides what kind it is: **who owns the means of production**, **who takes the decisions**, and **how the goods are distributed**.

| Type | Ownership of resources | Who decides | Distribution |
|---|---|---|---|
| **Capitalist (market) economy** | Private individuals | Producers responding to prices; the market | According to the ability to pay |
| **Socialist (centrally planned) economy** | The state | The central planning authority | According to need or to work |
| **Mixed economy** | Both private and state | Both the market and the state | Both profit and social policy |

**Capitalist economy.** A capitalist economy is one in which the means of production are owned and operated by private individuals for profit, and production is guided by the price mechanism — the interaction of demand and supply in free markets.

*Features.* (i) **Private ownership** of land, factories, machines and capital. (ii) **Freedom of enterprise** — anyone may start any business. (iii) **Profit motive** as the mainspring of production. (iv) **Consumer sovereignty** — the consumer's rupee decides what shall be produced. (v) **Price mechanism** allocates resources; there is no central plan. (vi) **Competition** among producers, which keeps prices down and quality up. (vii) **Freedom of choice** in occupation and consumption, and **limited government** whose job is to keep the peace and enforce contracts.

*Merits.* Efficiency, because a producer who wastes resources is driven out; consumer satisfaction, because production follows demand; rapid technological progress, because innovation pays; and a wide variety of goods.

*Demerits.* Inequality of income and wealth; unemployment during a depression, because no one is responsible for employing everybody; the production of luxuries for the rich while the necessities of the poor go short; the creation of monopolies which exploit the consumer; and social costs such as pollution that no private firm pays for.

**Socialist economy.** A socialist economy is one in which the means of production are owned by the state and the decisions on what, how and for whom to produce are taken by a central planning authority.

*Features.* Public ownership of the means of production; **central planning** with five-year plans and fixed targets; the **absence of the profit motive**, replaced by social welfare; **equality** of income, with wages fixed by the plan; and little or no competition.

*Merits.* It can wipe out extreme inequality; it can direct resources to what the society needs rather than what is profitable; it can avoid unemployment; and it can carry out big projects that no private firm would undertake. *Demerits.* It is often **inefficient**, because nobody's income depends on doing the work well; consumers have less choice; initiative and invention suffer; and the planning machinery is slow and can make very large mistakes.

**Mixed economy.** A mixed economy has a **private sector and a public sector side by side**, with the market taking many decisions and the state taking others and regulating the rest. Nepal is a mixed economy: private industry, trade and banking operate under a framework of law and policy, while the state runs railways, drinking water, part of the power sector, education and health services, and directs credit and investment through the budget and the Nepal Rastra Bank. A mixed economy tries to keep the **efficiency of the market** and to cure its **inequality and instability** by state action — through taxation, public expenditure, social security and the regulation of monopolies.

```figure caption="The three kinds of economy and the same three questions. What changes is not the question but who answers it."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.add_patch(FancyBboxPatch((3.4,8.6),3.2,1.1,boxstyle="round,pad=0.06",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(5.0,9.15,"THE THREE QUESTIONS",ha='center',va='center',fontsize=8,color=INK,weight='bold')
ax.text(5.0,7.85,"What to produce?  How to produce?  For whom to produce?",ha='center',fontsize=6.6,color=MUTED)
for x,name,who,c in ((0.3,"Capitalist","the market\n(price mechanism)","#eef3ff"),
                     (3.6,"Socialist","the central\nplan","#f6f8fc"),
                     (6.9,"Mixed","the market\nand the state","#fdf3f3")):
    ax.add_patch(FancyBboxPatch((x,4.2),2.8,2.4,boxstyle="round,pad=0.06",fc=c,
                 ec=ACCENT if x<1 else (MUTED if x<4 else SERIES[1]),lw=1.1))
    ax.text(x+1.4,5.9,name,ha='center',va='center',fontsize=7.6,color=INK,weight='bold')
    ax.text(x+1.4,4.95,"answered by\n"+who,ha='center',va='center',fontsize=6.4,color=INK)
ax.text(5.0,2.6,"Nepal is a mixed economy.",ha='center',fontsize=6.8,color=INK)
ax.text(5.0,1.4,"Ownership decides who answers: private owners, the state, or both together.",
        ha='center',fontsize=6.2,color=MUTED)
for x in (1.7,5.0,8.3):
    ax.add_patch(FancyArrowPatch((x,4.15),(x,3.5),arrowstyle="-|>",mutation_scale=9,color=MUTED,lw=1.0))
```

```photo id="eco10/market" caption="A Kathmandu market. Every stall is a small answer to the three central problems: what to sell, how to sell it, and for whom." width="80"
```

## 1.2 Scarcity, choice, opportunity cost and the allocation of resources

**Scarcity (दुर्लभता)** means that the resources available to satisfy human wants are **limited in supply relative to the wants** for them. It does not mean that a thing is rare in the ordinary sense. Air is abundant and free; land in Kathmandu, clean drinking water in the Terai in April, a surgeon's time and the government's budget are all scarce, because at a zero price more would be wanted than exists.

Two things follow from scarcity.

**Choice (छनोट).** Because there is not enough for everything, somebody must decide **what** shall be produced, **how** it shall be produced and **who** shall get it. Every choice is a decision to go without something else. A family with Rs. 40,000 chooses between a scooter and a year's tuition for two children. It cannot buy both, so it chooses.

**Opportunity cost (अवसर लागत).** The **opportunity cost** of a choice is the value of the **next best alternative forgone**. It is not the money paid — it is what the money and the resources would otherwise have produced.

> **Opportunity cost is the benefit lost by choosing the next best alternative, not the total of everything forgone.**

The idea is the same for a whole economy. If the government spends Rs. 50 crore building a road, the opportunity cost is what that Rs. 50 crore would have produced in its next best use — say, two hospitals. There was no waste; the road may be exactly the right choice. But the choice had a cost, and a wise government counts it.

```photo id="eco10/terraces" caption="Terrace farming in Ramechhap. Land is the first factor of production, and in Nepal it is scarce, steep and fragmented — which is why so much labour is needed for so little output." width="84"
```

**Resources and their allocation.** The **factors of production** are:

| Factor | What it provides | Its reward |
|---|---|---|
| **Land** | All natural resources — soil, water, forests, minerals | Rent |
| **Labour** | Human effort, physical and mental | Wages |
| **Capital** | Man-made means of production — tools, machines, buildings, money used to buy them | Interest |
| **Entrepreneurship** | The organisation and risk-taking that brings the other three together | Profit |

**Allocation of resources (साधनको बाँडफाँट)** is the process of deciding **how much** of each factor of production shall be used, and **where**, to produce the goods and services the society wants.

In a **capitalist** economy the allocation is done by the **price mechanism**: if people want more rice, the price rises, rice growers earn more, and land and labour move into rice by themselves. In a **socialist** economy it is done by the **central plan**: the planners decide, in physical quantities, how much steel, cloth and wheat shall be produced. In a **mixed** economy both operate — the market allocates among consumer goods while the state allocates through the budget to defence, roads, schools and health, and steers the rest by policy.

```figure caption="Scarcity, choice and opportunity cost. The economy can be at any point on the curve, not beyond it; moving from A to B buys 30 more units of cloth and costs 20 units of food."
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(figsize=(4.9,2.9))
food = np.linspace(0, 100, 200)
cloth = 100*(1 - (food/100)**2)
ax.plot(cloth, food, color=ACCENT, lw=1.6)
ax.set_xlabel("Units of cloth", color=INK); ax.set_ylabel("Units of food", color=INK)
ax.set_xlim(0,112); ax.set_ylim(0,112)
ax.grid(color=GRID, lw=0.6); ax.spines[['top','right']].set_visible(False)
ax.scatter([80],[36],color=SERIES[1],zorder=3,s=26)
ax.scatter([20],[96],color=SERIES[1],zorder=3,s=26)
ax.annotate("A (80 cloth, 36 food)",xy=(80,36),xytext=(30,20),fontsize=7,color=INK,
            arrowprops=dict(arrowstyle="->",color=MUTED,lw=0.9))
ax.annotate("B (20 cloth, 96 food)",xy=(20,96),xytext=(30,104),fontsize=7,color=INK,
            arrowprops=dict(arrowstyle="->",color=MUTED,lw=0.9))
ax.text(64,72,"unattainable\n(scarcity)",fontsize=6.6,color=MUTED,ha='center')
ax.text(8,8,"resources\nunemployed",fontsize=6.6,color=MUTED)
```

::: example Opportunity cost
**Problem.** A student has Rs. 30,000 and three possible uses for it, in order of preference: (i) a computer for study, which he values at Rs. 45,000 of benefit; (ii) a month's coaching class in mathematics, which he values at Rs. 38,000; (iii) a smartphone, which he values at Rs. 32,000. He chooses the computer. Find the opportunity cost of his choice and explain what the figure means.

**Solution.**
Step 1 — Write the ranked list: computer (Rs. 45,000), coaching (Rs. 38,000), smartphone (Rs. 32,000).
Step 2 — Apply the rule. Opportunity cost is the value of the **next best** alternative forgone — not the sum of all the alternatives, and not the price paid.
Step 3 — The next best alternative is the coaching class, valued at Rs. 38,000.
Step 4 — The smartphone is not part of the opportunity cost, because it is not the next best use.

**Answer.** Opportunity cost = **Rs. 38,000** (the coaching class given up), not Rs. 32,000 + Rs. 38,000 = Rs. 70,000 and not Rs. 30,000.
**What it means.** The cost of a decision is measured by the best thing you did not do. Note also that the money paid (Rs. 30,000) is the *accounting* cost; the Rs. 38,000 is the *economic* cost, and it is larger because it includes the benefit forgone.
:::

::: example Allocating a fixed budget
**Problem.** A municipality has Rs. 60 lakh to spend and four competing proposals: a health post (benefit to the community valued at Rs. 90 lakh), a school building (Rs. 75 lakh), a park (Rs. 40 lakh) and a new office vehicle (Rs. 25 lakh). Each proposal needs the whole of the health post's share — the budget can pay for the health post and one other small item, or for two or three of the smaller ones, but not all four.
Advise the municipality, and state the opportunity cost of its decision.

**Solution.**
Step 1 — Rank by benefit: health post (90), school (75), park (40), vehicle (25).
Step 2 — Apply the rule of choice under scarcity: take the proposal with the highest benefit first, and continue until the budget is exhausted.
Step 3 — Take the health post (Rs. 60 lakh would be spent on it alone in this illustration) — benefit Rs. 90 lakh.
Step 4 — The opportunity cost of the decision is the benefit of the **next best alternative given up**, which is the school building.
Step 5 — State the principle clearly: the municipality has not "lost" the money; it has decided that Rs. 90 lakh of health benefit is worth more than Rs. 75 lakh of school benefit. The choice is rational, and it still has a cost.

**Answer.** Spend on the health post; opportunity cost = the school building's benefit of Rs. 75 lakh.
**What it means.** Scarcity makes every public decision a comparison of benefits that cannot all be had, which is exactly why a budget has to be prepared and argued over rather than simply spent.
:::

## 1.3 The three central problems of an economy

Every economy, whatever its type, has to solve the same problems. They are called **central** because they arise from scarcity and cannot be avoided.

**1. What to produce, and how much?** Every economy must decide which goods and services — rice or cement, schools or fighter aircraft, luxuries or necessities — shall be produced, and in what quantities. A capitalist economy answers it by consumer demand expressed through prices; a socialist economy by the plan; a mixed economy by both.

**2. How to produce?** The same goods can be made with more labour and less machinery, or more machinery and less labour. A labour-abundant country such as Nepal, with more than a million people looking for work, should choose **labour-intensive** methods where quality permits; a labour-scarce country chooses capital-intensive methods. The choice is also about efficiency: the method that produces a given output at the lowest cost is the technically efficient one.

**3. For whom to produce?** This is the problem of **distribution**. Shall output go to those who can pay the most, or to those who need it most? A capitalist economy distributes by income and ability to pay; a socialist economy by need or by work; a mixed economy by a combination of the wage earned and the state's social policy — taxation, subsidies, free education and health.

To these three modern writers add two more: **how efficiently are the resources being used** (the problem of full employment of resources), and **how fast shall the economy grow** (the problem of growth over time).

## 1.4 Macroeconomic variables

**Microeconomics** studies the individual — one consumer, one firm, one market, one price. **Macroeconomics** studies the economy as a whole and the large totals and averages that describe it. The measures it uses are the **macroeconomic variables**.

| Variable | What it measures |
|---|---|
| **National income (GDP/GNP)** | The market value of all final goods and services produced in a country in a year (GDP); plus net factor income from abroad (GNP) |
| **Per capita income** | National income ÷ population — the average income of one person |
| **Consumption (C)** | Total spending by households on goods and services |
| **Saving (S)** | The part of income not consumed; $S = Y - C$ |
| **Investment (I)** | Spending on new capital — machines, buildings, stocks |
| **Inflation** | A sustained rise in the general price level, measured by the consumer price index |
| **Unemployment** | The number of people able and willing to work who have no work |
| **Money supply** | The total quantity of money in circulation |
| **Balance of payments** | The record of all a country's transactions with the rest of the world — trade, services, remittance, loans |
| **Government revenue and expenditure** | What the government collects and what it spends; the budget deficit is the difference |
| **Population** | The number of people, their growth rate and their structure |

Three relations are worth remembering.

$$National\ income\ (Y) = Consumption\ (C) + Saving\ (S)$$
$$Saving\ (S) = Income\ (Y) - Consumption\ (C)$$
$$Per\ capita\ income = \frac{National\ income}{Population}$$

```figure caption="Microeconomics looks at the tree, macroeconomics at the forest. The same economy is studied at two levels, and the totals of the macro level are the sums of millions of micro decisions."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.9,2.5))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6)
ax.add_patch(FancyBboxPatch((0.3,1.2),4.2,3.6,boxstyle="round,pad=0.08",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(2.4,4.1,"MICROECONOMICS",ha='center',fontsize=7.4,color=INK,weight='bold')
ax.text(2.4,2.7,"One consumer, one firm,\none market, one price\n\nDemand and supply,\ncost, revenue, market\nstructure",ha='center',va='center',fontsize=6.2,color=INK)
ax.add_patch(FancyBboxPatch((5.5,1.2),4.2,3.6,boxstyle="round,pad=0.08",fc="#fdf3f3",ec=SERIES[1],lw=1.2))
ax.text(7.6,4.1,"MACROECONOMICS",ha='center',fontsize=7.4,color=INK,weight='bold')
ax.text(7.6,2.7,"National income, saving,\ninvestment, inflation,\nunemployment, money\nsupply, balance of\npayments, the budget",
        ha='center',va='center',fontsize=6.2,color=INK)
ax.text(5.0,0.5,"The macro totals are the sums of millions of micro decisions",ha='center',fontsize=6.2,color=MUTED)
```

::: example Working with the macro variables
**Problem.** In a certain year a country's gross domestic product was Rs. 4,500 billion, its net factor income from abroad was Rs. 200 billion, its population was 30 million, and its consumption was Rs. 3,300 billion. Find (a) the gross national product, (b) the saving, (c) the per capita income, and (d) the saving rate.

**Solution.**
Step 1 — $GNP = GDP + net\ factor\ income\ from\ abroad = 4{,}500 + 200 = Rs.\ 5{,}200$ billion.
Step 2 — $Saving = Income - Consumption = 4{,}500 - 3{,}300 = Rs.\ 1{,}200$ billion. (Using GDP as the income of the economy for the year.)
Step 3 — $Per\ capita\ income = \frac{National\ income}{Population} = \frac{5{,}200\ billion}{30\ million} = Rs.\ 173{,}333$ per person per year, that is about **Rs. 1,73,333**.
Step 4 — $Saving\ rate = \frac{Saving}{Income} \times 100 = \frac{1{,}200}{4{,}500} \times 100 = 26.67\%$.

**Answer.** GNP Rs. 5,200 billion; saving Rs. 1,200 billion; per capita income Rs. 1,73,333; saving rate 26.67 %.
**What it means.** Per capita income is an *average*: it does not mean that every Nepali earns Rs. 1,73,333. But it is the number used to compare countries, and the saving rate shows how much of the year's income is available to build the factories and roads of the next year.
:::

## 1.5 Circular flow of income in a two-sector economy

In a simple **two-sector economy** there are only **households** and **firms**. The households own the factors of production; the firms buy them and produce goods and services. Money and goods therefore move round in a circle, in two directions at once.

**The real flow (goods and services) and the money flow (income and expenditure) run in opposite directions.**

1. Households supply **land, labour, capital and enterprise** to the firms (real flow).
2. Firms pay **rent, wages, interest and profit** to the households (money flow). This is **factor income**.
3. Households spend that income on the goods and services produced by the firms (money flow in the opposite direction).
4. Firms receive **sales revenue**, with which they again pay the factors, and the circle begins again.

The value of what the firms produce equals the income the households receive, equals what the households spend, equals the revenue the firms receive. If nothing is saved and nothing is invested, the circle is complete and the economy reproduces itself year after year.

**When saving and investment are added.** A part of household income may be **saved** instead of spent, and firms may **invest** in new capital. Then the circle has two leaks and two injections:

$$Y = C + S \qquad \text{and} \qquad Y = C + I \qquad \text{so that in equilibrium} \qquad S = I$$

Saving is a **leak** from the flow — money that leaves the circle of spending. Investment is an **injection** — money that a firm puts into buying capital goods, which returns to the households as income. The economy is in equilibrium when the leak equals the injection, that is, when saving equals investment. If investment is greater than saving, the level of income and employment tends to rise; if saving is greater than investment, it tends to fall.

```figure caption="The circular flow in a two-sector economy. The inner arrows carry goods and services; the outer arrows carry money. Saving leaks out and investment injects back in."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.1))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.add_patch(FancyBboxPatch((0.4,4.2),3.0,2.2,boxstyle="round,pad=0.07",fc="#eaf1ff",ec=ACCENT,lw=1.2))
ax.text(1.9,5.3,"HOUSEHOLDS",ha='center',va='center',fontsize=8,color=INK,weight='bold')
ax.add_patch(FancyBboxPatch((6.6,4.2),3.0,2.2,boxstyle="round,pad=0.07",fc="#fdf3f3",ec=SERIES[1],lw=1.2))
ax.text(8.1,5.3,"FIRMS",ha='center',va='center',fontsize=8,color=INK,weight='bold')
ax.add_patch(FancyArrowPatch((3.5,6.65),(6.5,6.65),arrowstyle="-|>",mutation_scale=11,color=ACCENT,lw=1.3))
ax.text(5.0,7.15,"Factor services: land, labour, capital, enterprise",ha='center',fontsize=6.2,color=ACCENT)
ax.add_patch(FancyArrowPatch((6.5,5.85),(3.5,5.85),arrowstyle="-|>",mutation_scale=11,color=SERIES[1],lw=1.3))
ax.text(5.0,5.35,"Factor income: rent, wages, interest, profit",ha='center',fontsize=6.2,color=SERIES[1])
ax.add_patch(FancyArrowPatch((3.5,4.55),(6.5,4.55),arrowstyle="-|>",mutation_scale=11,color=ACCENT,lw=1.3))
ax.text(5.0,4.05,"Consumption expenditure on goods and services",ha='center',fontsize=6.2,color=ACCENT)
ax.add_patch(FancyArrowPatch((6.5,3.75),(3.5,3.75),arrowstyle="-|>",mutation_scale=11,color=SERIES[1],lw=1.3))
ax.text(5.0,3.25,"Goods and services supplied to households",ha='center',fontsize=6.2,color=SERIES[1])
ax.add_patch(FancyBboxPatch((0.4,0.5),3.4,1.5,boxstyle="round,pad=0.06",fc="#f6f8fc",ec=MUTED,lw=1.1))
ax.text(2.1,1.25,"SAVING\\n(leak)",ha='center',va='center',fontsize=6.6,color=INK)
ax.add_patch(FancyBboxPatch((6.2,0.5),3.4,1.5,boxstyle="round,pad=0.06",fc="#f6f8fc",ec=MUTED,lw=1.1))
ax.text(7.9,1.25,"INVESTMENT\\n(injection)",ha='center',va='center',fontsize=6.6,color=INK)
ax.add_patch(FancyArrowPatch((1.9,4.15),(1.9,2.05),arrowstyle="-|>",mutation_scale=9,color=MUTED,lw=1.0))
ax.add_patch(FancyArrowPatch((8.1,2.05),(8.1,4.15),arrowstyle="-|>",mutation_scale=9,color=MUTED,lw=1.0))
ax.text(5.0,1.25,"Equilibrium when S = I",ha='center',fontsize=6.6,color=INK)
```

::: example The circular flow figures
**Problem.** In a two-sector economy, households receive Rs. 800 crore of factor income, consume Rs. 680 crore and save the rest. Firms invest Rs. 140 crore. Find (a) the total income, (b) the consumption, (c) the saving, (d) whether the economy is in equilibrium and, if not, in which direction income will tend to move.

**Solution.**
Step 1 — Total income $Y = Rs.\ 800$ crore.
Step 2 — Consumption $C = Rs.\ 680$ crore (given).
Step 3 — Saving $S = Y - C = 800 - 680 = Rs.\ 120$ crore.
Step 4 — Investment $I = Rs.\ 140$ crore (given).
Step 5 — Compare: $S = 120 < I = 140$. The injection is larger than the leak.
Step 6 — Where they are unequal, the total demand for goods (consumption plus investment) is greater than the total income, so firms sell more than they expected, and they respond by producing more and employing more. Income and employment will therefore **tend to rise**.

**Answer.** (a) Rs. 800 crore, (b) Rs. 680 crore, (c) Rs. 120 crore, (d) not in equilibrium — investment exceeds saving, so income and employment tend to rise until saving rises to meet investment.
**What it means.** The whole of macroeconomics rests on this identity. A government that wants to raise income can raise investment, or lower saving by taxing and spending, or encourage households to consume more — and it can see the effect in the circular flow.
:::

::: caution The common mistake
Opportunity cost is very often answered as "the money spent on the thing we chose" or "the total of all the things we gave up". Both are wrong. Opportunity cost is the value of **the next best alternative alone**. The money paid is the *accounting* or *explicit* cost; the benefit forgone is the *implicit* or *economic* cost. Another frequent error is to call Nepal a capitalist or a socialist economy: Nepal is a **mixed** economy, with both a private and a public sector.
:::

## Chapter summary

- An **economy** is the organised system by which a country produces, distributes and consumes goods and services to satisfy its wants with limited resources.
- A **capitalist economy** has private ownership, freedom of enterprise, the profit motive, consumer sovereignty and the price mechanism; it is efficient but unequal. A **socialist economy** has public ownership and central planning and is equal but often inefficient. A **mixed economy** has both sectors, the market taking many decisions and the state taking others; **Nepal is a mixed economy**.
- **Scarcity** means resources are limited relative to wants. It forces **choice**; the cost of choice is **opportunity cost**, the value of the next best alternative forgone — not the money paid and not the sum of all alternatives.
- The **factors of production** are land (rent), labour (wages), capital (interest) and entrepreneurship (profit).
- **Allocation of resources** is decided by the price mechanism in a capitalist economy, by the central plan in a socialist economy, and by both in a mixed economy.
- The **three central problems** are what to produce, how to produce and for whom to produce; modern writers add full employment of resources and growth.
- **Microeconomics** studies one consumer, firm or market; **macroeconomics** studies the economy as a whole through its **variables** — national income, per capita income, consumption, saving, investment, inflation, unemployment, money supply, the balance of payments, government revenue and expenditure and population.
- $Y = C + S$, so $S = Y - C$; and $Per\ capita\ income = \frac{National\ income}{Population}$.
- In the **circular flow** of a two-sector economy, households supply factor services and receive factor income, and spend it on the firms' output; the real and money flows run in opposite directions. **Saving** is a leak and **investment** an injection, and the economy is in equilibrium when **S = I**. If investment exceeds saving, income and employment tend to rise.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is an economy? <span class="marks">[1]</span>
2. Write any two features of a capitalist economy. <span class="marks">[1]</span>
3. What is a mixed economy? <span class="marks">[1]</span>
4. What is scarcity? <span class="marks">[1]</span>
5. Define opportunity cost. <span class="marks">[1]</span>
6. Write any two factors of production with their rewards. <span class="marks">[1]</span>
7. What is allocation of resources? <span class="marks">[1]</span>
8. Write any two central problems of an economy. <span class="marks">[1]</span>
9. Write any two macroeconomic variables. <span class="marks">[1]</span>
10. What is per capita income? <span class="marks">[1]</span>
11. What is meant by the circular flow of income? <span class="marks">[1]</span>

::: note Answers to Group A
**1.** An economy is the organised system by which the people of a country produce goods and services, distribute them and consume them, in order to satisfy their wants with limited resources.
**2.** Any two of: private ownership of the means of production; freedom of enterprise; profit motive; consumer sovereignty; price mechanism; competition; limited role of government.
**3.** A mixed economy is one in which the private sector and the public sector exist side by side, with the market taking many decisions and the state taking others and regulating the rest; Nepal is a mixed economy.
**4.** Scarcity means that the resources available to satisfy human wants are limited in supply relative to the wants for them.
**5.** Opportunity cost is the value of the next best alternative forgone when a choice is made.
**6.** Land — rent; labour — wages; capital — interest; entrepreneurship — profit. (Any two.)
**7.** Allocation of resources is the process of deciding how much of each factor of production shall be used, and where, to produce the goods and services the society wants.
**8.** Any two of: what to produce and how much; how to produce; for whom to produce.
**9.** Any two of: national income, per capita income, consumption, saving, investment, inflation, unemployment, money supply, balance of payments, government revenue and expenditure, population.
**10.** Per capita income is the national income of a country divided by its population — the average income of one person in a year.
**11.** The circular flow of income is the continuous movement of factor services and goods from households to firms and back, and of income and expenditure from firms to households and back, in a two-sector economy.
:::

**Group B — Short answer (5 marks each)**

1. What is a capitalist economy? Explain its main features. <span class="marks">[5]</span>
2. Distinguish between a capitalist, a socialist and a mixed economy. <span class="marks">[5]</span>
3. What is scarcity? Explain the relation between scarcity, choice and opportunity cost with an example. <span class="marks">[5]</span>
4. Explain the three central problems of an economy. <span class="marks">[5]</span>
5. What is meant by the allocation of resources? How are resources allocated in a capitalist and in a socialist economy? <span class="marks">[5]</span>
6. Explain the circular flow of income in a two-sector economy. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definition: an economy in which the means of production are owned and operated by private individuals for profit and production is guided by the price mechanism. Features: private ownership; freedom of enterprise; profit motive; consumer sovereignty; the price mechanism allocating resources; competition among producers; freedom of choice in occupation and consumption; and a limited role for government. Merits: efficiency, consumer satisfaction, innovation, variety. Demerits: inequality, unemployment in depression, production of luxuries, monopoly and social costs such as pollution.
**2.** *Capitalist*: resources privately owned; decisions by the market and prices; distribution by ability to pay; efficient but unequal. *Socialist*: resources owned by the state; decisions by the central plan; distribution by need or work; equal but often inefficient and with less consumer choice. *Mixed*: both private and public sectors; decisions shared between the market and the state; distribution by wages tempered by social policy; the aim is to keep the market's efficiency while curing its inequality and instability. Nepal is a mixed economy.
**3.** Scarcity means resources are limited relative to wants. Because they are limited, a choice must be made between alternative uses; and because a choice is made, something is given up. That which is given up is the opportunity cost — the value of the next best alternative forgone. Example: a student with Rs. 30,000 can buy a computer, join a coaching class or buy a smartphone; if he buys the computer and the coaching class was the next best use, the opportunity cost is the value of the coaching class.
**4.** (i) *What to produce and how much* — which goods and services, and in what quantities (rice or cement, schools or aircraft); answered by prices in a capitalist economy. (ii) *How to produce* — the technique: labour-intensive or capital-intensive; the method that produces a given output at the lowest cost is technically efficient. (iii) *For whom to produce* — distribution: by ability to pay, by need or by work. Modern writers add the full utilisation of resources and the growth of the economy over time.
**5.** Allocation of resources is the process of deciding how much of each factor of production is used, and where, to produce what society wants. In a **capitalist** economy it is done by the **price mechanism**: a rise in the price of a good that is in demand raises the profit from making it, and land, labour and capital move into that line by themselves. In a **socialist** economy it is done by the **central plan**: the planning authority decides in physical quantities how much of each good shall be produced and directs the resources accordingly.
**6.** In a two-sector economy there are households and firms. Households own the factors of production and supply factor services to firms; firms pay rent, wages, interest and profit as factor income. Households spend that income on the goods and services the firms produce; firms receive sales revenue and pay the factors again. The real flow and the money flow run in opposite directions, and the value of output equals income equals expenditure. When saving and investment are added, saving is a leak and investment an injection, and equilibrium requires **S = I**; if investment exceeds saving, income and employment tend to rise.
:::

**Group C — Long answer (8 marks each)**

1. Explain the types of economy and their features, merits and demerits, and state which type Nepal follows. <span class="marks">[8]</span>
2. What is an economy? Explain scarcity, choice, opportunity cost and the allocation of resources, and show with an example how opportunity cost is measured. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Types and features (6).* Capitalist economy — private ownership, freedom of enterprise, profit motive, consumer sovereignty, price mechanism, competition, limited government; merits: efficiency, consumer satisfaction, innovation, variety; demerits: inequality, unemployment, luxury production, monopoly, social costs. Socialist economy — public ownership, central planning, no profit motive, equality, little competition; merits: equality, resource direction to social needs, no unemployment, big projects; demerits: inefficiency, less consumer choice, weak initiative, planning errors. Mixed economy — private and public sectors together, decisions shared between the market and the state, regulation of monopoly, taxation and public expenditure to reduce inequality; merits: combines efficiency with social justice; demerits: it can combine the weaknesses of both and regulation can be slow.
*Nepal (2).* Nepal follows a **mixed economy**. The constitution and the law protect private property and private enterprise — industry, trade, banking, tourism and agriculture are largely private — while the state operates railways, drinking water, part of the power sector and most education and health services, and directs the economy through the budget, monetary policy, taxation and subsidies.
**2.** *Economy (1).* Definition as in Group A answer 1.
*Scarcity (2).* Resources are limited relative to wants; scarcity exists even when a thing is physically plentiful, because at a zero price more would be wanted than exists — as with land in Kathmandu or clean water in the dry season.
*Choice and opportunity cost (3).* Scarcity forces choice between alternatives; the cost of the choice is the opportunity cost, the value of the next best alternative forgone. It is the economic cost, and it is not the same as the money paid (the accounting cost) nor the total of all the alternatives given up. Example: a family with Rs. 40,000 ranks a scooter, a year's tuition and a television; if it chooses the scooter, the opportunity cost is the tuition, not the tuition plus the television.
*Allocation of resources (2).* Deciding how much of each factor to use and where: by the price mechanism in a capitalist economy, by the central plan in a socialist economy, and by both in a mixed economy such as Nepal, where the market allocates consumer goods while the state allocates through the budget to roads, education, health and defence and steers the rest by policy.
:::

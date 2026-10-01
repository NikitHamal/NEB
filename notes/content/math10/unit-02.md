---
subject: Mathematics
grade: 10
unit: 2
title: Tax and Money Exchange
hours: 0
area: Compulsory Mathematics
---

Every time you buy a packet of biscuits in a shop in Kathmandu, part of the price goes to the government as tax. Every time a migrant worker in Qatar sends money home, one currency is changed into another at a rate fixed by the bank. This chapter turns both everyday ideas into arithmetic: **value added tax (VAT)**, **excise duty**, **income tax**, and **foreign currency exchange**. All of it rests on one skill from earlier classes — finding a percentage of a quantity, and working backwards from a total to the original amount.

::: key What the SEE asks from this chapter
Almost every SEE paper has one 4-mark question from this unit and often a 3-mark one. The common types are: (i) **a bill with discount and VAT**; (ii) **a price with excise duty and then VAT**, sometimes worked backwards; (iii) **income tax by slabs**; (iv) **converting currencies at a buying or selling rate**, including gain or loss. Show the rate, the working and a final sentence with the unit (Rs, USD, INR).
:::

## 2.1 Tax and Money Exchange: concepts, formulas and worked problems

### Taxes: what they are and why we pay them

A **tax** is money that people and businesses must pay to the government. It pays for roads, schools, hospitals and the police. Taxes fall into two groups.

| Kind of tax | Who bears it | Examples |
|---|---|---|
| **Direct tax** | Paid straight to the government by the person whose income or property is taxed | Income tax, property tax |
| **Indirect tax** | Added to the price of goods or services; the buyer pays it through the seller | VAT, excise duty, customs duty |

In Nepal the standard rate of VAT is **13%**. Rates and slabs are changed by the government each year in the Finance Act, so in an exam you must use the rate **given in the question**. If a question says nothing, the textbook rate is 13%.

### Value added tax (VAT)

::: definition Value added tax (VAT)
**VAT** is a tax on the value added at each stage of production and sale, collected by the seller from the buyer and paid to the government. The price **before** VAT is the taxable price; the price **after** adding VAT is the bill amount.
:::

With VAT rate $r\%$:

::: key VAT formulas
$$ \text{VAT} = \frac{r}{100}\times \text{price without VAT} $$
$$ \text{Bill amount} = \text{price without VAT} + \text{VAT} = \text{price without VAT}\times\left(1+\frac{r}{100}\right) $$
$$ \text{Price without VAT} = \frac{\text{Bill amount}}{1+\dfrac{r}{100}} $$

For $r=13$: bill $=1.13\times$ price, so price $=$ bill $\div\, 1.13$.
:::

::: example Adding VAT to a price
**Problem.** A school bag is priced at Rs 2,500 without VAT. Find the VAT at 13% and the amount a customer pays.

**Solution.** VAT $=\dfrac{13}{100}\times 2500 = \text{Rs } 325$.

Bill amount $=2500+325=\text{Rs } 2{,}825$.

(Quick method: $2500\times 1.13=2825$ ✓.)
:::

::: example Finding the price from the bill
**Problem.** A customer paid Rs 9,040 for a pair of shoes including 13% VAT. Find the price before VAT and the VAT amount.

**Solution.** Let the price without VAT be Rs $x$. Then

$$ x\times 1.13 = 9040 \;\Rightarrow\; x = \frac{9040}{1.13} = 8000 $$

Price without VAT $=\text{Rs } 8{,}000$. VAT $=9040-8000=\text{Rs } 1{,}040$.

Check: $13\%$ of $8000=1040$ ✓.
:::

::: caution Do not take 13% of the bill
When the **bill amount** is given, the VAT is **not** $13\%$ of the bill. 13% of Rs 9,040 is Rs 1,175.20, which is wrong. The 13% is on the price **without VAT**, so divide the bill by 1.13 first.
:::

### Discount and VAT together

A shopkeeper first gives the **discount** on the marked price, and VAT is then charged on the **discounted price** (the actual selling price). The order matters.

**Order:** marked price → subtract discount → selling price → add VAT → bill amount.

::: example Discount, then VAT
**Problem.** The marked price of a jacket is Rs 15,000. The shopkeeper allows a 20% discount and charges 13% VAT. Find the amount the customer pays.

**Solution.** Discount $=20\%$ of $15000=\text{Rs } 3{,}000$.

Selling price $=15000-3000=\text{Rs } 12{,}000$.

VAT $=13\%$ of $12000=\text{Rs } 1{,}560$.

Bill amount $=12000+1560=\text{Rs } 13{,}560$.
:::

::: example Profit, discount and VAT
**Problem.** A shopkeeper buys an article for Rs 8,000. He marks it 25% above the cost price, gives a 10% discount and then charges 13% VAT. How much does the customer pay?

**Solution.** Marked price $=8000\times 1.25=\text{Rs } 10{,}000$.

Discount $=10\%$ of $10000=\text{Rs } 1{,}000$, so selling price $=\text{Rs } 9{,}000$.

VAT $=13\%$ of $9000=\text{Rs } 1{,}170$.

Customer pays $9000+1170=\text{Rs } 10{,}170$.
:::

### How VAT moves along the chain

VAT is called "value added" because each seller pays the government only the tax on **the value he or she added**. A seller collects VAT from the buyer, subtracts the VAT already paid to his own supplier, and pays the difference.

::: derivation Why the total VAT equals 13% of the final price
We start with a product that passes from a manufacturer to a wholesaler to a retailer to a customer. We show that the government's total receipts equal 13% of the final selling price, so the burden falls on the customer alone.

**Setting up.** Prices exclude VAT: manufacturer sells at Rs 1,000, wholesaler at Rs 1,500, retailer at Rs 2,000. VAT rate is 13%.

**Step 1 — manufacturer.** VAT collected $=13\%$ of $1000=130$. No earlier VAT to deduct, so pays Rs 130.

**Step 2 — wholesaler.** VAT collected $=13\%$ of $1500=195$. VAT already paid to the manufacturer $=130$. Pays $195-130=\text{Rs } 65$.

**Step 3 — retailer.** VAT collected $=13\%$ of $2000=260$. VAT already paid to the wholesaler $=195$. Pays $260-195=\text{Rs } 65$.

**Step 4 — total to the government.**

$$ 130 + 65 + 65 = 260 = 13\%\text{ of } 2000 $$

**Result.** The government receives exactly VAT on the final price. Each seller recovers the VAT paid on purchases, so the tax is finally paid by the customer.

**What it means.** Each person in the chain pays VAT only on his own profit margin: $13\%$ of $(1500-1000)=65$ and $13\%$ of $(2000-1500)=65$.
:::

```figure caption="VAT along a supply chain (prices without VAT). Each seller pays only the VAT on the value he adds; the three payments add up to 13% of the final price."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.8))
stages = ['Manufacturer', 'Wholesaler', 'Retailer']
paid = [130, 65, 65]
cum = [0, 130, 195]
for i, (p, c) in enumerate(zip(paid, cum)):
    ax.bar(i, p, bottom=c, color=SERIES[i], width=0.55)
    ax.text(i, c + p/2, 'Rs %d' % p, ha='center', va='center', color='white', fontsize=8.5, fontweight='bold')
ax.text(0, 140, 'sells at Rs 1,000', ha='center', va='bottom', fontsize=7.5, color=MUTED)
ax.text(1, 205, 'sells at Rs 1,500', ha='center', va='bottom', fontsize=7.5, color=MUTED)
ax.text(2, 265, 'sells at Rs 2,000', ha='center', va='bottom', fontsize=7.5, color=MUTED)
ax.axhline(260, color=INK, lw=0.8, ls='--')
ax.text(-0.5, 266, 'total VAT = Rs 260', ha='left', va='bottom', fontsize=8, color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(stages, fontsize=8.5)
ax.set_ylabel('cumulative VAT (Rs)', fontsize=8.5)
ax.set_ylim(0, 320); ax.set_xlim(-0.6, 2.6)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', color=GRID, lw=0.5)
ax.set_axisbelow(True)
```

::: example VAT payable by a shopkeeper
**Problem.** A shopkeeper buys goods for Rs 40,000 (without VAT) and sells them for Rs 50,000 (without VAT). VAT is 13%. How much VAT must he pay to the government?

**Solution.** VAT collected on sales $=13\%$ of $50000=\text{Rs } 6{,}500$.

VAT paid on purchases $=13\%$ of $40000=\text{Rs } 5{,}200$.

VAT payable $=6500-5200=\text{Rs } 1{,}300$.

Check: $13\%$ of the value added $(50000-40000=10000)$ is $1300$ ✓.
:::

### Excise duty

::: definition Excise duty
**Excise duty** is an indirect tax charged by the government on certain goods produced inside the country (for example cigarettes, alcohol, cars, TVs in many questions). It is charged on the **factory price** (the price at which the producer sells), **before** VAT.
:::

When both apply, the order is fixed:

**Order:** factory price → add excise duty → price with excise → add VAT on this price → final price.

**VAT is charged on the factory price plus the excise duty**, not on the factory price alone. So excise is a tax on which VAT is also charged.

::: key Excise duty and VAT
With excise rate $e\%$ and VAT rate $v\%$:

$$ \text{Final price} = \text{Factory price}\times\left(1+\frac{e}{100}\right)\times\left(1+\frac{v}{100}\right) $$

For $e=10$, $v=13$: final price $=$ factory price $\times 1.1\times 1.13=1.243\times$ factory price.
:::

::: example Excise duty, then VAT
**Problem.** The factory price of a television is Rs 50,000. Excise duty of 15% is charged and then VAT of 13% is added. Find the price a customer pays.

**Solution.** Excise duty $=15\%$ of $50000=\text{Rs } 7{,}500$.

Price with excise duty $=50000+7500=\text{Rs } 57{,}500$.

VAT $=13\%$ of $57500=\text{Rs } 7{,}475$.

Final price $=57500+7475=\text{Rs } 64{,}975$.

Total tax paid $=7500+7475=\text{Rs } 14{,}975$.
:::

```figure caption="Build-up of the television price (Rs). Excise duty is added to the factory price, and VAT is then charged on the sum of the two."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.9))
labels = ['Factory\nprice', 'Excise\nduty 15%', 'VAT 13%', 'Final\nprice']
vals = [50000, 7500, 7475, 64975]
bottoms = [0, 50000, 57500, 0]
cols = [SERIES[0], SERIES[2], SERIES[3], INK]
for i in range(4):
    ax.bar(i, vals[i], bottom=bottoms[i], color=cols[i], width=0.55)
txt = ['50,000', '+7,500', '+7,475', '64,975']
for i in range(4):
    ax.text(i, bottoms[i] + vals[i] + 1200, txt[i], ha='center', va='bottom', fontsize=8.5)
ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=8)
ax.set_ylim(0, 76000)
ax.set_yticks([0, 20000, 40000, 60000]); ax.set_yticklabels(['0', '20,000', '40,000', '60,000'], fontsize=8)
ax.set_ylabel('Rs', fontsize=8.5)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', color=GRID, lw=0.5); ax.set_axisbelow(True)
```

::: example Working backwards from the final price
**Problem.** A motorbike was bought for Rs 74,580 including 10% excise duty on the factory price and 13% VAT. Find the factory price, the excise duty and the VAT.

**Solution.** Let the factory price be Rs $x$.

With excise duty: $1.1x$. After VAT: $1.1x\times 1.13=1.243x$.

$$ 1.243x = 74580 \;\Rightarrow\; x = \frac{74580}{1.243} = 60000 $$

Factory price $=\text{Rs } 60{,}000$.

Excise duty $=10\%$ of $60000=\text{Rs } 6{,}000$, so price with excise $=\text{Rs } 66{,}000$.

VAT $=13\%$ of $66000=\text{Rs } 8{,}580$.

Check: $66000+8580=74580$ ✓.
:::

### Income tax

::: definition Income tax and taxable income
**Income tax** is a direct tax on a person's yearly income. It is not charged on the whole income. Allowed deductions (for example life-insurance premium, provident fund or contributions allowed by the government) are first subtracted, and the remainder is the **taxable income**:

$$ \text{Taxable income} = \text{Total annual income} - \text{Allowed deductions} $$
:::

Income tax is charged by **slabs**: the first part of the taxable income is taxed at a low rate, the next part at a higher rate, and so on. Each rate applies **only to the portion that lies inside its slab**. The table below is an example of the kind a question gives. Always use the slabs stated in your question — they change with each year's Finance Act.

| Slab (taxable income) | Rate: unmarried | Rate: married (couple) |
|---|---|---|
| First Rs 4,00,000 (couple: Rs 4,50,000) | 1% | 1% |
| Next Rs 1,00,000 | 10% | 10% |
| Next Rs 2,00,000 | 20% | 20% |
| Next Rs 13,00,000 | 30% | 30% |

```figure caption="Income tax is charged slab by slab. The slope of the graph is the rate in that slab (unmarried slabs from the table): 1%, then 10%, then 20%."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.8))
x = np.array([0, 4, 5, 7, 8]) 
tax = np.array([0, 4000, 14000, 54000, 54000+0.3*1e5])/1000.0
ax.plot(x, tax, color=ACCENT, lw=2)
ax.plot([4, 5, 7], [4, 14, 54], 'o', color=INK, ms=3.5)
for xi, ti, t in [(4, 4, '4,00,000 → Rs 4,000'), (5, 14, '5,00,000 → Rs 14,000'), (7, 54, '7,00,000 → Rs 54,000')]:
    pass
ax.annotate('Rs 4,000', xy=(4, 4), xytext=(2.7, 14), fontsize=8, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.annotate('Rs 14,000', xy=(5, 14), xytext=(3.5, 34), fontsize=8, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.annotate('Rs 54,000', xy=(7, 54), xytext=(5.3, 62), fontsize=8, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.text(2.0, 6.0, '1%', fontsize=8.5, color=INK, ha='center')
ax.text(4.55, 22, '10%', fontsize=8.5, color=INK, ha='right')
ax.text(6.05, 37, '20%', fontsize=8.5, color=INK, ha='right')
ax.text(7.55, 72, '30%', fontsize=8.5, color=INK, ha='right')
ax.set_xlabel('taxable income (Rs lakh)', fontsize=8.5)
ax.set_ylabel('income tax (Rs thousand)', fontsize=8.5)
ax.set_xlim(0, 8.2); ax.set_ylim(0, 90)
ax.spines[['top','right']].set_visible(False)
ax.grid(color=GRID, lw=0.5); ax.set_axisbelow(True)
```

::: example Income tax of an unmarried employee
**Problem.** Mr. Thapa, an unmarried employee, earns Rs 45,000 every month and also receives one extra month's salary as Dashain allowance. He pays Rs 25,000 as life-insurance premium, which is allowed as a deduction. Using the slabs in the table above, find his income tax for the year.

**Solution.** Annual income $=12\times 45000+45000=\text{Rs } 5{,}85{,}000$.

Taxable income $=585000-25000=\text{Rs } 5{,}60{,}000$.

Slab by slab:

| Portion | Amount | Rate | Tax |
|---|---|---|---|
| First slab | Rs 4,00,000 | 1% | Rs 4,000 |
| Next slab | Rs 1,00,000 | 10% | Rs 10,000 |
| Remaining | Rs 60,000 | 20% | Rs 12,000 |

Total tax $=4000+10000+12000=\text{Rs } 26{,}000$.
:::

::: example Income tax of a married couple
**Problem.** A married couple has a combined taxable income of Rs 8,20,000. Using the "married" slabs (first Rs 4,50,000 at 1%, next Rs 1,00,000 at 10%, next Rs 2,00,000 at 20%, the rest at 30%), find the tax payable.

**Solution.**

- First Rs 4,50,000 at 1% $=\text{Rs } 4{,}500$.
- Next Rs 1,00,000 at 10% $=\text{Rs } 10{,}000$.
- Next Rs 2,00,000 at 20% $=\text{Rs } 40{,}000$.
- Remaining: $820000-(450000+100000+200000)=\text{Rs } 70{,}000$ at 30% $=\text{Rs } 21{,}000$.

Total tax $=4500+10000+40000+21000=\text{Rs } 75{,}500$.
:::

::: example Finding the income from the tax
**Problem.** An unmarried person paid Rs 18,000 as income tax. Using the unmarried slabs, find his taxable income.

**Solution.** Tax on the first two slabs $=4000+10000=\text{Rs } 14{,}000$, for an income of Rs 5,00,000.

The tax is more than this, so the income enters the 20% slab. Remaining tax $=18000-14000=\text{Rs } 4{,}000$.

Income in the 20% slab $=\dfrac{4000}{0.20}=\text{Rs } 20{,}000$.

Taxable income $=500000+20000=\text{Rs } 5{,}20{,}000$.
:::

::: tip Slab method in four lines
Write the slabs in a column; subtract each full slab from the income, taking the remainder to the next slab; multiply each part by its rate; add. Stop when the remainder reaches zero. Never apply the highest rate to the whole income.
:::

### Foreign exchange

Each country has its own currency: Nepal the rupee (Rs or NPR), India the Indian rupee (INR), the USA the dollar (USD), the UK the pound (GBP), Qatar the riyal (QAR). **Foreign exchange** is the exchange of one currency for another. The **exchange rate** is the price of one unit of a foreign currency in the home currency.

Banks and money changers **buy** foreign currency from you at a lower rate and **sell** it to you at a higher rate. The difference is their earning.

| Term | Meaning |
|---|---|
| Buying rate | Rate at which the bank **buys** foreign currency from you (you receive Nepali rupees) |
| Selling rate | Rate at which the bank **sells** foreign currency to you (you pay Nepali rupees) |

The selling rate is always higher than the buying rate.

```figure caption="A money changer buys dollars from you at the lower rate and sells dollars to you at the higher rate. Rates are illustrative."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off')
def box(x, y, w, h, t, col):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05,rounding_size=0.15', fc='white', ec=col, lw=1.4))
    ax.text(x + w/2, y + h/2, t, ha='center', va='center', fontsize=8.5)
box(0.2, 1.7, 2.2, 1.6, 'You', SERIES[0])
box(6.6, 1.7, 3.0, 1.6, 'Bank /\nmoney changer', INK)
ax.annotate('', xy=(6.55, 3.0), xytext=(2.45, 3.0), arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.2))
ax.text(4.5, 3.25, 'you sell USD', ha='center', fontsize=8)
ax.text(4.5, 2.65, 'bank pays buying rate (lower)', ha='center', fontsize=7.5, color=MUTED)
ax.annotate('', xy=(2.45, 2.0), xytext=(6.55, 2.0), arrowprops=dict(arrowstyle='-|>', color=SERIES[3], lw=1.2))
ax.text(4.5, 1.7, 'you buy USD', ha='center', fontsize=8)
ax.text(4.5, 1.1, 'bank charges selling rate (higher)', ha='center', fontsize=7.5, color=MUTED)
ax.text(5.0, 0.55, 'Buying rate < Selling rate', ha='center', fontsize=8.5, fontweight='bold')
```

::: key Currency conversion
- To change **foreign currency into Nepali rupees**: **multiply** by the rate.
- To change **Nepali rupees into foreign currency**: **divide** by the rate.
- To change one foreign currency into another: convert through Nepali rupees (A $\to$ Rs $\to$ B).

Use the **buying rate** when the bank is buying foreign currency from you; use the **selling rate** when you are buying foreign currency from the bank.
:::

For India the rate is fixed: **INR 1 = Rs 1.6**, or **Rs 100 = INR 62.50**.

::: example Selling and buying dollars
**Problem.** A bank's rates are: buying USD 1 = Rs 131.50; selling USD 1 = Rs 132.10. (a) Find how many rupees a tourist gets by selling USD 500. (b) How many dollars can be bought with Rs 66,050?

**Solution.** (a) The bank **buys** dollars, so the buying rate applies:

$$ 500\times 131.50 = \text{Rs } 65{,}750 $$

(b) The bank **sells** dollars, so the selling rate applies:

$$ \frac{66050}{132.10} = \text{USD } 500 $$
:::

::: example Gain or loss in exchange
**Problem.** Using the rates above, Anita buys USD 2,000 and later sells all of them back. Find her loss.

**Solution.** She pays $2000\times 132.10=\text{Rs } 2{,}64{,}200$.

She later receives $2000\times 131.50=\text{Rs } 2{,}63{,}000$.

Loss $=264200-263000=\text{Rs } 1{,}200$.

(Check: Rs $0.60$ difference per dollar $\times\,2000=1200$ ✓.)
:::

::: example Converting between two foreign currencies
**Problem.** USD 1 = Rs 132 and GBP 1 = Rs 165. How many pounds are equal to USD 1,000?

**Solution.** USD 1,000 $=1000\times 132=\text{Rs } 1{,}32{,}000$.

Pounds $=\dfrac{132000}{165}=\text{GBP } 800$.
:::

::: example Nepal and India
**Problem.** A Nepali tourist takes Rs 48,000 to India and changes it into Indian currency (INR 1 = Rs 1.6). He spends INR 18,500 and changes the rest back into Nepali rupees. How many rupees does he get back?

**Solution.** INR received $=\dfrac{48000}{1.6}=\text{INR } 30{,}000$.

Left after spending $=30000-18500=\text{INR } 11{,}500$.

Rupees back $=11500\times 1.6=\text{Rs } 18{,}400$.
:::

::: example Which country is cheaper?
**Problem.** A laptop costs USD 800 in the USA and Rs 1,12,000 in Nepal. If USD 1 = Rs 133, in which country is it cheaper and by how much (in Nepali rupees)?

**Solution.** Price in the USA $=800\times 133=\text{Rs } 1{,}06{,}400$.

Price in Nepal $=\text{Rs } 1{,}12{,}000$.

Difference $=112000-106400=\text{Rs } 5{,}600$.

The laptop is cheaper in the USA by Rs 5,600.
:::

::: example Remittance and commission
**Problem.** A worker in Qatar sends QAR 1,500 each month. If QAR 1 = Rs 36.40, find the monthly amount and the yearly amount in Nepali rupees.

**Solution.** Monthly $=1500\times 36.40=\text{Rs } 54{,}600$.

Yearly $=54600\times 12=\text{Rs } 6{,}55{,}200$.

**Commission.** If a bank charges 1% commission on exchanging USD 600 at the buying rate Rs 131.50, the amount is $600\times 131.50=\text{Rs } 78{,}900$. Commission $=1\%$ of $78900=\text{Rs } 789$, so he receives $78900-789=\text{Rs } 78{,}111$.
:::

::: caution Common exchange mistakes
- Using the selling rate when the bank is buying (or the reverse). Ask: *who is buying the foreign currency?* If the bank is, use the lower (buying) rate.
- Multiplying when you should divide. Rupees to dollars is **divide**; dollars to rupees is **multiply**.
- Forgetting the unit. Always write Rs, USD, INR or GBP.
:::

## 2.2 Exercises of the SEE type

### Checklist for tax problems

1. Read the **order** of operations: marked price → discount → VAT, or factory price → excise → VAT.
2. Excise duty is on the factory price; VAT is on the price **including** excise.
3. For a backward problem, write final price $=$ factory price $\times 1.1\times 1.13$ (or the given rates) and divide.
4. For income tax, subtract deductions first, then fill the slabs in order.

### Checklist for exchange problems

1. Identify the rate and whether the bank is buying or selling.
2. Foreign to Nepali: multiply. Nepali to foreign: divide.
3. For two foreign currencies, go through Nepali rupees.
4. For gain or loss, find the cost and the receipt, then subtract.

## Chapter summary

- VAT $=\frac{r}{100}\times$ price; bill $=$ price $\times(1+\frac{r}{100})$; price $=$ bill $\div(1+\frac{r}{100})$. Nepal's standard rate is 13%.
- Discount is allowed on the marked price first; VAT is charged on the selling price.
- Excise duty is charged on the factory price; VAT is then charged on factory price + excise.
- Final price with excise $e\%$ and VAT $v\%$: factory $\times(1+\frac{e}{100})(1+\frac{v}{100})$.
- A seller pays VAT collected on sales minus VAT paid on purchases.
- Taxable income $=$ total income $-$ allowed deductions; tax is charged slab by slab at each slab's rate.
- Foreign to rupees: multiply by the rate; rupees to foreign: divide. The bank's buying rate is lower than its selling rate.
- INR 1 = Rs 1.6; convert one foreign currency to another through rupees.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The bill for an article of price Rs 1,000 with 13% VAT is <span class="marks">[1]</span>
   (a) Rs 1,013 (b) Rs 1,130 (c) Rs 1,300 (d) Rs 870
2. A bill including 13% VAT is Rs 11,300. The price before VAT is <span class="marks">[1]</span>
   (a) Rs 9,831 (b) Rs 10,000 (c) Rs 9,830 (d) Rs 10,300
3. If USD 1 = Rs 132, then USD 50 equals <span class="marks">[1]</span>
   (a) Rs 2,640 (b) Rs 6,600 (c) Rs 660 (d) Rs 13,200
4. A tax charged by the government on goods produced in the country, on the factory price, is called <span class="marks">[1]</span>
   (a) income tax (b) customs duty (c) excise duty (d) property tax
5. A bank's buying rate of foreign currency is <span class="marks">[1]</span>
   (a) equal to its selling rate (b) lower than its selling rate (c) higher than its selling rate (d) always Rs 100

::: note Answers to Group A
**1.** (b) — $1000\times 1.13=1130$.
**2.** (b) — $11300\div 1.13=10000$.
**3.** (b) — $50\times 132=6600$.
**4.** (c) — excise duty is charged on factory price.
**5.** (b) — banks buy low and sell high.
:::

**Group B — Short answer (2 marks each)**

1. Find the VAT at 13% on goods worth Rs 8,000. <span class="marks">[2]</span>
2. The price of a radio including 13% VAT is Rs 6,780. Find its price without VAT. <span class="marks">[2]</span>
3. Convert USD 250 into Nepali rupees if USD 1 = Rs 133. <span class="marks">[2]</span>
4. Convert Rs 24,000 into Indian currency if INR 1 = Rs 1.6. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** VAT $=\frac{13}{100}\times 8000=\text{Rs } 1{,}040$.
**2.** Price $=6780\div 1.13=\text{Rs } 6{,}000$.
**3.** $250\times 133=\text{Rs } 33{,}250$.
**4.** $24000\div 1.6=\text{INR } 15{,}000$.
:::

**Group C — Short answer (3 marks each)**

1. The marked price of a watch is Rs 12,000. A discount of 15% is given and 13% VAT is charged. Find the amount to be paid. <span class="marks">[3]</span>
2. A shopkeeper buys a fan for Rs 5,650 including 13% VAT and sells it at a price of Rs 6,000 without VAT. Find the VAT he pays to the government. <span class="marks">[3]</span>
3. Using the unmarried slabs of this chapter (4,00,000 at 1%, next 1,00,000 at 10%, next 2,00,000 at 20%), find the income tax on a taxable income of Rs 6,00,000. <span class="marks">[3]</span>
4. USD 1 = Rs 132.50. A man has Rs 53,000. How many dollars can he buy? <span class="marks">[3]</span>

::: note Answers to Group C
**1.** Discount $=15\%$ of $12000=1800$, so selling price $=10{,}200$. VAT $=13\%$ of $10200=1326$. Amount $=10200+1326=\text{Rs } 11{,}526$.
**2.** Price without VAT of purchase $=5650\div 1.13=5000$, VAT paid $=650$. VAT collected on sale $=13\%$ of $6000=780$. VAT payable $=780-650=\text{Rs } 130$.
**3.** First Rs 4,00,000 at 1% $=4000$. Next Rs 1,00,000 at 10% $=10000$. Remaining Rs 1,00,000 at 20% $=20000$. Tax $=4000+10000+20000=\text{Rs } 34{,}000$.
**4.** $53000\div 132.50=\text{USD } 400$.
:::

**Group D — Long answer (4 marks each)**

1. The factory price of a refrigerator is Rs 80,000. Excise duty of 10% is charged and then 13% VAT. Find the price a customer pays and the total tax. <span class="marks">[4]</span>
2. A customer paid Rs 1,24,300 for a machine including 10% excise duty on the factory price and 13% VAT. Find the factory price, the excise duty and the VAT. <span class="marks">[4]</span>
3. A married couple has a monthly salary of Rs 60,000 and pays Rs 20,000 yearly as insurance premium (allowed as deduction). Slabs: first Rs 4,50,000 at 1%, next Rs 1,00,000 at 10%, next Rs 2,00,000 at 20%. Find the yearly income tax. <span class="marks">[4]</span>
4. A traveller changes Rs 3,30,000 into USD at the selling rate Rs 132 per USD. On returning, he has USD 400 left and sells them at the buying rate Rs 131 per USD. How much did the trip cost him (in Nepali rupees)? <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Excise $=10\%$ of $80000=8000$, price with excise $=88{,}000$. VAT $=13\%$ of $88000=11440$. Customer pays $88000+11440=\text{Rs } 99{,}440$. Total tax $=8000+11440=\text{Rs } 19{,}440$.
**2.** Let factory price be $x$: $1.1x\times 1.13=1.243x=124300$, so $x=\text{Rs } 1{,}00{,}000$. Excise $=\text{Rs } 10{,}000$, price with excise $=1{,}10{,}000$, VAT $=13\%$ of $110000=\text{Rs } 14{,}300$. Check: $110000+14300=124300$ ✓.
**3.** Annual income $=60000\times 12=7{,}20{,}000$. Taxable $=720000-20000=\text{Rs } 7{,}00{,}000$. Tax: $4{,}50{,}000\times 1\%=4500$; $1{,}00{,}000\times 10\%=10000$; remaining $700000-550000=1{,}50{,}000$ at $20\%=30000$. Total $=4500+10000+30000=\text{Rs } 44{,}500$.
**4.** USD bought $=330000\div 132=2500$. He sells 400 USD for $400\times 131=\text{Rs } 52{,}400$. Cost of trip $=330000-52400=\text{Rs } 2{,}77{,}600$.
:::

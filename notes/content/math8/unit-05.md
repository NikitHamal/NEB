---
subject: Mathematics
grade: 8
unit: 5
title: Profit and Loss
hours: 0
area: Compulsory Mathematics
---

Every shopkeeper in your bazaar is doing this chapter in their head all day:
buy at one price, sell at another, and hope the difference covers the rent. The
mathematics is short — four formulas — but the words matter, because profit
percent is always measured against the **cost** while discount percent is always
measured against the **marked price**. Mixing those two up is the classic
mistake of this unit.

::: key What this chapter asks of you
You should be able to find profit or loss and express it as a percentage of the
cost price, find the selling price or cost price from a given percentage,
calculate a discount and a marked price, and work out commission.
:::

## 5.1 Cost price, selling price, profit and loss

- **Cost price (CP)** is the price at which an article is bought, including any
  expense of bringing it.
- **Selling price (SP)** is the price at which it is sold.
- If SP $>$ CP, the difference is **profit**: $\text{profit}=\text{SP}-\text{CP}$.
- If SP $<$ CP, the difference is **loss**: $\text{loss}=\text{CP}-\text{SP}$.

Percentages are always measured against the cost price:

$$\text{profit percent}=\frac{\text{SP}-\text{CP}}{\text{CP}}\times100\%$$

$$\text{loss percent}=\frac{\text{CP}-\text{SP}}{\text{CP}}\times100\%$$

Rearranged, these let you find a price from a percentage:

$$\text{SP}=\text{CP}\left(1+\frac{\text{profit}\%}{100}\right),\qquad
\text{SP}=\text{CP}\left(1-\frac{\text{loss}\%}{100}\right)$$

$$\text{CP}=\frac{100\times\text{SP}}{100+\text{profit}\%}\qquad\text{or}\qquad
\text{CP}=\frac{100\times\text{SP}}{100-\text{loss}\%}$$

::: tip Which number goes in the denominator?
**Profit and loss percent: cost price. Discount percent: marked price.**
Whatever the question gives as a percentage, the denominator is the price that
percentage was measured against. Write that sentence at the top of your answer
before you start the arithmetic.
:::

::: example Profit percent
**Problem.** A shopkeeper buys a bag for Rs 1,200 and sells it for Rs 1,380.
Find the profit and the profit percent.

**Solution.** Profit $=\text{SP}-\text{CP}=1380-1200=\text{Rs }180$.

$$\text{Profit percent}=\frac{180}{1200}\times100\%=15\%$$

**Answer.** Profit Rs 180; profit percent 15 %.

**Check.** 15 % of 1200 is $0.15\times1200=180$ ✓.
:::

::: example Loss percent and selling price
**Problem.** A trader buys 25 kg of apples at Rs 80 per kg and sells them at a
loss of 12 %. Find the total cost price and the selling price.

**Solution.** $\text{CP}=25\times80=\text{Rs }2000$.

Loss $=12\%$ of $2000=\frac{12}{100}\times2000=\text{Rs }240$.

$$\text{SP}=2000-240=\text{Rs }1760$$

**Answer.** Cost price Rs 2,000; selling price Rs 1,760.

**Check.** $\frac{240}{2000}\times100=12\%$ ✓. Equivalently, SP is 88 % of CP:
$0.88\times2000=1760$ ✓.
:::

::: example Finding the cost price from the selling price
**Problem.** By selling a bicycle for Rs 6,900 a dealer makes a profit of 15 %.
Find the cost price.

**Solution.** Using the formula,

$$\text{CP}=\frac{100\times\text{SP}}{100+\text{profit}\%}
=\frac{100\times6900}{115}=\text{Rs }6000$$

**Answer.** Rs 6,000.

**Check.** 15 % of 6000 is 900, and $6000+900=6900$ ✓.
:::

::: caution Dividing by the wrong number
If a bicycle sold at 15 % profit brings Rs 6,900, the cost price is
$6900\div1.15=6000$ and **not** $6900-15\%$ of 6900 (which is 5,865). The
percentage is measured on the cost, and the cost is the unknown — so the
selling price must be divided, not reduced.
:::

## 5.2 Marked price and discount

Shops do not usually sell at the price printed on the label. The printed price
is the **marked price (MP)**, also called the list price, and the reduction
allowed is the **discount**.

$$\text{discount}=\text{MP}-\text{SP}$$

$$\text{discount percent}=\frac{\text{discount}}{\text{MP}}\times100\%$$

$$\text{SP}=\text{MP}\left(1-\frac{\text{discount}\%}{100}\right)$$

A discount is measured on the marked price, while profit and loss are measured
on the cost price. A sale can therefore show a big discount and still be
profitable, which is exactly what shopkeepers rely on.

```figure caption="The two percentages act on different bases. The discount comes off the marked price; profit or loss is then measured from the marked price down to the cost price."
fig, ax = plt.subplots(figsize=(5.0, 2.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")
ax.annotate("", xy=(0.6, 4.1), xytext=(9.4, 4.1),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(5.0, 4.45, "marked price (MP)", ha="center", fontsize=7.0, color=INK)
ax.plot([2.2, 2.2], [1.6, 4.0], color=SERIES[1], lw=1.6)
ax.plot([2.2, 9.4], [1.6, 1.6], color=SERIES[1], lw=1.6)
ax.text(5.8, 1.15, "selling price (SP) = MP - discount", ha="center", fontsize=6.8,
        color=SERIES[1])
ax.plot([0.6, 0.6], [0.4, 4.0], color=ACCENT, lw=1.6)
ax.plot([0.6, 2.2], [0.4, 0.4], color=ACCENT, lw=1.6)
ax.text(1.4, 0.0, "cost price (CP)", ha="center", fontsize=6.8, color=ACCENT)
ax.text(0.75, 2.6, "discount", ha="left", fontsize=6.6, color=MUTED, rotation=90,
        va="center")
ax.text(2.35, 2.6, "profit or\\nloss", ha="left", fontsize=6.6, color=MUTED)
fig.tight_layout()
```

::: example A sale with a discount
**Problem.** The marked price of a jacket is Rs 3,200 and a discount of 20 % is
allowed. Find the selling price. If the shopkeeper had bought it for Rs 2,000,
find his profit percent.

**Solution.** Discount $=20\%$ of $3200=\frac{20}{100}\times3200=\text{Rs }640$.

$$\text{SP}=3200-640=\text{Rs }2560$$

Profit $=2560-2000=\text{Rs }560$.

$$\text{Profit percent}=\frac{560}{2000}\times100\%=28\%$$

**Answer.** Selling price Rs 2,560; profit 28 %.

**Check.** SP is 80 % of MP: $0.8\times3200=2560$ ✓. And
$2560:2000=1.28$, which is a 28 % profit on the cost ✓. Note that a 20 %
discount still left a 28 % profit — the two percentages are on different bases.
:::

::: example Finding the marked price
**Problem.** After a discount of 15 %, a watch sells for Rs 2,125. Find its
marked price.

**Solution.** $\text{SP}=85\%$ of MP, so

$$\text{MP}=\frac{2125\times100}{85}=\text{Rs }2500$$

**Answer.** Rs 2,500.

**Check.** 15 % of 2500 is 375, and $2500-375=2125$ ✓.
:::

## 5.3 Commission

A **commission** is a payment to an agent for selling something on someone
else's behalf, and it is a percentage of the sale value.

$$\text{commission}=\frac{\text{rate}\%}{100}\times\text{sale value}$$

::: example An agent's commission
**Problem.** An agent sells a plot of land for Rs 18,00,000 and charges a
commission of 2 %. How much does the owner receive?

**Solution.** Commission
$=\frac{2}{100}\times18\,00\,000=\text{Rs }36\,000$.

The owner receives $18\,00\,000-36\,000=\text{Rs }17\,64\,000$.

**Answer.** Commission Rs 36,000; the owner receives Rs 17,64,000.

**Check.** $17\,64\,000+36\,000=18\,00\,000$ ✓.
:::

## 5.5 Marked price, discount and VAT in order

The order of operations is where most marks are lost: **discount comes off the
marked price, VAT goes on to what is left.**

```figure caption="A Rs 2,000 article at 10% discount and 13% VAT. Notice that the VAT is charged on Rs 1,800, not on Rs 2,000 — the order changes the final bill."
stages = ["Marked\nprice", "Less 10%\ndiscount", "Plus 13%\nVAT"]
vals = [2000, 1800, 2034]
fig, ax = plt.subplots(figsize=(4.6, 3.0))
bars = ax.bar(stages, vals, color=[SERIES[1], SERIES[0], SERIES[3]],
              width=0.55, edgecolor="white", linewidth=1.1)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 40, f"Rs {v:,}", ha="center",
            color=INK, fontsize=9)
ax.set_ylim(0, 2400)
ax.set_ylabel("rupees", color=MUTED, fontsize=9)
ax.grid(axis="y", color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED, labelsize=8.6)
```

| Quantity | Formula | Always on |
|---|---|---|
| Profit | S.P. $-$ C.P. | — |
| Profit per cent | $\frac{\text{profit}}{\text{C.P.}}\times100$ | cost price |
| Loss per cent | $\frac{\text{loss}}{\text{C.P.}}\times100$ | cost price |
| Discount | $\frac{d}{100}\times \text{M.P.}$ | marked price |
| VAT | $\frac{v}{100}\times \text{(M.P. after discount)}$ | discounted price |

::: example The full chain, in one problem
**Question.** A shopkeeper buys a fan for Rs 3,000, marks it 25 % above cost,
allows a 12 % discount and charges 13 % VAT. Find (i) the marked price
(ii) the price after discount (iii) the amount the customer pays
(iv) the shopkeeper's profit per cent.

**Answer.**
(i) M.P. $= 3000 + 25\%$ of $3000 = 3000 + 750 = $ **Rs 3,750**.
(ii) Discount $= 12\%$ of $3750 = 450$; price after discount $=$ **Rs 3,300**.
(iii) VAT $= 13\%$ of $3300 = 429$; customer pays $=$ **Rs 3,729**.
(iv) The shopkeeper keeps Rs 3,300 (VAT goes to the government), so profit
$= 3300 - 3000 = 300$ and profit per cent $= \frac{300}{3000}\times100 =$ **10 %**.
:::

::: note Activity — read a real bill
Bring home a shop bill with VAT on it. Check three things: the price before
VAT, the VAT amount, and whether VAT is 13 % of the pre-VAT total. Then work
out what the bill would have been with a 10 % discount applied first.
**Discussion:** Why is taking the bill the customer's duty as well as the
shopkeeper's?
:::

## Chapter summary

- $\text{profit}=\text{SP}-\text{CP}$ when SP exceeds CP;
  $\text{loss}=\text{CP}-\text{SP}$ when CP exceeds SP.
- Profit percent and loss percent are measured against the **cost price**.
- $\text{SP}=\text{CP}(1\pm\frac{\%}{100})$;
  $\text{CP}=\frac{100\times\text{SP}}{100\pm\%}$.
- $\text{discount}=\text{MP}-\text{SP}$, and discount percent is measured against
  the **marked price**.
- $\text{SP}=\text{MP}(1-\frac{\text{discount}\%}{100})$.
- A sale can give a discount and a profit at the same time, because the two
  percentages are measured on different bases.
- Commission is a percentage of the sale value and is paid to the agent.

## Practice questions

**Group A — Objective (1 mark each)**

1. Profit percent is calculated on the <span class="marks">[1]</span>
   (a) selling price (b) marked price (c) cost price (d) discount
2. Discount percent is calculated on the <span class="marks">[1]</span>
   (a) selling price (b) marked price (c) cost price (d) profit
3. An article bought for Rs 500 is sold for Rs 450. The loss percent is
   <span class="marks">[1]</span>
   (a) 10% (b) 11% (c) 12.5% (d) 50%
4. If CP is Rs 800 and profit is 25 %, the SP is
   <span class="marks">[1]</span>
   (a) Rs 825 (b) Rs 1000 (c) Rs 1025 (d) Rs 1200
5. MP Rs 1,000 with a 30 % discount gives an SP of
   <span class="marks">[1]</span>
   (a) Rs 970 (b) Rs 700 (c) Rs 300 (d) Rs 1300
6. A 5 % commission on a sale of Rs 40,000 is
   <span class="marks">[1]</span>
   (a) Rs 200 (b) Rs 2000 (c) Rs 500 (d) Rs 8000

::: note Answers to Group A
**1.** (c) — cost price.
**2.** (b) — marked price.
**3.** (a) — $\frac{50}{500}\times100=10\%$.
**4.** (b) — $800\times1.25=1000$.
**5.** (b) — $1000\times0.7=700$.
**6.** (b) — $\frac{5}{100}\times40\,000=2000$.
:::

**Group B — Short answer (2 marks each)**

1. Find the profit percent when an article bought for Rs 2,500 is sold for
   Rs 2,800. <span class="marks">[2]</span>
2. The selling price of an article is Rs 1,440 at a loss of 10 %. Find its cost
   price. <span class="marks">[2]</span>
3. Find the selling price after a discount of 12 % on a marked price of
   Rs 4,000. <span class="marks">[2]</span>
4. An agent gets a commission of Rs 2,250 on a sale of Rs 45,000. Find the rate
   of commission. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Profit $=300$; profit percent $=\frac{300}{2500}\times100=12\%$.
**2.** $\text{CP}=\frac{100\times1440}{90}=\text{Rs }1600$.
**3.** Discount $=480$, so SP $=4000-480=\text{Rs }3520$.
**4.** Rate $=\frac{2250}{45000}\times100=5\%$.
:::

**Group C — Long answer (4 marks each)**

1. A shopkeeper marks his goods 40 % above the cost price and then allows a
   discount of 20 % on the marked price. Find his profit percent, and explain
   why the profit is not 20 %. <span class="marks">[4]</span>
2. A dealer sold two mobile phones for Rs 9,000 each. On one he made a profit of
   20 % and on the other a loss of 20 %. Find his total profit or loss, and
   explain the result. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Take CP $=$ Rs 100. Then
$\text{MP}=100\times1.40=\text{Rs }140$, and the discount is 20 % of the marked
price: $0.20\times140=\text{Rs }28$, so
$\text{SP}=140-28=\text{Rs }112$. Profit $=112-100=\text{Rs }12$, that is
**12 %** on the cost. **Why not 20 %.** The 40 % is added to the cost price while
the 20 % discount comes off the marked price, which is the larger number:
$0.40\times100=40$, but $0.20\times140=28$, so only 12 remains. Percentages
added and subtracted in this way only cancel when they are measured on the same
base.
**2.** **First phone (20 % profit).**
$\text{CP}=\frac{100\times9000}{120}=\text{Rs }7500$; profit $=1500$.
**Second phone (20 % loss).**
$\text{CP}=\frac{100\times9000}{80}=\text{Rs }11\,250$; loss $=2250$.
**Total.** $\text{CP}=7500+11\,250=\text{Rs }18\,750$, and
$\text{SP}=9000+9000=\text{Rs }18\,000$. So there is a **net loss of
Rs 750**, which is $\frac{750}{18\,750}\times100=4\%$ of the total cost.
**Explanation.** The loss is worked on a larger cost price than the profit, so
the two do not cancel. Equal percentage profit and loss on equal selling prices
always gives a net loss of $\frac{x^2}{100}\%$ — here
$\frac{20^2}{100}=4\%$ ✓.
:::

**Extra practice**

**Group B (2 marks)**

11. An article costing Rs 1,250 is sold at a profit of 16 %. Find the selling
    price.
12. VAT of Rs 338 was charged at 13 %. Find the price before VAT.

**Group C (4 marks)**

13. A radio marked at Rs 2,800 is sold at a 15 % discount with 13 % VAT. If the
    shopkeeper still makes a 19 % profit, find the cost price.

::: note Extra practice — answers
**11.** Profit $= 200$; S.P. $=$ **Rs 1,450**.
**12.** Price $= \frac{338}{0.13} =$ **Rs 2,600**.
**13.** After discount: $2800 - 15\%$ of $2800 = 2800 - 420 = $ Rs 2,380 — this is
what the shopkeeper receives. If that is a 19 % profit, then
$1.19 \times \text{C.P.} = 2380$, so C.P. $= \frac{2380}{1.19} =$ **Rs 2,000**.
(The VAT of $13\%$ of $2380 = $ Rs 309.40 is collected for the government and is
not part of the profit.)
:::

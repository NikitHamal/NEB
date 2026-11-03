---
subject: Applied Economics
grade: BCA Semester 3
unit: 6
title: National Income Accounting
hours: 6
area: BCA 206 · Applied Economics · Unit 6
---

**National income accounting** measures the total output and income of an economy: the macro counterpart of a company's accounts. Governments use it to judge growth and plan; analysts use it to compare countries.

::: key What this unit gives you
- The circular flow of income in two-, three- and four-sector economies.
- GDP, NDP, GNP, NNP, national income, personal income, disposable income, per capita income.
- Real versus nominal GDP and the deflator; the product, income and expenditure methods.
:::

## 6.1 Circular flow of income and expenditure

Output creates income (wages, rent, interest, profit) and income is spent on output: a **circular flow**.

**Two-sector economy (households and firms):** households supply factors and receive income Y; they spend on consumption C and save S. Firms' investment I is financed by saving. Equilibrium: **Y = C + I** and **S = I**. *Injections* (I) add to the flow, *leakages* (S) remove from it; the economy is in equilibrium when leakages equal injections.

**Three-sector (adding government):** **Y = C + I + G**; leakages are saving and taxes, S + T = I + G. **Four-sector (open economy):** **Y = C + I + G + (X − M)**; leakages S + T + M, injections I + G + X.

::: example Worked example: equilibrium and the multiplier
Consumption C = 100 + 0.8Y, investment I = 100. Equilibrium Y = C + I = 100 + 0.8Y + 100 → 0.2Y = 200 → **Y = 1,000**; saving S = Y − C = −100 + 0.2Y = **100 = I** ✓. The **multiplier** k = 1/(1 − MPC) = 1/0.2 = **5**: an investment rise of 20 raises income by **100**.
**Adding government** (G = 100 and a lump-sum tax T = 100): Y = 100 + 0.8(Y − 100) + 100 + 100 → 0.2Y = 220 → **Y = 1,100**.
:::

## 6.2 Concepts of national income

| Concept | Definition |
|---|---|
| **GDP at market prices** | market value of all **final** goods and services produced **within the country** in a year, whoever owns the factors |
| **GNP** | GDP + **net factor income from abroad** (NFIA: income earned abroad by nationals minus income earned by foreigners here); counts what *nationals* produce anywhere |
| **NDP** | GDP − depreciation (**capital consumption allowance**) |
| **NNP** | GNP − depreciation |
| **National income (NI) at factor cost** | NNP at market prices − (indirect taxes − subsidies): the income earned by factors of production |
| **Personal income (PI)** | income actually received by households: NI − undistributed (retained) profits − corporate taxes − social security contributions + **transfer payments** |
| **Disposable personal income (DI)** | PI − personal direct taxes: what households can spend or save |
| **Per capita income (PCI)** | national income ÷ population |

**Market price versus factor cost:** GDP_mp = GDP_fc + indirect taxes − subsidies. Only **final** goods are counted (counting intermediate goods would be **double counting**); transfer payments, second-hand sales, and purely financial transactions are excluded; **non-market activities** (housework) and the **underground economy** are mostly missed, and GDP ignores environmental damage and distribution: it is a measure of output, not welfare. For Nepal, **remittance** income received by households raises GNI and disposable income above GDP-based measures.

::: example Worked example: all concepts from one set of figures
Consumption C = 600; investment I = 200; government spending G = 150; exports X = 100; imports M = 120; NFIA = 20; depreciation = 50; indirect taxes − subsidies = 40; retained profits 30; corporate taxes 20; transfers 25; personal taxes 60; population 10 (million).
**GDP_mp** = C + I + G + (X − M) = 600 + 200 + 150 + (100 − 120) = **930**.
**GNP_mp** = 930 + 20 = **950**. **NNP_mp** = 950 − 50 = **900**. **NI (factor cost)** = 900 − 40 = **860**.
**PI** = 860 − 30 − 20 + 25 = **835**. **DI** = 835 − 60 = **775**. **PCI** = 860/10 = **86** (per person, in the same units).
:::

## 6.3 Real and nominal GDP; GDP deflator

**Nominal GDP** uses current prices, so it rises with both output and prices; **real GDP** uses base-year prices and shows only output changes. **GDP deflator = (nominal GDP/real GDP) × 100**, a price index for all goods; **real GDP = (nominal GDP/deflator) × 100**. Real growth rate = % change in real GDP.

::: example Worked example
Year 1 (base): nominal GDP 1,000, deflator 100, so real GDP = 1,000. Year 2: nominal GDP 1,320, deflator 120. **Real GDP** = 1,320/1.20 = **1,100**. Nominal growth = 32%; **real growth = 10%**; inflation (deflator) = **20%**. The apparent 32% growth was mostly a price rise.
:::

## 6.4 Methods of computing national income

Three equal ways of measuring the same flow:

1. **Product (value-added) method:** add the **value added** at each stage: VA = value of output − value of intermediate inputs.
2. **Income method:** add all factor incomes: **compensation of employees + rent + interest + profit (+ mixed income)** = NI at factor cost (+ depreciation + net indirect taxes for GDP_mp).
3. **Expenditure method:** **C + I + G + (X − M)**.

::: example Worked example
**Product method:** a farmer sells wheat for 100 to a miller; the miller sells flour for 250 to a baker; the baker sells bread for 400 to consumers. Value added: farmer 100, miller 250 − 100 = **150**, baker 400 − 250 = **150**; total = **400** = the final value of bread (adding the sales 100 + 250 + 400 = 750 would double-count).
**Income method (figures of 6.2):** wages 500 + rent 60 + interest 50 + profit 250 = **860** = NI at factor cost ✓ (equal to the product and expenditure results once depreciation and indirect taxes are accounted).
**Excel exercise:** `=C+I+G+(X-M)` for GDP; `=GDP+NFIA-DEP-NIT` for national income; `=Nominal/Deflator*100` for real GDP; chart real GDP across years.
:::

**Limitations:** unrecorded and subsistence activity (big in Nepal's agriculture), unpaid work, quality improvements, income inequality and environmental costs are ignored, and international comparisons need purchasing-power adjustments. Alternatives and supplements: the **Human Development Index** (income, education, health), green GDP.

## 6.5 Seeing national income: flows, the Keynesian cross and the value chain

```svgfig label="6.1" caption="Four-sector circular flow. Households sell factor services to firms and receive income; they spend on goods (C), pay taxes (T), save into financial markets (S) and buy imports (M). Firms invest (I), government spends (G) and the rest of the world buys exports (X). Leakages S + T + M equal injections I + G + X in equilibrium."
f = Fig(580, 290)
f.box(30, 20, 150, 52, "HOUSEHOLDS\nown the factors", fill=MINT, stroke=TEAL, bold=True, size=11)
f.box(400, 20, 150, 52, "FIRMS\nproduce goods", fill=BLUE, stroke=NAVY, bold=True, size=11)
f.box(215, 108, 150, 44, "FINANCIAL MARKETS", fill=SAND, stroke=AMBER, bold=True, size=11)
f.box(30, 222, 150, 46, "GOVERNMENT", fill=ROSE, stroke=RED, bold=True, size=11)
f.box(400, 222, 150, 46, "REST OF THE WORLD", fill=SOFT, stroke=SLATE, bold=True, size=11)
f.arrow([(180, 36), (400, 36)], color=TEAL, label="labour, land, capital", lpos=(290, 26))
f.arrow([(400, 58), (180, 58)], color=NAVY, label="wages, rent, interest, profit = Y", lpos=(290, 76))
f.arrow([(105, 72), (105, 115), (215, 125)], color=AMBER, label="saving S", lpos=(70, 100))
f.arrow([(365, 125), (475, 115), (475, 72)], color=AMBER, label="investment I", lpos=(520, 100))
f.arrow([(105, 72), (105, 222)], color=RED, label="taxes T", lpos=(75, 170))
f.arrow([(130, 222), (130, 72)], color=RED, dash=True, label="G, transfers", lpos=(158, 170))
f.arrow([(475, 72), (475, 222)], color=SLATE, label="imports M", lpos=(515, 170))
f.arrow([(450, 222), (450, 72)], color=SLATE, dash=True, label="exports X", lpos=(415, 170))
f.text(290, 205, "Leakages: S + T + M      Injections: I + G + X", size=11, color=NAVY, bold=True)
f.text(290, 238, "Y = C + I + G + (X − M)", size=13, color=TEAL, bold=True)
```

```svgfig label="6.2" caption="The Keynesian cross for C = 100 + 0.8Y and I = 100. (a) Aggregate expenditure 200 + 0.8Y meets the 45° line at Y = 1,000; adding G = 100 with a lump-sum tax of 100 lifts expenditure to 220 + 0.8Y and equilibrium to 1,100. (b) The multiplier of 5 as a chain: an extra investment of 20 raises income by 20, then 16, 12.8, and so on, until the total reaches 100."
f = Fig(580, 255)
a = Axes(f, 42, 14, 225, 190, (0, 1400), (0, 1400))
a.grid(400, 400).axes("Income Y", "Expenditure")
a.curve(lambda y: y, 0, 1400, color=SLATE, dash=True); a.curve(lambda y: 200 + 0.8 * y, 0, 1400, color=NAVY); a.curve(lambda y: 220 + 0.8 * y, 0, 1400, color=TEAL)
a.pt(1000, 1000, "E1 1,000", dx=-8, dy=-12, anchor="end"); a.pt(1100, 1100, "E2 1,100", dx=8, dy=18, color=TEAL)
a.tag(150, 1300, "45° line", size=10, color=SLATE, bold=True); a.tag(1000, 1310, "C+I+G", size=10, color=TEAL, bold=True); a.tag(1290, 1030, "C+I", size=10, color=NAVY, bold=True)
b = Axes(f, 335, 14, 225, 190, (0, 8), (0, 110))
b.grid(1, 20).axes("", "Income"); f.text(448, 226, "Round", size=9.5, color=SLATE)
tot = 0
for i in range(1, 8):
    d = 20 * 0.8 ** (i - 1); tot += d
    f.raw(f'<rect x="{b.X(i)-11}" y="{b.Y(d)}" width="22" height="{b.Y(0)-b.Y(d)}" fill="#fde68a" stroke="{AMBER}" stroke-width="1.2"/>')
    f.text(b.X(i), b.Y(d) - 4, f"{d:.1f}".rstrip("0").rstrip("."), size=9, color=SLATE, bold=True)
pts = " ".join(f"{b.X(i)},{b.Y(sum(20*0.8**(j-1) for j in range(1, i+1)))}" for i in range(1, 8))
f.raw(f'<polyline points="{pts}" fill="none" stroke="{TEAL}" stroke-width="2.2"/>')
b.hline(100, 0, 8, color=RED); b.tag(3.4, 93, "limit 100 = 20 × 5", size=10, color=RED, bold=True)
f.text(155, 244, "(a) equilibrium income", size=11, color=SLATE, italic=True); f.text(448, 244, "(b) multiplier rounds and running total", size=11, color=SLATE, italic=True)
```

```svgfig label="6.3" caption="From GDP to disposable income with the figures of the worked example: GDP_mp 930, add net factor income from abroad (+20) for GNP 950, subtract depreciation (−50) for NNP 900, subtract net indirect taxes (−40) for national income 860, then adjust for retained profit (−30), corporate tax (−20) and transfers (+25) for personal income 835, and personal taxes (−60) for disposable income 775. The vertical axis starts at 600."
f = Fig(580, 235)
a = Axes(f, 42, 14, 520, 175, (0, 7), (600, 1000))
a.grid(1, 100, labels=False).axes("", "")
for v in range(600, 1001, 100): f.text(36, a.Y(v) + 4, str(v), size=9.5, color=SLATE, anchor="end")
steps = [("GDP", 0, 930, NAVY), ("+NFIA\n+20", 930, 950, TEAL), ("−dep.\n−50", 950, 900, RED), ("−net ind.\ntax −40", 900, 860, RED), ("−ret., corp.\n+transf. −25", 860, 835, RED), ("−personal\ntax −60", 835, 775, RED), ("DI", 0, 775, NAVY)]
tops = [("GDP\n930", 930), ("GNP\n950", 950), ("NNP\n900", 900), ("NI\n860", 860), ("PI\n835", 835), ("", 775), ("DI\n775", 775)]
for i, (lab, s, e, c) in enumerate(steps):
    lo, hi = (600 if s == 0 else min(s, e)), max(s, e)
    f.raw(f'<rect x="{a.X(i+0.5)-30}" y="{a.Y(hi)}" width="60" height="{a.Y(lo)-a.Y(hi)}" fill="{c}" opacity="0.22" stroke="{c}" stroke-width="1.6"/>')
    f.text(a.X(i + 0.5), a.Y(hi) - 6, tops[i][0].replace("\n", " "), size=10, color=c, bold=True)
    f.text(a.X(i + 0.5), 206, lab.split("\n")[0], size=9.5, color=SLATE); f.text(a.X(i + 0.5), 219, lab.split("\n")[1] if "\n" in lab else "", size=9.5, color=SLATE)
```

```photogrid label="6.1" cols="3" ratio="1.0" caption="Where the concepts come from. (a) John Maynard Keynes (1883-1946), whose General Theory (1936) made total spending the centre of macroeconomics and gave us the multiplier. (b) Kalimati wholesale market and (c) an Asan retail stall: two stages in the value chain of the same vegetable, each adding value that the product method of national income counts once."
@ photo id="bca206/keynes" cap="J. M. Keynes, 1933"
fit 1.0
focus 0.5 0.6
@ photo id="bca206/kalimati" cap="Kalimati wholesale market (stage 2)"
fit 1.0
focus 0.55 0.5
@ photo id="bca206/asan" cap="Asan retail stall (stage 3)"
fit 1.0
focus 0.4 0.5
```

## 6.6 Eight uses of national income statistics

1. **Measuring the size and growth of the economy.** GDP tells how much the country produces in a year, and its growth rate tells whether output is rising. The Central Bureau of Statistics publishes it, and the Ministry of Finance bases the budget on it. Without such a figure, policy would work in the dark.
2. **Comparing living standards.** Per capita income divides national income by population, so it allows comparison between districts, years and countries. Nepal can see how far it is from other South Asian countries on this scale. It is an imperfect measure, but it is the most common starting point.
3. **Planning the budget and development projects.** Planners decide how much to invest, tax and borrow by looking at the size of the economy and its sectors. The share of agriculture, industry and services guides where roads, power and schools should go. Targets in each periodic plan are set as growth rates of GDP.
4. **Measuring real progress by removing inflation.** The GDP deflator turns nominal GDP into real GDP, so a price rise is not mistaken for growth. In the worked example, nominal growth of 32% was only 10% in real terms. This keeps politicians and students honest.
5. **Understanding the role of remittance.** Money sent home by Nepali workers raises household income and GNI more than it raises GDP. National accounts show how large this inflow is compared with exports and aid. This helps the Nepal Rastra Bank judge the economy's dependence on foreign jobs.
6. **Guiding monetary and fiscal policy.** Central banks and finance ministries watch GDP, investment and consumption to judge whether to raise or cut interest rates, taxes and spending. A fall in private investment may call for more public spending. The multiplier tells how large the effect will be.
7. **Showing the structure of the economy.** The product method splits GDP among agriculture, industry and services, and the expenditure method splits it into consumption, investment, government and net exports. Both reveal weaknesses, such as a very high share of imports. A student can read the structure at once.
8. **Allocating aid and judging credit risk.** International agencies and lenders use GDP, per capita income and growth to decide the size of loans and grants. A bank's country rating also depends on them. Accurate accounts therefore make borrowing cheaper and aid better targeted.

## Formula and fact sheet

- Two-sector: Y = C + I; S = I. Three: Y = C + I + G. Four: + (X − M). Multiplier k = 1/(1 − MPC).
- GNP = GDP + NFIA. NDP = GDP − depreciation. NI (factor cost) = NNP_mp − net indirect taxes.
- PI = NI − retained profits − corporate tax + transfers. DI = PI − personal taxes. PCI = NI/population.
- Deflator = nominal/real × 100. Real GDP = nominal/deflator × 100.
- Methods: product (value added), income, expenditure.

## Chapter summary

- The circular flow links output, income and spending; equilibrium needs leakages = injections.
- GDP, GNP, NDP, NNP, NI, PI, DI and PCI are successive adjustments for foreign income, depreciation, taxes and transfers.
- Real GDP strips out price changes using the deflator; national income is computed by product, income or expenditure methods, which agree.

## Practice

1. Differentiate GDP and GNP; real and nominal GDP.
2. C = 800, I = 250, G = 200, X = 150, M = 180, NFIA = −30, depreciation = 70, net indirect taxes = 60. Find GDP_mp, GNP_mp, NNP_mp and NI.
3. C = 50 + 0.75Y and I = 50. Find equilibrium Y, saving and the multiplier.
4. Nominal GDP rises from 2,000 to 2,860 while the deflator rises from 100 to 130. Find real GDP and real growth.
5. A mill buys wheat worth 200 and sells flour worth 500. Find its value added.
6. List the items excluded from GDP and give reasons.
7. Explain the income method.

::: note Answers and worked solutions
**1.** GDP counts output within the country's borders; GNP counts output of the country's residents anywhere (GDP + NFIA). Nominal uses current prices; real uses constant prices.
**2.** GDP_mp = 800 + 250 + 200 + (150 − 180) = **1,220**. GNP_mp = 1,220 − 30 = **1,190**. NNP_mp = 1,190 − 70 = **1,120**. NI = 1,120 − 60 = **1,060**.
**3.** Y = 50 + 0.75Y + 50 → 0.25Y = 100 → **Y = 400**; S = Y − C = 400 − 350 = **50 = I**; multiplier = 1/0.25 = **4**.
**4.** Real GDP = 2,860/1.30 = **2,200**; real growth = (2,200 − 2,000)/2,000 = **10%** (nominal growth 43%).
**5.** 500 − 200 = **300**.
**6.** Intermediate goods (double counting), transfer payments and second-hand sales (no new output), financial transactions, unpaid household work and the underground economy (not recorded).
**7.** Add all incomes earned by factors: wages and salaries, rent, interest and profits (and mixed income of the self-employed), to obtain national income at factor cost.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the circular flow of income in a two-sector, three-sector and four-sector economy. With C = 100 + 0.8Y and I = 100, find equilibrium income and the multiplier.**

*Introduction.* Output creates income and income is spent on output, so money, goods and factor services move in a **circular flow** (Figure 6.1). The economy is in equilibrium when **leakages equal injections**.

*Sectors.*

1. **Two sectors (households and firms):** households give factors and receive income Y, then consume C and save S. Firms' investment I is financed by saving. Equilibrium: **Y = C + I** and **S = I**.
2. **Three sectors (adding government):** **Y = C + I + G**; leakages are saving and taxes, S + T = I + G.
3. **Four sectors (open economy):** **Y = C + I + G + (X − M)**; leakages are S + T + M and injections are I + G + X.

*Numerical case (Figure 6.2).* Y = C + I gives Y = 100 + 0.8Y + 100, so 0.2Y = 200 and **Y = 1,000**. Saving S = Y − C = −100 + 0.2Y = **100 = I**. The multiplier is k = 1/(1 − MPC) = 1/0.2 = **5**, so an extra investment of 20 raises income by **100**. With G = 100 and a lump-sum tax T = 100: Y = 100 + 0.8(Y − 100) + 100 + 100, so 0.2Y = 220 and **Y = 1,100**.

*Conclusion.* Extra injections raise income by a multiple of themselves, and the more people spend of each extra rupee, the larger the multiplier.

**Q2 (5 marks). Distinguish between nominal and real GDP. What is the GDP deflator? Nominal GDP rises from 1,000 to 1,320 while the deflator rises from 100 to 120; find the real growth.**

*Introduction.* GDP is the market value of all final goods and services produced within a country in a year. Its value can rise because more is produced or because prices rise, so economists need two versions.

| Point | Nominal GDP | Real GDP |
|---|---|---|
| Prices used | current-year prices | base-year prices |
| Changes with | output and prices | output only |
| Use | size of the economy in money | true growth of output |
| Example | 1,320 in year 2 | 1,100 in year 2 |

*GDP deflator.* The deflator is a price index for all goods: **deflator = (nominal GDP / real GDP) × 100**. Hence **real GDP = nominal GDP / deflator × 100**.

*Calculation.* Real GDP in year 2 = 1,320 / 120 × 100 = **1,100**. Nominal growth is 32%, real growth is (1,100 − 1,000)/1,000 = **10%**, and inflation by the deflator is **20%**.

*Conclusion.* The headline 32% growth was mostly price rise; only 10% was real extra output.

**Q3 (10 marks). Define GDP, GNP, NDP, NNP, national income, personal income and disposable income. Explain the three methods of measuring national income, and compute all concepts from the given data.**

*Introduction.* **National income** is the value of the flow of goods and services produced by an economy in a year. Several related measures adjust GDP for foreign income, wear and tax (Figure 6.3).

*Concepts.*

1. **GDP (market prices):** value of final output produced within the country, whoever owns the factors.
2. **GNP:** GDP + net factor income from abroad (NFIA).
3. **NDP and NNP:** GDP and GNP minus depreciation.
4. **National income (NI) at factor cost:** NNP at market prices − (indirect taxes − subsidies).
5. **Personal income (PI):** NI − retained profits − corporate taxes + transfer payments.
6. **Disposable income (DI):** PI − personal direct taxes.
7. **Per capita income:** NI ÷ population.

*Three methods.* (1) **Product method:** add the value added at each stage, VA = output − intermediate inputs. A farmer sells wheat for 100, the miller flour for 250, the baker bread for 400: value added is 100, 150, 150, total **400**, not 750 (adding sales would double-count). (2) **Income method:** wages + rent + interest + profit = NI at factor cost. (3) **Expenditure method:** C + I + G + (X − M).

*Numerical illustration.* C = 600, I = 200, G = 150, X = 100, M = 120, NFIA = 20, depreciation = 50, net indirect taxes = 40, retained profit 30, corporate tax 20, transfers 25, personal tax 60, population 10.

| Measure | Working | Value |
|---|---|---|
| GDP_mp | 600 + 200 + 150 + (100 − 120) | 930 |
| GNP_mp | 930 + 20 | 950 |
| NNP_mp | 950 − 50 | 900 |
| NI | 900 − 40 | 860 |
| PI | 860 − 30 − 20 + 25 | 835 |
| DI | 835 − 60 | 775 |
| Per capita income | 860 / 10 | 86 |

*Limitations.* GDP leaves out unpaid household work, much subsistence farming and the underground economy; it ignores inequality, leisure and environmental damage. The Human Development Index adds education and health to income.

*Conclusion.* The three methods measure one flow and must agree. GDP measures output, not welfare, so it should be read together with other indicators.

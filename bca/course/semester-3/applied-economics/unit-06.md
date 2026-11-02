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

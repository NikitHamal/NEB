---
subject: Society and Technology
grade: BCA Semester 5
unit: 3
title: The Digital Divide and Digital Nepal
hours: 7
area: BCA 305 · Society and Technology · Unit 3
---

Two students in the same country sit the same national examination. One lives in Kathmandu with fibre broadband, a laptop and parents who use online banking; the other lives in a Karnali village where the 4G signal reaches only the hilltop, electricity cuts out for days, and the only phone is shared by the family. Both are "connected" in the national statistics, yet their digital lives are of different kinds. The **digital divide** names this gap, and this unit shows how to define it, how to *measure* it (shares, ratios, a Lorenz curve with a Gini coefficient, a composite index), and what Nepal's policy response, the **Digital Nepal Framework**, tries to do about it.

::: key What this unit gives you
- Three levels of the divide (access, skills, outcomes) and its dimensions: urban/rural, gender, income, age, disability, language.
- Measurement: ratios, Lorenz curve and Gini, a composite min-max index, with worked tables.
- Local-language computing, Unicode and Nepali content.
- The Digital Nepal Framework and its eight sectors; community and school initiatives; indicators and their sources.
:::

*All province-level figures in this unit are **invented for teaching** so that the arithmetic can be followed; real figures come from the National Statistics Office, the Nepal Telecommunications Authority (NTA) monthly MIS reports and the Ministry of Communication and Information Technology. Always check the latest publication.*

## 3.1 What is the digital divide?

The **digital divide** is the gap between those who have effective access to digital technologies and those who do not, and between those who *benefit* from them and those who do not. Researchers describe three levels:

1. **First-level divide (access):** devices, connectivity, electricity, affordability.
2. **Second-level divide (skills and use):** digital literacy, language, confidence; the difference between scrolling a feed and filing a tax return.
3. **Third-level divide (outcomes):** who actually gains income, education, health or political voice from being online.

Closing the first level does not close the others: a smartphone gives access, but a farmer who cannot read the interface in her language or does not trust mobile money gains little.

| Dimension | How the gap appears in Nepal |
|---|---|
| Geography | Urban valleys and the Terai towns have fibre and 4G; remote hill and mountain districts have thin coverage and costly backhaul |
| Income and cost | Data and device costs are a larger share of a low income; second-hand phones; no home computer |
| Gender | Women have fewer personal phones and lower use; norms, literacy and safety concerns |
| Age and disability | Older people and people with disabilities find interfaces and services inaccessible |
| Language and script | Most content is English; Nepali Unicode support, voice and local-language interfaces are limited; many mother-tongue communities have almost none |
| Caste and ethnicity | Historical disadvantage compounds access barriers |
| Skills | Low digital and financial literacy limits safe use |

## 3.2 Measuring the divide

### Simple ratios and gaps

Compare two groups with a **gap** (difference in percentage points) or a **ratio** (relative disadvantage). Suppose 38% of women and 52% of men use the internet: the gap is **14 points** and the **gender parity index** (female ÷ male) is **0.731**; parity is 1.0. Reporting both avoids mistakes: a 14-point gap sounds small if both groups are near 90%, but is large when use is 38% versus 52%.

### An example data set

| Province (invented data) | Population (million) | Internet use % | Fixed broadband per 100 homes | Smartphone % | Digital-skills % |
|---|---|---|---|---|---|
| Koshi | 4.97 | 62 | 21 | 48 | 42 |
| Madhesh | 6.1 | 41 | 9 | 35 | 25 |
| Bagmati | 6.1 | 82 | 40 | 70 | 68 |
| Gandaki | 2.4 | 70 | 25 | 58 | 50 |
| Lumbini | 5.1 | 55 | 15 | 45 | 38 |
| Karnali | 1.7 | 28 | 4 | 24 | 20 |
| Sudurpashchim | 2.7 | 36 | 6 | 30 | 27 |

Totals: population 29.07 million, of whom **16.52 million** use the internet, a national rate of **56.8%**. Bagmati's internet-use rate is **2.93 times** Karnali's, and its fixed broadband penetration is **10.0 times** higher. The national average hides these differences, which is why disaggregated data matter.

### Lorenz curve and Gini coefficient

Borrowed from the study of income inequality, the **Lorenz curve** plots the cumulative share of the population (poorest access first) against the cumulative share of internet users. Perfect equality is the diagonal; the farther the curve bends below it, the greater the inequality. The **Gini coefficient** is the area between the diagonal and the curve divided by the area under the diagonal: G = 1 − Σ (Xᵢ − Xᵢ₋₁)(Yᵢ + Yᵢ₋₁), summing over groups with cumulative population share X and cumulative user share Y. 0 is equality; 1 is one group having everything. Sorting provinces by users per head:

| Province (poorest access first) | Population share | Internet-user share | Cumulative population | Cumulative users |
|---|---|---|---|---|
| Karnali | 5.8% | 2.9% | 5.8% | 2.9% |
| Sudurpashchim | 9.3% | 5.9% | 15.1% | 8.8% |
| Madhesh | 21.0% | 15.1% | 36.1% | 23.9% |
| Lumbini | 17.5% | 17.0% | 53.7% | 40.9% |
| Koshi | 17.1% | 18.7% | 70.8% | 59.5% |
| Gandaki | 8.3% | 10.2% | 79.0% | 69.7% |
| Bagmati | 21.0% | 30.3% | 100.0% | 100.0% |

The Gini is **0.171**. This is low because the province is a coarse grouping; the divide inside provinces (urban against rural municipalities) and between households would be larger. Always state the unit of analysis before comparing Gini values.

### A composite digital divide index

No single indicator captures the divide, so analysts combine several. A common method is **min-max normalisation**: for each indicator, score = (value − minimum) / (maximum − minimum), so the lowest province gets 0 and the highest 1, then average the scores with equal weights (or chosen weights).

| Province | Internet | Broadband | Smartphone | Skills | DDI (mean of 4) |
|---|---|---|---|---|---|
| Koshi | 0.63 | 0.47 | 0.52 | 0.46 | 0.520 |
| Madhesh | 0.24 | 0.14 | 0.24 | 0.10 | 0.181 |
| Bagmati | 1.00 | 1.00 | 1.00 | 1.00 | 1.000 |
| Gandaki | 0.78 | 0.58 | 0.74 | 0.62 | 0.681 |
| Lumbini | 0.50 | 0.31 | 0.46 | 0.38 | 0.409 |
| Karnali | 0.00 | 0.00 | 0.00 | 0.00 | 0.000 |
| Sudurpashchim | 0.15 | 0.06 | 0.13 | 0.15 | 0.120 |

**Bagmati** ranks first (index 1.000) and **Karnali** last (0.000). Min-max scores are *relative*: a score of 0 means "lowest of these seven", not "no access". Changing the indicators or weights can change the middle ranks; publish the method with the result.

## 3.3 Language, script and content

A person cannot benefit from technology that does not speak their language. **Unicode** encodes Devanagari so that Nepali text, with its conjuncts and vowel signs, is stored and searched consistently; before Unicode, legacy fonts such as Preeti stored text in ways incompatible with search, email and the web, leaving much older government content unsearchable. Needs: Nepali keyboard layouts (Romanized and traditional), fonts that render conjuncts correctly, **spell-checkers and OCR** for Devanagari, **text-to-speech and speech recognition** in Nepali and other languages, and interfaces and government forms in the languages of the country (Nepal has over a hundred languages). **Local content** (agriculture advice, health information, news, education material) increases the relevance of connectivity. Accessibility standards (WCAG: text alternatives, contrast, keyboard operation, captions) address disability.

## 3.4 The Digital Nepal Framework

The Government of Nepal launched the **Digital Nepal Framework** in 2019 as a national roadmap to use digital technology for economic growth and better services. It identifies **eight sectors** where digital technology can have the largest effect and a set of enabling **"digital foundation" building blocks**:

| Sector | Examples of the digital focus |
|---|---|
| **Digital Foundation** | Connectivity and broadband, national data centre and cloud, digital ID, digital payments, cyber security, legal and regulatory reform, skills |
| **Agriculture** | Information and advisory services for farmers, market prices, supply-chain digitisation, e-agriculture |
| **Health** | Health information systems, electronic records, telemedicine |
| **Education** | Digital learning content, connectivity of schools, e-learning platforms |
| **Energy** | Smart metering, digital management of generation and distribution, electric mobility planning |
| **Tourism** | Online services for visitors, digital promotion, reservation and information systems |
| **Finance** | Digital payments and financial inclusion, interoperability, digital banking |
| **Urban Infrastructure** | Smart city and municipal digital services, traffic and utility management |

The framework lists many initiatives (on the order of eighty) with agencies and timelines; its progress depends on funding, coordination across ministries and the three tiers of government, and the legal reforms discussed in Unit 4. Complementary programmes: community information centres and **community learning centres**, school computer-lab and connectivity programmes, **rural telecommunication development** funded through the universal service fund of the NTA, and the expansion of optical-fibre backbones by the national utilities and private operators. Evaluate any programme by the three divides: did it provide access, build skills, *and* produce outcomes?

## 3.5 Closing the divide

- **Infrastructure and affordability:** shared towers, universal service funding, tax treatment of devices and data, community Wi-Fi, solar-powered access points where the grid is weak.
- **Skills:** digital literacy in schools and in community centres, training for women and older people, *train-the-trainer* networks.
- **Content and services:** services that work in Nepali and local languages, on low-end phones, offline or by USSD/SMS, with human help desks.
- **Inclusive design:** consult the excluded, test with real users, accessibility by default.
- **Trust and safety:** consumer protection for digital money and clear complaint channels; safe online spaces for women and girls.
- **Measurement:** collect gender-, age-, location- and disability-disaggregated data and publish it.

::: caution E-government can widen the divide
Moving a service online helps those connected and can *exclude* everyone else if the counter is closed. Keep an assisted channel (a ward office or help desk) until access is genuinely universal.
:::

## Chapter summary

- The divide has three levels (access, skills, outcomes) and many dimensions: geography, income, gender, age, disability, language and caste.
- Gaps, ratios, the gender parity index, Lorenz/Gini and min-max composite indices measure it; the unit of analysis and the method must be stated.
- Unicode, Nepali-language tools and local content are conditions for benefit, not extras.
- The Digital Nepal Framework (2019) has eight sectors: Digital Foundation, Agriculture, Health, Education, Energy, Tourism, Finance and Urban Infrastructure.
- Closing the divide needs infrastructure, affordability, skills, local content, inclusive design and trust, and assisted channels.

## Practice

1. Name the three levels of the digital divide.
2. State two ways the divide appears for women in Nepal.
3. With 45% of women and 60% of men online, compute the gap and the gender parity index.
4. In the example data, how many times higher is Madhesh's internet-use rate than Karnali's? (Use the table.)
5. Explain how the Lorenz curve and Gini coefficient are computed.
6. Why is a min-max index a relative, not absolute, measure?
7. Why did legacy fonts such as Preeti harm digital inclusion?
8. List the eight sectors of the Digital Nepal Framework.
9. Name four measures to reduce the divide in a remote municipality.
10. Why should e-government keep an assisted channel?

::: note Answers and worked solutions
**1.** Access, skills/use, outcomes.
**2.** Fewer women own a personal phone; lower literacy and safety concerns restrict use (also family norms and content not in their language).
**3.** Gap = 15 points; parity index = 45/60 = **0.75**.
**4.** 41 / 28 = **1.46 times**.
**5.** Sort groups by access per head; plot cumulative population share against cumulative user share; Gini = 1 − Σ(Xᵢ − Xᵢ₋₁)(Yᵢ + Yᵢ₋₁), the area between the diagonal and the curve over the area below the diagonal.
**6.** The scores rank places against the best and worst *in the sample*; a score of 0 only means lowest of those places.
**7.** Their encoding was not standard, so text could not be searched, copied between systems or displayed reliably on the web or phones.
**8.** Digital Foundation, Agriculture, Health, Education, Energy, Tourism, Finance, Urban Infrastructure.
**9.** Shared or community connectivity (solar-powered), digital-literacy training, services in local language and offline/USSD, subsidised devices or community access centres.
**10.** People without access or skills would otherwise be excluded from essential services.
:::

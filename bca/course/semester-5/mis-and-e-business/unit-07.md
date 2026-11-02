---
subject: MIS and e-Business
grade: BCA Semester 5
unit: 7
title: Developing and Justifying Information Systems
hours: 4
area: BCA 304 · MIS and e-Business · Unit 7
---

A hospital wants a new patient-record system. The vendor's quotation is Rs 12,00,000; the manager must answer one question before any programmer is hired: *is it worth it?* This final unit connects the technical chapters to money. It first shows how systems are developed and acquired (SDLC, prototyping, build, buy or outsource), then evaluates the investment with the standard measures: payback, NPV, IRR, ROI, total cost of ownership and break-even.

::: key What this unit gives you
- Development approaches and the build-versus-buy decision; project success factors and risks.
- Cost-benefit analysis: payback, discounted payback, NPV, IRR, profitability index, ROI.
- Total cost of ownership (on-premise versus cloud) and break-even analysis.
- Change management and ethical considerations.
:::

## 7.1 Developing and acquiring information systems

The **systems development life cycle (SDLC)**: investigation and feasibility, analysis (requirements), design, construction or acquisition, testing, implementation (conversion, training), and maintenance. (The *System Analysis and Design* and *Software Engineering* books treat these in detail.) Alternatives to the sequential waterfall approach: **prototyping** (build a quick model to clarify requirements), **agile** (short iterations with working software), **end-user development** (spreadsheets and no-code tools, with the risk of ungoverned data) and **RAD**.

**Build, buy or outsource?**

| Option | Choose when | Advantage | Risk |
|---|---|---|---|
| Build in-house | Unique process that is a source of advantage; skills available | Exact fit, control | Cost, time, key-person risk |
| Buy a package / SaaS | Standard process (accounting, HR) | Fast, proven, lower upfront cost | Fit gaps, vendor dependence |
| Customise a package | Mostly standard, a few special needs | Balance | Upgrades become hard |
| Outsource development or operation | Skills or capacity lacking | Access to expertise | Control, confidentiality, contract lock-in |

**Feasibility** has five facets: **technical** (can it be built?), **economic** (does it pay?), **operational** (will people use it?), **legal** (compliance) and **schedule**. Projects fail mainly for non-technical reasons: unclear requirements, lack of user involvement, scope creep, weak sponsorship and no change management.

## 7.2 Costs and benefits

**Costs** are one-time (hardware, software, development, data migration, training) and recurring (licences or subscriptions, support, staff, power, upgrades). **Benefits** are **tangible** (cash savings, higher revenue, lower inventory) or **intangible** (better decisions, customer satisfaction, compliance), which should be valued where possible, for example by estimating the cost of the errors avoided.

## 7.3 Payback, NPV, IRR and ROI

Money received later is worth less than money today, so cash flows are **discounted**. The **present value** of a cash flow C received in year t at discount rate r is C / (1 + r)ᵗ. The **net present value** is the sum of the discounted flows including the initial investment (negative). **NPV > 0** means the project earns more than the required rate and should be accepted. The **internal rate of return (IRR)** is the discount rate at which NPV = 0; accept if IRR exceeds the required rate. **Payback period** is the time to recover the investment (ignoring the time value of money); **discounted payback** uses discounted flows. **Profitability index (PI)** = PV of inflows ÷ investment.

::: example Hospital record system
Cost Rs 12,00,000 at year 0; net benefits (savings less running costs) in years 1–5 of Rs 3,50,000, 4,00,000, 4,50,000, 4,00,000 and 3,00,000. Required return 12%.

| Year | Cash flow (Rs) | Discount factor 1/1.12ᵗ | Present value (Rs) | Cumulative (Rs) | Cumulative PV (Rs) |
|---|---|---|---|---|---|
| 0 | -12,00,000 | 1.0000 | -12,00,000 | -12,00,000 | -12,00,000 |
| 1 | 3,50,000 | 0.8929 | 3,12,500 | -8,50,000 | -8,87,500 |
| 2 | 4,00,000 | 0.7972 | 3,18,878 | -4,50,000 | -5,68,622 |
| 3 | 4,50,000 | 0.7118 | 3,20,301 | 0 | -2,48,321 |
| 4 | 4,00,000 | 0.6355 | 2,54,207 | 4,00,000 | 5,886 |
| 5 | 3,00,000 | 0.5674 | 1,70,228 | 7,00,000 | 1,76,114 |

- **NPV at 12% = Rs 1,76,114**: positive, so accept.
- **Payback** = **3.00 years** (the cumulative cash flow reaches zero exactly at the end of year 3). **Discounted payback** = **3.98 years**.
- **IRR = 17.82%** (found by bisection; NPV at this rate is 0.0000 within rounding): above 12%, so accept. NPV at 8% is Rs 3,22,421 and at 20% it is **Rs -56,674**, so the NPV profile crosses zero between 12% and 20%, as the IRR says.
- **PI = 1.147**: each rupee invested returns Rs 1.147 in present-value terms.
:::

**Return on investment (ROI)** in its simple accounting form is (average annual net gain) ÷ (initial investment). Total inflows are Rs 19,00,000, so total net gain = 19,00,000 − 12,00,000 = Rs 7,00,000; average per year = Rs **1,40,000**; ROI = 1,40,000 / 12,00,000 = **11.7% per year** (or 58.3% over the whole life). ROI is easy to explain but ignores timing, so use NPV for the decision and ROI for communication. *Accounting rate of return on average investment* uses half the investment as the base: 23.3%.

::: caution Pitfalls of appraisal
Optimistic benefits are the most common error; test the sensitivity of NPV to a 20% lower benefit. IRR can mislead when comparing mutually exclusive projects of different size, or with alternating signs of cash flow (multiple IRRs); prefer NPV. Always include *recurring* costs and the cost of change management.
:::

## 7.4 Total cost of ownership (TCO)

**TCO** counts every cost over the life of the system, not just the purchase price. The usual surprise is that the initial hardware is a minor share. A five-year comparison of an on-premise server against a cloud service for the same office (invented figures; year 0 is purchase and set-up):

| Year | On-premise (Rs) | Cloud (Rs) |
|---|---|---|
| 0 | 11,50,000 | 2,00,000 |
| 1 | 6,90,000 | 8,90,000 |
| 2 | 6,90,000 | 8,80,000 |
| 3 | 6,90,000 | 9,20,000 |
| 4 | 6,90,000 | 9,60,000 |
| 5 | 6,90,000 | 10,00,000 |
| **5-year TCO** | **46,00,000** | **48,50,000** |

**On-premise costs Rs 46,00,000 over five years (Rs 9,20,000 a year); cloud costs Rs 48,50,000**, so on-premise minus cloud = Rs -2,50,000 undiscounted. But on-premise spends heavily at year 0, and discounting at 12% gives a present cost of Rs 36,37,296 for on-premise against Rs 35,28,536 for cloud: **cloud is cheaper in present-value terms**. The comparison flips when the discount rate or the subscription growth changes, so state the assumptions. Non-financial factors (data residency, connectivity in the region, control, compliance, skills) decide close cases.

## 7.5 Break-even analysis

**Break-even** is the volume at which revenue equals cost. With fixed cost F per year, price p and variable cost v per unit, break-even quantity = F / (p − v), where p − v is the **contribution margin**. An online service has Rs 1,80,000 fixed annual cost, earns Rs 30 per transaction and spends Rs 12 per transaction on variable costs. Contribution = **Rs 18** per transaction (60% of price), so break-even = 1,80,000 / 18 = **10,000 transactions a year**, which is revenue of Rs 3,00,000. At 20,000 transactions the annual profit would be 20,000 × 18 − 1,80,000 = **Rs 1,80,000**. A system that cannot realistically exceed its break-even volume should not be built.

## 7.6 Managing change and ethics

Systems change jobs; plan the human side. Typical stages: engage users early, communicate benefits and what changes, train *before* go-live, support staff during the first weeks, and measure adoption. **Ethical issues:** privacy of customers and employees, accuracy of information, intellectual property, access (who is excluded?), and accountability for automated decisions. A code of ethics (ACM, IEEE, a national IT body) offers a reference. Keep the post-implementation review: compare actual benefits and costs with the business case and record lessons.

## Chapter summary

- Choose build, buy, customise or outsource on fit, cost, skills and risk; failures are usually organisational.
- Discount cash flows; accept projects with NPV > 0 or IRR above the required rate; payback and ROI are simple supplements.
- TCO includes all lifetime costs; compare options at present value.
- Break-even volume = fixed cost ÷ contribution margin.
- Change management and post-implementation review complete the investment cycle.

## Practice

1. List the stages of the SDLC and three reasons projects fail.
2. When would you build rather than buy?
3. A project costs Rs 5,00,000 and returns Rs 2,00,000 for each of 3 years. Compute payback and simple ROI.
4. For the same project at 10%, compute the NPV and say whether to accept.
5. Define IRR and state the acceptance rule.
6. Why can IRR mislead when comparing projects?
7. Why might cloud TCO be lower in present value even if the nominal total is higher?
8. Fixed cost Rs 2,40,000, price Rs 50, variable cost Rs 20. Compute the break-even volume.
9. How much profit at 10,000 units in question 8?
10. Name three actions for managing user adoption.

::: note Answers and worked solutions
**1.** Investigation/feasibility, analysis, design, construction, testing, implementation, maintenance. Failures: unclear requirements, weak user involvement, scope creep.
**2.** When the process is unique and a source of advantage, no package fits, and the skills exist.
**3.** Payback = 5,00,000 / 2,00,000 = 2.5 years. Total gain = 6,00,000 − 5,00,000 = 1,00,000; per year 33,333; ROI = 33,333 / 5,00,000 = 6.7% per year.
**4.** Annuity factor at 10% for 3 years = 2.4869; PV = 2,00,000 × 2.4869 = 4,97,370; NPV = 4,97,370 − 5,00,000 = **−2,630**: marginally negative, so reject (or negotiate).
**5.** The discount rate at which NPV is zero; accept when IRR is above the required rate.
**6.** It ignores project scale, can give multiple values when cash-flow signs alternate, and may rank mutually exclusive projects differently from NPV.
**7.** Cloud defers costs (low year-0 spending) and discounting makes later costs smaller.
**8.** 2,40,000 / (50 − 20) = **8,000 units**.
**9.** 10,000 × 30 − 2,40,000 = **Rs 60,000**.
**10.** Early involvement, training before go-live, visible management support and post-go-live help.
:::

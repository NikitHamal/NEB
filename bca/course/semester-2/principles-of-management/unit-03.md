---
subject: Principles of Management
grade: BCA Semester 2
unit: 3
title: Planning and Decision Making
area: BCA 156 · Principles of Management · Unit 3
---

Planning decides *what* to do and *how*; decision making is the act of choosing at every step. This unit covers the types and hierarchy of plans, the planning process, strategic planning with SWOT, quantitative planning tools (break-even, decision tables and trees, critical path), decision making under certainty, risk and uncertainty, and problem solving. All the numbers below were recomputed by `tools/check_management.py`.

::: key What this unit gives you
- Concept, types, hierarchy and process of planning; importance and limits.
- Management by objectives (MBO); strategic planning; environmental scanning; SWOT.
- Quantitative tools: break-even analysis, decision tables and trees, critical-path scheduling.
- Decision making: approaches, types, certainty / risk / uncertainty criteria.
- Problem solving: types and strategies.
:::

## 3.1 Concept and importance of planning

**Planning** is deciding in advance what to do, when, how and who will do it; it bridges *where we are* and *where we want to be*. It is the first function: organising, leading and controlling all depend on it. **Importance**: gives direction; reduces uncertainty and risk; reduces waste and overlapping; sets standards for control; encourages innovation and foresight; improves coordination. **Limitations**: costs time and money; plans can be rigid; the future cannot be predicted exactly; may hinder initiative; internal and external changes make plans obsolete — so plans are reviewed and made flexible.

## 3.2 Types and hierarchy of plans

| Basis | Types |
|---|---|
| **By level / scope** | **Strategic** (top management, long term, whole organisation), **tactical** (middle, medium term, departments), **operational** (first-line, short term, daily work) |
| **By time** | long-range (> 5 years), medium (1–5), short (< 1 year) |
| **By use** | **Standing plans** — used repeatedly: **policies** (broad guides to decisions, e.g. "promote from within"), **procedures** (step-by-step methods), **rules** (specific do/don't, no discretion). **Single-use plans** — **programmes**, **projects**, **budgets** |
| **By specificity** | specific vs directional |
| **By contingency** | **contingency plans** (a "plan B" if assumptions fail) |

### The hierarchy of planning

```
Mission and vision (why we exist; the long-term picture)
   └─ Objectives / goals (what results, by when)
        └─ Strategies (how to use resources to reach objectives)
             └─ Policies (guides to decisions)
                  └─ Procedures (sequences of steps)
                       └─ Rules (specific requirements)
                            └─ Programmes, projects and budgets (the detailed single-use plans)
```
Each plan serves the one above it, which keeps the organisation consistent from mission to daily work.

## 3.3 The planning process

1. **Be aware of the opportunity**, through environmental scanning and self-analysis.
2. **Set objectives**, specific and measurable (SMART).
3. **Develop planning premises** — assumptions about the future (forecasts of demand, inflation, exchange rates, technology, policy). Premises must be agreed so that all plans rest on the same assumptions.
4. **Identify alternatives.**
5. **Evaluate alternatives** against objectives, risk, cost and resources.
6. **Choose the best alternative** (decision making).
7. **Formulate derivative (supporting) plans** — budgets, schedules, policies.
8. **Implement**, then **monitor and control** (which feeds back to step 1).

### Management by objectives (MBO)
A participative planning and control technique (Peter Drucker): superiors and subordinates **jointly set objectives**, define each person's key results, review progress regularly and appraise by results. Steps: set organisational goals → cascade to departments and individuals → agree on action plans → monitor → appraise and reward → reset. *Advantages*: clarity, commitment, motivation, objective appraisal. *Limitations*: time-consuming paperwork, emphasis on the measurable and short-term, rigid goals in a changing environment.

## 3.4 Strategic planning

A **strategy** is a comprehensive, long-term plan of how the organisation will use its resources to reach its goals and achieve **competitive advantage**. **Strategic planning** has five stages: (1) define mission, vision and objectives; (2) analyse the environment and the organisation; (3) formulate strategies; (4) implement; (5) evaluate and control.

### Environmental scanning
Systematically collecting and analysing information about the external environment (economic, social, political, technological, competitors, customers) and internal strengths. **Methods**: reading published reports and news; analysing statistics; surveys of customers and suppliers; competitor intelligence; **expert opinion and the Delphi method**; **scenario planning**; **trend extrapolation**; attending trade shows; **PEST analysis**; **Porter's five forces** (rivalry, new entrants, substitutes, buyer power, supplier power).

### SWOT analysis

| | **Helpful** | **Harmful** |
|---|---|---|
| **Internal** | **Strengths** — what we do well | **Weaknesses** — what we lack |
| **External** | **Opportunities** — favourable outside trends | **Threats** — unfavourable outside trends |

::: example Worked example: SWOT for a Pokhara software start-up
**Strengths**: skilled young developers, low cost. **Weaknesses**: no brand, limited capital. **Opportunities**: global demand for outsourcing, government support for ICT. **Threats**: brain drain, unstable power and internet, foreign competitors. Strategies by pairing: **SO** (use strengths to take opportunities: bid for overseas contracts), **WO** (overcome weaknesses using opportunities: partner with a foreign firm), **ST** (use strengths against threats: retention bonuses), **WT** (defend: save capital, avoid risky projects).
:::

### Formulating and implementing strategy
Levels: **corporate strategy** (what business to be in: growth, stability, retrenchment), **business strategy** (how to compete: cost leadership, differentiation, focus — Porter) and **functional strategy**. **Implementation** requires structure, resources, leadership, culture, policies and a budget; **evaluation** compares results with objectives. The **BCG matrix** (stars, cash cows, question marks, dogs) helps decide which businesses to invest in.

## 3.5 Quantitative tools for planning

### Break-even analysis

The **break-even point (BEP)** is the volume of sales at which revenue equals total cost — no profit, no loss.

**BEP (units) = Fixed cost ÷ (Price − Variable cost per unit)**; **BEP (sales value) = BEP units × price** = FC ÷ contribution margin ratio; **units for target profit = (FC + profit) ÷ contribution per unit**.

::: example Worked example: break-even
A shop's fixed costs are Rs 60,000 per month; each item sells for Rs 50 and costs Rs 30 to buy and handle. Contribution per unit = 50 − 30 = Rs 20 (the **contribution margin ratio** is 20/50 = **40 %**).

- **BEP = 60,000 ÷ 20 = 3,000 units** = Rs 1,50,000 of sales.
- For a profit of Rs 20,000: (60,000 + 20,000) ÷ 20 = **4,000 units**.
- At 3,500 units: profit = 3,500 × 20 − 60,000 = **Rs 10,000**.
- **Margin of safety** at 4,000 units = (4,000 − 3,000)/4,000 = **25 %** (sales can fall 25 % before losses begin).
Use: decide prices, volumes and whether to launch a product. Assumes costs and prices are linear and that everything produced is sold.
:::

### Decision tables and decision trees
A **payoff table** lists alternatives (rows), states of nature (columns) and the payoffs; a **decision tree** shows decisions (squares), chance events (circles), probabilities and payoffs, and is solved from right to left by computing **expected values**.

::: example Worked example: decision tree
A firm can build a **big** plant or a **small** plant. Demand is high with probability 0.6 and low with 0.4. Big plant: +Rs 200 lakh if high, −Rs 80 lakh if low. Small plant: +60 lakh if high, +10 lakh if low.
EV(big) = 0.6 × 200 + 0.4 × (−80) = 120 − 32 = **Rs 88 lakh**. EV(small) = 0.6 × 60 + 0.4 × 10 = 36 + 4 = **Rs 40 lakh**. Choose the **big plant** on expected value (a risk-averse owner might still prefer the small plant because it cannot lose).
:::

### Critical path method (CPM) and PERT
Projects are drawn as a network of activities with durations; the **critical path** is the **longest path** through the network and fixes the project duration. Activities on it have zero **slack** (delay one and the project is delayed); others have slack.

::: example Worked example: critical path
Activities: A (4 weeks) first; B (6 weeks) and C (5 weeks) both follow A; D (3 weeks) follows both B and C. Paths: A–B–D = 4 + 6 + 3 = **13 weeks**; A–C–D = 4 + 5 + 3 = 12 weeks. The **critical path is A–B–D, 13 weeks**; activity C has **1 week of slack**.
**PERT** handles uncertain durations with three estimates — optimistic *a*, most likely *m*, pessimistic *b*: expected time **tₑ = (a + 4m + b)/6**, variance **((b − a)/6)²**. For activity (2, 4, 6): tₑ = 24/6 = 4; for (3, 5, 13): tₑ = (3 + 20 + 13)/6 = 6.0 and variance (10/6)² = 2.78.
:::

Also used: **Gantt charts** (bars on a calendar), **forecasting** (moving averages, regression), **linear programming**, **queuing** and **inventory models**. Economic order quantity **EOQ = √(2DS/H)**: with annual demand D = 1,200, ordering cost S = Rs 50 and holding cost H = Rs 6 per unit per year, EOQ = √20,000 ≈ **141 units**.

## 3.6 Decision making

**Decision making** is the process of **choosing the best alternative** from the available ones to solve a problem or exploit an opportunity. It is a core managerial activity.

### Approaches

- **Rational (classical) model**: define the problem, list all alternatives, evaluate them, pick the optimum. Assumes complete information and a clear goal — rarely true.
- **Bounded rationality / administrative (Simon)**: limited information, time and thinking capacity; managers **satisfice** — accept the first solution that is good enough.
- **Intuitive**: experience-based, quick, for familiar situations.
- **Political / garbage-can**: decisions reflect power and chance as well as analysis.
- **Behavioural biases** to watch: anchoring, overconfidence, confirmation bias, escalation of commitment (throwing good money after bad), groupthink.

### Types of decisions

| Basis | Types |
|---|---|
| **Frequency** | **programmed** (routine, rule-based: reorder stock when it falls below 50) vs **non-programmed** (new, unstructured: enter a new market) |
| **Level** | strategic, tactical, operational |
| **Participants** | individual vs group (group: more ideas and acceptance, but slower; risk of groupthink) |
| **Importance** | major vs minor; **routine** vs **adaptive** vs **innovative** |
| **Certainty** | certainty, risk, uncertainty |

### The decision-making process

1. **Identify and define the problem** (distinguish symptoms from causes).
2. **Identify decision criteria** and their weights.
3. **Develop alternatives.**
4. **Analyse** each alternative (costs, benefits, risks).
5. **Select** the best.
6. **Implement.**
7. **Follow up and evaluate** the results; learn.

### Decision making under certainty, risk and uncertainty

- **Certainty**: outcomes are known. Choose the alternative with the best result (**weighted score**: 0.5 × 8 + 0.3 × 6 + 0.2 × 9 = **7.6**).
- **Risk**: the outcomes' **probabilities** are known: use the **expected monetary value (EMV)**.
- **Uncertainty**: probabilities unknown: use decision criteria that reflect your attitude.

::: example Worked example: payoff table (Rs thousand)
States of nature: S1 (boom), S2 (normal), S3 (slump). Probabilities (for risk): 0.3, 0.5, 0.2.

| Alternative | S1 | S2 | S3 |
|---|---|---|---|
| A: expand | 80 | 50 | −20 |
| B: moderate | 60 | 40 | 10 |
| C: hold | 45 | 40 | 30 |

**Under risk (EMV):** A = 0.3 × 80 + 0.5 × 50 + 0.2 × (−20) = 24 + 25 − 4 = **45**; B = 18 + 20 + 2 = **40**; C = 13.5 + 20 + 6 = **39.5** → choose **A**. *Expected value of perfect information* = 0.3 × 80 + 0.5 × 50 + 0.2 × 30 − 45 = 55 − 45 = **10** (the most it is worth paying for a perfect forecast).
**Under uncertainty (no probabilities):**

- **Maximax (optimist)**: best of the best: A 80, B 60, C 45 → **A**.
- **Maximin (Wald, pessimist)**: best of the worst: A −20, B 10, C 30 → **C**.
- **Laplace (equal likelihood)**: averages A 36.67, B 36.67, C 38.33 → **C**.
- **Hurwicz** with optimism α = 0.7: A = 0.7 × 80 + 0.3 × (−20) = **50**; B = 42 + 3 = **45**; C = 31.5 + 9 = **40.5** → **A**.
- **Minimax regret (Savage)**: regret = best payoff in the column − payoff. Column bests 80, 50, 30. Regrets: A (0, 0, 50) max 50; B (20, 10, 20) max **20**; C (35, 10, 0) max 35 → choose **B** (smallest maximum regret).
Different attitudes give different answers — which is the point: the criterion expresses the decision maker's attitude to risk.
:::

### Group decision techniques
**Brainstorming** (generate ideas without criticism), **nominal group technique** (silent writing, then ranked voting), **Delphi** (anonymous expert rounds), **devil's advocate**, **electronic meetings**.

## 3.7 Problem solving

A **problem** is a gap between the actual and the desired state. Types: **structured** (known, routine, clear solution) vs **unstructured** (novel, ambiguous); **crisis**, **non-crisis** and **opportunity** problems.

**Steps**: (1) **recognise and define** the problem (ask "why" five times to reach the root cause); (2) **gather facts and analyse causes** (cause-and-effect/fishbone diagram, Pareto chart); (3) **generate solutions**; (4) **evaluate and choose**; (5) **implement**; (6) **review**.

**Strategies/techniques**: **fishbone (Ishikawa) diagram** (categories of causes: people, method, machine, material, measurement, environment); **5 Whys**; **Pareto analysis** (about 80 % of effects come from 20 % of causes: if two of ten causes account for 15 of 25 complaints, that is 60 %, so fix those first); **brainstorming**; **trial and error**; **lateral thinking**; **algorithmic** (step-by-step rules) vs **heuristic** (rules of thumb); **PDCA**.

## Formula and fact sheet

- BEP units = FC ÷ (P − VC); target-profit units = (FC + profit) ÷ contribution; margin of safety = (actual − BEP) ÷ actual.
- Critical path = longest path; slack = 0 on it. PERT tₑ = (a + 4m + b)/6.
- EMV = Σ probability × payoff; EVPI = EV with perfect information − best EMV.
- Uncertainty criteria: maximax (optimist), maximin (pessimist), Laplace (average), Hurwicz (α-weighted), minimax regret.
- Plan hierarchy: mission → objectives → strategies → policies → procedures → rules → programmes/budgets.
- SWOT pairs: SO, WO, ST, WT. EOQ = √(2DS/H).

## Chapter summary

- Planning gives direction and a basis for control; strategic, tactical and operational plans fit into a hierarchy from mission to rules; the planning process runs from premises to evaluated, controlled implementation.
- MBO makes planning participative; strategic planning uses environmental scanning and SWOT.
- Break-even, decision trees, PERT/CPM and EOQ are practical quantitative tools.
- Decisions are programmed or non-programmed and made under certainty, risk or uncertainty, each with its own criteria; real managers satisfice.
- Problem solving finds root causes with fishbone, 5 Whys and Pareto analysis.

## Practice

1. Define planning; explain its importance and limitations.
2. Explain the types of plans and the hierarchy of plans.
3. Describe the planning process and explain MBO.
4. What is environmental scanning? Prepare a SWOT of a college computer lab.
5. A product sells at Rs 80, variable cost Rs 50, fixed cost Rs 90,000. Find the BEP in units and value, and units for Rs 30,000 profit.
6. Solve the decision tree: build (EV) a big shop with 0.5 chance of Rs 300 lakh and 0.5 chance of −Rs 100 lakh versus a small shop with a certain Rs 70 lakh.
7. Activities: A 3, B 5 (after A), C 7 (after A), D 2 (after B and C). Find the critical path and the slack of B.
8. Apply maximax, maximin and minimax regret to the table of 3.6.
9. Differentiate programmed and non-programmed decisions; explain the decision-making process.
10. Explain the steps of problem solving with a fishbone example for "late assignments".

::: note Answers and worked solutions
**1.** Planning = deciding in advance what, how, when and who. Importance: direction, lower risk, standards for control, coordination; limitations: cost, rigidity, uncertain future.
**2.** Strategic/tactical/operational; standing (policies, procedures, rules) and single-use (programmes, budgets); hierarchy from mission to budgets (3.2).
**3.** Steps in 3.3; MBO: superiors and subordinates jointly set measurable objectives, review progress and appraise results.
**4.** Scanning = collecting and analysing external information. SWOT sample: S — modern PCs, qualified instructor; W — limited lab hours; O — industry demand for skills; T — equipment obsolescence, power cuts.
**5.** Contribution = 80 − 50 = 30. BEP = 90,000/30 = **3,000 units** = Rs 2,40,000. For Rs 30,000 profit: (90,000 + 30,000)/30 = **4,000 units**.
**6.** Big: 0.5 × 300 + 0.5 × (−100) = 150 − 50 = **Rs 100 lakh**; small: **Rs 70 lakh** certain. Choose big on EV; the small shop is safer.
**7.** A–B–D = 3 + 5 + 2 = 10; A–C–D = 3 + 7 + 2 = 12. **Critical path A–C–D, 12 days**; slack of B = 12 − 10 = **2**.
**8.** Maximax → A (80); maximin → C (30); minimax regret → B (max regret 20).
**9.** Programmed: routine and rule-based; non-programmed: new and unstructured. Process: define the problem → criteria → alternatives → analyse → select → implement → follow up.
**10.** Define the gap (assignments are late) → analyse causes with a fishbone (People: poor time management; Method: unclear deadlines; Machine: no computers; Material: no references; Environment: noisy hostel) → choose solutions → implement (staged deadlines) → review.
:::

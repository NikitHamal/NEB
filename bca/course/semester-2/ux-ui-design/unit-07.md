---
subject: UX/UI Design
grade: BCA Semester 2
unit: 7
title: Design Evaluation
area: BCA 155 · UX/UI Design · Unit 7
hours: 6
---

A design that nobody has tested is a guess. Evaluation is how you find out whether a design works for real people. This unit covers formative and summative evaluation, usability testing (moderated and unmoderated), analysing results, expert and participatory evaluation, evaluation paradigms, the DECIDE framework, heuristic evaluation, and task analysis with performance metrics.

::: key What this unit gives you
- Formative versus summative evaluation.
- Usability testing: planning, moderated vs unmoderated, running a session, how many users.
- Analysing test results: metrics, SUS scoring, severity ratings.
- Evaluation by experts and with users; evaluation paradigms.
- The DECIDE framework; Nielsen's ten heuristics; task analysis and performance metrics.
:::

## 7.1 Why and when to evaluate

Evaluation checks that a design meets users' needs and the requirements, and finds problems while they are cheap to fix. It should be **iterative**: design → evaluate → redesign, repeating throughout the project.

### Formative evaluation
Done **during** design, on sketches, wireframes and prototypes, to **form** (improve) the design. **Qualitative**, quick, small samples (3–8 users), many cycles. Questions: *What is confusing? What should change?* Examples: paper-prototype test, heuristic review of a wireframe, think-aloud sessions on a clickable prototype.

### Summative evaluation
Done **after** (or at the end of) design, on a finished or near-final product, to **sum up** how well it performs against goals or competitors. Usually **quantitative**, larger samples, controlled conditions. Questions: *Does it meet the target (e.g. 90 % task success)? Is version B better than A?* Examples: benchmark test, A/B test, SUS survey, comparison against a competitor.

| | **Formative** | **Summative** |
|---|---|---|
| When | during design | at the end / after release |
| Goal | improve | judge, compare, certify |
| Data | mostly qualitative | mostly quantitative |
| Sample | small (3–8) | larger (20–100+) |
| Output | list of problems and fixes | scores and statistics |
| Product state | prototype | working product |

## 7.2 Usability testing

**Usability testing** observes **representative users attempting realistic tasks** with the product, to see where they succeed and struggle. Its core rule: **watch what they do, not what they say.**

### Planning a test

1. **Goals and questions**: what do you want to learn? ("Can new students find and pay the exam fee?")
2. **Participants**: recruit people who match the personas (5–8 for qualitative testing); screen them; get **informed consent**; compensate fairly.
3. **Tasks and scenarios**: realistic, goal-based, **not instructions**: Good: "You need to pay your exam fee before Friday. Show me how you would do it." Bad: "Click the *Payments* tab."
4. **Environment and equipment**: lab, the user's own place, or remote; device; screen and audio recording.
5. **Metrics**: what will you measure (below)?
6. **Script**: welcome, think-aloud instructions, tasks, follow-up questions, thanks.
7. **Pilot** the test with a colleague.

### Moderated versus unmoderated

| | **Moderated** | **Unmoderated** |
|---|---|---|
| Facilitator | a person guides the session, live or by video | none; the participant works alone with a tool (Maze, UserTesting, Lookback) |
| Probing | can ask "why?" and follow up | only written follow-up questions |
| Sample and speed | few participants, scheduled, slow | many participants, fast, cheap |
| Data | deep qualitative insight, facial and verbal cues | quantitative at scale (success, time, clicks), less context |
| Risks | moderator bias; leading questions | participants not serious; no recovery if they misunderstand a task |
| Best for | early prototypes, complex tasks, discovering *why* | validating a design, benchmarking, reaching many/diverse users |

Either can be **in-person** or **remote**. **Think-aloud**: the user speaks their thoughts while working ("I'm looking for payments… maybe under Profile?"). **Retrospective think-aloud** reviews a recording afterwards.

### Running the session (moderator rules)
Be neutral; do not help or lead; if the user asks "Is this right?", reply "What would you expect?"; stay silent during pauses; note **behaviour** (hesitation, wrong clicks, errors, quotes), not opinions only; stop a task when the user gives up or time runs out; record success/failure; end with debrief questions and a **SUS** questionnaire.

### How many users?
Nielsen and Landauer's model: the proportion of problems found by n users is **1 − (1 − L)ⁿ**, where L ≈ **0.31** is the average chance that one user hits a given problem. n = 3 → **67 %**; n = 5 → **84 %**; n = 15 → **99.6 %**. So **five users per round** find most problems, and it is better to test five users, fix, then test five more, than to test fifteen once. (Quantitative studies need ≥ 20.) Test with each distinct user *group*.

## 7.3 Analysing test results

### Measures and metrics

| Metric | Definition | Example |
|---|---|---|
| **Task success (completion) rate** | % of users who complete a task | 17 of 20 = **85 %** |
| **Time on task** | seconds to complete (successful attempts) | mean of 42, 55, 38, 61, 47 = **48.6 s** (median 47 s) |
| **Error rate** | errors per task or % of tasks with errors | 6 errors in 20 task attempts = **0.3 errors per task** |
| **Clicks / steps** | steps needed vs the minimum | 9 clicks where 4 would do |
| **Satisfaction** | questionnaires (SUS, SEQ, NPS) | SUS = 85 |
| **Learnability** | improvement over repeated trials | time falls from 90 s to 40 s by trial 3 |
| **Efficiency** | success per unit time (or goals ÷ time) | 6 tasks in 30 min |

### SUS — System Usability Scale

A 10-item questionnaire rated 1 (strongly disagree) to 5 (strongly agree), alternating positive (odd) and negative (even) statements: *I think I would like to use this system frequently; I found the system unnecessarily complex; I thought it was easy to use; …* **Scoring**: odd items contribute (response − 1), even items contribute (5 − response); add the ten contributions (0–40) and multiply by **2.5** for a score of 0–100.

::: example Worked example: SUS
Responses to items 1–10: 4, 2, 5, 1, 4, 2, 5, 1, 4, 2. Odd items (1, 3, 5, 7, 9): (4−1) + (5−1) + (4−1) + (5−1) + (4−1) = 3 + 4 + 3 + 4 + 3 = 17. Even items (2, 4, 6, 8, 10): (5−2) + (5−1) + (5−2) + (5−1) + (5−2) = 3 + 4 + 3 + 4 + 3 = 17. Sum = 34; **SUS = 34 × 2.5 = 85**. Interpretation: the **average SUS is about 68**; above 80 is excellent (grade A), below 51 is poor. (All neutral answers give 50; the best possible pattern gives 100. Do not read SUS as a percentage.)
:::

### Qualitative analysis and severity
Collect observations on notes, **cluster** by theme (affinity diagram), count how many users hit each problem, and write each as a **finding** (what happened, where, why, evidence/quote, recommendation). Rate each by **severity**:

| Rating | Meaning |
|---|---|
| 0 | not a usability problem |
| 1 | cosmetic — fix if time |
| 2 | minor — low priority |
| 3 | major — important to fix |
| 4 | catastrophic — must fix before release |

Priority = **severity × frequency** (and fix effort). The test report: goals, method, participants, tasks, results (metrics + findings), prioritised **recommendations**, highlights video clips. Report positive findings too.

### A/B testing
A summative technique: show version A to one random group and B to another and compare a metric. Example: A converts 40 of 800 visitors (**5.0 %**), B converts 56 of 800 (**7.0 %**): an uplift of (7 − 5)/5 = **40 %**; check **statistical significance** before acting. Needs enough traffic; tests *what* works, not *why*. Related metrics: click-through rate (30 clicks / 600 visitors = 5 %), bounce rate, conversion.

## 7.4 Evaluation through expert analysis and user participation

| | **Expert (inspection) methods** | **User-participation methods** |
|---|---|---|
| Who | usability specialists or designers | real users |
| Methods | **heuristic evaluation**, cognitive walkthrough, guideline/standards review, consistency inspection, expert review of accessibility | usability tests, think-aloud, field studies, questionnaires, interviews, focus groups, diary studies, A/B tests, analytics |
| Speed and cost | fast, cheap, no recruitment | slower, costlier |
| Finds | violations of principles; obvious problems; consistency issues | real behaviours, the *why*, context problems, surprises |
| Weakness | experts are not users; false alarms | small samples; artificial setting |

Use both: experts clear obvious problems first, then users find what experts cannot predict.

**Cognitive walkthrough**: a specialist steps through a task asking at each step: *Will the user try to achieve the right effect? Will they notice that the correct action is available? Will they associate the action with the effect? If the correct action is performed, will they see that progress is being made?* — good for learnability by first-time users.

### Evaluation paradigms (Preece et al.)

| Paradigm | Description |
|---|---|
| **"Quick and dirty"** | informal feedback from users or consultants at any stage; fast, cheap; the aim is to confirm ideas, not to produce rigorous data |
| **Usability testing** | measuring users' performance on typical tasks, often in a lab, with video, logs and questionnaires; mostly quantitative plus observation |
| **Field studies** | evaluation in the natural environment (home, workplace, village) to see real use and context; ethnography, interviews, observation |
| **Predictive evaluation** | experts predict usability problems without users: heuristics, walkthroughs; and **models** like **GOMS/KLM** and **Fitts's law** to predict performance |

**Iterative evaluation** means evaluating at each cycle with progressively higher-fidelity artefacts, so that findings drive the next version: sketch → wireframe test → prototype test → beta field test → post-release analytics.

## 7.5 The DECIDE framework

Preece, Rogers and Sharp's **DECIDE** is a checklist for **planning an evaluation**:

| Letter | Step | Questions |
|---|---|---|
| **D** | **Determine** the goals | What are the high-level goals? Who wants it and why? (e.g. "check whether new users can register in under 2 minutes") |
| **E** | **Explore** the questions | Break the goals into specific questions ("Can users find the sign-up button?") |
| **C** | **Choose** the evaluation approach and methods | Usability test, heuristic review, questionnaire, field study, A/B test — and budget and time |
| **I** | **Identify** the practical issues | Participants, facilities, equipment, schedule, budget, expertise, consent |
| **D** | **Decide** how to deal with the ethical issues | Informed consent, privacy and anonymity, right to withdraw, data protection, no harm |
| **E** | **Evaluate, interpret and present** the data | Reliability, validity, scope, biases, ecological validity; report the findings clearly |

Ethics: tell participants the purpose and what is recorded; stress that **the product, not the person, is being tested**; allow them to stop at any time; store data safely and anonymise.

## 7.6 Heuristic evaluation

Developed by **Jakob Nielsen and Rolf Molich**. Several evaluators (3–5 is ideal; one finds only ~35 % of problems) each inspect the interface independently against recognised **heuristics**, then combine their lists. Steps: choose heuristics; brief evaluators; each evaluator walks through the interface at least twice and records each problem with the heuristic violated and a **severity**; hold a debrief to merge and prioritise.

### Nielsen's 10 usability heuristics

| # | Heuristic | Example of a violation |
|---|---|---|
| 1 | **Visibility of system status** — keep users informed with timely feedback | no progress indicator after pressing Pay |
| 2 | **Match between system and the real world** — users' language, familiar concepts | "Authentication failure code 17" |
| 3 | **User control and freedom** — undo, cancel, easy exit | no way to cancel a booking |
| 4 | **Consistency and standards** — same words and actions mean the same | "Submit" in one place and "Send" in another for the same action |
| 5 | **Error prevention** — design to avoid mistakes; confirm destructive actions | Delete next to Save with no confirmation |
| 6 | **Recognition rather than recall** — show options; don't make people remember | asking for a code shown on a previous page |
| 7 | **Flexibility and efficiency of use** — accelerators for experts, personalisation | no keyboard shortcuts or saved addresses |
| 8 | **Aesthetic and minimalist design** — no irrelevant information | a cluttered dashboard hiding the main action |
| 9 | **Help users recognise, diagnose and recover from errors** — plain language, precise cause, constructive fix | "Invalid input" without saying which field or why |
| 10 | **Help and documentation** — searchable, task-focused, concise | no help for a complex form |

Strengths: cheap, quick, no users needed. Weaknesses: evaluators' bias, may miss real-user problems, false positives; therefore combine with user testing.

## 7.7 Task analysis and performance metrics

**Task analysis** breaks a user's task into **goals, sub-goals, actions and decisions** to understand how it is done, and to find ways to simplify it.

**Hierarchical Task Analysis (HTA)** decomposes a goal into sub-tasks with a **plan** saying in what order and under what conditions they are done.

::: example Worked example: HTA — pay exam fee
**0. Pay exam fee** (plan 0: do 1, then 2, then 3; repeat 2 if payment fails)

1. Log in — 1.1 enter email, 1.2 enter password, 1.3 press Log in.
2. Pay fee — 2.1 open Payments, 2.2 select exam, 2.3 choose eSewa, 2.4 confirm in eSewa.
3. Save receipt — 3.1 view receipt, 3.2 download.
Insights: 9 actions at the lowest level; steps 2.1–2.2 could be merged by showing the due fee on the home screen — a design improvement from the analysis.
:::

**GOMS** (Goals, Operators, Methods, Selection rules) is a family of models that predict expert, error-free performance. The simplest is the **Keystroke-Level Model (KLM)**, which adds standard operator times: **K** keystroke ≈ 0.2 s, **P** point with mouse ≈ 1.1 s, **B** mouse button press/release ≈ 0.1 s (click = 2B), **H** move hand between keyboard and mouse ≈ 0.4 s, **M** mental preparation ≈ 1.35 s.

::: example Worked example: KLM times
**Search a site:** M + P + click (2 B) + type 10 characters (10 K) + Enter (K) = 1.35 + 1.1 + 0.2 + 2.0 + 0.2 = **4.85 s**.
**Log in:** M + P + click (2 B) + H + type 8-character username (8 K) + Tab (K) + 8-character password (8 K) + Enter (K) = 1.35 + 1.1 + 0.2 + 0.4 + 1.6 + 0.2 + 1.6 + 0.2 = **6.65 s**.
A design that lets the browser autofill both fields would remove 16 K and the H operator, saving about 3.6 s per login. KLM lets you compare designs on paper, before any user test.
:::

### Performance metrics (summary)
Use measures tied to goals: **effectiveness** (task success, error rate), **efficiency** (time on task, number of steps, KLM-predicted time) and **satisfaction** (SUS, ratings). Set **targets** in advance (e.g. "≥ 90 % complete registration unaided; median time ≤ 90 s; SUS ≥ 80") and compare the measured values with them. Also analytics: drop-off in a funnel, conversion, bounce, search queries with no results, rage clicks.

## Formula and fact sheet

- Formative = during, improve, qualitative; summative = after, judge, quantitative.
- Moderated = depth and *why*; unmoderated = scale and speed. Think-aloud.
- Problems found by n users = 1 − (1 − 0.31)ⁿ: n = 3 → 67 %, n = 5 → 84 %, n = 15 → 99.6 %.
- Success rate = completed/attempted; error rate = errors/tasks; mean time on task.
- SUS = (Σ(odd − 1) + Σ(5 − even)) × 2.5; average ≈ 68; neutral = 50.
- Severity 0–4; priority = severity × frequency. A/B uplift = (B − A)/A.
- DECIDE: Determine, Explore, Choose, Identify, Decide, Evaluate.
- KLM: K 0.2, P 1.1, B 0.1, H 0.4, M 1.35 seconds.

## Chapter summary

- Evaluate iteratively: formative evaluation improves a design while it is made, summative evaluation judges the result.
- Usability tests observe representative users on realistic tasks; moderated tests give depth, unmoderated tests give scale; five users per round find most problems.
- Analyse with success rate, time, errors, SUS and severity-rated findings, then recommend fixes by priority.
- Expert methods (heuristic evaluation, walkthroughs) and user methods complement each other; paradigms range from quick-and-dirty to field studies and predictive models.
- DECIDE structures an evaluation plan; Nielsen's ten heuristics structure an expert review.
- Task analysis (HTA) and KLM predict and compare task effort.

## Practice

1. Differentiate formative and summative evaluation with examples.
2. Compare moderated and unmoderated usability testing.
3. Plan a usability test for a college fee-payment app: goals, participants, three tasks, metrics.
4. How many users find 75 % of the problems if L = 0.31? (Find the smallest n.)
5. Compute SUS for responses 5, 1, 4, 2, 5, 1, 4, 2, 5, 1 and interpret.
6. Twelve users attempt a task; 9 succeed. Times (s) for the successful ones: 30, 35, 28, 40, 33, 31, 45, 38, 36. Find the success rate and mean time.
7. Explain DECIDE with one line per letter.
8. List Nielsen's ten heuristics and identify which one is violated by (a) "Error 404x7" and (b) no undo after deleting a message.
9. Draw an HTA for "withdraw cash from an ATM".
10. Use KLM to compare logging in by typing 8 + 8 characters with using a fingerprint (M + P-free single touch, assume M + 1 key press of 0.2 s).

::: note Answers and worked solutions
**1.** Formative: during design, qualitative, e.g. testing a paper prototype with 5 users; summative: after release, quantitative, e.g. an A/B test or benchmark with 50 users against targets.
**2.** Moderated: a facilitator probes, small sample, deeper insight; unmoderated: tool-led, many participants, faster and cheaper, less context (see the table in 7.2).
**3.** Goal: can students pay their fee within 2 minutes? Participants: 5–8 students of mixed devices and ability. Tasks: log in; find the fee due; pay and obtain a receipt. Metrics: success rate, time on task, errors, SUS.
**4.** 1 − 0.69ⁿ ≥ 0.75 ⇒ 0.69ⁿ ≤ 0.25 ⇒ n ≥ ln 0.25/ln 0.69 = 3.73 ⇒ **n = 4** (1 − 0.69⁴ = 77 %).
**5.** Odd items: 5, 4, 5, 4, 5 → (4 + 3 + 4 + 3 + 4) = 18; even items: 1, 2, 1, 2, 1 → (4 + 3 + 4 + 3 + 4) = 18; sum 36 × 2.5 = **90** — excellent, well above the 68 average.
**6.** Success rate = 9/12 = **75 %**. Mean time = (30 + 35 + 28 + 40 + 33 + 31 + 45 + 38 + 36)/9 = 316/9 = **35.1 s**.
**7.** Determine goals; Explore questions; Choose methods; Identify practical issues; Decide ethical issues; Evaluate, interpret and present data.
**8.** The ten heuristics are listed in 7.6. (a) violates #9 (error messages in plain language) and #2 (real-world language); (b) violates #3 (user control and freedom).
**9.** 0. Withdraw cash (plan: 1 → 2 → 3 → 4 → 5): 1 insert card; 2 enter PIN; 3 choose Withdraw and the amount; 4 take card; 5 take cash and receipt.
**10.** Typing: 6.65 s (see 7.7). Fingerprint: M + one touch (0.2 s) = 1.35 + 0.2 = **1.55 s**, about 4.3 times faster.
:::

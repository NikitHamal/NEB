---
subject: Software Project Management
grade: BCA Semester 7
unit: 2
title: Software Project Scheduling
hours: 8
area: BCA 402 · Software Project Management · Unit 2
---

A plan that says "finish in six months" is a wish. A **schedule** says which activity starts on which day, who does it, and which activities cannot be delayed without delaying the whole project. This unit shows how to turn a vague project into a list of activities, link them in a network, calculate the shortest possible project duration and find the activities that decide it.

::: key What this unit gives you
- The objectives of activity planning and the work breakdown structure (WBS).
- Network planning models: activity-on-node and activity-on-arrow networks, precedence diagramming (PDM) with lags.
- Critical path method (CPM): forward pass, backward pass, float, critical activities.
- PERT: three-point estimates, expected time, variance and probability of completion.
- Shortening project duration: crashing and fast tracking; Gantt charts and earned-value monitoring.
:::

## 2.1 Objectives of activity planning

Activity planning is done *before* the project starts (to estimate and commit), and *during* it (to control and replan). Its objectives are:

1. **Feasibility assessment.** Is the target date achievable with the resources available?
2. **Resource allocation.** When is each skill needed, and are there clashes, such as two tasks needing the same tester in the same week?
3. **Detailed costing.** Cash flow depends on when work happens.
4. **Motivation.** Clear short-term targets keep a team focused.
5. **Co-ordination.** Who must finish what before others can start; when to hire, order hardware or arrange training.
6. **Control.** Without a baseline schedule, slippage cannot be measured.

A schedule is built from the **project** (the whole), its **activities** (tasks that consume time and resources and have a start and an end), **milestones** (events with zero duration, such as "requirements signed off") and **deliverables** (tangible products). Good activities have a clear end product, a measurable duration (typically one to two weeks) and a single owner.

## 2.2 Work breakdown structure (WBS)

A **work breakdown structure** is a hierarchical decomposition of the total work into smaller, manageable pieces. It is **deliverable-oriented**: the top level is the final product, lower levels are components, and the lowest level is the **work package** that can be estimated, assigned and tracked.

```svgfig label="2.1" caption="A work breakdown structure for the college admission portal, down to work packages."
f = Fig(620, 250)
f.box(220, 8, 180, 36, "Admission portal", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=12, bold=True)
tops = [(10, "1 Requirements"), (130, "2 Design"), (250, "3 Build"), (370, "4 Test"), (490, "5 Deploy")]
for x, t in tops:
    f.box(x, 90, 112, 34, t, fill=BLUE, color=NAVY, size=11, bold=True)
    f.arrow([(310, 44), (310, 66), (x + 56, 66), (x + 56, 90)], color=SLATE, sw=1.3)
kids = {10: ["1.1 Interviews", "1.2 SRS"], 130: ["2.1 Database", "2.2 UI mock-ups"], 250: ["3.1 Registration", "3.2 Payment", "3.3 Admin panel"], 370: ["4.1 Unit tests", "4.2 UAT"], 490: ["5.1 Hosting", "5.2 Training"]}
for x, ls in kids.items():
    for i, t in enumerate(ls):
        f.box(x + 8, 146 + i * 32, 100, 26, t, fill="#fde68a", stroke=AMBER, color=NAVY, size=10)
```

### Rules for a good WBS

- **100% rule:** the children of a node must cover all of the parent's work, and nothing outside it.
- Mutually exclusive elements: no overlap between sibling packages.
- Focus on *outcomes* (nouns such as "Payment module") rather than actions.
- Stop at a size you can estimate (commonly 8 to 80 hours of effort) and assign to one person.
- A **WBS dictionary** describes each package: owner, deliverable, acceptance criteria, estimate.

Three ways to organise the WBS are by **product** (as above), by **phase** (analysis, design, code) and by **function** (UI, back end, data). The WBS answers *what*; the activity list and network then answer *in what order and when*.

## 2.3 Network planning models

### Why networks?

A bar chart shows when tasks happen but hides *why*: dependencies. A **network** shows each activity and the activities that must finish before it can start (its **predecessors**). Two drawing conventions exist.

| Convention | Activities are | Dependencies are | Dummy activities | Used by |
|---|---|---|---|---|
| **Activity-on-node (AON)** or precedence diagram | boxes | arrows | not needed | PDM, MS Project, most modern tools |
| **Activity-on-arrow (AOA)** or arrow diagram | arrows | events (nodes) | sometimes required | traditional CPM and PERT |

### Dependencies and lags

The standard **precedence diagramming method (PDM)** allows four relationships between a predecessor P and a successor S:

| Type | Meaning | Example |
|---|---|---|
| **Finish-to-start (FS)** | S starts after P finishes (default) | testing starts after coding finishes |
| **Start-to-start (SS)** | S starts after P starts | documentation starts after coding has started |
| **Finish-to-finish (FF)** | S finishes after P finishes | final testing ends after bug-fixing ends |
| **Start-to-finish (SF)** | S finishes after P starts (rare) | old system is switched off only when the new system starts |

A **lag** is a delay added to a dependency (for example FS + 2 days: concrete must cure); a **lead** is a negative lag (overlap). Dependencies may be **mandatory** (design before coding), **discretionary** (preferred practice), or **external** (waiting for a supplier).

### The critical path method (CPM)

**CPM** (developed by DuPont and Remington Rand in the late 1950s) finds the **critical path**: the longest path through the network, which determines the shortest possible project duration. An activity on the critical path has no spare time: if it slips, the whole project slips.

**Steps.**

1. List activities with durations and predecessors (from the WBS).
2. Draw the network.
3. **Forward pass:** for each activity, **ES** (earliest start) = largest EF of its predecessors (0 for the first); **EF** = ES + duration.
4. The project duration is the largest EF.
5. **Backward pass:** for the last activity LF = project duration; **LS** (latest start) = LF − duration; for earlier activities LF = smallest LS of its successors.
6. **Total float (slack)** = LS − ES (equivalently LF − EF). The **critical path** joins the activities with float = 0.

**Free float** is the delay an activity can suffer without delaying the *earliest start of its successors*; **interfering float** is total float minus free float.

::: example Worked example: forward and backward pass
A small module has seven activities (durations in weeks):

| Activity | Description | Duration | Predecessors |
|---|---|---|---|
| A | Requirements | 3 | none |
| B | Database design | 4 | A |
| C | UI design | 2 | A |
| D | Back-end coding | 5 | B |
| E | Front-end coding | 3 | C |
| F | Integration and testing | 4 | D, E |
| G | Deployment | 2 | F |

**Forward pass.** A: ES 0, EF 3. B: ES 3, EF 7. C: ES 3, EF 5. D: ES 7, EF 12. E: ES 5, EF 8. F: ES = max(12, 8) = 12, EF 16. G: ES 16, EF 18. **Project duration = 18 weeks.**

**Backward pass.** G: LF 18, LS 16. F: LF 16, LS 12. D: LF 12, LS 7. E: LF 12, LS 9. B: LF 7, LS 3. C: LF = LS of E = 9, LS 7. A: LF = min(3, 7) = 3, LS 0.

| Activity | Dur | ES | EF | LS | LF | Float | Critical? |
|---|---|---|---|---|---|---|---|
| A | 3 | 0 | 3 | 0 | 3 | 0 | yes |
| B | 4 | 3 | 7 | 3 | 7 | 0 | yes |
| C | 2 | 3 | 5 | 7 | 9 | 4 | no |
| D | 5 | 7 | 12 | 7 | 12 | 0 | yes |
| E | 3 | 5 | 8 | 9 | 12 | 4 | no |
| F | 4 | 12 | 16 | 12 | 16 | 0 | yes |
| G | 2 | 16 | 18 | 16 | 18 | 0 | yes |

The **critical path is A → B → D → F → G = 3 + 4 + 5 + 4 + 2 = 18 weeks.** The front-end track C → E has 4 weeks of float, so the UI developer can start up to 4 weeks late without delaying delivery.
:::

```svgfig label="2.2" caption="The activity-on-node network for the worked example. Each box shows the activity, its duration and (ES - EF). The critical path A, B, D, F, G is drawn in red; C and E have 4 weeks of float."
f = Fig(640, 250)
def node(x, y, name, dur, es, ef, crit):
    f.box(x, y, 84, 48, name + " (" + str(dur) + ")\n" + str(es) + " - " + str(ef), fill="#fecaca" if crit else "#bbf7d0", stroke=RED if crit else TEAL, color=NAVY, size=11, bold=True)
node(10, 100, "A", 3, 0, 3, True)
node(140, 20, "B", 4, 3, 7, True)
node(140, 180, "C", 2, 3, 5, False)
node(270, 20, "D", 5, 7, 12, True)
node(270, 180, "E", 3, 5, 8, False)
node(400, 100, "F", 4, 12, 16, True)
node(530, 100, "G", 2, 16, 18, True)
f.arrow([(94, 116), (140, 54)], color=RED, sw=2)
f.arrow([(94, 134), (140, 196)], color=SLATE, sw=1.5)
f.arrow([(224, 44), (270, 44)], color=RED, sw=2)
f.arrow([(224, 204), (270, 204)], color=SLATE, sw=1.5)
f.arrow([(354, 54), (400, 114)], color=RED, sw=2)
f.arrow([(354, 196), (400, 136)], color=SLATE, sw=1.5)
f.arrow([(484, 124), (530, 124)], color=RED, sw=2)
```

### Activity-on-arrow networks and dummy activities

In an AOA diagram, nodes are **events** numbered in order (event i earlier than event j for activity i→j). When two activities share some but not all predecessors, a **dummy activity** (a dotted arrow of zero duration) preserves the logic without adding time. Event times: earliest event time TE (forward) and latest event time TL (backward); slack of an event is TL − TE, and the critical path joins events with zero slack. AON is more common today because it needs no dummies.

## 2.4 PERT: program evaluation and review technique

**PERT** was developed in 1958 by the US Navy for the Polaris missile programme, where activity durations were highly uncertain. CPM assumes one fixed duration per activity. PERT instead uses **three estimates** and treats duration as a random variable with a beta-like distribution.

| Estimate | Symbol | Meaning |
|---|---|---|
| Optimistic | O (or a) | shortest time if everything goes well |
| Most likely | M (or m) | the modal, most probable time |
| Pessimistic | P (or b) | longest time if things go wrong, excluding disasters |

- **Expected time** t<sub>e</sub> = (O + 4M + P) / 6
- **Standard deviation** σ = (P − O) / 6; **variance** σ² = ((P − O) / 6)²
- Along the critical path the expected durations and the variances **add**: T<sub>E</sub> = Σ t<sub>e</sub>, σ<sub>T</sub>² = Σ σ².
- **Probability of finishing by a target time** T: z = (T − T<sub>E</sub>) / σ<sub>T</sub>, then read the standard normal table.

::: example Worked example: PERT times and probability
A critical path has three activities (weeks):

| Activity | O | M | P | t<sub>e</sub> = (O + 4M + P)/6 | σ = (P − O)/6 | σ² |
|---|---|---|---|---|---|---|
| A | 2 | 4 | 6 | (2 + 16 + 6)/6 = **4.0** | 0.667 | 0.444 |
| B | 3 | 5 | 13 | (3 + 20 + 13)/6 = **6.0** | 1.667 | 2.778 |
| C | 1 | 2 | 3 | (1 + 8 + 3)/6 = **2.0** | 0.333 | 0.111 |

T<sub>E</sub> = 4 + 6 + 2 = **12 weeks**; σ<sub>T</sub>² = 0.444 + 2.778 + 0.111 = 3.333, so σ<sub>T</sub> = **1.826 weeks**.

Probability of finishing within 14 weeks: z = (14 − 12)/1.826 = 1.095, and Φ(1.095) ≈ **0.863 (86.3%)**.
Probability of finishing within 11 weeks: z = (11 − 12)/1.826 = −0.548, Φ(−0.548) ≈ **0.292 (29.2%)**.
A 95% confident date is T<sub>E</sub> + 1.645σ<sub>T</sub> = 12 + 3.0 = **15 weeks**.
:::

### CPM versus PERT

| Basis | CPM | PERT |
|---|---|---|
| Time estimate | one deterministic time | three times, probabilistic |
| Origin | industrial construction, 1957 | Polaris missile, 1958 |
| Focus | time and cost trade-off | time, uncertainty |
| Suited to | repetitive, well-known work | research, new software |
| Output | critical path, floats, crash costs | expected duration, probability of meeting a date |
| Orientation | activity | event |

PERT has known limits: it ignores near-critical paths (the true completion time is usually later than the critical-path estimate), and the beta assumption is only approximate. A Monte Carlo simulation addresses both.

## 2.5 Shortening project duration

The customer often asks: "Can it be done sooner?" Shortening only helps if it **shortens the critical path**; speeding up a non-critical activity wastes money.

### Techniques

1. **Crashing.** Add resources (people, overtime, tools) to critical activities. Each activity has a *normal* and *crash* duration and cost; crash cost per week = (crash cost − normal cost) / (normal duration − crash duration). Crash the cheapest critical activity first, then recheck: another path may become critical.
2. **Fast tracking.** Run critical activities in parallel that were planned in sequence (for example start coding after the design of the first module). It costs little but increases risk of rework.
3. **Reduce scope** or defer low-priority features.
4. **Improve productivity:** better tools, reuse, reduce interruptions, replace weak links.
5. **Remove delays:** dependencies on external parties, long approval cycles.
6. **Re-sequence** to shorten dependency chains, for example by using stubs so testing can start earlier.

::: example Worked example: crashing the critical path
The network of section 2.3 takes 18 weeks (critical path A, B, D, F, G). Crash options on the critical path:

| Activity | Normal | Minimum | Weeks available | Cost per week saved |
|---|---|---|---|---|
| A | 3 | 2 | 1 | Rs 12,000 |
| B | 4 | 3 | 1 | Rs 8,000 |
| D | 5 | 4 | 1 | Rs 6,000 |
| F | 4 | 3 | 1 | Rs 10,000 |

Cheapest first: **D** (Rs 6,000) gives 17 weeks; **B** (Rs 8,000) gives 16 weeks; **F** (Rs 10,000) gives 15 weeks. The C-E path is 3 + 2 + 3 + 4 + 2 = 14 weeks (13 after F is crashed), so it never becomes critical and no extra crashing of it is needed. Total crash cost for a 3-week saving: 6,000 + 8,000 + 10,000 = **Rs 24,000**. If the customer values each week at more than Rs 10,000, crashing pays; otherwise it does not.
:::

Crashing has diminishing returns, increases risk and communication overhead (Brooks' law), and a fully crashed schedule has no slack to absorb surprises.

## 2.6 Gantt charts and monitoring progress

A **Gantt chart** (Henry Gantt, about 1910) is a bar chart with activities down the side and time across the top. Each bar spans the planned start and end; shading shows progress, and a vertical **today line** shows where the project should be. Its strength is communication; its weakness is that dependencies are less visible than in a network. Modern tools (MS Project, Jira, Asana, ClickUp, GanttProject) generate both views from one data set.

```svgfig label="2.3" caption="A Gantt view of the worked example (weeks 0 to 18). Red bars are critical; green bars have float. The dashed outline on C and E shows their 4 weeks of float."
f = Fig(640, 250)
rows = [("A", 0, 3, True), ("B", 3, 7, True), ("C", 3, 5, False), ("D", 7, 12, True), ("E", 5, 8, False), ("F", 12, 16, True), ("G", 16, 18, True)]
x0, sc = 60, 30
for i in range(0, 19, 2):
    f.line(x0 + i * sc, 14, x0 + i * sc, 226, color="#e2e8f0", sw=1)
    f.text(x0 + i * sc, 10, str(i), size=9.5, color=SLATE)
for k, (n, s, e, c) in enumerate(rows):
    y = 24 + k * 29
    f.text(40, y + 11, n, size=12, color=NAVY, bold=True, anchor="end")
    if not c:
        f.box(x0 + s * sc, y, (e - s + 4) * sc, 20, "", fill="#ffffff", stroke=TEAL)
    f.box(x0 + s * sc, y, (e - s) * sc, 20, "", fill="#fecaca" if c else "#bbf7d0", stroke=RED if c else TEAL)
```

### Earned value analysis (progress and cost monitoring)

Comparing money spent with the plan is misleading: spending 50% of the budget means nothing unless you know how much *work* was done. **Earned value management (EVM)** combines scope, time and cost.

| Term | Symbol | Meaning |
|---|---|---|
| Budget at completion | BAC | total approved budget |
| Planned value | PV | budgeted cost of work *scheduled* to date |
| Earned value | EV | budgeted cost of work *actually completed* to date |
| Actual cost | AC | money actually spent to date |
| Cost variance | CV = EV − AC | negative means over budget |
| Schedule variance | SV = EV − PV | negative means behind schedule |
| Cost performance index | CPI = EV / AC | below 1 means over budget |
| Schedule performance index | SPI = EV / PV | below 1 means behind schedule |
| Estimate at completion | EAC = BAC / CPI | forecast total cost if the trend continues |
| Estimate to complete | ETC = EAC − AC | forecast cost of the remaining work |
| Variance at completion | VAC = BAC − EAC | forecast over or underspend |

::: example Worked example: earned value
A project has BAC = Rs 500,000. At the review date 60% of the work was planned, 50% is complete, and Rs 280,000 has been spent.

PV = 0.60 × 500,000 = **300,000**; EV = 0.50 × 500,000 = **250,000**; AC = **280,000**.
CV = 250,000 − 280,000 = **−30,000** (over budget). SV = 250,000 − 300,000 = **−50,000** (behind schedule).
CPI = 250,000 / 280,000 = **0.89**; SPI = 250,000 / 300,000 = **0.83**.
EAC = 500,000 / 0.893 = **Rs 560,000**; ETC = 560,000 − 280,000 = **Rs 280,000**; VAC = 500,000 − 560,000 = **−60,000**.
The project is 17% behind schedule and 11% over cost; if nothing changes it will overrun by Rs 60,000.
:::

## Formula and fact sheet

- Forward pass: ES = max(EF of predecessors); EF = ES + D. Backward pass: LF = min(LS of successors); LS = LF − D.
- Total float = LS − ES = LF − EF; the critical path has float 0 and is the longest path.
- PERT: t<sub>e</sub> = (O + 4M + P)/6; σ = (P − O)/6; z = (T − T<sub>E</sub>)/σ<sub>T</sub>.
- Crash cost per week = (crash cost − normal cost)/(normal time − crash time).
- EVM: CV = EV − AC; SV = EV − PV; CPI = EV/AC; SPI = EV/PV; EAC = BAC/CPI.

## Chapter summary

- Activity planning supports feasibility checks, resource allocation, costing, co-ordination and control; a WBS decomposes deliverables to work packages (100% rule).
- Network models show dependencies; AON with FS, SS, FF, SF relationships and lags is the modern standard; AOA needs dummy activities.
- CPM computes the critical path with a forward and a backward pass; float shows scheduling freedom.
- PERT uses three-point estimates and gives probabilities of meeting a date.
- Only shortening the critical path shortens the project: crash the cheapest critical activity, or fast-track.
- Gantt charts communicate schedules; earned value measures real progress against cost and time.

## Practice

1. State the objectives of activity planning.
2. What is a work breakdown structure? State the 100% rule and draw a WBS for an e-commerce website.
3. Differentiate activity-on-node from activity-on-arrow networks. What is a dummy activity?
4. Explain the four dependency types of PDM with a software example each.
5. Activities: P (4, none), Q (5, P), R (3, P), S (6, Q), T (2, R, S). Find the project duration, critical path and floats.
6. Write the PERT formulae. For O = 4, M = 6, P = 14 find the expected time and standard deviation.
7. Differentiate CPM from PERT.
8. A critical path has T<sub>E</sub> = 40 days and σ<sub>T</sub> = 4 days. What is the probability of finishing within 44 days? (Φ(1.00) = 0.8413.)
9. Explain how the project duration can be shortened. What is the effect of crashing a non-critical activity?
10. BAC = 800,000; EV = 300,000; PV = 400,000; AC = 360,000. Compute CV, SV, CPI, SPI and EAC.

::: note Answers and worked solutions
**1.** Feasibility assessment, resource allocation, detailed costing, motivation, co-ordination and control.
**2.** A deliverable-oriented hierarchical decomposition of the work into work packages. 100% rule: children together cover exactly 100% of the parent. For e-commerce: catalogue, cart, payment, orders, admin, testing, deployment, each split further.
**3.** AON uses boxes for activities and arrows for dependencies; AOA uses arrows for activities and nodes for events. A dummy is a zero-duration dotted arrow that keeps correct dependency logic in AOA.
**4.** FS: test after code; SS: documentation after coding starts; FF: final testing ends after bug-fix ends; SF: old system closes when new system starts.
**5.** P: ES 0, EF 4. Q: 4 to 9. R: 4 to 7. S: 9 to 15. T: ES = max(15, 7) = 15, EF 17. **Duration 17.** Backward: T LS 15; S LS 9; R LF = 15, LS 12; Q LS 4; P LS 0. Floats: P 0, Q 0, R 8, S 0, T 0. **Critical path P-Q-S-T.**
**6.** t<sub>e</sub> = (4 + 24 + 14)/6 = **7.0**; σ = (14 − 4)/6 = **1.67**.
**7.** CPM is deterministic with one time estimate and focuses on time-cost trade-off; PERT is probabilistic with three estimates and focuses on the uncertainty of the finish date.
**8.** z = (44 − 40)/4 = 1.0, so P = **84.1%**.
**9.** Crash critical activities (cheapest first), fast-track, reduce scope, improve productivity, remove delays. Crashing a non-critical activity costs money and saves no project time because the critical path is unchanged.
**10.** CV = 300,000 − 360,000 = **−60,000**; SV = 300,000 − 400,000 = **−100,000**; CPI = 300/360 = **0.833**; SPI = 300/400 = **0.75**; EAC = 800,000/0.833 = **960,000**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is the critical path? Explain how it is found, using forward and backward passes.**

*Introduction.* The critical path is the longest sequence of dependent activities in a project network. Its length is the minimum project duration, and every activity on it has zero float.

*Method.*

1. List activities, durations and predecessors, and draw the network.
2. **Forward pass:** ES of an activity = the largest EF of its predecessors; EF = ES + duration. The largest EF is the project duration.
3. **Backward pass:** LF of the last activity = project duration; LS = LF − duration; LF of earlier activities = smallest LS of successors.
4. **Float** = LS − ES. Activities with float 0 form the critical path.

*Example.* In the module network A (3), B (4), C (2), D (5), E (3), F (4), G (2) the critical path is A-B-D-F-G with a duration of 18 weeks; C and E have 4 weeks of float.

*Conclusion.* The manager watches critical activities closely and uses float on the others to level resources.

**Q2 (10 marks). Explain PERT with its three time estimates. Compute the expected time and the probability of completing a project in a given time.**

*Introduction.* PERT handles uncertain activity durations by using three estimates and probability theory.

*Three estimates.* Optimistic O, most likely M, pessimistic P. The expected time t<sub>e</sub> = (O + 4M + P)/6 and σ = (P − O)/6.

*Procedure.* Find expected times for every activity; find the critical path using the expected times; add expected times and variances along it; compute z = (T − T<sub>E</sub>)/σ<sub>T</sub>; read the probability from the normal table.

*Example.* With the three-activity path (t<sub>e</sub> 4, 6, 2; variances 0.444, 2.778, 0.111) T<sub>E</sub> = 12, σ<sub>T</sub> = 1.826, and P(T ≤ 14) = Φ(1.095) = 86.3%.

| Quantity | Value |
|---|---|
| Expected duration | 12 weeks |
| σ of path | 1.83 weeks |
| P(finish ≤ 14 weeks) | 86.3% |
| 95% date | 15 weeks |

*Limitations.* PERT ignores near-critical paths and relies on an approximate distribution; simulation gives better results.

*Conclusion.* PERT gives the manager not only a date but also the confidence with which it can be promised.

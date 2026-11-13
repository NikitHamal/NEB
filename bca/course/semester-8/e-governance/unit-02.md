---
subject: E-Governance
grade: BCA Semester 8 (Elective III)
unit: 2
title: E-Governance Models
hours: 12
area: BCA 453 · E-Governance · Unit 2
---

Two governments can own the same portal and still govern very differently. One uses it to publish the budget and stop there. Another uses it to let a ward group send a complaint, track it, and see the answer. A third lets citizens organise against a policy. A **model** of digital governance names the *pattern of information flow* behind the technology: who tells what to whom, and what is expected to happen next. This unit covers the five models of the TU outline, the five-level maturity scale, and the route from these models to good governance.

::: key What this unit gives you
- The five models of digital governance: **broadcasting (wider dissemination)**, **critical flow**, **comparative analysis**, **mobilization and lobbying**, and **interactive service (G2C2G)**, each with purpose, flow, strengths, limits and a Nepali or global example.
- Small programs that show each model at work: reach per channel, an audit-flag pipeline, a benchmark that ranks municipalities, a threshold cascade for mobilization, and a grievance service-level report.
- The five maturity levels with their characteristics and key focus areas, plus the UN and Layne-Lee stage scales for comparison.
- How the models connect to the eight characteristics of good governance, and how to answer the exam questions on them.
:::

## 2.1 Introduction to models of digital governance

A model is useful only if it helps you decide what to build. The five models below differ along two questions: **who is the source of the information** (the government or someone else), and **who acts on it** (the government, the citizens, or a third party such as the press).

```svgfig label="2.1" caption="Information flow in the five models. Arrows show the direction in which the main content moves; the broken arrow shows the action that the model hopes to trigger."
f = Fig(680, 330)
rows = [("Broadcasting", "Government", "Citizens at large", None, NAVY),
        ("Critical flow", "Source of the facts", "Media, NGOs, affected groups", "Government is pressed", RED),
        ("Comparative analysis", "Data from many places or years", "Policy makers and public", "Practice is copied or changed", TEAL),
        ("Mobilization and lobbying", "Citizens and groups", "Each other, then government", "Government is lobbied", AMBER),
        ("Interactive service (G2C2G)", "Government and citizens", "Both, in a loop", "Service and policy improve", NAVY)]
for i, (m, a, b, c, col) in enumerate(rows):
    y = 18 + i * 62
    f.box(10, y, 150, 46, m, fill=SOFT, stroke=col, size=9.5, bold=True)
    f.box(185, y, 135, 46, a, fill=BLUE, stroke=col, size=9)
    f.arrow([(320, y + 23), (355, y + 23)], color=col)
    f.box(355, y, 135, 46, b, fill=MINT, stroke=col, size=9)
    if c:
        f.arrow([(490, y + 23), (520, y + 23)], color=col, dash=True)
        f.box(520, y, 150, 46, c, fill=SAND, stroke=col, size=9)
```

| Model | Main idea | Direction | Typical tools |
|---|---|---|---|
| Broadcasting / wider dissemination | Put useful governance information in the public domain | One to many | Websites, SMS, radio, TV, open data |
| Critical flow | Send critical facts to groups able to use them against bad governance | Source to watchdogs | RTI, audit portals, whistle-blower channels |
| Comparative analysis | Compare performance across units or time to learn | Many to one analyst | Benchmarks, league tables, dashboards |
| Mobilization and lobbying | Build online communities to press for change | Many to many | Social media, petitions, mailing lists |
| Interactive service (G2C2G) | Two-way service and participation | Loop | Portals, apps, grievance and consultation systems |

The five models come from the e-governance literature (the reference usually cited with this syllabus is Michiel Backus, *e-Governance in Developing Countries*, IICD, 2001). The first four use ICT for good governance **without necessarily changing government services**; the fifth puts the citizen inside the loop. Real projects mix several.

## 2.2 Broadcasting / wider dissemination model

### 2.2.1 Idea and purpose

The government's information, laws, notices, budgets and court decisions are put into the public domain **widely and quickly** through ICT. The assumption is that an informed citizen governs and is governed better: farmers who know the support price decide what to plant; a ward resident who sees the budget can ask where the road money went. It is the oldest and the easiest model, because nothing needs to be re-engineered: the government publishes.

### 2.2.2 Features, uses and examples

- **Content:** laws and regulations, budget speech and expenditure, tender notices, citizen's charters (what service, in how many days, for what fee), exam results, weather and market prices, disaster alerts.
- **Channels:** government websites, radio and television, SMS and push notices, notice-board screens, social media pages, open-data portals.
- **Examples:** the publication of Nepal's laws by the Law Commission, the budget documents of the Ministry of Finance, tender notices on the public procurement portal, the Department of Hydrology and Meteorology's flood warnings, results of the Secondary Education Examination. Global examples include the **Gazette** moved online and USA.gov style information portals.
- **Strengths:** cheap, quick to start, no change in service procedure; supports the right to information.
- **Limits:** one-way (no feedback), tends to serve the connected and literate, information can be outdated or in a form that ordinary people cannot read, and publication does not guarantee that anyone acts on it.

The cheapest channel is not the best one. The program compares channels by **cost per citizen actually reached** for a municipality of 40,000 people, with illustrative inputs. "Reached" means the person sees and understands the notice, so reach is the covered share multiplied by the share who understand.

```python
population = 40000
channels = {
    # name: (monthly cost NPR, share covered, share who understand)
    "Ward notice board":      (2000,  0.20, 0.80),
    "Municipal website":      (3000,  0.25, 0.70),
    "Facebook page":          (4000,  0.45, 0.65),
    "Local FM radio spot":    (25000, 0.70, 0.85),
    "SMS to registered list": (20000, 0.30, 0.95),
}
print("%-24s %8s %8s %10s %12s" % ("channel", "cost", "reached", "NPR/person", "reach share"))
rows = []
for name, (cost, cov, und) in channels.items():
    reached = population * cov * und
    rows.append((cost / reached, name, cost, reached))
    print("%-24s %8d %8.0f %10.2f %11.1f%%" % (name, cost, reached, cost / reached, 100 * cov * und))
rows.sort()
print("\ncheapest per person reached:", rows[0][1], "NPR %.2f" % rows[0][0])
best = max(channels, key=lambda k: channels[k][1] * channels[k][2])
print("widest effective reach     :", best)
# Mixing channels: assume the audiences are independent, so P(not reached by any) = product of (1 - p)
mix = ["Ward notice board", "Facebook page", "Local FM radio spot"]
miss = 1.0
for m in mix:
    miss *= 1 - channels[m][1] * channels[m][2]
print("notice board + Facebook + radio reach %.1f%% at NPR %d a month" % (100 * (1 - miss), sum(channels[m][0] for m in mix)))
```
```output
channel                      cost  reached NPR/person  reach share
Ward notice board            2000     6400       0.31        16.0%
Municipal website            3000     7000       0.43        17.5%
Facebook page                4000    11700       0.34        29.2%
Local FM radio spot         25000    23800       1.05        59.5%
SMS to registered list      20000    11400       1.75        28.5%

cheapest per person reached: Ward notice board NPR 0.31
widest effective reach     : Local FM radio spot
notice board + Facebook + radio reach 75.9% at NPR 31000 a month
```
The lesson, which generalises to every broadcasting project, is that **a mixed set of channels** reaches far more people than the cheapest one, and the choice should follow the audience, not the technology.

## 2.3 Critical flow model

### 2.3.1 Idea and purpose

The critical flow model sends **critical information**, facts about the working (and failing) of governance such as corruption, waste, misuse of funds, rights violations and poor service, to people who can act on it: the press, audit and anti-graft bodies, civil society groups and the affected community. The word "critical" has two senses: the information is crucial, and it is used to criticise. The government does not control the flow; in the best cases it opens it (RTI, open audit reports) and in the worst cases it tries to block it.

### 2.3.2 Features, uses and examples

- **Source of the facts:** audit reports, procurement records, RTI replies, asset declarations of candidates, spending data, citizen complaints, leaked or whistle-blown documents.
- **Receivers:** journalists, watchdog NGOs, auditors, opposition and community groups.
- **Examples:** the annual report of the Office of the Auditor General published online; contract and bid data on the e-procurement portal; the asset and criminal-record declarations of election candidates placed on the Election Commission site; RTI requests answered through the National Information Commission; fact-checking and data-journalism groups which turn these records into stories.
- **Strengths:** low cost, fights corruption by exposing it, builds public pressure and trust when handled well.
- **Limits:** depends on a free press and a working legal system; information alone does not punish wrongdoing; data can be misread, and false claims travel the same channel. Privacy and defamation rules must be respected.

The step that makes critical flow real is turning a large record set into a short list of items worth a journalist's time. The pipeline below takes synthetic procurement records (contract value against the official estimate) and flags unusual items with a simple, explainable rule: bids far above the estimate, single-bidder contracts and splitting of contracts just under the competitive threshold. A flag is a **question to ask**, never proof of fraud.

```python
import statistics
# (contract id, sector, estimate NPR lakh, awarded NPR lakh, bidders)
contracts = [
    ("C01", "road",     120, 118, 5), ("C02", "road",     95, 97, 4),  ("C03", "road",    110, 176, 1),
    ("C04", "school",    60,  59, 6), ("C05", "school",   55, 56, 3),  ("C06", "school",   58, 57, 4),
    ("C07", "health",    40,  41, 3), ("C08", "health",   42, 63, 1),  ("C09", "health",   38, 39, 5),
    ("C10", "road",      49,  49, 2), ("C11", "road",     49.5, 49.5, 1), ("C12", "road",   48.8, 48.8, 1),
]
THRESHOLD = 50     # lakh: above this a contract needs open competitive bidding (illustrative)
ratios = [a / e for _, _, e, a, _ in contracts]
mu, sd = statistics.mean(ratios), statistics.pstdev(ratios)
print("award/estimate ratio: mean %.3f  sd %.3f" % (mu, sd))
for cid, sector, est, award, n in contracts:
    r = award / est
    flags = []
    if (r - mu) / sd > 1.5:
        flags.append("price %.0f%% above estimate (z=%.1f)" % (100 * (r - 1), (r - mu) / sd))
    if n == 1 and award > 0.5 * THRESHOLD:
        flags.append("single bidder")
    if 0.95 * THRESHOLD <= award < THRESHOLD:
        flags.append("just under the NPR %d lakh threshold" % THRESHOLD)
    if flags:
        print(cid, sector, "->", "; ".join(flags))
split = [c for c in contracts if c[1] == "road" and 0.95 * THRESHOLD <= c[3] < THRESHOLD]
print("road contracts just under the threshold: %d, total NPR %.1f lakh" % (len(split), sum(c[3] for c in split)))
```
```output
award/estimate ratio: mean 1.095  sd 0.205
C03 road -> price 60% above estimate (z=2.5); single bidder
C08 health -> price 50% above estimate (z=2.0); single bidder
C10 road -> just under the NPR 50 lakh threshold
C11 road -> single bidder; just under the NPR 50 lakh threshold
C12 road -> single bidder; just under the NPR 50 lakh threshold
road contracts just under the threshold: 3, total NPR 147.3 lakh
```
::: caution Check before you publish
A red flag from a script is a lead. The lawful use of critical flow requires a right of reply, the original documents, and care with names. Examiners like the sentence: *critical flow depends on the legal right to information and a free media, not only on technology.*
:::

## 2.4 Comparative analysis model

### 2.4.1 Idea and purpose

The comparative analysis model uses ICT to **compare** governance practices, policies or results across places and across time, so that decision-makers and citizens can learn what works. Two municipalities with the same budget and different results raise a question; a district whose test scores doubled in five years gives a lesson. The model does not tell governments to act; it supplies the evidence and the embarrassment that make action likely.

### 2.4.2 Features, uses and examples

- **Inputs:** indicators on a common definition (cost per service, time to issue a licence, test scores, spending per head, complaint resolution rate).
- **Methods:** benchmarking, league tables, dashboards, time series, peer-group comparison, pilot-versus-control comparison.
- **Examples:** the UN E-Government Survey ranking countries (Unit 1); Nepal's *Minimum Conditions and Performance Measures* system for local governments, which scores municipalities against listed criteria and ties a part of grants to the result; national assessment results compared across districts; comparison of cost and delay of a service before and after digitisation (the CARD and Bhoomi cases in Unit 5 are of this kind).
- **Strengths:** shows weak spots, encourages healthy rivalry, spreads good practice, supports evidence-based policy.
- **Limits:** a ranking depends on the chosen indicators and weights; poor data produce false comparisons; ranking places at the bottom can discourage places that started with fewer resources. Compare like with like (peer groups), and show the trend as well as the rank.

The sensitivity of a ranking to its weights is the most common examination point, and the program shows it with five invented municipalities: indicators are scaled to 0-100 (min to max), combined with two sets of weights, and the ranks are compared.

```python
munis = {  # name: (service days to issue recommendation, % grievances resolved, own-revenue share %, ward budget spent %)
    "Alpha": (2.0, 82, 18, 91), "Beta": (5.0, 91, 35, 78), "Gamma": (1.5, 60, 12, 88),
    "Delta": (3.0, 75, 25, 95), "Epsilon": (4.0, 88, 30, 70),
}
names = list(munis)
cols = list(zip(*munis.values()))
lower_better = [True, False, False, False]
def scale(col, low_is_good):
    lo, hi = min(col), max(col)
    return [100 * ((hi - v) if low_is_good else (v - lo)) / (hi - lo) for v in col]
scaled = [scale(c, lb) for c, lb in zip(cols, lower_better)]
def rank(weights):
    score = {n: sum(w * scaled[j][i] for j, w in enumerate(weights)) for i, n in enumerate(names)}
    order = sorted(score, key=score.get, reverse=True)
    return score, {n: order.index(n) + 1 for n in names}
sA, rA = rank([0.25, 0.25, 0.25, 0.25])      # equal weights
sB, rB = rank([0.50, 0.30, 0.10, 0.10])      # service speed counts most
print("%-8s %9s %5s   %9s %5s" % ("", "equal wts", "rank", "speed wts", "rank"))
for n in names:
    print("%-8s %9.1f %5d   %9.1f %5d" % (n, sA[n], rA[n], sB[n], rB[n]))
moved = [n for n in names if rA[n] != rB[n]]
print("ranks that change with the weights:", ", ".join(moved))
```
```output
         equal wts  rank   speed wts  rank
Alpha         66.7     1        75.2     1
Beta          58.0     3        43.2     5
Gamma         43.0     5        57.2     3
Delta         65.5     2        58.7     2
Epsilon       49.3     4        49.2     4
ranks that change with the weights: Beta, Gamma
```
The table shows that a municipality can move two places by a change in weights alone (Beta falls from 3rd to 5th, Gamma rises from 5th to 3rd). For that reason a published ranking should state its indicators, weights and data date, and ideally show a range rather than a single rank.

## 2.5 Mobilization and lobbying model

### 2.5.1 Idea and purpose

In this model ICT is used to **build networks of people and organisations** (local, national, global) who share a concern and then press the government: signing petitions, sending messages, planning protests, raising funds, pooling expertise. The initiative sits outside the government, in civil society, the media, professional bodies and ordinary users. Its currency is numbers and attention.

### 2.5.2 Features, uses and examples

- **Tools:** social media groups, messaging apps, mailing lists, online petition platforms, crowdfunding, hashtags, live streaming.
- **Uses:** raising awareness of an issue, recruiting volunteers, coordinating campaigns across districts or countries, organising relief (after the 2015 earthquake, volunteers matched needs and supplies through shared online lists), lobbying a law-making body.
- **Examples:** the online-organised **Occupy Baluwatar** campaign (2012) on violence against women; petitions to parliament and ministries; the youth protests of September 2025 in Nepal, organised largely through social media and chat channels after a government ban on a number of platforms, which led to a change in government. Read a current and neutral account of these events and quote only what you can verify.
- **Strengths:** low cost, speed, reach across geography, gives voice to groups with no seat at the table, can force a government to explain or reverse a decision.
- **Limits:** easy to start and easy to abandon ("clicktivism"); rumours and manipulation spread as quickly as facts; participants may not be representative of the whole population; governments may respond by blocking platforms or by surveillance.

Mass mobilisation often follows a **threshold pattern**: each person joins when enough others have joined. A person with a low threshold starts; each wave lowers the barrier for the next. The program uses a simple threshold (Granovetter-style) model on 1,000 people to show the tipping effect: with the same crowd, a small change in the number of early joiners decides whether the campaign stays at a few dozen people or reaches nearly everyone.

```python
import random
def cascade(initiators, n=1000, mean=0.30, sd=0.10, seed=3):
    """n ordinary people each join when the share already joined reaches their threshold;
    'initiators' extra committed people join regardless."""
    rnd = random.Random(seed)
    thr = [min(1.0, max(0.0, rnd.gauss(mean, sd))) for _ in range(n)]
    total = n + initiators
    joined = initiators
    while True:
        share = joined / total
        new = initiators + sum(1 for t in thr if t <= share)
        if new == joined:
            return joined, total
        joined = new
for k in (0, 30, 60, 90, 100, 110, 150):
    j, t = cascade(k)
    print("initiators %3d -> %4d of %4d take part (%3.0f%%)" % (k, j, t, 100 * j / t))
```
```output
initiators   0 ->    1 of 1000 take part (  0%)
initiators  30 ->   32 of 1030 take part (  3%)
initiators  60 ->   67 of 1060 take part (  6%)
initiators  90 ->  129 of 1090 take part ( 12%)
initiators 100 -> 1100 of 1100 take part (100%)
initiators 110 -> 1110 of 1110 take part (100%)
initiators 150 -> 1150 of 1150 take part (100%)
```
The result is **not smooth**: below a critical number of initiators (here about one in ten of the crowd) the campaign fades, above it the participation cascades. Organisers therefore invest in the first committed group (a core team, a recognised leader, an early media story). From the government side, the same model explains why a small issue can suddenly become national, and why tracking public conversation (listening, not spying) is part of responsive governance.

::: key Comparing models 2.2 to 2.5
Broadcasting and comparative analysis are driven by **information** from the state or from data. Critical flow and mobilization are driven by **citizens, press and civil society** and put pressure on the state. In the first three the state can ignore the audience; in mobilization and the next model it cannot.
:::

## 2.6 Interactive service model (Government-to-Citizen-to-Government, G2C2G)

### 2.6.1 Idea and purpose

In the first four models the citizen mainly receives or reacts. The interactive service model puts the citizen **inside** the governance loop: the government delivers services online, and the citizen answers back with requests, complaints, comments and votes that feed the next decision. The cycle is Government → Citizen → Government, hence **G2C2G**. It covers service delivery, consultation on policy, participation in budgets and the monitoring of services by the people who use them.

```svgfig label="2.2" caption="The G2C2G loop: service goes out, feedback comes back, and the feedback changes policy and service. Without the lower return path the system is only G2C."
f = Fig(680, 270)
f.box(30, 105, 170, 60, "Government\nagencies", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(480, 105, 170, 60, "Citizens and\nbusinesses", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(255, 20, 170, 46, "Service delivery\n(portal, app, counter)", fill=SAND, stroke=AMBER, size=10)
f.box(255, 205, 170, 46, "Feedback, grievance,\nconsultation, voting", fill=ROSE, stroke=RED, size=10)
f.arrow([(200, 125), (255, 50)], color=AMBER)
f.arrow([(425, 50), (480, 125)], color=AMBER)
f.arrow([(480, 150), (425, 225)], color=RED)
f.arrow([(255, 225), (200, 150)], color=RED)
f.text(340, 140, "policy and service\nimprovement", size=10, color=SLATE)
```

### 2.6.2 Features, uses and examples

- **Service side:** applications, certificates, payments, status tracking (G2C).
- **Voice side:** grievance redress, citizen charters with service levels, online consultation on draft laws, participatory budgeting, rating of services, e-voting in some countries (C2G).
- **Back-office change:** the feedback has an owner and a deadline; data are visible to a supervisor; recurring complaints change the process.
- **Examples:** the Prime Minister's office grievance system of Nepal (Hello Sarkar, call 1111) and the online complaint platform *Gunaso*; the ward and municipal complaint boxes; MyGov in India for citizens' suggestions on policy; the participatory budgeting of Porto Alegre in Brazil, later partly online; the online consultation and petition systems of Estonia and Taiwan.
- **Strengths:** better services because they are shaped by users; trust; early warning of failures; fits the participatory and accountable aims of good governance.
- **Limits:** needs back-office staff who answer; "consultation" without response breeds cynicism; digital divide again excludes the very users with most need; identity and security of online voting are hard problems.

The service level of the voice side can be measured. The program prints a report from a synthetic log of 14 grievances with a 7-day service-level target and an automatic escalation: an unresolved case after the target goes to the next officer, and after twice the target to the head of office.

```python
SLA = 7  # days to resolve
# (id, category, days taken; None = still open after 20 days of observation)
log = [("G01", "water", 3), ("G02", "road", 12), ("G03", "certificate", 2), ("G04", "water", 9),
       ("G05", "certificate", 1), ("G06", "road", None), ("G07", "tax", 6), ("G08", "water", 5),
       ("G09", "certificate", 4), ("G10", "road", 15), ("G11", "tax", 8), ("G12", "certificate", 2),
       ("G13", "water", None), ("G14", "tax", 3)]
OBS = 20
done = [(i, c, d) for i, c, d in log if d is not None]
within = [x for x in done if x[2] <= SLA]
print("received %d, resolved %d, still open %d" % (len(log), len(done), len(log) - len(done)))
print("resolved within %d days: %d of %d (%.0f%% of all received)" % (SLA, len(within), len(log), 100 * len(within) / len(log)))
print("mean days to resolve: %.1f; median: %.1f" % (sum(d for _, _, d in done) / len(done), sorted(d for _, _, d in done)[len(done) // 2]))
for cat in sorted({c for _, c, _ in log}):
    ds = [d for _, c, d in log if c == cat]
    ok = sum(1 for d in ds if d is not None and d <= SLA)
    print("  %-11s %d cases, %d within SLA" % (cat, len(ds), ok))
print("escalate to officer (> %d days):" % SLA, [i for i, c, d in log if (d or OBS) > SLA])
print("escalate to head (> %d days):  " % (2 * SLA), [i for i, c, d in log if (d or OBS) > 2 * SLA])
```
```output
received 14, resolved 12, still open 2
resolved within 7 days: 8 of 14 (57% of all received)
mean days to resolve: 5.8; median: 5.0
  certificate 4 cases, 4 within SLA
  road        3 cases, 0 within SLA
  tax         3 cases, 2 within SLA
  water       4 cases, 2 within SLA
escalate to officer (> 7 days): ['G02', 'G04', 'G06', 'G10', 'G11', 'G13']
escalate to head (> 14 days):   ['G06', 'G10', 'G13']
```
Reading the report like a manager: *roads* and *water* hold all the open cases, so the process, not the staff member, needs fixing there. A service-level report is the interactive model's equivalent of an audit.

## 2.7 Evolution in e-governance and maturity models

### 2.7.1 Why maturity models

Governments differ widely in how far they have travelled. A **maturity model** describes a small number of levels, each with observable characteristics, so that an organisation can place itself, see what the next level demands, and avoid skipping steps. The TU outline asks for five maturity levels, their characteristics and the key focus areas. The standard form borrows from the **Capability Maturity Model** of software engineering, with each level adding discipline to the one below.

```svgfig label="2.3" caption="Five maturity levels of e-governance, drawn as a staircase. Each level keeps what the one below has and adds the focus area written on its step."
f = Fig(680, 300)
steps = [("1 Initial", "ad hoc,\nisolated\nPCs", SOFT, SLATE), ("2 Managed", "repeatable,\nstandards,\nbasic services", BLUE, NAVY),
         ("3 Defined", "organisation-\nwide process,\narchitecture", MINT, TEAL), ("4 Measured", "indicators,\nservice levels,\ncitizen metrics", SAND, AMBER), ("5 Optimising", "continuous\nimprovement,\ninnovation", ROSE, RED)]
for i, (a, b, fill, col) in enumerate(steps):
    x = 20 + i * 128
    h = 100 + i * 36
    f.box(x, 285 - h, 120, h, "", fill=fill, stroke=col)
    f.text(x + 60, 285 - h + 18, a, size=11, color=col, bold=True)
    f.text(x + 60, 285 - h + 44, b, size=10, color=SLATE)
```

### 2.7.2 The five levels

| Level | Name | Characteristics | Key focus areas |
|---|---|---|---|
| 1 | **Initial** | Computers used by individuals; a static website; success depends on a few enthusiasts; no standards, no budget line for maintenance | Awareness, basic infrastructure, first champions |
| 2 | **Managed** (repeatable) | Projects planned and tracked; common standards inside a department; the same type of service can be repeated; some online forms and status check | Project planning and tracking, requirements management, configuration control, basic policy |
| 3 | **Defined** | Common process definitions and enterprise architecture across agencies; interoperable e-services; shared data centre, identity and payment; trained staff | Process definition and redesign, integration and interoperability, training programme, risk management |
| 4 | **Measured** (quantitatively managed) | Services have measured time, cost, error and satisfaction; managers act on data; service-level agreements | Performance indicators, quality management, citizen feedback analysis, capacity planning |
| 5 | **Optimising** | Continuous improvement driven by data and feedback; innovation; services delivered proactively (no application needed); open participation | Defect and cause analysis, technology and process change management, innovation, participation |

*Note.* Textbooks differ a little in the level names (for example "repeatable" for level 2, "quantitatively managed" for level 4). Learn the progression: ad hoc, planned, standardised, measured, improving.

### 2.7.3 Other stage scales that appear in questions

| Scale | Stages |
|---|---|
| UN online service stages (older form) | Emerging presence, enhanced presence, interactive, transactional, connected (networked) |
| Layne and Lee (2001), four stages | Catalogue, transaction, vertical integration (within one function across levels), horizontal integration (across functions, one-stop) |
| Gartner-style | Presence, interaction, transaction, transformation |

The UN and Layne-Lee scales describe **what citizens see**; the five maturity levels describe **how well the organisation behind the screen is run**. Both are needed: a department can have a transactional portal (UN stage 4) and still be at maturity level 1 or 2, because the portal depends on one vendor and one officer.

The program is a small self-assessment: score six dimensions from 1 to 5, take the **minimum** as the level (the weakest area limits the organisation, as in CMM), and compare with the average.

```python
dims = {"Strategy and leadership": 3, "Process and service design": 2, "Data and interoperability": 2,
        "Technology and security": 4, "People and skills": 3, "Measurement and feedback": 1}
level = min(dims.values())
avg = sum(dims.values()) / len(dims)
names = {1: "Initial", 2: "Managed", 3: "Defined", 4: "Measured", 5: "Optimising"}
print("assessed level: %d (%s)   average score: %.2f" % (level, names[level], avg))
for k, v in sorted(dims.items(), key=lambda kv: kv[1]):
    print("  %-28s %d %s" % (k, v, "#" * v))
weak = [k for k, v in dims.items() if v == level]
print("to reach level %d first raise: %s" % (level + 1, ", ".join(weak)))
```
```output
assessed level: 1 (Initial)   average score: 2.50
  Measurement and feedback     1 #
  Process and service design   2 ##
  Data and interoperability    2 ##
  Strategy and leadership      3 ###
  People and skills            3 ###
  Technology and security      4 ####
to reach level 2 first raise: Measurement and feedback
```
This municipality is at level 1 because it has no measurement, although its technology scores 4: money spent on servers cannot compensate for a missing feedback loop.

## 2.8 Towards good governance through e-governance models

### 2.8.1 What good governance means

The UN (ESCAP) lists **eight characteristics** of good governance. They give a checklist against which any e-governance model can be judged.

| Characteristic | Meaning | How ICT and the models help | Model most linked |
|---|---|---|---|
| Participation | Affected people take part, directly or through representatives | Online consultation, petitions, feedback | Interactive, mobilization |
| Rule of law | Fair, publicly known rules, applied impartially | Laws online, case tracking, audit trails | Broadcasting |
| Transparency | Decisions and records open and understandable | Open budget and tender data, RTI portals | Broadcasting, critical flow |
| Responsiveness | Institutions serve all stakeholders in reasonable time | Service-level tracking, grievance system | Interactive |
| Consensus orientation | Different interests are mediated toward a broad agreement | Open consultation, shared evidence | Comparative, interactive |
| Equity and inclusiveness | Everybody, especially the vulnerable, has a stake | Assisted counters, local languages, low-bandwidth design | All (bridging the divide) |
| Effectiveness and efficiency | Results meet needs with good use of resources | Process redesign, benchmarks | Comparative |
| Accountability | Officials answer to the public and to institutions | Audit publication, public dashboards, whistle-blowing | Critical flow |

Technology cannot supply any of these alone. An open-data portal on a government that ignores the Auditor General does not produce accountability; it produces tidy evidence of non-accountability.

### 2.8.2 A scorecard

The program turns the checklist into a transparent scorecard for one service (say an online building permit). Each characteristic is scored 0 to 5 from observable evidence, and the weakest ones become the improvement list. Unequal scores on an otherwise good service (very transparent but not inclusive) are common.

```python
evidence = {   # characteristic: (score 0-5, observable evidence used)
    "Participation": (2, "feedback form exists, no public consultation on rules"),
    "Rule of law": (4, "fee and rules published, appeal route stated"),
    "Transparency": (4, "application status and fee breakdown visible online"),
    "Responsiveness": (3, "7-day target met in 70% of cases"),
    "Consensus orientation": (2, "no forum for builders and neighbours"),
    "Equity and inclusiveness": (1, "Nepali version incomplete; no assisted counter at wards"),
    "Effectiveness and efficiency": (3, "3 signatures instead of 7"),
    "Accountability": (3, "audit log kept; public dashboard missing"),
}
total = sum(s for s, _ in evidence.values())
print("score %d / %d = %.0f%%" % (total, 5 * len(evidence), 100 * total / (5 * len(evidence))))
print("weakest first:")
for k, (s, why) in sorted(evidence.items(), key=lambda kv: kv[1][0])[:3]:
    print("  %d  %-26s %s" % (s, k, why))
```
```output
score 22 / 40 = 55%
weakest first:
  1  Equity and inclusiveness   Nepali version incomplete; no assisted counter at wards
  2  Participation              feedback form exists, no public consultation on rules
  2  Consensus orientation      no forum for builders and neighbours
```
The output points to inclusiveness, participation and consensus. It also shows that most items need **institutional** action (a consultation, a help desk, a translation), not new software. This is the central message of the unit: the model chooses the *relationship*; technology only carries it.

## 2.9 Summary and exercises

**Summary.** A model of digital governance describes a pattern of information flow. **Broadcasting** puts government information into the public domain; **critical flow** sends critical facts to watchdogs; **comparative analysis** compares performance to learn; **mobilization and lobbying** organises citizens around an issue; **interactive service (G2C2G)** closes the loop between service and feedback. Models differ in who starts the flow and who acts. The **five maturity levels** (initial, managed, defined, measured, optimising) describe the capability of the organisation, while the UN and Layne-Lee stages describe what the citizen sees. The eight characteristics of good governance (participation, rule of law, transparency, responsiveness, consensus orientation, equity and inclusiveness, effectiveness and efficiency, accountability) give the test for every model.

1. Define a model of digital governance. Why are five models described and not one?
2. Explain the broadcasting (wider dissemination) model with purpose, features, examples, strengths and limits.
3. A notice reaches 50 per cent of 20,000 residents and 80 per cent of those who see it understand it. The channel costs NPR 8,000 a month. Find the people reached and the cost per person reached.
4. Two independent channels reach 30 per cent and 40 per cent of a population. What share is reached by at least one?
5. Explain the critical flow model. What conditions must hold for it to work?
6. Why is a statistical flag in procurement data not proof of corruption? What steps follow a flag?
7. Describe the comparative analysis model with two examples. Why can a ranking mislead?
8. Three municipalities take 2, 5 and 3 days to issue a certificate (lower is better). Scale the indicator to 0-100 (min to max).
9. Describe the mobilization and lobbying model. State two benefits and two risks.
10. In the threshold model, what is the meaning of a "tipping point" and why do organisers focus on the first joiners?
11. Explain the interactive service model (G2C2G) with a diagram. How does it differ from G2C?
12. Of 20 grievances 15 were resolved in the target time and 3 are still open. Give the percentage within target and describe the escalation rule you would set.
13. Define maturity model. Describe the five levels with characteristics and key focus areas.
14. A department scores 3, 2, 4, 2, 3 on five dimensions. What is its maturity level and average? What to improve first?
15. Differentiate the UN stages, the Layne-Lee stages and the five maturity levels.
16. List the eight characteristics of good governance and link each to an e-governance tool.
17. Compare the five models in a table on source, receiver, aim and example.
18. Which model best suits (a) publishing the municipal budget, (b) exposing a delayed road contract, (c) a new ward-level complaint system? Give reasons.

**Answers to the numerical items.** (3) Reached = 20,000 x 0.5 x 0.8 = **8,000** people; cost per person = 8,000 / 8,000 = **NPR 1.00**. (4) Not reached by either = 0.7 x 0.6 = 0.42, so at least one = 1 - 0.42 = **58 per cent**. (8) Scaled value = 100 x (max - value)/(max - min) with max 5 and min 2: **100, 0 and 66.7**. (12) 15 / 20 = **75 per cent** within target; sensible rule: send to the next officer at the target day, to the head of office at twice the target, and report the open cases weekly. (14) Level = the minimum = **2 (Managed)**; the average = (3 + 2 + 4 + 2 + 3)/5 = **2.8**; raise the two dimensions scoring 2 first.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the broadcasting model of e-governance.**

In the broadcasting (wider dissemination) model, useful governance information such as laws, rules, budgets, notices, results and citizen charters is disseminated widely through ICT so that citizens are better informed and can hold government to account. Flow: government to citizens, one way. Channels: websites, SMS, radio, television, social media, open data. Examples: online publication of laws, budget documents, tender notices, weather and flood warnings. Strengths: cheap, quick, needs no change in procedure, supports the right to information. Limits: no feedback; reaches mainly connected and literate people; information may be old or hard to read. Remedy: use several channels and plain language.

**Q2 (5 marks). Explain the critical flow model with an example.**

The critical flow model sends critical information on the working of governance, such as corruption, waste and misuse of authority, to groups who can use it: the press, auditors, civil society and the affected public. The government does not control the flow. Examples: audit reports published online, procurement records, RTI replies, election candidates' asset declarations. It needs a legal right to information, a free media and working institutions to follow up. Limits: information may be misread, privacy and defamation concerns, and exposure does not itself punish wrongdoing.

**Q3 (10 marks). Explain the five models of digital governance.**

Define a model as a pattern of information flow. Then, for each of broadcasting, critical flow, comparative analysis, mobilization and lobbying, and interactive service (G2C2G), give a three-line description: purpose, direction of flow, tools, a Nepali or global example and one limit. Draw the comparison table of 2.1 (who is the source, who acts, what is hoped for). Add that the first four do not necessarily change the services of government, while the fifth places the citizen inside the loop of service and feedback; that real projects combine models (a municipality can broadcast its budget, publish audit results, benchmark itself against peers and run a grievance system); and that the choice depends on the objective and on the readiness of the government and of the citizens. Conclude by linking the models to good governance: transparency and rule of law (broadcasting), accountability (critical flow), effectiveness (comparative), participation (mobilization) and responsiveness (interactive).

**Q4 (10 marks). Describe the five maturity levels of e-governance and the key focus areas of each.**

Open with the purpose of a maturity model and its source in the Capability Maturity Model. Give the table of 2.7.2: level 1 initial (isolated computerisation, ad hoc, champions), level 2 managed (planned projects, department standards, basic online services; project planning, requirements management, configuration control), level 3 defined (organisation-wide process and architecture, interoperable services, trained staff; process definition, integration, training, risk), level 4 measured (service indicators, service-level agreements, decisions from data; performance and quality management, citizen feedback), level 5 optimising (continuous improvement, innovation, proactive services, participation; cause analysis, change management). Add the diagram of the staircase, state that an organisation is limited by its weakest area, and distinguish maturity levels from the UN and Layne-Lee stages (what the citizen sees versus how well the organisation is run).

**Q5 (10 marks). How can e-governance models lead to good governance?**

List the eight characteristics with their meanings (the table in 2.8.1), connect each to a model and an ICT tool, and give the scorecard idea: score each characteristic from observable evidence, find the weakest, and fix it. State the limits: technology carries the relationship but does not create it; without legal rights (RTI), institutional follow-up and inclusion measures (assisted service, local language) the tools produce information without accountability. Illustrate with the Nepali context: a published budget (transparency), a grievance system with service levels (responsiveness), benchmarks of local governments (effectiveness), and social media campaigns (participation), each with a limit.

---
subject: UX/UI Design
grade: BCA Semester 2
unit: 2
title: User Interaction Design and UX Research
area: BCA 155 · UX/UI Design · Unit 2
hours: 4
---

Design starts with people, not pixels. This unit follows the UX design process from understanding users — interviews, surveys, competitor analysis, personas, journey maps — through ideation with mood boards, brainstorming and sketching.

::: key What this unit gives you
- The UX design process and user-centred design (UCD).
- Mind maps as a planning tool.
- Conducting user research: interviews, surveys, competitive analysis.
- Creating personas and user journey maps.
- Ideation: mood boards, brainstorming, sketching.
:::

## 2.1 The UX design process

There is no single standard, but most models follow the same loop. A common five-stage version (the Stanford d.school "design thinking" model):

1. **Empathise** — learn about users through research.
2. **Define** — state the problem (a "how might we…" question) and the requirements.
3. **Ideate** — generate many possible solutions.
4. **Prototype** — build quick, cheap versions.
5. **Test** — try them with users, learn, and return to any earlier stage.

Another view is the **double diamond**: *discover* (diverge on the problem) → *define* (converge) → *develop* (diverge on solutions) → *deliver* (converge).

### User-centred design (UCD)

ISO 9241-210 describes UCD as an iterative process in which users are involved at every stage. Its steps: **specify the context of use** → **specify user requirements** → **produce design solutions** → **evaluate against requirements**, repeating until the design meets them. Principles: base design on an explicit understanding of users, tasks and environments; involve users throughout; drive the design by user-centred evaluation; iterate; address the whole user experience; use multidisciplinary skills.

::: example Worked example: the problem statement
A college wants students to apply for exam forms on a phone. Poor brief: "build an exam-form app". UCD brief: *"Students in remote areas, often on slow data, need to submit exam forms before the deadline without travelling to the college. How might we let them complete and pay for the form in under five minutes on a low-end phone?"* — it names the user, context, constraint and a measurable goal.
:::

## 2.2 Mind maps

A **mind map** is a diagram that puts a central idea in the middle and radiates branches of related topics, sub-topics and keywords. In UX it is used early to **explore the problem space**, list features and content, group ideas, and plan research questions or a site's structure.

How to make one: write the central topic (e.g. "Online exam form"); draw main branches for the big themes (users, tasks, payment, notifications, risks); add sub-branches; use colours and short keywords; look for clusters and gaps. Mind maps are fast and non-linear; later they are refined into a **sitemap** or **user-flow** diagram.

## 2.3 UX research

Research replaces guessing with evidence. Two orthogonal distinctions:

| | **Qualitative** | **Quantitative** |
|---|---|---|
| Answers | *why* and *how* | *how many* and *how much* |
| Data | words, observations, behaviour | numbers |
| Methods | interviews, field observation, diary studies, usability tests (small n) | surveys, analytics, A/B tests, click-tracking |
| Sample | 5–12 people | hundreds or thousands |

And **attitudinal** (what people *say*) versus **behavioural** (what people *do*): both are needed because they differ.

### User interviews

One-to-one conversations (20–60 minutes) to learn goals, context, pain points and vocabulary.

Good practice:

- Prepare a **discussion guide** of open questions; stay flexible.
- Ask **open-ended** questions ("Tell me about the last time you applied for…") not leading ones ("Don't you find the form confusing?").
- Ask about **past behaviour** not hypotheticals ("Would you use…?" produces polite lies).
- Use the "five whys" to dig for causes; stay silent and let people fill the pause.
- Get **consent**, record (with permission), keep notes, and thank participants.
- Recruit people who match the target users, not friends.

After interviews, make an **affinity diagram**: write each observation on a note, group similar ones, name the groups — the themes become insights.

### Surveys

Questionnaires reach many people cheaply. Types of question: multiple choice, rating scales (Likert: strongly disagree … strongly agree), ranking, and a few open text boxes. Rules: keep it **short**; one idea per question (no *double-barrelled* "Is the app fast and easy?"); neutral wording; offer "not applicable"; pilot-test; define the target group and sample size. Surveys show **what** and **how many**, but not **why**, so pair them with interviews.

### Competitive analysis

Study similar products to learn what the market does well and where it fails. Steps: list **direct competitors** (same product) and **indirect competitors** (different product, same need); define criteria (features, flows, content, pricing, platforms, usability problems); build a **comparison matrix**; record screenshots; draw conclusions — **opportunities** (gaps) and **conventions** (patterns users already expect). A **heuristic review** (Unit 7) of competitors is common.

| Criterion | Competitor A | Competitor B | Our idea |
|---|---|---|---|
| Works offline | No | Partly | **Yes** |
| Nepali language | No | Yes | **Yes** |
| Payment methods | Card only | eSewa | **eSewa, Khalti, bank** |

### Other methods
Field observation (watch users in context), contextual inquiry, diary studies, card sorting (for IA), analytics review, stakeholder interviews, and usability testing of the existing product.

## 2.4 User personas

A **persona** is a fictional but research-based character who represents a group of real users. It keeps the team's decisions anchored to someone specific ("Would Sita use this?") instead of "the user", who is usually the designer in disguise.

A persona contains: **name and photo**, **demographics** (age, occupation, location), **goals** (what she wants), **needs**, **frustrations/pain points**, **behaviours** (devices, habits, tech skill), **context** (where and when she uses the product), and a short **quote** or bio.

::: example Worked example: a persona
**Sita Gurung, 20, BCA student, Pokhara.** Uses a 4 GB Android phone on mobile data; shares a laptop with her brother. *Goals:* submit the exam form on time without a trip to college. *Frustrations:* the portal times out; forms lose data; forms are only in English. *Behaviour:* checks WhatsApp hourly; trusts eSewa. *Quote:* "I just want to know my form went through."
Design implications: save progress, light pages, Nepali labels, eSewa payment, instant confirmation by SMS.
:::

Personas must come from **research data**, not imagination; **limit them** (3–5, with one **primary** persona); and update them. A **proto-persona** (assumption-based) is acceptable only as a starting point to be validated. Related tools: **scenarios** (a short story of a persona achieving a goal) and **empathy maps** (says / thinks / does / feels).

## 2.5 User journey maps

A **user journey map** visualises the steps a persona takes to achieve a goal across time and touchpoints, along with what they do, think and feel.

Typical layout — columns are stages, rows are layers:

| | Awareness | Application | Payment | Confirmation |
|---|---|---|---|---|
| **Actions** | hears of the deadline | opens portal, fills form | pays via eSewa | waits for confirmation |
| **Touchpoints** | notice board, WhatsApp | website | eSewa app | SMS, email |
| **Thoughts** | "Is it really online?" | "Will my data be lost?" | "Is this safe?" | "Did it work?" |
| **Emotions** | curious (+) | frustrated by timeout (−−) | anxious (−) | uncertain (−) |
| **Pain points** | notice is unclear | session timeouts | no payment receipt | no confirmation |
| **Opportunities** | SMS reminder | autosave | show receipt | instant confirmation |

Steps to build one: choose the persona and scenario; list the stages; fill in actions, touchpoints, thoughts and emotions from research; draw the **emotion curve**; mark **moments of truth** (high-stakes points); extract **opportunities**. It makes pain points visible to the whole team — the lowest points of the curve are where to redesign first. A **service blueprint** adds the back-stage processes behind each step.

## 2.6 Ideation techniques

After research and definition, **ideate** — produce many ideas before judging any.

### Mood boards
A collage of images, colours, textures, typefaces, photos, quotes and logos that captures the **look, feel and emotion** a design should have (e.g. "calm, trustworthy, youthful"). Used to align the team and client on visual direction before any design work; made on paper, Pinterest or Figma/Miro. A mood board is *inspiration*, not a design — it leads to a style guide.

### Brainstorming
A group session to generate ideas fast. Rules: **defer judgement**; go for **quantity**; welcome wild ideas; build on others' ideas ("yes, and…"); stay focused on the question; one conversation at a time. Variants: **brainwriting** (silent writing first, avoids dominant voices), **Crazy 8s** (fold paper into 8 panels; sketch 8 ideas in 8 minutes), **worst possible idea**, **SCAMPER** (substitute, combine, adapt, modify, put to another use, eliminate, reverse). Afterwards **cluster and vote** (dot voting), then pick ideas to prototype.

### Sketching
Fast, rough drawings of screens and flows with pencil and paper. Low cost, no one is afraid to throw them away, and everyone can sketch. Boxes for images, squiggles for text, arrows for flow. Variants: **thumbnail sketches** (tiny, many), **storyboards** (a comic strip of a user's scenario), **paper prototypes** (cut-outs tested with users). Sketching is where wireframing begins (Unit 6).

## 2.7 Seeing the ideas: the process, mind map, sample sizes, persona, journey map and Crazy 8s

Research and ideation are hands-on work, so this section shows the real artefacts. Plate 2.1 shows the walls of sticky notes where interview findings are grouped. Plate 2.2 shows a mood board, a colour-swatch board and a paper prototype next to the phone screen it became. The figures then draw the design process, a mind map, the sample-size rule, a persona, a journey map and a Crazy 8s sheet with dot voting.

```photogrid label="2.1" cols="3" ratio="1.3" caption="Where research becomes insight: three photographs from a real design-thinking workshop (CC BY-SA 4.0). (a) An affinity wall: every observation from the interviews is on its own note, and similar notes are grouped; the red lines name each group. (b) An empathy-style board: rows for pain points and rituals, a pink note for the expert, a yellow note for the question. Notes can be moved, which is why they suit early work. (c) The team builds paper prototypes with scissors, pens and sticks; a rough model costs minutes and is thrown away without regret."
@ photo id="bca155/dtwhite1" cap="Affinity wall: notes grouped into themes"
fit 1.3
focus 0.45 0.5
call 0.4 0.1 0.3 0.5 "theme cluster"
@ photo id="bca155/dtwhite2" cap="Board of pain points and rituals"
fit 1.3
focus 0.5 0.55
call 0.35 0.9 0.2 0.65 "one idea per note"
@ photo id="bca155/dtgroup" cap="Team building paper prototypes"
fit 1.3
focus 0.5 0.62
call 0.35 0.1 0.6 0.55 "cut-out screens"
```

```photogrid label="2.2" cols="3" ratio="1.3" caption="Ideation artefacts. (a) A mood board (CC BY 4.0): a collage of photographs that says calm, misty, natural before any screen is drawn. (b) The same board with paint-colour swatches laid over it: a palette is chosen from the colours of the images. (c) A paper wireframe next to the phone screen it became (CC BY-SA 4.0): the sketch fixes the layout, the phone shows the finished idea. A mood board is inspiration, not a design; it leads to a style guide."
@ photo id="bca155/moodboard" cap="Mood board: the feeling"
fit 1.3
focus 0.5 0.5
call 0.5 0.1 0.3 0.45 "photos set the mood"
@ photo id="bca155/colorcharts" cap="Swatches: the palette"
fit 1.3
focus 0.6 0.5
call 0.45 0.1 0.75 0.4 "swatch strips"
@ photo id="bca155/dtproto" cap="Paper sketch and the phone screen"
fit 1.3
focus 0.5 0.55
call 0.55 0.1 0.35 0.45 "paper wireframe"
call 0.78 0.92 0.78 0.7 "phone screen"
```

```svgfig label="2.1" caption="The design process in two views. Top: the five stages of design thinking; the loop on top shows that any stage can send you back to an earlier one. Bottom: the double diamond. Each diamond first diverges (many options) and then converges (one choice): discover many problems, define one; develop many solutions, deliver one."
f = Fig(580, 280)
f.arrow([(518, 38), (518, 20), (62, 20), (62, 36)], color=TEAL, sw=1.4)
f.text(290, 13, "iterate: test results send you back", size=9.5, color=TEAL, bold=True)
stages = [("1 Empathise", "research users"), ("2 Define", "state the problem"), ("3 Ideate", "many ideas"), ("4 Prototype", "cheap models"), ("5 Test", "try with users")]
for i, (a, b) in enumerate(stages):
    x = 10 + i * 114
    f.box(x, 38, 104, 32, a, fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=16)
    f.text(x + 52, 86, b, size=9.5, color=SLATE)
    if i < 4:
        f.arrow([(x + 104, 54), (x + 114, 54)], color=NAVY, sw=1.3)
f.line(10, 108, 570, 108, color="#cbd5e1", sw=1)
f.text(10, 126, "Double diamond", size=11, color=NAVY, bold=True, anchor="start")
f.poly([(20, 192), (150, 148), (280, 192), (150, 236)], fill=SAND, stroke=AMBER, sw=1.6)
f.poly([(300, 192), (430, 148), (560, 192), (430, 236)], fill=MINT, stroke=TEAL, sw=1.6)
f.line(150, 148, 150, 236, color=AMBER, sw=1, dash=True)
f.line(430, 148, 430, 236, color=TEAL, sw=1, dash=True)
f.text(85, 192, "diverge", size=10, color=AMBER, bold=True)
f.text(215, 192, "converge", size=10, color=AMBER, bold=True)
f.text(365, 192, "diverge", size=10, color=TEAL, bold=True)
f.text(495, 192, "converge", size=10, color=TEAL, bold=True)
f.text(150, 140, "the problem", size=10, color=AMBER, bold=True)
f.text(430, 140, "the solution", size=10, color=TEAL, bold=True)
for x, t in [(85, "1 Discover"), (215, "2 Define"), (365, "3 Develop"), (495, "4 Deliver")]:
    f.text(x, 256, t, size=10.5, color=NAVY, bold=True)
f.arrow([(280, 192), (300, 192)], color=SLATE, sw=1.3)
```

```svgfig label="2.2" caption="A mind map for the online exam form. The centre holds the topic; six branches hold themes; short keywords sit under each branch. Looking at the map shows gaps (nothing yet about printing the admit card) and risks (timeout, double payment) that become research questions and later a sitemap."
f = Fig(580, 238)
rows = [10, 90, 170]
L = [("Users", "student, parent,\nexam officer"), ("Tasks", "fill, upload photo,\nprint admit card"), ("Payment", "eSewa, Khalti, bank,\nreceipt")]
R = [("Alerts", "SMS, email,\ndeadline reminder"), ("Risks", "timeout, data loss,\ndouble payment"), ("Data", "name, roll no,\nsubject list")]
for i, y in enumerate(rows):
    f.line(140, y + 13, 230, 120, color=NAVY, sw=1.6)
    f.line(440, y + 13, 350, 120, color=NAVY, sw=1.6)
for i, y in enumerate(rows):
    for (t, s), x, col, fl in [(L[i], 10, NAVY, BLUE), (R[i], 440, TEAL, MINT)]:
        f.box(x, y, 130, 26, t, fill=fl, stroke=col, size=11, bold=True, r=13)
        for j, ln in enumerate(s.split("\n")):
            f.text(x + 65, y + 42 + j * 14, ln, size=9.5, color=SLATE)
f.box(230, 95, 120, 50, "Online exam form", fill=SAND, stroke=AMBER, size=11, bold=True, r=25)
```

```svgfig label="2.3" caption="Why five to twelve users are enough for interviews but not for surveys. Left: the share of usability problems found by n users is 1 minus (1 minus 0.31) to the power n (Nielsen and Landauer), computed here: 5 users find about 84 percent and 10 find about 98 percent, because later users repeat what earlier users showed. Right: a survey estimates a percentage, and its margin of error at 95 percent confidence is 1.96 times the square root of 0.25 over n, so 100 answers give 9.8 points and 1000 give 3.1."
f = Fig(580, 230)
x0, y0, W, H = 44, 196, 300, 170
f.line(x0, y0, x0 + W, y0, color=SLATE, sw=1.4)
f.line(x0, y0, x0, y0 - H, color=SLATE, sw=1.4)
for p in (25, 50, 75, 100):
    yy = y0 - H * p / 100
    f.line(x0, yy, x0 + W, yy, color="#e2e8f0", sw=1)
    f.text(x0 - 6, yy, "%d%%" % p, size=9.5, color=SLATE, anchor="end", vmid=True)
for n in (0, 5, 10, 15):
    xx = x0 + W * n / 15
    f.text(xx, y0 + 14, str(n), size=9.5, color=SLATE)
f.text(x0 + W / 2, y0 + 28, "number of test users, n", size=9.5, color=SLATE, bold=True)
pts = []
for n in range(0, 16):
    pct = 100 * (1 - (1 - 0.31) ** n)
    pts.append((x0 + W * n / 15, y0 - H * pct / 100))
f.raw('<polyline points="%s" fill="none" stroke="#1e3a8a" stroke-width="2.4"/>' % " ".join("%.1f,%.1f" % p for p in pts))
for n, dx, dy in [(1, 8, 4), (3, 8, 8), (5, 8, 14), (10, 10, 30), (15, -8, 16)]:
    pct = 100 * (1 - (1 - 0.31) ** n)
    px, py = x0 + W * n / 15, y0 - H * pct / 100
    f.circle(px, py, 4, fill=AMBER, stroke=AMBER)
    f.text(px + dx, py + dy, "n=%d: %.0f%%" % (n, pct), size=9.5, color=AMBER, bold=True, anchor="start" if dx > 0 else "end")
f.text(x0, 14, "Problems found by n users (interviews, tests)", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(372, 28, "Survey margin of error (95%)", size=10.5, color=TEAL, bold=True, anchor="start")
for i, n in enumerate((100, 400, 1000)):
    m = 196 * (0.25 / n) ** 0.5
    yy = 46 + i * 52
    f.text(372, yy + 8, "n = %d answers" % n, size=10, color=SLATE, bold=True, anchor="start")
    f.box(372, yy + 16, m * 10, 18, "", fill=MINT, stroke=TEAL, r=3)
    f.text(372 + m * 10 + 6, yy + 25, "+/- %.1f points" % m, size=10, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(372, 206, "Few users: why. Many users: how many.", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="2.4" caption="A persona turned into design decisions. Left: the persona card for Sita Gurung (research-based, from Section 2.4). Right: each frustration found in research is answered by one design feature, so the persona is a design tool and not a decoration. A persona with no 'so we will...' line has not been used."
f = Fig(580, 236)
f.box(6, 6, 272, 224, "", fill="#ffffff", stroke=NAVY, r=10, sw=1.8)
f.box(6, 6, 272, 52, "", fill=NAVY, stroke=NAVY, r=10)
f.circle(36, 32, 19, fill="#ffffff", stroke="#ffffff", label="SG", size=12, color=NAVY)
f.text(66, 24, "Sita Gurung, 20", size=12, color="#ffffff", bold=True, anchor="start")
f.text(66, 42, "BCA student, Pokhara", size=10, color="#dbeafe", anchor="start")
f.text(16, 78, "Device: 4 GB Android, mobile data", size=10, color=SLATE, anchor="start")
f.text(16, 96, "Trusts: eSewa; checks WhatsApp hourly", size=10, color=SLATE, anchor="start")
f.text(16, 118, "GOAL", size=10, color=TEAL, bold=True, anchor="start")
f.text(16, 134, "Submit the exam form on time without", size=10, color=SLATE, anchor="start")
f.text(16, 148, "a trip to college.", size=10, color=SLATE, anchor="start")
f.text(16, 170, "FRUSTRATIONS", size=10, color=RED, bold=True, anchor="start")
f.text(16, 186, "Portal times out; forms lose data;", size=10, color=SLATE, anchor="start")
f.text(16, 200, "English only; no proof of payment.", size=10, color=SLATE, anchor="start")
f.text(16, 220, "\"I just want to know my form went through.\"", size=9.5, color=NAVY, italic=True, anchor="start")
pairs = [("Portal times out", "Autosave draft every field"), ("Forms lose data", "Resume from last step"), ("English only", "Nepali labels and hints"), ("No proof of payment", "eSewa receipt + SMS")]
f.text(430, 14, "so we will...", size=10.5, color=NAVY, bold=True)
for i, (a, b) in enumerate(pairs):
    y = 26 + i * 52
    f.box(296, y, 116, 34, a, fill=ROSE, stroke=RED, size=10, bold=True)
    f.arrow([(412, y + 17), (440, y + 17)], color=SLATE, sw=1.5)
    f.box(440, y, 134, 34, b, fill=MINT, stroke=TEAL, size=9.5, bold=True)
```

```svgfig label="2.5" caption="A user journey map for applying for an exam form. Columns are stages; the curve is the persona's emotion (plus 2 delighted, minus 2 angry). The solid line is today's journey, with its lowest point at the application stage; the dashed line is the expected journey after the opportunities in the bottom row are built. The ring marks the moment of truth, the payment, where trust is won or lost."
f = Fig(580, 262)
names = ["Awareness", "Application", "Payment", "Confirmation"]
cx = [145, 270, 395, 520]
for i, n in enumerate(names):
    f.box(cx[i] - 58, 6, 116, 24, n, fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=12)
f.text(4, 62, "Emotion", size=9.5, color=NAVY, bold=True, anchor="start")
f.line(76, 92, 574, 92, color="#cbd5e1", sw=1, dash=True)
f.text(66, 52, "+2", size=9.5, color=SLATE, anchor="end")
f.text(66, 92, "0", size=9.5, color=SLATE, anchor="end")
f.text(66, 132, "-2", size=9.5, color=SLATE, anchor="end")
now = [1, -2, -1, -1]
fut = [1, 1, 1, 2]
yy = lambda s: 92 - s * 20
f.raw('<polyline points="%s" fill="none" stroke="#b91c1c" stroke-width="2.6"/>' % " ".join("%d,%d" % (cx[i], yy(now[i])) for i in range(4)))
f.raw('<polyline points="%s" fill="none" stroke="#0f766e" stroke-width="2.4" stroke-dasharray="6 4"/>' % " ".join("%d,%d" % (cx[i], yy(fut[i])) for i in range(4)))
for i in range(4):
    f.circle(cx[i], yy(now[i]), 5, fill=RED, stroke=RED)
    f.circle(cx[i], yy(fut[i]), 4, fill="#ffffff", stroke=TEAL, sw=2)
for i, t in enumerate(["curious", "timeout!", "anxious", "unsure"]):
    f.text(cx[i] + 8, yy(now[i]) + (14 if now[i] < 0 else -9), t, size=9.5, color=RED, bold=True, anchor="start")
f.raw('<circle cx="395" cy="112" r="11" fill="none" stroke="#b45309" stroke-width="2"/>')
f.text(395, 148, "moment of truth: payment", size=9.5, color=AMBER, bold=True)
rowsd = [("Touchpoint", ["notice board", "website", "eSewa app", "SMS, email"], "#ffffff", SLATE),
         ("Pain point", ["unclear notice", "session timeout", "no receipt", "no confirmation"], ROSE, RED),
         ("Opportunity", ["SMS reminder", "autosave draft", "show receipt", "instant SMS"], MINT, TEAL)]
for r, (lab, cells, fl, col) in enumerate(rowsd):
    y = 156 + r * 34
    f.text(4, y + 14, lab, size=9.5, color=NAVY, bold=True, anchor="start")
    for i, c in enumerate(cells):
        f.box(cx[i] - 58, y, 116, 28, c, fill=fl, stroke=col, size=10, bold=True, r=4)
```

```svgfig label="2.6" caption="A Crazy 8s sheet: eight ideas for the exam-form app sketched in eight minutes, one per panel, and then dot voting (each of 6 people has 4 dots, 24 in total; the dots are counted in the code). The winners are the step-by-step wizard (6 dots) and autosave (5 dots); the team will combine them into one prototype. Quantity first, judgement later."
f = Fig(580, 238)
ideas = ["1 One long page", "2 Step wizard", "3 Chat helper", "4 QR scan", "5 SMS code", "6 Voice", "7 Autosave", "8 Checklist"]
votes = [1, 6, 4, 0, 2, 2, 5, 4]
assert sum(votes) == 24
for k, name in enumerate(ideas):
    px, py = 6 + (k % 4) * 143, 6 + (k // 4) * 116
    top = max(votes)
    hit = votes[k] >= 5
    f.box(px, py, 134, 78, "", fill="#ffffff", stroke=TEAL if hit else "#94a3b8", r=4, sw=2.2 if hit else 1.2)
    if k == 0:
        for j in range(4): f.box(px + 14, py + 8 + j * 14, 100, 9, "", fill="#f1f5f9", stroke="#94a3b8", r=2, sw=1)
        f.box(px + 40, py + 62, 54, 12, "", fill=BLUE, stroke=NAVY, r=3, sw=1)
    elif k == 1:
        for j in range(3):
            f.circle(px + 30 + j * 37, py + 16, 8, fill=BLUE, stroke=NAVY, label=str(j + 1), size=9.5)
        f.box(px + 14, py + 32, 106, 24, "", fill="#f1f5f9", stroke="#94a3b8", r=2, sw=1)
        f.box(px + 78, py + 62, 42, 12, "", fill=BLUE, stroke=NAVY, r=3, sw=1)
    elif k == 2:
        f.box(px + 10, py + 8, 70, 16, "", fill=BLUE, stroke=NAVY, r=8, sw=1)
        f.box(px + 54, py + 30, 70, 16, "", fill=SAND, stroke=AMBER, r=8, sw=1)
        f.box(px + 10, py + 52, 70, 16, "", fill=BLUE, stroke=NAVY, r=8, sw=1)
    elif k == 3:
        f.box(px + 42, py + 8, 50, 50, "", fill="#ffffff", stroke=SLATE, r=2, sw=1.4)
        for ax, ay in [(46, 12), (74, 12), (46, 40)]:
            f.box(px + ax, py + ay, 14, 14, "", fill=SLATE, stroke=SLATE, r=1, sw=1)
        f.box(px + 66, py + 36, 8, 8, "", fill=SLATE, stroke=SLATE, r=1, sw=1)
    elif k == 4:
        f.box(px + 44, py + 6, 46, 66, "", fill="#ffffff", stroke=SLATE, r=6, sw=1.4)
        f.box(px + 50, py + 16, 34, 14, "OTP", fill=SAND, stroke=AMBER, size=9.5, bold=True, r=2)
        f.text(px + 67, py + 48, "4 7 1 9", size=10, color=SLATE, bold=True)
    elif k == 5:
        f.circle(px + 44, py + 38, 16, fill=ROSE, stroke=RED)
        for r_ in (24, 32):
            f.raw('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#b91c1c" stroke-width="1.2" stroke-dasharray="3 3"/>' % (px + 44, py + 38, r_))
        f.text(px + 100, py + 38, "say it", size=10, color=SLATE, bold=True)
    elif k == 6:
        f.box(px + 14, py + 10, 70, 56, "", fill="#f1f5f9", stroke="#94a3b8", r=3, sw=1)
        f.box(px + 88, py + 28, 38, 20, "saved", fill=MINT, stroke=TEAL, size=9.5, bold=True, r=10)
    else:
        for j in range(4):
            f.box(px + 14, py + 8 + j * 16, 10, 10, "", fill=MINT if j < 3 else "#ffffff", stroke=TEAL, r=2, sw=1.2)
            f.box(px + 32, py + 10 + j * 16, 80, 7, "", fill="#e2e8f0", stroke="#e2e8f0", r=2, sw=1)
    f.text(px + 67, py + 92, name, size=10, color=NAVY, bold=True)
    for d in range(votes[k]):
        f.circle(px + 124 - (d % 3) * 13, py + 10 + (d // 3) * 13, 5, fill=RED, stroke=RED)
    f.text(px + 67, py + 106, "%d dot%s" % (votes[k], "" if votes[k] == 1 else "s"), size=9.5, color=TEAL if hit else SLATE, bold=True)
```

### 2.7.1 Eight benefits of UX research and structured ideation in Nepal

1. **Real needs instead of guesses.** Interviews and observation show what users actually do, not what the team imagines. A college that talks to ten students about exam forms will find problems such as slow mobile data or lost sessions that no one in the office noticed. This evidence replaces opinion in design meetings.
2. **Fewer expensive mistakes.** Finding a problem on a paper sketch costs minutes; finding it after launch costs months of developer time. Government portals such as the Nagarik App or the Tribhuvan University exam portal are used by thousands on the same day, so one late fix is very costly. Cheap early tests protect the budget.
3. **Designs for the users of Nepal, not of Silicon Valley.** Research reveals low-end phones, patchy 4G, Nepali (Devanagari) reading habits, and trust in eSewa, Khalti or Fonepay. These facts change the design: light pages, Nepali labels, offline-friendly forms. A foreign template would miss all of them.
4. **A shared picture inside the team.** A persona such as Sita, or a journey map on the wall, gives developers, designers and managers one person to think about. The question "Would Sita understand this?" ends many arguments quickly. Everyone argues about the user and not about taste.
5. **Pain points become visible and ranked.** The emotion curve of a journey map (Fig. 2.5) shows which stage hurts most. A bank can see that account opening is easy but the first transfer is frightening, and fix that first. Effort goes where users suffer most.
6. **More and better ideas.** Brainstorming, brainwriting and Crazy 8s (Fig. 2.6) produce many options before anyone judges. Quiet team members get a voice, and dot voting picks winners fairly. The final idea is usually a combination that no one would have proposed alone.
7. **Faster agreement with clients and teachers.** A mood board (Plate 2.2) lets a client point at the feeling they want, such as calm or youthful, before any screen exists. This avoids late changes of colour and style. For a student project, it also gives clear evidence for the viva.
8. **Smaller, cheaper samples that still work.** Fig. 2.3 shows that five to twelve users reveal most usability problems, so a small team in a college can run a real study in a week. A short survey then confirms how common each problem is. Good research does not need a large budget; it needs a plan.

## Formula and fact sheet

- Process: empathise → define → ideate → prototype → test (iterate). UCD: context → requirements → solutions → evaluation.
- Qualitative = why/how (5–12 users); quantitative = how many (surveys, analytics).
- Interview: open, non-leading questions about past behaviour; affinity diagram to find themes.
- Persona = goals, needs, frustrations, behaviours, context; from data, 3–5 of them.
- Journey map = stages × (actions, touchpoints, thoughts, emotions, pain points, opportunities).
- Ideation: mood board (feel), brainstorming (quantity, defer judgement), sketching (fast, low fidelity).

## Chapter summary

- UX design is an iterative loop; user-centred design involves users at every stage.
- A mind map explores a problem; research methods (interviews, surveys, competitive analysis) provide evidence, qualitative and quantitative.
- Personas and journey maps turn research into shared, human, visual artefacts; opportunities appear at the pain points.
- Ideation produces many options using mood boards, brainstorming and sketching before anything is built.

## Practice

1. Explain the five stages of the design-thinking process.
2. What is user-centred design? List its steps.
3. Draw a mind map for "online library system" (at least four branches).
4. Write five good interview questions for a study of how students pay college fees and explain what makes each good. Rewrite one bad leading question.
5. List four rules for writing survey questions. What is a double-barrelled question?
6. Perform a competitive analysis table for two ride-hailing apps in Nepal on four criteria.
7. Create a persona for a farmer using a mobile app for crop prices.
8. Draw a journey map for "buying a bus ticket online" with five stages and the emotion curve.
9. Differentiate between a mood board, a brainstorm and a sketch.
10. Why are 5–12 participants sufficient for qualitative research but not for a survey?

::: note Answers and worked solutions
**1.** Empathise (research users), define (state the problem), ideate (generate ideas), prototype (build quick versions), test (try with users and iterate).
**2.** A design approach that puts users' needs at the centre and involves them throughout; steps: specify context of use, specify requirements, produce design solutions, evaluate against requirements — repeating.
**3.** Central "Online library"; branches: users (students, teachers, librarian), tasks (search, borrow, renew, reserve), content (books, e-books, journals), rules (fines, limits), notifications, risks — each with sub-branches.
**4.** E.g. "Tell me about the last time you paid your fees" (open, past behaviour); "What was the hardest part?" (pain point); "Walk me through what you did first" (process); "How did you feel when…?" (emotion); "What would you change?" (improvement). Bad: "Don't you think online payment is easier?" → "How do you prefer to pay, and why?"
**5.** Short; one idea per question; neutral wording; pilot test; offer "not applicable". Double-barrelled = asks two things at once ("fast and easy"), so the answer is ambiguous.
**6.** A grid of criteria (price transparency, fare estimate, safety features, payment options) × two apps, with a conclusion listing gaps and conventions.
**7.** Name, age, location, phone type, goals (current prices, best market), frustrations (middlemen, low literacy, poor data), behaviour, context, quote.
**8.** Stages: search routes → select seat → pay → receive ticket → travel; actions/thoughts/emotions per stage; lowest emotion at payment failure or no confirmation.
**9.** Mood board — visual feel; brainstorming — group idea generation; sketch — rough drawing of a screen or flow.
**10.** Qualitative research looks for patterns of reasons, and most usability problems recur by the fifth user; surveys estimate proportions and need large samples for statistical confidence.
:::

## Model answers for Unit 2

**Q1. Explain the UX design process (design thinking) and user-centred design. Show how the two are related. (10 marks)**

**Introduction.** The UX design process is an iterative loop that turns an understanding of users into a tested product. The best-known model is the five-stage design-thinking model of the Stanford d.school (Fig. 2.1). User-centred design (UCD) is the international standard way of working, described in ISO 9241-210, in which users are involved at every stage.

**The five stages.**

1. **Empathise.** Learn about users through interviews, observation and surveys. The output is a set of findings, such as the affinity wall of Plate 2.1.
2. **Define.** State the problem as a "how might we..." question with a user, a context and a measurable goal.
3. **Ideate.** Produce many ideas using mind maps, brainstorming, mood boards and Crazy 8s (Fig. 2.6) before judging any.
4. **Prototype.** Build quick, cheap models, from paper sketches to clickable screens (Plate 2.2).
5. **Test.** Try the prototype with real users, learn, and go back to any earlier stage.

**The double diamond.** The Design Council's double diamond describes the same work as two diverge-then-converge phases: discover and define the problem, then develop and deliver the solution.

**User-centred design (ISO 9241-210).** UCD repeats four activities until the design meets its requirements: specify the **context of use**, specify the **user requirements**, **produce design solutions**, and **evaluate** them against the requirements. Its principles are: base design on an explicit understanding of users, tasks and environments; involve users throughout; let user-centred evaluation drive the design; iterate; address the whole user experience; and use a multidisciplinary team.

| Point | Design thinking | UCD (ISO 9241-210) |
|---|---|---|
| Origin | Stanford d.school and IDEO practice | International standard |
| Shape | five stages | four activities |
| Research | Empathise | Context of use, user requirements |
| Creation | Ideate, prototype | Produce design solutions |
| Checking | Test | Evaluate against requirements |
| Common rule | iterate, involve users | iterate, involve users |

**Relation.** The two are the same idea in different words: empathise and define match context and requirements; ideate and prototype match producing solutions; test matches evaluation.

**Example.** A college asks, "How might we let remote students complete and pay for the exam form in under five minutes on a low-end phone?" The team interviews students, builds paper screens, tests with five users and repeats.

**Conclusion.** The process works because it replaces assumption with evidence at every loop; a design is finished when users, not designers, say it meets the goal.

**Q2. What is a user interview? Describe good practice and explain how an affinity diagram turns interviews into insights. (5 marks)**

A **user interview** is a one-to-one conversation of 20 to 60 minutes in which a researcher learns the participant's goals, context, pain points and vocabulary. It is a **qualitative** method: it answers *why* and *how*, not *how many*.

**Good practice.**

- **Prepare a discussion guide** of open questions, but stay flexible and follow interesting answers.
- **Ask open questions about past behaviour.** "Tell me about the last time you applied for an exam form" gives facts. "Don't you find the form confusing?" is a leading question and "Would you use an app?" produces polite lies.
- **Dig for causes** with the "five whys", and stay silent so the person fills the pause.
- **Get consent**, record only with permission, take notes and thank the participant.
- **Recruit the right people**: real students from the target group, not friends.

**Affinity diagram.** After about eight interviews, write every observation on its own sticky note, put the notes on a wall, move similar notes together and name each group (Plate 2.1a). A group with many notes, such as "forms lose data", is a theme. Themes become insights, and insights become the problem statement.

**Example.** From eight student interviews, 24 notes fall into four groups: time-outs (9), language (6), payment doubts (6) and deadline confusion (3). Time-outs are fixed first.

**Q3. Compare qualitative and quantitative UX research. Describe interviews, surveys and competitive analysis and say why 5 to 12 users are enough for one but not for the other. (10 marks)**

**Introduction.** Research replaces guessing with evidence. Methods differ along two lines: qualitative versus quantitative, and attitudinal (what people say) versus behavioural (what people do). A good study combines them.

| | Qualitative | Quantitative |
|---|---|---|
| Question | why and how | how many, how much |
| Data | words, observations | numbers |
| Methods | interviews, field observation, diary studies, usability tests | surveys, analytics, A/B tests, click tracking |
| Sample | 5 to 12 people | hundreds or thousands |
| Output | themes, insights | percentages, trends |

**User interviews.** Open, non-leading questions about past behaviour; results are grouped with an affinity diagram.

**Surveys.** Questionnaires reach many people cheaply. Use multiple choice, Likert scales and few open boxes. Keep them short, ask one idea per question (never the double-barrelled "Is the app fast and easy?"), use neutral wording, offer "not applicable" and pilot-test. A survey shows *what* and *how many* but not *why*.

**Competitive analysis.** List direct competitors (same product) and indirect competitors (different product, same need), choose criteria, fill a comparison matrix and record screenshots. The result is **opportunities** (gaps, such as no offline mode or no Nepali language) and **conventions** (patterns users already expect).

**Why the sample sizes differ.** Fig. 2.3 shows that the share of problems found by n test users is 1 - (1 - 0.31)^n: five users find about 84 percent and ten about 98 percent, because later users repeat the same problems. A survey estimates a percentage, so its accuracy depends on n: the 95 percent margin of error is 1.96 x sqrt(0.25/n), which is 9.8 points for 100 answers, 4.9 for 400 and 3.1 for 1000.

**Worked example.** A college wants to improve its exam-form portal. The team first runs a competitive analysis of two other portals and finds that neither works offline. It then interviews eight students and learns that time-outs on mobile data are the main fear. Finally it sends a 10-question survey to 400 students: 62 percent say they lost a form at least once, with a margin of error of 4.9 points. Interviews gave the reason, the survey gave the size, and the analysis gave the gap to fill.

**Conclusion.** Use interviews to find the reasons, surveys to measure how common they are, and competitive analysis to see the market. Small samples suit finding problems; large samples suit measuring them.

**Q4. What is a user persona? Create a short persona for a student who pays college fees by phone and show how it affects design. (5 marks)**

A **persona** is a fictional but research-based character that represents a group of real users. It keeps decisions tied to a specific person ("Would Sita use this?") instead of "the user", who is usually the designer in disguise.

**Parts of a persona.** Name and photo, demographics (age, job, place), goals, needs, frustrations, behaviours (devices and habits), context of use, and a short quote.

**Example persona (Fig. 2.4).** *Sita Gurung, 20, BCA student, Pokhara.* She uses a 4 GB Android phone on mobile data and shares a laptop with her brother. *Goal:* pay the fee and submit the form on time without travelling to college. *Frustrations:* the portal times out, forms lose data, forms are only in English and she gets no proof of payment. *Behaviour:* checks WhatsApp every hour and trusts eSewa. *Quote:* "I just want to know my form went through."

**Design implications.** Autosave the draft, resume from the last step, show Nepali labels and hints, pay by eSewa and send a receipt by SMS.

**Rules.** A persona must come from research data, not imagination; keep only three to five, with one primary persona; and update them. An assumption-based **proto-persona** is only a starting point to validate.

**Q5. What is a user journey map? Explain its layout and the steps of building one using the exam-form journey. (10 marks)**

**Introduction.** A **user journey map** is a diagram of the steps a persona takes to reach a goal over time and across touchpoints, together with what the persona does, thinks and feels. It makes pain points visible to the whole team, so redesign starts where users suffer most.

**Layout (Fig. 2.5).** Columns are **stages**; rows are **layers**.

| Layer | Awareness | Application | Payment | Confirmation |
|---|---|---|---|---|
| Actions | hears of the deadline | opens portal, fills form | pays by eSewa | waits |
| Touchpoints | notice board, WhatsApp | website | eSewa app | SMS, email |
| Thoughts | "Is it really online?" | "Will my data be lost?" | "Is this safe?" | "Did it work?" |
| Emotion | curious (+1) | angry at timeout (-2) | anxious (-1) | unsure (-1) |
| Pain points | notice is unclear | session timeout | no receipt | no confirmation |
| Opportunities | SMS reminder | autosave draft | show receipt | instant SMS |

**Steps to build one.**

1. Choose the **persona and scenario** (Sita applies for an exam form).
2. List the **stages** of the journey, from first awareness to the end.
3. Fill in actions, touchpoints, thoughts and emotions using **research data**.
4. Draw the **emotion curve**: the lowest points, here the application stage, are where to redesign first.
5. Mark **moments of truth**: high-stakes steps, here the payment, where trust is won or lost.
6. Extract **opportunities** and turn them into features or backlog items.

**Related tool.** A **service blueprint** adds the back-stage processes (staff, systems) behind each step.

**Value.** The dashed curve in Fig. 2.5 shows the target journey after the opportunities are built, so the map is both a diagnosis and a goal.

**Worked example.** The lowest point of Sita's curve is the application stage (-2), because the portal times out and the typed data is lost. The team therefore builds autosave first. The moment of truth is payment: if Sita does not see a receipt she will not trust the system, so the second feature is an eSewa receipt with an SMS. After these two changes the expected curve rises to +1 at every stage, and a later round of testing checks whether it really does.

**Conclusion.** A journey map turns scattered research into one shared story. It is built from evidence, it ranks problems by emotion, and it ends in concrete opportunities.

**Q6. Describe the three ideation techniques: mood boards, brainstorming and sketching. (5 marks)**

After research and definition, **ideate**: produce many ideas before judging any.

- **Mood board.** A collage of images, colours, textures, typefaces and quotes that captures the **look and feeling** the design should have, for example "calm, trustworthy, youthful" (Plate 2.2a, b). It aligns the team and client before design starts. It is inspiration, not a design: it leads to a style guide with colours and fonts.
- **Brainstorming.** A group session to generate ideas quickly. The rules are defer judgement, aim for quantity, welcome wild ideas, build on others' ideas ("yes, and...") and keep to one conversation at a time. Variants are **brainwriting** (silent writing first), **Crazy 8s** (eight ideas in eight minutes, Fig. 2.6) and **SCAMPER**. Afterwards cluster the ideas and use dot voting.
- **Sketching.** Fast, rough pencil-and-paper drawings of screens and flows. Sketches are cheap, nobody fears throwing them away, and everyone can draw boxes and arrows. Types are thumbnails, storyboards and paper prototypes (Plate 2.2c). Wireframing starts here (Unit 6).

**Example.** For the exam-form app, a mood board gives calm blue and green, Crazy 8s gives eight flows, dot voting picks wizard plus autosave, and a paper prototype is tested with five students.

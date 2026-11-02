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

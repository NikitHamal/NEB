---
subject: UX/UI Design
grade: BCA Semester 2
unit: 1
title: Introduction to UX and UI
area: BCA 155 · UX/UI Design · Unit 1
hours: 4
---

Every app you love and every form you hate was *designed* — or was not. This unit separates **user experience (UX)** from **user interface (UI)**, states the principles that make products usable, names the disciplines inside UX, and surveys the kinds of interface and the tools designers use.

::: key What this unit gives you
- UX versus UI, and the tasks of a UX designer and a UI designer.
- The core principles: usability, accessibility, simplicity.
- The six disciplines of UX.
- Interface types: CLI, GUI, VUI, menu-driven, NLP-based.
- Properties of good UX/UI design and the industry tools (Figma, Adobe XD, Sketch).
:::

## 1.1 What is UX? What is UI?

**User experience (UX)** is the *whole* of a person's interaction with a product or service: how easy it is to learn, how efficient, how pleasant, how trustworthy — before, during and after use. **User interface (UI)** is the part the user *sees and touches*: screens, buttons, colours, type, icons, layout, sounds and animations.

> UI is the steering wheel, pedals and dashboard; UX is whether the whole journey — finding the car, driving, parking, refuelling — felt easy and safe.

| | **UX design** | **UI design** |
|---|---|---|
| Question | *Does it solve the right problem in an easy, useful way?* | *Does it look and respond clearly and consistently?* |
| Focus | research, flows, structure, usability | visual design, components, interaction details |
| Deliverables | personas, journey maps, information architecture, wireframes, test reports | style guide, colour and type system, high-fidelity mock-ups, component library, animations |
| Metrics | task success, time on task, satisfaction (SUS) | consistency, readability, visual polish, accessibility contrast |
| Comes | first, then continues | after structure is settled, then continues |

A beautiful UI on a confusing flow is **bad UX**; a clear flow in an ugly UI is **weak UI**. A product needs both. In small teams one person does both.

### Tasks of a UX designer
Understand users and the business problem (interviews, surveys, analytics); define personas and scenarios; map user journeys; structure the content (information architecture); design flows and wireframes; prototype and test with users; iterate; work with developers and product managers.

### Tasks of a UI designer
Translate wireframes into visual design; choose the **colour palette**, **typography**, spacing and iconography; build a **design system** of reusable components; design for different screens and states (hover, pressed, disabled, error, empty, loading); prepare assets and specifications for developers; keep the product consistent.

## 1.2 Why design matters

- **Business**: good UX raises conversion, retention and trust, and cuts support cost. Fixing a usability problem in design costs a small fraction of fixing it after release.
- **Users**: saved time, fewer errors, access for people with disabilities.
- **Safety**: a confusing medical device or banking screen causes real harm.
- **Local context**: Nepali users switch between English and Nepali, use low-end phones and slow connections — design must be light, legible and tolerant.

## 1.3 Core UX principles

### Usability

ISO 9241-11 defines usability as the **effectiveness, efficiency and satisfaction** with which specified users achieve specified goals in a specified context. Nielsen breaks it into five qualities:

| Quality | Meaning | Test question |
|---|---|---|
| **Learnability** | how easy for first-time users | can a new user do the task unaided? |
| **Efficiency** | speed once learned | how long does an expert take? |
| **Memorability** | can returning users remember how | after two months, can they still use it? |
| **Errors** | how many, how severe, how easy to recover | how many wrong turns, can they undo? |
| **Satisfaction** | how pleasant | would they use it again? |

### Accessibility

Designing so people with **visual, hearing, motor and cognitive impairments** can use the product — and everyone in poor conditions (sunlight, one hand, noise). The standard is **WCAG** (Web Content Accessibility Guidelines), organised under four principles, **POUR**: **Perceivable**, **Operable**, **Understandable**, **Robust**. Examples: text alternatives for images, captions for video, keyboard operability, sufficient colour contrast, no information conveyed by colour alone, resizable text, clear error messages. Accessible design usually helps *all* users (curb-cut effect).

### Simplicity

Remove what is not needed; make the next step obvious. Practical rules: **one primary action per screen**, progressive disclosure (show advanced options only when asked), plain language, sensible defaults, fewer choices (Hick's law, Unit 3). *Simple* does not mean *few features*; it means features are organised so that the user is never overwhelmed.

Other widely used principles: **consistency** (same things look and behave the same), **feedback** (every action gets a visible response), **affordance** (an object suggests how it is used — a button looks pressable), **error prevention**, and **recognition over recall**.

## 1.4 The core disciplines of UX

| Discipline | What it does |
|---|---|
| **User research** | learn who the users are, what they need and how they behave: interviews, surveys, observation, analytics |
| **Content strategy** | decide what content is needed, its wording, tone, structure and who maintains it ("UX writing", microcopy such as button labels and error text) |
| **Information architecture (IA)** | organise and label content so people can find it: sitemaps, navigation, taxonomies, card sorting |
| **Interaction design (IxD)** | design how the user and system respond to each other: flows, states, gestures, feedback, micro-interactions |
| **Visual design** | the look: layout, colour, type, imagery, consistency, brand |
| **Usability evaluation** | test whether the design works for real users: heuristic evaluation, usability testing (Unit 7) |

These loop rather than run in a line: research informs IA, IA informs interaction, visual design clothes it, evaluation sends you back to research.

## 1.5 Types of user interface

| Interface | How the user acts | Strengths | Weaknesses | Examples |
|---|---|---|---|---|
| **CLI** command-line | types commands | fast, scriptable, powerful for experts | steep learning curve, no discoverability | Bash, PowerShell, Git |
| **GUI** graphical | windows, icons, menus, pointer (WIMP), touch | discoverable, visual, easy to learn | needs screen and hardware; slower for repetitive tasks | Windows, Android, Figma |
| **Menu-driven** | selects from lists of options | no memorisation, constrained choices | deep menus slow experts | ATM, phone IVR trees, old DOS apps |
| **Form-based** | fills in fields | structured data entry | long forms tire users | registration, tax forms |
| **VUI** voice | speaks and listens | hands-free, accessible for blind users | recognition errors, no privacy, hard to scan options | Alexa, Google Assistant, in-car voice |
| **NLP-based / conversational** | writes or says natural language | flexible, low learning | ambiguity, unpredictable replies, hard to show options | chatbots, LLM assistants |
| **Touch / gesture / AR/VR** | taps, swipes, moves | direct, immersive | no hover, fat-finger errors, fatigue | phones, VR headsets |

Choosing the interface type is a design decision: a power-user developer tool deserves a CLI; a bank app needs a GUI; a car needs voice.

## 1.6 Properties of good UX/UI design

A good design is **useful** (solves a real need), **usable**, **findable**, **credible/trustworthy**, **accessible**, **desirable** and **valuable** (these are Peter Morville's *UX honeycomb* facets). In the interface itself, look for: **clarity** (no ambiguity), **consistency**, **feedback**, **efficiency** (shortcuts for experts), **error tolerance** (undo, confirmations for destructive actions, forgiving input), **visual hierarchy**, **aesthetic integrity** and **performance** (a slow screen is a bad screen).

## 1.7 UX/UI tools

| Tool | Notes |
|---|---|
| **Figma** | browser-based, real-time collaboration, auto layout, components and variants, prototyping, dev mode; free plan; industry standard today |
| **Adobe XD** | Adobe's design/prototyping tool (integrates with Photoshop/Illustrator); now in maintenance mode — Adobe stopped adding features, so courses mention it but new work usually starts in Figma |
| **Sketch** | macOS-only vector UI tool that popularised symbols and plugins |
| Others | Penpot (open source), Balsamiq (low-fidelity wireframes), Miro/FigJam (whiteboards and journey maps), Maze/UserTesting (remote usability tests), Zeplin (hand-off) |

Whatever the tool, the skills are the same: frames and grids, components, constraints/auto-layout, colour and text styles, prototypes and hand-off to developers. The 48-hour lab in this course is done in one of these tools (Unit 6 lists the exercises).

## Formula and fact sheet

- UX = the whole experience; UI = what is seen and touched. Both are needed.
- Usability (ISO 9241-11): effectiveness, efficiency, satisfaction. Nielsen's five: learnability, efficiency, memorability, errors, satisfaction.
- Accessibility = WCAG POUR: perceivable, operable, understandable, robust.
- UX disciplines: user research, content strategy, information architecture, interaction design, visual design, usability evaluation.
- Interface types: CLI, GUI, menu-driven, form, VUI, NLP/conversational, touch/AR/VR.
- Tools: Figma (current standard), Adobe XD (maintenance mode), Sketch (macOS).

## Chapter summary

- UX is the entire experience; UI is its visible and tangible layer. UX designers work on research, flows and structure; UI designers on visual and component design.
- The three guiding principles are usability, accessibility and simplicity, supported by consistency, feedback, affordance and error prevention.
- UX has six disciplines that feed each other in a loop.
- Interfaces range from CLI to GUI, menu-driven, voice and conversational; the right type depends on users and context.
- Good designs are useful, usable, findable, credible, accessible, desirable and valuable.
- Figma, Adobe XD and Sketch are the standard design tools.

## Practice

1. Differentiate between UX and UI with an example where one is good and the other poor.
2. List the tasks of a UX designer and of a UI designer.
3. Define usability and explain Nielsen's five quality components.
4. What is accessibility? Explain POUR with an example for each principle.
5. Explain simplicity as a UX principle; how does it differ from having fewer features?
6. Name the six core UX disciplines and describe each in one line.
7. Compare CLI, GUI and VUI with strengths and weaknesses.
8. Which interface type would you choose for (a) a server administration tool, (b) a bank's mobile app, (c) a car's navigation while driving? Why?
9. List five properties of good UX/UI design.
10. What are Figma, Adobe XD and Sketch? Why does the industry mostly use Figma now?

::: note Answers and worked solutions
**1.** E.g. a government portal with attractive colours but a 12-step form: good UI, bad UX; a plain site where one click completes the task: good UX, plain UI. UX = entire experience, UI = look and controls.
**2.** See 1.1: UX — research, personas, journeys, IA, flows, wireframes, testing; UI — visual design, colour, type, components, states, hand-off.
**3.** Effectiveness, efficiency, satisfaction (ISO 9241-11). Nielsen: learnability, efficiency, memorability, error rate/recovery, satisfaction.
**4.** Designing for people with disabilities and difficult conditions. Perceivable: alt text for images; Operable: full keyboard navigation; Understandable: clear error messages; Robust: works with screen readers and different browsers.
**5.** Simplicity removes unnecessary steps and noise and makes the next action obvious; a feature-rich product can be simple if it uses progressive disclosure and good organisation.
**6.** User research, content strategy, information architecture, interaction design, visual design, usability evaluation (descriptions in 1.4).
**7.** CLI: powerful and scriptable but hard to learn; GUI: visual and discoverable but slower for repetitive jobs; VUI: hands-free but error-prone and hard to scan options.
**8.** (a) CLI — scriptable, fast for experts; (b) GUI — visual, secure, familiar; (c) VUI — hands-free, eyes stay on the road.
**9.** E.g. clarity, consistency, feedback, error tolerance, visual hierarchy, accessibility, performance.
**10.** Design and prototyping tools; Figma runs in the browser, supports real-time collaboration and has a free tier, while Adobe XD has been placed in maintenance mode and Sketch is macOS-only.
:::

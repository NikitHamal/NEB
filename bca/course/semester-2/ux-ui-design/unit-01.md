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

## 1.8 Seeing the ideas: interface types, the honeycomb, contrast, the UX loop and a good form

UX and UI are easy to define and easy to confuse, so this section shows them. The first plate puts five real interfaces side by side, from a text terminal to a tactile Braille display. The second plate shows two tools of the trade. The figures then draw what the words claim: UI inside UX, Morville's honeycomb, the WCAG contrast test computed on real colours, the six disciplines as a loop, and the same form designed badly and well.

```photogrid label="1.1" cols="5" ratio="1.0" caption="Five kinds of user interface, all real. (a) A command-line interface: the MS-DOS prompt, where the user must remember the command. (b) A graphical interface: an Ubuntu desktop with windows, icons and a pointer. (c) A touch interface: an Android home screen, where the finger is the pointer. (d) A voice interface: an Amazon Echo (CC BY-SA 4.0); the only controls are a microphone button and your voice. (e) A tactile interface: a refreshable Braille display (CC0) that turns on-screen text into raised dots for a blind user."
@ photo id="bca101/dos" cap="CLI: MS-DOS"
fit 1.0
focus 0.3 0.5
@ photo id="bca101/ubuntu" cap="GUI: Ubuntu"
fit 1.0
focus 0.5 0.5
@ photo id="bca101/android" cap="Touch: Android"
fit 1.0
focus 0.5 0.8
@ photo id="bca155/echo" cap="Voice: Echo"
fit 1.0
focus 0.5 0.5
call 0.5 0.12 0.28 0.38 "mic button"
@ photo id="bca155/braille" cap="Tactile: Braille"
fit 1.0
focus 0.5 0.5
call 0.5 0.12 0.5 0.45 "raised dots"
```

```photogrid label="1.2" cols="2" ratio="1.5" caption="Two tools of the trade. (a) A to-do, doing, done board of sticky notes: UX teams use the same wall of notes to group interview findings and to plan a sprint; the notes can be moved, which is why low-fidelity tools are good for early ideas. (b) A refreshable Braille display under a keyboard (CC0): accessibility is not an extra feature, because for a blind user the Braille line is the interface. A page whose images have no text alternative is silent on this device."
@ photo id="bca256/kanban" cap="Sticky-note board"
fit 1.5
focus 0.5 0.5
@ photo id="bca155/braille" cap="Braille display in use"
fit 1.5
focus 0.5 0.5
call 0.5 0.12 0.45 0.5 "text becomes dots"
```

```svgfig label="1.1" caption="UI is a part of UX. The outer box is the whole experience: finding the product, learning it, doing the task, getting help and coming back. The inner box is the interface, the part the user sees and touches. A beautiful UI inside a confusing journey is bad UX; a clear journey in a plain UI is weak UI. The product needs both."
f = Fig(580, 232)
f.box(6, 4, 568, 224, "", fill="#f8fafc", stroke=NAVY, r=10, sw=2)
f.text(20, 22, "UX: the whole experience", size=12, color=NAVY, bold=True, anchor="start")
for i, t in enumerate(["find it", "learn it", "do the task", "get help", "come back"]):
    x = 20 + i * 108
    f.box(x, 34, 98, 26, t, fill=BLUE, stroke=NAVY, size=10, bold=True, r=13)
    if i < 4:
        f.arrow([(x + 98, 47), (x + 108, 47)], color=NAVY, sw=1.3)
f.box(150, 78, 280, 134, "", fill=SAND, stroke=AMBER, r=8, sw=2)
f.text(164, 96, "UI: what the user sees and touches", size=11, color=AMBER, bold=True, anchor="start")
for i, t in enumerate(["layout", "colour", "type", "icons", "buttons", "animation"]):
    f.box(162 + (i % 3) * 88, 108 + (i // 3) * 36, 80, 28, t, fill="#ffffff", stroke=AMBER, size=10, bold=True, r=4)
f.text(290, 196, "plus states: hover, error, empty, loading", size=9.5, color=SLATE, bold=True)
f.text(20, 124, "research", size=10, color=NAVY, bold=True, anchor="start")
f.text(20, 142, "flows", size=10, color=NAVY, bold=True, anchor="start")
f.text(20, 160, "structure", size=10, color=NAVY, bold=True, anchor="start")
f.text(20, 178, "testing", size=10, color=NAVY, bold=True, anchor="start")
f.text(440, 124, "content", size=10, color=NAVY, bold=True, anchor="start")
f.text(440, 142, "speed", size=10, color=NAVY, bold=True, anchor="start")
f.text(440, 160, "trust", size=10, color=NAVY, bold=True, anchor="start")
f.text(440, 178, "support", size=10, color=NAVY, bold=True, anchor="start")
```

```svgfig label="1.2" caption="Morville's UX honeycomb: seven facets of a good product. A design can be pretty yet fail one cell, for example a lovely portal that is not findable or not credible. The question beside each cell is the test a designer asks."
import math
f = Fig(580, 236)
names = [("Valuable", 0, 0, MINT, TEAL)]
ring = ["Useful", "Usable", "Desirable", "Findable", "Accessible", "Credible"]
cx, cy, R = 120, 118, 62
cells = [("Valuable", cx, cy, MINT, TEAL)]
for i, n in enumerate(ring):
    a = math.radians(-90 + 60 * i)
    cells.append((n, cx + R * math.cos(a), cy + R * math.sin(a), SAND if i % 2 == 0 else BLUE, AMBER if i % 2 == 0 else NAVY))
for n, x, y, fl, st in cells:
    pts = [(x + 34 * math.cos(math.radians(60 * k + 30)), y + 34 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    f.poly(pts, fill=fl, stroke=st, sw=1.8, label=n, lx=x, ly=y, size=9.5, color=st)
qs = [("Useful", "does it solve a real need?"), ("Usable", "can people do the task easily?"), ("Desirable", "do they want it, does it feel good?"), ("Findable", "can they find the content and the app?"), ("Accessible", "can everyone, even with a disability?"), ("Credible", "do they trust it with their data?"), ("Valuable", "does it deliver value to users and owner?")]
for i, (n, q) in enumerate(qs):
    y = 24 + i * 30
    f.box(262, y, 74, 24, n, fill=BLUE, stroke=NAVY, size=9.5, bold=True, r=3)
    f.text(344, y + 12, q, size=9.5, color=SLATE, bold=True, anchor="start", vmid=True)
```

```svgfig label="1.3" caption="The WCAG contrast test, computed. Contrast ratio = (L1 + 0.05) / (L2 + 0.05), where L1 and L2 are the relative luminances of the lighter and darker colour. WCAG level AA needs at least 4.5 to 1 for normal text. Grey 767676 on white just passes (4.54); the lighter 999999 fails (2.85). White on amber fails (2.15), but dark navy on the same amber passes comfortably (6.81). White on teal 0F766E passes (5.47)."
def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    g_ = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * g_(r) + 0.7152 * g_(g) + 0.0722 * g_(b)
def cr(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)
f = Fig(580, 226)
pairs = [("#000000", "#ffffff"), ("#767676", "#ffffff"), ("#999999", "#ffffff"), ("#ffffff", "#f59e0b"), ("#1e293b", "#f59e0b"), ("#ffffff", "#0f766e")]
for i, (fg, bg) in enumerate(pairs):
    x = 8 + (i % 3) * 190
    y = 8 + (i // 3) * 104
    r = cr(fg, bg)
    ok = r >= 4.5
    f.raw('<rect x="%d" y="%d" width="178" height="62" rx="6" fill="%s" stroke="#475569" stroke-width="1.2"/>' % (x, y, bg))
    f.raw('<text x="%d" y="%d" font-family="Inter, sans-serif" font-size="15" font-weight="700" fill="%s" text-anchor="middle">Sample text Aa</text>' % (x + 89, y + 46, fg))
    f.box(x, y + 68, 178, 24, "%.2f : 1   %s" % (r, "PASS AA" if ok else "FAIL"), fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, size=10.5, bold=True, r=3)
    f.text(x + 6, y + 14, fg[1:].upper() + " on " + bg[1:].upper(), size=10.5, color=fg if lum(bg) > 0.4 else "#ffffff", anchor="start")
f.text(8, 220, "Rule: normal text 4.5 to 1, large text (18 pt or 14 pt bold) 3 to 1.", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="1.4" caption="The six disciplines of UX form a loop, not a line. User research feeds content strategy and information architecture; interaction design gives them behaviour; visual design clothes the result; usability evaluation tests it with real users and sends the team back to research with new questions."
f = Fig(580, 232)
cx, cy = 290, 116
nodes = [("1 User research", 290, 22), ("2 Content strategy", 458, 66), ("3 Information architecture", 458, 166), ("4 Interaction design", 290, 210), ("5 Visual design", 122, 166), ("6 Usability evaluation", 122, 66)]
cols = [(BLUE, NAVY), (SAND, AMBER), (MINT, TEAL), (BLUE, NAVY), (SAND, AMBER), (ROSE, RED)]
for (n, x, y), (fl, st) in zip(nodes, cols):
    f.box(x - 78, y - 17, 156, 34, n, fill=fl, stroke=st, size=10, bold=True, r=17)
for i in range(6):
    n1 = nodes[i]
    n2 = nodes[(i + 1) % 6]
    x1, y1 = n1[1], n1[2]
    x2, y2 = n2[1], n2[2]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L, dy / L
    f.arrow([(mx - ux * 26, my - uy * 26), (mx + ux * 26, my + uy * 26)], color=SLATE, sw=1.8)
f.text(cx, cy - 8, "iterate", size=12, color=NAVY, bold=True)
f.text(cx, cy + 10, "test, learn, redesign", size=9.5, color=SLATE, bold=True)
```

```svgfig label="1.5" caption="The same registration form, designed badly and well. Left: the labels are only grey placeholders that vanish when you type, there is no format hint, the error says only Error 0x80, and the button text is low contrast. Right: (1) a visible label above each field, (2) a format hint, (3) a specific error next to the field, and (4) a button that names the action. This uses visibility, feedback, error prevention and recognition over recall."
f = Fig(580, 280)
f.box(8, 4, 268, 270, "", fill="#ffffff", stroke=RED, r=8, sw=2)
f.text(142, 22, "POOR", size=12, color=RED, bold=True)
f.text(22, 46, "Register", size=13, color=SLATE, bold=True, anchor="start")
for i, p in enumerate(["Name", "DOB", "Pwd"]):
    f.box(22, 58 + i * 42, 240, 32, p, fill="#f8fafc", stroke="#cbd5e1", color="#cbd5e1", size=10, bold=False, r=3, anchor="start")
f.text(22, 196, "Error 0x80: invalid input", size=10, color=RED, bold=True, anchor="start")
f.box(22, 212, 110, 34, "SUBMIT", fill="#e2e8f0", stroke="#cbd5e1", color="#cbd5e1", size=10, bold=True, r=3)
f.text(142, 262, "placeholders only, vague error", size=9.5, color=RED, bold=True)
f.box(304, 4, 268, 270, "", fill="#ffffff", stroke=TEAL, r=8, sw=2)
f.text(438, 22, "GOOD", size=12, color=TEAL, bold=True)
f.text(318, 46, "Create your account", size=13, color=NAVY, bold=True, anchor="start")
labs = [("Full name", "Sita Sharma", "#cbd5e1"), ("Date of birth (YYYY-MM-DD)", "2005-04-12", "#cbd5e1"), ("Password (8 or more characters)", "pass12", RED)]
for i, (l, v, st) in enumerate(labs):
    y = 68 + i * 42
    f.text(318, y, l, size=9, color=NAVY, bold=True, anchor="start")
    f.box(318, y + 6, 240, 26, v, fill="#ffffff", stroke=st, color=SLATE, size=10, bold=False, r=3, anchor="start", sw=2 if st == RED else 1.4)
f.text(318, 206, "Password needs 8 or more characters", size=9.5, color=RED, bold=True, anchor="start")
f.box(318, 218, 150, 34, "Create account", fill=TEAL, stroke=TEAL, color="#ffffff", size=11, bold=True, r=3)
f.text(438, 268, "labels, hints, specific error, clear action", size=9.5, color=TEAL, bold=True)
for n, x, y in ((1, 306, 85), (2, 306, 127), (3, 306, 202), (4, 306, 235)):
    f.circle(x, y, 8, fill=SAND, stroke=AMBER, label=str(n), size=9, color=AMBER)
```

### 1.8.1 Eight benefits of good UX/UI design in Nepal

1. **Faster completion of tasks.** A well-designed form lets a citizen finish an online task in minutes instead of a visit to an office. A passport or licence application with clear steps, labels and a progress bar saves a day of travel. Time on task is one of the main usability measures. Every removed field is time given back to thousands of users.
2. **Fewer errors and less rework.** Labels, format hints and specific messages, as in Fig. 1.5, stop people entering the wrong data. A wrong account number in a banking or ConnectIPS transfer can be costly, so confirmation screens and clear summaries matter. Fewer errors mean fewer complaints and fewer corrections made by staff.
3. **Trust in digital payments.** People move money only through an app that feels safe and predictable. Fonepay QR scans, eSewa and Khalti wallets show a clear amount, a payee name and a visible success message. This feedback tells the user that the action worked. A confusing screen makes people go back to cash.
4. **Access for every user.** Good contrast, large touch targets, readable Nepali (Devanagari) text and screen-reader labels make a service usable by older people, people with low vision and people in bright sunlight. Fig. 1.3 shows how to test contrast with a number. Accessibility also helps the user on a cheap phone in a village.
5. **Lower training and support cost.** An interface that is learnable needs a shorter manual and fewer helpdesk calls. A college result portal or an IRD tax portal with obvious steps saves staff time. This matters in offices where one clerk serves many users every day.
6. **Higher adoption and retention.** An app that is pleasant to use gets used again. Pathao, Foodmandu and the banking apps of Nepali banks compete on speed and ease as much as on price. A good first experience brings users back; a poor one is deleted within a day.
7. **Better use of small screens and weak networks.** Most Nepali users meet the web on a phone, often on a slow connection. A simple layout, one main action per screen and light pages load quickly and are easy to use with one hand. Simplicity is a technical benefit as well as a visual one.
8. **A stronger brand and a competitive edge.** Users judge a company by how its product feels. A consistent colour, type and component system, built by a UI designer, makes the product look dependable. When two services offer the same features, the better-designed one wins customers.

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

## Model answers for Unit 1

**Q1. Differentiate between UX and UI with an example where one is good and the other is poor. (5 marks)**

**User experience (UX)** is the whole of a person's interaction with a product or service: how easy it is to learn, how efficient it is, how pleasant it is and how far it can be trusted, before, during and after use. **User interface (UI)** is the part that the user sees and touches: screens, buttons, colours, type, icons, layout, sounds and animation. UI is inside UX (Fig. 1.1).

| Point | UX design | UI design |
|---|---|---|
| Main question | does it solve the right problem easily? | does it look clear and behave consistently? |
| Focus | research, flows, structure, testing | colour, type, components, states |
| Deliverables | personas, journey maps, sitemap, wireframes, test reports | style guide, high-fidelity mock-ups, component library |
| Measures | task success, time on task, satisfaction | consistency, readability, contrast |
| Stage | starts first and continues | follows structure and continues |

**Example.** A government portal with attractive colours and fonts but a twelve-step form with no progress indicator has a *good UI and poor UX*, because users give up. A plain text page on which one click completes the task has *good UX and plain UI*. A product needs both: structure first, then visual design. In a small team one designer often does both jobs.

**Q2. Explain usability and accessibility as core UX principles. Include Nielsen's quality components, POUR and a measurable accessibility test. (10 marks)**

**Usability.** ISO 9241-11 defines usability as the **effectiveness, efficiency and satisfaction** with which specified users reach specified goals in a specified context. Effectiveness is whether the task is completed correctly; efficiency is the effort or time spent; satisfaction is the comfort and attitude of the user. Jakob Nielsen breaks usability into five qualities:

| Quality | Meaning | Test question |
|---|---|---|
| Learnability | ease for first-time users | can a new user finish the task unaided? |
| Efficiency | speed once learned | how fast is an expert? |
| Memorability | ease of return after a break | can users still use it after two months? |
| Errors | number, severity, recovery | how many wrong turns, can they undo? |
| Satisfaction | pleasantness | will they use it again? |

Usability is measured with task success rate, time on task, error count and a questionnaire such as the System Usability Scale (SUS).

**Accessibility** means designing so that people with visual, hearing, motor or cognitive impairments can use the product, and so that everyone can use it in difficult conditions such as bright sunlight, noise or one-handed use. The standard is **WCAG**, built on four principles called **POUR**:

1. **Perceivable:** information can be seen or heard by every user, for example text alternatives for images and captions for video.
2. **Operable:** every function works with a keyboard, touch or switch, and targets are large enough.
3. **Understandable:** language is plain, behaviour is predictable, and error messages say what is wrong and how to fix it.
4. **Robust:** the content works with different browsers and with assistive tools such as screen readers.

**A measurable test.** Colour contrast is checked with the ratio (L1 + 0.05) / (L2 + 0.05). WCAG AA needs 4.5 to 1 for normal text. Grey 767676 on white gives 4.54 and passes, 999999 on white gives 2.85 and fails, and white on amber gives only 2.15 (Fig. 1.3).

In practice, a team tests both with a few real users before launch: five users usually reveal most major problems, and one of them should use a screen reader or large text. Fixing a problem at the wireframe stage costs a little, while fixing it after release costs much more.

In conclusion, usability asks whether the product works well for its users, and accessibility makes sure that *all* users are included. Together they make a design effective for the widest possible group.

**Q3. Name the six core disciplines of UX and describe each in one or two sentences. (5 marks)**

The six disciplines form a loop (Fig. 1.4).

1. **User research** learns who the users are, what they need and how they behave, by interviews, surveys, observation and analytics.
2. **Content strategy** decides what content is needed, its wording, tone and structure and who keeps it up to date. UX writing, such as button labels and error text, belongs here.
3. **Information architecture (IA)** organises and labels the content so that people can find it. Tools are sitemaps, navigation menus, taxonomies and card sorting.
4. **Interaction design (IxD)** defines how the user and the system respond to each other: flows, states, gestures, feedback and micro-interactions such as a button that changes when pressed.
5. **Visual design** gives the product its look: layout, colour, type, imagery, consistency and brand.
6. **Usability evaluation** tests whether the design works for real users, using heuristic evaluation and usability tests.

The disciplines do not run in a straight line. Research informs IA, IA informs interaction, visual design finishes the screens and evaluation sends the team back to research with new questions. For example, when users of a college result portal cannot find their result (a finding of evaluation), the team returns to IA and relabels the menu.

**Q4. Compare the main types of user interface (CLI, GUI, menu-driven, VUI and conversational). How would you choose one for a given product? (10 marks)**

A **user interface** is the means by which a person and a computer exchange information. The type of interface decides how the user acts and what skills they need (Plate 1.1).

| Interface | User action | Strengths | Weaknesses | Examples |
|---|---|---|---|---|
| CLI | types commands | fast, scriptable, powerful | steep learning, nothing to discover | Bash, PowerShell, Git |
| GUI | windows, icons, menus, pointer or touch | visual, discoverable, easy to learn | needs screen; slow for repetition | Windows, Android, Figma |
| Menu-driven | picks from lists | no memorising, limited choices | deep menus slow experts | ATM, phone IVR |
| Form-based | fills fields | structured data entry | long forms tire users | registration, tax forms |
| VUI | speaks and listens | hands-free, helps blind users | recognition errors, no privacy | Alexa, in-car voice |
| Conversational / NLP | writes or says natural language | flexible, low learning | ambiguous, unpredictable | chatbots, AI assistants |
| Touch, gesture, AR/VR | taps, swipes, moves | direct, immersive | no hover, fatigue | phones, VR headsets |

**How to choose.** The choice follows from the **user**, the **task** and the **context**.

1. For *experts doing repeated technical work*, such as a server administrator, a CLI is fastest and can be automated.
2. For *general users who need to discover features*, such as a bank mobile app, a GUI with touch is best.
3. For *hands busy or eyes busy* situations, such as a car navigator, voice is the safe choice.
4. For *users who cannot see*, voice and tactile interfaces such as Braille displays (Plate 1.2) are essential.
5. For *simple, constrained choices*, such as cash withdrawal, a menu-driven ATM screen is enough.

**Worked example.** A Nepali digital wallet is used by shopkeepers, students and older relatives, on cheap phones, often outdoors. The designer picks a touch GUI as the main interface because it is discoverable and needs no training; adds a QR scanner for speed; keeps a short form for registration; and offers a voice or large-text mode for users who cannot read small print. A CLI would be wrong here, however fast it is for experts, because the users would have to remember commands.

Many products combine types: a phone app has a GUI, accepts voice input and keeps a form for registration. In conclusion, no interface type is best everywhere; the best choice matches the user's skill, the task and the environment.

**Q5. What are Figma, Adobe XD and Sketch? Why is Figma the most used tool today? (5 marks)**

These are **UX/UI design tools** used to draw screens, build clickable prototypes and hand the design to developers.

- **Figma** is a browser-based tool with real-time collaboration, so a whole team can edit one file together. It has components and variants, auto layout, prototyping, a developer mode that shows measurements and code, and a free plan.
- **Adobe XD** is Adobe's design and prototyping tool, which works with Photoshop and Illustrator. It is now in maintenance mode: Adobe no longer adds new features, so new projects rarely start in it.
- **Sketch** is a vector UI tool that runs only on macOS. It popularised symbols and plugins but is limited by being Mac-only and by weaker real-time collaboration.

| Point | Figma | Adobe XD | Sketch |
|---|---|---|---|
| Platform | browser, Windows, macOS, Linux | desktop apps | macOS only |
| Collaboration | real time | limited | limited |
| Status | industry standard | maintenance mode | active, smaller share |
| Cost | free plan | stopped for new sales | paid licence |

Figma leads because it runs on any computer, needs no installation, lets designers, developers and managers work in the same file and keeps one shared version. Other tools serve special needs: Penpot (open source), Balsamiq (low-fidelity wireframes), Miro or FigJam (whiteboards) and Maze (remote testing). The skills of frames, grids, components, styles and prototypes carry over from one tool to another.

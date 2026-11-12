---
subject: UX/UI Design
grade: BCA Semester 2
unit: 3
title: User Interface Design
area: BCA 155 · UX/UI Design · Unit 3
hours: 6
---

This unit moves from understanding users to designing what they will touch: graphical and web interfaces, the five interaction styles, the principles of UI design, the design process, and the human and technological factors that shape every screen.

::: key What this unit gives you
- Graphical and web user interfaces and how they differ.
- Interaction styles: command line, menu selection, form fill-in, direct manipulation, anthropomorphic.
- Principles of UI design, including Fitts's and Hick's laws with worked numbers.
- The UI design process.
- Human considerations (perception, memory, attention, culture) and technological considerations (devices, platforms, performance).
:::

## 3.1 Graphical and web user interfaces

A **graphical user interface (GUI)** presents information as visual objects the user manipulates with a pointing device or touch. The classic building blocks are summarised as **WIMP**: **W**indows, **I**cons, **M**enus, **P**ointer. Advantages: visible options (recognition rather than recall), immediate feedback, learnable by exploration, consistent behaviour across applications. Disadvantages: needs more screen, memory and processing; slower than commands for experts doing repetitive work; can bury options in menus.

A **web user interface** is a GUI delivered through a browser. Differences from desktop GUIs:

| Desktop GUI | Web UI |
|---|---|
| Installed; fixed window chrome | Runs in a browser; the browser's controls (back, refresh, URL) are part of the experience |
| Designer controls the window size | Unknown screen size, browser, speed — design must be **responsive** |
| Rich, instant interaction | Network latency; page loads; progressive loading needed |
| Own look and conventions per OS | Users bring expectations from other websites (logo top-left links home, cart top-right) |
| Menus along the top | **Navigation** is the central design problem (Unit 5): users arrive by search from any page |
| Single user session | Anyone, anywhere: first-time visitors dominate |

Web users **scan, not read**: they are goal-driven, impatient and leave in seconds. Hence short text, clear headings, strong visual hierarchy, and fast pages. Mobile apps add touch, small screens, sensors, notifications and intermittent networks.

## 3.2 Interaction styles

An **interaction style** is the way the user and the system exchange information.

| Style | How it works | Strengths | Weaknesses | Examples |
|---|---|---|---|---|
| **Command line** | the user types commands with arguments | very powerful, flexible, scriptable, low resource | must recall syntax; poor discoverability; error-prone | `ls -l`, `git commit`, SQL console |
| **Menu selection** | choose an item from a displayed list | no memorisation; limited choices reduce errors; self-explanatory | deep hierarchies are slow; experts feel hindered | ATM, restaurant app, phone IVR, Windows menu bar |
| **Form fill-in** | enter data into labelled fields | structured, guides the user, good for data entry | tedious if long; validation needed | sign-up, tax return, admission form |
| **Direct manipulation** | act on visible objects continuously with immediate visible results (drag, resize, pinch) | intuitive, reversible, immediate feedback, low errors; learning by doing | needs a good visual metaphor; hard to automate repetitive work | drag-and-drop files, map zoom, photo editor, sliding a slider |
| **Anthropomorphic** (natural-language or human-like) | the system converses in human-like language, voice or with a character | natural, no learning, engaging, accessible | ambiguity, over-trusting a "human-like" system, recognition errors, privacy | chatbots, voice assistants, avatars |

The five styles are mixed in practice: a modern app uses direct manipulation for the canvas, menus for commands, forms for settings and a command palette (Ctrl-K) for experts. Shneiderman's **direct-manipulation principles**: continuous representation of objects, physical actions rather than complex syntax, rapid reversible incremental actions with immediate visible feedback.

## 3.3 Principles of UI design

Well-known sets: Shneiderman's **Eight Golden Rules**, Nielsen's **10 heuristics** (Unit 7), and Norman's design principles. Core ideas:

### Clarity and consistency

- **Visibility of system status** and **feedback**: every action gets a response (button state change, progress bar, toast message).
- **Consistency**: the same action looks and works the same everywhere — in terminology, colour, placement, behaviour; follow platform conventions.
- **Affordance and signifiers** (Norman): the design shows what can be done (a raised button, a text caret); a **mapping** matches controls to effects (a vertical slider moves things up and down); **constraints** prevent wrong actions (disable "Submit" until required fields are valid).
- **Recognition over recall**: show options rather than demand memory.
- **Error prevention** and graceful **error recovery**: confirmations for destructive actions, undo, forgiving formats, helpful messages ("The phone number must have 10 digits" rather than "Error 17").
- **User control and freedom**: cancel, back, undo.
- **Minimalism / aesthetic design**: every extra element competes with the relevant ones.
- **Shortcuts** for experts (accelerators), **defaults** for novices.

### Laws of interaction (with numbers)

**Fitts's law** — the time to move to a target depends on its **distance D** and **size W**:

**MT = a + b · log₂(D/W + 1)**, where a and b are constants measured for the device.

::: example Worked example: Fitts's law
Take a = 0.1 s and b = 0.15 s/bit. A button 20 px wide that is 200 px away: log₂(200/20 + 1) = log₂ 11 = 3.46, so MT = 0.1 + 0.15 × 3.46 = **0.619 s**. Make the button twice as wide (40 px): log₂ 6 = 2.58, MT = **0.488 s**, a 21 % saving. Moving the same 20 px button to 400 px away: log₂ 21 = 4.39, MT = **0.759 s**. Since only the ratio D/W matters, a 20 px button at 100 px equals a 40 px button at 200 px.
Design consequences: make primary buttons big; put related controls close; screen **edges and corners** are infinitely deep targets (the cursor stops there) — so menu bars at the screen top are easy to hit; make touch targets at least **44 × 44 px (iOS) / 48 × 48 dp (Android)**.
:::

**Hick's law** (Hick–Hyman) — decision time grows with the number of equally likely choices n: **T = b · log₂(n + 1)**.

::: example Worked example: Hick's law
With b = 0.2 s: 3 choices → 0.2 × log₂ 4 = **0.4 s**; 7 choices → 0.2 × log₂ 8 = **0.6 s**; 15 choices → 0.2 × log₂ 16 = **0.8 s**; 31 choices → **1.0 s**. Doubling the options adds a constant increment (+b), not double the time. Design consequences: group and categorise long lists, limit primary choices, use progressive disclosure, highlight a recommended option. (Note: this does *not* mean "never more than 7 items" — organise long lists sensibly.)
:::

**Miller's law** — short-term memory holds about **7 ± 2 chunks**: chunk phone numbers (98 4123 4567), group menu items. **Jakob's law** — users spend most of their time on *other* sites, so they prefer yours to work like those. **Law of proximity / similarity / common region** (Gestalt, Unit 5). **Doherty threshold** — respond within ~400 ms or users lose focus; show progress for longer waits (<1 s no indicator, 1–10 s spinner, >10 s progress bar with estimate). **Tesler's law** — complexity cannot be removed, only moved (to the system, not the user).

### The Eight Golden Rules (Shneiderman)

1. Strive for consistency. 2. Enable frequent users to use shortcuts. 3. Offer informative feedback. 4. Design dialogues to yield closure. 5. Offer simple error handling. 6. Permit easy reversal of actions. 7. Support internal locus of control. 8. Reduce short-term memory load.

## 3.4 The UI design process

1. **Understand** users, tasks and context (Unit 2 research output: personas, journeys).
2. **Define requirements and task flows**: user stories ("As a student I want to…"), use cases, task analysis (Unit 7).
3. **Structure**: information architecture, sitemap, screen inventory, navigation model (Unit 5).
4. **Sketch and wireframe** each screen, low fidelity (Unit 6).
5. **Design the visual layer**: grid, colour, typography, components, states.
6. **Prototype** (clickable) and **test** with users (Unit 7).
7. **Hand off** to developers: specs, assets, design tokens, a component library.
8. **Implement, measure, iterate**: analytics, feedback, A/B tests.

Related practices: **atomic design** (atoms → molecules → organisms → templates → pages), a **design system** (documented components, patterns, tokens, rules), and **agile** collaboration with developers.

## 3.5 Human considerations in interface and screen design

The designer must know the human being the screen is for.

| Factor | What the science says | Design response |
|---|---|---|
| **Perception** | the eye sees detail only at the fovea; we scan in F- or Z-patterns; colour vision deficiency affects about 1 in 12 men; contrast drops with age | clear hierarchy; don't rely on colour alone; adequate contrast and size |
| **Attention** | limited, easily distracted; "banner blindness" | one focus per screen; put key actions where users look |
| **Memory** | short-term memory is small (7 ± 2 chunks) and forgets fast; long-term improves with repetition and meaning | recognition over recall; chunk; show context and recent items |
| **Learning** | users form **mental models** from previous experience | match conventions; use familiar metaphors (folder, trash, cart) |
| **Motor skill** | pointing is limited by Fitts's law; thumbs reach the lower part of a phone screen | large targets; bottom navigation on mobile; spacing between tap targets |
| **Individual differences** | novice vs expert, age, language, literacy, disability, culture | accessibility, localisation, adjustable text size |
| **Culture** | reading direction, colour meanings (white = purity or mourning), date and number formats, icons and gestures differ | localise; test with local users; support Nepali (Devanagari) fonts, Nepali numerals and the Bikram Sambat calendar |
| **Emotion** | users are stressed, rushed, distracted | calm design, helpful tone, error messages without blame |

Screen-design guidelines that follow: group related items; align; leave **white space**; limit the number of fonts and colours; put the most important information at the top-left (for left-to-right scripts); use familiar words; keep sentences short; show only the necessary at each moment.

## 3.6 Technological considerations in interface design

| Factor | Considerations |
|---|---|
| **Devices and input** | mouse, keyboard, touch, stylus, voice, game controller; different precision → target sizes, hover vs tap (no hover on touch) |
| **Screen** | size, resolution, pixel density (@1x, @2x, @3x), aspect ratio, orientation, foldables; responsive layouts with breakpoints (typically ~600, ~900, ~1200 px) |
| **Platform** | Android (Material Design), iOS (Human Interface Guidelines), web, desktop — each has conventions; users expect them |
| **Performance** | loading time, image size, animation smoothness (60 frames per second = 16.7 ms per frame); target a first useful screen within about 2–3 seconds |
| **Network** | 2G/3G and unreliable links in rural Nepal → offline mode, small payloads, retry, optimistic UI |
| **Accessibility technology** | screen readers (TalkBack, VoiceOver, NVDA), switch control, magnifiers — design must expose proper labels and focus order |
| **Browsers and compatibility** | different rendering engines; test major browsers; progressive enhancement |
| **Security and privacy** | secure input masking, clear permission requests, safe defaults |
| **Development constraints** | what can be built in budget and time; reuse of components; design-to-code consistency |

Design for **the worst plausible conditions**: a cheap phone, a slow network, bright sunlight, one hand. If it works there, it works everywhere.

## 3.7 Seeing the ideas: interaction styles, Fitts and Hick, touch targets, the process, breakpoints and response time

User-interface design is about real devices and real people, so this section starts with photographs. Plate 3.1 shows four interfaces that stand for four interaction styles, from a text terminal to a voice speaker, including the Xerox Alto, the machine that made windows and a mouse-driven pointer famous. Plate 3.2 shows the mouse, a colour-vision test chart and an eye-tracking map: the human side of the screen. The figures then compute Fitts's and Hick's laws, draw touch targets to size, compare the five styles on one task, and show the design process, responsive breakpoints and the response-time ladder.

```photogrid label="3.1" cols="4" ratio="1.1" caption="Four interfaces, four interaction styles. (a) Command line: the MS-DOS prompt; the user types and must remember the command. (b) Menu selection: a bank ATM in Nepal, where the screen offers a short list and the user only chooses. (c) Graphical, direct manipulation: the Xerox Alto (1973, CC BY-SA 4.0), the research computer with a bit-mapped screen, windows and a mouse, the ancestor of every modern desktop. (d) Anthropomorphic: an Amazon Echo (CC BY-SA 4.0), which talks and listens like a person and has almost no visible controls."
@ photo id="bca101/dos" cap="Command line: MS-DOS"
fit 1.1
focus 0.3 0.5
@ photo id="bca101/atm-nepal" cap="Menu selection: ATM"
fit 1.1
focus 0.6 0.5
@ photo id="bca155/alto" cap="GUI: Xerox Alto, 1973"
fit 1.1
focus 0.4 0.5
call 0.45 0.9 0.4 0.72 "screen"
@ photo id="bca155/echo" cap="Anthropomorphic: voice"
fit 1.1
focus 0.5 0.5
```

```photogrid label="3.2" cols="3" ratio="1.3" caption="The human side of the screen. (a) A replica of Douglas Engelbart's first mouse (about 1964, CC BY-SA 4.0): a wooden shell and one red button. Pointing devices are why Fitts's law matters. (b) A colour-vision test chart (public domain): a person with colour-vision deficiency may not see the number that others see, so colour alone must never carry meaning. About 1 in 12 men are affected. (c) An eye-tracking heat map on a web page (CC BY-SA 4.0): red areas are looked at most, and the eye follows an F-shaped path along the top and down the left edge, so key actions go there."
@ photo id="bca155/mouse" cap="First mouse, replica"
fit 1.3
focus 0.3 0.5
call 0.45 0.88 0.12 0.62 "one red button"
@ photo id="bca155/ishihara" cap="Colour-vision test chart"
fit 1.3
focus 0.5 0.5
call 0.45 0.08 0.4 0.45 "hidden number"
@ photo id="bca155/eyetrack" cap="Eye-tracking heat map"
fit 1.3
focus 0.5 0.5
call 0.5 0.3 0.28 0.78 "red = most looked at"
```

```svgfig label="3.1" caption="Fitts's law, computed with a = 0.1 s and b = 0.15 s per bit. Left: the cursor starts at the left and must reach a button; distances are drawn at 70 percent of real size. Right: the movement time MT = 0.1 + 0.15 x log2(D/W + 1). Doubling the width of the 20 px button saves 0.131 s (21 percent); doubling the distance costs 0.140 s. Only the ratio D/W matters: 20 px at 100 px takes exactly as long as 40 px at 200 px."
f = Fig(580, 196)
cases = [(200, 20, "A"), (200, 40, "B"), (400, 20, "C")]
mt = lambda D, W: 0.1 + 0.15 * (__import__("math").log2(D / W + 1))
f.text(6, 12, "Distance D and width W (px)", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(366, 12, "Movement time MT (s)", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (D, W, name) in enumerate(cases):
    y = 30 + i * 52
    f.poly([(10, y + 4), (10, y + 22), (22, y + 17)], fill=SLATE, stroke=SLATE, sw=1)
    bx = 22 + D * 0.7
    f.box(bx, y, W * 0.7, 26, "", fill=SAND, stroke=AMBER, r=3, sw=2)
    f.arrow([(26, y + 38), (bx, y + 38)], color=TEAL, sw=1.3, both=True)
    f.text(24 + D * 0.35, y + 48, "D = %d, W = %d" % (D, W), size=9.5, color=TEAL, bold=True)
    f.text(bx + W * 0.7 + 6, y + 14, name, size=11, color=AMBER, bold=True, anchor="start")
    v = mt(D, W)
    f.box(366, y + 2, v * 250, 24, "", fill=BLUE, stroke=NAVY, r=3)
    f.text(372, y + 14, "%s  %.3f s" % (name, v), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(366, 188, "B is 21% faster than A; C is 23% slower.", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="3.2" caption="Hick's law, computed with b = 0.2 s: T = 0.2 x log2(n + 1). Each doubling of the number of equally likely choices adds only a constant 0.2 s: 3 choices 0.4 s, 7 choices 0.6 s, 15 choices 0.8 s, 31 choices 1.0 s. Choosing from a long list is slow mainly because the eye must scan it, so long lists should be grouped, ordered and searchable, with a recommended option highlighted."
f = Fig(580, 214)
x0, y0, W, H = 50, 178, 330, 150
f.line(x0, y0, x0 + W, y0, color=SLATE, sw=1.4)
f.line(x0, y0, x0, y0 - H, color=SLATE, sw=1.4)
for t in (0.25, 0.5, 0.75, 1.0):
    yy = y0 - H * t / 1.2
    f.line(x0, yy, x0 + W, yy, color="#e2e8f0", sw=1)
    f.text(x0 - 6, yy, "%.2f" % t, size=9.5, color=SLATE, anchor="end", vmid=True)
for n in (0, 8, 16, 24, 32):
    f.text(x0 + W * n / 32, y0 + 14, str(n), size=9.5, color=SLATE)
f.text(x0 + W / 2, y0 + 30, "number of choices, n", size=9.5, color=SLATE, bold=True)
f.text(8, 18, "T (s)", size=9.5, color=SLATE, bold=True, anchor="start")
pts = [(x0 + W * n / 32, y0 - H * (0.2 * (__import__("math").log2(n + 1))) / 1.2) for n in [i / 2 for i in range(0, 65)]]
f.raw('<polyline points="%s" fill="none" stroke="#1e3a8a" stroke-width="2.4"/>' % " ".join("%.1f,%.1f" % p for p in pts))
for n in (3, 7, 15, 31):
    v = 0.2 * __import__("math").log2(n + 1)
    px, py = x0 + W * n / 32, y0 - H * v / 1.2
    f.circle(px, py, 4.5, fill=AMBER, stroke=AMBER)
    f.text(px + 4, py + 16, "n=%d: %.1f s" % (n, v), size=9.5, color=AMBER, bold=True, anchor="start" if n < 31 else "end")
f.box(404, 30, 168, 140, "", fill=SAND, stroke=AMBER, r=6)
for j, s in enumerate(["Reading the curve", "", "n doubles", "time adds only 0.2 s", "", "So: group, rank and", "search long lists;", "highlight a default;", "reveal options step", "by step."]):
    f.text(414, 46 + j * 13, s, size=9.5 if j else 10.5, color=AMBER if j == 0 else SLATE, bold=(j == 0), anchor="start")
```

```svgfig label="3.3" caption="Touch targets and thumb reach. Left: a phone screen for a right-handed thumb. The lower third is easy to reach, the middle needs a stretch, the top corner is the hardest, so primary actions and the navigation bar belong at the bottom. Right: tap targets drawn at their true pixel size: 20 px is too small, 44 px is the iOS minimum and 48 dp is the Android minimum. Leave at least 8 dp between neighbouring targets."
f = Fig(580, 246)
f.box(20, 6, 130, 234, "", fill="#ffffff", stroke=SLATE, r=16, sw=2)
f.box(28, 20, 114, 70, "hard to reach", fill=ROSE, stroke=RED, size=10, bold=True, r=3)
f.box(28, 92, 114, 70, "stretch", fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
f.box(28, 164, 114, 62, "easy: thumb zone", fill=MINT, stroke=TEAL, size=10, bold=True, r=3)
f.box(28, 206, 114, 20, "", fill=NAVY, stroke=NAVY, r=3)
for i, t in enumerate(["Home", "Pay", "More"]):
    f.text(47 + i * 38, 216, t, size=9.5, color="#ffffff", bold=True)
f.text(85, 238, "bottom navigation", size=9.5, color=NAVY, bold=True)
f.text(180, 22, "Tap targets at true size", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (s, lab, ok) in enumerate([(20, "20 px: too small", False), (44, "44 px: iOS minimum", True), (48, "48 dp: Android minimum", True)]):
    x = 190 + i * 130
    f.box(x, 50, s, s, "", fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, r=4, sw=2)
    f.text(x + 24, 118, lab.split(":")[0], size=10.5, color=TEAL if ok else RED, bold=True)
    f.text(x + 24, 133, lab.split(": ")[1], size=9.5, color=SLATE)
f.box(180, 156, 380, 74, "", fill=BLUE, stroke=NAVY, r=6)
for j, s in enumerate(["Rules that follow from Fitts's law", "1. Make the main button large and close to the thumb.", "2. Keep 8 dp or more between neighbouring targets.", "3. Never put Delete next to Save."]):
    f.text(190, 172 + j * 16, s, size=9.5 if j else 10.5, color=NAVY if j == 0 else SLATE, bold=(j == 0), anchor="start")
```

```svgfig label="3.4" caption="One task, five interaction styles: send Rs 500 to Hari. Each style has a different cost for the user: the command line needs recalled syntax, the menu needs only a choice, the form needs typing, direct manipulation needs a drag, and the conversation needs plain words. A real app mixes several styles."
f = Fig(580, 214)
names = ["Command line", "Menu selection", "Form fill-in", "Direct manipulation", "Anthropomorphic"]
pro = ["+ fast, scriptable", "+ no recall", "+ structured", "+ intuitive, undo", "+ natural words"]
con = ["- must recall syntax", "- deep menus slow", "- tedious if long", "- needs a metaphor", "- ambiguity, errors"]
for i in range(5):
    x = 4 + i * 115
    f.box(x, 4, 110, 118, "", fill="#ffffff", stroke="#94a3b8", r=5, sw=1.2)
    f.text(x + 55, 134, names[i] if i != 3 else "Direct manip.", size=10, color=NAVY, bold=True)
    f.text(x + 55, 152, pro[i], size=9.5, color=TEAL, bold=True)
    f.text(x + 55, 168, con[i], size=9.5, color=RED, bold=True)
x = 4
f.box(x + 6, 10, 98, 106, "", fill="#0f172a", stroke="#0f172a", r=3)
f.text(x + 12, 28, "> send hari", size=9.5, color="#e2e8f0", anchor="start")
f.text(x + 12, 44, "  --amt 500", size=9.5, color="#e2e8f0", anchor="start")
f.text(x + 12, 60, "OK 500 sent", size=9.5, color="#86efac", anchor="start")
x = 119
for j, t in enumerate(["1 Send money", "2 Balance", "3 Statement", "4 Help"]):
    f.box(x + 8, 14 + j * 26, 94, 22, t, fill=SAND if j == 0 else BLUE, stroke=AMBER if j == 0 else NAVY, size=9.5, bold=True, r=3)
x = 234
for j, t in enumerate(["To: Hari", "Amount: 500"]):
    f.box(x + 8, 16 + j * 32, 94, 24, t, fill="#f8fafc", stroke="#94a3b8", size=9.5, r=3)
f.box(x + 28, 86, 54, 22, "Send", fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=4)
x = 349
f.text(x + 55, 26, "Rs 500", size=11, color=NAVY, bold=True)
f.box(x + 10, 44, 90, 8, "", fill="#e2e8f0", stroke="#94a3b8", r=4, sw=1)
f.box(x + 10, 44, 54, 8, "", fill=TEAL, stroke=TEAL, r=4, sw=1)
f.circle(x + 64, 48, 9, fill="#ffffff", stroke=TEAL, sw=2.5)
f.box(x + 12, 80, 86, 24, "drag to send", fill=MINT, stroke=TEAL, size=9.5, bold=True, r=12)
f.arrow([(x + 18, 70), (x + 90, 70)], color=SLATE, sw=1.3)
x = 464
f.box(x + 8, 14, 94, 26, "Send 500 to Hari", fill=BLUE, stroke=NAVY, size=9.5, bold=True, r=10)
f.box(x + 8, 50, 94, 26, "Sure. Confirm?", fill=SAND, stroke=AMBER, size=9.5, bold=True, r=10)
f.box(x + 8, 86, 94, 26, "Yes", fill=BLUE, stroke=NAVY, size=9.5, bold=True, r=10)
f.text(6, 200, "Real products mix styles: canvas, menus, forms and shortcuts.", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="3.5" caption="The eight steps of the UI design process, each with the artefact it produces. Steps 1 to 5 prepare the design; steps 6 to 8 check and ship it; the results of steps 6 to 8 send the team back to steps 1 to 5. No step is finished once and forgotten."
f = Fig(580, 206)
steps = [("1 Understand", "personas, journeys"), ("2 Requirements", "user stories, flows"), ("3 Structure", "sitemap, navigation"), ("4 Wireframe", "low-fidelity screens"),
         ("5 Visual design", "grid, colour, type"), ("6 Prototype, test", "clickable, test report"), ("7 Hand off", "specs, tokens, library"), ("8 Build, measure", "analytics, A/B tests")]
for i, (a, b) in enumerate(steps):
    x = 6 + (i % 4) * 143
    y = 8 if i < 4 else 108
    fl, st = (BLUE, NAVY) if i < 5 else (MINT, TEAL)
    f.box(x, y, 132, 54, "", fill=fl, stroke=st, r=8, sw=1.6)
    f.text(x + 66, y + 20, a, size=10.5, color=st, bold=True)
    f.text(x + 66, y + 40, b, size=9.5, color=SLATE)
    if i % 4 < 3:
        f.arrow([(x + 132, y + 27), (x + 143, y + 27)], color=SLATE, sw=1.4)
f.arrow([(501, 62), (501, 85), (72, 85), (72, 108)], color=SLATE, sw=1.4)
f.arrow([(72, 162), (72, 186), (290, 186)], color=TEAL, sw=1.3, dash=True)
f.text(298, 187, "iterate: steps 6 to 8 feed new findings back into steps 1 to 5", size=9.5, color=TEAL, bold=True, anchor="start", vmid=True)
```

```svgfig label="3.6" caption="Responsive breakpoints. The same content is rearranged as the screen widens: one column with bottom navigation on a phone (under about 600 px), two columns on a tablet (600 to 900 px), and three columns with a sidebar on a desktop (over about 1200 px). The designer chooses the breakpoints; the browser does not know the content."
f = Fig(580, 214)
def frame(x, w, h, cols, side, title, sub):
    f.box(x, 6, w, h, "", fill="#ffffff", stroke=SLATE, r=6, sw=2)
    f.box(x + 4, 10, w - 8, 14, "", fill=NAVY, stroke=NAVY, r=2)
    top = 30
    left = x + 4
    if side:
        f.box(left, top, 36, h - 30, "", fill=SAND, stroke=AMBER, r=2, sw=1)
        left += 42
    avail = x + w - 4 - left
    cw = (avail - (cols - 1) * 6) / cols
    for c in range(cols):
        for r_ in range(2 if cols < 3 else 2):
            f.box(left + c * (cw + 6), top + r_ * ((h - 34) / 2), cw, (h - 34) / 2 - 6, "", fill=BLUE, stroke=NAVY, r=2, sw=1)
    f.text(x + w / 2, h + 22, title, size=10.5, color=NAVY, bold=True)
    f.text(x + w / 2, h + 38, sub, size=9.5, color=SLATE)
frame(14, 80, 130, 1, False, "Phone", "under 600 px")
f.box(18, 124, 72, 10, "", fill=NAVY, stroke=NAVY, r=2)
frame(120, 170, 130, 2, False, "Tablet", "600 to 900 px")
frame(318, 256, 130, 3, True, "Desktop", "over 1200 px, sidebar")
f.text(14, 196, "Phone: 1 column, bottom bar.   Tablet: 2 columns.   Desktop: 3 columns + sidebar.", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="3.7" caption="The response-time ladder on a logarithmic scale. Up to about 0.1 s a response feels instant; the Doherty threshold of about 0.4 s keeps the user's attention; at 1 s the flow of thought is kept but a spinner should appear; at 10 s attention is lost and a progress bar with an estimate is needed. Animations need a new frame every 16.7 ms (60 frames per second)."
f = Fig(580, 214)
L = lambda t: 40 + 190 * (__import__("math").log10(t) + 1)
f.line(30, 106, 548, 106, color=SLATE, sw=2)
items = [(0.1, "0.1 s", "feels instant", "no feedback needed", True), (0.4, "0.4 s", "Doherty threshold", "keep attention", False),
         (1.0, "1 s", "flow of thought kept", "show a spinner", True), (10, "10 s", "attention lost", "progress bar + estimate", False)]
for t, lab, a, b, up in items:
    x = L(t)
    f.circle(x, 106, 5, fill=AMBER, stroke=AMBER)
    f.text(x, 124 if up else 90, lab, size=10.5, color=AMBER, bold=True)
    bx = max(6, min(x - 62, 580 - 130))
    y = 20 if up else 142
    f.box(bx, y, 124, 52, "", fill=MINT if up else SAND, stroke=TEAL if up else AMBER, r=6)
    f.text(bx + 62, y + 20, a, size=9.5, color=NAVY, bold=True)
    f.text(bx + 62, y + 38, b, size=9.5, color=SLATE)
    f.line(x, 72 if up else 142, x, 101 if up else 112, color="#94a3b8", sw=1, dash=True)
f.text(290, 204, "time after the user acts (log scale)", size=9.5, color=SLATE, bold=True)
```

### 3.7.1 Eight guidelines for designing user interfaces in Nepal

1. **Show the system status.** After every tap the screen must answer: a pressed state, a spinner or a message. When a Fonepay or ConnectIPS payment is processing, say so and say how long it may take. Without feedback people tap twice and pay twice.
2. **Be consistent.** The same action must look and work the same everywhere in the app. If "Pay" is a blue button on one screen, it must not be a green link on another. Consistency lets a user learn once and use everywhere, which matters for first-time users of the Nagarik App.
3. **Prefer recognition to recall.** Show the options instead of asking people to remember them. A list of saved payees in eSewa or Khalti is faster and safer than typing a number. This follows Miller's law, because short-term memory holds only about seven items.
4. **Make targets big and close.** Fitts's law (Fig. 3.1) says that large, near targets are fast to hit. Keep primary buttons at least 48 dp, put them in the thumb zone (Fig. 3.3) and never place Delete beside Save. Many Nepali users work one-handed on a bus or in sunlight.
5. **Limit the choices at one moment.** Hick's law (Fig. 3.2) shows that time grows with every extra option. Group long lists, put the most common choice first and reveal advanced options only on request. A tax or exam-form portal should show one step at a time.
6. **Prevent errors and allow recovery.** Disable the Submit button until the form is valid, ask for confirmation before a destructive action and offer undo. Write messages such as "The phone number must have 10 digits" instead of "Error 17". Users who can recover feel safe.
7. **Design for people and context.** Use Nepali (Devanagari) text, Nepali numerals and the Bikram Sambat date when users expect them. Never use colour alone (Plate 3.2b), keep contrast high and respect the body of the reader: older eyes, small screens, bright light. Test with real users, not only with the team.
8. **Respect time, device and network.** Respond within about 0.4 s and show progress for longer waits (Fig. 3.7). Use responsive breakpoints (Fig. 3.6), small images and offline-friendly screens, because a cheap phone on a weak 4G link is the normal case in many districts. If the design works there, it works everywhere.

## Formula and fact sheet

- Fitts: MT = a + b · log₂(D/W + 1); bigger and closer is faster. Hick: T = b · log₂(n + 1).
- Interaction styles: command line, menu selection, form fill-in, direct manipulation, anthropomorphic.
- Touch target ≥ 44 × 44 px (iOS) / 48 × 48 dp (Android). Response under ~0.1 s feels instant, ~1 s keeps flow, ~10 s loses attention (Nielsen).
- Miller: 7 ± 2 chunks. Doherty: respond within about 400 ms.
- Golden rules: consistency, shortcuts, feedback, closure, error handling, easy reversal, user control, low memory load.

## Chapter summary

- GUIs use windows, icons, menus and a pointer; web UIs add browser conventions, unknown screens and scanning behaviour.
- Five interaction styles each fit a task and user: command line, menus, forms, direct manipulation, anthropomorphic.
- UI principles stress consistency, feedback, affordance, error prevention and control; Fitts's and Hick's laws quantify pointing and choosing.
- The UI process runs from understanding and structure through wireframes, visual design, prototype, test and hand-off.
- Design must respect human limits (perception, memory, attention, motor skill, culture) and technical limits (devices, platforms, performance, network, accessibility technology).

## Practice

1. Differentiate between a GUI and a web UI.
2. Compare the five interaction styles with one example each.
3. State Fitts's law. For a = 0.1 s, b = 0.15 s/bit compute MT for D = 200 px with W = 20 px and with W = 40 px, and interpret.
4. State Hick's law and compute T for 3, 7 and 15 choices when b = 0.2 s.
5. List Shneiderman's eight golden rules.
6. What is affordance? Give two examples of good and bad affordance.
7. Describe the UI design process in steps.
8. Explain four human factors that affect screen design and the design response.
9. Explain four technological considerations in interface design with reference to Nepal.
10. Why are screen edges easy targets? Why must touch targets be at least 44 px?

::: note Answers and worked solutions
**1.** A GUI is a graphical interface of an installed application with controlled windows; a web UI runs in a browser, must be responsive across unknown screens, depends on the network and inherits browser conventions.
**2.** Table in 3.2: command line (`git`), menu selection (ATM), form fill-in (admission form), direct manipulation (drag-and-drop), anthropomorphic (chatbot).
**3.** MT = a + b log₂(D/W + 1): W = 20 → 0.1 + 0.15 × 3.46 = **0.619 s**; W = 40 → 0.1 + 0.15 × 2.58 = **0.488 s**. Doubling the target width saves about 21 % of the time.
**4.** T = b log₂(n + 1): n = 3 → 0.4 s; n = 7 → 0.6 s; n = 15 → 0.8 s.
**5.** Section 3.3 list.
**6.** Affordance = a perceived cue for how an object can be used. Good: a raised button, a text field with a caret. Bad: a flat label that is actually a link, a door with a handle that must be pushed.
**7.** Understand → requirements/task flows → structure/IA → sketch/wireframe → visual design → prototype and test → hand-off → measure and iterate.
**8.** E.g. perception (don't rely on colour alone), memory (recognition over recall), attention (one focus per screen), motor skill (large targets, bottom navigation), culture (localise, support Devanagari).
**9.** Low-end phones (performance and size), slow/unstable network (offline mode, small payloads), screen sizes (responsive), sunlight (high contrast), Android conventions (Material Design), Nepali fonts and calendar.
**10.** The pointer stops at the screen edge, so the target is effectively infinitely deep (W → ∞ in Fitts's law); fingertips are about 10 mm wide, and smaller targets cause mis-taps.
:::

## Model answers for Unit 3

**Q1. Explain the five interaction styles with their strengths, weaknesses and examples. How would you choose between them? (10 marks)**

**Introduction.** An **interaction style** is the way a user and a system exchange information. Five styles are classical: command line, menu selection, form fill-in, direct manipulation and anthropomorphic (natural-language or human-like) interaction. Plate 3.1 shows four of them on real devices, and Fig. 3.4 compares all five on one task, sending Rs 500 to Hari.

**The five styles.**

1. **Command line.** The user types commands with arguments, such as `ls -l` or `git commit`. It is very powerful, scriptable and light on resources, but the user must recall the syntax and the style is hard to discover.
2. **Menu selection.** The user chooses an item from a displayed list, as on an ATM (Plate 3.1b). No memorisation is needed and the limited choices reduce errors, but deep menus are slow and experts feel held back.
3. **Form fill-in.** The user enters data into labelled fields, as in a sign-up or admission form. It is structured and guides the user, but long forms are tedious and need validation.
4. **Direct manipulation.** The user acts on visible objects with immediate, reversible results: dragging a file, pinching a map, sliding a slider. It is intuitive and low in errors, but needs a good visual metaphor and is poor for repetitive work.
5. **Anthropomorphic.** The system talks in human-like language, by chat or voice (Plate 3.1d). It is natural and accessible, but suffers from ambiguity, recognition errors and privacy worries.

| Style | Learning effort | Speed for experts | Error risk | Example |
|---|---|---|---|---|
| Command line | high | very high | high | server shell |
| Menu selection | low | medium | low | ATM, IVR |
| Form fill-in | low | medium | medium | tax or exam form |
| Direct manipulation | low | high | low | map, photo editor |
| Anthropomorphic | very low | medium | medium | chatbot, voice assistant |

**Choosing.** Choose by user, task and context: experts doing repeated work want a CLI or shortcuts; first-time public users want menus and forms; hands-busy users want voice; visual tasks want direct manipulation.

**Conclusion.** No style wins everywhere. Good products mix them: direct manipulation for the canvas, menus for commands, forms for settings and a command palette for experts. The designer must test the mix with real users.

**Q2. Differentiate between a desktop GUI and a web user interface. Why do web users scan instead of read? (5 marks)**

A **graphical user interface (GUI)** shows information as visual objects that the user controls with a pointer or touch. Its building blocks are summarised as **WIMP**: windows, icons, menus and pointer. A **web user interface** is a GUI that is delivered through a browser.

| Point | Desktop GUI | Web UI |
|---|---|---|
| Delivery | installed on the computer | loaded in a browser |
| Window | designer controls size and chrome | unknown screen, browser and speed, so it must be responsive |
| Speed | instant response | network delay, page loads |
| Conventions | follow the operating system | follow other websites (logo top-left goes home) |
| Navigation | menus along the top | the central design problem; users arrive by search on any page |
| Users | known, trained | anyone, mostly first-time visitors |

**Why users scan.** Web users have a goal, little patience and many alternatives, so they leave within seconds. They look for headings, links and images that answer their question (Plate 3.2c shows the F-shaped path of the eye). The design response is short text, clear headings, a strong visual hierarchy, a fast page and the main action placed at the top and left.

**Example.** A student who opens a result portal wants only a roll-number box and a View button; any extra banner is ignored.

**Q3. Explain the principles of UI design. Include Norman's ideas, Shneiderman's eight golden rules and the laws of Fitts and Hick with worked numbers. (10 marks)**

**Introduction.** Principles of UI design are tested rules that make interfaces clear, consistent and forgiving. The best-known sets are Shneiderman's **Eight Golden Rules**, Nielsen's ten heuristics (Unit 7) and Norman's design principles.

**Core principles.**

- **Visibility and feedback.** Every action gets a response: a button state, a progress bar or a message.
- **Consistency.** The same action looks and works the same everywhere.
- **Affordance and signifiers (Norman).** The design shows what can be done; a **mapping** links controls to effects; **constraints** prevent wrong actions, such as disabling Submit until the form is valid.
- **Recognition over recall, and error prevention with recovery:** confirm destructive actions, offer undo, write helpful messages.
- **User control, shortcuts for experts and defaults for novices, and minimalism.**

**Shneiderman's eight golden rules:** strive for consistency; enable shortcuts; offer informative feedback; design dialogues to yield closure; offer simple error handling; permit easy reversal; support an internal locus of control; reduce short-term memory load.

**Fitts's law.** MT = a + b log2(D/W + 1). With a = 0.1 s and b = 0.15 s per bit, a 20 px button at 200 px takes 0.619 s; a 40 px button at the same distance takes 0.488 s, which is 21 percent faster (Fig. 3.1).

**Hick's law.** T = b log2(n + 1). With b = 0.2 s, 7 choices take 0.6 s and 31 choices take 1.0 s (Fig. 3.2): doubling the options adds only a constant 0.2 s.

| Law | Says | Design response |
|---|---|---|
| Fitts | big and near is fast | large primary buttons, thumb zone |
| Hick | more choices, slower decision | group lists, highlight a default |
| Miller | memory holds 7 +/- 2 chunks | chunk numbers: 98 4123 4567 |
| Doherty | respond in about 0.4 s | spinner after 1 s, progress bar after 10 s |

**Worked example.** A bill-payment screen applies the principles together. It shows a spinner and then a green success message (feedback), keeps the same blue Pay button on every screen (consistency), lists saved biller names (recognition), disables Pay until the amount is valid (constraint), asks "Pay Rs 1,250 to NEA?" before the final step (error prevention) and offers a clear Cancel (user control). The Pay button is 48 dp high and sits in the thumb zone, so Fitts's law favours it.

**Conclusion.** The principles agree: show the user where they are, keep behaviour predictable, make the right action easy and the wrong action hard, and undo whatever goes wrong.

**Q4. Using a = 0.1 s and b = 0.15 s/bit, find the Fitts movement time for a 40 px button at 600 px and for an 80 px button at 600 px. Using b = 0.2 s, find the Hick decision time for 10 and 63 choices. Comment on the results. (5 marks)**

**Fitts's law.** MT = a + b log2(D/W + 1).

- For W = 40 px and D = 600 px: D/W + 1 = 16, log2 16 = 4.000, so MT = 0.1 + 0.15 x 4.000 = **0.700 s**.
- For W = 80 px and D = 600 px: D/W + 1 = 8.5, log2 8.5 = 3.087, so MT = 0.1 + 0.15 x 3.087 = **0.563 s**.

Doubling the width saves 0.137 s, about 20 percent.

**Hick's law.** T = b log2(n + 1).

- For n = 10: log2 11 = 3.459, so T = 0.2 x 3.459 = **0.692 s**.
- For n = 63: log2 64 = 6.000, so T = 0.2 x 6.000 = **1.200 s**.

The number of options grew more than six times, but the time grew less than twice.

**Comment.** A larger target is a cheap way to speed up a click, so primary buttons should be big. Hick's law shows that the time to decide grows slowly with the number of choices, but real long lists are still hard because the eye must scan them. Designers should group, order and search long lists and highlight a recommended choice.

**Q5. Describe the steps of the UI design process and the artefact produced at each step. (5 marks)**

The UI design process (Fig. 3.5) turns research into a built and measured interface in eight steps.

1. **Understand** users, tasks and context; the output is personas and journey maps (Unit 2).
2. **Define requirements and task flows** as user stories and use cases, for example "As a student I want to pay the exam fee".
3. **Structure** the product with information architecture, a sitemap and a navigation model (Unit 5).
4. **Sketch and wireframe** each screen at low fidelity (Unit 6).
5. **Design the visual layer**: grid, colour, typography, components and every state (empty, loading, error).
6. **Prototype and test**: a clickable model is tried with real users (Unit 7).
7. **Hand off** to developers with specifications, design tokens and a component library.
8. **Build, measure and iterate** using analytics, feedback and A/B tests.

Related practices are **atomic design** (atoms, molecules, organisms, templates, pages), a **design system** of documented components and agile work with developers. The loop never ends: findings from steps 6 to 8 send the team back to earlier steps.

**Example.** For an exam-fee screen, the artefacts are Sita's persona, a user story, a three-screen sitemap, paper wireframes, a blue and white colour set, a Figma prototype tested with five students, a hand-off file and a conversion rate measured after launch.

**Q6. Discuss the human considerations and the technological considerations in interface design. (10 marks)**

**Introduction.** A screen is used by a human being on a real device. The designer must therefore consider both the human factors and the technological factors, and design for the worst plausible conditions: a cheap phone, a slow network, bright sunlight and one hand.

**Human considerations.**

1. **Perception.** Detail is seen only at the centre of vision; users scan in F or Z patterns (Plate 3.2c). About 1 in 12 men have colour-vision deficiency (Plate 3.2b), so never rely on colour alone and keep contrast high.
2. **Attention.** Attention is limited; use one focus per screen and put key actions where users look.
3. **Memory.** Short-term memory holds about 7 +/- 2 chunks, so prefer recognition to recall and chunk long numbers.
4. **Learning and mental models.** Match conventions and familiar metaphors such as folder, trash and cart.
5. **Motor skills.** Pointing follows Fitts's law; use large targets and bottom navigation on phones (Fig. 3.3).
6. **Culture and emotion.** Reading direction, colour meanings, date formats and gestures differ; support Devanagari, Nepali numerals and the Bikram Sambat calendar, and write calm, blame-free messages.

**Technological considerations.**

| Factor | Consideration |
|---|---|
| Devices and input | mouse, touch, stylus, voice; no hover on touch screens |
| Screen | size, pixel density, orientation; responsive breakpoints (Fig. 3.6) |
| Platform | Material Design on Android, Human Interface Guidelines on iOS, web conventions |
| Performance | first useful screen in 2 to 3 s; 16.7 ms per frame (Fig. 3.7) |
| Network | 2G and 3G in rural Nepal: offline mode, small payloads, retry |
| Accessibility technology | screen readers (TalkBack, NVDA), correct labels and focus order |
| Security and privacy | masked input, clear permission requests, safe defaults |

**Worked example.** A village health-post app is used by a nurse on a 3 GB phone, outdoors, over a weak signal. The human factors give large Nepali text, high contrast that survives sunlight, big buttons for gloved or hurried hands and a calm tone for error messages. The technology factors give an offline mode that saves records and syncs later, small images, a first screen in under three seconds and TalkBack labels for accessibility. Each decision traces back to a person or a device.

**Conclusion.** Human factors tell the designer what people can see, remember and reach; technological factors tell what the device and network can deliver. A design is good only when both agree.

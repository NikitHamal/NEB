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

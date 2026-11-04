---
subject: UX/UI Design
grade: BCA Semester 2
unit: 6
title: Wireframing and Prototyping
area: BCA 155 · UX/UI Design · Unit 6
---

Before building anything expensive, build something cheap and learn from it. This unit covers wireframes and mock-ups, low- and high-fidelity prototypes, interactive and software prototyping, storyboards, transitions and animation, and the steps of creating a simple clickable prototype — the skills the 48-hour lab practises.

::: key What this unit gives you
- Wireframes versus mock-ups versus prototypes.
- Low-fidelity and high-fidelity prototyping, with the trade-offs.
- Interactive prototypes and software prototyping tools.
- UX storyboarding.
- Transitions and animation, and how to create a simple clickable prototype.
:::

## 6.1 From idea to product: the fidelity ladder

| Artefact | What it shows | Fidelity | Made in | Used to |
|---|---|---|---|---|
| **Sketch** | rough ideas | very low | pen and paper | explore many ideas |
| **Wireframe** | structure and layout, no visual style | low | paper, Balsamiq, Figma | agree on content and flow |
| **Mock-up** | static, full visual design | high (visual) | Figma, XD, Sketch | agree on look and feel |
| **Prototype** | interactive simulation | low to high | Figma, paper, code | test the experience |
| **Product** | working software | final | code | ship |

The rule: **the earlier the stage, the cheaper the change.** A line moved on a wireframe costs seconds; the same change after coding costs days.

## 6.2 Wireframes

A **wireframe** is a simple, **black-and-white (grey-box) layout** of a screen that shows **what goes where**: the structure, content blocks, navigation, hierarchy and the functional elements — without colours, real images or final typography. Its purpose is to discuss **layout and function** without being distracted by aesthetics.

Conventions: boxes with a cross for images; horizontal lines or "Lorem ipsum" for text blocks (or real headings — real content is better); rectangles for buttons and inputs labelled with their action; annotations numbered and explained beside the frame; a few greys only.

| Level | Description |
|---|---|
| **Low-fidelity wireframe** | rough, often hand-sketched; no measurements; focuses on flow and concept |
| **Mid-fidelity wireframe** | digital, aligned to a grid, real labels, realistic proportions, still grey |
| **High-fidelity wireframe** | detailed layout with real content and exact spacing but little or no colour |

### What a wireframe must specify
Page purpose and **primary action**; content blocks and their **priority** (hierarchy); navigation (global, local, breadcrumbs); form fields and buttons; states (empty, error, loading) for important screens; **annotations** for behaviour ("clicking opens a modal"); the **flow** to the next screen. A set of wireframes connected by arrows forms a **user flow** or **screen flow**.

### Wireframing process

1. Review the personas, journey map, requirements and the site map.
2. List the screens (**screen inventory**) and the **task flow** for each key task.
3. **Sketch** each screen quickly (Crazy 8s).
4. Choose a **grid** and a **device** (design the smallest screen first).
5. Build the wireframes digitally, with real content where possible.
6. **Annotate** and number the notes.
7. **Review** with stakeholders and developers; **test** with 3–5 users using a clickable wireframe; revise.

::: example Worked example: a wireframe described in words
**Login screen (mobile, 360 px):** top: logo centred (48 px); heading "Welcome back"; below, an email field (label above, 48 px high), a password field with a show-password toggle, a full-width primary button **Log in**, below it a text link **Forgot password?**, and at the bottom the line "New here? **Create account**". Annotation 1: *"Log in" disabled until both fields are valid.* Annotation 2: *Wrong password: inline error under the password field, no page reload.* Hierarchy: heading → fields → primary button → secondary links. There is exactly one primary action.
:::

### Mock-ups
A **mock-up** is a **static, high-fidelity visual design** of a screen: real colours, typography, imagery, icons and spacing — what the product will look like — but not clickable. It applies the style guide to the wireframe. It is used to get visual sign-off and as the **source for developer hand-off** (measurements, assets, styles). A **style tile** or **mood board** precedes it; a **design system** keeps all mock-ups consistent.

## 6.3 Prototyping

A **prototype** is an **early, simplified, interactive simulation** of a product that lets you try the design and learn before the real build. Why: test usability cheaply, communicate ideas, get stakeholder buy-in, find problems early, and give developers a clear target.

### Low-fidelity prototyping

| | **Low-fidelity** | **High-fidelity** |
|---|---|---|
| Appearance | rough: paper, grey boxes, simple clickable wireframes | realistic: final colours, type, images, animations |
| Interaction | manual ("Wizard of Oz": a person plays the computer) or basic links | realistic clicks, transitions, form behaviour, sometimes real data |
| Speed and cost | minutes to hours; very cheap | hours to days; more expensive |
| Best for | early concept and flow testing; structure and content | late validation, visual and detailed interaction testing, stakeholder demos, developer reference |
| Feedback you get | about flow, labels, concept | about visual design, micro-interactions, finer usability |
| Risk | users may struggle to imagine; less realistic response | people comment on colours instead of function; cost of changes; team becomes attached |

**Paper prototyping**: draw screens on cards; a "facilitator" swaps the cards in response to the user's finger taps while a note-taker records. Fast and effective for testing flows. **Vertical** prototypes implement one feature in depth; **horizontal** prototypes show the whole breadth at shallow depth.

### High-fidelity and interactive prototyping

An **interactive prototype** links screens so the user can click through the flow. Elements: **hotspots/triggers** (click, tap, drag, hover, key press, after-delay), **actions** (navigate to a frame, open an overlay, scroll, change a component's variant, set a variable), **transitions** (how the next screen arrives), **overlays** (modals, drawers), **states/variants** of components (default/hover/pressed), and sometimes **variables and conditional logic** (e.g. show an error if the field is empty).

### Software prototyping tools

| Tool | Strength |
|---|---|
| **Figma** | design and prototype in one file; components with variants; Smart Animate; variables and conditional logic; prototypes shareable by link; free tier |
| **Adobe XD** | (maintenance mode) simple linking, auto-animate, voice prototyping |
| **Sketch** + plugins / Principle / InVision | macOS design, with separate prototyping tools |
| **Balsamiq** | intentionally sketchy low-fidelity wireframes |
| **Axure RP** | complex logic and conditional prototypes, documentation |
| **ProtoPie, Framer** | advanced, code-like interactions and sensors |
| **Marvel, Proto.io** | quick clickable image-based prototypes |
| **Code prototypes** (HTML/CSS/JS, Flutter) | when the interaction needs real behaviour |

### Software prototyping (in the software-engineering sense)
In software engineering, **prototyping** also means building a working early version to clarify requirements. **Throwaway (rapid) prototype**: built quickly to explore, then discarded; **evolutionary prototype**: refined step by step into the final system; **horizontal** (interface only) and **vertical** (a thin full slice) prototypes. Risk: stakeholders mistaking a prototype for the finished product or, worse, shipping it. UX prototypes are normally **throwaway**.

## 6.4 UX storyboarding

A **storyboard** is a sequence of drawn panels, like a comic strip, that shows **a user in a context achieving a goal with the product**. It puts the **human story** and the **environment** around the screens: where the user is, what triggers the need, what happens, how the user feels at the end.

Elements: a **persona** (character), a **scenario**/setting, a **trigger** (problem), **steps** of interaction (one panel each; typically 4–8), a **resolution** (outcome), short **captions** and (optionally) **emotion** cues. Use simple drawings, stick figures, speech bubbles.

::: example Worked example: a storyboard in six panels
*Persona: Sita, BCA student, bus to college.* 1. **Context** — Sita on the bus sees a notice: exam forms close tonight. 2. **Trigger** — she worries about travelling back to college before the deadline. 3. **Interaction** — she opens the college app, which has autosaved yesterday's partial form. 4. **Interaction** — she pays with eSewa in two taps. 5. **Feedback** — the app shows a green confirmation and the receipt; an SMS arrives. 6. **Outcome** — Sita smiles and puts the phone away. Storyboards reveal needs the screens alone do not: poor connectivity on the bus ⇒ the design needs offline autosave.
:::

Uses: communicate a concept, justify features, find missing steps and edge cases, align the team. **Storyboard types**: **scenario storyboards** (the whole story), **screen storyboards** (the sequence of screens, the same as a screen flow), **video prototypes**.

## 6.5 Transitions and animation in prototypes

**Motion** explains changes, gives feedback, directs attention and adds personality — but must serve a purpose.

| Purpose | Example |
|---|---|
| **Orientation** | a new screen slides in from the right, so "back" is obviously to the left |
| **Feedback** | a button depresses, a heart pulses after "like" |
| **Status** | a spinner or skeleton screen while loading |
| **Focus** | a shake on an invalid field; a highlight on a new item |
| **Continuity** | a thumbnail expands into the detail view (shared-element transition) |
| **Delight / brand** | a small celebratory animation on completing a task |

### Transition types in prototyping tools
**Instant**, **dissolve/fade**, **slide in/out** (left, right, up, down), **push**, **move in/out**, and **Smart Animate** (Figma) / **Auto-Animate** (XD) — the tool interpolates between two frames in which matching layers differ in position, size, colour or opacity.

### Timing and easing

- **Duration**: micro-interactions 100–200 ms; small transitions 200–300 ms; large transitions (full-screen) 300–500 ms; avoid > 500 ms — it feels sluggish. Mobile is a bit shorter than desktop.
- **Easing** (the speed curve): **ease-out** (fast start, slow end) for things *entering*; **ease-in** (slow start, fast end) for things *leaving*; **ease-in-out** for moving between points; **linear** only for continuous loops (spinners). Natural motion is never perfectly linear.
- **Accessibility**: some users get motion sickness or distraction — respect the system's **reduce motion** setting and avoid flashing (no more than three flashes per second); animation must never be the only way to convey information.
- **Performance**: animate `transform` and `opacity` (cheap) rather than layout properties; aim for 60 frames per second (16.7 ms per frame).

The 12 principles of animation (Disney), adapted for UI: **ease in/out** (slow in, slow out), **anticipation** (a slight pull-back before an action), **follow-through**, **staging**, **timing**, **secondary action**.

## 6.6 Creating a simple clickable prototype (the lab method)

A clickable prototype of a three-screen flow (Home → Product → Checkout confirmation) in Figma, or the equivalent in XD or Sketch:

1. **Set up**: create a file; choose the device frame (e.g. 360 × 800 for Android); set a **layout grid** (4 columns, 16 px margins) and **8 px spacing**.
2. **Define styles**: colour styles (primary, neutrals, semantic), text styles (H1–H3, body, caption), effect styles (shadow).
3. **Build components** once: button (variants primary/secondary, states default/hover/disabled), text field, card, top app bar, bottom tab bar. Use **auto layout** so components resize with their content.
4. **Design the three frames** from your wireframes using the components; name layers and frames clearly.
5. **Switch to prototype mode** and draw **connections**: from the "Buy now" button to the Checkout frame (trigger *On tap*, action *Navigate to*, animation *Smart animate* or *Slide in*, 300 ms, ease-out); from the Back arrow to the previous frame; from the tab-bar icons to their frames.
6. **Add an overlay** (a modal or bottom sheet) with *Open overlay* and a *Close overlay* action; add a **component variant** change for a pressed state and an **After delay** trigger for a splash screen.
7. **Set the starting frame** and **device preview**; run the prototype on a phone (the tool's mobile app) or in the browser.
8. **Test**: ask a colleague to complete a task ("Buy the blue shirt") while thinking aloud; note where they hesitate; fix and re-test.
9. **Share**: a link with comment access; **hand-off** via Dev Mode or inspect panel (spacing, colours, text styles, exported assets).

The lab outcomes in the syllabus map directly to these steps: using the tool's features; page layout, fonts and responsive design; colour theory and typography; grids and layouts; interactive elements; windows and controls; navigation styles; wireframes and prototypes; storyboards; effects, styles and animation.

## 6.7 Seeing the ideas: sketches, wireframes, prototypes, storyboards and motion

A prototype is a question asked cheaply. Plate 6.1 shows four real ones: hand-drawn screens on a desk, a paper prototype on a tablet, a cardboard mock-up of a hardware panel and a six-panel storyboard. Plate 6.2 shows a design teacher at a whiteboard and the difference between a horizontal and a vertical prototype. The figures then draw the fidelity ladder with the cost of change, annotate a real wireframe, show one screen at three fidelities, connect three frames into a clickable flow, tell a story in six panels and plot the easing curves that make motion feel natural.

```photogrid label="6.1" cols="4" ratio="1.0" caption="Four cheap prototypes. (a) Hand-drawn screens on a desk (CC BY-SA 4.0): paper wireframes can be redrawn in a minute, so many ideas get tested. (b) A paper prototype taped to a tablet (CC BY-SA 4.0): the paper buttons are the interface and a facilitator swaps the sheets when the user taps. (c) A cardboard and graph-paper mock-up of a synthesiser front panel (CC BY-SA 2.0): the maker checked the spacing of the jacks on card before drilling metal. (d) A storyboard of a phone app in two rows of three panels (CC BY-SA 4.0): the user, the place and the moment are drawn before any screen is built."
@ photo id="bca155/paperweb" cap="Hand-drawn screens"
fit 1.0
focus 0.45 0.5
call 0.5 0.9 0.4 0.55 "paper screens"
@ photo id="bca155/paperipad" cap="Paper on a tablet"
fit 1.0
focus 0.5 0.55
@ photo id="bca155/cardboard" cap="Cardboard mock-up"
fit 1.0
focus 0.4 0.5
call 0.5 0.08 0.35 0.55 "jack layout"
@ photo id="bca155/storyb" cap="Storyboard panels"
fit 1.0
focus 0.4 0.5
```

```photogrid label="6.2" cols="2" ratio="1.35" caption="Plate 6.2. (a) An interaction-design teacher sketching a model on a whiteboard (CC BY-SA 3.0): design thinking is done in public, with marker pens, before any code exists. (b) Horizontal and vertical prototypes: a horizontal prototype shows every feature but only the surface of each, so it tests navigation and labels; a vertical prototype builds one feature all the way down, so it tests whether that feature really works."
@ photo id="bca155/verplank" cap="Sketching a model on a whiteboard"
fit 1.35
focus 0.65 0.5
call 0.25 0.1 0.45 0.6 "whiteboard sketch"
@ svg cap="Horizontal and vertical prototypes"
f = Fig(280, 205)
feats = ["Search", "Cart", "Pay", "Track"]
f.text(140, 12, "Depth of each feature", size=10, color=SLATE, bold=True)
for c in range(4):
    f.text(38 + c * 58, 30, feats[c], size=10, color=NAVY, bold=True)
    for r in range(4):
        h = r == 0
        v = c == 2
        fill = MINT if h else ("#fde68a" if v else "#ffffff")
        stroke = TEAL if h else (AMBER if v else "#cbd5e1")
        f.box(10 + c * 58, 38 + r * 28, 52, 24, "", fill=fill, stroke=stroke, r=3, sw=1.4)
f.text(140, 162, "green row = horizontal: all features, shallow", size=10, color=TEAL, bold=True)
f.text(140, 180, "amber column = vertical: one feature, deep", size=10, color=AMBER, bold=True)
f.text(140, 198, "most projects need both, in that order", size=10, color=SLATE)
```

```svgfig label="6.1" caption="The fidelity ladder and the cost of one change. The five artefacts run from a sketch to the shipped product. The bars show how long one small change (move the Pay button) takes at each stage; the times are illustrative, and the bars use a log scale because the product is hundreds of times slower to change than the sketch. The earlier the stage, the cheaper the lesson."
f = Fig(580, 250)
import math as cm
names = ["Sketch", "Wireframe", "Mock-up", "Prototype", "Product"]
mins = [3, 15, 60, 120, 960]
lab = ["3 min", "15 min", "1 h", "2 h", "2 days"]
sub = ["pen, paper", "grey boxes", "full visuals", "clickable", "real code"]
for i in range(5):
    x = 14 + i * 114
    h = 30 * cm.log10(mins[i]) + 10
    col = [MINT, MINT, BLUE, SAND, "#fee2e2"][i]
    st = [TEAL, TEAL, NAVY, AMBER, RED][i]
    f.box(x, 150 - h, 96, h, "", fill=col, stroke=st, r=4, sw=1.6)
    f.text(x + 48, 144 - h, lab[i], size=11, color=st, bold=True)
    f.box(x, 162, 96, 26, names[i], fill="#ffffff", stroke=st, size=11, bold=True, r=4)
    f.text(x + 48, 204, sub[i], size=10, color=SLATE)
    if i < 4:
        f.arrow([(x + 98, 175), (x + 112, 175)], color=SLATE, sw=1.5)
f.text(290, 226, "fidelity rises left to right; so does the cost of changing your mind", size=10.5, color=NAVY, bold=True)
f.text(290, 242, "bar height = 30 x log10(minutes) + 10 pixels", size=9.5, color=SLATE)
```

```svgfig label="6.2" caption="An annotated wireframe of the login screen from Section 6.2, drawn at half scale of a 360 px by 640 px phone. Grey boxes show structure only: a cross marks the logo image, bars stand for text, and one button is the single primary action. Numbered notes explain behaviour that a picture cannot show. Hierarchy reads top to bottom: heading, fields, primary button, secondary links."
f = Fig(580, 360)
X0, Y0 = 20, 12
f.box(X0, Y0, 180, 336, "", fill="#ffffff", stroke=SLATE, r=14, sw=2)
f.box(X0 + 66, Y0 + 14, 48, 48, "", fill="#e2e8f0", stroke="#94a3b8", r=3)
f.line(X0 + 66, Y0 + 14, X0 + 114, Y0 + 62, color="#94a3b8", sw=1.2)
f.line(X0 + 114, Y0 + 14, X0 + 66, Y0 + 62, color="#94a3b8", sw=1.2)
f.text(X0 + 90, Y0 + 84, "Welcome back", size=12, color=SLATE, bold=True)
f.text(X0 + 14, Y0 + 108, "Email", size=9.5, color=SLATE, anchor="start")
f.box(X0 + 14, Y0 + 114, 152, 24, "", fill="#f1f5f9", stroke="#94a3b8", r=3)
f.text(X0 + 14, Y0 + 158, "Password", size=9.5, color=SLATE, anchor="start")
f.box(X0 + 14, Y0 + 164, 152, 24, "", fill="#f1f5f9", stroke="#94a3b8", r=3)
f.box(X0 + 140, Y0 + 170, 20, 12, "", fill="#e2e8f0", stroke="#94a3b8", r=2)
f.box(X0 + 14, Y0 + 206, 152, 28, "Log in", fill="#475569", stroke="#334155", color="#ffffff", size=11, bold=True, r=4)
f.text(X0 + 90, Y0 + 256, "Forgot password?", size=10, color=SLATE)
f.line(X0 + 14, Y0 + 280, X0 + 166, Y0 + 280, color="#cbd5e1", sw=1)
f.text(X0 + 90, Y0 + 302, "New here? Create account", size=10, color=SLATE, bold=True)
marks = [(1, Y0 + 38, 62, "Logo is a placeholder image:\n48 px, centred, links home."),
         (2, Y0 + 126, 132, "Email field: 48 px high, label\nabove it, email keyboard."),
         (3, Y0 + 176, 176, "Password field: a show toggle\nreveals the text."),
         (4, Y0 + 220, 220, "Log in stays disabled until both\nfields are valid (one primary action)."),
         (5, Y0 + 270, 270, "Wrong password: inline error under\nthe field, no page reload.")]
for n, cy, ty, txt in marks:
    f.circle(X0 + 190, cy, 9, fill=NAVY, stroke=NAVY, label=str(n), size=10, color="#ffffff")
    f.arrow([(X0 + 200, cy), (252, cy)], color=NAVY, sw=1.2)
    f.text(260, cy, txt, size=10, color=SLATE, anchor="start", vmid=True)
f.text(260, 322, "Screen flow: success goes to Home; failure stays here.", size=10, color=TEAL, bold=True, anchor="start")
f.text(260, 340, "Grey only: colour is decided later in the mock-up.", size=10, color=SLATE, anchor="start")
```

```svgfig label="6.3" caption="One screen at three fidelities. (a) A sketch takes about three minutes and invites change: nobody argues about colour. (b) A grey wireframe takes about half an hour and fixes structure, labels and priority. (c) A mock-up takes a few hours and fixes colour, type and imagery. The same four elements (title, picture, price, button) appear in each, but the questions you can ask are different: at (a) 'is this the right idea?', at (b) 'is this the right layout?', at (c) 'does it look right?'."
f = Fig(580, 270)
def phone(x, kind):
    f.box(x, 8, 130, 200, "", fill="#ffffff", stroke=SLATE, r=12, sw=2)
    if kind == 0:
        f.raw('<path d="M %d 30 q 8 -4 16 0 t 32 0 t 32 0" fill="none" stroke="#334155" stroke-width="1.6"/>' % (x + 20))
        f.raw('<path d="M %d 46 l 90 0 l 0 62 l -90 0 z M %d 46 l 90 62 M %d 108 l 90 -62" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 3"/>' % (x + 20, x + 20, x + 20))
        f.raw('<path d="M %d 124 q 10 -3 20 0 t 30 0" fill="none" stroke="#334155" stroke-width="1.6"/>' % (x + 20))
        f.raw('<path d="M %d 150 l 90 1 l 0 24 l -90 -1 z" fill="none" stroke="#334155" stroke-width="1.8"/>' % (x + 20))
        f.text(x + 65, 163, "BUY", size=11, color=SLATE, bold=True)
    elif kind == 1:
        f.box(x + 12, 20, 106, 14, "", fill="#cbd5e1", stroke="#cbd5e1", r=2)
        f.box(x + 12, 42, 106, 66, "image", fill="#e2e8f0", stroke="#94a3b8", r=2, size=10, color=SLATE)
        f.box(x + 12, 116, 60, 10, "", fill="#cbd5e1", stroke="#cbd5e1", r=2)
        f.box(x + 12, 140, 106, 28, "Buy now", fill="#475569", stroke="#334155", color="#ffffff", size=11, bold=True, r=3)
    else:
        f.box(x + 12, 20, 106, 14, "Dhaka topi", fill="#ffffff", stroke="#ffffff", size=10, color=NAVY, bold=True, r=2)
        f.box(x + 12, 42, 106, 66, "", fill="#99f6e4", stroke=TEAL, r=6)
        f.circle(x + 65, 75, 18, fill="#f59e0b", stroke=AMBER)
        f.box(x + 12, 114, 60, 14, "Rs 850", fill="#ffffff", stroke="#ffffff", size=11, color=RED, bold=True, r=2)
        f.box(x + 12, 140, 106, 28, "Buy now", fill=TEAL, stroke=TEAL, color="#ffffff", size=11, bold=True, r=14)
for i in range(3):
    phone(24 + i * 188, i)
heads = [("(a) Sketch: about 3 min", RED), ("(b) Wireframe: about 30 min", NAVY), ("(c) Mock-up: about 3 h", TEAL)]
qs = ["is this the right idea?", "is this the right layout?", "does it look right?"]
for i in range(3):
    f.text(89 + i * 188, 226, heads[i][0], size=10.5, color=heads[i][1], bold=True)
    f.text(89 + i * 188, 244, "asks: " + qs[i], size=10, color=SLATE)
f.text(290, 264, "times are illustrative", size=9.5, color=SLATE)
```

```svgfig label="6.4" caption="A clickable prototype of three frames, as built in Figma. Each arrow is a connection with a trigger, an action and a transition: tapping Buy now navigates to Checkout with Smart animate over 300 ms, ease-out; the Back arrow returns with a 250 ms slide to the right. The size picker is an overlay opened on top of the Product frame, and an After delay trigger moves the splash screen to Home after 1500 ms. The start frame is marked with a flag."
f = Fig(580, 300)
frames = [("Home", 20, "list of products"), ("Product", 220, "photo and price"), ("Checkout", 420, "address, Fonepay")]
for n, x, d in frames:
    f.box(x, 40, 140, 170, "", fill="#ffffff", stroke=NAVY, r=10, sw=2)
    f.box(x, 40, 140, 22, n, fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True, r=8)
    f.text(x + 70, 192, d, size=10, color=SLATE)
f.box(20 + 24, 76, 92, 26, "Splash 1.5 s", fill=SAND, stroke=AMBER, size=9.5, bold=True, r=4)
f.box(220 + 14, 150, 112, 24, "Buy now", fill=TEAL, stroke=TEAL, color="#ffffff", size=10.5, bold=True, r=12)
f.box(420 + 14, 150, 112, 24, "Confirm", fill=TEAL, stroke=TEAL, color="#ffffff", size=10.5, bold=True, r=12)
f.text(30, 30, "start frame", size=9.5, color=RED, bold=True, anchor="start")
f.arrow([(160, 100), (220, 100)], color=NAVY, sw=1.6)
f.text(190, 90, "On tap", size=9.5, color=NAVY, bold=True)
f.arrow([(332, 160), (420, 160)], color=TEAL, sw=1.8)
f.text(376, 148, "On tap", size=9.5, color=TEAL, bold=True)
f.arrow([(420, 196), (360, 196), (360, 204), (360, 222), (160, 222), (160, 204)], color=RED, sw=1.4, dash=True)
f.text(268, 238, "Back: slide right, 250 ms", size=9.5, color=RED, bold=True)
f.box(236, 72, 108, 52, "", fill=SAND, stroke=AMBER, r=6, sw=1.6, dash=True)
f.text(290, 90, "Overlay: size picker", size=9.5, color=AMBER, bold=True)
f.text(290, 108, "S    M    L", size=11, color=AMBER, bold=True)
f.box(10, 258, 560, 36, "", fill=SOFT, stroke="#cbd5e1", r=6, sw=1)
f.text(18, 270, "Connection  =  trigger (tap, drag, hover, key, after delay)  +  action (navigate, overlay, scroll, variant)", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(18, 285, "                      +  transition (instant, dissolve, slide, push, Smart animate) with a duration and an easing curve", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="6.5" caption="A six-panel storyboard of the Sita example from Section 6.4, drawn as the team would draw it: context, trigger, interaction, interaction, feedback, outcome. A storyboard shows the person and place around the screens. Panel 1 puts Sita on a bus with a poor signal, which is why the design needs offline autosave (panel 3). Stick figures are enough: the aim is shared understanding, not art."
f = Fig(580, 330)
caps = ["1 Context: on the bus, sees the notice", "2 Trigger: forms close tonight", "3 Interaction: app autosaved her form",
        "4 Interaction: pays in two taps", "5 Feedback: receipt and SMS", "6 Outcome: relieved, phone away"]
def person(x, y, mood="ok"):
    f.circle(x, y, 7, fill="#ffffff", stroke=SLATE, sw=1.6)
    f.line(x, y + 7, x, y + 30, color=SLATE, sw=1.8)
    f.line(x, y + 14, x - 10, y + 24, color=SLATE, sw=1.8)
    f.line(x, y + 14, x + 10, y + 24, color=SLATE, sw=1.8)
    f.line(x, y + 30, x - 8, y + 44, color=SLATE, sw=1.8)
    f.line(x, y + 30, x + 8, y + 44, color=SLATE, sw=1.8)
    if mood == "ok":
        f.raw('<path d="M %d %d q 3 3 6 0" fill="none" stroke="#334155" stroke-width="1.2"/>' % (x - 3, y + 2))
    else:
        f.raw('<path d="M %d %d q 3 -3 6 0" fill="none" stroke="#334155" stroke-width="1.2"/>' % (x - 3, y + 4))
def phone(x, y, col="#ffffff", txt=""):
    f.box(x, y, 36, 44, txt, fill=col, stroke=NAVY, r=4, sw=1.4, size=9.5, color=NAVY, bold=True)
for i in range(6):
    px = 10 + (i % 3) * 190
    py = 8 + (i // 3) * 160
    f.box(px, py, 180, 110, "", fill="#ffffff", stroke="#94a3b8", r=4, sw=1.4)
    f.text(px + 90, py + 126, caps[i], size=9.5, color=NAVY, bold=True)
    if i == 0:
        f.box(px + 10, py + 50, 100, 40, "", fill=BLUE, stroke=NAVY, r=4)
        f.circle(px + 32, py + 92, 8, fill=SLATE, stroke=SLATE); f.circle(px + 88, py + 92, 8, fill=SLATE, stroke=SLATE)
        person(px + 60, py + 22)
        f.box(px + 120, py + 14, 52, 38, "Exam forms\nclose today", fill=SAND, stroke=AMBER, size=8.5, color=AMBER, bold=True, r=3)
    elif i == 1:
        person(px + 60, py + 40, "sad")
        f.box(px + 90, py + 10, 80, 38, "Deadline\ntonight!", fill=SAND, stroke=AMBER, size=10, color=RED, bold=True, r=14)
    elif i == 2:
        person(px + 50, py + 40)
        phone(px + 96, py + 30, MINT, "Saved")
        f.text(px + 138, py + 54, "yesterday", size=9, color=TEAL, bold=True, anchor="start")
    elif i == 3:
        person(px + 50, py + 40)
        phone(px + 92, py + 30, "#ffffff", "Pay")
        f.text(px + 138, py + 46, "tap 1: Pay", size=9, color=NAVY, bold=True, anchor="start")
        f.text(px + 138, py + 62, "tap 2: OK", size=9, color=NAVY, bold=True, anchor="start")
    elif i == 4:
        phone(px + 26, py + 30, MINT, "OK")
        f.circle(px + 106, py + 54, 16, fill=MINT, stroke=TEAL, sw=2.2, label="ok", size=10)
        f.box(px + 130, py + 30, 44, 30, "SMS", fill=BLUE, stroke=NAVY, size=10, bold=True, r=4)
    else:
        person(px + 80, py + 40)
        f.text(px + 80, py + 14, "done", size=11, color=TEAL, bold=True)
f.text(290, 322, "persona + setting + trigger + 4 to 8 steps + outcome", size=10, color=SLATE, bold=True)
```

```svgfig label="6.6" caption="Easing curves computed from the CSS cubic-bezier functions over a 300 ms transition (progress against time). At half time (150 ms) linear motion has covered 50 percent of the distance, ease-out 68.5 percent, ease-in 31.5 percent and ease-in-out 50 percent. A 300 ms transition at 60 frames per second is 18 frames of 16.7 ms each, and 100 ms is only 6 frames. Use ease-out for things that enter, ease-in for things that leave and ease-in-out for moves between two points."
f = Fig(580, 270)
def bez(p1x, p1y, p2x, p2y):
    def X(t): return 3 * (1 - t) ** 2 * t * p1x + 3 * (1 - t) * t * t * p2x + t ** 3
    def Y(t): return 3 * (1 - t) ** 2 * t * p1y + 3 * (1 - t) * t * t * p2y + t ** 3
    def at(x):
        lo, hi = 0.0, 1.0
        for _ in range(50):
            m = (lo + hi) / 2
            if X(m) < x: lo = m
            else: hi = m
        return Y((lo + hi) / 2)
    return at
L, T, W, H = 56, 20, 280, 200
f.box(L, T, W, H, "", fill="#ffffff", stroke="#94a3b8", r=2, sw=1.2)
for k in range(1, 4):
    f.line(L + W * k / 4, T, L + W * k / 4, T + H, color="#e2e8f0", sw=1)
    f.line(L, T + H * k / 4, L + W, T + H * k / 4, color="#e2e8f0", sw=1)
for k, lab in enumerate(["0", "75", "150", "225", "300"]):
    f.text(L + W * k / 4, T + H + 14, lab, size=9.5, color=SLATE)
f.text(L + W / 2, T + H + 30, "time (ms)", size=10, color=SLATE, bold=True)
for k, lab in enumerate(["100%", "75%", "50%", "25%", "0%"]):
    f.text(L - 6, T + H * k / 4, lab, size=9.5, color=SLATE, anchor="end", vmid=True)
curves = [("linear", None, SLATE), ("ease-out", (0, 0, .58, 1), TEAL), ("ease-in", (.42, 0, 1, 1), RED), ("ease-in-out", (.42, 0, .58, 1), NAVY)]
for n, p, c in curves:
    fn = (lambda x: x) if p is None else bez(*p)
    pts = " ".join("%.1f,%.1f" % (L + W * i / 60.0, T + H - H * fn(i / 60.0)) for i in range(61))
    f.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (pts, c))
f.line(L + W / 2, T, L + W / 2, T + H, color=AMBER, sw=1.3, dash=True)
rows = [("Use", "Duration", "Easing"), ("Button press", "100-150 ms", "ease-out"), ("Menu opens", "150-200 ms", "ease-out"), ("Screen change", "250-300 ms", "ease-in-out"),
        ("Dialog closes", "~200 ms", "ease-in"), ("Spinner", "loops", "linear")]
for i, (a, b, c) in enumerate(rows):
    y = 36 + i * 24
    bold = i == 0
    f.text(360, y, a, size=10, color=NAVY, bold=True, anchor="start")
    f.text(458, y, b, size=10, color=SLATE, bold=bold, anchor="start")
    f.text(524, y, c, size=9.5, color=SLATE, bold=bold, anchor="start")
for i, (n, p, c) in enumerate(curves):
    f.line(360, 190 + i * 16, 384, 190 + i * 16, color=c, sw=3)
    f.text(392, 190 + i * 16, n, size=10, color=c, bold=True, anchor="start", vmid=True)
f.text(476, 190, "150 ms:", size=10, color=SLATE, bold=True, anchor="start", vmid=True)
for i, v in enumerate(["50%", "68.5%", "31.5%", "50%"]):
    f.text(526, 190 + i * 16, v, size=10, color=SLATE, anchor="start", vmid=True)
```

### 6.7.1 Eight advantages of prototyping before building, with Nepali examples

1. **Cheap mistakes.** A change on paper takes minutes, while the same change in finished code can take days (Fig. 6.1). A student team building a college fee app can redraw the payment screen ten times before a developer writes a single line. The money saved goes into features that users actually need.
2. **Early user feedback.** A paper prototype (Plate 6.1b) lets real users tap, hesitate and speak aloud while the facilitator swaps sheets. Three to five users usually reveal the biggest problems. An eSewa-style wallet team can find in one afternoon that people look for "Send money" and not "Transfer".
3. **A shared picture for the team.** Words such as "a simple home page" mean different things to different people. A wireframe (Fig. 6.2) fixes the structure, the priority and the primary action in a form that designers, developers and the client all read in the same way. Meetings become shorter because everybody points at the same drawing.
4. **Focus on function before beauty.** Grey boxes stop people arguing about colours and make them argue about content and flow (Fig. 6.3). A Nagarik App style service portal first needs the right steps for a citizenship certificate request. The style comes later, in the mock-up.
5. **Stakeholder buy-in.** A clickable prototype (Fig. 6.4) is easy for a principal or a bank manager to understand, because they can use it on a phone. A Tribhuvan University EMIS style result screen can be shown to the campus chief in a week. Agreement comes early, and late changes of mind become rarer.
6. **Problems found in context.** A storyboard (Fig. 6.5) puts the user on a bus, in a field or in a shop, where the real problems appear. A farmer checking prices with a weak mobile signal needs offline data and a Nepali interface. These needs never show up if you draw only the screens.
7. **Better hand-off to developers.** A finished prototype with named layers, components and styles gives developers exact sizes, colours and behaviours. It removes guesswork and rework. A ConnectIPS style form with its error states already shown is much faster to code than a form described in a long document.
8. **Better motion and feel.** A prototype lets you test timing and easing on a real phone (Fig. 6.6) and decide whether a screen change feels quick or sluggish. A 300 ms ease-out slide feels natural, while a 700 ms fade feels slow on a cheap phone. Testing early also lets you check reduced-motion settings for users who get dizzy.

## Formula and fact sheet

- Ladder: sketch → wireframe (structure, no style) → mock-up (static visual) → prototype (interactive) → product.
- Low-fi = quick, cheap, concept and flow; high-fi = realistic, visual and detail testing.
- Prototype triggers: tap, drag, hover, key, after-delay; actions: navigate, overlay, scroll, change variant.
- Storyboard: persona + context + trigger + 4–8 steps + outcome.
- Motion: 100–200 ms micro, 200–300 ms small, 300–500 ms large; ease-out entering, ease-in leaving; respect reduce-motion; 60 fps = 16.7 ms.

## Chapter summary

- Wireframes show structure and priority without style; mock-ups add the visual design; prototypes make them interactive so they can be tested.
- Low-fidelity prototypes (paper, grey boxes) test concepts early and cheaply; high-fidelity ones test visuals and detailed interaction late.
- Prototyping tools such as Figma link frames with triggers, actions and transitions; software prototypes may be throwaway or evolutionary.
- Storyboards tell the user's story in context and reveal needs that screens alone hide.
- Animation should orient, give feedback and focus attention, with sensible duration and easing and respect for accessibility.

## Practice

1. Differentiate between a wireframe, a mock-up and a prototype.
2. Compare low-fidelity and high-fidelity prototyping with advantages and risks.
3. Draw a low-fidelity wireframe of a mobile "attendance" app's home screen and annotate three elements.
4. What are the elements of a good wireframe? Describe the wireframing process.
5. Explain paper prototyping and the "Wizard of Oz" technique.
6. Create a six-panel storyboard for a farmer checking market prices on a phone.
7. List five purposes of animation in a prototype with an example each.
8. What duration and easing would you use for (a) a button press, (b) a screen transition, (c) a closing dialog? Why?
9. List the steps for building a simple clickable prototype in Figma.
10. Explain throwaway and evolutionary prototypes and one risk of prototyping.

::: note Answers and worked solutions
**1.** Wireframe: structure/layout without visual style; mock-up: static high-fidelity visual design; prototype: interactive simulation that can be clicked and tested.
**2.** Low-fi: fast, cheap, encourages structural feedback, but less realistic; high-fi: realistic, good for visual/interaction testing and demos, but costly, slow to change and invites comments on colours.
**3.** A header "Attendance" with the date, a list of classes (cards) each with a status chip and a "Mark" button, a bottom tab bar (Home, History, Profile). Annotations: card tap → class detail; Mark → marks present and shows a snackbar; empty state → "No classes today".
**4.** Elements: purpose and primary action, content blocks and hierarchy, navigation, forms and buttons, states, annotations, flow. Process: review research, list screens, sketch, choose grid, build, annotate, review, test, revise.
**5.** Paper screens are swapped by a facilitator in response to taps. In "Wizard of Oz" a person secretly plays the system (e.g. voice or smart responses) to test a concept without building it.
**6.** Panels: farmer at the field; wonders about today's price; opens the app (Nepali interface); selects the crop; sees today's market prices and trend; decides where to sell and smiles.
**7.** Orientation (slide-in), feedback (button press), status (spinner), focus (shake on error), continuity (shared-element expand), delight (celebration).
**8.** (a) 100–150 ms, ease-out (instant feedback); (b) 250–300 ms, ease-in-out or ease-out (clear but quick); (c) ~200 ms, ease-in (leaving elements accelerate away).
**9.** Set up frame and grid → styles → components → design frames → prototype mode and connections → overlays/variants/delay → set start and preview → test → share and hand off.
**10.** Throwaway: built to learn and then discarded; evolutionary: refined into the final product. Risk: a prototype mistaken for a finished product, or the team becoming attached to it and skipping redesign.
:::

## Model answers for Unit 6

**Q1. Differentiate between a wireframe, a mock-up and a prototype, and describe the process of creating wireframes. (10 marks)**

**Introduction.** Design moves from rough ideas to a working product in stages, and each stage has its own artefact. A **sketch** explores ideas, a **wireframe** fixes structure, a **mock-up** fixes appearance and a **prototype** fixes behaviour (Fig. 6.1). The rule behind this order is that the earlier the stage, the cheaper the change.

**Comparison.**

| Point | Wireframe | Mock-up | Prototype |
|---|---|---|---|
| What it shows | structure, content blocks, priority, flow | final colours, type, images, spacing | how screens connect and respond |
| Look | grey boxes, no style (Fig. 6.2) | fully styled, high fidelity (Fig. 6.3c) | low to high fidelity |
| Interaction | none, or simple links | none, it is static | clicks, transitions, overlays (Fig. 6.4) |
| Main question | is the layout right? | does it look right? | does it work for people? |
| Tools | paper, Balsamiq, Figma | Figma, XD, Sketch | Figma, paper, code |
| Typical use | agree content and flow | visual sign-off and hand-off | usability testing |

**What a wireframe must specify.** A good wireframe states the purpose of the page and its one **primary action**; the content blocks in priority order; the navigation (global, local, breadcrumbs); every form field and button; the important states (empty, error, loading); numbered **annotations** for behaviour; and the link to the next screen. Several wireframes joined by arrows form a **screen flow**.

**Process of wireframing.**

1. Review the personas, journey map, requirements and site map.
2. List the screens (screen inventory) and the task flow of each key task.
3. Sketch each screen quickly, for example with Crazy 8s.
4. Choose a grid and a device, and design the smallest screen first.
5. Build the wireframes digitally with real content where possible.
6. Annotate and number the notes (Fig. 6.2, notes 1 to 5).
7. Review with stakeholders and developers, test a clickable version with three to five users and revise.

**Fidelity levels.** Low-fidelity wireframes are hand-sketched and show flow only; mid-fidelity ones are digital, on a grid, with real labels; high-fidelity wireframes use real content and exact spacing but almost no colour.

**Worked example.** The login screen of a college app is drawn at 360 px width: a logo, the heading "Welcome back", an email field, a password field with a show toggle, one full-width Log in button, a "Forgot password?" link and "Create account" at the bottom. Note 4 says the button stays disabled until both fields are valid, and note 5 says that a wrong password shows an inline error without reloading the page.

**Conclusion.** The wireframe settles structure, the mock-up settles style and the prototype settles behaviour. Doing them in this order means expensive visual work is never wasted on a flawed layout.

**Q2. Compare low-fidelity and high-fidelity prototyping with advantages and risks. (5 marks)**

A **prototype** is an early, simplified, interactive simulation of a product, built to learn before the real build. Its fidelity is how close it is to the final product in look and behaviour (Fig. 6.3).

| Point | Low fidelity | High fidelity |
|---|---|---|
| Appearance | paper, grey boxes, simple clickable wireframes | final colours, type, images and animation |
| Interaction | manual, a person plays the computer, or basic links | realistic taps, transitions, form behaviour |
| Time and cost | minutes to hours, very cheap | hours to days, more costly |
| Best for | early concept, structure and flow | late visual and detailed interaction checks, demos |
| Feedback | about flow, labels and ideas | about visuals, timing and fine usability |
| Risk | users find it hard to imagine the real product | people comment on colours, and the team gets attached |

**Advantages.** Low-fidelity prototypes invite honest criticism because they look unfinished, and they can be thrown away without regret. High-fidelity prototypes feel real, so test users behave naturally, and they give developers a clear target. **Risks.** A rough prototype may be misunderstood, while a polished one costs time, hides structural problems under good looks and may be mistaken for the finished product. **Practical rule.** Start low, test, then move up; a Nepali college fee app might use a paper prototype in week one and a clickable Figma prototype in week three.

**Q3. Explain paper prototyping and the Wizard of Oz technique. (5 marks)**

**Paper prototyping** means drawing each screen of an interface on paper or cards and testing it with users before any software exists (Plate 6.1b). A **facilitator** acts as the computer: when the user taps a paper button, the facilitator swaps in the next sheet, adds a sticky note for a pop-up or writes a typed entry on a card. A **note-taker** records where the user hesitates, and often a second person watches.

**How a session runs.**

1. Prepare the sheets for one task, such as paying the exam fee, and the likely wrong paths.
2. Give the user a realistic task, not instructions for the buttons.
3. Ask the user to think aloud while tapping with a finger or a pencil.
4. Swap the sheets without helping; silence tells you where the design fails.
5. Redraw the weak screens immediately and test again with the next user.

**Advantages.** It needs only paper and pens, can be changed in minutes, lets non-designers join in and focuses the talk on structure and wording. **Limits.** It cannot test speed, animation or real data well.

**Wizard of Oz.** In this technique a person secretly plays the intelligent part of the system. For a voice assistant or a smart chatbot, a hidden team member types or speaks the replies while the user believes the machine is answering. The team learns what people would really ask and which replies work before spending money on speech recognition or machine learning.

**Q4. Explain the steps of creating a simple clickable prototype in a tool such as Figma, and the elements that make it interactive. (10 marks)**

**Introduction.** A **clickable prototype** links finished or rough frames so that a user can tap through a flow, such as Home to Product to Checkout, and feel it before it is built (Fig. 6.4). Tools such as Figma, Adobe XD and Sketch with plug-ins support this, and Figma is the most common free choice.

**Elements that make a prototype interactive.**

| Element | Meaning | Example |
|---|---|---|
| Hotspot or trigger | the event that starts a response | tap, drag, hover, key press, after delay |
| Action | what happens | navigate to a frame, open an overlay, scroll, change a variant |
| Transition | how the next screen arrives | instant, dissolve, slide, push, Smart animate |
| Overlay | a layer above the frame | modal, bottom sheet, drawer |
| Variant or state | a component in another state | button default, hover, pressed, disabled |
| Variable and logic | stored values and conditions | show an error if the field is empty |

**Steps.**

1. **Set up** a file, choose a device frame such as 360 by 800 px, add a layout grid and an 8 px spacing rule.
2. **Define styles** for colour (primary, neutrals, semantic), text (H1 to H3, body, caption) and shadows.
3. **Build components** once (button, text field, card, app bar, tab bar) and use auto layout so they resize with their content.
4. **Design the frames** from the wireframes using the components, and name the layers clearly.
5. **Switch to prototype mode** and draw connections: Buy now to Checkout (On tap, Navigate to, Smart animate, 300 ms, ease-out), Back to the previous frame, tab-bar icons to their frames.
6. **Add an overlay** such as a size picker with Open overlay and Close overlay, a pressed-state variant and an After delay trigger for a splash screen.
7. **Set the start frame** and run the prototype on a phone or in the browser.
8. **Test** with a colleague who thinks aloud while buying the blue shirt; note where they hesitate, fix and test again.
9. **Share** a link with comment access and **hand off** through the inspect panel (spacing, colours, text styles and exported assets).

**Good practice.** Prototype one key task and not the whole app; mark the start frame; keep names clear; and remember that a prototype is a throwaway for learning, not production code.

**Conclusion.** A clickable prototype turns static pictures into an experience that can be tested. Because it is built from reusable components and clear connections, it can be changed in minutes and handed to developers with exact measurements.

**Q5. What is a UX storyboard? Draw and explain a six-panel storyboard for a student paying an exam fee. (5 marks)**

A **storyboard** is a sequence of drawn panels, like a comic strip, that shows a person in a real setting using the product to reach a goal (Plate 6.1d, Fig. 6.5). It adds the human story and the surroundings that screens alone cannot show. A storyboard contains a **persona**, a **setting**, a **trigger** (the problem), **four to eight steps** of interaction, a **resolution** and short captions.

**Six panels for Sita.**

1. **Context:** Sita sits on the college bus and sees a notice that exam forms close tonight.
2. **Trigger:** she worries that she cannot reach the college computer before the deadline.
3. **Interaction:** she opens the college app, which saved her partly filled form yesterday.
4. **Interaction:** she pays with a wallet in two taps.
5. **Feedback:** a green confirmation, a receipt and an SMS arrive.
6. **Outcome:** she is relieved and puts the phone away.

**What the story reveals.** The bus and the weak signal show that the design needs **offline autosave** and a short, cheap form, which would never appear if only the payment screen were drawn. **Uses.** Storyboards communicate a concept, justify features, expose missing steps and edge cases, and align the team. There are scenario storyboards (the whole story), screen storyboards (the sequence of screens) and video prototypes.

**Q6. Explain the purposes of animation in prototypes, and choose duration and easing for common interface actions. (5 marks)**

**Motion** should explain a change, give feedback, direct attention or add character, and never exist only for decoration.

| Purpose | Example |
|---|---|
| Orientation | a new screen slides in from the right, so Back is clearly to the left |
| Feedback | a button depresses, a heart pulses after a like |
| Status | a spinner or skeleton screen while content loads |
| Focus | a field shakes when invalid, a new item is highlighted |
| Continuity | a thumbnail expands into the detail page (shared-element transition) |
| Delight | a small celebration after the task is finished |

**Duration and easing (Fig. 6.6).** Micro-interactions last 100 to 200 ms; small transitions 200 to 300 ms; full-screen transitions 300 to 500 ms; anything above 500 ms feels slow. Use **ease-out** for items that enter, **ease-in** for items that leave, **ease-in-out** for a move between two points and **linear** only for loops such as spinners. At 60 frames per second one frame lasts 16.7 ms, so 300 ms is 18 frames.

**Choices.** (a) A button press: 100 to 150 ms, ease-out, because feedback must feel instant. (b) A screen change: 250 to 300 ms, ease-in-out or ease-out, clear but quick. (c) A closing dialog: about 200 ms, ease-in, because leaving items accelerate away.

**Accessibility and performance.** Respect the reduce-motion setting, avoid flashing more than three times per second, never carry information by animation alone, and animate only `transform` and `opacity` to keep 60 frames per second on cheap phones.

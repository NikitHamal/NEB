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

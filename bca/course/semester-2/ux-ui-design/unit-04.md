---
subject: UX/UI Design
grade: BCA Semester 2
unit: 4
title: UI Components
area: BCA 155 · UX/UI Design · Unit 4
hours: 12
---

Interfaces are built from a small vocabulary of components: menus, windows and screen controls. This is the largest unit, because getting these basic parts right is most of everyday interface design. We cover the menu system, window types and presentation, the full range of controls and how to choose the right control for a task, and how to design icons, graphics and images.

::: key What this unit gives you
- System menus and their functions; formatting of menus (consistency, presentation, organisation, complexity, ordering, grouping).
- Types of menus: menu bar, pull-down, cascading, pop-up, tear-off, iconic.
- Windows: components, presentation styles (tiled, overlapping, cascading) and types (primary, secondary, dialog boxes).
- Screen-based controls: operable, text entry, selection, and other controls.
- Choosing the proper control for a task; icons, graphics and images.
:::

## 4.1 Menus

A **menu** presents a list of options (commands, settings, destinations) from which the user chooses. It lets the user **recognise rather than recall** commands. **Functions of menus**: navigation (move through the system), execution of commands, selection of options (toggle settings), and the display of available actions in context.

### Formatting menus

| Aspect | Guidelines |
|---|---|
| **Consistency** | same wording, order, location, shortcuts and look in every menu and screen; platform conventions (File, Edit, View, … Help) |
| **Display and presentation** | show items clearly; use **mixed-case** text (easier to read than ALL CAPS); distinguish unavailable items by greying out (and keep them visible); indicate submenus with an arrow › and shortcuts with the key combination; show the current selection with a tick or highlight; allow keyboard access (underlined mnemonic letter, e.g. **F**ile = Alt-F) |
| **Organisation** | arrange by task, by function or by user workflow; follow users' mental model (card-sort to find it) |
| **Complexity** | prefer **broad and shallow** to narrow and deep: 4–8 items per menu, at most 2–3 levels; long hierarchies slow users and cause errors (Hick's law, and hierarchy costs navigation) |
| **Item arrangement and ordering** | order by **convention** (File, Edit, View…), **frequency** (most used at the top), **importance**, **sequence** (steps of a process), **alphabetical** (for long lists of names), or **size/time**; never random; put destructive items (Delete, Exit) away from frequent ones |
| **Grouping** | cluster related items with separator lines or spacing — 3–5 items per group; give groups a clear label; place related groups together |
| **Naming** | short, meaningful verbs or nouns; the same word for the same thing; the most important word first; no ambiguity (Save vs Save As) |

### Types of menus

| Type | Description | Typical use | Notes |
|---|---|---|---|
| **Menu bar** | a horizontal strip of top-level titles at the top of the window or screen | the main command set of desktop applications | always visible; follows convention; the top edge is a Fitts's-law bonus |
| **Pull-down (drop-down) menu** | list that drops from a menu-bar title when clicked | commands of one category | closes after selection; supports keyboard mnemonics |
| **Cascading (hierarchical) menu** | a submenu opening to the side of an item with an arrow | sub-options (e.g. *Open Recent ›*) | needs steady pointer movement; limit to 2 levels; allow a short delay before closing |
| **Pop-up (context) menu** | appears at the pointer on right-click or long-press | actions for the selected object | context-specific, saves travel; not discoverable alone — duplicate important commands elsewhere |
| **Tear-off menu** | can be dragged off to become a floating window | frequently used palettes (tool options) | cuts repeated travel; rare today |
| **Iconic menu** | items are icons (toolbars, ribbon, dock, bottom tab bar) | frequently used actions; limited space | add tooltips and labels for unfamiliar icons |

Modern web and mobile patterns: **hamburger menu** (three stacked lines) hiding navigation (saves space but lowers discoverability — measured to reduce use of hidden items), **tab bar** (3–5 destinations always visible at the bottom on phones), **navigation drawer**, **mega-menu** (a large panel with grouped links on content-heavy sites), **kebab/overflow menu** (three vertical dots for extra actions) and **breadcrumbs**.

## 4.2 Windows

A **window** is a separate, bounded area of the screen showing one view of the system's content.

### Components of a window

**Title bar** (name; drag handle; window buttons — minimise, maximise/restore, close), **menu bar**, **toolbar**, **status bar** (feedback), **client (work) area**, **scroll bars**, **resize border/handle**, **window frame** and often **tabs**. Good window design uses a descriptive title, a consistent layout, visible controls and does not hide the close button.

### Window presentation styles

| Style | Description | Pros | Cons |
|---|---|---|---|
| **Tiled windows** | windows are arranged side by side, edge to edge, with no overlap | every window is fully visible; no window management; no lost windows; uses the screen fully | each window is small; resizing one changes the others; not good for many windows |
| **Overlapping windows** | windows may lie on top of each other like papers on a desk (the usual desktop) | familiar desk metaphor; larger windows; flexible; depth shows focus | windows can hide each other; time spent arranging and finding; visual clutter |
| **Cascading windows** | a variant of overlapping where each new window is placed slightly down and right of the previous, so every title bar is visible | automatic placement; easy to pick a window by its title | top windows hide most of the others; stacks quickly clutter the screen |

Other: **split panes** (two resizable areas in one window), **tabs** (many views in one window — the web standard), **virtual desktops/workspaces**, **full-screen** and **picture-in-picture**.

### Types of windows

| Type | Purpose | Behaviour |
|---|---|---|
| **Primary window** | the main window of an application; shows the main content and workspace; appears when launching the application | one per application (or document) with the full set of controls; closing it exits the application |
| **Secondary window** | supports the primary window: extra info, properties, tool palettes, help | dependent on the primary window; closes or minimises with it; may stay open |
| **Dialog box** | a short, focused exchange: asks for information, confirms an action or reports a message | usually small; may be **modal** or **modeless** |

**Modal dialog** blocks the parent until answered (use for decisions that must happen now: "Discard unsaved changes?"). **Modeless dialog** lets the user continue working (Find and Replace, palettes). Types of dialog: **message/alert**, **confirmation**, **input/property/settings**, **file open/save**, **wizards** (step-by-step with Next/Back), **tool dialogs**.

Dialog design: clear title; plain language; one main question; clearly labelled buttons that name the action (**Save / Don't save / Cancel**, not OK/Cancel when ambiguous); the safe action is the default; the primary button on the right (Windows) or follows platform rule; Escape cancels; Enter confirms; never use modal dialogs for non-urgent information — use **toasts/snackbars** or inline messages. On mobile: **bottom sheets** and **alerts** replace dialogs.

## 4.3 Screen-based controls

Controls (widgets) are the objects through which users give input and get output. Grouped by what the user does:

### Operable controls (cause an action)

| Control | Use | Guidelines |
|---|---|---|
| **Button (command/push button)** | trigger an action | label with a verb ("Submit", "Pay now"); **primary** (filled), **secondary** (outlined), **tertiary** (text); show states: default, hover, pressed, focused, disabled, loading; min size 44 px; one primary per screen; do not hide with only an icon unless universally known |
| **Default button** | the action triggered by Enter | the safe/likely action |
| **Toolbar** | a row of icon buttons for frequent commands | group by function; tooltips; allow customisation; same order across screens |
| **Link** | navigate | underlined or distinct colour; descriptive text (not "click here"); visited state |
| **Toggle / switch** | immediate on/off setting | takes effect instantly (not requiring Save); label states clearly |
| **Floating action button (FAB)** | the single primary action of a mobile screen | one per screen; reachable by thumb |
| **Spinner, progress bar** | show status | determinate when the length is known |

### Text entry and read-only controls

| Control | Use | Guidelines |
|---|---|---|
| **Single-line text box** | short free-text (name, email, search) | label above or beside (not only placeholder text — it vanishes and fails accessibility); size reflects expected length; use input types (email, tel, number) so mobile shows the right keyboard; show format hints; validate **inline** after leaving the field |
| **Multi-line text box (text area)** | long text (message, address) | resizable; character counter if limited |
| **Password field** | secret | mask with a "show password" toggle; allow paste for password managers |
| **Combo box / autocomplete** | type or pick | suggestions as the user types; good for long lists |
| **Spin box (stepper)** | numeric within a range | for small ranges; allow typing |
| **Read-only controls (labels, display fields, text blocks)** | show information | style differently from editable text; selectable to copy |

### Selection controls

| Control | Selection | Use |
|---|---|---|
| **Radio buttons** | **one** from a **small** set (2–6) of mutually exclusive options, all visible | a choice that must be seen and compared (delivery speed); preselect a sensible default; vertical list |
| **Check boxes** | **zero or more** from a set; each independent | options and consent ("Remember me"); label states the "on" meaning; a single check box = a yes/no flag |
| **List box** | one or several from a visible list (5–8 items visible) | longer lists where items should remain visible; allow multi-select with Ctrl/Shift |
| **Drop-down list (select)** | one from a list that is hidden until opened | long lists (country, district) to save space; sort sensibly; avoid for fewer than ~4 options (use radio buttons) |
| **Segmented control / toggle group** | one of 2–5 related options | switch view (Day / Week / Month) |
| **Chips/tags** | multi-select or filters | filter bars |

### Other controls

| Control | Use | Guidelines |
|---|---|---|
| **Slider** | choose a value in a continuous range where precision is not vital | show the value; min/max labels; large thumb; accompany with a number input if precision matters |
| **Tabs** | switch between related views of one object | few (≤ 7) tabs, labels short, current tab clearly marked; not for sequential steps |
| **Date picker** | choose a date | calendar for near dates; typing for far dates (date of birth); support the BS calendar for Nepal; show format |
| **Time picker** | choose a time | clock or spinner; 12/24-hour format |
| **Scroll bar** | move through content larger than the view | visible indication of position; keyboard support; avoid horizontal scroll |
| **Accordion / expander** | collapse and expand sections | progressive disclosure of details |
| **Stepper/progress indicator** | where the user is in a multi-step process | "Step 2 of 4" |
| **Tooltip** | short help on hover/focus | not for essential information (no hover on touch) |
| **Carousel** | rotating content | slow, users miss content; avoid for important content |
| **Pagination / infinite scroll** | split long lists | pagination for goal-directed finding; infinite scroll for browsing |
| **Table / data grid** | compare structured data | sortable headers, aligned numbers, zebra rows, sticky header |
| **Snackbar/toast/banner** | short non-blocking message | auto-dismiss only for non-critical messages |

### Selecting the proper control

| Task | Best control |
|---|---|
| Choose exactly one of 2–6 options | **radio buttons** (or a toggle for on/off) |
| Choose exactly one from many (> 6) | **drop-down list** (or autocomplete for very long lists) |
| Choose any number of options | **check boxes** (list box with multi-select if long) |
| Turn a setting on/off immediately | **switch** |
| Agree to terms (a single yes/no on submit) | **check box** |
| Enter free short text | **single-line text box** |
| Enter long text | **text area** |
| Enter a number in a small range | **spin box / slider** (slider if approximate) |
| Enter a number precisely | **text box** with validation |
| Choose a date | **date picker** (typed field for birthdates) |
| Switch between views | **tabs** or **segmented control** |
| Trigger an action | **button** |
| Navigate | **link** or **menu** |
| Show status | **progress bar / spinner / status text** |

Principles: use **standard controls** in the usual way; **label** every control clearly; **group** related controls (fieldsets, panels) with headings; align labels and fields; **tab order** follows the visual order; give **feedback** after use; show **disabled** states; validate input and describe errors beside the field with a fix; keep forms short, single-column, and mark optional rather than required fields where possible.

## 4.4 Graphics, icons and images

### Meaningful graphics
Graphics must **communicate**, not decorate. Use pictures where they speed understanding (maps, charts, product photos), keep them consistent in style, ensure legibility at the displayed size, provide **text alternatives** (alt text) and avoid cultural misunderstandings. Remove **chartjunk**; label axes; choose the right chart (line for trends, bar for comparison, pie for a few parts of a whole).

### Icons

An **icon** is a small pictorial symbol representing an object or action. Types (by Rogers): **resemblance** (looks like it: a printer), **exemplar** (typical example: a knife and fork for a restaurant), **symbolic** (a higher-level concept: a cracked glass for fragile), **arbitrary** (learned association: the radiation sign). Guidelines:

- **Familiar and distinguishable**: use standard icons (magnifier = search, trash = delete, gear = settings, envelope = mail).
- **Simple**: recognisable at 16–24 px; avoid fine detail; consistent stroke width, corner radius, style (outlined *or* filled, not mixed) and grid (e.g. 24 × 24 with 2 px padding).
- **Label them** (text with icon) whenever the meaning is not universal — icon-only buttons with ambiguous symbols (e.g. a "heart" vs "star") mislead.
- **Test** them with users (recognition test).
- **Avoid** culturally specific gestures, mailbox shapes (US mailbox for e-mail), or old technology (floppy disk for save is now a learned convention).
- Provide **accessible names** (aria-label) and adequate contrast and size; use vector formats (SVG).
- **Favicons and app icons**: simple, distinctive, readable at 16 px and 1024 px; follow platform shape guidelines.

### Images

Choose **real, relevant, high-quality** images; avoid generic stock photos that mean nothing. Technical rules: use **WebP/AVIF/JPEG** for photos, **PNG/SVG** for graphics; **compress**; use **responsive images** (several sizes); lazy-load; set width and height to prevent layout shift; give **alt text**; keep text outside images (so it can be read by screen readers and translated). Ensure that overlaid text keeps sufficient contrast with a scrim. Respect copyright and use properly licensed assets. Photos of people should be diverse and local when the audience is local.

## Formula and fact sheet

- Menus: 4–8 items, broad and shallow, ≤ 3 levels; group by function; order by convention/frequency/sequence; mixed case.
- Menu types: menu bar, pull-down, cascading, pop-up, tear-off, iconic.
- Window styles: tiled (no overlap), overlapping (desk), cascading (offset stack). Window types: primary, secondary, dialog (modal/modeless).
- Radio = one of few; check box = any of several; drop-down = one from many; switch = immediate on/off; slider = approximate value.
- Icons: familiar, simple, consistent, labelled, tested; four kinds — resemblance, exemplar, symbolic, arbitrary.
- Touch targets ≥ 44 px/48 dp; placeholder is not a label.

## Chapter summary

- Menus let users recognise commands; format them consistently, keep them short and well grouped, and pick the type — bar, pull-down, cascading, pop-up, tear-off, iconic — by the task.
- Windows may be tiled, overlapping or cascading; primary, secondary windows and dialog boxes serve different roles; modal dialogs should be rare.
- Controls are operable, text-entry, selection or other; choosing the proper control for the task prevents errors and speeds use.
- Icons and images must be meaningful, consistent, accessible and technically optimised.

## Practice

1. Explain the formatting rules for menus: consistency, organisation, complexity and ordering.
2. Describe six types of menus with one use each.
3. Differentiate between tiled, overlapping and cascading windows.
4. Differentiate between primary windows, secondary windows and dialog boxes; modal and modeless.
5. Choose the proper control for: (a) gender (3 options); (b) district (77 options); (c) subscribe to newsletter; (d) volume; (e) date of birth; (f) accept terms.
6. Why is placeholder text not a substitute for a label?
7. Compare radio buttons and check boxes.
8. Design a login dialog: list controls, states and error handling.
9. List the four kinds of icons with examples and five guidelines for good icons.
10. Explain the technical guidelines for web images.

::: note Answers and worked solutions
**1.** Consistent wording, order, placement and shortcuts; organise by task and users' mental model; keep complexity low (4–8 items per menu, 2–3 levels); order by convention, frequency, importance or sequence, never randomly; group related items with separators.
**2.** Menu bar (main commands), pull-down (one category), cascading (submenus), pop-up (context actions), tear-off (floating palette), iconic (toolbar, tab bar).
**3.** Tiled: windows side by side without overlap; overlapping: windows stacked like papers; cascading: overlapping windows offset diagonally so each title bar shows.
**4.** Primary window: the main application window; secondary: supporting window dependent on the primary; dialog box: focused short exchange. A modal dialog blocks the parent until closed; modeless lets the user continue.
**5.** (a) radio buttons (few exclusive options); (b) drop-down list with search/autocomplete (many); (c) check box (or switch); (d) slider; (e) typed fields or date picker with year/month dropdowns (typing is faster for far dates); (f) check box.
**6.** It disappears when typing begins (memory load), often has low contrast, is not reliably read by assistive technology, and is mistaken for a pre-filled value. Use a persistent visible label.
**7.** Radio buttons: exactly one of a few visible, mutually exclusive options; check boxes: independent on/off choices, any number.
**8.** Fields: username/email (text box, label), password (masked with show toggle), "Remember me" (check box), primary button **Log in**, link **Forgot password?**, link **Create account**. States: default, focus, error, disabled while submitting. Errors: inline beside the field, specific ("The password is wrong. 2 attempts left.") without revealing which field is wrong if security demands it; keep typed data.
**9.** Resemblance (printer), exemplar (knife and fork), symbolic (cracked glass), arbitrary (radiation sign). Guidelines: familiar, simple, consistent style, labelled, tested, accessible name.
**10.** Choose the format (WebP/AVIF/JPEG for photos, SVG/PNG for graphics), compress, serve responsive sizes, lazy-load, specify width and height, add alt text, keep text out of images, license properly.
:::

---
subject: Computer Science
grade: 8
unit: 9
title: Presentation Software
hours: 0
area: Application Software
---

In a science fair, a school assembly or a class project, you often have to
explain something to a group of people. A **presentation** — a set of slides
shown on a screen or projector while you speak — helps them follow you: the
key points, pictures, charts and short videos appear exactly when you need
them. This lesson teaches presentation software as a practical skill: making
slides with layouts, themes and placeholders; adding text, pictures, tables,
charts, sound and video; adding transitions and animations; using the slide
views and the slide master; running the show; and, most important, designing
slides that people can actually read. Commands are given for **Microsoft
PowerPoint (Microsoft 365)**, with **LibreOffice Impress** in brackets.

::: key What questions on this lesson ask
Expect: define **presentation software, slide, layout, theme, placeholder,
transition, animation, slide master**; name **examples**; list **features**;
the difference between a **transition and an animation**, and between
**Normal and Slide Sorter view**; steps to **insert a picture, chart, audio or
video**, add a **transition** to all slides, or **start the slide show** (F5);
and **rules for an effective presentation**. A practical test asks for a short
presentation on a topic such as "Tourism in Nepal".
:::

## 9.1 Presentation software: features and examples

::: definition Presentation software
**Presentation software** is application software used to create a series of
**slides** containing text, pictures, charts, sound and video, and to **show
them one after another** on a screen or through a projector to support a talk.
A file of slides is called a **presentation** (or slide deck).
:::

**Examples:** **Microsoft PowerPoint**, **LibreOffice Impress** (free and open
source), **Google Slides** (works in a browser), Apple Keynote, Canva and WPS
Presentation.

**Features of presentation software**

- ready-made **layouts** and **themes** (designs) for slides;
- **placeholders** for titles, text, pictures, tables, charts and video;
- **multimedia**: pictures, audio, video, icons, shapes and SmartArt diagrams;
- **transitions** between slides and **animations** of objects on a slide;
- several **views**: Normal, Outline, Slide Sorter, Notes Page, Reading View;
- a **slide master** that changes every slide at once;
- **speaker notes** and **Presenter View** for the speaker;
- **rehearse timings**, self-running shows and **export** to PDF or video;
- sharing and editing together online (PowerPoint for the web, Google Slides).

**Uses:** classroom teaching and student projects, school assemblies and
parents' meetings, business and NGO reports, training workshops, wedding and
birthday slide shows, and information screens in banks, hotels and hospitals.

```figure caption="The Microsoft PowerPoint window (Microsoft 365) in Normal view, drawn with its parts numbered. The slide being edited fills the middle; thumbnails of all slides run down the left; speaker notes go below the slide."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 4.4))
T = 1.75
ax.add_patch(Rectangle((0, T), 10, 6.0, fc="white", ec=INK, lw=1.0))
ax.add_patch(Rectangle((0, T + 5.55), 10, 0.45, fc="#b7472a", ec=INK, lw=0.8))
ax.text(0.2, T + 5.775, "AutoSave  ▣  ↶  ↷", ha="left", va="center", fontsize=6.6, color="white")
ax.text(4.8, T + 5.775, "Our Nepal - PowerPoint", ha="center", va="center", fontsize=7.0, color="white")
ax.text(9.15, T + 5.775, "–   □   ×", ha="center", va="center", fontsize=7.4, color="white")
tabs = ["File", "Home", "Insert", "Draw", "Design", "Transitions", "Animations", "Slide Show", "Record", "Review", "View"]
ax.set_xlim(-0.1, 10.1); ax.set_ylim(-0.05, T + 6.1)
fig.canvas.draw()
rend = fig.canvas.get_renderer(); inv = ax.transData.inverted()
x = 0.12
for t in tabs:
    txt = ax.text(x, T + 5.3, t, ha="left", va="center", fontsize=6.1, color=INK,
                  fontweight="bold" if t == "Home" else "normal", zorder=3)
    bb = txt.get_window_extent(rend)
    w = inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]
    if t == "Home":
        ax.add_patch(Rectangle((x - 0.06, T + 5.12), w + 0.12, 0.38, fc="#f3f3f3", ec=MUTED, lw=0.6, zorder=2))
    x += w + 0.1
ax.add_patch(Rectangle((0, T + 4.25), 10, 0.85, fc="#f3f3f3", ec=MUTED, lw=0.6))
ax.text(0.2, T + 4.67, "Paste    New Slide ▾   Layout ▾      Font  B I U      Paragraph  •≡  1≡      Shapes   Arrange", ha="left",
        va="center", fontsize=6.3, color=INK)
ax.add_patch(Rectangle((0, T + 0.4), 1.75, 3.85, fc="#f7f7f7", ec=MUTED, lw=0.6))
for k in range(4):
    yy = T + 3.55 - k * 0.85
    ax.text(0.15, yy + 0.3, str(k + 1), ha="left", va="center", fontsize=6.4, color=MUTED)
    ax.add_patch(Rectangle((0.38, yy), 1.2, 0.68, fc="white", ec=SERIES[1] if k == 0 else GRID, lw=1.2 if k == 0 else 0.6))
    ax.plot([0.5, 1.45], [yy + 0.48, yy + 0.48], color="#9aa1ab", lw=1.4)
    if k:
        for j in range(2):
            ax.plot([0.5, 1.2], [yy + 0.28 - j * 0.12, yy + 0.28 - j * 0.12], color="#c8ccd2", lw=1.0)
ax.add_patch(Rectangle((1.75, T + 0.4), 8.25, 3.85, fc="#e8e8e8", ec="none"))
ax.add_patch(Rectangle((2.6, T + 1.35), 6.55, 2.75, fc="white", ec=MUTED, lw=0.7))
ax.add_patch(Rectangle((3.1, T + 2.85), 5.55, 0.8, fc="none", ec="#9aa1ab", lw=0.8, ls="--"))
ax.text(5.875, T + 3.25, "Click to add title", ha="center", va="center", fontsize=9, color=MUTED)
ax.add_patch(Rectangle((3.1, T + 1.7), 5.55, 0.9, fc="none", ec="#9aa1ab", lw=0.8, ls="--"))
ax.text(5.875, T + 2.15, "Click to add subtitle", ha="center", va="center", fontsize=7.4, color=MUTED)
ax.add_patch(Rectangle((1.75, T + 0.4), 8.25, 0.75, fc="white", ec=MUTED, lw=0.6))
ax.text(1.95, T + 0.78, "Click to add notes", ha="left", va="center", fontsize=6.6, color=MUTED)
ax.add_patch(Rectangle((0, T), 10, 0.4, fc="#f3f3f3", ec=MUTED, lw=0.6))
ax.text(0.15, T + 0.2, "Slide 1 of 4    English (India)", ha="left", va="center", fontsize=6.2, color=INK)
ax.text(6.4, T + 0.2, "Notes   ▭ ▦ ▣ ▷    −──●──+  68%", ha="left", va="center", fontsize=6.2, color=INK)
def mk(x, y, n):
    ax.text(x, y, str(n), ha="center", va="center", fontsize=6.6, color="white", fontweight="bold", zorder=6,
            bbox=dict(boxstyle="circle,pad=0.22", fc=SERIES[1], ec="white", lw=0.6))
marks = [(7.75, T + 5.775, 1), (9.72, T + 5.3, 2), (9.7, T + 4.67, 3), (0.95, T + 0.7, 4), (9.45, T + 3.6, 5),
         (8.35, T + 3.25, 6), (5.5, T + 0.78, 7), (3.4, T + 0.2, 8), (6.15, T + 0.2, 9)]
for x, y, n in marks:
    mk(x, y, n)
keys = ["title bar", "ribbon tabs", "ribbon commands", "Slides pane (thumbnails)", "slide pane",
        "placeholder", "notes pane", "status bar", "view buttons and zoom"]
for n, t in enumerate(keys, 1):
    col, row = (n - 1) // 3, (n - 1) % 3
    xk, yk = 0.25 + col * 3.45, 1.3 - row * 0.45
    mk(xk, yk, n)
    ax.text(xk + 0.28, yk, t, ha="left", va="center", fontsize=6.9, color=INK)
ax.axis("off")
```

The ribbon of PowerPoint has the tabs File, Home, Insert, Draw, Design,
**Transitions**, **Animations**, **Slide Show**, Record, Review, View and Help.
New presentations use **widescreen (16:9)** slides; Design → **Slide Size**
changes this to 4:3 if a projector needs it.

```photo id="cs8/impress-window" caption="LibreOffice Impress, the free presentation program, editing a 17-slide presentation. The Slides pane on the left shows thumbnails in different layouts; the slide being edited fills the middle." width="96"
mark 0.43 0.922 "1"
mark 0.162 0.79 "2"
mark 0.89 0.775 "3"
mark 0.10 0.037 "4"
mark 0.815 0.037 "5"
mark 0.975 0.44 "6"
key 1 Menu bar: the Slide and Slide Show menus hold the slide commands
key 2 Slides pane: thumbnails of every slide; drag to change their order
key 3 Slide pane: the slide being edited
key 4 Status bar: Slide 1 of 17
key 5 Zoom slider
key 6 Sidebar: properties, transitions, animations and master slides
```

```photogrid label="9.H" cols="3" ratio="1.3" caption="From slide to screen. (a) A data projector throws the slide show on a wall or screen for a whole class. (b) The Impress window: the slide panel on the left, the slide in the middle and the tools around it. (c) A slide with a chart: a picture of numbers is understood faster than a table. Good presentation software joins the slide design, the chart and the projector into one clear talk."
@ photo id="bcagk/projector" cap="(a) Data projector: output to a screen"
@ photo id="cs8/impress-window" cap="(b) The presentation window"
@ photo id="cs8/impress-chart-slide" cap="(c) A slide with a chart"
```

## 9.2 Creating a presentation: slides, layouts, themes and placeholders

::: definition Slide, layout, theme and placeholder
A **slide** is one page of a presentation. A **layout** is the arrangement of
boxes on a slide — for example a title with a list below it. A **theme** is a
ready-made design — background, colours, fonts and effects — applied to all
the slides together. A **placeholder** is a dotted box on a slide that holds a
title, text, a picture, a table or a chart; it shows a prompt such as *Click to
add title* until you fill it.
:::

**Steps to create a presentation**

1. Open PowerPoint and click **Blank Presentation** (or **Ctrl + N**). The first
   slide has the **Title Slide** layout. (Impress: File → New → Presentation.)
2. Click in *Click to add title* and type the title; type your name and class in
   the subtitle placeholder.
3. **Home → New Slide** (**Ctrl + M**) adds a slide; the arrow on New Slide lets
   you choose its layout. **Home → Layout** changes the layout of the current
   slide. (Impress: Slide → New Slide, Ctrl + M; Slide → Layout.)
4. **Design → Themes**: click a theme for the whole presentation; **Variants**
   changes its colours, fonts and background. Microsoft 365's **Designer**
   (Design → Designer) suggests ready layouts for your content. (Impress: the
   Master Slides section of the sidebar.)
5. Fill each placeholder: type text, or click the small icons in a content
   placeholder to insert a table, chart, SmartArt, picture, icon or video.
6. Save with **Ctrl + S**: PowerPoint saves **.pptx**; Impress saves **.odp**
   (choose PowerPoint format to share with PowerPoint users).

Right-click a thumbnail in the Slides pane to **Duplicate**, **Delete** or
**Hide** a slide; drag thumbnails up or down to **reorder** slides.

```figure caption="Six common slide layouts (Home → Layout in PowerPoint; Slide → Layout in Impress). Each dashed box is a placeholder that waits for a title, text, a picture, a table or a chart."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(2, 3, figsize=(5.0, 2.25))
def ph(ax, x, y, w, h, t, fs=6.6):
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec="#8a93a0", lw=0.7, ls="--"))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=MUTED)
specs = {
    "Title Slide": [(0.1, 0.42, 0.8, 0.28, "title"), (0.2, 0.15, 0.6, 0.18, "subtitle")],
    "Title and Content": [(0.07, 0.74, 0.86, 0.17, "title"), (0.07, 0.08, 0.86, 0.6, "text, table,\nchart or picture")],
    "Two Content": [(0.07, 0.74, 0.86, 0.17, "title"), (0.07, 0.08, 0.41, 0.6, "content"), (0.52, 0.08, 0.41, 0.6, "content")],
    "Comparison": [(0.07, 0.77, 0.86, 0.15, "title"), (0.07, 0.56, 0.41, 0.16, "heading", ), (0.52, 0.56, 0.41, 0.16, "heading"),
                   (0.07, 0.06, 0.41, 0.45, "content"), (0.52, 0.06, 0.41, 0.45, "content")],
    "Title Only": [(0.07, 0.74, 0.86, 0.17, "title")],
    "Picture with Caption": [(0.07, 0.08, 0.5, 0.84, "picture"), (0.62, 0.55, 0.31, 0.3, "title"), (0.62, 0.12, 0.31, 0.36, "caption")]}
for ax, (name, boxes) in zip(axs.flat, specs.items()):
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=INK, lw=0.8))
    for b in boxes:
        ph(ax, *b[:4], b[4], fs=6.0 if len(b[4]) > 9 else 6.6)
    ax.set_title(name, fontsize=7.4, pad=3)
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02); ax.set_aspect(0.5625 * 1.0)
    ax.set_xticks([]); ax.set_yticks([]); ax.axis("off")
fig.subplots_adjust(wspace=0.12, hspace=0.32)
```

::: example Worked example 9.1 — choosing layouts
**Problem.** Ritika is making a presentation on *Tourism in Nepal*. Choose a
layout for each slide: (a) the first slide with the topic and her name; (b) a
slide with five points about trekking; (c) a slide comparing Pokhara and
Chitwan side by side, each with a heading; (d) a slide with a big photograph of
Lumbini and a short caption; (e) a slide that separates the "Problems" part of
the talk from the "Solutions" part.

**Solution.** (a) **Title Slide**. (b) **Title and Content** (a bulleted
list). (c) **Comparison** — two headings with content under each (Two Content
would do without the headings). (d) **Picture with Caption**. (e) **Section
Header** — a slide that introduces a new part.
:::

## 9.3 Inserting text, pictures, tables, charts, audio and video

| To insert | PowerPoint | Impress | Tips |
|---|---|---|---|
| Text | type in a placeholder; or **Insert → Text Box**, then drag | Insert → Text Box | keep to short points |
| Picture | **Insert → Pictures → This Device** (also Stock Images, Online Pictures) | Insert → Image | resize from a corner handle so it is not stretched |
| Table | **Insert → Table** → choose rows × columns | Insert → Table | a few rows only; large type |
| Chart | **Insert → Chart** → choose a type → type the data in the small Excel sheet that opens | Insert → Chart → edit the data table | one message per chart |
| Audio | **Insert → Audio → Audio on My PC** (or Record Audio) | Insert → Audio or Video | set how it starts on the Playback tab |
| Video | **Insert → Video → This Device** (also Stock Videos, Online Videos) | Insert → Audio or Video | short clips; test before the show |
| SmartArt, icons, shapes | Insert → SmartArt / Icons / Shapes | Insert → Shape | diagrams instead of long lists |

```photo id="cs8/impress-chart-slide" caption="A chart slide in LibreOffice Impress with the Tabbed interface. The column chart was added with Insert → Chart and its numbers typed in a small data table, as in a spreadsheet." width="96"
mark 0.735 0.956 "1"
mark 0.865 0.908 "2"
mark 0.115 0.775 "3"
mark 0.65 0.52 "4"
mark 0.085 0.022 "5"
key 1 Tabs of the Tabbed interface: Home, Insert, Layout, Slide Show, Review, View
key 2 Start from First Slide and Start from Current Slide
key 3 Slides pane with thumbnails of all twelve slides
key 4 A column chart inserted on the slide
key 5 Status bar: Slide 6 of 12
```

**Audio and video options.** Click the inserted audio or video and open the
**Playback** tab:

- **Start:** *In Click Sequence* or *When Clicked On* (plays when you click), or
  **Automatically** (plays as soon as the slide appears);
- **Play Across Slides** (keeps music playing through later slides) and
  **Loop until Stopped**;
- **Hide During Show** (for background music), **Volume**, **Trim Audio/Video**
  to cut the start or end.

::: caution Insert from the computer, and carry the files
A video or audio file that is **inserted from the computer** becomes part of the
presentation. A video **linked from the internet** (Online Videos) plays only
if the hall has internet. Before a school function, copy the presentation to a
pen drive and test it on the computer that will be used — and keep a PDF copy in
case the computer has an older program.
:::

## 9.4 Transitions and animations

::: definition Transition and animation
A **transition** is the visual effect when one **slide changes to the next**,
such as Fade, Push or Wipe. An **animation** is a movement effect given to an
**object on a slide** — a title, a bullet point, a picture — so that it appears,
moves or disappears during the show.
:::

**Adding a transition**

1. Select the slide in the Slides pane. **Transitions** tab → choose an effect
   (Fade, Push, Wipe, Split, Reveal, Cover, Morph …).
2. **Effect Options** sets its direction; **Duration** sets how long it lasts.
3. **Advance Slide:** tick *On Mouse Click*, or *After* and type a time (for a
   self-running show).
4. **Apply To All** gives the same transition to every slide.

(Impress: Slide → Slide Transition, or the Slide Transition section of the
sidebar.)

**Adding an animation**

1. Select the object (for example the text placeholder).
2. **Animations** tab → choose an effect. The four groups are colour-coded:
   - **Entrance** (green): the object appears — Appear, Fade, Fly In, Zoom;
   - **Emphasis** (yellow): it draws attention while visible — Pulse, Grow/Shrink, Spin;
   - **Exit** (red): it leaves — Disappear, Fade, Fly Out;
   - **Motion Paths**: it moves along a line, arc or custom path.
3. **Effect Options** (e.g. *From Left*, *By Paragraph*); **Add Animation** gives
   the same object a second effect.
4. **Timing** — **Start:** *On Click* (waits for a click), *With Previous* (at
   the same time as the effect before it), *After Previous* (when the effect
   before it ends); **Duration**; **Delay**.
5. **Animation Pane** lists all effects in order; drag to reorder.

(Impress: select the object → Format → Animation, or the Animation section of
the sidebar.)

| Transition | Animation |
|---|---|
| effect **between slides** | effect on **an object within a slide** |
| applied to a slide | applied to text, a picture, a chart or a shape |
| one per slide | many per slide, in an order |
| Transitions tab | Animations tab |
| e.g. Fade, Push, Wipe | e.g. Fly In, Pulse, Fly Out, Motion Path |

::: example Worked example 9.2 — a self-running information screen
**Problem.** A bank shows a 12-slide presentation on a TV in its waiting hall.
Every slide is set to **Advance Slide After 10 seconds**, and the show loops.
(a) How long does one full run take? (b) How many times does it run in an hour?
(c) Which setting makes it loop?

**Solution.** (a) 12 × 10 = **120 seconds = 2 minutes**.
(b) 60 ÷ 2 = **30 times** an hour.
(c) **Slide Show → Set Up Slide Show** → tick **Loop continuously until 'Esc'**
(and choose *Browsed at a kiosk*), so it repeats until someone presses Esc.
:::

::: example Worked example 9.3 — when does each animation play?
**Problem.** On one slide: the title has **Fade**, *On Click*, duration 0.5 s;
bullet 1 has **Fly In**, *After Previous*, 1 s; a picture has **Zoom**, *With
Previous*, 1 s, with a **delay of 0.5 s**; bullet 2 has **Fly In**, *On Click*,
1 s. Taking the first click as 0 s, when does each effect start and end? How
many clicks does the presenter need to show everything?

**Solution.** The title starts at the first click: **0 to 0.5 s**. Bullet 1
starts *after* the title ends: **0.5 to 1.5 s**. The picture starts *with*
bullet 1 (0.5 s) but waits 0.5 s: **1.0 to 2.0 s**. Bullet 2 waits for a
**second click** and then takes 1 s. So the presenter needs **2 clicks** (and a
third to move to the next slide).
:::

```figure caption="The animation timeline of Worked example 9.3. After the first click the title fades in; bullet 1 starts After Previous; the picture starts With Previous (with bullet 1) but waits 0.5 s of delay. Bullet 2 needs a second click."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.4))
items = [("Title: Fade (On Click)", 0.0, 0.5, ACCENT), ("Bullet 1: Fly In (After Previous)", 0.5, 1.0, SERIES[2]),
         ("Picture: Zoom (With Previous, delay 0.5 s)", 1.0, 1.0, SERIES[3]), ("Bullet 2: Fly In (On Click)", 3.0, 1.0, SERIES[1])]
for i, (name, s, d, c) in enumerate(items):
    y = 3 - i
    ax.barh(y, d, left=s, height=0.5, color=c, alpha=0.9)
    ax.text(s + d + 0.05, y, f"{s:g}–{s + d:g} s", va="center", fontsize=6.9, color=INK)
    ax.text(-0.1, y, name, ha="right", va="center", fontsize=6.9, color=INK)
ax.barh(1, 0.5, left=0.5, height=0.5, color=SERIES[3], alpha=0.25, hatch="///", edgecolor=SERIES[3])
for t, lab in ((0, "click 1"), (3.0, "click 2")):
    ax.axvline(t, color=MUTED, lw=0.8, ls="--")
    ax.text(t + 0.06, 3.55, lab, ha="left", va="bottom", fontsize=6.9, color=MUTED)
ax.set_xlim(-0.05, 4.6); ax.set_ylim(-0.5, 3.9)
ax.set_yticks([]); ax.set_xticks([0, 1, 2, 3, 4]); ax.tick_params(labelsize=7)
ax.set_xlabel("time in seconds (the presenter clicks again at 3 s)", fontsize=7.2)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
```

## 9.5 Slide views, the slide master and running a slide show

### Slide views

The **View** tab, and the small buttons on the status bar, switch between
views (Impress: the View menu).

| View | What it shows | Used for |
|---|---|---|
| **Normal** | one slide large, with thumbnails and the notes pane | creating and editing slides (the usual view) |
| **Outline View** | the titles and text of all slides as an outline | typing and organizing the content quickly |
| **Slide Sorter** | small thumbnails of all slides in rows | reordering, deleting, hiding slides; setting transitions |
| **Notes Page** | the slide with its speaker notes below | writing and printing notes for the speaker |
| **Reading View** | the slide show inside a window | checking the show without full screen |
| **Slide Show** | slides full-screen, one at a time | presenting to the audience |

### The slide master

::: definition Slide master
The **slide master** is the top slide in a hidden set of master slides that
stores the design of the presentation — background, fonts, colours, the
positions of placeholders and items such as a logo or footer. A change made on
the slide master appears **on every slide** that uses it.
:::

**View → Slide Master** opens it: the large thumbnail at the top is the slide
master and the smaller ones under it are its **layouts**. Change the title font,
add the school logo or a footer there, then click **Close Master View**.
(Impress: View → Master Slide; close with View → Normal.)

::: example Worked example 9.4 — why use the slide master?
**Problem.** A 20-slide presentation needs the school logo in the top right
corner of every slide, and later the title font must change from Calibri to
Arial everywhere. Compare doing this slide by slide with using the slide
master.

**Solution.** Slide by slide: the logo is inserted and positioned **20 times**,
probably not in exactly the same place, and the font is changed 20 times. With
the slide master: the logo is inserted **once** and the title font changed
**once**, and all 20 slides (and any new ones) follow it, in exactly the same
position.
:::

### Running a slide show

- **Slide Show → From Beginning** (**F5**) starts at slide 1; **From Current
  Slide** (**Shift + F5**) starts at the selected slide. (Impress: Slide Show →
  Start from First Slide, F5.)
- **Next slide or animation:** click, Space, Enter, → or N. **Previous:** ←,
  Backspace or P. Type a **slide number and press Enter** to jump to it.
- **B** makes the screen black (press again to return); **Esc** ends the show.
- **Ctrl + L** shows a laser pointer and **Ctrl + P** a pen for writing on the
  slide.
- With two screens, **Presenter View** shows the speaker the current slide, the
  next slide, the notes and a timer while the audience sees only the slide.
- **Rehearse Timings** records how long you spend on each slide, and **Hide
  Slide** keeps a slide out of the show without deleting it.

## 9.6 Designing an effective presentation

A presentation supports a speaker; it does not replace one. People cannot read
a long paragraph and listen at the same time.

```figure caption="The same slide badly and well designed. The first has a paragraph of small text, too many fonts, poor colour contrast and no picture; the second keeps one idea, five short points in large type, strong contrast and a relevant picture."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.3))
for ax in (a, b):
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.set_aspect("equal"); ax.axis("off")
a.add_patch(Rectangle((0, 0), 16, 9, fc="#2f4fa8", ec=INK, lw=0.8))
a.text(8, 8.0, "MOUNT EVEREST!!!", ha="center", va="center", fontsize=8.2, color="#e23b3b", fontweight="bold", style="italic")
para = ("Mount Everest is the highest mountain\nin the world and it is 8,848.86 metres\nhigh and it lies in Nepal in Solukhumbu\n"
        "district in Sagarmatha National Park and\nit was first climbed in 1953 by Tenzing\nNorgay Sherpa and Edmund Hillary ...")
a.text(0.6, 7.0, para, ha="left", va="top", fontsize=6.0, color="#d8473b", linespacing=1.2)
a.set_title("Poor slide", fontsize=7.8, pad=3, color=SERIES[1])
b.add_patch(Rectangle((0, 0), 16, 9, fc="white", ec=INK, lw=0.8))
b.add_patch(Rectangle((0, 7.2), 16, 1.8, fc="#1d3f72", ec="none"))
b.text(8, 8.1, "Mount Everest", ha="center", va="center", fontsize=9.5, color="white", fontweight="bold")
pts = ["8,848.86 m — highest peak", "Solukhumbu, Nepal", "Sagarmatha National Park", "First climbed in 1953", "Tenzing Norgay, Hillary"]
for k, p in enumerate(pts):
    b.text(0.7, 6.3 - k * 1.2, "•  " + p, ha="left", va="center", fontsize=6.8, color=INK)
b.add_patch(Polygon([[10.4, 1.0], [13.0, 5.6], [15.4, 1.0]], closed=True, fc="#8fa6bf", ec="#55697f"))
b.add_patch(Polygon([[12.3, 4.35], [13.0, 5.6], [13.7, 4.35]], closed=True, fc="white", ec="none"))
b.set_title("Better slide", fontsize=7.8, pad=3, color=SERIES[2])
fig.subplots_adjust(wspace=0.08)
```

**Rules for effective slides**

1. **Plan first:** know your audience, your purpose and the 3–5 main points;
   sketch the slides on paper (a storyboard).
2. **One idea per slide**, with a clear title.
3. **Keywords, not paragraphs.** A common guide is the **6 × 6 rule**: no more
   than about **six points**, each of about **six words**.
4. **Large, readable type:** titles about 36–44 pt and body text at least 24 pt
   (never below 18 pt); one or two plain fonts.
5. **Strong contrast:** dark text on a light background or light on dark; avoid
   red on blue and red on green.
6. **A consistent design:** one theme, the same colours and the same transition
   throughout.
7. **Pictures and charts** that explain; a chart is easier than a table of
   numbers. Give the source of pictures you did not make.
8. **Few animations:** use them to reveal points one by one, not to spin and
   bounce.
9. **Check** spelling, numbers and facts; add slide numbers; end with a summary
   or *Thank you / Questions?* slide.
10. **Rehearse** with a timer: about one to two minutes per slide.

::: example Worked example 9.5 — fixing a poor slide
**Problem.** The "Poor slide" in the figure above has a title in capitals with
three exclamation marks, a 64-word paragraph in red on blue at a very small
size, and no picture. List its faults and describe a better slide.

**Solution.** *Faults:* a paragraph that the audience must read instead of
listen; text far too small; red on blue has poor contrast; shouting capitals
and "!!!"; no picture. *Better slide:* title *Mount Everest*; five short points
— 8,848.86 m, highest peak; Solukhumbu, Nepal; Sagarmatha National Park; first
climbed in 1953; Tenzing Norgay and Hillary — in 24 pt or more, dark text on a
white background, with a photograph of the mountain. The speaker says the rest.
:::

::: note Activity 9.1 — a five-slide project
Make a five-slide presentation on *Our District* or *Tourism in Nepal*: a
title slide; three content slides using different layouts, with at least one
picture, one table or chart and one short audio or video clip; and a thank-you
slide. Apply one theme and one transition to all slides, animate the bullet
points of one slide, add the school name in a footer through the slide master,
write speaker notes, rehearse timings, and present it to your group in under
five minutes. Ask your listeners to check it against the ten rules above.
:::

::: tip Learn the keys of the show
**Ctrl + M** new slide · **F5** show from the beginning · **Shift + F5** from the
current slide · **Esc** end the show · **B** black screen · **N / P** next and
previous. In a "steps" answer, name the tab: *Transitions → Fade → Apply To All*.
:::

## Chapter summary

- **Presentation software** (PowerPoint, Impress, Google Slides, Keynote, Canva)
  creates and shows **slides**; files are .pptx or .odp.
- A **layout** arranges placeholders on a slide (Title Slide, Title and Content,
  Two Content, Comparison, Title Only, Picture with Caption); a **theme**
  designs all slides; a **placeholder** holds a title, text or object.
- **New slide** Ctrl + M; insert pictures, tables, charts, audio and video from
  the **Insert** tab; the **Playback** tab sets how audio and video start.
- A **transition** works **between slides** (Transitions tab, Apply To All,
  Advance After); an **animation** works on **objects** (entrance, emphasis,
  exit, motion paths; On Click, With Previous, After Previous).
- **Views:** Normal, Outline, Slide Sorter, Notes Page, Reading View, Slide
  Show. The **slide master** changes every slide at once.
- **Show:** F5 from the beginning, Shift + F5 from the current slide, Esc to
  end; Presenter View for the speaker.
- **Effective slides:** one idea per slide, 6 × 6 rule, large type, strong
  contrast, consistent design, few animations, rehearse.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these is presentation software? <span class="marks">[1]</span>
   (a) LibreOffice Calc (b) LibreOffice Impress (c) Notepad (d) Firefox
2. The default file extension of a PowerPoint presentation is <span class="marks">[1]</span>
   (a) .docx (b) .xlsx (c) .pptx (d) .odp
3. A dotted box on a slide that shows *Click to add title* is a <span class="marks">[1]</span>
   (a) theme (b) placeholder (c) transition (d) master
4. The shortcut key to add a new slide is <span class="marks">[1]</span>
   (a) Ctrl + N (b) Ctrl + M (c) Ctrl + S (d) F5
5. The effect when one slide changes to the next is a <span class="marks">[1]</span>
   (a) transition (b) animation (c) layout (d) theme
6. An animation that makes an object appear on the slide belongs to the group <span class="marks">[1]</span>
   (a) Exit (b) Emphasis (c) Entrance (d) Motion Paths
7. The view that shows small thumbnails of all slides for reordering is <span class="marks">[1]</span>
   (a) Normal (b) Slide Sorter (c) Notes Page (d) Reading View
8. Pressing F5 in PowerPoint <span class="marks">[1]</span>
   (a) saves the file (b) starts the show from the first slide (c) adds a slide (d) opens the slide master
9. To put the school logo on every slide at once, use the <span class="marks">[1]</span>
   (a) slide master (b) Slide Sorter (c) Notes Page (d) Outline View
10. An animation set to *After Previous* starts <span class="marks">[1]</span>
    (a) on a mouse click (b) at the same time as the previous effect (c) when the previous effect ends (d) at the end of the show
11. According to the 6 × 6 rule, a slide should have at most about <span class="marks">[1]</span>
    (a) six slides (b) six points of about six words each (c) six pictures (d) six colours
12. A 15-slide show advances every 8 seconds. One run lasts <span class="marks">[1]</span>
    (a) 23 s (b) 1 minute (c) 2 minutes (d) 2 minutes 30 seconds

::: note Answers to Group A
**1.** (b) — Impress is LibreOffice's presentation program.
**2.** (c) — .pptx; .odp is Impress's format.
**3.** (b) — a placeholder.
**4.** (b) — Ctrl + M.
**5.** (a) — a transition works between slides.
**6.** (c) — Entrance effects bring objects in.
**7.** (b) — Slide Sorter.
**8.** (b) — F5 runs the show from the beginning.
**9.** (a) — the slide master.
**10.** (c) — after the previous effect finishes.
**11.** (b) — six points of about six words.
**12.** (c) — 15 × 8 = 120 s = 2 minutes.
:::

**Group B — Short answer (2 marks each)**

1. What is presentation software? Name two examples. <span class="marks">[2]</span>
2. Write any four features of presentation software. <span class="marks">[2]</span>
3. Define slide layout and theme. <span class="marks">[2]</span>
4. Differentiate between a transition and an animation. <span class="marks">[2]</span>
5. Write the steps to apply the same transition to all slides. <span class="marks">[2]</span>
6. Write the steps to insert a video stored on the computer into a slide. <span class="marks">[2]</span>
7. What is the slide master? Why is it useful? <span class="marks">[2]</span>
8. Name four views of PowerPoint and write the use of any two. <span class="marks">[2]</span>
9. Write the keys used to start a slide show from the beginning, start from the current slide, show a black screen and end the show. <span class="marks">[2]</span>
10. Write any four rules for making effective slides. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Presentation software is application software for creating slides with
text, pictures, charts and multimedia and showing them one after another to
support a talk. Examples: Microsoft PowerPoint, LibreOffice Impress, Google
Slides (any two).

**2.** Any four: layouts and themes; placeholders; pictures, tables, charts,
audio and video; transitions and animations; several views; slide master;
speaker notes and Presenter View; rehearse timings; export to PDF or video.

**3.** A slide layout is the arrangement of placeholders on a slide, such as
Title and Content. A theme is a ready-made design of background, colours, fonts
and effects applied to all the slides.

**4.** A transition is the effect when moving from one slide to the next and is
set on the Transitions tab; an animation is an effect on an object (text,
picture) within a slide and is set on the Animations tab. A slide has one
transition but may have many animations.

**5.** Select a slide → Transitions tab → click an effect such as Fade → set
Effect Options and Duration → click **Apply To All**.

**6.** Select the slide → Insert tab → Video → This Device → find and select the
video file → Insert; then set Start (On Click or Automatically) on the Playback
tab.

**7.** The slide master is the top master slide that stores the design of the
presentation — background, fonts, colours, placeholder positions, logo and
footer. It is useful because a change made on it appears on every slide at
once, saving time and keeping all slides consistent.

**8.** Normal, Outline View, Slide Sorter, Notes Page, Reading View, Slide Show
(any four). Normal — editing one slide; Slide Sorter — reordering and
deleting slides; Notes Page — writing speaker notes; Slide Show — presenting
full screen (any two uses).

**9.** F5 — from the beginning; Shift + F5 — from the current slide; B — black
screen; Esc — end the show.

**10.** Any four: one idea per slide; keywords not paragraphs (6 × 6 rule);
large type (title 36–44 pt, body at least 24 pt); strong contrast between text
and background; one consistent theme; relevant pictures and charts; few
animations; check spelling; rehearse.
:::

**Group C — Long answer (4 marks each)**

1. Write the steps to create a four-slide presentation on "Tourism in Nepal" with a title slide, a picture, a table and a transition on every slide. <span class="marks">[4]</span>
2. Explain the four types of animation effect and the three ways an animation can start. <span class="marks">[4]</span>
3. Describe any four slide views with the use of each. <span class="marks">[4]</span>
4. On a slide, the title has Fade (On Click, 1 s), a picture has Zoom (After Previous, 1.5 s) and a caption has Fly In (With Previous, 1 s, delay 0.5 s). Taking the click as 0 s, find when each starts and ends, and when the slide is fully shown. <span class="marks">[4]</span>
5. Your friend's slide has a full paragraph in 12-point yellow text on a white background, three different fonts and a spinning animation on every word. Explain four problems and how to correct them. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Open PowerPoint → Blank Presentation. Slide 1 (Title Slide): type
*Tourism in Nepal* and your name. Ctrl + M for slide 2 (Title and Content):
type four points about tourist places. Ctrl + M for slide 3: Insert → Pictures
→ This Device → choose a photo of Pokhara → Insert, and add a title. Ctrl + M
for slide 4: Insert → Table → 3 columns × 4 rows, type the places, districts
and attractions. Design → choose a theme. Transitions → Fade → Apply To All.
Save (Ctrl + S) as *Tourism in Nepal.pptx* and press F5 to check.

**2.** *Entrance* (green) — the object appears, e.g. Fly In, Fade. *Emphasis*
(yellow) — draws attention while visible, e.g. Pulse, Spin. *Exit* (red) — the
object leaves, e.g. Fly Out, Disappear. *Motion Paths* — the object moves along
a line, arc or custom path. Start options: *On Click* — waits for a click;
*With Previous* — starts together with the previous effect; *After Previous* —
starts when the previous effect ends.

**3.** Any four. *Normal* — one slide large with thumbnails and notes, for
creating and editing. *Outline* — the text of all slides as an outline, for
writing content. *Slide Sorter* — thumbnails of all slides, for reordering,
deleting, hiding and setting transitions. *Notes Page* — the slide with its
notes, for preparing the speaker's notes. *Reading View* — the show in a window,
for checking. *Slide Show* — full screen, for presenting.

**4.** Title: starts at the click, **0 to 1 s**. Picture (After Previous):
starts when the title ends, **1 to 2.5 s**. Caption (With Previous, delay
0.5 s): starts with the picture at 1 s, waits 0.5 s, so **1.5 to 2.5 s**. The
slide is fully shown at **2.5 s**.

**5.** (1) *A full paragraph* — the audience reads instead of listening; use 4–6
short points. (2) *12-point text* — too small to read from the back; use at least
24 pt. (3) *Yellow on white* — poor contrast; use dark text on a light
background. (4) *Three fonts* — looks untidy; use one or two plain fonts.
(5) *Spinning animation on every word* — distracting and slow; use a simple
entrance such as Appear or Fade by paragraph, or none. (Any four.)
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. What is presentation software? Explain its eight main features. <span class="marks">[10]</span>
2. Explain transitions and animations and the rules of an effective presentation. <span class="marks">[10]</span>

### Model answer D1: features of presentation software (10 marks)

**Introduction.** **Presentation software** is application software used to make a series of **slides** containing text, pictures, charts, sound and video, and to show them to an audience. MS PowerPoint, LibreOffice Impress and Google Slides are examples. A teacher, a student or a businessperson uses it to explain ideas clearly (Plate 9.H).

1. **Slides and layouts.** A presentation is made of slides, and each slide has a layout such as Title, Title and Content, or Two Content. Placeholders in the layout hold the text and pictures in the right place. This makes slides tidy.
2. **Themes and templates.** A theme gives the whole presentation matching colours, fonts and background in one click. A school can choose one theme for all its slides so they look uniform.
3. **Text, pictures and tables.** Headings, bullet points, photographs, shapes and tables can be added and formatted. A science project slide may have a picture and three bullet points.
4. **Charts and graphs.** Numbers are shown as column, pie or line charts. For example, a pie chart of how students come to school makes the facts clear at a glance.
5. **Audio and video.** Music, a voice-over or a short film can be put on a slide, which makes a talk lively.
6. **Transitions and animations.** Transitions control how a slide enters; animations control how an object enters, moves or leaves. They attract attention when used sparingly.
7. **Slide master and views.** The Slide Master changes the design of all slides at once. Views such as Normal, Slide Sorter and Slide Show let us edit, rearrange and present.
8. **Saving and sharing.** The file can be saved as .pptx, printed as handouts, exported to PDF or shared online, and the show can run on a projector.

**Conclusion.** Presentation software makes a talk clear, interesting and easy to remember, so it is a standard tool in schools and offices.

### Model answer D2: transitions, animations and effective presentations (10 marks)

**Introduction.** A good presentation depends on both the software features and the way the slides are designed.

**Transition.** A **transition** is the visual effect when one slide changes to the next, such as Fade, Push or Wipe. It is set from the **Transitions** tab and can be applied to one slide or to all.

**Animation.** An **animation** is the effect given to an object on a slide, such as text flying in or a picture growing. It is set from the **Animations** tab. Animation has types: Entrance, Emphasis, Exit and Motion path.

| Point | Transition | Animation |
|---|---|---|
| Works on | The whole slide | One object on the slide |
| Happens | Between two slides | Inside a slide |
| Tab | Transitions | Animations |
| Types | Fade, Push, Wipe | Entrance, Emphasis, Exit, Motion path |
| Example | Fade from slide 1 to 2 | Bullet points appear one by one |

**Rules of an effective presentation.**

1. Keep one idea on each slide and use short bullet points, about six lines of six words at most.
2. Use a large font (at least 24 points for body text) so that the back bench can read it.
3. Choose strong contrast, such as dark text on a light background.
4. Use clear pictures and charts instead of long paragraphs.
5. Use only two or three fonts and a few colours.
6. Use transitions and animations sparingly; too many distract the audience.
7. Check spelling and keep the order logical: title, introduction, body, conclusion.
8. Rehearse, look at the audience and do not read the slide aloud.

**Slide show steps.** Press **F5** to start from the first slide, **Shift + F5** to start from the current slide, and **Esc** to end.

**Conclusion.** Transitions and animations add interest only when used wisely; a clear, simple and well-practised presentation is the real mark of quality.

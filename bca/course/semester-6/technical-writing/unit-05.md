---
subject: Technical Writing
grade: BCA Semester 6
unit: 5
title: Visual Communication - Tables, Charts, Diagrams and Slides
hours: 7
area: BCA 354 · Technical Writing · Unit 5
---

A table of numbers, a flowchart and a well-chosen bar chart can say in seconds what a page of prose cannot. A badly chosen graphic can mislead, sometimes deliberately. Visual communication in technical writing is therefore both a design skill and an ethical duty: show the data honestly, make it readable by everyone (including readers with colour-vision deficiency), and label it so that it stands on its own. This unit gives the rules for tables, charts and diagrams, a numerical measure of graphical honesty (Tufte's **lie factor**), the WCAG **contrast ratio** computed for common text colours, and guidance for slides and posters.

::: key What this unit gives you
- Choosing between table, chart and diagram; captions, labels and references in the text.
- Chart types and when to use each; the lie factor and truncated axes; pie-chart angles.
- Colour and accessibility: WCAG contrast ratios computed from the formula.
- Technical diagrams (flowchart, UML, architecture, sequence), screenshots, slides and posters.
:::

## 5.1 Words, tables, charts or diagrams?

| Use | When | Example |
|---|---|---|
| **Prose** | Explaining reasoning, narrative, nuance | Why one design was chosen |
| **List** | Items or steps | Installation steps |
| **Table** | Exact values, several attributes, lookup | Parameter reference, results of five algorithms on four metrics |
| **Chart** | Pattern, trend, comparison, distribution | Response time against load |
| **Diagram** | Structure, flow, relationships | Network layout, data-flow, state machine |
| **Photo / screenshot** | What something looks like | An interface screen with callouts |

**General rules.** Every graphic must be **necessary** (it adds something the text does not), **referred to** in the text ("Figure 3 shows…") before it appears, **numbered and captioned** (tables: caption above; figures: caption below, in most styles), and **understandable on its own** (title or caption saying what it shows, labelled axes with **units**, a legend if needed, the data source). Place it near the text that discusses it. State the **conclusion** in the caption or the sentence introducing it ("Response time doubles above 200 users").

## 5.2 Tables

Tables are for exact numbers and comparisons. Make them readable: a clear title; headings that say what each column contains, **with units**; **align numbers on the decimal point** (or right-align) so magnitudes are comparable; use the same number of decimals within a column; keep rows and columns few; use light horizontal rules and avoid heavy grid lines; order rows meaningfully (by size or by logical order, not randomly); highlight the key row sparingly; and put sources and notes under the table. Do not split a small table across pages. Avoid putting a long table in the main text; place it in an appendix and summarise.

## 5.3 Charts: choose by the question

| Question | Chart | Notes |
|---|---|---|
| Compare values across categories | **Bar chart** (horizontal for long labels) | Start the value axis at zero |
| Change over time | **Line chart** | Time on the x-axis; limit to a few lines; a truncated axis can be acceptable for lines if labelled |
| Parts of a whole | **Stacked bar** or **pie** (few slices) | Pies are poor for more than five slices or for comparing similar sizes |
| Relationship between two variables | **Scatter plot** | Add a trend line only if justified |
| Distribution | **Histogram** or **box plot** | Say how the bins were chosen |
| Process or sequence | **Flowchart / timeline / Gantt** | Standard symbols |
| Geography | **Map** | Use for data that depend on place |

Avoid 3-D effects, decorative backgrounds and "chartjunk"; Edward Tufte's principle of a high **data-ink ratio** says that ink should show data, not decoration. Use direct labels instead of a legend where possible, and the same colour for the same thing in every figure.

### Honest scales and the lie factor

Tufte defines the **lie factor** = (size of effect shown in the graphic) / (size of effect in the data); an honest graphic has a lie factor close to 1. **Truncating the axis of a bar chart** is the classic distortion. Suppose a company's uptime rose from 100 to 105 units, a **5%** increase in the data. If the bars are drawn on an axis that starts at 95, the first bar has height 100 − 95 = 5 and the second 105 − 95 = 10: the graphic shows a **100%** increase, so the lie factor is 100 / 5 = **20.0**. The reader would think that the quantity doubled. Rules: begin bars at zero; if you must truncate (for example on a line chart of a very stable series), mark the break clearly; keep the aspect ratio so that the slope does not exaggerate; do not use area or volume (a bubble twice as high *and* twice as wide looks four times as big) to encode a single number without noting it.

**Pie charts** divide 360° in proportion to the shares. Shares of 45%, 30%, 15% and 10% occupy angles of 162°, 108°, 54° and 36° (each angle = share × 3.6°). They sum to 360°. With similar-sized slices the eye cannot rank them, so a sorted bar chart is better.

## 5.4 Colour and accessibility

About 1 in 12 men and 1 in 200 women have some colour-vision deficiency, many readers use black-and-white printouts, and screens are read in bright sunlight, so **never use colour as the only carrier of meaning**: add labels, patterns or shapes. Use colour palettes that remain distinguishable (colour-blind-safe sets such as the Okabe–Ito palette). **Contrast** between text and background is the most important factor for legibility. The Web Content Accessibility Guidelines (**WCAG**) define a **contrast ratio** from the **relative luminance** L of the two colours: with each sRGB channel c (0–1) linearised as c/12.92 if c ≤ 0.03928 else ((c + 0.055)/1.055)^2.4, L = 0.2126·R + 0.7152·G + 0.0722·B, and **ratio = (L_lighter + 0.05) / (L_darker + 0.05)**, from 1:1 (identical) to 21:1 (black on white). WCAG level AA requires **4.5:1** for normal text (3:1 for large text and graphics); AAA requires 7:1. For text on a white background:

| Text colour on white | Hex | Contrast ratio | WCAG AA (4.5:1) for body text |
|---|---|---|---|
| Black | #000000 | 21.00:1 | pass |
| Blue | #0000ff | 8.59:1 | pass |
| Dark grey | #767676 | 4.54:1 | pass |
| Red | #ff0000 | 4.00:1 | fail |
| Medium grey | #999999 | 2.85:1 | fail |

So a medium grey such as #999999 (**2.85:1**) fails AA for body text although it looks "clean", while #767676 (**4.54:1**) is the lightest grey that passes on white. Pure red (**4.00:1**) just misses the 4.5:1 requirement for small text. Other accessibility rules: add **alt text** to every figure (a short description of what it shows and why it matters, or empty alt for pure decoration); caption videos; use real table headers; make sure figures can be understood in grayscale; and avoid text in images.

## 5.5 Technical diagrams

| Diagram | Shows | Notes |
|---|---|---|
| **Flowchart** | Steps and decisions of a process or algorithm | Terminator (start/end), process rectangle, decision diamond with labelled Yes/No branches, arrows; one start |
| **Data-flow diagram (DFD)** | Processes, data stores and external entities | Levels: context (level 0), level 1, level 2 |
| **UML** (use-case, class, sequence, activity, state) | Software structure and behaviour | Use only the diagrams that answer a question |
| **ER diagram** | Entities and relationships of a database | Cardinality labels |
| **Architecture / deployment diagram** | Components, servers, networks, trust boundaries | Layers, labelled connections with protocols (see the C4 model: context, containers, components, code) |
| **Sequence diagram** | Messages between components over time | Time flows down; good for protocols such as TLS |
| **Gantt chart** | Tasks and schedule | Show dependencies and milestones |

Principles: **one diagram, one message**; limit to about seven elements per level of detail and split larger diagrams; **consistent shapes and arrow styles**; label every arrow; a legend if notation is unusual; left-to-right or top-to-bottom flow; avoid crossing lines; use tools (draw.io, Mermaid, PlantUML, Graphviz) that store diagrams as text or editable files so they can be versioned. **Screenshots**: crop to the relevant part, use callouts numbered to match the steps, blur private data, keep them current (they age quickly), and give the text alternative.

## 5.6 Slides and posters

A presentation supports a speaker; it is not the speech. **Slides:** one idea per slide with a **sentence-style headline** that states the point ("Response time doubles above 200 users", not "Results"); large fonts (at least 24 pt body, 32 pt titles; readable from the back of the room), few words, high contrast, consistent template; one chart or image per slide with the message highlighted; no reading from the slide. The "6 × 6" rule (at most six lines of six words) is a rough guide. Structure the talk: *tell them what you will say, say it, tell them what you said*, with an opening that states the problem, three or four points, a clear conclusion and call to action. **Rehearse** with a timer (a common rate is about two minutes per slide), prepare for questions, test the projector and file format, and bring a backup (PDF). **Posters** for project exhibitions: a title and authors, the problem and objective, method, results as large figures, conclusion; readable at 1–2 metres; roughly 300–800 words in total; QR code to the demo or repository.

## 5.7 Seeing the ideas: honest axes, chart choice and contrast

```svgfig label="5.1" caption="The lie factor. The data rose from 100 to 105 (+5%). (a) On an axis that starts at 95 the bars are 5 and 10 units tall: a 100% jump, lie factor 100/5 = 20. (b) On a zero-based axis the bars are 100 and 105 tall and the picture shows what the data say, lie factor 1."
f = Fig(580, 240)
f.text(145, 18, "(a) axis starts at 95: misleading", size=12, color=RED, bold=True)
f.line(40, 200, 250, 200, color=SLATE, sw=1.6)
f.box(70, 200 - 60, 60, 60, "100", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(160, 200 - 120, 60, 120, "105", fill=ROSE, stroke=RED, size=11, bold=True)
f.text(145, 220, "baseline 95: heights 5 and 10", size=10.5, color=SLATE, italic=True)
f.text(435, 18, "(b) axis starts at 0: honest", size=12, color=TEAL, bold=True)
f.line(330, 200, 540, 200, color=SLATE, sw=1.6)
f.box(360, 200 - 120, 60, 120, "100", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(450, 200 - 126, 60, 126, "105", fill=MINT, stroke=TEAL, size=11, bold=True)
f.text(435, 220, "baseline 0: heights 100 and 105", size=10.5, color=SLATE, italic=True)
```

```svgfig label="5.2" caption="Choosing a chart by the question the reader asks. Follow the question to the chart; if no chart fits, use a table or a sentence."
f = Fig(580, 214)
f.box(200, 8, 180, 34, "What is the question?", fill=NAVY, color="#ffffff", bold=True, size=12)
C = [(8, "Exact values?", "Table", MINT, TEAL), (124, "Compare\ncategories?", "Bar chart", BLUE, NAVY), (240, "Change\nover time?", "Line chart", SAND, AMBER), (356, "Parts of a\nwhole (few)?", "Pie or\nstacked bar", ROSE, RED), (472, "Two variables\nrelated?", "Scatter plot", MINT, TEAL)]
for x, q, c, fl, st in C:
    f.arrow([(290, 42), (x + 50, 74)], color=SLATE)
    f.box(x, 74, 100, 46, q, fill=fl, stroke=st, size=11)
    f.arrow([(x + 50, 120), (x + 50, 146)], color=SLATE)
    f.box(x, 146, 100, 44, c, fill="#ffffff", stroke=st, bold=True, size=11.5)
f.text(290, 206, "start each chart with a title that states the message", size=10.5, color=SLATE, italic=True)
```

```svgfig label="5.3" caption="WCAG contrast ratios computed in this unit: the same sentence in five text colours on white. The AA requirement for body text is 4.5 to 1. Medium grey looks clean but fails; red just misses."
f = Fig(580, 176)
S = [("#000000", "21.00:1", "pass"), ("#0000ff", "8.59:1", "pass"), ("#767676", "4.54:1", "pass"), ("#ff0000", "4.00:1", "fail"), ("#999999", "2.85:1", "fail")]
for i, (c, r, v) in enumerate(S):
    x = 10 + i * 114
    f.box(x, 12, 104, 72, "", fill="#ffffff", stroke=SLATE)
    f.text(x + 52, 40, "Aa Sample", size=14, color=c, bold=True)
    f.text(x + 52, 66, "text", size=12, color=c)
    f.text(x + 52, 104, c, size=11, color=SLATE)
    f.box(x + 12, 114, 80, 24, r, fill=MINT if v == "pass" else ROSE, stroke=TEAL if v == "pass" else RED, size=11.5, bold=True)
    f.text(x + 52, 156, "AA " + v, size=11.5, color=TEAL if v == "pass" else RED, bold=True)
```

### 5.7.1 Eight rules for honest and readable visuals

1. **Choose the graphic from the question.** Use a table for exact values, a bar chart to compare categories, a line chart for change over time and a scatter plot for a relationship. A pie chart only works for a few parts of one whole. The wrong chart hides the message even when the data are correct.
2. **Start bar charts at zero.** Bars encode length, so a cut axis changes the story. In Figure 5.1 a 5% rise looks like 100%. If a line chart must be cut, mark the break clearly.
3. **Give every graphic a message title.** "Uptime rose 5% after the upgrade" tells the reader what to see, while "Uptime chart" does not. Add units, axis labels and the source. A reader should understand the figure without reading the paragraph.
4. **Keep it simple.** Remove 3-D effects, heavy grid lines and decoration that carry no data. Use direct labels instead of a legend where possible. A Nepal Rastra Bank report with clean charts is easier to trust than one with shadows and gradients.
5. **Do not use colour alone.** One man in twelve has some colour-vision deficiency, and many pages are printed in black and white. Add labels, patterns or shapes. Use limited, consistent colours so each means one thing.
6. **Check contrast.** Body text needs at least 4.5 to 1 on its background (Figure 5.3). Light grey on white is a frequent failure on slides and websites. Test with a contrast checker before publishing.
7. **Draw diagrams with a purpose.** A diagram should have one idea, consistent boxes and arrows, a legend if needed and labels you can read in print. Flowcharts, block diagrams and network maps each have conventions to follow. Too many boxes on one page become a puzzle.
8. **Design slides for the room.** Use one message per slide, at most about six lines, a font of at least 24 points and a picture instead of a paragraph. Put detail in a handout. A speaker at a college project defence should be heard, not read from the screen.

```photogrid label="5.1" cols="2" ratio="1.4" caption="Honest size encoding: Minard's map of 1869. (a) Charles Minard drew the fate of Napoleon's army in Russia (1812-1813) as a band whose width is proportional to the number of men, 1 mm for 10,000. The army crossed the Niemen with about 422,000 men, about 100,000 reached Moscow and about 10,000 came back, so the band is 42.2 mm, 10 mm and 1 mm wide. (b) Width proportional to value is honest: the survivors are 23.7 per cent at Moscow and 2.4 per cent at the end. If the same men were drawn as circles with radius proportional to the count, the area, which the eye reads, would shrink (422,000 / 10,000)^2 = 1,781 times while the data fell only 42.2 times. Tufte's lie factor, the size of the effect in the graphic divided by the size in the data, would be 1,781 / 42.2 = 42. Encode counts by length or width, never by radius."
@ photo id="bcatw/minard" cap="Minard's map (1869)"
fit 1.4
focus 0.5 0.5
@ svg cap="Band width against circle radius"
men = [422000, 100000, 10000]
assert round(men[1] / men[0] * 100, 1) == 23.7 and round(men[2] / men[0] * 100, 1) == 2.4
area = (men[0] / men[2]) ** 2; data = men[0] / men[2]
assert round(area) == 1781 and round(data, 1) == 42.2 and round(area / data) == 42
f = Fig(300, 240)
f.text(150, 14, "honest: width = number of men", size=10.5, color=TEAL, bold=True)
for i, (m, lab) in enumerate(zip(men, ["Niemen 422,000", "Moscow 100,000", "end 10,000"])):
    wd = max(m / 10000, 1)
    y = 24 + i * 20
    th = max(wd * 0.4, 1.5)
    f.box(120, y + 9 - th / 2, 160, th, "", fill="#fdba74", stroke=AMBER, r=0, sw=1)
    f.text(112, y + 9, lab, size=10.5, color=NAVY, anchor="end", vmid=True)
f.text(150, 112, "misleading: radius = number of men", size=10.5, color=RED, bold=True)
for i, m in enumerate(men):
    r = 38 * m / men[0]
    f.circle(60 + i * 90, 168, max(r, 1.5), fill="#fecaca", stroke=RED, sw=1.2)
f.text(150, 222, "area falls 1,781x, data 42.2x: lie factor 42", size=10.5, color=RED, bold=True)
```

```photogrid label="5.2" cols="2" ratio="1.0" caption="Colour must carry less than the reader needs. (a) An Ishihara plate: about 1 man in 12 and 1 woman in 200 cannot separate certain reds from greens, so a chart that uses red against green to mean bad against good is unreadable for them. (b) The WCAG contrast ratio is (L1 + 0.05) / (L2 + 0.05), with L the relative luminance of the lighter and darker colour; body text needs at least 4.5 and large text 3. Black on white scores 21.0, near-black ink 17.8 and the book's blue 5.2, all passing. Red on green scores 1.07 and grey #999999 on white 2.85, both fail; the popular grey #777777 gives 4.48, missing the limit by 0.02. Always add a second cue (a label, a pattern or a marker shape) and check contrast with a tool."
@ photo id="bcatw/ishihara" cap="An Ishihara colour-vision plate"
fit 1.0
focus 0.5 0.5
@ svg cap="WCAG contrast ratio of text and background"
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
pairs = [("#000000", "#ffffff"), ("#14181f", "#ffffff"), ("#1d6fb8", "#ffffff"), ("#777777", "#ffffff"), ("#999999", "#ffffff"), ("#d9534f", "#2e8b57")]
r = [cr(a, b) for a, b in pairs]
assert [round(x, 2) for x in r] == [21.0, 17.79, 5.23, 4.48, 2.85, 1.07]
f = Fig(300, 240)
f.text(150, 14, "pass = 4.5 or more for body text", size=10.5, color=SLATE)
for i, ((fg, bg), x) in enumerate(zip(pairs, r)):
    y = 26 + i * 33
    f.box(10, y, 64, 26, "Aa text", fill=bg, stroke=SLATE, color=fg, size=11, bold=True, r=4, sw=1)
    f.text(84, y + 13, f"{x:.2f}", size=10.5, color=NAVY, anchor="start", bold=True, vmid=True)
    ok = x >= 4.5
    f.box(140, y + 3, 54 + 0, 20, "pass" if ok else "fail", fill="#bbf7d0" if ok else "#fecaca", stroke=TEAL if ok else RED, color=TEAL if ok else RED, size=10.5, bold=True, r=4, sw=1)
    f.text(204, y + 13, fg, size=10.5, color=SLATE, anchor="start", vmid=True)
f.text(150, 230, "#777777 misses by 0.02", size=10.5, color=RED, bold=True)
```

## Chapter summary

- Choose the medium by purpose: tables for exact values, charts for patterns, diagrams for structure; every graphic is referred to, numbered, captioned and self-explanatory.
- Chart type follows the question; bars start at zero; the lie factor measures distortion (a truncated bar chart showing 5% as 100% has a lie factor of 20.0).
- Never rely on colour alone; WCAG contrast needs 4.5:1 for body text; #999999 on white gives 2.85:1 and fails.
- Diagrams carry one message with consistent notation; slides carry one idea with a headline sentence.

## Practice

1. When would you choose a table instead of a chart?
2. Name the right chart for (a) monthly rainfall over a year, (b) market share of four firms, (c) height against weight.
3. A bar chart's axis starts at 50; values are 60 and 66. Compute the lie factor.
4. Compute the pie-chart angles for shares 50%, 25%, 15%, 10%.
5. What are the WCAG AA contrast ratios for normal and large text?
6. Why is #999999 on white a poor choice for body text?
7. Give three rules for a good table.
8. What should a figure caption contain?
9. List the standard flowchart symbols and what each means.
10. State four rules for effective slides.

::: note Answers and worked solutions
**1.** When readers need exact values, several attributes per item, or lookup.
**2.** (a) Line chart (or bars) over time; (b) bar chart (or a pie with few slices); (c) scatter plot.
**3.** Data: (66 − 60)/60 = 10%. Graphic: bar heights 10 and 16, so (16 − 10)/10 = 60%. Lie factor = 60/10 = **6**.
**4.** 0.5 × 360 = **180°**, 0.25 × 360 = **90°**, 0.15 × 360 = **54°**, 0.10 × 360 = **36°** (sum 360°).
**5.** 4.5:1 for normal text and 3:1 for large text (AAA: 7:1 and 4.5:1).
**6.** Its contrast ratio is about 2.85:1, below the 4.5:1 needed for readable body text.
**7.** Numbered caption, headings with units, aligned numbers with consistent decimals, few light rules, meaningful order (any three).
**8.** What is shown, the main message, units and data source, and enough information to understand it without the text.
**9.** Rounded terminator (start/end), rectangle (process step), diamond (decision with Yes/No exits), parallelogram (input/output), arrows (flow).
**10.** One idea per slide, sentence headlines, large fonts and high contrast, minimal text with a clear visual, consistent template, rehearse with a timer (any four).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the lie factor with an example. How can charts be made honest?**

*Definition.* Tufte's **lie factor** = (size of effect shown in the graphic) / (size of effect in the data). An honest graphic has a lie factor close to 1.

*Example (Figure 5.1).* A company's uptime rose from 100 to 105, a 5% increase. If the bars start at 95, their heights are 5 and 10, so the picture shows a 100% rise. Lie factor = 100 / 5 = **20**: the reader believes the quantity doubled. On a zero-based axis the bars are 100 and 105 tall and the factor is 1.

*Making charts honest.*

1. Start bar charts at zero; mark any break on a line chart.
2. Keep the aspect ratio reasonable and the scale even.
3. Show units, source and sample size.
4. Avoid 3-D and area effects that exaggerate size.
5. Choose the chart from the reader's question.

*Conclusion.* A chart is evidence, so its size must match the data. A distorted chart misleads even if every number printed on it is correct.

**Q2 (5 marks). What is colour accessibility? Compute and interpret WCAG contrast for the colours given in the unit.**

*Accessibility.* About 1 in 12 men and 1 in 200 women have a colour-vision deficiency; readers also use black-and-white printouts and read in sunlight. So never use colour as the only carrier of meaning, and give text enough contrast with its background.

*WCAG rule.* The contrast ratio is (L1 + 0.05) / (L2 + 0.05), where L is relative luminance. WCAG AA asks for **4.5 : 1** for body text and 3 : 1 for large text.

| Text on white | Hex | Ratio | AA body text |
|---|---|---|---|
| Black | #000000 | 21.00:1 | pass |
| Blue | #0000ff | 8.59:1 | pass |
| Dark grey | #767676 | 4.54:1 | pass |
| Red | #ff0000 | 4.00:1 | fail |
| Medium grey | #999999 | 2.85:1 | fail |

*Interpretation.* #767676 is the lightest grey that still passes on white; #999999 looks neat but fails. Fix by darkening the text, adding a label or pattern, and checking with a contrast tool. *Conclusion:* accessible design helps everyone, not only people with disabilities.

**Q3 (10 marks). Explain how to choose and design tables, charts, diagrams and slides for a technical document.**

*Introduction.* Words, tables, charts and diagrams each carry information best in different cases. The writer must choose by the reader's question and then design the graphic so that it is honest, readable and accessible (Figures 5.1 to 5.3).

*1. Tables.* Use when readers need exact values or comparisons across several attributes. Rules: a title, clear column headings with units, aligned numbers, consistent decimals, light lines, no empty cells without a note.

*2. Charts.* Choose by question (Figure 5.2): bar for categories, line for time, scatter for relationships, pie or stacked bar for a few parts of a whole, histogram for distribution. Give a message title, axis labels with units and the data source.

*3. Honest scales.* Bars start at zero. The lie factor compares the effect drawn with the effect in the data: truncating an axis for a 5% change gives a factor of 20.

*4. Colour and accessibility.* Do not rely on colour alone; use patterns and labels; keep contrast at 4.5 : 1 or better (#767676 passes at 4.54, #999999 fails at 2.85).

*5. Technical diagrams.* One idea per diagram; consistent shapes and arrows; labels in readable size; a legend; a caption and a reference in the text. Types: flowchart, block, network, UML, ER and sequence diagrams.

*6. Slides and posters.* One message per slide, at most about six lines, large type, one picture, and detail in a handout. Rehearse with a timer.

*Comparison.*

| Need | Best form | Avoid |
|---|---|---|
| exact values | table | chart without labels |
| compare categories | bar chart | pie with 12 slices |
| trend over time | line chart | 3-D bars |
| relationship | scatter plot | dual axes without warning |
| process | flowchart | paragraph of steps |
| talk | slide with one idea | slide of full sentences |

*Conclusion.* Good visuals are chosen by the question, drawn with honest scales and checked for contrast, so they let the reader see the point in seconds without being misled.

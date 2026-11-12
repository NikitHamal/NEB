---
subject: Technical Writing
grade: BCA Semester 6
unit: 8
title: Instructions, Technical Descriptions and Formal Reports
hours: 10
area: BCA 354 · Technical Writing · Unit 8
---

The TU Technical Writing outline names three genres that Units 1 to 7 only brush against: **instructions** (how to do a task), **technical definitions and descriptions** (what a thing is and how it is built) and **formal reports** (the long, structured document that ends a project or study). This unit treats each of them as a full chapter, with the parts, the language, the checks and a model you can copy in an examination.

::: key What this unit gives you
- How to write **instructions** that a stranger can follow without asking you: structure, imperative style, notices, visuals, and a usability test.
- How to write a **technical definition** (term, class, differentia) and an **extended definition**, and how a *description* differs from *instructions*.
- The full anatomy of a **formal report**: front matter, body, back matter, page numbering and the letter of transmittal.
- **Recommendation and feasibility reports**: criteria, a weighted decision matrix and the honest handling of the result.
- A report **checklist** and the ethics of reporting (nothing hidden, nothing invented).
:::

## 8.1 Instructions

**Instructions** are step-by-step directions that tell a reader how to carry out a task safely and correctly: install a program, configure a router, reset a password, submit an online form. They differ from a *process description* (Unit 7), which explains **how something happens** to a reader who will only watch, in that instructions are written for a reader who will **act**, and who will often have the page next to the keyboard and be following it one step at a time.

### Why instructions fail

Most bad instructions fail for the same few reasons:

| Failure | What goes wrong | Cure |
|---|---|---|
| The writer knows too much | Steps are skipped because they are "obvious" | Do the task yourself from a clean start and record every action |
| Several actions in one step | The reader does the first and forgets the second | **One action per step** |
| Vague verbs and objects | "Set up the server", "adjust the settings" | Name the exact button, menu, command or value |
| Warnings after the damage | "Do not unplug the device" appears after step 6 | Put the notice **before** the step it protects |
| No result described | Reader cannot tell if the step worked | Say what the reader should see after the step |
| No test with real users | The writer is the only reader | Usability test with someone who has never done the task |

### Plan before you write

1. **The reader.** A first-time user, a trained technician or an administrator? A student installing Python needs "click Next"; an administrator needs the command and the flags.
2. **The task.** State it as one goal in the form *verb + object* ("Install Python 3 on Windows 11"). If a task is too big, split it into several documents or chapters.
3. **The conditions.** What does the reader need before starting: hardware, software, permissions, time, files? List them.
4. **The risks.** What can be damaged, lost or injured? Each risk becomes a notice.
5. **The medium.** Printed card, PDF, web page, video, in-app tooltips. Phone screens suit short numbered steps and screenshots; a lab bench suits large print.

### Parts of a set of instructions

A complete set has most of these parts, in this order:

| Part | Content | Example |
|---|---|---|
| **Title** | Verb-led, names the task and the product | "Connect a Laptop to the College Wi-Fi" |
| **Introduction** | What the task achieves, who should do it, how long it takes, what the reader will have at the end | "This takes about 5 minutes and gives you internet access on any campus floor." |
| **Requirements** | A list of tools, materials, accounts, files and prerequisites | "A laptop with Wi-Fi, your student ID number, the password sheet" |
| **Notices** | Warnings, cautions and notes (see below) | "Do not share your password." |
| **Steps** | A numbered sequence of single actions, grouped under headings when there are more than about eight | "1. Open **Settings** > **Network**." |
| **Result and verification** | What the reader should see, and a way to test it | "The Wi-Fi icon shows *Connected*. Open any web page." |
| **Troubleshooting** | A table of problem, likely cause, fix | "No *Connect* button: Wi-Fi is switched off; press Fn + F2." |
| **Further help** | Contact, support hours, link to a longer manual | "IT desk, room 104, 10:00 to 16:00" |

### The language of instructions

- **Imperative mood, active voice, second person understood:** "Press **Enter**", not "The Enter key should be pressed" or "The user must press Enter".
- **Begin each step with a verb**: Open, Select, Type, Click, Wait, Check, Save.
- **One action per step**, except when two actions are inseparable ("Type your password and press **Enter**" is acceptable; "Type your password, press Enter, wait for the page, and click Profile" is not).
- **Parallel form:** all steps in the same grammatical pattern, all numbered the same way.
- **Exact names for things**, written the same way every time and in the same typeface as on the screen: **Start**, **Control Panel**, `ipconfig /all`.
- **Specific quantities with units:** "Wait 30 seconds", not "Wait a bit".
- **Say what happens:** "A dialog box titled *Security Alert* appears. Click **Yes**."
- **Put conditions first:** "If the light is red, hold the reset button for five seconds." (the reader checks the light, then acts), not "Hold the reset button for five seconds if the light is red".
- **Avoid** "should", "may want to", "it is recommended", and long paragraphs between steps.

### Notices: danger, warning, caution and note

Four levels of notice are used in most industrial and consumer documentation, following the safety-sign standards (ANSI Z535 in the United States and ISO 3864 internationally):

| Level | Meaning | Position | Example |
|---|---|---|---|
| **Danger** | Immediate hazard that **will** cause death or serious injury | Before the step, large, red | "Danger: 230 V inside. Disconnect the mains before opening the case." |
| **Warning** | Hazard that **could** cause death or serious injury | Before the step, orange | "Warning: the power-supply capacitors can hold charge for minutes after switching off." |
| **Caution** | Hazard that could cause minor injury or damage to equipment or data | Before the step, yellow | "Caution: formatting erases all files on the drive." |
| **Note** | Useful information that is not a hazard | Before or after the step | "Note: the update takes about ten minutes." |

Write each notice as: **the signal word, the hazard, the consequence, the avoidance**. "Caution: static electricity can destroy RAM. Touch the metal case before handling the module, or wear an anti-static wrist strap." Do not overuse notices; if everything is a warning, the reader stops seeing them.

### Visuals in instructions

Use a picture wherever words would take longer or be ambiguous: a screenshot with the target button circled, a labelled photograph of a motherboard, a diagram of a cable pinout (T568B), a flowchart for troubleshooting. Each image has a number and caption, is placed **next to the step it supports**, and carries a label that matches the text word-for-word. Do not decorate; every visual must help someone act (Unit 5).

```svgfig label="8.1" caption="The anatomy of a set of instructions: the reader meets the goal, the requirements and the notices before the first step, and finishes with a way to check the result and a troubleshooting table. Notices sit before the step they protect."
f = Fig(600, 300)
f.text(300, 18, "Instructions: what the reader meets, in order", size=12, color=NAVY, bold=True)
f.box(20, 36, 170, 50, "Title and goal\nverb + object", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(215, 36, 170, 50, "Requirements\ntools, files, accounts", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(410, 36, 170, 50, "Notices\ndanger, warning,\ncaution, note", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.box(20, 120, 170, 56, "Numbered steps\none action each,\nimperative verb", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(215, 120, 170, 56, "Visuals\nscreenshots, diagrams\nnear their step", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(410, 120, 170, 56, "Result check\nwhat the reader\nshould see", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(115, 210, 170, 50, "Troubleshooting\nproblem, cause, fix", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(315, 210, 170, 50, "Further help\ncontact, longer manual", fill=BLUE, color=NAVY, size=10, bold=True)
f.text(300, 284, "tested with a first-time user before release", size=10, color=NAVY)
```

### A model: installing Python on Windows

**Install Python 3 on Windows 11**

This takes about ten minutes and gives you the `python` command in a terminal. You need an internet connection and permission to install programs.

*You will need:* a Windows 11 computer, about 300 MB of free disk space, and the installer from python.org.

::: caution Notice before step 4
**Caution:** tick **Add python.exe to PATH** on the first installer screen. If you forget, the `python` command will not be found and you will have to reinstall.
:::

1. Open a browser and go to **python.org/downloads**.
2. Click **Download Python 3.x** (the number on the button is the current release).
3. Open the downloaded file from your **Downloads** folder.
4. Tick **Add python.exe to PATH** at the bottom of the first window.
5. Click **Install Now** and wait until the bar is full (about two minutes).
6. Click **Close** when you see *Setup was successful*.
7. Press **Windows + R**, type `cmd`, and press **Enter**. A black window opens.
8. Type `python --version` and press **Enter**.

*Result:* the window prints `Python 3.x.y` with the version you installed. If it prints *'python' is not recognized*, go to the troubleshooting table.

| Problem | Likely cause | Fix |
|---|---|---|
| *'python' is not recognized* | PATH box was not ticked | Run the installer again, choose **Modify**, tick **Add to environment variables** |
| Installer asks for an administrator password | Standard account | Ask the IT desk or install for the current user only |
| `python --version` shows 2.7 | Old installation earlier in PATH | Use `py -3 --version` or remove the old version |

Notice what the model does: a verb-led title, a time and result in the introduction, the requirement list, the caution **before** step 4, one action per step, exact names in bold, a stated result, and a troubleshooting table.

### Usability testing

The only way to know that instructions work is to **watch someone use them**. Choose a reader like your real user, give them the document and the product (not you), say nothing, and note: where they hesitate, which step they skip, which word they misread, whether they reach the result. Revise and test again with a new person. Even three testers find most problems. This is the "testing documents with readers" practice of Unit 1.

::: tip Exam tip
"Write instructions for ..." is a common 10-mark question (to make tea, to send an email with an attachment, to change a tyre, to install an app). Give it a **title**, a one-line **introduction**, a **requirements** list, a **caution** if there is any risk, **numbered one-action steps beginning with verbs**, and a **result line**. Eight to twelve steps and a note is enough; a clean form earns more than a long text.
:::

## 8.2 Technical definitions and descriptions

### Technical definitions

A **definition** fixes the meaning of a term so that every reader reads it the same way. In technical writing three levels are used, from shortest to longest.

**1. Parenthetical definition.** A few words in brackets or between commas, when the reader nearly knows the word: "The router uses NAT (network address translation) to share one public address."

**2. Formal (sentence) definition.** One sentence in the pattern

> **term = class + differentia**

The **class** (genus) is the larger group the thing belongs to; the **differentia** is what separates it from the other members of that group.

| Term | Class | Differentia (what makes it different) |
|---|---|---|
| A **compiler** is | a program | that translates a whole source program into machine code before it runs. |
| A **firewall** is | a network security system | that allows or blocks traffic according to rules. |
| A **primary key** is | a column or set of columns of a table | whose values are unique and not null and identify each row. |
| A **router** is | a network device | that forwards packets between different networks using IP addresses. |

Tests of a good formal definition:

- It is **not circular**: "A database is a system for managing databases" fails.
- The class is **close enough** to be useful: "A router is a thing that..." is too wide; "network device" is right.
- The differentia is **necessary and sufficient**: it covers every router and only routers.
- It uses **simpler words** than the term and is **not negative** unless unavoidable ("A mammal is an animal that is not a bird" is poor).
- It does not use "**is when**" or "**is where**": write "Phishing is a fraud technique in which...", not "Phishing is when...".

**3. Extended definition.** A paragraph, section or page that develops a formal definition when the reader needs more. Choose from these methods, using as many as the audience requires:

| Method | What it adds | Example for *cloud computing* |
|---|---|---|
| **Formal definition** | Class and differentia | On-demand delivery of computing resources over the Internet with pay-as-you-go pricing |
| **Etymology / history** | Where the word came from | The cloud-shaped symbol drawn for "the network" in diagrams |
| **Examples** | Typical cases | Gmail, Google Drive, AWS EC2 |
| **Analogy / comparison** | A familiar parallel | Like renting electricity from the grid instead of running your own generator |
| **Contrast / negation** | What it is not | Not the same as a website hosted on a single local server |
| **Classification** | Kinds or types | IaaS, PaaS, SaaS; public, private, hybrid |
| **Process / function** | How it works or what it does | A user requests a virtual machine and the provider allocates it from a pool |
| **Components** | The parts | Data centres, virtualisation layer, APIs, billing |
| **Visual** | Picture or diagram | The layered stack |

Where to place a definition: **in the text** (a sentence or parenthetical) for short ones; in a **footnote** or **glossary** for terms used in many places; in a **separate section** for a concept the whole document depends on.

### Technical descriptions

A **technical description** tells a reader what an object, device, system or place **is, looks like and is made of**. It uses **space** and **parts** as its organising principle; a process description or set of instructions uses **time**.

| Kind | Describes | Organised by | Example |
|---|---|---|---|
| **Description of a mechanism** | An object or device | Parts, top to bottom or outside to inside | A computer mouse, a smartphone, a router |
| **Description of a process** | A sequence of events | Time order (stages) | How a compiler works, how a packet travels |
| **Description of a system / place** | A larger structure | Zones or subsystems | The college computer lab, a data centre |

A description of a mechanism (the Unit 7 section gave the outline and a mouse example) contains:

1. **Title** and **introduction**: the object's name, a formal definition, its purpose, its main parts in a sentence.
2. **General description**: overall look, size, weight, materials, an overview diagram.
3. **Part-by-part description**: for each part, its shape, size, material, location, purpose and relation to the others, in a logical order.
4. **Description of operation** (optional): how the parts work together.
5. **Conclusion**: a summary or a note on use and care.

**Language of description:** precise **measurements** with units (15 cm x 8 cm, 120 g), **comparisons** to familiar things (about the size of a credit card), **spatial words** (above, beneath, to the left of, attached to, adjacent to), **present tense** and **third person**, and a **consistent** order (always left to right, or always input to output).

**Description versus instructions.** For a router: a *description* says "The router is a rectangular box 20 cm wide with four LAN ports on the back"; *instructions* say "Plug one end of the cable into the WAN port". The first lets the reader picture the object; the second makes the reader do something. Many manuals combine both, with the description first.

## 8.3 Formal reports

A **formal report** is a long, structured document, prepared for a defined reader and a decision, that presents the results of an investigation, a project or an analysis. It follows a **standard format** so that the reader can find any part without reading the whole. BCA students meet it as the **project report**, the **internship report** and the **feasibility study**.

### Kinds of formal reports

| Kind | Purpose | Typical reader |
|---|---|---|
| **Informational** | Presents facts (annual report, a survey of the library's use) | Managers, committees |
| **Analytical** | Presents facts and **interprets** them (why sales fell) | Executives |
| **Recommendation** | Compares options and **recommends** one | Decision makers |
| **Feasibility study** | Judges whether a proposed project is possible, affordable and worthwhile | Sponsors, boards |
| **Lab or test report** | Records an experiment or test and its results | Supervisors, peers |
| **Progress report** | Reports state of work during a project (Unit 7) | Supervisor, client |
| **Project or thesis report** | Documents a complete piece of work | Examiners, future developers |

### The three zones of a formal report

```svgfig label="8.2" caption="The three zones of a formal report. Front matter helps the reader decide and navigate and is numbered in lower-case roman numerals; the body is numbered in arabic from 1; back matter supports the body. The executive summary and abstract are written last."
f = Fig(600, 330)
f.text(300, 18, "Formal report: front matter, body, back matter", size=12, color=NAVY, bold=True)
f.box(20, 34, 170, 40, "FRONT MATTER  (i, ii, iii ...)", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.box(20, 84, 170, 28, "Cover and title page", fill=BLUE, color=NAVY, size=10)
f.box(20, 118, 170, 28, "Letter of transmittal", fill=BLUE, color=NAVY, size=10)
f.box(20, 152, 170, 28, "Abstract / executive summary", fill=BLUE, color=NAVY, size=10)
f.box(20, 186, 170, 28, "Contents, lists of figures, tables", fill=BLUE, color=NAVY, size=10)
f.box(20, 220, 170, 28, "Acknowledgements", fill=BLUE, color=NAVY, size=10)
f.box(215, 34, 170, 40, "BODY  (1, 2, 3 ...)", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(215, 84, 170, 28, "1 Introduction", fill="#d1fae5", stroke=TEAL, color=NAVY, size=10)
f.box(215, 118, 170, 28, "2 Method / background", fill="#d1fae5", stroke=TEAL, color=NAVY, size=10)
f.box(215, 152, 170, 28, "3 Findings / discussion", fill="#d1fae5", stroke=TEAL, color=NAVY, size=10)
f.box(215, 186, 170, 28, "4 Conclusions", fill="#d1fae5", stroke=TEAL, color=NAVY, size=10)
f.box(215, 220, 170, 28, "5 Recommendations", fill="#d1fae5", stroke=TEAL, color=NAVY, size=10)
f.box(410, 34, 170, 40, "BACK MATTER", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(410, 84, 170, 28, "References / bibliography", fill=BLUE, color=NAVY, size=10)
f.box(410, 118, 170, 28, "Appendices (A, B, C)", fill=BLUE, color=NAVY, size=10)
f.box(410, 152, 170, 28, "Glossary", fill=BLUE, color=NAVY, size=10)
f.box(410, 186, 170, 28, "Index (long reports)", fill=BLUE, color=NAVY, size=10)
f.text(300, 280, "Reader decides from the front, learns from the body, checks from the back", size=10, color=NAVY)
f.text(300, 300, "write the summary and the introduction last", size=10, color=NAVY)
```

### Front matter

| Element | What it contains | Note |
|---|---|---|
| **Cover** | Title, author, organisation, date | Often a university-prescribed layout |
| **Title page** | Full title, "submitted to", "submitted by", date; in TU reports also programme, semester, supervisor | Title says what, for whom, and about what |
| **Letter or memo of transmittal** | A short letter that **presents** the report to the reader: what it is, why it was written, main finding, thanks, offer to discuss | Follows business-letter form; not numbered |
| **Certificate / approval** | Supervisor's and examiner's signatures (academic reports) | Needed in TU project reports |
| **Abstract** | 150 to 250 words: purpose, method, main findings, conclusion | For researchers who decide whether to read |
| **Executive summary** | One page: problem, findings, recommendation, cost | For busy managers; stands alone; written last |
| **Acknowledgements** | Thanks to supervisors, organisations, helpers | Brief |
| **Table of contents** | All headings with page numbers | Generated by the software |
| **Lists of figures and tables** | Numbers, captions, pages | Needed if there are more than a few |

**The letter of transmittal.** Written by the author to the person who asked for the report. Paragraph 1 says "Here is the report you requested on ..." with its title and date; paragraph 2 summarises its scope and main conclusion; paragraph 3 notes any limits or special help; the last paragraph thanks and offers to discuss. About 150 to 200 words.

> Dear Principal Sharma,
>
> I submit the attached report, *Feasibility of a Biometric Attendance System for NEBians College*, which you requested on 12 Kartik. It compares three systems on cost, accuracy, installation time and maintenance, and recommends the fingerprint terminal with cloud sync. The estimated cost for 400 students is Rs 3,20,000, recovered in about 14 months from savings in staff time. I thank the administration office and the IT desk for the data. I would be glad to discuss the report at your convenience.
>
> Yours sincerely, Sita Rai, BCA Semester 6

**Page numbering.** Cover and title page carry no visible number; the remaining front matter uses **lower-case roman numerals** (ii, iii, iv...); the body begins at **1** in arabic numerals and continues through the back matter. Appendices may be numbered A-1, A-2...

### The body

The body is divided into numbered sections with **informative headings**. Sections and their order depend on the report kind. A **project report** typically has:

1. **Introduction:** background, problem statement, objectives, scope and limitations, significance, organisation of the report.
2. **Literature review / related work:** what others have done and the gap.
3. **Methodology:** the approach, tools, data, and design (system analysis, design diagrams).
4. **Implementation and results:** what was built, screenshots, test results, data tables.
5. **Discussion:** interpretation of results, strengths, limitations.
6. **Conclusions and recommendations (or future work).**

A **recommendation or feasibility report** has an **Introduction** (purpose, background, scope), **Criteria** (how options are judged), **Options** (each described and evaluated against the criteria), **Comparison** (a table or matrix), **Conclusion** (the finding) and **Recommendation** (the action to take).

**Two points on writing the body.** First, **conclusions** are what the findings *mean*; **recommendations** are what the reader *should do*; keep them in separate, parallel lists, and never put a new fact into either. Second, each section opens with a **topic sentence** that states its point, and each figure or table is numbered, captioned, and **referred to in the text** before it appears.

### Back matter

| Element | Purpose |
|---|---|
| **References** | Full details of every source cited, in one citation style (APA, IEEE; Unit 4) |
| **Bibliography** | Sources read but not cited (optional) |
| **Appendices** | Material the body should not carry: questionnaires, raw data, long code, screenshots, calculations; each lettered and titled, and cited in the text |
| **Glossary** | Technical terms and abbreviations with meanings |
| **Index** | Alphabetical list of topics with page numbers (long reports only) |

## 8.4 Recommendation and feasibility reports

A **recommendation report** compares two or more options and says which one to choose. A **feasibility report** asks whether *one* proposed course of action is possible, affordable and worthwhile. Both stand on **criteria**: the standards that the options are judged against. The principle is that the reader should be able to **re-do the judgement** from the report and arrive at the same answer.

### Feasibility: the usual tests

| Test | Question | Evidence |
|---|---|---|
| **Technical** | Can it be built or done with available technology and skills? | Specifications, prototype, expert opinion |
| **Economic** | Do benefits exceed costs? How long to pay back? | Cost table, payback period, cost-benefit ratio |
| **Operational** | Will people use it and will it fit the way they work? | Survey, interviews, pilot |
| **Schedule** | Can it be done in the time available? | Work plan, Gantt chart |
| **Legal and ethical** | Does it respect law, privacy and policy? | Regulations, consent, data-protection review |

### Choosing criteria and a weighted decision matrix

1. List **criteria** that matter to the reader (cost, accuracy, installation time, maintenance).
2. Give each a **weight** (percent) that reflects its importance; the weights add to 100.
3. **Score** each option on each criterion on one scale (1 = poor to 5 = excellent), using evidence, not impressions.
4. Multiply score by weight and add: the highest total wins.
5. **Test the result:** change the weights a little and see whether the winner changes (**sensitivity analysis**). A winner that survives is robust; a winner that flips shows the decision depends on the weights, which must then be stated openly.

```python
criteria = ["Cost", "Accuracy", "Install time", "Maintenance"]
weights  = [0.30, 0.30, 0.15, 0.25]
scores = {
    "Fingerprint + cloud": [3, 5, 4, 4],
    "RFID cards":          [5, 3, 5, 3],
    "Face recognition":    [2, 4, 3, 3],
}
def totals(w):
    return {name: sum(x * y for x, y in zip(w, s)) for name, s in scores.items()}
print("Base weights:", dict(zip(criteria, weights)))
for name, t in sorted(totals(weights).items(), key=lambda kv: -kv[1]):
    print("%-22s %.2f" % (name, t))
# sensitivity: if cost matters more and accuracy less
w2 = [0.45, 0.15, 0.15, 0.25]
print("Cost-heavy weights:", dict(zip(criteria, w2)))
for name, t in sorted(totals(w2).items(), key=lambda kv: -kv[1]):
    print("%-22s %.2f" % (name, t))
```
```output
Base weights: {'Cost': 0.3, 'Accuracy': 0.3, 'Install time': 0.15, 'Maintenance': 0.25}
Fingerprint + cloud    4.00
RFID cards             3.90
Face recognition       3.00
Cost-heavy weights: {'Cost': 0.45, 'Accuracy': 0.15, 'Install time': 0.15, 'Maintenance': 0.25}
RFID cards             4.20
Fingerprint + cloud    3.70
Face recognition       2.70
```
The result is worth reading carefully. With the base weights the fingerprint terminal narrowly leads (4.00 against 3.90), but when the weight on cost rises from 30% to 45% the RFID cards win. An honest report therefore says: "**Fingerprint is recommended because accuracy and low maintenance matter most to the college; if the budget is the overriding constraint, RFID cards are the better choice.**" Hiding that the ranking is sensitive to the weights is a form of manipulation (Unit 6 of this book).

### Costs, benefits and payback

For the **economic** test, show the costs in a table that adds up, estimate the **recurring savings**, and compute a **payback period** = initial cost / saving per period. State every assumption.

```python
students = 400
items = {"Terminals (4 x Rs 45,000)": 180000, "Cloud licence (1 year)": 60000,
         "Installation and cabling": 50000, "Training and pilot": 30000}
total = sum(items.values())
for k, v in items.items():
    print("%-30s Rs %8d" % (k, v))
print("%-30s Rs %8d" % ("TOTAL", total))
print("Cost per student: Rs %.0f" % (total / students))
saving_per_month = 23000    # staff time on manual registers, estimated by the admin office
print("Payback: %.1f months" % (total / saving_per_month))
```
```output
Terminals (4 x Rs 45,000)      Rs   180000
Cloud licence (1 year)         Rs    60000
Installation and cabling       Rs    50000
Training and pilot             Rs    30000
TOTAL                          Rs   320000
Cost per student: Rs 800
Payback: 13.9 months
```
The model letter of transmittal above quotes exactly these figures: Rs 3,20,000, recovered in about 14 months. **Every number in the summary must be traceable to a table in the body**, and every table to an appendix or reference.

### The structure of a recommendation report (model)

| Section | Content for the attendance example |
|---|---|
| **Executive summary** | Problem, options compared, recommendation, cost and payback in 150 words |
| **1 Introduction** | Manual attendance wastes about 10 minutes per class; scope: 400 students |
| **2 Criteria** | Cost (30%), accuracy (30%), installation time (15%), maintenance (25%), and why |
| **3 Options** | Fingerprint with cloud sync; RFID cards; face recognition, each with specification and source |
| **4 Evaluation** | Score table and weighted totals; sensitivity analysis |
| **5 Costs and benefits** | Cost table, payback |
| **6 Conclusions** | The fingerprint option scores highest; the result is sensitive to the cost weight |
| **7 Recommendation** | Adopt the fingerprint option; pilot on one floor first; review after one term |
| **Appendices** | Questionnaire, quotations, product data sheets |

## 8.5 Report checklist and ethics of reporting

Before submitting a formal report, check it three times: for **content**, for **form** and for **honesty**.

**Content**
- The purpose, the reader and the decision are stated on the first page.
- The executive summary or abstract matches the body and can be read alone.
- Every conclusion follows from a stated finding; every recommendation from a conclusion.
- Numbers add up; units are stated; tables and charts agree with the text.

**Form**
- The headings are informative and consistently numbered; the contents page matches.
- Every figure and table is numbered, captioned and cited in the text.
- Every source in the text is in the reference list and vice versa, in one style.
- Front matter in roman numerals, body in arabic numerals; margins, fonts and spacing consistent.
- Language is plain (Unit 2): short sentences, active voice, no unexplained jargon, spelling checked.

**Honesty**
- No data were invented, rounded favourably or dropped because they were inconvenient.
- Limits and uncertainties are stated; opposing evidence is reported.
- Others' work is cited; no copied text or figures without credit (Unit 4).
- Charts have honest axes (Unit 5); the sensitivity of the recommendation is shown.
- Confidential or personal information is protected or anonymised (Unit 6).

**Why it matters.** Technical reports are used to spend money, to certify safety and to choose systems. The reader cannot check everything, so they rely on the writer's honesty. A report that conceals a risk may be unprofessional in tone but is unethical in effect; professional codes (such as the ACM Code) ask for honest, accurate reporting of all known risks and results.

## Formula and fact sheet

- Instruction set: title, introduction, requirements, notices, numbered steps, result, troubleshooting, help. One action per step, imperative verb, notice before the step.
- Notice levels: **danger** (will kill or seriously injure), **warning** (could), **caution** (minor injury or damage), **note** (information).
- Formal definition: **term = class + differentia**. Extended definition methods: formal, etymology, examples, analogy, contrast, classification, process, components, visual.
- Description of a mechanism: introduction, general description, part-by-part, operation, conclusion; space order; measurements and spatial words.
- Formal report: front matter (roman), body (arabic), back matter. Transmittal letter, abstract/executive summary, contents, introduction ... conclusions, recommendations, references, appendices.
- Recommendation report: criteria, options, comparison, conclusion, recommendation. Score = sum of weight x score. Check sensitivity.
- Payback period = initial cost / saving per period.

## Chapter summary

- Instructions tell a reader how to act, so they need a verb-led title, requirements, notices before steps, one action per step, a stated result and a troubleshooting table, and they must be tested with a first-time user.
- A formal definition names the class and the differentia; an extended definition adds methods such as examples, analogy, classification and process.
- A description of a mechanism pictures an object by parts in a fixed spatial order with exact measurements; a process description uses time order.
- A formal report has front matter, body and back matter; the abstract or executive summary and letter of transmittal are written last, and the body separates findings, conclusions and recommendations.
- Recommendation and feasibility reports rest on stated criteria, a transparent decision matrix, costs that add up and a sensitivity check; honesty about uncertainty is a professional duty.

## Practice

1. List the parts of a good set of instructions in order.
2. Write four rules for the language of instructions and illustrate each with a correct and a faulty step.
3. Differentiate danger, warning, caution and note, with one example of each from computing.
4. Write formal definitions for: (a) a database, (b) a web browser, (c) a switch (network device).
5. Name five methods of extended definition and apply three of them to the term *API*.
6. Differentiate a description of a mechanism from a set of instructions.
7. Draw and label the three zones of a formal report and state the page-numbering convention.
8. What is a letter of transmittal, and what four things should it say?
9. Differentiate conclusions from recommendations in a report.
10. In a decision matrix, criteria weights are Cost 40%, Quality 35%, Support 25%. Option X scores 4, 3, 5 and Option Y scores 3, 5, 3 on a 1 to 5 scale. Compute the weighted totals and state which wins.
11. A project costs Rs 2,40,000 and is expected to save Rs 15,000 per month. Compute the payback period.
12. Write a one-page set of instructions to send an email with an attachment.

::: note Answers and worked solutions
**1.** Title, introduction (goal and time), requirements, notices, numbered steps, result and verification, troubleshooting, further help.
**2.** (i) Use the imperative: "Press Enter" not "Enter should be pressed". (ii) One action per step: "Click **Save**" not "Click Save, close the window and open the folder". (iii) Name things exactly: "Click **File** > **Export**" not "go to the export option". (iv) State conditions first: "If the light is red, press Reset" not "Press Reset if the light is red".
**3.** Danger: "230 V inside; disconnect mains before opening the power supply." Warning: "Lithium batteries can ignite if punctured." Caution: "Formatting erases all data on the drive." Note: "The update takes about ten minutes."
**4.** (a) A database is an organised collection of related data stored so that it can be retrieved and updated by software. (b) A web browser is a software application that retrieves and displays web pages from servers using HTTP. (c) A switch is a network device that forwards frames between devices on the same network using MAC addresses.
**5.** Formal definition: a set of rules by which one program requests services from another. Example: a weather API returns tomorrow's forecast as JSON. Analogy: a waiter who takes your order to the kitchen and brings back food. (Also: classification into REST, SOAP; components, endpoints, methods.)
**6.** A description of a mechanism pictures the object by parts in spatial order for a reader who will look; instructions tell the reader what to do in time order, with verbs and notices.
**7.** Front matter (roman numerals: transmittal letter, abstract, contents, lists), body (arabic from 1: introduction to recommendations), back matter (references, appendices, glossary). Cover and title page carry no number.
**8.** A short letter that presents the report: (1) names the report and who requested it; (2) states its scope and main conclusion; (3) mentions limits or special help; (4) thanks the reader and offers to discuss.
**9.** Conclusions are what the findings mean (statements of fact or judgement); recommendations are actions the reader should take. Neither contains new facts.
**10.** X = 0.40 x 4 + 0.35 x 3 + 0.25 x 5 = 1.60 + 1.05 + 1.25 = **3.90**. Y = 0.40 x 3 + 0.35 x 5 + 0.25 x 3 = 1.20 + 1.75 + 0.75 = **3.70**. Option X wins.
**11.** 2,40,000 / 15,000 = **16 months**.
**12.** Model: *Send an Email with an Attachment (about 2 minutes).* Requirements: an email account and the file. Steps: 1. Open your email and click **Compose**. 2. Type the address in **To**. 3. Type a clear **Subject**. 4. Write the message. 5. Click the **paperclip** icon. 6. Select the file and click **Open**. 7. Wait until the file name appears under the message. 8. Click **Send**. Result: the file appears in your **Sent** folder with a paperclip. Caution: attachments larger than 25 MB cannot be sent by most services; use a link instead.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a formal definition? How is it written?**

A formal definition is a one-sentence statement of a term's meaning in the pattern *term = class + differentia*. The class is the larger group to which the thing belongs, and the differentia is the feature that separates it from other members of the group. Example: "A firewall (term) is a network security system (class) that allows or blocks traffic according to rules (differentia)." A good definition is not circular, is neither too wide nor too narrow, uses simpler words than the term, and avoids "is when" and "is where". It is used in the first mention of a term, and extended definitions build on it with examples, analogy, classification and process description.

**Q2 (5 marks). Explain the four levels of notice in instructions.**

Instructions use four notice levels. A **danger** notice warns of a hazard that will cause death or serious injury, for example live mains voltage inside a power supply. A **warning** notice describes a hazard that could cause death or serious injury, for example a swollen lithium battery. A **caution** notice marks a risk of minor injury or of damage to equipment or data, for example formatting a drive. A **note** gives helpful information that is not a hazard. Each notice states the signal word, the hazard, the consequence and how to avoid it, and is placed **before** the step it protects.

**Q3 (10 marks). Describe the structure of a formal report. Explain the purpose of each part.**

A formal report has three zones. **Front matter** helps the reader decide whether and how to read: the cover and title page identify the report; the **letter of transmittal** presents it to the person who requested it; the **abstract** (150 to 250 words) or **executive summary** (one page) gives purpose, findings and recommendation for busy readers and is written last; the **table of contents** and **lists of figures and tables** allow navigation; **acknowledgements** thank helpers. Front matter is numbered with lower-case roman numerals.

The **body**, numbered in arabic from 1, carries the argument: an **introduction** (background, problem, objectives, scope), then the method or background, the **findings or discussion** with figures and tables, **conclusions** (what the findings mean) and **recommendations** (what the reader should do). Each section has an informative heading and a topic sentence; every table and figure is numbered, captioned and cited.

The **back matter** supports the body: **references** in a consistent style, **appendices** for questionnaires, raw data and long code, a **glossary** and, in long reports, an **index**. The format is standard so that any reader can find any part quickly. Honesty rules apply throughout: data are reported as found, limits are stated and sources are cited.

**Q4 (10 marks). What is a recommendation report? Explain how criteria and a decision matrix are used and why sensitivity matters.**

A recommendation report compares options and recommends one. Its structure is introduction, criteria, options, evaluation, conclusion and recommendation. The writer first selects **criteria** that matter to the reader (for example cost, accuracy, installation time and maintenance) and gives each a **weight** that adds up to 100%. Each option is **scored** on each criterion on a common scale using evidence, the score is multiplied by the weight, and the weighted scores are added in a **decision matrix**; the highest total is the preferred option. For example, with weights 30, 30, 15 and 25, a fingerprint system scoring 3, 5, 4 and 4 totals 4.00, while RFID cards scoring 5, 3, 5 and 3 total 3.90.

Because weights are judgements, the result must be tested by a **sensitivity analysis**: raising the cost weight to 45% makes RFID cards win. If a small change of weights changes the winner, the report must say so and state which priorities lead to which choice. The report should also give a cost table that adds up, the payback period (initial cost divided by saving per period) and the feasibility tests (technical, economic, operational, schedule, legal). Presenting the evidence openly lets the reader re-do the judgement, which is the ethical core of a recommendation.

**Q5 (10 marks). Write a set of instructions to connect a laptop to a Wi-Fi network, and name the features that make it effective.**

*Connect a Laptop to the College Wi-Fi.* This takes about five minutes and gives you internet access on every floor. *You will need:* a laptop with Wi-Fi switched on, your student ID number and the password from the IT desk. **Note:** do not share your password; it is linked to your name.

1. Click the **Wi-Fi** icon in the taskbar.
2. Select **NEBians-Campus** from the list.
3. Click **Connect**.
4. Type your **student ID** in the user name box.
5. Type your **password**.
6. Click **OK** and wait ten seconds.
7. Open a browser and go to any web page.

*Result:* the icon shows **Connected** and the page loads. *Troubleshooting:* if *NEBians-Campus* is not listed, press **Fn + F2** to switch Wi-Fi on; if the password is rejected, check Caps Lock or ask the IT desk to reset it.

Features: verb-led title; introduction with time and result; requirements list; a notice; numbered steps with one action each; imperative verbs; exact names in bold; a result line; and a troubleshooting section. Before release it should be tested with a first-year student who has not done the task.

---
subject: Technical Writing
grade: BCA Semester 6
unit: 7
title: Writing for the Web, Information Reports, Proposals and Group Work
hours: 12
area: BCA 354 · Technical Writing · Unit 7
---

The TU Technical Writing outline (the same course taught to CSIT and BCA) lists several topics that Units 1 to 6 touch only briefly: **collaborative writing**, **writing for the web**, **information reports** (summary and abstract, mechanism description, periodic and progress reports, news releases), **proposals** (informal and formal), and **group presentations**. This unit supplies them, with a model document for each so that you can copy the *form*, not the words.

::: key What this unit gives you
- How to write **collaboratively** without chaos: roles, shared outline, version control, review rules.
- **Web writing**: how people read screens, page structure, headings and links, special pages (home, FAQ, about, contact).
- **Information reports**: summary versus abstract, mechanism description, periodic report, progress report, news release.
- **Proposals**: informal and formal, solicited and unsolicited, with a budget and schedule.
- Planning, rehearsing and delivering a **group presentation**.
:::

## 7.1 Writing collaboratively

Most technical documents (a requirements specification, a user manual, a project report) are written by teams. Collaboration fails in predictable ways: two people write the same section, styles clash, the last person to edit overwrites the rest, and nobody owns the final check. A good team avoids this with a small set of habits.

1. **Agree the audience, purpose and outline first** (Unit 1). Every member then writes toward the same document.
2. **Assign roles.** A *coordinator* keeps the schedule, *writers* own sections, an *editor* unifies style, and a *reviewer* checks facts and numbers. In a four-person student project one person may hold two roles.
3. **Use one style sheet.** Decide headings, number format, spelling (British or American), units, and how to cite. A one-page style sheet saves hours of editing.
4. **One master copy.** Use a shared document with edit history, or a Git repository with documents in Markdown. Never email five versions of "final.docx".
5. **Review in rounds.** Content first (is it right?), then structure, then style, then proofreading. Comment, do not silently rewrite another person's section.
6. **Set deadlines before the real deadline** and leave a day at the end for merging and checking.

| Tool | Good for | Care needed |
|---|---|---|
| Shared word processor (Google Docs, Word online) | Live co-editing and comments | Lock headings and use "suggesting" mode |
| Git with Markdown or LaTeX | Documentation next to code, history and branches | Everyone must learn pull, merge and resolve conflicts |
| Chat and issue tracker | Questions, tasks, decisions | Record decisions in the document, not only in chat |

::: tip Exam tip
Write "advantages and difficulties of collaborative writing" as two lists of four points each: *advantages* (more ideas, shared workload, better quality through review, larger documents possible); *difficulties* (conflict, uneven contribution, inconsistent style, scheduling, version confusion). Then add three practices that reduce the difficulties.
:::

## 7.2 Writing for the web

People do not read web pages the way they read printed pages. Studies of eye-tracking by the Nielsen Norman Group found that most visitors **scan**: they look for headings, bold words, bullets and links, and leave quickly if they do not find what they came for. Web writing therefore follows four rules.

| Rule | In practice |
|---|---|
| **Put the answer first** | Inverted pyramid: conclusion or the most useful fact in the first sentence; details below (compare Unit 1's pyramid). |
| **Chunk the text** | Short paragraphs of two to four sentences; one idea each; a heading every few paragraphs. |
| **Make it scannable** | Descriptive headings, bulleted lists, bold for key terms (not for whole sentences), tables for comparisons. |
| **Write for the screen** | Plain, active sentences; about half the words of the print version; avoid jargon; put the date on anything that goes out of date. |

**Getting started on a web page.** Ask: who will arrive, from where (search, link, QR code), on what device (most Nepali users are on a phone), and what single task are they trying to do? Write that task as the page's one-sentence purpose, and every other element must serve it.

**Organising and designing.** Websites are organised as a **hierarchy** (home page, sections, pages) with **navigation** that is the same on every page, so the reader always knows where they are (a *breadcrumb* trail such as Home > Courses > BCA > Semester 6 helps). Keep any page within three clicks of the home page. Use a clear **visual hierarchy**: one `h1` per page, then `h2` and `h3` in order, because screen readers and search engines use headings as the page outline. Use enough white space and large enough text (at least 16 px for body text on phones), and good colour contrast (Unit 5).

**Writing the text.**

1. **Title** that matches the words people search for ("BCA Technical Writing syllabus", not "Welcome").
2. **Summary line** under the title.
3. **Headings** that are statements or questions, not single vague nouns ("How to apply", not "Process").
4. **Link text** that says where the link goes: "download the 2025 admission form (PDF, 1.2 MB)", never "click here". This helps scanning, search engines and users of screen readers.
5. **Images** with **alt text** that describes the information in the picture, for accessibility and for slow connections.
6. **Calls to action** as verbs: *Register*, *Download*, *Contact the office*.

**Special pages.**

- **Home page.** Says in one sentence what the site is for, and shows the three to five main tasks as links. It is a *signpost*, not a brochure.
- **About page.** Who you are, what you do, evidence of credibility (years, numbers, people), and a way to contact.
- **FAQ page.** Real questions in the user's words, each with a short direct answer; group by topic; keep it updated.
- **Contact page.** Address, phone, email, office hours, a map; make email addresses and phone numbers clickable.
- **Search and error pages.** A friendly "page not found" that suggests where to go next.

A rewrite shows the effect:

| Print-style (poor on a screen) | Web-style (better) |
|---|---|
| "The college is pleased to announce that, following a meeting of the academic committee, applications for admission to the Bachelor of Computer Application programme will be accepted from the beginning of Shrawan until the middle of Bhadra." | **BCA admission open** — Apply from 1 Shrawan to 15 Bhadra. [Apply online] [Download the form] |

::: caution Cautions
Do not copy a brochure onto a page. Do not hide the contact details. Do not use text inside images, since search engines and screen readers cannot read it. Do not let pages go out of date: a page that says "Admissions 2019" damages trust.
:::

## 7.3 Information reports

An **information report** presents facts for readers who will use them to understand or decide, without arguing for a particular action. The syllabus names several forms.

### Summary and abstract

A **summary** condenses a longer document for a reader who may not read it: it states the main points in the same order and in about **one tenth** of the length. An **abstract** is a short, self-contained description that stands at the head of a paper or report (often 150 to 250 words) so that a reader can decide whether to read on. Two styles exist: a **descriptive abstract** tells what the document covers (topics, scope, method, but not results); an **informative abstract** gives the *purpose, method, key results and conclusion* in miniature. Technical papers use informative abstracts.

How to write an abstract: write the document first; then state the *problem* (one sentence), *method* (one or two), *main result with a number* (one or two), *conclusion* (one). Use past tense for what was done and present tense for what the results mean; do not cite references or add new information.

Example (informative abstract, 60 words; the figures are invented for illustration): *"Students at a Pokhara college lose about 40 minutes a day waiting for the shared computer lab. We surveyed 120 students and logged lab use for four weeks. Peak demand (10:00 to 14:00) exceeded the 40 available seats on 17 of 24 days. A booking system with 45-minute slots cut average waiting to 12 minutes in a two-week trial. We recommend adopting it."*

### Mechanism description

A **mechanism description** explains *what a device or system is, what its parts are, and how it works*. Structure: (1) an **introduction** that states what it is, its purpose and general appearance; (2) a **list of parts** in the order a reader will meet them; (3) a **description of each part** (shape, size, material, function); (4) an **explanation of how the parts work together**; (5) a **conclusion** that summarises and may mention limits. Use a labelled diagram, define each technical term, and describe in a **spatial order** (left to right, outside to inside) or a **functional order**. Compare a **process description**, which explains *how something happens* in steps (how a router forwards a packet) and uses verbs in time order, with a **set of instructions**, which tells the reader what to *do*. Typical exam subject: "describe a mouse", "describe a hard disk", "describe the working of an ATM".

### Periodic reports

A **periodic report** is written at regular intervals (weekly, monthly, quarterly, annually) in a fixed format so that readers can compare one period with the next: a monthly sales report, a quarterly server-uptime report, an annual report of a college. Its parts: **period covered**, a short **summary of highlights**, the **data** (tables and charts always in the same layout), **comments** on changes and causes, and **next steps**. The value of a periodic report comes from *consistency*: the same measures, the same units, the same order.

### Progress reports

A **progress report** tells a supervisor or client how a long task is going: what has been **done**, what is **being done**, what is **left**, what **problems** have appeared and whether the **schedule and budget** still hold. It answers "Are we on time?" and "Do you need to decide anything?" Typical parts: **introduction** (project and period), **summary** (status in two sentences), **work completed**, **work in progress**, **work remaining** with revised dates, **problems and how they are handled**, and **conclusion** (expected completion, requests). It is not a diary of effort; it is a statement of **results against the plan**.

```python
# Progress report arithmetic: percentage complete weighted by task effort
tasks = [("Requirements", 10, 100), ("Design", 15, 100), ("Coding", 40, 60), ("Testing", 25, 0), ("Documentation", 10, 30)]
total = sum(w for _, w, _ in tasks)
done = sum(w * p / 100 for _, w, p in tasks)
print("weights add to", total)
print("overall complete: %.1f%%" % (100 * done / total))
for name, w, p in tasks:
    print("%-14s weight %2d%%  done %3d%%  contributes %.1f points" % (name, w, p, w * p / 100))
```
```output
weights add to 100
overall complete: 52.0%
Requirements   weight 10%  done 100%  contributes 10.0 points
Design         weight 15%  done 100%  contributes 15.0 points
Coding         weight 40%  done  60%  contributes 24.0 points
Testing        weight 25%  done   0%  contributes 0.0 points
Documentation  weight 10%  done  30%  contributes 3.0 points
```
### News release

A **news release** (press release) is a short announcement sent to the media in the hope that it will be published. Form: a **headline** that states the news; a **dateline** (place and date); a **lead paragraph** that answers *who, what, when, where, why* in two sentences (the inverted pyramid again); **supporting paragraphs** with a quotation, facts and background in decreasing importance; a short **boilerplate** about the organisation; and **contact details** for the press. Keep it to one page, factual, free from advertising words, and ready to publish with few edits.

*Example headline and lead.* **Pokhara college launches free coding lab for school students.** *Pokhara, 12 Baisakh —* The NEBians College Computer Club will open a free evening coding lab for Grade 9 to 12 students from 1 Jestha, with 30 seats and a weekly project showcase, the college announced on Tuesday.

```svgfig label="7.1" caption="Five information-report forms placed on two questions: does the document look back or forward in time, and is it written once or at regular intervals? Abstract and news release are short and one-off; periodic and progress reports are tied to a schedule; the mechanism description explains a thing rather than a period."
f = Fig(600, 260)
f.text(300, 18, "Information reports: what each one does", size=12, color=NAVY, bold=True)
f.box(20, 36, 170, 56, "Abstract\nwhole document in 150-250 words", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(215, 36, 170, 56, "Mechanism description\nparts, then how they work", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(410, 36, 170, 56, "News release\nheadline, lead, quote, contact", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.box(70, 140, 200, 56, "Periodic report\nsame format every period", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(330, 140, 200, 56, "Progress report\ndone, doing, left, problems", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.text(300, 118, "tied to a schedule", size=10, color=NAVY, bold=True)
f.text(300, 224, "all: facts first, one idea per paragraph, numbers with units", size=10, color=NAVY)
```

## 7.4 Proposals

A **proposal** is a document that *offers to do something* and asks the reader to approve it: to fund a project, to buy a product or service, to allow a study, or to accept a student's thesis topic. It answers four reader questions: **What exactly will you do? Why is it worth doing? How and by when? What will it cost?**

| Kind | Meaning | Example |
|---|---|---|
| **Solicited** | Written in answer to a request (RFP, tender, call for projects) | A software firm answers a college's tender for a library system |
| **Unsolicited** | Written on your own initiative, so it must first *persuade the reader that there is a problem* | A student club proposes a free coding lab |
| **Informal** | Short (a letter, email or two to three pages), few parts, for a small internal or low-cost decision | Request to the principal to buy ten extra keyboards |
| **Formal** | Long, with cover letter, title page, executive summary, table of contents, and appendices, for large or external decisions | Project proposal to a donor, a bank's tender response |

### Informal proposal (letter or memo form)

Parts: **introduction** (the problem or opportunity and your proposal in one paragraph), **background** (evidence for the problem), **proposal** (what you will do, how, with a short schedule), **costs and benefits**, **conclusion** (a clear request and your contact). Typical length: one to three pages.

### Formal proposal

| Section | What it contains |
|---|---|
| Cover letter | Short note to the reader that presents the proposal and states the key benefit |
| Title page | Title, client, author, date |
| **Executive summary** | One page for the busy decision maker: problem, proposed solution, cost, timeline, benefit; write it last |
| Table of contents, list of figures | Navigation |
| **Introduction and problem statement** | Background, needs, purpose, scope |
| **Objectives** | Specific, measurable (for example "cut lab waiting time below 15 minutes by Poush") |
| **Method and work plan** | Activities, who, how, tools, deliverables |
| **Schedule** | Gantt chart or table with milestones |
| **Budget** | Itemised costs with totals and sources of funds |
| **Qualifications** | Why this team can do it: past work, skills, references |
| **Evaluation and risks** | How success will be measured; what could go wrong and the response |
| **Conclusion and request** | A call for approval |
| Appendices, references | CVs, quotations, data |

The persuasion in a proposal rests on **specifics**: not "we will improve the lab" but "we will install a booking page that reserves 45-minute slots for the 40 seats, tested for two weeks". Evidence beats adjectives, and a **budget that adds up** beats an enthusiastic one.

```python
# A proposal budget must add up: itemised costs with a 10% contingency and a check
items = [("Server and domain (1 year)", 36000), ("Developer stipend (2 students x 3 months)", 90000), ("Testing devices", 24000), ("Printing and promotion", 10000)]
subtotal = sum(c for _, c in items)
contingency = round(subtotal * 0.10)
total = subtotal + contingency
for n, c in items:
    print("%-45s Rs %8d" % (n, c))
print("%-45s Rs %8d" % ("Subtotal", subtotal))
print("%-45s Rs %8d" % ("Contingency (10%)", contingency))
print("%-45s Rs %8d" % ("TOTAL REQUESTED", total))
```
```output
Server and domain (1 year)                    Rs    36000
Developer stipend (2 students x 3 months)     Rs    90000
Testing devices                               Rs    24000
Printing and promotion                        Rs    10000
Subtotal                                      Rs   160000
Contingency (10%)                             Rs    16000
TOTAL REQUESTED                               Rs   176000
```
::: tip Exam tip
"Write a proposal to your principal for a Wi-Fi network in the library" is a favourite. Use this skeleton: heading and date, salutation, *Introduction* (problem and request), *Background* (what exists, what is wrong, evidence), *Proposal* (what, where, how), *Schedule and cost* (a small table), *Benefits*, *Conclusion* (request approval, offer a meeting). Keep it under one page and make the cost visible.
:::

## 7.5 Group presentations

A group presentation (Unit 2 of BCA 105 covered single speakers; here the problem is *several* speakers) is judged as one performance, so the audience should never be able to see the seams.

1. **Plan together.** One shared message ("a booking system fixes the lab queue") and a time split. For a 15-minute talk with four speakers allow about 2 minutes each for content, 2 minutes for the shared opening and 3 minutes for the shared close and questions.
2. **Divide by topic, not by slide count.** Each speaker owns one part of the story (problem, method, result, recommendation), so transitions follow logic.
3. **Use one design.** One slide template, one font, one colour scheme (Unit 5).
4. **Plan the hand-offs.** End each part with a sentence that introduces the next speaker: "Now Sita will show how we tested it."
5. **Rehearse as a group, with a timer**, at least twice, including the technical set-up (laptop, adapter, clicker, backup copy on a USB stick).
6. **Stand and behave as a team.** Speakers who are not talking face the audience, do not whisper or look at their phones, and stay out of the projector beam.
7. **Plan questions.** Decide who answers which kind of question; say "I will let Ram answer that, it is his area."
8. **Deliver, then review.** After the talk, note one thing to keep and one to change.

| Stage | Output |
|---|---|
| Planning | Message, audience, time, roles |
| Organising and composing | Outline, slides, speaker notes |
| Preparing | Handouts, backup file, room check |
| Rehearsing | Two timed runs, trimmed to time |
| Presenting | Hand-offs, eye contact, questions handled |

## Formula and fact sheet

- Collaborative writing: shared outline, roles, one style sheet, one master copy, review in rounds.
- Web: answer first, chunk, scan, short; link text names the destination; alt text for images; one `h1`, ordered headings.
- Summary about 1/10 of the original; abstract 150 to 250 words (descriptive or informative).
- Mechanism description: introduction, parts, each part, working, conclusion. Process description is in time order.
- Progress report: done, doing, left, problems, schedule/budget status, request.
- News release: headline, dateline, lead (5 Ws), quote, boilerplate, contact.
- Proposal: problem, objectives, method, schedule, budget, qualifications, evaluation, request. Solicited versus unsolicited; informal versus formal.

## Chapter summary

- Team writing works when roles, a style sheet and a single master copy are fixed in advance and reviews happen in rounds.
- Web readers scan, so pages put the answer first, use headings and lists, and give links and images descriptive text.
- Information reports (abstracts, mechanism and process descriptions, periodic and progress reports, news releases) present facts in a fixed form for a defined reader.
- Proposals persuade with specific objectives, a plan, a schedule and a budget that adds up.
- A group presentation needs one message, divided topics, planned hand-offs and joint rehearsal.

## Practice

1. List four advantages and four difficulties of collaborative writing.
2. Why do readers scan web pages, and how should a writer respond? Give five rules.
3. Rewrite as web text: "It is hereby notified for the information of all students that the examination routine has been published and may be consulted on the college notice board and website."
4. Differentiate between a descriptive and an informative abstract.
5. Write a mechanism description (about 150 words) of a computer mouse.
6. Distinguish a periodic report from a progress report.
7. In a progress report the tasks Design (weight 20%, 100% done) and Coding (weight 50%, 40% done) and Testing (weight 30%, 0% done) are given. Compute the overall percentage complete.
8. Write the lead paragraph of a news release announcing a college hackathon.
9. Differentiate solicited and unsolicited, informal and formal proposals.
10. A budget has items of Rs 45,000, Rs 30,000 and Rs 15,000 and a 10% contingency. What is the total requested?

::: note Answers and worked solutions
**1.** Advantages: more ideas, shared workload, better quality through peer review, larger documents possible. Difficulties: conflict, uneven contribution, inconsistent style, version confusion and scheduling.
**2.** Readers scan because they want a specific answer fast and screens tire the eye. Rules: answer first; short chunks; descriptive headings, lists and bold key terms; plain words and about half the print length; descriptive link text and alt text.
**3.** "**Exam routine published.** See the college notice board or [download the routine (PDF)]." (Short, answer first, descriptive link.)
**4.** A descriptive abstract tells what the document covers (topics and scope) without results; an informative abstract states the purpose, method, main results and conclusion in miniature.
**5.** Model: "A computer mouse is a hand-held pointing device about 10 cm long that moves a cursor on the screen. It has a plastic shell, two buttons and a scroll wheel on top, an optical sensor and an LED underneath, and a cable or wireless transmitter. The sensor photographs the surface thousands of times a second; the chip compares the images to find the direction and distance moved and sends them to the computer, which moves the cursor. Pressing a button closes a switch, which the computer reads as a click." (Introduction, parts, working, conclusion.)
**6.** A periodic report is written at set intervals in a fixed format to compare periods; a progress report is written during one project to show results against the plan and flag problems.
**7.** 20 x 1.00 + 50 x 0.40 + 30 x 0 = 20 + 20 + 0 = **40% complete**.
**8.** "**Kathmandu, 5 Magh —** NEBians College will hold its first 24-hour hackathon on 20 and 21 Falgun, inviting teams of up to four BCA and CSIT students to build solutions for local problems, the organisers announced on Monday. Registration closes on 10 Falgun." 
**9.** Solicited answers a request or tender; unsolicited is initiated by the writer and must first prove the need. Informal is a short letter or memo for small decisions; formal has cover letter, executive summary and sections for large decisions.
**10.** Subtotal 90,000; contingency 9,000; total Rs 99,000.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a progress report? Describe its contents.**

A progress report informs a supervisor, client or sponsor about the state of a task during its execution, comparing results with the plan. Its parts are: (1) **introduction**: project and period covered; (2) **summary**: overall status and whether it is on time and within budget; (3) **work completed**; (4) **work in progress**; (5) **work remaining** with revised dates; (6) **problems** and how they are being solved; (7) **conclusion** with the expected completion and any decision requested. It uses numbers (percentage complete, money spent) and is written for a reader who has little time.

**Q2 (10 marks). What is a proposal? Explain the types and write the structure of a formal proposal.**

*Definition.* A proposal offers to do work and asks the reader to approve it. *Types.* Solicited and unsolicited; informal and formal (table in Section 7.4). *Structure.* Cover letter, title page, executive summary, contents, introduction and problem, objectives, method and work plan, schedule, budget, qualifications, evaluation and risk, conclusion and request, appendices. *Persuasion.* Explain that specific objectives, a realistic schedule and a budget that adds up convince the reader more than praise. *Example.* The booking-system proposal for the computer lab, with a budget of Rs 1,76,000 including a 10% contingency (subtotal Rs 1,60,000 plus Rs 16,000) (the Python block above gives the itemised sum).

**Q3 (5 marks). Explain the principles of writing for the web.**

(1) Put the answer first (inverted pyramid). (2) Chunk text into short paragraphs under informative headings. (3) Make the page scannable with lists, bold key terms and tables. (4) Write plainly and briefly for the screen. (5) Give links descriptive text and images alt text. (6) Keep navigation consistent and pages within three clicks of the home page. (7) Use special pages (home, FAQ, about, contact) for their jobs.

**Q4 (5 marks). Describe a mechanism, with the structure of a mechanism description.**

A mechanism description explains what a device is, what parts it has and how they work together. Structure: introduction (what, purpose, appearance), list of parts, description of each part (shape, size, material, function), an account of how the parts work together, and a conclusion. A labelled diagram and defined technical terms are essential. A process description, by contrast, narrates the steps of something that happens; instructions tell the reader what to do.

---
subject: Technical Writing
grade: BCA Semester 6
unit: 1
title: Audience, Purpose and the Writing Process
hours: 5
area: BCA 354 · Technical Writing · Unit 1
---

A system administrator once wrote a one-line message for the whole office: "The server will be down for scheduled maintenance." Fifty people read it. The accountant did not know whether to save her work, the teacher did not know which day, and the developer wanted to know *which* server. Every word was correct, and the message failed. **Technical writing** is the discipline of conveying technical information so that a particular reader can *do something* with it: install, decide, fix, approve, learn. It is not decoration added at the end of an engineering task; it is part of the task. This unit sets out how to decide *who* you are writing for and *why*, and a repeatable process (plan, draft, revise, test) for producing documents that work.

::: key What this unit gives you
- What makes writing technical: accuracy, clarity, concision, accessibility, and the reader's task.
- Audience and purpose analysis; the pyramid structure; outlining.
- The writing process and revision passes; document design basics.
- Measuring documents by testing them with readers.
:::

## 1.1 What is technical writing?

Technical writing communicates specialised information to a defined audience for a practical purpose. Its marks (the "seven Cs" in many textbooks) are: **clear**, **concise**, **correct**, **complete**, **coherent**, **courteous** and **concrete**. It differs from literary writing: the reader reads to *use* the text, often in a hurry, often while doing something else, so the writer's job is to reduce the reader's effort. Typical products: user manuals, API reference, requirements specifications, README files, installation guides, lab and test reports, project proposals, emails to clients, release notes, policies, error messages and interface text, and research papers.

| Literary writing | Technical writing |
|---|---|
| Purpose: to move, entertain, explore | Purpose: to inform, instruct, persuade, record |
| Reader reads for pleasure | Reader reads to act |
| Ambiguity can be a virtue | Ambiguity is a defect |
| Style is personal | Style follows conventions and house style |
| Success: the reader feels | Success: the reader succeeds at the task |

Poor technical writing has a real cost: an unclear configuration step wastes a day, an ambiguous requirement leads to the wrong system, an unreadable error message floods the help desk. In safety-related fields a misread instruction can cause injury.

## 1.2 Know your audience

Before writing, answer: **Who will read this? What do they already know? What do they need to do with it? In what situation will they read it?** Classify the audience by technical level:

| Reader type | Knows | Needs | Write like this |
|---|---|---|---|
| **Layperson / end user** | Nothing technical | Steps to complete a task | Plain words, numbered steps, screenshots, no jargon |
| **Technician / operator** | Tools of the trade | Procedures, settings, troubleshooting | Precise steps, tables of parameters, warnings |
| **Expert / peer** | The theory | Details, evidence, methods | Terms of art allowed, equations, references |
| **Manager / executive** | The business | Decisions, costs, risks, deadlines | Summary first, numbers, recommendation |
| **Mixed audience** | Varied | Different parts for different readers | Layered document: summary, body, appendices |

Most documents have **several audiences**: the *primary* reader acts on the document; *secondary* readers (reviewers, auditors, the next maintainer) read it later. Write the main text for the primary reader and put the detail for others in appendices or links. **Cultural and language factors** matter in Nepal: many readers read English as a second language, so prefer short sentences, common words, consistent terms, and avoid idioms ("touch base", "ballpark") and humour that does not translate; provide Nepali text where the reader needs it (forms, public notices, safety warnings); and use units, date formats (say "15 Baisakh 2082 (28 April 2025)" when it matters) and currency (Rs, with the lakh/crore grouping used in Nepal) consistently.

A quick **audience profile** form: role; technical background; reading goal; reading environment (desk, field, phone); time available; attitude (supportive, sceptical, hurried); language level; what they will do next. Writing for "everyone" produces a document for no one.

## 1.3 Define the purpose

State the purpose in **one sentence** before drafting: "After reading this, the ward officer will be able to approve or reject the server purchase by Friday." A purpose has a verb: *instruct* (how to do), *inform* (what is), *explain* (why), *persuade* (decide for), *record* (what happened), *request*. If you cannot write the sentence, you are not ready to write. The same facts yield different documents for different purposes: for a **user guide** the facts are arranged as tasks; for a **proposal**, as problem, solution, cost, benefit; for a **report**, as what was done, found, concluded.

Also decide the **scope** (what is in and out), the **format** (email, PDF, web page, wiki, slides, printed sheet), the **length** (the reader's time), and the **deadline**.

## 1.4 Organise: the pyramid and the outline

Readers read from the top and stop when they have what they need, so use the **inverted pyramid** (borrowed from journalism): put the **conclusion, recommendation or most important result first**, then the supporting details in decreasing importance. A business-style report begins with a **summary** (the answer in 3–5 sentences), then background, details and appendices. A manual is organised by **task**, not by program feature ("How do I print a certificate?" rather than "The Print menu").

Common patterns of organisation:

- **Chronological / procedural** (steps in order): installation, procedures, incident reports.
- **Spatial** (by location): hardware descriptions, network diagrams.
- **General to specific / specific to general:** concepts, then examples.
- **Problem – cause – solution:** troubleshooting guides, proposals.
- **Comparison / alternatives:** feasibility studies and evaluations (criteria, options, recommendation).
- **Order of importance:** summaries and emails.

An **outline** is a hierarchical plan (headings and one-line notes) written before the text. It exposes gaps and order problems cheaply. Use **parallel structure** in headings (all noun phrases or all verb phrases). **Chunk** information: groups of five to nine items, headings every few paragraphs, short paragraphs (three to five sentences, one idea each), lists for items and numbered lists for steps, tables for comparisons.

## 1.5 The writing process

A reliable process has five stages, repeated as needed:

1. **Plan:** audience, purpose, scope, outline, collect facts (interview experts, run the procedure yourself, capture screenshots).
2. **Draft:** write fast without editing; get the content down; mark gaps ("[CHECK PORT NUMBER]") instead of stopping.
3. **Revise:** change *content and structure* (global); is the answer first? Is anything missing or redundant? Does each section serve the purpose?
4. **Edit:** change *sentences and words* (local) for clarity, concision and consistency; then **proofread** for spelling, punctuation, numbers and formatting.
5. **Test and publish:** have someone from the audience *use* the document, then fix what failed; version and date it; plan updates.

**Revision passes.** Do separate passes, because the eye cannot check everything at once: (1) *structure and completeness*; (2) *accuracy* (verify every number, command, name; run the commands); (3) *clarity and concision*; (4) *consistency* (terms, capitalisation, units, tense); (5) *format and links*; (6) *proofreading*, ideally after a break, aloud or backward. Reading aloud reveals long sentences; a second reader reveals assumptions. Keep a **style guide** (even one page) for terminology and conventions: a team that writes "log in", "login" and "sign-in" for the same action confuses readers.

## 1.6 Document design

Design helps reading: **headings** that tell what the section answers, **white space**, a readable **typeface** (a sans-serif at 10–12 pt for screens, a serif acceptable for print), **consistent formatting** (bold only for user-interface labels, `monospace` for code and commands), **visual hierarchy**, and **alignment**. **Warnings** use a standard label and come *before* the step they relate to: **Danger** (serious injury or data loss), **Warning**, **Caution**, **Note**. Number steps, give one action per step, start with a verb ("Click **Save**"), state the expected result ("The message *Saved* appears"), and put conditions *before* actions ("If you have a USB drive, insert it"). **Accessibility:** provide text alternatives for images, do not rely on colour alone, ensure sufficient contrast (Unit 5), use real headings and lists so that screen readers can navigate.

## 1.7 Testing documents with readers

The test of a document is whether readers succeed. **Usability testing:** give a representative reader the document and a task, watch silently, and note where they hesitate or err; five readers reveal most problems. **Walkthrough:** the writer follows the instructions on a clean machine. **Peer review:** a colleague checks accuracy and clarity; the Unit 2 readability scores supply a rough numeric check. **Feedback loop:** collect questions that reach the help desk; every repeated question marks a defect in the documentation. Treat documentation like software: version it, review it, track issues against it, and keep it close to the thing it describes (documentation as code, in the same repository).

## 1.8 Seeing the ideas: tools, manuals, signs and the shape of a message

```photogrid label="1.1" cols="3" ratio="1.0" caption="Technical writing is older than computers and lives everywhere. (a) An Olympia Simplex typewriter of 1935: for a century, offices drafted letters and manuals on machines like this, so the habit of short, ordered paragraphs began here. (b) A 2007 car owner's manual: a document read in a hurry, by a layperson, to act safely. (c) A tsunami hazard sign: a picture and one instruction, readable in two seconds by a person who is running."
@ photo id="bca354/typewriter" cap="Typewriter, 1935"
fit 1.0
focus 0.5 0.5
@ photo id="bca354/manual" cap="Owner's manual"
fit 1.0
focus 0.4 0.5
@ photo id="bca354/warning" cap="Hazard sign"
fit 1.0
focus 0.5 0.4
```

```svgfig label="1.1" caption="The inverted pyramid. The conclusion goes first and the detail follows in decreasing importance, so a reader who stops after any layer still leaves with the most important facts."
f = Fig(580, 236)
L = [("Conclusion and recommendation", 20, 340, 50, 310, MINT, TEAL), ("Key reasons and figures", 50, 310, 80, 280, BLUE, NAVY), ("Supporting details", 80, 280, 110, 250, SAND, AMBER), ("Background", 110, 250, 140, 220, ROSE, RED)]
for i, (t, a, b, c, d, fl, st) in enumerate(L):
    y = 12 + i * 52
    f.poly([(a, y), (b, y), (d, y + 50), (c, y + 50)], fill=fl, stroke=st, label=t, lx=180, ly=y + 25, size=10.5, color=NAVY)
notes = ["A reader with 30 seconds\nstops here", "A reader who must act\nreads this far", "A specialist checking the\nwork reads this far", "An auditor or newcomer;\ncan go in an appendix"]
for i, t in enumerate(notes):
    y = 12 + i * 52
    f.arrow([(350, y + 25), (385, y + 25)], color=SLATE)
    f.text(392, y + 25, t, size=11, color=SLATE, anchor="start", vmid=True)
f.text(180, 228, "most important at the top", size=10.5, color=SLATE, italic=True)
```

```svgfig label="1.2" caption="The writing process is a loop, not a line. Testing with a real reader sends the writer back to planning or revising; each pass has one job."
f = Fig(580, 150)
S = [("1 Plan", "audience,\npurpose,\noutline", MINT, TEAL), ("2 Draft", "write fast,\nmark gaps", BLUE, NAVY), ("3 Revise", "structure,\ncontent", SAND, AMBER), ("4 Edit", "words,\nsentences", ROSE, RED), ("5 Test", "a real reader\nuses it", MINT, TEAL)]
for i, (t, d, fl, st) in enumerate(S):
    x = 14 + i * 114
    f.box(x, 14, 96, 36, t, fill=fl, stroke=st, bold=True, size=12.5)
    f.text(x + 48, 76, d, size=10.5, color=SLATE)
    if i < 4: f.arrow([(x + 96, 32), (x + 114, 32)])
f.arrow([(534, 98), (534, 120), (62, 120), (62, 100)], color=RED, dash=True, label="what failed in the test sends you back", lpos=(300, 136))
```

### 1.8.1 Eight habits of effective technical writers

1. **Start from the reader.** Write a one-line profile of the reader before the first sentence. A Nagarik App help page for a villager needs different words from the same page written for the app's developers. Most bad documents are written for the author, not for the person who must use them.
2. **Put the answer first.** Open with the decision, the result or the warning, and add detail after it. A ward officer reading a purchase request wants "approve the NPR 4.2 lakh server" before the background. Inverted pyramids respect the reader's time.
3. **Use the reader's words.** Choose the term your audience already uses and keep it the same everywhere. If one page says "log in", the next says "sign in" and a third says "authenticate", a beginner thinks three actions are needed. A short glossary fixes this for ConnectIPS or Fonepay guides.
4. **Write one idea per paragraph.** Keep paragraphs to three to five sentences with the main point in the first one. A screen full of text is skipped, while short chunks are scanned. Headings that ask or answer a question help the eye find the part it needs.
5. **Number steps and list items.** Steps that must happen in order get a numbered list, one action per step. Items with no order get bullets. The steps to renew a licence at the Department of Transport Management are easy to follow when each line starts with a verb.
6. **Place warnings before the step.** A warning after the action is too late. Name the danger, the result and how to avoid it, in a consistent box. The tsunami sign works because the instruction is short and the picture needs no translation.
7. **Show, do not only tell.** A screenshot, table or diagram can replace a long paragraph, and a worked example turns a rule into something the reader can copy. Label every figure and refer to it in the text.
8. **Test, revise and date.** Let one person from the audience try the document while you watch silently. Fix what they stumble on, then record the version and date so readers know it is current. A manual that nobody tested is only a guess.

## Chapter summary

- Technical writing serves the reader's task; qualities are clarity, concision, correctness, completeness, coherence, courtesy and concreteness.
- Profile the audience (knowledge, task, environment, language) and state the purpose in one sentence with a verb.
- Put the answer first (inverted pyramid), organise by the reader's tasks, use outlines, chunking, lists and tables.
- Process: plan, draft, revise, edit and proofread in separate passes, then test with real readers.
- Design (headings, warnings, steps, accessibility) is part of the message.

## Practice

1. Define technical writing and give three differences from literary writing.
2. Create an audience profile for a guide to resetting a password for a school's office staff.
3. Rewrite as a purpose sentence: "This document is about the new backup system."
4. Why is the inverted pyramid used for reports and emails?
5. Name four patterns of organisation and a document type for each.
6. List the stages of the writing process.
7. Why should the writer draft first and edit later?
8. Rewrite the step "The Save button should be clicked in order to save" as a good instruction.
9. Where should a warning be placed relative to the step it concerns?
10. How would you test a user manual?

::: note Answers and worked solutions
**1.** Communicating specialised information so the reader can act. Differences: purpose (inform and instruct versus entertain), ambiguity (a defect, not a virtue), success (reader completes the task).
**2.** Role: office clerks; background: basic computer skills, no IT; goal: regain access quickly; environment: office desk, possibly stressed; time: minutes; language: Nepali/English mix; next action: log in and continue work. So use short numbered steps with screenshots and plain words.
**3.** "After reading this, staff will be able to restore a file from last night's backup in under five minutes."
**4.** Readers stop reading when they have what they need; putting the conclusion first serves hurried readers and decision-makers.
**5.** Chronological (installation guide); problem–cause–solution (troubleshooting guide); comparison (feasibility study); order of importance (executive summary or email).
**6.** Plan, draft, revise, edit/proofread, test and publish.
**7.** Editing while drafting slows the flow and wastes effort on text that may be cut; drafting first gets the content down.
**8.** "Click **Save**."
**9.** Before the step, so the reader sees it before acting.
**10.** Give a representative user a real task and observe where they hesitate or fail; follow the steps on a clean machine; fix and retest.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Define technical writing and distinguish it from literary writing.**

*Definition.* **Technical writing** communicates specialised information to a defined audience for a practical purpose: to instruct, inform, explain, persuade or record. The reader reads in order to *act*, so success is measured by whether the reader can do the task (Plate 1.1 shows an owner's manual and a hazard sign, both read in a hurry).

*Qualities.* Good technical writing is clear, concise, correct, complete, coherent, courteous and concrete. A wrong port number in an installation guide, for example, can waste a whole day.

*Differences.*

| Point | Literary writing | Technical writing |
|---|---|---|
| Purpose | to move or entertain | to inform, instruct, record |
| Reader | reads for pleasure | reads to do something |
| Ambiguity | may be a virtue | is a defect |
| Style | personal | follows house style and conventions |
| Success | the reader feels | the reader succeeds at the task |

*Example.* A poem about a river may be read in many ways, but the instruction "Press and hold the power button for five seconds" must be read in only one. *Conclusion:* technical writing is judged by the reader's success, literary writing by the reader's response.

**Q2 (5 marks). Explain audience analysis. How would you write the same message for a layperson and for a manager?**

*Audience analysis* means answering four questions before drafting: who will read, what do they already know, what must they do with the text, and in what situation will they read it. Readers are classed as layperson, technician, expert, manager or mixed, and most documents have a *primary* reader who acts and *secondary* readers who review or maintain.

*Profile form.* Role, technical background, reading goal, environment (desk, field, phone), time available, attitude, language level and next action.

*Same message, two readers.* Suppose a college server will be replaced.

| For | Write like this |
|---|---|
| Layperson (student) | "The college website will be offline on Saturday from 6 to 9 pm. Please finish uploading assignments before then." Plain words, date and time first, no jargon. |
| Manager (principal) | "Approve NPR 4.2 lakh to replace the failing server. Risk if delayed: a fee-collection outage in admission season. Decision needed by Friday." Recommendation first, cost, risk, deadline. |

*Nepali context.* Many readers use English as a second language, so use short sentences and consistent terms. *Conclusion:* the facts stay the same, but the order, vocabulary and detail change with the reader.

**Q3 (10 marks). Describe the technical-writing process in detail. Explain planning, the inverted pyramid and the testing of a document.**

*Introduction.* Technical documents are produced by a repeatable process rather than by inspiration. A reliable process has five stages, repeated as needed, as in Figure 1.2: **plan, draft, revise, edit, test**.

*The stages.*

1. **Plan.** Profile the audience, write the purpose in one sentence with a verb ("After reading this, the ward officer can approve or reject the purchase by Friday"), fix scope, format, length and deadline, and make an outline. Collect facts by interviewing experts and running the procedure yourself.
2. **Draft.** Write quickly without editing and mark gaps such as [CHECK PORT NUMBER] instead of stopping.
3. **Revise.** Change structure and content: is the answer first, is anything missing, does each section serve the purpose?
4. **Edit.** Change words and sentences for clarity and concision, then proofread spelling, numbers and formatting.
5. **Test and publish.** Ask a representative reader to perform a task with the document while you watch silently; five readers expose most defects. Version and date the final text.

*The inverted pyramid (Figure 1.1).* Readers read from the top and stop when they have enough, so the conclusion or recommendation comes first, then the key reasons, then supporting detail, and last the background or appendices. A report therefore starts with a three-to-five sentence summary. A manual is organised by *task* ("How to renew a licence") rather than by program menu.

*Organisation patterns.* Chronological (procedures), spatial (hardware), general to specific, problem-cause-solution (troubleshooting), comparison (feasibility studies) and order of importance (summaries, e-mails).

*Revision passes.* Do separate passes for structure, accuracy, clarity, consistency, format and proofreading, because the eye cannot check everything at once. Reading aloud exposes long sentences.

*Testing.* A usability test, a walkthrough on a clean machine and a peer review each find different defects; the readability scores of Unit 2 add a rough numeric check.

*Comparison of drafting styles.*

| Aspect | Writer-centred draft | Reader-centred draft |
|---|---|---|
| Opening | history and background | decision or key result |
| Order | order of discovery | order of importance or task |
| Words | writer's jargon | reader's vocabulary |
| Check | writer rereads | a reader performs the task |

*Conclusion.* A staged process, an answer-first structure and a real reader test turn a collection of facts into a document that works.

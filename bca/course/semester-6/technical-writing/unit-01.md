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

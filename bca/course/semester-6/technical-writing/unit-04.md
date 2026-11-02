---
subject: Technical Writing
grade: BCA Semester 6
unit: 4
title: Research Proposals, Academic Writing and Citation
hours: 8
area: BCA 354 · Technical Writing · Unit 4
---

Every BCA student eventually writes a project proposal, a literature review or a final-year report, and the readers (a supervisor, a committee, an examiner) judge it by the same tests: is the problem clear, is the method sound, is the evidence honestly sourced? This unit covers the structure of a research proposal, the IMRaD paper, the abstract, the literature review, citation styles with an executed formatter for APA and IEEE references, and academic integrity, including a small executed **similarity** measure that shows why copying with a few words changed is easy to detect while a genuine paraphrase is not flagged.

::: key What this unit gives you
- Proposal and report structure; research questions and objectives; the abstract.
- The literature review as synthesis; the IMRaD format.
- Citation and reference styles (APA, IEEE) with an executed example; reference managers.
- Quoting, paraphrasing, summarising; plagiarism and similarity; responsible use of AI tools.
:::

## 4.1 The research proposal

A **proposal** persuades a reader that a problem deserves work, that you know what has been done, and that your plan can be completed. A typical BCA project or research proposal has:

| Section | Answers | Tips |
|---|---|---|
| **Title** | What is it about? | Specific, under about 15 words, no "Study of" padding |
| **Abstract / summary** | The whole thing in 150–250 words | Write last |
| **Introduction and problem statement** | Why does this matter, and what exactly is the problem? | Context, gap, significance; local relevance (Nepal) |
| **Objectives / research questions** | What will you find out or build? | Verbs: *measure, compare, design, evaluate*; SMART (specific, measurable, achievable, relevant, time-bound) |
| **Literature review** | What is known; what is missing? | Group by theme; end with the gap |
| **Methodology** | How will you do it? | Data sources, tools, algorithm, evaluation metrics, ethics |
| **Scope and limitations** | What will you *not* do? | Honest boundaries |
| **Work plan / timeline** | When? | Gantt chart with milestones |
| **Budget / resources** | What is needed? | Hardware, data, software, time |
| **References** | Where did the ideas come from? | One style, all cited works |

A good **problem statement** is specific and evidence-based: "Ward offices in the three municipalities issue about 400 recommendation letters a week by hand, taking an average of 25 minutes each; this study designs and evaluates a web system to cut the time to under 5 minutes" is better than "Manual processes are slow." **Research questions** must be answerable: "Does the system reduce the processing time per letter compared with the manual process?" **Objectives** are the steps to answer them. For a software project add *deliverables* and *acceptance criteria* that tie to the requirements of Unit 3.

## 4.2 The structure of a paper or report: IMRaD

Research papers in computing and the sciences follow **IMRaD**: **I**ntroduction (problem, motivation, contribution), **M**ethods (enough detail to repeat the work), **R**esults (what you found, with tables and figures; no interpretation), **a**nd **D**iscussion (what it means, limitations, future work), then **conclusion** and **references**. A final-year report adds a title page, acknowledgement, abstract, table of contents, list of figures and tables, and appendices (code listings, questionnaires). Rules: every figure and table is numbered, captioned and *referred to in the text*; every claim is supported by your data or a citation; the conclusion answers the research questions and introduces nothing new.

### The abstract

An abstract is a self-contained summary read far more often than the paper. A **structured abstract** has five parts in 150–250 words: **background** (one sentence), **objective**, **method**, **main results (with numbers)** and **conclusion**. Example: "Ward offices spend about 25 minutes producing each recommendation letter. We built a web system for letter issue and evaluated it in two ward offices over four weeks. The mean time fell from 25.1 to 4.3 minutes (n = 312 letters), and staff satisfaction rose from 2.9 to 4.4 on a five-point scale. A simple web system can cut processing time by over 80% in small offices." Avoid references, abbreviations and claims not in the paper.

## 4.3 The literature review

A literature review is not a list of summaries; it is an **argument about what is known**. Steps: define the search (keywords, databases such as IEEE Xplore, ACM Digital Library, Google Scholar, Scopus, with date limits); read the abstracts, then the relevant papers; record each source in a **table** (authors, year, problem, method, data, findings, limitations); then **group by theme** and write by theme, comparing and contrasting sources ("Both Sharma (2021) and Thapa (2022) report faster approvals, but only Thapa measured error rates") and ending with the **gap** that your work fills. Prefer primary, peer-reviewed sources and recent work; evaluate quality (sample size, method, venue); and distinguish *your* voice from the sources'.

## 4.4 Citing sources

A **citation** in the text points to an entry in the **reference list**. Citations give credit, let readers check, and show the work's foundation. Choose the style your institution requires and apply it consistently.

| Style | In-text | Reference list order | Typical field |
|---|---|---|---|
| **IEEE** | Numbers in brackets: "as shown in [1]" | Order of first citation | Engineering, computing |
| **APA (7th)** | Author–date: "(Rivest et al., 1978)" | Alphabetical by author | Social sciences, education, information systems |
| **Harvard** | Author–date: "(Rivest et al. 1978)" | Alphabetical | Business, general |

The program below stores one reference as data and produces both an APA and an IEEE entry, which is how reference managers (Zotero, Mendeley, BibTeX with LaTeX) work: keep the *data* once and let software format it. (Plain text here; in real documents the journal name and volume are set in italics.)

```python
refs = [
    {"authors": [("Rivest", "R."), ("Shamir", "A."), ("Adleman", "L.")], "year": 1978,
     "title": "A method for obtaining digital signatures and public-key cryptosystems",
     "journal": "Communications of the ACM", "vol": 21, "no": 2, "pages": "120-126"},
]

def apa(r):
    names = [last + ", " + ini for last, ini in r["authors"]]
    who = ", ".join(names[:-1]) + ", & " + names[-1]
    return "%s (%d). %s. %s, %d(%d), %s." % (
        who, r["year"], r["title"], r["journal"], r["vol"], r["no"], r["pages"].replace("-", "–"))

def ieee(r):
    names = [ini + " " + last for last, ini in r["authors"]]
    who = ", ".join(names[:-1]) + ", and " + names[-1]
    return '%s, "%s," %s, vol. %d, no. %d, pp. %s, %d.' % (
        who, r["title"], r["journal"], r["vol"], r["no"], r["pages"].replace("-", "–"), r["year"])

print(apa(refs[0]))
print(ieee(refs[0]))
```
```output
Rivest, R., Shamir, A., & Adleman, L. (1978). A method for obtaining digital signatures and public-key cryptosystems. Communications of the ACM, 21(2), 120–126.
R. Rivest, A. Shamir, and L. Adleman, "A method for obtaining digital signatures and public-key cryptosystems," Communications of the ACM, vol. 21, no. 2, pp. 120–126, 1978.
```
Differences to notice: APA puts the *year* after the authors and capitalises only the first word of the title; IEEE uses initials before surnames, quotation marks around the title and abbreviations (*vol.*, *no.*, *pp.*). Cite **web pages** with author, year, title, site and URL with access date; **software** and **datasets** with version and DOI; and give a **DOI** when one exists. Do not cite what you have not read; if you rely on a secondary source, say so.

## 4.5 Plagiarism and academic integrity

**Plagiarism** is presenting someone else's words, ideas, data or code as your own. Forms: copying text without quotation marks and citation; *patchwork* copying with a few words changed; paraphrasing without credit; submitting someone else's work or code; self-plagiarism (reusing your earlier submission without permission); inventing or altering data. Consequences range from failing the assignment to dismissal; for professionals, loss of reputation and legal liability under copyright (Unit 4 of *Society and Technology*).

The three legitimate ways to use a source, all **with a citation**:

- **Quote:** exact words in quotation marks (short) or a block quote (long), only when the wording itself matters.
- **Paraphrase:** restate the *idea* in your own words and structure at similar length; changing a few words is not paraphrase.
- **Summarise:** a shorter statement of the main points.

**Common knowledge** (the earth orbits the sun, TCP is a transport protocol) needs no citation, but when unsure, cite. **Code:** reuse is fine when the licence allows it; keep the licence notice, cite the source in a comment, and do not present copied code as your own work.

Detection software compares your text with a database; a rough way to see how it works is **shingling**: split each text into overlapping word triples (3-grams) and compute the **Jaccard similarity** |A ∩ B| / |A ∪ B| of the two sets. The program compares a source sentence with a copy that changes the ending, and with a genuine paraphrase.

```python
def shingles(text, k=3):
    w = text.lower().replace(".", "").replace(",", "").split()
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}

def jaccard(a, b):
    A, B = shingles(a), shingles(b)
    return len(A & B) / len(A | B)

source = "Public key cryptography removes the need for two parties to share a secret key in advance."
copied = "Public key cryptography removes the need for two parties to share a secret key beforehand."
paraphrase = "Two strangers can communicate securely with asymmetric cryptography because no secret has to be exchanged first."
print("copy: %.2f  paraphrase: %.2f" % (jaccard(source, copied), jaccard(source, paraphrase)))
```
```output
copy: 0.80  paraphrase: 0.00
```
The lightly edited copy scores high (most triples are identical), and the paraphrase scores zero because it shares no three-word sequence with the source. Real checkers use more sophisticated methods and cannot judge whether a low score hides stolen *ideas*; they provide a screening score that a human must interpret, and a high score for properly quoted and cited passages is not misconduct.

**Using AI tools.** Text and code generators can help with brainstorming, outlines, language polishing and explanation, but they can also **invent facts and references** that look real. Follow your institution's policy; **disclose** what you used and how; **verify every claim and every citation** against the original; never submit generated text as your own analysis; and remember that you remain responsible for the accuracy of what you submit.

## Chapter summary

- A proposal states a specific problem, answerable research questions, a review ending in a gap, a method, scope, timeline and references.
- Papers follow IMRaD; a structured abstract has background, objective, method, results with numbers and conclusion.
- A literature review synthesises by theme; record sources in a table.
- Cite in one consistent style (IEEE numeric, APA author–date); store reference data once and let tools format it.
- Quote, paraphrase or summarise *with citation*; patchwork copying is plagiarism; similarity scores screen, humans judge; disclose and verify AI assistance.

## Practice

1. List the sections of a research proposal in order.
2. Rewrite as an answerable research question: "Mobile apps are important."
3. State the five parts of a structured abstract.
4. How does a literature review differ from an annotated bibliography?
5. Format a book reference in IEEE style: Tanenbaum and Wetherall, *Computer Networks*, 5th ed., Pearson, 2011.
6. What is the difference between a quotation and a paraphrase?
7. Why is changing three words in a copied paragraph still plagiarism?
8. What is a Jaccard similarity of 0.5 between two sets of shingles?
9. Name three risks of using generated text in an assignment.
10. When should you cite software?

::: note Answers and worked solutions
**1.** Title, abstract, introduction and problem, objectives/research questions, literature review, methodology, scope and limitations, work plan, budget, references.
**2.** "Does an Android app for bus timetables reduce passengers' waiting time at the Kalanki stop compared with printed timetables?"
**3.** Background, objective, method, results (with numbers), conclusion.
**4.** A review synthesises sources by theme to argue what is known and what is missing; an annotated bibliography summarises each source separately.
**5.** [1] A. S. Tanenbaum and D. J. Wetherall, *Computer Networks*, 5th ed. Boston, MA, USA: Pearson, 2011.
**6.** A quotation reproduces the exact words in quotation marks; a paraphrase restates the idea in your own words and structure; both need a citation.
**7.** The ideas, structure and most wording remain someone else's and are presented as yours without credit.
**8.** Half of all distinct three-word sequences in either text appear in both.
**9.** Invented facts or references, no real understanding or originality, and a breach of integrity rules if undisclosed.
**10.** Whenever you use or adapt someone else's code, library or tool in your work, to give credit and meet the licence.
:::

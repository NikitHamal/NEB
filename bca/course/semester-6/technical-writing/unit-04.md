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

## 4.6 Seeing the ideas: the library, the hourglass and two citation styles

```photogrid label="4.1" cols="2" ratio="1.0" caption="(a) A university reading room: the literature review begins in places like this, or today on a library portal such as TU's. Searching, reading and noting sources is the slow, honest part of research. (b) The IMRaD paper is an hourglass: it opens broad, narrows to what you did and found, then widens again to meaning."
@ photo id="bca354/library" cap="University reading room"
fit 1.0
focus 0.5 0.55
@ svg cap="IMRaD hourglass"
f = Fig(300, 300)
f.poly([(20, 10), (280, 10), (200, 90), (100, 90)], fill=BLUE, stroke=NAVY, label="Introduction\nbroad to narrow", lx=150, ly=45, size=12.5, color=NAVY)
f.box(100, 90, 100, 56, "Methods\nwhat you did", fill=MINT, stroke=TEAL, size=12.5)
f.box(100, 146, 100, 56, "Results\nwhat you found", fill=SAND, stroke=AMBER, size=12.5)
f.poly([(100, 202), (200, 202), (280, 282), (20, 282)], fill=ROSE, stroke=RED, label="Discussion\nnarrow to broad", lx=150, ly=244, size=12.5, color=NAVY)
```

```svgfig label="4.1" caption="The same reference in APA 7 and IEEE style. APA puts the year right after the authors; IEEE numbers the source, uses initials first, quotes the title and ends with the year. Both give the same facts, so choose one style and keep it throughout."
f = Fig(580, 200)
def row(y, lab, parts):
    f.text(14, y - 10, lab, size=12, color=NAVY, bold=True, anchor="start")
    x = 14
    for t, w, fl, st in parts:
        f.box(x, y, w, 40, t, fill=fl, stroke=st, size=9.5)
        x += w + 4
row(32, "APA 7", [("Rivest, R., Shamir, A., &\nAdleman, L.", 140, BLUE, NAVY), ("(1978).", 50, SAND, AMBER), ("A method for obtaining digital\nsignatures and public-key\ncryptosystems.", 160, MINT, TEAL), ("Communications of the ACM,\n21(2), 120-126.", 178, ROSE, RED)])
row(112, "IEEE", [("[1] R. Rivest, A. Shamir, and\nL. Adleman,", 150, BLUE, NAVY), ("\"A method for obtaining digital\nsignatures and public-key\ncryptosystems,\"", 166, MINT, TEAL), ("Commun. ACM,\nvol. 21, no. 2,\npp. 120-126,", 120, ROSE, RED), ("1978.", 100, SAND, AMBER)])
f.text(290, 176, "author  |  title  |  source  |  year: the same four parts in a different order", size=11, color=SLATE, italic=True)
```

### 4.6.1 Eight habits of honest academic writing

1. **Define a narrow question.** A proposal that says "study the internet in Nepal" is too wide to finish. "How many of 120 BCA students at one Pokhara campus use mobile wallets weekly?" can be answered in a month. A sharp question decides the method, the sample and the length.
2. **Read before you write.** Spend the first weeks finding five to fifteen good sources and noting what each says. Use Google Scholar, institutional access and the university library. The review shows what is already known and where your work fits.
3. **Keep a source log.** Record author, year, title, source, page and a one-line note for every source as you read. This takes a minute and saves hours when the bibliography is due. A spreadsheet or a free reference manager is enough.
4. **Quote, paraphrase and cite correctly.** Put exact words in quotation marks with a page number, and when paraphrasing change the structure and still cite. Every number, figure and idea that is not common knowledge needs a source. Copying a few lines from a blog without credit is plagiarism even if it is short.
5. **Use one citation style.** APA is common in social science and IEEE in engineering and computing, but a department may demand its own. Check the guide at the start, then use a formatter or tool consistently. Mixed styles look careless and make sources hard to find.
6. **Write the abstract last.** A good abstract states the problem, method, main result and conclusion in 150 to 250 words. Because it summarises the finished work, write it after the discussion. It is the part most readers see, so check every number.
7. **Report the method so others can repeat it.** Give the sample size, tools, versions, dates and steps. A reader should be able to follow the Methods section and get a similar result. Hiding the method makes the work impossible to check.
8. **Be honest about limits and AI use.** Say what the study could not show, such as a small sample from one campus. Follow the institution's rule on AI tools and disclose any help, and never accept a reference without finding the real source. Honesty about limits makes the findings more trusted, not less.

```photogrid label="4.2" cols="2" ratio="1.2" caption="Plain sentences score higher and read faster. (a) A typewriter: when every letter has to be hammered onto paper, writers learned to cut empty words, a habit that is still the heart of technical writing. (b) The Flesch reading-ease formula, 206.835 minus 1.015 times the words per sentence minus 84.6 times the syllables per word, was applied to two pairs of sentences that say the same thing. The wordy first sentence (25 words) scores -1 and its plain version (9 words) scores 76; the second pair goes from 18 to 76. Long words such as utilisation and long sentences are what push the score down. In a project report, aim for a score near 50 to 60 for explanations, keep terms of art where they are needed, and cut phrases such as it is the case that. Syllables were counted by a simple rule, so scores are approximate."
@ photo id="bcapc/typewriter" cap="A typewriter: every extra word costs effort"
fit 1.2
focus 0.5 0.5
@ svg cap="Flesch reading ease: wordy vs plain"
import re
def syl(w):
    w = w.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(n, 1)
def fre(t):
    sents = [s for s in re.split(r"[.!?]+", t) if s.strip()]
    ws = re.findall(r"[A-Za-z']+", t)
    sy = sum(syl(w) for w in ws)
    return 206.835 - 1.015 * len(ws) / len(sents) - 84.6 * sy / len(ws), len(ws)
pairs = [
 ("It is the case that the utilisation of an implementation of the aforementioned methodology resulted in a considerable improvement in the performance of the system.",
  "We used the method, and the system ran faster."),
 ("In the event that the participants are in possession of the requisite documentation, the registration procedure will be commenced.",
  "If you bring your documents, we will register you."),
]
res = [(fre(a), fre(b)) for a, b in pairs]
assert all(r[1][0] > r[0][0] + 30 for r in res)
facts = dict(w1=res[0][0][1], p1=res[0][1][1], w1s=round(res[0][0][0]), p1s=round(res[0][1][0]), w2s=round(res[1][0][0]), p2s=round(res[1][1][0]), w2=res[1][0][1], p2=res[1][1][1])
f = Fig(300, 236)
f.text(150, 12, "Flesch reading ease (higher is easier)", size=10.5, color=NAVY, bold=True)
labs = ["wordy 1 (%d words)" % res[0][0][1], "plain 1 (%d words)" % res[0][1][1], "wordy 2 (%d words)" % res[1][0][1], "plain 2 (%d words)" % res[1][1][1]]
vals = [res[0][0][0], res[0][1][0], res[1][0][0], res[1][1][0]]
for i, (l, v) in enumerate(zip(labs, vals)):
    y = 28 + i * 36
    f.text(6, y + 7, l, size=10.5, color=NAVY, bold=True, anchor="start")
    wv = max(v, 0) / 100 * 200
    f.box(6, y + 14, max(wv, 3), 16, "", fill="#bbf7d0" if i % 2 else "#fecaca", stroke=SLATE, r=3, sw=1)
    f.text(12 + max(wv, 3), y + 22, "%d" % round(v), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 186, "90+ very easy, 60 plain English,", size=10.5, color=SLATE)
f.text(150, 202, "30 or below: graduate level", size=10.5, color=SLATE)
f.text(150, 224, "cutting words raised both scores a lot", size=10.5, color=TEAL, bold=True)
```

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the structure of a research proposal.**

*Introduction.* A **research proposal** asks permission and funding to carry out a study by showing that the question is worth asking and the plan is sound. It is judged on clarity, feasibility and value.

*Parts.*

1. **Title:** specific and informative.
2. **Abstract or summary:** the whole plan in 150 to 250 words.
3. **Introduction and background:** the problem and why it matters.
4. **Literature review:** what is known, and the gap.
5. **Objectives or research questions:** two to four, measurable.
6. **Methodology:** design, population and sample, data collection, analysis, ethics.
7. **Work plan (Gantt chart) and budget:** tasks, weeks, costs.
8. **Expected outcome and references.**

*Example.* "Mobile-wallet use among 120 BCA students of one Pokhara campus": objective, to estimate weekly use; method, an online questionnaire with a random sample; analysis, percentages and a chi-square test; timeline, 8 weeks. *Conclusion:* a proposal convinces by being narrow, feasible and clearly planned.

**Q2 (5 marks). Distinguish plagiarism from legitimate use of sources. How can plagiarism be avoided?**

*Plagiarism* is presenting another person's words, ideas, data or code as your own. Forms include copying without quotation marks, patchwork copying with a few words changed, paraphrasing without credit, submitting bought or AI-generated work as your own, and self-plagiarism.

*Legitimate use* acknowledges the source in the text and in a reference list.

| Action | Plagiarism? |
|---|---|
| Quoting with quotation marks, page and citation | no |
| Paraphrasing in your own structure and citing | no |
| Common knowledge (water boils at 100 °C at sea level) | no citation needed |
| Copying a paragraph, changing a few words | yes |
| Using a figure without credit | yes |

*Avoiding it.* Keep a source log, take notes in your own words, quote exactly when needed, cite as you write, use one style, and check with a similarity tool. A similarity checker only measures matching text: in the book's shingle program, a lightly edited copy scored 0.80 while a true paraphrase scored 0.00, so a person must still judge. *Conclusion:* credit every borrowed idea and the work stays honest.

**Q3 (10 marks). Explain the structure of a scientific paper (IMRaD), the literature review and the APA and IEEE citation styles.**

*Introduction.* A scientific report follows a conventional structure so that readers can find what they need quickly. The most common is **IMRaD** (Figure 4.1 hourglass in Plate 4.1).

*IMRaD.*

1. **Abstract:** a stand-alone summary of problem, method, result and conclusion.
2. **Introduction:** begins broad, states the problem, the gap and the objective.
3. **Methods:** exactly what was done, so it can be repeated.
4. **Results:** the findings, with tables and figures, without interpretation.
5. **Discussion:** what the results mean, how they compare with earlier work, limits and future work.
6. **Conclusion and references.**

*Literature review.* It is a critical summary of existing work, organised by theme and not by source, that shows what is known, where studies disagree and what gap remains. Steps: search (keywords, databases), screen, read, note, group by theme, compare, state the gap. It is not a list of abstracts.

*Citation.* Citing credits sources, lets readers verify and avoids plagiarism. Two styles (Figure 4.1 in the text):

| Feature | APA 7 | IEEE |
|---|---|---|
| In-text | (Rivest et al., 1978) | [1] |
| Order of list | alphabetical by author | order of first citation |
| Author names | Rivest, R. | R. Rivest |
| Year | after the authors | at the end |
| Title | plain, sentence case | in quotation marks |
| Typical field | social science, education | engineering, computing |

*Example output of the book's formatter.* APA: Rivest, R., Shamir, A., & Adleman, L. (1978). A method for obtaining digital signatures and public-key cryptosystems. *Communications of the ACM, 21*(2), 120–126. IEEE: R. Rivest, A. Shamir, and L. Adleman, "A method for obtaining digital signatures and public-key cryptosystems," *Communications of the ACM*, vol. 21, no. 2, pp. 120–126, 1978.

*Conclusion.* IMRaD gives every paper the same map, the literature review shows the gap, and one consistent citation style gives credit and makes sources traceable.

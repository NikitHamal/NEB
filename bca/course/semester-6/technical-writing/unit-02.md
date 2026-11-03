---
subject: Technical Writing
grade: BCA Semester 6
unit: 2
title: Style, Clarity and Readability
hours: 8
area: BCA 354 · Technical Writing · Unit 2
---

Compare two sentences telling a user the same thing. *"It is imperative that users of the application ensure the utilization of authentication credentials prior to the initiation of any transaction."* and *"Log in before you start a transaction."* The first has 21 words and five long abstract nouns; the second has 7 words and one. Both are grammatical, but only the second is read the first time. This unit gives you the rules for writing at the level of the sentence (active voice, strong verbs, concrete words, parallel lists, consistent terms) and, because writing quality can be *measured* in a crude way, three **readability formulas** (Flesch Reading Ease, Flesch–Kincaid Grade Level and Gunning Fog) computed by a program from hand-counted syllables, so that every figure can be verified by hand.

::: key What this unit gives you
- Plain-language rules: short sentences, active voice, strong verbs, concrete nouns, no needless nominalisation or jargon.
- Parallelism, lists, definitions, consistency, and numbers and units.
- The readability formulas with definitions and limits; a worked, executed computation on a plain and a heavy sentence.
- Common errors of Nepali users of English.
:::

## 2.1 Rules of clear technical sentences

1. **Prefer short sentences.** Aim for an average of 15–20 words; vary length, but split any sentence that carries more than one instruction or idea. One instruction per sentence in procedures.
2. **Use the active voice** when the actor matters. Passive: "The file is saved by the system." Active: "The system saves the file." Active sentences name who acts, are shorter and are easier to follow. Use the passive deliberately when the actor is unknown or unimportant ("The server was restarted at 02:00") or when the *receiver* is the topic.
3. **Choose strong verbs; avoid nominalisation.** Nominalisations turn verbs into nouns and need extra helper verbs: "perform an analysis of" → "analyse"; "make a decision" → "decide"; "give consideration to" → "consider"; "carry out the installation of" → "install"; "is in agreement with" → "agrees with".
4. **Use concrete, familiar words.** "Use" not "utilise"; "start" not "commence" or "initiate"; "help" not "facilitate"; "about" not "approximately" (unless precision is needed); "buy" not "procure"; "end" not "terminate".
5. **Cut deadwood.** "In order to" → "to"; "due to the fact that" → "because"; "at this point in time" → "now"; "it is important to note that" → delete; "a large number of" → "many"; "in the event that" → "if"; "has the ability to" → "can".
6. **Be specific and quantitative.** "The page loads fast" → "The page loads in under 2 seconds on a 4G connection". "A large file" → "A file over 100 MB". Replace "soon", "recently", "several" with dates and numbers.
7. **Place modifiers carefully and avoid ambiguity.** "Only" and "also" belong next to the word they limit. "Remove the batteries from the old devices that are damaged" is ambiguous (which are damaged?). Prefer "Remove the batteries from damaged old devices". Avoid unclear pronouns: replace "it" or "this" with the noun when the reference is not obvious.
8. **Put the main idea first;** conditions before actions ("If the light is red, press Reset").
9. **Avoid noun stacks.** "Network packet loss detection threshold configuration parameter" is hard to parse; rewrite as "the parameter that sets the threshold for detecting packet loss".
10. **Use the imperative for instructions** ("Press Enter"), second person ("you"), present tense, and the same word for the same thing throughout.

**Jargon and abbreviations.** Use technical terms only for readers who know them; otherwise define on first use ("DNS (Domain Name System), the service that converts website names to addresses"). Spell out an abbreviation at first use and keep a **glossary** for long documents. Avoid **idioms and humour** for international readers. **Gender-neutral** and respectful language is part of correctness ("they", not "he or she"; "staff", not "manpower").

## 2.2 Parallelism, lists and consistency

Items in a list or heading must have the **same grammatical form**: *Parallel:* "Installing the driver, configuring the port, testing the printer." *Not parallel:* "Installing the driver, to configure the port, and the printer test." Use **bulleted lists** for items of equal weight, **numbered lists** for sequences, and introduce each with a complete lead-in sentence. Keep list items similar in length and begin them consistently. Use a **table** when each item has several attributes.

**Consistency** is a form of clarity: one term per concept ("Settings" everywhere, not "Preferences" in one place); one format for dates (2082-01-15 or 15 Baisakh 2082, not both without need); numbers: spell out one to nine in prose and use numerals for 10 and above, but always use numerals with units (5 MB, 3 seconds); put a **space between number and unit** (16 GB); use **SI units** and state currency and the lakh/crore grouping (Rs 12,00,000) consistently with a note if readers use millions; write **times** in 24-hour format when precision matters ("02:00 NPT").

## 2.3 Measuring readability

A **readability formula** estimates how hard text is from simple counts. Let *w* be the number of words, *s* the number of sentences, *y* the number of syllables and *c* the number of **complex words** (three or more syllables, in the usual Gunning definition).

- **Flesch Reading Ease (FRE)** = 206.835 − 1.015·(w/s) − 84.6·(y/w). Higher is easier: about 90–100 is very easy, 60–70 plain English, 30–50 difficult, below 30 very difficult (graduate level).
- **Flesch–Kincaid Grade Level (FK)** = 0.39·(w/s) + 11.8·(y/w) − 15.59: an approximate U.S. school grade. Eight means an eighth grader can read it.
- **Gunning Fog Index** = 0.4·[(w/s) + 100·(c/w)]: also a grade level, penalising complex words.

All three use the same two ideas: **long sentences and long words make text hard**. They are **crude**: they ignore content, order, layout and the reader's knowledge; short sentences can still be confusing, and a technical term such as "database" counts as a complex word although the audience knows it. They also do not suit non-English text. Use them to *compare drafts* and to catch runaway sentences, not as a target to be gamed. A reasonable aim for general technical documents is FK grade 8–10 and Fog under 12; user-facing instructions should be lower.

### A worked, executed computation

Syllable counting by program is unreliable (English spelling is irregular), so the program below uses a **hand-labelled syllable table** for the words in three short texts, which makes every number reproducible by hand. *Plain* is a sample of good advice; *Before* is the heavy sentence from the start of this unit; *After* is its rewrite.

```python
import re

PLAIN = "Write short sentences. Use common words. A reader who understands quickly will trust the writer."
BEFORE = "It is imperative that users of the application ensure the utilization of authentication credentials prior to the initiation of any transaction."
AFTER = "Log in before you start a transaction."

SYL = {"write": 1, "short": 1, "sentences": 3, "use": 1, "common": 2, "words": 1, "a": 1,
       "reader": 2, "who": 1, "understands": 3, "quickly": 2, "will": 1, "trust": 1,
       "the": 1, "writer": 2, "it": 1, "is": 1, "imperative": 4, "that": 1, "users": 2,
       "of": 1, "application": 4, "ensure": 2, "utilization": 5, "authentication": 5,
       "credentials": 3, "prior": 2, "to": 1, "initiation": 5, "any": 2, "transaction": 3,
       "log": 1, "in": 1, "before": 2, "you": 1, "start": 1}

def scores(text):
    words = re.findall(r"[A-Za-z']+", text)
    s = len(re.findall(r"[.!?]", text))
    w = len(words)
    y = sum(SYL[x.lower()] for x in words)
    c = sum(1 for x in words if SYL[x.lower()] >= 3)
    fre = 206.835 - 1.015 * w / s - 84.6 * y / w
    fk = 0.39 * w / s + 11.8 * y / w - 15.59
    fog = 0.4 * (w / s + 100 * c / w)
    return (w, s, y, c, round(fre, 1), round(fk, 1), round(fog, 1))

for label, text in (("Plain", PLAIN), ("Before", BEFORE), ("After", AFTER)):
    print(label, "(words, sentences, syllables, complex, FRE, FK, Fog) =", scores(text))
```
```output
Plain (words, sentences, syllables, complex, FRE, FK, Fog) = (15, 3, 23, 2, 72.0, 4.5, 7.3)
Before (words, sentences, syllables, complex, FRE, FK, Fog) = (21, 1, 47, 7, -3.8, 19.0, 21.7)
After (words, sentences, syllables, complex, FRE, FK, Fog) = (7, 1, 10, 1, 78.9, 4.0, 8.5)
```
Verify the first one by hand: the Plain text has 15 words in 3 sentences (3 + 3 + 9), 23 syllables (5 + 4 + 14) and 2 complex words (*sentences* and *understands*). Then FRE = 206.835 − 1.015 × 5 − 84.6 × 23/15 = 206.835 − 5.075 − 129.72 = **72.0**; FK = 0.39 × 5 + 11.8 × 1.5333 − 15.59 = **4.5**; Fog = 0.4 × (5 + 13.33) = **7.3**. The heavy *Before* sentence has 21 words, 47 syllables and 7 complex words, so its FRE is **negative** (−3.8, off the usual scale), its FK grade is **19.0** and its Fog **21.7**: it needs a postgraduate reading level to understand a login instruction. The rewrite has 7 words, 10 syllables and one complex word (*transaction*): FRE 78.9, FK 4.0, Fog 8.5. Note that the *After* Fog (8.5) is higher than the *Plain* Fog (7.3) although it is short: one complex word among seven is a high *proportion*, which shows how the formulas behave on tiny samples. Use paragraphs of at least 100 words for any serious measurement.

## 2.4 Common problems in Nepali English writing

| Problem | Example | Better |
|---|---|---|
| Missing or wrong articles | "Server is down." / "Please submit the your form." | "The server is down." / "Please submit your form." |
| Overly formal openings | "With due respect and humble request, I beg to state..." | "I am writing to request..." |
| Redundant phrases | "Kindly do the needful." | State the action: "Please send the signed form by Friday." |
| Wrong prepositions and tense | "He is discussing about the project." | "He is discussing the project." |
| Direct translation of forms of address | "Respected Sir/Madam" in every email | "Dear Mr Sharma," (or "Dear Team,") |
| Unclear dates and numbers | "10/11/12" | "12 Poush 2082 (27 Dec 2025)" or ISO 2025-12-27 |
| Mixed spelling conventions | "colour" and "color" | Choose one (British or American) and keep it |

Reading good technical English (documentation of widely used tools, standards such as RFCs, quality newspapers) is the best way to absorb idiom; use a spell-checker and a grammar tool, but verify their suggestions, and keep your own list of recurring errors.

## 2.5 Seeing the ideas: scores and sentence surgery

```svgfig label="2.1" caption="The three texts of the executed program in 2.3. Lower bars are easier. The heavy sentence needs a postgraduate reading level (FK 19.0, Fog 21.7); the seven-word rewrite sits near fourth grade. After is a tiny sample, so its Fog (8.5) exceeds Plain (7.3) even though it is shorter."
f = Fig(580, 214)
rows = [("Plain (15 words)", 4.5, 7.3), ("Before (21 words)", 19.0, 21.7), ("After (7 words)", 4.0, 8.5)]
k = 11
for i, (t, fk, fog) in enumerate(rows):
    y = 14 + i * 62
    f.text(14, y + 25, t, size=11.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.box(130, y + 4, fk * k, 22, "", fill=BLUE, stroke=NAVY)
    f.text(130 + fk * k + 6, y + 15, "FK %.1f" % fk, size=10.5, color=NAVY, anchor="start", vmid=True)
    f.box(130, y + 30, fog * k, 22, "", fill=SAND, stroke=AMBER)
    f.text(130 + fog * k + 6, y + 41, "Fog %.1f" % fog, size=10.5, color=AMBER, anchor="start", vmid=True)
f.line(130 + 8 * k, 8, 130 + 8 * k, 198, color=TEAL, dash=True)
f.text(130 + 8 * k, 208, "grade 8 target for general readers", size=10, color=TEAL, italic=True)
f.box(440, 20, 130, 74, "FK = Flesch-Kincaid\ngrade level\nFog = Gunning Fog\nindex (also a grade)", fill=MINT, stroke=TEAL, size=10.5)
```

```svgfig label="2.2" caption="Sentence surgery on the 21-word instruction. Struck-out words are deadwood or abstract nouns; each coloured pair shows the replacement. Result: 7 words, one instruction, active voice."
f = Fig(580, 196)
W = ["It is imperative that", "users of the application", "ensure", "the utilization of", "authentication credentials", "prior to", "the initiation of any", "transaction."]
X = [14, 14, 14, 14, 14, 14, 14, 14]
f.box(14, 12, 552, 40, "It is imperative that users of the application ensure the utilization of authentication\ncredentials prior to the initiation of any transaction.", fill=ROSE, stroke=RED, size=11)
steps = [("It is imperative\nthat", "delete", 14), ("users of the\napplication", "you", 154), ("ensure the utilization\nof authentication\ncredentials", "log in", 294), ("prior to the initiation\nof any", "before you start a", 434)]
for t, r, x in steps:
    f.box(x, 66, 132, 50, t, fill=SAND, stroke=AMBER, size=10)
    f.arrow([(x + 66, 116), (x + 66, 130)], color=TEAL)
    f.box(x, 130, 132, 26, r, fill=MINT, stroke=TEAL, bold=True, size=11)
f.box(150, 164, 280, 24, "Log in before you start a transaction.", fill=NAVY, color="#ffffff", bold=True, size=12)
```

### 2.5.1 Eight benefits of plain language in Nepali public and business writing

1. **Fewer mistakes by citizens.** A form that says "write your name as on your citizenship certificate" is filled correctly, while one that says "furnish particulars as per the instrument of identity" is returned. Every returned form costs the citizen a trip and the office a second review. Plain words cut rework on both sides.
2. **Faster service.** Staff spend less time explaining what a notice means when the notice is clear. A Department of Transport Management counter that hands out a one-page numbered checklist answers fewer repeated questions. The queue moves faster for everybody.
3. **Wider reach for second-language readers.** Many Nepali readers learn English as a second or third language after Nepali and a mother tongue. Short sentences and common words are understood without a dictionary. This is why Nagarik App help text should avoid words like "authenticate" when "sign in" will do.
4. **Lower support cost.** Every unclear error message becomes a call or a visit to the help desk. Replacing "Error 0x80070057" with "The file name is too long. Use fewer than 100 characters." removes the need to ask. A bank or wallet such as Fonepay saves money when users solve problems alone.
5. **Safer instructions.** In electrical, medical or office-safety text, a misread step can injure someone. One action per sentence and the warning before the step reduce the chance of error. The same rule protects a data centre technician who must pull cables in the right order.
6. **Better legal and financial clarity.** Contracts, terms and tax notices written in plain language leave less room for dispute. A loan notice that states "pay NPR 12,500 by 15 Magh 2082" is harder to misunderstand than "remit the requisite amount in due course". Clear dates and amounts also protect the writer.
7. **Stronger trust.** Readers trust a writer who does not hide behind long words. An institution whose circulars are easy to read looks organised and honest. Tribhuvan University EMIS notices that give a plain date and time are respected more than vague ones.
8. **Easier translation and reuse.** Short, active sentences with consistent terms translate into Nepali, Maithili or Newari with fewer errors, and they can be reused in a manual, a chatbot and a poster. Machine translation also works better on plain text. One clear source becomes many useful documents.

## Chapter summary

- Write short, active sentences with strong verbs, concrete words, specific numbers and consistent terms; cut deadwood and noun stacks.
- Use parallel structure in lists and headings; stay consistent in terms, numbers, dates and units.
- Flesch Reading Ease = 206.835 − 1.015(w/s) − 84.6(y/w); FK = 0.39(w/s) + 11.8(y/w) − 15.59; Fog = 0.4[(w/s) + 100(c/w)]. They measure sentence and word length only.
- The heavy sentence scores FK 19.0 and Fog 21.7; its seven-word rewrite scores FK 4.0 and Fog 8.5.
- Common errors by Nepali writers include articles, over-formal phrases, prepositions and ambiguous dates.

## Practice

1. Rewrite in active voice: "The report was approved by the committee."
2. Replace the nominalisation: "We will perform an evaluation of the vendors."
3. Replace the wordy phrases: "In order to proceed, due to the fact that the file is large."
4. Make this list parallel: "Reading the manual, to install the software, and configuration of the network."
5. Compute FRE for a text with 100 words, 5 sentences and 150 syllables.
6. Compute FK for the same text.
7. Compute the Gunning Fog index for the same text if it has 12 complex words.
8. Why can a short sentence still be hard to read?
9. State two limitations of readability formulas.
10. Rewrite for clarity: "Kindly do the needful regarding the aforementioned matter at your earliest convenience."

::: note Answers and worked solutions
**1.** "The committee approved the report."
**2.** "We will evaluate the vendors."
**3.** "To proceed, because the file is large."
**4.** "Reading the manual, installing the software and configuring the network."
**5.** w/s = 20; y/w = 1.5. FRE = 206.835 − 1.015 × 20 − 84.6 × 1.5 = 206.835 − 20.3 − 126.9 = **59.6**.
**6.** FK = 0.39 × 20 + 11.8 × 1.5 − 15.59 = 7.8 + 17.7 − 15.59 = **9.9**.
**7.** Fog = 0.4 × (20 + 100 × 12/100) = 0.4 × 32 = **12.8**.
**8.** It may use unfamiliar terms, missing context or ambiguous references; the formulas measure length only, not meaning.
**9.** They ignore content, structure and the reader's background knowledge; they can be gamed; they are unreliable on short samples and non-English text.
**10.** "Please send me the signed form by Friday." (State the action, the object and the deadline.)
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). State the rules for writing clear technical sentences, with examples.**

*Introduction.* A technical sentence should be read once and understood the first time, because the reader is usually trying to do something. Figure 2.2 shows how a 21-word sentence becomes a 7-word one.

*Rules with examples.*

1. **Short sentences** of 15 to 20 words on average, one instruction in each.
2. **Active voice** when the actor matters: "The system saves the file", not "The file is saved by the system".
3. **Strong verbs, not nominalisations:** "analyse", not "perform an analysis of".
4. **Familiar words:** "use" for "utilise", "start" for "initiate".
5. **No deadwood:** "because" for "due to the fact that"; "if" for "in the event that".
6. **Specific numbers:** "loads in under 2 seconds on 4G", not "loads fast".
7. **Conditions before actions:** "If the light is red, press Reset".
8. **Parallel structure** in lists and headings, and one term for one thing.

*Example.* "It is imperative that users of the application ensure the utilization of authentication credentials prior to the initiation of any transaction" (21 words, FK 19.0) becomes "Log in before you start a transaction" (7 words, FK 4.0). *Conclusion:* clarity comes from short sentences, active verbs and plain words.

**Q2 (5 marks). Compute the Flesch Reading Ease and Flesch-Kincaid grade for a text of 120 words, 8 sentences and 180 syllables. Interpret the result.**

*Formulae.* FRE = 206.835 − 1.015 (w/s) − 84.6 (y/w); FK = 0.39 (w/s) + 11.8 (y/w) − 15.59.

*Working.* Words per sentence w/s = 120 / 8 = 15. Syllables per word y/w = 180 / 120 = 1.5.

1. FRE = 206.835 − 1.015 × 15 − 84.6 × 1.5 = 206.835 − 15.225 − 126.9 = **64.71**.
2. FK = 0.39 × 15 + 11.8 × 1.5 − 15.59 = 5.85 + 17.7 − 15.59 = **7.96**.

*Interpretation.* A score of 60 to 70 is "plain English", and a grade near 8 means an eighth-grade student can read it. This suits a general audience such as a user guide for a ward-level service.

| Measure | Value | Meaning |
|---|---|---|
| FRE | 64.7 | plain English |
| FK | 7.96 | about grade 8 |

*Limits.* Both formulas count only sentence and word length. They ignore order, layout and the reader's knowledge, and they are unreliable below 100 words. *Conclusion:* use the scores as a rough check, then test with real readers.

**Q3 (10 marks). Explain readability and its measures (Flesch, Flesch-Kincaid and Gunning Fog). Discuss their limitations and describe how to improve a hard-to-read text.**

*Introduction.* **Readability** is how easily a reader can read and understand a text. Formulas estimate it from surface features, and writers use them as a quick signal (Figure 2.1).

*The three measures.*

1. **Flesch Reading Ease** = 206.835 − 1.015 (w/s) − 84.6 (y/w). Higher is easier: 90 to 100 very easy, 60 to 70 plain English, 30 to 50 difficult, below 30 very difficult.
2. **Flesch-Kincaid Grade** = 0.39 (w/s) + 11.8 (y/w) − 15.59, an approximate school grade.
3. **Gunning Fog** = 0.4 [(w/s) + 100 (c/w)], where c is the number of complex words (three or more syllables); it also gives a grade.

*Worked data from the book's program.*

| Text | Words | Sentences | FRE | FK | Fog |
|---|---|---|---|---|---|
| Plain | 15 | 3 | 72.0 | 4.5 | 7.3 |
| Before | 21 | 1 | −3.8 | 19.0 | 21.7 |
| After | 7 | 1 | 78.9 | 4.0 | 8.5 |

*Limitations.* (a) They ignore content, logic, order and layout. (b) Short sentences can still confuse, as in a string of unexplained abbreviations. (c) Syllable counting is approximate. (d) Tiny samples mislead: *After* has a higher Fog than *Plain* because one complex word is a large share of seven words. (e) They do not measure the reader's prior knowledge, so a technical term such as "router" may be easy for a BCA student but not for a villager.

*Improving a hard text.* (1) Split long sentences. (2) Replace nominalisations and long words with familiar ones. (3) Use the active voice and the imperative. (4) Cut deadwood. (5) Add headings, lists and tables. (6) Define unavoidable jargon on first use. (7) Re-measure on at least 100 words. (8) Test with five real readers.

*Conclusion.* Readability formulas are a thermometer, not a diagnosis. They show that a text is hard; the writer's edit and a reader's test show why and how to fix it.

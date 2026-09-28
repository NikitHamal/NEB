---
subject: Compulsory English
grade: 12
unit: 34
title: 'Unseen Reading Comprehension Strategy'
hours: 7
area: Writing and Skills
---

Question 1 is worth fifteen marks — a fifth of the whole written paper — and it is the
only question in which the answers are already printed in front of you. That is the
point most candidates miss. You are not being asked what you know about fog or
homestays; you are being asked whether you can find, in a passage you have never seen,
the exact place where the answer lives, and then say it in your own words without
changing its meaning.

::: key The passage is the authority, not you
Every answer must be defensible by pointing at a line. If you cannot put your finger on
the words that justify what you have written, you have written what you believe, and
what you believe earns nothing.
:::

## 34.1 What Question 1 asks

An unseen passage of 350 to 450 words, followed by three sets of questions. The commonest
shape at Grade 12:

| Set | Task | Marks |
|---|---|---|
| **A** | True / False / Not Given, or fill in the blanks from the text | 5 |
| **B** | Short answers in your own words | 5 |
| **C** | Vocabulary in context — find the word that means … | 5 |

**Time: twenty-five minutes.** That is a budget, and it should be spent unequally.

```figure caption="A twenty-five minute budget for a fifteen-mark passage. Reading the questions before the second reading is what makes the second reading fast."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1, 2.4))
stages = ["Skim the\npassage", "Read the\nquestions",
          "Re-read and\nmark the text", "Write the\nanswers", "Check"]
mins = [3, 3, 5, 11, 3]
cols = [SERIES[3], SERIES[3], ACCENT, ACCENT, MUTED]
left = 0
for m, c, t in zip(mins, cols, stages):
    ax.barh([0], [m], left=left, height=0.55, color=c, edgecolor="white", linewidth=1.2)
    ax.text(left + m / 2, 0.0, str(m), ha="center", va="center",
            fontsize=7.0, color="white")
    ax.text(left + m / 2, -0.47, t, ha="center", va="top",
            fontsize=6.1, color=INK, linespacing=1.5)
    left += m
ax.set_xlim(0, 25)
ax.set_ylim(-1.05, 0.60)
ax.set_yticks([])
ax.set_xticks([0, 5, 10, 15, 20, 25])
ax.set_xlabel("minutes", fontsize=7.0)
ax.tick_params(axis="x", labelsize=6.6)
ax.spines[["top", "right", "left"]].set_visible(False)
```

## 34.2 The five steps

1. **Skim** — ninety seconds. Read the title, the first sentence of every paragraph and
   the last sentence of the passage. You now know the subject and the shape, and that is
   all you need.
2. **Read the questions** — all of them, before you read the passage properly. Underline
   the **key word** in each question: the one word that must appear, or be paraphrased,
   in the passage.
3. **Scan and mark.** Go back into the passage hunting for those key words. When you
   find one, write the question number in the margin beside the line. Do not answer yet.
4. **Write**, question by question, from the marked lines. Keep the passage open in
   front of you; do not answer from memory.
5. **Check** against the checklist in Section 34.8.

::: tip Why the questions come before the careful reading
A passage read without questions has to be remembered in full. A passage read with five
underlined key words in your head is a search, and searching is four times faster than
remembering. This single change in order is worth two or three marks.
:::

## 34.3 Skimming and scanning are different skills

| | Skimming | Scanning |
|---|---|---|
| Looking for | the gist | one particular fact |
| Eye movement | down the left edge, first lines | zig-zag, hunting a shape |
| You already know | nothing | exactly what you want |
| Used in step | 1 | 3 |
| Everyday parallel | deciding whether to read a news article | finding a name in a phone list |

**What to scan for.** Numbers, dates and capital letters are the easiest shapes to
find, so questions containing them are the ones to answer first. Next easiest are
technical words the passage cannot paraphrase — *condensation*, *mesh*, *homestay*.
Hardest are questions built entirely of common words; leave those until last.

## 34.4 The question types and what each demands

| Type | What is being tested | The rule |
|---|---|---|
| **Stated fact** (*What does X do?*) | scanning | answer in a phrase; no need for a full sentence unless asked |
| **Own words** (*Explain in your own words…*) | paraphrase | change the words, keep the meaning; copying scores zero |
| **Inference** (*Why do you think…? · What does this suggest?*) | reasoning | the answer is implied by the text — quote the clue in your head first |
| **Vocabulary in context** | word attack | find the word, read the whole sentence, replace and test |
| **Reference** (*What does 'it' in line 12 refer to?*) | cohesion | look backwards, usually to the nearest preceding noun phrase |
| **True / False / Not Given** | precision | see Section 34.5 |
| **Summary / note completion** | selection | the missing word is almost always taken from the passage unchanged |
| **Title** | gist | must cover the whole passage, not the first paragraph |

## 34.5 True, False, or Not Given

This is the set that separates a 12 from a 15. The three answers mean three quite
different things, and only one of them is about the world.

- **True** — the passage says it, in these words or in others.
- **False** — the passage says the **opposite**. There is a line you could point at that
  contradicts the statement.
- **Not Given** — the passage neither says it nor contradicts it. It may well be true in
  real life. That is irrelevant.

```figure caption="The decision a True / False / Not Given question really asks. Most wrong answers come from the left-hand branch: the candidate knows the statement is true in the world and forgets that the question is about the passage."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(5.1, 3.2))
ax.axis("off")
def box(x, y, w, h, t, fc, ec, fs=6.2):
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.0,rounding_size=0.10",
                 linewidth=1.0, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center",
            fontsize=fs, color=INK, linespacing=1.5)
box(2.55, 8.05, 4.9, 1.15, "Find the line in the passage\nthat the statement is about",
    "#ffffff", GRID)
box(0.35, 5.35, 4.0, 1.15, "There is such a line", "#e8f1f9", ACCENT)
box(5.65, 5.35, 4.3, 1.15, "There is no such line\nanywhere", "#e8f1f9", ACCENT)
box(0.35, 2.55, 1.85, 1.15, "It agrees", "#ffffff", GRID)
box(2.50, 2.55, 1.85, 1.15, "It says the\nopposite", "#ffffff", GRID)
box(0.35, 0.35, 1.85, 1.05, "TRUE", "#ffffff", ACCENT, 6.8)
box(2.50, 0.35, 1.85, 1.05, "FALSE", "#ffffff", ACCENT, 6.8)
box(5.65, 0.35, 4.3, 1.05, "NOT GIVEN", "#ffffff", ACCENT, 6.8)
def arr(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9,
                                mutation_scale=8))
arr(4.10, 8.00, 2.35, 6.55)
arr(5.90, 8.00, 7.80, 6.55)
arr(2.00, 5.30, 1.28, 3.75)
arr(2.70, 5.30, 3.43, 3.75)
arr(1.28, 2.50, 1.28, 1.45)
arr(3.43, 2.50, 3.43, 1.45)
arr(7.80, 5.30, 7.80, 1.45)
ax.set_xlim(0.1, 10.2)
ax.set_ylim(0.2, 9.4)
```

::: caution The four traps in a True / False / Not Given set
- **All, every, never, only.** A passage that says *most cliff bees nest on north-facing
  rock* does not support *all cliff bees nest on north-facing rock*. That is **False**.
- **Comparisons you were never given.** If the passage praises fog nets and never
  mentions wells, *fog nets are cheaper than wells* is **Not Given**.
- **Cause smuggled in.** The passage may say two things happened; unless it says one
  caused the other, a causal statement is **Not Given**.
- **Your own knowledge.** You may know the statement is true. If the passage does not
  say so, it is still **Not Given**.
:::

## 34.6 Vocabulary in context and inference

**Vocabulary.** Never answer from the dictionary you remember. Work through four moves:

1. Find the word in the passage and read the **whole sentence**, not the phrase.
2. Decide the **part of speech** — a noun answer for a noun question.
3. Look for a **signal**: a definition after a comma, an example after *such as*, a
   contrast after *but* or *unlike*, a repetition in the next sentence.
4. **Replace and test**: put your guess into the sentence and see whether the sentence
   still makes sense.

::: example Worked example 34.1 — reasoning your way to a meaning
**The sentence.** *The committee was wary of large groups, and for two seasons it
**capped** the number of guests in any one house at four.*

**The question.** Find a word in the passage which means *set an upper limit on*.

**The reasoning.** *Capped* sits between *it* and *the number*, so it is a verb in the
past tense — the answer must be a verb. The sentence gives its own signal: *at four*
tells you that something was fixed at a maximum, and *wary of large groups* tells you
why. Test the replacement: *it set an upper limit on the number of guests at four*
makes sense, so the guess holds. The everyday meaning of *cap* — a thing worn on the
head — is irrelevant here, and a candidate who answers from that meaning loses a mark
that the sentence was handing him.

**The answer.** *capped*
:::

**Inference.** An inferred answer is not a guess; it is a conclusion with a line behind
it. If the passage says *the school now has eleven pupils, and the youngest teacher is
fifty-four*, then *the village is losing its young families* is a fair inference — two
facts point at it. *The teachers are badly paid* is not; nothing points at it.

## 34.7 Practice passage 1, with a worked key

::: example Worked passage 34.2 — Water Out of the Air
**[1]** On the ridges above many hill villages the fog arrives before the rain does. For
weeks before the monsoon breaks, cloud moves up the valley in the late afternoon,
wraps the ridge until nothing is visible at twenty paces, and then drains away again
after dark, leaving the leaves wet and the tanks empty. That water has always been
there. What was missing was a way of catching it.

**[2]** A fog net does nothing clever. It is a rectangle of fine plastic mesh, usually
about four metres by ten, stretched between two poles and set at right angles to the
wind. Fog is not vapour but a cloud of droplets small enough to stay airborne, and when
the wind pushes those droplets through the mesh, some of them strike a thread and stick.
Struck droplets run together, grow heavy, and slide down the mesh into a gutter at its
foot, from which a pipe carries the water to a tank. There are no moving parts and
nothing to switch on.

**[3]** The yield depends on three things: how often the fog comes, how fast the wind
drives it, and how coarse the mesh is. A mesh that is too open lets the droplets pass;
a mesh that is too dense behaves like a wall, so that the air goes round it instead of
through it, and the droplets go round with the air. The best fabrics collect roughly
half the water that passes them.

**[4]** The attraction of the method is not its output, which is modest, but its cost.
A village that installs a row of nets on the ridge needs no fuel, no electricity and no
technician; a broken panel is a sewing job. Against that must be set two real
limitations. A fog net cannot be built where there is no fog, which usually means a
ridge exposed to a moist wind, and ridges are seldom where people live. And the season
is short: in most hill districts the reliable fog lasts a few weeks, exactly the weeks
before the monsoon when the springs run lowest.

**[5]** That last coincidence is what keeps engineers interested. The technology is
poor at supplying a village all year. It is very good at carrying one dry in the worst
month of the dry season, and that, in a district where water is carried uphill by
women and children, is not a small thing.

---

**Set A — Write True, False or Not Given.** <span class="marks">[5]</span>

1. The fog described in the passage appears mainly in the afternoon.
2. A fog net has to be turned on before it will collect water.
3. A denser mesh always collects more water than an open one.
4. Fog nets cost less to install than a deep tube well.
5. In most hill districts the fog season lasts only a few weeks.

**Set B — Answer these questions.** <span class="marks">[5]</span>

6. In your own words, explain how a droplet of fog becomes a drop of water in the tank.
7. Why does a very dense mesh fail to collect water?
8. What two limitations of the method does the writer admit?
9. Why does the writer think the shortness of the fog season is not fatal to the idea?
10. Suggest a suitable title of your own for paragraph 4.

**Set C — Find a word in the passage which means:** <span class="marks">[5]</span>

11. floats or remains in the air (paragraph 2)
12. rough in texture; with wide gaps (paragraph 3)
13. the amount produced (paragraph 3 or 4)
14. small in amount (paragraph 4)
15. something that can be depended on (paragraph 4)

---

**Worked key — and where each answer comes from**

| | Answer | The evidence |
|---|---|---|
| 1 | **True** | Para 1: *cloud moves up the valley in the late afternoon*. |
| 2 | **False** | Para 2 ends: *There are no moving parts and nothing to switch on.* The passage states the opposite. |
| 3 | **False** | Para 3: *a mesh that is too dense behaves like a wall… and the droplets go round with the air*. The word **always** is contradicted. |
| 4 | **Not Given** | Para 4 says the method is cheap and needs no fuel, but a tube well is never mentioned. The comparison is not in the passage — even though it may well be true. |
| 5 | **True** | Para 4: *the reliable fog lasts a few weeks*. |
| 6 | Wind blows the fog through the mesh; some droplets hit the threads and cling to them; these join up until they are heavy enough to run down into a gutter, and a pipe takes them to the tank. | Para 2, sentences 3–4. *Note that the answer paraphrases:* strike → hit, stick → cling, slide down → run down. Copying the sentence unchanged would lose the mark. |
| 7 | Because the air cannot pass through it. It acts like a wall, so the wind goes around the net and carries the droplets around with it. | Para 3, sentence 2. |
| 8 | It can only be built on a ridge that has moist wind, which is usually far from where people live; and the fog season is only a few weeks long. | Para 4, last three sentences. Two limitations, so two halves to the answer. |
| 9 | Because those few weeks fall at the end of the dry season, when the springs are lowest — that is exactly when a village most needs the water. | Para 4 last sentence plus para 5. This is an **inference** question: the two facts are stated separately and you must put them together. |
| 10 | *Cheap but limited* (or *The bargain and its price*). | A title for a paragraph must cover the whole paragraph. Para 4 gives one advantage and two limitations, so a title naming only the cost would be incomplete. |
| 11 | **airborne** | Para 2: *droplets small enough to stay airborne*. |
| 12 | **coarse** | Para 3: *how coarse the mesh is*. |
| 13 | **yield** | Para 3: *The yield depends on three things*. |
| 14 | **modest** | Para 4: *its output, which is modest*. |
| 15 | **reliable** | Para 4: *the reliable fog lasts a few weeks*. |
:::

## 34.8 Practice passage 2, with a worked key

::: example Worked passage 34.3 — The Ledger at Thumka
**[1]** Thumka is a village of thirty-one households on a spur above the Marsyangdi,
two hours' walk from the road. Until eight years ago its only visitors were the
occasional trekker who had taken a wrong turning and the buyers who came up twice a
year for cardamom. Today eleven of its houses are registered homestays, and on a good
week in autumn the village sleeps forty guests.

**[2]** The change began with a decision that seemed, at the time, to be about
plumbing. The village committee agreed that no house could take guests until it had
built a covered toilet and a tap in the yard. Fourteen households applied; six could not
afford the pipe and dropped out. What survived that first rule was a group of families
who had each put their own money into the scheme, and who therefore argued fiercely
about how it was run.

**[3]** The second decision mattered more. Guests are not booked by individual houses.
A visitor writes to the committee, and the committee sends her to whichever registered
house is next on the roster, regardless of how comfortable that house is or how well its
owner speaks English. Ten per cent of every payment goes into a village fund; the rest
stays with the host. The roster removed at a stroke the competition that has damaged
homestay schemes elsewhere, where the two families nearest the trail take almost all
the guests and the rest drop out within three seasons.

**[4]** The village fund has since paid for a water tank, the repair of the trail and,
last year, a solar lamp at each of the four junctions where the path divides. None of
these was a tourist facility. The committee's rule is that the fund may only be spent
on something the village would still want if no guest ever came again.

**[5]** Thumka is not a model that can simply be copied. It had, to begin with, a
committee that people obeyed, and a trail that brought walkers past the door. What can
be copied is the pair of ideas underneath it: make the households invest before they
earn, and take the choosing of the guest out of the hands of the host.

---

**Set A — Complete each sentence with ONE WORD from the passage.** <span class="marks">[5]</span>

1. Thumka lies on a __________ above the Marsyangdi.
2. Before a house could take guests it had to build a covered toilet and a __________ in
   the yard.
3. Guests are allotted to houses by a __________ kept by the committee.
4. __________ per cent of each payment goes to the village fund.
5. The fund paid for a water tank, trail repairs and a solar __________ at each junction.

**Set B — Answer these questions.** <span class="marks">[5]</span>

6. Why did six of the fourteen applicant households drop out?
7. What, according to the writer, was the effect of the rule that the committee, and not
   the host, chooses who stays where?
8. Explain in your own words the committee's rule about spending the village fund.
9. What does the writer mean by saying that the first decision *seemed, at the time, to
   be about plumbing*?
10. Why does the writer say Thumka cannot simply be copied?

**Set C — Find a word or phrase in the passage which means:** <span class="marks">[5]</span>

11. a ridge running out from a mountain (paragraph 1)
12. a list showing whose turn it is (paragraph 3)
13. put money into something in the hope of a return (paragraph 2 or 5)
14. without paying attention to (paragraph 3)
15. immediately and completely (paragraph 3)

---

**Worked key — and where each answer comes from**

| | Answer | The evidence |
|---|---|---|
| 1 | **spur** | Para 1: *on a spur above the Marsyangdi*. A one-word answer taken from the passage unchanged — do not paraphrase in a gap-fill. |
| 2 | **tap** | Para 2: *a covered toilet and a tap in the yard*. |
| 3 | **roster** | Para 3: *whichever registered house is next on the roster*. |
| 4 | **Ten** | Para 3: *Ten per cent of every payment goes into a village fund*. |
| 5 | **lamp** | Para 4: *a solar lamp at each of the four junctions*. |
| 6 | They could not afford the pipe needed for the tap and toilet. | Para 2: *six could not afford the pipe and dropped out*. |
| 7 | It ended the competition between households. Elsewhere the families nearest the trail take nearly all the guests and the others give up, but in Thumka every registered house gets its turn. | Para 3, last sentence. The question says *effect*, so the answer must name the thing that stopped happening. |
| 8 | Money from the fund may be used only for things that would still be useful to the villagers themselves if the tourists stopped coming. | Para 4, last sentence — paraphrased. *Would still want if no guest ever came again* must be reworded. |
| 9 | That the rule about toilets and taps looked like a small practical matter, but it in fact decided who joined the scheme — only those willing to spend their own money stayed in, and they were the ones who then took it seriously. | Paras 2 and 5. An **inference**: the passage never uses the word *filter*, but *What survived that first rule…* and *make the households invest before they earn* together justify it. |
| 10 | Because Thumka already had two advantages that cannot be created to order: a committee whose decisions people actually obeyed, and a walking trail that brought visitors past the village. | Para 5, sentence 2. |
| 11 | **spur** | Para 1. |
| 12 | **roster** | Para 3. |
| 13 | **invest** | Para 5: *make the households invest before they earn*. |
| 14 | **regardless of** | Para 3: *regardless of how comfortable that house is*. |
| 15 | **at a stroke** | Para 3: *removed at a stroke the competition*. |
:::

## 34.9 Marking checklist for Question 1

| | Check | Mark at risk |
|---|---|---|
| 1 | Could I point at the line that justifies every answer? | Content |
| 2 | For *in your own words*, have I actually changed the wording? | Own-words mark |
| 3 | For a gap-fill, have I used the passage's word **unchanged**, and only one? | Content |
| 4 | Did I mark any statement False that is merely Not Given? | Precision |
| 5 | Did I use outside knowledge anywhere? Remove it. | Precision |
| 6 | Is each vocabulary answer the right part of speech? | Vocabulary |
| 7 | Does my one-word vocabulary answer fit back into the sentence? | Vocabulary |
| 8 | Two-mark questions: have I given two things? | Content |
| 9 | Does my title cover the whole passage, not just paragraph one? | Content |
| 10 | Have I answered every question, including the hard one I skipped? | Content |

## Chapter summary

- Question 1 is 15 marks in 25 minutes: typically 5 for True/False/Not Given or
  gap-fill, 5 for short answers, 5 for vocabulary in context.
- The order is: skim, **read the questions**, scan and mark the passage, write, check.
- Skimming finds the gist; scanning hunts one fact. Scan for numbers, dates and capital
  letters first — they are the easiest shapes to find.
- **True** = the passage says it. **False** = the passage says the opposite. **Not
  Given** = the passage is silent, however true the statement may be in real life.
- Watch *all, every, never, only*; comparisons that were never made; and causes the
  passage did not claim.
- Vocabulary in context: read the whole sentence, fix the part of speech, look for a
  signal, replace and test.
- An inference must have a line behind it; if nothing in the text points at it, it is a
  guess.
- *In your own words* means the words must change and the meaning must not.

## Practice questions

**Reading comprehension skills (1 mark each)**

1. What should you do immediately after skimming the passage?
   <span class="marks">[1]</span>
2. The passage says *most students walk to school*. The statement is *all students walk
   to school*. True, False or Not Given? <span class="marks">[1]</span>
3. The passage praises solar lamps and never mentions kerosene. The statement is *solar
   lamps are cheaper than kerosene*. True, False or Not Given? <span class="marks">[1]</span>
4. Why should you answer questions containing numbers and names first?
   <span class="marks">[1]</span>
5. A question asks for the meaning of *modest* as an adjective. You write *modesty*.
   What have you lost the mark for? <span class="marks">[1]</span>
6. What does *in your own words* forbid? <span class="marks">[1]</span>
7. A title is offered for a five-paragraph passage, and it names only what paragraph 1
   says. What is wrong with it? <span class="marks">[1]</span>
8. *What does 'it' in line 8 refer to?* Where do you look? <span class="marks">[1]</span>
9. Name one signal inside a sentence that gives away a difficult word's meaning.
   <span class="marks">[1]</span>
10. A two-mark question asks *What two reasons does the writer give?* You give one very
    good reason. What is the maximum you can score? <span class="marks">[1]</span>

::: note Answers
**1.** Read all the questions and underline the key word in each, before the careful reading.
**2.** **False** — *most* is not *all*, so the passage contradicts the statement.
**3.** **Not Given** — no comparison with kerosene is made anywhere in the passage.
**4.** Numbers and capital letters are the easiest shapes to scan for, so those answers cost the least time.
**5.** The part of speech. The answer must be an adjective, as the question was.
**6.** Copying the passage's wording. The meaning must survive; the words must not.
**7.** A title must cover the whole passage, not one paragraph of it.
**8.** Backwards in the text, usually at the nearest preceding noun phrase.
**9.** A definition after a comma or a dash, an example after *such as*, a contrast after *but* or *unlike*, or a restatement in the following sentence.
**10.** One mark out of two — a two-mark question wants two things.
:::

**Longer practice** <span class="marks">[15]</span>

11. Re-read Worked passage 34.2 and write, in about 80 words, a summary of how a fog net
    works and what limits its usefulness. Use no more than three sentences copied from
    the passage in any form.

::: note Model summary
A fog net is a rectangle of fine mesh hung across the wind. Airborne droplets that
strike its threads gather together, grow heavy, run down into a gutter and are piped to
a tank; nothing has to be powered or switched on. It is cheap, and a village can mend it
with a needle. Its usefulness is limited, however, by geography and by season: it needs
a ridge with a moist wind, which is rarely where houses stand, and in most hill
districts the dependable fog lasts only a few weeks. *(78 words)*
:::

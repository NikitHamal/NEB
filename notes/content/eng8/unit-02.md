---
subject: Compulsory English
grade: 8
unit: 2
title: A Father's Letter to his Son / Poem: Changing
hours: 0
area: Units
---

This unit pairs two pieces of advice. The first is a father's **letter of
advice** to his son, written in a warm, personal tone rather than the formal
tone of a business letter. The second is a **poem about change** — about how a
person grows, and how the world around us will not stay the same. Both texts
say the same thing in different ways: advice is what one generation hands to
the next, and change is the one thing you cannot refuse. The unit also teaches
**yes/no questions** and the two writing tasks of the year: completing a
skeleton story, and writing an e-mail.

::: key What this unit asks of you
By the end you should be able to (1) explain what makes a letter of advice
different from a formal letter, in tone, point of view and structure, (2) find
the **speaker** and the **theme** of a poem and explain how the poem shows
change, (3) turn statements into yes/no questions and answer them with a short
answer, (4) write an e-mail with a subject line, a greeting, a body and a
sign-off, and (5) complete a skeleton story so that it has a beginning, a
middle and an end.
:::

## 2.1 A Father's Letter to his Son

### About the text

The text is a **letter of advice**: a parent writing to a child who is growing
up. It is not a request letter and not a business letter. Its purpose is to
guide, warn and encourage, and its tone is affectionate — the writer is
allowed to use the word *dear*, to remember shared moments and to speak
directly to the reader as *you*.

### What the text says

A father writes to his son at a moment of change in the boy's life — a new
school, a new class, or the beginning of more responsibility. He does not begin
with rules. He begins by **remembering**: a time when the boy was small, a
thing the boy once did, something the father noticed but never said. That
memory is what makes the advice land; advice from a stranger is a lecture, and
advice from someone who knows you is help.

The advice itself is ordinary and therefore useful. Work steadily rather than
in bursts. Choose friends who make you better. Tell the truth even when it
costs you something. Respect your teachers, and do not be afraid to ask them a
question. Read something that is not on the syllabus. Keep your body strong and
your temper quiet. Be kind to those who cannot repay you. And when you fail —
because you will fail — do not confuse failing at something with being a
failure.

The letter closes by handing over the responsibility. The father says, in
effect, that he cannot live his son's life for him, and that he does not want
to. That last movement — from advice to trust — is the **point of view** of the
whole letter. It is written *to* the son, but it is also written *past* the son,
for the reader who will one day understand it.

### Tone, point of view and structure

| Feature | In a letter of advice | In a formal letter |
|---|---|---|
| Tone | warm, personal, encouraging | polite, impersonal, brief |
| Point of view | first person — *I*, *you* | third person — *the undersigned*, *the students* |
| Salutation | *My dear son,* | *Dear Sir,* |
| Closing | *Your loving father,* | *Yours faithfully,* |
| Structure | memory → advice → trust | purpose → details → request |
| Length of paragraphs | short and uneven; each idea gets its own | long and even |

```figure caption="The movement of a letter of advice. It begins in the past with a shared memory, builds through practical advice, and ends by handing responsibility to the son — which is what makes the reader trust it."
fig, ax = plt.subplots(figsize=(4.9, 2.7))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.0); ax.axis("off")
stages = [("Shared memory", "creates trust", SERIES[0]),
          ("Advice, given kindly", "work, friends, truth,\nhealth, kindness", SERIES[3]),
          ("Warning, not scolding", "failing is not\nbeing a failure", ACCENT),
          ("Handing over trust", "\"I cannot live\nyour life for you\"", SERIES[2])]
for i, (title, note, colour) in enumerate(stages):
    x = 0.35 + i * 2.45
    ax.add_patch(plt.Rectangle((x, 2.5), 2.15, 1.5, fc="white", ec=colour, lw=1.4))
    ax.text(x + 1.07, 3.72, title, ha="center", va="center", fontsize=6.6,
            color=INK, fontweight="bold")
    ax.text(x + 1.07, 3.02, note, ha="center", va="center", fontsize=5.9, color=MUTED)
    if i < 3:
        ax.annotate("", xy=(x + 2.45, 3.25), xytext=(x + 2.2, 3.25),
                    arrowprops=dict(arrowstyle="->", color=GRID, lw=1.4))
ax.text(5.0, 1.5, "topic of each paragraph follows this order", ha="center",
        fontsize=6.4, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| advice | an opinion about what somebody should do |
| to encourage | to give somebody confidence to do something |
| responsibility | a duty you are trusted to carry out |
| steadily | at a regular pace, without stopping and starting |
| to hand over | to give control or responsibility to somebody else |
| in effect | in fact, when you look at what was really said |

### Questions and model answers

**1. Why does the father begin with a memory instead of a rule?**
A shared memory proves that he knows his son. Advice that follows a memory
sounds like help; the same sentence from a stranger sounds like a lecture.

**2. What does the father mean by "do not confuse failing at something with
being a failure"?**
A failed test, a lost match or a broken promise is an event, not a person. You
may fail at a hundred things and still be a good, capable person — what matters
is what you do next.

::: note Model answers
**3. Find two pieces of advice from the letter and say why each is useful for
a student of your age.**
(a) *Work steadily rather than in bursts* — because a small amount every day
beats a whole night before the examination. (b) *Do not be afraid to ask a
teacher a question* — because a doubt that is not cleared today becomes a
chapter you cannot understand next month.
**4. What is the tone of the letter? How do you know?**
It is warm and encouraging. The writer uses *dear*, addresses the boy as
*you*, remembers small personal things, and never orders him about.
:::

## 2.2 Poem: Changing

### About the poem

The poem is about **change** — the change that happens inside a person as they
grow up, and the change that happens in the world around them. Poems are not
read the way a story is read. A story tells you what happens; a poem makes you
*feel* what happens, using fewer words, repeated sounds and pictures in the
mind.

### The speaker, the theme and the images

**The speaker** of a poem is the voice that says it. It is not always the poet:
the poet may write as a child, as an old man, or as a river. Always ask, "Who
is talking?" before you answer anything else. In this poem the speaker is
looking back at an earlier self and noticing how much has altered — and then
looking forward, and accepting that more will alter still.

**The theme** is the idea the poem keeps returning to. Here the theme is
change: that growing up means losing some things and gaining others, that
nothing stays exactly as it is, and that the healthy response is not to fight
the change but to keep something steady inside it.

**The images** are the pictures the poem uses to make the idea visible. A
favourite device is the seasons: spring, summer, autumn and winter stand in for
childhood, youth, middle age and age. A tree that loses its leaves and grows
them again, a river that is never the same water twice, a road that curves out
of sight — all are pictures of change. When a poem asks a question and does not
answer it, that is deliberate: the question is meant to stay in your head.

```figure caption="How a poem on change is built. The speaker moves from looking back, to looking around, to accepting what is coming — and the questions left unanswered are the point, not a fault."
fig, ax = plt.subplots(figsize=(4.7, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.axis("off")
ax.annotate("", xy=(9.4, 1.1), xytext=(0.5, 1.1),
            arrowprops=dict(arrowstyle="->", color=GRID, lw=1.6))
ax.text(9.3, 0.62, "time", fontsize=6.4, color=MUTED, ha="right")
steps = [("1. Looking back", 1.7), ("2. Looking around", 4.3), ("3. Looking ahead", 7.0)]
for label, x in steps:
    ax.plot(x, 1.1, "o", color=ACCENT, ms=7)
    ax.text(x, 1.55, label, ha="center", fontsize=6.8, color=INK, fontweight="bold")
ax.text(1.7, 3.1, "childhood:\neasy, familiar", ha="center", fontsize=6.1, color=MUTED)
ax.text(4.3, 3.6, "what I have lost\nand what I have gained", ha="center",
        fontsize=6.1, color=MUTED)
ax.text(7.0, 3.1, "the future:\naccepted, not feared", ha="center", fontsize=6.1,
        color=MUTED)
ax.add_patch(plt.Rectangle((0.5, 4.4), 8.9, 1.3, fc="white", ec=SERIES[2], lw=1.3))
ax.text(4.95, 5.05, "theme: change   ·   tone: thoughtful, hopeful", ha="center",
        va="center", fontsize=6.6, color=SERIES[2])
fig.tight_layout()
```

### Themes and questions and model answers

**1. What is the theme of the poem?**
Change — in oneself and in the world — and the importance of accepting it while
holding on to what matters.

**2. Who is the speaker?**
A person older than the child in the poem, looking back at how they have
changed and forward at what is still to come. The speaker is not necessarily
the poet.

::: note Model answers
**3. Pick one image from the poem and explain what it stands for.**
The tree that sheds its leaves and grows new ones every year stands for a
person who loses something — a habit, a fear, a friend — and then grows
something else in its place. The tree is not damaged by the change; it is how
it stays alive.
**4. Does the poem see change as good or bad?**
As unavoidable, and then as good. The speaker admits that something has been
lost, but does not wish to go back, which is what makes the tone hopeful rather
than sad.
:::

## 2.3 Grammar and writing tasks of the unit

### Grammar: Yes/no questions

A **yes/no question** is one that can be answered with *yes* or *no*. It is made
by putting the helping verb before the subject. If there is no helping verb,
use *do*, *does* or *did*.

| Statement | Yes/no question | Short answer |
|---|---|---|
| You are a student. | **Are** you a student? | Yes, I am. / No, I am not. |
| He writes poems. | **Does** he write poems? | Yes, he does. / No, he does not. |
| They went home. | **Did** they go home? | Yes, they did. / No, they did not. |
| She can swim. | **Can** she swim? | Yes, she can. / No, she cannot. |
| We have finished. | **Have** we finished? | Yes, we have. / No, we have not. |

Two rules matter in the examination. First, a short answer repeats the helping
verb and never just says *Yes* or *No* alone. Second, a **negative** yes/no
question shows surprise or an expectation: *Don't you like the poem?* — meaning
"I thought you did."

::: caution Common mistakes
- *Do he write poems?* ✗ — third person singular needs **does**: *Does he write
  poems?* ✓
- *Yes, I.* ✗ — the short answer needs the helping verb: *Yes, I **do**.* ✓
- Answering a yes/no question in one word sounds abrupt; in a conversation or a
  letter, follow it with a sentence: *Yes, I am. I joined last week.*
:::

### Writing I: Completing a skeleton story

A skeleton story gives you the beginning and the end and leaves the middle to
you. Plan it in four moves before you write a single sentence:

1. **Setting** — who, where, when. One or two sentences.
2. **Problem** — something goes wrong or is missing.
3. **Attempts** — two or three tries; the first two may fail.
4. **Resolution** — the last attempt succeeds, and there is a point to it.

Write in the **past simple** for the events, and use *suddenly*, *then*,
*after that*, *at last* to move the story forward. Keep one tense. Nothing
loses marks faster than a story that slides between past and present.

::: example Worked example
**Skeleton.** *Ramesh was walking home when he saw an envelope on the road. …
He reached home tired but happy.*

**Completed middle.** He picked it up. Inside was a bank card and a slip of
paper with a telephone number. He looked around, but the road was empty.
He waited ten minutes; nobody came. He took it home and dialled the number.
A woman answered, and she began to cry: the card was her mother's, and the
pension money for the whole month was in the account. Ramesh cycled back to the
market and handed the envelope to her. She offered him a hundred rupees, and he
said no.
:::

### Writing II: Writing an e-mail

An e-mail has six parts, and an examiner looks for each one:

| Part | Example |
|---|---|
| To | sujata.sharma@example.com |
| Subject | Request for a leave of three days |
| Greeting | Dear Madam, |
| Body | short paragraphs, one idea each |
| Closing | Yours sincerely, / Best regards, |
| Signature | Name, class and roll number |

::: tip The examiner is looking for
A **subject line that is not empty**. An e-mail with no subject is the single
commonest lost mark in this question. After that: a greeting, a body of two or
three short paragraphs, a closing that matches the greeting, and your name.
Keep the language slightly more formal than a chat message — no "plz", no
"u", no emoji.
:::

::: note Key to Exercise A
**1.** Does she sing well? **2.** Did they arrive late? **3.** Are you ready?
**4.** Can he drive? **5.** Have we finished? **6.** Do they live here?
**7.** Was she happy? **8.** Will it rain?
:::

## Chapter summary

- A letter of advice is warm and personal: it uses the first person, begins
  with a shared memory and ends by handing responsibility to the reader.
- Its structure is memory → advice → trust, and its tone is encouraging, never
  scolding.
- A poem has a **speaker** (the voice), a **theme** (the idea it returns to)
  and **images** (the pictures that make the idea visible).
- The theme of "Changing" is that change is unavoidable and can be accepted.
- A yes/no question begins with a helping verb; if there is none, use *do*,
  *does* or *did*.
- A short answer repeats the helping verb: *Yes, he does.* Not *Yes, he.*
- A skeleton story is planned in four moves: setting, problem, attempts,
  resolution — and written in one tense.
- An e-mail needs a subject line, a greeting, short body paragraphs, a closing
  and a signature.

## Practice questions

**Reading**

1. What is a letter of advice? Give two features that make it different from a
   formal letter. <span class="marks">[2]</span>
2. Why does the father say that he cannot live his son's life for him? <span class="marks">[2]</span>
3. In the poem, who is the speaker and what is the theme? <span class="marks">[2]</span>
4. Read these lines and answer: *"Everything I knew has altered, / and I did
   not ask it to."* What does the speaker feel here? <span class="marks">[2]</span>

::: note Answers
**1.** A letter giving somebody guidance about how to live or act. It is warm
and personal rather than polite and impersonal, and it uses the first person
(*I* speaking to *you*) instead of the third person.
**2.** Because advice can only help somebody who then acts; the father can
guide, warn and encourage, but the choices — and their consequences — belong to
the son.
**3.** The speaker is someone looking back at their younger self and forward at
the future; the theme is change.
**4.** Surprise and a little helplessness: the change happened without his or
her permission. It prepares the reader for the acceptance that comes later in
the poem.
:::

**Grammar**

5. Make yes/no questions from these statements. <span class="marks">[5]</span>
   (a) He plays the flute. (b) They were at home. (c) You can ride a bicycle.
   (d) She has finished her homework. (e) We went to Mustang.

6. Give short answers — one affirmative and one negative — for each question
   in 5. <span class="marks">[5]</span>

::: note Answers
**5.** (a) Does he play the flute? (b) Were they at home? (c) Can you ride a
bicycle? (d) Has she finished her homework? (e) Did we go to Mustang?
**6.** (a) Yes, he does. / No, he does not. (b) Yes, they were. / No, they were
not. (c) Yes, I can. / No, I cannot. (d) Yes, she has. / No, she has not.
(e) Yes, we did. / No, we did not.
:::

**Writing**

7. Complete this skeleton story in about 120 words. <span class="marks">[5]</span>
   *Anita found a small dog outside the school gate. … She named it Kalu.*
8. Write an e-mail to your class teacher asking for leave for three days
   because of an illness. <span class="marks">[5]</span>

::: note Answers
**7.** Plan: setting (school gate, after the last period) → problem (the dog is
hurt and nobody claims it) → attempts (the guard says no; her mother says no) →
resolution (the vet treats the leg, the mother agrees to keep it, they name it
Kalu). Keep the whole story in the past simple and finish with the effect on
Anita.
**8.** Subject: *Request for leave of three days*. Dear Sir/Madam, I am
writing to ask for leave from … to … because I am suffering from fever and the
doctor has advised three days' rest. I will complete the work I miss. Thank
you. Yours sincerely, name, class, roll number.
:::

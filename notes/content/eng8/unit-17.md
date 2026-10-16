---
subject: Compulsory English
grade: 8
unit: 17
title: Naresh and the Stranger / Poem: From a Railway Carriage
hours: 0
area: Units
---

A story with suspense and a poem about a journey seen from a train window. The
story is about a decision — whether to trust a stranger — and the poem is about
speed and observation: everything is seen for a second and then gone. The
grammar of the unit is **voice**: the difference between a sentence that says
who did something and a sentence that says what was done.

::: key What this unit asks for
By the end you should be able to (1) explain how a story builds suspense,
(2) describe the rhythm and the imagery of a poem, (3) change a sentence from
the active voice to the passive and back, and (4) write an e-mail and a reply
letter to an invitation.
:::

## 17.1 Naresh and the Stranger

### About the text

The text is a **short story** built on suspense. Suspense is not the same as
surprise: surprise is a sudden event, while suspense is the reader's
**uncertainty** about what will happen next, and it is built deliberately.

### How suspense is built

| Device | What it does | Where you see it |
|---|---|---|
| A stranger | an unknown person whose motives are hidden | the beginning |
| A small doubt | one detail that does not fit | early in the story |
| Limited information | the reader knows only what Naresh knows | throughout |
| Delay | the decision is put off, and the waiting is described | the middle |
| A false resolution | something seems settled, then is not | just before the end |
| The decision | the character acts, and the suspense ends | the climax |

A story like this is a test of **character** as well as of the reader's nerves.
Naresh has to decide something about a person he does not know, on incomplete
information, and whatever he decides says something about him. That is why the
story is not really about the stranger: it is about what Naresh is willing to
believe.

The **setting** does quiet work too. A road, a bus park, an evening, a place
where nobody else is — a setting with few people in it makes a stranger
important, because there is nobody else to ask.

```figure caption="Suspense is a graph, not a moment. The writer raises the reader's uncertainty step by step, holds it, and releases it only when the character decides."
fig, ax = plt.subplots(figsize=(4.8, 2.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")
xs = [0.6, 2.2, 3.8, 5.4, 7.0, 8.6, 9.4]
ys = [0.8, 1.6, 2.4, 3.4, 3.6, 2.2, 0.9]
labels = ["meets\nthe stranger", "", "first\ndoubt", "the wait", "close\nto harm",
          "false\nresolution", "decision"]
ax.plot(xs, [y + 0.8 for y in ys], color=ACCENT, lw=2)
for x, y, lab in zip(xs, ys, labels):
    ax.plot(x, y + 0.8, "o", color=ACCENT, ms=4.5)
    if lab:
        ax.text(x, y + 1.55, lab, ha="center", fontsize=5.8, color=INK)
ax.text(5.0, 0.25, "reader's uncertainty", ha="center", fontsize=6.1, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| stranger | a person you do not know |
| suspense | the feeling of not knowing what will happen next |
| motive | the reason a person does something |
| to trust | to believe that somebody is honest and safe |
| hesitation | a pause before deciding |
| resolution | the point at which the problem is settled |

::: note Model answers
**1. How does the writer build suspense in this story?**
By giving the reader only what Naresh knows: an unknown stranger, a small doubt
about him, a delay while Naresh decides, and a moment near the end when the
situation seems settled and then is not.
**2. Why is the setting important?**
Because a place with few other people in it makes one stranger matter — Naresh
has nobody else to ask, so the decision is his alone.
:::

## 17.2 Poem: From a Railway Carriage

### About the poem

The poem describes what a passenger sees from the window of a moving train. It
is by **Robert Louis Stevenson** and appears in his collection *A Child's Garden
of Verses* (1885). Its subject is speed, and its method is to put one image after
another with no pause, so that the reader feels the train's hurry.

### Rhythm, rhyme and imagery

The poem's **rhythm** imitates the train. The lines are short, the beat is
strong and regular, and the rhymes come in pairs — *fairies / witches*,
*battle / cattle*, *plain / rain* — which gives a click at the end of every two
lines, exactly like wheels crossing the joints in the rail.

The **imagery** is all sight, because that is all a passenger has. Bridges,
houses, hedges, ditches, meadows, cattle, a tramp, a cart, a mill, a river and a
station all arrive and vanish. Notice the words that make speed: *fly*,
*whistle by*, *in the wink of an eye*. Notice also that the poet does not
describe any one thing fully. The **incompleteness is the point**: at speed you
catch a glimpse, not a picture.

The **theme** is that travel turns the world into a series of pictures, and that
the traveller sees everything and touches nothing. It is a child's wonder at
speed, and it is also a quiet observation about how quickly things pass.

### Vocabulary

| Word | Meaning |
|---|---|
| carriage | a coach of a train |
| hedge | a line of bushes forming a boundary |
| ditch | a long narrow channel beside a road or field |
| wink | a very short moment |
| tramp | a person who walks from place to place with no fixed home |
| glimpse | a quick, incomplete look |

::: note Model answers
**1. How does the rhythm of the poem imitate the train?**
The lines are short with a strong regular beat, and the rhymes come in pairs, so
the poem moves in a steady series of clicks, like wheels crossing the rail
joints.
**2. Why does the poet not describe anything fully?**
Because a passenger at speed only catches a glimpse: the things arrive and are
gone. Leaving each image incomplete is what makes the reader feel the speed.
:::

## 17.3 Grammar and writing tasks of the unit

### Grammar: Voice — active and passive

In the **active** voice the subject does the action. In the **passive** voice
the subject receives it.

| | Form | Example |
|---|---|---|
| Active | subject + verb + object | The train **carried** the passengers. |
| Passive | subject + be + past participle (+ by …) | The passengers **were carried** by the train. |

The passive is used (1) when the doer is unknown or unimportant — *My bag **has
been stolen***; (2) in formal and scientific writing — *The samples **were
tested***; and (3) when the thing done matters more than the doer.

| Tense | Active | Passive |
|---|---|---|
| Present simple | He writes a letter. | A letter **is written**. |
| Past simple | She broke the glass. | The glass **was broken**. |
| Present perfect | They have finished it. | It **has been finished**. |
| Future | We will announce it. | It **will be announced**. |
| Modal | You must sign it. | It **must be signed**. |

::: caution Common mistakes
- *The letter was wrote.* ✗ → *The letter was **written**.* ✓ (past participle,
  not past simple)
- Leaving out the auxiliary: *The window broken by him.* ✗ → *The window **was**
  broken by him.* ✓
- Using the passive when the active is stronger and shorter. Prefer *The
  caretaker opened the gate* to *The gate was opened by the caretaker* unless
  the gate is the subject of the sentence.
:::

### Writing: An e-mail and a reply to an invitation

An e-mail needs the six parts: *To*, *Subject*, greeting, short body paragraphs,
closing and signature. A reply to an invitation is either **accepting** or
**declining**, and both must be polite and definite:

- Accepting: thank the host, say you are glad to come, confirm the date and
  time, and ask if anything is needed.
- Declining: thank the host, say you are sorry, give a **brief** reason (not a
  long excuse), and wish the event well. Never leave an invitation unanswered:
  the host is counting chairs.

::: note Model answers to the practice questions
**Declining model.** "Dear Sunita, Thank you very much for inviting me to your
sister's birthday party on Saturday. I am sorry that I will not be able to come,
as I am visiting my grandmother in Dhading that day, and we will not be back
until Sunday. I hope the party goes very well, and please wish your sister a
happy birthday from me. Yours, Binod."
:::

## 17.4 Describing a journey: the language of narrative

| Function | Useful expressions |
|---|---|
| Setting the scene | *It was a cold morning in Poush …*, *We set out just after dawn.* |
| Sequencing | *first, then, after that, meanwhile, at last* |
| Describing movement | *the train rattled past*, *we climbed steadily*, *the bus crawled uphill* |
| Sudden events | *all of a sudden*, *before we knew it*, *out of nowhere* |
| Sensory detail | *the smell of wet earth*, *the clang of the bell*, *the taste of smoky tea* |
| Closing a narrative | *By the time we reached home …*, *Looking back, I realise …* |

```figure caption="The shape of a narrative. Marks in a story or a memoir come from the middle — the complication and the climax — not from a long introduction."
stages = ["Orientation\n(who, where, when)", "Complication",
          "Climax", "Resolution", "Reflection"]
fig, ax = plt.subplots(figsize=(5.0, 2.4))
xs = np.arange(len(stages))
ys = [0.25, 0.55, 0.9, 0.5, 0.3]
ax.plot(xs, ys, color=SERIES[0], linewidth=2.2, marker="o", markersize=7)
for x, y, lab in zip(xs, ys, stages):
    ax.annotate(lab, xy=(x, y), xytext=(x, y + 0.14), ha="center",
                fontsize=7.6, color=INK)
ax.set_ylim(0, 1.25)
ax.set_xlim(-0.5, len(stages) - 0.5)
ax.axis("off")
```

::: note Activity — the journey in six sentences
Think of a journey you remember — to school in the monsoon, to a relative's
village, a first bus ride alone. Write exactly six sentences, one for each
stage of the narrative shape above, plus one sensory detail somewhere.
Read it aloud to a partner; the partner names the stage each sentence belongs
to. If two sentences land in the same stage, rewrite one.
:::

::: example From flat to vivid
**Flat.** *We went to Pokhara by bus. It took a long time. We were tired. The
lake was nice.*

**Vivid.** *We left Kathmandu at five in the morning, when the air still smelt
of last night's rain. For seven hours the bus swung round the bends above the
Trishuli, and by Mugling my brother had stopped complaining and fallen asleep
on my shoulder. Then, just as the light was going, the valley opened and the
lake lay flat and grey below us — and nobody in the bus said anything at all.*

The second version adds no new events. It adds **time**, **place**, **a sense**
and **one small human detail** — which is exactly what the marks reward.
:::

## Chapter summary

- Suspense is the reader's uncertainty about what happens next, built by a
  stranger, a small doubt, limited information, delay and a false resolution.
- A story about a trust decision is really a story about the character who has
  to make it.
- "From a Railway Carriage" is by Robert Louis Stevenson (*A Child's Garden of
  Verses*, 1885); its short lines and paired rhymes imitate the sound of a
  train.
- Its imagery is entirely visual, and its incompleteness is what conveys speed.
- **Active**: the subject does the action. **Passive**: be + past participle,
  used when the doer is unknown or unimportant, or when the action matters more.
- An e-mail has *To*, *Subject*, greeting, body, closing and signature.
- A reply to an invitation must be definite — accepting with thanks, or
  declining with thanks and a brief reason.

## Practice questions

**Reading**

1. Give three devices the writer uses to build suspense. <span class="marks">[3]</span>
2. What is the difference between suspense and surprise? <span class="marks">[2]</span>
3. How does the poem's rhythm suit its subject? <span class="marks">[2]</span>
4. What is the theme of "From a Railway Carriage"? <span class="marks">[2]</span>

::: note Answers
**1.** A stranger whose motives are unknown; a small doubt or detail that does
not fit; delay while the character decides; and a false resolution near the end.
**2.** Surprise is a sudden event that the reader did not expect; suspense is the
reader's continuing uncertainty about what will happen, which the writer builds
over the whole story.
**3.** The lines are short with a strong regular beat, and the rhymes come in
pairs, so the poem moves with the click of a train's wheels crossing the rail
joints.
**4.** That travel turns the world into a series of glimpses — the traveller sees
everything at speed and is part of none of it.
:::

**Grammar**

5. Change into the passive. <span class="marks">[5]</span>
   (a) The driver stopped the train. (b) They have repaired the bridge.
   (c) Somebody has stolen my bag. (d) The school will publish the results.
   (e) You must sign this form.

::: note Answers
**5.** (a) The train was stopped by the driver. (b) The bridge has been
repaired. (c) My bag has been stolen. (d) The results will be published by the
school. (e) This form must be signed.
:::

**Writing**

6. Write an e-mail to a friend inviting them to your school's sports day. <span class="marks">[4]</span>
7. Write a reply declining an invitation to a wedding, giving a brief reason. <span class="marks">[5]</span>

::: note Answers
**6.** Subject line: *Invitation to our sports day*. Greeting, then: what the
event is, the date and time, where it is, and why you want your friend there.
Close with *Yours* or *Best wishes* and your name.
**7.** Thank the host first, say you are sorry not to be able to come, give one
brief reason, wish the couple well, and sign off politely. Do not explain at
length — a short reason is more polite than a long excuse.
:::

**Extra practice**

**Group B (2 marks each)**

**11.** Rewrite with sensory detail: *It was raining and we waited for the bus.*
**12.** Join using *as soon as*: *The bell rang. The children ran out.*

**Group C (4 marks)**

**13.** Write a short memoir (about 120 words) of a day that did not go as planned.

::: note Extra practice — answers
**11.** e.g. *Rain hammered on the tin roof of the shelter, and we stood
shoulder to shoulder, watching the empty road and smelling the wet dust.*
**12.** *As soon as the bell rang, the children ran out.*
**13.** Marks: the five narrative stages in order; past tense held
consistently; at least two sensory details; one short reflection at the end;
and correct paragraphing with no more than five serious language errors.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** A narrative usually opens with
   (a) the climax (b) the orientation (c) the resolution (d) the moral
**2.** *All of a sudden* is used to signal
   (a) sequence (b) a sudden event (c) a conclusion (d) a reason
**3.** *The train rattled past* appeals mainly to
   (a) sight (b) sound (c) smell (d) taste
**4.** The stage after the complication is the
   (a) orientation (b) climax (c) reflection (d) setting
**5.** A narrative is normally written in the
   (a) past tense (b) present simple (c) future (d) imperative

::: note Objective practice — answers
**1.** (b) — the orientation: who, where, when. **2.** (b) — a sudden event. **3.** (b) — sound. **4.** (b) — the climax. **5.** (a) — the past tense.
:::

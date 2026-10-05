---
subject: Compulsory English
grade: 8
unit: 5
title: The Old Woman and the Lime Tree / Poem: Free Birds
hours: 0
area: Units
---

A story and a poem, both about the same question: what do we owe to the living
things we share the world with, and what is the difference between keeping
something and loving it? The story is a **folk tale** — a short narrative with a
clear plot, few characters and a message at the end. The poem, **Free Birds**,
is a lyric about freedom: birds that will not trade the open sky for the
safest, warmest cage. This unit teaches you how a story is put together (plot,
character, message) and the two language skills that go with it — reported
speech for imperatives, and punctuation.

::: key What this unit asks of you
By the end you should be able to (1) tell the **plot** of a story in five
stages, (2) describe a **character** from what they do and say rather than from
what you feel about them, (3) state the **message** of a story in one sentence,
(4) report an order or a request in indirect speech, and (5) punctuate direct
speech correctly.
:::

## 5.1 The Old Woman and the Lime Tree

### About the text

The text is a **folk tale** — a story that was told aloud long before anybody
wrote it down. Folk tales are short, have very few characters, and end with a
message you can state in one sentence. They often use a rule of three: three
wishes, three attempts, three days. If you can find the rule of three in a folk
tale, you have usually found its structure.

### How a story is put together

Every story, from a folk tale to a film, has the same five parts. Learning their
names gives you the words to answer any question about plot.

| Stage | What happens | Typical question |
|---|---|---|
| Exposition | we meet the characters and the setting | Who is the story about, and where? |
| Rising action | a problem appears and grows | What goes wrong? |
| Climax | the moment of decision or danger | What is the turning point? |
| Falling action | the result of that moment | How is it settled? |
| Resolution | the new situation, and the message | What has changed, and what does it teach? |

In this story the two characters are an **old woman** — poor, alone, and
practical, because she must be — and a **lime tree**, the large shade tree that
grows beside her house. The tree gives her shade in summer, dead wood for her
fire in winter, and the lime flowers whose scent fills the yard. Around this
relationship the tale builds its problem: what does the old woman do when the
tree is inconvenient — when its roots reach the wall of the house, when it takes
the water she needs, when a neighbour offers her money for the timber?

That question is the whole of the tale, and it is why folk tales last. It is
not really a question about a tree. A tree cannot argue. It is a question about
the **weak** — those who cannot speak for themselves but whose lives depend on
our decision.

```figure caption="The five stages of the plot. A folk tale moves quickly through the first three and takes its time over the last two, because the message lives there."
fig, ax = plt.subplots(figsize=(4.9, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.4); ax.axis("off")
xs = [1.0, 3.0, 5.0, 7.0, 9.0]
hs = [1.0, 1.9, 3.4, 2.4, 1.5]
labels = ["exposition", "rising\naction", "climax", "falling\naction", "resolution"]
for x, y, lab in zip(xs, hs, labels):
    ax.plot([x, x], [0.8, 0.8 + y], color=ACCENT, lw=3)
    ax.text(x, 0.6 + y + 0.22, lab, ha="center", fontsize=6.3, color=INK)
ax.plot(xs, [0.8 + h for h in hs], color=GRID, lw=1.2, ls="--")
ax.text(5.0, 0.2, "the decision at the climax decides the message",
        ha="center", fontsize=6.2, color=MUTED)
fig.tight_layout()
```

### Character and message

A folk tale never tells you what a character *is*; it shows you what they *do*.
So describe a character with evidence.

| Character | What they do | What it shows |
|---|---|---|
| The old woman | keeps the tree although it costs her | she values what she cannot sell |
| The lime tree | gives shade, wood and flowers without being asked | nature gives before it is asked |
| The neighbour / the buyer | offers money for the timber | things that seem free always have a price attached |

The **message** of a tale like this is usually one of two: either *take care of
what takes care of you*, or *what is worth having is worth paying for*. Say
which one you think the tale means and give the moment in the story that proves
it. A message without evidence from the text is only your opinion, and the
examiner will say so.

### Vocabulary

| Word | Meaning |
|---|---|
| lime tree | a large tree with heart-shaped leaves and sweet-smelling flowers (the linden) |
| timber | wood cut and prepared for building |
| shade | the shadow of a tree, where the sun does not reach |
| roots | the part of a plant that holds it and takes in water |
| folk tale | an old story handed down by word of mouth |
| moral | the lesson a story teaches |

::: note Model answers
**1. Where is the climax of this story?**
At the moment the old woman must decide — when the tree has become
inconvenient and she is offered money for it. That single decision contains the
whole message.
**2. Why is a folk tale short and simple?**
Because it was told aloud, to a listening audience, and had to be remembered
exactly and finished in one sitting. Few characters and a repeated pattern
(three attempts, three days) make it easy to remember.
:::

## 5.2 Poem: Free Birds

### About the poem

The poem is a lyric about **freedom**. Its speaker watches birds and notices
that they refuse every comfort that would cost them their liberty. The poem
does not argue; it shows. That is what poetry does — it puts a picture in your
head and lets the picture do the arguing.

### Image, contrast and theme

The poem works by **contrast**, and contrast is the easiest device to write
about in an examination.

| The cage | The open sky |
|---|---|
| food given, not found | food found, not given |
| safe from hawks and cold | exposed to hawks and cold |
| a small, known space | a huge, unknown space |
| the bird is kept | the bird is itself |

The **speaker** admires what the birds choose. The **theme** is that freedom is
worth more than safety, and that a life without risk is not a full life. Notice
that the poem does not say this in a sentence anywhere. It says it by placing
the two pictures side by side and trusting the reader to feel the difference.

A useful examination technique: when a poem asks a question and does not answer
it, the question **is** the answer. Ask yourself what the question makes you
feel, and write that feeling down with the line that caused it.

```figure caption="The poem's argument is made of contrast, not of statement. Put the two lives side by side and the reader supplies the conclusion."
fig, ax = plt.subplots(figsize=(4.8, 2.7))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
ax.add_patch(plt.Rectangle((0.5, 1.0), 4.1, 3.7, fc="white", ec=GRID, lw=1.3))
ax.add_patch(plt.Rectangle((5.4, 1.0), 4.1, 3.7, fc="white", ec=ACCENT, lw=1.4))
ax.text(2.55, 4.4, "the cage", ha="center", fontsize=7, color=MUTED,
        fontweight="bold")
ax.text(7.45, 4.4, "the sky", ha="center", fontsize=7, color=ACCENT,
        fontweight="bold")
for i, t in enumerate(["food provided", "no hawks", "known walls", "safe"]):
    ax.text(2.55, 3.75 - i * 0.62, t, ha="center", fontsize=6.3, color=MUTED)
for i, t in enumerate(["food sought", "real danger", "no walls", "free"]):
    ax.text(7.45, 3.75 - i * 0.62, t, ha="center", fontsize=6.3, color=INK)
ax.text(5.0, 0.4, "theme: freedom is worth more than safety",
        ha="center", fontsize=6.6, color=SERIES[2])
fig.tight_layout()
```

::: note Model answers
**1. What is the theme of "Free Birds"?**
That freedom matters more than comfort and safety, and that a caged life — even
a kind cage — is not a full life.
**2. How does the poet make the reader agree without arguing?**
By contrast. He shows the food, shelter and safety of the cage and then shows
the birds refusing them, and the reader's own sense of which matters more does
the rest.
**3. Who is the speaker of the poem?**
Someone watching the birds from outside — an observer who admires their choice,
not the birds themselves.
:::

## 5.3 Grammar and writing tasks of the unit

### Grammar: Reported speech — imperatives

An **imperative** is an order, a warning or a request: *Close the door. Don't
touch it. Please help me.* When you report one, you do not report a tense at
all — you use **told** (for an order), **asked** (for a request) or **warned**
(for a warning), plus **to** or **not to** and the verb.

| Direct | Reported |
|---|---|
| "Close the window," she said. | She **told** me **to** close the window. |
| "Please help me," he said. | He **asked** me **to** help him. |
| "Don't touch the wire," she said. | She **warned** me **not to** touch the wire. |
| "Stand up," the teacher said. | The teacher **told** us **to** stand up. |
| "Please don't be late," mother said. | Mother **asked** us **not to** be late. |

Notice the three changes: the reporting verb becomes *told / asked / warned*,
the imperative becomes **to + verb**, and the pronoun changes to fit the new
speaker. The word *please* disappears.

::: caution Common mistakes
- *She told to close the window.* ✗ — *told* needs a person: *She told **me** to
  close the window.* ✓
- *He asked me close the door.* ✗ — *He asked me **to** close the door.* ✓
- *She said me to sit down.* ✗ — *She **told** me to sit down.* ✓
- *He told me don't go.* ✗ — *He told me **not to** go.* ✓
:::

### Grammar: Punctuation of direct speech

The punctuation of a quotation is fixed, and examiners mark it.

1. Put the spoken words inside **quotation marks**.
2. Put a **comma** after the reporting clause (or before it, if the quoting
   comes first).
3. Start the quotation with a **capital letter**.
4. Put the **full stop or question mark inside** the closing quotation marks.
5. Start a **new line and a new paragraph** when a different person speaks.

*She said, "I am tired."* — *"I am tired," she said.* — *"Are you tired?" she
asked.*

### Writing: Completing a skeleton story

Plan the four moves — setting, problem, attempts, resolution — and use the
rule of three for the attempts. Write the whole story in the past simple, and
give the last line to the message rather than a moral in bold.

::: tip The examiner is looking for
In a story question: a clear beginning, one problem (not four), and a proper
ending. In a reported-speech question: the right reporting verb (*told* for an
order, *asked* for a request), **to** before the verb, and *not to* for a
negative. In a punctuation question: the comma in the right place and the full
stop inside the quotation marks.
:::

## Chapter summary

- A **folk tale** was told aloud before it was written; it is short, has few
  characters, often uses a rule of three, and ends with a message.
- Every plot has five stages: exposition, rising action, climax, falling
  action, resolution.
- Describe a character from what they **do**, not from what you feel about them.
- The theme of the story is the relationship between a person and a living
  thing that cannot speak for itself; the message is proved by the climax.
- "Free Birds" shows, through **contrast** between the cage and the sky, that
  freedom is worth more than safety.
- Reported imperatives use *told / asked / warned* + object + **to** + verb,
  and **not to** for negatives.
- In direct speech the quotation takes a capital letter, the comma goes after
  the reporting clause, and the full stop or question mark goes **inside** the
  quotation marks.

## Practice questions

**Reading**

1. Name the five stages of a plot. <span class="marks">[5]</span>
2. Why does the old woman keep the lime tree even when it costs her? Answer
   from what she does in the story. <span class="marks">[2]</span>
3. What is the theme of the poem "Free Birds"? <span class="marks">[2]</span>
4. Give two things the poem contrasts. <span class="marks">[2]</span>

::: note Answers
**1.** Exposition, rising action, climax, falling action, resolution.
**2.** Because the tree gives her shade, wood and flowers without being asked,
and she values what she cannot sell; the story shows her choosing the tree over
the money offered for its timber.
**3.** That freedom is worth more than safety and comfort, and that a caged
life, however kind the cage, is not a full life.
**4.** The cage and the open sky; or food given and food found; or safety and
risk.
:::

**Grammar**

5. Report these sentences. <span class="marks">[5]</span>
   (a) "Shut the gate," he said. (b) "Please lend me your book," she said.
   (c) "Don't walk on the grass," the guard said. (d) "Wait here," mother
   said. (e) "Please don't tell anyone," he said.

6. Punctuate correctly. <span class="marks">[3]</span>
   (a) sit down said the teacher (b) are you coming with us she asked
   (c) don't move he whispered the snake is near

::: note Answers
**5.** (a) He told me to shut the gate. (b) She asked me to lend her my book.
(c) The guard warned us not to walk on the grass. (d) Mother told me to wait
there. (e) He asked me not to tell anyone.
**6.** (a) "Sit down," said the teacher. (b) "Are you coming with us?" she
asked. (c) "Don't move," he whispered. "The snake is near."
:::

**Writing**

7. Complete the story in about 120 words. *An old man planted a lime tree
   beside the road. Thirty years later, a boy came with an axe. … the old man
   smiled.* <span class="marks">[5]</span>
8. Write a paragraph of about 80 words on why freedom matters more than
   comfort, using one example from the poem. <span class="marks">[4]</span>

::: note Answers
**7.** Setting: the lime tree, now huge, shading the road. Problem: the boy
wants its wood — his family needs the money. Attempts: he raises the axe; the
old man asks him to sit in the shade first; a woodcutter offers a cheaper
price. Resolution: the shade is worth more than the timber, the boy puts the
axe down, and the old man smiles. End with what the boy understood.
**8.** Take the clearest image from the poem — for example the birds refusing
food that is offered inside the cage — and say plainly what it costs them and
what it wins them.
:::

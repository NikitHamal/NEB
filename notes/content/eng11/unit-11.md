---
subject: Compulsory English
grade: 11
unit: 11
title: Who are you, little i?
hours: 3
area: Literature — Poems
---

This poem is eight short lines long, contains one sentence, and has not a single
capital letter in it. An adult looks back at himself as a child of five or six,
standing at a high window watching a November sunset. The child thinks that if
the day must end, this is a lovely way for it to go — and the grown man, much
closer to his own ending, finds that the child was right.

::: key What the exam wants from this poem
Three things. **Who "little i" is** (the poet's own childhood self, not another
person). **What the sunset stands for** (the end of the day, and behind it the
end of a life). And **why the unusual typography is deliberate** — the lower-case
"i", the missing spaces, the brackets. Never call them printing mistakes.
:::

## 11.1 About the poet

Edward Estlin Cummings (14 October 1894 – 3 September 1962) was an American poet,
painter, playwright and novelist. He was born at Cambridge, Massachusetts, the
son of a Harvard teacher who later became a minister, and he took two degrees at
Harvard. In 1917 he went to France as a volunteer ambulance driver in the First
World War and was held for three months in a French detention camp after a
censor misread his friend's letters; he turned the experience into his prose book
*The Enormous Room* (1922).

His poetry collections include *Tulips and Chimneys* (1923), *is 5* (1926), *No
Thanks* (1935) and *95 Poems* (1958), in which "who are you,little i" appears as
poem 12. He wrote some 2,900 poems in all, and he was also a serious painter —
which matters, because he treated the page as a surface to design as well as a
place to print words.

Cummings belongs to **modernism**, the movement that broke with inherited forms
in the early twentieth century. His own signature was **typographical
experiment**: lower-case letters where capitals are expected, brackets opening
inside sentences, punctuation without spaces, words split across lines, invented
compounds. Underneath the experiments his subjects are surprisingly traditional —
love, spring, childhood, the individual against the crowd, and death. One small
point of fact: his name is often printed as "e. e. cummings", but this styling
came from publishers and from the look of his poems; he himself signed his name
with capitals.

## 11.2 Summary

The poem is a single unbroken stanza of eight lines and a single sentence. It
divides naturally into two halves.

### Lines 1–4 — the question and the child at the window

The poem opens with a question — "who are you,little i" — addressed to a small
child who is, we soon realise, the speaker himself at the age of five or six. The
age is given in brackets, as though it were a quiet aside. The child is
"peering" — looking hard and with concentration — out of a high window. The word
"high" tells us two things at once: the window is upstairs, and the child is
small. He is not playing; he is watching something, and the sentence carries us
over the line-break to find out what.

### Lines 5–8 — the sunset and the child's thought

What he is watching is "the gold / of november sunset". November is late autumn,
the year's own evening, and the sunset is the day's ending; the one colour named
is gold, which makes the ending rich rather than sad. The last three lines, again
placed in brackets, give us the child's own feeling: that **if** the day has to
turn into night, then this is a beautiful way for it to happen. Nothing more is
said. The poem has no full stop; it closes with a bracket and leaves the child at
the window.

The force of the poem lies in what it does not spell out. An old poet is asking
his childhood self a question, and the child's answer — the acceptance of a
beautiful ending — turns out to be the answer the adult needs about his own life.

```figure caption="The shape of the poem: eight short lines, the rhyme pattern A B A B  C D E D, and the two bracketed asides."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
syl = [6,5,5,5,6,6,5,7]
rhyme = ["A","B","A","B","C","D","E","D"]
pairs = {"A":ACCENT, "B":"#0B6A62", "D":"#A8271F"}
ys = np.arange(8)[::-1]
for i in range(8):
    c = pairs.get(rhyme[i], "#9aa3b0")
    ax.barh(ys[i], syl[i], color=c, height=0.52, alpha=0.85)
    ax.text(syl[i]+0.12, ys[i], f"{syl[i]} syllables", va="center",
            fontsize=7.6, color=MUTED)
    ax.text(-0.25, ys[i], f"line {i+1}", va="center", ha="right",
            fontsize=8.0, color=INK)
    ax.text(-2.15, ys[i], rhyme[i], va="center", ha="center", fontsize=9.6,
            color=c, fontweight="bold")
ax.text(-2.15, 8.05, "rhyme", ha="center", va="bottom", fontsize=7.6, color=MUTED)
for y0, y1, lab in [(6,6,"aside 1:\nthe child's age"), (0,2,"aside 2:\nthe child's thought")]:
    ax.plot([10.6,11.0,11.0,10.6], [y1+0.34, y1+0.34, y0-0.34, y0-0.34],
            color=MUTED, lw=1.1)
    ax.text(11.2, (y0+y1)/2, lab, va="center", ha="left", fontsize=7.6,
            color=MUTED, linespacing=1.4)
ax.text(-2.6, -1.25, "One sentence.  No capital letters.  No full stop at the end.",
        fontsize=8.2, color="#A8271F", ha="left")
ax.set_xlim(-3.0, 15.0); ax.set_ylim(-1.7, 8.5); ax.axis("off")
```

## 11.3 Themes

**Childhood and the wisdom in it.** The child is not taught anything by the poem;
the child does the teaching. A five-year-old, without arguing about it,
understands something about endings that adults spend their lives avoiding.

**Memory and identity.** "Who are you" is a real question. Are we the same person
as the child we once were? The poem keeps the two apart — one asks, the other is
looked at — and yet the whole poem is one voice. The self is both continuous and
strange to itself.

**The beauty of transience.** The day is ending, the year is ending (November),
the light is going. The poem's answer is not to deny this but to notice how
beautiful it is while it happens.

**Acceptance of death.** The sunset is the oldest symbol in poetry for the close
of a life. The child's thought — if day *has* to become night, this is a
beautiful way — is a quiet statement about dying, made by someone too young to
know it.

**Smallness before a large world.** The "i" is lower-case and little; the window
is high; the sunset fills the sky. The poem sets a very small watcher against a
very large evening, and finds the relation between them peaceful rather than
frightening.

**Innocence and perception.** Cummings believed children see more clearly than
adults because they have not yet learned what they are supposed to see. The poem
is an argument for that belief rather than a statement of it.

## 11.4 Form, structure and rhyme

**Stanza form.** One stanza of eight lines, unpunctuated by any full stop, written
as a single continuous sentence. The lines are short: five to seven syllables
each. There is no regular metre, so the poem is **free verse** — but it is
controlled free verse, since the line lengths hardly vary.

**Rhyme scheme.** The poem does rhyme, which surprises many students:

- lines 1–4: **A B A B** — "i" rhymes with "high", "old" with "gold"
- lines 5–8: **C D E D** — "day" rhymes with "way", while "sunset" and "night"
  are left unrhymed

So the first half is tightly woven and the second half loosens, as if the poem
were relaxing into thought. The one rhyme that survives in the second half links
"day" to "way" — that is, links the thing that is ending to the manner of its
ending, which is exactly the poem's subject.

**The typography is the poem.** This is the central point of any question on form.

| What Cummings does | Why he does it |
|---|---|
| writes "i" in lower case | makes the self small, modest and childlike; the capital "I" of the adult ego is refused |
| drops the space after punctuation — "you,little", "window;at", "feeling:that" | the words crowd together the way a child's excited speech does, and the eye is forced to slow down |
| uses no capital letter even for "november" | levels everything: no word is more important than any other |
| puts lines 2 and 6–8 inside brackets | creates an inner voice — a thought inside a thought — so the child's feeling is overheard rather than announced |
| breaks the line at "high / window" | leaves "high" hanging at the end of the line, so the word is physically raised above the one it belongs to |
| ends with a bracket and no full stop | the moment is not closed off; the child is still at the window |

::: caution Not mistakes
Every one of these is a choice. In an examination, never write that the poet "has
made errors in capitalisation" or that the poem is "wrongly punctuated". The
correct answer is that Cummings uses **deliberate typographical experiment** to
make the printed page carry meaning, and then explain what a particular choice
achieves.
:::

**Enjambment.** Almost every line runs on into the next without a pause: "some
high / window", "the gold / of november sunset". Because the sentence never
stops, reading the poem feels like one continuous act of looking — which is what
the child is doing.

**What the form does for the meaning.** A poem about a small self quietly
accepting an ending is written in small, quiet, lower-case units that never come
to a stop. Form and subject are the same thing here.

```figure caption="The movement of the poem: a question travels back sixty years, and an answer comes forward."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.7))
def box(x, w, title, sub, col):
    ax.add_patch(FancyBboxPatch((x, 0.34), w, 0.34,
        boxstyle="round,pad=0.010,rounding_size=0.03", fc="white", ec=col, lw=1.6,
        transform=ax.transAxes, zorder=2))
    ax.text(x+w/2, 0.585, title, ha="center", va="center", fontsize=9.2,
            color=col, fontweight="bold", transform=ax.transAxes, zorder=3)
    ax.text(x+w/2, 0.445, sub, ha="center", va="center", fontsize=7.8,
            color=MUTED, transform=ax.transAxes, zorder=3, linespacing=1.4)
box(0.02, 0.40, "the grown poet", "looking back,\nnear his own evening", ACCENT)
box(0.58, 0.40, "little i", "five or six, at a high\nwindow, watching gold", "#A8271F")
ax.annotate("", xy=(0.575, 0.625), xytext=(0.425, 0.625), xycoords=ax.transAxes,
            textcoords=ax.transAxes,
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=12))
ax.text(0.50, 0.70, "the question:\n\"who are you\"", ha="center", va="bottom",
        fontsize=8.0, color=INK, transform=ax.transAxes, linespacing=1.4)
ax.annotate("", xy=(0.425, 0.395), xytext=(0.575, 0.395), xycoords=ax.transAxes,
            textcoords=ax.transAxes,
            arrowprops=dict(arrowstyle="-|>", color="#0B6A62", lw=1.4, mutation_scale=12))
ax.text(0.50, 0.325, "the answer, carried forward:\nan ending can be beautiful",
        ha="center", va="top", fontsize=8.0, color="#0B6A62",
        transform=ax.transAxes, linespacing=1.4)
ax.text(0.50, 0.06, "one voice, one sentence, sixty years apart", ha="center",
        va="center", fontsize=8.0, color=MUTED, transform=ax.transAxes)
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
```

## 11.5 Poetic devices

The poem is modern and in copyright, so only short phrases are quoted below.

| Device | Example | Effect |
|---|---|---|
| Apostrophe (self-address) | "who are you,little i" | The poet speaks to his own past self, turning memory into a conversation |
| Symbolism | the "november sunset" | Stands for the end of a day, the end of a year, and the end of a life, all at once |
| Symbolism | the window | A frame between the small watcher inside and the large world outside |
| Metaphor | the gold of the sunset | The dying light is treated as treasure, so the ending is valuable rather than pitiable |
| Personification | the day that "has to become night" | Day and night are given the obligation of living creatures, which quietly brings in mortality |
| Imagery (visual) | "peering from some high / window;at the gold" | One clear picture holds the entire poem: a small figure, a high window, a gold sky |
| Simile | none used | Cummings gives us the thing itself rather than a comparison — worth saying in an answer, because the absence is a choice |
| Hyperbole (mild) | "some high" window | To a five-year-old an upstairs window is enormously high; the exaggeration is the child's, not the poet's |
| Alliteration | "who ... you"; "beautiful ... become" | Light sound-links hold the short lines together in place of a metre |
| Enjambment | "some high / window" ; "the gold / of november sunset" | The sentence never stops, so reading becomes one long act of looking |
| Parenthesis | the bracketed lines 2 and 6–8 | Creates a private inner voice; the child's thought is overheard, not declared |
| Typography | lower-case "i", "november"; no spaces after punctuation | Shrinks the self, levels all words, and slows the eye down on the page |
| Ambiguity | "who are you" | Both a real question to a remembered child and a question about what a self is |

## 11.6 Glossary

| Word | Meaning |
|---|---|
| peering | looking hard and with effort, especially at something far away or half-hidden |
| gold | here, the colour of the low sun; also suggests something precious |
| november | the eleventh month; in the northern hemisphere, late autumn, just before winter |
| sunset | the daily disappearance of the sun below the horizon |
| typography | the arrangement and appearance of printed letters on the page |
| lower case | small letters, as opposed to capitals |
| parenthesis | a word, phrase or passage inserted into a sentence, often inside brackets |
| syntax | the arrangement of words into sentences |
| free verse | poetry with no fixed metre or rhyme scheme |
| enjambment | the running on of a sentence from one line of verse into the next without a pause |
| apostrophe | a direct address to someone absent, or to a thing or idea |
| modernism | the early twentieth-century movement that broke deliberately with inherited artistic forms |
| persona | the assumed voice or character through which a poem speaks |
| transience | the quality of lasting only a short time |
| mortality | the condition of being subject to death |
| innocence | freedom from experience of the world's harm; here, a way of seeing clearly |
| nostalgia | a fond and slightly sad longing for the past |
| ambiguity | the quality of having more than one possible meaning, often on purpose |

## Chapter summary

- "who are you,little i" is poem 12 of E. E. Cummings's *95 Poems* (1958): eight
  lines, one sentence, no capital letters, no full stop.
- The speaker, an old poet, addresses his own self at five or six, remembered
  standing at a high window and watching a gold November sunset.
- The child's thought — if the day has to become night, this is a beautiful way —
  is an acceptance of endings, and by extension of death.
- Rhyme: **A B A B** in lines 1–4 (i/high, old/gold) and **C D E D** in lines 5–8
  (day/way). The poem is otherwise **free verse**, with short, nearly equal lines
  and continuous enjambment.
- The typography is the meaning: the lower-case "i" makes the self small and
  humble; the missing spaces crowd the words; the brackets make a private inner
  voice; the missing full stop leaves the moment open.
- Themes: childhood wisdom, memory and identity, the beauty of transience,
  acceptance of death, and smallness before a large world.

## Practice questions

**Short answer questions (2 marks each)**

1. Who is "little i" in the poem, and who is asking the question? <span class="marks">[2]</span>
2. What is the child doing, and where? <span class="marks">[2]</span>
3. Why does the poet choose a **November** sunset rather than a summer one? <span class="marks">[2]</span>
4. Why is the pronoun "i" written in lower case? <span class="marks">[2]</span>
5. Write the rhyme scheme of the poem. <span class="marks">[2]</span>
6. What is the effect of putting the last three lines inside brackets? <span class="marks">[2]</span>
7. Why does the poem have no full stop at the end? <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** "little i" is the poet's own self as a child of five or six, remembered
many years later. The questioner is the grown poet. The poem is therefore a
conversation between one person's two selves, which is why the same small "i"
serves for both.

**2.** He is "peering" — looking hard and with concentration — out of a high
window, watching the gold of a November sunset. He is alone, still, and completely
absorbed in what he sees.

**3.** November is late autumn in the northern hemisphere, the last month before
winter, so the year itself is ending. Putting the day's ending inside the year's
ending doubles the idea of things drawing to a close, and prepares us for the
poem's real subject, the end of a life.

**4.** To make the self small and humble. A capital "I" would put the speaker at
the centre of the poem; the lower-case "i" matches the size of a five-year-old
child at a high window and keeps him in proportion to the enormous sunset he is
watching. It is one of Cummings's trademark devices, not an error.

**5.** Lines 1–4 rhyme **A B A B** ("i" with "high", "old" with "gold"); lines 5–8
rhyme **C D E D** ("day" with "way", while "sunset" and "night" do not rhyme with
anything). Apart from this the poem is free verse.

**6.** The brackets turn the last three lines into a private, inner voice — the
child's own feeling, thought rather than spoken. We seem to overhear it instead of
being told it, which makes the poem's large statement about death sound gentle and
unforced.

**7.** Because a full stop would close the moment. Cummings ends on a bracket
instead, leaving the child still standing at the window and the light still going.
The thought is left open, so the reader carries it on rather than filing it away.
:::

**Long answer questions (5 marks each)**

1. Discuss the significance of the sunset in "who are you,little i". <span class="marks">[5]</span>
2. "In this poem the typography is not decoration; it is the meaning." Discuss. <span class="marks">[5]</span>
3. What view of childhood does the poem present? How does the adult speaker
   relate to the child? <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** The sunset is the centre of the poem and its main symbol. On the surface it
is simply what the child can see: the gold of the sky at the end of a November
afternoon, watched from an upstairs window. But every detail is chosen to make it
mean more. It is a **sunset**, the oldest image in poetry for the close of a life.
It is in **November**, so the year is in its own late afternoon, with winter next.
The only colour named is **gold**, which turns the fading light into something
precious rather than something lost. And it is watched through a **window**,
which frames it like a picture and keeps the small watcher separate from the vast
sky. The child's response makes the symbolism explicit: if day *has* to become
night, this is a beautiful way for it to happen. The word "has to" admits that the
ending is not optional. What the child offers is not denial but acceptance — the
recognition that an ending can be beautiful. Read back through the grown poet who
asks the opening question, the sunset therefore becomes his own. A man near the
end of his life asks his childhood self what to think about endings, and is given
a gold sky as the answer.

**2.** Cummings trained as a painter, and he treats the printed page as a surface
to be designed. In this poem every unusual mark does a job. The **lower-case "i"**
refuses the tall capital of the adult ego and makes the speaker small — the exact
size of a five-year-old, and the right size to stand under a whole sky. The
**missing spaces** after the comma, semicolon and colon ("you,little",
"window;at", "feeling:that") press the words together, so the eye has to slow down
and pick them apart; the effect is of speech hurrying, and of a child's attention
that does not pause where grammar says it should. The **brackets** around the
second line and the last three create a second, quieter voice inside the poem, so
the child's feeling is overheard rather than announced — which is why so large a
thought about death can be carried by so small a poem. The **line-break** at "some
high / window" leaves the word "high" hanging at the edge of the line, raised
above the noun it describes. Keeping **"november"** in lower case levels every
word, so no part of the picture shouts. Finally, the **absent full stop** refuses
to close the moment. Take away these choices, print the poem in ordinary
sentences, and nothing survives but a pleasant memory of a sunset. The typography
is not a style laid over the meaning; it is how the meaning exists.

**3.** The poem presents childhood as a state of clear seeing rather than of
ignorance. The child does nothing remarkable — he stands at a window and looks —
but his looking is total, which is what "peering" conveys. He is not told about
the sunset and does not describe it to anyone; he simply receives it, and out of
that receiving comes a thought that most adults never manage: that if an ending
must come, it can come beautifully. Cummings gives the child no argument and no
consolation, only acceptance, and that is precisely the point. The relation
between the two selves is the poem's structure. The adult asks; the child, sixty
years back and without knowing he is answering, replies. The question "who are
you" holds the two apart — the man cannot simply step back into the boy — while
the single unbroken sentence and the single small "i" hold them together. The
grown poet, writing in his sixties and nearer his own night than his morning,
goes back to his earliest self not for nostalgia but for instruction. That is the
poem's quiet reversal: the small, lower-case, five-year-old "i" turns out to be
the wiser of the two.
:::

**Reference to the context**

1. The poem opens by asking a small child of five or six who he is, and then
   shows him peering from a high window.
   (a) Who asks the question, and whom does he address? (b) Why is the word
   "high" placed at the end of its line? (c) What does the opening question
   suggest about identity? <span class="marks">[5]</span>
2. The child, watching the last gold light of a November evening, feels that if
   the day has to turn into night, this is a beautiful way for it to happen.
   (a) What is the child looking at? (b) What larger meaning does this carry?
   (c) Why are these lines placed inside brackets? <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) The question is asked by the grown poet, E. E. Cummings, and he
addresses his own self as a small child — the "little i" he once was. The poem is
a conversation between two selves of the same person.
(b) Because of **enjambment**. The sentence runs on to "window" in the next line,
so "high" is left hanging at the line's edge with nothing after it. The word is
physically raised above the noun it belongs to, and the reader has to climb to the
window just as the small child had to.
(c) It suggests that the self is not simple. The adult can see the child clearly,
yet has to ask who he is, as though looking at a stranger; and at the same time
the poem is one sentence in one voice, with the same small "i" used throughout. We
are both continuous with the children we were and separated from them, and the
poem holds both truths without resolving them.

**2.** (a) He is looking through a high window at the gold of a November sunset —
the last light of a late-autumn day.
(b) The sunset is a symbol for the end of a life, and November, the last month
before winter, doubles the idea of things closing. The child's feeling — that if
the ending must come, it may come beautifully — is therefore a quiet acceptance of
death, arrived at innocently by someone far too young to know what he has said.
Because the poet asking the question is himself an old man, that childhood
acceptance becomes the answer he is looking for.
(c) The brackets make the words an inner voice rather than a statement. We seem to
overhear the child's private thought instead of being lectured, and the poem's
largest idea therefore arrives in its smallest, softest form. The bracket that
closes the poem also takes the place of a full stop, so the moment is never quite
shut.
:::

---
subject: Compulsory English
grade: 11
unit: 9
title: A Red, Red Rose
hours: 3
area: Literature — Poems
---

"A Red, Red Rose" is probably the best-known love song in the English language,
and it is barely sixteen lines long. Robert Burns took two old Scottish folk
songs, reshaped them, and produced a lyric that says only one thing — I love you
and I will not stop — but says it with such music that it has been sung for more
than two hundred years. This unit looks at how so plain a statement is made so
memorable.

::: key What the exam wants from this poem
Know the **two similes** of the first stanza, the **three impossible conditions**
of stanzas two and three, and the **turn to farewell** in stanza four. Be able to
name the form (ballad stanza, ABCB) and to explain why exaggeration here sounds
sincere rather than silly.
:::

## 9.1 About the poet

Robert Burns (25 January 1759 – 21 July 1796) is the national poet of Scotland.
He was born at Alloway in Ayrshire, the eldest son of a poor tenant farmer, and
he spent his short life close to the hard farm work that ruined his health. He
died at Dumfries at the age of thirty-seven.

Burns published his first collection, *Poems, Chiefly in the Scottish Dialect*
(known as the Kilmarnock edition), in 1786. Its success made him famous overnight
in Edinburgh, where he was admired — and patronised — as the "heaven-taught
ploughman". His major poems include "Tam o' Shanter", "To a Mouse", "To a
Louse", "Ae Fond Kiss", "Scots Wha Hae" and "Auld Lang Syne", which is still sung
across the world at the turn of the year. In his last years he worked without
payment on two great song collections, James Johnson's *The Scots Musical Museum*
and George Thomson's *Select Collection*, hunting down old Scottish airs and
writing new words for them. "A Red, Red Rose" (1794) came out of exactly that
work: Burns himself described it as a simple old song which he had taken down and
set to music.

Burns wrote in **Scots**, the language of ordinary Ayrshire speech, at a time when
polished English was expected of poets. That choice, together with his interest in
strong personal feeling, folk song and the lives of the poor, makes him a
**forerunner of the Romantic movement**; Wordsworth and Coleridge, whose *Lyrical
Ballads* appeared two years after Burns's death, admired him greatly. Scotland
still keeps his birthday as Burns Night.

## 9.2 Summary

### Stanza 1 — Two similes

> O my Luve's like a red, red rose,
> That's newly sprung in June;
> O my Luve's like the melodie
> That's sweetly play'd in tune.

The speaker compares his beloved to two things. First to a rose — not any rose,
but a **red** one that has **just** opened in June, so the comparison carries
colour, freshness, perfection and the height of summer. Then to a **melody**
sweetly played in tune. The first comparison appeals to the eye, the second to
the ear; the first is a thing of nature, the second a thing of art. Together they
say that the beloved is both beautiful to look at and harmonious to live with.

### Stanza 2 — The first vow

> As fair art thou, my bonnie lass,
> So deep in luve am I;
> And I will luve thee still, my dear,
> Till a' the seas gang dry.

Now the speaker moves from description to promise. The construction is careful:
*as* beautiful as you are, *so* deeply am I in love — his love is measured by her
beauty. He then swears to go on loving her until all the seas dry up, which is to
say for ever, since the seas will not dry up.

### Stanza 3 — The vow made larger

> Till a' the seas gang dry, my dear,
> And the rocks melt wi' the sun;
> And I will luve thee still, my dear,
> While the sands o' life shall run.

The stanza opens by repeating the last line of stanza two, so the two stanzas
lock together like links in a chain — a device taken straight from folk song. The
impossible condition is then raised higher: not only until the seas dry, but until
the very rocks melt in the heat of the sun. The last line quietly changes the
measure from the life of the earth to the life of a man: he will love her while
"the sands o' life shall run", that is, as long as the sand keeps falling through
the hourglass of his own life.

### Stanza 4 — The farewell

> And fare-thee-weel, my only Luve!
> And fare-thee-weel, a while!
> And I will come again, my Luve,
> Tho' 'twere ten thousand mile!

Only in the final stanza do we learn that the lovers are about to be separated.
The whole poem has in fact been a parting speech. The speaker says goodbye twice,
then softens it at once with "a while" — this is not an ending but an interval —
and promises to return even if ten thousand miles lie between them. The poem
closes on movement towards the beloved rather than away from her, which is why it
feels joyful and not sad.

```figure caption="Stanza 1 scanned. Four iambic feet in the long lines, three in the short; only the B lines rhyme."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
lines = [
  (["O","my","Luve's","like","a","red,","red","rose,"], "A", "4 feet (tetrameter)"),
  (["That's","new-","ly","sprung","in","June;"],        "B", "3 feet (trimeter)"),
  (["O","my","Luve's","like","the","me-","lo-","die"],  "C", "4 feet (tetrameter)"),
  (["That's","sweet-","ly","play'd","in","tune."],      "B", "3 feet (trimeter)"),
]
u = 0.0175
for r, (syls, letter, note) in enumerate(lines):
    y = 0.84 - r*0.20
    pos = 0.035
    for i, sy in enumerate(syls):
        w = (len(sy) + 1.7) * u
        cx = pos + w/2
        ax.text(cx, y+0.062, "x" if i % 2 == 0 else "/", ha="center", va="center",
                fontsize=9.5, color=MUTED if i % 2 == 0 else ACCENT, fontweight="bold")
        ax.text(cx, y, sy, ha="center", va="center", fontsize=8.6, color=INK)
        pos += w
    c = "#A8271F" if letter == "B" else MUTED
    ax.text(0.80, y, letter, ha="center", va="center", fontsize=11,
            color=c, fontweight="bold")
    ax.text(0.86, y, note, ha="left", va="center", fontsize=7.8, color=MUTED)
ax.plot([0.765,0.765],[0.18,0.92], color=GRID, lw=1.0)
ax.text(0.035, 1.00, "x = unstressed       / = stressed", fontsize=8.2, color=MUTED)
ax.text(0.035, 0.04, "Rhyme scheme A B C B  \u2014  only the B lines rhyme:  June / tune",
        fontsize=8.2, color="#A8271F")
ax.set_xlim(0,1.14); ax.set_ylim(0.0,1.05); ax.axis("off")
```

## 9.3 Themes

**The intensity of young love.** The poem does not analyse love or doubt it. It
simply declares it at full volume, with the confidence of a folk singer rather
than the caution of a philosopher.

**Love against time.** Every vow in the poem is a vow about duration. Seas, rocks
and sand are all images of time — geological time in the first two, a human
lifetime in the third. Love is set against the largest clocks the speaker can
imagine, and claims to outlast them.

**Beauty and nature.** The beloved is praised only through natural and musical
images: a June rose, a tune. Burns finds the language of love in the countryside
he worked in, not in classical mythology.

**Separation and constancy.** The parting of the last stanza gives the poem its
occasion. Distance is admitted — ten thousand miles of it — and then dismissed.
Constancy is the proof of love, and absence is the test it must pass.

**The folk tradition.** Repetition, simple diction, the linking of stanzas and the
singable rhythm all come from oral song. The poem belongs to ordinary people, and
that is part of what it is saying about love.

## 9.4 Form, structure and rhyme

**Stanza form.** Four **quatrains** (four-line stanzas) in the **ballad stanza**,
also called common metre — the oldest and most singable stanza in English and
Scots verse.

**Metre.** The long lines are in **iambic tetrameter** (four iambs) and the short
lines in **iambic trimeter** (three iambs). An **iamb** is a foot of two
syllables, an unstressed one followed by a stressed one — the sound *da-DUM*.
Scanning line 1:

> O **my** | Luve's **like** | a **red**, | red **rose**

Four feet, eight syllables. Line 2 has three:

> That's **new**- | ly **sprung** | in **June**

Two small irregularities are worth noticing, because examiners like them. In line
1 "red, red rose" wants a stress on both *reds*, so the third foot pushes against
the iambic beat and the repetition is pressed on our attention. And in stanza 3
the short lines carry an extra light syllable ("And the rocks melt wi' the sun"),
which keeps the singing rhythm from becoming mechanical.

**Rhyme scheme.** **ABCB** in every stanza — only the second and fourth lines
rhyme:

- Stanza 1: rose (A), June (B), melodie (C), tune (B)
- Stanza 2: lass (A), I (B), dear (C), dry (B)
- Stanza 3: dear (A), sun (B), dear (C), run (B)
- Stanza 4: Luve (A), while (B), Luve (C), mile (B)

**What the form does for the meaning.** The half-rhymed ABCB pattern leaves the
long lines free and un-tied, so the poem moves forward easily, the way speech and
song do, while the returning B rhyme gives just enough closure to each stanza. The
alternation of four beats and three leaves a silent beat at the end of every short
line — exactly the gap a singer fills with the tune. And the **chain link**
between stanzas 2 and 3, where the last line of one becomes the first line of the
next, is a technique of oral ballad: it makes the vow sound repeated, sworn twice,
the way real promises are.

::: tip Answering a "form" question
Never answer only "it is a four-stanza poem". Name the ballad stanza, name iambic
tetrameter and trimeter, write out ABCB, quote one line to show the *da-DUM* beat,
and finish with one sentence on what the form achieves. Those five moves are the
five marks.
:::

## 9.5 Poetic devices

| Device | Example | Effect |
|---|---|---|
| Simile | "my Luve's like a red, red rose" | Gives the beloved the colour, freshness and perfection of a flower at its peak |
| Simile | "like the melodie / That's sweetly play'd in tune" | Adds sound to sight: she is harmony as well as beauty |
| Metaphor | "the sands o' life" | Life becomes an hourglass, so the vow is measured against the speaker's own death |
| Personification | "the rocks melt wi' the sun" | The stubborn earth is made to give way, as if nature itself could be overcome by time |
| Hyperbole | "Till a' the seas gang dry"; "ten thousand mile" | Deliberate exaggeration that measures love against impossibility |
| Alliteration | "red, red rose"; "sweetly ... sprung" | The repeated consonants make the lines sing and slow the reader on the key words |
| Imagery | the June rose, dry seas, melting rocks, running sand | Abstract love is made visible in four sharp pictures |
| Enjambment | "O my Luve's like a red, red rose, / That's newly sprung in June" | The sense runs over the line-break, so the voice flows instead of stopping |
| Repetition | "red, red"; "fare-thee-weel ... fare-thee-weel"; "my dear" | Insistence; the mark of a song rather than a speech |
| Refrain / chain link | "Till a' the seas gang dry" ending stanza 2 and opening stanza 3 | Binds the stanzas and makes the promise sound sworn twice |
| Symbolism | the red rose | Beauty, passion and love — but also, since roses fade, the pressure of time behind the poem |
| Dialect (Scots) | "Luve", "bonnie lass", "gang", "wi'", "a'" | Roots a universal feeling in a real place and a real speaking voice |
| Apostrophe | "O my Luve"; "fare-thee-weel, my only Luve!" | The beloved is addressed directly, so we overhear a conversation, not a description |

## 9.6 Glossary

| Word | Meaning |
|---|---|
| Luve | love; Burns uses it both for the feeling and for the beloved person |
| newly sprung | just come into flower |
| melodie | melody, tune |
| play'd | played (the apostrophe marks a dropped letter, as in song) |
| in tune | correctly pitched; in harmony |
| fair | beautiful |
| art thou | are you (old second-person singular) |
| bonnie | pretty, fine, healthy-looking (Scots) |
| lass | girl, young woman (Scots) |
| thee | you (object form, old singular) |
| still | always, continually — not "even now" |
| a' | all (Scots) |
| gang | go (Scots); "gang dry" = run dry |
| wi' | with |
| sands o' life | the sand in an hourglass, standing for the time a person has to live |
| fare-thee-weel | farewell, goodbye |
| a while | for a short time only |
| Tho' 'twere | though it were |
| ballad stanza | a four-line stanza rhyming ABCB, with lines of four and three beats |
| iamb | a metrical foot of one unstressed then one stressed syllable (da-DUM) |

```figure caption="Syllables per line across the whole poem. The 8–6–8–6 pulse of the ballad stanza repeats four times; the two seven-syllable lines in stanza 3 take one extra light syllable."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.7))
counts = [8,6,8,6, 8,6,8,6, 8,7,8,7, 8,6,8,6]
letters = list("ABCB")*4
cols = [ACCENT if c >= 8 else "#8FB8DA" for c in counts]
xs = np.arange(16)
ax.bar(xs, counts, color=cols, width=0.68)
for i, c in enumerate(counts):
    ax.text(i, c+0.18, str(c), ha="center", va="bottom", fontsize=7.6, color=INK)
ax.set_xticks(xs); ax.set_xticklabels(letters, fontsize=8.2, color="#A8271F")
ax.set_ylim(0,9.9); ax.set_ylabel("syllables in the line")
ax.set_xlabel("rhyme letter, line by line")
for b in (3.5, 7.5, 11.5):
    ax.axvline(b, color=GRID, lw=1.0)
for i, s in enumerate(["stanza 1","stanza 2","stanza 3","stanza 4"]):
    ax.text(1.5+4*i, 9.4, s, ha="center", va="center", fontsize=7.8, color=MUTED)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis="y", alpha=.45)
ax.set_axisbelow(True)
```

## Chapter summary

- "A Red, Red Rose" (1794) by Robert Burns is a four-stanza Scots love song built
  from older folk material.
- Stanza 1 praises the beloved with **two similes** (a newly opened red rose; a
  sweetly played melody); stanzas 2 and 3 swear love **until the seas dry, the
  rocks melt, and the speaker's own life runs out**; stanza 4 turns out to be a
  **farewell** with a promise to return across ten thousand miles.
- Form: four quatrains in the **ballad stanza**, alternating **iambic
  tetrameter** and **iambic trimeter**, rhyming **ABCB**.
- Central devices: simile, hyperbole, symbolism of the rose, repetition and the
  chain link between stanzas 2 and 3.
- Themes: the intensity of love, love against time, beauty drawn from nature,
  constancy in separation, and the folk-song tradition.
- The Scots dialect and the singable rhythm are not decoration; they are why a
  very simple statement has lasted more than two centuries.

## Practice questions

**Short answer questions (2 marks each)**

1. To what two things does the speaker compare his beloved in the first stanza,
   and why are both needed? <span class="marks">[2]</span>
2. What impossible conditions does the speaker use to describe how long he will
   love? <span class="marks">[2]</span>
3. What does the phrase "the sands o' life" mean, and what does it add to the
   poem? <span class="marks">[2]</span>
4. Why does the poem end with a farewell? <span class="marks">[2]</span>
5. Write the rhyme scheme of the poem and name its stanza form. <span class="marks">[2]</span>
6. Identify the metre of the poem and scan the line "O my Luve's like a red, red
   rose". <span class="marks">[2]</span>
7. Why does Burns write in the Scots dialect? <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** He compares her to a red rose that has just opened in June, and to a
melody sweetly played in tune. The first is an image for the eye and suggests
colour, freshness and perfection; the second is an image for the ear and suggests
harmony and sweetness. Together they praise both how she looks and how she makes
him feel.

**2.** He says he will love her till all the seas run dry, till the rocks melt in
the sun, and for as long as the sands of his own life keep running. Since none of
the first two can happen, the vow means "for ever", measured against the age of
the earth and then against his own lifetime.

**3.** It refers to the sand falling through an hourglass, and so means the time a
person has left to live. It brings the huge, geological exaggerations of the
earlier lines back to a human scale, and quietly admits that the speaker himself
is mortal even while his love claims to be endless.

**4.** The whole poem turns out to be a parting speech: the lovers are about to be
separated. The farewell explains why the speaker has been swearing constancy, and
because he says goodbye only "a while" and promises to return "tho' 'twere ten
thousand mile", the poem ends looking forward to reunion rather than to loss.

**5.** The rhyme scheme is **ABCB** in each of the four stanzas — only the second
and fourth lines rhyme (June/tune, I/dry, sun/run, while/mile). The stanza form is
the **ballad stanza**, or common metre: a quatrain of alternating four-beat and
three-beat lines.

**6.** The metre alternates iambic tetrameter and iambic trimeter. The line scans
as four iambs: "O **my** | Luve's **like** | a **red**, | red **rose**" —
da-DUM, da-DUM, da-DUM, da-DUM. The repeated "red" pulls an extra stress into the
third foot, which is a deliberate variation.

**7.** Scots was the everyday speech of the Ayrshire country people Burns lived
and worked among. Using it keeps the poem close to real speech and to oral folk
song, gives it a distinct music ("gang", "bonnie", "a'"), and asserts the dignity
of ordinary Scottish life at a time when poets were expected to write polished
English.
:::

**Long answer questions (5 marks each)**

1. Discuss how Burns uses hyperbole in "A Red, Red Rose". Does the exaggeration
   weaken the poem or strengthen it? <span class="marks">[5]</span>
2. Show how the form of "A Red, Red Rose" — its stanza, metre, rhyme and
   repetitions — supports what the poem says. <span class="marks">[5]</span>
3. "A Red, Red Rose is a poem about time as much as about love." Discuss. <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** Hyperbole — deliberate exaggeration — is the engine of the poem's second
half. The speaker promises to love "till a' the seas gang dry", until "the rocks
melt wi' the sun", and to return even if "ten thousand mile" separate them. Taken
literally these are absurd; nobody expects oceans to evaporate. But the poem is a
song, not a contract, and the exaggeration is doing emotional work rather than
factual work. Each image is drawn from the most permanent things the speaker can
think of — the sea, the rock, the sun — so that love is measured against the
largest and most unchanging objects in the world, and still claims to outlast
them. The exaggerations also **escalate**: the seas drying is followed by
something even less likely, rocks melting, and the chain link between the stanzas
makes the vow sound sworn twice. What saves the poem from sounding foolish is the
plainness of everything around the hyperbole: simple Scots words, a folk-song
rhythm, and the very human admission of "the sands o' life", which reminds us that
the speaker will die. The exaggeration therefore strengthens the poem. It does not
ask us to believe the seas will dry; it asks us to feel how much a young man in
love needs to say that they might.

**2.** Burns chooses the ballad stanza — four quatrains of alternating iambic
tetrameter and trimeter, rhyming ABCB — and every feature of it serves the
meaning. The metre is the *da-DUM* of ordinary English and Scots speech, so the
declaration sounds spoken rather than composed. The short three-beat lines leave a
silent fourth beat at the end of each, the natural gap for a singer's tune, which
is why the poem has been sung for two centuries. Rhyming only the second and
fourth lines leaves the long lines free to run on, giving the movement of easy
speech while the returning rhyme still rounds each stanza off. Repetition works at
three levels: inside the line ("red, red"), inside the stanza ("fare-thee-weel …
fare-thee-weel"), and between stanzas, where the last line of stanza 2 becomes the
first line of stanza 3 — the chain link of oral ballad, which makes the promise
sound repeated and therefore binding. Small departures from the metre carry
meaning too: the double stress on "red, red rose" presses the colour on us, and
the extra light syllable in stanza 3's short lines keeps the song from becoming
mechanical. The structure moves from description (stanza 1) to vow (stanzas 2–3)
to farewell (stanza 4), so the form delivers the surprise of the ending. Simple
feeling is given a simple, perfect shape.

**3.** The subject of the poem looks like love, but almost every line is really
about duration. Stanza 1 already contains time: the rose is "newly sprung in
June", caught at the exact moment of perfection — and any reader knows that a June
rose has a fortnight to live. The praise therefore carries its own shadow. The
middle stanzas answer that shadow by measuring love against the biggest clocks the
speaker knows: the seas will have to dry and the rocks melt before his love
changes. These are geological spans, far beyond a human life, and they are
invoked precisely because they are beyond it. Then stanza 3 turns the measure
inward — he will love "while the sands o' life shall run", an hourglass image that
brings us from the age of the earth back to one man's mortality, honestly admitted.
The last stanza changes the unit again, from time to distance and back: the parting
is only "a while", and the ten thousand miles will be crossed. The poem's real
argument, then, is that love is the one human thing willing to stand up against
time, even though the lover knows perfectly well that the rose fades and the sand
runs out. Its confidence is moving because it is not ignorant.
:::

**Reference to the context**

1. Read the following stanza and answer the questions.
   > O my Luve's like a red, red rose,
   > That's newly sprung in June;
   > O my Luve's like the melodie
   > That's sweetly play'd in tune.

   (a) Name the figure of speech used twice here. (b) Why is the rose described
   as "newly sprung in June"? (c) What does the second comparison add that the
   first cannot? <span class="marks">[5]</span>
2. Read the following stanza and answer the questions.
   > And fare-thee-weel, my only Luve!
   > And fare-thee-weel, a while!
   > And I will come again, my Luve,
   > Tho' 'twere ten thousand mile!

   (a) What situation does this stanza reveal? (b) Identify one example of
   hyperbole and one of repetition. (c) Why does the poem not end sadly? <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) **Simile** — the comparisons are made openly with the word "like",
first to a rose and then to a melody.
(b) June is the height of the Scottish summer and "newly sprung" means the flower
has only just opened. The beloved is therefore compared not to a rose in general
but to a rose at the single moment of its greatest freshness, colour and
perfection. The detail also hints, without saying so, at how briefly such
perfection lasts — which is why the rest of the poem is so concerned with
lastingness.
(c) The rose is seen; the melody is heard. The second simile moves the praise from
sight to sound, and from nature to art. A tune "sweetly play'd in tune" suggests
harmony, order and rightness, so the beloved is not only beautiful to look at but
pleasing to be with. Between them the two similes praise her whole effect on the
speaker.

**2.** (a) It reveals, for the first time, that the lovers are about to be
**separated**: the speaker is leaving, and the entire poem has been a parting
speech rather than a general praise of love.
(b) Hyperbole: "ten thousand mile", a deliberately enormous distance. Repetition:
"fare-thee-weel" is repeated in consecutive lines (and "my Luve" twice in the
stanza), giving the insistence of a song.
(c) Because the farewell is immediately limited and then cancelled. "A while" turns
the goodbye into a short interval, and the last two lines promise return in spite
of any distance. The stanza therefore ends on the idea of coming back, not of
going away, and the final movement of the poem is towards the beloved.
:::

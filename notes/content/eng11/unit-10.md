---
subject: Compulsory English
grade: 11
unit: 10
title: All the World's a Stage
hours: 3
area: Literature — Poems
---

"All the World's a Stage" is not a separate poem at all. It is twenty-eight lines
of a play — a speech given to a character called Jaques in Shakespeare's comedy
*As You Like It*, Act II, Scene vii. In it a bitter, watchful man compares human
life to a play in seven acts and takes us from a crying baby to a toothless old
man in a single breath. It is the most quoted description of a human lifetime in
English.

::: key What the exam wants from this speech
The seven ages **in order**, with the image attached to each; the fact that the
speaker is **Jaques** in *As You Like It*, not Shakespeare himself; the
**extended metaphor** of world-as-stage; and the form — **blank verse**, that is,
unrhymed iambic pentameter. Learn the seven ages as a list you can write out
without thinking.
:::

## 10.1 About the poet

William Shakespeare (baptised 26 April 1564 – 23 April 1616) was born at
Stratford-upon-Avon in England and died there at the age of fifty-two. He was an
actor, a shareholder in a theatre company and the greatest dramatist in the
English language. From about 1590 he worked in London with the Lord
Chamberlain's Men, renamed the King's Men in 1603, the company that performed at
the Globe Theatre on the south bank of the Thames.

He wrote about thirty-eight plays — comedies such as *A Midsummer Night's Dream*,
*Twelfth Night* and *As You Like It*; tragedies such as *Hamlet*, *Macbeth*,
*Othello* and *King Lear*; and histories such as *Henry V*. He also wrote 154
sonnets and two long narrative poems. Half his plays would have been lost if two
fellow actors had not collected them in the First Folio of 1623.

Shakespeare belongs to the **English Renaissance**, the Elizabethan and Jacobean
period, when the theatre was the popular entertainment of London and playwrights
were expected to write in verse. His usual verse line is **blank verse**, which is
the form of this speech.

## 10.2 Summary

*As You Like It* is set largely in the Forest of Arden, where a banished duke and
his followers live in exile. Just before this speech, Duke Senior remarks that the
world is a wide theatre full of sadder scenes than their own. Jaques — the
melancholy lord of the play, a man who enjoys being gloomy — picks up the image
and expands it into the speech we study.

### The governing metaphor

Jaques begins by declaring that the whole world is a stage and that all men and
women are merely players on it. Each person enters at birth and leaves at death —
"They have their exits and their entrances" — and in between plays many parts.
He then fixes the number of parts at seven, and the rest of the speech is the
list.

### Ages one to three: infant, schoolboy, lover

The **infant** comes first, "Mewling and puking in the nurse's arms": crying and
being sick, completely helpless, not yet even able to hold itself.

Next the **schoolboy**, with his satchel and "shining morning face", creeping
"like snail / Unwillingly to school". The face is washed and bright, but the boy
is dragging his feet; Shakespeare catches in one line something every student
recognises.

Third the **lover**, "Sighing like furnace", writing a sad ballad in praise of his
mistress's eyebrow. The detail is comic: a grown man breathing out hot sighs and
composing poetry about one small feature of a girl's face. Love at this stage is
mostly performance.

### Ages four and five: soldier and justice

The **soldier** is full of strange oaths and "bearded like the pard" (the
leopard). He is touchy about his honour, quick to quarrel, and hunts "the bubble
reputation / Even in the cannon's mouth" — he will risk death at the mouth of a
gun for a fame that is as light and as short-lived as a bubble.

Then the **justice**, a judge. He has grown a "fair round belly" lined with good
capon — bribes, in the shape of dinners, are implied. His eyes are stern, his
beard trimmed in the correct official fashion, and he is full of "wise saws and
modern instances": old proverbs and fashionable examples, borrowed wisdom
delivered as though it were his own. He has reached the top, and Jaques quietly
tells us it is mostly an act.

### Ages six and seven: pantaloon and second childishness

The sixth age "shifts / Into the lean and slippered pantaloon" — the thin,
slippered old man of Italian comedy, spectacles on his nose and a money-pouch at
his side. The body has begun to shrink: the stockings he carefully saved from his
youth are now "a world too wide / For his shrunk shank", and the deep manly voice
has turned back to a childish treble that pipes and whistles when he speaks.

The last age, which "ends this strange eventful history", is "second
childishness and mere oblivion" — a return to the helplessness of the infant, and
then forgetfulness of everything. The speech closes with one of the most famous
lines Shakespeare wrote: "Sans teeth, sans eyes, sans taste, sans everything."
*Sans* is French for "without". Everything the man gathered in seven ages is
taken away again.

```figure caption="The seven ages of man. Life rises to the justice at its peak and falls back to the helplessness it began in."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.0))
names = ["infant","schoolboy","lover","soldier","justice","pantaloon","oblivion"]
tags  = ["helpless","unwilling","sighing","reckless","pompous","shrinking","nothing left"]
x = np.arange(7)
y = np.sin(np.pi*(x+0.55)/7.1)
xs = np.linspace(-0.42, 6.42, 300)
ax.plot(xs, np.sin(np.pi*(xs+0.55)/7.1), color=GRID, lw=8,
        solid_capstyle="round", zorder=1)
ax.plot(x, y, "o", color=ACCENT, ms=10, zorder=3)
for i in range(7):
    ax.text(x[i], y[i], str(i+1), ha="center", va="center", fontsize=7.4,
            color="white", fontweight="bold", zorder=4)
    ax.text(x[i], y[i]+0.11, names[i], ha="center", va="bottom", fontsize=8.6,
            color=INK, fontweight="bold", zorder=4)
    ax.text(x[i], y[i]-0.11, tags[i], ha="center", va="top", fontsize=7.4,
            color=MUTED, zorder=4)
ax.annotate("", xy=(6.55,-0.42), xytext=(-0.55,-0.42),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=11))
ax.text(3.0, -0.52, "one lifetime  \u2014  birth to oblivion", ha="center", va="top",
        fontsize=8.0, color=MUTED)
ax.set_xlim(-0.80, 6.80); ax.set_ylim(-0.72, 1.32); ax.axis("off")
```

## 10.3 Themes

**Life as a performance.** The controlling idea is that people do not simply live,
they *play parts*. Each age has its costume, its lines and its gestures, and the
part is handed to us by the world rather than chosen by us. The soldier's oaths
and the judge's proverbs are props, not proofs of character.

**The passing of time.** Seven ages are crossed in twenty-eight lines. The speed
is the argument: a whole life, compressed, looks short and oddly repetitive.

**Life as a circle, not a line.** The last age is called "second childishness".
The old man of the sixth age is already drifting back towards a child's high
voice, and the seventh returns him to the helplessness of the first. What looked
like progress turns out to be a curve that comes back down to where it started.

**The decay of the body.** Shakespeare is unsentimental. Teeth, eyes, taste,
voice, and even the size of the leg are listed as things that go. Nothing is
promised in return.

**Satire on human vanity.** Every age is gently mocked: the lover's ridiculous
ballad to an eyebrow, the soldier dying for a bubble, the judge fat with the good
dinners of office. Ambition is shown to be as childish as the schoolboy's
satchel.

**The melancholy view — and its limits.** Remember that this is Jaques speaking,
and that the play does not agree with him. Immediately after the speech, old
Adam is carried in and fed with tenderness by younger men — a living answer to
Jaques's claim that old age is nothing but oblivion. Shakespeare gives the cynic
his say and then quietly shows him a kinder picture.

## 10.4 Form, structure and rhyme

**It is a speech from a play.** *As You Like It*, Act II, Scene vii, spoken by
Jaques before Duke Senior and his company in the Forest of Arden. It is printed
in textbooks as a poem, but it is a **dramatic monologue inside a comedy**, and
the speaker is a character whose gloom the play treats with some amusement.

**Blank verse.** The speech is written in **blank verse**: unrhymed **iambic
pentameter**. "Blank" means no rhyme; "pentameter" means five feet to a line; an
**iamb** is an unstressed syllable followed by a stressed one, *da-DUM*. So the
standard line has ten syllables in five *da-DUM* beats:

> And **one** | man **in** | his **time** | plays **ma-** | ny **parts**

**Rhyme scheme.** There is **none** — that is the definition of blank verse. If a
question asks for the rhyme scheme, answer "blank verse: unrhymed iambic
pentameter", and explain that rhyme would make a stage speech sound artificial,
because people do not rhyme when they talk.

**Variations.** Shakespeare's verse is a pattern to play against, not a cage. Many
lines here end with an extra unstressed syllable — a **feminine ending** — as in
"And all the men and women merely players" (eleven syllables). Lines are broken by
strong mid-line pauses (**caesura**), and most of them run on into the next
(**enjambment**), for instance "creeping like snail / Unwillingly to school". The
result is verse that moves at the speed of thought.

**Structure.** One unbroken verse paragraph of twenty-eight lines: a statement of
the metaphor, then a list of seven parts in time order, then a closing line that
strips everything away. There are no stanzas. The list form is deliberate — it
makes a human life look like an inventory.

**What the form does for the meaning.** Blank verse is the closest verse form to
natural English speech, so the outrageous claim that your whole life is a piece of
acting is delivered in a calm, ordinary, conversational voice. Enjambment keeps
one age spilling into the next without a pause, which is exactly what the speech
says time does to us. And because there is no rhyme to give each age a neat
ending, the only real ending arrives in the last line — and it is a list of
absences.

```figure caption="Blank verse: five iambic feet to a line and no rhyme. The lower line takes an extra unstressed syllable, a feminine ending."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.8))
rows = [
 (["And","one","man","in","his","time","plays","ma-","ny","parts"],
  "10 syllables  —  regular pentameter", 0.70),
 (["And","all","the","men","and","wo-","men","mere-","ly","play-","ers"],
  "11 syllables  —  feminine ending", 0.32),
]
u = 0.0168
for syls, note, y in rows:
    pos = 0.035
    edges = [pos]
    for i, sy in enumerate(syls):
        w = (len(sy) + 1.8) * u
        cx = pos + w/2
        extra = (i == 10)
        ax.text(cx, y+0.105, "x" if i % 2 == 0 else "/", ha="center", va="center",
                fontsize=9.5, fontweight="bold",
                color=MUTED if (i % 2 == 0 or extra) else ACCENT)
        ax.text(cx, y, sy, ha="center", va="center", fontsize=8.8, color=INK)
        pos += w
        edges.append(pos)
    for k in range(0, len(syls)+1, 2):
        if k < len(edges):
            ax.plot([edges[k]-0.006]*2, [y-0.055, y+0.055], color=GRID, lw=1.0)
    ax.text(0.035, y-0.135, note, fontsize=8.0, color=MUTED)
ax.text(0.035, 0.96, "x = unstressed      / = stressed      | = foot division",
        fontsize=8.2, color=MUTED)
ax.text(0.035, 0.03, "No rhyme at the line-ends: parts / players do not chime.",
        fontsize=8.2, color="#A8271F")
ax.set_xlim(0,1.0); ax.set_ylim(0.0,1.02); ax.axis("off")
```

## 10.5 Poetic devices

| Device | Example | Effect |
|---|---|---|
| Extended metaphor | "All the world's a stage" | One comparison is carried through the whole speech, so every detail of life becomes a detail of theatre |
| Metaphor | "the bubble reputation" | Fame becomes something round, shining, weightless and certain to burst |
| Metaphor | "exits and their entrances" | Death and birth become stage directions, which drains them of drama |
| Simile | "creeping like snail" | The boy's unwillingness is made slow, small and visible |
| Simile | "Sighing like furnace" | The lover's breath is hot and loud; the comparison mocks him even as it describes him |
| Simile | "bearded like the pard" | The soldier is given the look of a leopard — fierce, but also slightly ridiculous |
| Personification | "the cannon's mouth" | The weapon is given a mouth that swallows men |
| Hyperbole | "a world too wide / For his shrunk shank" | The gap between the old stocking and the thin leg is exaggerated to show how far the body has shrunk |
| Alliteration | "shining morning face"; "shrunk shank"; "plays many parts" | Repeated sounds bind each picture together and make lines easy to remember |
| Imagery | the satchel, the round belly, the spectacles and pouch, the piping voice | Seven quick portraits; each age is seen, not explained |
| Enjambment | "creeping like snail / Unwillingly to school" | The sense spills across the line-break, imitating time running on from one age to the next |
| Caesura | "His acts being seven ages. At first, the infant," | The mid-line stop lets one part end and another begin inside a single line |
| Repetition (anaphora) | "Sans teeth, sans eyes, sans taste, sans everything" | Four losses hammered in one line; the repetition itself sounds like something being taken away again and again |
| Symbolism | the stage, the satchel, the bubble, the spectacles | Ordinary objects stand for whole stages of a human life |
| Irony / satire | the judge "with good capon lined" | The respectable are shown to have grown fat on the gifts of office |
| Catalogue | the numbered list of seven ages | Reduces a human life to an inventory, which is the point being made |

## 10.6 Glossary

| Word | Meaning |
|---|---|
| players | actors |
| exits and entrances | the moments when an actor leaves and comes onto the stage; here, death and birth |
| mewling | crying feebly, like a kitten |
| puking | vomiting |
| satchel | a school bag carried on the shoulder |
| creeping | moving very slowly |
| woeful ballad | a sad song or love poem |
| mistress | here, the woman a man is in love with |
| oaths | swear-words; also solemn promises |
| pard | leopard |
| jealous in honour | very sensitive about his reputation |
| bubble reputation | fame that is showy, empty and short-lived |
| cannon's mouth | the open end of a gun; a place of great danger |
| justice | a judge |
| capon | a fattened cock, a rich dish — here suggesting good dinners and bribes |
| saws | old sayings, proverbs |
| modern instances | up-to-date examples |
| pantaloon | the thin, foolish old man of Italian comedy |
| hose | stockings or tight trousers |
| shank | the lower part of the leg |
| treble | a high-pitched voice |
| second childishness | old age, when a person becomes helpless like a child again |
| oblivion | forgetfulness; being completely forgotten |
| sans | without (French) |
| blank verse | unrhymed iambic pentameter |

## Chapter summary

- The speech is spoken by **Jaques** in Shakespeare's *As You Like It*, **Act II,
  Scene vii**, in the Forest of Arden. It is a dramatic speech, not a stand-alone
  poem, and Jaques's gloom is his own, not the play's verdict.
- Its controlling idea is an **extended metaphor**: the world is a stage, people
  are actors, birth and death are entrances and exits, and each person plays
  seven parts.
- The seven ages in order: **infant, schoolboy, lover, soldier, justice,
  pantaloon, second childishness**.
- Form: **blank verse** — unrhymed iambic pentameter, one unbroken verse
  paragraph of 28 lines, with feminine endings, caesura and heavy enjambment.
- Themes: life as performance, the speed of time, the circle from childhood to
  second childhood, bodily decay, and satire on human vanity.
- The closing line, "Sans teeth, sans eyes, sans taste, sans everything", strips
  away in one breath everything the seven ages built up.

## Practice questions

**Short answer questions (2 marks each)**

1. Who speaks these lines, and in which play and scene do they occur? <span class="marks">[2]</span>
2. List the seven ages of man in the correct order. <span class="marks">[2]</span>
3. What does Shakespeare mean by "the bubble reputation"? <span class="marks">[2]</span>
4. How is the schoolboy described, and what does the description suggest? <span class="marks">[2]</span>
5. Why is the last age called "second childishness"? <span class="marks">[2]</span>
6. What is blank verse? <span class="marks">[2]</span>
7. Explain the effect of the repeated word "sans" in the final line. <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** The lines are spoken by **Jaques**, the melancholy lord, in Shakespeare's
comedy *As You Like It*, **Act II, Scene vii**. He speaks them in the Forest of
Arden, to the banished Duke Senior and his followers, taking up an image the Duke
has just used.

**2.** Infant, schoolboy, lover, soldier, justice (judge), pantaloon (the lean
slippered old man), and second childishness or oblivion.

**3.** It is a metaphor for fame won in battle. A bubble is bright and round and
attractive, but weightless and certain to burst in a moment. The soldier will face
the mouth of a cannon for something that empty, which is Shakespeare's comment on
military glory.

**4.** He is described with his satchel and "shining morning face", "creeping like
snail / Unwillingly to school". The washed, bright face shows he has been
carefully prepared by others, while the snail simile shows that he has no wish to
go. The gap between the two is the comedy of the second age.

**5.** Because the very old man returns to the condition of the infant he once
was. He cannot feed or look after himself, his voice has climbed back to a child's
high treble, and finally memory and the senses go. Life is therefore shown as a
circle rather than a straight line.

**6.** Blank verse is unrhymed **iambic pentameter**: lines of five iambic feet
(ten syllables, a *da-DUM* beat five times over) with no rhyme at the line-ends.
It is the standard verse form of Elizabethan drama because it is the closest verse
form to natural English speech.

**7.** "Sans" means "without", and it is repeated four times in one short line.
Each repetition removes something more — teeth, eyes, taste, and then
"everything". The rhythm of the line therefore imitates the process it describes:
loss after loss, until nothing at all is left.
:::

**Long answer questions (5 marks each)**

1. Describe the seven ages of man as Shakespeare presents them, and show how the
   pictures are chosen to build a single argument. <span class="marks">[5]</span>
2. Discuss "All the World's a Stage" as an extended metaphor. How far do you
   agree that life is a performance? <span class="marks">[5]</span>
3. Examine the form and dramatic context of the speech. Why does blank verse suit
   it, and why does it matter that Jaques, not Shakespeare, is speaking? <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** Jaques presents seven pictures in time order. The **infant** is helpless,
"Mewling and puking in the nurse's arms". The **schoolboy**, with satchel and
shining morning face, creeps "like snail / Unwillingly to school". The **lover**
sighs "like furnace" and writes a sad ballad to his mistress's eyebrow. The
**soldier**, bearded like the leopard and quick to quarrel, chases "the bubble
reputation" even at the cannon's mouth. The **justice**, with a fair round belly
lined with capon and a formally cut beard, hands out borrowed wisdom in the form
of "wise saws and modern instances". The sixth age is the **pantaloon**, thin and
slippered, spectacles on nose, his youthful stockings now "a world too wide / For
his shrunk shank" and his voice piping like a child's. The seventh is **second
childishness and mere oblivion**, "Sans teeth, sans eyes, sans taste, sans
everything". Each picture is chosen for one reason: to show the person acting a
part supplied by his age rather than living a life he has chosen. The ages also
form an arc, rising to the judge at the top of the world and then falling; and
because the last age returns to the helplessness of the first, the arc closes into
a circle. The argument, built entirely out of pictures, is that a human life is
short, borrowed and repetitive.

**2.** The speech is built on a single comparison carried through to the end,
which is what an extended metaphor means. The world becomes a stage, men and
women become "merely players", birth and death become "entrances" and "exits", and
a lifetime becomes a play in seven acts. Once the metaphor is set, every detail
follows from it: each age arrives with a costume (satchel, beard, spectacles,
slippers), a voice (mewling, sighing, swearing, piping) and a set of lines (the
ballad, the oaths, the proverbs). The metaphor does real work, because it lets
Jaques suggest that our behaviour is not personal but scripted — the soldier
quarrels because soldiers quarrel, the judge pronounces because judges pronounce.
There is truth in this. We do take on roles, and much of what we call personality
is behaviour expected of our age, our job and our place in society. But the
metaphor is not the whole truth, and Shakespeare knows it. Actors can put the
costume off; human beings cannot. More importantly, a script cannot explain the
scene that follows immediately in the play, where the starving old servant Adam
is carried in and fed with real kindness. That act is not in anybody's part. The
metaphor is brilliant and partial at the same time, which is why the play gives it
to a character rather than stating it as truth.

**3.** The speech is written in **blank verse** — unrhymed iambic pentameter, five
*da-DUM* feet to a line, as in "And **one** man **in** his **time** plays **ma**-ny
**parts**". Shakespeare uses the pattern loosely: many lines carry an extra
unstressed syllable at the end (a feminine ending, such as "merely players"),
strong pauses cut lines in half, and the sense constantly runs over the line-break
in enjambment. These freedoms matter, because they make verse sound like a man
thinking aloud. Rhyme would have been fatal here; it would have turned a bitter
observation into a jingle, and would have given each age a neat, satisfying close
that the argument does not want. Instead the lines push forward without rest, one
age spilling into the next, exactly as time does. The context matters just as
much. These are not Shakespeare's opinions but **Jaques's**, and Jaques is the
play's professional pessimist, a man who, as another character says, enjoys his
own sadness. He speaks in the Forest of Arden, in a scene where Duke Senior has
just made the same comparison more gently. Within thirty lines the play answers
him: old Adam is brought in, weak and hungry, and is treated with tenderness — so
the audience sees that the seventh age need not be "mere oblivion" after all.
Recognising the speaker keeps us from mistaking a character's mood for the play's
conclusion.
:::

**Reference to the context**

1. Read the following lines and answer the questions.
   > All the world's a stage,
   > And all the men and women merely players;
   > They have their exits and their entrances,
   > And one man in his time plays many parts,
   > His acts being seven ages.

   (a) Who is the speaker and to whom is he speaking? (b) Identify the figure of
   speech in the first two lines and explain it. (c) What do "exits" and
   "entrances" stand for here? <span class="marks">[5]</span>
2. Read the following lines and answer the questions.
   > Last scene of all,
   > That ends this strange eventful history,
   > Is second childishness and mere oblivion,
   > Sans teeth, sans eyes, sans taste, sans everything.

   (a) Which age of man is described? (b) Why is the human life called a "strange
   eventful history"? (c) Comment on the effect of the last line. <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) The speaker is **Jaques**, the melancholy lord in *As You Like It*
(Act II, Scene vii). He is speaking in the Forest of Arden to the banished Duke
Senior and the other exiled lords, taking up a comparison the Duke has just made.
(b) The figure of speech is **metaphor**, and because it is carried through the
whole speech it is an **extended metaphor**. The world is called a stage and human
beings are called actors, without "like" or "as". The comparison suggests that
people do not simply live their lives but perform parts written for them by their
age and situation.
(c) "Exits" and "entrances" are stage directions: the moments an actor leaves and
comes on. Here they stand for **death and birth**. Calling them stage directions
makes them routine and impersonal — actors come and go all evening — which is
exactly the cool, detached view of human life that Jaques wants to press on his
listeners.

**2.** (a) The **seventh and last age**, extreme old age, which Jaques calls
"second childishness and mere oblivion".
(b) Because a lifetime is full of incident — seven different parts, each with its
own costume, ambitions and follies — yet it is "strange" in that all this activity
leads only back to the helplessness it began in. Calling it a "history" also keeps
the theatre metaphor alive, since a history was a kind of play.
(c) The last line lists four losses in a single breath, using the French word
"sans" ("without") four times. The repetition (anaphora) makes the line sound like
a series of subtractions, and the movement from three concrete losses — teeth,
eyes, taste — to the sweeping "sans everything" empties the life out completely.
There is no consolation offered and no rhyme to soften it; the play's most famous
line is a line of pure absence.
:::

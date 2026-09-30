---
subject: Compulsory English
grade: 12
unit: 13
title: On Libraries
hours: 3
area: Literature - Essays
---

Most people meet a library as a place where you must be quiet. Oliver Sacks met it as
the place where he became himself. His essay "On Libraries" is a short memoir of the
rooms in which he read — the oak-panelled library at home, the public library five
minutes from his door, the school and museum libraries where he hunted for chemistry,
the vaults under an Oxford college — and it ends, unexpectedly, in grief: the shelves
he loved are being emptied because students now find everything on a screen. It is one
of the easiest essays in your book to read and one of the hardest to answer badly,
because every paragraph is a memory and every memory carries a small argument.

::: key What the exam wants from this essay
The **two-sided shape** of the essay: eleven paragraphs of gratitude, then two of
loss. The **places** (home library, Willesden Public Library, Walker Library, Science
Museum library, Radcliffe Science Library, the Bodleian, the Queen's College library,
the Albert Einstein College of Medicine library) and what each gave him. The
**contrast between a pupil and a learner**. The **community** that grew between
strangers in the stacks. And Sacks's attitude to the **digital library**: not anger at
technology, but sorrow for the physical book — "its look, its smell, its heft". Short
questions are almost always one fact from one paragraph; the long question is almost
always "traditional versus digital" or "what libraries gave the writer".
:::

## 13.1 About the author

```photo id="eng12/oliver-sacks" caption="Oliver Sacks (1933–2015) in his consulting-room white coat, holding a reflex hammer, the doctor's tool for testing reflexes. The photograph is by Bernard Gotfryd and is in the public domain." width="40"
crop 0.0 0.18 1.0 1.0
```

Oliver Wolf Sacks was born in London on **9 July 1933**, the youngest of four sons of
two doctors — a physician father and a surgeon mother. His parents met, as the essay
tells us, in a medical students' society devoted to the plays of Ibsen. He was educated
at St Paul's School in London and then at **The Queen's College, Oxford**, where he
qualified in medicine. In the early 1960s he crossed the Atlantic: he interned at
**Mount Zion Hospital** in San Francisco and trained in neurology at **UCLA**, and in
1965 he settled in **New York**, the city that appears in the middle of the essay. He
worked there for nearly fifty years as a neurologist and died on **30 August 2015**,
aged 82.

What made Sacks famous was not only his medicine but his prose. In the hospital he met
patients that other doctors had given up on — the survivors of the 1920s sleeping-sickness
epidemic whom he woke with a new drug, people who could not recognise faces, people who
heard music that was not there — and he wrote about them as human beings rather than as
cases. The books that came out of this work are the ones your textbook names:

| Book | Year | What it is about |
|---|---|---|
| *Migraine* | 1970 | his first book, on the headache and its visual aura |
| *Awakenings* | 1973 | patients revived from sleeping sickness; filmed in 1990 with Robin Williams and Robert De Niro |
| *The Man Who Mistook His Wife for a Hat* | 1985 | case histories of unusual disorders of perception and memory |
| *Musicophilia* | 2007 | music and the brain |
| *Hallucinations* | 2012 | why healthy and sick minds see and hear what is not there |
| *On the Move* | 2015 | his memoir, published shortly before his death |

The *New York Times* called him "the poet laureate of medicine", and the textbook
adds that he won honours from the Guggenheim Foundation, the National Science
Foundation, the American Academy of Arts and Letters and the Royal College of
Physicians. After his death a further book of essays, ***Everything in Its Place: First
Loves and Last Tales*** (2019), was put together from the pieces he left. "On
Libraries" was printed in the American literary magazine *The Threepenny Review*, and
it appears in that posthumous collection under the shorter title "Libraries".

::: note Why a scientist wrote this essay
Sacks describes himself as a boy who was "biased towards the sciences, especially
astronomy and chemistry". He did not become a literary man who happened to study
medicine; he became a doctor who never stopped reading. That is why the essay moves so
easily between Mellor's *Treatise on Inorganic Chemistry*, the diaries of a witty
nineteenth-century entertainer and the seventeenth-century prose of Sir Thomas Browne.
For him there was no wall between the sciences and the humanities — the library was
where they met.
:::

::: caution Study-guide mistakes to avoid
Several popular guides to this essay contain errors that will cost you marks if you
copy them. **Dickens is Charles Dickens**, the English novelist — not "Emily" Dickens
and not an American poet. **Kipling** was English, born in Bombay, not an Irish
playwright. **Willesden Public Library** was the library of Sacks's *growing-up years*,
not of his "adult life". And the essay says he was **a good learner, not a good
listener** (see §13.7). Always check a fact against the essay itself.
:::

## 13.2 The essay: source, shape and message

"On Libraries" is a **personal (reflective) essay**: the writer speaks in the first
person, draws on his own memories and moves towards an opinion without proving it like
a lawyer. Your textbook's headnote calls it "a praise of intellectual freedom,
community work, and the ecstasy of serendipitous discovery". The three phrases are
worth learning, because each names a strand of the essay:

- **intellectual freedom** — the freedom to choose your own books and follow your own
  curiosity (paragraph on Willesden);
- **community** — the quiet friendship of strangers in the stacks (paragraphs on New
  York);
- **serendipity** — the joy of finding a valuable thing by lucky accident, which only
  browsing among real shelves allows (the "unexpected treasures, lucky finds").

The essay is built in **three movements**. First comes **childhood and youth**
(paragraphs 1–9): the home library, Willesden, school, the science books, Oxford.
Second comes **adult life in New York** (paragraphs 10–11): the crowded flat, the
spacious library, the whispered conversations. Third comes **the turn** (paragraphs
12–13): the 1990s, the students who ignore the shelves, the discarded books, the
librarian's reassurance and the writer's refusal to be reassured. Nothing in the first
eleven paragraphs tells you that the last two are coming — which is why they hit so hard.

```figure caption="The essay's route through Sacks's libraries, from the oak-panelled room at home to the emptied shelves. Positions are in the order of the essay, not to scale."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.5))
ax.set_xlim(0,10); ax.set_ylim(-2.6,2.6); ax.axis('off')
ax.plot([0.3,9.7],[0,0],color=GRID,lw=3,zorder=0)
nodes = [
 (0.9,'1','Home library\n(oak panels;\nreads at 3–4)',1),
 (2.2,'2','Willesden\nPublic Library\n("real education")',-1),
 (3.5,'3','Walker Library and\nScience Museum\nlibrary (age 12+)',1),
 (4.8,'4','Oxford: Radcliffe,\nBodleian (1602),\nQueen’s College',-1),
 (6.1,'5','New York, 1965:\nAlbert Einstein\nCollege library',1),
 (7.4,'6','Whispers in\nthe stacks;\nfriendship',-1),
 (8.7,'7','1990s: shelves\nignored, books\nthrown out',1),
]
for i,(x,n,lab,s) in enumerate(nodes):
    col = ACCENT if i<6 else '#A8271F'
    ax.plot([x,x],[0,1.0*s],color=MUTED,lw=0.8,zorder=1)
    ax.scatter([x],[0],s=210,color=col,zorder=3)
    ax.text(x,0,n,color='white',ha='center',va='center',fontsize=8,fontweight='bold',zorder=4)
    ax.text(x,1.15*s,lab,ha='center',va='bottom' if s>0 else 'top',fontsize=6.3,color=INK,linespacing=1.25)
fig.subplots_adjust(left=0.02,right=0.98,top=0.98,bottom=0.02)
```

## 13.3 The essay, paragraph by paragraph

The essay has thirteen short paragraphs. This section retells them in order, in plain
words, with only the shortest quotations, so that you can find any detail the
examiner asks for.

### Paragraphs 1–4 — the library at home

Sacks's favourite room as a child was the family library: a large **oak-panelled**
room, every wall lined with bookcases, a solid table in the middle for writing and
study. It held his father's special collection as a **Hebrew scholar**; all of
**Ibsen's** plays; a shelf of the young poets of his father's generation, "many killed
in the Great War"; and, on the lowest shelves where a small boy could reach them, the
adventure and history books of his three older brothers. Among these he found **Kipling's
*The Jungle Book***, identified with the wolf-boy **Mowgli**, and used his adventures as
a launching-pad for his own fantasies.

His mother kept her own books in a separate bookcase in the lounge: **Dickens, Trollope
and Thackeray**; **Bernard Shaw's plays** in pale green bindings; a complete Kipling in
soft **morocco** leather; a three-volume Shakespeare; a gilt-edged Milton; and poetry
she had won as school prizes. **Medical books** lived in a locked cabinet in the
parents' surgery — but the key was in the door, which tells you how easily a curious
child could get at anything.

The fourth paragraph sums up. The library was the quietest and most beautiful room in
the house; it "vied with" his little chemistry lab as his favourite place. He would curl
up in a chair and lose all sense of time, and when he was late for lunch or dinner
the family knew where to look. He learned to read at **three or four**, and "books, and
our library, are among my first memories".

### Paragraphs 5–6 — Willesden: the "Ur-library"

The library that mattered most, he says, was not the one at home but **Willesden Public
Library**, a five-minute walk from his house. He calls it his **"Ur-library"** — *Ur-* is
a German prefix for "original, archetypal", so this was the first of all libraries, the
one against which every later library was measured. "It was there I received my real
education."

The next paragraph explains why. He **disliked school**: sitting in class receiving
instruction, information went "in one ear and out by the other". He could not be
passive; he had to learn actively, what he wanted and in the way that suited him. He
puts it in one balanced sentence: he was **"not a good pupil, but … a good learner"**.
In Willesden and in every library afterwards he roamed the shelves, chose freely and
followed paths that fascinated him — "to become myself". The paragraph closes with the
feeling that runs through the whole essay: at the library he felt **free** — free to
look at tens of thousands of books, and to enjoy the "quiet companionship of other
readers, all, like myself, on quests of their own".

### Paragraphs 7–8 — science, and the search for books that were not there

As he grew older his reading leaned towards **astronomy and chemistry**. At **St Paul's
School**, which he entered at twelve, the **Walker Library** was excellent but strong in
history and politics; it could not feed his hunger for science, and above all for
chemistry. A master wrote him a special **testimonial**, which got him a ticket to the
library of the **Science Museum** in London, where he "devoured" the many volumes of
**Mellor's *Comprehensive Treatise on Inorganic and Theoretical Chemistry*** and the
even longer **Gmelin's *Handbook of Inorganic Chemistry***. Note what this shows: a
school library, however good, cannot hold everything; a boy who wants more must go
looking, and a great library will let him in.

At **Oxford** he could use the two great university libraries, the **Radcliffe Science
Library** and the **Bodleian** — "a wonderful general library that could trace itself
back to 1602". In the Bodleian he stumbled on the forgotten works of **Theodore Hook**,
an early-nineteenth-century wit admired for his brilliance at improvising in theatre and
music (he was said to have composed **more than five hundred operas** on the spot).
Sacks became so fascinated that he decided to write a kind of biography, a
"case-history", of Hook. For that he needed materials that only the Bodleian and the
**British Museum Library** could supply, and the "tranquil atmosphere" of the Bodleian was
ideal for writing.

```photo id="eng12/radcliffe-camera" caption="The Radcliffe Camera at Oxford, a domed reading room of the Bodleian Libraries. Sacks used the Bodleian and the Radcliffe Science Library as a student; the library he loved best, however, was his own college's." width="46"
```

### Paragraph 9 — the library he loved most: the Queen's College

The Oxford library he loved best was not the grand university one but **the library of
his own college, the Queen's College**. The magnificent library building itself, he says,
was designed by **Christopher Wren**; **beneath** it, "in an underground maze of heating
pipes and shelves", lay the vast holdings — the **catacombs** of the library. Here he held
**incunabula** (books printed before 1501) for the first time and adored **Gesner's
*Historiae Animalium*** (1551), illustrated with **Dürer's rhinoceros**, and **Agassiz's
four-volume work on fossil fishes**. He saw **all of Darwin's works in their original
editions**, and found and fell in love with **Sir Thomas Browne** — *Religio Medici*,
*Hydrotaphia*, *The Garden of Cyrus*: "How absurd some of these were, but how magnificent
the language!" When Browne's grand style (his **magniloquence**) became too much, he could
switch to the sharp, chiselled prose of **Swift**.

He had grown up on the nineteenth-century books his parents loved; the Queen's vaults
introduced him to the **seventeenth and eighteenth centuries** — **Johnson, Hume, Pope and
Dryden**. And the great thing was that these books were "freely available, not in some
special, locked-away rare books enclave, but just sitting on the shelves". In those vaults
he "really gained a sense of history, and of my own language".

```photo id="eng12/queens-upper-library" caption="The Upper Library of the Queen's College, Oxford, with its carved shelving and plasterwork ceiling. Sacks's favourite books lay in the vaults beneath a library building like this one." width="44"
crop 0.0 0.12 1.0 1.0
```

### Paragraphs 10–11 — New York: space, treasures and friendship

In **1965** Sacks arrived in **New York** and found himself in "a horrid, pokey little
apartment" with almost no surface to read or write on. He wrote part of ***Migraine***
(the book named in the essay) balancing at the top of the **refrigerator**, one elbow
held awkwardly aloft. He longed for spaciousness, and found it at the library of the
**Albert Einstein College of Medicine**, where he worked. There he could sit at a large
table to read or write, then wander among the stacks with no idea what his eye might fall
on — "unexpected treasures, lucky finds", which he carried back to his seat. This is the
**serendipity** of the headnote.

The next paragraph adds **people**. Though the library was quiet, "whispered
conversations might start in the stacks" — two readers hunting for the same old book, the
same bound volumes of the journal ***Brain*** from **1890** — and such conversations "could
lead to friendships". Everyone was absorbed in a private world, and yet there was "a sense
of community, even intimacy". Part of this camaraderie came from the **physicality of
books**: handling them, sharing them, passing them between readers, even seeing the names
of earlier borrowers and the dates they took the books out.

### Paragraphs 12–13 — the turn: the 1990s and the empty shelves

"But a shift was occurring by the 1990s." Sacks still sat at a table with a mountain of
books, but **students increasingly ignored the bookshelves** and got what they needed on
their **computers**. The books, so far as they were concerned, were unnecessary — and because
most users no longer used the books, the college decided in the end to **dispose of them**.
He had no idea this was happening, "not only in the AECOM library but in college and
public libraries all over the country".

When he visited "a couple of months ago" he was **horrified**: the once-overflowing shelves
were sparsely occupied, most books thrown out "with remarkably little objection from
anyone". He felt "that a murder, a crime had been committed — the destruction of centuries
of knowledge". A **librarian**, seeing his distress, reassured him that everything "of
worth" had been **digitised**. But he **does not use a computer**, and he mourns the loss of
books — even bound periodicals — because "there is something irreplaceable about a physical
book: its look, its smell, its heft". He remembers how libraries once **cherished old
books** and kept a special room for old and rare ones, and how in **1967**, rummaging in the
stacks, he found an 1873 book, **Edward Liveing's *Megrim***, which inspired him to write his
own first book. That last detail closes the circle: an old book on a shelf, found by
accident, produced a new book. Digitise the shelf and you may keep the text — but you lose
the accident.

::: tip Paragraph anchors for short questions
When a short question begins with *Where, When, Why did he …*, the answer is nearly
always in one of these anchors. **Late for meals; first memories** → ¶4. **Willesden**
→ ¶5. **Dislike of school; freedom** → ¶6. **Science bias; Science Museum** → ¶7.
**Hook; the Bodleian** → ¶8. **Queen's library** → ¶9. **New York; Einstein College** →
¶10. **Friendship** → ¶11. **The 1990s** → ¶12. **Horror, librarian, smell and heft** →
¶13.
:::

## 13.4 Arguments and themes

**1. The library is a place of freedom.** The word appears in the Willesden paragraph
three times in three lines. Sacks contrasts two kinds of education. School is
**instruction**: someone else chooses what you learn, how fast, and in what order. The
library is **self-education**: you choose, you wander, you follow the odd book that
catches your eye. He was, by his own account, a poor pupil and a good learner — and the
library is where the learner, rather than the pupil, is allowed to flourish.

**2. Books and libraries are the seedbed of a writer and thinker.** The essay is really a
map of how a mind was fed. Home shelves gave him fantasy (*The Jungle Book*) and the
habit of absorption; Willesden gave him independence; the Science Museum gave him
chemistry; the Bodleian gave him a subject (Hook); Queen's gave him "a sense of history,
and of my own language"; the Einstein College library gave him space to write *Migraine*;
and a stray 1873 book gave him the idea of his first book. A library is not a warehouse
but a *workshop*.

**3. Serendipity — discovery by lucky accident.** Sacks never knew what his eyes "might
alight upon" in the stacks. Shelves arrange knowledge by neighbourhood, so that what you
find beside the book you wanted is often better than the book you wanted. A search box
returns exactly what you asked for and nothing else.

**4. Community without conversation.** A library is one of the few places where strangers
share a room in silence and still feel connected — "all of us … reading our own books,
absorbed in our own worlds, and yet there was a sense of community, even intimacy". The
friendships that started from two people looking for the same old volume are Sacks's
proof that a quiet place can still be a social one.

**5. The physical book and its irreplaceable qualities.** Sacks does not say digitisation
is useless. He says it does not replace *everything*. A physical book has a **look**, a
**smell**, a **heft** — and, in a library copy, the traces of earlier readers, the names
and dates that make a shelf a shared memory. Old books are also *artefacts*: an original
edition of Darwin or a Gesner from 1551 tells you something a scan cannot.

**6. The danger of forgetting: technology, progress and loss.** The ending is an alarm.
Libraries were emptied "with remarkably little objection from anyone". Sacks's word for
it is **murder**, and the target is "centuries of knowledge". The essay asks a hard
modern question: when we make something more convenient, what do we quietly stop
valuing? Note that he offers no plan; he ends with a memory, not a slogan.

```figure caption="A schematic of the writer's mood, paragraph by paragraph (an illustration of the essay's structure, not measured data). Feeling rises through childhood, Oxford and New York, then drops sharply in the last two paragraphs."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.7))
x = np.arange(1,14)
y = np.array([6.5,6.8,6.4,7.4,8.4,8.8,8.4,8.9,9.6,8.6,9.2,4.8,1.2])
xs = np.linspace(1,13,300)
ax.plot(xs, np.interp(xs,x,y), color=ACCENT, lw=2.2)
ax.scatter(x,y,color=ACCENT,s=16,zorder=3)
ax.axvspan(11.5,13.4,color='#A8271F',alpha=0.08,lw=0)
ax.set_xticks(x)
ax.set_xlim(0.6,13.4); ax.set_ylim(0,10.8)
ax.set_yticks([])
ax.set_xlabel('paragraph number',fontsize=7.5,color=MUTED)
ax.tick_params(axis='x',labelsize=7,colors=MUTED)
ax.spines[['top','right','left']].set_visible(False)
ax.text(1.0,10.2,'gratitude and discovery',fontsize=7.4,color=ACCENT,va='center')
ax.text(13.3,10.2,'the turn',fontsize=7.4,color='#A8271F',va='center',ha='right')
ax.annotate('Queen\u2019s College\nvaults',xy=(9,9.6),xytext=(6.2,3.4),fontsize=6.6,color=INK,arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8),ha='center')
ax.annotate('\u201cnot a good pupil,\nbut a good learner\u201d',xy=(6,8.8),xytext=(3.0,3.0),fontsize=6.6,color=INK,arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8),ha='center')
ax.annotate('\u201ca murder,\na crime\u201d',xy=(13,1.2),xytext=(10.3,1.3),fontsize=6.6,color='#A8271F',arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8),ha='center',va='center')
fig.subplots_adjust(left=0.03,right=0.97,top=0.97,bottom=0.17)
```

## 13.5 Style and devices

**Personal voice and plain diction.** Sacks writes in the first person and in short,
unforced sentences. The essay contains very few difficult words; the difficulty (as the
glossary shows) is in the *names* — Mellor, Gmelin, Gesner, Agassiz, Browne — and these
are there for a reason, described below.

**Catalogues.** Long lists of authors and titles recur (the mother's shelf; the Queen's
vaults). They work like the shelves themselves: the reader is made to walk along them.
The lists also show Sacks's range — Kipling to Gmelin, Dryden to Darwin.

**Contrast (antithesis).** *Not a good pupil, but a good learner.* *Instruction* versus
*freedom*. *Quiet* library versus *whispered* friendships. Above all, the essay's two
halves — **then** and **now**, shelf and screen.

**Allusion and the "Ur-library".** Naming real books and real places makes the essay
credible and lets the reader see the shelves. *Ur-* (German for "original") gives
Willesden a mythic importance: the first library, the source of all others.

**Metaphors of space and journey.** The library is a **maze**, **catacombs**, **vaults**,
**stacks** to be "roamed"; the readers are on **quests**. These images make reading an
adventure and the reader an explorer.

**Verbs of hunger.** He *hungered* for science books and *devoured* Mellor's volumes.
Reading is presented as appetite — which is why the modern preference for a quick
search feels, to him, like a diet of crumbs.

**Tone.** Warm and grateful for ten paragraphs; sober and then **indignant** in the
last two. The single most forceful word, "murder", is saved for the end and applied to
books, which is a deliberate **hyperbole** — an exaggeration that shows the depth of
feeling.

**Symbol of the physical book.** "Its look, its smell, its heft" — three senses, three
words — stands for everything a screen cannot carry: memory, place, continuity.

## 13.6 Glossary

| Word | Meaning |
|---|---|
| fantasies | imaginary adventures; things one dreams up |
| morocco | fine, soft goat-skin leather used for binding books |
| curl up | to sit or lie with the legs drawn up in a comfortable position |
| absorbed | so deeply interested that nothing else is noticed (an *adjective*; the textbook wrongly marks it as an adverb) |
| vied with | competed with |
| Ur-library | (*Ur-* is German) the original, first and archetypal library |
| astronomy | the scientific study of the sun, moon, stars and planets |
| hungered for | wanted very strongly |
| testimonial | a written statement recommending someone |
| devoured | read greedily and quickly, as if eating |
| Comprehensive Treatise | a very complete, formal, multi-volume work on a subject |
| stumbled upon | found by chance |
| improvisation | composing or performing on the spot without preparation |
| case-history | a detailed record of one person's life and condition, as doctors keep |
| tranquil | calm and quiet |
| incunabula | books printed in the earliest years of printing, before 1501 |
| magniloquence | grand, high-flown language |
| lapidary | (of writing) elegant, exact and concise, as if cut in stone |
| catacombs | underground passages or chambers |
| stacks | the rows of shelving in which library books are stored |
| enclave | a small area with a special character, enclosed within a larger one |
| pokey | small, cramped and unpleasant |
| aloft | high up; in the air |
| camaraderie | friendship and trust among people who spend time together |
| rummaging | searching by turning things over |
| heft | weight; the feel of something heavy in the hand (the textbook glossary misprints this as "helt") |
| digitised | converted into computer-readable form |
| irreplaceable | impossible to replace once lost |

::: note Words that are easy to confuse
**Library** (a collection of books, or the room that holds it) and **librarian** (the
person who looks after it). **Serendipity** (finding something good by chance) and
**synchronicity** (a meaningful coincidence). **Digital** (stored and read on a
computer) and **physical** (held in the hand).
:::

## 13.7 Textbook exercises

**Before you read**

*a. Why do people visit the libraries?*

People go to libraries for many reasons. Students go to **study quietly** and to find
books they cannot afford to buy; researchers go for **reference works and old records**
that are found nowhere else; ordinary readers go for **pleasure and relaxation**; and
many go simply for the **company** of other readers. Libraries also lend newspapers,
magazines and, today, computers and internet access, so that people without them at home
are not left behind.

*b. Have you ever borrowed books from the library? If yes, what kinds of books do you like to read?*

A personal answer is expected. Model: Yes, I borrow from my school library and from the
community library in our ward. I like **short stories and biographies** because they show
how real people overcame difficulties, and I borrow **science magazines** when I want
explanations that are simpler than my textbook's. I avoid books that are only summaries of
exam answers, because they teach me nothing that I can use outside the examination hall.

**Understanding the text**

*a. Where could the author be found when he was late for lunch or dinner?*

He could be found in the **oak-panelled library at home**, curled up in a chair and so
completely absorbed in a book that he had lost all sense of time.

*b. What are his first memories?*

His first memories are of **books and the family library**. He learned to read early, at
three or four, and the library where his father, mother and brothers kept their books
was already his favourite room.

*c. Why did he dislike school?*

He disliked sitting in class **passively receiving instruction**: information seemed to
go in one ear and out of the other. He wanted to learn actively — what he chose, in the
way that suited him — and school did not allow that. He calls himself "not a good pupil,
but … a good learner".

*d. What did he feel about the library?*

He felt **free**. In the library he could look at thousands of books, choose whatever he
liked, follow whatever paths fascinated him and "become myself". He also enjoyed its
special atmosphere and the quiet companionship of other readers, each on a quest of his
or her own.

*e. Why was he so biased towards the sciences, especially astronomy and chemistry?*

As he grew older his interests turned towards science, and the essay gives no reason
beyond that growing interest. What it does show is how strong the interest was: he
"hungered" for chemistry books, which the excellent but history-heavy Walker Library at
St Paul's could not supply, so he got a ticket to the Science Museum library and read
Mellor and Gmelin. His little chemistry "lab" at home, which he says rivalled the library
as his favourite place, points the same way.

*f. Why did he become so fascinated by Hook?*

Theodore Hook was a man greatly admired in the early nineteenth century for his **wit**
and for his genius at **improvising** in theatre and music; he was even said to have
composed more than five hundred operas on the spot. Sacks found his forgotten works by
chance in the Bodleian and was so struck by such a gifted, neglected man that he decided
to write a biography or "case-history" of him.

*g. Describe the library at the Queen's College.*

The library building was designed by **Christopher Wren** and was magnificent. Beneath it,
in an underground **maze of heating pipes and shelves**, lay the huge holdings, like
catacombs. There Sacks handled **incunabula**, saw **Gesner's *Historiae Animalium*** (1551)
with Dürer's rhinoceros, Agassiz's volumes on fossil fishes and **all of Darwin's works in
their original editions**, and discovered Sir Thomas Browne, Swift, Johnson, Hume, Pope and
Dryden. The books were **freely available** on open shelves, not locked away. He says it was
there that he gained "a sense of history, and of my own language".

*h. Why did the students ignore the bookshelves in the 1990s?*

Because they could get what they needed through their **computers**. Few of them went to
the shelves any more; as far as they were concerned the books were unnecessary.

*i. Why was he horrified when he visited the library a couple of months ago?*

He found the shelves, once overflowing, **sparsely occupied**: most books had been thrown
out, with almost no objection from anyone. He felt it was like "a murder, a crime" — the
destruction of centuries of knowledge.

**Reference to the context**

*a. The author says, "I was not a good pupil, but I was a good listener." Justify it with textual evidence.*

Note first that the textbook has misquoted the essay: Sacks writes "a good **learner**",
not "listener". Answer the question as it is set, but if you can, use the right word.
Sacks disliked school because passive instruction bored him: "information seemed to go in
one ear and out by the other." A good pupil accepts what the teacher offers; Sacks could
not. But he was an excellent *learner*, because he **learned actively for himself**. In the
library he "roamed the shelves and stacks", chose "whatever I wanted", and followed
"paths which fascinated me". As a boy he devoured Mellor's and Gmelin's chemistry volumes
after a school library could not supply them, and at Oxford he taught himself
seventeenth-century literature in the Queen's vaults and researched Theodore Hook. A
pupil waits to be taught; a learner goes and finds out — and Sacks was the second kind.

*b. A proverb says, "Nothing is pleasanter than exploring a library." Does this proverb apply in the essay? Explain.*

Yes, it applies completely. Exploring is exactly what Sacks describes: he "roamed the
shelves and stacks" at Willesden, discovered Hook by chance in the Bodleian, "stumbled
upon" old treasures in the Queen's catacombs and, in New York, would "wander around the
shelves and stacks" without knowing what he might find. Each search ends in delight — the
"unexpected treasures, lucky finds". The pleasure of exploring is also social, because
whispered conversations in the stacks turned into friendships. The proverb even explains
his sorrow at the end: when the shelves are emptied there is nothing left to explore.

*c. Are there any other services that you would like to see added to the library?*

An opinion answer. Model: I would like libraries to add **audio books and large-print
and Braille editions** so that visually impaired readers can use them; a **digital
section** with internet and e-books, provided that the printed books stay on the shelves;
**quiet study rooms** for group work; **evening and holiday opening hours**; **reading
clubs and author talks** to bring young readers in; and a **mobile library** to serve
villages far from any town. New services should be *added* to the shelves, not put in
their place — which is the lesson of Sacks's essay.

**Reference beyond the text**

*a. Write an essay on Libraries and its uses for students.*

Model essay (about 250 words).

**Libraries and Their Uses for Students.** A library is an organised collection of books,
journals, newspapers and other resources kept for public use. For a student it is a
second classroom, and in many ways a better one, because the student chooses the lesson.

The first use of a library is **reference and study**. A textbook gives one writer's
account; a library gives many, so that a student can compare, check facts and understand a
topic more deeply. Books that are too expensive to buy — dictionaries, encyclopaedias,
atlases, past question papers — are available free of charge. The second use is
**self-education**. Like Oliver Sacks, a curious student can follow a subject as far as his
interest takes him, beyond the syllabus. Reading widely also improves vocabulary,
writing and concentration, which help in every examination. Third, a library gives a
**quiet place to work**, especially to students whose homes are crowded or noisy. It also
teaches **discipline and respect** — silence, careful handling of books, and return on time.

Today most libraries also provide computers, e-books and internet access, which open
further sources of knowledge. But the printed shelves still matter, for browsing among them
often leads to discoveries that a search cannot. A student who uses the library regularly
learns not only facts but how to find them, and that is the beginning of independent
thought.

*b. Do you have any public library in your locality? If so, do the people in your community use it? Give a couple of examples.*

A personal answer, drawn from the student's own community, is expected. Model: Yes, there
is a community library in our tole, opened by a youth club with donated books. **Students**
use it most, especially in the weeks before the board examinations, when they borrow past
papers and reference books and study in its small reading room. **Older residents** come in
the morning to read the newspapers and magazines, and on Saturdays a local teacher runs a
story hour for young children. Use is less than it could be, because many families do not
know the library exists and because it has few new books. A regular reading campaign and a
computer with internet would bring more readers.

## Chapter summary

- "On Libraries" is a personal essay by the neurologist and writer **Oliver Sacks**
  (1933–2015); it praises libraries as places of **intellectual freedom, community and
  serendipitous discovery**, and was published in *The Threepenny Review* and, as
  "Libraries", in *Everything in Its Place* (2019).
- Childhood: the **oak-panelled home library** (father's Hebrew scholarship, Ibsen, war
  poets, brothers' adventure books, *The Jungle Book*; mother's Dickens, Trollope,
  Thackeray, Shaw, Kipling, Shakespeare, Milton); he read at **three or four** and was
  found in the library when late for meals.
- **Willesden Public Library** was his "Ur-library" and his "real education". He disliked
  school but was "not a good pupil, but … a good learner": in libraries he was **free**
  to choose and "become myself".
- Science: the **Walker Library** at St Paul's lacked chemistry, so a testimonial got him
  into the **Science Museum library** (Mellor's *Treatise*, Gmelin's *Handbook*).
- Oxford: the **Radcliffe Science Library** and the **Bodleian** (traced to 1602; Theodore
  Hook, over 500 improvised operas; British Museum Library); above all the **Queen's
  College library** (Wren; catacombs; incunabula, Gesner 1551, Agassiz, Darwin, Browne,
  Swift, Johnson, Hume, Pope, Dryden) — "a sense of history, and of my own language".
- New York, 1965: *Migraine* begun on top of a refrigerator; the **Albert Einstein
  College of Medicine** library gave space, lucky finds and friendships (*Brain* from
  1890).
- The turn: by the **1990s** students ignored the shelves, books were disposed of; Sacks
  was **horrified** ("a murder, a crime"), was told everything "of worth" had been
  digitised, and answered that a physical book has "its look, its smell, its heft".
- Devices: first-person memoir, catalogues, contrast, metaphors of maze and quest, hyperbole
  ("murder"), the symbol of the physical book.

## Practice questions

**Short answer questions (2 marks each)**

1. Why did Sacks call Willesden Public Library his "Ur-library"? <span class="marks">[2]</span>
2. How did Sacks get into the library of the Science Museum? <span class="marks">[2]</span>
3. Why does the author appreciate the Queen's College library? (NEB 2080, GIE Set A) <span class="marks">[2]</span>
4. Why do you think the modern students ignore the bookshelves? (NEB 2081, Set A) <span class="marks">[2]</span>
5. What made the essayist unhappy when he visited the library a couple of months ago? (NEB 2081, Set B) <span class="marks">[2]</span>
6. How does the writer's family background inspire him to learn from the library? (NEB 2081, Set B) <span class="marks">[2]</span>
7. What impression did the author have about the library at the Albert Einstein College of Medicine? (NEB 2081, Set C) <span class="marks">[2]</span>
8. What did the librarian assure the author? (NEB 2079, GIE) <span class="marks">[2]</span>
9. Why does the digital library not interest the author? (NEB 2082) <span class="marks">[2]</span>
10. Why was the author biased towards science? (NEB 2080, Set D) <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** *Ur-* is a German prefix meaning "original". Willesden, the public library a
five-minute walk from his home, was the first great library of his life and the standard
for every library after it: there, he says, he "received my real education".

**2.** The Walker Library at his school, St Paul's, had few science books, so a
schoolmaster wrote him a special **testimonial**. With that recommendation he obtained a
ticket to the Science Museum library and read the huge chemistry works of Mellor and
Gmelin.

**3.** He appreciates it for its **magnificent building** (designed by Wren), its
underground "maze of heating pipes and shelves", and above all its holdings: ancient
books, Gesner's *Historiae Animalium*, Agassiz, Darwin's works in original editions, Browne,
Swift, and the seventeenth- and eighteenth-century writers. The books were freely available
on the shelves, and there he "really gained a sense of history, and of my own language".

**4.** Because by the 1990s they could find whatever they needed through **computers**, so
the shelves seemed unnecessary. To them the printed books were no longer the first place to
look, and few visited the stacks at all.

**5.** He found the shelves, once overflowing, **sparsely occupied**; most of the books
had been thrown out over a few years, with hardly any objection. He felt that a crime had
been committed against centuries of knowledge.

**6.** His father's Hebrew scholarship, his parents' Ibsen society, his mother's books
and his brothers' adventure books meant that **shelves of books surrounded him from birth**.
He could pick up a book at any time, learned to read at three or four and made the oak-panelled
library his favourite place — the beginning of a lifelong habit of learning in libraries.

**7.** He found it **spacious**, which he had longed for after his cramped flat. It had a
large table where he could read and write and shelves and stacks where he could wander and
find "unexpected treasures, lucky finds". It was quiet, but whispered conversations led
to friendships, and it gave him a sense of **community, even intimacy**.

**8.** The librarian, seeing his distress, assured him that everything "of worth" had
already been **digitised**, so nothing valuable was lost.

**9.** He values what only a **physical book** can offer — "its look, its smell, its
heft" — and the freedom of browsing among shelves. He does not use a computer himself, and
he feels a digital copy cannot replace the book, the shelf and the reader's community.

**10.** As he grew older his interest turned to **astronomy and chemistry**. The essay says
his reading became "increasingly biased towards the sciences", and his hunger for chemistry
books that the school library lacked led him to the Science Museum library.
:::

**Long answer questions (5 marks each)**

1. In the essay "On Libraries", Oliver Sacks talks about two kinds of library — the
   traditional library and the modern, digital one. Which do you find more impressive, and
   why? (NEB 2082, adapted) <span class="marks">[5]</span>
2. "On Libraries" is written in praise of intellectual freedom, community and serendipitous
   discovery. Discuss. <span class="marks">[5]</span>
3. What did libraries give Oliver Sacks at each stage of his life? Trace the
   development of his relationship with libraries. <span class="marks">[5]</span>
4. Do you agree with Sacks that the loss of physical books is a great loss? Give reasons
   from the essay and from your own experience. <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** Sacks describes the **traditional library** in loving detail: oak-panelled rooms, open
shelves and stacks, quiet tables, whispered talk that turns to friendship, old books
in original editions — and, at the end, a **digital library** in which books are scanned and
the paper copies thrown away. I find the traditional library more impressive, and Sacks
gives me the reasons. First, it gives **freedom to browse**: he "roamed the shelves" and
found "unexpected treasures, lucky finds", such as Hook in the Bodleian and Liveing's
*Megrim* in the stacks. A search returns only what you ask for; a shelf shows you
what you did not know to ask. Second, it builds **community**: readers looking for the same
volume of *Brain* became friends, and handling books and seeing earlier borrowers' names
created "camaraderie". Third, the physical book has a **sensory and historical value** —
"its look, its smell, its heft" — which a scan cannot carry. That said, a digital library
has real advantages: it reaches distant readers, it saves space and it can protect fragile
texts. The wisest answer is that we should **add** the digital library to the traditional
one, not use it to destroy the shelves; Sacks's grief is at the destruction, not at the
technology itself.

**2.** The headnote's three phrases each name a strand of the essay. **Intellectual
freedom** is the freedom to choose what to read, which he found at Willesden, where he was
"free to look at the thousands, tens of thousands, of books" and "to become myself", in
contrast with school where he was passive. **Community** is the intimacy of strangers
in a quiet room: two readers whispering over the same old book, sharing volumes and seeing
each other's names on the library slips. **Serendipity** is the joy of lucky finds —
discovering Hook, or Sir Thomas Browne in the stacks, or the 1873 book that inspired
his first book. All three depend on **physical shelves and open access**, which is why the
essay ends in sorrow when students ignore them and colleges dispose of the books.
The praise of libraries is therefore also a defence of a certain kind of education:
self-directed, sociable and full of surprise.

**3.** *Home library:* books and reading became his first memories; he read at three or four
and found fantasy in *The Jungle Book*. *Willesden:* his "real education"; freedom to choose;
independence from the school that bored him. *Walker Library and Science Museum library:*
his first serious training in chemistry, when his school could not supply the books.
*Oxford:* the Bodleian gave him a subject in Theodore Hook and a quiet place to write; the
Queen's College library gave him "a sense of history, and of my own language" through
original editions of Darwin, Browne, Swift and others. *New York:* the Einstein College
library gave him space to read and write after his cramped flat, lucky finds and
friendships. *The 1990s:* the library as he had known it began to disappear, and he was
left grieving. The relationship therefore grows from **shelter** to **freedom** to
**training** to **scholarship** to **community**, and ends as a **loss** he cannot
prevent.

**4.** I agree with Sacks that it is a great loss, though not one to be blamed on
technology alone. His argument is that digitisation saves the *text* but destroys the
*book*: its "look, its smell, its heft", its neighbours on the shelf and the names of
earlier readers. It also destroys **serendipity**: he found Hook and *Megrim* only by
wandering among real shelves. And a library that disposes of its old books cannot
rediscover them later; once a book is thrown out and the scan is lost or unreadable,
knowledge vanishes. In my own experience, a book on a school shelf beside the one I
wanted has often taught me something I did not plan to learn. On the other hand, I know
that digital libraries help students in remote parts of Nepal who have no shelves at
all. So the loss is real but avoidable: keep the books and add the screens.
:::

::: tip Reference-to-the-context practice
Take any sentence from the essay and ask four things of it: (a) who says it and where;
(b) what comes immediately before or after; (c) what it means in plain words; (d) why it
matters to the whole essay. For "But a shift was occurring by the 1990s": (a) Sacks, at the
turn from memories to the loss of libraries; (b) after the New York friendships, before
the students who ignore the shelves; (c) the way people used libraries was changing;
(d) it is the hinge of the essay, from praise to grief.
:::

---
subject: Compulsory English
grade: 8
unit: 8
title: Having Fun / Historical Inventions
hours: 0
area: Units
---

Two texts that look backwards. The first is a piece about **leisure** — how
people take their fun, and how the way we spend free time has changed within
living memory. The second is **historical writing** about inventions: not who
thought of them, but how they changed the ordinary day of ordinary people. Both
need the tenses that place events in the past and in order, and both need the
structure *used to* for habits that have gone.

::: key What this unit asks of you
By the end you should be able to (1) narrate a past event using the past simple
and the past continuous together, (2) use the past perfect to show which of two
past actions happened first, (3) use *used to* for a habit that has stopped,
and (4) write a narrative essay and complete a skeleton story.
:::

## 8.1 Having Fun

### About the text

The text is **descriptive and comparative** writing about the way people enjoy
themselves. It sets the older pattern — games in the street or the field, songs
at a festival, stories told in the evening — beside the newer one: television,
mobile games, films and organised sport. It does not say the older way was
better; it notices what has been gained and what has been lost.

### What the text says

Leisure is the time that is left when work, school and sleep have taken their
share. What people do with it says a great deal about them: how much money they
have, how much room, how much daylight, and how far from the next house they
live.

In Nepal, as recently as two generations ago, most of the country's leisure was
**shared and outdoors**. Children played *dandi biyo*, *kabaddi*, *lukamari*,
marbles and gilli in the open ground, and the games needed nothing that had to
be bought. Women sang *dohori* at festivals and at the rice-planting; whole
villages danced at Tihar and in the *mela* that came with the festival. Adults
gathered in the evening to tell stories, to play *madal* and *sarangi*, and to
argue about the harvest. Almost all of it happened in public, with other
people, and most of it cost nothing.

Three changes altered that pattern. First, **the radio and then the television**
brought an audience of one: entertainment no longer needed the company of
others. Second, **migration and city life** removed the open ground and the
long evening; a family living in a rented room in a crowded street cannot play
kabaddi in the lane. Third, **the mobile phone** made entertainment portable and
private — and put a screen where a friend used to be. There is now more
entertainment available than at any time in history and, many people argue,
less *play*.

The older ways have not gone, however. Kabaddi is still played, *dohori* is
still sung, and the new games most people enjoy are still the ones played with
somebody else. What has changed is that each of them now competes with a screen,
and has to be chosen deliberately.

| Then | Now | What changed |
|---|---|---|
| Street games (kabaddi, lukamari, marbles) | Mobile and video games | the players no longer need to be in the same place |
| Songs at every festival and in the fields | Streaming and recorded music | the singing is listened to, not joined |
| Stories told in the evening | Television, film, short video | the family sits together, looking one way |
| Village *mela* and fairs | City parks, organised sport | leisure moved indoors and became paid |
| Cheap and shared | Often private and paid for | the cost of fun has risen |

```figure caption="What leisure needs. When a society loses a public open space, a long free evening or a comfortable income, the shared form of fun loses its place to the private form."
fig, ax = plt.subplots(figsize=(4.9, 2.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.0); ax.axis("off")
req = [("open space", SERIES[0]), ("free time", SERIES[1]),
       ("other people", SERIES[2]), ("money", SERIES[3])]
for i, (name, colour) in enumerate(req):
    x = 0.5 + i * 2.4
    ax.add_patch(plt.Circle((x + 1.0, 3.4), 0.72, fc="white", ec=colour, lw=1.5))
    ax.text(x + 1.0, 3.4, name, ha="center", va="center", fontsize=6.2, color=INK)
    ax.annotate("", xy=(x + 1.0, 2.55), xytext=(x + 1.0, 2.68),
                arrowprops=dict(arrowstyle="->", color=GRID, lw=1.2))
ax.text(5.0, 1.9, "shared play", ha="center", fontsize=7.4, color=ACCENT,
        fontweight="bold")
ax.text(5.0, 0.9, "remove any one of the four and the shared form gives way to the private one",
        ha="center", fontsize=6.1, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| leisure | free time, when there is no work to do |
| dohori | a Nepali question-and-answer folk song |
| mela | a fair or festival gathering |
| deliberately | on purpose, after thinking about it |
| portable | able to be carried about |
| public | open to everybody, in a shared place |

::: note Model answers
**1. Why was most leisure in the past shared and outdoors?**
Because there was not much to buy, the evenings were long and there was open
ground in every village — so entertainment had to be made by the people present,
which made it a public and shared activity.
**2. What are the two sides of the mobile phone as a form of leisure?**
It offers more choice than any previous generation had, and it can be used
anywhere; but it also makes entertainment private, so it can replace the company
of other people rather than add to it.
:::

## 8.2 Historical Inventions

### About the text

The text is **historical writing**. It explains what an invention was, when it
appeared, and — the part that matters — what difference it made. Good
historical writing answers "so what?" after every date.

### What the text says

**The printing press.** Before Johannes Gutenberg's movable-type press (around
1440), every book was copied by hand, and a single copy of the Bible could take
a scribe a year. The press made copies cheap and many, and ideas that had
travelled by word of mouth began to travel in print.

**The steam engine.** Thomas Newcomen's engine (1712) pumped water out of mines;
James Watt improved it from 1769, and by the nineteenth century steam powered
mills, ships and railways. Work moved from the home to the factory, and towns
grew wherever the coal was.

**Electricity and the light bulb.** Michael Faraday's experiments in the 1830s
showed how a changing magnetic field produces an electric current, which made
generators possible. Practical incandescent lamps arrived in the 1870s, and
streets, homes and factories could work after dark.

**The telephone and the radio.** Alexander Graham Bell patented the telephone in
1876, and Guglielmo Marconi sent the first radio signals across the Atlantic in
1901. Distance stopped deciding who could speak to whom.

**The computer and the internet.** Early electronic computers of the 1940s filled
a room; the internet grew out of research networks in the 1960s and 1970s and
reached the public in the 1990s. The change is best described simply: the cost
of storing, finding and sending information collapsed.

Each of these inventions did the same three things: it made something **cheaper**
or **faster**, it moved activity from one place to another, and it changed the
**daily routine** of ordinary people.

| Invention | Date | Before | After |
|---|---|---|---|
| Printing press | c. 1440 | a book copied by hand | books printed in hundreds |
| Steam engine | 1712, improved 1769 | work at home, by muscle and water | factories, railways, cities |
| Electric light | 1870s | the day ended at sunset | work and study after dark |
| Telephone, radio | 1876, 1901 | news travelled by post | voices crossed continents at once |
| Computer, internet | 1940s–1990s | information expensive and slow | information almost free |

::: note Model answers
**1. Why is the printing press called a turning point in history?**
Because it made copies cheap and plentiful, so knowledge stopped depending on
the memory of a few scribes and could spread to many people at once.
**2. Which invention changed daily routine the most, and why do you think so?**
Answers will vary, but a strong answer names the change: the electric light
extended the working and studying day, while the internet changed how
information is found, so both altered what an ordinary evening contains.
:::

## 8.3 Grammar and writing tasks of the unit

### Grammar: Past simple, past continuous and past perfect

| Tense | Form | Use | Example |
|---|---|---|---|
| Past simple | verb + -ed / irregular | a finished action | We **played** kabaddi. |
| Past continuous | was/were + -ing | an action in progress, often interrupted | We **were playing** when it began to rain. |
| Past perfect | had + past participle | the earlier of two past actions | The rain **had stopped** before we went out. |

The past continuous usually sets the scene and the past simple interrupts it.
The past perfect is used only when you need to make clear that one past action
happened **before** another; if the order is already clear from *then*,
*after* or *before*, the past simple is enough.

### Grammar: used to

**used to + bare verb** describes a habit or a state in the past that is no
longer true: *We **used to** play in the street.* The negative is *didn't use
to* (no *-d* after *did*), and the question is *Did you use to…?* Notice that
*used to* can only describe the past — for the present habit, use the present
simple with an adverb: *I usually play football on Saturdays.*

::: caution Common mistakes
- *I am used to play football.* ✗ (that means "I am accustomed to it") →
  *I **used to play** football.* ✓
- *He didn't used to smoke.* ✗ → *He didn't **use** to smoke.* ✓
- *When we arrived, they already left.* ✗ → *When we arrived, they **had
  already left**.* ✓
- Mixing tenses without reason across a narrative. Choose one past tense for
  the events and keep it.
:::

### Writing: A narrative essay

A narrative essay tells a story with a point. Paragraph 1: the setting, in the
past continuous (*The sun was setting and the field was full of people*).
Paragraph 2: the events in order, in the past simple, with one moment given in
detail. Paragraph 3: what it meant, or what you understand now that you did
not then.

::: note Model answers to the writing tasks
**Skeleton story.** *When I reached the ground, the match had already begun.*
Continue: the setting (dust, crowd, the score), the problem (you are late and
your team is losing), the attempts (you are sent on; you miss; you get one more
chance), the resolution (the last point, and what your team-mates said
afterwards). Keep the *had already begun* construction to show which action
came first.
:::

## Chapter summary

- Leisure is the time left after work, school and sleep; how people spend it
  shows how much space, money and daylight they have.
- Older Nepali leisure was shared, public and cheap; modern leisure is often
  private, indoor and paid for.
- Radio, television, migration to cities and the mobile phone changed that
  pattern within two generations.
- Historical writing about an invention must always answer "so what?" — what
  changed for ordinary people.
- The printing press, the steam engine, electric light, the telephone and radio,
  and the computer all made something cheaper or faster, moved activity to a
  new place, and changed the daily routine.
- **Past simple** = finished action; **past continuous** = in progress;
  **past perfect** = the earlier of two past actions.
- **used to** describes a past habit that has stopped; after *did*, write *use
  to*, with no *-d*.

## Practice questions

**Reading**

1. Give three reasons why the pattern of leisure changed in Nepal. <span class="marks">[3]</span>
2. Why is the printing press considered a turning point? <span class="marks">[2]</span>
3. Name two inventions of the nineteenth century and say what each changed. <span class="marks">[2]</span>
4. "There is now more entertainment available than at any time in history and,
   less play." What does this sentence mean? <span class="marks">[2]</span>

::: note Answers
**1.** Radio and television brought entertainment to a single viewer at home;
migration and city life removed open ground and the long free evening; the
mobile phone made entertainment private and portable.
**2.** It made copies cheap and plentiful, so knowledge could spread to many
people instead of depending on a few scribes copying by hand.
**3.** The steam engine — moved work from home to factories and made railways
possible. The electric light — extended the working day past sunset. (The
telephone and radio are also correct.)
**4.** There are far more things to watch and do, but they are often done
alone in front of a screen, so the shared, active element of play — playing
with other people — has become less common.
:::

**Grammar**

5. Put the verbs in the correct past tense. <span class="marks">[5]</span>
   (a) We ______ (play) when the bell ______ (ring).
   (b) She ______ (finish) her work before her father ______ (come) home.
   (c) They ______ (walk) to school every day when they lived in the village.
   (d) I ______ (see) him yesterday at the mela.
   (e) By the time we arrived, the film ______ (start).

::: note Answers
**5.** (a) were playing / rang (b) had finished / came (c) used to walk
(d) saw (e) had started
:::

**Writing**

6. Write a narrative essay of about 150 words on a festival you remember
   vividly. <span class="marks">[5]</span>
7. Write a paragraph of about 80 words comparing how your grandparents spent
   their free time with how you spend yours. Use *used to* at least twice. <span class="marks">[4]</span>

::: note Answers
**6.** Paragraph 1: set the scene with the past continuous ("The drums were
still going and the whole lane was full of people"). Paragraph 2: the events in
order in the past simple, with one moment in detail. Paragraph 3: what the day
meant to you, and what you understand about it now.
**7.** Use *used to* for the grandparents ("They used to gather in the
courtyard after dinner") and the present simple with an adverb for yourself
("I usually watch videos before bed"). End with one sentence about what has
been gained and one about what has been lost.
:::

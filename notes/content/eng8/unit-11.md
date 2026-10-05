---
subject: Compulsory English
grade: 8
unit: 11
title: Sir Isaac Newton / Khaptad National Park
hours: 0
area: Units
---

This unit gives you one **biography** and one **description of a place**. They
look like very different texts, but they share a purpose: both take a subject
that the reader does not know and make it clear by giving facts in order and
adding one thing at a time. The grammar of the unit is the glue that holds such
writing together: **relative clauses** (which add information about a noun) and
**articles** (*a, an, the*).

::: key What this unit asks for
By the end you should be able to (1) write a profile of a person in
chronological order, (2) describe a place — its location, features and
importance — without turning it into a list, (3) join sentences with who,
which, that, where and whose, and (4) choose correctly between *a*, *an*, *the*
and no article.
:::

```photo id="eng8/newton-portrait" caption="Sir Isaac Newton, painted by Godfrey Kneller in 1689, two years after the Principia was published." width="68"
```

```photo id="eng8/khaptad" caption="The open plateau of Khaptad National Park in far-western Nepal. Its high-altitude grassland, ringed by oak and rhododendron forest, is the habitat that makes the park unusual." width="92"
```

## 11.1 Sir Isaac Newton

### About the text

The text is a **biography** — the story of a real person's life, told in time
order. A biography is not a list of dates. It chooses the events that explain
the person and leaves the rest out, and it shows how the work of one period led
to the work of the next.

### What the text says

**Isaac Newton** was born in Woolsthorpe, in Lincolnshire, England, on
25 December 1642 — the same year in which Galileo died. His father had died
before he was born, and he was brought up for a time by his grandmother while
his mother remarried. He was not a remarkable schoolboy, but he was good with
his hands, and he made water clocks and model windmills.

He entered Trinity College, Cambridge, in 1661. In 1665 the plague closed the
university and he went home to Woolsthorpe for nearly two years. Those two
years — he was twenty-three — were the most productive of his life. He worked
out the **binomial theorem**, began the mathematics of what we now call
**calculus**, and used a prism to show that white light is a mixture of colours
which the prism separates and a second prism can recombine.

The story of the falling apple is the one everybody knows. Whether or not the
apple actually fell on his head, Newton himself said that watching an apple
fall made him ask whether the force that pulls an apple to the ground is the
same force that holds the Moon in its path. The answer — that the same
**gravitation** acts on both, with a force that weakens with the square of the
distance — is the idea of the *Principia* (*Mathematical Principles of Natural
Philosophy*), published in 1687.

Newton was also, for thirty years, a public servant. He became a Member of
Parliament for Cambridge, then Warden and later Master of the Mint, where he
reformed the coinage. He was elected President of the Royal Society in 1703 and
was knighted in 1705. He died on 20 March 1727 and was buried in Westminster
Abbey.

He was not a modest man: he quarrelled fiercely with other scientists, notably
with Robert Hooke and with Gottfried Leibniz over who invented calculus first.
His most quoted sentence is modest, though: *"If I have seen further, it is by
standing on the shoulders of giants."*

| Year | Event |
|---|---|
| 1642 | Born at Woolsthorpe; Galileo dies the same year |
| 1661 | Enters Trinity College, Cambridge |
| 1665–66 | The plague years at Woolsthorpe: light, calculus, gravitation |
| 1687 | Publishes the *Principia* |
| 1703 | Elected President of the Royal Society |
| 1705 | Knighted |
| 1727 | Dies and is buried in Westminster Abbey |

```figure caption="A biography is a shape, not a list. Newton's most productive two years came at twenty-three; the famous book came twenty years later. It is the connection between the periods that makes a profile worth reading."
fig, ax = plt.subplots(figsize=(4.9, 2.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.0); ax.axis("off")
ax.annotate("", xy=(9.6, 1.2), xytext=(0.4, 1.2),
            arrowprops=dict(arrowstyle="->", color=GRID, lw=1.5))
events = [(1.2, "1642\nborn", SERIES[0]), (3.0, "1665–66\nplague years", ACCENT),
          (5.3, "1687\nPrincipia", SERIES[2]), (7.4, "1705\nknighted", SERIES[3]),
          (9.0, "1727\ndies", SERIES[4])]
for x, label, colour in events:
    ax.plot(x, 1.2, "o", color=colour, ms=7)
    ax.text(x, 1.85, label, ha="center", fontsize=6.2, color=INK)
ax.add_patch(plt.Rectangle((2.2, 3.1), 1.6, 1.0, fc="white", ec=ACCENT, lw=1.3))
ax.text(3.0, 3.6, "the two years that\nmattered most", ha="center", va="center",
        fontsize=6.0, color=ACCENT)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| biography | the written life of a real person |
| plague | a deadly infectious disease that spreads fast |
| prism | a triangular piece of glass that splits light into colours |
| calculus | the mathematics of change and of areas |
| gravitation | the force by which every mass attracts every other |
| knighthood | the honour of being made "Sir" by a monarch |

::: note Model answers
**1. Why are the plague years called the most productive of Newton's life?**
Because, sent home from Cambridge by the plague, he worked alone for two years
on the binomial theorem, calculus, the nature of light and the beginning of the
idea of universal gravitation — a large part of his life's work at the age of
twenty-three.
**2. What is the scientific point of the apple story?**
Not that an apple hit him, but that he asked whether the force pulling the apple
down is the same as the force keeping the Moon in orbit — the insight that made
one law explain both the earth and the sky.
:::

## 11.2 Khaptad National Park

### About the text

The text is a **descriptive** account of a protected area. A description of a
place answers four questions in order: **where** it is, **what** it is like,
**what** lives there, and **why** it matters. It uses the present simple tense,
because a place keeps its shape from year to year.

### What the text says

**Khaptad National Park** lies in the far west of Nepal, spread across the
districts of Bajhang, Bajura, Achham and Doti in Sudurpashchim Province. It was
established in 1984 and covers about 225 square kilometres, at an altitude
between roughly 1,000 and 3,300 metres. The **Khaptad plateau** at its centre is
a wide, open grassland set among hills of oak, rhododendron and fir — a rare
combination in Nepal, where most protected areas are either forest or high
mountain, and one reason the park is famous for its **wild flowers and
medicinal herbs**, which are at their best after the first monsoon rains.

The park is named after **Khaptad Baba**, a saint who lived and meditated on the
plateau for many years and whose hermitage is still visited; there is a temple
and an ashram there, and a temple at **Sahashra Linga** on the eastern side.
Because the plateau is high and open, the nights are cold even in summer, and
snow falls in winter.

| Aspect | Detail |
|---|---|
| Location | Far-western Nepal: Bajhang, Bajura, Achham and Doti |
| Established | 1984 |
| Area | about 225 km² |
| Altitude | roughly 1,000–3,300 m |
| Main habitat | open high-altitude grassland ringed by oak, rhododendron and fir forest |
| Famous for | wild flowers, medicinal herbs, and the hermitage of Khaptad Baba |
| Access | by road and on foot from Chainpur, Dipayal and Sanphebagar |

The park is important for three reasons. It protects a **habitat** that exists
in very few places in Nepal, so it protects the plants and animals that live
only in such a habitat. Its grassland catches and stores the water of the
monsoon, which feeds the streams that four districts depend on. And it supports
**local livelihoods** — guiding, portering, homestays and the collection of
herbs under licence — which gives the people around it a reason to protect it.
Its problems are the usual ones: grazing by livestock inside the boundary,
the illegal collection of herbs, forest fire in the dry season, and litter left
by visitors.

### Vocabulary

| Word | Meaning |
|---|---|
| plateau | a high, flat area of land |
| habitat | the natural home of a plant or an animal |
| hermitage | the place where a hermit lives |
| medicinal herb | a plant used as medicine |
| livelihood | the way a person earns a living |
| biodiversity | the variety of living things in a place |

::: note Model answers
**1. Why is Khaptad unusual among Nepal's protected areas?**
Because its centre is a wide, open high-altitude grassland rather than forest
or snow-covered mountain, and that habitat supports a distinctive community of
wild flowers and medicinal herbs.
**2. Give two reasons why protecting the park matters to the people around it.**
It stores the monsoon water that feeds the streams four districts depend on,
and it supports local livelihoods — guiding, portering, homestays and licensed
herb collection.
:::

## 11.3 Grammar and writing tasks of the unit

### Grammar: Relative clauses

A **relative clause** adds information about a noun. It begins with a relative
pronoun — **who** (people), **which** (things), **that** (people or things),
**whose** (possession) — or with **where** (places) and **when** (times).

| Pronoun | Joins | Example |
|---|---|---|
| who | a person | Newton, **who** was born in 1642, … |
| which | a thing | a park **which** lies in the far west |
| that | a person or thing (defining) | the saint **that** lived on the plateau |
| whose | possession | the saint **whose** hermitage is still visited |
| where | a place | the plateau **where** he meditated |
| when | a time | the year **when** the plague closed Cambridge |

The clause sits immediately after the noun it describes. If you can remove it
and the sentence still says what it needs to say, put it between commas: *Newton,
who was born in 1642, studied light.* If removing it destroys the meaning, use
no commas: *The man who discovered calculus was English.*

### Grammar: Articles

| Article | Used before | Example |
|---|---|---|
| a | a singular countable noun beginning with a consonant sound | a park, a university (a *y* sound) |
| an | a singular countable noun beginning with a vowel sound | an hour, an MA, an apple |
| the | something already mentioned, unique, or made specific | the park I visited; the sun; the best answer |
| (no article) | plurals and uncountable nouns used generally | Parks protect wildlife. Water is life. |

The choice depends on the **sound**, not the letter: *an hour* (silent h),
*a university* (sounds like "you"), *an MA* (sounds like "em-ay").

::: caution Common mistakes
- *He is best student in class.* ✗ → *He is **the** best student in **the**
  class.* ✓
- *I saw a elephant.* ✗ → *I saw **an** elephant.* ✓
- *The Mount Everest is the highest peak.* ✗ → *Mount Everest is the highest
  peak.* ✓ (no article before most proper names of mountains, lakes and
  countries)
- Leaving out the relative pronoun: *The man discovered calculus was English.*
  → *The man **who** discovered calculus was English.* ✓
:::

### Writing: A profile and a place description

A **profile** runs in time order and gives the person's dates, the work they
are known for, one difficulty they faced, one thing they were like as a
person, and the effect of their work. A **place description** answers where,
what it is like, what lives there and why it matters — and ends with one
sentence on what should be done to keep it.

::: note Model answers to the practice questions
**Profile of a person you admire.** Paragraph 1: name, dates and where they
were born. Paragraph 2: the work they are known for, with two dates and one
example. Paragraph 3: the difficulty they faced, and one detail that shows
what they were like. Paragraph 4: why their work still matters.
**Description of a place.** Paragraph 1: where it is, and its size or altitude.
Paragraph 2: what it looks like and what lives there. Paragraph 3: why it
matters to the people around it. Paragraph 4: one problem and one thing that
should be done.
:::

## Chapter summary

- A **biography** tells a real person's life in time order and explains the
  connection between its periods.
- Isaac Newton (1642–1727) worked out the binomial theorem, calculus and the
  composition of white light during the plague years of 1665–66, and published
  the *Principia* in 1687.
- The apple story stands for the insight that one force — gravitation — governs
  both a falling apple and the orbit of the Moon.
- A **place description** answers: where, what it is like, what lives there and
  why it matters.
- Khaptad National Park (est. 1984, about 225 km²) is in the far west of Nepal,
  and is famous for its open plateau grassland, wild flowers, medicinal herbs
  and the hermitage of Khaptad Baba.
- **Relative clauses** use *who, which, that, whose, where, when* and sit
  immediately after the noun they describe.
- Use **a/an** by sound, **the** for something specific or unique, and **no
  article** for plurals and uncountable nouns used generally.

## Practice questions

**Reading**

1. Give four events of Newton's life with their years. <span class="marks">[4]</span>
2. Why were the years 1665–66 so important for him? <span class="marks">[2]</span>
3. Where is Khaptad National Park, and when was it established? <span class="marks">[2]</span>
4. Why is the Khaptad plateau unusual in Nepal? <span class="marks">[2]</span>

::: note Answers
**1.** Any four: born 1642; entered Trinity College 1661; plague years 1665–66;
published the *Principia* 1687; President of the Royal Society 1703; knighted
1705; died 1727.
**2.** Sent home from Cambridge by the plague, he worked alone and developed the
binomial theorem, the beginnings of calculus, the theory of colours and the
idea of universal gravitation.
**3.** In the far west of Nepal, in Bajhang, Bajura, Achham and Doti districts
of Sudurpashchim Province; established in 1984.
**4.** Because its centre is a wide, open high-altitude grassland, while most
protected areas in Nepal are forest or high mountain.
:::

**Grammar**

5. Join each pair using a relative pronoun. <span class="marks">[4]</span>
   (a) Newton was an English scientist. He discovered the law of gravitation.
   (b) This is the park. It lies in the far west.
   (c) I met a saint. His hermitage is on the plateau.
   (d) That was the year. The plague closed the university then.

6. Fill in *a, an, the* or nothing. <span class="marks">[5]</span>
   (a) Khaptad is ______ national park. (b) He waited for ______ hour.
   (c) She is ______ best student in ______ class. (d) ______ water is
   necessary for life. (e) I bought ______ umbrella.

::: note Answers
**5.** (a) Newton was an English scientist **who** discovered the law of
gravitation. (b) This is the park **which/that** lies in the far west. (c) I met
a saint **whose** hermitage is on the plateau. (d) That was the year **when**
the plague closed the university.
**6.** (a) a (b) an (c) the / the (d) no article (e) an
:::

**Writing**

7. Write a profile of about 150 words of a person you admire. <span class="marks">[5]</span>
8. Describe a place in Nepal that you have visited, in about 120 words. Say
   where it is, what it is like and why it matters. <span class="marks">[5]</span>

::: note Answers
**7.** Paragraph 1: name, dates, birthplace. Paragraph 2: what they are known
for, with two dates and one example. Paragraph 3: one difficulty they faced and
one personal detail. Paragraph 4: why their work still matters.
**8.** Paragraph 1: location and size or altitude. Paragraph 2: what it looks
like and what lives there. Paragraph 3: why it matters to the people around it.
Paragraph 4: one problem and one thing that should be done about it.
:::

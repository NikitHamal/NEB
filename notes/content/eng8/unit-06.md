---
subject: Compulsory English
grade: 8
unit: 6
title: Traditional Wedding Customs around the World / Life Saving Inventions
hours: 0
area: Units
---

This unit gives you two pieces of **expository writing** — writing whose job is
to explain rather than to tell a story. The first describes wedding customs in
different countries: what people wear, what they eat, what they do, and why.
The second explains a handful of inventions that have saved more lives than any
weapon ever took. Both texts are organised the same way: one paragraph, one
idea, with the general statement first and the examples after it. The grammar of
the unit is about who does the work — the **causative** — and about making a
verb agree with its subject.

::: key What this unit asks of you
By the end you should be able to (1) describe a ceremony using the present
simple and the passive, (2) paraphrase a paragraph without copying it,
(3) use *have / get something done* and *make / let / help somebody do*
correctly, and (4) make a verb agree with its subject even when a phrase sits
between them.
:::

## 6.1 Traditional Wedding Customs around the World

### About the text

The text is a **descriptive and comparative** account of weddings. It does not
say which custom is best; it sets several side by side and explains what each
one means to the people who practise it. Writing like this always answers three
questions about every custom: **what** is done, **why** it is done, and **what
it symbolises**.

### What the text says

A wedding is a ceremony that turns two families into relatives, and almost
every culture marks it three times: with a **promise**, a **feast** and a
**procession**. What changes from country to country is the form.

In Nepal a Hindu wedding is arranged around the **kanyadaan**, the giving away
of the bride, followed by the **saptapadi** — seven steps taken together, each
one a vow; the marriage is complete when the seventh step is taken. The bride
wears red, the colour of good fortune, and the ceremony is fixed by consulting
an astrologer for an auspicious date. In many Nepali communities the groom's
party walks to the bride's house with a *janti*, a procession of relatives,
music and dancing.

In **Japan** a couple may be married at a Shinto shrine before the *kami* gods,
drinking three sips from three cups of sake — nine sips in all — which seals
the bond. In **China** red is the wedding colour; the couple may bow to heaven
and earth, to their parents, and to each other. In **India**, a *mehndi*
ceremony decorates the bride's hands the day before. In **Western** countries
the bride traditionally wears white, something old and something new are worn
for luck, and the couple exchange rings. In several **African** traditions two
families negotiate with gifts and the ceremony joins the two kinship groups as
much as the two people. In **Islamic** weddings a contract (*nikah*) is signed
before witnesses, with the groom promising a *mehr* to the bride.

| Country or culture | Custom | What it means |
|---|---|---|
| Nepal (Hindu) | saptapadi — seven steps | the vows that complete the marriage |
| Japan | nine sips of sake | the bond sealed before the gods |
| China | bowing to heaven, earth and parents | respect to the powers and to family |
| India | mehndi on the bride's hands | blessing and celebration |
| Western | something old, new, borrowed, blue | continuity, hope, friendship, fidelity |
| Islamic | nikah before witnesses | a public, binding contract |

Whatever the form, the same three ideas keep returning: a public promise, a
shared meal, and the joining of two families rather than only two people.

```figure caption="Different forms, the same three parts. A wedding is a promise, a feast and a procession — cultures differ in how they perform the three, not in how many there are."
fig, ax = plt.subplots(figsize=(4.9, 2.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")
cols = [("promise", SERIES[0]), ("feast", SERIES[2]), ("procession", SERIES[3])]
ex = [["kanyadaan", "seven steps", "nikah", "ring exchange"],
      ["janti meal", "wedding cake", "sake", "sweets shared"],
      ["janti", "baraat", "bridal car", "drummers"]]
for i, (name, colour) in enumerate(cols):
    x = 0.6 + i * 3.15
    ax.add_patch(plt.Rectangle((x, 3.5), 2.8, 0.95, fc="white", ec=colour, lw=1.5))
    ax.text(x + 1.4, 3.97, name, ha="center", va="center", fontsize=7.2,
            color=colour, fontweight="bold")
    for j, e in enumerate(ex[i]):
        ax.text(x + 1.4, 2.9 - j * 0.62, e, ha="center", fontsize=6.1, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| custom | a usual way of doing something in a society |
| ceremony | a formal act performed on an important occasion |
| auspicious | believed to bring good luck |
| procession | a line of people moving together on a formal occasion |
| vow | a solemn promise |
| kinship | the relationship of being family |
| fiance | the man a woman has promised to marry |

### Paraphrasing

**Paraphrasing** means saying the same thing in your own words. It is not
copying and changing two words: change the **structure** as well.

> Original: *The marriage is complete when the seventh step is taken.*
> Paraphrase: *Only after the couple has walked the seventh step together are
> they considered married.*

::: note Model answers
**1. What three ideas do all wedding ceremonies share?**
A public promise, a shared meal, and the joining of two families rather than
only two individuals.
**2. Why is the seventh step of the saptapadi important?**
Because it completes the marriage: the first six steps are vows, and the
seventh finishes them, so the couple is married only when all seven have been
taken.
:::

## 6.2 Life Saving Inventions

### About the text

The text is a **cause-and-effect** explanation. It names an invention, explains
the problem it solved, and gives the effect it had on the number of people who
live. It is written mostly in the **passive voice** (*was discovered*, *are
given*, *were prevented*), because the important thing is the invention, not
the person who invented it.

### What the text says

Before the twentieth century, the greatest killer of children was not war but
**water and infection**. A cut could kill; a birth could kill; a sore throat
could kill. Four inventions changed that.

**Vaccination.** Edward Jenner showed in 1796 that a person who had had the mild
cowpox did not catch smallpox; the idea of vaccination grew from there. Smallpox
was declared eradicated in 1980 — the only human disease ever to be wiped out
worldwide. Vaccines now prevent measles, polio, tetanus, diphtheria, whooping
cough and many other diseases.

**Antiseptics.** Ignaz Semmelweis showed in the 1840s that doctors who washed
their hands between patients lost far fewer mothers to childbed fever, and
Joseph Lister used carbolic acid to keep wounds clean in surgery. Simple hand
washing with soap, which we now take for granted, is still one of the cheapest
life savers there is.

**Antibiotics.** Alexander Fleming noticed in 1928 that a mould had killed the
bacteria growing on a plate. Penicillin, mass-produced during the 1940s, turned
pneumonia, blood poisoning and infected wounds from death sentences into
ordinary illnesses.

**Oral rehydration salts (ORS).** Cholera and diarrhoea killed children by
taking the water out of them. The discovery that a simple mixture of salt,
sugar and water can be absorbed even by a badly damaged gut — and that the
mother can mix it at home — has saved tens of millions of lives, mostly of
children under five.

| Invention | Problem it solved | Why it saved so many lives |
|---|---|---|
| Vaccination | epidemic disease | prevents the illness instead of treating it |
| Antiseptics and hand washing | infection in childbirth and surgery | stops infection entering the body |
| Antibiotics | bacterial infection | cures illness that was almost always fatal |
| ORS | dehydration from diarrhoea | cheap, home-made, and usable without a hospital |

The pattern is worth noticing: the inventions that saved most lives were the
**cheap** ones, and the ones that could be taught to ordinary people.

### Vocabulary

| Word | Meaning |
|---|---|
| vaccine | a preparation that makes the body resist a disease |
| eradicated | completely removed from the world |
| antiseptic | a substance that kills germs on the skin or in a wound |
| antibiotic | a medicine that kills bacteria inside the body |
| dehydration | the loss of too much water from the body |
| rehydration | putting that water back |

::: note Model answers
**1. Why is ORS considered one of the greatest life-saving inventions?**
Because it treats the dehydration that actually kills, it costs almost nothing,
it can be mixed at home by a parent, and it works without a doctor or a
hospital — so it reached millions of children who could never have reached a
clinic.
**2. Why is much of this text written in the passive voice?**
Because the subject is the invention and the effect it had, not the inventor;
the passive keeps the reader's attention on what was done, not on who did it.
:::

## 6.3 Grammar and writing tasks of the unit

### Grammar: Causative verbs

A **causative** sentence says that you arranged for somebody else to do the
work. Use **have** or **get** + object + **past participle**.

| Structure | Example | Meaning |
|---|---|---|
| have + object + past participle | I **had my hair cut**. | someone else cut it for me |
| get + object + past participle | She **got the room painted**. | someone else painted it |
| make + somebody + bare verb | The teacher **made us rewrite** it. | we had no choice |
| let + somebody + bare verb | They **let him go** home. | he was allowed |
| help + somebody + (to) verb | She **helped me (to) carry** it. | both verb forms are correct |

::: caution Common mistakes
- *I had cut my hair yesterday.* — that means you cut it yourself. If a barber
  did it: *I **had my hair cut** yesterday.* ✓
- *He made me to sit down.* ✗ — after *make*, *let* and *see* use the bare
  verb: *He made me **sit** down.* ✓
- *She let me to go.* ✗ → *She let me **go**.* ✓
:::

### Grammar: Subject–verb agreement

The verb must agree with its **subject**, not with the nearest noun.

| Rule | Example |
|---|---|
| A phrase between subject and verb changes nothing | The box of sweets **is** on the table. |
| Two subjects joined by *and* take a plural verb | Ram and Sita **are** here. |
| *Each, every, either, neither* are singular | Every one of the boys **has** a book. |
| Uncountable nouns are singular | The water **is** cold. |
| A collective noun may be singular | The team **is** playing well. |

::: example Worked example
**Correct these sentences.** (1) The list of names are on the board. (2) Each of
the students have a copy. (3) He made me to wait. (4) She got her shoes
repair. (5) Neither of the answers are right.

**Answers.** (1) The list of names **is** on the board. (2) Each of the
students **has** a copy. (3) He made me **wait**. (4) She got her shoes
**repaired**. (5) Neither of the answers **is** right.
:::

### Writing: Describing a ceremony

Paragraph 1: what the ceremony is for and when it happens. Paragraph 2: what
happens, in order. Paragraph 3: what each action symbolises. Use the present
simple, and use the passive when the act matters more than the actor (*the
bride **is given** away by her father*).

## Chapter summary

- Expository writing explains; descriptive-comparative writing sets several
  things side by side and explains each one.
- Every wedding custom can be described by answering: what is done, why, and
  what it symbolises.
- Weddings everywhere contain a promise, a feast and a procession.
- Cause-and-effect writing names the problem, the invention and the effect.
- Vaccination, antiseptics, antibiotics and ORS are four inventions that
  together saved more lives than any other group of inventions in history.
- The cheapest life savers reached the most people.
- **Causative:** have / get + object + past participle (*I had my hair cut*).
- **make / let / help** take a bare verb or *to* + verb: *made me sit*, *let me
  go*, *helped me carry*.
- A verb agrees with its subject; a phrase in between does not change it.

## Practice questions

**Reading**

1. Which three things are common to weddings everywhere? <span class="marks">[3]</span>
2. Explain the saptapadi. <span class="marks">[2]</span>
3. Why did the discovery of penicillin change medicine? <span class="marks">[2]</span>
4. What is ORS and why does it work even without a hospital? <span class="marks">[2]</span>

::: note Answers
**1.** A public promise, a shared meal, and the joining of the two families.
**2.** Seven steps taken together by the bride and groom, each step a vow; the
marriage is complete when the seventh is taken.
**3.** It turned diseases that were almost always fatal — pneumonia, blood
poisoning and infected wounds — into ordinary, treatable illnesses.
**4.** Oral rehydration salts: a mixture of salt, sugar and clean water that
replaces the water a child loses through diarrhoea. It works because the gut can
still absorb the mixture even when it is damaged, and a parent can mix it at
home.
:::

**Grammar**

5. Rewrite using the causative. <span class="marks">[4]</span>
   (a) A tailor stitched my shirt. (b) A mechanic repaired our car.
   (c) She is painting the house. (d) A doctor checked my eyes.

6. Choose the correct verb. <span class="marks">[4]</span>
   (a) The bag of apples (is / are) heavy. (b) Each of them (has / have) a pen.
   (c) Neither of the boys (was / were) present. (d) Bread and butter
   (is / are) his breakfast.

::: note Answers
**5.** (a) I had my shirt stitched. (b) We had our car repaired. (c) She is
having the house painted. (d) I had my eyes checked.
**6.** (a) is (b) has (c) was (d) is
:::

**Writing**

7. Describe a festival or ceremony you have taken part in, in about 120
   words. Say what happens in order and what it means. <span class="marks">[5]</span>
8. Write a paragraph of about 80 words explaining one invention that has saved
   lives, with its problem and its effect. <span class="marks">[4]</span>

::: note Answers
**7.** Paragraph 1: name the ceremony and when it falls in the year.
Paragraph 2: what happens, in the order it happens. Paragraph 3: what the main
actions mean. Use the present simple; use the passive where the act matters
more than the actor.
**8.** Name the invention, state the problem it solved in one sentence, then
give its effect on the number of people who die — for example ORS, which treats
the dehydration caused by diarrhoea and can be mixed at home, so it reaches
children who never see a clinic.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** A *custom* is
   (a) a tax at the border only (b) a traditional practice of a community (c) a customer (d) a costume
**2.** *Traditional* is the adjective form of
   (a) trade (b) tradition (c) traditionally (d) trader
**3.** If it ______ tomorrow, the wedding will move indoors.
   (a) rain (b) rains (c) will rain (d) rained
**4.** The invention that saved most lives in the passage sense is best called a
   (a) life-saving invention (b) lifelong invention (c) lively invention (d) living invention
**5.** The opposite of *ancient* is
   (a) antique (b) historic (c) modern (d) old

::: note Objective practice — answers
**1.** (b) — a traditional practice. **2.** (b) — *tradition* → *traditional*. **3.** (b) — type 1 conditional: *if* + present simple. **4.** (a) — life-saving invention. **5.** (c) — modern.
:::

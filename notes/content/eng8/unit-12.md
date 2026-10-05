---
subject: Compulsory English
grade: 8
unit: 12
title: Nepal's Bird Man / Poem: My Teacher Ate my Homework
hours: 0
area: Units
---

A profile of a conservationist and a funny poem: the two texts of this unit
could hardly be more different in tone, and that is the point. One is serious,
factual writing about a person and a cause; the other is a joke in verse. Both,
however, are built on patterns — the profile on the pattern of a life, and the
poem on the pattern of exaggeration and rhyme. The grammar of the unit is the
verb pattern after another verb, and the whole family of questions.

::: key What this unit asks for
By the end you should be able to (1) write a profile of a living person and
explain the value of their work, (2) explain what makes a poem funny —
exaggeration, rhyme and the punch line, (3) use the *-ing* form and the
infinitive correctly after other verbs, and (4) form both yes/no questions and
wh- questions.
:::

## 12.1 Nepal's Bird Man

### About the text

The text is a **profile** — a short biography of a living person, written to
explain what they do rather than to tell their whole life. A profile of a
conservationist must answer four things: what the problem is, what the person
did about it, what has changed as a result, and why it was hard.

### What the text says

A **conservationist** is somebody who works to keep wild species and their
habitats alive. In Nepal one such person has come to be known as **Nepal's Bird
Man**, because he has spent his working life watching, counting and protecting
the country's birds.

The problem is easy to state and hard to solve. Nepal is unusually rich in
birds: more than eight hundred and fifty species have been recorded within its
borders, which is more than one twelfth of all the bird species in the world,
inside a country smaller than one per cent of the earth's land surface. The
country sits on a **migratory flyway**: birds that breed in Siberia and central
Asia fly south across the Himalaya each autumn, rest and feed in Nepal's
wetlands and forests, and return in spring. A country that loses its wetlands
therefore loses not only its own birds but part of a route that crosses half the
planet.

The threats are ordinary and human. **Wetlands are drained and built over**;
forest is cut; rivers are polluted; and — the worst single blow — the veterinary
drug **diclofenac**, given to cattle, poisoned the vultures that fed on the
carcasses, and three species of South Asian vulture fell by more than ninety per
cent within a decade. Nepal banned the veterinary use of the drug in 2006 and
set up *vulture restaurants*, where safe carcasses are left for the birds.

The work of a conservationist is therefore of four kinds: **counting** (a
species cannot be protected until you know how many remain and where they
live); **protecting habitat** (wetlands, forests and grasslands); **working with
people** (because a wetland that a village depends on is protected by the
village, not by a notice board); and **teaching** (school bird clubs, village
awareness, and getting birds into the school curriculum, which is how a
generation changes its habits).

The results are measurable. Several vulture species have begun to recover at
the safe feeding sites; wetland sites such as **Koshi Tappu** and **Ghodaghodi**
are Ramsar sites; and bird tourism brings visitors and income to places that had
none. What the profile shows is that conservation is not sentiment. It is
counting, law, agriculture, education and patience.

| Problem | Cause | What helps |
|---|---|---|
| Wetlands drained | building, encroachment, silt | Ramsar protection, community management |
| Vultures dying | diclofenac in cattle carcasses | ban on the drug, safe feeding sites |
| Birds caught for trade | demand for cage birds | enforcement, awareness in schools |
| Habitat cut | firewood, timber, grazing | community forests, alternative fuel |

```figure caption="Why counting comes first. Until the number of birds and the places they use are known, protection cannot be aimed at anything, and nobody can tell whether it has worked."
fig, ax = plt.subplots(figsize=(4.9, 2.3))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.0); ax.axis("off")
chain = [("count", SERIES[0]), ("map habitat", SERIES[1]),
         ("protect with people", SERIES[2]), ("teach", SERIES[3]),
         ("count again", ACCENT)]
for i, (name, colour) in enumerate(chain):
    x = 0.25 + i * 1.98
    ax.add_patch(plt.Rectangle((x, 2.5), 1.72, 1.1, fc="white", ec=colour, lw=1.4))
    ax.text(x + 0.86, 3.05, name, ha="center", va="center", fontsize=6.2, color=INK)
    if i < len(chain) - 1:
        ax.annotate("", xy=(x + 1.98, 3.05), xytext=(x + 1.7, 3.05),
                    arrowprops=dict(arrowstyle="->", color=GRID, lw=1.3))
ax.text(5.0, 1.6, "the loop is the point: a count proves whether the work succeeded",
        ha="center", fontsize=6.2, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| conservationist | a person who works to protect nature |
| species | a group of living things that can breed together |
| flyway | a route that migrating birds follow year after year |
| wetland | marshy ground, lake or riverbank where water birds feed |
| carcass | the dead body of an animal |
| Ramsar site | a wetland protected under an international agreement |
| encroachment | the illegal taking over of land |

::: note Model answers
**1. Why does a country that loses its wetlands lose more than its own birds?**
Because Nepal lies on a migratory route: birds that breed far to the north rest
and feed in Nepal's wetlands on their way south and north again. Destroying the
wetland breaks a link in a route that crosses much of Asia.
**2. Why is counting the first task of a conservationist?**
Because you cannot protect what you have not measured: a count tells you how
many remain, where they are and whether the number is falling, and it is the
only way to prove later that the protection worked.
:::

## 12.2 Poem: My Teacher Ate my Homework

### About the poem

The poem is **humorous verse**. Its speaker is a schoolchild who explains that
the homework is missing because the teacher ate it — and then keeps inventing
more and more impossible explanations. It is funny for three reasons, and all
three are worth naming in an answer: **exaggeration**, **rhyme** and the
**punch line**.

**Exaggeration** (also called hyperbole) means describing something as far
bigger, stranger or worse than it is. A dog eating homework is almost possible;
a teacher frying it with toast is not, and the poem keeps pushing the idea until
it collapses. **Rhyme** makes the joke land: the paired lines fall into place
with a click, and the reader starts to expect the next rhyme, which the poet
then uses to surprise them. The **punch line** is the last line or two, where the
absurdity is admitted or turned around.

| Device | What it does | What to say about it |
|---|---|---|
| exaggeration | makes the excuse absurd | "the effect is comedy, not information" |
| rhyme | makes the lines memorable and predictable | "the rhyme sets up an expectation the poet then breaks" |
| repetition | the excuses pile up | "each excuse is bigger than the last" |
| the punch line | turns the joke | "the last lines admit the real reason" |
| childish words | the voice sounds like a child | "the register shows who is speaking" |

::: note Model answers
**1. What is the theme of the poem?**
The poem is not really about homework. It is about the excuses children invent,
and about the way a small lie grows when it is fed — which is why the excuse
gets bigger with every line until it is impossible.
**2. Who is the speaker, and how do you know?**
A schoolchild, because of the vocabulary and the point of view — the poem is
told by the person who has failed to do the work, and it sounds like speech
rather than like writing.
:::

## 12.3 Grammar and writing tasks of the unit

### Grammar: Verb + -ing and verb + infinitive

Some verbs are followed by the **-ing** form, some by **to + verb**, and a few
take either.

| Pattern | Verbs | Example |
|---|---|---|
| verb + -ing | enjoy, finish, mind, keep, stop, suggest, avoid, practise | I **enjoy watching** birds. |
| verb + to + verb | want, need, decide, hope, plan, try, promise, forget, learn | She **decided to join** the club. |
| verb + object + to + verb | ask, tell, want, advise, allow, encourage | They **asked us to help**. |
| bare verb after make, let, see, hear | make, let, see, hear, watch | He **made me wait**; she **let me go**. |
| either form, same meaning | begin, start, continue, like, love, hate | I **like watching** / **like to watch** birds. |
| either form, different meaning | stop, remember, forget | He **stopped watching** (he no longer watched) / He **stopped to watch** (he paused in order to watch). |

### Grammar: Questions — yes/no and wh-

| Type | How it is made | Example |
|---|---|---|
| Yes/no | helping verb + subject + verb | **Do** you like birds? |
| Wh- | question word + helping verb + subject + verb | **Where do** you watch birds? |
| Subject question | question word + verb (no helping verb) | **Who wrote** the poem? |
| Question with a preposition | preposition usually at the end | **What** are you looking **at**? |

The question words are *who, whom, whose, what, which, when, where, why, how*,
and the compounds *how many, how much, how long, how far, how often*.

::: caution Common mistakes
- *Who did write the poem?* ✗ when *who* is the subject → *Who **wrote** the
  poem?* ✓
- *I enjoy to watch birds.* ✗ → *I enjoy **watching** birds.* ✓
- *She suggested to go early.* ✗ → *She suggested **going** early.* ✓
- *Did you went there?* ✗ → *Did you **go** there?* ✓
:::

### Writing: An essay on hobbies and interests

Shape: paragraph 1 names the hobby and says when it began; paragraph 2 explains
what you actually do, with one specific detail; paragraph 3 says what it has
taught you; paragraph 4 invites the reader to try it. Use *enjoy, love, like,
prefer, spend time, practise* — and remember that *enjoy* and *practise* take
the *-ing* form.

::: note Model answers to the practice questions
**Essay on a hobby.** "I began birdwatching two years ago, when a teacher lent
me a pair of binoculars. Every Saturday morning I walk to the riverbank with my
cousin and write down what we see: a white-throated kingfisher on the wire, egrets
in the shallow water, sometimes a flock of ducks in winter. Keeping the list has
taught me patience and taught me to notice. It costs nothing, and I recommend
it."
:::

## Chapter summary

- A **profile** explains what a living person does: the problem, the work, the
  result and the difficulty.
- Conservation is counting, protecting habitat, working with people and
  teaching — not only sentiment.
- Nepal has recorded more than 850 bird species and lies on a migratory flyway,
  so its wetlands matter far beyond its borders.
- The veterinary drug **diclofenac** caused a collapse in South Asian vultures;
  the ban in 2006 and the safe feeding sites are the remedy.
- Humorous verse works by exaggeration, rhyme and a punch line.
- **enjoy, finish, mind, avoid, practise, suggest** take the **-ing** form.
- **want, decide, hope, plan, try, promise, learn** take **to + verb**.
- **make, let, see, hear, watch** take the bare verb.
- Subject questions (*Who wrote…?*) take no helping verb.

## Practice questions

**Reading**

1. What is a flyway, and why does it make Nepal important for birds? <span class="marks">[3]</span>
2. What happened to South Asian vultures, and why? <span class="marks">[2]</span>
3. What four kinds of work does a conservationist do? <span class="marks">[4]</span>
4. Give two reasons why the poem is funny. <span class="marks">[2]</span>

::: note Answers
**1.** A flyway is a route that migrating birds follow year after year. Nepal
lies across one, so its wetlands and forests are feeding and resting places for
birds that breed far to the north — losing them breaks a link in a route that
crosses much of Asia.
**2.** Three South Asian vulture species fell by more than ninety per cent in a
decade because they ate cattle carcasses containing the veterinary drug
diclofenac, which caused kidney failure.
**3.** Counting, protecting habitat, working with local people, and teaching.
**4.** Exaggeration (the excuse becomes impossible) and rhyme (the paired lines
make the joke land), helped by the punch line at the end.
:::

**Grammar**

5. Choose the correct form. <span class="marks">[5]</span>
   (a) I enjoy (to watch / watching) birds.
   (b) She decided (joining / to join) the club.
   (c) He made me (to wait / wait) outside.
   (d) They stopped (to buy / buying) petrol — the car had broken down.
   (e) Do you mind (to close / closing) the window?

6. Make questions for these answers. <span class="marks">[4]</span>
   (a) "Ramesh wrote it." (b) "I live in Dhangadhi." (c) "I go there twice a
   week." (d) "I am looking at that heron."

::: note Answers
**5.** (a) watching (b) to join (c) wait (d) to buy (e) closing
**6.** (a) Who wrote it? (b) Where do you live? (c) How often do you go there?
(d) What are you looking at?
:::

**Writing**

7. Write an essay of about 150 words on a hobby you enjoy. <span class="marks">[5]</span>
8. Write a paragraph of about 80 words on why some birds are in danger in
   Nepal, and what can be done. <span class="marks">[4]</span>

::: note Answers
**7.** Paragraph 1: the hobby and when it started. Paragraph 2: exactly what
you do, with one specific detail. Paragraph 3: what it has taught you.
Paragraph 4: why you recommend it. Use *enjoy / like + -ing*.
**8.** Name the dangers — wetlands drained and built over, forest cut, rivers
polluted, birds caught for the cage-bird trade — and match each with an action:
Ramsar protection, community forests, enforcement, school bird clubs.
:::

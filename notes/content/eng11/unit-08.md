---
subject: Compulsory English
grade: 11
unit: 8
title: Corona Says
hours: 3
area: Literature — Poems
---

"Corona Says" is a short poem written by the Nepali writer Vishnu S. Rai during
the COVID-19 pandemic of 2020. Its trick is simple and powerful: the virus itself
is given a voice. Instead of a human complaining about a disease, a disease
complains about human beings. By the end of the poem the reader is no longer sure
which of the two is the real infection of the earth.

::: key What the exam wants from this poem
Examiners ask three things again and again: **who is the speaker** (the
coronavirus, not the poet), **what charges the speaker brings against
humankind**, and **why the poem is called a satire**. Learn the list of human
crimes the virus names, and learn to say in one sentence that the poem turns the
accusation around — the accused becomes the accuser.
:::

## 8.1 About the poet

Vishnu S. Rai is a contemporary Nepali writer, translator and linguist who writes
in both Nepali and English. For many years he taught English Education at
Tribhuvan University in Kathmandu, and he has been an active figure in NELTA
(the Nepal English Language Teachers' Association), for whose journal he has
written and edited. His published work spans several kinds of writing: poems and
short stories in English, translations between Nepali and English, and academic
books on language, linguistics and English language teaching. He is also known as
a collector and reteller of Nepali folk material.

Rai does not belong to a formal literary "movement". He is best placed in the
generation of Nepali writers who, from the late twentieth century onwards, chose
to write creatively in English about Nepali and global subjects, so that Nepali
experience could reach readers beyond South Asia. His manner is plain, ironic and
conversational — everyday words, short lines, no ornament — and his subjects are
usually social: power, hypocrisy, and the gap between what people say and what
they do. "Corona Says" is a pandemic poem, written while the whole world was shut
indoors in 2020, and it belongs to the large body of literature that the pandemic
produced almost overnight.

## 8.2 Summary

The poem is a **dramatic monologue**: one speaker talks, and we understand the
silent listener only from what the speaker says. The speaker is the coronavirus.
The listener is the whole human race. The poem moves through four clear stages,
which are best studied one at a time.

### Movement 1 — The virus admits it is hated

The virus begins by acknowledging what human beings feel about it. It knows that
people hate it, fear it and want it dead, and that they call it a killer. It does
not argue with this. It accepts, calmly, that it has caused death and that the
world is frightened of it. This quiet, reasonable opening is important: the
speaker sounds not like a monster but like someone willing to discuss the charge.

### Movement 2 — The virus turns the accusation round

Having accepted the charge, the virus asks who the greater killer really is. It
reminds human beings of what they have done to the earth long before any virus
arrived: forests cut down, rivers and air poisoned, other living creatures
hunted, caged and killed for pleasure or profit, and wars in which human beings
destroyed their own kind in millions. The point the virus makes is one of
proportion. Whatever harm a virus has done in a few months, humankind has done
far more, for far longer, and on purpose. A virus kills because that is its
nature; people destroy while knowing exactly what they are doing.

### Movement 3 — The virus as a teacher of equality

The virus then describes its own most uncomfortable quality: it makes no
distinctions. It does not ask whether a body is rich or poor, powerful or
powerless, of one religion or another, of one colour or another, from a rich
country or a poor one. Money, weapons, armies and titles are of no use against
it. In a world organised around exactly such differences, this is presented as a
kind of grim lesson: the virus has shown human beings the equality they preach
but never practise.

### Movement 4 — The earth breathes, and the warning

Finally the virus points to what happened while human beings stayed shut in their
houses. Factories and vehicles stopped; the air cleared; rivers ran cleaner; birds
and animals were heard and seen in places from which people had driven them away.
The planet, in other words, recovered a little the moment human activity paused —
which quietly proves the virus's case about who the real destroyer is. The poem
closes on a conditional note rather than a triumphant one: the virus will pass,
as such things do, but whether human beings have actually learnt anything is left
as an open question addressed to the reader.

```figure caption="How the monologue builds its case. Each stage leads to the next, and the final stage sends the reader back to re-judge the first."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.7,4.6))
steps = [
 ("1. The charge", "\"You hate me, you call me\na killer.\"  The virus accepts it."),
 ("2. The counter-charge", "Forests felled, water and air\npoisoned, animals killed, wars\nfought — and all of it chosen."),
 ("3. The lesson", "The virus asks no one's wealth,\nrace, religion or rank.\nIt is the only true equaliser."),
 ("4. The proof", "People stopped; the sky cleared,\nrivers ran clean, birds returned.\nSo who was harming the earth?"),
]
cols = [MUTED, "#A8271F", ACCENT, "#0B6A62"]
y = 0.990; h = 0.220; gap = 0.033
for (title, body), c in zip(steps, cols):
    ax.add_patch(FancyBboxPatch((0.045, y-h), 0.91, h,
        boxstyle="round,pad=0.008,rounding_size=0.02",
        fc="white", ec=c, lw=1.5, transform=ax.transAxes, zorder=2))
    ax.text(0.075, y-0.045, title, transform=ax.transAxes, fontsize=9.6,
            color=c, fontweight="bold", va="center", zorder=3)
    ax.text(0.075, y-0.080, body, transform=ax.transAxes, fontsize=8.3,
            color=INK, va="top", zorder=3, linespacing=1.40)
    if y - h - gap > 0.02:
        ax.annotate("", xy=(0.5, y-h-gap+0.004), xytext=(0.5, y-h-0.004),
                    xycoords=ax.transAxes, textcoords=ax.transAxes,
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3,
                                    mutation_scale=11))
    y = y - h - gap
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
```

## 8.3 Themes

**Human destruction of nature.** This is the poem's central subject. The virus's
list of human crimes is all environmental: trees, water, air, animals. The poem
argues that the pandemic is not an accident that fell on an innocent world but a
symptom of the way human beings have been treating the planet.

**Who is the real killer?** The poem is built on a reversal. We open the poem
sure that the virus is the villain, and close it wondering about ourselves. The
question is left with the reader deliberately.

**Death as the great equaliser.** The virus is indifferent to wealth, caste,
colour, religion and nationality. For a world in which those differences decide
everything, this indifference is frightening — and instructive.

**Human arrogance.** People believed that money, science, armies and borders made
them masters of the earth. A microscopic organism that cannot even be seen
showed how thin that mastery was.

**Nature's power to heal itself.** The clearing skies and returning birds of 2020
show that the damage is not yet beyond repair, provided human pressure is
reduced. This is the one hopeful note in the poem.

**Satire and self-examination.** The poem does not preach directly. It hands the
microphone to the enemy and lets the enemy's calm voice do the accusing, which
makes the criticism much harder to shrug off.

## 8.4 Form, structure and rhyme

**Form.** "Corona Says" is written in **free verse** — verse with no fixed metre
and no rhyme scheme. The lines are short and of unequal length, and they break
where a speaking voice would pause, not where a metrical pattern would end. If
you are asked for the rhyme scheme, the correct answer is that the poem has
**none**: there is no ABAB or AABB pattern to write out, because the poet has
deliberately given it up.

**Why free verse suits this poem.** A regular metre would make the virus sound
like a song or a hymn. Free verse makes it sound like someone talking to you
across a table — patient, matter-of-fact, unhurried. The plainness is the point.
The poet also avoids grand poetic vocabulary, so that the horror in the content
(forests, wars, dead bodies) is left to speak for itself.

**Structure.** The poem is a **dramatic monologue**, and its structure is the
structure of an argument, not of a story: charge accepted, counter-charge made,
evidence given, conclusion left open. The "you" addressed throughout is the
reader, which is what gives the poem its uncomfortable force — we are not
watching an accusation, we are receiving one.

**Voice and device.** Giving speech, reasoning and feeling to a virus is
**personification** used as the frame of the whole poem, not as a decoration in
one line. Everything else in the poem depends on it.

::: caution A very common mistake
Do not write that "the poet says he hates human beings" or that "the poet
describes the coronavirus". Neither is true. The **poet does not speak at all**.
The speaker is the virus, and the poet's opinion reaches us only indirectly,
through what he makes the virus say. Confusing poet with speaker loses marks in
almost every literature paper.
:::

## 8.5 Poetic devices

Because the poem is modern and in copyright, the table below names each device
and the place in the poem where it works, rather than reprinting the lines.

| Device | Where it appears | Effect |
|---|---|---|
| Personification | the virus speaks as "I" and reasons like a person | Makes the whole poem possible; an enemy is allowed to state its case |
| Apostrophe (direct address) | the repeated "you" aimed at humankind | The reader is put in the dock; the criticism becomes personal |
| Irony | a killer disease lecturing us on killing | Exposes human hypocrisy far better than direct preaching |
| Metaphor | humankind pictured as the true disease of the earth | Reverses villain and victim in a single stroke |
| Imagery (visual) | cleared skies, clean rivers, animals moving freely in empty streets | Turns an argument into something the reader can see |
| Imagery (of violence) | felled forests, poisoned water, caged and slaughtered animals, war dead | Piles up evidence so that the counter-charge feels proved |
| Symbolism | the virus stands for nature's revenge and for a warning | Lifts the poem above one disease in one year |
| Hyperbole | the sweeping claim that human beings have destroyed everything they touch | The exaggeration is emotional, not factual; it conveys anger |
| Repetition / anaphora | the clauses of accusation stacked one on another | Creates the rhythm of a courtroom charge-sheet |
| Enjambment | the short lines running on without punctuation | Keeps the speaking voice moving and refuses a singsong effect |
| Alliteration | the poem's clusters of repeated opening consonants | Small musical touches inside an otherwise plain style |
| Satire | the poem as a whole | Uses ridicule of human behaviour to demand a change in it |

## 8.6 Glossary

| Word | Meaning |
|---|---|
| corona | crown; the coronavirus is so named because of the crown-like spikes on its surface |
| pandemic | a disease outbreak spread over many countries at the same time |
| epidemic | a disease outbreak confined to one area or population |
| virus | a microscopic agent that can reproduce only inside the living cells of another organism |
| monologue | a long speech by one person |
| dramatic monologue | a poem in which an invented speaker, not the poet, addresses a silent listener |
| free verse | poetry without regular metre or rhyme |
| personification | giving human qualities, speech or feeling to a thing, animal or idea |
| apostrophe | a direct address to an absent person, a group, or an abstract thing |
| satire | writing that attacks folly or wrongdoing through ridicule |
| irony | a gap between what is said or expected and what is actually the case |
| hypocrisy | claiming to hold standards that one's own behaviour does not follow |
| lockdown | an official order confining people to their homes |
| quarantine | keeping a person apart from others to stop infection spreading |
| deforestation | the clearing away of forests |
| pollution | the poisoning of air, water or land by harmful substances |
| equaliser | something that removes differences of rank or wealth |
| arrogance | an exaggerated sense of one's own importance or power |
| indifferent | showing no preference or concern either way |
| revenge | harm done in return for harm received |

## Chapter summary

- "Corona Says" by Vishnu S. Rai is a **dramatic monologue in free verse** in
  which the **coronavirus** speaks to the whole human race.
- Its four movements are: the virus accepts that it is hated; it accuses human
  beings of far greater destruction; it points out that it alone treats all
  people equally; and it shows that nature began to heal the moment people
  stopped.
- Central themes: destruction of the environment, human arrogance and hypocrisy,
  death as an equaliser, nature's capacity to recover, and the reversal of
  villain and victim.
- There is **no rhyme scheme and no metre** — the plain speaking voice of free
  verse is chosen on purpose.
- The governing device is **personification**; the governing mode is **satire**;
  the governing effect is **irony**.
- The poet never speaks in his own voice. Never confuse the poet with the
  speaker.

## Practice questions

**Short answer questions (2 marks each)**

1. Who is the speaker in "Corona Says", and who is being addressed? <span class="marks">[2]</span>
2. What charges does the virus bring against human beings? <span class="marks">[2]</span>
3. In what sense is the coronavirus called an equaliser in the poem? <span class="marks">[2]</span>
4. What changes in nature does the speaker point to as evidence for its argument? <span class="marks">[2]</span>
5. Why has the poet chosen free verse instead of a regular metre? <span class="marks">[2]</span>
6. What is a dramatic monologue? Show how "Corona Says" fits the definition. <span class="marks">[2]</span>
7. Explain the irony on which the poem depends. <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** The speaker is the coronavirus itself, given a human voice by the poet. It
addresses the whole human race — the repeated "you" of the poem. The poet himself
never speaks directly; his opinion reaches us only through what the virus says.

**2.** The virus accuses human beings of cutting down forests, poisoning rivers
and the air, hunting, caging and killing other creatures, and destroying millions
of their own kind in wars. Its point is that all this damage was deliberate,
long-lasting and far greater than the harm a virus can do.

**3.** The virus does not ask whether the body it enters is rich or poor, of
which country, colour, caste or religion, or how powerful its owner is. Wealth,
weapons and rank give no protection. In a world divided by exactly these
differences, the virus treats everybody the same, and so becomes an equaliser.

**4.** During the lockdown the air became clear, the rivers ran cleaner, and
birds and wild animals reappeared in places from which people had driven them.
The earth recovered as soon as human activity stopped, which supports the virus's
claim that human beings, not viruses, are the planet's real problem.

**5.** Free verse has no fixed metre or rhyme, so the poem sounds like ordinary
speech rather than a song. That plain, calm, conversational voice makes the
virus's accusation sound reasonable, and keeps the reader's attention on the
terrible content instead of on pretty sound patterns.

**6.** A dramatic monologue is a poem in which an invented speaker, who is not
the poet, talks at length to a silent listener whose presence we infer from the
speech. In "Corona Says" the invented speaker is the virus, the silent listener
is humankind, and we learn what humankind feels ("you hate me") only from the
virus's words.

**7.** The irony is that a deadly disease takes the moral high ground and lectures
human beings about killing. The accused becomes the accuser, and the creature we
call a killer proves that we kill more. The gap between our view of ourselves as
civilised and the evidence the virus produces is the poem's irony.
:::

**Long answer questions (5 marks each)**

1. "Corona Says" reverses the roles of villain and victim. Discuss. <span class="marks">[5]</span>
2. Discuss "Corona Says" as a satire on modern human civilisation. <span class="marks">[5]</span>
3. Examine the form and language of "Corona Says" and show how they serve its
   meaning. <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** The poem begins where the reader already stands: the virus is the killer,
human beings are its victims, and the speaker openly admits that it is hated and
wished dead. Having accepted that charge, it immediately reverses it. It asks who
has done more killing, and answers with a list of human acts — forests cut down,
rivers and air poisoned, animals hunted and caged, wars in which millions of
human beings destroyed one another. The comparison is one of scale and of
intention: a virus spreads because that is its nature, while people destroy
knowing exactly what they do. The reversal is then confirmed by evidence from the
lockdown. When human activity stopped, the sky cleared, the water cleaned itself
and animals returned to the streets — so the planet was healthier without us than
with us. By the end, the word "virus" has changed owners: the true infection of
the earth is humankind, and the disease is merely a symptom. Because the
accusation comes from the enemy's own mouth and not from the poet's, the reader
cannot dismiss it as preaching, and has to sit with the discomfort.

**2.** Satire attacks human folly and wrongdoing by holding it up to ridicule,
and that is precisely what this poem does. Its satirical method is to give the
speech to the coronavirus, so that human behaviour is described from outside by
somebody with no reason to flatter us. The targets are exact. First, our
hypocrisy: we call the virus a murderer while conducting wars and slaughtering
other species. Second, our arrogance: we believed money, technology, armies and
borders had made us masters of the earth, and an organism too small to see
undid that belief in weeks. Third, our inequality: we announce that all human
beings are equal and then organise the world by wealth, colour, religion and
nationality, and it takes a disease — which asks none of those questions — to
treat us all alike. Fourth, our carelessness towards nature, proved by how
quickly the earth improved without us. The tone is not shrill; the virus is calm,
patient and almost polite, and this restraint sharpens the attack. The poem ends
not with a punishment but with a question about whether we have learnt anything,
which is satire's real aim: not to wound but to correct.

**3.** The poem is written in free verse: the lines are short, of unequal length,
and there is no metre and no rhyme scheme at all. This is a deliberate choice. A
regular pattern would have made the virus sound like a chant or a hymn, whereas
free verse makes it sound like a person speaking quietly and reasonably to
someone across a table, which is far more unsettling. The vocabulary matches the
form: ordinary, unornamented words, so that the frightening content — felled
forests, poisoned water, war dead — is allowed to do the work without help from
grand poetic language. Structurally the poem is an argument rather than a story:
the charge is accepted, a counter-charge is made, evidence is produced, and the
conclusion is handed to the reader. Two devices hold everything together.
**Personification** frames the whole poem, since without a speaking virus there
is no poem at all. **Apostrophe** — the insistent "you" — keeps the reader inside
the poem as the accused rather than outside it as an observer. Enjambment lets
the short lines run on so the voice never falls into singsong, and the stacked
clauses of accusation give the passage the rhythm of a charge-sheet being read
out in court. Form, language and meaning are therefore inseparable: a poem about
stripping away human pretence is itself stripped of poetic decoration.
:::

**Reference to the context**

1. The speaker tells human beings that it does not ask whether a body belongs to
   a rich person or a poor one, to one religion or another, before it enters.
   (a) Who is the speaker? (b) What quality of the speaker is being described
   here? (c) What comment on human society does this make? <span class="marks">[5]</span>
2. The speaker points out that while people remained shut inside their houses,
   the sky grew clear, the rivers ran clean, and the birds and animals came back.
   (a) Which period is being described? (b) Why does the speaker mention these
   changes? (c) What does the passage suggest about the relation between human
   beings and nature? <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) The speaker is the coronavirus, which the poet has personified and
allowed to address humankind throughout the poem.
(b) It describes the virus's complete **indifference to human distinctions**. It
infects anyone, and wealth, power, caste, colour, nationality and religion give
no protection. This is why the poem presents it as the one true equaliser.
(c) The comment is a bitter one about human hypocrisy. Human society claims that
all people are equal, yet it is organised by exactly the differences the virus
ignores. It has taken a disease to give human beings the equality their own
declarations promise but their behaviour denies. The lines therefore work as
satire: the virus is not boasting, it is exposing us.

**2.** (a) The passage describes the COVID-19 lockdown of 2020, when factories,
vehicles and daily movement stopped almost everywhere in the world.
(b) The speaker mentions these changes as **evidence** in its argument. Having
claimed that human beings, not viruses, are the earth's real destroyers, it
points to what happened the moment human activity paused: the proof of the claim
is that the planet immediately began to recover.
(c) The passage suggests that the relationship has become one-sided and harmful —
nature does not need human beings, but suffers from them, and is able to heal
itself quickly if the pressure is lifted. It carries one hopeful implication: the
damage is not yet beyond repair. Whether people will choose to reduce that
pressure after the pandemic is the open question on which the poem ends.
:::

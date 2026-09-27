---
subject: Compulsory English
grade: 11
unit: 13
title: Sharing Tradition
hours: 3
area: Literature — Essays
---

Frank LaPena was a Native American artist, dancer and teacher, and this essay is
his attempt to explain something outsiders almost always get wrong: what a
tradition actually is. It is not a set of old objects or a list of customs
recorded in a book. It is a living relationship between people, their ancestors
and the land, and it survives only for as long as somebody keeps doing it — and
passing it on.

::: key What the exam wants from this essay
Be able to state LaPena's thesis in one sentence: **tradition is a living
practice, and knowledge of it carries the responsibility to share it.** Then know
his four supports for that claim — the role of elders, the place of ceremony,
the traditional artist, and the difference between living tradition and museum
display.
:::

## 13.1 About the author

Frank LaPena (1937–2019) was an American artist, poet, dancer, ceremonial leader
and university teacher of Nomtipom Wintu descent — the Wintu are an indigenous
people of northern California, in the Sacramento River valley. He was born in San
Francisco, was sent as a child to government boarding schools of the kind that
were designed to separate Native children from their own languages and customs,
and came back to his people's traditions as a young man.

He studied art and anthropology, and for many years taught at California State
University, Sacramento, where he directed the Native American Studies programme
and became Professor Emeritus of Art. He was a painter whose work was widely
exhibited, a published poet, and — just as importantly for this essay — an active
participant in the dance and ceremonial life of his community. His books include
*The World Is a Gift* (2004), a collection of his poems, essays and paintings.

LaPena therefore writes from two positions at once: as a scholar who knows how
outsiders study Native cultures, and as an insider who has taken part in the
ceremonies being studied. "Sharing Tradition" comes out of that double position,
and much of its quiet force comes from it.

## 13.2 Summary

### What makes a person "traditional"

LaPena begins with a question rather than a definition. Who counts as a
traditional person? Not, he argues, whoever knows the most facts about the old
ways, and certainly not whoever owns the most old objects. A traditional person is
someone who **lives** the tradition: who takes part in the ceremonies, keeps the
obligations, behaves in the way the community expects, and accepts the discipline
that goes with all this. Tradition, in his account, is something you do, not
something you have.

### How tradition is learnt

It is learnt from the elders, and it is learnt slowly. The old people do not hand
over information in lessons; they teach by example, by letting a young person be
present, by giving small tasks, and by telling stories whose meaning may not be
clear for years. Much of what matters is passed on **orally** — in songs, names,
prayers and accounts of what happened long ago — and much of it is learnt through
the body, by dancing and by doing, rather than through the head.

This also means that knowledge is **earned**. A learner has to show patience,
respect and steadiness before more is given. Some knowledge is sacred and is not
given to everybody at all; certain songs and names belong to particular families
or to particular ceremonial roles. To LaPena, this is not secrecy for its own
sake. It is the recognition that some things are powerful and can be damaged by
careless handling.

### Ceremony, art and the world

Ceremony is the heart of the essay. Dances and songs are not entertainment and
not performances put on for an audience; they are work that has to be done, and
their purpose is to keep the relationship between the people and the natural
world in good order — to renew the world, to give thanks, to mark the seasons and
the passages of a life.

This changes what "art" means. The traditional artist does not make objects to be
admired in a gallery or sold to collectors. Regalia, baskets, feathers, paint and
song are made for use, and they carry obligations: how they are made, who may make
them, what may be done with them afterwards. An object taken out of that setting,
put behind glass and labelled, is no longer the thing it was. It has become
information about a tradition rather than a part of one.

LaPena is direct about what follows. When outsiders — anthropologists, collectors,
tourists, businesses — take songs, designs and ceremonies out of their community
and use them for study, decoration or profit, they are not preserving a culture.
They are removing the living part and keeping the shell.

### Tradition is not frozen

A common misunderstanding, he says, is that a tradition must stay exactly as it
was or it is not "authentic". Living traditions have always changed: new materials
are used, new songs are received, practices are adapted to the circumstances of
each generation. What has to stay constant is not the outward detail but the
relationship — the respect, the purpose and the connection to the ancestors and to
the land. A tradition that cannot change is already a museum piece.

### Sharing as responsibility

The essay closes on the idea in its title. Because tradition exists only in its
practice, each generation holds it in trust rather than owning it. Receiving
knowledge from the elders therefore creates a debt, and the debt is paid forward,
not back: the receiver is obliged to live the tradition properly and to give it to
those who come after. Sharing, in LaPena's sense, is not the same as making
everything public. It means teaching the right things to the right people at the
right time, which is the only way a tradition can survive.

```figure caption="Tradition as LaPena describes it: a circle held in trust. Each generation receives, practises, and hands on."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.4))
labels = ["the elders", "ceremony,\nsong and dance", "the learner\ntakes part",
          "knowledge is\nearned, not taken", "the duty to\npass it on"]
n = 5
ang = np.deg2rad(90 - np.arange(n)*360/n)
R = 1.0
xs, ys = R*np.cos(ang), R*np.sin(ang)
for i in range(n):
    j = (i+1) % n
    ax.annotate("", xy=(xs[j]*0.88, ys[j]*0.88), xytext=(xs[i]*0.88, ys[i]*0.88),
                arrowprops=dict(arrowstyle="-|>", color=GRID, lw=2.4,
                                connectionstyle="arc3,rad=-0.22",
                                shrinkA=13, shrinkB=13, mutation_scale=13))
for i in range(n):
    ax.plot([xs[i]],[ys[i]], "o", color=ACCENT, ms=13, zorder=3)
    ax.text(xs[i], ys[i], str(i+1), ha="center", va="center", color="white",
            fontsize=7.6, fontweight="bold", zorder=4)
    rx, ry = xs[i]*1.22, ys[i]*1.28
    ha = "left" if rx > 0.15 else ("right" if rx < -0.15 else "center")
    va = "bottom" if ry > 0.4 else ("top" if ry < -0.4 else "center")
    ax.text(rx, ry, labels[i], ha=ha, va=va, fontsize=8.3, color=INK,
            linespacing=1.4)
ax.text(0, 0, "held in trust,\nnot owned", ha="center", va="center",
        fontsize=8.4, color=MUTED, style="italic", linespacing=1.45)
ax.set_xlim(-2.45, 2.45); ax.set_ylim(-1.75, 1.75)
ax.set_aspect("equal"); ax.axis("off")
```

## 13.3 The central argument

**The thesis.** Tradition is not a body of knowledge or a collection of objects
but a living practice; it belongs to a community rather than to an individual;
and anyone who receives it takes on the responsibility of living it properly and
handing it on.

**How the argument is built.** LaPena does not argue like a debater. He builds by
accumulation, laying one observation beside another until the conclusion is
already obvious by the time he states it.

1. **He redefines the key term.** By asking what makes a person traditional, he
   moves "tradition" from the category of *things known* to the category of
   *things done*. Everything else follows from this move.
2. **He shows how the knowledge travels.** Because tradition is learnt from
   elders, orally, slowly and by participation, it cannot be separated from the
   people who carry it. A song written down is not the same as a song sung.
3. **He redefines art in the same way.** Ceremonial objects are made for use, and
   their meaning lies in that use. This supplies the sharpest evidence for the
   thesis: take the object out of the practice and you are left holding something
   that looks the same and is not the same.
4. **He removes the obvious objection.** If tradition is alive, must it never
   change? No — living things change. What must not change is the relationship
   behind the practice.
5. **He draws the conclusion.** If a tradition exists only while it is being
   practised, then keeping it alive is nobody's private business. It is a duty
   owed to the ancestors who gave it and to the children who have not yet
   received it.

**The quiet warning.** Running under the argument is a criticism of outsiders who
collect, record, display and sell what belongs to a living community. LaPena
rarely raises his voice about it, but the logic of the essay condemns the practice
completely: you cannot preserve a tradition by removing it from the only place it
can live.

## 13.4 Themes

**Identity.** Who a person is, in this essay, is settled by what they take part
in. Identity is communal and practical rather than private and declared.

**Continuity between generations.** The past is not behind the community; it is
present in the songs, the names and the ceremonies. The ancestors are participants,
not history.

**Responsibility.** The essay's key word. Knowledge is a trust, and a trust
creates duties.

**Respect for elders.** Authority rests with those who have lived the tradition
longest, and the correct attitude of the young is patience.

**Human beings and the natural world.** Ceremonies exist to keep the relationship
with the land, the water, the animals and the seasons in repair. Nature is family,
not scenery or resource.

**The sacred and the restricted.** Not everything may be told to everybody. The
essay asks outsiders to accept limits they would rather not accept.

**Appropriation and commercialisation.** Taking cultural material for study,
fashion or profit is treated as a kind of quiet destruction.

**Change within continuity.** A tradition survives by adapting. Rigid imitation of
the past is the opposite of tradition, not its purest form.

## 13.5 Style and technique

**A reflective personal essay.** LaPena writes in the first person and from
inside. He does not pretend to the neutral voice of an anthropologist; his
authority comes from having danced, not from having researched.

**Tone.** Calm, patient, unhurried, occasionally firm. He is explaining rather
than attacking, and the restraint is a strategy: a reader who would resist a
protest may accept an explanation.

**Definition as a weapon.** His central technique is to take a familiar word —
tradition, art, sharing, authentic — and quietly replace the reader's definition
with his own. The argument is won at the level of vocabulary.

**Concrete example instead of abstraction.** Dances, songs, regalia, feathers,
baskets, the behaviour of elders: the ideas arrive attached to things that can be
seen and handled, which keeps a philosophical essay readable.

**Inclusive pronouns.** "We" and "our" appear throughout, marking him as a member
of the community he describes and reminding the reader that this is testimony as
much as analysis.

**Repetition of key words.** *Tradition*, *share*, *respect*, *responsibility*
recur until they carry the weight of the whole argument, in the way that repeated
words in a ceremony gather force.

**Understatement.** The criticism of collectors and researchers is made by
implication rather than accusation. He states what a tradition is, and leaves the
reader to see what taking it away must therefore do.

**Circular structure.** The essay ends where its title began — on sharing — so the
form of the essay repeats the shape of the thing it describes: a circle in which
what is received must be given again.

## 13.6 Glossary

| Word | Meaning |
|---|---|
| tradition | a way of doing things handed down within a community from one generation to the next |
| indigenous | belonging naturally to a place; the original inhabitants of a region |
| Wintu | an indigenous people of northern California; LaPena was of Nomtipom Wintu descent |
| elder | an older member of a community, respected for experience and knowledge |
| ceremony | a formal act or series of acts performed on a sacred or important occasion |
| ritual | the fixed order of actions followed in a ceremony |
| oral tradition | knowledge passed on by speech and song rather than in writing |
| ancestors | the people of one's family or community who lived in the past |
| regalia | the special clothing and ornaments worn in a ceremony |
| sacred | set apart as holy; to be treated with reverence |
| secular | not religious; belonging to ordinary daily life |
| heritage | what is inherited from earlier generations |
| continuity | unbroken connection over time |
| custodian | a person responsible for looking after something belonging to others |
| in trust | held on behalf of someone else, to be handed on rather than owned |
| appropriation | taking something that belongs to another culture and using it as one's own |
| commercialisation | turning something into a product to be bought and sold |
| anthropologist | a scholar who studies human societies and cultures |
| authentic | genuine; truly what it claims to be |
| renewal | the act of making something new or whole again |
| reciprocity | the practice of giving in return for what one has received |

## Chapter summary

- Frank LaPena (1937–2019), a Nomtipom Wintu artist, dancer and professor,
  writes from inside the tradition he describes.
- **Thesis:** tradition is a living practice, not a collection of facts or
  objects; it belongs to a community; and receiving it creates the duty to live
  it and pass it on.
- A "traditional person" is defined by participation — ceremony, obligation,
  discipline — not by knowledge or ownership.
- Tradition is learnt from **elders**, **orally** and **by doing**; knowledge is
  **earned**, and some of it is sacred and restricted.
- Ceremonial art is made for **use**, not display. An object in a museum has been
  separated from the only setting that gave it meaning.
- Living traditions **change**; what must not change is the relationship behind
  them. Rigid imitation is not authenticity.
- Style: reflective first-person essay; calm tone; redefinition of key words;
  concrete examples; inclusive "we"; understated criticism of collectors and
  commercial users; circular structure.

## Practice questions

**Short answer questions (2 marks each)**

1. According to LaPena, who counts as a "traditional" person? <span class="marks">[2]</span>
2. How is traditional knowledge passed from one generation to the next? <span class="marks">[2]</span>
3. Why does LaPena say that knowledge must be earned? <span class="marks">[2]</span>
4. How does the traditional artist differ from the artist who works for a
   gallery? <span class="marks">[2]</span>
5. Why is a ceremonial object in a museum not the same object? <span class="marks">[2]</span>
6. Does LaPena believe a tradition must never change? Explain. <span class="marks">[2]</span>
7. What does the title "Sharing Tradition" mean in the essay? <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** A traditional person is one who **lives** the tradition: who takes part in
the ceremonies, keeps the obligations that go with them, accepts the discipline of
the community and behaves accordingly. Knowing many facts about the old ways, or
owning old objects, does not make anyone traditional.

**2.** It is passed on by the elders, orally and by example — through songs,
names, prayers, stories and, above all, through taking part in ceremonies and
dances. The learner is present, watches, is given small tasks, and slowly grows
into the knowledge instead of being taught it in lessons.

**3.** Because some knowledge is sacred and powerful, and careless handling can
damage both the knowledge and the person. A learner has to show patience, respect
and steadiness before more is given; certain songs, names and roles belong to
particular families and are not given out generally. Earning it is part of
learning to treat it properly.

**4.** The traditional artist makes things for **use** — regalia, baskets, songs,
paint for a ceremony — under obligations about how they are made and what may be
done with them. A gallery artist makes objects to be looked at, judged and sold.
The first kind of art has a job to do in the life of a community; the second is
complete when it is admired.

**5.** Because its meaning lay in its use. Once it is taken out of the ceremony,
put behind glass and labelled, it is cut off from the people, the purpose and the
relationships that made it what it was. It looks the same, but it has become
information about a tradition rather than a living part of one.

**6.** No. He says that living traditions have always changed — new materials, new
songs, new circumstances in every generation — and that a tradition which cannot
change has already become a museum piece. What must stay constant is not the
outward detail but the relationship behind it: the respect, the purpose and the
connection to ancestors and land.

**7.** It means passing the tradition on: teaching the right things to the right
people at the right time, so that the practice continues into the next
generation. It does **not** mean making everything public. Because each generation
holds the tradition in trust rather than owning it, sharing is a duty owed to the
ancestors who gave it and to the children who have not yet received it.
:::

**Long answer questions (5 marks each)**

1. State LaPena's central argument in "Sharing Tradition" and show how he builds
   it. <span class="marks">[5]</span>
2. How does LaPena describe the relationship between art, ceremony and community?
   Why does he object to ceremonial objects being collected and displayed? <span class="marks">[5]</span>
3. Discuss the style and technique of "Sharing Tradition". How does LaPena
   persuade a reader who is outside his culture? <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** LaPena's thesis is that tradition is a **living practice** rather than a
body of information or a collection of objects, that it belongs to a community
rather than to an individual, and that anyone who receives it takes on the
responsibility of living it properly and handing it on. He builds this in five
moves. First he redefines the key term: instead of asking what tradition is, he
asks who counts as a traditional person, and answers that it is the one who takes
part, keeps the obligations and accepts the discipline — so tradition shifts from
*things known* to *things done*. Second, he shows how the knowledge travels: from
elders, orally, slowly, through participation and the body, so that it cannot be
detached from the people who carry it. Third, he applies the same test to art:
regalia, songs and baskets are made for use in ceremony, which gives him his
strongest evidence, because an object removed from its use looks identical and is
not the same thing. Fourth, he disposes of the obvious objection — that a real
tradition must be unchanging — by pointing out that living things change, and that
what must be constant is the relationship, not the detail. Finally he draws the
conclusion the reader has already reached: since a tradition exists only while it
is practised, keeping it alive is a duty owed backwards to the ancestors and
forwards to the children.

**2.** In LaPena's account the three are not separable. Ceremony is the centre of
community life: dances and songs are not entertainment but work that has to be
done, to give thanks, to mark the seasons and the stages of a life, and to keep
the relationship between the people and the natural world in good repair. Art
exists to serve that work. Regalia, feathers, baskets, paint and song are made for
use, and they come with obligations — who may make them, how, and what may be done
with them afterwards. There is no separate category of "the artist" standing apart
from the community and expressing a private vision; the maker is a member with a
job. This is exactly why LaPena objects to collection and display. A ceremonial
object in a museum has been cut away from the people who used it, the occasion it
was used for, and the obligations that surrounded it; what remains behind the
glass is the shape of the thing without the thing itself. Worse, the removal is
presented as preservation, when in fact it takes the living part away and keeps
the shell. The same objection covers songs recorded by researchers, designs
borrowed by businesses, and ceremonies watched as tourist spectacle. His position
is consistent rather than merely protective: if meaning lies in practice, then
anything taken out of practice has lost its meaning, however carefully it is
stored.

**3.** LaPena writes a reflective personal essay in the first person, and his
authority is that of a participant rather than a researcher — he has danced, not
merely studied. That position governs everything else. The tone is calm, patient
and explanatory; he sets out to make an outsider understand rather than to accuse,
and the restraint is persuasive, because a reader who would argue with a protest
will often accept an explanation. His central technique is **redefinition**: he
takes familiar words — tradition, art, authentic, sharing — and quietly replaces
the reader's everyday meaning with his own, so that the argument is largely won at
the level of vocabulary before any conclusion is stated. He keeps the essay
readable by attaching ideas to concrete things: dances, songs, regalia, baskets,
the behaviour of the old people. The pronouns "we" and "our" mark him as a member
of the community, turning parts of the essay into testimony. Key words —
*tradition*, *respect*, *responsibility*, *share* — are repeated until they carry
the weight of the argument, much as repetition in a ceremony gathers force.
Finally, his criticism of collectors, researchers and commercial users is made by
**understatement**: he describes what a tradition is and lets the reader work out
what removing it must do. The essay ends on the idea its title began with,
closing a circle — which is also the shape of the tradition it describes.
:::

**Reference to the context**

1. LaPena argues that a person is not traditional because of what he knows or
   owns, but because of what he takes part in.
   (a) What definition of tradition does this imply? (b) Why does the definition
   matter for the rest of the essay? (c) What responsibility does it place on the
   individual? <span class="marks">[5]</span>
2. LaPena points out that a ceremonial object placed in a museum case is no
   longer the object it was.
   (a) Why does he say this? (b) What criticism of outsiders is implied?
   (c) What, according to him, is the right way to keep a tradition alive? <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) It implies that tradition is a **living practice** — something done
rather than something known or possessed. A tradition exists in ceremonies
performed, songs sung, obligations kept and discipline accepted, not in facts
stored or objects owned.
(b) It matters because every later claim in the essay rests on it. If tradition
lives only in practice, then knowledge cannot be separated from the people who
carry it, ceremonial art cannot be separated from its use, and a recorded or
collected version of a tradition is necessarily a dead one. The definition is the
foundation of the whole argument.
(c) It makes each person a **custodian** rather than an owner. Because the
tradition exists only while it is practised, the individual who has received it
must go on living it properly and must pass it on to those who come after. The
responsibility runs in two directions: to the ancestors who handed it down and to
the children who have not yet received it.

**2.** (a) Because the meaning of such an object lay in its **use**. It was made
for a ceremony, under obligations about who could make it and what could be done
with it. Behind glass it is separated from the people, the occasion and the
relationships that gave it meaning, so what survives is the shape of the thing
without the thing itself.
(b) The implied criticism is of anthropologists, collectors, tourists and
businesses who take songs, designs and objects out of living communities for
study, decoration or profit, and then describe what they are doing as preserving a
culture. LaPena's logic makes this impossible: they remove the living part and
keep the shell. He makes the charge by understatement rather than accusation,
which gives it more force.
(c) By continuing to practise it. Traditions are kept alive by elders teaching,
young people taking part, ceremonies being performed, and knowledge being earned
and then passed on at the right time to the right people. Traditions may change
their outward details in every generation, and should; what must be preserved is
the relationship of respect between the community, its ancestors and the natural
world.
:::

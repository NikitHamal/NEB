---
subject: Compulsory English
grade: 12
unit: 16
title: Humility
hours: 3
area: Literature - Essays
---

Every group of people likes to believe that its story is the most important story ever told.
Greeks say history began in Athens, Chinese nationalists say it began with the Yellow Emperor,
some Hindu nationalists say aeroplanes were flying in the age of the sages, pious Muslims see
all earlier history as irrelevant, and the Aztecs thought the sun would not rise without their
sacrifices. Yuval Noah Harari collects these claims in one breezy, funny and unsettling
essay, and then does something unusual: he turns the same lens on **his own people**. "Humility"
is an essay about the most dangerous form of pride — the belief that *my* nation, *my* culture,
*my* religion is the centre of the world. It is shorter than the other essays in this unit and
very easy to read, but examiners like it because the claims are concrete and the question
"Why is history a contested issue?" invites a good, thoughtful answer.

::: key What the exam wants from this essay
**The thesis**: you are **not** the centre of the world; no nation or religion invented human
civilisation. **The catalogue of claims**: Greeks, Chinese nationalists, Hindu nativists,
pious Muslims (with the Turkish, Iranian and Egyptian exceptions), British, French, Germans and
others, and the Aztecs. **The verdict**: "All these claims are false" — they combine wilful
ignorance of history with "more than a hint of racism". **The truth**: **morality, art,
spirituality and creativity** are universal human abilities embedded in our DNA, born in Stone
Age Africa. **The method**: Harari criticises his **own people** (the Jews) first, with the
yoga example, because "it is more polite to criticise one's own people than to criticise
foreigners". Short questions ask for a group's claim, the universal abilities or the yoga story;
the long question is about why history is contested.
:::

## 16.1 About the author

```photo id="eng12/harari" caption="Yuval Noah Harari, historian and author, at the Frankfurt Book Fair in 2024. Photograph by Martin Kraft, licensed CC BY-SA 4.0." width="36"
crop 0.0 0.08 1.0 1.0
```

Yuval Noah Harari was born in **1976** in Israel. He studied history at the Hebrew University of
Jerusalem and completed his doctorate at the **University of Oxford** in 2002, working on
medieval and military history. He is now a **professor of history at the Hebrew University of
Jerusalem**, where he teaches world history, and he is also known as a public thinker, who
writes about the long past of humankind in order to ask what kind of future we are choosing.

His books have sold in tens of millions of copies in dozens of languages:

| Book | Year | Theme |
|---|---|---|
| *Sapiens: A Brief History of Humankind* | 2011 (Hebrew); 2014 (English) | how *Homo sapiens* came to dominate the planet: the cognitive, agricultural and scientific revolutions |
| *Homo Deus: A Brief History of Tomorrow* | 2015 (Hebrew); 2016 (English) | what humans may become with biotechnology and artificial intelligence |
| *21 Lessons for the 21st Century* | 2018 | the present: work, liberty, nationalism, religion, truth, education, meaning |
| *Sapiens: A Graphic History* | 2020 onwards | a comic-book retelling of *Sapiens* (named in your textbook) |
| *Nexus* | 2024 | information networks from the Stone Age to artificial intelligence |

Your textbook's note adds that he is a co-founder of **Sapienship**, a social-impact company
whose mission, the textbook says, is "to clarify the public conversation, support the quest for
solutions and focus attention on the most important challenges facing the world". It also says
that Harari "exemplifies the virtue of humility in that he debunks humanity's illusions of
superiority and mastery". The essay "Humility" is taken from ***21 Lessons for the 21st Century***
(2018): it is chapter 12 of the book, which has five parts and twenty-one short "lessons". The
passage in your textbook is an **extract** from the opening of that chapter, under the heading
"You are not the centre of the world".

::: caution Harari reports these claims; he does not endorse them
When Harari writes "Did you know … that it was Maharishi Bhardwaj who invented rockets and
aeroplanes …?" he is **quoting what some nationalists claim**, in order to show that the claim is
absurd. He is not insulting Hinduism, Islam, Judaism, China or Greece. His point is that *every*
group does this, and that *all* of them are wrong in the same way. He spends the most words on
**his own people**. In an answer, write "some Hindu nativists claim …", never "Harari says that
Indians invented aeroplanes".
:::

## 16.2 The essay: shape and argument

"Humility" is an **argumentative (persuasive) essay** with a strong thread of **satire**. It is
built like a good speech: a bold claim, a long series of examples, a one-line verdict, a
positive truth, a personal confession, and a closing image. Seen as a list, the structure is:

| Step | What happens |
|---|---|
| 1. The claim | "Most people tend to believe they are the centre of the world, and their culture is the linchpin of human history." |
| 2. The catalogue | Greeks; Chinese nationalists; Hindu nativists; pious Muslims; Turkish, Iranian and Egyptian nationalists; British, French, Germans, Americans, Russians, Japanese; the Aztecs. |
| 3. The verdict | "All these claims are false." Reasons: they show wilful ignorance and a hint of racism; no present-day nation or religion existed when humans settled the world, tamed plants and animals, built the first cities or invented writing and money. |
| 4. The truth | Morality, art, spirituality and creativity are universal human abilities in our DNA, born in Stone Age Africa; to place them in a later time and place is "crass egotism". |
| 5. The confession | "I am all too familiar with such crass egotism": the Jews think they are the most important thing in the world. The yoga story. |
| 6. The escalation | Orthodox Jews think the cosmos exists so that rabbis can study; secular Jews too believe Jews are the heroes of history. |
| 7. The method | Harari uses his own people as the example, and leaves the reader to "puncture the hot-air balloons inflated by their own tribes". |

```figure caption="How recent the claimed beginnings are. The approximate age of each event, in years before now, on a logarithmic scale: every nation's proud starting point falls in the last few thousand years, while the human abilities Harari names are far older. Dates are approximate and the Xia and Shang dates are the traditional ones."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.3))
items=[('Homo sapiens appears in Africa',300000,'#2E7D32'),
       ('First farming and domesticated animals',11000,'#2E7D32'),
       ('First writing (Sumer)',5200,'#2E7D32'),
       ('Xia dynasty (traditional date)',4100,ACCENT),
       ('Shang dynasty (traditional date)',3600,ACCENT),
       ('Homer, the Greek epics',2800,ACCENT),
       ('Plato in Athens',2400,ACCENT),
       ('Revelation of the Quran begins',1400,ACCENT)]
names=[i[0] for i in items][::-1]; vals=[i[1] for i in items][::-1]; cols=[i[2] for i in items][::-1]
y=np.arange(len(items))
ax.barh(y,vals,color=cols,height=0.62)
ax.set_xscale('log'); ax.set_xlim(300,2500000)
ax.set_yticks(y); ax.set_yticklabels(names,fontsize=6.8,color=INK)
for yi,v in zip(y,vals):
    ax.text(v*1.25,yi,f'{v:,}',va='center',fontsize=6.6,color=INK)
ax.set_xticks([1000,10000,100000]); ax.set_xticklabels(['1,000','10,000','100,000'],fontsize=6.8,color=MUTED)
ax.set_xlabel('years ago (log scale)',fontsize=7.2,color=MUTED)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='x',color=GRID,lw=0.6); ax.set_axisbelow(True)
fig.subplots_adjust(left=0.42,right=0.97,top=0.98,bottom=0.15)
```

## 16.3 The essay, part by part

### Part 1 — "You are not the centre of the world"

The heading is the thesis. "Most people tend to believe they are the centre of the world, and
their culture is the **linchpin** of human history." A linchpin is the pin through the end of an
axle that stops the wheel from coming off; without it everything falls apart. Each group thinks
*its* culture is that pin. Then comes the catalogue:

- **The Greeks.** "Many Greeks believe that history began with **Homer, Sophocles and Plato**, and
  that all important ideas and inventions were born in **Athens, Sparta, Alexandria or
  Constantinople**."
- **Chinese nationalists.** They "retort that history really began with the **Yellow Emperor and the
  Xia and Shang dynasties**, and that whatever Westerners, Muslims or Indians achieved is but a
  pale copy of original Chinese breakthroughs."
- **Hindu nativists.** They "dismiss these Chinese boasts" and argue that "even **airplanes and
  nuclear bombs** were invented by ancient sages in the Indian subcontinent long before Confucius
  or Plato, not to mention Einstein and the Wright brothers". Harari gives examples, asking in
  mock surprise: "Did you know … that it was **Maharishi Bhardwaj** who invented rockets and
  aeroplanes, that **Vishwamitra** not only invented but also used missiles, that **Acharya Kanad**
  was the father of atomic theory, and that the **Mahabharata** accurately describes nuclear
  weapons?"
- **Pious Muslims.** They "regard all history prior to the Prophet Muhammad as largely
  irrelevant", and they consider all history after the revelation of the Quran "to revolve
  around the **Muslim ummah**" (the worldwide community of believers). The exceptions are
  **Turkish, Iranian and Egyptian nationalists**, who argue that even before Muhammad *their*
  nation was "the fountainhead of all that was good about humanity", and that after the Quran it
  was mainly *their* people who preserved the purity of Islam and spread its glory.
- **Everyone else.** "British, French, German, American, Russian, Japanese and countless other
  groups are similarly convinced that humankind would have lived in **barbarous and immoral
  ignorance** if it wasn't for the spectacular achievements of their nation."
- **The Aztecs.** Some peoples went so far as to think that political institutions and religious
  practices were essential to the laws of physics: "the Aztecs firmly believed that without the
  **sacrifices** they performed each year, the **sun would not rise** and the entire universe would
  disintegrate".

```figure caption="Everyone at the centre. Each group in Harari's catalogue places itself at the centre of history; the truth he offers in the middle is that the shared human abilities are older than all of them."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.6))
ax.set_xlim(-5.2,5.2); ax.set_ylim(-3.6,3.6); ax.axis('off')
pos=[(0,2.85,'Greeks','Homer, Plato: ideas\nborn in Athens'),
     (3.45,1.35,'Chinese nationalists','Yellow Emperor, Xia,\nShang: rest a pale copy'),
     (3.45,-1.35,'Hindu nativists','sages invented rockets,\natoms, aeroplanes'),
     (0,-2.85,'Pious Muslims','history before Muhammad\nlargely irrelevant'),
     (-3.45,-1.35,'Aztecs','sacrifice keeps the\nsun rising'),
     (-3.45,1.35,'Jews (his own people)','Abraham invented yoga;\nrabbis hold up the cosmos')]
for x,y,t,d in pos:
    ax.plot([0,x*0.62],[0,y*0.62],color=GRID,lw=1.2,zorder=0)
    ax.add_patch(FancyBboxPatch((x-1.45,y-0.5),2.9,1.0,boxstyle='round,pad=0.02,rounding_size=0.12',fc='white',ec=ACCENT,lw=1.3))
    ax.text(x,y+0.22,t,ha='center',va='center',fontsize=6.9,fontweight='bold',color=INK)
    ax.text(x,y-0.18,d,ha='center',va='center',fontsize=6.2,color=MUTED,linespacing=1.15)
ax.add_patch(Ellipse((0,0),3.7,2.0,fc='#2E7D32',ec='none'))
ax.text(0,0.36,'the truth',ha='center',va='center',color='white',fontsize=7,fontweight='bold')
ax.text(0,-0.14,'morality, art, spirituality,\ncreativity: universal,\nfrom Stone Age Africa',ha='center',va='center',color='white',fontsize=6.0,linespacing=1.1)
fig.subplots_adjust(left=0.01,right=0.99,top=0.99,bottom=0.01)
```

### Part 2 — "All these claims are false"

The verdict is a short paragraph: "All these claims are false. They combine a **wilful ignorance
of history** with more than a hint of **racism**." Harari's reasons are historical. "None of the
religions or nations of today existed when humans **colonised the world**, **domesticated plants and
animals**, **built the first cities**, or **invented writing and money**." Those steps, which made
civilisation possible, were taken by peoples long before any of today's nations and faiths.
Then the positive truth: "**Morality, art, spirituality and creativity are universal human
abilities embedded in our DNA.** Their genesis was in **Stone Age Africa**." To place them later —
"China in the age of the Yellow Emperor, Greece in the age of Plato, or Arabia in the age of
Muhammad" — is "**crass egotism**".

::: note How solid is "embedded in our DNA"?
Harari uses "DNA" as a vivid way of saying "part of what it is to be human", because these
abilities are shared by all modern human groups and appear in very old human sites — cave
paintings, burials and jewellery, for instance. You may quote him, but in an answer also say
what he *means*: they are **inborn, universal and ancient**, not the invention of any single
nation. (*Homo sapiens* itself appears in Africa some 300,000 years ago, according to fossils
found in Morocco and elsewhere.)
:::

### Part 3 — "my own people" and the yoga story

Now Harari makes the essay personal. "Personally, I am all too familiar with such crass
egotism, because **the Jews, my own people**, also think that they are the most important thing
in the world. Name any human achievement or invention, and they will quickly claim credit for
it." He knows, he says, that they are **genuinely convinced**.

Then the story. "I once went to a **yoga teacher in Israel**, who in the introductory class
explained in all seriousness that yoga was invented by **Abraham**, and that all the basic yoga
postures derive from the **shape of the letters of the Hebrew alphabet**." (The triangle
posture *trikonasana* imitates the letter *aleph*, *tuladandasana* the letter *daled*.) Abraham
taught the postures to the son of one of his **concubines**, who went to India and taught yoga to
the Indians. Asked for evidence, the teacher quoted **Genesis 25:6**: "And to the sons of his
concubines Abraham gave gifts, and while he was still living he sent them away from his son
Isaac, eastward to the east country." Harari's punchline is a question: "**What do you think these
gifts were?** So you see, even yoga was actually invented by the Jews." The joke lies in the
leap from a *gift* mentioned in a verse to *yoga* — evidence that proves nothing, taken with
total seriousness.

```photo id="eng12/pale-blue-dot" caption="The 'Pale Blue Dot': Earth, marked by the label, is a speck about one pixel wide in a photograph taken by the Voyager 1 spacecraft from about 6 billion kilometres away in 1990. The picture is often used to illustrate humility; it is Carl Sagan's image, not Harari's. NASA image, public domain." width="42"
crop 0.30 0.22 0.90 0.78
call 0.22 0.78 0.49 0.467 "Earth"
```

### Part 4 — the escalation, and the method

The yoga story is "a fringe notion". But "mainstream Judaism solemnly maintains that the
**entire cosmos exists just so that Jewish rabbis can study their holy scriptures**, and that if
Jews cease this practice, the universe will come to an end. China, India, Australia and even the
distant galaxies will all be annihilated if the rabbis in Jerusalem and Brooklyn stop debating the
Talmud." This is "a central article of faith of Orthodox Jews, and anyone who dares doubt it is
considered an ignorant fool". **Secular Jews** are a little more sceptical about so grand a
claim, "but they too believe that the Jewish people are the **central heroes of history** and the
ultimate wellspring of human morality, spirituality and learning".

Harari then explains why he chose this example. "What my people lack in numbers and real
influence, they more than compensate for in **chutzpah**" (a Yiddish word for bold,
shameless audacity). "Since it is more polite to criticise one's own people than to criticise
foreigners, I will use the example of Judaism to illustrate how **ludicrous** such self-important
narratives are, and I will leave it to readers around the world to **puncture the hot-air balloons
inflated by their own tribes**." The last phrase hands the job to the reader: *now check your
own group's balloon.*

::: tip Paragraph anchors for short questions
**Greeks; Chinese nationalists** → ¶1. **Hindu nativists** → ¶2. **Pious Muslims** → ¶3. **Other
nations; the Aztecs** → ¶4. **"All these claims are false"; universal abilities** → ¶5. **The yoga
story** → ¶6. **The cosmos and the rabbis** → ¶7. **Why he criticises his own people; the hot-air
balloons** → ¶8.
:::

## 16.4 Ideas and themes

**1. Egocentrism of nations and cultures.** The essay's first theme is that *every* group
thinks of itself as central. The repeated pattern — "X believe that history began with X" —
shows that the belief is a human habit, not a fact about any one people. The habit is natural
(we are born into one group and see the world from it) and dangerous (it justifies contempt for
others).

**2. Humility as honesty about evidence.** Humility here is not shyness; it is **intellectual
honesty**. To be humble about history means to check claims against evidence: Harari's
"evidence" for the Jewish yoga story is a verse that mentions *gifts* and nothing more. The
essay teaches the reader to ask, of any proud claim, "What is the proof?"

**3. The shared human heritage.** The positive message is that **morality, art, spirituality and
creativity are universal human abilities**, born in Stone Age Africa. No nation owns them. This
turns pride into a kind of **kinship**: if these abilities are ours together, then the
achievements of others are also, in a real sense, *ours*.

**4. Criticise yourself first.** Harari's method is as important as his message. He does not
pick on foreigners; he starts with "my own people". This is what gives the essay its
authority: a critic who begins with himself cannot be accused of prejudice.

**5. Why history is contested.** History is not only a record of the past but a **source of
identity, pride and political claims**. Whoever controls the story controls how people see
themselves and others. As George Orwell put it in *1984*: "Who controls the past controls the
future." This is the idea behind the textbook's question about history as a "major contested
issue".

**6. Humility and danger.** Beneath the humour is a warning. Nations convinced that they are
the centre of history have often used that belief to justify wars, conquest and persecution.
The essay suggests that a little humility is a condition of peace.

::: note Reading "Humility" with "Knowledge and Wisdom"
The two essays are neighbours in your book, and they fit together. Russell says the essence of
wisdom is freedom from "the tyranny of the **here and now**"; Harari's essay is an example of
that tyranny at the level of nations — people who cannot see beyond *their own* place and time.
Both men say that a wise person learns to see from outside the self. If an exam question lets
you compare essays, this link is an easy way to score.
:::

::: caution Do not over-claim
Harari does not say that all cultures are identical, that nothing was invented in China, India,
Greece or Arabia, or that religion is false. He says that **no single group invented the basic
human abilities**, and that the exaggerated claims of priority are false. The Chinese, Indians,
Greeks and Muslims made enormous real achievements; the essay complains about the *inflation* of
those achievements, not about the achievements themselves.
:::

## 16.5 Style and devices

**Satire and irony.** The essay is funny because it is serious about absurd things. The yoga
teacher explains the origin of yoga "in all seriousness"; the Hindu nativist list is offered
as fact ("Did you know …?"). The gap between the confident tone and the ridiculous claims is
the irony.

**Catalogue and parallelism.** A long list — Greeks, Chinese, Hindus, Muslims, British, French,
Germans, Americans, Russians, Japanese — with the same sentence pattern repeated. The repetition
makes the point before any argument is offered: *everyone* says the same thing.

**Rhetorical questions and direct address.** "Did you know … ?" "What do you think these gifts
were?" These address the reader as a partner in the joke and invite the reader to supply the
judgement.

**Hyperbole, understatement and sarcasm.** "Even airplanes and nuclear bombs"; "the entire
cosmos exists just so that Jewish rabbis can study"; and, later, "a bit more sceptical". The
mock-gravity makes each claim look silly without Harari having to say so.

**Metaphor.** "Linchpin" (of history), "fountainhead" (source), "puncture the hot-air
balloons inflated by their own tribes". The balloon image says that pride is *inflation* —
full of air, and fragile.

**Short verdict sentences.** "All these claims are false." Four words after a long list; they
sound like a judge's verdict and give the essay its force.

**Strong evaluative words.** "Wilful ignorance", "racism", "crass egotism", "ludicrous". After
the light, joking catalogue, these heavy words tell the reader that the subject, however funny,
matters.

**Personal anecdote and confession.** The yoga teacher, "my own people", "I know … they are
genuinely convinced". The first person gives a voice, a face and a source of authority.

**Foreign words.** *Ummah* (Arabic: the community of Muslim believers) and *chutzpah*
(Yiddish: audacity) are not translated in the text; they give local colour and show that Harari
knows the groups from inside.

**Tone.** Conversational, ironic, then serious; it reads like a spoken lecture rather than a
scholarly article.

## 16.6 Glossary

| Word | Meaning |
|---|---|
| linchpin | something essential that holds everything else together |
| retort | to reply sharply, often in a challenge |
| nativist | a person who defends the interests of the native-born or an "original" culture against outsiders |
| pious | deeply religious |
| ummah | (Arabic) the whole community of Muslim believers |
| fountainhead | the original source of something |
| barbarous | uncivilised and cruel |
| spectacular | very impressive |
| disintegrate | to break into pieces |
| wilful | deliberate and stubborn; done on purpose |
| embedded | fixed deeply in something |
| genesis | the origin or beginning of something |
| crass | stupid and insensitive; very obvious and tasteless |
| egotism | too much concern with oneself and one's own importance |
| concubine | in some societies, a woman who lives with a man as a partner, but with lower status than a wife |
| fringe | (as used here) at the edge of the mainstream; marginal. The textbook's gloss — "the front part of hair" — does not fit this sentence |
| annihilated | completely destroyed |
| grandiose | grand, larger and more impressive than is justified |
| chutzpah | (Yiddish) extreme self-confidence; nerve; audacity |
| ludicrous | so foolish as to be laughable |
| puncture | to make a hole in something so that the air escapes |
| tribes | (here) any group that thinks of itself as "us" against "them" |

## 16.7 Textbook exercises

**Before you read**

*a. What do you know about the Chinese civilization?*

Chinese civilisation is one of the world's oldest that has continued to the present day. It
grew up along the **Yellow River** and the **Yangtze**, and it was ruled for some four thousand
years by a succession of **dynasties** (Xia, Shang, Zhou, Qin, Han, Tang, Song, Ming, Qing and
others) until the republic of 1912. Its contributions include **paper, printing, gunpowder and
the compass**, silk, porcelain, the Great Wall and the philosophies of **Confucius** and Laozi. Its
writing system, in continuous use for more than three thousand years, has helped hold together a
very large and diverse country.

*b. Are there any similarities between South Indian and Chinese civilizations? Discuss.*

(The textbook labels this question "c"; there is no "b".) Yes, there are several similarities.
Both are **very old, continuous civilisations** with their own classical languages and literature
(Tamil and Sanskrit in the south of India; classical Chinese). Both developed **rice-growing
societies** and great **river and coastal trade**; the ancient Tamil kingdoms traded with the
Roman world and with South-East Asia, while China traded along the Silk Road and the sea. The two
were in **direct contact**: Buddhism travelled from India to China, and the Chola kings of South
India sent embassies to the Song court in the eleventh century. Both are also proud of their
long history and value family, ancestors and ritual. The differences (language families,
religions, writing) are equally important; the similarities show that great civilisations have
long learned from one another, which is exactly Harari's point.

**Understanding the text**

*a. Describe the claim of the Chinese nationalists about human history.*

Chinese nationalists "retort that history really began with the **Yellow Emperor and the Xia and
Shang dynasties**", and that whatever Westerners, Muslims or Indians achieved is "but a **pale
copy** of original Chinese breakthroughs". That is, they believe that Chinese civilisation is
the source of all human history and invention and everything else is an imitation.

*b. What do pious Muslims believe about human history?*

Pious Muslims regard **all history before the Prophet Muhammad as largely irrelevant**, and
believe that all history after the revelation of the Quran **revolves around the Muslim ummah**.
The main exceptions are Turkish, Iranian and Egyptian nationalists, who say that even before
Muhammad their own nation was the fountainhead of all that was good in humanity, and that
afterwards it was their people who kept Islam pure and spread its glory.

*c. What did the Aztecs firmly believe about the universe?*

They firmly believed that **without the human sacrifices they performed each year, the sun
would not rise and the entire universe would disintegrate**. They thought their religious
practices were essential to the working of physical laws.

*d. What, according to the essay, are the universal human abilities?*

**Morality, art, spirituality and creativity.** The essay says they are "embedded in our DNA"
and that their genesis was in **Stone Age Africa**, long before any present-day nation or religion.

*e. How are the basic yoga postures derived from the shape of the letters of the Hebrew alphabet?*

According to a yoga teacher in Israel, whom Harari quotes, yoga was **invented by Abraham**,
and its basic postures are **copied from the shapes of Hebrew letters**: *trikonasana* (the
triangle posture) imitates the letter *aleph*, *tuladandasana* the letter *daled*. Abraham taught
these postures to the son of one of his concubines, who travelled to India and taught the
Indians. The "evidence" was Genesis 25:6, which says Abraham gave gifts to his concubines' sons
and sent them away eastward. Harari treats this as a comic example of self-important history.

**Reference to the context**

*a. How do Hindu nationalists refute the Chinese claim that human history really began with the Yellow Emperor and the Xia and Shang dynasties? Who do you agree with, and why?*

The Hindu nativists "dismiss these Chinese boasts" by making an **even bigger claim of their
own**: that even airplanes and nuclear bombs were invented by ancient sages of the Indian
subcontinent long before Confucius or Plato, not to mention Einstein and the Wright brothers.
As examples they say that Maharishi Bhardwaj invented rockets and aeroplanes, that Vishwamitra
invented and used missiles, that Acharya Kanad was the father of atomic theory and that the
Mahabharata describes nuclear weapons accurately.

I agree with neither, and I think Harari does not either. Each claim rests on national pride and
not on evidence: there is no archaeological or documentary proof of ancient aeroplanes or
atomic weapons, and the Chinese and Indian claims contradict each other. The real history is
that writing, farming, cities, moral systems and art arose in many places and were shared and
improved through trade and travel. Ancient China and India made great real achievements —
Indian mathematics gave the world the zero and the decimal system, and China gave paper and
printing — and they do not need to be exaggerated.

*b. The author has dealt with a controversial debate on human history. Why do you think history has been a major contested issue in the present world?*

History is contested because it is **more than the past**: it shapes identity, pride and power.
A nation that can say it is the oldest or the most creative feels entitled to respect, territory
and leadership, and its leaders often use the story to unite people or to justify politics.
School textbooks, museums, monuments and festivals become battlegrounds, since whoever tells the
story influences how the young see themselves and their neighbours. Colonial rule, wars and
migrations have left many groups with memories of injury, each telling a different version. And
in our age social media spreads simple, flattering stories much faster than careful research.
The result, as Harari shows, is that every group thinks it is at the centre of history, and
conflicts over history become conflicts over who matters.

**Reference beyond the text**

*a. Write a short essay on The Conflicting History of Human Civilization.*

Model essay (about 220 words).

**The Conflicting History of Human Civilization.** Human civilisation has many authors, but each
people likes to think that it was the main one. The Greeks point to Homer and Plato; Chinese
nationalists to the Yellow Emperor; some Indians to ancient sages and their flying machines; many
Muslims see history as beginning with the Prophet; the Aztecs believed the sun itself depended on
them. Every group tells a story in which it stands at the centre.

The evidence says otherwise. The first steps towards civilisation — language, art, religion,
farming, cities and writing — were taken long before any present nation or religion existed.
Modern humans arose in Africa, and their abilities to make art, to create myths and to ask moral
questions belong to all. Civilisations grew through contact: numerals from India, paper from
China, geometry from Greece, medicine from many lands.

Why, then, are histories in conflict? Because history gives pride, identity and political power.
Nations use the past to justify the present. The remedy is humility — to test claims against
evidence, to admit what we owe to others and to study other people's histories as seriously as
our own. Human civilisation is a shared inheritance, not anyone's private property.

*b. The author claims, "Since it is more polite to criticize one's own people than to criticize foreigners." Do you agree with his claim? Give your reasons.*

I largely agree. **First**, criticising outsiders is easily heard as an insult, and the listeners
stop thinking and start defending. Criticism of one's own people is heard as honesty, because
it comes from someone who shares their fate. **Second**, a critic who starts at home has
**authority**: he cannot be accused of prejudice, as Harari shows by starting with the Jews and
only then inviting others to look at their own "hot-air balloons". **Third**, it is fairer: each of us
knows our own group's faults best and is best placed to change them. **However**, politeness is
not the only test. Honest criticism of others is sometimes necessary, for example when they do
real harm, and self-criticism can become self-hatred or an easy way to avoid the truth about
others. The best rule is Harari's own: begin with your own people, but do not stop there.

## Chapter summary

- **Yuval Noah Harari** (born 1976) is a historian at the Hebrew University of Jerusalem and
  the author of *Sapiens*, *Homo Deus* and *21 Lessons for the 21st Century*; "Humility" is an
  extract from chapter 12 of the last.
- Thesis: "You are not the centre of the world" — most people believe that their culture is the
  linchpin of history.
- Catalogue: **Greeks** (Homer, Plato, Athens); **Chinese nationalists** (Yellow Emperor, Xia and
  Shang; others a pale copy); **Hindu nativists** (Bhardwaj, Vishwamitra, Kanad, the Mahabharata);
  **pious Muslims** (pre-Muhammad history irrelevant; the ummah; Turkish, Iranian and Egyptian
  exceptions); British, French, Germans and others; the **Aztecs** (sacrifice keeps the sun
  rising).
- Verdict: "All these claims are false" — wilful ignorance of history and "more than a hint of
  racism". No present nation or religion existed when humans colonised the world, domesticated
  plants and animals, built the first cities, invented writing and money.
- Truth: **morality, art, spirituality and creativity** are universal human abilities embedded in
  our DNA; their genesis was in **Stone Age Africa**; to place them later is **crass egotism**.
- Confession: the **Jews, his own people**, also claim credit for everything — the **yoga**
  story (Abraham; Hebrew letters; Genesis 25:6) and the belief that the cosmos exists so rabbis
  can study the Talmud.
- Method: "more polite to criticise one's own people"; he leaves readers to "puncture the
  hot-air balloons inflated by their own tribes".
- Devices: satire, irony, catalogue, rhetorical questions, hyperbole, metaphor, personal
  anecdote, strong evaluative words.

## Practice questions

**Short answer questions (2 marks each)**

1. What are the universal human abilities according to Harari? (NEB 2079, Set A and Set E) <span class="marks">[2]</span>
2. How do the Hindu nativists oppose the claim of Chinese nationalists about human history and civilisation? (NEB 2081, Set B) <span class="marks">[2]</span>
3. The essayist calls on readers around the world to "puncture the hot-air balloons inflated by their own tribes". What do you think is the reason behind this? (NEB 2081, Set A) <span class="marks">[2]</span>
4. Why is one not the centre of the world? Explain. (NEB 2080, Set C) <span class="marks">[2]</span>
5. What makes the author conclude that morality, art, spirituality and creativity are universal human abilities embedded in our DNA? Give your opinion. (NEB 2080, Set D) <span class="marks">[2]</span>
6. Do you agree with the author's view that history has been a major debatable issue in the present world? Give your opinion. (Model) <span class="marks">[2]</span>
7. What did the Aztecs believe about the sun, and what does Harari think of such beliefs? <span class="marks">[2]</span>
8. Why does Harari use the example of the Jews to illustrate his point? <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** According to Harari, the universal human abilities are **morality, art, spirituality and
creativity**. They are "embedded in our DNA", he says, and they began in Stone Age Africa, long
before any present-day nation or religion.

**2.** They "dismiss these Chinese boasts" by claiming something larger: that even **airplanes and
nuclear bombs** were invented by ancient sages in the Indian subcontinent long before Confucius
or Plato, not to mention Einstein and the Wright brothers — for instance, that Bhardwaj invented
rockets and aeroplanes and Kanad was the father of atomic theory.

**3.** Harari means that every group inflates its own importance — "hot-air balloons" are full of
air and nothing else — and that only the members of each group can best puncture their own pride.
By criticising his own people first, he hopes to make readers honest about their own nation,
culture or religion, so that they see how ridiculous exaggerated claims are.

**4.** Because no nation, culture or religion was the source of human history. Modern
civilisation developed from abilities that all humans share and that arose in Stone Age Africa,
long before any present-day nation; every group makes the same claim of centrality, so all the
claims cancel out. Thinking otherwise is "crass egotism".

**5.** He says these abilities existed **before any of today's nations or religions**, when humans
colonised the world, domesticated plants and animals, built the first cities and invented writing
and money, so they cannot belong to any one of them; they are common to all human groups and
have their genesis in Stone Age Africa. In my opinion the conclusion is convincing: people of
every culture paint, pray, tell stories and distinguish right from wrong, which suggests a
common, very ancient inheritance.

**6.** Yes, I agree. History is debated because it gives **pride, identity and power**. Each group
wants to be seen as the oldest or the most creative, and tells the past in ways that flatter it.
Disputes about textbooks, monuments and ancient achievements show this, and since each version
contradicts the next, history becomes contested.

**7.** The Aztecs believed that without the human sacrifices they offered every year, **the sun
would not rise** and the whole universe would fall apart. Harari uses this as an extreme case of a
people imagining that their rituals were part of the laws of nature — an example of crass
egotism.

**8.** Because, he says, "it is more polite to criticise one's own people than to criticise
foreigners". He also knows the Jews best, and starting with them shows that he is not singling
out anyone else. The yoga story and the belief that the cosmos exists for the rabbis' study show
how ludicrous self-important narratives are, and he leaves readers to treat their own tribes the
same way.
:::

**Long answer questions (5 marks each)**

1. How do Hindu nationalists refute the Chinese claim that human history really began with the
   Yellow Emperor and the Xia and Shang dynasties? (NEB 2080, GIE Set A) <span class="marks">[5]</span>
2. "You are not the centre of the world." How does Harari support this thesis in his
   essay? <span class="marks">[5]</span>
3. Why do you think history has been a major contested issue in the present world? Discuss
   with reference to the essay. (Model) <span class="marks">[5]</span>
4. Discuss the title "Humility". Is it a suitable title for the essay? <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** In his catalogue of national claims, Harari first reports that **Chinese nationalists**
say history began with the Yellow Emperor and the Xia and Shang dynasties and that whatever
Westerners, Muslims or Indians achieved is a pale copy of Chinese breakthroughs. Then he reports
the answer of **Hindu nativists**: they "dismiss these Chinese boasts" and argue that even
**airplanes and nuclear bombs** were invented by ancient sages in the Indian subcontinent long
before Confucius or Plato, not to mention Einstein and the Wright brothers. They give examples:
Maharishi Bhardwaj is said to have invented rockets and aeroplanes; Vishwamitra invented and used
missiles; Acharya Kanad was the father of atomic theory; and the Mahabharata is said to describe
nuclear weapons accurately. So the Hindu nativists do not refute the Chinese claim by evidence;
they answer it with a bigger claim of their own. Harari quotes all this in a mocking tone
("Did you know …?") to show that such claims rest on pride and not on proof, and he later says
that all such claims "are false".

**2.** Harari supports the thesis in four steps. First, he shows by a **long catalogue** that every
group believes it is at the centre: Greeks, Chinese nationalists, Hindu nativists, pious Muslims,
Turkish, Iranian and Egyptian nationalists, British, French, Germans and others, and even the
Aztecs, who thought the sun needed their sacrifices. Since all claim the centre, none can be
right. Second, he gives a **verdict and reasons**: "All these claims are false"; none of today's
nations or religions existed when humans colonised the world, domesticated plants and animals,
built the first cities and invented writing and money. Third, he states the **truth**: morality,
art, spirituality and creativity are universal human abilities embedded in our DNA and born in
Stone Age Africa, so placing them in China, Greece or Arabia is "crass egotism". Fourth, he gives
a **personal example**: the Jews, his own people, who claim to have invented yoga and believe that
the cosmos exists for the rabbis' study. By criticising his own people first, he gains authority
and invites every reader to puncture their own tribe's "hot-air balloons".

**3.** History is a contested issue first because it gives a **group its identity and pride**.
Harari's catalogue shows that every group wants to be the origin of civilisation, because
being first seems to give a right to respect and leadership. Second, history is used as a
**political tool**: governments use the past to justify their authority, borders and policies, and
to unite people against "others". Third, the **memory of injury** — conquest, colonialism, war —
leaves different communities with different versions of the same events. Fourth, in the age of
social media, flattering stories spread faster than careful research. Finally, because there is
seldom a single complete record, many claims cannot be disproved easily, and emotion fills the
gap. The result, as the essay shows, is that groups with contradictory claims each think they are
the centre. The answer is the humility Harari recommends: test claims against evidence, admit our
debt to others, and treat the human past as a common inheritance.

**4.** The title "Humility" is well chosen. Humility means not thinking oneself more important
than one is, and the whole essay is about its opposite, **pride in one's group**, which Harari
calls "crass egotism". The catalogue shows proud claims from many nations; the verdict shows
that they are false; the positive message is that the great human abilities belong to everyone,
so no group has reason for superiority; and the method of criticising his own people first is
itself an act of humility. The title is also ironic: the essay never mentions humility in its
text, but it teaches the virtue by showing the absurdity of its absence. The textbook's note,
which says Harari "exemplifies the virtue of humility", supports the title.
:::

::: tip Reference to the context
Lines that make good "explain with reference to the context" questions: "All these claims are
false. They combine a wilful ignorance of history with more than a hint of racism." "Morality,
art, spirituality and creativity are universal human abilities embedded in our DNA." "I will
leave it to readers around the world to puncture the hot-air balloons inflated by their own
tribes." Say who speaks, what comes before and after, what it means in plain words, and how it
supports the thesis that you are not the centre of the world.
:::

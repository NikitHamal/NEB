---
subject: Compulsory English
grade: 11
unit: 5
title: Civil Peace
hours: 3
area: Literature — Short Stories
---

Chinua Achebe's "Civil Peace" is set in Nigeria in the first weeks after the
Nigerian Civil War of 1967–70. Its hero, Jonathan Iwegbu, has lost a son, a job and
almost everything he owned, and still insists that he is an extraordinarily lucky
man. The story is on the syllabus because it shows, in very few pages, what
ordinary people do after a war ends — and how little the word "peace" may actually
mean to them.

::: key The central idea
The war is over but the violence is not. What has changed is only its name. Against
that, Achebe sets Jonathan's stubborn, practical, almost comic determination to
survive, count his blessings and begin again.
:::

## 5.1 About the author

Chinua Albert Chinualumogu Achebe (1930–2013) was a Nigerian novelist, poet, short
story writer and essayist, and is usually called the father of modern African
literature written in English. He was born at Ogidi in eastern Nigeria, into an Igbo
family; his parents were Christian converts, but the traditional life of the village
went on around him, and that double inheritance runs through all his work. He studied
at University College, Ibadan, and afterwards worked for the Nigerian Broadcasting
Service.

His first novel, *Things Fall Apart* (1958), is the most widely read African novel
ever written; it was followed by *No Longer at Ease* (1960), *Arrow of God* (1964),
*A Man of the People* (1966) and, much later, *Anthills of the Savannah* (1987). He
also wrote a famous essay attacking Joseph Conrad's picture of Africa in *Heart of
Darkness*. When the eastern region of Nigeria broke away in 1967 as the Republic of
Biafra, Achebe supported it and travelled abroad on its behalf; the war that
followed killed perhaps a million people, mostly of hunger, and it is out of that
experience that the stories in *Girls at War and Other Stories* (1972) — which
contains "Civil Peace" — were written. A car accident in 1990 left him unable to
walk, and he spent his last years teaching in the United States. He died in 2013.

::: definition Biafra and the Nigerian Civil War
In 1967 the mainly Igbo eastern region of Nigeria declared itself the independent
state of Biafra. The federal government fought to prevent this. The war lasted from
1967 to January 1970 and ended in Biafra's defeat, after a blockade that caused mass
starvation. "Civil Peace" begins immediately after the surrender.
:::

What is distinctive about Achebe's voice is its calm. He writes about catastrophe in
clear, unexcited sentences and lets the facts do the work. He gives his characters
their own English — here, the Nigerian Pidgin of the thieves and of Jonathan
himself — and he refuses to make his people either saints or victims. The result is
irony rather than protest: he shows you the situation and trusts you to judge it.

## 5.2 The story

**A lucky man.** The story opens with Jonathan Iwegbu deciding that he has been
extraordinarily lucky. The war is over. He has come through it with what he calls
five "inestimable blessings": his own head, his wife Maria's head, and the heads of
three of his four children. The missing child is mentioned in the same sentence as
the others, without a pause for grief, and that flat arithmetic tells us how much
death there has been. Whenever anything happens to him, good or bad, Jonathan says
the same thing: "Nothing puzzles God."

**The bicycle.** His sixth blessing is his old bicycle. During the war a Biafran
officer in a war-time uniform had tried to commandeer it for military use; Jonathan,
certain the man was no real officer, argued, then quietly paid him two pounds, and
the bicycle was released. Jonathan then buried it in the ground, wrapped up, and dug
it out after the fighting stopped to find it in working order. He at once turned it
into a taxi, carrying people and goods between the camps and the military cemetery,
and in two weeks he made a hundred and fifteen pounds — a small fortune in a
destroyed country.

**The house.** With that money he took his family back to Enugu, expecting to find
nothing. Instead his little zinc-roofed house in Ogui Overside was still standing,
though houses far more solid than his lay in rubble all around it. It needed only a
few nails, some wire and some cardboard; he found a carpenter, a man as desperate
as himself, who did the repairs for a small payment, and the family moved back in.

**Everyone works.** The whole household then sets about earning. The children pick
mangoes and sell them to soldiers' wives. Maria makes and sells breakfast balls of
fried bean paste — akara — to her neighbours. Jonathan finds that his old job at
the coal mine no longer exists: the office is open, but no one can tell him when or
whether the mines will reopen, so after a few visits he stops wasting his time and
opens a bar in his house instead, selling palm-wine to soldiers and to the few
other people with money. Achebe is careful to show that survival here is a family
business, not the achievement of one clever man.

**The ex-gratia award.** Then comes the *egg-rasher*. Biafran currency is now
worthless, and anyone who hands it in at the treasury receives a flat
"ex-gratia award" of twenty pounds — which the crowd, unable to manage the Latin
phrase, pronounces "egg-rasher". Jonathan queues for his, and Achebe fills the
scene with anxiety: people pushed together, rumours, and one man who is robbed of
his money the moment he has collected it. Jonathan, clutching his twenty pounds,
gets home safely and, for once, does not sleep well.

**The thieves.** That night the family is woken by loud knocking and a voice calling
politely to the owner of the house. Jonathan and his family begin to shout "Thief!
Thief!" into the darkness, calling for neighbours, for police, for soldiers. Nobody
comes. Then, in the most frightening moment in the story, the leader of the thieves
joins in and shouts for police and neighbours himself, mockingly, to prove that no
help exists. He tells Jonathan that the war is over and that there is no need for
anybody to be hurt: "No Civil War again. This time na Civil Peace." He wants one
hundred pounds, and says that he knows Jonathan has just collected his award. He
offers, almost courteously, to go away if the money is handed out, and even to
provide a guard afterwards.

**The bargain.** Jonathan opens the door and pleads. He has no hundred pounds; he
has only the twenty from the treasury, and they may have it. He hands over the whole
egg-rasher. The thieves take it, wish the family a good night, and go.

**The morning after.** At daybreak the neighbours arrive to sympathise. They find
Jonathan already at work, palm-wine kegs being loaded, Maria frying her akara, the
children on their way to the mango trees. He tells them not to trouble themselves.
The money came to him from nowhere a week ago, so losing it means nothing, and
anyway, he says once more, "Nothing puzzles God."

```figure caption="Jonathan's money. The twenty pounds the thieves take is a sixth of what his buried bicycle earned in a fortnight — which is exactly why he can shrug it off the next morning."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
labels = ['Bicycle taxi\n(two weeks)', 'Ex-gratia award\n("egg-rasher")',
          'Taken by the\nthieves that night']
vals   = [115, 20, -20]
cols   = ['#2e8b57', ACCENT, '#A8271F']
y = [2.0, 1.0, 0.0]
for yi, v, c in zip(y, vals, cols):
    ax.barh(yi, abs(v), height=0.44, color=c, alpha=0.88, zorder=2)
    ax.text(abs(v)+3, yi, f'{abs(v)} pounds', va='center', ha='left',
            fontsize=8.0, color=c, weight='bold')
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=7.6, color=INK, linespacing=1.4)
ax.tick_params(axis='y', length=0)
ax.set_xlim(0, 168); ax.set_ylim(-0.62, 2.62)
ax.set_xlabel('pounds', fontsize=7.8, color=MUTED)
ax.tick_params(axis='x', labelsize=7.2, colors=MUTED)
for s in ('top','right','left'):
    ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(GRID)
ax.grid(axis='x', color=GRID, lw=0.7, zorder=0)
ax.set_axisbelow(True)
ax.text(60, -0.05, 'a loss he refuses to mourn', fontsize=7.4, color=MUTED,
        style='italic', va='center')
ax.set_title('What Jonathan earned, received and lost', fontsize=8.6,
             color=INK, pad=8)
```

## 5.3 Characters

| Character | Who they are | Role in the story |
|---|---|---|
| Jonathan Iwegbu | A former coal-mine worker in Enugu; husband, father, owner of a bicycle | The protagonist: practical, cheerful, religious, endlessly adaptable |
| Maria | Jonathan's wife | Works beside him; makes and sells akara; screams for help with the family |
| The three surviving children | Unnamed; the fourth child died in the war | Pick and sell mangoes; part of the family's survival economy |
| The leader of the thieves | An unnamed man who speaks Pidgin English, polite and utterly without fear | The antagonist, and the voice of the story's title |
| The Biafran officer | Tried to commandeer the bicycle during the war | Shows that robbery in uniform came before robbery in the dark |
| The neighbours | People of Ogui Overside | Their silence at night, and their sympathy in the morning, measure the state of society |

**Jonathan Iwegbu.** He is one of the great survivors in modern fiction, and Achebe
builds him out of actions rather than feelings. Notice what he actually does: he
bribes an officer rather than argue to the end; he buries his bicycle; he digs it up
and immediately turns it into income; he stops going to the mine office the moment he
sees that the job is gone; he repairs a house with wire and cardboard; he puts his
wife and children to work; he gives the thieves everything he has rather than risk a
life. Every one of these is a decision to accept the world as it is and act. His
religion is part of the same practicality — "Nothing puzzles God" is not deep
theology but a way of refusing to be destroyed by what he cannot control. Whether we
admire this or find it disturbing is the question the story leaves open. He counts
his dead child among his blessings because three of four survived; that is either
courage or numbness, and Achebe will not tell us which.

**Maria.** She has few lines but she is never a decoration. She cooks akara before
dawn and sells it; she is with Jonathan in the dark, shouting for help; and she is
back at her frying the next morning. Achebe uses her to make the point that the
family survives as a unit, and that the labour is shared.

**The leader of the thieves.** He is the most chilling character because he is so
reasonable. He does not break down the door; he knocks and calls politely. He does
not deny that he is a thief. When the family cries for help, he takes up the cry
himself to demonstrate that no help will come — a piece of theatre that tells
Jonathan more about his country than any speech could. And it is he, not the
narrator, who names the story: the war has ended, so this is "Civil Peace". He
represents a society in which authority has collapsed and the only remaining rule is
that the armed take from the unarmed.

## 5.4 Themes

**Peace in name only.** The title is the theme. Achebe sets the whole story in the
weeks after a formal surrender and then shows a family being robbed at gunpoint
while the neighbours, police and soldiers stay silent. The thief's own phrase — "No
Civil War again. This time na Civil Peace" — makes the irony explicit. For ordinary
Nigerians, the difference between civil war and civil peace is a change of
vocabulary, not of danger.

**Survival, adaptability and work.** The story is full of small, concrete acts of
recovery: the buried bicycle, the taxi service, the cardboard and wire, the mangoes,
the akara, the palm-wine bar. Achebe's respect goes to people who do not wait to be
rescued. Jonathan's genius is that he never mourns a loss longer than it takes to
find the next opportunity.

**Loss and the value of a human life.** Behind the cheerfulness the story is full of
death. A son is gone. The bicycle earns its money by carrying people to and from a
military cemetery. Jonathan's list of blessings is literally a count of heads,
because in that war heads were what people lost. The comedy of the story sits on top
of a very large grave, and the reader is meant to feel both at once.

**Faith and fatalism.** "Nothing puzzles God" is repeated at the start of the story
and again at the very end, after the robbery. It is Jonathan's whole philosophy: what
comes, comes, and complaining changes nothing. Read positively, this faith is what
keeps him working and sane. Read critically, it is the attitude that allows injustice
to continue, because nobody demands an explanation.

**The breakdown of law and community.** The most frightening fact in "Civil Peace" is
not the thieves but the silence. Jonathan's family shout into the night for
neighbours, police and soldiers, and the only answer is the thief's mocking echo.
Yet the same neighbours come at daybreak to sympathise. Achebe is describing a
community that still feels for one another but can no longer protect one another.

```figure caption="How one family stays alive. Every member earns, and the bicycle — buried through the war — is the machine that restarts the household."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.2))
def box(x,y,w,h,t,fc,ec,fs=7.4,bold=False):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,
        boxstyle="round,pad=0.03,rounding_size=0.12",fc=fc,ec=ec,lw=1.1))
    ax.text(x,y,t,ha='center',va='center',fontsize=fs,color=INK,
            linespacing=1.45,weight='bold' if bold else 'normal')
def link(x1,y1,x2,y2):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),
        arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=10,
                        shrinkA=3,shrinkB=3))
box(5.0,2.55,3.5,0.95,'THE IWEGBU HOUSEHOLD\nEnugu, Ogui Overside','#eef3f9',ACCENT,7.6,True)
box(1.35,4.35,2.5,0.80,'Jonathan\nbicycle taxi','#f2f7f3','#2e8b57')
box(4.55,4.35,2.5,0.80,'Jonathan\npalm-wine bar','#f2f7f3','#2e8b57')
box(7.95,4.35,2.9,0.80,'Maria\nfries and sells akara','#f2f7f3','#2e8b57')
box(1.75,0.72,3.1,0.80,'Children\nsell mangoes','#f2f7f3','#2e8b57')
box(6.60,0.72,4.3,0.80,'Treasury: twenty pounds\n"egg-rasher"','#f7f3ea','#b8860b')
for x in (1.35,4.55,7.95):
    link(x,3.93,x*0.25+5.0*0.75,3.05)
link(3.0,1.10,4.2,2.06)
link(6.9,1.12,5.7,2.06)
ax.annotate('taken by thieves\nthe same night',xy=(8.80,0.72),xytext=(10.35,0.72),
    textcoords='data',ha='center',va='center',fontsize=7.2,color='#A8271F',
    style='italic',linespacing=1.4,
    arrowprops=dict(arrowstyle='<|-',color='#A8271F',lw=1.0,mutation_scale=10,
                    shrinkA=4,shrinkB=4))
ax.set_xlim(-0.4,12.3); ax.set_ylim(0.1,5.0)
ax.axis('off')
```

## 5.5 Setting, structure and point of view

**Setting.** Enugu, in eastern Nigeria, in the weeks immediately following the end
of the civil war in January 1970. The details are exact and they all carry meaning:
the zinc-roofed house standing among rubble, the military cemetery, the closed coal
mine, the treasury queue, the worthless Biafran currency. The time is the crucial
part of the setting. This is the moment when a country announces that normal life
has resumed, and the story asks what that announcement is worth.

**Structure.** The story has two clearly marked halves. The first is a rapid,
almost cheerful account of recovery — blessings, bicycle, house, jobs, money. The
second is a single night scene of about half the story's length, in which the
thieves arrive. Achebe lets the first half build our confidence in Jonathan's luck
so that the robbery lands hard. The ending then returns us, in a few lines, to
exactly where we began: a working family and the sentence "Nothing puzzles God."
This circular shape is the point. Nothing Jonathan can do changes the conditions he
lives in; all he can change is how fast he starts again.

**Point of view.** Third person, limited to Jonathan. We share his thoughts, his
valuations and his ignorance — we never learn who the thieves were, and neither does
he. Achebe also keeps his narration close to Jonathan's own speech rhythms, and he
writes the thieves' dialogue in Nigerian Pidgin English, so that the difference in
voice does part of the characterisation. The narrator never comments on the morality
of anything, which is why the irony is so strong.

::: definition Irony
Saying or showing one thing while the situation means the opposite. In "Civil Peace"
almost everything is ironic: a man who has lost a son calls himself lucky; a robbery
is conducted politely; and the word "peace" is spoken by an armed thief.
:::

## 5.6 Literary devices

| Device | Example from the text | Effect |
|---|---|---|
| Irony (situational) | A thief announces the arrival of "Civil Peace" | The title's meaning is reversed; peace is shown to be only a word |
| Irony (verbal) | Jonathan calls himself "extraordinarily lucky" after losing a child and a job | Measures how low expectations have fallen |
| Refrain / repetition | "Nothing puzzles God", spoken at the beginning and at the end | Frames the story and defines Jonathan's philosophy |
| Symbolism | The bicycle | Buried through the war and dug up after it: the buried, indestructible ability to start again |
| Symbolism | The zinc house standing in a field of rubble | Survival is arbitrary, not deserved |
| Pidgin English | The thief leader's speech | Gives the robbers a real voice and separates their world from Jonathan's formal English |
| Understatement | The dead child mentioned in the same breath as the survivors | The absence of visible grief conveys the scale of loss |
| Black humour | The mispronunciation of *ex-gratia* as "egg-rasher" | Laughter placed directly beside desperation |
| Contrast | The family's shouting versus the total silence of the neighbourhood | Shows the collapse of law and mutual protection |
| Circular structure | The last paragraph returns to the first line's attitude | Nothing has changed; the cycle of loss and work resumes |

::: caution Two misreadings to avoid
(i) "Civil Peace" is not a simple happy story about optimism. Achebe's tone is
ironic throughout, and the robbery is meant to disturb you. An answer that praises
Jonathan's cheerfulness without noticing the irony is only half an answer.
(ii) Do not say that the thieves are soldiers. The story never states who they are —
the leader only says they are not as wicked as some others. The point is that the
victim cannot tell, and that nobody comes when he calls.
:::

## 5.7 Glossary

| Word / phrase | Meaning |
|---|---|
| civil war | a war between groups inside the same country |
| Biafra | the short-lived breakaway state in eastern Nigeria, 1967–70 |
| inestimable | too valuable to be measured |
| to commandeer | to seize private property for official or military use |
| rubble | broken pieces of stone and concrete left after a building falls |
| destitute | extremely poor; having nothing at all |
| zinc (roof) | a roof made of corrugated metal sheets |
| ex-gratia award | a payment made as a favour, not because it is legally owed |
| "egg-rasher" | the crowd's pronunciation of *ex-gratia*; the twenty-pound award |
| treasury | the government office that holds and pays out public money |
| akara | fried balls of ground bean paste, eaten in West Africa for breakfast |
| palm-wine | an alcoholic drink made from the sap of palm trees |
| coal mine | an underground works where coal is dug; Jonathan's old employer |
| Pidgin English | a simplified mixed English used widely in Nigeria for daily speech |
| demobilised | released from the army after a war |
| loot | goods stolen, especially in wartime or disorder |
| vigil | staying awake, usually at night, to watch or guard |
| verandah | a roofed open platform along the outside of a house |
| miracle | an event so lucky that it seems impossible |
| to shrug off | to treat something bad as unimportant |

::: tip Exam technique for this story
Almost every question on "Civil Peace" turns on the title. Whatever you are asked —
about Jonathan, the thieves, the ending, the theme — make sure that somewhere in
your answer you explain the irony of calling this "peace", and quote the thief's own
line to prove it. Also learn the five blessings and the list of the family's
occupations; short questions are often set directly on those details.
:::

## Chapter summary

- Chinua Achebe (1930–2013), Nigerian, author of *Things Fall Apart*; "Civil Peace"
  comes from *Girls at War and Other Stories* (1972) and is set just after the
  Nigerian Civil War of 1967–70.
- Jonathan Iwegbu counts five "inestimable blessings" — his own head, his wife
  Maria's and those of three of his four children — and repeats "Nothing puzzles
  God."
- His buried bicycle survives the war; as a taxi it earns him a hundred and fifteen
  pounds in two weeks, which takes the family back to Enugu.
- Their small zinc house still stands among ruins; the whole family works — mangoes,
  akara, a palm-wine bar — since the coal mine will not reopen.
- At the treasury he receives a twenty-pound ex-gratia award, which the crowd calls
  "egg-rasher".
- That night thieves knock; nobody answers the family's cries for help, and the
  leader mockingly calls for the police himself, saying "This time na Civil Peace."
- Jonathan hands over the whole twenty pounds; by morning the family is back at
  work, and he says again that nothing puzzles God.
- Themes: peace in name only, survival and work, loss, faith or fatalism, and the
  collapse of law and community; devices include irony, the repeated refrain, the
  bicycle as symbol, Pidgin English and a circular structure.

## Practice questions

**Short answer questions (2 marks each)**

1. What are Jonathan Iwegbu's five "inestimable blessings"? <span class="marks">[2]</span>
2. Why does Jonathan treat his bicycle as a blessing, and how did he save it? <span class="marks">[2]</span>
3. How does the Iwegbu family earn a living after they return to Enugu? <span class="marks">[2]</span>
4. What is the "egg-rasher", and how much is it? <span class="marks">[2]</span>
5. What happens when Jonathan's family shouts for help during the robbery? <span class="marks">[2]</span>
6. How does Jonathan react to the loss of his money the next morning? <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** They are five heads that survived the war: his own, his wife Maria's, and
those of three of his four children. The fourth child died. He counts survival
itself as wealth, which shows both his gratitude and how much the war destroyed.

**2.** The bicycle is the machine that restarts his life: used as a taxi between the
camps and the military cemetery, it earns him a hundred and fifteen pounds in two
weeks. He saved it during the war by paying two pounds to an officer who wanted to
commandeer it, and then burying it in the ground until the fighting was over.

**3.** Everyone works. Jonathan rides his bicycle as a taxi and later opens a bar
selling palm-wine in his house; Maria makes and sells akara balls; and the children
pick mangoes and sell them to soldiers' wives. His old job at the coal mine no
longer exists.

**4.** It is the crowd's pronunciation of "ex-gratia award", a payment of twenty
pounds made by the treasury to anyone who handed in the now worthless Biafran
currency. Jonathan queues for his and receives it, and it is exactly this money the
thieves demand that night.

**5.** Nothing happens. They call for neighbours, police and soldiers, and no one
answers. The leader of the thieves then shouts for the police himself, in mockery,
to prove to Jonathan that there is no help anywhere in the neighbourhood.

**6.** He refuses to be upset. He tells the sympathising neighbours not to trouble
themselves, saying that the money came to him from nowhere only a few days before,
so that losing it means nothing to him; and he repeats "Nothing puzzles God." He and
his family are already back at work.
:::

**Long answer questions (5 marks each)**

1. Why is the story called "Civil Peace"? Discuss the irony of the title. <span class="marks">[5]</span>
2. Sketch the character of Jonathan Iwegbu. Is his attitude to life admirable? <span class="marks">[5]</span>
3. Discuss "Civil Peace" as a picture of a society just after a war. <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** The title is ironic from beginning to end. It comes from the thief himself,
who tells Jonathan through the locked door that the civil war is finished and that
this time it is "Civil Peace" — meaning that nobody need be killed provided the
money is handed out. Achebe's point is that for ordinary Nigerians the end of the
fighting brought a change of name rather than a change of condition. In the official
version, peace has returned: the treasury is paying awards, offices are open, the
government has won. In Jonathan's version, a man is robbed in the treasury queue,
armed men knock at his door at night, and when his family screams for the police,
the neighbours, and the soldiers, no one in the entire quarter answers. The thief
even shouts for the police himself to prove the point. The irony is deepened by
Jonathan's own language: he calls himself "extraordinarily lucky" when he has lost a
child, a job and nearly all his property, and he describes the survival of five
heads as inestimable blessings. In a genuine peace, none of this would be luck. The
title therefore does exactly what a good title should: it states the official word
for the situation and leaves the reader to discover what the word conceals.

**2.** Jonathan Iwegbu is a small man with an extraordinary capacity to begin again.
Achebe shows him almost entirely through action. He bribes an officer to keep his
bicycle and then buries it; he digs it up and has it earning money within days; he
repairs a ruined house with wire and cardboard; he abandons the coal mine as soon as
he sees the job will not return; he sets his wife and children to work; and when
armed thieves come, he gives up everything rather than risk a life. His faith is of
the same practical kind — "Nothing puzzles God" is less a doctrine than a refusal to
be paralysed by what he cannot control. Much of this is admirable: his energy,
independence and refusal of self-pity are exactly the qualities that rebuild a
country, and Achebe clearly respects them. But the story also leaves room for doubt.
Jonathan counts a dead son inside an arithmetic of blessings; he asks nobody for
justice; he loses his award to criminals and by morning has decided that it does not
matter. Endurance of that completeness may also be a kind of surrender, since a
society in which everybody shrugs will never demand anything better. Achebe does not
decide for us, and the best answers hold both views together.

**3.** Achebe's post-war Nigeria is drawn in a handful of exact details, and every
one of them tells us something. Physically, the country is broken: houses lie in
rubble, and Jonathan's flimsy zinc house survives when stronger ones did not, so
that survival looks arbitrary rather than deserved. Economically, it is in
collapse: the coal mine cannot say when it will reopen, the Biafran currency is
waste paper, and the government's answer is a flat twenty-pound award for everyone.
Whole families therefore live on tiny trades — mangoes, fried akara, palm-wine, a
bicycle taxi that earns its money carrying people to and from a military cemetery.
Socially, the most disturbing fact is the silence. The old protections have gone: no
police come, no soldiers come, and the neighbours who will arrive at dawn to
sympathise do not open a door at night. Violence has simply moved from the
battlefield into the street, and its new practitioners are polite, organised and
confident that nobody will stop them. Against all this Achebe sets the stubborn
industry of one family. The picture that results is neither hopeless nor
comfortable: people survive, but they survive alone, and the peace that has been
declared protects nobody.
:::

**Reference to the context**

1. "Nothing puzzles God."

   (a) Who says this, and when is it first said? (b) What does the speaker mean by
   it? (c) Where in the story is it repeated, and why is that placing important?
   (d) What does the line reveal about the speaker's character? <span class="marks">[5]</span>

2. "No Civil War again. This time na Civil Peace."

   (a) Who speaks these words, and to whom? (b) What is the situation at that
   moment? (c) Why is the sentence written in Pidgin English? (d) Explain the irony
   of the phrase and its link with the story's title. <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) The words are Jonathan Iwegbu's, and they are first heard at the very
beginning of the story, when he is counting the five "inestimable blessings" he has
brought out of the civil war — his own head, his wife Maria's, and those of three of
his four children. (b) He means that God's ways cannot be understood or questioned,
so that whatever happens, good or bad, has to be accepted without complaint. (c) The
same line closes the story, on the morning after the thieves have taken his entire
twenty-pound award, when the neighbours come to sympathise. Placing it at both ends
makes the story circular and shows that nothing has shaken him. (d) It reveals a man
whose religion is entirely practical. He does not use it to explain the world but to
avoid being destroyed by it; it is what allows him to stop grieving and start
working again, and it is also, less comfortably, what allows him to demand nothing
from anyone.

**2.** (a) They are spoken by the leader of the group of thieves, calling through the
door to Jonathan Iwegbu at night. (b) The thieves have knocked and asked politely
for the owner of the house; the family has screamed for neighbours, police and
soldiers, and nobody has come — the leader has just mocked them by shouting for the
police himself. He is now demanding a hundred pounds and assuring Jonathan that
nobody need be hurt. (c) Achebe writes the thieves' speech in Nigerian Pidgin
English because it is the real language of the street in that place and time. It
makes the man immediately believable, and its casual, almost friendly tone against
such a threat is far more frightening than shouting would be. (d) The irony is
complete: the word "peace" is spoken by an armed robber, and what he means by it is
only that he will not kill anyone if he is paid. It gives the story its title and
states its theme — that the end of the war brought ordinary people a new name for
their danger rather than safety from it.
:::

---
subject: Compulsory English
grade: 12
unit: 17
title: Human Rights and the Age of Inequality
hours: 3
area: Literature - Essays
---

Samuel Moyn's "Human Rights and the Age of Inequality" is the last essay in your
Grade 12 book and the hardest to read, because it argues instead of telling a
story. Moyn, a historian of law, asks a question that sounds rude: if human rights
have spread round the world since 1948, why has the gap between the rich and the
poor grown wider at the same time? His answer is that human rights were never
designed to close that gap. They promise everyone a *floor* to stand on; they say
nothing about a *ceiling* above which nobody may rise. This chapter explains the
argument one step at a time, gives you the key terms, and shows how to answer
every kind of question the board asks about it.

::: key The central idea
Human rights law and the human rights movement are good at two things: stopping
state cruelty (torture, censorship, political killing) and guaranteeing a
minimum of decent living. They are **not equipped to challenge inequality itself**.
Even "perfectly realized" human rights would leave huge differences of wealth
untouched. Moyn does **not** say human rights are bad or that they caused inequality;
he says they are the wrong tool for this job, so the job needs a **supplement**,
not a substitute. Every question on this essay comes back to that one sentence.
:::

## 17.1 About the author

Samuel Moyn (born 1972) is an American legal historian and intellectual historian.
He studied history and French literature at Washington University in St. Louis
(A.B., 1994), took a Ph.D. in history at the University of California, Berkeley
(2000) and a law degree (J.D.) at Harvard Law School (2001). He taught at Columbia
University for thirteen years and at Harvard for three, and since 2017 he has been a
professor at Yale, where he holds the Chancellor Kent Chair in Law and History.

```photo id="eng12/moyn" caption="Samuel Moyn lecturing at Queen's University Belfast School of Law, 2018." width="40"
crop 0.0 0.30 1.0 1.0
```

Moyn is best known for re-telling the history of human rights with a sceptical eye.
His main books are:

| Book | Year | What it argues |
|---|---|---|
| *The Last Utopia: Human Rights in History* | 2010 | Human rights as a mass movement are younger than people think; they rose in the 1970s after older political hopes had failed |
| *Christian Human Rights* | 2015 | The religious roots of the modern idea of rights |
| *Not Enough: Human Rights in an Unequal World* | 2018 | The book behind this essay: human rights and the growth of economic inequality |
| *Humane: How the United States Abandoned Peace and Reinvented War* | 2021 | How efforts to make war "humane" made it easier to keep fighting |
| *Liberalism Against Itself* | 2023 | Cold War thinkers and the shape of modern liberalism |

A shorter version of this essay was published on **27 October 2015** on the website
*OpenGlobalRights* under the title "Human rights and the age of inequality". The text
in your textbook is a longer form of the same argument and opens with an ancient
story about King Croesus, which is explained in section 17.3.

::: note Why the author matters for the exam
Examiners sometimes ask "Who is Samuel Moyn?" as a two-mark question. A safe answer:
*an American professor of law and history at Yale University, known for critical
studies of the history of human rights, such as* The Last Utopia *and* Not Enough.
:::

## 17.2 Background: the ideas you need before you read

The essay assumes you know seven things. Read this section first and the essay
becomes much easier.

### The Universal Declaration of Human Rights (UDHR)

On **10 December 1948** the General Assembly of the United Nations adopted the
Universal Declaration of Human Rights in Paris. It was drafted in the shadow of
the Second World War and the Holocaust by the UN Commission on Human Rights,
chaired by **Eleanor Roosevelt**. It lists basic rights of every person: life,
liberty, equality before the law, freedom of thought and expression, and also
social rights such as the right to education, work and a standard of living
adequate for health. **Human Rights Day** is celebrated every year on 10 December
to mark its adoption. Article 1 begins with the famous sentence that "all human
beings are born free and equal in dignity and rights".

```photo id="eng12/udhr-roosevelt" caption="Eleanor Roosevelt holding a poster of the Universal Declaration of Human Rights (in English), Lake Success, New York, November 1949." width="62"
```

### Status equality and distributive equality

These two phrases carry the whole essay.

| | Status equality | Distributive equality |
|---|---|---|
| Meaning | Everyone counts as an equal *person*: same dignity, same legal rights | Everyone holds a *similar share* of wealth and resources, or at least there is a limit to how large the gap may grow |
| Question it answers | "Are you a full human being in the eyes of the law?" | "How much do you own compared with others?" |
| Where it appears | Article 1 of the UDHR | Missing from the UDHR and from human rights law |
| Example | Abolishing slavery or caste discrimination | A tax system that narrows the gap between the richest and the poorest |

### Floor and ceiling

A **floor of protection** is a minimum everybody must be lifted to: enough food,
basic health care, schooling. A **ceiling on inequality** is a limit on how far
the top can pull away from the rest. A society can have a floor without a ceiling
(everyone eats, but a few own almost everything) or both together. Moyn's whole
point is that human rights give you the floor but never mention the ceiling.

```figure caption="A floor lifts the poorest (left); a ceiling also limits the richest (right). Grey bars are the starting incomes, blue bars the result. The numbers are invented to illustrate the idea, not real data."
import matplotlib.pyplot as plt
import numpy as np
fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.6), sharey=True)
orig = np.array([1, 2, 3, 5, 8, 14, 30])
x = np.arange(len(orig))
floor, ceil = 4, 12
a = np.maximum(orig, floor)
b = np.minimum(np.maximum(orig, floor), ceil)
for ax, vals, title in ((axes[0], a, 'Floor only'), (axes[1], b, 'Floor and ceiling')):
    ax.bar(x, orig, color=GRID, width=0.7)
    ax.bar(x, vals, color=ACCENT, width=0.7, alpha=0.85)
    ax.bar(x, orig, color='none', edgecolor=MUTED, width=0.7, lw=0.6)
    ax.axhline(floor, color=INK, ls='--', lw=0.9)
    ax.set_title(title, fontsize=8, color=INK)
    ax.set_xticks([])
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_ylim(0, 33)
axes[0].set_ylabel('Income (invented units)', fontsize=7, color=INK)
axes[0].text(-0.45, 6.4, 'floor', fontsize=7, color=INK)
axes[1].axhline(ceil, color='#A8271F', ls='--', lw=0.9)
axes[1].text(-0.45, 13.4, 'ceiling', fontsize=7, color='#A8271F')
axes[0].text(3.2, 30, 'the top is\nstill enormous', fontsize=6.5, color=INK, ha='center', va='top')
for ax in axes:
    ax.tick_params(labelsize=6.5)
fig.tight_layout()
```

### Welfarism and the welfare state

A **welfare state** is a state that protects citizens from the risks of market life:
unemployment, sickness, old age, accident. After the Great Depression of the 1930s
and the Second World War, nearly every Western government accepted this duty. Moyn
calls the agreement the **welfarist consensus**. Welfare states usually did more
than set a floor: they taxed high incomes, built public schools and hospitals, and
so narrowed the gap, which is why Moyn says they had a ceiling of a kind.

### Neoliberalism and market fundamentalism

**Neoliberalism** is the set of policies that became dominant from the 1970s:
cutting state spending on welfare, lowering taxes on the rich, privatising public
services and freeing markets. Moyn's own label for the same idea is **market
fundamentalism**: the belief that markets should be trusted to decide almost
everything. Politicians such as Margaret Thatcher in Britain and Ronald Reagan in
the United States are the best-known examples, though Moyn does not name them in
the short *OpenGlobalRights* text.

### The "global south"

An expression for the poorer countries of Latin America, Africa and Asia. Moyn
notes that these countries, freed from empire after 1945, tried to copy the
national welfare state but could not, and that the wealth gap between rich and
poor *countries* has lasted to this day.

### Croesus and Herodotus

**Croesus** was the last king of Lydia (an old kingdom in what is now western
Turkey), who ruled from about 585 BC until 546 BC. He was so rich that his name
became a proverb ("rich as Croesus"). **Herodotus**, the Greek historian of the
fifth century BC, tells his story in *The Histories*: the Athenian lawgiver
**Solon** visited Croesus, refused to call him the happiest of men, and warned
that nobody should be called happy before he is dead. Later the Persian king
**Cyrus the Great** defeated Croesus and took his kingdom.

```photo id="eng12/croesus-pyre" caption="Croesus on his funeral pyre, from a Greek red-figure amphora of about 500-490 BC (Louvre). Herodotus tells how Cyrus of Persia defeated Croesus and condemned him to the flames." width="56"
```

## 17.3 The essay, section by section

Moyn writes as a historian, so the essay follows time: from an old parable, through
the 1940s, to the present. Keep this outline in your head.

### Step 1 — Croesus's world

The textbook version opens with the parable of **Croesus**. Moyn asks us to imagine a
modern Croesus: a ruler fabulously wealthy, yet kind, who hates cruelty, insists
that nobody in his kingdom should starve, and so guarantees a "floor of protection".
Who could object to such a man? Moyn can, and does. A world in which one man owns
everything and treats everyone decently is still a world of extreme inequality.
Moyn's blunt claim is that **we now live in Croesus's world**: human rights fight
repression and misery, but they sit comfortably beside the most enormous inequality.

### Step 2 — What the Universal Declaration leaves out

Moyn says the value of **distributive equality**, "any ceiling on the wealth gap
between rich and poor", is "as absent from the Universal Declaration of Human
Rights, as it is from the legal regimes and social movements that take it as their
polestar". He quotes Philip Alston, the United Nations special rapporteur on
extreme poverty and human rights, who admitted that "there is no explicitly stated
right to equality, as such, under international human rights law."

Moyn is fair about what the Declaration did achieve. Its first article announced
**status equality**: every human being is "born free and equal in dignity and
rights". In a world "devastated by the evils of racism and genocide", he grants,
even that bare statement was "a revolutionary act". But status equality "implies
nothing more". He gives a famous thought experiment: one can "imagine one man
owning everything—an absolute overlord—and he would not violate the current scheme
of human rights, so long as everyone had their basic rights fulfilled". His
summary: "Even perfectly realized human rights are compatible with radical
inequality."

He adds that rights cost money and, especially economic and social rights such as
education and health care, have redistributive effects. But those effects belong to
a "more modest effort to build a floor of protection against indigence", not to "an
ambitious attempt to create a ceiling on inequality".

### Step 3 — The age of national welfare (1940s-1970s)

Moyn now gives the history. In the 1940s human rights were only "one version of the
update to the entitlements of citizenship" on which everyone agreed "after
depression and war". They were a modest, optional synonym for the **national
welfare state**.

His key example is **Franklin D. Roosevelt**. In his State of the Union address of
**January 1944**, the year before his death, Roosevelt called for a "second bill
of rights" covering jobs, health, housing and education. Everyone remembers the
slogan **"freedom from want"**. Moyn argues that people miss what Roosevelt's speech
really promised. The president's highest promise was not a floor for the masses but
the end of "special privilege for the few", which is nothing less than a **ceiling
on inequality**. Welfare states of that age aimed to make society "a more equal society than
before (or since)".

But there was a price. The happy marriage of a floor and a ceiling worked only
inside nations, "mostly North Atlantic states, and then only partially". The moment
human rights became global, the demand for local equality was dropped: "as if
globalization of the norms of basic protection were a kind of reward for the
relinquishment of the imperative of local equality."

Decolonisation, too, changed little. The new states of the global south adopted the
same national welfare ideal, but they could not make it work, and the wealth gap
between rich and poor countries endured.

### Step 4 — The turn to neoliberal globalisation (1970s onward)

Some hoped to take the welfare idea worldwide. The Swedish economist **Gunnar
Myrdal** believed it was possible, and the global south's 1970s call for a **New
International Economic Order** had the same spirit. Both failed. What arrived
instead, in historian Mark Mazower's bitter phrase, was "the real new international
economic order" of **global market fundamentalism**.

Moyn adds a famous irony: in 1974 the Nobel Prize in economics went jointly to
Myrdal and to his opponent **Friedrich Hayek**, but "where one of them was
forgotten, the other saw his fondest wishes come true." In the 1970s, "starting in
the United Kingdom and the United States", governments cut social provision and set
out "to destroy the national welfarist consensus".

The **human rights movement** adapted to this new climate. It prized the freedom of
the individual from harm, and a "rudimentary government that at best averted
disaster". The idea of a ceiling, which welfare states had already let slip, was
forgotten in human rights thinking. The floor went global; the ceiling vanished.

```figure caption="Moyn's story as a timeline. Through the heroic age of national welfare states, human rights were a modest companion of welfare; from the 1970s the economy went global and human rights became a global floor without a ceiling."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(1938, 2024); ax.set_ylim(-2.7, 2.7); ax.axis('off')
ax.add_patch(Rectangle((1940, -0.28), 35, 0.56, fc='#DCE6F7', ec='none'))
ax.add_patch(Rectangle((1975, -0.28), 46, 0.56, fc='#F7E4D6', ec='none'))
ax.text(1957.5, 0, 'Heroic age of\nnational welfare states', ha='center', va='center', fontsize=6, color=INK)
ax.text(1998, 0, 'Neoliberal globalisation:\nfloor, no ceiling', ha='center', va='center', fontsize=6, color=INK)
events = [
    (1944, 1, 'Jan 1944\nRoosevelt asks for a\n"second bill of rights"'),
    (1948, -1, '10 Dec 1948\nUniversal Declaration\nof Human Rights'),
    (1974, 1, '1974 Nobel Prize to\nMyrdal and Hayek;\nwelfare states retrenched'),
    (2015, -1, '27 Oct 2015\nMoyn publishes\nthe essay'),
]
for yr, side, label in events:
    top = 2.1 * side
    ax.plot([yr, yr], [0.28 * side, top * 0.78], color=MUTED, lw=0.8)
    ax.plot(yr, 0.28 * side, 'o', color=ACCENT, ms=4)
    ax.text(yr, top, label, ha='center', va='center', fontsize=6.2, color=INK, linespacing=1.3)
fig.tight_layout()
```

### Step 5 — Is another human rights movement needed?

The last section asks the question directly: "Could a different form of human
rights than the legal regimes and movements spawned so far correct this mistake?"
Moyn's reply is "I doubt it." He is at pains to add that this "is not to
contradict the moral significance and possibly even historical success of human
rights when it comes to their core uses in combating political repression and
restraining excessive violence."

He offers three reasons.

1. **History.** When inequality has been contained, it was never through the
   individualistic, "often anti-statist" approach that human rights share with
   their "market fundamentalist Doppelgänger". It was done by strong states, taxes
   and organised political movements.
2. **The tools do not fit.** The human rights movement's most famous weapons, which
   are to criticise state repression and to ease the disasters of war, "are simply
   not fit for use in the socioeconomic domain". Naming and shaming a government that
   tortures works; naming and shaming the rich for having too much does not.
3. **The wrong agents.** The movement is not up to the task, so it offers "no
   meaningful alternative, and certainly no serious threat, to market
   fundamentalism". Elsewhere he says socioeconomic rights have become "a helpless
   bystander of market fundamentalism".

He also heads off a misreading: "Unlike some Marxists, I think it is foolish to
blame human rights for the explosion of inequality in our time". In "a vulgar
formula," he says, "neoliberalism, not human rights, is to blame for neoliberalism."

His closing image is the man "who, lacking anything but a hammer, then treats
everything like a nail". Human rights have become so successful and famous that
people try to use them for every problem, including inequality. His conclusion:
"The drastic mismatch between the egalitarian crisis and the human rights remedy
demands not a substitute but a supplement." That is to say, keep human rights, but
add a separate politics that can actually make wealth move.

The Croesus story comes back at this point in the textbook version. In Herodotus,
Solon's wise words did not change Croesus; it was the army of Cyrus that ended his
world. Moyn's lesson is that **redistribution has always needed pressure strong
enough to frighten the rich, never polite appeals alone**. Exactly how to apply that
pressure today is a question the essay deliberately leaves open.

::: caution Study-guide mistakes to avoid
Several online guides repeat errors. Check them against the essay.

- Some say Moyn argues that "another human rights movement is required". He says the
  opposite: he **doubts** that any version of human rights can close the gap and
  asks for a **supplement**.
- Some say Moyn blames human rights for inequality. He calls that "foolish".
- The UDHR was adopted on **10 December 1948**. Roosevelt's "second bill of rights"
  speech was in **1944**; the UDHR was not his work, and Eleanor Roosevelt, not
  Franklin, chaired the UN commission that drafted it.
- "Status equality" and "distributive equality" are **not** the same thing. The first
  is in the UDHR; the second is missing from it.
:::

## 17.4 Central idea and themes

| Theme | How the essay shows it |
|---|---|
| **Limits of human rights** | The UDHR guarantees status equality and a floor, never a ceiling on wealth |
| **Inequality as the defining problem of our age** | Wealth gaps have exploded just as human rights became world-famous |
| **Floor versus ceiling** | The organising metaphor of the whole essay |
| **Power and pressure** | Real redistribution comes when the rich are afraid, as in the fall of Croesus |
| **History as explanation** | Moyn reads present problems through two eras: national welfare and neoliberal globalisation |
| **Honest scepticism** | He praises what human rights have done while insisting on what they cannot do |

**The argument as a chain of steps.** Moyn's essay is built like a proof:

1. Human rights promise a floor (status equality plus minimum protection).
2. They do not promise a ceiling (distributive equality).
3. They spread worldwide exactly when welfare states, which did have a ceiling, were
   being dismantled.
4. Their tools (law, reports, naming and shaming) suit political repression, not
   wealth.
5. Therefore they cannot be the main remedy for inequality; something else must add
   to them.

**Why the essay matters.** It is an essay of the 2010s, when economists and
politicians began to speak openly of "the age of inequality". For a student in
Nepal, which has promised citizens a long list of economic and social rights in its
2015 Constitution but still struggles with poverty and unequal opportunity, the
question is not remote: *is a right on paper the same as a fair share in life?*

## 17.5 Style, tone and form

**Form.** An **argumentative (analytical) essay**, part historical narrative, part
philosophical argument. It has a clear claim in the first paragraph, a chronological
middle and a conclusion that turns the claim into advice.

| Feature | Example | Effect |
|---|---|---|
| **Parable / allusion** | Croesus and Herodotus | Makes an abstract thesis memorable; adds the lesson that wise advice rarely beats power |
| **Metaphor** | "floor of protection", "ceiling on inequality" | One picture the reader can hold on to |
| **Thought experiment** | "one man owning everything—an absolute overlord" | Shows, in one image, that rights and inequality can coexist |
| **Irony** | The 1974 Nobel shared by Myrdal and Hayek: "one of them was forgotten, the other saw his fondest wishes come true" | Gives history a sting |
| **Proverbial metaphor** | "lacking anything but a hammer, then treats everything like a nail" | Hits the movement's over-confidence |
| **Loanword** | *Doppelgänger* (German: a ghostly double) | Suggests that human rights and market fundamentalism look alike |
| **Concession** | "I think it is foolish to blame human rights…" | Shows fairness and protects him against an easy reply |
| **Balanced contrast** | "not a substitute but a supplement" | Sums up the thesis in seven words |

**Tone.** Serious, scholarly, calm and somewhat ironic. Moyn is not angry; he is
diagnosing. Sentences are long and academic, so when you paraphrase, break them
into short plain ones.

**Point of view.** First person ("I doubt it", "I think") in the last section only;
the rest is impersonal exposition.

::: tip Naming the device correctly
If a question asks for the figure of speech in "a floor of protection without a
ceiling on inequality", the answer is **metaphor** (a building is used to picture
social policy). "Croesus's world" is an **allusion** and an **extended analogy**.
"Lacking anything but a hammer…" is a **proverbial metaphor**.
:::

## 17.6 Critical appreciation

**Strengths.** The essay is clear about its target and honest about its limits. The
floor/ceiling picture makes a difficult idea visible. It respects what human rights
have done for victims of torture and war, so the reader does not feel it is an
attack. It is well grounded in history: Roosevelt's speech, the Nobel shared by
Myrdal and Hayek, the collapse of the welfare consensus.

**Weaknesses and challenges.** A careful reader may say: (1) Moyn gives no
programme; he tells us what human rights *cannot* do but only hints at what *can*.
(2) The socioeconomic rights in some constitutions, including Nepal's, can be argued
in courts and do reduce hardship, so the "helpless bystander" charge may be too
strong. (3) The essay concentrates on the United States and Europe; much of the
world's experience of rights is left out. (4) Some human rights lawyers reply that
a floor itself is already a great achievement for people who had none.

**Relevance to Nepal.** The Constitution of Nepal (2015) lists rights to food,
health, education, housing, employment and social security beside civil and
political rights, and the National Human Rights Commission monitors them. Yet
differences of region, caste, gender and income remain wide. Moyn's question fits: a
right written in the Constitution is a floor; a fair society needs more than a
floor.

## 17.7 Glossary

| Word | Meaning as used here |
|---|---|
| **distributive equality** | fairness in how wealth and resources are shared, e.g. a limit on the gap between rich and poor |
| **status equality** | equal standing as persons before the law, regardless of wealth |
| **egalitarian** (adj.) | believing that all people should have equal rights and similar shares of resources |
| **indigence** (n.) | extreme poverty; lack of the basic needs of life |
| **abjection** (n.) | a wretched, hopeless condition of misery |
| **welfarism** (n.) | the policy that a state should protect its citizens from economic risk |
| **national welfare state** (n.) | a state that provides pensions, health care, education and jobs to its own citizens |
| **consensus** (n.) | general agreement among a group |
| **polestar** (n.) | a guiding principle (literally, the North Star) |
| **regime** (n.) | a system of rules, here the body of human rights law |
| **retrench** (v.) | to cut spending, especially on social services |
| **neoliberalism** (n.) | policy favouring free markets, low taxes on wealth and small government spending |
| **market fundamentalism** (n.) | an extreme faith that markets alone should decide how society is organised |
| **decolonisation** (n.) | the process by which colonies became independent states |
| **global south** (n.) | poorer countries of Latin America, Africa and Asia |
| **repression** (n.) | cruel control of people by force, e.g. by a government |
| **Doppelgänger** (n.) | a double or look-alike, often an eerie one |
| **mordantly** (adv.) | in a biting, sarcastic way |
| **supplement** (n.) | something added to complete or improve a thing, not to replace it |
| **utopia** (n.) | an imagined perfect society |
| **parable** (n.) | a short story that teaches a lesson |
| **egalitarian crisis** | a crisis caused by extreme inequality |

::: memory Five lines to carry into the exam
1. Human rights give a **floor**, not a **ceiling**.
2. UDHR: **10 December 1948**; Article 1 gives **status equality**.
3. Roosevelt, **1944**: "freedom from want" *and* an end to "special privilege for the few".
4. From the **1970s**, neoliberalism rose; human rights went global as welfare states retreated.
5. Moyn wants human rights **supplemented**, not substituted.
:::

## 17.8 Textbook exercises

The wording below follows the CDC Grade 12 textbook; printings and guides differ in
small details, so read the question carefully in your own copy.

**Understanding the text**

*a. What was the first United Nations declaration on human rights?*

It was the **Universal Declaration of Human Rights**, adopted by the United Nations
General Assembly on 10 December 1948. It was the founding document of the modern
human rights regime.

*b. When is Human Rights Day celebrated?*

On **10 December** every year, the anniversary of the day in 1948 when the General
Assembly adopted the Universal Declaration.

*c. What does the Universal Declaration of Human Rights aim to accomplish?*

It aims to set out, in one world document, the basic rights and freedoms that every
person has simply by being human: life, liberty, equality before the law, freedom of
thought, and social rights such as education and an adequate standard of living. Its
first article declares that all people are born "free and equal in dignity and
rights". Its purpose, in the words of its preamble, is to be the foundation of
freedom, justice and peace in the world.

*d. When writing the history of human rights in relation to the history of political
economy, what are the two major stages?*

The first is the **heroic age of national welfare states** after the Second World
War, from the 1940s to the 1970s, when human rights were only a modest companion
of the welfare state and welfare states set both a floor and, in practice, a
ceiling. The second is the age of **neoliberal globalisation** from the 1970s,
when political economy made "a scalar leap beyond the nation and towards the
globe", welfare states retreated, and human rights spread worldwide as a global
floor without a ceiling.

*e. What facts have been overlooked in Roosevelt's call for a "Second Bill of
Rights"?*

Three things are commonly missed. (1) His call for socioeconomic protections was
America's late, cautious entry into a welfare consensus already shared by the
countries of the North Atlantic. (2) His highest promise was not just a floor of
protection for the masses, but the end of "special privilege for the few", a
ceiling on inequality. (3) He hoped for "freedom from want" everywhere in the world,
but in practice the promise was carried out only nationally, mostly in North
Atlantic states and only partly.

*f. Write the truth that Herodotus tells in his stories.*

The lesson of Croesus's story is that the powerful rarely give way to advice alone.
Solon's warning to Croesus changed nothing; his world ended only when the Persian
army under Cyrus overthrew him. Moyn draws the parallel: global socioeconomic
justice, like local justice, would need redistribution from the rich to the poor
driven by pressure that the wealthy truly fear, which is not what the human rights
movement as we know it can provide.

*g. What is the significance of the Universal Declaration of Human Rights to you?*

This is an opinion question. A model: The Declaration matters to me because it tells
the world that every person, whatever his caste, sex, nationality or wealth, has
equal dignity and basic rights. It gives people like me a standard against which to
judge our own government, and it inspired many constitutions, including the rights
chapter of Nepal's own 2015 Constitution. Yet after reading Moyn, I also see that
it is only a beginning: dignity on paper has to be matched by fair chances in life.

**Reference to the context**

*a. Does the essay offer strategies for stigmatising inequality? Explain.*

Only in part. Moyn gives a **diagnosis** rather than a programme. He shows that the
human rights movement's usual method, "naming and shaming", works against
repression but not against wealth, and so it cannot stigmatise inequality
effectively. What he does offer is a direction: history shows that inequality has
been contained only by strong states, redistribution and organised political
pressure. He calls for "a supplement", a politics that can move wealth, but he
deliberately does not draw up its details. A good answer states both: no detailed
strategy, but a clear indication that strategy must be political and redistributive,
not merely legal and moral.

*b. Is a new movement for human rights required? Why?*

The essay answers "I doubt it". Moyn asks whether "a different form of human rights"
could correct the mistake and doubts it, because the human rights idea is
individualistic and often anti-statist, and because its chief tools, criticism of
state repression and relief of war, "are simply not fit for use in the
socioeconomic domain". So the need, he says, is not for another human rights
movement but for a different kind of politics that stands *beside* human rights as
"a supplement". If your paper words the question as "Is a new *kind* of movement
needed?", the answer is yes: a political movement for distributive equality, which
will not be a human rights movement.

**Reference beyond the text**

*a. What obstacles hinder the upkeep of human rights in Nepal?*

Model answer: Nepal's Constitution guarantees a long list of rights, but several
obstacles stand in the way. (1) **Poverty and inequality**: poor families, especially
in remote hills and the Terai, cannot reach health care and schools. (2) **Social
discrimination**: caste, gender and ethnic prejudice continue in practice though
illegal. (3) **Weak enforcement and corruption**: laws exist, but officials and
police sometimes ignore them and powerful people escape the courts. (4) **Low
awareness**: many people do not know their rights or how to claim them. (5) **Slow
justice**: delayed cases and scarce legal aid deny justice to the poor. Remedies
include free legal aid, better schools in villages, faster courts, a strong National
Human Rights Commission and civic education.

## Chapter summary

- Samuel Moyn (born 1972), professor of law and history at Yale, argues in "Human
  Rights and the Age of Inequality" that human rights are not equipped to fight
  global inequality.
- The Universal Declaration of Human Rights (10 December 1948; Human Rights Day)
  announced **status equality** (Article 1) but no ceiling on wealth, that is,
  **distributive equality**.
- Human rights give a **floor of protection** against extreme want; welfare states
  also gave a **ceiling** on inequality, as in Roosevelt's 1944 promise to end
  "special privilege for the few".
- From the 1970s neoliberalism, or "market fundamentalism", dismantled welfare
  states; human rights became global exactly when the demand for equality was
  dropped.
- The wealth gap between rich and poor countries outlasted decolonisation; Myrdal and
  Hayek shared the 1974 Nobel Prize, but only Hayek's wishes came true.
- Human rights remain valuable against repression and violence, but their tools
  (law, naming and shaming) do not fit economic inequality. Moyn does not blame
  human rights for inequality: "neoliberalism, not human rights, is to blame for
  neoliberalism".
- Conclusion: the "mismatch" demands "not a substitute but a supplement".
  Croesus's world and the lesson of Herodotus: redistribution needs real pressure.
- Devices: parable and allusion (Croesus), metaphor (floor/ceiling, hammer and
  nail), thought experiment (one man owning everything), irony, concession.

## Practice questions

**Short answer questions (2 marks each)**

1. Who is Samuel Moyn, and what is he best known for? <span class="marks">[2]</span>
2. What is the difference between status equality and distributive equality?
   <span class="marks">[2]</span>
3. What does Moyn mean by a "floor of protection" and a "ceiling on inequality"?
   <span class="marks">[2]</span>
4. Why does Moyn call the UDHR's first article "a revolutionary act"?
   <span class="marks">[2]</span>
5. What was Roosevelt's "highest promise" in his 1944 speech, according to Moyn?
   <span class="marks">[2]</span>
6. What irony does Moyn find in the 1974 Nobel Prize in economics?
   <span class="marks">[2]</span>
7. What does the hammer-and-nail image tell us about the human rights movement?
   <span class="marks">[2]</span>
8. Why does Moyn say a supplement, not a substitute, is needed?
   <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** Samuel Moyn is an American professor of law and history at Yale University. He is known for critical studies of the history of human rights, such as *The Last Utopia* (2010) and *Not Enough* (2018).

**2.** Status equality means everyone has the same standing and basic rights as a person, as in Article 1 of the UDHR. Distributive equality concerns how wealth is shared, including any limit on the gap between rich and poor. The UDHR has the first but not the second.

**3.** A floor of protection is a minimum standard of living, such as food, health care and schooling, that everyone must be raised to. A ceiling on inequality is a limit on how far the richest can rise above the rest. Human rights offer the floor but not the ceiling.

**4.** Because in a world "devastated by the evils of racism and genocide", proclaiming that every human being is born free and equal in dignity and rights was a bold break with the ideas that had justified those evils, even though it said nothing about how wealth should be shared.

**5.** It was not just a floor of protection for the masses but the end of "special privilege for the few", a ceiling on inequality, which Moyn says people overlook because they remember only "freedom from want".

**6.** Myrdal, who hoped to spread welfare worldwide, and Hayek, the champion of free markets, shared the prize; but Moyn says "where one of them was forgotten, the other saw his fondest wishes come true": market fundamentalism won.

**7.** Human rights have become so successful that people use them as the tool for every problem, like a man who has only a hammer and treats everything like a nail. The image warns that rights are not suited to reduce inequality.

**8.** Because human rights law works well against repression and violence and Moyn does not want to throw that away; what is missing is a separate political force for redistribution that can stand beside rights. So a supplement is needed, not a replacement.
:::

**Long answer questions (5 marks each)**

1. Explain Moyn's argument that human rights are "not equipped to challenge global
   inequalities". <span class="marks">[5]</span>
2. How does Moyn trace the history of human rights in relation to political economy?
   <span class="marks">[5]</span>
3. "The Croesus story is more than a decoration; it carries the argument of the
   essay." Discuss. <span class="marks">[5]</span>
4. Do you agree with Moyn that human rights need a supplement rather than a
   substitute? Give reasons with reference to Nepal. <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** Moyn's claim is that human rights law and movements aim at a **floor**, not a **ceiling**. The UDHR announced status equality ("born free and equal in dignity and rights"), but it does not mention distributive equality, any limit on the wealth gap between rich and poor. As Moyn puts it, one could "imagine one man owning everything" and still not break the current scheme of human rights, provided everyone's basic rights were met; so "even perfectly realized human rights are compatible with radical inequality."

Second, the tools of the movement do not fit the task. Its best campaigns, criticism of state repression and relief of war, use law, reports and public shaming. These work against a government that tortures; they are "simply not fit for use in the socioeconomic domain", where the question is how money is distributed. Third, history shows that inequality has been contained by strong states and political movements, not by an individualistic rights approach that human rights share with their "market fundamentalist Doppelgänger". For these reasons human rights have been "a helpless bystander" while inequality exploded. Moyn does not blame rights for this, but he says something else must be added.

**2.** Moyn uses two stages. In the **first**, the heroic age of national welfare states (1940s-1970s), human rights were a modest, optional synonym for the welfare consensus reached "after depression and war". Roosevelt's 1944 call for a "second bill of rights" promised "freedom from want" and, more importantly, the end of "special privilege for the few", a ceiling. This worked only within nations, mostly in the North Atlantic. Even decolonisation left the wealth gap between rich and poor nations.

In the **second** stage, from the 1970s, the economy went global. Politicians in Britain and America dismantled welfare states; the dream of a global welfare order (Myrdal, the New International Economic Order) died; Hayek's market fundamentalism won. Human rights became global, but only as "a floor of protection without a ceiling on inequality". Moyn's pattern: human rights went international at the same moment as the demand for equality retreated. The irony that the floor went global while the ceiling vanished is the core of his history.

**3.** The essay begins with Croesus, the very rich, benevolent king of Lydia. Moyn asks us to picture a modern Croesus who hates cruelty and insists on a floor of protection for his subjects. The story does three jobs. (1) It makes his thesis concrete: a kind world can still be wildly unequal, and we live, in Moyn's phrase, in Croesus's world. (2) It shows that protection without limits on wealth leaves power untouched. (3) It returns at the end with the lesson from Herodotus: Solon's moral advice did not change Croesus; his world ended when Cyrus's army came. The suggestion is that redistribution has always come from pressure that the rich fear, not from polite persuasion or naming and shaming. So the parable is the essay's argument in miniature: the figure (Croesus), the moral remedy that fails (Solon) and the real remedy (power).

**4.** Moyn says human rights cannot close the wealth gap, so they need a supplement: a politics of redistribution with the power to frighten the privileged. I agree. Human rights are valuable: they protect people from torture, censorship and arbitrary arrest, and many Nepalis rely on the rights in the 2015 Constitution and on the National Human Rights Commission. But rights alone do not make a poor child in Karnali as likely to get a good school as a child in Kathmandu. Fair tax systems, public schools and hospitals, land reform, and strong trade unions and citizens' groups are political, not just legal, instruments. Nepal's own history shows that change came when organised movements pressed the state. At the same time I would not discard rights, as Moyn also says. So the right view is **both**: keep human rights as the floor and build a separate politics for fairness above it.
:::

**Reference to the context**

1. "Even perfectly realized human rights are compatible with radical inequality."

   (a) Who says this, and in which essay? (b) What thought experiment leads to this
   sentence? (c) What does "radical inequality" mean here? (d) Why does this sentence
   matter for the whole argument? <span class="marks">[5]</span>

2. "The drastic mismatch between the egalitarian crisis and the human rights remedy
   demands not a substitute but a supplement."

   (a) What is the "egalitarian crisis"? (b) What is "the human rights remedy"?
   (c) What is the difference between a substitute and a supplement? (d) Why is
   this the conclusion of the essay? <span class="marks">[5]</span>

3. "...the man who, lacking anything but a hammer, then treats everything like a
   nail."

   (a) To whom does this image refer? (b) What proverb does it resemble? (c) What
   mistake does it describe? (d) What does Moyn think should be done? <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) Samuel Moyn, in "Human Rights and the Age of Inequality". (b) The thought experiment of a world where "one man" owns everything, "an absolute overlord": even then the scheme of human rights would not be broken so long as everyone's basic rights were fulfilled. (c) A huge gap of wealth and power between the top and the rest; the phrase shows that rights permit it so long as a floor of protection exists. (d) It sums up his whole thesis: human rights aim at a floor, not a ceiling, so they cannot be the tool to fight inequality.

**2.** (a) The crisis of vast and growing inequality between rich and poor, within and between countries. (b) The response of the human rights movement and law: declarations, legal rights, reports and naming and shaming. (c) A substitute would replace human rights; a supplement would be added to them and leave them in place. (d) It is where the argument ends: human rights remain valuable against repression but need a separate politics of redistribution beside them.

**3.** (a) The human rights movement, whose success has led people to use it for every problem. (b) The saying "If all you have is a hammer, everything looks like a nail." (c) Over-reliance on one familiar tool, here using human rights law and advocacy against inequality, where they do not fit. (d) Keep human rights for what they do well, and add other political approaches that can actually cause redistribution.
:::

**Reference beyond the text**

1. "Rights on paper are not the same as fairness in life." Discuss with examples from
   Nepal. <span class="marks">[5]</span>
2. Write a paragraph on how the gap between rich and poor can be narrowed in your
   country. <span class="marks">[5]</span>

::: note Answer hints — reference beyond the text
**1.** Begin with the thesis: a right is a promise; fairness needs resources and institutions. Give three examples: the right to free basic education, yet children leave school because of poverty; equality before the law, yet caste or gender discrimination persists; the right to health, yet no hospital within a day's walk. Conclude that a right is a floor and policy must also narrow the gap.

**2.** Suggest progressive taxes, well-funded public schools and health posts in remote districts, land and housing programmes, employment and skills training, transparent governance, and strong civic movements. End with Moyn's insight that change needs political pressure, not just good laws.
:::

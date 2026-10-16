---
subject: Compulsory English
grade: 8
unit: 15
title: Conservation of Earth / An Official Notice
hours: 0
area: Units
---

The first text is an **argumentative essay** about the environment: it takes a
position, gives reasons for it, answers the obvious objection, and asks for
something. The second is an **official notice** — a short, formal, public
announcement issued by an office. They need the same equipment in different
proportions: the essay needs **connectives** that show reason, purpose and
contrast, and the notice needs a layout that cannot be mistaken.

::: key What this unit asks for
By the end you should be able to (1) write an argumentative essay with a clear
position and two or three supported reasons, (2) write an official notice in the
correct form, (3) use connectives of reason (*because, since, as*), purpose
(*to, in order to, so that, so as not to*) and contrast (*but, however,
although, whereas, on the other hand*), and (4) use commas where they are
required.
:::

## 15.1 Conservation of Earth

### About the text

The text is an **argument**. It does not merely describe pollution; it claims
that something must be done, gives the reasons, and calls for action. An
argument has four parts, and an examiner looks for all four:

| Part | What it does | Typical opening |
|---|---|---|
| Position | states what the writer believes | "The earth's resources are not unlimited." |
| Reasons | gives two or three reasons, each with evidence | "First, … Second, … Third, …" |
| Counter-argument | admits the other side, then answers it | "Some say … However, …" |
| Call to action | says what should happen, and by whom | "Therefore every school should …" |

### What the text says

**Position.** The earth's air, water, soil and forests have limits. They are
being used faster than they can renew themselves, and the cost is already being
paid by the poorest people, who depend most directly on the land.

**Reason 1 — consumption.** The richest part of the world uses far more than its
share of energy and materials. Every tonne of fuel burnt puts carbon dioxide
into the atmosphere, where it traps heat, and the average global temperature is
already about 1.1 °C above the pre-industrial level. The people who suffer most
from floods, landslides and erratic rain in Nepal contributed least to those
emissions.

**Reason 2 — loss of forests and biodiversity.** Forest is cut for timber,
firewood and new building land. A forest does more than store carbon: it holds
the soil on slopes, recharges the springs, and shelters a share of the world's
species. When it goes, the slope fails, the stream dries and the species go with
it.

**Reason 3 — waste.** Plastic, chemical fertiliser and sewage reach the rivers.
Plastic does not rot; it breaks into smaller and smaller pieces, and it is now
found in the stomachs of fish and birds and in the water we drink.

**Counter-argument.** Some say that poorer countries cannot afford conservation
while their people need development, and that rich countries should act first
and pay the bill. The argument grants the point — the largest historical
emitters do owe a debt — but answers it: conservation is not the opposite of
development. It is what protects the soil, the water and the forest on which
Nepal's farms and tourism depend. Development that destroys its own base cannot
last.

**Call to action.** Governments must enforce limits on emissions and on waste.
Businesses must count what they take and what they throw away. Schools must
teach conservation by practice, not only by slogan: tree planting, waste
segregation, water saving, and a school forest or wetland patch kept by the
students themselves. And every household can do three things today: refuse
single-use plastic, segregate waste, and plant something that will still be
alive in twenty years.

```figure caption="How an argument is built. The counter-argument is not a weakness: an essay that never mentions the other side has not yet considered the question."
fig, ax = plt.subplots(figsize=(4.9, 2.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")
blocks = [("Position", SERIES[0]), ("Reason 1", SERIES[1]),
          ("Reason 2", SERIES[2]), ("Reason 3", SERIES[3]),
          ("Counter-\nargument", SERIES[4]), ("Call to\naction", ACCENT)]
for i, (name, colour) in enumerate(blocks):
    x = 0.3 + i * 1.6
    ax.add_patch(plt.Rectangle((x, 2.6), 1.4, 1.3, fc="white", ec=colour, lw=1.4))
    ax.text(x + 0.7, 3.25, name, ha="center", va="center", fontsize=5.9, color=INK)
    if i < len(blocks) - 1:
        ax.annotate("", xy=(x + 1.6, 3.25), xytext=(x + 1.38, 3.25),
                    arrowprops=dict(arrowstyle="->", color=GRID, lw=1.1))
ax.text(5.0, 1.6, "each reason needs evidence; the conclusion must ask for something",
        ha="center", fontsize=6.1, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| conservation | protecting nature from damage or loss |
| consumption | the using up of goods, energy or materials |
| emission | a gas sent out into the air |
| biodiversity | the variety of living things |
| renewable | able to be replaced by nature in a short time |
| segregate | to separate one kind of thing from another |
| sustainable | able to continue without destroying what it depends on |

::: note Model answers
**1. What is the writer's position in this essay?**
That the earth's resources are limited and are being used faster than they can
renew, so conservation is necessary — and that conservation protects the soil,
water and forest on which development itself depends.
**2. How does the essay answer the argument that poor countries cannot afford
conservation?**
It admits that the largest historical emitters owe the largest debt, and then
points out that conservation is not opposed to development: a country that
destroys its soil, water and forest destroys the base of its own farming and
tourism, so development without conservation cannot last.
:::

## 15.2 An Official Notice

### About the text

An **official notice** is a short public announcement issued by a school, an
office, a hospital, a municipality or a company. Like any announcement it must
answer what, where, when, who and what to do — but it uses formal, impersonal
language and it is signed by the office that issued it, not by a person alone.

### The form of an official notice

| Line | Example |
|---|---|
| Name of the office, at the top | **SHREE JANATA SECONDARY SCHOOL, DHADING** |
| The word NOTICE, centred | **NOTICE** |
| Reference number and date | Ref. No. 078/079-14, dated 5 Bhadra 2082 |
| Subject line | **Subject: Closure of the school for Dashain** |
| Body — the information, in short formal sentences | All classes of this school will remain closed from … to … . The school will reopen on … . |
| Action required | Students must collect their holiday assignments from their class teachers before … . |
| Signature block | By order of the Principal, (name), Principal |

An official notice does not use *Dear*, does not use *please come*, and does not
end with *Yours faithfully*. It is written in the third person and often in the
**passive** (*will remain closed*), because the office is not addressing one
person but the public.

::: caution The three commonest errors in a notice
1. Leaving out the **dates**. A closure notice without a reopening date is
   useless.
2. Mixing the formal and the informal register — *"Hi everyone, school band hai"*
   in an official notice.
3. Forgetting the **signature block**. A notice without the office's name and
   the date carries no authority.
:::

## 15.3 Grammar and writing tasks of the unit

### Grammar: Connectives of reason, purpose and contrast

| Purpose | Connectives | Example |
|---|---|---|
| Reason | because, since, as, because of + noun, due to + noun | **Because** the forest was cut, the spring dried. |
| Purpose | to + verb, in order to + verb, so as to + verb, so that + clause | We plant trees **in order to** hold the soil. |
| Contrast | but, however, although, though, even though, whereas, while, on the other hand | **Although** it rained, the stream stayed dry. |
| Result | so, therefore, as a result, consequently | The slope failed; **as a result**, the road closed. |
| Addition | and, moreover, in addition, besides, also | **Moreover**, plastic does not rot. |

*Because* takes a clause; *because of* takes a noun: *because it rained* /
*because of the rain*. *Although* takes a clause and no *but*: *Although it
rained, we went* — never *Although it rained, but we went*.

### Grammar: Commas

Use a comma (1) between items in a list, (2) after an introductory phrase or
clause, (3) before *but*, *so* and *yet* when they join two full sentences, and
(4) around a non-defining relative clause. Do not use a comma between a subject
and its verb, and do not join two full sentences with only a comma.

::: example Worked example
**Punctuate.** *although the school was closed we continued our tree planting
because the monsoon had begun so the saplings would live*
**Answer.** *Although the school was closed, we continued our tree planting
because the monsoon had begun, so the saplings would live.*
:::

### Writing: An argumentative essay and an official notice

For the essay, use the four-part shape. For the notice, use the seven-line
form. Both are marked more for their **structure** than for their vocabulary:
the examiner is looking for the shape first and the grammar second.

::: note Model answers to the practice questions
**Notice model.** SHREE JANATA SECONDARY SCHOOL, DHADING — **NOTICE** — Ref.
No. 078/079-14, dated 5 Bhadra 2082 — Subject: Closure of the school for
Dashain — All classes of this school will remain closed from 10 to 17 Bhadra
2082 on the occasion of Bada Dashain. The school will reopen on 18 Bhadra 2082
at the usual time. Students must collect their holiday assignments from their
class teachers before 9 Bhadra. By order of the Principal, (name), Principal.
:::

## 15.4 The language of persuasion

Writing about conservation means asking someone to **act**. Four tools do most
of the work.

| Tool | How it sounds | Example |
|---|---|---|
| Evidence | numbers, named places | *Nepal's forest cover rose from 39 % to about 45 % under community forestry.* |
| Modal verbs | obligation, possibility | *Every household **should** separate its waste; a village **can** compost its own leaves.* |
| Imperatives | direct call to act | *Plant one tree. Keep it alive.* |
| Cause and effect | consequences made visible | *Because the slope was cleared, the spring below it dried within three years.* |

```figure caption="Nepal's forest cover over three decades (approximate figures). The rise after community forestry began is one of the strongest conservation arguments available to a Nepali student."
yrs = ["1994", "2004", "2014", "2024"]
cover = [39, 39.6, 44.7, 45.3]
fig, ax = plt.subplots(figsize=(4.7, 2.8))
ax.plot(yrs, cover, color=SERIES[1], marker="o", markersize=5.5, linewidth=2.2)
ax.fill_between(range(len(yrs)), cover, color=SERIES[1], alpha=0.14)
for i, v in enumerate(cover):
    ax.text(i, v + 0.5, f"{v}%", ha="center", color=INK, fontsize=8.6)
ax.set_ylim(36, 48)
ax.set_ylabel("forest cover (% of land)", color=MUTED, fontsize=9)
ax.grid(axis="y", color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED, labelsize=8.4)
```

::: note Activity — the two-minute campaign
In groups of four, choose one problem in your school or ward: waste, a dried
spring, plastic in the river, a bare slope. Prepare a two-minute spoken
campaign with: one number, one local example, one thing you ask the listener to
do this week, and one thing you will do yourselves. Deliver it to the class;
the class votes on which campaign they would actually join, and says why.
:::

::: example Notice and essay from the same facts
**As a notice (for the board).**
> **NOTICE** — *All students are informed that waste will be separated from
> Sunday. Two bins will be placed in every corridor: green for kitchen and
> garden waste, blue for paper, plastic and glass. Class monitors will keep the
> weekly record. — Coordinator, Eco Club, 5 Asar*

**As an essay opening.**
> *Our school throws away about forty kilograms of waste a week, and almost
> half of it is vegetable peel that could be compost by next month. Separating
> waste is not an environmental slogan; it is a change of two bins and one
> habit.*

Same facts, two jobs: a notice tells people **what will happen**; an essay
argues **why it should**.
:::

## Chapter summary

- An argumentative essay has four parts: position, reasons with evidence,
  counter-argument and call to action.
- The main environmental problems in the text are over-consumption and
  emissions, the loss of forest and biodiversity, and waste.
- Conservation is not the opposite of development: it protects the soil, water
  and forest that farming and tourism depend on.
- An **official notice** names the office, carries the word NOTICE, a reference
  number and date, a subject line, the information, the action required and a
  signature block.
- **Reason:** because, since, as; *because of* + noun.
- **Purpose:** to, in order to, so as to, so that + clause.
- **Contrast:** but, however, although, whereas, on the other hand. Never pair
  *although* with *but*.
- Commas separate list items, follow an introductory clause, and precede *but*
  and *so* between full sentences.

## Practice questions

**Reading**

1. What is the writer's position and what is the call to action? <span class="marks">[3]</span>
2. Give three reasons the essay offers for conserving the earth. <span class="marks">[3]</span>
3. What is an official notice and how is it different from an ordinary
   announcement? <span class="marks">[2]</span>
4. Why does an official notice use the passive voice? <span class="marks">[1]</span>

::: note Answers
**1.** Position: the earth's resources are limited and are being used faster
than they renew, and people already suffer the cost. Call to action: governments
must enforce limits, businesses must account for what they take and throw away,
schools must teach conservation by practice, and households should refuse
single-use plastic, segregate waste and plant trees.
**2.** Over-consumption and emissions; loss of forest and biodiversity; waste
reaching the rivers.
**3.** A short formal public announcement issued by an office. It is impersonal,
written in the third person, signed by the office with a reference number and
date, and it does not greet or thank anybody.
**4.** Because the office speaks to the public rather than to one person, so the
subject of the sentence is the action, not the actor — "the school will remain
closed".
:::

**Grammar**

5. Join each pair with the connective given. <span class="marks">[5]</span>
   (a) The spring dried. The forest was cut. (because)
   (b) We plant trees. We want to hold the soil. (in order to)
   (c) It rained heavily. The match was not cancelled. (although)
   (d) Plastic is cheap. It does not rot. (however)
   (e) The road was blocked. We reached late. (as a result)

::: note Answers
**5.** (a) The spring dried because the forest was cut. (b) We plant trees in
order to hold the soil. (c) Although it rained heavily, the match was not
cancelled. (d) Plastic is cheap; however, it does not rot. (e) The road was
blocked; as a result, we reached late.
:::

**Writing**

6. Write an argumentative essay of about 200 words on why your school should
   start a waste-segregation programme. <span class="marks">[5]</span>
7. Write an official notice from your school about a tree-planting programme
   next Saturday. <span class="marks">[5]</span>

::: note Answers
**6.** Paragraph 1: state the position plainly. Paragraph 2: two reasons with
evidence — for example the volume of waste the school produces and the cost of
disposing of it mixed. Paragraph 3: admit the objection (time, space, habit) and
answer it. Paragraph 4: say exactly what should happen, by whom and by when.
**7.** Use the seven-line form: office name, NOTICE, reference number and date,
subject line, the information (what, where, when, who), the action required
(bring gloves and a spade, report at 7 a.m.), and the signature block.
:::

**Extra practice**

**Group B (2 marks each)**

**11.** Rewrite with a modal verb of obligation: *Separating waste is necessary.*
**12.** Write one cause-and-effect sentence about deforestation.

**Group C (4 marks)**

**13.** Write an essay of about 150 words on *Conservation of the Earth Begins at
    Home*.

::: note Extra practice — answers
**11.** *Every household should separate its waste.*
**12.** e.g. *Because the slope above the village was cleared for firewood, the
monsoon rain carried the topsoil away and the spring below dried up.*
**13.** Marks: an introduction that states the claim; a body with concrete
household actions (separate waste, compost, refuse single-use plastic, repair
leaking taps, LED lamps, plant and water a sapling, walk or cycle short
distances); at least one number or named local example; a counter-point
acknowledged (one household alone changes little) and answered (habits scale
through a community); and a short, specific conclusion.
:::

---
subject: Compulsory English
grade: 11
unit: 4
title: The Wish
hours: 3
area: Literature — Short Stories
---

Roald Dahl's "The Wish" is barely a thousand words long and almost nothing happens
in it. A small boy, alone in the hall of his house, invents a game on the patterned
carpet: the black parts are snakes, the red parts are burning coals, and only the
yellow is safe. Within a page the game has stopped being a game. The story is on
the syllabus because it shows how suspense is built out of ordinary materials, and
how an ending can frighten a reader most by refusing to say what happened.

::: key The central idea
Nothing in the story is dangerous. A carpet is a carpet. The terror is entirely
produced by the boy's imagination — and Dahl makes the reader share it, which is
his whole point about how imagination works.
:::

## 4.1 About the author

Roald Dahl (1916–1990) was a British writer, born in Llandaff, Cardiff, in Wales,
to Norwegian parents; he was named after the explorer Roald Amundsen. His father
and elder sister died when he was three. He chose not to go to university, joined
the Shell Oil Company and was posted to East Africa, and when the Second World War
began he became a fighter pilot in the Royal Air Force. He was badly injured when
his plane crashed in the Libyan desert in 1940 — an accident he later wrote about,
and which left him with pain for the rest of his life. Posted to Washington, he
began writing there almost by chance.

Dahl's career has two halves. For adults he wrote short stories with cruel, exact
twist endings, collected in *Someone Like You* (1953) — which contains "The Wish"
— and *Kiss Kiss* (1960); many were later filmed for the television series *Tales
of the Unexpected*. For children he wrote some of the most widely read books of the
twentieth century: *James and the Giant Peach* (1961), *Charlie and the Chocolate
Factory* (1964), *Fantastic Mr Fox* (1970), *Danny the Champion of the World*
(1975), *The BFG* (1982), *The Witches* (1983) and *Matilda* (1988). He worked in a
small hut in the garden of his house at Great Missenden in England, and died in
1990.

::: definition Macabre
Having death, injury or horror as its subject, and treating it with a disturbing
kind of enjoyment. Dahl's adult stories are usually described as macabre.
:::

What is distinctive about Dahl's voice is its coolness. He writes in plain,
short, concrete sentences and never tells you how to feel. He is unusually good at
describing physical sensation — texture, temperature, the feel of skin — and at
using an ordinary domestic object as the source of fear. Above all, he takes
children seriously: in his work a child's inner life is not charming but intense
and often frightening, and adults are absent exactly when they are needed.

## 4.2 The story

**A boy alone.** A small boy is sitting by himself at the foot of the staircase in
the hall of his house. No adult is with him; the reader is never told his name, or
the name of anyone else. He is picking at a scab on his knee — a half-healed
injury whose crust has gone hard at the edges. He works it loose carefully, lifts
it off whole, and looks with satisfaction at the clean pink skin underneath before
flicking the scab away. It is a small, private, slightly disgusting pleasure, and
it tells us at once what sort of child this is: solitary, curious, absorbed, and
perfectly happy to be interested in something a little horrible.

**The rules of the game.** Then he looks at the carpet. It is very large, stretching
from the bottom stair across the hall to the front door, and it is patterned in
three colours: red, black and yellow. Out of that pattern he builds a world. The
black patches become poisonous snakes — adders "mostly, and cobras, thick like
tree-trunks", as Dahl puts it — lying coiled and alive; the red patches become
red-hot lumps of coal; and only the yellow is safe ground. The rules are absolute:
touch black and the snakes will bite him and he will be dead before teatime; touch
red and he will be burnt. Then he sets his own prize, and it is the detail that
makes the story ache — if he can cross the whole carpet without one mistake, he
will be given a puppy for his birthday, which is tomorrow.

**The crossing begins.** He takes off his slippers and starts. The first steps are
easy: he places one foot on a yellow patch near the stairs and then another,
arms held out sideways for balance. But the yellow patches are irregular — some
broad, some no more than a narrow strip — so that he must go slowly, measure each
step, sometimes stand on tiptoe and sometimes balance on one foot while he decides
where the next safe place is.

**The game becomes real.** This is the part of the story that matters, and Dahl
does it by very small degrees. The boy begins to *see* the snakes rather than
imagine them: they seem to stir, to lift their heads, to be watching him and
waiting for a single false step. The red begins to look hot. His breathing changes;
he starts to feel dizzy and afraid. He is no longer a child playing on a carpet, and
Dahl never tells us so directly — we learn it from the boy's body, which behaves
exactly as a frightened body does.

**The last stretch.** More than half-way across, he comes to the obstacle he has
been dreading. A wide band of black lies right across his route, and the nearest
yellow beyond it is very far away — too far for an ordinary step. He has no choice
but to attempt an enormous stride: one foot planted on the yellow behind him, the
other swung out as far as it will go, his whole body stretched over the black.

**The fall.** He gets the toes of his leading foot down on the far side, but cannot
bring his weight across. For a moment he hangs, balanced on nothing, arms whirling
round like the sails of a windmill as he fights to stay upright. Then the balance
goes, and to save himself his hand comes down — flat on the black. Dahl gives the
result in one short, terrible paragraph: the boy screams, and the snakes come.

**The last sentence.** The story does not stay with him. In a single closing line
it moves right outside the house, to the garden and the sunshine, where "his mother
was searching for him". Nothing more is said. Dahl does not tell us whether the boy
is hurt, terrified, unconscious or gone; he simply changes the camera angle and
stops. The distance of that final sentence — warm daylight, an ordinary parent, a
child who cannot be found — is the most frightening thing in the story.

```figure caption="The boy's route across the hall carpet. The rules he invents make two-thirds of the floor lethal; the wide black band near the far side forces the stretch he cannot complete."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,3.3))
COLS, ROWS = 12, 5
YEL, RED, BLK = '#efd25e', '#d9534f', '#2b2f38'
path = [(0,2),(1,2),(2,1),(3,1),(4,2),(5,2),(6,3),(7,3),(8,2),(11,2)]
safe = set(path) | {(1,4),(4,0),(7,0),(9,4),(11,4),(2,3),(10,0)}
rng = np.random.default_rng(7)
for c in range(COLS):
    for r in range(ROWS):
        if (c,r) in safe:
            col = YEL
        elif 9 <= c <= 10 and 1 <= r <= 3:
            col = BLK
        else:
            col = BLK if rng.random() < 0.5 else RED
        ax.add_patch(Rectangle((c,r),1,1,fc=col,ec='white',lw=0.8))
px = [c+0.5 for c,r in path]; py = [r+0.5 for c,r in path]
ax.plot(px[:-1],py[:-1],color='white',lw=2.6,zorder=3)
ax.plot(px[:-1],py[:-1],color=ACCENT,lw=1.6,ls='--',zorder=4)
ax.plot(px[:-1],py[:-1],'o',color=ACCENT,ms=3.6,zorder=5)
ax.annotate('', xy=(px[-1],py[-1]), xytext=(px[-2],py[-2]),
            arrowprops=dict(arrowstyle='-|>',color='white',lw=2.6,
                            mutation_scale=13,shrinkA=0,shrinkB=0),zorder=3)
ax.annotate('', xy=(px[-1],py[-1]), xytext=(px[-2],py[-2]),
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.4,ls='--',
                            mutation_scale=11,shrinkA=0,shrinkB=0),zorder=4)
ax.plot([10.5],[2.5],marker='X',color='white',ms=11,zorder=6)
ax.plot([10.5],[2.5],marker='X',color='#ffd400',ms=8,zorder=7)
ax.annotate('he starts at\nthe bottom stair',(0.5,2.5),xytext=(-0.6,2.5),
            textcoords='data',ha='right',va='center',fontsize=7.4,color=INK,
            linespacing=1.4,
            arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8,shrinkA=2,shrinkB=3))
ax.annotate('the far side:\na puppy tomorrow',(11.5,2.5),xytext=(12.6,2.5),
            textcoords='data',ha='left',va='center',fontsize=7.4,color=INK,
            linespacing=1.4,
            arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8,shrinkA=2,shrinkB=3))
ax.annotate('the long stretch — his\nhand comes down on black',(10.5,2.5),
            xytext=(10.5,-0.75),textcoords='data',ha='center',va='top',
            fontsize=7.4,color='#A8271F',linespacing=1.4,
            arrowprops=dict(arrowstyle='-|>',color='#A8271F',lw=0.9,
                            mutation_scale=9,shrinkA=3,shrinkB=3))
for i,(col,lab) in enumerate([(YEL,'yellow = safe'),(RED,'red = burning coals'),
                              (BLK,'black = poisonous snakes')]):
    x0 = [-3.2, 3.2, 10.0][i]
    ax.add_patch(Rectangle((x0,-2.5),0.6,0.6,fc=col,ec=MUTED,lw=0.6))
    ax.text(x0+0.85,-2.2,lab,ha='left',va='center',fontsize=7.4,color=INK)
ax.set_xlim(-5.0,17.4); ax.set_ylim(-3.0,5.3)
ax.axis('off')
```

## 4.3 Characters

| Character | Who they are | Role in the story |
|---|---|---|
| The boy | A small, unnamed child, alone in the hall; his birthday is tomorrow | The only real character; everything is seen through his mind |
| The mother | Unnamed; appears only in the final sentence, outside in the sunshine | Represents the ordinary adult world, arriving too late and in the wrong place |
| The snakes and coals | The black and red patches of the carpet | An antagonist that exists only in the boy's imagination — and is therefore unbeatable |

**The boy.** Dahl tells us almost nothing about him — no name, no age, no
description of his face — and yet he is completely alive on the page, because we
are given his attention rather than his appearance. Three things define him. First,
he is *alone*: there is no adult in the house's hall, nobody to laugh at the game or
to call him for tea. Second, he is *imaginative to an unusual degree*: he does not
merely pretend that the black is snakes, he ends up seeing them move. Third, he is
*serious*. He sets himself a rule, a punishment (death) and a prize (the puppy),
and then he keeps to them with a discipline most adults would not manage. The scab
in the opening paragraph prepares us for all of this: a child who can spend several
minutes closely studying a wound on his own knee is a child who can turn a carpet
into a jungle.

**The mother.** She has one sentence and no dialogue, yet she carries half of the
story's meaning. She is outside, in the sunshine — in a world with no snakes in it —
and she is "searching", which tells us that something has gone wrong and that she
does not know where. Dahl uses her to measure the distance between the adult world
and the child's. She was not there while it mattered, and now she cannot find him.

**The carpet.** It is worth treating the carpet as a character, because it behaves
like one. It is described as huge, with an intricate pattern the boy did not design
and cannot argue with. Once the rules are made, the carpet decides where he may
walk, how wide his steps must be, and finally whether he lives. It is the perfect
antagonist because it is entirely passive: everything it does to him, he has done to
himself.

## 4.4 Themes

**The power — and danger — of a child's imagination.** The story's whole action is
imaginary, and Dahl's achievement is to make the reader forget that. He builds the
illusion in stages: first a rule ("black is snakes"), then a description (adders,
cobras thick as tree-trunks), then movement (the heads lifting, the eyes watching),
then physical symptoms in the boy. By the end, imagination has overridden the
evidence of his own eyes. The question the story leaves is whether imagination is a
gift or a trap.

**Play, rules and self-imposed tests.** Nobody asks the boy to cross the carpet.
He invents the danger, the law and the prize entirely by himself, and then obeys
them absolutely. Dahl is describing something every reader recognises — the private
games in which children practise courage — but he lets it run past the point where
a parent would have stopped it.

**Loneliness and the absence of adults.** The hall is empty. There is no mention of
a brother, a sister, a servant or a friend. The only adult in the story is offstage
until the last line, and when she does appear she is looking in the wrong place.
Dahl's children are frequently left to manage terror alone, and this story is the
purest example.

**Desire and reward: the puppy.** The prize the boy chooses is touchingly ordinary
— a puppy, for a birthday that is only one day away. The gap between what is at
stake in his mind (being bitten to death before teatime) and what he is actually
playing for (a pet) is the source of both the story's tenderness and its irony. It
also explains why he will not give up when the black band appears: the reward is
real to him even though the danger is not.

**The thin line between the imagined and the real.** Dahl deliberately blurs the
boundary. Nothing supernatural is ever stated; every frightening detail could be a
child's overheated mind. But the ending gives that reading a shake. The mother
cannot find him, and the story simply stops, so the reader is left holding two
incompatible explanations at once.

```figure caption="Why the ending disturbs: Dahl supplies the same last sentence for two entirely different stories and refuses to say which one you have just read."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.0))
def box(x,y,w,h,title,body,fc,ec):
    ax.add_patch(FancyBboxPatch((x,y),w,h,
        boxstyle="round,pad=0.03,rounding_size=0.14",fc=fc,ec=ec,lw=1.1))
    ax.text(x+w/2,y+h-0.38,title,ha='center',va='center',fontsize=7.8,
            color=ec,weight='bold')
    ax.text(x+w/2,y+h-1.05,body,ha='center',va='center',fontsize=7.2,
            color=INK,linespacing=1.45)
box(0.15,4.05,9.7,1.55,'THE LAST THING WE ARE TOLD',
    'his hand comes down on black — he screams —\n'
    '"his mother was searching for him"','#eef3f9',ACCENT)
ax.annotate('',xy=(2.6,3.35),xytext=(4.2,3.95),
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.1,mutation_scale=11))
ax.annotate('',xy=(7.4,3.35),xytext=(5.8,3.95),
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.1,mutation_scale=11))
box(0.15,1.30,4.6,2.00,'READING A — the natural',
    'He panicked, fell, fainted\nor ran off and hid.\nThe snakes were never there.',
    '#f7f3ea','#b8860b')
box(5.25,1.30,4.6,2.00,'READING B — the uncanny',
    'The game became true.\nSomething has happened\nthat cannot be undone.',
    '#f6eeee','#A8271F')
ax.text(5.0,0.62,'Dahl gives no evidence for either — and that is the effect he wanted',
        ha='center',va='center',fontsize=7.2,color=MUTED,style='italic')
ax.set_xlim(0,10); ax.set_ylim(0.2,5.8)
ax.axis('off')
```

## 4.5 Setting, structure and point of view

**Setting.** The hall of an ordinary English house, on an ordinary day, with the
front door at the far end and sunshine outside. Dahl chooses the safest imaginable
place on purpose: the horror has to be manufactured out of furniture. The only
detailed object in the story is the carpet, and it is described almost entirely in
terms of colour, because colour is what the game is built from.

**Structure.** The story is a single unbroken scene, told more or less in real
time, and it has the simplest possible shape: a rule is made, the rule is obeyed,
the rule is broken. There is no subplot and no second character to interrupt. Dahl
controls the tension by steadily increasing the difficulty of the steps — easy
ones first, then narrow strips, then one impossible stretch — so that the reader
can feel the crisis coming several paragraphs before it arrives. The ending is
abrupt: a scream, and then one sentence from a completely different place.

**Point of view.** Third person, but so closely tied to the boy that we see only
what he sees, and we are given his thoughts in his own words — a technique called
**free indirect style**. This is why the snakes are convincing: the narrator does
not stand outside the child saying "he imagined that…", but reports the carpet the
way the boy experiences it. The final sentence breaks this closeness deliberately.
The viewpoint pulls back out of the house into the garden, and that sudden distance
is what makes the last line so cold.

::: definition Free indirect style
A way of writing third-person narration that slips into the character's own
thoughts and vocabulary, without quotation marks and without "he thought". It lets
the reader stand inside a character while the story still says "he" and "she".
:::

## 4.6 Literary devices

| Device | Example from the text | Effect |
|---|---|---|
| Symbolism | The carpet; the scab; the puppy | The carpet is the world with rules the child cannot change; the scab is a small wound he enjoys examining; the puppy is innocent desire |
| Colour symbolism | Red, black, yellow | Three colours carry the whole plot: danger by fire, danger by poison, and safety |
| Imagery (tactile and visual) | The hard-edged crust of the scab, the raw pink skin, snakes "thick like tree-trunks" | Makes an entirely imaginary danger physically convincing |
| Personification | The snakes stir, lift their heads and watch him | Turns a pattern into a predator; the carpet acquires a will |
| Suspense | Steps that grow narrower and further apart as he crosses | The reader is made to calculate the danger along with the boy |
| Foreshadowing | The opening scab episode; the widening black patches ahead | Prepares us for pain, and for a child fascinated by his own body's damage |
| Irony | Enormous stakes (death) for a very small prize (a puppy) | Measures the distance between the child's world and the adult's |
| Ambiguity / open ending | The final sentence about his mother searching | Two readings remain possible; the reader supplies the horror |
| Shift of point of view | The camera moves outside into the sunshine for one line | Sudden distance after intense closeness makes the ending chilling |

::: caution What students get wrong here
(i) Do not write that the snakes were real. Dahl never says so — and do not write
that they were only imagined either. The story is built to keep both answers open,
and an answer that discusses the ambiguity scores higher than one that settles it.
(ii) Do not treat the opening paragraph about the scab as pointless. It establishes
the boy's solitude, his fascination with small horrors, and the story's method of
describing the body in close-up.
:::

## 4.7 Glossary

| Word / phrase | Meaning |
|---|---|
| scab | the hard dry crust that forms over a healing cut |
| crust | a hard outer layer |
| to prise off | to lift something away with careful force |
| patch | a small area different from what is around it |
| intricate | complicated and detailed, with many small parts |
| adder | a small poisonous European snake |
| cobra | a large poisonous snake that spreads its hood |
| poisonous | containing poison; able to kill by biting |
| lump of coal | a solid piece of the black rock that is burned for heat |
| red-hot | so hot that it glows red |
| on tiptoe | standing on the front part of the feet, heels lifted |
| to balance | to keep steady without falling |
| to sway | to move slowly from side to side |
| to topple | to fall over |
| stretch (noun) | the act of reaching out as far as possible |
| windmill (verb) | to swing the arms round and round in circles |
| to shriek | to give a loud, high cry of fear or pain |
| dread | great fear of something that is about to happen |
| at stake | able to be won or lost |
| teatime | the late-afternoon meal in a British household |

::: tip Exam technique for this story
Questions on "The Wish" usually ask *how* Dahl creates tension. Do not simply
retell the plot. Name the techniques — the escalating difficulty of the steps, the
close third-person viewpoint, the physical details of fear, the shrinking gaps of
yellow — and give one example of each. Finish with the change of viewpoint in the
final sentence, which is worth a mark on its own.
:::

## Chapter summary

- Roald Dahl (1916–1990), British, born in Wales of Norwegian parents, RAF pilot,
  author of macabre adult stories and famous children's books; "The Wish" is from
  *Someone Like You* (1953).
- A small boy alone in the hall picks off a scab, examines the new skin, and then
  studies the large red, black and yellow carpet.
- He invents a game: black is poisonous snakes, red is red-hot coals, yellow is
  safe; the prize for crossing is a puppy for his birthday the next day.
- As he crosses, the imagined danger becomes real to him — the snakes seem to stir
  and watch — and he begins to show the physical signs of real fear.
- A wide band of black forces an enormous stretch; he loses his balance, whirls his
  arms and puts his hand down on black. He screams.
- The story ends outside in the sunshine with his mother searching for him, and
  explains nothing.
- Themes: imagination and its dangers; self-imposed rules and play; loneliness and
  absent adults; desire (the puppy); the blurred line between imagined and real.
- Devices: symbolism and colour symbolism, tactile imagery, personification,
  suspense, foreshadowing, irony, free indirect style, and a deliberately
  ambiguous ending.

## Practice questions

**Short answer questions (2 marks each)**

1. What is the boy doing at the beginning of the story, and what does it show about him? <span class="marks">[2]</span>
2. What rules does the boy make for his game on the carpet? <span class="marks">[2]</span>
3. What prize has the boy promised himself for crossing the carpet successfully? <span class="marks">[2]</span>
4. How does Dahl show that the game has stopped being a game for the boy? <span class="marks">[2]</span>
5. Why is the last stretch across the black band impossible for him? <span class="marks">[2]</span>
6. Why does Dahl end the story with the mother outside in the sunshine? <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** He is sitting alone at the foot of the stairs, carefully picking the scab off
his knee and examining the clean pink skin underneath. It shows that he is solitary,
patient and closely interested in small, slightly unpleasant things — exactly the
kind of attention he will soon turn on the carpet.

**2.** The black parts of the carpet are poisonous snakes, the red parts are red-hot
lumps of coal, and only the yellow parts are safe. If he touches black he will be
bitten and die; if he touches red he will be burnt. He must cross the whole carpet
stepping on yellow alone.

**3.** He has decided that if he crosses the carpet without a single mistake, he will
be given a puppy for his birthday, which falls the very next day. The smallness of
this reward, set against the death he has imagined for himself, is one of the
story's quiet ironies.

**4.** Dahl stops describing what the boy pretends and starts describing what he
sees: the snakes appear to stir, raise their heads and watch him, and the red looks
genuinely hot. At the same time the boy's body reacts — his breathing quickens and
he feels dizzy and frightened — which shows that he now believes in the danger.

**5.** A wide band of black lies across his route, and the nearest yellow patch on
the far side is further away than a normal step. He can only reach it by an enormous
stretch, with one foot behind and his weight hanging over the black, which leaves
him no way to recover if he wobbles.

**6.** Because the sudden distance is more frightening than any description of what
happened. After a whole story spent inside the boy's mind, the reader is pushed
outside into warm daylight, where an ordinary mother is looking for a child she
cannot find. Dahl explains nothing, and the silence does the work.
:::

**Long answer questions (5 marks each)**

1. How does Roald Dahl build tension in "The Wish"? Discuss the techniques he
   uses. <span class="marks">[5]</span>
2. "The real subject of 'The Wish' is the imagination of a lonely child." Discuss. <span class="marks">[5]</span>
3. Comment on the ending of "The Wish". Why does Dahl leave it unexplained? <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** Dahl builds tension out of materials that are completely harmless, which is
why the effect is so striking. First he establishes the rules, and makes them
absolute: black means snakes and death before teatime, red means burning, yellow
alone is safe. Because the reader accepts the rules, every later step can be
measured against them. Second, he arranges the physical difficulty in a rising
order. The early steps are simple; then the yellow patches narrow, so the boy must
balance on tiptoe and on one foot; and finally a wide band of black demands a
stretch no child of his size can make. The reader can see the crisis approaching
several paragraphs before it arrives, which is the classic source of suspense.
Third, he moves from pretence to perception. At first the boy decides that the black
is snakes; soon he sees them stir and lift their heads to watch him. Fourth, he
reports the boy's body — the quickened breathing, the dizziness, the arms whirling
like a windmill — so that the fear is felt physically rather than described. Last,
he controls the speed of the prose, slowing to almost nothing for the great stretch,
then delivering the fall, the scream and the closing sentence in a few lines.

**2.** Almost nothing happens in this story except inside one child's head, and Dahl
arranges everything else to make that inner life visible. The boy is alone: no adult
appears until the last sentence, no other child is mentioned, and the house is
silent. That solitude is the condition for the whole game. It is also the reason
nobody interrupts him — an older brother or a mother in the hall would have laughed
and the danger would have collapsed. Into this emptiness the boy pours an
extraordinary imaginative energy. He takes an ordinary domestic pattern and turns it
into a landscape with laws, punishments and a prize; he populates it with adders and
cobras "thick like tree-trunks"; and he then submits to his own invention so
completely that he suffers real, physical fear. Dahl shows how close such
imagination lies to the ordinary details of childhood: the story opens with the boy
absorbed in the scab on his own knee, a small private world of exactly the same kind.
The longing behind the game is childish and touching — a puppy for tomorrow's
birthday — and the punishment he invents is death. The story therefore ends by
asking whether imagination this strong is a gift or a danger, and Dahl leaves it
genuinely unclear, which is his answer.

**3.** The ending is abrupt and deliberately incomplete. The boy's hand comes down on
black, he screams, Dahl gives a single short paragraph of snakes, and then the story
leaves the house altogether for one last sentence, in which his mother is outside in
the sunshine, searching for him. Everything a conventional ending would supply is
missing: no rescue, no explanation, no return to the hall. Two readings remain
possible, and the text supports both. In the natural reading, the boy has frightened
himself into a panic, has fallen, fainted or run and hidden, and his mother simply
cannot find him for the moment; the snakes were never there. In the uncanny reading,
the game has somehow become true, and the last sentence quietly tells us that the
boy is gone. Dahl refuses to decide. He also changes the viewpoint at the same
moment, pulling back from the child's mind — where we have been for the entire story
— to a cool outside view in ordinary daylight. The contrast between that warm,
normal world and the terror we have just shared is what makes the ending memorable.
The horror is handed to the reader to complete, which is always more frightening
than being told.
:::

**Reference to the context**

1. "adders mostly, and cobras, thick like tree-trunks"

   (a) What is being described here, and by whom? (b) Where exactly is the boy at
   this moment? (c) What rule has he attached to these things? (d) How does this
   description help the story's later effect? <span class="marks">[5]</span>

2. "his mother was searching for him"

   (a) Where does this line occur in the story? (b) What has just happened?
   (c) Why does Dahl change the viewpoint here? (d) What two interpretations of the
   ending does the line allow? <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) The phrase describes the black patches of the large carpet in the hall of
the boy's house, which he has decided are poisonous snakes. It comes to us through
the narrator, but in the boy's own words and imagination. (b) He is sitting alone at
the bottom of the staircase, having just picked the scab off his knee, and is looking
across the carpet that stretches from the stairs to the front door. (c) He has made
the rule that if he touches a black patch he will be bitten and will die before
teatime, while red means burning coals and yellow alone is safe ground; if he crosses
untouched, he will get a puppy for his birthday the next day. (d) The detail is
specific and physical — named species, and a comparison to the thickness of
tree-trunks — so the reader can see the snakes too. Having accepted them once, we
accept them again when they begin to stir and watch him, and the fear of the final
stretch becomes ours as well as his.

**2.** (a) It is the last line of the story, standing alone after the boy has fallen
and screamed. (b) He has attempted an enormous stretch over a wide band of black,
failed to bring his weight across, whirled his arms to save his balance and put his
hand down flat on the black. He screams, and Dahl gives one brief paragraph of the
snakes. (c) Because after an entire story spent inside the child's mind, the sudden
move outside to warm sunshine and an ordinary parent creates a shock of distance. The
reader is separated from the boy at exactly the moment he most needs company, and
nothing is explained. (d) Either the boy has simply panicked, fallen or hidden, and
his mother will find him in a moment — the snakes having been imaginary all along; or
the game has become real and the boy has been lost for good. Dahl provides no
evidence for either, and that refusal is the source of the ending's power.
:::

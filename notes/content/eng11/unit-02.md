---
subject: Compulsory English
grade: 11
unit: 2
title: The Oval Portrait
hours: 3
area: Literature — Short Stories
---

"The Oval Portrait" is one of the shortest stories Edgar Allan Poe ever wrote —
under a thousand words — and one of the most tightly built. A wounded traveller
takes shelter in an abandoned castle, notices a portrait of a young woman that
seems frighteningly alive, and reads the terrible explanation in a book beside
his bed. It is on the syllabus because it shows, in a very small space, how a
Gothic writer creates atmosphere, how a frame narrative works, and how a whole
argument about art and life can be made in a single closing sentence.

::: key The central idea
The painter puts life into his canvas by taking it out of his wife. When the
picture is finally "Life itself", the living woman is dead. Art and life, in this
story, are rivals, and art wins.
:::

## 2.1 About the author

Edgar Allan Poe (1809–1849) was an American poet, short-story writer, editor and
critic. He was born in Boston. His father abandoned the family and his mother
died before he was three, and he was taken in — though never legally adopted — by
John Allan, a merchant of Richmond, Virginia, from whom he took his middle name.
He quarrelled with Allan over money, left the University of Virginia after less
than a year, served briefly in the army, and spent the rest of his short life
working for magazines, always poor. In 1836 he married his cousin Virginia Clemm;
she died of tuberculosis in 1847, after years of slow decline. Poe himself died in
Baltimore in 1849, aged forty, in circumstances that have never been explained.

Poe belongs to **Dark Romanticism**, also called the American Gothic: writing that
explores fear, madness, guilt, death and the parts of the mind we do not control.
His best-known works are the poems "The Raven" (1845) and "Annabel Lee", and the
stories "The Fall of the House of Usher", "The Tell-Tale Heart", "The Masque of the
Red Death" and "The Cask of Amontillado". With "The Murders in the Rue Morgue"
(1841) he effectively invented the **detective story**.

::: definition Unity of effect
Poe's own rule for the short story: every word, incident and detail should work
towards one single emotional effect on the reader, and the story should be short
enough to be read in one sitting. In "The Oval Portrait" that single effect is
dread.
:::

What is distinctive about Poe's voice is its controlled excess. The sentences are
long and formal, crowded with unusual words, and they slow the reader down so that
the atmosphere has time to thicken. He almost always narrates in the first person,
often through a speaker who is ill, frightened or unreliable, so the reader can
never be quite sure how much of the horror is in the world and how much is in the
narrator's head. He returns again and again to one subject — the death of a
beautiful woman — which he once called the most poetical topic in the world.
"The Oval Portrait" first appeared in 1842 under the title "Life in Death", and
Poe cut it to its present shape in 1845.

## 2.2 The story

**Taking shelter.** The narrator is badly wounded — we are never told how — and is
travelling with his servant, Pedro. Rather than let his master spend a night in
the open, Pedro forces his way into an abandoned château in the Apennine mountains
of Italy, a building of "commingled gloom and grandeur". Poe compares it to the
castles in the novels of Mrs Radcliffe, a famous writer of Gothic romances, which
tells the reader at once what kind of story this will be.

**The turret chamber.** The two settle in a small room in a remote turret. Its
decorations are rich but old and torn: tapestry on the walls, coats of arms, and an
unusual number of very lively modern paintings in gilded frames, hung not only on
the main walls but in the odd corners created by the château's strange
architecture. The narrator says that his "incipient delirium" — the beginning of
fever — may be why the pictures interest him so much. He tells Pedro to close the
heavy shutters, light the many candles of a tall candelabrum by the bed and open the
black velvet bed-curtains, so that he can look at the paintings and read a small
book found on the pillow, which describes and criticises them.

**Midnight, and the hidden picture.** He reads and gazes for hours. At midnight he
is unhappy with the position of the candelabrum, and reaches out — carefully, so as
not to wake the sleeping Pedro — to move it nearer the book. The result is
unexpected. The candles now light a niche of the room that had been in deep shadow
behind one of the bed-posts, and he sees a picture he had not noticed: the portrait
of a young girl "just ripening into womanhood".

**The shock.** He glances at it, then shuts his eyes. He does this by instinct, and
only afterwards works out why: he wants a moment to be sure his eyes have not
deceived him. Looking again, he is fully awake, all drowsiness gone. The picture is
only a head and shoulders, painted in the *vignette* manner — arms, shoulders and
the ends of the hair fading into the dark background — in the style of the American
portrait painter Thomas Sully, in an oval gilded frame. He lies half-sitting for
perhaps an hour, staring, and finally understands what disturbs him. It is not the
skill of the painting, nor the beauty of the face, and it is certainly not that he
mistook the picture for a living person: the oval frame and the vignette style make
that impossible. The secret is "an absolute life-likeliness of expression", which
startles, then confuses, then overcomes and terrifies him. Shaken, he moves the
candelabrum back so that the portrait falls into darkness again, and reaches
eagerly for the book, turning to the entry that explains this picture.

**The story in the book.** The book tells of a girl of rare beauty, full of
laughter, who loved and married a painter. It was an evil hour when she did so, for
the painter already had a bride — his Art. She loved everything, and hated only the
Art that was her rival, and feared only the brushes and palette that took her
husband's face away from her. So when he announced that he wished to paint her, it
was terrible news. But she was humble and obedient, and sat for many weeks in a
dark, high turret-chamber where light fell on the canvas only from above.

**The painting and the death.** The painter, wild, moody and lost in his work,
laboured day and night and would not see that the ghastly light of the turret was
draining the health and spirits of his bride, who faded visibly to everyone except
him. She kept smiling and never complained, because she could see how much joy the
work gave him. Visitors spoke in low voices of how like her the portrait was, and
called it proof both of his skill and of his love. As the work neared its end he
allowed nobody into the turret; he had become so wild in his eagerness that he
hardly turned his eyes from the canvas even to look at his wife's face; and he
would not see that the colours he was spreading on the canvas were being taken from
her cheeks. At last only one stroke on the mouth and one tint on the eye remained.
The lady's spirit flickered up once more, "as the flame within the socket of the
lamp". The brush was given and the tint placed. For one moment the painter stood
entranced before his finished work; the next, he grew pale and trembling and cried
aloud, "This is indeed Life itself!" Then he turned to look at his beloved. She was
dead.

```figure caption="The exchange at the heart of the story: week by week, life leaves the bride at exactly the rate it enters the canvas. Both reach their opposite extremes at the last brush-stroke."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
w = np.linspace(0, 10, 200)
life = 100*np.cos(np.pi*w/20)**2
art  = 100 - life
ax.plot(w, life, color='#A8271F', lw=2.0, label='life in the bride')
ax.plot(w, art,  color=ACCENT, lw=2.0, ls='--', label='life in the portrait')
ax.plot([10,10],[0,100],color=MUTED,lw=0.8,ls=':')
ax.plot([10],[100],'o',color=ACCENT,ms=5,zorder=5)
ax.plot([10],[0],'o',color='#A8271F',ms=5,zorder=5)
ax.annotate('the portrait is\n"Life itself"',(10,100),xytext=(9.55,64),
            textcoords='data',ha='right',va='center',fontsize=7.4,color=ACCENT,
            linespacing=1.4,
            arrowprops=dict(arrowstyle='-',color=ACCENT,lw=0.7,shrinkA=3,shrinkB=3))
ax.annotate('the bride is dead',(10,0),xytext=(9.55,34),
            textcoords='data',ha='right',va='center',fontsize=7.4,color='#A8271F',
            arrowprops=dict(arrowstyle='-',color='#A8271F',lw=0.7,shrinkA=3,shrinkB=3))
ax.set_xlabel('weeks of sitting in the turret-chamber')
ax.set_ylabel('vitality')
ax.set_xlim(0,10.5); ax.set_ylim(-4,112)
ax.set_yticks([0,50,100]); ax.set_yticklabels(['none','half','full'])
ax.set_xticks([0,10]); ax.set_xticklabels(['first sitting','last tint'])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.45)
ax.legend(loc='lower center', bbox_to_anchor=(0.5,1.02), ncol=2, fontsize=8.0,
          frameon=False, handlelength=2.0)
```

## 2.3 Characters

| Character | Who they are | Role in the story |
|---|---|---|
| The narrator | An unnamed traveller, "desperately wounded", feverish | Tells the outer story; his fear and his reading frame everything we learn |
| Pedro | His valet (personal servant) | Breaks into the château, lights the candles, then sleeps — a practical man untouched by the horror |
| The painter | A husband of "high renown", passionate, studious, austere, wild and moody | The real antagonist: he kills without meaning to, by not looking up |
| The bride | A young woman of rare beauty, "frolicsome as the young fawn" | The victim; she is never named and never speaks in the story |
| Art (personified) | The painter's first "bride" | The rival who defeats the living wife |

**The narrator.** He is important not for what he does — he does almost nothing but
move a candlestick — but for how he sees. He tells us himself that a delirium is
beginning, and Poe leaves it deliberately unclear whether the portrait's dreadful
liveliness is a fact or a symptom. His reactions are described with unusual
precision: he glances, shuts his eyes, reasons about why he shut them, looks again,
lies staring for an hour, and only then names the cause of his terror. That slow,
analytical movement is what makes the horror convincing; a hysterical narrator
would be much less frightening.

**The painter.** Poe is careful not to make him a monster. He loves his wife —
visitors read the portrait as proof of it — and he never intends her any harm. His
crime is a kind of blindness: he "would not see" the light withering her, and he
"would not see" that the colours going onto the canvas were coming off her cheeks.
The word repeated is *see*, which is savage irony in a man whose whole profession is
looking. He is the type of the obsessed artist, for whom the work becomes more real
than the person, and his cry at the end — "This is indeed Life itself!" — is both
his triumph and his sentence.

**The bride.** She is given no name, no dialogue and no choice. Everything we learn
about her is in the first few lines of the book's account: beautiful, full of glee,
loving all things, hating only the Art that was her rival. Her tragedy is that she
is "humble and obedient": she sits for weeks in a dark room, smiling
uncomplainingly, precisely because she loves him. Poe's simile for her last moment
— her spirit flickering up like a flame in the socket of a lamp just before it goes
out — makes her death seem like something quietly used up rather than violently
taken.

## 2.4 Themes

**Art demands life, and takes it.** This is the story's central claim, and Poe
makes it literal, not merely symbolic. The tints spread on the canvas are "drawn
from the cheeks of her who sate beside him". As the portrait grows more lifelike,
the model grows weaker, until the exact moment of completion is the exact moment of
death. The idea also explains the original title, "Life in Death": the life in the
picture is the death of the woman.

**Obsession and the blindness it causes.** The painter is not cruel; he is
absorbed. He locks the turret against visitors, works day and night, hardly lifts
his eyes from the canvas, and loses the ordinary human power of noticing that
someone in the room is dying. Poe is describing a danger he knew from inside — the
artist who sacrifices the people around him to the work.

**Beauty, death and the woman as object.** The wife is turned into a picture, and
the picture is more admired than the woman ever was. She is looked at, arranged,
copied and hung on a wall; the one thing nobody does is listen to her. It is worth
noticing that the portrait survives in a gilded oval frame for years, while she is
gone in a single sentence.

**Perception, fever and the unreliable eye.** The outer story keeps reminding us
that its narrator is wounded and half-delirious, that the room is lit by
candle-flame, and that a single movement of the candelabrum can make a whole
painting appear out of the dark. Poe wants the reader to feel that the boundary
between seeing and imagining is thin, and that what frightens us most is what we
half-see.

**The power of a story told by someone else.** The most horrifying part of the tale
does not happen to the narrator at all: he only reads it. Poe demonstrates that
horror travels through narration, and that an old book, in the right room at the
right hour, can be more terrifying than any ghost.

## 2.5 Setting, structure and point of view

**Setting.** An abandoned château among the Apennines, at night, in a remote
turret; heavy shutters closed, black velvet curtains thrown open, a tall candelabrum
burning; rich decorations that are "tattered and antique". Every element is standard
Gothic furniture, and Poe openly admits the debt by naming Mrs Ann Radcliffe. Note
the deliberate echo: the narrator lies in a turret chamber looking at a portrait, and
the portrait was painted in a turret chamber. The two rooms rhyme, which is why the
reader feels trapped inside the painting's history.

**Structure — a frame narrative.** The story is built in three layers, like boxes
inside boxes: the narrator's night in the château; the small book of criticism found
on the pillow; and, inside the book's entry, the painter's tale. Poe never returns
to the outer layer. The story ends on the last words of the book — "She was dead!" —
with no comment from the narrator at all, and that missing return is what leaves the
reader without a safe place to stand.

::: definition Frame narrative
A story placed inside another story. The outer story (the "frame") introduces a
narrator or a document, and the inner story is what that narrator tells or that
document contains.
:::

**Point of view.** The frame is first person: a wounded, feverish "I" whose
judgement we are invited to doubt. The inner tale is third person, told in the
archaic, formal language of an old book ("And evil was the hour when she saw, and
loved, and wedded the painter"), which distances the events and makes them sound
like a legend. The shift between these two voices is one of the story's most skilful
effects.

```figure caption="The three nested layers of the narrative. Poe never brings the reader back out through them — the story ends inside the innermost box."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.9,3.3))
boxes = [((0.20,0.20),9.60,5.70,'#eef3f9',ACCENT,
          'OUTER FRAME  —  first person',
          'The wounded narrator and Pedro in the turret of the château;\nthe candelabrum is moved and the portrait appears'),
         ((0.95,0.85),8.10,3.50,'#f7f3ea','#b8860b',
          'MIDDLE FRAME  —  a written document',
          'The small volume found on the pillow, which\ndescribes and criticises the paintings'),
         ((1.70,1.45),6.60,1.40,'#f6eeee','#A8271F',
          'INNER TALE  —  third person, archaic',
          'The painter, his bride, the weeks of sitting,\nand the last tint of all')]
for (xy,w,h,fc,ec,title,body) in boxes:
    ax.add_patch(FancyBboxPatch(xy,w,h,boxstyle="round,pad=0.03,rounding_size=0.16",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(xy[0]+w/2, xy[1]+h-0.40, title, ha='center', va='center',
            fontsize=7.7, color=ec, weight='bold')
    ax.text(xy[0]+w/2, xy[1]+h-1.02, body, ha='center', va='center',
            fontsize=7.1, color=INK, linespacing=1.45)
ax.text(5.0, 0.44, 'the story stops inside the innermost box — it never comes back out',
        ha='center', va='center', fontsize=7.1, color=MUTED, style='italic')
ax.set_xlim(0,10); ax.set_ylim(0,6.1)
ax.axis('off')
```

## 2.6 Literary devices

| Device | Example from the text | Effect |
|---|---|---|
| Frame narrative | The narrator reads the portrait's history in a book | Puts distance between reader and horror, then removes the way back out |
| Gothic setting | Abandoned château, remote turret, deep midnight, candlelight, tattered tapestry | Builds dread before anything frightening has actually happened |
| Symbolism | The candelabrum (what light reveals and hides); the oval frame; the dark turret | Turns the physical room into a statement about art, seeing and death |
| Situational irony | The painter's cry, "This is indeed Life itself!", spoken over a corpse | The moment of artistic triumph is the moment of human catastrophe |
| Paradox / oxymoron | The original title, "Life in Death"; a portrait more alive than its model | Compresses the whole theme into two words |
| Personification | Art is the painter's first "bride" and the wife's "rival" | Makes an abstraction into a character who can compete and win |
| Simile | Her spirit "flickered up as the flame within the socket of the lamp" | Makes her death gentle, domestic and inevitable rather than violent |
| Foreshadowing | "Evil was the hour when she saw, and loved, and wedded the painter" | Warns the reader of the ending on the first line of the inner tale |
| Imagery of light and shade | Light "dripped" from overhead onto the canvas; the niche "thrown into deep shade" | Light gives life to the picture and takes it from the woman |
| Unreliable narration | "My incipient delirium, perhaps, had caused me to take deep interest" | Leaves it open whether the terror is in the picture or in the narrator |

## 2.7 Glossary

| Word / phrase | Meaning |
|---|---|
| château | a large French or Italian country house or castle |
| valet | a manservant who looks after his master personally |
| forcible entrance | going into a building by breaking a door or lock |
| commingled | mixed together |
| sumptuously | richly and expensively |
| turret | a small tower at the corner or top of a large building |
| tapestry | heavy cloth with pictures woven into it, hung on walls |
| armorial trophies | displays of family coats of arms, shields and weapons |
| arabesque | an ornamental design of curling lines and leaf shapes |
| candelabrum | a tall stand holding several candles |
| incipient delirium | fever-madness that is just beginning |
| perusal | careful reading |
| niche | a hollow space set into a wall |
| vignette manner | a portrait style in which the edges fade gradually into the background |
| filigreed | decorated with fine, delicate ornamental work |
| Moresque | in the Moorish (North African / Spanish-Arab) style |
| austere | severe and strict; taking no pleasure in comfort |
| pallet (palette) | the board on which a painter mixes colours |
| reveries | daydreams; states of being lost in thought |
| pined | grew weak and thin from sorrow or longing |
| ardor | burning eagerness or passion |
| in sooth | (old) in truth, truly |
| tremulous | trembling, shaking |
| aghast | struck with sudden horror |
| entranced | held still as if under a spell |

::: caution Two mistakes to avoid
(i) Do not write that the painter murdered his wife. There is no violence in the
story; the point is that he never noticed. The horror is neglect, not crime.
(ii) Do not write that the narrator thought the portrait was a real woman. Poe
explicitly rules this out — the oval frame and vignette style "must have instantly
dispelled such idea". What frightens him is the *expression*, not a mistake.
:::

::: tip What the examiner wants from this story
Most questions turn on one sentence: "This is indeed Life itself!" If you can
explain why that line is ironic, why it is the climax, and how the frame narrative
delivers it to us second-hand, you can answer nearly anything asked about this text.
:::

## Chapter summary

- Edgar Allan Poe (1809–1849), American, a founder of Dark Romanticism and of the
  detective story; "The Oval Portrait" appeared in 1842 as "Life in Death".
- A wounded narrator and his valet Pedro shelter in an abandoned château in the
  Apennines and take a small turret room hung with paintings.
- Moving the candelabrum at midnight reveals an oval portrait of a young girl whose
  "absolute life-likeliness of expression" terrifies him.
- A book on the pillow explains it: a painter married a beautiful girl who hated
  his Art as her rival, then made her sit for weeks in a dark turret.
- Absorbed in his work, he did not see her fading; the colours he laid on the canvas
  were drawn from her cheeks.
- At the last brush-stroke he cried, "This is indeed Life itself!", turned to his
  bride, and found her dead. The story ends there, inside the book.
- Themes: art consuming life; artistic obsession and blindness; beauty and death;
  the woman as object; the unreliable, feverish eye.
- Devices: frame narrative, Gothic setting, situational irony, paradox, the lamp
  simile, light-and-shade imagery, unity of effect.

## Practice questions

**Short answer questions (2 marks each)**

1. Why did the narrator and Pedro enter the château? <span class="marks">[2]</span>
2. How did the narrator come to notice the oval portrait? <span class="marks">[2]</span>
3. What exactly was it about the portrait that terrified the narrator? <span class="marks">[2]</span>
4. Why did the painter's wife hate Art? <span class="marks">[2]</span>
5. What does the narrator mean by his "incipient delirium", and why does Poe mention it? <span class="marks">[2]</span>
6. Explain the irony in the painter's words, "This is indeed Life itself!" <span class="marks">[2]</span>

::: note Model answers — short questions
**1.** The narrator was desperately wounded and could not spend a night in the open
air. His valet Pedro therefore broke into an abandoned château in the Apennines so
that his master could rest, and they settled in a small room in a remote turret.

**2.** At midnight the narrator was displeased with the position of the tall
candelabrum and reached out to move it so that its light fell better on his book.
The candles then lit a niche that had been hidden in shadow by a bed-post, and the
portrait appeared in vivid light.

**3.** It was not the skill of the painting nor the beauty of the face, and he did
not mistake it for a living woman. What appalled him was its "absolute
life-likeliness of expression" — the picture seemed to be alive, and that impression
first startled, then confused and finally overcame him.

**4.** She hated Art because it was her rival. The painter already had a bride in
his Art, and the palette and brushes took him away from her, so that she was
deprived of her husband's company and even of his face. When he wished to paint her,
she therefore heard it as terrible news.

**5.** "Incipient delirium" means a fever-madness that is just beginning. Poe
mentions it so that the reader cannot be certain whether the portrait is truly
uncanny or whether the narrator's sick imagination is at work. This uncertainty
deepens the fear and makes the narrator unreliable.

**6.** The painter believes he has captured life on canvas, and in that instant he
has — but the life came out of his wife. He shouts his triumph over a woman who has
just died, and the picture is "Life itself" only because she is no longer alive.
Success and disaster arrive in the same moment.
:::

**Long answer questions (5 marks each)**

1. Discuss "The Oval Portrait" as a story about the conflict between art and life. <span class="marks">[5]</span>
2. Explain how Poe uses the frame narrative and the Gothic setting to produce his
   single effect of dread. <span class="marks">[5]</span>
3. Sketch the character of the painter. Is he guilty of his wife's death? <span class="marks">[5]</span>

::: note Model answers — long questions
**1.** Poe builds the story on a single idea: that a work of art may be paid for
with a human life, and he presents it literally rather than as a figure of speech.
The painter already has "a bride in his Art" before he marries; the living wife is
therefore a second wife from the beginning, and she knows it, for she hates only
the Art which is her rival and dreads the palette and brushes that steal her
husband from her. When she begins to sit in the dark turret, the exchange starts.
The narrator of the book tells us that the painter "would not see" that the light
withered her, and would not see that the tints he spread on the canvas were "drawn
from the cheeks of her who sate beside him". Week by week the portrait gains
exactly what the model loses, so that the perfection of the one requires the
extinction of the other. The two curves meet at the final brush-stroke: the moment
the picture becomes "Life itself" is the moment she stops living. Poe's original
title, "Life in Death", states the theme directly. The conclusion is not that art
is evil but that an art which stops looking at the human being in front of it has
already killed something.

**2.** Poe said that a short story should aim at one single effect, and here that
effect is dread. He gets it first from the setting. Everything is Gothic: an
abandoned château among the Apennines, "commingled gloom and grandeur", a remote
turret, heavy shutters closed against the night, black velvet bed-curtains,
tattered antique decorations, and candlelight as the only illumination. He even
names Mrs Radcliffe, so the reader recognises the tradition. He then makes light
itself the instrument of terror: a single small movement of the candelabrum takes a
picture out of the darkness, as though the room had been concealing it. The frame
narrative does the rest. We meet a narrator who is wounded and half-delirious, so
we cannot fully trust him; inside his story sits an old book, and inside the book
sits the painter's tale in archaic, legendary language. Each layer makes the horror
older and less escapable. Most importantly, Poe does not come back out. The story
ends on the book's last words, "She was dead!", with no return to the turret and no
comforting comment from the narrator, leaving the reader shut inside the innermost
box.

**3.** The painter is presented in four words — "passionate, studious, austere" and
already wedded to his Art — and every later detail develops them. He is celebrated,
"of high renown", and he genuinely loves his wife: those who saw the portrait spoke
of it as proof both of his power and of his deep love for the woman he painted so
well. Yet he is also "wild, and moody", a man who becomes lost in reveries. As the
work advances he shuts everyone out of the turret, works day and night, and barely
lifts his eyes from the canvas even to look at the living face he is copying. Poe
twice uses the same phrase, that he "would not see" — that the ghastly overhead
light was destroying her health, and that his colours were being taken from her
cheeks. The repetition is bitterly ironic in a man whose art is seeing. Is he
guilty? Not of murder: there is no violence, no intention, and he is appalled at
the end. But he is guilty of a moral blindness that amounts to neglect. He had
weeks in which any ordinary husband would have noticed, and he chose the canvas
over the woman every single day. His cry of triumph over her corpse is his
punishment as well as his achievement.
:::

**Reference to the context**

1. "She was a maiden of rarest beauty, and not more lovely than full of glee."

   (a) Where in the story do these words occur, and who is being described?
   (b) Who is reading them, and in what circumstances? (c) What contrast does the
   line set up with the rest of her story? (d) What does the language of this
   sentence tell you about the inner narrative? <span class="marks">[5]</span>

2. "This is indeed Life itself!"

   (a) Who says this, and at what moment? (b) What does the speaker mean by it?
   (c) What does he discover immediately afterwards? (d) Why is this the climax of
   the story? <span class="marks">[5]</span>

::: note Model answers — reference to the context
**1.** (a) They are the opening words of the entry in the small volume found on the
narrator's pillow — the account of the oval portrait — and they describe the young
woman in the picture, the painter's bride. (b) The wounded narrator is reading them
at midnight, in a turret room of an abandoned château in the Apennines, after the
candelabrum's light has accidentally revealed the portrait and frightened him.
(c) The line shows her as she was before the painting began — beautiful, laughing,
"frolicsome as the young fawn" — which makes the rest of the account unbearable, for
that living gaiety is exactly what the weeks in the dark turret slowly take away
from her. (d) The formal, old-fashioned phrasing, with its inverted construction and
its "And evil was the hour" a line later, shows that the inner tale is told in the
voice of an old book rather than of a modern person. That legendary voice makes the
events feel distant and fated, which increases their power.

**2.** (a) The painter says it in the innermost story, at the instant he lays the
last brush-stroke on the mouth and the last tint on the eye of his wife's portrait,
after many weeks of work in the shut turret. (b) He means that he has succeeded
completely: the painted face is no longer a mere likeness but seems to possess life
of its own, and for one moment he stands entranced before what he has made.
(c) He grows pale, trembling and aghast, turns round to look at his beloved, and
finds that she is dead. (d) It is the climax because the two lines of the story meet
here. The life the painter has been transferring to the canvas is his wife's life,
so the completion of the portrait is necessarily the end of her. The sentence is the
story's supreme irony and also its theme in five words, and Poe ends the whole
narrative two lines later without another word of comment.
:::

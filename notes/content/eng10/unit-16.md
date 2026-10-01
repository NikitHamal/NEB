---
subject: Compulsory English
grade: 10
unit: 16
title: 'Unit 16: Success and Celebration'
hours: 0
area: Units
---

Success is rarely sudden. Behind most famous achievements lie years of failure, patience and effort, and a good deal of luck. This unit studies two texts on that theme. The first is a biography, "Walt Disney: An Example of Struggle and Success", which shows how the creator of Mickey Mouse and Disneyland went bankrupt, lost his best character and suffered a breakdown before he became a world name. The second is the famous poem "If" by Rudyard Kipling, a father's advice to his son on how to become a good and successful person. In grammar you will practise **prepositions and prepositional phrases**, and in writing you will produce a **message and a letter of congratulation** and a **speech**.

::: key What the examiner wants from this unit
Accurate facts and events from Disney's life, in the right order, plus the lesson. For the poem: the "if … then" structure, the qualities Kipling recommends and the meaning of difficult words. In grammar: the right preposition after a word or in a set phrase. In writing: a congratulation message that is warm and short, a letter with correct layout, and a speech that greets the audience, develops one idea and closes with a call.
:::

## 16.1 Walt Disney: An Example of Struggle and Success

### About the text

This is a **biographical article**: an account of a real person's life in order of time. It follows Disney from an unhappy childhood to the opening of Disneyland, and its purpose is to show that success comes from **determination and perseverance**. Notice how each paragraph gives a setback and then a recovery. This is a useful model for your own writing about a person who has inspired you.

```photo id="eng10/disney-mickey" caption="Walt Disney (1901–1966) with a film roll and Mickey Mouse, 1935." width="52"
```

### Summary

**A hard childhood.** Walter Elias Disney was born in Chicago on 5 December 1901, one of five children. His family was poor, and his father was a **domineering** man who was strict and sometimes violent. The young Walt found comfort in drawing, and as a boy he sold sketches to neighbours.

**Early jobs.** He left school and went to France to work as an **ambulance driver** at the end of the First World War. Back in the United States he worked in Chicago and Kansas City, first as a **trainee** in an art studio. There he met Ub Iwerks, a talented artist who became his lifelong partner.

**The first failure.** Disney started his own cartoon company in Kansas City, but it ran out of money and collapsed (it went **bankrupt**). He tried acting and then, in 1923, moved to Hollywood with almost no money. For years he lived on very little, eating cheap beans and sinking deeper into debt, as he struggled to start again.

**Oswald and Mickey.** In Hollywood he created a cartoon character called **Oswald the Lucky Rabbit**, who became popular. But in 1928 his distributor took the character, and most of his animators, away from him; the textbook says his employer "stole" his best animation film. It was a cruel blow. On the train home, Disney and Ub Iwerks created a new character, a cheerful mouse. **Mickey Mouse** appeared in 1928, and *Steamboat Willie*, the first Mickey cartoon with synchronised sound, made him famous. The strain of these years, however, caught up with him, and in 1931 he suffered a severe mental and emotional illness (a **nervous breakdown**).

**Feature films and flops.** In 1937 Disney released *Snow White and the Seven Dwarfs*, the first full-length cel-animated film in colour, which earned huge profits. He then made *Pinocchio*, *Fantasia* and *Bambi*, wonderful films that were **commercial failures** at first because the Second World War had closed the European market.

**Television and Disneyland.** Disney shifted his attention from the big screen to **television shows**, which brought him a new, large audience. Then he built **Disneyland** in California. Its opening day, 17 July 1955, was a disaster: the crowd was huge, many people had trouble standing in lines, and there was not enough drinking water in the summer heat. The press called it **"Black Sunday"**. Yet Disneyland soon became a success and was copied across the world.

**What made him succeed?** The text says it was his **determination and perseverance**. He failed many times, but each time he got up and began again. Walt Disney died on 15 December 1966, having won more Academy Awards than anyone in history.

```figure caption="Walt Disney: setbacks (below the line) and successes (above) in order."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.0))
ev=[(1901,'Born in Chicago;\nharsh father',-1),(1918,'Ambulance driver\nin France',1),(1923,'First company\nbankrupt',-1),(1928,'Mickey Mouse\ncreated',1),(1931,'Breakdown\n(Oswald lost)',-1),(1937,'Snow White\nbig success',1),(1941,'Pinocchio, Fantasia,\nBambi lose money',-1),(1955,'Disneyland opens\n("Black Sunday")',1)]
xs=[0,1,2,3,4,5,6,7]
ax.plot([-0.5,7.5],[0,0],color=INK,lw=1.4)
for x,(yr,l,s) in zip(xs,ev):
    c = ACCENT if s>0 else '#B8402E'
    ax.plot([x],[0],'o',color=c,ms=6)
    h = 0.35 + 0.5*(x%2)
    ax.plot([x,x],[0,s*h],color=MUTED,lw=0.8)
    ax.text(x,s*h+s*0.06,f'{yr}\n{l}',ha='center',va='bottom' if s>0 else 'top',fontsize=6.6,color=INK,linespacing=1.2)
ax.set_xlim(-0.9,7.9); ax.set_ylim(-1.9,1.9); ax.axis('off')
```

### Glossary

| Word | Meaning | Example |
|---|---|---|
| domineering | controlling others in an unkind way | He grew up under a domineering father. |
| solace | comfort in a time of sadness | She found solace in music. |
| apprentice | a person learning a trade by working | He was an apprentice electrician. |
| bankrupt | unable to pay debts | The shop went bankrupt. |
| afloat | not sinking; surviving financially | He sold his car to keep the business afloat. |
| mounting | growing; increasing | There was mounting pressure on the minister. |
| harness | to control and use (a natural force) | We can harness the sun's energy. |
| plotting | secretly planning | They were plotting a robbery. |
| perseverance | continuing in spite of difficulty | Perseverance is the key to success. |
| colossal | extremely large | A colossal amount of money was spent. |

**Idioms from the text**

| Idiom | Meaning | Sentence |
|---|---|---|
| make ends meet | to have just enough money to live | It is hard for a low-paid worker to make ends meet. |
| silver lining | the good side of a bad situation | The silver lining of the flood was the new road. |
| nervous breakdown | a period of severe mental illness from stress | He had a nervous breakdown after repeated failure. |
| drop out | to leave school or a course early | She dropped out of college to earn. |
| a kick in the teeth | a cruel disappointment | His refusal was a kick in the teeth. |
| set off | to begin a journey | We set off at dawn. |

### Disney's life in order (exam task)

1. Disney left home and went to France to work as an ambulance driver.
2. He returned to Chicago and worked as a trainee at an art studio.
3. His cartoon company collapsed.
4. He created the characters Oswald the Lucky Rabbit and Mickey Mouse.
5. Disney suffered severe mental and emotional illness.
6. He shifted his focus from the big screen to television shows.
7. He successfully founded the famous Disneyland.

*(The order of events 3, 4 and 5 follows the textbook key; historically, the mental illness came a few years after Mickey's creation.)*

### Comprehension questions with model answers

**A. Objective questions (1 mark each)**

1. Disney's father was <span class="marks">[1]</span>
   (a) kind (b) domineering (c) rich (d) a film director
2. His first film business <span class="marks">[1]</span>
   (a) collapsed (b) made a huge profit (c) won an Oscar (d) opened in London
3. The film that produced great profits was <span class="marks">[1]</span>
   (a) *Fantasia* (b) *Bambi* (c) *Snow White and the Seven Dwarfs* (d) *Pinocchio*
4. Write **True** or **False**: Disneyland's opening day was called "Black Sunday". <span class="marks">[1]</span>

::: note Answers — objective
**1.** (b) domineering. **2.** (a) collapsed. **3.** (c) *Snow White and the Seven Dwarfs*. **4.** True.
:::

**B. Short questions (2 marks each)**

1. How was Walt Disney's childhood? <span class="marks">[2]</span>
2. Describe Disney's family background. <span class="marks">[2]</span>
3. What did Disney do after the failure of his first business? <span class="marks">[2]</span>
4. Why did Disney suffer a mental breakdown? <span class="marks">[2]</span>
5. Which of his films were commercially unsuccessful? <span class="marks">[2]</span>
6. Why was the opening of Disneyland called "Black Sunday"? <span class="marks">[2]</span>

::: note Answers — short
**1.** His childhood was unhappy. His father was strict, domineering and sometimes abusive, and the family was poor.

**2.** Walt was one of five children in a poor family. His father was a hard, domineering man.

**3.** After the failure of his first business he tried acting and then moved to Hollywood to start again in cartoons.

**4.** His distributor took away Oswald, his best character, and most of his animators, which broke his spirit.

**5.** *Pinocchio*, *Fantasia* and *Bambi* did not make money at first.

**6.** On the opening day, huge crowds came, people had trouble in the lines, and there was not enough water to drink in the summer heat, so the day was a disaster.
:::

**C. Long questions (4 marks each)**

1. What special quality made Disney a successful entrepreneur? <span class="marks">[4]</span>
2. What lesson do you learn from Disney's life? Who has inspired you in your life? <span class="marks">[4]</span>

::: note Answers — long
**1.** Determination and perseverance made Disney a successful entrepreneur. His first company went bankrupt, he lost Oswald, he suffered a breakdown, and several of his best films lost money. Each time, instead of giving up, he started again with a new idea such as Mickey Mouse, the first feature-length cartoon, television shows and Disneyland. His belief in his own ideas and his willingness to learn from failure finally made him one of the most famous creators in history.

**2.** From Disney's life I learn that failure is not the end but a step towards success. Anyone who keeps trying with courage and imagination can win in the end. A person who has inspired me is my mother, who brought up three children by working as a seamstress. She never complained, and she always said that hard work and patience would be rewarded. Her example teaches me to keep going when things are hard.
:::

## 16.2 If

### The poet

**Rudyard Kipling** (1865–1936) was born in Bombay (now Mumbai), India, and spent his early childhood there before being sent to school in England. He returned to India as a young journalist and became famous for his stories and poems about India and the British Empire. His best-known books are *The Jungle Book* (1894), *Kim* (1901) and the *Just So Stories* (1902). In 1907 he became the first English-language writer to win the **Nobel Prize in Literature**, and he remains the youngest person ever to receive it (aged 41). "If—" was published in 1910 in his collection *Rewards and Fairies*. It is said to have been inspired by the character of a British colonial official, Dr. Leander Starr Jameson.

```photo id="eng10/kipling" caption="Rudyard Kipling (1865–1936), British writer and poet, Nobel Prize winner (1907)." width="52"
```

### The poem

"If—" is a poem of **four stanzas of eight lines**. Each stanza lists conditions (*If you can …*) and the last stanza gives the result: "Yours is the Earth and everything that's in it, / And — which is more — you'll be a Man, my son!" The poem is spoken by a father to his son, but its advice applies to everyone, boys and girls. It describes the qualities of a **mature, balanced, honest and strong person**.

### Stanza-by-stanza explanation

| Stanza | Main advice | Key phrases |
|---|---|---|
| **1** | Keep calm, trust yourself, be patient and honest | "keep your head when all about you are losing theirs"; "trust yourself when all men doubt you"; "don't deal in lies" |
| **2** | Dream and think, but act; treat success and failure alike; be strong when your work is destroyed | "dream — and not make dreams your master"; "meet with Triumph and Disaster / And treat those two impostors just the same"; "watch the things you gave your life to, broken, / And stoop and build 'em up with worn-out tools" |
| **3** | Take risks and accept losses without complaint; keep going by willpower | "risk it on one turn of pitch-and-toss … And lose, and start again at your beginnings"; "hold on when there is nothing in you / Except the Will which says to them: 'Hold on!'" |
| **4** | Stay humble with all kinds of people; value every minute | "talk with crowds and keep your virtue, / Or walk with Kings — nor lose the common touch"; "fill the unforgiving minute / With sixty seconds' worth of distance run" |

**Stanza 1.** The speaker says that if you can stay calm when others lose their heads and blame you, trust yourself even when everyone doubts you (while also allowing for their doubt), be patient and not tired by waiting, not **deal in lies** when others lie about you, and not hate when others hate you, then you have taken the first step. You should also avoid looking too good or talking too wise: do not be proud of your own virtue.

**Stanza 2.** You may dream, but do not let dreams rule you; you may think, but do not make thoughts your only aim. Meet success and failure alike, calling both "impostors" because neither is permanent. Bear it when your words are twisted by **knaves** to trap fools, and when you see your life's work broken, rebuild it with worn-out tools.

**Stanza 3.** Be ready to risk all your winnings on one game of **pitch-and-toss** (a game of chance), lose it, and start again from scratch without a word of complaint. Force your heart, nerve and **sinew** to serve you long after they are tired and "hold on" through willpower alone.

**Stanza 4.** Talk with crowds without losing your goodness, walk with kings without losing the common touch, do not let enemies or loving friends hurt you, let all men count with you, but none too much. Fill each "unforgiving minute" — the minute that can never be repeated — with sixty seconds' worth of work. If you can do all this, the whole Earth is yours and, better still, you will be a true human being.

```figure caption="The structure of 'If': four stanzas of conditions leading to one promise."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.7))
labs=['Stanza 1\nCalm, self-trust,\npatience, truth','Stanza 2\nDream and think\nbut act; success\n= failure','Stanza 3\nRisk, lose, start\nagain; hold on\nby will','Stanza 4\nHumble with all;\nuse every\nminute']
for i,l in enumerate(labs):
    x=i*1.7
    ax.add_patch(FancyBboxPatch((x,1.3),1.5,1.3,boxstyle='round,pad=0.02,rounding_size=0.1',fc='#E8F0FA',ec=INK,lw=0.8))
    ax.text(x+0.75,1.95,l,ha='center',va='center',fontsize=6.2,color=INK,linespacing=1.3)
    ax.annotate('',xy=(3.35,0.75),xytext=(x+0.75,1.27),arrowprops=dict(arrowstyle='->',color=MUTED,lw=0.9))
ax.add_patch(FancyBboxPatch((0.2,0.0),6.3,0.7,boxstyle='round,pad=0.02,rounding_size=0.1',fc='#FFF3D6',ec=INK,lw=0.8))
ax.text(3.35,0.35,'"Yours is the Earth and everything that\'s in it ... you\'ll be a Man, my son!"',ha='center',va='center',fontsize=6.6,color=INK)
ax.set_xlim(-0.1,6.8); ax.set_ylim(-0.2,2.8); ax.axis('off')
```

### Glossary

| Word | Meaning |
|---|---|
| impostor | a person who pretends to be someone else; here, something false |
| triumph | great success or victory |
| knave | a dishonest man (old-fashioned) |
| stoop | to bend forwards and downwards |
| worn-out | badly damaged by use |
| pitch-and-toss | a game of chance, played by tossing coins |
| sinew | a strong band of tissue joining muscle to bone; strength |
| virtue | high moral quality |
| unforgiving | allowing no second chance |

### Figures of speech and form

| Device | Example |
|---|---|
| Repetition (anaphora) | "If you can …" begins most clauses |
| Personification | "Triumph and Disaster" are named like people |
| Metaphor | "build 'em up with worn-out tools"; "the unforgiving minute" |
| Paradox | success and failure are both "impostors" |
| Rhyme scheme | *ababcdcd* in each stanza |
| Tone | firm, wise, affectionate (a father's advice) |

### Theme

The central theme is the **making of character**. True success does not depend on wealth or fame but on self-control, honesty, courage and perseverance. The poet advises that we should be balanced: dream but act, win but stay humble, lose but not lose heart, and respect time. The result is a person of strength and wisdom who is master of himself or herself.

### Comprehension questions with model answers

**A. Objective questions (1 mark each)**

1. "If" is a poem by <span class="marks">[1]</span>
   (a) Wordsworth (b) Hardy (c) Kipling (d) Whitman
2. "Pitch-and-toss" is <span class="marks">[1]</span>
   (a) a game of chance (b) a farm tool (c) a poem (d) a song
3. The poet calls triumph and disaster <span class="marks">[1]</span>
   (a) friends (b) impostors (c) teachers (d) enemies
4. Write **True** or **False**: The poet says we should make dreams our master. <span class="marks">[1]</span>

::: note Answers — objective
**1.** (c) Kipling. **2.** (a) a game of chance. **3.** (b) impostors. **4.** False. We should not make dreams our master.
:::

**B. Short questions (2 marks each)**

1. What does the poet suggest about dealing with lies? <span class="marks">[2]</span>
2. What does "not be tired by waiting" mean? <span class="marks">[2]</span>
3. Why should we not aim only to dream? <span class="marks">[2]</span>
4. What can knaves do to us? <span class="marks">[2]</span>
5. What should we do if we lose at pitch-and-toss? <span class="marks">[2]</span>
6. What does "the unforgiving minute" mean? <span class="marks">[2]</span>

::: note Answers — short
**1.** The poet says that even when others tell lies about us we should not deal in lies; we should stay truthful.

**2.** It means we should be patient. If we have to wait for something, we should not lose heart or become angry.

**3.** A dream without action is useless. We must work to turn dreams into reality.

**4.** Knaves can twist our words and trick fools with them.

**5.** We should accept the loss without complaint and start again from the beginning.

**6.** It means a minute that can never be called back. Time lost is lost for ever, so every minute should be used well.
:::

**C. Long questions (4 marks each)**

1. Summarise the advice given in the poem. <span class="marks">[4]</span>
2. What suggestions do your parents and teachers give you to be successful in life? <span class="marks">[4]</span>

::: note Answers — long
**1.** In "If", Kipling gives a young man advice on how to be a person of character. In stanza one he asks us to stay calm, trust ourselves, be patient and honest. In stanza two he asks us to dream and think but also to act, to treat success and failure alike and to rebuild what is broken. In stanza three he says we should take risks, accept losses without complaint and use willpower to hold on when we are tired. In the final stanza he asks us to be humble with all people and to use every minute wisely. A person who does these things will be master of himself and of the world.

**2.** My parents and teachers advise me to set clear goals and make a timetable. They tell me to work hard and to be regular in my studies. They ask me to be honest, respectful and punctual, and to learn from my mistakes without being discouraged. They also tell me to read newspapers, to keep a positive attitude and to choose good friends. They remind me that success comes to those who persevere.
:::

## 16.3 Grammar and writing tasks

### Grammar I and II — Prepositions

Unit 15 introduced the main time and place prepositions. This unit adds more precise uses and **prepositional phrases**: a preposition plus a noun that work as a fixed expression.

```figure caption="At, on, in for time: from the narrowest point to the widest period."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,2.4))
rows=[('AT',1.6,2.4,'clock times, noon, night, a point in time','#DCE8F8'),('ON',0.8,3.6,'days and dates, special days','#C6DAF3'),('IN',0.0,5.0,'months, years, seasons, centuries, parts of the day','#B0CCEE')]
for lab,y,w,txt,c in rows:
    x=(5.0-w)/2
    ax.add_patch(FancyBboxPatch((x,y),w,0.65,boxstyle='round,pad=0.02,rounding_size=0.08',fc=c,ec=INK,lw=0.8))
    ax.text(x+0.25,y+0.325,lab,ha='left',va='center',fontsize=9,color=INK,fontweight='bold')
ax.text(2.95,1.925,'clock times, noon, night',ha='center',va='center',fontsize=6.8,color=INK)
ax.text(2.8,1.125,'days and dates',ha='center',va='center',fontsize=6.8,color=INK)
ax.text(2.8,0.325,'months, years, seasons, parts of day',ha='center',va='center',fontsize=6.8,color=INK)
ax.set_xlim(-0.1,5.1); ax.set_ylim(-0.1,2.4); ax.axis('off')
```

**Prepositions of time (more).**

| Preposition | Meaning | Example |
|---|---|---|
| **between … and** | within a range | I reached school between 9:00 and 9:15. |
| **from … to / until** | start and end | I stay in the office from 10 am to 4 pm. Ram worked in the hotel until 2010. |
| **within / in** | no later than a period | Finish your test in the next 30 minutes. |
| **by** | not later than | Submit the form by Friday. |
| **for / since** | duration / starting point | for two years; since 2070 |

**Prepositions with other uses**

| Preposition | Use | Example |
|---|---|---|
| **under** | below; in the control of | Ten members work under him. |
| **in** | a period of life; a state | She is in her twenties. There is a great deal of violence in some countries. |
| **into** | change of state | The discussion turned into an unpleasant quarrel. |
| **at** | exact temperature or rate | Water boils at 100 °C. Science has developed at a great pace. |
| **on** | on a trip, on the radio, on a diet | We went on a trip. I heard it on the radio. |
| **in** | opinion; the dark | In my opinion, violent films should be banned. |

**Prepositional phrases to learn**

| Phrase | Meaning | Example |
|---|---|---|
| in cash | by payment in notes and coins | Would you pay in cash or by cheque? |
| at playing (good at) | skilled in | Ram is brilliant at playing the violin. |
| interested in | wanting to know about | She is not interested in politics. |
| with each other | one another | The bus and the lorry collided with each other. |
| out of hand | out of control | The concert went out of hand. |
| in a hurry | rushing | I can't talk, I am in a hurry. |
| out of reach | too far to contact or touch | His phone is out of reach. |
| on a diet | eating specially to lose weight | She is on a diet. |
| at large | free; not caught | The criminal is still at large. |
| on board | on a ship, plane or bus | All passengers were on board. |
| out of control | no longer managed | The fire got out of control. |
| by heart | from memory | He learnt the poem by heart. |
| in time / on time | early enough / exactly at the time | The train arrived on time. |
| for sale | available to buy | The house is for sale. |

::: example Worked example 16.1 — choose the phrase
**Problem.** "The criminal who took five lives is still ______." (at large / on board)

**Solution.** *At large* means "free, not yet caught". Answer: *at large.*
:::

::: example Worked example 16.2 — in, on or at?
**Problem.** (a) "Water boils ______ 100 degrees Celsius." (b) "Can you turn the light ______?" (c) "She was married ______ the age of 20."

**Solution.** (a) **at** (a point on a scale). (b) **on** (the light is switched on). (c) **at** (a point in life: *at the age of*).
:::

::: caution Between / among
Use *between* for two (or clearly separate) things and *among* for many: *between you and me*, *among the trees*.
:::

**Exercise 1.** Choose the correct preposition.

1. I reached school sometime (between / among) 9:00 and 9:15.
2. I usually stay in my office (from / since) 10 a.m. to 4 p.m.
3. You should finish your test (in / at) the next 30 minutes.
4. Ram worked in the hotel (until / by) 2010.
5. Ten members work (under / below) him.
6. Ram is (at / in) her twenties.
7. Their discussion turned (into / to) an unpleasant quarrel.
8. Water boils (in / at) 100 °C.
9. She heard the news (on / in) the radio.
10. Science has developed (at / on) a great pace.

::: note Key to Exercise 1
**1.** between **2.** from **3.** in **4.** until **5.** under **6.** in **7.** into **8.** at **9.** on **10.** at
:::

**Exercise 2.** Complete with a phrase from the list: *with each other, in cash, at large, out of hand, in a hurry, on board, out of reach, on a diet, interested in.*

1. The bus and the lorry collided ______.
2. The criminal who took five lives is still ______.
3. I cannot contact him; his phone is ______.
4. The concert went ______ and the police had to intervene.
5. He is ______ these days for fear of putting on weight.
6. I can't talk now; I am ______.
7. All passengers were ______ safe and sound.
8. Would you like to pay ______ or by cheque?
9. She is not ______ politics.

::: note Key to Exercise 2
**1.** with each other **2.** at large **3.** out of reach **4.** out of hand **5.** on a diet **6.** in a hurry **7.** on board **8.** in cash **9.** interested in
:::

### Writing I — Message and letter of congratulation

A **congratulation message** expresses joy and respect for someone's success. It must be **short, warm and specific**. For a notice-board message, put the greeting in a clear heading, say who succeeded and in what, praise the qualities that led to success and close with good wishes.

**Task A.** Your school football team has won the Inter-school Football Tournament organised by the District Sports Development Committee. Write a message of congratulation to appear on the school notice board.

**Model message.**

**CONGRATULATIONS!**

Heartiest congratulations to our school football team on winning the Inter-school Football Tournament organised by the District Sports Development Committee. Your discipline, teamwork and hard training have brought great honour to our school. We are proud of every member of the team and of the coach. May you continue to win in every contest and set a bright example for all of us.

*— Students and teachers of Sunrise Secondary School*

**Task B.** Your maternal uncle has been promoted to Inspector of Nepal Police. Write a letter of congratulation.

**Model letter.**

> Kathmandu
> 12 April 2023
>
> Dear Uncle,
>
> I was delighted to hear that you have been promoted to the post of Inspector of Nepal Police. Please accept my warmest congratulations.
>
> You have always served with honesty and courage, so this promotion is the reward for years of hard work. All of us at home, especially mother, are very proud of you. I hope your new responsibility will give you more chances to serve the people.
>
> When you are free, please visit us, so that we can celebrate together. With love and best wishes for further success,
>
> Your loving nephew,
> Ram

| Feature | Message | Letter |
|---|---|---|
| Length | 40–70 words | 100–150 words |
| Layout | heading + body + name | address, date, greeting, body, closing, name |
| Tone | formal and bright | personal and warm |

### Writing II — A speech

A **speech** is spoken to an audience, so it uses a clear opening, simple sentences, repetition and direct appeal ("my friends", "we"). Its parts are: **greeting → introduction of the topic → body (2–3 points with examples) → conclusion with a call to action → thanks.**

**Task.** Draft a speech on "Failure as a Pillar of Success". Include examples of renowned and successful people.

**Model speech.**

Good morning, respected principal, teachers and my dear friends.

Today I want to talk about a word that all of us fear: *failure*. I believe that failure is not the opposite of success. It is a pillar on which success is built.

Think of Walt Disney. His first company went bankrupt, and he lost his best character to a distributor. He had a breakdown, yet he started again and gave the world Mickey Mouse, *Snow White* and Disneyland. Think of Thomas Edison, who is said to have tested thousands of materials before he found a suitable filament for the light bulb. When asked about it, he replied that he had not failed; he had found thousands of ways that did not work. Think of Nepal's own mountaineers, who turn back near the summit again and again and return the next season, wiser and stronger.

Why is failure so valuable? First, it teaches us what does not work, so that our next attempt is better. Second, it builds resilience: someone who has fallen and risen once is not afraid to fall again. Third, it makes our eventual success sweeter and more lasting.

So, my friends, if you do not do well in an exam, do not cry. Ask what went wrong, correct it, and try again. As Kipling says in "If", we should "meet with Triumph and Disaster and treat those two impostors just the same".

Let us make a promise today: we will never give up. Thank you.

::: tip Speech checklist
Greet the audience; state the topic early; one idea per paragraph; two real examples; a call to action; thank the audience.
:::

## Chapter summary

- Walt Disney (1901–1966): poor childhood under a domineering father; ambulance driver in France; first company bankrupt; Oswald lost; breakdown; Mickey Mouse (1928); *Snow White* (1937) a success; *Pinocchio, Fantasia, Bambi* flopped at first; television; Disneyland (1955, "Black Sunday"). Key quality: determination and perseverance.
- Kipling's "If" (1910): four stanzas, rhyme *ababcdcd*; a father's advice: calm, self-trust, patience, truth, act on dreams, treat success and failure alike, rebuild, take risks, hold on by will, stay humble, use every minute; promise: "you'll be a Man, my son!"
- Prepositions: *at* (clock times, points), *on* (days, trips, radio), *in* (months, years, periods); *between … and, from … to, until, by, under, into*; phrases such as *at large, out of hand, in cash, on board, out of reach*.
- Congratulation message: short and warm; congratulation letter: letter layout.
- Speech: greeting, topic, body with examples, conclusion/call to action, thanks.

## Practice questions

**Reading comprehension**

> Wilma Rudolph was born in 1940 in Tennessee, USA, the twentieth of twenty-two children. As a child she suffered from polio and wore a metal brace on her leg for years. Doctors said she would never walk normally. Yet she exercised every day, and by the age of twelve she could walk without the brace. She took up running and, in 1960, won three gold medals at the Rome Olympics, becoming the fastest woman in the world.

1. When was Wilma Rudolph born? <span class="marks">[1]</span>
2. What illness did she have as a child? <span class="marks">[1]</span>
3. Write **True** or **False**: She won three gold medals at the 1960 Olympics. <span class="marks">[1]</span>
4. What did the doctors say about her? <span class="marks">[2]</span>
5. How did she overcome her difficulty? <span class="marks">[2]</span>
6. What lesson does her story teach? Write in about 50 words. <span class="marks">[4]</span>

::: note Answers
**1.** 1940. **2.** Polio. **3.** True. **4.** They said she would never walk normally. **5.** She exercised every day, learned to walk without the brace, and later took up running. **6.** Her story teaches that determination can defeat even the hardest handicap. Though doctors had little hope for her, she worked hard and trained every day until she became an Olympic champion. We should never let weakness or other people's doubts stop us from pursuing our goals.
:::

**Grammar**

1. Fill in: "The meeting starts ______ 10 o'clock." <span class="marks">[1]</span>
2. Fill in: "My birthday is ______ 12 June." <span class="marks">[1]</span>
3. Fill in: "I was born ______ 2008." <span class="marks">[1]</span>
4. Fill in: "The thief is still ______ (free / caught)." Use *at large*. <span class="marks">[1]</span>
5. Fill in: "He worked here ______ 2015 (until / since)." (He left in 2015.) <span class="marks">[1]</span>
6. Fill in: "She is very good ______ mathematics." <span class="marks">[1]</span>
7. Fill in: "I will return ______ the end of the week (by / until)." <span class="marks">[1]</span>
8. Fill in: "The fire went out ______ control." <span class="marks">[1]</span>
9. Fill in: "Divide the sweets ______ the three children (between / among)." <span class="marks">[1]</span>
10. Fill in: "He paid the bill ______ cash." <span class="marks">[1]</span>

::: note Answers
**1.** at **2.** on **3.** in **4.** at large **5.** until **6.** at **7.** by **8.** of **9.** among **10.** in
:::

**Writing**

1. Your friend has won first prize in the district-level essay competition. Write a letter of congratulation. <span class="marks">[5]</span>
2. Draft a speech for the school assembly on "Perseverance is the key to success". <span class="marks">[5]</span>

::: note Outline for answers
**1.** Address and date; greeting; delight at the news; praise for his or her effort; wish for future success; closing.

**2.** Greeting; definition of perseverance; examples (Disney, Edison, a Nepali athlete or mountaineer); reasons it works; call to action; thanks.
:::

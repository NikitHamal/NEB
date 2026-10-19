---
subject: Question Bank
grade: 10
unit: 8
title: "Compulsory English: Unit-wise Objective Question Bank"
hours: 0
area: Compulsory English
---

The Grade 10 English paper carries 75 marks in three hours, and a large share of those marks are *objective*: true/false, multiple-choice, matching, gap-filling and one-word items. They appear in the reading questions on the two textbook passages, in the vocabulary question on the long unseen passage, and in the ten grammar items. This chapter gives practice items for all 18 units of the Grade 10 book, with an answer key and a short reason for every item.

::: caution About the labels in this chapter
Every item here is an **original practice item** written to the pattern of the SEE English paper and to the facts of the book chapters in this series. None is claimed to be a question from a particular year's paper. A book that prints a board year beside each item is usually guessing, and a wrong label teaches you to trust the wrong thing.
:::


```figure caption="Actual practice-question coverage in this chapter. Counts describe this book, not examination weightage or the probability of a question appearing."
fig, ax = barh_ranked(
    ["Reading items by unit", "Vocabulary items", "Grammar items by unit", "Practice questions"],
    [108, 15, 37, 9], unit=" questions")
```


## 8.1 Where objective items sit in the paper

The Curriculum Development Centre (CDC) specification grid for Grade 10 English (2080 curriculum) divides the 75 marks as follows. Check the current grid on the CDC site before the examination, because boards can adjust small details such as the marks of a single task.

| Part | Marks | What is tested | Objective item types |
|---|---|---|---|
| Reading 1: seen text, about 100 words | 5 | comprehension of a textbook passage | one type, often true/false or gap-fill |
| Reading 2: seen text, about 200 words | 10 | comprehension | two types, such as multiple-choice and short answer |
| Reading 3: unseen text, about 200 words | 10 | story, notice, advertisement, letter, news story | two types |
| Reading 4: unseen text, about 300 words | 15 | essay, article, biography, review | three types, including vocabulary |
| Writing: guided and free tasks | 25 | five-to-nine-mark writing tasks | none (marked on a scale) |
| Grammar | 10 | ten one-mark items | reproduction and multiple-choice in context |

```figure caption="Marks of the Grade 10 English paper by part. Reading carries more than half of the 75 marks, and most reading items are objective or short-answer."
import matplotlib.pyplot as plt
labels = ["Reading 4 (unseen, 300 w)", "Reading 2 (seen, 200 w)", "Reading 3 (unseen, 200 w)", "Reading 1 (seen, 100 w)", "Grammar", "Writing (4 tasks)"]
vals = [15, 10, 10, 5, 10, 25]
order = sorted(range(len(vals)), key=lambda i: vals[i])
fig, ax = plt.subplots(figsize=(4.8, 2.7))
y = list(range(len(order)))
ax.barh(y, [vals[i] for i in order], height=0.6, color=ACCENT)
for yi, i in zip(y, order):
    ax.text(vals[i] + 0.4, yi, str(vals[i]), va="center", fontsize=8.5, color=INK)
ax.set_yticks(y); ax.set_yticklabels([labels[i] for i in order], fontsize=8)
ax.set_xlim(0, 30)
ax.set_xlabel("Marks out of 75", fontsize=8)
ax.tick_params(labelsize=8, length=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

::: tip How to use the bank
Cover the key and answer the items of one unit in five minutes. Mark them. For every error, go back to the passage in the book chapter and find the sentence that gives the answer. For objective reading items, the answer is always *in the text*; your own opinion earns nothing.
:::

## 8.2 Reading items by unit

Each unit below tests the two textbook passages. Items marked T/F are true/false.

### Unit 1: Current Affairs and Issues

1. The article on driverless cars was written by Jenny Cusack for (a) BBC Future (b) The Himalayan Times (c) Nature (d) Time
2. Mcity, the test "town" for driverless cars, belongs to the University of (a) Oxford (b) Tokyo (c) Michigan (d) Delhi
3. The open letter of 7 August 2020 was addressed to (a) Ban Ki-moon (b) Antonio Guterres (c) Kofi Annan (d) Greta Thunberg
4. The charity that wrote the letter asked that children under 18 be included in (a) the Security Council (b) the UN Youth Advisory Group on climate change (c) the World Bank (d) the Olympic Committee
5. T/F: Waymo One is a driverless taxi service that operates in Phoenix, USA.
6. T/F: The article says driverless cars have already solved the problem of human drivers.

::: note Answers: Unit 1
**1.** (a) — Jenny Cusack, BBC Future, 2021.
**2.** (c) — Mcity is at the University of Michigan.
**3.** (b) — Antonio Guterres.
**4.** (b) — the letter asks for children's voices on climate policy.
**5.** True.
**6.** False — cars must still learn to cope with unpredictable human drivers.
:::

### Unit 2: Festivals and Celebrations

1. The Carnevale di Ivrea is held in (a) Spain (b) Italy (c) Brazil (d) Greece
2. The teams who throw oranges are called (a) aranceri (b) matadors (c) gauchos (d) torreros
3. The red hat worn by participants is a symbol of (a) war (b) harvest (c) freedom (d) wealth
4. Chuseok is the harvest festival of (a) Japan (b) South Korea (c) Ghana (d) Iran
5. Match: Homowo / Crop Over / Mehregan with Barbados / Iran / Ghana.
6. T/F: *Thanksgiving Around the World* describes harvest festivals of more than one continent.

::: note Answers: Unit 2
**1.** (b) Italy. **2.** (a) aranceri. **3.** (c) freedom. **4.** (b) South Korea.
**5.** Homowo — Ghana; Crop Over — Barbados; Mehregan — Iran.
**6.** True — the USA, South Korea, Brazil, Liberia, Barbados, Ghana and Iran are covered.
:::

### Unit 3: Health and Wellness

1. In "A Letter from a Patient" the writer is (a) a doctor (b) a nurse (c) the mother of a sick baby (d) a hospital director
2. The mother felt her baby was treated as "not a priority" by (a) a busy nurse (b) the receptionist (c) the cook (d) the driver
3. The speaker in "A Healthy Diet for a Healthy Life" calls the greatest public-health challenge (a) smoking (b) obesity (c) pollution (d) malaria
4. Horizon 2020 is a research fund of about (a) 8 million euros (b) 80 million euros (c) 80 billion euros (d) 800 billion euros
5. T/F: The speaker asks EU member states to work separately on food research.
6. T/F: The mother's letter complains that a chart contained a mistake.

::: note Answers: Unit 3
**1.** (c). **2.** (a). **3.** (b) obesity. **4.** (c) about 80 billion euros.
**5.** False — he asks them to cooperate and to use a multidisciplinary approach.
**6.** True — a wrong chart is one of her complaints.
:::

### Unit 4: Work and Leisure

1. In "Cabbage White" the children get work (a) in a shop (b) picking caterpillars off cabbages (c) in a school (d) driving a tractor
2. The children destroy the field while trying to (a) water it (b) kill the butterflies (c) harvest it (d) fence it
3. *Leave This Chanting and Singing* is poem 11 of (a) *Gitanjali* (b) *The Gardener* (c) *Crescent Moon* (d) *Fruit-Gathering*
4. Tagore won the Nobel Prize in Literature in (a) 1903 (b) 1913 (c) 1923 (d) 1933
5. In the poem, *dost* means (a) does (b) did (c) will (d) shall
6. T/F: The poem says God is found with those who do honest work such as the tiller and the path-maker.

::: note Answers: Unit 4
**1.** (b). **2.** (b). **3.** (a). **4.** (b) 1913.
**5.** (a) — *dost* is the old form of *do* with *thou*.
**6.** True — honest toil is worship.
:::

### Unit 5: Science and Experiment

1. Water boils when its vapour pressure equals (a) its colour (b) the external pressure (c) its mass (d) the room temperature
2. At higher altitude, water boils at a (a) higher temperature (b) lower temperature (c) same temperature (d) negative temperature
3. The poet of "The Voice of the Rain" is (a) Walt Whitman (b) Robert Frost (c) Amy Lowell (d) Thomas Hardy
4. The poem is written in (a) rhyming couplets (b) free verse (c) a sonnet (d) ballad form
5. T/F: In the poem the rain calls itself "the Poem of Earth".
6. T/F: Pulling the plunger of a syringe with warm water in it raises the boiling point.

::: note Answers: Unit 5
**1.** (b). **2.** (b) — pressure is lower, so less heat is needed.
**3.** (a). **4.** (b).
**5.** True.
**6.** False — pulling the plunger lowers the pressure, so the boiling point falls.
:::

### Unit 6: Food and Cuisine

1. Haggis is a traditional food of (a) Japan (b) Scotland (c) Vietnam (d) France
2. Shiokara comes from (a) Japan (b) China (c) Australia (d) Scotland
3. The Nepali chef interviewed in the unit is (a) Santosh Shah (b) Gordon Ramsay (c) Sanjeev Kapoor (d) Rajesh Shrestha
4. His restaurant mentioned in the interview is called (a) Dhaulagiri (b) Ayla (c) Annapurna (d) Himal
5. The idiom *a bridge too far* means (a) a long journey (b) too extreme (c) a short cut (d) a big success
6. T/F: The first text says taste in food is cultural.

::: note Answers: Unit 6
**1.** (b). **2.** (a). **3.** (a) Santosh Shah (MasterChef: The Professionals, 2020, BBC One). **4.** (b) Ayla.
**5.** (b). **6.** True.
:::

### Unit 7: Cyber Security

1. In "Parents" the mother wrongly thinks the father is (a) a thief (b) a suspicious stranger (c) a teacher (d) a policeman
2. The main theme of "Parents" is (a) the generation gap and online safety (b) sports (c) farming (d) a festival
3. How many pieces of advice does the internet-safety text give? (a) four (b) six (c) eight (d) ten
4. Two-factor authentication is advised to (a) speed up the computer (b) add a second proof of identity (c) save data (d) clean the screen
5. Match *lurk* with (a) to hide and wait (b) to shout (c) to run (d) to forget.
6. T/F: The text advises keeping backups of your data.

::: note Answers: Unit 7
**1.** (b). **2.** (a). **3.** (c) eight. **4.** (b). **5.** (a). **6.** True.
:::

### Unit 8: Hobbies and Interests

1. Which of these is *not* named as a common hobby in the text? (a) reading (b) painting (c) knitting (d) mountaineering
2. The poem "Climbing" is by (a) Amy Lowell (b) Emily Dickinson (c) Tagore (d) Frost
3. The child in the poem climbs (a) a hill (b) an apple tree (c) a ladder (d) a staircase of stone
4. The message of the poem is that (a) trees are dangerous (b) determination can carry us to the top (c) children should stay home (d) light is harmful
5. T/F: The text says a hobby can become a career.
6. T/F: The poem uses light imagery to describe the imagined town.

::: note Answers: Unit 8
**1.** (d) — the list is reading, dancing, painting, antiques, photography, journaling and knitting.
**2.** (a). **3.** (b). **4.** (b). **5.** True. **6.** True — the town is "shining".
:::

### Unit 9: History and Culture

1. Pratap Malla was king of (a) Bhaktapur (b) Kantipur (c) Lalitpur (d) Gorkha
2. He took the title (a) Kabindra (b) Mahendra (c) Narendra (d) Surendra
3. Which structure is linked with Pratap Malla? (a) Rani Pokhari (b) Nyatapola (c) Dharahara (d) Narayanhiti
4. In Russian flower etiquette, the red carnation stands for (a) patriotism (b) bad luck (c) healing (d) break-up
5. Chamomile is associated with (a) healing (b) war (c) wealth (d) luck
6. T/F: Yellow flowers are thought to signal a break-up.

::: note Answers: Unit 9
**1.** (b). **2.** (a). **3.** (a). **4.** (a). **5.** (a). **6.** True.
:::

### Unit 10: Games and Sports

1. The ancient Olympic Games began at Olympia in (a) 776 BCE (b) 1896 CE (c) 500 BCE (d) 1000 CE
2. The modern Games began in Athens in (a) 1876 (b) 1896 (c) 1906 (d) 1936
3. In the myth, Pelops won Hippodamia by (a) a chariot race (b) a wrestling match (c) a foot race (d) a riddle
4. Basketball was invented by (a) Naismith (b) Pelops (c) Tantalus (d) Olympia
5. The Olympic torch is lit from (a) a candle (b) the sun's rays (c) a gas stove (d) lightning
6. T/F: Football and basketball need costly equipment.

::: note Answers: Unit 10
**1.** (a). **2.** (b). **3.** (a) — the king's chariot wheel pins were replaced by wax. **4.** (a). **5.** (b).
**6.** False — they need cheap equipment, which is why they are so popular.
:::

### Unit 11: Ethics and Morality

1. In "Wisdom of Little Girls" the quarrel begins with (a) a splash in a puddle (b) a stolen cow (c) a lost purse (d) a broken window
2. The calm in the end is brought by (a) the police (b) the grandmother (c) the priest (d) the king
3. The story is a version of a tale by (a) Tolstoy (b) Dickens (c) Chekhov (d) Poe
4. In "World Record" Albert stands in hot soup for (a) 7 h 2 min (b) 7 h 3 min (c) 3 h 7 min (d) 2 h 7 min
5. Albert's rival record to beat is (a) 7 h 2 min (b) 7 h 3 min (c) 8 h (d) 6 h
6. T/F: The play makes fun of the craze for setting records.

::: note Answers: Unit 11
**1.** (a). **2.** (b). **3.** (a). **4.** (a). **5.** (b) — he stands 7 h 2 min against a record of 7 h 3 min. **6.** True — it is a satire.
:::

### Unit 12: Nature and Development

1. The Fast Track runs from Khokana to (a) Nijgadh (b) Birgunj (c) Butwal (d) Hetauda
2. Its length is about (a) 52.5 km (b) 62.5 km (c) 72.5 km (d) 92.5 km
3. Wordsworth's sonnet was written in (a) 1792 (b) 1802 (c) 1812 (d) 1822
4. The sestet of a Petrarchan sonnet has the rhyme (a) abbaabba (b) cdcdcd (c) aabbcc (d) abab
5. "Mighty heart" is a (a) simile (b) metaphor (c) hyperbole (d) irony
6. T/F: The text lists environmental damage as a challenge of the Fast Track.

::: note Answers: Unit 12
**1.** (a). **2.** (c). **3.** (b). **4.** (b) — the octave is *abbaabba*. **5.** (b) — the city is not literally a heart. **6.** True.
:::

### Unit 13: Population and Migration

1. World population in 1950 was just over (a) 1 billion (b) 2.5 billion (c) 4 billion (d) 6 billion
2. The fastest growth was about 2.1% a year in the (a) 1930s (b) 1960s (c) 1990s (d) 2010s
3. The text expects about 9.7 billion people by (a) 2030 (b) 2040 (c) 2050 (d) 2100
4. The peak of about 10.4 billion is expected in the (a) 2030s (b) 2050s (c) 2080s (d) 2100s
5. Birds are not said to migrate for (a) food (b) breeding (c) climate (d) examinations
6. T/F: Sub-Saharan Africa is described as a fast-growing region.

::: note Answers: Unit 13
**1.** (b). **2.** (b). **3.** (c). **4.** (c). **5.** (d). **6.** True.
:::

### Unit 14: Travel and Adventure

1. In "Expect the Unexpected" the town known for paragliding and the Sarangkot sunrise is (a) Pokhara (b) Chitwan (c) Janakpur (d) Dharan
2. Chitwan is described as suitable for (a) active travellers who like a jeep safari and canoeing (b) skiers (c) deep-sea divers (d) only pilgrims
3. "Weathers" was written by (a) Thomas Hardy (b) Wordsworth (c) Kipling (d) Tennyson
4. The refrain of each stanza is (a) "And so do I" (b) "Nevermore" (c) "Come away" (d) "So it goes"
5. In the poem, the weather *shunned* by the speaker is (a) spring weather (b) winter weather (c) the weather of June (d) none
6. T/F: The text says Pashupatinath and the Durbar squares are World Heritage Sites.

::: note Answers: Unit 14
**1.** (a). **2.** (a). **3.** (a). **4.** (a). **5.** (b) — winter weather is shunned and spring weather is liked. **6.** True.
:::

### Unit 15: People and Places

1. Jhamak Ghimire's autobiography is (a) *Jiwan Kada Ki Phool* (b) *Muna Madan* (c) *Sumnima* (d) *Basain*
2. She writes with her (a) right hand (b) left foot (c) mouth (d) right foot
3. The book won the Madan Puraskar in (a) 2000 (b) 2005 (c) 2010 (d) 2015
4. Sugarloaf Mountain stands at the entrance to (a) Guanabara Bay (b) Hudson Bay (c) Bay of Bengal (d) Botany Bay
5. Its height is about (a) 196 m (b) 396 m (c) 896 m (d) 1,396 m
6. T/F: Two cable cars take visitors up Sugarloaf Mountain, via Morro da Urca.

::: note Answers: Unit 15
**1.** (a). **2.** (b) — she writes with her left foot. **3.** (c) 2010. **4.** (a). **5.** (b). **6.** True.
:::

### Unit 16: Success and Celebration

1. Walt Disney's first successful character, created in 1928, was (a) Donald Duck (b) Mickey Mouse (c) Goofy (d) Pluto
2. *Snow White* appeared in (a) 1928 (b) 1937 (c) 1955 (d) 1966
3. Disneyland opened in (a) 1937 (b) 1950 (c) 1955 (d) 1965
4. Kipling's poem "If" was published in (a) 1810 (b) 1910 (c) 1930 (d) 1950
5. The poem ends with the promise (a) "you'll be a Man, my son!" (b) "and so do I" (c) "we shall overcome" (d) "all is well"
6. T/F: The text says Walt Disney's first company went bankrupt.

::: note Answers: Unit 16
**1.** (b). **2.** (b). **3.** (c). **4.** (b). **5.** (a). **6.** True.
:::

### Unit 17: Countries and Towns

1. The rivers of London and Paris are (a) the Thames and the Seine (b) the Rhine and the Danube (c) the Nile and the Congo (d) the Tiber and the Po
2. Which city is almost fifteen times larger? (a) London (b) Paris
3. London has about (a) 24 museums (b) 240 museums (c) 2,400 museums (d) 40 museums
4. In the fable the country mouse finally chooses (a) the feast in the city (b) plain food in peace (c) a palace (d) a ship
5. The moral of the fable is that (a) peace is worth more than luxury (b) cities are best (c) mice are clever (d) food is cheap
6. T/F: The text says Paris is better for food and slightly cheaper.

::: note Answers: Unit 17
**1.** (a). **2.** (a) London. **3.** (b). **4.** (b). **5.** (a). **6.** True.
:::

### Unit 18: Media and Entertainment

1. *Hachi: A Dog's Tale* was directed by (a) Lasse Hallström (b) Steven Spielberg (c) Ang Lee (d) Ridley Scott
2. The leading actor is (a) Richard Gere (b) Tom Hanks (c) Brad Pitt (d) Will Smith
3. The film is based on the true story of Hachikō of (a) Osaka (b) Tokyo (c) Kyoto (d) Seoul
4. The social-media account *We Rate Dogs* raised about (a) 700 US dollars for a wheelchair (b) 7 US dollars (c) 7,000 pounds (d) nothing
5. The New York hawk was rescued through (a) Twitter (b) radio (c) a newspaper (d) a letter
6. T/F: The review praises the bond between the dog and his master.

::: note Answers: Unit 18
**1.** (a). **2.** (a). **3.** (b). **4.** (a). **5.** (a). **6.** True.
:::

## 8.3 Vocabulary items

The long unseen passage (Reading 4) always carries a vocabulary item; the seen passages test words from the book. Choose the best meaning or fill the gap.

**A. Choose the word closest in meaning to the underlined word (1 mark each)**

1. The mountain village has a calm *serene* atmosphere. (a) noisy (b) peaceful (c) crowded (d) dirty
2. She was *obsessed* with her phone. (a) bored by (b) unable to stop thinking about (c) afraid of (d) angry with
3. Dark clouds began to *lurk* above the hills. (a) hide and wait (b) disappear (c) sing (d) fall
4. The *altitude* of Kathmandu is about 1,400 m. (a) width (b) height above sea level (c) temperature (d) population
5. The shopkeeper *swerved* to avoid the cow. (a) stopped (b) turned suddenly aside (c) shouted (d) jumped
6. The rice was *scarce* after the flood. (a) plentiful (b) hard to find (c) cheap (d) tasty

**B. Choose the opposite (1 mark each)**

7. *ancient* (a) old (b) modern (c) ruined (d) valuable
8. *expand* (a) grow (b) shrink (c) shout (d) cover
9. *generous* (a) kind (b) selfish (c) rich (d) bright
10. *bright* (a) dull (b) shiny (c) clever (d) warm

**C. Fill the gap with the best word from the box (1 mark each)**

Box: *determination, valuable, humble, peaceful, perseverance*

11. His ____ helped him to keep working after he failed three times.
12. In spite of fame, the chef remained ____ and thanked his teachers.
13. Walt Disney's ____ is a good lesson for every student.
14. The ____ countryside is a pleasant escape from the noisy city.

**D. Prefixes, suffixes and compounds (1 mark each)**

15. Add a prefix to make the opposite of *possible*. 16. Add a suffix to *care* to mean "without care". 17. Make an adjective from *danger*. 18. Write the compound word from Unit 9 that means "the act of giving presents". 19. The word *cardboard* is made of two nouns. Write them.

::: note Answers: vocabulary
**1.** (b) peaceful. **2.** (b). **3.** (a). **4.** (b). **5.** (b). **6.** (b).
**7.** (b) modern. **8.** (b) shrink. **9.** (b) selfish. **10.** (a) dull.
**11.** determination (or perseverance). **12.** humble. **13.** perseverance (or determination). **14.** peaceful.
**15.** impossible. **16.** careless. **17.** dangerous. **18.** gift-giving. **19.** card + board.
:::

::: caution Compound words
The SEE checks compound items against the words in the book: gift-giving, heart-warming, cardboard, flower etiquette, break-up, fortune-telling, newly-wed. Learn them as a list.
:::


## 8.4 Grammar items by unit

The CDC grid asks ten one-mark grammar items covering articles, prepositions, tenses, connectives, question tags, reported speech, voice, conditionals, subject-verb agreement, relative clauses and causatives. Practise by unit; the sets below follow the book's order.

### Reported speech: statements, questions, commands (Units 1 to 3)

Change into reported speech (1 mark each).

1. "I am tired," said Ram. 2. "We will go to Pokhara tomorrow," said the girls. 3. "Did you finish the work?" the teacher asked Sita. 4. "Where do you live?" he asked me. 5. "Please close the door," she said to him. 6. "Don't touch the wire," the mother told the child. 7. "The earth moves round the sun," the teacher said. 8. "I have lost my pen," said Hari.

::: note Answers: reported speech
**1.** Ram said that he was tired.
**2.** The girls said that they would go to Pokhara the next day.
**3.** The teacher asked Sita if (whether) she had finished the work.
**4.** He asked me where I lived.
**5.** She requested him to close the door.
**6.** The mother told the child not to touch the wire.
**7.** The teacher said that the earth moves round the sun. (no backshift for a universal truth)
**8.** Hari said that he had lost his pen.
:::

### Modals and imperatives (Unit 4)

Choose the correct word (1 mark each).

1. You ____ wear a helmet; it is the law. (a) can (b) must (c) may (d) might
2. "____ I borrow your pen?" (a) May (b) Must (c) Would (d) Shall to
3. He ____ have missed the bus; he is not here. (a) must (b) can (c) should (d) will
4. You look pale. You ____ see a doctor. (a) should (b) can't (c) used (d) shall
5. ____ you help me with this bag? (a) Could (b) Might to (c) Ought (d) Dare
6. She ____ to get up early when she was a child. (a) has (b) had (c) must (d) would be

::: note Answers: modals
**1.** (b) must — legal compulsion. **2.** (a) May — permission. **3.** (a) must — certainty. **4.** (a) should — advice. **5.** (a) Could — polite request. **6.** (b) had — *had to* is the past of *have to*.
:::

### Conditionals (Unit 5)

Fill in with the correct form (1 mark each).

1. If you heat ice, it ____ (melt). 2. If it rains tomorrow, we ____ (stay) at home. 3. If I ____ (be) a bird, I would fly to Lukla. 4. If she had studied, she ____ (pass). 5. ____ you hurry, you will miss the bus. (unless/if) 6. I will lend you the book provided you ____ (return) it. 7. If he ____ (leave) earlier, he would have caught the bus. 8. ____ I known, I would have come. (inverted)

::: note Answers: conditionals
**1.** melts (zero conditional). **2.** will stay. **3.** were (second conditional uses *were* for all persons). **4.** would have passed. **5.** Unless — *Unless you hurry* means *If you do not hurry*, and the result is that you miss the bus. **6.** return (present after *provided*). **7.** had left. **8.** Had.
:::

### Present continuous and reasons (Unit 6)

Choose the correct word (1 mark each).

1. Look! The chef ____ the soup. (a) stirs (b) is stirring (c) stirred (d) has stirring
2. We ____ to Pokhara next week; the tickets are booked. (a) go (b) are going (c) went (d) have gone
3. He stayed at home ____ he was ill. (a) because (b) because of (c) in spite of (d) so
4. He stayed at home ____ his illness. (a) because (b) because of (c) although (d) but
5. She went to the market ____ buy vegetables. (a) for (b) in order to (c) so (d) because
6. They are saving money ____ they can buy a house. (a) so that (b) in order (c) although (d) to

::: note Answers: reasons
**1.** (b) — action happening now. **2.** (b) — planned future. **3.** (a) — *because* + clause. **4.** (b) — *because of* + noun. **5.** (b) — purpose with the base verb. **6.** (a) — *so that* + clause.
:::

### Articles and advice (Unit 7)

Fill in with *a*, *an*, *the* or X for no article (1 mark each).

1. He is ____ honest boy. 2. She works at ____ university in Kathmandu. 3. ____ Sun rises in the east. 4. Ram plays ____ football every evening. 5. I saw ____ one-eyed man. 6. ____ Himalayas are in the north of Nepal. 7. You ____ keep your password secret. (should/must not) 8. You ____ share your password with strangers. (must not/should)

::: note Answers: articles
**1.** an (honest begins with a vowel sound). **2.** a (university begins with a consonant sound, /j/). **3.** The (unique). **4.** X (games take no article). **5.** a (one begins with /w/). **6.** The (mountain range). **7.** should (advice). **8.** must not (prohibition).
:::

### Passive voice (Units 8 and 10)

Change into the passive voice (1 mark each).

1. Sita writes a letter. 2. The farmers are planting rice. 3. They built a bridge last year. 4. The teacher has corrected the exercise books. 5. Who wrote this poem? 6. Someone will finish the work tomorrow. 7. The committee should have decided the matter. 8. They are showing a film tonight.

::: note Answers: passive
**1.** A letter is written by Sita.
**2.** Rice is being planted by the farmers.
**3.** A bridge was built last year.
**4.** The exercise books have been corrected by the teacher.
**5.** By whom was this poem written? (or: Who was this poem written by?)
**6.** The work will be finished by someone tomorrow. (or: The work will be finished tomorrow.)
**7.** The matter should have been decided by the committee.
**8.** A film is being shown tonight.
:::

### Present perfect and agreement (Units 10 and 11)

Choose the correct word (1 mark each).

1. I ____ here since 2020. (a) live (b) have lived (c) am living (d) lived
2. She has been waiting ____ two hours. (a) since (b) for (c) from (d) by
3. A number of students ____ absent today. (a) is (b) are (c) was (d) has been
4. The number of students ____ increasing. (a) are (b) is (c) were (d) have
5. Neither the teacher nor the students ____ present. (a) was (b) were (c) is (d) has
6. Each of the boys ____ a ticket. (a) have (b) has (c) are (d) were
7. He doesn't know, ____? (tag) 8. Nobody came, ____ they?

::: note Answers: perfect and agreement
**1.** (b) — *since* + point in time takes the present perfect. **2.** (b) — *for* + period. **3.** (b) — *a number of* is plural. **4.** (b) — *the number of* is singular. **5.** (b) — verb agrees with the nearer subject (*students*). **6.** (b) — *each* is singular. **7.** does he. **8.** did — *nobody* makes the clause negative, so the tag is positive; the pronoun is *they*.
:::

### Future forms and connectives (Units 12 and 13)

Choose the correct word (1 mark each).

1. The train ____ at 6 a.m. tomorrow (timetable). (a) leaves (b) is leaving (c) will have left (d) left
2. Look at those clouds. It ____ rain. (a) will (b) is going to (c) shall (d) is raining
3. By next year I ____ my SEE. (a) will pass (b) will have passed (c) pass (d) am passing
4. ____ it was raining, we played football. (a) Because (b) Although (c) So (d) Unless
5. ____ the heavy rain, the match went on. (a) Although (b) Despite (c) Though (d) Even though
6. The road is useful. ____, it harms the environment. (a) However (b) Because (c) Although (d) Despite

::: note Answers: future and connectives
**1.** (a) timetable. **2.** (b) — plan or prediction from evidence. **3.** (b) — completed before a future time. **4.** (b). **5.** (b) — *despite* is followed by a noun phrase. **6.** (a) — *however* takes a comma and starts a new sentence. Never use *although … but* together.
:::

### Question tags and relative clauses (Units 14 and 15)

Add a question tag or fill in the relative word (1 mark each).

1. You are a student, ____? 2. Let's go home, ____? 3. Open the window, ____? 4. I am late, ____? 5. The girl ____ won the prize is my cousin. 6. This is the pen ____ I bought yesterday. 7. The man ____ car was stolen called the police. 8. Pokhara, ____ is a lake city, attracts tourists. 9. He never lies, ____?

::: note Answers: tags and relatives
**1.** aren't you. **2.** shall we. **3.** will you. **4.** aren't I. **5.** who. **6.** which (or that). **7.** whose. **8.** which (non-defining; *that* is not allowed). **9.** does he — *never* is negative in sense, so the tag is positive.
:::

### Prepositions (Units 15 and 16)

Fill in with the correct preposition (1 mark each).

1. The class starts ____ 10 a.m. 2. He was born ____ Monday. 3. They came to Nepal ____ 2015. 4. She is afraid ____ dogs. 5. I am good ____ mathematics. 6. He divided the money ____ his two sons. 7. We stayed ____ Friday ____ Sunday. (from … to) 8. The book is ____ the table.

::: note Answers: prepositions
**1.** at (clock time). **2.** on (day). **3.** in (year). **4.** of (afraid of). **5.** at (good at). **6.** between (two persons). **7.** from … to. **8.** on (surface).
:::

### Adverbs, comparison and causatives (Units 17 and 18)

Choose the correct word (1 mark each).

1. She sings ____. (a) beautiful (b) beautifully (c) beauty (d) more beauty
2. He is the ____ boy in the class. (a) taller (b) tallest (c) more tall (d) most tall
3. This book is ____ than that one. (a) good (b) better (c) best (d) more good
4. She ____ the barber cut her hair. (a) had (b) made to (c) was (d) got to
5. He ____ his car repaired yesterday. (a) had (b) made (c) let (d) told
6. The teacher ____ us write an essay. (a) made (b) got (c) was made (d) forced to

::: note Answers: adverbs and causatives
**1.** (b) — adverb of manner. **2.** (b) — superlative of a short adjective. **3.** (b) — irregular *good, better, best*. **4.** (a) — *have + person + base verb*. **5.** (a) — *have + thing + past participle*. **6.** (a) — *make + person + base verb*.
:::

## Chapter summary

- The paper is 75 marks in 3 hours: Reading 40 (5 + 10 + 10 + 15), Writing 25 and Grammar 10. Objective and short-answer items fill most of the reading part.
- Answer reading items from the text. Read the question first, then find the line.
- Tag questions reverse polarity: *aren't I*, *shall we* (after *let's*), *will you* (after commands), *they* (after *nobody*, *everyone*).
- Reported speech steps the tense back after a past reporting verb but not for universal truths; commands take *to* or *not to*.
- Conditionals: zero (present, present), first (present, will), second (past, would), third (past perfect, would have). *Unless* means *if not*.
- *A number of* is plural; *the number of* is singular; *each*, *everyone* are singular; with *neither … nor* the verb agrees with the nearer subject.
- Passive is *be + past participle* in the tense of the active verb; use *by + agent* only when it matters.

## Practice questions

**Reading items (1 mark each)**

1. Who wrote the open letter that asks for children to be heard on climate change? <span class="marks">[1]</span>
   (a) Save the Children (b) The BBC (c) Waymo (d) Oxbotica
2. Which poem uses the refrain "And so do I"? <span class="marks">[1]</span>
   (a) Weathers (b) If (c) Climbing (d) The Voice of the Rain
3. True or false: In "World Record", Albert stands in soup for more than the existing record. <span class="marks">[1]</span>
4. Jhamak Ghimire writes with her ____. <span class="marks">[1]</span>

::: note Answers to Reading items
**1.** (a) — the letter is from Save the Children.
**2.** (a) — Hardy's "Weathers".
**3.** False — he stands 7 h 2 min against a record of 7 h 3 min.
**4.** left foot.
:::

**Grammar items (1 mark each)**

1. Report: "Where do you live?" he asked me. <span class="marks">[1]</span>
2. Passive: They are building a road. <span class="marks">[1]</span>
3. Add a tag: Let's go, ____? <span class="marks">[1]</span>
4. Fill in: If I ____ you, I would apologise. <span class="marks">[1]</span>
5. Choose: She stayed at home ____ her illness. (because / because of) <span class="marks">[1]</span>

::: note Answers to Grammar items
**1.** He asked me where I lived.
**2.** A road is being built.
**3.** shall we.
**4.** were.
**5.** because of — a noun phrase follows.
:::

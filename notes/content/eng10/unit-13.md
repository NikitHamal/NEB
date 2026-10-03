---
subject: Compulsory English
grade: 10
unit: 13
title: 'Unit 13: Population and Migration'
hours: 0
area: Units
---

People are born, people die, and people move. These three facts decide how many of us live in each country and what our world will look like in the future. This unit has two reading texts. The first, "A Century of World Population Trends: 1950 to 2050", is a data-rich article about how fast the world's population has grown and how it will change. The second, "Discovering Migration: What Birds Reveal", looks at one of nature's most amazing journeys, bird migration. The grammar is **connectives of contrast** (*although, despite, however, yet …*) and the writing tasks are **interpreting graphs and charts** and an **opinion essay** on the migration of Nepali youth.

::: key What the examiner wants from this unit
Facts and figures from the first text, quoted exactly. A clear explanation of how birds migrate in the second. In grammar: using *although / in spite of / however* in the correct pattern. In writing: a graph interpretation that states the topic, the highest and lowest values, the trend and a conclusion, and an essay with an introduction, balanced body and conclusion.
:::

## 13.1 A Century of World Population Trends: 1950 to 2050

### About the text

The article is an **informative report** based on the projections of the United Nations (UN) on world population. A "projection" is a calculation of what numbers are likely to be in the future if present trends continue. The writer uses numbers, percentages and the names of regions, so the passage is full of **demographic vocabulary** — words about population such as *fertility, mortality, peak, trajectory*. Read slowly and keep a note of every figure.

### Summary

**Growth over the last century.** In the middle of the twentieth century (about 1950) the world's population was a little over **2.5 billion**. It then grew faster than ever before. At its fastest, in the 1960s, the growth rate was around **2.1 per cent a year**. Today the rate is below 1 per cent a year, because on average families have fewer children than before.

**What decides the population.** Only two things change the size of a population over time (apart from migration): **fertility**, the number of children born, and **mortality**, the number of deaths. If fertility rises, the population rises; if mortality rises, growth falls.

**The next decades.** The United Nations projects that the world's population will reach about **8.5 billion** around 2030 and **9.7 billion** by 2050. It may peak at around 10.4 billion in the 2080s and then become stable or fall. Different regions will follow very different paths:

- **Eastern and South-Eastern Asia** had about 2.3 billion people in the early 2020s. China and India together make up most of the region's and the world's population. India is expected to surpass China as the world's most populous country (the UN estimated this would happen in 2023).
- **Sub-Saharan Africa** has the fastest growth. Its population is likely to pass 2 billion by the end of the 2040s.
- **Europe and Northern America** have such low fertility that their populations will begin to fall from about the late 2030s.
- Over half the growth in world population to 2050 will come from eight countries: the Democratic Republic of the Congo, Egypt, Ethiopia, India, Nigeria, Pakistan, the Philippines and the United Republic of Tanzania.

```figure caption="World population, 1950 to 2050 (billions, rounded UN estimates and projections)."
import matplotlib.pyplot as plt
yrs = [1950,1960,1970,1980,1990,2000,2010,2020,2030,2040,2050]
pop = [2.5,3.0,3.7,4.4,5.3,6.1,6.9,7.8,8.5,9.2,9.7]
fig, ax = plt.subplots(figsize=(4.9,2.8))
ax.plot(yrs[:8],pop[:8],color=ACCENT,lw=2.2,marker='o',ms=3.5)
ax.plot(yrs[7:],pop[7:],color=ACCENT,lw=2.2,ls='--',marker='o',ms=3.5)
for x,y in [(1950,2.5),(2020,7.8),(2050,9.7)]:
    ax.annotate(f'{y} bn',(x,y),textcoords='offset points',xytext=(0,7),ha='center',fontsize=7.5,color=INK)
ax.text(2038,6.6,'projection',fontsize=7.5,color=MUTED,rotation=0)
ax.text(1962,5.4,'estimates',fontsize=7.5,color=MUTED)
ax.set_ylim(0,11); ax.set_xlim(1945,2055)
ax.set_ylabel('Billion people',fontsize=8,color=MUTED)
ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',color=GRID,lw=0.6)
ax.tick_params(labelsize=7.5,colors=MUTED)
```

### Glossary

| Word | Meaning | Example |
|---|---|---|
| populous | having a large population | India is the most populous country. |
| mortality | the number of deaths in a place or period | Infant mortality has fallen. |
| projection | an estimate of future figures | The projection shows rapid growth. |
| demographic | connected with the study of population | Demographic data come from the census. |
| peak | to reach the highest point | Growth peaked in the 1960s. |
| stabilization | becoming steady, unlikely to change | Stabilization of prices helped. |
| trajectory | the path followed by something | The country's economic trajectory is upward. |
| surpass | to be greater than | Her score surpassed all records. |
| disparate | completely different | They came from disparate backgrounds. |

### Comprehension questions with model answers

**A. Objective questions (1 mark each)**

1. The highest growth rate of world population in the past century was about <span class="marks">[1]</span>
   (a) 0.5 per cent (b) 1.2 per cent (c) 2.1 per cent (d) 4 per cent
2. The two factors that decide population growth are <span class="marks">[1]</span>
   (a) fertility and mortality (b) trade and tourism (c) education and health (d) food and land
3. The world population is projected to be about 9.7 billion by <span class="marks">[1]</span>
   (a) 2030 (b) 2040 (c) 2050 (d) 2100
4. Write **True** or **False**: Europe and Northern America will keep growing rapidly. <span class="marks">[1]</span>

::: note Answers — objective
**1.** (c) 2.1 per cent. **2.** (a) fertility and mortality. **3.** (c) 2050. **4.** False. Their populations will begin to fall because of low fertility.
:::

**B. Short questions (2 marks each)**

1. What was the size of world population in the mid-twentieth century? <span class="marks">[2]</span>
2. Why has the growth rate declined in recent years? <span class="marks">[2]</span>
3. How do fertility and mortality affect population size? <span class="marks">[2]</span>
4. Which countries make up the largest part of the population of Eastern and South-Eastern Asia? <span class="marks">[2]</span>
5. Name four countries that will contribute most to world population growth by 2050. <span class="marks">[2]</span>

::: note Answers — short
**1.** It was a little over 2.5 billion.

**2.** The growth rate has fallen because the fertility rate is lower: on average, families have fewer children than before.

**3.** They are the two main causes of population change. Higher fertility adds people and so increases the population; higher mortality removes people and so slows growth.

**4.** China and India.

**5.** The Democratic Republic of the Congo, Egypt, Ethiopia and India (also Nigeria, Pakistan, the Philippines and Tanzania).
:::

**C. Long questions (4 marks each)**

1. Why will different regions have different population changes in the next thirty years? <span class="marks">[4]</span>
2. Do you think the world population will increase as projected? Discuss. <span class="marks">[4]</span>

::: note Answers — long
**1.** Regions will change differently because their rates of fertility and mortality are different. In sub-Saharan Africa fertility is still high, so the population will more than double over several decades and pass 2 billion by the 2040s. In Europe and Northern America fertility is low, so the number of deaths will exceed births and the population will begin to fall by the late 2030s. In Asia, China's population is expected to decline while India's keeps growing for some time. As a result, the world's population will grow, but unevenly.

**2.** (Open answer.) I think the population will probably grow more slowly than projected. First, education, especially of girls, is spreading, and educated people choose to have fewer children. Second, the cost of bringing up children is high and many families now prefer small families. Third, health care and family planning are improving. However, if mortality falls greatly in poor countries the numbers may still rise, so the projection may be close to the truth in some regions.
:::

## 13.2 Discovering Migration: What Birds Reveal

### About the text

This is a **popular-science article**: it explains a scientific topic in simple language for the general reader. It begins with a question that puzzled people for centuries: where do birds go when winter comes? It then shows what scientists know today about **migration** — the regular movement of animals from one region to another according to the season. Notice that the writer moves from the *past* (old beliefs) to the *present* (modern knowledge) and ends with what we can still learn from the birds.

### Summary

**Old beliefs.** In the past, people could not explain why birds disappeared in autumn and returned in spring. They had a misconception that birds hid underground, or turned into other birds. We now know that most of them travel, sometimes thousands of kilometres.

**Incredible journeys.** The most amazing thing about migration is that birds cross lands and oceans **without roadmaps**. They must judge weather, food, resting places (called **stopovers**) and the dangers of the route. Birds are not the only migrants: fish, mammals, reptiles and amphibians also migrate.

**Different ways of migrating.**

- Some birds fly **at night**, and their dark shapes can be seen crossing the moon on spring nights. Night flight gives cool air and calmer winds and lets them feed by day.
- Some **travel in large flocks**, which gives better flying conditions and protection.
- Some, such as sea terns, cannot rest on water for long because their feathers become **waterlogged**, so they must keep flying or find land.
- **Scoters**, sea ducks, dive to the sea floor to catch shellfish before moving on.
- Mountain birds like the brindled titmouse and mountain chickadee do not go north to south at all. They **move up and down the mountain**, from high ground to lower elevations in winter.
- In **partial migration**, some birds of a species migrate while others of the same species stay at home.

**Fuel for the journey.** Birds feed on flying insects as they travel, or stop at stopovers to feed on grain and other food and to refuel for the next stage. In spring, when the weather is favourable, they fly back to their breeding grounds.

```photo id="eng10/arctic-tern" caption="The Arctic tern (Sterna paradisaea) makes the longest known migration of any animal, flying from the Arctic to the Antarctic and back each year." width="75"
```

### Glossary

| Word | Meaning |
|---|---|
| transform | to change completely |
| incredible | very hard to believe; amazing |
| roadmap | a plan or guide showing the way |
| retrace | to go back over the same path |
| elevation | height above sea level |
| waterlogged | so full of water that it cannot work properly |
| refuel | to supply with energy again |
| cluster | a close group |
| crucial | extremely important |
| perilous | very dangerous |

**Synonyms and antonyms (from the exercise)**

| Word | Synonym | Antonym |
|---|---|---|
| transform | change | stagnate |
| incredible | unbelievable | credible |
| retrace | backtrack | forget |
| grab | snatch | release |
| elevation | height | lowness |
| waterlogged | soaked | dry |
| refuel | replenish | deplete |
| crucial | vital | trivial |
| perilous | dangerous | harmless |

### Why animals migrate

| Reason | Example |
|---|---|
| Food and water | herds move to fresh grass; birds follow insects |
| Breeding | sea turtles return to beaches to lay eggs |
| Climate | birds leave cold regions in winter |
| Safety | animals avoid dangerous seasons or predators |

### Comprehension questions with model answers

**A. Objective questions (1 mark each)**

1. In the past, people believed that birds <span class="marks">[1]</span>
   (a) hid underground (b) flew to the moon (c) slept in the sea (d) never moved
2. Mountain birds migrate <span class="marks">[1]</span>
   (a) east to west (b) north to south (c) up and down the mountain (d) not at all
3. Scoters dive to catch <span class="marks">[1]</span>
   (a) fish (b) shellfish (c) insects (d) seeds
4. Write **True** or **False**: Only birds migrate. <span class="marks">[1]</span>

::: note Answers — objective
**1.** (a). **2.** (c). **3.** (b) shellfish. **4.** False. Fish, mammals, reptiles and amphibians also migrate.
:::

**B. Short questions (2 marks each)**

1. What is incredible about the migration of birds? <span class="marks">[2]</span>
2. What things do birds consider while flying to their destinations? <span class="marks">[2]</span>
3. What is partial migration? <span class="marks">[2]</span>
4. Why can sea terns not stay long in water? <span class="marks">[2]</span>
5. How do birds feed themselves during their journeys? <span class="marks">[2]</span>

::: note Answers — short
**1.** The incredible thing is that birds fly over land and oceans without any roadmap and still reach the same places each year.

**2.** They consider the weather, the availability of food and the stopovers where they can rest.

**3.** In partial migration, some birds of a species migrate while others of the same species stay in the same place.

**4.** Because their feathers become waterlogged, so they cannot float for long and must find land.

**5.** Some birds catch flying insects as they fly; others stop at stopovers to feed on grain and other food and refuel.
:::

**C. Long question (4 marks)**

1. You may have seen or heard of animals migrating. What could be the reasons for animals to migrate? Discuss. <span class="marks">[4]</span>

::: note Answer
**1.** Animals migrate for several reasons. The first is food: herbivores move to new grazing land when grass dries up, and birds follow insects. The second is breeding: sea turtles travel hundreds of kilometres to lay eggs on the beach where they were born, and many birds return to nesting sites each year. The third is climate: when winter makes the north too cold, birds travel south to find warmth. The fourth is safety, as animals try to avoid dangerous seasons or enemies. Migration is therefore a way to survive and to continue the species.
:::

## 13.3 Grammar and writing tasks

### Grammar I and II — Connectives of contrast

**Connectives of contrast** (concession) join two ideas that seem to oppose each other: *It was raining; we played.* The two ideas are linked in unexpected ways.

| Connective | Pattern | Example |
|---|---|---|
| **although / though / even though** | + full clause (subject + verb) | **Although** it was raining heavily, we continued the match. |
| **despite / in spite of** | + noun / gerund (V-ing) | **In spite of** his hard work, he failed. **Despite** being Nepali, she speaks French. |
| **despite the fact that / in spite of the fact that** | + full clause | He came **despite the fact that** he was ill. |
| **however / nevertheless** | begins a new sentence (or after a semicolon), followed by a comma | I leave early; **however**, I always arrive on time. |
| **yet / but** | joins two clauses | It was snowing heavily, **yet** it was not too cold. |
| **while / whereas** | contrasts two facts | I love cricket **while** my brother loves football. |

```figure caption="Two patterns for the same meaning: clause after although; noun or -ing after despite."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.2))
def box(x,y,w,t,c): 
    ax.add_patch(FancyBboxPatch((x,y),w,0.5,boxstyle='round,pad=0.02,rounding_size=0.08',fc=c,ec=INK,lw=0.8))
    ax.text(x+w/2,y+0.25,t,ha='center',va='center',fontsize=7.4,color=INK)
box(0,1.5,1.6,'Although','#DCE8F8'); box(1.75,1.5,2.6,'she was tired,','#F4F4F4'); box(4.5,1.5,2.4,'she kept working.','#F4F4F4')
box(0,0.5,1.6,'Despite','#F8E7CC'); box(1.75,0.5,2.6,'being tired,','#F4F4F4'); box(4.5,0.5,2.4,'she kept working.','#F4F4F4')
ax.text(3.45,1.2,'clause (subject + verb)',ha='center',fontsize=6.8,color=MUTED)
ax.text(3.45,0.2,'noun or -ing form',ha='center',fontsize=6.8,color=MUTED)
ax.set_xlim(-0.1,7.0); ax.set_ylim(0,2.2); ax.axis('off')
```

**Rules to remember**

1. Never use **although** and **but** together: *Although it rained, but we played* is wrong. Choose one: *Although it rained, we played.*
2. After **despite / in spite of** use a noun or -ing: *despite the rain*, *despite having no money*. If you want a clause, add *the fact that*.
3. **However** needs a full stop or semicolon before it and a comma after: *He tried hard. However, he failed.*
4. **Even though** is stronger than *although*: it stresses the surprise. *Even if* is different, since it means "whether or not".
5. **While** and **whereas** show contrast between two things at the same time; they do not mean "although" in every context.

::: example Worked example 13.1 — join with the connective
**Problem.** Join with *despite*: "She was injured. She completed her assignment."

**Solution.** *Despite* must be followed by a noun or -ing form. *She was injured* becomes *her injury* or *being injured*. Answer: *She completed her assignment despite her injury.* (or *Despite being injured, she completed her assignment.*)
:::

::: example Worked example 13.2 — complete the sentence
**Problem.** Complete: "In spite of ______, he failed the exam."

**Solution.** A noun or -ing form is needed. *In spite of his hard work, he failed the exam.*
:::

::: caution Although … but
Many students write *Although he is rich, but he is unhappy.* Use only one connective: *Although he is rich, he is unhappy* or *He is rich, but he is unhappy.*
:::

**Exercise 1.** Fill in with *although, despite, in spite of, however, yet* or *while*.

1. ______ it was snowing, we did not feel cold.
2. He did not give up smoking ______ the doctor's warnings.
3. I have never been to that town ______ it is not far from my home.
4. She is rich; ______, she is not happy.
5. ______ studying hard, he failed.
6. We were lost ______ we had a map.
7. The food was tasty, ______ the restaurant was not popular.
8. I like tea ______ my brother likes coffee.
9. He came ______ the fact that he was ill.
10. ______ our best efforts, we did not qualify for the final.

::: note Key to Exercise 1
**1.** Although / Even though **2.** in spite of / despite **3.** though / although **4.** however **5.** Despite / In spite of **6.** although / though **7.** yet / although **8.** while **9.** despite / in spite of **10.** Despite / In spite of
:::

**Exercise 2.** Join the pairs using the word in brackets.

1. I was exhausted. I could not sleep. (although)
2. She was shortlisted. She had no experience. (in spite of)
3. The pay was low. I decided to work for the company. (even though)
4. We prepared well. We lost the match. (yet)
5. She had an injury. She completed the assignment. (despite)
6. Ram exercises every day. He is gaining weight. (however)
7. He went to bed late. He woke up early. (in spite of)
8. The team had ten players. It won the match. (nevertheless)

::: note Key to Exercise 2
**1.** Although I was exhausted, I could not sleep. **2.** She was shortlisted in spite of having no experience. **3.** I decided to work for the company even though the pay was low. **4.** We prepared well, yet we lost the match. **5.** She completed the assignment despite her injury. **6.** Ram exercises every day; however, he is gaining weight. **7.** He woke up early in spite of going to bed late. **8.** The team had only ten players; nevertheless, it won the match.
:::

### Writing I — Interpreting a graph or chart

A graph or chart **interpretation** explains in words what the visual shows. Do not just list numbers; describe and conclude.

| Step | What to write |
|---|---|
| 1. Introduction | what the chart is about, the period, the source and the units |
| 2. Highest and lowest | name the largest and smallest values and when they occurred |
| 3. Trend | rise, fall, steady, sharp, gradual |
| 4. Comparison | compare two items with *higher than, twice as many as, whereas* |
| 5. Conclusion | what the data shows overall; a possible reason |

**Useful language:** *rose sharply, increased steadily, fell slightly, remained stable, peaked at, reached a low of, accounted for 40 per cent, a quarter of, the majority.*

```figure caption="Sample chart: how 40 students in Class 10 come to school (illustrative data)."
import matplotlib.pyplot as plt
labels = ['Walk','Bicycle','Bus','Motorbike']
vals = [18,10,8,4]
fig, ax = plt.subplots(figsize=(4.4,2.5))
bars = ax.bar(labels,vals,color=[ACCENT,'#6DA7DA','#9DBFE3','#C9D9EE'])
for b,v in zip(bars,vals):
    ax.text(b.get_x()+b.get_width()/2,v+0.4,str(v),ha='center',fontsize=8,color=INK)
ax.set_ylim(0,22); ax.set_ylabel('Number of students',fontsize=8,color=MUTED)
ax.spines[['top','right']].set_visible(False); ax.tick_params(labelsize=8,colors=MUTED)
```

**Model interpretation.**

The bar chart shows how forty students of Class 10 travel to school. Walking is by far the most common way: 18 students, or 45 per cent of the class, walk. Ten students (25 per cent) ride a bicycle, while eight come by bus. Only four students, one-tenth of the class, are brought by motorbike, the lowest figure. Therefore, almost three-quarters of the class use free or cheap means of transport. This is probably because most students live close to the school and the roads in the locality are not suitable for fast vehicles.

**For the textbook-style tasks.** On a line graph about Nepali students going abroad to study, you would say that the number *increased* from about 10,000 in 2012 to over 63,000 in 2019, with only a short dip at the start, and conclude that more students were seeking better education abroad. For a pie chart of languages in Kathmandu, you would say that Nepali was spoken by the largest share (about 61 per cent), followed by Newar, and that the smaller languages together made up the rest.

### Writing II — The opinion essay

An **essay** presents a topic in a set of connected paragraphs. For an opinion essay, state your view clearly and support it with reasons.

| Part | Job |
|---|---|
| **Title** | short and clear |
| **Introduction** | introduce the issue and give your opinion |
| **Body paragraphs** | (a) positive effects, (b) negative effects, each with examples |
| **Solutions** | what government and people can do |
| **Conclusion** | summarise and finish with a strong thought |

**Task.** Every year a large number of youths and professionals leave Nepal. Write an essay on the impacts of such migration. Include suggestions and solutions.

**Model essay — The Impacts of Youth Migration**

Every year thousands of young Nepalis leave their homes to study or work in the Gulf, Malaysia, Australia, Japan or Europe. Migration has become a part of Nepali life, and it has both good and bad effects on the country.

On the positive side, migrants send money home. This **remittance** supports their families, pays for children's education and has become an important part of the national economy. Migrants also learn new skills and ideas that they can bring back to Nepal, and they build links between Nepal and the countries where they live.

On the negative side, the departure of so many young people causes **brain drain**: doctors, engineers, teachers and technicians go abroad and the country is short of skilled people. Villages are left with old people and children, and farmland lies empty. Families suffer from long separation, and some workers face risky jobs, low pay or even accidents abroad. A country that depends too much on remittance also finds it harder to develop its own industries.

What can be done? The government should create more jobs at home, support small industries and agriculture, improve the quality of education and make sure that talented people are given fair opportunities. Foreign employment should be safe, with proper training, honest agents and legal protection. Returning migrants should be helped to use their savings and skills to start businesses in Nepal.

In conclusion, migration cannot be stopped, but it can be managed. If Nepal makes it possible for young people to find good work at home, they will migrate by choice and not by necessity.

## Chapter summary

- World population: just over 2.5 billion in 1950; fastest growth about 2.1% a year (1960s); now below 1%; about 8.5 billion by 2030, 9.7 billion by 2050, peak about 10.4 billion in the 2080s. Fertility and mortality decide change.
- Regions differ: sub-Saharan Africa grows fast (over 2 billion by 2040s); Europe and Northern America decline from the late 2030s; eight countries drive over half of the growth.
- Birds migrate for food, breeding and climate, using stopovers, night flight and flocks; partial migration; mountain birds move up and down.
- Although / though / even though + clause; despite / in spite of + noun or -ing; however + comma; never use *although … but*.
- Graph interpretation: introduction, highest and lowest, trend, comparison, conclusion.
- Essay: title, introduction with opinion, positive and negative effects, solutions, conclusion.

## Practice questions

**Reading comprehension**

> Every spring, millions of swallows fly from southern Africa to Europe, a journey of more than 10,000 kilometres. They fly by day, catching insects as they go, and use rivers and coastlines as guides. Some die of cold or hunger on the way, and strong winds can push them far off course. In autumn they return. Scientists fit tiny rings on their legs so that, when a bird is found again, they can discover where it has been.

1. From where to where do swallows migrate in spring? <span class="marks">[1]</span>
2. How do swallows feed during the journey? <span class="marks">[1]</span>
3. Write **True** or **False**: Swallows fly only at night. <span class="marks">[1]</span>
4. What guides the swallows on their way? <span class="marks">[2]</span>
5. Why do scientists put rings on the birds' legs? <span class="marks">[2]</span>
6. Describe in about 50 words the dangers of migration. <span class="marks">[4]</span>

::: note Answers
**1.** From southern Africa to Europe. **2.** By catching insects as they fly. **3.** False; they fly by day. **4.** Rivers and coastlines. **5.** So that when a bird is found again, scientists can learn where it has travelled. **6.** Migration is dangerous. The birds may die of cold or hunger because food is scarce on the way. Strong winds can blow them off course over the sea, where they cannot rest, and storms may exhaust them. Only the strongest return to their breeding grounds.
:::

**Grammar**

1. Join with *although*: "He is poor. He is honest." <span class="marks">[1]</span>
2. Fill in: "______ the heavy rain, the match went on." (despite/although) <span class="marks">[1]</span>
3. Correct: "Although it was cold, but he went out." <span class="marks">[1]</span>
4. Join with *however*: "She studied hard. She did not pass." <span class="marks">[1]</span>
5. Fill in: "In spite of ______ (be) ill, he attended class." <span class="marks">[1]</span>
6. Join with *while*: "Ram likes maths. Hari likes English." <span class="marks">[1]</span>
7. Rewrite with *despite*: "Although he was tired, he finished the work." <span class="marks">[1]</span>
8. Fill in: "It was hot, ______ we enjoyed the trek." (yet/because) <span class="marks">[1]</span>

::: note Answers
**1.** Although he is poor, he is honest. **2.** Despite **3.** Although it was cold, he went out. **4.** She studied hard; however, she did not pass. **5.** being **6.** Ram likes maths while Hari likes English. **7.** Despite being tired, he finished the work. **8.** yet
:::

**Writing**

1. The pie chart shows how a family of Rs 60,000 monthly income spends it: food 40%, education 20%, housing 20%, health 10%, savings 10%. Write an interpretation. <span class="marks">[5]</span>
2. Write an essay of about 200 words on "Rural-to-urban migration: causes and effects". <span class="marks">[5]</span>

::: note Outline for answers
**1.** Introduction (family budget); highest: food 40% = Rs 24,000; education and housing 20% each = Rs 12,000; health and savings 10% each = Rs 6,000; conclusion: nearly half goes to basic needs and only a tenth is saved.

**2.** Causes: jobs, schools, hospitals, roads, conflict and disaster. Effects: crowded cities, pollution, rising rent, empty villages and abandoned farms; also remittance and mixed cultures. Solutions: develop rural areas, local jobs, decentralised services.
:::

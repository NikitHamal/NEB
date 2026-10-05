---
subject: Compulsory English
grade: 8
unit: 7
title: Weather Forecast / Migration
hours: 0
area: Units
---

Two texts about things that are going to happen and things that have been
happening for a very long time. A **weather forecast** is the language of
prediction — what the sky will do tomorrow, and how sure the forecaster is
allowed to be. **Migration** is the movement of people or animals from one place
to another, and the chapter asks why it happens and what it does to the places
left behind. The grammar of the unit is the whole family of future forms.

::: key What this unit asks of you
By the end you should be able to (1) read a weather forecast and say what it
predicts and how confident it is, (2) give the causes and effects of migration,
(3) choose correctly between *will*, *going to* and the future perfect, and
(4) write an information paragraph on the environment using the future tense.
:::

## 7.1 Weather Forecast

### About the text

A weather forecast is **predictive writing**. Its job is not to record what
happened but to tell people what to expect, so that they can decide: take an
umbrella, cancel the match, harvest today rather than tomorrow.

The language of a forecast is carefully graded, and the grading is the most
interesting thing about it. A forecaster never says "it will rain in Pokhara at
4 p.m." with total confidence. The forecast says:

- *It **will** rain.* — the model is confident.
- *It **is likely to** rain.* — more than half the runs agree.
- *There **may be** showers.* — the chance is real but small.
- *Rain **is expected** in the hills.* — the writer avoids naming who expects it.
- *Outlook: **scattered** showers.* — scattered means some places and not
  others, which is not the same as saying the whole district gets rain.

That graded language is not vagueness. It is honesty: the atmosphere is a
chaotic system, and a forecast that pretends to certainty is a worse forecast
than one that gives its own confidence level.

A Nepali forecast also has its own vocabulary because of the terrain. The
**monsoon** (June to September) brings the rain that the fields need; the winter
months bring dry, clear weather; the pre-monsoon months bring dust, heat and
afternoon thunderstorms. The country is divided into regions — the Tarai, the
hill districts and the Himalayan region — and the forecast is usually given
region by region, because the weather of Jumla and the weather of Janakpur
have almost nothing to do with each other.

| Forecast phrase | What it means | What you should do |
|---|---|---|
| "heavy rainfall at one or two places" | intense rain, but local | check whether you are in those places |
| "partly cloudy" | half the sky covered | nothing changes |
| "thunderstorm likely in the afternoon" | convection after a hot morning | avoid open ground after 2 p.m. |
| "visibility poor in the morning" | fog or mist | travel after it lifts |
| "temperature falling by 4 °C" | a cold front or snowfall | keep warm clothes out |

```figure caption="Certainty in a forecast. A good forecast says not only what will happen but how sure the forecaster is — which is why 'may' and 'likely' are content words, not filler."
fig, ax = plt.subplots(figsize=(4.9, 2.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.0); ax.axis("off")
levels = [("will", 0.9, SERIES[0]), ("is likely to", 0.7, SERIES[1]),
          ("is expected to", 0.6, SERIES[2]), ("may / might", 0.4, SERIES[3]),
          ("could possibly", 0.25, SERIES[4])]
for i, (label, conf, colour) in enumerate(levels):
    y = 4.3 - i * 0.82
    ax.text(2.5, y, label, ha="right", va="center", fontsize=6.8, color=INK)
    ax.add_patch(plt.Rectangle((2.7, y - 0.22), conf * 6.4, 0.44, fc=colour, ec="none"))
ax.text(5.9, 0.35, "chance of the forecast coming true", ha="center",
        fontsize=6.3, color=MUTED)
fig.tight_layout()
```

### Vocabulary

| Word | Meaning |
|---|---|
| forecast | a statement about what is expected to happen |
| outlook | a short summary of what is expected |
| scattered | happening in some places, not everywhere |
| visibility | how far you can see clearly |
| monsoon | the seasonal wind that brings the summer rain |
| humidity | the amount of water vapour in the air |

::: note Model answers
**1. Why does a forecast use words like *may*, *likely* and *expected*?**
Because the atmosphere is a chaotic system and no forecast can be certain. The
words tell the reader how much confidence to place in the prediction, which is
more useful than false certainty.
**2. Why is a Nepali forecast given region by region?**
Because the country's altitude changes from about 60 metres in the Tarai to
8,848 metres at the summit of Everest within a short distance, so the Tarai,
the hills and the Himalaya have different climates at the same moment.
:::

## 7.2 Migration

### About the text

The text is **cause-and-effect** writing about movement — of people, and of
birds and animals. It defines migration, lists its causes, divides it into
kinds, and then describes the effects on both the place that is left and the
place that is reached.

### What the text says

**Migration** is the movement of people from one place to another, usually to
live, either inside one country (**internal migration**) or from one country to
another (**international migration**).

The **causes** fall into two groups. **Push factors** drive people away from a
place: poverty and unemployment, low wages, scarcity of fertile land, drought
and flood, landslides, conflict and insecurity, poor schools and hospitals.
**Pull factors** attract them to a new place: better-paid work, fertile land,
industry and cities, good schools and hospitals, safety and family already
settled there.

In Nepal the largest movement has been **internal**, from the hills to the
Tarai and from villages to Kathmandu, Pokhara and the fast-growing
municipalities along the highways. The second is **international**, to the Gulf
states, Malaysia and India, and the money sent home — **remittances** — is one
of the largest single sources of foreign currency in the country.

The **effects** are not all on one side. Where people arrive, labour becomes
cheap, building booms, and the city grows faster than its water pipes, roads and
schools can manage; rents rise, and land is built over. Where people leave,
fields may go out of cultivation, schools close for want of children, and the
grandparents who remain are left without help at home. But the same movement
brings money back: many families build a house, educate a child and open a shop
on remittance money.

Animal migration has the same shape and the same purpose: **birds** fly
thousands of kilometres on the same route every year to reach food and a
nesting place — the **diversity** of Nepal makes it a stop on the migratory
flyway — while fish swim upstream to spawn, and grazing animals move with the
rain.

| Question | People | Birds and animals |
|---|---|---|
| Why move? | work, land, safety, schooling | food, breeding, weather |
| How often? | once, or seasonally | seasonally, on the same route |
| Effect of leaving | labour shortage, empty fields | fewer birds in the wetland they left |
| Effect of arriving | cheap labour, crowded city | grazing pressure, new competition |

::: note Model answers
**1. Give three push factors and three pull factors of migration.**
Push: unemployment and low wages, drought and flood, and conflict or
insecurity. Pull: better-paid work, good schools and hospitals, and family
already settled there.
**2. Name one good effect and one bad effect of migration on a village.**
Good: remittances let families build houses and educate children. Bad: fields
go out of cultivation and schools close for want of children.
:::

## 7.3 Grammar and writing tasks of the unit

### Grammar: The future — will, going to, future perfect

| Form | Use | Example |
|---|---|---|
| will + verb | a prediction, or a decision made now | It **will** rain later. / I **will** help you. |
| going to + verb | a plan already made; something clearly about to happen | We **are going to** visit Pokhara in Chaitra. |
| present continuous | a fixed arrangement | We **are leaving** tomorrow at six. |
| present simple | a timetable | The bus **leaves** at seven. |
| future continuous | an action in progress at a future time | At 8 p.m. I **will be studying**. |
| future perfect | an action finished before a future time | By Sunday I **will have finished** the book. |

The difference between *will* and *going to* is intention. "I **will** carry
that bag" is decided at the moment of speaking. "I **am going to** carry that
bag" was decided before.

::: caution Common mistakes
- *I will going to school tomorrow.* ✗ → *I **will go** to school tomorrow.* ✓
- *She will has finished.* ✗ → *She **will have** finished.* ✓
- *Look at those clouds — it will rain.* (a prediction from evidence takes
  *going to*: *it **is going to** rain*) ✓
- *By next month he will complete it.* → *By next month he **will have
  completed** it.* ✓
:::

### Writing: Paraphrasing and environment paragraphs

To paraphrase, change the words **and** the sentence shape, and keep the
meaning. For an environment paragraph, use this skeleton: a general statement
(*Climate change is already changing the monsoon*), two pieces of evidence, one
consequence, and one thing that is being done about it. Use the future tense
wherever the paragraph is about what is still to come.

::: example Worked example
**Original.** *More than half of Nepal's households now receive money from a
family member working abroad.*
**Paraphrase.** *It is now unusual for a Nepali household to have no relative
working outside the country.*
:::

## Chapter summary

- A weather forecast is predictive writing; its *may*, *likely* and *expected*
  tell you how confident the forecaster is.
- Nepali forecasts are regional because the Tarai, the hills and the Himalaya
  have different climates at the same moment.
- Migration is the movement of people to live in another place; internal
  migration stays inside the country, international migration crosses a border.
- Push factors drive people out; pull factors attract them in.
- Remittances are a large part of Nepal's economy, but migration also empties
  fields and closes village schools.
- Birds migrate on the same routes each year, for food and for breeding.
- **will** = prediction or a decision made now; **going to** = a plan already
  made; present continuous = an arrangement; present simple = a timetable.
- **Future perfect** (*will have + past participle*) = finished before a stated
  future time.

## Practice questions

**Reading**

1. What is a forecast and why does it use graded language? <span class="marks">[2]</span>
2. Give three push factors and two pull factors of migration. <span class="marks">[3]</span>
3. Name two bad effects of migration on a village. <span class="marks">[2]</span>
4. Why do birds migrate? <span class="marks">[1]</span>

::: note Answers
**1.** A statement about what is expected to happen. It uses graded language
because a forecast cannot be certain, and the reader needs to know how much to
trust it.
**2.** Push: unemployment and low wages; drought and flood; conflict and
insecurity. Pull: better-paid work; good schools and hospitals.
**3.** Fields go out of cultivation; schools close for want of children (also:
grandparents left without help, local labour shortage).
**4.** To reach food and a suitable nesting place at the right season.
:::

**Grammar**

5. Choose *will* or *going to*. <span class="marks">[5]</span>
   (a) Look at the sky — it ______ rain.
   (b) I have bought the ticket. I ______ travel on Friday.
   (c) The phone is ringing. I ______ answer it.
   (d) She ______ study medicine; she has already applied.
   (e) Don't worry, I ______ help you with the bags.

6. Put the verbs in the future perfect. <span class="marks">[3]</span>
   (a) By next July I ______ (finish) school.
   (b) By the time you arrive, we ______ (eat).
   (c) By 2085 Nepal ______ (build) many new roads.

::: note Answers
**5.** (a) is going to (b) am going to (c) will (d) is going to (e) will
**6.** (a) will have finished (b) will have eaten (c) will have built
:::

**Writing**

7. Write a weather forecast of about 80 words for your district for tomorrow,
   using *will*, *likely* and *may*. <span class="marks">[4]</span>
8. Write a paragraph of about 100 words on the effects of migration on Nepali
   villages. Give one good effect and one bad one. <span class="marks">[5]</span>

::: note Answers
**7.** Name the region and the day, then give the outlook with graded language:
"Tomorrow will be partly cloudy in the morning, with rain likely in the
afternoon in one or two places. Winds may be strong on the ridges. Visibility
will be poor before 9 a.m." Add the temperature if you know it, and end with
what people should carry.
**8.** General statement: migration has changed village life more than any
other force in the last thirty years. Good effect: remittances build houses,
pay school fees and start small shops. Bad effect: fields go out of
cultivation, schools close for want of children, and the elderly are left
without help at home. Consequence: the village keeps its houses but loses its
workers.
:::

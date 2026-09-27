---
subject: Biology
grade: 12
unit: 9
title: Human Population and Health Disorders
hours: 6
area: Zoology
---

This unit turns the biology of a single human body outwards onto whole
populations. First it asks how many of us there are, how fast that number is
changing, and what shape the population has — because the age structure of Nepal
decides how many schools, jobs and hospital beds the country will need. Then it
asks what makes people ill: microbes that pass from person to person, disorders
that grow out of the way we live, and diseases caused simply by something missing
from the plate.

::: key What the examiner asks from this unit
Two things come almost every year. One is a **definition-plus-calculation**
question on population: crude birth rate, death rate, growth rate, doubling time
or dependency ratio, worked from given numbers. The other is a **disease
question** — the life cycle of the malarial parasite, the structure of HIV and
the course of AIDS, or a table comparing communicable and non-communicable
diseases. Learn the malaria cycle as a drawing, not as a paragraph.
:::

## 9.1 Human Population

**Demography** is the statistical study of human populations — their size,
composition, distribution and the rates at which they change. It rests on three
processes only: **births** add people, **deaths** remove them, and **migration**
moves them between places.

### 9.1.1 The basic measures

Every demographic rate is a count divided by the population at risk, multiplied
by a convenient factor (1000 or 100,000) so that the answer is a whole-ish number.

::: definition The five rates you must be able to state
- **Crude birth rate (CBR)** — live births per 1000 people per year.
- **Crude death rate (CDR)** — deaths per 1000 people per year.
- **Rate of natural increase (RNI)** — CBR minus CDR, per 1000 per year.
- **Total fertility rate (TFR)** — the average number of children a woman
  would bear in her lifetime at current age-specific fertility rates.
- **Infant mortality rate (IMR)** — deaths of children under one year per 1000
  **live births** (not per 1000 population).
:::

$$ \text{CBR} = \frac{B}{P}\times 1000, \qquad \text{CDR} = \frac{D}{P}\times 1000,
\qquad \text{RNI} = \text{CBR} - \text{CDR} $$

where $B$ is the number of live births in the year, $D$ the number of deaths and
$P$ the mid-year population. Two more measures matter in Nepal:

- **Maternal mortality ratio (MMR)** — maternal deaths per 100,000 live births.
- **Sex ratio** — in Nepal this is reported as males per 100 females.

::: caution "Crude" means crude
CBR and CDR ignore age structure. A country full of young adults can have a low
CDR while being *less* healthy than a country full of pensioners. That is why
Japan's CDR is higher than Nepal's even though Japanese people live much longer.
Compare **age-specific** rates or life expectancy instead.
:::

::: example Worked example 9.1 — birth, death and natural increase rates
**Problem.** A municipality had a mid-year population of 250,000. During that
year 4500 live births and 1300 deaths were registered, and 90 of the deaths were
of infants under one year old. Find (a) the CBR, (b) the CDR, (c) the rate of
natural increase as a percentage, (d) the IMR, and (e) the time the population
would take to double from natural increase alone.

**Solution.**

(a) $\text{CBR} = \dfrac{4500}{250000}\times 1000 = 18.0$ per 1000 per year.

(b) $\text{CDR} = \dfrac{1300}{250000}\times 1000 = 5.2$ per 1000 per year.

(c) $\text{RNI} = 18.0 - 5.2 = 12.8$ per 1000, and since "per 1000" divided by
10 gives "per cent",

$$ \text{RNI} = \frac{12.8}{10} = 1.28\ \% \text{ per year} $$

(d) The IMR uses **live births**, not population, as the denominator:

$$ \text{IMR} = \frac{90}{4500}\times 1000 = 20 \text{ per 1000 live births} $$

(e) By the rule of 70, $T_d \approx 70/1.28 = 54.7 \approx 55$ years.
:::

### 9.1.2 How populations grow

If a population grows by a fixed *number* each year the growth is **arithmetic**
and the graph is a straight line. Real populations grow by a fixed *proportion*
each year, so the increase itself gets bigger every year. This is **exponential**
(geometric) growth, and its graph is the familiar J-shaped curve:

$$ P_t = P_0\,e^{rt} \qquad \Longrightarrow \qquad r = \frac{1}{t}\ln\!\left(\frac{P_t}{P_0}\right) $$

Here $P_0$ is the population at the start, $P_t$ the population after time $t$
years, and $r$ the annual growth rate expressed as a decimal fraction.

::: derivation Doubling time and the rule of 70
The population has doubled when $P_t = 2P_0$. Substituting into
$P_t = P_0e^{rt}$ and cancelling $P_0$,

$$ 2 = e^{rT_d} \;\Longrightarrow\; \ln 2 = rT_d \;\Longrightarrow\;
T_d = \frac{\ln 2}{r} = \frac{0.693}{r} $$

If the rate is quoted as a percentage, $r = R/100$, so

$$ T_d = \frac{0.693\times 100}{R} = \frac{69.3}{R} \approx \frac{70}{R} $$

This is the **rule of 70**: divide 70 by the percentage growth rate to get the
doubling time in years.
:::

Nepal has been counted every ten years since 1911, so its growth curve is one of
the best-documented in South Asia.

```figure caption="Nepal's population at every census since 1911 (bars) and the annual intercensal growth rate (line). Growth peaked at 2.62 % in 1971–81 and fell to 0.92 % in 2011–21, the lowest positive rate ever recorded. Source: CBS/NSO census reports; the 1952/54 round is plotted at 1952."
import numpy as np, matplotlib.pyplot as plt
yr  = [1911,1920,1930,1941,1952,1961,1971,1981,1991,2001,2011,2021]
pop = [5.639,5.574,5.533,6.284,8.257,9.413,11.556,15.023,18.491,23.151,26.495,29.165]
gr  = [np.nan,-0.13,-0.07,1.16,2.28,1.64,2.05,2.62,2.08,2.25,1.35,0.92]
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.bar(yr, pop, width=6.2, color=ACCENT, alpha=.80, label='population')
ax.set_ylabel('population (million)'); ax.set_ylim(0,34)
ax.set_xlabel('census year')
ax.set_xticks([1911,1930,1952,1971,1991,2011,2021])
ax.set_xticklabels(['1911','1930','1952','1971','1991','2011','2021'], fontsize=7.6)
ax.spines[['top']].set_visible(False)
ax2 = ax.twinx()
ax2.plot(yr, gr, color='#d9534f', lw=1.8, marker='o', ms=4, label='growth rate')
ax2.set_ylabel('annual growth rate (%)', color='#d9534f')
ax2.tick_params(axis='y', colors='#d9534f'); ax2.set_ylim(-0.5,3.2)
ax2.axhline(0, color=MUTED, lw=.7, ls=':')
ax2.spines[['top']].set_visible(False)
ax2.annotate('peak growth 2.62 %\n(1971–81)', xy=(1981,2.62), xytext=(1924,2.92),
             fontsize=7.2, color='#d9534f', ha='left', va='center',
             arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0,
                             mutation_scale=9))
ax.grid(True, axis='y', alpha=.45)
```

::: example Worked example 9.2 — Nepal's growth rate and doubling time
**Problem.** The 2011 census (reference date 22 June 2011) counted 26,494,504
people and the 2021 census (reference date 25 November 2021) counted 29,164,578.
The interval between the two reference dates is 10.43 years. Calculate (a) the
annual exponential growth rate and (b) the doubling time at that rate.

**Solution.**

(a) $\dfrac{P_t}{P_0} = \dfrac{29\,164\,578}{26\,494\,504} = 1.1008$, so

$$ r = \frac{1}{t}\ln\!\left(\frac{P_t}{P_0}\right) = \frac{\ln 1.1008}{10.43}
= \frac{0.0960}{10.43} = 0.00921 $$

That is $r = 0.92\ \%$ per year — exactly the figure the National Statistics
Office published for the 2021 census.

(b) $T_d = \dfrac{0.693}{0.00921} = 75.2$ years. (The rule of 70 gives
$70/0.92 = 76$ years, close enough for a quick check.)

Notice what would happen if you carelessly used $t = 10$ years instead of 10.43:
you would get 0.96 %, and your answer would not match the official figure. The
census was delayed five months by COVID-19, and the extra months matter.
:::

### 9.1.3 Age–sex structure and the population pyramid

A **population pyramid** (age–sex pyramid) is a pair of back-to-back horizontal
bar graphs: age groups stacked from youngest at the bottom to oldest at the top,
males to the left of the axis and females to the right. Its shape is a fingerprint
of a country's birth rate, death rate and migration history.

```figure caption="The three classical population pyramid shapes. Males are plotted to the left of the axis, females to the right."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.1,2.9), sharey=True)
bands = ['0–9','10–19','20–29','30–39','40–49','50–59','60–69','70+']
y = np.arange(len(bands))
shapes = {
 'Expanding\n(broad base)':      [26,22,18,14,10,6,3,1],
 'Stable / stationary\n(bell)':  [15,15,15,15,14,12,8,4],
 'Declining\n(narrow base)':     [9,11,13,15,16,15,12,8],
}
for ax, (title, v) in zip(axes, shapes.items()):
    v = np.array(v, dtype=float)
    ax.barh(y, -v, height=.82, color=ACCENT, alpha=.85)
    ax.barh(y,  v, height=.82, color='#d9534f', alpha=.85)
    ax.axvline(0, color=INK, lw=.8)
    ax.set_title(title, fontsize=7.8, pad=16)
    ax.set_xlim(-30,30); ax.set_xticks([]); ax.set_ylim(-0.7, 8.9)
    ax.tick_params(left=False)
    ax.spines[['top','right','bottom','left']].set_visible(False)
axes[0].set_yticks(y); axes[0].set_yticklabels(bands, fontsize=7.2)
axes[0].set_ylabel('age group (years)', fontsize=8)
for ax in axes:
    ax.text(-15, 7.9, 'male', ha='center', fontsize=6.8, color=ACCENT)
    ax.text( 15, 7.9, 'female', ha='center', fontsize=6.8, color='#d9534f')
fig.tight_layout()
```

| Pyramid shape | Birth rate | Death rate | Growth | Example |
|---|---|---|---|---|
| Expanding — broad base, narrow top | high | high | rapid | Niger, Afghanistan |
| Stable — nearly vertical sides | moderate | low | slow | Nepal today, India |
| Declining — narrow base, wide middle | low | low | negative | Japan, Italy |

Nepal's own age structure has changed visibly in one decade. The base of the
pyramid is now **narrower than the band above it** — the 0–9 group (5.21 million)
is smaller than the 10–19 group (5.88 million). That is the arithmetic signature
of falling fertility.

```figure caption="Left: Nepal's population by ten-year age band, Census 2021 — the 0–9 band is already smaller than 10–19. Right: the share of children, working-age adults and elderly in 2011 and 2021. Source: National Population and Housing Census 2011 and 2021 (CBS/NSO)."
import numpy as np, matplotlib.pyplot as plt
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(5.2,3.0),
                              gridspec_kw={'width_ratios':[1.55,1]})
bands = ['0–9','10–19','20–29','30–39','40–49','50–59','60–69','70–79','80+']
val = np.array([5205710,5876269,5242409,4189204,3183872,2489796,
                1727222,962573,287523])/1e6
y = np.arange(len(bands))
ax.barh(y, val, height=.74, color=ACCENT, alpha=.88)
for i, v in enumerate(val):
    ax.text(v+0.12, i, f'{v:.2f}', va='center', fontsize=6.8, color=MUTED)
ax.set_yticks(y); ax.set_yticklabels(bands, fontsize=7.4)
ax.set_xlabel('population (million)', fontsize=8); ax.set_xlim(0,7.4)
ax.set_title('Census 2021 age structure', fontsize=8.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='x', alpha=.4)
# right panel: broad bands 2011 vs 2021
labels = ['0–14', '15–64', '65+']
d2011 = [34.91, 59.82, 5.27]
d2021 = [27.83, 65.24, 6.93]
x = np.arange(3); w = 0.36
ax2.bar(x-w/2, d2011, w, color=MUTED, alpha=.85, label='2011')
ax2.bar(x+w/2, d2021, w, color='#2e8b57', alpha=.9, label='2021')
for xi, a, b in zip(x, d2011, d2021):
    ax2.text(xi-w/2, a+1.2, f'{a:.1f}', ha='center', fontsize=6.6, color=MUTED)
    ax2.text(xi+w/2, b+1.2, f'{b:.1f}', ha='center', fontsize=6.6, color='#2e8b57')
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=7.6)
ax2.set_ylabel('% of population', fontsize=8); ax2.set_ylim(0,78)
ax2.set_title('broad age bands', fontsize=8.4)
ax2.legend(fontsize=7.2, loc='upper left')
ax2.spines[['top','right']].set_visible(False)
ax2.grid(True, axis='y', alpha=.4)
fig.tight_layout()
```

The **dependency ratio** turns the age structure into a single number: how many
people who are not of working age each 100 workers must support.

$$ \text{Dependency ratio} = \frac{P_{0-14} + P_{65+}}{P_{15-64}}\times 100 $$

::: example Worked example 9.3 — Nepal's dependency ratio from census figures
**Problem.** The 2021 census counted 8,115,575 people aged 0–14, 19,027,289 aged
15–64 and 2,021,714 aged 65 and over. Calculate the child, old-age and total
dependency ratios, and comment.

**Solution.** Number of dependants $= 8\,115\,575 + 2\,021\,714 = 10\,137\,289$.

$$ \text{Child dependency} = \frac{8\,115\,575}{19\,027\,289}\times 100 = 42.7 $$
$$ \text{Old-age dependency} = \frac{2\,021\,714}{19\,027\,289}\times 100 = 10.6 $$
$$ \text{Total dependency} = \frac{10\,137\,289}{19\,027\,289}\times 100 = 53.3 $$

So every 100 Nepalis of working age support about 53 dependants, of whom 43 are
children and 11 are elderly. Since dependency is low and falling, Nepal is inside
its **demographic dividend** — a few decades in which the working-age share is
unusually large. The dividend only pays if those workers find jobs.
:::

### 9.1.4 The demographic transition

The **demographic transition model (DTM)** describes the path every industrialising
society has followed from high birth and death rates to low ones. It has four
recognised stages (a fifth, of population decline, is sometimes added).

```figure caption="The demographic transition model. Natural increase (shaded) is the gap between the birth-rate and death-rate curves; it is widest in Stage 2. Nepal's rates in the early 2020s place it in late Stage 3."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.1))
t = np.linspace(0, 100, 500)
def logi(t, mid, k, hi, lo):
    return lo + (hi-lo)/(1+np.exp((t-mid)/k))
cdr = logi(t, 30, 5.0, 42, 9) + 0.9*np.sin(t/2.2)*np.exp(-t/9)
cbr = logi(t, 58, 8.0, 44, 11) + 0.8*np.sin(t/2.0)*np.exp(-t/9)
ax.fill_between(t, cdr, cbr, where=cbr>cdr, color='#2e8b57', alpha=.16,
                label='natural increase')
ax.plot(t, cbr, color=ACCENT, lw=2.0, label='birth rate')
ax.plot(t, cdr, color='#d9534f', lw=2.0, label='death rate')
for x in (22, 46, 74):
    ax.axvline(x, color=MUTED, lw=.7, ls='--')
for x, lab in [(11,'Stage 1\nhigh\nstationary'), (34,'Stage 2\nearly\nexpanding'),
               (60,'Stage 3\nlate\nexpanding'), (87,'Stage 4\nlow\nstationary')]:
    ax.text(x, 50, lab, ha='center', va='top', fontsize=7.0, color=INK)
ax.annotate('Nepal, early 2020s:\nCBR ≈ 19, CDR ≈ 6', xy=(70, 19.6),
            xytext=(52, 33), fontsize=7.2, color='#8F5507', ha='left',
            arrowprops=dict(arrowstyle='-|>', color='#8F5507', lw=1.0,
                            mutation_scale=9))
ax.plot([70],[19.6],'o', color='#8F5507', ms=5, zorder=6)
ax.set_xlabel('time  →'); ax.set_ylabel('rate per 1000 per year')
ax.set_xlim(0,100); ax.set_ylim(0,56); ax.set_xticks([])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.4)
ax.legend(loc='lower left', fontsize=7.4)
```

| Stage | Birth rate | Death rate | Natural increase | Why |
|---|---|---|---|---|
| 1 High stationary | high (~40) | high (~40) | near zero | famine, epidemics, no medicine |
| 2 Early expanding | high | falls steeply | very rapid | clean water, vaccines, better food |
| 3 Late expanding | falls | low | slows down | contraception, girls' education, urban life |
| 4 Low stationary | low (~12) | low (~10) | near zero | small planned families |

Nepal moved through Stage 2 between about 1950 and 1990 — malaria control in the
Terai, smallpox eradication and expanded immunisation cut deaths while births
stayed high, which is why growth peaked at 2.62 % in the 1970s. Since 1990 the
birth rate has fallen sharply: the total fertility rate was 4.6 children per
woman in 1996 and **2.1 in 2022** (Nepal Demographic and Health Survey 2022) —
essentially replacement level.

### 9.1.5 Nepal's population situation

| Indicator | Value | Year and source |
|---|---|---|
| Total population | 29,164,578 | Census 2021 (NSO) |
| Male : female | 14,253,551 : 14,911,027 | Census 2021 |
| Sex ratio | 95.59 males per 100 females | Census 2021 |
| Annual growth rate | 0.92 % | Census 2011–2021 |
| Population density | 198 per km² | Census 2021 |
| Households / mean size | 6,666,937 / 4.37 persons | Census 2021 |
| Urban (municipality) share | 66.17 % | Census 2021 |
| Absent population abroad | 2,190,592 (82.2 % male) | Census 2021 |
| Literacy (age 5+) | 76.2 % (M 83.6, F 69.4) | Census 2021 |
| Life expectancy at birth | 71.3 yr (M 68.2, F 73.8) | Census 2021 (NSO) |
| Total fertility rate | 2.1 children per woman | NDHS 2022 |
| Infant mortality rate | 28 per 1000 live births | NDHS 2022 |
| Neonatal mortality rate | 21 per 1000 live births | NDHS 2022 |
| Under-five mortality rate | 33 per 1000 live births | NDHS 2022 |
| Maternal mortality ratio | 151 per 100,000 live births | NMMS 2021 |
| Projected population | 30,034,040 (1 July 2026) | NSO projection |

Four features of this table deserve comment.

1. **There are more women than men.** Nepal is one of few countries with a sex
   ratio below 100, and the reason is on the next line of the table: over 2.1
   million Nepalis, four-fifths of them men, were abroad on census day.
2. **Growth has almost stopped.** Falling fertility plus emigration gave the
   slowest growth in 110 years of census-taking.
3. **Nepal has become an urban country on paper.** The 66 % urban share follows
   the 2015–17 redrawing of local units, which converted many rural areas into
   municipalities; much of that "urban" land is still farmland.
4. **Mortality has fallen fast.** Maternal deaths fell from 539 per 100,000 live
   births in 1996 to 151 in 2021 — one of the fastest declines recorded anywhere.

::: note Consequences and control
Rapid growth strains land, forest, water, housing and schools, drives
encroachment on the Chure hills, and makes unemployment and out-migration worse.
Nepal's response has combined **family planning services**, **female education**,
**raising the legal age of marriage to 20**, **immunisation and safe-motherhood
programmes** that make parents confident their children will survive, and
**social security for the elderly**. Education is the single most effective
measure: fertility falls fastest where girls stay longest in school.
:::

## 9.2 Health disorders

::: definition Health (WHO, 1948)
Health is a state of complete physical, mental and social well-being, and not
merely the absence of disease or infirmity.
:::

A **disease** is any disturbance of the normal structure or working of the body
that produces recognisable signs and symptoms. Diseases are grouped as follows.

- **Communicable (infectious)** — caused by a pathogen and transmissible from
  one host to another: bacterial, viral, protozoan, helminthic, fungal.
- **Non-communicable (NCD)** — not transmissible: degenerative, metabolic,
  neoplastic (cancer), allergic and genetic disorders.
- **Deficiency diseases** — caused by lack of a nutrient.

### 9.2.1 Communicable diseases

| Disease | Pathogen | Transmission | Main symptoms | Prevention |
|---|---|---|---|---|
| Tuberculosis | *Mycobacterium tuberculosis* (bacterium) | airborne droplets | chronic cough >2 weeks, blood in sputum, evening fever, weight loss | BCG vaccine, DOTS treatment, ventilation |
| Typhoid | *Salmonella typhi* (bacterium) | faecal contamination of food and water | step-ladder fever, rose spots, abdominal pain | safe water, TCV vaccine, hygiene |
| Cholera | *Vibrio cholerae* (bacterium) | contaminated water | painless rice-water stools, rapid dehydration | chlorination, ORS, oral vaccine |
| Tetanus | *Clostridium tetani* (bacterium) | spores entering deep wounds | lock-jaw, muscle spasm, opisthotonus | TT/DPT vaccine, wound cleaning |
| Pneumonia | *Streptococcus pneumoniae* and others | droplets | fast breathing, chest indrawing, fever | PCV vaccine, avoid indoor smoke |
| Influenza | Influenza A/B virus | droplets | fever, body ache, sore throat | annual vaccine, cough etiquette |
| Hepatitis B | Hepatitis B virus | blood, sexual contact, mother to child | jaundice, dark urine, liver damage | HBV vaccine, screened blood |
| Rabies | Rabies virus (*Lyssavirus*) | bite or lick of an infected dog, bat, jackal | hydrophobia, excitement, paralysis, death | dog vaccination, post-exposure vaccine |
| Dengue | Dengue virus (4 serotypes) | bite of *Aedes aegypti* / *Ae. albopictus* | high fever, retro-orbital pain, rash, joint pain | destroy clean-water breeding sites |
| AIDS | Human immunodeficiency virus | unsafe sex, infected blood/needles, mother to child | opportunistic infections, wasting | safe sex, screened blood, ART |
| Malaria | *Plasmodium* spp. (protozoan) | bite of female *Anopheles* | cold–hot–sweating fever paroxysms, anaemia, enlarged spleen | bed nets, spraying, prompt treatment |
| Amoebic dysentery | *Entamoeba histolytica* (protozoan) | cysts in food and water | stool with blood and mucus, cramps | safe water, hand washing |
| Kala-azar | *Leishmania donovani* (protozoan) | bite of *Phlebotomus argentipes* sandfly | long fever, darkened skin, huge spleen | indoor spraying, plastered walls |
| Ascariasis | *Ascaris lumbricoides* (roundworm) | eggs in soil-contaminated food | abdominal pain, malnutrition, worms in stool | latrine use, deworming, washing vegetables |
| Taeniasis | *Taenia solium* (tapeworm) | undercooked pork with cysticerci | abdominal discomfort, segments in stool | meat inspection, thorough cooking |
| Ringworm | *Trichophyton*, *Microsporum* (fungi) | contact, shared towels and combs | itchy ring-shaped scaly patches | keep skin dry, do not share clothing |

::: tip How the marker reads a disease answer
Four marks usually means four facts: **pathogen, mode of transmission, two or
three symptoms, and one control measure.** Write the pathogen's scientific name
in *italics* with a capital for the genus and lower case for the species —
*Plasmodium vivax*, not plasmodium Vivax. Markers do deduct for this.
:::

### 9.2.2 Malaria — the parasite and its two hosts

Malaria is caused by four species of *Plasmodium*: *P. vivax* (benign tertian
malaria, fever every 48 h), *P. falciparum* (malignant tertian, 48 h, the species
that kills), *P. malariae* (quartan, 72 h) and *P. ovale*. In Nepal *P. vivax*
is by far the commonest. The vector is the **female *Anopheles* mosquito**; the
recognised vectors in Nepal are *Anopheles fluviatilis*, *An. annularis*,
*An. maculatus* and *An. minimus*.

::: key Which host is which
Humans are the **intermediate host**, because only the **asexual** phase
(schizogony) occurs in us. The mosquito is the **definitive host**, because
**fertilisation and the sexual phase** (gamogony and sporogony) occur in it.
Students reverse this constantly — the definitive host is defined by sex, not by
size or by who suffers.
:::

```figure caption="Life cycle of *Plasmodium*. Asexual multiplication (schizogony) takes place in the human liver and red blood cells; fertilisation and sporogony take place in the female *Anopheles*, which is therefore the definitive host."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.15,4.55))
ax.axis('off'); ax.set_xlim(-0.1,10.1); ax.set_ylim(0.6,10.4)
ax.add_patch(FancyBboxPatch((0.15,6.55), 9.7, 3.35, boxstyle='round,pad=0.05',
             fc='#eaf1f8', ec=ACCENT, lw=1.0, alpha=.55, zorder=0))
ax.add_patch(FancyBboxPatch((0.15,1.35), 9.7, 3.10, boxstyle='round,pad=0.05',
             fc='#fdeeed', ec='#d9534f', lw=1.0, alpha=.55, zorder=0))
ax.text(5.0, 9.66, 'HUMAN — intermediate host   (asexual: schizogony)',
        fontsize=7.8, color=ACCENT, weight='bold', ha='center')
ax.text(5.0, 1.60, 'FEMALE ANOPHELES — definitive host   (sexual: gamogony + sporogony)',
        fontsize=7.6, color='#d9534f', weight='bold', ha='center')

def stage(x, y, sub, label, c, dy=0.42):
    ax.add_patch(Circle((x,y), 0.27, fc='white', ec=c, lw=1.3, zorder=4))
    ax.text(x, y, sub, ha='center', va='center', fontsize=6.2, color=c, zorder=5)
    ax.text(x, y-dy, label, ha='center', va='top', fontsize=6.2, color=INK,
            zorder=5, linespacing=1.25)

def arrow(p, q, rad=0.0, c=MUTED, lw=1.2):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f'arc3,rad={rad}',
                 arrowstyle='-|>', mutation_scale=11, lw=lw, color=c, zorder=3))

hx = [1.25, 3.05, 4.95, 6.85, 8.75]
stage(hx[0], 8.35, 'sp', 'sporozoites\ninjected\nin saliva', ACCENT)
stage(hx[1], 8.35, 'lv', 'liver cells:\npre-erythrocytic\nschizogony', ACCENT)
stage(hx[2], 8.35, 'tr', 'RBC: ring\ntrophozoite', ACCENT)
stage(hx[3], 8.35, 'mz', 'schizont bursts:\nmerozoites\n(fever)', ACCENT)
stage(hx[4], 8.35, 'gc', 'gametocytes\n♂ micro,\n♀ macro', ACCENT)
for a, b in zip(hx[:-1], hx[1:]):
    arrow((a+0.31, 8.35), (b-0.31, 8.35))
arrow((6.85, 8.66), (4.95, 8.66), rad=0.45, c='#8F5507')
ax.text(5.90, 9.24, 're-invade fresh RBCs', fontsize=6.3, color='#8F5507', ha='center')

mx = [1.25, 3.60, 6.20, 8.75]
stage(mx[3], 3.30, 'gm', 'micro- and\nmacrogametes', '#d9534f')
stage(mx[2], 3.30, 'ok', 'zygote →\nmotile ookinete', '#d9534f')
stage(mx[1], 3.30, 'oc', 'oocyst on\nstomach wall', '#d9534f')
stage(mx[0], 3.30, 'sp', 'sporozoites in\nsalivary glands', '#d9534f')
for a, b in zip(mx[1:][::-1], mx[:-1][::-1]):
    arrow((a-0.31, 3.30), (b+0.31, 3.30))
ax.text(7.48, 3.58, 'fertilisation', fontsize=6.4, color='#d9534f', ha='center')
ax.text(4.90, 3.58, 'sporogony', fontsize=6.4, color='#d9534f', ha='center')
ax.text(2.42, 3.58, 'migration', fontsize=6.4, color='#d9534f', ha='center')

arrow((9.35, 6.45), (9.35, 4.55), c='#2e8b57', lw=1.7)
ax.text(9.62, 5.50, 'mosquito sucks blood', fontsize=6.6, color='#2e8b57',
        rotation=90, ha='center', va='center')
arrow((0.62, 4.55), (0.62, 6.45), c='#2e8b57', lw=1.7)
ax.text(0.34, 5.50, 'infective bite', fontsize=6.6, color='#2e8b57',
        rotation=90, ha='center', va='center')
```

The fever comes from the bursting of red cells. In *P. vivax* the erythrocytic
cycle takes 48 hours, so paroxysms recur every third day (counting inclusively) —
hence "tertian". Each paroxysm has three phases: a **cold stage** with shivering,
a **hot stage** with high fever, and a **sweating stage** as the temperature falls.

::: note Malaria in Nepal
Malaria has been pushed to the edge of elimination. The Epidemiology and Disease
Control Division recorded **37 indigenous cases and 1006 imported cases in 2024**,
and WHO's *World Malaria Report 2025* records 2 deaths for that year. Almost all
remaining transmission is in the Terai; most imported cases are in migrant
workers returning from India and Africa. Nepal's elimination target has been
moved from 2026 to **2030**.
:::

### 9.2.3 AIDS and HIV

**AIDS** — acquired immunodeficiency syndrome — is the late stage of infection
with **HIV**, a retrovirus of the family *Retroviridae*. HIV is a spherical
enveloped virus about 100–120 nm across, with two identical strands of
single-stranded RNA and three enzymes of its own.

```figure caption="Structure of the HIV virion. The gp120–gp41 spike binds CD4; reverse transcriptase copies the viral RNA into DNA, which integrase then inserts into the host chromosome."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0,3.8))
ax.axis('off'); ax.set_aspect('equal')
ax.set_xlim(-3.3,4.0); ax.set_ylim(-2.5,2.7)
ax.add_patch(Circle((0,0), 1.62, fc='#eaf1f8', ec=ACCENT, lw=1.6, zorder=2))
ax.add_patch(Circle((0,0), 1.48, fc='#eaf1f8', ec=ACCENT, lw=1.0, zorder=2))
ax.add_patch(Circle((0,0), 1.30, fc='#f5f2fb', ec='#6a5acd', lw=1.2, zorder=3))
# spikes
for a in np.linspace(0, 2*np.pi, 13)[:-1]:
    x0, y0 = 1.55*np.cos(a), 1.55*np.sin(a)
    x1, y1 = 1.95*np.cos(a), 1.95*np.sin(a)
    ax.plot([x0,x1],[y0,y1], color='#2e8b57', lw=1.3, zorder=4)
    ax.add_patch(Circle((x1,y1), 0.13, fc='#2e8b57', ec='none', zorder=5))
# conical capsid
ax.add_patch(Polygon([(-0.62,-0.95),(0.62,-0.95),(0.30,0.92),(-0.30,0.92)],
             closed=True, fc='#fdeeed', ec='#d9534f', lw=1.4, zorder=5))
# RNA strands
t = np.linspace(-0.80, 0.78, 120)
for dx in (-0.14, 0.14):
    ax.plot(dx + 0.10*np.sin(t*11), t, color='#8F5507', lw=1.3, zorder=6)
ax.add_patch(Circle((-0.34,0.40), 0.10, fc=INK, ec='none', zorder=6))
ax.add_patch(Circle(( 0.36,-0.12), 0.10, fc=INK, ec='none', zorder=6))
ax.add_patch(Circle((-0.30,-0.55), 0.10, fc=INK, ec='none', zorder=6))

def lab(txt, xy, xytext, c=INK):
    ax.annotate(txt, xy=xy, xytext=xytext, fontsize=7.2, color=c,
                ha='left' if xytext[0] > xy[0] else 'right',
                va='center',
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.9,
                                shrinkA=0, shrinkB=2))
lab('gp120 knob (binds CD4)', (0.98,1.69), (1.70,2.42), '#2e8b57')
lab('gp41 stalk', (1.51,0.87), (2.55,1.55), '#2e8b57')
lab('lipid envelope', (1.35,-0.79), (2.45,-0.28), ACCENT)
lab('p17 matrix', (1.07,-0.74), (2.45,-1.02), '#6a5acd')
lab('p24 conical capsid', (0.62,-0.95), (2.45,-1.78), '#d9534f')
lab('two (+) ssRNA strands', (-0.16,0.66), (-1.95,2.05), '#8F5507')
lab('reverse transcriptase,\nintegrase, protease', (-0.34,-0.55), (-2.05,-1.62), INK)
```

The target of HIV is the **helper T lymphocyte (CD4⁺ T cell)**, the cell that
coordinates the whole immune response. Reverse transcriptase copies viral RNA into
DNA, integrase splices that DNA into the host chromosome as a **provirus**, and
the infected cell then manufactures new virions until it is destroyed.

```figure caption="Course of untreated HIV infection. The acute phase is a burst of viraemia; through the long asymptomatic phase the CD4⁺ count falls steadily, and AIDS is defined by a CD4⁺ count below 200 cells mm⁻³."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.1))
t = np.linspace(0, 11, 800)
cd4 = np.where(t < 0.30, 1000 - 1000*t,
      np.where(t < 0.90, 700 + 133*(t-0.30),
               780*np.exp(-0.20*(t-0.90))))
vl  = np.where(t < 0.25, 3.0 + 16.0*t,
      np.where(t < 1.00, 7.0 - 3.33*(t-0.25),
               4.5 + 0.10*np.maximum(t-1.0, 0)**1.4))
ax.plot(t, cd4, color=ACCENT, lw=2.0, label='CD4$^+$ T cells')
ax.set_ylabel('CD4$^+$ count (cells mm$^{-3}$)', color=ACCENT)
ax.tick_params(axis='y', colors=ACCENT)
ax.set_ylim(0, 1200); ax.set_xlim(0, 11)
ax.axhline(200, color=MUTED, lw=.9, ls='--')
ax.text(1.35, 232, 'AIDS threshold: CD4 < 200 cells mm⁻³', fontsize=6.8, color=MUTED)
ax2 = ax.twinx()
ax2.plot(t, vl, color='#d9534f', lw=2.0, label='plasma viral load')
ax2.set_ylabel('log$_{10}$ viral RNA (copies mL$^{-1}$)', color='#d9534f')
ax2.tick_params(axis='y', colors='#d9534f'); ax2.set_ylim(2.2, 9.6)
ax.axvspan(0, 1.0, color='#d9534f', alpha=.07)
ax.axvspan(7.7, 11, color='#8F5507', alpha=.09)
ax.text(0.52, 1040, 'acute', fontsize=7.0, color='#d9534f', ha='center')
ax.text(4.3, 1040, 'asymptomatic (clinical latency)', fontsize=7.0,
        color=MUTED, ha='center')
ax.text(9.35, 1040, 'AIDS', fontsize=7.0, color='#8F5507', ha='center')
ax.set_xlabel('years after infection')
ax.set_xticks([0,1,2,4,6,8,10])
ax.spines[['top']].set_visible(False); ax2.spines[['top']].set_visible(False)
ax.grid(True, axis='y', alpha=.35)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, loc='lower left', fontsize=7.4)
```

HIV spreads by **unprotected sexual contact**, **transfusion of infected blood or
sharing of needles**, and **from mother to child** across the placenta, during
birth or in breast milk. It does **not** spread by touching, sharing food,
mosquito bites, coughing or using the same toilet. There is no cure, but
**antiretroviral therapy (ART)** holds the virus down for decades.

::: note HIV in Nepal
The National Centre for AIDS and STD Control estimated **34,337 people living
with HIV in Nepal in 2024**, with **614 new infections** and **559 AIDS-related
deaths** in that year, and about **77 % of those diagnosed on ART**. New
infections have fallen by roughly three-quarters since 2010 (2557 new infections
that year). About two-thirds of transmission is heterosexual, and the largest
risk group is male labour migrants and their partners.
:::

### 9.2.4 Immunity and the immune response

**Immunity** is the ability of the body to resist a pathogen.

| Basis | Type | Example |
|---|---|---|
| Present from birth, non-specific | **innate (natural) immunity** | skin, mucus, lysozyme in tears, stomach acid, phagocytes, inflammation |
| Developed after exposure, specific | **acquired (adaptive) immunity** | antibodies after chickenpox |
| Body makes its own antibodies | **active** — natural (after infection) or artificial (vaccine) | BCG, DPT, measles–rubella |
| Ready-made antibodies given | **passive** — natural (placenta, colostrum) or artificial (antiserum) | anti-tetanus serum, anti-rabies serum |

An **antigen** is any foreign molecule that provokes a response; an **antibody**
(immunoglobulin) is a Y-shaped protein made by plasma cells that binds one
antigen specifically. The five classes are **IgG** (most abundant, the only one
crossing the placenta), **IgM** (first made, largest), **IgA** (in mucus, saliva
and colostrum), **IgE** (allergy) and **IgD** (receptor on B cells).

```figure caption="The acquired immune response. An antigen-presenting macrophage activates a helper T cell, which drives the humoral limb (B cells → plasma cells → antibodies) and the cell-mediated limb (cytotoxic T cells). Memory cells make the second response faster and larger."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.15,3.6))
ax.axis('off'); ax.set_xlim(0,10.4); ax.set_ylim(0.1,7.5)
def cell(x, y, w, h, label, c, fc, fs=6.4):
    ax.add_patch(Ellipse((x,y), w, h, fc=fc, ec=c, lw=1.3, zorder=3))
    ax.text(x, y, label, ha='center', va='center', fontsize=fs,
            color=c, zorder=4, linespacing=1.2)
def arr(p, q, c=MUTED, rad=0.0, lw=1.2):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f'arc3,rad={rad}',
                 arrowstyle='-|>', mutation_scale=10, lw=lw, color=c, zorder=2))
ax.add_patch(FancyBboxPatch((0.12,3.30), 1.05, 0.80,
             boxstyle='round,pad=0.05', fc='#fdeeed', ec='#d9534f', lw=1.1))
ax.text(0.645, 3.70, 'antigen\n(pathogen)', ha='center', va='center',
        fontsize=6.4, color='#d9534f')
cell(2.55, 3.70, 1.80, 1.15, 'macrophage\n(APC)', INK, '#eef0f3')
cell(4.85, 3.70, 1.75, 1.15, 'helper T cell\n(CD4)', '#8F5507', '#fbf4e8')
cell(6.95, 5.85, 1.45, 0.95, 'B cell', ACCENT, '#eaf1f8')
cell(9.20, 5.85, 1.65, 1.05, 'plasma cell', ACCENT, '#eaf1f8')
cell(6.95, 1.55, 1.70, 1.05, 'cytotoxic T\ncell (CD8)', '#2e8b57', '#eaf6ee')
cell(9.20, 1.55, 1.65, 1.05, 'infected cell\nlysed', '#2e8b57', '#eaf6ee')
arr((1.24,3.70),(1.60,3.70), '#d9534f')
arr((3.50,3.70),(3.93,3.70))
ax.text(3.28, 4.52, 'antigen\npresentation', ha='center', va='bottom',
        fontsize=6.0, color=MUTED)
arr((5.55,4.18),(6.30,5.42), ACCENT, rad=0.10)
arr((5.55,3.22),(6.25,2.02), '#2e8b57', rad=-0.10)
arr((7.70,5.85),(8.35,5.85), ACCENT)
arr((7.82,1.55),(8.35,1.55), '#2e8b57')
ax.text(8.02, 6.46, 'antibodies', ha='center', va='bottom', fontsize=6.2, color=ACCENT)
ax.text(8.12, 2.13, 'perforin', ha='center', va='bottom', fontsize=6.2, color='#2e8b57')
ax.text(9.20, 6.92, 'HUMORAL immunity', ha='center', fontsize=7.2,
        color=ACCENT, weight='bold')
ax.text(9.20, 0.50, 'CELL-MEDIATED immunity', ha='center', fontsize=7.2,
        color='#2e8b57', weight='bold')
cell(6.95, 4.32, 1.40, 0.66, 'memory B', ACCENT, 'white', fs=6.0)
cell(6.95, 3.10, 1.40, 0.66, 'memory T', '#2e8b57', 'white', fs=6.0)
arr((6.95,5.36),(6.95,4.68), ACCENT, lw=0.9)
arr((6.95,2.04),(6.95,2.74), '#2e8b57', lw=0.9)
ax.text(7.80, 3.71, 'memory cells →\nfaster, stronger\nsecond response',
        fontsize=6.0, color=MUTED, ha='left', va='center')
ax.annotate('HIV destroys\nthis cell', xy=(4.85,3.10), xytext=(4.30,1.35),
            fontsize=6.4, color='#d9534f', ha='center',
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0,
                            mutation_scale=9))
```

Because the helper T cell sits at the centre of the diagram, destroying it — as
HIV does — disables **both** limbs at once. That is why AIDS patients die of
ordinary organisms: tuberculosis, *Pneumocystis* pneumonia, candidiasis, Kaposi's
sarcoma.

A **vaccine** is a preparation of killed, weakened (attenuated), toxoid or
subunit antigen that produces active artificial immunity together with memory
cells, without causing the disease.

### 9.2.5 Non-communicable diseases

| Disease | Nature | Main causes / risk factors | Prevention |
|---|---|---|---|
| Hypertension | persistent BP ≥ 140/90 mm Hg | salt, obesity, alcohol, stress, heredity | less salt, exercise, weight control |
| Coronary heart disease | narrowing of coronary arteries by atheroma | smoking, high LDL, diabetes, inactivity | no tobacco, diet, exercise |
| Stroke | brain artery blocked or ruptured | hypertension, smoking, atrial fibrillation | blood-pressure control |
| COPD | irreversible airway obstruction | tobacco smoke, biomass and indoor smoke, dust | clean cooking fuel, no smoking |
| Asthma | reversible bronchospasm | allergens, cold air, exercise, pollution | avoid triggers, inhalers |
| Diabetes mellitus | type 1 — no insulin; type 2 — insulin resistance | heredity, obesity, inactivity, sugar-rich diet | weight control, exercise |
| Cancer | uncontrolled cell division, metastasis | tobacco, chewing tobacco, HPV, radiation, aflatoxin | screening, vaccination, no tobacco |
| Goitre | enlarged thyroid | dietary iodine deficiency | iodised salt |
| Arthritis | joint inflammation / cartilage wear | age, autoimmunity, obesity | weight control, physiotherapy |
| Allergy | hypersensitivity, IgE-mediated | pollen, dust mite, foods, drugs | avoid allergen, antihistamines |

::: note Nepal's changing disease burden
Nepal is going through an **epidemiological transition**: infections are
retreating and NCDs are taking over. WHO has put the NCD share of all deaths in
Nepal at about **66 %**, and GBD-based estimates for 2019 at about **71 %**. The
Global Burden of Disease 2023 analysis ranks **chronic obstructive pulmonary
disease, ischaemic heart disease and stroke** as the three leading causes of
death, with **air pollution** the leading risk factor. Nepal's NCD **STEPS Survey
2019** (adults 15–69) found raised blood pressure in **24.5 %**, raised blood
glucose in **5.8 %**, raised total cholesterol in **11 %**, overweight or obesity
in **24.3 %**, and tobacco use in **28.9 %** (48.3 % of men, 11.6 % of women).
GLOBOCAN 2022 recorded **22,008 new cancer cases and 14,704 cancer deaths** in
Nepal.
:::

### 9.2.6 Deficiency diseases

| Missing nutrient | Disease | Chief signs |
|---|---|---|
| Protein + energy | kwashiorkor | oedema of feet, moon face, flaky skin, enlarged liver |
| Energy (severe) | marasmus | extreme wasting, "old man" face, no subcutaneous fat |
| Vitamin A | night blindness → xerophthalmia | poor vision in dim light, Bitot's spots, corneal ulcer |
| Vitamin B₁ (thiamine) | beriberi | leg oedema (wet) or nerve damage and weakness (dry) |
| Vitamin B₂ (riboflavin) | cheilosis | cracks at corners of the mouth, sore red tongue |
| Vitamin B₃ (niacin) | pellagra | the three D's — dermatitis, diarrhoea, dementia |
| Vitamin B₁₂ / folate | megaloblastic anaemia | large immature red cells, weakness, sore tongue |
| Vitamin C | scurvy | bleeding spongy gums, loose teeth, slow wound healing |
| Vitamin D | rickets (child), osteomalacia (adult) | bow legs, pigeon chest, soft painful bones |
| Vitamin K | bleeding tendency | prolonged clotting time |
| Iron | iron-deficiency anaemia | pallor, tiredness, breathlessness, spoon nails |
| Iodine | goitre; cretinism in infants | neck swelling; stunted growth and mental retardation |
| Calcium | tetany, osteoporosis | muscle cramps, brittle bones |

::: memory The three D's and the three shapes
- **Pellagra** = **D**ermatitis, **D**iarrhoea, **D**ementia (vitamin B₃).
- **Kwashiorkor** swells (oedema); **marasmus** shrinks (wasting).
- **Rickets** bends growing bone; **osteomalacia** softens grown bone.
:::

Nepal's own figures show real progress with real gaps. The **Nepal Demographic
and Health Survey 2022** found **25 % of children under five stunted** (down from
57 % in 1996), **8 % wasted** and **19 % underweight**, while **43 % of children
aged 6–59 months** and **34 % of women aged 15–49** were anaemic. Universal salt
iodisation has made endemic goitre in the hills, once very common, rare.

## Chapter summary

- $\text{CBR} = (B/P)\times 1000$; $\text{CDR} = (D/P)\times 1000$;
  $\text{RNI} = \text{CBR}-\text{CDR}$; IMR uses **live births** as denominator.
- Exponential growth: $P_t = P_0e^{rt}$, so $r = \frac{1}{t}\ln(P_t/P_0)$ and
  doubling time $T_d = 0.693/r \approx 70/R\%$.
- Dependency ratio $= \dfrac{P_{0-14}+P_{65+}}{P_{15-64}}\times 100$; for Nepal in
  2021 it is 53.3 (child 42.7, old-age 10.6).
- Census 2021: 29,164,578 people, growth 0.92 % per year, sex ratio 95.59,
  density 198 km⁻², 66.17 % urban, 2.19 million absent abroad, life expectancy
  71.3 years. NDHS 2022: TFR 2.1, IMR 28, U5MR 33. NMMS 2021: MMR 151.
- Population pyramids are expanding (broad base), stable or declining (narrow
  base); Nepal's base is now narrower than the band above it.
- The demographic transition runs from Stage 1 (high birth, high death) through
  Stage 2 (death falls, growth fastest) and Stage 3 (birth falls) to Stage 4
  (both low). Nepal is in late Stage 3.
- Malaria: human = intermediate host (schizogony in liver and RBC); female
  *Anopheles* = definitive host (gamogony and sporogony); infection by
  sporozoites in saliva.
- HIV is a retrovirus that destroys CD4⁺ helper T cells; AIDS is diagnosed when
  the CD4⁺ count falls below 200 cells mm⁻³.
- Immunity is innate or acquired; acquired immunity is active (infection or
  vaccine) or passive (placenta, colostrum, antiserum), and has a humoral
  (antibody) and a cell-mediated limb.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The definitive host of the malarial parasite is <span class="marks">[1]</span>
   (a) man (b) female *Anopheles* (c) male *Anopheles* (d) *Culex*
2. Crude death rate is expressed as deaths per <span class="marks">[1]</span>
   (a) 100 population (b) 1000 population (c) 1000 live births (d) 100,000 live births
3. AIDS is diagnosed when the CD4⁺ T-cell count falls below <span class="marks">[1]</span>
   (a) 1000 mm⁻³ (b) 800 mm⁻³ (c) 500 mm⁻³ (d) 200 mm⁻³
4. A population pyramid with a broad base and a narrow apex indicates <span class="marks">[1]</span>
   (a) a declining population (b) a stationary population (c) a rapidly growing population (d) zero growth
5. Which immunoglobulin crosses the placenta? <span class="marks">[1]</span>
   (a) IgA (b) IgM (c) IgG (d) IgE
6. The annual population growth rate reported by Nepal's 2021 census was <span class="marks">[1]</span>
   (a) 0.92 % (b) 1.35 % (c) 2.25 % (d) 2.62 %

::: note Answers to Group A
**1.** (b) — fertilisation and sporogony occur in the female *Anopheles*.
**2.** (b) — CDR is per 1000 mid-year population; (c) and (d) are IMR and MMR.
**3.** (d) — below 200 cells mm⁻³ the patient is defined as having AIDS.
**4.** (c) — many children and few old people means high birth rate and fast growth.
**5.** (c) — IgG is the only class small enough to cross the placenta, giving the newborn passive natural immunity.
**6.** (a) — 0.92 %, the lowest positive rate since censuses began in 1911.
:::

**Group B — Short answer (4 marks each)**

1. Define crude birth rate, crude death rate and rate of natural increase. A
   district of 480,000 people registered 8160 live births and 3360 deaths in one
   year; find all three rates. <span class="marks">[4]</span>
2. What is a population pyramid? Draw and label the pyramid of a rapidly growing
   population and state two features that identify it. <span class="marks">[4]</span>
3. Explain the four stages of the demographic transition model and state, with a
   reason, which stage Nepal is in. <span class="marks">[4]</span>
4. Differentiate between communicable and non-communicable diseases, giving two
   examples of each. <span class="marks">[4]</span>
5. The 2021 census counted 29,164,578 people in Nepal's area of 147,516 km².
   Calculate the population density, and the population expected in 2031 if
   growth continues at 0.92 % per year. <span class="marks">[4]</span>
6. Write short notes on active and passive immunity, with one example of
   each. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Definitions as in §9.1.1.
$\text{CBR} = \frac{8160}{480000}\times 1000 = 17.0$ per 1000;
$\text{CDR} = \frac{3360}{480000}\times 1000 = 7.0$ per 1000;
$\text{RNI} = 17.0 - 7.0 = 10.0$ per 1000, i.e. **1.0 % per year** (doubling time
$\approx 70$ years).

**3.** Outline: Stage 1 both rates high, growth near zero; Stage 2 death rate
falls (clean water, vaccines) while birth rate stays high, growth fastest; Stage 3
birth rate falls (contraception, female education), growth slows; Stage 4 both
rates low, growth near zero. Nepal is in **late Stage 3** — CDR is already low
(about 6 per 1000) and the birth rate has fallen to about 19 per 1000 with TFR
2.1, so natural increase is small but still positive.

**5.** Density $= \dfrac{29\,164\,578}{147\,516} = 197.7 \approx 198$ persons km⁻².

$$ P_{2031} = 29\,164\,578\times e^{0.0092\times 10} = 29\,164\,578\times 1.0964
= 3.20\times 10^{7} $$

About **32.0 million** — an increase of roughly 2.8 million in ten years.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the life cycle of *Plasmodium vivax* in man and in the mosquito
   with a labelled diagram. <span class="marks">[6]</span>
   (b) Name the vector, state why the mosquito is called the definitive host, and
   give two control measures used in Nepal. <span class="marks">[2]</span>
2. (a) Draw a labelled diagram of the HIV virion and describe how HIV infects a
   helper T cell. <span class="marks">[4]</span>
   (b) List the modes of transmission of HIV, describe the three clinical phases
   of untreated infection, and state four preventive measures. <span class="marks">[4]</span>
3. The 2011 census recorded 26,494,504 people and the 2021 census 29,164,578, an
   interval of 10.43 years. The 2021 age distribution was 0–14: 8,115,575;
   15–64: 19,027,289; 65+: 2,021,714.
   (a) Calculate the annual growth rate and the doubling time. <span class="marks">[4]</span>
   (b) Calculate the total, child and old-age dependency ratios and explain what
   they tell a planner about Nepal's future. <span class="marks">[4]</span>

::: note Answer outline to Group C question 3
(a) $P_t/P_0 = 1.1008$, $\ln 1.1008 = 0.0960$, so
$r = 0.0960/10.43 = 0.00921 = 0.92\ \%$ per year, and
$T_d = 0.693/0.00921 = 75.2$ years.

(b) Total dependency $= \frac{10\,137\,289}{19\,027\,289}\times 100 = 53.3$;
child $= 42.7$; old-age $= 10.6$. Interpretation: two-thirds of Nepalis are of
working age, so the country is inside its **demographic dividend** and needs jobs
and skills above all. But old-age dependency is rising (65+ rose from 5.27 % of
the population in 2011 to 6.93 % in 2021), so pensions, geriatric care and NCD
services must be built now, before the dividend closes.
:::

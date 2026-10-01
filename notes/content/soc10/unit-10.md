---
subject: Social Studies and Human Value Education
grade: 10
unit: 10
title: Population and Its Management
hours: 0
area: Units
---

Nepal has about 29 million people. They live on 147,516 square kilometres of land that runs from the hot Terai to the snows of the Himalaya, and they are not spread evenly: more than half live in the Terai, a million live in the Kathmandu Valley alone, while whole districts of the mountains hold only a few thousand. How many people there are, how fast they are growing, how old they are, where they live, how healthy they are and what they do to the environment are all questions of **population**. Study them well, because the schools, hospitals, jobs, roads and food of the next generation depend on the answers. All the figures in this unit come from the **National Population and Housing Census 2021** of the National Statistics Office.

::: key What the SEE paper expects from this unit
Be ready to define population terms (census, growth rate, density, sex ratio, dependency ratio), to read a table or diagram of census data and to calculate density or growth, to explain **causes and effects** of uneven distribution and rapid growth, to list **family-planning methods and benefits**, to describe the relation between **population and environment**, and to describe **community health** measures. Quote 2021 census figures correctly.
:::

## 10.1 Size and growth of Nepal's population

### Census and population size

A **census** is the official count of all people living in a country on a given day, together with information on their age, sex, education, work and housing. Nepal's first (partial) census was taken in **1911 AD (1968 BS)**; modern censuses began in 1952/54 and are now held **every ten years**. The 12th census was held on **25 November 2021 (10 Mangsir 2078 BS)**. It counted **29,164,578 people**, of whom 14,253,551 are male (48.87%) and 14,911,027 female (51.13%). The census also counted 2,928 persons who reported "other gender", the first time such information was collected.

| Census year | Population | Increase since previous census | Annual growth rate (%) |
|---|---|---|---|
| 1911 | 5,638,749 | — | — |
| 1941 | 6,283,649 | — | 1.16 |
| 1952/54 | 8,256,625 | 1,972,976 | 2.27 |
| 1961 | 9,412,996 | 1,156,371 | 1.64 |
| 1971 | 11,555,983 | 2,142,987 | 2.05 |
| 1981 | 15,022,839 | 3,466,856 | 2.62 |
| 1991 | 18,491,097 | 3,468,258 | 2.08 |
| 2001 | 23,151,423 | 4,660,326 | 2.25 |
| 2011 | 26,494,504 | 3,343,081 | 1.35 |
| **2021** | **29,164,578** | **2,670,074** | **0.92** |

```figure caption="Population of Nepal (bars, millions) and annual growth rate (line, per cent) at each census since 1952/54. The growth rate peaked at 2.62% in 1981 and has fallen to 0.92% in 2021."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
yrs = ["1952/54","1961","1971","1981","1991","2001","2011","2021"]
pop = [8.26,9.41,11.56,15.02,18.49,23.15,26.49,29.16]
gr = [2.27,1.64,2.05,2.62,2.08,2.25,1.35,0.92]
x = np.arange(len(yrs))
ax.bar(x, pop, color=ACCENT, width=0.6)
for i,v in enumerate(pop): ax.text(i, v+0.5, f"{v:.1f}", ha="center", fontsize=7, color=INK)
ax.set_xticks(x); ax.set_xticklabels(yrs, fontsize=7)
ax.set_ylabel("Population (million)", fontsize=8); ax.set_ylim(0,58)
ax2 = ax.twinx()
ax2.plot(x, gr, color=SERIES[1], marker="o", lw=1.8)
for i,v in enumerate(gr): ax2.text(i, v+0.12, f"{v}", ha="center", fontsize=7, color=SERIES[1])
ax2.set_ylim(-2.4,3.2); ax2.set_ylabel("Growth rate (%)", fontsize=8, color=SERIES[1])
ax.spines[['top']].set_visible(False); ax2.spines[['top']].set_visible(False)
ax.tick_params(labelsize=7.5); ax2.tick_params(labelsize=7.5)
```

### How population changes

Population changes through three things: **births** (fertility), **deaths** (mortality) and **migration**.

| Term | Meaning |
|---|---|
| **Crude birth rate (CBR)** | Live births per 1,000 people in a year |
| **Crude death rate (CDR)** | Deaths per 1,000 people in a year |
| **Natural increase** | Births minus deaths |
| **Growth rate** | Percentage change in population per year (natural increase plus net migration) |
| **Net migration** | Immigrants minus emigrants |

$$\text{Growth rate} \; (\%) = \frac{\text{CBR} - \text{CDR}}{10} + \frac{\text{net migration rate}}{10}$$

::: example Natural increase and doubling time
**Problem.** A country has a crude birth rate of 22 and a crude death rate of 6 per 1,000, with no migration. Find (a) the natural increase rate per 1,000, (b) the annual growth rate in per cent and (c) the approximate number of years it takes the population to double (rule of 70).

**Solution.**
(a) Natural increase = 22 − 6 = **16 per 1,000**.
(b) Growth rate = 16 ÷ 10 = **1.6 per cent** a year.
(c) Doubling time ≈ 70 ÷ 1.6 = **about 44 years**.
For Nepal's present growth of 0.92 per cent, doubling time would be 70 ÷ 0.92 ≈ 76 years.
:::

::: example Where does the 0.92 per cent come from?
**Problem.** The population was 26,494,504 in 2011 and 29,164,578 in 2021. The census dates are 10.43 years apart. Find the annual exponential growth rate.

**Solution.** Ratio = 29,164,578 ÷ 26,494,504 = 1.1008.
Natural logarithm of 1.1008 = 0.0960.
Rate = 0.0960 ÷ 10.43 = 0.00920, or **0.92% a year**.
(Dividing by 10 years instead would give 0.96%, which is why the exact interval is used.)
:::

### Why the growth rate rose and then fell

| Period | What happened |
|---|---|
| **1950s–1980s** | Malaria control in the Terai, vaccines, better food and health care caused **death rates to fall quickly** while **birth rates stayed high**; opening of the Terai attracted migrants. Growth rose to 2.62% in 1981. |
| **1990s–2000s** | Growth stayed above 2% as population momentum continued, but family planning, education and urban life began to lower births |
| **2011–2021** | Growth fell to 0.92%. Reasons: **fewer births** (the fertility rate is about 2.1 children per woman, at the replacement level), later marriage, more education of girls, and **large emigration** (the census counted **2,190,592 Nepalis absent abroad**, 82% of them men) |

Growth is not equal in all places. Between 2011 and 2021, **Bhaktapur (3.35%)** grew fastest, while **Ramechhap (−1.67%)** and many hill and mountain districts lost people. The Mountain belt (−0.05%) shrank slightly, the Hill grew by 0.30% and the Terai by 1.54% a year.

### Uses of census data

Census data are the base of all planning. The government and municipalities use them to decide where to build schools and health posts, how many teachers and doctors are needed, how to divide the national budget among provinces and local levels, how to draw electoral constituencies, how to measure poverty, literacy and housing, and how to plan food, jobs and pensions. Without a census a country is planning in the dark. That is why every person must answer the census honestly and why Nepal conducted it even during the Covid-19 pandemic.

### Demographic transition

Countries pass through stages as they develop. In the first stage, birth and death rates are both high and population grows slowly; in the second, death rates fall (health and food improve) while birth rates stay high and population grows rapidly; in the third, birth rates also fall (education, family planning, urban life) and growth slows; in the fourth, both are low and the population is stable or ageing. **Nepal is in the late-second to third stage**: death rates have fallen steeply, and birth rates are now low enough that the growth rate is below 1 per cent.

```figure caption="The demographic transition (schematic). Death rate falls first, birth rate later; the gap between them is the natural increase."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
x = np.linspace(0,10,200)
birth = 40 - 25/(1+np.exp(-(x-6.5)*1.2))
death = 39 - 31/(1+np.exp(-(x-3.5)*1.4))
ax.plot(x, birth, color=SERIES[1], lw=2, label="Birth rate")
ax.plot(x, death, color=ACCENT, lw=2, label="Death rate")
ax.fill_between(x, death, birth, where=birth>death, color="#e8f0fb")
for xs,lab in ((1,"Stage 1"),(3.5,"Stage 2"),(6.5,"Stage 3"),(9,"Stage 4")):
    ax.text(xs, 2, lab, ha="center", fontsize=8, color=INK)
for xb in (2.3,5.0,8.0):
    ax.axvline(xb, color=GRID, lw=1)
ax.text(4.7,28,"Natural increase", fontsize=8, color=INK)
ax.legend(fontsize=8, frameon=False, loc="upper right")
ax.set_xlabel("Time (development)", fontsize=8); ax.set_ylabel("Rate per 1,000", fontsize=8)
ax.set_ylim(0,45); ax.set_xticks([])
ax.spines[['top','right']].set_visible(False)
ax.tick_params(labelsize=8)
```

### Effects of rapid population growth

Rapid growth strains food, land, schools, jobs, health services and the environment, and makes it harder to raise **per capita income**. Very slow growth with an ageing population brings other problems. Therefore the goal of **population management** is not to hit a number but to make sure that population size, structure and distribution suit the country's resources.

## 10.2 Composition of the population

Composition means the structure of the population: its age, sex, caste/ethnicity, language, religion, education and rural-urban division.

### Age structure

Demographers divide people into three broad groups:

| Age group | Share in 2021 | Meaning |
|---|---|---|
| **0–14 years** (children) | **27.83%** | Dependent; need school and care |
| **15–59 years** (working age) | **61.96%** | Economically active; produce and pay tax (56.96% in 2011) |
| **60 years and above** (elderly) | **10.21%** | Often dependent; need health care and pensions |

::: definition Dependency ratio
The dependency ratio is the number of dependent persons (children under 15 plus persons aged 60 and above) for every 100 persons of working age (15–59).
:::

::: example Dependency ratio of Nepal, 2021
**Problem.** Use the 2021 census age shares to find Nepal's total dependency ratio.

**Solution.** Dependents = 27.83% + 10.21% = 38.04%.
Working age = 61.96%.
Dependency ratio = (38.04 ÷ 61.96) × 100 = **61.4**.
So there are about 61 dependents for every 100 working-age persons. The ratio was higher in 2011 because there were more children.
:::

A big working-age share and few dependants can be a **demographic dividend**: a chance for fast growth if there are enough jobs and skills. If the young have no jobs, the chance is lost. Meanwhile the number of **elderly** is rising fast, so pensions, senior-citizen allowances and health care need planning.

### The population pyramid

A **population pyramid** is a double bar graph showing the numbers of males and females in each five-year age group. Its shape tells the story: a broad base means many births, and a narrow top means few old people.

```figure caption="Population pyramid of Nepal, census 2021 (per cent of total population in each five-year age group; males left, females right). The base is narrowing; the bulge at ages 10-24 is the 'youth bulge'. The females aged 20-39 are more numerous than the males because so many men are abroad."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.4))
ages = ["0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85+"]
m = [1290525,1443405,1495954,1494523,1301018,1122242,978976,936931,828493,687525,692494,537558,465962,379689,292054,170998,78315,56889+36888+13191]
f = [1148758,1323022,1413911,1471881,1482042,1337107,1168736,1104561,919339,748515,721358,538386,489642,391929,317316,182205,83241,69078+41439+17215]
tot = 29164578
mm = [-v/tot*100 for v in m]; ff = [v/tot*100 for v in f]
y = np.arange(len(ages))
ax.barh(y, mm, color=ACCENT, height=0.85, label="Male")
ax.barh(y, ff, color=SERIES[1], height=0.85, label="Female")
ax.set_yticks(y); ax.set_yticklabels(ages, fontsize=7)
ax.set_xlim(-12,12)
ax.set_xticks([-10,-5,0,5,10]); ax.set_xticklabels(["10","5","0","5","10"], fontsize=7.5)
ax.set_xlabel("Per cent of total population", fontsize=8)
ax.set_ylabel("Age group (years)", fontsize=8)
ax.legend(fontsize=8, frameon=False, loc="upper right")
ax.spines[['top','right']].set_visible(False)
```

### Sex composition

**Sex ratio** is the number of males per 100 females.

$$\text{Sex ratio} = \frac{\text{number of males}}{\text{number of females}} \times 100$$

::: example Sex ratio
**Problem.** In 2021 Nepal had 14,253,551 males and 14,911,027 females. Find the sex ratio.

**Solution.** Sex ratio = (14,253,551 ÷ 14,911,027) × 100 = **95.59**.
There are about 96 males for every 100 females. It was 94.16 in 2011. The ratio is below 100 mainly because of **male emigration**: women outnumber men in the 20–44 age groups.
:::

### Other aspects of composition

| Aspect | Main facts (census 2021) |
|---|---|
| **Ethnic/caste diversity** | More than 140 caste and ethnic groups (142 recorded), among them Chhetri, Brahmin, Magar, Tharu, Tamang, Newar, Dalit communities, Madhesi groups, Kirat peoples and many Janajati groups |
| **Language** | 124 mother tongues; Nepali is the mother tongue of about 45 per cent; Maithili, Bhojpuri, Tharu, Tamang, Bajjika and Magar follow |
| **Religion** | Hindu (about 81 per cent), Buddhist (about 8 per cent), Muslim (about 5 per cent), Kirat (about 3 per cent), Christian (under 2 per cent) |
| **Literacy** | **76.2%** of those aged 5+ (male 83.6%, female 69.4%); it was 65.9% in 2011 |
| **Urban and rural** | **66.17%** live in urban municipalities; 33.83% in rural municipalities |
| **Households** | 6,666,937 households; average size **4.37** (4.88 in 2011); 31.55% headed by women |
| **Disability** | 2.2% of the population have a disability |
| **Absentees** | 2,190,592 persons absent abroad (23.4% of households have a member abroad) |

::: tip Compare 2011 and 2021
SEE questions often ask for a trend: "literacy rose from 65.9% to 76.2%", "household size fell from 4.88 to 4.37", "growth fell from 1.35% to 0.92%". A comparison with two numbers is worth more than a vague word like "improved".
:::

### Ageing and senior citizens

Because people live longer and have fewer children, the share of those aged 60 and above rose to **10.21%** in 2021 (about three million people). Nepal gives a **senior citizen allowance** (monthly social security allowance) to those aged 70 and above, and 60 and above in certain cases (such as Dalits, and those in Karnali), and the Constitution guarantees the rights of senior citizens. Families and communities must give respect, health care and company to the elderly; they carry the knowledge and culture of the community.

### Population policy

The **National Population Policy 2071 BS (2015)** aims to improve the quality of life by balancing population size, structure and distribution with resources, by promoting reproductive health and women's empowerment, by managing migration and urbanisation, and by preparing for the ageing population and use of the demographic dividend. It is carried out through the Ministry of Health and Population, the National Statistics Office and the local governments.

## 10.3 Distribution of population

**Population distribution** is the way people are spread over the land. **Population density** is the average number of persons per square kilometre.

$$\text{Density} = \frac{\text{population}}{\text{area in km}^2}$$

::: example Population density
**Problem.** Nepal has a population of 29,164,578 and an area of 147,516 km². Find the density. A district has 120,000 people on 3,000 km². Find its density.

**Solution.** Nepal: 29,164,578 ÷ 147,516 = **197.7 ≈ 198 persons per km²**.
District: 120,000 ÷ 3,000 = **40 persons per km²**, which is far below the national figure.
:::

### Distribution in Nepal, 2021

| Region | Population | Share | Density (per km²) | Growth 2011–21 (%) |
|---|---|---|---|---|
| **Mountain** | 1,772,948 | 6.08% | **34** | −0.05 |
| **Hill** | 11,757,624 | 40.31% | 192 | 0.30 |
| **Terai (Tarai)** | 15,634,006 | **53.61%** | **460** | 1.54 |
| **Nepal** | 29,164,578 | 100% | 198 | 0.92 |

| Province | Population | Density (per km²) |
|---|---|---|
| Koshi | 4,961,412 | 192 |
| Madhesh | 6,114,600 | **633** |
| Bagmati | 6,116,866 | 301 |
| Gandaki | 2,466,427 | 115 |
| Lumbini | 5,122,078 | 230 |
| Karnali | 1,688,412 | **60** |
| Sudurpashchim | 2,694,783 | 138 |

```figure caption="Population density of Nepal's seven provinces, census 2021 (persons per square kilometre). The national average is 198."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
names = ["Madhesh","Bagmati","Lumbini","Koshi","Sudurpashchim","Gandaki","Karnali"]
vals = [633,301,230,192,138,115,60]
y = np.arange(len(names))[::-1]
cols = [SERIES[1] if v>198 else ACCENT for v in vals]
ax.barh(y, vals, color=cols)
ax.axvline(198, color=INK, ls="--", lw=1)
ax.text(210, 0, "National average 198", fontsize=7.5, color=INK, va="center")
for yy,v in zip(y,vals): ax.text(v+8, yy, str(v), va="center", fontsize=8, color=INK)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8)
ax.set_xlim(0,720); ax.set_xlabel("Persons per sq km", fontsize=8)
ax.tick_params(labelsize=8)
ax.spines[['top','right']].set_visible(False)
```

**Extremes:** the most populous district is **Kathmandu** (2,041,587 persons; density **5,169 per km²**); the least populous is **Manang** (5,658 persons; density **3 per km²**). Morang, Rupandehi, Jhapa and Sunsari follow Kathmandu in size. **Bagmati** is the largest province (20.97%) and **Karnali** the smallest (5.79%).

```photo id="soc10/ktm-haze" caption="The Kathmandu Valley seen from the Shivapuri hills under haze. With about 2 million people in Kathmandu district alone, the valley is Nepal's densest and fastest-urbanising region, with its traffic, dust and waste." width="86"
```

### Causes of uneven distribution

| Factor | Effect |
|---|---|
| **Relief** | Plains and river valleys are flat and easy to farm and build on (Terai, Kathmandu Valley); steep, high land has few people |
| **Climate** | Warm, moist land supports crops; very cold, dry highlands do not |
| **Soil and water** | Fertile alluvium of the Terai and fresh water attract settlement |
| **Transport** | Roads, airports and markets bring people (East-West Highway, Kathmandu Valley) |
| **Economic opportunity** | Cities, industries, offices, tourism and trade offer jobs |
| **Services** | Schools, hospitals and electricity attract people |
| **History and politics** | Eradication of malaria and the resettlement programmes opened the Terai from the 1950s |
| **Hazards** | Landslides and floods push people away; earthquakes damage cities |

### Migration

**Migration** is the movement of people from one place to another to live. **Internal migration** takes place within the country (hill to Terai, village to town); **international migration** crosses the border (Nepalis to India, the Gulf, Malaysia and developed countries).

| Push factors (make people leave) | Pull factors (draw them in) |
|---|---|
| Poverty, unemployment, low income | Jobs and higher wages |
| Lack of schools, health care and roads | Better services in cities |
| Natural disasters, landslides | Fertile land and security |
| Conflict (the 1996–2006 conflict) | Education, business, family and marriage |

In the census, **marriage** (38.2%), dependent family member (19.5%) and **work or job** (15.2%) were the most common reasons for the 9.3 million people who had changed their place of residence. The result is rapid growth of towns: two-thirds of Nepalis now live in urban municipalities, but many are small towns, and some hill villages are left with only the old and the very young.

### Problems

Overcrowded cities (traffic, housing shortage, pollution, waste, informal settlements); emptying villages (abandoned farms, shortage of labour); pressure on Terai forests; inequality between regions; difficult service delivery to scattered mountain villages. **Solutions:** balanced development, roads and electricity for the hills, rural jobs, decentralised services under federalism, planned cities, and land-use zoning.

## 10.4 Family planning and quality of life

::: definition Family planning
Family planning is the voluntary decision of couples to decide the number of children and the interval between births, using safe and effective methods, so that every child is wanted and cared for.
:::

### Methods

| Type | Methods |
|---|---|
| **Temporary (spacing)** | **Condom**; **oral pills**; **injectable** (Depo-Provera, 3-monthly); **implant** (under the skin of the arm, lasts 3–5 years); **IUCD** (Copper-T); natural methods such as the calendar method |
| **Permanent (limiting)** | **Vasectomy** (male) and **minilap / tubectomy** (female) |
| **Emergency** | Emergency contraceptive pills |

Family-planning counselling and most methods are available free at government health posts and hospitals across Nepal.

### Benefits

- **Health of mothers**: spacing births by at least **three years** reduces the risk of death in childbirth; the **maternal mortality ratio** fell to **151 per 100,000 live births** in the 2021 census.
- **Health of children**: well-spaced and wanted children are healthier, better fed and less likely to die; fewer deaths below age five.
- **Education and opportunity**: parents can afford to send all children to school, especially girls; women gain time for work and learning.
- **Economic benefit**: lower expenses, higher savings and a better living standard; less pressure on land, food, forests and public services.
- **Rights and choice**: a woman and man can make their own decision about family, reducing early marriage and teenage pregnancy.
- **National benefit**: slower population growth makes it easier to provide schools, jobs and health care.

Nepal's progress: the **total fertility rate** has dropped from about 5 children per woman in the 1990s to about **2.1** today (Nepal Demographic and Health Survey 2022), and the average age at first marriage has risen (the median is 19 years: 21 for males and 18 for females). The legal age of marriage is **20** for both sexes.

### Safe motherhood and child survival

Nepal's health indicators have improved quickly. The maternal mortality ratio fell from about 539 per 100,000 live births in 1996 to **151** in the 2021 census, and the infant mortality rate (about 28 per 1,000 live births in 2022) and under-five mortality have fallen sharply compared with the 1990s. The causes are the Safe Motherhood Programme, free delivery under the **Aama programme**, more **skilled birth attendants**, birthing centres in rural areas, immunisation, vitamin A supplements and better nutrition. Remaining problems are anaemia, **stunting** (about a quarter of children under five are too short for their age), early marriage and teenage pregnancy, and unequal access in remote districts.

### Quality of life

Quality of life means the level of wellbeing of people: health, education, income, housing, safe water, freedom, security, a clean environment and social relations. It is measured by indicators such as the **Human Development Index (HDI)** (income, education and life expectancy), literacy, life expectancy (about 70 years), child and maternal mortality, access to electricity (92.2% of households use electricity for lighting) and sanitation (95.5% of households have a toilet).

| Small, planned family | Large family with poor spacing |
|---|---|
| Food, health, education for all children | Limited resources shared among many |
| Mother's health protected | Mothers at higher risk |
| Savings and investment possible | Little saving; debt |
| Time for education and work for parents | Early school leaving of children |

::: caution Family planning is not forced
Family planning is a **voluntary** choice by the couple, supported by information and services. It is not a compulsory limit by the state, and it is not just for women: men share the responsibility.
:::

## 10.5 The relationship between population and environment

**Environment** is everything around us: air, water, soil, forests, wildlife and the things humans have built. People depend on it and also change it.

### How population affects the environment

| Pressure | Effect on the environment |
|---|---|
| **More people needing food** | Forest and grass cleared for farms; overgrazing; chemical fertilisers pollute water |
| **More fuel and timber** | Deforestation, firewood use (about 51% of households still cook mainly with firewood), forest fires |
| **More houses and roads** | Farmland and wetlands lost; hill roads trigger landslides; cities spread |
| **More vehicles and industries** | **Air pollution** (Kathmandu often has unhealthy air in winter); noise |
| **More waste** | Garbage, plastic, polluted rivers (Bagmati), landfill problems |
| **More water use** | Shortage of drinking water; falling groundwater and drying springs |
| **More energy use** | Greenhouse-gas emissions leading to climate change and glacier melt |

### How the environment affects population

A healthy environment feeds and shelters people; a damaged one harms them. Floods, landslides, drought and earthquakes cause deaths and displacement; polluted air and water cause disease; loss of fertile land forces migration; and climate change threatens farming and water supply.

```figure caption="The two-way link between population and environment (schematic). Growth in numbers increases the demand for resources; damage to the environment then reduces the quality of life."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
def box(x,y,w,h,t,c):
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=8,color=INK,bbox=dict(boxstyle="round,pad=0.4",fc=c,ec=INK,lw=0.8))
box(0.3,1.5,1.7,0.8,"Population growth","#cfe0f5")
box(3.5,2.5,2.2,0.8,"Demand for food,\nfuel, land, water","#fbe5c4")
box(3.5,0.4,2.2,0.8,"Lower quality\nof life","#d9efd3")
box(6.5,1.5,2.2,0.8,"Pollution, forest loss,\nclimate change","#f6d4d0")
for a,b in (((2.1,2.1),(3.4,2.8)),((5.8,2.7),(7.2,2.35)),((7.3,1.45),(5.8,0.95)),((3.4,0.8),(1.4,1.4))):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1.2))
ax.set_xlim(0,9); ax.set_ylim(0,3.7); ax.axis("off")
```

### Nepal's examples

- **Forest:** forests cover about **45 per cent** of Nepal (about 6.6 million hectares). Nepal is a world leader in **community forestry**: around 22,000 community forest user groups manage forests for the benefit of villagers, and forest cover has recovered in the middle hills since the 1990s.
- **Kathmandu Valley:** urban sprawl, vehicles, brick kilns and burning waste make air quality poor in the dry months; the Bagmati and its tributaries are heavily polluted by sewage.
- **Terai:** land clearing, brick kilns, groundwater depletion and Churia hills erosion.
- **Mountains:** melting glaciers, glacial-lake floods and rubbish along trekking trails (Everest).

### Solutions

1. **Control population growth** through family planning and women's education.
2. **Plant and protect forests**; support community forests; promote alternatives to firewood: LPG, biogas, electricity and improved cookstoves.
3. **Waste management**: the 3Rs: *reduce, reuse, recycle*; segregate waste; ban single-use plastic bags.
4. **Clean transport and energy**: public transport, electric vehicles, solar and hydropower.
5. **Planned settlements and land-use rules**; no building on floodplains and steep slopes; green spaces.
6. **Environmental education** and law: the Environment Protection Act 2076 (2019).
7. **Sustainable development**: meeting today's needs without harming the needs of future generations (SDGs).

::: key Carrying capacity
An area's **carrying capacity** is the maximum number of people that its resources can support in a sustainable way. If the population is larger than the carrying capacity, the environment is damaged; clever use of technology can raise the limit but cannot remove it.
:::

## 10.6 Community health

### Meaning

The World Health Organization defines **health** as "a state of complete physical, mental and social well-being and not merely the absence of disease or infirmity". **Community health** is the organised effort of the community, the government and others to protect and improve the health of **all** the people of a locality, especially through prevention.

### Components

| Component | Examples |
|---|---|
| **Safe drinking water and sanitation** | Tap water (57% of households), toilets (95.5%), the declaration of Nepal as **open-defecation-free in 2019** |
| **Nutrition** | Balanced diet, breastfeeding for 6 months, vitamin A and iron supplements, school meals |
| **Immunisation** | The Expanded Programme on Immunisation: BCG, DPT-HepB-Hib, polio, pneumococcal, rotavirus, measles-rubella, Japanese encephalitis, typhoid, HPV |
| **Maternal and child health** | Antenatal check-ups, skilled birth attendants, institutional delivery, **Aama programme** (free delivery and transport allowance), growth monitoring |
| **Disease control** | TB, malaria, HIV/AIDS, dengue, diarrhoea, pneumonia; health surveillance |
| **Health education** | Hand-washing, safe food, oral rehydration solution, avoid tobacco and alcohol, adolescent health |
| **First aid and emergency** | Basic first aid, ambulances, disaster preparedness |
| **Mental health** | Counselling, stress control, suicide prevention, reducing stigma |

```photo id="soc10/health-post" caption="A health post in Batulechaur, Pokhara. Health posts and basic health service centres are the first point of care in Nepal's three-tier health system and offer immunisation, maternal and child care, family planning and basic treatment, often free of cost." width="76"
```

### Nepal's community health system

- The **Constitution of Nepal** guarantees free basic health services as a fundamental right; the **Public Health Service Act (2018/2075 BS)** and the **Health Insurance Act (2017)** expand it.
- **Three tiers:** the federal government (policy, central hospitals), provinces (provincial hospitals) and **local governments** (health posts, basic hospitals).
- **Female Community Health Volunteers (FCHVs):** about 50,000 women volunteers, since 1988, who distribute vitamin A, oral rehydration solution and contraceptives and spread health messages; one of Nepal's greatest community-health successes.
- **Public health achievements:** smallpox eradicated (the last case in Nepal in 1973); **polio-free** certification in 2014; elimination of **maternal and neonatal tetanus** (2005); **trachoma** eliminated as a public health problem (2018); major falls in child death and maternal mortality; **Covid-19** vaccination.

### Common health problems

| Communicable diseases | Non-communicable diseases |
|---|---|
| Diarrhoea, typhoid, pneumonia, TB, malaria, dengue, hepatitis | Diabetes, high blood pressure, heart disease, cancer, lung disease |
| Spread by germs, water, food, insects and contact | Related to lifestyle, tobacco, alcohol, inactivity, pollution and ageing |
| Control: vaccines, clean water, sanitation, vector control | Control: healthy diet, exercise, regular checks, no smoking |

### What can we do?

Wash hands with soap before eating and after using the toilet; drink boiled or filtered water; keep the surroundings clean and kill mosquito breeding sites; get all vaccines on time; eat a balanced diet; take part in school and community health campaigns; avoid tobacco, drugs and alcohol; and visit the health post early rather than late.

::: tip Health answer pattern
For "Explain the measures of community health", write: **safe water and sanitation, immunisation, nutrition, maternal and child health, health education and disease control**; add one Nepali fact to each, such as the FCHV programme or polio-free status in 2014.
:::

## Chapter summary

- The 2021 census counted **29,164,578** people (male 48.87%, female 51.13%); growth rate **0.92%** (1.35% in 2011); the rate peaked at **2.62% in 1981**. **2.19 million** Nepalis were absent abroad.
- Growth = (CBR − CDR) ÷ 10 (plus net migration); doubling time ≈ 70 ÷ rate.
- **Composition:** 0–14: **27.83%**; 15–59: **61.96%**; 60+: **10.21%**; dependency ratio ≈ 61.4; **sex ratio 95.59**; literacy **76.2%**; **66.17%** urban; household size 4.37.
- **Density** = population ÷ area: Nepal **198**; Terai 460, Hill 192, Mountain 34; Madhesh 633 (highest province), Karnali 60 (lowest); Kathmandu 5,169, Manang 3.
- Uneven distribution is due to relief, climate, soil, transport, jobs and services; **migration** is driven by push and pull factors.
- **Family planning**: temporary and permanent methods; benefits for health, education, income and environment; TFR about 2.1; maternal mortality ratio 151.
- Population and environment affect each other; pressures include deforestation, pollution, waste and climate change; solutions include family planning, community forestry, 3Rs and clean energy.
- **Community health** works through water and sanitation, nutrition, immunisation, maternal and child health, education and disease control; FCHVs and health posts are the base; polio-free in 2014; ODF in 2019.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The total population of Nepal in the census of 2021 was <span class="marks">[1]</span>
   (a) 26,494,504 (b) 28,000,000 (c) 29,164,578 (d) 30,500,000
2. The population density of Nepal in 2021 was about <span class="marks">[1]</span>
   (a) 98 (b) 198 (c) 298 (d) 460
3. Which district has the highest population? <span class="marks">[1]</span>
   (a) Morang (b) Kathmandu (c) Jhapa (d) Rupandehi
4. The sex ratio is the number of <span class="marks">[1]</span>
   (a) females per 100 males (b) males per 100 females (c) children per 100 adults (d) births per 1,000 people
5. The ecological belt with the highest share of Nepal's population is <span class="marks">[1]</span>
   (a) Mountain (b) Hill (c) Terai (d) Himal
6. Which of the following is a permanent method of family planning? <span class="marks">[1]</span>
   (a) Condom (b) Pills (c) Vasectomy (d) Implant
7. Nepal was declared open-defecation-free in <span class="marks">[1]</span>
   (a) 2010 (b) 2014 (c) 2019 (d) 2022
8. The percentage of Nepal's population aged 60 and above in 2021 was <span class="marks">[1]</span>
   (a) 5.2 (b) 10.21 (c) 27.83 (d) 61.96

::: note Answers to Group A
**1.** (c): 29,164,578.
**2.** (b): 29,164,578 ÷ 147,516 ≈ 198.
**3.** (b): Kathmandu, 2,041,587 persons.
**4.** (b): males per 100 females.
**5.** (c): 53.61% live in the Terai.
**6.** (c): vasectomy; condoms, pills and implants are temporary.
**7.** (c): 2019.
**8.** (b): 10.21%.
:::

**Group B — Short answer (2 marks each)**

1. What is a population census? <span class="marks">[2]</span>
2. Define population density and write the formula. <span class="marks">[2]</span>
3. Mention any two reasons for the decline of Nepal's growth rate to 0.92%. <span class="marks">[2]</span>
4. A district has 240,000 people and an area of 1,200 km². Calculate its density. <span class="marks">[2]</span>
5. Write any two benefits of family planning. <span class="marks">[2]</span>
6. What is community health? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A census is the official count of all people of a country on a particular day, with their age, sex, education, work and housing. Nepal holds one every ten years.
**2.** Population density is the average number of persons per square kilometre. Density = population ÷ area (km²).
**3.** Fall in birth rate (family planning, education of girls, later marriage); large emigration abroad (2.19 million absentees). (Any two.)
**4.** Density = 240,000 ÷ 1,200 = **200 persons per km²**.
**5.** Protects the health of mothers and children; lets parents educate all children; reduces pressure on resources. (Any two.)
**6.** Community health is the organised effort of the people, government and others to protect and improve the health of all the people of a locality, mainly through prevention.
:::

**Group C — Long answer (4 marks each)**

1. Explain the causes of uneven distribution of population in Nepal. <span class="marks">[4]</span>
2. Describe the age composition of Nepal's population from the 2021 census and its importance. <span class="marks">[4]</span>
3. Explain the benefits of family planning. <span class="marks">[4]</span>
4. Explain the relationship between population and environment, with four suggestions for protecting the environment. <span class="marks">[4]</span>
5. Describe the measures of community health in Nepal. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Relief (Terai plains, valleys dense; mountains sparse: Terai 460 vs Mountain 34); climate; soil and water; transport; jobs and urban facilities; services; history (malaria control and resettlement); natural hazards. Use the examples Kathmandu (5,169) and Manang (3).
**2.** 0–14: 27.83%; 15–59: 61.96%; 60+: 10.21%. The dependency ratio is about 61. A large working-age group is a demographic dividend if jobs are available; the share of the elderly is rising so pensions and health services are needed; the child share has fallen so family planning is working.
**3.** Health of mother and child; spacing of births; education of children; lower expenses and higher savings; less pressure on resources and environment; women's empowerment; better quality of life.
**4.** More people need food, fuel, houses and water, causing deforestation, pollution, waste and climate change; a damaged environment causes disease, disasters and migration. Suggestions: family planning; plant and protect forests; manage waste by the 3Rs; use clean energy and public transport.
**5.** Safe water and sanitation; immunisation; nutrition; maternal and child care (Aama programme, birthing centres); health education; disease control; FCHVs and health posts; free basic health services and insurance; mental health and first aid.
:::


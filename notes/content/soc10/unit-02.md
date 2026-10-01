---
subject: Social Studies and Human Value Education
grade: 10
unit: 2
title: Development and the Foundations of Development
hours: 0
area: Units
---

A country is not developed just because it has tall buildings. A country develops when its people live long and healthy lives, learn, earn a decent income, take part in decisions, and leave a healthy planet for their children. This unit follows that idea through four topics: how development is measured (the Human Development Index), how it can last (sustainable development), how power is shared to bring it closer to the people (federalism in Nepal) and which very large projects Nepal has chosen as engines of change (national pride projects). Many of the facts here are numbers and dates, so a careful reader will collect easy marks.

::: key What the SEE paper expects from this unit
Typical questions: "What is HDI? Write its three indicators." (2 marks); "Write the meaning of sustainable development" (2 marks); "Name the three tiers of government of Nepal" (1 or 2 marks); "Explain the importance of national pride projects" or "Describe the federal structure of Nepal" (4 marks). Learn the definition of each key term, the lists (three HDI dimensions, 17 SDGs, 3 tiers, 7 provinces, 753 local levels) and at least three named projects with place and purpose.
:::

## 2.1 Human Development Index

### Development and growth

**Economic growth** means an increase in a country's total output, usually measured by the **Gross Domestic Product (GDP)** or by income per person. **Development** is wider: it means a better life in health, education, income, safety, freedom and the environment. A country can grow richer while many of its people stay ill or unschooled, so growth alone does not prove development.

| Economic growth | Development |
|---|---|
| Narrow: a rise in income or output | Broad: better life in all respects |
| Measured by GDP or income per capita | Measured by HDI, poverty, health, schooling and more |
| A number that can be quickly counted | A process that includes quality of life |
| Can happen without benefiting everybody | Aims to benefit everybody |

### What is the Human Development Index?

::: definition Human Development Index (HDI)
The Human Development Index is a summary measure of the average achievement of a country in three basic dimensions of human development: a long and healthy life, knowledge, and a decent standard of living. It is published every year by the United Nations Development Programme (UNDP) in its *Human Development Report*.
:::

The idea that people, not only money, are the real wealth of a nation was put forward by the Pakistani economist **Mahbub ul Haq**, helped by the Indian economist **Amartya Sen**. The first *Human Development Report* appeared in **1990**. The HDI takes a value between **0 and 1**. The nearer to 1, the higher the development.

### The three dimensions and their indicators

| Dimension | What it shows | Indicator used |
|---|---|---|
| Health | A long and healthy life | Life expectancy at birth |
| Education | Knowledge | Mean years of schooling (adults aged 25+) and expected years of schooling (for children) |
| Standard of living | A decent income | Gross national income (GNI) per person, in purchasing power parity dollars |

Life expectancy at birth is the number of years a newborn would live if present death rates continued. Mean years of schooling is the average number of years of education adults have completed. Expected years of schooling is the number of years a child starting school today can expect to complete. GNI per capita in PPP dollars corrects for the fact that a rupee buys different amounts in different countries.

```figure caption="The three dimensions of the Human Development Index and the indicators that measure them. Each dimension is converted to an index from 0 to 1 and the three are combined into one HDI."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.0))
ax.set_xlim(0,10); ax.set_ylim(0,6.4); ax.axis('off')
cols=[(1.7,'Health','Life expectancy\nat birth'),(5.0,'Education','Mean years +\nexpected years\nof schooling'),(8.3,'Standard\nof living','GNI per capita\n(PPP dollars)')]
for x,t,s in cols:
    ax.add_patch(FancyBboxPatch((x-1.4,3.9),2.8,1.2,boxstyle='round,pad=0.05',fc=ACCENT,ec='none'))
    ax.text(x,4.5,t,ha='center',va='center',color='white',fontsize=9,weight='bold')
    ax.add_patch(FancyBboxPatch((x-1.4,1.9),2.8,1.4,boxstyle='round,pad=0.05',fc='white',ec=INK,lw=1))
    ax.text(x,2.6,s,ha='center',va='center',color=INK,fontsize=8)
    ax.annotate('',xy=(x,3.35),xytext=(x,3.85),arrowprops=dict(arrowstyle='<-',color=MUTED,lw=1.2))
    ax.annotate('',xy=(5,0.95),xytext=(x,1.85),arrowprops=dict(arrowstyle='->',color=MUTED,lw=1.2))
ax.add_patch(FancyBboxPatch((3.2,0.15),3.6,0.8,boxstyle='round,pad=0.05',fc='#e8f0f8',ec=ACCENT,lw=1.2))
ax.text(5,0.55,'HDI (0 to 1)',ha='center',va='center',fontsize=9,weight='bold',color=INK)
```

### How the index is calculated

For each dimension the UNDP fixes a minimum and a maximum, and converts the actual value into an index between 0 and 1:

$$ \text{Dimension index} = \frac{\text{actual value} - \text{minimum}}{\text{maximum} - \text{minimum}} $$

The fixed limits are: life expectancy 20 to 85 years; mean years of schooling 0 to 15; expected years of schooling 0 to 18; income 100 to 75,000 PPP dollars (income uses the logarithm of the value, because extra income matters less to a rich person). The education index is the average of the two schooling indices. Since 2010 the final HDI is the **geometric mean** of the three indices, which means that a low score in one dimension cannot be fully hidden by high scores in the others.

$$ \text{HDI} = \left(I_{\text{health}} \times I_{\text{education}} \times I_{\text{income}}\right)^{1/3} $$

::: example Worked example: HDI of an imaginary country
**Problem.** Country X has life expectancy 70 years, mean years of schooling 6, expected years of schooling 13.5 and GNI per capita of 5,000 PPP dollars. Find its HDI and say which group it belongs to.

**Solution.**
Health index = (70 − 20) / (85 − 20) = 50 / 65 = 0.769.
Mean schooling index = 6 / 15 = 0.400; expected schooling index = 13.5 / 18 = 0.750. Education index = (0.400 + 0.750) / 2 = 0.575.
Income index = (ln 5000 − ln 100) / (ln 75000 − ln 100) = ln 50 / ln 750 = 3.912 / 6.620 = 0.591.
HDI = (0.769 × 0.575 × 0.591)^(1/3) = (0.2613)^(1/3) = 0.639.
An HDI of 0.639 lies between 0.550 and 0.699, so Country X is in the **medium human development** group.
:::

::: note The SEE paper will not ask you to compute the HDI
The CDC textbook treats the HDI at the level of meaning, indicators, groups, Nepal's position and the ways of improving it. The worked example is here so that you understand *why* the index behaves as it does.
:::

### HDI groups

| Group | HDI value | Example |
|---|---|---|
| Very high human development | 0.800 and above | Norway, Switzerland, Japan, Australia |
| High human development | 0.700 to 0.799 | Sri Lanka, Thailand, China |
| Medium human development | 0.550 to 0.699 | Nepal, India, Bangladesh, Bhutan |
| Low human development | below 0.550 | Afghanistan, Mali, Niger and others |

### Nepal's human development

The *Human Development Report 2025* of the UNDP (which uses data for 2023) gave Nepal an HDI of **0.622**, ranking it **145th among 193 countries** and placing it in the medium human development group. The report said Nepal's HDI had risen by about **54%** between 1990 and 2023, from about 0.40 in 1990. Nepal's rise has been among the faster ones in South Asia, helped by longer life expectancy, more children in school and remittance income. Nepal still lags behind the very high human development countries, and inequality between provinces, between rural and urban areas and between social groups pulls the national average down.

```figure caption="HDI groups and Nepal's position. Nepal's HDI of 0.622 (UNDP Human Development Report 2025, 2023 data) lies in the medium band."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.2))
bands=[(0,0.55,'Low',SERIES[1]),(0.55,0.70,'Medium',SERIES[3]),(0.70,0.80,'High',SERIES[2]),(0.80,1.0,'Very high',ACCENT)]
for a,b,t,c in bands:
    ax.barh(0,b-a,left=a,height=0.5,color=c,alpha=0.85,edgecolor='white')
    ax.text((a+b)/2,0,t,ha='center',va='center',fontsize=8,color='white',weight='bold')
ax.plot([0.622,0.622],[0.3,0.62],color=INK,lw=1.5)
ax.text(0.622,0.68,'Nepal 0.622',ha='center',va='bottom',fontsize=8,color=INK)
ax.set_xlim(0,1); ax.set_ylim(-0.4,1.1)
ax.set_xticks([0,0.55,0.70,0.80,1.0]); ax.tick_params(axis='x',labelsize=8)
ax.set_yticks([]); ax.spines[['top','right','left']].set_visible(False)
ax.set_xlabel('Human Development Index',fontsize=8)
```

### Why a low HDI? Problems in Nepal

- Many people still depend on low-income farming and have limited access to quality health care in remote hills and mountains.
- Many adults, especially older women, have had little schooling; the quality of schools varies greatly.
- Employment at home is scarce, so millions of young people work abroad.
- Regional and social gaps: Karnali Province has the lowest HDI among the provinces and Bagmati the highest.
- Natural disasters such as the 2015 earthquake, floods and landslides destroy homes and schools.

### How can Nepal raise its HDI?

1. Make basic health services reach every ward and keep vaccination, safe delivery and nutrition programmes strong.
2. Make school education free, compulsory and of good quality; promote technical and vocational training.
3. Create jobs through agriculture, tourism, energy, small industries and cooperatives, so income rises at home.
4. Reduce poverty and inequality with targeted programmes for women, Dalits, the disabled and remote areas.
5. Build roads, electricity, drinking water and internet in the villages.
6. Prepare for disasters and protect the environment so that gains are not washed away.

```photo id="soc10/terraces" caption="Terraced farmland in the hills of Dailekh. A large share of Nepalis still live by farming small plots, so raising farm incomes is central to improving the standard-of-living part of the HDI." width="78"
```

::: caution HDI is an average
An HDI value hides differences inside a country. Two provinces, or a boy and a girl, may have very different life chances although the national HDI is the same. HDI also does not measure freedom, safety or the environment. That is why other indices, such as the Gender Development Index and the Multidimensional Poverty Index, are used alongside it.
:::

## 2.2 Sustainable development

### Meaning

A farmer who eats all his seed this year has nothing to plant next year. A country that cuts all its forests, empties its rivers and pollutes its air is doing the same on a bigger scale. **Sustainable development** is development that does not eat the seed.

::: definition Sustainable development
Sustainable development is development that meets the needs of the present generation without reducing the ability of future generations to meet their own needs. (Brundtland Commission, *Our Common Future*, 1987)
:::

### The three pillars

| Pillar | Idea | Nepali example |
|---|---|---|
| Economic | Steady growth, jobs and fair income that can be kept up | Hydropower and tourism that give income for decades |
| Social | Equality, inclusion, education, health, safety for everyone | Girls' scholarships, free basic health, reservation for the disadvantaged |
| Environmental | Using natural resources within their capacity to renew | Community forests, clean energy, waste management, river protection |

Sustainable development exists only where all three overlap. A project that makes money but poisons a river is not sustainable; neither is one that saves a forest while leaving the villagers hungry.

### Milestones on the road to sustainable development

| Year | Event |
|---|---|
| 1972 | UN Conference on the Human Environment, Stockholm; 5 June becomes World Environment Day |
| 1987 | *Our Common Future* (Brundtland Report) defines sustainable development |
| 1992 | Earth Summit, Rio de Janeiro: Agenda 21 and the climate and biodiversity conventions |
| 2000 | Millennium Development Goals (MDGs): eight goals to be met by 2015 |
| 2015 | UN General Assembly adopts the 2030 Agenda with **17 Sustainable Development Goals (SDGs)** and 169 targets; the Paris Agreement on climate is adopted the same year |

### The 17 Sustainable Development Goals

| No. | Goal | No. | Goal |
|---|---|---|---|
| 1 | No poverty | 10 | Reduced inequalities |
| 2 | Zero hunger | 11 | Sustainable cities and communities |
| 3 | Good health and well-being | 12 | Responsible consumption and production |
| 4 | Quality education | 13 | Climate action |
| 5 | Gender equality | 14 | Life below water |
| 6 | Clean water and sanitation | 15 | Life on land |
| 7 | Affordable and clean energy | 16 | Peace, justice and strong institutions |
| 8 | Decent work and economic growth | 17 | Partnerships for the goals |
| 9 | Industry, innovation and infrastructure | | |

::: memory Group the 17 goals
**People** — 1 to 5 (poverty, hunger, health, education, gender). **Prosperity and planet** — 6 to 15 (water, energy, work, industry, inequality, cities, consumption, climate, water life, land life). **Peace and partnership** — 16 and 17.
:::

### Nepal and the SDGs

Nepal has accepted the SDGs and its National Planning Commission has linked the periodic plans with them. The government has published a status and roadmap for the goals and has tried to take them to the provinces and local levels. Nepal has done well in some areas — for example, access to electricity and to drinking water has expanded and many more children attend school — but gaps remain in nutrition, quality of education, jobs and the protection of the environment. The country is also due to graduate from the group of **Least Developed Countries (LDCs)** in November 2026, a sign of progress that must now be made lasting.

### Ways of achieving sustainable development in Nepal

1. **Protect forests.** Community forestry, in which local forest user groups manage the forest, is a world-famous Nepali method. More than 22,000 groups manage forests across the country, and forest cover is about 45% of the land.
2. **Use clean energy.** Hydropower, solar, biogas and electric transport lower the need for firewood and imported fuel.
3. **Promote organic and climate-friendly farming** and protect soil and water.
4. **Manage waste** by reducing, reusing and recycling, and treating sewage and solid waste.
5. **Control population and plan settlements** so that farmland and forests are not lost to unplanned building.
6. **Prepare for climate change.** Himalayan glaciers are melting faster as the world warms; glacial lake outburst floods, drought and flood are a threat to farms and villages.
7. **Educate people** so that every citizen understands that water, soil and air are shared wealth.
8. **Make strong rules and follow them:** environmental impact assessment before big projects, fair rules for mining and building.

### Threats to sustainable development

- Deforestation, soil erosion and landslides
- Air pollution in the Kathmandu Valley and Terai towns, and polluted rivers
- Unplanned urbanisation and the loss of farmland
- Climate change and natural disasters
- Poverty, which forces people to over-use forests and land
- Weak enforcement of environmental laws

::: tip Four-mark answer pattern
"Explain the importance of sustainable development" — (1) conserves natural resources for future generations; (2) protects the environment; (3) reduces poverty with lasting jobs; (4) brings social justice and peace. Add one Nepali example.
:::

## 2.3 Federalism in Nepal

### What is federalism?

::: definition Federalism
Federalism is a system of government in which power is divided by the constitution between a central (federal) government and units such as provinces, and each level has its own powers to make laws and decisions in its own area.
:::

In a **unitary** system power rests with the centre, and lower units get only what the centre gives. In a **federal** system the constitution itself gives powers to each level, so the centre cannot take them away.

| Unitary system | Federal system |
|---|---|
| All power with one central government | Power divided among federal, provincial and local governments |
| Lower units depend on the centre | Each level has its own constitutional powers |
| Decisions made far from the people | Decisions closer to the people |
| Nepal until 2015 | Nepal since 2015 |

### How Nepal became federal

- For about two centuries after the unification, Nepal was governed from Kathmandu as a unitary state.
- Many groups, especially in Madhesh, among indigenous peoples and in remote areas, felt left out of power. The Madhesh movement of 2007 (2063/64 BS) and the demands of the Janajati groups made federalism a national demand.
- The **Interim Constitution of 2063** (2007) opened the way, and the first Constituent Assembly declared Nepal a **federal democratic republic** on **15 Jestha 2065 (28 May 2008)**.
- The second Constituent Assembly adopted the new constitution, which was promulgated on **3 Ashwin 2072 (20 September 2015)**. It sets up a three-tier federal system.
- The first elections to the three tiers under the new constitution were held in 2074 BS (2017). Local elections were held again in 2079 (May 2022).

### The three tiers

```figure caption="The three tiers of government in Nepal. Article 232 of the Constitution says that their relations rest on cooperation, coexistence and coordination."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.3))
ax.set_xlim(0,10); ax.set_ylim(0,7.6); ax.axis('off')
tiers=[(5.0,'Federal government','Federal Parliament, President, Prime Minister,\nCouncil of Ministers, Supreme Court',ACCENT),(2.75,'7 Provincial governments','Provincial Assembly, Governor, Chief Minister,\nCouncil of Ministers, High Court','#2e6da4'),(0.5,'753 Local governments','Municipal or Rural Municipal Assembly,\nMayor or Chair, ward committees','#4f8bbf')]
for y,t,s,c in tiers:
    ax.add_patch(FancyBboxPatch((0.3,y),9.4,1.8,boxstyle='round,pad=0.04',fc=c,ec='none'))
    ax.text(5,y+1.3,t,ha='center',va='center',color='white',fontsize=10,weight='bold')
    ax.text(5,y+0.62,s,ha='center',va='center',color='white',fontsize=7.5)
ax.text(5,7.3,'Constitution of Nepal (2015)',ha='center',va='center',fontsize=9,color=INK,weight='bold')
```

#### Federal level

The federal government at Kathmandu handles matters of national concern: defence, foreign affairs, currency and monetary policy, citizenship, federal police and security, large national projects, customs, national planning and inter-province matters. Its powers are listed in **Schedule 5** of the Constitution.

#### Provincial level

Nepal has **seven provinces**, formed by grouping districts. Each has an elected Provincial Assembly, a Chief Minister and Council of Ministers, and a **Governor** (*Pradesh Pramukh*) appointed by the President as the federal representative. The powers are in **Schedule 6**: provincial police, provincial roads and transport, health and education beyond the basic level, provincial electricity and irrigation, agriculture and cooperatives, provincial planning, and similar.

| Province | Capital | Population (Census 2021) |
|---|---|---|
| Koshi | Biratnagar | 4,972,021 |
| Madhesh | Janakpur | 6,126,288 |
| Bagmati | Hetauda | 6,084,042 |
| Gandaki | Pokhara | 2,479,745 |
| Lumbini | Deukhuri (Bhalubang) | 5,124,225 |
| Karnali | Birendranagar (Surkhet) | 1,694,889 |
| Sudurpashchim | Godawari (Kailali) | 2,711,270 |

```photo id="soc10/provinces" caption="The seven provinces of Nepal. The provinces group the 77 districts; each province's assembly chose its name and capital." width="92"
label 0.13 0.68 "Sudurpashchim"
label 0.29 0.60 "Karnali"
label 0.37 0.31 "Lumbini"
label 0.52 0.52 "Gandaki"
label 0.67 0.38 "Bagmati"
call 0.58 0.08 0.62 0.21 "Madhesh"
label 0.85 0.27 "Koshi"
```

```figure caption="Population of the seven provinces, Census 2021 (millions). Madhesh and Bagmati have the most people; Karnali, the largest province by area, has the fewest."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
names=['Madhesh','Bagmati','Lumbini','Koshi','Sudurpashchim','Gandaki','Karnali']
vals=[6.126,6.084,5.124,4.972,2.711,2.480,1.695]
y=list(range(len(names)))[::-1]
ax.barh(y,vals,color=ACCENT,height=0.62)
for yy,v in zip(y,vals):
    ax.text(v+0.08,yy,f'{v:.2f}',va='center',fontsize=8,color=INK)
ax.set_yticks(y); ax.set_yticklabels(names,fontsize=8)
ax.set_xlim(0,7.2); ax.set_xlabel('Population (millions)',fontsize=8)
ax.spines[['top','right']].set_visible(False); ax.tick_params(axis='x',labelsize=8)
```

#### Local level

There are **753 local levels**: 6 metropolitan cities, 11 sub-metropolitan cities, 276 municipalities and 460 rural municipalities, with 6,743 wards in all. The local level is the government closest to the people and the one a citizen meets first, for birth and marriage registration, recommendation letters, local roads, drinking water and basic schools. Its powers are in **Schedule 8**. There are also powers shared by federal, province and local levels (Schedule 9) and by federal and province (Schedule 7).

| Level | Number | Head | Law-making body |
|---|---|---|---|
| Federal | 1 | Prime Minister (executive), President (head of state) | Federal Parliament |
| Province | 7 | Chief Minister (executive), Governor (federal representative) | Provincial Assembly |
| Local | 753 | Mayor/Deputy Mayor or Chair/Vice-chair | Municipal or Rural Municipal Assembly |

### Why federalism?

1. **Brings government close to the people**: decisions on local roads, schools and clinics are made in the locality.
2. **Gives power and recognition to all** regions, languages, and communities, which promotes inclusion.
3. **Speeds development** because each level plans and spends according to need.
4. **Strengthens democracy** with thousands of elected representatives and with women and Dalit members guaranteed in each ward.
5. **Reduces the sense of neglect** that earlier fed conflict, and so protects national unity.

### Challenges of federalism

- Lack of enough trained staff and laws at the provincial and local levels.
- Dependence on money from the centre, since provinces and local levels raise limited revenue of their own.
- Unclear division of work and overlaps between levels.
- High cost of running three tiers of government.
- Unequal capacity between urban and rural local units.

### Federal powers, provincial powers, local powers — who does what?

| Task | Level |
|---|---|
| Army, foreign affairs, currency, citizenship | Federal |
| Provincial police, provincial highways, higher health services | Province |
| Basic education, basic health, local roads, drinking water, market, birth and death registration | Local |
| Forests, water resources, national parks, health, education, social security | Shared (concurrent) powers |

```photo id="soc10/singha-durbar" caption="Singha Durbar, Kathmandu, the seat of the Government of Nepal's secretariat. Federalism means that the powers once held only here are now shared with seven provincial and 753 local governments." width="78"
```

::: tip Do not mix up
Federal democratic republic = **three** tiers (federal, province, local), not two. The 77 districts still exist as administrative units, with a District Coordination Committee that coordinates between local levels and the province, but they are not a separate government tier.
:::

## 2.4 National pride projects

### Meaning

Some projects are so big and so important that they can change the economy of the whole country. A nation cannot build a long highway, a huge dam or an international airport as a small local scheme; it needs a long plan, strong management and large money. Nepal calls such projects **National Pride Projects** (*Rastriya Gaurav ka Aayojana*).

::: definition National pride projects
National pride projects are large, strategic development projects selected by the Government of Nepal, with a very large investment, that are expected to bring major change in the economy and in the lives of the people and so bring pride to the nation.
:::

The National Planning Commission has prepared the criteria and the government has selected the list, which has been revised from time to time. The projects are chosen because they are expected to change the country's economy and the lives of many people, because they need heavy investment and long construction, and because they link regions or use Nepal's natural strength such as water and geography.

### Objectives and importance

1. **Economic growth** — create employment during construction and later through industry, trade and tourism.
2. **Energy security** — produce electricity for homes and industry, and export the surplus.
3. **Better transport and trade** — roads, railways and airports connect hills, Terai and the Himalaya with each other and with the world.
4. **Water for drinking and irrigation** — secure drinking water for cities and irrigation for farms.
5. **Balanced development** — carry growth to backward regions.
6. **Reduced dependence** on imports and raised self-reliance.
7. **National unity and pride** — a feeling that Nepalis can build great things.

### Some national pride projects

| Project | Type | Main purpose and facts |
|---|---|---|
| Melamchi Water Supply Project | Drinking water | Brings water from the Melamchi River (Sindhupalchok) through a tunnel of about 26.5 km to the Kathmandu Valley; the first phase (about 170 million litres a day) reached Kathmandu in 2021 |
| Upper Tamakoshi Hydropower Project | Energy | 456 MW run-of-river plant in Dolakha, in full operation since 2021; largely financed from within Nepal, including shares sold to the public |
| Budhi Gandaki Hydropower Project | Energy | A planned storage project of about 1,200 MW on the Budhi Gandaki River, between Gorkha and Dhading |
| Kathmandu–Terai (Madhesh) Expressway (Fast Track) | Transport | A planned expressway of about 72 km that will shorten the road from Kathmandu to the Terai |
| Pokhara Regional International Airport | Aviation | Opened on 1 January 2023; meant to bring tourists and migrant workers directly to Pokhara and the Gandaki region |
| Gautam Buddha International Airport, Bhairahawa | Aviation | Opened for international services in 2022 to serve pilgrims to Lumbini |
| Mid-Hill (Pushpalal) Highway | Transport | An east-west highway of about 1,776 km through the mid-hills from Panchthar to Baitadi |
| Postal (Hulaki) Highway | Transport | A road of about 1,790 km in the Terai, linking small towns along the plains |
| Bheri-Babai Diversion Multipurpose Project | Irrigation, energy | Tunnel that diverts water from the Bheri River to the Babai River basin to irrigate dry lands in Bardiya |

*(Figures are approximate and may change as projects are completed. Check the latest government list.)*

```photo id="soc10/melamchi" caption="Melamchi Water Supply Project, near the headworks in Sindhupalchok. The project takes water from the Melamchi River across the ridge by tunnel to Kathmandu, a city that has faced chronic water shortage." width="80"
```

```photo id="soc10/utk-tunnel" caption="A road tunnel to the dam site of the Upper Tamakoshi Hydropower Project, Dolakha. At 456 MW, it is one of the biggest power plants in Nepal and a national pride project." width="80"
```

### Problems of national pride projects

- **Delays and cost increases**: many projects take far longer than planned.
- **Funding**: large loans or aid are needed, and repayment becomes a burden.
- **Weak project management**, contractor problems and corruption.
- **Land acquisition** and the resettlement of affected families.
- **Environmental and social impact**: forest loss, effects on rivers and communities.
- **Natural hazards**: the Melamchi works were damaged by a flood in June 2021.

### How to make them succeed

1. Plan carefully, with proper surveys and environmental assessment before starting.
2. Provide the money on time and manage it honestly.
3. Appoint capable project managers and monitor progress openly.
4. Compensate and rehabilitate families affected by land acquisition.
5. Involve local people and protect the environment.
6. Keep the project away from party politics so that a change of government does not stop it.

::: caution Do not confuse pride projects with local projects
Neither a village irrigation canal nor a school building is a national pride project, however useful. The test is *scale, national importance and strategic effect on the economy*.
:::

## Chapter summary

- **Development** is better life in health, education, income and freedom; economic growth is only a part of it.
- **HDI** (UNDP, since 1990) combines **health** (life expectancy), **education** (mean and expected years of schooling) and **standard of living** (GNI per capita, PPP) into a value from 0 to 1; groups: very high (0.800+), high (0.700–0.799), medium (0.550–0.699), low (below 0.550).
- **Nepal's HDI** is 0.622 and rank 145 (Human Development Report 2025, 2023 data): medium group.
- **Sustainable development** meets present needs without harming the future (Brundtland, 1987); it rests on economic, social and environmental pillars. The **17 SDGs** (169 targets) were adopted in 2015 for 2030.
- **Federalism** divides power among federal, provincial and local governments; Nepal was declared a federal democratic republic on 15 Jestha 2065 and the Constitution was promulgated on 3 Ashwin 2072.
- Nepal has **7 provinces** and **753 local levels** (6 metropolitan, 11 sub-metropolitan, 276 municipalities, 460 rural municipalities) and 77 districts.
- **National pride projects** are very large strategic projects, such as Melamchi, Upper Tamakoshi, Budhi Gandaki, the Fast Track, new international airports and the highways, meant to speed up growth and bring national pride.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The Human Development Index is published by <span class="marks">[1]</span>
   (a) World Bank (b) UNDP (c) WHO (d) IMF
2. Which one is NOT a dimension of the HDI? <span class="marks">[1]</span>
   (a) health (b) education (c) standard of living (d) political stability
3. The 2030 Agenda adopted in 2015 has how many Sustainable Development Goals? <span class="marks">[1]</span>
   (a) 8 (b) 12 (c) 17 (d) 21
4. How many local levels does Nepal have? <span class="marks">[1]</span>
   (a) 77 (b) 460 (c) 753 (d) 6,743
5. The Constitution of Nepal was promulgated on <span class="marks">[1]</span>
   (a) 15 Jestha 2065 (b) 3 Ashwin 2072 (c) 7 Falgun 2007 (d) 15 Jestha 2063
6. The capital of Madhesh Province is <span class="marks">[1]</span>
   (a) Hetauda (b) Biratnagar (c) Janakpur (d) Pokhara
7. Who defined sustainable development in 1987 in the report *Our Common Future*? <span class="marks">[1]</span>
   (a) Brundtland Commission (b) UNICEF (c) SAARC (d) Earth Summit
8. The Upper Tamakoshi Hydropower Project has a capacity of <span class="marks">[1]</span>
   (a) 45.6 MW (b) 456 MW (c) 1,200 MW (d) 900 MW

::: note Answers to Group A
**1.** (b) — the UNDP publishes the Human Development Report with the HDI.
**2.** (d) — the three dimensions are health, education and standard of living.
**3.** (c) — 17 SDGs with 169 targets.
**4.** (c) — 753 local levels (460 is the number of rural municipalities).
**5.** (b) — 3 Ashwin 2072 (20 September 2015).
**6.** (c) — Janakpur is the capital of Madhesh Province.
**7.** (a) — the Brundtland Commission gave the definition.
**8.** (b) — 456 MW.
:::

**Group B — Short answer (2 marks each)**

1. What is the Human Development Index? Write its three indicators. <span class="marks">[2]</span>
2. Define sustainable development. <span class="marks">[2]</span>
3. What is federalism? Name the three tiers of government in Nepal. <span class="marks">[2]</span>
4. Write any four of the 17 Sustainable Development Goals. <span class="marks">[2]</span>
5. What are national pride projects? Give two examples. <span class="marks">[2]</span>
6. Differentiate between economic growth and development (two points). <span class="marks">[2]</span>

::: note Answers to Group B
**1.** The HDI is a measure of the average achievement of a country in health, education and standard of living, published by UNDP. Indicators: life expectancy at birth, years of schooling (mean and expected), and GNI per capita.
**2.** Development that meets the needs of the present generation without harming the ability of future generations to meet their needs.
**3.** Federalism is a system in which the constitution divides power between the federal government and units such as provinces. Tiers: federal, province and local.
**4.** No poverty; zero hunger; good health and well-being; quality education; gender equality; clean water and sanitation; climate action (any four).
**5.** Very large strategic projects selected by the government to bring big change to the economy. Examples: Melamchi Water Supply Project, Upper Tamakoshi Hydropower Project.
**6.** Growth is only an increase in income or output; development is a wider improvement in quality of life. Growth is measured by GDP, development by HDI and other indicators.
:::

**Group C — Long answer (4 marks each)**

1. A country has life expectancy of 75 years. Find its health index using minimum 20 and maximum 85 years. If its education index is 0.656 and income index is 0.662, find its HDI to two decimal places. <span class="marks">[4]</span>
2. Explain how sustainable development can be achieved in Nepal. <span class="marks">[4]</span>
3. Describe the federal structure of Nepal and mention any two benefits of federalism. <span class="marks">[4]</span>
4. Explain the importance and the problems of national pride projects. <span class="marks">[4]</span>
5. What is HDI? How can Nepal improve its human development? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Health index = (75 − 20)/(85 − 20) = 55/65 = 0.846. HDI = (0.846 × 0.656 × 0.662)^(1/3) = (0.3674)^(1/3) = 0.716, so HDI ≈ 0.72, in the high human development group.
**2.** Protect forests through community forestry; use clean energy; follow environment-friendly farming; manage waste; plan settlements; prepare for climate change; educate people; enforce environmental laws (any four, with a reason each).
**3.** Three tiers: federal (Parliament, President, Prime Minister), seven provinces (assembly, governor, chief minister) and 753 local levels (municipalities and rural municipalities), each with powers listed in the schedules. Benefits: government closer to the people; inclusion of all communities; faster, need-based development.
**4.** Importance: economic growth and jobs; energy and water; transport; balanced development; national pride. Problems: delays and cost overruns; funding; weak management and corruption; land acquisition; environmental impact.
**5.** HDI is a measure of health, education and standard of living (explain). Improvement: health services in every ward; free, quality education; jobs and income at home; reducing poverty and inequality; roads, electricity and water in villages; disaster preparedness.
:::

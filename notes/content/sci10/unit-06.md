---
subject: Science and Technology
grade: 10
unit: 6
title: Nature and Environment
hours: 0
area: Science and Technology
---

Everything around you, the air, water, soil, plants, animals and other people, makes up your environment. Nepal is one of the most varied small countries in the world: from the hot plains of the terai, where the rhino lives, to the cold peaks of the Himalaya, where the snow leopard lives. But the same environment now faces pollution, climate change and growing piles of waste. In this unit you learn how living things and their surroundings work together as an ecosystem, how human activity damages the environment, and what we can do to protect it.

::: key What the SEE paper expects from this unit
Common questions: define ecosystem, food chain, food web (1–2 marks); draw a food chain or pyramid; causes, effects and control of air, water and soil pollution (4 marks); greenhouse effect, global warming and ozone depletion (2 or 4 marks); the 3 Rs and waste segregation (2 marks); national parks and conservation in Nepal (2 marks).
:::

## 6.1 Ecosystem

::: definition Ecosystem
An **ecosystem** is a community of living organisms (plants, animals, microbes) interacting with each other and with the non-living things (air, water, soil, light, temperature) of the place where they live.
:::

The study of the relationship between living things and their surroundings is **ecology**. A pond, a forest, a grassland, a farm or even a school garden is an ecosystem.

### Components of an ecosystem

| Component | Meaning | Examples |
|---|---|---|
| **Abiotic** (non-living) | Physical and chemical factors | Sunlight, temperature, water, air, soil, minerals |
| **Biotic** (living) | All living things | Producers, consumers, decomposers |

The biotic part is arranged by how each organism gets its food:

- **Producers** (autotrophs) make their own food by photosynthesis: green plants, algae, phytoplankton.
- **Consumers** (heterotrophs) eat other organisms.
  - **Primary consumers** (herbivores) eat plants: deer, cow, grasshopper.
  - **Secondary consumers** (carnivores) eat herbivores: frog, snake eating mice, small birds.
  - **Tertiary consumers** (top carnivores) eat other carnivores: tiger, eagle, hawk.
  - **Omnivores** eat both plants and animals: human, bear, crow.
- **Decomposers** (bacteria and fungi) break down dead plants and animals and return minerals to the soil. They are nature's recyclers.

### Types of ecosystem

| Natural ecosystems | Artificial (man-made) ecosystems |
|---|---|
| Terrestrial (on land): forest, grassland, desert, mountain | Crop fields, orchards |
| Aquatic: pond, lake, river, wetland, ocean | Aquarium, fish farm, garden |

### Food chain

::: definition Food chain
A **food chain** is the sequence of living things in which each one is eaten by the next, so that food energy passes from one organism to another.
:::

Examples (the arrow means "is eaten by"):

- Grass → grasshopper → frog → snake → eagle
- Phytoplankton → zooplankton → small fish → big fish → fish-eating bird (pond)
- Rice plant → rat → snake → hawk (field)

Each step in the chain is a **trophic level**: first level = producers, second = primary consumers, third = secondary consumers, fourth = tertiary consumers.

### Food web

Organisms usually eat more than one thing and are eaten by more than one kind of animal, so several food chains join to form a **food web**. A food web is more stable than a single chain: if one food source is lost, the animal can switch to another.

```figure caption="A simple food web of a grassland. Arrows point from the organism that is eaten to the organism that eats it."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.4))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,9)
def bx(x,y,t,fc,w=2.6):
    ax.add_patch(FancyBboxPatch((x-w/2,y-0.38),w,0.76,boxstyle="round,pad=0.04",fc=fc,ec=INK,lw=0.9))
    ax.text(x,y,t,ha='center',va='center',fontsize=7.8,color=INK)
def ar(x1,y1,x2,y2):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color=INK,lw=1))
bx(6,0.8,"Grass (producer)","#c8e6c0",w=3.4)
bx(2.2,3.2,"Grasshopper","#fff3c9"); bx(6,3.2,"Mouse","#fff3c9"); bx(9.8,3.2,"Deer","#fff3c9")
bx(2.2,5.6,"Frog","#ffd9c7"); bx(6.6,5.6,"Snake","#ffd9c7")
bx(4.2,8.2,"Eagle","#f3b8b8"); bx(9.8,6.0,"Tiger","#f3b8b8")
ar(5,1.2,2.6,2.8); ar(6,1.2,6,2.8); ar(7,1.2,9.4,2.8)
ar(2.2,3.6,2.2,5.2); ar(2.9,3.6,5.9,5.2); ar(6.2,3.6,6.4,5.2)
ar(2.9,6.0,3.6,7.8); ar(6.2,6.0,4.8,7.8)
ar(9.8,3.6,9.8,5.6); ar(4.0,0.0,4.0,0.0)
ax.text(0.1,0.1,"Decomposers act on the dead remains of all of these",fontsize=7,color=MUTED)
```

### Ecological pyramid and energy flow

Energy flows in **one direction** through an ecosystem: from the **sun** to producers, and then to consumers. At every step only about **10%** of the energy passes to the next trophic level (the **10% law**); the rest is used for life processes or lost as heat. So there are fewer organisms at higher levels and a food chain rarely has more than four or five steps. A diagram of this is an **ecological pyramid**: a wide base of producers and a narrow top.

::: example Worked example 6.1 (10% law)
**Problem.** Grass in a field receives and stores 20,000 kJ of energy. How much energy is available to (a) the grasshopper, (b) the frog, and (c) the snake in the chain Grass → grasshopper → frog → snake?

**Solution.** At each step 10% of the energy is passed on.

(a) Grasshopper = 10% of 20,000 = **2,000 kJ**.

(b) Frog = 10% of 2,000 = **200 kJ**.

(c) Snake = 10% of 200 = **20 kJ**.

So the snake gets only 0.1% of the energy stored by the grass. This is why a field can feed many more grass-eaters than snakes.
:::

```figure caption="Pyramid of energy for the chain grass, grasshopper, frog, snake (values in kJ). Each higher level has only 10 percent of the level below."
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.4,2.8))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,8)
lv=[("Grass (producer)","20,000 kJ","#c8e6c0"),("Grasshopper (primary)","2,000 kJ","#fff3c9"),("Frog (secondary)","200 kJ","#ffd9c7"),("Snake (tertiary)","20 kJ","#f3b8b8")]
for i,(n,e,c) in enumerate(lv):
    y0=i*1.9; w=10.4-i*1.9
    ax.add_patch(Polygon([(6-w/2,y0),(6+w/2,y0),(6+w/2-1.0,y0+1.7),(6-w/2+1.0,y0+1.7)],fc=c,ec=INK,lw=0.9))
    ax.text(6,y0+0.85,n+"  "+e,ha='center',va='center',fontsize=7,color=INK)
ax.annotate("",xy=(11.6,7.4),xytext=(11.6,0.3),arrowprops=dict(arrowstyle="->",color=MUTED))
ax.text(11.5,3.8,"energy\ndecreases",fontsize=7,color=MUTED,ha='right',va='center',rotation=90)
```

### Biogeochemical cycles

Matter, unlike energy, is **recycled**. The main cycles are the **water cycle**, **carbon cycle** and **nitrogen cycle**.

- **Carbon cycle.** Plants take carbon dioxide from the air to make food (photosynthesis). Animals eat the plants. Respiration, decay and burning of fuels return CO₂ to the air.
- **Nitrogen cycle.** Air is 78% nitrogen, but plants cannot use it directly. Bacteria (*Rhizobium* in the root nodules of legumes such as peas and beans; and some free soil bacteria) change it to nitrates that plants take up. Animals eat plants; decomposers return nitrogen to the soil; denitrifying bacteria return some to the air.
- **Water cycle.** Water evaporates from oceans and plants, forms clouds, falls as rain or snow and flows back by rivers.

### Ecosystems of Nepal

Nepal has three ecological belts: the **terai** (below 1,000 m: sal forest, grasslands; rhino, tiger, gharial), the **hills** (1,000–3,000 m: subtropical and temperate forests of rhododendron and oak; red panda, Himalayan black bear) and the **Himalaya** (above 3,000 m: alpine meadows and snow; snow leopard, musk deer, Himalayan monal). Nepal is rich in biodiversity: about 118 ecosystems, over 6,500 species of flowering plants and about 880 species of birds in a country that covers only 0.1% of the world's land.

## 6.2 Environmental pollution

::: definition Pollution
**Pollution** is the addition of harmful substances (pollutants) to air, water or soil, or the presence of harmful energy such as noise, so that the environment becomes unfit for living things.
:::

A **pollutant** is any substance that causes pollution. Pollution may come from **natural** causes (volcano, forest fire, dust storm) or from **human** activities, which are the bigger cause.

### Air pollution

**Air pollution** is the presence of harmful gases, smoke and dust in the air.

```photo id="sci10/air-kathmandu" caption="Air pollution in Kathmandu: smoke and dust hang over the city and cut down the view." width="76"
```

| Pollutant | Source | Harm |
|---|---|---|
| Carbon monoxide (CO) | Incomplete burning of fuel, vehicle exhaust, cooking on firewood | Binds haemoglobin, so less oxygen reaches the body; causes headache and even death |
| Carbon dioxide (CO₂) | Burning fuel, forest fires | Global warming |
| Sulphur dioxide (SO₂) | Burning coal, brick kilns, factories | Lung disease, acid rain |
| Oxides of nitrogen (NOₓ) | Vehicle engines | Smog, acid rain, breathing disease |
| Particulate matter (PM₁₀, PM₂.₅) | Dust, smoke, construction, brick kilns | Asthma, lung and heart disease |
| CFCs | Old refrigerators, aerosol sprays | Destroy the ozone layer |
| Smoke from burning waste and crop residue | Open burning | Respiratory disease |

**Causes in Nepal.** Old and unmaintained vehicles, dust from roads and construction, brick kilns in the Kathmandu valley, burning of plastic and wastes, forest fires, and smoke from firewood and kerosene in homes (**indoor air pollution**). In winter, the bowl shape of the Kathmandu valley traps the pollution.

**Effects.** Asthma, bronchitis, eye problems, lung cancer, heart disease, damage to crops and buildings, acid rain, smog, global warming.

**Control.** Use of electric and well-maintained vehicles; public transport; clean cookstoves, LPG, biogas and solar energy instead of firewood; tree planting; filters in chimneys; stopping the burning of waste; regular testing of vehicle emissions; and the use of CFC-free appliances.

### Acid rain

When SO₂ and NOₓ from fuel burning dissolve in rain water, they form sulphuric acid and nitric acid, and the rain becomes acidic (pH below 5.6). **Acid rain** damages forests, kills fish in lakes, harms crops and eats away marble and metal (it is damaging the Taj Mahal in India).

```text
SO₂ + H₂O → H₂SO₃ (then oxidised to H₂SO₄)
```

### Water pollution

**Water pollution** is the addition of harmful substances to water so that it becomes unfit for use.

```photo id="sci10/bagmati-waste" caption="Solid waste dumped on the bank of the Bagmati river near Kathmandu. Garbage like this pollutes the river water." width="76"
```

| Source | Pollutant |
|---|---|
| Households | Sewage, soaps, detergents, kitchen waste |
| Industry | Chemicals, dyes, oil, heavy metals (lead, mercury) |
| Agriculture | Fertilisers, pesticides |
| Dumping | Plastic, garbage, dead bodies thrown in rivers |
| Oil spills | Oil from ships and vehicles |

**Effects.** Water-borne diseases such as **cholera, typhoid, dysentery, diarrhoea and jaundice**; death of fish and other water life; bad smell; harm to crops; loss of drinking water.

**Eutrophication.** Fertilisers and detergents rich in nitrates and phosphates that run into ponds and lakes make algae grow explosively (**algal bloom**). When the algae die, bacteria use up the oxygen of the water in decomposing them, and fish die for want of oxygen.

**Control.** Treat sewage before releasing; never dump garbage in rivers; reduce fertiliser and pesticide use; use compost; boil, filter or chlorinate drinking water; and keep the river banks clean. The Bagmati river is an example of a river in the Kathmandu valley badly affected by waste, which people's campaigns are trying to clean.

### Soil pollution

Soil pollution is the addition of harmful substances to the soil. **Causes:** plastic and other garbage, chemical fertilisers and pesticides, industrial wastes, and mining. **Effects:** loss of soil fertility, harm to soil organisms such as earthworms, poisoning of crops and groundwater, and spread of diseases. **Control:** use organic manure and compost, reduce plastic, practise integrated pest management, sort and recycle waste, and plant trees to stop erosion.

```photo id="sci10/plastic-waste" caption="Plastic waste choking a roadside drain. Plastic does not rot, so it stays in the soil and blocks water." width="70"
```

### Noise pollution

**Noise** is unwanted loud sound. Loudness is measured in **decibels (dB)**: whisper 30 dB, normal talk 60 dB, heavy traffic 80–90 dB, loud horn or loudspeaker 100–110 dB, aeroplane engine 120–140 dB. Continuous noise above about 85 dB can damage hearing. **Sources:** vehicles' horns, loudspeakers, factories, construction, aircraft. **Effects:** hearing loss, headache, stress, high blood pressure, poor sleep and poor study. **Control:** limit horns and loudspeakers, plant trees, use sound-absorbing walls, and keep factories and airports away from homes.

### Radioactive and light pollution

Radiation from nuclear accidents and wastes can cause cancer and harm genes. Excess artificial light at night harms sleep and confuses the animals that move at night.

::: caution Common mistake
Do not mix up **ozone depletion** and **global warming**. Ozone depletion lets more ultraviolet rays reach the Earth (caused by CFCs). Global warming is the rise of the Earth's temperature due to greenhouse gases like CO₂ and methane. They are different problems with different causes.
:::

## 6.3 Climate change

**Weather** is the state of the atmosphere at a place on a given day. **Climate** is the average weather of a place over a long time (30 years or more). **Climate change** is a long-term change in the Earth's climate, mostly the rise in temperature caused by human activity since about 1850.

### Greenhouse effect

Some gases in the air, called **greenhouse gases**, let the sun's light in but trap the heat that the Earth sends back, like the glass of a greenhouse. This natural **greenhouse effect** keeps the Earth warm: without it the average temperature of the Earth would be about −18 °C instead of about +15 °C, and life would not be possible.

The main greenhouse gases are:

| Gas | Main source |
|---|---|
| Carbon dioxide (CO₂) | Burning of coal, oil and gas; deforestation |
| Methane (CH₄) | Rice fields, cattle, landfills, biogas leaks |
| Nitrous oxide (N₂O) | Fertilisers, burning of fuel |
| CFCs | Refrigerators, air conditioners |
| Water vapour | Evaporation (natural) |

```figure caption="The greenhouse effect (schematic). Sunlight passes through the atmosphere; some heat from the Earth is trapped by greenhouse gases and sent back to the surface."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.6,3.2))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,8.5)
ax.add_patch(Rectangle((0,0),12,1.6,fc="#8fcf7a",ec=INK,lw=1))
ax.text(6,0.8,"Earth's surface",ha='center',va='center',fontsize=8,color=INK)
ax.add_patch(Rectangle((0,4.6),12,1.6,fc="#dbe8ff",ec=ACCENT,lw=1,alpha=0.8))
ax.text(6,5.4,"Greenhouse gases (CO2, CH4, N2O)",ha='center',va='center',fontsize=8,color=INK)
ax.annotate("",xy=(2.2,1.7),xytext=(1.0,8.2),arrowprops=dict(arrowstyle="->",color="#e0a800",lw=2.2))
ax.text(0.2,7.9,"Sunlight",fontsize=8,color="#a07800",ha='left')
ax.annotate("",xy=(4.2,4.6),xytext=(3.4,1.7),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.8))
ax.annotate("",xy=(7.2,2.0),xytext=(6.6,4.6),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.8))
ax.annotate("",xy=(10.4,8.2),xytext=(9.6,6.2),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.8))
ax.annotate("",xy=(9.6,6.2),xytext=(9.2,1.7),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.8))
ax.text(11.0,3.1,"Heat from\nEarth",fontsize=7.5,color=SERIES[1],ha='center')
ax.text(6.6,3.3,"trapped heat\nreturns",fontsize=7.5,color=SERIES[1],ha='left')
ax.text(9.0,7.4,"escapes\nto space",fontsize=7.5,color=SERIES[1],ha='right')
```

### Global warming

**Global warming** is the rise of the average temperature of the Earth's surface because of more greenhouse gases in the air. Since about 1850 the Earth has warmed by about **1.1–1.2 °C**, and the amount of CO₂ in the air has risen from about 280 parts per million (ppm) before industry to over **420 ppm** today. The main causes are:

```photo id="sci10/khumbu-glacier" caption="The Khumbu Glacier below Mount Everest in Nepal. Many Himalayan glaciers are shrinking as the climate warms." width="80"
```

- burning coal, petrol, diesel and gas;
- **deforestation**, which removes the trees that absorb CO₂;
- agriculture (methane from cattle and rice fields, nitrous oxide from fertilisers);
- industrial gases and CFCs.

```figure caption="Carbon dioxide in the air (annual average, ppm, measured at Mauna Loa, Hawaii) has risen steadily. The values are rounded."
import numpy as np, matplotlib.pyplot as plt
yrs=[1960,1980,2000,2020]
co2=[317,339,370,414]
fig, ax = plt.subplots(figsize=(4.4,2.7))
ax.bar([str(y) for y in yrs],co2,color=[SERIES[0],SERIES[0],SERIES[1],SERIES[1]],width=0.55)
for i,v in enumerate(co2):
    ax.text(i,v+4,str(v),ha='center',fontsize=8,color=INK)
ax.axhline(280,color=INK,ls='--',lw=0.9)
ax.set_xlim(-0.5,4.5); ax.text(3.4,288,"before\nindustry:\n280 ppm",ha='left',fontsize=7.5,color=INK,va='bottom')
ax.set_ylim(0,470); ax.set_ylabel("CO2 (ppm)",color=INK); ax.set_xlabel("Year",color=INK)
ax.spines[['top','right']].set_visible(False)
```

### Effects of climate change

| Effect | What happens | Nepal example |
|---|---|---|
| Melting of glaciers and snow | Glaciers shrink; glacial lakes swell and may burst (**GLOF**) | Himalayan glaciers shrinking; Tsho Rolpa lake in Rolwaling |
| Sea-level rise | Oceans expand and ice melts | Threatens coastal countries such as Bangladesh |
| Changed rainfall | Floods in some places, droughts in others; stronger monsoon storms | Floods and landslides in the hills and terai; drought in other years |
| Heat waves and warm winters | More heat stroke; fewer cold days | Rising temperatures in the terai |
| Harm to farming | Crop failure; new pests | Shifting of apple farming to higher places |
| Loss of biodiversity | Species cannot adapt | Plants moving higher up the mountains |
| Spread of diseases | Mosquitoes move to new heights | Dengue and malaria in the hills |

Nepal produces only a tiny part of the world's greenhouse gases (well under 0.1%), but it is among the countries most at risk from climate change, because of its steep mountains, melting glaciers and dependence on farming.

### Ozone layer depletion

The **ozone layer** (O₃) is a thin region of the stratosphere, about 15–35 km above the Earth, that absorbs most of the harmful **ultraviolet (UV) rays** of the sun. **CFCs** (chlorofluorocarbons) from refrigerators, air conditioners and spray cans rise to the stratosphere, where UV breaks them and frees chlorine atoms. Each chlorine atom can destroy thousands of ozone molecules. The thinning of the ozone layer is greatest over Antarctica (the **ozone hole**).

**Effects of a thinner ozone layer:** skin cancer, cataract of the eye, weak immunity, damage to crops and to plankton in the sea.

The **Montreal Protocol** (1987) is an international agreement that has phased out most CFCs; the ozone layer is now slowly recovering.

### What can we do?

- Save energy: switch off lights and fans, use LED bulbs and efficient appliances.
- Use clean energy: hydropower, solar, wind and biogas instead of fossil fuels.
- Walk, cycle or use public transport.
- Plant trees and protect forests.
- Reduce, reuse and recycle waste.
- Buy local food and avoid waste of food.
- Spread awareness; support the national and global agreements (the **Kyoto Protocol**, **Paris Agreement of 2015**, which aims to keep warming well below 2 °C).


::: example Worked example 6.2 (carbon dioxide change)
**Problem.** The carbon dioxide level in the air was 280 ppm before industry and is about 420 ppm today. Find the increase and the percentage increase.

**Solution.** Increase = 420 − 280 = **140 ppm**.

Percentage increase = (140 / 280) × 100 = **50%**.

The amount of CO₂ in the air has risen by about half since industry began.
:::

## 6.4 Waste management

**Waste** is any unwanted or useless material thrown away. Nepal's cities produce more and more waste each year, and the Kathmandu valley alone produces more than a thousand tonnes of it every day. Poor handling of waste pollutes the air, water and soil, causes disease, and spoils the look of cities.

### Types of waste

| Type | Examples |
|---|---|
| **Biodegradable** (decays by bacteria) | Kitchen waste, vegetable peels, leaves, paper, dung |
| **Non-biodegradable** (does not decay quickly) | Plastic, glass, metal cans, rubber, thermocol |
| **Hazardous** | Batteries, medicines, chemicals, paints, e-waste, hospital waste |
| **E-waste** | Old mobile phones, computers, televisions |

By source: **household** (domestic), **industrial**, **agricultural**, **hospital (medical)**, **commercial** and **electronic** waste.

### The 3 Rs and the waste hierarchy

The best way to manage waste is not to produce it. The order of preference is:

1. **Reduce:** use less; buy only what you need; say no to single-use plastic.
2. **Reuse:** use the same thing again, such as bottles, cloth bags and old clothes.
3. **Recycle:** turn waste into a new product, such as old paper into new paper, metal into new metal, plastic into new plastic goods.

Some add a fourth R, **Recover** (get energy from waste, e.g. biogas), and **Refuse** or **Repair**. The last choice is **disposal** in a landfill.

```figure caption="The waste hierarchy. Methods nearer the top are better for the environment."
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.4,2.8))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(-0.7,8)
lv=[("Reduce","most preferred","#7bbf6a"),("Reuse","","#a8d48a"),("Recycle and compost","","#e6e18a"),("Recover energy (biogas)","","#f3c34b"),("Landfill","least preferred","#e57373")]
for i,(n,s,c) in enumerate(lv):
    y0=7.2-(i+1)*1.4; w=4.0+i*1.7
    ax.add_patch(Polygon([(6-w/2,y0),(6+w/2,y0),(6+w/2-0.4,y0+1.3),(6-w/2+0.4,y0+1.3)],fc=c,ec=INK,lw=0.8))
    ax.text(6,y0+0.65,n,ha='center',va='center',fontsize=8,color=INK)
ax.text(11.8,7.4,"most\npreferred",fontsize=7,color=MUTED,ha='right',va='top')
ax.text(11.8,-0.1,"least preferred",fontsize=7,color=MUTED,ha='right',va='top')
```

### Segregation at source

Waste should be separated at home into at least **three bins**:

| Bin | Colour (common) | Contents |
|---|---|---|
| Green | Biodegradable (wet) waste | Food scraps, leaves |
| Blue | Recyclable dry waste | Paper, plastic, glass, metal |
| Red or black | Hazardous and other waste | Batteries, medicines, sanitary waste |

### Methods of waste treatment

- **Composting.** Kitchen and garden waste is put in a pit or a bin and left for weeks; bacteria and fungi turn it into dark, rich **compost** (manure). It improves soil without chemical fertiliser.
- **Vermicomposting.** Earthworms are added to the waste to make **vermicompost** faster.
- **Biogas.** Cattle dung and kitchen waste are fermented without air in a **biogas plant (digester)**; methane gas is made, which is used for cooking and light, and the slurry left is a good manure. Nepal has more than 400,000 household biogas plants.
- **Recycling.** Paper, glass, metal and plastic are collected, cleaned and made into new goods. Recycling saves energy and raw materials.
- **Sanitary landfill.** A designed pit lined with plastic or clay, where waste is buried in layers and covered with soil; the gas and the leachate are collected. Open dumping is not a landfill. Kathmandu's Sisdol landfill site is one example.
- **Incineration.** Burning waste at high temperature in closed furnaces; used for hospital and hazardous waste. Open burning is dangerous.
- **Waste water treatment.** Sewage is treated in plants before being released.

::: example Worked example 6.3 (waste calculation)
**Problem.** A household makes 1.5 kg of waste every day, of which 60% is biodegradable kitchen waste. How much compostable waste does it make in a month of 30 days? If 4 kg of waste makes 1 kg of compost, how much compost is made?

**Solution.** Total waste in 30 days = 1.5 × 30 = 45 kg.

Biodegradable waste = 60% of 45 = 0.6 × 45 = **27 kg**.

Compost = 27 / 4 = **6.75 kg**.

The other 40% (18 kg) is non-biodegradable and must be reduced, reused or recycled.
:::

```photo id="sci10/landfill" caption="A landfill site: mixed waste is dumped, compacted and covered with soil. Leachate and methane from it must be managed." width="80"
```

### E-waste and plastic

**Plastic** takes hundreds of years to break down. It chokes drains, kills cows and fish that swallow it, and gives off poisonous gases when burned. Use cloth or jute bags, avoid single-use plastic, and recycle. **E-waste** contains lead, mercury and cadmium, and also precious metals; old phones and computers should be given to authorised recyclers, not thrown away.

### Role of people and law

Management of solid waste is the duty of local government (municipality) under the Solid Waste Management Act of Nepal, but it cannot succeed without every home and school. The principle is "**polluter pays**": the one who makes the waste should bear the cost of managing it.

## 6.5 Conservation

**Conservation** is the wise use and protection of natural resources so that they can serve both present and future generations.

### Natural resources

| Renewable | Non-renewable |
|---|---|
| Can be replaced naturally in a short time: forests, water, sunlight, wind, soil | Cannot be replaced in a human lifetime: coal, petroleum, natural gas, metals |

```photo id="sci10/kaligandaki" caption="The Kaligandaki A hydroelectric power station in Nepal. Falling water is a renewable source of energy." width="80"
```

### Biodiversity

**Biodiversity** is the variety of all living things on Earth: the variety of species, of genes within species, and of ecosystems. It is important because it gives us food, medicine, wood and clean air; keeps the ecosystem stable; and has beauty and culture value. Nepal is a "hotspot" of biodiversity. Threats to biodiversity: **loss of habitat** (deforestation, expansion of cities), **poaching** and illegal trade of wildlife, **pollution**, **climate change**, **invasive alien species** (such as the weed *Mikania micrantha* in Chitwan) and over-use of resources.

### Conservation methods

| Method | Meaning | Examples in Nepal |
|---|---|---|
| **In-situ conservation** | Protecting the species in its natural home | National parks, wildlife reserves, conservation areas, buffer zones, community forests |
| **Ex-situ conservation** | Protecting species outside their natural home | Zoos (Central Zoo, Jawalakhel), botanical gardens (Godawari), gene banks, seed banks, breeding centres (the Gharial Breeding Centre in Chitwan) |

### Protected areas of Nepal

Nepal has about **23%** of its land in protected areas. It has **12 national parks** (such as **Chitwan**, the first, established in 1973; **Sagarmatha**; **Langtang**; **Bardia**; **Shey-Phoksundo**, the biggest), a **wildlife reserve** (Koshi Tappu, also a Ramsar site, famous for birds and wild water buffalo), a **hunting reserve** (Dhorpatan) and **conservation areas** (Annapurna, the first; Manaslu; Kanchenjunga, and others). The national parks and conservation areas are surrounded by **buffer zones**, where local people share the income and manage the forest. **Chitwan National Park** and **Sagarmatha National Park** are **World Heritage Sites**.

```photo id="sci10/tiger" caption="A Bengal tiger in Bardiya National Park, Nepal. National parks protect the habitat of such rare animals." width="76"
```

| Wildlife | Status in Nepal |
|---|---|
| One-horned rhinoceros | Recovered to over 750 in the terai |
| Bengal tiger | Doubled to about 355 (2022 count) |
| Snow leopard, red panda, musk deer | Endangered or vulnerable |
| Gharial, Ganges river dolphin | Critically endangered / endangered |

```photo id="sci10/rhino" caption="Greater one-horned rhinoceros with calf in Chitwan National Park, one of the species saved by protection in Nepal." width="80"
```

```photo id="sci10/snow-leopard" caption="The snow leopard, the top predator of the high Himalaya, found in Nepal's mountain national parks such as Shey Phoksundo." width="60"
```

### Community forestry

Nepal's **community forestry** programme, where local forest user groups look after nearby forests and use the products, is a world example of conservation by people. It has restored hill forests and today about 45% of Nepal's land is forest.

### Other conservation steps

- **Afforestation** (planting trees on new land) and **reforestation** (replanting trees where forest was cut).
- Controlled grazing and firewood use; improved cookstoves and biogas that save wood.
- **Soil conservation:** terrace farming, contour ploughing, planting cover crops and trees on slopes to prevent erosion and landslides.
- **Water conservation:** rainwater harvesting, repairing leaks, protecting the headwaters and wetlands, and drip irrigation.
- **Energy conservation:** use of renewable energy and efficient devices.
- Laws and agreements: the National Parks and Wildlife Conservation Act 1973, the Forest Act 2019, CITES (regulates trade in endangered species), the Ramsar Convention on wetlands, and the Convention on Biological Diversity.
- **Education and awareness:** school eco-clubs, tree-planting and clean-up campaigns, and World Environment Day (5 June).

::: example Worked example 6.4 (forest cover)
**Problem.** The land area of Nepal is about 147,500 km². If about 45% of it is under forest, find the forest area in km². If a community forest of 60 km² loses 6 km² to fire, what percentage of it is lost?

**Solution.** Forest area = 45% of 147,500 = 0.45 × 147,500 = **66,375 km²**.

Percentage loss = (6 / 60) × 100 = **10%**.
:::

::: tip The big idea
Sustainable development means meeting today's needs without harming the ability of future generations to meet theirs. Whenever you answer a conservation question, link your answer to this idea.
:::

## Chapter summary

- An ecosystem is the living (producers, consumers, decomposers) and non-living parts of a place interacting. Energy flows in one direction (10% passes to the next level); matter is recycled in carbon, nitrogen and water cycles.
- Food chains join to form a food web: producer → herbivore → carnivore → top carnivore.
- Air pollutants: CO, CO₂, SO₂, NOₓ, particles, CFCs; water pollution from sewage, chemicals and fertilisers (eutrophication); soil pollution from plastic and agrochemicals; noise above 85 dB harms hearing.
- Greenhouse gases (CO₂, CH₄, N₂O, CFCs) trap heat. Global warming melts glaciers, raises sea level and changes rainfall. CFCs thin the ozone layer, allowing more UV rays; the Montreal Protocol controls them.
- Waste is biodegradable or non-biodegradable. Follow the 3 Rs (reduce, reuse, recycle) and segregate at source; compost, biogas and sanitary landfill are the main treatments.
- Conservation is wise use of resources: in-situ (parks, reserves, community forests) and ex-situ (zoos, gene banks). Nepal protects about 23% of its land; Chitwan was the first national park (1973).

## Practice questions

**Group A — Objective questions (1 mark each)**

1. Which of the following is a decomposer? <span class="marks">[1]</span>
   (a) Grass (b) Frog (c) Fungus (d) Eagle
2. The gas mainly responsible for the greenhouse effect is <span class="marks">[1]</span>
   (a) oxygen (b) nitrogen (c) carbon dioxide (d) hydrogen
3. The ozone layer is depleted mainly by <span class="marks">[1]</span>
   (a) CO (b) CFCs (c) methane (d) SO₂
4. According to the 10% law, if the producers store 5,000 kJ, the energy at the secondary consumer level is <span class="marks">[1]</span>
   (a) 500 kJ (b) 50 kJ (c) 5 kJ (d) 250 kJ
5. The first national park of Nepal is <span class="marks">[1]</span>
   (a) Sagarmatha (b) Chitwan (c) Bardia (d) Langtang
6. Which one is a biodegradable waste? <span class="marks">[1]</span>
   (a) plastic bag (b) glass bottle (c) vegetable peel (d) aluminium can

::: note Answers to Group A
**1.** (c) — fungi (and bacteria) break down dead matter.
**2.** (c) — CO₂ is the main greenhouse gas from human activity.
**3.** (b) — chlorine from CFCs destroys ozone.
**4.** (b) — 5,000 × 10% = 500 kJ (primary), then 10% = 50 kJ (secondary).
**5.** (b) — Chitwan National Park, 1973.
**6.** (c) — vegetable peel is decayed by bacteria.
:::

**Group B — Short answer (2 marks each)**

1. Define ecosystem and food chain. <span class="marks">[2]</span>
2. What is the greenhouse effect? Name two greenhouse gases. <span class="marks">[2]</span>
3. What is acid rain? State one harm it causes. <span class="marks">[2]</span>
4. What are the 3 Rs of waste management? <span class="marks">[2]</span>
5. Differentiate between in-situ and ex-situ conservation with one example each. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** An ecosystem is a community of living things interacting with each other and with the non-living environment. A food chain is the sequence of organisms in which each is eaten by the next, so that energy passes along.
**2.** The trapping of the Earth's heat by gases in the atmosphere, which keeps the Earth warm. Two gases: carbon dioxide and methane.
**3.** Rain with pH below 5.6 containing sulphuric and nitric acid made from SO₂ and NOₓ. It damages crops, forests, buildings or kills fish.
**4.** Reduce, reuse, recycle.
**5.** In-situ: protecting the species in its natural home, e.g. Chitwan National Park. Ex-situ: protecting outside its home, e.g. the Central Zoo.
:::

**Group C — Long answer (4 marks each)**

1. Explain the causes, effects and control of air pollution. <span class="marks">[4]</span>
2. What is global warming? Describe its causes and four effects. <span class="marks">[4]</span>
3. In the food chain grass → grasshopper → frog → snake → eagle, 50,000 kJ of energy is stored in the grass. Find the energy received by the snake and by the eagle. Draw an energy pyramid. <span class="marks">[4]</span>
4. Describe the methods of waste management that can be used at home and in the community. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Causes: vehicle smoke, brick kilns, factories, burning of waste, dust, firewood smoke. Effects: asthma, lung disease, eye irritation, acid rain, smog, global warming, damage to crops and buildings. Control: public and electric vehicles, vehicle testing, clean stoves and biogas, filters on chimneys, tree planting, ban on burning waste.
**2.** Global warming is the rise of the average temperature of the Earth due to the increase of greenhouse gases. Causes: burning fossil fuels, deforestation, agriculture (methane, nitrous oxide), CFCs. Effects: glaciers melt; sea level rises; floods and droughts; harm to crops and biodiversity; spread of diseases.
**3.** Grasshopper = 10% of 50,000 = 5,000 kJ; frog = 500 kJ; snake = 50 kJ; eagle = 5 kJ. Pyramid: widest base grass (50,000), then grasshopper (5,000), frog (500), snake (50), top eagle (5).
**4.** Reduce, reuse and recycle; segregate waste at source into biodegradable, recyclable and hazardous; compost kitchen waste or use vermicompost; make biogas from dung and kitchen waste; sanitary landfill for the remaining waste; avoid open burning; treat sewage; e-waste to authorised recyclers.
:::

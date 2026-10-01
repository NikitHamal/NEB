---
subject: Social Studies and Human Value Education
grade: 10
unit: 6
title: Our Earth
hours: 0
area: Units
---

The Earth is the only home we have, and it is not the same everywhere. A farmer in the Terai grows rice under a hot monsoon sky; a herder in Mustang watches snow arrive in October; a fisher in the Amazon lives where it rains almost every afternoon; an Inuit hunter lives where the sun does not rise for weeks in winter. The difference is mostly **climate**, and climate is shaped by latitude, height, the sea and the winds. In this unit you will first learn why climates differ and how the world is divided into tropical, temperate and cold regions. Then you will take a tour of three continents (North America, South America and Africa), study the natural disaster that matters most to Nepal, the earthquake, and finish with the skills of reading and drawing maps and the modern technology that now makes them.

::: key What the SEE paper expects from this unit
Expect definitions (weather, climate, earthquake, scale), "state any four factors" questions on climate, comparisons between climate regions in a table, the location and features of the three continents, the causes and safety measures for earthquakes, and one practical map question (convert a scale, find a direction, or read a grid). Learn the **facts and numbers** in the tables; they are what earns the marks.
:::

```photo id="soc10/blue-marble" caption="The Earth photographed by the Apollo 17 crew in December 1972. Africa lies at the centre, with Arabia to its right and the white cloud of the Antarctic ice cap below. Oceans cover about 71 per cent of the surface; the climates and continents of this unit are all squeezed into the remaining 29 per cent." width="64"
```

## 6.1 Factors affecting climate

### Weather and climate

**Weather** is the condition of the atmosphere (temperature, rain, wind, cloud, humidity) at a particular place and time. It can change within hours. **Climate** is the average weather of a place over a long period, usually **30 years or more**. "It is raining in Pokhara today" is weather; "Pokhara has heavy monsoon rain and mild winters" is climate.

::: definition Climate
Climate is the average condition of weather of a place or region over a long period of time, usually thirty years or more.
:::

| Weather | Climate |
|---|---|
| Short-term condition of the atmosphere | Long-term average of weather |
| Changes from hour to hour and day to day | Changes very slowly |
| Describes one place at one time | Describes a whole region over many years |
| Example: a foggy morning in Kathmandu | Example: monsoon climate of Nepal |

### The main factors

Seven factors decide the climate of a place. Learn them as a list.

**1. Latitude.** Latitude is the distance of a place north or south of the equator. Near the equator the sun's rays fall almost vertically, so a small area receives concentrated heat. Towards the poles the rays fall at a slant and are spread over a larger area, so the ground is cooler. That is why the climate becomes colder as we move from the equator to the poles.

**2. Altitude.** The air gets thinner and cooler with height. On average the temperature falls by about **6.5 °C for every 1,000 m** you climb (about 0.65 °C per 100 m). This is called the **normal lapse rate**. It explains why Kathmandu (about 1,400 m) is cooler than Birgunj (about 100 m), and why the Himalaya keep snow all year even though Nepal lies at the same latitude as Florida.

::: example Altitude and temperature
**Problem.** At Biratnagar (about 70 m above sea level) the temperature at noon is 32 °C. What temperature would you expect at Namche Bazaar (about 3,440 m) at the same moment, using the lapse rate of 6.5 °C per 1,000 m?

**Solution.**
Height difference = 3,440 m − 70 m = 3,370 m.
Fall in temperature = 3.37 × 6.5 °C ≈ 21.9 °C.
Temperature at Namche ≈ 32 − 21.9 = **10.1 °C**.

The real value differs a little because of cloud and wind, but the method shows why high places are cold.
:::

```figure caption="Temperature falls with height at about 6.5 °C per 1,000 m. The places are plotted for a sea-level temperature of 30 °C; real values vary with season and weather."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
h = np.linspace(0, 5000, 50)
t = 30 - 6.5*h/1000
ax.plot(t, h, color=ACCENT, lw=2)
pts = [("Terai plain (100 m)", 100), ("Kathmandu (1,400 m)", 1400), ("Namche Bazaar (3,440 m)", 3440), ("Everest Base Camp (5,364 m)", None)]
for name, hh in pts[:3]:
    tt = 30 - 6.5*hh/1000
    ax.plot([tt],[hh],'o',color=SERIES[1])
    ax.annotate(name, (tt, hh), xytext=(tt+2.5, hh+60), fontsize=7.5, color=INK)
ax.set_xlabel("Temperature (deg C)", fontsize=8)
ax.set_ylabel("Height above sea level (m)", fontsize=8)
ax.set_ylim(0,5000); ax.set_xlim(-4,34)
ax.grid(color=GRID, lw=0.5)
ax.spines[['top','right']].set_visible(False)
ax.tick_params(labelsize=8)
```

**3. Distance from the sea.** Water heats and cools slowly; land heats and cools quickly. Places near the sea therefore have a **maritime (equable)** climate with mild summers and winters. Places deep inside a continent have a **continental** climate with hot summers, cold winters and little rain. Compare coastal Mumbai with inland Nagpur, or coastal Britain with inland Siberia.

**4. Ocean currents.** A warm current heats the air above it and carries moisture to the land, while a cold current cools and dries it. The warm North Atlantic Drift keeps the ports of Norway ice-free in winter although they lie far north. The cold Peru (Humboldt) Current helps to create the dry Atacama coast of Chile.

**5. Winds.** Winds from the sea bring rain; winds blowing from the land are dry. The **monsoon** is a seasonal wind. In summer it blows from the Indian Ocean and Bay of Bengal to South Asia and brings about 80 per cent of Nepal's annual rainfall (June to September); in winter it blows from the land and the weather is dry.

**6. Relief (mountains and slope).** Mountains force moist wind to rise, cool and drop rain on the windward side (**relief rain**). The far, leeward side receives little rain and is called the **rain shadow**. Mustang, behind the Annapurna and Dhaulagiri ranges, is a rain-shadow desert with only about 25 cm rain a year, while Pokhara in front of the range receives over 3,000 mm. Slopes facing the sun are also warmer than those in shadow.

**7. Vegetation and soil.** Forests keep the air humid and cool, return water to the air by transpiration and shelter the soil, so forested lands tend to have more rain and gentler temperatures. Bare soil and cities heat up faster.

```figure caption="Rain-shadow effect (schematic). Moist wind rises over the mountain, cools and drops rain on the windward side; the leeward side is dry."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8,2.6))
ax.add_patch(Polygon([(0,0),(3.2,0),(5,3.2),(6.8,0),(10,0)], color="#b9a98a"))
ax.add_patch(Polygon([(4.4,2.2),(5,3.2),(5.6,2.2)], color="white", ec=GRID))
ax.annotate("", xy=(3.4,1.9), xytext=(0.2,0.8), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6))
ax.text(0.2,1.6,"Moist wind", fontsize=8, color=ACCENT)
for x in (3.0,3.5,4.0):
    ax.plot([x,x-0.15],[2.6,2.1], color=SERIES[0], lw=1.2)
ax.text(1.3,3.0,"Heavy rain", fontsize=8, color=SERIES[0])
ax.annotate("", xy=(9.5,1.1), xytext=(6.2,2.3), arrowprops=dict(arrowstyle="-|>", color=SERIES[3], lw=1.6))
ax.text(7.3,2.55,"Dry, warm air", fontsize=8, color=SERIES[3])
ax.text(1.0,-0.45,"Windward side", fontsize=8, color=INK)
ax.text(7.0,-0.45,"Leeward side (rain shadow)", fontsize=8, color=INK)
ax.set_xlim(0,10); ax.set_ylim(-0.7,3.8); ax.axis('off')
```

::: caution Weather is not climate
Students write "the climate of Kathmandu today is foggy". Fog today is **weather**. Climate is always a long-term average. Examiners withhold the mark for this slip.
:::

## 6.2 Types of world climate

Geographers divide the world into **climate regions** (also called zones or *mandals*): large areas with a similar pattern of temperature, rainfall and natural vegetation. The textbook classifies them by **latitude, heat from the sun and air pressure** into three main groups, and each is then split into sub-types.

| Main region | Latitude (approx.) | Sub-types in the textbook |
|---|---|---|
| **Tropical** (hot) | 0° to 30° N and S | Equatorial, savanna, monsoon, hot desert |
| **Temperate** (mild) | 30° to 60° N and S | Mediterranean, China type (warm temperate east margin), British (west European) type, temperate grassland |
| **Cold** (polar and sub-polar) | 60° to 90° N and S | Taiga (coniferous forest), tundra, polar ice cap |

(The astronomical heat belts, torrid, temperate and frigid zones, are bounded by the Tropics at 23.5° and the Arctic and Antarctic Circles at 66.5°; the climate regions above are broader, more practical groupings.)

```figure caption="World climate regions by latitude (schematic bands, not an exact map). Tropical 0-30, temperate 30-60, cold 60-90 degrees in each hemisphere."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
bands = [(60,90,"#cfe3f5","Cold (taiga, tundra, ice cap)"),(30,60,"#cfe8c6","Temperate"),(0,30,"#f6d9a8","Tropical")]
for lo,hi,c,name in bands:
    ax.axhspan(lo,hi,color=c,ec="none")
    ax.axhspan(-hi,-lo,color=c,ec="none")
    ax.text(0.5,(lo+hi)/2,name,ha="center",va="center",fontsize=8,color=INK)
    if lo!=0 or True:
        ax.text(0.5,-(lo+hi)/2,name.split(" (")[0],ha="center",va="center",fontsize=8,color=INK)
ax.axhline(0,color=INK,lw=1)
ax.text(0.99,1.5,"Equator",ha="right",fontsize=7.5,color=INK)
for y in (23.5,-23.5,66.5,-66.5):
    ax.axhline(y,color=MUTED,lw=0.7,ls="--")
ax.text(0.01,25,"Tropic of Cancer 23.5",fontsize=7,color=MUTED)
ax.text(0.01,-30,"Tropic of Capricorn 23.5",fontsize=7,color=MUTED)
ax.text(0.01,68,"Arctic Circle 66.5",fontsize=7,color=MUTED)
ax.text(0.01,-73,"Antarctic Circle 66.5",fontsize=7,color=MUTED)
ax.set_xlim(0,1); ax.set_ylim(-90,90)
ax.set_yticks([-90,-60,-30,0,30,60,90]); ax.set_xticks([])
ax.set_yticklabels(["90S","60S","30S","0","30N","60N","90N"],fontsize=8)
ax.set_ylabel("Latitude",fontsize=8)
for s in ax.spines.values(): s.set_visible(False)
```

::: definition Climate region
A climate region is a large area of the Earth that has a similar climate, shown by similar temperature, rainfall and natural vegetation.
:::

Nepal is unusual. Lying at about 26° to 30° N, it belongs to the **tropical monsoon** to **warm temperate** belt, yet because the land rises from about 60 m to 8,849 m within 150 km, it also contains alpine and polar-like conditions. Few countries in the world pack so many climates into so small an area.

## 6.3 Tropical region

The tropical region lies on both sides of the equator and receives strong, direct sunshine all year, so every month is warm; the average temperature seldom falls below 18 °C. It has four sub-types.

### Equatorial climate

- **Location:** within about 5° to 10° of the equator: the Amazon basin (Brazil), the Congo basin (Central Africa), Indonesia and Malaysia.
- **Climate:** hot and wet all year. Average temperature about 27 °C; the yearly range is tiny (1 to 3 °C). Heavy rain of 200 cm or more falls nearly every afternoon as **convectional rain** (the hot ground heats the air, which rises, cools and condenses).
- **Vegetation:** dense **tropical evergreen rainforest**: tall hardwood trees (mahogany, ebony, rosewood), thick undergrowth, vines, trees in several layers; so dense that little sunlight reaches the floor.
- **Animals:** monkeys, snakes, jaguars (Amazon), gorillas, okapi (Congo), colourful birds, insects.
- **People and economy:** thinly populated; hunter-gatherers such as the Pygmies of the Congo and tribes of the Amazon; plantation crops: rubber, oil palm, cocoa; timber extraction (threatens forests).

```photo id="soc10/amazon" caption="The Amazon rainforest seen from the International Space Station: unbroken green canopy and a winding river. The Amazon basin holds the world's largest tropical rainforest and is a prime example of the equatorial climate." width="86"
```

### Savanna (tropical grassland) climate

- **Location:** on the edges of the equatorial belt, about 5° to 20° (up to 30°) north and south: the Sudan region and East Africa (Serengeti, Kenya), the Llanos of Venezuela, the Campos of Brazil and northern Australia.
- **Climate:** hot all year (about 20 to 30 °C) with a **wet summer and a long dry winter**; annual rain 75 to 150 cm.
- **Vegetation:** tall **elephant grass** with scattered umbrella-shaped trees such as acacia and baobab; trees are drought-resistant and shed leaves in the dry season.
- **Animals:** lion, elephant, giraffe, zebra, wildebeest, rhinoceros; the largest herds of wild animals in the world.
- **People:** pastoral peoples (Maasai of Kenya and Tanzania) and farmers growing maize, millet, cotton; tourism from national parks is a major earner.

```photo id="soc10/serengeti" caption="Wildebeest on the Serengeti plain, Tanzania. Each year about 1.5 million wildebeest, with zebra and gazelle, follow the rains in a circular migration across the savanna; the herds are the main attraction for tourists." width="84"
```

### Monsoon climate

- **Location:** South Asia (India, Bangladesh, Nepal, Sri Lanka, Myanmar), Southeast Asia (Thailand, Vietnam, Cambodia) and southern China.
- **Climate:** the seasons are named for the wind: **hot summer** (March to May), **rainy monsoon** (June to September, wet winds from the sea) and **cool, dry winter**. Rainfall varies from 50 cm to over 250 cm; it is the heaviest on windward slopes (Cherrapunji and Mawsynram in Meghalaya, India, are among the wettest places on Earth).
- **Vegetation:** **deciduous (monsoon) forest** such as sal, teak and sissoo, which sheds its leaves in the dry season; evergreen forest where rainfall is very high.
- **People and economy:** the most densely populated climate region on Earth. Because the rains come in one season, the main food crop is **rice**, with wheat, maize, sugarcane, jute, tea and cotton; farming depends heavily on the arrival of the monsoon.

Most of the Terai and the inner Madhesh of Nepal has this climate; this is the answer to the textbook question "In which climate region do you live?".

### Hot desert climate

- **Location:** on the western side of continents between 15° and 30° in both hemispheres: the Sahara and Kalahari (Africa), the Arabian and Thar deserts (Asia), the Atacama (South America), the Great Australian Desert.
- **Climate:** very hot days (over 40 °C, even 50 °C), cold nights because the clear dry sky lets heat escape; rainfall below 25 cm and irregular. The Sahara reaches 50 °C in the shade.
- **Vegetation:** cactus, thorny shrubs, date palms at **oases**; long roots or waxy leaves to save water.
- **Animals:** camel, snake, lizards, scorpions, desert fox.
- **People:** nomads such as the Bedouin and Tuareg who herd camels and goats; settled life only at oases and along the Nile. Oil in Arabia has turned some deserts into rich economies.

```photo id="soc10/sahara" caption="Sand dunes, the classic landscape of a hot desert. The Sahara of North Africa is the largest hot desert in the world, with an area of about 9 million square kilometres, almost as large as the United States." width="78"
```

| Feature | Equatorial | Savanna | Monsoon | Hot desert |
|---|---|---|---|---|
| Temperature | ~27 °C all year | 20–30 °C | Hot summer, cool winter | 40 °C+ day, cold night |
| Rainfall | 200 cm+, daily | 75–150 cm, summer | 50–250 cm, June–Sept | Under 25 cm |
| Vegetation | Evergreen rainforest | Tall grass, scattered trees | Deciduous forest | Cactus, thorny shrubs |
| Famous areas | Amazon, Congo | Serengeti, Llanos | South Asia, Terai | Sahara, Thar |
| People | Hunter-gatherers, plantation workers | Herders, farmers | Dense farming population | Nomads, oasis farmers |

## 6.4 Temperate region

Between 30° and 60° the sun's rays are neither vertical nor too slanting, so the region has **moderate temperature with four distinct seasons**: spring, summer, autumn and winter. It is the most favourable region for human life, which is why large parts of Europe, East Asia and the eastern United States are densely populated and highly developed.

### Mediterranean climate

- **Location:** the western margins of continents between 30° and 40°: around the Mediterranean Sea (Italy, Greece, Spain), California (USA), central Chile, the Cape of South Africa, south-west and south Australia.
- **Climate:** **hot, dry, sunny summers and mild, rainy winters**; rain 40–100 cm falls mainly in winter, brought by westerly winds.
- **Vegetation:** evergreen trees with thick leaves and long roots: olive, cork oak, citrus, and scrub; this is called **Mediterranean vegetation**.
- **Economy:** citrus fruits (oranges, lemons), grapes and wine, olives, figs; the dry sunny summers also bring tourists to the beaches of Spain and Greece.

### China type (warm temperate eastern margin) climate

- **Location:** the eastern sides of continents between about 25° and 40°: central and south China, southern Japan, south-east USA, south-east Australia, Uruguay.
- **Climate:** warm to hot, humid summers with monsoon-like rain; cool winters; rain 100–150 cm throughout the year, heaviest in summer.
- **Vegetation:** mixed forest; much land cleared for farms.
- **Economy:** very productive agriculture; rice, tea, silk, cotton, maize, fruits; high population density, large industrial cities such as Shanghai.

### British (west European marine) climate

- **Location:** western margins between 40° and 60°: Britain, Ireland, France, Norway, Netherlands, south-west Canada, southern Chile, New Zealand.
- **Climate:** a gentle, **maritime** climate: cool summers, mild winters (the warm North Atlantic Drift prevents freezing), rain all year (60–150 cm) with frequent cloud and changeable weather.
- **Vegetation:** deciduous broad-leaved forest (oak, beech, elm), losing leaves in autumn.
- **Economy:** dairy farming, mixed farming, fishing; the birthplace of the Industrial Revolution; densely populated, urban.

### Temperate grassland (steppe) climate

- **Location:** in the interior of continents where the sea cannot moderate the weather: the **prairies** of North America, the **pampas** of Argentina, the **steppes** of Eurasia, the **veld** of South Africa and the **downs** of Australia.
- **Climate:** continental: hot summers, very cold winters, 25–75 cm of rain (mostly spring and summer).
- **Vegetation:** short, nutritious grass, almost treeless.
- **Economy:** the "granary of the world": wheat, maize and cattle ranching on huge mechanised farms.

| Feature | Mediterranean | China type | British type | Grassland |
|---|---|---|---|---|
| Position | West coast, 30–40° | East coast, 25–40° | West coast, 40–60° | Continental interior |
| Rainy season | Winter | All year, summer peak | All year | Spring/summer |
| Summer | Hot, dry | Hot, humid | Cool | Hot |
| Winter | Mild, wet | Cool | Mild | Very cold |
| Chief products | Citrus, olives, grapes | Rice, tea, silk | Dairy, wheat, fish | Wheat, beef |

## 6.5 Cold region

Beyond 60° the sun is low in the sky even at midday; in the polar night the sun may not rise for weeks, and in the polar summer it may not set (the **midnight sun**). The region has a long, bitter winter and a short, cool summer.

### Taiga (coniferous forest) climate

- **Location:** a broad belt across northern Canada, Alaska, Scandinavia and Siberia (Russia) at roughly 50° to 70° N; there is almost no equivalent in the southern hemisphere because there is little land there.
- **Climate:** winters of 6 to 9 months with temperatures far below freezing (Verkhoyansk in Siberia has recorded about −68 °C); summers short, cool to warm; precipitation 25–50 cm, mostly snow.
- **Vegetation:** the world's largest forests: **coniferous (softwood) trees**, namely pine, fir, spruce and larch, with needle-shaped leaves and conical shape so that snow slides off.
- **Economy:** lumbering is the main activity (paper, pulp, furniture and matches); fur trapping; thinly populated.

### Tundra climate

- **Location:** the coast of the Arctic Ocean north of the taiga: northern Canada, Alaska, Greenland's margins, northern Russia and Scandinavia, and also the higher mountains.
- **Climate:** winter temperature down to −30 to −50 °C; the short summer barely reaches 10 °C; a layer of soil stays frozen all year (**permafrost**); low precipitation, mostly snow.
- **Vegetation:** only mosses, lichens, sedges and tiny flowering plants in the short summer.
- **Animals:** reindeer (caribou), musk ox, Arctic fox, polar bear, seals, snowy owl.
- **People:** thin population: the Inuit (Eskimo) of Canada and Greenland and the Sami and Nenets of Eurasia; hunting, fishing and herding of reindeer.

### Polar ice cap climate

- **Location:** Antarctica and most of Greenland, and the Arctic Ocean ice.
- **Climate:** the coldest on Earth; the lowest temperature ever recorded, **−89.2 °C**, was at Vostok Station, Antarctica; permanent ice and snow; strong winds; very little precipitation (it is a "cold desert").
- **Life:** no permanent population; scientists live in research stations; penguins, seals, whales and seabirds live on the coast.

::: tip Comparing regions
When asked to "compare the tundra and taiga", draw a two-column table of location, temperature, vegetation, animals and people. Always include **one example place** in each cell: this is how marks are earned.
:::

## 6.6 World climate: relief and its effects

Climate and relief (land shape) decide where people can live, what they eat, how they dress and what work they do. The textbook asks you to connect the two.

| Climate or land | Natural vegetation | Typical animals | Population | Main activity |
|---|---|---|---|---|
| Equatorial lowland | Rainforest | Monkey, jaguar | Sparse | Plantation, forestry |
| Savanna | Grass and acacia | Lion, zebra | Medium | Herding, tourism |
| Monsoon plains | Deciduous forest | Tiger, rhino, elephant | **Very dense** | Rice farming |
| Desert | Cactus | Camel | Very sparse | Nomadism, oil |
| Mediterranean | Olive, citrus | Sheep, goat | Dense | Fruit, tourism |
| West European marine | Broad-leaf forest | Cattle | Dense | Dairy, industry |
| Taiga | Conifers | Elk, bear, fox | Sparse | Lumbering |
| Tundra / ice | Moss, lichen | Reindeer, polar bear | Almost none | Hunting, research |
| High mountains | Alpine meadow, snow | Yak, snow leopard | Sparse | Herding, tourism |

**Relief matters too.** Great plains (the Ganga plain, the Mississippi valley, the Nile delta) have flat land, deep fertile soils and easy transport, so they carry the world's densest populations. Mountains (the Himalaya, the Andes) have steep slopes and thin soils, so people live scattered on terraces and in valleys. **Altitudinal zonation** is the change of vegetation with height. In Nepal one can pass from tropical sal forest in the Terai, through subtropical and temperate forest of the hills, to alpine meadow, bare rock and the permanent snow of the Himal within a day's flight.

**Effects on human life:** *Clothes:* cotton and light clothes in the tropics, woollen and fur in tundra and high mountains. *Houses:* thatched or stilted houses in rainy tropics, igloos or insulated houses in the cold, flat-roofed mud houses in deserts, sloping roofs in snowy lands. *Food:* rice in monsoon lands, wheat in temperate lands, dates and milk in deserts, fish and meat in the Arctic. *Health:* malaria in hot wet lands; frostbite in the cold.

## 6.7 The continent of North America

**Location and size.** North America lies in the northern and western hemispheres, between the Arctic Ocean in the north, the Atlantic in the east, the Pacific in the west, and joined to South America at the narrow Isthmus of Panama. With an area of about **24.7 million km²** it is the **third largest** continent. It includes Canada, the United States, Mexico, the seven nations of Central America and the island states of the Caribbean, in all 23 sovereign countries (the textbook count), and Greenland. Population is about 600 million.

### Physical features

- **Western mountains (the Cordillera):** the **Rocky Mountains** and the Sierra Nevada, with **Denali (Mount McKinley)** in Alaska, 6,190 m, the highest peak.
- **Central plains:** the **Great Plains** and Mississippi basin: a huge, flat, fertile lowland.
- **Eastern highlands:** the old, low **Appalachian Mountains**.
- **Rivers:** the **Mississippi-Missouri** (about 6,000 km together, the longest in North America), the St Lawrence, the Colorado and Mackenzie.
- **Lakes:** the five **Great Lakes** (Superior, Michigan, Huron, Erie, Ontario), the largest group of freshwater lakes on Earth, with **Niagara Falls** between Erie and Ontario.
- **Lowest point:** **Death Valley**, California, about 86 m below sea level, and one of the hottest places on Earth.

### Climate and vegetation

The vast north-south extent produces almost every climate: tundra and taiga in Canada and Alaska; cool temperate forests and prairie in the middle; Mediterranean in California; warm humid China-type in the south-east; hot desert and tropical savanna in Mexico; equatorial rainforest in Central America. Hurricanes strike the Atlantic and Gulf coasts every year, and tornadoes are common in the central plains.

### Social and economic life

- **People:** the Native peoples, Europeans (the English and French language zones), Africans (brought as slaves) and recent migrants from Asia and Latin America; English is the main language in the USA and Canada, Spanish in Mexico and Central America.
- **Agriculture:** the **wheat belt** (Great Plains), the **corn belt** (Midwest), cotton and soybean, beef cattle; the USA is among the world's largest exporters of grain; Canada produces wheat and canola.
- **Minerals and energy:** coal, oil, natural gas, iron ore (Great Lakes), copper, gold, uranium; Canada has huge forests and hydropower.
- **Industry:** cars (Detroit), aircraft, computers and software (Silicon Valley, California), steel, finance (New York).
- **Nepal connection:** the USA and Canada host large Nepali communities of students and workers; the USA is a major export market for Nepal's carpets and garments and a development partner; Nepali students are among the major groups studying in the USA.

| Fact | North America |
|---|---|
| Rank by area | 3rd |
| Area | About 24.7 million km² |
| Highest point | Denali, 6,190 m |
| Lowest point | Death Valley, about −86 m |
| Longest river | Mississippi–Missouri |
| Largest country | Canada by area, USA by population |

## 6.8 The continent of South America

**Location and size.** South America lies mostly in the southern and western hemispheres. It is bounded by the Caribbean Sea and the Atlantic on the north and east, the Pacific on the west, and the Drake Passage and the Southern Ocean in the south. The equator crosses its northern part (Ecuador, Colombia, Brazil) and the Tropic of Capricorn crosses the south of Brazil, Paraguay and northern Chile. With about **17.8 million km²** it is the **fourth largest** continent, with 12 independent countries (plus French Guiana, a French territory) and a population of about 440 million.

### Physical features

- **The Andes:** the longest mountain range on land, about **7,000 km** along the Pacific coast. **Aconcagua** in Argentina, about 6,960 m, is the highest peak in the Americas and outside Asia.
- **The Amazon basin:** the **Amazon River** carries more water than any other river on Earth (about one-fifth of all the river water reaching the oceans) and flows about 6,400 km from the Andes to the Atlantic. The basin holds the largest tropical rainforest.
- **Highlands:** the Guiana Highlands and the Brazilian Highlands.
- **Plains:** the Orinoco plains (the Llanos), and the Pampas of Argentina and Uruguay.
- **Lakes and falls:** **Lake Titicaca**, one of the highest navigable lakes (about 3,800 m); **Angel Falls** in Venezuela, the world's tallest waterfall (979 m).
- **Desert:** the **Atacama** in Chile, one of the driest places on Earth.

### Climate and vegetation

Equatorial climate and rainforest in the Amazon basin; savanna (Llanos, Campos); hot desert (Atacama, coastal Peru); Mediterranean in central Chile; temperate grassland (Pampas); cold and windy Patagonia in the south; and highland climates in the Andes where altitude produces snow even on the equator.

### Social and economic life

- **People and language:** indigenous Quechua and Aymara peoples, descendants of Spanish and Portuguese settlers and Africans; **Portuguese** is spoken in Brazil, **Spanish** in most others. The Inca civilisation built Machu Picchu in the 15th century.
- **Agriculture:** **Brazil** is the world's leading producer of coffee and sugarcane and a leading exporter of soybean and beef; Argentina's pampas supply wheat and beef; Ecuador and Colombia export bananas, flowers and coffee.
- **Minerals:** Chile is the world's largest copper producer; Bolivia has tin and lithium; Venezuela has oil; Brazil has iron ore.
- **Cities:** São Paulo, Buenos Aires, Lima and Bogotá are large cities; Brazil is by far the largest country by both area and population.
- **Problems:** deforestation of the Amazon, uneven wealth, and rapid urban growth.

```photo id="soc10/machu-picchu" caption="Machu Picchu, the 15th-century Inca citadel high in the Andes of Peru, about 2,430 m above sea level. Built of stone without mortar, it is a World Heritage Site and the country's most visited place." width="86"
```

## 6.9 The continent of Africa

**Location and size.** Africa straddles the equator, lying between the Mediterranean Sea in the north, the Atlantic in the west, the Indian Ocean in the east and the meeting of the two oceans at the Cape of Good Hope in the south. It is joined to Asia at the Sinai peninsula and separated from Europe by the narrow Strait of Gibraltar. At about **30.3 million km²** it is the **second largest** continent and has **54 countries** and about 1.4 billion people, the youngest population on Earth. Its latitude spans about 37° N to 35° S, so it has both tropics.

### Physical features

- **Plateaus:** most of Africa is a high plateau, with a narrow coastal plain.
- **Mountains:** **Kilimanjaro** in Tanzania, 5,895 m, the highest peak; Mount Kenya; the Atlas in the north and the Drakensberg in the south.
- **Great Rift Valley:** a huge crack in the Earth's crust running from East Africa to the Red Sea, containing long deep lakes.
- **Rivers:** the **Nile**, about 6,650 km, the longest river in the world, flowing north from East Africa into the Mediterranean; the Congo (deepest river), the Niger and the Zambezi.
- **Lakes and falls:** **Lake Victoria**, the largest lake in Africa and second largest freshwater lake in the world by area; **Victoria Falls** on the Zambezi.
- **Deserts:** the **Sahara** (about 9 million km², the largest hot desert), the Kalahari and the Namib.
- **Lowest point:** Lake Assal, Djibouti, about 155 m below sea level.

```photo id="soc10/victoria-falls" caption="Victoria Falls (Mosi-oa-Tunya, 'the smoke that thunders') on the Zambezi River between Zambia and Zimbabwe. About 1.7 km wide and over 100 m high, it is among the largest waterfalls in the world." width="96"
```

### Climate and vegetation

Because the equator crosses the middle, Africa is the most tropical of continents. The climate is arranged in a nearly symmetrical pattern north and south of the equator: **equatorial rainforest** (Congo basin) in the centre; **savanna** to either side; **hot desert** (Sahara in the north, Kalahari and Namib in the south-west); **Mediterranean** at the northern and southern tips; and high-mountain climates, with snow even on Kilimanjaro near the equator.

### Social and economic life

- **People:** hundreds of ethnic groups and languages; Arabic in the north, and Swahili, Hausa, Amharic, English and French elsewhere. Nigeria is the most populous country (over 200 million); Algeria is the largest by area.
- **Agriculture:** subsistence farming of millet, maize, cassava and yams; cash crops: **cocoa** (Ivory Coast, Ghana), coffee (Ethiopia, Uganda), tea (Kenya), cotton (Egypt), cloves (Zanzibar).
- **Minerals:** diamonds (Botswana, South Africa), gold (South Africa, Ghana), copper (Zambia, DR Congo), oil (Nigeria, Libya, Algeria), cobalt (DR Congo).
- **Tourism:** wildlife safaris in Kenya and Tanzania, the pyramids of Egypt, and Victoria Falls.
- **Challenges:** poverty, drought in the Sahel, diseases such as malaria and HIV/AIDS, conflicts, and dependence on raw material exports.

| Fact | North America | South America | Africa |
|---|---|---|---|
| Rank by area | 3rd | 4th | 2nd |
| Area (million km²) | ~24.7 | ~17.8 | ~30.3 |
| Highest peak | Denali 6,190 m | Aconcagua ~6,960 m | Kilimanjaro 5,895 m |
| Longest river | Mississippi–Missouri | Amazon | Nile |
| Largest desert | Great Basin / Sonoran | Atacama | Sahara |
| Equator crosses? | No | Yes | Yes |
| Number of countries | 23 | 12 | 54 |

```figure caption="Areas of the seven continents (million square kilometres, rounded). The three continents of this unit are shaded."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
names = ["Asia","Africa","N. America","S. America","Antarctica","Europe","Oceania"]
vals = [44.6,30.3,24.7,17.8,14.2,10.2,8.5]
cols = [GRID,ACCENT,ACCENT,ACCENT,GRID,GRID,GRID]
y = np.arange(len(names))[::-1]
ax.barh(y, vals, color=cols)
for yy,v in zip(y,vals):
    ax.text(v+0.6, yy, f"{v}", va="center", fontsize=8, color=INK)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8)
ax.set_xlabel("Area (million sq km)", fontsize=8)
ax.set_xlim(0,52)
ax.tick_params(labelsize=8)
ax.spines[['top','right']].set_visible(False)
```

## 6.10 Natural disaster: earthquakes

### What is an earthquake?

::: definition Earthquake
An earthquake is the sudden shaking or trembling of the ground caused by the release of energy stored in the rocks of the Earth's crust.
:::

The Earth's crust is broken into huge slabs called **tectonic plates** which move a few centimetres a year. Where they collide, slide or pull apart, rocks bend and build up stress. When the stress becomes greater than the strength of the rock, it breaks along a **fault**, and the stored energy is released in **seismic waves** that make the ground shake.

- **Focus (hypocentre):** the point underground where the rock breaks and the earthquake starts.
- **Epicentre:** the point on the surface directly above the focus. Shaking is usually strongest here.
- **Seismic waves:** *P-waves* (primary, fastest, push and pull), *S-waves* (secondary, slower, shake sideways) and *surface waves* (the slowest but the most destructive).

```figure caption="Focus and epicentre of an earthquake (schematic cross-section). Seismic waves spread outwards from the focus."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.6,3.0))
ax.axhspan(-6,0,color="#d9cdb4")
ax.axhline(0,color=INK,lw=1.2)
fx, fy = 0, -4.2
for r in (0.8,1.6,2.4,3.2):
    th = np.linspace(np.pi*1.08, np.pi*1.92, 60)
    ax.plot(fx+r*np.cos(th), fy+r*np.sin(th)+0, color=ACCENT, lw=1, alpha=0.8)
ax.plot([fx],[fy],'o',color=SERIES[3],ms=8)
ax.plot([0],[0],'^',color=SERIES[3],ms=9)
ax.plot([0,0],[fy,0],color=MUTED,ls="--",lw=1)
ax.annotate("Focus", (0,fy), xytext=(1.3,-5.3), fontsize=8, arrowprops=dict(arrowstyle="-", color=MUTED))
ax.annotate("Epicentre", (0,0), xytext=(1.3,0.8), fontsize=8, arrowprops=dict(arrowstyle="-", color=MUTED))
ax.text(-5.2,-1.2,"Depth", fontsize=8, rotation=90, va="center", color=INK)
ax.text(-3.8,0.5,"Earth's surface", fontsize=8, color=INK)
ax.text(-5.0,-2.6,"Seismic waves\nspread out", fontsize=8, color=ACCENT)
ax.set_xlim(-5.5,5.5); ax.set_ylim(-6,2); ax.axis('off')
```

### Measuring earthquakes

A **seismograph** records the ground motion and the record is called a **seismogram**. The **magnitude** (energy released) is expressed on the **Richter scale** (or the more modern *moment magnitude*) from 1 to 9; each whole number represents about 32 times more energy. The **intensity** (the visible damage at a place) is measured on the **Modified Mercalli scale** I to XII. Magnitude is one number for the quake; intensity differs from place to place.

### Why is Nepal at risk?

Nepal lies on the boundary where the **Indian Plate** is pushing northwards under the **Eurasian (Tibetan) Plate** at about 4 to 5 cm per year. This slow collision built the Himalaya and still stores huge strain in the rocks beneath Nepal. It is one of the most earthquake-prone countries in the world, and a great earthquake is expected again in future.

```figure caption="Why Nepal shakes (schematic). The Indian Plate moves northwards at about 4-5 cm a year and slides under the Eurasian Plate; the strain stored along the fault is released in earthquakes."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8,2.8))
ax.add_patch(Polygon([(0,0),(5.5,0),(5.5,-0.9),(0,-0.9)], color="#c9b790"))
ax.add_patch(Polygon([(5.5,0),(6.6,2.4),(7.8,1.0),(8.6,2.0),(10,0.6),(10,-1.6),(7.5,-1.6),(5.5,-0.9)], color="#9a9a9a"))
ax.add_patch(Polygon([(0,-0.9),(5.5,-0.9),(10,-3.4),(10,-4.4),(0,-4.4)], color="#e0d2b0"))
ax.annotate("", xy=(4.0,-0.5), xytext=(0.6,-0.5), arrowprops=dict(arrowstyle="-|>", color=SERIES[3], lw=2))
ax.text(0.4,0.35,"Indian Plate", fontsize=8, color=INK)
ax.text(0.4,-0.25,"moves north", fontsize=7.5, color=SERIES[3])
ax.text(6.4,-2.7,"Eurasian Plate", fontsize=8, color=INK)
ax.text(6.2,2.8,"Himalaya", fontsize=8, color=INK)
ax.annotate("Fault (earthquake\nenergy released)", xy=(5.5,-0.9), xytext=(2.0,-3.2), fontsize=8, arrowprops=dict(arrowstyle="-|>", color=MUTED))
ax.set_xlim(0,10); ax.set_ylim(-4.5,3.3); ax.axis('off')
```

### Major earthquakes in Nepal

| Earthquake | Date | Magnitude (approx.) | Effect |
|---|---|---|---|
| Nepal–Bihar earthquake | 15 January 1934 (2 Magh 2090 BS) | about 8.0–8.4 | About 8,500 deaths in Nepal; much of Kathmandu, Bhaktapur and Patan destroyed |
| Udayapur earthquake | 21 August 1988 (6 Bhadra 2045 BS) | 6.8 | About 700 deaths in Nepal, thousands of houses damaged in the east |
| Gorkha earthquake | 25 April 2015 (12 Baisakh 2072 BS) | 7.8 | About 9,000 deaths, about 22,000 injured, more than 500,000 houses destroyed; 31 districts badly hit |

The **2015 Gorkha earthquake** had its epicentre at Barpak, Gorkha, and struck at about midday. A second shock of magnitude 7.3 followed on 12 May 2015 with its epicentre near Kodari in Sindhupalchok. Many heritage sites, including the Dharahara tower and the durbar squares of Kathmandu, Patan and Bhaktapur, were damaged; the earthquake also set off avalanches on Everest and Langtang. Reconstruction was led by the **National Reconstruction Authority**, set up in 2015.

```photo id="soc10/quake-basantapur" caption="Basantapur Durbar Square, Kathmandu, after the 25 April 2015 earthquake. The collapse of temples and old brick buildings was the loss of centuries of heritage; houses of poor construction suffered most." width="88"
```

### Safety measures

| Before | During | After |
|---|---|---|
| Build houses by the building code; bolt heavy furniture; keep an emergency bag with torch, radio, water, first-aid kit; know an open assembly area; practise **Drop, Cover, Hold** drills at school | **Drop** to the ground, take **cover** under a strong table, **hold** on; stay away from windows and walls; if outdoors, go to open ground away from buildings, wires and slopes; if driving, stop in the open | Check for injuries and give first aid; expect **aftershocks**; leave damaged buildings; turn off gas and electricity; listen to the radio; do not spread rumours; help neighbours |

**Tsunami.** A strong earthquake beneath the ocean can displace water and cause a huge sea wave, a **tsunami** (Japanese: "harbour wave"). It does not threaten Nepal directly, but the Indian Ocean tsunami of December 2004 killed more than 200,000 people in the countries around it.

::: caution Do not run during the shaking
Many injuries occur when people run out through doorways and stairs while the building is shaking. The correct action is *drop, cover and hold on*, and to go out only when the shaking stops.
:::

## 6.11 Map work

### What is a map?

A **map** is a drawing, to scale, of the whole or part of the Earth's surface on a flat sheet of paper, as seen from above. A **globe** is a model of the Earth that shows shapes and distances correctly; a map is easier to carry but always has some distortion.

| Type of map | Shows | Example |
|---|---|---|
| Physical | Mountains, rivers, plains | Relief map of Nepal |
| Political | Countries, boundaries, capitals | Map of South Asia |
| Thematic | One topic (rainfall, population, roads) | Population density map |
| Topographic | Detailed natural and man-made features, with contours | Survey Department 1:25,000 sheets |
| Cadastral | Land parcels, ownership | Land-registration (*naksa*) maps |

### Components of a map

Every good map has a **title**, a **scale**, a **direction** (north arrow), a **legend** (key) explaining the signs and colours, a **border** and **grid lines** (latitude and longitude), and a **source/date**.

### Scale

**Scale** is the ratio between a distance on the map and the real distance on the ground. It is shown in three ways:

1. **Statement:** "1 cm represents 5 km".
2. **Representative fraction (RF)**, a ratio with the same unit on both sides: 1 : 500,000.
3. **Graphical (linear) scale**, a ruler drawn on the map with ground distances marked.

::: example Converting a scale
**Problem.** Convert the statement scale "1 cm represents 5 km" into a representative fraction. On that map two towns are 7.5 cm apart. What is the real distance?

**Solution.** 5 km = 5 × 1,000 × 100 cm = 500,000 cm.
So 1 cm on the map = 500,000 cm on the ground, and the RF is **1 : 500,000**.
Real distance = 7.5 cm × 5 km = **37.5 km**.
:::

::: example Large-scale and small-scale
**Problem.** Which is the larger scale, 1 : 25,000 or 1 : 1,000,000?

**Solution.** Compare the fractions 1/25,000 and 1/1,000,000. The first is bigger, so **1 : 25,000 is the larger scale**. It shows a small area in great detail (a village); 1 : 1,000,000 is a small scale and shows a large area with little detail (a country).
:::

### Direction, grid and contours

- **Direction:** The four cardinal points are north, east, south and west; the intercardinal points are NE, SE, SW and NW. On most maps the top is north.
- **Grid reference:** the position of a place can be given by the number of the vertical (easting) line followed by the horizontal (northing) line, "read along the corridor, then up the stairs".
- **Contour lines** join places of the same height above sea level. They show relief: **closely spaced** contours mean a steep slope, **widely spaced** contours a gentle slope, **concentric closed rings** a hill, and **V-shapes pointing to higher ground** a valley.

```figure caption="Contour lines of a hill with a steep side (west) and a gentle side (east). Closely spaced lines mean a steep slope."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.0))
x = np.linspace(-4,6,200); y = np.linspace(-3,3,150)
X,Y = np.meshgrid(x,y)
Z = 500*np.exp(-((X-0)**2/(2*1.1**2)*np.where(X<0,1.6,0.08) + Y**2/(2*1.6**2)))
levels=[100,200,300,400]
cs = ax.contour(X,Y,Z,levels=levels,colors=[SERIES[3]],linewidths=1.1)
ax.clabel(cs, fmt="%d m", fontsize=7)
ax.plot([0],[0],'^',color=INK,ms=7)
ax.text(0.15,0.3,"Peak",fontsize=8,color=INK)
ax.text(-3.8,2.4,"Steep slope",fontsize=8,color=INK)
ax.text(2.5,2.4,"Gentle slope",fontsize=8,color=INK)
ax.set_aspect("equal"); ax.axis("off")
```

### Drawing a sketch map

1. Decide the area and draw a frame; mark **north**.
2. Choose a scale; mark fixed points: roads, river, school.
3. Use **conventional signs** (e.g. a cross for a church, a triangle for a hill, blue lines for rivers).
4. Add a title, legend and scale. A **sketch map** is a quick map of an area not made by exact measurement; a **plan** is drawn to scale.

::: tip Map questions
In the exam, always write the formula "Real distance = map distance × scale" and show units. If the question gives an RF, convert to km (divide cm by 100,000).
:::

## 6.12 Modern technology in mapping

Maps were once drawn by walking and measuring with chains, theodolites and plane tables. Today they are built from data collected from the air and from space.

| Technology | What it is | Use |
|---|---|---|
| **Aerial photography** | Photographs taken from aeroplanes or drones | Topographic maps, land use, damage after disasters |
| **Remote sensing** | Collecting information about the Earth from a distance using satellites and sensors | Weather forecasting, forest and crop monitoring, glacier and flood mapping (e.g. Landsat, Sentinel) |
| **GPS (Global Positioning System)** | A network of 24+ satellites that lets a receiver compute its exact position, height and time | Navigation, surveying, tracking vehicles, finding a trail |
| **GIS (Geographic Information System)** | Computer software that stores, analyses and displays map layers (roads, rivers, population) together | Planning schools and roads, disaster risk maps, municipal land records |
| **Online map tools** | Google Earth, OpenStreetMap, digital maps | Everyday directions; community mapping after the 2015 earthquake |

- **GPS** was developed by the United States (NAVSTAR); similar systems are GLONASS (Russia), Galileo (Europe), BeiDou (China) and NavIC (India), collectively called **GNSS**. A receiver needs signals from at least four satellites to fix latitude, longitude and height.
- **Nepal's Survey Department** uses aerial photography, satellite images and GPS to prepare topographic and cadastral maps; Nepali mappers on the OpenStreetMap platform drew thousands of buildings and roads in the days after the 2015 earthquake so that rescuers could find their way.
- **Drones** now provide cheap, very high-resolution images for municipal planning.

::: key Advantages of modern mapping
It is faster and cheaper, more accurate, easy to update, gives maps of places that are hard to reach (glaciers, jungles) and can overlay many kinds of information. Weaknesses: needs training and equipment, and electronic data can be misused if privacy is not protected.
:::

## Chapter summary

- **Weather** is the day-to-day condition of the atmosphere; **climate** is its long-term (30-year) average.
- Climate depends on **latitude, altitude (6.5 °C per 1,000 m), distance from the sea, ocean currents, winds, relief (rain shadow) and vegetation**.
- The world has **tropical** (equatorial, savanna, monsoon, hot desert), **temperate** (Mediterranean, China type, British type, grassland) and **cold** (taiga, tundra, ice cap) regions.
- Climate and relief decide vegetation, wildlife, population density, clothing, food and work. Monsoon plains hold the densest populations.
- North America (3rd, ~24.7 million km², Denali 6,190 m), South America (4th, ~17.8 million km², Aconcagua ~6,960 m, Amazon) and Africa (2nd, ~30.3 million km², Kilimanjaro 5,895 m, Nile, Sahara) differ in relief, climate and economy.
- An **earthquake** is the sudden shaking of the ground; **focus** is underground, **epicentre** is above it. Nepal sits on the Indian–Eurasian plate boundary; major quakes: 1934, 1988, 2015 (7.8).
- Safety: **Drop, Cover, Hold**; build to code; keep an emergency kit.
- A **map** has title, scale, direction, legend and border. Scale can be a statement, RF or graph. Contours show relief.
- Modern mapping uses **aerial photos, remote sensing, GPS and GIS**.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The average weather of a place over thirty or more years is called its <span class="marks">[1]</span>
   (a) season (b) climate (c) weather (d) temperature
2. Temperature falls by about 6.5 °C for every 1,000 m rise in <span class="marks">[1]</span>
   (a) latitude (b) longitude (c) altitude (d) humidity
3. Which climate has hot, dry summers and mild, rainy winters? <span class="marks">[1]</span>
   (a) Monsoon (b) Mediterranean (c) Tundra (d) Savanna
4. The longest river in Africa is the <span class="marks">[1]</span>
   (a) Congo (b) Niger (c) Zambezi (d) Nile
5. The highest peak of South America is <span class="marks">[1]</span>
   (a) Denali (b) Aconcagua (c) Kilimanjaro (d) Chimborazo
6. The point on the Earth's surface directly above the focus is the <span class="marks">[1]</span>
   (a) fault (b) epicentre (c) crater (d) hypocentre
7. A map with a scale of 1 : 25,000 is a <span class="marks">[1]</span>
   (a) small-scale map (b) large-scale map (c) sketch map (d) globe
8. Which system uses satellites to find a position on the Earth? <span class="marks">[1]</span>
   (a) GPS (b) CBS (c) ICT (d) UNESCO

::: note Answers to Group A
**1.** (b): climate is the long-term average.
**2.** (c): this is the normal lapse rate.
**3.** (b): the Mediterranean type is dry in summer, wet in winter.
**4.** (d): the Nile, about 6,650 km, is also the longest river in the world.
**5.** (b): Aconcagua, about 6,960 m, in Argentina.
**6.** (b): epicentre; the focus lies underground.
**7.** (b): the fraction 1/25,000 is larger than 1/1,000,000.
**8.** (a): GPS, the Global Positioning System.
:::

**Group B — Short answer (2 marks each)**

1. Differentiate between weather and climate. <span class="marks">[2]</span>
2. Why is the Terai warmer than Kathmandu? <span class="marks">[2]</span>
3. Name any two features of the equatorial climate. <span class="marks">[2]</span>
4. What is the rain-shadow effect? Give one example from Nepal. <span class="marks">[2]</span>
5. Why is Nepal at high risk of earthquakes? <span class="marks">[2]</span>
6. Convert the scale 1 cm = 2 km into an RF. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Weather is the short-term state of the atmosphere (hours or days); climate is the average weather of a region over thirty or more years.
**2.** The Terai is much lower (about 100 m) than Kathmandu (about 1,400 m); temperature falls about 6.5 °C per 1,000 m, so the Terai is hotter.
**3.** Hot and wet all year (about 27 °C, over 200 cm of rain with daily afternoon showers) and dense evergreen rainforest.
**4.** Moist wind rises over mountains and drops rain on the windward side, leaving the leeward side dry. Mustang lies in the rain shadow of the Annapurna–Dhaulagiri ranges.
**5.** Nepal lies on the boundary of the Indian and Eurasian plates; the Indian Plate keeps pushing north at 4 to 5 cm a year, storing strain that is released as earthquakes.
**6.** 2 km = 200,000 cm, so RF = 1 : 200,000.
:::

**Group C — Long answer (4 marks each)**

1. Describe the savanna climate under location, climate, vegetation and human life. <span class="marks">[4]</span>
2. Explain any four factors that affect the climate of a place with examples. <span class="marks">[4]</span>
3. Describe the physical features and economic activities of Africa. <span class="marks">[4]</span>
4. What should we do before, during and after an earthquake? Write four measures in all. <span class="marks">[4]</span>
5. What are the uses of GPS, remote sensing and GIS in mapping? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Savanna lies about 5° to 20° (up to 30°) north and south of the equator: Sudan and East Africa, the Llanos and Campos in South America, northern Australia. Climate: hot all year, wet summer and long dry winter, rain 75–150 cm. Vegetation: tall elephant grass and umbrella-shaped acacia and baobab. People: herders such as the Maasai, farming of maize and millet, wildlife tourism (lion, elephant, zebra).
**2.** Latitude (hotter near the equator); altitude (cooler by 6.5 °C per 1,000 m: Kathmandu vs Birgunj); distance from the sea (maritime vs continental: Mumbai vs Nagpur); winds and relief (monsoon rain on windward slopes of the Himalaya, rain shadow of Mustang). Ocean currents and vegetation also matter.
**3.** Features: Sahara, Kalahari and Namib deserts; Nile, Congo, Niger; Kilimanjaro; Great Rift Valley; Lake Victoria; Victoria Falls. Economy: subsistence farming, cash crops (cocoa, coffee, tea, cotton), minerals (gold, diamonds, copper, oil), tourism.
**4.** Before: build by the code, keep an emergency kit, practise drop–cover–hold. During: drop, take cover under a table, stay away from windows; outdoors go to open ground. After: check injuries, expect aftershocks, leave damaged buildings, switch off gas and power and listen to the radio.
**5.** GPS gives exact position and elevation for surveying and navigation; remote sensing (satellites, aerial photos) gives images for land use, forests, floods and glaciers; GIS stores and combines map layers for planning, disaster maps and land records. Together they make maps faster, cheaper, more accurate and easy to update.
:::


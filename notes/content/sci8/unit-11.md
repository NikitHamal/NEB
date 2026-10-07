---
subject: Science and Technology
grade: 8
unit: 11
title: The Earth and Universe
hours: 0
area: Science and Technology
---

Earth is a planet with air, liquid water and many forms of life. Weather changes from day to day, while Earth's movements and tilt help create regular patterns such as day and night and the seasons. Looking at the Moon and planets expands our view beyond Earth; studying hazards and resources helps us care for the place where we live.

::: key Weather is not climate
**Weather** describes the conditions of the atmosphere at a particular place and time. **Climate** describes patterns of weather over many years. A cold day does not by itself show that a region's climate has changed.
:::

## 11.1 Earth systems, weather, seasons and the solar system

Earth has connected systems. The **atmosphere** is the layer of gases around Earth; the **hydrosphere** includes water in oceans, rivers, ice and underground; the **geosphere** includes rocks, soil and landforms; and the **biosphere** includes living things. A change in one system can affect others: heavy rain in the atmosphere can cause a river in the hydrosphere to rise, erode soil and affect organisms.

Weather observations include air temperature, cloud cover, rainfall, wind direction and wind speed. A rain gauge collects rain so its depth can be measured; a thermometer measures temperature. Record the place, date, time and units so observations can be compared fairly. Forecasts use observations and models to estimate likely conditions; they are useful but can be uncertain.

Earth rotates once in about 24 hours, giving most places a cycle of day and night. Earth takes about one year to orbit the Sun. Earth's axis is tilted relative to its orbit and points in nearly the same direction as Earth travels around the Sun. This tilt changes the angle and length of sunlight in each hemisphere during the year, causing seasons. Seasons are not caused mainly by Earth being closer to or farther from the Sun.

```figure caption="Earth's axis keeps the same tilt as it orbits the Sun; sunlight and seasons are simplified and not to scale."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(4.9, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Circle((5,3),0.42,fc="#ffd86b",ec="#d99b28",lw=1.0))
ax.text(5,2.25,"Sun",ha="center",fontsize=7.5,color=INK)
ax.annotate("",xy=(2.65,3.0),xytext=(4.55,3.0),arrowprops=dict(arrowstyle="->",color=SERIES[2],lw=1.0))
ax.annotate("",xy=(7.35,3.0),xytext=(5.45,3.0),arrowprops=dict(arrowstyle="->",color=SERIES[2],lw=1.0))
for cx,label in [(2.0,"Northern winter"),(8.0,"Northern summer")]:
    ax.add_patch(Circle((cx,3),0.58,fc="#83b9dc",ec=ACCENT,lw=1.0))
    ax.plot([cx+0.35,cx-0.35],[2.4,3.6],color=INK,lw=1.0)
    ax.add_patch(FancyArrowPatch((cx+0.15,2.75),(cx-0.32,3.55),arrowstyle="-|>",mutation_scale=8,color=SERIES[4],lw=1.1))
    ax.text(cx-0.52,3.76,"N",fontsize=7,color=SERIES[4])
    ax.text(cx,1.85,label,ha="center",fontsize=7,color=INK)
ax.text(5,5.25,"Axis tilt changes sunlight angle and day length",ha="center",fontsize=7,color=MUTED)
fig.tight_layout()
```

The solar system has the Sun at its centre and eight recognised planets orbiting it: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune. The four inner planets are rocky; Jupiter and Saturn are gas giants, while Uranus and Neptune are ice giants. The planets differ greatly in size and distance, so a classroom drawing is usually not to scale. Many planets have moons, and smaller objects such as asteroids also orbit the Sun.

::: example Read a weather record
**Problem.** A class records morning temperatures for three days: 18 °C, 20 °C and 17 °C. What is the highest recorded temperature, and can these values alone describe the local climate?

**Solution.** The highest reading is **20 °C**. Three morning readings describe a small sample of weather; they are not enough to describe climate, which uses patterns collected over many years and considers more than one weather measure.
:::

## 11.2 The Moon, planets, stars and observations of the sky

The Moon is Earth's natural satellite. It does not make its own visible light; sunlight reflects from its surface. As the Moon orbits Earth, we see different portions of its sunlit half, producing phases such as new Moon, crescent, quarter and full Moon. The phases are not usually caused by Earth's shadow. Earth's shadow on the Moon occurs during a lunar eclipse, which is less frequent.

The planets appear bright because they reflect sunlight. Stars produce their own light and are extremely far away; the Sun is the star closest to Earth. A planet can appear to move against the background stars over weeks or months because it orbits the Sun and Earth is also moving. Constellations are patterns people identify in the sky; the stars in a pattern may be at very different distances from Earth.

Observe the sky from a safe location and record the date, time, direction and conditions. Never look directly at the Sun with eyes, binoculars or an unfiltered telescope. Use a teacher-approved indirect viewing method for any solar observation. Light pollution from bright outdoor lamps can make faint stars harder to see, so shielding lights and using only the brightness needed helps people and wildlife.

```figure caption="The planets orbit the Sun in an approximate order; spacing and sizes are not to scale."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.9, 2.6))
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
ax.add_patch(Circle((1.0,2.5),0.28,fc="#f5c94e",ec="#d99b28",lw=0.8))
ax.text(1.0,1.9,"Sun",ha="center",fontsize=7,color=INK)
planets=[("Mercury",2.3), ("Venus",3.55), ("Earth",4.8), ("Mars",6.05), ("Jupiter",7.4), ("Saturn",8.7), ("Uranus",10.0), ("Neptune",11.2)]
for i,(name,x) in enumerate(planets):
    size=0.10 if i<4 else (0.17 if i<6 else 0.14)
    ax.add_patch(Circle((x,2.5),size,fc=SERIES[i%len(SERIES)],ec="white",lw=0.4))
    ax.text(x,2.0,name,ha="center",fontsize=6.2,color=INK,rotation=35)
    ax.plot([x,x],[2.5,2.75+0.06*(i%2)],color=GRID,lw=0.7)
ax.annotate("orbiting outward",xy=(11.5,3.5),xytext=(2,3.5),ha="center",fontsize=7,color=MUTED,arrowprops=dict(arrowstyle="->",color=MUTED,lw=0.8))
ax.text(6.5,0.65,"Sizes and distances are not to scale",ha="center",fontsize=7,color=MUTED)
fig.tight_layout()
```

::: example Explain the Moon's phases
**Problem.** Why does a full Moon look bright, and why is it not full every night?

**Solution.** Sunlight reflects from the Moon. As the Moon orbits Earth, the angle between the Sun, Moon and observer changes, so we see different portions of its sunlit half. At full Moon, most of the visible face is illuminated; at other times, only part of that face is visible from Earth.
:::

## 11.3 Natural resources, hazards and responsible stewardship

Natural resources include soil, fresh water, forests, minerals, sunlight and fuels. Some resources renew on human time scales if managed carefully; others, such as fossil fuels and many mineral deposits, form too slowly to replace what people use. Responsible stewardship means using resources thoughtfully, preventing pollution, protecting habitats and considering how present choices affect future communities.

Natural hazards include earthquakes, landslides, floods, storms, droughts and lightning. A hazard can cause harm when people or infrastructure are exposed and vulnerable. Local risk depends on location, building design, land use, warning systems and preparedness. Follow official local alerts, learn safe routes and practise the plan provided by school or community authorities. Do not enter floodwater, approach a landslide or stand under a tree during lightning to collect observations.

Households and schools can conserve water, reduce litter, protect vegetation and use energy efficiently. Trees and healthy slopes can help reduce erosion, but planting alone cannot prevent every landslide or flood. Community plans should use local knowledge and advice from relevant experts rather than promising that one action removes all risk.

::: example Make a safe weather observation
**Problem.** A class wants to compare rainfall at school over one month. Suggest a safe method and one limitation.

**Solution.** Place a suitable rain gauge in an open, secure location away from roofs and trees, read it at the same time each day, record the date and rainfall depth in millimetres, and ask an adult to help with placement. A single gauge describes only that location; nearby places may receive different rainfall.
:::

::: example Prepare for a local hazard
**Problem.** Heavy rain may cause flooding near a school. Name two safe preparations that students can make with adults.

**Solution.** Learn the school's official evacuation route and meeting place, and keep emergency contact information available through approved channels. Listen to local warnings and avoid low-lying roads or floodwater. Students should not attempt to rescue people or belongings from moving water; alert trained adults and emergency services.
:::

::: caution Never observe the Sun directly
Looking at the Sun through binoculars, a telescope or an unfiltered camera can permanently damage eyesight. Use only a teacher-approved indirect method with proper equipment, or study a safe image supplied by a trusted source.
:::

## Chapter summary

- The atmosphere, hydrosphere, geosphere and biosphere interact; changes in one can affect the others.
- Weather is short-term atmospheric condition; climate describes long-term patterns.
- Earth's rotation causes day and night; its orbit and tilted axis create seasonal patterns.
- The Moon reflects sunlight; its phases result from the changing view of its illuminated half.
- Planets orbit the Sun and reflect its light; stars produce their own light.
- Natural resources require responsible use, while hazard safety depends on local warnings and preparation.

## Practice questions

1. What causes the regular cycle of day and night? (a) Moon phases (b) Earth's rotation (c) Earth's seasons (d) clouds
2. Is a single rainy afternoon a description of weather or climate?
3. Why does the Moon appear bright to us?
4. Name one natural hazard that may affect a community.

::: note Answers to questions 1–4
**1.** (b) — Earth rotates about its axis in roughly 24 hours.
**2.** Weather — it describes a particular time and place.
**3.** It reflects sunlight toward Earth.
**4.** Examples: flood, landslide, earthquake, storm, drought or lightning.
:::

5. Name the four Earth systems and give one example of an interaction between two of them.
6. Explain why seasons are not caused mainly by Earth being closer to the Sun.
7. Describe one difference between a planet and a star.
8. State two safe actions students can take when heavy rain threatens flooding.

::: note Answers to questions 5–8
**5.** Atmosphere, hydrosphere, geosphere and biosphere. Example: rainfall in the atmosphere fills a river and can erode soil.
**6.** Earth's axis is tilted and keeps nearly the same direction during its orbit, changing sunlight angle and day length between hemispheres.
**7.** A planet orbits a star and reflects its light; a star produces its own light.
**8.** Follow official alerts, learn the school's evacuation route, stay away from floodwater and alert an adult. Any two safe actions are acceptable.
:::

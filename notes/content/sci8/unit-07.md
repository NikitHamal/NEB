---
subject: Science and Technology
grade: 8
unit: 7
title: Energy in Daily Life
hours: 0
area: Science and Technology
---

Energy is needed to move vehicles, cook food, light rooms and run devices. It appears in different forms and can be transferred from one object or place to another. Comparing energy sources and reducing waste help families and communities meet their needs while protecting the environment.

::: key Energy changes form; it does not appear from nowhere
In an energy transfer, energy moves between objects or changes form. In a lamp, electrical energy is transferred mainly to light and thermal energy. Useful output and unwanted heating can occur together.
:::

## 7.1 Forms, transfer and transformation of energy

Common forms include **kinetic energy** of moving objects, **gravitational potential energy** due to height, **chemical energy** stored in fuels and food, **thermal energy** related to particle motion, **sound energy**, **light energy** and **electrical energy**. The word “stored” describes energy available to be transferred; it does not mean the energy is a material substance inside an object.

Energy is transferred by heating, light, sound, electrical current or forces doing work. A falling stone transfers gravitational potential energy into kinetic energy. When it hits the ground, some energy becomes sound, heating and deformation. Energy is conserved overall, although some spreads into the surroundings and is less useful for the original task.

```figure caption="A battery-powered lamp transfers chemical energy through an electrical circuit to light and heating."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.6))
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
labels=[("Battery\nchemical",0.5),("Electrical\ntransfer",3.4),("Lamp",6.4),("Light",9.1),("Heating",9.1)]
ys=[3.2,3.2,3.2,3.8,1.3]
for (label,x),y in zip(labels,ys):
    ax.add_patch(FancyBboxPatch((x,y),2.0,0.8,boxstyle="round,pad=0.06",fc="#fff4dd" if "Light" in label or "Heating" in label else "#eef3fb",ec=ACCENT,lw=1.0))
    ax.text(x+1,y+0.4,label,ha="center",va="center",fontsize=7.2,color=INK)
for a,b in [((2.6,3.6),(3.25,3.6)),((5.5,3.6),(6.25,3.6)),((8.5,3.6),(9.0,4.0)),((8.5,3.4),(9.0,1.8))]:
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=SERIES[2],lw=1.1))
fig.tight_layout()
```

::: example Trace energy changes
**Problem.** A ball is released from a raised shelf and bounces on the floor. Name two energy changes.

**Solution.** As the ball falls, gravitational potential energy decreases while kinetic energy increases. On impact, kinetic energy is transferred into sound, heating and temporary deformation. As the ball rises after bouncing, some kinetic energy becomes gravitational potential energy. The ball does not return to its original height because some energy spreads to the surroundings.
:::

## 7.2 Renewable and non-renewable sources

An **energy source** is something from which useful energy can be obtained. Solar radiation, moving air, flowing water and geothermal heat are renewable sources on human time scales when managed appropriately. Biomass can be renewable if plants regrow and harvesting does not exceed renewal. Coal, petroleum and natural gas are fossil fuels formed over very long periods; they are non-renewable resources that can run out.

Each source has benefits and limits. Solar panels generate electricity when sunlight is available, but output varies with weather and time of day. Hydropower can provide electricity but dams change river habitats and land use. Fossil fuels can provide energy when needed but burning them releases air pollutants and carbon dioxide. A good choice considers reliability, cost, local conditions, safety and environmental effects, not one label alone.

::: example Compare two cooking options
**Problem.** A family can use a well-maintained electric hotplate or burn damp firewood in a poorly ventilated room. Give one reason the hotplate may be safer indoors and one broader factor to consider.

**Solution.** The hotplate does not release smoke into the room at its point of use, while burning damp wood can produce harmful smoke and gases. The family should also consider the electricity source, cost, reliability and safe wiring. Any heater or stove must be used according to instructions; never block ventilation or leave a flame unattended.
:::

## 7.3 Efficient use and conservation

**Energy efficiency** compares useful energy output with total energy input. A more efficient device transfers a larger share of input into the intended task, though some energy still spreads to the surroundings. Insulation slows unwanted heat transfer from a warm room or hot-water container. Switching off unused lights and devices, using daylight and selecting efficient appliances can reduce energy use.

The kilowatt-hour (kWh) is a unit of electrical energy used for household bills. One kilowatt-hour is the energy used by a 1 kW appliance operating for 1 hour; 1 kWh = 3.6 megajoules. For example, a 100 W lamp is 0.1 kW. If it is on for 5 hours, it uses 0.1 kW × 5 h = 0.5 kWh. A lower bill may result from using less energy, but electricity costs and household needs differ.

```figure caption="Simple choices reduce avoidable energy use while keeping the service people need."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.7, 2.7))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
items=[("Use daylight",(0.6,4.0)),("Switch off\nunused devices",(3.8,4.0)),("Reduce heat\nloss",(7.0,4.0)),("Choose an\nefficient device",(3.8,1.0))]
for label,(x,y) in items:
    ax.add_patch(FancyBboxPatch((x,y),2.3,1.0,boxstyle="round,pad=0.08",fc="#eef5e8",ec=SERIES[2],lw=1.0))
    ax.text(x+1.15,y+0.5,label,ha="center",va="center",fontsize=7.4,color=INK)
for a,b in [((2.95,4.5),(3.7,4.5)),((6.15,4.5),(6.9,4.5)),((5.0,3.9),(5.0,2.1))]:
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.0))
ax.text(5,0.35,"Less wasted energy for the same useful task",ha="center",fontsize=7,color=MUTED)
fig.tight_layout()
```

::: example Estimate household energy use
**Problem.** A 200 W fan runs for 3 hours. How much electrical energy does it use in kWh?

**Solution.** Convert power: 200 W = 0.2 kW. Energy = power × time = 0.2 kW × 3 h = **0.6 kWh**. This is energy used, not the cost; the bill depends on the local tariff.
:::

::: caution Saving energy does not mean sacrificing safety
Do not switch off a device that someone needs for safety or health, block ventilation to save heat, or overload a socket. Choose safe ways to reduce avoidable use and follow appliance instructions.
:::

## Chapter summary

- Energy occurs in forms such as kinetic, gravitational potential, chemical, thermal, sound, light and electrical.
- Energy is transferred or transformed and is conserved overall; some spreads into less useful forms.
- Solar, wind and flowing water are renewable sources; fossil fuels are non-renewable.
- Every source has limits and environmental effects that should be considered.
- Efficient devices provide more useful output for the same input; insulation reduces unwanted heat transfer.
- Electrical energy use in kWh = power in kW × time in hours; 1 kWh = 3.6 MJ.

## Practice questions

1. Which is a non-renewable source? (a) sunlight (b) wind (c) coal (d) flowing water
2. What energy form is associated with a moving bicycle?
3. A 1 kW heater runs for 2 h. How much energy does it use?
4. Name one way to reduce avoidable energy use at home.

::: note Answers to questions 1–4
**1.** (c) — coal takes millions of years to form and is not renewed on a human time scale.
**2.** Kinetic energy.
**3.** 1 kW × 2 h = 2 kWh.
**4.** Examples: switch off unused lights, use daylight, insulate a hot-water container or select an efficient appliance.
:::

5. Describe the main energy changes in a torch switched on with a battery.
6. Give one benefit and one limitation of solar electricity.
7. A 500 W appliance runs for 4 h. Calculate its energy use in kWh.
8. Explain why energy conservation can help both a household and the environment.

::: note Answers to questions 5–8
**5.** Chemical energy in the battery is transferred electrically to the lamp and becomes light and thermal energy.
**6.** Benefit: sunlight is renewable and the panel produces no smoke at its point of use. Limitation: output depends on sunlight and may require storage or another source.
**7.** 500 W = 0.5 kW; energy = 0.5 kW × 4 h = 2 kWh.
**8.** Using less energy can lower household costs and reduce demand for fuel or electricity generation, which may reduce pollution and resource use.
:::

---
subject: Science and Technology
grade: 8
unit: 6
title: Force and Motion
hours: 0
area: Science and Technology
---

Motion describes how an object's position changes. To explain motion, we measure distance or displacement over time. A force can change an object's speed, direction or shape, while friction and gravity affect the motion we see every day. These ideas help us understand transport, sports and safe use of tools.

::: key Describe a motion with a reference point
An object is in motion when its position changes relative to a chosen reference point. Distance is the total path travelled; displacement is the change from the starting point to the finishing point in a stated direction.
:::

## 6.1 Distance, displacement, speed and motion graphs

**Distance** is the length of the path travelled and has no direction. **Displacement** is the straight-line change from the initial position to the final position, with direction. If a student walks 300 m east and then 100 m west, the distance is 400 m but the displacement is 200 m east.

Average **speed** is distance divided by time. Its SI unit is metres per second (m s⁻¹); kilometres per hour (km h⁻¹) is also used for travel. Convert units before comparing: 1 km = 1,000 m and 1 h = 3,600 s. Speed describes how fast an object moves, not its direction. An object may change speed during a journey, so average speed does not tell every detail of the motion.

A distance–time graph shows how distance from a reference point changes. A straight rising line means steady speed; a horizontal line means the distance is not changing during that interval. A steeper line represents a greater speed when the axes use the same scale. Do not confuse a distance–time graph with a picture of the object's path.

```figure caption="A straight distance–time line shows constant speed; a horizontal part shows rest."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.8))
ax.plot([0,2,4,6],[0,20,40,40],marker="o",color=ACCENT,lw=2)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Distance from start (m)")
ax.set_xlim(0,6); ax.set_ylim(0,45); ax.set_xticks([0,2,4,6]); ax.set_yticks([0,10,20,30,40])
ax.grid(color=GRID,lw=0.7); ax.spines[["top","right"]].set_visible(False)
fig.tight_layout()
```

::: example Calculate average speed
**Problem.** A student cycles 600 m in 120 s. Find the average speed.

**Solution.** Average speed = distance ÷ time = 600 m ÷ 120 s = **5 m s⁻¹**. The unit follows from metres divided by seconds.
:::

::: example Compare distance and displacement
**Problem.** A person walks 3 km north, then 4 km south. Find the total distance and displacement.

**Solution.** Distance = 3 km + 4 km = **7 km**. The final position is 1 km south of the start, so displacement is **1 km south**. Distance is the total route; displacement includes direction.
:::

## 6.2 Forces, friction, gravity and balanced forces

A **force** is a push or pull. Forces can change motion or deform an object. A force has both size and direction and is measured in newtons (N). **Gravity** attracts objects toward Earth; it gives unsupported objects weight. **Friction** acts between surfaces in contact and usually opposes their relative motion. Air resistance is a type of friction acting on an object moving through air.

When forces on an object are **balanced**, their combined effect is zero: an object at rest stays at rest, and a moving object continues at constant velocity unless another force changes the balance. When forces are **unbalanced**, the object's motion can change. A book resting on a table has gravity downward and a supporting contact force upward; the forces balance while it remains at rest.

Friction can be useful: it lets shoes grip the ground, brakes slow a bicycle and a pencil mark paper. Too much friction can wear surfaces and waste energy as heat. Lubricants reduce friction between moving parts. Smooth tyres, wet floors and worn shoe soles can reduce grip, so safe movement depends on appropriate friction.

```figure caption="Forces on a box resting on a level table: the upward support balances its weight."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(4.4, 2.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
ax.add_patch(Rectangle((3.5,2.2),3.0,1.8,fc="#eef3fb",ec=ACCENT,lw=1.2))
ax.plot([1.8,8.2],[2.15,2.15],color=INK,lw=1.5)
ax.add_patch(FancyArrowPatch((5,4.0),(5,6.0),arrowstyle="-|>",mutation_scale=14,color=SERIES[2],lw=1.8))
ax.add_patch(FancyArrowPatch((5,2.2),(5,0.45),arrowstyle="-|>",mutation_scale=14,color=SERIES[4],lw=1.8))
ax.text(5.3,5.4,"support force",fontsize=8,color=SERIES[2])
ax.text(5.3,0.9,"weight (gravity)",fontsize=8,color=SERIES[4])
ax.text(5,3.05,"box",ha="center",va="center",fontsize=9,color=INK)
fig.tight_layout()
```

::: example Find an unknown force in balance
**Problem.** A sign hangs at rest. Its weight is 18 N downward. What is the size and direction of the support force from the rope, if the forces are balanced?

**Solution.** Balanced forces have equal sizes in opposite directions. The rope pulls **18 N upward**, balancing the 18 N weight downward. The resultant force is zero while the sign remains at rest.
:::

::: example Choose where friction helps
**Problem.** Why does a bicycle need both tyre grip and working brakes? Give one way to improve safe grip on a wet path.

**Solution.** Tyre friction helps the bicycle grip the road and turn; brake friction reduces its speed. On a wet path, ride slowly, leave more stopping distance and avoid sudden turns. A rider should use a suitable helmet and obey local safety rules; no tyre can remove every risk.
:::

## 6.3 Safe applications in transport and everyday tools

A seat belt helps restrain a passenger if a vehicle slows suddenly. A helmet reduces the risk of serious head injury in many crashes, though it cannot prevent every injury. Reflective clothing and lights help others see a person in poor light. Keep a safe distance, cross at a suitable place and follow local traffic directions. Never test forces by pushing people, standing in a moving vehicle or using an unsafe ramp.

Simple tools change how a force is applied. A lever can help lift a load, a wheel and axle can help move it, and a ramp spreads the effort over a longer distance. Tools do not create energy: they trade force, distance or direction. Use a tool only for its intended job and ask an adult before handling sharp, heavy or powered equipment.

::: caution Mass and weight are different
Mass describes the amount of matter and is measured in kilograms (kg). Weight is a gravitational force and is measured in newtons (N). A scale may display mass in everyday use, but the scientific terms and units are not interchangeable.
:::

## Chapter summary

- Distance is total path length; displacement is the change in position with direction.
- Average speed = distance ÷ time; convert units before comparing speeds.
- A distance–time graph's slope indicates speed; a flat section means distance is not changing.
- Forces are pushes or pulls measured in newtons; gravity attracts objects toward Earth.
- Balanced forces have zero resultant; unbalanced forces can change motion.
- Friction can provide grip and braking, but excessive friction can wear surfaces or waste energy.
- Safe transport uses restraints, visibility, distance and suitable protective equipment.

## Practice questions

1. A runner travels 100 m in 20 s. What is the average speed? (a) 2 m s⁻¹ (b) 5 m s⁻¹ (c) 20 m s⁻¹ (d) 2,000 m s⁻¹
2. Which unit measures force? (a) kg (b) m (c) N (d) s
3. What does a horizontal section on a distance–time graph show?
4. Name one situation where friction is useful.

::: note Answers to questions 1–4
**1.** (b) — 100 m ÷ 20 s = 5 m s⁻¹.
**2.** (c) — force is measured in newtons (N).
**3.** Distance from the reference point is not changing during that interval; the object is at rest relative to it.
**4.** Examples: walking grip, bicycle braking, tyre grip or writing with a pencil.
:::

5. A child walks 50 m east and 20 m west. Find the distance and displacement.
6. Explain why a book at rest on a table is not force-free.
7. Give one advantage and one disadvantage of friction.
8. State two safety measures for a person cycling on a road.

::: note Answers to questions 5–8
**5.** Distance = 70 m. Displacement = 30 m east.
**6.** Gravity pulls downward and the table exerts an upward support force; these forces balance.
**7.** Advantage: it provides grip or braking. Disadvantage: it can wear surfaces or produce unwanted heating.
**8.** Any two: wear a suitable helmet, use lights or reflective clothing, obey traffic rules, keep distance and ride at a safe speed.
:::

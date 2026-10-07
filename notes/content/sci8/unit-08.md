---
subject: Science and Technology
grade: 8
unit: 8
title: Electricity and Magnetism
hours: 0
area: Science and Technology
---

Electricity and magnetism are useful in lights, bells, motors and communication devices. A simple electrical circuit must provide a complete path for current. Materials differ in how easily current passes through them, and magnets exert forces without touching. Safe handling matters because household mains electricity can cause severe injury.

::: key A circuit needs a complete conducting path
A cell provides energy to a circuit. Current flows only when there is a complete conducting loop. A switch opens or closes that path; a lamp lights only when the circuit is connected properly and the lamp works.
:::

## 8.1 Electric charge, cells, circuits and conductors

Electric charge is a property of matter. In ordinary circuits, moving electrons in conducting wires help carry charge. A **cell** converts stored chemical energy into electrical energy that can drive current around a circuit. A battery is one cell or a group of connected cells. Cells have positive and negative terminals; use the correct orientation for a device.

A circuit is a continuous path containing a source and components joined by conductors. A lamp, buzzer or motor can act as a load that changes electrical energy into another form. A metal wire usually conducts electricity well. Plastic, dry wood and rubber are usually insulators in everyday conditions and can cover wires or tool handles. Water containing dissolved substances can conduct, so wet hands and electricity are a dangerous combination.

```figure caption="A closed low-voltage circuit with a cell, switch and lamp."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.6, 2.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
# Wire segments leave a visible space for the closed switch symbol.
ax.plot([2,2,4.2],[1.2,4.8,4.8],color=INK,lw=1.6)
ax.plot([5.0,7.5,7.5,2],[4.8,4.8,1.2,1.2],color=INK,lw=1.6)
# Cell symbol on lower wire.
ax.plot([3.4,3.4],[0.95,1.45],color=ACCENT,lw=1.2); ax.plot([3.8,3.8],[0.8,1.6],color=ACCENT,lw=2.2)
ax.text(3.25,0.45,"−",fontsize=9,color=INK); ax.text(3.75,0.45,"+",fontsize=9,color=INK)
# Lamp symbol on right side.
ax.add_patch(Circle((7.5,3.0),0.52,fc="#fff4dd",ec=ACCENT,lw=1.4))
ax.plot([7.15,7.85],[2.65,3.35],color=ACCENT,lw=1.2); ax.plot([7.15,7.85],[3.35,2.65],color=ACCENT,lw=1.2)
# Closed switch: two terminals joined by a conducting blade.
ax.add_patch(Circle((4.2,4.8),0.07,fc=ACCENT,ec=ACCENT))
ax.add_patch(Circle((5.0,4.8),0.07,fc=ACCENT,ec=ACCENT))
ax.plot([4.2,5.0],[4.8,4.8],color=ACCENT,lw=1.5)
ax.text(5.9,5.25,"closed switch",fontsize=7,color=MUTED)
ax.text(7.5,1.95,"lamp",ha="center",fontsize=7,color=MUTED)
ax.text(3.6,1.85,"cell",ha="center",fontsize=7,color=MUTED)
fig.tight_layout()
```

::: example Find the fault in a circuit
**Problem.** A lamp connected to one cell does not light. The wires are attached correctly, but the switch is open. What should happen when the switch is safely closed?

**Solution.** Closing the switch completes the conducting path. If the cell, lamp and wires are working and correctly connected, current can flow and the lamp should light. If it still does not, check the circuit under teacher supervision; never connect bare wires directly across a cell for a long time.
:::

## 8.2 Current, simple circuit diagrams and electrical safety

**Electric current** is the rate at which electric charge flows through a point in a circuit. It is measured in amperes (A). A simple circuit diagram uses agreed symbols for cells, wires, switches and components. A diagram shows how parts connect, not their actual size or position. In a series circuit, components share one path; if that path breaks, current stops throughout the loop.

Use only a teacher-approved low-voltage cell for classroom circuit work. Never experiment with wall sockets, damaged cords, exposed wires or power lines. Keep electricity away from water, disconnect a cell before changing a circuit, and do not place metal objects in a socket. If an electrical accident occurs, do not touch the person while the source may still be live; alert an adult and emergency services immediately.

::: example Read a simple series circuit
**Problem.** Two lamps are connected in one series loop. One lamp is removed and the circuit becomes open. What happens to the other lamp?

**Solution.** The single current path is broken, so current cannot flow through the loop. The remaining lamp also goes out. A parallel circuit has separate branches, so a break in one branch need not stop current in another, but household wiring must only be installed by qualified people.
:::

## 8.3 Magnets, magnetic effects and useful devices

A magnet has two poles, called north and south. Like poles repel and unlike poles attract. A magnet attracts some materials, including iron and many steels, but it does not attract every metal. The magnetic force is strongest near the poles. If a bar magnet is freely suspended, it tends to line up approximately north–south with Earth's magnetic field.

A magnetic field is the region where a magnetic force can be detected. Field lines are a model: outside a bar magnet, arrows point from the north pole toward the south pole, and closer lines indicate a stronger field. A compass needle is a small magnet that turns to align with the local field. Earth acts approximately like a large magnet, though its magnetic poles do not exactly match the geographic poles.

An **electromagnet** is made when current flows through a coil of wire, often around an iron core. Switching off the current usually removes much of its magnetism. Electromagnets are used in devices such as electric bells, relays and lifting magnets. A current-carrying coil can also produce motion in an electric motor; motors convert electrical energy into movement.

```figure caption="A simplified magnetic field pattern around a bar magnet; the outside arrows point from north to south."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8, 2.8))
ax.set_xlim(-4,4); ax.set_ylim(-2.6,2.6); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((-1.5,-0.42),3.0,0.84,fc="#eef3fb",ec=ACCENT,lw=1.2))
ax.text(-0.82,0,"N",ha="center",va="center",fontsize=10,color=INK,weight="bold")
ax.text(0.82,0,"S",ha="center",va="center",fontsize=10,color=INK,weight="bold")
for y in [-1.8,-1.2,1.2,1.8]:
    ax.annotate("",xy=(1.85,y),xytext=(-1.85,y),arrowprops=dict(arrowstyle="->",color=SERIES[2],lw=0.9,connectionstyle=f"arc3,rad={0.2 if y>0 else -0.2}"))
for x in [-2.2,2.2]:
    start,end=((x,-0.85),(x,0.85)) if x<0 else ((x,0.85),(x,-0.85))
    ax.annotate("",xy=end,xytext=start,arrowprops=dict(arrowstyle="->",color=MUTED,lw=0.8,connectionstyle="arc3,rad=0.35"))
fig.tight_layout()
```

::: example Test an unknown bar
**Problem.** A student brings a bar that may be iron or aluminium. Suggest a safe test using a magnet and explain what a positive result means.

**Solution.** Bring a classroom magnet close to the bar without striking it. If the bar is attracted, it may contain iron or a magnetic steel; the test does not prove that it is pure iron. Aluminium is not attracted strongly by an ordinary classroom magnet. Record the result and do not use the magnet near sensitive electronics or medical devices.
:::

::: caution A magnet attracts some metals, not all metals
Iron and many steels are magnetic, while aluminium and copper are not attracted in the same way by an ordinary bar magnet. Test a sample rather than assuming every metal is magnetic.
:::

## Chapter summary

- Electric charge is a property of matter; a cell provides energy that can drive current in a circuit.
- A complete conducting path is needed for current; conductors allow charge to flow more easily than insulators.
- Current is measured in amperes; a series path is broken if one connection opens.
- Use low-voltage cells for supervised experiments and keep all household mains electricity out of classroom tests.
- Magnets have north and south poles; like poles repel and unlike poles attract.
- Magnetic field models show direction and relative strength; electromagnets use current in a coil and have useful applications.

## Practice questions

1. What is needed for a current to flow in a simple circuit? (a) open path (b) complete conducting path (c) wooden path (d) no cell
2. Name one good electrical conductor.
3. Which poles attract? (a) north and north (b) south and south (c) north and south (d) all poles repel
4. What happens to a series circuit when its only path is broken?

::: note Answers to questions 1–4
**1.** (b) — the circuit must have a complete conducting path and a source.
**2.** Copper or aluminium wire is a common conductor.
**3.** (c) — unlike poles attract.
**4.** Current stops in the loop and its components no longer operate.
:::

5. Explain one difference between a conductor and an insulator.
6. Why must students never test a circuit using a household wall socket?
7. Describe how an electromagnet can be switched on and off.
8. A compass is placed near a bar magnet. What may happen when the compass is turned, and why?

::: note Answers to questions 5–8
**5.** A conductor lets charge flow more easily; an insulator resists charge flow and is often used as a protective covering.
**6.** Mains electricity can cause severe injury or death; classroom tests should use only teacher-approved low-voltage cells.
**7.** Current through a coil makes it magnetic; opening the circuit stops current and removes most of the electromagnet's magnetism.
**8.** The needle turns to align with the magnetic field at its location. Its direction changes as the compass is moved around the magnet.
:::

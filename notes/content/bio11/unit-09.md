---
subject: Biology
grade: 11
unit: 9
title: Biota and Environment
hours: 10
area: Zoology
---

The *biota* of a place is every living thing in it — the gharials of the Narayani,
the marmots of Mustang, the bacteria in a Kathmandu drain. None of them lives in
a vacuum. Each is shaped by its surroundings, each behaves in ways that improve
its chances, and each is now being pushed by an environment that people are
changing fast. This unit therefore has three jobs: to show *how* animals are
fitted to where they live (adaptation), *what* they do there (behaviour), and
*what happens* when we foul the place (pollution).

::: key What the examiner asks from this unit
Three reliable patterns. First, a **list-with-reasons** question: "describe four
adaptations of a bird for flight" — one mark per adaptation *plus its function*,
so never write the structure alone. Second, a **compare-and-contrast** table:
innate vs learned behaviour, hibernation vs aestivation, BOD vs DO,
bioaccumulation vs biomagnification. Third, an **8-mark pollution essay** —
sources, effects, control measures, in that order, with Nepali examples.
:::

## 9.1 Animal adaptation

An **adaptation** is any inherited feature of an animal — in its shape, its
chemistry or its behaviour — that raises its chance of surviving and breeding in
its own habitat. Two words must be kept apart from the start. The **habitat** is
the physical address where an animal lives (a Terai grassland, a cold Himalayan
stream). The **niche** is its job description: what it eats, when it is active,
what eats it, what it competes with. Two species can share a habitat, but no two
can occupy exactly the same niche for long.

Adaptations arise by natural selection acting on inherited variation over many
generations. They are *not* produced on demand by an individual: a chital does
not decide to grow longer legs because it is being chased. What a single animal
can do inside its own lifetime is **acclimatisation** — a reversible adjustment,
like the extra red blood cells a trekker makes at Namche Bazaar.

::: definition Adaptation
Adaptation is the sum of the hereditary morphological, physiological and
behavioural characters of an organism that fit it to its particular environment
and enable it to survive and reproduce successfully in that environment.
:::

### Three kinds of adaptation

| Kind | What changes | Examples |
|---|---|---|
| Morphological (structural) | body form, organs, colour | streamlined fish body, webbed feet of a duck, hollow bones of a bird |
| Physiological (functional) | chemistry and organ working | concentrated urine of the kangaroo rat, extra haemoglobin of the yak, venom of a krait |
| Behavioural | what the animal does | migration of the bar-headed goose, hibernation of the Himalayan marmot, nocturnal habit of the porcupine |

A single problem is usually solved by all three at once. A camel resists drought
structurally (fat hump, long legs), physiologically (concentrated urine, wide body
temperature swing) and behaviourally (feeding at dawn and dusk, sitting with legs
tucked in to reduce heat gain).

### Aquatic adaptation

Water is 800 times denser than air, holds only about 1/30 as much oxygen per
unit volume, and its salt concentration continuously pulls water into or out of
an animal's body. Aquatic animals are graded by how long their ancestors have
been in water:

- **Primary aquatic** animals never left the water — fishes, sponges, molluscs.
- **Secondary aquatic** animals had land-living ancestors and returned — whales,
  dolphins, seals, sea snakes, turtles.
- **Tertiary (partial) aquatic** animals divide their lives between land and
  water — frogs, otters, crocodiles.

```figure caption="Adaptations of a bony fish (teleost) for life in water. Water taken in at the mouth passes over the gills and out under the operculum, flowing opposite to the blood — a counter-current that strips up to 80 % of the dissolved oxygen."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(5.1, 2.4))

def prof(x):
    return np.sin(np.pi*(x/8.0)**0.70)**0.70

xs = np.linspace(0, 7.4, 400)
f = prof(xs)
top, bot = 1.30*f, -1.00*f
ax.fill_between(xs, bot, top, color=ACCENT, alpha=0.12, zorder=1)
ax.plot(xs, top, color=INK, lw=1.5, zorder=4)
ax.plot(xs, bot, color=INK, lw=1.5, zorder=4)
ax.plot([7.4, 7.4], [1.30*prof(7.4), -1.00*prof(7.4)], color=INK, lw=0.7, zorder=4)

# caudal (tail) fin - homocercal, forked
ax.add_patch(Polygon([(7.35, 0.37), (9.0, 1.25), (8.35, 0.0), (9.0, -1.15),
                      (7.35, -0.29)], closed=True, facecolor=ACCENT, alpha=0.30,
                     edgecolor=INK, lw=1.1, zorder=2))
# dorsal fin
ax.add_patch(Polygon([(2.5, 1.28), (3.45, 2.12), (4.35, 1.20)], closed=True,
                     facecolor=ACCENT, alpha=0.30, edgecolor=INK, lw=1.1, zorder=2))
# anal fin
ax.add_patch(Polygon([(5.55, -0.74), (5.95, -1.48), (6.65, -0.51)], closed=True,
                     facecolor=ACCENT, alpha=0.30, edgecolor=INK, lw=1.1, zorder=2))
# paired fins
ax.add_patch(Ellipse((3.05, -1.22), 1.75, 0.60, angle=-30, facecolor=SERIES[2],
                     alpha=0.30, edgecolor=INK, lw=1.0, zorder=2))
ax.add_patch(Ellipse((4.75, -1.20), 1.15, 0.45, angle=-22, facecolor=SERIES[2],
                     alpha=0.30, edgecolor=INK, lw=1.0, zorder=2))

# operculum (gill cover)
op = PathPatch(Path([(1.32, 1.10), (1.85, 0.10), (1.32, -0.86)],
                    [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
               facecolor='none', edgecolor=INK, lw=1.2, zorder=5)
ax.add_patch(op)
# air bladder
ax.add_patch(Ellipse((3.7, 0.38), 2.7, 0.52, facecolor=SERIES[3], alpha=0.25,
                     edgecolor=SERIES[3], lw=1.0, ls=(0, (3, 2)), zorder=3))
# eye and mouth
ax.add_patch(Circle((0.78, 0.36), 0.155, facecolor='white', edgecolor=INK,
                    lw=1.0, zorder=6))
ax.add_patch(Circle((0.78, 0.36), 0.065, facecolor=INK, zorder=7))
ax.plot([0.02, 0.62], [-0.02, -0.30], color=INK, lw=1.2, zorder=6)

# lateral line
lx = np.linspace(1.95, 7.25, 60)
ax.plot(lx, 0.40 - 0.040*(lx - 1.95), color=SERIES[1], lw=1.2,
        ls=(0, (1.4, 1.6)), zorder=5)

# water flow arrows through the gill chamber
for y0 in (-0.15, 0.12):
    ax.annotate('', xy=(1.95, y0 - 0.25), xytext=(-0.95, y0),
                arrowprops=dict(arrowstyle='-|>', color=SERIES[5], lw=1.2,
                                mutation_scale=9,
                                connectionstyle='arc3,rad=-0.25'), zorder=6)
def lab(text, xy, xytext, ha='center'):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=8.0, color=INK, ha=ha,
                va='center',
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8,
                                shrinkA=2, shrinkB=3))

ax.text(-1.25, 0.00, 'water in', fontsize=7.8, color=SERIES[5], ha='right',
        va='center')
lab('streamlined (fusiform) body,\nmucus-coated scales', (1.9, 1.16), (1.3, 3.40))
lab('dorsal fin\n(prevents rolling)', (3.55, 2.06), (7.6, 3.40), ha='left')
lab('homocercal caudal fin\n\u2014 thrust and steering', (8.60, 0.85), (9.7, 1.70), ha='left')
lab('air (swim) bladder\n\u2014 buoyancy control', (4.95, 0.42), (9.7, -0.35), ha='left')
lab('lateral line: senses\ncurrents and vibration', (6.60, 0.17), (9.7, -2.35), ha='left')
lab('eye,\nno eyelid', (0.78, 0.50), (-1.25, 1.95), ha='right')
lab('operculum over\nthe gill arches', (1.62, -0.55), (-1.25, -2.20), ha='right')
lab('pectoral fin', (3.15, -1.35), (2.2, -3.30))
lab('pelvic fin', (4.85, -1.28), (5.1, -3.30))
lab('anal fin', (5.95, -1.42), (7.5, -3.30))

ax.set_xlim(-4.4, 13.8); ax.set_ylim(-4.30, 4.26)
ax.set_aspect('equal'); ax.axis('off')
```

The teleost solves five problems at once:

1. **Drag.** A fusiform (spindle) body, scales pointing backwards and a slippery
   mucus coat cut friction; the mucus also blocks bacteria and fungi.
2. **Propulsion and balance.** The muscular tail and homocercal (equally lobed)
   caudal fin drive the fish forward; unpaired dorsal and anal fins stop it
   rolling; paired pectoral and pelvic fins act as brakes, rudders and hydrofoils.
3. **Gas exchange.** Four pairs of gills with thousands of thin, highly vascular
   gill lamellae give a huge surface area. Water flows over them in the direction
   *opposite* to the blood — a **counter-current** — so a diffusion gradient is
   maintained all along the lamella.
4. **Buoyancy.** The gas-filled **air (swim) bladder** is adjusted so the fish is
   almost weightless in water and need not swim to avoid sinking. Cartilaginous
   fishes lack it and compensate with a large oil-rich liver, a heterocercal tail
   and wing-like pectoral fins.
5. **Osmoregulation.** A freshwater fish is *hypertonic* to its surroundings, so
   water floods in: it drinks nothing, passes large volumes of very dilute urine
   and actively pumps salts inward through the gills. A marine bony fish is
   *hypotonic* to seawater and loses water: it drinks seawater, excretes salt
   through chloride cells in the gills and passes a small volume of concentrated
   urine.

::: caution Gills are not lungs turned inside out
Gill lamellae work only when supported by water. Out of water they stick
together, the surface area collapses and the fish suffocates in air — even though
air holds thirty times more oxygen. The failure is mechanical, not chemical.
:::

### Adaptation to land: cursorial, arboreal, fossorial and volant habits

| Habit | Meaning | Key adaptations | Example |
|---|---|---|---|
| Cursorial | running | long slender limbs, reduced digits, deep chest, unguligrade stance | horse, chital, blackbuck |
| Arboreal | tree-living | prehensile tail, opposable digits, long forelimbs, binocular vision | langur, red panda |
| Fossorial | burrowing | spindle body, spade-like forelimbs, reduced eyes and ears, strong claws | mole, pangolin |
| Volant | flying | pneumatic bones, air sacs, keeled sternum, feathers | pigeon, bat (gliding membrane instead of feathers) |
| Desmocryptic | camouflage | colour and pattern matching background | tiger stripes, leaf insect |

Flight is the most demanding of these and is worth learning as a complete list,
because it is asked almost every year. A bird is adapted for flight by:

- a **streamlined, boat-shaped body** with no external projections;
- **feathers** — light, strong, replaceable, giving both the aerofoil surface and
  insulation;
- **forelimbs modified into wings**, the hand bones fused and reduced;
- **pneumatic bones**: hollow, air-filled, with internal struts — strong but light;
- a **keeled sternum (carina)** giving a broad origin for the flight muscles;
- huge **pectoralis major** (pulls the wing down) and a smaller **pectoralis minor**
  (raises it), together up to a fifth of body mass;
- **nine air sacs** continuous with the lungs, giving one-way flow of air and a
  second oxygen extraction during exhalation, plus cooling;
- a **four-chambered heart** and fast double circulation with no mixing of blood;
- **weight economy**: no urinary bladder, uric acid excreted as a semi-solid paste,
  no teeth, one functional ovary in the female, short rectum.

### Desert (xeric) adaptation

Deserts impose two problems — heat and water shortage — and animals solve them by
never wasting water on cooling.

- The **camel** stores fat (not water) in the hump, tolerates its body temperature
  drifting from about 34 °C at dawn to 41 °C by afternoon before it begins to
  sweat, produces very concentrated urine and dry faeces, has oval red blood
  cells that resist bursting when it rehydrates, and can lose a quarter of its
  body water without collapsing.
- The **kangaroo rat** drinks no water at all. It gains metabolic water from the
  oxidation of dry seeds, has no sweat glands, stays in a humid burrow by day,
  and has extremely long loops of Henle that make urine several times more
  concentrated than its blood. A counter-current in the nasal passages recovers
  water from exhaled air.

### Cold and high-altitude adaptation

Nepal's own species supply the best examples. Two rules of thumb apply to warm-
blooded animals:

- **Bergmann's rule** — within a related group, individuals in colder regions tend
  to be **larger**, because a big body has a smaller surface-area-to-volume ratio
  and so loses heat more slowly.
- **Allen's rule** — extremities (ears, tail, limbs) tend to be **shorter** in
  colder regions, again cutting the surface for heat loss. Compare the small ears
  of a snow leopard with the enormous ears of a desert fox.

Additional Himalayan adaptations include thick fur with a dense woolly undercoat
and subcutaneous fat (yak, blue sheep, snow leopard); **counter-current heat
exchange** in the limbs, where warm arterial blood pre-warms cold venous blood
returning from the feet; more red blood cells carrying haemoglobin with a higher
oxygen affinity, plus larger lungs and heart (yak); wide splayed hooves for snow;
an enlarged nasal chamber that warms inhaled air (snow leopard); and behavioural
dormancy — the Himalayan marmot hibernates for six to eight months in a sealed
burrow, its heart rate and metabolism falling dramatically.

| Dormancy | Season | Trigger | Example |
|---|---|---|---|
| Hibernation (winter sleep) | winter | cold and short days | Himalayan marmot, frogs, bats |
| Aestivation (summer sleep) | dry summer | heat and drought | African lungfish, land snails, some toads |
| Diapause | any | unfavourable season | insect eggs and pupae |

### Life-history adaptation: r-strategists and K-strategists

Adaptation also shows in *how an animal spends its reproductive effort*. Two
extreme strategies are recognised, and both are described by a growth equation.

An unlimited population grows **exponentially**. If $N$ is the number of
individuals and $r$ the intrinsic rate of natural increase (births minus deaths
per individual per unit time),

$$ \frac{dN}{dt} = rN \qquad \Longrightarrow \qquad N_t = N_0\,e^{rt} $$

The graph is a **J-shaped curve** with no upper limit — real only for a short
while, in a new or emptied habitat.

Resources are finite. Let $K$ be the **carrying capacity**: the largest population
the habitat can support indefinitely. The **logistic** equation adds a braking
term $(K-N)/K$ that falls to zero as $N$ approaches $K$:

$$ \frac{dN}{dt} = rN\left(\frac{K-N}{K}\right) $$

whose solution is the **sigmoid (S-shaped) curve** with a lag phase, a log phase,
a phase of decreasing increase and a stationary phase at $N = K$.

```figure caption="Exponential (J) and logistic (S) growth plotted from $N_t = N_0e^{rt}$ and the logistic equation, both with $N_0 = 10$, $r = 0.5$ yr$^{-1}$ and $K = 1000$. Growth is fastest at $N = K/2$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.0))
N0, r, K = 10.0, 0.5, 1000.0
t = np.linspace(0, 18, 600)
expo = N0*np.exp(r*t)
logi = K/(1 + ((K - N0)/N0)*np.exp(-r*t))
ax.plot(t, expo, color=SERIES[1], lw=1.9, label='exponential (J-shaped)')
ax.plot(t, logi, color=ACCENT, lw=1.9, label='logistic (S-shaped)')
ax.axhline(K, color=MUTED, lw=0.9, ls=(0, (4, 3)))
ax.axhline(K/2, color=GRID, lw=0.9, ls=(0, (2, 3)))
ax.text(17.8, K + 26, 'carrying capacity  K', ha='right', fontsize=8.2, color=MUTED)
ax.text(0.2, K/2 + 28, 'K/2', fontsize=8.2, color=MUTED)
ti = np.log((K - N0)/N0)/r
ax.plot([ti], [K/2], 'o', color=ACCENT, ms=5, zorder=5)
ax.annotate('point of inflexion:\ngrowth rate is maximum', xy=(ti, K/2),
            xytext=(ti + 1.0, K/2 - 320), fontsize=8.0, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9, mutation_scale=9))
for x0, x1, name in [(0, 4.5, 'lag'), (4.5, 9.2, 'log'), (9.2, 13.8, 'deceleration'),
                     (13.8, 18.0, 'stationary')]:
    ax.annotate('', xy=(x1, 1140), xytext=(x0, 1140),
                arrowprops=dict(arrowstyle='|-|,widthA=0.25,widthB=0.25',
                                color=MUTED, lw=0.7))
    ax.text((x0 + x1)/2, 1175, name, ha='center', fontsize=7.4, color=MUTED)
ax.set_xlabel('time (years)'); ax.set_ylabel('population size  $N$')
ax.set_xlim(0, 18); ax.set_ylim(0, 1320)
ax.set_yticks([0, 250, 500, 750, 1000])
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, axis='y', alpha=0.5)
ax.legend(loc='upper left', bbox_to_anchor=(0.03, 0.80))
```

| Feature | r-strategist | K-strategist |
|---|---|---|
| Body size | small | large |
| Life span | short | long |
| Offspring | very many, small | few, large |
| Parental care | none or little | prolonged |
| Mortality of young | very high | low |
| Growth curve | J-shaped, crashes | S-shaped, settles near $K$ |
| Example | housefly, rat, carp | one-horned rhinoceros, tiger, elephant |

This is exactly why a rhinoceros is hard to conserve and a mosquito impossible to
eradicate. A rhino cow first calves at about six years and then produces one calf
every three years or so; a lost individual takes years to replace.

::: example Worked example 9.1 — growth rate of Nepal's rhinos
**Problem.** Nepal's national rhino count found **645** greater one-horned
rhinoceroses in 2015 and **752** in 2021. Assuming exponential growth over these
6 years, calculate (a) the intrinsic rate of natural increase $r$, (b) the
percentage annual growth rate, and (c) the doubling time of the population.

**Solution.**

(a) From $N_t = N_0e^{rt}$, taking natural logarithms,

$$ r = \frac{1}{t}\ln\!\left(\frac{N_t}{N_0}\right)
     = \frac{1}{6}\ln\!\left(\frac{752}{645}\right) $$

$$ r = \frac{1}{6}\ln(1.1659) = \frac{0.1535}{6} = 0.0256\ \text{yr}^{-1} $$

(b) Percentage annual growth $= 0.0256 \times 100 = 2.56\ \%$ per year.

(c) The doubling time is obtained by putting $N_t = 2N_0$:

$$ t_d = \frac{\ln 2}{r} = \frac{0.693}{0.0256} = 27.1\ \text{years} $$

So at this rate Nepal would hold about 1500 rhinos only in the late 2040s — and
that is before any density-dependent braking is allowed for. Slow growth is the
signature of a K-strategist.
:::

::: example Worked example 9.2 — carrying capacity
**Problem.** A grassland block is estimated to have a carrying capacity of
$K = 1200$ chital and an intrinsic rate of increase $r = 0.20\ \text{yr}^{-1}$.
Using the logistic model, find the rate of increase of the herd when it numbers
(a) 400 animals, (b) 600 animals, (c) 1200 animals. At what size does the herd
grow fastest?

**Solution.** The logistic equation is $\dfrac{dN}{dt} = rN\left(\dfrac{K-N}{K}\right)$.

(a) $N = 400$:

$$ \frac{dN}{dt} = 0.20 \times 400 \times \frac{1200-400}{1200}
 = 80 \times 0.667 = 53.3 \approx 53\ \text{animals yr}^{-1} $$

(b) $N = 600$:

$$ \frac{dN}{dt} = 0.20 \times 600 \times \frac{1200-600}{1200}
 = 120 \times 0.500 = 60\ \text{animals yr}^{-1} $$

(c) $N = 1200 = K$:

$$ \frac{dN}{dt} = 0.20 \times 1200 \times \frac{1200-1200}{1200} = 0 $$

The product $N(K-N)$ is largest when $N = K/2 = 600$, so growth is fastest at
**600 animals**, i.e. at half the carrying capacity. This is why wildlife managers
aim to hold a harvested population near $K/2$ rather than near $K$.
:::

## 9.2 Animal behavior

**Behaviour** is everything an animal does — every movement, posture, sound and
chemical signal — and the way it changes with the situation. Its scientific study
is **ethology**. The subject's founders, Konrad Lorenz, Nikolaas Tinbergen and
Karl von Frisch, shared the Nobel Prize in Physiology or Medicine in 1973.

Behaviour is switched on by a **stimulus** and executed as a **response**, but the
programme itself may come from the genes, from experience, or from both. That
gives the basic division of the topic.

| | Innate (instinctive) behaviour | Learned behaviour |
|---|---|---|
| Origin | inherited, coded in the genes | acquired through experience |
| Needs practice? | no — correct at the first attempt | yes |
| Variation | almost identical in all members of a species | differs between individuals |
| Flexibility | rigid, hard to modify | flexible, can be unlearned |
| Nervous system | simple systems suffice | needs a well-developed brain |
| Example | a spider spinning its first web | a dog sitting on command |

### Innate behaviour

- **Taxis** — a *directed* movement of the whole animal towards or away from a
  stimulus: positive phototaxis of a moth to a lamp, negative phototaxis of a
  cockroach, chemotaxis of a mosquito to carbon dioxide, rheotaxis of a fish
  facing the current, geotaxis of an earthworm moving down.
- **Kinesis** — an *undirected* change in the rate of movement or turning. A
  woodlouse simply moves faster in dry air and slows in damp air, and so
  accumulates where it is damp without ever steering.
- **Reflex** — a rapid, automatic response of a *part* of the body through a spinal
  reflex arc: knee jerk, blinking, withdrawal from a hot object.
- **Fixed action pattern (FAP)** — a stereotyped chain of movements that, once
  triggered by a **sign stimulus (releaser)**, runs to completion. A herring gull
  chick pecks at the red spot on its parent's bill; a greylag goose rolls any
  egg-like object back into the nest.
- **Instinct** — a complex, unlearned, species-specific behaviour such as nest
  building, web spinning or the honeybee dance.
- **Imprinting** — a special, very rapid learning that occurs only during a short
  **critical period** just after hatching or birth and is then irreversible.
  Lorenz's newly hatched greylag goslings followed the first moving object they
  saw, including Lorenz himself. It is the bridge between innate and learned
  behaviour.

### Learned behaviour

- **Habituation** — the simplest learning: the response to a repeated but harmless
  stimulus fades. Crows stop flying up at a scarecrow after a few days.
- **Classical (associative) conditioning** — Pavlov's dogs. Food (the unconditioned
  stimulus) causes salivation (the unconditioned response). A bell (a neutral
  stimulus) rung repeatedly just before feeding becomes a **conditioned stimulus**
  and by itself produces salivation, now a **conditioned response**.
- **Operant (trial-and-error) conditioning** — Skinner's rat learns to press a
  lever because pressing is followed by a food reward. Behaviour followed by
  **reinforcement** becomes commoner; behaviour followed by punishment becomes
  rarer.
- **Insight learning** — solving a new problem at once by reorganising past
  experience, without trial and error. Köhler's chimpanzee stacked boxes to reach
  a hanging banana.
- **Latent (exploratory) learning** — an animal builds a mental map of its
  territory with no immediate reward, and uses it later to escape a predator.
- **Imitation** — copying another individual, as when one langur's alarm call sets
  the whole troop moving.

### Communication and the honeybee dance

Animals signal in four channels: **chemical** (pheromones — the alarm pheromone of
a honeybee, the trail pheromone of ants, bombykol released by the female silk
moth), **visual** (the peacock's display, the threat gape of a rhesus monkey),
**auditory** (bird song, the alarm call of a chital) and **tactile** (grooming,
antennal contact).

The most famous single piece of animal communication is the **dance language of
the honeybee**, worked out by Karl von Frisch. A returning forager dances on the
vertical surface of the comb in the dark hive:

- a **round dance** — a simple circle, reversed repeatedly — means food is close,
  within roughly 50–100 m, and gives no direction;
- a **waggle (tail-wagging) dance** — a figure-of-eight with a straight, abdomen-
  waggling run in the middle — is used for food farther away and encodes **both**
  distance and direction.

```figure caption="The waggle dance of the honeybee. On the vertical comb the angle of the straight waggle run from the upward vertical equals the angle between the sun and the food source as seen from the hive. Longer waggling means a longer flight."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

fig, (axL, axR) = plt.subplots(1, 2, figsize=(5.2, 2.9))
th = np.radians(40.0)

# ---------------- left: dance on the vertical comb ----------------
def rot(px, py, a):
    return px*np.cos(a) + py*np.sin(a), -px*np.sin(a) + py*np.cos(a)

# honeycomb background (pointy-top hexagons)
R = 0.34
ang6 = np.linspace(0, 2*np.pi, 7) + np.pi/6
for row in range(-5, 6):
    for col in range(-4, 5):
        cx = col*np.sqrt(3)*R + (np.sqrt(3)*R/2 if row % 2 else 0.0)
        cy = row*1.5*R
        axL.plot(cx + R*np.cos(ang6), cy + R*np.sin(ang6),
                 color=GRID, lw=0.6, zorder=0)

axL.annotate('', xy=(0, 1.95), xytext=(0, -1.95),
             arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0,
                             ls=(0, (4, 3)), mutation_scale=10), zorder=2)
axL.text(0.08, 1.98, 'vertical\n(gravity)', fontsize=7.6, color=MUTED, va='bottom')

# waggle run
wx, wy = rot(np.array([0.0, 0.0]), np.array([-1.05, 1.05]), th)
axL.annotate('', xy=(wx[1], wy[1]), xytext=(wx[0], wy[0]),
             arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=2.4,
                             mutation_scale=13), zorder=5)
# zig-zag showing the side-to-side waggling of the abdomen
sv = np.linspace(-1.0, 1.0, 19)
zz = 0.15*((-1.0)**np.arange(19))
zx, zy = rot(zz, sv, th)
axL.plot(zx, zy, color=SERIES[1], lw=0.9, zorder=6)

# return loops (two arcs bulging left and right)
R, c = 1.28, -np.sqrt(1.28**2 - 1.05**2)
a0 = np.degrees(np.arctan2(1.05, -c))
for sgn in (1, -1):
    ang = np.radians(np.linspace(a0, -a0, 80))
    lx = sgn*(c + R*np.cos(ang)); ly = R*np.sin(ang)
    rx, ry = rot(lx, ly, th)
    axL.plot(rx, ry, color=ACCENT, lw=1.1, zorder=3)
    k = 40
    axL.annotate('', xy=(rx[k+1], ry[k+1]), xytext=(rx[k], ry[k]),
                 arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0,
                                 mutation_scale=10), zorder=3)

arc = np.radians(np.linspace(90, 90 - 40, 60))
axL.plot(0.80*np.cos(arc), 0.80*np.sin(arc), color=INK, lw=0.9, zorder=6)
axL.text(0.46, 0.93, r'$\theta$', fontsize=10.5, color=INK, zorder=6)
axL.text(0, -2.50, 'dance on the vertical comb', ha='center', fontsize=8.2,
         color=INK)
axL.set_xlim(-2.1, 2.1); axL.set_ylim(-2.85, 2.45)
axL.set_aspect('equal'); axL.axis('off')

# ---------------- right: the real field geometry ----------------
axR.add_patch(Circle((1.35, 1.75), 0.26, facecolor=SERIES[3], alpha=0.85,
                     edgecolor='none'))
for a in np.linspace(0, 2*np.pi, 12, endpoint=False):
    axR.plot([1.35 + 0.33*np.cos(a), 1.35 + 0.48*np.cos(a)],
             [1.75 + 0.33*np.sin(a), 1.75 + 0.48*np.sin(a)],
             color=SERIES[3], lw=0.9)
axR.text(1.35, 2.32, 'sun', ha='center', fontsize=8.0, color=INK)

axR.add_patch(Polygon([(-1.30, -1.55), (-0.60, -1.55), (-0.60, -0.95),
                       (-0.95, -0.62), (-1.30, -0.95)], closed=True,
                      facecolor=MUTED, alpha=0.35, edgecolor=INK, lw=1.0))
axR.text(-0.95, -1.88, 'hive', ha='center', fontsize=8.0, color=INK)

for dx, dy in [(0, 0), (0.22, 0.16), (-0.20, 0.18)]:
    axR.add_patch(Circle((1.55 + dx, -0.25 + dy), 0.115, facecolor=SERIES[1],
                         alpha=0.8, edgecolor='none'))
axR.text(1.62, -0.72, 'food source', ha='center', fontsize=8.0, color=INK)

H = np.array([-0.95, -0.95])
for tgt, col, lab in [(np.array([1.30, 1.72]), SERIES[3], None),
                      (np.array([1.48, -0.20]), SERIES[1], None)]:
    axR.annotate('', xy=tgt, xytext=H,
                 arrowprops=dict(arrowstyle='-|>', color=col, lw=1.4,
                                 ls=(0, (5, 3)), mutation_scale=11))
aS = np.arctan2(1.72 + 0.95, 1.30 + 0.95)
aF = np.arctan2(-0.20 + 0.95, 1.48 + 0.95)
arc2 = np.linspace(aF, aS, 60)
axR.plot(H[0] + 1.35*np.cos(arc2), H[1] + 1.35*np.sin(arc2), color=INK, lw=0.9)
axR.text(H[0] + 1.62*np.cos((aS + aF)/2), H[1] + 1.62*np.sin((aS + aF)/2),
         r'$\theta$', fontsize=10.5, color=INK, ha='center', va='center')
axR.text(0.35, -2.50, 'the same angle out in the field', ha='center',
         fontsize=8.2, color=INK)
axR.set_xlim(-1.9, 2.6); axR.set_ylim(-2.85, 2.45)
axR.set_aspect('equal'); axR.axis('off')
fig.subplots_adjust(wspace=0.02)
```

Two rules make the dance a genuine language. **Direction:** the angle the straight
waggle run makes with the upward vertical on the comb is the same as the angle
between the direction of the sun and the direction of the food, measured from the
hive. A run straight up means "fly towards the sun". **Distance:** the farther the
food, the longer each waggle run lasts — roughly one second of waggling for each
kilometre of flight. Bees that watch the dance in the dark, feeling it with their
antennae, then fly out and find the flowers.

### Social behaviour

Living in a group costs food and risks disease but buys protection, easier
hunting and shared care of young. Its main forms are:

- **Aggregation** — a temporary gathering with no organisation, e.g. moths at a light.
- **Dominance hierarchy** — a ranked order that settles disputes without fighting.
  The "pecking order" in hens is the classical case; in a wolf pack or a rhesus
  troop the alpha animal feeds and breeds first.
- **Territoriality** — the defence of an area by song, scent marking or display. A
  tiger patrols and scent-marks a territory of tens of square kilometres in
  Chitwan; a territory guarantees food and a mate rather than space for its own sake.
- **Altruism** — behaviour that lowers the actor's own reproductive success and
  raises another's: a worker bee stinging and dying, a sentinel langur giving an
  alarm call. It is favoured when the helped individuals are close relatives, so
  copies of the same genes are passed on (**kin selection**).
- **Eusociality** — the extreme case, with a reproductive division of labour, as in
  the honeybee colony: one fertile **queen**, a few hundred haploid **drones** whose
  only role is mating, and thousands of sterile female **workers** that forage,
  build, nurse and defend.

### Rhythms, migration and courtship

Behaviour is timed. **Biological rhythms** are internally generated cycles kept in
step by external cues: *circadian* rhythms of about 24 hours (sleep, activity),
*circalunar* and *circannual* rhythms (breeding seasons, moulting).

**Migration** is the regular two-way movement of a population between breeding and
non-breeding areas. The Arctic tern makes the longest journey of any animal;
**bar-headed geese** cross the Himalaya over Nepal at heights above 7000 m; the
**demoiselle crane** passes through Nepali valleys each autumn. Fish migrate too —
salmon are *anadromous* (sea to river to breed), eels *catadromous* (river to sea).
Navigation uses the sun, star patterns, the Earth's magnetic field, landmarks and
smell.

**Courtship** is ritualised behaviour that identifies a partner of the right
species, sex and readiness, suppresses aggression, and synchronises the release of
gametes — the peacock's fanned train, the croaking chorus of *Rana tigrina* at the
start of the monsoon, the firefly's coded flashes.

### Interactions between species

Behaviour towards *other* species can be summarised in a table of signs: $+$ for
benefit, $-$ for harm, $0$ for no measurable effect.

```figure caption="The seven possible interspecific interactions, classified by the effect on each partner ($+$ benefit, $-$ harm, $0$ no effect)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

rows = [('Mutualism',    '+', '+', 'lichen: alga + fungus;\nRhizobium in root nodules'),
        ('Commensalism', '+', '0', 'cattle egret and cattle;\nremora on a shark'),
        ('Predation',    '+', '\u2212', 'tiger eats chital'),
        ('Parasitism',   '+', '\u2212', 'Ascaris in human gut;\nleech, tick'),
        ('Competition',  '\u2212', '\u2212', 'chital and hog deer\nfor the same grass'),
        ('Amensalism',   '0', '\u2212', 'Penicillium inhibits\nbacteria'),
        ('Neutralism',   '0', '0', 'a tiger and a termite')]
cols = {'+': SERIES[2], '\u2212': SERIES[1], '0': MUTED}

fig, ax = plt.subplots(figsize=(5.1, 3.1))
n = len(rows)
for i, (name, a, b, ex) in enumerate(rows):
    y = n - 1 - i
    if i % 2 == 0:
        ax.add_patch(Rectangle((-0.02, y - 0.46), 4.92, 0.92, facecolor=GRID,
                               alpha=0.35, edgecolor='none', zorder=0))
    ax.text(0.86, y, name, ha='right', va='center', fontsize=8.5, color=INK,
            fontweight='600', zorder=3)
    for j, s in enumerate((a, b)):
        cx = 1.25 + j*0.64
        ax.add_patch(Rectangle((cx - 0.20, y - 0.21), 0.40, 0.42,
                               facecolor=cols[s], alpha=0.22,
                               edgecolor=cols[s], lw=1.0, zorder=2))
        ax.text(cx, y, s, ha='center', va='center', fontsize=10.5,
                color=cols[s], fontweight='bold', zorder=3)
    ax.text(2.30, y, ex, ha='left', va='center', fontsize=7.6, color=MUTED, zorder=3)

ax.text(1.25, n - 0.30, 'species\nA', ha='center', va='bottom', fontsize=7.8, color=INK)
ax.text(1.89, n - 0.30, 'species\nB', ha='center', va='bottom', fontsize=7.8, color=INK)
ax.text(2.30, n - 0.30, 'example', ha='left', va='bottom', fontsize=7.8, color=INK)
ax.plot([-0.02, 4.90], [n - 0.52, n - 0.52], color=INK, lw=0.9)
ax.set_xlim(-0.45, 4.95); ax.set_ylim(-0.6, n + 0.62)
ax.axis('off')
```

Predation and parasitism have the same sign pattern but differ in scale: a
predator is usually bigger than its prey and kills it at once, while a parasite is
smaller, lives on or in the host and weakens it slowly. Competition is the only
interaction that harms both partners, and it is the engine of **resource
partitioning** — the reason a chital grazes short grass while a sambar browses
leaves in the same forest.

## 9.3 Environmental Pollution

::: definition Pollution and pollutant
**Pollution** is any undesirable change in the physical, chemical or biological
properties of air, water or land that harms living organisms or damages
property. The agent causing the change is a **pollutant**.
:::

Pollutants are classified in three useful ways:

| Basis | Classes | Examples |
|---|---|---|
| Degradability | biodegradable / non-biodegradable | sewage, cow dung / DDT, plastics, mercury |
| Origin | primary (released as such) / secondary (formed in the environment) | CO, SO₂, NOₓ / ozone, PAN, H₂SO₄ in acid rain |
| Source pattern | point source / non-point (diffuse) source | a factory outfall, a chimney / farm run-off, vehicle exhaust |

### Air pollution and the disturbed carbon cycle

Carbon moves endlessly between the atmosphere, living bodies and rocks. Green
plants remove CO₂ by photosynthesis; respiration and decay return it; a tiny
fraction is locked away as coal, petroleum and limestone. That store took
hundreds of millions of years to build and we are burning it in two centuries,
so the return arrow is now far bigger than the removal arrow.

```figure caption="The carbon cycle. The grey and green arrows are the natural loops, which balance. The red arrow — combustion of fossil fuel, together with deforestation — is the human addition that is raising atmospheric CO$_2$. (The ocean absorbs part of the excess as dissolved carbonate.)"
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.0, 4.3))

def box(x, y, w, h, text, fc, ec, fs=7.6):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle='round,pad=0.10,rounding_size=0.16',
                                facecolor=fc, edgecolor=ec, lw=1.1, zorder=4))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK, zorder=5)

def arrow(p, q, label=None, color=MUTED, rad=0.0, lw=1.2, off=(0, 0), fs=6.9,
          ha='center'):
    p = np.array(p, float); q = np.array(q, float)
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                mutation_scale=10, shrinkA=2, shrinkB=2,
                                connectionstyle=f'arc3,rad={rad}'), zorder=3)
    if label:
        d = q - p
        m = (p + q)/2 + 0.5*rad*np.array([-d[1], d[0]])
        ax.text(m[0] + off[0], m[1] + off[1], label, ha=ha, va='center',
                fontsize=fs, color=color, zorder=6)

GREEN, RED = SERIES[2], SERIES[1]
box(5.0, 7.30, 5.2, 1.00, 'ATMOSPHERIC  CO$_2$\n~280 ppm before 1800,  >420 ppm now',
    '#e8eef6', ACCENT, fs=7.7)
box(1.60, 5.00, 2.7, 0.95, 'PRODUCERS\ngreen plants', '#e9f3ec', GREEN)
box(8.40, 5.00, 2.7, 0.95, 'CONSUMERS\nanimals', '#e9f3ec', GREEN)
box(5.00, 2.70, 3.7, 0.95, 'DEAD ORGANIC MATTER\nand decomposers', '#f2f0e6', SERIES[3])
box(8.60, 0.60, 2.9, 0.85, 'FOSSIL FUELS\ncoal, oil, gas', '#f7e8e7', RED)

arrow((2.55, 7.00), (1.05, 5.52), 'photosynthesis', GREEN, rad=-0.35,
      off=(-0.20, 0.10), ha='right', lw=1.5)
arrow((2.45, 5.50), (4.05, 6.78), 'respiration', MUTED, rad=0.18, off=(0.10, -0.55))
arrow((8.15, 5.50), (6.30, 6.80), 'respiration', MUTED, rad=-0.18, off=(0.00, -0.55))
arrow((2.98, 5.00), (7.02, 5.00), 'feeding', MUTED, off=(0, 0.28))
arrow((1.75, 4.50), (3.55, 3.22), 'litter, death', MUTED, rad=-0.12,
      off=(-0.30, -0.45), ha='right')
arrow((8.25, 4.50), (6.45, 3.22), 'death, excreta', MUTED, rad=0.12,
      off=(0.30, -0.45), ha='left')
arrow((4.85, 3.20), (4.85, 6.78), 'decomposition', MUTED, rad=0.16,
      off=(-0.70, -1.02), ha='right')
arrow((6.40, 2.32), (7.45, 1.05), 'fossilisation\n(millions of years)', MUTED,
      off=(-0.55, -0.35), ha='right')
arrow((9.55, 1.05), (7.35, 6.82), 'COMBUSTION\nof fossil fuel', RED, rad=-0.30,
      lw=2.2, off=(0.80, -1.45), ha='left')

ax.text(4.6, -0.75, 'net effect: enhanced greenhouse effect \u2192 global warming',
        ha='center', fontsize=7.8, color=RED)
ax.set_xlim(-2.6, 12.8); ax.set_ylim(-1.15, 8.25)
ax.axis('off')
```


**Major air pollutants and their effects**

| Pollutant | Chief source | Main effect |
|---|---|---|
| Carbon monoxide, CO | incomplete combustion in engines | binds haemoglobin ~200 times more strongly than O₂ → headache, asphyxia |
| Sulphur dioxide, SO₂ | coal burning, brick kilns, smelters | bronchitis; forms H₂SO₄ → acid rain |
| Oxides of nitrogen, NOₓ | high-temperature combustion | forms HNO₃ and photochemical smog |
| Particulates PM₁₀, PM₂.₅ | dust, diesel, brick kilns, crop burning | PM₂.₅ reaches the alveoli → asthma, heart disease, lung cancer |
| Ozone and PAN (secondary) | NOₓ + hydrocarbons + sunlight | eye irritation, damage to leaves and crops |
| CFCs | old refrigerants, aerosols | destroy stratospheric ozone |
| CO₂, CH₄, N₂O | fossil fuel, paddy fields, livestock | greenhouse effect |

Three consequences deserve separate names.

- **Acid rain.** Normal rain is already slightly acidic, pH ≈ 5.6, because CO₂
  dissolves in it. When SO₂ and NOₓ are converted to sulphuric and nitric acids the
  pH can fall below 4. The result is leaching of calcium and magnesium from soil,
  damage to leaves, death of fish in lakes, and corrosion of limestone and marble
  (**stone leprosy**).
- **The enhanced greenhouse effect.** CO₂, CH₄, N₂O, CFCs and water vapour let
  short-wave solar radiation in but absorb the long-wave infrared radiated back
  by the Earth, warming the lower atmosphere. Rising temperature means retreating
  Himalayan glaciers, growing glacial lakes and the risk of **GLOF** (glacial lake
  outburst floods), an immediate hazard for Nepal.
- **Ozone depletion.** Chlorine atoms freed from CFCs by ultraviolet light destroy
  ozone catalytically — a single chlorine atom can break down thousands of O₃
  molecules — thinning the shield that absorbs UV-B. More UV-B means more skin
  cancer, cataract and reduced crop yield. The **Montreal Protocol (1987)** phased
  out CFCs and the layer is now slowly recovering.

::: caution The greenhouse effect is not the same as ozone depletion
They are different problems with different gases, different atmospheric layers
and different effects. The greenhouse effect traps *outgoing infrared* in the
**troposphere**; ozone depletion lets in *incoming ultraviolet* through the
**stratosphere**. CFCs happen to do both — that is the only link.
:::

**Air pollution in Nepal.** The Kathmandu Valley is a bowl. In winter a
temperature inversion puts a lid on it, and smoke from vehicles, brick kilns,
waste burning and household fuel has nowhere to go. Kathmandu's annual mean
PM₂.₅ was **45.1 µg m⁻³ in 2024** — above Nepal's own national standard of
40 µg m⁻³ and about nine times the WHO guideline of 5 µg m⁻³. A 2025 World Bank
assessment ranked air pollution as the single largest risk factor for death and
disability in Nepal.

### Water pollution and the disturbed nitrogen cycle

Nitrogen is needed for every protein and nucleic acid, yet the huge atmospheric
supply is inert. Only a few prokaryotes — *Rhizobium* in legume root nodules,
free-living *Azotobacter* and *Clostridium*, cyanobacteria such as *Anabaena* —
together with lightning, can fix it. Industrial fertiliser has now roughly doubled
the amount of reactive nitrogen entering the biosphere, and the surplus ends up in
rivers and lakes.

```figure caption="The nitrogen cycle. Grey and green arrows are the natural route: fixation, nitrification, assimilation, ammonification and denitrification. Red arrows are human additions — fertiliser and combustion — which enter the cycle faster than denitrification can remove them."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.0, 4.3))

def box(x, y, w, h, text, fc, ec, fs=7.6):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle='round,pad=0.10,rounding_size=0.16',
                                facecolor=fc, edgecolor=ec, lw=1.1, zorder=4))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK, zorder=5)

def arrow(p, q, label=None, color=MUTED, rad=0.0, lw=1.2, off=(0, 0), fs=6.9,
          ha='center'):
    p = np.array(p, float); q = np.array(q, float)
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                mutation_scale=10, shrinkA=2, shrinkB=2,
                                connectionstyle=f'arc3,rad={rad}'), zorder=3)
    if label:
        d = q - p
        m = (p + q)/2 + 0.5*rad*np.array([-d[1], d[0]])
        ax.text(m[0] + off[0], m[1] + off[1], label, ha=ha, va='center',
                fontsize=fs, color=color, zorder=6)

GREEN, RED = SERIES[2], SERIES[1]

box(5.00, 7.70, 5.0, 0.85, 'ATMOSPHERIC  N$_2$   (78 % of air)', '#e8eef6', ACCENT, fs=8.0)
box(1.55, 5.55, 2.7, 0.95, 'AMMONIA\nNH$_3$ / NH$_4^+$', '#f2f0e6', SERIES[3])
box(1.30, 2.95, 2.7, 0.95, 'NITRITE\nNO$_2^-$', '#f2f0e6', SERIES[3])
box(4.20, 0.70, 2.6, 0.85, 'NITRATE\nNO$_3^-$', '#f2f0e6', SERIES[3])
box(8.60, 2.60, 2.9, 0.95, 'PROTEIN in plants\nand animals', '#e9f3ec', GREEN)
box(8.80, 5.30, 2.9, 0.95, 'DEAD MATTER,\nurea, excreta', '#e9f3ec', GREEN)

arrow((3.30, 7.32), (1.80, 6.08), 'nitrogen fixation\n(Rhizobium, Azotobacter,\nlightning)',
      GREEN, rad=-0.32, off=(-0.35, 0.02), ha='right', lw=1.5)
arrow((1.50, 5.06), (1.40, 3.46), 'nitrification:\nNitrosomonas', MUTED,
      off=(-0.35, 0), ha='right')
arrow((2.25, 2.55), (3.25, 1.18), 'then\nNitrobacter', MUTED, off=(-0.40, -0.45),
      ha='right')
arrow((5.35, 0.95), (7.85, 2.05), 'assimilation', GREEN, rad=-0.20, lw=1.4,
      off=(0.50, -0.58))
arrow((8.70, 3.10), (8.75, 4.80), 'death,\nexcretion', MUTED, off=(0.32, 0), ha='left')
arrow((7.40, 5.35), (3.00, 5.62), 'ammonification\nby decomposers', MUTED, rad=-0.18,
      off=(1.20, 0.30), ha='left')
arrow((3.55, 1.14), (4.30, 7.26), 'denitrification\n(Pseudomonas)', ACCENT, rad=0.05,
      lw=1.4, off=(0.38, 0.22), ha='left')
arrow((7.55, 7.86), (9.75, 6.62), 'NO$_x$ from combustion\n\u2192 acid rain', RED,
      lw=1.6, off=(0.30, 0.60), ha='left')
arrow((6.40, -0.72), (4.70, 0.26), 'fertiliser\n(urea, DAP)', RED, rad=0.12,
      lw=1.6, off=(0.60, -0.42), ha='left')
arrow((3.25, 0.28), (2.05, -0.62), 'run-off \u2192\neutrophication', RED, rad=0.10,
      lw=1.6, off=(-0.28, -0.35), ha='right')

ax.set_xlim(-3.3, 13.5); ax.set_ylim(-1.75, 8.55)
ax.axis('off')
```



**Sources of water pollution** are domestic sewage, industrial effluent (dyes,
tannery chromium, heavy metals), agricultural run-off (fertiliser and pesticide),
oil spills, hot water from power stations (**thermal pollution**, which lowers
dissolved oxygen) and radioactive waste.

Two measurements matter in every exam.

- **Dissolved oxygen (DO)** — the oxygen actually present in the water, in mg L⁻¹.
  Clean cold water holds 8–10 mg L⁻¹; below about 4 mg L⁻¹ most fish die.
- **Biochemical oxygen demand (BOD)** — the oxygen consumed by aerobic microbes
  while decomposing the organic matter in a sample, measured over 5 days at 20 °C.
  **High BOD means heavy organic pollution.** Clean river water has BOD under
  3 mg L⁻¹; raw sewage exceeds 300 mg L⁻¹.

**Eutrophication** is the chain that follows nutrient enrichment: nitrate and
phosphate from fertiliser, detergent and sewage enter a lake → algae and
water-hyacinth multiply explosively (an **algal bloom**) → the surface mat cuts off
light so submerged plants die → bacteria decompose the dead mass → BOD rises and
DO collapses → fish and other aerobic life suffocate → the lake fills with
sediment and eventually becomes a marsh. Phewa Tal and the lower Bagmati both show
the early stages.

Other specific water-borne hazards:

| Pollutant | Disease / effect |
|---|---|
| Methyl mercury (industrial) | Minamata disease — nerve and brain damage |
| Cadmium | Itai-itai disease — brittle painful bones |
| Nitrate above about 45 mg L⁻¹ | methaemoglobinaemia ("blue baby syndrome") |
| Arsenic in Terai tube-wells | arsenicosis: skin lesions, cancer |
| Excess fluoride | dental and skeletal fluorosis |
| Faecal coliforms in sewage | cholera, typhoid, dysentery, hepatitis A |

### Soil, noise and radioactive pollution

**Soil pollution** comes from over-use of fertiliser and pesticide, industrial
sludge, mine tailings and unsegregated solid waste; it destroys soil micro-flora,
lowers fertility and leaches into groundwater. **Noise pollution** is measured in
decibels; continuous exposure above about 80 dB damages hearing, and noise also
causes hypertension, sleeplessness and, in animals, abandonment of nests.
**Radioactive pollution** from mining, nuclear testing, reactor accidents
(Chernobyl 1986, Fukushima 2011) and careless disposal of medical isotopes causes
mutation, cancer and genetic damage, and the isotopes remain dangerous for
centuries.

### Bioaccumulation and biomagnification

A **persistent** pollutant — one that is not biodegradable and is fat-soluble, such
as DDT, dieldrin, PCBs or methyl mercury — is absorbed faster than it can be
excreted.

- **Bioaccumulation** is the build-up of such a substance *inside one individual*
  over its lifetime.
- **Biomagnification** is the increase in its concentration *from one trophic level
  to the next* along a food chain, because each predator eats many prey and keeps
  nearly all the poison.

::: example Worked example 9.3 — biomagnification of DDT
**Problem.** In a classic study of an estuarine food chain the concentration of
DDT was found to be:

| Trophic level | DDT (ppm) |
|---|---|
| Water | 0.000003 |
| Zooplankton | 0.04 |
| Small fish | 0.5 |
| Large fish | 2.0 |
| Fish-eating bird | 25.0 |

Calculate (a) the magnification factor from water to zooplankton, (b) the factor
from small fish to fish-eating bird, and (c) the overall magnification from water
to the bird.

**Solution.**

(a) $\dfrac{0.04}{0.000003} = 1.33\times 10^{4}$ — that is, about 13 300 times.

(b) $\dfrac{25.0}{0.5} = 50$ times.

(c) $\dfrac{25.0}{0.000003} = 8.33\times 10^{6}$ — over eight million times.

Water containing DDT at three parts per *billion* is legally "almost clean", yet
the top predator carries 25 ppm. This is why DDT thinned the eggshells of
fish-eating birds and why persistent organochlorines are banned worldwide.
:::

### Control of pollution

| Type | Control measures |
|---|---|
| Air | electrostatic precipitators, cyclone separators and bag filters on chimneys; scrubbers for SO₂; catalytic converters and unleaded fuel in vehicles; electric public transport; zig-zag technology in brick kilns; afforestation; green belts |
| Water | primary, secondary and tertiary sewage treatment before discharge; effluent standards; constructed wetlands; ban on phosphate detergents; organic farming |
| Soil | segregation and recycling of solid waste; sanitary landfill; composting; integrated pest management; biofertilisers |
| Noise | sound barriers and silencers; ban on pressure horns; industrial zoning; tree belts |
| General | the 4 Rs — **Refuse, Reduce, Reuse, Recycle**; environmental impact assessment before any big project; environmental education |

In Nepal the legal framework is the **Environment Protection Act, 2076 (2019)**,
which makes a clean and healthy environment a right, requires an Initial
Environmental Examination or an Environmental Impact Assessment before large
projects, and empowers the government to fix national ambient standards and to
recover compensation from polluters.

## Chapter summary

- **Adaptation** is an inherited morphological, physiological or behavioural
  feature that fits an animal to its habitat; acclimatisation, by contrast, is a
  reversible change within one lifetime.
- A bony fish is adapted by a fusiform body, mucus and scales, paired and unpaired
  fins, counter-current gills, an air bladder for buoyancy, and osmoregulation
  that is opposite in fresh and salt water.
- Flight adaptations: streamlined body, feathers, wings, pneumatic bones, keeled
  sternum, huge pectoral muscles, nine air sacs, four-chambered heart and weight
  economy (no urinary bladder, uric acid, one ovary).
- **Bergmann's rule** — colder climate, larger body; **Allen's rule** — colder
  climate, shorter extremities.
- Unlimited growth is exponential, $dN/dt = rN$, $N_t = N_0e^{rt}$, a J-curve;
  limited growth is logistic, $dN/dt = rN(K-N)/K$, an S-curve, fastest at $N=K/2$
  and levelling at the carrying capacity $K$. Doubling time $t_d = \ln 2/r$.
- **Innate** behaviour (taxis, kinesis, reflex, fixed action pattern, instinct,
  imprinting) is inherited and rigid; **learned** behaviour (habituation, classical
  and operant conditioning, insight, latent learning, imitation) needs experience.
- In the honeybee **waggle dance**, the angle of the waggle run to the vertical
  equals the angle of the food from the sun, and the duration of waggling
  indicates the distance; a round dance means food is close.
- Species interactions are classified by signs: mutualism $(+,+)$, commensalism
  $(+,0)$, predation and parasitism $(+,-)$, competition $(-,-)$, amensalism
  $(0,-)$, neutralism $(0,0)$.
- Pollutants are biodegradable or not, primary or secondary. Key effects: acid
  rain (pH below 5.6), enhanced greenhouse effect, ozone depletion,
  eutrophication (nutrients → bloom → high BOD → low DO → fish kill) and
  biomagnification of persistent, fat-soluble poisons.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The air bladder of a bony fish mainly helps in <span class="marks">[1]</span>
   (a) respiration (b) buoyancy (c) hearing (d) excretion
2. Following of the first moving object by a newly hatched gosling is <span class="marks">[1]</span>
   (a) habituation (b) conditioning (c) imprinting (d) insight learning
3. A population growing in an environment with unlimited resources shows <span class="marks">[1]</span>
   (a) a sigmoid curve (b) a J-shaped curve (c) a zero growth rate (d) a bell-shaped curve
4. The relationship between a cattle egret and a grazing buffalo is <span class="marks">[1]</span>
   (a) mutualism (b) parasitism (c) commensalism (d) amensalism
5. A high BOD value of river water indicates <span class="marks">[1]</span>
   (a) plenty of dissolved oxygen (b) heavy organic pollution
   (c) high nitrate only (d) that the water is fit to drink

::: note Answers to Group A
**1.** (b) — the gas-filled bladder makes the fish nearly weightless in water.
**2.** (c) — imprinting happens only in a short critical period and is irreversible.
**3.** (b) — with no limiting factor $dN/dt = rN$, giving exponential J-shaped growth.
**4.** (c) — the egret gains insects disturbed by the buffalo; the buffalo is unaffected $(+,0)$.
**5.** (b) — BOD is the oxygen microbes need to decompose organic matter, so high BOD means much organic waste.
:::

**Group B — Short answer (4 marks each)**

1. Describe any four adaptations of a bird for aerial life, stating the function
   of each. <span class="marks">[4]</span>
2. Differentiate between innate and learned behaviour, with two examples of each. <span class="marks">[4]</span>
3. A herd of 500 blue sheep grows exponentially with an intrinsic rate of natural
   increase $r = 0.08\ \text{yr}^{-1}$. Calculate (a) the number after 10 years and
   (b) the doubling time of the herd. <span class="marks">[4]</span>
4. What is eutrophication? Explain, step by step, how it kills the fish of a lake. <span class="marks">[4]</span>
5. Distinguish between bioaccumulation and biomagnification, and give one example
   of a pollutant that shows both. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Any four, each with its function: *pneumatic bones* — hollow and air-filled,
reducing weight without losing strength; *feathers* — light, form the aerofoil and
insulate; *keeled sternum* — gives a large surface for the origin of flight
muscles; *pectoralis major and minor* — depress and raise the wing; *nine air sacs* —
one-way airflow so oxygen is extracted during both inhalation and exhalation, and
the body is cooled; *no urinary bladder and uric acid excretion* — saves weight.

**2.** Innate: inherited, present at birth, identical in all members, rigid, needs
no practice (a spider spinning its first web; a herring gull chick pecking the red
spot). Learned: acquired by experience, differs between individuals, flexible, can
be forgotten (Pavlov's dog salivating at a bell; a monkey opening a latch by
trial and error). Award one mark per contrasted pair and one for examples.

**3.** (a) $N_t = N_0e^{rt} = 500\,e^{0.08\times 10} = 500\,e^{0.8}
= 500 \times 2.2255 = 1113$ animals (to the nearest animal).
(b) $t_d = \dfrac{\ln 2}{r} = \dfrac{0.693}{0.08} = 8.66\ \text{years}$.

**4.** Eutrophication is the over-enrichment of a water body with nutrients,
chiefly nitrate and phosphate. Sequence: fertiliser, detergent and sewage run in →
algae and water hyacinth bloom → the surface mat blocks light so submerged plants
die → aerobic bacteria decompose the huge dead mass → BOD rises sharply and
dissolved oxygen falls below about 4 mg L⁻¹ → fish and other aerobic animals
suffocate and die.

**5.** *Bioaccumulation* is the gradual build-up of a persistent pollutant within a
single organism, because intake exceeds excretion. *Biomagnification* is the
stepwise rise in its concentration from one trophic level to the next along a food
chain, because each consumer eats many individuals of the level below and retains
almost all of the poison. DDT (also methyl mercury, PCBs) shows both: about
0.000003 ppm in water but 25 ppm in a fish-eating bird.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define adaptation and distinguish it from acclimatisation. <span class="marks">[2]</span>
   (b) With the help of a labelled diagram, describe the adaptations of a bony
   fish for aquatic life. <span class="marks">[4]</span>
   (c) State Bergmann's rule and Allen's rule, giving one Himalayan example of each. <span class="marks">[2]</span>
2. (a) Explain the logistic model of population growth and sketch the curve,
   marking the carrying capacity. <span class="marks">[4]</span>
   (b) A fish population in Phewa Tal has a carrying capacity $K = 8000$ and an
   intrinsic rate of increase $r = 0.30\ \text{yr}^{-1}$. Find $dN/dt$ when
   $N = 2000$ and when $N = 4000$, and state the population size at which the
   growth rate is greatest. <span class="marks">[4]</span>
3. Describe air pollution under the headings: major pollutants and their sources;
   three global effects; the particular situation of the Kathmandu Valley; and
   control measures. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** (a) Adaptation is an inherited, population-level feature produced by natural
selection over generations; acclimatisation is a reversible physiological
adjustment made by one individual within its own lifetime (extra red cells at
high altitude). (b) Expect the labelled fish diagram plus streamlining and mucus,
fins for propulsion and balance, counter-current gills, air bladder, and the
opposite osmoregulatory strategies in fresh and sea water. (c) Bergmann — in
colder regions bodies are larger, so the surface-to-volume ratio and heat loss are
lower (the yak compared with lowland cattle). Allen — extremities are shorter in
colder regions (the short ears and stubby muzzle of a snow leopard compared with a
desert fox).

**2.** (a) The logistic model adds the braking factor $(K-N)/K$ to exponential
growth: $dN/dt = rN(K-N)/K$. When $N$ is small the factor is nearly 1 and growth is
almost exponential; as $N \to K$ the factor $\to 0$ and growth stops. The curve is
sigmoid with lag, log, deceleration and stationary phases, levelling off at $N=K$.

(b) When $N = 2000$:
$$ \frac{dN}{dt} = 0.30 \times 2000 \times \frac{8000-2000}{8000}
 = 600 \times 0.75 = 450\ \text{fish yr}^{-1} $$
When $N = 4000$:
$$ \frac{dN}{dt} = 0.30 \times 4000 \times \frac{8000-4000}{8000}
 = 1200 \times 0.50 = 600\ \text{fish yr}^{-1} $$
$N(K-N)$ is greatest at $N = K/2 = 4000$, so growth is fastest at **4000 fish**.

**3.** Outline: *pollutants and sources* — CO from incomplete combustion, SO₂ from
coal and brick kilns, NOₓ from engines, PM₂.₅ and PM₁₀ from diesel, dust and waste
burning, CFCs from old refrigerants, secondary ozone and PAN from photochemical
reaction. *Global effects* — acid rain (pH below 5.6, leached soils, dead lakes,
stone leprosy); the enhanced greenhouse effect (CO₂, CH₄, N₂O trap infrared →
warming → retreating Himalayan glaciers and GLOF risk); ozone depletion (chlorine
from CFCs destroys O₃ catalytically → more UV-B → skin cancer and cataract;
controlled by the Montreal Protocol, 1987). *Kathmandu Valley* — a bowl-shaped
basin with winter temperature inversion; annual mean PM₂.₅ of 45.1 µg m⁻³ in 2024,
above Nepal's standard of 40 and about nine times the WHO guideline of 5; air
pollution is Nepal's largest single risk factor for death and disability.
*Control* — precipitators, scrubbers and bag filters; catalytic converters and
electric public transport; zig-zag brick kilns; green belts and afforestation;
enforcement of the Environment Protection Act, 2076 (2019).
:::

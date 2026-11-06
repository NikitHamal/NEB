---
subject: Artificial Intelligence
grade: BCA Semester 5
unit: 1
title: Introduction to Artificial Intelligence and Intelligent Agents
hours: 6
area: BCA 302 · Artificial Intelligence · Unit 1
---

A thermostat that switches the heater off at 22 °C is not intelligent; a program that beats a grandmaster at chess, translates a Nepali sentence or recognises a face probably is. Where is the line? Artificial intelligence (AI) is the branch of computer science that tries to build systems that perceive, reason, learn and act, and it has a surprisingly practical core: **an agent that picks actions to maximise a measurable goal**. This unit defines AI, sketches its foundations and applications, and introduces the *agent* view that organises the rest of the book.

::: key What this unit gives you
- Definitions of AI (the four approaches), weak versus strong AI, the Turing test.
- Foundations and history of AI; applications, including ones relevant in Nepal.
- Intelligent agents: PEAS descriptions, agent types and properties of environments.
:::

## 1.1 What is artificial intelligence?

There is no single definition. Russell and Norvig group the many definitions into four approaches, arranged by whether they care about *thought* or *behaviour*, and about *human* performance or *ideal* (rational) performance.

| | Human-like | Rational (ideal) |
|---|---|---|
| **Thinking** | Cognitive modelling: build programs that think the way people do | Laws of thought: logic-based reasoning |
| **Acting** | The Turing test approach: behave so that a person cannot tell | The **rational agent** approach: act to achieve the best expected outcome |

Most modern AI follows the last cell: a **rational agent** is one that does the right thing given what it knows. Rationality is not omniscience (the agent cannot know everything) and not perfection (it maximises *expected* performance), and it depends on the task, not on resembling people. Aeroplanes do not flap their wings; the goal was flying, not imitating birds.

### The Turing test

Alan Turing (1950) proposed replacing the question "can machines think?" with an *imitation game*: a human judge converses in writing with a hidden human and a hidden machine; if the judge cannot reliably tell which is which, the machine passes. To pass it needs natural language processing, knowledge representation, automated reasoning and machine learning; the *total* Turing test adds computer vision and robotics. Critics note that the test rewards deception and chat tricks. **Searle's Chinese Room** argument says a program could manipulate symbols to produce correct answers without any understanding.

### Weak AI and strong AI

**Weak (narrow) AI** builds systems that perform specific tasks intelligently (spam filtering, route planning, a chess engine, speech recognition); every working AI system today is of this kind. **Strong AI** (artificial general intelligence) is the hypothesis that a machine could genuinely *have* a mind and general intelligence matching or exceeding a human's across tasks. It remains a goal and a subject of philosophical debate rather than a product. Related terms: **machine learning** (systems that improve with data) is a *subfield* of AI; **deep learning** is a subfield of machine learning based on many-layered neural networks.

## 1.2 Foundations of AI

AI borrows from many disciplines.

| Discipline | What it contributed |
|---|---|
| Philosophy | logic, reasoning, the mind–body question, rationality |
| Mathematics | formal logic, probability, computability, optimisation |
| Economics | utility theory and decision theory, game theory |
| Neuroscience | the brain as a network of neurons, inspiration for neural nets |
| Psychology | models of perception, memory and problem solving |
| Computer engineering | fast hardware (CPUs, GPUs), software, data |
| Control theory | feedback and optimal control of systems |
| Linguistics | grammar and the structure of language |

### A short history

- **1943** McCulloch and Pitts model an artificial neuron. **1950** Turing's paper. **1956** the Dartmouth workshop names the field "artificial intelligence".
- **1950s–60s** optimism: theorem provers, the General Problem Solver, early game programs, the perceptron (1958), ELIZA (1966).
- **1970s** the first **AI winter**: promises outran results; Minsky and Papert show a single perceptron cannot compute XOR (1969); funding falls.
- **1980s** **expert systems** (MYCIN, XCON) make money; the back-propagation algorithm revives neural networks; then a second winter as expert systems prove brittle and costly to maintain.
- **1990s–2000s** the **probabilistic turn** (Bayesian networks, statistical learning), support vector machines, speech recognition; Deep Blue beats the world chess champion (1997).
- **2010s** large datasets, GPUs and deep networks: ImageNet breakthrough (2012), AlphaGo (2016), transformer language models (2017); **2020s** large language models and generative AI.

## 1.3 Applications of AI

- **Language**: machine translation, speech-to-text, chatbots, search engines, spell checking. In Nepal: Devanagari OCR, Nepali speech recognition and text-to-speech for accessibility, mobile keyboards with Nepali prediction.
- **Vision**: face unlock, medical imaging (finding tumours on X-rays), number-plate recognition for traffic, satellite images for crop and flood monitoring.
- **Recommendation and prediction**: what to watch or buy, credit scoring, fraud detection for digital payments, demand forecasting.
- **Robotics and control**: industrial robots, drones, self-driving cars, smart agriculture.
- **Games and planning**: chess and Go engines, route planning in maps, timetabling and logistics.
- **Healthcare and education**: symptom checkers, personalised tutoring.

Every one of these is a mix of search (Unit 2), knowledge and reasoning (Unit 3), learning (Unit 4), neural networks and language (Unit 5), and rule-based or perceptual systems (Unit 6).

::: caution AI in society
AI systems inherit the biases in their training data, can be wrong with confidence, and consume personal data. A model that predicts loan defaults from past decisions can reproduce past discrimination. Treat AI output as evidence to check, not as an oracle, and see the ethics of Society and Technology (BCA 305) later this semester.
:::

## 1.4 Intelligent agents

An **agent** is anything that **perceives** its **environment** through **sensors** and **acts** on it through **actuators**. A human agent has eyes and ears and hands; a robot has cameras and motors; a software agent has keystrokes, files and network packets as percepts and actions. The **percept sequence** is everything perceived so far. The **agent function** maps every possible percept sequence to an action; the **agent program** is its concrete implementation.

A **rational agent** chooses, for each percept sequence, the action expected to maximise its **performance measure**, given the built-in knowledge it has. The performance measure belongs to the *designer's* idea of success in the environment, not to the agent's idea of its own behaviour. Rewarding a vacuum cleaner by the amount of dirt it sucks up would teach it to dump dirt and suck it again; a better measure is the number of clean squares over time.

### PEAS descriptions

To design an agent, first specify the task environment as **P**erformance measure, **E**nvironment, **A**ctuators and **S**ensors.

| Agent | Performance | Environment | Actuators | Sensors |
|---|---|---|---|---|
| Self-driving taxi | safe, fast, legal, comfortable trip, profit | roads, traffic, pedestrians, weather | steering, accelerator, brake, signals, horn | cameras, radar, GPS, speedometer |
| Medical diagnosis system | healthy patient, low cost | patient, hospital, staff | questions, tests, treatments | symptoms, test results, answers |
| Spam filter | few false positives and false negatives | mailbox, mail stream | mark spam, delete, move | message text, headers, sender |
| Tutoring system | student's test score | students, curriculum | exercises, hints, feedback | answers, response time |
| Crop-health drone | accurate disease map, flight time | fields, weather | motors, camera gimbal | camera, GPS, battery sensor |

### Properties of intelligent agents

An intelligent agent is **autonomous** (acts without constant human direction), **reactive** (responds to changes in time), **proactive** (pursues goals rather than just reacting), **social** (communicates with other agents or people) and, in many designs, able to **learn** from experience.

### Types of agents

1. **Simple reflex agent**: chooses an action from the *current* percept only, by condition–action rules (if the car in front brakes, then brake). Fast, tiny, works only if the correct decision can be made from the current percept (a fully observable environment); can loop forever otherwise.
2. **Model-based reflex agent**: keeps an internal **state** that tracks the part of the world it cannot see now, updated using a model of how the world evolves and how its own actions affect it (remembering which squares are clean).
3. **Goal-based agent**: knows what it wants (reach the destination) and considers the future consequences of actions; uses **search** and **planning** (Unit 2). More flexible: change the goal and the behaviour changes.
4. **Utility-based agent**: when goals can be reached in many ways, a **utility function** scores states (speed, safety, cost) and the agent maximises *expected utility*, trading off conflicting goals and handling uncertainty.
5. **Learning agent**: has a **performance element** (the agent above), a **critic** that tells how well it is doing against a standard, a **learning element** that improves the performance element and a **problem generator** that suggests exploratory actions.

### Environment types

| Property | Choice | Example of the first | Example of the second |
|---|---|---|---|
| Observability | fully / partially observable | chess | taxi driving, poker |
| Agents | single / multi-agent (competitive or cooperative) | crossword | chess, traffic |
| Determinism | deterministic / stochastic | chess moves | taxi driving |
| Episodic | episodic / sequential | classifying images | chess, driving |
| Dynamics | static / dynamic (semi-dynamic if only the score changes with time) | crossword | taxi, chess with a clock (semi) |
| State space | discrete / continuous | chess | taxi driving |
| Knowledge | known / unknown rules | chess | a new video game |

The hardest case is **partially observable, multi-agent, stochastic, sequential, dynamic, continuous and unknown**, which describes real driving.

## Practising the commands

This program implements the two-square vacuum world with a simple reflex agent and a model-based agent, and compares their performance measure (clean squares per time step, summed over 10 steps) from several starting situations.

```python
def reflex(percept, memory):
    loc, dirty = percept
    return "suck" if dirty else ("right" if loc == "A" else "left"), memory

def model_based(percept, memory):
    loc, dirty = percept
    memory = dict(memory); memory[loc] = "dirty" if dirty else "clean"
    if dirty: return "suck", memory
    if memory.get("A") == "clean" and memory.get("B") == "clean": return "stop", memory
    return ("right" if loc == "A" else "left"), memory

def run(agent, start, dirt, steps=10):
    loc, dirty, memory, score, moves = start, set(dirt), {}, 0, 0
    for _ in range(steps):
        action, memory = agent((loc, loc in dirty), memory)
        if action == "suck": dirty.discard(loc)
        elif action == "right": loc = "B"; moves += 1
        elif action == "left": loc = "A"; moves += 1
        score += 2 - len(dirty)
    return score, moves

for dirt in (("A", "B"), ("B",), ()):
    print("dirt", dirt, "reflex", run(reflex, "A", dirt), "model-based", run(model_based, "A", dirt))
```
```output
dirt ('A', 'B') reflex (18, 8) model-based (18, 1)
dirt ('B',) reflex (19, 9) model-based (19, 1)
dirt () reflex (20, 10) model-based (20, 1)
```
Both agents clean the same squares at the same time, so their scores are equal, but the reflex agent keeps shuffling between the squares after the room is clean (8, 9 and 10 moves in the three runs) while the model-based agent, which remembers that both squares are clean, makes at most one move and then stops. A performance measure that also charged for movement would separate them clearly.

## 1.5 Seeing the ideas: people, machines, agents and environments

Artificial intelligence is easier to understand when the ideas are drawn and computed. Plate 1.1 shows three founders of the field: Alan Turing (the imitation game), John McCarthy (who named the field in 1956 and invented the Lisp language) and Marvin Minsky (neural networks, frames and the first AI laboratory). Plate 1.2 shows four milestones as real machines: IBM's Deep Blue (the chess computer that beat the world champion in 1997), Shakey (the first robot to reason about its own actions), the first Roomba (a commercial reactive agent) and a Waymo self-driving car (the hardest agent in this unit). Plate 1.3 shows the simplest agent, a thermostat, next to its percept-action rule. The figures then compute the unit's ideas: the four approaches, the agent loop, a vacuum-cleaner simulation, a PEAS description, the five agent architectures, the learning agent, a table of environment properties, the Turing test, a timeline to scale and a rational decision under uncertainty.

```photogrid label="1.1" cols="3" ratio="1.0" caption="Three founders. (a) Alan Turing in 1951 (public domain), who proposed the imitation game in 1950 and showed what a machine can compute. (b) John McCarthy (CC BY 2.0), who coined the term 'artificial intelligence' for the 1956 Dartmouth workshop and created Lisp, the language of early AI. (c) Marvin Minsky (CC BY-SA 2.0), co-founder of the MIT AI laboratory, whose 1969 book with Seymour Papert showed that a single-layer perceptron cannot compute XOR."
@ photo id="bca302/turing" cap="Alan Turing: imitation game"
fit 1.0
focus 0.5 0.3
@ photo id="bca302/mccarthy" cap="John McCarthy: named AI (1956)"
fit 1.0
focus 0.4 0.4
@ photo id="bca302/minsky" cap="Marvin Minsky: MIT AI Lab"
fit 1.0
focus 0.5 0.35
```

```photogrid label="1.2" cols="4" ratio="1.0" caption="Four milestones. (a) IBM Deep Blue (CC BY 2.0), a rack of 30 processors with 480 special chess chips that beat world champion Garry Kasparov 3.5 to 2.5 in 1997 by searching about 200 million positions a second. (b) Shakey, built at SRI in 1966-1972 (CC BY-SA 4.0), the first mobile robot that planned its own actions with logic and search; the A* algorithm and the STRIPS planner came from it. (c) The first Roomba of 2002 (CC BY 4.0), a cheap reactive agent that bumps, turns and follows simple rules. (d) A Waymo self-driving car (CC BY-SA 4.0), whose roof carries the sensors of a utility-based learning agent."
@ photo id="bca302/deepblue" cap="Deep Blue (1997)"
fit 1.0
focus 0.5 0.35
@ photo id="bca302/shakey" cap="Shakey the robot (1969)"
fit 1.0
focus 0.5 0.4
@ photo id="bca302/roomba" cap="Roomba: reactive agent"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/waymo" cap="Self-driving car"
fit 1.0
focus 0.5 0.55
```

```photogrid label="1.3" cols="2" ratio="1.33" caption="The simplest agent. (a) A room thermostat (CC0): its sensor is a bimetal thermometer and its actuator switches the heater. (b) Its whole agent program is one condition-action rule per percept, so it is a simple reflex agent: it needs no memory and no model of the room, and it works because the room is fully observable at the thermometer."
@ photo id="bca302/thermostat" cap="Thermostat: sensor and actuator"
fit 1.33
focus 0.5 0.5
@ svg cap="A simple reflex agent"
f = Fig(300, 226)
f.text(150, 16, "thermostat agent program", size=13, color=NAVY, bold=True)
rules = [("percept: temp below 20", "action: heater ON", "#fee2e2", RED), ("percept: 20 to 22", "action: no change", SAND, AMBER), ("percept: temp above 22", "action: heater OFF", BLUE, NAVY)]
for i, (a, b, fl, st) in enumerate(rules):
    y = 28 + i * 56
    f.box(6, y, 288, 48, a + "\n" + b, fill=fl, stroke=st, size=12.5, r=6, color=NAVY, bold=True)
f.text(150, 208, "no memory, no model: percept to action", size=12, color=SLATE, bold=True)
```

```svgfig label="1.1" caption="The four approaches to defining AI. The rows ask whether the goal is thinking or acting; the columns ask whether the standard is human performance or ideal (rational) performance. Cognitive modelling builds programs that think the way people do; the laws-of-thought approach uses logic; the Turing-test approach tries to behave so that a person cannot tell it from a human; and the rational-agent approach (highlighted) acts to achieve the best expected outcome. Most modern AI follows the rational-agent approach because it works for any task and does not need to imitate people, just as aeroplanes do not flap their wings."
f = Fig(580, 252)
f.text(150, 18, "human-like", size=11, color=NAVY, bold=True)
f.text(430, 18, "rational (ideal)", size=11, color=NAVY, bold=True)
cells = [(0, 0, "Cognitive modelling\nbuild programs that think\nlike people\nexample: models of memory", BLUE, NAVY), (1, 0, "Laws of thought\nlogic-based reasoning\n\nexample: a theorem prover", BLUE, NAVY), (0, 1, "Turing test approach\nbehave so a judge cannot\ntell you from a human\nexample: a chatbot", SAND, AMBER), (1, 1, "RATIONAL AGENT\nact for the best expected\noutcome\nexample: a route planner", MINT, TEAL)]
for c, r, t, fl, st in cells:
    f.box(8 + c * 284, 28 + r * 112 + (0 if r == 0 else 6), 276, 100, t, fill=fl, stroke=st, size=11, r=8, color=NAVY, bold=(c == 1 and r == 1), sw=2.4 if (c == 1 and r == 1) else 1.4)
```

```svgfig label="1.2" caption="The agent-environment loop. Sensors turn the state of the environment into percepts; the agent program (an implementation of the agent function that maps percept sequences to actions) chooses an action; actuators carry it out and change the environment. The designer's performance measure judges the sequence of environment states that results, not the agent's own opinion of itself. A human agent has eyes, ears and hands, a robot has cameras and motors, and a software agent has files and network packets as its percepts and actions."
f = Fig(580, 236)
f.text(290, 14, "performance measure judges the sequence of environment states", size=10.5, color=RED, bold=True)
f.box(10, 150, 560, 70, "", fill="#f1f5f9", stroke="#94a3b8", r=8, sw=1.4)
f.text(290, 172, "ENVIRONMENT", size=12, color=SLATE, bold=True)
f.text(290, 194, "roads, rooms, mailboxes, a chess board: whatever the agent acts on", size=10, color=SLATE)
f.box(10, 46, 144, 46, "SENSORS\n(cameras, keys, packets)", fill=BLUE, stroke=NAVY, size=9.5, r=6, bold=True, color=NAVY)
f.box(206, 36, 170, 66, "AGENT PROGRAM\nagent function:\npercept sequence to action", fill=MINT, stroke=TEAL, size=10, r=8, bold=True, color=NAVY, sw=2)
f.box(426, 46, 144, 46, "ACTUATORS\n(wheels, screen, send)", fill=SAND, stroke=AMBER, size=9.5, r=6, bold=True, color=NAVY)
f.arrow([(82, 150), (82, 92)], color=NAVY, sw=2, label="percepts", lpos=(120, 124), lsize=10.5)
f.arrow([(154, 69), (206, 69)], color=NAVY, sw=2)
f.arrow([(376, 69), (426, 69)], color=AMBER, sw=2)
f.arrow([(496, 92), (496, 150)], color=AMBER, sw=2, label="actions", lpos=(536, 124), lsize=10.5)
```

```svgfig label="1.3" caption="A simple reflex vacuum cleaner simulated in the figure code. The world has two squares A and B, both dirty at the start, and the agent starts in A. The rule is: if the current square is dirty, suck; otherwise move to the other square. The performance measure gives 1 point for each clean square at the end of every time step. In 8 steps the agent scores 1, 1, 2, 2, 2, 2, 2, 2 = 14 points (the figure computes each step). Rewarding 'dirt sucked' instead would teach the agent to dump dirt and suck it up again, collecting a point every second step forever, which shows why the performance measure must describe the outcome the designer wants: clean squares over time."
f = Fig(580, 268)
dirty = {"A": True, "B": True}
loc = "A"
rows = []
total = 0
for t in range(8):
    if dirty[loc]:
        act = "Suck"; dirty[loc] = False
    else:
        act = "Right" if loc == "A" else "Left"
        newloc = "B" if loc == "A" else "A"
    here = loc
    if act != "Suck":
        loc = newloc
    clean = sum(1 for v in dirty.values() if not v)
    total += clean
    rows.append((here, act, dict(dirty), loc, clean))
assert total == 14
f.text(290, 14, "step: percept -> action; squares after the action (red = dirty, green = clean)", size=10.5, color=NAVY, bold=True)
for t, (here, act, d, newloc, clean) in enumerate(rows):
    x = 8 + t * 71
    f.text(x + 32, 32, "t = %d" % t, size=10, color=SLATE, bold=True)
    for k, sq in enumerate("AB"):
        f.box(x, 40 + k * 40, 64, 34, "", fill="#fecaca" if d[sq] else "#bbf7d0", stroke=RED if d[sq] else TEAL, r=4, sw=1.3)
        f.text(x + 10, 57 + k * 40, sq, size=10, color=NAVY, bold=True)
        if newloc == sq:
            f.poly([(x + 40, 48 + k * 40), (x + 58, 57 + k * 40), (x + 40, 66 + k * 40)], fill=NAVY, stroke=NAVY, sw=1)
    f.text(x + 32, 134, act, size=10.5, color=NAVY, bold=True)
    f.text(x + 32, 150, "at %s" % here, size=9.5, color=SLATE)
    f.box(x + 8, 160, 48, 24, "+%d" % clean, fill=SAND, stroke=AMBER, size=11, r=4, bold=True, color=NAVY)
f.text(290, 204, "reward: 1 point per clean square per step  ->  total = %d points" % total, size=11, color=RED, bold=True)
f.box(8, 216, 564, 40, "Perverse measure 'reward per dirt sucked': the agent can suck, dump the dirt and suck again for 1 point every 2 steps\nwithout ever making the room cleaner, so measure the outcome (clean squares), not the activity (dirt sucked)", fill=BLUE, stroke=NAVY, size=9.5, r=5, color=NAVY)
```

```svgfig label="1.4" caption="The PEAS description of a self-driving taxi, the four parts of a task environment. Performance measure: a safe, fast, legal, comfortable trip and profit. Environment: roads, traffic, pedestrians and weather. Actuators: steering, accelerator, brake, signals and horn. Sensors: cameras, radar, GPS and a speedometer. Writing the PEAS description first forces the designer to decide what success means and what the agent can sense and do, and it reveals the difficulty of the environment: this one is partially observable, multi-agent, stochastic, sequential, dynamic and continuous (Fig. 1.7)."
f = Fig(580, 266)
q = [(8, 8, "P  PERFORMANCE MEASURE\nsafe, fast, legal, comfortable\ntrip, profit", MINT, TEAL), (302, 8, "E  ENVIRONMENT\nroads, traffic, pedestrians,\nweather, road signs", BLUE, NAVY), (8, 152, "A  ACTUATORS\nsteering, accelerator, brake,\nindicators, horn", SAND, AMBER), (302, 152, "S  SENSORS\ncameras, radar, GPS, lidar,\nspeedometer", "#fce7f3", "#9d174d")]
for x, y, t, fl, st in q:
    f.box(x, y, 270, 106, t, fill=fl, stroke=st, size=11, r=8, color=NAVY, bold=True)
f.circle(290, 133, 54, fill="#e0e7ff", stroke=NAVY, sw=2, label="self-driving\ntaxi", size=11)
```

```svgfig label="1.5" caption="The four basic agent architectures. A simple reflex agent maps the current percept straight to an action by condition-action rules. A model-based reflex agent keeps an internal state, updated with knowledge of how the world evolves and what its own actions do, so it can act on what it cannot see now. A goal-based agent predicts the result of each possible action and picks one that reaches its goal. A utility-based agent also scores how happy each predicted state would make it, so it can trade off speed against safety and handle uncertainty. Each step to the right adds one box and one capability."
f = Fig(580, 372)
def panel(x0, y0, title, stack, side, col):
    f.text(x0 + 140, y0 + 10, title, size=11, color=col, bold=True)
    f.box(x0 + 4, y0 + 22, 100, 32, "SENSORS", fill=BLUE, stroke=NAVY, size=9.5, r=4, bold=True, color=NAVY)
    for j, s in enumerate(side):
        f.box(x0 + 4, y0 + 66 + j * 44, 100, 38, s, fill="#f1f5f9", stroke="#64748b", size=9.5, r=4, color=NAVY)
        f.arrow([(x0 + 104, y0 + 85 + j * 44), (x0 + 118, y0 + 85 + j * 44)], color="#64748b", sw=1.3)
    for i, s in enumerate(stack):
        last = i == len(stack) - 1
        f.box(x0 + 118, y0 + 22 + i * 36, 160, 28, s, fill=SAND if last else MINT, stroke=AMBER if last else TEAL, size=9.5, r=4, color=NAVY, bold=last)
        if i:
            f.arrow([(x0 + 198, y0 + 22 + i * 36 - 8), (x0 + 198, y0 + 22 + i * 36)], color=SLATE, sw=1.3)
    f.arrow([(x0 + 104, y0 + 38), (x0 + 118, y0 + 38)], color=NAVY, sw=1.5)
panel(6, 4, "1  simple reflex", ["what the world is like now", "condition-action rules", "ACTUATORS: action now"], [], NAVY)
panel(296, 4, "2  model-based reflex", ["state of the world (kept)", "condition-action rules", "ACTUATORS: action now"], ["how the world\nevolves", "what my actions\ndo"], NAVY)
panel(6, 190, "3  goal-based", ["state of the world", "predicted state if I do A", "goals: pick best action", "ACTUATORS: action now"], ["how the world\nevolves", "what my actions\ndo"], TEAL)
panel(296, 190, "4  utility-based", ["state of the world", "predicted state if I do A", "utility: how happy am I?", "ACTUATORS: action now"], ["how the world\nevolves", "what my actions\ndo"], AMBER)
```

```svgfig label="1.6" caption="The learning agent adds four parts to the performance element (the agent of Fig. 1.5). The performance standard says what counts as good; the critic compares the percepts with that standard and reports how well the agent is doing; the learning element uses the critic's feedback to change the performance element, for example by adjusting a rule or a weight; and the problem generator suggests exploratory actions that may be worse now but teach something new. A spam filter fits this picture: the user pressing 'report spam' is the critic's feedback."
f = Fig(580, 240)
f.box(8, 16, 120, 38, "performance\nstandard", fill="#f1f5f9", stroke="#64748b", size=10, r=5, bold=True, color=NAVY)
f.box(150, 16, 90, 38, "CRITIC", fill=SAND, stroke=AMBER, size=10.5, r=5, bold=True, color=NAVY)
f.box(266, 16, 130, 38, "LEARNING\nELEMENT", fill=MINT, stroke=TEAL, size=10.5, r=5, bold=True, color=NAVY)
f.box(430, 16, 140, 38, "PROBLEM\nGENERATOR", fill="#e0e7ff", stroke=NAVY, size=10.5, r=5, bold=True, color=NAVY)
f.box(8, 108, 96, 42, "SENSORS", fill=BLUE, stroke=NAVY, size=10.5, r=5, bold=True, color=NAVY)
f.box(210, 108, 180, 42, "PERFORMANCE\nELEMENT (the agent)", fill=MINT, stroke=TEAL, size=10.5, r=5, bold=True, color=NAVY, sw=2)
f.box(476, 108, 96, 42, "ACTUATORS", fill=SAND, stroke=AMBER, size=10.5, r=5, bold=True, color=NAVY)
f.box(8, 188, 564, 40, "ENVIRONMENT", fill="#f1f5f9", stroke="#94a3b8", size=11, r=6, bold=True, color=SLATE)
f.arrow([(128, 35), (150, 35)], color=SLATE, sw=1.5)
f.arrow([(240, 35), (266, 35)], color=SLATE, sw=1.5)
f.arrow([(56, 108), (56, 74), (195, 74), (195, 54)], color=NAVY, sw=1.5)
f.arrow([(331, 54), (331, 108)], color=TEAL, sw=2, label="changes", lpos=(366, 84), lsize=9.5)
f.arrow([(470, 54), (380, 108)], color=NAVY, sw=1.5, label="experiments", lpos=(462, 90), lsize=9.5)
f.arrow([(104, 129), (210, 129)], color=NAVY, sw=2, label="percepts", lpos=(157, 122), lsize=9.5)
f.arrow([(390, 129), (476, 129)], color=AMBER, sw=2, label="actions", lpos=(433, 122), lsize=9.5)
f.arrow([(56, 188), (56, 150)], color=NAVY, sw=2)
f.arrow([(524, 150), (524, 188)], color=AMBER, sw=2)
f.text(66, 68, "feedback", size=9.5, color=NAVY, bold=True, anchor="start")
```

```svgfig label="1.7" caption="How hard is the environment? Each row is a task and each column a property; a red dot means the hard side of that property (partially observable, multi-agent, stochastic, sequential, dynamic, continuous, unknown rules). The score is the number of red dots, computed from the table: an image classifier scores 0, a crossword 1, chess 2, poker 4 and taxi driving 6. Agent designs get more complex as the score rises: a lookup rule is enough for a classifier of single images, search is enough for chess, and probability and learning are needed for poker and driving."
f = Fig(580, 270)
props = ["partly\nobservable", "multi-\nagent", "stochastic", "sequential", "dynamic", "continuous", "unknown\nrules"]
tasks = [("image classifier", [0, 0, 0, 0, 0, 0, 0]), ("crossword", [0, 0, 0, 1, 0, 0, 0]), ("chess (no clock)", [0, 1, 0, 1, 0, 0, 0]), ("poker", [1, 1, 1, 1, 0, 0, 0]), ("taxi driving", [1, 1, 1, 1, 1, 1, 0])]
sc = [sum(v) for _, v in tasks]
assert sc == [0, 1, 2, 4, 6]
for j, p in enumerate(props):
    f.text(176 + j * 52, 22, p, size=9.5, color=NAVY, bold=True)
f.text(550, 22, "hard\nscore", size=9.5, color=RED, bold=True)
for i, (nm, v) in enumerate(tasks):
    y = 56 + i * 40
    f.box(6, y - 14, 568, 32, "", fill="#f8fafc" if i % 2 == 0 else "#ffffff", stroke="#e2e8f0", r=3, sw=1)
    f.text(12, y + 2, nm, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    for j, b in enumerate(v):
        f.circle(176 + j * 52, y + 2, 8, fill="#ef4444" if b else "#e2e8f0", stroke=RED if b else "#94a3b8", sw=1.2)
    f.text(550, y + 2, "%d / 7" % sc[i], size=11, color=RED if sc[i] > 3 else TEAL, bold=True, vmid=True)
f.text(290, 262, "red = hard side:  the more red dots, the more machinery the agent needs", size=10, color=SLATE)
```

```svgfig label="1.8" caption="The imitation game (Turing test). A judge in one room types questions to two hidden players, a human and a machine, and reads their typed answers. If the judge cannot reliably say which is the machine, the machine passes. To pass, a machine needs natural language processing (to talk), knowledge representation (to store what it knows), automated reasoning (to answer from it) and machine learning (to adapt); the total Turing test adds computer vision and robotics. Critics say the test rewards trickery, and Searle's Chinese Room argues that manipulating symbols correctly is not the same as understanding them."
f = Fig(580, 250)
f.box(8, 80, 100, 70, "JUDGE\nasks by typing", fill=BLUE, stroke=NAVY, size=10.5, r=8, bold=True, color=NAVY)
f.box(170, 20, 120, 70, "player A\n(hidden)", fill="#f1f5f9", stroke="#64748b", size=10.5, r=8, dash=True, color=SLATE)
f.box(170, 130, 120, 70, "player B\n(hidden)", fill="#f1f5f9", stroke="#64748b", size=10.5, r=8, dash=True, color=SLATE)
f.arrow([(108, 100), (170, 58)], color=NAVY, sw=1.8, both=True)
f.arrow([(108, 130), (170, 170)], color=NAVY, sw=1.8, both=True)
f.text(139, 70, "Q / A", size=9.5, color=NAVY, bold=True)
f.text(139, 160, "Q / A", size=9.5, color=NAVY, bold=True)
f.text(230, 224, "one is a human, one is a machine", size=10, color=SLATE)
f.text(60, 176, "cannot tell which?", size=10, color=RED, bold=True)
f.text(60, 192, "the machine passes", size=10, color=RED, bold=True)
caps = [("natural language processing", MINT, TEAL), ("knowledge representation", MINT, TEAL), ("automated reasoning", MINT, TEAL), ("machine learning", MINT, TEAL), ("TOTAL test adds: computer vision", SAND, AMBER), ("TOTAL test adds: robotics", SAND, AMBER)]
f.text(440, 14, "what the machine needs", size=10.5, color=NAVY, bold=True)
for i, (t, fl, st) in enumerate(caps):
    f.box(320, 26 + i * 34, 250, 28, t, fill=fl, stroke=st, size=10, r=4, color=NAVY, bold=True)
```

```svgfig label="1.9" caption="The history of AI to scale, 1940-2025, with the two AI winters shaded (roughly 1974-1980 and 1987-1993). The artificial neuron (1943), Turing's paper (1950), the Dartmouth workshop (1956), the perceptron (1958) and ELIZA (1966) belong to the early optimism; Minsky and Papert's XOR result (1969) began the first winter. Expert systems brought a boom and then a second winter. Deep Blue (1997) came from search; the ImageNet breakthrough (2012), AlphaGo (2016) and the transformer (2017) came from data, GPUs and deep learning, which led to today's large language models. The spacing shows how recent the deep-learning era is: it fills the last 13 of 85 years."
f = Fig(580, 270)
def X(y): return 14 + (y - 1940) * 6.6
f.box(X(1974), 100, X(1980) - X(1974), 70, "", fill="#dbeafe", stroke="#93c5fd", r=0, sw=1)
f.box(X(1987), 100, X(1993) - X(1987), 70, "", fill="#dbeafe", stroke="#93c5fd", r=0, sw=1)
f.text(X(1977), 182, "winter 1", size=9.5, color=NAVY, bold=True)
f.text(X(1990), 182, "winter 2", size=9.5, color=NAVY, bold=True)
f.line(X(1940), 134, X(2025), 134, color=SLATE, sw=3)
for yr in range(1940, 2026, 10):
    f.line(X(yr), 128, X(yr), 140, color=SLATE, sw=1.5)
    f.text(X(yr), 154, str(yr), size=9.5, color=SLATE)
ev = [(1943, "neuron", 1), (1950, "Turing", 2), (1956, "Dartmouth", 3), (1958, "perceptron", 4), (1966, "ELIZA", 1), (1969, "XOR limit", 2), (1980, "expert systems", 3), (1986, "backprop", 4), (1997, "Deep Blue", 1), (2012, "ImageNet", 2), (2016, "AlphaGo", 3), (2017, "transformer", 4)]
for yr, nm, lv in ev:
    up = lv in (1, 3)
    y0 = 134 - (20 if lv == 1 else 58) if up else 134 + (46 if lv == 2 else 70)
    ytxt = y0 - 6 if up else y0 + 12
    f.line(X(yr), 134, X(yr), y0, color="#94a3b8", sw=1.2)
    f.circle(X(yr), 134, 4.5, fill="#fde68a", stroke=AMBER, sw=1.4)
    anc = "end" if yr >= 2012 else "middle"
    f.text(X(yr), ytxt, "%d %s" % (yr, nm), size=9.5, color=NAVY, bold=True, anchor=anc)
f.text(290, 262, "scale: 6.6 px per year; deep learning era (2012-2025) = 13 years of 85", size=9.5, color=SLATE)
```

```svgfig label="1.10" caption="A rational choice under uncertainty, computed. A taxi agent can take route A (always 30 minutes), route B (50 percent chance of 20 minutes, 50 percent of 50) or route C (80 percent chance of 25 minutes, 20 percent of 70). The expected times are 30, 35 and 34 minutes, and the chances of arriving within 40 minutes are 100, 50 and 80 percent. A rational agent maximises the expected value of the performance measure, so it picks route A on both counts; route B has the faster best case but is the worst bet. Rationality is therefore about the best expected result given what the agent knows, not about luck or perfection."
f = Fig(580, 260)
routes = [("A", [(1.0, 30)]), ("B", [(0.5, 20), (0.5, 50)]), ("C", [(0.8, 25), (0.2, 70)])]
exp = [sum(p * t for p, t in o) for _, o in routes]
within = [sum(p for p, t in o if t <= 40) for _, o in routes]
assert [round(e) for e in exp] == [30, 35, 34] and within == [1.0, 0.5, 0.8]
f.text(150, 14, "expected travel time (minutes)", size=10.5, color=NAVY, bold=True)
f.text(440, 14, "chance of arriving within 40 min", size=10.5, color=NAVY, bold=True)
best = exp.index(min(exp))
for i, ((nm, o), e, w) in enumerate(zip(routes, exp, within)):
    y = 34 + i * 62
    f.text(10, y + 18, "route " + nm, size=11, color=NAVY, bold=True, anchor="start", vmid=True)
    f.box(60, y, e * 4.2, 36, "", fill=MINT if i == best else SAND, stroke=TEAL if i == best else AMBER, r=3)
    f.text(60 + e * 4.2 + 6, y + 18, "%g" % e, size=11, color=RED, bold=True, anchor="start", vmid=True)
    f.box(330, y, w * 150, 36, "", fill=MINT if i == best else SAND, stroke=TEAL if i == best else AMBER, r=3)
    f.text(330 + w * 150 + 6, y + 18, "%d percent" % round(w * 100), size=11, color=RED, bold=True, anchor="start", vmid=True)
    f.text(60, y + 50, "outcomes: " + ", ".join("%d%% -> %d min" % (round(p * 100), t) for p, t in o), size=9.5, color=SLATE, anchor="start")
f.text(290, 238, "rational choice = route %s: lowest expected time and best chance of being on time" % routes[best][0], size=10.5, color=TEAL, bold=True)
```

### 1.5.1 Eight applications of AI in Nepal

1. **Reading and speaking Nepali.** Optical character recognition for Devanagari lets scanned books, citizenship certificates and old government records be searched as text. Speech recognition and text-to-speech help blind users and let people dictate messages in Nepali. These are narrow AI systems that combine language, vision and learning, and they work better as more Nepali text and recordings are collected.
2. **Fraud detection in digital payments.** Wallets and banks such as eSewa, Fonepay and ConnectIPS handle millions of small transfers, and a learning agent can flag an unusual one, for example a large amount sent at night from a new device. The system is a utility-based agent: it weighs the cost of stopping an honest customer against the cost of missing a thief. Humans check the flagged cases and the model learns from their decisions.
3. **Farming and flood monitoring.** Satellite images and drones, like the crop-health drone of the PEAS example, can show dry fields, plant disease or river-bank damage before people reach the place. A vision model turns pictures into a map that an agency can act on. This helps in a country where many farms are small and far apart.
4. **Health care and X-rays.** A program that finds signs of tuberculosis or pneumonia on a chest X-ray can help a district hospital that has few radiologists. It is a decision aid, not a doctor: it ranks the pictures that need attention first. Mistakes and bias in the training data must be checked before such a tool is used.
5. **Traffic and number plates.** Cameras in Kathmandu can read number plates to find vehicles that jump red lights or enter restricted roads. The program is a simple reflex agent for each frame (see a plate, record it) wrapped in a vision system. Privacy rules decide how long such images may be kept.
6. **Education and tutoring.** Learning apps adapt the next question to a student's answers, the same loop as the critic and learning element of Fig. 1.6. An exam-preparation app can find which topics a student keeps getting wrong. Teachers still decide the curriculum, and the system is checked against the student's real test score.
7. **Chatbots and translation.** Banks, telecom companies and government help desks use chatbots to answer common questions, and machine translation moves text between Nepali and English. These systems pass a small version of the Turing test only for narrow questions, and they fail on unusual ones. A human hand-over is needed for anything complicated.
8. **Search, recommendation and personal assistants.** Search engines, video sites and phone keyboards predict what you want to read, watch or type next in Nepali and English. Each is a rational agent that tries to maximise a measurable goal, such as the number of useful clicks. The risk is that the goal is not the same as the user's real interest, which is why the performance measure matters.

## Formula and fact sheet

- Rational agent: for each percept sequence choose the action that maximises the *expected* performance measure.
- PEAS = Performance measure, Environment, Actuators, Sensors.
- Agent types in increasing power: simple reflex → model-based reflex → goal-based → utility-based; any of them can be a learning agent.
- Environment properties: observable, deterministic, episodic, static, discrete, single-agent (the "easy" side).
- Turing test: a judge cannot distinguish the machine from a human by conversation.

## Chapter summary

- AI is the study of agents that act rationally. Four definitions (thinking or acting, humanly or rationally) co-exist; the rational-agent view is the most used.
- Weak AI solves specific tasks and is the only AI that exists; strong AI is a general machine mind and remains a hypothesis.
- AI draws on philosophy, mathematics, economics, neuroscience, psychology and computing; its history alternates enthusiasm and AI winters.
- An agent maps percepts to actions; PEAS specifies its task; agents range from simple reflex to learning agents; the environment type determines how hard the task is.

## Practice

1. Give the four approaches to AI with one sentence each.
2. What is the Turing test? State one criticism.
3. Differentiate weak AI from strong AI, and AI from machine learning.
4. Define a rational agent. Why is "rational" not the same as "perfect"?
5. Write a PEAS description for (a) a Nepali-language spam filter, (b) a robot that sorts tomatoes by ripeness.
6. Describe the five agent types with an example of each.
7. Classify chess, poker and taxi driving along the observability, determinism and episodic properties.
8. Why does a simple reflex vacuum cleaner with no memory loop forever when both squares are clean? How does the model-based agent in the program avoid it?
9. Name four applications of AI in Nepal's context and the technique each needs.
10. Name two risks of AI that arise from training data.

::: note Answers and worked solutions
**1.** Thinking humanly (cognitive modelling); thinking rationally (laws of thought, logic); acting humanly (Turing test); acting rationally (rational agents that maximise expected outcome).
**2.** A judge converses with a hidden human and a hidden machine; if the judge cannot tell them apart, the machine passes. Criticism: it measures imitation and deception, not understanding (Searle's Chinese Room).
**3.** Weak AI does particular tasks; strong AI would have general human-level intelligence and, on some definitions, a mind. Machine learning is a technique (learning from data) used within AI, and AI also includes search, logic and planning that need no learning.
**4.** An agent that acts to maximise the expected value of its performance measure given its percepts and knowledge. It is not perfect because it cannot know the future or all facts; it is the best choice in expectation.
**5.** (a) P: low false-positive and false-negative rate; E: a mailbox receiving Nepali and English mail; A: label, move, delete; S: message text, headers, sender reputation. (b) P: sorting accuracy and speed; E: conveyor of tomatoes, lighting; A: arm or air jets; S: colour camera, weight sensor.
**6.** Simple reflex (thermostat); model-based (a robot remembering which rooms are cleaned); goal-based (route planner); utility-based (a navigation app trading time against toll cost); learning (a spam filter that learns from user corrections).
**7.** Chess: fully observable, deterministic, sequential (and multi-agent). Poker: partially observable, stochastic, sequential. Taxi driving: partially observable, stochastic, sequential, dynamic. Image classification would be episodic.
**8.** With no memory, "if clean then move" bounces between A and B forever. The model-based agent records which squares are clean and returns "stop" once both are known to be clean.
**9.** Devanagari OCR (computer vision, pattern recognition); Nepali speech assistants (speech recognition, NLP); crop-disease detection from phone photos (image classification, learning); flood or landslide risk maps (prediction from satellite and rainfall data).
**10.** Bias reproduced from historical data; privacy loss from data collection; also confident but wrong output.
:::

## Model answers for Unit 1

**Q1. Define artificial intelligence. Explain the four approaches, the Turing test and the difference between weak and strong AI. (10 marks)**

**Introduction.** Artificial intelligence (AI) is the branch of computer science that builds systems which perceive, reason, learn and act. There is no single definition, so Russell and Norvig group the definitions along two questions: is the goal thinking or acting, and is the standard human performance or ideal (rational) performance (Fig. 1.1).

**The four approaches.**

| | Human-like | Rational (ideal) |
|---|---|---|
| Thinking | Cognitive modelling: programs that think like people | Laws of thought: logic-based reasoning |
| Acting | Turing test approach: behave so a judge cannot tell | Rational agent: act for the best expected outcome |

Most modern AI follows the rational-agent approach. A rational agent does the right thing given what it knows: it maximises the expected value of a performance measure. It is not omniscient and not perfect, and it does not have to imitate people; aeroplanes fly without flapping their wings.

**The Turing test.** In 1950 Alan Turing replaced "can machines think?" with the imitation game (Fig. 1.8). A judge converses in writing with a hidden human and a hidden machine; if the judge cannot reliably tell which is which, the machine passes. To pass, the machine needs natural language processing, knowledge representation, automated reasoning and machine learning; the total test adds computer vision and robotics. Critics say the test rewards deception, and Searle's Chinese Room argument claims that a program can manipulate symbols and give correct answers without any understanding.

**Weak and strong AI.** Weak (narrow) AI builds systems for specific tasks, such as spam filtering, route planning, speech recognition or a chess engine; every working AI system today is of this kind. Strong AI, or artificial general intelligence, is the hypothesis that a machine could really have a mind and general intelligence equal to or beyond a human's. It remains a research goal and a philosophical debate. Machine learning is a subfield of AI, and deep learning is a subfield of machine learning.

**Conclusion.** AI is best defined as the design of rational agents; the Turing test is historically important, but today's systems are narrow tools judged by how well they achieve measurable goals.

**Q2. What is an intelligent agent? Explain the types of agents with diagrams. (10 marks)**

**Introduction.** An agent is anything that perceives its environment through sensors and acts on it through actuators (Fig. 1.2). The agent function maps every percept sequence to an action, and the agent program implements it. A rational agent picks the action expected to maximise its performance measure. An intelligent agent is also autonomous, reactive, proactive, social and often able to learn.

**Types of agents (Fig. 1.5, Fig. 1.6).**

1. **Simple reflex agent.** It chooses an action from the current percept only, with condition-action rules, such as "if the car in front brakes, brake". It is fast and tiny but works only when the right decision can be made from the current percept; in a partially observable world it can loop forever.
2. **Model-based reflex agent.** It keeps an internal state that records what it cannot see now, updated using a model of how the world evolves and what its own actions do.
3. **Goal-based agent.** It predicts the result of each action and chooses one that reaches its goal, using search and planning. Changing the goal changes the behaviour without rewriting rules.
4. **Utility-based agent.** A utility function scores states (speed, safety, cost), and the agent maximises expected utility, which lets it trade off conflicting goals and handle uncertainty.
5. **Learning agent.** It adds a critic, a learning element and a problem generator to a performance element, so it improves with experience.

| Agent | Uses | Limitation |
|---|---|---|
| Simple reflex | current percept | needs full observability |
| Model-based | percept and internal state | needs a good model |
| Goal-based | search toward a goal | cannot rank equal goals |
| Utility-based | expected utility | needs probabilities and a utility |
| Learning | feedback from a critic | needs data and exploration |

**Example.** A thermostat is a simple reflex agent; a robot vacuum that remembers cleaned squares is model-based; a route planner is goal-based; a taxi that weighs time against safety is utility-based; and a spam filter that learns from "report spam" clicks is a learning agent.

**Conclusion.** The types form a ladder of increasing flexibility; any of them can be made a learning agent.

**Q3. Explain PEAS and the properties of task environments with examples. (10 marks)**

**Introduction.** Before designing an agent the designer specifies its task environment. The PEAS description lists the Performance measure, Environment, Actuators and Sensors, and the environment is then classified by its properties, which decide how complex the agent must be.

**PEAS example (Fig. 1.4).** For a self-driving taxi the performance measure is a safe, fast, legal, comfortable trip and profit; the environment is roads, traffic, pedestrians and weather; the actuators are steering, accelerator, brake, signals and horn; and the sensors are cameras, radar, lidar, GPS and a speedometer. For a spam filter the performance is few false positives and false negatives, the environment is the mail stream, the actuators mark or delete messages and the sensors read the text and headers.

**Environment properties.**

| Property | Easy side | Hard side |
|---|---|---|
| Observability | fully observable (chess) | partially observable (poker, driving) |
| Agents | single agent (crossword) | multi-agent (chess, traffic) |
| Determinism | deterministic (chess moves) | stochastic (driving) |
| Episodes | episodic (classifying images) | sequential (chess, driving) |
| Dynamics | static (crossword) | dynamic (taxi) |
| State space | discrete (chess) | continuous (driving) |
| Knowledge | known rules | unknown rules (a new game) |

**Difficulty.** Counting the hard sides gives a rough score (Fig. 1.7): an image classifier scores 0, a crossword 1, chess 2, poker 4 and taxi driving 6 of 7. A low score allows a simple agent: a fixed rule or a search is enough. A high score needs a model of the world, probabilities, learning and continuous control. Real driving is partially observable, multi-agent, stochastic, sequential, dynamic and continuous, so it is among the hardest tasks.

**Design consequences.** Each property changes the design. A partially observable world needs an internal state, because the agent cannot see everything at once. A stochastic world needs probabilities and expected utility, because the same action may have different results. A sequential world needs planning, because today's action changes tomorrow's options, and a dynamic world needs fast decisions, because the world does not wait. An unknown world needs learning. For a crop-health drone in Nepal's hills, for example, the weather is stochastic, the terrain is continuous and the battery limits the plan, so the drone needs a model of its battery and a planner, not just reflex rules.

**Conclusion.** Writing PEAS and classifying the environment first tells the designer what the agent must sense, remember and compute.

**Q4. What is a rational agent? Why is the performance measure important? (5 marks)**

A rational agent chooses, for every percept sequence, the action that is expected to maximise its performance measure, given what it knows. Rationality is not omniscience, because the agent cannot know everything, and not perfection, because it maximises the expected outcome, not the actual one. The performance measure is chosen by the designer and describes what success means in the environment.

A bad measure produces bad behaviour. In the two-square vacuum world of Fig. 1.3 the agent follows a simple rule: suck if the square is dirty, otherwise move. With the measure "one point per clean square per time step" it scores 1, 1, 2, 2, 2, 2, 2, 2 = 14 points in 8 steps. If we rewarded the amount of dirt sucked instead, the agent could dump the dirt and suck it again, collecting points while the room never gets cleaner. The measure should therefore describe the outcome we want (clean squares over time) rather than the activity of the agent.

The same idea appears with a taxi choosing between routes (Fig. 1.10): the rational choice is the route with the best expected result, not the one with the best lucky case.

**Q5. Describe the history of AI, including the AI winters. (5 marks)**

AI grew from several roots: in 1943 McCulloch and Pitts modelled an artificial neuron, in 1950 Turing wrote his paper on machine intelligence, and in 1956 the Dartmouth workshop, organised by John McCarthy and others, named the field (Fig. 1.9). The 1950s and 1960s were years of optimism: theorem provers, the General Problem Solver, the perceptron (1958), early game programs and the chatbot ELIZA (1966).

The first **AI winter** (about 1974 to 1980) followed when promises outran results; Minsky and Papert showed in 1969 that a single perceptron cannot compute XOR, and funding fell. In the 1980s **expert systems** such as MYCIN and XCON made money, and back-propagation revived neural networks, but expert systems proved brittle and costly to maintain, and a second winter followed (about 1987 to 1993).

The 1990s and 2000s brought the probabilistic turn (Bayesian networks, statistical learning, support vector machines) and Deep Blue's 1997 victory over the chess champion. Since 2010, large data sets, GPUs and deep networks gave the ImageNet breakthrough (2012), AlphaGo (2016), the transformer (2017) and today's large language models.

**Q6. List the applications of AI, with examples from Nepal. (5 marks)**

AI is used wherever a task needs perception, prediction or decision making. **Language**: machine translation, speech recognition, chatbots and search; in Nepal, Devanagari OCR for old records, Nepali text-to-speech for blind users and keyboards that predict Nepali words. **Vision**: face unlock, medical imaging such as X-ray screening, number-plate reading for traffic cameras, and satellite or drone images for crop and flood monitoring. **Prediction and recommendation**: credit scoring, demand forecasting and fraud detection in digital payments such as eSewa, Fonepay and ConnectIPS, where a model flags unusual transfers. **Robotics and control**: industrial robots, drones and self-driving vehicles. **Games and planning**: chess and Go engines, route planning in maps and timetabling. **Health and education**: symptom checkers and tutoring apps that adapt questions to the student.

Each application is a narrow AI agent with its own PEAS description and a measurable performance goal. AI also brings risks: systems inherit the bias in their training data, can be confidently wrong and use personal data, so their output must be treated as evidence to check, not as an oracle.

**Q7. Differentiate a simple reflex agent from a model-based reflex agent. (5 marks)**

A **simple reflex agent** selects an action from the current percept alone, using condition-action rules. A thermostat is the standard example (Plate 1.3): if the temperature is below 20 degrees, switch the heater on; if above 22, switch it off. It has no memory, so it works only when the current percept contains everything needed to decide, which means a fully observable environment. In a partially observable world it can behave badly: a vacuum cleaner that sees only "clean" in its own square may shuttle between two squares forever, as in Fig. 1.3.

A **model-based reflex agent** keeps an internal **state** that tracks the part of the world it cannot see now. The state is updated using two kinds of knowledge: how the world evolves independently of the agent, and what the agent's own actions do (Fig. 1.5). The vacuum cleaner can then remember which squares it has already cleaned and stop, and a taxi can remember a car that is in its blind spot.

| Feature | Simple reflex | Model-based reflex |
|---|---|---|
| Input | current percept | percept plus remembered state |
| Memory | none | internal state |
| Environment | fully observable | partially observable allowed |
| Cost | tiny, fast | needs a model and more memory |

**Q8. Explain the components of a learning agent. (5 marks)**

A learning agent can start with little knowledge and improve with experience, and it has four conceptual components (Fig. 1.6). The **performance element** is the agent of the previous types: it perceives and chooses actions. The **critic** looks at the percepts and tells the agent how well it is doing against a fixed **performance standard**; without it the agent would have no idea whether its behaviour is good. The **learning element** takes the critic's feedback and changes the performance element, for example by adjusting a rule, a weight or an estimated value, so that the agent does better next time. The **problem generator** suggests exploratory actions that may be worse in the short term but lead to new, informative experiences; without exploration the agent would repeat what it already knows.

For example, a spam filter's performance element marks messages as spam or not. When the user presses "report spam" or rescues a good message from the spam folder, that is the critic's feedback; the learning element updates the word statistics, and the problem generator occasionally lets a doubtful message through to check whether the filter's belief is right. Over months the filter becomes better with no new rules from the programmer.

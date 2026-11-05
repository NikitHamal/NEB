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

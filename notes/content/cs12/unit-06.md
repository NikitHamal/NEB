---
subject: Computer Science
grade: 12
unit: 6
title: Software Process Model (SPM)
hours: 10
---

Writing a 50-line program needs no plan. Building the software that prints the
NEB result of half a million students, or that runs a bank's mobile app, needs a
plan more than it needs clever code: what exactly must it do, who decides that,
in what order will the work happen, how will anyone know it is correct, and what
happens when the rules change next year. Software engineering is the answer to
those questions, and a **software process model** is a ready-made plan for the
order of the work. This unit covers the life cycle, the people, the
requirement-gathering methods, design, quality, and the models themselves —
which you must be able to **draw** as well as describe.

::: key What the exam asks from this unit
Group B favours *define SDLC and explain its phases*, *differentiate system
analyst and software engineer*, *explain any three requirement collection
methods*. Group C almost always asks you to **draw and explain** the waterfall,
prototype or spiral model, often with "state its advantages and disadvantages
and where it is suitable". Practise drawing each diagram from memory in under
three minutes.
:::

## 6.1 Software project concept

**Software** is the set of programs, associated data and documentation that make
a computer do useful work. A **software project** is a temporary, planned effort
with a fixed goal, a budget, a deadline and a team, which produces a software
product. "Temporary" is the key word: a project ends, a product lives on.

Every software project is managed along four constraints, and you cannot change
one without moving the others:

| Constraint | Question it answers | Typical measure |
|---|---|---|
| Scope | what will the software do? | list of features, requirement document |
| Time | when must it be delivered? | schedule, milestones, Gantt chart |
| Cost | what may it cost? | person-months × salary + hardware + licences |
| Quality | how good must it be? | defect rate, availability, usability targets |

The project manager plans the work (breaking it into tasks), estimates effort in
**person-months**, assigns people, tracks progress against milestones and
manages **risk** — anything that might go wrong: staff leaving, a requirement
changing, a vendor being late, an earthquake closing the office.

::: example Worked example 6.1 — estimating a project
**Problem.** A Kathmandu software house wins a contract to build a school
management system. The plan is 8 developers for 5 months. The average cost of a
developer is Rs 60,000 per month, hardware and licences cost Rs 3,00,000, and the
company adds 20 % of the total for management overhead and risk. What is the
estimated effort in person-months and the estimated cost?

**Solution.**

Effort $= 8 \times 5 = 40$ person-months.

Staff cost $= 40 \times 60{,}000 = \text{Rs } 24{,}00{,}000$.

Direct cost $= 24{,}00{,}000 + 3{,}00{,}000 = \text{Rs } 27{,}00{,}000$.

Overhead $= 0.20 \times 27{,}00{,}000 = \text{Rs } 5{,}40{,}000$.

Total estimated cost $= 27{,}00{,}000 + 5{,}40{,}000 = \text{Rs } 32{,}40{,}000$.

Note that effort and time are not interchangeable: putting 40 developers on the
job does not finish it in one month, because the communication paths between
$n$ people grow as $n(n-1)/2$ — with 40 people that is 780 channels.
:::

## 6.2 Concept of the software development process

A **software development process** is the set of activities, together with their
order, inputs and outputs, that turns a customer's need into working software
that stays working. Four activities appear in every process, whatever its name:

1. **Specification** — find out and write down what the software must do.
2. **Design and implementation** — decide the structure, then build it.
3. **Validation** — check that it does what the customer wanted.
4. **Evolution (maintenance)** — change it as needs change.

A **process model** (also called a software development life cycle model) is an
abstract description of how those activities are arranged in time: all at once in
one pass (waterfall), in repeated small passes (incremental, agile), or driven by
risk (spiral). Choosing the model is the first management decision of the
project.

::: caution Process ≠ life cycle ≠ model
The **process** is the activities you perform; the **SDLC** is the standard list
of phases those activities are grouped into; a **process model** is one
particular arrangement of those phases. In the exam, define the one that is
asked — marks are lost for answering "waterfall" when the question said "SDLC".
:::

## 6.3 Concept of the SDLC life cycle

::: definition System/Software Development Life Cycle
The SDLC is the structured sequence of phases — from the first study of the
problem to the retirement of the system — through which an information system
passes, each phase producing a defined deliverable that becomes the input of the
next.
:::

```figure caption="The software development life cycle. Each phase hands a deliverable to the next, and maintenance feeds new requirements back into the start — which is why it is drawn as a cycle, not a line."
from matplotlib.patches import FancyArrowPatch, Ellipse
fig, ax = plt.subplots(figsize=(5.0, 4.0))
ax.axis('off'); ax.set_xlim(-6.6, 6.6); ax.set_ylim(-6.3, 6.3); ax.set_aspect('equal')
phases = ['1. Preliminary\ninvestigation', '2. Feasibility\nstudy',
          '3. System\nanalysis', '4. System\ndesign', '5. Coding',
          '6. Testing', '7. Implemen-\ntation', '8. Maintenance']
R, A, B = 4.7, 1.52, 0.78
cen = []
for i, lab in enumerate(phases):
    a = np.radians(90 - i * 360 / len(phases))
    x, y = R * np.cos(a), R * np.sin(a)
    cen.append(np.array([x, y]))
    ax.add_patch(Ellipse((x, y), 2 * A, 2 * B, fc='#eaf1f8', ec=ACCENT, lw=1.1))
    ax.text(x, y, lab, ha='center', va='center', fontsize=6.8, color=INK)
for i in range(len(phases)):
    c0, c1 = cen[i], cen[(i + 1) % len(phases)]
    d = c1 - c0
    u = d / np.hypot(*d)
    rad = 1.0 / np.sqrt((u[0] / A) ** 2 + (u[1] / B) ** 2)
    p0 = c0 + u * (rad + 0.10)
    p1 = c1 - u * (rad + 0.10)
    ax.add_patch(FancyArrowPatch(tuple(p0), tuple(p1), arrowstyle='-|>',
                                 mutation_scale=9,
                                 color=MUTED if i < len(phases) - 1 else '#d9534f',
                                 lw=1.1, shrinkA=0, shrinkB=0))
ax.text(0, 0.75, 'SDLC', ha='center', fontsize=11, color=INK, weight='bold')
ax.text(0, -0.9, 'maintenance feeds new\nrequirements back to phase 1', ha='center',
        fontsize=6.8, color='#d9534f')
```

| Phase | What happens | Deliverable |
|---|---|---|
| Preliminary investigation | study the existing system, define the problem and scope | project request / problem statement |
| Feasibility study | is it technically, economically, operationally and legally possible? | feasibility report, cost–benefit analysis |
| System analysis | gather and analyse requirements, model the current and proposed system | SRS, DFDs, ER diagrams |
| System design | decide architecture, database, inputs, outputs, interfaces, algorithms | design document, schema, screen layouts |
| Coding | write and unit-test the programs | source code, unit test results |
| Testing | unit, integration, system and acceptance testing | test report, defect list |
| Implementation | install, convert data, train users, go live | working system, user manual, training |
| Maintenance | fix defects, adapt to change, improve performance | change requests, new versions |

The four kinds of **feasibility** are worth memorising: *technical* (do we have
the technology and skills?), *economic* (do the benefits exceed the costs?),
*operational* (will the staff actually use it?) and *schedule/legal* (can it be
done in time, and is it lawful — for example does it obey Nepal's Electronic
Transactions Act and privacy rules?).

Maintenance is the longest and most expensive phase — typically **60–70 % of the
total cost** over a system's lifetime — and comes in four flavours: *corrective*
(fix defects), *adaptive* (new OS, new tax rate), *perfective* (new features,
faster) and *preventive* (restructure the code so future change is cheaper).

::: memory The eight phases in order
**P**lease **F**inish **A**ll **D**esign **C**ode **T**esting **I**nstallation
**M**aintenance — Preliminary investigation, Feasibility, Analysis, Design,
Coding, Testing, Implementation, Maintenance.
:::

## 6.4 System analyst vs software engineer

Both work on the same project; they look in opposite directions. The analyst
faces the **customer and the problem**; the engineer faces the **machine and the
solution**.

| Point | System analyst | Software engineer |
|---|---|---|
| Main role | studies the business problem and defines what the system must do | designs, builds and tests the software that does it |
| Works mostly with | users, managers, clients | code, tools, other developers |
| Key output | requirement specification (SRS), DFDs, feasibility report | source code, design documents, test cases, builds |
| Phases involved | investigation, feasibility, analysis, acceptance, training | design, coding, testing, maintenance |
| Core skills | communication, interviewing, business knowledge, modelling | programming, algorithms, data structures, databases, tools |
| Question answered | **What** should the system do? | **How** will the system do it? |
| Typical background | management information systems, business + IT | computer science / software engineering |

In a small Nepali software company one person often plays both roles; in a large
project they are separate, and the SRS is the contract between them.

## 6.5 Requirement collection methods

A requirement is a statement of what the system must do (*functional* — "the
system shall print a mark ledger class-wise") or of a quality it must have
(*non-functional* — "results for 500 students shall be generated in under 30
seconds"). Requirements are collected from users by these methods:

| Method | How it works | Strength | Weakness |
|---|---|---|---|
| Interview | structured or unstructured face-to-face questioning of users | deep, allows follow-up questions, body language | slow, costly, needs skill, one user at a time |
| Questionnaire | a fixed set of written questions sent to many users | cheap, reaches many people, easy to summarise | no follow-up, low response rate, poor questions give poor data |
| Observation | the analyst watches the existing work being done | shows what people really do, not what they say | time-consuming; people behave differently when watched |
| Record / document review | reading existing forms, reports, files, manuals, laws | shows the real data items and volumes | documents may be out of date |
| Group discussion (JAD) | users, managers and analysts in one workshop | conflicts resolved on the spot, fast agreement | hard to arrange, a loud person can dominate |
| Prototyping | show a mock screen and let users react to it | users are far better at criticising than at describing | users may think the prototype is the finished product |
| Brainstorming | open idea generation for a new system with no precedent | uncovers ideas nobody asked for | unstructured, needs filtering |

The collected requirements are written into a **Software Requirement
Specification (SRS)**: an agreed, numbered, testable document. A good requirement
is *complete, consistent, unambiguous, verifiable, traceable* and *feasible*.
"The system should be fast" fails: it is not verifiable. "A fee receipt shall be
printed within 5 seconds of confirmation" passes.

## 6.6 Concept of system design

Design answers *how*. It takes the SRS and produces a blueprint detailed enough
for a programmer to code from. It is done at two levels:

- **Logical (conceptual) design** — what the system does, drawn independently of
  any machine: data flow diagrams, ER diagrams, data dictionary, decision tables.
- **Physical design** — how it will actually be built: tables and indexes in a
  particular DBMS, file formats, screen and report layouts, program modules,
  hardware and network.

The main design activities are **architectural design** (splitting the system
into modules and fixing how they talk), **database design** (ER model →
normalised tables), **input design** (forms, validation), **output design**
(reports, screens), **interface design** (usability, navigation) and **process
design** (algorithms). Two properties decide whether a design is good:
**cohesion** (each module does one job — high is good) and **coupling** (modules
depend on each other as little as possible — low is good).

### 6.6.1 Data flow diagrams

A **DFD** shows how data moves through a system — never control flow, never
timing. Four symbols are used (Yourdon–DeMarco notation):

| Symbol | Meaning | Naming rule |
|---|---|---|
| Circle / bubble | process — transforms data | verb + object, e.g. "Compute result" |
| Rectangle (square) | external entity — source or sink outside the system | noun, e.g. "Student" |
| Open-ended rectangle | data store — a file or table | D1, D2 … plus a noun |
| Arrow | data flow | noun describing the data, e.g. "marks" |

The **level-0 DFD (context diagram)** shows the whole system as one process with
its external entities. It is exploded into a **level-1 DFD**, which shows the
main processes (numbered 1.0, 2.0, …) and the data stores between them. The rule
that catches errors is **balancing**: the flows crossing the boundary of the
level-1 diagram must be exactly the flows on the context diagram.

```figure caption="Level-0 (context) DFD of a school result system: the whole system is one process, surrounded by its external entities."
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6.4)
ax.add_patch(Circle((5.0, 3.2), 1.25, fc='#eaf1f8', ec=ACCENT, lw=1.3))
ax.text(5.0, 3.55, '0', ha='center', va='center', fontsize=9, color=INK, weight='bold')
ax.text(5.0, 2.95, 'School Result\nSystem', ha='center', va='center',
        fontsize=7.4, color=INK)
ents = [('Subject\nteacher', 0.3, 4.4), ('Student', 8.2, 4.4),
        ('Exam\nsection', 0.3, 1.0), ('Head\nteacher', 8.2, 1.0)]
for lab, x, y in ents:
    ax.add_patch(Rectangle((x, y), 1.8, 1.1, fc='white', ec=INK, lw=1.1))
    ax.text(x + 0.9, y + 0.55, lab, ha='center', va='center', fontsize=7.4, color=INK)
def flow(p0, p1, lab, rad, off):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=9,
                                 color=MUTED, lw=1.0,
                                 connectionstyle='arc3,rad=' + str(rad)))
    m = ((p0[0] + p1[0]) / 2 + off[0], (p0[1] + p1[1]) / 2 + off[1])
    ax.text(m[0], m[1], lab, ha='center', va='center', fontsize=6.9, color=ACCENT)
flow((2.1, 5.0), (4.2, 3.9), 'subject marks', 0.15, (0.1, 0.55))
flow((4.0, 2.7), (2.1, 1.6), 'exam schedule', 0.15, (0.75, -0.3))
flow((6.1, 3.9), (8.2, 5.0), 'mark-sheet', 0.15, (0.0, 0.55))
flow((8.2, 1.6), (6.0, 2.7), 'result approval', 0.15, (-0.7, -0.35))
ax.text(5.0, 0.15, 'External entity = rectangle   Process = circle   Data flow = arrow',
        ha='center', fontsize=6.8, color=MUTED, style='italic')
```

```figure caption="Level-1 DFD: process 0 exploded into three numbered processes with two data stores. The flows crossing the edge of the diagram are the same four flows as on the context diagram — the diagram is balanced."
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.2, 3.7))
ax.axis('off'); ax.set_xlim(0, 10.4); ax.set_ylim(0, 7.6)
def ent(x, y, lab):
    ax.add_patch(Rectangle((x, y), 1.7, 1.0, fc='white', ec=INK, lw=1.1))
    ax.text(x + 0.85, y + 0.5, lab, ha='center', va='center', fontsize=7.0, color=INK)
def proc(x, y, num, lab):
    ax.add_patch(Circle((x, y), 0.95, fc='#eaf1f8', ec=ACCENT, lw=1.2))
    ax.text(x, y + 0.3, num, ha='center', va='center', fontsize=7.6, weight='bold',
            color=INK)
    ax.text(x, y - 0.25, lab, ha='center', va='center', fontsize=6.6, color=INK)
def store(x, y, tag, lab):
    ax.plot([x, x + 2.6], [y, y], color=INK, lw=1.0)
    ax.plot([x, x + 2.6], [y + 0.72, y + 0.72], color=INK, lw=1.0)
    ax.plot([x + 0.55, x + 0.55], [y, y + 0.72], color=INK, lw=1.0)
    ax.text(x + 0.27, y + 0.36, tag, ha='center', va='center', fontsize=6.8, color=INK)
    ax.text(x + 1.6, y + 0.36, lab, ha='center', va='center', fontsize=6.8, color=INK)
def arw(p0, p1, lab, lx, ly):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=8,
                                 color=MUTED, lw=0.95, shrinkA=0, shrinkB=0))
    ax.text(lx, ly, lab, ha='center', va='center', fontsize=6.4, color=ACCENT)
ent(0.1, 5.3, 'Subject\nteacher'); ent(0.1, 0.5, 'Exam\nsection')
ent(8.6, 5.3, 'Student');          ent(8.6, 0.5, 'Head\nteacher')
proc(3.6, 6.0, '1.0', 'Record\nmarks')
proc(6.0, 3.2, '2.0', 'Compute\nresult')
proc(8.6, 3.2, '3.0', 'Print\nmark-sheet')
store(1.4, 3.9, 'D1', 'Marks file')
store(1.4, 2.2, 'D2', 'Student file')
arw((1.8, 5.9), (2.62, 5.98), 'subject marks', 2.25, 6.6)
arw((3.35, 5.08), (3.15, 4.68), 'validated marks', 4.7, 4.95)
arw((4.05, 4.15), (5.18, 3.6), 'marks', 4.75, 4.35)
arw((4.05, 2.62), (5.18, 2.9), 'student record', 5.15, 2.25)
arw((1.8, 1.1), (5.25, 2.65), 'exam schedule', 3.4, 1.35)
arw((6.96, 3.2), (7.62, 3.2), 'grade, GPA', 7.3, 4.25)
arw((8.9, 4.08), (9.4, 5.25), 'mark-sheet', 7.85, 4.95)
arw((9.2, 1.5), (8.85, 2.3), 'result approval', 7.45, 1.6)
```

::: tip Drawing a DFD in the exam
Number every process (0 on the context diagram; 1.0, 2.0 on level 1). Label
**every** arrow with the data, not with a verb. Never draw an arrow from a data
store straight to another data store, or from an external entity straight to a
data store — data must pass through a process. Never draw a decision diamond:
that is a flowchart, not a DFD.
:::

### 6.6.2 From ER model to tables

Database design starts with an ER diagram — entities (rectangles), attributes
(ellipses, key attribute underlined) and relationships (diamonds) — and converts
it into relational tables using three rules: each entity becomes a table with its
key as the primary key; a 1:M relationship puts the key of the "one" side into
the "many" table as a **foreign key**; and an M:N relationship becomes a **new
table** whose primary key is the pair of foreign keys.

```figure caption="Mapping an M:N ER relationship to tables. STUDENT and COURSE become tables; the many-to-many relationship ENROLS becomes a third table whose key is the pair of foreign keys, and which carries the relationship's own attribute."
from matplotlib.patches import Rectangle, Ellipse, Polygon, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.2, 3.4))
ax.axis('off'); ax.set_xlim(0, 12.5); ax.set_ylim(0, 7.2)
def entity(x, y, lab):
    ax.add_patch(Rectangle((x, y), 1.9, 0.85, fc='#eaf1f8', ec=ACCENT, lw=1.1))
    ax.text(x + 0.95, y + 0.42, lab, ha='center', va='center', fontsize=7.4, color=INK)
def attr(x, y, lab, key=False):
    ax.add_patch(Ellipse((x, y), 1.75, 0.72, fc='white', ec=MUTED, lw=1.0))
    ax.text(x, y + (0.07 if key else 0), lab, ha='center', va='center',
            fontsize=6.6, color=INK)
    if key:
        ax.plot([x - 0.42, x + 0.42], [y - 0.13, y - 0.13], color=INK, lw=0.8)
entity(0.4, 5.6, 'STUDENT'); entity(0.4, 1.4, 'COURSE')
ax.add_patch(Polygon([[1.35, 4.35], [2.5, 3.5], [1.35, 2.65], [0.2, 3.5]],
                     closed=True, fc='#fdf6e6', ec='#b8860b', lw=1.1))
ax.text(1.35, 3.5, 'ENROLS', ha='center', va='center', fontsize=6.6, color=INK)
ax.plot([1.35, 1.35], [5.6, 4.35], color=MUTED, lw=1.0)
ax.plot([1.35, 1.35], [2.65, 2.25], color=MUTED, lw=1.0)
ax.text(1.55, 4.9, 'M', fontsize=7.0, color=INK); ax.text(1.55, 2.4, 'N', fontsize=7.0, color=INK)
attr(3.4, 6.7, 'roll_no', True); attr(3.4, 5.6, 'name')
ax.plot([2.3, 2.62], [6.05, 6.6], color=MUTED, lw=0.9)
ax.plot([2.3, 2.55], [6.0, 5.6], color=MUTED, lw=0.9)
attr(3.4, 3.5, 'grade')
ax.plot([2.5, 2.55], [3.5, 3.5], color=MUTED, lw=0.9)
attr(3.4, 1.8, 'course_id', True)
ax.plot([2.3, 2.55], [1.85, 1.8], color=MUTED, lw=0.9)
ax.add_patch(FancyArrowPatch((4.5, 3.6), (5.6, 3.6), arrowstyle='-|>',
                             mutation_scale=12, color='#d9534f', lw=1.4))
ax.text(5.05, 4.0, 'maps to', ha='center', fontsize=7.0, color='#d9534f')
def table(x, y, name, cols, rows):
    w = 6.0; ax.add_patch(Rectangle((x, y), w, 0.62, fc='#eaf1f8', ec=INK, lw=1.0))
    ax.text(x + 0.12, y + 0.31, name, va='center', fontsize=7.0, weight='bold', color=INK)
    ax.add_patch(Rectangle((x, y - 0.62), w, 0.62, fc='white', ec=INK, lw=1.0))
    ax.text(x + 0.12, y - 0.31, cols, va='center', fontsize=6.4, color=ACCENT)
    ax.add_patch(Rectangle((x, y - 1.24), w, 0.62, fc='white', ec=INK, lw=1.0))
    ax.text(x + 0.12, y - 0.93, rows, va='center', fontsize=6.4, color=MUTED)
table(6.1, 6.5, 'STUDENT', 'roll_no (PK) | name', '1 | Sita Rai')
table(6.1, 4.3, 'COURSE', 'course_id (PK) | title', 'CS12 | Computer Science')
table(6.1, 2.1, 'ENROLS', 'roll_no (PK,FK) | course_id (PK,FK) | grade',
      '1 | CS12 | A')
ax.text(9.1, 0.5, 'M:N relationship → a separate table', ha='center',
        fontsize=6.8, color='#d9534f', style='italic')
```

## 6.7 Software and quality

Software quality is not "no bugs". It is **conformance to the stated
requirements, to the explicitly documented development standards, and to the
implicit expectations of professional software** (Pressman's definition — worth
quoting). The international standard **ISO/IEC 25010**, whose 2023 revision
replaced the older ISO 9126, lists nine quality characteristics:

| Characteristic | Question it answers |
|---|---|
| Functional suitability | does it do the required jobs, correctly and completely? |
| Performance efficiency | is it fast enough, and economical with memory and CPU? |
| Compatibility | can it co-exist and exchange data with other systems? |
| Interaction capability (usability) | can users learn it and operate it without errors? |
| Reliability | does it keep working, and recover after failure? |
| Security | is data protected from unauthorised access and change? |
| Maintainability | how cheaply can it be corrected, adapted or improved? |
| Flexibility (portability) | can it be moved, scaled and adapted to new environments? |
| Safety | can it harm people, property or the environment? |

The older **McCall factors** are still asked for in NEB papers and group the
same ideas as *product operation* (correctness, reliability, efficiency,
integrity, usability), *product revision* (maintainability, flexibility,
testability) and *product transition* (portability, reusability,
interoperability).

Quality is built in by two complementary activities: **quality assurance (QA)**,
which is process-oriented and preventive — standards, reviews, inspections,
audits — and **quality control (QC)**, which is product-oriented and detective —
testing the built software. Their companion pair is **verification** ("are we
building the product right?" — reviews, static checks against the design) and
**validation** ("are we building the right product?" — testing against the user's
real need).

Two quality measures are easy to examine numerically:

$$ \text{Availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}} \times 100\% $$

$$ \text{Defect removal efficiency} = \frac{E}{E + D} \times 100\% $$

where MTBF is the mean time between failures, MTTR the mean time to repair,
$E$ the number of defects found **before** delivery and $D$ the number found by
users **after** delivery.

::: example Worked example 6.2 — availability and defect removal
**Problem.** A result-processing server fails on average once every 400 hours of
operation and takes 5 hours to repair. During development the team found 92
defects; users reported 8 more in the first year. Compute the availability and
the defect removal efficiency.

**Solution.**

$$ \text{Availability} = \frac{400}{400 + 5} \times 100\% = \frac{400}{405} \times 100\% = 98.77\% $$

$$ \text{DRE} = \frac{92}{92 + 8} \times 100\% = \frac{92}{100} \times 100\% = 92\% $$

An availability of 98.77 % sounds high, but it is about 4.5 days of downtime a
year — unacceptable for a payment system, where "four nines" (99.99 %, under an
hour a year) is the target.
:::

The earlier a defect is found, the cheaper it is to remove — this single fact is
the economic argument for reviews, for writing a good SRS, and for the
iterative models in the next section.

```figure caption="Relative cost of fixing one defect, by the phase in which it is found (industry rule-of-thumb figures popularised by Boehm). Note the logarithmic scale: a requirement error that survives to maintenance costs about 100 times more."
fig, ax = plt.subplots(figsize=(4.8, 2.8))
phases = ['Require-\nment', 'Design', 'Coding', 'Testing', 'Mainte-\nnance']
cost = [1, 5, 10, 20, 100]
bars = ax.bar(phases, cost, color=[ACCENT, ACCENT, ACCENT, '#b8860b', '#d9534f'],
              width=0.62)
ax.set_yscale('log')
ax.set_ylabel('relative cost to fix one defect')
ax.set_ylim(0.6, 260)
ax.set_yticks([1, 10, 100]); ax.set_yticklabels(['1×', '10×', '100×'])
for b, c in zip(bars, cost):
    ax.text(b.get_x() + b.get_width() / 2, c * 1.18, str(c) + '×', ha='center',
            fontsize=8.0, color=INK)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, axis='y', alpha=0.5)
ax.tick_params(axis='x', labelsize=7.4)
```

::: example Worked example 6.3 — the cost of a late requirement error
**Problem.** A team discovers that the fee module ignores the sibling discount.
Fixing such an error during the requirement phase costs about Rs 2,000 of
effort. Using the relative costs in the figure above, what would the same error
cost if it were found (a) during testing and (b) after the system had gone live,
and what is the extra cost of the delay in case (b)?

**Solution.**

(a) Testing is $20\times$: $20 \times 2{,}000 = \text{Rs } 40{,}000$.

(b) Maintenance is $100\times$: $100 \times 2{,}000 = \text{Rs } 2{,}00{,}000$.

Extra cost of the delay $= 2{,}00{,}000 - 2{,}000 = \text{Rs } 1{,}98{,}000$ —
and that ignores the cost of wrong bills already sent to parents. One hour of
requirement review would have been the cheapest hour in the project.
:::

## 6.8 Software development models

### 6.8.1 Waterfall model

The oldest model (described by Royce in 1970). The phases are executed **once**,
strictly in order, and each must be completed and signed off before the next
begins — like water falling from one step to the next, never upwards. The only
backward movement is a feedback loop to the phase immediately above when a
defect is found.

```figure caption="The waterfall model. Work flows one way down the steps; the dashed arrows are the limited feedback allowed to the phase immediately above."
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1, 3.2))
ax.axis('off'); ax.set_xlim(0, 11.5); ax.set_ylim(0, 7.4)
steps = ['Requirement\nanalysis', 'System\ndesign', 'Implementation\n(coding)',
         'Testing &\nintegration', 'Deployment', 'Maintenance']
w, h = 2.45, 0.95
pos = []
for i, s in enumerate(steps):
    x = 0.25 + i * 1.78
    y = 6.1 - i * 1.05
    pos.append((x, y))
    ax.add_patch(Rectangle((x, y), w, h, fc='#eaf1f8', ec=ACCENT, lw=1.1))
    ax.text(x + w / 2, y + h / 2, s, ha='center', va='center', fontsize=7.0, color=INK)
for i in range(len(steps) - 1):
    x0, y0 = pos[i]; x1, y1 = pos[i + 1]
    ax.add_patch(FancyArrowPatch((x0 + w * 0.72, y0), (x1 + w * 0.28, y1 + h),
                                 arrowstyle='-|>', mutation_scale=9, color=MUTED, lw=1.1))
    ax.add_patch(FancyArrowPatch((x1 + w * 0.62, y1 + h), (x0 + w * 0.95, y0),
                                 arrowstyle='-|>', mutation_scale=7, color='#d9534f',
                                 lw=0.8, ls=(0, (3, 2))))
ax.text(9.8, 6.4, 'feedback only to\nthe phase above', ha='center', fontsize=7.0,
        color='#d9534f')
ax.text(0.3, 0.35, 'each phase is completed and signed off before the next starts',
        fontsize=7.2, color=MUTED, style='italic')
```

**Advantages.** Simple to understand and manage; every phase has a fixed
deliverable and review; documentation is complete; easy to estimate cost and
schedule; works well when requirements are frozen and well understood.

**Disadvantages.** Working software appears only very late; going back is
expensive; the customer sees nothing until delivery, so a misunderstood
requirement is discovered at the worst possible moment; it cannot cope with
changing requirements; risk is not addressed explicitly.

**Suitable for** short, well-understood projects whose requirements cannot
change — payroll rewrites, government systems defined by a fixed law, projects
with a legal or tender-based specification.

### 6.8.2 Prototype model

A **prototype** is a quick, incomplete working model of the system, built to be
shown to the user and then refined — or thrown away once the requirements are
understood. It exists because users cannot describe what they want in the
abstract, but can criticise a screen instantly.

```figure caption="The prototype model. The inner loop (quick design → build → evaluate → refine) repeats until the customer is satisfied; only then is the final product engineered."
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 4.25))
ax.axis('off'); ax.set_xlim(-6.0, 6.0); ax.set_ylim(-5.4, 4.8); ax.set_aspect('equal')
loop = ['1. Requirement\ngathering', '2. Quick\ndesign', '3. Build\nprototype',
        '4. Customer\nevaluation', '5. Refine\nprototype']
R = 3.1
pts = []
for i, lab in enumerate(loop):
    a = np.radians(90 - i * 72)
    x, y = R * np.cos(a), R * np.sin(a)
    pts.append((x, y))
    ax.add_patch(FancyBboxPatch((x - 1.05, y - 0.52), 2.1, 1.04,
                                boxstyle='round,pad=0.06', fc='#eaf1f8',
                                ec=ACCENT, lw=1.1))
    ax.text(x, y, lab, ha='center', va='center', fontsize=6.9, color=INK)
for i in range(5):
    a0 = np.radians(90 - i * 72 - 26); a1 = np.radians(90 - (i + 1) * 72 + 26)
    ax.add_patch(FancyArrowPatch((R * np.cos(a0), R * np.sin(a0)),
                                 (R * np.cos(a1), R * np.sin(a1)),
                                 arrowstyle='-|>', mutation_scale=9, color=MUTED,
                                 lw=1.0, connectionstyle='arc3,rad=-0.3'))
ax.text(0, 0.35, 'repeat until the\ncustomer agrees', ha='center', fontsize=7.2,
        color='#d9534f')
ax.add_patch(FancyBboxPatch((-1.55, -5.1), 3.1, 1.0, boxstyle='round,pad=0.06',
                            fc='#fdf6e6', ec='#b8860b', lw=1.1))
ax.text(0.0, -4.6, '6. Engineer the\nfinal product', ha='center', va='center',
        fontsize=6.9, color=INK)
ax.add_patch(FancyArrowPatch((-1.5, -3.1), (-0.55, -4.05), arrowstyle='-|>',
                             mutation_scale=9, color='#b8860b', lw=1.2))
ax.text(-2.55, -3.95, 'customer\naccepts', ha='center', va='center', fontsize=6.6,
        color='#b8860b')
```

**Advantages.** Requirements are clarified early; the user is involved
throughout; missing functions and misunderstandings surface before real coding;
reduces the risk of building the wrong product.

**Disadvantages.** The customer may demand that the throw-away prototype be
shipped; quick-and-dirty choices (wrong language, no error handling) can leak
into the product; more customer meetings mean more cost and time; it is hard to
know when to stop iterating.

**Suitable for** systems with unclear or changing requirements and a heavy user
interface — a new online service, a first-of-its-kind app.

### 6.8.3 Incremental and iterative models

The system is divided into **increments**; each increment goes through the whole
mini life cycle and delivers working software. The first increment is the core
product; later increments add features. The customer therefore has something
usable after a few weeks instead of a year.

```figure caption="Incremental development. Each increment repeats analysis, design, coding and testing, and ends in a usable release; features accumulate release by release."
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1, 2.9))
ax.axis('off'); ax.set_xlim(0, 12.2); ax.set_ylim(0, 6.6)
labels = ['A', 'D', 'C', 'T']
names = {'A': 'analysis', 'D': 'design', 'C': 'coding', 'T': 'testing'}
for k in range(3):
    y = 4.6 - k * 1.7
    x0 = 0.4 + k * 1.5
    for j, l in enumerate(labels):
        ax.add_patch(Rectangle((x0 + j * 1.15, y), 1.05, 0.85, fc='#eaf1f8',
                               ec=ACCENT, lw=1.0))
        ax.text(x0 + j * 1.15 + 0.52, y + 0.42, l, ha='center', va='center',
                fontsize=7.6, color=INK)
    ax.add_patch(FancyArrowPatch((x0 + 4 * 1.15 - 0.05, y + 0.42),
                                 (x0 + 4 * 1.15 + 0.5, y + 0.42),
                                 arrowstyle='-|>', mutation_scale=9, color=MUTED, lw=1.0))
    ax.add_patch(Rectangle((x0 + 4 * 1.15 + 0.55, y - 0.05), 2.6, 0.95,
                           fc='#fdf6e6', ec='#b8860b', lw=1.1))
    ax.text(x0 + 4 * 1.15 + 1.85, y + 0.42, 'Release ' + str(k + 1) + '\n(increment ' +
            str(k + 1) + ')', ha='center', va='center', fontsize=6.8, color=INK)
ax.annotate('', xy=(11.9, 0.55), xytext=(0.4, 0.55),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0))
ax.text(6.0, 0.15, 'time', ha='center', fontsize=7.4, color=INK)
ax.text(0.4, 5.9, '   '.join(k + ' = ' + v for k, v in names.items()),
        fontsize=7.0, color=MUTED)
```

**Advantages.** Working software early; easier to test and debug a small
increment; customer feedback shapes later increments; risk is spread out; money
comes in from the first release.

**Disadvantages.** Needs a good architecture up front or the increments will not
fit together; total cost can exceed a single-pass build; planning across
increments is harder.

### 6.8.4 Spiral model

Boehm's spiral model (1988) is the **risk-driven** model: development proceeds
in loops, and each loop is divided into four quadrants. The radius of the spiral
represents the cost accumulated so far, and the angle the progress through the
current loop. A prototype is built in every loop to attack the biggest remaining
risk, and the customer reviews the result before the next loop is funded.

```figure caption="The spiral model. Each loop passes through four quadrants — set objectives, analyse and resolve risks, develop and test, plan the next loop — and the radius grows with the cost committed so far."
from matplotlib.patches import FancyArrowPatch
fig, ax = plt.subplots(figsize=(4.8, 4.2))
ax.axis('off'); ax.set_aspect('equal')
ax.set_xlim(-6.4, 6.4); ax.set_ylim(-6.0, 6.4)
th = np.linspace(0.5 * np.pi, 0.5 * np.pi + 6.6 * np.pi, 900)
r = 0.28 + 0.235 * (th - 0.5 * np.pi)
x, y = r * np.cos(th), r * np.sin(th)
ax.plot(x, y, color=ACCENT, lw=1.6)
ax.add_patch(FancyArrowPatch((x[-14], y[-14]), (x[-1], y[-1]), arrowstyle='-|>',
                             mutation_scale=12, color=ACCENT, lw=1.6))
ax.plot([-6.0, 6.0], [0, 0], color=MUTED, lw=0.9)
ax.plot([0, 0], [-5.6, 6.0], color=MUTED, lw=0.9)
ax.text(-5.9, 5.6, '1. Determine objectives,\nalternatives, constraints',
        fontsize=7.2, color=INK, va='top')
ax.text(6.0, 5.6, '2. Identify and resolve risks\n(build a prototype)',
        fontsize=7.2, color=INK, ha='right', va='top')
ax.text(6.0, -4.5, '3. Develop and verify\nthe next-level product',
        fontsize=7.2, color=INK, ha='right')
ax.text(-5.9, -4.5, '4. Plan the next phase\n(customer review)', fontsize=7.2, color=INK)
ax.annotate('', xy=(0.1, -5.2), xytext=(0.1, -0.2),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0))
ax.text(0.32, -3.0, 'cumulative cost', fontsize=7.0, color='#d9534f', rotation=90,
        va='center', ha='left',
        bbox=dict(fc='white', ec='none', pad=0.6))
for rr, lab in [(1.15, 'loop 1'), (2.75, 'loop 2'), (4.3, 'loop 3')]:
    ax.text(-rr, 0.0, lab, fontsize=6.8, color=MUTED, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.6))
```

**Advantages.** Risk is handled explicitly and early; suits very large, costly
or novel projects; the customer sees a prototype in every loop; changes can be
absorbed in the next loop.

**Disadvantages.** Expensive; needs genuine risk-assessment expertise, which is
rare; no fixed end — a project can spiral forever; over-complicated for small
projects.

### 6.8.5 Agile model

Agile is a family of iterative methods (Scrum, XP, Kanban) built on the **Agile
Manifesto of 2001**, whose four values are: *individuals and interactions* over
processes and tools; *working software* over comprehensive documentation;
*customer collaboration* over contract negotiation; *responding to change* over
following a plan — while accepting that the items on the right still have value.

Work is delivered in **sprints** (time-boxes of one to four weeks). In Scrum the
**product owner** keeps a prioritised **product backlog**; the team pulls the top
items into a **sprint backlog**, holds a 15-minute **daily stand-up**, and ends
the sprint with a **review** (demo of the shippable increment) and a
**retrospective** (how do we improve?). A **scrum master** removes obstacles.

```figure caption="One Scrum sprint. Items are pulled from the product backlog into a sprint backlog, developed in a time-boxed sprint with a daily stand-up, and delivered as a working increment; whatever is left returns to the backlog."
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1, 3.0))
ax.axis('off'); ax.set_xlim(0, 12.0); ax.set_ylim(0, 6.6)
ax.add_patch(Rectangle((0.2, 2.2), 2.2, 2.4, fc='#eaf1f8', ec=ACCENT, lw=1.1))
ax.text(1.3, 4.25, 'Product\nbacklog', ha='center', va='center', fontsize=7.2, color=INK)
for i in range(4):
    ax.add_patch(Rectangle((0.45, 3.35 - i * 0.42), 1.7, 0.3, fc='white',
                           ec=MUTED, lw=0.8))
ax.add_patch(Rectangle((3.1, 2.7), 2.0, 1.6, fc='#fdf6e6', ec='#b8860b', lw=1.1))
ax.text(4.1, 3.95, 'Sprint\nbacklog', ha='center', va='center', fontsize=7.2, color=INK)
for i in range(2):
    ax.add_patch(Rectangle((3.3, 3.0 + i * 0.42), 1.6, 0.3, fc='white', ec=MUTED, lw=0.8))
ax.add_patch(Circle((7.2, 3.5), 1.55, fc='none', ec=ACCENT, lw=1.4))
ax.add_patch(Circle((7.2, 3.5), 0.72, fc='#eaf1f8', ec=MUTED, lw=1.0, ls=(0, (3, 2))))
ax.text(7.2, 3.5, 'daily\nstand-up', ha='center', va='center', fontsize=6.4, color=INK)
ax.text(7.2, 5.45, 'Sprint  (1–4 weeks)', ha='center', fontsize=7.2, color=INK)
ax.add_patch(FancyArrowPatch((8.35, 4.35), (9.2, 3.85), arrowstyle='-|>',
                             mutation_scale=11, color=ACCENT, lw=1.3))
ax.add_patch(Rectangle((9.3, 2.7), 2.5, 1.6, fc='#eaf1f8', ec=ACCENT, lw=1.1))
ax.text(10.55, 3.5, 'Working\nincrement\n(review + demo)', ha='center', va='center',
        fontsize=6.8, color=INK)
ax.add_patch(FancyArrowPatch((2.45, 3.5), (3.05, 3.5), arrowstyle='-|>',
                             mutation_scale=10, color=MUTED, lw=1.1))
ax.add_patch(FancyArrowPatch((5.15, 3.5), (5.6, 3.5), arrowstyle='-|>',
                             mutation_scale=10, color=MUTED, lw=1.1))
ax.add_patch(FancyArrowPatch((10.55, 2.6), (1.3, 2.1), arrowstyle='-|>',
                             mutation_scale=10, color='#d9534f', lw=1.0,
                             connectionstyle='arc3,rad=-0.22'))
ax.text(6.0, 0.15, 'unfinished items and new requirements go back to the backlog',
        ha='center', fontsize=7.0, color='#d9534f')
```

**Advantages.** Working software every few weeks; welcomes changing
requirements, even late; continuous customer involvement; defects found early;
high team motivation and communication.

**Disadvantages.** Little documentation, which hurts long-term maintenance;
needs experienced, self-organising teams and an available customer; the final
cost and date are hard to fix in advance, so it fits badly with tender-based
government contracts.

### 6.8.6 Comparing the models

| Model | Requirements must be | Cost | Risk handling | Customer involvement | Working software | Best suited to |
|---|---|---|---|---|---|---|
| Waterfall | fixed and fully known | low (if no rework) | poor — risk appears at testing | only at start and end | very late | short projects with a frozen, legal or tender specification |
| Prototype | unclear, UI-heavy | medium — prototypes are extra work | medium — requirement risk reduced | high, continuous | early, but not production-ready | new services where users cannot state requirements |
| Incremental | core known, rest can evolve | medium | medium — spread over increments | after each release | after the first increment | medium/large systems that can be split into features |
| Spiral | may change; project is large | high | best — explicit risk analysis each loop | at every loop review | after a few loops | large, expensive, novel or safety-critical systems |
| Agile | expected to change constantly | medium, hard to fix in advance | good — short feedback loops | very high, daily | every 1–4 weeks | startups, apps, web products with an engaged customer |

::: example Worked example 6.4 — choosing a model
**Problem.** Choose and justify a process model for each: (a) a system for the
Department of Transport Management to print smart driving licences, whose rules
and forms are fixed by regulation; (b) a mobile app for a Kathmandu startup that
delivers groceries, where the founders keep changing their minds about features;
(c) the air-traffic control software for Tribhuvan International Airport.

**Solution.**
(a) **Waterfall.** The requirements come from a written regulation and cannot
change during the project; the contract is tender-based, so cost and schedule
must be fixed in advance; complete documentation is required for audit.

(b) **Agile (Scrum).** Requirements change weekly, the customer is in the same
city and available daily, and the startup needs a usable app in the market fast;
two-week sprints give them a shippable increment every fortnight.

(c) **Spiral.** The system is large, expensive and safety-critical; a failure
costs lives, so each loop must identify and resolve technical risks with
prototypes before more money is committed, and each loop ends with a formal
customer review.
:::

::: example Worked example 6.5 — planning sprints
**Problem.** A product backlog holds 260 story points of work. The team's
measured velocity is 40 story points per three-week sprint. How many sprints and
how many weeks are needed, and what happens to the plan if the customer adds 60
more story points after the second sprint?

**Solution.**

Sprints needed $= \dfrac{260}{40} = 6.5 \rightarrow 7$ sprints (you cannot do
half a sprint).

Time $= 7 \times 3 = 21$ weeks.

After adding 60 points the backlog is $260 + 60 = 320$ points, so
$320 / 40 = 8$ sprints $= 24$ weeks. The extra work costs exactly three weeks
and, crucially, **nothing already built has to be thrown away** — in a waterfall
project the same change after the design sign-off would have forced rework of the
design, code and test documents.
:::

::: caution Waterfall's feedback arrows
Drawing the waterfall model with long arrows from every phase back to every
earlier phase turns it into the iterative model and loses marks. Waterfall
allows feedback only to the phase **immediately** above, and even that is
expensive.
:::

## Chapter summary

- A software project is a temporary, planned effort constrained by scope, time,
  cost and quality; effort is measured in person-months and adding people late
  does not buy time.
- The software development process = specification, design and implementation,
  validation, evolution. A process model arranges those in time.
- The SDLC phases are preliminary investigation, feasibility study, analysis,
  design, coding, testing, implementation and maintenance; maintenance takes
  60–70 % of lifetime cost and is corrective, adaptive, perfective or preventive.
- The system analyst answers **what** (SRS, DFDs, talks to users); the software
  engineer answers **how** (design, code, tests).
- Requirements are collected by interview, questionnaire, observation, document
  review, JAD workshops, prototyping and brainstorming, and are written into an
  SRS that must be unambiguous and verifiable.
- Design is logical (DFD, ER, data dictionary) then physical (tables, screens,
  modules); aim for high cohesion and low coupling. DFD symbols: circle =
  process, rectangle = external entity, open rectangle = data store, arrow =
  data flow. An M:N relationship maps to a separate table.
- Quality = conformance to requirements, standards and implicit expectations;
  ISO/IEC 25010 (2023) lists nine characteristics. QA is preventive and
  process-based, QC is detective and product-based. Availability
  $= \text{MTBF}/(\text{MTBF}+\text{MTTR})$ and DRE $= E/(E+D)$.
- Models: waterfall (linear, fixed requirements), prototype (unclear
  requirements), incremental (release by release), spiral (risk-driven loops),
  agile (sprints, change welcomed).

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which phase of the SDLC consumes the largest share of the total lifetime cost? <span class="marks">[1]</span>
   (a) analysis (b) coding (c) testing (d) maintenance
2. In a data flow diagram, an open-ended rectangle represents <span class="marks">[1]</span>
   (a) a process (b) a data store (c) an external entity (d) a data flow
3. The model that is driven by risk analysis in every loop is <span class="marks">[1]</span>
   (a) waterfall (b) prototype (c) spiral (d) incremental
4. The Agile Manifesto was published in <span class="marks">[1]</span>
   (a) 1970 (b) 1988 (c) 2001 (d) 2010
5. "Are we building the right product?" is the question asked by <span class="marks">[1]</span>
   (a) verification (b) validation (c) debugging (d) compilation
6. A feasibility study that asks whether the staff will accept and use the system is <span class="marks">[1]</span>
   (a) technical (b) economic (c) operational (d) legal

::: note Answers to Group A
**1.** (d) — maintenance is 60–70 % of lifetime cost.
**2.** (b) — the open-ended rectangle (with a D-number) is a data store.
**3.** (c) — Boehm's spiral devotes a whole quadrant to identifying and resolving risk.
**4.** (c) — seventeen practitioners signed it in Utah in 2001.
**5.** (b) — validation checks against the user's real need; verification checks against the design.
**6.** (c) — operational feasibility concerns people and working practice.
:::

**Group B — Short answer (5 marks each)**

1. Define SDLC and explain any five of its phases with their deliverables. <span class="marks">[5]</span>
2. Differentiate between a system analyst and a software engineer on any five points. <span class="marks">[5]</span>
3. Explain any three requirement collection methods, stating one advantage and
   one disadvantage of each. <span class="marks">[5]</span>
4. What is software quality? Explain any four quality characteristics. <span class="marks">[5]</span>
5. A server has MTBF = 500 hours and MTTR = 4 hours. Compute its availability.
   The team removed 114 defects before release and users found 6 afterwards;
   compute the defect removal efficiency. <span class="marks">[5]</span>
6. Draw a level-0 DFD for a school library issue-and-return system and label all
   its symbols. <span class="marks">[5]</span>

::: note Answers to Group B
**1.–4.** Use §6.3, §6.4, §6.5 and §6.7; one mark per phase/point/method with its
deliverable or advantage.

**5.** Availability $= \frac{500}{500+4}\times 100\% = \frac{500}{504}\times 100\% = 99.21\%$.
DRE $= \frac{114}{114+6}\times100\% = \frac{114}{120}\times100\% = 95\%$.

**6.** One circle labelled "0 — Library system" in the centre. External entities
(rectangles): *Member*, *Librarian*, *Supplier*. Flows: Member → "membership
details", "book request"; system → Member "issued book slip", "due date"; system
→ Librarian "overdue list"; Librarian → system "new book details". No data
stores are shown on a context diagram — that is the commonest error.
:::

**Group C — Long answer (8 marks each)**

1. Draw and explain the waterfall model. State its advantages, disadvantages and
   the situations in which it should be used, and compare it with the agile
   model. <span class="marks">[8]</span>
2. What is a prototype? Draw the prototype model and explain each step. Compare
   it with the spiral model on cost, risk and customer involvement. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** Diagram as in §6.8.1 (2 marks — six phases in a descending cascade with
one-step feedback), explanation of each phase (2), three advantages (1.5), three
disadvantages (1.5), suitability + comparison with agile using the table in
§6.8.6 (1).

**2.** Definition of a prototype (1), diagram of the five-step loop plus the final
engineering step (2), explanation of each step (2), advantages and disadvantages
(2), comparison with spiral (1): the prototype model reduces **requirement** risk
only and is cheap; the spiral model addresses **all** technical and management
risks, costs much more, and gives the customer a formal review at the end of
every loop.
:::

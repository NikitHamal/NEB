---
subject: Principles of Management
grade: BCA Semester 2
unit: 7
title: IT in Management, Forms of Business, Job Design and Leadership Approaches
area: BCA 156 · Principles of Management · Unit 7
---

The revised BCA outline for this course is organised around four units (Introduction, Planning and Decision Making, Organizing, Leading) and names several topics that Units 1 to 6 treat only briefly or not at all: **forms of business**, the **integrated management framework**, the **role of IT in management, planning and decision making**, **job design, job description and job specification**, **forms of organisational design**, the **generic, situational and emerging approaches to leadership**, **managing teams in a crisis** and **leadership challenges in an IT-based organisation**. This unit closes those gaps. Read it after Units 1 to 6, because it builds on them.

::: key What this unit gives you
- Forms of business (sole proprietorship, partnership, company, cooperative, public enterprise) with the Nepali legal setting.
- The integrated management framework: how the four functions, the roles, the skills and the environment fit into one picture.
- Where information technology helps managers: planning, decision making, organising and control, with a worked cost-benefit example.
- Job analysis, job design, job description and job specification, with a complete sample for a software role.
- Forms of organisational design: functional, divisional, matrix, team, network and virtual.
- Generic, situational and emerging approaches to leadership; managing teams in a crisis; leadership challenges in IT firms.
:::

## 7.1 Forms of business

A **business** is an organisation that offers goods or services to customers in order to earn a profit. The **form of business** is its legal and ownership structure. It decides who owns the firm, who takes the decisions, who bears the losses and how much money can be raised, so it is the first management decision an entrepreneur takes. Nepali law recognises several forms; the sections below state the usual textbook features. Check the current Act before you register a real firm, because thresholds and fees are revised from time to time.

### Sole proprietorship

One person owns, controls and runs the business and keeps all profit and bears all loss. Examples are a neighbourhood computer repair shop, a freelance web developer working under a registered trade name, or a cyber cafe.

- **Strengths:** easy to start and close, quick decisions, full control, business secrecy, direct motivation because the owner gets all the profit.
- **Weaknesses:** **unlimited liability** (personal property can be sold to pay business debts), limited capital and skills, uncertain life (the business often ends with the owner), little scope for growth.

### Partnership

Two or more persons agree to run a business together and share profit and loss in an agreed ratio. In Nepal a partnership firm is governed by the Partnership Act, 2020 BS (1964). The agreement is normally written in a **partnership deed** that states each partner's capital, profit ratio, duties and what happens when a partner leaves.

- **Strengths:** more capital and a wider range of skills than one person, shared risk, easy to form, flexible.
- **Weaknesses:** in a general partnership liability is unlimited and **joint and several** (a creditor can claim the whole debt from any one partner); disputes between partners; the firm may dissolve when a partner leaves; shares cannot be sold freely.

### Company

A **company** is an artificial legal person created by registration. It can own property, sign contracts, sue and be sued in its own name, and it continues to exist even when its owners change (**perpetual succession**). Nepal's Companies Act, 2063 BS (2006) is the main law, and companies are registered at the Office of the Company Registrar.

| Point | Private limited company | Public limited company |
|---|---|---|
| Shareholders | few; the shares cannot be offered to the public; the usual textbook limit is 101 | at least seven promoters; shares may be offered to the public |
| Transfer of shares | restricted by the articles | free once the shares are listed on the stock exchange |
| Capital | limited to what founders and private investors give | large; raised through public issue of shares and debentures |
| Disclosure | little | heavy: audited accounts and reports must be published |
| Typical example | a software start-up owned by its founders | a bank or insurer listed on the Nepal Stock Exchange |

- **Strengths:** **limited liability** (a shareholder can lose only the money invested), large capital, professional management separate from ownership, perpetual succession, easy growth.
- **Weaknesses:** formation cost and many legal formalities, public disclosure, slow decisions in a large company, **separation of ownership and control** (managers may serve themselves instead of shareholders), the risk of fraud and excessive tax burden.

### Cooperative

A cooperative is a voluntary association of persons who join to meet a common economic, social or cultural need by running a jointly owned business. It follows the principle of **one member, one vote** regardless of the money invested, and profit is shared in proportion to use or share. Savings and credit cooperatives, dairy cooperatives and agricultural cooperatives are common in Nepal under the Cooperatives Act, 2074 BS (2017), and the constitution lists the cooperative as one of the three pillars of the national economy next to the public and private sectors.

### Public enterprise and non-profit bodies

A **public enterprise** is owned by the government and run for public service (for example the electricity authority or the telecom company in which the state holds a share). **Non-profit organisations** such as NGOs, clubs and trusts exist for a social purpose and use any surplus for that purpose, not for dividends. For a manager, the difference matters for goals (profit versus service), accountability (shareholders versus the public or donors) and flexibility (private firms decide faster).

### Choosing a form

| Question the founder asks | Points toward |
|---|---|
| Can I run it alone with little money? | sole proprietorship |
| Do two or three people each bring different skills and trust each other? | partnership |
| Do investors need protection from personal loss, or will outside money be needed? | private company |
| Do we need to raise large capital from many small investors? | public company |
| Is the aim mutual benefit of the users, not dividends? | cooperative |

::: example Worked example: liability under different forms
A business fails with debts of Rs 12,00,000. Its assets can pay only Rs 5,00,000, so Rs 7,00,000 is unpaid.

- **Sole proprietor:** the owner must meet the Rs 7,00,000 from personal property.
- **General partnership with two partners:** the creditor may claim the whole Rs 7,00,000 from either one; the two settle between themselves by their profit-sharing ratio, for example 60 : 40 means Rs 4,20,000 and Rs 2,80,000.
- **Company:** the shareholders lose their investments, but nobody has to pay the Rs 7,00,000 from personal property; the creditors bear that loss.
:::

## 7.2 The integrated management framework

Units 1 to 6 describe management one piece at a time: the functions, the roles, the skills, the environment, the ethics. The **integrated management framework** is the habit of looking at all of them together, because in a real job they arrive together. A single morning of a software team lead can include planning a sprint (planning), assigning tasks (organising), motivating a tired developer (leading), checking defect counts (controlling), answering a client (interpersonal role) and judging whether a feature is ethical to ship (ethics).

Figure 7.1 draws the framework in four layers.

```svgfig label="7.1" caption="The integrated management framework. Inside the organisation, managers use skills (technical, human, conceptual) to play roles (interpersonal, informational, decisional) and carry out the four functions in order to reach the goals. The whole system sits in an environment (economy, law, technology, society) and is held in shape by ethics, diversity and social responsibility; information technology runs through every layer."
f = Fig(580, 290)
f.box(8, 8, 564, 274, "", fill=SOFT, stroke=SLATE, dash=True)
f.text(20, 24, "Environment: economy, law, technology, society, competitors, customers", size=10.5, color=SLATE, bold=True, anchor="start")
f.box(30, 42, 520, 36, "ETHICS, DIVERSITY AND SOCIAL RESPONSIBILITY: the values that frame every decision", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(30, 92, 160, 82, "SKILLS\ntechnical\nhuman\nconceptual", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(210, 92, 160, 82, "ROLES\ninterpersonal\ninformational\ndecisional", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(390, 92, 160, 82, "FUNCTIONS\nplanning, organising\nleading, controlling", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(190, 133), (210, 133)], color=SLATE, sw=2)
f.arrow([(370, 133), (390, 133)], color=SLATE, sw=2)
f.box(150, 190, 280, 38, "GOALS: effectiveness and efficiency", fill=NAVY, stroke=NAVY, size=11, bold=True, color="#ffffff")
f.arrow([(110, 174), (110, 209), (150, 209)], color=SLATE, sw=1.6)
f.arrow([(470, 174), (470, 209), (430, 209)], color=SLATE, sw=1.6)
f.box(30, 242, 520, 30, "INFORMATION TECHNOLOGY: data, communication and automation in every layer", fill="#ffffff", stroke=TEAL, size=10.5, bold=True)
```

Three ideas follow from the framework.

1. **Fit.** A function, a skill or a role is good only when it matches the situation: the same planning style that suits a bank branch does not suit a start-up that changes direction every month. This is the **contingency** idea of Unit 2.
2. **Balance.** Effectiveness (doing the right things, reaching the goal) and efficiency (doing things right, with few resources) must be pursued together. A team can efficiently build a feature nobody wants.
3. **Feedback.** Results from controlling flow back into planning, and what the environment tells the organisation changes the goals. The framework is a loop, not a ladder.

## 7.3 Managing ethics and diversity, and social responsibility (revision map)

These topics are examined under Introduction in the revised outline. They are covered in depth in Unit 1 (managerial skills and challenges) and Unit 2 (section 2.5 on social responsibility and business ethics). For revision, remember the following core points.

- **Ethics** is the set of moral principles that tells people what is right. A manager meets **ethical dilemmas**, where every option has a cost; a useful test asks three questions: is it legal, is it fair to everyone affected, and could I explain it openly without shame?
- **Diversity** means differences among employees in gender, age, ethnicity, language, ability and background. Managed well it brings wider ideas and market understanding; managed badly it causes conflict and discrimination. Managers respond through fair recruitment, anti-harassment policy, flexible work and mentoring.
- **Social responsibility** is the duty of a business to act for the benefit of society as well as for profit. The **classical view** (Friedman) holds that profit is the main duty; the **socioeconomic view** holds that the firm must also protect and improve society. Areas include fair treatment of employees, honest dealing with customers, environmental protection and community development.

## 7.4 The role of IT in management

Information technology is the use of computers, networks, software and data to collect, store, process and send information. For a manager it is not a separate subject but a tool that supports each function. This book is in the BCA course, so the useful question is: which management problem does each technology solve?

| Function | Typical IT support | What it improves |
|---|---|---|
| Planning | spreadsheets and forecasting tools, dashboards, scenario simulation, project software | quality of forecasts, speed of what-if analysis |
| Decision making | management information system (MIS), decision support system (DSS), business intelligence, data mining, expert systems | decisions based on facts that arrive in time |
| Organising | organisation charts and HR software, workflow tools, ERP, shared drives, video meetings | clear tasks, remote and virtual teams |
| Leading | email, chat, intranet, e-learning, performance systems | communication and motivation at a distance |
| Controlling | real-time reports, balanced scorecard dashboards, audit logs, automated alerts | fast detection of deviation |

### IT in planning

Planning needs forecasts and alternatives. **Spreadsheets and statistical software** compare scenarios in minutes (best, expected and worst cases of sales), **project scheduling software** shows the critical path, **geographic information systems** help choose a branch location, and **enterprise resource planning (ERP)** systems share one database across finance, sales, stock and HR so that plans use the same numbers in every department. A bank that studies customer data can plan where to place the next ATM by transaction volume instead of by guess.

### IT in decision making

Managers meet three kinds of decision. **Structured** decisions repeat and have rules (approving a leave request, reordering a stock item) and can be automated by a **transaction processing system** or a rule engine. **Semi-structured** decisions mix rules and judgement (setting a discount, choosing a supplier) and use a **decision support system** that lets the manager vary the assumptions. **Unstructured** decisions are new and unclear (entering a new market) and call for judgement supported by **business intelligence** and expert advice. The higher the level of management, the more unstructured the decisions become, which is why the MIS reports for top managers are summaries and trends, and the screens for supervisors are detailed and operational.

### Advantages and limits of IT

- **Advantages:** speed, accuracy, lower routine cost, better information, communication across locations, new products and services (online banking, e-commerce).
- **Limits and risks:** high cost and training need, resistance from employees, **information overload**, dependence on systems that can fail or be attacked, privacy and security issues, and the risk that managers trust a model that is built on poor data (garbage in, garbage out).

::: example Worked example: is an inventory system worth buying?
A shop spends Rs 2,40,000 a year on losses from stock-outs, expired stock and manual counting errors. A computerised inventory system costs Rs 3,00,000 to buy and set up, lasts 5 years with no resale value, and costs Rs 30,000 a year to run. It is expected to cut the losses by 70 percent.

Saving per year = 0.70 x 2,40,000 = Rs 1,68,000. Net benefit per year = 1,68,000 - 30,000 = Rs 1,38,000. Payback period = 3,00,000 / 1,38,000 = **2.17 years**, or about 2 years 2 months. Over 5 years the total net benefit is 5 x 1,38,000 = Rs 6,90,000, which exceeds the Rs 3,00,000 cost, so the net gain is **Rs 3,90,000**. The decision supports buying, provided the 70 percent estimate is realistic; the manager should also test it with a pessimistic figure (for example 40 percent saving gives 96,000 - 30,000 = Rs 66,000 a year and a payback of 4.5 years, which is still within the 5-year life but much less comfortable).
:::

## 7.5 Job analysis, job design, job description and job specification

Organising begins with work: what tasks exist, how they are grouped into jobs, and who is suited to each job. Four related terms are used.

- **Job analysis** is the systematic study of a job to find out its tasks, duties, responsibilities, conditions and the knowledge and skills needed. Information comes from observation, interviews with job holders and supervisors, questionnaires and work logs. Its two outputs are the job description and the job specification.
- **Job description** states **what the job is**: title, purpose, reporting line, main duties, tools and working conditions.
- **Job specification** states **who is needed**: qualification, experience, skills, knowledge and personal traits.
- **Job design** decides **how the tasks are combined** into a job so that work gets done efficiently and the job holder stays motivated.

| Job description | Job specification |
|---|---|
| about the job | about the person |
| duties, tasks, reporting line, conditions | education, skills, experience, traits |
| used for orientation, performance review, job evaluation | used for recruitment and selection |
| Example: "tests each release and reports defects" | Example: "BCA degree and two years of manual and automated testing" |

### Job design approaches

1. **Job simplification (specialisation).** The job is broken into small, repeated tasks (Taylor). Training is quick and output is high, but boredom, error and absence grow.
2. **Job rotation.** Workers move between jobs at the same level at planned intervals. It spreads skills and relieves boredom but does not make any single job richer.
3. **Job enlargement (horizontal loading).** More tasks of the same level are added, for example a data-entry operator also checks the entries.
4. **Job enrichment (vertical loading).** Planning, decision and control are added to the job so the person has more **autonomy and responsibility**. This follows Herzberg's two-factor theory, where achievement, responsibility and growth are motivators.
5. **Job characteristics model (Hackman and Oldham).** A job motivates when it has **skill variety, task identity, task significance, autonomy and feedback**. These create meaningful work, a feeling of responsibility and knowledge of results, which raise motivation, satisfaction and performance. A growth-need strength of the person moderates the effect.
6. **Modern designs:** flexible hours, job sharing, telecommuting (work from home), and **self-managed teams**.

### Sample job description and job specification

::: example A complete sample: Junior Software Tester, Himal Digital Pvt. Ltd.
**Job description.** Title: Junior Software Tester. Department: Quality Assurance. Reports to: QA Lead. Purpose: make sure each release of the company's web applications meets the agreed requirements before delivery.

*Main duties:* (1) read requirements and write test cases; (2) run manual tests on each build; (3) record defects with steps to reproduce, screenshots and severity; (4) retest fixed defects; (5) update the test report each week; (6) help automate stable test cases under supervision. *Working conditions:* office hours, occasional extended hours before a release.

**Job specification.** *Education:* BCA or equivalent. *Knowledge:* software testing basics, SQL queries, browser developer tools. *Skills:* careful observation, clear written reports, ability to work in a team. *Experience:* none required for a junior post; internship preferred. *Traits:* patience, honesty in reporting, willingness to learn.
:::

Notice that the description would not change if a different person filled the job, while the specification would change if the company moved from manual to automated testing. Both must be revised when the job changes.

## 7.6 Authority distribution and forms of organisational design

Unit 4 covers authority, responsibility, delegation and centralisation. In the revised outline these are grouped as **authority distribution**. Remember the summary: **line authority** is the right to direct subordinates through the chain of command; **staff authority** is the right to advise and support; **functional authority** gives a specialist (such as the HR manager) the right to direct others on one subject. **Delegation** passes authority to carry out tasks to a subordinate while the manager keeps the accountability; **decentralisation** is the systematic spreading of decision power to many levels.

An **organisational design** is the formal arrangement of jobs, departments and reporting lines. The commonly taught forms are below.

| Form | How the work is grouped | Strengths | Weaknesses | Typical IT example |
|---|---|---|---|---|
| **Functional** | by specialist function: development, testing, sales, finance | depth of expertise, no duplication, clear careers | silos, slow cross-department decisions | a small software house |
| **Divisional** | by product, customer or region, each division with its own functions | responds to markets, clear profit responsibility | duplication of resources, competition between divisions | a telecom with mobile, internet and enterprise divisions |
| **Matrix** | a grid; each person reports to a functional manager and to a project manager | shares scarce experts across projects, flexible | **two bosses**, conflict, confusion | a consulting firm that runs many client projects |
| **Team-based** | work done by cross-functional teams with few levels | speed, high involvement | needs skilled team members, role ambiguity | agile product teams |
| **Network** | the core firm keeps its main skill and outsources other activities through contracts | low cost, flexibility | less control over partners, dependence | a start-up that outsources hosting, payment and design |
| **Virtual** | members in different places work through information technology | access to talent anywhere, low office cost | trust, time-zone and communication problems | a remote-first open-source company |

```svgfig label="7.2" caption="Three common organisational designs drawn as reporting lines. In the functional form every person has one boss and the departments are grouped by speciality. In the divisional form each product division has its own copies of the functions. In the matrix form each specialist (a row) works on projects (a column) and answers to two managers, which gives flexibility but divides loyalty."
f = Fig(580, 270)
f.text(95, 14, "FUNCTIONAL", size=11, color=NAVY, bold=True)
f.box(45, 24, 100, 28, "CEO", fill=NAVY, stroke=NAVY, size=10.5, bold=True, color="#ffffff")
f.box(8, 90, 54, 30, "Dev", fill=BLUE, stroke=NAVY, size=10)
f.box(68, 90, 54, 30, "Test", fill=BLUE, stroke=NAVY, size=10)
f.box(128, 90, 54, 30, "Sales", fill=BLUE, stroke=NAVY, size=10)
f.arrow([(95, 52), (95, 70), (35, 70), (35, 90)], color=SLATE, sw=1.4)
f.arrow([(95, 52), (95, 90)], color=SLATE, sw=1.4)
f.arrow([(95, 70), (155, 70), (155, 90)], color=SLATE, sw=1.4)
f.text(95, 140, "one boss each", size=10, color=SLATE)
f.text(262, 14, "DIVISIONAL", size=11, color=TEAL, bold=True)
f.box(212, 24, 100, 28, "CEO", fill=NAVY, stroke=NAVY, size=10.5, bold=True, color="#ffffff")
f.box(198, 80, 62, 28, "Mobile", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(268, 80, 62, 28, "Internet", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(262, 52), (262, 66), (229, 66), (229, 80)], color=SLATE, sw=1.4)
f.arrow([(262, 52), (262, 66), (299, 66), (299, 80)], color=SLATE, sw=1.4)
f.box(198, 120, 62, 24, "Dev+Sales", fill=SOFT, stroke=TEAL, size=9.5)
f.box(268, 120, 62, 24, "Dev+Sales", fill=SOFT, stroke=TEAL, size=9.5)
f.arrow([(229, 108), (229, 120)], color=SLATE, sw=1.4)
f.arrow([(299, 108), (299, 120)], color=SLATE, sw=1.4)
f.text(264, 162, "functions repeated per division", size=10, color=SLATE)
f.text(485, 14, "MATRIX", size=11, color=AMBER, bold=True)
f.box(450, 28, 58, 24, "Project A", fill=SAND, stroke=AMBER, size=10)
f.box(520, 28, 58, 24, "Project B", fill=SAND, stroke=AMBER, size=10)
f.box(385, 64, 50, 30, "Dev", fill=BLUE, stroke=NAVY, size=10)
f.box(385, 104, 50, 30, "Test", fill=BLUE, stroke=NAVY, size=10)
for x in (479, 549):
    for y in (79, 119):
        f.circle(x, y, 9, fill=NAVY, stroke=NAVY)
f.arrow([(435, 79), (468, 79)], color=SLATE, sw=1.2)
f.arrow([(435, 119), (468, 119)], color=SLATE, sw=1.2)
f.arrow([(479, 52), (479, 68)], color=RED, sw=1.2)
f.arrow([(549, 52), (549, 68)], color=RED, sw=1.2)
f.text(480, 162, "two bosses: row and column", size=10, color=SLATE)
f.box(8, 190, 564, 66, "Rule of thumb. Stable work and one product: functional. Many products or regions: divisional.\nMany projects sharing a few experts: matrix. Fast, changing work: teams.\nLow-cost growth through partners: network. Remote talent: virtual.", fill=SOFT, stroke=SLATE, size=10.5)
```

## 7.7 Approaches to leadership: generic, situational and emerging

**Leadership** is the process of influencing people to work willingly toward group goals (see section 5.1). The revised outline arranges the theories in three families, which mirror the history of leadership research: first people asked **who** leaders are, then **what** they do, then **in which situation** a style works, and recently **how** leaders change people and organisations.

### Generic approaches: traits and behaviours

**Trait approach.** Early researchers listed the personal qualities of great leaders: intelligence, self-confidence, determination, integrity and sociability. Studies found that no list of traits guarantees success and that traits can be learned or hidden, so the approach was abandoned as a complete theory, though traits such as integrity and drive still matter in selection.

**Behavioural approach.** If leaders are made, then the behaviour is the thing to study.

- **Ohio State studies:** two independent dimensions, **initiating structure** (defining tasks and roles, setting deadlines) and **consideration** (respect, warmth, concern for people). A leader can be high or low on each.
- **University of Michigan studies:** **job-centred** versus **employee-centred** leaders; the employee-centred ones tended to have more productive groups.
- **Blake and Mouton's Managerial Grid** plots concern for production against concern for people on 1 to 9 scales:

| Position | Style | Meaning |
|---|---|---|
| (1,1) | impoverished | minimum effort for both; the leader has withdrawn |
| (9,1) | authority-compliance | results first; people are treated as tools |
| (1,9) | country club | friendly atmosphere; tasks are neglected |
| (5,5) | middle of the road | balance by compromise, adequate performance |
| (9,9) | team management | committed people, shared purpose, high results; presented as the ideal |

**Autocratic, democratic and laissez-faire** styles (Lewin) are also grouped here: the leader decides alone, decides with the group, or leaves the group to decide.

### Situational (contingency) approaches

The best style depends on the situation. Four models are standard.

1. **Fiedler's contingency model.** The leader's style is fixed and is measured by the **least preferred co-worker (LPC)** scale: a high LPC score means relationship-oriented, a low score means task-oriented. Effectiveness depends on **situational favourableness**, which is made up of **leader-member relations, task structure and position power**. Task-oriented leaders do best in very favourable and very unfavourable situations; relationship-oriented leaders do best in the middle. The practical lesson is to **change the situation, not the person**.
2. **Hersey and Blanchard's situational leadership.** The leader adapts the style to the **readiness (maturity)** of followers, which is a mix of ability and willingness.

| Follower readiness | Style | Task behaviour | Relationship behaviour |
|---|---|---|---|
| R1: unable and unwilling or insecure | **telling** (directing) | high | low |
| R2: unable but willing | **selling** (coaching) | high | high |
| R3: able but unwilling or insecure | **participating** (supporting) | low | high |
| R4: able and willing | **delegating** | low | low |

3. **House's path-goal theory.** The leader's job is to clear the path to the goal and to raise the rewards. Four styles: **directive, supportive, participative** and **achievement-oriented**, chosen to suit the subordinates (for example, those with high ability dislike directive leadership) and the task (a vague task needs direction).
4. **Vroom-Yetton-Jago decision model.** The leader chooses how much to involve the group (decide alone, consult individually, consult as a group, or let the group decide) by answering questions about decision quality, available information, acceptance needed and time available.

### Emerging approaches

- **Transformational leadership** (Burns 1978; Bass). The leader raises followers' motives and morals and moves them beyond self-interest toward a shared vision. Four components, the "four I's": **idealised influence** (a role model), **inspirational motivation** (vision and optimism), **intellectual stimulation** (questioning and creativity) and **individualised consideration** (coaching each person). Contrast **transactional leadership**, which exchanges rewards for performance and corrects deviations.
- **Charismatic leadership.** Followers attribute exceptional ability to a leader with a strong personality and vision. It can inspire, but it also carries the risk of dependence on one person and of misuse.
- **Servant leadership** (Greenleaf 1970). The leader serves first: listens, develops people and puts the needs of followers and community ahead of personal power.
- **Authentic leadership.** The leader is self-aware, acts on stated values, is transparent and weighs balanced information before deciding.
- **Emotional intelligence in leadership** (Goleman): self-awareness, self-regulation, motivation, **empathy** and social skill predict how well a leader handles people.
- **Distributed and shared leadership.** Leadership moves to whoever has the knowledge for the task, as in agile teams where the developer who knows the module leads that discussion.

::: example Worked example: choosing a style with the Hersey-Blanchard model
Ramesh leads a four-person development team. A new member, Sita, has just joined, has never used the company's framework and is nervous: she is **unable and insecure** (R1), so Ramesh uses **telling**: a clear task list, pair programming and daily check-in. After two months she delivers well but sometimes doubts her choices (**able but insecure**, R3), so he moves to **participating**: asking her opinion and praising her decisions, with fewer instructions. When she works confidently on her own (R4), he **delegates** whole modules. If the company switches to a new language, Sita's readiness for that new task drops back to R1 and the style must move back to telling, because readiness is **task-specific**, not a permanent label for the person.
:::

## 7.8 Managing teams in a time of crisis

A **crisis** is a sudden, serious event that threatens people, assets or reputation and leaves little time to decide: a fire in the office, a data breach, a pandemic lockdown, a major outage during the election results, or an earthquake like that of 2015 in Nepal. Normal planning is not enough, and the leader's behaviour decides whether the team holds together.

### Stages of a crisis

1. **Before (preparation):** risk assessment, a written **crisis plan**, named roles, training and drills, backups, contact lists.
2. **During (response):** detect and confirm the event, activate the crisis team, protect life first, then assets, communicate quickly and honestly, make decisions with incomplete information.
3. **After (recovery and learning):** restore operations, support affected people, review what happened without blame, update the plan.

### What leaders should do

- **Stay calm and visible.** A leader who looks anxious spreads anxiety; one who is present and steady gives the team a point of reference.
- **Set priorities and give clear, short instructions.** In a crisis a more directive style (telling) is usually correct, because there is no time to build consensus; return to participation when the pressure falls.
- **Communicate often and truthfully.** State what is known, what is not known and when the next update will come. Silence invites rumour. Use one channel as the single source of truth.
- **Assign roles in a small crisis team:** incident commander (decides), operations lead (fixes), communication lead (informs staff, customers, media), and a scribe who logs times and actions.
- **Care for people.** Fatigue, fear and family worries reduce judgement; plan rest in shifts and recognise effort.
- **Decide and adjust.** Take the best available decision, watch the result and correct it quickly; avoid both paralysis and recklessness.
- **Learn.** A **post-incident review** records the timeline, causes and improvements and is blameless, because blame teaches people to hide problems.

::: example Short case: a ransomware attack at a bank branch network
On a Sunday night the file servers of a small finance company show encrypted files and a ransom note. The IT manager acts as incident commander. Within the first hour she **isolates** the affected servers from the network, calls the crisis team (operations, legal, communication), and tells the managing director what is known and not known. The communication lead informs branch managers by phone and prepares a short customer notice for Monday: services are slow, customer money and data are being protected. The team restores from the offline backup taken on Saturday, losing about a day of transactions that branch staff re-enter from paper slips. The following week a blameless review finds that one unpatched server was the entry point; patching, staff training on phishing and a second offline backup are added to the plan. Notice the sequence: protect, communicate, recover, learn.
:::

## 7.9 Leadership challenges in an IT-based organisation

IT firms and IT departments have features that make leadership harder than in a traditional factory or office.

| Challenge | Why it arises | What a good leader does |
|---|---|---|
| **Fast change** in tools and markets | skills become outdated in a few years | build a learning culture, allow time for training, keep plans short and revisable |
| **Managing knowledge workers** | developers know more about their work than the manager | lead by vision and trust, not by command; give autonomy; judge by outcomes |
| **Attracting and keeping talent** | strong demand and migration of skilled people abroad | fair pay and growth paths, interesting work, recognition, flexible conditions |
| **Remote and distributed teams** | people in different places and time zones | clear written communication, agreed working hours, regular video meetings, trust |
| **Deadline pressure and burnout** | fixed release dates, overtime, on-call duty | realistic estimates, protect rest, share on-call duty, discuss workload openly |
| **Technology versus people** | technical experts promoted to manager lack people skills | train managers in communication, coaching and conflict handling (the human skill of Katz) |
| **Ethics and security** | systems hold personal data and affect lives | set standards, support whistle-blowing, insist on privacy and testing, say no to harmful features |
| **Diverse and cross-cultural teams** | clients and colleagues from different countries | cultural awareness, inclusive meetings, language support |
| **Innovation versus stability** | customers want both new features and no outages | separate experiments from production, use staged releases |
| **Measuring performance** | creative work is hard to count (lines of code is a poor measure) | use outcomes, quality, peer review and customer feedback together |

A style that fits most of these is a blend of **transformational** leadership (a shared vision of what the product will do for users), **servant** leadership (removing obstacles for the team) and a **situational** adjustment to each person and task. The one thing that does not change is the **human skill**: listening, explaining and being fair.

## Key facts at a glance

| Topic | Remember |
|---|---|
| Forms of business | sole proprietorship, partnership, private and public company, cooperative, public enterprise; liability and capital are the main differences |
| Integrated framework | skills, roles and functions, set in the environment, held by ethics and supported by IT |
| IT and decisions | structured (automate), semi-structured (DSS), unstructured (judgement and BI) |
| Job analysis outputs | job description (the job) and job specification (the person) |
| Job design | simplification, rotation, enlargement, enrichment, job characteristics model |
| Designs | functional, divisional, matrix, team, network, virtual |
| Behavioural leadership | Ohio State (structure and consideration), Michigan, Managerial Grid (1,1) to (9,9) |
| Situational leadership | Fiedler, Hersey-Blanchard (telling, selling, participating, delegating), path-goal, Vroom-Yetton-Jago |
| Emerging leadership | transformational, charismatic, servant, authentic, emotional intelligence |
| Crisis leadership | prepare, respond, recover; calm, clear, truthful, caring, learning |

## Chapter summary

- A form of business is chosen by liability, capital, control and continuity; companies give limited liability and perpetual succession, sole traders and general partners carry unlimited liability.
- The integrated framework shows management as skills, roles and functions inside an environment, steered by ethics and supported by IT.
- IT supports planning, decision making, organising, leading and controlling; it helps structured decisions most and unstructured decisions least, and a cost-benefit view (payback) tests an IT purchase.
- Job analysis produces the description and the specification; job design ranges from simplification to enrichment and the job characteristics model.
- Organisational design may be functional, divisional, matrix, team, network or virtual, each with a trade-off.
- Leadership theories moved from traits to behaviour, to situation, to transformation and service; no single style is best, and a crisis calls for calm, directive and honest leadership.
- IT organisations ask for leaders who combine vision, trust in experts, care for people and a firm ethical line.

## Practice

1. Define a business and compare a sole proprietorship, a partnership and a private limited company on liability, capital and continuity.
2. A business fails owing Rs 9,00,000 and its assets raise Rs 4,00,000. Explain who pays the Rs 5,00,000 shortfall under (a) sole proprietorship, (b) a general partnership of three partners sharing 50 : 30 : 20, (c) a private limited company.
3. Explain the integrated management framework with a diagram.
4. Explain with examples how IT supports any three functions of management.
5. Differentiate structured, semi-structured and unstructured decisions and name the IT tool suited to each.
6. A shop loses Rs 1,80,000 a year through stock problems. A software system costs Rs 2,40,000, runs at Rs 20,000 a year and is expected to remove 60 percent of the losses. Compute the payback period.
7. Differentiate job analysis, job description, job specification and job design.
8. Write a job description and a job specification for the post of "Network Support Officer".
9. Explain job enlargement, job enrichment and the five core characteristics of the Hackman-Oldham model.
10. Compare the functional, divisional and matrix designs with strengths, weaknesses and an IT example for each.
11. Explain the behavioural approach to leadership with the Managerial Grid.
12. Explain Fiedler's contingency model and Hersey-Blanchard's situational leadership model.
13. Explain transformational, servant and authentic leadership. How do they differ from transactional leadership?
14. How should a leader manage a team during a crisis? Use a data-breach example.
15. Discuss the leadership challenges of an IT-based organisation and suggest how a manager can meet any five of them.

::: note Answers and worked solutions
**1.** A business supplies goods or services for profit. *Liability:* sole proprietor and general partners unlimited, company shareholders limited to their investment. *Capital:* sole proprietor smallest, partnership larger, private company larger again but not from the public. *Continuity:* the sole proprietorship and partnership may end with the owner or a partner, the company has perpetual succession.
**2.** Shortfall = 9,00,000 - 4,00,000 = Rs 5,00,000. (a) The proprietor pays all Rs 5,00,000 from personal property. (b) A creditor may claim the whole amount from any partner; among themselves the shares are 50 percent = Rs 2,50,000, 30 percent = Rs 1,50,000 and 20 percent = Rs 1,00,000. (c) Shareholders lose only their invested money; the creditors absorb the Rs 5,00,000 loss.
**3.** Draw Figure 7.1: skills, roles and functions leading to goals, inside an environment, framed by ethics, diversity and social responsibility, with IT across all layers; explain fit, balance and feedback.
**4.** Planning: spreadsheets, forecasting and scheduling software. Decision making: MIS and DSS. Controlling: dashboards and automated alerts. Organising: ERP and workflow tools. Leading: email, chat and e-learning. Explain any three with one example each.
**5.** Structured: routine with rules (leave approval): transaction processing or a rule engine. Semi-structured: rules plus judgement (supplier selection): DSS. Unstructured: new and unclear (entering a market): business intelligence plus expert judgement.
**6.** Saving = 0.60 x 1,80,000 = Rs 1,08,000; net = 1,08,000 - 20,000 = Rs 88,000 a year; payback = 2,40,000 / 88,000 = **2.73 years** (about 2 years 9 months).
**7.** Analysis is the study of a job; the description records what the job is; the specification records the person needed; design decides how tasks are combined to make the job efficient and motivating.
**8.** Use the format of the sample in 7.5: title, department, reporting line, purpose, duties (monitor network, fix faults, maintain cabling, record tickets, update documents) for the description; qualification (BCA or diploma, networking certification), skills (routing, switching, troubleshooting), experience, traits for the specification.
**9.** Enlargement adds tasks of the same level; enrichment adds planning and control and responsibility. Core characteristics: skill variety, task identity, task significance, autonomy, feedback.
**10.** Use the table in 7.6: functional (expertise, silos; small software house), divisional (market focus, duplication; telecom with product divisions), matrix (shared experts, two bosses; consulting firm).
**11.** Ohio State: initiating structure and consideration; Michigan: job-centred and employee-centred; the Grid: (1,1) impoverished, (9,1) authority-compliance, (1,9) country club, (5,5) middle of the road, (9,9) team management, the recommended style.
**12.** Fiedler: style fixed (LPC), effectiveness depends on leader-member relations, task structure and position power. Hersey-Blanchard: style follows follower readiness: telling, selling, participating, delegating (R1 to R4).
**13.** Transformational: vision and the four I's; servant: serves followers' growth first; authentic: self-aware, value-led and transparent; transactional uses exchange of reward for performance and corrects errors.
**14.** Isolate the affected systems, form the crisis team with roles, give clear directions, communicate truthfully to staff and customers, restore from backups, review without blame and update the plan (see the ransomware case in 7.8).
**15.** Any five from the table in 7.9: rapid change, knowledge workers, talent retention, remote teams, burnout, ethics and security; give one leadership response for each.
:::

## Model answers (5 and 10 marks)

**Q1 (5 marks). Explain the forms of business organisation with their merits and demerits.**

*Introduction.* The form of business is the legal structure that decides ownership, liability, capital and control.

1. **Sole proprietorship.** One owner. Merits: easy formation, quick decisions, full profit. Demerits: unlimited liability, limited capital, uncertain life.
2. **Partnership.** Two or more persons share profit and loss under a deed (Partnership Act, 2020 BS). Merits: more capital and skills, shared risk. Demerits: joint unlimited liability, disputes, instability.
3. **Company.** A registered legal person (Companies Act, 2063 BS), private or public. Merits: limited liability, large capital, perpetual succession. Demerits: formalities, disclosure, separation of ownership and control.
4. **Cooperative.** Members of a common need own and manage it on one member, one vote. Merits: mutual help, democratic control. Demerits: limited capital and professional skill.

*Conclusion.* The choice depends on the scale, capital need, risk, and the number of persons involved.

**Q2 (5 marks). What is job analysis? Differentiate job description and job specification, with an example.**

*Introduction.* Job analysis is the systematic study of tasks, responsibilities and requirements of a job, using observation, interview and questionnaires.

*Outputs.* The **job description** states the title, reporting line, duties and conditions, so it is about the job. The **job specification** lists the education, experience, skills and traits needed, so it is about the person. For a junior software tester, the description lists writing test cases, running tests and reporting defects; the specification asks for a BCA, knowledge of SQL, attention to detail and clear writing.

*Uses.* Recruitment, selection, training, performance appraisal and pay decisions depend on these documents.

**Q3 (10 marks). Discuss the situational approaches to leadership. Use Fiedler's and Hersey-Blanchard's models in the answer.**

*Introduction.* Early trait and behavioural studies failed to find one style that works everywhere. Situational (contingency) approaches say that effective leadership depends on the match between the leader, the followers and the situation.

1. **Fiedler's contingency model.** The leader's style is measured by the least preferred co-worker scale; a high LPC score marks a relationship-oriented leader and a low score a task-oriented one. The situation is rated by **leader-member relations, task structure and position power**, which together make the situation favourable or unfavourable. Task-oriented leaders do best in the most and least favourable situations, relationship-oriented leaders in the moderate ones. Since style is hard to change, management should **change the situation** (for example, give more position power) or **match the leader to it**.
2. **Hersey and Blanchard's situational leadership.** The leader changes style with follower readiness: R1 (unable, unwilling) **telling**, R2 (unable, willing) **selling**, R3 (able, unwilling) **participating**, R4 (able, willing) **delegating**. Readiness is task-specific, so the same person can need different styles on different tasks.
3. **Path-goal theory.** The leader chooses directive, supportive, participative or achievement-oriented behaviour to clear the follower's path to the goal and raise rewards.
4. **Vroom-Yetton-Jago model.** The degree of participation in a decision is selected by decision quality, information, acceptance and time.

*Evaluation.* The models are realistic and useful, but Fiedler's LPC measure is criticised, and Hersey-Blanchard has weak research support although it is easy to apply.

*Conclusion.* In practice a manager should read the situation, diagnose the readiness of followers and flex the style.

**Q4 (10 marks). Explain the role of IT in management. Discuss the benefits and risks for a modern organisation.**

*Introduction.* IT is the use of hardware, software, networks and data to collect and share information. It supports each management function.

1. **Planning:** spreadsheets, forecasting and scheduling software, ERP data for realistic plans.
2. **Decision making:** MIS reports, DSS for what-if analysis, and business intelligence for large data; structured decisions can be automated.
3. **Organising:** ERP, workflow and HR systems, shared documents and video meetings support virtual teams.
4. **Leading:** email, chat and e-learning keep communication and training going across locations.
5. **Controlling:** dashboards, alerts and audit trails compare results with standards at once.

*Benefits.* Speed, accuracy, lower routine cost, better information, new services and wider markets.

*Risks.* High cost and training, resistance to change, information overload, system failure, cyber attack and privacy problems, and over-trust in poor data. A cost-benefit check, such as payback period, helps decide which investments to make.

*Conclusion.* IT improves management only when it is matched with sound goals, trained people and good security.

---
subject: Professional Communication and Ethics
grade: BCA Semester 1
unit: 4
title: Interpersonal and Group Communication
area: BCA 105 · Professional Communication and Ethics · Unit 4
---

Most of a working day is spent with other people: a senior who gives a task, a classmate who needs a file, a client who is unhappy, a team that must ship a project on Friday. This unit studies communication between individuals and inside groups. It covers interpersonal communication in the workplace, the listening environment, intercultural communication, effective communication in teams (including virtual teams and what makes a team successful), leadership and communication, and the skill of adapting your style to different audiences. It ends with vocabulary and grammar for the topic and two prescribed readings: "Computer and the Pursuit of Happiness" by David Gelernter and "The Collapse of the Family and the Community" by Yuval Noah Harari.

::: key What this unit gives you
- Interpersonal communication in the workplace: its features, types of relationships, and skills (4.1).
- The listening environment: barriers inside and around the listener, and how a workplace builds a listening culture (4.2).
- Intercultural communication: culture, Hofstede and Hall models, stereotypes and practical rules (4.3).
- Effective communication in teams and the rise of virtual teams (4.4); what defines a successful team (4.5).
- Leadership and communication, including adapting communication styles to diverse audiences (4.6).
- Vocabulary and grammar (4.7); reading notes, analysis and solved exercises for two prescribed readings (4.8).
:::

## 4.1 Interpersonal communication in the workplace

**Interpersonal communication** is the exchange of messages, verbal and non-verbal, between two (or a few) people who influence each other and build a relationship through the exchange. It differs from mass communication (one source, many unseen receivers) and from public speaking (one speaker, a large audience, little feedback). In the workplace it is the daily traffic of instructions, requests, updates, jokes, complaints and thanks.

### Features of interpersonal communication

1. **Two-way and immediate.** Sender and receiver swap roles all the time; feedback arrives at once, as a nod, a frown or a question.
2. **Personal and relational.** Every message carries a *content* level (what is said) and a *relationship* level (how the two people stand to each other). "Send me the file" and "Could you please send me the file when you get a minute?" have the same content but different relationship messages.
3. **Rich in channels.** Face to face, words, voice, face, gaze, posture and space all work together (see 1.5).
4. **Irreversible.** What has been said cannot be unsaid; a harsh word to a colleague stays in memory even after an apology.
5. **Contextual.** The same sentence means different things in a staff room, in a client meeting and in a group chat.
6. **Ethical.** Honesty, respect and confidentiality apply to every conversation, not only to formal documents.

### Types of workplace relationships and directions of flow

| Direction | Between | Typical content | Common problem |
|---|---|---|---|
| **Downward** | manager to team | instructions, goals, policy, feedback | too little context; commands without reasons |
| **Upward** | team to manager | progress, problems, suggestions | fear of giving bad news; filtering |
| **Horizontal (lateral)** | peers | coordination, sharing information | rivalry; silos between departments |
| **Diagonal** | across levels and departments | cross-functional projects | unclear authority |
| **Grapevine** | informal network | rumours, gossip, mood | distortion; can be managed by openness |

### The Johari Window

The **Johari Window** (Joseph Luft and Harrington Ingham, 1955) is a simple model of how well people know each other. It divides what is known about a person into four areas.

| | **Known to self** | **Not known to self** |
|---|---|---|
| **Known to others** | **Open (arena):** shared facts, opinions, behaviour | **Blind spot:** habits others see but you do not (always interrupting) |
| **Not known to others** | **Hidden (facade):** private things you choose not to share | **Unknown:** unrealised abilities and feelings |

Trust grows when the **open** area expands: you *disclose* appropriate information about yourself (shrinking the hidden area) and you *ask for and accept feedback* (shrinking the blind spot). In a new project team, a student who says "I am strong in front end but weak in databases; please review my SQL" enlarges the open area and helps the team plan.

```svgfig label="4.2" caption="The Johari Window. Asking for feedback shrinks the blind spot and appropriate self-disclosure shrinks the hidden area; both enlarge the open area, where communication is easiest and trust is highest."
f = Fig(760, 290)
f.text(255, 20, "Known to self", size=11.5, color=NAVY, bold=True)
f.text(425, 20, "Not known to self", size=11.5, color=NAVY, bold=True)
f.text(110, 82, "Known to others", size=11.5, color=NAVY, bold=True)
f.text(110, 192, "Not known to others", size=11.5, color=NAVY, bold=True)
cells = [(170, 34, "OPEN", "free to all", MINT), (340, 34, "BLIND SPOT", "others see it, you do not", ROSE),
         (170, 144, "HIDDEN", "you know, others do not", BLUE), (340, 144, "UNKNOWN", "neither side knows yet", SAND)]
for x, y, t, s, col in cells:
    f.box(x, y, 168, 106, "", fill=col, stroke=NAVY)
    f.text(x + 84, y + 44, t, size=13, color=NAVY, bold=True)
    f.text(x + 84, y + 66, s, size=10, color=SLATE)
f.arrow([(520, 70), (560, 70)], color=TEAL, sw=2)
f.text(572, 66, "feedback", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(572, 80, "shrinks blind spot", size=10, color=SLATE, anchor="start")
f.arrow([(520, 196), (560, 196)], color=TEAL, sw=2)
f.text(572, 192, "disclosure", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(572, 206, "shrinks hidden area", size=10, color=SLATE, anchor="start")
f.text(425, 280, "Aim: a larger open area.", size=10.5, color=SLATE)
```

### Interpersonal skills for professionals

- **Active listening** (4.2) and **empathy**: understand the other person's feelings before replying.
- **Assertiveness**: stating your needs and views clearly and respectfully, neither passive (staying silent) nor aggressive (attacking). "I cannot finish all three modules by Wednesday; I can finish two. Which should I drop?" is assertive.
- **Questioning**: open questions ("What worries you about the deadline?") to explore, closed questions ("Is the server ready?") to confirm.
- **Giving and receiving feedback** (SBI model, below).
- **Respect for hierarchy without fear**: address seniors courteously, but report problems early.
- **Rapport and small talk**: a short, sincere greeting builds the trust that makes difficult conversations possible.
- **Emotional intelligence** (Daniel Goleman): self-awareness, self-regulation, motivation, empathy and social skill.

::: example Worked example: feedback with the SBI model
**Situation:** In yesterday's sprint review, **Behaviour:** you showed the demo without testing the login page, **Impact:** it crashed in front of the client and we lost ten minutes. Next time, could we run a five-minute smoke test before the demo?
The comment names a situation, describes an observable behaviour (not "you are careless"), states the impact, and ends with a request. The receiver can act on it.
:::

### Conflict in interpersonal communication

Conflict is normal where people share goals, scarce resources and different habits. Thomas and Kilmann describe five styles: **competing, collaborating, compromising, avoiding and accommodating**. Collaborating (solving the problem so that both sides gain) is best for important issues; avoiding is sensible only for trivial matters or to cool down. Steps: (1) choose a private time; (2) state the issue, not the person; (3) listen to the other view and repeat it; (4) agree on common interests; (5) write down the action and a review date.

## 4.2 Listening environment in the workplace

**Listening** is the active process of receiving, attending to, understanding, evaluating and responding to messages. **Hearing** is only the physical act of sound reaching the ear. Managers spend about half their communication time listening, but studies repeatedly show that people recall only a fraction of what they have just heard, so listening must be trained.

### Stages of listening

**Receiving** (sensing) → **attending** (choosing to focus) → **understanding** (decoding meaning) → **evaluating** (judging) → **responding** (feedback) → **remembering**. A break in any stage breaks the chain.

### Types of listening

| Type | Purpose | Example |
|---|---|---|
| **Informational** | learn facts | a lecture, a briefing on the new server |
| **Critical (evaluative)** | judge arguments | a vendor's sales pitch |
| **Empathic (therapeutic)** | understand and support feelings | a colleague who is stressed |
| **Appreciative** | enjoy | music, a speech, a story |
| **Active** | show attention and confirm meaning | repeat, paraphrase, ask |

### What is a listening environment?

A **listening environment** is the physical, social and organisational setting that makes it easy or hard for people to listen to each other. A manager can have excellent personal skills and still fail if the room is noisy, the meeting is overloaded, or people are punished for speaking up.

**Physical factors:** noise (generators, traffic, open offices), poor acoustics, bad audio on an online call, uncomfortable temperature, phones and notifications, seating that stops eye contact.
**Psychological factors:** stress, fatigue, prejudice about the speaker, defensiveness, daydreaming, the habit of preparing a reply while the other person is still speaking.
**Organisational factors:** meetings with no agenda, information overload, strict hierarchy that discourages bottom-up messages, no channel for questions, a culture that rewards talking over listening.
**Semantic factors:** jargon, unfamiliar accents, a language that is not the listener's first language.

::: key Building a listening culture
- Put phones away or face down in meetings; give a clear agenda and time limit.
- Choose a quiet room; check microphones and screen-sharing in virtual meetings.
- Invite quiet members to speak ("Sita, what is your view?"); do not let two voices dominate.
- Paraphrase before you reply: "So you are saying the database should move first. Is that right?"
- Reward bad news that arrives early; never shoot the messenger.
- Take short written notes and circulate action points afterwards.
:::

### Poor listening habits to avoid

*Pseudo-listening* (pretending), *selective listening* (hearing only what you like), *interrupting*, *finishing the speaker's sentences*, *jumping to conclusions*, *defensive listening* (hearing criticism as attack), and *stage hogging* (turning every story into your own).

### Active listening: a short method

Face the speaker, keep an open posture and eye contact (as culture allows), **nod and use minimal encouragers** ("I see", "go on"), **paraphrase** content, **reflect** feelings ("You sound worried about the deadline"), **ask clarifying questions**, **summarise** at the end, and **do not interrupt**.

::: example Worked example: bad listening versus good listening
*Bad:* Ram: "The payment API keeps timing out." Hari (typing, not looking): "Yes, yes, restart it." Ram leaves without being heard; the real fault, a wrong timeout setting, stays.
*Good:* Hari stops typing: "Timing out how often, and since when?" Ram: "Since the update yesterday." Hari: "So it started with the update; let us check that setting." The problem is solved in ten minutes because Hari questioned and paraphrased.
:::

## 4.3 Intercultural communication

**Culture** is the shared set of values, beliefs, customs, language, symbols and behaviours of a group that is learned and passed on. **Intercultural communication** is communication between people whose cultural backgrounds are different enough to change how messages are sent and understood. In Nepal this is a daily matter: a Newar, a Tharu and a Sherpa classmate, a Maithili-speaking client in Janakpur, a Chinese or Indian vendor, a Korean employer, a remote team lead in Germany.

### Why it matters in IT

Software teams are global. Nepali developers work for clients in the USA, Europe and Australia; students move abroad; products are used by people who read different languages and expect different colours, dates and names. Poor cultural awareness causes missed deadlines ("yes" that meant "I heard you"), offence (a gesture or joke), and bad products (a form that demands a surname from people who have none).

### Dimensions of culture

**Edward T. Hall: high-context and low-context cultures.**

| | **High-context** | **Low-context** |
|---|---|---|
| Meaning lies in | the situation, relationship, tone and what is *not* said | the explicit words |
| Style | indirect, polite, face-saving | direct, precise, written |
| "No" is expressed as | "We will try", "It is difficult", silence | "No, we cannot" |
| Examples (broadly) | Nepal, India, Japan, China, Arab countries | USA, Germany, Scandinavia, Australia |
| Agreements | built on trust, can be verbal | in detail in a written contract |

**Geert Hofstede's dimensions** (original four, later extended): *power distance* (how far less powerful members accept unequal power: high in Nepal, so juniors rarely contradict seniors in public); *individualism versus collectivism* (self versus group loyalty); *masculinity versus femininity* (competition versus care); *uncertainty avoidance* (comfort with ambiguity); later *long-term orientation* and *indulgence*.

**Time:** **monochronic** cultures treat time as a line (schedule, one task at a time, punctuality is respect); **polychronic** cultures treat it as flexible and relational (many things at once, relationships before schedules).

### Barriers in intercultural communication

- **Ethnocentrism:** judging other cultures by your own as the standard.
- **Stereotyping:** fixed ideas about a whole group ("all Westerners are rude").
- **Language and accent**, idioms and slang ("let us touch base"), humour that does not translate.
- **Non-verbal differences:** the head wobble, the thumbs-up, eye contact (a sign of honesty in the West, of disrespect to elders in some cultures), personal space, the use of the left hand, the meaning of silence.
- **Different attitudes** to hierarchy, time, deadlines, feedback and women at work.

::: example Worked example: one sentence, two readings
A Nepali developer is asked by an American manager, "Can you finish this by Friday?" Because saying "no" to a senior is impolite, he replies, "I will try." The manager hears a **yes** (low-context: words carry the meaning). On Friday the work is not ready and both are upset. **Fix:** the manager asks open questions ("What might stop you?"), the developer says, "I can finish the login page by Friday and the reports by Tuesday." Both state expectations explicitly and write them in the ticket.
:::

### Practical rules for intercultural competence

1. **Learn before you meet:** read about the country, holidays, greeting customs and business hours.
2. **Use plain English:** short sentences, no idioms, define acronyms, speak slowly (not loudly).
3. **Check understanding:** ask the other person to restate the plan; do not ask "Do you understand?", which invites a polite "yes".
4. **Confirm in writing** after a call: dates, owner, deliverable.
5. **Be patient with silence and accent;** do not finish sentences for others.
6. **Avoid stereotypes:** treat each person as an individual first.
7. **Respect holidays and time zones:** schedule meetings at an hour fair to both sides; share the inconvenience.
8. **Adapt, do not abandon:** respect the other culture while staying true to your own values; seek a "third culture" that works for the team.

## 4.4 Effective communication in teams

A **group** is a collection of people; a **team** is a small group with a common goal, complementary skills, shared accountability and interdependent work. In a team the quality of communication decides the quality of results, because teams succeed or fail at hand-offs: design to code, code to test, test to client.

### Group communication networks

| Network | Shape | Speed | Accuracy | Morale | Best for |
|---|---|---|---|---|---|
| **Chain** | A → B → C → D | slow at the ends | distorted | low at ends | formal hierarchy |
| **Wheel (star)** | all through the leader | fast for simple tasks | high | low except for the leader | routine tasks, emergencies |
| **Circle** | each speaks to two neighbours | slow | low | moderate | social groups |
| **All-channel (web)** | everyone to everyone | slower to decide, fast to share | high on complex tasks | highest | creative, complex work |

The number of **possible pairs** in a team of n people is **n(n - 1)/2**: 3 people have 3 channels, 5 have 10, 9 have 36, 20 have 190. Large teams therefore need structure: roles, stand-ups, written decisions and a shared board.

### Stages of team development (Tuckman)

**Forming** (polite, unsure) → **storming** (conflict about roles and methods) → **norming** (rules and trust form) → **performing** (high productivity) → **adjourning** (project ends). Leaders help teams pass through storming by naming it as normal and agreeing on working rules.

```svgfig label="4.3" caption="Tuckman's five stages of team development. The leader's style should change with the stage: direct in forming, coaching in storming, facilitating in norming, delegating in performing and recognising in adjourning."
f = Fig(760, 270)
st = [("Forming", "polite, unsure,\nrely on leader", "Direct", 80), ("Storming", "conflict over roles\nand methods", "Coach", 105), ("Norming", "rules agreed,\ncohesion grows", "Facilitate", 130),
      ("Performing", "high trust,\nresults flow", "Delegate", 155), ("Adjourning", "work ends,\nmixed feelings", "Recognise", 105)]
for i, (a, b, c, h) in enumerate(st):
    x = 10 + i * 150
    f.box(x, 215 - h, 140, h, "", fill=[BLUE, ROSE, MINT, SAND, SOFT][i], stroke=NAVY)
    f.text(x + 70, 215 - h + 20, a, size=12.5, color=NAVY, bold=True)
    for k, ln in enumerate(b.split("\n")): f.text(x + 70, 215 - h + 42 + k * 14, ln, size=10, color=SLATE)
    f.text(x + 70, 238, "Leader: " + c, size=10.5, color=TEAL, bold=True)
f.arrow([(30, 36), (640, 36)], color=AMBER, sw=2)
f.text(30, 22, "productivity and cohesion rise with each stage (adjourning is the planned end)", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(380, 262, "A new member or a new goal can send the team back to an earlier stage.", size=10, color=SLATE)
```

### Communication practices that make teams effective

- **A shared goal and definition of done**, written where everyone can see it.
- **A single source of truth** (a task board, a shared repository, a project wiki), not private chats.
- **Regular, short meetings:** a daily stand-up (yesterday, today, blockers) and a sprint review.
- **Meeting discipline:** agenda, time-keeper, notes, actions with owners and dates (see 2.3).
- **Respectful discussion norms:** one speaker at a time, ideas criticised, not people, decisions recorded.
- **Psychological safety:** members can admit mistakes and ask questions without ridicule. Google's Project Aristotle found it the strongest predictor of team effectiveness.
- **Constructive feedback** (SBI) and a retrospective after each milestone.
- **Documentation:** README, decisions log and meeting minutes, so knowledge does not live only in one head.

### The rise of virtual teams

A **virtual team** works across locations, and often time zones, mainly through technology. Reasons for their rise: broadband and cloud tools; global hiring; freelancing and outsourcing (a major export of Nepal's IT sector); the pandemic years (2020 to 2022), which made remote work normal; lower office costs; access to talent anywhere.

| Advantages | Challenges |
|---|---|
| wider talent pool and 24-hour work cycles | loss of non-verbal cues; messages read as cold |
| savings on travel and office space | time-zone gaps and slow answers |
| flexible hours; no commute | low trust and feelings of isolation |
| written records of decisions | tool overload; unreliable power and internet |
| inclusion of people who cannot relocate | cultural and language misunderstandings |

**Best practices for virtual teams:** hold regular video meetings, with cameras on where bandwidth permits; define **core overlap hours**; prefer **asynchronous** updates (written status notes) so people in other time zones are not blocked; state response-time expectations (for example, "within one working day"); use one tool per purpose (chat for quick questions, a board for tasks, a repository for code, a wiki for decisions); begin calls with a short personal check-in; rotate unfriendly meeting times; send agendas in advance and notes afterwards; celebrate wins online; and meet in person when possible.

```svgfig label="4.4" caption="Four communication networks in a team of five. Chain and wheel are centralised and fast for simple tasks but depend on one person; circle and all-channel suit complex problems and give the highest morale, at the cost of speed and more messages."
import math
f = Fig(760, 290)
def node(x, y, t=""): f.circle(x, y, 12, fill=BLUE, stroke=NAVY, sw=1.4, label=t, size=9)
def ring(cx, cy, r, n=5): return [(cx + r * math.cos(-math.pi / 2 + 2 * math.pi * k / n), cy + r * math.sin(-math.pi / 2 + 2 * math.pi * k / n)) for k in range(n)]
cx = [100, 290, 480, 670]
pts = [(cx[0] - 60 + 30 * k, 120) for k in range(5)]
for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=SLATE, sw=1.6)
for p in pts: node(*p)
c = (cx[1], 120); outer = ring(c[0], c[1], 62, 4)
for p in outer: f.line(c[0], c[1], p[0], p[1], color=SLATE, sw=1.6)
node(*c, "L")
for p in outer: node(*p)
pr = ring(cx[2], 120, 62)
for k in range(5): f.line(pr[k][0], pr[k][1], pr[(k + 1) % 5][0], pr[(k + 1) % 5][1], color=SLATE, sw=1.6)
for p in pr: node(*p)
pa = ring(cx[3], 120, 62)
for i in range(5):
    for j in range(i + 1, 5): f.line(pa[i][0], pa[i][1], pa[j][0], pa[j][1], color=SLATE, sw=1.2)
for p in pa: node(*p)
caps = [("Chain", "follows the hierarchy\nslow, message distorts"), ("Wheel", "all via the leader (L)\nfast, low morale"), ("Circle", "talk to neighbours only\nmoderate speed"), ("All-channel", "everyone talks to all\nslow but highest morale")]
for x, (a, b) in zip(cx, caps):
    f.text(x, 220, a, size=12.5, color=NAVY, bold=True)
    for k, ln in enumerate(b.split("\n")): f.text(x, 240 + k * 15, ln, size=10, color=SLATE)
```

## 4.5 Defining successful teams

A successful team **achieves its goal on time and with quality, stays healthy** (members learn and want to continue), and **improves its own working method**. Eight characteristics are usually named:

1. **A shared, clear goal** that every member can state in one sentence.
2. **Clear roles and ownership:** each task has one owner.
3. **Open and honest communication,** especially early reporting of problems.
4. **Mutual trust and respect,** including for differences of language, gender and background.
5. **Constructive handling of conflict:** about the problem, not the person.
6. **Shared responsibility and accountability:** success and failure are shared.
7. **Regular meetings and feedback:** short, focused and followed by actions.
8. **Complementary skills:** leader, idea generator, finisher and specialist; members cover each other's weak points.

Team roles (Belbin) include **coordinator, shaper, plant (ideas), monitor-evaluator, implementer, completer-finisher, resource investigator, team worker and specialist**. A team of nine "shapers" fights; a team of nine "plants" never finishes.

```svgfig label="4.1" caption="Communication channels grow much faster than team size. The number of possible pairs is n(n-1)/2: a team of 9 has 36 channels, a team of 18 has 153 (4.25 times more). This is why larger teams need roles, stand-ups and a shared task board."
ns = [3, 5, 9, 12, 20]
ch = [n * (n - 1) // 2 for n in ns]
assert ch == [3, 10, 36, 66, 190]
f = Fig(560, 270)
f.text(280, 20, "possible communication pairs in a team of n people", size=12, color=NAVY, bold=True)
base, sc = 210, 150 / 190
for i, (n, c) in enumerate(zip(ns, ch)):
    x = 40 + i * 100
    h = c * sc
    f.box(x, base - h, 70, max(h, 2), "", fill=BLUE if n != 9 else AMBER, stroke=NAVY)
    f.text(x + 35, base - h - 9, str(c), size=12, color=NAVY, bold=True)
    f.text(x + 35, base + 16, "n = " + str(n), size=11, color=SLATE)
f.line(30, base, 540, base, color=SLATE, sw=1.4)
f.text(280, 252, "n = number of people; each pair is one channel", size=10.5, color=TEAL, bold=True)
```

## 4.6 Leadership and communication

A **leader** influences others to work towards a goal. A **manager** plans, organises and controls resources; a leader inspires direction. In a small IT team the same person is often both. Leadership is largely a communication skill: a leader's main tools are talking, listening, writing and example.

### Leadership styles

| Style | How decisions are made | Communication pattern | Suits |
|---|---|---|---|
| **Autocratic (authoritarian)** | leader alone | one-way orders | emergencies, inexperienced staff |
| **Democratic (participative)** | after consultation | two-way discussion | creative work, skilled teams |
| **Laissez-faire** | the team | little guidance | expert, self-motivated people |
| **Transformational** | shared vision, inspiring | vision, stories, high expectations | change and innovation |
| **Servant** | leader serves the team's needs | listening, coaching | knowledge teams, retention |

Kurt Lewin identified the first three; there is no single "best" style. **Situational leadership** (Hersey and Blanchard) says that the leader should adapt: direct a new member, coach a learning one, support a capable one, delegate to an expert.

### What leaders must communicate

- **Vision and purpose:** why the project matters, in a sentence people can repeat.
- **Expectations:** deliverables, quality standards, dates.
- **Feedback and recognition:** praise in public (specific and sincere), correct in private.
- **Context:** the reasons behind decisions, so that instructions are not "because I said so".
- **Bad news, early:** projects survive late-but-honest news better than hidden news.
- **Change:** what is changing, why, what stays the same and what happens next.

### Communication skills of effective leaders

Listening first; asking questions instead of only giving answers; speaking simply and consistently (words and actions must match); transparency about what is not yet known; empathy for stress and personal issues; and *credibility*, which comes from competence, honesty and keeping promises.

::: example Worked example: announcing a delay
*Poor:* "The release is delayed. Work harder." *Better:* "We will miss Friday by one week because the payment gateway changed its API. Here is the new plan: Monday to Wednesday, integrate; Thursday, test; the next Tuesday, release. I need two volunteers for testing and I will tell the client today. If you see another risk, tell me today, not on release day."
The better version gives the reason, the new plan, the request for help, and an action by the leader.
:::

### Adapting communication styles for diverse audiences

Good communicators change style, not substance, to suit the audience. The question before every message is: **Who is the receiver, what do they already know, what do they need to do, and how do they like to receive information?**

| Audience | What it needs | How to adapt |
|---|---|---|
| **Technical experts** (developers, engineers) | detail, evidence, precision | use exact terms, data, diagrams, code and references |
| **Non-technical** (managers, clients, users) | benefits, risks, cost, time | analogies, plain words, visuals, no jargon; start with the result |
| **Senior executives** | the decision required | one-page summary: bottom line, options, recommendation |
| **Seniors and elders** | respect and clarity | polite address, patient pace, face-to-face where possible |
| **Different generations** | preferred channel | email or phone for some, instant chat for others |
| **Non-native speakers** | simple language | short sentences, written follow-up, avoid idioms |
| **People with disabilities** | accessible formats | captions, alt text, large type, screen-reader-friendly files |
| **Cross-cultural** | cultural fit | see 4.3: context, hierarchy, time, formality |

### Four common communication styles

1. **Passive:** avoids conflict, hides needs; leads to resentment.
2. **Aggressive:** wins at others' expense; leads to fear.
3. **Passive-aggressive:** indirect hostility (sarcasm, silent treatment).
4. **Assertive:** clear, honest, respectful: "I disagree with this schedule because testing is missing; can we move the release by two days?"

The **DISC** model (dominance, influence, steadiness, conscientiousness) describes preferences: a "D" colleague wants the bottom line fast; a "C" colleague wants accuracy and detail; an "S" colleague wants stability and time to adjust; an "I" colleague wants conversation and enthusiasm. Use such models as a prompt for flexibility, not as labels for people.

::: example Worked example: one fact, three audiences
*Fact:* a database index will cut the report time from 40 s to 2 s.
*To the developer:* "Adding a composite index on (customer_id, date) reduces the full table scan to an index range scan; the report goes from 40 s to 2 s on 5 million rows."
*To the manager:* "A small change (half a day) will make the monthly report 20 times faster, so staff stop waiting."
*To the client:* "Your monthly report will open in two seconds instead of forty."
The fact is identical; the vocabulary, detail and benefit change.
:::

## Exercise (Sections 4.1 to 4.6)

1. Define interpersonal communication. List four of its features.
2. What is the Johari Window? Explain with a workplace example.
3. Differentiate between hearing and listening. Name the stages of listening.
4. What is a listening environment? List four factors that damage it and four ways to improve it.
5. What is meant by high-context and low-context cultures? Give an example of a misunderstanding.
6. Write short notes on: (a) ethnocentrism, (b) monochronic and polychronic time, (c) power distance.
7. What are virtual teams? Discuss their advantages and challenges.
8. Explain the features of a successful team.
9. Compare autocratic, democratic and laissez-faire leadership with an example for each.
10. How should a project manager change the way he explains a delay to (a) a client, (b) a developer, (c) the college principal?
11. Long answer: "Communication, not technology, decides whether a software team succeeds." Discuss with reference to the content of this unit.

::: note Answers and worked solutions
**1.** Interpersonal communication is the two-way exchange of verbal and non-verbal messages between people who influence each other and build a relationship. Features: two-way and immediate feedback; personal and relational (content plus relationship message); uses many channels; irreversible; depends on context.
**2.** A model of Luft and Ingham (1955) with four areas: open, blind, hidden and unknown. Disclosure shrinks the hidden area and feedback shrinks the blind spot, so the open area grows and trust increases. Example: a new team member says what she is good and weak at, and asks for review of her SQL.
**3.** Hearing is physical reception of sound; listening is the active process of attending, understanding, evaluating and responding. Stages: receiving, attending, understanding, evaluating, responding, remembering.
**4.** It is the physical, social and organisational setting for listening. Damaging factors: noise, phones and notifications, overloaded meetings without agenda, a culture that punishes bad news, jargon. Improvements: quiet room, agenda and time limit, phones away, paraphrasing, inviting quiet members, circulating notes.
**5.** In high-context cultures meaning lies in the situation and what is unsaid (indirect "no"); in low-context cultures meaning is in the explicit words. A Nepali developer says "I will try" meaning "no" and a US manager hears "yes".
**6.** (a) Judging other cultures by the standards of one's own. (b) Monochronic: time is a line with strict schedules; polychronic: time is flexible, many things at once, relationships first. (c) The extent to which less powerful members accept unequal power; high in Nepal, so juniors seldom contradict seniors openly.
**7.** Teams that work across places and time zones mainly through technology. Advantages: wider talent, round-the-clock work, savings, flexibility. Challenges: weak non-verbal cues, time zones, trust and isolation, tool overload, unreliable internet and power.
**8.** Clear shared goal; clear roles; open communication; trust and respect; constructive conflict handling; shared accountability; regular meetings and feedback; complementary skills.
**9.** Autocratic: leader decides alone, one-way orders, for emergencies (a fire drill). Democratic: decision after consultation (choosing a framework for a project). Laissez-faire: team decides with little guidance (senior researchers in a lab).
**10.** (a) Client: the new date, the reason in plain words, what is being done, no jargon. (b) Developer: the technical cause, revised tasks and owners. (c) Principal: one short paragraph with the impact on the programme, the new date and what support is needed.
**11.** Introduction: tools only carry messages. Body: (i) interpersonal skills and listening prevent misunderstanding; (ii) intercultural awareness avoids silent "yes" problems in global teams; (iii) virtual teams need explicit rules, overlap hours and written records; (iv) leaders must give a vision, feedback and early bad news; (v) the 8 characteristics of success are all communication habits. Conclusion: the best tools fail in a team that does not listen, and a good team succeeds even with simple tools.
:::

## 4.7 Vocabulary and grammar

The textbook's own list for this section is not reproduced here. This book teaches vocabulary and grammar that you need for the unit: words for people, teams and cultures (4.7.1) and the modal verbs and conditionals used for suggestions, requests and negotiation (4.7.2).

### 4.7.1 Vocabulary of interpersonal and group communication

| Word | Meaning | Example |
|---|---|---|
| **rapport** | friendly, trusting relationship | She quickly built rapport with the client. |
| **empathy** | ability to understand others' feelings | A leader needs empathy, not only authority. |
| **consensus** | general agreement | The team reached a consensus on the framework. |
| **collaborate** | work together on something | Three groups collaborated on the app. |
| **delegate** | give a task to someone else | The manager delegated testing to Sita. |
| **mediate** | help two sides to settle a dispute | The coordinator mediated between the groups. |
| **accountable** | responsible for results | Every owner is accountable for the ticket. |
| **cohesive** | united, sticking together | A cohesive team survives pressure. |
| **stereotype** | fixed, oversimplified idea of a group | Do not apply stereotypes to colleagues. |
| **assertive** | confident and respectful | An assertive reply states needs clearly. |
| **feedback** | information about performance | Give feedback within a day. |
| **bias** | unfair preference or prejudice | Check your own bias before judging. |
| **inclusive** | open to all kinds of people | Use inclusive language in a diverse team. |
| **synchronous / asynchronous** | at the same time / at different times | Email is asynchronous; a call is synchronous. |

**Phrasal verbs for the workplace.** *follow up* (check later), *carry out* (perform), *bring up* (mention a topic), *back up* (support or copy data), *sort out* (resolve), *look into* (investigate), *take over* (assume control), *hand over* (transfer), *come up with* (invent), *put off* (postpone), *call off* (cancel), *get across* (make understood), *speak up* (talk more loudly or openly), *step down* (resign from a post).

**Collocations:** build rapport, reach a consensus, meet a deadline, give feedback, resolve a conflict, set a goal, hold a meeting, make a decision, pay attention, raise a concern.

### Exercise 4.7.1

1. Fill in the blanks with a word from the table: (a) The two departments reached a ______ after a long meeting. (b) A good manager does not do everything but ______ tasks. (c) A ______ team does not break under pressure. (d) A neutral colleague agreed to ______ between the two developers.
2. Choose the correct phrasal verb: The meeting was (called off / called up) because of the strike.
3. Replace the underlined words with a phrasal verb: "We must *investigate* the complaint and *resolve* it before Friday."
4. Write two sentences using *rapport* and *inclusive*.

::: note Answers and worked solutions
**1.** (a) consensus (b) delegates (c) cohesive (d) mediate.
**2.** called off (cancelled).
**3.** "We must look into the complaint and sort it out before Friday."
**4.** *Sample:* The trainer built rapport by learning every student's name. The college uses inclusive language in its notices.
:::

### 4.7.2 Modals and conditionals in suggestions, requests and negotiation

**Polite requests and suggestions** use modal verbs. From more direct to more polite: *Send me the file.* → *Can you send me the file?* → *Could you send me the file?* → *Would you mind sending me the file?* → *I was wondering if you could send me the file.* Suggestions: *You could ask the supervisor.* *We should test again.* *Why don't we meet on Monday?* *Shall we begin?*

**Obligation and advice:** must (strong, personal), have to (external rule), should and ought to (advice), need to, had better (warning).
**Ability and permission:** can/could; may/might for formal permission (May I leave early?).
**Possibility:** may, might, could, can't (impossibility), must (strong deduction): *She must be in a meeting; her phone is off.*

**Conditionals** (used in negotiation, planning and advice).

| Type | Form | Use | Example |
|---|---|---|---|
| **Zero** | if + present, present | general truths | If a server overheats, it shuts down. |
| **First** | if + present, will + base verb | real, likely future | If you finish by Friday, we will release on Monday. |
| **Second** | if + past, would + base verb | unreal or unlikely present/future | If we had more time, we would add a search page. |
| **Third** | if + past perfect, would have + past participle | unreal past | If we had tested, the demo would not have crashed. |

In formal English use *were* for all persons in the second conditional (*If I were you, I would call the client*). **Negotiation phrases:** *If you can offer a discount, we would consider a bigger order.* *Unless we get a reply today, we will cancel the booking.* (unless = if not).

### Exercise 4.7.2

1. Make this request more polite: "Give me the report."
2. Complete: (a) If it rains, the match ______ (be) postponed. (b) If I ______ (be) the manager, I would hire two more testers. (c) If she had backed up the data, she ______ (not lose) it.
3. Choose the best modal: "You (must / might) be tired after the flight." (deduction)
4. Combine using *unless*: "We will not release if the tests do not pass."
5. Correct the sentence: "If I would have time, I would help you."

::: note Answers and worked solutions
**1.** "Could you please send me the report?" or "Would you mind giving me the report?"
**2.** (a) will be (first conditional) (b) were (c) would not have lost.
**3.** must.
**4.** "We will not release unless the tests pass."
**5.** "If I had time, I would help you." (do not use *would* in the if-clause)
:::

## 4.8 Readings

*Reading note.* The two texts below are prescribed in the textbook. This book does not reprint them; it gives a detailed summary, the argument or structure, themes, critical analysis, rhetorical notes, vocabulary and solved exercises. Read the original in your textbook first, and check names and figures against your copy before using them in an answer.

### 4.8.1 "Computer and the Pursuit of Happiness" by David Gelernter

#### The writer and the text

**David Gelernter** (born 1955) is an American professor of computer science at Yale University, a pioneer of parallel computing (the *Linda* coordination language) and a writer on technology and culture. His essay "Computers and the Pursuit of Happiness" first appeared in *Commentary* magazine (January 2001), at the height of the dot-com boom, when politicians and journalists were announcing that the Internet had begun a "new information age". It is an **argumentative essay** and a good example of a **sceptic's case written by an insider**: a computer scientist asks whether computers have really made people happier.

#### Summary

Gelernter organises the essay around **three questions**:

1. **Are we living in a new "Information Age"?** He says **no**. People who say yes make three claims: we have new machines that create, store and deliver information; networks have defeated geography; and these machines are intelligent. He answers each in turn.
   - *Information machines are not new.* The twentieth century was already one information-gusher after another: movies, the phonograph, colour photography, radio and radio networks, newsreels, television, transistor electronics, long-distance telephone, satellites. Computers are the latest, not the first. He compares this to **faucets stuck open**, with information pouring into lives.
   - *Distance was conquered earlier.* Railways, the telegraph, the telephone, highways, aeroplanes and broadcasting had already shrunk geography; the Internet continues a long line.
   - *Intelligent machines are not new either:* thermostats, electrical systems in cars and similar devices already acted "intelligently".
   He argues that our basic needs have **not** moved from physical to informational: we still need food, clothing, shelter, **and one another**. "Virtual" gourmet food does not keep you from starving; we still depend on coal, steel and concrete. He concedes that computers have **revolutionised science and engineering**, where models are cheaper than experiments, but this is a narrower change.
2. **Have computers been good for people over the last fifty years?** Poor and ignorant people need wealth and information, so computers help while people are climbing out of poverty and ignorance. But once the basic threshold is passed, more wealth and information add **little to happiness**. He shows that modern life is more convenient, yet he doubts that it is happier: children enjoyed toys before computers, and he and his wife were happy in childhoods without them. He adds the **plumbing analogy**: indoor plumbing was a clear convenience, but it ended the daily gathering at the village well. Each technology gives something and takes away a **human ingredient**, replaced by a **machine ingredient** (a shop where you meet people replaced by a website). He worries that new social structures built on machines may be worse than the old ones built on people.
3. **Will computers help people in the next fifty years?** He is cautious, even hopeful. He expects the greatest change in **education**: online software could be a "world-spanning switchboard" matching the right student with the right teacher. But he prefers **face-to-face teaching** and says that schools must also form character, not only transfer information. Looking to 2050, he hopes computers will make people see more clearly what is **unique in humans**: that humans are not machines and that qualities such as morality, humour and holiness cannot be computed. In the end, a computer may help us to understand ourselves better.

His central conclusion: **computers and the Internet are important, but not revolutionary in the way their promoters claim; they will have little to do with human happiness unless we use them to strengthen real human bonds.** The three ages he names: the **solid** age of agriculture, the **liquid** age of industry and the **gaseous** age of information, a metaphor showing that information flows everywhere but has no body.

*Check your textbook copy.* Some editions print a short letter to the editor responding to Gelernter after the essay; if yours does, read it as a counter-argument and use it in "discuss" answers.

#### Themes

- **Technology versus happiness.** Convenience, wealth and information do not automatically give happiness.
- **Continuity, not revolution.** New machines continue old patterns; hype exaggerates novelty.
- **Human ingredient.** Social life, shopping, teaching and play have value because people are present.
- **Education.** Technology can widen access; character, trust and moral development need people.
- **Responsibility of the technologist.** The writer is a computer scientist warning his own field to be humble.

#### Critical analysis and rhetorical notes

- **Structure.** Three numbered questions; each is answered directly (no, not much, maybe). This is a model of clear argumentative organisation.
- **Ethos.** A Yale computer scientist speaking against exaggeration gains credibility: "he knows the machine and still doubts it".
- **Logos.** Historical comparison (twentieth-century information media; railways before the Internet), the distinction between needs and wants, and the cost-benefit logic of poverty thresholds.
- **Pathos and personal examples.** His own childhood and his wife's, children's toys, the village well and the shop; they make the abstract claim human.
- **Figurative language.** Stuck-open faucets; the solid, liquid and gaseous ages; plumbing replacing the well; "virtual" food that cannot feed.
- **Tone.** Calm, ironic, confident; it deflates hype without anger.
- **Critique.** Gelernter wrote in 2001, before smartphones, social networks, cloud services and generative AI. Critics could say that he underrates the way the Internet has changed access to education and health for poor and remote communities (for example, students in rural Nepal with online lectures), and that "happiness" is hard to measure. A balanced answer gives his argument first, then these limits.
- **Link to professional communication.** Technology is a means; the goal of professional communication is human understanding. Use tools to support relationships, not to replace them.

#### Key vocabulary

*revolutionary, information age, sceptic, geography, surrogate, convenience, threshold, structure, tangible, gaseous, unique, moral.*

### Exercise: "Computer and the Pursuit of Happiness"

1. What three questions does Gelernter raise?
2. Why does he say that we are not living in a new information age?
3. What does he mean by saying that computers have not changed human needs?
4. Explain the analogy of plumbing and the village well.
5. What does he expect from computers in education? Why does he prefer face-to-face teaching?
6. What is his conclusion about computers and happiness?
7. Long answer: "Computers and the Internet have made humans no happier." Do you agree with Gelernter? Give reasons with examples from your own life.
8. Write a paragraph on the rhetorical devices Gelernter uses.

::: note Answers and worked solutions
**1.** (i) Are we living in a new information age? (ii) Have computers been good for people in the last fifty years? (iii) Will computers be good for people in the next fifty years?
**2.** Because information machines (radio, television, telephone, film) filled the whole twentieth century; distance had already been conquered by railways and telegraph; intelligent machines such as thermostats existed before computers. Computers are the latest in a long line.
**3.** People still need food, clothing, shelter and one another. We eat bread, not data; virtual food does not stop hunger. Information is needed by the poor and ignorant, but once that need is satisfied it adds little to well-being.
**4.** Plumbing brought clean water to the home (convenience) but ended the gathering at the village well (a social meeting). Likewise the Internet makes tasks easy but removes human contact: a machine ingredient replaces a human ingredient.
**5.** He expects software that connects the right student to the right teacher across the world and cheap access to knowledge. He prefers face-to-face teaching because a teacher also builds character and trust, which a screen cannot.
**6.** Computers and the Internet are useful, especially in science and engineering, but they are not revolutionary and do not make people happier; the real task is to use them to make us understand what is human.
**7.** *Model plan.* Introduction: state the claim. For Gelernter: children and adults were happy before computers; happiness depends on relationships; time spent on screens reduces face-to-face contact; wealth and information stop adding happiness after basic needs. Against: online learning, telemedicine, remittance apps and video calls help Nepali families separated by migration; access to information lifts people from poverty and ignorance, where Gelernter himself says it helps. Own experience: concrete example. Conclusion: technology helps happiness when it serves relationships and basic needs, not when it replaces them.
**8.** Gelernter uses direct questions as structure; historical comparison (twentieth-century media, railways); analogy (plumbing and the well); metaphor (stuck-open faucets; gaseous age); personal example (his children and wife); and a calm ironic tone. Together they make a complex argument clear and memorable.
:::

### 4.8.2 "The Collapse of the Family and the Community" by Yuval Noah Harari

#### The writer and the text

**Yuval Noah Harari** (born 1976) is an Israeli historian at the Hebrew University of Jerusalem. His books *Sapiens: A Brief History of Humankind* (Hebrew 2011, English 2014), *Homo Deus* and *21 Lessons for the 21st Century* made him a leading public thinker on history and technology. "The Collapse of the Family and the Community" is a section of the chapter **"A Permanent Revolution"** in *Sapiens*. It is an **expository and analytical essay** that asks a big question: what happened to the oldest human institutions when states and markets grew powerful?

#### Summary

1. **The old world.** Before the Industrial Revolution, people's lives passed in three ancient frames: the **nuclear family**, the **extended family** and the **local intimate community** (a group of people who know one another well and depend on each other for survival). Most people worked in the family farm or workshop, or in the neighbours'. If an illness was too grave, an investment too large, or a quarrel turned violent, the **community** helped, by local custom and an **economy of favours**, not by market supply and demand.
2. **A cost, too.** Harari does not romanticise the past: families and communities could **oppress their members as brutally as modern states and markets**, and they were full of tension and violence. But people had **no choice**: someone who lost family and community around 1750 was **as good as dead**, with no job, education, support in sickness, loan, or protection. There were no policemen, social workers or compulsory schools.
3. **The market and state move in.** At first the market and the state found their path blocked by families and communities that disliked outside intervention. Parents and elders resisted letting youngsters be indoctrinated by nationalist education, conscripted or turned into a rootless urban proletariat. Over time the state and the market used growing power to weaken traditional bonds: the **state sent policemen to stop family vendettas** and replaced them with court decisions; youngsters are increasingly excused from obeying elders, while **parents are blamed** for anything that goes wrong in a child's life. He compares parents in the "Freudian courtroom" to defendants in a Stalinist show trial.
4. **Courting and money, then and now.** He gives a vivid picture: earlier, bride and groom met in the family living room and money passed from the hands of one father to another; today courting happens in bars and cafés and money passes to waitresses and, in larger amounts, to fashion designers, gym managers, dieticians, cosmeticians and plastic surgeons who help us look like the market's ideal.
5. **Imagined communities.** People still need belonging, so states and markets provide **imagined communities**: communities of people who do not really know one another but imagine that they do. The two most important are **the nation** (the imagined community of the state) and **the consumer tribe** (the imagined community of the market). These are not new: in ancient China tens of millions saw themselves as one family with the emperor as father; medieval Muslims imagined themselves brothers and sisters in the community of Islam. But in the past imagined communities played "second fiddle" to intimate communities of several dozen people. **In the last two centuries the intimate communities have withered, leaving imagined communities to fill the emotional vacuum.**
6. **Conclusion.** Social revolutions were once rare and slow; people believed that "this is how it always was and always will be". Now history has still not decided where we will end up, and "a string of coincidences might yet send us rolling in either direction".

#### Themes

- **Individual liberty versus belonging.** The individual is freed from oppressive elders but is left alone before the state and market.
- **Replacement of institutions.** Services once provided by kin (care, credit, protection, education) are provided by the state and market.
- **Imagined communities.** The idea draws on Benedict Anderson's concept; nation and brand can supply identity, but at a distance.
- **Loss and gain.** The essay is balanced: it shows the cruelty of the old order and the loneliness of the new.
- **Link to digital life.** Online groups, fan clubs and social networks are new "imagined communities", important for Unit 5.

#### Critical analysis and rhetorical notes

- **Style.** Short clear sentences, vivid images (living room versus café) and **memorable paradoxes** ("as good as dead").
- **Comparison and contrast** between the old and the new is the basic structure; **cause and effect** explains how states and markets took over.
- **Irony and hyperbole.** The "Freudian courtroom" and "Stalinist show trial" comparison is intentionally exaggerated to make a point about blaming parents.
- **Definition.** The footnote defining "intimate community" and the definition of "imagined community" make a complex idea easy to follow.
- **Balance and caution.** The closing passage does not predict the future; it says the outcome is open.
- **Possible critique.** The essay generalises across continents and centuries; in Nepal, joint families, caste and village communities remain strong in many places, while migration for work abroad is weakening them quickly. Its picture is clearer as a model than as an exact history.
- **Link to professional communication.** Workplaces are now "communities" for many people; teams, culture and trust matter because families are smaller and people move.

#### Key vocabulary

*collapse, intimate community, extended family, economy of favours, vendetta, indoctrinate, conscript, proletariat, imagined community, consumer tribe, alienated, vacuum.*

### Exercise: "The Collapse of the Family and the Community"

1. What three frames did human life revolve around before the Industrial Revolution?
2. According to Harari, why did people "have little choice" about staying in family and community?
3. How did the state weaken the family and the community?
4. What is an imagined community? Give the two examples named in the text.
5. What does Harari mean by "the emotional vacuum"?
6. Explain the comparison between parents and defendants in a Stalinist show trial.
7. Long answer: Do you think a nation or a brand community can replace the family and village? Discuss with reference to Nepali society.
8. Write a note on Harari's style in this essay.

::: note Answers and worked solutions
**1.** The nuclear family, the extended family and the local intimate community.
**2.** Because the family and community gave work, education, care in illness, credit and protection. A person who lost them around 1750 was as good as dead; there were no policemen, social workers or schools to replace them.
**3.** It sent policemen to stop vendettas and replaced them with courts; it set up compulsory schools and armies that took the young from elders' control; it protected young people against elders and blamed parents for children's problems.
**4.** A community of people who do not know one another but imagine that they do. The nation (of the state) and the consumer tribe (of the market).
**5.** As intimate communities withered, people lost the emotional support and sense of belonging they gave; imagined communities such as nations and brands fill that empty space.
**6.** In the Freudian view parents are blamed for the psychological problems of a child, so they have little hope of an acquittal, as accused persons in a Stalinist show trial had none. The comparison is exaggerated for effect.
**7.** *Model plan.* Introduction: Harari says these communities fill an emotional vacuum. Yes: nationalism, fan groups and online groups give identity; shared festivals such as Dashain and Tihar, and the diaspora's online groups, link strangers. No: they cannot provide direct help in sickness or old age, or the trust of people who know us; remittance-based families in Nepal still need real relatives; consumer tribes sell products and may exploit loneliness. Conclusion: imagined communities supplement, but do not replace, intimate ones.
**8.** Clear short sentences; concrete images (living room versus café); definition and footnote; contrast between old and new; paradox and irony; a balanced, open conclusion.
:::


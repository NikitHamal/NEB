---
subject: Professional Communication and Ethics
grade: BCA Semester 1
unit: 2
title: Listening, Speaking and Presentation Skills
area: BCA 105 · Professional Communication and Ethics · Unit 2
---

Technical skill gets you shortlisted; speaking and listening get you hired, promoted and understood. This unit covers active listening, clear speaking, presentations with slides, group discussion and interviews.

::: key What this unit gives you
- Hearing versus listening; types of listening; active listening techniques.
- Speaking clearly: structure, voice, body language, handling nerves.
- Planning, designing and delivering a presentation, including slide rules and Q&A.
- Group discussion and job interview technique with sample answers.
:::

## 2.1 Listening

**Hearing** is physical; **listening** is mental effort to understand. We speak at roughly 125 to 150 words per minute but can think at much higher speeds, so attention wanders unless we work at it.

| Type | Purpose | Example |
|---|---|---|
| Appreciative | enjoyment | music, a speech |
| Informational | learn | a lecture, a briefing |
| Critical | evaluate | a sales pitch, a project proposal |
| Empathic | understand feelings | a colleague describing a problem |

**Barriers to listening:** distraction (phone), pre-judging the speaker, thinking about your reply while the other speaks, jargon, fatigue, noise.

**Active listening**

1. **Attend**: stop other tasks, face the speaker, make appropriate eye contact.
2. **Show you are listening**: nod, short responses ("I see").
3. **Do not interrupt**; let them finish.
4. **Paraphrase**: "So you mean the report is due on the 15th, not the 5th?"
5. **Ask open questions** ("What happened next?") and clarify closed facts ("Which server?").
6. **Take notes** on key points, numbers and actions.
7. **Summarise** and confirm next steps.

**Taking notes.** Use headings, short phrases, abbreviations of your own, and a margin column for action items. In a requirement meeting write: *who needs what, by when, how success is judged*.

## 2.2 Speaking clearly

**Structure.** Whatever the length, give the listener a map: **opening** (state the point), **body** (two or three supporting points with examples), **closing** (restate the point and the action). *PREP*: **P**oint, **R**eason, **E**xample, **P**oint again.

**Voice:** volume (be audible at the back), **pace** (about 120 to 150 words a minute; slow down for key points), **pitch and intonation** (avoid monotone), **pauses** (silence lets ideas land), **clear pronunciation** and no filler ("um", "like").

**Body language:** upright posture, open hands, eye contact in short bursts with different people, a natural smile where suitable, no pointing, no hiding behind arms or paper.

**Nerves.** Stage fright is normal, not a sign of failure. Prepare and rehearse aloud (twice at full length), arrive early and check the equipment, breathe slowly before starting, memorise your first sentence, and move purposefully rather than freezing.

**Telephone and video etiquette.** Greet and identify yourself ("Good morning, this is Sita Sharma from…"), speak slightly slower, take notes, repeat numbers and names back, end with a summary. On video calls: camera at eye level, mute when not speaking, look at the camera when you speak, and have a neutral background.

## 2.3 Presentations

**Plan with four questions:** *Who* is the audience (background, what they want)? *Why*: inform, persuade, train or report? *What* is the one key message? *How long* and in what setting?

**Structure** (for 10 minutes): introduction (1 min: hook, topic, outline) → body (7 min: 3 main points) → conclusion (1 min: summary and call to action) → questions (1 min or more).

**Slide design rules**

| Do | Avoid |
|---|---|
| one idea per slide | paragraphs of text |
| ≤ 6 lines, ≤ 6 words per line as a guide | reading the slide aloud |
| large font (≥ 24 pt body, ≥ 32 pt titles) | tiny fonts, cluttered diagrams |
| high contrast (dark on light, or white on dark) | red on green, busy backgrounds |
| a chart, diagram or screenshot for data | 3-D charts, pie with 10 slices |
| consistent template and a clear title | too many animations |

**Delivery:** speak to the audience, not the screen; use slides as prompts; tell a short story or give an example for each point; for a technical demo, rehearse the demo and keep a recorded backup in case the network fails.

**Handling questions:** listen to the whole question, repeat it, answer briefly, admit "I don't know; I will find out and email you" rather than bluffing, and move on if a questioner dominates.

**Feedback checklist** for a peer's talk: Was the message clear? Was the structure easy to follow? Did eye contact, voice and pace help? Were slides readable? Was the time kept? Were questions handled well?

```svgfig label="2.1" caption="Time plan for a 10-minute presentation. The bar is drawn to scale: a short hook and outline, three main points of about 2 minutes 20 seconds each, a summary with a call to action, and time for questions. Rehearse with a timer; talks that overrun lose the audience."
f = Fig(760, 190)
segs = [("Intro", 1, SAND, AMBER, "hook, topic,\noutline"), ("Point 1", 7 / 3, BLUE, NAVY, "claim +\nexample"), ("Point 2", 7 / 3, BLUE, NAVY, "claim +\nexample"), ("Point 3", 7 / 3, BLUE, NAVY, "claim +\nexample"), ("Close", 1, MINT, TEAL, "summary,\ncall to act"), ("Q&A", 1, ROSE, RED, "listen,\nrepeat, answer")]
x = 20; u = 72
for n, m, fl, st, d in segs:
    w = m * u
    f.box(x, 40, w, 56, n, fill=fl, stroke=st, size=11.5, bold=True)
    for i, ln in enumerate(d.split("\n")): f.text(x + w / 2, 116 + i * 13, ln, size=9, color=SLATE)
    x += w
f.line(20, 150, 740, 150, color=SLATE, sw=1.4)
for m in range(0, 11): f.line(20 + m * u, 146, 20 + m * u, 154, color=SLATE, sw=1.2); f.text(20 + m * u, 168, f"{m}", size=10, color=SLATE)
f.text(380, 184, "minutes", size=10, color=SLATE, italic=True); f.text(380, 22, "10-minute talk: 1 + 7 + 1 + 1", size=12, color=NAVY, bold=True)
```

```photogrid label="2.1" cols="2" ratio="1.45" caption="Delivery and slides. (a) A speaker at an international conference faces the audience and uses the microphone and open gestures; the slide behind him is only a prompt. (b) The same content as a poor slide (paragraph, tiny font) and a good slide (one idea, large type, a simple chart)."
@ photo id="bca105/speaker" cap="Speaker facing the audience"
fit 1.45
focus 0.78 0.5
call 0.45 0.90 0.74 0.62 "Open gestures"
call 0.42 0.08 0.62 0.40 "Microphone"
@ svg cap="Poor slide versus good slide"
f = Fig(420, 290)
f.box(8, 20, 190, 190, "", fill="#fff", stroke=RED, sw=2)
for i in range(11): f.line(18, 36 + i * 15, 188 - (i % 3) * 22, 36 + i * 15, color="#94a3b8", sw=2.2)
f.text(103, 232, "Poor: 11 lines, tiny font,", size=10, color=RED, bold=True); f.text(103, 246, "read aloud, red on green", size=10, color=RED, bold=True)
f.box(222, 20, 190, 190, "", fill="#fff", stroke=TEAL, sw=2)
f.text(317, 52, "Mobile payments", size=13, color=NAVY, bold=True)
for i, h in enumerate([40, 70, 105, 140]): f.box(246 + i * 38, 190 - h, 28, h, "", fill=BLUE, stroke=NAVY)
f.text(317, 202, "2021   2022   2023   2024", size=8.5, color=SLATE); f.text(317, 232, "Good: one idea, large title,", size=10, color=TEAL, bold=True); f.text(317, 246, "one chart, high contrast", size=10, color=TEAL, bold=True)
```

## 2.4 Group discussion and meetings

A **group discussion (GD)** is a structured conversation among 6 to 10 candidates on a topic, used in selection. Evaluators look at content, clarity, listening, leadership, teamwork and composure; they do *not* count who spoke loudest.

**Tips:** start with a short, relevant point if you know the topic; support claims with a fact or example; respect others ("I see your point, and I would add…"); bring a dominating member back politely; summarise at the end if given the chance; do not interrupt, shout or repeat.

**Meetings.** Before: set the purpose and agenda, invite only needed people, circulate documents. During: start on time, follow the agenda, give everyone a turn, record decisions and action items (*who does what by when*). After: send **minutes** within 24 hours. Roles: chair, secretary (minute-taker), timekeeper. (Writing agendas and minutes is covered in Unit 3.)

## 2.5 Job interviews

**Before:** research the organisation and the role; read the job advertisement and list how your skills match; prepare 3 to 4 stories from projects (use **STAR**: **S**ituation, **T**ask, **A**ction, **R**esult); prepare questions to ask; check documents; dress neatly; arrive 10 to 15 minutes early.

**During:** greet and shake hands (if appropriate), sit upright, listen to the full question, answer concisely (1 to 2 minutes), be honest, show enthusiasm, and never speak badly of a previous employer or teacher.

**Common questions with approach**

| Question | Approach |
|---|---|
| "Tell me about yourself." | 60 to 90 seconds: education, key skills or projects, why this role (present → past → future); not your life story |
| "Why should we hire you?" | match your strongest skills to their stated needs, with one proof |
| "What are your weaknesses?" | a real, minor weakness plus what you are doing about it |
| "Describe a time you solved a problem." | a STAR story with a measured result |
| "Where do you see yourself in five years?" | growth in skills and responsibility in this field, not "your job" |
| "Do you have any questions?" | always ask: team structure, learning opportunities, first-month expectations |

::: example Worked example: a STAR answer
*Question: Tell me about a time you worked in a team.* **Situation:** In my second-semester C project our group of four was behind schedule. **Task:** I was asked to finish the file-handling module in three days. **Action:** I split the work into read, write and search functions, tested each with sample data, and asked a teammate to review. **Result:** We merged on time and the project was marked 92 %.
:::

**After:** send a short thank-you email within a day (thank them, restate interest in one sentence, mention one point from the conversation). For **video interviews:** test camera, microphone and connection; keep notes off-screen; avoid distractions.

## 2.6 Eight habits of a good presenter and listener

1. **Know your audience.** Ask who will listen, what they already know and what they want from you. A talk for first-semester students needs everyday examples, while a talk for a bank manager needs numbers and risks. The same topic is explained in different words.
2. **Give one key message.** Decide the single sentence you want people to remember when they leave. Every slide and example should support it. A talk with five messages is remembered as none.
3. **Use a clear structure.** Tell them what you will say, say it in three points, and then tell them what you said. This simple frame helps listeners follow even if their attention slips. Use phrases such as "first", "next" and "in conclusion".
4. **Keep slides simple.** One idea per slide, large letters and a picture or chart instead of paragraphs. The slide supports you; it does not replace you. If listeners read the slide, they stop listening to you.
5. **Look at the audience and use your voice.** Eye contact builds trust, and changes of pace and volume keep interest. Pause after an important point. Avoid reading from the screen or the paper.
6. **Practise and keep time.** Rehearse aloud at least twice with a timer, in front of a friend if possible. For a software demo, keep a recorded backup in case the network or projector fails. Practice reduces fear.
7. **Listen actively.** Look at the speaker, do not interrupt, take short notes and ask a question to check understanding. Paraphrase: "So you mean the deadline moved to Friday?" The speaker feels respected and mistakes are caught early.
8. **Handle questions politely.** Listen to the whole question, repeat it, and answer in a few sentences. If you do not know, say "I will find out and email you" instead of guessing. Honest answers increase your credibility.

```photogrid label="2.2" cols="2" ratio="1.0" caption="Why we forget, and when to review. (a) Hermann Ebbinghaus (1850-1909), who memorised lists of nonsense syllables and measured how much he saved when relearning them. (b) His quoted results: after 20 minutes 58.2 per cent was retained, after 1 hour 44.2, after 8.8 hours 35.8, after 1 day 33.7, after 2 days 27.8, after 6 days 25.4 and after 31 days 21.1. A power law fitted in code, R = 31.9 x t^(-0.126) with t in days, follows the points closely: most loss comes in the first day, then the curve flattens. For a listener or a student this means that notes taken in a meeting are worth reading the same evening, and again within a week, because each review resets the curve. A listener who writes three key points while the speaker talks keeps far more than one who relies on memory alone."
@ photo id="bcapc/ebbinghaus" cap="Hermann Ebbinghaus (1850-1909)"
fit 1.0
focus 0.5 0.3
@ svg cap="Retention after learning (Ebbinghaus data, log time)"
import numpy as np, math
t = np.array([20 / 60 / 24, 1 / 24, 8.8 / 24, 1, 2, 6, 31]); r = np.array([58.2, 44.2, 35.8, 33.7, 27.8, 25.4, 21.1])
b, a = np.polyfit(np.log(t), np.log(r), 1)
assert round(float(np.exp(a)), 1) == 31.9 and round(float(b), 3) == -0.126
X = lambda l: 44 + (l + 2) / 3.6 * 240
Y = lambda v: 180 - v / 70 * 150
f = Fig(300, 240)
f.text(150, 14, "% retained against time since learning", size=10.5, color=NAVY, bold=True)
for v in (0, 20, 40, 60):
    f.line(44, Y(v), 284, Y(v), color="#e2e8f0", sw=1); f.text(38, Y(v), str(v), size=10.5, color=SLATE, anchor="end", vmid=True)
pts = [(X(math.log10(x)), Y(y)) for x, y in zip(t, r)]
xs = np.linspace(math.log10(t[0]), math.log10(t[-1]), 40)
curve = [(X(l), Y(float(np.exp(a)) * (10 ** l) ** float(b))) for l in xs]
for p, q in zip(curve, curve[1:]): f.line(p[0], p[1], q[0], q[1], color=NAVY, sw=1.6, dash=True)
for (x, y), lab in zip(pts, ["20m", "1h", "9h", "1d", "2d", "6d", "31d"]):
    f.circle(x, y, 4, fill=RED, stroke=RED, sw=1)
    f.text(x, 194, lab, size=10, color=SLATE)
f.text(150, 212, "fit: R = 31.9 x t^-0.126 (t in days)", size=10.5, color=NAVY, bold=True)
f.text(150, 230, "58% after 20 min, 34% after a day", size=10.5, color=RED, bold=True)
```

## Formula and fact sheet

- Speaking pace about 125 to 150 words per minute; a 10-minute talk is about 1,300 words, or 8 to 10 slides.
- Active listening: attend, acknowledge, don't interrupt, paraphrase, question, note, summarise.
- PREP and STAR structures. 
- Presentation = introduction, body (3 points), conclusion, questions.
- Slide rule: one idea, few words, large font, high contrast.

## Chapter summary

- Listening is an active skill built on attention, paraphrasing and questions.
- Clear speaking comes from structure, pace, voice, body language and rehearsal.
- A presentation starts from the audience and one key message; slides support rather than replace the speaker.
- Group discussions and interviews reward preparation, honest and specific answers, and respect for others.

## Practice

1. Differentiate hearing and listening. List four barriers to listening.
2. Explain the steps of active listening with an example of paraphrasing.
3. How would you control nervousness before a presentation? Give five measures.
4. Explain the PREP structure by answering "Should BCA students learn Linux?" in four sentences.
5. List eight rules for good slides.
6. Prepare the outline of a 10-minute presentation on "Cyber safety for school students".
7. What do evaluators look for in a group discussion? Give six dos and don'ts.
8. Write a 60-second "Tell me about yourself" for a BCA graduate applying as a junior web developer.
9. Write a STAR answer for "Tell me about a time you failed".
10. How many slides would you prepare for a 15-minute talk, and why?

::: note Answers and worked solutions
**1.** Hearing is receiving sound; listening is paying attention and understanding. Barriers: distraction, prejudice, rehearsing a reply, noise, jargon, fatigue.
**2.** Attend, acknowledge, do not interrupt, paraphrase, ask questions, note, summarise. Paraphrase: "So the demo is moved from Tuesday to Thursday at 11 am?"
**3.** Prepare and rehearse aloud, arrive early and test equipment, breathe slowly, memorise the opening line, concentrate on the message and the audience rather than yourself, accept that some nerves are normal.
**4.** *Point:* Yes, BCA students should learn Linux. *Reason:* most servers, cloud systems and developer tools run on it. *Example:* a Nepali web start-up deploying to a Linux cloud server needs the command line daily. *Point:* So Linux is a basic professional skill.
**5.** One idea per slide; few words; large fonts; high contrast; relevant visuals; consistent design; minimal animation; no reading from the slide.
**6.** Title and hook (a real phishing example) → why it matters → three points (passwords and 2FA, phishing, privacy settings) → demo or quiz → summary and "three things to do today" → questions.
**7.** Content, clarity, listening, leadership, teamwork, composure. Do: support points with examples, respect others, summarise. Don't: interrupt, shout, dominate, go off-topic, repeat.
**8.** Education (BCA), a project or two with technologies, a skill and a result, interest in this role and what you want to learn. About 150 words, spoken in 60 seconds.
**9.** Choose a real, modest failure, take ownership, state what you did to recover and what you learnt and now do differently.
**10.** About 10 to 12 slides (roughly 1 to 1.5 minutes per slide), fewer if a demo takes time. Fewer, clearer slides beat many dense ones.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). What is active listening? Explain the levels of listening and five techniques of active listening, with an example.**

**Listening** is more than hearing. Hearing is a physical process of receiving sound; **active listening** is a deliberate effort to take in the speaker's words, feelings and intention, and to show that you have understood. Poor listening causes repeated work, wrong orders and hurt feelings, so employers value it highly.

**Levels of listening.** (1) *Ignoring*: no effort, the person is thinking of something else. (2) *Pretending*: nods and "yes" without attention. (3) *Selective*: listening only to the parts that interest us. (4) *Attentive*: following the words closely. (5) *Empathic*: understanding the speaker's feelings and point of view as well. Professional listening aims at levels 4 and 5.

**Five techniques.**
1. **Give full attention:** put the phone away and look at the speaker.
2. **Do not interrupt:** let the speaker finish before you reply.
3. **Show interest:** nod, keep an open posture and say "I see".
4. **Ask questions and paraphrase:** "Do you mean the server must be ready by Friday?"
5. **Take brief notes** of names, numbers and actions, then confirm them at the end.

*Example:* A client says, "The report must be perfect." The active listener asks, "Do you mean free of mistakes or in a special format?" and discovers that the client wanted the college logo. **Conclusion:** active listening saves time and builds trust.

**Q (10 marks). Explain how to plan, structure and deliver an effective presentation. Include slide design rules, handling questions and a peer-feedback checklist.**

**Introduction.** A presentation is spoken communication supported by visuals, intended to inform, persuade, train or report. A good one is planned, structured and rehearsed; a poor one is a set of slides read aloud.

**1. Plan with four questions.** *Who* is the audience? *Why* am I speaking (inform, persuade, train, report)? *What* is my single key message? *How long* and in what setting do I speak?

**2. Structure (Figure 2.1).** For ten minutes: introduction (1 min: hook, topic, outline), body (7 min: three main points, each with a claim and an example), conclusion (1 min: summary and call to action), questions (1 min or more).

**3. Slide design.**

| Do | Avoid |
|---|---|
| one idea per slide | paragraphs of text |
| at most 6 lines, 6 words per line | reading the slide aloud |
| large font (24 pt body, 32 pt titles) | tiny fonts, clutter |
| high contrast | red on green, busy backgrounds |
| a chart, diagram or screenshot for data | 3-D charts, pies with 10 slices |

**4. Delivery (Plate 2.1).** Speak to the audience, not the screen; use slides as prompts; stand open and use gestures; vary pace and volume; use a short story or example for each point. For a technical demo, rehearse it and keep a recorded backup.

**5. Handling questions.** Listen to the whole question, repeat it, answer briefly and honestly, and say "I will find out and email you" when you do not know. If one person dominates, offer to continue after the session.

**6. Peer-feedback checklist.** Was the message clear? Was the structure easy to follow? Did eye contact, voice and pace help? Were slides readable? Was time kept? Were questions handled well?

**Conclusion.** Planning gives direction, structure gives clarity and practice gives confidence. A presenter who follows these steps is understood and remembered.

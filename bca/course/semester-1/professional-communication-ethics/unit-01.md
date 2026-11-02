---
subject: Professional Communication and Ethics
grade: BCA Semester 1
unit: 1
title: The Communication Process and Its Barriers
area: BCA 105 · Professional Communication and Ethics · Unit 1
---

An IT professional spends far more time communicating than coding: reading requirements, explaining a bug, writing an email to a client, presenting a design to a team. Most failed projects fail through misunderstanding, not through bad algorithms. This unit explains how communication works, what makes it fail, and the principles of clear professional writing and speaking.

::: key What this unit gives you
- The communication process and models; verbal, non-verbal, written communication.
- Formal and informal channels; direction of flow in an organisation.
- Barriers to communication and how to overcome them.
- The 7 Cs of effective communication and a readability measure you can calculate.
:::

## 1.1 What communication is

**Communication** is the exchange of information, ideas or feelings so that the receiver *understands the meaning the sender intended*. If the message was sent but not understood, communication has not happened.

**The process.**

```text
Sender ──encodes──▶ MESSAGE ──channel──▶ Receiver ──decodes──▶ understanding
   ▲                    ▲ noise (interference)                       │
   └─────────────────────────── FEEDBACK ◀───────────────────────────┘
```

| Element | Meaning | Example (a lecturer announces a deadline) |
|---|---|---|
| Sender (source) | originates the message | the lecturer |
| Encoding | turning the idea into words, symbols, images | writing "Submit by Friday 5 pm" |
| Message | the content | the deadline |
| Channel (medium) | the route | class notice, email, Viber group |
| Receiver | the target | students |
| Decoding | interpreting the message | "Friday of this week or next?" |
| Noise | anything distorting the message | a typo, loud classroom, unclear phrase |
| Feedback | the receiver's response | "Which Friday, sir?" |

The **Shannon–Weaver model** (1948) is a one-way model with noise; the **Schramm** and **transactional** models add feedback and treat both parties as sender and receiver at once. Real conversation is transactional.

## 1.2 Forms of communication

**Verbal.** *Oral* (conversation, phone call, meeting, presentation: quick, immediate feedback, but no record) and *written* (email, report, manual, chat: permanent and checkable, but slower and feedback is delayed).

**Non-verbal.** Body language, facial expression, eye contact, posture, gesture, tone of voice (**paralanguage**), appearance, use of space (**proxemics**), time (**chronemics**: arriving late sends a message). Researchers agree that tone and body language carry much of the *emotional* meaning of a spoken message; the often-quoted "93 % non-verbal" figure is a misreading of Mehrabian's narrow experiments on feelings, and should not be quoted as a general fact.

**Visual.** Charts, diagrams, UML, screenshots, slides. A good diagram can replace a page of text.

**Direction of flow in an organisation**

| Flow | Direction | Example |
|---|---|---|
| Downward | manager → staff | instructions, policy, feedback |
| Upward | staff → manager | progress reports, suggestions, complaints |
| Horizontal (lateral) | peer ↔ peer | developers coordinating with testers |
| Diagonal | across levels and departments | a developer asking finance about a licence |

**Formal channels** follow the organisational chart (memos, official emails, minutes); **informal channels** (the *grapevine*) are social and fast but unreliable. Good managers use formal channels for facts and decisions, and listen to the grapevine for mood.

**Levels:** intrapersonal (self-talk), interpersonal (two people), group/team, organisational, public (one to many), mass (media).

## 1.3 Barriers to communication

| Barrier | Examples | Remedy |
|---|---|---|
| **Physical / environmental** | noise, poor network, bad audio, distance | choose a quiet place, test the link, send a written follow-up |
| **Semantic / language** | jargon, ambiguity, different native languages, abbreviations | use plain words, define terms, check understanding |
| **Psychological / emotional** | anger, fear, stress, boredom, prejudice, defensiveness | pause, calm down, stay objective |
| **Perceptual** | stereotypes, assumptions, first impressions | seek facts, ask rather than assume |
| **Cultural** | different norms about eye contact, hierarchy, directness, gestures | learn the audience's norms; be respectful |
| **Organisational** | too many levels, unclear roles, slow approvals | flatten the path, define who informs whom |
| **Information overload** | long emails, too many channels | summarise, prioritise, one message one purpose |
| **Technological** | wrong tool, incompatible format, unreadable attachment | agree on tools and formats |

**Jargon example.** To a client, "the API is returning 500 because of a null pointer in the DAO layer" means nothing. Better: "the system fails when it looks up a customer who has no address saved; we are fixing it and will test it tomorrow."

## 1.4 Principles: the 7 Cs

| C | Meaning | Weak → better |
|---|---|---|
| **Clear** | one main idea, plain words | "It has been decided to initiate commencement" → "We will start" |
| **Concise** | no padding | "due to the fact that" → "because" |
| **Concrete** | specific facts, numbers, dates | "soon" → "by Friday 5 pm" |
| **Correct** | accurate facts, grammar, names | check spelling of the recipient's name |
| **Coherent** | logical order, linked ideas | use headings and transitions (first, however, therefore) |
| **Complete** | all that the receiver needs: who, what, when, where, why, how | attach the file; give the link |
| **Courteous** | respectful, positive, considerate | "You failed to send…" → "Could you please send…" |

**Active vs passive voice.** "The team fixed the bug" (active, direct) is usually clearer than "The bug was fixed by the team". Passive is acceptable when the doer is unknown or unimportant ("The server was restarted at 2 am").

**Plain-word swaps:** utilise → use, endeavour → try, commence → begin, in the event that → if, at this point in time → now, kindly be advised → (delete).

## 1.5 Measuring readability

The **Flesch Reading Ease** score is **206.835 − 1.015 × (words ÷ sentences) − 84.6 × (syllables ÷ words)**. Higher is easier: 60–70 is plain English, 30–50 is difficult (college level), below 30 is very hard.

::: example Worked example
A 100-word paragraph with 5 sentences and 150 syllables: average sentence length 20 words; syllables per word 1.5. Score = 206.835 − 1.015 × 20 − 84.6 × 1.5 = 206.835 − 20.3 − 126.9 = **59.6**, standard plain English. Shorten the sentences to 12 words (about 8 sentences) with the same word choice and the score rises to 206.835 − 12.18 − 126.9 = **67.8**.
:::

Short sentences (15 to 20 words), common words and one idea per paragraph raise readability without making the content childish.

## 1.6 Cross-cultural and digital communication

- **High-context** cultures (Nepal, Japan, much of South Asia) rely on tone, relationship and what is *not* said; **low-context** cultures (Germany, the US) expect explicit statements. A Nepali "I will try" may mean a polite "no" to a foreign colleague who hears it as "yes"; when working across cultures, confirm in writing.
- **Hierarchy and address:** use respectful forms (Sir, Madam, Mr, Ms, Dr, with surnames) until invited otherwise.
- **Digital etiquette (netiquette):** do not write in ALL CAPS (reads as shouting); avoid sarcasm; reply-all only when needed; keep chat messages complete rather than "hi" and then waiting; think before posting, because digital messages are permanent and can be forwarded; mute during video calls when not speaking; be on time.
- **Choose the medium by purpose:** a quick question: chat; a decision that needs record: email; sensitive or emotional matter: speak face to face or call; complex discussion: meeting; long reference: document.

## Formula and fact sheet

- Process: sender → encode → message → channel → decode → receiver → feedback; noise anywhere.
- Flows: downward, upward, horizontal, diagonal; formal vs grapevine.
- Barriers: physical, semantic, psychological, perceptual, cultural, organisational, overload.
- 7 Cs: clear, concise, concrete, correct, coherent, complete, courteous.
- Flesch = 206.835 − 1.015(W/S) − 84.6(Syl/W).

## Chapter summary

- Communication succeeds only when the intended meaning is understood; feedback confirms it.
- Messages travel in verbal, non-verbal and visual forms and along formal and informal channels.
- Barriers can be removed by plain language, good channel choice, listening and cultural awareness.
- The 7 Cs and a readability check are a practical test for any message before you send it.

## Practice

1. Define communication and draw the communication process with all its elements.
2. Differentiate verbal and non-verbal communication; give four examples of non-verbal signals.
3. Differentiate downward, upward and horizontal communication with an example each.
4. What is the grapevine? State one advantage and one disadvantage.
5. Explain any four barriers to communication and how to overcome them.
6. Rewrite concisely: "In the event that you are not in a position to attend the meeting, kindly be advised to inform us at your earliest convenience."
7. A passage of 120 words has 6 sentences and 168 syllables. Find its Flesch Reading Ease score and comment.
8. Explain the 7 Cs with an example of a poor and a better version of one sentence for each.
9. A foreign client says "We might look at this next quarter." What are two interpretations and how would you clarify?
10. Choose the best medium (chat, email, call, meeting) for: (a) telling a teammate the build failed, (b) confirming a project deadline with a client, (c) giving a team member sensitive negative feedback.

::: note Answers and worked solutions
**1.** Communication is the exchange of messages so that the receiver understands the sender's intended meaning. Diagram and elements as in §1.1.
**2.** Verbal uses words (spoken or written); non-verbal uses no words: eye contact, posture, facial expression, tone, gesture, dress, silence.
**3.** Downward: principal's notice to staff; upward: a team's weekly report to the manager; horizontal: the design team coordinating with the QA team.
**4.** The informal network of rumours and social talk. Advantage: very fast and shows morale. Disadvantage: unreliable and may spread false information.
**5.** Any four from §1.3 with remedies, e.g. semantic: avoid jargon and define terms; physical: reduce noise and test the channel; psychological: delay the conversation until calm; cultural: learn the audience's norms.
**6.** "If you cannot attend the meeting, please tell us as soon as possible." (about 55 % shorter)
**7.** W/S = 20, Syl/W = 1.4. Score = 206.835 − 20.3 − 118.44 = **68.1**, plain English, easy for most readers.
**8.** Clear: "We will start" instead of "initiate commencement". Concise: "because" instead of "due to the fact that". Concrete: "by Friday 5 pm" instead of "soon". Correct: check names and figures. Coherent: add "first / then / therefore". Complete: include the attachment and the deadline. Courteous: "Could you please send…" instead of "You failed to send…".
**9.** It could be a genuine possibility or a polite way of declining. Clarify: "To plan resources, could you confirm in writing whether this is approved for next quarter, and by what date you will decide?"
**10.** (a) chat; (b) email (record of the commitment); (c) a call or face-to-face meeting, followed by a short written summary.
:::

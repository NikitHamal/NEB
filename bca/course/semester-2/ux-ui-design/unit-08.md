---
subject: UX/UI Design
grade: BCA Semester 2
unit: 8
title: Advanced Techniques: VUI and NLP-based UI
area: BCA 155 · UX/UI Design · Unit 8
---

Not every interface has a screen. Voice assistants, chatbots and smartwatches ask designers to think about conversation, sound and tiny glanceable displays. This unit covers command-and-control versus conversational UI, personas, avatars and actors, speech recognition and dialog management, and designing for wearable devices.

::: key What this unit gives you
- Voice user interfaces (VUI) and natural-language (NLP-based) UIs.
- Command-and-control versus conversational interaction.
- Personas, avatars, actors and video-game characters in interface design.
- Speech recognition technology and dialog management.
- Designing for wearable devices.
:::

## 8.1 Voice and NLP-based interfaces

A **voice user interface (VUI)** lets people interact by speaking and listening (smart speakers, phone assistants, in-car systems, IVR phone menus). An **NLP-based UI** (natural language processing) lets people use ordinary language — by speech or text — which the system **parses and interprets**: chatbots, search assistants, LLM-based assistants.

Why use them: **hands-free and eyes-free** (driving, cooking), **accessibility** (blind, motor-impaired, low-literacy users — including voice for people who cannot type in Nepali), **speed** for some tasks ("set a timer for ten minutes"), **natural** and low learning curve, and use on devices without screens.

Challenges: **no visible options** (discoverability — users do not know what they can say); **speech is linear and slow to listen to** (you cannot scan a spoken list), **recognition errors** (accents, noise, Nepali dialects, code-switching between Nepali and English), **ambiguity**, **privacy** (speaking aloud in public, always-listening microphones), **memory load** (users must remember what was said), **no visual feedback**, and the "**uncanny**" expectations created by human-like voices.

### VUI vs GUI

| | **GUI** | **VUI** |
|---|---|---|
| Output | visual, persistent, scannable | audio, transient, serial |
| Input | pointing, typing | speech |
| Discoverability | menus and buttons show what is possible | invisible; must be taught (prompts, examples) |
| Error type | wrong click | misrecognition, misunderstanding |
| Information density | high | low — keep prompts short |
| Best for | complex, visual, comparison tasks | simple, quick, hands-free tasks |
| Privacy | screen shows data privately | speaks data aloud |

Many products are **multimodal** (voice + screen + touch): the assistant answers aloud and shows a card.

## 8.2 Command and control versus conversational UI

| | **Command-and-control** | **Conversational UI** |
|---|---|---|
| Interaction | the user speaks **fixed commands** from a limited vocabulary and the system executes ("Call Ram", "Volume up") | the user speaks or writes **naturally**, in sentences, and the system holds a **dialogue** across several turns |
| Understanding | keyword/grammar matching | natural-language understanding: **intent** and **entities (slots)** |
| Context | one-shot; no memory | keeps **context**: "Book a bus to Pokhara." "For tomorrow." "Make it two seats." |
| Flexibility | low; users must know the exact phrases | high; many ways to say the same thing |
| Reliability | high within vocabulary | lower; needs repair strategies |
| Learning curve | must memorise commands | none, but capabilities are not obvious |
| Examples | old voice dialling, car voice control, IVR "press or say 1" | Alexa, Google Assistant, customer-service chatbots, LLM assistants |

Choice: use **command-and-control** for a small, safety-critical, well-defined command set (hospital equipment, car functions); use **conversational** for open tasks and mixed expertise. Real systems mix them: a few reliable commands inside a conversational frame.

### Natural language understanding in a conversational UI

- **Utterance**: what the user says. **Intent**: what they want (*BookTicket*, *CheckBalance*). **Entities/slots**: the parameters (*destination = Pokhara*, *date = tomorrow*, *seats = 2*).
- The system extracts intent and fills slots; if a **required slot is missing**, it asks ("What day would you like to travel?"); it **confirms** before irreversible actions.
- **Ambiguity** ("book it" — what?) and **out-of-scope** requests must be handled gracefully.

## 8.3 Personas, avatars, actors and video games

Here **persona** has a second meaning: the **personality of the voice or character** the system presents — name, tone, language style — distinct from the user personas of Unit 2.

### System persona
Every voice or chat interface *has* a personality, whether designed or accidental. Decide on it deliberately: **who is the assistant?** (a helpful bank clerk, a cheerful guide, a neutral tool); its **tone** (formal/friendly), **vocabulary** (Nepali honorifics — *hajur*, *tapai* — versus informal *timi*), **humour**, **gender and voice**, and **consistency**. The persona must fit the **brand and the context** (a banking assistant should not joke about a failed payment), the **users' culture and language**, and should be **honest about being a machine** (no pretending to be human; disclose the bot). Write a **persona sheet** (name, role, personality adjectives, do/don't phrases, sample dialogues) and use it as a **style guide** for all prompts.

### Avatars
An **avatar** is a visual embodiment of the system or the user: an animated assistant character, a profile image, a 3D virtual agent. Benefits: friendliness, attention, non-verbal feedback (nod, smile, "thinking" animation), engagement and trust, learning companions. Risks: distraction, slowness, **uncanny valley** (nearly-human characters that feel eerie), stereotyping, and raising expectations the system cannot meet. Guidelines: keep the avatar's **capability matched to its realism** (a simple cartoon for a simple bot), animate **state** (listening, thinking, speaking), allow it to be turned off, and design inclusively (diverse and culturally appropriate).

### Actors (embodied agents) and video games
**Actors** are characters that act in a scripted or autonomous way: voice actors who record the prompts; **embodied conversational agents** such as a virtual shop assistant; **non-player characters (NPCs)** in games. **Video games** are rich laboratories of interface design from which UX borrows: **immediate feedback**, **clear goals**, **progressive difficulty and onboarding by doing** (tutorial levels), **reward loops**, **character voice and personality**, **heads-up displays** that show status without clutter, **diegetic** interfaces (UI elements inside the game world), and **flow** (challenge matched to skill). Applications: **gamification** (points, badges, streaks in a learning or fitness app — useful when it motivates real goals and harmful when manipulative), voice-acted tutorials, and characters as guides.

Design implications for conversational UIs: write dialogue like a **script** — read aloud, perform it with a colleague (**table read**), use **Wizard-of-Oz** tests; keep persona **consistent across channels**; use sound design (earcons) for status.

## 8.4 Speech recognition technology

**Automatic speech recognition (ASR / speech-to-text)** turns a sound wave into text. **Speech synthesis (text-to-speech, TTS)** does the reverse.

### Pipeline of a speech recogniser

1. **Audio capture** and sampling (typically 16 kHz).
2. **Pre-processing**: noise reduction, echo cancellation, **voice activity detection** (where speech starts and ends).
3. **Feature extraction**: the signal is cut into ~25 ms frames; **MFCCs** or spectrogram features are computed.
4. **Acoustic model**: maps features to **phonemes** (earlier **HMM-GMM**; now **deep neural networks**: end-to-end models such as CTC, RNN-T, Whisper-style transformers).
5. **Pronunciation lexicon** and **language model**: choose the word sequence that is most probable (*"recognise speech"* versus *"wreck a nice beach"*).
6. **Decoder** produces the transcript, often with confidence scores and alternatives (n-best list).
7. **NLU** then derives intent and entities.

### Measures and problems
**Word error rate (WER) = (S + D + I) / N** — substitutions + deletions + insertions over the number of reference words. Example: reference "set an alarm for six", output "set an alarm for sticks" → 1 substitution in 5 words → **WER = 20 %**. Factors that raise errors: **noise**, **accents and dialects**, **speaking style**, **vocabulary** (names, domain terms), **homophones**, **code-switching**, **low-resource languages** (Nepali has far less training data than English — accuracy is lower and varies by region), **overlapping speakers**.

Types: **speaker-dependent vs independent**; **isolated-word vs continuous**; **small vocabulary vs large vocabulary**; **on-device vs cloud** recognition (privacy and latency vs accuracy); **wake word** detection ("Hey Google") runs locally and always listens for the trigger only. **Speaker recognition (voice biometrics)** identifies *who* is speaking.

### Speech synthesis and prompt design
TTS (concatenative → neural) must sound clear and natural; control **speed, pitch, pauses** with **SSML** markup. **Prompt guidelines**: be **brief** (first-turn prompts under ~10 seconds), put the **key information last** (the end of a spoken sentence is remembered best), offer at most **3 options** at a time, use **everyday words**, front-load the question ("Which city? Pokhara, Chitwan or Butwal?"), **avoid long menus**, and use **earcons** (short sounds) for state changes.

## 8.5 Dialog management

A **dialog manager** controls the conversation: it keeps **state** (what has been said and what is still needed), decides the **next action** (ask a question, confirm, call a service, answer, hand off), and manages **turn-taking**. Core elements:

- **Dialog state tracking**: current intent, filled and missing slots, history, user profile.
- **Dialog policy**: rules or learned strategies deciding the next system action.
- **Natural-language generation**: the wording of the reply.

### Dialog styles
| Style | Description |
|---|---|
| **Directed (system-initiative, form-filling)** | the system asks one question at a time ("Which city?") — reliable, easy, rigid |
| **Mixed-initiative** | the user can volunteer extra information ("A ticket to Pokhara tomorrow, two seats") and the system fills several slots at once |
| **Open-ended / free** | LLM-style, any topic; flexible but harder to control and to keep accurate |

Techniques: **finite-state** dialogs (flow charts), **frame/slot-filling**, **rule-based**, **statistical/reinforcement-learning** policies, and **LLM-driven** agents with tool use and guardrails.

### Principles of good dialog design

| Principle | Practice |
|---|---|
| **Grice's cooperative maxims** | be **truthful** (quality), say **enough but not too much** (quantity), be **relevant**, be **clear** (manner) |
| **Set expectations** | greet, say what the system can do ("I can help you book a bus, check a booking, or cancel."), disclose that it is automated |
| **Give users a way out** | "agent", "help", "start over" always work; hand-off to a human with context |
| **Confirmation** | **explicit** ("Did you say Pokhara?") for high-risk, low-confidence steps; **implicit** ("Booking a bus to Pokhara. What date?") for low risk; avoid confirming everything |
| **Error handling and repair** | detect: *no input*, *no match*, *low confidence*; respond with **escalating help**: rephrase → give examples ("You can say tomorrow or a date") → offer another channel; never say only "I didn't understand" twice; limit to ~3 attempts then hand off |
| **Context and memory** | remember within the session ("it", "that one"), without being creepy; clear **barge-in** (the user interrupts the voice prompt) |
| **Turn-taking and timing** | respond within ~1 second; use filler sounds for long processing; do not cut off the user |
| **Personality and politeness** | consistent persona; polite but not verbose |
| **Privacy and security** | do not speak sensitive data aloud (PINs, balances) without authentication; confirm before payments; offer a visual channel |
| **Discoverability** | contextual hints, example phrases, "What can I say?" |
| **Test with real users** | collect real utterances, measure **task completion**, **WER**, **intent accuracy**, **containment rate** (resolved without a human) and user satisfaction |

::: example Worked example: a dialog with repair
**System:** "Namaste! I can book, check or cancel bus tickets. What would you like to do?"
**User:** "Ticket Pokhara kal." (Nepali–English mix)
**System:** (intent *BookTicket*, destination = Pokhara, date = tomorrow: slots filled by mixed initiative) "Booking a bus to Pokhara for tomorrow. How many seats?"
**User:** "Dui." (two)
**System:** "Two seats to Pokhara tomorrow, morning bus at 7:00 for NPR 1,200 each. Shall I book it?" (explicit confirmation before payment)
**User:** (noise, unrecognised)
**System:** "Sorry, I didn't catch that. You can say yes or no." (repair with an example)
**User:** "Yes."
**System:** "Booked. Your confirmation was sent by SMS." — each turn is short, key information last, one question at a time.
:::

## 8.6 Designing for wearable devices

**Wearables** are computers worn on the body: smartwatches, fitness bands, smart glasses, earbuds (hearables), smart rings, health patches, AR/VR headsets.

### Characteristics and constraints

- **Tiny screens** (a watch face ≈ 1.2–1.9 inches, some bands have none); little room for text and controls.
- **Glanceable use**: interactions of **a few seconds**; information must be understood in a glance (the "**glance test**": 2–5 seconds).
- **Limited input**: touch with a big finger on a small screen, crown/button, voice, gestures, tap-to-pay; text entry is slow.
- **Limited battery and processing**: use dark themes (OLED saves power), simple animation, offload to the phone.
- **Always on the body**: **context-aware and sensor-driven** (heart rate, steps, GPS, accelerometer) — **proactive** notifications at the right moment.
- **Social acceptability**: talking to or gesturing at a device in public; discreet **haptic feedback** (vibration patterns) is often better than sound.
- **Privacy and health data**: highly personal; clear consent, local processing, secure storage.
- **Companion model**: the watch and the phone divide work — the watch for glance and quick actions, the phone for setup and detail.

### Design guidelines

| Guideline | Practice |
|---|---|
| **Glanceable** | show the single most important item; large type (≥ 16 pt), high contrast; one idea per screen |
| **Minimal interaction** | at most 1–2 taps for the main task; use **complications/widgets** and **quick replies** instead of typing; voice dictation for text |
| **Large touch targets** | min ~ 44 pt (watchOS) / 48 dp (Wear OS); keep targets away from the edge of round screens |
| **Prioritise notifications** | short, actionable, only what matters; let users control; **haptics** to attract attention; never spam the wrist |
| **Context-awareness** | use sensors to anticipate (show boarding pass at the airport, workout controls during a run); allow quick dismissal |
| **Multimodal** | combine haptic, visual and audio feedback; allow **eyes-free** use during sport |
| **Respect the shape** | round vs square screens, bezel and crown interaction; content centred and hierarchical |
| **Battery-aware** | black backgrounds on OLED, limited animation, reduce wake-ups |
| **Accessibility** | text size, VoiceOver/TalkBack, haptic cues, colour-blind safe palettes |
| **Seamless handoff** | continue on the phone for complex tasks ("Open on iPhone") |
| **Safety** | do not distract while driving or cycling; minimise glances |

Example: a Nepal bus-ticket watch app — shows the next departure ("Pokhara 7:00, Seat 12 — 25 min"), a single button **Show QR**, a haptic reminder 30 minutes before departure; everything else (changing the booking) is handed off to the phone. For **smart glasses/AR** add: do not obstruct vision; use short bursts of information anchored in the world; voice and gaze input. For **hearables**: audio-only UI with earcons and voice; very short prompts.

## Formula and fact sheet

- VUI: eyes-free and hands-free; weak discoverability; speech is serial → short prompts, ≤ 3 options, key information last.
- Command-and-control = fixed phrases; conversational = intents + slots + context across turns.
- System persona: deliberate name, tone and language; disclose that it is a bot. Avatars: match realism to capability (uncanny valley).
- ASR pipeline: audio → features → acoustic model → language model → decoder → text → NLU. WER = (S + D + I)/N.
- Dialog manager: state tracking + policy + generation. Mixed-initiative fills several slots at once. Confirm risky steps; repair with escalating help; hand off to a human after ~3 failures.
- Wearables: glanceable (2–5 s), 1–2 taps, haptics, sensors, phone companion, battery-aware, large targets.

## Chapter summary

- VUI and NLP-based UIs give hands-free and natural interaction but hide their options and suffer from recognition and ambiguity errors.
- Command-and-control uses fixed commands and is reliable; conversational UIs use intents, slots and context and are flexible but less predictable.
- A designed persona gives a voice or chatbot a consistent personality; avatars and game-style characters can engage users when their realism matches their ability.
- Speech recognition converts speech to text through acoustic and language models; Nepali is a low-resource language with higher error rates.
- Dialog management tracks state, chooses the next action, confirms risk, and repairs errors with a human fallback.
- Wearables demand glanceable, minimal, context-aware, haptic-rich design.

## Practice

1. Compare VUI and GUI with advantages and limitations of each.
2. Differentiate between command-and-control and conversational UI with examples.
3. Define utterance, intent and entity; analyse "Book two seats to Pokhara for tomorrow".
4. What is a system persona? Write a persona sheet for a bank's voice assistant in Nepal.
5. What are avatars and the uncanny valley? List two design guidelines for avatars.
6. How can video-game design inform UX? Give three techniques.
7. Describe the pipeline of speech recognition. Compute the WER for reference "turn on the kitchen light", output "turn off the kitchen night".
8. Explain dialog management, directed vs mixed-initiative dialog, and confirmation and repair strategies.
9. List six guidelines for designing wearable interfaces.
10. Design the interaction of a smartwatch app for medicine reminders (screens, notification, input).

::: note Answers and worked solutions
**1.** VUI — hands-free, accessible, natural; but invisible options, errors, privacy. GUI — visible, scannable, precise; needs eyes and hands.
**2.** Command-and-control: fixed phrases ("Call Ram"); conversational: natural multi-turn dialogue with intent and context ("Book a bus to Pokhara" … "make it two seats").
**3.** Utterance = the sentence; intent = BookTicket; entities: seats = 2, destination = Pokhara, date = tomorrow.
**4.** The persona is the assistant's designed personality: name (e.g. "Dhan"), role (a calm, respectful bank clerk), tone (formal, uses *tapai/hajur*), do/don't phrases (no jokes about money problems), disclosure ("I'm the bank's virtual assistant"), sample dialogues.
**5.** An avatar is a visual embodiment of the system or user; the uncanny valley is the eeriness of nearly-human characters. Match realism to ability; show states (listening/thinking); allow disabling.
**6.** Immediate feedback; onboarding by playing tutorials; progress, rewards and badges (gamification); heads-up displays; flow.
**7.** Audio capture → pre-processing/voice detection → features (MFCC) → acoustic model → language model → decoder → text (→ NLU). Words: 5; "on→off" and "light→night" are 2 substitutions: **WER = 2/5 = 40 %**.
**8.** The dialog manager tracks state, chooses the next action and generates replies. Directed: one question at a time; mixed-initiative: user volunteers several slots. Confirm explicitly for risky or low-confidence steps; repair with rephrase → examples → alternative channel → human hand-off.
**9.** Glanceable content, minimal interaction, big targets, haptic and prioritised notifications, context-awareness, battery-awareness, accessibility, phone hand-off.
**10.** Notification: haptic tap plus "Paracetamol 500 mg — 8:00" with big buttons **Taken** and **Snooze 10 min**; main screen shows only the next dose; voice reply allowed; detailed schedule editing on the phone; missed-dose escalation to a caregiver after 30 minutes.
:::

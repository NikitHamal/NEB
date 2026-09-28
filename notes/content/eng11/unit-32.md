---
subject: Compulsory English
grade: 11
unit: 32
title: 'Functional Writing: Letters, Emails, Applications and Notices'
hours: 7
area: Writing and Skills
---

Question 5 of the NEB paper carries eight marks for **functional writing** — the
everyday written forms an adult actually has to produce: a letter to an office, an
email, an application for a job or for leave, a notice on a board. Unlike an essay,
each of these has a **fixed shape**. Half the marks are for putting the right parts
in the right places; the other half are for hitting the right level of politeness.
Learn the shapes and this becomes the easiest question on the paper.

::: key Format first, then language
A brilliant letter written in the wrong format loses the format marks and cannot get
them back. Before you write a word, draw the skeleton in your head: where the date
goes, where the address goes, which closing goes with which salutation. Then fill it.
:::

## 32.1 The forms, and how formal each one is

| Form | Written to | Register | Typical length |
|---|---|---|---|
| Formal letter (office, editor, company) | someone you do not know | formal | 120–180 words |
| Application (job, leave, scholarship) | an authority | formal | 120–180 words |
| Email — official | a teacher, an office | semi-formal | 80–140 words |
| Email or letter — personal | a friend, a relative | informal | 100–150 words |
| Notice | everybody, on a board | impersonal | **50 words or fewer** |
| Advertisement, invitation | the public | impersonal | very short |

**Register** is the level of formality. The same message can be written three ways,
and choosing wrongly is the commonest reason a well-written answer scores six out of
eight instead of eight.

| Function | Formal | Neutral | Informal |
|---|---|---|---|
| Opening | With reference to your advertisement of 12 Bhadra … | I am writing about … | Just a quick note about … |
| Requesting | I should be grateful if you would send … | Could you please send … | Can you send …? |
| Apologising | I regret any inconvenience caused. | I am sorry about the delay. | Sorry about that! |
| Thanking | I am much obliged to you. | Thank you very much. | Thanks a lot! |
| Complaining | I wish to draw your attention to … | I am not happy about … | This is really bad. |
| Closing | I look forward to hearing from you. | I hope to hear from you soon. | Write soon! |

::: caution Register mistakes that Nepali candidates make most often
- ***Myself Ramesh Thapa.*** → **I am Ramesh Thapa** / **My name is Ramesh Thapa.**
- ***Kindly do the needful.*** → **Please take the necessary action.** (office
  English of a hundred years ago; examiners mark it down)
- ***Your's faithfully*** → **Yours faithfully** — no apostrophe, ever.
- ***Thanking you*** used on its own as the close → **Thank you.** or **I look
  forward to your reply.**
- ***Please reply back*** → **Please reply.** *Back* is already inside *reply*.
- ***I request for two days' leave*** → **I request two days' leave** or **I am
  applying for two days' leave.**
- Contractions (*I'm, don't, can't*) belong in a personal letter, **never** in a
  formal one. Write *I am, do not, cannot*.
:::

## 32.2 The formal letter: the parts and where they go

```figure caption="A formal letter in modern block style: every part starts at the left margin, nothing is indented, and one blank line separates the blocks."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.4,4.4))
ax.set_xlim(0,10); ax.set_ylim(0,13.6); ax.axis('off')
ax.add_patch(Rectangle((0.6,0.4), 6.6, 12.8, fc='#fdfdfe', ec='#aab0ba', lw=1.0))
L = 1.15
def blk(y, lines, n, note):
    for i, s in enumerate(lines):
        ax.text(L, y-0.52*i, s, fontsize=7.2, color=INK, ha='left', va='center')
    ax.text(0.92, y+0.30, str(n), fontsize=6.6, color='white', ha='center',
            va='center', zorder=6, fontweight='bold',
            bbox=dict(boxstyle='circle,pad=0.24', fc=ACCENT, ec='white', lw=0.6))
    ax.plot([7.35, 7.75], [y-0.26*(len(lines)-1), y-0.26*(len(lines)-1)],
            color=GRID, lw=0.8)
    ax.text(7.95, y-0.26*(len(lines)-1), note, fontsize=6.8, color=MUTED,
            ha='left', va='center')
blk(12.60, ['Ramesh Thapa', 'Ward No. 4, Lekhnath', 'Pokhara'], 1, 'your address')
blk(10.70, ['14 Bhadra 2082'], 2, 'date')
blk(9.70, ['The Editor', 'The Himalayan Times', 'Kathmandu'], 3, 'who it goes to')
blk(7.55, ['Subject: Dust on the Lekhnath road'], 4, 'one line, no full stop')
blk(6.55, ['Dear Sir or Madam,'], 5, 'comma after it')
blk(5.55, ['Paragraph 1 — why you are writing.',
           'Paragraph 2 — the facts, in order.',
           'Paragraph 3 — what you want done.'], 6, 'three short paragraphs')
blk(3.25, ['Yours faithfully,'], 7, 'matches the salutation')
blk(2.25, ['(signature)', 'Ramesh Thapa', 'Student, Grade 11'], 8, 'sign, then print')
```

```photo id="eng11/letterhead" caption="A real business letter of 1898. Every part named in the skeleton above is present, in the same order — only the style is the older indented one, with the sender's address and the date on the right." width="72"
crop 0.02 0.02 0.98 0.99
mark 0.085 0.905 "1"
mark 0.455 0.852 "2"
mark 0.065 0.790 "3"
mark 0.065 0.726 "4"
mark 0.065 0.520 "5"
mark 0.500 0.227 "6"
mark 0.455 0.170 "7"
key 1 Letterhead — the sender's name and business, printed at the top
key 2 The sender's street address and the date of writing
key 3 The inside address — the name and place of the person written to
key 4 The salutation, followed by a colon or a comma
key 5 The body, divided into short paragraphs, one idea each
key 6 The complimentary close, on its own line
key 7 The signature, written by hand. A modern letter adds a subject line between 3 and 4, and prints the name under the signature
```

**Salutation and close must agree.** This is a one-mark point every year.

| You are writing to | Salutation | Close |
|---|---|---|
| someone whose name you do not know | Dear Sir, / Dear Madam, / Dear Sir or Madam, | **Yours faithfully,** |
| someone whose name you know | Dear Mr Adhikari, / Dear Ms Rai, | **Yours sincerely,** |
| a friend or a relative | Dear Sabina, / My dear brother, | Yours ever, / With love, |

Only the **first** word of the close takes a capital letter: *Yours faithfully*, not
~~Yours Faithfully~~. Write the date in full — *14 Bhadra 2082* or *30 August 2025* —
never as 9/12/26, which means two different days in two different countries.

## 32.3 Kinds of formal letter, and the envelope

**A letter of complaint** states the facts calmly: what you bought or experienced,
when, where, what went wrong, and exactly what you want (a repair, a refund, an
apology). Never threaten and never abuse.

**A letter to the editor** names the problem in the first line, gives two or three
concrete details, and ends by asking the authority concerned to act. It is signed
with your name and place.

**A letter of enquiry** asks numbered questions so that the reader can answer each
one: *Could you please tell me (a) the fee for the whole course, (b) the dates of
the next intake, and (c) whether a hostel is available?*

**A letter of invitation** gives the occasion, the date, the time, the place and how
to reply.

```photo id="eng11/envelope" caption="An addressed envelope. The sender's address goes small in the top left corner, the receiver's address large across the middle, and the stamp in the top right corner, where the post office cancels it with a dated postmark." width="86"
crop 0.03 0.03 0.98 0.97
call 0.235 0.705 0.130 0.845 "sender's address"
call 0.570 0.585 0.762 0.772 "stamp and postmark"
call 0.280 0.190 0.300 0.440 "receiver's name and address"
```

On a Nepali envelope the receiver's block runs, one item to a line: **name and
title · ward number and street · municipality or rural municipality · district ·
postal code**. The sender's block, in the top left corner, gives the same details in
smaller writing, so that the letter can be returned if it cannot be delivered.

## 32.4 Emails

An email is a letter without the addresses. What it gains instead is a **subject
line**, and that line does most of the work: it tells a busy reader what the message
is about before it is opened.

| Field | What goes in it |
|---|---|
| **To** | the main reader |
| **Cc** | others who should see it (everyone can see this list) |
| **Bcc** | others who should see it without the rest knowing |
| **Subject** | four to eight words, specific: *Request for leave, 12–14 Asoj* |
| Greeting | *Dear Sir or Madam,* · *Dear Ms Rai,* · *Hello Anil,* |
| Body | short paragraphs; one blank line between them |
| Sign-off | *Yours faithfully,* / *Regards,* / *Best wishes,* + your full name |

::: caution Email faults that cost format marks
- **An empty or vague subject line** — *Hello*, *Important*, *Question* tell the
  reader nothing. Name the thing: *Application for the post of Office Assistant.*
- **SMS spelling** — *u, plz, thnx, gr8, asap* have no place in a graded answer.
- **No greeting and no name at the end.** An email that begins *I want leave* and
  ends with nothing is not a complete answer.
- **Shouting.** A message typed IN CAPITALS reads as anger.
- **Forgetting the attachment you promised.** If you write *Please find my CV
  attached*, say in the answer that it is attached.
:::

## 32.5 Applications, and the curriculum vitae

A **job application** has a fixed set of moves. Keep to them and keep it to one page.

1. Where you saw the advertisement, and the exact post you want.
2. Why you are suitable — your qualification, then your experience, then one skill.
3. What you are sending with the letter (CV, certificates, citizenship copy).
4. A request for an interview, and thanks.

A **leave application** to a principal is shorter: the reason, the exact dates, who
will cover your work or notes, and the request itself.

```photo id="eng11/cv" caption="A real curriculum vitae. Notice what the layout does for the reader: name and contact details at the top, then a short profile, then clearly headed blocks in reverse order of date, newest first." width="66"
crop 0.02 0.02 0.98 0.98
```

A student's CV is **one page**, not three. Use these headings:

| Heading | What goes under it |
|---|---|
| Personal details | full name, address, mobile number, email, date of birth |
| Career objective | one sentence: the kind of post you are seeking |
| Academic qualifications | a small table: examination, board, year, division — newest first |
| Work experience | post, organisation, dates, one line on duties |
| Skills | languages, computer skills, driving licence |
| Extra-curricular activities | sport, debate, scouting, volunteering |
| Referees | two people, with their post and contact — ask them first |

## 32.6 Notices

A notice is written **to everybody and by an office**, so it uses no *I* and no *you*.
It goes in a box on a board, and the body must be **fifty words or fewer**.

```figure caption="The skeleton of a notice. The body answers what, when, where and who in three or four lines; the issuing officer signs at the bottom right."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.6,3.4))
ax.set_xlim(0,10); ax.set_ylim(0,9.2); ax.axis('off')
ax.add_patch(Rectangle((0.5,0.35), 9.0, 8.5, fc='#fdfdfe', ec=INK, lw=1.3))
ax.text(5.0, 8.30, 'SHREE JANATA SECONDARY SCHOOL', fontsize=7.8, color=INK,
        ha='center', va='center')
ax.text(5.0, 7.55, 'N O T I C E', fontsize=9.4, color=ACCENT, ha='center',
        va='center', fontweight='bold')
ax.plot([3.60,6.40],[7.17,7.17], color=ACCENT, lw=0.9)
ax.text(1.0, 6.45, '20 Asoj 2082', fontsize=7.2, color=INK, ha='left', va='center')
ax.text(5.0, 5.65, 'Inter-house Quiz Competition', fontsize=7.8, color=INK,
        ha='center', va='center')
ax.text(0.95, 4.00,
        'All students of Grades 11 and 12 are informed that an\n'
        'inter-house quiz will be held in the school hall on\n'
        'Friday, 27 Asoj, at 1 p.m. Teams of three should give\n'
        'their names to the class teacher by 25 Asoj.',
        fontsize=6.5, color=INK, ha='left', va='center', linespacing=1.55)
ax.text(8.9, 1.90, 'Sd/-', fontsize=7.0, color=INK, ha='right', va='center')
ax.text(8.9, 1.35, 'Bimala Karki', fontsize=7.2, color=INK, ha='right', va='center')
ax.text(8.9, 0.85, 'Principal', fontsize=7.0, color=MUTED, ha='right', va='center')
for y, t in [(8.30,'issuing body'), (7.55,'the word NOTICE'), (6.45,'date'),
             (5.65,'heading'), (4.00,'body — 50 words or fewer'),
             (1.35,'signature, name, post')]:
    ax.annotate('', xy=(0.45,y), xytext=(-0.55,y),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8,
                                mutation_scale=7))
    ax.text(-0.65, y, t, fontsize=6.9, color=MUTED, ha='right', va='center')
ax.set_xlim(-3.6,10)
```

```photo id="eng11/notice-board" caption="A village notice board. The two boxed sheets are a notice of an election and a notice of an auction. Public notices compete for attention, which is why a heading in large type and a date near the top matter as much as the words themselves." width="88"
crop 0.11 0.02 0.95 0.76
box 0.140 0.323 0.211 0.453
box 0.528 0.134 0.148 0.308
```

::: example Model answer 32.1 — a letter to the editor
**Question.** Write a letter to the editor of a national daily drawing the attention
of the authorities to the dust and the broken road in your locality.
<span class="marks">[8]</span>

**Model answer.**

Ramesh Thapa
Ward No. 4, Lekhnath
Pokhara

14 Bhadra 2082

The Editor
The Himalayan Times
Kathmandu

Subject: Dust and broken road in Lekhnath

Dear Sir or Madam,

Through the columns of your respected daily I wish to draw the attention of the
Pokhara Metropolitan City office to the condition of the road that runs from Lekhnath
chowk to the campus gate.

The road was dug up for a water pipeline eight months ago and has not been resurfaced
since. In the dry season the dust is so thick that shopkeepers must close their
shutters by midday, and three of the four schools on this stretch report a rise in
chest complaints among their pupils. In the monsoon the same stretch becomes a line
of pits in which two motorcyclists have already been injured.

I therefore request the city office to resurface the road before the festival season
and, until that is done, to water it twice a day. A reply through your newspaper
would reassure several thousand residents.

Yours faithfully,

Ramesh Thapa
Student, Grade 11

**Why it scores.** All eight parts of the skeleton are present and in block style;
*Dear Sir or Madam* is correctly paired with *Yours faithfully*; the three paragraphs
do three separate jobs — why, what, what next; and the complaint is supported by
facts rather than by anger.
:::

::: example Model answer 32.2 — an application for a job
**Question.** An advertisement in *The Kathmandu Post* of 5 Asoj invites applications
for the post of Office Assistant at Everest Trading Pvt. Ltd., Naxal. Write an
application for the post. <span class="marks">[8]</span>

**Model answer.**

Sabina Rai
Ward No. 9, Dhankuta

8 Asoj 2082

The Manager
Everest Trading Pvt. Ltd.
Naxal, Kathmandu

Subject: Application for the post of Office Assistant

Dear Sir or Madam,

With reference to your advertisement in *The Kathmandu Post* of 5 Asoj 2082, I wish
to apply for the post of Office Assistant in your organisation.

I passed the Secondary Education Examination in 2080 with a GPA of 3.4 and am at
present studying in Grade 11 at Dhankuta Multiple Campus. For the past eight months I
have kept the sales register and answered the telephone at a stationery shop in
Dhankuta, so I am used to dealing with customers. I can type in both Nepali and
English and can work in Word and Excel.

I am enclosing my curriculum vitae, copies of my certificates and a copy of my
citizenship certificate. I should be grateful for the opportunity of an interview at
any time convenient to you.

Thank you for considering my application.

Yours faithfully,

Sabina Rai

**Why it scores.** It names the advertisement and its date in the first line, so the
reader knows at once which post is meant; qualification, experience and skill come in
that order; the enclosures are listed; and the request for an interview is polite
without being humble.
:::

::: example Model answer 32.3 — a notice
**Question.** You are the secretary of the school's eco club. Write a notice in not
more than fifty words informing the students about a tree-plantation programme.
<span class="marks">[8]</span>

**Model answer.**

**SHREE JANATA SECONDARY SCHOOL, BIRATNAGAR**

**N O T I C E**

22 Asoj 2082

**Tree-plantation Programme**

All students of Grades 9 to 12 are informed that the Eco Club will plant three
hundred saplings on the school ground on Saturday, 28 Asoj, from 7 a.m. Students
should bring a spade and a water bottle. Names may be given to the class teacher by
26 Asoj.

Sd/-
Nirmala Gurung
Secretary, Eco Club

**Why it scores.** The body is 46 words. It is impersonal — *students are informed*,
not *I inform you* — and it answers what, who, where, when and what to bring. The
date, the heading and the signature block are all in their proper places.
:::

## 32.7 Checking your own answer

| | Check |
|---|---|
| 1 | Sender's address, date, receiver's address — all present and in order? |
| 2 | Subject line: one line, capital on the first word, **no** full stop? |
| 3 | Does the close match the salutation (*Sir* → *faithfully*, *Mr Rai* → *sincerely*)? |
| 4 | Is the body in three short paragraphs, one job each? |
| 5 | Any contractions in a formal letter? Expand them. |
| 6 | Any *Myself…*, *do the needful*, *reply back*, *Your's*? Remove them. |
| 7 | Is a notice inside a box, impersonal, and fifty words or fewer? |
| 8 | Is the signature block signed, then printed, then given a post? |

## Chapter summary

- Q5, functional writing, 8 marks: roughly half for format, half for language and
  register. Fix the skeleton before you write.
- Formal letter, block style, in order: sender's address · date · receiver's address ·
  subject · salutation · three body paragraphs · close · signature, name, post.
- *Dear Sir / Madam* → **Yours faithfully**; *Dear Mr Rai* → **Yours sincerely**.
  Only the first word of the close is capitalised.
- Formal register: *I should be grateful if you would…*, *I regret any inconvenience
  caused*, *I look forward to hearing from you*. No contractions.
- Avoid *Myself Ram*, *kindly do the needful*, *reply back*, *Your's faithfully*,
  *request for leave*.
- An email needs a specific subject line, a greeting, short paragraphs and a signed
  sign-off; no SMS spelling, no capitals throughout.
- A job application names the advertisement and its date, then qualification,
  experience, skill, enclosures and a request for an interview.
- A CV for a student is one page: personal details, objective, qualifications,
  experience, skills, activities, referees.
- A notice is impersonal, boxed, fifty words or fewer, and carries the issuing body,
  the word NOTICE, the date, a heading and a signature with a post.

## Practice questions

**Functional writing (8 marks each)**

1. Write a letter to the manager of a mobile phone company complaining that the
   handset you bought three weeks ago switches itself off, and asking for a
   replacement. <span class="marks">[8]</span>
2. Write an email to your class teacher asking for three days' leave to attend your
   sister's wedding, and saying how you will cover the lessons you miss.
   <span class="marks">[8]</span>
3. You are the head boy of your school. Write a notice in not more than fifty words
   informing students that the annual sports week has been postponed because of rain.
   <span class="marks">[8]</span>

::: note Model answers
**1.** *Anisha Shrestha, Ward No. 6, Itahari · 12 Kartik 2082 · The Customer Service
Manager, Him Mobile Pvt. Ltd., Putalisadak, Kathmandu · Subject: Faulty handset,
invoice no. 4417 · Dear Sir or Madam,* — **Para 1:** I bought a Him M20 handset from
your Itahari showroom on 18 Asoj 2082; the invoice number is 4417 and the warranty
runs for one year. **Para 2:** From the fourth day the handset has switched itself
off without warning, between six and ten times a day, even when the battery is above
eighty per cent. Your showroom reset the software on 2 Kartik, but the fault returned
the same evening. **Para 3:** As the handset is within warranty and has failed twice,
I request a replacement rather than a further repair. I am enclosing a copy of the
invoice and the warranty card, and I look forward to your reply within seven days.
*Yours faithfully, Anisha Shrestha.*

**2.** *Subject: Request for leave, 14–16 Mangsir.* — *Dear Sir,* I am writing to
request three days' leave from 14 to 16 Mangsir 2082, as my elder sister's wedding
takes place at our home in Gorkha and I am needed there. I have asked Sunita Adhikari
to keep a copy of the notes for Physics and English, and I shall complete the
laboratory report for Chemistry before I leave. I shall return to class on 17
Mangsir. I should be grateful if you would grant me leave for these three days.
*Yours faithfully, Prakash Bhandari, Grade 11 "A", Roll No. 17.*

**3.** **SHREE BAGMATI SECONDARY SCHOOL · N O T I C E · 3 Falgun 2082 · Annual Sports
Week Postponed.** All students are informed that the annual sports week, announced
for 6 to 10 Falgun, has been postponed because of continuous rain. The new dates will
be put up on this board on 8 Falgun. Practice sessions are cancelled until then.
*Sd/- Rajan Limbu, Head Boy.* (44 words.)
:::

**Register and format (1 mark each)**

4. Make this formal: *Can you send me the fee details fast?* <span class="marks">[1]</span>
5. Correct: *Your's sincerely, Bibek* (the letter began *Dear Sir,*) <span class="marks">[1]</span>
6. Correct: *Myself Sita Poudel and I want two days leave.* <span class="marks">[1]</span>
7. Write a suitable subject line for an email applying for the post of Lab Assistant. <span class="marks">[1]</span>
8. Correct: *Kindly do the needful and reply back soon.* <span class="marks">[1]</span>
9. Rewrite without contractions: *I'm afraid I can't attend the meeting.* <span class="marks">[1]</span>
10. What is wrong with this notice line: *I want to inform all of you that the picnic is cancelled.* <span class="marks">[1]</span>

::: note Answers
**4.** I should be grateful if you would send me the details of the fee at your earliest convenience. — formal request pattern; *fast* is too blunt.
**5.** **Yours faithfully, Bibek** — no apostrophe, and *Dear Sir* pairs with *faithfully*, not *sincerely*.
**6.** **I am Sita Poudel, and I wish to apply for two days' leave.** — *myself* is not a subject; *two days'* needs the apostrophe.
**7.** **Application for the post of Lab Assistant** — specific, four to eight words, no full stop.
**8.** **Please take the necessary action and reply soon.** — *do the needful* is dead office English; *back* is already inside *reply*.
**9.** **I am afraid I cannot attend the meeting.** — contractions are for informal writing only.
**10.** A notice is impersonal: there is no *I* and no *you*. Write **All students are informed that the picnic has been cancelled.**
:::

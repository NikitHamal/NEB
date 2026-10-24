---
subject: Question Bank
grade: 10
unit: 20
title: "Computer Science: Unit-wise Objective Question Bank"
hours: 0
area: Computer Science
---

The new SEE Computer Science paper is short — **two hours, fifty marks** — and
it opens with **ten one-mark multiple-choice questions**. They are the fastest
marks on the paper, but the CDC model paper shows what kind of MCQs to expect:
not only "what is the full form of…" but short scenarios, a line of Python
whose output must be worked out, or a choice of the right file format for a
job. This chapter drills those items unit by unit for the five units of the
Python curriculum examined from 2083.

Each section opens with a **facts line** — the results the items in it
actually use — then gives the items, then a key with a one-line reason. Work an
item in under a minute; check it in ten seconds; move on.

::: key The shape of the paper (CDC specification grid, Grade 10)
| Group | Items | Marks each | Total | What it tests |
|---|---|---|---|---|
| A | 10 | 1 | 10 | multiple choice: recall, output of code, choosing a tool or format |
| B | 10 | 2 | 20 | short answers: two differences, a definition with an example, a small program |
| C | 5 | 4 | 20 | long answers, often split [1+3] or [2+2]: explain with examples, programs, scenarios |
| **Total** | **25** | | **50** | **2 hours** |

| Unit | Working hours | Marks | MCQ | Short | Long |
|---|---|---|---|---|---|
| 1. Computer Network and Communication | 14 | 11 | 3 | 2 | 1 |
| 2. Database Management System | 10 | 8 | 2 | 1 | 1 |
| 3. Multimedia | 10 | 8 | 2 | 1 | 1 |
| 4. Programming in Python | 16 | 12 | 2 | 3 | 1 |
| 5. AI and Contemporary Technologies | 14 | 11 | 1 | 3 | 1 |
| **Total** | **64** | **50** | **10** | **10** | **5** |

The grid also asks for about 20% knowledge, 30% understanding, 30% application
and 20% higher-ability questions.
:::

::: caution Practice items, not past questions
Every item below is an original **practice** item written to the CDC pattern.
None is claimed to have appeared in a particular year's paper. Every output of
Python code and every SQL result was produced by actually running the code
(Python 3.12, MySQL 8.4).
:::

```figure caption="Marks carried by each unit in the 50-mark written paper. Programming in Python is the largest single unit; Networking and AI together carry almost half the paper."
fig, ax = barh_ranked(["Programming in Python", "Computer Network and Communication",
                       "AI and Contemporary Technologies", "Database Management System", "Multimedia"],
                      [12, 11, 11, 8, 8], unit=" marks", figsize=(5.0, 2.5),
                      highlight=["Programming in Python"])
ax.set_xlabel("marks out of 50", fontsize=8)
```

## 20.1 Computer Network and Communication

**Facts.** Bandwidth is the maximum data rate of a link, throughput the rate
actually achieved; time = data in bits ÷ rate, and 1 byte = 8 bits. Simplex is
one way, half duplex both ways in turn, full duplex both ways at once. Guided
media: twisted pair (CAT6, 100 m per run), coaxial, optical fibre (light, no
electrical interference); unguided: radio, microwave, infrared, satellite,
Wi-Fi, Bluetooth. RJ-45 is Ethernet (8 pins), RJ-11 telephone, BNC coaxial;
ST, SC, LC and SMA are fibre connectors. A hub copies to every port, a switch
uses MAC addresses, a router joins networks by IP address. A full mesh of n
nodes has n(n−1)/2 links. IPv4 is 32 bits, IPv6 128 bits; 10.x, 172.16–31.x and
192.168.x are private.

1. The maximum amount of data a link can carry each second is its <span class="marks">[1]</span>
   (a) throughput (b) bandwidth (c) latency (d) frequency
2. A 300 MB file is downloaded at a throughput of 40 Mbps. The time taken is <span class="marks">[1]</span>
   (a) 7.5 s (b) 60 s (c) 75 s (d) 120 s
3. Two friends talk on mobile phones, both able to speak at the same moment. The mode is <span class="marks">[1]</span>
   (a) simplex (b) half duplex (c) full duplex (d) broadcast
4. Which medium is not affected by electrical interference? <span class="marks">[1]</span>
   (a) UTP cable (b) coaxial cable (c) optical fibre (d) STP cable
5. The longest single run of CAT6 Ethernet cable allowed is <span class="marks">[1]</span>
   (a) 10 m (b) 100 m (c) 500 m (d) 2 km
6. Which connector is used on coaxial cable for CCTV cameras? <span class="marks">[1]</span>
   (a) RJ-45 (b) RJ-11 (c) BNC (d) LC
7. The square, push-pull connector on most home fibre (FTTH) equipment is <span class="marks">[1]</span>
   (a) ST (b) SC (c) SMA (d) RJ-45
8. Which device forwards data between different networks using IP addresses? <span class="marks">[1]</span>
   (a) hub (b) switch (c) router (d) repeater
9. Which device sends every signal it receives to all its ports? <span class="marks">[1]</span>
   (a) hub (b) switch (c) router (d) bridge
10. How many links does a full mesh of 7 computers need? <span class="marks">[1]</span>
    (a) 7 (b) 14 (c) 21 (d) 42
11. A network spread over the whole Kathmandu Valley is a <span class="marks">[1]</span>
    (a) PAN (b) LAN (c) MAN (d) WAN
12. In which network does every computer act as both client and server? <span class="marks">[1]</span>
    (a) client–server (b) peer-to-peer (c) star (d) WAN
13. Which of these is a private IPv4 address? <span class="marks">[1]</span>
    (a) 172.20.4.1 (b) 172.40.4.1 (c) 8.8.4.4 (d) 1.1.1.1
14. Which command shows the IP address and default gateway of a Windows computer? <span class="marks">[1]</span>
    (a) ping (b) ipconfig (c) nslookup (d) tracert
15. A company's portal that only its own staff can open is an <span class="marks">[1]</span>
    (a) Internet (b) intranet (c) extranet (d) MAN

::: note Answers to 20.1
**1.** (b) — throughput is the rate actually achieved.
**2.** (b) — 300 × 8 = 2,400 Mb, and 2,400 ÷ 40 = 60 s.
**3.** (c) — both directions at the same time.
**4.** (c) — fibre carries light, not electricity.
**5.** (b) — 100 m; longer links need fibre or a switch in between.
**6.** (c) — the bayonet BNC plug fits coaxial cable.
**7.** (b) — SC is square and push-pull; ST is round and twist-lock.
**8.** (c) — routers read IP addresses and choose a path.
**9.** (a) — a hub repeats to all ports; a switch sends to one.
**10.** (c) — 7 × 6 ÷ 2 = 21.
**11.** (c) — a city or valley network is a MAN.
**12.** (b) — peers are equal.
**13.** (a) — 172.16 to 172.31 is private; 172.40 is outside it.
**14.** (b) — ipconfig; ping only tests whether a host replies.
**15.** (b) — staff-only means intranet; outsiders with access make it an extranet.
:::

::: caution Bits and bytes in Group A
Item 2 is the one most often missed: the file is in megabytes, the speed in
mega**bits**. Multiply the file size by 8 before dividing.
:::

## 20.2 Database Management System

**Facts.** Data are raw facts; information is processed data. A DBMS (MySQL)
manages a database; an RDBMS keeps it in tables linked by keys. Types: INT,
DECIMAL(p, s) for money, VARCHAR(n) for names, CHAR(n) fixed, DATE written
'YYYY-MM-DD'. A field is a column, a record a row. Primary key: unique, never
NULL, one per table; foreign key: refers to another table's primary key;
composite key: two or more fields. Relationships: 1 : 1, 1 : M, M : N (through a
junction table). DDL — CREATE, ALTER, DROP, TRUNCATE; DML — INSERT, SELECT,
UPDATE, DELETE. WHERE filters rows, ORDER BY sorts (ascending by default), LIKE
matches patterns with % (any characters) and _ (one character).

1. "The class average in Computer is 72" is an example of <span class="marks">[1]</span>
   (a) data (b) information (c) a field (d) a key
2. Software that creates and manages databases is called <span class="marks">[1]</span>
   (a) a spreadsheet (b) a DBMS (c) a compiler (d) a browser
3. The best data type for a price such as 545.50 is <span class="marks">[1]</span>
   (a) INT (b) DECIMAL(7,2) (c) DATE (d) CHAR(2)
4. In MySQL a DATE value is written as <span class="marks">[1]</span>
   (a) '15-04-2026' (b) '2026/15/04' (c) '2026-04-15' (d) 2026.04.15
5. A column of a table is also called a <span class="marks">[1]</span>
   (a) record (b) field (c) row (d) query
6. In the table `borrow(roll, book_no, issue_date)` a student may borrow many books. Which can be the primary key? <span class="marks">[1]</span>
   (a) roll (b) issue_date (c) (roll, book_no) (d) book_no alone
7. A foreign key <span class="marks">[1]</span>
   (a) must be unique (b) refers to the primary key of another table (c) can never repeat (d) is always the first column
8. One district has many schools and each school is in one district. The relationship is <span class="marks">[1]</span>
   (a) one-to-one (b) one-to-many (c) many-to-many (d) none
9. Which of these is a DDL command? <span class="marks">[1]</span>
   (a) INSERT (b) UPDATE (c) ALTER (d) SELECT
10. Which command removes a table together with its structure? <span class="marks">[1]</span>
    (a) DELETE (b) TRUNCATE (c) DROP (d) ALTER
11. The prices in table `items` are 20, 60, 1200, 10 and 35. How many rows does `SELECT * FROM items WHERE price > 30;` return? <span class="marks">[1]</span>
    (a) 2 (b) 3 (c) 4 (d) 5
12. `WHERE name LIKE '%a'` selects names that <span class="marks">[1]</span>
    (a) start with a (b) end with a (c) contain only a (d) have a as the second letter
13. If neither ASC nor DESC is written, ORDER BY sorts <span class="marks">[1]</span>
    (a) in descending order (b) in ascending order (c) at random (d) in the order of entry
14. Which command changes data already stored in a table? <span class="marks">[1]</span>
    (a) ALTER (b) UPDATE (c) INSERT (d) CREATE
15. MySQL Workbench is <span class="marks">[1]</span>
    (a) a Python editor (b) a graphical tool for writing and running SQL (c) a web browser (d) a spreadsheet

::: note Answers to 20.2
**1.** (b) — it is processed and meaningful.
**2.** (b) — e.g. MySQL, Oracle.
**3.** (b) — exact decimals with 2 places.
**4.** (c) — year, month, day in quotes.
**5.** (b) — field = column; record = row.
**6.** (c) — neither roll nor book_no is unique alone, the pair is.
**7.** (b) — it links to another table's primary key and may repeat.
**8.** (b) — one district, many schools.
**9.** (c) — ALTER changes structure; the others are DML.
**10.** (c) — DROP removes structure and data; TRUNCATE keeps the structure.
**11.** (b) — 60, 1,200 and 35 are above 30 (tested: Copy, Bag, Ruler).
**12.** (b) — % first, then a at the end.
**13.** (b) — ASC is the default.
**14.** (b) — UPDATE … SET … WHERE.
**15.** (b) — the GUI for MySQL.
:::

## 20.3 Multimedia

**Facts.** Multimedia combines text, graphics, audio, video and animation. TXT
stores plain text, RTF and DOCX formatted text, PDF a fixed layout. Raster images
are pixels (JPG lossy, PNG lossless with transparency, GIF 256 colours and
animation, BMP uncompressed); vector images are mathematical shapes (SVG) that
stay sharp. Amplitude is loudness, frequency is pitch; audio size = sampling
rate × bit depth × channels × seconds (÷ 8 for bytes); WAV is uncompressed,
MP3 and AAC are compressed. Frames shown per second = frame rate; SD 720 × 480,
HD 1280 × 720, FHD 1920 × 1080, 4K 3840 × 2160; MP4 = MPEG-4 Part 14, MOV is
Apple's, AVI Microsoft's. Keyframe animation lets the software make the
in-between frames (tweens).

1. Which one is NOT an element of multimedia? <span class="marks">[1]</span>
   (a) animation (b) audio (c) router (d) text
2. Which text format keeps fonts and colours and opens in almost any word processor? <span class="marks">[1]</span>
   (a) TXT (b) RTF (c) CSV (d) MP3
3. An image 800 pixels wide and 600 pixels high contains <span class="marks">[1]</span>
   (a) 1,400 pixels (b) 48,000 pixels (c) 480,000 pixels (d) 4,800,000 pixels
4. Which graphic stays sharp when enlarged to billboard size? <span class="marks">[1]</span>
   (a) a JPEG photo (b) a vector drawing (c) a BMP image (d) a GIF
5. A logo is needed with a transparent background and no loss of detail. Choose <span class="marks">[1]</span>
   (a) JPG (b) PNG (c) BMP (d) MP4
6. A GIF image can contain at most <span class="marks">[1]</span>
   (a) 16 colours (b) 256 colours (c) 65,536 colours (d) 16.7 million colours
7. The pitch of a sound depends on its <span class="marks">[1]</span>
   (a) amplitude (b) frequency (c) file name (d) number of channels
8. One second of mono, 8-bit sound sampled at 8,000 Hz needs <span class="marks">[1]</span>
   (a) 1,000 bytes (b) 8,000 bytes (c) 64,000 bytes (d) 128,000 bytes
9. Which audio format stores sound without compression? <span class="marks">[1]</span>
   (a) MP3 (b) AAC (c) WAV (d) OGG
10. A 5-second animation at 24 fps contains <span class="marks">[1]</span>
    (a) 29 frames (b) 60 frames (c) 120 frames (d) 240 frames
11. The HD resolution is <span class="marks">[1]</span>
    (a) 720 × 480 (b) 1280 × 720 (c) 1920 × 1080 (d) 3840 × 2160
12. MP4 stands for <span class="marks">[1]</span>
    (a) Media Player 4 (b) MPEG-4 Part 14 (c) Multi Picture 4 (d) Motion Picture 4
13. In keyframe animation, the frames between two keyframes are <span class="marks">[1]</span>
    (a) drawn by hand (b) created by the software (c) deleted (d) stored as text
14. Which program is used to cut, arrange and export video clips on a timeline? <span class="marks">[1]</span>
    (a) Audacity (b) CapCut (c) Notepad (d) MySQL

::: note Answers to 20.3
**1.** (c) — a router is network hardware.
**2.** (b) — Rich Text Format.
**3.** (c) — 800 × 600 = 480,000.
**4.** (b) — vectors are redrawn at any size.
**5.** (b) — PNG is lossless with transparency.
**6.** (b) — GIF uses a palette of 256 colours.
**7.** (b) — frequency sets pitch; amplitude sets loudness.
**8.** (b) — 8,000 × 8 × 1 × 1 = 64,000 bits = 8,000 bytes.
**9.** (c) — WAV stores the raw samples.
**10.** (c) — 24 × 5 = 120.
**11.** (b) — 1920 × 1080 is Full HD.
**12.** (b) — the MP4 container standard.
**13.** (b) — tweening is automatic.
**14.** (b) — CapCut is a video editor; Audacity edits sound.
:::

## 20.4 Programming in Python

**Facts.** `//` is floor division, `%` the remainder, `/` always a float;
`range(start, stop, step)` stops before `stop`; `input()` returns a string. A
function is defined with `def`, default parameters come last, and a function
with no `return` gives None. `import math`, `from math import sqrt`,
`import pandas as pd`; `random.randint(a, b)` includes both ends. A regular
n-gon needs turns of 360° ÷ n. `10 / 0` raises ZeroDivisionError, `int("abc")`
ValueError; `finally` always runs. File modes: r (read), w (overwrite), a
(append), x (new file only). pandas: `df.shape` is (rows, columns),
`df[df["Marks"] > 80]` filters. Line charts show trends, bar charts compare,
pie charts show parts of a whole.

1. What does `print(7 // 2 + 7 % 2)` display? <span class="marks">[1]</span>
   (a) 3 (b) 3.5 (c) 4 (d) 4.5
2. Which of these is NOT a valid identifier? <span class="marks">[1]</span>
   (a) total_marks (b) _count (c) 2nd_term (d) marks2
3. After `x = 5`, `x += 3` and `x *= 2`, the value of x is <span class="marks">[1]</span>
   (a) 10 (b) 13 (c) 16 (d) 26
4. `for i in range(2, 10, 3): print(i, end=" ")` displays <span class="marks">[1]</span>
   (a) 2 5 8 (b) 2 5 8 11 (c) 3 6 9 (d) 2 4 6 8
5. With `def f(a, b=4): return a * b`, the call `f(3)` returns <span class="marks">[1]</span>
   (a) 7 (b) 12 (c) 3 (d) an error
6. A function that has no return statement returns <span class="marks">[1]</span>
   (a) 0 (b) an empty string (c) None (d) False
7. Which statement imports only the sqrt function from math? <span class="marks">[1]</span>
   (a) import sqrt (b) from math import sqrt (c) import math.sqrt (d) from sqrt import math
8. `random.randint(1, 3)` can never return <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) 4
9. After `import math`, `print(math.floor(7.9), math.ceil(7.1))` displays <span class="marks">[1]</span>
   (a) 7 8 (b) 8 7 (c) 7 7 (d) 8 8
10. To draw a regular pentagon, the turtle must turn at each corner by <span class="marks">[1]</span>
    (a) 60° (b) 72° (c) 90° (d) 108°
11. `print(10 / 0)` raises <span class="marks">[1]</span>
    (a) ValueError (b) TypeError (c) ZeroDivisionError (d) NameError
12. Which file mode raises an error if the file already exists? <span class="marks">[1]</span>
    (a) "r" (b) "w" (c) "a" (d) "x"
13. A DataFrame `df` has 8 rows and 7 columns. `df.shape` is <span class="marks">[1]</span>
    (a) 56 (b) (7, 8) (c) (8, 7) (d) [8, 7]
14. Which expression selects the rows whose Marks are more than 80? <span class="marks">[1]</span>
    (a) df["Marks" > 80] (b) df[df["Marks"] > 80] (c) df.Marks(80) (d) df.select(Marks > 80)
15. Which chart best shows the share of each expense in a family's monthly budget? <span class="marks">[1]</span>
    (a) line chart (b) scatter plot (c) pie chart (d) histogram

::: note Answers to 20.4
**1.** (c) — 7 // 2 = 3 and 7 % 2 = 1, so 4 (tested).
**2.** (c) — an identifier cannot start with a digit.
**3.** (c) — 5 + 3 = 8, then 8 × 2 = 16.
**4.** (a) — start 2, step 3, stop before 10 (tested: 2 5 8).
**5.** (b) — b takes its default 4, so 3 × 4 = 12.
**6.** (c) — Python returns None.
**7.** (b) — `from module import name`.
**8.** (d) — randint stays between 1 and 3 inclusive.
**9.** (a) — floor rounds down, ceil rounds up.
**10.** (b) — 360° ÷ 5 = 72°.
**11.** (c) — division by zero.
**12.** (d) — "x" creates only a new file.
**13.** (c) — (rows, columns) as a tuple.
**14.** (b) — the condition goes inside `df[ ]`.
**15.** (c) — parts of one whole.
:::

::: tip Output questions: trace, do not guess
For any "what is the output" item, write the variables down the margin and
update them line by line. Two seconds of tracing beats choosing the option that
"looks right" — items 1, 3 and 4 above are built to catch guessers.
:::

## 20.5 AI and Contemporary Technologies

**Facts.** Every AI in use today is narrow AI; ML learns from data. Supervised
learning uses labelled data, unsupervised finds groups in unlabelled data,
reinforcement learns from rewards. Robots sense (sensors), think (controller)
and act (actuators). LLMs write by predicting the next token; image generators
remove noise step by step; false but confident output is hallucination. AI
ethics: bias, privacy, security; reduce bias with diverse data. IoT: things
with sensors that share data and act. VR replaces reality, AR adds to it. Cloud
models: IaaS (servers), PaaS (platform), SaaS (ready software). e-Commerce
(Daraz), e-governance (Nagarik App: G2C), e-education (Sikai Chautari).

1. Chatbots and face unlock are examples of <span class="marks">[1]</span>
   (a) narrow AI (b) general AI (c) super AI (d) self-aware AI
2. Grouping customers by their shopping habits, with no groups given in advance, is <span class="marks">[1]</span>
   (a) supervised learning (b) unsupervised learning (c) reinforcement learning (d) manual entry
3. An agent that learns from rewards and penalties uses <span class="marks">[1]</span>
   (a) supervised learning (b) unsupervised learning (c) reinforcement learning (d) no learning
4. The part of a robot that measures the distance to an obstacle is a <span class="marks">[1]</span>
   (a) sensor (b) actuator (c) gripper (d) prompt
5. A large language model writes an answer by <span class="marks">[1]</span>
   (a) copying a whole web page (b) predicting the next token again and again (c) looking up a dictionary (d) asking a human
6. An AI image generator usually begins with <span class="marks">[1]</span>
   (a) a photograph (b) random noise (c) a pencil sketch (d) an MP3 file
7. When an AI tool states a false fact confidently, it is called <span class="marks">[1]</span>
   (a) encryption (b) hallucination (c) tweening (d) streaming
8. Submitting an AI-written essay as your own work breaks the rule of <span class="marks">[1]</span>
   (a) privacy (b) academic honesty (c) bandwidth (d) cloud storage
9. Training an AI on data from only one group of people mainly causes <span class="marks">[1]</span>
   (a) bias (b) faster speed (c) better privacy (d) lower cost
10. A street light that switches itself off when no one is nearby is an example of <span class="marks">[1]</span>
    (a) IoT (b) VR (c) SaaS (d) e-commerce
11. A game that shows creatures on the real street through a phone camera uses <span class="marks">[1]</span>
    (a) virtual reality (b) augmented reality (c) IaaS (d) a PAN
12. Renting virtual servers from Amazon EC2 is <span class="marks">[1]</span>
    (a) SaaS (b) PaaS (c) IaaS (d) e-governance
13. The Nagarik App is an example of <span class="marks">[1]</span>
    (a) e-commerce (b) G2C e-governance (c) e-education (d) virtual reality
14. Daraz is an example of <span class="marks">[1]</span>
    (a) B2C e-commerce (b) G2G e-governance (c) PaaS (d) an intranet

::: note Answers to 20.5
**1.** (a) — each does one task well; general AI does not exist yet.
**2.** (b) — the groups are discovered, not taught.
**3.** (c) — learning from reward is reinforcement.
**4.** (a) — sensors measure; actuators move.
**5.** (b) — next-token prediction, one token at a time.
**6.** (b) — diffusion models remove noise step by step.
**7.** (b) — hallucination.
**8.** (b) — use AI to learn, not to do the work.
**9.** (a) — the AI copies the imbalance in its data.
**10.** (a) — a sensing, connected, acting object.
**11.** (b) — digital images added to the real view.
**12.** (c) — raw infrastructure on rent.
**13.** (b) — government to citizen.
**14.** (a) — business to consumer.
:::

## Chapter summary

- Group A is **10 × 1** marks: three from Networking, two each from DBMS,
  Multimedia and Python, one from AI. Give each item under a minute.
- **Networking**: time = bits ÷ rate (bytes × 8); hub/switch/router by what
  they read (nothing/MAC/IP); mesh n(n−1)/2; IPv4 32-bit, IPv6 128-bit; private
  10.x, 172.16–31.x, 192.168.x.
- **DBMS**: primary key unique and not NULL; foreign key refers to another
  table's primary key; DDL changes structure, DML changes data; LIKE with % and _.
- **Multimedia**: raster pixels vs vector shapes; PNG transparent and lossless,
  JPG lossy, GIF 256 colours; audio bytes = rate × bits × channels × seconds ÷ 8;
  frames = fps × seconds.
- **Python**: trace output line by line; `//`, `%`, range stops before the end;
  default parameters last; None from a function with no return; df.shape is
  (rows, columns).
- **AI**: supervised (labels), unsupervised (groups), reinforcement (rewards);
  hallucination and bias; IoT, AR/VR, IaaS/PaaS/SaaS, G2C and B2C.

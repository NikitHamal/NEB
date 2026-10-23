---
subject: Question Bank
grade: 10
unit: 22
title: "Computer Science: Model Question Sets and Predicted Questions"
hours: 0
area: Computer Science
---

This chapter does three jobs. It sets out the **specification grid** of the
new SEE Computer Science paper and what it means for your preparation; it gives
**two complete model papers**, each of 50 marks and two hours, built exactly to
the grid, with a full answer to every question; and it closes with a **ranked
list of practice priorities**, each with the reason it holds its place. Every
program and SQL query in the answers was run (Python 3.12, MySQL 8.4).

::: caution What "predicted" means here, and what it does not
Nobody outside the examination board knows next year's questions. The ranks in
section 22.4 rest on public facts only: the **CDC specification grid** (how
many questions of each kind each unit carries), the **CDC model question** that
accompanies it, and the **syllabus**. A high rank means *practise this first*,
never *this will come*. All the questions below are original practice items,
not copies of any past or model paper.
:::

::: key The grid: 50 marks in 2 hours
| Group | Questions | Marks each | Total | What it asks for |
|---|---|---|---|---|
| A | 10 | 1 | 10 | multiple choice |
| B | 10 | 2 | 20 | short answers: two points, a small program, a calculation |
| C | 5 | 4 | 20 | long answers, often [1+3] or [2+2] |
| **Total** | **25** | | **50** | |

| Unit | MCQ | Short | Long | Marks |
|---|---|---|---|---|
| 1. Computer Network and Communication | 3 | 2 | 1 | 11 |
| 2. Database Management System | 2 | 1 | 1 | 8 |
| 3. Multimedia | 2 | 1 | 1 | 8 |
| 4. Programming in Python | 2 | 3 | 1 | 12 |
| 5. AI and Contemporary Technologies | 1 | 3 | 1 | 11 |

Internal assessment adds **50 more marks**: practical and project work 35,
participation 5 and terminal examinations 10.
:::

## 22.1 What the grid implies

```figure caption="Marks against time in the two-hour paper. Group A is a fifth of the marks and should take about a tenth of the time; the forty marks of Groups B and C deserve most of the two hours."
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
groups = ["A", "B", "C", "check"]
marks = [10, 20, 20, 0]
minutes = [12, 45, 50, 13]
cols = [MUTED, ACCENT, SERIES[3], SERIES[2]]
a1.bar(groups[:3], marks[:3], color=cols[:3], width=0.6)
for i, m in enumerate(marks[:3]):
    a1.text(i, m + 0.6, str(m), ha="center", fontsize=8, color=INK)
a1.set_title("marks (of 50)", fontsize=8.5, color=INK)
a1.set_ylim(0, 25)
a2.bar(groups, minutes, color=cols, width=0.6)
for i, m in enumerate(minutes):
    a2.text(i, m + 1.2, str(m), ha="center", fontsize=8, color=INK)
a2.set_title("minutes (of 120)", fontsize=8.5, color=INK)
a2.set_ylim(0, 60)
for ax in (a1, a2):
    ax.tick_params(labelsize=8, length=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
fig.tight_layout()
```

Four things follow from the grid.

1. **Python is the largest unit (12 marks) and the most practical.** Three short
   questions and one long question are Python — expect to write a function, a
   try-except block and to read or modify a pandas program.
2. **Most AI marks are written answers.** Unit 5 has only one MCQ but three short
   questions and a long one: definitions with examples, ethical issues with
   safeguards, IoT and cloud applications to a situation.
3. **Networking has the most MCQs (three).** Its facts — devices, media,
   connectors, IP addresses, commands — are cheap marks if they are memorised.
4. **Every unit has exactly one long question.** No unit can be skipped.

The grid also fixes the **thinking levels**: about 20% knowledge (10 marks), 30%
understanding (15), 30% application (15) and 20% higher ability (10), within
two marks either way. Higher-ability marks come from scenarios — "a school
wants…", "suggest…", "modify the program to…".

::: tip A clock that fits two hours
Group A: **12 minutes** (70 seconds an item). Group B: **45 minutes** (4½ minutes
a question). Group C: **50 minutes** (10 minutes a question). That leaves
**13 minutes** to check program indentation, SQL semicolons and quotes, units
in calculations, and that all 25 question numbers are written.
:::

## 22.2 Model Set 1

**Optional Computer Science — Class 10. Time: 2 hours. Full marks: 50.**
**Give answers in your own words as far as practicable.**

### Question paper

**Group A — Choose the correct answer. [10 × 1 = 10]**

1. Which mode of communication does a television broadcast use?
   (a) simplex (b) half duplex (c) full duplex (d) duplex
2. Which device connects a school's LAN to the Internet and acts as its default gateway?
   (a) hub (b) switch (c) router (d) repeater
3. Which of these is a valid IPv4 address?
   (a) 192.168.1.256 (b) 10.0.0.1 (c) 172.16.300.1 (d) 2001:db8::1
4. Which SQL command adds a new column to an existing table?
   (a) INSERT (b) ALTER (c) UPDATE (d) CREATE
5. Which constraint stops two students from having the same symbol number but allows the value to be missing?
   (a) PRIMARY KEY (b) UNIQUE (c) DEFAULT (d) CHECK
6. A club wants to post a short looping animated sticker. Which format should it use?
   (a) GIF (b) WAV (c) TXT (d) MP3
7. The colour of one dot of a raster image is stored in a
   (a) frame (b) pixel (c) vector (d) layer
8. What does `print(type(8 / 2))` display?
   (a) <class 'int'> (b) <class 'float'> (c) 4 (d) 4.0
9. `marks = int(input())` crashes when the user types "abc". Which block should handle this?
   (a) except ValueError (b) except ZeroDivisionError (c) else (d) finally
10. A spam filter that learns from emails marked "spam" or "not spam" uses
    (a) supervised learning (b) unsupervised learning (c) reinforcement learning (d) no learning

**Group B — Answer the following questions briefly. [10 × 2 = 20]**

11. Write two differences between a LAN and a WAN.
12. A 900 MB video is downloaded at a throughput of 30 Mbps. How long does it take?
13. What is a foreign key? Explain with an example.
14. Write two differences between the WAV and MP3 audio formats.
15. Write a Python function `cube(n)` that returns the cube of n, and call it with 4.
16. Write the output of the following program.

```python
for i in range(5, 0, -2):
    print(i, end=" ")
```

17. Why should a file be closed after use? Write the statement that opens `marks.txt` so that new lines are added at the end.
18. What is generative AI? Name two generative AI tools.
19. Write any two features of cloud computing.
20. What is augmented reality? Write one use of it in education.

**Group C — Answer the following questions in detail. [5 × 4 = 20]**

21. Explain star and mesh topologies with diagrams. Which would you choose for a computer lab of 40 computers, and why? [3+1]
22. A stationery shop keeps `products(pid, pname, price, stock)`. Write SQL to (a) create the table with pid as primary key; (b) insert the product 6, "Pencil box", Rs 180, 25 in stock; (c) display the name and price of products costing Rs 100 to Rs 500, cheapest first; (d) delete the products that are out of stock. [4]
23. What is animation? Write two differences between 2D and 3D animation, and explain keyframe animation. [1+2+1]
24. Study the program and answer the questions. [2+2]

```python
marks = [45, 78, 32, 90, 66]
count = 0
for m in marks:
    if m >= 40:
        count += 1
print("Passed:", count)
```

(a) Write the output. (b) Modify the program so that it also prints the average mark of the students who passed.

25. What is the Internet of Things? Explain its main components and two applications in a smart city. [2+2]

### Solutions

::: note Group A — answers with reasons
**1.** (a) — the station sends and viewers only receive.
**2.** (c) — a router joins networks and is the way out of the LAN.
**3.** (b) — each octet must be 0–255, and (d) is an IPv6 address.
**4.** (b) — ALTER TABLE … ADD changes the structure.
**5.** (b) — UNIQUE forbids repeats but allows NULL; a primary key allows neither.
**6.** (a) — GIF stores simple animation.
**7.** (b) — a pixel is one picture element.
**8.** (b) — `/` always gives a float, here 4.0.
**9.** (a) — `int("abc")` raises ValueError.
**10.** (a) — the training data are labelled.
:::

::: note Group B — answers
**11.** A LAN covers a small area such as a room, building or campus; a WAN covers
a country or the whole world. A LAN is owned by one organisation and is very
fast; a WAN uses links of many organisations and is slower with more delay.

**12.** 900 MB × 8 = 7,200 Mb; 7,200 ÷ 30 = **240 s = 4 minutes**.

**13.** A foreign key is a field in one table that refers to the primary key of
another table, linking the two. Example: `roll` in `marks(roll, subject, marks)`
refers to `roll` in `students`, so marks can be stored only for existing
students.

**14.** WAV is uncompressed, so it keeps the exact recording but makes large files;
MP3 is compressed (lossy), so files are about ten times smaller with slight loss
of quality. WAV is used for recording and editing, MP3 for sharing and playing.

**15.**
```python
def cube(n):
    return n ** 3

print(cube(4))
```
Output: `64`.

**16.** `range(5, 0, -2)` counts down from 5 in steps of 2 and stops before 0:
output **5 3 1**.

**17.** Closing saves any data still in memory to the disk and frees the file
for other programs. `f = open("marks.txt", "a")`.

**18.** Generative AI is AI that creates new content — text, images, music, video
or code — from a prompt. Tools: ChatGPT and Gemini (also Copilot, DALL·E).

**19.** On-demand access from anywhere over the Internet; scalability — resources
grow or shrink as needed (also pay-as-you-go, automatic backup and updates).

**20.** AR adds digital images or information on top of the real world seen
through a phone or glasses. In education, pointing a phone at a textbook picture
can show a 3D model of the heart or the solar system.
:::

::: note Group C — answers
**21.** *Star*: every computer is joined by its own cable to a central switch
(sketch: a switch with computers around it); one faulty cable affects only one
computer and faults are easy to find, but if the switch fails all stop. *Mesh*:
computers are joined by many links, in a full mesh each to every other (sketch:
five computers with all ten links); data has other paths if one fails, but it
needs n(n−1)/2 cables — 780 for 40 computers. For a 40-computer lab choose the
**star**: one 48-port switch and 40 cables are cheap, easy to install and easy
to troubleshoot.

**22.**
```sql
CREATE TABLE products (
    pid   INT PRIMARY KEY,
    pname VARCHAR(30) NOT NULL,
    price DECIMAL(8, 2),
    stock INT DEFAULT 0
);
INSERT INTO products (pid, pname, price, stock) VALUES (6, 'Pencil box', 180, 25);
SELECT pname, price FROM products WHERE price BETWEEN 100 AND 500 ORDER BY price;
DELETE FROM products WHERE stock = 0;
```
With five more products in the table, the SELECT returned Notebook 120.00,
Pencil box 180.00, Geometry box 280.00 and Water bottle 350.00, and the DELETE
removed the water bottle (stock 0): `1 row affected`.

**23.** Animation is the illusion of movement created by showing slightly
different pictures quickly one after another (1). 2D animation is flat (width
and height) and usually drawn; 3D animation has depth and is modelled, rigged
and rendered, needing more time and computing power (2). In keyframe animation
the animator sets only the key positions and the software calculates the
in-between frames (tweens) (1).

**24.** (a) Four marks (45, 78, 90, 66) are 40 or more: output `Passed: 4`.
(b)
```python
marks = [45, 78, 32, 90, 66]
count = 0
total = 0
for m in marks:
    if m >= 40:
        count += 1
        total += m
print("Passed:", count)
print("Average of passed students:", total / count)
```
```text
Passed: 4
Average of passed students: 69.75
```

**25.** IoT is the network of everyday objects fitted with sensors, software and
Internet connections that collect and share data and act on it (1). Components:
sensors, a microcontroller or device, a network connection, a cloud server,
an app and actuators (1). Smart-city applications: traffic lights that adjust to
the number of vehicles, reducing jams; street lights that dim or switch off when
roads are empty, saving electricity (also full-bin alerts, smart parking)
(1 + 1).
:::

| Question | 1–3 | 4–5 | 6–7 | 8–9 | 10 | 11–12 | 13 | 14 | 15–17 | 18–20 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Unit | 1 | 2 | 3 | 4 | 5 | 1 | 2 | 3 | 4 | 5 | 1 | 2 | 3 | 4 | 5 |

## 22.3 Model Set 2

**Optional Computer Science — Class 10. Time: 2 hours. Full marks: 50.**
**Give answers in your own words as far as practicable.**

### Question paper

**Group A — Choose the correct answer. [10 × 1 = 10]**

1. Which cable carries data as pulses of light?
   (a) CAT6 (b) coaxial (c) optical fibre (d) STP
2. Which protocol gives devices their IP addresses automatically?
   (a) DNS (b) DHCP (c) FTP (d) HTTP
3. A phone, a smartwatch and wireless earbuds connected together form a
   (a) PAN (b) LAN (c) MAN (d) WAN
4. The most suitable MySQL data type for a student's name is
   (a) INT (b) VARCHAR(40) (c) DATE (d) BOOLEAN
5. `SELECT name FROM students ORDER BY name DESC;` lists the names
   (a) from A to Z (b) from Z to A (c) at random (d) in the order entered
6. Which resolution is called Full HD?
   (a) 1280 × 720 (b) 1920 × 1080 (c) 720 × 480 (d) 3840 × 2160
7. Which program is used to record and edit sound?
   (a) Audacity (b) Canva (c) Pixlr (d) Excel
8. Which pandas function reads a CSV file into a DataFrame?
   (a) pd.open_csv() (b) pd.read_csv() (c) pd.load() (d) pd.csv()
9. Which pair of turtle methods must surround the drawing of a shape to fill it with colour?
   (a) penup() and pendown() (b) begin_fill() and end_fill() (c) hideturtle() and showturtle() (d) left() and right()
10. Gmail used in a web browser is an example of
    (a) IaaS (b) PaaS (c) SaaS (d) on-premises software

**Group B — Answer the following questions briefly. [10 × 2 = 20]**

11. What is a protocol? Name two protocols with their uses.
12. Write two functions of a router.
13. Write an SQL statement to display all records from `employee(eid, name, salary)` whose name ends with "sh".
14. What is the resolution of an image? How does it affect the file size?
15. Write a Python program that reads a number and prints whether it is odd or even.
16. Write a program that divides 100 by a number entered by the user, using try-except to handle division by zero.
17. What is the difference between `import math` and `from math import sqrt`? Show how the square root of 49 is found with each.
18. Write two ethical issues of AI with an example of each.
19. Differentiate between e-commerce and e-governance with one Nepali example of each.
20. What is a robot? Write two uses of robots in hospitals.

**Group C — Answer the following questions in detail. [5 × 4 = 20]**

21. What are guided media? Explain their types, and write two differences between twisted-pair cable and optical fibre. [2+2]
22. What is a relationship in a database? Explain the one-to-many relationship with an example, and write SQL to create two tables linked by a foreign key for it. [1+1+2]
23. A 2-minute song is recorded in stereo at 44.1 kHz and 16 bits. Find its size as a WAV file and as a 192 kbps MP3, and say which you would upload to a website. [2+1+1]
24. Study the program and answer the questions. [2+2]

```python
import pandas as pd
df = pd.DataFrame({"Name": ["Ram", "Sita", "Gopal", "Rita"],
                   "Age": [15, 16, 15, 17],
                   "Marks": [72, 88, 54, 91]})
print(df[df["Age"] == 15])
```

(a) Write the output. (b) Modify the last line to show only the Name and Marks of students who scored more than 80.

25. A school wants to use cloud computing. Explain IaaS, PaaS and SaaS with an example each, and say which the school should use to share notes with students. [3+1]

### Solutions

::: note Group A — answers with reasons
**1.** (c) — fibre carries light.
**2.** (b) — the Dynamic Host Configuration Protocol.
**3.** (a) — devices around one person form a PAN.
**4.** (b) — names are text of varying length.
**5.** (b) — DESC means descending, Z to A.
**6.** (b) — 1920 × 1080 is Full HD; 1280 × 720 is HD.
**7.** (a) — Audacity is a free audio editor.
**8.** (b) — `pd.read_csv("file.csv")`.
**9.** (b) — the fill colour is applied between them.
**10.** (c) — ready software used online is SaaS.
:::

::: note Group B — answers
**11.** A protocol is a set of rules that devices follow to communicate over a
network. HTTP/HTTPS transfers web pages; SMTP sends email (also DHCP, DNS,
FTP).

**12.** It joins different networks, such as a LAN and the Internet; and it
chooses the best path for each packet using IP addresses (also NAT, DHCP and
firewall in a home router).

**13.**
```sql
SELECT * FROM employee WHERE name LIKE '%sh';
```
On four sample rows it returned Ramesh and Mahesh.

**14.** Resolution is the number of pixels in an image, width × height, such as
1920 × 1080. More pixels show more detail but need more storage: an uncompressed
24-bit image needs width × height × 3 bytes, so doubling both width and height
makes the file four times bigger.

**15.**
```python
n = int(input("Enter a number: "))
if n % 2 == 0:
    print(n, "is even")
else:
    print(n, "is odd")
```
With 17: `17 is odd`; with 24: `24 is even`.

**16.**
```python
try:
    n = float(input("Enter a number: "))
    print("100 divided by", n, "is", 100 / n)
except ZeroDivisionError:
    print("Cannot divide by zero.")
```
With 8: `100 divided by 8.0 is 12.5`; with 0: `Cannot divide by zero.`

**17.** `import math` loads the whole module, so its functions are called with
the module name: `math.sqrt(49)`. `from math import sqrt` loads only sqrt, which
is then called directly: `sqrt(49)`. Both give 7.0.

**18.** *Bias* — a hiring system trained mostly on men's CVs may reject women;
*privacy* — face-recognition cameras may record people without their consent
(also security: a hacked self-driving car).

**19.** e-Commerce is buying and selling over the Internet, e.g. Daraz;
e-governance is the government giving services and information online, e.g. the
Nagarik App or online passport applications.

**20.** A robot is a programmable machine that senses its surroundings, decides
and acts. In hospitals: robot-assisted surgery with tiny precise movements; and
delivering medicines or disinfecting rooms (also helping patients move).
:::

::: note Group C — answers
**21.** Guided media are communication media that carry signals along a physical
cable (1). Types: *twisted pair* (pairs of copper wires twisted to reduce
interference; CAT6 in LANs), *coaxial cable* (copper core, insulator, braided
shield; cable TV, CCTV) and *optical fibre* (light in a glass core; ISP
backbones) (1). Differences: twisted pair carries electrical signals and is
limited to 100 m per run, while fibre carries light for tens of kilometres;
twisted pair is cheap and easy to fit but affected by interference, while fibre
is costlier but immune to electrical noise and much faster (2).

**22.** A relationship is a logical link between two tables through a common key
field (1). One-to-many: one record in the first table matches many in the
second, each of which matches only one — e.g. one teacher teaches many classes
(1).
```sql
CREATE TABLE teachers (tid INT PRIMARY KEY, tname VARCHAR(40) NOT NULL);
CREATE TABLE classes (
    class_id VARCHAR(5) PRIMARY KEY,
    room     VARCHAR(10),
    tid      INT,
    FOREIGN KEY (tid) REFERENCES teachers(tid)
);
```
Tested: classes 9A, 10A (both teacher 1) and 10B (teacher 2) were accepted, and a
class for a non-existent teacher 7 was refused with error 1452 (2).

**23.** WAV: 44,100 × 16 × 2 × 120 = 169,344,000 bits; ÷ 8 = **21,168,000 bytes ≈
21.2 MB** (2). MP3: 192,000 × 120 = 23,040,000 bits; ÷ 8 = **2,880,000 bytes ≈
2.9 MB** (1). Upload the **MP3**: about seven times smaller, so it loads and
streams quickly, with quality that is very close to the original (1).

**24.** (a)
```text
    Name  Age  Marks
0    Ram   15     72
2  Gopal   15     54
```
(b)
```python
print(df[df["Marks"] > 80][["Name", "Marks"]])
```
```text
   Name  Marks
1  Sita     88
3  Rita     91
```

**25.** *IaaS* provides virtual servers, storage and networks that the user's IT
staff manage, e.g. Amazon EC2; *PaaS* provides a ready platform to build and run
applications, e.g. Google App Engine; *SaaS* provides complete applications used
online, e.g. Google Docs and Gmail (3). To share notes the school should use
**SaaS** such as Google Drive or Google Classroom: nothing to install, students
open the notes on any device, and the provider handles storage and backup (1).
:::

## 22.4 Ranked practice priorities

The order below is a judgement from the grid, the CDC model question and the
syllabus. Rank 1 means "rehearse this until it is automatic"; a low rank means
"less likely", never "skip it".

| Rank | Question form | Why it ranks here |
|---|---|---|
| 1 | Read a short pandas program: write its output, then modify the filter or columns | Unit 4's long question; the CDC model question uses exactly this form, and it tests reading and writing code together |
| 2 | Write a function that takes parameters and returns a value, with a call | one of Unit 4's three short questions in the model; marks are given separately for the definition and the call |
| 3 | try-except for ValueError or ZeroDivisionError | also in the model's Group B; every robust-input question reduces to it |
| 4 | SQL for a given table: CREATE with constraints, INSERT, SELECT with WHERE and ORDER BY, UPDATE, DELETE | Unit 2's long question is most naturally a set of SQL tasks; each statement is one mark |
| 5 | Database, DBMS, field and record defined with examples | the model's Unit 2 long question; a pure-theory alternative to rank 4 |
| 6 | Supervised, unsupervised (and reinforcement) learning, with examples | a Unit 5 short question in the model; three short questions give room for it every year |
| 7 | Ethical issues of an AI system, or guidelines for responsible AI use (privacy, bias, safety, honesty) | appears twice in the model (a short and the long question); scenario form suits higher-ability marks |
| 8 | Two differences: Internet / intranet / extranet; LAN / MAN / WAN; client–server / peer-to-peer | Unit 1 has two short questions; "two differences" is the commonest 2-mark form |
| 9 | Types of broadband, or guided and unguided media, with features and uses | the model's Unit 1 long question; [1+3] lists are easy to prepare |
| 10 | Raster against vector graphics | the model's Unit 3 short question; also the basis of format-choice MCQs |
| 11 | Components of multimedia with uses in education or business | the model's Unit 3 long question |
| 12 | IoT applications for a scenario (traffic, energy, farming) | a model Unit 5 short question; local scenarios are easy to set |
| 13 | How a chart helps, and choosing line, bar or pie | the model's third Python short question; chart programs are also likely |
| 14 | Network devices — hub, switch, router, modem, access point, gateway | three Unit 1 MCQs a year draw on devices, media and connectors |
| 15 | Topologies with diagrams, or planning a network for a school, home or office | scenario long questions fit Unit 1's higher-ability marks |
| 16 | IPv4 and IPv6; private and public addresses; ping and ipconfig | regular MCQ material and an easy short question |
| 17 | Cloud service models IaaS, PaaS, SaaS with examples | a natural Unit 5 short or long question with a clear marking scheme |
| 18 | Choosing file formats: PNG, JPG, GIF, SVG, WAV, MP3, MP4 | two Unit 3 MCQs each year; the model asks for PNG and WAV |
| 19 | A short turtle program (square, polygon, filled circle) | in the syllabus but not in the model paper; a possible short question |
| 20 | e-commerce, e-governance and e-education in Nepal, with merits and limitations | Unit 5 content well suited to a [1+3] long question |

::: tip The last week before the paper
Work down the table. For each of the top ten ranks do three questions from the
subjective bank (chapter 21) and mark them by key element. Then sit both model
papers above **under the clock, in two hours each**, and compare with the
solutions line by line — especially indentation in Python and quotes, commas
and semicolons in SQL.
:::

## 22.5 Two answers written the way the marker pays

::: example A 2-mark difference: raster and vector graphics
**Question.** Write two differences between raster and vector graphics.

**Model answer.** (1) Raster graphics are made of a grid of pixels, whereas vector
graphics are made of shapes described mathematically. (2) Raster graphics lose
quality (pixelate) when enlarged, whereas vector graphics stay sharp at any size.

Each point compares **both** sides in one sentence, so each earns its full mark.
"Raster uses pixels" alone is only half a difference.
:::

::: example A 4-mark program question [2+2]
**Question.** Write the output of
`print(df[df["Marks"] >= 60])` for a DataFrame of Anil 48, Bimala 75 and Chetan
60, and modify it to show those below 60.

**Model answer.** (a) Two marks for the exact output, including the index
numbers and the column heading:

```text
     Name  Marks
1  Bimala     75
2  Chetan     60
```

Chetan's 60 is included because the condition is "60 or more". (b) Two marks
for the changed condition and a complete, correctly indented program:
`print(df[df["Marks"] < 60])`, which shows only Anil. A frequent loss of marks is
writing `df["Marks"] < 60` without the outer `df[ ]`, which prints a column of
True and False instead of the rows.
:::

## Chapter summary

- The paper is **10 × 1 + 10 × 2 + 5 × 4 = 50 marks in 2 hours**, with 50 more
  internal marks (practical and project 35, participation 5, terminal tests 10).
- Unit split (MCQ, short, long): Networking 3, 2, 1; DBMS 2, 1, 1; Multimedia
  2, 1, 1; Python 2, 3, 1; AI 1, 3, 1. Every unit has one long question.
- Plan the clock: 12 minutes for Group A, 45 for B, 50 for C, 13 to check.
- Highest priorities: pandas output-and-modify, a function with return,
  try-except, SQL for a table, learning types, AI ethics, two-point network
  differences.
- Both model papers are original practice items built to the grid; they are a
  rehearsal, not a forecast.

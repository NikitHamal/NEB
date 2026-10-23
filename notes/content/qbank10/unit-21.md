---
subject: Question Bank
grade: 10
unit: 21
title: "Computer Science: Unit-wise Subjective Question Bank"
hours: 0
area: Computer Science
---

Group A is ten single marks. The other **40 marks** of the Computer Science
paper come from **ten short questions of 2 marks** (Group B) and **five long
questions of 4 marks** (Group C), and here the marker gives **one mark for each
correct key element** of your answer: a definition, a difference, an example, a
correct line of code, a correct output. This chapter works through the five
units in syllabus order. Each section opens with a fully worked model question,
then gives 2-mark and 4-mark questions with complete answers.

::: key How to use this bank
Read the model question at the head of each unit, then close the book and write
the other answers yourself. Mark them **by key element**: a 2-mark difference
needs two separate, complete points; a [1+3] question needs the definition plus
three explained points. Every program and query here was run (Python 3.12,
MySQL 8.4) and its output is printed: compare yours line by line. A 2-mark
question deserves about **4 minutes** and a 4-mark question about **8**.
:::

::: caution Practice items, not past questions
Every question below is an original **practice** item written to the CDC grid
and model paper. None is claimed to have appeared in an SEE paper.
:::

```figure caption="Where the 40 written-answer marks come from. Python and AI each carry three short questions; every unit has exactly one long question."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.6))
units = ["Networking", "DBMS", "Multimedia", "Python", "AI and tech"]
short = [4, 2, 2, 6, 6]
long_ = [4, 4, 4, 4, 4]
y = np.arange(len(units))[::-1]
ax.barh(y, short, color=ACCENT, height=0.55, label="Group B: short (2 marks each)")
ax.barh(y, long_, left=short, color=SERIES[3], height=0.55, label="Group C: long (4 marks)")
for yi, s, l in zip(y, short, long_):
    ax.text(s + l + 0.2, yi, f"{s + l}", va="center", fontsize=8, color=INK)
ax.set_yticks(y); ax.set_yticklabels(units, fontsize=8)
ax.set_xlim(0, 20)
ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
ax.set_xlabel("marks from Groups B and C", fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(fontsize=7.2, loc="center right", frameon=False)
```

## 21.1 Computer Network and Communication

::: example Model question: planning a small network
**Problem.** A health post in a rural municipality has four computers, a
printer and a Wi-Fi access point. There is no fibre line, so it will use a 4G
router for the Internet. Plan the network: name the topology, the devices and
media, and explain how the computers get their IP addresses. <span class="marks">[4]</span>

**Solution.** (1) **Topology**: a **star**, with an 8-port **switch** at the
centre, because one faulty cable then affects only one computer and devices are
easy to add. (2) **Media and devices**: **CAT6** cables with **RJ-45**
connectors from each computer, the printer and the **access point** to the
switch; the **4G router** connects the switch to the mobile network, so it is
the **default gateway**. (3) **Addressing**: the router's **DHCP** server gives
each computer a **dynamic private address** such as 192.168.1.10, while the
printer is given a **static address** (192.168.1.20) so that everyone can always
find it. (4) **Wi-Fi**: staff phones and laptops join through the access point,
protected by a WPA2/WPA3 password. One mark for each numbered point.
:::

**Short questions (2 marks each)**

1. Define bandwidth and throughput. <span class="marks">[2]</span>
2. Differentiate between simplex and half-duplex communication with one example each. <span class="marks">[2]</span>
3. Give two reasons for joining two school buildings 500 m apart with optical fibre. <span class="marks">[2]</span>
4. Write two differences between a switch and a router. <span class="marks">[2]</span>
5. A 1.2 GB software update downloads at 50 Mbps. Find the time in minutes (take 1 GB = 1,000 MB). <span class="marks">[2]</span>
6. Differentiate between IPv4 and IPv6 in two points. <span class="marks">[2]</span>
7. What are the uses of the ping and ipconfig commands? <span class="marks">[2]</span>
8. Differentiate between an intranet and an extranet with one example each. <span class="marks">[2]</span>

**Long questions (4 marks each)**

1. Explain any four network topologies, with a sketch and one advantage of each. <span class="marks">[4]</span>
2. What are guided and unguided media? Give two examples of each and write two differences. <span class="marks">[1+1+2]</span>
3. Define IP address. Explain private and public, and static and dynamic, addresses with examples. <span class="marks">[1+3]</span>
4. Compare client–server and peer-to-peer networks. Which one should a bank use, and why? <span class="marks">[3+1]</span>

::: note Solutions to 21.1
**Short 1.** Bandwidth is the maximum amount of data a link can carry per
second; throughput is the amount actually delivered per second. Both are
measured in bps, Mbps or Gbps.

**Short 2.** Simplex: data flows in one direction only, e.g. TV broadcasting.
Half duplex: data flows both ways but one way at a time, e.g. a walkie-talkie.

**Short 3.** Copper Ethernet is limited to 100 m per run, while fibre carries
data for kilometres; and fibre carries light, so lightning and electrical noise
between the buildings cannot disturb it (it is also faster).

**Short 4.** A switch joins devices within one LAN and forwards frames by MAC
address; a router joins different networks (a LAN and the Internet) and
forwards packets by IP address, choosing the best path.

**Short 5.** 1.2 GB = 1,200 MB = 1,200 × 8 = 9,600 Mb; time = 9,600 ÷ 50 =
**192 s = 3.2 minutes**.

**Short 6.** IPv4 addresses are 32 bits, written as four decimal numbers with
dots (192.168.1.1); IPv6 addresses are 128 bits, written as eight hexadecimal
groups with colons (2001:db8::1). IPv4 offers about 4.3 billion addresses, IPv6
about 3.4 × 10³⁸.

**Short 7.** `ping` checks whether another computer or website can be reached
and shows the time each reply takes; `ipconfig` shows this computer's IP
address, subnet mask and default gateway.

**Short 8.** An intranet is a private network for an organisation's own staff,
e.g. a bank's staff portal; an extranet opens part of it to selected outsiders,
e.g. a supplier portal where shops check their orders.

**Long 1.** *Bus*: all nodes on one backbone cable with terminators — uses the
least cable. *Ring*: each node joined to the next in a closed loop, data in one
direction — no collisions. *Star*: every node cabled to a central switch — one
faulty cable affects only one computer and faults are easy to find. *Mesh*:
nodes joined by many links — data takes another path if a link fails. (A tree
or hybrid is also acceptable.) Each needs a small labelled sketch.

**Long 2.** Guided media carry signals along a cable — twisted pair, coaxial,
optical fibre. Unguided media carry electromagnetic waves through air or
space — radio, microwave, infrared, satellite, Wi-Fi, Bluetooth. Differences:
guided media give a fixed path and are little affected by weather, while
unguided signals spread out and are weakened by walls and rain; guided media are
harder to tap, while unguided media allow devices to move freely.

**Long 3.** An IP address is the logical number given to every device on a
network to identify it and route data to it. *Private* addresses (10.x,
172.16–31.x, 192.168.x) are used inside LANs and not routed on the Internet;
*public* addresses are unique worldwide and assigned by ISPs, e.g. 8.8.8.8.
*Static* addresses are set by hand and never change, e.g. a printer at
192.168.1.20; *dynamic* addresses are given by DHCP for a lease period, e.g. a
phone joining Wi-Fi.

**Long 4.** Client–server: dedicated servers provide services to clients;
central control, strong security and central backup; costly; suits large
networks. Peer-to-peer: all computers equal, each shares its own resources;
cheap and simple, but weak security and separate backups; suits about ten
computers. A **bank** must use **client–server**, because customer accounts need
central security, access control, backup and many simultaneous users.
:::

## 21.2 Database Management System

::: example Model question: SQL for a library table
**Problem.** A school library keeps `library(book_id, title, author, price,
copies)`. Write SQL to (a) create the table with book_id as primary key, title
required and price greater than 0; (b) add the book 5, "Shirishko Phool" by
Parijat, Rs 300, 3 copies; (c) show the title and price of books costing more
than Rs 500, the most expensive first; (d) add two copies of book 2. <span class="marks">[4]</span>

**Solution.**

```sql
CREATE TABLE library (
    book_id INT PRIMARY KEY,
    title   VARCHAR(60) NOT NULL,
    author  VARCHAR(40),
    price   DECIMAL(7, 2) CHECK (price > 0),
    copies  INT DEFAULT 1
);
INSERT INTO library (book_id, title, author, price, copies)
VALUES (5, 'Shirishko Phool', 'Parijat', 300.00, 3);
SELECT title, price FROM library WHERE price > 500 ORDER BY price DESC;
UPDATE library SET copies = copies + 2 WHERE book_id = 2;
```

Tested with four more books in the table, the SELECT returned:

| title | price |
|---|---|
| Karnali Blues | 700.00 |
| Palpasa Cafe | 650.00 |
| Seto Dharti | 550.00 |

and the UPDATE reported `1 row affected`, raising Palpasa Cafe from 2 to 4
copies. One mark for each correct statement.
:::

**Short questions (2 marks each)**

1. Define primary key and foreign key with one example each. <span class="marks">[2]</span>
2. Write two differences between DDL and DML, naming two commands of each. <span class="marks">[2]</span>
3. Write two advantages of a DBMS over a paper filing system. <span class="marks">[2]</span>
4. What is a composite key? When is it needed? Give an example. <span class="marks">[2]</span>
5. Write an SQL statement to display the names of students that begin with S from `students(roll, name, class)`. <span class="marks">[2]</span>
6. What is the difference between DELETE and DROP? <span class="marks">[2]</span>
7. Name the type of relationship, with a reason: (a) a citizen and his or her citizenship certificate; (b) a class teacher and the students of the class. <span class="marks">[2]</span>

**Long questions (4 marks each)**

1. Define DBMS. Explain any three of its features. <span class="marks">[1+3]</span>
2. A school keeps `staff(sid, name, post, salary)`. Write SQL to (a) show the name and salary of staff earning from Rs 30,000 to Rs 50,000; (b) list all names in alphabetical order; (c) change the post of sid 5 to "Head"; (d) remove all staff whose post is "Peon". <span class="marks">[4]</span>
3. Explain the three types of relationship with an example of each, and state how each is stored in tables. <span class="marks">[4]</span>

::: note Solutions to 21.2
**Short 1.** A primary key uniquely identifies each record and cannot be NULL,
e.g. `roll` in `students`. A foreign key is a field that refers to the primary
key of another table, e.g. `roll` in `marks` referring to `students(roll)`.

**Short 2.** DDL defines the structure of the database — CREATE, ALTER, DROP;
DML works on the data in the tables — INSERT, SELECT, UPDATE, DELETE. DDL changes
are committed at once; DML changes can be undone inside a transaction.

**Short 3.** Searching, sorting and updating take seconds instead of hours; and
keys and constraints stop duplicate or invalid entries (also security,
backup, many users at once).

**Short 4.** A composite key is a key made of two or more fields that together
identify a record; it is needed when no single field is unique, e.g.
(`roll`, `subject`) in a marks table, where a student has many subjects.

**Short 5.**
```sql
SELECT name FROM students WHERE name LIKE 'S%';
```
On the `students` table of the DBMS chapter it returned Subigya Nepal and
Sampada Bhattarai.

**Short 6.** DELETE (DML) removes chosen rows or all rows but keeps the table;
DROP (DDL) removes the whole table, its structure and data, permanently.

**Short 7.** (a) **One-to-one** — each citizen has one certificate and each
certificate belongs to one citizen. (b) **One-to-many** — one class teacher has
many students, but each student has one class teacher.

**Long 1.** A DBMS is software that creates, stores, retrieves, updates and
manages data in a database, e.g. MySQL. Features: *data storage* in tables of
rows and columns; *data retrieval* with queries in seconds; *data integrity*
through keys and constraints such as CHECK; *security* through accounts and
permissions; *backup and recovery*; *control of redundancy* (any three, one
mark each).

**Long 2.**
```sql
SELECT name, salary FROM staff WHERE salary BETWEEN 30000 AND 50000;
SELECT name FROM staff ORDER BY name;
UPDATE staff SET post = 'Head' WHERE sid = 5;
DELETE FROM staff WHERE post = 'Peon';
```
On six sample records, (a) returned Gita Sharma 42000.00, Hari Thapa 38000.00
and Mohan Rai 46000.00; (b) listed Bina KC, Gita Sharma, Hari Thapa, Mohan Rai,
Ram Lama, Sita Magar; (c) changed 1 row; (d) removed 2 rows, leaving four staff.

**Long 3.** *One-to-one*: one record matches exactly one, e.g. person —
passport; stored by putting one table's primary key as a unique foreign key in
the other. *One-to-many*: one record matches many, each of which matches one,
e.g. teacher — classes; the foreign key goes in the "many" table. *Many-to-many*:
many match many, e.g. students — courses; stored with a junction table
`enrolment(roll, course_code)` holding both keys.
:::

## 21.3 Multimedia

::: example Model question: which audio format to send?
**Problem.** A 3-minute song is recorded in stereo at 44.1 kHz and 16 bits.
(a) Find its size as a WAV file. (b) Find its size as a 128 kbps MP3. (c) Which
should be sent on WhatsApp, and which kept for editing? <span class="marks">[2+1+1]</span>

**Solution.** (a) Size = 44,100 × 16 × 2 × 180 = 254,016,000 bits; ÷ 8 =
**31,752,000 bytes ≈ 31.8 MB**. (b) 128,000 × 180 = 23,040,000 bits; ÷ 8 =
**2,880,000 bytes ≈ 2.9 MB**, about 11 times smaller. (c) Send the **MP3**: small
and plays everywhere. Keep the **WAV** for editing, because it is uncompressed
and every edit and re-save of an MP3 loses more quality.
:::

**Short questions (2 marks each)**

1. Define multimedia. Write two of its uses in business. <span class="marks">[2]</span>
2. Write two differences between raster and vector graphics. <span class="marks">[2]</span>
3. What is the difference between lossy and lossless compression? Name one format of each. <span class="marks">[2]</span>
4. What are the frame rate and the resolution of a video? <span class="marks">[2]</span>
5. Why is PNG preferred for a logo on a website, while JPG is preferred for a photograph? <span class="marks">[2]</span>
6. What is typography? Write two typography rules for a poster. <span class="marks">[2]</span>
7. Write two differences between 2D and 3D animation. <span class="marks">[2]</span>

**Long questions (4 marks each)**

1. Explain the steps to make a poster in Pixlr: creating the project, adding text and a shape, using layers, and exporting it. <span class="marks">[4]</span>
2. A 3-minute Full HD video is recorded at 30 fps. Find (a) the number of frames, (b) the uncompressed size of one frame at 24-bit colour, and (c) the file size at 10 Mbps; (d) explain why video is compressed. <span class="marks">[4]</span>
3. Differentiate between frame-by-frame and keyframe animation with an example. Write two uses of animation in education. <span class="marks">[2+2]</span>

::: note Solutions to 21.3
**Short 1.** Multimedia is the combined use of text, graphics, audio, video and
animation to present information. In business it is used for advertisements
and product videos, and for presentations and video meetings.

**Short 2.** Raster graphics are grids of pixels and pixelate when enlarged;
vector graphics are mathematical shapes and stay sharp at any size. Raster suits
photographs (JPG, PNG), vector suits logos (SVG).

**Short 3.** Lossless compression makes a file smaller without losing any
detail (PNG, FLAC); lossy compression throws away detail that is hard to notice,
giving much smaller files (JPG, MP3).

**Short 4.** Frame rate is the number of frames shown each second (fps), e.g.
30 fps; resolution is the number of pixels in each frame, width × height, e.g.
1920 × 1080.

**Short 5.** PNG is lossless and supports a transparent background, so a logo
keeps sharp edges and sits cleanly on any colour. JPG's lossy compression makes
photographs much smaller with no visible loss, while PNG photos would be very
large.

**Short 6.** Typography is the art of arranging text for readability and
appearance. Rules: use at most two fonts; make headings much larger than body
text, with strong contrast between text and background.

**Short 7.** 2D animation has width and height only and looks flat; 3D has
depth, perspective, light and shadow. 2D is drawn or built from flat parts; 3D is
modelled, rigged and rendered.

**Long 1.** (1) Open pixlr.com → Pixlr Express → Create new; type a name and a
size such as 1920 × 1080 → Create. (2) Choose the Text tool → Add new text, type
the title and set font, size and colour; add a shape from Arrange/Elements →
Shape and set its fill. (3) In the Layers panel add, rename, hide, lock or
reorder layers so that the background, photo and text stay separate. (4) Click
Save, choose PNG (or JPG), set the quality and Save as.

**Long 2.** (a) 3 × 60 × 30 = **5,400 frames**. (b) 1920 × 1080 × 3 =
**6,220,800 bytes** (about 6.2 MB). (c) 10,000,000 × 180 = 1,800,000,000 bits;
÷ 8 = **225,000,000 bytes = 225 MB**. (d) Uncompressed, the video would need
6.2 MB × 5,400 ≈ 33.6 GB; codecs such as H.264 make it small enough to store,
upload and stream.

**Long 3.** Frame-by-frame animation draws every frame separately, e.g. a
hand-drawn cartoon at 24 drawings per second. Keyframe animation sets only the
key positions and the software calculates the in-between frames, e.g. a ball
placed at the start and end of its path. Uses in education: animated science
processes such as the water cycle or a beating heart; simulations and
interactive lessons such as E-Paath.
:::

## 21.4 Programming in Python

::: example Model question: read a pandas program, then change it
**Problem.** Study the program and answer.

```python
import pandas as pd
data = {"Item": ["Pen", "Copy", "Bag", "Pencil"], "Price": [20, 60, 1200, 10]}
df = pd.DataFrame(data)
print(df[df["Price"] < 50])
```

(a) Write its output. (b) Modify it to show the items costing Rs 50 or more,
the most expensive first. <span class="marks">[2+2]</span>

**Solution.** (a)

```text
     Item  Price
0     Pen     20
3  Pencil     10
```

Only rows whose Price is below 50 are kept, with their original index numbers.

(b)

```python
import pandas as pd
data = {"Item": ["Pen", "Copy", "Bag", "Pencil"], "Price": [20, 60, 1200, 10]}
df = pd.DataFrame(data)
costly = df[df["Price"] >= 50]
print(costly.sort_values("Price", ascending=False))
```

```text
   Item  Price
2   Bag   1200
1  Copy     60
```
:::

**Short questions (2 marks each)**

1. Write a function `simple_interest(p, t, r)` that returns the simple interest, and call it for p = 5000, t = 2, r = 10. <span class="marks">[2]</span>
2. Write a program that reads the user's age and uses try-except to handle a ValueError when letters are typed. <span class="marks">[2]</span>
3. Write the output of the following program, showing how you got it. <span class="marks">[2]</span>

```python
total = 1
for i in range(1, 5):
    total *= i
print(total)
```

4. Differentiate between a local and a global variable with an example. <span class="marks">[2]</span>
5. What is the difference between the file modes "w" and "a"? <span class="marks">[2]</span>
6. Write a turtle program to draw a square of side 120 using a loop. <span class="marks">[2]</span>
7. Write a program that reads `marks.csv` (columns Name, Marks) with pandas and prints the average mark. <span class="marks">[2]</span>
8. Why is a bar chart suitable for comparing the population of Nepal's seven provinces? <span class="marks">[2]</span>

**Long questions (4 marks each)**

1. Write a program with a function `grade(p)` that returns the SEE letter grade for a percentage p, and use it to print the grades of 55, 82.5, 91 and 33. <span class="marks">[4]</span>
2. Write a pandas program that makes a DataFrame of four students' Name, Club and Score, saves it as `club.csv` without the index, reads it back and shows the students who scored more than 70. <span class="marks">[4]</span>
3. A family spends Rs 15,000 on food, 10,000 on rent, 8,000 on education and 7,000 on other things each month. Write a program to draw a pie chart with a title and percentages, and state the percentage for food. <span class="marks">[3+1]</span>
4. Write a program that asks for a file name, displays the file, shows a message if the file does not exist, and always prints "Done" at the end. <span class="marks">[4]</span>

::: note Solutions to 21.4
**Short 1.**
```python
def simple_interest(p, t, r):
    return p * t * r / 100

print("Simple interest:", simple_interest(5000, 2, 10))
```
Output: `Simple interest: 1000.0`.

**Short 2.**
```python
try:
    age = int(input("Enter your age: "))
    print("In five years you will be", age + 5)
except ValueError:
    print("Please type your age in digits, for example 15.")
```
Typing "fifteen" prints the message; typing 15 prints `In five years you will
be 20`.

**Short 3.** The loop multiplies total by 1, 2, 3 and 4: 1 × 1 × 2 × 3 × 4 =
**24** (it computes 4!).

**Short 4.** A local variable is created inside a function and exists only
there; a global variable is created outside all functions and can be read
anywhere. In `x = 10` followed by `def f(): y = 5`, x is global and y is local —
`print(y)` outside f gives a NameError.

**Short 5.** "w" erases the file's old content and writes from the start; "a"
keeps the old content and adds the new data at the end. Both create the file if
it does not exist.

**Short 6.**
```python
import turtle
t = turtle.Turtle()
for i in range(4):
    t.forward(120)
    t.right(90)
turtle.done()
```

**Short 7.**
```python
import pandas as pd
df = pd.read_csv("marks.csv")
print("Average marks:", df["Marks"].mean())
```
With marks 78, 64, 91 and 55 it printed `Average marks: 72.0`.

**Short 8.** The provinces are separate categories to be compared, and bars of
different lengths show at a glance which province has the most and the fewest
people; a line chart would wrongly suggest a trend between provinces.

**Long 1.**
```python
def grade(p):
    if p >= 90:
        return "A+"
    elif p >= 80:
        return "A"
    elif p >= 70:
        return "B+"
    elif p >= 60:
        return "B"
    elif p >= 50:
        return "C+"
    elif p >= 40:
        return "C"
    elif p >= 35:
        return "D"
    else:
        return "NG"

for p in [55, 82.5, 91, 33]:
    print(p, "->", grade(p))
```
```text
55 -> C+
82.5 -> A
91 -> A+
33 -> NG
```

**Long 2.**
```python
import pandas as pd

data = {"Name": ["Asmita", "Bijay", "Chandani", "Dipesh"],
        "Club": ["Science", "Sports", "Coding", "Eco"],
        "Score": [78, 64, 91, 70]}
pd.DataFrame(data).to_csv("club.csv", index=False)

df = pd.read_csv("club.csv")
print(df[df["Score"] > 70])
```
```text
       Name     Club  Score
0    Asmita  Science     78
2  Chandani   Coding     91
```
Dipesh's 70 is not more than 70, so he is left out.

**Long 3.**
```python
import matplotlib.pyplot as plt

items = ["Food", "Rent", "Education", "Others"]
amount = [15000, 10000, 8000, 7000]

plt.pie(amount, labels=items, autopct="%1.1f%%")
plt.title("Monthly expenses of a family")
plt.show()
```
Food is 15,000 ÷ 40,000 × 100 = **37.5 %**, the largest slice.

**Long 4.**
```python
name = input("Enter file name: ")
try:
    f = open(name, "r")
    print(f.read())
    f.close()
except FileNotFoundError:
    print("File", name, "was not found.")
finally:
    print("Done")
```
For a missing file it printed `File notes.txt was not found.` and then `Done`;
for an existing file it printed the file's contents and then `Done`.
:::

## 21.5 AI and Contemporary Technologies

::: example Model question: AI cameras for traffic
**Problem.** A municipality wants to use AI cameras to manage traffic and to
detect vehicles breaking the rules. Write two benefits and two ethical concerns,
with a safeguard for each concern. <span class="marks">[2+2]</span>

**Solution.** *Benefits*: (1) traffic lights can adjust to the real flow of
vehicles, reducing jams and fuel waste; (2) rule-breakers are detected day and
night, making roads safer. *Concerns and safeguards*: (1) **privacy** — cameras
record everyone's movements; keep only the footage needed, delete it after a
fixed period and allow only authorised officers to view it; (2) **bias and
errors** — the system may misread number plates or faces in poor light or for
some groups; have a human officer check every fine before it is issued and test
the system's accuracy regularly.
:::

**Short questions (2 marks each)**

1. Define artificial intelligence and machine learning. <span class="marks">[2]</span>
2. Differentiate between supervised and unsupervised learning, with an example of each. <span class="marks">[2]</span>
3. What is reinforcement learning? Give an example. <span class="marks">[2]</span>
4. Write two limitations of generative AI. <span class="marks">[2]</span>
5. Write the three stages of the sense–think–act cycle of a robot. <span class="marks">[2]</span>
6. What is the Internet of Things? Give two examples of IoT in a home. <span class="marks">[2]</span>
7. Differentiate between virtual reality and augmented reality. <span class="marks">[2]</span>
8. Differentiate between IaaS and SaaS with an example of each. <span class="marks">[2]</span>
9. Write two merits of e-governance with examples from Nepal. <span class="marks">[2]</span>

**Long questions (4 marks each)**

1. Explain how a large language model and an image generator produce their output. Write two tips for writing a good prompt. <span class="marks">[2+2]</span>
2. Explain the three cloud service models with an example of each. Which would a school use to prepare its routine, and why? <span class="marks">[3+1]</span>
3. Discuss the use of IoT in smart agriculture in Nepal with two examples, and write two challenges of IoT. <span class="marks">[2+2]</span>

::: note Solutions to 21.5
**Short 1.** AI is the branch of computer science that makes machines do tasks
needing human intelligence, such as reasoning and understanding language. ML is
the part of AI in which machines learn from data and improve with experience.

**Short 2.** Supervised learning trains on labelled data, e.g. emails marked
spam or not spam; unsupervised learning finds groups in unlabelled data, e.g.
grouping customers by shopping habits.

**Short 3.** Reinforcement learning is learning by trial and error: an agent
acts, receives rewards or penalties, and learns the actions that earn most
reward — e.g. a robot learning to walk or a program learning to play a game.

**Short 4.** It can produce false information confidently (hallucination); and
it can repeat bias from its training data (also out-of-date knowledge, privacy
risks, copyright issues).

**Short 5.** *Sense*: sensors collect information; *think*: the controller or
AI decides what to do; *act*: actuators such as motors carry out the action.

**Short 6.** IoT is the network of everyday objects with sensors and Internet
connections that collect and share data and act on it. Home examples: smart
bulbs or plugs controlled from a phone; a doorbell camera that sends alerts.

**Short 7.** VR replaces the real world with a computer-made 3D world seen
through a headset, e.g. a VR game; AR adds digital information on top of the
real world through a phone or glasses, e.g. Google Lens translating a sign.

**Short 8.** IaaS provides virtual servers, storage and networks managed by the
customer's IT staff, e.g. Amazon EC2; SaaS provides complete applications used
through a browser, e.g. Gmail or Google Docs.

**Short 9.** Faster service without queues, e.g. applying for a passport
online; and transparency, e.g. tracking applications and seeing SEE results
online (also less corruption, and services such as the Nagarik App from any
district).

**Long 1.** An LLM is trained on huge amounts of text to predict the next token
(word piece); when given a prompt it writes the answer one token at a time,
choosing likely tokens, so it does not look facts up. An image generator
(diffusion model) learns from pictures and captions; it starts from random noise
and removes the noise step by step, guided by the prompt, until an image forms.
Prompt tips: state the task, audience, length and format clearly; give context
or an example, and refine the prompt if the first answer is not right.

**Long 2.** *IaaS*: virtual servers, storage and networks on rent, managed by
your own IT staff — Amazon EC2. *PaaS*: a ready platform to build and run
applications — Google App Engine. *SaaS*: finished software used online —
Gmail, Google Docs. A school would use **SaaS** such as Google Docs or Sheets to
prepare its routine: nothing to install, teachers can edit and view it from
anywhere, and it is free or cheap.

**Long 3.** Soil-moisture sensors in a field can switch irrigation pumps on only
when the soil is dry, saving water and electricity for farmers in the Terai; and
temperature and humidity sensors in a greenhouse or poultry farm can send alerts
to the farmer's phone so that conditions are corrected in time (also livestock
trackers, crop-disease alerts). Challenges: devices need reliable Internet and
electricity, which villages may lack; and connected devices can be hacked and
the cost is high for small farmers.
:::

## Chapter summary

- Groups B and C carry **40 of the 50 marks**; the marker gives one mark per
  key element, so write separate, complete points.
- **Networking**: definitions with units, two-point differences, network
  planning with topology, devices, media and addressing.
- **DBMS**: keys, DDL vs DML, relationships, and full SQL statements — CREATE
  with constraints, INSERT with a column list, SELECT with WHERE and ORDER BY,
  UPDATE and DELETE with WHERE.
- **Multimedia**: raster vs vector, lossy vs lossless, file-size calculations
  (audio: rate × bits × channels × seconds ÷ 8; video: frames × bytes per frame
  or bitrate × seconds ÷ 8), tool steps.
- **Python**: complete programs with def, parameters and return, try-except,
  file modes, pandas filters and sorts, and Matplotlib charts — every output
  above was produced by running the code.
- **AI**: learning types with examples, robot cycle, generative AI and
  prompting, ethics with safeguards, IoT, AR/VR, cloud models, and e-services in
  Nepal.

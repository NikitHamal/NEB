---
subject: Question Bank
grade: 12
unit: 14
title: "Computer Science: Unit-wise Objective Question Bank"
hours: 0
area: Computer Science
---

Group A of the Computer Science paper is worth nine marks out of fifty. That is
eighteen per cent of the written paper, and it is the only part of the paper
where a candidate who knows the fact gets the mark instantly and a candidate who
does not gets nothing at all. There is no partial credit in Group A. There is
also no thinking time to spare: nine marks at the paper's own rate of 2.4
minutes per mark is about twenty-two minutes, and most good candidates finish
Group A in eight to ten minutes so that the time banks forward into Group C.

This chapter is a bank of **162 multiple-choice questions**, arranged in the
order of the seven units of the NEB Grade 12 Computer Science syllabus. Every
question has a worked answer key that gives the reason in one line — because a
reason you can restate is a fact you will still own in Chait, and a bare letter
is not.

::: key What the real papers actually asked
Three papers could be verified for this book: the NEB 2080 (2023) Computer
Science paper, subject code 4281; the NEB 2079 Grade 12 Computer paper; and the
NEB Grade 12 Computer model question issued for the new course. Between them
they contain **27 Group A items**, and **26 of those 27 are reproduced here** —
25 word for word, and one in corrected form because the original offered the
same answer twice. (The twenty-seventh depended on a printed program listing
that could not be recovered.) Reproduced items carry a tag such as
`(NEB 2080)`. Everything untagged is written to the same pattern and difficulty
but is **not** claimed to be a past question.
:::

## 14.1 How the nine Group A marks are spread

Before the bank itself, one piece of evidence worth more than any study tip.
Across the three verified papers there are 27 Group A items in total. Sorting
each item into the syllabus unit it tests gives the picture below.

```figure caption="Where the 27 verified Group A marks came from, across the NEB 2079 paper, the NEB 2080 paper and the NEB model question. Web Technology II supplied more MCQs than any other unit."
import numpy as np, matplotlib.pyplot as plt

units = ["Web Tech II", "DBMS", "Networking", "Prog. in C", "Softw. Process", "OOP", "Recent Trends"]
count = [8, 5, 4, 3, 3, 2, 2]
hours = [12, 12, 15, 12, 10, 10, 9]
y = np.arange(len(units))[::-1]
fig, ax = plt.subplots(figsize=(5.1, 3.0))
ax.barh(y, count, height=0.58, color=ACCENT)
for yi, c, h in zip(y, count, hours):
    ax.text(c + 0.18, yi, f"{c}", va="center", ha="left",
            fontsize=8.5, color=INK, fontweight="bold")
    ax.text(10.6, yi, f"{h} hr", va="center", ha="right",
            fontsize=7.4, color=MUTED)
ax.set_yticks(y); ax.set_yticklabels(units, fontsize=8)
ax.set_xlim(0, 10.8)
ax.set_xticks([0, 2, 4, 6, 8])
ax.set_xlabel("Group A items in the three verified papers", fontsize=8)
ax.text(10.6, y[0] + 0.72, "teaching\nhours", ha="right", va="bottom",
        fontsize=7, color=MUTED, linespacing=1.2)
ax.tick_params(labelsize=8, length=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.xaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

Read that carefully, because it contradicts what most candidates do. Web
Technology II carries **twelve** teaching hours, fewer than Networking's
fifteen, yet it produced **eight** of the 27 MCQs — nearly one in three. The
reason is structural, not accidental: Web Technology II is full of exact,
checkable, one-line facts. The `$` sign in jQuery. `mysqli_connect()`. The tag
that makes a hyperlink. The syntax for an external script. An examiner writing a
one-mark item needs a question with exactly one defensible answer, and web
syntax hands that over free. Networking, by contrast, is full of comparisons and
diagrams, which make excellent five- and eight-mark questions and awkward MCQs.

::: tip Where to spend the last week
If you are revising Group A specifically, revise **syntax** — web syntax, SQL
keyword categories, C declarations. Those are where the one-mark questions live.
Revise topologies and the OSI model for Group B and C, not for Group A.
:::

## 14.2 Unit 1: Database Management System

Twelve teaching hours; five of the 27 verified MCQs. The examiner's favourite
targets here are the keyword categories of SQL (which statements are DDL, which
are DML), the key vocabulary (primary, candidate, foreign, super), and the
normal forms.

```figure caption="The two-table schema used by several questions in this section. student_info.class_id is a foreign key referring to class_info.class_id; the M : 1 arrow reads many students to one class."
import numpy as np, matplotlib.pyplot as plt

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0.30, 3.72); ax.axis("off")

def table(x, y, w, title, rows, keyrow=0):
    h = 0.62 + 0.46 * len(rows)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                                fc="white", ec=INK, lw=1.1))
    ax.add_patch(FancyBboxPatch((x, y + h - 0.60), w, 0.60,
                                boxstyle="square,pad=0", fc=ACCENT, ec="none"))
    ax.text(x + w / 2, y + h - 0.30, title, ha="center", va="center",
            fontsize=8.4, color="white", fontweight="bold")
    for i, r in enumerate(rows):
        yy = y + h - 0.60 - 0.30 - 0.46 * i
        ax.text(x + 0.22, yy, r, ha="left", va="center", fontsize=7.6, color=INK)
    return h

h1 = table(0.35, 0.55, 4.1, "student_info",
           ["regno  (PK)", "name", "class_id  (FK)", "gender", "address"])
h2 = table(5.55, 1.45, 4.1, "class_info",
           ["class_id  (PK)", "class_name", "teacher"])
arr = FancyArrowPatch((4.45, 0.55 + h1 - 0.60 - 0.30 - 0.46 * 2),
                      (5.55, 1.45 + h2 - 0.60 - 0.30),
                      arrowstyle="-|>", mutation_scale=11,
                      color=SERIES[1], lw=1.3,
                      connectionstyle="arc3,rad=-0.22")
ax.add_patch(arr)
ax.text(5.18, 1.48, "M : 1", ha="center", va="bottom",
        fontsize=7.8, color=SERIES[1], style="italic")
fig.tight_layout()
```

**Set A — data, the relational model and keys**

1. A field that is used to uniquely define a particular record in a table is
   called <span class="marks">[1]</span>
   (a) primary key (b) entity (c) relationship (d) constraints *(NEB 2079)*
2. In relational terminology, a row of a table is called a <span class="marks">[1]</span>
   (a) tuple (b) attribute (c) domain (d) degree
3. The number of attributes in a relation is called its <span class="marks">[1]</span>
   (a) cardinality (b) degree (c) domain (d) arity of the key
4. A candidate key that has been chosen by the designer becomes the <span class="marks">[1]</span>
   (a) foreign key (b) super key (c) primary key (d) alternate key
5. An attribute in one table that refers to the primary key of another table is a <span class="marks">[1]</span>
   (a) composite key (b) foreign key (c) candidate key (d) secondary key
6. The set of permitted values for an attribute is its <span class="marks">[1]</span>
   (a) domain (b) tuple (c) schema (d) instance
7. Which of the following is **not** an advantage of a DBMS over a file system? <span class="marks">[1]</span>
   (a) controlled redundancy (b) data consistency (c) lower initial cost (d) data sharing
8. The ability to change the internal storage structure without changing the
   application programs is called <span class="marks">[1]</span>
   (a) logical data independence (b) physical data independence (c) data integrity (d) data abstraction
9. Who is responsible for granting and revoking access rights on a database? <span class="marks">[1]</span>
   (a) end user (b) application programmer (c) database administrator (d) system analyst

::: note Answers — Set A
**1.** (a) — a primary key is by definition the attribute that identifies one record uniquely.
**2.** (a) — row = tuple = record; column = attribute = field.
**3.** (b) — degree counts columns; cardinality counts rows.
**4.** (c) — a relation may have several candidate keys but only one is made primary.
**5.** (b) — that is the definition of a foreign key; it enforces referential integrity.
**6.** (a) — the domain is the pool of legal values, e.g. `gender` over {M, F}.
**7.** (c) — a DBMS costs *more* to set up; the other three are genuine advantages.
**8.** (b) — physical independence insulates programs from the storage layer.
**9.** (c) — `GRANT` and `REVOKE` are DCL statements, and the DBA owns them.
:::

**Set B — SQL**

1. Which of the statements are used in DDL? <span class="marks">[1]</span>
   (a) create, alter and drop (b) create, insert and select (c) insert, update and delete (d) delete, alter and drop *(NEB model question)*
2. Which of the following is a DML statement? <span class="marks">[1]</span>
   (a) create (b) select (c) create view (d) drop *(NEB 2080)*
3. Which SQL statement is used to delete **rows** from a database table? <span class="marks">[1]</span>
   (a) DELETE (b) REMOVE (c) DROP (d) CLEAR *(NEB 2079)*
4. With SQL, how do you select all the records from a table named `Persons`
   where the value of the column `FirstName` ends with an `a`? <span class="marks">[1]</span>
   (a) `WHERE FirstName='a'` (b) `WHERE FirstName LIKE 'a%'` (c) `WHERE FirstName LIKE '%a'` (d) `WHERE FirstName='%a%'` *(NEB model question)*
5. Which clause filters rows **after** they have been grouped? <span class="marks">[1]</span>
   (a) WHERE (b) HAVING (c) ORDER BY (d) GROUP BY
6. `SELECT COUNT(*) FROM student_info;` returns <span class="marks">[1]</span>
   (a) the number of columns (b) the number of rows (c) the number of non-null names (d) an error
7. Which SQL keyword removes duplicate rows from the result of a query? <span class="marks">[1]</span>
   (a) UNIQUE (b) DISTINCT (c) SINGLE (d) ONLY
8. `GRANT` and `REVOKE` belong to which category of SQL? <span class="marks">[1]</span>
   (a) DDL (b) DML (c) DCL (d) TCL
9. Which statement removes the whole table together with its structure? <span class="marks">[1]</span>
   (a) `DELETE FROM student_info;` (b) `TRUNCATE TABLE student_info;` (c) `DROP TABLE student_info;` (d) `ALTER TABLE student_info;`

::: note Answers — Set B
**1.** (a) — DDL defines *structure*: `CREATE`, `ALTER`, `DROP` (and `TRUNCATE`).
**2.** (b) — DML manipulates *data*; `SELECT`, `INSERT`, `UPDATE`, `DELETE` are DML.
**3.** (a) — `DELETE` removes rows and leaves the table; `DROP` removes the table itself.
**4.** (c) — `%` is the wildcard, so `'%a'` means "anything, then a final a".
**5.** (b) — `WHERE` filters rows before grouping, `HAVING` filters the groups.
**6.** (b) — `COUNT(*)` counts rows, including rows with nulls.
**7.** (b) — `SELECT DISTINCT class_id FROM student_info;`
**8.** (c) — Data Control Language governs privileges.
**9.** (c) — `DROP` destroys structure and data; `DELETE`/`TRUNCATE` keep the structure.
:::

::: example Working a real item: the SQL `LIKE` wildcard
The model question asked how to select all records from `Persons` where
`FirstName` **ends with** an `a`. Suppose the column holds *Asha*, *Bina*,
*Amrita* and *Rajesh*. The answer must return Asha, Bina and Amrita, and reject
Rajesh.

- `WHERE FirstName='a'` returns only a name that is literally the single letter
  `a`. It returns nothing. Dead.
- `WHERE FirstName LIKE 'a%'` means "an `a`, then anything" — it matches names
  that **begin** with `a`. That would return Asha and Amrita, and wrongly drop
  Bina. Dead.
- `WHERE FirstName LIKE '%a'` means "anything, then a final `a`". Asha ✓,
  Bina ✓, Amrita ✓, Rajesh ✗. Correct.
- `WHERE FirstName='%a%'` uses `=` instead of `LIKE`, so `%` is not a wildcard at
  all — it looks for the literal string `%a%`. Dead.

Answer **(c)**. The rule to memorise is positional: **the `%` goes where the
unknown text is.** Unknown text before the `a` means `'%a'`.
:::

**Set C — normalisation, integrity and database architecture**

1. A relation is in 1NF if <span class="marks">[1]</span>
   (a) every attribute is atomic (b) there is no partial dependency (c) there is no transitive dependency (d) every determinant is a candidate key
2. Removing **partial dependency** on a composite primary key takes a relation to <span class="marks">[1]</span>
   (a) 1NF (b) 2NF (c) 3NF (d) BCNF
3. A relation in 2NF becomes 3NF when we remove <span class="marks">[1]</span>
   (a) multi-valued attributes (b) partial dependency (c) transitive dependency (d) foreign keys
4. The main purpose of normalisation is to <span class="marks">[1]</span>
   (a) increase redundancy (b) reduce redundancy and update anomalies (c) speed up every query (d) reduce the number of users
5. Which constraint guarantees that a foreign-key value always matches an
   existing primary-key value? <span class="marks">[1]</span>
   (a) entity integrity (b) domain integrity (c) referential integrity (d) key integrity
6. In the schema of the figure above, inserting a `student_info` row with
   `class_id = 99` when no such `class_info` row exists violates <span class="marks">[1]</span>
   (a) entity integrity (b) referential integrity (c) domain integrity (d) nothing at all
7. In an E-R diagram, an ellipse represents a <span class="marks">[1]</span>
   (a) entity (b) relationship (c) attribute (d) weak entity
8. In a **distributed** database system, the data is <span class="marks">[1]</span>
   (a) stored on one machine at one site (b) split across several sites but appears as one database (c) never shared (d) stored only in main memory
9. Which property of a transaction guarantees that it either completes entirely
   or has no effect at all? <span class="marks">[1]</span>
   (a) atomicity (b) consistency (c) isolation (d) durability

::: note Answers — Set C
**1.** (a) — 1NF forbids repeating groups and multi-valued cells.
**2.** (b) — 2NF = 1NF plus full functional dependence on the whole key.
**3.** (c) — a transitive dependency is a non-key attribute determining another non-key attribute.
**4.** (b) — normalisation trades a little join cost for a lot of integrity.
**5.** (c) — referential integrity is exactly the foreign-key rule.
**6.** (b) — the referenced `class_info.class_id` does not exist.
**7.** (c) — rectangle = entity, diamond = relationship, ellipse = attribute.
**8.** (b) — fragments sit at several sites; the user sees a single logical database.
**9.** (a) — atomicity is the "all or nothing" property of ACID.
:::

## 14.3 Unit 2: Data Communication and Networking

Fifteen teaching hours, the largest unit in the syllabus, but only four of the
27 verified MCQs. Most of this unit's marks are collected in Group B and Group C.
For Group A, concentrate on the numbers — address lengths, port counts, address
classes — and on which device works at which layer.

```figure caption="Four topologies for identification questions. Each circle is a host; the small square is a central device."
import numpy as np, matplotlib.pyplot as plt

fig, axarr = plt.subplots(2, 2, figsize=(4.6, 3.4))
axes = axarr.ravel()
th = np.linspace(0, 2 * np.pi, 6, endpoint=False) + np.pi / 2

def dots(ax, pts):
    for (x, y) in pts:
        ax.plot(x, y, "o", ms=6.5, color=ACCENT, zorder=3)

# A: bus
ax = axes[0]
ax.plot([-1.05, 1.05], [0, 0], color=INK, lw=1.6)
xs = [-0.7, -0.23, 0.23, 0.7]
for i, x in enumerate(xs):
    s = 0.62 if i % 2 == 0 else -0.62
    ax.plot([x, x], [0, s], color=MUTED, lw=1.0)
    ax.plot(x, s, "o", ms=6.5, color=ACCENT, zorder=3)
ax.set_title("A", fontsize=9, color=INK)

# B: star
ax = axes[1]
pts = [(np.cos(t) * 0.82, np.sin(t) * 0.82) for t in th[:5]]
for (x, y) in pts:
    ax.plot([0, x], [0, y], color=MUTED, lw=1.0)
dots(ax, pts)
ax.plot(0, 0, "s", ms=8, color=INK, zorder=4)
ax.set_title("B", fontsize=9, color=INK)

# C: ring
ax = axes[2]
pts = [(np.cos(t) * 0.82, np.sin(t) * 0.82) for t in th]
for i in range(len(pts)):
    x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
    ax.plot([x1, x2], [y1, y2], color=MUTED, lw=1.0)
dots(ax, pts)
ax.set_title("C", fontsize=9, color=INK)

# D: mesh
ax = axes[3]
pts = [(np.cos(t) * 0.82, np.sin(t) * 0.82) for t in th[:5]]
for i in range(len(pts)):
    for j in range(i + 1, len(pts)):
        ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]],
                color=MUTED, lw=0.75)
dots(ax, pts)
ax.set_title("D", fontsize=9, color=INK)

for ax in axes:
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.25, 1.2)
    ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(hspace=0.10, wspace=0.02)
fig.tight_layout()
```

**Set A — media, modes and topology**

1. Coaxial cable is an example of <span class="marks">[1]</span>
   (a) communication software (b) guided transmission media (c) unguided transmission media (d) all of them *(NEB 2080)*
2. Which of the following statements is true about a star network topology? <span class="marks">[1]</span>
   (a) each device is connected to a switch or hub (b) each device is connected to every other device (c) each device is connected in a trunk (d) each device is connected to a terminal *(NEB model question)*
3. In the figure above, which panel shows a **mesh** topology? <span class="marks">[1]</span>
   (a) A (b) B (c) C (d) D
4. In the figure above, which panel shows the topology in which a break in the
   backbone brings down the whole network? <span class="marks">[1]</span>
   (a) A (b) B (c) C (d) D
5. A fully connected mesh of $n$ nodes needs how many duplex links? <span class="marks">[1]</span>
   (a) $n$ (b) $n-1$ (c) $n(n-1)/2$ (d) $n^2$
6. A walkie-talkie communicates in which mode? <span class="marks">[1]</span>
   (a) simplex (b) half duplex (c) full duplex (d) multiplex
7. Which medium is completely immune to electromagnetic interference? <span class="marks">[1]</span>
   (a) unshielded twisted pair (b) coaxial cable (c) optical fibre (d) shielded twisted pair
8. The loss of signal strength as it travels down a medium is called <span class="marks">[1]</span>
   (a) distortion (b) attenuation (c) crosstalk (d) jitter
9. Bandwidth of a digital channel is measured in <span class="marks">[1]</span>
   (a) hertz (b) bits per second (c) bytes (d) watts

::: note Answers — Set A
**1.** (b) — coaxial is a physical cable, therefore guided (bounded) media.
**2.** (a) — every host in a star hangs off one central hub or switch.
**3.** (d) — panel D joins every node to every other node.
**4.** (a) — panel A is a bus; the single backbone is a single point of failure.
**5.** (c) — each of $n$ nodes links to $n-1$ others, and each link is counted twice.
**6.** (b) — both ends can transmit, but only one at a time.
**7.** (c) — fibre carries light, so no electrical noise couples into it.
**8.** (b) — attenuation is loss of energy; a repeater or amplifier undoes it.
**9.** (b) — analogue bandwidth is in hertz, digital capacity in bits per second.
:::

A five-port Ethernet switch of the kind a school computer lab actually uses is
shown below. Almost every star-topology question in this bank describes exactly
this device.

```photo id="qbank/lan-switch-front" caption="A five-port 10/100 Mbps Ethernet switch — the central device of a star topology in a small LAN. The POWER lamp shows the unit is live; the five Link/ACT lamps show which ports have a cable plugged in and carrying traffic." width="78"
call 0.400 0.712 0.390 0.578 "POWER lamp"
call 0.150 0.418 0.380 0.525 "Link/ACT 1–5"
```

**Set B — addressing and devices**

1. What does "MAC" stand for in MAC address? <span class="marks">[1]</span>
   (a) mandatory access control (b) media access control (c) micro access control (d) media access certificate *(NEB 2079)*
2. Which of the following IPv4 addresses is valid? <span class="marks">[1]</span>
   (a) 192.168.1.1 (b) EEE.000.33.000 (c) 257.2.5.1 (d) 202.70.71.262 *(NEB 2080)*
3. A MAC address is how many bits long? <span class="marks">[1]</span>
   (a) 32 (b) 48 (c) 64 (d) 128
4. The address 192.168.10.25 belongs to which class? <span class="marks">[1]</span>
   (a) class A (b) class B (c) class C (d) class D
5. The default subnet mask of a class B address is <span class="marks">[1]</span>
   (a) 255.0.0.0 (b) 255.255.0.0 (c) 255.255.255.0 (d) 255.255.255.255
6. How many usable host addresses does one default class C network provide? <span class="marks">[1]</span>
   (a) 254 (b) 255 (c) 256 (d) 65534
7. Which device forwards a frame only to the port on which the destination host
   sits? <span class="marks">[1]</span>
   (a) hub (b) switch (c) repeater (d) modem
8. A router operates at which layer of the OSI model? <span class="marks">[1]</span>
   (a) data link (b) network (c) transport (d) session
9. Which device converts digital signals to analogue and back for a telephone
   line? <span class="marks">[1]</span>
   (a) gateway (b) bridge (c) modem (d) repeater

::: note Answers — Set B
**1.** (b) — media access control; the address is burnt into the NIC.
**2.** (a) — each octet must be 0–255 and numeric, which rules out (b), (c) and (d).
**3.** (b) — 48 bits, written as twelve hexadecimal digits.
**4.** (c) — the first octet 192 lies in the class C range 192–223.
**5.** (b) — class B uses the first two octets for the network part.
**6.** (a) — $2^{8}-2 = 254$, after removing the network and broadcast addresses.
**7.** (b) — a switch learns MAC addresses; a hub floods every port.
**8.** (b) — routers read IP addresses, which live at layer 3.
**9.** (c) — modulator–demodulator.
:::

::: example Working a real item: which IPv4 address is valid?
The NEB 2080 paper offered `192.168.1.1`, `EEE.000.33.000`, `257.2.5.1` and
`202.70.71.262`. Do not look for the right one; kill the wrong ones.

An IPv4 address is four decimal numbers, separated by dots, each in the range
0–255. That single sentence is the whole test. Apply it in order:

- `EEE.000.33.000` — the first group is letters, not a decimal number. Dead.
- `257.2.5.1` — 257 is greater than 255. Dead.
- `202.70.71.262` — 262 is greater than 255. Dead.
- `192.168.1.1` — four groups, all between 0 and 255. Survives.

Answer **(a)**. Notice that two of the three distractors were built from the same
trick, the out-of-range octet, placed once at the front and once at the back so
that a candidate scanning quickly catches one and misses the other. Check every
octet, not the first.
:::

**Set C — models, protocols and network types**

1. How many layers does the OSI reference model have? <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 7 (d) 9
2. Which OSI layer is responsible for end-to-end error recovery and flow
   control? <span class="marks">[1]</span>
   (a) network (b) transport (c) session (d) presentation
3. Encryption and data compression are carried out at which OSI layer? <span class="marks">[1]</span>
   (a) application (b) session (c) presentation (d) data link
4. Which protocol guarantees delivery by using acknowledgements and
   retransmission? <span class="marks">[1]</span>
   (a) UDP (b) TCP (c) IP (d) ICMP
5. Which protocol translates a domain name into an IP address? <span class="marks">[1]</span>
   (a) DHCP (b) DNS (c) FTP (d) SMTP
6. Which protocol assigns an IP address to a host automatically when it joins
   the network? <span class="marks">[1]</span>
   (a) DNS (b) ARP (c) DHCP (d) SNMP
7. HTTP normally uses which port number? <span class="marks">[1]</span>
   (a) 21 (b) 25 (c) 80 (d) 443
8. A network spread over a single building or campus is a <span class="marks">[1]</span>
   (a) PAN (b) LAN (c) MAN (d) WAN
9. In a peer-to-peer network <span class="marks">[1]</span>
   (a) one machine holds all the data (b) every machine can act as both client and server (c) no machine can share files (d) a dedicated server is compulsory

::: note Answers — Set C
**1.** (c) — physical, data link, network, transport, session, presentation, application.
**2.** (b) — the transport layer owns end-to-end reliability; the network layer only routes.
**3.** (c) — the presentation layer handles translation, encryption and compression.
**4.** (b) — TCP is connection-oriented and reliable; UDP is neither.
**5.** (b) — the Domain Name System is the Internet's directory.
**6.** (c) — Dynamic Host Configuration Protocol leases addresses.
**7.** (c) — port 80 for HTTP, 443 for HTTPS, 21 for FTP, 25 for SMTP.
**8.** (b) — a LAN is limited to one building or campus.
**9.** (b) — peers are equals; there is no dedicated server.
:::

## 14.4 Unit 3: Web Technology II

Twelve teaching hours and **eight** of the 27 verified MCQs — more than any
other unit. If you have one hour left before the paper and you want marks in
Group A, spend it here. The questions are almost always about exact syntax, so
learn the syntax by typing it, not by reading it.

**Set A — HTML, CSS and the web**

1. A collection of hyperlinked documents on the Internet is called <span class="marks">[1]</span>
   (a) HTML (b) webpage (c) www (d) email system *(NEB 2080)*
2. What is the use of the `<a>` tag? <span class="marks">[1]</span>
   (a) to insert an image (b) to create a hyperlink (c) to create a table (d) to create a list *(adapted from the NEB model question)*
3. Which attribute of the `<a>` tag holds the destination address? <span class="marks">[1]</span>
   (a) `src` (b) `href` (c) `link` (d) `url`
4. Which HTML tag creates the largest heading? <span class="marks">[1]</span>
   (a) `<h1>` (b) `<h6>` (c) `<head>` (d) `<heading>`
5. Which tag inserts an image into a web page? <span class="marks">[1]</span>
   (a) `<image>` (b) `<img>` (c) `<pic>` (d) `<src>`
6. Which of these is an **empty** (self-closing) HTML element? <span class="marks">[1]</span>
   (a) `<p>` (b) `<div>` (c) `<br>` (d) `<span>`
7. Which tag is used to create an ordered list? <span class="marks">[1]</span>
   (a) `<ul>` (b) `<ol>` (c) `<li>` (d) `<dl>`
8. An external style sheet is attached to a page with <span class="marks">[1]</span>
   (a) `<style>` (b) `<link>` (c) `<css>` (d) `<script>`
9. In CSS, a selector beginning with `#` selects by <span class="marks">[1]</span>
   (a) class (b) id (c) tag name (d) attribute

::: note Answers — Set A
**1.** (c) — the World Wide Web is the hyperlinked document collection; HTML is only its language.
**2.** (b) — the anchor tag makes a link; note that the original model question listed "create a link" and "create a hyperlink" as two options, which is a flaw in that paper.
**3.** (b) — `<a href="page.html">`; `src` belongs to `<img>` and `<script>`.
**4.** (a) — `<h1>` is largest, `<h6>` smallest.
**5.** (b) — `<img src="photo.jpg" alt="...">`.
**6.** (c) — `<br>` has no closing tag and no content.
**7.** (b) — `<ol>` numbers the items, `<ul>` bullets them.
**8.** (b) — `<link rel="stylesheet" href="style.css">` goes in the head.
**9.** (b) — `#header` selects `id="header"`; `.header` would select the class.
:::

**Set B — JavaScript and jQuery**

1. What is the correct syntax for referring to an external JavaScript script? <span class="marks">[1]</span>
   (a) `<script src="myscript.js"></script>` (b) `<script href="myscript.js"></script>` (c) `<js href="myscript.js"></js>` (d) `<js src="myscript.js"></js>` *(NEB 2079)*
2. Which of the following is the correct syntax to display "Stay Safe" in an
   alert box using JavaScript? <span class="marks">[1]</span>
   (a) `alert-box("Stay Safe");` (b) `confirm("Stay Safe");` (c) `msgbox("Stay Safe");` (d) `alert("Stay Safe");` *(NEB model question)*
3. Which of the given signs is used as a shortcut for jQuery? <span class="marks">[1]</span>
   (a) the `%` sign (b) the `&` sign (c) the `$` sign (d) the `@` sign *(NEB 2080)*
4. Which jQuery method is used to hide selected elements? <span class="marks">[1]</span>
   (a) `hide()` (b) `hide(on)` (c) `invisible()` (d) `display(none)` *(NEB 2080)*
5. Which keyword declares a block-scoped variable in modern JavaScript? <span class="marks">[1]</span>
   (a) `var` (b) `let` (c) `dim` (d) `int`
6. JavaScript is which kind of scripting language? <span class="marks">[1]</span>
   (a) server-side only (b) client-side (c) compiled (d) markup
7. Which operator in JavaScript tests value **and** type? <span class="marks">[1]</span>
   (a) `=` (b) `==` (c) `===` (d) `!=`
8. Which jQuery statement runs code only after the page has loaded? <span class="marks">[1]</span>
   (a) `$(document).ready(function(){ ... });` (b) `$(window).load;` (c) `$.start();` (d) `$(page).begin();`
9. Which method writes text directly into the HTML document? <span class="marks">[1]</span>
   (a) `document.write()` (b) `window.print()` (c) `console.log()` (d) `document.getElementById()`

::: note Answers — Set B
**1.** (a) — `<script>` takes `src`, exactly like `<img>`.
**2.** (d) — `alert()` is the built-in dialog; `confirm()` asks OK/Cancel instead.
**3.** (c) — `$` is an alias for the `jQuery` function.
**4.** (a) — `$("p").hide();`
**5.** (b) — `let` (and `const`) are block-scoped; `var` is function-scoped.
**6.** (b) — it runs inside the browser; PHP runs on the server.
**7.** (c) — `===` is strict equality, so `"5" === 5` is false.
**8.** (a) — the ready handler waits for the DOM.
**9.** (a) — `console.log()` writes to the console, not the page.
:::

**Set C — PHP, MySQL connectivity and XML**

1. Which of the following is the correct way of defining a variable in PHP? <span class="marks">[1]</span>
   (a) `$variable name = value;` (b) `$variable_name = value;` (c) `$variable_name = value` (d) `$variable name as value;` *(NEB 2079)*
2. Which function is used to connect to a MySQL database? <span class="marks">[1]</span>
   (a) `mysqli_open()` (b) `mysqli_connect()` (c) `var mysqli_query()` (d) `$mysqli_con()` *(NEB 2080)*
3. Every PHP statement must end with <span class="marks">[1]</span>
   (a) a full stop (b) a semicolon (c) a colon (d) nothing
4. PHP code is enclosed in <span class="marks">[1]</span>
   (a) `<php> ... </php>` (b) `<?php ... ?>` (c) `<script> ... </script>` (d) `{{ ... }}`
5. Which PHP function runs an SQL query on an open connection? <span class="marks">[1]</span>
   (a) `mysqli_query()` (b) `mysqli_fetch()` (c) `mysqli_run()` (d) `mysqli_exec()`
6. Which superglobal array carries data submitted by a form using the POST
   method? <span class="marks">[1]</span>
   (a) `$_GET` (b) `$_POST` (c) `$_FORM` (d) `$_REQUESTED`
7. PHP is executed <span class="marks">[1]</span>
   (a) in the browser (b) on the web server (c) in the database engine (d) in the operating system kernel
8. XML differs from HTML mainly because XML <span class="marks">[1]</span>
   (a) displays data (b) describes and carries data with user-defined tags (c) has a fixed tag set (d) cannot be nested
9. Which protocol transfers web pages securely between browser and server? <span class="marks">[1]</span>
   (a) HTTP (b) HTTPS (c) FTP (d) SMTP

::: note Answers — Set C
**1.** (b) — a PHP variable name starts with `$`, cannot contain a space, and the statement needs its semicolon.
**2.** (b) — `mysqli_connect($server, $user, $pass, $db);`
**3.** (b) — the semicolon is the statement terminator.
**4.** (b) — the short opening tag `<?php` and closing `?>`.
**5.** (a) — `mysqli_query($conn, $sql);`
**6.** (b) — `$_POST['name']` reads a posted field.
**7.** (b) — PHP is server-side; the browser only ever sees its output.
**8.** (b) — XML tags are invented by the author and carry meaning, not layout.
**9.** (b) — HTTPS is HTTP inside TLS.
:::

## 14.5 Unit 4: Programming in C

Twelve teaching hours and three of the 27 verified MCQs — but Group C almost
always carries a C program worth five to eight marks, so the objective questions
here are also revision for the biggest single answer on the paper. Every output
shown in the answer keys below was obtained by compiling and running the code
with `gcc`.

**Set A — data types, operators and control flow**

1. Which of the following is a valid C identifier? <span class="marks">[1]</span>
   (a) `2sum` (b) `total_marks` (c) `total marks` (d) `int`
2. On a typical 64-bit compiler, `sizeof(int)` evaluates to <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 4 (d) 8
3. What does `10 % 3` evaluate to in C? <span class="marks">[1]</span>
   (a) 3 (b) 1 (c) 3.33 (d) 0
4. Which operator has the highest precedence among these? <span class="marks">[1]</span>
   (a) `+` (b) `*` (c) `=` (d) `&&`
5. `int x = 5; printf("%d", x++);` prints <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) nothing
6. Which loop is guaranteed to execute its body at least once? <span class="marks">[1]</span>
   (a) `for` (b) `while` (c) `do...while` (d) nested `for`
7. Which statement skips the rest of the current iteration and starts the next? <span class="marks">[1]</span>
   (a) `break` (b) `continue` (c) `goto` (d) `return`
8. The `switch` expression in standard C may be of which type? <span class="marks">[1]</span>
   (a) `float` (b) `double` (c) `int` or `char` (d) any type
9. Which format specifier prints a `float` value? <span class="marks">[1]</span>
   (a) `%d` (b) `%c` (c) `%f` (d) `%s`

::: note Answers — Set A
**1.** (b) — an identifier may not start with a digit, contain a space, or be a keyword.
**2.** (c) — verified: `printf("%d", (int)sizeof(int));` printed `4`.
**3.** (b) — `%` gives the remainder, `10/3` gives the quotient 3.
**4.** (b) — multiplicative operators bind tighter than additive, logical or assignment.
**5.** (b) — verified: the post-increment prints the old value 5, then `x` becomes 6.
**6.** (c) — `do...while` tests its condition after the body.
**7.** (b) — `break` leaves the loop, `continue` only ends the current pass.
**8.** (c) — `switch` needs an integral expression.
**9.** (c) — `%f` for `float` and `double`, `%d` for `int`, `%c` for `char`.
:::

**Set B — functions, arrays and strings**

1. In C, the execution of a program always begins from <span class="marks">[1]</span>
   (a) the first function defined (b) the `main()` function (c) the last function (d) any function
2. Passing a variable to a function so that changes inside the function affect
   the caller's variable is called <span class="marks">[1]</span>
   (a) call by value (b) call by reference (c) call by name (d) call by result
3. The valid index range of `int a[5];` is <span class="marks">[1]</span>
   (a) 1 to 5 (b) 0 to 5 (c) 0 to 4 (d) 1 to 4
4. For `int arr[5] = {1,2,3,4,5};` the value of `arr[2]` is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) undefined
5. For `char str[] = "NEB";` the value of `sizeof(str)` is <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 5 (d) 8
6. Which function returns the number of characters in a string, not counting the
   terminator? <span class="marks">[1]</span>
   (a) `strlen()` (b) `strcpy()` (c) `strcat()` (d) `strcmp()`
7. Which header file must be included to use `strlen()`? <span class="marks">[1]</span>
   (a) `stdio.h` (b) `string.h` (c) `conio.h` (d) `stdlib.h`
8. A function that calls itself is called <span class="marks">[1]</span>
   (a) inline (b) nested (c) recursive (d) static
9. `float area(float r);` written before `main()` is a <span class="marks">[1]</span>
   (a) function definition (b) function prototype (c) function call (d) macro

::: note Answers — Set B
**1.** (b) — `main()` is the entry point wherever it is written in the file.
**2.** (b) — call by reference passes the address, so the function edits the original.
**3.** (c) — C array indices start at 0, so the last is `n-1`.
**4.** (b) — verified: printing `arr[2]` gave `3`.
**5.** (b) — verified: `sizeof` gave `4` (three letters plus `'\0'`) while `strlen` gave `3`.
**6.** (a) — `strlen("NEB")` is 3.
**7.** (b) — all the `str...` functions are declared in `string.h`.
**8.** (c) — recursion needs a base case or it never stops.
**9.** (b) — a prototype declares the return type and parameters, and ends with a semicolon.
:::

**Set C — pointers, structures and files**

1. Which of the following is true about `FILE *fpt;`? <span class="marks">[1]</span>
   (a) `FILE` is a keyword in C for representing files and `fpt` is a variable of `FILE` type (b) `FILE` is a buffered stream (c) `FILE` is a stream (d) `FILE` is a structure and `fpt` is a pointer to the structure of `FILE` type *(NEB 2080)*
2. What is the output of `void main(){ int b=25; int *p; p=&b; printf("%d %d", &b, p); }`? <span class="marks">[1]</span>
   (a) `25 25` (b) the same address printed twice (c) `25` then an address (d) an address then `25` *(NEB 2079)*
3. The operator that returns the address of a variable is <span class="marks">[1]</span>
   (a) `*` (b) `&` (c) `->` (d) `.`
4. If `int a[5] = {2,4,6,8,10};` and `int *q = a;`, then `*(q+3)` is <span class="marks">[1]</span>
   (a) 4 (b) 6 (c) 8 (d) 10
5. A member of a structure is accessed through a structure **pointer** using <span class="marks">[1]</span>
   (a) `.` (b) `->` (c) `::` (d) `*`
6. Which keyword defines a user-defined data type that groups different types
   together? <span class="marks">[1]</span>
   (a) `array` (b) `struct` (c) `enum` (d) `typedef`
7. In a `union`, all the members <span class="marks">[1]</span>
   (a) have separate memory (b) share the same memory location (c) must be of the same type (d) cannot be accessed
8. Which mode opens a file for writing and erases any existing contents? <span class="marks">[1]</span>
   (a) `"r"` (b) `"w"` (c) `"a"` (d) `"r+"`
9. Which function closes an open file? <span class="marks">[1]</span>
   (a) `fclose()` (b) `fend()` (c) `close()` (d) `fstop()`

::: note Answers — Set C
**1.** (d) — `FILE` is a `typedef` for a structure, so `fpt` is a pointer to that structure.
**2.** (b) — verified: `&b` and `p` hold the same address, so both fields print identically. (Strictly, `%d` on a pointer is wrong; `%p` is correct.)
**3.** (b) — `&b` is "address of b", `*p` is "value at p".
**4.** (c) — verified: `*(q+3)` printed `8`, the fourth element.
**5.** (b) — `sp->roll` is shorthand for `(*sp).roll`.
**6.** (b) — a `struct` bundles members of different types under one name.
**7.** (b) — a union is exactly as large as its biggest member.
**8.** (b) — `"w"` truncates; `"a"` appends; `"r"` fails if the file is absent.
**9.** (a) — `fclose(fp);` flushes the buffer and releases the handle.
:::

## 14.6 Unit 5: Object-Oriented Programming

Ten teaching hours and two of the 27 verified MCQs. Both were about the four
pillars — and in fact every OOP objective question the papers have asked so far
can be answered by someone who can say, in one sentence each, what
encapsulation, inheritance, polymorphism and abstraction mean.

**Set A — the four pillars**

1. Which feature of OOP illustrates code reusability? <span class="marks">[1]</span>
   (a) polymorphism (b) abstraction (c) encapsulation (d) inheritance *(NEB 2079)*
2. Where is a class derived in inheritance? <span class="marks">[1]</span>
   (a) superclass (b) subclass (c) subset class (d) relative class *(NEB model question)*
3. Wrapping data and the functions that operate on it into a single unit is <span class="marks">[1]</span>
   (a) inheritance (b) encapsulation (c) polymorphism (d) overloading
4. Showing only the essential features and hiding the internal detail is <span class="marks">[1]</span>
   (a) abstraction (b) encapsulation (c) inheritance (d) instantiation
5. "One interface, many implementations" describes <span class="marks">[1]</span>
   (a) encapsulation (b) abstraction (c) polymorphism (d) modularity
6. Two functions in the same class with the same name but different parameter
   lists is an example of <span class="marks">[1]</span>
   (a) function overriding (b) function overloading (c) recursion (d) inheritance
7. A class is best described as <span class="marks">[1]</span>
   (a) an object in memory (b) a blueprint from which objects are created (c) a function (d) a variable
8. Which access specifier makes a member visible to derived classes but not to
   the outside world? <span class="marks">[1]</span>
   (a) `public` (b) `private` (c) `protected` (d) `static`
9. Which of the following is **not** a feature of object-oriented programming? <span class="marks">[1]</span>
   (a) inheritance (b) polymorphism (c) goto statement (d) data hiding

::: note Answers — Set A
**1.** (d) — a derived class reuses the code of its base class without rewriting it.
**2.** (b) — the derived class is the subclass; the class it derives *from* is the superclass.
**3.** (b) — encapsulation binds data with its methods and hides the data behind them.
**4.** (a) — abstraction is about the interface; encapsulation is about the wrapping.
**5.** (c) — polymorphism lets the same call behave differently by object type.
**6.** (b) — overloading is compile-time; overriding needs inheritance and is run-time.
**7.** (b) — the class is the template, the object is the instance.
**8.** (c) — `protected` is visible inside the class and its descendants.
**9.** (c) — `goto` is an unstructured jump and belongs to no OOP principle.
:::

**Set B — objects, constructors and paradigms**

1. Creating an object from a class is called <span class="marks">[1]</span>
   (a) declaration (b) instantiation (c) inheritance (d) compilation
2. A special member function that runs automatically when an object is created
   is a <span class="marks">[1]</span>
   (a) destructor (b) constructor (c) friend function (d) virtual function
3. A constructor has which return type? <span class="marks">[1]</span>
   (a) `void` (b) `int` (c) the class type (d) none at all
4. In procedural programming, a program is divided into <span class="marks">[1]</span>
   (a) objects (b) functions (c) classes (d) packages
5. Which of these is a purely object-oriented way of protecting data? <span class="marks">[1]</span>
   (a) global variables (b) making members `private` and exposing `public` methods (c) using `goto` (d) using macros
6. Inheriting from more than one base class is called <span class="marks">[1]</span>
   (a) single inheritance (b) multilevel inheritance (c) multiple inheritance (d) hierarchical inheritance
7. A function that is declared in the base class and redefined in the derived
   class with the same signature demonstrates <span class="marks">[1]</span>
   (a) overloading (b) overriding (c) hiding (d) nesting
8. Which of the following is an object-oriented language? <span class="marks">[1]</span>
   (a) C (b) COBOL (c) Java (d) FORTRAN 77
9. Data hiding in OOP mainly improves <span class="marks">[1]</span>
   (a) execution speed (b) security and maintainability (c) file size (d) network bandwidth

::: note Answers — Set B
**1.** (b) — `Student s;` instantiates the class `Student`.
**2.** (b) — the constructor initialises the object's data members.
**3.** (d) — a constructor declares no return type, not even `void`.
**4.** (b) — procedural code is a set of functions acting on shared data.
**5.** (b) — private data plus public accessors is the standard idiom.
**6.** (c) — multiple inheritance takes from two or more bases at once.
**7.** (b) — same name, same parameters, different class level = overriding.
**8.** (c) — C, COBOL and FORTRAN 77 are procedural.
**9.** (b) — hidden data cannot be corrupted from outside the class.
:::

## 14.7 Unit 6: Software Process Model

Ten teaching hours and three of the 27 verified MCQs — one in every paper this
book could verify. The examiner keeps returning to the same two things: the
**order** of the SDLC phases, and which phase does what.

**Set A — the SDLC and its phases**

1. Which of these is the correct order of the SDLC? <span class="marks">[1]</span>
   (a) analysis, design, coding, testing, implementation (b) analysis, design, testing, implementation, coding (c) implementation, coding, analysis, design, testing (d) design, testing, implementation, coding, analysis *(NEB model question)*
2. Which SDLC phase is used to ensure quality software? <span class="marks">[1]</span>
   (a) implementation (b) maintenance (c) testing (d) system study *(NEB 2080)*
3. Which activity discovers the requirements from the user during requirement
   collection? <span class="marks">[1]</span>
   (a) feasibility study (b) requirement elicitation (c) requirement specification (d) requirement validation *(NEB 2079)*
4. Which is normally the **longest and most expensive** phase over the whole
   life of a system? <span class="marks">[1]</span>
   (a) analysis (b) design (c) coding (d) maintenance
5. A study that asks whether the organisation can afford the proposed system is <span class="marks">[1]</span>
   (a) technical feasibility (b) economic feasibility (c) operational feasibility (d) legal feasibility
6. The document that records exactly what the system must do is the <span class="marks">[1]</span>
   (a) DFD (b) SRS (c) ERD (d) user manual
7. Converting the design into actual program code happens in which phase? <span class="marks">[1]</span>
   (a) analysis (b) design (c) coding (d) testing
8. Running the old and the new system side by side for a period is which
   changeover method? <span class="marks">[1]</span>
   (a) direct (b) parallel (c) phased (d) pilot
9. A data flow diagram is produced mainly during <span class="marks">[1]</span>
   (a) system analysis (b) coding (c) maintenance (d) testing

::: note Answers — Set A
**1.** (a) — you cannot test code that has not been written, nor implement what has not been tested.
**2.** (c) — testing is the quality gate before release.
**3.** (b) — elicitation is the *gathering*; specification writes it down; validation checks it.
**4.** (d) — maintenance typically consumes more than half the whole-life cost.
**5.** (b) — economic feasibility is the cost-benefit question.
**6.** (b) — Software Requirement Specification.
**7.** (c) — coding, sometimes called implementation of the design.
**8.** (b) — parallel running is the safest but the most expensive changeover.
**9.** (a) — a DFD models the flow of data through the existing and proposed system.
:::

**Set B — process models**

1. Which model completes each phase fully before the next begins and does not
   easily allow going back? <span class="marks">[1]</span>
   (a) waterfall (b) spiral (c) prototype (d) agile
2. Which model is driven by **risk analysis** at the start of every cycle? <span class="marks">[1]</span>
   (a) waterfall (b) spiral (c) V-model (d) big-bang
3. Which model builds a quick working mock-up so that the user can refine the
   requirements? <span class="marks">[1]</span>
   (a) waterfall (b) prototyping (c) V-model (d) incremental
4. The waterfall model is most suitable when <span class="marks">[1]</span>
   (a) requirements are unclear and change often (b) requirements are well understood and stable (c) the project is very large and risky (d) the user is unavailable
5. Which model delivers the software in successive usable builds? <span class="marks">[1]</span>
   (a) incremental (b) waterfall (c) V-model (d) build-and-fix
6. Testing the system as a whole against the requirements is <span class="marks">[1]</span>
   (a) unit testing (b) integration testing (c) system testing (d) regression testing
7. Testing carried out by the customer at the customer's own site before
   acceptance is <span class="marks">[1]</span>
   (a) alpha testing (b) beta testing (c) unit testing (d) stress testing
8. Testing an individual function or module in isolation is <span class="marks">[1]</span>
   (a) unit testing (b) system testing (c) acceptance testing (d) load testing
9. The main disadvantage of the waterfall model is that <span class="marks">[1]</span>
   (a) it has no documentation (b) a requirement error found late is very costly to fix (c) it cannot be planned (d) it needs no testing

::: note Answers — Set B
**1.** (a) — the waterfall flows one way, which is its strength and its weakness.
**2.** (b) — each spiral loop is plan, risk-analyse, engineer, evaluate.
**3.** (b) — the prototype is thrown away or evolved once requirements are agreed.
**4.** (b) — stable, well-understood requirements are exactly what the waterfall needs.
**5.** (a) — the incremental model ships a working subset, then adds to it.
**6.** (c) — system testing checks the integrated whole against the SRS.
**7.** (b) — alpha testing is at the developer's site, beta at the customer's.
**8.** (a) — unit testing is the smallest testable piece.
**9.** (b) — the cost of correcting a requirement grows with the phase it is found in.
:::

## 14.8 Unit 7: Recent Trends in Technology

Nine teaching hours, the shortest unit, and two of the 27 verified MCQs. It is
also the easiest unit in which to score, because the questions are definitional.
Both verified items — sensors in IoT, and why cloud computing is popular — could
be answered from the first sentence of the definition.

**Set A — cloud, AI and IoT**

1. Why is cloud computing popular nowadays? <span class="marks">[1]</span>
   (a) cost-sharing and easily accessible (b) modern technology and costly (c) accessible and freely available (d) affordable to all *(NEB model question)*
2. What devices detect and respond to changes in an environment, are embedded in
   smart phones, and are an integral part of the Internet of Things? <span class="marks">[1]</span>
   (a) Wi-Fi (b) barcode (c) RFID (d) sensors *(NEB 2079)*
3. Renting a virtual machine on which you install your own operating system is
   which cloud service model? <span class="marks">[1]</span>
   (a) SaaS (b) PaaS (c) IaaS (d) DaaS
4. Gmail and Google Docs are examples of <span class="marks">[1]</span>
   (a) IaaS (b) PaaS (c) SaaS (d) a private cloud
5. A cloud used exclusively by a single organisation is a <span class="marks">[1]</span>
   (a) public cloud (b) private cloud (c) hybrid cloud (d) community cloud
6. The branch of AI in which a system improves its performance from data without
   being explicitly programmed is <span class="marks">[1]</span>
   (a) machine learning (b) robotics (c) expert systems (d) computer vision
7. A program that answers customer questions in natural language is an
   application of <span class="marks">[1]</span>
   (a) natural language processing (b) data mining (c) virtual reality (d) cryptography
8. In the Internet of Things, the component that gives every object a unique
   identity on the network is its <span class="marks">[1]</span>
   (a) sensor (b) actuator (c) IP address (d) battery
9. An **actuator** in an IoT system <span class="marks">[1]</span>
   (a) measures a physical quantity (b) converts a control signal into a physical action (c) stores data in the cloud (d) encrypts the data

::: note Answers — Set A
**1.** (a) — many users share one pool of resources, so the cost per user falls and the service is reachable from anywhere.
**2.** (d) — sensors are the input organs of IoT; RFID only identifies, it does not sense change.
**3.** (c) — Infrastructure as a Service hands you raw compute and storage.
**4.** (c) — Software as a Service: the finished application, in the browser.
**5.** (b) — a private cloud is single-tenant, on or off premises.
**6.** (a) — machine learning generalises from examples.
**7.** (a) — NLP covers chatbots, translation and sentiment analysis.
**8.** (c) — without an address the "thing" cannot be reached over the Internet.
**9.** (b) — sensors read the world, actuators change it (a motor, a valve, a relay).
:::

**Set B — mobile computing, big data, virtual reality and e-commerce**

1. Which generation of mobile technology first made high-speed mobile broadband
   ordinary? <span class="marks">[1]</span>
   (a) 1G (b) 2G (c) 3G (d) 4G
2. Computing that lets a user access data and services while moving is <span class="marks">[1]</span>
   (a) grid computing (b) mobile computing (c) parallel computing (d) batch processing
3. The three classic "V"s of big data are <span class="marks">[1]</span>
   (a) volume, velocity, variety (b) volume, value, vision (c) variety, virtue, velocity (d) volume, virtual, verified
4. A computer-generated environment that a user can move inside and interact
   with is <span class="marks">[1]</span>
   (a) augmented reality (b) virtual reality (c) simulation modelling (d) teleconferencing
5. Overlaying digital information on a view of the real world is <span class="marks">[1]</span>
   (a) virtual reality (b) augmented reality (c) holography (d) animation
6. Buying and selling goods over the Internet is <span class="marks">[1]</span>
   (a) e-governance (b) e-commerce (c) e-learning (d) e-mail
7. An online store selling directly to individual shoppers is which e-commerce
   model? <span class="marks">[1]</span>
   (a) B2B (b) B2C (c) C2C (d) G2C
8. A distributed, tamper-evident ledger shared across many computers is <span class="marks">[1]</span>
   (a) a data warehouse (b) blockchain (c) a relational database (d) a spreadsheet
9. Which of the following is the best example of an embedded system? <span class="marks">[1]</span>
   (a) a desktop PC (b) the controller inside a washing machine (c) a web browser (d) a spreadsheet package

::: note Answers — Set B
**1.** (c) — 3G introduced mobile broadband; 4G made it fast enough for video everywhere.
**2.** (b) — mobile computing is computing without a fixed physical link.
**3.** (a) — volume (how much), velocity (how fast), variety (how many forms).
**4.** (b) — VR replaces the world; AR adds to it.
**5.** (b) — a phone camera view with directions drawn on it is AR.
**6.** (b) — electronic commerce.
**7.** (b) — business to consumer.
**8.** (b) — each block carries the hash of the previous one, so tampering shows.
**9.** (b) — an embedded system is a computer dedicated to one task inside a larger device.
:::

## 14.9 Distractor analysis: how the wrong options are built

An examiner writing a one-mark item does not invent three random wrong answers.
The wrong options — the **distractors** — are chosen so that each one catches a
particular misunderstanding. Once you can name the trick, the item stops being a
guess. Across the 27 verified questions in this bank, five patterns account for
almost every distractor.

**1. The neighbouring term.** The distractor is the concept one shelf along.
`DELETE`/`DROP`. Alpha/beta testing. Subclass/superclass. Elicitation /
specification / validation. Encapsulation / abstraction. These are the most
dangerous distractors, because you half-know them.

*Defence:* for every pair of terms you meet, write one sentence that names the
difference, not two sentences that define each separately. "`DELETE` removes
rows and keeps the table; `DROP` removes the table."

**2. The plausible-looking syntax.** `hide(on)`, `invisible()`,
`display(none)`, `mysqli_open()`, `alert-box("...")`, `<js src="...">`. Every one
of these reads like something that might exist. None does.

*Defence:* type the real syntax at least once. A distractor only works on a
candidate who has read the syntax and never written it.

**3. The off-by-one or out-of-range number.** `257.2.5.1` and `202.70.71.262` in
the IPv4 item; 255 instead of 254 usable hosts; index 0 to 5 instead of 0 to 4;
`sizeof("NEB")` as 3 instead of 4.

*Defence:* when a number appears in the options, check the boundary before you
check the value. Is it in range? Does it count from zero? Does it include the
terminator, the network address, the broadcast address?

**4. The true-but-irrelevant statement.** In the `FILE *fpt` item, options (b)
and (c) — "`FILE` is a buffered stream", "`FILE` is a stream" — are things a
textbook does say. They are simply not what the *declaration* means.

*Defence:* re-read the stem. The question asked what `FILE *fpt` is, not what a
file is. Underline the actual subject of the question before scanning the
options.

::: example Working a real item: reading the stem before the options
The NEB 2080 paper asked what is true about `FILE *fpt;`. Three of the four
options are sentences that a textbook really does contain:

- "`FILE` is a keyword in C for representing files and `fpt` is a variable of
  `FILE` type"
- "`FILE` is a buffered stream"
- "`FILE` is a stream"
- "`FILE` is a structure and `fpt` is a pointer to the structure of `FILE` type"

The stem is not asking what a file is, or what a stream is. It is asking what the
**declaration** `FILE *fpt;` means. Take it apart:

- `FILE` is not a C keyword. C has 32 keywords and `FILE` is not among them; it
  is a `typedef` name defined inside `stdio.h`. That kills the first option, and
  it also kills the idea that `fpt` is "a variable of `FILE` type".
- The `*` in the declaration means `fpt` is a **pointer**, not a `FILE`.
- Whether a stream is buffered is true of the *stream*, not of the declaration.

Only the last option describes the declaration: `FILE` is a structure type and
`fpt` points to it. Answer **(d)**.

The transferable habit: underline the exact grammatical subject of the stem —
here, the declaration — before your eye reaches the options. Half of Group A's
difficulty is options answering a question that was not asked.
:::

**5. The over-general option.** "All of them", "any type", "affordable to all".
In the verified coaxial-cable item, "all of them" is offered and is wrong.

::: caution "All of the above" is not a safe default
Some coaching notes teach that "all of the above" is usually right. In the
verified NEB papers it was offered once and was **wrong**. Judge it on the
content, not on folklore.
:::

::: tip A rule that is worth two or three marks
Do Group A twice. On the first pass answer only the items you are certain of,
and put a light pencil dot beside the rest. On the second pass — after Group B,
when your memory of the syllabus has been warmed up by writing about it — come
back to the dotted ones. Candidates regularly recover a mark or two this way,
because a term that would not come in minute four comes easily in minute
seventy.
:::

## Chapter summary

- Group A is **9 marks of 50** — 18% of the written paper — with no partial
  credit and no second chance.
- Across the three verified papers, **Web Technology II supplied 8 of 27 MCQs**,
  more than any other unit, although it is not the largest unit by teaching
  hours. Syntax makes good one-mark questions.
- DBMS supplied 5, Networking 4, Programming in C 3, Software Process Model 3,
  OOP 2 and Recent Trends 2.
- The whole of Software Process Model's MCQ history is about the **order** of
  the SDLC phases and **which phase does what**.
- Distractors are built to catch five specific errors: the neighbouring term,
  invented syntax, an out-of-range number, a true-but-irrelevant statement, and
  the over-general option.
- Never leave a Group A item blank. There is no negative marking in the NEB
  scheme, so an eliminated guess between two options is worth half a mark on
  average and a blank is worth nothing.

::: note Sources reached for this chapter
- **NEB 2080 (2023), Computer Science, Sub. Code 4281, "New course", 2 hrs, Full
  Marks 50** — the original scanned question paper, read page by page. All nine
  Group A items in this chapter tagged *(NEB 2080)* are transcribed from it.
- **NEB 2079 Grade 12 Computer examination paper**, published with worked
  solutions at nepalieducate.com. The nine items tagged *(NEB 2079)* come from
  it. Note that the published solution to the `DELETE`/`DROP` item is wrong; the
  answer given in this chapter is the correct one.
- **NEB Grade 12 Computer model question** for the new course (Group A 9×1,
  Group B 5×5, Group C 2×8), same source. Items tagged *(NEB model question)*
  come from it.
- **NEB Grade 12 Computer Science curriculum**, units and teaching hours, as
  used throughout this book.
- **Could not be verified:** the 2078 and 2081 Computer Science papers were not
  reachable, and neb.gov.np's model-question repository did not respond. No
  question in this chapter is tagged with either of those years. One item in the
  model question (the `<A>` tag) listed "create a link" and "create a hyperlink"
  as separate options; it is reproduced here in corrected form and marked as
  adapted. One model-question item depended on a program image that could not be
  recovered, and is not reproduced.
:::

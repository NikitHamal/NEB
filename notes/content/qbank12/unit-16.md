---
subject: Question Bank
grade: 12
unit: 16
title: "Computer Science: Model Question Sets and Predicted Questions"
hours: 0
area: Computer Science
---

The Computer Science paper is short (two hours, 50 marks) and, unlike most papers,
**extremely regular**. This chapter rests on seven papers: NEB 2079, NEB 2080 (only partly
recovered), the 2080 supplementary, NEB 2081, NEB 2082, NEB 2083, and the Curriculum
Development Centre's model question — the last six read in full. Laid side by side,
they show that almost every slot of the paper asks about the same syllabus unit every
year. Once you see that, revision stops being a hunt through 80 teaching hours and
becomes the preparation of about a dozen answers you can write from memory.

The chapter has four parts. **16.1** is the pattern analysis — the slot map, the unit
weights and the question types that come back. **16.2** and **16.3** are two complete
model papers built to the exact grid (9 MCQs, five 5-mark questions, two 8-mark
questions), each fully solved. **16.4** is a ranked list of 46 predicted questions,
every one with the reason it is ranked where it is and a model answer.

Every program in this chapter was compiled and run. C programs were built with
`gcc -Wall`, the C++ snippets with `g++`, the JavaScript was executed under Node with
`document.write` and `prompt` supplied, and the PHP scripts were run against a real
MariaDB server. The SQL outputs are pasted from a real session. Where an output is
printed under a listing, it is the output the program produced.

::: key How to read the year tags
`(NEB 2083)` means the question was read in that paper. `(2080 supplementary)` is the
supplementary-examination paper. `(CDC model)` is the Curriculum Development Centre's
model question. Nothing in this chapter is a claim about the coming paper: the
predicted questions are ranked by how often and how recently a question type has
appeared, and each one says so.
:::

## 16.1 Pattern analysis of the Grade 12 Computer Science papers

### 16.1.1 The grid, and what has not changed

| Group | Questions | Marks each | Total | What is asked |
|---|---|---|---|---|
| A | 1–9 | 1 | 9 | multiple choice, all compulsory |
| B | 10–14 | 5 | 25 | five questions; Q10 and Q11 each offer an *or* choice |
| C | 15–16 | 8 | 16 | two questions; Q16 offers an *or* choice |
| **Total** | **16** | | **50** | time 2 hours, pass marks 20 |

The marking scheme is often printed in the bracket after the question: *(1+4)*,
*(2+3)*, *(2.5+2.5)*, *(3+5)*, *(2+6)*. The first number is the definition or the
introductory part and the remaining numbers are the body. Answer to the bracket —
the examiner awards marks to the parts, not to the page.

### 16.1.2 The slot map: what each question number asked

The table below was assembled question by question from the seven papers. Only the
main wording is given; *or* alternatives are separated by a slash. A dash means that
slot of that paper could not be recovered for this book.

| Slot | Unit | 2079 | 2080 | 2080 supp. | 2081 | 2082 | 2083 | CDC model |
|---|---|---|---|---|---|---|---|---|
| Q10 | DBMS | centralized vs distributed / purposes of normalization, 2NF example | relational model / SQL create, alter, drop | importance of database / relational model | advantages of DBMS over files / 1NF vs 2NF | DDL vs DML / normalization, 2NF and 3NF | hierarchical vs relational / 2NF with example | centralized vs distributed for a bank / why relational |
| Q11 | Web Technology II | JavaScript factorial / PHP fetch data | JavaScript factorial / PHP insert into studentDB | JavaScript largest of three / PHP connect to MySQL | JavaScript even or odd / `mysqli_connect()` | JavaScript smallest of three / PHP connect to MySQL | JavaScript smallest of three / PHP school.student as HTML table | JavaScript swap / PHP connect |
| Q12 | OOP | OOP vs procedural | — | inheritance with example | class and object | class and inheritance | what is OOP, four features | object-oriented vs procedural |
| Q13 | Software process | activities of software design | importance of system testing | requirement collection methods | requirement gathering techniques | requirement gathering methods | technical and economic feasibility | five qualities of good software |
| Q14 | Recent trends | five areas of AI | — | cloud computing services | five AI examples in education | AI in education | cloud computing, three advantages | mobile computing |
| Q15 | Networking (8) | star vs ring, cable for LAN | topology; guided vs unguided media | CAT-6 and optical fibre | star vs bus | transmission media | twisted pair, coaxial, fibre | client-server architecture |
| Q16 | C (8) | structure, 5 students / file `emp.txt` | pointer advantage and area of a football by function | structure, 5 students / pointer and file | structure, 5 books / binary file, `fwrite()`, `getw()` | array of structure, 10 customers / function components, call by value and reference | positive/negative/zero and Fibonacci by function / array of structure, 10 students | structure, 12 students / data file `score.dat` |

Three facts jump out of this table and all three are safe to revise against.

1. **Each slot belongs to one unit.** Q10 is DBMS, Q11 is web, Q12 is OOP, Q13 is the
   software process, Q14 is recent trends, Q15 is networking and Q16 is C. This held
   in every paper, so far as each could be read.
2. **Q15 is always about the physical network** — topologies (2079, 2081, 2080),
   transmission media (2080, 2080 supp., 2082, 2083) or an architecture (model).
3. **Q16 is always a C program** — structures or an array of structures in six of the
   seven papers, with file handling or a function/pointer question as the *or* choice.

```figure caption="Marks carried by each unit in a typical paper. Group A follows the pattern seen in every paper read: two DBMS, one networking, two web, one C, one OOP, one software process and one recent-trends item. The written marks follow the slot map above. Networking and C carry 9 marks each."
import numpy as np, matplotlib.pyplot as plt

units = ["Networking", "Programming in C", "DBMS", "Web Technology II",
         "OOP", "Software process", "Recent trends"]
ga = [1, 1, 2, 2, 1, 1, 1]
wr = [8, 8, 5, 5, 5, 5, 5]
y = np.arange(len(units))[::-1]

fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.barh(y, ga, height=0.56, color=SERIES[1], label="Group A (MCQ)")
ax.barh(y, wr, left=ga, height=0.56, color=ACCENT, label="Group B / C (written)")
for yi, a, w in zip(y, ga, wr):
    ax.text(a + w + 0.15, yi, f"{a + w}", va="center", ha="left",
            fontsize=8.5, fontweight="bold", color=INK)
ax.set_yticks(y)
ax.set_yticklabels(units, fontsize=8)
ax.set_xlim(0, 11)
ax.set_xticks([0, 2, 4, 6, 8, 10])
ax.set_xlabel("Marks out of 50", fontsize=8)
ax.tick_params(labelsize=8, length=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.xaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
ax.legend(fontsize=7.4, frameon=False, loc="lower right")
fig.tight_layout()
```

### 16.1.3 Unit by unit: marks carried, years seen, expected weight

| Unit | Teaching hours | Group A items per paper | Written marks per paper | Marks per paper | Seen in (of 7 papers) | Expected weight |
|---|---|---|---|---|---|---|
| 1. DBMS | 12 | 2 | 5 (Q10) | 7 | 7 of 7 | normalization (2NF) is in 4 of 7; DDL/DML, the models and database types fill the rest |
| 2. Networking | 15 | 1 | 8 (Q15) | 9 | 7 of 7 | topologies or cables, almost never anything else |
| 3. Web Technology II | 12 | 2 | 5 (Q11) | 7 | 7 of 7 | one JavaScript program *or* one PHP–MySQL script |
| 4. Programming in C | 12 | 1 | 8 (Q16) | 9 | 7 of 7 | structure + display; file handling as the alternative |
| 5. OOP | 10 | 1 | 5 (Q12) | 6 | 6 of 7 checked | features, class/object, inheritance, comparison with procedural |
| 6. Software process | 10 | 1 | 5 (Q13) | 6 | 7 of 7 | requirement gathering (3 papers), feasibility, testing, design, quality |
| 7. Recent trends | 9 | 1 | 5 (Q14) | 6 | 6 of 7 checked | AI (3 papers), cloud (2), mobile computing (1) |

The Group A column is exact for NEB 2079, 2080 supplementary, 2081, 2082 and 2083:
in **each** of those five papers the nine items split 2–1–2–1–1–1–1 across the units
in the order DBMS, networking, web, C, OOP, software process, recent trends. The CDC
model question was heavier on DBMS and web (three items each) and had none on C or
recent trends, which is a reminder that a *model* question is a sample of the style,
not a template of the weights.

::: tip What the table means for the last week
The written marks alone are **41 of 50**, and 17 of them (Q15 + Q16) depend on two
units. A candidate who can draw and compare the three topologies, list the three
guided media with their advantages and disadvantages, and write a structure program,
a file program and a function program from memory has secured about 20 of the 50
marks — the pass mark — before touching anything else. Start there.
:::

### 16.1.4 Question types that return

| Type | Seen | Answer form the examiner rewards |
|---|---|---|
| Array of structure: read *n* records and display | 2079, 2080 supp., 2081, 2082, 2083, model | `struct` declaration, array, input loop, output loop, `main()` |
| File handling: write and read a data file | 2079, 2080 supp., 2081, model | `fopen` mode, `fprintf`/`fscanf` or `fwrite`/`fread`, `fclose`, read loop |
| Requirement gathering methods | 2080 supp., 2081, 2082 | named methods, one or two lines each, advantage/limitation |
| Star, bus or ring topology compared | 2079, 2081, 2080 | diagram + table of advantages and disadvantages |
| Twisted pair, coaxial, fibre | 2080 supp., 2082, 2083 | structure, speed/distance, cost, use, advantage, disadvantage |
| AI and its applications | 2079, 2081, 2082 | definition + five named application areas with one line each |
| Cloud computing | 2080 supp., 2083 | definition, IaaS/PaaS/SaaS, three advantages |
| JavaScript smallest/largest of three | 2080 supp., 2082, 2083 | `prompt`, `parseFloat`, `if`, `document.write` |
| PHP connect/fetch/insert | every paper | `mysqli_connect`, test, `mysqli_query`, fetch loop, `mysqli_close` |
| Normalization, 2NF | 2079, 2081, 2082, 2083 | definition, unnormalized table, 1NF, 2NF tables |
| OOP: features, inheritance, class and object | every paper | definition, example (code or real-world), four features |

### 16.1.5 Numbers and programs that recur

The Computer Science paper has no numericals, but it has **a small fixed set of
programs**. Practise these until you can write them without looking: factorial
(2079, 2080), smallest or largest of three (2080 supp., 2082, 2083), even/odd
(2081), swap (model), a structure for 5–12 records (six papers), a positive/negative/
zero function (2083), Fibonacci by function (2083), the area of a circle by function
(2080), and a file with roll, name and marks (four papers).

::: caution The marks are in the brackets — use them
In 2083 the long question was printed *(4+4)* for two programs, in 2080 *(3+5)* for
the advantage of pointers plus a program, and in 2079 *(2+6)* for "what is a
structure" plus a program. Candidates who write only the program lose the 2, 3 or 4
theory marks, which is 25–50 per cent of the question.
:::

## 16.2 Model Set 1

### 16.2.1 Question paper

**Computer Science — Grade XII — Model Set 1**  
Time: 2 hours  Full marks: 50  Pass marks: 20  
*Candidates are required to give their answers in their own words as far as practicable. The figures in the margin indicate full marks. Attempt all questions.*

**Group A — Multiple choice questions** (9 × 1 = 9)  
*Rewrite the correct option of each question in your answer sheet.*

1. A row of a table, which collects all the fields about one entity, is called a <span class="marks">[1]</span>
   (a) field (b) record (c) file (d) key
2. Which SQL statement displays the names of the students who scored 50 marks or more from the table `student`? <span class="marks">[1]</span>
   (a) `SELECT name FROM student WHERE marks >= 50;` (b) `SELECT * name FROM student WHERE marks >= 50;` (c) `SELECT name WHERE marks >= 50 FROM student;` (d) `SELECT name FROM student HAVING marks = 50;`
3. Which device connects two different networks and forwards data packets using their IP addresses? <span class="marks">[1]</span>
   (a) hub (b) switch (c) router (d) repeater
4. Which HTML tag is used to place JavaScript code inside a web page? <span class="marks">[1]</span>
   (a) `<js>` (b) `<script>` (c) `<javascript>` (d) `<code>`
5. What is displayed by the PHP code `<?php $x = 5; echo $x++ + 2; ?>`? <span class="marks">[1]</span>
   (a) 6 (b) 7 (c) 8 (d) 5
6. What is the output of the C statements `int x = 10; x += 5; printf("%d", x % 4);`? <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) 15
7. The ability of one function name or operator to behave differently in different situations is called <span class="marks">[1]</span>
   (a) encapsulation (b) polymorphism (c) inheritance (d) abstraction
8. Which software development model builds an early working sample so that users can comment on it before the final system is made? <span class="marks">[1]</span>
   (a) waterfall model (b) prototype model (c) sequential model (d) linear model
9. Which technology gives on-demand access to shared storage and servers through the internet? <span class="marks">[1]</span>
   (a) robotics (b) virtual reality (c) cloud computing (d) bluetooth

**Group B — Short answer questions** (5 × 5 = 25)

10. (a) What is a database? Explain any four advantages of a DBMS. *(1+4)* <span class="marks">[5]</span>  
    **Or** (b) What is second normal form (2NF)? Convert a table with a partial dependency into 2NF, with an example. *(1+4)* <span class="marks">[5]</span>
11. (a) Write a JavaScript program to input a number and find whether it is prime or not using a function. <span class="marks">[5]</span>  
    **Or** (b) Write a PHP script to connect to a MySQL database named `school` and insert one record into the table `student`. <span class="marks">[5]</span>
12. What is polymorphism? Explain polymorphism and inheritance in OOP with an example. *(2.5+2.5)* <span class="marks">[5]</span>
13. Explain the waterfall model of software development with a diagram. Write one advantage and one limitation. *(3+2)* <span class="marks">[5]</span>
14. What is the Internet of Things (IoT)? Explain any three of its application areas. *(2+3)* <span class="marks">[5]</span>

**Group C — Long answer questions** (2 × 8 = 16)

15. What is network topology? Explain the bus, ring and star topologies with diagrams, advantages and disadvantages. *(2+6)* <span class="marks">[8]</span>
16. (a) Write a C program to read the id, name and salary of six employees using an array of structure, display them in a table and print the name of the highest-paid employee. <span class="marks">[8]</span>  
    **Or** (b) Write a C program to create a data file named `students.txt` to store roll number, name and marks of students. The program should ask whether to continue after each record. When the user finishes, read the file and display all the records. <span class="marks">[8]</span>

### 16.2.2 Solutions to Model Set 1

::: note Answers — Group A
**1.** (b) — a *record* is one complete row; a *field* (a) is a single column value, a *file* (c) is the whole table and a *key* (d) is a field used to identify records.
**2.** (a) — SELECT lists the column, WHERE filters the rows; (b) has `* name` together, (c) puts WHERE before FROM, (d) uses HAVING, which works on groups and would also test equality with 50.
**3.** (c) — a router forwards by IP address between networks; a switch (b) works inside one network on MAC addresses, a hub (a) only repeats, and a repeater (d) regenerates a weak signal.
**4.** (b) — JavaScript is written between `<script>` and `</script>`; the other three tags do not exist in HTML.
**5.** (b) — `$x++` is a post-increment, so the old value 5 is used: 5 + 2 = 7 (and `$x` becomes 6 afterwards). Choosing 8 means treating it as a pre-increment. Verified by running the code.
**6.** (c) — x becomes 15 and 15 % 4 is the remainder 3. Option (d) forgets the `%`; option (a) divides instead of taking the remainder.
**7.** (b) — polymorphism means "many forms"; encapsulation (a) hides data, inheritance (c) reuses a parent class, abstraction (d) shows only essentials.
**8.** (b) — the prototype model builds a quick working sample for user feedback; the waterfall (a), sequential (c) and linear (d) descriptions all move strictly phase by phase.
**9.** (c) — cloud computing provides shared resources on demand over the internet; robotics (a), virtual reality (b) and bluetooth (d) do not.
:::

**10 (a).** **What is a database? Four advantages of a DBMS.**

A **database** is an organised collection of related data stored together so that it
can be stored, retrieved, updated and managed easily — for example the records of all
the students of a college. A **DBMS** (database management system) is the software
that creates and controls the database. *(1)*

Four advantages of a DBMS: *(4)*

1. **Reduced data redundancy.** Each fact is stored once instead of in many separate
   files, so storage is saved and the copies cannot disagree.
2. **Data consistency and integrity.** Rules such as primary keys, data types and
   constraints keep the data correct and accurate.
3. **Data sharing.** Many authorised users and programs can use the same data at the
   same time.
4. **Data security.** Usernames, passwords and permissions decide who may read or
   change which data.

(Other accepted points: backup and recovery, data independence, faster access by
queries.)

**10 (b).** **Second normal form.**

A table is in **second normal form (2NF)** if it is already in 1NF (every value is
atomic) and **every non-key field depends on the whole primary key**, not on just a
part of it — that is, it has no partial dependency. *(1)*

*Unnormalised table* (the `Courses` column holds several values):

| StudentID | Name | Courses |
|---|---|---|
| 101 | Asha | Physics, Chemistry |
| 102 | Bikash | Physics |

*1NF* — one atomic value per cell, one row per student–course pair. The primary key
is the pair (StudentID, CourseID):

| StudentID | Name | CourseID | Title | Marks |
|---|---|---|---|---|
| 101 | Asha | P | Physics | 78 |
| 101 | Asha | C | Chemistry | 84 |
| 102 | Bikash | P | Physics | 66 |

Here `Name` depends only on StudentID, and `Title` depends only on CourseID — both are
partial dependencies, so the table is not in 2NF. *(1)*

*2NF* — split the table so that every field depends on the whole key of its table: *(3)*

*STUDENT*

| **StudentID** | Name |
|---|---|
| 101 | Asha |
| 102 | Bikash |

*COURSE*

| **CourseID** | Title |
|---|---|
| P | Physics |
| C | Chemistry |

*RESULT* (primary key = StudentID + CourseID)

| **StudentID** | **CourseID** | Marks |
|---|---|---|
| 101 | P | 78 |
| 101 | C | 84 |
| 102 | P | 66 |

Now the name of a student and the title of a course are each stored once.

**11 (a).** **JavaScript prime-number program with a function.**

```html
<html>
<body>
<script>
function isPrime(n) {
    if (n < 2) return false;
    for (var i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}

var num = parseInt(prompt("Enter a number"));
if (isPrime(num))
    document.write(num + " is a prime number");
else
    document.write(num + " is not a prime number");
</script>
</body>
</html>
```

*Output of the page for three inputs (run under Node with `prompt` and
`document.write` supplied):*

| Input | Page shows |
|---|---|
| 29 | 29 is a prime number |
| 91 | 91 is not a prime number |
| 1 | 1 is not a prime number |

*Working.* `isPrime(n)` returns `false` for n < 2. Otherwise it tries every divisor
`i` from 2 while `i * i <= n`; if any `i` divides `n` exactly (`n % i == 0`), n is not
prime. If no divisor is found, it returns `true`. `parseInt()` converts the text
returned by `prompt()` into a number, and `document.write()` prints the result on the
page. (Marks: function 2, loop and test 2, input and output 1.)

**11 (b).** **PHP script to insert a record.**

```php
<?php
$conn = mysqli_connect("localhost", "root", "", "school");
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$sql = "INSERT INTO student (roll, name, address, marks)
        VALUES (4, 'Dipa', 'Pokhara', 55)";

if (mysqli_query($conn, $sql)) {
    echo "New record inserted successfully";
} else {
    echo "Error: " . mysqli_error($conn);
}
mysqli_close($conn);
?>
```

*Output:* `New record inserted successfully` — and a `SELECT` on the table afterwards
showed the new row (4, Dipa, Pokhara, 55).

*Working.* `mysqli_connect(server, user, password, database)` opens the connection and
returns `false` on failure, which the `if (!$conn)` test catches. `mysqli_query()`
sends the SQL `INSERT` statement to the server and returns `true` on success.
`mysqli_error()` reports what went wrong, and `mysqli_close()` closes the connection.

**12.** **Polymorphism and inheritance.**

**Polymorphism** means "many forms": one name — a function or an operator — behaves
differently according to the situation. In C++ it can be *compile-time* (function
overloading, operator overloading) or *run-time* (virtual functions). *(1)*

**Inheritance** is the mechanism by which a new class (the *derived* or child class)
acquires the data and functions of an existing class (the *base* or parent class) and
adds its own. It gives **code reuse**: the parent's code is written once. *(1.5)*

```cpp
#include <iostream>
#include <string>
using namespace std;

class Person {
protected:
    string name;
public:
    Person(string n) : name(n) {}
    void show() { cout << "Name   : " << name << endl; }
};

class Student : public Person {
    int roll;
public:
    Student(string n, int r) : Person(n), roll(r) {}
    void show() {
        Person::show();
        cout << "Roll   : " << roll << endl;
    }
};

class Area {
public:
    double find(double r) { return 3.14159 * r * r; }
    double find(double l, double b) { return l * b; }
};

int main()
{
    Student s("Anita Sharma", 12);
    s.show();

    Area a;
    cout << "Circle (r = 7)        : " << a.find(7.0) << endl;
    cout << "Rectangle (8 x 5)     : " << a.find(8.0, 5.0) << endl;
    return 0;
}
```

*Output:*

```text
Name   : Anita Sharma
Roll   : 12
Circle (r = 7)        : 153.938
Rectangle (8 x 5)     : 40
```

`Student` inherits `name` and `show()` from `Person` and adds `roll` — this is
**inheritance**. The class `Area` has two functions named `find()` that differ in the
number of parameters — the compiler chooses by the arguments (one argument for a
circle, two for a rectangle) — this is **polymorphism** by function overloading. *(2.5)*

**13.** **Waterfall model.**

The **waterfall model** is the oldest software-development model. The project flows
through the phases in a fixed order, like water falling down steps; a phase begins
only when the previous one is complete. *(1)*

```figure caption="The waterfall model: each phase is completed before the next begins."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

steps = ["Requirement\nanalysis", "System\ndesign", "Implementation\n(coding)",
         "Testing", "Deployment and\nmaintenance"]
fig, ax = plt.subplots(figsize=(5.0, 2.8))
w, h, dx, dy = 2.1, 0.62, 1.15, 0.95
for i, s in enumerate(steps):
    x = i * dx
    y = 4.3 - i * dy
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=ACCENT if i % 2 == 0 else SERIES[1], ec="none"))
    ax.text(x + w / 2, y + h / 2, s, ha="center", va="center", fontsize=7.4,
            color="white", fontweight="bold", linespacing=1.05)
    if i < len(steps) - 1:
        ax.add_patch(FancyArrowPatch((x + 1.6, y), (x + 1.6, y - dy + h + 0.03),
                                     arrowstyle="-|>", mutation_scale=10, color=INK, lw=1.1))
ax.set_xlim(-0.1, 6.9)
ax.set_ylim(0.3, 5.1)
ax.axis("off")
fig.tight_layout()
```

1. **Requirement analysis** — find out, from the users, what the system must do.
2. **System design** — plan the architecture, database and screens.
3. **Implementation** — programmers write the code.
4. **Testing** — find and remove faults; check that the requirements are met.
5. **Deployment and maintenance** — install the system and keep it working and updated. *(2)*

*Advantage:* it is simple and easy to manage because every phase has a clear output
and a clear end. *Limitation:* it is inflexible — once a phase is finished it is hard
to go back, so changing requirements late in the project is costly, and the user
sees the working system only at the very end. *(2)*

**14.** **Internet of Things.**

The **Internet of Things (IoT)** is a network of physical objects — "things" such as
sensors, appliances, vehicles and wearable devices — that have sensors, software and
an internet connection, so that they can collect data and exchange it with other
devices and systems without human involvement. *(2)*

Application areas (any three): *(3)*

1. **Smart home** — a thermostat, lights or a door lock that can be controlled from a
   phone or that reacts to sensor readings.
2. **Healthcare** — wearable devices that monitor pulse or blood oxygen and send the
   reading to a doctor.
3. **Agriculture** — soil-moisture sensors that switch irrigation on only when the
   soil is dry.
4. **Transport and cities** — connected vehicles, smart traffic signals and
   street lighting.

**15.** **Network topology: bus, ring and star.**

**Network topology** is the physical or logical arrangement of the computers
(nodes), cables and devices in a network — the way they are connected to one another.
*(2)*

```figure caption="Bus, ring and star topologies."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

fig, axs = plt.subplots(1, 3, figsize=(5.1, 2.3))
ang = np.linspace(0, 2 * np.pi, 6, endpoint=False) + np.pi / 2

ax = axs[0]
ax.plot([0.8, 9.2], [5.0, 5.0], color=INK, lw=2)
for x in (2.0, 4.0, 6.0, 8.0):
    ax.plot([x, x], [5.0, 3.2], color=MUTED, lw=1)
    ax.add_patch(Circle((x, 2.7), 0.55, fc=ACCENT, ec="none"))
ax.plot([0.8, 0.8], [4.6, 5.4], color=INK, lw=3)
ax.plot([9.2, 9.2], [4.6, 5.4], color=INK, lw=3)
ax.text(5, 5.9, "backbone", ha="center", fontsize=6.6, color=MUTED)
ax.set_title("Bus", fontsize=8.5, color=INK)

ax = axs[1]
xs, ys = 5 + 3 * np.cos(ang), 3.5 + 2.4 * np.sin(ang)
for i in range(6):
    j = (i + 1) % 6
    ax.annotate("", xy=(xs[j], ys[j]), xytext=(xs[i], ys[i]),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0,
                                shrinkA=9, shrinkB=9))
for x, y in zip(xs, ys):
    ax.add_patch(Circle((x, y), 0.55, fc=ACCENT, ec="none"))
ax.set_title("Ring", fontsize=8.5, color=INK)

ax = axs[2]
for x, y in zip(xs, ys):
    ax.plot([5, x], [3.5, y], color=MUTED, lw=1)
    ax.add_patch(Circle((x, y), 0.55, fc=ACCENT, ec="none"))
ax.add_patch(FancyBboxPatch((3.7, 3.0), 2.6, 1.0,
             boxstyle="round,pad=0.02,rounding_size=0.15", fc=SERIES[2], ec="none"))
ax.text(5, 3.5, "switch", ha="center", va="center", fontsize=6.6, color="white")
ax.set_title("Star", fontsize=8.5, color=INK)

for ax in axs:
    ax.set_xlim(0, 10)
    ax.set_ylim(0.2, 6.8)
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout()
```

| | Bus | Ring | Star |
|---|---|---|---|
| **Layout** | all nodes tap one common backbone cable with terminators at both ends | each node joined to exactly two neighbours, forming a closed loop | every node joined to a central hub or switch |
| **Data path** | broadcast along the cable; every node sees it | passes around the ring, usually in one direction | node → hub → destination node |
| **Advantages** | needs the least cable; cheap; easy to set up for a small network | orderly access — no collisions when a token is used; performs fairly under heavy load | a fault in one cable or node affects only that node; easy to add, remove or find a fault |
| **Disadvantages** | a break in the backbone stops the whole network; performance falls as nodes are added; faults are hard to trace | one failed node or cable can break the whole ring; adding a node interrupts the network | the hub is a single point of failure; needs more cable and a hub or switch |

The star topology, with a switch at the centre, is the one used in most office and
school LANs today. *(6: bus 2, ring 2, star 2, with diagrams)*

**16 (a).** **Array of structure: six employees.**

```c
#include <stdio.h>

struct employee {
    int id;
    char name[30];
    float salary;
};

int main(void)
{
    struct employee e[6];
    int i, top = 0;

    for (i = 0; i < 6; i++) {
        printf("Enter id, name and salary of employee %d: ", i + 1);
        scanf("%d %s %f", &e[i].id, e[i].name, &e[i].salary);
        if (e[i].salary > e[top].salary)
            top = i;
    }

    printf("\n%-5s %-12s %10s\n", "ID", "Name", "Salary");
    for (i = 0; i < 6; i++)
        printf("%-5d %-12s %10.2f\n", e[i].id, e[i].name, e[i].salary);

    printf("\nHighest paid: %s (Rs. %.2f)\n", e[top].name, e[top].salary);
    return 0;
}
```

*Output (input typed by the user shown after each prompt):*

```text
Enter id, name and salary of employee 1: 1 Asha 42000
Enter id, name and salary of employee 2: 2 Bikash 38500
Enter id, name and salary of employee 3: 3 Chandra 51000.50
Enter id, name and salary of employee 4: 4 Deepa 47250
Enter id, name and salary of employee 5: 5 Eshan 29900
Enter id, name and salary of employee 6: 6 Fulmaya 45000

ID    Name             Salary
1     Asha           42000.00
2     Bikash         38500.00
3     Chandra        51000.50
4     Deepa          47250.00
5     Eshan          29900.00
6     Fulmaya        45000.00

Highest paid: Chandra (Rs. 51000.50)
```

*Working.* `struct employee` groups the three different data types under one name.
`e[6]` is an array of six such structures, so `e[i].salary` is the salary of the
(i+1)th employee. The `for` loop reads each employee and remembers the index `top` of
the largest salary seen so far. The second loop prints the table with field widths
(`%-12s`, `%10.2f`) for alignment, and the last line uses `top` to print the
highest-paid employee. (Marks: structure 2, input loop 2, display 2, highest 2.)

**16 (b).** **Data file: write and read student records.**

```c
#include <stdio.h>

int main(void)
{
    FILE *fp;
    int roll, marks;
    char name[30], more;

    fp = fopen("students.txt", "w");
    if (fp == NULL) {
        printf("File could not be opened.\n");
        return 1;
    }
    do {
        printf("Roll, name and marks: ");
        scanf("%d %s %d", &roll, name, &marks);
        fprintf(fp, "%d %s %d\n", roll, name, marks);
        printf("Add another record (y/n)? ");
        scanf(" %c", &more);
    } while (more == 'y' || more == 'Y');
    fclose(fp);

    fp = fopen("students.txt", "r");
    printf("\n%-6s %-12s %s\n", "Roll", "Name", "Marks");
    while (fscanf(fp, "%d %s %d", &roll, name, &marks) == 3)
        printf("%-6d %-12s %d\n", roll, name, marks);
    fclose(fp);
    return 0;
}
```

*Output:*

```text
Roll, name and marks: 1 Sita 78
Add another record (y/n)? y
Roll, name and marks: 2 Ram 65
Add another record (y/n)? y
Roll, name and marks: 3 Gita 91
Add another record (y/n)? n

Roll   Name         Marks
1      Sita         78
2      Ram          65
3      Gita         91
```

*Working.* `fopen("students.txt", "w")` creates the file for writing and returns
`NULL` if it fails, which is tested. `fprintf()` writes each record as a line of text,
and the `do … while` loop repeats while the user answers `y`. After `fclose()` the same
file is opened in `"r"` mode; `fscanf()` returns the number of items read (3 for a
good record), so the `while` loop stops at the end of the file. The file afterwards
holds exactly the three lines `1 Sita 78`, `2 Ram 65` and `3 Gita 91`.
(Marks: open/check 2, write loop with continue question 3, read and display 3.)

## 16.3 Model Set 2

### 16.3.1 Question paper

**Computer Science — Grade XII — Model Set 2**  
Time: 2 hours  Full marks: 50  Pass marks: 20  
*Candidates are required to give their answers in their own words as far as practicable. The figures in the margin indicate full marks. Attempt all questions.*

**Group A — Multiple choice questions** (9 × 1 = 9)  
*Rewrite the correct option of each question in your answer sheet.*

1. A candidate key that is not chosen as the primary key is called the <span class="marks">[1]</span>
   (a) foreign key (b) alternate key (c) composite key (d) super key
2. In which normal form are partial dependencies removed? <span class="marks">[1]</span>
   (a) 1NF (b) 2NF (c) 3NF (d) BCNF
3. In which topology does the failure of one cable disconnect only the one computer attached to it? <span class="marks">[1]</span>
   (a) bus (b) ring (c) star (d) all of them
4. Which of the following correctly declares a function in JavaScript? <span class="marks">[1]</span>
   (a) `function show() { }` (b) `def show() { }` (c) `void show() { }` (d) `fun show() { }`
5. What does the PHP code `<?php echo "5" + "3"; ?>` display? <span class="marks">[1]</span>
   (a) 53 (b) 8 (c) 5+3 (d) an error
6. Which C operator gives the value stored at the address held by a pointer? <span class="marks">[1]</span>
   (a) `&` (b) `*` (c) `->` (d) `.`
7. Which OOP feature binds data and the functions that work on it into a single unit? <span class="marks">[1]</span>
   (a) polymorphism (b) encapsulation (c) inheritance (d) overloading
8. Collecting requirements by giving a set of written questions to many users is called <span class="marks">[1]</span>
   (a) interview (b) observation (c) questionnaire (d) prototyping
9. Paying a vehicle tax through a government website is an example of <span class="marks">[1]</span>
   (a) e-commerce (b) e-governance (c) e-medicine (d) mobile computing

**Group B — Short answer questions** (5 × 5 = 25)

10. (a) Differentiate between a centralized and a distributed database system. <span class="marks">[5]</span>  
    **Or** (b) Consider the table `student(roll, name, address, marks)`. Write SQL statements to (i) create the table, (ii) insert one record, (iii) add a column `phone`, (iv) display the name and address of the students who live in Kathmandu or Bhaktapur, (v) delete the record of roll 4. <span class="marks">[5]</span>
11. (a) Write a JavaScript program to validate a form: the name must not be empty and the age must be a number of at least 18. <span class="marks">[5]</span>  
    **Or** (b) Write a PHP script that connects to a MySQL database named `school`, retrieves all records from the table `student` and displays them in an HTML table. <span class="marks">[5]</span>
12. What is OOP? Explain class and object with an example. *(1+4)* <span class="marks">[5]</span>
13. Describe any four requirement collection methods used in the analysis phase of the software development life cycle. *(1+4)* <span class="marks">[5]</span>
14. What is virtual reality? Explain any three of its applications. *(2+3)* <span class="marks">[5]</span>

**Group C — Long answer questions** (2 × 8 = 16)

15. What is a transmission medium? Explain twisted pair cable, coaxial cable and optical fibre cable with their advantages and disadvantages. *(2+6)* <span class="marks">[8]</span>
16. (a) What is recursion? Write a C program to find the factorial of a number using a recursive function and to display the first ten Fibonacci numbers. *(2+6)* <span class="marks">[8]</span>  
    **Or** (b) What is a pointer? Write a C program to swap two numbers using call by reference. *(2+6)* <span class="marks">[8]</span>

### 16.3.2 Solutions to Model Set 2

::: note Answers — Group A
**1.** (b) — an *alternate key* is a candidate key left unused; a *foreign key* (a) points to another table's key, a *composite key* (c) has several fields, and *super key* (d) is any field set that identifies a row.
**2.** (b) — 2NF removes partial dependencies; 1NF (a) only makes values atomic and 3NF (c) removes transitive dependencies.
**3.** (c) — in a star each node has its own cable to the hub, so only that node is lost; in a bus (a) a backbone break stops everyone and in a ring (b) a break stops the loop.
**4.** (a) — `function` is the JavaScript keyword; `def` (b) is Python, `void` (c) is C and `fun` (d) is Kotlin.
**5.** (b) — `+` is arithmetic addition in PHP and the strings are converted to numbers: 8. Concatenation would need the dot (`"5" . "3"` gives 53). Verified by running the code.
**6.** (b) — `*` is the indirection (dereference) operator; `&` (a) gives the address, `->` (c) reaches a member through a structure pointer and `.` (d) a member of a structure.
**7.** (b) — encapsulation; polymorphism (a) and overloading (d) are about one name with many forms, inheritance (c) is reuse of a parent class.
**8.** (c) — a questionnaire; an interview (a) is face-to-face, observation (b) means watching users work, prototyping (d) shows a sample system.
**9.** (b) — a citizen–government service is e-governance; e-commerce (a) is buying and selling, e-medicine (c) is health care at a distance and mobile computing (d) is about the device.
:::

**10 (a).** **Centralized and distributed database.**

A **centralized database** keeps all the data in one place, on one computer or one
server, and all users access it from there. A **distributed database** splits the data
over several computers at different locations that are connected by a network, but
users see it as one database.

| Basis | Centralized database | Distributed database |
|---|---|---|
| Location of data | one site | several sites, connected by a network |
| Access speed for remote users | slow when the user is far from the site | fast — users use the nearest copy |
| Reliability | if the single site fails, all users lose the data | a failure at one site does not stop the others |
| Cost and complexity | low cost, simple to manage | costly, and harder to manage and keep consistent |
| Security | easy to secure one site | harder — every site and the links between them must be protected |
| Example | the records of a small college | a bank with data at branches in many cities |

**10 (b).** **SQL statements** (run on MariaDB; the output is real).

```sql
CREATE TABLE student (
    roll INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    address VARCHAR(30),
    marks INT
);
INSERT INTO student VALUES (1, 'Anita', 'Kathmandu', 78);
ALTER TABLE student ADD phone VARCHAR(10);
SELECT name, address FROM student
WHERE address = 'Kathmandu' OR address = 'Bhaktapur';
DELETE FROM student WHERE roll = 4;
```

With the rows (1, Anita, Kathmandu), (2, Binod, Bhaktapur), (3, Chhiring, Lalitpur)
and (4, Dipa, Kathmandu) in the table, the `SELECT` returned:

```text
+-------+-----------+
| name  | address   |
+-------+-----------+
| Anita | Kathmandu |
| Binod | Bhaktapur |
| Dipa  | Kathmandu |
+-------+-----------+
```

`CREATE` and `ALTER` are **DDL** statements (they define structure); `INSERT`, `SELECT`
and `DELETE` are **DML** statements (they work on the data). Note that the condition
is written as `address = 'Kathmandu' OR address = 'Bhaktapur'` — writing
`address = 'Kathmandu' OR 'Bhaktapur'` is a common mistake. (Marks: one each.)

**11 (a).** **JavaScript form validation.**

```html
<html>
<head>
<script>
function validateForm() {
    var name = document.getElementById("name").value;
    var age = document.getElementById("age").value;

    if (name.trim() == "") {
        alert("Name must not be empty");
        return false;
    }
    if (isNaN(age) || age == "") {
        alert("Age must be a number");
        return false;
    }
    if (Number(age) < 18) {
        alert("You must be at least 18");
        return false;
    }
    return true;
}
</script>
</head>
<body>
<form onsubmit="return validateForm()">
    Name: <input type="text" id="name"><br>
    Age: <input type="text" id="age"><br>
    <input type="submit" value="Register">
</form>
</body>
</html>
```

*Result of the checks* (the function was run under Node with a stand-in for the
page's form fields):

```text
""     "20"   -> Name must not be empty | submitted: false
"Ram"  "abc"  -> Age must be a number | submitted: false
"Ram"  "16"   -> You must be at least 18 | submitted: false
"Ram"  "21"   -> (no alert) | submitted: true
```

*Working.* `document.getElementById("name").value` reads what the user typed. `trim()`
removes spaces, so a name made of spaces is also rejected. `isNaN(age)` is `true` when
the text is not a number. The function returns `false` to stop the form being
submitted (`onsubmit="return validateForm()"`) and `true` when all checks pass.
(Marks: function and reading values 2, three tests 2, form and submit handling 1.)

**11 (b).** **PHP: display a table in an HTML table.**

```php
<?php
$conn = mysqli_connect("localhost", "root", "", "school");
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$result = mysqli_query($conn, "SELECT * FROM student");

echo "<table border='1'>";
echo "<tr><th>Roll</th><th>Name</th><th>Address</th><th>Marks</th></tr>";
while ($row = mysqli_fetch_assoc($result)) {
    echo "<tr><td>" . $row['roll'] . "</td><td>" . $row['name'] .
         "</td><td>" . $row['address'] . "</td><td>" . $row['marks'] . "</td></tr>";
}
echo "</table>";
mysqli_close($conn);
?>
```

The page produced by the script (with the table holding four rows):

```text
<table border='1'>
<tr><th>Roll</th><th>Name</th><th>Address</th><th>Marks</th></tr>
<tr><td>1</td><td>Anita</td><td>Kathmandu</td><td>78</td></tr>
<tr><td>2</td><td>Binod</td><td>Bhaktapur</td><td>64</td></tr>
<tr><td>3</td><td>Chhiring</td><td>Lalitpur</td><td>91</td></tr>
<tr><td>4</td><td>Dipa</td><td>Pokhara</td><td>55</td></tr>
</table>
```

which a browser shows as a four-row table with the headings Roll, Name, Address and
Marks. `mysqli_query()` returns a result set; `mysqli_fetch_assoc()` returns the next
row as an array indexed by column name and `false` at the end, so the `while` loop
prints one `<tr>` per row. (Marks: connect and check 1, query 1, loop 2, HTML table 1.)

**12.** **OOP, class and object.**

**Object-oriented programming (OOP)** is a programming paradigm in which a program is
organised as a collection of *objects* that hold both data and the functions that
operate on it, rather than as a list of procedures that act on separate data. *(1)*

A **class** is a user-defined blueprint or template that defines the data (attributes)
and functions (methods) common to a group of similar things. An **object** is an
*instance* of a class — a real item built from the blueprint, with its own values. No
memory is used for the data until an object is created. Real-world example: the
class `Student` has the attributes name and roll; Ram and Sita are two objects of
that class. *(2)*

```cpp
#include <iostream>
#include <string>
using namespace std;

class Book {
    string title;
    float price;
public:
    void set(string t, float p) { title = t; price = p; }
    void display() { cout << title << " - Rs. " << price << endl; }
};

int main()
{
    Book b1, b2;
    b1.set("Computer Science 12", 650);
    b2.set("Nepali Reader", 280);
    b1.display();
    b2.display();
    return 0;
}
```

*Output:*

```text
Computer Science 12 - Rs. 650
Nepali Reader - Rs. 280
```

`Book` is the class; `b1` and `b2` are two objects with different titles and prices;
`set()` and `display()` are its member functions. *(2)*

**13.** **Requirement collection methods.**

**Requirement gathering** is the activity in the analysis phase of the SDLC in which
the analyst finds out what the users need the new system to do. *(1)*

| Method | How it works | Good for | Limitation |
|---|---|---|---|
| **Interview** | the analyst asks questions face to face | detailed, deep answers; clearing doubts on the spot | time-consuming; only a few people can be interviewed |
| **Questionnaire** | a written set of questions given to many users | collecting views from a large, scattered group cheaply | no chance to explain; answers may be shallow; some forms are not returned |
| **Observation** | the analyst watches how the present system is actually used | finding what users do rather than what they say | time-consuming; people may behave differently when watched |
| **Document review** | studying forms, reports, manuals and records of the present system | understanding the data and rules already in use | documents may be out of date or incomplete |

(Joint application development and prototyping are also accepted.) *(4)*

**14.** **Virtual reality.**

**Virtual reality (VR)** is a computer-generated, three-dimensional environment that
the user can enter and interact with using a head-mounted display and sensors or
controllers that track head and hand movement, so that the user feels present inside
the simulated world. *(2)*

Applications (any three): *(3)*

1. **Education and training** — students can "walk through" a cell, a historical site
   or a laboratory; pilots, drivers and surgeons practise in a simulator without risk.
2. **Entertainment and games** — immersive games, virtual concerts and films.
3. **Architecture and real estate** — a client can tour a building before it is built.
4. **Healthcare** — pain distraction, therapy for phobias, rehabilitation exercises.
5. **Tourism** — virtual visits to heritage sites.

**15.** **Transmission medium: twisted pair, coaxial, optical fibre.**

A **transmission medium** is the physical path (a cable) or the wireless channel
through which data travels from the sender to the receiver. Cable media are called
**guided** media because the signal is guided along a wire or fibre. *(2)*

```photo id="cs12/utp-cable" caption="A twisted-pair (UTP) network cable ending in an RJ-45 connector; the eight thin wires, twisted in four pairs, can be seen through the clear plug." width="70"
```

```photo id="cs12/coaxial-cable-cut" caption="A coaxial cable cut back to show its layers." width="70"
mark 0.17 0.22 "1"
mark 0.52 0.42 "2"
mark 0.76 0.72 "3"
mark 0.88 0.88 "4"
key 1 Outer insulating jacket
key 2 Braided metal shield
key 3 Insulator (dielectric)
key 4 Centre conductor
```

| | Twisted pair | Coaxial cable | Optical fibre |
|---|---|---|---|
| **Structure** | pairs of insulated copper wires twisted together (UTP, or STP with a shield) | a copper centre conductor, insulator, metal shield and outer jacket, all on one axis | a hair-thin glass or plastic core with cladding and a protective jacket |
| **Signal** | electrical | electrical | pulses of light |
| **Typical use** | telephone lines and LAN cables (Cat5e, Cat6) | cable TV, older Ethernet, antenna leads | backbone links, internet service providers |
| **Advantages** | cheap, thin, easy to install and to join | better shielded than twisted pair, so less interference; longer distance and higher bandwidth than UTP | very high speed and bandwidth; very long distance; immune to electrical noise; hard to tap |
| **Disadvantages** | the most affected by noise and crosstalk; short distance (about 100 m for LAN) | thicker, stiffer and dearer than twisted pair; a break stops the link | costly; fragile and difficult to join; needs special tools and skill |

The twisting in a twisted pair makes the magnetic fields of the two wires cancel, which
reduces crosstalk. *(6: two marks for each cable — structure and use, advantage,
disadvantage.)*

**16 (a).** **Recursion: factorial and Fibonacci.**

**Recursion** is the process in which a function calls itself, directly or indirectly,
to solve a smaller copy of the same problem; it needs a **base case** that stops the
calls. *(2)*

```c
#include <stdio.h>

long factorial(int n)
{
    if (n <= 1)
        return 1;
    return n * factorial(n - 1);
}

int fibonacci(int n)
{
    if (n == 0)
        return 0;
    if (n == 1)
        return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main(void)
{
    int n, i;

    printf("Enter a number: ");
    scanf("%d", &n);
    printf("%d! = %ld\n", n, factorial(n));

    printf("First 10 Fibonacci numbers: ");
    for (i = 0; i < 10; i++)
        printf("%d ", fibonacci(i));
    printf("\n");
    return 0;
}
```

*Output:*

```text
Enter a number: 6
6! = 720
First 10 Fibonacci numbers: 0 1 1 2 3 5 8 13 21 34 
```

`factorial(6)` expands as 6 × 5 × 4 × 3 × 2 × 1 = 720; the base case `n <= 1`
returns 1 and ends the calls. `fibonacci(n)` returns the sum of the two previous
terms, with base cases 0 and 1. *(6)*

**16 (b).** **Pointer and call by reference.**

A **pointer** is a variable that stores the *address* of another variable. It is
declared with `*` (for example `int *p;`); `&` gives the address of a variable and `*`
(the indirection operator) gives the value stored at an address. *(2)*

```c
#include <stdio.h>

void swap(int *a, int *b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

int main(void)
{
    int x, y;

    printf("Enter two numbers: ");
    scanf("%d %d", &x, &y);
    printf("Before swap: x = %d, y = %d\n", x, y);
    swap(&x, &y);
    printf("After swap:  x = %d, y = %d\n", x, y);
    return 0;
}
```

*Output:*

```text
Enter two numbers: 15 40
Before swap: x = 15, y = 40
After swap:  x = 40, y = 15
```

In **call by reference** the function receives the *addresses* of the actual
arguments (`&x`, `&y`), so `*a` and `*b` are the original variables and the swap is
visible in `main()`. In call by value the function would get only copies and the
original numbers would remain unchanged. *(6)*

## 16.4 Predicted Questions

### 16.4.1 How the ranking was made

Every question below is ranked by three things, and each entry states which applied.
**Slot certainty**: the slot of the paper it would fill (Q10–Q16) has come from the
same unit in every paper read. **Frequency**: how many of the seven papers carried
that question type. **Gap**: how long since it last appeared, and whether a syllabus
bullet has never yet been a written question at all. None of this is a prediction of
the actual paper; it is a way of spending revision time where the evidence points.

| Tier | Meaning | Questions |
|---|---|---|
| **A** | the slot is certain and the type has appeared in three or more papers | 1–15 |
| **B** | the slot is certain; the type has appeared once or twice, or is a syllabus bullet asked only as MCQs | 16–34 |
| **C** | the syllabus names it and it has not yet been a full written question, or it fits a large slot | 35–47 |

### 16.4.2 Tier A — the slot is certain and the type keeps returning

**1. Compare the star topology with the bus topology, giving advantages and disadvantages. Which topology is better for a school LAN? *(5+3)* [8]**

*Why:* Q15 took topologies in 2079, 2080 and 2081, and transmission media in 2080
supplementary, 2082 and 2083 — so topologies are due back. Star vs bus was asked in
2081, star vs ring in 2079.

| | Star | Bus |
|---|---|---|
| Layout | each node has its own cable to a central switch or hub | all nodes on one backbone cable with a terminator at each end |
| Cable needed | more | less |
| Fault in one node or cable | only that node is affected | a break in the backbone stops the whole network |
| Fault finding | easy — look at the port or cable of the failed node | hard — the whole cable must be checked |
| Adding a node | easy, plug into the switch | possible, but performance falls as nodes increase |
| Main disadvantage | if the central switch fails, the whole network fails | cheap but unreliable; slow under heavy traffic; collisions |
| Cost | higher (switch plus cable) | lower |

*Advantages of star:* easy to install, extend and troubleshoot; failure of one node
does not affect the others; good performance. *Disadvantages of star:* needs more
cable and a central device, and that device is a single point of failure. *Advantages
of bus:* the cheapest and simplest for a few computers. *Disadvantages of bus:* one
cable fault stops everything, performance drops as nodes are added, and faults are
hard to locate.

**Choice:** the **star topology** with twisted-pair cable (Cat5e or Cat6) and a switch
is the better choice for a school LAN, because a fault in one lab computer must not
stop the others and new computers must be easy to add.

**2. Describe the features of CAT-6 and optical fibre cable. Which is more suitable for a local area network? *(2080 supplementary)* [8]**

*Why:* cables were Q15 in 2080 supplementary, 2082 and 2083; this exact pairing is the
2080 supplementary question, so a close variant is likely.

**CAT-6** is a twisted-pair copper cable of four twisted pairs with an RJ-45
connector. Features: carries up to 1 Gbps (and 10 Gbps over short runs of about 55 m);
the usual maximum run is 100 m; cheap, flexible and easy to install and terminate;
the signals are electrical, so it is affected by electrical noise and crosstalk (the
tight twisting and often a plastic divider inside reduce this).

**Optical fibre** sends pulses of light through a glass or plastic core. Features:
very high bandwidth and speed; very long distance (kilometres); no effect from
electrical or radio noise; very secure because it is hard to tap; thin and light; but
expensive, fragile, hard to join and needing special connectors and tools.

| | CAT-6 | Optical fibre |
|---|---|---|
| Signal | electrical | light |
| Distance without a repeater | 100 m | kilometres |
| Interference | affected | immune |
| Cost | low | high |
| Installation | easy | needs skill and tools |

**Choice:** for a LAN inside a building (computer lab, office) **CAT-6** is more
suitable, since distances are below 100 m, it is cheap and easy to install and its
speed is enough; fibre is better used for the backbone between buildings.

**3. What is client-server architecture? Compare it with peer-to-peer architecture with advantages and disadvantages. *(CDC model asked the client-server part)* [8]**

*Why:* the model question asked client-server; it is a named syllabus bullet that has
never been a real-paper question, and 8 marks are available in the networking slot.

In a **client-server** network one or more powerful computers, the **servers**, store
the shared data and provide services (files, printing, web, database); the other
computers, the **clients**, request those services. In a **peer-to-peer (P2P)**
network there is no dedicated server — every computer is both a client and a server
and shares its own resources directly with the others.

| | Client-server | Peer-to-peer |
|---|---|---|
| Server | dedicated server | none; every computer is equal |
| Security | centralised; the administrator controls access | each user protects their own computer; weak |
| Backup | done once at the server | done on every computer |
| Cost | high (server, licence, administrator) | low |
| Performance | good for many users | slows when many computers share |
| Suitable for | banks, schools, large offices | home or a small office of fewer than about ten computers |
| Main risk | the server is a single point of failure | no control; hard to manage as the network grows |

*Advantages of client-server:* centralised control and security, easy backup and
management of data, can serve many clients, easy to upgrade. *Disadvantages:*
expensive to set up, needs a network administrator, and if the server fails, clients
cannot be served.

**4. Write a C program to read the roll number, name and marks of five students using an array of structure and display the students who passed (marks 40 or more). *(array-of-structure family: 2079, 2080 supplementary, 2081, 2082, 2083, model)* [8]**

*Why:* the most frequent Q16 type — six of seven papers — and variants differ only in
the fields; the filter condition is the usual way of varying it.

```c
#include <stdio.h>

struct student {
    int roll;
    char name[20];
    int marks;
};

int main(void)
{
    struct student s[5];
    int i, pass = 0;

    for (i = 0; i < 5; i++) {
        printf("Roll, name, marks: ");
        scanf("%d %s %d", &s[i].roll, s[i].name, &s[i].marks);
    }
    printf("\nPassed students (marks >= 40):\n");
    for (i = 0; i < 5; i++)
        if (s[i].marks >= 40) {
            printf("%d %s %d\n", s[i].roll, s[i].name, s[i].marks);
            pass++;
        }
    printf("Total passed = %d\n", pass);
    return 0;
}
```

*Output:*

```text
Roll, name, marks: 1 Ram 72
Roll, name, marks: 2 Sita 35
Roll, name, marks: 3 Hari 40
Roll, name, marks: 4 Gita 28
Roll, name, marks: 5 Mina 91

Passed students (marks >= 40):
1 Ram 72
3 Hari 40
5 Mina 91
Total passed = 3
```

**5. Write a C program to add a new record to an existing data file `emp.txt` and then display the whole file. List the file opening modes. *(file-handling family: 2079, 2080 supplementary, 2081, model)* [8]**

*Why:* the file-handling alternative appeared in four of seven papers. "Append" is the
one mode the model programs in this chapter have not used.

| Mode | Meaning |
|---|---|
| `"r"` | open an existing file for reading |
| `"w"` | create a file for writing; an existing file is erased |
| `"a"` | open for writing at the end; the file is created if it does not exist |
| `"r+"`, `"w+"`, `"a+"` | as above, and also allow the other operation |

```c
#include <stdio.h>

int main(void)
{
    FILE *fp;
    char line[80];
    int id;
    char name[30];

    fp = fopen("emp.txt", "w");
    fprintf(fp, "101 Ramesh\n102 Sunita\n");
    fclose(fp);

    fp = fopen("emp.txt", "a");
    printf("Enter id and name to append: ");
    scanf("%d %s", &id, name);
    fprintf(fp, "%d %s\n", id, name);
    fclose(fp);

    fp = fopen("emp.txt", "r");
    printf("\nContents of emp.txt:\n");
    while (fgets(line, sizeof(line), fp) != NULL)
        printf("%s", line);
    fclose(fp);
    return 0;
}
```

*Output:*

```text
Enter id and name to append: 103 Tara

Contents of emp.txt:
101 Ramesh
102 Sunita
103 Tara
```

The first `"w"` block only creates the test file so that the program can be run; in the
answer you may assume `emp.txt` exists and start at `fopen("emp.txt", "a")`.

**6. Discuss binary file handling in C. Write a program that stores student records in a binary file using `fwrite()` and reads them back with `fread()`. *(NEB 2081 asked this with `fwrite()` and `getw()`)* [8]**

*Why:* the 2081 *or* question, asked once; a binary file is a named bullet and the
only file type not yet covered by a model program.

A **binary file** stores data in the same form as in memory — a structure's bytes are
written exactly, not converted to text. It is faster and more compact than a text
file, but cannot be read in a text editor. It is opened with `"wb"`, `"rb"` or `"ab"`.
`fwrite(&s, sizeof(s), 1, fp)` writes one record (address, size of one item, number of
items, file pointer); `fread()` has the same arguments and returns the number of
items read, which is 0 at the end of the file. `putw()` and `getw()` write and read
one integer.

```c
#include <stdio.h>

struct student {
    int roll;
    char name[20];
    float marks;
};

int main(void)
{
    struct student s, t;
    FILE *fp;
    int n, i;

    fp = fopen("student.dat", "wb");
    printf("How many students? ");
    scanf("%d", &n);
    for (i = 0; i < n; i++) {
        printf("Roll, name, marks: ");
        scanf("%d %s %f", &s.roll, s.name, &s.marks);
        fwrite(&s, sizeof(s), 1, fp);
    }
    fclose(fp);

    fp = fopen("student.dat", "rb");
    printf("\nRecords read back from the binary file:\n");
    while (fread(&t, sizeof(t), 1, fp) == 1)
        printf("%d %-8s %.1f\n", t.roll, t.name, t.marks);
    fclose(fp);
    return 0;
}
```

*Output:*

```text
How many students? 2
Roll, name, marks: 7 Kiran 66.5
Roll, name, marks: 9 Laxmi 81

Records read back from the binary file:
7 Kiran    66.5
9 Laxmi    81.0
```

**7. What are the components of a function in C? Differentiate between call by value and call by reference with a program. *(NEB 2082, or-choice)* [8]**

*Why:* the 2082 *or* question; the function family also includes 2080 and 2083.

A function has four components: **prototype (declaration)** — `int add(int, int);`,
which tells the compiler the name, return type and parameter types before use;
**definition** — the header and body, `int add(int a, int b) { return a + b; }`;
**call** — `add(5, 3);`; and the **return statement**, which sends a value back.

| | Call by value | Call by reference |
|---|---|---|
| What is passed | a copy of the value | the address of the variable |
| Changes inside the function | do not affect the original | change the original |
| Parameters | ordinary variables | pointers (`int *a`) |
| Call | `f(n)` | `f(&n)` |

```c
#include <stdio.h>

void by_value(int a)
{
    a = a + 10;
    printf("  inside by_value : a = %d\n", a);
}

void by_reference(int *a)
{
    *a = *a + 10;
    printf("  inside by_reference : *a = %d\n", *a);
}

int main(void)
{
    int n = 5;

    printf("n = %d before call by value\n", n);
    by_value(n);
    printf("n = %d after call by value\n", n);

    by_reference(&n);
    printf("n = %d after call by reference\n", n);
    return 0;
}
```

*Output:*

```text
n = 5 before call by value
  inside by_value : a = 15
n = 5 after call by value
  inside by_reference : *a = 15
n = 15 after call by reference
```

**8. Write the advantages of a pointer. Write a C program to enter the radius of a football and find its area using a user-defined function. *(NEB 2080, 3+5)* [8]**

*Why:* asked in 2080 exactly; the function family (2080, 2082, 2083) is the third
most common Q16 type.

*Advantages of pointers (three marks):* (1) they let a function change the caller's
variables (call by reference); (2) they give direct access to memory, so arrays,
strings and structures are handled efficiently; (3) they allow dynamic memory
allocation and data structures such as linked lists; (4) passing an address instead of
a large structure saves time and memory.

```c
#include <stdio.h>

float area(float r)
{
    return 3.14159f * r * r;
}

int main(void)
{
    float r;
    printf("Enter the radius of the football in cm: ");
    scanf("%f", &r);
    printf("Area = %.2f square cm\n", area(r));
    return 0;
}
```

*Output:*

```text
Enter the radius of the football in cm: 11
Area = 380.13 square cm
```

Check: 3.14159 × 11 × 11 = 380.13.

**9. What is artificial intelligence? Explain any five application areas of AI. *(NEB 2079, 2081, 2082)* [5]**

*Why:* three of the last six papers (2079, 2081, 2082); in 2081 and 2082 it was AI in
education, so a general or another-sector version is plausible.

**Artificial intelligence (AI)** is the branch of computer science that builds
computers and software able to do tasks that normally need human intelligence, such as
learning, reasoning, understanding language and recognising images. *(1)*

1. **Education** — adaptive learning programs, automatic marking and chatbots that
   answer students' questions.
2. **Healthcare** — programs that help doctors find disease in X-ray and scan images.
3. **Agriculture** — cameras and apps that identify crop disease and advise on water.
4. **Banking and business** — fraud detection, credit scoring, customer chatbots.
5. **Transport** — route finding and self-driving vehicles.
6. **Voice assistants and translation** — speech recognition and language translation. *(4)*

**10. What is cloud computing? Explain its service models and three advantages. *(NEB 2080 supplementary, 2083)* [5]**

*Why:* two of the last four papers (2080 supplementary and 2083); an MCQ on cloud
service types came in 2082.

**Cloud computing** is the delivery of computing services — storage, servers,
databases, software — over the internet ("the cloud") on demand, on a pay-as-you-use
basis. *(2)*

*Service models:* **IaaS** (Infrastructure as a Service) — virtual servers and
storage, for example Amazon EC2; **PaaS** (Platform as a Service) — a platform for
building and running applications, for example Google App Engine; **SaaS**
(Software as a Service) — ready-made software used through a browser, for example Gmail
or Google Docs.

*Advantages (three):* (1) **low cost** — no need to buy and maintain servers;
(2) **scalability** — resources can be increased or reduced quickly; (3) **access from
anywhere** on any device with internet, and automatic backup and updates. *(3)*

**11. Explain technical, economic and operational feasibility. *(NEB 2083 asked technical and economic; MCQs in 2082, 2080 supplementary and the CDC model)* [5]**

*Why:* 2083 asked it in writing; feasibility also came as an MCQ in 2082, 2080
supplementary and the CDC model, so it is a live topic. Operational is the third kind
not yet asked.

A **feasibility study** in the planning or analysis phase of the SDLC decides whether
the proposed system is worth building. *(1)*

| Type | Question answered | Example |
|---|---|---|
| **Technical** | is the technology — hardware, software, skills — available or obtainable? | can the school's computers run the new software? |
| **Economic** (cost–benefit) | do the benefits outweigh the costs? | is the saving in staff time worth the price of the software? |
| **Operational** | will the users accept and use the system in the organisation? | will teachers actually use the new result system? |

*(4: about 1.5 marks for each of the three, or 2+2 when only two are asked.)*

**12. Write a JavaScript program to find the factorial of a number using a function. *(NEB 2079, 2080)* [5]**

*Why:* two papers (2079, 2080); the smallest/largest-of-three and even/odd programs
are the other members of this recurring family (next question).

```html
<html>
<body>
<script>
function factorial(n) {
    var f = 1;
    for (var i = 1; i <= n; i++) {
        f = f * i;
    }
    return f;
}
var n = parseInt(prompt("Enter a number"));
document.write("Factorial of " + n + " is " + factorial(n));
</script>
</body>
</html>
```

For the input 6 the page shows: `Factorial of 6 is 720`.

**13. Write JavaScript programs (a) to check whether a number is even or odd, (b) to swap two numbers, (c) to find the smallest of three numbers. *(NEB 2081; CDC model; NEB 2082, 2083)* [5]**

*Why:* one of these has been the JavaScript alternative in every recent paper; the
smallest-of-three program was asked in 2082 *and* 2083, consecutively.

```html
<html>
<body>
<script>
function check(n) {
    if (n % 2 == 0)
        document.write(n + " is even");
    else
        document.write(n + " is odd");
}
check(parseInt(prompt("Enter a number")));
</script>
</body>
</html>
```

Input 13 — the page shows `13 is odd`.

```html
<html>
<body>
<script>
var x = 25, y = 60, temp;
document.write("Before: x = " + x + ", y = " + y + "<br>");
temp = x;
x = y;
y = temp;
document.write("After: x = " + x + ", y = " + y);
</script>
</body>
</html>
```

The page shows `Before: x = 25, y = 60` and then `After: x = 60, y = 25`.

```html
<html>
<body>
<script>
var a = parseFloat(prompt("Enter first number"));
var b = parseFloat(prompt("Enter second number"));
var c = parseFloat(prompt("Enter third number"));
var smallest = a;
if (b < smallest)
    smallest = b;
if (c < smallest)
    smallest = c;
document.write("The smallest number is " + smallest);
</script>
</body>
</html>
```

For the inputs 42, 17 and 30 the page shows `The smallest number is 17`.

**14. What is the purpose of `mysqli_connect()` in PHP? Describe its parameters and usage with an example. *(NEB 2081; 2080 supplementary; 2082)* [5]**

*Why:* the PHP alternative in every paper has started with this function; in 2081 it was
asked directly.

`mysqli_connect()` opens a connection between a PHP script and a MySQL database
server; nothing can be read or written before it succeeds. Syntax:
`mysqli_connect(server, username, password, database)`. The **server** is the host
name (`"localhost"` when MySQL is on the same machine), the **username** and
**password** are the MySQL account's, and the optional **database** selects the
database to use. It returns a connection object on success and `false` on failure.

```php
<?php
$conn = mysqli_connect("localhost", "root", "", "school");
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
echo "Connected successfully";
mysqli_close($conn);
?>
```

*Output:*

```text
Connected successfully
```

**15. What is normalization? Explain 1NF, 2NF and 3NF with an example. *(NEB 2082; 2079, 2081, 2083)* [5]**

*Why:* normalization was a Q10 option in four of the last five papers, each time
asking 2NF; 2082 asked 2NF *and* 3NF, so 3NF is the new edge.

**Normalization** is the process of organising the fields and tables of a relational
database to remove redundancy and unwanted dependencies. *(2)*

* **1NF** — every field holds one atomic value and there are no repeating groups.
* **2NF** — the table is in 1NF and there are no **partial dependencies** (no non-key
  field depends on only part of a composite key).
* **3NF** — the table is in 2NF and there are no **transitive dependencies** (no
  non-key field depends on another non-key field).

*Example of 3NF.* `EMPLOYEE(EmpID, Name, DeptID, DeptName)` has the key EmpID, and
`DeptName` depends on `DeptID`, which in turn depends on EmpID — a transitive
dependency. Split it into `EMPLOYEE(EmpID, Name, DeptID)` and
`DEPARTMENT(DeptID, DeptName)`; each department name is now stored once. *(3; the
2NF example is in Model Set 1, Question 10 (b).)*

### 16.4.3 Tier B — the slot is certain; the type is rarer or only asked as an MCQ

**16. Differentiate between DDL and DML. Give three SQL examples of each. *(NEB 2082; SQL create/alter/drop in 2080)* [5]**

*Why:* 2082 asked it; SQL commands fill many of the DBMS MCQs (2082 `ALTER`, 2083 `SELECT`).

| | DDL (Data Definition Language) | DML (Data Manipulation Language) |
|---|---|---|
| Purpose | defines and changes the structure of the database | inserts, changes, deletes and retrieves the data |
| Commands | `CREATE`, `ALTER`, `DROP` | `INSERT`, `UPDATE`, `DELETE`, `SELECT` |
| Acts on | tables, views, indexes | rows of a table |
| Rollback | changes are made permanent immediately | can be rolled back inside a transaction |

Examples — DDL: `CREATE TABLE student(roll INT, name VARCHAR(30));`,
`ALTER TABLE student ADD phone VARCHAR(10);`, `DROP TABLE student;`. DML:
`INSERT INTO student VALUES (1, 'Anita');`, `UPDATE student SET name = 'Asha' WHERE roll = 1;`,
`DELETE FROM student WHERE roll = 1;`.

**17. Explain the hierarchical, network and relational database models. *(hierarchical vs relational NEB 2083; relational 2080, 2080 supplementary, model)* [5]**

*Why:* the relational model was asked four times, hierarchical once; the network model
has never been a written question.

| Model | Structure | Relationships | Merits | Demerits |
|---|---|---|---|---|
| **Hierarchical** | a tree of parent and child records | one parent to many children | fast for top-down access | one parent only; rigid; hard to change |
| **Network** | a graph of records joined by links | a record can have many parents (many-to-many) | flexible, efficient | complex to design and maintain |
| **Relational** | tables (relations) of rows and columns | tables joined by keys | simple, flexible, SQL language, most widely used | needs care in design of keys; joins can be slow on huge data |

The relational model is preferred by most organisations because data is held in
simple tables, queries are written in SQL without knowing how the data is stored, and
the structure can be changed easily.

**18. Explain the advantages of a DBMS over a traditional file-based system. *(NEB 2081; 2080 supplementary "importance of a database")* [5]**

*Why:* asked in 2081 and, as "importance of a database", in the 2080 supplementary.

| File system | DBMS |
|---|---|
| the same data stored in several files — redundancy | data stored once — low redundancy |
| copies may disagree — inconsistency | one copy — consistent |
| programs depend on the file format | data independence |
| little security and no access control | passwords and privileges |
| hard to share between users at once | many users at once |
| backup and recovery by hand | built-in backup and recovery |

**19. Define primary key, candidate key and alternate key with an example. *(MCQs in 2079, 2080 supplementary, 2082, 2083; syllabus bullet)* [5]**

*Why:* key MCQs appeared in four of the last six papers but the topic has not been a
written question — a typical gap.

A **primary key** is the field (or fields) that uniquely identifies each record; it
cannot be duplicated or NULL. A **candidate key** is any field or set of fields that
could serve as the primary key. An **alternate key** is a candidate key that was not
chosen as the primary key.

*Example.* In `student(roll, email, name, phone)`, both `roll` and `email` are unique,
so both are **candidate keys**; `roll` is chosen as the **primary key**, which makes
`email` the **alternate key**.

**20. Write short notes on database security. *(syllabus bullet, never yet asked)* [5]**

*Why:* pure gap — a named bullet in the DBMS unit that no paper has asked in writing.

**Database security** is the protection of the data from unauthorised access, change,
theft and loss. Main measures: (1) **authentication** — usernames and passwords (or
other identity checks) for every user; (2) **authorisation / access control** —
privileges decide who may read, insert, change or delete each table; (3) **encryption**
of stored and transmitted data; (4) **backup and recovery** so that data can be
restored after a failure; (5) **firewall and anti-virus** to block attacks through the
network; (6) **audit trail** — a log of who did what; (7) physical protection of the
server room.

**21. Differentiate between object-oriented and procedural programming. *(NEB 2079, CDC model)* [5]**

*Why:* asked in 2079 and in the model question.

| Basis | Procedural programming | Object-oriented programming |
|---|---|---|
| Emphasis | procedures (functions) | data (objects) |
| Approach | top-down | bottom-up |
| Data | global data, shared by functions; less secure | data hidden inside objects; more secure |
| Reuse | copy or call functions | inheritance |
| Real-world modelling | difficult | natural |
| Examples | C, Pascal | C++, Java |

**22. What are the features of OOP? Explain four of them. *(NEB 2083)* [5]**

*Why:* asked in 2083; OOP appears in every paper, so the next question is another
angle on the same unit.

1. **Class** — a blueprint that defines the data and functions of a kind of object.
2. **Object** — an instance of a class, with its own values.
3. **Polymorphism** — one name, many forms: a function or operator behaves
   differently in different situations (overloading).
4. **Inheritance** — a new class acquires the properties and behaviour of an
   existing one, giving reuse.

(Also: **encapsulation** — data and functions bound in one unit with data hiding;
**abstraction** — showing only what is essential.)

**23. Explain inheritance with an example. *(NEB 2080 supplementary, 2082)* [5]**

*Why:* asked in 2080 supplementary and 2082.

**Inheritance** lets a *derived class* acquire the members of a *base class*, so code
written once is reused. Types: single, multilevel, multiple, hierarchical and
hybrid. Real-world example: a child inherits features from its parents. In the
program, `Dog` inherits `eat()` from `Animal`, and `Puppy` inherits from `Dog` —
multilevel inheritance, so a `Puppy` object can call all three functions.

```cpp
#include <iostream>
using namespace std;

class Animal {
public:
    void eat() { cout << "This animal eats food." << endl; }
};

class Dog : public Animal {
public:
    void bark() { cout << "The dog barks." << endl; }
};

class Puppy : public Dog {
public:
    void weep() { cout << "The puppy weeps." << endl; }
};

int main()
{
    Puppy p;
    p.eat();
    p.bark();
    p.weep();
    return 0;
}
```

*Output:*

```text
This animal eats food.
The dog barks.
The puppy weeps.
```

**24. State the advantages and applications of OOP. *(syllabus bullets)* [5]**

*Why:* both are named syllabus bullets and neither has been a written question.

*Advantages:* **reusability** through inheritance; **data hiding** gives security;
**modularity** — classes can be developed and tested separately; easier
**maintenance** and extension; natural **modelling of real-world** problems.
*Applications:* graphical user interfaces and desktop software, computer games,
simulation and modelling, database systems, computer-aided design, artificial
intelligence and real-time systems.

**25. Differentiate between a system analyst and a software engineer. *(syllabus bullet)* [5]**

*Why:* a named bullet of the software-process unit that has not been a written question.

| | System analyst | Software engineer |
|---|---|---|
| Main work | studies the user's problem and decides what the system must do | designs, builds, tests and maintains the software |
| Focus | *what* — requirements, feasibility | *how* — design and code |
| Skills | communication, business knowledge, analysis | programming, design, testing |
| Role | links the users with the developers | works with the development team |
| Produces | requirement specification, system models | working, tested software |

**26. Explain the phases of the system development life cycle (SDLC). *(syllabus bullet)* [5]**

*Why:* SDLC phases are asked indirectly (design 2079, system testing 2080,
requirements 2080 supplementary to 2082, feasibility 2083) — the complete life cycle is
the parent question.

The **SDLC** is the series of phases through which a software project passes: (1)
**planning and feasibility study**; (2) **requirement analysis** — gathering and
specifying what users need; (3) **design** — architecture, database and screens;
(4) **implementation (coding)**; (5) **testing** — finding and correcting faults;
(6) **deployment** — installing the system; (7) **maintenance** — corrections and
improvements after delivery.

**27. Compare the waterfall model with the agile model. *(waterfall MCQs in 2081 and 2083; syllabus)* [5]**

*Why:* the waterfall model has been an MCQ in 2081 and 2083; a written comparison with
the agile model — the third model in the syllabus bullet — is the natural step up.

| | Waterfall | Agile |
|---|---|---|
| Approach | linear, one phase after the other | iterative and incremental, in short cycles |
| Changes in requirements | hard and costly | welcome at any time |
| User involvement | mainly at the start and the end | continuous |
| Delivery | one final product | working software delivered often |
| Suited to | small projects with fixed requirements | projects whose needs change |

**28. Explain the importance of system testing in the SDLC. *(NEB 2080, 1+4)* [5]**

*Why:* asked in 2080 with the bracket (1+4): one definition and four reasons.

**System testing** is the testing of the complete, integrated system to check that it
meets the specified requirements. *(1)* Importance: (1) finds errors before the user
does; (2) checks that the requirements are met; (3) raises quality and reliability;
(4) costs less than correcting faults after delivery; (5) builds the user's
confidence. Other tests: unit, integration and acceptance testing. *(4)*

**29. Write any five qualities of good software. *(CDC model)* [5]**

*Why:* the model question asked it; it is the "software and quality" bullet.

(1) **Correctness** — it does what the requirements say; (2) **reliability** — works
without failure; (3) **efficiency** — uses little time and memory; (4) **usability** —
easy to learn and use; (5) **maintainability** — easy to correct and improve;
(6) **portability** — runs on different systems; (7) **security** — protects data.

**30. What activities are performed to design software? *(NEB 2079)* [5]**

*Why:* asked in 2079 as "major activities performed to design the software".

System design turns the requirement specification into a plan for the program. The
main activities: **architectural design** (choosing the overall structure and
modules); **database design** (tables, keys, relationships); **interface design**
(screens, menus and reports for users); **input and output design**; **program
(component) design** (algorithms, flowcharts and pseudocode for each module).

**31. Explain mobile computing with its advantages and disadvantages. *(CDC model)* [5]**

*Why:* the recent-trends slot has had AI, cloud and mobile computing in turn; the
model question carried mobile computing.

**Mobile computing** is the use of portable computing devices — smartphones, tablets,
laptops — that can communicate over wireless networks while the user is moving.
*Advantages:* work and communicate anywhere, anytime; instant access to information
and services; saves time. *Disadvantages:* small screen and keyboard; limited battery
life; security risks on public networks; depends on network coverage.

**32. What is big data? Explain its characteristics. *(MCQ on the four V's, 2080 supplementary)* [5]**

*Why:* the four V's came as an MCQ in the 2080 supplementary.

**Big data** means data sets so large, fast-growing and varied that ordinary database
tools cannot store and process them. The four characteristics: **Volume** — the huge
quantity; **Velocity** — the speed at which it is generated; **Variety** — text,
images, video and sensor data; **Veracity** — the accuracy and trustworthiness of the
data. Uses: social-media analysis, recommendations in online shopping, weather
forecasting, health records.

**33. What is robotics? State its advantages and applications. *(syllabus: "AI and Robotics")* [5]**

*Why:* the syllabus bullet pairs AI with robotics, but only AI has been asked.

**Robotics** is the branch of technology that designs, builds and programs robots —
machines that can carry out tasks automatically. *Advantages:* accuracy and speed;
works without tiring; replaces people in dangerous jobs. *Applications:* factory
assembly, surgery, bomb disposal, space exploration, warehouses. *Disadvantage:*
high cost and possible loss of jobs.

**34. Explain e-commerce, e-governance and e-medicine with examples. *(syllabus bullet)* [5]**

*Why:* a three-part syllabus bullet that has not yet been a written question.

**E-commerce** — buying and selling goods and services over the internet, such as
shopping on Daraz. **E-governance** — use of ICT to deliver government services to
citizens, such as applying for a passport online. **E-medicine** — health care using
ICT, for example a doctor in a city advising a patient in a remote district by video
call.

### 16.4.4 Tier C — named in the syllabus, not yet a written question, or fits the 8-mark slot

**35. Explain the OSI reference model. *(OSI full form asked as an MCQ in 2083)* [8]**

*Why:* 2083's MCQ shows the examiner is reading this bullet; it has never been a written
question, and networking owns an 8-mark slot.

The **OSI (Open Systems Interconnection) reference model** divides network communication
into seven layers so that different systems can communicate. Memory aid: *Please Do
Not Throw Sausage Pizza Away*.

| No. | Layer | Function | Example |
|---|---|---|---|
| 7 | Application | services that the user's program uses | HTTP, FTP, SMTP |
| 6 | Presentation | translation, encryption, compression | JPEG, TLS |
| 5 | Session | starts, maintains and ends a dialogue | session control |
| 4 | Transport | end-to-end delivery, error control, segmentation | TCP, UDP |
| 3 | Network | logical addressing (IP) and routing | IP, router |
| 2 | Data link | frames, MAC addressing, error detection between neighbours | Ethernet, switch |
| 1 | Physical | transmits raw bits as signals | cable, hub |

**36. Write the function of NIC, modem, router and switch. *(syllabus bullet)* [5]**

*Why:* the device bullet produced a router MCQ in this chapter's Set 1 but no written
question in the papers.

* **NIC (network interface card)** — the card that connects a computer to a network and
  holds its unique MAC address.
* **Modem** (modulator–demodulator) — converts digital signals to analogue for
  transmission over a telephone or cable line and back again.
* **Router** — joins different networks and forwards packets by IP address along the best path.
* **Switch** — joins computers in a LAN and forwards data only to the port of the destination.

**37. Explain the terms IP address, subnet mask, gateway and MAC address. *(IP/MAC MCQs in 2079, 2080 supplementary, 2081, CDC model)* [5]**

*Why:* four MCQs in seven papers; it is the most frequently used network fact base.

**IP address** — the logical address of a host: IPv4 has 32 bits, written as four
decimal numbers from 0 to 255 (for example 192.168.1.1); `256.2.5.76` and
`192.168.1` are invalid. Private ranges: 10.x.x.x, 172.16.x.x–172.31.x.x, 192.168.x.x.
**Subnet mask** — tells which part of the IP address is the network and which the host
(for example 255.255.255.0). **Gateway** — the router address through which a host
reaches other networks. **MAC address** — the 48-bit physical address burned into the
NIC, written as six hexadecimal pairs.

**38. What are transmission impairments? Explain any four. *(syllabus bullet)* [5]**

*Why:* the syllabus lists eight impairments; none has been a written question.

**Transmission impairments** are the faults that weaken or change a signal on its way
from the sender to the receiver. **Noise** — unwanted electrical energy added to the
signal. **Crosstalk** — the signal of one wire leaking into a neighbouring wire.
**Echo** — part of the signal reflected back to the sender. **Distortion** — change in
the shape of the signal because its frequency components travel and weaken
differently. (Others: jitter — irregular delay in arrival; singing — a continuous
whistle caused by feedback; limited bandwidth; too many receivers.)

**39. Differentiate between LAN and WAN. Explain simplex, half duplex and full duplex. *(syllabus bullets)* [5]**

*Why:* both are basic bullets; no written question so far.

| | LAN | WAN |
|---|---|---|
| Area | a room, building or campus | cities, countries, the world |
| Speed | high | lower |
| Ownership | one organisation | many; uses leased and public carriers |
| Cost | low | high |

**Simplex** — data flows in one direction only (keyboard to computer, television
broadcast). **Half duplex** — both directions but one at a time (walkie-talkie).
**Full duplex** — both directions at the same time (telephone).

**40. Differentiate between structure and union in C. *(syllabus bullet)* [5]**

*Why:* a named bullet ("difference between union and structure") not yet asked.

A **structure** gives every member its own memory, so its size is about the sum of the
members; all members can hold values at the same time. A **union** shares one memory
area among all members, so its size equals that of the largest member and only one
member holds a value at a time. Declared with `struct` and `union`.

```c
#include <stdio.h>

struct sdata { int i; float f; char c; };
union  udata { int i; float f; char c; };

int main(void)
{
    union udata u;
    printf("sizeof(struct sdata) = %zu bytes\n", sizeof(struct sdata));
    printf("sizeof(union udata)  = %zu bytes\n", sizeof(union udata));

    u.i = 65;
    printf("u.i = %d\n", u.i);
    u.c = 'Z';
    printf("after u.c = 'Z' : u.c = %c, u.i = %d\n", u.c, u.i & 0xFF);
    return 0;
}
```

*Output (gcc on a 64-bit Linux machine; the structure size includes padding):*

```text
sizeof(struct sdata) = 12 bytes
sizeof(union udata)  = 4 bytes
u.i = 65
after u.c = 'Z' : u.c = Z, u.i = 90
```

**41. Explain the automatic and external storage classes with an example. *(syllabus bullet)* [5]**

*Why:* a named bullet of the C unit not yet asked.

An **automatic** variable (`auto`, the default inside a function) is created when the
function is entered and destroyed when it ends; it is visible only inside that function.
An **external** variable (`extern`) is declared outside all functions, is created when
the program starts, lives until it ends and can be used by every function.

```c
#include <stdio.h>

int total = 100;

void demo(void)
{
    int a = 0;
    static int s = 0;
    a++;
    s++;
    total += 10;
    printf("a = %d, s = %d, total = %d\n", a, s, total);
}

int main(void)
{
    demo();
    demo();
    demo();
    return 0;
}
```

*Output:*

```text
a = 1, s = 1, total = 110
a = 1, s = 2, total = 120
a = 1, s = 3, total = 130
```

`a` is automatic and starts at 0 in every call; `total` is external and keeps
growing; `s` (static) keeps its value between calls.

**42. Write a C program (a) to check whether a number is positive, negative or zero using a function and (b) to generate the Fibonacci series starting with 7 and 14 up to ten terms using a function. *(NEB 2083, 4+4)* [8]**

*Why:* the 2083 question with two 4-mark parts; programs do repeat in consecutive years
(smallest of three in 2082 and 2083), so it is worth having ready.

```c
#include <stdio.h>

void fibonacci(int first, int second, int terms)
{
    int i, next;
    printf("%d %d", first, second);
    for (i = 3; i <= terms; i++) {
        next = first + second;
        printf(" %d", next);
        first = second;
        second = next;
    }
    printf("\n");
}

void check(int n)
{
    if (n > 0)
        printf("%d is positive\n", n);
    else if (n < 0)
        printf("%d is negative\n", n);
    else
        printf("Zero\n");
}

int main(void)
{
    int n;
    printf("Enter a number: ");
    scanf("%d", &n);
    check(n);
    fibonacci(7, 14, 10);
    return 0;
}
```

*Output:*

```text
Enter a number: -5
-5 is negative
7 14 21 35 56 91 147 238 385 623
```

**43. Explain the file functions `putw()`, `getw()`, `putc()`, `getc()`, `fscanf()` and `fprintf()`. Differentiate between sequential and random files. *(syllabus bullet)* [5]**

*Why:* the function list is itself a syllabus bullet.

| Function | Purpose |
|---|---|
| `putc(ch, fp)` / `getc(fp)` | write / read one character |
| `putw(n, fp)` / `getw(fp)` | write / read one integer |
| `fprintf(fp, format, args)` / `fscanf(fp, format, args)` | write / read formatted data, as `printf` and `scanf` do for the screen |

A **sequential file** is read or written record after record from the beginning; a
**random file** lets the program jump straight to any record (with `fseek()`).

```c
#include <stdio.h>

int main(void)
{
    FILE *fp;
    int n, sum = 0, i;

    fp = fopen("numbers.dat", "wb");
    for (i = 1; i <= 5; i++)
        putw(i * 10, fp);
    fclose(fp);

    fp = fopen("numbers.dat", "rb");
    while ((n = getw(fp)) != EOF) {
        printf("%d ", n);
        sum += n;
    }
    fclose(fp);
    printf("\nSum = %d\n", sum);
    return 0;
}
```

```text
10 20 30 40 50 
Sum = 150
```

```c
#include <stdio.h>

int main(void)
{
    FILE *in, *out;
    int ch;

    out = fopen("note.txt", "w");
    fputs("NEBians is free.\nStudy every day.\n", out);
    fclose(out);

    in = fopen("note.txt", "r");
    out = fopen("copy.txt", "w");
    while ((ch = getc(in)) != EOF)
        putc(ch, out);
    fclose(in);
    fclose(out);

    out = fopen("copy.txt", "a");
    fprintf(out, "Appended line: %d\n", 2083);
    fclose(out);

    in = fopen("copy.txt", "r");
    while ((ch = getc(in)) != EOF)
        putchar(ch);
    fclose(in);
    return 0;
}
```

```text
NEBians is free.
Study every day.
Appended line: 2083
```

**44. Write a PHP script with variables of different data types and operators, and explain the data types. *(syllabus bullets)* [5]**

*Why:* the basic-syntax bullets have produced MCQs (`$variable`, an invalid variable
name in 2082) but no written question.

PHP variables start with `$`, need no type declaration and are case-sensitive. The
main data types are integer, float (double), string, boolean and array.

```php
<?php
$name = "Nepal";
$area = 147516;
$ratio = 0.6;
$open = true;
$items = array("pen", "book", "bag");
$a = 17;
$b = 5;

echo "Country: $name\n";
echo "Area: $area square km, gettype = " . gettype($area) . "\n";
echo "a + b = " . ($a + $b) . ", a % b = " . ($a % $b) . "\n";
echo "Items: " . implode(", ", $items) . " (" . count($items) . ")\n";
echo "a > b and b > 0 is ";
echo ($a > $b && $b > 0) ? "true" : "false";
echo "\n";
?>
```

```text
Country: Nepal
Area: 147516 square km, gettype = integer
a + b = 22, a % b = 2
Items: pen, book, bag (3)
a > b and b > 0 is true
```

**45. Write a PHP script to create a database and a table. *(syllabus bullet: "creating SQL database with server-side scripting")* [5]**

*Why:* a named bullet not yet asked.

```php
<?php
$conn = mysqli_connect("localhost", "root", "");
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
if (mysqli_query($conn, "CREATE DATABASE library")) {
    echo "Database created\n";
}
mysqli_select_db($conn, "library");
$sql = "CREATE TABLE book (id INT PRIMARY KEY, title VARCHAR(50), price FLOAT)";
if (mysqli_query($conn, $sql)) {
    echo "Table created\n";
}
mysqli_close($conn);
?>
```

*Output:*

```text
Database created
Table created
```

**46. Write short notes on JavaScript events, with an example that changes an image; and on jQuery hide/show. *(syllabus bullets; `hide()` as a 2080 MCQ)* [5]**

*Why:* the 2080 paper asked the jQuery `hide()` method as an MCQ and event handling is
a named bullet.

An **event** is an action on the page, such as a click, a mouse-over or a form
submit; **event handling** is running JavaScript code when it happens, using
attributes such as `onclick`, `onmouseover` and `onsubmit`.

```html
<html>
<body>
<img id="pic" src="close.png" width="80">
<button id="b" onclick="change()">Open</button>
<script>
function change() {
    document.getElementById("pic").src = "open.png";
}
</script>
</body>
</html>
```

Result: before the click `src = close.png`; after the click `src = open.png`.

**jQuery** is a JavaScript library that shortens common tasks; the `$` sign starts
every statement, for example `$("p").hide();` and `$("p").show();`.

```html
<html>
<head>
<script src="jquery.min.js"></script>
<script>
$(document).ready(function () {
    $("#hide").click(function () { $("p").hide(); });
    $("#show").click(function () { $("p").show(); });
});
</script>
</head>
<body>
<p>NEBians is a free study platform.</p>
<button id="hide">Hide</button>
<button id="show">Show</button>
</body>
</html>
```

Clicking *Hide* set the paragraph's style to `display: none`; clicking *Show* restored
it (checked with jQuery running in a simulated browser page).

**47. Explain pointer expressions and the address (&) and indirection (\*) operators. *(`&` asked as an MCQ in 2081; syllabus bullet)* [5]**

*Why:* the pointer MCQs (2079 output, 2081 `&`) show the topic is live.

```c
#include <stdio.h>

int main(void)
{
    int a = 10, b = 4;
    int *p = &a, *q = &b;
    int arr[4] = {2, 4, 6, 8};
    int *r = arr;

    printf("*p + *q = %d\n", *p + *q);
    printf("*p * *q = %d\n", *p * *q);
    *p = *p + 5;
    printf("a after *p = *p + 5 : %d\n", a);
    printf("Is p == &a ? %s\n", p == &a ? "yes" : "no");
    printf("*(r + 2) = %d\n", *(r + 2));
    r++;
    printf("after r++ : *r = %d\n", *r);
    return 0;
}
```

*Output:*

```text
*p + *q = 14
*p * *q = 40
a after *p = *p + 5 : 15
Is p == &a ? yes
*(r + 2) = 6
after r++ : *r = 4
```

`&a` is the address of `a`; `*p` is the value at the address stored in `p`, so `*p = *p + 5`
changes `a` itself. `r++` moves the pointer to the next `int`, and `*(r + 2)` is the third
element.

## Chapter summary

- The paper is regular: Q10 is DBMS, Q11 web (JavaScript *or* PHP), Q12 OOP, Q13
  software process, Q14 recent trends, Q15 networking (8 marks) and Q16 a C program
  (8 marks) in every paper read.
- Group A splits 2–1–2–1–1–1–1 across DBMS, networking, web, C, OOP, software
  process and recent trends in the five papers that could be checked closely.
- Marks by unit in a typical paper: networking 9, C 9, DBMS 7, web 7, OOP 6, software
  process 6, recent trends 6.
- Q15 is topologies or transmission media; Q16 is an array of structure, with file
  handling or a function/pointer program as the *or* choice.
- Answer to the bracket — *(1+4)*, *(2+6)* — and underline the keyword, draw the
  diagram, and number the points.
- The recurring programs — factorial, smallest of three, swap, even/odd, structure,
  file — are worth writing out until they are automatic.
- Practise the two model sets against the clock: nine MCQs in ten minutes, leaving
  about 110 minutes for the 41 written marks.

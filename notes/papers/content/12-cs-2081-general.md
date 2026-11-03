---
file: NEBians-Past-Paper-Grade-12-Computer-Science-2081.pdf
subject: Computer Science
grade: 12
year_bs: 2081
year_ad: 2024
stream: Regular and Grade Increment
code: 4281
time: 2 hrs
marks: 50
students: For regular and grade increment students whose first two digits of registration number start from 78, 79 and 80
category: Board Exam
---
## Group 'A'
<small>Multiple choice questions · rewrite the correct option of each question in your answer sheet · [9×1=9]</small>

@mcq 1
Which one of the following given statements is correct?
@opts-col SELECT * FROM emp WHERE empid = 103; | SELECT FROM emp WHERE empid = 103; | SELECT empid WHERE emp = 103 FROM emp; | SELECT empid WHERE empid = 103 AND table = emp;

@mcq 2
Which database system normally offers better performance for geographically dispersed users?
@opts Centralized database system | Distributed database system | NoSQL database system | Relational database system

@mcq 3
Which of the following is an example of a public IPv4 address?
@opts 192.168.1.1 | 172.16.10.1 | 10.10.10.10 | 203.0.113.10

@mcq 4
What is the correct syntax for a 'for' loop in JavaScript?
@opts-col for (var i = 0; i < 5; i++) {} | for (i = 0; i < 5; i++) {} | for (var i = 0; i < 5) {} | for (var i < 5; i++) {}

@mcq 5
Which PHP function is commonly used to execute SQL queries on a database connection established using the mysqli extension?
@opts mysqli_query() | pdo_query() | mysql_query() | pgsql_query()

@mcq 6
What is the correct syntax to declare a structure in C?
@opts struct { } | define struct { } | struct [ ] | struct <name> { }

@mcq 7
In C, which operator is used to get the address of a variable?
@opts * | & | -> | .

@mcq 8
Which OOP feature allows a class to inherit properties and behaviour from another class?
@opts Inheritance | Encapsulation | Polymorphism | Abstraction

@mcq 9
Which model of SDLC is characterized by a linear progression of phases from requirements gathering to maintenance?
@opts Waterfall model | Agile model | Spiral model | RAD model

## Group 'B'
<small>Short answer questions · [5×5=25]</small>

@q 10
Evaluate the advantages of DBMS compared to traditional file-based data storage systems. [[5]]
@or
How does Second Normal Form (2NF) differ from First Normal Form (1NF), and what are the key benefits of achieving 2NF in database design? Explain. [[2+3]]

@q 11
Write a JavaScript function that checks if a number is even or odd and prints the result. [[1+4]]
@or
What is the purpose of the mysqli_connect() function in PHP? Describe its usage and parameters. [[2+3]]

@q 12
Write a short note on class and object in OOP with a real-world example. [[2.5+2.5]]

@q 13
How do various requirement gathering techniques help in achieving a careful grasp of user needs and system requirements during the analysis phase of the SDLC? [[5]]

@q 14
Give five examples of AI applications in education. [[5]]

## Group 'C'
<small>Long answer questions · [2×8=16]</small>

@q 15
How does the star network topology differ from the bus network topology in terms of its architectural layout and data transmission methodology in modern computing environments? [[8]]

@q 16
Write a C program that uses structures to represent details of five books (title, author, publisher and price) and prints them out. [[8]]
@or
Discuss the concept of binary file handling in C programming and explain how putw() and getw() functions facilitate binary input/output operations. Give examples. [[8]]

<!-- SOLUTIONS -->
### Group A — answer key

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Ans | A | B | D | A | A | D | B | A | A |

**1. A.** The correct form is `SELECT <columns> FROM <table> WHERE <condition>;`. Options B, C and D have the column list, FROM or WHERE in the wrong place.

**2. B.** A distributed database stores data at several sites close to the users, which reduces network delay and gives local autonomy and better availability for geographically dispersed users.

**3. D.** 192.168.x.x, 172.16.x.x–172.31.x.x and 10.x.x.x are private ranges (RFC 1918), not routable on the internet. 203.0.113.10 is outside those ranges, so it is a public address.

**4. A.** JavaScript syntax is `for (initialization; condition; increment) { }`, with all three parts. (Option B also runs if `i` is already declared; A is the standard, correct form which declares `i` with `var`.)

**5. A.** `mysqli_query($conn, $sql)` sends a query to a MySQL server through the mysqli extension. `mysql_query()` belongs to the old, removed mysql extension.

**6. D.** `struct name { members };` declares a structure type in C.

**7. B.** `&` is the address-of operator (`&x`), while `*` dereferences a pointer.

**8. A.** Inheritance lets a derived class reuse the data members and member functions of a base class.

**9. A.** The Waterfall model moves through requirements → design → implementation → testing → deployment → maintenance in a strict linear sequence.

### Group B

@s 10
**Advantages of a DBMS over the file-based system**

In a file-processing system every application keeps its own files, so the same data is stored again and again and each program depends on the file format. A database management system (DBMS) keeps all data in one organised database and gives all users controlled access to it. The advantages are:
1. **Reduced data redundancy:** data is stored once in a central database, not in many files, so storage is saved and duplicate entry is avoided.
2. **Data consistency and integrity:** since there is one copy, an update is seen by all users. Integrity constraints (primary key, foreign key, check, not null) keep the data correct.
3. **Data sharing:** many users and applications can use the same data at the same time, with concurrency control to avoid conflicts.
4. **Data independence:** programs are separated from the physical storage, so the structure can change without rewriting the application programs.
5. **Security:** the DBMS gives passwords, user roles and privileges (GRANT/REVOKE), so that each user sees only the data they may see.
6. **Backup and recovery:** automatic logs, checkpoints and recovery after a system failure; a file system has no such tools.
7. **Easy querying and fast development:** a standard language (SQL) can answer new queries easily, while a file system needs a new program for each.

| File-based system | DBMS |
|---|---|
| High redundancy and inconsistency | Controlled redundancy |
| Program–data dependence | Data independence |
| Weak security | Strong security and access control |
| Difficult sharing and concurrency | Concurrent multi-user access |
| No standard recovery | Backup and recovery tools |

**Or.** **1NF vs 2NF.** A relation is in **First Normal Form (1NF)** if every attribute holds only atomic (indivisible) values, there are no repeating groups or multivalued attributes, and every row is uniquely identified. A relation is in **Second Normal Form (2NF)** if it is already in 1NF and **every non-key attribute is fully functionally dependent on the whole primary key**, i.e. there is no *partial dependency* (a non-key attribute depending on only a part of a composite key).

*Example:* Enrol(StudentID, CourseID, StudentName, Grade) with key (StudentID, CourseID) is in 1NF, but StudentName depends only on StudentID (a partial dependency), so it is not in 2NF. We split it into Student(StudentID, StudentName) and Enrol(StudentID, CourseID, Grade).

*Benefits of 2NF:*
- Removes the redundancy of repeated student names, so less storage is used.
- Avoids update anomaly (a name must be changed in many rows), insertion anomaly (a student cannot be stored until he enrols in a course) and deletion anomaly (deleting the last enrolment loses the student).
- Improves the consistency and gives a good base for 3NF.

@s 11
A number is **even** if it is divisible by 2 with no remainder (`n % 2 === 0`); otherwise it is odd.

```js
function checkEvenOdd(n) {
  if (n % 2 === 0) {
    console.log(n + " is even");
  } else {
    console.log(n + " is odd");
  }
}

checkEvenOdd(14);   // 14 is even
checkEvenOdd(7);    // 7 is odd

// In a web page the number can be read from a text box:
// let n = Number(prompt("Enter a number"));
// checkEvenOdd(n);  // or document.write(...) / alert(...)
```

The function takes a parameter `n`, uses the modulus operator `%` to find the remainder after division by 2 and prints the result by an `if–else` statement. Negative numbers also work, because −3 % 2 gives −1, which is not 0.

**Or.** **Purpose.** `mysqli_connect()` opens a connection from a PHP script to a MySQL/MariaDB database server using the `mysqli` extension. It returns a connection object (resource) on success, or `false` on failure, and this connection is used by later functions such as `mysqli_query()`, `mysqli_fetch_assoc()` and `mysqli_close()`.

**Syntax and parameters:**
`mysqli_connect(host, username, password, dbname, port, socket);`
- **host**: the server name or IP address, e.g. `"localhost"`.
- **username**: the MySQL user, e.g. `"root"`.
- **password**: the password of that user (empty string for none).
- **dbname**: the default database to use (optional).
- **port**: the MySQL port, default 3306 (optional); **socket**: the socket or named pipe (optional).

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
`mysqli_connect_error()` returns the reason for failure, and `mysqli_close($conn)` ends the connection.

@s 12
**Class.** A class is a user-defined *blueprint* or template that describes the *data members* (attributes/properties) and the *member functions* (methods/behaviour) common to a group of similar objects. It does not use memory for data until objects are created from it.
**Object.** An object is a *real instance* of a class. It has its own state (values of the attributes), behaviour (the methods that can be called on it) and identity, and it occupies memory. Many objects can be made from one class.

**Real-world example.** `Car` is a class: attributes are `colour`, `model`, `speed`; behaviours are `start()`, `accelerate()`, `brake()`. A red Toyota and a white Hyundai are two *objects* of the class Car, with different values of the attributes but the same set of operations.

```cpp
#include <iostream>
using namespace std;

class Car {
public:
    string model;
    int speed;
    void accelerate() { speed += 10; }
    void show() { cout << model << " runs at " << speed << " km/h\n"; }
};

int main() {
    Car c1, c2;            // c1 and c2 are objects of class Car
    c1.model = "Toyota"; c1.speed = 40;
    c2.model = "Hyundai"; c2.speed = 60;
    c1.accelerate();
    c1.show();             // Toyota runs at 50 km/h
    c2.show();             // Hyundai runs at 60 km/h
    return 0;
}
```
A class gives *encapsulation* (data and functions bound together) and the reuse of code, because one class definition produces any number of objects.

@s 13
In the **analysis phase** of the SDLC the analyst must find out *what* the users need from the new system. Missing or wrongly understood requirements are the main reason for failed projects, so several **requirement gathering (fact-finding) techniques** are used together:
1. **Interviews:** face-to-face questions to managers and users give detailed, first-hand information and let the analyst ask follow-up questions and notice attitudes. They are time-consuming but rich in detail.
2. **Questionnaires/surveys:** the same set of questions sent to many users collects the opinions of a large and scattered group quickly and cheaply, and the answers are easy to tabulate.
3. **Observation:** watching users do their real work shows what they actually do, the problems and the bottlenecks that they forget or fail to tell.
4. **Document and record review:** studying forms, reports, manuals and old files shows the current data, rules and procedures of the organisation.
5. **Joint Application Development (JAD) workshops / brainstorming:** users, managers and developers meet together, so that conflicts are settled early and a shared view is built.
6. **Prototyping:** a working sample screen or model is shown to the users, who can react to something concrete, which clarifies unclear requirements.

By combining these techniques the analyst can cross-check the facts from several sources, find hidden and conflicting needs, avoid errors that would be costly to correct later, and write a complete and agreed Software Requirement Specification (SRS), which is the base for design.

@s 14
Five applications of AI in education:
1. **Personalised/adaptive learning:** platforms (e.g. Khan Academy, Duolingo) study each student's answers and change the content, speed and difficulty to suit the learner.
2. **Intelligent tutoring systems and chatbots:** virtual tutors answer questions 24 hours a day, explain steps and give hints, e.g. ChatGPT-based study assistants.
3. **Automated grading and feedback:** AI marks multiple-choice tests and even essays or programming assignments, saving the teachers' time and giving quick feedback.
4. **Speech recognition and language translation:** tools such as Google Translate and speech-to-text help students learn languages and help the hearing- or visually-impaired learners (text-to-speech, captions).
5. **Smart content and learning analytics:** AI makes digital lessons, summaries and quizzes, and analyses attendance and marks to predict the students at risk of failing so that teachers can help early. (Other examples: plagiarism detection, virtual labs, admission and timetable automation.)

@s 15
**Network topology** is the physical or logical arrangement of the nodes and links of a network. Two common types are the bus and the star.

```figure caption="Bus topology (left) and star topology (right)."
from matplotlib.patches import Circle, Rectangle
fig, (a,b) = plt.subplots(1,2,figsize=(5.2,2.5))
a.plot([0.4,5.6],[1.4,1.4],color=INK,lw=3)
for x in (1,2.2,3.4,4.6):
    a.plot([x,x],[1.4,0.9],color=INK,lw=1); a.add_patch(Rectangle((x-0.3,0.4),0.6,0.5,fc='#eef3fc',ec=ACCENT,lw=1.2)); a.text(x,0.65,'PC',ha='center',va='center',fontsize=7)
a.add_patch(Rectangle((0.2,1.25),0.2,0.3,fc=INK)); a.add_patch(Rectangle((5.6,1.25),0.2,0.3,fc=INK))
a.text(0.3,1.75,'terminator',fontsize=6.5); a.text(3.0,1.75,'backbone (single cable)',fontsize=7,ha='center')
a.set_xlim(0,6); a.set_ylim(0,2.2); a.set_aspect('equal'); a.axis('off')
b.add_patch(Circle((0,0),0.45,fc='#fdf1e6',ec=ACCENT,lw=1.4)); b.text(0,0,'Hub /\\nSwitch',ha='center',va='center',fontsize=6.5)
import numpy as np
for k in range(6):
    t=k*np.pi/3+0.5; x,y=1.4*np.cos(t),1.4*np.sin(t)
    b.plot([0.45*np.cos(t),x*0.85],[0.45*np.sin(t),y*0.85],color=INK,lw=1.2); b.add_patch(Rectangle((x-0.22,y-0.17),0.44,0.34,fc='#eef3fc',ec=ACCENT,lw=1.2)); b.text(x,y,'PC',ha='center',va='center',fontsize=6.5)
b.set_xlim(-2,2); b.set_ylim(-2,2); b.set_aspect('equal'); b.axis('off')
```

| Basis | Bus topology | Star topology |
|---|---|---|
| **Architectural layout** | All devices are connected to one common backbone cable by drop lines/taps, with terminators at both ends. | Every device has its own dedicated cable to a central hub or switch. |
| **Data transmission** | Data is broadcast on the single shared cable; every node sees it and only the addressed node accepts it. Needs CSMA/CD to handle collisions, and only one device can send at a time. | The hub/switch receives the frames and forwards them (hub: to all ports; switch: only to the destination port), so many pairs can communicate at the same time with very few collisions. |
| **Failure** | A break in the backbone splits the network; the whole network may fail. | Failure of a node or its cable affects only that node; only the failure of the central device stops the network. |
| **Fault finding** | Difficult; the fault must be traced along the cable. | Easy; the faulty link is found from the central device. |
| **Cost and cabling** | Cheap, needs the least cable and no central device. | Needs more cable and a hub/switch, so costs more. |
| **Expansion** | Difficult; performance falls as nodes are added. | Easy; a new node is just plugged into a free port. |
| **Performance and security** | Low, because the bandwidth is shared; any node can capture the data. | High, dedicated link to each node; the switch gives better security. |
| **Use today** | Obsolete (old 10BASE2 Ethernet). | The standard layout of modern LANs: offices, schools, home Wi-Fi routers (access point acts as the centre). |

**Conclusion.** The bus is simple and cheap but is unreliable and slow when it grows, so in modern computing environments the **star topology** with switches is used because of its reliability, easy management and high speed.

@s 16
```c
#include <stdio.h>

struct book {
    char title[50];
    char author[40];
    char publisher[40];
    float price;
};

int main() {
    struct book b[5];
    int i;

    for (i = 0; i < 5; i++) {
        printf("\nEnter details of book %d\n", i + 1);
        printf("Title: ");     scanf(" %[^\n]", b[i].title);
        printf("Author: ");    scanf(" %[^\n]", b[i].author);
        printf("Publisher: "); scanf(" %[^\n]", b[i].publisher);
        printf("Price: ");     scanf("%f", &b[i].price);
    }

    printf("\n%-5s %-25s %-20s %-20s %s\n", "S.N.", "Title", "Author", "Publisher", "Price");
    for (i = 0; i < 5; i++) {
        printf("%-5d %-25s %-20s %-20s %.2f\n", i + 1,
               b[i].title, b[i].author, b[i].publisher, b[i].price);
    }
    return 0;
}
```
**Explanation.**
1. `struct book` is a user-defined type grouping four members of different types: three character arrays (strings) and a `float` for the price.
2. `struct book b[5];` declares an *array of structures*, so five books can be stored and handled in a loop.
3. The first `for` loop reads the members of each book, using `%[^\n]` so that the strings can contain spaces (the space before `%` skips the leftover newline). The members are reached with the dot operator `b[i].title`.
4. The second loop prints a formatted table of all five books.

**Or. Binary file handling in C.** A **binary file** stores data in the same internal (machine) form as in memory, as a sequence of bytes, not as readable text. Compared with text files it is *faster* (there is no conversion between number and characters), *takes less space* (an `int` always uses 2/4 bytes) and is exact for numbers, but it cannot be read by a text editor. A binary file is opened with a binary mode: `"rb"` (read), `"wb"` (write), `"ab"` (append), `"rb+"`, `"wb+"`. The usual steps are: declare `FILE *fp;` → open with `fopen()` → read/write with a function → close with `fclose()`. The main binary I/O functions are `fread()`/`fwrite()` (blocks, such as structures) and `putw()`/`getw()` (integers).

**putw() and getw().**
- `putw(int w, FILE *fp)` writes one **integer** (in its binary form, the full `sizeof(int)` bytes) to the file, and returns the integer written, or EOF on error.
- `getw(FILE *fp)` reads the next **integer** from the file and returns it; at the end of the file or on error it returns EOF, so `feof(fp)` must be used to find the real end because EOF (−1) may also be a valid number.
These functions make binary I/O simple because no format string or conversion is needed, and the integers can be written and read back exactly as they are in memory.

*Example: write ten integers, then read them back.*
```c
#include <stdio.h>

int main() {
    FILE *fp;
    int i, n;

    fp = fopen("numbers.dat", "wb");     /* binary write */
    if (fp == NULL) { printf("Cannot open file\n"); return 1; }
    for (i = 1; i <= 10; i++)
        putw(i * i, fp);                 /* writes 1, 4, 9, ... 100 */
    fclose(fp);

    fp = fopen("numbers.dat", "rb");     /* binary read */
    if (fp == NULL) { printf("Cannot open file\n"); return 1; }
    while ((n = getw(fp)) != EOF) {
        if (feof(fp)) break;
        printf("%d ", n);                /* 1 4 9 16 25 36 49 64 81 100 */
    }
    fclose(fp);
    return 0;
}
```
The first part creates `numbers.dat` and stores the squares of 1 to 10 as binary integers by `putw()`; the second part reopens the file for reading and `getw()` brings them back one at a time until the end of file. For records such as structures, `fwrite(&rec, sizeof(rec), 1, fp)` and `fread()` are used in the same way.

---
file: NEBians-Past-Paper-Grade-12-Computer-Science-2082.pdf
subject: Computer Science
grade: 12
year_bs: 2082
year_ad: 2025
stream: Regular and Partial
code: 4281 'D'
time: 2 hrs
marks: 50
students: For regular and partial students whose first two digits of registration number start from 78, 79, 80 and 81
category: Board Exam
---
## Group 'A'
<small>Multiple choice questions · rewrite the correct option of each question in your answer sheet · [9×1=9]</small>

@mcq 1
Which of the following is the purpose of using a primary key in a database?
@opts-col To uniquely identify a record | To store duplicate record | To backup data | To enhance database size

@mcq 2
A company needs to modify an existing table by adding a new column for employee email addresses. For this, which SQL command should be used?
@opts CREATE | ALTER | SELECT | UPDATE

@mcq 3
Which protocol is used for secure communication over a computer network?
@opts HTTP | FTP | HTTPS | Telnet

@mcq 4
Which control structure in JS (JavaScript) is used to execute a block of code repeatedly based on a given condition?
@opts For loop | if-else | switch-case | function

@mcq 5
Select the invalid variable name in PHP.
@opts &#36;name | &#36;_name | &#36;1name | &#36;name123

@mcq 6
The statement `int number(int a);` is a …
@opts function call | function definition | function declaration | function execution

@mcq 7
In which of the following programming approaches is the emphasis given on data rather than on procedures?
@opts Procedural programming | Structural programming | Object-oriented programming | Declarative programming

@mcq 8
Which type of feasibility study evaluates whether a system can be developed with the available technology?
@opts Operational feasibility | Social feasibility | Technical feasibility | Economical feasibility

@mcq 9
Which of the following is NOT a type of cloud computing service?
@opts-col Infrastructure as a Service (IaaS) | Platform as a Service (PaaS) | Software as a Service (SaaS) | Hardware as a Service (HaaS)

## Group 'B'
<small>Short answer questions · [5×5=25]</small>

@q 10
Write any three differences between DDL and DML. Give examples of each. [[3+2]]
@or
What is normalization? Explain 2NF and 3NF. [[2+3]]

@q 11
Write JavaScript code to input any three numbers and find the smallest number among them. [[5]]
@or
Write a PHP script to connect to a MySQL database. [[5]]

@q 12
Write short notes on class and inheritance in OOP with example. [[5]]

@q 13
What is Requirement Gathering? Explain different Requirement Gathering methods. [[1+4]]

@q 14
What is AI? Explain application areas of AI in education. [[5]]

## Group 'C'
<small>Long answer questions · [2×8=16]</small>

@q 15
What is transmission medium? Explain its major types with advantages and disadvantages. [[2+6]]

@q 16
Write a C program that reads the account_number, name and address of ten customers from users and displays the account_number, name and address of these customers using array and structure. [[8]]
@or
What are the components of a function of C? Describe the call-by-value and call-by-reference and passing the function parameters. [[4+4]]

<!-- SOLUTIONS -->
### Group A — answer key

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Ans | A | B | C | A | C | C | C | C | D |

**1. A.** A primary key uniquely identifies each record (row) of a table and cannot be NULL or duplicated.

**2. B.** `ALTER TABLE employee ADD email VARCHAR(100);` changes the structure of an existing table. CREATE makes a new table, SELECT reads, UPDATE changes data in rows.

**3. C.** HTTPS is HTTP over SSL/TLS: the data is encrypted. HTTP, FTP and Telnet send data as plain text.

**4. A.** A loop (`for`, `while`, `do…while`) repeats a block while its condition holds. `if-else` and `switch-case` select a block once; a function is a named block.

**5. C.** A PHP variable name must start with `$` followed by a letter or underscore, never a digit. `$1name` is invalid.

**6. C.** `int number(int a);` ends with a semicolon and has no body: it is a function declaration (prototype).

**7. C.** In object-oriented programming, data and the functions that work on it are bound into objects; the data is given importance over procedure.

**8. C.** Technical feasibility checks whether the required hardware, software and technical skill are available to develop the system.

**9. D.** The cloud service models are IaaS, PaaS and SaaS. "Hardware as a Service" is not a standard model.

### Group B

@s 10
**Differences between DDL and DML**

| DDL (Data Definition Language) | DML (Data Manipulation Language) |
|---|---|
| Defines and changes the structure (schema) of database objects | Inserts, changes, deletes and retrieves the data in the tables |
| Commands: CREATE, ALTER, DROP, TRUNCATE | Commands: SELECT, INSERT, UPDATE, DELETE |
| Changes are auto-committed and cannot normally be rolled back | Changes can be rolled back before COMMIT |
| Affects the whole table or database | Affects rows (records) |

*Examples:* DDL: `CREATE TABLE student(id INT PRIMARY KEY, name VARCHAR(30));` DML: `INSERT INTO student VALUES(1,'Sita');`

**Or.** *Normalization* is the process of organising the data of a database into tables so that redundancy (repetition) and anomalies of insertion, deletion and update are removed, by splitting a large table into smaller related tables.
*2NF (second normal form):* the table is in 1NF (atomic values, no repeating groups) and every non-key attribute is fully functionally dependent on the whole primary key (no partial dependency). Example: Marks(student_id, subject_id, student_name, marks): `student_name` depends only on `student_id`; split it into Student(student_id, student_name) and Marks(student_id, subject_id, marks).
*3NF (third normal form):* the table is in 2NF and no non-key attribute depends on another non-key attribute (no transitive dependency). Example: Student(roll, name, zip, city): `city` depends on `zip`, which depends on `roll`; split into Student(roll, name, zip) and Zip(zip, city).

@s 11
```html
<script>
  var a = parseFloat(prompt("Enter first number"));
  var b = parseFloat(prompt("Enter second number"));
  var c = parseFloat(prompt("Enter third number"));
  var smallest = a;
  if (b < smallest) smallest = b;
  if (c < smallest) smallest = c;
  document.write("The smallest number is " + smallest);
</script>
```

**Or.**
```php
<?php
$servername = "localhost";
$username   = "root";
$password   = "";
$dbname     = "school";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
echo "Connected successfully";
mysqli_close($conn);
?>
```

@s 12
A **class** is a user-defined blueprint (template) that groups data members (attributes) and member functions (methods); an **object** is an instance of a class. **Inheritance** is the mechanism by which a new class (derived/child class) acquires the properties and methods of an existing class (base/parent class), which gives code reuse and a hierarchy of classes.
```cpp
#include <iostream>
using namespace std;

class Person {            // base class
public:
    string name;
    void show() { cout << "Name: " << name << endl; }
};

class Student : public Person {   // derived class
public:
    int roll;
    void display() { show(); cout << "Roll: " << roll << endl; }
};

int main() {
    Student s;
    s.name = "Ram";
    s.roll = 12;
    s.display();
    return 0;
}
```
Here `Student` inherits `name` and `show()` from `Person` and adds `roll`.

@s 13
*Requirement gathering* is the process of collecting, from users and stakeholders, what the new system must do (functional requirements) and the constraints it must meet (non-functional requirements), before design begins.
*Methods:*
- **Interview:** analysts ask questions face to face with users and managers; detailed and flexible but time-consuming.
- **Questionnaire (survey):** written questions given to many users; cheap and fast for large groups but replies are limited.
- **Observation:** the analyst watches users perform their work to see the real process.
- **Document review:** studying existing forms, reports, manuals and records.
- **Joint Application Development (JAD) / workshops:** users and developers meet together to agree on requirements.
- **Prototyping:** a working model is shown to users to draw out feedback.

@s 14
*Artificial intelligence (AI)* is the branch of computer science that builds machines and software able to perform tasks that normally need human intelligence, such as learning, reasoning, problem solving, understanding language and perception.
*Application in education:*
- **Personalised learning:** adaptive platforms adjust content and pace to each student.
- **Intelligent tutoring systems and chatbots:** answer questions and give hints at any time.
- **Automated grading:** objective tests, and in part written answers, are marked quickly and consistently.
- **Language and speech tools:** translation, speech-to-text, pronunciation practice.
- **Administration:** attendance, admission and timetable automation, and early warning for students at risk.
- **Accessibility:** text-to-speech and captioning for learners with disabilities.

### Group C

@s 15
*Transmission medium:* the physical path (or the space) through which data signals travel from a sender to a receiver in a network.

**Types**

**1. Guided (wired) media**

| Medium | Advantages | Disadvantages |
|---|---|---|
| Twisted pair (UTP/STP) | Cheap, easy to install, flexible | Short distance, noise and interference, low bandwidth |
| Coaxial cable | More bandwidth and better noise resistance than twisted pair, used for cable TV | Costlier and bulkier, signal loss over distance |
| Optical fibre | Very high bandwidth and speed, long distance, immune to electromagnetic interference, secure | Expensive, delicate, hard to install and repair |

**2. Unguided (wireless) media**

| Medium | Advantages | Disadvantages |
|---|---|---|
| Radio waves | Omnidirectional, pass through walls, no cabling | Interference, can be intercepted, limited security |
| Microwave | High data rate, no cables over long distance with towers | Line-of-sight needed, affected by weather |
| Satellite | Covers wide and remote areas | High cost, propagation delay |
| Infrared | Cheap, secure within a room | Very short range, blocked by walls |

@s 16
```c
#include <stdio.h>

struct customer {
    int  account_number;
    char name[30];
    char address[40];
};

int main() {
    struct customer c[10];
    int i;

    for (i = 0; i < 10; i++) {
        printf("Enter details of customer %d\n", i + 1);
        printf("Account number: ");
        scanf("%d", &c[i].account_number);
        printf("Name: ");
        scanf(" %[^\n]", c[i].name);
        printf("Address: ");
        scanf(" %[^\n]", c[i].address);
    }

    printf("\nAccount No.\tName\t\tAddress\n");
    for (i = 0; i < 10; i++) {
        printf("%d\t\t%s\t\t%s\n", c[i].account_number, c[i].name, c[i].address);
    }
    return 0;
}
```

**Or.** *Components of a C function:*
- **Function declaration (prototype):** tells the compiler the name, return type and parameters, e.g. `int add(int, int);`
- **Function definition:** the header (return type, name, parameter list) and the body (statements) that does the work.
- **Function call:** the statement that invokes it, e.g. `s = add(a, b);`
- **Return statement:** sends the result back to the caller.

*Call by value:* the values of the actual arguments are copied into the formal parameters; changes inside the function do not affect the originals.
```c
void swap(int x, int y) { int t = x; x = y; y = t; }   /* a and b unchanged */
/* call: swap(a, b); */
```
*Call by reference:* the addresses of the actual arguments are passed (pointers); the function works on the originals, so the changes are visible to the caller.
```c
void swap(int *x, int *y) { int t = *x; *x = *y; *y = t; }   /* a and b swapped */
/* call: swap(&a, &b); */
```
*Passing parameters:* arguments are matched with the formal parameters by position, number and type; arrays are passed by giving the base address of the array.

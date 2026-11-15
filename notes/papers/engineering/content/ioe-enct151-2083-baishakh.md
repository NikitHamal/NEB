---
file: NEBians-IOE-Past-Paper-Object-Oriented-Programming-ENCT151-2083-Baishakh.pdf
subject: Object Oriented Programming
level: BE · Year I / Part II
code: ENCT 151
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What are the advantages of object oriented programming? Differentiate between procedural oriented programming and object oriented programming. [[2+2]]

@q 2
When do we use default argument in functions? When can conflict occur when default argument and function overloading are used together? Create a C++ program to illustrate the concept of default arguments. Define a function named printMessage that takes two parameters: a message and a count. The function should print the string for count number of times. Set the default value of count to 1. [[1+2+4]]

@q 3
What do you mean by a constructor? Explain with example types of constructors in C++. Create a class person with data members name, age, address and citizenship_number. Define constructor to initialize the value of the person. Assign citizenship number if the age of the person is greater than 16 otherwise assign value zero to citizenship number. Also create a function to display the values. [[1+4+4]]

@q 4
Explain different ways of how binary operator overloading is performed? Using a class to model a 3×3 matrix, overload the + and - operator to add and subtract two matrices. [[3+4]]

@q 5
What is the difference between private and protected access specifier? Define function overriding. Write a program with a class to represent cricketer that has data members to represent name, age and number of matches played. From this class derive two classes bowler and batsman. The bowler class should have number of wickets as data member and batsman class should have number of runs and number of centuries as data members. Implement the concept of function overriding in your program and also mention the type of inheritance involved in the program. [[2+1+4]]

@q 6
Why do you need virtual destructor? Distinguish between function overloading and overriding with example. [[1+4]]

@q 7
Explain how abnormal situations are handled in I/O process. Write a program that writes text to source file after reading from the user. Copy the content from source file, change the case of letters to uppercase if they are in lowercase and then store in destination file. Also, display the content of destination file too. [[3+5]]

@q 8
Why are templates in C++ referred to as a form of generic programming? What are containers and iterators in STL? Briefly explain default arguments with Class Template with suitable example. [[2+2+4]]

@q 9
How is explain exception handling mechanism in C++ better than tradition techniques? Write a program to read name, roll number and marks that catches multiple exceptions using exception class if roll number is negative and marks greater than full marks. Also, handle the exceptions. [[2+3]]

<!-- SOLUTIONS -->

@s 1
**Benefits (advantages) of object oriented programming.**

1. **Reusability**: classes can be reused in other programs and extended through inheritance, which saves development time and removes redundant code.
2. **Data hiding and security**: the data is private to the object and is only accessible through member functions.
3. **Modularity and easy maintenance**: each class is a self-contained module, so errors are located and corrected locally.
4. **Natural modelling** of real-world problems with objects and the messages between them, which makes the design easy to understand.
5. **Extensibility**: new features are added by deriving classes or adding objects, without disturbing the existing code.
6. **Polymorphism** gives one interface with many implementations, so the code is flexible; and **abstraction** hides complexity.
7. It is suited to large projects (team work, upgradeable systems, and software libraries).


**Difference between procedural and object oriented programming.**

| Point | Procedural oriented programming (POP) | Object oriented programming (OOP) |
|---|---|---|
| Approach | **top-down**: the program is divided into functions (procedures) | **bottom-up**: the program is divided into objects (data and the functions that act on it) |
| Importance | priority is on the *function* (what is done) | priority is on the *data* (the object) |
| Data | data is global and shared by all functions, so it can be changed accidentally | data is hidden inside the object and is accessible only through its member functions (**encapsulation**) |
| Security | no data hiding, less secure | data hiding by access specifiers (private, protected, public) |
| Reuse | code is reused by copying or by calling functions | reuse by **inheritance**, templates and composition |
| Extension | changes in the data structure affect many functions | new classes are derived without changing the old |
| Polymorphism | not supported (only by different function names) | function and operator overloading, virtual functions |
| Examples | C, FORTRAN, Pascal, COBOL | C++, Java, C#, Python |


@s 2
**When default arguments are used.** A *default argument* is a value given to a function parameter in the declaration, which the compiler uses **when the caller omits that argument**. It is used when:

1. a function is usually called with the **same value** for one or more parameters (for example a count of 1, a precision, a default size or a default flag), so the call becomes shorter;
2. the **same function is to be called in several forms** without writing many overloaded versions;
3. new parameters are added to an existing function without changing the old calls.

Rules: the defaults are given **from right to left** (once a parameter has a default, all parameters to its right must have one), they are given **once**, in the declaration (prototype) or the definition but not both, and the omitted arguments must be the trailing ones.

**Conflict with function overloading.** When a function with default arguments is overloaded, a call may match **more than one function equally well**, and the compiler reports an **ambiguity** error. For example:

```cpp
void show(int a);
void show(int a, int b = 10);     // default argument

int main() {
    show(5);          // ERROR: ambiguous - matches show(int) and show(int, int = 10)
    show(5, 6);       // fine: only the second matches
}
```

The conflict is removed by deleting the default value or one overload, or by giving the overloads different parameter lists, and by not making the defaulted version overlap an existing overload.

**Program: `printMessage` with a default count of 1.**

```cpp
#include <iostream>
#include <string>
using namespace std;

void printMessage(const string &message, int count = 1) {   // default count = 1
    for (int i = 0; i < count; i++)
        cout << message << endl;
}

int main() {
    printMessage("Hello, IOE!", 3);   // count given: printed 3 times
    printMessage("Only once");        // count omitted: default 1
    return 0;
}
```

Output:

```
Hello, IOE!
Hello, IOE!
Hello, IOE!
Only once
```

@s 3
A **constructor** is a special member function that has the **same name as the class**, has **no return type** (not even `void`), and is **called automatically when an object is created**, to initialise its data members. It can be overloaded, can have default arguments, and must be declared in the `public` section to be called from outside. A destructor `~ClassName()` does the opposite and is called when the object is destroyed.

**Types of constructors in C++.**

| Type | Syntax | Purpose |
|---|---|---|
| **Default constructor** | `Box() { l = 0; }` | takes no arguments (or all with defaults); the compiler generates one if none is written |
| **Parameterised constructor** | `Box(int x, int y) { l = x; b = y; }` | initialises the object with given values: `Box b1(3, 4);` |
| **Copy constructor** | `Box(const Box &o) { l = o.l; b = o.b; }` | makes a new object as a copy of an existing one: `Box b2(b1);` or `Box b2 = b1;` |
| **Constructor with default arguments** | `Box(int x = 1, int y = 1)` | one constructor for several call forms |
| **Dynamic constructor** | `Name(const char *s) { p = new char[strlen(s)+1]; strcpy(p, s); }` | allocates memory with `new` at object creation |

```cpp
#include <iostream>
using namespace std;

class Box {
    int l, b;
public:
    Box() : l(0), b(0) { cout << "default\n"; }
    Box(int x, int y) : l(x), b(y) { cout << "parameterised\n"; }
    Box(const Box &o) : l(o.l), b(o.b) { cout << "copy\n"; }
    int area() const { return l * b; }
};

int main() {
    Box b1;            // default
    Box b2(3, 4);      // parameterised
    Box b3(b2);        // copy
    cout << b3.area() << endl;   // 12
}
```


**Class `person`.** The constructor assigns the citizenship number only when the age is greater than 16 (a citizen can hold a citizenship certificate from 16), and otherwise stores 0.

```cpp
#include <iostream>
#include <string>
using namespace std;

class person {
    string name;
    int age;
    string address;
    long citizenship_number;
public:
    person(string n, int a, string ad, long cn) {
        name = n;
        age = a;
        address = ad;
        if (age > 16) citizenship_number = cn;   // eligible
        else          citizenship_number = 0;    // minor
    }
    void display() const {
        cout << "Name: " << name << "\nAge: " << age
             << "\nAddress: " << address
             << "\nCitizenship number: " << citizenship_number << "\n\n";
    }
};

int main() {
    person p1("Ram Sharma", 25, "Kathmandu", 12345678L);
    person p2("Sita Karki", 14, "Pokhara", 87654321L);   // age <= 16, so number becomes 0
    p1.display();
    p2.display();
    return 0;
}
```

Output: Ram's citizenship number is shown as 12345678 and Sita's as 0.

@s 4
**Ways of performing binary operator overloading.** A binary operator (`+`, `-`, `*`, `/`, `==`, `<` and so on) has two operands. It is overloaded by writing a function named `operator@` in one of three ways:

1. **As a member function.** The left operand is the invoking object and the right operand is the single argument: `Matrix operator+(const Matrix &m);`, called as `a + b`, i.e. `a.operator+(b)`. The left operand must be an object of the class.
2. **As a friend function (a non-member with access to the private data).** Both operands are arguments: `friend Matrix operator+(const Matrix &a, const Matrix &b);`. It is needed when the left operand is *not* an object of the class (for example `5 + obj`) or for `<<` and `>>`.
3. **As an ordinary non-member function** using only the public interface of the class (getters and setters): `Matrix operator+(const Matrix &a, const Matrix &b)`.

**3×3 matrix with + and − overloaded (member functions).**

```cpp
#include <iostream>
using namespace std;

class Matrix {
    int m[3][3];
public:
    void input() {
        cout << "Enter 9 elements row-wise:\n";
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) cin >> m[i][j];
    }
    void display() const {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) cout << m[i][j] << "\t";
            cout << "\n";
        }
    }
    Matrix operator+(const Matrix &b) const {          // a + b
        Matrix r;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) r.m[i][j] = m[i][j] + b.m[i][j];
        return r;
    }
    Matrix operator-(const Matrix &b) const {          // a - b
        Matrix r;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) r.m[i][j] = m[i][j] - b.m[i][j];
        return r;
    }
};

int main() {
    Matrix a, b;
    cout << "Matrix A\n"; a.input();
    cout << "Matrix B\n"; b.input();
    Matrix s = a + b, d = a - b;
    cout << "A + B =\n"; s.display();
    cout << "A - B =\n"; d.display();
    return 0;
}
```

*Example:* for A = [[1,2,3],[4,5,6],[7,8,9]] and B = the identity matrix, A + B has diagonal 2, 6, 10 and A − B has diagonal 0, 4, 8, and the off-diagonal elements are unchanged.

@s 5
**Private and protected access specifiers.**

| Point | `private` | `protected` |
|---|---|---|
| Access inside the class | yes | yes |
| Access from a **derived class** | **no** | **yes** |
| Access from outside (objects, other functions) | no | no |
| Purpose | strongest hiding of the internal data of the class | data hidden from the outside but available to child classes |
| Default | default for a class | has to be written |

(Friend functions and friend classes can access both.)

**Function overriding** means that a **derived class defines a function with the same name, same parameters and same return type as a function of its base class**, so that the derived version *replaces* (hides) the base version for objects of the derived class. With a `virtual` base function it is resolved at run time (run-time polymorphism); without, by the type of the object name.

```cpp
#include <iostream>
#include <string>
using namespace std;

class Cricketer {
protected:
    string name;
    int age, matches;
public:
    Cricketer(string n, int a, int m) : name(n), age(a), matches(m) {}
    virtual void display() const {
        cout << "Name: " << name << ", Age: " << age << ", Matches: " << matches << "\n";
    }
    virtual ~Cricketer() {}
};

class Bowler : public Cricketer {
    int wickets;
public:
    Bowler(string n, int a, int m, int w) : Cricketer(n, a, m), wickets(w) {}
    void display() const override {                       // overrides Cricketer::display
        Cricketer::display();
        cout << "Role: Bowler, Wickets: " << wickets << "\n\n";
    }
};

class Batsman : public Cricketer {
    int runs, centuries;
public:
    Batsman(string n, int a, int m, int r, int c) : Cricketer(n, a, m), runs(r), centuries(c) {}
    void display() const override {                       // overrides Cricketer::display
        Cricketer::display();
        cout << "Role: Batsman, Runs: " << runs << ", Centuries: " << centuries << "\n\n";
    }
};

int main() {
    Bowler b("Sandeep Lamichhane", 24, 60, 110);
    Batsman t("Rohit Paudel", 22, 45, 1850, 3);
    Cricketer *list[2] = { &b, &t };
    for (int i = 0; i < 2; i++) list[i]->display();       // the derived version is called
    return 0;
}
```

**Type of inheritance:** this is **hierarchical inheritance** (two classes, `Bowler` and `Batsman`, are derived from the one base class `Cricketer`), and each derivation is **single, public inheritance**.

@s 6
**Need for a virtual destructor.** When a derived class object is created with `new` and **deleted through a pointer to the base class** (`Base *p = new Derived; delete p;`), the call `delete p` runs only the **base destructor** if the destructor is not virtual. This is *undefined behaviour*: the derived part (its dynamically allocated memory, file handles and so on) is not destroyed, giving **memory leaks**. If the base destructor is declared `virtual`, the destructor of the actual (derived) object is called first, then the base destructor, in the correct order.

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    virtual ~Base() { cout << "Base destroyed\n"; }      // without 'virtual', Derived's destructor is skipped
};
class Derived : public Base {
    int *data;
public:
    Derived() : data(new int[100]) {}
    ~Derived() { delete[] data; cout << "Derived destroyed\n"; }
};

int main() {
    Base *p = new Derived;
    delete p;        // prints: Derived destroyed, Base destroyed
}
```

**Function overloading and function overriding.**

| Point | Overloading | Overriding |
|---|---|---|
| Meaning | several functions with the **same name but different parameter lists** (number, type or order) in the same scope | the derived class redefines a base-class function with the **same signature** |
| Scope | within one class (or one scope) | between a base class and a derived class |
| Return type | may differ (not used for selection) | must be the same (or covariant) |
| Binding | compile time (early, static polymorphism) | run time with `virtual` (dynamic polymorphism) |
| `virtual` keyword | not needed | needed for run-time selection |
| Example | `int add(int,int); double add(double,double);` | `Base::show()` and `Derived::show()` |

```cpp
#include <iostream>
using namespace std;

class Shape {
public:
    int area(int s)          { return s * s; }               // overloading: same name, different parameters
    int area(int l, int b)   { return l * b; }
    virtual void show()      { cout << "Shape\n"; }
};
class Circle : public Shape {
public:
    void show() override     { cout << "Circle\n"; }         // overriding: same signature
};

int main() {
    Shape s;  Circle c;  Shape *p = &c;
    cout << s.area(4) << " " << s.area(3, 5) << endl;        // 16 15
    p->show();                                               // Circle
}
```

@s 7
**Handling abnormal situations in I/O.** Errors during file and stream operations (the file does not exist, a disk or read error, an attempt to read past the end, wrong data type) are detected from the **stream state flags**, which are held by the stream object and tested with member functions (or by testing the stream itself):

| Function | True when |
|---|---|
| `good()` | no error, the next operation can succeed |
| `eof()` | the end of the file has been reached |
| `fail()` | a logical error occurred (a format error, or the file could not be opened); recoverable |
| `bad()` | a serious, non-recoverable error (hardware error, loss of data) |
| `clear()` | resets the flags (after handling the error) |
| `!file` or `file.is_open()` | the open failed |

Typical handling: **test the stream after `open()`** (`if (!fin) { cerr << "cannot open"; return 1; }`), loop on the read (`while (fin.get(ch))` or `while (getline(fin, line))`) so that EOF ends the loop, use `fail()` after an input to detect a bad format, `clear()` and `ignore()` to recover, and close the files at the end. C++ streams can also be made to throw exceptions with `exceptions(ios::failbit | ios::badbit)`.

**Program.**

```cpp
#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    // 1. read text from the user and write it to the source file
    ofstream src("source.txt");
    if (!src) { cerr << "Cannot create source.txt\n"; return 1; }
    string line;
    cout << "Enter text (empty line to stop):\n";
    while (getline(cin, line) && !line.empty())
        src << line << '\n';
    src.close();

    // 2. copy from source to destination, converting lower case to upper case
    ifstream in("source.txt");
    ofstream out("destination.txt");
    if (!in || !out) { cerr << "File error\n"; return 1; }
    char ch;
    while (in.get(ch)) {
        if (islower(static_cast<unsigned char>(ch))) ch = toupper(ch);
        out.put(ch);
    }
    in.close();
    out.close();

    // 3. display the destination file
    ifstream dest("destination.txt");
    if (!dest) { cerr << "Cannot open destination.txt\n"; return 1; }
    cout << "\nContent of destination.txt:\n";
    while (dest.get(ch)) cout << ch;
    dest.close();
    return 0;
}
```

For the input `Nepal is Beautiful` the destination file contains `NEPAL IS BEAUTIFUL`.

@s 8
**Templates and generic programming.**

A **template** lets one function or class definition work with **any data type**; the compiler generates the type-specific code (instantiation) at compile time. This is **generic programming**: the algorithm is written once, independent of the data type, so it removes the redundancy of writing the same code for `int`, `float`, `double`, and so on, is type safe, and (unlike a macro) is type checked.

```cpp
#include <iostream>
using namespace std;

template <class T>
T maxOf(T a, T b) { return (a > b) ? a : b; }          // function template

template <class T>
class Pair {                                           // class template
    T x, y;
public:
    Pair(T a, T b) : x(a), y(b) {}
    T larger() const { return maxOf(x, y); }
};

int main() {
    cout << maxOf(3, 9) << " " << maxOf(2.5, 1.5) << " " << maxOf('a', 'z') << endl;   // 9 2.5 z
    Pair<int> p(4, 7);  Pair<double> q(1.5, 0.5);
    cout << p.larger() << " " << q.larger() << endl;                                    // 7 1.5
}
```


**Containers and iterators in the STL.** The Standard Template Library has three main parts: containers, algorithms and iterators.

- **Containers** are **template classes that hold collections of objects** and manage their storage. *Sequence containers*: `vector`, `list`, `deque`, `array`; *associative containers* (sorted): `set`, `multiset`, `map`, `multimap`; *unordered* containers: `unordered_set`, `unordered_map`; *container adapters*: `stack`, `queue`, `priority_queue`.
- **Iterators** are **pointer-like objects that point to an element of a container and move through it**: `*it` gives the element, `++it` moves to the next, and `begin()` and `end()` give the first element and one past the last. They connect the containers with the algorithms (`sort`, `find`, `copy`) so that the same algorithm works on any container. Types: input, output, forward, bidirectional and random-access iterators.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> v = {5, 2, 9, 1};              // container
    sort(v.begin(), v.end());                  // algorithm using iterators
    for (vector<int>::iterator it = v.begin(); it != v.end(); ++it)
        cout << *it << " ";                    // 1 2 5 9
}
```

**Default arguments with a class template.** A template parameter may be given a default type (or a default value for a non-type parameter), used when the user does not supply it, as with function default arguments. The defaults are given from right to left.

```cpp
#include <iostream>
using namespace std;

template <class T = int, int SIZE = 5>          // default type int, default size 5
class Stack {
    T data[SIZE];
    int top = -1;
public:
    void push(T x) { if (top < SIZE - 1) data[++top] = x; else cout << "overflow\n"; }
    T pop()        { return (top >= 0) ? data[top--] : T(); }
    bool empty() const { return top == -1; }
};

int main() {
    Stack<> a;                  // Stack<int, 5>  (both defaults used)
    Stack<double> b;            // Stack<double, 5>
    Stack<char, 3> c;           // Stack<char, 3>
    a.push(10); a.push(20);
    b.push(1.5);
    c.push('x');
    cout << a.pop() << " " << b.pop() << " " << c.pop() << endl;   // 20 1.5 x
}
```

@s 9
An **exception** is a run-time error or abnormal condition (division by zero, array index out of range, invalid input, memory exhaustion, file not found) that interrupts normal execution. C++ handles it with three keywords:

| Keyword | Role |
|---|---|
| `try` | block of statements in which an exception may occur |
| `throw` | raises (throws) an exception object of some type when the error is detected |
| `catch` | handler that receives the exception of a matching type; there may be several, and `catch(...)` catches any type |

*Flow:* the code in the `try` block runs; when `throw` executes, control leaves the block (the stack is unwound and local objects are destroyed) and goes to the first `catch` whose parameter type matches; if there is none, `terminate()` is called. After the handler, execution continues after the last `catch`.

**Better than the traditional techniques** (checking return values or error flags, `exit()`, `assert`): the error-handling code is **separated** from the normal logic; the error cannot be ignored (an unhandled exception stops the program); it can carry **detailed information** in an object; it travels up through **several function levels** without checking at every level; it is **type-safe** and the objects are destroyed correctly (RAII).

```cpp
#include <iostream>
using namespace std;

double divide(double a, double b) {
    if (b == 0) throw "division by zero";      // throw a string literal
    return a / b;
}

int main() {
    try {
        cout << divide(10, 2) << endl;          // 5
        cout << divide(1, 0) << endl;           // throws
    }
    catch (const char *msg) { cout << "Error: " << msg << endl; }
    catch (...)             { cout << "unknown\n"; }
}
```


**Program: user defined exception classes (roll number negative, marks above full marks).** The full marks are taken as 100.

```cpp
#include <iostream>
#include <string>
using namespace std;

class NegativeRoll {                       // exception class 1
public:
    int roll;
    NegativeRoll(int r) : roll(r) {}
    void show() const { cout << "Exception: roll number " << roll << " cannot be negative.\n"; }
};

class MarksExceeded {                      // exception class 2
public:
    double marks, full;
    MarksExceeded(double m, double f) : marks(m), full(f) {}
    void show() const { cout << "Exception: marks " << marks << " exceed full marks " << full << ".\n"; }
};

int main() {
    const double FULL = 100;
    string name;
    int roll;
    double marks;
    try {
        cout << "Enter name, roll number and marks: ";
        cin >> name >> roll >> marks;
        if (roll < 0)      throw NegativeRoll(roll);
        if (marks > FULL)  throw MarksExceeded(marks, FULL);
        cout << "Name: " << name << ", Roll: " << roll << ", Marks: " << marks << endl;
    }
    catch (const NegativeRoll &e)  { e.show(); }
    catch (const MarksExceeded &e) { e.show(); }
    catch (...)                    { cout << "Unknown exception\n"; }
    cout << "Program continues after handling.\n";
    return 0;
}
```

Sample runs: `Hari -5 80` gives the roll number exception, `Hari 5 120` gives the marks exception, and `Hari 5 80` prints the record.

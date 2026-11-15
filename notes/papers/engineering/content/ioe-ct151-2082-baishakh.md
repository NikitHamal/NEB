---
file: NEBians-IOE-Past-Paper-Object-Oriented-Programming-CT151-2082-Baishakh.pdf
subject: Object Oriented Programming
level: BE · Year I / Part II
code: CT 151
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BCT, BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Compare procedure oriented programming and object-oriented programming. Explain the basic concept of object oriented programming. [[2+2]]

@q 2
When should you prefer the use of inline function? Explain with example. Explain function overloading in object-oriented programming. [[3+4]]

@q 3
Write about different types constructors with respective syntaxes. In which condition can a class be made friend? WAP to create a class information to store the name and address of students. Store the information of two students and swap the values of these objects. [[3+2+4]]

@q 4
What are the rules for operator overloading? Write a program to create a class "time" with data members – hour, minute and seconds and then overload post increment operator for increment in seconds. [[2+5]]

@q 5
Define inheritance in OOP. Give a suitable example to show how function overriding differ from function overloading? Write a program to show constructor invocation order in multilevel inheritance. [[1+3+3]]

@q 6
What is virtual function? Define pure virtual function with suitable example. [[1+4]]

@q 7
How random access of data in file can be handled? Write a program to store name, roll_no, address and batch of 'n' students in a file. Also add a feature to search the student information by roll_no. [[2+6]]

@q 8
"Templates in C++ enable generic programming, allowing the creation of reusable functions and classes that work with different data types within a single framework". Give example to justify the given statement. [[4+4]]

@q 9
What are exceptions in a program? Write a meaningful program that can handle multiple exceptions. [[1+4]]

<!-- SOLUTIONS -->

@s 1
**Comparison of procedure oriented programming (POP) and object oriented programming (OOP).**

| Point | Procedure oriented (C, Pascal) | Object oriented (C++, Java) |
|---|---|---|
| Basic unit | the **function** (procedure); the program is a list of instructions | the **object** (data + functions together) |
| Approach | **top-down**: the problem is divided into functions | **bottom-up**: classes and objects are designed first |
| Data | data is **global** and shared by many functions, with little protection | data is **hidden** inside objects and changed only through member functions |
| Security | no data hiding; any function may change the data | data hiding by `private` and `protected` |
| Reuse | by copying or calling functions | by **inheritance**, templates and composition |
| Real world modelling | poor | natural: real entities become objects |
| Polymorphism | not supported (only by function pointers) | function and operator overloading, virtual functions |
| Maintenance | a change of the data structure affects many functions | changes are local to the class |
| Example | `printf("%d", x)` with a global `x` | `obj.display()` |

**Basic concepts of object oriented programming.**

1. **Object**: a run-time entity that has *state* (data members) and *behaviour* (member functions), e.g. a particular student or bank account.
2. **Class**: a user-defined data type, the blueprint from which objects are created. An object is a variable of a class.
3. **Data abstraction**: showing only the essential features (the interface) and hiding the implementation details.
4. **Encapsulation**: wrapping data and the functions that operate on it into a single unit (the class). Together with access specifiers, it gives **data hiding**.
5. **Inheritance**: a new (derived) class acquires the properties of an existing (base) class; it gives **reusability** and a hierarchy of classes.
6. **Polymorphism**: one name, many forms: compile-time (function and operator overloading) and run-time (virtual functions).
7. **Dynamic binding**: the code executed for a function call is decided at run time.
8. **Message passing**: objects communicate by calling each other's member functions, `object.function(arguments)`.

@s 2
**Inline function.** A function declared with the keyword `inline` asks the compiler to **replace each call by the body of the function** (inline expansion), which removes the call overhead (pushing the arguments, jumping, returning).

**When to prefer an inline function.**

1. For **small, short functions** (one to three statements) such as getters, setters, `square()`, `max()`, which are **called many times**, especially inside loops.
2. When **speed matters more than code size**, since the call overhead is comparable with the work done by the function.
3. As a **type-safe replacement for the `#define` macro** with arguments (no side-effect problems such as `SQUARE(i++)`).

**Do not use it** for large functions, functions with loops, `switch` or `goto`, recursive functions, or functions whose address is taken (the compiler may then ignore the request). Disadvantage: the code size increases (code bloat).

```cpp
#include <iostream>
using namespace std;

inline int square(int x) { return x * x; }          // short function, expanded at each call
inline double maxOf(double a, double b) { return a > b ? a : b; }

int main() {
    for (int i = 1; i <= 5; i++)
        cout << square(i) << " ";                    // 1 4 9 16 25
    cout << "\nmax = " << maxOf(3.5, 2.1) << endl;   // 3.5
    return 0;
}
```

**Function overloading.** It is the feature of C++ by which **several functions with the same name but different parameter lists** (different number, types or order of arguments) are defined in the same scope. The compiler selects the right one at **compile time** from the arguments of the call (compile-time or static polymorphism). The return type alone is not sufficient to distinguish overloaded functions.

```cpp
#include <iostream>
using namespace std;

int    area(int s)            { return s * s; }               // square
int    area(int l, int b)     { return l * b; }               // rectangle
double area(double r)         { return 3.14159 * r * r; }     // circle
double area(double b, double h, char) { return 0.5 * b * h; } // triangle (extra dummy parameter)

int main() {
    cout << area(4) << endl;               // 16     (int)
    cout << area(4, 5) << endl;            // 20     (int, int)
    cout << area(2.0) << endl;             // 12.5664 (double)
    cout << area(6.0, 3.0, 't') << endl;   // 9
    return 0;
}
```

Overloading gives one meaningful name for one operation (`area`) with different data, so the program is easy to read and remember.

@s 3
**Constructor.** A constructor is a special member function with the **same name as the class and no return type** (not even `void`). It is called **automatically** when an object is created and initialises the data members. It is normally public and may be overloaded.

| Type | Syntax | Remark |
|---|---|---|
| **Default constructor** | `ClassName() { ... }` | takes no argument (or all arguments have defaults); the compiler supplies one if no constructor is written |
| **Parameterised constructor** | `ClassName(int a, float b) { ... }` | takes arguments; called as `ClassName obj(5, 2.5);` |
| **Copy constructor** | `ClassName(const ClassName &obj) { ... }` | initialises an object from another object of the same class: `ClassName b(a);` or `ClassName b = a;`; it is called when an object is passed or returned by value |
| **Constructor overloading** | several of the above in one class | selected by the arguments |
| **Constructor with initialiser list** | `ClassName(int a) : x(a) { }` | initialises members before the body runs |

```cpp
class Point {
    int x, y;
public:
    Point() : x(0), y(0) {}                       // default
    Point(int a, int b) : x(a), y(b) {}           // parameterised
    Point(const Point &p) : x(p.x), y(p.y) {}     // copy
};
```

**Condition for friendship.** A class can be made a friend of another class when it **needs direct access to the private and protected members** of that class, although it is not derived from it (for example two closely cooperating classes such as `Matrix` and `Vector`, or `LinkedList` and `Node`). The class that owns the private data **grants** friendship by the declaration `friend class B;`. Friendship is **not mutual, not inherited and not transitive**. In this program, the swap is done by a friend function.

**Program: class `information` for name and address of students; two students are stored and their values are swapped.** A `friend` function takes both objects by reference and exchanges them (the swapping of whole objects is done member by member).

```cpp
#include <iostream>
#include <string>
using namespace std;

class information {
    string name, address;
public:
    information() {}
    information(string n, string a) : name(n), address(a) {}
    void input() {
        cout << "Name: ";    getline(cin, name);
        cout << "Address: "; getline(cin, address);
    }
    void display() const { cout << name << ", " << address << endl; }
    friend void swapInfo(information &a, information &b);     // friend function
};

void swapInfo(information &a, information &b) {
    information temp = a;      // copy of the whole object
    a = b;
    b = temp;
}

int main() {
    information s1("Ram Thapa", "Kathmandu"), s2("Sita Rai", "Dharan");
    cout << "Before swapping:\n"; s1.display(); s2.display();
    swapInfo(s1, s2);
    cout << "After swapping:\n";  s1.display(); s2.display();
    return 0;
}
```

Output:

```
Before swapping:
Ram Thapa, Kathmandu
Sita Rai, Dharan
After swapping:
Sita Rai, Dharan
Ram Thapa, Kathmandu
```

(To read the data from the keyboard use `s1.input(); s2.input();` instead of the constructors.)

@s 4
**Rules for operator overloading.**

1. Only **existing operators** can be overloaded; new operators cannot be created (for example `**`).
2. The operators **`::` (scope), `.` (member access), `.*` (pointer to member), `?:` (conditional) and `sizeof`** cannot be overloaded.
3. At least one operand must be an object of a **user-defined type**; the meaning of an operator for built-in types cannot be changed.
4. The **number of operands (arity)**, the **precedence** and the **associativity** of the operator cannot be changed.
5. The operators `=`, `[]`, `()` and `->` must be overloaded as **member functions**; `<<` and `>>` for streams must be non-member (friend) functions.
6. A **unary** operator overloaded as a member takes no explicit argument; a **binary** operator overloaded as a member takes one argument (the right operand), the left one being the calling object. As a friend, a unary operator takes one and a binary operator two arguments.
7. For the **post-increment** `obj++` the member function has a dummy `int` parameter, `operator++(int)`; the pre-increment is `operator++()`.
8. Overloaded operators should behave in a way natural for the operator (they do not change the meaning of the other operators automatically, e.g. `+` does not give `+=`).

**Program: class `time` with post-increment on the seconds.** One second is added; 60 seconds carry into the minute, 60 minutes into the hour and 24 hours wrap to 0. (The class is named `time` as in the question; to avoid a clash with `time()` from `<ctime>`, it is spelled `Time` here.)

```cpp
#include <iostream>
using namespace std;

class Time {
    int hour, minute, second;
public:
    Time(int h = 0, int m = 0, int s = 0) : hour(h), minute(m), second(s) {}
    Time operator++(int) {               // post-increment: returns the OLD value
        Time old = *this;
        second++;
        if (second == 60) {              // carry
            second = 0; minute++;
            if (minute == 60) {
                minute = 0; hour++;
                if (hour == 24) hour = 0;
            }
        }
        return old;
    }
    void display() const {
        cout << (hour < 10 ? "0" : "") << hour << ":"
             << (minute < 10 ? "0" : "") << minute << ":"
             << (second < 10 ? "0" : "") << second << endl;
    }
};

int main() {
    Time t(10, 59, 58), r;
    r = t++;                                   // r gets the old value
    cout << "old: "; r.display();              // 10:59:58
    cout << "new: "; t.display();              // 10:59:59
    t++;
    cout << "after another ++: "; t.display(); // 11:00:00
    Time m(23, 59, 59);
    m++;
    cout << "midnight: "; m.display();         // 00:00:00
    return 0;
}
```

@s 5
**Inheritance** is the mechanism by which a **derived class acquires the data members and member functions of an existing base class**, so that existing code is reused and an "is-a" hierarchy is formed. Syntax: `class Derived : public Base { ... };`

**Function overriding versus function overloading.**

| Point | Function overloading | Function overriding |
|---|---|---|
| Meaning | same name, **different parameter lists**, in the **same class** | same name and **same signature**, in the **base and the derived class** |
| Needs inheritance | no | yes |
| Binding | compile time (static) | run time if the base function is `virtual` (otherwise compile time) |
| Purpose | one operation on different kinds of data | the derived class gives its **own version** of an inherited behaviour |
| `virtual` | not used | used for run-time polymorphism |

```cpp
#include <iostream>
using namespace std;

class Shape {
public:
    virtual void draw() { cout << "Shape::draw\n"; }
    void print(int x)    { cout << "int " << x << endl; }      // overloaded pair
    void print(double x) { cout << "double " << x << endl; }   // (same class, different types)
};
class Circle : public Shape {
public:
    void draw() override { cout << "Circle::draw\n"; }         // overriding (same signature)
};

int main() {
    Shape s;  Circle c;  Shape *p = &c;
    s.print(3); s.print(2.5);          // overloading: chosen by the argument type
    s.draw();                          // Shape::draw
    p->draw();                         // Circle::draw (overriding, run-time decision)
}
```

**Program: order of constructor (and destructor) invocation in multilevel inheritance** (`A` → `B` → `C`). Constructors run from the **base to the derived** class, destructors in the reverse order.

```cpp
#include <iostream>
using namespace std;

class A {
public:
    A()  { cout << "Constructor of A (grandparent)\n"; }
    ~A() { cout << "Destructor of A\n"; }
};
class B : public A {
public:
    B()  { cout << "Constructor of B (parent)\n"; }
    ~B() { cout << "Destructor of B\n"; }
};
class C : public B {
public:
    C()  { cout << "Constructor of C (child)\n"; }
    ~C() { cout << "Destructor of C\n"; }
};

int main() {
    C obj;                       // A(), then B(), then C()
    cout << "Object created\n";
    return 0;                    // ~C(), ~B(), ~A()
}
```

Output:

```
Constructor of A (grandparent)
Constructor of B (parent)
Constructor of C (child)
Object created
Destructor of C
Destructor of B
Destructor of A
```

The base class part of an object must exist before the derived part is built, so the order is always base first; the destruction is in the opposite order.

@s 6
**Virtual function.** A **virtual function** is a member function of a base class declared with the keyword `virtual`, which is expected to be **redefined (overridden) in the derived classes**. When it is called through a **base class pointer or reference**, the version of the **actual object** is executed (decided at run time, **dynamic binding**; implemented with the vtable). This gives run-time polymorphism.

**Pure virtual function.** A virtual function that has **no definition in the base class** and is declared with `= 0`:

```
virtual ReturnType functionName(parameters) = 0;
```

A class with one or more pure virtual functions is an **abstract class**: no object of it can be created, but pointers and references to it can. A derived class must **override** every pure virtual function; otherwise it is abstract as well. It defines an interface that all derived classes must supply.

```cpp
#include <iostream>
using namespace std;

class Shape {                               // abstract class
public:
    virtual double area() const = 0;        // pure virtual function
    virtual void   name() const { cout << "Shape\n"; }   // ordinary virtual function
    virtual ~Shape() {}
};

class Rectangle : public Shape {
    double l, b;
public:
    Rectangle(double l, double b) : l(l), b(b) {}
    double area() const override { return l * b; }
    void name() const override { cout << "Rectangle\n"; }
};

class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }
    void name() const override { cout << "Circle\n"; }
};

int main() {
    // Shape s;                              // error: cannot create an object of an abstract class
    Shape *p[2] = { new Rectangle(4, 5), new Circle(2) };
    for (int i = 0; i < 2; i++) {
        p[i]->name();
        cout << "Area = " << p[i]->area() << endl;   // 20, then 12.5664
        delete p[i];
    }
    return 0;
}
```

@s 7
**Random access of data in a file.** A file normally is read sequentially, but a **file pointer** can be moved to any byte position, which gives **random access**. Each stream has two pointers: the **get pointer** (for reading, `ifstream`) and the **put pointer** (for writing, `ofstream`); an `fstream` has both.

| Function | Use |
|---|---|
| `seekg(offset, dir)` | move the **get** pointer; `dir` is `ios::beg`, `ios::cur` or `ios::end` |
| `seekp(offset, dir)` | move the **put** pointer |
| `tellg()` / `tellp()` | return the current position of the get / put pointer |

With fixed-size records written by `write()`, the record number `k` (counted from 0) starts at byte `k * sizeof(record)`, so `file.seekg(k * sizeof(rec), ios::beg);` followed by `file.read(...)` gets the record directly, and `seekp` followed by `write` updates it in place. The number of records is `(file size) / sizeof(rec)`, with the file size got by `seekg(0, ios::end); tellg();`.

**Program.** The records of `n` students (name, roll number, address, batch) are stored as fixed-size binary records, and the student is then searched by `roll_no`: the file pointer is moved record by record with `seekg()` (binary random access) and the record found is displayed.

```cpp
#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;

class Student {
    char name[30];
    int  roll_no;
    char address[30];
    int  batch;
public:
    void input() {
        cout << "Name: ";    cin >> name;
        cout << "Roll no: "; cin >> roll_no;
        cout << "Address: "; cin >> address;
        cout << "Batch: ";   cin >> batch;
    }
    void display() const {
        cout << "Name: " << name << "\nRoll no: " << roll_no
             << "\nAddress: " << address << "\nBatch: " << batch << endl;
    }
    int getRoll() const { return roll_no; }
};

int main() {
    int n;
    cout << "How many students? ";
    cin >> n;

    // 1. store the n students in a file
    ofstream fout("students.dat", ios::binary);
    Student s;
    for (int i = 0; i < n; i++) {
        cout << "Student " << i + 1 << ":\n";
        s.input();
        fout.write(reinterpret_cast<char *>(&s), sizeof(s));
    }
    fout.close();

    // 2. search by roll_no with random access (seekg)
    ifstream fin("students.dat", ios::binary);
    fin.seekg(0, ios::end);
    int records = fin.tellg() / sizeof(Student);          // number of records in the file
    int key;
    cout << "Enter the roll_no to search: ";
    cin >> key;
    bool found = false;
    for (int k = 0; k < records && !found; k++) {
        fin.seekg(k * sizeof(Student), ios::beg);          // jump straight to record k
        fin.read(reinterpret_cast<char *>(&s), sizeof(s));
        if (s.getRoll() == key) {
            cout << "Record found (record no. " << k + 1 << "):\n";
            s.display();
            found = true;
        }
    }
    if (!found) cout << "No student with roll_no " << key << endl;
    fin.close();
    return 0;
}
```

Sample run with `n = 2`, records `Ram 5 Pokhara 2080` and `Sita 9 Dharan 2081`, key `9`: the program prints `Record found (record no. 2):` followed by Sita's name, roll number 9, address and batch.

@s 8
**Templates and generic programming.** A template is a blueprint in which the **data type is a parameter**: the programmer writes the logic **once**, and the compiler generates a separate function or class for each type that is used (**instantiation**). This is why one framework works with many data types, and the code is reusable, type-safe and has no run-time cost (unlike `void*` or macros). There are two kinds: **function templates** and **class templates**.

**(a) Function template: one `largest()` for any type.**

```cpp
#include <iostream>
#include <string>
using namespace std;

template <typename T>
T largest(T a, T b) { return (a > b) ? a : b; }

template <typename T>
void swapValues(T &a, T &b) { T t = a; a = b; b = t; }

int main() {
    cout << largest(12, 7) << endl;                    // int    -> 12
    cout << largest(3.5, 8.25) << endl;                // double -> 8.25
    cout << largest('a', 'z') << endl;                 // char   -> z
    cout << largest(string("ram"), string("sita")) << endl;   // string -> sita
    int x = 1, y = 2;  swapValues(x, y);
    cout << x << " " << y << endl;                     // 2 1
    return 0;
}
```

**(b) Class template: one `Stack` for any element type.**

```cpp
#include <iostream>
using namespace std;

template <class T, int SIZE = 10>
class Stack {
    T data[SIZE];
    int top;
public:
    Stack() : top(-1) {}
    bool push(T x) { if (top == SIZE - 1) return false; data[++top] = x; return true; }
    bool pop(T &x) { if (top == -1) return false; x = data[top--]; return true; }
    bool empty() const { return top == -1; }
};

int main() {
    Stack<int> a;                 // stack of int
    Stack<double, 5> b;           // stack of double (capacity 5)
    Stack<char> c;                // stack of char
    a.push(10); a.push(20);
    b.push(1.5); b.push(2.5);
    c.push('x'); c.push('y');
    int i; double d; char ch;
    a.pop(i); b.pop(d); c.pop(ch);
    cout << i << " " << d << " " << ch << endl;       // 20 2.5 y
    return 0;
}
```

The functions `largest`, `swapValues` and the class `Stack` were each written **once**, but the output shows them working for `int`, `double`, `char` and `string`. Writing them without templates would need a separate copy for every type (`largestInt`, `largestDouble`, ...), which is the redundancy that templates remove; the standard library itself (`vector`, `map`, `sort`) is built this way. This justifies the given statement.

@s 9
An **exception** is a **run-time error or abnormal condition** (division by zero, array index out of range, memory not available, file not found, invalid input) that the normal flow of the program cannot handle, so that the program would otherwise terminate abnormally. C++ exception handling uses `try` (the block that may cause the error), `throw` (signals the error with an object or value) and `catch` (the handler of a given type; `catch(...)` handles every type).

**Program: a bank account that handles several exceptions** (a user-defined exception for insufficient balance, an invalid amount, a standard `out_of_range`, and a catch-all).

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;

class InsufficientFunds {                                // user-defined exception
public:
    double balance, needed;
    InsufficientFunds(double b, double n) : balance(b), needed(n) {}
};

class Account {
    double balance;
public:
    Account(double b) : balance(b) {}
    void deposit(double x) {
        if (x <= 0) throw invalid_argument("deposit must be positive");
        balance += x;
    }
    void withdraw(double x) {
        if (x <= 0) throw invalid_argument("withdrawal must be positive");
        if (x > balance) throw InsufficientFunds(balance, x);
        balance -= x;
    }
    double get() const { return balance; }
};

int main() {
    Account acc(1000);
    vector<int> history = {1, 2, 3};
    for (int test = 1; test <= 5; test++) {
        try {
            if (test == 1) { acc.deposit(500);  cout << "Balance " << acc.get() << endl; }
            if (test == 2) acc.withdraw(5000);                    // insufficient
            if (test == 3) acc.deposit(-20);                      // invalid
            if (test == 4) cout << history.at(10) << endl;        // out_of_range
            if (test == 5) throw 'x';                             // some other type
        }
        catch (const InsufficientFunds &e) {
            cout << "Test " << test << ": insufficient funds, balance " << e.balance
                 << " but " << e.needed << " needed\n";
        }
        catch (const invalid_argument &e) { cout << "Test " << test << ": invalid argument: " << e.what() << endl; }
        catch (const out_of_range &e)     { cout << "Test " << test << ": out of range\n"; }
        catch (...)                       { cout << "Test " << test << ": unknown exception\n"; }
    }
    return 0;
}
```

Output:

```
Balance 1500
Test 2: insufficient funds, balance 1500 but 5000 needed
Test 3: invalid argument: deposit must be positive
Test 4: out of range
Test 5: unknown exception
```

The order of the `catch` blocks matters: specific handlers come first and `catch(...)` is last; once an exception is thrown, control leaves the `try` block, the rest of it is skipped, and the program continues after the handlers.

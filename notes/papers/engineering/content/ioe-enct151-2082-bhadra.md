---
file: NEBians-IOE-Past-Paper-Object-Oriented-Programming-ENCT151-2082-Bhadra.pdf
subject: Object Oriented Programming
level: BE · Year I / Part II
code: ENCT 151
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCT, BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What is the drawback of procedural programming and advantage of object-oriented programming along with suitable program code of each? [[2+2]]

@q 2
What do you mean by Namespace? Why namespace feature is needed in C++? Explain with an example program. [[1+2+4]]

@q 3
Explain with example how object can be passed or returned from functions. In which condition a class can be made friend? How can we make a specific member function of a class a friend function of another class? With a complete example show the both of these cases of friend class and friend function of another class. [[3+1+1+4]]

@q 4
What is an operator overloading? Write down the syntax for overloading binary operator using non-member operator function in a class. Write a program to perform addition, subtraction, multiplication and division with complex objects with real and imaginary members. [[1+2+4]]

@q 5
Explain different forms of inheritance with an example for each. Create a class person with data members to identify a person and inherit it to create a class student with appropriate members. Write a complete program showing function overriding to make your program meaningful. [[3+4]]

@q 6
Discuss about late binding and early binding. Write a program to create a classes Employee. Now create a class manager which is derived from employee. Show the use of virtual function with suitable data members and member functions. [[2+3]]

@q 7
What are the different types of file modes used in C++? Write a program with a class to represent an employee having data members to represent name, employee Id, age and salary. Add record of 10 employees in a file and display them in a console. Also search a specific record of an employee using employee Id as a key from the user input. [[2+6]]

@q 8
Show with an example how do we eliminate code redundancy using template. Give with example. WAP to read n numbers of any types and sort them on descending order. For sorting, you can use vector member function. [[4+4]]

@q 9
Explain exception along with their handling constructs. Develop a C++ program that shows multiple exception handling scenarios. [[2+3]]

<!-- SOLUTIONS -->

@s 1
**Drawbacks of procedural programming.**

1. Data is **global** and is shared by many functions; a change in one function can silently corrupt the data used by another, so the programs are hard to debug.
2. There is **no data hiding or protection**: any function can access any data.
3. The real-world objects are **not modelled naturally** (the function is the unit and not the object), so large programs become complex to design and maintain.
4. A change in the data structure forces changes in **all functions** that use it, and the code is **hard to reuse and extend**.

**Advantages of object oriented programming.** Data hiding (security), reusability by inheritance, easy maintenance and extension, natural modelling of real-world entities, polymorphism, less development time, and a modular, easily tested design.


**Procedural program (the drawback).** The global balance is visible to every function, so a careless function can corrupt it:

```cpp
#include <iostream>
using namespace std;

double balance = 1000;                 // global data, open to every function

void deposit(double x)  { balance += x; }
void buggy()            { balance = -5; }          // any function can damage the data

int main() {
    deposit(500);
    buggy();                                        // nothing stops this
    cout << "Balance = " << balance << endl;       // -5 : corrupted
}
```

**Object oriented program (the advantage: data hiding and encapsulation).** The data is private and changes only through checked member functions:

```cpp
#include <iostream>
using namespace std;

class Account {
    double balance;                                  // hidden data
public:
    Account(double b) : balance(b) {}
    void deposit(double x) { if (x > 0) balance += x; }
    double get() const { return balance; }
};

int main() {
    Account a(1000);
    a.deposit(500);
    // a.balance = -5;   // compile error: balance is private
    cout << "Balance = " << a.get() << endl;        // 1500
}
```

@s 2
**Namespace.** A **namespace** is a **named declarative region** that groups related identifiers (variables, functions, classes) under one name, so that they have their own scope and do not clash with identifiers of the same name elsewhere. Syntax: `namespace name { declarations }`. Members are used with the scope resolution operator (`name::member`), a using-declaration (`using name::member;`) or a using-directive (`using namespace name;`). The standard library lives in the namespace `std`.

**Why it is needed.**

1. To **avoid name collision** (the same function or variable name in two libraries or by two programmers in a large project).
2. To **organise** the code into logical groups (modules) and to separate the global scope.
3. To allow the **same names in different libraries** to be used together, and to keep the library names out of the global scope (`std::cout`).

```cpp
#include <iostream>
using namespace std;

namespace Nepal {
    int population = 30;                       // in millions
    void greet() { cout << "Namaste from Nepal\n"; }
}
namespace India {
    int population = 1400;
    void greet() { cout << "Namaste from India\n"; }     // same names, no clash
}

int main() {
    Nepal::greet();                            // scope resolution operator
    India::greet();
    cout << Nepal::population << " " << India::population << endl;   // 30 1400
    {
        using namespace Nepal;                 // using directive within a block
        greet();
    }
    namespace NP = Nepal;                      // namespace alias
    cout << NP::population << endl;
    return 0;
}
```

@s 3
**Passing and returning objects.** An object can be passed to a function like any variable:

1. **By value**: a copy of the object is made (the copy constructor is called); changes in the function do not affect the original.
2. **By reference** (`const Complex &c`) or **by pointer**: no copy is made; the function works on the original object, and it is efficient for large objects.

An object can also be **returned** from a function (by value, which creates a temporary copy, or by reference).

```cpp
#include <iostream>
using namespace std;

class Complex {
    double re, im;
public:
    Complex(double r = 0, double i = 0) : re(r), im(i) {}
    Complex add(Complex c) {                     // object passed by value
        return Complex(re + c.re, im + c.im);    // object returned by value
    }
    void show() const { cout << re << " + " << im << "i\n"; }
};

int main() {
    Complex a(3, 4), b(1, 2);
    Complex c = a.add(b);
    c.show();                                    // 4 + 6i
}
```

**Condition for a friend class.** A class can be made a friend of another class when the second class **needs direct access to the private and protected members of the first** because the two are closely related (for example `Engine` and `Car`, or a `LinkedList` and its `Node`, or a tester of the class); it is declared inside the granting class by `friend class B;`. Friendship is **not mutual** (A granting B does not give A access to B), **not inherited** and **not transitive**.

**Making a member function of one class a friend of another.** Declare the other class (forward declaration), then name the function with its class in the friend declaration, `friend void C::showA(A &);`. The class containing the function must be defined *before* the class that grants the friendship, and the function must be defined *after* both classes are complete.

**Complete example (friend class and friend member function).**

```cpp
#include <iostream>
using namespace std;

class A;                                         // forward declaration

class C {                                        // C has a member function that will be a friend of A
public:
    void showA(A &a);                            // declared here, defined after A
};

class A {
    int x;
public:
    A(int v) : x(v) {}
    friend class B;                              // whole class B is a friend
    friend void C::showA(A &);                   // only this member function of C is a friend
};

class B {
public:
    void setA(A &a, int v) { a.x = v; }          // B can use the private member x
    int  getA(A &a)        { return a.x; }
};

void C::showA(A &a) { cout << "C::showA reads x = " << a.x << endl; }   // private access allowed

int main() {
    A obj(10);
    B b;  C c;
    b.setA(obj, 25);
    cout << "B::getA gives x = " << b.getA(obj) << endl;     // 25
    c.showA(obj);                                            // 25
    return 0;
}
```

@s 4
**Operator overloading.** It is the feature of C++ by which an **existing operator is given an additional meaning for the objects of a user-defined class**, using a special function `operator@`, so that objects can be used like built-in types (`c3 = c1 + c2`). It is a form of compile-time (static) polymorphism; it does not change the precedence, associativity or the operand count of the operator.

**Syntax of a non-member (friend) function for a binary operator.** All operands are passed as arguments:

```
friend ReturnType operator@ (const ClassName &left, const ClassName &right);   // declared in the class

ReturnType operator@ (const ClassName &left, const ClassName &right) {         // defined outside
    // body
}
```

For example, `friend Complex operator+(const Complex &a, const Complex &b);`, and `c1 + c2` is interpreted as `operator+(c1, c2)`.

**Complex arithmetic.** For $(a+bi)$ and $(c+di)$: sum $(a+c)+(b+d)i$, difference $(a-c)+(b-d)i$, product $(ac-bd)+(ad+bc)i$, quotient $\dfrac{(ac+bd)+(bc-ad)i}{c^2+d^2}$.

```cpp
#include <iostream>
using namespace std;

class Complex {
    double re, im;
public:
    Complex(double r = 0, double i = 0) : re(r), im(i) {}
    friend Complex operator+(const Complex &a, const Complex &b);
    friend Complex operator-(const Complex &a, const Complex &b);
    friend Complex operator*(const Complex &a, const Complex &b);
    friend Complex operator/(const Complex &a, const Complex &b);
    void show() const { cout << re << (im < 0 ? " - " : " + ") << (im < 0 ? -im : im) << "i\n"; }
};

Complex operator+(const Complex &a, const Complex &b) { return Complex(a.re + b.re, a.im + b.im); }
Complex operator-(const Complex &a, const Complex &b) { return Complex(a.re - b.re, a.im - b.im); }
Complex operator*(const Complex &a, const Complex &b) {
    return Complex(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
}
Complex operator/(const Complex &a, const Complex &b) {
    double d = b.re * b.re + b.im * b.im;                    // c^2 + d^2
    return Complex((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d);
}

int main() {
    Complex x(3, 4), y(1, -2);
    cout << "x + y = "; (x + y).show();     // 4 + 2i
    cout << "x - y = "; (x - y).show();     // 2 + 6i
    cout << "x * y = "; (x * y).show();     // 11 - 2i
    cout << "x / y = "; (x / y).show();     // -1 + 2i
    return 0;
}
```

Check: $(3+4i)(1-2i) = 3 - 6i + 4i + 8 = 11 - 2i$ and $(3+4i)/(1-2i) = (3+4i)(1+2i)/5 = (-5+10i)/5 = -1+2i$.

@s 5
**Inheritance** is the mechanism by which a **derived (child) class acquires the data members and member functions of a base (parent) class**, so that the code can be reused and a class hierarchy is created. Syntax: `class Derived : public Base { ... };`

| Form | Structure | Example |
|---|---|---|
| **Single** | one base, one derived: `A → B` | `Person → Student` |
| **Multiple** | two or more bases, one derived: `A, B → C` | `Employee, Student → Manager` |
| **Multilevel** | a chain: `A → B → C` | `Person → Employee → Manager` |
| **Hierarchical** | one base, several derived: `A → B, A → C` | `Shape → Circle, Rectangle` |
| **Hybrid** | a combination of the above (for example a diamond: `A → B, A → C, B,C → D`) | `Person → Student, Person → Employee, Student + Employee → TeachingAssistant` |

```cpp
#include <iostream>
using namespace std;

class A { public: int a = 1; };
class B : public A { public: int b = 2; };            // single:     A -> B
class C : public B { public: int c = 3; };            // multilevel: A -> B -> C
class D : public A { public: int d = 4; };            // hierarchical: A -> B, A -> D
class E1 { public: int e1 = 5; };
class E2 { public: int e2 = 6; };
class F : public E1, public E2 { public: int f = 7; };// multiple: E1, E2 -> F

int main() {
    C obj;  F obj2;
    cout << obj.a + obj.b + obj.c << " " << obj2.e1 + obj2.e2 + obj2.f << endl;   // 6 18
}
```


**Class `person` and derived class `student` with function overriding.**

```cpp
#include <iostream>
#include <string>
using namespace std;

class person {
protected:
    string name;
    int age;
    string address;
public:
    person(string n, int a, string ad) : name(n), age(a), address(ad) {}
    void display() const {                                   // base version
        cout << "Name: " << name << "\nAge: " << age << "\nAddress: " << address << "\n";
    }
};

class student : public person {                              // single inheritance
    int roll;
    string faculty;
    float gpa;
public:
    student(string n, int a, string ad, int r, string f, float g)
        : person(n, a, ad), roll(r), faculty(f), gpa(g) {}
    void display() const {                                   // overrides person::display()
        person::display();                                   // reuse the base version
        cout << "Roll: " << roll << "\nFaculty: " << faculty << "\nGPA: " << gpa << "\n";
    }
};

int main() {
    person p("Hari Thapa", 40, "Lalitpur");
    student s("Gita Rai", 20, "Dharan", 7, "Computer", 3.6f);
    cout << "-- person --\n";  p.display();                  // base version
    cout << "-- student --\n"; s.display();                  // derived version (overriding)
    return 0;
}
```

@s 6
**Early (static) binding** means that the call of a function is resolved at **compile time**, from the declared type of the pointer or reference (normal functions, overloaded functions and operators). It is fast. **Late (dynamic) binding** means that the call is resolved at **run time**, from the type of the object actually pointed to. It is obtained with **virtual functions** called through a base class pointer or reference, and it implements run-time polymorphism (through the **vtable**: each class with virtual functions has a table of function addresses and each object has a hidden pointer to it).

| Point | Early binding | Late binding |
|---|---|---|
| Time | compile time | run time |
| Decided by | type of the pointer | type of the object |
| Needs | ordinary and overloaded functions | `virtual` functions and a base pointer or reference |
| Speed | faster | slightly slower (vtable lookup) |
| Flexibility | less | more |

A **virtual function** is a member function of the base class, declared with the keyword `virtual`, which a derived class may **override**; a call through a base pointer then runs the derived version. A **pure virtual function** has no definition in the base class and is declared as `virtual void f() = 0;`; a class with at least one pure virtual function is an **abstract class**, and cannot be instantiated; the derived class must override it (otherwise it is abstract too).


**Program: `Employee` and `Manager` with a virtual function.**

```cpp
#include <iostream>
#include <string>
using namespace std;

class Employee {
protected:
    string name;
    int id;
    double salary;
public:
    Employee(string n, int i, double s) : name(n), id(i), salary(s) {}
    virtual void display() const {                           // virtual: decided at run time
        cout << "Employee " << name << " (ID " << id << "), salary " << salary << "\n";
    }
    virtual ~Employee() {}
};

class Manager : public Employee {
    double bonus;
    int teamSize;
public:
    Manager(string n, int i, double s, double b, int t) : Employee(n, i, s), bonus(b), teamSize(t) {}
    void display() const override {                          // overriding
        cout << "Manager " << name << " (ID " << id << "), salary " << salary
             << ", bonus " << bonus << ", team of " << teamSize << "\n";
    }
};

int main() {
    Employee e("Ramesh", 101, 40000);
    Manager  m("Sunita", 102, 80000, 15000, 8);
    Employee *p;                                             // base class pointer
    p = &e;  p->display();                                   // Employee::display()
    p = &m;  p->display();                                   // Manager::display(): late binding
    return 0;
}
```

Without the keyword `virtual`, the second call would also run `Employee::display()` (early binding, by the pointer type).

@s 7
**File modes** (the second argument of `open()` or of the `fstream` constructor):

| Mode | Meaning |
|---|---|
| `ios::in` | open for reading (default for `ifstream`) |
| `ios::out` | open for writing; an existing file is truncated (default for `ofstream`) |
| `ios::app` | append: every write goes to the end of the file |
| `ios::ate` | open and move to the end of the file at once (writes may be anywhere) |
| `ios::trunc` | discard the contents of an existing file |
| `ios::binary` | binary mode (no newline translation) |
| `ios::nocreate`, `ios::noreplace` | (old compilers) fail if the file does not exist or already exists |

Modes are combined with `|`, e.g. `fstream f("data.dat", ios::in | ios::out | ios::binary);`.


**Program.** The records are stored as fixed-size binary records, so that each can be read back with `read()`; the file is first written with 10 employees, then displayed, then searched by employee ID.

```cpp
#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;

class Employee {
    char name[30];
    int id;
    int age;
    double salary;
public:
    void input() {
        cout << "Name: ";   cin >> name;
        cout << "ID: ";     cin >> id;
        cout << "Age: ";    cin >> age;
        cout << "Salary: "; cin >> salary;
    }
    void display() const {
        cout << id << "\t" << name << "\t" << age << "\t" << salary << "\n";
    }
    int getId() const { return id; }
};

int main() {
    const int N = 10;
    // 1. add the records of 10 employees to the file
    ofstream fout("employee.dat", ios::binary | ios::out);
    if (!fout) { cerr << "Cannot open file\n"; return 1; }
    Employee e;
    for (int i = 0; i < N; i++) {
        cout << "Employee " << i + 1 << ":\n";
        e.input();
        fout.write(reinterpret_cast<char *>(&e), sizeof(e));
    }
    fout.close();

    // 2. display all records on the console
    ifstream fin("employee.dat", ios::binary | ios::in);
    cout << "\nID\tName\tAge\tSalary\n";
    while (fin.read(reinterpret_cast<char *>(&e), sizeof(e)))
        e.display();
    fin.close();

    // 3. search a record by employee ID
    int key;
    cout << "\nEnter the employee ID to search: ";
    cin >> key;
    fin.open("employee.dat", ios::binary | ios::in);
    bool found = false;
    while (fin.read(reinterpret_cast<char *>(&e), sizeof(e))) {
        if (e.getId() == key) {
            cout << "Record found:\n";
            e.display();
            found = true;
            break;
        }
    }
    if (!found) cout << "No employee with ID " << key << endl;
    fin.close();
    return 0;
}
```

@s 8
**Removing code redundancy with a template.** Without templates, the same algorithm has to be written again for every data type:

```cpp
int    maxi(int a, int b)       { return a > b ? a : b; }
double maxd(double a, double b) { return a > b ? a : b; }
char   maxc(char a, char b)     { return a > b ? a : b; }     // three copies of the same logic
```

With one **function template** the compiler writes each version when it is needed:

```cpp
#include <iostream>
using namespace std;

template <class T>
T maximum(T a, T b) { return (a > b) ? a : b; }               // one definition for all types

int main() {
    cout << maximum(3, 8) << " " << maximum(2.5, 1.2) << " " << maximum('p', 'k') << endl;   // 8 2.5 p
}
```

The logic is written and maintained **once**; a bug fix or change applies to all the types, and the code is still type checked.

**Program: read n numbers of any type and sort them in descending order** (a function template with `vector` member functions `push_back()`, `size()`, `begin()` and `end()`).

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
using namespace std;

template <class T>
void readAndSort(int n) {
    vector<T> v;                                   // vector of any type
    T x;
    cout << "Enter " << n << " numbers: ";
    for (int i = 0; i < n; i++) {
        cin >> x;
        v.push_back(x);                            // member function
    }
    sort(v.begin(), v.end(), greater<T>());       // descending order
    cout << "Descending order: ";
    for (size_t i = 0; i < v.size(); i++) cout << v[i] << " ";
    cout << endl;
}

int main() {
    int n;
    cout << "How many numbers? ";
    cin >> n;
    cout << "Integers:\n"; readAndSort<int>(n);
    cout << "Real numbers:\n"; readAndSort<double>(n);
    return 0;
}
```

For the input `4 7 1 9` the integers are printed as `9 7 4 1`; for `2.5 9.1 0.3 4` the reals are printed as `9.1 4 2.5 0.3`.

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


**Program with multiple exception handling scenarios** (divide by zero, array index out of range, invalid argument and a standard library exception, with a catch-all handler).

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>
#include <cmath>
using namespace std;

class DivideByZero {};                                       // user defined exception class

double divide(double a, double b) {
    if (b == 0) throw DivideByZero();
    return a / b;
}

double elementAt(const vector<double> &v, int i) {
    if (i < 0 || i >= (int)v.size()) throw out_of_range("index out of range");
    return v[i];
}

double squareRoot(double x) {
    if (x < 0) throw invalid_argument("square root of a negative number");
    return sqrt(x);
}

int main() {
    vector<double> v = {1.5, 2.5, 3.5};
    for (int test = 1; test <= 4; test++) {
        try {
            if (test == 1) cout << divide(10, 0) << endl;
            if (test == 2) cout << elementAt(v, 7) << endl;
            if (test == 3) cout << squareRoot(-4) << endl;
            if (test == 4) throw 42;                         // an int exception
        }
        catch (const DivideByZero &)       { cout << "Test " << test << ": division by zero\n"; }
        catch (const out_of_range &e)      { cout << "Test " << test << ": out_of_range: " << e.what() << "\n"; }
        catch (const invalid_argument &e)  { cout << "Test " << test << ": invalid_argument: " << e.what() << "\n"; }
        catch (...)                        { cout << "Test " << test << ": unknown exception\n"; }
    }
    return 0;
}
```

Output:

```
Test 1: division by zero
Test 2: out_of_range: index out of range
Test 3: invalid_argument: square root of a negative number
Test 4: unknown exception
```

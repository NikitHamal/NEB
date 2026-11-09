---
file: NEBians-IOE-Past-Paper-Object-Oriented-Programming-CT151-2081-Ashwin.pdf
subject: Object Oriented Programming
level: BE · Year I / Part II
code: CT 151
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BCT, BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What are the benefits of object-oriented programming? Describe the feature of object-oriented programming. [[2+2]]

@q 2
Define reference variable and write syntax for defining reference variable. WAP a function which calculates A where $A = P\left(1 + \dfrac{r}{100}\right)^n$ for data p, r and n. But for some cases value of r is fix that is 50. Call this function in main. [[2+5]]

@q 3
Explain friend function and with program code, how friend function can be used to make bridge between two classes? Create a class time, constructor having hour, minutes and second as arguments is used to initialize time objects. The add function that takes two class objects as arguments add them respectively then display the aggregate result. (Apply 60 seconds = 1 minute, 60 minutes = 1 hour and 24 hour = 1 day). [[2+3+4]]

@q 4
How is operator overloading used in case of binary operator? List down the rules of operator overloading. Create a class Length that has two data members meter and centimeter. Write a program to compare the length of two objects of this class by overloading '>' operator. Use constructor to initialize data members. [[1+2+4]]

@q 5
What is IS-A relation and HAS-A relationship? What do you mean by multipath inheritance? Explain how ambiguity due to multipath inheritance could be resolved. [[2+2+3]]

@q 6
What do you mean by abstract class? WAP to create two classes employee and student. Now create a class manager which is derived from two base classes employee and student and a class secretary derived from employee. Show the use of virtual destructor. [[1+4]]

@q 7
Explain different types of file access. Write a program for library to store information of different books (as least 5 items) in a file and display them on console. [[3+5]]

@q 8
Explain the use of default argument in template class. Write to suitable program to show the concept of function template. Explain in brief about stack in Standard Template Library. [[3+3+2]]

@q 9
Discuss steps taken during exception handling. Write a program to compute square root of a number. The input value must be tested for validity. If it is negative, an exception must be raised. [[2+3]]

<!-- SOLUTIONS -->

@s 1
**Benefits (advantages) of object oriented programming.**

1. **Data hiding and security**: the data is private to the object and is reached only through its member functions, so it cannot be corrupted accidentally.
2. **Reusability**: classes already written and tested can be reused directly or extended by **inheritance**, which saves time and cost.
3. **Natural modelling**: real world entities (student, account, vehicle) become objects, so the design is close to the problem; complex software is easier to design.
4. **Easy maintenance and extension**: a change is limited to the class concerned, and new features are added by deriving new classes.
5. **Modularity and team work**: classes are independent modules which different programmers can develop and test separately.
6. **Polymorphism**: the same interface works for many types, so the code is flexible and shorter.
7. **Less redundancy** (inheritance, templates), and the programs are **easy to upgrade** from small to large systems.
8. Several objects of one class can **coexist** without interfering with each other, and **message passing** simplifies the interface between parts of the program.

**Features (basic concepts) of object oriented programming.**

| Feature | Meaning |
|---|---|
| **Object and class** | an object is an instance having data and functions; a class is its user-defined type (blueprint) |
| **Encapsulation** | binding the data and the functions into one unit, the class |
| **Data abstraction** | exposing only the essential interface and hiding the implementation |
| **Data hiding** | `private` and `protected` members cannot be accessed from outside |
| **Inheritance** | a derived class acquires the members of a base class (reuse, hierarchy) |
| **Polymorphism** | many forms of one name: overloading (compile time), virtual functions (run time) |
| **Dynamic binding** | the function executed is decided at run time |
| **Message passing** | objects communicate by calling member functions |

@s 2
**Reference variable.** A reference variable is an **alias (another name) for an already existing variable**. It does not occupy a separate variable of its own; it must be **initialised when it is declared** and cannot be made to refer to another variable later. Any change through the reference changes the original variable.

Syntax:

```
datatype &reference_name = variable_name;
```

For example, `int x = 10; int &r = x;` makes `r` another name of `x` (`r = 20;` makes `x` equal to 20). References are used as function parameters (call by reference) and as return types of functions.

**The function.** $A = P\left(1 + \dfrac{r}{100}\right)^n$. Because the rate $r$ is **fixed at 50 in some cases**, it is given as a **default argument** (the last parameter), which is used when the caller does not supply $r$.

```cpp
#include <iostream>
#include <cmath>
using namespace std;

double amount(double p, int n, double r = 50);      // default value r = 50 given once, at the declaration

int main() {
    double p, r;
    int n;
    cout << "Enter principal P and number of years n: ";
    cin >> p >> n;
    cout << "A with the fixed rate r = 50 : " << amount(p, n) << endl;   // r takes the default value 50
    cout << "Enter another rate r: ";
    cin >> r;
    cout << "A with r = " << r << " : " << amount(p, n, r) << endl;      // r is supplied
    return 0;
}

double amount(double p, int n, double r) {           // the default is NOT repeated in the definition
    return p * pow(1 + r / 100, n);
}
```

For $P = 1000$, $n = 2$: with $r = 50$, $A = 1000(1.5)^2 = 2250$; with $r = 10$, $A = 1000(1.1)^2 = 1210$.

@s 3
**Friend function.** A **friend function** is a function that is **not a member** of a class but is allowed to access its **private and protected members**. It is declared inside the class with the keyword `friend` (the declaration may be placed in the private or the public part), and is defined outside like an ordinary function, without `friend` and without the scope operator. It is called like an ordinary function (not with the dot operator), it receives the objects as arguments, and it cannot use the member names directly (`obj.member` is needed).

**Friend function as a bridge between two classes.** When one function has to work on the private data of **two different classes**, it is declared as a friend in **both**; it then acts as a bridge. For example, a function that compares the temperature in a `Celsius` object with a `Fahrenheit` object:

```cpp
#include <iostream>
using namespace std;

class Fahrenheit;                                    // forward declaration

class Celsius {
    double c;
public:
    Celsius(double v) : c(v) {}
    friend bool hotter(const Celsius &, const Fahrenheit &);   // bridge
};

class Fahrenheit {
    double f;
public:
    Fahrenheit(double v) : f(v) {}
    friend bool hotter(const Celsius &, const Fahrenheit &);   // the same function
};

bool hotter(const Celsius &a, const Fahrenheit &b) {          // uses the private data of both
    return a.c > (b.f - 32) * 5.0 / 9.0;
}

int main() {
    Celsius c(40);
    Fahrenheit f(98.6);                                        // 37 degrees C
    cout << (hotter(c, f) ? "Celsius object is hotter" : "Fahrenheit object is hotter") << endl;
    return 0;
}
```

Output: `Celsius object is hotter` (40 °C > 37 °C).

**Class `time` and the friend function `add`.** The constructor takes hour, minute and second. Seconds are added first; every 60 seconds carry one minute, every 60 minutes one hour, and 24 hours make one day (the hours are reduced modulo 24 and the days are shown separately).

The program below stores the result in a `Time` that also keeps the `day` count, so that all the carries (seconds → minutes → hours → days) are done in one place and the friend function stays simple.

```cpp
#include <iostream>
using namespace std;

class Time {
    int day, hour, minute, second;
public:
    Time(int h = 0, int m = 0, int s = 0) {              // constructor initialises the time object
        second = s % 60;           m = m + s / 60;       // 60 seconds = 1 minute
        minute = m % 60;           h = h + m / 60;       // 60 minutes = 1 hour
        hour   = h % 24;           day = h / 24;         // 24 hours  = 1 day
    }
    friend Time add(const Time &a, const Time &b);
    void display() const {
        cout << day << " day " << hour << " hr " << minute << " min " << second << " sec\n";
    }
};

Time add(const Time &a, const Time &b) {                 // adds hour+hour, minute+minute, second+second
    int h = a.day * 24 + a.hour + b.day * 24 + b.hour;
    int m = a.minute + b.minute;
    int s = a.second + b.second;
    return Time(h, m, s);                                // the constructor applies the carries
}

int main() {
    Time t1(15, 45, 50), t2(10, 20, 30);
    cout << "t1: "; t1.display();
    cout << "t2: "; t2.display();
    Time sum = add(t1, t2);
    cout << "t1 + t2 = "; sum.display();
    return 0;
}
```

Output: seconds $50 + 30 = 80 = 1$ min $20$ s; minutes $45 + 20 + 1 = 66 = 1$ hr $6$ min; hours $15 + 10 + 1 = 26 = 1$ day $2$ hr, so

```
t1: 0 day 15 hr 45 min 50 sec
t2: 0 day 10 hr 20 min 30 sec
t1 + t2 = 1 day 2 hr 6 min 20 sec
```

@s 4
**Operator overloading for a binary operator.** A binary operator (`+`, `-`, `*`, `>`, `==`, ...) takes two operands. When it is overloaded as a **member function**, the **left operand is the calling object** and the **right operand is the single argument**: `a > b` is read as `a.operator>(b)`. When it is overloaded as a **friend (non-member) function**, both operands are passed as arguments: `operator>(a, b)`. The function name is `operator` followed by the symbol, and it returns the result (an object for `+`, a `bool` for `>`).

**Rules of operator overloading.**

1. Only the **existing operators** can be overloaded; new symbols cannot be made.
2. `::`, `.`, `.*`, `?:` and `sizeof` **cannot be overloaded**.
3. At least one operand must be a **user-defined type**; the behaviour for built-in types cannot be changed.
4. The **precedence, associativity and number of operands** of the operator remain the same.
5. `=`, `[]`, `()` and `->` can be overloaded only as **member functions**; `<<` and `>>` as non-member (friend) functions.
6. A unary operator as a member takes **no** argument, a binary operator as a member takes **one**; as friends, they take one and two.
7. Overloading should keep the **natural meaning** of the operator.

**Program: class `Length` with `>` overloaded.** The length is normalised so that 100 cm make 1 m, which makes the comparison simple: meters are compared first, then centimeters.

```cpp
#include <iostream>
using namespace std;

class Length {
    int meter, centimeter;
public:
    Length(int m = 0, int cm = 0) {
        meter = m + cm / 100;                 // normalise: 100 cm = 1 m
        centimeter = cm % 100;
    }
    bool operator>(const Length &other) const {      // a > b   ==   a.operator>(b)
        if (meter != other.meter) return meter > other.meter;
        return centimeter > other.centimeter;
    }
    void display() const { cout << meter << " m " << centimeter << " cm"; }
};

int main() {
    Length a(3, 45), b(2, 180);              // b = 3 m 80 cm after normalising
    cout << "L1 = "; a.display(); cout << "\nL2 = "; b.display(); cout << endl;
    if (a > b)      cout << "L1 is longer than L2\n";
    else if (b > a) cout << "L2 is longer than L1\n";
    else            cout << "Both lengths are equal\n";
    return 0;
}
```

Output: `L2 is longer than L1` (3 m 45 cm against 3 m 80 cm).

@s 5
**IS-A relationship.** It expresses **inheritance** (a "kind of" relationship): the derived class *is a* special type of the base class and can be used wherever the base class is expected. It is implemented with public inheritance: `class Dog : public Animal`, "a Dog IS-A Animal"; a `Student` is a `Person`.

**HAS-A relationship.** It expresses **composition or aggregation** (a "part of" or "contains" relationship): a class has an object of another class as a **data member**. A `Car` HAS-A `Engine`; a `Library` has `Book`s. The container uses the services of the member object but is not a kind of it.

```cpp
class Engine { public: void start() {} };
class Vehicle { };
class Car : public Vehicle {          // IS-A: Car is a Vehicle
    Engine e;                         // HAS-A: Car has an Engine
public:
    void drive() { e.start(); }
};
```

**Multipath inheritance.** It is a form of **hybrid inheritance in which a class is derived from two classes that have a common base class**, so that the derived class reaches that base through **more than one path** (the *diamond*): `A → B`, `A → C`, and `B, C → D`. The object of `D` then contains **two copies** of the members of `A` (one through `B`, one through `C`).

```
        A
       / \
      B   C
       \ /
        D
```

**Ambiguity and its resolution.** For `D d; d.a;` the compiler cannot decide whether the `a` of `A` via `B` or via `C` is meant, so the call is **ambiguous** (a compile error), and the duplicate copy wastes memory. Two solutions:

1. **Scope resolution operator**: name the path explicitly, `d.B::a` or `d.C::a`. The two copies still exist.
2. **Virtual base class** (the correct solution): declare the common base as `virtual` in the intermediate classes, `class B : virtual public A`, `class C : virtual public A`. Then `D` contains **only one shared copy** of `A`, and `d.a` is unambiguous.

```cpp
#include <iostream>
using namespace std;

class A { public: int a = 5; };
class B : virtual public A { public: int b = 1; };     // virtual base class
class C : virtual public A { public: int c = 2; };
class D : public B, public C { public: int d = 3; };

int main() {
    D obj;
    cout << obj.a << endl;                              // 5, unambiguous: only one copy of A
    cout << obj.a + obj.b + obj.c + obj.d << endl;      // 11
    cout << sizeof(D) << endl;                          // one A subobject only
    return 0;
}
```

Without `virtual`, the statement `obj.a` would not compile ("request for member 'a' is ambiguous"), and `obj.B::a` would have to be written.

@s 6
**Abstract class.** An abstract class is a class that has **at least one pure virtual function** (`virtual void f() = 0;`). It is meant only as a **base class**: no object of it can be created, but pointers and references to it can be used for run-time polymorphism. A derived class becomes concrete only when it overrides **all** the pure virtual functions.

**Program.** `employee` and `student` are the two base classes; `manager` is derived from both (multiple inheritance); `secretary` is derived from `employee`. The destructors are **virtual**, so that deleting an object through a base class pointer calls the destructor of the **derived** class first and then those of the bases, and no part is leaked.

```cpp
#include <iostream>
#include <string>
using namespace std;

class employee {
protected:
    string name;
    int id;
public:
    employee(string n = "", int i = 0) : name(n), id(i) { cout << "employee constructor\n"; }
    virtual void display() const { cout << "Employee: " << name << " (ID " << id << ")\n"; }
    virtual ~employee() { cout << "employee destructor\n"; }       // virtual destructor
};

class student {
protected:
    string course;
    float gpa;
public:
    student(string c = "", float g = 0) : course(c), gpa(g) { cout << "student constructor\n"; }
    virtual ~student() { cout << "student destructor\n"; }          // virtual destructor
};

class manager : public employee, public student {                   // two base classes
    int teamSize;
public:
    manager(string n, int i, string c, float g, int t)
        : employee(n, i), student(c, g), teamSize(t) { cout << "manager constructor\n"; }
    void display() const override {
        cout << "Manager: " << name << " (ID " << id << "), studying " << course
             << " GPA " << gpa << ", team of " << teamSize << "\n";
    }
    ~manager() { cout << "manager destructor\n"; }
};

class secretary : public employee {                                 // derived from employee only
    string boss;
public:
    secretary(string n, int i, string b) : employee(n, i), boss(b) { cout << "secretary constructor\n"; }
    void display() const override { cout << "Secretary: " << name << " (ID " << id << "), works for " << boss << "\n"; }
    ~secretary() { cout << "secretary destructor\n"; }
};

int main() {
    employee *p1 = new manager("Anita", 11, "MBA", 3.6f, 8);
    employee *p2 = new secretary("Bimal", 12, "Anita");
    p1->display();
    p2->display();
    cout << "--- deleting through base class pointers ---\n";
    delete p1;          // virtual destructor: ~manager, ~student, ~employee
    delete p2;          // ~secretary, ~employee
    return 0;
}
```

Output (the part that shows the virtual destructor):

```
--- deleting through base class pointers ---
manager destructor
student destructor
employee destructor
secretary destructor
employee destructor
```

If `~employee()` were not virtual, `delete p1` would call only `employee::~employee()`, the `manager` part would never be destroyed (undefined behaviour and a resource leak).

@s 7
**Types of file access.**

1. **Sequential access**: the records are processed one after another from the beginning to the end (the file is read in the order in which it was written). To reach record $k$ all previous records are passed. It is simple and is used for text files, e.g. `ifstream`/`ofstream` with `>>`, `<<`, `getline()` or `read()`/`write()` in a loop.
2. **Random (direct) access**: the file pointer can be **moved to any position** and the record there is read or written directly, with `seekg()` / `seekp()` (and `tellg()` / `tellp()`), which is fast for fixed-length records (the position of record $k$ is $k \times$ `sizeof(record)`). It is used with an `fstream` opened for `ios::in | ios::out | ios::binary`.

Besides, by content the files are **text files** (characters, with newline translation, `<<` `>>`) and **binary files** (the bytes of the object as they are in memory, written with `write()` and read with `read()`). The access mode is given in `open()`: `ios::in`, `ios::out`, `ios::app`, `ios::ate`, `ios::trunc`, `ios::binary`.

**Program: library books stored in a file and displayed.** Five books (at least) are written as fixed-size binary records, and then the file is read back sequentially and shown on the console.

```cpp
#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;

class Book {
    int  id;
    char title[40];
    char author[30];
    float price;
public:
    void input() {
        cout << "Book id: ";  cin >> id;
        cout << "Title (no spaces): ";  cin >> title;
        cout << "Author (no spaces): "; cin >> author;
        cout << "Price: ";    cin >> price;
    }
    void display() const {
        cout << left << setw(6) << id << setw(20) << title << setw(15) << author << price << "\n";
    }
};

int main() {
    const int N = 5;
    ofstream fout("library.dat", ios::binary);          // write mode
    Book b;
    for (int i = 0; i < N; i++) {
        cout << "Enter book " << i + 1 << ":\n";
        b.input();
        fout.write(reinterpret_cast<char *>(&b), sizeof(b));
    }
    fout.close();

    ifstream fin("library.dat", ios::binary);           // read mode
    cout << "\n" << left << setw(6) << "ID" << setw(20) << "Title" << setw(15) << "Author" << "Price\n";
    while (fin.read(reinterpret_cast<char *>(&b), sizeof(b)))
        b.display();
    fin.close();
    return 0;
}
```

Sample input of five books such as `1 DataStructures Tanenbaum 850`, `2 CppPrimer Lippman 1200` ... gives a table with the heading `ID Title Author Price` followed by the five rows.

@s 8
**Default argument in a template class.** A template parameter may be given a **default value** in the same way as a function argument, so that the user need not supply it. It is a default **type** (`template <class T = int>`) or a default **non-type** value (`template <class T, int SIZE = 10>`). If the argument is omitted at the point of the object declaration, the default is used; the angle brackets are still written (`Stack<> s;`). Defaults must be given from the **right** (a parameter with a default cannot be followed by one without it). This avoids repeating the common choice and keeps the interface simple.

```cpp
#include <iostream>
using namespace std;

template <class T = int, int SIZE = 5>              // default type int, default size 5
class Stack {
    T data[SIZE];
    int top;
public:
    Stack() : top(-1) {}
    void push(T x) { if (top < SIZE - 1) data[++top] = x; else cout << "overflow\n"; }
    T pop() { return top >= 0 ? data[top--] : T(); }
    int size() const { return top + 1; }
};

int main() {
    Stack<> s1;                 // Stack<int, 5>
    Stack<double> s2;           // Stack<double, 5>
    Stack<char, 3> s3;          // Stack<char, 3>
    s1.push(7); s1.push(9);
    s2.push(2.5);
    s3.push('a'); s3.push('b'); s3.push('c'); s3.push('d');      // overflow
    cout << s1.pop() << " " << s2.pop() << " " << s3.pop() << endl;   // 9 2.5 c
    return 0;
}
```

**Function template program.** A function template defines a family of functions; the compiler deduces `T` from the arguments. The program finds the largest element of an array of any type and swaps two values.

```cpp
#include <iostream>
using namespace std;

template <class T>
T maxElement(T arr[], int n) {
    T m = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > m) m = arr[i];
    return m;
}

template <class T>
void swapT(T &a, T &b) { T t = a; a = b; b = t; }

int main() {
    int    a[] = {4, 19, 7, 12};
    double d[] = {2.5, 1.75, 9.5};
    char   c[] = {'m', 'z', 'b'};
    cout << maxElement(a, 4) << " " << maxElement(d, 3) << " " << maxElement(c, 3) << endl;   // 19 9.5 z
    double x = 1.5, y = 4.5;
    swapT(x, y);
    cout << x << " " << y << endl;                                                          // 4.5 1.5
    return 0;
}
```

**Stack in the Standard Template Library (STL).** `std::stack` (header `<stack>`) is a **container adaptor** that gives a **LIFO** (last in, first out) structure, built on top of another container (by default `deque`; `vector` or `list` can be chosen). It is itself a class template, `stack<T, Container>`, and offers only the stack interface:

| Member | Action |
|---|---|
| `push(x)` | put `x` on the top |
| `pop()` | remove the top element (returns nothing) |
| `top()` | access the top element |
| `empty()` | `true` when no element |
| `size()` | number of elements |

All operations take constant time. There is no iterator and no access to the middle elements.

```cpp
#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> st;
    st.push(10); st.push(20); st.push(30);
    cout << st.top() << " " << st.size() << endl;     // 30 3
    st.pop();
    cout << st.top() << endl;                         // 20
    while (!st.empty()) { cout << st.top() << " "; st.pop(); }   // 20 10
    cout << endl;
    return 0;
}
```

@s 9
**Steps taken during exception handling.**

1. **Find the problem (hit the exception)**: the program runs inside a **`try` block** and an error condition occurs (division by zero, invalid value, out of range).
2. **Throw the exception**: the code that detects the error executes a **`throw`** statement with an object or value that describes it; the normal flow stops at once, and the rest of the `try` block is skipped.
3. **Catch the exception**: the run-time system **unwinds the stack** (destroying the local objects) and looks for the **first `catch` handler whose parameter type matches** the thrown object; `catch(...)` catches any type.
4. **Handle the exception**: the statements of the handler take the corrective action (message, retry, clean-up).
5. **Continue**: after the handler, the program resumes with the statements **after the last `catch` block**. If no handler matches, `std::terminate()` is called and the program aborts.

```
try { ... throw obj; ... }  ->  catch (type e) { handle }  ->  execution continues after the handlers
```

**Program: square root with validity test.** A negative input raises an exception, caught in `main`.

```cpp
#include <iostream>
#include <cmath>
#include <stdexcept>
using namespace std;

double squareRoot(double x) {
    if (x < 0)
        throw invalid_argument("negative number has no real square root");   // raise the exception
    return sqrt(x);
}

int main() {
    double x;
    cout << "Enter a number: ";
    cin >> x;
    try {
        double r = squareRoot(x);                 // may throw
        cout << "Square root of " << x << " = " << r << endl;
    }
    catch (const invalid_argument &e) {
        cout << "Error: " << e.what() << endl;
    }
    cout << "Program ends normally.\n";
    return 0;
}
```

Runs: input `49` gives `Square root of 49 = 7`; input `-9` gives `Error: negative number has no real square root`, and in both cases the program ends with `Program ends normally.`

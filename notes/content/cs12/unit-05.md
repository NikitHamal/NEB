---
subject: Computer Science
grade: 12
unit: 5
title: Object-Oriented Programming (OOP)
hours: 10
---

Every program you wrote in Unit 4 was a list of instructions that pushed data
around: `main()` called a function, the function worked on variables, and the
variables sat outside in the open. Object-oriented programming turns that
picture inside out. Data and the code that is allowed to touch it are locked
together into one unit called an **object**, and a program becomes a set of
objects sending messages to each other. This unit is about that idea — the four
features the syllabus names (class, object, inheritance, polymorphism), why the
software industry moved to it, and where it is used.

::: key What the exam asks from this unit
This is a 10-hour unit but it is mostly **theory**. Group B almost always has
one of: *define class and object with an example*, *differentiate between
procedural and object-oriented programming*, *explain any four features of OOP*.
Group C asks you to **write a program** with a class, a constructor, inheritance
and function overloading/overriding, so learn one complete program template by
heart. All example code here is C++, the language NEB uses for OOP.
:::

## 5.1 Programming paradigms: procedural, structural and object oriented

A **programming paradigm** is a style of organising a program — a way of
thinking about what a program *is*. Three paradigms matter for this course.

**Procedural (or monolithic-then-procedural) programming.** The program is a
sequence of instructions grouped into procedures (functions). Data is usually
**global**, so any function can read or change it. Design is **top-down**: split
the job into functions, then split those into smaller functions. FORTRAN (1957),
COBOL (1959) and C (1972) are procedural languages.

**Structured programming.** This is procedural programming with discipline
added. It insists that every algorithm be built from only three control
structures — sequence, selection (`if`, `switch`) and iteration (`for`, `while`)
— each with a single entry and a single exit, and that `goto` be avoided.
Dijkstra's 1968 letter *"Go To Statement Considered Harmful"* started it. A
structured program is divided into independent modules that communicate through
parameters and return values instead of global variables. C is the classic
structured language, and everything you did in Unit 4 was structured
programming.

**Object-oriented programming.** The program is organised around the *data*, not
the actions. Data and the functions that operate on it are wrapped into a single
unit (an object); outside code can only reach the data through the functions the
object chooses to publish. Design is **bottom-up**: first identify the objects
in the problem, then give them behaviour. Simula 67 (Dahl and Nygaard, 1967) was
the first object-oriented language; Smalltalk (Xerox PARC, 1970s) made the ideas
famous; C++ (Bjarne Stroustrup, Bell Labs — "C with Classes" in 1979, renamed
C++ in 1983, released 1985), Java (1995), Python, C# and Kotlin are the
languages in use today.

```figure caption="Left: procedural code — functions reach into shared global data, so a change in the data affects every function. Right: object-oriented code — data is sealed inside the object and reached only through its public methods."
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.1, 2.9))
for ax in (a1, a2):
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
a1.add_patch(Rectangle((1.6, 7.4), 6.8, 1.8, fc='#eaf1f8', ec=ACCENT, lw=1.3))
a1.text(5.0, 8.3, 'GLOBAL DATA', ha='center', va='center', fontsize=9, color=INK)
for x, lab in [(0.4, 'fn1()'), (3.7, 'fn2()'), (7.0, 'fn3()')]:
    a1.add_patch(Rectangle((x, 2.8), 2.6, 1.5, fc='none', ec=MUTED, lw=1.0))
    a1.text(x + 1.3, 3.55, lab, ha='center', va='center', fontsize=8.8, color=INK)
    a1.add_patch(FancyArrowPatch((x + 1.3, 4.35), (5.0, 7.3), arrowstyle='<|-|>',
                                mutation_scale=9, color=MUTED, lw=0.9,
                                shrinkA=0, shrinkB=0))
a1.text(5.0, 1.3, 'data is exposed to every function', ha='center',
        fontsize=8.2, color=MUTED, style='italic')
a1.set_title('Procedural / structured', fontsize=9.6)
a2.add_patch(Circle((5.0, 5.2), 3.3, fc='#eaf1f8', ec=ACCENT, lw=1.3))
a2.add_patch(Circle((5.0, 5.2), 1.6, fc='white', ec=INK, lw=1.1, ls='--'))
a2.text(5.0, 5.2, 'DATA\n(private)', ha='center', va='center', fontsize=8.4, color=INK)
for ang, lab in [(115, 'put()'), (235, 'get()'), (325, 'show()')]:
    r = np.radians(ang)
    a2.text(5.0 + 2.05 * np.cos(r), 5.2 + 2.15 * np.sin(r), lab, ha='center',
            va='center', fontsize=8.2, color=ACCENT)
a2.add_patch(FancyArrowPatch((9.4, 9.4), (6.9, 7.1), arrowstyle='-|>',
                             mutation_scale=10, color='#d9534f', lw=1.2))
a2.text(9.6, 9.6, 'message', ha='right', fontsize=8.2, color='#d9534f')
a2.text(5.0, 1.3, 'only the methods can touch the data', ha='center',
        fontsize=8.2, color=MUTED, style='italic')
a2.set_title('Object-oriented', fontsize=9.6)
```

The same tiny job — the area of a rectangle — written both ways makes the
difference concrete. First procedural C:

```c
#include <stdio.h>

struct Rect { float len, bre; };          /* data only */

float area(struct Rect r) {               /* function kept separate */
    return r.len * r.bre;
}

int main() {
    struct Rect r = {12.5f, 8.0f};
    printf("Area = %.2f sq. m\n", area(r));
    return 0;
}
```

Output:

```
Area = 100.00 sq. m
```

Nothing stops another part of the program from writing `r.len = -5;`. Now the
object-oriented version in C++:

```cpp
#include <iostream>
using namespace std;

class Rect {
    float len, bre;                       // data: private, hidden
  public:
    Rect(float l, float b) {              // constructor
        len = l; bre = b;
    }
    float area() {                        // behaviour: bundled with the data
        return len * bre;
    }
};

int main() {
    Rect r(12.5, 8.0);
    cout << "Area = " << r.area() << " sq. m" << endl;
    return 0;
}
```

Output:

```
Area = 100 sq. m
```

`r.len` is now inaccessible from `main()`; the only way in is the constructor,
and the only way out is `area()`.

| Feature | Procedural / structured | Object-oriented |
|---|---|---|
| Basic unit | function (procedure) | class / object |
| Design direction | top-down | bottom-up |
| Data handling | mostly global, shared | private inside objects |
| Data security | weak — any function can change data | strong — access specifiers protect data |
| Code reuse | by calling functions again | by inheritance, plus functions |
| Adding a new feature | often means editing existing functions | usually means adding a new class |
| Real-world modelling | poor | direct (one object per real thing) |
| Suitable for | small and medium programs | large, long-lived, multi-programmer software |
| Examples | C, FORTRAN, COBOL, Pascal | C++, Java, Python, C#, Kotlin |

::: caution "Structural" is not a third kind of language
The syllabus word *structural* means **structured programming**, which is a
disciplined form of procedural programming — not a separate family. C is both
procedural and structured. Do not write that C is "structural but not
procedural".
:::

## 5.2 Features of OOP: class, object, polymorphism and inheritance

### 5.2.1 Class and object

::: definition Class and object
A **class** is a user-defined data type that binds together data members
(attributes) and member functions (methods) under one name. It is only a
*blueprint* — writing a class allocates no memory for data.
An **object** is an instance of a class: a real variable of that class type,
with its own copy of the data members, created in memory at run time.
:::

Class is to object what `struct Student` is to a particular student variable —
except that a class also carries the functions. In `Rect r(12.5, 8.0);` the class
is `Rect` and the object is `r`.

```figure caption="One class, many objects. The class fixes what attributes exist; each object stores its own values for them."
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(Rectangle((0.2, 3.6), 3.0, 4.6, fc='#eaf1f8', ec=ACCENT, lw=1.3))
ax.text(1.7, 7.7, 'class Student', ha='center', fontsize=9.2, color=INK, weight='bold')
ax.plot([0.2, 3.2], [7.3, 7.3], color=ACCENT, lw=1.0)
for i, t in enumerate(['name', 'roll', 'marks[3]']):
    ax.text(0.45, 6.75 - 0.55 * i, '- ' + t, fontsize=8.4, color=INK)
ax.plot([0.2, 3.2], [4.9, 4.9], color=ACCENT, lw=1.0)
for i, t in enumerate(['+ total()', '+ display()']):
    ax.text(0.45, 4.45 - 0.55 * i, t, fontsize=8.4, color=ACCENT)
ax.text(1.7, 2.3, 'blueprint — no memory\nfor data', ha='center', fontsize=8.0,
        color=MUTED, style='italic')
objs = [('s1', 'Sita Rai', '1', '78 85 92'), ('s2', 'Bikash Thapa', '2', '55 61 48'),
        ('s3', 'Mina Gurung', '3', '90 88 95')]
for k, (nm, a, b, c) in enumerate(objs):
    y = 7.6 - 2.7 * k
    ax.add_patch(Rectangle((5.6, y - 1.9), 4.2, 1.9, fc='white', ec=MUTED, lw=1.0))
    ax.text(5.8, y - 0.45, 'object ' + nm, fontsize=8.4, color=ACCENT, weight='bold')
    ax.text(5.8, y - 1.05, a + '   roll ' + b, fontsize=8.0, color=INK)
    ax.text(5.8, y - 1.6, 'marks  ' + c, fontsize=8.0, color=INK)
    ax.add_patch(FancyArrowPatch((3.3, 5.9), (5.5, y - 0.95), arrowstyle='-|>',
                                mutation_scale=9, color=MUTED, lw=0.9,
                                connectionstyle='arc3,rad=0.12'))
ax.text(4.4, 9.2, 'instantiation', ha='center', fontsize=8.2, color=MUTED)
```

The general form of a class in C++ is:

```cpp
class ClassName {
  private:                 // default; hidden from outside
    // data members
  protected:               // visible to derived classes only
    // data members
  public:                  // the interface
    ClassName();           // constructor
    ~ClassName();          // destructor
    // member functions
};                         // note the semicolon
```

A **constructor** is a member function with the same name as the class, with no
return type, called automatically when an object is created; it is used to
initialise the data members. A **destructor** (`~ClassName()`) is called
automatically when the object is destroyed. Here is a full class with both kinds
of constructor, a validating setter and a static member:

```cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

class Student {
    // ---- private data members: hidden state of the object ----
    string name;
    int    roll;
    int    marks[3];

  public:
    static int count;                       // one copy shared by all objects

    Student() {                             // default constructor
        name = "not admitted"; roll = 0;
        marks[0] = marks[1] = marks[2] = 0;
        count++;
    }
    Student(string n, int r, int m1, int m2, int m3) {   // parameterised
        name = n; roll = r;
        marks[0] = m1; marks[1] = m2; marks[2] = m3;
        count++;
    }
    int total() const { return marks[0] + marks[1] + marks[2]; }

    double percentage() const { return total() / 3.0; }

    char grade() const {
        double p = percentage();
        if (p >= 80)      return 'A';
        else if (p >= 60) return 'B';
        else if (p >= 40) return 'C';
        else              return 'F';
    }
    void setMarks(int i, int m) {            // controlled write access
        if (i >= 0 && i < 3 && m >= 0 && m <= 100) marks[i] = m;
        else cout << "Invalid mark rejected" << endl;
    }
    void display() const {
        cout << setw(5) << roll << setw(16) << name << setw(7) << total()
             << setw(9) << fixed << setprecision(2) << percentage()
             << setw(7) << grade() << endl;
    }
};

int Student::count = 0;                      // static member defined outside

int main() {
    Student s1("Sita Rai", 1, 78, 85, 92);
    Student s2("Bikash Thapa", 2, 55, 61, 48);

    cout << setw(5) << "Roll" << setw(16) << "Name" << setw(7) << "Total"
         << setw(9) << "Percent" << setw(7) << "Grade" << endl;
    s1.display();
    s2.display();

    s2.setMarks(1, 105);                     // rejected by the setter
    cout << "Students created = " << Student::count << endl;
    return 0;
}
```

Output (compiled with `g++ student.cpp -o student`):

```
 Roll            Name  Total  Percent  Grade
    1        Sita Rai    255    85.00      A
    2    Bikash Thapa    164    54.67      C
Invalid mark rejected
Students created = 2
```

### 5.2.2 Data encapsulation and data hiding

**Encapsulation** is the wrapping of data and the functions that act on it into
one unit — the class. The consequence is **data hiding**: because `name`, `roll`
and `marks` are `private`, no statement outside the class can read or write them
directly. `s1.marks[0] = 999;` is a compile-time error. All traffic goes through
the public interface, which can check it — that is why `setMarks(1, 105)`
printed a rejection instead of storing an impossible mark.

| Access specifier | Same class | Derived class | Outside the class |
|---|---|---|---|
| `private` | yes | no | no |
| `protected` | yes | yes | no |
| `public` | yes | yes | yes |

```figure caption="What each access specifier lets through. Code outside the class reaches only the public interface; a derived class also sees the protected part; nothing outside reaches the private part."
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1, 3.0))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(Rectangle((0.3, 0.9), 5.4, 8.2, fc='white', ec=INK, lw=1.2))
ax.text(3.0, 8.6, 'class Student', ha='center', fontsize=8.8, weight='bold', color=INK)
bands = [('private:  name, roll, marks[3]', 5.6, '#fdeeed', '#d9534f'),
         ('protected:  schoolCode', 3.7, '#fdf6e6', '#b8860b'),
         ('public:  total()  display()', 1.4, '#eaf1f8', ACCENT)]
for lab, y, fc, ec in bands:
    ax.add_patch(Rectangle((0.7, y), 4.6, 1.9, fc=fc, ec=ec, lw=1.1))
    ax.text(3.0, y + 0.95, lab, ha='center', va='center', fontsize=7.6, color=INK)
ax.add_patch(Rectangle((6.6, 6.2), 3.2, 1.4, fc='white', ec=MUTED, lw=1.0))
ax.text(8.2, 6.9, 'class Teacher\n(derived)', ha='center', va='center',
        fontsize=7.8, color=INK)
ax.add_patch(Rectangle((6.6, 2.2), 3.2, 1.4, fc='white', ec=MUTED, lw=1.0))
ax.text(8.2, 2.9, 'main()\n(outside code)', ha='center', va='center',
        fontsize=7.8, color=INK)
ax.add_patch(FancyArrowPatch((6.5, 6.9), (5.4, 4.7), arrowstyle='-|>',
                             mutation_scale=9, color='#b8860b', lw=1.1))
ax.add_patch(FancyArrowPatch((6.5, 6.6), (5.4, 2.4), arrowstyle='-|>',
                             mutation_scale=9, color=ACCENT, lw=1.1))
ax.add_patch(FancyArrowPatch((6.5, 2.9), (5.4, 2.3), arrowstyle='-|>',
                             mutation_scale=9, color=ACCENT, lw=1.1))
ax.add_patch(FancyArrowPatch((6.5, 3.6), (6.05, 6.3), arrowstyle='-|>',
                             mutation_scale=9, color='#d9534f', lw=1.0, ls=':'))
ax.text(5.95, 6.55, '\u2715', fontsize=12, color='#d9534f', ha='center')
ax.text(6.75, 4.6, 'blocked', ha='left', fontsize=7.4, color='#d9534f')
```

### 5.2.3 Abstraction

**Abstraction** means showing only the essential features and hiding the
internal detail. You call `s1.percentage()` without knowing whether the marks
are stored in an array, three separate variables or a file. In C++, abstraction
is achieved with the class interface and, at a higher level, with **abstract
classes** — classes containing at least one *pure virtual* function
(`virtual double earning() const = 0;`), which cannot be instantiated and exist
only to fix the interface that derived classes must provide.

::: tip Encapsulation vs abstraction in one line
Encapsulation is **how** it is hidden (bundling + access specifiers);
abstraction is **what** the user is shown (the interface). Give this one line and
one example in the exam and the mark is yours.
:::

### 5.2.4 Inheritance

::: definition Inheritance
Inheritance is the mechanism by which one class (the **derived**, child or
sub-class) acquires the data members and member functions of another class (the
**base**, parent or super-class), and may then add its own members or redefine
inherited ones. It gives *reusability* and expresses an **"is-a"** relationship:
a Teacher *is a* Person.
:::

```cpp
class Teacher : public Person {   // public inheritance
    // extra members
};
```

Five forms of inheritance are examinable:

| Type | Structure | Example |
|---|---|---|
| Single | one base, one derived | `Person → Student` |
| Multilevel | derived class becomes a base | `Person → Student → HostelStudent` |
| Multiple | one derived, two or more bases | `Student + Athlete → SportsScholar` |
| Hierarchical | one base, many derived | `Person → Student, Teacher, Staff` |
| Hybrid | a combination of the above | multilevel + multiple together |

```figure caption="The five forms of inheritance. An arrow points from the derived class to its base class, as in UML."
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, axes = plt.subplots(1, 5, figsize=(5.2, 2.5))
def box(ax, x, y, t, w=1.5, h=0.62):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc='#eaf1f8',
                           ec=ACCENT, lw=1.0))
    ax.text(x, y, t, ha='center', va='center', fontsize=7.6, color=INK)
def up(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                 mutation_scale=8, color=MUTED, lw=0.9))
titles = ['Single', 'Multilevel', 'Multiple', 'Hierarchical', 'Hybrid']
for ax, t in zip(axes, titles):
    ax.axis('off'); ax.set_xlim(0, 4); ax.set_ylim(0, 6)
    ax.set_title(t, fontsize=8.2, pad=4)
a, b, c, d, e = axes
box(a, 2, 5, 'A'); box(a, 2, 2, 'B'); up(a, 2, 2.35, 2, 4.65)
box(b, 2, 5.2, 'A'); box(b, 2, 3.1, 'B'); box(b, 2, 1.0, 'C')
up(b, 2, 3.45, 2, 4.85); up(b, 2, 1.35, 2, 2.75)
box(c, 1.1, 5, 'A'); box(c, 2.9, 5, 'B'); box(c, 2, 2, 'C')
up(c, 1.8, 2.35, 1.2, 4.65); up(c, 2.2, 2.35, 2.8, 4.65)
box(d, 2, 5, 'A'); box(d, 1.0, 2, 'B'); box(d, 3.0, 2, 'C')
up(d, 1.1, 2.35, 1.8, 4.65); up(d, 2.9, 2.35, 2.2, 4.65)
box(e, 2, 5.2, 'A'); box(e, 1.0, 3.1, 'B'); box(e, 3.0, 3.1, 'C'); box(e, 2, 1.0, 'D')
up(e, 1.1, 3.45, 1.85, 4.85); up(e, 2.9, 3.45, 2.15, 4.85)
up(e, 1.9, 1.35, 1.1, 2.75); up(e, 2.1, 1.35, 2.9, 2.75)
```

When an object of a derived class is created, the **base constructor runs
first**, then the derived constructor; destructors run in the exact reverse
order. This order is a favourite one-mark question.

```figure caption="Order of constructor and destructor calls for a derived object. Construction goes base-first, destruction derived-first."
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 2.4))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
steps = [('Person()', 1), ('Teacher()', 2), ('object\nin use', 3),
         ('~Teacher()', 4), ('~Person()', 5)]
for i, (lab, n) in enumerate(steps):
    x = 0.25 + i * 1.98
    fc = '#eaf1f8' if n in (1, 2) else ('#fdeeed' if n in (4, 5) else 'white')
    ec = ACCENT if n in (1, 2) else ('#d9534f' if n in (4, 5) else MUTED)
    ax.add_patch(Rectangle((x, 2.4), 1.72, 1.3, fc=fc, ec=ec, lw=1.1))
    ax.text(x + 0.86, 3.05, lab, ha='center', va='center', fontsize=7.6, color=INK)
    if i < 4:
        ax.add_patch(FancyArrowPatch((x + 1.78, 3.05), (x + 1.92, 3.05),
                                     arrowstyle='-|>', mutation_scale=9,
                                     color=MUTED, lw=1.0))
ax.text(2.1, 1.6, 'construction: base → derived', ha='center', fontsize=8.2, color=ACCENT)
ax.text(8.0, 1.6, 'destruction: derived → base', ha='center', fontsize=8.2, color='#d9534f')
ax.text(5.0, 4.6, 'Teacher t("Ram Sharma", 41, "Computer", 48500);', ha='center',
        fontsize=8.0, color=INK, family='monospace')
```

### 5.2.5 Polymorphism

::: definition Polymorphism
Polymorphism (Greek: *many forms*) is the ability of one name, operator or
message to behave differently depending on the type or number of the data it is
used with. C++ provides **compile-time polymorphism** through function
overloading and operator overloading, and **run-time polymorphism** through
virtual functions and overriding.
:::

**Compile-time (static) polymorphism.** Several functions share one name but
differ in the number or type of parameters; the compiler picks the right one from
the call:

```cpp
#include <iostream>
using namespace std;

// compile-time polymorphism: one name, three different signatures
int  volume(int s)                  { return s * s * s; }          // cube
int  volume(int l, int b, int h)    { return l * b * h; }          // cuboid
double volume(double r, double h)   { return 3.1416 * r * r * h; } // cylinder

int main() {
    cout << "Cube      : " << volume(4)          << endl;
    cout << "Cuboid    : " << volume(5, 4, 3)    << endl;
    cout << "Cylinder  : " << volume(2.0, 7.0)   << endl;
    return 0;
}
```

Output:

```
Cube      : 64
Cuboid    : 60
Cylinder  : 87.9648
```

**Run-time (dynamic) polymorphism.** A base-class pointer holds a derived-class
object, and the function that actually runs is decided while the program is
running. The base function must be declared `virtual`, otherwise the compiler
binds the call early and the base version runs:

```cpp
#include <iostream>
using namespace std;

class Base {
  public:
    void show()         { cout << "Base::show  (not virtual)" << endl; }
    virtual void draw() { cout << "Base::draw  (virtual)"     << endl; }
};

class Derived : public Base {
  public:
    void show()          { cout << "Derived::show" << endl; }
    void draw() override { cout << "Derived::draw" << endl; }
};

int main() {
    Derived d;
    Base *bp = &d;        // base pointer holding a derived object
    bp->show();           // early (compile-time) binding  -> Base
    bp->draw();           // late  (run-time)  binding     -> Derived
    return 0;
}
```

Output:

```
Base::show  (not virtual)
Derived::draw
```

```figure caption="Compile-time polymorphism resolves the call by signature before the program runs; run-time polymorphism resolves it from the actual object type while the program runs."
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.1, 2.8))
for ax in (a1, a2):
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
a1.set_title('Compile-time (overloading)', fontsize=9.0)
a1.add_patch(Rectangle((2.0, 7.8), 6.0, 1.4, fc='white', ec=INK, lw=1.1))
a1.text(5.0, 8.5, 'volume(5, 4, 3)', ha='center', va='center', fontsize=7.6,
        family='monospace', color=INK)
sigs = ['volume(int)', 'volume(int,int,int)', 'volume(double,double)']
for i, s in enumerate(sigs):
    y = 5.6 - 2.0 * i
    sel = (i == 1)
    a1.add_patch(Rectangle((1.2, y), 7.6, 1.3, fc='#eaf1f8' if sel else 'none',
                           ec=ACCENT if sel else MUTED, lw=1.2 if sel else 0.9))
    a1.text(5.0, y + 0.65, s, ha='center', va='center', fontsize=8.0,
            family='monospace', color=INK)
a1.add_patch(FancyArrowPatch((5.0, 7.7), (5.0, 7.0), arrowstyle='-|>',
                             mutation_scale=9, color=MUTED, lw=1.0))
a1.text(5.0, 0.7, 'the compiler picks the matching signature', ha='center',
        fontsize=7.8, color=ACCENT)
a2.set_title('Run-time (virtual function)', fontsize=9.0)
a2.add_patch(Rectangle((2.6, 8.0), 4.8, 1.3, fc='white', ec=INK, lw=1.1))
a2.text(5.0, 8.65, 'p->earning()', ha='center', va='center', fontsize=8.2,
        family='monospace', color=INK)
for i, (lab, txt, x0) in enumerate([('Teacher', 'salary', 0.2),
                                    ('Student', 'scholarship', 5.2)]):
    a2.add_patch(Rectangle((x0, 3.4), 4.6, 2.4, fc='#eaf1f8', ec=ACCENT, lw=1.0))
    a2.text(x0 + 0.25, 5.1, lab + '::', fontsize=7.8, family='monospace', color=ACCENT)
    a2.text(x0 + 0.25, 4.5, 'earning()', fontsize=7.8, family='monospace', color=ACCENT)
    a2.text(x0 + 0.25, 3.8, 'return ' + txt + ';', fontsize=6.0, family='monospace',
            color=INK)
    a2.add_patch(FancyArrowPatch((5.0, 7.95), (x0 + 2.3, 5.9), arrowstyle='-|>',
                                 mutation_scale=9, color=MUTED, lw=1.0))
a2.text(5.0, 1.8, 'the object that p points to\npicks the version', ha='center',
        fontsize=7.8, color=ACCENT)
```

| | Function overloading | Function overriding |
|---|---|---|
| Where | same class (or scope) | base class and derived class |
| Signature | must differ | must be identical |
| Binding | early, at compile time | late, at run time |
| Keyword needed | none | `virtual` in the base class |
| Type of polymorphism | compile-time (static) | run-time (dynamic) |

### 5.2.6 Message passing and dynamic binding

Objects do not call each other's code directly; they **send messages** — a
message is the name of a member function plus its arguments, sent to a named
object (`s1.display()`). **Dynamic binding** (late binding) means the code
associated with a message is not known until run time, which is exactly what
makes `p[i]->display()` behave differently for each element of the array below.

Putting every feature into one program gives the classic Group C answer:

```cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

// ---------------- base class ----------------
class Person {
  protected:
    string name;
    int    age;
  public:
    Person(string n, int a) : name(n), age(a) {
        cout << "Person constructor: " << name << endl;
    }
    virtual void display() const {                 // virtual -> late binding
        cout << left << setw(14) << name << setw(5) << age;
    }
    virtual double earning() const = 0;            // pure virtual: abstract class
    virtual ~Person() { cout << "Person destructor: " << name << endl; }
};

// ---------------- derived class 1 ----------------
class Teacher : public Person {
    string subject;
    double salary;
  public:
    Teacher(string n, int a, string s, double sal)
        : Person(n, a), subject(s), salary(sal) {
        cout << "Teacher constructor: " << name << endl;
    }
    void display() const override {
        Person::display();                          // reuse the base version
        cout << setw(10) << "Teacher" << setw(12) << subject
             << "Rs " << fixed << setprecision(2) << earning() << endl;
    }
    double earning() const override { return salary; }
};

// ---------------- derived class 2 ----------------
class Student : public Person {
    string faculty;
    double scholarship;
  public:
    Student(string n, int a, string f, double sc)
        : Person(n, a), faculty(f), scholarship(sc) {
        cout << "Student constructor: " << name << endl;
    }
    void display() const override {
        Person::display();
        cout << setw(10) << "Student" << setw(12) << faculty
             << "Rs " << fixed << setprecision(2) << earning() << endl;
    }
    double earning() const override { return scholarship; }
};

int main() {
    Person *p[3];                                   // base-class pointers
    p[0] = new Teacher("Ram Sharma", 41, "Computer", 48500);
    p[1] = new Student("Sita Rai",   18, "Science",   1200);
    p[2] = new Teacher("Gita Magar", 35, "Maths",    52000);

    cout << "\n--- Staff and student list ---" << endl;
    double sum = 0;
    for (int i = 0; i < 3; i++) {
        p[i]->display();                            // same call, different code
        sum += p[i]->earning();
    }
    cout << "Total monthly payout = Rs " << sum << "\n" << endl;

    for (int i = 0; i < 3; i++) delete p[i];        // virtual destructor runs
    return 0;
}
```

Output:

```
Person constructor: Ram Sharma
Teacher constructor: Ram Sharma
Person constructor: Sita Rai
Student constructor: Sita Rai
Person constructor: Gita Magar
Teacher constructor: Gita Magar

--- Staff and student list ---
Ram Sharma    41   Teacher   Computer    Rs 48500.00
Sita Rai      18   Student   Science     Rs 1200.00
Gita Magar    35   Teacher   Maths       Rs 52000.00
Total monthly payout = Rs 101700.00

Person destructor: Ram Sharma
Person destructor: Sita Rai
Person destructor: Gita Magar
```

A class diagram is how this design is drawn on paper. UML notation puts the
class name, then attributes, then methods in one box, marks private members with
`-` and public with `+`, uses a hollow triangle arrow for inheritance and a plain
line for association.

```figure caption="UML class diagram for the program above: `Teacher` and `Student` inherit from the abstract class `Person` (hollow triangle), and a `School` is associated with many of each."
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon
fig, ax = plt.subplots(figsize=(5.1, 3.4))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
def uml(x, y, w, title, attrs, meths, italic=False):
    h1, ha_, hm = 0.62, 0.42 * len(attrs), 0.42 * len(meths)
    H = h1 + ha_ + hm
    ax.add_patch(Rectangle((x, y), w, H, fc='white', ec=INK, lw=1.0))
    ax.add_patch(Rectangle((x, y + ha_ + hm), w, h1, fc='#eaf1f8', ec=INK, lw=1.0))
    ax.text(x + w / 2, y + ha_ + hm + h1 / 2, title, ha='center', va='center',
            fontsize=8.0, color=INK, weight='bold',
            style='italic' if italic else 'normal')
    ax.plot([x, x + w], [y + hm, y + hm], color=INK, lw=0.9)
    for i, a in enumerate(attrs):
        ax.text(x + 0.16, y + hm + ha_ - 0.26 - 0.42 * i, a, fontsize=7.4, color=INK)
    for i, m in enumerate(meths):
        ax.text(x + 0.16, y + hm - 0.26 - 0.42 * i, m, fontsize=7.4, color=ACCENT)
    return (x + w / 2, y, x + w / 2, y + H)
pc = uml(3.4, 6.3, 4.2, 'Person  {abstract}',
         ['# name : string', '# age : int'],
         ['+ display()', '+ earning() = 0'], italic=True)
tc = uml(0.1, 1.4, 4.1, 'Teacher',
         ['- subject : string', '- salary : double'],
         ['+ display()', '+ earning()'])
sc = uml(5.6, 1.4, 4.3, 'Student',
         ['- faculty : string', '- scholarship : double'],
         ['+ display()', '+ earning()'])
def inherit(child):
    cx, cy0, _, cy1 = child
    ax.plot([cx, cx], [cy1, 5.3], color=MUTED, lw=1.0)
    ax.plot([cx, 5.5], [5.3, 5.3], color=MUTED, lw=1.0)
    ax.plot([5.5, 5.5], [5.3, 5.98], color=MUTED, lw=1.0)
    ax.add_patch(Polygon([[5.5, 6.3], [5.22, 5.98], [5.78, 5.98]], closed=True,
                         fc='white', ec=MUTED, lw=1.0))
inherit(tc); inherit(sc)
ax.add_patch(Rectangle((0.1, 9.0), 2.2, 0.8, fc='white', ec=INK, lw=1.0))
ax.text(1.2, 9.4, 'School', ha='center', va='center', fontsize=8.4, weight='bold')
ax.plot([2.3, 5.5], [9.4, 9.4], color=MUTED, lw=1.0)
ax.plot([5.5, 5.5], [9.4, 8.6], color=MUTED, lw=1.0)
ax.text(2.6, 9.55, 'employs / enrols', fontsize=7.2, color=MUTED)
ax.text(5.65, 8.8, '1..*', fontsize=7.2, color=MUTED)
```

| OOP principle | What it means | Example from this chapter |
|---|---|---|
| Class | blueprint of data + methods | `class Student { ... };` |
| Object | an instance with its own data | `Student s1("Sita Rai", 1, 78, 85, 92);` |
| Encapsulation | data + methods in one unit | `marks[3]` is `private`, reached via `setMarks()` |
| Data hiding | outsiders cannot touch the data | `s1.marks[0] = 999;` fails to compile |
| Abstraction | show the interface, hide the detail | `percentage()` hides how marks are stored |
| Inheritance | derived class reuses a base class | `class Teacher : public Person` |
| Polymorphism | one name, many behaviours | `volume()` overloaded; `earning()` overridden |
| Dynamic binding | function chosen at run time | `p[i]->display()` inside the loop |
| Message passing | calling a method on an object | `s1.display()` |

::: example Worked example 5.1 — class with a calculation
**Problem.** Write a C++ class `Employee` with a parameterised constructor that
stores a name and a basic salary. Add member functions to compute a 20 % allowance,
the gross pay, 1 % social-security tax on the gross, and the net pay. Show the
payslip for Hari Bahadur, whose basic salary is Rs 35,000.

**Solution.**

```cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

class Employee {
    string name;
    double basic;
  public:
    Employee(string n, double b) : name(n), basic(b) {}
    double allowance() const { return 0.20 * basic; }        // 20% of basic
    double gross()     const { return basic + allowance(); }
    double tax()       const { return 0.01 * gross(); }      // 1% social security
    double net()       const { return gross() - tax(); }
    void payslip() const {
        cout << "Employee : " << name << endl;
        cout << fixed << setprecision(2);
        cout << "  Basic     Rs " << setw(10) << basic      << endl;
        cout << "  Allowance Rs " << setw(10) << allowance() << endl;
        cout << "  Gross     Rs " << setw(10) << gross()     << endl;
        cout << "  Tax (1%)  Rs " << setw(10) << tax()       << endl;
        cout << "  Net pay   Rs " << setw(10) << net()       << endl;
    }
};

int main() {
    Employee e("Hari Bahadur", 35000);
    e.payslip();
    return 0;
}
```

Checking the arithmetic by hand: allowance $= 0.20 \times 35000 = 7000$, gross
$= 35000 + 7000 = 42000$, tax $= 0.01 \times 42000 = 420$, net
$= 42000 - 420 = 41580$. The program prints exactly that:

```
Employee : Hari Bahadur
  Basic     Rs   35000.00
  Allowance Rs    7000.00
  Gross     Rs   42000.00
  Tax (1%)  Rs     420.00
  Net pay   Rs   41580.00
```
:::

::: example Worked example 5.2 — predict the output
**Problem.** What does this program print, and why?

```cpp
class A {
  public:
    A()              { cout << "A "; }
    void f()         { cout << "A::f "; }
    virtual void g() { cout << "A::g "; }
};
class B : public A {
  public:
    B()              { cout << "B "; }
    void f()         { cout << "B::f "; }
    void g()         { cout << "B::g "; }
};
int main() { A *p = new B(); p->f(); p->g(); }
```

**Solution.** `new B()` first runs the base constructor `A()`, then `B()`, so the
first output is `A B `. `f()` is **not** virtual, so `p->f()` is bound at compile
time using the pointer's type `A*` and prints `A::f `. `g()` **is** virtual, so
the call is bound at run time using the object's real type `B` and prints `B::g `.

Full output: `A B A::f B::g `
:::

::: caution Three errors that cost marks every year
1. Forgetting the **semicolon** after the closing brace of a class.
2. Writing a return type for a constructor (`void Student()` is not a constructor).
3. Expecting a base pointer to call the derived function **without** `virtual` —
   it will not. Overriding needs `virtual` in the base class.
:::

## 5.3 Advantages of OOP

1. **Reusability.** Inheritance lets a tested class be extended instead of
   rewritten, and a class can be shipped as a library others reuse.
2. **Data security.** Access specifiers make the data private, so an object
   cannot be corrupted by unrelated code.
3. **Easier maintenance.** A bug in `percentage()` can only be caused by code
   inside `Student`, so the search space is one class, not the whole program.
4. **Modelling power.** Objects map one-to-one onto real things — student,
   invoice, bus route — so the design is easier to discuss with the customer.
5. **Extensibility.** Adding a `Staff` class to the payroll program above needs
   no change at all to `main()`, because `main()` only talks to `Person*`.
6. **Modular team work.** Different programmers can own different classes and
   agree only on the public interfaces.
7. **Message passing** makes communication between parts of a large system
   explicit and easy to trace.

The costs are real too, and examiners accept them as "disadvantages": programs
are larger and need more memory, execution can be slightly slower because of
dynamic binding, the design phase takes longer, and the paradigm is overkill for
a 20-line calculation.

## 5.4 Application of OOP

| Application area | Why OOP fits | Typical tools |
|---|---|---|
| Graphical user interfaces | every widget is an object with properties and events | Qt, Android SDK, JavaFX |
| Simulation and modelling | the original purpose of Simula — each entity is an object | traffic, weather, queue simulations |
| Computer games and graphics | player, enemy, bullet all inherit from a common base | Unity (C#), Unreal (C++) |
| Mobile applications | activity/view classes are extended by the developer | Kotlin, Swift |
| Web frameworks | request, model, controller classes | Laravel (PHP), Django (Python) |
| Operating systems and device drivers | device classes with a common interface | C++ subsystems in Windows, macOS |
| CAD/CAM and design software | geometric shapes form a natural class hierarchy | AutoCAD, SolidWorks |
| Database and ORM layers | a table row becomes an object | Hibernate, Eloquent |
| Banking, ERP and payroll software | account, customer, transaction objects; auditability | Java/C# enterprise systems |
| AI and data-science libraries | model classes with a shared `fit/predict` interface | scikit-learn, TensorFlow |

::: example Worked example 5.3 — choosing the paradigm
**Problem.** A Kathmandu school wants (a) a program to convert a temperature from
Celsius to Fahrenheit for a physics class, and (b) a school management system
holding students, teachers, fees, attendance and exam results, to be maintained
for the next ten years by different programmers. Which paradigm suits each, and
why?

**Solution.**
(a) Procedural/structured C is the right choice. The task is a single formula,
$F = \frac{9}{5}C + 32$; one function is enough, and a class would add code
without adding safety.

(b) Object-oriented design is the right choice. There are many real-world
entities (Student, Teacher, Fee, Attendance, Exam) with shared attributes, so a
`Person` base class removes duplication; the data is sensitive, so private
members with validating setters protect it; the system will be extended for ten
years, so adding a class must not break existing code; and several programmers
can own separate classes at once.
:::

## Chapter summary

- A paradigm is a style of organising a program: procedural (functions on shared
  data), structured (procedural with only sequence/selection/iteration and
  modules), object-oriented (data and behaviour bundled into objects).
- A **class** is a blueprint binding data members and member functions; an
  **object** is an instance of a class with its own copy of the data.
- A **constructor** has the class's name, no return type, and runs automatically
  at creation; the destructor `~Class()` runs at destruction. In inheritance,
  constructors run base→derived and destructors derived→base.
- **Encapsulation** bundles data with methods; **data hiding** follows from
  `private`; **abstraction** exposes only the interface. `private` = class only,
  `protected` = class + derived, `public` = everywhere.
- **Inheritance** (single, multilevel, multiple, hierarchical, hybrid) gives
  reuse and expresses "is-a"; the derived class inherits with
  `class D : public B`.
- **Polymorphism** is compile-time (function/operator overloading, early
  binding) or run-time (overriding a `virtual` function through a base pointer,
  late binding).
- Advantages: reusability, data security, easy maintenance, real-world modelling,
  extensibility, parallel team work. Costs: bigger code, slower dynamic
  dispatch, longer design phase.
- OOP is used for GUIs, simulation, games, mobile apps, web frameworks,
  operating systems, CAD, ORMs, banking systems and ML libraries.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is **not** a feature of object-oriented programming? <span class="marks">[1]</span>
   (a) inheritance (b) polymorphism (c) encapsulation (d) global data sharing
2. A class is best described as <span class="marks">[1]</span>
   (a) an instance of an object (b) a blueprint for objects
   (c) a block of memory (d) a library function
3. Which member function is called automatically when an object is created? <span class="marks">[1]</span>
   (a) destructor (b) friend function (c) constructor (d) `main()`
4. Members declared `protected` in a base class are accessible in <span class="marks">[1]</span>
   (a) the base class only (b) the base and derived classes
   (c) everywhere (d) nowhere
5. Function overloading is an example of <span class="marks">[1]</span>
   (a) run-time polymorphism (b) compile-time polymorphism
   (c) inheritance (d) encapsulation
6. `class C : public A, public B` is an example of <span class="marks">[1]</span>
   (a) single inheritance (b) multilevel inheritance
   (c) multiple inheritance (d) hierarchical inheritance

::: note Answers to Group A
**1.** (d) — OOP *hides* data rather than sharing it globally.
**2.** (b) — a class allocates no data memory; objects do.
**3.** (c) — the constructor; it has the class name and no return type.
**4.** (b) — `protected` is private to the outside world but visible to children.
**5.** (b) — the compiler picks the version from the signature.
**6.** (c) — one derived class with two base classes.
:::

**Group B — Short answer (5 marks each)**

1. Define class and object. Write a C++ class `Circle` with a constructor and a
   member function that returns the area, and create one object of it. <span class="marks">[5]</span>
2. Differentiate between procedural and object-oriented programming on any five
   points. <span class="marks">[5]</span>
3. What is inheritance? Explain any three types with a diagram. <span class="marks">[5]</span>
4. Distinguish between function overloading and function overriding with one
   example of each. <span class="marks">[5]</span>
5. State any five advantages of OOP and any two of its disadvantages. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definitions as in §5.2.1. Program:

```cpp
#include <iostream>
using namespace std;
class Circle {
    double r;
  public:
    Circle(double radius) { r = radius; }
    double area() { return 3.1416 * r * r; }
};
int main() {
    Circle c(7.0);
    cout << "Area = " << c.area() << endl;   // prints Area = 153.938
    return 0;
}
```

Check: $3.1416 \times 7^2 = 3.1416 \times 49 = 153.9384$, so the output is
`Area = 153.938` (`cout` shows six significant figures by default).

**2.** Use any five rows of the table in §5.1 — basic unit, design direction,
data handling, security, reuse, suitability.

**3.** Inheritance = a derived class acquiring the members of a base class, giving
reuse and an "is-a" relationship. Single (`A → B`), multilevel (`A → B → C`),
multiple (`A, B → C`), hierarchical (one base, many derived) — draw as in the
figure in §5.2.4.

**4.** Table in §5.2.5: overloading is same class + different signature + early
binding; overriding is base/derived + identical signature + `virtual` + late
binding. Examples: `volume(int)` / `volume(int,int,int)`, and
`Person::earning()` / `Teacher::earning()`.

**5.** Advantages: reusability, data security, maintainability, real-world
modelling, extensibility (§5.3). Disadvantages: larger programs and more memory;
slower because of dynamic binding; longer design time.
:::

**Group C — Long answer (8 marks each)**

1. Explain the four features of OOP named in the syllabus — class, object,
   inheritance and polymorphism — giving a short C++ code fragment for each. <span class="marks">[8]</span>
2. Write a complete C++ program that defines a base class `Person` with `name`
   and `age`, derives `Teacher` (with subject and salary) and `Student` (with
   faculty and scholarship) from it, uses a virtual function to display the
   details of each, and prints the total monthly payment for an array of three
   base-class pointers. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** Definition + fragment for each of the four, as in §5.2: the class/object
fragment from `Student`, `class Teacher : public Person` for inheritance, the
overloaded `volume()` and the virtual `earning()` for the two kinds of
polymorphism. One mark for each definition, one for each fragment.

**2.** The complete program and its verified output are given at the end of
§5.2.6. Marking usually goes: class definitions with correct access specifiers
(2), constructors with an initialisation list or assignment (2), `virtual`
function correctly overridden (2), array of base pointers and the loop (1),
correct total and output format (1). The total for the data used is
Rs 48,500 + Rs 1,200 + Rs 52,000 = **Rs 1,01,700**.
:::

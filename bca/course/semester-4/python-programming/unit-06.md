---
subject: Python Programming
grade: BCA Semester 4
unit: 6
title: Object-Oriented Programming in Python
hours: 7
area: BCA 254 · Python Programming · Unit 6
---

When a program grows beyond a few hundred lines, scattered variables and functions become hard to manage. **Object-oriented programming (OOP)** bundles data and the functions that work on it into *objects*. You met OOP with Java in Semester II; here is how Python does it, with less ceremony and a few surprises.

::: key What this unit gives you
- Classes, objects, `__init__`, instance and class attributes, methods.
- Encapsulation conventions, properties.
- Inheritance, `super()`, polymorphism, abstract classes.
- Special ("dunder") methods and operator overloading; dataclasses; composition.
:::

## 6.1 Classes and objects

A **class** is a blueprint; an **object** (instance) is something built from it. `__init__` is the initialiser, called when an object is created; `self` is the object being worked on (always the first parameter of an instance method).

```python
class Student:
    college = "Patan Multiple Campus"          # class attribute (shared)

    def __init__(self, name, roll):
        self.name = name                       # instance attributes
        self.roll = roll
        self.marks = []

    def add_mark(self, m):
        self.marks.append(m)

    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0.0

s1, s2 = Student("Sita", 1), Student("Ram", 2)
for m in (80, 90, 70):
    s1.add_mark(m)
print(s1.name, s1.average(), s2.average(), s1.college is s2.college)
Student.college = "Thapathali Campus"
print(s2.college, type(s1), isinstance(s1, Student))
```
```output
Sita 80.0 0.0 True
Thapathali Campus <class '__main__.Student'> True
```
**Instance attributes** belong to one object; **class attributes** are shared by all. Python has no declarations: an attribute exists once assigned. Methods are ordinary functions stored in the class; `s1.average()` is shorthand for `Student.average(s1)`.

```python
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1
    @classmethod
    def how_many(cls):
        return cls.count
    @staticmethod
    def is_even(n):
        return n % 2 == 0

a, b, c = Counter(), Counter(), Counter()
print(Counter.how_many(), Counter.is_even(7), c.count)
```
```output
3 False 3
```
A **class method** receives the class (`cls`); a **static method** receives neither and is just a function in the class's namespace.

## 6.2 Encapsulation

Python has no `private` keyword; it relies on convention:

- `_name`: "internal; please don't touch" (a single underscore).
- `__name`: **name mangling**: stored as `_ClassName__name` to avoid accidental clashes in subclasses (not true privacy).

A **property** lets you keep a clean attribute-style interface while controlling access:

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

    def deposit(self, amount):
        self.balance += amount

acct = Account("Ram", 100)
acct.deposit(50)
print(acct.balance)
try:
    acct.balance = -5
except ValueError as e:
    print("rejected:", e)
print(sorted(k for k in vars(acct)))
```
```output
150
rejected: balance cannot be negative
['_balance', 'owner']
```
## 6.3 Inheritance and polymorphism

A subclass inherits attributes and methods of its parent and can **override** them. `super()` calls the parent's version.

```python
class Employee:
    def __init__(self, name, base):
        self.name, self.base = name, base
    def pay(self):
        return self.base
    def __str__(self):
        return f"{type(self).__name__}({self.name}, pay={self.pay()})"

class Manager(Employee):
    def __init__(self, name, base, bonus):
        super().__init__(name, base)
        self.bonus = bonus
    def pay(self):
        return super().pay() + self.bonus

class Intern(Employee):
    def pay(self):
        return self.base * 0.5

staff = [Employee("Hari", 40000), Manager("Gita", 60000, 15000), Intern("Bikash", 20000)]
for p in staff:
    print(p)
print(sum(p.pay() for p in staff), isinstance(staff[1], Employee), issubclass(Intern, Employee))
print(Manager.__mro__[1].__name__, [c.__name__ for c in Manager.__mro__])
```
```output
Employee(Hari, pay=40000)
Manager(Gita, pay=75000)
Intern(Bikash, pay=10000.0)
125000.0 True True
Employee ['Manager', 'Employee', 'object']
```
**Polymorphism**: the loop calls `p.pay()` and each object responds according to its own class, with no `if` on the type. Python is **duck-typed**: "if it walks like a duck and quacks like a duck, it is a duck"; any object with a `pay()` method would work. **Multiple inheritance** is allowed (`class C(A, B)`); the **method resolution order (MRO)** decides which parent is searched first (`C.__mro__`).

### Abstract classes

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self): ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return math.pi * self.r ** 2

class Rect(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h

print([round(s.area(), 2) for s in (Circle(1), Rect(3, 4))])
try:
    Shape()
except TypeError as e:
    print("TypeError:", e)
```
```output
[3.14, 12]
TypeError: Can't instantiate abstract class Shape without an implementation for abstract method 'area'
```
An abstract class cannot be instantiated until subclasses implement every abstract method.

## 6.4 Special methods and operator overloading

Methods with double underscores let your objects work with built-in syntax.

| Method | Called by |
|---|---|
| `__init__`, `__del__` | creation, destruction |
| `__str__`, `__repr__` | `str(x)` / `print`, `repr(x)` (debugging) |
| `__len__`, `__getitem__`, `__iter__`, `__contains__` | `len`, `x[i]`, `for`, `in` |
| `__add__`, `__sub__`, `__mul__`, `__eq__`, `__lt__` | `+ - * == <` |
| `__call__`, `__enter__`/`__exit__` | `obj()`, `with obj:` |

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def __len__(self):
        return 2

v, w = Vector(3, 4), Vector(1, 2)
print(v + w, v * 3, abs(v), v == Vector(3, 4), len(v))
```
```output
Vector(4, 6) Vector(9, 12) 5.0 True 2
```
## 6.5 Dataclasses and composition

Boilerplate classes that just hold data are quicker with `@dataclass`, which writes `__init__`, `__repr__` and `__eq__` for you.

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Course:
    code: str
    credits: int = 3
    topics: list = field(default_factory=list, compare=False)

c1, c2 = Course("BCA 251", 3), Course("BCA 256", 2)
c1.topics.append("deadlocks")
print(c1, c1 == Course("BCA 251", 3), sorted([c1, c2])[0].code)
```
```output
Course(code='BCA 251', credits=3, topics=['deadlocks']) True BCA 251
```
**Composition** ("has-a") builds objects from other objects; it is often a better choice than inheritance ("is-a") when the relationship is not truly a specialisation. A `Library` has a list of `Book` objects; a `Car` has an `Engine`.

```python
class Book:
    def __init__(self, title, copies):
        self.title, self.copies = title, copies

class Library:
    def __init__(self):
        self.books = {}
    def add(self, title, copies=1):
        book = self.books.setdefault(title, Book(title, 0))
        book.copies += copies
    def lend(self, title):
        book = self.books.get(title)
        if not book or book.copies == 0:
            return False
        book.copies -= 1
        return True

lib = Library()
lib.add("SICP", 2)
print([lib.lend("SICP") for _ in range(3)], lib.lend("Missing"), lib.books["SICP"].copies)
```
```output
[True, True, False] False 0
```
## 6.6 Seeing the ideas: one mould, many objects

Object-oriented programming asks you to describe a kind of thing once and then make as many of them as you need. The photograph shows the oldest picture of that idea, a metal cutter that stamps out any number of identical cookies. The figures then show a class and its subclass, the order in which Python searches parent classes, and the special methods that make `+` and `print` work on your own objects.

```photogrid label="6.1" cols="2" ratio="1.0" caption="Class and object. (a) A real tin cookie cutter in the shape of an animal. The cutter is the class: it fixes the shape (the attributes and behaviour that every object has). Each cookie it stamps is an object: same shape, but its own dough, its own decoration (its own values). (b) The same idea in Python: Student is written once, and each call Student(...) builds a new object with its own name and marks."
@ photo id="bca254/cutter" cap="A tin cookie cutter: the class"
fit 1.0
focus 0.5 0.62
call 0.45 0.65 0.04 0.9 "one mould"
@ svg cap="One class, three objects"
f = Fig(300, 300)
f.box(60, 8, 180, 84, "", fill=BLUE, stroke=NAVY)
f.text(150, 26, "class Student", size=14, color=NAVY, bold=True)
f.text(150, 48, "name, marks", size=12, color=SLATE)
f.text(150, 68, "grade(), show()", size=12, color=SLATE)
data = [("Ram", 72), ("Sita", 88), ("Hari", 55)]
for i, (n, m) in enumerate(data):
    x = 8 + i * 98
    f.box(x, 150, 88, 100, "", fill=MINT, stroke=TEAL)
    f.text(x + 44, 170, f"s{i + 1}", size=14, color=TEAL, bold=True)
    f.text(x + 44, 196, f"'{n}'", size=13, color=SLATE, bold=True)
    f.text(x + 44, 220, str(m), size=13, color=SLATE, bold=True)
    f.arrow([(x + 44, 148), (150 + (i - 1) * 40, 94)], color=TEAL, sw=1.4, dash=True)
f.text(150, 276, "Student('Ram', 72) builds s1", size=12, color=NAVY, bold=True)
```

```svgfig label="6.1" caption="A class diagram in UML style. Each box has three parts: the class name, its attributes (data) and its methods (behaviour). The arrow points from the subclass SavingsAccount to the parent class Account and reads 'is a'. The subclass inherits every attribute and method of the parent and adds its own (interest_rate and add_interest). The leading underscore on _balance is the Python convention for 'internal: do not touch from outside'."
f = Fig(580, 216)
def cls(x, y, w, name, attrs, meths, fill, stroke):
    h = 30 + 17 * len(attrs) + 17 * len(meths) + 8
    f.box(x, y, w, h, "", fill=fill, stroke=stroke)
    f.text(x + w / 2, y + 15, name, size=12, color=stroke, bold=True)
    f.line(x, y + 28, x + w, y + 28, color=stroke, sw=1)
    yy = y + 30 + 17 * len(attrs) + 4
    f.line(x, yy, x + w, yy, color=stroke, sw=1)
    for i, a in enumerate(attrs):
        f.text(x + 8, y + 42 + i * 17, a, size=10, color=SLATE, anchor="start")
    for i, m in enumerate(meths):
        f.text(x + 8, yy + 13 + i * 17, m, size=10, color=SLATE, anchor="start")
cls(20, 8, 220, "Account", ["owner: str", "_balance: float"], ["deposit(amount)", "withdraw(amount)", "__str__()"], BLUE, NAVY)
cls(330, 100, 240, "SavingsAccount", ["interest_rate: float"], ["add_interest()", "withdraw(amount)   # overridden"], MINT, TEAL)
f.arrow([(450, 100), (450, 60), (242, 60)], color=NAVY, sw=1.6)
f.text(350, 52, "is a", size=10.5, color=NAVY, bold=True)
f.text(20, 160, "SavingsAccount inherits owner, _balance,", size=10, color=SLATE, anchor="start")
f.text(20, 176, "deposit and __str__; it adds interest_rate,", size=10, color=SLATE, anchor="start")
f.text(20, 192, "add_interest and its own version of withdraw.", size=10, color=SLATE, anchor="start")
```

```svgfig label="6.2" caption="Method resolution order (MRO) in diamond inheritance. D inherits from B and C, and both inherit from A. Python builds one linear search order with the C3 rule, shown by the cell from the real D.__mro__: D, then B, then C, then A, then object. A call to super() inside a method means 'the next class in this list', not simply 'the parent', which is why every class in a diamond runs its code once."
class A:
    def who(self): return "A"
class B(A):
    def who(self): return "B>" + super().who()
class C(A):
    def who(self): return "C>" + super().who()
class D(B, C):
    def who(self): return "D>" + super().who()
mro = [k.__name__ for k in D.__mro__]
f = Fig(580, 188)
pos = {"A": (110, 20), "B": (40, 80), "C": (180, 80), "D": (110, 140)}
for k, (x, y) in pos.items():
    pass
f.box(80, 8, 60, 30, "A", fill=SAND, stroke=AMBER, size=13, bold=True)
f.box(10, 68, 60, 30, "B", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.box(150, 68, 60, 30, "C", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.box(80, 128, 60, 30, "D", fill=MINT, stroke=TEAL, size=13, bold=True)
f.arrow([(40, 68), (96, 40)], color=SLATE); f.arrow([(180, 68), (126, 40)], color=SLATE)
f.arrow([(96, 128), (40, 100)], color=SLATE); f.arrow([(126, 128), (180, 100)], color=SLATE)
f.text(110, 178, "class D(B, C)", size=10.5, color=NAVY, bold=True)
f.text(250, 24, "D.__mro__ (search order):", size=11, color=NAVY, bold=True, anchor="start")
for i, n in enumerate(mro):
    x = 250 + i * 66
    f.box(x, 36, 58, 32, n, fill=MINT if i < 4 else SOFT, stroke=TEAL if i < 4 else SLATE, size=11.5, bold=True)
    if i < len(mro) - 1:
        f.arrow([(x + 59, 52), (x + 65, 52)], color=SLATE, sw=1.4)
f.text(250, 100, "D().who() with super() in each class:", size=11, color=NAVY, bold=True, anchor="start")
f.box(250, 112, 300, 34, D().who(), fill=SAND, stroke=AMBER, size=14, bold=True)
f.text(250, 166, "each class runs once, in MRO order", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="6.3" caption="Special (dunder) methods connect your class to Python's syntax. The cell defines a small Vector class and evaluates each expression for real; the right column is the actual result. Writing __add__ makes + work, __eq__ makes ==, __len__ makes len(), __str__ decides what print shows and __repr__ what the interactive prompt shows."
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, o): return Vector(self.x + o.x, self.y + o.y)
    def __mul__(self, k): return Vector(self.x * k, self.y * k)
    def __eq__(self, o): return (self.x, self.y) == (o.x, o.y)
    def __len__(self): return 2
    def __str__(self): return f"({self.x}, {self.y})"
    def __repr__(self): return f"Vector({self.x}, {self.y})"
a, b = Vector(1, 2), Vector(3, 4)
rows = [("a + b", "__add__", str(a + b)), ("a * 3", "__mul__", str(a * 3)), ("a == Vector(1, 2)", "__eq__", str(a == Vector(1, 2))),
        ("len(a)", "__len__", str(len(a))), ("print(a)", "__str__", str(a)), ("repr(a)", "__repr__", repr(a))]
f = Fig(580, 40 + 30 * len(rows))
f.text(10, 14, "a = Vector(1, 2)     b = Vector(3, 4)", size=11, color=NAVY, bold=True, anchor="start")
for i, (e, m, r) in enumerate(rows):
    y = 28 + i * 30
    f.box(10, y, 190, 26, e, fill=SOFT, stroke=SLATE, size=11, bold=True)
    f.arrow([(202, y + 13), (250, y + 13)], color=SLATE, sw=1.2)
    f.box(252, y, 130, 26, m, fill=BLUE, stroke=NAVY, size=11, bold=True)
    f.arrow([(384, y + 13), (432, y + 13)], color=SLATE, sw=1.2)
    f.box(434, y, 136, 26, r, fill=MINT, stroke=TEAL, size=11, bold=True)
```

### 6.6.1 Eight advantages of object-oriented programming

1. **Models real things naturally.** A `Student`, `Account` or `Book` in the program matches the thing it stands for, with its data and actions in one place. A college system can use one class for a student and another for a course. This makes the design easier to explain to a client.
2. **Encapsulation protects data.** Attributes can be kept internal (a leading underscore) and changed only through methods that check the values. A `withdraw()` method can refuse to make a balance negative. Without this, any line of the program could damage the data.
3. **Reuse through inheritance.** A `SavingsAccount` gets everything of `Account` for free and adds only what is new (Fig. 6.1). The shared code is written and tested once. The weakness is that a deep chain of parent classes becomes hard to follow, so keep hierarchies shallow.
4. **Polymorphism gives flexible code.** The same call, such as `shape.area()`, works on a circle, a square or a triangle, and each object runs its own version. A loop can handle all of them without `if` tests on the type. New shapes can be added without changing the loop.
5. **Easier maintenance.** A change inside one class does not break the others as long as its public methods stay the same. A bug in fee calculation is searched for in the `Fee` class only. This saves time in large programs that live for years.
6. **Many objects, one description.** The class is written once and Plate 6.1 shows how many objects can be made from it, each with its own values. A school can make five hundred `Student` objects from one definition. This keeps the program short and uniform.
7. **Natural for teams and libraries.** Each member can build and test a class, and the group joins them through their public methods. Libraries such as Pandas and Django expose classes (`DataFrame`, `Model`) that you extend. Classes with clear names are also easier for a new member to read.
8. **Operators and built-ins for your own types.** With special methods (Fig. 6.3) your objects can use `+`, `==`, `len()` and `print()`, so `a + b` for two vectors or two money amounts reads like mathematics. This makes the code short and clear. Use it with care: an operator that does something surprising makes the program harder to read.

## Formula and fact sheet

- `class C(Parent):` with `def __init__(self, …)`; `self` is explicit.
- Class attribute shared; instance attribute per object; `@classmethod` gets `cls`; `@staticmethod` gets nothing.
- `_x` convention, `__x` mangled; `@property` for controlled attributes.
- `super().method()`; polymorphism through overriding; duck typing; MRO.
- `__str__`, `__repr__`, `__eq__`, `__add__`, `__len__`…; `@dataclass`.

## Chapter summary

- Classes bundle data and behaviour; objects are instances; `self` and `__init__` are explicit.
- Encapsulation in Python is by convention and properties.
- Inheritance specialises a class, polymorphism lets code treat different objects uniformly, and abstract classes force a common interface.
- Dunder methods integrate your classes with the language; dataclasses and composition keep designs small.

## Practice

1. Define a class `Rectangle` with `area()` and `perimeter()` and test it.
2. Explain the difference between class and instance attributes with a program.
3. Why does the `@property` decorator exist? Show a validated setter.
4. Create `Animal` and `Dog`, `Cat` subclasses that override `speak()`, and call them polymorphically.
5. What is an abstract class and when do you need one?
6. Implement `__add__` and `__str__` for a `Money` class.
7. Compare inheritance and composition with an example of each.

::: note Answers and worked solutions
**1.**

```python
class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h
    def perimeter(self):
        return 2 * (self.w + self.h)

r = Rectangle(3, 5)
print(r.area(), r.perimeter())
```
```output
15 16
```
**2.**

```python
class A:
    shared = []
    def __init__(self, tag):
        self.tag = tag
a, b = A("x"), A("y")
a.shared.append(1)
print(b.shared, a.tag, b.tag)
```
```output
[1] x y
```
`shared` is one list for all instances; `tag` is separate for each.
**3.** A property keeps attribute syntax while running code (validation, computed values); the Section 6.2 `Account` shows a setter that rejects negative balances.
**4.**

```python
class Animal:
    def speak(self): return "..."
class Dog(Animal):
    def speak(self): return "Woof"
class Cat(Animal):
    def speak(self): return "Meow"
print([a.speak() for a in (Dog(), Cat(), Animal())])
```
```output
['Woof', 'Meow', '...']
```
**5.** A class that defines methods subclasses must implement (marked `@abstractmethod`) and cannot be instantiated itself; use it to enforce a common interface, such as `Shape.area()`.
**6.**

```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __add__(self, other):
        return Money(self.amount + other.amount)
    def __str__(self):
        return f"NPR {self.amount:,.2f}"
print(Money(1500) + Money(250.5))
```
```output
NPR 1,750.50
```
**7.** Inheritance models "is-a": `Manager` is an `Employee`. Composition models "has-a": a `Library` has `Book`s, a `Car` has an `Engine`. Prefer composition when the relationship is not a true specialisation, since it is more flexible and avoids deep hierarchies.
:::

## Model answers (5 and 10 marks)

**Q1. Explain class, object, constructor and `self` in Python with a program. (5 marks)**

A **class** is a blueprint that defines the attributes (data) and methods (functions) of a kind of object. An **object** (instance) is one thing made from the class; it has its own attribute values (Plate 6.1). Objects are created by calling the class, `Student("Ram", 72)`.

The **constructor** is the special method `__init__(self, ...)`, which Python calls automatically when an object is created; it sets the starting values. The parameter **`self`** is the object on which the method is running; Python passes it automatically, so `s.show()` means `Student.show(s)`. Attributes made with `self.name = name` belong to the object (**instance attributes**), while a variable written in the class body, such as `school = "TU"`, is shared by all objects (**class attribute**).

```python
class Student:
    school = "TU"
    count = 0

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        Student.count += 1

    def grade(self):
        return "Pass" if self.marks >= 40 else "Fail"

    def __str__(self):
        return f"{self.name} ({self.marks}) {self.grade()}"

s1, s2 = Student("Ram", 72), Student("Hari", 35)
print(s1)
print(s2, "|", Student.count, s1.school is s2.school)
```
```output
Ram (72) Pass
Hari (35) Fail | 2 True
```
**Q2. Explain encapsulation and access control in Python. How does a property help? (5 marks)**

**Encapsulation** means keeping data and the code that works on it together, and hiding the internal detail so that outside code can use the object only through its public methods. Python has no strict `private` keyword and relies on naming conventions.

- **Public** `name`: free to use.
- **Protected** `_name`: a single underscore means "internal, do not use from outside".
- **Private** `__name`: a double underscore triggers **name mangling**; the attribute is stored as `_Class__name`, which prevents accidental clashes in subclasses, but it can still be reached by that long name.

A **property** lets you keep the simple syntax `acc.balance` while running code, for example validation, on every read or write. `@property` defines the getter and `@balance.setter` defines the setter.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = 0
        self.balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self.__balance = value

a = Account("Sita", 500)
a.balance += 250
print(a.balance, sorted(k for k in vars(a)))
try:
    a.balance = -1
except ValueError as e:
    print("ValueError:", e)
```
```output
750 ['_Account__balance', 'owner']
ValueError: balance cannot be negative
```
The output shows the mangled name `_Account__balance`, proving that the data is hidden by convention and not locked.

**Q3. What is inheritance? Explain its types, method overriding, `super()` and polymorphism with a program, and compare the types of inheritance. (10 marks)**

**Introduction.** **Inheritance** lets a new class (the **subclass** or child) take over the attributes and methods of an existing class (the **superclass** or parent) and add or change some of them. It models an "is a" relationship, as `SavingsAccount` **is an** `Account` (Fig. 6.1), and it gives reuse of code. **Polymorphism** ("many forms") means that one call can behave differently depending on the object that receives it.

**Syntax.** `class Child(Parent):`. A child can **override** a method by defining one with the same name. `super()` gives access to the next class in the method resolution order, so `super().__init__(...)` runs the parent constructor and `super().withdraw(x)` reuses the parent's method.

**Types of inheritance.**

1. **Single:** one parent, one child.
2. **Multilevel:** a chain, grandparent to parent to child.
3. **Hierarchical:** one parent with several children.
4. **Multiple:** a child with two or more parents; Python searches them in the **MRO** (Fig. 6.2), which you can print with `Class.__mro__`.
5. **Hybrid:** a combination, such as the diamond.

**Polymorphism** in Python works through overriding and **duck typing**: any object that has the needed method can be used, whatever its class.

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return round(3.14159 * self.r ** 2, 2)

class Square(Rectangle):
    def __init__(self, s):
        super().__init__(s, s)

shapes = [Rectangle(3, 4), Circle(2), Square(5)]
print([s.area() for s in shapes])
print(isinstance(shapes[2], Rectangle), issubclass(Square, Shape))
```
```output
[12, 12.57, 25]
True True
```
**Comparison.**

| Type | Parents | Example | Main risk |
|---|---|---|---|
| Single | 1 | `Square(Rectangle)` | none |
| Multilevel | chain | `C(B)`, `B(A)` | long chains are hard to follow |
| Hierarchical | 1 parent, many children | `Circle`, `Rectangle` from `Shape` | parent change affects all |
| Multiple | 2 or more | `D(B, C)` | ambiguity, solved by the MRO |
| Hybrid | mixed | the diamond | complexity |

**Advantages:** reuse, a natural hierarchy, and polymorphic code; **disadvantages:** tight coupling between parent and child, and deep hierarchies. Prefer **composition** ("has a") when "is a" does not fit.

**Conclusion.** Inheritance and polymorphism let one loop work on many kinds of objects; use them with shallow hierarchies and a clear "is a" relationship.

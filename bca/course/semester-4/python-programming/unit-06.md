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

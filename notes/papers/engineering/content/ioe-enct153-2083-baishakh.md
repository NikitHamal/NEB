---
file: NEBians-IOE-Past-Paper-Advanced-Computer-Programming-ENCT153-2083-Baishakh.pdf
subject: Advanced Computer Programming
level: BE · Year I / Part II
code: ENCT 153
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Explain different programming paradigms with examples. Which one is Python based on and why? [[2+2]]

@q 2
What are application areas of Python in electrical engineering? Mention features of Python. [[2+2]]

@q 3
Explain comparison operators with examples. Write a Python program using loop and conditional statements to check whether a number is prime or not. [[2+4]]

@q 4
What is lambda function? Write a Python program using lambda function to filter even numbers from a list. [[2+3]]

@q 5
Explain the use of set, dictionary, list and tuples data types in Python with examples. [[5]]

@q 6
What is the purpose of the `__init__()` method in Python classes? Write a Python program to declare class student with attributes name, roll, marks and method to display student details. Create an object of student and display the student details. [[2+4]]

@q 7
Explain the concept of inheritance. Show single, multiple, hierarchical and multi-level inheritance in Python with suitable example. [[2+4]]

@q 8
Define operator overloading. Overload binary operators (+ and −) to calculate the sum, difference of two vectors. Use class as Vector with attributes x and y. [[2+4]]

@q 9
Differentiate between syntax error and exception with examples. Write a Python program to define a custom exception class. [[2+4]]

@q 10
What is NumPy? Explain how to create, slice and reshape NumPy arrays with examples. [[1+3]]

@q 11
What are Python modules, packages and libraries? What are the common ways of importing a module? [[1+3]]

@q 12
Describe how NumPy can be used to calculate basic statistical measures such as mean, median, standard deviation and variance with example. [[4]]
<!-- SOLUTIONS -->

@s 1
A **programming paradigm** is a style or way of organising a program: it decides how the problem is broken up and how the code expresses the solution. The main paradigms are:

| Paradigm | Idea | Example languages | Example |
|---|---|---|---|
| **Procedural** | A program is a sequence of instructions grouped into procedures (functions) that operate on data | C, Pascal, Python | `def area(r): return 3.14*r*r` |
| **Object oriented (OOP)** | Data and the functions that work on it are bundled into objects created from classes; uses encapsulation, inheritance, polymorphism | Java, C++, Python | `class Car:` with `drive()` |
| **Functional** | Computation is the evaluation of (pure) functions; avoids changing state; functions are values | Haskell, Lisp, Python | `list(map(lambda x: x*x, [1,2,3]))` |
| **Imperative** | Explicit statements that change the program state step by step | C, Python | `total = 0; total += 5` |
| **Declarative / logic** | State *what* result is wanted, not how to get it | SQL, Prolog | `SELECT * FROM student` |
| **Event driven** | Flow of the program is decided by events (clicks, sensor input, messages) | JavaScript, Python (Tkinter) | `button.bind("<Click>", handler)` |

**Python is a multi-paradigm language.** It is primarily **object-oriented** (everything, even an integer or a function, is an object; classes, inheritance and polymorphism are built in) and it is also **procedural/imperative** (scripts made of statements and functions) and supports **functional** features (`lambda`, `map`, `filter`, `reduce`, comprehensions, generators). The reason is that this flexibility lets the programmer choose the simplest style for each problem: quick scripts in procedural style, large systems with classes, data processing in a functional style.

@s 2
**Application areas of Python in electrical engineering**

- **Circuit and power-system analysis:** solving network equations with NumPy/SciPy, load-flow, short-circuit and stability studies (PyPSA, pandapower), transient simulation of RLC circuits with `scipy.integrate`.
- **Signal processing and communication:** filtering, FFT, modulation studies (`scipy.signal`, `numpy.fft`), software-defined radio (GNU Radio).
- **Control systems:** transfer functions, Bode/Nyquist/root-locus and PID tuning (`python-control`).
- **Embedded systems and IoT:** MicroPython, Raspberry Pi, Arduino interfacing, sensor reading and data logging (`pyserial`, `RPi.GPIO`).
- **Instrument automation and measurement:** controlling oscilloscopes and multimeters over GPIB/USB (PyVISA), automated testing.
- **Machine learning for energy systems:** load forecasting, fault classification, smart-grid analytics (scikit-learn, TensorFlow).
- **Data visualisation and reports:** plots of waveforms and results with Matplotlib, pandas for measured data.
- **Scripting EDA tools:** automation in KiCad, SPICE (PySpice), FPGA verification (cocotb).

**Features of Python**

1. Simple, readable syntax (indentation marks blocks), easy to learn.
2. **Interpreted** and interactive (REPL), so code is tested line by line.
3. **Dynamically typed**: no declaration of variable types.
4. **Object oriented**, procedural and functional (multi-paradigm).
5. **Portable / cross-platform** (Windows, Linux, macOS) and free and open source.
6. **Large standard library** and a huge third-party ecosystem (NumPy, SciPy, Matplotlib, pandas).
7. Automatic memory management (garbage collection); built-in high-level data types (list, dict, set, tuple).
8. **Extensible and embeddable**: C/C++ code can be called from Python, and Python can be embedded in applications.
9. Exception handling, modules and packages for large programs.

@s 3
**Comparison (relational) operators** compare two values and give a Boolean result (`True` or `False`).

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | equal to | `5 == 5` | `True` |
| `!=` | not equal to | `5 != 3` | `True` |
| `>` | greater than | `3 > 7` | `False` |
| `<` | less than | `3 < 7` | `True` |
| `>=` | greater than or equal to | `7 >= 7` | `True` |
| `<=` | less than or equal to | `8 <= 7` | `False` |

Python also allows chained comparison: `1 < x < 10` is `True` when $1 < x$ and $x < 10$. Comparisons are used in `if` and `while` conditions; `==` compares values, while the assignment operator is `=`.

**Program to check whether a number is prime.** A prime is an integer $n>1$ whose only divisors are 1 and $n$. It is enough to test divisors from 2 up to $\sqrt{n}$.

```python
n = int(input("Enter a number: "))

if n <= 1:
    print(n, "is not a prime number")
else:
    is_prime = True
    i = 2
    while i * i <= n:          # test divisors up to sqrt(n)
        if n % i == 0:         # found a divisor
            is_prime = False
            break
        i += 1
    if is_prime:
        print(n, "is a prime number")
    else:
        print(n, "is not a prime number")
```

*Sample runs:* input `29` prints `29 is a prime number`; input `15` prints `15 is not a prime number` (15 % 3 == 0); input `1` prints `1 is not a prime number`. The loop executes at most $\sqrt{n}$ times.

@s 4
A **lambda function** is a small *anonymous* function defined in one line with the keyword `lambda`: `lambda arguments: expression`. It can take any number of arguments but contains only one expression, whose value is returned automatically. It is usually used where a short function is needed once, e.g. as argument of `filter()`, `map()` or `sorted()`.

```python
square = lambda x: x * x
print(square(5))                 # 25
```

**Program: filter even numbers from a list using lambda**

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

even = list(filter(lambda x: x % 2 == 0, numbers))

print("Original list:", numbers)
print("Even numbers :", even)
```

*Output*

```
Original list: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Even numbers : [2, 4, 6, 8, 10, 12]
```

`filter(function, iterable)` keeps those items for which the lambda returns `True` (`x % 2 == 0`); `list()` converts the filter object to a list.

@s 5
Python has four built-in collection types:

| Type | Syntax | Ordered | Mutable | Duplicates | Typical use |
|---|---|---|---|---|---|
| **List** | `[1, 2, 3]` | yes (indexed) | yes | allowed | general sequence of items that changes |
| **Tuple** | `(1, 2, 3)` | yes (indexed) | **no** | allowed | fixed records, coordinates, dictionary keys |
| **Set** | `{1, 2, 3}` | no | yes (items are unique) | **not** allowed | removing duplicates, membership tests, set algebra |
| **Dictionary** | `{"a": 1}` | insertion ordered (3.7+) | yes | keys unique | key-value lookup (a table of records) |

```python
# List - ordered, changeable
marks = [70, 85, 90]
marks.append(60)            # [70, 85, 90, 60]
marks[0] = 75               # [75, 85, 90, 60]
print(marks, len(marks))    # [75, 85, 90, 60] 4

# Tuple - ordered, unchangeable
point = (3, 4)
x, y = point                # unpacking: x = 3, y = 4
# point[0] = 5              # TypeError: tuple does not support item assignment

# Set - unique, unordered, supports set algebra
a = {1, 2, 3, 3, 2}         # {1, 2, 3}
b = {3, 4}
print(a | b, a & b, a - b)  # {1, 2, 3, 4} {3} {1, 2}

# Dictionary - key: value pairs
student = {"name": "Sita", "roll": 7}
student["marks"] = 88       # add a new key
print(student["name"])      # Sita
for k, v in student.items():
    print(k, v)
```

A list is used when the data change, a tuple when it must stay fixed (and it is hashable and faster), a set when uniqueness and fast membership matter ($O(1)$ average), and a dictionary when items are found by a name (key) instead of a position.

@s 6
**Purpose of `__init__()`.** `__init__()` is the **constructor** (initializer) of a Python class. It is called automatically when an object is created (`Student(...)`) and is used to give the new object its initial attribute values. Its first parameter, `self`, refers to the object being created, so `self.name = name` stores the data in that object. Without it every object would have to be filled in by separate statements.

**Program**

```python
class Student:
    def __init__(self, name, roll, marks):
        self.name = name          # attributes
        self.roll = roll
        self.marks = marks

    def display(self):            # method to display details
        print("Name :", self.name)
        print("Roll :", self.roll)
        print("Marks:", self.marks)


s1 = Student("Ram Thapa", 12, 85.5)   # object creation calls __init__
s1.display()
```

*Output*

```
Name : Ram Thapa
Roll : 12
Marks: 85.5
```

@s 7
**Inheritance** is the mechanism by which a new class (the **child / derived / sub class**) acquires the attributes and methods of an existing class (the **parent / base / super class**) and can add or override them. It gives **code reuse**, a natural is-a hierarchy and makes polymorphism possible. Syntax: `class Child(Parent):`.

```python
# 1. Single inheritance: one parent, one child
class Person:
    def __init__(self, name):
        self.name = name
    def show(self):
        print("Name:", self.name)

class Student(Person):                 # Student -> Person
    def study(self):
        print(self.name, "is studying")

# 2. Multiple inheritance: one child, two (or more) parents
class Father:
    def skill(self):
        print("Father: driving")

class Mother:
    def talent(self):
        print("Mother: singing")

class Child(Father, Mother):           # Child -> Father, Mother
    pass

# 3. Hierarchical inheritance: several children, one parent
class Animal:
    def eat(self):
        print("Animal eats")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

class Cat(Animal):
    def meow(self):
        print("Cat meows")

# 4. Multilevel inheritance: grandparent -> parent -> child
class Vehicle:
    def move(self):
        print("Vehicle moves")

class Car(Vehicle):
    def drive(self):
        print("Car is driven")

class SportsCar(Car):
    def speed(self):
        print("Sports car is fast")


s = Student("Hari"); s.show(); s.study()
c = Child(); c.skill(); c.talent()
d = Dog(); d.eat(); d.bark()
k = Cat(); k.eat(); k.meow()
sc = SportsCar(); sc.move(); sc.drive(); sc.speed()
```

*Output*

```
Name: Hari
Hari is studying
Father: driving
Mother: singing
Animal eats
Dog barks
Animal eats
Cat meows
Vehicle moves
Car is driven
Sports car is fast
```

| Type | Structure |
|---|---|
| Single | Person ← Student |
| Multiple | Father, Mother ← Child |
| Hierarchical | Animal ← Dog, Animal ← Cat |
| Multilevel | Vehicle ← Car ← SportsCar |

In multiple inheritance Python searches the parents in the **method resolution order** (`Child.__mro__`), left to right.

@s 8
**Operator overloading** means giving an operator an additional meaning for objects of a user-defined class, so that `a + b` works on objects as it does on numbers. In Python the operator calls a special ("magic" or dunder) method: `+` calls `__add__`, `-` calls `__sub__`, `*` calls `__mul__`, `==` calls `__eq__`, and so on. The meaning of the operator is changed but not its precedence or number of operands.

For vectors $\vec{a} = (x_1, y_1)$ and $\vec{b} = (x_2, y_2)$:

$$\begin{gathered}\vec{a}+\vec{b} = (x_1 + x_2,\ y_1 + y_2) \\ \vec{a}-\vec{b} = (x_1 - x_2,\ y_1 - y_2)\end{gathered}$$

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):                 # overloads +
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):                 # overloads -
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):                        # how print() shows the vector
        return f"({self.x}, {self.y})"


v1 = Vector(3, 4)
v2 = Vector(1, 2)

print("v1 =", v1)
print("v2 =", v2)
print("v1 + v2 =", v1 + v2)
print("v1 - v2 =", v1 - v2)
```

*Output*

```
v1 = (3, 4)
v2 = (1, 2)
v1 + v2 = (4, 6)
v1 - v2 = (2, 2)
```

`v1 + v2` is translated by Python into `v1.__add__(v2)`, which builds and returns a new `Vector`.

@s 9
| Point | Syntax error | Exception |
|---|---|---|
| When | Detected **before** the program runs, while the source is parsed | Occurs **during execution** of syntactically correct code |
| Cause | Violation of the grammar of the language (missing colon, bracket, wrong indentation) | Illegal operation or situation at run time (division by zero, bad index, missing file) |
| Handling | Cannot be caught; the code must be corrected | Can be handled with `try ... except` |
| Effect | The program does not start | The program stops at that statement if not handled |
| Example | `if x > 5` (missing `:`) gives `SyntaxError: expected ':'` | `10 / 0` gives `ZeroDivisionError`; `int("abc")` gives `ValueError`; `lst[10]` gives `IndexError` |

```python
# syntax error (program will not run)
# print("Hello"          -> SyntaxError: '(' was never closed

# exception, handled
try:
    a = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

**Custom exception class.** A user-defined exception is a class derived from `Exception`. It is raised with `raise` and caught with `except`.

```python
class NegativeAgeError(Exception):
    """Raised when the age entered is negative."""
    def __init__(self, age, message="Age cannot be negative"):
        self.age = age
        self.message = message
        super().__init__(f"{message}: {age}")


def check_age(age):
    if age < 0:
        raise NegativeAgeError(age)
    print("Valid age:", age)


try:
    check_age(25)
    check_age(-5)
except NegativeAgeError as e:
    print("Error ->", e)
```

*Output*

```
Valid age: 25
Error -> Age cannot be negative: -5
```

@s 10
**NumPy** (Numerical Python) is the fundamental Python library for scientific computing. It provides the **`ndarray`**, a fast, fixed-type, N-dimensional array, together with vectorised mathematical functions, linear algebra, Fourier transforms and random numbers. NumPy arrays are much faster and more compact than Python lists because the data are stored in one contiguous block and the loops run in C.

**Creating arrays**

```python
import numpy as np

a = np.array([1, 2, 3, 4])            # from a list         -> [1 2 3 4]
b = np.array([[1, 2, 3], [4, 5, 6]])  # 2-D array (2 x 3)
z = np.zeros((2, 3))                  # 2 x 3 of 0.0
o = np.ones((2, 2))                   # 2 x 2 of 1.0
r = np.arange(0, 10, 2)               # [0 2 4 6 8]
l = np.linspace(0, 1, 5)              # [0.   0.25 0.5  0.75 1.  ]
print(b.shape, b.ndim, b.dtype)       # (2, 3) 2 int64
```

**Slicing** uses `array[start:stop:step]` for each axis (stop is excluded):

```python
m = np.arange(12).reshape(3, 4)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
print(m[1, :])        # second row         -> [4 5 6 7]
print(m[:, 2])        # third column       -> [ 2  6 10]
print(m[0:2, 1:3])    # sub-matrix         -> [[1 2]
                      #                        [5 6]]
print(m[::2, ::2])    # every second item  -> [[ 0  2]
                      #                        [ 8 10]]
```

**Reshaping** changes the shape without changing the data; the number of elements must stay the same (`-1` lets NumPy compute one dimension):

```python
a = np.arange(12)              # [ 0  1 ... 11]
b = a.reshape(3, 4)            # 3 x 4
c = a.reshape(2, 2, 3)         # 3-D
d = b.reshape(-1)              # flattened back to 1-D (12,)
e = a.reshape(4, -1)           # 4 x 3
print(b.shape, c.shape, e.shape)   # (3, 4) (2, 2, 3) (4, 3)
```

@s 11
- A **module** is a single Python file (`.py`) that contains definitions (functions, classes, variables) and can be imported and reused, e.g. `math.py`, or a file `mytools.py` written by the user.
- A **package** is a directory of modules (with an `__init__.py` file) that groups related modules in a namespace, e.g. `numpy`, `os.path`, or `shop/` containing `billing.py` and `stock.py`, used as `import shop.billing`.
- A **library** is a collection of modules and packages that provide ready-made functionality for a domain, e.g. the Python standard library, NumPy, Matplotlib, pandas.

**Common ways of importing a module** (taking `math` as example)

| Form | Example | Use |
|---|---|---|
| import the whole module | `import math` then `math.sqrt(16)` | names stay in the module namespace (safest) |
| import with an alias | `import numpy as np` then `np.array([1, 2])` | shorter names |
| import specific names | `from math import sqrt, pi` then `sqrt(16)` | use names directly |
| import all names | `from math import *` | brings every public name in; discouraged (name clashes) |
| import a module from a package | `from os import path` or `import os.path` | submodule access |
| dynamic import | `importlib.import_module("math")` | module name known only at run time |

```python
import math
from math import sqrt, pi
import numpy as np

print(math.factorial(5))   # 120
print(sqrt(81))            # 9.0
print(round(pi, 4))        # 3.1416
print(np.sum([1, 2, 3]))   # 6
```

Python looks for a module in the current directory, then in the directories of `sys.path`; third-party libraries are installed with `pip install`.

@s 12
NumPy provides vectorised functions that compute statistics for a whole array in one call. For a data set $x_1,\dots,x_n$:

$$\begin{gathered}\text{mean} = \bar{x} = \frac{1}{n}\sum x_i \\ \text{variance } \sigma^2 = \frac{1}{n}\sum (x_i-\bar{x})^2 \\ \text{std. deviation } \sigma = \sqrt{\sigma^2}\end{gathered}$$

and the **median** is the middle value of the sorted data (the average of the two middle values when $n$ is even). The functions are `np.mean`, `np.median`, `np.var` and `np.std` (all with the optional `axis` argument; the default `ddof=0` is the population formula, `ddof=1` gives the sample formula).

```python
import numpy as np

data = np.array([12, 15, 11, 18, 14, 20, 15])

print("Mean              :", np.mean(data))
print("Median            :", np.median(data))
print("Variance (pop.)   :", np.var(data))
print("Std. deviation    :", np.std(data))
print("Variance (sample) :", np.var(data, ddof=1))
print("Std. dev. (sample):", np.std(data, ddof=1))
```

*Output*

```
Mean              : 15.0
Median            : 15.0
Variance (pop.)   : 8.571428571428571
Std. deviation    : 2.9277002188455996
Variance (sample) : 10.0
Std. dev. (sample): 3.1622776601683795
```

*Check by hand.* Mean $=105/7 = 15$; sorted data $11,12,14,15,15,18,20$ gives median 15; the deviations from the mean are $-3,0,-4,3,-1,5,0$, so $\sum(x_i-\bar x)^2 = 9+0+16+9+1+25+0 = 60$; population variance $=60/7 = 8.571$, $\sigma = 2.928$; sample variance $= 60/6 = 10$, $s = 3.162$.

For a 2-D array, `np.mean(a, axis=0)` gives the column means and `axis=1` the row means.

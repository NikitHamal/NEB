---
file: NEBians-IOE-Past-Paper-Advanced-Computer-Programming-ENCT153-2082-Bhadra.pdf
subject: Advanced Computer Programming
level: BE · Year I / Part II
code: ENCT 153
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Compare object-oriented and functional programming paradigms with examples. List two advantages and disadvantages of imperative programming. [[2+2]]

@q 2
What are top Python implementations? Mention limitations of Python. [[2+2]]

@q 3
Explain logical operators with examples. An electrical engineer collects resistance values (in ohms) from 10 different resistors. Write a Python program to store these values in a list and calculate sum and average using loops and operators. [[2+4]]

@q 4
What is lambda function? How does it differ from a user defined function? Explain with examples. [[5]]

@q 5
Explain the difference between mutable and immutable data types in Python. Write a Python program to create a set and perform union and intersection operations. [[2+3]]

@q 6
Define classes and objects in Python. Write a Python program that represents a rectangle class with attributes length and width. Add methods that return area and perimeter of the rectangle. [[2+4]]

@q 7
How can a Python class be made iterable? Describe the necessary methods to implement and their roles. Give an example of an iterable class. [[2+4]]

@q 8
Explain operator overloading in Python. Create a class Book with "noOfPages" as an attribute. Overload + operator to add two book objects. [[2+4]]

@q 9
Explain exception handling in Python with try-except-finally block. [[1+2]]

@q 10
Explain file handling in Python. Write a Python program to write and read from a binary file. [[1+2]]

@q 11
What are Python modules, packages and libraries? List any three commonly used libraries. [[3+2]]

@q 12
Explain with an example how NumPy arrays are better than Python lists for numerical operations. Use NumPy to create two 2x2 matrices representing current (I) and resistance (R) in a simple electrical network, perform matrix multiplication using V=IR, and output the resulting voltage matrix. [[3+4]]
<!-- SOLUTIONS -->

@s 1
**Object-oriented programming (OOP)** organises a program around *objects*: each object bundles **data (attributes)** with the **functions (methods)** that operate on it. A class is the blueprint; programs are built from interacting objects. Its pillars are encapsulation, abstraction, inheritance and polymorphism, and the state of an object changes as methods run.

**Functional programming (FP)** organises a program as the *evaluation of functions*. Functions are first-class values (they can be passed, returned and stored), data is preferably **immutable**, and functions are **pure**: the same input always gives the same output, with no side effects. Loops are replaced by recursion, `map`, `filter` and `reduce`.

| Point | Object-oriented | Functional |
|---|---|---|
| Basic unit | Object (data + methods) | Function |
| State | Mutable state kept inside objects | Avoids state; data is immutable |
| Side effects | Methods may change the object | Pure functions, no side effects |
| Repetition | Loops, method calls | Recursion, `map`, `filter`, `reduce` |
| Reuse | Inheritance and polymorphism | Function composition, higher-order functions |
| Best for | Large systems with many interacting entities (GUI, simulation, banking) | Data transformation, parallel processing, mathematical computation |
| Languages | Java, C++, Python | Haskell, Lisp, Python (partly) |

*OOP example*

```python
class Counter:
    def __init__(self):
        self.value = 0          # state stored in the object
    def increment(self):
        self.value += 1         # method changes the state

c = Counter()
c.increment(); c.increment()
print(c.value)                  # 2
```

*Functional example*

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, nums))            # [1, 4, 9, 16, 25]
evens = list(filter(lambda x: x % 2 == 0, nums))      # [2, 4]
total = reduce(lambda a, b: a + b, nums)              # 15
print(squares, evens, total)
```

**Imperative programming** describes *how* to reach the result through statements that change the program state step by step (C, Python scripts, assembly).

Two advantages:

1. Simple and close to the way the machine works, so it is easy to learn and to follow step by step.
2. Efficient: direct control over memory and flow gives fast execution, and it is well suited to algorithms such as loops over arrays.

Two disadvantages:

1. Programs with many shared variables and side effects are hard to debug, test and run in parallel (state can be changed anywhere).
2. For large programs the code becomes long and tangled (spaghetti code); reuse and maintenance are poorer than in OOP or functional styles.

@s 2
**Python implementation** means a program (interpreter and runtime) that executes Python code. The language is one, but there are several implementations:

| Implementation | Written in | Notes |
|---|---|---|
| **CPython** | C | The reference and most widely used implementation, from python.org; compiles source to bytecode and runs it on a virtual machine; has the GIL |
| **PyPy** | RPython | Has a **just-in-time (JIT) compiler**, often several times faster than CPython for long-running programs |
| **Jython** | Java | Runs on the Java Virtual Machine and uses Java classes directly (supports Python 2.7 only) |
| **IronPython** | C# | Runs on .NET / CLR and uses .NET libraries |
| **MicroPython / CircuitPython** | C | Small versions for microcontrollers (ESP32, Raspberry Pi Pico), very useful in embedded systems |
| **Stackless Python** | C | CPython fork with lightweight micro-threads (tasklets) |
| **GraalPy, RustPython, Cython** (compiles Python to C) | various | Other implementations and compilers |

**Limitations of Python**

1. **Slower execution** than compiled languages such as C/C++/Java, because it is interpreted and dynamically typed.
2. **High memory use** (every value is an object with overhead), so it is unsuitable for very memory-constrained systems.
3. **Global Interpreter Lock (GIL)** in CPython: only one thread executes Python bytecode at a time, so CPU-bound multithreading does not use several cores (use `multiprocessing`).
4. **Weak for mobile and browser development** and for low-level system or hardware programming.
5. **Dynamic typing causes run-time errors**: type errors show up only when the line runs; this needs more testing.
6. **Database access layers** (e.g. ODBC wrappers) are less mature than in Java or .NET.
7. Indentation-based syntax can cause errors when code is copied between editors.

@s 3
**Logical operators** combine Boolean conditions and give `True` or `False`.

| Operator | Meaning | Example (`a = 7`, `b = 3`) | Result |
|---|---|---|---|
| `and` | `True` only if both operands are true | `a > 5 and b > 5` | `False` |
| `or` | `True` if at least one operand is true | `a > 5 or b > 5` | `True` |
| `not` | reverses the truth value | `not (a > 5)` | `False` |

Truth table:

| A | B | A and B | A or B | not A |
|---|---|---|---|---|
| T | T | T | T | F |
| T | F | F | T | F |
| F | T | F | T | T |
| F | F | F | F | T |

`and` and `or` use *short-circuit evaluation*: in `x != 0 and 10 / x > 1` the division is never evaluated when `x == 0`. They actually return one of the operands: `0 or 5` gives `5`, `3 and 8` gives `8`. Precedence is `not` > `and` > `or`.

```python
age, has_id = 20, True
if age >= 18 and has_id:
    print("Allowed")            # Allowed
print(not has_id)               # False
```

**Program for ten resistors**

```python
resistors = []                                   # empty list
for i in range(10):
    value = float(input(f"Enter resistance {i + 1} (ohm): "))
    resistors.append(value)

total = 0
for r in resistors:                              # sum using a loop
    total += r

average = total / len(resistors)                 # average using operators

print("Resistance values:", resistors)
print("Sum     =", total, "ohm")
print("Average =", round(average, 2), "ohm")
```

*Sample run* with the values `10 22 47 33 15 68 100 4.7 56 12`:

```
Resistance values: [10.0, 22.0, 47.0, 33.0, 15.0, 68.0, 100.0, 4.7, 56.0, 12.0]
Sum     = 367.7 ohm
Average = 36.77 ohm
```

(Sum $=10+22+47+33+15+68+100+4.7+56+12 = 367.7\ \Omega$ and average $=367.7/10 = 36.77\ \Omega$.) The same sum for the series connection of these resistors is the equivalent resistance, 367.7 ohm.

@s 4
A **lambda function** is a small anonymous (nameless) function created with the keyword `lambda`. Syntax:

$$\texttt{lambda arguments : expression}$$

It can take any number of arguments but holds **a single expression**, whose value is returned automatically (no `return` keyword). It is normally used where a short function is needed once, for example as an argument of `map()`, `filter()`, `sorted()`.

**Difference from a user-defined function**

| Lambda function | User-defined function (`def`) |
|---|---|
| Anonymous (can be bound to a name but need not be) | Always has a name |
| Defined with `lambda` | Defined with `def` |
| Only **one expression**; no statements, no assignments, no loops | Any number of statements, loops, `if`, nested functions |
| Result returned implicitly | Needs `return` (otherwise gives `None`) |
| No docstring or type-annotation | Can have docstring and annotations |
| One line, for short throw-away use | Reusable, readable, easy to debug for long logic |

```python
# User defined function
def square(x):
    return x * x

# Equivalent lambda
sq = lambda x: x * x

print(square(6), sq(6))                          # 36 36

add = lambda a, b: a + b
print(add(4, 5))                                 # 9

# Typical use with built-in functions
nums = [3, 8, 1, 6]
print(list(map(lambda n: n ** 2, nums)))         # [9, 64, 1, 36]
print(list(filter(lambda n: n % 2 == 0, nums)))  # [8, 6]
students = [("Ram", 80), ("Sita", 92), ("Hari", 75)]
print(sorted(students, key=lambda s: s[1]))      # [('Hari', 75), ('Ram', 80), ('Sita', 92)]
```

@s 5
**Mutable** objects can be changed in place after creation (their contents change but their identity `id()` stays the same): `list`, `dict`, `set`, `bytearray`. **Immutable** objects cannot be changed after creation; an "update" creates a new object: `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes`.

| | Mutable | Immutable |
|---|---|---|
| Examples | list, dict, set | int, float, str, tuple |
| Change in place | allowed | `TypeError` |
| Hashable (dict key) | no | yes (if all items immutable) |
| Shared references | change is seen through every name | safe, cannot be altered |

```python
a = [1, 2, 3]
b = a                    # same object
a.append(4)
print(b)                 # [1, 2, 3, 4]  (changed in place)

s = "hello"
# s[0] = "H"             # TypeError: 'str' object does not support item assignment
s = "H" + s[1:]          # creates a new string
t = (1, 2, 3)
# t[0] = 9               # TypeError
```

**Program: set, union and intersection**

```python
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7}

print("Set A       :", A)
print("Set B       :", B)
print("Union       :", A | B)                 # also A.union(B)
print("Intersection:", A & B)                 # also A.intersection(B)
```

*Output*

```
Set A       : {1, 2, 3, 4, 5}
Set B       : {4, 5, 6, 7}
Union       : {1, 2, 3, 4, 5, 6, 7}
Intersection: {4, 5}
```

A set holds unique, unordered elements, so duplicates vanish: `set([1, 1, 2])` gives `{1, 2}`.

@s 6
A **class** is a user-defined blueprint (template) that describes the attributes (data) and methods (functions) common to a set of things. An **object** (instance) is a concrete entity created from the class; it has its own copy of the attributes. A class is defined with the `class` keyword and an object is created by calling the class, `obj = ClassName(args)`. `self` is the reference to the current object.

```python
class Rectangle:
    def __init__(self, length, width):
        self.length = length          # attributes
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


r = Rectangle(8, 5)
print("Length    :", r.length)
print("Width     :", r.width)
print("Area      :", r.area())
print("Perimeter :", r.perimeter())
```

*Output*

```
Length    : 8
Width     : 5
Area      : 40
Perimeter : 26
```

Area $= l \times w = 8\times 5 = 40$ and perimeter $= 2(l+w) = 2(8+5) = 26$. Another object `Rectangle(3, 2)` has its own independent attributes.

@s 7
A class is **iterable** if its objects can be used in a `for` loop. This is done by implementing the **iterator protocol**:

| Method | Role |
|---|---|
| `__iter__(self)` | Called by `iter()` / at the start of a `for` loop; must return an **iterator object** (usually `self`) |
| `__next__(self)` | Called by `next()` in every loop step; returns the next item and raises **`StopIteration`** when there are no more items |

(Alternatively, `__iter__` can be written as a generator with `yield`, or the class can define `__getitem__` with integer indices starting at 0.)

```python
class Countdown:
    """Iterable that counts down from start to 1."""
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        self.current = self.start
        return self                      # the object is its own iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration          # signals the end
        value = self.current
        self.current -= 1
        return value


for n in Countdown(5):
    print(n, end=" ")                    # 5 4 3 2 1
print()
print(list(Countdown(3)))                # [3, 2, 1]
```

*Output*

```
5 4 3 2 1 
[3, 2, 1]
```

A `for` loop calls `iter(obj)` once, then `next()` repeatedly until `StopIteration` is raised. Generator version of the same class:

```python
class Countdown2:
    def __init__(self, start):
        self.start = start
    def __iter__(self):
        for i in range(self.start, 0, -1):
            yield i

print(list(Countdown2(4)))               # [4, 3, 2, 1]
```

@s 8
**Operator overloading** means giving an operator (`+`, `-`, `*`, `==`, `<`, ...) a user-defined meaning for objects of a class. Python calls a special ("dunder") method when the operator is used: `a + b` calls `a.__add__(b)`. Common ones: `__add__` (+), `__sub__` (−), `__mul__` (*), `__eq__` (==), `__lt__` (<), `__str__` (printing), `__len__` (len). It makes user-defined types behave like built-in types, so the code reads naturally. The method receives the left operand as `self` and the right operand as `other`, and normally returns a new object.

```python
class Book:
    def __init__(self, noOfPages):
        self.noOfPages = noOfPages

    def __add__(self, other):                  # overloads +
        return Book(self.noOfPages + other.noOfPages)

    def __str__(self):
        return f"Book with {self.noOfPages} pages"


b1 = Book(250)
b2 = Book(180)
b3 = b1 + b2                                   # b1.__add__(b2)
print(b1)
print(b2)
print(b3)
print("Total pages:", b3.noOfPages)
```

*Output*

```
Book with 250 pages
Book with 180 pages
Book with 430 pages
Total pages: 430
```

@s 9
An **exception** is an error that occurs during execution and disrupts the normal flow of the program (e.g. `ZeroDivisionError`, `ValueError`, `FileNotFoundError`). **Exception handling** catches such errors so that the program can recover or end cleanly instead of crashing.

| Block | Role |
|---|---|
| `try` | contains the code that may raise an exception |
| `except` | runs if an exception occurs in `try`; may name the exception type (`except ValueError`) |
| `else` (optional) | runs only if no exception occurred |
| `finally` | **always** runs, whether or not an exception occurred (clean-up: close files, release resources) |

```python
try:
    a = int(input("Enter numerator  : "))
    b = int(input("Enter denominator: "))
    result = a / b
except ZeroDivisionError:
    print("Error: division by zero")
except ValueError:
    print("Error: enter integers only")
else:
    print("Result =", result)
finally:
    print("Finished (finally always runs)")
```

*Run 1* (`10` and `2`): `Result = 5.0` then `Finished (finally always runs)`.
*Run 2* (`10` and `0`): `Error: division by zero` then `Finished (finally always runs)`.
*Run 3* (`ten`): `Error: enter integers only` then `Finished (finally always runs)`.

Flow: Python executes `try`; on an exception it jumps to the first matching `except`; the `finally` block executes last in every case, even if a `return` or an uncaught exception occurs.

@s 10
**File handling** is reading from and writing to files on disk so that data persists after the program ends. Steps: (1) **open** the file with `open(name, mode)`, (2) **read/write**, (3) **close** it (the `with` statement closes it automatically).

| Mode | Meaning |
|---|---|
| `r` / `w` / `a` | read / write (truncate) / append, text |
| `rb` / `wb` / `ab` | the same in **binary** mode |
| `r+` / `w+` | read and write |

Text files store characters; **binary files** store raw bytes (images, audio, serialised objects), read with `rb` and written with `wb`.

```python
import pickle

# ---- write to a binary file ----
data = {"name": "Ram", "roll": 12, "marks": [78, 85, 91]}
with open("student.dat", "wb") as f:
    pickle.dump(data, f)                  # serialise the object to bytes

# ---- read from the binary file ----
with open("student.dat", "rb") as f:
    loaded = pickle.load(f)
print(loaded)
print(loaded["name"], sum(loaded["marks"]))
```

*Output*

```
{'name': 'Ram', 'roll': 12, 'marks': [78, 85, 91]}
Ram 254
```

Raw bytes without `pickle`:

```python
with open("raw.bin", "wb") as f:
    f.write(bytes([72, 101, 108, 108, 111]))
with open("raw.bin", "rb") as f:
    content = f.read()
print(content)             # b'Hello'
print(list(content))       # [72, 101, 108, 108, 111]
```

@s 11
- A **module** is one Python file (`.py`) containing functions, classes and variables that can be imported: `import math`.
- A **package** is a directory of modules containing an `__init__.py` file; it groups related modules in a hierarchy: `import package.module`.
- A **library** is a collection of modules and packages that offers ready-made functionality for a field. The Python Standard Library comes with Python; others are installed with `pip`.

| | Module | Package | Library |
|---|---|---|---|
| Form | single `.py` file | folder of modules + `__init__.py` | collection of packages/modules |
| Example | `math`, `random` | `numpy.linalg`, `os.path` | NumPy, Matplotlib |

**Three commonly used libraries**

1. **NumPy**: fast n-dimensional arrays and linear algebra, used for numerical computation.
2. **Matplotlib**: plotting and visualisation (graphs of waveforms, charts).
3. **pandas**: tabular data analysis (DataFrames, reading CSV/Excel).

(Others: SciPy for scientific computing, requests for HTTP, scikit-learn for machine learning, Tkinter for GUI.)

```python
import math                      # module of the standard library
import numpy as np               # third-party library
import matplotlib.pyplot as plt  # module inside a package
print(math.sqrt(49), np.arange(3))   # 7.0 [0 1 2]
```

@s 12
**Why NumPy arrays are better than lists for numerical work**

| Python list | NumPy array (`ndarray`) |
|---|---|
| Can hold mixed types; each item is a separate Python object with pointer overhead | Holds items of one data type stored in a contiguous block of memory |
| Needs a loop or comprehension for element-wise work | **Vectorised** operations on the whole array without an explicit loop |
| `[1,2]+[3,4]` joins lists to `[1,2,3,4]`; `*` repeats | `+`, `-`, `*`, `/` act element by element |
| Slow for large data (interpreted loops) | Operations are implemented in C: typically 10 to 100 times faster and use less memory |
| No built-in matrix algebra | `dot`, `@`, `linalg.inv`, `linalg.solve`, statistics, broadcasting |

```python
import numpy as np

lst = [1, 2, 3, 4]
arr = np.array([1, 2, 3, 4])

print(lst * 2)          # [1, 2, 3, 4, 1, 2, 3, 4]   repetition, not arithmetic
print(arr * 2)          # [2 4 6 8]                    element-wise
print(arr + arr)        # [2 4 6 8]
print([x * 2 for x in lst])   # list needs a comprehension
print(arr.mean(), arr.sum())  # 2.5 10
```

**Voltage matrix $V = IR$.** Take the current matrix $I$ (in amperes) and the resistance matrix $R$ (in ohm):

$$I=\begin{bmatrix}2&1\\3&4\end{bmatrix},\qquad R=\begin{bmatrix}10&5\\20&15\end{bmatrix}$$

```python
import numpy as np

I = np.array([[2, 1],
              [3, 4]])          # current matrix (A)
R = np.array([[10, 5],
              [20, 15]])        # resistance matrix (ohm)

V = np.dot(I, R)                # matrix multiplication, same as I @ R
print("Current matrix I:\n", I)
print("Resistance matrix R:\n", R)
print("Voltage matrix V = I R:\n", V)
```

*Output*

```
Current matrix I:
 [[2 1]
 [3 4]]
Resistance matrix R:
 [[10  5]
 [20 15]]
Voltage matrix V = I R:
 [[ 40  25]
 [110  75]]
```

Check by hand using row by column products:

$$V=\begin{bmatrix}2(10)+1(20) & 2(5)+1(15)\\ 3(10)+4(20) & 3(5)+4(15)\end{bmatrix}=\begin{bmatrix}40&25\\110&75\end{bmatrix}\ \text{V}$$

(If Ohm's law is applied branch by branch instead, the element-wise product `I * R` gives `[[20, 5], [60, 60]]` V; the question asks for matrix multiplication, so the answer is $V=\begin{bmatrix}40&25\\110&75\end{bmatrix}$.)

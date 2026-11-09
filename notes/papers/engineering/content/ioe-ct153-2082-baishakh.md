---
file: NEBians-IOE-Past-Paper-Advanced-Computer-Programming-CT153-2082-Baishakh.pdf
subject: Advanced Computer Programming
level: BE · Year I / Part II
code: CT 153
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Discuss about the different programming paradigms with their advantage and disadvantage. [[4]]

@q 2
Briefly explain different application areas of python programming. [[4]]

@q 3
Define recursive function. Write a program to find the n<sup>th</sup> term of Fibonacci series using recursive function. [[2+4]]

@q 4
Explain the concept of mutable and immutable data type in python. For the given list of dictionaries, find the TOTAL MARKS obtained: [[4+4]]

```
d = [{"subject":"math","marks":80},
     {"subject":"science","marks":90},
     {"subject":"english","marks":80}]
```

@q 5
Explain the significance of lambda function with an example. [[2]]

@q 6
Explain the benefits of object-oriented programming over procedural programming. [[6]]

@q 7
Explain the concept of dynamic binding. Write python code to illustrate concept of abstract class. [[2+4]]

@q 8
Using concept of binary operator overloading, find the sum of complex numbers. Use class called as complex, with two attributes: [real and imaginary]. [[6]]

@q 9
Define exception. You cannot divide a given number by zero. Based on given statement, write python code to handle the given exception. [[2+4]]

@q 10
Discuss the difference between a Python module, package, and library. What are the different ways to import modules? [[3+3]]

@q 11
How do you reshape a NumPy array? Write a program to solve following system of linear equations using NumPy. [[2+4]]

$$\begin{gathered}2x + 3y = 12 \\ 4x - 5y = -2\end{gathered}$$
<!-- SOLUTIONS -->

@s 1
A **programming paradigm** is a fundamental style of writing programs. The main paradigms, with their advantages and disadvantages, are:

| Paradigm | Idea | Advantages | Disadvantages |
|---|---|---|---|
| **Imperative / procedural** (C, Pascal, Python scripts) | A sequence of statements changes program state; code is grouped into procedures | Simple, fast, close to hardware, easy to learn | Global data is unsafe; large programs become hard to maintain and reuse |
| **Object oriented** (Java, C++, Python) | Programs are objects (data + methods) created from classes; encapsulation, inheritance, polymorphism | Code reuse, data hiding, easy maintenance, models real-world entities | More design effort, larger and slower programs, steeper learning curve |
| **Functional** (Haskell, Lisp, Python features) | Programs are compositions of pure functions; immutable data, recursion | No side effects so easy to test and parallelise; short code | Recursion and immutability can be slow and memory hungry; I/O and state are awkward |
| **Declarative / logic** (SQL, Prolog, HTML) | Describe *what* is wanted, the system decides *how* | Short, high-level programs | Little control over performance; limited to specific domains |
| **Event driven** (GUI, JavaScript, Tkinter) | Control flow is decided by events (click, key, sensor) | Responsive interactive programs | Flow is hard to trace and debug |

Python is a **multi-paradigm** language: procedural, object-oriented and functional styles can be mixed in one program.

@s 2
Python is a general-purpose language with a huge library ecosystem. Its main application areas are:

1. **Web development:** server-side frameworks Django, Flask, FastAPI.
2. **Data science and analytics:** NumPy, pandas, Matplotlib for analysis and visualisation.
3. **Artificial intelligence and machine learning:** scikit-learn, TensorFlow, PyTorch, OpenCV.
4. **Scientific and engineering computing:** SciPy and SymPy for simulation, signal processing, numerical solution of circuits and control problems.
5. **Automation and scripting:** file handling, web scraping (BeautifulSoup, Selenium), system administration, testing.
6. **Embedded systems and IoT:** MicroPython and Raspberry Pi for sensors and robotics.
7. **Desktop GUI and games:** Tkinter, PyQt, Pygame.
8. **Networking and cyber-security:** socket programming, penetration testing tools.
9. **Education:** the first language in many courses because of its simple syntax.

@s 3
A **recursive function** is a function that calls itself, directly or indirectly, to solve a smaller instance of the same problem. A correct recursive function has (i) a **base case** that stops the recursion and (ii) a **recursive case** that moves toward the base case. Each call is stacked in memory until the base case returns.

The Fibonacci series is $0, 1, 1, 2, 3, 5, 8, 13, \dots$ defined by

$$\begin{gathered}F(0)=0 \\ F(1)=1 \\ F(n)=F(n-1)+F(n-2)\ \ (n\ge 2)\end{gathered}$$

```python
def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:                 # base cases
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)   # recursive case


n = int(input("Enter n: "))
print(f"The {n}th term of the Fibonacci series is", fibonacci(n))
print("Series:", [fibonacci(i) for i in range(n + 1)])
```

*Sample run* with `n = 8`:

```
The 8th term of the Fibonacci series is 21
Series: [0, 1, 1, 2, 3, 5, 8, 13, 21]
```

The plain recursion makes about $2^n$ calls; adding `functools.lru_cache` (memoisation) makes it linear:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(50))          # 12586269025
```

@s 4
**Mutable data types** can be modified in place after creation and keep the same identity: `list`, `dict`, `set`. **Immutable data types** cannot be changed once created; any modification builds a new object: `int`, `float`, `str`, `tuple`, `bool`, `frozenset`.

```python
L = [1, 2, 3]
print(id(L)); L.append(4); print(id(L))     # same id: modified in place
T = (1, 2, 3)
# T[0] = 5                                  # TypeError: tuple does not support item assignment
S = "abc"; S2 = S + "d"                     # new string object, S is unchanged
```

Mutable objects can be used as shared, growing containers but are not hashable (cannot be dictionary keys); immutable objects are hashable, thread-safe and safe to share.

**Total marks from the list of dictionaries**

```python
d = [{"subject": "math", "marks": 80},
     {"subject": "science", "marks": 90},
     {"subject": "english", "marks": 80}]

total = 0
for item in d:                  # each item is a dictionary
    total += item["marks"]
print("TOTAL MARKS =", total)

# one-line alternatives
print(sum(item["marks"] for item in d))
print(sum(map(lambda x: x["marks"], d)))
```

*Output*

```
TOTAL MARKS = 250
250
250
```

$80 + 90 + 80 = 250$ marks (average $=250/3 = 83.33$).

@s 5
A **lambda function** is an anonymous, single-expression function: `lambda arguments: expression`. Its significance:

- It is **short** (one line) and needs no `def` or name, so it keeps code compact where a tiny function is needed only once.
- It is a convenient argument for **higher-order functions** such as `map()`, `filter()`, `sorted()`, `reduce()` and for callbacks (GUI buttons).
- It supports the functional style of programming.

```python
nums = [1, 2, 3, 4, 5, 6]
square = lambda x: x ** 2
print(square(7))                                 # 49
print(list(filter(lambda x: x % 2 == 0, nums)))  # [2, 4, 6]
print(sorted(["pear", "fig", "banana"], key=lambda s: len(s)))   # ['fig', 'pear', 'banana']
```

@s 6
**Procedural programming** divides a program into procedures (functions) that act on shared data. **Object-oriented programming** divides it into objects that combine data and behaviour. Benefits of OOP over procedural programming:

1. **Encapsulation and data hiding.** Data and methods are bound in a class and private data is accessed only through methods, so it cannot be corrupted by unrelated code. In procedural programs global data is open to every function.
2. **Reusability through inheritance.** A new class can reuse and extend an existing class, so no code is rewritten. Procedural reuse is limited to copying functions.
3. **Polymorphism.** The same method name or operator works differently for different objects (`speak()` of `Dog` and `Cat`), giving flexible and extensible code.
4. **Abstraction.** Users of a class see only the interface, not the implementation; complexity is hidden.
5. **Models the real world.** Real entities (student, bank account, resistor) map directly to objects, giving a natural design (bottom-up approach, versus the top-down approach of procedural code).
6. **Easier maintenance and modification.** Changes inside a class do not affect other parts; large programs are modular and teams can work on different classes.
7. **Security and reliability** through access control and fewer unintended side effects; **easier testing** of each class separately.
8. **Extensibility.** New objects are added without changing existing code (open-closed principle).

| Feature | Procedural | Object oriented |
|---|---|---|
| Unit | function | object / class |
| Approach | top-down | bottom-up |
| Data | global, exposed | hidden inside objects |
| Reuse | function calls | inheritance, composition |
| Security | low | high |
| Example | C, Pascal | Java, C++, Python |

@s 7
**Dynamic binding** (late binding, run-time polymorphism) means that the method to be executed is decided **at run time** from the actual type of the object, not at compile time. In Python all method calls are dynamically bound: when a base-class reference (or any variable) refers to a derived-class object, the overridden method of the derived class runs. It is the basis of method overriding.

```python
class Animal:
    def sound(self):
        return "some sound"

class Dog(Animal):
    def sound(self):
        return "Bark"

class Cat(Animal):
    def sound(self):
        return "Meow"

for a in (Dog(), Cat(), Animal()):     # the method is chosen at run time
    print(type(a).__name__, "->", a.sound())
```

*Output*

```
Dog -> Bark
Cat -> Meow
Animal -> some sound
```

**Abstract class.** An abstract class has at least one *abstract method* (declared but not implemented) and cannot be instantiated. Subclasses must implement all abstract methods. Python provides it with the `abc` module (`ABC`, `@abstractmethod`).

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):                       # abstract class
    @abstractmethod
    def area(self):                     # abstract method
        pass

    def describe(self):                 # concrete method
        print(type(self).__name__, "with area", round(self.area(), 2))

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return math.pi * self.r ** 2

class Rectangle(Shape):
    def __init__(self, l, w):
        self.l, self.w = l, w
    def area(self):
        return self.l * self.w

# s = Shape()      # TypeError: Can't instantiate abstract class Shape
for s in (Circle(3), Rectangle(4, 5)):
    s.describe()                        # dynamic binding picks the right area()
```

*Output*

```
Circle with area 28.27
Rectangle with area 20
```

@s 8
**Binary operator overloading** gives a binary operator such as `+` a meaning for user-defined objects by defining the special method `__add__(self, other)`. For complex numbers $z_1=a_1+ib_1$ and $z_2=a_2+ib_2$:

$$z_1+z_2=(a_1+a_2)+i(b_1+b_2)$$

```python
class Complex:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __add__(self, other):                       # overloads +
        return Complex(self.real + other.real,
                       self.imaginary + other.imaginary)

    def __str__(self):
        sign = "+" if self.imaginary >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imaginary)}i"


c1 = Complex(3, 4)
c2 = Complex(5, -2)
c3 = c1 + c2                                        # c1.__add__(c2)
print("First  :", c1)
print("Second :", c2)
print("Sum    :", c3)
```

*Output*

```
First  : 3 + 4i
Second : 5 - 2i
Sum    : 8 + 2i
```

Check: $(3+4i)+(5-2i)=8+2i$. The same call `c1 + c2` is translated by Python to `c1.__add__(c2)`.

@s 9
An **exception** is a run-time event (error) that disturbs the normal flow of instructions, raised as an object such as `ZeroDivisionError`, `ValueError`, `TypeError`, `IndexError`, `FileNotFoundError`. If it is not handled, the program terminates with a traceback. Division of a number by zero raises `ZeroDivisionError`, so the division is placed in a `try` block and handled in `except`.

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: a number cannot be divided by zero")
        return None
    else:
        return result
    finally:
        print("Division attempted")


try:
    x = float(input("Enter dividend: "))
    y = float(input("Enter divisor : "))
    print("Quotient =", divide(x, y))
except ValueError:
    print("Please enter numeric values only")
```

*Run 1* (`10` and `4`):

```
Division attempted
Quotient = 2.5
```

*Run 2* (`10` and `0`):

```
Error: a number cannot be divided by zero
Division attempted
Quotient = None
```

A custom check is also possible: `if b == 0: raise ZeroDivisionError("divisor is zero")`, caught by the same `except`.

@s 10
- **Module:** a single `.py` file with functions, classes and variables, e.g. `math`, `random`, or the user's own `utils.py`.
- **Package:** a directory containing an `__init__.py` file and several modules (and sub-packages), giving a hierarchical namespace, e.g. `numpy.linalg`, `os.path`, `mypkg/geometry.py`.
- **Library:** a collection of related modules and packages that provides functionality for a domain, e.g. the Python Standard Library, NumPy, Matplotlib, pandas.

| | Module | Package | Library |
|---|---|---|---|
| Structure | one file | folder with `__init__.py` | many packages/modules |
| Purpose | reuse code | organise modules | ready-made toolkit |
| Import | `import math` | `import numpy.linalg` | `import numpy` |

**Different ways to import modules**

```python
import math                      # 1. whole module: math.sqrt(16)
import numpy as np               # 2. with alias: np.array([1, 2])
from math import sqrt, pi        # 3. specific names: sqrt(16)
from math import sqrt as root    # 4. specific name with alias
from math import *               # 5. everything (discouraged: name clashes)
import os.path                   # 6. sub-module of a package
from os import path              # 7. sub-module via from
import importlib                 # 8. dynamic import at run time
m = importlib.import_module("math")

print(math.sqrt(16), sqrt(25), root(36), np.pi == pi, m.floor(2.7))   # 4.0 5.0 6.0 True 2
```

Python searches the current directory, then the directories in `sys.path`. Own modules are imported by file name without `.py`.

@s 11
**Reshaping.** `reshape()` gives an array a new shape without changing its data; the new shape must have the same total number of elements. One dimension may be `-1` and is then calculated automatically.

```python
import numpy as np

a = np.arange(1, 13)              # [ 1  2 ... 12 ]  shape (12,)
b = a.reshape(3, 4)               # 3 rows, 4 columns
c = a.reshape(2, -1)              # 2 x 6 (-1 is inferred)
d = a.reshape(2, 3, 2)            # 3-D
print(b)
print(c.shape, d.shape)           # (2, 6) (2, 3, 2)
print(b.reshape(-1))              # flatten back to 1-D
```

*Output*

```
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
(2, 6) (2, 3, 2)
[ 1  2  3  4  5  6  7  8  9 10 11 12]
```

(`a.reshape(5, 3)` fails with `ValueError` because $12 \ne 15$.) `ravel()` and `flatten()` also give a 1-D array.

**Solving the linear system.** Write $AX=B$:

$$\begin{bmatrix}2&3\\4&-5\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}=\begin{bmatrix}12\\-2\end{bmatrix}$$

```python
import numpy as np

A = np.array([[2, 3],
              [4, -5]])
B = np.array([12, -2])

X = np.linalg.solve(A, B)          # solves A X = B
print("x =", X[0])
print("y =", X[1])
print("check A@X =", A @ X)
```

*Output*

```
x = 2.4545454545454546
y = 2.3636363636363638
check A@X = [12. -2.]
```

*Check by hand.* Multiply the first equation by 5 and the second by 3: $10x+15y=60$ and $12x-15y=-6$. Adding gives $22x=54$, so

$$\begin{gathered}x=\frac{27}{11}=2.4545 \\ y=\frac{12-2x}{3}=\frac{26}{11}=2.3636\end{gathered}$$

and $4(27/11)-5(26/11)=(108-130)/11=-2$, as required. The determinant of $A$ is $2(-5)-3(4)=-22\neq0$, so a unique solution exists. Equivalent forms are `np.linalg.inv(A) @ B` and `np.dot(np.linalg.inv(A), B)`.

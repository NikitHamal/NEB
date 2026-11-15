---
file: NEBians-IOE-Past-Paper-Advanced-Computer-Programming-CT153-2081-Ashwin.pdf
subject: Advanced Computer Programming
level: BE · Year I / Part II
code: CT 153
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Explain different programming paradigm with example for each. [[4]]

@q 2
List out the features and limitations of python. [[2+2]]

@q 3
What do you mean by operators? Explain different types of operators available in python with example. [[2+4]]

@q 4
With example, explain following data structures in python: (a) List (b) Tuple (c) Dictionary [[6]]

@q 5
Using two-dimensional list, write a program to add two matrices and create the third matrix and display it. [[4]]

@q 6
In object-oriented programming, explain the concept of constructor. Write a python code to illustrate the concept of constructor. [[2+4]]

@q 7
Write python code to explain the concept of Single, Hierarchical and multi-level inheritance. [[6]]

@q 8
Write a program to create a class called **Time** with attributes (hour, minute and second) to represent time and add time objects and return the result. [[6]]

@q 9
Explain different types of errors in python program. Write a python program to create a file called "record.txt" and use it to store the information of two students [Name, Roll No and college Name]. Ask user to enter the information. [[2+4]]

@q 10
Explain the advantages of using NumPy array over python sequences with an example. [[3]]

@q 11
Write a python program to create two 2X2 NumPy arrays and performs matrix addition, subtraction and element-wise multiplication and display the result. [[9]]
<!-- SOLUTIONS -->

@s 1
A **programming paradigm** is a style or model of programming that determines how a program is structured and how its computation is expressed.

| Paradigm | Idea | Example |
|---|---|---|
| **Imperative** | Statements change the state step by step | `total = 0` then `for i in range(1, 6): total += i` |
| **Procedural** | Imperative code organised into procedures (functions) | C, Pascal; `def area(r): return 3.14 * r * r` |
| **Object oriented** | Objects (data + methods) created from classes; encapsulation, inheritance, polymorphism | `class Student:` with `show()`; Java, C++, Python |
| **Functional** | Pure functions, immutable data, no side effects | `list(map(lambda x: x * x, [1, 2, 3]))`; Haskell, Lisp |
| **Declarative / logic** | State what is wanted, not how | `SELECT name FROM student WHERE marks > 50` (SQL), Prolog facts and rules |
| **Event driven** | Execution is driven by events (click, key press, sensor) | `button.config(command=on_click)` in Tkinter, JavaScript |

```python
# Procedural / imperative
def total(n):
    s = 0
    for i in range(1, n + 1):
        s += i
    return s

# Object oriented
class Circle:
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

# Functional
squares = list(map(lambda x: x * x, range(1, 6)))

print(total(5), Circle(2).area(), squares)     # 15 12.56636 [1, 4, 9, 16, 25]
```

Python supports imperative, procedural, object-oriented and functional paradigms (multi-paradigm).

@s 2
**Features of Python**

1. Simple, easy to read and learn; clean syntax with indentation.
2. **Interpreted** language (no separate compile step) with an interactive shell.
3. **Dynamically typed**; no type declarations.
4. **Object oriented**, and also procedural and functional (multi-paradigm).
5. **Free and open source**; large community.
6. **Portable / platform independent**: runs on Windows, Linux, macOS.
7. **Large standard library** plus third-party packages (NumPy, SciPy, Matplotlib, pandas, Django).
8. High-level built-in data types (list, tuple, dict, set) and automatic memory management with garbage collection.
9. **Extensible and embeddable** with C/C++; supports GUI programming and exception handling.

**Limitations of Python**

1. **Slower** than compiled languages (C, C++, Java) because it is interpreted and dynamically typed.
2. **High memory consumption**; not suitable for memory-limited or real-time systems.
3. **Weak in mobile computing and browser-side programming.**
4. The **Global Interpreter Lock** prevents true multi-threaded parallelism for CPU-bound tasks in CPython.
5. **Run-time errors**: type errors are found only when the code executes.
6. Database access layers are less developed than JDBC/ODBC technologies; indentation errors are easy to make.

@s 3
An **operator** is a special symbol that performs an operation on values or variables called **operands**; for example in `a + b` the symbol `+` is the operator and `a`, `b` are the operands. Python has the following types (take `a = 12`, `b = 5`):

| Type | Operators | Example | Result |
|---|---|---|---|
| **Arithmetic** | `+ - * / // % **` | `a + b`, `a / b`, `a // b`, `a % b`, `a ** b` | 17, 2.4, 2, 2, 248832 |
| **Relational (comparison)** | `== != > < >= <=` | `a > b`, `a == b` | True, False |
| **Logical** | `and or not` | `a > 5 and b > 5`, `not(a > b)` | False, False |
| **Assignment** | `= += -= *= /= //= %= **=` | `a += 3` | a becomes 15 |
| **Bitwise** | `& \| ^ ~ << >>` | `a & b`, `a \| b`, `a ^ b`, `a << 1` | 4, 13, 9, 24 |
| **Membership** | `in`, `not in` | `3 in [1, 2, 3]` | True |
| **Identity** | `is`, `is not` | `x is y` | True if both refer to the same object |

```python
a, b = 12, 5
print(a + b, a - b, a * b, a / b, a // b, a % b, a ** b)   # 17 7 60 2.4 2 2 248832
print(a > b, a == b, a != b)                               # True False True
print(a > 5 and b > 5, a > 5 or b > 5, not (a > b))        # False True False
print(a & b, a | b, a ^ b, ~a, a << 1, a >> 1)             # 4 13 9 -13 24 6
a += 3; print(a)                                           # 15
print(3 in [1, 2, 3], "x" not in "abc")                    # True True
x = [1, 2]; y = x; z = [1, 2]
print(x is y, x is z, x == z)                              # True False True
```

@s 4
**(a) List** is an ordered, **mutable** collection of items written in square brackets; items can be of mixed types and repeated; indexed from 0 (negative indices count from the end).

```python
marks = [45, 67, 89, "A", 67]
marks.append(90)            # add at end
marks.insert(1, 50)         # insert at index 1
marks.remove("A")           # remove first matching value
marks[0] = 48               # change an item
print(marks)                # [48, 50, 67, 89, 67, 90]
print(marks[1:4], marks[-1], len(marks))   # [50, 67, 89] 90 6
marks.sort(); print(marks)  # [48, 50, 67, 67, 89, 90]
```

**(b) Tuple** is an ordered, **immutable** collection written in round brackets. It cannot be changed after creation, so it is faster and safe for fixed data (coordinates, days of week); it can be a dictionary key.

```python
point = (3, 4, 5)
print(point[0], len(point), point.count(4), point.index(5))   # 3 3 1 2
x, y, z = point                      # unpacking
single = (7,)                        # one-item tuple needs the comma
# point[0] = 9                       # TypeError: tuple does not support item assignment
print(point + (6,))                  # (3, 4, 5, 6)
```

**(c) Dictionary** is an unordered (insertion-ordered since Python 3.7) **mutable** collection of **key : value** pairs in curly braces; keys are unique and immutable; lookup by key is very fast.

```python
student = {"name": "Sita", "roll": 7, "marks": 88}
student["college"] = "IOE"           # add
student["marks"] = 90                # update
print(student["name"], student.get("age", "N/A"))   # Sita N/A
del student["roll"]
for k, v in student.items():
    print(k, ":", v)
print(list(student.keys()))          # ['name', 'marks', 'college']
```

| | List | Tuple | Dictionary |
|---|---|---|---|
| Brackets | `[ ]` | `( )` | `{ k : v }` |
| Mutable | yes | no | yes |
| Ordered / indexed | yes, by position | yes, by position | by key |
| Duplicates | allowed | allowed | keys unique |

@s 5
Two matrices are added element by element: $C_{ij}=A_{ij}+B_{ij}$; they must have the same order. A matrix is stored as a list of lists (rows).

```python
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

print("Enter elements of matrix A:")
A = [[int(input(f"A[{i}][{j}] = ")) for j in range(cols)] for i in range(rows)]
print("Enter elements of matrix B:")
B = [[int(input(f"B[{i}][{j}] = ")) for j in range(cols)] for i in range(rows)]

C = [[0] * cols for _ in range(rows)]        # third matrix
for i in range(rows):
    for j in range(cols):
        C[i][j] = A[i][j] + B[i][j]

print("Sum matrix C = A + B:")
for row in C:
    print(*row)
```

*Sample run* with a $2\times 3$ pair $A=\begin{bmatrix}1&2&3\\4&5&6\end{bmatrix}$ and $B=\begin{bmatrix}9&8&7\\6&5&4\end{bmatrix}$:

```
Sum matrix C = A + B:
10 10 10
10 10 10
```

A fixed-data version (no input):

```python
A = [[1, 2, 3], [4, 5, 6]]
B = [[9, 8, 7], [6, 5, 4]]
C = [[A[i][j] + B[i][j] for j in range(3)] for i in range(2)]
print(C)               # [[10, 10, 10], [10, 10, 10]]
```

@s 6
A **constructor** is a special method of a class that is called **automatically when an object is created**, to initialise its attributes. In Python it is the method `__init__(self, ...)`. Features: same fixed name `__init__`; it has no return value; it can take parameters, so each object can be created with different initial values; if the class defines none, Python supplies a default constructor that does nothing. Types: **default** (only `self`), **parameterised** (extra arguments) and one with default argument values. (Python has no true constructor overloading; one `__init__` with default arguments is used.) The method `__new__` creates the object and `__init__` initialises it; `__del__` is the destructor.

```python
class Student:
    def __init__(self, name="Unknown", roll=0, marks=0.0):   # constructor
        self.name = name
        self.roll = roll
        self.marks = marks
        print("Constructor called for", self.name)

    def display(self):
        print(f"Name: {self.name}, Roll: {self.roll}, Marks: {self.marks}")


s1 = Student()                      # default values
s2 = Student("Ram", 12, 85.5)       # parameterised
s1.display()
s2.display()
```

*Output*

```
Constructor called for Unknown
Constructor called for Ram
Name: Unknown, Roll: 0, Marks: 0.0
Name: Ram, Roll: 12, Marks: 85.5
```

@s 7
**Inheritance** lets a *child (derived) class* acquire the attributes and methods of a *parent (base) class*, giving code reuse. The syntax is `class Child(Parent):`.

- **Single inheritance:** one child class derives from one parent.
- **Hierarchical inheritance:** several child classes derive from one parent.
- **Multi-level inheritance:** a class derives from a class that itself derives from another (grandparent to parent to child).

```python
# ---------- Single inheritance : Person -> Student ----------
class Person:
    def __init__(self, name):
        self.name = name
    def show(self):
        print("Name:", self.name)

class Student(Person):
    def study(self):
        print(self.name, "is studying")

# ---------- Hierarchical inheritance : Person -> Teacher, Person -> Clerk ----------
class Teacher(Person):
    def teach(self):
        print(self.name, "is teaching")

class Clerk(Person):
    def work(self):
        print(self.name, "is doing office work")

# ---------- Multi-level inheritance : Person -> Student -> GraduateStudent ----------
class GraduateStudent(Student):
    def research(self):
        print(self.name, "is doing research")

s = Student("Ram");          s.show(); s.study()
t = Teacher("Sita");         t.show(); t.teach()
c = Clerk("Hari");           c.work()
g = GraduateStudent("Gita"); g.show(); g.study(); g.research()
print(issubclass(GraduateStudent, Person))      # True
```

*Output*

```
Name: Ram
Ram is studying
Name: Sita
Sita is teaching
Hari is doing office work
Name: Gita
Gita is studying
Gita is doing research
True
```

```figure
import numpy as _np, matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(9, 3.2))
ax.set_xlim(0, 18); ax.set_ylim(0, 6.4); ax.axis('off')
def box(x, y, t, w=3.2, h=0.9):
    ax.add_patch(mp.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle='round,pad=0.05', fc='white', ec=INK, lw=1.4))
    ax.text(x, y, t, ha='center', va='center', fontsize=9, color=INK)
def arr(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.6))
# single
box(2.2, 5.3, 'Person'); box(2.2, 2.6, 'Student'); arr(2.2, 2.15, 2.2, 4.85)
ax.text(2.2, 0.8, 'Single', ha='center', fontsize=10, color=INK, weight='bold')
# hierarchical
box(9, 5.3, 'Person'); box(6.9, 2.6, 'Teacher', w=2.6); box(11.1, 2.6, 'Clerk', w=2.6)
arr(6.9, 3.05, 8.4, 4.85); arr(11.1, 3.05, 9.6, 4.85)
ax.text(9, 0.8, 'Hierarchical', ha='center', fontsize=10, color=INK, weight='bold')
# multilevel
box(15.8, 5.5, 'Person', w=3.0, h=0.8); box(15.8, 3.7, 'Student', w=3.0, h=0.8); box(15.8, 1.9, 'GraduateStudent', w=3.0, h=0.8)
arr(15.8, 4.1, 15.8, 5.1); arr(15.8, 2.3, 15.8, 3.3)
ax.text(15.8, 0.6, 'Multi-level', ha='center', fontsize=10, color=INK, weight='bold')
```

@s 8
Time is kept as hour, minute, second. Adding two times: add seconds, carry $\lfloor s/60\rfloor$ into minutes, add minutes, carry $\lfloor m/60\rfloor$ into hours. A cleaner way is to convert both to total seconds, add and convert back:

$$\begin{gathered}\text{total}=3600h+60m+s \\ h=\lfloor \text{total}/3600\rfloor,\ \ m=\lfloor (\text{total}\bmod 3600)/60\rfloor,\ \ s=\text{total}\bmod 60\end{gathered}$$

```python
class Time:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def add(self, other):                         # returns a new Time object
        s = self.second + other.second
        m = self.minute + other.minute + s // 60  # carry from seconds
        h = self.hour + other.hour + m // 60      # carry from minutes
        return Time(h, m % 60, s % 60)

    def display(self):
        print(f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}")


print("Enter first time")
t1 = Time(int(input("hour: ")), int(input("minute: ")), int(input("second: ")))
print("Enter second time")
t2 = Time(int(input("hour: ")), int(input("minute: ")), int(input("second: ")))

t3 = t1.add(t2)
print("Sum of the times = ", end="")
t3.display()
```

*Sample run*: $t_1 = 2\text{ h }45\text{ min }50\text{ s}$ and $t_2 = 1\text{ h }30\text{ min }25\text{ s}$:

```
Sum of the times = 04:16:15
```

Check: seconds $50+25=75=1\text{ min }15\text{ s}$; minutes $45+30+1=76=1\text{ h }16\text{ min}$; hours $2+1+1=4$. So $4\text{ h }16\text{ min }15\text{ s}$.

(Operator form: define `__add__` instead of `add` and write `t3 = t1 + t2`.)

@s 9
**Types of errors in Python**

| Error type | When it occurs | Example |
|---|---|---|
| **Syntax error** | The code breaks the grammar of the language; detected at **compile/parse time**, program does not run | `print("hi"` ; `if x > 5` (missing colon); bad indentation (`IndentationError`) |
| **Run-time error (exception)** | Program is syntactically correct but fails while running | `10 / 0` gives `ZeroDivisionError`; `int("abc")` gives `ValueError`; `[1,2][5]` gives `IndexError`; `open("x")` gives `FileNotFoundError`; `undefined_name` gives `NameError` |
| **Logical error** | The program runs without any error message but gives a wrong result | `average = a + b / 2` instead of `(a + b) / 2` |

Syntax errors must be corrected before running; exceptions can be handled with `try`/`except`; logical errors are found by testing and debugging.

**Program to store the details of two students in `record.txt`**

```python
with open("record.txt", "w") as f:               # create the file
    for i in range(1, 3):
        print(f"Enter information of student {i}")
        name = input("Name: ")
        roll = input("Roll No: ")
        college = input("College Name: ")
        f.write(f"{name},{roll},{college}\n")    # one line per student

print("Records written. File contents:")
with open("record.txt", "r") as f:               # read it back to display
    for line in f:
        name, roll, college = line.strip().split(",")
        print(f"Name: {name} | Roll No: {roll} | College: {college}")
```

*Sample run* (inputs: `Ram`, `101`, `Pulchowk Campus`; `Sita`, `102`, `Thapathali Campus`):

```
Records written. File contents:
Name: Ram | Roll No: 101 | College: Pulchowk Campus
Name: Sita | Roll No: 102 | College: Thapathali Campus
```

and `record.txt` holds

```
Ram,101,Pulchowk Campus
Sita,102,Thapathali Campus
```

Mode `"w"` creates the file (or overwrites an existing one); `"a"` would append. The `with` statement closes the file automatically.

@s 10
NumPy's `ndarray` is a homogeneous, fixed-type, n-dimensional array stored in contiguous memory. Advantages over Python sequences (list, tuple):

1. **Speed:** operations run in compiled C code and avoid Python's per-item overhead; they are typically 10 to 100 times faster.
2. **Less memory:** items of one type are stored compactly (a list stores a pointer to a separate object for every item).
3. **Vectorised operations:** arithmetic on whole arrays without loops (`a + b`, `a * 2`, `np.sin(a)`); with lists `+` concatenates and `*` repeats.
4. **Broadcasting** of arrays of different shapes and powerful indexing, slicing and boolean masking.
5. **Built-in mathematical tools:** linear algebra (`dot`, `inv`, `solve`), statistics, Fourier transform and random numbers.
6. **Multi-dimensional arrays** with `shape`, `reshape`, `transpose`.

```python
import numpy as np

lst = [1, 2, 3, 4]
arr = np.array(lst)

print(lst + lst)          # [1, 2, 3, 4, 1, 2, 3, 4]  concatenation
print(arr + arr)          # [2 4 6 8]                 element-wise addition
print(arr * 10)           # [10 20 30 40]
print(arr ** 2)           # [ 1  4  9 16]
print(arr[arr > 2])       # [3 4]  boolean masking
```

@s 11
For two $2\times2$ arrays $A$ and $B$: addition and subtraction work element by element, and `*` in NumPy is the **element-wise (Hadamard) product** $C_{ij}=A_{ij}B_{ij}$ (not the matrix product, which is `A @ B` or `np.dot`).

```python
import numpy as np

A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

add = A + B                      # np.add(A, B)
sub = A - B                      # np.subtract(A, B)
mul = A * B                      # np.multiply(A, B), element-wise

print("A =\n", A)
print("B =\n", B)
print("A + B =\n", add)
print("A - B =\n", sub)
print("A * B (element-wise) =\n", mul)
print("A @ B (matrix product, for comparison) =\n", A @ B)
```

*Output*

```
A =
 [[1 2]
 [3 4]]
B =
 [[5 6]
 [7 8]]
A + B =
 [[ 6  8]
 [10 12]]
A - B =
 [[-4 -4]
 [-4 -4]]
A * B (element-wise) =
 [[ 5 12]
 [21 32]]
A @ B (matrix product, for comparison) =
 [[19 22]
 [43 50]]
```

Check by hand: $1+5=6$, $2+6=8$, $3+7=10$, $4+8=12$; $1-5=-4$; $1\cdot5=5$, $2\cdot6=12$, $3\cdot7=21$, $4\cdot8=32$.

A version that reads the two arrays from the user:

```python
import numpy as np
A = np.array([[int(input(f"A[{i}][{j}]: ")) for j in range(2)] for i in range(2)])
B = np.array([[int(input(f"B[{i}][{j}]: ")) for j in range(2)] for i in range(2)])
print("Sum:\n", A + B, "\nDifference:\n", A - B, "\nElement-wise product:\n", A * B)
```

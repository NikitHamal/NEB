---
subject: OOP in Java
grade: BCA Semester 2
unit: 1
title: Object-Oriented Concepts and Java Fundamentals
area: BCA 153 · OOP in Java · Unit 1
---

Java is a class-based, object-oriented language that compiles to bytecode and runs on the Java Virtual Machine, so one program runs unchanged on Windows, Linux, macOS and Android-style runtimes. This unit introduces the ideas behind object-oriented programming and the basic Java language: types, operators, control flow, arrays and strings. Every program in this book was compiled and run; the output shown is the real output.

::: key What this unit gives you
- The object-oriented paradigm: objects, classes, the four pillars.
- How Java works: JDK, JRE, JVM, bytecode; compiling and running.
- Data types, operators, casting and overflow; control statements; arrays.
- Reading input and formatting output.
:::

## 1.1 Object-oriented programming

**Procedural programming** (C) organises code as functions acting on separate data. **Object-oriented programming (OOP)** bundles **data (fields)** and the **behaviour (methods)** that works on it into **objects**, so a program becomes a collection of cooperating objects.

- A **class** is a blueprint; an **object** (instance) is a thing built from it with its own state. `Student` is a class; Sita and Ram are objects.
- **Four pillars**

| Pillar | Idea | Benefit |
|---|---|---|
| **Encapsulation** | keep fields private, expose a controlled interface | protects invariants; the inside can change freely |
| **Abstraction** | show *what* an object does, hide *how* | manage complexity |
| **Inheritance** | a subclass reuses and extends a superclass (*is-a*) | code reuse, hierarchies |
| **Polymorphism** | one interface, many behaviours (overriding, overloading) | flexible, extensible code |

Other terms: **message passing** (calling a method), **coupling** (how much classes depend on each other; keep low) and **cohesion** (how focused a class is; keep high).

## 1.2 How Java works

**Write → compile → run:** `Hello.java` → `javac Hello.java` → `Hello.class` (**bytecode**) → `java Hello` (the **JVM** loads, verifies and executes it, with a just-in-time (JIT) compiler turning hot code into machine code).

| Term | Meaning |
|---|---|
| JVM | Java Virtual Machine: runs bytecode; platform-specific |
| JRE | JVM + standard class libraries |
| JDK | JRE + compiler `javac` and tools (`jar`, `javadoc`, `jshell`) |
| Garbage collector | frees memory of objects no longer reachable; no `free()` |

Features: platform independence ("write once, run anywhere"), strong typing, automatic memory management, no pointers, built-in multithreading, rich standard library. Java gives each program a **stack** (method calls and local variables) and a **heap** (objects). Names: classes `PascalCase`, methods and variables `camelCase`, constants `UPPER_SNAKE`; the file name must match the public class.

## 1.3 Types, operators and conversions

**Primitive types:** `byte` 8-bit, `short` 16, `int` 32, `long` 64 (suffix `L`), `float` 32 (suffix `f`), `double` 64, `char` 16-bit Unicode, `boolean`. Everything else (including `String`, arrays) is a **reference type**. `var` lets the compiler infer a local type (`var n = 5;`).

Operators: arithmetic `+ - * / %`; relational `== != < > <= >=`; logical `&& || !` (short-circuit); bitwise `& | ^ ~ << >> >>>`; assignment `= += -= …`; ternary `c ? a : b`; `instanceof`. **Integer division truncates**, `%` follows the dividend's sign, and `int` arithmetic **overflows silently**.

```java
public class Basics {
    public static void main(String[] args) {
        int a = 7, b = 2;
        double avg = (a + b) / 2.0;
        System.out.println(a / b);
        System.out.println(a % b);
        System.out.println(avg);
        char c = 'A'; c += 2;
        System.out.println(c);
        long big = Integer.MAX_VALUE + 1L;
        System.out.println(big);
        int overflow = Integer.MAX_VALUE + 1;
        System.out.println(overflow);
        String s = "Nepal";
        System.out.println(s.length() + " " + s.toUpperCase() + " " + s.charAt(2) + " " + s.substring(1, 4));
        System.out.println((byte) 200);
        System.out.println(10 / 4 * 2.0);
    }
}
```
```output
3
1
4.5
C
2147483648
-2147483648
5 NEPAL p epa
-56
4.0
```

**Casting.** *Widening* (int → long → double) is automatic; *narrowing* needs a cast and can lose data: `(byte) 200` is −56 because 200 − 256 = −56. `10 / 4 * 2.0` evaluates left to right: 10 / 4 = 2 (integer), then × 2.0 = 4.0. **Wrapper classes** (`Integer`, `Double`, `Character`, `Boolean`) box primitives for collections; **autoboxing** converts automatically (`Integer x = 5;`). Compare wrapper objects with `equals`, not `==` (small cached values hide the bug).

## 1.4 Control flow and arrays

`if / else if / else`, `switch` (classic and the Java 14+ **switch expression** with `->`), loops `for`, enhanced `for (T x : collection)`, `while`, `do … while`, `break`, `continue` (with labels for nested loops), `return`.

An **array** is a fixed-size object holding elements of one type; indices start at 0; `length` is a field; out-of-range access throws `ArrayIndexOutOfBoundsException` (Java checks bounds, unlike C). A 2-D array is an array of arrays.

```java
public class Arrays1 {
    public static void main(String[] args) {
        int[] marks = {72, 85, 64, 91, 58};
        int sum = 0, max = marks[0];
        for (int m : marks) { sum += m; if (m > max) max = m; }
        System.out.println("Sum=" + sum + " Max=" + max + " Avg=" + (double) sum / marks.length);
        int[][] grid = new int[3][3];
        for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) grid[i][j] = i * 3 + j;
        System.out.println(java.util.Arrays.deepToString(grid));
        int n = 5; long f = 1;
        for (int i = 2; i <= n; i++) f *= i;
        System.out.println(n + "! = " + f);
        String grade = switch (max / 10) { case 10, 9 -> "A"; case 8 -> "B"; default -> "C"; };
        System.out.println(grade);
    }
}
```

```output
Sum=370 Max=91 Avg=74.0
[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
5! = 120
A
```

Useful utilities: `Arrays.sort(a)`, `Arrays.toString(a)`, `Arrays.fill`, `Arrays.copyOf`, `Arrays.equals`, `Arrays.binarySearch` (on a sorted array). **Varargs:** `static int sum(int... xs)`.

## 1.5 Input and output

Output: `System.out.println` (with newline), `print`, and `printf("%d %.2f %s %n", …)`. Input: `java.util.Scanner`:

```java
import java.util.Scanner;
public class ReadInput {
    public static void main(String[] args) {
        Scanner in = new Scanner("12 3.5 Sita\nSecond line here");
        int n = in.nextInt();
        double d = in.nextDouble();
        String w = in.next();
        in.nextLine();
        String line = in.nextLine();
        System.out.printf("%d %.1f %s | %s%n", n, d, w, line);
    }
}
```

```output
12 3.5 Sita | Second line here
```

(Here the `Scanner` reads from a string so the example is self-contained; use `new Scanner(System.in)` for the keyboard.) **Common bug:** after `nextInt()` the newline remains, so a following `nextLine()` returns an empty string; consume it with an extra `nextLine()`, as above. `String.format` and `printf` share the format codes: `%5d` width, `%-8s` left-aligned, `%08.3f` zero-padded, `%x` hex. Command-line arguments arrive in `String[] args`.

## 1.6 From idea to running program

Java was designed at Sun Microsystems in the early 1990s by a team led by James Gosling, first for small consumer devices and then for the Internet. Its central trick is the **bytecode**: the compiler does not produce machine code for one processor, it produces instructions for an imaginary computer (the JVM) that every platform implements. Plate 1.1 shows the creator and one of the smallest places Java still runs. Figure 1.1 shows the full path from source file to running program, and Figure 1.2 shows the four pillars on one small class design that the Model Answers below turn into working code.

```photogrid label="1.1" cols="2" ratio="1.1" caption="(a) James Gosling, who led the team that created Java at Sun Microsystems. (b) The silicon die of a SIM-card chip. Java Card, a cut-down Java platform, runs on chips of this kind in SIM cards and bank cards, which shows how small the JVM idea can be made."
@ photo id="bca153/gosling" cap="James Gosling, creator of Java"
fit 1.1
focus 0.5 0.62
@ photo id="bca153/simchip" cap="Die of a smart-card (SIM) chip: memory blocks and logic"
fit 1.1
focus 0.5 0.5
call 0.28 0.80 0.30 0.55 "Memory array"
```

```svgfig label="1.1" caption="Write once, run anywhere. Hello.java is compiled once by javac into platform-neutral bytecode (Hello.class). Each platform has its own JVM, which loads, verifies and runs the same bytecode; the JIT compiler turns hot methods into machine code."
f = Fig(600, 240)
f.box(14, 90, 100, 52, "Hello.java\nsource code", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(160, 90, 100, 52, "javac\ncompiler", fill="#fde68a", color=NAVY, size=11, bold=True)
f.box(306, 90, 100, 52, "Hello.class\nbytecode", fill="#bbf7d0", color=NAVY, size=11, bold=True)
f.arrow([(114, 116), (160, 116)], color=SLATE, sw=2)
f.arrow([(260, 116), (306, 116)], color=SLATE, sw=2)
for i, (name, y) in enumerate((("JVM on Windows", 20), ("JVM on Linux", 90), ("JVM on Android", 160))):
    f.box(452, y, 140, 52, name, fill="#ffffff", stroke=TEAL, color=NAVY, size=10.5, bold=True)
    f.arrow([(406, 116), (430, 116), (430, y + 26), (452, y + 26)], color=TEAL, sw=1.6)
f.text(210, 170, "java Hello", size=11, color=RED, bold=True)
f.text(210, 186, "loads, verifies, interprets,", size=10, color=SLATE)
f.text(210, 200, "JIT-compiles hot code", size=10, color=SLATE)
f.text(160, 70, "once per program", size=10.5, color=TEAL, bold=True)
f.text(500, 232, "once per platform", size=10.5, color=TEAL, bold=True)
```

```svgfig label="1.2" caption="Four pillars on one design. Encapsulation: balance is private. Abstraction: Account is abstract and promises monthlyEffect(). Inheritance: Savings and Current extend Account. Polymorphism: the same call applyMonth() runs different code for each subclass."
f = Fig(600, 250)
f.box(190, 14, 220, 78, "", fill=BLUE, stroke=NAVY)
f.text(300, 30, "abstract class Account", size=12, color=NAVY, bold=True)
f.line(190, 40, 410, 40, color=NAVY, sw=1)
f.text(300, 55, "- balance : double   (private)", size=10.5, color=NAVY)
f.text(300, 70, "+ deposit(a)   + applyMonth()", size=10.5, color=NAVY)
f.text(300, 85, "+ abstract monthlyEffect()", size=10.5, color=RED, bold=True)
f.box(70, 160, 190, 58, "Savings\nmonthlyEffect() = +interest", fill="#bbf7d0", color=NAVY, size=10.5, bold=True)
f.box(340, 160, 190, 58, "Current\nmonthlyEffect() = -50 fee", fill="#fde68a", color=NAVY, size=10.5, bold=True)
f.arrow([(165, 160), (165, 126), (300, 126), (300, 92)], color=SLATE, sw=1.8)
f.arrow([(435, 160), (435, 126), (300, 126)], color=SLATE, sw=1.8)
f.text(310, 120, "extends (is-a)", size=10, color=SLATE, bold=True, anchor="start")
f.text(430, 46, "Encapsulation", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(430, 62, "Abstraction", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(300, 240, "Polymorphism: for (Account a : list) a.applyMonth();", size=10.5, color=NAVY, bold=True)
```

## 1.7 Eight features of Java

1. **Platform independence.** The compiler produces bytecode, and any computer with a JVM can run it. A billing program written on a Windows laptop in Kathmandu runs unchanged on the Linux server of a bank. This saves the cost of rewriting software for each machine.
2. **Object-oriented design.** Almost everything in Java lives inside a class, and programs are built from cooperating objects. This keeps large programs organised, because each class owns its data and its behaviour. Teams can work on different classes at the same time.
3. **Automatic memory management.** The garbage collector frees objects that nothing refers to any more, so programmers never call `free()`. This removes whole families of bugs such as memory leaks and dangling pointers. A long-running service, like a mobile-banking back end, stays stable for months.
4. **Strong typing and compile-time checks.** Every variable has a declared type, and the compiler rejects mistakes such as assigning text to an `int`. Many errors are therefore found before the program ever runs. This is valuable in systems where a wrong value means a wrong payment.
5. **Robust exception handling.** Errors are objects that can be thrown and caught, so a program can recover instead of crashing. Checked exceptions force the programmer to think about failure, such as a missing file or a lost network link.
6. **Built-in multithreading.** Threads are part of the language and the standard library, so one program can do several jobs at once. A web server can answer many users together, and a desktop program can stay responsive while it downloads.
7. **Security.** The JVM verifies bytecode and has no raw pointers, which blocks many attacks that exploit memory errors. A security manager and class loaders can restrict what downloaded code may do. This is one reason Java is trusted in banking and government systems.
8. **Rich standard library and ecosystem.** Collections, networking, file handling, dates, GUI and database access (JDBC) come ready-made. Android apps, large web back ends and tools used by Nepali fintech companies are all written with the same library.

## 1.8 Lexical elements: the tokens of a Java program

Before the compiler understands what a program *means*, it breaks the text into **tokens**, the smallest pieces that carry meaning. Every Java source file is a stream of six kinds of token plus white space and comments. Exam questions often ask you to "list the tokens of Java" or to spot an illegal identifier, so learn the six kinds by heart.

| Token kind | What it is | Examples |
|---|---|---|
| **Keyword** | A word reserved by the language (about 50, all lower case) | `class`, `public`, `static`, `if`, `while`, `new`, `return` |
| **Identifier** | A name you invent for a class, variable, method or package | `Student`, `totalMarks`, `calcFee` |
| **Literal** | A fixed value written directly in the code | `42`, `3.14`, `'A'`, `"Kathmandu"`, `true`, `null` |
| **Operator** | A symbol that acts on operands | `+`, `-`, `*`, `==`, `&&`, `?:`, `instanceof` |
| **Separator** | Punctuation that structures code | `( ) { } [ ] ; , . ::` |
| **Comment** | Ignored by the compiler; for humans | `// line`, `/* block */`, `/** Javadoc */` |

**Rules for identifiers.** An identifier may contain letters, digits, the underscore `_` and the dollar sign `$`. It must **not start with a digit**, must **not be a keyword**, and is **case sensitive** (`Total`, `total` and `TOTAL` are three different names). `true`, `false` and `null` are literals, not keywords, but they are reserved too, so they cannot be identifiers either. Spaces are never allowed. Valid: `marks1`, `_temp`, `$price`, `studentName`. Invalid: `1stYear` (starts with a digit), `class` (keyword), `my-name` (hyphen is the minus operator), `total marks` (space).

**Naming conventions** (not enforced by the compiler, but followed by every Java team and expected in lab work):

| Kind | Convention | Example |
|---|---|---|
| Class, interface, enum, record | `UpperCamelCase`, usually a noun | `LoanAccount`, `Comparable` |
| Method, variable | `lowerCamelCase`; methods usually start with a verb | `computeInterest`, `rollNo` |
| Constant (`static final`) | `UPPER_SNAKE_CASE` | `MAX_SEATS`, `PI` |
| Package | all lower case, reversed domain | `np.edu.tu.library` |

**Literals in detail.** Integer literals are `int` unless they end with `L` (`long`): `100`, `5_000_000L` (underscores are allowed for readability), `0b1010` (binary, = 10), `017` (octal, = 15) and `0xFF` (hexadecimal, = 255). Floating literals are `double` unless they end with `f`: `2.5`, `1.5e3` (= 1500.0), `2.5f`. A `char` literal uses single quotes and may be an escape: `'\n'` (newline), `'\t'` (tab), `'\\'`, `'\''`, or a Unicode escape such as `'\u0905'`, which is the Devanagari letter अ. A `String` literal uses double quotes. Since Java 15 a **text block** `"""..."""` holds several lines without escapes.

```java
public class Tokens {
    public static void main(String[] args) {
        int bin = 0b1010, oct = 017, hex = 0xFF, big = 5_000_000;
        long population = 29_164_578L;
        double sci = 1.5e3;
        float f = 2.5f;
        char devanagari = '\u0905';
        var $price = 99.5;
        int _count = 3;
        System.out.println(bin + " " + oct + " " + hex + " " + big);
        System.out.println(population + " " + sci + " " + f);
        System.out.println(devanagari + " " + (int) devanagari);
        System.out.println($price * _count);
        System.out.println('a' + 1);
        System.out.println((char) ('a' + 1));
        System.out.println("Tab:\t|" + " Quote:\" Backslash:\\");
    }
}
```

```output
10 15 255 5000000
29164578 1500.0 2.5
अ 2309
298.5
98
b
Tab:	| Quote:" Backslash:\
```

The output shows the literal values converted to decimal (`10 15 255 5000000`), the Devanagari letter together with its Unicode number 2309, and the classic surprise `'a' + 1`: a `char` in arithmetic is promoted to `int`, so the result is the number 98, and only the cast `(char)` turns it back into the letter `b`. Note also that `System.out.println(1 + 2 + "x")` prints `3x` while `"x" + 1 + 2` prints `x12`, because `+` is evaluated left to right and becomes concatenation as soon as one operand is a `String`.

**Primitive default values.** Fields (not local variables) get automatic defaults: `0` for `byte`, `short`, `int`, `long`; `0.0` for `float`, `double`; `'\u0000'` for `char`; `false` for `boolean`; `null` for every reference type. **Local variables have no default**: using one before assigning it is a compile-time error ("variable might not have been initialized"), a rule that catches many bugs before the program runs.

## 1.9 Garbage collection: how an object's life ends

In C you call `free()`; in Java there is no `delete`. The **garbage collector (GC)**, a background service of the JVM, finds objects that the program can no longer reach and reclaims their memory. This removes two whole families of bugs (memory leaks from forgotten `free()`, and crashes from using freed memory), which is why the list of Java's features in 1.7 includes "automatic memory management".

**Reachability, not reference counting.** An object is *alive* if it can be reached from a **GC root** by following references: local variables on a thread's stack, static fields, and active threads. Everything else is garbage, even objects that point to each other in a cycle. When `Student s = new Student("Sita"); s = null;` runs, the `Student` object has no remaining route from any root and becomes **eligible** for collection. Eligible does not mean "collected now": the JVM decides when.

```java
public class Gc {
    static class Node {
        String name; Node next;
        Node(String n) { name = n; }
    }
    public static void main(String[] args) {
        Node a = new Node("A");
        Node b = new Node("B");
        a.next = b;
        b.next = a;
        System.out.println(a.next.next.name);
        a = null;
        b = null;
        System.out.println("A and B point to each other, yet both are unreachable now");
        Runtime rt = Runtime.getRuntime();
        System.out.println(rt.maxMemory() > rt.totalMemory() / 2);
        System.out.println(rt.freeMemory() <= rt.totalMemory());
    }
}
```
```output
A
A and B point to each other, yet both are unreachable now
true
true
```

The two nodes form a cycle, so a reference-counting scheme would never free them; the Java collector does, because no *root* reaches either one.

**Generations.** Most objects die young (a temporary `String`, a loop's `Integer`). HotSpot therefore divides the heap into a **young generation** (new objects are born in *Eden*; survivors are copied between two small *survivor* spaces and their **age** is incremented) and an **old generation** (objects that survive several young collections are promoted). A *minor GC* cleans only the young generation and is fast; a *major* or *full GC* cleans everything and may pause the program. The method area (called **Metaspace** since Java 8) holds class metadata.

| Collector | Idea | Typical use |
|---|---|---|
| Serial | one thread, stop-the-world | tiny programs, single core |
| Parallel | many threads collect together | throughput-oriented batch jobs |
| G1 (default since Java 9) | the heap is split into regions; collects the most garbage-filled regions first | general servers |
| ZGC, Shenandoah | concurrent, pause time of a millisecond or less | very large heaps, latency-sensitive services |

**What the programmer controls.** `System.gc()` is only a *request*; the JVM may ignore it, and calling it in production code is a poor practice. The `finalize()` method was once used for cleanup but is **deprecated for removal** (it is unpredictable and slows collection); use **try-with-resources** (`AutoCloseable`) for files, sockets and connections, because the GC reclaims *memory* but knows nothing about *file handles*. Java can still leak memory logically: a static `List` that keeps growing, a listener that is never removed, or a cache without a size limit keeps objects *reachable* and therefore alive. For caches, `WeakReference` and `WeakHashMap` hold objects that the GC may reclaim when nothing else refers to them.

::: tip Exam answer in four lines
Garbage collection is the automatic reclamation of memory held by unreachable objects. An object becomes eligible when no live thread can reach it, for example after its only reference is set to `null` or goes out of scope. The collector runs when the JVM chooses, working mostly on the young generation; `System.gc()` is merely a hint. It frees memory but not other resources, so files must still be closed with try-with-resources.
:::

## Formula and fact sheet

- Pillars: encapsulation, abstraction, inheritance, polymorphism.
- Source `.java` → `javac` → bytecode `.class` → JVM. JDK ⊃ JRE ⊃ JVM.
- `int` 32-bit, `long` 64-bit, `double` 64-bit, `char` 16-bit Unicode; integer division truncates; overflow wraps.
- Narrowing needs a cast; `(byte) 200 = −56`.
- Arrays: zero-based, bounds-checked, `length` field.
- `Scanner` for input; consume the newline after `nextInt`.

## Chapter summary

- OOP organises programs around objects that combine state and behaviour, with four guiding pillars.
- Java compiles to bytecode that the JVM runs; the garbage collector manages memory.
- Primitive types are fixed-size and overflow silently; reference types are objects on the heap.
- Control statements, arrays and formatted I/O are the foundation for the class design of the next unit.

## Practice

1. Differentiate procedural and object-oriented programming. Explain encapsulation with an example.
2. Differentiate JDK, JRE and JVM. Explain how Java achieves platform independence.
3. Predict the output: `System.out.println(5 / 2 + " " + 5 % 2 + " " + 5 / 2.0 + " " + (char)('a' + 1));`
4. What does `int x = Integer.MAX_VALUE; x++;` do? What does `(int) 3.99` give?
5. Write a program that finds the second largest element of an `int[]`.
6. Write a program that prints a multiplication table of 7 up to 10 using `printf`.
7. Write a method `static boolean isPrime(int n)` and use it to list the primes below 30.
8. Why does `"a" + 1 + 2` give `a12` but `1 + 2 + "a"` give `3a`?
9. Explain widening and narrowing conversions with examples.
10. Differentiate `==` and `equals` for `String`.

::: note Answers and worked solutions
**1.** Procedural: functions and data separate; OOP: objects bundle both. Encapsulation: a `BankAccount` keeps `balance` private and changes it only via `deposit()` and `withdraw()`, which enforce the rules.
**2.** JVM executes bytecode; JRE = JVM + libraries; JDK = JRE + compiler and tools. The compiler produces platform-neutral bytecode and each platform supplies its own JVM.
**3.** `2 1 2.5 b`
**4.** It overflows to −2147483648 (the minimum). `(int) 3.99` is **3** (truncation, not rounding).
**5.** Track `first` and `second`; for each x: if x > first { second = first; first = x; } else if x > second && x != first { second = x; }.
**6.** `for (int i = 1; i <= 10; i++) System.out.printf("7 x %2d = %3d%n", i, 7 * i);`
**7.** `if (n < 2) return false; for (int i = 2; (long) i * i <= n; i++) if (n % i == 0) return false; return true;` Primes below 30: 2 3 5 7 11 13 17 19 23 29.
**8.** `+` is left-associative: `"a" + 1` is the string "a1", then "a12". In `1 + 2 + "a"`, 1 + 2 is integer addition (3) first.
**9.** Widening goes to a larger type automatically (`long l = 5;`); narrowing needs a cast and may lose data (`int i = (int) 9.8;` gives 9).
**10.** `==` compares references (whether both names point to the same object); `equals` compares the characters. Always use `equals` to compare string contents.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Differentiate JDK, JRE and JVM, and explain how Java achieves platform independence.**

*Introduction.* Java is compiled and interpreted: the source file becomes bytecode, and the bytecode is run by a virtual machine. Three terms describe the layers of this system.

*The three layers.*

1. **JVM (Java Virtual Machine).** It loads, verifies and executes bytecode, with a JIT compiler for speed and a garbage collector for memory. The JVM itself is different for each operating system.
2. **JRE (Java Runtime Environment).** The JVM plus the standard class libraries (`java.lang`, `java.util` and others). It is what a user needs to run a program.
3. **JDK (Java Development Kit).** The JRE plus development tools: `javac`, `jar`, `javadoc` and `jshell`. A programmer needs it to write programs.

| Term | Contains | Used by |
|---|---|---|
| JVM | bytecode executor, GC, JIT | the machine |
| JRE | JVM + class libraries | end user |
| JDK | JRE + compiler and tools | developer |

*Platform independence.* `javac` turns `Hello.java` into `Hello.class`, bytecode for an imaginary processor (Figure 1.1). Each platform supplies a JVM that understands this bytecode, so the **same** `.class` file runs on Windows, Linux or macOS. Only the JVM is platform-specific; the program is not.

*Conclusion.* JDK contains JRE, which contains JVM (JDK ⊃ JRE ⊃ JVM). Bytecode plus a JVM per platform gives "write once, run anywhere".

**Q2 (10 marks). Explain the four pillars of object-oriented programming with a Java program, and differentiate procedural and object-oriented programming.**

*Introduction.* Object-oriented programming (OOP) organises a program as objects that combine data (fields) and behaviour (methods). A class is the blueprint and an object is one instance. Four ideas guide good design: encapsulation, abstraction, inheritance and polymorphism (Figure 1.2).

*The four pillars.*

1. **Encapsulation.** Fields are `private` and changed only through methods that enforce rules. In the program, `balance` can change only through `deposit`, which rejects zero or negative amounts.
2. **Abstraction.** `Account` is abstract: it states that every account has a `monthlyEffect()` without saying how it is calculated.
3. **Inheritance.** `Savings` and `Current` extend `Account` and reuse `deposit` and `applyMonth` (an *is-a* relation).
4. **Polymorphism.** The loop calls `applyMonth()` on each `Account`; at run time Java picks the version belonging to the real object (dynamic dispatch).

```java
import java.util.List;

public class BankDemo {
    static abstract class Account {
        private double balance;
        protected final String owner;
        Account(String owner, double opening) { this.owner = owner; this.balance = opening; }
        void deposit(double a) {
            if (a <= 0) throw new IllegalArgumentException("deposit must be positive");
            balance += a;
        }
        double getBalance() { return balance; }
        abstract double monthlyEffect();
        void applyMonth() { balance += monthlyEffect(); }
    }
    static class Savings extends Account {
        Savings(String o, double b) { super(o, b); }
        double monthlyEffect() { return getBalance() * 0.04 / 12; }
    }
    static class Current extends Account {
        Current(String o, double b) { super(o, b); }
        double monthlyEffect() { return -50; }
    }
    public static void main(String[] args) {
        List<Account> list = List.of(new Savings("Sita", 10000), new Current("Ram", 5000));
        list.get(0).deposit(2000);
        try { list.get(1).deposit(-5); } catch (IllegalArgumentException e) { System.out.println("Rejected: " + e.getMessage()); }
        for (Account a : list) {
            a.applyMonth();
            System.out.printf("%-5s %-8s %9.2f%n", a.owner, a.getClass().getSimpleName(), a.getBalance());
        }
    }
}
```
```output
Rejected: deposit must be positive
Sita  Savings   12040.00
Ram   Current    4950.00
```

The output shows encapsulation (the bad deposit is rejected) and polymorphism (Sita gains 40.00 interest on 12,000, Ram pays a 50.00 fee, from one loop).

*Procedural versus object-oriented.*

| Point | Procedural (C) | Object-oriented (Java) |
|---|---|---|
| Unit of design | function | class and object |
| Data and code | kept separate | bundled together |
| Data hiding | weak (global data) | strong (`private`) |
| Reuse | copy or call functions | inheritance, composition |
| Change | edits spread widely | changes stay inside a class |

*Conclusion.* The four pillars make programs easier to extend and protect their data; Java enforces them with `private`, `abstract`, `extends` and overriding.

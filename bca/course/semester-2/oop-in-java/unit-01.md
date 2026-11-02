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

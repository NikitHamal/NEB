# OOP in Java — BCA 153 (Semester II, 3 credits)

In the 2074 curriculum this was CACS204 in Semester III; the revised curriculum moves it to Semester II.

| Unit | Title |
|---|---|
| 1 | Object-Oriented Concepts and Java Fundamentals |
| 2 | Classes, Objects, Constructors and Encapsulation |
| 3 | Inheritance, Polymorphism, Abstract Classes and Interfaces |
| 4 | Exception Handling, Strings and Wrapper Classes |
| 5 | Generics, Collections, Lambdas, Streams and File I/O |
| 6 | Multithreading, GUI Event Handling and Database Access |
| 7 | Design Patterns and Advanced OOP Concepts (singleton, factory, observer, copy constructors, nested classes, jagged arrays, varargs, lambdas, `Optional`) |

## Verification

All programs were compiled and run with OpenJDK 17 by `bca/tools/check_java_examples.py bca/course/semester-2/oop-in-java`; each `output` block is the real output (one value, the file size in unit 5, was predicted wrongly in the first draft, was caught by this check and corrected). The Swing program (unit 6) and the JDBC program are compile-checked only because they need a display and a database server.

## Source and honesty

**The unit structure is reconstructed** from the usual content of TU's Java course (CACS204) and what the secondary sources list; the revised BCA 153 PDF was not retrievable. Hours per unit are not stated. Applets and RMI, which appear in some older Java syllabi, are omitted because they are obsolete.


## Session 21 update: current TU syllabus check

The current TU outline (checked against hamronotes.com and benchpartner.com chapter lists) has 8 units: Java and OOP concepts; Java basics (tokens, arrays, strings, `StringBuffer`, garbage collection); classes and objects (constructors including copy constructors, `this`, `static`, passing, recursion, nested and inner classes, varargs, packages); inheritance and polymorphism; exceptions and multithreading; file handling; collections and generics; advanced OOP (singleton, factory, observer, lambda, Stream API, `Optional`, method references). Units 1 to 6 of this book already cover all of these except **design patterns, copy constructors, inner classes and jagged arrays**, which are now Unit 7 (all 8 programs compiled and run with OpenJDK by `fill_java_outputs.py`). The book keeps its own unit order (collections, lambdas and file I/O are in Unit 5) because the content, not the numbering, is what the exam tests.

# Programming in C — BCA 102 (old code CACS151)

Semester I (revised curriculum, 2082 batch) · 3 credits. For students on the 2074 curriculum this is CACS151 (4 credits, Semester II).

## What is in this book

| Unit | Title | Syllabus topics covered |
|---|---|---|
| 1 | Problem Solving with a Computer, and the Shape of a C Program | programming languages, algorithms, pseudocode, flowcharts, history of C, structure of a C program, compile/link/run, errors and debugging |
| 2 | Elements of C: Tokens, Data Types, Operators and Console I/O | character set, tokens, data types, constants, variables, operators and precedence, type conversion, `printf`/`scanf`, `getchar`/`putchar` |
| 3 | Control Statements | `if`, `else-if`, `switch`, `for`, `while`, `do-while`, `break`, `continue`, `goto`, nested loops and patterns |
| 4 | Arrays and Strings | 1-D and 2-D arrays, searching, sorting, matrices, string library, string handling |
| 5 | Functions, Recursion and Storage Classes | prototypes, call by value, arrays as arguments, recursion, scope, `auto`/`static`/`extern`/`register` |
| 6 | Pointers and Dynamic Memory Allocation | `&`/`*`, pointer arithmetic, pointers and arrays/strings, array of pointers, pointer to pointer, `malloc`/`calloc`/`realloc`/`free` |
| 7 | Structures, Unions and File Handling | structures, nested/array of structures, unions, enum, preprocessor, text and binary files, random access |

Each unit has worked examples, a formula and fact sheet, a chapter summary and a practice set (short questions, predict-the-output, programs) **with worked answers**.

## How this was verified

Every complete program in the book (26 of them) is compiled with `gcc -std=c11 -Wall` and run by `bca/tools/check_c_examples.py`, which compares the real output with the output printed in the book. The checker caught two programs whose output depended on the unspecified order of evaluation of function arguments; both were rewritten. All predict-the-output questions in units 2–4 were also compiled and run to confirm the answer key.

## Source and honesty

The unit structure follows the TU C-programming syllabus family (the TU IOST 10-unit "C Programming" outline: Introduction, Elements of C, I/O, Control, Arrays and Strings, Functions, Pointers, Structure and Union, File Handling) and the BCA 2074 CACS151 course description. **The revised BCA 102 syllabus PDF itself could not be retrieved**, so the topic list was matched to the older BCA and the IOST syllabi rather than to the new PDF. If your college's syllabus lists a topic not found here (for example bit-fields or graphics functions), tell us.

Examples use C11 and the GCC compiler; Turbo C (16-bit, 2-byte `int`) differences are called out where an older exam answer would differ.

## Study plan (4 weeks, 1 to 2 hours a day)

1. Week 1: units 1–2. Type every example; change a value and predict the new output before you run it.
2. Week 2: units 3–4. Do all the pattern and array programs without notes.
3. Week 3: units 5–6. Trace recursion on paper; draw boxes and arrows for every pointer exercise.
4. Week 4: unit 7, then redo every "predict the output" question and all the programs from memory.

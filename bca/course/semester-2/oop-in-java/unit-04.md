---
subject: OOP in Java
grade: BCA Semester 2
unit: 4
title: Exception Handling, Strings and Wrapper Classes
area: BCA 153 · OOP in Java · Unit 4
---

Programs meet errors: bad input, missing files, broken networks. Java makes error handling a structured part of the language through **exceptions**. This unit covers the exception hierarchy, `try`/`catch`/`finally`, custom exceptions and try-with-resources, then the string classes and the wrapper classes that every program uses.

::: key What this unit gives you
- The `Throwable` hierarchy; checked versus unchecked exceptions.
- `try`/`catch`/`finally`, `throw`/`throws`, multi-catch, custom exceptions, try-with-resources.
- `String` immutability, the string pool, `StringBuilder`, common methods and `regex`.
- Wrapper classes, autoboxing, `Math`, and date/time basics.
:::

## 4.1 Exceptions

An **exception** is an object that represents an abnormal event; when one is **thrown**, normal flow stops and the JVM looks up the call stack for a matching **handler**; if none exists the thread ends and prints a stack trace.

```text
Throwable
├── Error                      (JVM problems: OutOfMemoryError, StackOverflowError; do not catch)
└── Exception
    ├── IOException, SQLException, InterruptedException …   CHECKED: must be caught or declared
    └── RuntimeException                                     UNCHECKED
        ├── NullPointerException, ArithmeticException
        ├── ArrayIndexOutOfBoundsException, ClassCastException
        └── IllegalArgumentException (NumberFormatException), IllegalStateException
```

- **Checked** exceptions are recoverable conditions outside the program's control (a missing file); the compiler forces you to handle or declare them with `throws`.
- **Unchecked** (`RuntimeException`) exceptions are usually programming bugs; fix the code instead of catching.

```java
class InsufficientFundsException extends Exception {
    InsufficientFundsException(String m) { super(m); }
}
class Res implements AutoCloseable {
    String n;
    Res(String n) { this.n = n; System.out.println("open " + n); }
    public void close() { System.out.println("close " + n); }
}
public class Errors {
    static void withdraw(double bal, double amt) throws InsufficientFundsException {
        if (amt > bal) throw new InsufficientFundsException("Need " + (amt - bal) + " more");
    }
    @SuppressWarnings("finally")
    static int f() { try { return 1; } finally { System.out.println("finally runs"); } }
    public static void main(String[] a) {
        try { withdraw(100, 150); } catch (InsufficientFundsException e) { System.out.println(e.getMessage()); }
        try { int[] x = new int[2]; x[2] = 1; } catch (ArrayIndexOutOfBoundsException e) { System.out.println("AIOOBE: " + e.getMessage()); }
        try { Integer.parseInt("12x"); } catch (NumberFormatException e) { System.out.println(e.getMessage()); }
        try (Res r1 = new Res("A"); Res r2 = new Res("B")) { System.out.println("body"); }
        System.out.println(f());
        String s = null;
        try { s.length(); } catch (NullPointerException e) { System.out.println("NPE"); }
        try { System.out.println(10 / (a.length)); } catch (ArithmeticException e) { System.out.println("Arithmetic: " + e.getMessage()); }
    }
}
```
```output
Need 50.0 more
AIOOBE: Index 2 out of bounds for length 2
For input string: "12x"
open A
open B
body
close B
close A
finally runs
1
NPE
Arithmetic: / by zero
```

**Rules and idioms**

- `try` needs at least one `catch` or a `finally`. **`finally`** always runs (even after `return`), so use it to release resources; **try-with-resources** closes `AutoCloseable` resources automatically, in reverse order, as seen above.
- Catch **specific** exceptions first, general last; multi-catch: `catch (IOException | SQLException e)`.
- `throw new X(…)` raises; `throws X` in a method signature declares; **rethrow** or wrap: `throw new ServiceException("load failed", e)` preserves the **cause**.
- Never swallow exceptions silently (`catch (Exception e) {}`); log them or rethrow. Do not use exceptions for ordinary control flow.
- A method overriding another cannot declare broader checked exceptions.
- **Stack trace** reads top-down: the first line is where it was thrown, the lines below are the callers. `e.printStackTrace()` for diagnostics.
- **Assertions** (`assert x > 0 : "msg";`, enabled with `java -ea`) check internal invariants during testing.

### Exceptions as circuit breakers

A circuit breaker cuts one faulty circuit so the rest of the house keeps its power. An exception handler does the same for a program: the fault is thrown, caught at a chosen place, and the other work goes on. Java's own rules decide which exception a fault raises. Plate 4.1 lists five everyday faults, the exception each one throws and whether it is checked (the compiler forces you to handle it) or unchecked.

```photogrid label="4.1" cols="2" ratio="1.0" caption="Isolate the fault. (a) A household breaker panel: a fault trips one breaker and the other circuits keep working. (b) Five common faults, the exception Java throws for each, and whether it is checked or unchecked; only the IOException family must be handled or declared."
@ photo id="bca153/breaker" cap="Breaker panel: one fault is cut off, the rest continue"
fit 1.0
focus 0.5 0.5
@ svg cap="Fault, exception, checked or unchecked"
rows = [("10 / 0 (int)", "ArithmeticException", False), ("Integer.parseInt(\"abc\")", "NumberFormatException", False), ("arr[5] on 3 cells", "ArrayIndexOutOfBounds", False), ("s.length() when s is null", "NullPointerException", False), ("new FileReader(\"x.txt\") missing", "FileNotFoundException", True)]
assert sum(1 for *_, c in rows if c) == 1
f = Fig(400, 250)
f.text(200, 16, "Fault and the exception it throws", size=11, color=NAVY, bold=True)
for i, (a, b, c) in enumerate(rows):
    y = 28 + i * 40
    f.box(6, y, 388, 34, "", fill=ROSE if c else MINT, stroke=RED if c else TEAL, r=4)
    f.text(12, y + 11, a, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(12, y + 25, b, size=10.5, color=SLATE, anchor="start", vmid=True)
    f.text(386, y + 17, "checked" if c else "unchecked", size=10.5, color=RED if c else TEAL, bold=True, anchor="end", vmid=True)
f.text(200, 238, "Unchecked = RuntimeException family; checked = must catch or declare.", size=10.5, color=SLATE)
```

## 4.2 Strings

`String` is an **immutable** sequence of UTF-16 characters: no method changes it, they return a new string. Because of this, string literals can be shared in the **string pool**.

```java
public class Strings {
    public static void main(String[] a) {
        String s1 = "hello", s2 = "hel" + "lo", s3 = new String("hello");
        System.out.println((s1 == s2) + " " + (s1 == s3) + " " + s1.equals(s3));
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5; i++) sb.append(i).append(',');
        sb.setLength(sb.length() - 1);
        System.out.println(sb.reverse());
        System.out.println(String.join("-", "a", "b", "c") + " " + "a,b,,c".split(",").length);
        System.out.println("Java".compareTo("Jav") + " " + "b".compareTo("a"));
        System.out.println(String.valueOf(3.5) + 1 + 2);
        System.out.println("  Trim Me ".strip().toLowerCase().replace('m', 'n').contains("tri"));
        System.out.println("banana".indexOf("an") + " " + "banana".lastIndexOf("an") + " " + "banana".chars().filter(c -> c == 'a').count());
        System.out.println("madam".contentEquals(new StringBuilder("madam").reverse()));
    }
}
```
```output
true false true
4,3,2,1,0
a-b-c 4
1 1
3.512
true
1 3 3
true
```

| Class | Mutable | Thread-safe | Use |
|---|---|---|---|
| `String` | no | yes (immutable) | fixed text, keys |
| `StringBuilder` | yes | no | building strings in a loop (fast) |
| `StringBuffer` | yes | yes (synchronised) | legacy shared use |

**Why `StringBuilder`:** `s += x` in a loop creates a new string each time, giving O(n²) copying; a builder appends in amortised O(1).

Frequent methods: `length`, `charAt`, `substring(i, j)`, `indexOf`, `lastIndexOf`, `contains`, `startsWith`, `endsWith`, `equals`, `equalsIgnoreCase`, `compareTo`, `toUpperCase`, `toLowerCase`, `trim`/`strip`, `replace`, `split(regex)`, `isEmpty`/`isBlank`, `format`, `join`, `repeat`, `toCharArray`, `String.valueOf(x)`. **Text blocks** (`"""…"""`) hold multi-line text. **Regular expressions** (`java.util.regex`): `"2082-05-14".matches("\\d{4}-\\d{2}-\\d{2}")` is true; `Pattern`/`Matcher` find groups. Since `==` compares references, **always use `equals`** for content.

### Strings are shared, and never change

The Java string pool keeps one copy of each literal, so identical literals are one object, like identical containers stacked in a yard that all hold the same standard cargo. `new String("NEB")` deliberately makes a second object, so `==` between them is false although `equals` is true. Strings are immutable, so `s = s + x` in a loop builds a new string each time and copies all the old characters; for n appends that is 1 + 2 + ... + n copies, against only n for a `StringBuilder`. Plate 4.2 shows both facts.

```photogrid label="4.2" cols="2" ratio="1.4" caption="Shared and unchangeable. (a) Stacked shipping containers: identical standard units. (b) String comparisons for the literal NEB (same pool object, new String creates another) and the number of character copies when appending one character n times: string concatenation copies n(n+1)/2 characters, StringBuilder about n."
@ photo id="bca153/containers" cap="Standard containers: identical units shared by everyone"
fit 1.4
focus 0.5 0.5
@ svg cap="String pool and the cost of concatenation"
cmp = [("\"NEB\" == \"NEB\"", "true", "one pool object", TEAL, MINT), ("new String(\"NEB\") == \"NEB\"", "false", "two objects", RED, ROSE), ("new String(\"NEB\").equals(\"NEB\")", "true", "same characters", TEAL, MINT)]
cp = {n: n * (n + 1) // 2 for n in (10, 100, 1000)}
assert cp == {10: 55, 100: 5050, 1000: 500500}
f = Fig(400, 250)
for i, (a, v, why, st, fl) in enumerate(cmp):
    y = 8 + i * 38
    f.box(6, y, 388, 32, "", fill=fl, stroke=st, r=4)
    f.text(12, y + 10, a, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(12, y + 23, why, size=10.5, color=SLATE, anchor="start", vmid=True)
    f.text(386, y + 16, v, size=12, color=st, bold=True, anchor="end", vmid=True)
f.text(200, 136, "Characters copied by s = s + \"x\" (n times)", size=10.5, color=NAVY, bold=True)
for i, (n, c) in enumerate(cp.items()):
    y = 146 + i * 30
    f.text(10, y + 10, f"n = {n:,}", size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    w = max(c / 500500 * 200, 4)
    f.box(80, y, w, 12, "", fill=ROSE, stroke=RED, r=2); f.text(86 + w, y + 6, f"{c:,}", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
    f.box(80, y + 14, max(n / 500500 * 200, 3), 8, "", fill=MINT, stroke=TEAL, r=1); f.text(90 + max(n / 500500 * 200, 3), y + 18, f"StringBuilder: about {n:,}", size=10.5, color=TEAL, anchor="start", vmid=True)
```

## 4.3 Wrapper classes, `Math`, dates

Each primitive has a wrapper: `Integer`, `Long`, `Double`, `Boolean`, `Character` (…). They are needed for generics (`List<Integer>`), carry utilities (`Integer.parseInt("42")`, `Integer.toBinaryString(10)` = `"1010"`, `Integer.MAX_VALUE`, `Double.compare`, `Character.isDigit`) and may be `null`. **Autoboxing/unboxing** is automatic, and unboxing a `null` throws `NullPointerException`. Caution: `Integer a = 127, b = 127; a == b` is true (cache of −128…127) but with 1000 it is false; use `equals`.

`Math`: `abs`, `pow`, `sqrt`, `max`, `min`, `round`, `floor`, `ceil`, `random`, `hypot`; `Math.floorMod(-7, 3)` is 2 whereas `-7 % 3` is −1. For **money** use `java.math.BigDecimal`, not `double` (0.1 + 0.2 is 0.30000000000000004). Dates: `java.time.LocalDate.of(2026, 5, 14).plusDays(30)`, `LocalDateTime`, `Duration`, `DateTimeFormatter`; avoid the old `Date`.

## 4.4 Two pictures: the exception family and the string pool

Every error in Java is an object of a class under `Throwable` (Figure 4.1). **Errors** such as `OutOfMemoryError` signal that the JVM itself is in trouble and are not normally caught. **Exceptions** are problems a program can handle. Those under `RuntimeException` are **unchecked** (programming bugs such as a bad index or a null reference); every other exception, such as `IOException`, is **checked**, and the compiler forces you to catch it or declare it with `throws`. Figure 4.2 explains why strings need care: a `String` never changes, and identical literals share one object in the **string pool**, whereas `new String("nepal")` always creates another object on the heap. That is why `==` on strings is unreliable and `equals` must be used.

```svgfig label="4.1" caption="The Throwable family. Checked exceptions (amber) must be caught or declared; unchecked exceptions (green) and errors need not be. A try block may be followed by several catch blocks and one finally block that always runs."
f = Fig(600, 250)
f.box(230, 10, 140, 34, "Throwable", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(90, 78, 110, 34, "Error", fill="#fecaca", stroke=RED, color=NAVY, size=11, bold=True)
f.box(300, 78, 120, 34, "Exception", fill=BLUE, color=NAVY, size=11, bold=True)
f.arrow([(300, 44), (300, 62), (145, 62), (145, 78)], color=SLATE, sw=1.6)
f.arrow([(300, 44), (360, 78)], color=SLATE, sw=1.6)
f.box(210, 150, 120, 40, "IOException\nSQLException", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.box(380, 150, 140, 40, "RuntimeException", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10.5, bold=True)
f.arrow([(340, 112), (340, 130), (270, 130), (270, 150)], color=SLATE, sw=1.6)
f.arrow([(380, 112), (380, 130), (450, 130), (450, 150)], color=SLATE, sw=1.6)
f.box(10, 150, 170, 40, "OutOfMemoryError\nStackOverflowError", fill="#ffffff", stroke=RED, color=NAVY, size=10, bold=True)
f.arrow([(145, 112), (145, 150)], color=SLATE, sw=1.6)
f.text(450, 208, "NullPointerException, ArithmeticException,", size=10, color=NAVY, bold=True)
f.text(450, 222, "ArrayIndexOutOfBounds, NumberFormatException", size=10, color=NAVY, bold=True)
f.text(270, 208, "checked", size=10.5, color=AMBER, bold=True)
f.text(95, 208, "not caught normally", size=10.5, color=RED, bold=True)
f.text(450, 240, "unchecked", size=10.5, color=TEAL, bold=True)
```

```svgfig label="4.2" caption="String pool. The literals a and b share one pooled object, so a == b is true. new String(...) makes a separate heap object, so a == c is false even though equals gives true. intern() returns the pooled copy."
f = Fig(600, 220)
f.text(90, 16, "Variables", size=11.5, color=NAVY, bold=True)
f.text(400, 16, "Memory", size=11.5, color=NAVY, bold=True)
for i, (n, c) in enumerate((("a", BLUE), ("b", BLUE), ("c", "#fde68a"))):
    f.box(40, 34 + i * 50, 100, 34, n, fill=c, color=NAVY, size=12, bold=True)
f.box(290, 28, 250, 60, "", fill="#bbf7d0", stroke=TEAL)
f.text(415, 44, "String pool", size=10.5, color=TEAL, bold=True)
f.text(415, 68, "\"nepal\"  (one shared object)", size=11.5, color=NAVY, bold=True)
f.box(290, 118, 250, 56, "", fill="#fde68a", stroke=AMBER)
f.text(415, 134, "Heap (new String)", size=10.5, color=AMBER, bold=True)
f.text(415, 156, "\"nepal\"  (separate object)", size=11.5, color=NAVY, bold=True)
f.arrow([(140, 51), (290, 56)], color=TEAL, sw=1.8)
f.arrow([(140, 101), (290, 66)], color=TEAL, sw=1.8)
f.arrow([(140, 151), (290, 146)], color=AMBER, sw=1.8)
f.text(300, 205, "a == b true  |  a == c false  |  a.equals(c) true  |  c.intern() == a true", size=11, color=RED, bold=True)
```

## 4.5 Eight benefits of exception handling and of immutable strings

1. **Programs survive errors.** A caught exception lets the program recover, for example by asking the user for a new file name. Without it the program would stop at the first problem. A bank's mobile app must not crash because one request had a bad value.
2. **Error code is separated from normal code.** The `try` block holds the main logic and the `catch` blocks hold the repair. The normal path stays easy to read instead of being buried under many `if` checks.
3. **Errors travel upward.** If a method cannot handle a problem it lets the exception pass to the caller, which may know what to do. A low-level file reader can report failure and the screen code can show a message to the user.
4. **Compiler-enforced care.** Checked exceptions force the programmer to plan for failures such as a missing file or a network break. This reduces nasty surprises after deployment.
5. **Clean-up is guaranteed.** The `finally` block, or try-with-resources, always runs, so files and database connections are closed. This prevents resource leaks in a server that runs for weeks.
6. **Meaningful custom errors.** You can define your own exception, such as `InsufficientFundsException`, with a clear message. Support staff then see exactly what went wrong instead of a vague failure.
7. **Safe sharing of strings.** Because a `String` can never change, many parts of a program can share one object without surprises. This also makes strings safe as keys in a `HashMap` and safe between threads.
8. **Memory and speed savings.** The string pool stores each distinct literal once, and the hash code of a string is cached. A program that uses the word "Kathmandu" thousands of times keeps just one copy.

## Formula and fact sheet

- Checked: must handle or declare. Unchecked (`RuntimeException`): bugs. `Error`: do not catch.
- `finally` always runs; try-with-resources closes in reverse order.
- Catch specific before general; never swallow; keep the cause when wrapping.
- `String` immutable; `==` compares references, `equals` compares content; use `StringBuilder` in loops.
- Wrapper cache −128…127; unboxing `null` → NPE. Use `BigDecimal` for money.

## Chapter summary

- Exceptions separate error handling from normal logic; the compiler enforces handling of checked ones.
- `try-with-resources` and `finally` guarantee clean-up.
- Strings are immutable shared objects; builders make repeated modification efficient.
- Wrapper classes bridge primitives and objects, with pitfalls around `null` and `==`.

## Practice

1. Differentiate checked and unchecked exceptions with two examples each.
2. What is the output of a method with `try { return 1; } finally { print("F"); }`?
3. Write a custom checked exception `InvalidAgeException` and a method that throws it for age < 0 or > 120.
4. Explain try-with-resources and why it is better than `finally` for closing a file.
5. Why is `String` immutable? Give two benefits.
6. Compare the time to build a string of 100,000 characters with `+=` and with `StringBuilder`.
7. Write a method that checks whether a string is a palindrome ignoring case and spaces.
8. Count the words in a sentence using `split("\\s+")`.
9. Why is `new Integer(5) == new Integer(5)` false while `Integer.valueOf(5) == Integer.valueOf(5)` is true?
10. Compute 0.1 + 0.2 with `double` and with `BigDecimal` and explain the difference.

::: note Answers and worked solutions
**1.** Checked: `IOException`, `SQLException` (compile-time enforced). Unchecked: `NullPointerException`, `ArrayIndexOutOfBoundsException` (bugs).
**2.** Prints `F`, then the method returns 1.
**3.** `class InvalidAgeException extends Exception { InvalidAgeException(String m){ super(m);} }` and `static void check(int age) throws InvalidAgeException { if (age < 0 || age > 120) throw new InvalidAgeException("Invalid age: " + age); }`.
**4.** Resources declared in the `try (…)` header are closed automatically, in reverse order, even on exceptions, and exceptions from `close()` are attached as *suppressed* rather than hiding the original one.
**5.** Immutability makes strings safe to share between threads and to use as hash keys, and it allows the string pool to save memory (also security: a file name cannot change after checking).
**6.** `+=` copies the whole string on each append: about n²/2 = 5 × 10⁹ character copies for n = 100,000 (seconds); `StringBuilder` is linear (milliseconds).
**7.** `String t = s.replaceAll("\\s+", "").toLowerCase(); return new StringBuilder(t).reverse().toString().equals(t);`
**8.** `sentence.trim().split("\\s+").length` (guard against an empty string).
**9.** `new` always creates a distinct object; `valueOf` returns cached objects for −128…127.
**10.** `0.1 + 0.2` as `double` is 0.30000000000000004 because binary floating point cannot represent 0.1 exactly. `new BigDecimal("0.1").add(new BigDecimal("0.2"))` is exactly 0.3 (always build from strings).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain exception handling in Java with try, catch, finally, throw and throws. Distinguish checked and unchecked exceptions.**

*Introduction.* An exception is an object that represents an abnormal event during execution. Exception handling lets a program deal with it without crashing (Figure 4.1).

*Keywords.*

1. **`try`.** Encloses code that may fail.
2. **`catch`.** Handles one exception type; several catch blocks are checked from top to bottom, so the specific type comes first.
3. **`finally`.** Runs whether or not an exception occurred; used for clean-up.
4. **`throw`.** Raises an exception explicitly: `throw new IllegalArgumentException("...")`.
5. **`throws`.** In a method header, declares the checked exceptions the method may pass to its caller.

*Checked versus unchecked.* Checked exceptions (`IOException`, user-defined subclasses of `Exception`) must be caught or declared. Unchecked exceptions (subclasses of `RuntimeException`) need not be, because they usually show a bug.

```java
public class ExcDemo {
    static class InsufficientFundsException extends Exception {
        InsufficientFundsException(String m) { super(m); }
    }
    static int parse(String s) {
        try { return Integer.parseInt(s); }
        catch (NumberFormatException e) { System.out.println("bad number: " + s); return -1; }
        finally { System.out.println("finally for " + s); }
    }
    static void withdraw(double bal, double amt) throws InsufficientFundsException {
        if (amt > bal) throw new InsufficientFundsException("need Rs " + (amt - bal) + " more");
    }
    public static void main(String[] args) {
        System.out.println(parse("42"));
        System.out.println(parse("4x2"));
        try { withdraw(500, 800); } catch (InsufficientFundsException e) { System.out.println("Caught: " + e.getMessage()); }
        try { int[] a = new int[2]; a[2] = 1; }
        catch (ArrayIndexOutOfBoundsException | ArithmeticException e) { System.out.println("Unchecked: " + e.getMessage()); }
    }
}
```
```output
finally for 42
42
bad number: 4x2
finally for 4x2
-1
Caught: need Rs 300.0 more
Unchecked: Index 2 out of bounds for length 2
```

*Conclusion.* The output shows `finally` running in both cases. Use checked exceptions for failures a caller can reasonably handle and unchecked ones for programming mistakes.

**Q2 (10 marks). Explain the `String`, `StringBuilder` and `StringBuffer` classes. Why is `String` immutable? Illustrate the string pool and common methods with a program.**

*Introduction.* Text in Java is handled by three classes. `String` is immutable; `StringBuilder` and `StringBuffer` are mutable buffers for building text.

*Key points.*

1. **Immutability.** A `String` object never changes; methods like `toUpperCase()` return a new object.
2. **Reasons.** Safe sharing, safe use as hash keys, thread safety, security (file names, class names) and pooling.
3. **String pool.** Literals with equal text share one object (Figure 4.2); `new String` creates another; `intern()` returns the pooled one.
4. **Comparison.** `==` compares addresses; `equals` compares characters; `compareTo` gives alphabetical order.
5. **Common methods.** `length`, `charAt`, `substring`, `indexOf`, `replace`, `split`, `trim`, `toLowerCase`.
6. **`StringBuilder`.** Mutable, not synchronised, fast; use it to build text in loops.
7. **`StringBuffer`.** Mutable and synchronised (thread-safe) but slower.
8. **Concatenation in loops.** `s += x` creates a new object each time, so n additions cost about n² copying; a builder costs about n.

```java
public class StringDemo {
    public static void main(String[] args) {
        String a = "nepal", b = "nepal", c = new String("nepal");
        System.out.println(a == b);
        System.out.println(a == c);
        System.out.println(a.equals(c));
        System.out.println(a == c.intern());
        String s = "Tribhuvan University";
        System.out.println(s.toUpperCase() + " | original still: " + s);
        System.out.println(s.substring(0, 8) + " " + s.indexOf("Uni") + " " + s.length());
        int vowels = 0;
        for (char ch : s.toLowerCase().toCharArray()) if ("aeiou".indexOf(ch) >= 0) vowels++;
        System.out.println("vowels = " + vowels);
        StringBuilder sb = new StringBuilder();
        for (String w : s.split(" ")) sb.insert(0, w + " ");
        System.out.println(sb.toString().trim() + " | reversed: " + new StringBuilder(s).reverse());
    }
}
```
```output
true
false
true
true
TRIBHUVAN UNIVERSITY | original still: Tribhuvan University
Tribhuva 10 20
vowels = 7
University Tribhuvan | reversed: ytisrevinU navuhbirT
```

| Class | Mutable | Thread-safe | Use |
|---|---|---|---|
| `String` | no | yes (immutable) | fixed text, keys |
| `StringBuilder` | yes | no | building text, single thread |
| `StringBuffer` | yes | yes | building text shared by threads |

*Conclusion.* Strings are immutable so they can be pooled and shared safely; compare content with `equals`, and use `StringBuilder` when text is assembled in a loop.

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

## 4.3 Wrapper classes, `Math`, dates

Each primitive has a wrapper: `Integer`, `Long`, `Double`, `Boolean`, `Character` (…). They are needed for generics (`List<Integer>`), carry utilities (`Integer.parseInt("42")`, `Integer.toBinaryString(10)` = `"1010"`, `Integer.MAX_VALUE`, `Double.compare`, `Character.isDigit`) and may be `null`. **Autoboxing/unboxing** is automatic, and unboxing a `null` throws `NullPointerException`. Caution: `Integer a = 127, b = 127; a == b` is true (cache of −128…127) but with 1000 it is false; use `equals`.

`Math`: `abs`, `pow`, `sqrt`, `max`, `min`, `round`, `floor`, `ceil`, `random`, `hypot`; `Math.floorMod(-7, 3)` is 2 whereas `-7 % 3` is −1. For **money** use `java.math.BigDecimal`, not `double` (0.1 + 0.2 is 0.30000000000000004). Dates: `java.time.LocalDate.of(2026, 5, 14).plusDays(30)`, `LocalDateTime`, `Duration`, `DateTimeFormatter`; avoid the old `Date`.

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

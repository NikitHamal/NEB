---
subject: OOP in Java
grade: BCA Semester 2
unit: 2
title: Classes, Objects, Constructors and Encapsulation
area: BCA 153 · OOP in Java · Unit 2
---

A class is the unit of design in Java. This unit shows how to define classes with fields, methods and constructors; how objects live on the heap; how `static`, `final`, `this` and access modifiers work; and how to write the `toString`, `equals` and `hashCode` methods that every well-behaved class provides.

::: key What this unit gives you
- Class and object syntax; instance versus static members.
- Constructors, overloading, `this`, initialisation order.
- Access modifiers and encapsulation with getters and setters.
- Object references, parameter passing, `equals`/`hashCode`/`toString`, enums and records.
:::

## 2.1 Defining a class

A class declares **fields** (state), **methods** (behaviour) and **constructors** (initialisation). An object is created with `new`, which allocates it on the heap, runs a constructor and returns a **reference**.

```java
public class Account {
    private static int count = 0;
    private final String id;
    private double balance;

    public Account(String id, double opening) { this.id = id; this.balance = opening; count++; }
    public Account(String id) { this(id, 0.0); }

    public void deposit(double amt) {
        if (amt <= 0) throw new IllegalArgumentException("Deposit must be positive");
        balance += amt;
    }
    public boolean withdraw(double amt) {
        if (amt > balance) return false;
        balance -= amt;
        return true;
    }
    public double getBalance() { return balance; }
    public static int getCount() { return count; }
    @Override public String toString() { return id + ":" + String.format("%.2f", balance); }

    public static void main(String[] args) {
        Account a = new Account("A1", 1000);
        Account b = new Account("B1");
        a.deposit(500);
        System.out.println(a.withdraw(2000));
        System.out.println(a.withdraw(300));
        System.out.println(a + " " + b);
        System.out.println(Account.getCount());
        try { b.deposit(-5); } catch (IllegalArgumentException e) { System.out.println("Error: " + e.getMessage()); }
    }
}
```
```output
false
true
A1:1200.00 B1:0.00
2
Error: Deposit must be positive
```

Points to notice: `balance` is `private`, so the only way to change it is through methods that enforce the rules (**encapsulation**); `id` is `final`, so it is assigned once; the second constructor calls the first with `this(...)` (**constructor chaining**); `count` is `static`, shared by all objects; and `println(a + " " + b)` calls `toString()` automatically.

## 2.2 Members, `this`, `static` and `final`

| Keyword | Meaning |
|---|---|
| instance member | belongs to each object; accessed through an object |
| `static` member | belongs to the class; one copy; accessed as `ClassName.member`; a static method cannot use `this` or instance fields directly |
| `this` | reference to the current object; disambiguates `this.x = x`; passes the object on |
| `final` field | assigned once (constant if also `static`); `final` method cannot be overridden; `final` class cannot be extended (`String`) |
| default constructor | the compiler supplies a no-argument constructor *only if you write none* |

**Overloading** means several methods with the same name but different parameter lists (number, types or order), resolved at **compile time**: `print(int)`, `print(double)`, `print(String)`. The return type alone cannot distinguish overloads.

**Initialisation order** for `new C()`: static initialisers (once, when the class loads) → instance field initialisers and instance blocks (in order) → the constructor body.

```java
public class Init {
    static int s;
    int i;
    static { s = 10; System.out.println("static block"); }
    { i = 5; System.out.println("instance block"); }
    Init() { System.out.println("constructor i=" + i + " s=" + s); }
    public static void main(String[] args) { new Init(); new Init(); }
}
```
```output
static block
instance block
constructor i=5 s=10
instance block
constructor i=5 s=10
```

## 2.3 Access control and packages

| Modifier | Same class | Same package | Subclass (other package) | Anywhere |
|---|---|---|---|---|
| `private` | yes | no | no | no |
| (default / package-private) | yes | yes | no | no |
| `protected` | yes | yes | yes | no |
| `public` | yes | yes | yes | yes |

**Rule of thumb:** fields `private`, methods `public` only if part of the interface. **Packages** group classes and avoid name clashes: `package np.edu.college.bank;` as the first statement, with the folder structure `np/edu/college/bank/`; `import java.util.*;` brings other packages' classes in; `java.lang` is imported automatically. Compile with `javac -d out src/np/.../*.java` and run with `java -cp out np.edu.college.bank.Main`.

**JavaBeans convention:** private fields with `getX()` / `isX()` (boolean) / `setX(v)`; a public no-argument constructor. Setters are where validation lives.

## 2.4 References, parameter passing and memory

Variables of class type hold **references**, not objects. Assignment copies the reference, so two names can refer to the same object; `==` compares references. Java is **always pass-by-value**, but for objects the value passed *is the reference*: a method can change the object's contents but cannot make the caller's variable point somewhere else.

```java
public class Pass {
    static void change(int[] arr, int x) { arr[0] = 99; x = 99; arr = new int[]{-1}; }
    public static void main(String[] args) {
        int[] data = {1, 2, 3};
        int n = 5;
        change(data, n);
        System.out.println(data[0] + " " + n + " " + data.length);
        StringBuilder a = new StringBuilder("hi"), b = a;
        b.append("!");
        System.out.println(a + " " + (a == b));
    }
}
```
```output
99 5 3
hi! true
```

`arr[0] = 99` modified the shared array; `x = 99` changed only the local copy; `arr = new int[]{-1}` re-pointed only the local reference. An object with no remaining references becomes eligible for **garbage collection**. `null` means "refers to nothing"; using it raises `NullPointerException`. **Shallow copy** copies references; a **deep copy** copies the referenced objects too.

## 2.5 `toString`, `equals` and `hashCode`

Every class extends `java.lang.Object`, which provides `toString()`, `equals()`, `hashCode()`, `getClass()` and others. Override **`equals` and `hashCode` together**: equal objects must have equal hash codes, otherwise hash-based collections (`HashSet`, `HashMap`) misbehave.

```java
import java.util.*;
public class EqHash {
    static class P {
        final int x, y;
        P(int x, int y) { this.x = x; this.y = y; }
        @Override public boolean equals(Object o) { return o instanceof P p && p.x == x && p.y == y; }
        @Override public int hashCode() { return Objects.hash(x, y); }
        @Override public String toString() { return "(" + x + "," + y + ")"; }
    }
    public static void main(String[] args) {
        Set<P> set = new HashSet<>();
        set.add(new P(1, 2)); set.add(new P(1, 2)); set.add(new P(2, 1));
        System.out.println(set.size() + " " + new P(1, 2).equals(new P(1, 2)) + " " + (new P(1, 2) == new P(1, 2)));
    }
}
```
```output
2 true false
```

Without the overrides, the two `P(1, 2)` objects would be different references and the set would hold 3 elements.

## 2.6 Enums, records and nested classes

An **enum** is a fixed set of named constants, and can have fields, constructors and methods:

```java
public class Days {
    enum Level {
        LOW(1), HIGH(3);
        final int w;
        Level(int w) { this.w = w; }
    }
    public static void main(String[] args) {
        for (Level l : Level.values()) System.out.println(l + " " + l.w + " " + l.ordinal());
    }
}
```
```output
LOW 1 0
HIGH 3 1
```

A **record** (Java 16+) is a compact immutable data class: `record Point(int x, int y) {}` automatically gives a constructor, accessors `x()` and `y()`, `equals`, `hashCode` and `toString`. **Nested classes:** a `static` nested class (like `P` above) is independent of an outer instance; an **inner (non-static)** class holds a reference to its outer object; **anonymous classes** and **lambdas** (Unit 5) create one-off implementations. The **singleton** pattern: private constructor + static `getInstance()`; the **builder** pattern constructs complex objects stepwise.

## Formula and fact sheet

- Class = fields + methods + constructors; `new` creates an object on the heap; variables hold references.
- `static` = one per class; `this` = current object; `final` = assigned once / not overridden / not extended.
- Overloading = compile-time, same name different parameters; no return-type-only overloads.
- Init order: static blocks → instance initialisers → constructor.
- Access: private < package < protected < public.
- Java is pass-by-value (references are copied); `==` compares references; override `equals` with `hashCode`.

## Chapter summary

- A class defines the state and behaviour of its objects; constructors create valid objects.
- Encapsulation through `private` fields and validated methods keeps objects consistent.
- Static members belong to the class; instance members belong to each object.
- References explain aliasing, parameter passing and why `equals`/`hashCode` must be overridden for value-like classes.
- Enums, records and nested classes express fixed sets, data carriers and helper types.

## Practice

1. Write a `Student` class with `name`, `rollNo`, `marks[]`, a constructor, `average()`, `toString()` and a static counter of students created.
2. Differentiate overloading and overriding (preview of Unit 3). Write three overloads of `area` (circle, rectangle, triangle).
3. Predict the output of `Init` if `new Init()` is called three times.
4. Explain why `this.x = x` is needed in a constructor `Point(int x)`.
5. What is the difference between `static` and instance members? Can a static method access an instance field?
6. A method receives an `int[]` and sets `arr = null`. Does the caller's array become null? Explain.
7. Why must `equals` and `hashCode` be overridden together? Give a failing scenario.
8. Create an enum `Day` with `isWeekend()`; loop over `Day.values()`.
9. Write an immutable `Money` class (final fields, no setters, `add` returning a new object).
10. Explain the singleton pattern and write a thread-unsafe and a safe version (enum or holder).

::: note Answers and worked solutions
**1.** Fields private; constructor sets them and increments `static int total`; `average()` sums `marks` and divides by `marks.length` as a double; `toString` returns formatted name, roll and average.
**2.** Overloading: same name, different parameters, resolved at compile time within one class. Overriding: a subclass redefines an inherited method with the same signature, resolved at run time. Overloads: `area(double r)`, `area(double w, double h)`, `area(double a, double b, double c)` (Heron).
**3.** `static block` once, then three times `instance block` + `constructor i=5 s=10`.
**4.** The parameter `x` shadows the field `x`; `this.x` names the field, so `this.x = x` assigns parameter to field. Without `this`, the line assigns the parameter to itself.
**5.** Static: one copy per class, accessed through the class; instance: one per object. A static method has no `this`, so it cannot access an instance field without an object reference.
**6.** No. The reference is copied; setting the local `arr` to `null` changes only the local copy. The caller's array is intact.
**7.** Hash collections first use `hashCode` to find a bucket, then `equals`. If two equal objects have different hash codes they land in different buckets, so `set.contains(new P(1,2))` returns false even though an equal element exists.
**8.** `enum Day { MON, TUE, WED, THU, FRI, SAT, SUN; boolean isWeekend() { return this == SAT || this == SUN; } }`
**9.** `public final class Money { private final long paisa; Money(long p){paisa=p;} Money add(Money o){ return new Money(paisa + o.paisa); } long paisa(){ return paisa; } }`
**10.** A singleton has one instance. Simple (not thread-safe): `static Foo inst; static Foo get(){ if(inst==null) inst=new Foo(); return inst; }`. Safe: `enum Foo { INSTANCE; }` or a holder class `private static class H { static final Foo I = new Foo(); }`.
:::

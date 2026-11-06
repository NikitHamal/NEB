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

### A class is a plan, an object is a thing built from it

An architect's drawing is not a building; it only says what a building will have. A class is the same: it lists the fields and methods, and `new` builds an object from it in memory. Every object has its own copy of the fields plus a small header that the JVM needs. For a `Student` with an `int id`, a reference `name` and a `double marks`, a typical 64-bit HotSpot JVM with compressed references uses 12 bytes of header, 4 + 4 + 8 bytes of fields, and rounds up to a multiple of 8. Plate 2.1 adds this up and shows that three objects of the same class cost three times as much.

```photogrid label="2.1" cols="2" ratio="1.4" caption="One plan, many buildings. (a) An architectural drawing of a building front: it describes the building but is not one. (b) The size of one Student object on a typical 64-bit HotSpot JVM (12-byte header, int 4, compressed reference 4, double 8, padded to a multiple of 8) and of 1, 100 and 1,000,000 such objects, computed from those figures."
@ photo id="bca153/blueprint" cap="Architect's blueprint (1920): the plan, not the building"
fit 1.4
focus 0.5 0.5
@ svg cap="Memory of Student objects"
fields = [("header", 12), ("int id", 4), ("String name (reference)", 4), ("double marks", 8)]
raw = sum(b for _, b in fields); size = (raw + 7) // 8 * 8
assert raw == 28 and size == 32
f = Fig(400, 250)
f.text(200, 16, "One Student object = 32 bytes", size=11, color=NAVY, bold=True)
x = 10
for nm, b in fields:
    w = b * 11
    f.box(x, 32, w - 2, 36, "", fill=BLUE if nm != "header" else SAND, stroke=NAVY if nm != "header" else AMBER, r=3)
    f.text(x + w / 2 - 1, 46, f"{b} B", size=10.5, color=NAVY, bold=True)
    x += w
f.box(x, 32, 4 * 11 - 2, 36, "", fill=SOFT, stroke=SLATE, r=3); f.text(x + 21, 46, "pad 4", size=10.5, color=SLATE, bold=True)
for i, (nm, b) in enumerate(fields):
    f.text(14, 92 + i * 18, f"{nm}: {b} bytes", size=10.5, color=SLATE, anchor="start")
f.text(14, 168, "12 + 4 + 4 + 8 = 28, rounded up to 32 (multiple of 8)", size=10.5, color=NAVY, bold=True, anchor="start")
for i, n in enumerate((1, 100, 1000000)):
    y = 184 + i * 22
    f.box(14, y, 372, 18, "", fill=SAND if i < 2 else ROSE, stroke=AMBER if i < 2 else RED, r=3)
    f.text(20, y + 9, f"{n:,} object(s)", size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(380, y + 9, f"{n * size:,} bytes" + (" = 32 MB" if n == 1000000 else ""), size=10.5, color=RED if i == 2 else AMBER, bold=True, anchor="end", vmid=True)
```

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

### Same data, different objects: == against equals

Two cookies from the same cutter have the same shape but are two cookies. In Java, `==` on references asks whether both names point to the same object; `equals` asks whether the contents are equal, once you override it. If you override `equals` you must override `hashCode` so that equal objects give equal hash codes, or `HashMap` and `HashSet` will lose your objects. Plate 2.2 computes the hash code by the same rule as `Objects.hash(id, name)` and shows the four possible outcomes.

```photogrid label="2.2" cols="2" ratio="1.4" caption="Same shape, different cookie. (a) An old tin cookie cutter: every cookie it makes has the same shape but is a separate piece. (b) Two Student objects with the same id 101 and name Sita: == is false (two objects), equals is true after override, and the hash codes are equal; hash code computed by Java's own formula (31 x previous + element hash)."
@ photo id="bca153/cutter" cap="Cookie cutter: equal shapes, separate cookies"
fit 1.4
focus 0.5 0.5
@ svg cap="== against equals and the hash contract"
def jhash(s):
    h = 0
    for c in s: h = (31 * h + ord(c)) & 0xFFFFFFFF
    return h - (1 << 32) if h >= (1 << 31) else h
def objhash(*hs):
    r = 1
    for h in hs: r = (31 * r + h) & 0xFFFFFFFF
    return r - (1 << 32) if r >= (1 << 31) else r
assert jhash("NEB") == 77163 and jhash("Aa") == jhash("BB") == 2112
h1 = objhash(101, jhash("Sita")); h2 = objhash(101, jhash("Sita"))
assert h1 == h2
f = Fig(400, 250)
f.box(8, 26, 180, 62, "", fill=BLUE, stroke=NAVY, r=4); f.text(98, 44, "a  (id 101, Sita)", size=10.5, color=NAVY, bold=True); f.text(98, 66, "new Student(101, \"Sita\")", size=10.5, color=SLATE)
f.box(212, 26, 180, 62, "", fill=BLUE, stroke=NAVY, r=4); f.text(302, 44, "b  (id 101, Sita)", size=10.5, color=NAVY, bold=True); f.text(302, 66, "new Student(101, \"Sita\")", size=10.5, color=SLATE)
rows = [("a == b", "false", "two objects", RED, ROSE), ("a.equals(b)", "true", "after overriding equals", TEAL, MINT), ("a.hashCode() == b.hashCode()", "true", f"both {h1:,}", TEAL, MINT)]
for i, (q, v, why, st, fl) in enumerate(rows):
    y = 106 + i * 40
    f.box(8, y, 384, 34, "", fill=fl, stroke=st, r=4)
    f.text(14, y + 11, q, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(14, y + 25, why, size=10.5, color=SLATE, anchor="start", vmid=True)
    f.text(384, y + 17, v, size=13, color=st, bold=True, anchor="end", vmid=True)
f.text(200, 240, "\"NEB\".hashCode() = 77,163 and \"Aa\", \"BB\" both give 2,112.", size=10.5, color=SLATE)
```

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

## 2.7 Seeing references: stack and heap

Most beginner bugs in Java come from not seeing what a variable really holds. A **primitive** variable holds the value itself. A **reference** variable holds the *address* of an object on the heap. In Figure 2.1, `a` and `b` hold the same address, so they are two names for one object; `c` points to a second, separate object that merely has equal contents. That is why `a == b` is true (same address), `a == c` is false, and `a.equals(c)` is true once `equals` compares the fields. The same picture explains parameter passing: Java always passes a *copy* of the variable, so a method receives a copy of the address and can change the object but cannot make the caller's variable point elsewhere.

```svgfig label="2.1" caption="Stack and heap after: a = new Student(Sita); b = a; c = new Student(Sita). a and b share one object; c is a different object with equal contents. a == b is true, a == c is false, a.equals(c) is true when equals compares names."
f = Fig(600, 250)
f.text(100, 18, "Stack (local variables)", size=11.5, color=NAVY, bold=True)
f.text(430, 18, "Heap (objects)", size=11.5, color=NAVY, bold=True)
f.box(40, 36, 120, 36, "a   0x1A40", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(40, 86, 120, 36, "b   0x1A40", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(40, 136, 120, 36, "c   0x2B90", fill="#fde68a", color=NAVY, size=11, bold=True)
f.box(330, 44, 190, 70, "", fill="#bbf7d0", stroke=TEAL)
f.text(425, 62, "Student object @0x1A40", size=10.5, color=NAVY, bold=True)
f.text(425, 84, "name = \"Sita\"", size=11, color=NAVY)
f.text(425, 102, "marks = 78", size=11, color=NAVY)
f.box(330, 138, 190, 70, "", fill="#fde68a", stroke=AMBER)
f.text(425, 156, "Student object @0x2B90", size=10.5, color=NAVY, bold=True)
f.text(425, 178, "name = \"Sita\"", size=11, color=NAVY)
f.text(425, 196, "marks = 78", size=11, color=NAVY)
f.arrow([(160, 54), (330, 66)], color=TEAL, sw=1.8)
f.arrow([(160, 104), (330, 92)], color=TEAL, sw=1.8)
f.arrow([(160, 154), (330, 166)], color=AMBER, sw=1.8)
f.text(300, 232, "a == b true   |   a == c false   |   a.equals(c) true", size=11, color=RED, bold=True)
```

## 2.8 Eight benefits of good class design

1. **Data protection.** Private fields can be changed only through methods that check the new value. A `Student` class can refuse marks above 100, so wrong data never gets into the object. This is encapsulation at work.
2. **Reuse.** A class written once can be used in many programs and can be extended by subclasses. A `Student` class built for a library system can also serve a fee-collection program in a college. Less code is written, so fewer bugs appear.
3. **Easy maintenance.** When the inside of a class changes, code that uses its public methods does not need to change. A college can change how it stores marks without rewriting the result-printing code. Changes stay local.
4. **Clear model of the real world.** Nouns of a problem become classes and verbs become methods. Students, courses and teachers map directly to code, which makes designs easy to discuss with non-programmers.
5. **Constructors guarantee valid objects.** A constructor sets the starting state, so an object never exists half-built. A `Student` can require a roll number at creation. This removes many null and uninitialised-value errors.
6. **Shared data with `static`.** A `static` field belongs to the class, not to any object, so all objects see one value. A counter of registered students or the college name can be kept this way. It saves memory and keeps one source of truth.
7. **Correct comparison and hashing.** Overriding `equals` and `hashCode` lets objects work properly in sets and maps. Two `Student` objects with the same roll number can then be recognised as the same person, which prevents duplicate entries in a register.
8. **Readable output.** Overriding `toString` gives each object a clear text form for logs and screens. Debugging a program that prints `Student[roll=7, name=Sita]` is far easier than reading `Student@1b6d3586`.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Java is "pass by value". Explain with a program how objects and primitives behave when passed to a method.**

*Introduction.* When a method is called, Java copies the value of each argument into the parameter. For a primitive the copy is the number itself; for an object the copy is the *reference* (address), so both names point to the same object (Figure 2.1).

*Behaviour.*

1. **Primitives.** The method changes only its own copy; the caller's variable is unchanged.
2. **Object contents.** Through the copied reference the method can modify the object's fields, and the caller sees the change.
3. **Re-pointing.** Assigning a new object to the parameter changes only the copy; the caller's reference is unaffected, so a classic `swap(a, b)` method cannot work.

```java
public class PassDemo {
    static class Box { int v; Box(int v) { this.v = v; } }
    static void bump(int x) { x = x + 10; }
    static void bump(Box b) { b.v = b.v + 10; }
    static void replace(Box b) { b = new Box(999); }
    public static void main(String[] args) {
        int n = 5; Box box = new Box(5);
        bump(n);   System.out.println("after bump(int):  n = " + n);
        bump(box); System.out.println("after bump(Box):  v = " + box.v);
        replace(box); System.out.println("after replace():  v = " + box.v);
    }
}
```
```output
after bump(int):  n = 5
after bump(Box):  v = 15
after replace():  v = 15
```

*Reading the output.* `n` stays 5 (copy), `v` becomes 15 (shared object changed), and `replace` leaves 15 because only the parameter was re-pointed.

*Conclusion.* Java never passes objects themselves, only copies of references. Methods can mutate an object but cannot change which object the caller's variable names.

**Q2 (10 marks). Design a Java class `Student` with private fields, constructors, a static counter, and overridden `toString`, `equals` and `hashCode`. Explain each element and show how it behaves in a `HashSet`.**

*Introduction.* A class defines the fields and methods of its objects. Good design hides the fields and exposes a small, safe interface. Overriding the methods of `Object` makes the class behave correctly in collections.

*Design elements.*

1. **Private fields.** `roll` and `name` cannot be read or written from outside except through methods.
2. **Constructor.** `Student(int roll, String name)` creates a valid object and rejects a roll below 1.
3. **`static int count`.** One counter shared by the class, increased in the constructor.
4. **`toString`.** Gives the readable form `Student[roll=7, name=Sita]`.
5. **`equals`.** Two students are equal when their roll numbers are equal.
6. **`hashCode`.** Must agree with `equals`: equal objects must give the same hash code, here `Integer.hashCode(roll)`.
7. **`this`.** Separates the field from the parameter of the same name.
8. **`HashSet`.** Uses `hashCode` to find a bucket and `equals` to compare, so the duplicate is dropped.

```java
import java.util.HashSet;
import java.util.Set;

public class StudentDemo {
    static class Student {
        private final int roll;
        private final String name;
        static int count = 0;
        Student(int roll, String name) {
            if (roll < 1) throw new IllegalArgumentException("roll must be >= 1");
            this.roll = roll; this.name = name; count++;
        }
        @Override public String toString() { return "Student[roll=" + roll + ", name=" + name + "]"; }
        @Override public boolean equals(Object o) {
            return o instanceof Student s && s.roll == roll;
        }
        @Override public int hashCode() { return Integer.hashCode(roll); }
    }
    public static void main(String[] args) {
        Student a = new Student(7, "Sita"), b = new Student(7, "Sita R."), c = new Student(8, "Ram");
        System.out.println(a);
        System.out.println("a == b: " + (a == b) + ", a.equals(b): " + a.equals(b));
        Set<Student> set = new HashSet<>(Set.of(a, c));
        System.out.println("set.add(b) -> " + set.add(b) + ", size = " + set.size());
        System.out.println("objects created: " + Student.count);
    }
}
```
```output
Student[roll=7, name=Sita]
a == b: false, a.equals(b): true
set.add(b) -> false, size = 2
objects created: 3
```

*Comparison.*

| Operation | Compares | Result here |
|---|---|---|
| `a == b` | addresses | false |
| `a.equals(b)` | roll numbers (our rule) | true |
| `set.add(b)` | `hashCode` then `equals` | false (duplicate) |

*Conclusion.* Private fields and a validating constructor protect the object, `static` shares class-wide data, and consistent `equals`/`hashCode` make the class safe in `HashSet` and `HashMap`.

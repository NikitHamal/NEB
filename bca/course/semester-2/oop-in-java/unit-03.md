---
subject: OOP in Java
grade: BCA Semester 2
unit: 3
title: Inheritance, Polymorphism, Abstract Classes and Interfaces
area: BCA 153 · OOP in Java · Unit 3
---

Inheritance and polymorphism are the features that let one piece of code work with many kinds of objects. This unit covers extending classes, overriding, dynamic method dispatch, abstract classes, interfaces (including default methods and lambdas), and the design guidance that says when to use which.

::: key What this unit gives you
- `extends`, `super`, constructor chaining, overriding rules, `@Override`.
- Dynamic dispatch: how Java chooses the method at run time (and what it does *not* do).
- Abstract classes versus interfaces; default, static and functional interfaces.
- The `Object` class, casting and `instanceof`; composition over inheritance.
:::

## 3.1 Inheritance

A **subclass** `extends` one **superclass** and inherits its non-private members; Java has **single inheritance** of classes (but many interfaces). A subclass is-a superclass, so a `Square` can be used wherever a `Rect` is expected. Constructors are not inherited: the first statement of a subclass constructor is `super(...)` (implicit `super()` if omitted), so the **superclass part is built first**.

**Overriding** redefines an inherited instance method with the *same signature* (same name and parameters; return type same or a subtype; access not narrower; no broader checked exceptions). Mark it with `@Override` so the compiler catches typos. **`super.method()`** calls the superclass version. `private`, `static` and `final` methods cannot be overridden (static methods are *hidden*).

## 3.2 Polymorphism and dynamic dispatch

A superclass reference may hold a subclass object. When an **overridden instance method** is called through that reference, the JVM picks the version from the **actual object's class at run time** (dynamic dispatch, run-time polymorphism).

```java
abstract class Shape {
    abstract double area();
    public String toString() { return getClass().getSimpleName() + String.format("[%.2f]", area()); }
}
class Circle extends Shape {
    double r;
    Circle(double r) { this.r = r; }
    double area() { return Math.PI * r * r; }
}
class Rect extends Shape {
    double w, h;
    Rect(double w, double h) { this.w = w; this.h = h; }
    double area() { return w * h; }
}
class Square extends Rect {
    Square(double s) { super(s, s); }
}
interface Drawable {
    void draw();
    default String info() { return "drawable"; }
}
public class Shapes {
    public static void main(String[] a) {
        Shape[] list = { new Circle(1), new Rect(2, 3), new Square(4) };
        double total = 0;
        for (Shape s : list) { System.out.println(s); total += s.area(); }
        System.out.printf("total=%.3f%n", total);
        System.out.println(list[2] instanceof Rect);
        Drawable d = () -> System.out.println("drawing");
        d.draw();
        System.out.println(d.info());
    }
}
```
```output
Circle[3.14]
Rect[6.00]
Square[16.00]
total=25.142
true
drawing
drawable
```

The loop calls `s.area()` once in the source, yet three different methods run. New shapes can be added (a `Triangle`) **without changing this loop**: that is the open–closed principle in action.

**What is *not* polymorphic:** fields and static methods are resolved by the **declared (reference) type**, not the object's class.

```java
class Animal {
    String name = "Animal";
    String sound() { return "..."; }
    static String kind() { return "animal"; }
}
class Dog extends Animal {
    String name = "Dog";
    @Override String sound() { return "Woof"; }
    static String kind() { return "dog"; }
}
public class Dispatch {
    public static void main(String[] x) {
        Animal a = new Dog();
        System.out.println(a.sound() + " " + a.name + " " + a.kind());
        System.out.println(((Dog) a).name + " " + Dog.kind());
    }
}
```
```output
Woof Animal animal
Dog dog
```

**Compile-time versus run-time:** *overloading* is decided at compile time from the argument types; *overriding* is decided at run time from the object. **Casting:** upcasting (`Animal a = dog`) is automatic and safe; downcasting `(Dog) a` needs a cast and throws `ClassCastException` if the object is not a `Dog`; check first with `if (a instanceof Dog d) { … }` (pattern matching, Java 16+).

### One tool, many blades

A Swiss Army knife is one object with many tools behind one handle. Polymorphism is similar on the software side: one call, `shape.area()`, runs a different method depending on the object that receives it. The reference type decides what you may call; the object type decides which version runs. Plate 3.1 computes the area of a circle, a rectangle and a triangle through the same call and adds them in one loop.

```photogrid label="3.1" cols="2" ratio="1.4" caption="One call, many behaviours. (a) A Swiss Army knife open: one handle, many tools. (b) Three objects held in one Shape[] and the result of calling area() on each: circle of radius 2, rectangle 3 x 4 and right triangle with legs 3 and 4; the loop adds them to 12.57 + 12 + 6 = 30.57."
@ photo id="bca153/knife" cap="Swiss Army knife: one object, many tools"
fit 1.4
focus 0.5 0.5
@ svg cap="shape.area() on three kinds of Shape"
import math
areas = [("Circle(2)", math.pi * 2 * 2), ("Rectangle(3, 4)", 3 * 4), ("Triangle(3, 4)", 0.5 * 3 * 4)]
tot = sum(a for _, a in areas)
assert round(areas[0][1], 2) == 12.57 and areas[1][1] == 12 and areas[2][1] == 6 and round(tot, 2) == 30.57
f = Fig(400, 250)
f.text(200, 16, "for (Shape s : shapes) total += s.area();", size=11, color=NAVY, bold=True)
for i, ((nm, a), (fl, st)) in enumerate(zip(areas, [(BLUE, NAVY), (SAND, AMBER), (MINT, TEAL)])):
    y = 32 + i * 50
    f.box(8, y, 150, 40, nm, fill=fl, stroke=st, color=st, size=11, bold=True)
    f.arrow([(158, y + 20), (200, y + 20)], color=SLATE, sw=1.5)
    f.text(206, y + 14, "own area() runs", size=10.5, color=SLATE, anchor="start", vmid=True)
    f.box(206, y + 22, max(a / 12.57 * 150, 10), 14, "", fill=fl, stroke=st, r=2)
    f.text(212 + max(a / 12.57 * 150, 10), y + 29, f"{a:.2f}", size=10.5, color=st, bold=True, anchor="start", vmid=True)
f.box(8, 190, 384, 44, "", fill=ROSE, stroke=RED, r=4)
f.text(200, 206, "total = 12.57 + 12.00 + 6.00 = 30.57", size=12, color=RED, bold=True)
f.text(200, 224, "The loop never asks which kind of shape it is holding.", size=10.5, color=SLATE)
```

## 3.3 Abstract classes

An **abstract class** cannot be instantiated; it may have fields, constructors, concrete methods and `abstract` methods (no body) that subclasses must implement. Use it for a family sharing code and state: `Shape` above. A class with any abstract method must itself be abstract; the first concrete subclass must implement them all.

## 3.4 Interfaces

An **interface** is a contract: a set of method signatures (implicitly `public abstract`) and constants (`public static final`). A class `implements` any number of interfaces, so interfaces give **multiple inheritance of type**. Since Java 8 an interface may also contain:

- **`default` methods** (with a body, inherited unless overridden),
- **`static` methods**, and (Java 9) **`private` methods**.

If a class inherits two defaults with the same signature it must override and choose (`A.super.m()`). An interface with exactly one abstract method is a **functional interface** and can be implemented by a **lambda** (`Runnable`, `Comparator<T>`, `Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`).

| | Abstract class | Interface |
|---|---|---|
| Instances | no | no |
| Fields | any | constants only |
| Constructors | yes | no |
| Methods | abstract + concrete | abstract + default/static |
| Inheritance | one class | many interfaces |
| Use when | related classes share state and code | unrelated classes share a capability (`Comparable`, `Serializable`, `Runnable`) |

```java
import java.util.*;
public class Sorting {
    static class Student implements Comparable<Student> {
        String name; int marks;
        Student(String n, int m) { name = n; marks = m; }
        public int compareTo(Student o) { return Integer.compare(o.marks, marks); }
        public String toString() { return name + "=" + marks; }
    }
    public static void main(String[] args) {
        List<Student> l = new ArrayList<>(List.of(new Student("Sita", 82), new Student("Ram", 67), new Student("Gita", 91)));
        Collections.sort(l);
        System.out.println(l);
        l.sort(Comparator.comparing(s -> s.name));
        System.out.println(l);
    }
}
```
```output
[Gita=91, Sita=82, Ram=67]
[Gita=91, Ram=67, Sita=82]
```

`Comparable<T>` defines the **natural order** (`compareTo`: negative, zero, positive); `Comparator<T>` supplies an alternative order from outside.

### One interface, many implementations

An interface is a promise: any class that implements it can be used wherever the interface is expected. The TV-B-Gone is a small device that sends the switch-off codes of many makes of television in turn, so one button works with all of them; in code, one `Comparator` variable can hold many different ways of ordering the same list. Plate 3.2 sorts four students by name and by marks using two `Comparator` implementations and gets two different, correct orders from the same `sort` call.

```photogrid label="3.2" cols="2" ratio="1.4" caption="One button, many codes. (a) A TV-B-Gone circuit with several infrared LEDs: one device sends many different codes. (b) The same list of four students sorted twice through one sort call: by name (alphabetical) and by marks (highest first), using two different Comparator objects."
@ photo id="bca153/tvbgone" cap="TV-B-Gone: one device, many behaviours"
fit 1.4
focus 0.5 0.5
@ svg cap="list.sort(comparator) with two comparators"
st = [("Sita", 78), ("Ram", 91), ("Hari", 66), ("Gita", 85)]
by_name = sorted(st, key=lambda t: t[0]); by_marks = sorted(st, key=lambda t: -t[1])
assert [n for n, _ in by_name] == ["Gita", "Hari", "Ram", "Sita"] and [n for n, _ in by_marks] == ["Ram", "Gita", "Sita", "Hari"]
f = Fig(400, 250)
f.text(200, 16, "Same list, two Comparator objects", size=11, color=NAVY, bold=True)
f.text(8, 40, "original:", size=10.5, color=SLATE, bold=True, anchor="start")
for i, (n, m) in enumerate(st): f.box(76 + i * 80, 28, 74, 26, f"{n} {m}", fill=BLUE, stroke=NAVY, color=NAVY, size=10.5, bold=True)
for j, (ttl, lst, fl, sc) in enumerate([("(a, b) -> a.name.compareTo(b.name)", by_name, MINT, TEAL), ("(a, b) -> b.marks - a.marks", by_marks, SAND, AMBER)]):
    y = 76 + j * 80
    f.text(8, y, ttl, size=10.5, color=sc, bold=True, anchor="start")
    for i, (n, m) in enumerate(lst): f.box(8 + i * 96, y + 10, 90, 34, f"{n} {m}", fill=fl, stroke=sc, color=sc, size=11, bold=True)
f.text(200, 238, "Sorting code is written once; the ordering rule is plugged in.", size=10.5, color=SLATE, bold=True)
```

## 3.5 The `Object` class and design guidance

`Object` gives every class `toString`, `equals`, `hashCode`, `getClass`, `clone`, `finalize` (deprecated) and the thread methods `wait`/`notify`. **`final`** stops inheritance where it would break invariants; **sealed classes** (Java 17) restrict which classes may extend a type.

**Inheritance vs composition.** Inheritance is *is-a* (a `Dog` is an `Animal`); **composition** is *has-a* (a `Car` has an `Engine`). Prefer composition and interfaces when you only need to reuse behaviour: inheritance couples the subclass tightly to the superclass's internals (the *fragile base class* problem). Liskov's rule: a subclass must be usable wherever the superclass is without surprising the caller; a `Square` extending a *mutable* `Rect` breaks that, because setting the width of a square must also change its height.

**Design principles (SOLID, in one line each):** one reason to change per class; extend without modifying; subtypes substitutable; small focused interfaces; depend on abstractions, not concretions.

## 3.6 One call, many behaviours

Figure 3.1 shows a small payroll design that uses every idea of this unit. `Payable` is an **interface**: it promises a `pay()` method and says nothing about how. `Employee` is an **abstract class** that partly implements it and holds the shared field `name`. `Teacher` and `Clerk` are concrete subclasses with different pay rules, and `Vendor` is an unrelated class that also implements `Payable`. A single loop over `List<Payable>` can print a pay slip for all of them, and at run time the JVM picks the right `pay()` for each object (dynamic dispatch). The loop does not change when a new kind of payee is added, which is the practical value of polymorphism.

```svgfig label="3.1" caption="Payroll design. Solid arrows with a hollow tip mean extends; dashed arrows mean implements. The call p.pay() on a Payable variable runs Teacher.pay(), Clerk.pay() or Vendor.pay() depending on the real object."
f = Fig(600, 270)
f.box(190, 12, 220, 52, "interface Payable\n+ pay() : double", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(30, 118, 220, 52, "abstract class Employee\n# name : String", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(380, 118, 190, 52, "class Vendor\n+ pay() = invoice", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(10, 208, 140, 48, "Teacher\npay() = hours x rate", fill="#ffffff", stroke=NAVY, color=NAVY, size=10, bold=True)
f.box(170, 208, 140, 48, "Clerk\npay() = fixed salary", fill="#ffffff", stroke=NAVY, color=NAVY, size=10, bold=True)
f.arrow([(140, 118), (140, 90), (260, 90), (260, 64)], color=AMBER, sw=1.8, dash=True)
f.arrow([(475, 118), (475, 90), (340, 90), (340, 64)], color=AMBER, sw=1.8, dash=True)
f.arrow([(80, 208), (80, 188), (110, 188), (110, 170)], color=NAVY, sw=1.8)
f.arrow([(240, 208), (240, 188), (170, 188), (170, 170)], color=NAVY, sw=1.8)
f.text(330, 105, "implements", size=10, color=AMBER, bold=True, anchor="start")
f.text(470, 236, "for (Payable p : list)", size=11, color=RED, bold=True)
f.text(470, 252, "    p.pay();   // late binding", size=11, color=RED)
```

## 3.7 Eight uses of inheritance, polymorphism and interfaces

1. **Code reuse.** A subclass inherits fields and methods of its parent and adds only what is new. A `Teacher` and a `Clerk` share `name` and `toString` from `Employee`. Fixing a bug in the parent fixes it for every child.
2. **Extending without editing.** New behaviour is added by writing a new subclass, so tested code stays untouched. Adding a `Contractor` to the payroll needs no change in the loop that prints pay slips.
3. **Common handling of different objects.** A parent-type or interface variable can hold any child. One method can accept a `Payable` and work for staff, vendors and scholarship payments alike.
4. **Contracts between teams.** An interface fixes the method names and types before anyone writes the code. One team can write the user interface while another writes the payment code, and they meet at the interface.
5. **Multiple capabilities.** A class can extend only one class but implement many interfaces. A `Student` can be `Comparable` for sorting and `Serializable` for saving at the same time.
6. **Flexible testing.** Code that depends on an interface can be tested with a simple fake object. A fee-collection program can be tested with a fake payment gateway instead of a real bank connection.
7. **Framework design.** Libraries define interfaces such as `Runnable`, `Comparator` and `List`, and your classes plug in. The Android and Java collections frameworks both work this way.
8. **Controlled templates.** An abstract class gives the fixed steps and leaves some steps for subclasses. A report generator can fix the layout and let each subclass supply its own data.

## Formula and fact sheet

- Single inheritance of classes, multiple of interfaces; `super(...)` first in a constructor.
- Override: same signature, `@Override`, run-time dispatch. Overload: compile time.
- Fields and static methods resolve by reference type.
- Abstract class: shared state and code; interface: capability contract; default methods allowed.
- Downcast needs `instanceof` check. Prefer composition for reuse.

## Chapter summary

- Inheritance reuses and specialises; constructors chain upward.
- Overridden methods are chosen at run time by the object's class, which is what lets one loop handle many shapes.
- Abstract classes share implementation among related types; interfaces define capabilities and enable lambdas.
- Good designs favour small interfaces and composition, keeping subclasses substitutable for their parents.

## Practice

1. Differentiate abstract class and interface. When would you choose each?
2. Predict the output for a class `A` with `void show(){print("A");}`, `B extends A` overriding it with "B", and `A x = new B(); x.show();`.
3. Create `Employee` (abstract, `salary()` abstract) with `FullTime` and `PartTime` subclasses and print the total payroll of an array of mixed employees.
4. Why does `A a = new B(); a.fieldX` read A's field even if B declares one with the same name?
5. What is wrong with calling an overridable method from a constructor?
6. Write a functional interface `Operation { int apply(int a, int b); }` and use lambdas for add and multiply.
7. Sort a list of strings by length, then alphabetically, using `Comparator`.
8. What happens when a class implements two interfaces with the same default method?
9. Explain `instanceof` with pattern matching and give an example of a `ClassCastException`.
10. Explain with an example why `Square extends Rectangle` can violate Liskov substitution.

::: note Answers and worked solutions
**1.** Abstract class: single inheritance, may hold state and constructors; use it for closely related classes sharing code. Interface: capability across unrelated classes, multiple implementation; use for contracts and callbacks.
**2.** Prints **B** (dynamic dispatch uses the object's class).
**3.** `abstract class Employee { abstract double salary(); }`; `FullTime` returns monthly pay; `PartTime` returns hours × rate; a loop adds `e.salary()` for each element of `Employee[]`.
**4.** Fields are not overridden, only hidden; field access is resolved at compile time from the reference type `A`.
**5.** The superclass constructor runs before the subclass's fields are initialised, so the overridden method may see default values (0 or null) and fail.
**6.** `Operation add = (a, b) -> a + b; Operation mul = (a, b) -> a * b; add.apply(2, 3)` is 5 and `mul.apply(2, 3)` is 6.
**7.** `list.sort(Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder()));`
**8.** Compile error unless the class overrides the method; inside, it can pick one with `A.super.m()`.
**9.** `if (obj instanceof String s) { s.length(); }` tests and binds. `Object o = "text"; Integer i = (Integer) o;` throws `ClassCastException`.
**10.** A `Rectangle` promises that setting width does not change height. A `Square` must change both, so code written for rectangles (`r.setWidth(5); r.setHeight(2); assert area == 10`) fails for a square.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Differentiate an abstract class and an interface, and show both in one Java program.**

*Introduction.* Both define a type that cannot be instantiated directly and that subclasses must complete, but they serve different purposes: an abstract class shares state and partial code; an interface defines a pure capability.

*Differences.*

1. **State.** An abstract class may have instance fields; an interface has only constants.
2. **Code.** An abstract class may have constructors and ordinary methods; an interface has abstract methods plus `default` and `static` methods.
3. **Inheritance.** A class extends only one abstract class but may implement many interfaces.
4. **Relation.** An abstract class expresses *is-a* with shared code; an interface expresses *can-do*.

| Point | Abstract class | Interface |
|---|---|---|
| Keyword | `abstract class` / `extends` | `interface` / `implements` |
| Fields | any | `public static final` only |
| Constructor | yes | no |
| Multiple | no | yes |

```java
import java.util.List;

public class PayDemo {
    interface Payable {
        double pay();
        default String slip() { return String.format("Pay slip: Rs %.2f", pay()); }
    }
    static abstract class Employee implements Payable {
        protected final String name;
        Employee(String n) { name = n; }
        @Override public String toString() { return name; }
    }
    static class Teacher extends Employee {
        private final double hours, rate;
        Teacher(String n, double h, double r) { super(n); hours = h; rate = r; }
        public double pay() { return hours * rate; }
    }
    static class Clerk extends Employee {
        Clerk(String n) { super(n); }
        public double pay() { return 32000; }
    }
    static class Vendor implements Payable {
        public double pay() { return 12500.5; }
        @Override public String toString() { return "Vendor"; }
    }
    public static void main(String[] args) {
        List<Payable> list = List.of(new Teacher("Sita", 90, 450), new Clerk("Ram"), new Vendor());
        for (Payable p : list) System.out.println(p + " -> " + p.slip());
    }
}
```
```output
Sita -> Pay slip: Rs 40500.00
Ram -> Pay slip: Rs 32000.00
Vendor -> Pay slip: Rs 12500.50
```

*Conclusion.* Use an abstract class when subclasses share fields and code (`Employee`); use an interface for a capability that unrelated classes can offer (`Payable`, implemented even by `Vendor`).

**Q2 (10 marks). Explain method overloading and overriding, dynamic dispatch and the `instanceof` check with a program. Differentiate overloading and overriding.**

*Introduction.* Polymorphism means "many forms": one name, different behaviour. Java has compile-time polymorphism (overloading) and run-time polymorphism (overriding).

*Concepts.*

1. **Overloading.** Several methods in the same class share a name but differ in parameter lists. The compiler chooses by the argument types.
2. **Overriding.** A subclass supplies its own version of an inherited method with the same signature, marked `@Override`.
3. **Dynamic dispatch.** For an overridden method the JVM picks the version from the *actual object* at run time, not from the declared type (Figure 3.1).
4. **Static methods.** They are hidden, not overridden, so the declared type decides.
5. **`instanceof`.** Tests the real type before a downcast; a pattern such as `a instanceof Dog d` tests and casts in one step.
6. **`super`.** Lets an override call the parent's version.
7. **`final`.** A `final` method cannot be overridden; a `final` class cannot be extended.
8. **Access.** An override may not reduce visibility.

```java
public class DispatchDemo {
    static class Animal {
        String sound() { return "..."; }
        static String kind() { return "animal"; }
    }
    static class Dog extends Animal {
        @Override String sound() { return "Woof"; }
        static String kind() { return "dog"; }
        String fetch() { return "fetching"; }
    }
    static int area(int side) { return side * side; }
    static double area(double w, double h) { return w * h; }
    public static void main(String[] args) {
        Animal a = new Dog();
        System.out.println("a.sound() = " + a.sound());
        System.out.println("Animal.kind() = " + Animal.kind() + ", Dog.kind() = " + Dog.kind());
        if (a instanceof Dog d) System.out.println("downcast ok: " + d.fetch());
        System.out.println("area(3) = " + area(3) + ", area(2.5, 4) = " + area(2.5, 4));
        Animal plain = new Animal();
        System.out.println("plain instanceof Dog: " + (plain instanceof Dog));
    }
}
```
```output
a.sound() = Woof
Animal.kind() = animal, Dog.kind() = dog
downcast ok: fetching
area(3) = 9, area(2.5, 4) = 10.0
plain instanceof Dog: false
```

| Feature | Overloading | Overriding |
|---|---|---|
| Where | same class | parent and child |
| Signature | different parameters | identical |
| Binding | compile time | run time |
| Purpose | convenience | specialised behaviour |

*Conclusion.* The variable's declared type decides what can be called, while the object's real type decides which overridden version runs. That separation makes extensible designs possible.

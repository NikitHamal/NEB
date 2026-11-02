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

## 3.5 The `Object` class and design guidance

`Object` gives every class `toString`, `equals`, `hashCode`, `getClass`, `clone`, `finalize` (deprecated) and the thread methods `wait`/`notify`. **`final`** stops inheritance where it would break invariants; **sealed classes** (Java 17) restrict which classes may extend a type.

**Inheritance vs composition.** Inheritance is *is-a* (a `Dog` is an `Animal`); **composition** is *has-a* (a `Car` has an `Engine`). Prefer composition and interfaces when you only need to reuse behaviour: inheritance couples the subclass tightly to the superclass's internals (the *fragile base class* problem). Liskov's rule: a subclass must be usable wherever the superclass is without surprising the caller; a `Square` extending a *mutable* `Rect` breaks that, because setting the width of a square must also change its height.

**Design principles (SOLID, in one line each):** one reason to change per class; extend without modifying; subtypes substitutable; small focused interfaces; depend on abstractions, not concretions.

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

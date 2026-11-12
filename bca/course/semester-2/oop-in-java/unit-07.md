---
subject: OOP in Java
grade: BCA Semester 2
unit: 7
title: Design Patterns and Advanced OOP Concepts
area: BCA 153 · OOP in Java · Unit 7
---

The revised TU syllabus ends with a unit on **advanced OOP concepts in Java**: design patterns (singleton, factory, observer), lambda expressions, the Stream API, `Optional` and method references. Lambdas, streams and `Optional` were introduced in Unit 5; this unit completes the list with the three patterns, and it also closes four smaller gaps that the syllabus names in its class and array topics: **copy constructors**, **nested and inner classes**, **jagged arrays** and **variable-length arguments**.

::: key What this unit gives you
- What a design pattern is, and why the same three solutions keep appearing in real code.
- **Singleton**, **Factory** and **Observer**, each with a program that was compiled and run.
- Copy constructors and the shallow-versus-deep copy trap.
- The four kinds of nested class, including anonymous classes and why lambdas replaced most of them.
- Jagged arrays and `varargs`.
:::

## 7.1 What a design pattern is

A **design pattern** is a named, reusable solution to a design problem that keeps coming back. It is not a library and not a piece of code you copy; it is a *shape* of classes and calls that experienced programmers recognise. The famous catalogue of 23 patterns (Gamma, Helm, Johnson and Vlissides, 1994, the "Gang of Four") groups them in three families.

| Family | Question it answers | Examples |
|---|---|---|
| Creational | How is an object made, and who decides which class to instantiate? | Singleton, Factory, Builder |
| Structural | How are classes and objects combined into larger structures? | Adapter, Decorator, Facade |
| Behavioural | How do objects share work and talk to each other? | Observer, Strategy, Iterator |

The syllabus asks for one pattern from each of the first and third families and the most common creational helper: **singleton** (creational), **factory** (creational) and **observer** (behavioural). Every pattern below uses only ideas from earlier units: private constructors and `static` (Unit 2), interfaces and polymorphism (Unit 3) and collections (Unit 5).

::: tip Exam tip
Answer every pattern question in four parts: *intent* (one sentence), *structure* (a small class diagram or the list of classes), *code* (10 to 20 lines), *use* (one real example). Examiners award marks for each part.
:::

## 7.2 Singleton: exactly one instance

**Intent.** Guarantee that a class has only one instance and give a global access point to it. Typical uses: a configuration object, a logger, a connection pool, an application-wide cache.

**How it is built.**

1. Make the constructor `private`, so no other class can write `new`.
2. Keep the single instance in a `private static` field.
3. Provide a `public static` method (conventionally `getInstance()`) that returns it.

```java
public class SingletonDemo {
    static class AppConfig {
        private static AppConfig instance;          // the one and only object
        private final String college = "NEBians College";
        private int created = 0;

        private AppConfig() { created++; System.out.println("AppConfig created"); }

        static synchronized AppConfig getInstance() {   // lazy and thread-safe
            if (instance == null) instance = new AppConfig();
            return instance;
        }
        String college() { return college; }
    }

    public static void main(String[] args) {
        AppConfig a = AppConfig.getInstance();
        AppConfig b = AppConfig.getInstance();
        System.out.println(a.college());
        System.out.println("same object? " + (a == b));
    }
}
```

The constructor message prints only once, and `a == b` is `true`, because the second call finds `instance` already set.

**Why `synchronized`?** Without it, two threads could both see `instance == null` and each create an object (a race condition, Unit 6). `synchronized` makes the check-and-create step atomic, at a small cost on every call. Three common variants:

| Variant | How | Note |
|---|---|---|
| Lazy, synchronized method | as above | simple; every call takes a lock |
| Eager | `private static final AppConfig INSTANCE = new AppConfig();` | created at class-load time, thread-safe, but built even if never used |
| Enum singleton | `enum AppConfig { INSTANCE; }` | the JVM guarantees one instance and it survives serialization and reflection attacks |

::: caution Cautions
A singleton is global state in disguise. It makes classes harder to test (you cannot easily replace it with a fake) and hides dependencies. Use it for things that are genuinely one per program, not as a way to avoid passing an argument.
:::

## 7.3 Factory: let a method choose the class

**Intent.** Move the decision "which concrete class do I create?" out of the calling code into one place. The caller asks for a *kind* of object and receives something that implements a common interface.

Without a factory, code such as `if (type.equals("sms")) n = new SmsNotifier(); else if (type.equals("email")) n = new EmailNotifier();` is repeated wherever notifications are made, and every new channel means editing every copy. With a factory the `if` lives once.

```java
public class FactoryDemo {
    interface Notifier { void send(String to, String msg); }

    static class SmsNotifier implements Notifier {
        public void send(String to, String msg) { System.out.println("SMS to " + to + ": " + msg); }
    }
    static class EmailNotifier implements Notifier {
        public void send(String to, String msg) { System.out.println("Email to " + to + ": " + msg); }
    }

    static class NotifierFactory {
        static Notifier create(String type) {
            switch (type.toLowerCase()) {
                case "sms":   return new SmsNotifier();
                case "email": return new EmailNotifier();
                default: throw new IllegalArgumentException("Unknown channel: " + type);
            }
        }
    }

    public static void main(String[] args) {
        String[] channels = {"sms", "email"};
        for (String c : channels) {
            Notifier n = NotifierFactory.create(c);   // caller never says new SmsNotifier()
            n.send("9800000000", "Exam routine published");
        }
        try { NotifierFactory.create("fax"); }
        catch (IllegalArgumentException e) { System.out.println(e.getMessage()); }
    }
}
```

The caller depends only on the `Notifier` interface (polymorphism, Unit 3). Adding `PushNotifier` means one new class and one new `case`; nothing that *uses* notifiers changes. This is the **open/closed principle**: open for extension, closed for modification.

::: note Simple factory, factory method, abstract factory
What is shown above is the *simple factory* (one static method with a `switch`). The **factory method** pattern moves creation into an overridable method of a base class, so each subclass chooses its own product. The **abstract factory** creates whole families of related objects (for example a Windows button and a Windows scrollbar). For the TU paper the simple factory with the interface is what is expected.
:::

## 7.4 Observer: tell everyone who is interested

**Intent.** Define a one-to-many dependency, so that when one object (the **subject**) changes state, all its dependents (the **observers**) are notified and updated automatically.

You know it already: a YouTube channel (subject) and its subscribers (observers); a button and its click listeners in Swing (Unit 6); a stock ticker and the screens that display it. The subject keeps a *list* of observers and calls the same method on each; it does not know or care what each observer does with the news.

```java
import java.util.ArrayList;
import java.util.List;

public class ObserverDemo {
    interface Observer { void update(String course, String notice); }

    static class NoticeBoard {                       // the subject
        private final List<Observer> observers = new ArrayList<>();
        void subscribe(Observer o)   { observers.add(o); }
        void unsubscribe(Observer o) { observers.remove(o); }
        void publish(String course, String notice) {
            for (Observer o : observers) o.update(course, notice);
        }
    }

    static class Student implements Observer {
        private final String name;
        Student(String name) { this.name = name; }
        public void update(String course, String notice) {
            System.out.println(name + " got [" + course + "] " + notice);
        }
    }

    public static void main(String[] args) {
        NoticeBoard board = new NoticeBoard();
        Student sita = new Student("Sita"), ram = new Student("Ram");
        board.subscribe(sita);
        board.subscribe(ram);
        board.subscribe((c, n) -> System.out.println("Office log: " + c + " / " + n));  // a lambda is an Observer

        board.publish("Java", "Lab moved to Room 4");
        board.unsubscribe(ram);
        board.publish("Java", "Assignment due Friday");
    }
}
```

Three points deserve attention. First, `Observer` has a single abstract method, so a **lambda** can stand in for it, which is why lambdas are listed with patterns in the syllabus: they make small observers one line long. Second, `NoticeBoard` never mentions `Student`: new kinds of observers can be added without touching the subject (loose coupling). Third, the order of notification is the order of subscription, and a slow observer delays all that follow; real systems may notify on separate threads.

Java once shipped `java.util.Observable` and `Observer`, but both have been deprecated since Java 9 because they are not type-safe and not thread-safe. Modern code writes its own small interface, as above, or uses `PropertyChangeListener` or reactive streams.

```svgfig label="7.1" caption="The three patterns at a glance. Singleton: every caller gets the same object. Factory: the caller asks a factory for a product that implements an interface. Observer: one subject notifies many subscribed observers."
f = Fig(600, 250)
f.text(100, 18, "Singleton", size=12, color=NAVY, bold=True)
f.box(40, 34, 120, 40, "getInstance()", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(40, 150, 120, 44, "AppConfig\nthe one object", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.arrow([(70, 74), (70, 150)], color=NAVY, sw=1.8)
f.arrow([(130, 74), (130, 150)], color=NAVY, sw=1.8)
f.text(100, 112, "A and B", size=10, color=NAVY)
f.text(300, 18, "Factory", size=12, color=NAVY, bold=True)
f.box(240, 34, 120, 40, "Factory.create(type)", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(215, 150, 80, 44, "Sms\nNotifier", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(305, 150, 80, 44, "Email\nNotifier", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.arrow([(270, 74), (255, 150)], color=NAVY, sw=1.8)
f.arrow([(330, 74), (345, 150)], color=NAVY, sw=1.8)
f.text(300, 218, "both implement Notifier", size=10, color=NAVY)
f.text(505, 18, "Observer", size=12, color=NAVY, bold=True)
f.box(445, 34, 120, 40, "NoticeBoard\n(subject)", fill=BLUE, color=NAVY, size=10, bold=True)
f.box(425, 150, 70, 44, "Sita", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.box(515, 150, 70, 44, "Ram", fill="#fde68a", stroke=AMBER, color=NAVY, size=10, bold=True)
f.arrow([(480, 74), (460, 150)], color=NAVY, sw=1.8, dash=True)
f.arrow([(530, 74), (550, 150)], color=NAVY, sw=1.8, dash=True)
f.text(505, 218, "publish() calls update()", size=10, color=NAVY)
```


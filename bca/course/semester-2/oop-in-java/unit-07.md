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
```output
AppConfig created
NEBians College
same object? true
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
```output
SMS to 9800000000: Exam routine published
Email to 9800000000: Exam routine published
Unknown channel: fax
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
```output
Sita got [Java] Lab moved to Room 4
Ram got [Java] Lab moved to Room 4
Office log: Java / Lab moved to Room 4
Sita got [Java] Assignment due Friday
Office log: Java / Assignment due Friday
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

## 7.5 Copy constructors, shallow copy and deep copy

A **copy constructor** is a constructor that takes an object of its own class and builds a new object with the same state: `Student(Student other)`. Java has no automatic copy constructor (C++ does), so you write it yourself. It is the cleanest way to copy an object, simpler and safer than `clone()`.

The trap is what is copied. Primitive fields are copied by value, but a field that holds an *object reference* copies only the reference, so both objects then share one inner object. That is a **shallow copy**. A **deep copy** also creates new copies of the referenced objects.

```java
import java.util.ArrayList;
import java.util.List;

public class CopyDemo {
    static class Course {
        String title; List<Integer> marks = new ArrayList<>();
        Course(String title) { this.title = title; }

        Course(Course other) {                       // copy constructor (deep)
            this.title = other.title;
            this.marks = new ArrayList<>(other.marks);   // new list, same Integer values
        }
        Course shallow() {                           // shallow: shares the list
            Course c = new Course(title); c.marks = this.marks; return c;
        }
    }

    public static void main(String[] args) {
        Course a = new Course("Java");
        a.marks.add(78);

        Course deep = new Course(a);
        Course shallow = a.shallow();

        a.marks.add(91);                             // change the original
        System.out.println("original: " + a.marks);
        System.out.println("deep copy: " + deep.marks);
        System.out.println("shallow copy: " + shallow.marks);
    }
}
```
```output
original: [78, 91]
deep copy: [78]
shallow copy: [78, 91]
```
The deep copy keeps its own list `[78]`, while the shallow copy sees the new mark because it shares the list with the original. Strings and wrappers are immutable, so sharing them is harmless; the danger is only with **mutable** referenced objects (lists, arrays, `Date`, your own classes). A related defensive habit: when a constructor receives a mutable object, copy it before storing it, and when a getter returns one, return a copy.

## 7.6 Nested and inner classes

A class declared inside another class is a **nested class**. It is used when the helper class makes sense only inside its outer class (a `Node` inside a `LinkedList`), and it can reach the outer class's private members. There are four kinds.

| Kind | Declared | Has outer instance? | Typical use |
|---|---|---|---|
| Static nested class | `static class N` inside the class body | No | helper that does not need the outer object (`Node`, `Builder`) |
| Inner (member) class | `class N` inside the class body | Yes | object tightly tied to one outer object (an iterator over its list) |
| Local class | inside a method body | Yes (if method is non-static) | one-off helper used only in that method |
| Anonymous class | `new Interface() { ... }` expression | Yes (if in an instance context) | one-off implementation; replaced by lambdas for single-method interfaces |

```java
public class NestedDemo {
    private int counter = 100;                       // private field of the outer class

    static class Helper {                            // static nested: no outer object
        static String tag() { return "[static nested]"; }
    }

    class Ticket {                                   // inner: belongs to one NestedDemo
        final int no;
        Ticket() { no = ++counter; }                 // reads and writes outer private field
    }

    interface Greeter { String greet(String n); }

    public static void main(String[] args) {
        System.out.println(Helper.tag());

        NestedDemo office = new NestedDemo();
        NestedDemo.Ticket t1 = office.new Ticket();  // inner class needs an outer object
        NestedDemo.Ticket t2 = office.new Ticket();
        System.out.println("tickets " + t1.no + ", " + t2.no);

        Greeter anon = new Greeter() {               // anonymous class
            public String greet(String n) { return "Namaste, " + n; }
        };
        Greeter lambda = n -> "Namaste, " + n;       // same thing, shorter
        System.out.println(anon.greet("Sita") + " / " + lambda.greet("Ram"));

        class Local {                                // local class
            int twice(int x) { return 2 * x; }
        }
        System.out.println(new Local().twice(21));
    }
}
```
```output
[static nested]
tickets 101, 102
Namaste, Sita / Namaste, Ram
42
```
Key rules. An inner class object always lives inside an outer object, created with `outer.new Inner()` from outside or plainly `new Inner()` from inside. A **static nested** class has no hidden outer reference, so it uses less memory and cannot leak the outer object. Local and anonymous classes can read local variables only if those are `final` or *effectively final* (never reassigned), the same rule lambdas follow. For a single-method interface prefer a lambda; for an interface with several methods, or when the object needs its own fields, an anonymous class is still the tool.

## 7.7 Jagged arrays and variable-length arguments

A two-dimensional array in Java is an **array of arrays**, so the rows need not have equal length. A **rectangular** array is declared `new int[3][4]` (three rows of four). A **jagged** array gives only the number of rows and then creates each row separately.

```java
import java.util.Arrays;

public class JaggedDemo {
    static int total(int... nums) {                  // varargs: zero or more ints
        int s = 0;
        for (int n : nums) s += n;
        return s;
    }

    public static void main(String[] args) {
        int[][] attendance = new int[3][];           // 3 rows, lengths not yet decided
        attendance[0] = new int[]{1, 1, 0, 1};       // Sem I class: 4 sessions
        attendance[1] = new int[]{1, 0};             // Sem II class: 2 sessions
        attendance[2] = new int[]{1, 1, 1};          // Sem III class: 3 sessions

        for (int r = 0; r < attendance.length; r++)
            System.out.println("row " + r + " (length " + attendance[r].length + "): "
                               + Arrays.toString(attendance[r]));

        int[][] grid = new int[2][3];                // rectangular, filled with default 0
        System.out.println(Arrays.deepToString(grid));

        System.out.println(total());                 // 0
        System.out.println(total(5));                // 5
        System.out.println(total(5, 10, 15));        // 30
    }
}
```
```output
row 0 (length 4): [1, 1, 0, 1]
row 1 (length 2): [1, 0]
row 2 (length 3): [1, 1, 1]
[[0, 0, 0], [0, 0, 0]]
0
5
30
```
A **varargs** parameter (`int... nums`) accepts any number of arguments and inside the method is an ordinary array. Rules: only one varargs parameter, and it must be the **last** one in the list (`void log(String level, String... msgs)`). `System.out.printf` and `String.format` are the varargs methods you use most.

## 7.8 Lambdas, streams, `Optional` and method references: the syllabus checklist

Unit 5 explained these in detail; the last item of the syllabus is only to be able to *use* them together. The short reference below is what a practical question expects.

| Feature | Form | Replaces |
|---|---|---|
| Lambda | `(a, b) -> a + b` | anonymous class for a single-method interface |
| Method reference | `String::toUpperCase`, `System.out::println`, `Student::new` | a lambda that only calls one method or constructor |
| Stream | `list.stream().filter(...).map(...).collect(...)` | explicit loop with temporary lists |
| `Optional<T>` | `Optional.ofNullable(x).map(...).orElse(d)` | `null` checks and `null` returns |

```java
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

public class AdvancedDemo {
    static Optional<String> findStudent(List<String> names, String prefix) {
        return names.stream().filter(n -> n.startsWith(prefix)).findFirst();
    }

    public static void main(String[] args) {
        List<String> names = List.of("sita", "ram", "gita", "hari");

        List<String> upper = names.stream()
                .filter(n -> n.length() == 4)            // lambda
                .map(String::toUpperCase)                // method reference
                .sorted()
                .collect(Collectors.toList());
        System.out.println(upper);

        names.forEach(System.out::println);              // method reference to an instance method

        System.out.println(findStudent(names, "h").orElse("nobody"));
        System.out.println(findStudent(names, "z").orElse("nobody"));
        System.out.println(findStudent(names, "r").map(String::length).orElse(0));
    }
}
```
```output
[GITA, HARI, SITA]
sita
ram
gita
hari
hari
nobody
3
```
`Optional` makes "there may be no result" visible in the method's return type, so the caller is forced to decide what to do (`orElse`, `orElseThrow`, `ifPresent`). Never call `get()` without checking `isPresent()`, and do not use `Optional` for fields or parameters.

## 7.9 Eight uses of patterns and advanced OOP features

1. **One shared resource.** A singleton ensures a logger or a configuration is created once and every class sees the same settings.
2. **Hiding `new`.** A factory keeps the choice of class in one method, so a change from SMS to push notifications touches one file.
3. **Loose coupling.** An observer-style subject does not know what its listeners do; new listeners are added without editing it.
4. **Event handling.** Swing buttons, Android click listeners and web frameworks are all the observer pattern behind a different name.
5. **Safe copies.** Copy constructors and defensive copies stop one part of a program from silently changing another part's data.
6. **Encapsulated helpers.** Nested classes keep a helper type next to the only class that uses it, and out of the package's public face.
7. **Irregular data.** Jagged arrays store rows of different lengths (attendance per class, triangles, adjacency lists) without wasting memory.
8. **Shorter, clearer code.** Lambdas, method references, streams and `Optional` replace loops and null checks with a description of *what* is wanted.

## Formula and fact sheet

- Singleton: `private` constructor + `private static` instance + `public static getInstance()`; synchronize or use an enum for thread safety.
- Factory: one method returns an interface type; callers never write `new` for the concrete class. Adding a product = new class + one `case`.
- Observer: subject keeps `List<Observer>`; `subscribe`, `unsubscribe`, `publish` loops calling `update`.
- Copy constructor: `T(T other)`; shallow copies share mutable references, deep copies do not.
- Nested kinds: static nested, inner, local, anonymous. Inner needs `outer.new Inner()`.
- Jagged: `new int[rows][]` then `a[i] = new int[len]`. Varargs: `T... x`, last parameter, behaves as an array.
- `Optional`: `ofNullable`, `map`, `orElse`, `orElseThrow`, `ifPresent`; avoid bare `get()`.

## Chapter summary

- A design pattern is a named solution to a recurring design problem; the three required ones are singleton, factory and observer.
- Singleton restricts a class to one instance; factory centralises object creation behind an interface; observer lets a subject broadcast to many subscribed objects.
- Copy constructors make explicit copies; shallow copies share mutable inner objects, deep copies do not.
- Nested classes come in four kinds; lambdas replace most anonymous classes for single-method interfaces.
- Jagged arrays have rows of different lengths; varargs lets a method take any number of arguments.

## Practice

1. Define a design pattern and name its three families with one example each.
2. Write a thread-safe singleton `Logger` with a method `log(String)` that numbers each message.
3. Why is the constructor of a singleton private? What goes wrong if two threads call `getInstance()` at the same time on an unsynchronized lazy version?
4. Write a factory that returns `Shape` objects (`Circle`, `Rectangle`) from the strings `"circle"` and `"rectangle"`.
5. Explain the observer pattern with a class diagram or a list of classes and one real example.
6. What is the difference between a shallow and a deep copy? Show with a class that holds an `ArrayList`.
7. List the four kinds of nested class and give one use of each.
8. Create a jagged array of three rows with 1, 2 and 3 elements and print it.
9. Write a varargs method `max(int... a)` and explain why it must be the last parameter.
10. Rewrite `Collections.sort(list, new Comparator<String>() { ... })` using a lambda and then a method reference.

::: note Answers and worked solutions
**1.** A reusable, named solution to a common design problem. Creational (singleton), structural (adapter), behavioural (observer).
**2.** `class Logger { private static Logger inst; private int n; private Logger(){} static synchronized Logger get(){ if(inst==null) inst=new Logger(); return inst;} void log(String m){ System.out.println(++n + ": " + m);} }`
**3.** A private constructor stops other classes writing `new`. Without synchronization, two threads can both see `inst == null` and create two objects, so the "single" instance is no longer single.
**4.** `interface Shape { double area(); }` with `Circle` and `Rectangle` implementing it, and `static Shape of(String t){ switch(t){ case "circle": return new Circle(1); case "rectangle": return new Rectangle(2,3); default: throw new IllegalArgumentException(t);} }`
**5.** Classes: `Subject` (list of observers, `subscribe`, `publish`), `Observer` interface (`update`), concrete observers. Example: a notice board and its subscribed students.
**6.** Shallow: the copy's list field points to the same list; changing one changes the other. Deep: the copy gets `new ArrayList<>(other.list)`.
**7.** Static nested (helper `Node`), inner (an iterator), local (one-off helper in a method), anonymous (inline interface implementation).
**8.** `int[][] a = new int[3][]; for (int i = 0; i < 3; i++) a[i] = new int[i + 1]; System.out.println(Arrays.deepToString(a));` prints `[[0], [0, 0], [0, 0, 0]]`.
**9.** `static int max(int... a){ int m = a[0]; for(int x : a) if(x > m) m = x; return m; }`. It must be last because the compiler cannot tell where the varargs list ends if other parameters follow it.
**10.** `list.sort((a, b) -> a.compareTo(b));` and then `list.sort(String::compareTo);` (or `Comparator.naturalOrder()`).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is the singleton pattern? Write a program to implement it.**

*Intent.* Ensure that a class has only one instance and provide a global point of access to it.

*Steps.* (1) private constructor; (2) private static field holding the instance; (3) public static method returning it, creating it on first use.

```java
public class OneOnly {
    static class Settings {
        private static Settings inst;
        private Settings() { System.out.println("created once"); }
        static synchronized Settings get() {
            if (inst == null) inst = new Settings();
            return inst;
        }
    }
    public static void main(String[] args) {
        Settings x = Settings.get(), y = Settings.get();
        System.out.println(x == y);
    }
}
```
```output
created once
true
```
*Use.* Logger, configuration, database connection pool. `synchronized` keeps it safe when threads race.

**Q2 (5 marks). Explain the factory pattern with an example. Why is it useful?**

*Idea.* A factory method creates objects and returns them through an interface, so callers never name the concrete class.

*Example.* `Notifier n = NotifierFactory.create("sms");` returns an `SmsNotifier`; `create("email")` returns an `EmailNotifier`; both implement `Notifier.send()`.

*Benefits.* (1) The choice of class is in one place. (2) New products are added without changing the callers (open/closed principle). (3) Callers depend on the interface, so they are easy to test with fake objects.

**Q3 (10 marks). Explain the observer pattern. Write a Java program with one subject and two observers.**

*Introduction.* The observer pattern defines a one-to-many link: when the subject changes, every registered observer is told automatically (Figure 7.1, right).

*Participants.* (1) `Observer` interface with `update(...)`. (2) `Subject` that stores `List<Observer>` and offers `subscribe`, `unsubscribe`, `publish`. (3) Concrete observers that decide how to react.

*Working.* An observer subscribes; when `publish()` is called the subject loops over its list and calls `update` on each. The subject never mentions concrete observer classes, so coupling is loose.

*Program.* The `NoticeBoard`, `Student` and lambda observer program of Section 7.4 has one subject and three observers; after `unsubscribe(ram)` only the remaining observers receive the second notice.

*Real uses.* GUI listeners, publish-subscribe messaging, stock tickers, YouTube subscriptions.

*Limits.* Notification order is fixed by subscription order; a slow observer delays the rest; forgetting to unsubscribe keeps objects alive (a memory leak). `java.util.Observable` is deprecated since Java 9.

**Q4 (5 marks). What are nested classes? Describe their types.**

A nested class is a class declared inside another class. **Static nested** classes are attached to the outer class and need no outer object. **Inner** classes belong to an outer object and can use its private members. **Local** classes are declared inside a method. **Anonymous** classes have no name and are created with `new Interface() { ... }` for one-off use; for single-method interfaces a lambda is shorter. Reasons to nest: logical grouping, better encapsulation, and readable code.

**Q5 (5 marks). Differentiate a shallow copy from a deep copy and show a copy constructor.**

A shallow copy duplicates the object but its reference fields point to the same inner objects, so a change through one copy is visible in the other. A deep copy also duplicates the inner mutable objects. A copy constructor such as `Course(Course o){ title = o.title; marks = new ArrayList<>(o.marks); }` makes a deep copy; the program in Section 7.5 prints `[78]` for the deep copy and `[78, 91]` for the shallow one after the original is changed.

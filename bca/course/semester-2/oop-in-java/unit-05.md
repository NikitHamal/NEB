---
subject: OOP in Java
grade: BCA Semester 2
unit: 5
title: Generics, Collections, Lambdas, Streams and File I/O
area: BCA 153 · OOP in Java · Unit 5
---

Real programs store many objects and read and write files. Java's **Collections Framework** provides ready-made, tested data structures; **generics** make them type-safe; **lambdas and streams** let you process them declaratively; and the **I/O classes** connect programs to files. This unit gives a working command of all four.

::: key What this unit gives you
- Generic classes and methods, bounded types, wildcards.
- `List`, `Set`, `Map`, `Queue`, `Deque` and the right implementation for each job (with complexity).
- Lambdas, method references, and the Stream API.
- Text and binary file I/O with `java.nio.file`, and serialization basics.
:::

## 5.1 Generics

**Generics** parameterise a class, interface or method by type, giving compile-time type safety and removing casts. Without generics a `List` holds `Object` and errors appear at run time; with `List<String>` the compiler rejects `list.add(5)`.

```java
import java.util.*;
class Box<T> {
    private T v;
    Box(T v) { this.v = v; }
    T get() { return v; }
}
public class Gen {
    static <T extends Comparable<T>> T maxOf(List<T> l) {
        T m = l.get(0);
        for (T x : l) if (x.compareTo(m) > 0) m = x;
        return m;
    }
    static double sum(List<? extends Number> l) {
        double s = 0;
        for (Number n : l) s += n.doubleValue();
        return s;
    }
    public static void main(String[] a) {
        Box<String> b = new Box<>("hi");
        System.out.println(b.get().length());
        System.out.println(maxOf(Arrays.asList(3, 9, 4)) + " " + maxOf(Arrays.asList("pear", "apple", "zebra")));
        System.out.println(sum(List.of(1, 2.5, 3L)));
    }
}
```
```output
2
9 zebra
6.5
```

- **Bounded type** `T extends Comparable<T>` allows `compareTo` inside the method.
- **Wildcards**: `List<?>` (unknown), `List<? extends Number>` (read-only producer), `List<? super Integer>` (consumer): "PECS: producer extends, consumer super".
- **Type erasure**: generics exist only at compile time; at run time `List<String>` and `List<Integer>` are both `List`, so you cannot do `new T()`, `instanceof List<String>` or create generic arrays. Primitives are not allowed (`List<int>` is illegal; use `List<Integer>`).

## 5.2 The Collections Framework

```text
Iterable → Collection → List  (ordered, duplicates)      ArrayList, LinkedList
                      → Set   (no duplicates)            HashSet, LinkedHashSet, TreeSet
                      → Queue → Deque                    ArrayDeque, LinkedList, PriorityQueue
Map (key → value; not a Collection)                      HashMap, LinkedHashMap, TreeMap
```

| Implementation | Order | Get / contains | Add | Notes |
|---|---|---|---|---|
| `ArrayList` | insertion | O(1) by index | O(1) amortised at end | the default list |
| `LinkedList` | insertion | O(n) | O(1) at ends | rarely better than ArrayList |
| `HashSet` / `HashMap` | none | O(1) average | O(1) | needs good `hashCode`/`equals` |
| `LinkedHashSet` / `LinkedHashMap` | insertion | O(1) | O(1) | predictable iteration |
| `TreeSet` / `TreeMap` | sorted | O(log n) | O(log n) | red–black tree; range queries |
| `ArrayDeque` | FIFO/LIFO | | O(1) at ends | stack and queue |
| `PriorityQueue` | heap order | peek O(1) | O(log n) | smallest (or custom) first |

```java
import java.util.*;
import java.util.stream.*;
public class Collect {
    record Student(String name, int marks) {}
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>(List.of(5, 3, 8, 3, 1));
        Collections.sort(list);
        System.out.println(list);
        Set<Integer> set = new TreeSet<>(list);
        System.out.println(set);
        Map<String, Integer> m = new TreeMap<>();
        for (String w : "to be or not to be".split(" ")) m.merge(w, 1, Integer::sum);
        System.out.println(m);
        Deque<Integer> st = new ArrayDeque<>();
        st.push(1); st.push(2);
        System.out.println(st.pop() + " " + st.peek());
        Queue<String> q = new LinkedList<>();
        q.offer("a"); q.offer("b");
        System.out.println(q.poll() + q.size());
        PriorityQueue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder());
        pq.addAll(list);
        System.out.println(pq.poll());
        List<Student> ss = List.of(new Student("Sita", 82), new Student("Ram", 67), new Student("Hari", 74), new Student("Gita", 91));
        System.out.println(ss.stream().filter(s -> s.marks() >= 70).map(Student::name).sorted().collect(Collectors.toList()));
        System.out.println(ss.stream().mapToInt(Student::marks).average().getAsDouble());
        System.out.println(ss.stream().max(Comparator.comparingInt(Student::marks)).get());
        Map<String, Long> g = ss.stream().collect(Collectors.groupingBy(s -> s.marks() >= 75 ? "high" : "low", TreeMap::new, Collectors.counting()));
        System.out.println(g);
    }
}
```
```output
[1, 3, 3, 5, 8]
[1, 3, 5, 8]
{be=2, not=1, or=1, to=2}
2 1
a1
8
[Gita, Hari, Sita]
78.5
Student[name=Gita, marks=91]
{high=2, low=2}
```

**Iterating safely:** use the enhanced `for` or an `Iterator` (`it.remove()` to delete); removing inside an enhanced `for` throws `ConcurrentModificationException`; use `list.removeIf(x -> x < 0)`. **Immutable factories:** `List.of`, `Set.of`, `Map.of` (modification throws `UnsupportedOperationException`). **Utilities:** `Collections.sort/reverse/shuffle/max/min/unmodifiableList/frequency`, `Arrays.asList`. `Map` operations: `put`, `get`, `getOrDefault`, `containsKey`, `merge`, `computeIfAbsent`, `entrySet()`; for a **word-frequency count** use `merge(word, 1, Integer::sum)`.

## 5.3 Lambdas and method references

A **lambda** is an anonymous function that implements a functional interface: `(a, b) -> a + b`, `x -> x * x`, `() -> System.out.println("hi")`. A **method reference** is shorthand: `String::length`, `System.out::println`, `Student::new`.

| Interface | Method | Example |
|---|---|---|
| `Predicate<T>` | `boolean test(T)` | `s -> s.isEmpty()` |
| `Function<T,R>` | `R apply(T)` | `String::length` |
| `Consumer<T>` | `void accept(T)` | `System.out::println` |
| `Supplier<T>` | `T get()` | `() -> new ArrayList<>()` |
| `BiFunction<T,U,R>`, `UnaryOperator<T>`, `BinaryOperator<T>` | | `Integer::sum` |
| `Comparator<T>` | `int compare(T,T)` | `Comparator.comparing(Student::name)` |

A lambda may use local variables only if they are **effectively final** (never reassigned).

## 5.4 Streams

A **stream** is a pipeline: **source** → zero or more **intermediate** operations (lazy: `filter`, `map`, `sorted`, `distinct`, `limit`, `skip`) → one **terminal** operation (`collect`, `forEach`, `count`, `sum`, `reduce`, `min`, `max`, `anyMatch`, `findFirst`). Streams do not change the source.

```java
import java.util.*;
import java.util.stream.*;
public class Streams {
    public static void main(String[] args) {
        List<Integer> nums = List.of(4, 8, 15, 16, 23, 42);
        System.out.println(nums.stream().filter(n -> n % 2 == 0).map(n -> n * n).collect(Collectors.toList()));
        System.out.println(nums.stream().reduce(0, Integer::sum));
        System.out.println(IntStream.rangeClosed(1, 5).mapToObj(Integer::toString).collect(Collectors.joining("+")));
        Map<Character, Integer> byInitial = Stream.of("kathmandu", "pokhara", "biratnagar")
            .collect(Collectors.toMap(s -> s.charAt(0), String::length, (x, y) -> x, TreeMap::new));
        System.out.println(byInitial);
        System.out.println(nums.stream().anyMatch(n -> n > 40) + " " + nums.stream().allMatch(n -> n > 5));
        System.out.println(nums.stream().mapToInt(Integer::intValue).summaryStatistics());
    }
}
```
```output
[16, 64, 256, 1764]
108
1+2+3+4+5
{b=10, k=9, p=7}
true false
IntSummaryStatistics{count=6, sum=108, min=4, average=18.000000, max=42}
```

`parallelStream()` splits work across cores, helpful only for large CPU-bound data with no shared state. `Optional<T>` models "maybe absent" (`findFirst().orElse(default)`) and avoids `null` returns.

## 5.5 File I/O

Two families: **byte streams** (`InputStream`, `OutputStream`, `FileInputStream`) for binary data and **character streams** (`Reader`, `Writer`, `BufferedReader`, `FileWriter`, `PrintWriter`) for text; wrap with `Buffered…` for speed. Prefer the modern **`java.nio.file`** API (`Path`, `Files`).

```java
import java.io.*;
import java.nio.file.*;
import java.util.*;
public class Files1 {
    public static void main(String[] a) throws IOException {
        Path p = Files.createTempFile("neb", ".txt");
        Files.write(p, List.of("alpha", "beta", "gamma"));
        try (BufferedReader br = Files.newBufferedReader(p)) {
            String line; int n = 0;
            while ((line = br.readLine()) != null) n += line.length();
            System.out.println(n);
        }
        try (PrintWriter pw = new PrintWriter(new FileWriter(p.toFile(), true))) { pw.println("delta"); }
        System.out.println(Files.readAllLines(p).size());
        System.out.println(Files.size(p));
        Files.delete(p);
        System.out.println(Files.exists(p));
    }
}
```
```output
14
4
23
false
```

The file holds `alpha`, `beta`, `gamma`, `delta`: 5 + 4 + 5 + 5 = 19 characters plus 4 newline bytes = **23 bytes** (on Windows the line separator is two bytes, so the size would be 27; the sample output was produced on Linux). The first count, 14, is the length of the first three lines without newlines.

**Other I/O facts.** `Scanner(new File(…))` reads tokens; `Files.lines(path)` gives a lazy `Stream<String>`; `File` represents a path and gives `exists()`, `isDirectory()`, `listFiles()`, `length()`. **Always close** streams (try-with-resources). Use `Charset` explicitly (`StandardCharsets.UTF_8`) so Nepali text (Devanagari) survives. **`RandomAccessFile`** allows seeking; `DataOutputStream`/`DataInputStream` write primitives in binary.

**Serialization.** A class implementing the marker interface `Serializable` can be written with `ObjectOutputStream.writeObject(obj)` and restored with `ObjectInputStream.readObject()`; fields marked `transient` are skipped; declare `private static final long serialVersionUID`. Modern systems often prefer JSON (via Jackson or Gson) for portability; never deserialize untrusted data.

## 5.6 The framework map and the stream pipeline

Java's Collections Framework is a family tree (Figure 5.1). `Collection` has three main branches: `List` (ordered, duplicates allowed), `Set` (no duplicates) and `Queue`/`Deque` (processing order). `Map` stores key–value pairs and sits on its own branch because it is not a `Collection`. The class names tell you the mechanism: `Array` (resizable array, fast by index), `Linked` (nodes, fast at the ends), `Hash` (hash table, fast lookup, no order), `Tree` (sorted tree, ordered, log n). Figure 5.2 shows a **stream**, which treats data as a conveyor belt: a source feeds *intermediate* operations (`filter`, `map`, `sorted`) that are lazy, and one *terminal* operation (`collect`, `count`, `forEach`) starts the work.

```svgfig label="5.1" caption="Collections Framework. Interfaces are amber; common implementations are white. Map is separate from Collection. Pick by need: ArrayList for index access, HashSet/HashMap for fast lookup, TreeSet/TreeMap for sorted order, ArrayDeque for stacks and queues."
f = Fig(600, 250)
f.box(230, 8, 140, 34, "Iterable", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(230, 62, 140, 34, "Collection", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.arrow([(300, 42), (300, 62)], color=SLATE, sw=1.6)
for x, n, impl in ((20, "List", "ArrayList\nLinkedList"), (170, "Set", "HashSet\nTreeSet"), (320, "Queue / Deque", "ArrayDeque\nPriorityQueue")):
    f.box(x, 130, 130, 34, n, fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
    f.arrow([(300, 96), (300, 112), (x + 65, 112), (x + 65, 130)], color=SLATE, sw=1.4)
    f.box(x, 190, 130, 44, impl, fill="#ffffff", stroke=NAVY, color=NAVY, size=10.5, bold=True)
    f.arrow([(x + 65, 164), (x + 65, 190)], color=SLATE, sw=1.4, dash=True)
f.box(475, 62, 110, 34, "Map", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(475, 190, 110, 44, "HashMap\nTreeMap", fill="#ffffff", stroke=NAVY, color=NAVY, size=10.5, bold=True)
f.arrow([(530, 96), (530, 190)], color=SLATE, sw=1.4, dash=True)
f.text(530, 130, "key -> value", size=10.5, color=RED, bold=True)
f.text(530, 148, "not a Collection", size=10, color=SLATE)
```

```svgfig label="5.2" caption="A stream pipeline over six marks. filter keeps marks of 60 or more, map turns each into a grade point, sorted orders them, and the terminal operation collect gathers the result. Nothing runs until the terminal operation is called."
f = Fig(600, 190)
f.box(10, 70, 100, 50, "source\nlist.stream()", fill=BLUE, color=NAVY, size=10.5, bold=True)
f.box(140, 70, 100, 50, "filter\nmarks >= 60", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.box(270, 70, 100, 50, "map\nmarks / 10.0", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.box(400, 70, 80, 50, "sorted", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.box(510, 70, 80, 50, "collect\n(terminal)", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10.5, bold=True)
for x1, x2 in ((110, 140), (240, 270), (370, 400), (480, 510)):
    f.arrow([(x1, 95), (x2, 95)], color=SLATE, sw=2)
f.text(60, 150, "88 72 45 61 55 90", size=10.5, color=NAVY, bold=True)
f.text(190, 150, "88 72 61 90", size=10.5, color=NAVY, bold=True)
f.text(320, 150, "8.8 7.2 6.1 9.0", size=10.5, color=NAVY, bold=True)
f.text(440, 150, "6.1 7.2 8.8 9.0", size=10.5, color=NAVY, bold=True)
f.text(550, 150, "List", size=10.5, color=TEAL, bold=True)
f.text(300, 30, "intermediate operations are lazy; the terminal operation pulls the data through", size=11, color=RED, bold=True)
```

## 5.7 Eight uses of collections, lambdas and streams

1. **Growing data without fixed size.** An `ArrayList` expands automatically, so a program need not guess how many students will enrol. Arrays in Java must be sized in advance. A library system can add members all year without code changes.
2. **Fast lookup by key.** A `HashMap` finds a value from its key in about constant time. Searching a citizenship-number table of a million records takes the same few steps as one of a hundred. This is how caches and login tables work.
3. **Removing duplicates.** Putting items into a `Set` drops repeats automatically. A college can collect the unique faculties of its students from a long list of records in a single line.
4. **Sorted data.** `TreeMap`, `TreeSet` and `Collections.sort` keep or put data in order. A merit list sorted by marks, or a leaderboard, is produced with a comparator instead of hand-written sorting code.
5. **Queues and stacks.** `ArrayDeque` supports first-in-first-out and last-in-first-out processing. A ticket counter queue and the undo stack of a text editor are both modelled with it.
6. **Type safety with generics.** `List<String>` allows only strings, and the compiler rejects anything else. Casting errors that once appeared at run time are found when compiling.
7. **Short, clear code with lambdas.** A lambda such as `(a, b) -> b.marks() - a.marks()` passes behaviour as data. Sorting, event handling and threading code becomes a line or two instead of a whole class.
8. **Data processing with streams.** Streams filter, map, group and total data in a readable pipeline. Average marks per faculty or the count of students above 60 are computed without explicit loops, and the same pipeline can be made parallel.

## Formula and fact sheet

- Generics: compile-time safety, erased at run time; `<T extends X>` bounded; PECS wildcards.
- ArrayList (index O(1)), HashMap/HashSet (O(1) average), TreeMap/TreeSet (O(log n), sorted), ArrayDeque (stack/queue), PriorityQueue (heap).
- Lambda = implementation of a functional interface; variables captured must be effectively final.
- Stream: source → lazy intermediate ops → one terminal op; the source is unchanged.
- Use `java.nio.file.Files`, try-with-resources, explicit UTF-8.
- `Serializable` + `transient`; avoid deserialising untrusted data.

## Chapter summary

- Generics make collections type-safe, and the framework offers the right structure for each access pattern.
- Choosing between list, set, map, queue and their implementations is a question of ordering, uniqueness and cost.
- Lambdas and streams express filter-map-reduce logic concisely and safely.
- File I/O is done with buffered, closed-after-use readers and writers or the `Files` helpers.

## Practice

1. Write a generic method `swap(T[] arr, int i, int j)` and a generic class `Pair<A, B>`.
2. Count the frequency of each word in `"the cat and the hat and the bat"` using a `Map`.
3. Choose a collection for each: (a) unique roll numbers in sorted order, (b) undo history, (c) tasks served by priority, (d) a phone book. Justify.
4. Remove all negative numbers from a list safely in two ways.
5. Using streams, find the names of students with marks above the average, sorted descending by marks.
6. Using `reduce`, compute the product of 1 to 6.
7. Write a program that reads a text file and prints its number of lines, words and characters.
8. Differentiate `ArrayList` and `LinkedList`, and `HashMap` and `TreeMap`.
9. Why does `list.remove(i)` inside an enhanced for loop fail?
10. What is `transient`? When do you need `serialVersionUID`?

::: note Answers and worked solutions
**1.** `static <T> void swap(T[] a, int i, int j) { T t = a[i]; a[i] = a[j]; a[j] = t; }` and `class Pair<A, B> { final A first; final B second; Pair(A a, B b) { first = a; second = b; } }`.
**2.** `for (String w : text.split(" ")) m.merge(w, 1, Integer::sum);` gives {and=2, bat=1, cat=1, hat=1, the=3} (for a `TreeMap`).
**3.** (a) `TreeSet<Integer>` (unique and sorted). (b) `ArrayDeque` used as a stack. (c) `PriorityQueue`. (d) `HashMap<String, String>` (or `TreeMap` for alphabetical listing).
**4.** `list.removeIf(x -> x < 0);` or an `Iterator` with `it.remove()` when `x < 0`.
**5.** `double avg = ss.stream().mapToInt(Student::marks).average().orElse(0); ss.stream().filter(s -> s.marks() > avg).sorted(Comparator.comparingInt(Student::marks).reversed()).map(Student::name).toList();`
**6.** `IntStream.rangeClosed(1, 6).reduce(1, (a, b) -> a * b)` is **720**.
**7.** `List<String> lines = Files.readAllLines(p); long words = lines.stream().flatMap(l -> Arrays.stream(l.trim().split("\\s+"))).filter(w -> !w.isEmpty()).count(); long chars = Files.size(p);` (bytes; for characters use the string length).
**8.** ArrayList: array-backed, O(1) index, fast iteration; LinkedList: node-based, O(1) insert at known nodes but O(n) access. HashMap: unordered O(1); TreeMap: sorted keys O(log n).
**9.** Modifying the list while its iterator is active changes `modCount`; the iterator detects it and throws `ConcurrentModificationException`.
**10.** `transient` excludes a field from serialization (passwords, caches). `serialVersionUID` is the class version id; set it explicitly so that compatible changes to the class do not make old serialized data unreadable.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the List, Set and Map interfaces of the Collections Framework with a program. Differentiate ArrayList and LinkedList.**

*Introduction.* The Collections Framework provides ready-made data structures behind common interfaces (Figure 5.1), so a program can change the implementation without changing the code that uses it.

*Interfaces.*

1. **`List`.** An ordered sequence with duplicates and index access: `ArrayList`, `LinkedList`.
2. **`Set`.** No duplicates: `HashSet` (unordered, fast), `LinkedHashSet` (insertion order), `TreeSet` (sorted).
3. **`Map`.** Unique keys mapped to values: `HashMap`, `TreeMap`; useful methods are `put`, `get`, `getOrDefault`, `merge`.

```java
import java.util.*;

public class CollDemo {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>(List.of("Sita", "Ram", "Hari", "Sita"));
        Set<String> unique = new TreeSet<>(names);
        Set<String> inOrder = new LinkedHashSet<>(names);
        Map<String, Integer> count = new TreeMap<>();
        for (String n : names) count.merge(n, 1, Integer::sum);
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1); stack.push(2); stack.push(3);
        System.out.println("list   = " + names);
        System.out.println("TreeSet = " + unique + ", LinkedHashSet = " + inOrder);
        System.out.println("counts = " + count + ", Ram -> " + count.getOrDefault("Ram", 0) + ", Gita -> " + count.getOrDefault("Gita", 0));
        System.out.println("stack pop = " + stack.pop() + ", peek = " + stack.peek());
    }
}
```
```output
list   = [Sita, Ram, Hari, Sita]
TreeSet = [Hari, Ram, Sita], LinkedHashSet = [Sita, Ram, Hari]
counts = {Hari=1, Ram=1, Sita=2}, Ram -> 1, Gita -> 0
stack pop = 3, peek = 2
```

*ArrayList versus LinkedList.*

| Operation | `ArrayList` | `LinkedList` |
|---|---|---|
| Get by index | O(1) | O(n) |
| Add at end | O(1) amortised | O(1) |
| Insert/remove in middle | O(n) shifting | O(1) after reaching the node |
| Memory | compact array | extra link per element |

*Conclusion.* Choose the interface for what you need (order, uniqueness, lookup) and the implementation for speed; `ArrayList` is the right default for lists.

**Q2 (10 marks). Explain lambda expressions, the `Stream` API and generics, and write a program that filters, sorts, groups and totals student records.**

*Introduction.* Java 8 added lambdas and streams for a functional style. Generics, from Java 5, make collections type-safe. Together they let a program process data in a short pipeline (Figure 5.2).

*Concepts.*

1. **Lambda.** An anonymous function `(parameters) -> expression`, usable wherever a functional interface (one abstract method) is expected, such as `Comparator` or `Runnable`.
2. **Method reference.** A shorter lambda: `String::length`, `System.out::println`.
3. **Stream.** A sequence of elements from a source, processed by operations; it does not store data and cannot be reused.
4. **Intermediate operations.** `filter`, `map`, `sorted`, `distinct`, `limit`; lazy.
5. **Terminal operations.** `collect`, `count`, `sum`, `forEach`, `reduce`; start the pipeline.
6. **Collectors.** `toList`, `joining`, `groupingBy`, `partitioningBy`, `averagingInt`.
7. **Generics.** `List<T>` and methods such as `<T extends Comparable<T>> T max(List<T>)` work for many types with compile-time checking.
8. **Records.** A compact immutable data class, ideal as stream elements.

```java
import java.util.*;
import java.util.stream.*;

public class StreamDemo {
    record Student(String name, String faculty, int marks) {}
    static <T extends Comparable<T>> T max(List<T> list) {
        T best = list.get(0);
        for (T t : list) if (t.compareTo(best) > 0) best = t;
        return best;
    }
    public static void main(String[] args) {
        List<Student> s = List.of(new Student("Sita", "BCA", 88), new Student("Ram", "BBA", 72),
            new Student("Hari", "BCA", 45), new Student("Gita", "BBA", 61),
            new Student("Mina", "BCA", 55), new Student("Bimal", "BIT", 90));
        System.out.println("passed: " + s.stream().filter(x -> x.marks() >= 60)
            .sorted((a, b) -> b.marks() - a.marks()).map(Student::name).collect(Collectors.joining(", ")));
        System.out.println("average by faculty: " + s.stream().collect(
            Collectors.groupingBy(Student::faculty, TreeMap::new, Collectors.averagingInt(Student::marks))));
        System.out.println("pass/fail counts: " + s.stream().collect(
            Collectors.partitioningBy(x -> x.marks() >= 50, Collectors.counting())));
        System.out.println("total marks = " + s.stream().mapToInt(Student::marks).sum());
        System.out.println("generic max = " + max(List.of(7, 42, 19)) + ", " + max(List.of("ram", "sita", "hari")));
    }
}
```
```output
passed: Bimal, Sita, Ram, Gita
average by faculty: {BBA=66.5, BCA=62.666666666666664, BIT=90.0}
pass/fail counts: {false=1, true=5}
total marks = 411
generic max = 42, sita
```

| Feature | Loop style | Stream style |
|---|---|---|
| Describes | how to iterate | what result is wanted |
| State | mutable counters | none |
| Parallel | manual threads | `parallelStream()` |

*Conclusion.* Lambdas pass behaviour, streams express data processing as a pipeline, and generics keep it type-safe; the program above replaces four loops with four short expressions.

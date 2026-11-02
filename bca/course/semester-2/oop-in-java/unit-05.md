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

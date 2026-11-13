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

### Generics: a typed container

A shipping container is labelled with what it holds, and the port refuses to load a different cargo. `List<String>` is the same idea: the compiler knows the cargo type, so adding an `Integer` is rejected before the program runs, and no cast is needed when you take an element out. Under the surface a `HashMap` uses `hashCode` to choose a bucket among 16 at the start. Plate 5.1 computes the bucket for six names with Java's own formulas: `h ^ (h >>> 16)` then `& 15`.

```photogrid label="5.1" cols="2" ratio="1.4" caption="A labelled container and a bucket choice. (a) Stacked shipping containers, each for one kind of cargo. (b) The bucket (0 to 15) that a HashMap with 16 buckets chooses for six names, computed with String.hashCode and the HashMap spreading step h ^ (h >>> 16); two names in one bucket form a collision."
@ photo id="bca153/containers" cap="Containers: one label, one kind of cargo"
fit 1.4
focus 0.5 0.5
@ svg cap="HashMap bucket for each name"
def jhash(s):
    h = 0
    for c in s: h = (31 * h + ord(c)) & 0xFFFFFFFF
    return h
def bucket(s, n=16):
    h = jhash(s); return (h ^ (h >> 16)) & (n - 1)
names = ["Sita", "Ram", "Gita", "Hari", "Maya", "Bikash"]
bk = {n: bucket(n) for n in names}
assert jhash("NEB") == 77163 and all(0 <= b < 16 for b in bk.values())
from collections import Counter
cnt = Counter(bk.values())
f = Fig(400, 250)
f.text(200, 16, "name  ->  hashCode  ->  bucket (of 16)", size=11, color=NAVY, bold=True)
for i, n in enumerate(names):
    y = 28 + i * 28
    f.box(6, y, 388, 24, "", fill=BLUE if cnt[bk[n]] == 1 else ROSE, stroke=NAVY if cnt[bk[n]] == 1 else RED, r=3)
    f.text(12, y + 12, n, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(180, y + 12, f"{jhash(n):,}", size=10.5, color=SLATE, anchor="middle", vmid=True)
    f.text(384, y + 12, f"bucket {bk[n]}", size=10.5, color=RED if cnt[bk[n]] > 1 else TEAL, bold=True, anchor="end", vmid=True)
col = sum(1 for v in cnt.values() if v > 1)
f.text(200, 214, "Red rows share a bucket (collision)." if col else "All six names fall in different buckets.", size=10.5, color=SLATE, bold=True)
f.text(200, 234, "hashCode (unsigned shown) -> (h ^ (h >>> 16)) & 15", size=10.5, color=SLATE)
```

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

### A stream is a pipeline

A water filter passes water through stages, each removing something, and what leaves is cleaner than what entered. A stream pipeline in Java is the same: a source, some intermediate stages such as `filter` and `map`, and one terminal stage such as `sum` that pulls the data through. Nothing runs until the terminal stage is called. Plate 5.2 follows the numbers 1 to 10 through `filter(even)`, `map(square)` and `sum`: ten items go in, five survive the filter, five are squared and one total comes out.

```photogrid label="5.2" cols="2" ratio="1.4" caption="Stages that each do one job. (a) An under-sink water filter: water goes through stages and comes out cleaner. (b) The stream IntStream.rangeClosed(1, 10).filter(even).map(square).sum() traced stage by stage: 10 items, 5 even numbers, their squares 4, 16, 36, 64, 100 and the total 220."
@ photo id="bca153/filter" cap="Water filter: each stage does one job on what flows through"
fit 1.4
focus 0.5 0.5
@ svg cap="Numbers 1 to 10 through filter, map and sum"
src = list(range(1, 11)); ev = [x for x in src if x % 2 == 0]; sq = [x * x for x in ev]; tot = sum(sq)
assert ev == [2, 4, 6, 8, 10] and sq == [4, 16, 36, 64, 100] and tot == 220
f = Fig(400, 250)
f.text(200, 16, "IntStream.rangeClosed(1, 10)", size=11, color=NAVY, bold=True)
stages = [("source", src, BLUE, NAVY), ("filter(x -> x % 2 == 0)", ev, MINT, TEAL), ("map(x -> x * x)", sq, SAND, AMBER)]
for i, (nm, d, fl, st) in enumerate(stages):
    y = 28 + i * 58
    f.text(8, y + 6, f"{nm}: {len(d)} items", size=10.5, color=st, bold=True, anchor="start")
    for j, v in enumerate(d): f.box(8 + j * 38.5, y + 14, 36, 24, str(v), fill=fl, stroke=st, color=st, size=10.5, bold=True)
    if i < 2: f.arrow([(200, y + 40), (200, y + 56)], color=SLATE, sw=1.4)
f.box(8, 204, 384, 38, "", fill=ROSE, stroke=RED, r=4)
f.text(200, 223, "sum()  ->  4 + 16 + 36 + 64 + 100 = 220", size=12, color=RED, bold=True)
```

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

## 5.8 Iterators, ordering and the `Collections` utilities

### The Iterator pattern

Every `Collection` is `Iterable`, which means it can produce an **`Iterator`**, an object that walks through the elements one by one without exposing how they are stored. The enhanced `for` loop is just shorthand for an iterator loop. The interface has three methods: `hasNext()`, `next()` and the optional `remove()`, which deletes the element *most recently returned* by `next()`. A **`ListIterator`** (lists only) can also move backwards (`hasPrevious()`, `previous()`), replace (`set`) and insert (`add`).

**Fail-fast behaviour.** An `ArrayList` counts its structural changes in a field `modCount`. An iterator remembers the value when it was created and compares it on every `next()`; if the list was changed by anything other than the iterator itself, it throws `ConcurrentModificationException`. The check is a *bug detector*, not a thread-safety guarantee.

```java
import java.util.*;
public class IterDemo {
    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 4, 5, 6));
        Iterator<Integer> it = nums.iterator();
        while (it.hasNext()) {
            if (it.next() % 2 == 0) it.remove();
        }
        System.out.println(nums);
        try {
            for (Integer n : nums) if (n == 1) nums.remove(n);
        } catch (ConcurrentModificationException e) {
            System.out.println("fail-fast: " + e.getClass().getSimpleName());
        }
        List<Integer> three = new ArrayList<>(List.of(1, 2, 3));
        for (Integer n : three) if (n == 2) three.remove(n);
        System.out.println("no exception for the second last element: " + three);
        List<String> names = new ArrayList<>(List.of("sita", "ram", "hari"));
        ListIterator<String> li = names.listIterator();
        while (li.hasNext()) {
            String s = li.next();
            li.set(s.toUpperCase());
            if (s.equals("ram")) li.add("LAXMAN");
        }
        StringBuilder back = new StringBuilder();
        while (li.hasPrevious()) back.append(li.previous()).append(' ');
        System.out.println(names + " | backwards: " + back.toString().trim());
        nums.removeIf(x -> x > 3);
        System.out.println(nums);
    }
}
```

```output
[1, 3, 5]
fail-fast: ConcurrentModificationException
no exception for the second last element: [1, 3]
[SITA, RAM, LAXMAN, HARI] | backwards: HARI LAXMAN RAM SITA
[3]
```

Look at the third experiment: removing the *second-last* element of a three-element list ends the loop silently, because after the removal `hasNext()` compares the cursor (2) with the new size (2) and returns `false` before `next()` can run the check. It is an old quirk that examiners love; the lesson is the same as before: never modify a collection inside an enhanced `for`; use `Iterator.remove()` or `removeIf`.

### Ordering: `Comparable` and `Comparator`

`TreeSet`, `TreeMap`, `PriorityQueue` and `Collections.sort` need to know which of two objects comes first.

| | `Comparable<T>` | `Comparator<T>` |
|---|---|---|
| Package | `java.lang` | `java.util` |
| Method | `int compareTo(T other)` | `int compare(T a, T b)` |
| Where it lives | inside the class itself | in a separate object or lambda |
| Number of orders | one **natural** order | as many as you like |
| Use when | the class has an obvious order (`roll`, `String`, dates) | you need other orders, or cannot modify the class |

Both return a negative number if the first operand comes first, zero if equal, positive otherwise. Always write them with `Integer.compare(a, b)`, `Double.compare` or `String.compareTo`; the shortcut `return a - b;` **overflows** for large values and gives wrong answers. `Comparator` has combinators: `comparingInt(...)`, `.reversed()`, `.thenComparing(...)`, `nullsFirst(...)`.

```java
import java.util.*;
public class Order {
    static class Student implements Comparable<Student> {
        final String name; final int roll; final double gpa;
        Student(String n, int r, double g) { name = n; roll = r; gpa = g; }
        public int compareTo(Student o) { return Integer.compare(roll, o.roll); }
        public String toString() { return name + "#" + roll; }
    }
    public static void main(String[] args) {
        List<Student> l = new ArrayList<>(List.of(new Student("Sita", 3, 3.6), new Student("Ram", 1, 3.2),
                new Student("Hari", 2, 3.6), new Student("Gita", 4, 3.9)));
        Collections.sort(l);
        System.out.println("natural (roll): " + l);
        l.sort(Comparator.comparingDouble((Student s) -> s.gpa).reversed().thenComparing(s -> s.name));
        System.out.println("gpa desc, name: " + l);
        l.sort(Comparator.comparing((Student s) -> s.name.length()).thenComparing(Comparator.reverseOrder()));
        System.out.println("name length, then reverse natural: " + l);
        TreeSet<Student> set = new TreeSet<>(l);
        System.out.println(set.first() + " " + set.last() + " " + set.higher(l.get(0)));
        System.out.println(Integer.MAX_VALUE - (-5) < 0);
        PriorityQueue<String> pq = new PriorityQueue<>(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));
        pq.addAll(List.of("pear", "fig", "banana", "kiwi", "apple"));
        StringBuilder sb = new StringBuilder();
        while (!pq.isEmpty()) sb.append(pq.poll()).append(' ');
        System.out.println(sb.toString().trim());
    }
}
```
```output
natural (roll): [Ram#1, Hari#2, Sita#3, Gita#4]
gpa desc, name: [Gita#4, Hari#2, Sita#3, Ram#1]
name length, then reverse natural: [Ram#1, Gita#4, Sita#3, Hari#2]
Ram#1 Gita#4 Hari#2
true
fig kiwi pear apple banana
```

The line that prints `true` demonstrates the subtraction trap: `Integer.MAX_VALUE - (-5)` wraps around to a negative number, so a comparator written as `a - b` would claim that a large positive value is *smaller* than −5. Note also that a `PriorityQueue` iterates in heap order, not sorted order, so you must `poll()` repeatedly to get sorted output, as above.

### Useful `Map` and `Collections` methods

```java
import java.util.*;
public class CacheDemo {
    static class Lru<K, V> extends LinkedHashMap<K, V> {
        private final int cap;
        Lru(int cap) { super(16, 0.75f, true); this.cap = cap; }
        protected boolean removeEldestEntry(Map.Entry<K, V> e) { return size() > cap; }
    }
    public static void main(String[] args) {
        Lru<String, Integer> c = new Lru<>(3);
        c.put("a", 1); c.put("b", 2); c.put("c", 3);
        c.get("a");
        c.put("d", 4);
        System.out.println("LRU keys: " + c.keySet());
        Map<Character, List<String>> byInitial = new TreeMap<>();
        for (String w : List.of("nepal", "india", "norway", "iran", "peru"))
            byInitial.computeIfAbsent(w.charAt(0), k -> new ArrayList<>()).add(w);
        System.out.println(byInitial);
        Map<String, Integer> stock = new HashMap<>();
        System.out.println(stock.getOrDefault("pen", 0));
        stock.merge("pen", 5, Integer::sum); stock.merge("pen", 3, Integer::sum);
        System.out.println(stock);
        List<Integer> v = new ArrayList<>(List.of(4, 1, 3, 1, 5));
        Collections.sort(v);
        System.out.println(v + " idx(4)=" + Collections.binarySearch(v, 4) + " freq(1)=" + Collections.frequency(v, 1)
                + " max=" + Collections.max(v) + " min=" + Collections.min(v));
        Collections.reverse(v); Collections.swap(v, 0, 4);
        System.out.println(v);
        List<Integer> ro = Collections.unmodifiableList(v);
        try { ro.add(9); } catch (UnsupportedOperationException e) { System.out.println("read-only view"); }
        v.add(9);
        System.out.println(ro.size());
    }
}
```
```output
LRU keys: [c, a, d]
{i=[india, iran], n=[nepal, norway], p=[peru]}
0
{pen=8}
[1, 1, 3, 4, 5] idx(4)=3 freq(1)=2 max=5 min=1
[1, 4, 3, 1, 5]
read-only view
6
```

The `Lru` class is a complete **least-recently-used cache** in eight lines: the third constructor argument `true` makes the map reorder entries on every `get`, and `removeEldestEntry` evicts the oldest entry when the size exceeds the capacity. After `get("a")` the order is `b, c, a`; inserting `d` pushes out `b`, leaving `c, a, d`. Last two lines: `unmodifiableList` is a **view**, not a copy, so it blocks writes through the view while later changes to the original (`v.add(9)`) are visible through it (size 6). Use `List.copyOf(v)` for a true immutable copy. For multi-threaded code use `Collections.synchronizedList(...)` or, better, `ConcurrentHashMap` and `CopyOnWriteArrayList`.

## 5.9 File handling in depth

Unit 5.5 introduced the two stream families. This section completes the picture the TU course asks for: the `File` class, byte-stream copying, character streams, data streams, random access and object serialization, each shown on a real file.

```svgfig label="5.3" caption="The java.io stream families. Byte streams (green) move raw bytes; character streams (amber) add character encoding. Decorators such as BufferedReader and DataInputStream wrap another stream, while InputStreamReader is the bridge from bytes to characters."
f = Fig(640, 300)
f.text(150, 16, "Bytes", size=12, color=TEAL, bold=True)
f.text(490, 16, "Characters", size=12, color=AMBER, bold=True)
f.box(80, 28, 140, 30, "InputStream", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(420, 28, 140, 30, "Reader", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(10, 100, 130, 40, "FileInputStream", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(160, 100, 130, 40, "DataInputStream\nObjectInputStream", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=9.5, bold=True)
f.box(340, 100, 130, 40, "InputStreamReader\n(bytes to chars)", fill="#fde68a", stroke=AMBER, color=NAVY, size=9.5, bold=True)
f.box(490, 100, 140, 40, "BufferedReader\nFileReader", fill="#fde68a", stroke=AMBER, color=NAVY, size=9.5, bold=True)
for x in (75, 225):
    f.arrow([(x, 100), (x, 80), (150, 80), (150, 58)], color=SLATE, sw=1.4)
for x in (405, 560):
    f.arrow([(x, 100), (x, 80), (490, 80), (490, 58)], color=SLATE, sw=1.4)
f.box(80, 190, 140, 30, "OutputStream", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(420, 190, 140, 30, "Writer", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(10, 255, 130, 36, "FileOutputStream", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10, bold=True)
f.box(160, 255, 130, 36, "DataOutputStream\nObjectOutputStream", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=9.5, bold=True)
f.box(340, 255, 130, 36, "OutputStreamWriter", fill="#fde68a", stroke=AMBER, color=NAVY, size=9.5, bold=True)
f.box(490, 255, 140, 36, "BufferedWriter\nFileWriter, PrintWriter", fill="#fde68a", stroke=AMBER, color=NAVY, size=9, bold=True)
for x in (75, 225):
    f.arrow([(x, 255), (x, 238), (150, 238), (150, 220)], color=SLATE, sw=1.4)
for x in (405, 560):
    f.arrow([(x, 255), (x, 238), (490, 238), (490, 220)], color=SLATE, sw=1.4)
f.text(320, 160, "each arrow points from a subclass to its superclass", size=10, color=NAVY, bold=True)
```

### The `File` class and byte streams

A `java.io.File` object represents a **path name**, not the file's contents. Creating it does not touch the disk; calling `createNewFile()` does. Useful methods: `exists()`, `isFile()`, `isDirectory()`, `getName()`, `getParent()`, `getAbsolutePath()`, `length()`, `list()` / `listFiles()`, `mkdir()` / `mkdirs()`, `renameTo()`, `delete()`.

A **byte stream** copies raw bytes. `read(byte[] buf)` returns the number of bytes actually read, or **−1 at end of file**; always use that count when writing, because the last block is usually shorter than the buffer. Copying 8 KB at a time is far faster than one byte per call because each call to the operating system is expensive; `BufferedInputStream` does this blocking for you.

```java
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
public class FileLab1 {
    public static void main(String[] args) throws IOException {
        File dir = Files.createTempDirectory("neb153").toFile();
        File src = new File(dir, "data.bin");
        System.out.println(src.exists() + " " + src.createNewFile() + " " + src.exists() + " " + src.length());
        try (FileOutputStream out = new FileOutputStream(src)) {
            for (int i = 0; i < 1000; i++) out.write(i % 256);
        }
        File copy = new File(dir, "copy.bin");
        int total = 0, calls = 0;
        try (InputStream in = new FileInputStream(src); OutputStream out = new FileOutputStream(copy)) {
            byte[] buf = new byte[400];
            int n;
            while ((n = in.read(buf)) != -1) { out.write(buf, 0, n); total += n; calls++; }
        }
        System.out.println(total + " bytes in " + calls + " reads; equal: " + Arrays.equals(Files.readAllBytes(src.toPath()), Files.readAllBytes(copy.toPath())));
        File txt = new File(dir, "marks.txt");
        try (BufferedWriter w = new BufferedWriter(new FileWriter(txt, StandardCharsets.UTF_8))) {
            w.write("Sita 82"); w.newLine(); w.write("Ram 67"); w.newLine(); w.write("नमस्ते 100"); w.newLine();
        }
        int sum = 0;
        try (BufferedReader r = new BufferedReader(new FileReader(txt, StandardCharsets.UTF_8))) {
            String line;
            while ((line = r.readLine()) != null) {
                String[] p = line.split(" ");
                sum += Integer.parseInt(p[1]);
                System.out.println(p[0].length() + " chars: " + p[0]);
            }
        }
        System.out.println("sum = " + sum + ", size in bytes = " + txt.length());
        try (Scanner sc = new Scanner(txt, StandardCharsets.UTF_8)) {
            int words = 0;
            while (sc.hasNext()) { sc.next(); words++; }
            System.out.println("tokens: " + words);
        }
        String[] names = dir.list();
        Arrays.sort(names);
        System.out.println(Arrays.toString(names) + " dir=" + dir.isDirectory());
        for (File f : dir.listFiles()) f.delete();
        System.out.println(dir.delete() + " " + dir.exists());
        try (FileReader fr = new FileReader("no_such_file.txt")) {
        } catch (FileNotFoundException e) {
            System.out.println("FileNotFoundException handled");
        }
    }
}
```
```output
false true true 0
1000 bytes in 3 reads; equal: true
4 chars: Sita
3 chars: Ram
6 chars: नमस्ते
sum = 249, size in bytes = 38
tokens: 6
[copy.bin, data.bin, marks.txt] dir=true
true false
FileNotFoundException handled
```

The 1000 bytes are read in blocks of 400, 400 and 200, which is **3 reads**; the loop uses `n`, not `buf.length`, when it writes, so the copy is exactly 1000 bytes. The Devanagari word has 6 characters (four consonants न म स त, the virama ् and the vowel sign े, six code points) but occupies **18 bytes** in UTF-8, three bytes per character, which is why `txt.length()` returns bytes, not characters. Count the file: `Sita 82` plus newline is 8 bytes, `Ram 67` plus newline is 7 bytes, and `नमस्ते 100` plus newline is 18 + 1 + 3 + 1 = 23 bytes, so the size is **38 bytes** and the three numbers sum to 82 + 67 + 100 = 249. Always name the charset (`StandardCharsets.UTF_8`) in `FileReader`, `FileWriter` and `Scanner`; otherwise the platform default is used and Nepali text may be damaged on another computer.

### Data streams, random access and serialization

**`DataOutputStream` / `DataInputStream`** write Java primitives in a fixed binary format (`writeInt` = 4 bytes, `writeDouble` = 8, `writeUTF` = a 2-byte length plus modified UTF-8). Data must be read back in the **same order and types** it was written.

**`RandomAccessFile`** treats a file as a large byte array with a **file pointer**: `seek(pos)` moves it, `getFilePointer()` reports it, `read…`/`write…` act at the pointer and advance it. If every record has a fixed size, record *i* starts at byte `i × recordSize`, so any record can be read or updated in O(1) without touching the others. This is how simple database files work.

```svgfig label="5.4" caption="A RandomAccessFile of fixed 12-byte records (int id, double mark). The byte offset of record i (counting from 0) is 12 * i; the mark field starts 4 bytes later. seek() jumps straight there, so one record is updated without reading or rewriting the rest."
f = Fig(640, 200)
for i in range(3):
    x = 40 + i * 180
    f.box(x, 60, 60, 40, "int id", fill=BLUE, color=NAVY, size=11, bold=True)
    f.box(x + 60, 60, 120, 40, "double mark", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
    f.text(x + 90, 50, "record %d" % i, size=10.5, color=NAVY, bold=True)
    f.text(x, 118, "byte %d" % (12 * i), size=10, color=SLATE, bold=True, anchor="start")
f.text(580, 118, "end: byte 36", size=10, color=SLATE, bold=True, anchor="end")
f.arrow([(160, 170), (160, 104)], color=RED, sw=2)
f.text(160, 186, "seek(12 * 1 + 4) = byte 16: mark of record 1", size=11, color=RED, bold=True)
f.text(320, 22, "file length = 3 * 12 = 36 bytes", size=11.5, color=NAVY, bold=True)
```

```java
import java.io.*;
import java.nio.file.*;
public class FileLab2 {
    static class Account implements Serializable {
        private static final long serialVersionUID = 1L;
        String owner; double balance; transient String pin;
        Account(String o, double b, String p) { owner = o; balance = b; pin = p; }
    }
    public static void main(String[] args) throws Exception {
        Path dir = Files.createTempDirectory("neb153b");
        File data = dir.resolve("rec.dat").toFile();
        try (DataOutputStream out = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(data)))) {
            out.writeInt(7); out.writeDouble(2.5); out.writeUTF("Pokhara"); out.writeBoolean(true);
        }
        try (DataInputStream in = new DataInputStream(new BufferedInputStream(new FileInputStream(data)))) {
            System.out.println(in.readInt() + " " + in.readDouble() + " " + in.readUTF() + " " + in.readBoolean());
        }
        System.out.println("size = " + data.length());
        File recs = dir.resolve("marks.dat").toFile();
        try (RandomAccessFile raf = new RandomAccessFile(recs, "rw")) {
            for (int i = 1; i <= 3; i++) { raf.writeInt(i); raf.writeDouble(50.0 + 10 * i); }
            System.out.println("length = " + raf.length() + ", pointer = " + raf.getFilePointer());
            raf.seek(12L * 1 + 4);
            System.out.println("record 2 mark = " + raf.readDouble());
            raf.seek(12L * 1 + 4);
            raf.writeDouble(99.5);
            raf.seek(12L * 2);
            System.out.println("record 3: " + raf.readInt() + " " + raf.readDouble());
            raf.seek(12L * 1);
            System.out.println("record 2 now: " + raf.readInt() + " " + raf.readDouble());
        }
        File ser = dir.resolve("acct.ser").toFile();
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(ser))) {
            oos.writeObject(new Account("Sita", 1250.75, "4321"));
        }
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(ser))) {
            Account a = (Account) ois.readObject();
            System.out.println(a.owner + " " + a.balance + " pin=" + a.pin);
        }
        try (var walk = Files.walk(dir)) {
            System.out.println(walk.filter(Files::isRegularFile).count() + " files under the folder");
        }
        try (var walk = Files.walk(dir)) {
            walk.sorted(java.util.Comparator.reverseOrder()).map(Path::toFile).forEach(File::delete);
        }
        System.out.println(Files.exists(dir));
    }
}
```
```output
7 2.5 Pokhara true
size = 22
length = 36, pointer = 36
record 2 mark = 70.0
record 3: 3 80.0
record 2 now: 2 99.5
Sita 1250.75 pin=null
3 files under the folder
false
```

The first record file holds 4 + 8 + (2 + 7) + 1 = **22 bytes** (`writeUTF` stores a two-byte length then the seven bytes of "Pokhara"). The marks file has 3 records of 12 bytes (an `int` of 4 and a `double` of 8) = **36 bytes**, and after writing the file pointer is at the end, 36. Record 2 starts at byte 12; its mark is 4 bytes further on (`12 × 1 + 4`), which is how the program updates **only** that field to 99.5 without rewriting the file. The serialized `Account` comes back with its `owner` and `balance` but `pin=null`, because a **`transient`** field is skipped; that is the correct way to keep passwords out of saved objects. `serialVersionUID` identifies the class version: if the class changes and the number does not match, `readObject` throws `InvalidClassException`.

::: caution Serialization safety
Reading a serialized stream from an untrusted source can run attacker-chosen code (a long list of real-world vulnerabilities began this way). Use it only for your own files, prefer JSON for exchange, and consider `ObjectInputFilter` to whitelist classes.
:::

| Need | Best tool |
|---|---|
| Copy or read a whole small file | `Files.readAllBytes`, `Files.readString`, `Files.copy` |
| Read a text file line by line | `BufferedReader` or `Files.lines` |
| Write text with formatting | `PrintWriter` (`printf`, `println`) |
| Binary primitives in a fixed format | `DataOutputStream` / `DataInputStream` |
| Update one record in a big file | `RandomAccessFile` with fixed-size records |
| Save an object graph (your own use) | `ObjectOutputStream` with `Serializable` |
| Exchange data with other systems | JSON (Jackson, Gson), CSV, XML |

**Exceptions in file code.** Almost every I/O call declares the checked `IOException`; its subclasses `FileNotFoundException`, `EOFException` (reading past the end with a data stream) and `NoSuchFileException` (the `Files` API) let you respond precisely. Always use **try-with-resources** so that the file is closed even when an exception occurs, and so that data buffered in a writer is flushed by `close()`.

## Formula and fact sheet

- Generics: compile-time safety, erased at run time; `<T extends X>` bounded; PECS wildcards.
- ArrayList (index O(1)), HashMap/HashSet (O(1) average), TreeMap/TreeSet (O(log n), sorted), ArrayDeque (stack/queue), PriorityQueue (heap).
- Lambda = implementation of a functional interface; variables captured must be effectively final.
- Stream: source → lazy intermediate ops → one terminal op; the source is unchanged.
- Use `java.nio.file.Files`, try-with-resources, explicit UTF-8.
- `Serializable` + `transient`; avoid deserialising untrusted data.
- `Iterator.remove()` and `removeIf` are the safe ways to delete while looping; the enhanced `for` with `list.remove` throws `ConcurrentModificationException` (except when removing the second-last element).
- `Comparable.compareTo` = natural order inside the class; `Comparator.compare` = any other order; never compare with `a - b` (overflow); use `Integer.compare`.
- `LinkedHashMap(16, 0.75f, true)` + `removeEldestEntry` = LRU cache. `computeIfAbsent`, `merge`, `getOrDefault` replace most `if (containsKey)` code.
- File I/O: `read(buf)` returns -1 at end; `RandomAccessFile` record *i* starts at `i * size`; `transient` fields are not serialized; name the charset (UTF-8); `File.length()` is in bytes.

## Chapter summary

- Generics make collections type-safe, and the framework offers the right structure for each access pattern.
- Choosing between list, set, map, queue and their implementations is a question of ordering, uniqueness and cost.
- Lambdas and streams express filter-map-reduce logic concisely and safely.
- File I/O is done with buffered, closed-after-use readers and writers or the `Files` helpers.
- Iterators, comparators and the `Collections` helpers give precise control over traversal and ordering.
- The `File` class, byte and character streams, data streams, `RandomAccessFile` and serialization cover all the file-handling questions in the syllabus.

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
11. Explain `ConcurrentModificationException` and show two correct ways to remove all even numbers from a list.
12. Differentiate `Comparable` and `Comparator` in a table. Sort a `List<Student>` by marks descending, then name ascending.
13. Why is `return a - b;` a wrong comparator? Give integers that break it.
14. Write a program that copies a binary file with a 4 KB buffer and reports the number of bytes copied.
15. A file holds fixed 12-byte records (`int id`, `double mark`). Show how to update the mark of record number 7 (counting from 1) with `RandomAccessFile`.
16. What does `transient` do? What happens to it after `readObject`? Why must you never deserialize untrusted data?
17. A file contains the text `नेपाल` (5 characters). Why may `File.length()` return 15 and how do you read it correctly?

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
**11.** The list's iterator detects that the list was changed behind its back (`modCount` differs) and throws on the next `next()`. Correct: `Iterator<Integer> it = list.iterator(); while (it.hasNext()) if (it.next() % 2 == 0) it.remove();` or `list.removeIf(x -> x % 2 == 0);`.
**12.** `Comparable` is in `java.lang`, defines `compareTo` inside the class and gives one natural order; `Comparator` is in `java.util`, defines `compare` in a separate object and gives any number of orders. Code: `list.sort(Comparator.comparingInt((Student s) -> s.marks).reversed().thenComparing(s -> s.name));`.
**13.** The difference can overflow `int`: `Integer.MAX_VALUE - (-5)` wraps to a negative number, so the comparator says the big value is smaller. Use `Integer.compare(a, b)`.
**14.** `try (InputStream in = new FileInputStream(src); OutputStream out = new FileOutputStream(dst)) { byte[] buf = new byte[4096]; int n; long total = 0; while ((n = in.read(buf)) != -1) { out.write(buf, 0, n); total += n; } System.out.println(total); }`. Write `n` bytes, not `buf.length`.
**15.** Record 7 starts at `(7 - 1) * 12 = 72`; its mark is 4 bytes later: `raf.seek(76); raf.writeDouble(newMark);` inside `try (RandomAccessFile raf = new RandomAccessFile(file, "rw"))`.
**16.** `transient` excludes a field from serialization (use it for passwords and caches). After `readObject` the field has its default value (`null`, `0`). A crafted stream can instantiate arbitrary classes and trigger harmful code during deserialization.
**17.** Devanagari characters take 3 bytes each in UTF-8, so 5 characters are 15 bytes. Read with an explicit charset: `Files.readString(path, StandardCharsets.UTF_8)` or `new BufferedReader(new FileReader(f, StandardCharsets.UTF_8))`.
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

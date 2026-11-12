---
subject: Advanced Java Programming
grade: BCA Semester 5
unit: 1
title: Foundations for Advanced Java: Threads, I/O and Serialization
hours: 6
area: BCA 303 · Advanced Java Programming · Unit 1
---

You already know how to write a Java class (OOP in Java, Semester II). Everything in this book (windows that stay responsive while a download runs, a database server answering ten clients, a servlet container handling hundreds of requests) rests on three ideas you must be able to use fluently: **doing several things at once** (threads), **moving data in and out of programs** (streams) and **turning an object into bytes and back** (serialization). Every program in this book was compiled with a real JDK (OpenJDK 17) and run; the output you see is the output that came out.

::: key What this unit gives you
- Threads: creating, life cycle, synchronisation, thread pools and futures.
- Streams and files: byte and character streams, try-with-resources, `java.nio.file`.
- Object serialization: `Serializable`, `transient`, `serialVersionUID`.
- How the rest of the book fits together (the Java platform map).
:::

## 1.1 The map of the Java platform

| Edition | What it is | In this book |
|---|---|---|
| Java SE | the language and core libraries: collections, I/O, threads, networking, Swing, JDBC, RMI | Units 1–5 and 7 |
| Jakarta EE (formerly Java EE) | enterprise APIs: Servlets, JSP, JSF, EJB, JPA, JMS | Unit 6 |
| Java ME / Android | small devices | not covered |

The rest of the units: Unit 2 builds graphical interfaces with Swing and event handling; Unit 3 talks to databases with JDBC; Unit 4 does network programming with sockets and HTTP; Unit 5 calls objects on other machines with RMI (and explains CORBA); Unit 6 writes server-side web components (servlets and JSP); Unit 7 packages reusable components as JavaBeans.

::: caution Namespace change
Since Jakarta EE 9 (2020) the enterprise packages moved from `javax.servlet` to `jakarta.servlet`. Older textbooks, Tomcat 9 and below, and this book's compiled examples (servlet API 4.0) use `javax.servlet`; Tomcat 10 and above expects `jakarta.servlet`. The code is otherwise identical.
:::

## 1.2 Multithreading

A **thread** is an independent path of execution inside a process; threads of one process share its memory. A GUI uses one thread to draw windows and others to do work; a server uses one per client or a pool. **Multitasking** among processes is managed by the operating system; **multithreading** is cheaper because threads share heap memory (and therefore need care).

### Creating threads

1. Extend `Thread` and override `run()`.
2. Implement `Runnable` and pass it to `new Thread(runnable)` (preferred: the class remains free to extend something else; a lambda works because `Runnable` has one method).
3. Submit a `Runnable` or `Callable` to an `ExecutorService` (preferred in real programs).

`start()` creates the new thread and calls `run()` in it; calling `run()` directly merely calls a method in the current thread.

### Life cycle

A thread is **new** (created), **runnable** (after `start()`, ready or running), **blocked** (waiting for a monitor lock), **waiting** or **timed waiting** (`wait()`, `join()`, `sleep(ms)`) and **terminated** (when `run()` ends). `join()` makes the caller wait until another thread finishes; `sleep` pauses the current thread; `interrupt()` politely asks a thread to stop. Priorities (1–10) are hints only. **Daemon** threads do not keep the JVM alive.

### Synchronisation

Two threads executing `count++` can both read the same value and both write back value + 1, losing an update: a **race condition**. The increment is really three steps (read, add, write). Remedies:

- **`synchronized`** methods or blocks acquire the **monitor lock** of an object; only one thread at a time may hold it. Entering a synchronised region also makes earlier writes visible (memory visibility).
- **`volatile`** guarantees visibility of one variable but not atomicity of compound actions.
- **`java.util.concurrent.atomic`** classes (`AtomicInteger`) do lock-free atomic updates; **`ReentrantLock`** gives explicit locking with `tryLock`.
- **`wait()`/`notify()`/`notifyAll()`** (inside synchronized code) let threads cooperate, as in the producer–consumer pattern.

**Deadlock** occurs when threads wait for locks in a circle (thread 1 holds A and wants B while thread 2 holds B and wants A). Avoid it by always acquiring locks in the same global order.

### Executors and futures

Creating a thread per task is wasteful. An **`ExecutorService`** keeps a **pool** of worker threads that run submitted tasks; a **`Callable<V>`** returns a result, delivered through a **`Future<V>`** whose `get()` waits for it.

```java
import java.util.concurrent.*;
import java.util.*;
public class ThreadDemo {
    static int safe = 0; static final Object lock = new Object();
    public static void main(String[] args) throws Exception {
        Thread[] ts = new Thread[4];
        for (int i = 0; i < ts.length; i++) {
            ts[i] = new Thread(() -> { for (int k = 0; k < 50_000; k++) { synchronized (lock) { safe++; } } }, "worker-" + i);
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        System.out.println("synchronized counter = " + safe);
        ExecutorService pool = Executors.newFixedThreadPool(3);
        List<Future<Long>> fs = new ArrayList<>();
        for (int n = 1; n <= 5; n++) {
            final int m = n;
            fs.add(pool.submit(() -> { long s = 0; for (long j = 1; j <= m * 1000L; j++) s += j * j; return s; }));
        }
        for (int i = 0; i < fs.size(); i++) System.out.println("sum of squares up to " + (i + 1) * 1000 + " = " + fs.get(i).get());
        pool.shutdown();
        System.out.println("terminated: " + pool.awaitTermination(1, TimeUnit.SECONDS));
    }
}
```
```output
synchronized counter = 200000
sum of squares up to 1000 = 333833500
sum of squares up to 2000 = 2668667000
sum of squares up to 3000 = 9004500500
sum of squares up to 4000 = 21341334000
sum of squares up to 5000 = 41679167500
terminated: true
```
Four threads each add 1 fifty thousand times, so the total is exactly 200,000 only because of the `synchronized` block; without it the result would usually be smaller and different on each run. The five tasks run concurrently, but the futures are read in submission order so the output is deterministic.

## 1.3 Streams and files

Java I/O is built from **streams**: a sequence of data flowing from a source or to a destination.

| | Bytes | Characters |
|---|---|---|
| Input | `InputStream` (`FileInputStream`, `ByteArrayInputStream`) | `Reader` (`FileReader`, `InputStreamReader`) |
| Output | `OutputStream` (`FileOutputStream`) | `Writer` (`FileWriter`, `PrintWriter`) |
| Buffered | `BufferedInputStream` | `BufferedReader`, `BufferedWriter` |
| Objects | `ObjectInputStream`, `ObjectOutputStream` | n/a |

Wrapping one stream in another (a **decorator**) adds capabilities: `new BufferedReader(new InputStreamReader(socket.getInputStream()))` reads text lines from a network socket. Always close streams; the **try-with-resources** statement closes anything that implements `AutoCloseable` even when an exception occurs. The modern `java.nio.file` API (`Files`, `Path`) does common tasks in one call: `Files.readAllLines`, `Files.write`, `Files.walk`.

```java
import java.io.*;
import java.nio.file.*;
import java.util.*;
public class FileDemo {
    public static void main(String[] args) throws IOException {
        Path p = Files.createTempFile("nebians", ".txt");
        Files.write(p, Arrays.asList("Advanced Java", "JDBC and Servlets", "RMI"));
        try (BufferedReader br = Files.newBufferedReader(p)) {
            String line; int lines = 0, words = 0;
            while ((line = br.readLine()) != null) { lines++; words += line.split("\\s+").length; }
            System.out.println(lines + " lines, " + words + " words");
        }
        try (PrintWriter pw = new PrintWriter(new FileWriter(p.toFile(), true))) { pw.println("appended line"); }
        System.out.println("now " + Files.readAllLines(p).size() + " lines, last = " + Files.readAllLines(p).get(3));
        System.out.println("size in bytes: " + Files.size(p));
        Files.delete(p);
        System.out.println("exists after delete: " + Files.exists(p));
    }
}
```
```output
3 lines, 6 words
now 4 lines, last = appended line
size in bytes: 50
exists after delete: false
```
## 1.4 Object serialization

**Serialization** converts an object (and everything reachable from it) to a byte stream; **deserialization** rebuilds an equal object. It is how objects are saved to disk, sent over sockets and passed between machines in RMI (Unit 5).

- The class must implement the marker interface **`java.io.Serializable`**; all its non-transient field types must be serializable too, otherwise `NotSerializableException`.
- Fields marked **`transient`** are skipped and come back as defaults (null, 0): use it for passwords, caches and handles such as open files.
- **`static`** fields belong to the class, not the object, and are not serialized.
- **`serialVersionUID`** identifies the class version; if the sender's and receiver's UIDs differ, deserialization throws `InvalidClassException`. Declare it explicitly.
- A subclass of a non-serializable class needs the superclass to have a no-argument constructor, which is run on deserialization.
- `writeObject`/`readObject` private methods customise the format; `Externalizable` gives full control.

```java
import java.io.*;
public class SerialDemo {
    static class Student implements Serializable {
        private static final long serialVersionUID = 1L;
        String name; int roll; transient String password;
        Student(String n, int r, String p) { name = n; roll = r; password = p; }
        public String toString() { return name + " #" + roll + " password=" + password; }
    }
    public static void main(String[] args) throws Exception {
        Student s = new Student("Sita", 7, "secret");
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        try (ObjectOutputStream out = new ObjectOutputStream(bos)) { out.writeObject(s); }
        System.out.println("before: " + s);
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bos.toByteArray()))) {
            Student t = (Student) in.readObject();
            System.out.println("after : " + t);
        }
        System.out.println("bytes produced: " + (bos.size() > 0));
    }
}
```
```output
before: Sita #7 password=secret
after : Sita #7 password=null
bytes produced: true
```
The `transient` password is gone after the round trip. Serialization is also a security risk: never deserialize untrusted data (it can run attacker-chosen code), and prefer JSON for public interfaces.

## 1.5 Collections and generics in a line

Servlets, JDBC and GUI code all pass around `List`, `Map` and `Set`. Remember the rules: `ArrayList` (fast random access), `LinkedList` (fast insertion at the ends), `HashMap` (key → value, no order), `TreeMap` (sorted keys), `HashSet`; use the generic form (`List<String>`) so the compiler checks types and no casts are needed; `Collections.synchronizedList` or `ConcurrentHashMap` when threads share a collection.

## 1.6 Seeing the ideas: threads, streams and serialization

Concurrency is easier to understand when you can watch it. Plate 1.1 shows the people, the place and the processor behind it. Figure 1.1 maps the Java platform. Figures 1.2 to 1.7 follow a thread from birth to death, show a lost update, a deadlock, the dining philosophers, a bounded buffer and a thread pool, and Plate 1.2 gives an everyday picture for each. Figures 1.8 to 1.11 do the same for streams, character sets and serialization. Every program behind a number was compiled with OpenJDK 17 and run, and the figure code re-checks the arithmetic.

```photogrid label="1.1" cols="4" ratio="1.0" caption="People, place and hardware behind Java threads. (a) James Gosling (CC BY-SA 4.0), who led the team at Sun Microsystems that created Java, released in 1995. (b) A building on the Sun Microsystems campus in Santa Clara (CC BY-SA 3.0); Oracle bought Sun in 2010. (c) A photograph of a Skylake processor die (CC0): a modern processor holds several cores, and each core runs one thread at a time, or two with hyper-threading, so the operating system shares a few cores among hundreds of threads. (d) Edsger Dijkstra at a lecture in 1994 (CC BY-SA 4.0), who introduced the semaphore and posed the dining philosophers problem in 1965."
@ photo id="bca303/gosling" cap="James Gosling, Java's lead designer"
fit 1.0
focus 0.5 0.6
@ photo id="bca303/sunhq" cap="Sun Microsystems campus"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/skylake" cap="Processor die: several cores"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/dijkstra" cap="Dijkstra: semaphores, philosophers"
fit 1.0
focus 0.6 0.5
```

```svgfig label="1.1" caption="The Java platform. The JDK holds the developer tools such as javac; inside it the JRE holds the JVM and the class libraries; Java SE is covered in Units 1 to 5 and 7 and Jakarta EE in Unit 6. A source file is compiled once to bytecode and the same .class file runs on any system that has a JVM."
f = Fig(580, 270)
f.text(290, 14, "from source file to running program: the JDK, the JRE and the JVM", size=11.5, color=NAVY, bold=True)
f.box(6, 30, 568, 128, "", fill=SOFT, stroke="#94a3b8", dash=True)
f.text(16, 44, "JDK: tools for developers (javac, jar, javadoc, jshell)", size=10, color=SLATE, bold=True, anchor="start")
f.box(16, 54, 380, 96, "", fill=BLUE, stroke=NAVY)
f.text(26, 68, "JRE: what a user needs to run Java", size=10, color=NAVY, bold=True, anchor="start")
f.box(26, 78, 160, 64, "JVM\nclass loader, bytecode\nverifier, JIT, GC", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(200, 78, 186, 64, "class libraries\njava.lang, java.util, java.io,\njava.net, java.sql, javax.swing", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(410, 54, 156, 96, "Editions\nJava SE: Units 1-5, 7\nJakarta EE: Unit 6\n(servlets, JSP)", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(6, 190, 110, 36, "Hello.java\nsource text", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.box(160, 190, 110, 36, "javac\ncompiler", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(314, 190, 110, 36, "Hello.class\nbytecode", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(468, 190, 106, 36, "JVM\nruns it", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
for x in (116, 270, 424):
    f.arrow([(x, 208), (x + 44, 208)], color=SLATE)
f.text(290, 250, "the same .class file runs on Windows, Linux or macOS: each has its own JVM", size=10, color=NAVY, bold=True)
```

```svgfig label="1.2" caption="The six values of Thread.State and the moves between them. A new thread becomes RUNNABLE on start(); it can be BLOCKED waiting for a monitor lock, WAITING (wait, join) or TIMED_WAITING (sleep) and returns to RUNNABLE; it ends TERMINATED. A real run of a small program printed NEW, RUNNABLE, WAITING, TIMED_WAITING, WAITING, BLOCKED and TERMINATED, so all six states were observed."
f = Fig(580, 290)
real = ["NEW", "RUNNABLE", "WAITING", "TIMED_WAITING", "WAITING", "BLOCKED", "TERMINATED"]
assert set(real) == {"NEW", "RUNNABLE", "WAITING", "TIMED_WAITING", "BLOCKED", "TERMINATED"}
f.text(290, 14, "the six Thread.State values and the moves between them", size=11.5, color=NAVY, bold=True)
f.box(10, 100, 90, 40, "NEW", fill=SOFT, stroke=SLATE, size=11, bold=True)
f.box(160, 100, 110, 40, "RUNNABLE", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(450, 100, 120, 40, "TERMINATED", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(320, 30, 120, 36, "BLOCKED", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(320, 100, 120, 36, "WAITING", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(320, 170, 120, 36, "TIMED_WAITING", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(100, 120), (160, 120)], color=SLATE, label="start()", lpos=(130, 112))
f.arrow([(270, 106), (320, 44)], color=SLATE); f.arrow([(320, 58), (270, 114)], color=SLATE, dash=True)
f.arrow([(270, 116), (320, 114)], color=SLATE); f.arrow([(320, 128), (270, 128)], color=SLATE, dash=True)
f.arrow([(270, 130), (320, 184)], color=SLATE); f.arrow([(320, 192), (270, 136)], color=SLATE, dash=True)
f.arrow([(270, 140), (330, 238), (510, 238), (510, 140)], color=SLATE, label="run() ends", lpos=(420, 230))
f.text(10, 160, "synchronized block", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(10, 174, "taken by another thread", size=9.5, color=SLATE, anchor="start")
f.text(10, 196, "wait(), join(), park()", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(10, 210, "sleep(ms), wait(ms)", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(290, 262, "a real run printed: " + ", ".join(real[:4]) + ",", size=9.5, color=TEAL, bold=True)
f.text(290, 277, ", ".join(real[4:]) + " (all six states were seen)", size=9.5, color=TEAL, bold=True)
```

```svgfig label="1.3" caption="A race condition. count++ is read, add and write. In the unlucky order T1 and T2 both read 5, both write 6 and one increment is lost (final 6, expected 7); in a one-at-a-time order the result is 7 (both orders computed in the figure). On the right is a real run of two threads adding 1,000,000 times each: the unsynchronized counter ended at 1,985,476 (14,524 increments lost, 0.73 percent), while synchronized and AtomicInteger gave exactly 2,000,000. The bars start at 1,980,000 to show the difference."
f = Fig(580, 276)
def run(order):
    mem = {"count": 5}; reg = {}
    log = []
    for who, op in order:
        if op == "read":
            reg[who] = mem["count"]; log.append("%s reads %d" % (who, reg[who]))
        elif op == "add":
            reg[who] += 1
        else:
            mem["count"] = reg[who]; log.append("%s writes %d" % (who, reg[who]))
    return log, mem["count"]
bad = [("T1", "read"), ("T2", "read"), ("T1", "add"), ("T2", "add"), ("T1", "write"), ("T2", "write")]
good = [("T1", "read"), ("T1", "add"), ("T1", "write"), ("T2", "read"), ("T2", "add"), ("T2", "write")]
lb, fb = run(bad); lg, fg = run(good)
assert fb == 6 and fg == 7
exp, unsync, sync, atom = 2000000, 1985476, 2000000, 2000000
f.text(150, 14, "count++ is three steps (count = 5)", size=11.5, color=NAVY, bold=True)
for k, (title, log, fin, col, fc) in enumerate([("unlucky order", lb, fb, RED, ROSE), ("one thread at a time", lg, fg, TEAL, MINT)]):
    y0 = 28 + k * 110
    f.box(6, y0, 288, 100, "", fill=fc, stroke=col)
    f.text(14, y0 + 13, title, size=10.5, color=col, bold=True, anchor="start")
    for i, s in enumerate(log):
        f.text(14 + (i % 2) * 140, y0 + 32 + (i // 2) * 16, "%d  %s" % (i + 1, s), size=9.5, color=SLATE, anchor="start")
    f.text(14, y0 + 86, "final count = %d, expected 7" % fin, size=10.5, color=col, bold=True, anchor="start")
f.text(436, 14, "a real run, 2 threads x 1,000,000 increments", size=10.5, color=NAVY, bold=True)
base = 1980000
for i, (nm, v, col, fc) in enumerate([("unsynchronized", unsync, RED, ROSE), ("synchronized", sync, TEAL, MINT), ("AtomicInteger", atom, TEAL, MINT)]):
    y = 40 + i * 52
    w = 250 * (v - base) / (exp - base)
    f.text(310, y, nm, size=10, color=col, bold=True, anchor="start")
    f.box(310, y + 8, w, 22, "", fill=fc, stroke=col)
    f.text(316, y + 19, "{:,}".format(v), size=10, color=col, bold=True, anchor="start", vmid=True)
f.text(436, 206, "bars start at 1,980,000, not at 0", size=9.5, color=SLATE)
f.text(436, 222, "unsynchronized lost %s increments (%.2f percent)" % ("{:,}".format(exp - unsync), (exp - unsync) / exp * 100), size=9.5, color=RED, bold=True)
f.text(436, 238, "the loss differs on every run", size=9.5, color=SLATE)
f.text(290, 266, "the two correct versions give exactly 2,000,000 every time", size=10, color=NAVY, bold=True)
```

```photogrid label="1.2" cols="4" ratio="1.0" caption="Everyday pictures of concurrency. (a) Supermarket checkout lanes (CC BY 4.0): each open lane serves one customer at a time like a thread, the customers waiting are tasks in a queue, and the set of lanes is a thread pool. (b) A worker at one machine of a factory line (Library of Congress, public domain): stages of work joined by trays of parts are a producer and consumer with a buffer. (c) Gridlock in New York (CC BY-SA 3.0): every vehicle blocks another and none can move, a circular wait, which is a deadlock. (d) The dining philosophers problem (CC BY-SA 3.0): five philosophers and five forks, each philosopher needs the two forks beside the plate."
@ photo id="bca303/checkout" cap="Checkout lanes: a thread pool"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/assembly" cap="One stage of an assembly line"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/gridlock" cap="Gridlock: circular waiting"
fit 1.0
focus 0.5 0.5
@ photo id="bca303/dining" cap="Dining philosophers"
fit 1.0
focus 0.5 0.5
```

```svgfig label="1.4" caption="Deadlock as a cycle. T1 holds lock A and wants B while T2 holds B and wants A; the figure code finds the cycle T1, B, T2, A, T1 in the wait-for graph. A real run with these two threads ended with both BLOCKED and findDeadlockedThreads reported 2 threads. If both threads take A first and then B, no cycle exists."
f = Fig(580, 232)
def has_cycle(edges):
    g = {}
    for a, b in edges:
        g.setdefault(a, []).append(b)
    def dfs(n, path):
        if n in path:
            return path[path.index(n):] + [n]
        for m in g.get(n, []):
            c = dfs(m, path + [n])
            if c:
                return c
    for n in list(g):
        c = dfs(n, [])
        if c:
            return c
cyc = has_cycle([("T1", "B"), ("B", "T2"), ("T2", "A"), ("A", "T1")])
ordered = has_cycle([("T1", "B"), ("B", "T2")])
assert cyc and cyc[0] == cyc[-1] and ordered is None
f.text(145, 14, "deadlock: a cycle in the wait-for graph", size=11.5, color=NAVY, bold=True)
f.circle(60, 80, 24, fill=BLUE, stroke=NAVY, label="T1", size=11, color=NAVY)
f.circle(230, 80, 24, fill=BLUE, stroke=NAVY, label="T2", size=11, color=NAVY)
f.box(120, 36, 50, 28, "A", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(120, 112, 50, 28, "B", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(80, 66), (120, 50)], color=TEAL, label="holds", lpos=(76, 44), lsize=9)
f.arrow([(170, 50), (210, 66)], color=RED, label="wants", lpos=(196, 44), lsize=9)
f.arrow([(210, 94), (170, 126)], color=TEAL, label="holds", lpos=(204, 126), lsize=9)
f.arrow([(120, 126), (80, 94)], color=RED, label="wants", lpos=(80, 126), lsize=9)
f.text(145, 164, "T1 holds A and wants B; T2 holds B and wants A", size=9.5, color=SLATE)
f.text(145, 182, "cycle found: " + " > ".join(cyc), size=9.5, color=RED, bold=True)
f.text(145, 202, "a real run: 2 threads deadlocked, both BLOCKED,", size=9.5, color=NAVY, bold=True)
f.text(145, 216, "found by ThreadMXBean.findDeadlockedThreads()", size=9.5, color=NAVY, bold=True)
f.text(435, 14, "cure: one global lock order", size=11.5, color=NAVY, bold=True)
f.circle(350, 80, 24, fill=BLUE, stroke=NAVY, label="T1", size=11, color=NAVY)
f.circle(520, 80, 24, fill=BLUE, stroke=NAVY, label="T2", size=11, color=NAVY)
f.box(410, 36, 50, 28, "A", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(410, 112, 50, 28, "B", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(370, 66), (410, 50)], color=TEAL); f.arrow([(460, 50), (500, 66)], color=TEAL, dash=True)
f.arrow([(500, 94), (460, 126)], color=SLATE, dash=True); f.arrow([(410, 126), (370, 94)], color=TEAL)
f.text(435, 164, "both threads take A first, then B:", size=9.5, color=SLATE)
f.text(435, 182, "T2 must wait at A, so no one", size=9.5, color=SLATE)
f.text(435, 196, "holds B while waiting for A", size=9.5, color=SLATE)
f.text(435, 216, "graph without a cycle: %s" % ("none found" if ordered is None else "cycle"), size=9.5, color=TEAL, bold=True)
```

```svgfig label="1.5" caption="The dining philosophers. Each philosopher needs two forks and fork k lies between P(k-1) and Pk. If everyone takes the left fork first, all five wait for the right one in a circle. Taking the lower-numbered fork first changes only P4 (fork 0 before fork 4) and breaks the circle; a real run of the ordered version gave meals = [3, 3, 3, 3, 3]."
f = Fig(580, 290)
cm = __import__("math")
N = 5
order = [(min(i, (i + 1) % N), max(i, (i + 1) % N)) for i in range(N)]
assert order == [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]
naive = [(i, (i + 1) % N) for i in range(N)]
nxt = {a: b for a, b in naive}
assert nxt[4] == 0
meals = [3, 3, 3, 3, 3]
f.text(145, 14, "five philosophers, five forks", size=11.5, color=NAVY, bold=True)
cx, cy = 145, 140
f.circle(cx, cy, 52, fill=SAND, stroke=AMBER, sw=2)
for i in range(N):
    a = -cm.pi / 2 + 2 * cm.pi * i / N
    px, py = cx + 105 * cm.cos(a), cy + 105 * cm.sin(a)
    f.circle(px, py, 18, fill=BLUE, stroke=NAVY, label="P%d" % i, size=10, color=NAVY)
    a2 = a + cm.pi / N
    fx, fy = cx + 78 * cm.cos(a2), cy + 78 * cm.sin(a2)
    f.circle(fx, fy, 10, fill=MINT, stroke=TEAL, label="%d" % ((i + 1) % N), size=9.5, color=TEAL)
f.text(145, 262, "fork k lies between P(k-1) and Pk", size=9.5, color=SLATE)
f.text(145, 278, "the fork between P4 and P0 is fork 0", size=9.5, color=SLATE)
f.text(430, 14, "who takes which fork first", size=11.5, color=NAVY, bold=True)
f.text(350, 36, "philosopher", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(430, 36, "naive: left, right", size=9.5, color=RED, bold=True, anchor="start")
f.text(520, 36, "ordered", size=9.5, color=TEAL, bold=True, anchor="start")
for i in range(N):
    y = 56 + i * 24
    f.text(364, y, "P%d" % i, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(450, y, "%d then %d" % naive[i], size=10, color=SLATE, anchor="start", vmid=True)
    f.text(524, y, "%d then %d" % order[i], size=10, color=SLATE, bold=(i == 4), anchor="start", vmid=True)
f.box(340, 172, 230, 50, "naive: everyone holds the left fork\nand waits for the right one:\na circle, so deadlock", fill=ROSE, stroke=RED, size=9.5)
f.box(340, 230, 230, 50, "ordered: P4 takes fork 0 before 4,\nbreaking the circle. Real run:\nmeals = [3, 3, 3, 3, 3]", fill=MINT, stroke=TEAL, size=9.5)
```

```svgfig label="1.6" caption="Producer and consumer with a bounded buffer of 3, simulated in the figure: the producer fills the buffer faster than the consumer empties it, so the buffer is full at the red steps and put() must wait. All 10 items come out in order with sum 55, the same sum that a real run with ArrayBlockingQueue gave."
f = Fig(580, 262)
CAP = 3
q = []; nxt = 1; got = []; occ = []; steps = 24
for t in range(steps):
    if nxt <= 10 and len(q) < CAP:
        q.append(nxt); nxt += 1
    if t % 2 == 1 and q:
        got.append(q.pop(0))
    occ.append(len(q))
while q:
    got.append(q.pop(0)); occ.append(len(q))
assert sum(got) == 55 and got == list(range(1, 11)) and max(occ) == CAP
f.text(290, 14, "bounded buffer of 3: a fast producer must wait for a slower consumer", size=11.5, color=NAVY, bold=True)
a = Axes(f, 44, 28, 360, 150, (0, len(occ)), (0, 4)); a.grid(4, 1).axes("time step", "items in the buffer")
for i, v in enumerate(occ):
    f.box(a.X(i), a.Y(v), a.X(1) - a.X(0) - 1, a.Y(0) - a.Y(v), "", fill=ROSE if v == CAP else MINT, stroke=RED if v == CAP else TEAL, r=0, sw=0.8)
a.hline(CAP, color=RED, dash=True)
f.text(a.X(len(occ)) - 4, a.Y(CAP) - 8, "capacity 3: put() blocks", size=9.5, color=RED, bold=True, anchor="end")
f.text(490, 40, "producer", size=10.5, color=NAVY, bold=True)
f.text(490, 56, "put(1) ... put(10)", size=9.5, color=SLATE)
f.text(490, 72, "waits when full", size=9.5, color=SLATE)
f.text(490, 100, "consumer", size=10.5, color=NAVY, bold=True)
f.text(490, 116, "take() each 2nd step", size=9.5, color=SLATE)
f.text(490, 132, "waits when empty", size=9.5, color=SLATE)
f.text(490, 160, "items taken in order:", size=9.5, color=TEAL, bold=True)
f.text(490, 174, "1, 2, ... 10, sum %d" % sum(got), size=9.5, color=TEAL, bold=True)
f.text(290, 214, "a real run with ArrayBlockingQueue(3), two threads and 10 items gave consumer sum = 55", size=10, color=NAVY, bold=True)
f.text(290, 232, "red steps: the buffer was full; the queue does the wait()/notify() work for you", size=9.5, color=SLATE)
f.text(290, 250, "no item is lost or taken twice, because put and take are thread-safe", size=9.5, color=SLATE)
```

```svgfig label="1.7" caption="A fixed pool of 3 threads and 8 tasks of 4, 3, 5, 2, 6, 1, 3 and 2 units, each task going to the first free worker. The pool finishes at time 10 where one thread needs 26, a speed-up of 2.6 times. A real run split the sum of the squares of 1 to 1000 into four Callable tasks, and the four Future values added up to 333,833,500, which equals 1000 x 1001 x 2001 / 6."
f = Fig(580, 262)
dur = [4, 3, 5, 2, 6, 1, 3, 2]
free = [0, 0, 0]; sched = []
for i, d in enumerate(dur):
    w = free.index(min(free)); s = free[w]; free[w] = s + d; sched.append((i + 1, w, s, s + d))
make = max(free); seq = sum(dur)
assert make == 10 and seq == 26 and sched[4] == (5, 0, 4, 10)
f.text(290, 14, "a fixed pool of 3 threads runs 8 tasks (units of time, tasks taken in order)", size=11.5, color=NAVY, bold=True)
a = Axes(f, 70, 30, 480, 120, (0, 12), (0, 3)); a.grid(1, 3, labels=False)
cols = [(BLUE, NAVY), (MINT, TEAL), (SAND, AMBER)]
for t, w, s, e in sched:
    fc, sc = cols[t % 3]
    f.box(a.X(s), a.Y(w + 1) + 4, a.X(e) - a.X(s) - 1, a.Y(w) - a.Y(w + 1) - 8, "T%d" % t, fill=fc, stroke=sc, size=10, bold=True, r=3)
for w in range(3):
    f.text(60, a.Y(w + 0.5), "worker %d" % (w + 1), size=10, color=NAVY, bold=True, anchor="end", vmid=True)
for t in range(0, 13, 2):
    f.text(a.X(t), 164, str(t), size=9.5, color=SLATE)
f.line(a.X(make), 30, a.X(make), 150, color=RED, sw=1.6, dash=True)
f.text(a.X(make), 24, "all done at %d" % make, size=9.5, color=RED, bold=True)
f.text(290, 188, "one thread would take 4+3+5+2+6+1+3+2 = %d units; the pool finishes in %d: speed-up %.1f times" % (seq, make, seq / make), size=10, color=NAVY, bold=True)
f.text(290, 208, "not 3 times, because T5 (6 units) starts late and ends last", size=9.5, color=SLATE)
f.text(290, 232, "a real run: 4 Callable tasks summed squares of 1..1000 in 250-number slices;", size=9.5, color=TEAL, bold=True)
f.text(290, 248, "Future.get() returned 5,239,625 + 36,552,125 + 99,114,625 + 192,927,125 = 333,833,500", size=9.5, color=TEAL, bold=True)
```

```svgfig label="1.8" caption="Layered streams. Each layer adds one service to the one below it. In a real run, reading a 1,000,000-byte file one byte at a time through FileInputStream made 1,000,001 calls to the stream, but with BufferedInputStream the file stream was called only 124 times (123 buffer fills of 8,192 bytes and one end-of-file call), 8,065 times fewer."
f = Fig(580, 262)
un, bu = 1000001, 124
cm = __import__("math")
assert un // bu == 8065 or round(un / bu) == 8065
f.text(150, 14, "streams are layered decorators", size=11.5, color=NAVY, bold=True)
chain = [("file on disk", SOFT, "#94a3b8"), ("FileInputStream\nraw bytes", BLUE, NAVY), ("BufferedInputStream\n8,192-byte buffer", MINT, TEAL), ("InputStreamReader\nbytes to chars (UTF-8)", SAND, AMBER), ("BufferedReader\nreadLine()", ROSE, RED)]
for i, (t, fc, sc) in enumerate(chain):
    y = 28 + i * 44
    f.box(20, y, 260, 34, t, fill=fc, stroke=sc, size=9.5, bold=True)
    if i:
        f.arrow([(150, y - 10), (150, y)], color=SLATE)
f.text(430, 14, "system calls to read a 1,000,000-byte file", size=11, color=NAVY, bold=True)
f.text(310, 44, "FileInputStream, one byte at a time", size=9.5, color=RED, bold=True, anchor="start")
f.box(310, 52, 250, 24, "{:,} calls".format(un), fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(310, 104, "wrapped in BufferedInputStream", size=9.5, color=TEAL, bold=True, anchor="start")
f.box(310, 112, max(2, 250 * bu / un), 24, "", fill=MINT, stroke=TEAL)
f.text(318 + max(2, 250 * bu / un), 124, "{:,} calls".format(bu), size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(430, 166, "%.0f times fewer calls" % (un / bu), size=11, color=NAVY, bold=True)
f.text(430, 186, "1,000,000 / 8,192 = 122.1, so 123 buffer fills", size=9.5, color=SLATE)
f.text(430, 200, "plus 1 call that reports the end of the file", size=9.5, color=SLATE)
f.text(430, 220, "counted with a real wrapper class in a Java run", size=9.5, color=TEAL, bold=True)
f.text(430, 238, "try-with-resources closes every layer for you", size=9.5, color=SLATE)
```

```svgfig label="1.9" caption="Why the character set matters. The Nepali word with five characters takes 15 bytes in UTF-8 (3 per character), 10 bytes in UTF-16, and cannot be held in ISO-8859-1 at all; reading the UTF-8 bytes as ISO-8859-1 gives 15 wrong characters. The numbers come from a real Java run and are re-checked in the figure code."
f = Fig(580, 250)
s = "\u0928\u0947\u092a\u093e\u0932"
u8 = [c.encode("utf-8") for c in s]
assert len(s) == 5 and sum(map(len, u8)) == 15 and len(s.encode("utf-16-be")) == 10
assert len(s.encode("utf-8").decode("latin-1")) == 15
f.text(290, 14, "one Nepali word, five characters, three views of its bytes", size=11.5, color=NAVY, bold=True)
for i, c in enumerate(s):
    x = 14 + i * 112
    f.box(x, 30, 104, 44, c, fill=BLUE, stroke=NAVY, size=24, bold=True)
    f.text(x + 52, 86, "U+%04X" % ord(c), size=9.5, color=SLATE, bold=True)
    f.box(x, 98, 104, 26, " ".join("%02X" % b for b in u8[i]), fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(8, 140, "UTF-8: 3 bytes per character here, 15 bytes in all (ASCII letters need 1 byte)", size=10, color=TEAL, bold=True, anchor="start")
f.text(8, 160, "UTF-16: 2 bytes per character, 10 bytes in all", size=10, color=NAVY, bold=True, anchor="start")
f.text(8, 180, "ISO-8859-1 cannot hold Devanagari: getBytes gives question marks, ?????", size=10, color=RED, bold=True, anchor="start")
f.text(8, 200, "reading UTF-8 bytes as ISO-8859-1 gives 15 wrong characters instead of 5", size=10, color=RED, bold=True, anchor="start")
f.text(8, 224, "so always name the charset: new InputStreamReader(in, StandardCharsets.UTF_8)", size=10, color=NAVY, bold=True, anchor="start")
f.text(8, 242, "the vowel signs show a dotted circle because they combine with the letter before them", size=9.5, color=SLATE, anchor="start")
```

```svgfig label="1.10" caption="Inside a serialized object. The 78 bytes written by writeObject for Student(Sita, 7, password) begin with the magic number AC ED and version 00 05, then describe the class (its name, serialVersionUID 1, two fields roll and name) and finally hold the values: roll = 7 and name = Sita. The transient password does not appear in the stream."
f = Fig(580, 276)
hx = "AC ED 00 05 73 72 00 0B 53 65 72 24 53 74 75 64 65 6E 74 00 00 00 00 00 00 00 01 02 00 02 49 00 04 72 6F 6C 6C 4C 00 04 6E 61 6D 65 74 00 12 4C 6A 61 76 61 2F 6C 61 6E 67 2F 53 74 72 69 6E 67 3B 78 70 00 00 00 07 74 00 04 53 69 74 61"
b = hx.split()
assert len(b) == 78
segs = [(4, "stream header: magic AC ED, version 5", NAVY, BLUE), (2, "TC_OBJECT, TC_CLASSDESC", SLATE, SOFT), (2, "class name length 11", AMBER, SAND), (11, "class name, 11 characters", AMBER, SAND),
        (8, "serialVersionUID = 1", RED, ROSE), (1, "flags: serializable", SLATE, SOFT), (2, "2 fields", SLATE, SOFT), (7, "field I: type int, name roll", TEAL, MINT),
        (7, "field L: object, name name", TEAL, MINT), (21, "type string: Ljava/lang/String;", TEAL, MINT), (2, "end of class info, no superclass", SLATE, SOFT),
        (4, "roll = 7", NAVY, BLUE), (7, "name = Sita", NAVY, BLUE)]
assert sum(s[0] for s in segs) == 78
f.text(290, 14, "the 78 bytes of Student(Sita, 7, password) after writeObject, from a real run", size=11.5, color=NAVY, bold=True)
pos = 0
for i, (n, lab, col, fc) in enumerate(segs):
    y = 28 + i * 18.6
    chunk = " ".join(b[pos:pos + n]); pos += n
    shown = chunk if len(chunk) <= 38 else chunk[:35] + "..."
    f.box(8, y, 262, 16, shown, fill=fc, stroke=col, size=9.5, r=2, sw=0.9, bold=True)
    f.text(280, y + 8, "%d  %s" % (n, lab), size=9.5, color=SLATE, anchor="start", vmid=True)
f.text(290, 272, "transient password is not in the stream: the letters of secret do not appear", size=9.5, color=RED, bold=True)
```

```svgfig label="1.11" caption="Serialization keeps object sharing. Two Person objects that share one Address are written as 198 bytes, with the second reference stored as a short back-reference; with two separate but equal Address objects the stream is 204 bytes. After reading, the two Persons still share one Address (true), but that Address is not the original object (false)."
f = Fig(580, 250)
shared, copies = 198, 204
f.text(145, 14, "two people share one Address object", size=11.5, color=NAVY, bold=True)
f.box(20, 40, 100, 30, "Person Ram", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(20, 130, 100, 30, "Person Sita", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(190, 85, 100, 40, "Address\nPokhara", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(120, 55), (190, 95)], color=SLATE); f.arrow([(120, 145), (190, 115)], color=SLATE)
f.text(145, 190, "written once, then a back-reference", size=10, color=TEAL, bold=True)
f.text(145, 208, "after reading: both Persons still share ONE Address", size=10, color=TEAL, bold=True)
f.text(145, 226, "(real run: same object after round trip = true)", size=9.5, color=SLATE)
f.text(430, 14, "size of the byte stream", size=11.5, color=NAVY, bold=True)
f.text(330, 44, "one shared Address", size=10, color=TEAL, bold=True, anchor="start")
f.box(330, 52, 220 * shared / copies, 24, "%d bytes" % shared, fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(330, 100, "two separate Address objects", size=10, color=AMBER, bold=True, anchor="start")
f.box(330, 108, 220, 24, "%d bytes" % copies, fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.text(430, 160, "the stream keeps the shape of the object graph,", size=9.5, color=SLATE)
f.text(430, 174, "not only the values; the difference is %d bytes" % (copies - shared), size=9.5, color=SLATE)
f.text(430, 196, "but a deserialized copy is never == to the original:", size=9.5, color=NAVY, bold=True)
f.text(430, 210, "real run: same as original = false", size=9.5, color=NAVY, bold=True)
```

### 1.6.1 Eight uses of threads, streams and serialization in Nepal

1. **Many users on one server.** When thousands of people pay a bill through a wallet such as Fonepay or ConnectIPS at the same time, the server cannot serve them one after another. It keeps a pool of threads, as in Figure 1.7, and gives each request to a free thread. A pool of fixed size also protects the server, because extra requests wait in a queue instead of using up all memory.
2. **Apps that stay responsive.** An app such as Nagarik App must keep the screen alive while it downloads a document. The download runs in a second thread and the screen thread only draws. If the download ran on the screen thread, the app would freeze and users would think it had crashed.
3. **Batch jobs.** A utility such as the Nepal Electricity Authority prints bills for lakhs of customers at the end of the month. The work can be cut into slices, one task per slice, and run on a thread pool, as the sum of squares in Figure 1.7 was cut into four tasks. Shared totals must then be protected by `synchronized` or an atomic class (Figure 1.3).
4. **Reading data files.** Weather stations of the Department of Hydrology and Meteorology send readings that arrive as text files. A program reads them line by line through a `BufferedReader`, which makes thousands of times fewer calls than reading byte by byte (Figure 1.8). The program can then average, clean and store the values.
5. **Names in Nepali.** Result sheets of schools and campuses carry names in Devanagari. A program must read and write them with the UTF-8 character set, because the same word that is five characters long is 15 bytes in UTF-8 (Figure 1.9). Forgetting the character set is the commonest reason for question marks in a printed result.
6. **Logs and backups.** Every server writes a log of what it did, and offices copy files to a backup disk each night. Both are stream jobs: a buffered output stream collects many small writes and sends them in large blocks. The `try-with-resources` statement guarantees that the file is closed even when an error occurs.
7. **Saving the state of an application.** An application that keeps a list of records in memory, such as a cache of student records in an education management system, can write the whole object graph to a file with serialization and read it back after a restart. Fields such as passwords are marked `transient` so that they never reach the disk (Figure 1.10). The class needs an explicit `serialVersionUID` so that old files can still be read after a small change.
8. **Sending objects between programs, with care.** Two Java programs, for example a branch application and a central bank server, can pass objects through a socket or RMI, and both use serialization. Never read serialized data from an untrusted sender, because crafted data can run harmful code. For public interfaces, such as an API used by many mobile apps, use JSON instead.

## Formula and fact sheet

- Thread creation: `new Thread(runnable).start()`; `start()` not `run()`. States: new, runnable, blocked, waiting, timed waiting, terminated.
- Race condition fix: `synchronized`, atomic classes or locks. Deadlock needs a circular wait; order locks globally.
- Executor: `Executors.newFixedThreadPool(n)`, `submit(Callable)` → `Future.get()`, `shutdown()`.
- Streams: bytes (`InputStream`/`OutputStream`), characters (`Reader`/`Writer`); try-with-resources closes automatically.
- Serialization: `Serializable`, `transient` skipped, `static` skipped, explicit `serialVersionUID`.

## Chapter summary

- A thread is an independent path of execution sharing the process's memory; shared mutable data needs synchronisation.
- Executors and futures are the practical way to run tasks concurrently and collect results.
- Java I/O is layered streams; try-with-resources and `java.nio.file` make file work short and safe.
- Serialization turns an object graph into bytes (and back) and underlies persistence and RMI; `transient` fields are not saved.

## Practice

1. Differentiate a process from a thread. Give two ways to create a thread.
2. Why is `start()` used rather than `run()`?
3. Show how a race condition can lose an update and fix it with `synchronized`.
4. Describe the life cycle of a thread.
5. What is a deadlock and how can it be avoided?
6. Write code that reads a text file line by line and counts words using try-with-resources.
7. Differentiate byte streams from character streams; name a decorator and its effect.
8. What do `Serializable`, `transient` and `serialVersionUID` do?
9. Why must `Serializable` data from untrusted sources not be deserialized?
10. Explain how a `Callable` and a `Future` differ from a `Runnable`.

::: note Answers and worked solutions
**1.** A process has its own memory space; threads of a process share memory. Create threads by extending `Thread` and overriding `run()`, or by passing a `Runnable` (or lambda) to `new Thread(...)`; or use an executor.
**2.** `start()` creates a new thread of execution and calls `run()` there; calling `run()` executes it in the caller's thread without concurrency.
**3.** Two threads read `count` = 5 at the same time and both write 6, losing one increment. Put `count++` inside `synchronized (lock) { ... }` (or use `AtomicInteger`), so that only one thread updates at a time: four threads of 50,000 increments then produce exactly 200,000.
**4.** New → runnable (after `start`) → running; it may be blocked on a lock, waiting (`wait`, `join`) or timed waiting (`sleep`); when `run()` returns it is terminated.
**5.** Threads waiting for each other's locks in a cycle. Avoid by acquiring locks in a fixed order, holding few locks, using timeouts (`tryLock`) or higher-level concurrency classes.
**6.** `try (BufferedReader br = Files.newBufferedReader(path)) { String line; while ((line = br.readLine()) != null) words += line.split("\\s+").length; }`, as in the FileDemo program.
**7.** Byte streams move raw bytes; character streams convert bytes to characters using an encoding. `BufferedReader` wraps a `Reader` and adds buffering and `readLine()`.
**8.** `Serializable` marks a class as convertible to bytes; `transient` excludes a field; `serialVersionUID` is the version stamp checked at deserialization.
**9.** Deserialization can instantiate arbitrary classes and run their code; attacker-crafted streams have been used to execute commands. Use data formats such as JSON and validate input.
**10.** `Runnable.run()` returns nothing and cannot throw checked exceptions; `Callable.call()` returns a value and may throw; the `Future` returned by `submit` lets the caller wait for that value (`get`) or cancel the task.
:::

## Model answers for Unit 1

**Q1. What is a thread? Explain the ways of creating a thread and the life cycle of a thread. (10 marks)**

**Introduction.** A **thread** is an independent path of execution inside a process. Threads of one process share its heap memory, so they are cheaper to create and switch than processes. A GUI uses one thread to draw and others to work; a server uses a pool of threads, one for each request.

**Creating threads.** (1) Extend `Thread` and override `run()`. (2) Implement `Runnable` and pass it to `new Thread(runnable)`; this is preferred because the class can still extend another class, and a lambda can be used because `Runnable` has one method. (3) Submit a `Runnable` or `Callable` to an `ExecutorService`, the usual way in real programs. In all cases `start()` creates the new thread and calls `run()` in it; calling `run()` directly only calls a method in the current thread.

**Life cycle (Fig. 1.2).** A thread goes through six states of `Thread.State`:

| State | Meaning | How it is entered |
|---|---|---|
| NEW | created, not started | `new Thread(...)` |
| RUNNABLE | ready or running | `start()` |
| BLOCKED | waiting for a monitor lock | entering a `synchronized` block that another thread holds |
| WAITING | waiting without a time limit | `wait()`, `join()` |
| TIMED_WAITING | waiting for a limited time | `sleep(ms)`, `wait(ms)` |
| TERMINATED | finished | `run()` ends |

A real run of a test program printed NEW, RUNNABLE, WAITING, TIMED_WAITING, WAITING, BLOCKED and TERMINATED, so every state was seen. `interrupt()` politely asks a thread to stop; priorities 1 to 10 are only hints; daemon threads do not keep the JVM alive.

**Conclusion.** Create threads with `Runnable` or an executor, call `start()`, and remember that the operating system, not the program, decides which runnable thread gets the processor.

**Q2. What is a race condition? How does `synchronized` remove it? Name two other remedies. (10 marks)**

**Introduction.** A **race condition** occurs when the result of a program depends on the order in which threads touch shared data. The standard example is `count++`, which is really three steps: read, add one, write.

**How an update is lost (Fig. 1.3).** Let count be 5. If T1 and T2 both read 5 before either writes, both compute 6 and both write 6, so the final value is 6 instead of 7. If one thread finishes its three steps before the other begins, the result is 7. A real run with two threads adding 1,000,000 times each ended at 1,985,476 for the unsynchronized counter, which lost 14,524 increments (0.73 percent), and the loss is different on every run.

**Synchronized.** A `synchronized` method or block takes the **monitor lock** of an object. Only one thread can hold it, so the three steps of `count++` cannot interleave, and the real run gave exactly 2,000,000. Leaving the block also makes the new value visible to the other threads (memory visibility).

| Remedy | Idea | Note |
|---|---|---|
| `synchronized` | one thread at a time holds the monitor | simple; may cause blocking |
| `AtomicInteger` | hardware compare-and-set, no lock | exact 2,000,000 in the real run |
| `ReentrantLock` | explicit lock, `tryLock` possible | must unlock in `finally` |
| `volatile` | visibility of one variable only | does not make `count++` atomic |

**Conclusion.** Shared mutable data must be protected; the smaller the protected region, the less the threads wait.

**Q3. What is a deadlock? State the conditions and explain how it can be avoided, using the dining philosophers problem. (10 marks)**

**Introduction.** A **deadlock** is a state in which each thread of a group waits for a lock held by another thread of the group, so none can go on. A traffic gridlock is the everyday picture (Plate 1.2).

**Example (Fig. 1.4).** T1 holds lock A and wants B, while T2 holds B and wants A. The wait-for graph has the cycle T1, B, T2, A, T1. A real run with these two threads ended with both threads BLOCKED, and `findDeadlockedThreads()` reported 2 threads.

**Four conditions (Coffman).** (1) *Mutual exclusion*: a lock can be held by one thread only. (2) *Hold and wait*: a thread keeps one lock while it asks for another. (3) *No pre-emption*: a lock cannot be taken away. (4) *Circular wait*: the threads form a cycle of waiting. Removing any one prevents deadlock.

**Dining philosophers (Fig. 1.5).** Five philosophers sit at a round table with a fork between neighbours, and each needs both neighbouring forks. If every philosopher takes the left fork first, all five hold one fork and wait for the right one: a circular wait. If every philosopher takes the lower-numbered fork first, only P4 changes (fork 0 before fork 4), the cycle is broken, and a real run gave every philosopher 3 meals.

**Avoiding deadlock.** Acquire locks in one global order; use `tryLock` with a time limit and back off; hold as few locks as possible; keep locked regions short.

**Conclusion.** Deadlock cannot be repaired by luck; it is prevented by design, most simply by a global lock order.

**Q4. Explain the producer–consumer problem and how it is solved in Java. (5 marks)**

In the **producer–consumer problem** one or more threads produce items and others consume them through a shared buffer of limited size. The producer must wait when the buffer is full and the consumer must wait when it is empty, and no item may be lost or used twice (Plate 1.2, the factory line).

**Classical solution.** Keep the buffer in an object and guard it with `synchronized`. The producer calls `wait()` while the buffer is full and `notifyAll()` after adding; the consumer calls `wait()` while it is empty and `notifyAll()` after removing. The `wait()` call is placed in a `while` loop, not an `if`, because a woken thread must test the condition again.

**Simple solution.** Use a `BlockingQueue` such as `ArrayBlockingQueue`: `put()` blocks when the queue is full and `take()` blocks when it is empty, so the waiting is done for you. In Fig. 1.6 the buffer holds 3 items; the producer fills it faster than the consumer empties it, the buffer is full at the red steps, and all 10 items come out in order with the sum 55, as in a real run with two threads.

**Q5. What are executors, `Callable` and `Future`? How do they differ from `Runnable`? (5 marks)**

Creating a new thread for every task is costly. An **`ExecutorService`** keeps a pool of threads and runs submitted tasks on them; `Executors.newFixedThreadPool(n)` makes a pool of n threads, and `shutdown()` stops it after the queued tasks finish.

A **`Runnable`** has `void run()`: it returns nothing and cannot throw a checked exception. A **`Callable<V>`** has `V call() throws Exception`: it returns a value and may throw. `submit(callable)` returns a **`Future<V>`**, a receipt for a result that may not be ready; `get()` waits until the result is ready (or rethrows the failure), `isDone()` tests it and `cancel()` tries to stop the task.

**Example (Fig. 1.7).** Eight tasks of 4, 3, 5, 2, 6, 1, 3 and 2 units on a pool of 3 threads finish at time 10, where one thread needs 26 units: a speed-up of 2.6 times, not 3, because task T5 ends last. In a real run four Callable tasks summed squares of 1 to 1000 in slices, and the four Future values 5,239,625, 36,552,125, 99,114,625 and 192,927,125 add up to 333,833,500 = 1000 × 1001 × 2001 / 6.

**Q6. Differentiate byte streams from character streams. Why are buffered streams and a character set important? (5 marks)**

**Byte streams** (`InputStream`, `OutputStream`) move raw 8-bit bytes and suit images, audio, class files and serialized objects. **Character streams** (`Reader`, `Writer`) move 16-bit characters and convert between bytes and text using a character set; they suit text files. `InputStreamReader` is the bridge from a byte stream to a character stream.

**Buffering (Fig. 1.8).** A call to the operating system is slow. Reading a 1,000,000-byte file one byte at a time through `FileInputStream` made 1,000,001 calls in a real run, but wrapped in `BufferedInputStream` it made only 124, which is 8,065 times fewer. `BufferedReader` adds `readLine()`.

**Character set (Fig. 1.9).** The Nepali word नेपाल has 5 characters but 15 bytes in UTF-8 and 10 bytes in UTF-16, and it cannot be stored in ISO-8859-1. Reading UTF-8 bytes as ISO-8859-1 gives 15 wrong characters. Always name the charset, for example `StandardCharsets.UTF_8`, and close files with try-with-resources.

**Q7. What is serialization? Explain `Serializable`, `transient`, `static` and `serialVersionUID`, and the dangers of deserialization. (10 marks)**

**Introduction.** **Serialization** converts an object, and everything reachable from it, into a stream of bytes; **deserialization** builds an equal object from the bytes. It is used to save objects to disk, send them through sockets and pass them in RMI (Unit 5).

**Rules.**

1. The class must implement the marker interface **`java.io.Serializable`**, and so must the types of all its non-transient fields; otherwise `NotSerializableException` is thrown.
2. **`transient`** fields are skipped and come back as null or 0; use it for passwords, caches and open files.
3. **`static`** fields belong to the class and are not written.
4. **`serialVersionUID`** names the version of the class; if the value in the stream differs from the class, `InvalidClassException` is thrown, so declare it explicitly.
5. Sharing is preserved (Fig. 1.11): two Persons that share one Address give a stream of 198 bytes with a back-reference, against 204 bytes for two separate Addresses, and after reading they still share one Address. The copy is never `==` to the original.

**The stream (Fig. 1.10).** Writing Student(Sita, 7, password) gave 78 bytes: the header AC ED 00 05, a description of the class (name, serialVersionUID 1, fields roll and name) and then the values roll = 7 and name = Sita. The transient password is absent, so reading gives password = null.

**Dangers.** Deserialization can construct objects of any serializable class on the classpath and run their code, so data from an untrusted source can run harmful code. Never deserialize untrusted data; filter classes with `ObjectInputFilter`, or use JSON for public interfaces.

**Conclusion.** Serialization is convenient for trusted, same-version Java programs and risky everywhere else.

**Q8. Write a program that reads a text file line by line and counts its lines and words using try-with-resources. (5 marks)**

The program writes a three-line sample file and then reads it back with a `BufferedReader`. The reader is declared in the parentheses of `try`, so it is closed automatically, even if an exception occurs. `readLine()` returns `null` at the end of the file, and `split("\\s+")` cuts a line at runs of white space.

```java
import java.io.*;
import java.nio.file.*;
public class WordCount {
    public static void main(String[] args) throws IOException {
        Path p = Files.createTempFile("w", ".txt");
        Files.writeString(p, "Nepal is a country\nKathmandu is its capital\nPokhara has a lake\n");
        int lines = 0, words = 0;
        try (BufferedReader r = Files.newBufferedReader(p)) {
            String s;
            while ((s = r.readLine()) != null) {
                lines++;
                if (!s.isBlank()) words += s.trim().split("\\s+").length;
            }
        }
        System.out.println("lines=" + lines + " words=" + words);
    }
}
```
```output
lines=3 words=12
```
The three lines hold 4, 4 and 4 words, so 12 words in all. The text is read with the default character set; for Nepali text use `Files.newBufferedReader(p, StandardCharsets.UTF_8)`.

**Q9. Differentiate a process from a thread, and say why multithreading helps on a multi-core processor. (5 marks)**

A **process** is a running program with its own address space, files and resources. A **thread** is a unit of execution inside a process; threads of the same process share its heap, code and open files but each has its own stack and program counter.

| Point | Process | Thread |
|---|---|---|
| Memory | separate address space | shared heap of the process |
| Creation and switch | slow, heavy | fast, light |
| Communication | pipes, sockets, shared memory | shared variables (need locks) |
| Failure | one process rarely harms another | an unhandled error can affect the whole process |

**Multi-core use (Plate 1.1).** A processor die has several cores, and each core runs one thread at a time. A program with one thread can use only one core; a program with several threads can run them at the same moment on different cores, as the pool of 3 workers in Fig. 1.7 finished eight tasks in 10 units against 26 units for a single worker. Threads also hide waiting: while one thread waits for a disk or a network, another keeps working. The price is the need for synchronisation and the risk of deadlock.

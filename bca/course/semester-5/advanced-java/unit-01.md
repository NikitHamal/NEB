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

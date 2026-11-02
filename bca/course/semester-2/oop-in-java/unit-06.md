---
subject: OOP in Java
grade: BCA Semester 2
unit: 6
title: Multithreading, GUI Event Handling and Database Access
area: BCA 153 · OOP in Java · Unit 6
---

Modern programs do several things at once, respond to users through graphical interfaces and keep data in databases. This final unit introduces **threads and synchronisation**, **event-driven GUI programming** with Swing, and **JDBC** for relational databases, and ends with a mini project that combines the whole course.

::: key What this unit gives you
- Creating threads, the thread life cycle, race conditions, `synchronized`, `ExecutorService`.
- Swing components, layout, and the event-listener model.
- JDBC: connect, query, update with prepared statements, transactions.
- A design for a small project using all the pillars.
:::

## 6.1 Threads

A **thread** is an independent path of execution inside a process; threads share the process's heap but each has its own stack. **Multithreading** keeps a GUI responsive, uses multiple cores and overlaps waiting for I/O.

**Creating threads:** implement `Runnable` (preferred; `new Thread(runnable).start()`) or extend `Thread`. Call **`start()`** (runs `run()` on a new thread), not `run()` (which runs in the caller's thread).

**Life cycle:** *New* → `start()` → *Runnable* (ready or running) → *Blocked/Waiting/Timed-waiting* (lock, `wait`, `sleep`, `join`) → *Terminated*. Useful: `Thread.sleep(ms)`, `join()` (wait for another thread to finish), `interrupt()`, `setDaemon(true)` (a background thread that does not keep the JVM alive), `Thread.currentThread().getName()`, priorities (hints only).

**Race condition.** `counter++` is three steps (read, add, write); two threads can interleave and lose updates. **`synchronized`** makes a block or method hold the object's **monitor lock**, so only one thread at a time runs it (mutual exclusion).

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
public class Threads {
    static int counter = 0;
    static final Object lock = new Object();
    public static void main(String[] a) throws Exception {
        Runnable r = () -> { for (int i = 0; i < 100000; i++) synchronized (lock) { counter++; } };
        Thread t1 = new Thread(r), t2 = new Thread(r);
        t1.start(); t2.start(); t1.join(); t2.join();
        System.out.println(counter);
        ExecutorService ex = Executors.newFixedThreadPool(2);
        Future<Integer> f = ex.submit(() -> { int s = 0; for (int i = 1; i <= 100; i++) s += i; return s; });
        System.out.println(f.get());
        AtomicInteger at = new AtomicInteger();
        Runnable r2 = () -> { for (int i = 0; i < 50000; i++) at.incrementAndGet(); };
        Future<?> g1 = ex.submit(r2), g2 = ex.submit(r2);
        g1.get(); g2.get();
        System.out.println(at.get());
        ex.shutdown();
    }
}
```
```output
200000
5050
100000
```

Without `synchronized`, the first total would usually be *less* than 200000 and would change from run to run, the signature of a race. Alternatives to locking: **`AtomicInteger`** (lock-free), **`ConcurrentHashMap`**, `volatile` (visibility only, not atomicity), immutable objects.

**Thread pools and `ExecutorService`** reuse threads (creating one per task is costly): `submit(Callable)` returns a `Future` whose `get()` blocks for the result; always `shutdown()`. **`CompletableFuture`** chains asynchronous steps.

**Coordination:** `wait()`/`notify()` inside `synchronized` for producer–consumer; better, a `BlockingQueue` (`put` blocks when full, `take` blocks when empty). **Deadlock** needs mutual exclusion, hold-and-wait, no pre-emption and circular wait; prevent it by acquiring locks in one global order. **Thread-safety checklist:** share nothing if you can; make shared data immutable; otherwise guard *all* access with the same lock.

## 6.2 GUI programming with Swing

**Swing** (`javax.swing`) is Java's classic desktop GUI toolkit (JavaFX is the newer one; the ideas are identical). A GUI is a tree of **components** inside a **container**:

- Top level: `JFrame`. Containers: `JPanel`. Components: `JLabel`, `JButton`, `JTextField`, `JTextArea`, `JCheckBox`, `JRadioButton`, `JComboBox`, `JList`, `JTable`, `JMenuBar`.
- **Layout managers** place components: `FlowLayout` (left to right), `BorderLayout` (north, south, east, west, centre), `GridLayout` (grid), `BoxLayout`, `GridBagLayout`.
- **Event model:** a **source** (a button) fires an **event** object (`ActionEvent`, `MouseEvent`, `KeyEvent`, `WindowEvent`) to registered **listeners** (`ActionListener`, `MouseListener` …); you write the handler. In modern code the listener is a lambda.
- Swing is single-threaded: build and update the GUI on the **Event Dispatch Thread** via `SwingUtilities.invokeLater(...)`; run long tasks in a worker thread (`SwingWorker`) so the window does not freeze.

```java
import javax.swing.*;
import java.awt.*;
public class Adder extends JFrame {
    public Adder() {
        super("Adder");
        JTextField a = new JTextField(5), b = new JTextField(5);
        JLabel out = new JLabel("Result: ");
        JButton add = new JButton("Add");
        add.addActionListener(e -> {
            try { out.setText("Result: " + (Integer.parseInt(a.getText().trim()) + Integer.parseInt(b.getText().trim()))); }
            catch (NumberFormatException ex) { out.setText("Enter whole numbers"); }
        });
        setLayout(new FlowLayout());
        add(a); add(new JLabel("+")); add(b); add(add); add(out);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Adder().setVisible(true));
    }
}
```

This program needs a display, so it is compiled by the checker but not run there. Run it on a desktop with `java Adder`. The pattern to remember: *create components → add listeners → add to a layout → pack → show*. Handling keyboard and mouse events uses `KeyAdapter` or `MouseAdapter` (empty implementations of the listener interfaces, so you override only what you need).

## 6.3 Database access with JDBC

**JDBC** (`java.sql`) is the standard API to relational databases. Steps: obtain a `Connection` (URL, user, password) → create a `PreparedStatement` → execute → read a `ResultSet` → close everything (try-with-resources). A **driver** JAR for the database (MySQL, PostgreSQL, SQLite) must be on the class path.

```java
import java.sql.*;
public class Jdbc {
    static void demo(String url, String user, String pass) throws SQLException {
        try (Connection con = DriverManager.getConnection(url, user, pass)) {
            con.setAutoCommit(false);
            try (PreparedStatement ins = con.prepareStatement("INSERT INTO student(name, marks) VALUES (?, ?)")) {
                ins.setString(1, "Sita");
                ins.setInt(2, 82);
                ins.executeUpdate();
            }
            try (PreparedStatement q = con.prepareStatement("SELECT name, marks FROM student WHERE marks >= ? ORDER BY marks DESC")) {
                q.setInt(1, 70);
                try (ResultSet rs = q.executeQuery()) {
                    while (rs.next()) System.out.println(rs.getString("name") + " " + rs.getInt("marks"));
                }
            }
            con.commit();
        }
    }
    public static void main(String[] args) { System.out.println("needs a database driver and a running server"); }
}
```

Points: use **`PreparedStatement` with `?` placeholders**, never string concatenation, to prevent **SQL injection** (an input of `' OR '1'='1` would otherwise change the query's meaning). Turn off **auto-commit** and `commit()`/`rollback()` for multi-step changes (the ACID transaction from the Computer Fundamentals database unit). A **connection pool** (HikariCP) reuses connections. A **DAO** (data access object) class hides the SQL behind methods such as `findById`; this keeps the rest of the program independent of the database.

## 6.4 Putting it together: a small project design

**Library Management System** (a typical BCA mini project):

| Layer | Classes | Concepts used |
|---|---|---|
| Model | `abstract class Item` (id, title); `Book`, `Magazine` extend it; `Member`; `Loan` (member, item, dates) | encapsulation, inheritance, `equals`/`hashCode` |
| Interfaces | `Borrowable` with `loanDays()`; `Repository<T>` generic CRUD | interfaces, generics |
| Logic | `LibraryService` with `borrow()`, `giveBack()`, `fine()`; throws `ItemNotAvailableException` | exceptions, collections, streams |
| Persistence | `JdbcLoanRepository` or file store using `Files` | JDBC / file I/O |
| UI | Swing screens or a console menu | event handling, threads for long tasks |

**Fine rule example** (to make it concrete): Rs 5 per day after 14 days; a book returned after 20 days owes (20 − 14) × 5 = **Rs 30**. Write unit tests (JUnit) for it first, then the code. Document with Javadoc (`/** … */`, generated by `javadoc`), use Git, and package the result as a `jar`.

## Formula and fact sheet

- `start()` creates a thread, `run()` does not; `join()` waits.
- `counter++` is not atomic; fix with `synchronized`, `AtomicInteger` or a lock.
- Executors reuse threads; `Future.get()` blocks; `shutdown()` at the end.
- Deadlock = mutual exclusion + hold-and-wait + no pre-emption + circular wait; break by lock ordering.
- Swing: source → event → listener; update the GUI on the EDT.
- JDBC: `PreparedStatement` with `?`, try-with-resources, transactions via `commit`/`rollback`.

## Chapter summary

- Threads give concurrency, but shared mutable state needs synchronisation to avoid races and deadlocks.
- Executors, atomics and concurrent collections are safer than raw threads and locks.
- GUI programs are event driven: components register listeners and long work moves off the UI thread.
- JDBC connects Java to SQL databases; prepared statements and transactions make it safe.
- A real project combines classes, interfaces, generics, collections, exceptions, I/O, threads and a database.

## Practice

1. Differentiate a process and a thread. List the states of a thread.
2. Why can two threads incrementing a shared `int` lose updates? Fix with two different techniques.
3. Differentiate `run()` and `start()`. Differentiate `synchronized` method and block.
4. Write a producer–consumer using `BlockingQueue<Integer>` (describe the steps).
5. What is a deadlock? Give an example with two locks and a fix.
6. Explain the event-delegation model with a `JButton` example.
7. Differentiate `FlowLayout`, `BorderLayout` and `GridLayout`.
8. Why is it dangerous to build a SQL query with string concatenation? Show the fix.
9. Write JDBC steps to transfer Rs 500 between two accounts atomically.
10. Design the class diagram (in words) for a Student Result System and list the exceptions you would define.

::: note Answers and worked solutions
**1.** A process has its own memory space; threads in a process share memory. States: new, runnable, running, blocked/waiting, timed waiting, terminated.
**2.** `x++` is read–modify–write; interleaving loses an update. Fix with a `synchronized` block around the increment, or use `AtomicInteger.incrementAndGet()`.
**3.** `start()` creates a new thread that calls `run()`; calling `run()` directly executes in the current thread. A `synchronized` method locks `this` for the whole method; a block locks the named object for only the critical section (finer-grained).
**4.** Create `BlockingQueue<Integer> q = new ArrayBlockingQueue<>(10)`; the producer thread loops `q.put(i)`; the consumer loops `q.take()` and processes; `put` blocks when full and `take` blocks when empty, so no explicit `wait`/`notify` is needed.
**5.** Thread 1 holds lock A and waits for B while thread 2 holds B and waits for A. Fix: make every thread acquire the locks in the same order (A then B), or use `tryLock` with a timeout.
**6.** The button is the event source; `button.addActionListener(e -> label.setText("Clicked"))` registers a listener; on click, Swing creates an `ActionEvent` and calls the listener on the event-dispatch thread.
**7.** FlowLayout: left to right, wrapping; BorderLayout: five regions; GridLayout: equal cells in rows and columns.
**8.** Input such as `x' OR '1'='1` changes the query logic (SQL injection). Use `prepareStatement("… WHERE name = ?")` and `setString(1, name)`, so the input is always treated as data.
**9.** `setAutoCommit(false)`; `UPDATE account SET bal = bal - 500 WHERE id = ? AND bal >= 500`; check the update count is 1; `UPDATE account SET bal = bal + 500 WHERE id = ?`; `commit()`; on any exception `rollback()`.
**10.** Classes `Student`, `Course`, `Result` (student, course, marks), `ResultService`; interface `GradingPolicy` with implementations; exceptions `InvalidMarksException` (checked) and `StudentNotFoundException`.
:::

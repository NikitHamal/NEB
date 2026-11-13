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
// compile-only
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
```output
needs a database driver and a running server
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

## 6.5 Threads, servers and databases in pictures

A **thread** is a path of execution inside a program. Modern processors contain several cores (Plate 6.1a), and each core can run a different thread at the same instant, so a program that uses threads can really do several jobs together. A thread passes through the states of Figure 6.1: it is *runnable* until the scheduler gives it a core, can wait for a lock or for a timer, and ends when `run()` finishes. Real applications usually keep their data on a database server (Plate 6.1b) and reach it through JDBC. Figure 6.2 shows why the same Java code can talk to different databases: the program uses only the standard `java.sql` interfaces, and a **driver** translates the calls into the protocol of the particular database.

```photogrid label="6.1" cols="2" ratio="1.2" caption="(a) The die of a system-on-chip with many processing blocks: threads let a program use several cores at once. (b) A cold aisle in a data centre: the servers that host databases reached through JDBC."
@ photo id="bca153/socdie" cap="Die of a multi-block system-on-chip"
fit 1.2
focus 0.5 0.5
call 0.30 0.60 0.50 0.60 "Processing blocks"
@ photo id="bca153/dcrack" cap="Data-centre aisle of server racks"
fit 1.2
focus 0.5 0.5
call 0.28 0.28 0.50 0.62 "Server racks"
```

```svgfig label="6.1" caption="Thread life cycle. start() moves a NEW thread to RUNNABLE; the scheduler runs it. It can be BLOCKED waiting for a lock, WAITING for another thread (join, wait) or TIMED_WAITING (sleep). When run() ends it is TERMINATED."
f = Fig(600, 230)
f.box(10, 88, 70, 40, "NEW", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(130, 88, 100, 40, "RUNNABLE", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(480, 88, 110, 40, "TERMINATED", fill="#fecaca", stroke=RED, color=NAVY, size=11, bold=True)
f.box(330, 14, 120, 36, "BLOCKED", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(330, 88, 120, 36, "WAITING", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(330, 168, 120, 36, "TIMED_WAITING", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.arrow([(80, 108), (130, 108)], color=SLATE, sw=2)
f.text(105, 78, "start()", size=10.5, color=NAVY, bold=True)
f.arrow([(230, 96), (330, 32)], color=SLATE, sw=1.5)
f.arrow([(230, 108), (330, 108)], color=SLATE, sw=1.5, both=True)
f.arrow([(230, 120), (330, 184)], color=SLATE, sw=1.5, both=True)
f.arrow([(180, 128), (180, 150), (535, 150), (535, 128)], color=SLATE, sw=1.5)
f.text(380, 164, "run() ends", size=10, color=NAVY, bold=True)
f.text(235, 56, "lock busy", size=10, color=AMBER, bold=True, anchor="end")
f.text(280, 98, "join / wait", size=10, color=AMBER, bold=True)
f.text(235, 176, "sleep(ms)", size=10, color=AMBER, bold=True, anchor="end")
```

```svgfig label="6.2" caption="JDBC architecture. The Java program uses only the java.sql interfaces (Connection, PreparedStatement, ResultSet). DriverManager loads the driver for the URL, and the driver speaks the database's own protocol."
f = Fig(600, 190)
f.box(10, 70, 110, 50, "Java application\nSELECT, INSERT", fill=BLUE, color=NAVY, size=10.5, bold=True)
f.box(160, 70, 110, 50, "JDBC API\njava.sql", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.box(310, 70, 110, 50, "DriverManager\n+ driver (JAR)", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10.5, bold=True)
for y, n in ((20, "MySQL / MariaDB"), (80, "PostgreSQL"), (140, "H2 / SQLite")):
    f.box(470, y, 120, 36, n, fill="#ffffff", stroke=NAVY, color=NAVY, size=10.5, bold=True)
    f.arrow([(420, 95), (445, 95), (445, y + 18), (470, y + 18)], color=SLATE, sw=1.5)
for x1, x2 in ((120, 160), (270, 310)):
    f.arrow([(x1, 95), (x2, 95)], color=SLATE, sw=2)
f.text(300, 175, "jdbc:postgresql://host/db   |   jdbc:h2:mem:college", size=10.5, color=RED, bold=True)
```

## 6.6 Eight uses of threads, GUI and JDBC

1. **Responsive programs.** A background thread can download a file or save data while the window stays usable. If everything ran on the user-interface thread, the screen would freeze. Swing programs use `SwingWorker` for exactly this reason.
2. **Serving many users.** A web or chat server gives each request its own thread, or takes one from a pool. A server for an online exam can accept hundreds of students together instead of one by one.
3. **Using many cores.** Splitting a big job into parts that run on different cores finishes it sooner. Adding up a million marks, resizing images or searching log files can all be divided among threads.
4. **Safe sharing.** `synchronized`, locks and atomic classes make sure two threads do not update the same variable at once. Without them the total of two counters can come out wrong, as the race demonstration shows.
5. **Desktop and tool interfaces.** Swing builds windows from components such as `JFrame`, `JButton` and `JTable`, and responds to events. Small administration tools for a school or a shop are quickly built with it.
6. **Persistent data.** JDBC lets a program store records in a database that survives restarts. Student results, bills and attendance are kept safely and can be searched with SQL.
7. **Database independence.** The program uses standard `java.sql` interfaces, so changing from H2 to PostgreSQL mostly means changing a driver and a URL. This protects an application when the organisation changes its database.
8. **Safe queries and transactions.** Prepared statements stop SQL injection, and commit and rollback keep related changes together. A fund transfer either completes both the debit and the credit or neither, which matters for any payment system.

## 6.7 Synchronisation in depth: thread states, producer–consumer and deadlock

### Thread states, observed

`Thread.getState()` returns one of six values: **NEW** (created, not started), **RUNNABLE** (running, or ready and waiting for a CPU), **BLOCKED** (waiting to *enter* a `synchronized` block held by another thread), **WAITING** (indefinite wait: `Object.wait()`, `join()`, `LockSupport.park`), **TIMED_WAITING** (`sleep(ms)`, `wait(ms)`, `join(ms)`) and **TERMINATED**. The program below drives one thread through each state and prints it.

```java
public class States {
    public static void main(String[] args) throws Exception {
        Object lock = new Object();
        Thread t = new Thread(() -> { synchronized (lock) { } });
        System.out.println("1 " + t.getState());
        synchronized (lock) {
            t.start();
            while (t.getState() != Thread.State.BLOCKED) Thread.sleep(5);
            System.out.println("2 " + t.getState());
        }
        t.join();
        System.out.println("3 " + t.getState());
        Thread s = new Thread(() -> {
            try { Thread.sleep(5000); } catch (InterruptedException e) { System.out.println("sleeper interrupted"); }
        });
        s.start();
        while (s.getState() != Thread.State.TIMED_WAITING) Thread.sleep(5);
        System.out.println("4 " + s.getState());
        s.interrupt(); s.join();
        Thread w = new Thread(() -> { synchronized (lock) { try { lock.wait(); } catch (InterruptedException e) { } } });
        w.start();
        while (w.getState() != Thread.State.WAITING) Thread.sleep(5);
        System.out.println("5 " + w.getState());
        synchronized (lock) { lock.notifyAll(); }
        w.join();
        System.out.println("6 " + w.getState());
    }
}
```

```output
1 NEW
2 BLOCKED
3 TERMINATED
4 TIMED_WAITING
sleeper interrupted
5 WAITING
6 TERMINATED
```

While `main` holds `lock`, thread `t` reaches `synchronized (lock)` and becomes **BLOCKED**; a sleeping thread is **TIMED_WAITING** and `interrupt()` wakes it with an `InterruptedException`, which is the standard way to ask a thread to stop; a thread inside `wait()` is **WAITING** until another thread calls `notify` or `notifyAll` on the same monitor. Never ignore `InterruptedException`: restore the flag with `Thread.currentThread().interrupt()` if you cannot handle it.

### Producer–consumer with `wait` and `notifyAll`

A **bounded buffer** lets a fast producer and a slow consumer cooperate. The producer must wait when the buffer is full, the consumer when it is empty. Both methods are `synchronized`, check the condition in a **`while` loop** (never `if`, because a thread can wake up spuriously or after another thread has already taken the item) and call `notifyAll()` after changing the state.

```svgfig label="6.3" caption="A bounded buffer of capacity 3. The producer thread calls put and sleeps in wait() when the buffer is full; the consumer calls take and sleeps when it is empty. Each side calls notifyAll() after it changes the buffer, which wakes the other."
f = Fig(620, 210)
f.box(20, 70, 130, 60, "Producer\nthread", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
f.box(470, 70, 130, 60, "Consumer\nthread", fill="#fde68a", stroke=AMBER, color=NAVY, size=12, bold=True)
for i, (lab, fl) in enumerate((("4", BLUE), ("5", BLUE), ("6", BLUE))):
    f.box(215 + i * 62, 80, 56, 40, lab, fill=fl, color=NAVY, size=13, bold=True)
f.box(205, 70, 196, 60, "", fill="none", stroke=NAVY)
f.text(303, 62, "buffer: capacity 3, size 3 (full)", size=10.5, color=NAVY, bold=True)
f.arrow([(150, 100), (205, 100)], color=TEAL, sw=2, label="put(7)", lpos=(178, 90))
f.arrow([(401, 100), (470, 100)], color=AMBER, sw=2, label="take()", lpos=(436, 90))
f.text(85, 160, "buffer full: wait()", size=11, color=RED, bold=True)
f.text(85, 178, "until the consumer takes", size=10, color=NAVY)
f.text(535, 160, "after take(): notifyAll()", size=11, color=TEAL, bold=True)
f.text(535, 178, "wakes the producer", size=10, color=NAVY)
f.text(303, 160, "state is protected by one lock (the Buffer object)", size=10.5, color=NAVY, bold=True)
f.text(303, 178, "conditions are re-checked in a while loop", size=10, color=NAVY)
```

```java
import java.util.*;
public class ProdCons {
    static class Buffer {
        private final Queue<Integer> q = new LinkedList<>();
        private final int cap;
        int maxSeen = 0;
        Buffer(int cap) { this.cap = cap; }
        synchronized void put(int v) throws InterruptedException {
            while (q.size() == cap) wait();
            q.add(v);
            maxSeen = Math.max(maxSeen, q.size());
            notifyAll();
        }
        synchronized int take() throws InterruptedException {
            while (q.isEmpty()) wait();
            int v = q.remove();
            notifyAll();
            return v;
        }
    }
    public static void main(String[] args) throws Exception {
        Buffer b = new Buffer(3);
        int[] sum = {0};
        Thread prod = new Thread(() -> {
            try { for (int i = 1; i <= 20; i++) b.put(i); b.put(-1); } catch (InterruptedException e) { }
        });
        Thread cons = new Thread(() -> {
            try { int v; while ((v = b.take()) != -1) sum[0] += v; } catch (InterruptedException e) { }
        });
        prod.start(); cons.start();
        prod.join(); cons.join();
        System.out.println("sum = " + sum[0]);
        System.out.println("never more than 3 items: " + (b.maxSeen <= 3));
    }
}
```

```output
sum = 210
never more than 3 items: true
```

The consumer receives every number from 1 to 20 exactly once (the value −1 is a **poison pill** telling it to stop), so the sum is 20 × 21 / 2 = **210**, and the buffer never holds more than its capacity. In new code prefer `ArrayBlockingQueue` or `LinkedBlockingQueue`: `put` and `take` already do this waiting for you.

### Deadlock: detect it, then design it away

A **deadlock** is a permanent standstill in which each of a set of threads holds a lock that another needs. It needs all four **Coffman conditions** together: mutual exclusion, hold and wait, no pre-emption and circular wait. The program below *creates* a real deadlock between two daemon threads and uses the JVM's own `ThreadMXBean` to detect it, which is what `jstack` and `jcmd Thread.print` do when you diagnose a frozen server.

```java
import java.lang.management.*;
import java.util.*;
import java.util.concurrent.CountDownLatch;
public class Dead1 {
    static final Object A = new Object(), B = new Object();
    public static void main(String[] args) throws Exception {
        CountDownLatch bothHold = new CountDownLatch(2);
        Thread t1 = new Thread(() -> {
            synchronized (A) {
                bothHold.countDown();
                try { bothHold.await(); } catch (InterruptedException e) { }
                synchronized (B) { System.out.println("never printed"); }
            }
        }, "worker-1");
        Thread t2 = new Thread(() -> {
            synchronized (B) {
                bothHold.countDown();
                try { bothHold.await(); } catch (InterruptedException e) { }
                synchronized (A) { System.out.println("never printed"); }
            }
        }, "worker-2");
        t1.setDaemon(true); t2.setDaemon(true);
        t1.start(); t2.start();
        ThreadMXBean mx = ManagementFactory.getThreadMXBean();
        long[] ids = null;
        for (int i = 0; i < 200 && ids == null; i++) { Thread.sleep(25); ids = mx.findDeadlockedThreads(); }
        List<String> names = new ArrayList<>();
        for (ThreadInfo ti : mx.getThreadInfo(ids)) names.add(ti.getThreadName() + " waits for " + ti.getLockOwnerName());
        Collections.sort(names);
        System.out.println("deadlocked threads: " + ids.length);
        names.forEach(System.out::println);
    }
}
```

```output
deadlocked threads: 2
worker-1 waits for worker-2
worker-2 waits for worker-1
```

Thread `worker-1` holds `A` and wants `B`; `worker-2` holds `B` and wants `A`: a **cycle** in the wait-for graph, which is exactly what Figure 6.4 draws.

```svgfig label="6.4" caption="Wait-for graph of the program above. Solid arrows: holds. Dashed arrows: wants. The cycle worker-1, B, worker-2, A, worker-1 is the deadlock. If both threads took A first and then B, no cycle could form."
f = Fig(560, 230)
f.circle(110, 70, 34, fill="#bbf7d0", stroke=TEAL, label="worker-1", size=10, color=NAVY)
f.circle(450, 70, 34, fill="#fde68a", stroke=AMBER, label="worker-2", size=10, color=NAVY)
f.box(60, 170, 100, 36, "lock A", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(400, 170, 100, 36, "lock B", fill=BLUE, color=NAVY, size=12, bold=True)
f.arrow([(95, 104), (95, 170)], color=TEAL, sw=2, label="holds", lpos=(70, 138))
f.arrow([(465, 104), (465, 170)], color=AMBER, sw=2, label="holds", lpos=(495, 138))
f.arrow([(144, 76), (400, 176)], color=RED, sw=1.8, dash=True, label="wants B", lpos=(215, 118))
f.arrow([(416, 76), (160, 176)], color=RED, sw=1.8, dash=True, label="wants A", lpos=(345, 118))
f.text(280, 24, "circular wait", size=12, color=RED, bold=True)
```

The standard cures attack one Coffman condition:

| Condition removed | Technique | Example |
|---|---|---|
| Circular wait | **global lock ordering** | always lock the account with the smaller id first |
| Hold and wait | take all locks at once, or none | one coarse lock; or `tryLock` and back off |
| No pre-emption | **timed locks** that give up | `ReentrantLock.tryLock(timeout)` |
| Mutual exclusion | share nothing, or use immutable/atomic data | `AtomicLong`, copy-on-write |

The next program shows two of them: `tryLock` with a timeout (both threads give up instead of freezing) and lock ordering (two threads moving money in opposite directions finish with the right totals).

```java
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
public class Dead2 {
    static class Account {
        final int id; long balance; final ReentrantLock lock = new ReentrantLock();
        Account(int id, long b) { this.id = id; balance = b; }
    }
    static void transfer(Account from, Account to, long amt) {
        Account first = from.id < to.id ? from : to;
        Account second = first == from ? to : from;
        first.lock.lock();
        try {
            second.lock.lock();
            try { from.balance -= amt; to.balance += amt; }
            finally { second.lock.unlock(); }
        } finally { first.lock.unlock(); }
    }
    public static void main(String[] args) throws Exception {
        ReentrantLock a = new ReentrantLock(), b = new ReentrantLock();
        CountDownLatch holding = new CountDownLatch(2), finished = new CountDownLatch(2);
        ConcurrentLinkedQueue<String> log = new ConcurrentLinkedQueue<>();
        Runnable r1 = () -> attempt(a, b, "t1", holding, finished, log), r2 = () -> attempt(b, a, "t2", holding, finished, log);
        Thread t1 = new Thread(r1), t2 = new Thread(r2);
        t1.start(); t2.start(); t1.join(); t2.join();
        System.out.println(log.stream().sorted().toList());
        Account x = new Account(1, 1000), y = new Account(2, 1000);
        Thread u = new Thread(() -> { for (int i = 0; i < 500; i++) transfer(x, y, 1); });
        Thread v = new Thread(() -> { for (int i = 0; i < 300; i++) transfer(y, x, 1); });
        u.start(); v.start(); u.join(); v.join();
        System.out.println(x.balance + " " + y.balance + " total " + (x.balance + y.balance));
    }
    static void attempt(ReentrantLock mine, ReentrantLock other, String name, CountDownLatch holding, CountDownLatch finished, ConcurrentLinkedQueue<String> log) {
        mine.lock();
        try {
            holding.countDown(); holding.await();
            boolean got = other.tryLock(200, TimeUnit.MILLISECONDS);
            log.add(name + (got ? " got both" : " gave up"));
            if (got) other.unlock();
            finished.countDown(); finished.await();
        } catch (InterruptedException e) { }
        finally { mine.unlock(); }
    }
}
```

```output
[t1 gave up, t2 gave up]
800 1200 total 2000
```

Each thread in `attempt` holds one lock and cannot get the other within 200 ms, so both log "gave up" and release; with plain `synchronized` they would freeze forever. The second half uses ordering: `transfer(x, y)` and `transfer(y, x)` both lock account 1 first, so no cycle is possible; the balances are 1000 − 500 + 300 = **800** and 1000 + 500 − 300 = **1200**, and the total is conserved.

### Higher-level concurrency utilities

`java.util.concurrent` offers building blocks that replace most hand-written `wait/notify`.

| Utility | Purpose | Example use |
|---|---|---|
| `ReentrantLock` (+ `Condition`) | explicit lock with `tryLock`, timeouts and fairness; always `unlock()` in `finally` | the bank transfer above |
| `ReadWriteLock` | many readers or one writer | a cache read far more than written |
| `Semaphore(n)` | at most *n* threads inside a section | limit simultaneous downloads |
| `CountDownLatch(n)` | one-shot: wait until *n* events happened | start all workers together, or wait for all to finish |
| `CyclicBarrier(n)` | reusable meeting point for *n* threads | phased simulations |
| `ExecutorService` | thread pool; `submit`, `invokeAll`, `shutdown` | web-server request handling |
| `ConcurrentHashMap` | thread-safe map with atomic `merge`, `compute` | word counts from many threads |
| `AtomicInteger/Long` | lock-free counters via compare-and-set | request counter |
| `BlockingQueue` | producer–consumer without `wait/notify` | task queue |

::: key Four rules that prevent most concurrency bugs
1. Prefer **immutable** objects and thread confinement; share as little as possible.
2. Guard *every* access to shared mutable state (reads too) with the *same* lock, or use an atomic class.
3. When you need several locks, take them in one fixed global order and hold them briefly.
4. Use the library classes (`ExecutorService`, `BlockingQueue`, `ConcurrentHashMap`) instead of raw `Thread`, `wait` and `notify`.
:::

## 6.8 The event-delegation model in depth

In Section 6.2 you saw a button and a lambda. This section explains the model that stands behind every Swing, AWT and JavaFX program, because a TU question on "event handling" asks for the **three participants** and an example of each listener.

```svgfig label="6.5" caption="The delegation event model. The listener registers with the source once; later, every user action creates an event object that the Event Dispatch Thread delivers to each registered listener."
f = Fig(640, 200)
f.box(20, 60, 150, 60, "Event source\nJButton", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
f.box(245, 60, 150, 60, "Event object\nActionEvent", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(470, 60, 150, 60, "Event listener\nActionListener", fill="#fde68a", stroke=AMBER, color=NAVY, size=12, bold=True)
f.arrow([(470, 140), (330, 160), (95, 160), (95, 120)], color=RED, sw=1.8, dash=True, label="1  addActionListener(...)", lpos=(280, 150))
f.arrow([(170, 90), (245, 90)], color=SLATE, sw=2)
f.arrow([(395, 90), (470, 90)], color=SLATE, sw=2)
f.text(208, 78, "creates", size=10, color=NAVY, bold=True)
f.text(433, 78, "delivers", size=10, color=NAVY, bold=True)
f.text(320, 24, "2  user clicks  ->  3  EDT calls actionPerformed(event)", size=11, color=NAVY, bold=True)
f.text(545, 135, "handler code runs here", size=10, color=AMBER, bold=True)
```

1. The **event source** is the component the user touched (`JButton`, `JTextField`, `JFrame`). It keeps a list of registered listeners.
2. The **event object** (`ActionEvent`, `MouseEvent`, `KeyEvent`, `WindowEvent`, `ItemEvent`) describes what happened: which source, which key or mouse position, which modifiers.
3. The **event listener** is an object implementing a listener interface (`ActionListener`, `MouseListener`, ...). Registering it with `source.addXxxListener(listener)` is called **delegation**: the source *delegates* the handling to the listener instead of handling the event itself.

When the user acts, the operating system tells AWT, which puts an event on a queue. The single **Event Dispatch Thread (EDT)** takes events from the queue and calls the listener methods of the right source, one at a time. This is the observer pattern of Unit 7 applied to user interfaces.

| Listener (event) | Methods | Adapter | Typical source |
|---|---|---|---|
| `ActionListener` (`ActionEvent`) | `actionPerformed` | none | button, Enter key, menu item |
| `ItemListener` (`ItemEvent`) | `itemStateChanged` | none | check box, combo box |
| `MouseListener` (`MouseEvent`) | `mouseClicked`, `mousePressed`, `mouseReleased`, `mouseEntered`, `mouseExited` | `MouseAdapter` | any component |
| `MouseMotionListener` (`MouseEvent`) | `mouseMoved`, `mouseDragged` | `MouseMotionAdapter` | drawing panel |
| `KeyListener` (`KeyEvent`) | `keyPressed`, `keyReleased`, `keyTyped` | `KeyAdapter` | text field |
| `WindowListener` (`WindowEvent`) | `windowOpened`, `windowClosing`, `windowClosed`, `windowIconified`, and three more | `WindowAdapter` | the frame |
| `FocusListener` (`FocusEvent`) | `focusGained`, `focusLost` | `FocusAdapter` | form field (validate on lost focus) |
| `ListSelectionListener` | `valueChanged` | none | list or table rows |

**Adapter classes.** An interface forces you to implement *every* method. `WindowListener` has seven, but you may care only about `windowClosing`. An **adapter** class implements all methods with empty bodies, so you extend it and override just one: `addWindowListener(new WindowAdapter() { public void windowClosing(WindowEvent e) { ... } })`. Because Java has single inheritance, a class that already extends `JFrame` cannot also extend an adapter, and must use an anonymous or inner class.

**Three ways to write a handler.**

| Style | Example | Good for |
|---|---|---|
| Frame implements the interface | `class App extends JFrame implements ActionListener` | one source; simple labs, but all buttons share one method |
| Anonymous or inner class | `b.addActionListener(new ActionListener() { ... })` | a few sources, different handlers |
| Lambda or method reference | `b.addActionListener(e -> save())` | any interface with one abstract method; the modern default |

The program below runs **without a window**, because `JButton` and `DefaultTableModel` do not need a display. It uses `doClick()` to fire the same event a mouse click would, and a `TableModelListener` to show the model-view split of Swing's MVC design.

```java
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.event.*;
import java.util.*;
public class EventDemo {
    static class CounterListener implements ActionListener {
        int clicks;
        public void actionPerformed(ActionEvent e) {
            clicks++;
            System.out.println("counter listener: command=" + e.getActionCommand() + " clicks=" + clicks);
        }
    }
    public static void main(String[] args) {
        JButton ok = new JButton("Save");
        ok.setActionCommand("SAVE");
        CounterListener counter = new CounterListener();
        ok.addActionListener(counter);
        ok.addActionListener(e -> System.out.println("lambda listener: source is " + ((JButton) e.getSource()).getText()));
        ok.doClick();
        ok.doClick();
        System.out.println("listeners registered: " + ok.getActionListeners().length);
        ok.removeActionListener(counter);
        ok.doClick();
        JTextField name = new JTextField(10);
        name.addActionListener(e -> System.out.println("Enter pressed with text '" + name.getText() + "'"));
        name.setText("Sita");
        name.postActionEvent();
        JCheckBox agree = new JCheckBox("I agree");
        agree.addItemListener(e -> System.out.println("check box selected = " + (e.getStateChange() == ItemEvent.SELECTED)));
        agree.setSelected(true);
        agree.setSelected(false);
        DefaultTableModel model = new DefaultTableModel(new Object[] {"Name", "Marks"}, 0);
        model.addTableModelListener(e -> System.out.println("table changed: type=" + e.getType() + " row=" + e.getFirstRow()));
        model.addRow(new Object[] {"Sita", 82});
        model.addRow(new Object[] {"Ram", 67});
        model.setValueAt(90, 1, 1);
        int total = 0;
        for (int r = 0; r < model.getRowCount(); r++) total += (Integer) model.getValueAt(r, 1);
        System.out.println("rows=" + model.getRowCount() + " total=" + total);
    }
}
```

```output
lambda listener: source is Save
counter listener: command=SAVE clicks=1
lambda listener: source is Save
counter listener: command=SAVE clicks=2
listeners registered: 2
lambda listener: source is Save
Enter pressed with text 'Sita'
check box selected = true
check box selected = false
table changed: type=1 row=0
table changed: type=1 row=1
table changed: type=0 row=1
rows=2 total=172
```

Read the output carefully. Two listeners are registered on one button, so one click calls **both**; after `removeActionListener(counter)` only the lambda remains. Swing does not promise an order among listeners of one source, so never write code that depends on it. `postActionEvent()` on a text field behaves like pressing Enter. The table model announces each change (type 1 means insert, 0 means update) to any registered view, which is why a `JTable` redraws itself without you telling it to.

### A complete window (compile-checked)

The next program is a small mark-entry form. It cannot run on a server without a screen, so it is compiled but not executed here; run it on a desktop with `java MarkForm`. It combines layout managers (`BorderLayout` for the frame, `GridLayout` for the form), a mouse listener on the table, a window-closing confirmation and a `SwingWorker` that keeps the interface responsive.

```java
// compile-only
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
public class MarkForm extends JFrame {
    private final DefaultTableModel model = new DefaultTableModel(new Object[] {"Name", "Marks"}, 0);
    private final JLabel status = new JLabel("Ready");
    public MarkForm() {
        super("Mark entry");
        JTextField name = new JTextField(), marks = new JTextField();
        JButton add = new JButton("Add"), avg = new JButton("Average");
        JPanel form = new JPanel(new GridLayout(3, 2, 6, 6));
        form.add(new JLabel("Name")); form.add(name);
        form.add(new JLabel("Marks")); form.add(marks);
        form.add(add); form.add(avg);
        JTable table = new JTable(model);
        add.addActionListener(e -> {
            try {
                int m = Integer.parseInt(marks.getText().trim());
                if (m < 0 || m > 100) throw new NumberFormatException();
                model.addRow(new Object[] {name.getText().trim(), m});
                name.setText(""); marks.setText(""); name.requestFocus();
                status.setText("Rows: " + model.getRowCount());
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Marks must be a whole number from 0 to 100", "Invalid input", JOptionPane.WARNING_MESSAGE);
            }
        });
        avg.addActionListener(e -> new SwingWorker<Double, Void>() {
            protected Double doInBackground() {
                double s = 0;
                for (int r = 0; r < model.getRowCount(); r++) s += (Integer) model.getValueAt(r, 1);
                return model.getRowCount() == 0 ? 0.0 : s / model.getRowCount();
            }
            protected void done() {
                try { status.setText("Average = " + get()); } catch (Exception ex) { status.setText("Error"); }
            }
        }.execute());
        table.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) status.setText("Row " + (table.getSelectedRow() + 1) + " double-clicked");
            }
        });
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                if (JOptionPane.showConfirmDialog(MarkForm.this, "Exit?", "Confirm", JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION) dispose();
            }
        });
        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        add(form, BorderLayout.NORTH);
        add(new JScrollPane(table), BorderLayout.CENTER);
        add(status, BorderLayout.SOUTH);
        setSize(380, 320);
        setLocationRelativeTo(null);
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new MarkForm().setVisible(true));
    }
}
```

Points to explain in an exam: (1) validation catches `NumberFormatException` and tells the user what is wrong instead of crashing; (2) the `SwingWorker` computes in a background thread (`doInBackground`) and updates the label back on the EDT (`done`), the rule from Section 6.2; (3) the anonymous `MouseAdapter` and `WindowAdapter` override a single method each; (4) `DO_NOTHING_ON_CLOSE` plus the confirmation dialog gives the user a chance to cancel.

::: tip Sample question
**Q.** Explain the delegation event model with an example. **A.** (1) Define source, event, listener. (2) Draw the three boxes with the arrows *register* (listener to source) and *notify* (source to listener, carrying the event object). (3) Show `button.addActionListener(e -> ...)`. (4) Add that events are dispatched on the EDT one at a time, that adapters avoid empty methods, and that one source may have many listeners.
:::

## 6.9 JDBC you can run: CRUD, transactions and SQL injection

The JDBC example in 6.3 needs a database server. The program below uses **H2**, a database written in Java, in its in-memory mode: the URL `jdbc:h2:mem:neb` creates a throw-away database inside the program, so every statement really executes. For MySQL or PostgreSQL only the URL, the user name and the driver JAR change; the JDBC code is identical. (This book's checker runs it with `h2.jar` on the class path.)

```java
import java.sql.*;
public class JdbcLab {
    public static void main(String[] args) throws Exception {
        try (Connection con = DriverManager.getConnection("jdbc:h2:mem:neb;DB_CLOSE_DELAY=-1", "sa", "")) {
            try (Statement st = con.createStatement()) {
                st.execute("CREATE TABLE student(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(30) NOT NULL, marks INT CHECK (marks BETWEEN 0 AND 100))");
            }
            String ins = "INSERT INTO student(name, marks) VALUES (?, ?)";
            try (PreparedStatement ps = con.prepareStatement(ins)) {
                Object[][] rows = {{"Sita", 82}, {"Ram", 67}, {"Hari", 74}, {"Gita", 91}};
                for (Object[] r : rows) { ps.setString(1, (String) r[0]); ps.setInt(2, (Integer) r[1]); ps.addBatch(); }
                System.out.println("batch inserted " + ps.executeBatch().length + " rows");
            }
            try (PreparedStatement ps = con.prepareStatement("UPDATE student SET marks = marks + ? WHERE name = ?")) {
                ps.setInt(1, 5); ps.setString(2, "Ram");
                System.out.println("updated " + ps.executeUpdate());
            }
            try (PreparedStatement ps = con.prepareStatement("DELETE FROM student WHERE marks < ?")) {
                ps.setInt(1, 75);
                System.out.println("deleted " + ps.executeUpdate());
            }
            try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery("SELECT id, name, marks FROM student ORDER BY marks DESC")) {
                while (rs.next()) System.out.println(rs.getInt("id") + " " + rs.getString("name") + " " + rs.getInt("marks"));
            }
            con.setAutoCommit(false);
            try (Statement st = con.createStatement()) {
                st.executeUpdate("UPDATE student SET marks = 0 WHERE name = 'Sita'");
                st.executeUpdate("INSERT INTO student(name, marks) VALUES ('Bad', 150)");
                con.commit();
            } catch (SQLException e) {
                con.rollback();
                System.out.println("rolled back: constraint violated");
            }
            try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery("SELECT marks FROM student WHERE name = 'Sita'")) {
                rs.next();
                System.out.println("Sita still has " + rs.getInt(1));
            }
            con.setAutoCommit(true);
            String evil = "x' OR '1'='1";
            try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM student WHERE name = '" + evil + "'")) {
                rs.next();
                System.out.println("concatenated query matched " + rs.getInt(1) + " rows");
            }
            try (PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) FROM student WHERE name = ?")) {
                ps.setString(1, evil);
                try (ResultSet rs = ps.executeQuery()) {
                    rs.next();
                    System.out.println("prepared query matched " + rs.getInt(1) + " rows");
                }
            }
        }
    }
}
```
```output
batch inserted 4 rows
updated 1
deleted 2
4 Gita 91
1 Sita 82
rolled back: constraint violated
Sita still has 82
concatenated query matched 2 rows
prepared query matched 0 rows
```

Walk through it. Four rows are inserted in one **batch** (one round trip instead of four). Ram's 67 becomes 72 after the update, so deleting everyone below 75 removes Ram (72) and Hari (74), and the final query lists Gita 91 and Sita 82 only. The **transaction** updates Sita and then tries to insert a row that violates the `CHECK` constraint; the exception triggers `rollback()`, so Sita's mark is **still 82**: the two statements succeed or fail together (*atomicity*). Last, the **SQL injection** demonstration: concatenating the text `x' OR '1'='1` into the query turns the condition into `name = 'x' OR '1'='1'`, which is always true, so it matches *every* row, whereas the `PreparedStatement` sends the text as data, never as SQL, and matches none.

| JDBC object | Role | Remember |
|---|---|---|
| `DriverManager` / `DataSource` | creates connections (production code uses a connection pool such as HikariCP) | connections are expensive |
| `Connection` | one session; owns transactions | `setAutoCommit(false)`, `commit`, `rollback` |
| `Statement` | fixed SQL text | only for SQL without user input |
| `PreparedStatement` | precompiled SQL with `?` parameters | stops SQL injection, faster when repeated |
| `CallableStatement` | calls a stored procedure | `{call proc(?, ?)}` |
| `ResultSet` | cursor over the rows | starts *before* the first row; `next()` moves; column numbers start at 1 |
| `SQLException` | any database error | has `getSQLState()` and `getErrorCode()` |

## Formula and fact sheet

- `start()` creates a thread, `run()` does not; `join()` waits.
- `counter++` is not atomic; fix with `synchronized`, `AtomicInteger` or a lock.
- Executors reuse threads; `Future.get()` blocks; `shutdown()` at the end.
- Deadlock = mutual exclusion + hold-and-wait + no pre-emption + circular wait; break by lock ordering.
- Swing: source → event → listener; update the GUI on the EDT.
- JDBC: `PreparedStatement` with `?`, try-with-resources, transactions via `commit`/`rollback`.
- Thread states: NEW, RUNNABLE, BLOCKED (waiting for a monitor), WAITING (`wait`, `join`), TIMED_WAITING (`sleep`), TERMINATED. `interrupt()` wakes a sleeper with `InterruptedException`.
- `wait()` must be called in a `synchronized` block and inside a `while` loop; `notifyAll()` wakes all waiters. Prefer `BlockingQueue`.
- Deadlock needs mutual exclusion, hold and wait, no pre-emption and circular wait; cure by lock ordering, `tryLock(timeout)`, or fewer locks. Detect with `jstack` or `ThreadMXBean.findDeadlockedThreads()`.
- Delegation event model: source, event object, listener; listeners register with `addXxxListener`; events are dispatched one at a time on the EDT; adapters implement all methods with empty bodies.
- JDBC: `PreparedStatement` for every statement with user input; `setAutoCommit(false)`, `commit`, `rollback` for atomic changes; `ResultSet` columns count from 1.

## Chapter summary

- Threads give concurrency, but shared mutable state needs synchronisation to avoid races and deadlocks.
- Executors, atomics and concurrent collections are safer than raw threads and locks.
- GUI programs are event driven: components register listeners and long work moves off the UI thread.
- JDBC connects Java to SQL databases; prepared statements and transactions make it safe.
- A real project combines classes, interfaces, generics, collections, exceptions, I/O, threads and a database.
- Correct concurrent code needs the right lock, the right waiting condition and a fixed lock order.
- Swing handles every user action by delegating an event object to registered listeners on the EDT.
- JDBC programs use prepared statements and transactions; the H2 in-memory database lets you run them anywhere.

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
11. Name the six thread states and give one situation for each.
12. Why must `wait()` be called in a loop and inside `synchronized`? What is the difference between `notify()` and `notifyAll()`?
13. State the four conditions for deadlock. Show code that deadlocks and two different ways to prevent it.
14. Explain the delegation event model. What is an adapter class and why does `WindowAdapter` exist?
15. Write the code for a button that increments a counter label and a window that asks for confirmation before closing.
16. Why should long-running work not run inside an `ActionListener`? Name the class that solves this.
17. Using JDBC, show how to transfer Rs 500 between two accounts so that both updates succeed or neither does.
18. Show how the input `x' OR '1'='1` breaks a concatenated query and how `PreparedStatement` prevents it.

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
**11.** NEW: created, not started. RUNNABLE: executing or ready. BLOCKED: waiting to enter a synchronized block held by another thread. WAITING: in `wait()` or `join()`. TIMED_WAITING: in `sleep(ms)`. TERMINATED: `run()` has finished.
**12.** `wait()` releases the monitor and requires you to own it, hence `synchronized` (otherwise `IllegalMonitorStateException`). The condition must be re-checked in a `while` loop because of spurious wake-ups and because another thread may have changed the state first. `notify()` wakes one waiting thread, `notifyAll()` wakes all; `notifyAll()` is safer when different waiters wait for different conditions.
**13.** Mutual exclusion, hold and wait, no pre-emption, circular wait. Code: thread 1 locks A then B, thread 2 locks B then A. Prevention: always lock in the same global order (by account id), or use `ReentrantLock.tryLock(timeout)` and back off.
**14.** A source (button) creates an event object when the user acts and passes it to every registered listener, which handles it. Because an interface forces all methods, an adapter class provides empty bodies so you override only the ones you need (`windowClosing` alone).
**15.** Counter: `int[] c = {0}; button.addActionListener(e -> label.setText("Clicks: " + (++c[0])));`. Closing: `setDefaultCloseOperation(DO_NOTHING_ON_CLOSE); addWindowListener(new WindowAdapter() { public void windowClosing(WindowEvent e) { if (JOptionPane.showConfirmDialog(frame, "Exit?") == JOptionPane.YES_OPTION) frame.dispose(); } });`.
**16.** The listener runs on the single EDT; if it blocks, no repaint or other event is processed and the window freezes. Use `SwingWorker` (`doInBackground` off the EDT, `done` back on it).
**17.** `con.setAutoCommit(false); try { debit.executeUpdate(); credit.executeUpdate(); con.commit(); } catch (SQLException e) { con.rollback(); }`, both statements being `PreparedStatement`s.
**18.** `"... WHERE name = '" + in + "'"` becomes `name = 'x' OR '1'='1'`, which is always true and returns every row. A `PreparedStatement` sends the text as a parameter value, never as SQL, so it matches only a name literally equal to that string.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a thread? Explain how threads are created and why synchronisation is needed, with a program.**

*Introduction.* A thread is a lightweight path of execution within a process. Threads of one program share memory, so they communicate easily but can interfere with each other.

*Creating threads.*

1. **Implement `Runnable`** (preferred): pass the object to `new Thread(r)` and call `start()`.
2. **Extend `Thread`** and override `run()`; this uses up the single inheritance slot.
3. **Executor framework:** `ExecutorService` keeps a pool of threads and returns `Future` results.
4. `start()` creates the new thread; calling `run()` directly would run in the current thread.

*Why synchronisation.* `count++` is three steps (read, add, write). If two threads interleave, one update is lost: a **race condition** (Figure 6.1 shows the states a waiting thread passes through). A `synchronized` block lets one thread at a time enter, so the steps cannot interleave.

```java
import java.util.*;
import java.util.concurrent.*;

public class RaceDemo {
    static int unsafe = 0, safe = 0;
    static final Object lock = new Object();
    public static void main(String[] args) throws Exception {
        Runnable job = () -> {
            for (int i = 0; i < 100000; i++) {
                unsafe++;
                synchronized (lock) { safe++; }
            }
        };
        Thread t1 = new Thread(job), t2 = new Thread(job);
        t1.start(); t2.start(); t1.join(); t2.join();
        System.out.println("synchronised counter = " + safe);
        System.out.println("unsynchronised never exceeds it: " + (unsafe <= 200000));
        ExecutorService pool = Executors.newFixedThreadPool(4);
        List<Future<Long>> parts = new ArrayList<>();
        for (int p = 0; p < 4; p++) {
            final int lo = p * 250 + 1, hi = lo + 249;
            parts.add(pool.submit(() -> { long s = 0; for (int i = lo; i <= hi; i++) s += (long) i * i; return s; }));
        }
        long total = 0;
        for (Future<Long> f : parts) total += f.get();
        pool.shutdown();
        System.out.println("sum of squares 1..1000 = " + total);
    }
}
```

```output
synchronised counter = 200000
unsynchronised never exceeds it: true
sum of squares 1..1000 = 333833500
```

*Conclusion.* The synchronised counter is always exactly 200000, while the unsynchronised one is usually smaller. Use threads for responsiveness and speed, and protect shared data with locks or atomic classes.

**Q2 (10 marks). Explain the steps of JDBC with a program, the role of `PreparedStatement`, and transactions.**

*Introduction.* JDBC (Java Database Connectivity) is the standard API for relational databases. It hides each database's protocol behind common interfaces and a driver (Figure 6.2).

*Steps.*

1. **Driver.** Put the driver JAR on the classpath; modern JDBC loads it automatically from the URL.
2. **Connection.** `DriverManager.getConnection(url, user, password)`.
3. **Statement.** Create a `Statement` for fixed SQL or a `PreparedStatement` with `?` placeholders.
4. **Execute.** `executeUpdate` for INSERT/UPDATE/DELETE; `executeQuery` returns a `ResultSet`.
5. **Process.** Loop `while (rs.next())` and read columns with `getString`, `getInt`.
6. **Close.** try-with-resources closes the connection, statement and result set.
7. **Prepared statements** are precompiled and treat input as data, which prevents SQL injection.
8. **Transactions.** `setAutoCommit(false)`, then `commit()` on success or `rollback()` on failure.

```java
import java.sql.*;

public class JdbcDemo {
    public static void main(String[] args) throws Exception {
        try (Connection con = DriverManager.getConnection("jdbc:h2:mem:college")) {
            try (Statement st = con.createStatement()) {
                st.execute("CREATE TABLE student(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(30), marks INT)");
            }
            con.setAutoCommit(false);
            try (PreparedStatement ins = con.prepareStatement("INSERT INTO student(name, marks) VALUES (?, ?)")) {
                String[] n = {"Sita", "Ram", "Hari"}; int[] m = {88, 72, 45};
                for (int i = 0; i < 3; i++) { ins.setString(1, n[i]); ins.setInt(2, m[i]); ins.addBatch(); }
                ins.executeBatch();
            }
            con.commit();
            try (PreparedStatement q = con.prepareStatement("SELECT name, marks FROM student WHERE marks >= ? ORDER BY marks DESC")) {
                q.setInt(1, 60);
                try (ResultSet rs = q.executeQuery()) {
                    while (rs.next()) System.out.println(rs.getString("name") + " " + rs.getInt("marks"));
                }
            }
            try (PreparedStatement q = con.prepareStatement("SELECT COUNT(*) FROM student WHERE name = ?")) {
                q.setString(1, "x' OR '1'='1");
                try (ResultSet rs = q.executeQuery()) { rs.next(); System.out.println("injection attempt matches " + rs.getInt(1) + " rows"); }
            }
            try (Statement st = con.createStatement()) {
                st.executeUpdate("INSERT INTO student(name, marks) VALUES ('Temp', 1)");
                con.rollback();
                ResultSet rs = st.executeQuery("SELECT COUNT(*), AVG(marks) FROM student");
                rs.next(); System.out.println("after rollback: " + rs.getInt(1) + " rows, average " + rs.getInt(2));
            }
        }
    }
}
```

```output
Sita 88
Ram 72
injection attempt matches 0 rows
after rollback: 3 rows, average 68
```

| Feature | `Statement` | `PreparedStatement` |
|---|---|---|
| SQL | text built by concatenation | `?` placeholders |
| Injection | vulnerable | safe |
| Reuse | parsed each time | precompiled, batchable |

*Conclusion.* JDBC connects Java to any relational database through one API. Use prepared statements for safety and transactions to keep related changes all-or-nothing.

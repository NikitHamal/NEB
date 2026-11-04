---
subject: Advanced Java Programming
grade: BCA Semester 5
unit: 3
title: Database Programming with JDBC
hours: 9
area: BCA 303 · Advanced Java Programming · Unit 3
---

Almost every business application is a front end to a database. **JDBC** (Java Database Connectivity) is the standard Java API for talking to relational databases: you send SQL, you read the rows back, and you do it the same way whether the engine is MySQL, PostgreSQL, Oracle or the embedded SQLite used for all the programs in this unit. Every listing here was compiled and run against a real database through a real JDBC driver (the Xerial SQLite driver, SQLite 3.40); the output shown is what the database returned.

::: key What this unit gives you
- JDBC architecture, driver types and the connection steps.
- `Statement`, `PreparedStatement` and `CallableStatement`; `ResultSet` and metadata.
- Transactions: commit, rollback, isolation; batch updates.
- Disconnected data with `RowSet`; the DAO pattern; avoiding SQL injection.
:::

## 3.1 JDBC architecture

The application uses the interfaces of **`java.sql`** (`Connection`, `Statement`, `ResultSet`); the **`DriverManager`** (or a `DataSource`) finds a **driver**, a library written by the database vendor that implements those interfaces for its own wire protocol. Changing database means changing the driver and the URL, not the code, as long as the SQL is portable.

| Driver type | Description | Today |
|---|---|---|
| Type 1 | JDBC–ODBC bridge | removed from Java 8 |
| Type 2 | native API: Java calls the vendor's C library | rare |
| Type 3 | network protocol: talks to a middle-tier server | rare |
| Type 4 | **pure Java**, speaks the database's protocol directly | standard (MySQL Connector/J, PostgreSQL JDBC, Xerial SQLite) |

### The steps of a JDBC program

1. **Load the driver**: automatic since JDBC 4 if the driver jar is on the classpath (`Class.forName("org.sqlite.JDBC")` is only needed for very old drivers).
2. **Open a connection**: `DriverManager.getConnection(url, user, password)`. URLs: `jdbc:mysql://localhost:3306/college`, `jdbc:postgresql://localhost/college`, `jdbc:sqlite:college.db`, `jdbc:sqlite::memory:`.
3. **Create a statement** from the connection.
4. **Execute** SQL: `executeQuery` (SELECT → `ResultSet`), `executeUpdate` (INSERT/UPDATE/DELETE/DDL → row count), `execute` (anything).
5. **Process the results** row by row.
6. **Close** result set, statement and connection (use try-with-resources).

## 3.2 Statements, PreparedStatements and ResultSets

- **`Statement`**: executes a fixed SQL string. Fine for static SQL, dangerous with user input.
- **`PreparedStatement`**: SQL with `?` placeholders, **precompiled** once and executed many times with different parameters set by `setInt(1, …)`, `setString(2, …)`. It is faster for repeated use, handles quoting and types, and **prevents SQL injection**.
- **`CallableStatement`**: calls a database **stored procedure** or function: `{call raise_marks(?, ?)}`, with `registerOutParameter` for results. (SQLite has no stored procedures, so the syntax is described here but not executed; MySQL and PostgreSQL support it.)
- **`ResultSet`**: a cursor over the result rows. `next()` moves to the next row (initially before the first) and returns false at the end; `getInt("marks")` or `getString(1)` reads columns by name or by 1-based index; `wasNull()` tests for SQL NULL. By default a `ResultSet` is forward-only and read-only; `TYPE_SCROLL_INSENSITIVE` and `CONCUR_UPDATABLE` allow `absolute(n)`, `previous()` and `updateRow()` where the driver supports them.
- **`ResultSetMetaData`** reports the number, names and types of the columns, and **`DatabaseMetaData`** describes the database itself (tables, driver version).

```java
import java.sql.*;
public class JdbcBasics {
    public static void main(String[] args) throws SQLException {
        try (Connection con = DriverManager.getConnection("jdbc:sqlite::memory:")) {
            try (Statement st = con.createStatement()) {
                st.executeUpdate("CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, program TEXT, marks INTEGER)");
            }
            String sql = "INSERT INTO student(name, program, marks) VALUES (?, ?, ?)";
            try (PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
                Object[][] rows = {{"Ram", "BCA", 72}, {"Sita", "BCA", 91}, {"Hari", "BBA", 64}, {"Gita", "BCA", 85}};
                for (Object[] r : rows) { ps.setString(1, (String) r[0]); ps.setString(2, (String) r[1]); ps.setInt(3, (Integer) r[2]); ps.executeUpdate(); }
                try (ResultSet keys = ps.getGeneratedKeys()) { keys.next(); System.out.println("last generated id = " + keys.getInt(1)); }
            }
            try (PreparedStatement ps = con.prepareStatement("SELECT id, name, marks FROM student WHERE program = ? AND marks >= ? ORDER BY marks DESC")) {
                ps.setString(1, "BCA"); ps.setInt(2, 80);
                try (ResultSet rs = ps.executeQuery()) {
                    ResultSetMetaData md = rs.getMetaData();
                    System.out.println("columns: " + md.getColumnCount() + " first = " + md.getColumnName(1));
                    while (rs.next()) System.out.println(rs.getInt("id") + " " + rs.getString("name") + " " + rs.getInt("marks"));
                }
            }
            try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery("SELECT program, COUNT(*) AS n, AVG(marks) AS avg FROM student GROUP BY program ORDER BY program")) {
                while (rs.next()) System.out.printf("%s: %d students, average %.2f%n", rs.getString("program"), rs.getInt("n"), rs.getDouble("avg"));
            }
            try (Statement st = con.createStatement()) {
                System.out.println("rows updated: " + st.executeUpdate("UPDATE student SET marks = marks + 5 WHERE marks < 70"));
            }
        }
    }
}
```
```output
last generated id = 4
columns: 3 first = id
2 Sita 91
4 Gita 85
BBA: 1 students, average 64.00
BCA: 3 students, average 82.67
rows updated: 1
```
The generated key is that of the last inserted row (4). Placeholders are 1-based. The update row count (1: Hari's 64) comes from `executeUpdate`.

## 3.3 SQL injection and why we use PreparedStatement

Building SQL by joining strings lets the user's input become part of the SQL. Suppose the login query is `"SELECT * FROM users WHERE name='" + name + "' AND pw='" + pw + "'"`. Two classic attacks:

- **Comment injection**: the user types `admin' --` as the name and anything as the password. The query becomes `... WHERE name='admin' --' AND pw='x'`; everything after `--` is an SQL comment, so the password test disappears and the attacker is logged in as admin.
- **Tautology injection**: typing `' OR '1'='1` in *both* fields gives `WHERE name='' OR '1'='1' AND pw='' OR '1'='1'`, which is true for every row.

(Typing the tautology in the name field only does *not* work here, because AND binds tighter than OR and the password test `'1'='1' AND pw='x'` still fails; this is one of the points the program below found when it was run.) A prepared statement sends the SQL and the values separately, so the input is always treated as data.

```java
import java.sql.*;
public class InjectionDemo {
    static int unsafeCount(Statement st, String name, String pw) throws SQLException {
        String q = "SELECT COUNT(*) FROM users WHERE name='" + name + "' AND pw='" + pw + "'";
        try (ResultSet rs = st.executeQuery(q)) { rs.next(); return rs.getInt(1); }
    }
    public static void main(String[] args) throws SQLException {
        try (Connection con = DriverManager.getConnection("jdbc:sqlite::memory:"); Statement st = con.createStatement()) {
            st.executeUpdate("CREATE TABLE users (name TEXT, pw TEXT)");
            st.executeUpdate("INSERT INTO users VALUES ('admin', 's3cret'), ('ram', 'pass')");
            System.out.println("wrong password, honest input    : " + unsafeCount(st, "admin", "x") + " rows");
            System.out.println("comment injection  admin' --     : " + unsafeCount(st, "admin' --", "x") + " rows");
            System.out.println("tautology in name only          : " + unsafeCount(st, "' OR '1'='1", "x") + " rows");
            System.out.println("tautology in both fields        : " + unsafeCount(st, "' OR '1'='1", "' OR '1'='1") + " rows");
            try (PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) FROM users WHERE name = ? AND pw = ?")) {
                for (String[] in : new String[][]{{"admin' --", "x"}, {"' OR '1'='1", "' OR '1'='1"}}) {
                    ps.setString(1, in[0]); ps.setString(2, in[1]);
                    try (ResultSet rs = ps.executeQuery()) { rs.next(); System.out.println("prepared statement, input " + in[0] + " : " + rs.getInt(1) + " rows"); }
                }
            }
        }
    }
}
```
```output
wrong password, honest input    : 0 rows
comment injection  admin' --     : 1 rows
tautology in name only          : 0 rows
tautology in both fields        : 2 rows
prepared statement, input admin' -- : 0 rows
prepared statement, input ' OR '1'='1 : 0 rows
```
With string concatenation the comment injection returns 1 row (the admin account, without its password) and the double tautology returns both rows; the prepared statement matches none. Also store **password hashes** (bcrypt, Argon2), never plaintext as in this teaching table.

## 3.4 Transactions

A **transaction** is a group of statements that must succeed or fail as a unit (ACID: atomicity, consistency, isolation, durability). A bank transfer subtracts from one account and adds to another; if only the first happens, money vanishes. By default JDBC runs in **auto-commit** mode (each statement is its own transaction). For a multi-statement transaction: `con.setAutoCommit(false)`, run the statements, then `con.commit()`, or `con.rollback()` in a `catch` block; restore auto-commit afterwards.

```java
import java.sql.*;
public class TransactionDemo {
    static void transfer(Connection con, int from, int to, int amount) throws SQLException {
        con.setAutoCommit(false);
        try (PreparedStatement debit = con.prepareStatement("UPDATE account SET balance = balance - ? WHERE id = ?");
             PreparedStatement credit = con.prepareStatement("UPDATE account SET balance = balance + ? WHERE id = ?")) {
            debit.setInt(1, amount); debit.setInt(2, from); debit.executeUpdate();
            credit.setInt(1, amount); credit.setInt(2, to); credit.executeUpdate();
            try (Statement chk = con.createStatement(); ResultSet rs = chk.executeQuery("SELECT balance FROM account WHERE id = " + from)) {
                rs.next(); if (rs.getInt(1) < 0) throw new SQLException("insufficient funds");
            }
            con.commit(); System.out.println("transfer of " + amount + " committed");
        } catch (SQLException ex) {
            con.rollback(); System.out.println("transfer of " + amount + " rolled back: " + ex.getMessage());
        } finally { con.setAutoCommit(true); }
    }
    static void show(Connection con) throws SQLException {
        try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery("SELECT id, balance FROM account ORDER BY id")) {
            StringBuilder sb = new StringBuilder("balances:");
            while (rs.next()) sb.append(" [").append(rs.getInt(1)).append("]=").append(rs.getInt(2));
            System.out.println(sb);
        }
    }
    public static void main(String[] args) throws SQLException {
        try (Connection con = DriverManager.getConnection("jdbc:sqlite::memory:"); Statement st = con.createStatement()) {
            st.executeUpdate("CREATE TABLE account (id INTEGER PRIMARY KEY, balance INTEGER NOT NULL)");
            st.executeUpdate("INSERT INTO account VALUES (1, 500), (2, 300)");
            show(con); transfer(con, 1, 2, 200); show(con); transfer(con, 1, 2, 400); show(con);
        }
    }
}
```
```output
balances: [1]=500 [2]=300
transfer of 200 committed
balances: [1]=300 [2]=500
transfer of 400 rolled back: insufficient funds
balances: [1]=300 [2]=500
```
The first transfer leaves 300 and 500; the second would overdraw account 1 (300 − 400 < 0), so the exception triggers `rollback()` and the balances are unchanged. **Isolation levels** (`con.setTransactionIsolation(...)`): READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE, in increasing protection against dirty reads, non-repeatable reads and phantom reads and increasing cost. **Savepoints** (`con.setSavepoint()`, `rollback(savepoint)`) allow partial rollback where the driver supports them.

## 3.5 Batch updates and metadata

Sending 1,000 inserts one by one costs 1,000 round trips; **batching** queues them with `addBatch()` and sends them together with `executeBatch()`, which returns an `int[]` of update counts. Combine batching with a transaction for speed.

```java
import java.sql.*;
public class BatchDemo {
    public static void main(String[] args) throws SQLException {
        try (Connection con = DriverManager.getConnection("jdbc:sqlite::memory:")) {
            con.createStatement().executeUpdate("CREATE TABLE sq (n INTEGER PRIMARY KEY, square INTEGER)");
            con.setAutoCommit(false);
            try (PreparedStatement ps = con.prepareStatement("INSERT INTO sq VALUES (?, ?)")) {
                for (int i = 1; i <= 1000; i++) { ps.setInt(1, i); ps.setInt(2, i * i); ps.addBatch(); }
                int[] counts = ps.executeBatch();
                int total = 0; for (int c : counts) total += c;
                System.out.println("batch statements: " + counts.length + ", rows affected: " + total);
            }
            con.commit();
            try (ResultSet rs = con.createStatement().executeQuery("SELECT COUNT(*), SUM(square), MAX(square) FROM sq")) {
                rs.next(); System.out.println("count=" + rs.getInt(1) + " sum=" + rs.getLong(2) + " max=" + rs.getInt(3));
            }
            DatabaseMetaData dm = con.getMetaData();
            System.out.println("product: " + dm.getDatabaseProductName() + ", driver: " + dm.getDriverName());
            try (ResultSet t = dm.getTables(null, null, "sq", null)) { while (t.next()) System.out.println("table found: " + t.getString("TABLE_NAME")); }
        }
    }
}
```
```output
batch statements: 1000, rows affected: 1000
count=1000 sum=333833500 max=1000000
product: SQLite, driver: SQLite JDBC
table found: sq
```
The sum of the squares 1² + … + 1000² is 1000 × 1001 × 2001 / 6 = 333,833,500, matching the database's answer.

## 3.6 RowSets: connected and disconnected data

A **`RowSet`** (package `javax.sql.rowset`) is a JavaBean-style `ResultSet` that can be **disconnected**. A **`CachedRowSet`** copies the rows into memory, so the connection can be closed and the data can still be scrolled, edited and later written back with `acceptChanges(connection)`; it is ideal for a GUI table or for passing data between layers. Other kinds: `JdbcRowSet` (connected, scrollable and updatable wrapper), `WebRowSet` (serialises to XML), `FilteredRowSet` (applies a filter) and `JoinRowSet` (joins in memory).

```java
import java.sql.*;
import javax.sql.rowset.*;
public class RowSetDemo {
    public static void main(String[] args) throws SQLException {
        CachedRowSet crs = RowSetProvider.newFactory().createCachedRowSet();
        try (Connection con = DriverManager.getConnection("jdbc:sqlite::memory:"); Statement st = con.createStatement()) {
            st.executeUpdate("CREATE TABLE city (name TEXT, population INTEGER)");
            st.executeUpdate("INSERT INTO city VALUES ('Kathmandu', 1000000), ('Pokhara', 520000), ('Biratnagar', 240000)");
            try (ResultSet rs = st.executeQuery("SELECT name, population FROM city ORDER BY population DESC")) { crs.populate(rs); }
        }
        System.out.println("connection closed; rows cached: " + crs.size());
        crs.beforeFirst();
        while (crs.next()) System.out.println(crs.getString("name") + " " + crs.getInt("population"));
        crs.absolute(2); System.out.println("row 2 = " + crs.getString(1));
        crs.last(); System.out.println("last row = " + crs.getString(1) + ", row number " + crs.getRow());
        crs.previous(); System.out.println("previous = " + crs.getString(1));
    }
}
```
```output
connection closed; rows cached: 3
Kathmandu 1000000
Pokhara 520000
Biratnagar 240000
row 2 = Pokhara
last row = Biratnagar, row number 3
previous = Pokhara
```
The rows can be scrolled in both directions after the connection is closed. (Writing changes back with `acceptChanges` needs a driver whose metadata identifies the table; it is left out here.)

## 3.7 The DAO pattern and connection pools

The **Data Access Object** pattern keeps SQL out of the rest of the program: a `StudentDao` interface offers `insert`, `findById`, `findAll`, `delete`, and one implementation does the JDBC work, so the GUI or servlet never sees a `Connection`. It makes the database replaceable and the logic testable.

```java
import java.sql.*;
import java.util.*;
public class DaoDemo {
    record Student(int id, String name, int marks) {}
    static class StudentDao {
        private final Connection con;
        StudentDao(Connection con) throws SQLException {
            this.con = con;
            try (Statement st = con.createStatement()) { st.executeUpdate("CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY, name TEXT, marks INTEGER)"); }
        }
        void insert(Student s) throws SQLException {
            try (PreparedStatement ps = con.prepareStatement("INSERT INTO student VALUES (?, ?, ?)")) { ps.setInt(1, s.id()); ps.setString(2, s.name()); ps.setInt(3, s.marks()); ps.executeUpdate(); }
        }
        Optional<Student> findById(int id) throws SQLException {
            try (PreparedStatement ps = con.prepareStatement("SELECT id, name, marks FROM student WHERE id = ?")) {
                ps.setInt(1, id);
                try (ResultSet rs = ps.executeQuery()) { return rs.next() ? Optional.of(new Student(rs.getInt(1), rs.getString(2), rs.getInt(3))) : Optional.empty(); }
            }
        }
        List<Student> findAll() throws SQLException {
            List<Student> list = new ArrayList<>();
            try (Statement st = con.createStatement(); ResultSet rs = st.executeQuery("SELECT id, name, marks FROM student ORDER BY id")) {
                while (rs.next()) list.add(new Student(rs.getInt(1), rs.getString(2), rs.getInt(3)));
            }
            return list;
        }
        boolean delete(int id) throws SQLException {
            try (PreparedStatement ps = con.prepareStatement("DELETE FROM student WHERE id = ?")) { ps.setInt(1, id); return ps.executeUpdate() == 1; }
        }
    }
    public static void main(String[] args) throws SQLException {
        try (Connection con = DriverManager.getConnection("jdbc:sqlite::memory:")) {
            StudentDao dao = new StudentDao(con);
            dao.insert(new Student(1, "Ram", 72)); dao.insert(new Student(2, "Sita", 91)); dao.insert(new Student(3, "Hari", 64));
            System.out.println(dao.findAll());
            System.out.println("find 2: " + dao.findById(2).map(Student::name).orElse("none") + ", find 9: " + dao.findById(9).map(Student::name).orElse("none"));
            System.out.println("deleted 1: " + dao.delete(1) + ", deleted 1 again: " + dao.delete(1));
            System.out.println("remaining: " + dao.findAll().size());
        }
    }
}
```
```output
[Student[id=1, name=Ram, marks=72], Student[id=2, name=Sita, marks=91], Student[id=3, name=Hari, marks=64]]
find 2: Sita, find 9: none
deleted 1: true, deleted 1 again: false
remaining: 2
```
Opening a connection is slow (network handshake, authentication), so servers use a **connection pool** (a `DataSource` such as HikariCP, Apache DBCP or the server's own) that keeps connections open and lends them out; `close()` on a pooled connection returns it to the pool instead of closing it. In a servlet container the pool is configured in the server and obtained through **JNDI**: `DataSource ds = (DataSource) new InitialContext().lookup("java:comp/env/jdbc/College")`.

## 3.8 Seeing the ideas: drivers, cursors, transactions and pools

JDBC code looks like a list of method calls, but behind the calls there are layers, cursors, locks and queues. Plate 3.1 shows the people who made the relational model, SQL, SQLite and transactions practical. Plate 3.2 gives four everyday pictures: an adapter for the driver, toll booths and swimming lanes for the connection pool, and a passbook for the transaction record. Plate 3.3 shows an ATM, a rack of database servers and the anatomy of a JDBC URL. Figures 3.1 to 3.14 then show the layers, the cursor, the timings and the transaction behaviour, using numbers from real runs of Java 17 with the Xerial SQLite driver 3.45.3.0.

```photogrid label="3.1" cols="4" ratio="1.0" caption="People behind the tools of this unit. (a) Don Chamberlin (CC BY-SA 4.0), who with Raymond Boyce designed SEQUEL, later called SQL, at IBM in 1974. (b) Raymond Boyce at 25 (CC BY-SA 4.0), co-designer of SQL and of Boyce-Codd normal form, who died in 1974 at the age of 26. (c) D. Richard Hipp (CC BY 2.0), author of SQLite, the database engine inside every real run in this unit. (d) Jim Gray (CC BY-SA 3.0 us), who made the transaction (ACID) a precise engineering idea and won the Turing Award in 1998."
@ photo id="bca303/chamberlin" cap="Don Chamberlin, SQL"
fit 1.0
focus 0.4 0.8
@ photo id="bca303/boyce" cap="Raymond Boyce, SQL"
fit 1.0
focus 0.5 0.55
@ photo id="bca303/hipp" cap="D. Richard Hipp, SQLite"
fit 1.0
focus 0.5 0.55
@ photo id="bca202/jimgray" cap="Jim Gray, transactions"
fit 1.0
focus 0.5 0.6
```

```svgfig label="3.1" caption="The layers of JDBC. Your code calls only the interfaces of java.sql; DriverManager chooses a driver by the prefix of the URL; the driver translates the calls into the protocol of one database. A real run listed exactly 1 registered driver, org.sqlite.JDBC version 3.45, and the connection reported product SQLite 3.45.3, auto-commit true and isolation level 8 (SERIALIZABLE)."
f = Fig(580, 262)
drivers = ["org.sqlite.JDBC"]
assert len(drivers) == 1
f.text(180, 14, "from your code down to the database", size=11.5, color=NAVY, bold=True)
rows = [("Your Java program (the application)", BLUE, NAVY), ("java.sql interfaces: Connection, Statement, ResultSet", MINT, TEAL), ("DriverManager: matches the URL prefix", SAND, AMBER), ("Driver jar (type 4, pure Java)", MINT, TEAL), ("Database engine: SQLite, MySQL, PostgreSQL", SOFT, SLATE)]
for i, (t, fl, st) in enumerate(rows):
    y = 28 + i * 46
    f.box(10, y, 340, 32, t, fill=fl, stroke=st, size=10, bold=True)
    if i < 4:
        f.arrow([(180, y + 32), (180, y + 46)], color=SLATE, both=True)
f.box(372, 28, 200, 100, "", fill="#ffffff", stroke=SLATE)
f.text(472, 44, "the real run printed", size=10.5, color=NAVY, bold=True)
for i, t in enumerate(["drivers listed: 1", "class: org.sqlite.JDBC v3.45", "product: SQLite 3.45.3", "auto-commit: true", "isolation: 8 = SERIALIZABLE"]):
    f.text(382, 64 + i * 15, t, size=9.5, color=SLATE, anchor="start")
f.box(372, 140, 200, 106, "", fill=SAND, stroke=AMBER)
f.text(472, 156, "same code, other database", size=10.5, color=AMBER, bold=True)
for i, t in enumerate(["jdbc:sqlite:college.db", "jdbc:mysql://localhost:3306/college", "jdbc:postgresql://localhost/college", "change the jar and the URL;", "the rest of the code stays"]):
    f.text(382, 176 + i * 15, t, size=9.5, color=SLATE, anchor="start")
```

```svgfig label="3.2" caption="The four driver types as stacks between the program and the database. Type 1 needs three layers in between (bridge, ODBC, native client), type 2 needs two, type 3 needs two (driver and middleware server) and type 4 needs only the driver itself, which speaks the database protocol, so it is the standard today (MySQL Connector/J, PostgreSQL JDBC, Xerial SQLite). The counts are computed from the stacks."
f = Fig(580, 276)
stacks = [("Type 1", ["JDBC-ODBC bridge", "ODBC driver", "native client"], "removed in Java 8", RED, ROSE),
          ("Type 2", ["JDBC driver (Java + C)", "native client library"], "rare", AMBER, SAND),
          ("Type 3", ["JDBC driver (Java)", "middleware server"], "rare", AMBER, SAND),
          ("Type 4", ["JDBC driver (pure Java)"], "standard today", TEAL, MINT)]
for i, (nm, layers, note, st, fl) in enumerate(stacks):
    x = 8 + i * 143
    f.text(x + 65, 14, nm, size=12, color=st, bold=True)
    f.box(x, 24, 130, 26, "Java application", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
    y = 62
    for t in layers:
        f.arrow([(x + 65, y - 12), (x + 65, y)], color=SLATE)
        f.box(x, y, 130, 26, t, fill=fl, stroke=st, size=9.5, bold=True)
        y += 38
    f.arrow([(x + 65, y - 12), (x + 65, y)], color=SLATE)
    f.box(x, y, 130, 26, "Database", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
    f.text(x + 65, 222, "%d layer%s in between" % (len(layers), "" if len(layers) == 1 else "s"), size=10, color=st, bold=True)
    f.text(x + 65, 238, note, size=9.5, color=SLATE)
f.text(290, 262, "Fewer layers means fewer parts to install and to fail: use a type 4 driver", size=10, color=NAVY, bold=True)
```

```photogrid label="3.2" cols="4" ratio="1.3" caption="Everyday pictures for JDBC ideas. (a) A plug adapter (CC0): the program's plug stays the same and the adapter, like a driver, fits it to a different socket. (b) Toll booths on a Chinese expressway (CC BY-SA 3.0): a few booths serve many cars, like a few pooled connections serving many requests. (c) Swimming lanes (CC BY-SA 4.0): a fixed number of lanes, and swimmers wait when all are in use, like a pool of size 3. (d) A post-office savings passbook (CC BY-SA 4.0): every deposit and withdrawal is written in a permanent record, as a commit is."
@ photo id="bca303/adapter" cap="Plug adapter: the driver"
fit 1.3
focus 0.55 0.5
call 0.62 0.9 0.35 0.55 "adapter"
@ photo id="bca303/toll" cap="Toll booths: a pool"
fit 1.3
focus 0.5 0.5
@ photo id="bca303/pool" cap="Swimming lanes: pool size"
fit 1.3
focus 0.55 0.5
@ photo id="bca303/passbook" cap="Passbook: committed record"
fit 1.3
focus 0.5 0.5
```

```svgfig label="3.3" caption="The six steps of a JDBC program and what can go wrong at each step, with real error values. A URL with no driver gave SQLState 08001 ('No suitable driver found'). A misspelt SELEKT gave error code 1 (syntax error near SELEKT), a missing table gave code 1 (no such table) and a duplicate e-mail gave code 19 (UNIQUE constraint failed). Reading a SQL NULL with getInt returned 0 and wasNull() returned true."
f = Fig(580, 262)
steps = [("1 Driver", "jar on the\nclasspath"), ("2 Connect", "DriverManager\n.getConnection"), ("3 Statement", "create or\nprepare"), ("4 Execute", "executeQuery\nexecuteUpdate"), ("5 Process", "while\n(rs.next())"), ("6 Close", "try-with-\nresources")]
for i, (a, b) in enumerate(steps):
    x = 6 + i * 96
    f.box(x, 22, 88, 30, a, fill=BLUE, stroke=NAVY, size=10, bold=True)
    f.box(x, 62, 88, 36, b, fill=MINT, stroke=TEAL, size=9.5)
    if i < 5:
        f.arrow([(x + 88, 37), (x + 96, 37)], color=SLATE)
f.text(290, 14, "steps (blue), calls (green) and failures (red)", size=11, color=NAVY, bold=True)
errs = ["no jar: SQLState\n08001, 'No\nsuitable driver'", "wrong URL or\npassword: same\nSQLState 08001", "bad SQL text is\nfound only when\nthe SQL runs", "SELEKT: code 1\nno table: code 1\nduplicate: code 19", "NULL with getInt:\n0, and wasNull()\nis true", "forgotten close\nleaks a\nconnection"]
for i, t in enumerate(errs):
    x = 6 + i * 96
    f.arrow([(x + 44, 98), (x + 44, 118)], color=RED, dash=True)
    f.box(x, 118, 88, 56, t, fill=ROSE, stroke=RED, size=9, color=SLATE)
f.box(6, 190, 568, 56, "", fill=SAND, stroke=AMBER)
f.text(290, 206, "SQLException carries three useful things", size=10.5, color=AMBER, bold=True)
f.text(290, 224, "getMessage() (text)   getSQLState() (portable 5-character code)   getErrorCode() (vendor number)", size=9.5, color=SLATE)
f.text(290, 238, "print all three in the log; the SQLite driver returned errorCode 19 for both UNIQUE and NOT NULL failures", size=9.5, color=SLATE)
```

```svgfig label="3.4" caption="The ResultSet cursor, from a real run over four rows. The cursor starts before the first row (isBeforeFirst true, getRow 0); each next() moves down one row (getRow 1, 2, 3, 4) and the last call returns false with the cursor after the last row. Columns are numbered from 1 (getInt(1) is id); a SQL NULL read with getInt gives 0 and wasNull() tells it apart from a real 0."
f = Fig(580, 232)
rows = [(1, "Ram", 72), (2, "Sita", 91), (3, "Hari", 64), (4, "Gita", 85)]
f.text(165, 14, "SELECT id, name, marks FROM student", size=11, color=NAVY, bold=True)
f.box(70, 24, 190, 24, "before first: getRow() = 0", fill=SAND, stroke=AMBER, size=9.5, bold=True)
for i, (a, b, c) in enumerate(rows):
    y = 56 + i * 26
    f.box(70, y, 40, 22, str(a), fill=BLUE, stroke=NAVY, size=10.5, bold=True)
    f.box(110, y, 90, 22, b, fill=BLUE, stroke=NAVY, size=10.5)
    f.box(200, y, 60, 22, str(c), fill=BLUE, stroke=NAVY, size=10.5)
    f.text(64, y + 11, "row %d" % (i + 1), size=9.5, color=SLATE, anchor="end", vmid=True)
f.box(70, 164, 190, 24, "after last: next() = false", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.text(90, 204, "column 1", size=9.5, color=TEAL, bold=True)
f.text(155, 204, "column 2", size=9.5, color=TEAL, bold=True)
f.text(230, 204, "column 3", size=9.5, color=TEAL, bold=True)
for k in range(5):
    f.arrow([(20, 36 + k * 26), (20, 62 + k * 26)], color=RED, sw=2)
f.text(6, 20, "next()", size=9.5, color=RED, bold=True, anchor="start")
f.box(310, 24, 260, 96, "", fill="#ffffff", stroke=SLATE)
f.text(440, 40, "reading the current row", size=10.5, color=NAVY, bold=True)
for i, t in enumerate(["rs.getInt(1)       -> 1 (by index, first column is 1)", "rs.getString(\"name\") -> Ram (by name)", "rs.getInt(\"marks\")   -> 72", "rs.getInt(0) is an error: no column 0"]):
    f.text(320, 60 + i * 15, t, size=9, color=SLATE, anchor="start")
f.box(310, 132, 260, 84, "", fill=SAND, stroke=AMBER)
f.text(440, 148, "NULL handling (real run)", size=10.5, color=AMBER, bold=True)
for i, t in enumerate(["born is NULL for Hari (id 3):", "rs.getInt(\"born\")   -> 0", "rs.wasNull()        -> true", "rs.getObject(\"born\") -> null"]):
    f.text(320, 168 + i * 15, t, size=9, color=SLATE, anchor="start")
f.text(440, 228, "ask wasNull() right after the read", size=9.5, color=RED, bold=True)
```

```svgfig label="3.5" caption="How SQL types map to Java types. The left table is from a real run of getObject on one row of a table with five declared types: INTEGER came back as Integer, TEXT as String, REAL as Double, BLOB as byte[] and NUMERIC holding 20050301 as Integer. The right table is the standard JDBC mapping that MySQL and PostgreSQL drivers follow."
f = Fig(580, 252)
f.text(135, 14, "real run (SQLite, declared type to Java class)", size=10.5, color=NAVY, bold=True)
real = [("INTEGER", "Integer", "getInt"), ("TEXT", "String", "getString"), ("REAL", "Double", "getDouble"), ("BLOB", "byte[]", "getBytes"), ("NUMERIC", "Integer (20050301)", "getInt / getObject")]
f.box(8, 26, 260, 24, "", fill=NAVY, stroke=NAVY)
for x, t in [(14, "declared"), (88, "Java class"), (190, "getter")]:
    f.text(x, 38, t, size=9.5, color="#ffffff", bold=True, anchor="start", vmid=True)
for i, (a, b, c) in enumerate(real):
    y = 50 + i * 28
    f.box(8, y, 260, 28, "", fill=BLUE if i % 2 == 0 else "#ffffff", stroke=SLATE, r=0, sw=0.8)
    f.text(14, y + 14, a, size=9.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(88, y + 14, b, size=9.5, color=SLATE, anchor="start", vmid=True)
    f.text(190, y + 14, c, size=9, color=TEAL, anchor="start", vmid=True)
f.text(435, 14, "standard JDBC mapping", size=10.5, color=NAVY, bold=True)
std = [("VARCHAR, CHAR", "String"), ("INTEGER", "int / Integer"), ("BIGINT", "long / Long"), ("DECIMAL, NUMERIC", "BigDecimal"), ("DOUBLE, FLOAT", "double"), ("DATE", "java.sql.Date / LocalDate"), ("TIMESTAMP", "Timestamp / LocalDateTime"), ("BLOB", "byte[] / Blob"), ("BOOLEAN", "boolean")]
f.box(290, 26, 282, 24, "", fill=NAVY, stroke=NAVY)
f.text(298, 38, "SQL type", size=9.5, color="#ffffff", bold=True, anchor="start", vmid=True)
f.text(420, 38, "Java type", size=9.5, color="#ffffff", bold=True, anchor="start", vmid=True)
for i, (a, b) in enumerate(std):
    y = 50 + i * 20
    f.box(290, y, 282, 20, "", fill=MINT if i % 2 == 0 else "#ffffff", stroke=SLATE, r=0, sw=0.8)
    f.text(298, y + 10, a, size=9, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(420, y + 10, b, size=9, color=SLATE, anchor="start", vmid=True)
f.text(135, 214, "use BigDecimal, never double, for money", size=9.5, color=RED, bold=True)
f.text(135, 230, "SQLite stores by value, so 'declared' is only a hint", size=9.5, color=SLATE)
f.text(435, 242, "getObject(i) works for any type; getInt(i) converts", size=9.5, color=SLATE)
```

```photogrid label="3.3" cols="3" ratio="1.0" caption="Where JDBC code ends up. (a) A cash machine (CC0): the machine's program connects to the bank's database to read the balance and to debit it, which must happen as one transaction. (b) Racks of servers at CERN (CC BY-SA 3.0): a database runs on a server like these, and the program reaches it by host name and port in the JDBC URL. (c) The parts of a JDBC URL, from a MySQL example: protocol, sub-protocol (which picks the driver), host, port, database and options."
@ photo id="bca202/atm" cap="ATM: a debit is a transaction"
fit 1.0
focus 0.5 0.5
@ photo id="bca301/cernrack" cap="Database servers in racks"
fit 1.0
focus 0.5 0.5
@ svg cap="Anatomy of a JDBC URL"
f = Fig(190, 250)
f.text(95, 12, "jdbc:mysql://localhost:3306/", size=9.5, color=NAVY, bold=True)
f.text(95, 26, "college?useSSL=false", size=9.5, color=NAVY, bold=True)
parts = [("jdbc", "protocol (always)", BLUE, NAVY), ("mysql", "sub-protocol: the driver", MINT, TEAL), ("localhost", "host name or IP", SAND, AMBER), ("3306", "port (MySQL default)", SAND, AMBER), ("college", "database name", MINT, TEAL), ("useSSL=false", "option after the ?", ROSE, RED)]
for i, (a, b, fl, st) in enumerate(parts):
    y = 36 + i * 34
    f.box(4, y, 182, 18, a, fill=fl, stroke=st, size=9.5, bold=True, r=4)
    f.text(95, y + 27, b, size=9.5, color=SLATE)
f.text(95, 246, "SQLite: jdbc:sqlite:file.db", size=9.5, color=NAVY, bold=True)
```

```svgfig label="3.6" caption="Why transactions and batches matter, measured. A real run inserted 1,000 rows into a SQLite file. With auto-commit on, a concatenated Statement took 1,233 ms and a PreparedStatement 1,250 ms, because each of the 1,000 commits waits for the disk. One transaction around 1,000 prepared inserts took 10 ms and a batch inside one transaction took 9 ms (a repeat took 4 ms). The speed-up over the first case is computed in the figure. The scale is logarithmic."
f = Fig(580, 232)
cm = __import__("math")
data = [("Statement, concatenated SQL, auto-commit on", 1233, RED), ("PreparedStatement, auto-commit on", 1250, RED), ("PreparedStatement, one transaction", 10, TEAL), ("PreparedStatement + addBatch, one transaction", 9, TEAL)]
f.text(290, 14, "time to insert 1,000 rows (milliseconds, log scale)", size=11, color=NAVY, bold=True)
x0, x1 = 20, 540
def X(v):
    return x0 + (x1 - x0) * cm.log10(v) / cm.log10(2000)
for t in [1, 10, 100, 1000]:
    f.line(X(t), 30, X(t), 176, color="#cbd5e1", sw=1)
    f.text(X(t), 190, str(t), size=9.5, color=SLATE)
for i, (a, v, c) in enumerate(data):
    y = 34 + i * 36
    f.text(x0, y + 4, a, size=9.5, color=SLATE, anchor="start")
    f.box(x0, y + 10, X(v) - x0, 16, "", fill=c, stroke=c, r=2)
    f.text(X(v) + 6, y + 18, "%d ms" % v, size=10, color=c, bold=True, anchor="start", vmid=True)
sp = 1233 / 9
assert round(sp) == 137
f.text(290, 214, "1,233 / 9 = about %d times faster with one transaction and a batch" % round(sp), size=10.5, color=NAVY, bold=True)
f.text(290, 228, "the commit (a disk write) is the cost; PreparedStatement alone does not remove it, but it makes the SQL safe", size=9.5, color=SLATE)
```

```svgfig label="3.7" caption="SQL injection, built from the real strings of the demo program. The WHERE text is produced by the same concatenation as the Java code. The honest wrong password matched 0 rows; the comment injection admin' -- matched 1 row because everything after the two dashes is a comment; a tautology in the name field only matched 0; a tautology in both fields matched 2 (every row). The prepared statement matched 0 rows for both attacks. Grey text is ignored by the database."
f = Fig(580, 262)
cases = [("honest, wrong password", "admin", "x", 0), ("comment injection", "admin' --", "x", 1), ("tautology, name only", "' OR '1'='1", "x", 0), ("tautology, both fields", "' OR '1'='1", "' OR '1'='1", 2)]
f.text(290, 14, "WHERE clause produced by concatenation", size=11, color=NAVY, bold=True)
for i, (lab, n, p, r) in enumerate(cases):
    y = 26 + i * 38
    q = "name='" + n + "' AND pw='" + p + "'"
    live = q.split("--")[0] if "--" in q else q
    dead = q[len(live):]
    f.box(6, y, 120, 30, lab, fill=BLUE, stroke=NAVY, size=9.5, bold=True)
    f.box(132, y, 330, 30, "", fill="#ffffff", stroke=SLATE)
    f.text(140, y + 15, live, size=9.5, color=NAVY, anchor="start", vmid=True)
    if dead:
        f.text(140 + len(live) * 5.3, y + 15, dead, size=9.5, color="#94a3b8", anchor="start", vmid=True)
    f.box(468, y, 106, 30, "%d row%s" % (r, "" if r == 1 else "s"), fill=ROSE if r else MINT, stroke=RED if r else TEAL, size=10.5, bold=True)
f.box(6, 184, 568, 66, "", fill=MINT, stroke=TEAL)
f.text(290, 200, "PreparedStatement: WHERE name = ? AND pw = ?", size=10.5, color=TEAL, bold=True)
f.text(290, 218, "the SQL text is sent once with two holes; the values travel separately and are only data", size=9.5, color=SLATE)
f.text(290, 234, "input admin' -- gave 0 rows and input ' OR '1'='1 in both fields gave 0 rows (real run)", size=9.5, color=SLATE, bold=True)
```

```svgfig label="3.8" caption="The states of a transaction and the bank-transfer example, simulated in the figure with the numbers of the real program. Transfer 1 moves 200 from account 1 (500) to account 2 (300) and commits: 300 and 500. Transfer 2 tries 400: the debit would leave 300 - 400 = -100, the check throws 'insufficient funds', rollback restores 300 and 500, and the state ends in Aborted."
f = Fig(580, 262)
a1, a2 = 500, 300
f.text(290, 14, "states of a transaction", size=11, color=NAVY, bold=True)
f.box(10, 30, 90, 30, "Active", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(150, 30, 120, 30, "Partially\ncommitted", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(330, 30, 90, 30, "Committed", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(150, 84, 120, 30, "Failed", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(330, 84, 90, 30, "Aborted", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(100, 45), (150, 45)], color=SLATE, label="last statement", lpos=(125, 37), lsize=8.5) if False else f.arrow([(100, 45), (150, 45)], color=SLATE)
f.arrow([(270, 45), (330, 45)], color=TEAL, label="commit()", lpos=(300, 38), lsize=9.5)
f.arrow([(60, 60), (60, 99), (150, 99)], color=RED)
f.arrow([(210, 60), (210, 84)], color=RED)
f.arrow([(270, 99), (330, 99)], color=RED, label="rollback()", lpos=(300, 92), lsize=9.5)
f.text(500, 45, "all changes kept", size=9.5, color=TEAL, bold=True)
f.text(500, 99, "all changes undone", size=9.5, color=RED, bold=True)
def transfer(a, b, amt):
    na = a - amt
    if na < 0:
        return a, b, "rolled back"
    return na, b + amt, "committed"
y = 138
f.text(290, y, "the real program: two transfers", size=11, color=NAVY, bold=True)
steps = [("start", a1, a2, None)]
a1n, a2n, s1 = transfer(a1, a2, 200)
steps.append(("transfer 200: " + s1, a1n, a2n, TEAL))
a1m, a2m, s2 = transfer(a1n, a2n, 400)
steps.append(("transfer 400: " + s2, a1m, a2m, RED))
assert (a1n, a2n, a1m, a2m) == (300, 500, 300, 500) and s2 == "rolled back"
for i, (lab, p, q, c) in enumerate(steps):
    x = 10 + i * 192
    f.box(x, y + 14, 180, 60, "", fill="#ffffff", stroke=c or SLATE)
    f.text(x + 90, y + 30, lab, size=9.5, color=c or NAVY, bold=True)
    f.text(x + 90, y + 50, "account 1 = %d, account 2 = %d" % (p, q), size=9.5, color=SLATE)
    f.text(x + 90, y + 64, "sum = %d" % (p + q), size=9.5, color=NAVY, bold=True)
    if i < 2:
        f.arrow([(x + 180, y + 44), (x + 192, y + 44)], color=SLATE)
f.text(290, 238, "the sum stays 800 in every state: money is neither created nor lost (consistency)", size=10, color=NAVY, bold=True)
```

```svgfig label="3.9" caption="Isolation seen in a real run with two connections. Connection c1 starts a transaction and sets marks of row 1 to 999. Before the commit, c1 sees 999 but c2 still sees 1 (no dirty read); after the commit c2 sees 999. The table lists which anomalies each standard isolation level allows (by the SQL standard; real engines differ in details: SQLite is always SERIALIZABLE, MySQL InnoDB defaults to REPEATABLE READ and PostgreSQL to READ COMMITTED)."
f = Fig(580, 270)
f.text(145, 14, "real run: two connections", size=11, color=NAVY, bold=True)
f.text(40, 44, "c1", size=11, color=NAVY, bold=True)
f.text(40, 94, "c2", size=11, color=TEAL, bold=True)
f.line(60, 44, 290, 44, color=NAVY, sw=1.5)
f.line(60, 94, 290, 94, color=TEAL, sw=1.5)
ev = [(80, 44, "UPDATE\nmarks = 999", NAVY, "c1"), (140, 44, "reads 999", NAVY, "c1"), (140, 94, "reads 1", TEAL, "c2"), (210, 44, "commit()", RED, "c1"), (260, 94, "reads 999", TEAL, "c2")]
for x, y, t, c, w in ev:
    f.circle(x, y, 5, fill=c, stroke=c)
    f.text(x, y + (-20 if w == "c1" else 20), t, size=9, color=c, bold=True)
f.line(210, 44, 210, 120, color=RED, sw=1.2, dash=True)
f.text(210, 134, "commit makes the change\nvisible to others", size=9.5, color=RED)
f.text(145, 176, "uncommitted changes are invisible to c2", size=9.5, color=SLATE)
levels = {"READ UNCOMMITTED": (1, 1, 1), "READ COMMITTED": (0, 1, 1), "REPEATABLE READ": (0, 0, 1), "SERIALIZABLE": (0, 0, 0)}
hdr = ["dirty read", "non-repeat.", "phantom"]
f.text(435, 14, "anomalies allowed by the standard", size=10.5, color=NAVY, bold=True)
f.box(310, 24, 262, 26, "", fill=NAVY, stroke=NAVY, r=2)
f.text(316, 37, "level", size=9, color="#ffffff", bold=True, anchor="start", vmid=True)
for j, h in enumerate(hdr):
    f.text(432 + j * 52, 37, h, size=9, color="#ffffff", bold=True, vmid=True)
for i, (lv, flags) in enumerate(levels.items()):
    y = 50 + i * 30
    f.box(310, y, 262, 30, "", fill=BLUE if i % 2 == 0 else "#ffffff", stroke=SLATE, r=0, sw=0.8)
    f.text(316, y + 15, lv, size=8.5, color=NAVY, bold=True, anchor="start", vmid=True)
    for j, v in enumerate(flags):
        f.text(432 + j * 52, y + 15, "yes" if v else "no", size=9.5, color=RED if v else TEAL, bold=True, vmid=True)
f.text(435, 190, "more protection = more locking = slower", size=9.5, color=SLATE, bold=True)
f.box(10, 196, 560, 64, "", fill=SAND, stroke=AMBER)
f.text(290, 212, "con.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE)   (constant 8)", size=9.5, color=AMBER, bold=True)
f.text(290, 230, "dirty read: see another transaction's uncommitted data   non-repeatable: same row read twice, two values", size=9, color=SLATE)
f.text(290, 244, "phantom: the same query returns extra rows the second time   choose the lowest level that is safe", size=9, color=SLATE)
```

```svgfig label="3.10" caption="A savepoint is a bookmark inside a transaction. In the real run the program updated row 2 (marks = 1), set the savepoint afterFirst, updated row 3 (marks = 2), then called rollback(savepoint) and commit(). The result was id 2 = 1 (kept) and id 3 = 3 (its original value restored), so only the work after the savepoint was undone."
f = Fig(580, 188)
f.text(290, 14, "one transaction, one savepoint", size=11, color=NAVY, bold=True)
f.line(20, 84, 560, 84, color=SLATE, sw=2)
nodes = [(50, "begin\n(auto-commit off)", NAVY), (150, "UPDATE id 2\nmarks = 1", NAVY), (250, "setSavepoint\n(afterFirst)", AMBER), (350, "UPDATE id 3\nmarks = 2", NAVY), (450, "rollback\n(afterFirst)", RED), (535, "commit()", TEAL)]
for x, t, c in nodes:
    f.circle(x, 84, 6, fill=c, stroke=c)
    f.text(x, 56, t, size=9, color=c, bold=True)
f.arrow([(450, 100), (250, 100)], color=RED, dash=True, label="undo the work after the savepoint", lpos=(350, 118), lsize=9.5)
f.box(20, 134, 250, 40, "after commit: id 2 = 1 (kept)", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(310, 134, 250, 40, "after commit: id 3 = 3 (original)", fill=SAND, stroke=AMBER, size=10, bold=True)
```

```svgfig label="3.11" caption="Reusing a connection and batching, measured and modelled. Left: a real run of 300 small queries took 186 microseconds each when every query opened its own connection to a SQLite file and 27 microseconds each on one reused connection, 6.9 times faster; for a database on another machine the opening cost (network handshake, login) is far larger. Right: a model with 1 ms per round trip: 1,000 single statements need 1,000 trips (1,000 ms), batches of 100 need 10 trips and one batch needs 1 trip."
f = Fig(580, 240)
f.text(140, 14, "per query, real run (microseconds)", size=10.5, color=NAVY, bold=True)
op, ru = 186, 27
for i, (t, v, c) in enumerate([("open a connection each time", op, RED), ("one reused connection", ru, TEAL)]):
    y = 40 + i * 62
    f.text(10, y, t, size=9.5, color=SLATE, anchor="start")
    f.box(10, y + 8, v * 1.3, 24, "", fill=c, stroke=c, r=2)
    f.text(10 + v * 1.3 + 6, y + 20, "%d us" % v, size=10.5, color=c, bold=True, anchor="start", vmid=True)
ratio = op / ru
assert round(ratio, 1) == 6.9
f.text(140, 176, "%.1f times faster when reusing" % ratio, size=10.5, color=NAVY, bold=True)
f.text(140, 196, "a pool keeps connections open for this reason", size=9.5, color=SLATE)
f.text(435, 14, "batching model, 1 ms per round trip", size=10.5, color=NAVY, bold=True)
f.box(300, 26, 272, 24, "", fill=NAVY, stroke=NAVY, r=2)
for x, t in [(308, "how sent"), (430, "trips"), (500, "time")]:
    f.text(x, 38, t, size=9.5, color="#ffffff", bold=True, anchor="start", vmid=True)
for i, (t, trips) in enumerate([("1,000 executeUpdate calls", 1000), ("10 batches of 100", 10), ("1 batch of 1,000", 1)]):
    y = 50 + i * 34
    f.box(300, y, 272, 34, "", fill=BLUE if i % 2 == 0 else "#ffffff", stroke=SLATE, r=0, sw=0.8)
    f.text(308, y + 17, t, size=9.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(430, y + 17, "{:,}".format(trips), size=9.5, color=SLATE, anchor="start", vmid=True)
    f.text(500, y + 17, "{:,} ms".format(trips), size=9.5, color=RED if trips == 1000 else TEAL, bold=True, anchor="start", vmid=True)
f.text(435, 170, "executeBatch() returns int[]: one count per statement", size=9.5, color=SLATE, bold=True)
f.text(435, 188, "in the real run: 1000 counts, 1000 rows affected", size=9.5, color=TEAL, bold=True)
f.text(290, 226, "fewer round trips and fewer commits: both batching and pooling attack waiting time", size=10, color=NAVY, bold=True)
```

```svgfig label="3.12" caption="A CachedRowSet is disconnected. In the real run the program opened a connection, ran the query and called populate(rs), then the connection was closed; the three rows (Kathmandu, Pokhara, Biratnagar) were still there and could be scrolled both ways: absolute(2) gave Pokhara, last() gave Biratnagar at row number 3 and previous() gave Pokhara. A plain ResultSet stops working when its connection closes."
f = Fig(580, 232)
f.text(290, 14, "time runs left to right", size=11, color=NAVY, bold=True)
f.text(10, 50, "connection", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(110, 36, 120, 28, "open: query, populate", fill=SAND, stroke=AMBER, size=9, bold=True)
f.box(230, 36, 330, 28, "closed (the server is free for other users)", fill=SOFT, stroke=SLATE, size=9.5, dash=True)
f.text(10, 100, "rows in memory", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(230, 86, 330, 28, "3 rows cached: size() = 3", fill=MINT, stroke=TEAL, size=10, bold=True)
f.line(230, 64, 230, 86, color=TEAL, sw=2)
f.text(10, 150, "scrolling", size=10.5, color=NAVY, bold=True, anchor="start")
moves = [("beforeFirst\n+ next()", "Kathmandu"), ("absolute(2)", "Pokhara"), ("last()", "Biratnagar, row 3"), ("previous()", "Pokhara")]
for i, (a, b) in enumerate(moves):
    x = 110 + i * 117
    f.box(x, 130, 108, 30, a, fill=BLUE, stroke=NAVY, size=9, bold=True)
    f.arrow([(x + 54, 160), (x + 54, 172)], color=SLATE)
    f.box(x, 172, 108, 26, b, fill=MINT, stroke=TEAL, size=9, bold=True)
f.text(290, 220, "good for GUI tables and for sending data between layers; use acceptChanges(con) to write edits back", size=9.5, color=SLATE, bold=True)
```

```svgfig label="3.13" caption="The DAO pattern as layers. The servlet, window or test calls only the StudentDao interface (insert, findById, findAll, delete). One class implements it with JDBC; another could keep the students in memory for tests. In the real run findAll listed 3 students, findById(2) gave Sita, findById(9) gave none, delete(1) gave true and a second delete(1) gave false, leaving 2."
f = Fig(580, 232)
f.box(180, 12, 220, 32, "Servlet, Swing window or test", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.arrow([(290, 44), (290, 62)], color=SLATE)
f.box(150, 62, 280, 44, "interface StudentDao\ninsert  findById  findAll  delete", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(220, 106), (130, 130)], color=SLATE)
f.arrow([(360, 106), (450, 130)], color=SLATE)
f.box(20, 130, 220, 40, "JdbcStudentDao\n(SQL and PreparedStatement)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(340, 130, 220, 40, "MemoryStudentDao\n(a List, for tests)", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.arrow([(130, 170), (130, 188)], color=SLATE)
f.box(60, 188, 140, 30, "database", fill=SOFT, stroke=SLATE, size=10, bold=True)
res = [("findAll", "3 students"), ("findById(2)", "Sita"), ("findById(9)", "none"), ("delete(1) twice", "true, false")]
f.text(450, 190, "the real run", size=10, color=NAVY, bold=True)
f.text(340, 204, "findAll 3, findById(2) Sita, findById(9) none", size=9, color=SLATE, anchor="start")
f.text(340, 218, "delete(1) true then false; 2 remain", size=9, color=SLATE, anchor="start")
```

```svgfig label="3.14" caption="A connection pool of size 3 serving 8 requests, simulated in the figure. A request arrives every 1 ms and each query holds a connection for 5 ms. The pool never opens a new connection, so the first three requests start at once and later ones wait up to 4 ms for a free connection. The average response time is computed below; without a pool every request would also pay the cost of opening a connection (50 ms is assumed for a remote database), so its response would be 55 ms."
f = Fig(580, 262)
arr = [i for i in range(8)]
free = [0, 0, 0]
sched = []
for i, a in enumerate(arr):
    k = min(range(3), key=lambda j: free[j])
    s = max(a, free[k])
    e = s + 5
    free[k] = e
    sched.append((i + 1, a, k, s, e))
resp = [e - a for (_, a, _, _, e) in sched]
avg = sum(resp) / len(resp)
assert resp == [5, 5, 5, 7, 7, 7, 9, 9] and max(resp) == 9 and abs(avg - 6.75) < 1e-9
f.text(290, 14, "pool of 3 connections, 8 requests (time in ms)", size=11, color=NAVY, bold=True)
x0, sc = 80, 28
for t in range(0, 21, 2):
    f.line(x0 + t * sc * 0.5 * 1.0, 30, x0 + t * sc * 0.5, 134, color="#e2e8f0", sw=1)
    f.text(x0 + t * sc * 0.5, 148, str(t), size=9, color=SLATE)
for j in range(3):
    f.text(70, 56 + j * 30, "conn %d" % (j + 1), size=10, color=NAVY, bold=True, anchor="end", vmid=True)
cols = [BLUE, MINT, SAND, ROSE, "#e0e7ff", "#cffafe", "#fef9c3", "#fae8ff"]
for (n, a, k, s, e) in sched:
    f.box(x0 + s * sc * 0.5, 44 + k * 30, 5 * sc * 0.5, 24, "R%d" % n, fill=cols[n - 1], stroke=NAVY, size=9, bold=True, r=3)
f.text(290, 164, "arrivals at 0, 1, 2, 3, 4, 5, 6, 7 ms; each holds a connection 5 ms", size=9.5, color=SLATE)
f.box(10, 180, 280, 70, "", fill=MINT, stroke=TEAL)
f.text(150, 196, "with a pool of 3", size=10.5, color=TEAL, bold=True)
f.text(150, 214, "responses: " + ", ".join(str(r) for r in resp) + " ms", size=9.5, color=SLATE)
f.text(150, 232, "average = %.3f ms, worst = %d ms" % (avg, max(resp)), size=10, color=NAVY, bold=True)
f.box(300, 180, 270, 70, "", fill=ROSE, stroke=RED)
f.text(435, 196, "open a new connection each time", size=10.5, color=RED, bold=True)
f.text(435, 214, "50 ms (assumed) + 5 ms = 55 ms each", size=9.5, color=SLATE)
f.text(435, 232, "and the server may refuse the 100th at once", size=9.5, color=SLATE, bold=True)
```

### 3.8.1 Eight uses of JDBC in Nepal

1. **Bank and wallet transfers.** Payment systems such as ConnectIPS and Fonepay move money between banks, and inside a bank a Java service must debit one account and credit another. These two updates are written as one transaction with `commit()` and `rollback()` (Figure 3.8), so a failure between them cannot lose money. The bank also keeps the record that the passbook of Plate 3.2 once kept on paper.
2. **Student records and exam results.** Tribhuvan University, colleges and the EMIS of schools keep students, subjects and marks in relational tables. A result-entry program reads a roll number from a form, so it must use a `PreparedStatement` and never join the text into the SQL (Figure 3.7). Batch updates let a college load the marks of several hundred students in one transaction (Figure 3.6).
3. **Government services and the Nagarik App.** Services that check a citizen's record, such as a certificate request or a tax payment, look up rows by a citizen number. The Java back end opens a pooled connection, runs one parameterised query and returns the connection at once (Figure 3.14). A pool keeps the service quick when many people use it on the same morning.
4. **Weather and river data.** The Department of Hydrology and Meteorology collects readings from stations on rivers and hills every few minutes. A loader program inserts the readings with `addBatch()` and commits them together, which is much faster than one commit per reading (Figure 3.6). Forecasters then query the table for a station and a date.
5. **Hospital information systems.** A hospital stores patients, visits, tests and bills, and a clerk's screen reads and writes these rows all day. A bill and its line items are inserted in one transaction, so a half-saved bill never appears. The DAO layer lets the hospital change its database without rewriting the screens (Figure 3.13).
6. **Cooperatives and microfinance.** Savings cooperatives keep members, shares, loans and instalments in a database, and each end-of-month run updates thousands of rows. A batch inside a transaction does this in seconds, and a rollback undoes the whole run if one row breaks a rule. A savepoint (Figure 3.10) can undo only a bad part of a long run.
7. **Online shops and ticket sellers.** A shop or a bus-ticket site checks a user's login, reserves stock or a seat, and records an order. The seat or the last item must be taken by one buyer only, so the reservation runs at a safe isolation level (Figure 3.9). The login check must use a prepared statement and a stored password hash.
8. **Utility bills and reports.** A bill-payment site for electricity or water looks up an account, shows the amount due and records the payment. Reports for managers use `ResultSetMetaData` to print any table without knowing its columns in advance (Figure 3.4). Disconnected rows (Figure 3.12) can be shown in a table on a screen while the connection returns to the pool.

## Formula and fact sheet

- Steps: driver → `getConnection(url)` → `createStatement`/`prepareStatement` → `executeQuery`/`executeUpdate` → `while (rs.next())` → close.
- `executeQuery` → `ResultSet`; `executeUpdate` → int; placeholders `?` are 1-based; column indexes are 1-based.
- Always use `PreparedStatement` for user input (prevents SQL injection) and try-with-resources for closing.
- Transaction: `setAutoCommit(false)` … `commit()` / `rollback()`; ACID; isolation levels.
- Batch: `addBatch()` then `executeBatch()` (int[]). `CachedRowSet`: disconnected, scrollable.
- URL examples: `jdbc:mysql://host:3306/db`, `jdbc:postgresql://host/db`, `jdbc:sqlite:file.db`.

## Chapter summary

- JDBC defines database-independent interfaces; a vendor driver (type 4 today) implements them; the program loads the driver, connects, runs SQL and processes results.
- `PreparedStatement` is faster for repeated SQL and the cure for SQL injection; `ResultSet` is a cursor and metadata describes its columns.
- Transactions make groups of statements atomic through commit and rollback; batching reduces round trips.
- `RowSet`s offer disconnected, scrollable data; the DAO pattern and connection pools separate persistence from the rest of the application.

## Practice

1. List the steps of a JDBC program and the four driver types.
2. Differentiate `Statement`, `PreparedStatement` and `CallableStatement`.
3. Write code to insert a student with a prepared statement and to list all students with marks above 80.
4. Explain SQL injection with an example and how `PreparedStatement` prevents it.
5. What is a transaction? Write the JDBC code for transferring money atomically.
6. What does `executeBatch()` return and why use batching?
7. What is a `ResultSet` cursor? How do `next()`, `getInt(1)` and `getInt("marks")` differ in indexing?
8. Describe `RowSet` and the advantage of `CachedRowSet`.
9. What is the DAO pattern? Sketch the interface for a `Student` DAO.
10. Why are connection pools used and how does a servlet obtain a pooled connection?

::: note Answers and worked solutions
**1.** Load the driver, open a connection, create a statement, execute SQL, process the results, close the resources. Types: 1 JDBC–ODBC bridge, 2 native API, 3 network protocol (middleware), 4 pure Java.
**2.** `Statement`: fixed SQL text. `PreparedStatement`: parameterised, precompiled SQL for repeated and safe use. `CallableStatement`: calls stored procedures with IN and OUT parameters.
**3.** `PreparedStatement ps = con.prepareStatement("INSERT INTO student(name, marks) VALUES (?, ?)"); ps.setString(1, "Ram"); ps.setInt(2, 72); ps.executeUpdate();` and `ResultSet rs = con.createStatement().executeQuery("SELECT name FROM student WHERE marks > 80"); while (rs.next()) System.out.println(rs.getString(1));`
**4.** If SQL is built by concatenation, input such as `admin' --` (comment out the password test) or `' OR '1'='1` in both fields changes the query's logic and returns rows without valid credentials (1 and 2 rows in the demo). A prepared statement sends SQL and parameters separately; the input is only data and matches 0 rows.
**5.** A unit of work that is all or nothing (ACID). Code: `con.setAutoCommit(false); try { debit; credit; con.commit(); } catch (SQLException e) { con.rollback(); } finally { con.setAutoCommit(true); }`.
**6.** An `int[]` of update counts, one per queued statement. Batching reduces network round trips, which is much faster for many inserts.
**7.** `next()` advances to the next row. Column indexes are 1-based, so `getInt(1)` reads the first column; `getInt("marks")` reads by column name.
**8.** A `RowSet` is a `ResultSet` that is also a JavaBean; a `CachedRowSet` holds its rows in memory, so it works after the connection is closed, can be scrolled and edited, and is easy to pass between layers.
**9.** The Data Access Object hides persistence behind an interface: `interface StudentDao { void insert(Student s); Optional<Student> findById(int id); List<Student> findAll(); boolean delete(int id); }` with a JDBC implementation.
**10.** Opening connections is slow; a pool reuses them. In a container the pool is a `DataSource` configured in the server and found through JNDI (`java:comp/env/jdbc/...`).
:::

## Model answers for Unit 3

**Q1. Explain the architecture of JDBC, the four driver types and the steps of a JDBC program. (10 marks)**

**Introduction.** JDBC (Java Database Connectivity) is the standard API, in the package `java.sql`, that lets a Java program send SQL to a relational database and read the results in the same way for every vendor. The application depends only on interfaces; the database vendor supplies the classes behind them (Fig. 3.1).

**Architecture.** There are four layers. (1) The application calls `Connection`, `Statement` and `ResultSet`. (2) The `java.sql` interfaces define the contract. (3) The `DriverManager` (or a `DataSource`) matches the prefix of the URL, such as `jdbc:mysql:` or `jdbc:sqlite:`, to a registered driver. (4) The driver translates the calls into the protocol of one database. A real run listed one driver, `org.sqlite.JDBC` 3.45, for SQLite 3.45.3. Changing the database means changing the jar and the URL, not the code.

**Driver types (Fig. 3.2).**

| Type | Name | Layers between program and database | Today |
|---|---|---|---|
| 1 | JDBC-ODBC bridge | bridge, ODBC driver, native client (3) | removed in Java 8 |
| 2 | Native API | Java plus C driver, native client library (2) | rare |
| 3 | Network protocol | driver and a middleware server (2) | rare |
| 4 | Pure Java | only the driver (1): it speaks the database protocol | standard |

**Steps of a program.**
1. Put the driver jar on the classpath; JDBC 4 loads it automatically.
2. Open a connection with `DriverManager.getConnection(url, user, password)`.
3. Create a `Statement` or `PreparedStatement` from the connection.
4. Execute: `executeQuery` for SELECT, `executeUpdate` for INSERT, UPDATE, DELETE and DDL.
5. Process the `ResultSet` with `while (rs.next())`.
6. Close everything; a try-with-resources block does this even when an exception occurs.

**Errors.** Every step may throw `SQLException`, which carries a message, a portable SQLState (08001 for a failed connection) and a vendor error code (19 for a constraint failure in SQLite).

**Conclusion.** JDBC separates the program from the database by interfaces and drivers; a type 4 driver is the practical choice, and the six steps with try-with-resources are the pattern behind every database program in Java.

**Q2. Differentiate Statement, PreparedStatement and CallableStatement. (5 marks)**

All three come from a `Connection` and send SQL to the database, but they differ in how the SQL is prepared and what it is used for.

- `Statement` runs a complete SQL string. It is simple, but if the string contains user input the program is open to SQL injection (Fig. 3.7).
- `PreparedStatement` takes SQL with `?` placeholders. The database compiles it once; the program sets values with `setInt(1, ...)` and `setString(2, ...)` and runs it many times. Values travel separately from the SQL, so the input is always data and never code.
- `CallableStatement` calls a stored procedure kept inside the database, written as `{call raise_marks(?, ?)}`. It can register OUT parameters for results. SQLite has no stored procedures, so this form was described but not run; MySQL and PostgreSQL support it.

| Point | Statement | PreparedStatement | CallableStatement |
|---|---|---|---|
| SQL | fixed text | text with `?` | procedure call |
| Safe with user input | no | yes | yes, if parameters are used |
| Repeated use | recompiled | precompiled | procedure is stored |
| Typical use | static DDL | queries and updates | business logic in the database |

In the real timing, a PreparedStatement did not make 1,000 auto-committed inserts faster (1,250 ms against 1,233 ms); its main gain is safety, and speed comes from transactions and batches (Fig. 3.6).

**Q3. What is SQL injection? Show an example and explain how PreparedStatement prevents it. (10 marks)**

**Introduction.** SQL injection is an attack in which the user types SQL text into a form field, and a program that builds its SQL by joining strings runs that text as part of the query. It is one of the most common causes of data theft from web and desktop applications.

**Vulnerable code.** `"SELECT COUNT(*) FROM users WHERE name='" + name + "' AND pw='" + pw + "'"`.

**Attacks (real run, Fig. 3.7).**
1. *Comment injection.* The user enters `admin' --` as the name. The query becomes `WHERE name='admin' --' AND pw='x'`. The two dashes start a comment, so the password test disappears. The program returned 1 row and the attacker became admin without a password.
2. *Tautology.* The user enters `' OR '1'='1` in both fields. The condition becomes true for every row, and the query returned 2 rows, every user.
3. A tautology in the name field only returned 0 rows, because AND binds tighter than OR and the password test still failed. This shows that an attack depends on the exact query, but a program must never rely on that.

**Prevention.** A `PreparedStatement` sends the SQL `WHERE name = ? AND pw = ?` first, and the values afterwards as parameters. The database already knows the structure of the query, so the quote marks and dashes are only characters of a value. Both attacks above matched 0 rows.

| Defence | How it helps |
|---|---|
| PreparedStatement | separates code from data |
| Input validation | rejects impossible values (a roll number must be digits) |
| Least privilege | the program's database user cannot drop tables |
| Password hashing | stored values are bcrypt or Argon2 hashes, never plain text |
| Error handling | show a short message to the user, log the details |

**Conclusion.** Never build SQL by concatenation with user input. Use parameters for every value, validate input, give the database account only the rights it needs, and store hashed passwords. Parameters cannot be used for table or column names, which must be chosen from a fixed list in the program.

**Q4. What is a transaction? Explain ACID and write JDBC code for a bank transfer, with commit and rollback. (10 marks)**

**Introduction.** A transaction is a group of database operations that must succeed or fail as a whole. Moving 200 rupees from one account to another has two updates; if only the debit happened, money would vanish (Fig. 3.8).

**ACID properties.**
1. **Atomicity**: all the operations happen or none do.
2. **Consistency**: the database moves from one valid state to another; the sum of the two accounts stays 800.
3. **Isolation**: other transactions do not see the unfinished work; in the real run c2 still saw 1 while c1 had updated the row to 999, and saw 999 only after the commit (Fig. 3.9).
4. **Durability**: once committed, the change survives a crash.

**JDBC code.**

```
con.setAutoCommit(false);
try {
    debit.executeUpdate();   // UPDATE ... balance = balance - ?
    credit.executeUpdate();  // UPDATE ... balance = balance + ?
    check the balance is not negative, else throw SQLException
    con.commit();
} catch (SQLException e) {
    con.rollback();
} finally {
    con.setAutoCommit(true);
}
```

**Real run.** Balances were 500 and 300. A transfer of 200 committed and gave 300 and 500. A transfer of 400 would leave -100, the check threw `insufficient funds`, `rollback()` ran and the balances stayed 300 and 500.

**Why each step matters.** `setAutoCommit(false)` is the line that makes the two updates one unit; if it is forgotten, the debit is committed on its own and the credit may then fail. The balance check is done inside the transaction, after both updates, because the database then holds the state that would be committed, and a negative balance proves the rule would be broken. `rollback()` goes in the `catch` block so that any exception, not only the one thrown by the check, leaves the data as it was. The `finally` block restores auto-commit, because the connection may be returned to a pool and used by another request. In a real bank the same pattern also writes a row in a transaction log, so that the transfer can be traced and audited later.

**States.** A transaction is Active, then Partially Committed, then Committed; a failure leads to Failed and then Aborted (Fig. 3.8).

| Mode | Behaviour |
|---|---|
| Auto-commit (default) | each statement is its own transaction |
| Manual | `commit()` or `rollback()` ends the group |

**Speed and safety.** One commit per statement is slow; 1,000 auto-committed inserts took 1,233 ms, while one transaction took 10 ms (Fig. 3.6). **Savepoints** allow a partial rollback inside a transaction (Fig. 3.10).

**Conclusion.** Group related updates in one transaction, turn auto-commit off, commit on success, roll back on any exception, and restore auto-commit in a `finally` block.

**Q5. What are batch updates? Explain `addBatch()` and `executeBatch()` with an example. (5 marks)**

A batch sends many SQL statements to the database together instead of one by one. Each separate call costs a round trip to the server; with 1 ms per trip, 1,000 inserts need about 1,000 ms of waiting, while one batch needs a single trip (Fig. 3.11).

**Method.**
1. Prepare one statement: `PreparedStatement ps = con.prepareStatement("INSERT INTO sq VALUES (?, ?)")`.
2. For each row set the values and call `ps.addBatch()`, which only queues the row.
3. Call `int[] counts = ps.executeBatch()` to send them all. The array holds one update count for each queued statement.
4. Wrap the work in `con.setAutoCommit(false)` and `con.commit()` so the batch is also one transaction.

**Example from the book.** The program queued 1,000 rows of `(i, i * i)`. `executeBatch()` returned 1,000 counts, and the rows affected were 1,000. The table then held count 1000, sum 333,833,500 and maximum 1,000,000; the sum equals 1000 x 1001 x 2001 / 6.

In the measured run a batch inside one transaction took 9 ms, against 1,233 ms for single auto-committed inserts, about 137 times faster (Fig. 3.6). For very large loads, send the batch in pieces of a few hundred or thousand rows, so memory use stays small and one bad row does not undo hours of work.

**Q6. Explain ResultSet and ResultSetMetaData. How does a CachedRowSet differ from a ResultSet? (5 marks)**

A `ResultSet` is a cursor over the rows returned by a query. It starts before the first row (`getRow()` is 0). Each call of `next()` moves down one row and returns `false` after the last one (Fig. 3.4). Columns are read by index, counted from 1, as in `getInt(1)`, or by name, as in `getInt("marks")`. A SQL NULL read with `getInt` gives 0, so `wasNull()` must be asked straight after the read. By default a result set is forward-only and read-only.

`ResultSetMetaData` describes the columns: `getColumnCount()`, `getColumnName(i)` and `getColumnTypeName(i)`. A generic report program uses it to print any table. In the demo the query had 3 columns and the first was `id`.

**CachedRowSet.** It copies the rows into memory with `populate(rs)`, so it works after the connection is closed (Fig. 3.12).

| Point | ResultSet | CachedRowSet |
|---|---|---|
| Connection | must stay open | can be closed |
| Movement | usually forward only | both ways: `absolute(2)`, `last()`, `previous()` |
| Editing | limited | edit, then `acceptChanges(con)` |
| Memory | small | holds all rows |

In the real run three city rows were scrolled after the connection was closed. Use a cached row set for a screen table or for passing data between layers, but not for millions of rows.

**Q7. Explain the DAO pattern and connection pooling. Why are they used in real applications? (10 marks)**

**Introduction.** In a small program the SQL is written wherever it is needed, so a change of table or database means a search through every file. Two patterns solve this: the Data Access Object (DAO) hides persistence, and a connection pool hides the cost of opening connections.

**The DAO pattern (Fig. 3.13).** A DAO is an interface with a few methods for one kind of data. For students:

```
interface StudentDao {
    void insert(Student s);
    Optional<Student> findById(int id);
    List<Student> findAll();
    boolean delete(int id);
}
```

One class, `JdbcStudentDao`, implements it with `PreparedStatement` and `ResultSet`; the servlet or the window calls only the interface and never sees a `Connection`. In the real run three students were inserted, `findAll` returned all 3, `findById(2)` returned Sita and `findById(9)` returned an empty `Optional`, `delete(1)` returned true the first time and false the second, and 2 students remained.

**Benefits of DAO.**
1. The SQL lives in one place, so it is easy to change and test.
2. The database can be replaced without touching screens.
3. A test can use `MemoryStudentDao`, which keeps a list.
4. Business code stays free of `SQLException` details.

**Connection pooling (Fig. 3.14).** Opening a connection needs a network handshake and a login. In the measurement, 300 queries took 186 microseconds each when every query opened its own connection and 27 microseconds each on one reused connection (Fig. 3.11); for a remote server the gap is much larger. A pool opens a fixed number of connections at start-up and lends them out; `close()` on a pooled connection returns it to the pool. In the simulation a pool of 3 served 8 requests with an average response of 6.75 ms and a worst case of 9 ms.

| Point | New connection each time | Pool |
|---|---|---|
| Cost per request | high | low |
| Load on the server | unlimited | limited by pool size |
| Waiting | none, but the server may refuse | requests queue when all are busy |
| Examples | demo programs | HikariCP, Apache DBCP, the server's DataSource |

In a servlet container the pool is configured in the server and found through JNDI: `new InitialContext().lookup("java:comp/env/jdbc/College")`.

**Conclusion.** Use a DAO to keep SQL out of the rest of the program and a pool to keep connections cheap; together they make a database application easier to change and faster under load.

**Q8. Explain transaction isolation levels and savepoints. (5 marks)**

When many transactions run together, one may see the unfinished work of another. The SQL standard names three anomalies. A **dirty read** sees uncommitted data. A **non-repeatable read** reads the same row twice and gets two values. A **phantom** is a query that returns extra rows the second time.

Four levels are set with `con.setTransactionIsolation(...)` (Fig. 3.9).

| Level | Dirty read | Non-repeatable | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | yes | yes | yes |
| READ COMMITTED | no | yes | yes |
| REPEATABLE READ | no | no | yes |
| SERIALIZABLE | no | no | no |

Higher levels protect more but need more locking, so they are slower. PostgreSQL defaults to READ COMMITTED and MySQL InnoDB to REPEATABLE READ. In the real SQLite run the level was 8, SERIALIZABLE: connection c1 changed a row to 999 without committing, c2 still read the old value 1, and read 999 only after the commit.

A **savepoint** is a bookmark inside a transaction: `Savepoint sp = con.setSavepoint("afterFirst")`, later `con.rollback(sp)`. In the run, the update of row 2 was kept and the update of row 3 was undone, so id 2 = 1 and id 3 kept its original 3 (Fig. 3.10).

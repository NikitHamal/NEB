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

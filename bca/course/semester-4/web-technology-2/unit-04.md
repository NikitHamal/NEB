---
subject: Web Technology II
grade: BCA Semester 4
unit: 4
title: Connecting PHP to MySQL
hours: 7
area: BCA 255 · Web Technology II · Unit 4
---

This unit joins the two halves: PHP code that opens a connection, runs SQL, reads rows back and closes the connection. This is the engine of every dynamic website. PHP offers two good interfaces: **mysqli** (MySQL only) and **PDO** (many databases). The old `mysql_*` functions were removed in PHP 7 and must not be used.

::: key What this unit gives you
- Connecting and closing with mysqli and PDO; error handling.
- **Prepared statements** for every query that includes user data.
- Complete CRUD (create, read, update, delete); transactions.
:::

All programs ran on PHP 8.2 against MariaDB 10.11 with a user `demo`, password `demo123`, database `demo`. In real projects keep credentials in a configuration file outside the web root.

## 4.1 Connecting and closing

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);   // throw exceptions on errors
try {
    $db = new mysqli("localhost", "demo", "demo123", "demo");
    $db->set_charset("utf8mb4");
    echo "connected to ", $db->server_info, " | charset ", $db->character_set_name(), "\n";
    $db->close();
    echo "closed\n";
} catch (mysqli_sql_exception $e) {
    echo "connection failed: ", $e->getMessage(), "\n";
}
try {
    new mysqli("localhost", "demo", "wrong-password", "demo");
} catch (mysqli_sql_exception $e) {
    echo "expected failure: ", $e->getMessage(), "\n";
}
```
```output
connected to 10.11.19-MariaDB-0+deb12u1 | charset utf8mb4
closed
expected failure: Access denied for user 'demo'@'localhost' (using password: YES)
```
Without the `mysqli_report` line, PHP 8.1+ throws exceptions by default as well; earlier versions silently returned `false`. Always set the **character set** (`utf8mb4`), always check for failure, and close the connection when finished (PHP also closes it at script end).

## 4.2 Running queries: insert, select

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$db = new mysqli("localhost", "demo", "demo123", "demo");
$db->query("DROP TABLE IF EXISTS student");
$db->query("CREATE TABLE student (roll INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, dept VARCHAR(10), marks DECIMAL(5,2))");
$db->query("INSERT INTO student (name, dept, marks) VALUES ('Ram','BCA',78.5),('Sita','BCA',91),('Hari','BIT',64.25)");
echo "inserted ", $db->affected_rows, " rows; last id ", $db->insert_id, "\n";

$result = $db->query("SELECT roll, name, marks FROM student ORDER BY marks DESC");
echo "rows: ", $result->num_rows, "\n";
while ($row = $result->fetch_assoc()) {
    printf("%d %-5s %6.2f\n", $row["roll"], $row["name"], $row["marks"]);
}
$result->free();
$one = $db->query("SELECT COUNT(*) AS n, AVG(marks) AS mean FROM student")->fetch_assoc();
echo "count=", $one["n"], " mean=", round((float) $one["mean"], 2), "\n";
$all = $db->query("SELECT name FROM student")->fetch_all(MYSQLI_ASSOC);
echo json_encode($all), "\n";
$db->close();
```
```output
inserted 3 rows; last id 1
rows: 3
2 Sita   91.00
1 Ram    78.50
3 Hari   64.25
count=3 mean=77.92
[{"name":"Ram"},{"name":"Sita"},{"name":"Hari"}]
```
`query()` returns a result object for `SELECT` and `true` for other statements. Fetch rows with `fetch_assoc()` (array keyed by column name), `fetch_row()`, `fetch_object()` or `fetch_all()`.

## 4.3 Prepared statements: the only safe way

If you build SQL by pasting user input into a string, a user can change the meaning of your query (**SQL injection**, Unit 7). A **prepared statement** sends the SQL *template* with `?` placeholders to the server first, then sends the values **separately**; the server never treats a value as SQL.

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$db = new mysqli("localhost", "demo", "demo123", "demo");
$db->query("DROP TABLE IF EXISTS student");
$db->query("CREATE TABLE student (roll INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, dept VARCHAR(10), marks DECIMAL(5,2))");

$ins = $db->prepare("INSERT INTO student (name, dept, marks) VALUES (?, ?, ?)");
foreach ([["Ram", "BCA", 78.5], ["Sita", "BCA", 91.0], ["O'Brien", "BIT", 64.25]] as [$n, $d, $m]) {
    $ins->bind_param("ssd", $n, $d, $m);          // s = string, d = double, i = integer
    $ins->execute();
}
echo "inserted ", $db->query("SELECT COUNT(*) FROM student")->fetch_row()[0], " rows (note the apostrophe in O'Brien)\n";

$min = 70.0;
$sel = $db->prepare("SELECT name, marks FROM student WHERE marks >= ? ORDER BY name");
$sel->bind_param("d", $min);
$sel->execute();
$res = $sel->get_result();
foreach ($res->fetch_all(MYSQLI_ASSOC) as $r) { echo $r["name"], ": ", $r["marks"], "\n"; }
```
```output
inserted 3 rows (note the apostrophe in O'Brien)
Ram: 78.50
Sita: 91.00
```
Type letters in `bind_param`: `i` integer, `d` double, `s` string, `b` blob. The name `O'Brien` is stored correctly with no escaping by hand. Table and column names **cannot** be placeholders: if they come from the user, check them against a fixed whitelist.

## 4.4 Complete CRUD

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$db = new mysqli("localhost", "demo", "demo123", "demo");
$db->query("DROP TABLE IF EXISTS book");
$db->query("CREATE TABLE book (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(80) NOT NULL, price DECIMAL(8,2) NOT NULL, stock INT NOT NULL DEFAULT 0)");

function create(mysqli $db, string $title, float $price, int $stock): int {
    $st = $db->prepare("INSERT INTO book (title, price, stock) VALUES (?, ?, ?)");
    $st->bind_param("sdi", $title, $price, $stock); $st->execute();
    return $db->insert_id;
}
function read(mysqli $db, ?int $id = null): array {
    if ($id === null) return $db->query("SELECT * FROM book ORDER BY id")->fetch_all(MYSQLI_ASSOC);
    $st = $db->prepare("SELECT * FROM book WHERE id = ?"); $st->bind_param("i", $id); $st->execute();
    return $st->get_result()->fetch_assoc() ?? [];
}
function update(mysqli $db, int $id, float $price): int {
    $st = $db->prepare("UPDATE book SET price = ? WHERE id = ?"); $st->bind_param("di", $price, $id); $st->execute();
    return $st->affected_rows;
}
function remove(mysqli $db, int $id): int {
    $st = $db->prepare("DELETE FROM book WHERE id = ?"); $st->bind_param("i", $id); $st->execute();
    return $st->affected_rows;
}

$a = create($db, "C Programming", 450, 10); $b = create($db, "Python", 700, 8); create($db, "DBMS", 550, 0);
echo "created ids $a, $b, ", $db->insert_id, "\n";
echo "update: ", update($db, $b, 650), " row | read #2: ", json_encode(read($db, $b)), "\n";
echo "delete: ", remove($db, 3), " row | delete again: ", remove($db, 3), " rows | read #3: ", json_encode(read($db, 3)), "\n";
foreach (read($db) as $r) { echo "{$r['id']} {$r['title']} NPR {$r['price']} stock {$r['stock']}\n"; }
```
```output
created ids 1, 2, 3
update: 1 row | read #2: {"id":2,"title":"Python","price":"650.00","stock":8}
delete: 1 row | delete again: 0 rows | read #3: []
1 C Programming NPR 450.00 stock 10
2 Python NPR 650.00 stock 8
```
A web CRUD application is these four functions behind four pages: a list page (`SELECT`), an add form (`INSERT`), an edit form (`UPDATE`) and a delete button (`DELETE`, via `POST`, never a `GET` link).

## 4.5 PDO, errors and transactions

**PDO** (PHP Data Objects) has one interface for MySQL, PostgreSQL, SQLite and others, plus named placeholders. It is the usual choice in modern code.

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=demo;charset=utf8mb4", "demo", "demo123",
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$pdo->exec("DROP TABLE IF EXISTS account");
$pdo->exec("CREATE TABLE account (id INT PRIMARY KEY, owner VARCHAR(30), balance DECIMAL(10,2) NOT NULL CHECK (balance >= 0)) ENGINE=InnoDB");
$st = $pdo->prepare("INSERT INTO account VALUES (:id, :owner, :bal)");
$st->execute([":id" => 1, ":owner" => "Ram", ":bal" => 500]);
$st->execute([":id" => 2, ":owner" => "Sita", ":bal" => 300]);

function transfer(PDO $pdo, int $from, int $to, float $amt): string {
    try {
        $pdo->beginTransaction();
        $pdo->prepare("UPDATE account SET balance = balance - :a WHERE id = :i")->execute([":a" => $amt, ":i" => $from]);
        $pdo->prepare("UPDATE account SET balance = balance + :a WHERE id = :i")->execute([":a" => $amt, ":i" => $to]);
        $pdo->commit();
        return "committed";
    } catch (PDOException $e) {
        $pdo->rollBack();
        return "rolled back (" . substr($e->getMessage(), 0, 60) . "...)";
    }
}
echo transfer($pdo, 1, 2, 200), "\n";
echo transfer($pdo, 1, 2, 900), "\n";
foreach ($pdo->query("SELECT owner, balance FROM account ORDER BY id") as $r) { echo $r["owner"], " ", $r["balance"], "\n"; }
echo "total ", $pdo->query("SELECT SUM(balance) FROM account")->fetchColumn(), "\n";
```
```output
committed
rolled back (SQLSTATE[23000]: Integrity constraint violation: 4025 CONSTR...)
Ram 300.00
Sita 500.00
total 800.00
```
The second transfer would drive Ram below zero; the `CHECK` constraint fails after the *first* `UPDATE`, `rollBack()` undoes it, and the total stays 800.00: **atomicity**. Use InnoDB tables for transactions.

### Pagination, search and common patterns

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=demo;charset=utf8mb4", "demo", "demo123", [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$pdo->exec("DROP TABLE IF EXISTS post");
$pdo->exec("CREATE TABLE post (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(40))");
$pdo->exec("INSERT INTO post (title) VALUES " . implode(",", array_map(fn($i) => "('Post $i')", range(1, 25))));
$page = 3; $perPage = 10;
$st = $pdo->prepare("SELECT id, title FROM post ORDER BY id LIMIT :n OFFSET :o");
$st->bindValue(":n", $perPage, PDO::PARAM_INT); $st->bindValue(":o", ($page - 1) * $perPage, PDO::PARAM_INT);
$st->execute();
echo "page $page of ", ceil($pdo->query("SELECT COUNT(*) FROM post")->fetchColumn() / $perPage), ": ", implode(", ", array_column($st->fetchAll(), "title")), "\n";
$q = "Post 1";
$s2 = $pdo->prepare("SELECT title FROM post WHERE title LIKE :q ORDER BY id LIMIT 3");
$s2->execute([":q" => "%" . addcslashes($q, "%_") . "%"]);
echo implode(", ", $s2->fetchAll(PDO::FETCH_COLUMN)), "\n";
```
```output
page 3 of 3: Post 21, Post 22, Post 23, Post 24, Post 25
Post 1, Post 10, Post 11
```
## 4.6 Error handling and good practice

- Turn on exceptions (`mysqli_report` or `PDO::ERRMODE_EXCEPTION`) and catch them; **log** the real message to a file, show the user a generic one ("Something went wrong"): database messages can reveal table names to attackers.
- Use **prepared statements everywhere** there is variable data.
- Select only the columns you need (`SELECT *` wastes bandwidth and breaks when the schema changes).
- Keep connection details in one configuration file outside the document root.
- Open one connection per request; close or let PHP close it at the end.
- Set a connection character set so that Nepali text is not corrupted.

## Formula and fact sheet

- `new mysqli(host, user, pass, db)`, `$db->query()`, `fetch_assoc()`, `close()`; `affected_rows`, `insert_id`.
- `prepare("… ?")`, `bind_param("sdi", …)`, `execute()`, `get_result()`.
- `new PDO("mysql:host=…;dbname=…;charset=utf8mb4", u, p, [ERRMODE_EXCEPTION])`, named placeholders `:name`.
- Transaction: `beginTransaction()`, `commit()`, `rollBack()` (InnoDB).
- Never concatenate user input into SQL.

## Chapter summary

- PHP talks to MySQL through mysqli or PDO: connect, query, fetch, close, with exceptions for errors.
- Prepared statements separate SQL from data and are the defence against SQL injection.
- CRUD, pagination and transactions are small patterns repeated across every web application.

## Practice

1. Write PHP code that connects to a database and prints all rows of a `student` table.
2. Why are prepared statements safer than string concatenation?
3. Implement `add_student(name, marks)` using a prepared statement.
4. What do `affected_rows` and `insert_id` report?
5. Compare mysqli and PDO.
6. Explain with code why a failed money transfer must be wrapped in a transaction.
7. How should a production site report a database error to the user?

::: note Answers and worked solutions
**1.** See Section 4.2 (`query` and `fetch_assoc` loop).
**2.** The SQL text and the values travel separately; the server parses the statement before any value arrives, so a value such as `x'; DROP TABLE student; --` is only data. Concatenation lets that value become part of the SQL.
**3.**

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$db = new mysqli("localhost", "demo", "demo123", "demo");
$db->query("DROP TABLE IF EXISTS student");
$db->query("CREATE TABLE student (roll INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), marks DECIMAL(5,2))");
function add_student(mysqli $db, string $name, float $marks): int {
    $st = $db->prepare("INSERT INTO student (name, marks) VALUES (?, ?)");
    $st->bind_param("sd", $name, $marks);
    $st->execute();
    return $db->insert_id;
}
echo add_student($db, "Sita", 91.5), " ", add_student($db, "Ram", 78), "\n";
```
```output
1 2
```
**4.** `affected_rows`: the number of rows changed/deleted/inserted by the last statement; `insert_id`: the `AUTO_INCREMENT` value generated by the last `INSERT`.
**5.** mysqli: MySQL only, procedural and object styles, MySQL-specific features. PDO: 12 databases with one API, named placeholders, consistent exceptions; the usual choice for portable code.
**6.** Without a transaction, if the debit succeeds but the credit fails, money disappears. With `beginTransaction` / `commit` / `rollBack`, both updates succeed or neither does (Section 4.5, total stays 800.00).
**7.** Log the technical message (server-side file), and display a generic message with a reference code; never show SQL or table names to the visitor.
:::

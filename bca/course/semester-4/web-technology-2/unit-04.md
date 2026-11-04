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

## 4.7 Seeing the ideas: PHP talking to MySQL

A PHP script and a MySQL server are two programs, and every query is a short conversation between them. The plate shows two places where such conversations matter: a cash machine, which must never lose a transaction, and a bank vault, which must never open for the wrong person. The figures show the real results of the code of this unit, run on PHP 8.2.35 against MariaDB 10.11.19.

```photogrid label="4.1" cols="3" ratio="1.25" caption="Why database code must be careful. (a) A cash machine asks a bank database to check a balance and to subtract an amount; either both steps happen or neither, which is a transaction. (b) A bank vault of 1908: only the right key opens it, as only a prepared statement keeps the wrong input out of a query. (c) The four verbs of a database application, Create, Read, Update and Delete, map to the SQL statements INSERT, SELECT, UPDATE and DELETE."
@ photo id="bca202/atm" cap="Cash machine: a transaction"
fit 1.25
focus 0.5 0.5
@ photo id="bca254/vault" cap="Vault: only the right key"
fit 1.25
focus 0.5 0.5
@ svg cap="The four CRUD verbs"
f = Fig(300, 250)
rows = [("Create", "INSERT", BLUE, NAVY), ("Read", "SELECT", MINT, TEAL), ("Update", "UPDATE", SAND, AMBER), ("Delete", "DELETE", ROSE, RED)]
for i, (a, b, fl, st) in enumerate(rows):
    y = 8 + i * 60
    f.box(8, y, 110, 48, a, fill=fl, stroke=st, size=14, bold=True)
    f.arrow([(120, y + 24), (166, y + 24)], color=SLATE, sw=1.8)
    f.box(168, y, 124, 48, b, fill="#ffffff", stroke=st, size=14, bold=True)
```

```svgfig label="4.1" caption="Life of a database connection in PHP, with the real messages. The script connects with a host, user, password and database, sets the character set utf8mb4 (so that Nepali text survives), prepares and runs statements, fetches rows, and closes the connection. A wrong password does not return a connection: PHP 8.2 throws mysqli_sql_exception with the real text shown on the right, which the script must catch so that a visitor never sees a stack trace that contains the server name and the user name."
f = Fig(580, 214)
steps = [("1  connect", "new mysqli(host, user,\npassword, database)"), ("2  charset", "set_charset('utf8mb4')"), ("3  prepare + execute", "statement, bind values,\nrun"), ("4  fetch", "get_result() then\nfetch_assoc()"), ("5  close", "close() frees the\nconnection")]
for i, (a, b) in enumerate(steps):
    y = 8 + i * 40
    f.box(8, y, 150, 34, a, fill=BLUE, stroke=NAVY, size=11, bold=True, anchor="start")
    f.text(170, y + 17, b.replace("\n", " "), size=9.5, color=SLATE, anchor="start", vmid=True)
    if i < 4:
        f.arrow([(83, y + 35), (83, y + 39)], color=SLATE, sw=1.3)
f.box(396, 8, 176, 80, "", fill=MINT, stroke=TEAL)
f.text(484, 26, "success (real)", size=11, color=TEAL, bold=True)
f.text(484, 48, "connected to 10.11.19-", size=9.5, color=SLATE)
f.text(484, 62, "MariaDB | charset utf8mb4", size=9.5, color=SLATE)
f.text(484, 78, "closed", size=9.5, color=SLATE)
f.box(396, 100, 176, 96, "", fill=ROSE, stroke=RED)
f.text(484, 118, "wrong password (real)", size=11, color=RED, bold=True)
f.text(484, 140, "mysqli_sql_exception:", size=9.5, color=SLATE)
f.text(484, 154, "Access denied for user", size=9.5, color=SLATE)
f.text(484, 168, "'demo'@'localhost'", size=9.5, color=SLATE)
f.text(484, 184, "(using password: YES)", size=9.5, color=SLATE)
```

```svgfig label="4.2" caption="SQL injection and the prepared statement, one real experiment. The table users holds three rows. The login code builds the query by pasting the password into the text: the attacker types the password ' OR '1'='1, the query becomes WHERE name='ram' AND pass='' OR '1'='1', the last condition is always true, and the server returns all 3 rows, so the login is accepted. With a prepared statement the same text is sent as data, after the query has already been parsed, so it is only a very strange password and 0 rows match. The comment trick admin'-- also returned 1 row from the pasted query."
f = Fig(580, 214)
f.box(8, 8, 276, 198, "", fill=ROSE, stroke=RED)
f.text(146, 26, "Pasted into the query (unsafe)", size=11.5, color=RED, bold=True)
f.text(18, 50, "password typed by the attacker:", size=9.5, color=SLATE, anchor="start")
f.box(18, 56, 140, 22, "' OR '1'='1", fill="#ffffff", stroke=RED, size=11, bold=True, r=3)
f.text(18, 98, "query the server receives:", size=9.5, color=SLATE, anchor="start")
f.text(18, 116, "WHERE name='ram' AND pass=''", size=9.5, color=NAVY, anchor="start")
f.text(18, 132, "      OR '1'='1'", size=9.5, color=RED, bold=True, anchor="start")
f.box(18, 148, 256, 44, "rows returned: 3   (everyone)", fill="#ffffff", stroke=RED, size=12, bold=True)
f.box(296, 8, 276, 198, "", fill=MINT, stroke=TEAL)
f.text(434, 26, "Prepared statement (safe)", size=11.5, color=TEAL, bold=True)
f.text(306, 50, "step 1: parse the query once", size=9.5, color=SLATE, anchor="start")
f.text(306, 66, "WHERE name = ? AND pass = ?", size=9.5, color=NAVY, anchor="start")
f.text(306, 90, "step 2: send values as data", size=9.5, color=SLATE, anchor="start")
f.box(306, 98, 140, 22, "' OR '1'='1", fill="#ffffff", stroke=TEAL, size=11, bold=True, r=3)
f.text(306, 138, "the text can no longer change", size=9.5, color=TEAL, anchor="start")
f.text(306, 152, "the meaning of the query", size=9.5, color=TEAL, anchor="start")
f.box(306, 160, 256, 36, "rows returned: 0", fill="#ffffff", stroke=TEAL, size=12, bold=True)
```

```svgfig label="4.3" caption="One prepared statement, many executions, and real results of the CRUD run in Section 4.4. The INSERT is parsed once with three question marks and then run three times with different values; the server hands out the ids 1, 2 and 3 (insert_id) and each run reports affected_rows = 1. The UPDATE that adds 5 to the stock of book 3 reports affected_rows = 1; the DELETE of books with stock below 5 removes the 4-copy Physics book, and the two rows 1 and 3 remain. A statement that matches nothing reports affected_rows = 0, which is how a script knows that an update or a delete found no row."
f = Fig(580, 206)
f.box(8, 8, 170, 40, "", fill=BLUE, stroke=NAVY)
f.text(93, 24, "prepare once", size=11.5, color=NAVY, bold=True)
f.text(93, 40, "INSERT ... VALUES (?, ?, ?)", size=8.5, color=SLATE)
vals = [("Nepali Grammar", "450.00", "10"), ("Physics 12", "680.50", "4"), ("Maths 11", "520.00", "0")]
for i, (t, p, s) in enumerate(vals):
    y = 62 + i * 36
    f.arrow([(93, 50 if i == 0 else y - 6), (93, y)], color=SLATE, sw=1.3)
    f.box(8, y, 170, 30, "", fill="#ffffff", stroke=NAVY, r=4)
    f.text(16, y + 15, "execute: %s, %s, %s" % (t, p, s), size=8.5, color=SLATE, anchor="start", vmid=True)
    f.arrow([(180, y + 15), (214, y + 15)], color=TEAL, sw=1.4)
    f.box(216, y, 110, 30, "id %d  affected 1" % (i + 1), fill=MINT, stroke=TEAL, size=9.5, bold=True, r=4)
f.box(350, 8, 222, 40, "", fill=SAND, stroke=AMBER)
f.text(461, 24, "UPDATE stock = stock + 5, id 3", size=10, color=AMBER, bold=True)
f.text(461, 40, "affected_rows = 1  (stock 0 -> 5)", size=9.5, color=SLATE)
f.box(350, 58, 222, 40, "", fill=ROSE, stroke=RED)
f.text(461, 74, "DELETE WHERE stock < 5", size=10, color=RED, bold=True)
f.text(461, 90, "affected_rows = 1  (Physics 12 gone)", size=9.5, color=SLATE)
f.box(350, 108, 222, 90, "", fill=MINT, stroke=TEAL)
f.text(461, 126, "SELECT after the run (real)", size=10.5, color=TEAL, bold=True)
f.text(461, 148, "id 1  Nepali Grammar  stock 10", size=9.5, color=SLATE)
f.text(461, 166, "id 3  Maths 11  stock 5", size=9.5, color=SLATE)
f.text(461, 186, "2 rows remain", size=9.5, color=TEAL, bold=True)
```

```svgfig label="4.4" caption="A transaction is all or nothing, shown with the real PDO run of Section 4.5. Ram has 500 and Sita 300, total 800. Transfer 1 moves 200: both UPDATE statements succeed and commit() makes them permanent, giving 300 and 500. Transfer 2 tries to move 900: the first UPDATE would make Ram's balance negative, the CHECK constraint fails, rollBack() undoes everything, and the balances are still 300 and 500. In both cases the total stays 800.00, because money is never created or lost half-way."
f = Fig(580, 190)
f.text(96, 16, "start", size=11, color=NAVY, bold=True)
f.box(8, 24, 176, 40, "Ram 500   Sita 300", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.text(96, 78, "total 800", size=10, color=SLATE)
f.box(228, 12, 160, 62, "", fill=MINT, stroke=TEAL)
f.text(308, 28, "transfer 200", size=11, color=TEAL, bold=True)
f.text(308, 46, "2 UPDATEs, COMMIT", size=9.5, color=SLATE)
f.text(308, 62, "committed", size=10.5, color=TEAL, bold=True)
f.arrow([(186, 36), (226, 36)], color=TEAL, sw=1.6)
f.box(414, 24, 158, 40, "Ram 300   Sita 500", fill=MINT, stroke=TEAL, size=11, bold=True)
f.text(545, 78, "total 800.00", size=10, color=TEAL, bold=True)
f.box(228, 104, 160, 74, "", fill=ROSE, stroke=RED)
f.text(308, 120, "transfer 900", size=11, color=RED, bold=True)
f.text(308, 138, "UPDATE 1 breaks CHECK", size=9.5, color=SLATE)
f.text(308, 154, "ROLLBACK: undone", size=10, color=RED, bold=True)
f.text(308, 170, "(error 4025)", size=9.5, color=SLATE)
f.arrow([(493, 66), (493, 100)], color=SLATE, sw=1.4)
f.arrow([(414, 130), (390, 130)], color=RED, sw=1.6)
f.box(414, 112, 158, 40, "Ram 300   Sita 500", fill=MINT, stroke=TEAL, size=11, bold=True)
f.text(493, 168, "unchanged, total 800.00", size=10, color=TEAL, bold=True)
```

```svgfig label="4.5" caption="Pagination with LIMIT and OFFSET, real numbers. A table of 23 items shown 10 per page has ceil(23 / 10) = 3 pages. Page p starts at OFFSET (p - 1) x 10, so page 1 shows ids 1 to 10 (offset 0), page 2 shows ids 11 to 20 (offset 10) and page 3 shows ids 21 to 23 (offset 20, only 3 rows). The page number comes from the URL and must be forced to an integer of at least 1 before it is used, because it is user input."
f = Fig(580, 150)
f.text(8, 16, "SELECT id FROM item ORDER BY id LIMIT 10 OFFSET (page - 1) * 10", size=10, color=NAVY, bold=True, anchor="start")
pages = [("page 1", "offset 0", "ids 1 - 10", 10, BLUE, NAVY), ("page 2", "offset 10", "ids 11 - 20", 10, MINT, TEAL), ("page 3", "offset 20", "ids 21 - 23", 3, SAND, AMBER)]
for i, (a, b, c, n, fl, st) in enumerate(pages):
    x = 8 + i * 193
    f.box(x, 30, 180, 60, "", fill=fl, stroke=st)
    f.text(x + 90, 48, a + "   " + b, size=11, color=st, bold=True)
    f.text(x + 90, 66, c, size=10, color=SLATE)
    f.text(x + 90, 82, "%d rows" % n, size=10, color=st, bold=True)
for k in range(23):
    f.box(8 + k * 24.2, 104, 21, 20, str(k + 1), fill=BLUE if k < 10 else (MINT if k < 20 else SAND), stroke=NAVY if k < 10 else (TEAL if k < 20 else AMBER), size=10, r=3, sw=1)
f.text(290, 144, "23 rows, 10 per page: 3 pages (ceil of 2.3)", size=10.5, color=NAVY, bold=True)
```

### 4.7.1 Eight rules for safe PHP and MySQL code

1. **Always use prepared statements for user input.** Write the query with `?` or `:name` placeholders and send the values separately. The real experiment of Fig. 4.2 returned 3 rows for the pasted query and 0 for the prepared one. A login or search form of a college portal must never paste text into SQL.
2. **Turn on exceptions and catch them.** Set `mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT)` or use `PDO::ERRMODE_EXCEPTION`. A failed query then cannot be ignored by accident. In the `catch` block show a short message to the visitor and write the details to a log.
3. **Never use the database root account in a web page.** Create a user that has only the rights the site needs, such as `SELECT`, `INSERT` and `UPDATE` on one database. If an attacker finds a hole, the damage stays small. A result portal needs no right to `DROP TABLE`.
4. **Keep passwords outside the public folder.** Put the connection settings in a file above the web root, or in an environment variable, and load it with `require`. Never commit them to a public repository. A leaked password gives full access to every student's record.
5. **Set the character set to utf8mb4.** Call `set_charset('utf8mb4')` right after connecting, and create tables with the same set. Nepali names in Devanagari then travel to the server and back unchanged. A wrong set shows question marks.
6. **Group related changes in a transaction.** A fee payment that changes a balance and writes a receipt must happen entirely or not at all (Fig. 4.4). Use InnoDB tables, `beginTransaction()`, `commit()` and `rollBack()`. This protects wallets and ledgers from half-finished changes.
7. **Limit and page the results.** Use `LIMIT` and `OFFSET` with a page number forced to an integer (Fig. 4.5), and never print a whole table of ten thousand rows. A page of 10 or 20 rows loads quickly on a slow mobile connection. Add `ORDER BY` so that the pages are stable.
8. **Escape output and check what a change did.** Print every value from the database with `htmlspecialchars()`, and look at `affected_rows` after an update or delete (Fig. 4.3). A result of 0 means that no row matched, and the user should be told. Close the connection and free the result when the script is done.

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

## Model answers (5 and 10 marks)

**Q1. Explain how a PHP script connects to MySQL using `mysqli`. Write a program for the CRUD operations on a `book` table using prepared statements. (10 marks)**

**Introduction.** PHP talks to MySQL through an extension. The two common ones are `mysqli` (MySQL only) and PDO (many databases). A script must connect, run statements, read the result and close the connection (Fig. 4.1). The four basic database actions are called **CRUD**: Create (`INSERT`), Read (`SELECT`), Update (`UPDATE`) and Delete (`DELETE`).

**Steps.**

1. **Report errors as exceptions** with `mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT)`.
2. **Connect** with `new mysqli($host, $user, $password, $database)`.
3. **Set the character set** to `utf8mb4` so that Nepali text is stored correctly.
4. **Prepare** each statement with `?` placeholders, **bind** the values with `bind_param()` (the letters `s`, `i`, `d` mean string, integer, double) and **execute**.
5. **Check the effect** with `insert_id` and `affected_rows`.
6. **Read results** with `get_result()` and `fetch_assoc()`, and **close** the connection.

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$db = new mysqli("localhost", "demo", "demo123", "demo");
$db->set_charset("utf8mb4");
$db->query("DROP TABLE IF EXISTS book");
$db->query("CREATE TABLE book (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(60), price DECIMAL(8,2), stock INT)");

$ins = $db->prepare("INSERT INTO book (title, price, stock) VALUES (?, ?, ?)");
foreach ([["Nepali Grammar", 450.00, 10], ["Physics 12", 680.50, 4], ["Maths 11", 520.00, 0]] as [$t, $p, $s]) {
    $ins->bind_param("sdi", $t, $p, $s);
    $ins->execute();
    echo "created id ", $ins->insert_id, "\n";
}
$upd = $db->prepare("UPDATE book SET stock = stock + ? WHERE id = ?");
$add = 5; $id = 3;
$upd->bind_param("ii", $add, $id);
$upd->execute();
echo "updated rows: ", $upd->affected_rows, "\n";
$del = $db->prepare("DELETE FROM book WHERE stock < ?");
$min = 5;
$del->bind_param("i", $min);
$del->execute();
echo "deleted rows: ", $del->affected_rows, "\n";
$res = $db->query("SELECT id, title, price, stock FROM book ORDER BY id");
while ($r = $res->fetch_assoc()) {
    echo $r["id"], " ", $r["title"], " NPR ", $r["price"], " stock ", $r["stock"], "\n";
}
$db->query("DROP TABLE book");
$db->close();
```
```output
created id 1
created id 2
created id 3
updated rows: 1
deleted rows: 1
1 Nepali Grammar NPR 450.00 stock 10
3 Maths 11 NPR 520.00 stock 5
```

**Common mistakes and good practice.** Beginners often forget to set the character set, so Nepali names appear as question marks. They also forget to check the connection, so the page prints a warning that shows the server name and the user name to every visitor. Another frequent mistake is to keep the password inside a file in the public folder. The correct habits are: keep the settings in a file above the web root, give the web user only `SELECT`, `INSERT`, `UPDATE` and `DELETE` on the one database it needs, catch `mysqli_sql_exception` and show a short, friendly message, and free the result and close the connection when the work is done. A college result portal that follows these habits is both safer and easier to maintain.

**Reading the run (Fig. 4.3).** The three inserts gave the ids 1, 2 and 3; the update changed one row; the delete removed the book with stock below 5. The prepared forms mean that no user text is ever pasted into the SQL.

**Conclusion.** Connecting with exceptions on, using prepared statements for every value and checking `affected_rows` gives a safe and clear CRUD layer. The same four steps (connect, prepare, execute, fetch) are repeated in every PHP and MySQL application.

**Q2. What is SQL injection? How do prepared statements prevent it? (5 marks)**

**SQL injection** is an attack in which the input of a visitor changes the meaning of an SQL query. It happens when a script pastes the input into the query text, for example `"... WHERE name='$n' AND pass='$p'"`.

1. **The attack.** The attacker types the password `' OR '1'='1`. The query becomes `WHERE name='ram' AND pass='' OR '1'='1'`, and since the last condition is always true, the real run returned all 3 rows and the login would be accepted (Fig. 4.2).
2. **Other forms.** The comment trick `admin'-- ` cuts off the password test; `; DROP TABLE ...` tries to run a second statement; `UNION SELECT` reads other tables.
3. **The defence.** A prepared statement sends the query with placeholders first and the values afterwards as data. The server has already parsed the query, so the values cannot add a new condition. The same password returned 0 rows.
4. **Extra measures.** Give the web user minimum rights, hide database error messages from visitors, validate input, and store passwords with `password_hash()`.

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$db = new mysqli("localhost", "demo", "demo123", "demo");
$db->query("DROP TABLE IF EXISTS users");
$db->query("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(30), pass VARCHAR(30))");
$db->query("INSERT INTO users (name, pass) VALUES ('admin','s3cret'),('ram','pw1'),('sita','pw2')");
$n = "ram"; $p = "' OR '1'='1";
echo "pasted:   ", $db->query("SELECT id FROM users WHERE name='$n' AND pass='$p'")->num_rows, " rows\n";
$st = $db->prepare("SELECT id FROM users WHERE name = ? AND pass = ?");
$st->bind_param("ss", $n, $p);
$st->execute();
echo "prepared: ", $st->get_result()->num_rows, " rows\n";
$db->query("DROP TABLE users");
```
```output
pasted:   3 rows
prepared: 0 rows
```

Rule: **never concatenate input into SQL; always bind it.**

**Q3. Explain PDO. Compare it with `mysqli`, and describe a transaction with a bank-transfer program. (10 marks)**

**Introduction.** PDO (PHP Data Objects) is a single interface for many databases: MySQL, PostgreSQL, SQLite and others. Only the connection string (the DSN) names the database, so the rest of the code stays the same when the database is changed. It supports prepared statements with named placeholders such as `:amount`, and exceptions.

**Comparison.**

| Point | `mysqli` | PDO |
|---|---|---|
| Databases supported | MySQL and MariaDB only | about a dozen, through drivers |
| Style | procedural and object-oriented | object-oriented only |
| Placeholders | `?` only | `?` and named `:name` |
| Errors | exceptions with `mysqli_report` | `PDO::ERRMODE_EXCEPTION` |
| Fetch modes | `fetch_assoc`, `fetch_row` | `FETCH_ASSOC`, `FETCH_OBJ`, `FETCH_CLASS` and more |
| Speed | very slightly faster | almost the same |
| Typical use | small MySQL-only code | frameworks and larger projects |

**Transactions.** A transaction groups several statements into one unit. It follows the ACID rules: **A**tomic (all or nothing), **C**onsistent (constraints hold), **I**solated (other users do not see half-done work) and **D**urable (after commit, data survives a crash). The methods are `beginTransaction()`, `commit()` and `rollBack()`, and the tables must use InnoDB.

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=demo;charset=utf8mb4", "demo", "demo123",
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$pdo->exec("DROP TABLE IF EXISTS wallet");
$pdo->exec("CREATE TABLE wallet (id INT PRIMARY KEY, owner VARCHAR(20), balance DECIMAL(10,2) NOT NULL CHECK (balance >= 0)) ENGINE=InnoDB");
$pdo->exec("INSERT INTO wallet VALUES (1,'Ram',500),(2,'Sita',300)");

function pay(PDO $pdo, int $from, int $to, float $amount): string {
    try {
        $pdo->beginTransaction();
        $q = $pdo->prepare("UPDATE wallet SET balance = balance + :d WHERE id = :id");
        $q->execute([":d" => -$amount, ":id" => $from]);
        $q->execute([":d" => $amount, ":id" => $to]);
        $pdo->commit();
        return "committed";
    } catch (PDOException $e) {
        $pdo->rollBack();
        return "rolled back";
    }
}
echo pay($pdo, 1, 2, 200), " | ", pay($pdo, 1, 2, 900), "\n";
foreach ($pdo->query("SELECT owner, balance FROM wallet ORDER BY id") as $r) echo $r["owner"], " ", $r["balance"], "\n";
echo "total ", $pdo->query("SELECT SUM(balance) FROM wallet")->fetchColumn(), "\n";
$pdo->exec("DROP TABLE wallet");
```
```output
committed | rolled back
Ram 300.00
Sita 500.00
total 800.00
```

**Why a web application needs transactions.** A web request can fail at any moment: the server may restart, the connection may drop, or a constraint may refuse one of the statements. Without a transaction, a wallet payment could take money from Ram and fail before it gives it to Sita, so that 200 rupees would disappear. With a transaction the database itself guarantees that the two updates stand or fall together. The same idea protects a fee receipt and the matching ledger line, an exam seat booking and its payment, and the stock count of a shop against an order.

**Reading the result (Fig. 4.4).** The first payment committed. The second would make Ram's balance negative, the `CHECK` constraint refused it, `rollBack()` undid the first `UPDATE`, and the total stayed at 800.00.

**Conclusion.** PDO is preferred in larger projects for its uniform interface and named placeholders, while `mysqli` is adequate for MySQL-only code. Whichever is chosen, a transaction is the tool that keeps related changes, such as a fee payment and its receipt, consistent.

**Q4. How do you show the rows of a table page by page in PHP? Write the code and explain the calculations. (5 marks)**

Showing thousands of rows on one page is slow and unreadable, so a script shows a fixed number per page (pagination), using `LIMIT` and `OFFSET` in SQL.

1. **Count the rows:** `SELECT COUNT(*) FROM item` gives the total, here 23.
2. **Number of pages:** `ceil(total / per_page)`; with 10 per page that is 3.
3. **Read the page number** from the URL, `$_GET['page']`, and force it into range with `max(1, min($pages, (int) $page))`.
4. **Offset:** `($page - 1) * $per_page`; page 3 starts at offset 20.
5. **Query:** `SELECT ... ORDER BY id LIMIT 10 OFFSET 20`. Always add `ORDER BY`, or the pages may overlap.
6. **Links:** print "Previous" and "Next" links, and keep the search text in the link (Fig. 4.5).

```php
<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$db = new mysqli("localhost", "demo", "demo123", "demo");
$db->query("DROP TABLE IF EXISTS item");
$db->query("CREATE TABLE item (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20))");
for ($k = 1; $k <= 23; $k++) $db->query("INSERT INTO item (name) VALUES ('item$k')");
$per = 10;
$total = (int) $db->query("SELECT COUNT(*) FROM item")->fetch_row()[0];
$pages = (int) ceil($total / $per);
echo "total $total, pages $pages\n";
foreach ([1, 3, 9] as $asked) {
    $page = max(1, min($pages, $asked));
    $off = ($page - 1) * $per;
    $st = $db->prepare("SELECT id FROM item ORDER BY id LIMIT ? OFFSET ?");
    $st->bind_param("ii", $per, $off);
    $st->execute();
    $ids = array_column($st->get_result()->fetch_all(MYSQLI_ASSOC), "id");
    echo "asked $asked -> page $page, offset $off, ", count($ids), " rows (ids ", $ids[0], "-", end($ids), ")\n";
}
$db->query("DROP TABLE item");
```
```output
total 23, pages 3
asked 1 -> page 1, offset 0, 10 rows (ids 1-10)
asked 3 -> page 3, offset 20, 3 rows (ids 21-23)
asked 9 -> page 3, offset 20, 3 rows (ids 21-23)
```

The request for page 9 was forced to page 3, and the last page held only 3 rows. Forcing the page number into range is also a security step, because the value comes from the user.

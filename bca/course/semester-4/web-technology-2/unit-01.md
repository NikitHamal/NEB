---
subject: Web Technology II
grade: BCA Semester 4
unit: 1
title: Server-Side Scripting and PHP Fundamentals
hours: 8
area: BCA 255 · Web Technology II · Unit 1
---

In Web Technology I your pages came to life in the browser with JavaScript. But the browser cannot read the college's student database, check a password safely or send an e-mail: that work happens on a **server**. This unit introduces server-side scripting and the language that powers most of the web's server side, **PHP**: its syntax, types, control structures, arrays and functions.

::: key What this unit gives you
- How a dynamic page is produced: request, server-side script, response.
- PHP syntax, variables, types, operators, control structures, arrays, `foreach`, functions, and `include`.
- Running PHP from the command line, so you can test every example.
:::

Every PHP program in this book was run with **PHP 8.2** from the command line; the output shown is real. A web server runs the same code and sends its output to the browser. Programs begin with the opening tag `<?php`.

## 1.1 Client-side versus server-side scripting

| | Client-side (JavaScript) | Server-side (PHP) |
|---|---|---|
| Runs on | the user's browser | the web server |
| Source visible to the user | yes | **no**, only the output is sent |
| Can access | the page, the browser | files, databases, e-mail, other servers |
| Typical tasks | validation hints, animation, AJAX calls | login, saving data, reports, payments |
| Trust | none: the user can change it | the server is trusted, but must never trust the **input** |

**How a dynamic page is produced.** (1) The browser sends an HTTP request for `result.php`. (2) The web server (Apache, Nginx) sees the `.php` extension and passes the file to the PHP interpreter. (3) PHP runs the code, perhaps querying MySQL, and produces HTML. (4) The server sends that HTML back as the response. The browser never sees the PHP code. The classic **LAMP** stack is **L**inux + **A**pache + **M**ySQL + **P**HP (on Windows, XAMPP or WAMP bundles them). For development PHP also has a built-in server: `php -S localhost:8000`.

**Features of PHP.** Free and open source, runs on all major platforms and servers, simple C-like syntax, loosely typed (with optional strict types), embedded in HTML, a huge function library, easy database connectivity (MySQL, PostgreSQL, SQLite), and the engine behind WordPress, Joomla, Laravel and Wikipedia's MediaWiki.

```php
<?php
echo "Hello from PHP ", PHP_VERSION_ID >= 80000 ? "8+" : "7", "\n";
print("Namaste\n");
?>
<p>Today is a plain HTML line, outside the PHP tags.</p>
<?= "short echo tag: " . 6 * 7 ?>
```
```output
Hello from PHP 8+
Namaste
<p>Today is a plain HTML line, outside the PHP tags.</p>
short echo tag: 42
```
Anything outside `<?php … ?>` is sent unchanged, so PHP can be mixed into HTML templates. Statements end with `;`. Comments: `// line`, `# line`, `/* block */`.

## 1.2 Variables, constants and types

Variables begin with `$`, are case-sensitive, and need no declaration. PHP is **loosely typed**: the type belongs to the value and may change. Constants are defined with `const NAME = value;` or `define()`.

```php
<?php
$name = "Sita"; $age = 20; $gpa = 3.75; $enrolled = true; $nothing = null;
const COLLEGE = "Patan";
var_dump($name, $age, $gpa, $enrolled, $nothing);
echo gettype($age), " ", gettype("5" + 5), " ", "5" + "5.5", " ", "3" . 4, "\n";
echo "Hello $name, you are {$age} years old at " . COLLEGE . "\n";
echo 'Single quotes do not expand $name', "\n";
echo intdiv(17, 5), " ", 17 % 5, " ", 2 ** 10, " ", 7 / 2, " ", (int) "42abc", "\n";
```
```output
string(4) "Sita"
int(20)
float(3.75)
bool(true)
NULL
integer integer 10.5 34
Hello Sita, you are 20 years old at Patan
Single quotes do not expand $name
3 2 1024 3.5 42
```
**Types:** `int`, `float`, `string`, `bool`, `array`, `object`, `null`, `callable`. **Double-quoted strings** expand variables and escapes (`\n`); **single-quoted** do not. `.` concatenates (PHP uses `+` only for numbers). **Type juggling:** `"5" + 5` is 10 and `"5" + "5.5"` is 10.5. PHP 8 throws a `TypeError` for non-numeric strings in arithmetic, and compares more sensibly than PHP 7 did, but you should still use `===`.

### Comparison: `==` versus `===`

`==` compares after type conversion; `===` also demands the same type. Prefer `===` and `!==`.

```php
<?php
var_dump(0 == "a", "1" == "01", "10" == "1e1", 100 == "1e2", null == false);
var_dump(0 === "a", "1" === "01", null === false, 1 <=> 2, "b" <=> "a");
var_dump(null ?? "default", isset($undefined), empty("0"), empty([]));
$score = 55;
echo $score >= 40 ? "pass" : "fail", " ", $score <=> 50, "\n";
```
```output
bool(false)
bool(true)
bool(true)
bool(true)
bool(true)
bool(false)
bool(false)
bool(false)
int(-1)
int(1)
string(7) "default"
bool(false)
bool(true)
bool(true)
pass 1
```
The **null coalescing operator** `??` supplies a default when a value is unset or null; `<=>` (spaceship) returns −1, 0 or 1; `empty()` treats `"0"`, `0`, `""`, `[]`, `null`, `false` as empty.

### Operators

Arithmetic `+ - * / % **` (and `intdiv`), assignment `= += -= .= ??=`, comparison `== === != !== < > <= >= <=>`, logical `&& || ! and or xor`, increment `++ --`, string `.`, ternary `?:`, null-coalescing `??`, array `+` (union). Precedence is like C; `&&` binds tighter than `||`; use parentheses.

## 1.3 Control structures

```php
<?php
$marks = 67;
if ($marks >= 80) { $g = "Distinction"; }
elseif ($marks >= 60) { $g = "First"; }
else { $g = "Other"; }
echo "$marks => $g\n";

switch (date("N", strtotime("2026-11-02"))) {      // 1 = Monday
    case 6: echo "Saturday: holiday\n"; break;
    case 1: case 2: echo "weekday near the start\n"; break;
    default: echo "other day\n";
}
echo match (true) { $marks >= 80 => "A", $marks >= 60 => "B", default => "C" }, "\n";

for ($i = 1; $i <= 5; $i++) { echo $i * $i, " "; }
$n = 5; $f = 1;
while ($n > 1) { $f *= $n--; }
do { echo "[do-while runs once: $f]"; } while (false);
echo "\n";
for ($i = 0; $i < 10; $i++) {
    if ($i % 2) continue;
    if ($i > 6) break;
    echo $i, ",";
}
echo "\n";
```
```output
67 => First
weekday near the start
B
1 4 9 16 25 [do-while runs once: 120]
0,2,4,6,
```
`switch` uses loose comparison and needs `break`; the PHP 8 **`match`** expression uses strict comparison, returns a value and has no fall-through. Loops: `for`, `while`, `do … while`, `foreach` (below); `break` and `continue` work as in C.

## 1.4 Arrays

PHP's **array** is an ordered map: it serves as list, dictionary, stack and queue. Keys are integers or strings.

```php
<?php
$days = ["Sun", "Mon", "Tue"];                 // indexed
$days[] = "Wed";
$student = ["name" => "Ram", "age" => 19, "marks" => [78, 85]];   // associative
$student["dept"] = "BCA";
echo count($days), " ", $days[1], " ", $student["marks"][1], " ", implode(",", array_keys($student)), "\n";
foreach ($days as $i => $d) { echo "$i=$d "; }
echo "\n";
foreach ($student as $key => $value) {
    echo $key, ": ", is_array($value) ? implode("/", $value) : $value, "\n";
}
print_r(array_slice($days, 1, 2));
var_dump(in_array("Tue", $days), array_search("Wed", $days), isset($student["phone"]));
```
```output
4 Mon 85 name,age,marks,dept
0=Sun 1=Mon 2=Tue 3=Wed 
name: Ram
age: 19
marks: 78/85
dept: BCA
Array
(
    [0] => Mon
    [1] => Tue
)
bool(true)
int(3)
bool(false)
```
| Function | Purpose |
|---|---|
| `count`, `array_keys`, `array_values`, `array_merge` | inspect and combine |
| `array_push`/`[]`, `array_pop`, `array_shift`, `array_unshift` | stack and queue |
| `in_array`, `array_search`, `array_key_exists` | search |
| `sort`, `rsort`, `asort`, `ksort`, `usort` | sorting (by value, key, custom) |
| `array_map`, `array_filter`, `array_reduce`, `array_sum` | functional style |
| `array_slice`, `array_splice`, `array_unique`, `array_column` | slicing and shaping |

```php
<?php
$marks = ["Ram" => 78, "Sita" => 92, "Hari" => 64, "Gita" => 85];
arsort($marks);
print_r($marks);
$passed = array_filter($marks, fn($m) => $m >= 70);
echo implode(", ", array_keys($passed)), " | avg ", round(array_sum($marks) / count($marks), 2), "\n";
$sq = array_map(fn($x) => $x ** 2, [1, 2, 3, 4]);
echo implode(" ", $sq), " | ", array_reduce($sq, fn($c, $x) => $c + $x, 0), "\n";
$rows = [["n" => "Ram", "m" => 78], ["n" => "Sita", "m" => 92]];
usort($rows, fn($a, $b) => $b["m"] <=> $a["m"]);
echo implode(",", array_column($rows, "n")), "\n";
```
```output
Array
(
    [Sita] => 92
    [Gita] => 85
    [Ram] => 78
    [Hari] => 64
)
Sita, Gita, Ram | avg 79.75
1 4 9 16 | 30
Sita,Ram
```
## 1.5 Functions

```php
<?php
declare(strict_types=1);

function area(float $w, float $h = 1.0): float { return $w * $h; }
function swap(int &$a, int &$b): void { [$a, $b] = [$b, $a]; }
function total(int ...$nums): int { return array_sum($nums); }
function greet(string $name, string $greeting = "Hello"): string { return "$greeting, $name!"; }

echo area(3, 4), " ", area(5), " ", total(1, 2, 3, 4), " ", greet(greeting: "Namaste", name: "Sita"), "\n";
$x = 1; $y = 2; swap($x, $y); echo "$x $y\n";
$counter = function () { static $n = 0; return ++$n; };
echo $counter(), $counter(), $counter(), "\n";
try { echo area("abc"); } catch (TypeError $e) { echo "TypeError caught\n"; }
```
```output
12 5 10 Namaste, Sita!
2 1
123
TypeError caught
```
Type declarations (`int`, `float`, `string`, `bool`, `array`, `?int` nullable, `int|string` union) and return types make code self-documenting; with `strict_types=1` PHP refuses silent conversions. Parameters can have defaults, be **passed by reference** (`&`), be **variadic** (`...$nums`) and be **named** at the call (PHP 8). **Scope:** variables inside a function are local; use `global $x` or, better, parameters. `static` variables keep their value between calls. Arrow functions `fn($x) => …` capture outer variables automatically.

### Useful string and math functions

```php
<?php
$s = "  Kathmandu Valley  ";
echo strlen(trim($s)), "|", strtoupper(trim($s)), "|", ucwords("bca fourth semester"), "|", str_replace("Valley", "City", trim($s)), "\n";
echo substr("Pokhara", 0, 4), " ", strpos("Pokhara", "k"), " ", str_contains("Pokhara", "kha") ? "yes" : "no", " ", strrev("abc"), " ", str_pad("7", 3, "0", STR_PAD_LEFT), "\n";
print_r(explode(",", "a,b,c")); echo sprintf("%05.1f|%-6s|%3d|%x", 3.14159, "ab", 42, 255), " ", number_format(1234567.891, 2), "\n";
echo max(3, 9, 4), " ", round(2.567, 1), " ", floor(-1.5), " ", abs(-8), " ", sqrt(144), " ", pi() > 3 ? "pi" : "", "\n";
```
```output
16|KATHMANDU VALLEY|Bca Fourth Semester|Kathmandu City
Pokh 2 yes cba 007
Array
(
    [0] => a
    [1] => b
    [2] => c
)
003.1|ab    | 42|ff 1,234,567.89
9 2.6 -2 8 12 pi
```
## 1.6 Including files and running from the command line

`include 'header.php'` inserts another file (a warning if it is missing, and it returns `false`); `require` stops with a fatal error if missing; the `_once` variants avoid loading twice. Use them for shared headers, footers and configuration.

```php
<?php
file_put_contents("config.php", '<?php return ["site" => "BCA Portal", "year" => 2026];');
file_put_contents("lib.php", '<?php function banner(string $t): string { return "== $t =="; }');
$config = require "config.php";
require_once "lib.php";
require_once "lib.php";
echo banner($config["site"]), " ", $config["year"], "\n";
$r = @include "missing.php";
var_dump($r);
echo basename(__FILE__), " line ", __LINE__, "\n";
```
```output
== BCA Portal == 2026
bool(false)
p.php line 10
```
Run a script with `php script.php`; pass arguments through `$argv`. The built-in web server is started with `php -S localhost:8000`.

## Formula and fact sheet

- Server-side code runs on the server; the browser receives only its output.
- `$var`, `const`, `===` vs `==`, `??`, `<=>`; double quotes expand, single quotes do not; `.` concatenates.
- `if/elseif/else`, `switch`, `match`, `for`, `while`, `foreach ($a as $k => $v)`.
- Arrays are ordered maps; `[]` appends; `count`, `sort`, `array_map`, `array_filter`.
- `function f(int $x = 1): int`; `&` by reference; `...` variadic; `declare(strict_types=1)`.
- `include`, `require`, `require_once`.

## Chapter summary

- PHP runs on the server, generates HTML dynamically and can reach files and databases; the browser never sees the source.
- The language is loosely typed, with strict mode and type declarations available; use `===`.
- Arrays are the universal data structure; functions can take defaults, references, variadics and named arguments.
- Files are shared with `include`/`require`; the command line and the built-in server make testing easy.

## Practice

1. Differentiate client-side and server-side scripting, and explain the steps in producing a dynamic page.
2. What is the difference between `==` and `===`? Predict `var_dump("10" == "1e1", "10" === "1e1")`.
3. Write a PHP script that prints the multiplication table of 7.
4. Create an associative array of five students' marks and print the names with marks above the average.
5. Write a function with a default parameter and one that takes its argument by reference.
6. Differentiate `include` and `require`.
7. Explain the output of `echo "5" + "5", "5" . "5";`.

::: note Answers and worked solutions
**1.** See Section 1.1: client-side code runs in the browser and is visible; server-side code runs on the server and only its output is sent. Steps: request → web server → PHP interpreter runs script (and database) → HTML response.
**2.** `==` converts types before comparing, `===` requires equal types and values. `"10" == "1e1"` is true (both numeric strings, 10 = 10.0); `"10" === "1e1"` is false.
**3.**

```php
<?php
for ($i = 1; $i <= 10; $i++) { echo "7 x $i = ", 7 * $i, "\n"; }
```
```output
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```
**4.**

```php
<?php
$m = ["Ram" => 78, "Sita" => 92, "Hari" => 64, "Gita" => 85, "Bikash" => 55];
$avg = array_sum($m) / count($m);
foreach ($m as $n => $v) { if ($v > $avg) echo "$n ($v)\n"; }
echo "average $avg\n";
```
```output
Ram (78)
Sita (92)
Gita (85)
average 74.8
```
**5.**

```php
<?php
function power(int $b, int $e = 2): int { return $b ** $e; }
function addTax(float &$price): void { $price *= 1.13; }
$p = 100.0; addTax($p);
echo power(5), " ", power(2, 8), " ", $p, "\n";
```
```output
25 256 113
```
**6.** `include` raises a warning and continues if the file is missing; `require` raises a fatal error and stops. Use `require` for essential files.
**7.** `"5" + "5"` adds numerically to 10; `"5" . "5"` concatenates to `55`; `echo` with a comma prints both: `1055`.
:::

---
subject: Web Technology II
grade: BCA Semester 4
unit: 6
title: AJAX, JSON and Web APIs
hours: 6
area: BCA 255 · Web Technology II · Unit 6
---

When you type in a search box and suggestions appear without the page reloading, or a "like" count changes in place, the browser has made a background request and updated only part of the page. That technique is **AJAX** (Asynchronous JavaScript and XML), now almost always carried by JSON. This unit shows both sides: PHP endpoints that return JSON, and the JavaScript (from Web Technology I) that calls them.

::: key What this unit gives you
- JSON encoding and decoding in PHP.
- Writing a PHP endpoint (an API) and testing it over real HTTP.
- AJAX from the browser: `XMLHttpRequest`, `fetch`, jQuery; with PHP and with PHP + MySQL.
:::

**What was executed.** The PHP code was run on PHP 8.2 (including a real HTTP request to PHP's built-in web server). The JavaScript snippets are shown but were **not machine-executed** in this book, because they need a browser; check them in your browser's developer tools.

## 6.1 JSON in PHP

**JSON** is a text format for structured data: objects `{"k": v}`, arrays `[…]`, strings, numbers, `true/false/null`.

```php
<?php
$student = ["name" => "Sita", "marks" => [88, 92.5], "passed" => true, "address" => null, "note" => "नमस्ते"];
$json = json_encode($student, JSON_UNESCAPED_UNICODE);
echo $json, "\n";
echo json_encode($student, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
$back = json_decode($json, true);                       // true = associative arrays
echo $back["marks"][1], " ", var_export($back["passed"], true), "\n";
$obj = json_decode('{"a": {"b": [1, 2, 3]}}');           // objects
echo $obj->a->b[2], " ", count($obj->a->b), "\n";
var_dump(json_decode("{bad json}"), json_last_error_msg());
try { json_decode("{bad", false, 512, JSON_THROW_ON_ERROR); } catch (JsonException $e) { echo "JsonException: ", $e->getMessage(), "\n"; }
```
```output
{"name":"Sita","marks":[88,92.5],"passed":true,"address":null,"note":"नमस्ते"}
{
    "name": "Sita",
    "marks": [
        88,
        92.5
    ],
    "passed": true,
    "address": null,
    "note": "नमस्ते"
}
92.5 true
3 3
NULL
string(12) "Syntax error"
JsonException: Syntax error
```
`json_encode` turns arrays and objects into JSON text; `json_decode($text, true)` turns JSON into associative arrays. Always check for errors (`JSON_THROW_ON_ERROR` is the neatest).

## 6.2 A PHP endpoint and a real HTTP request

An **endpoint** is a PHP script that returns data (JSON) instead of a page. It must set the `Content-Type` header and send only JSON. The program below creates an endpoint file, starts PHP's built-in web server on port 8089, makes real HTTP requests (GET with a query string and POST with JSON), prints what came back, and stops the server.

```php
<?php
$dir = sys_get_temp_dir() . "/api_" . getmypid(); mkdir($dir);
file_put_contents("$dir/api.php", <<<'PHP'
<?php
header("Content-Type: application/json; charset=utf-8");
$method = $_SERVER["REQUEST_METHOD"];
if ($method === "GET") {
    $q = trim($_GET["q"] ?? "");
    $all = ["Kathmandu", "Pokhara", "Patan", "Bhaktapur", "Biratnagar"];
    $hits = array_values(array_filter($all, fn($c) => $q !== "" && stripos($c, $q) === 0));
    echo json_encode(["query" => $q, "matches" => $hits]);
} elseif ($method === "POST") {
    $in = json_decode(file_get_contents("php://input"), true);
    if (!is_array($in) || !isset($in["name"])) { http_response_code(400); echo json_encode(["error" => "name required"]); exit; }
    http_response_code(201);
    echo json_encode(["id" => 101, "saved" => htmlspecialchars($in["name"])]);
}
PHP);
$proc = proc_open(["php", "-S", "127.0.0.1:8089", "-t", $dir], [1 => ["file", "/dev/null", "w"], 2 => ["file", "/dev/null", "w"]], $pipes);
for ($i = 0; $i < 30 && @file_get_contents("http://127.0.0.1:8089/api.php") === false; $i++) usleep(200000);

$res = file_get_contents("http://127.0.0.1:8089/api.php?q=pa");
echo $http_response_header[0], " | ", $res, "\n";
function post(string $body): string {
    $ctx = stream_context_create(["http" => ["method" => "POST", "header" => "Content-Type: application/json", "content" => $body, "ignore_errors" => true]]);
    $r = file_get_contents("http://127.0.0.1:8089/api.php", false, $ctx);
    global $http_response_header;
    return $http_response_header[0] . " | " . $r;
}
echo post('{"name": "Sita <b>"}'), "\n";
echo post('{"age": 20}'), "\n";
proc_terminate($proc);
```
```output
HTTP/1.1 200 OK | {"query":"pa","matches":["Patan"]}
HTTP/1.1 200 OK | {"id":101,"saved":"Sita &lt;b&gt;"}
HTTP/1.1 200 OK | {"error":"name required"}
```
Notice the **HTTP status codes** that a good API returns: `200 OK`, `201 Created` after a `POST`, `400 Bad Request` for invalid input, and (not shown) `404`, `401`, `500`. The name `Sita <b>` came back escaped, so it can safely be inserted into a page.

**REST** style: URLs name *resources* (`/students/14`), HTTP methods give the action (`GET` read, `POST` create, `PUT`/`PATCH` update, `DELETE` remove), and responses are JSON with proper status codes.

## 6.3 AJAX from the browser

The browser object `XMLHttpRequest` (older) and the `fetch()` function (modern, returns a Promise) send a request without leaving the page. The pattern: **event → request → response → update the DOM**.

```js
// modern: fetch + async/await
async function suggest(prefix) {
  const res = await fetch("api.php?q=" + encodeURIComponent(prefix));
  if (!res.ok) throw new Error("HTTP " + res.status);
  const data = await res.json();                  // parse the JSON body
  document.getElementById("list").innerHTML =
    data.matches.map(m => "<li>" + m + "</li>").join("");   // see the XSS warning below
}
document.getElementById("box").addEventListener("input", e => suggest(e.target.value));

// POST JSON
fetch("api.php", { method: "POST",
                   headers: { "Content-Type": "application/json" },
                   body: JSON.stringify({ name: "Sita" }) })
  .then(r => r.json()).then(console.log);
```

```js
// older: XMLHttpRequest
const xhr = new XMLHttpRequest();
xhr.open("GET", "api.php?q=pa");
xhr.onreadystatechange = function () {
  if (xhr.readyState === 4 && xhr.status === 200) {      // 4 = DONE
    console.log(JSON.parse(xhr.responseText));
  }
};
xhr.send();

// jQuery (Web Technology I, Unit 6)
$.getJSON("api.php", { q: "pa" }, function (data) { $("#list").text(data.matches.join(", ")); });
$.ajax({ url: "api.php", method: "POST", contentType: "application/json",
         data: JSON.stringify({ name: "Sita" }), success: r => console.log(r) });
```

**`readyState`** goes 0 (unsent), 1 (opened), 2 (headers received), 3 (loading), 4 (done). Requests are **asynchronous**: the page stays responsive and your code runs in a callback or after `await`.

::: caution XSS in AJAX code
Putting server data into `innerHTML` is dangerous if it contains markup. Use `textContent` (or build elements) for untrusted text, and escape in PHP with `htmlspecialchars` as the endpoint above did.
:::

### Same-origin policy and CORS

The browser lets a page call only its **own origin** (scheme + host + port) unless the other server opts in with the header `Access-Control-Allow-Origin`. If your front end at `localhost:3000` calls an API at `localhost:8000`, the API must send that header. This is a browser rule: tools such as `curl` are not affected.

## 6.4 AJAX with PHP and MySQL

A live search joins the earlier units: the browser sends the prefix, PHP queries MySQL with a prepared statement and returns JSON.

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=demo;charset=utf8mb4", "demo", "demo123", [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$pdo->exec("DROP TABLE IF EXISTS city");
$pdo->exec("CREATE TABLE city (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(40), population INT)");
$pdo->exec("INSERT INTO city (name, population) VALUES ('Kathmandu', 845767), ('Pokhara', 518452), ('Patan', 284922), ('Bhaktapur', 81748), ('Biratnagar', 244750)");

function search(PDO $pdo, string $prefix): string {            // what the endpoint would echo
    $st = $pdo->prepare("SELECT name, population FROM city WHERE name LIKE :p ORDER BY population DESC LIMIT 5");
    $st->execute([":p" => addcslashes($prefix, "%_\\") . "%"]);
    return json_encode(["query" => $prefix, "results" => $st->fetchAll()]);
}
echo search($pdo, "Pa"), "\n";
echo search($pdo, "B"), "\n";
echo search($pdo, "' OR '1'='1"), "\n";
```
```output
{"query":"Pa","results":[{"name":"Patan","population":284922}]}
{"query":"B","results":[{"name":"Biratnagar","population":244750},{"name":"Bhaktapur","population":81748}]}
{"query":"' OR '1'='1","results":[]}
```
The third call is an injection attempt; because the query is prepared, it is just an unusual prefix and matches nothing. (Population figures are illustrative.)

## Formula and fact sheet

- `json_encode($data, flags)`, `json_decode($text, true)`, `JSON_THROW_ON_ERROR`, `JSON_UNESCAPED_UNICODE`.
- Endpoint: `header("Content-Type: application/json")`, `http_response_code(n)`, `php://input` for the body.
- Status codes: 200, 201, 400, 401, 404, 500. REST: resource URLs, verbs `GET POST PUT DELETE`.
- Browser: `fetch(url).then(r => r.json())`, `XMLHttpRequest` (`readyState` 4, `status` 200), `$.ajax`.
- Same-origin policy; CORS via `Access-Control-Allow-Origin`.

## Chapter summary

- AJAX updates part of a page using a background request; JSON is the usual data format.
- A PHP endpoint decodes input, validates it, uses prepared statements, and returns JSON with correct headers and status codes.
- The browser side uses `fetch` or `XMLHttpRequest` (or jQuery); output inserted into the page must be escaped.

## Practice

1. Define AJAX and list its advantages.
2. Convert a PHP array into JSON and back; what does the second argument of `json_decode` do?
3. Write a PHP endpoint that returns `{"sum": a+b}` for `?a=2&b=3`, validating that both are numbers.
4. Show the JavaScript that calls it and displays the sum.
5. Explain the states of `XMLHttpRequest.readyState`.
6. What are the same-origin policy and CORS?
7. Why does the live-search endpoint use a prepared statement?

::: note Answers and worked solutions
**1.** AJAX updates parts of a page via asynchronous background requests. Advantages: no page reload, faster feel, less data transferred, richer interfaces.
**2.**

```php
<?php
$a = ["x" => 1, "y" => [2, 3]];
$j = json_encode($a);
echo $j, " ", json_decode($j, true)["y"][1], " ", json_decode($j)->x, "\n";
```
```output
{"x":1,"y":[2,3]} 3 1
```
With `true`, objects become associative arrays; without it they become `stdClass` objects.
**3.**

```php
<?php
// the logic of sum.php, with a simulated query string
$_GET = ["a" => "2", "b" => "3"];
$a = filter_var($_GET["a"] ?? null, FILTER_VALIDATE_FLOAT);
$b = filter_var($_GET["b"] ?? null, FILTER_VALIDATE_FLOAT);
if ($a === false || $b === false) { http_response_code(400); echo json_encode(["error" => "numbers required"]); }
else echo json_encode(["sum" => $a + $b]);
```
```output
{"sum":5}
```
**4.**

```js
fetch("sum.php?a=2&b=3").then(r => r.json())
  .then(d => document.getElementById("out").textContent = d.sum);
```

**5.** 0 UNSENT, 1 OPENED (`open` called), 2 HEADERS_RECEIVED, 3 LOADING (body arriving), 4 DONE; check `readyState === 4 && status === 200`.
**6.** The browser lets scripts call only the same scheme, host and port as the page. CORS lets a server relax this by sending `Access-Control-Allow-Origin` for trusted origins.
**7.** The prefix comes from the user (the search box). Binding it as a parameter stops SQL injection (third call in Section 6.4).
:::

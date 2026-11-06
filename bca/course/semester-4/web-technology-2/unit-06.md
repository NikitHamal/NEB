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

**What was executed.** The PHP code was run on PHP 8.2 (including a real HTTP request to PHP's built-in web server). The older JavaScript snippets in Sections 6.3 are shown but were **not machine-executed**, because they need a browser; check them in your browser's developer tools. The `fetch` programs in the model answers and the figures of Section 6.5 were run for real with Node 22 against a live PHP endpoint.

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

## 6.5 Seeing the ideas: AJAX, JSON and REST

A page that updates itself is really three ideas working together: a browser that can ask for data in the background (**AJAX**), a text format that both sides understand (**JSON**), and a set of rules for naming and answering requests (**REST**). The plate puts a face to each idea, and the figures that follow show the real bytes, status codes, event order and headers measured on PHP 8.2.35 and Node 22 with a small endpoint called over real HTTP.

```svgfig label="6.1" caption="Why AJAX feels faster, with measured sizes. The same city search was run twice against PHP 8.2.35. The classic way (a form submit) returns a complete page of 484 bytes: head, menu, form, list and footer all travel again and the whole window repaints. The AJAX way (fetch to the endpoint) returns only the answer as JSON, 34 bytes, and one list on the page is updated. The bars are drawn to scale, so the JSON reply is about one fourteenth of the page. Here the page is tiny; a real page with images, scripts and styles is many kilobytes, so the saving grows."
f = Fig(580, 168)
f.text(8, 12, "Classic form submit", size=12, color=NAVY, bold=True, anchor="start")
f.box(8, 22, 96, 30, "click Search", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.arrow([(104, 37), (140, 37)], color=SLATE)
f.box(142, 22, 400, 30, "full page: 484 bytes (head, menu, form, list, footer)", fill=ROSE, stroke=RED, size=11, bold=True)
f.text(8, 66, "the browser throws the old page away and repaints everything", size=10.5, color=RED, anchor="start")
f.line(8, 78, 572, 78, color="#cbd5e1", sw=1)
f.text(8, 94, "AJAX with fetch", size=12, color=NAVY, bold=True, anchor="start")
f.box(8, 104, 96, 30, "type 'pa'", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.arrow([(104, 119), (140, 119)], color=SLATE)
f.box(142, 104, 28, 30, "", fill=MINT, stroke=TEAL)
f.text(184, 119, "JSON only: 34 bytes", size=11, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(8, 148, "script updates one list; the menu, form and footer stay as they were", size=10.5, color=TEAL, anchor="start")
f.text(8, 162, "bar lengths to scale: 484 bytes = 400 px, 34 bytes = 28 px", size=10, color=SLATE, anchor="start")
```

```photogrid label="6.1" cols="4" ratio="1.0" caption="Three ideas and one picture to remember them. (a) Jesse James Garrett, who gave the technique its name AJAX in a 2005 essay, speaking at a web conference. (b) Douglas Crockford, who specified and popularised JSON as the plain-text data format that replaced XML in most web APIs. (c) Roy Fielding, who defined REST in his 2000 doctoral dissertation and also helped write HTTP and the Apache web server. (d) A waiter carrying drinks on a tray: the customer never enters the kitchen, he sends a short order and gets a ready item back, exactly how a client uses a web API."
@ photo id="bca255/garrett" cap="Garrett: named AJAX"
fit 1.0
focus 0.6 0.5
@ photo id="bca255/crockford" cap="Crockford: JSON"
fit 1.0
focus 0.5 0.45
@ photo id="bca255/fielding" cap="Fielding: REST"
fit 1.0
focus 0.55 0.5
@ photo id="bca255/waiter" cap="The waiter: an API"
fit 1.0
focus 0.75 0.5
```

```svgfig label="6.2" caption="How json_encode maps PHP values to JSON text (real PHP 8.2.35 results). A list with keys 0, 1, 2 becomes a JSON array; any other key pattern becomes an object, so the array with keys 1 and 2 turns into an object with the keys as strings, a classic surprise for beginners. An empty array is [] but an empty object is {}. The value 1.0 is written as 1 unless JSON_PRESERVE_ZERO_FRACTION is given. NAN cannot be encoded: the function returns false and json_last_error_msg says why. Slashes are escaped as backslash-slash, and Nepali text becomes escape sequences of 47 bytes unless JSON_UNESCAPED_UNICODE is used (29 bytes)."
f = Fig(580, 330)
f.box(8, 8, 270, 26, "PHP value", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
f.box(282, 8, 290, 26, "json_encode result", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
rows = [("[1, 2]  (keys 0, 1)", "[1,2]", 0),
        ("['a' => 1]", "{\"a\":1}", 0),
        ("[0 => 'a', 1 => 'b']", "[\"a\",\"b\"]", 0),
        ("[1 => 'a', 2 => 'b']  (keys start at 1)", "{\"1\":\"a\",\"2\":\"b\"}", 1),
        ("[]   and   new stdClass", "[]   and   {}", 0),
        ("92.5   and   1.0", "92.5   and   1", 1),
        ("true, null", "true, null", 0),
        ("NAN", "false  (Inf and NaN cannot be encoded)", 1),
        ("'a/b'", "\"a\\/b\"   (slash is escaped)", 0),
        ("'नमस्ते' (default)", "\\u0928\\u092e...   47 bytes", 1),
        ("'नमस्ते' + JSON_UNESCAPED_UNICODE", "\"नमस्ते\"   29 bytes", 0)]
for i, (a, b, warn) in enumerate(rows):
    y = 38 + i * 24
    f.box(8, y, 270, 22, a, fill=SAND if warn else SOFT, stroke=AMBER if warn else SLATE, size=10, r=3, bold=False)
    f.box(282, y, 290, 22, b, fill=SAND if warn else MINT, stroke=AMBER if warn else TEAL, size=10, r=3, bold=False)
f.text(8, 322, "amber rows are the ones that surprise beginners", size=10, color=AMBER, anchor="start")
```

```svgfig label="6.3" caption="Eight real requests to one PHP endpoint and what came back (measured with curl). Good APIs answer with the right status code, not always 200. 200 means success with a body; 201 Created follows a successful POST and adds a Location header with the new address; 204 means success with no body; 400 means the client sent bad input (a POST without marks); 404 means the resource does not exist; 405 means the method is not allowed on that URL (PUT here). The JavaScript then tests response.ok or response.status instead of guessing from the body."
f = Fig(580, 312)
f.box(8, 8, 214, 26, "Request", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
f.box(226, 8, 74, 26, "Status", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
f.box(304, 8, 268, 26, "Body returned", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
rows = [("GET  /api.php?q=pa", "200", "{\"query\":\"pa\",\"matches\":[\"Patan\"]}"),
        ("GET  /students/14", "200", "{\"id\":14,\"name\":\"Sita\",\"marks\":88}"),
        ("GET  /students/99", "404", "{\"error\":\"student 99 not found\"}"),
        ("POST /students  (Hari, 71)", "201", "{\"id\":16,\"name\":\"Hari\",\"marks\":71}"),
        ("POST /students  (no marks)", "400", "{\"error\":\"name and integer marks required\"}"),
        ("DELETE /students/15", "204", "(empty body, 0 bytes)"),
        ("PUT  /students/14", "405", "{\"error\":\"method not allowed\"}"),
        ("GET  /teachers", "404", "{\"error\":\"no such resource\"}")]
for i, (a, s, b) in enumerate(rows):
    y = 38 + i * 30
    ok = s.startswith("2")
    f.box(8, y, 214, 26, a, fill=SOFT, stroke=SLATE, size=10, r=3, anchor="start")
    f.box(226, y, 74, 26, s, fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, size=12, r=3, bold=True)
    f.box(304, y, 268, 26, b, fill=SOFT, stroke=SLATE, size=9.5, r=3, anchor="start")
f.text(8, 302, "201 adds the header  Location: /api.php/students/16;  405 adds  Allow: GET, POST, DELETE", size=10, color=NAVY, anchor="start")
```

```svgfig label="6.4" caption="Asynchronous means the page does not wait. This is the real console order of a Node 22 run of the code beside it. The first message prints, then fetch() hands the request to the browser and returns a Promise at once, so the second message prints before any answer exists. About a moment later the response arrives and the then() callbacks run, printing the third message. Two more facts from the same run: a 404 does NOT make fetch fail (the promise resolves, response.ok is false and the status is 404), while a network failure rejects the promise with a TypeError, so both cases must be handled."
f = Fig(580, 262)
f.box(8, 8, 270, 28, "JavaScript (one thread, never blocked)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(330, 8, 242, 28, "Browser network + PHP server", fill=SAND, stroke=AMBER, size=11, bold=True)
f.line(143, 36, 143, 244, color="#cbd5e1", sw=1.2, dash=True)
f.line(451, 36, 451, 244, color="#cbd5e1", sw=1.2, dash=True)
f.box(18, 50, 250, 30, "1  print: before fetch", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(18, 98, 250, 30, "fetch(url) returns a Promise", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(18, 146, 250, 30, "2  print: after fetch call", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(18, 206, 250, 30, "3  then(): print response data", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(330, 98, 242, 30, "request sent, PHP runs api.php", fill=SAND, stroke=AMBER, size=10.5)
f.box(330, 146, 242, 30, "waiting for the reply ...", fill=SAND, stroke=AMBER, size=10.5)
f.box(330, 206, 242, 30, "reply: 34 bytes of JSON", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(268, 113), (330, 113)], color=SLATE)
f.arrow([(330, 221), (268, 221)], color=AMBER)
f.text(299, 252, "the page stays usable while the reply is on its way", size=10, color=SLATE)
```

```svgfig label="6.5" caption="Cross-origin calls and the preflight, with the real headers of the test endpoint. A page at localhost:3000 calling an API on another port is a different origin, so the browser insists the server agree. For a simple GET the reply must carry Access-Control-Allow-Origin naming the page (it did). For a POST with a JSON body the browser first sends an OPTIONS request, the preflight, asking permission for the method and header; the server answered 204 No Content with the allowed origin, methods and headers, and only then does the browser send the real POST (201 in the run). The rule is enforced by the browser: curl ignores it."
f = Fig(580, 262)
f.box(8, 8, 150, 40, "Page at\nlocalhost:3000", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(422, 8, 150, 40, "API at\n127.0.0.1:8090", fill=SAND, stroke=AMBER, size=11, bold=True)
f.line(83, 48, 83, 250, color="#cbd5e1", sw=1.2, dash=True)
f.line(497, 48, 497, 250, color="#cbd5e1", sw=1.2, dash=True)
f.arrow([(84, 74), (496, 74)], color=NAVY)
f.text(290, 66, "1  OPTIONS  (preflight): Origin, Request-Method POST", size=10.5, color=NAVY, bold=True)
f.arrow([(496, 120), (84, 120)], color=TEAL)
f.text(290, 90, "2  204 No Content", size=10.5, color=TEAL, bold=True)
f.text(290, 104, "Allow-Origin: localhost:3000  Allow-Methods: GET, POST, DELETE", size=9.5, color=TEAL)
f.text(290, 134, "Allow-Headers: Content-Type", size=9.5, color=TEAL)
f.arrow([(84, 170), (496, 170)], color=NAVY)
f.text(290, 162, "3  POST /students  with JSON body", size=10.5, color=NAVY, bold=True)
f.arrow([(496, 214), (84, 214)], color=TEAL)
f.text(290, 188, "4  201 Created", size=10.5, color=TEAL, bold=True)
f.text(290, 202, "Allow-Origin: localhost:3000   Vary: Origin", size=9.5, color=TEAL)
f.text(290, 238, "without these headers the browser hides the reply from the page", size=10, color=RED, bold=True)
```

### 6.5.1 Eight applications of AJAX and web APIs

1. **Live search suggestions.** As a user types the first letters, the page sends a short request and the server returns a few matching names (Fig. 6.1). A college site can suggest courses or students without reloading the page. Only a few dozen bytes travel each time, so the box feels instant.
2. **Online payments and wallet balances.** Payment pages such as ConnectIPS, Fonepay and eSewa-style checkouts call APIs in the background to check an account or confirm a payment. The page shows "processing" and then the result without leaving the screen. The JSON reply carries a status that the script reads before telling the user.
3. **Form validation on the server.** A registration page can ask the server whether a username or email is already taken as soon as the field loses focus. The endpoint answers 200 or 400 (Fig. 6.3) and the page shows a message at once. The user fixes the problem before pressing the submit button.
4. **Dashboards that refresh themselves.** A page showing NEPSE prices, weather from the Department of Hydrology and Meteorology or load-shedding information can call an API every few seconds. Only the numbers are replaced, so the user keeps their place on the page. This is the same fetch pattern in a timer.
5. **Mobile apps and web pages sharing one backend.** The same JSON API can serve a website, an Android app and a kiosk. Apps such as the Nagarik App and bank apps rely on this: the server holds the rules and every client only shows the data. A change in the server benefits all clients at once.
6. **Maps, weather and other third-party data.** A page can show a map, an exchange rate or the Nepal Rastra Bank rate list by calling someone else's API and drawing the result. The same-origin rule means the provider must allow your site with CORS headers (Fig. 6.5). Many providers also ask for a key, which must stay on the server.
7. **Infinite scroll, comments and likes.** When the user reaches the bottom of a news page, the script asks for the next page of items and appends them. A "like" button sends one small POST and updates one counter. Neither action reloads the page, so reading is not interrupted.
8. **Saving work in the background.** Online exam and form systems, such as university result or admission portals, can save answers every minute with a small POST request. If the connection drops, the rejected promise (Fig. 6.4) lets the script warn the student and retry. This protects a long form from being lost.

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

## Model answers (5 and 10 marks)

**Q1. What is AJAX? Explain how it works, the technologies it uses, and its advantages and limitations with an example. (10 marks)**

**Introduction.** AJAX (Asynchronous JavaScript and XML) is a technique in which a web page sends a request to the server in the background and updates only a part of the page with the reply, without a full reload. The name was given by Jesse James Garrett in 2005 (Plate 6.1). Today the data is usually JSON and not XML, but the name stayed. A live search box and a "like" counter are everyday examples.

**How it works.** Fig. 6.1 and Fig. 6.4 show the cycle. It has four steps.

1. **Event.** Something happens on the page: a key is typed, a button is clicked or a timer fires.
2. **Request.** JavaScript creates a request with `fetch()` or `XMLHttpRequest` and sends it to a PHP endpoint. The call returns at once, so the page stays usable (the word *asynchronous*).
3. **Response.** PHP runs, reads the database if needed, and sends back a small JSON text with the correct status code.
4. **Update.** A callback (or code after `await`) parses the JSON and changes the DOM, for example the items of a list.

**Technologies used.** HTML and CSS for the page, JavaScript and the DOM to react and to update, `fetch`/`XMLHttpRequest` to send requests, JSON (or XML) as the data format, and a server-side language such as PHP with MySQL to answer.

**Example.** The program below was run against the test endpoint with Node 22 (the same code works in a browser; the output is a real run).

```js
async function suggest(prefix) {
  const res = await fetch("http://127.0.0.1:8090/api.php?q=" + encodeURIComponent(prefix));
  if (!res.ok) throw new Error("HTTP " + res.status);
  const data = await res.json();
  return data.matches;                      // a page would write these into the list
}
console.log(await suggest("pa"), await suggest("b"));
```
```output
[ 'Patan' ] [ 'Bhaktapur', 'Biratnagar' ]
```

**Advantages and limitations.**

| Advantages | Limitations |
|---|---|
| Only the changed part is sent: 34 bytes against 484 bytes in Fig. 6.1 | Needs JavaScript; a user who blocks scripts sees nothing |
| The page does not flicker and keeps the scroll position | The back button and bookmarks do not follow the changes unless the code manages the address |
| Feels fast, so users stay longer | Search engines may not see content that is loaded later |
| One JSON API can serve a website and a mobile app | Errors are silent unless every call checks `response.ok` and failures |
| Less load on the server for each action | Same-origin rules (CORS) must be handled for other servers |

**Conclusion.** AJAX replaces whole-page reloads with small background calls. It is the base of modern sites such as payment pages, dashboards and live search, as long as each call checks status codes, escapes the data it writes into the page and handles failure.

**Q2. Differentiate between JSON and XML. Show how PHP converts an array to JSON and back. (5 marks)**

**JSON** (JavaScript Object Notation) is a light text format built from objects `{ }`, arrays `[ ]`, strings, numbers, `true`, `false` and `null`. **XML** (Extensible Markup Language) describes data with opening and closing tags and attributes. JSON is shorter and maps straight to the data structures of JavaScript and PHP, so most modern APIs use it. XML is more verbose but supports attributes, namespaces, comments and schemas, so it is still used in older services, office documents and SOAP.

| Point | JSON | XML |
|---|---|---|
| Syntax | Key/value pairs and arrays | Tags and attributes |
| Size | Small | Larger because every value has two tags |
| Reading in JavaScript | `JSON.parse` in one call | Needs an XML parser and DOM walking |
| Data types | Numbers, booleans, null are built in | Everything is text unless a schema says more |
| Comments | Not allowed | Allowed |

In PHP, `json_encode` turns an array into JSON text and `json_decode($text, true)` turns it back into an associative array. The second argument `true` asks for arrays instead of objects. The program shows both directions (real output):

```php
<?php
$s = ["name" => "Sita", "marks" => [88, 92.5], "passed" => true];
$text = json_encode($s);
echo $text, "\n";
$back = json_decode($text, true);
echo $back["name"], " ", $back["marks"][1], " ", strlen($text), " bytes\n";
```
```output
{"name":"Sita","marks":[88,92.5],"passed":true}
Sita 92.5 47 bytes
```
The same record in XML needs the tags `<student><name>Sita</name>...</student>` and is clearly longer, which is why JSON is preferred when the reply is read by a script.

**Q3. What is a REST API? Explain its rules, the HTTP methods and status codes, and write a PHP endpoint with a JavaScript client. (10 marks)**

**Introduction.** REST (Representational State Transfer) is a style for designing web APIs, defined by Roy Fielding in his 2000 dissertation (Plate 6.1). A **resource** (a student, a book, a payment) has an address (URL), and the HTTP method says what to do with it. The reply is usually JSON with a status code. The waiter in Plate 6.1 is the picture to remember: the client sends a short order and receives a finished item, and never enters the kitchen.

**Main rules (principles).**

1. **Resources have URLs.** `/students` is the collection and `/students/14` is one student; names are nouns, not verbs.
2. **Methods give the action.** `GET` reads, `POST` creates, `PUT` or `PATCH` updates, `DELETE` removes.
3. **Stateless.** Each request carries everything the server needs (an id, a token); the server keeps no hidden conversation between calls.
4. **Uniform replies.** JSON with the header `Content-Type: application/json` and a meaningful status code (Fig. 6.3).
5. **Cacheable and layered.** `GET` replies may be cached, and proxies or gateways may sit between client and server.

**Methods and codes (measured in Fig. 6.3).**

| Action | Request | Success | Typical failure |
|---|---|---|---|
| Read one | `GET /students/14` | 200 with JSON | 404 not found |
| Create | `POST /students` | 201 and `Location` | 400 bad input |
| Delete | `DELETE /students/15` | 204 no body | 404 not found |
| Wrong method | `PUT /students/14` | not offered | 405 and `Allow` header |

**Endpoint (server side).** This is the core of the tested endpoint.

```php
// noexec
<?php
header("Content-Type: application/json; charset=utf-8");
$students = [14 => ["id" => 14, "name" => "Sita", "marks" => 88]];   // a table in real life
$m  = $_SERVER["REQUEST_METHOD"];
$id = (int)(explode("/", trim($_SERVER["PATH_INFO"] ?? "", "/"))[1] ?? 0);
if ($m === "GET" && $id) {
    if (isset($students[$id])) { echo json_encode($students[$id]); }
    else { http_response_code(404); echo json_encode(["error" => "student $id not found"]); }
} elseif ($m === "POST") {
    $in = json_decode(file_get_contents("php://input"), true);
    if (!is_array($in) || !isset($in["name"]) || !is_int($in["marks"] ?? null)) {
        http_response_code(400); echo json_encode(["error" => "name and integer marks required"]); exit;
    }
    http_response_code(201); header("Location: /api.php/students/16");
    echo json_encode(["id" => 16, "name" => $in["name"], "marks" => $in["marks"]]);
} else { http_response_code(405); header("Allow: GET, POST, DELETE"); }
```
**Client side (real run).**

```js
const base = "http://127.0.0.1:8090/api.php";
const r = await fetch(base + "/students", { method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: "Hari", marks: 71 }) });
console.log(r.status, r.headers.get("location"), await r.json());
```
```output
201 /api.php/students/16 { id: 16, name: 'Hari', marks: 71 }
```

**Why it is popular.** The rules are simple enough that a student can read an unknown API from its URLs alone, and the same endpoint works for a browser, an Android app and a test script. In Nepal, services such as ConnectIPS, Fonepay and the Nagarik App expose or consume APIs of exactly this kind, so the skill is directly useful.

**Conclusion.** A REST API names resources with URLs, uses the HTTP methods for actions and tells the client what happened with status codes. It keeps the server stateless and lets one backend serve a website and an app. Such an API must validate every input, escape output and use prepared statements when it talks to MySQL.

**Q4. Explain the same-origin policy and CORS. Why does a preflight request occur? (5 marks)**

The **same-origin policy** is a browser rule: a script loaded from one *origin* (scheme + host + port) may not read replies from another origin. `http://localhost:3000` and `http://127.0.0.1:8090` are different origins, even on one computer. The rule protects the user: otherwise a hostile page could use your logged-in session to read your bank or university data.

**CORS** (Cross-Origin Resource Sharing) is the controlled exception. The other server opts in by sending headers such as `Access-Control-Allow-Origin: http://localhost:3000`. The browser reads the header and either gives the reply to the script or hides it (Fig. 6.5).

A **preflight** is an extra `OPTIONS` request that the browser sends first when the real request is not "simple": for example a `POST` with `Content-Type: application/json`, a `PUT` or `DELETE`, or a custom header. It asks, "may this origin use this method and these headers?" The test endpoint answered `204 No Content` with `Access-Control-Allow-Methods: GET, POST, DELETE` and `Access-Control-Allow-Headers: Content-Type`, and then the browser sent the real `POST`, which returned 201.

Points to remember: CORS is enforced by the browser only, so `curl` and servers are not blocked; allow named origins, not `*`, for APIs that use cookies or tokens; and CORS does not replace authentication, because it protects the user's browser and not the server.

**Q5. Explain the states of `XMLHttpRequest` and compare it with `fetch()`. (5 marks)**

`XMLHttpRequest` (XHR) is the older browser object for AJAX. It reports its progress in the property `readyState` and calls `onreadystatechange` each time it changes.

| readyState | Name | Meaning |
|---|---|---|
| 0 | UNSENT | the object is created, `open()` not yet called |
| 1 | OPENED | `open()` was called; headers can be set |
| 2 | HEADERS_RECEIVED | `send()` was called; status and headers have arrived |
| 3 | LOADING | the body is arriving (`responseText` holds part of it) |
| 4 | DONE | the whole reply has arrived, or the request failed |

The usual test is `xhr.readyState === 4 && xhr.status === 200`, followed by `JSON.parse(xhr.responseText)`.

`fetch()` is the modern replacement. It returns a **Promise**, so the code can use `.then()` or `await` and avoids nested callbacks. It has a cleaner syntax for headers, methods and bodies (`method`, `headers`, `body`), and `response.json()` parses the body in one step. Two points matter in exams. A reply with status 404 or 500 still *resolves* the promise: the program must test `response.ok` or `response.status` (Fig. 6.4). Only a network failure *rejects* the promise, with a `TypeError`, so a `try/catch` or `.catch()` is also needed. XHR can report upload progress more easily, but for new code `fetch()` is preferred.

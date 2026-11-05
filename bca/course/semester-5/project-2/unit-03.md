---
subject: Project II
grade: BCA Semester 5
unit: 3
title: Security: Login, Passwords, Tokens and Attacks
area: BCA 306 · Project II · Unit 3
---

The moment ClinicQ is on a network, a stranger can send it any request. This unit adds the defences a student project must have: salted password hashes, signed login tokens, parameterised SQL, role checks and rate limits. Each defence is shown with a short program and its real output, and each attack is shown failing against the defence.

::: key What this unit gives you
- The login flow from password to signed token to protected request, with a figure.
- Salted PBKDF2 password hashing and why plain text or a bare hash is not acceptable.
- An HMAC-signed token with expiry, and proof that tampering is detected.
- SQL injection shown working on bad code and failing on good code, plus brute-force arithmetic.
:::

## 3.1 Who are you, and what may you do?

Security begins with two questions. **Authentication** asks "who are you?" and is proved by something only the user knows (a password). **Authorisation** asks "what may you do?" and is decided by the user's role. In ClinicQ there are three roles: *public* (read the queue), *clerk* (issue tokens) and *nurse* (mark tokens served). A failed authentication gets **401**; a failed authorisation gets **403**.

```svgfig label="3.1" caption="ClinicQ login flow. The password is sent once over HTTPS and checked against a salted hash. The server returns a signed token; every later request carries the token, so the password is not sent again."
f = Fig(560, 200)
f.box(20, 20, 110, 40, "Client (browser)", fill=BLUE, stroke=NAVY, size=11, color=NAVY)
f.box(430, 20, 110, 40, "ClinicQ server", fill=SOFT, stroke=TEAL, size=11, color=NAVY)
f.line(75, 60, 75, 185, color=SLATE, dash=True)
f.line(485, 60, 485, 185, color=SLATE, dash=True)
f.arrow([(75, 85), (485, 85)], color=NAVY)
f.text(280, 78, "1  POST /api/login  {user, password}", size=10.5, color=NAVY)
f.text(485, 100, "2 verify salted hash", size=10, color=RED, anchor="end")
f.arrow([(485, 120), (75, 120)], color=TEAL)
f.text(280, 113, "3  200  {token: user.role.expiry.signature}", size=10.5, color=NAVY)
f.arrow([(75, 150), (485, 150)], color=NAVY)
f.text(280, 143, "4  PATCH /api/tokens/1   Authorization: Bearer token", size=10.5, color=NAVY)
f.text(485, 172, "5 verify signature and expiry", size=10, color=RED, anchor="end")
```

## 3.2 Passwords: never store them, store a salted slow hash

A **hash** is a one-way function: easy to compute, practically impossible to reverse. If the database file leaks, plain-text passwords are lost at once, and a bare fast hash such as MD5 can be reversed with pre-computed tables of common passwords. Two defences fix this. A **salt** is a random value stored beside the hash; it makes the same password produce different hashes, so pre-computed tables are useless. A **slow** function (PBKDF2, bcrypt, scrypt, Argon2) repeats the work many times, so each guess costs the attacker real time.

```python
import hashlib, hmac
def make(password, salt, rounds=200_000):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, rounds).hex()
def check(password, salt, stored, rounds=200_000):
    return hmac.compare_digest(make(password, salt, rounds), stored)

salt_a, salt_b = bytes.fromhex("a1" * 16), bytes.fromhex("b2" * 16)   # in real code: os.urandom(16)
h1, h2 = make("Namaste@2083", salt_a), make("Namaste@2083", salt_b)
print("same password, salt A:", h1[:24], "...")
print("same password, salt B:", h2[:24], "...")
print("hashes equal?", h1 == h2, "| length in hex digits:", len(h1))
print("right password:", check("Namaste@2083", salt_a, h1))
print("wrong password:", check("namaste@2083", salt_a, h1))
```
```output
same password, salt A: 305242b1dce2e952413778ca ...
same password, salt B: 748f73bab0bd7b56c2ec4bbb ...
hashes equal? False | length in hex digits: 64
right password: True
wrong password: False
```
The same password gives two different hashes because the salts differ, and one changed letter fails the check. `compare_digest` compares in constant time so that response time does not leak how many leading characters were right. In production use `os.urandom(16)` for the salt, store `rounds`, `salt` and `hash` in the user row, and raise `rounds` as computers become faster (a common 2023 guideline is at least 600,000 for PBKDF2-HMAC-SHA256).

## 3.3 Signed tokens: logging in without sending the password again

After the password check the server issues a **token** that proves the login. A simple design is `user.role.expiry.signature`, where the signature is an **HMAC** (hash-based message authentication code) of the first three parts under a secret key that only the server knows. A client cannot change `role=nurse` or the expiry without invalidating the signature.

```python
import hmac, hashlib
SECRET = b"change-me-and-keep-in-an-environment-variable"
def issue(user, role, expires):
    body = f"{user}.{role}.{expires}"
    return body + "." + hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()[:20]
def verify(token, now):
    try: user, role, expires, sig = token.split(".")
    except ValueError: return "401 malformed"
    good = hmac.new(SECRET, f"{user}.{role}.{expires}".encode(), hashlib.sha256).hexdigest()[:20]
    if not hmac.compare_digest(sig, good): return "401 bad signature"
    if int(expires) < now: return "401 expired"
    return f"200 ok as {role}"
t = issue("sunita", "clerk", 1000)
print(t)
print(verify(t, now=500))
print(verify(t, now=1500))
print(verify(t.replace(".clerk.", ".nurse."), now=500))
print(verify("garbage", now=500))
```
```output
sunita.clerk.1000.0d4e4654644f8914f4bd
200 ok as clerk
401 expired
401 bad signature
401 malformed
```
The valid token is accepted, the same token after its expiry is refused, the edited role is refused and garbage is refused. Real projects usually use the standard **JWT** format with a library, but the idea is exactly this. Four rules: keep the secret out of the source code (environment variable), make tokens short-lived, send them only over HTTPS, and check the role on **every** protected endpoint on the server.

## 3.4 SQL injection: the attack and the cure

**SQL injection** happens when user input is pasted into SQL text. The attacker types SQL instead of a name, and the database obeys. The program below uses a login lookup written both ways.

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("CREATE TABLE staff(name TEXT, role TEXT, pw TEXT);"
                 "INSERT INTO staff VALUES ('sunita','clerk','x1'),('prakash','nurse','x2');")
evil = "nobody' OR '1'='1"
bad_sql = f"SELECT name, role FROM staff WHERE name = '{evil}'"
print("BAD  sql :", bad_sql)
print("BAD  rows:", db.execute(bad_sql).fetchall())
print("GOOD rows:", db.execute("SELECT name, role FROM staff WHERE name = ?", (evil,)).fetchall())
```
```output
BAD  sql : SELECT name, role FROM staff WHERE name = 'nobody' OR '1'='1'
BAD  rows: [('sunita', 'clerk'), ('prakash', 'nurse')]
GOOD rows: []
```
The bad query becomes `WHERE name = 'nobody' OR '1'='1'`, which is true for every row, so the attacker sees all staff. With a `?` placeholder the whole string is compared as one name, nobody matches and nothing leaks. Never build SQL with f-strings, `+` or `%` on user input; always pass values separately.

## 3.5 Brute force and rate limiting

A **brute-force** attack tries many passwords. The defence is to make each guess slow (Section 3.2), make the password space big, and limit attempts (reply **429 Too Many Requests**). The numbers below show why length matters.

```python
rate = 1_000_000_000   # offline guesses per second against a fast, unsalted hash
for label, alphabet, length in [("6 digits (PIN)", 10, 6), ("8 lowercase letters", 26, 8),
                                ("8 mixed letters+digits+symbols", 94, 8), ("12 mixed", 94, 12)]:
    space = alphabet ** length
    secs = space / rate
    unit, div = ("seconds", 1) if secs < 3600 else ("hours", 3600) if secs < 86400 * 365 else ("years", 86400 * 365)
    print(f"{label:32} {space:>26,d} guesses  worst case {secs / div:,.1f} {unit}")
online = 5 * 24 * 60 / 10
print("Online with 5 tries per 10 min per account: tries per day =", online)
print("6-digit PIN worst case online: %.0f days = %.1f years" % (10**6 / online, 10**6 / online / 365))
```
```output
6 digits (PIN)                                    1,000,000 guesses  worst case 0.0 seconds
8 lowercase letters                         208,827,064,576 guesses  worst case 208.8 seconds
8 mixed letters+digits+symbols        6,095,689,385,410,816 guesses  worst case 1,693.2 hours
12 mixed                         475,920,314,814,253,376,475,136 guesses  worst case 15,091,334.2 years
Online with 5 tries per 10 min per account: tries per day = 720.0
6-digit PIN worst case online: 1389 days = 3.8 years
```
A 6-digit PIN falls in a fraction of a second offline, but online with a 5-tries-per-10-minutes limit it needs about 1,389 days (3.8 years) in the worst case. This is why the limit must be on the **server** and why password length beats complexity rules.

```photogrid label="3.1" cols="2" ratio="1.4" caption="Security is layers, not one lock. (a) A padlock: one barrier that anyone with the right key defeats. (b) Defence in depth for ClinicQ: each layer stops what the layer before it missed, so an attacker must defeat all of them."
@ photo id="bca306/padlock" cap="A single lock"
fit 1.4
focus 0.5 0.55
call 0.5 0.92 0.5 0.75 "One barrier only"
@ svg cap="Layers around the data"
f = Fig(330, 235)
f.box(8, 8, 314, 219, "", fill=BLUE, stroke=NAVY)
f.text(165, 24, "HTTPS and firewall", size=11, color=NAVY, bold=True)
f.box(34, 36, 262, 177, "", fill=SOFT, stroke=TEAL)
f.text(165, 52, "Login, roles, rate limit", size=11, color=NAVY, bold=True)
f.box(62, 64, 206, 130, "", fill=BLUE, stroke=AMBER)
f.text(165, 80, "Validation + placeholders", size=11, color=NAVY, bold=True)
f.box(95, 92, 140, 80, "Data: salted hashes, backups", fill=SOFT, stroke=RED, size=11, color=NAVY)
```

## 3.6 The common attacks and their defences

| Attack | What the attacker does | ClinicQ defence |
|---|---|---|
| SQL injection | types SQL into a form field | `?` placeholders |
| Broken authentication | guesses or steals passwords | salted slow hash, rate limit, 429 |
| Broken access control | calls a staff URL as a patient | check the role on every endpoint, 403 |
| Cross-site scripting (XSS) | stores `<script>` in a name | escape output, `Content-Security-Policy` header |
| Cross-site request forgery (CSRF) | tricks a logged-in browser into sending a request | `SameSite` cookies or a token in the header |
| Sensitive data exposure | reads traffic on public Wi-Fi | HTTPS only, hide stack traces |
| Misconfiguration | default password, debug mode on | settings from environment, no default accounts |
| Insufficient logging | nobody notices the attack | log logins and changes, alert on repeats |

The list follows the idea of the OWASP Top 10, a widely used awareness list of web risks; check the current edition on owasp.org for the exact order. Under Nepal's Electronic Transactions Act 2063, unauthorised access to a computer system and damage to data are offences; a project that holds patient data should treat privacy as a legal duty as well as a technical one.

## 3.7 Eight security practices every student web project needs

1. **Use HTTPS everywhere.** HTTPS encrypts the connection, so a stranger on café Wi-Fi cannot read passwords or tokens. Free certificates from Let's Encrypt make it cost nothing. Redirect every HTTP request to HTTPS and tell browsers to remember it with the `Strict-Transport-Security` header.
2. **Hash passwords with a salt and a slow function.** Plain text, MD5 and a bare SHA-256 are all unacceptable. Use PBKDF2, bcrypt or Argon2 from a standard library. If your database leaks, the attacker still needs years per password.
3. **Check every input on the server.** Browser checks are only for convenience. Validate type, length and range, and reject at once. A blank name or a phone number of 98x must receive a clear 400 reply.
4. **Use parameterised SQL only.** Placeholders turn input into data. This one habit removes the most famous web attack. An ORM does it for you, but raw SQL in your own code must still use `?`.
5. **Give every user the least power needed.** The public may read the queue; a clerk may issue tokens; only a nurse may mark served. Check the role in the server for every endpoint, because hiding a button in the browser protects nothing.
6. **Keep secrets out of the code.** Passwords, signing keys and database URLs go in environment variables or a file outside Git. A secret pushed to a public repository must be treated as stolen and replaced at once.
7. **Limit and log.** Rate-limit logins, and write a log line for each login, failure and status change with time and user name. Never log passwords or tokens. Logs are what let you answer "what happened?" after an incident.
8. **Update and back up.** Old libraries have known holes, so update them before the demo. Take a daily database backup and test a restore once. A backup you have never restored is only a hope.

## Formula and fact sheet

- Authentication = who you are (401). Authorisation = what you may do (403).
- Stored password = PBKDF2(password, random salt, many rounds); compare with `compare_digest`.
- Token = body + HMAC(secret, body); check signature, then expiry, then role.
- Search space = alphabet length ^ password length; online guesses per day = tries per window × windows per day.
- Placeholders keep values out of SQL text; never concatenate user input.

## Chapter summary

- Authentication and authorisation are different questions with different status codes.
- Passwords are stored as salted slow hashes; the run showed different hashes for one password and a failed check for one changed letter.
- Signed tokens carry user, role and expiry; the run refused edited, expired and malformed tokens.
- Parameterised SQL beats injection; rate limits and long passwords beat brute force.
- Security is layered: HTTPS, login and roles, validation, protected data and logs.

## Practice

1. Differentiate authentication and authorisation with a ClinicQ example.
2. Why is storing `MD5(password)` without a salt unsafe?
3. What does the salt do, and where is it stored?
4. Why does `compare_digest` exist?
5. Why does the token contain an expiry time?
6. What would happen if the signing key were hard-coded and pushed to a public repository?
7. Show the SQL that results from the name `x' OR '1'='1` in a concatenated query.
8. A system allows 3 tries per 5 minutes. How many tries per day is that for one account?
9. Name four defences listed in Section 3.6 and the attack each stops.
10. Which status code should a patient receive for `PATCH /api/tokens/1` and why?

::: note Answers and worked solutions
**1.** Authentication: a nurse logs in with a password. Authorisation: the logged-in nurse may mark a token served, a patient may not.
**2.** Equal passwords give equal hashes and fast hashing lets attackers try billions of guesses or use pre-computed tables.
**3.** It makes each hash unique and defeats tables; it is stored in clear beside the hash.
**4.** It compares in constant time so timing does not reveal how much of the value matched.
**5.** A stolen token stops working after a short time.
**6.** Anyone could sign tokens for any role; the key must be replaced and all tokens invalidated.
**7.** `... WHERE name = 'x' OR '1'='1'`, which is true for every row.
**8.** 3 × 12 × 24 = 864 tries per day.
**9.** Placeholders stop SQL injection; rate limit stops brute force; role checks stop broken access control; HTTPS stops sniffing.
**10.** 403 if logged in as a patient (known but not allowed); 401 if not logged in.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain how passwords should be stored in a web application.**

*Introduction.* A database can be leaked through a bug, a stolen backup or a careless employee, so the design must assume that an attacker may read every row. Passwords must therefore never be readable from the stored data.

*Method.*

1. **Never plain text.** Plain text exposes every user at once, and people reuse passwords on other sites.
2. **Use a salt.** A random 16-byte value is generated per user and stored beside the hash. In the run, one password gave two different hashes under two salts, so pre-computed tables fail.
3. **Use a slow function.** PBKDF2, bcrypt, scrypt or Argon2 repeat the work (for example 200,000 rounds), so each guess costs time.
4. **Compare safely.** Use a constant-time comparison such as `hmac.compare_digest`.
5. **Store parameters.** Keep algorithm, rounds, salt and hash in the row so the cost can be raised later.

*Example.* ClinicQ stores `pbkdf2$200000$salt$hash`. Login recomputes the hash with the stored salt and compares; a wrong password fails.

*Conclusion.* Salted slow hashing means that a leaked database does not leak the passwords.

**Q2 (5 marks). What is SQL injection? Show an example and explain how to prevent it.**

*Introduction.* SQL injection is an attack in which the attacker enters SQL code in an input field and the application runs it as part of its own query.

*Example.* A login query is built as `"... WHERE name = '" + name + "'"`. The attacker enters `nobody' OR '1'='1`. The query becomes `WHERE name = 'nobody' OR '1'='1'`, which is true for every row. In the run the bad query returned both staff rows; the same input with a placeholder returned none.

*Effects.* Reading private data, bypassing login, changing or deleting rows, and in some databases running operating-system commands.

*Prevention.*

1. Use parameterised queries (`?` placeholders) or an ORM.
2. Validate input type, length and range on the server.
3. Give the database account only the permissions it needs, so a hole cannot drop tables.
4. Show generic error messages and log details privately.

*Conclusion.* Keeping data separate from SQL text removes the attack completely, which is why placeholders are mandatory in every project.

**Q3 (10 marks). Describe the security measures required for a web-based system that stores patient data, such as ClinicQ. Use the login flow, a table of attacks and the principle of defence in depth.**

*Introduction.* A clinic system holds names and phone numbers of patients, and a leak harms real people. Because attackers need only one weakness, the system must have several layers of defence, each covering the failures of the others (Figure 3.1).

*1. Transport security.* HTTPS encrypts all traffic between browser and server so that passwords and tokens cannot be read on shared Wi-Fi. The reverse proxy redirects HTTP to HTTPS and adds the Strict-Transport-Security header.

*2. Authentication.* A staff member sends the password once; the server compares a salted PBKDF2 hash (many rounds) using a constant-time comparison. Wrong passwords receive 401 and repeated failures receive 429 after five attempts in ten minutes.

*3. Session token.* The server returns `user.role.expiry.signature`, an HMAC under a secret kept in an environment variable. Editing the role or expiry breaks the signature, as the run showed. Tokens are short-lived.

*4. Authorisation.* Every endpoint checks the role: public may read the queue, clerks issue tokens, nurses mark served. Violations get 403. Checks happen on the server, never only in the browser.

*5. Input handling.* All input is validated for type and length; SQL uses placeholders; output is escaped before it is placed in HTML, which stops injection and cross-site scripting.

*6. Data protection and privacy.* The public queue page shows initials only. The database is backed up daily and the restore is tested. Access to the database file is limited to the service account.

*7. Monitoring.* Logins, failures and status changes are logged with time and user, without passwords. Repeated failures raise an alert.

| Attack | Defence |
|---|---|
| SQL injection | placeholders |
| Password guessing | slow hash, rate limit, 429 |
| Forged token | HMAC signature, expiry |
| Access by wrong role | role check, 403 |
| Eavesdropping | HTTPS |
| XSS | output escaping, CSP |

*Conclusion.* No single measure is enough, but together they raise the cost of an attack beyond what a casual attacker will pay. Under the Electronic Transactions Act 2063 unauthorised access is an offence, and a project that stores health data should show these layers, tested, in its report.

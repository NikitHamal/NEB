---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 3
title: Authentication, Entropy, Key Derivation and Access Control Models
hours: 7
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 3
---

Every access decision in a system rests on two questions: *who are you?* (authentication) and *what are you allowed to do?* (authorisation). Weak answers to the first question undermine everything built on the second, which is why stolen or guessed credentials are behind a large share of breaches. This unit puts numbers on password strength, explains how defenders store credentials so that a stolen database is worth as little as possible, and compares the four classic access control models.

::: key What this unit gives you
- The authentication factors, multi-factor authentication and phishing-resistant methods.
- Password entropy: H = L × log₂(R), and what it does and does not tell you.
- Key-derivation work factors: PBKDF2, bcrypt, scrypt and Argon2 cost arithmetic, and a salted verification routine.
- Access control: DAC, MAC (Bell–LaPadula), RBAC with separation of duties, and ABAC.
:::

## 3.1 Authentication factors

Factors are *something you know* (password, PIN), *something you have* (phone, hardware key, smart card) and *something you are* (fingerprint, face). **Multi-factor authentication (MFA)** combines factors from at least two categories, so a stolen password alone is useless. Not all second factors are equal:

- **SMS codes** are better than nothing but can be diverted by SIM-swap fraud.
- **Time-based one-time passwords (TOTP, RFC 6238)** compute a short code from a shared secret and the current 30-second window using HMAC; they work offline but can be relayed by a fake login page in real time.
- **FIDO2/WebAuthn security keys and passkeys** use public-key cryptography bound to the website's origin, so a lookalike site cannot obtain a valid response. These are called *phishing-resistant*.

NIST SP 800-63B (digital identity guidelines) recommends allowing long passphrases, screening new passwords against lists of breached passwords, avoiding forced periodic changes and composition rules, and rate-limiting failed attempts.

## 3.2 Entropy of a secret

If a secret is chosen uniformly at random from a set of *R* symbols and has length *L*, the number of possibilities is R^L and the **entropy** is

::: key Password entropy
**H = L × log₂(R) bits.** Each added bit doubles the search space. Expected work to find the secret by exhaustive guessing is about 2^(H−1) trials.
:::

The formula is valid only for *randomly generated* secrets. Human-chosen passwords are far weaker than the formula suggests because people pick words, dates and patterns; the formula gives an upper bound for the policy, not a measurement of a person's password.

```python
import math
cases = [("8 chars, 95 printable", 95, 8), ("12 chars, lowercase", 26, 12),
         ("6 Diceware words", 7776, 6), ("16 chars, alphanumeric", 62, 16)]
for name, R, L in cases:
    print(f"{name}: {L * math.log2(R):.1f} bits")
```
```output
8 chars, 95 printable: 52.6 bits
12 chars, lowercase: 56.4 bits
6 Diceware words: 77.5 bits
16 chars, alphanumeric: 95.3 bits
```
A random 8-character password from the 95 printable ASCII characters carries 52.6 bits. A random 12-letter lowercase string gives 56.4 bits, *more* than the 8-character "complex" password, so length beats composition. Six words picked by dice from a list of 7,776 give 77.5 bits and are easy to remember; 16 random alphanumeric characters give 95.3 bits and are best held in a password manager.

## 3.3 Work factors and key derivation

Never store passwords. Store the output of a **password hashing** (key derivation) function that is deliberately slow, together with a unique random **salt**. The salt ensures that identical passwords give different stored values and defeats precomputed tables; a secret server-side **pepper** can be added for extra protection. Fast general-purpose hashes (SHA-256 on its own) are the wrong tool, because speed helps whoever holds a stolen file.

The defender tunes a **cost parameter** so that one verification takes tens to hundreds of milliseconds, which is invisible to a legitimate user and multiplies the work of anyone testing guesses offline:

- **PBKDF2-HMAC** repeats the HMAC *c* times; OWASP guidance for PBKDF2-HMAC-SHA256 is 600,000 iterations. Its memory use is tiny, so specialised hardware parallelises it well.
- **bcrypt** has a cost factor *n* with work 2^n and a small fixed memory footprint; a 72-byte input limit applies.
- **scrypt** and **Argon2** are *memory-hard*: each guess needs a large block of memory, which limits how many guesses specialised hardware can run in parallel. **Argon2id** (RFC 9106) is the usual recommendation; OWASP's minimum profile is 19 MiB of memory, 2 passes and 1 lane.

The next program is pure arithmetic for the planning figures a defender uses. It assumes, for planning purposes only, an adversary with specialised hardware holding a stolen file of *fast* hashes and able to test 10 billion candidates per second.

```python
space = 95 ** 8
half = space // 2                          # expected search effort is about half the space
rate = 1e10                                # assumed planning figure: guesses per second against a fast hash
days = half / rate / 86400
years = half * 600000 / rate / 86400 / 365 # each guess costs 600000 times more work under PBKDF2
print(f"fast hash at 1e10 guesses/s: {days:.2f} days")
print(f"PBKDF2 at 600000 iterations: {years:.0f} years")
print(f"argon2 memory bound: {24 * 1024 // 19} instances in 24 GiB")
```
```output
fast hash at 1e10 guesses/s: 3.84 days
PBKDF2 at 600000 iterations: 6311 years
argon2 memory bound: 1293 instances in 24 GiB
```
Against a fast hash, the average search of a random 8-character password takes only 3.84 days at that rate, so a stolen unsalted fast-hash database of such passwords is nearly worthless to the owner. With 600,000 iterations the same search stretches to roughly 6311 years of the same hardware, a 600,000-fold increase. The last line shows why memory-hardness matters: a 24 GiB accelerator can hold only 1293 simultaneous 19 MiB Argon2 instances, which caps its parallelism regardless of its raw compute. These figures are planning arithmetic, not predictions: real guess rates, password distributions and hardware change continuously.

The following verification routine shows the defensive pattern: a fresh random salt per user, a slow derivation, and a **constant-time comparison** (`hmac.compare_digest`) so that the time taken does not leak how many bytes matched.

```python
import hashlib, hmac, os
ITER = 600000

def hash_pw(pw, salt):
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, ITER)

def verify(pw, salt, stored):
    return hmac.compare_digest(hash_pw(pw, salt), stored)

salt = os.urandom(16)
stored = hash_pw("correct horse battery staple", salt)
print(f"correct password accepted: {verify('correct horse battery staple', salt, stored)}")
print(f"wrong password accepted: {verify('not the password', salt, stored)}")
other = hash_pw("correct horse battery staple", os.urandom(16))
print(f"same password, different salt, different hash: {other != stored}")
```
```output
correct password accepted: True
wrong password accepted: False
same password, different salt, different hash: True
```
::: caution
Online guessing is a different problem from offline guessing. Against a login page the controls are rate limiting, temporary lockout with care (lockouts can be abused to deny service), MFA and monitoring of failed logins. The work factor protects *stolen data*; the rate limit protects the *live service*.
:::

## 3.4 Access control models

Once a user is authenticated, an **access control model** decides what is permitted.

| Model | Who decides | Rule | Strength | Weakness |
|---|---|---|---|---|
| **DAC** (discretionary) | The resource owner | Owner grants rights via ACLs (file permissions) | Flexible, simple | Users can leak rights; hard to audit at scale |
| **MAC** (mandatory) | The system policy | Labels (clearance vs classification) enforced by the system | Strong, central control | Rigid; heavy administration |
| **RBAC** (role-based) | The administrator, via roles | Permissions attach to roles; users get roles | Maps to job functions; easy review | Role explosion; coarse for context |
| **ABAC** (attribute-based) | A policy engine | Rules over attributes of user, resource, action and environment | Very fine-grained; context aware | Complex policies; harder to analyse |

**Bell–LaPadula**, the classic confidentiality model behind MAC, has two rules: *no read up* (a subject may read only objects at or below its clearance) and *no write down* (a subject may write only at or above its level, so secrets cannot be copied to a lower level). **Biba** is its integrity twin with the directions reversed. **Separation of duties** (SoD) splits critical tasks so that no one person can complete both halves, for example creating *and* approving a payment.

```python
roles = {"clerk": {"create_payment", "view_invoice"}, "manager": {"approve_payment", "view_invoice"},
         "admin": {"manage_users"}}
users = {"alice": ["clerk"], "bob": ["manager"], "carol": ["clerk", "manager"], "dev": ["admin"]}

def can(user, perm):
    return any(perm in roles[r] for r in users[user])

for u in ("alice", "bob", "carol"):
    print(f"{u} can approve_payment: {can(u, 'approve_payment')}")
violations = [u for u in users if can(u, "create_payment") and can(u, "approve_payment")]
print(f"separation-of-duties violations: {violations}")

levels = {"public": 0, "internal": 1, "secret": 2}
def can_read(s, o):
    return levels[s] >= levels[o]
def can_write(s, o):
    return levels[s] <= levels[o]
print(f"internal reads secret: {can_read('internal', 'secret')}")
print(f"internal writes secret: {can_write('internal', 'secret')}")
print(f"secret writes public: {can_write('secret', 'public')}")
```
```output
alice can approve_payment: False
bob can approve_payment: True
carol can approve_payment: True
separation-of-duties violations: ['carol']
internal reads secret: False
internal writes secret: True
secret writes public: False
```
Each user is individually legitimate, but the *combination* of roles gives carol both halves of the payment workflow: the SoD check finds her. In Bell–LaPadula an internal user cannot read a secret document, may write upward into it, and a secret-cleared user cannot write down to public. RBAC reviews at this level (who holds which role, who holds conflicting roles) are a standard audit procedure.

## 3.5 Practical guidance

Use a password manager and a unique passphrase per service, enable phishing-resistant MFA on email and administrative accounts first, remove default and shared accounts, review privileged access regularly and log every authentication event. For privileged operations, use just-in-time elevation with approval and time limits.

## 3.6 Summary and exercises

Authentication combines factors, strength is quantified by entropy H = L × log₂(R) for random secrets, stored credentials use salted, slow, ideally memory-hard derivation with constant-time comparison, and authorisation follows DAC, MAC, RBAC or ABAC models, with separation of duties as a cross-cutting control.

1. Compute the entropy of a random 10-character password drawn from 62 symbols, and of 5 Diceware words.
2. Explain why a 12-letter lowercase random string is stronger than an 8-character mixed-case password with a symbol.
3. Why must a salt be unique per user, and why is it not secret?
4. Describe what the memory cost of Argon2 changes, compared with PBKDF2, for an adversary with many parallel processors.
5. Give a business example for each of DAC, MAC, RBAC and ABAC.
6. Extend the RBAC program with a role "auditor" that can view invoices only, and write a check that no user holds both auditor and clerk.

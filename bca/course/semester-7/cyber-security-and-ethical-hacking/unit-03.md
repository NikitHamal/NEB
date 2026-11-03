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

## 3.6 Seeing the ideas: factors in hardware, entropy bars and access models

Each authentication factor has a physical form. Plate 3.1 shows four: a hardware security key, a fingerprint sensor, a contactless smart card and the Trusted Platform Module chip that protects keys on a laptop motherboard.

```photogrid label="3.1" cols="4" ratio="1.0" caption="Authentication in hardware. (a) A YubiKey FIDO2 security key beside its packaging: something you have, phishing-resistant. (b) A laptop fingerprint reader: something you are. (c) A contactless RFID smart card of a metro system: something you have, read by radio. (d) The Infineon SLB9655 TPM chip on a motherboard, which stores keys so that they cannot be copied out."
@ photo id="bca401/yubikey" cap="FIDO2 security key"
fit 1.0
focus 0.75 0.5
@ photo id="bca401/fingerprint" cap="Fingerprint sensor"
fit 1.0
focus 0.5 0.45
@ photo id="bca401/metrocard" cap="RFID smart card"
fit 1.0
focus 0.55 0.5
@ photo id="bca401/tpm" cap="TPM chip on a board"
fit 1.0
focus 0.5 0.5
```

```svgfig label="3.1" caption="The three factor families and the strength ladder of second factors. Combining two different families is MFA; the ladder shows that not all second factors resist a fake login page."
f = Fig(580, 262)
for i, (t, s, fl, st) in enumerate([("Something you KNOW", "password, PIN, passphrase", BLUE, NAVY), ("Something you HAVE", "phone, security key, smart card", SAND, AMBER), ("Something you ARE", "fingerprint, face, iris", MINT, TEAL)]):
    f.box(8 + i * 192, 8, 180, 50, t + "\n" + s, fill=fl, stroke=st, size=10, bold=True)
f.text(290, 76, "Two different families = multi-factor authentication. Strength of the second factor:", size=10.5, color=NAVY, bold=True)
for i, (t, fl, st) in enumerate([("Password only", ROSE, RED), ("+ SMS code\n(SIM-swap risk)", "#fdba74", AMBER), ("+ TOTP app\n(can be relayed)", "#fde68a", AMBER), ("+ FIDO2 key or passkey\n(phishing resistant)", MINT, TEAL)]):
    f.box(8 + i * 144, 88, 136, 44, t, fill=fl, stroke=st, size=10, bold=True)
f.box(8, 150, 564, 100, "Why the ladder matters: a fake bank page can collect a password and a TOTP code\nand replay both within 30 seconds. A FIDO2 key signs a challenge that is bound to the\nreal website name, so the lookalike site gets nothing that works. This is why banks\nare moving to passkeys and why SMS should be the fallback, not the first choice.", fill="#f8fafc", stroke=SLATE, size=10)
```

```svgfig label="3.2" caption="Entropy in bits for five secrets, computed as length x log2(alphabet size). Each extra bit doubles the guesses. A 12-character password drawn from all 94 printable ASCII characters has 78.7 bits; six random words from a 7776-word list give 77.5 bits and are far easier to remember. Entropy applies only to randomly chosen secrets, not to human-chosen ones."
f = Fig(580, 212)
data = [("8 lowercase letters", 37.6, ROSE, RED), ("8 letters and digits (62)", 47.6, "#fdba74", AMBER), ("4 random words (7776)", 51.7, "#fde68a", AMBER), ("6 random words (7776)", 77.5, MINT, TEAL), ("12 printable chars (94)", 78.7, MINT, TEAL)]
for i, (t, v, fl, st) in enumerate(data):
    y = 14 + i * 36
    f.text(8, y + 14, t, size=10, color=NAVY, bold=True, anchor="start")
    f.box(190, y, v * 3.9, 26, "", fill=fl, stroke=st)
    f.text(190 + v * 3.9 + 6, y + 14, "%.1f bits" % v, size=10, color=SLATE, bold=True, anchor="start")
f.line(190, 8, 190, 196, color=SLATE)
f.text(380, 206, "bits of entropy (bar length)", size=9.5, color=SLATE)
```

```svgfig label="3.3" caption="Four access control models side by side. DAC lets the owner decide, MAC lets a central policy decide using labels, RBAC attaches permissions to roles and ABAC evaluates attributes at request time."
f = Fig(580, 226)
items = [("DAC", "Owner grants access\nExample: share a file\nwith a friend\nRisk: rights spread", BLUE, NAVY), ("MAC", "System policy and labels\nExample: Secret clearance\nreads Secret documents\nRisk: rigid", ROSE, RED),
         ("RBAC", "Permissions on roles\nExample: manager approves,\nclerk only creates\nRisk: role explosion", MINT, TEAL), ("ABAC", "Rules on attributes\nExample: nurse reads records\nonly in own ward, on duty\nRisk: complex policy", SAND, AMBER)]
for i, (t, s, fl, st) in enumerate(items):
    x = 8 + (i % 2) * 284
    y = 8 + (i // 2) * 110
    f.box(x, y, 278, 100, "", fill=fl, stroke=st)
    f.text(x + 139, y + 18, t, size=13, color=st, bold=True)
    f.text(x + 139, y + 62, s, size=10, color=SLATE)
```

### 3.6.1 Eight good practices for authentication

1. **Use multi-factor authentication.** Add a second factor from a different family to every important account. A stolen password alone then no longer opens the account. Start with email, banking and admin accounts.
2. **Prefer phishing-resistant factors.** Security keys and passkeys check the real website name. A lookalike page cannot reuse their answer. SMS codes are weaker because SIM-swap fraud can divert them.
3. **Allow long passphrases.** Length adds entropy faster than special symbols. A phrase of six random words is easier to remember than a short mixed password. Allow at least 64 characters and allow spaces.
4. **Screen against breached passwords.** Reject passwords that appear in public leak lists. Many Nepali users choose names plus birth years, which attackers try first. Screening stops these before they are saved.
5. **Store passwords with a slow salted hash.** Use a key-derivation function such as PBKDF2, bcrypt or Argon2 with a unique salt. The slow work factor makes mass guessing expensive. Never store plain text or an unsalted fast hash.
6. **Limit and watch failed attempts.** Rate-limit logins and alert on many failures. Lock or delay an account after repeated failures without letting attackers lock out real users forever. Logs help investigate attacks.
7. **Apply least privilege after login.** Authentication only proves who the user is. Authorisation, through RBAC or ABAC, decides what they may do. A clerk must not see manager functions.
8. **Plan recovery safely.** Account recovery is often the weakest door. Use backup codes, verified contacts and delays for sensitive resets. A helpdesk must verify identity before any reset.

## 3.7 Summary and exercises

Authentication combines factors, strength is quantified by entropy H = L × log₂(R) for random secrets, stored credentials use salted, slow, ideally memory-hard derivation with constant-time comparison, and authorisation follows DAC, MAC, RBAC or ABAC models, with separation of duties as a cross-cutting control.

1. Compute the entropy of a random 10-character password drawn from 62 symbols, and of 5 Diceware words.
2. Explain why a 12-letter lowercase random string is stronger than an 8-character mixed-case password with a symbol.
3. Why must a salt be unique per user, and why is it not secret?
4. Describe what the memory cost of Argon2 changes, compared with PBKDF2, for an adversary with many parallel processors.
5. Give a business example for each of DAC, MAC, RBAC and ABAC.
6. Extend the RBAC program with a role "auditor" that can view invoices only, and write a check that no user holds both auditor and clerk.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is multi-factor authentication? Compare SMS, TOTP and FIDO2 as second factors.**

*Introduction.* Authentication proves who a user is. Multi-factor authentication (MFA) demands proof from at least two different families: something you know, something you have and something you are (Figure 3.1).

*Why it helps.* A password can be guessed, reused or phished. If a second family is also required, a stolen password alone is not enough, which is why banks and ConnectIPS-style services ask for an OTP or device approval.

| Factor | How it works | Strength | Weakness |
|---|---|---|---|
| SMS code | Code sent by text message | Easy for everyone | SIM-swap fraud, interception |
| TOTP app | HMAC of a shared secret and the 30-second time window | Works offline | A fake page can relay the code in real time |
| FIDO2 key or passkey | Public-key signature bound to the website name | Phishing-resistant | Needs a device; recovery planning |

*Example.* A student's email protected by a password and a FIDO2 key is safe even if the password is leaked on a fake login page, because the key will not answer a lookalike site.

*Conclusion.* MFA greatly lowers account takeover risk. Choose the strongest factor each service supports and keep recovery codes safe.

**Q2 (5 marks). Define entropy of a password. Calculate and compare the strength of an 8-letter lowercase password and a six-word passphrase.**

*Introduction.* The entropy of a secret is the number of bits of uncertainty in it. If a secret is chosen uniformly at random from N possibilities, its entropy is log2 N bits, and each extra bit doubles the number of guesses (Figure 3.2).

*Formula.* For a password of length L over an alphabet of size A, entropy is H = L x log2 A.

*Case 1.* Eight random lowercase letters: H = 8 x log2 26 = 8 x 4.70 = 37.6 bits. The space is 26^8 = 208,827,064,576 passwords. An offline attacker testing 10^10 guesses per second against a fast unsalted hash needs only about 20.9 seconds to try all, and 10.4 seconds on average.

*Case 2.* Six words chosen randomly from a 7776-word list: H = 6 x log2 7776 = 6 x 12.92 = 77.5 bits. The space is 7776^6 = about 2.2 x 10^23. At the same rate, trying everything takes about 7.0 x 10^5 years.

| Secret | Entropy | Time at 10^10 guesses/s |
|---|---|---|
| 8 lowercase letters | 37.6 bits | 20.9 seconds |
| 6 random words | 77.5 bits | about 700,000 years |

*Warning.* These figures hold only for random choice. Human-chosen passwords such as a name plus a year are far weaker, so users should let a password manager generate them. Slow salted hashes (PBKDF2, bcrypt, Argon2) multiply the attacker's cost further.

**Q3 (10 marks). Explain the access control models DAC, MAC, RBAC and ABAC with a suitable example of each. Which model suits a hospital information system?**

*Introduction.* Once a user is authenticated, an access control model decides what the user may do. Different models trade flexibility against central control (section 3.4 and Figure 3.3).

*1. Discretionary access control (DAC).* The owner of a resource decides who may access it, usually with an access control list. File permissions on Linux and sharing a document with a friend are examples. It is flexible and simple but users can pass rights on carelessly, so it is hard to audit at scale.

*2. Mandatory access control (MAC).* A central policy enforces labels. Each subject has a clearance and each object a classification. The Bell-LaPadula model has two rules: no read up (a subject reads only at or below its clearance) and no write down (a subject cannot copy secrets to a lower level). For example, a person cleared Confidential cannot read a Secret file, and a Secret user cannot save a Secret summary into a public folder. It is strong but rigid.

*3. Role-based access control (RBAC).* Permissions belong to roles and users receive roles. In a payment workflow a clerk role has create_payment and view_invoice, while a manager role has approve_payment and view_invoice. A clerk therefore cannot approve their own payment, which enforces separation of duties. The weakness is role explosion when many special cases appear.

*4. Attribute-based access control (ABAC).* A policy engine evaluates attributes of the user, resource, action and environment at request time. For example, allow a nurse to read a record only if the patient is in her ward and she is on duty. It is very fine grained but policies are harder to design and test.

| Model | Decided by | Strength | Weakness | Example |
|---|---|---|---|---|
| DAC | Owner | Simple | Rights leak | Shared file |
| MAC | System labels | Strong | Rigid | Classified documents |
| RBAC | Administrator, roles | Easy review | Role explosion | Clerk and manager |
| ABAC | Policy engine | Context aware | Complex | Nurse in own ward |

*Suitable choice.* A hospital needs RBAC for the main structure (doctor, nurse, billing clerk) with ABAC rules for context, such as the patient's ward, the shift and emergency "break-glass" access that is logged and reviewed. Pure MAC would be too rigid for emergencies, and pure DAC would let patient records spread.

*Conclusion.* No single model fits all cases. Real systems combine RBAC for clarity, ABAC for context and strict logging, always following the principle of least privilege.

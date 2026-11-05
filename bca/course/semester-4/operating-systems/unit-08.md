---
subject: Operating Systems
grade: BCA Semester 4
unit: 8
title: Security Management
hours: 3
area: BCA 251 · Operating Systems · Unit 8
---

An OS holds your files, passwords and bank sessions. Security is the discipline of keeping the *wrong* people and programs away from them while letting the *right* ones work. Protection (Unit 7) is the mechanism; **security** is the larger problem of authenticating users and resisting attack. The numbers in this unit were computed in Python (`bca/tools/check_os_misc.py`).

::: key What this unit gives you
- The security problem and the goals: confidentiality, integrity, availability.
- User authentication: passwords, their weaknesses, hashing and salting, one-time passwords, biometrics.
- Authorization.
- Program threats (Trojan horse, trap door, buffer overflow) and system threats (worms, viruses, denial of service).
:::

## 8.1 The security problem

A system is **secure** if its resources are used and accessed as intended under all circumstances. The classical goals are the **CIA triad**:

| Goal | Meaning | Violated by |
|---|---|---|
| **Confidentiality** | only authorised parties read the data | eavesdropping, stolen database |
| **Integrity** | only authorised parties change the data | tampering, virus altering files |
| **Availability** | legitimate users can use the system | denial of service, ransomware |

Attackers exploit the weakest link, often people (**social engineering**: phishing, a caller pretending to be IT support). Security is therefore needed at four levels: **physical** (locked server room), **human** (training, careful password handling), **operating system** (this unit and Unit 7) and **network**.

## 8.2 User authentication

Authentication proves *who you are*. The three families of evidence:

1. **Something you know**: password, PIN.
2. **Something you have**: smartphone, smart card, hardware token.
3. **Something you are**: fingerprint, face, iris.

Using two or more families is **multi-factor authentication (MFA)**, for example an ATM card plus PIN, or a bank app password plus an SMS or authenticator code.

### Passwords and their vulnerabilities

Passwords are cheap but weak. Attacks: **guessing** (birthdays, "123456"), **dictionary attack** (try common words and variations), **brute force** (try everything), **shoulder surfing**, **keylogging**, **phishing**, and reuse of a leaked password on other sites.

Brute-force cost depends on the character set and the length. At an assumed 10⁹ guesses per second (a good GPU against a fast unsalted hash):

| Password | Possibilities | Time at 10⁹ guesses/s |
|---|---|---|
| 8 lowercase letters (26⁸) | 208,827,064,576 | **209 seconds** (about 3.5 minutes) |
| 8 letters + digits (36⁸) | 2,821,109,907,456 | 2,821 seconds ≈ 47 minutes |
| 8 printable ASCII (95⁸) | 6,634,204,312,890,625 | 6.6 × 10⁶ s ≈ **77 days** |
| 12 printable ASCII (95¹²) | 5.4 × 10²³ | 5.4 × 10¹⁴ s ≈ **17 million years** |

**Length beats complexity.** Adding four characters multiplies the work by 95⁴ ≈ 81 million. Real users pick predictable passwords, so the true search space is far smaller than the table, which is why dictionary attacks work.

### Encrypted (hashed) passwords

A system must never store passwords in plain text. It stores a **one-way hash** h(password); at login it hashes the typed password and compares. A stolen file then yields only hashes. Two refinements are essential:

- **Salt**: a random value stored beside the hash and mixed in, so two users with the same password get different hashes and **precomputed (rainbow) tables** become useless.
- **Slow hashing**: functions such as bcrypt, scrypt, Argon2 and PBKDF2 repeat the computation thousands of times, making each guess expensive.

Real output of Python's `hashlib` for the password `nepal123` (first 32 hex digits shown):

```text
sha256('nepal123')        = bda4423a69fcc5aed2bad4acb580dd5a...
sha256(salt+'nepal123')   = 22a43f6baab6158b6aa47bba7dbc0b2b...
pbkdf2-sha256 x100000     = eddbe59cb38808bb7557e8263a9de235...
```

The same password gives completely different digests once salted and stretched. UNIX stores these in `/etc/shadow`, readable only by root, instead of the world-readable `/etc/passwd`.

::: caution Plain SHA-256 is not a password hash
SHA-256 is designed to be fast, which helps the attacker. The 10⁹ guesses/s assumed above is realistic against it. PBKDF2 with 100,000 iterations makes each guess about 100,000 times slower, cutting that rate to roughly 10⁴ guesses/s per device.
:::

### One-time passwords

A **one-time password (OTP)** is valid for a single login, so a captured one is useless. Methods: a printed list; a hash chain (S/KEY); and the standard **HOTP** (counter-based) and **TOTP** (time-based) algorithms. HOTP computes HMAC-SHA-1(secret, counter), takes 4 bytes selected by the low nibble of the digest, and keeps the last digits. For the RFC 4226 test secret `12345678901234567890`, the real codes for counters 0 to 9 computed here are:

```text
755224 287082 359152 969429 338314 254676 287922 162583 399871 520489
```

These agree with the RFC's published test values. TOTP uses the counter ⌊time / 30 s⌋; authenticator apps and many Nepali banks' mobile apps follow this scheme. (The RFC 6238 test vector for time 59 s gives 94287082 with 8 digits.)

### Biometrics

Fingerprint, face, iris and voice recognition identify *you*. Weaknesses: they cannot be changed if stolen, they have **false accept** and **false reject** rates (set the threshold to trade one against the other), and they raise privacy concerns. Typically used as one factor among several.

## 8.3 User authorization

Authentication asks *who are you*; **authorization** asks *what may you do*. After login, each process carries the user's identity and every access is checked against permission bits, ACLs or capabilities (Unit 7). Good practice: **least privilege** (run the web server as an unprivileged user), **separation of duties**, **auditing** (logs of access and failures), and short-lived credentials. On UNIX the **setuid** bit lets a program run with its owner's rights (so `passwd` can write the password file); a flaw in such a program is a route to full control, so these programs are kept few and small.

## 8.4 Program threats

### Trojan horse

A program that appears useful but contains hidden malicious code, running with the *user's* rights: a "free game" that sends files out, a fake installer. A variant is a spoofed login screen that records the typed password. Defence: install software only from trusted sources, verify checksums and signatures, and never put the current directory first in `PATH`.

### Trap door (back door)

A secret entry point left by the programmer: a hard-coded password or a special input that skips authentication. It may be added by an insider and is hard to find in a large code base; defences are code review and source-code control. (A well-known fictional example: a login that accepts a magic username without checking the password.)

### Stack and buffer overflow

The most common exploit of C programs. A function copies input into a fixed array without checking its size; extra bytes overwrite neighbouring memory, including the **return address** saved on the stack. The attacker supplies input that places machine code in the buffer and replaces the return address to point at it.

```c
void greet(const char *name) {
    char buf[16];
    strcpy(buf, name);        /* no length check: 16+ bytes overflow buf */
    printf("Hello, %s\n", buf);
}
```

The safe version bounds the copy: `snprintf(buf, sizeof buf, "%s", name)` or `strncpy` with explicit termination. Defences: bounds-checked languages, **stack canaries** (a secret value checked before return), **non-executable stack (NX)**, **address-space layout randomisation (ASLR)**, and compiler warnings. The classic functions to avoid are `gets`, `strcpy`, `sprintf` and `scanf("%s")` without a width.

## 8.5 System threats

| Threat | What it is | Spreads by |
|---|---|---|
| **Virus** | code attached to a host program; runs when the host runs; infects other files | user running infected files, e-mail attachments, USB drives (needs a host and user action) |
| **Worm** | self-contained program that copies itself across a network *without* a host or user action | exploiting network service flaws (the Morris worm 1988; Blaster, WannaCry 2017) |
| **Denial of service (DoS)** | makes a service unavailable by exhausting resources | flooding with requests; **DDoS** uses thousands of compromised machines (a *botnet*) |
| **Ransomware** | encrypts the victim's files and demands payment | phishing, unpatched services |
| **Spyware / keylogger** | records activity | bundled software |

**Virus types:** file infector, boot-sector, macro (documents), polymorphic (changes its code to evade scanners). **Defences:** keep the OS patched, use an antivirus (signature and behaviour-based), a **firewall**, regular **backups** (the only reliable cure for ransomware), disable macros from unknown sources, and teach users not to click unknown links. **For DoS:** rate-limiting, traffic filtering, upstream scrubbing, and spare capacity.

::: example A DoS in numbers
A small web server can handle 2,000 requests per second. An attacker with 500 bots sending 10 requests each per second produces 5,000 requests per second: 2.5 times capacity. Legitimate requests are dropped or time out, and the service is down without a single file being touched. This is an attack on **availability**, not confidentiality.
:::

## Formula and fact sheet

- CIA: confidentiality, integrity, availability.
- Search space = (alphabet size)^length; time = space ÷ guess rate; average success after half the space.
- Hash passwords with a **salt** and a **slow** function (bcrypt, scrypt, Argon2, PBKDF2).
- MFA = two of: know, have, are.
- Virus needs a host and user action; worm spreads alone; Trojan disguises itself; trap door bypasses authentication; overflow overwrites the return address.

## Chapter summary

- Security aims at confidentiality, integrity and availability and must be applied at physical, human, OS and network levels.
- Passwords are weak against guessing and brute force; they must be stored salted and hashed; longer is far better than "complex".
- OTPs (HOTP/TOTP), tokens and biometrics add factors; authorization applies least privilege after login.
- Program threats (Trojan, trap door, buffer overflow) abuse trust in code; system threats (viruses, worms, DoS) abuse trust in the network and the host.

## Practice

1. Define the CIA triad with an example violation of each.
2. Explain three password attacks and two defences.
3. Why should passwords be stored hashed and salted? What does the salt prevent?
4. How long does exhaustive search of 6 lowercase letters take at 10⁸ guesses per second?
5. What is multi-factor authentication? Give an example from Nepali banking or e-wallets.
6. Distinguish authentication and authorization.
7. Explain how a buffer overflow lets an attacker run code, and three defences.
8. Differentiate virus, worm and Trojan horse.
9. What is a DoS attack? How does DDoS differ?
10. How does a TOTP code stay valid for only a short time?

::: note Answers and worked solutions
**1.** Confidentiality: leaked exam paper before the exam. Integrity: marks changed in the result database. Availability: the result portal is knocked offline by a flood on the night results are published.
**2.** Dictionary attack (try common words), brute force (try all combinations), phishing (trick the user into typing it). Defences: long, unique passwords and a password manager; MFA; rate-limiting and lockout; slow salted hashing.
**3.** A stolen file of plain passwords gives immediate access; a hashed file does not reveal the password directly. The salt makes identical passwords produce different hashes and defeats precomputed rainbow tables; the attacker must attack each user separately.
**4.** 26⁶ = 308,915,776 combinations ÷ 10⁸ = **3.09 seconds** to try everything (about 1.5 s on average).
**5.** Authentication with two or more factor types. Example: a banking app login with password (know) plus a one-time code sent by SMS or an authenticator app on the registered phone (have).
**6.** Authentication establishes identity (password check); authorization decides what the authenticated identity may do (file permissions, ACL).
**7.** An unchecked copy writes past a buffer onto the saved return address; the attacker supplies shellcode and an address pointing to it, so on return the CPU executes it. Defences: bounds-checked functions and languages, stack canaries, NX stack, ASLR.
**8.** Virus: attaches to a host program, needs user action to run and spread. Worm: stand-alone, spreads over the network by itself. Trojan: pretends to be useful, does not self-replicate.
**9.** DoS makes a service unavailable by overwhelming it with requests or exhausting resources. DDoS does it from many distributed machines (a botnet), making it hard to block by address.
**10.** The code is HMAC(secret, ⌊time/30⌋). When the 30-second window moves on, the counter changes and the old code no longer matches; the server accepts only the current (and maybe adjacent) windows.
:::

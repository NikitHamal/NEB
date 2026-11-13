---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 8
title: Malware, Intruders, Steganography, Network Management Security and Cyber Law
hours: 6
area: BCA 353 · Cryptography and Network Security · Unit 8 (system security, SNMP, SET and legal aspects)
---

The first seven units protect messages and perimeters. Textbook courses on network security also expect the topics that sit around them: **malicious software and intruders** (system security), **steganography** (hiding that a message exists), **network management security** (SNMP), the **Secure Electronic Transaction** idea of a dual signature, and the **legal frame** in which a security professional works. This unit covers them, with small programs that were run and whose output is printed.

::: key What this unit gives you
- A taxonomy of malware (virus, worm, trojan, ransomware, rootkit, bot, logic bomb, spyware) with their propagation and defences.
- Intruder classes, password attacks and the arithmetic of guessing; why salted slow hashes are required.
- Steganography versus cryptography, least-significant-bit embedding with a working program, and watermarking.
- SNMP versions 1, 2c and 3 and what each protects.
- The dual signature of SET and its modern descendant, 3-D Secure.
- Cybercrime categories and the Nepali legal setting (Electronic Transactions Act, 2063).
:::

## 8.1 Malicious software

**Malware** is software written to damage, disrupt or take control of a system. The classic classification separates programs that *need a host* from those that are *independent*, and those that *replicate* from those that do not.

| Type | How it spreads or acts | Typical payload | Main defence |
|---|---|---|---|
| Virus | attaches itself to a host file or boot sector; runs when the host runs | corrupt files, spread further | antivirus, no untrusted executables |
| Worm | self-replicates over the network by itself, using a vulnerability or e-mail | consumes bandwidth, installs a backdoor | patching, firewalls, segmentation |
| Trojan horse | looks useful, carries hidden code; does not replicate | backdoor, credential theft | install from trusted sources, application allow-lists |
| Ransomware | encrypts the victim's files (often with a hybrid scheme from unit 4) | demands payment for the key | offline backups, least privilege |
| Rootkit | hides processes, files and network connections at kernel or firmware level | persistent hidden access | secure boot, integrity checking |
| Bot / botnet | a compromised host that obeys a command-and-control server | DDoS, spam, click fraud | egress filtering, patching |
| Logic bomb | code that triggers on a condition (a date, a deleted account) | destroy data | code review, separation of duties |
| Spyware, keylogger | records keystrokes, screens, browsing | steal passwords and banking data | anti-malware, two-factor authentication |

**Phases of a virus**: dormant (waits for a trigger), propagation (copies itself), triggering (the condition occurs) and execution (the payload runs). Viruses hide with *encryption* (the body is encrypted, only the small decryptor is visible), *polymorphism* (the decryptor is rewritten for each copy) and *metamorphism* (the whole body is rewritten), which is why signature scanners are supplemented by behaviour-based detection.

Four historical cases show the pattern. The **Morris worm** (November 1988) was released by a Cornell student and exploited a buffer overflow in `fingerd`, a debug mode in `sendmail` and weak passwords; a bug in its re-infection check made it install many copies on each machine, so thousands of Internet hosts slowed to a stop. The **ILOVEYOU** worm (May 2000) travelled as a Visual Basic attachment named `LOVE-LETTER-FOR-YOU.TXT.vbs` and mailed itself to every address in the victim's Outlook address book, an early lesson in social engineering. **Stuxnet** (found in 2010) targeted industrial controllers, which showed that malware can cause physical damage. **WannaCry** (May 2017) combined ransomware with a worm that used the SMB vulnerability MS17-010 for which Microsoft had issued a patch two months earlier; unpatched machines were hit across the world, including hospitals.

### Countermeasures in layers

1. **Prevention**: apply security updates, remove unneeded services, use least privilege, train users not to open unexpected attachments and disable macros.
2. **Detection**: signature scanning (known byte patterns and hashes), heuristics (suspicious instruction sequences), behaviour monitoring (a program that suddenly rewrites thousands of files), sandboxing (run the file in an isolated virtual machine and watch it).
3. **Containment and recovery**: network segmentation to stop worms, immutable offline backups tested by restoring, an incident response plan.

## 8.2 Intruders and password attacks

An **intruder** is a person who gains access to a system or resources without authorisation. Stallings' classification is still the clearest: a **masquerader** is an outsider who uses a legitimate user's account; a **misfeasor** is a legitimate user who accesses data or resources beyond his rights; a **clandestine user** seizes supervisory control and uses it to evade auditing. Techniques include password guessing, dictionary attacks, rainbow tables, phishing, shoulder surfing, exploiting unpatched software and, increasingly, **credential stuffing** (trying passwords leaked from one site on other sites).

### The arithmetic of guessing

If a password is drawn at random from an alphabet of size *a* with length *n*, the search space is *a*<sup>n</sup>. The program below compares several policies against an attacker who can test 10 billion hashes per second, a realistic figure for a fast unsalted hash such as MD5 on a few graphics cards.

```python
import math

RATE = 1e10   # guesses per second against a fast hash

def report(name, alphabet, n):
    space = alphabet ** n
    bits = math.log2(space)
    seconds = space / 2 / RATE      # on average half the space is searched
    if seconds < 60:
        t = f"{seconds:.2f} s"
    elif seconds < 86400:
        t = f"{seconds / 3600:.2f} h"
    elif seconds < 86400 * 365:
        t = f"{seconds / 86400:.1f} days"
    else:
        t = f"{seconds / (86400 * 365):.3g} years"
    print(f"{name:34s} {bits:6.1f} bits   average time {t}")

report("8 digits", 10, 8)
report("8 lowercase letters", 26, 8)
report("8 letters and digits (62)", 62, 8)
report("8 printable ASCII (95)", 95, 8)
report("12 printable ASCII (95)", 95, 12)
report("4 random words of a 7776 list", 7776, 4)
report("6 random words of a 7776 list", 7776, 6)
```
```output
8 digits                             26.6 bits   average time 0.01 s
8 lowercase letters                  37.6 bits   average time 10.44 s
8 letters and digits (62)            47.6 bits   average time 3.03 h
8 printable ASCII (95)               52.6 bits   average time 3.8 days
12 printable ASCII (95)              78.8 bits   average time 8.57e+05 years
4 random words of a 7776 list        51.7 bits   average time 2.1 days
6 random words of a 7776 list        77.5 bits   average time 3.51e+05 years
```
Two lessons follow. Length beats complexity: twelve random printable characters are far stronger than eight, and six random words (a *diceware* passphrase) are strong and easy to remember. And these numbers apply only to **random** choices; human passwords such as `Nepal@123` fall to dictionary rules in seconds, and a leaked-password list is searched before brute force.

### How a server should store passwords

Never store the password and never store a fast, unsalted hash. Store a **salt** (a unique random value per user) and the output of a deliberately **slow, memory-hard** function: Argon2id, scrypt, bcrypt or PBKDF2 with a high iteration count. The salt defeats precomputed rainbow tables and makes identical passwords hash differently; the slowness multiplies the attacker's cost per guess. Add rate limiting, account lockout with care (it can itself be used for denial of service), breach-password checks and multi-factor authentication. The program shows the effect of salt and iterations with Python's standard library:

```python
import hashlib, time

pw = b"nepal123"
for salt in (b"\x01" * 16, b"\x02" * 16):
    d = hashlib.pbkdf2_hmac("sha256", pw, salt, 1000)
    print("salt", salt[:1].hex(), "->", d.hex()[:16])

plain1 = hashlib.sha256(pw).hexdigest()[:16]
plain2 = hashlib.sha256(pw).hexdigest()[:16]
print("unsalted twice ->", plain1, plain2, "(identical, so a table works)")

def slow(n):
    t = time.perf_counter()
    hashlib.pbkdf2_hmac("sha256", pw, b"s" * 16, n)
    return time.perf_counter() - t

ratio = slow(200000) / max(slow(2000), 1e-9)
print("200000 iterations cost more than 2000 iterations:", ratio > 20)
```
```output
salt 01 -> 00b67b88c5ddd13e
salt 02 -> ad4edc7e8fae7aed
unsalted twice -> bda4423a69fcc5ae bda4423a69fcc5ae (identical, so a table works)
200000 iterations cost more than 2000 iterations: True
```
The last line prints a Boolean instead of a time, because timings differ between computers; the point is that 100 times the iterations costs about 100 times the time, for the defender once per login and for the attacker for every guess.

## 8.3 Steganography and watermarking

**Cryptography** hides the *meaning* of a message; an observer can see that a secret exists. **Steganography** (Greek: "covered writing") hides the *existence* of the message inside an innocent **cover** such as an image, audio file or text. The result is a **stego object**. Historical examples are invisible ink, microdots and the shaved-head message of Histiaeus. The two are complementary: encrypt first so that even a detected hidden message is unreadable, then hide.

| | Cryptography | Steganography |
|---|---|---|
| Goal | confidentiality of content | secrecy of existence |
| Visible to observer | yes, looks random | no, looks ordinary |
| Failure mode | cipher is broken | presence is detected |
| Metric | key size, cipher strength | capacity, invisibility, robustness |

### Least-significant-bit (LSB) embedding

A grey-scale pixel is a byte 0 to 255. Changing its lowest bit changes the brightness by at most 1 out of 256, which the eye cannot see. A message of *m* bits therefore needs *m* cover bytes (one bit each), and a 1024 x 768 grey image has capacity 786,432 bits = 98,304 bytes with 1 bit per pixel. The program hides two characters in 24 bytes and reads them back:

```python
cover = [(i * 37 + 11) % 256 for i in range(24)]       # stand-in for 24 pixels
message = "Hi"
bits = [int(b) for ch in message for b in format(ord(ch), "08b")]
print("message bits:", "".join(map(str, bits)))

stego = cover[:]
for i, bit in enumerate(bits):
    stego[i] = (cover[i] & ~1) | bit                    # replace the lowest bit

changed = sum(1 for a, b in zip(cover, stego) if a != b)
biggest = max(abs(a - b) for a, b in zip(cover, stego))
print("pixels changed:", changed, "of", len(cover), "largest change:", biggest)

got = [stego[i] & 1 for i in range(len(bits))]
text = "".join(chr(int("".join(map(str, got[k:k + 8])), 2)) for k in range(0, len(got), 8))
print("recovered:", text)
```
```output
message bits: 0100100001101001
pixels changed: 8 of 24 largest change: 1
recovered: Hi
```
Because the message bits are random-like, about half the pixels already carried the right bit, so about half are changed, and none by more than 1. LSB embedding is simple but fragile: re-saving the image as a JPEG, resizing it, or compressing the audio destroys the hidden bits. Statistical **steganalysis** (the chi-square test, RS analysis) detects it because the pairs of values (2k, 2k+1) become artificially equal in frequency. More robust schemes embed in the transform domain (the DCT coefficients of JPEG, spread-spectrum in audio).

### Watermarking

A **digital watermark** is a hidden mark whose purpose is *ownership or tracking*, not secret communication. A *robust* watermark must survive cropping and recompression (copyright marking of a photograph); a *fragile* watermark breaks on any change (tamper detection); a *fingerprint* encodes the buyer's identity so a leaked copy can be traced. Banknotes, e-books and streaming services all use it. Legitimate uses of steganography include protecting dissidents' communications; malware authors also use it to hide command channels in images, which is why security tools inspect unusual file sizes and entropy.

## 8.4 Network management security: SNMP

The **Simple Network Management Protocol (SNMP)** lets a management station monitor and configure routers, switches, printers and servers. A **manager** talks to an **agent** on each device; the agent exposes variables arranged in a tree called the **MIB** (Management Information Base), each named by an **object identifier (OID)** such as `1.3.6.1.2.1.1.5.0` (`sysName`). Operations: `GET`, `GETNEXT`, `GETBULK` (read), `SET` (write), `TRAP`/`INFORM` (an agent reports an event). SNMP uses UDP ports 161 (requests) and 162 (traps).

| Version | Authentication | Privacy | Notes |
|---|---|---|---|
| SNMPv1 | community string, sent in clear text | none | `public` and `private` defaults are guessed instantly |
| SNMPv2c | community string, clear text | none | adds `GETBULK` and 64-bit counters, same weak security |
| SNMPv3 | user-based (USM): HMAC-MD5/SHA with a per-user key | optional DES/AES encryption | view-based access control (VACM) limits which OIDs each user sees |

SNMPv3 offers three security levels: **noAuthNoPriv** (user name only), **authNoPriv** (messages authenticated with HMAC and protected against modification and replay by engine boots and time counters) and **authPriv** (authenticated and encrypted). Attacks against SNMP are practical: a read community string reveals the routing table and the device's configuration, and a write community lets an attacker reconfigure it. Defences: use SNMPv3 with authPriv, disable v1 and v2c, change default strings if they cannot be removed, restrict the manager's IP with an access list, place management traffic on a separate management VLAN, and do not expose UDP 161 to the Internet.

## 8.5 Secure Electronic Transaction and the dual signature

**SET** was a protocol designed by Visa and MasterCard (1996) for card payments over open networks. It was never widely deployed because it needed software and certificates on every cardholder's machine, but one idea in it remains important: the **dual signature**. Its problem is this: the merchant should see the **order information (OI)** but not the card number; the bank should see the **payment information (PI)** but not what is being bought; yet the two must be *linked*, so the merchant cannot reuse a payment for another order.

The customer computes `PIMD = H(PI)` and `OIMD = H(OI)`, joins them to give `POMD = H(PIMD || OIMD)` and signs `POMD` with his private key; that signature is the **dual signature DS**. The merchant receives OI, DS and PIMD; the bank receives PI, DS and OIMD.

```svgfig label="8.1" caption="The dual signature of SET. The merchant can recompute POMD from OI and PIMD without learning PI; the bank can recompute it from PI and OIMD without learning OI. Both can verify the same signature DS."
f = Fig(780, 270)
f.box(10, 20, 110, 40, "PI (payment\ninfo)", fill=SAND, stroke=NAVY, size=10, bold=True)
f.box(10, 150, 110, 40, "OI (order\ninfo)", fill=MINT, stroke=NAVY, size=10, bold=True)
f.box(170, 20, 100, 40, "PIMD = H(PI)", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(170, 150, 100, 40, "OIMD = H(OI)", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.arrow([(120, 40), (170, 40)], color=NAVY)
f.arrow([(120, 170), (170, 170)], color=NAVY)
f.box(320, 85, 130, 50, "POMD =\nH(PIMD || OIMD)", fill=SOFT, stroke=NAVY, size=10, bold=True)
f.arrow([(270, 40), (300, 40), (300, 100), (320, 100)], color=NAVY)
f.arrow([(270, 170), (300, 170), (300, 120), (320, 120)], color=NAVY)
f.box(500, 85, 120, 50, "DS = sign(\nPOMD, K_priv)", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.arrow([(450, 110), (500, 110)], color=NAVY)
f.box(650, 10, 120, 80, "Merchant gets\nOI, PIMD, DS", fill=MINT, stroke=NAVY, size=10, bold=True)
f.box(650, 150, 120, 80, "Bank gets\nPI, OIMD, DS", fill=SAND, stroke=NAVY, size=10, bold=True)
f.arrow([(620, 100), (635, 100), (635, 50), (650, 50)], color=TEAL)
f.arrow([(620, 120), (635, 120), (635, 190), (650, 190)], color=TEAL)
```

```python
import hashlib

def H(b):
    return hashlib.sha256(b).digest()

PI = b"card=4111-XXXX-XXXX-1111;amount=2500"
OI = b"item=USB-C cable;qty=2;shop=Kathmandu Tech"
PIMD, OIMD = H(PI), H(OI)
POMD = H(PIMD + OIMD)
print("POMD   :", POMD.hex()[:24])

merchant_view = H(PIMD + H(OI))      # merchant has OI and PIMD
bank_view = H(H(PI) + OIMD)                         # bank has PI and OIMD
print("merchant recomputes POMD:", merchant_view == POMD)
print("bank recomputes POMD    :", bank_view == POMD)

OI2 = b"item=Laptop;qty=1;shop=Kathmandu Tech"      # attacker reuses the payment
print("payment reused for another order verifies:", H(PIMD + H(OI2)) == POMD)
```
```output
POMD   : efb1bb233818b02d273e7f75
merchant recomputes POMD: True
bank recomputes POMD    : True
payment reused for another order verifies: False
```
Real systems have replaced SET with **3-D Secure** (Verified by Visa, Mastercard Identity Check, now 3-D Secure 2): the card issuer authenticates the cardholder with a one-time password or a banking app, and card data travels over TLS to a payment gateway; tokenisation and PCI DSS rules limit where card numbers are stored. The design goal of separating what each party may see lives on in tokenisation.

## 8.6 Cybercrime and the law

Security work happens within the law. **Cybercrime** is any crime in which a computer is the target, the tool or the place. Typical categories: unauthorised access (hacking), data theft and breach, malware distribution, denial of service, online fraud and phishing, identity theft, defamation and harassment, child sexual abuse material, and copyright violation.

In Nepal, the **Electronic Transactions Act, 2063 (2006)**, with its 2064 Rules, gives legal recognition to electronic records and **digital signatures**, creates the **Controller of Certification** and licensed certifying authorities (the PKI of unit 5), and lists computer-related offences: piracy and destruction of source code, unauthorised access to computer material, damage to a computer system or data, publishing illegal material and fraud, with fines and imprisonment fixed by the Act. The **Individual Privacy Act, 2075 (2018)** protects personal information, and the Constitution (2015) guarantees privacy. Reports go to the **Nepal Police Cyber Bureau**. Because the text of the Act and its amendments should be read in the current official version, quote section numbers in an exam only from your syllabus textbook. Internationally, the **Budapest Convention** (2001) harmonises cybercrime laws, GDPR governs personal data of EU residents, and professional codes (ACM, IEEE, ISC2) bind practitioners.

**Ethical rules for a student of security**: test only systems you own or are authorised in writing to test; report vulnerabilities responsibly (to the owner, with a reasonable time to fix); never keep or publish other people's data found during testing; and understand that "I was only learning" is not a defence.

## 8.7 Cloud, mobile and e-mail security in brief

- **Cloud**: the provider secures the infrastructure and you secure your data, identities and configuration (the *shared responsibility* model). Typical failures are public storage buckets, leaked access keys and over-privileged roles; defences are encryption at rest and in transit with customer-managed keys, multi-factor authentication, least-privilege roles and audit logs.
- **Mobile devices**: install apps only from official stores, review permissions, keep the OS updated, enable screen lock and device encryption (modern phones encrypt storage by default), and use mobile device management for staff phones.
- **E-mail**: PGP and S/MIME (unit 6) protect content end to end; SPF, DKIM and DMARC authenticate the sending domain and reduce spoofing; STARTTLS encrypts server-to-server hops.

## Chapter summary

- Malware types differ by host dependence and replication; defence is layered (patching, least privilege, detection, backups).
- Intruders are masqueraders, misfeasors or clandestine users; password strength is a matter of random length and slow salted hashing.
- Steganography hides existence, cryptography hides content; LSB embedding is simple, invisible and fragile.
- SNMPv1/v2c use clear-text community strings; SNMPv3 adds authentication, privacy and access control.
- The dual signature links PI and OI while hiding each from the wrong party.
- Law and ethics define what a security professional may do; in Nepal the Electronic Transactions Act, 2063 is the core statute.

## Practice

1. Differentiate a virus, a worm and a trojan horse.
2. List the four phases of a virus and explain polymorphism.
3. What made WannaCry spread so quickly?
4. Define masquerader, misfeasor and clandestine user.
5. Compute the search space of a 10-character password drawn from 62 characters, in bits.
6. Why must passwords be stored salted and with a slow hash?
7. Distinguish steganography and cryptography.
8. How many bytes can a 640 x 480 grey image hide at 1 bit per pixel?
9. Why does JPEG recompression destroy LSB data?
10. Compare SNMPv1, v2c and v3 security.
11. What problem does the dual signature in SET solve?
12. State three categories of cybercrime and the Nepali statute that covers digital signatures.

::: note Answers and worked solutions
**1.** A virus needs a host file and a user action to run; a worm replicates itself across the network without a host; a trojan pretends to be useful and does not replicate.
**2.** Dormant, propagation, triggering, execution. A polymorphic virus changes its decryptor (and so its byte signature) in every copy to evade signature scanners.
**3.** It combined ransomware with a worm that used the SMB vulnerability MS17-010 to infect unpatched machines on the same network, with no user action.
**4.** Masquerader: outsider using a valid account. Misfeasor: legitimate user exceeding rights. Clandestine user: one who takes supervisory control to avoid auditing.
**5.** 62^10, so 10 x log2(62) = 10 x 5.954 = 59.5 bits.
**6.** The salt makes equal passwords hash differently and kills rainbow tables; slowness (iterations or memory hardness) multiplies the attacker's cost per guess.
**7.** Cryptography makes the content unreadable but visible; steganography hides that any message exists.
**8.** 640 x 480 = 307,200 bits = 38,400 bytes.
**9.** Lossy compression quantises pixel values and discards the small changes that carry the lowest bits.
**10.** v1 and v2c: clear-text community string, no encryption. v3: per-user HMAC authentication, optional AES/DES encryption and view-based access control.
**11.** It lets merchant and bank each see only their part (OI or PI) while binding the two together so the payment cannot be attached to a different order.
**12.** Unauthorised access, online fraud/phishing and malware distribution; the Electronic Transactions Act, 2063 recognises digital signatures.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain the types of malicious software.**

Malware is software designed to harm or take control of a system. A **virus** attaches to a host file and spreads when the host is run; a **worm** replicates independently over a network; a **trojan horse** hides malicious code inside apparently useful software; **ransomware** encrypts files and demands payment; a **rootkit** hides the attacker's presence; a **bot** is a compromised machine controlled remotely, and many bots form a botnet used for denial of service; a **logic bomb** triggers on a condition; **spyware** records user activity. Defences are patching, least privilege, antivirus and behaviour monitoring, sandboxing, network segmentation and tested offline backups.

**Q (10 marks). What is steganography? Explain LSB image steganography, its capacity and weaknesses, and contrast it with cryptography and watermarking.**

Define steganography as hiding the existence of a message in a cover medium, and state the difference from cryptography (content versus existence; use both together). Explain LSB: each cover byte's lowest bit is replaced by one message bit, so a change is at most 1 of 256 grey levels; capacity is one bit per pixel, e.g. 640 x 480 gives 38,400 bytes. Give the embedding formula `stego = (cover & ~1) | bit` and the extraction `stego & 1`, and use the program of section 8.3. Weaknesses: destroyed by lossy compression, resizing and filtering; detectable by chi-square and RS steganalysis. Close with watermarking: its aim is ownership or tracking rather than secrecy, and it may be robust, fragile or a fingerprint.

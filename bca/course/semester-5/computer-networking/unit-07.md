---
subject: Computer Networking
grade: BCA Semester 5
unit: 7
title: Network Security
hours: 3
area: BCA 301 · Computer Networking · Unit 7
---

A network built only for speed and reach is a network built for attackers: every layer you met in this book was designed when the users were trusted colleagues. This unit gives the vocabulary of network security, the cryptographic tools (symmetric, public-key, hashes, signatures), the protocols that use them (TLS, IPsec, WPA2) and the defensive devices (firewalls, IDS, VPN). The RSA and hash examples are small enough to do by hand and are also executed by the program at the end.

::: key What this unit gives you
- Security goals and attacks: confidentiality, integrity, availability, authentication, non-repudiation.
- Cryptography: symmetric and public-key encryption, hashing, digital signatures, certificates.
- Secure protocols: TLS/HTTPS, IPsec and VPNs, WPA2/WPA3.
- Defences: firewalls, IDS/IPS, good practice.
:::

## 7.1 Security goals and threats

The **CIA triad**: **confidentiality** (only authorised parties can read), **integrity** (data is not altered unnoticed), **availability** (the service works when needed). Added goals are **authentication** (who are you?), **authorisation** (what may you do?) and **non-repudiation** (the sender cannot deny sending).

| Attack | Goal attacked | How it works | Typical defence |
|---|---|---|---|
| Eavesdropping / sniffing | confidentiality | capture frames on a shared or compromised link | encryption (TLS, WPA2) |
| Spoofing | authentication | forged source address, MAC or e-mail sender | ingress filtering, authentication, SPF |
| Man-in-the-middle | confidentiality, integrity | attacker relays and alters traffic (ARP spoofing, rogue access point) | TLS with certificate validation, dynamic ARP inspection |
| Replay | integrity | resend a captured valid message | nonces, timestamps, sequence numbers |
| Denial of service (DoS, DDoS) | availability | flood a victim (SYN flood, amplification via DNS) with traffic | rate limiting, SYN cookies, scrubbing services |
| Phishing, social engineering | authentication | trick users into giving credentials | training, multi-factor authentication |
| Malware: virus, worm, ransomware | all | self-spreading or extortion code | patching, backups, endpoint protection |

A **passive** attack only observes; an **active** attack modifies or injects. Passive attacks are hard to detect and are defeated by encryption; active attacks are detected by integrity checks.

## 7.2 Cryptography basics

**Plaintext** is encrypted with a **key** by an algorithm to give **ciphertext**; decryption reverses it. *Kerckhoffs' principle*: the algorithm is public, only the key is secret.

### Classical ciphers

A **Caesar** cipher shifts each letter by k (k = 3 turns "NEB" into "QHE"); only 25 keys, broken at once by trying all. A **monoalphabetic substitution** has 26! ≈ 4 × 10²⁶ keys but falls to letter-frequency analysis. **Vigenère** uses a repeating key to defeat simple frequency counts. **Transposition** rearranges letters. Modern ciphers combine substitution and transposition in many rounds (confusion and diffusion).

### Symmetric-key cryptography

The same secret key encrypts and decrypts. **DES** (56-bit key, now breakable in hours), **3DES**, and the standard **AES** (128-, 192- or 256-bit keys, block size 128 bits, 10, 12 or 14 rounds). A block cipher needs a **mode of operation**: ECB (each block alone: identical plaintext blocks give identical ciphertext, leaking patterns), **CBC** (each block XORed with the previous ciphertext), **CTR** and **GCM** (counter mode, with authentication). Strengths: fast. Weakness: the **key distribution problem**: n people who each need a private channel with every other need n(n − 1)/2 keys (45 keys for 10 people).

### Public-key cryptography

Each party has a **public key** (published) and a **private key** (secret). What one key encrypts, only the other decrypts. To send a secret to Bob, encrypt with Bob's public key; only Bob's private key opens it. Public-key operations are slow (about a thousand times slower than AES), so they are used to exchange a symmetric session key and to sign.

### The RSA algorithm

1. Choose two primes p and q; n = p q.
2. φ(n) = (p − 1)(q − 1).
3. Choose e coprime to φ(n); compute d with e d ≡ 1 (mod φ(n)).
4. Public key (e, n); private key (d, n). Encrypt: c = mᵉ mod n. Decrypt: m = cᵈ mod n.

::: example A textbook RSA example
p = 61, q = 53, so n = 3233 and φ = 60 × 52 = 3120. Take e = 17 (coprime to 3120); then d = 2753 because 17 × 2753 = 46,801 = 15 × 3120 + 1. Encrypt m = 65: c = 65¹⁷ mod 3233 = **2790**. Decrypt: 2790²⁷⁵³ mod 3233 = 65. A **signature** is the reverse: s = hᵈ mod n on the hash h, checked by anyone with the public key. Real RSA uses primes of 1024 bits or more (a 2048-bit n) and padding (OAEP, PSS); these small numbers are for understanding only.
:::

**Diffie–Hellman** lets two parties build a shared secret over a public channel: with public g and prime p, Alice picks a and sends gᵃ mod p, Bob picks b and sends gᵇ mod p, and both compute gᵃᵇ mod p. With p = 23, g = 5, a = 6 and b = 15: Alice sends 5⁶ mod 23 = 8, Bob sends 5¹⁵ mod 23 = 19, and the shared secret is 19⁶ mod 23 = 8¹⁵ mod 23 = 2. An eavesdropper sees only p, g, 8 and 19. Without authentication it is open to a man-in-the-middle.

### Hash functions

A **cryptographic hash** maps any input to a fixed-size digest and is **one-way**, **collision-resistant** and has the **avalanche** effect (one flipped input bit changes about half the output bits). **SHA-256** gives 256 bits; the digest of "abc" is ba7816bf 8f01cfea 414140de 5dae2223 b00361a3 96177a9c b410ff61 f20015ad. MD5 and SHA-1 are broken for collisions and must not be used for security. Hashes store passwords (with a per-user **salt** and a slow function such as bcrypt, scrypt or Argon2), check file integrity, and build blockchains. A **MAC** or **HMAC** is a hash keyed with a shared secret, giving integrity *and* authenticity.

### Digital signatures and certificates

A **digital signature** is the hash of a message encrypted with the sender's private key; anyone can verify it with the public key, which gives integrity, authentication and non-repudiation. But how do you know a public key belongs to Bob? A **certificate authority** (CA) signs an X.509 **certificate** that binds a name to a public key; browsers trust a list of root CAs, and a chain of certificates leads from the site's certificate up to a root. In Nepal the Controller of Certification (Office of the Controller of Certification, under the Electronic Transactions Act) licenses certifying authorities for digital signatures.

## 7.3 Secure protocols

### TLS (and HTTPS)

**Transport Layer Security** (successor to SSL) sits between TCP and the application and provides encryption, integrity and server authentication (optionally client authentication). A simplified TLS 1.3 handshake: (1) **ClientHello** with supported cipher suites and a key share (Diffie–Hellman); (2) **ServerHello** with the chosen suite, its key share and its **certificate** and a signature proving possession of the private key; (3) both derive session keys; (4) **Finished** messages confirm; (5) application data is encrypted with a symmetric cipher (AES-GCM or ChaCha20). TLS 1.3 needs one round trip (TLS 1.2 needed two), and the Diffie–Hellman exchange gives **forward secrecy**: stealing the server's long-term key later does not reveal old sessions. HTTPS = HTTP over TLS on port 443; the browser's padlock means the certificate matched the host name and was signed by a trusted CA, **not** that the site is honest.

### IPsec and VPNs

**IPsec** secures at the IP layer. The **AH** header gives integrity and authentication; **ESP** gives encryption plus integrity. In **transport mode** only the payload is protected (host to host); in **tunnel mode** the whole original packet is encrypted and wrapped in a new IP packet (gateway to gateway), the basis of a site-to-site **VPN**. Keys are negotiated by **IKE**. Remote-access VPNs use IPsec, TLS-based VPNs or WireGuard to give a traveller a private tunnel to the office network.

### Wireless security

WEP's RC4 usage is broken in minutes. **WPA2** uses AES-CCMP; with a pre-shared key (personal) all users share a passphrase, with **802.1X/EAP** (enterprise) each user has credentials checked by a RADIUS server. **WPA3** adds SAE (a password-authenticated key exchange resisting offline guessing) and mandatory protected management frames. Hiding the SSID and MAC filtering are not real security.

### E-mail and DNS security

**PGP/S-MIME** encrypt and sign mail end to end; **STARTTLS** protects the hop between servers; SPF, DKIM and DMARC authenticate sending domains; **DNSSEC** signs DNS records; **DNS over HTTPS/TLS** hides queries from eavesdroppers.

## 7.4 Firewalls and intrusion detection

A **firewall** enforces a policy between networks of different trust. Types:

- **Packet filter** (stateless): examines IP and port in each packet against an ordered rule list (an ACL); first match wins, with an implicit *deny all* at the end.
- **Stateful inspection**: remembers connections; return traffic of a connection initiated inside is allowed automatically; unsolicited inbound is dropped.
- **Application gateway (proxy)**: terminates the connection and inspects content (HTTP, SMTP); also used for caching and URL filtering.
- **Next-generation firewall**: adds application identification, intrusion prevention and user identity.

A **DMZ** (demilitarised zone) is a separate network segment for public-facing servers, so that a compromised web server does not sit on the internal LAN.

::: example An access control list
Allow web access to the DMZ web server 203.0.113.10 and deny everything else from outside:

| # | Action | Protocol | Source | Destination | Port |
|---|---|---|---|---|---|
| 1 | permit | TCP | any | 203.0.113.10 | 80, 443 |
| 2 | permit | TCP | established | any | any |
| 3 | deny | IP | any | any | — |

A packet to 203.0.113.10:443 matches rule 1 and passes; a packet to 203.0.113.10:22 matches no permit rule and hits rule 3.
:::

An **IDS** monitors traffic or hosts and *alerts*; an **IPS** sits in line and *blocks*. **Signature-based** detection matches known patterns (fast, misses new attacks); **anomaly-based** detection flags deviations from a baseline (finds new attacks, more false positives). Honeypots are decoy systems that attract and study attackers.

## 7.5 Good practice

Use TLS everywhere, keep systems patched, give users least privilege, segment networks (VLANs, DMZ), enable multi-factor authentication, back up offline, change default passwords on routers and cameras, disable unused services (a closed port cannot be attacked), log and monitor, and teach users to recognise phishing. Security is a process, not a product, and a chain is as strong as its weakest link, which is usually a person.

## Practising the commands

This program checks every cryptographic example above: Caesar, the RSA key and message, Diffie–Hellman, the SHA-256 digest, the avalanche effect and an HMAC check.

```python
import hashlib, hmac
print("Caesar +3:", "".join(chr((ord(ch) - 65 + 3) % 26 + 65) for ch in "NEB"))
p, q, e = 61, 53, 17; n = p * q; phi = (p - 1) * (q - 1); d = pow(e, -1, phi)
print("n", n, "phi", phi, "d", d, "check e*d mod phi =", e * d % phi)
c = pow(65, e, n); print("cipher", c, "plain", pow(c, d, n))
sig = pow(7, d, n); print("signature of h=7:", sig, "verifies:", pow(sig, e, n) == 7)
P, g, a, b = 23, 5, 6, 15; A, B = pow(g, a, P), pow(g, b, P)
print("DH:", A, B, pow(B, a, P), pow(A, b, P))
print(hashlib.sha256(b"abc").hexdigest())
x, y = hashlib.sha256(b"abc").digest(), hashlib.sha256(b"abd").digest()
print("avalanche bits changed:", sum(bin(i ^ j).count("1") for i, j in zip(x, y)), "of 256")
mac = hmac.new(b"key", b"message", hashlib.sha256).hexdigest(); print(mac[:16], hmac.compare_digest(mac, hmac.new(b"key", b"message", hashlib.sha256).hexdigest()))
print("keys for 10 people (symmetric):", 10 * 9 // 2)
```
```output
Caesar +3: QHE
n 3233 phi 3120 d 2753 check e*d mod phi = 1
cipher 2790 plain 65
signature of h=7: 2667 verifies: True
DH: 8 19 2 2
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
avalanche bits changed: 122 of 256
6e9ef29b75fffc5b True
keys for 10 people (symmetric): 45
```
## 7.6 Seeing the ideas: ciphers, keys, hashes, handshakes and firewalls

Security is mostly arithmetic that can be checked, so this section computes the unit's examples instead of only describing them. Plate 7.1 shows the history of secret writing in three objects: a bust of Julius Caesar (whose shift cipher gives the simplest example), an Enigma machine and a Lorenz cipher machine from the Second World War. Plate 7.2 shows the people and the machine of modern cryptography: Diffie and Hellman (public-key exchange), Rivest, Shamir and Adleman (RSA) and the DES-cracking board that proved a 56-bit key was too short. Plate 7.3 shows the inside of a real firewall appliance and a hardware security key. The figures that follow compute the Caesar cipher and its key space, letter-frequency analysis, key counts, the RSA and Diffie-Hellman examples, the avalanche effect of a hash, digital signatures and certificates, the TLS handshake, IPsec modes, an access control list, two denial-of-service attacks and password strength.

```photogrid label="7.1" cols="3" ratio="1.0" caption="Secret writing, old and mechanical. (a) A marble bust of Julius Caesar (CC0), who is said to have shifted each letter of his orders by three places: the first well-known substitution cipher, with only 25 possible keys. (b) A three-rotor Enigma machine in its wooden case (CC BY-SA 2.0 France): each key press turns the rotors and changes the substitution, so the same letter encrypts differently every time, yet the key settings were eventually recovered. (c) A Lorenz SZ42 teleprinter cipher machine (CC0) at a museum, used for the German high command; it was broken at Bletchley Park without ever having seen a machine."
@ photo id="bca301/caesar" cap="Caesar: shift cipher"
fit 1.0
focus 0.5 0.3
@ photo id="bca301/enigma" cap="Enigma: rotor machine"
fit 1.0
focus 0.4 0.5
@ photo id="bca301/lorenz" cap="Lorenz SZ42: teleprinter cipher"
fit 1.0
focus 0.4 0.55
```

```photogrid label="7.2" cols="3" ratio="1.25" caption="Modern cryptography. (a) Whitfield Diffie (left) and Martin Hellman (right) (CC BY-SA 3.0), who published the first public key exchange in 1976. (b) Ron Rivest, Adi Shamir and Leonard Adleman (CC BY-SA 3.0) answering questions at the CRYPTO 2017 conference; their 1977 RSA algorithm is the basis of most digital signatures. (c) A circuit board from the Electronic Frontier Foundation's DES cracker (CC BY-SA 3.0): each board carries many custom chips that tried keys in parallel, and in 1998 the machine found a 56-bit DES key in under three days, which ended DES as a secure cipher."
@ photo id="bca301/diffie" cap="Diffie and Hellman: key exchange"
fit 1.25
focus 0.5 0.4
@ photo id="bca301/rsatrio" cap="Rivest, Shamir, Adleman: RSA"
fit 1.25
focus 0.5 0.5
@ photo id="bca301/descrack" cap="DES cracker board: 56 bits fell"
fit 1.25
focus 0.5 0.5
```

```photogrid label="7.3" cols="3" ratio="1.25" caption="Hardware that enforces security. (a) The inside of a small business firewall and VPN router (CC BY-SA 3.0): the green board carries the processor and network chips under the aluminium heat sinks, and the row of sockets at the right edge are the Ethernet ports that connect the Internet, the DMZ and the LAN. (b) A YubiKey hardware security key beside a bunch of house keys (CC BY 4.0): it holds a private key that never leaves the device, so a phishing site cannot steal it. (c) The three kinds of evidence behind multi-factor authentication."
@ photo id="bca301/firewall" cap="Firewall appliance: inside"
fit 1.25
focus 0.5 0.5
call 0.5 0.92 0.4 0.45 "heat sinks"
@ photo id="bca301/yubikey" cap="Hardware security key (FIDO2)"
fit 1.25
focus 0.65 0.5
@ svg cap="Three kinds of evidence"
f = Fig(300, 240)
f.text(150, 16, "Multi-factor authentication", size=13, color=NAVY, bold=True)
rows = [("Something you KNOW", "password, PIN", BLUE, NAVY), ("Something you HAVE", "phone OTP, key", MINT, TEAL), ("Something you ARE", "fingerprint, face", SAND, AMBER)]
for i, (a, b, fl, st) in enumerate(rows):
    y = 30 + i * 52
    f.box(6, y, 288, 44, a + "\n" + b, fill=fl, stroke=st, size=12.5, r=6, color=NAVY, bold=True)
f.text(150, 206, "two different kinds = much harder", size=12, color=RED, bold=True)
f.text(150, 226, "to steal than a password alone", size=12, color=RED, bold=True)
```

```svgfig label="7.1" caption="The goals of security and the attacks aimed at them. The CIA triad is confidentiality (only the right people can read), integrity (data is not changed unnoticed) and availability (the service works when needed). Eavesdropping and sniffing attack confidentiality, tampering and man-in-the-middle attacks attack integrity, and denial of service attacks availability. Three further goals sit beside the triad: authentication (who are you?), authorisation (what may you do?) and non-repudiation (you cannot deny sending). A passive attack only observes and is defeated by encryption; an active attack modifies or injects and is detected by integrity checks."
f = Fig(580, 304)
cm = __import__("math")
cx, cy, R = 290, 150, 88
pts = [(cx, cy - R), (cx + R * cm.sin(2 * cm.pi / 3), cy - R * cm.cos(2 * cm.pi / 3)), (cx + R * cm.sin(4 * cm.pi / 3), cy - R * cm.cos(4 * cm.pi / 3))]
for i in range(3):
    a, b = pts[i], pts[(i + 1) % 3]
    f.line(a[0], a[1], b[0], b[1], color="#94a3b8", sw=2.4)
cols = [("Confidentiality", BLUE, NAVY), ("Integrity", MINT, TEAL), ("Availability", SAND, AMBER)]
for (x, y), (t, fl, st) in zip(pts, cols):
    f.circle(x, y, 30, fill=fl, stroke=st, sw=2)
    f.text(x, y, t[0], size=20, color=st, bold=True, vmid=True)
f.text(cx, cy - R - 42, "Confidentiality", size=11, color=NAVY, bold=True)
f.text(pts[1][0] + 44, pts[1][1] + 34, "Integrity", size=11, color=TEAL, bold=True)
f.text(pts[2][0] - 8, pts[2][1] + 40, "Availability", size=11, color=AMBER, bold=True, anchor="end")
f.text(cx, cy + 6, "CIA", size=18, color=NAVY, bold=True)
f.box(380, 22, 190, 56, "attacks:\nsniffing, eavesdropping,\nphishing for secrets", fill="#fee2e2", stroke=RED, size=9.5, r=5, color=RED)
f.arrow([(380, 50), (330, 80)], color=RED, sw=1.5)
f.box(412, 138, 160, 60, "attacks:\ntampering, replay,\nman-in-the-middle", fill="#fee2e2", stroke=RED, size=9.5, r=5, color=RED)
f.arrow([(412, 168), (382, 190)], color=RED, sw=1.5)
f.box(8, 244, 190, 50, "attacks:\nDoS, DDoS, SYN flood,\nransomware", fill="#fee2e2", stroke=RED, size=9.5, r=5, color=RED)
f.arrow([(120, 244), (200, 206)], color=RED, sw=1.5)
f.box(8, 22, 190, 56, "also needed:\nauthentication, authorisation,\nnon-repudiation", fill="#ffffff", stroke=SLATE, size=9.5, r=5, dash=True, color=SLATE)
f.text(430, 252, "passive: observe only (defeat by encryption)", size=9.5, color=SLATE, anchor="middle")
f.text(430, 268, "active: modify or inject (detect by integrity)", size=9.5, color=SLATE, anchor="middle")
```

```svgfig label="7.2" caption="The Caesar cipher computed. The cipher alphabet is the plain alphabet shifted left by k = 3, so N E B becomes Q H E. Because there are only 25 useful keys, an attacker simply tries them all (rows below): decrypting QHE with k = 1, 2, 3, 4 and 5 gives PGD, OFC, NEB, MDA and LCZ, and only k = 3 makes sense. A general substitution cipher has 26! = 4.03 x 10^26 keys, far too many to try, yet it still falls to letter-frequency analysis (Fig. 7.3); a modern 128-bit key has 2^128 = 3.4 x 10^38 keys."
f = Fig(580, 290)
cm = __import__("math")
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
k = 3
enc = lambda s, k: "".join(A[(A.index(c) + k) % 26] for c in s)
assert enc("NEB", 3) == "QHE"
f.text(290, 14, "Caesar cipher, key k = 3: each letter moves 3 places on", size=11, color=NAVY, bold=True)
for i, c in enumerate(A):
    x = 12 + i * 21.5
    hl = c in "NEB"
    f.box(x, 26, 20, 24, c, fill="#fde68a" if hl else BLUE, stroke=AMBER if hl else NAVY, size=10, r=2, bold=True, color=NAVY, sw=1)
    d = A[(i + k) % 26]
    f.box(x, 62, 20, 24, d, fill="#fde68a" if d in "QHE" else MINT, stroke=AMBER if d in "QHE" else TEAL, size=10, r=2, bold=True, color=NAVY, sw=1)
f.text(10, 98, "plain", size=9.5, color=SLATE, anchor="start")
f.text(10, 108, "cipher", size=9.5, color=SLATE, anchor="start")
f.text(290, 126, "NEB  ->  %s       (cipher text QHE is read back with k = 3)" % enc("NEB", 3), size=11, color=RED, bold=True)
f.text(145, 150, "Brute force: try every key on QHE", size=10.5, color=NAVY, bold=True)
for j, kk in enumerate(range(1, 6)):
    y = 160 + j * 24
    ok = kk == 3
    f.box(20, y, 60, 20, "k = %d" % kk, fill="#fde68a" if ok else SOFT, stroke=AMBER if ok else "#94a3b8", size=10, r=3, color=NAVY, bold=ok)
    f.box(88, y, 60, 20, enc("QHE", -kk), fill="#fde68a" if ok else SOFT, stroke=AMBER if ok else "#94a3b8", size=10.5, r=3, bold=True, color=NAVY)
    if ok: f.text(160, y + 10, "<- readable", size=10, color=RED, bold=True, anchor="start", vmid=True)
f.text(450, 150, "key space", size=10.5, color=NAVY, bold=True)
spaces = [("Caesar", 25), ("substitution", cm.factorial(26)), ("AES-128", 2 ** 128)]
for j, (nm, v) in enumerate(spaces):
    y = 162 + j * 36
    e = cm.log10(v)
    f.text(296, y + 10, nm, size=10, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(384, y, max(4, e * 3), 20, "", fill=SAND if j < 2 else MINT, stroke=AMBER if j < 2 else TEAL, r=2)
    f.text(384 + max(4, e * 3) + 5, y + 10, ("%d keys" % v) if v < 1000 else ("%.2e" % v), size=10, color=RED, bold=True, anchor="start", vmid=True)
f.text(290, 278, "bar length = number of digits in the key space (log scale)", size=9.5, color=SLATE)
```

```svgfig label="7.3" caption="Why simple substitution fails: letter frequencies, computed from a 310-letter sample of English. In plain English the most common letter is E; after a Caesar shift of 3 the same bar pattern appears three places to the right, so the tallest bar sits at H. An attacker who sees that one letter dominates the ciphertext guesses it stands for E and recovers the key in one step. The same method breaks any monoalphabetic substitution, because each plain letter always maps to the same cipher letter. Modern ciphers hide statistics by using many rounds and keys that change for every block."
f = Fig(580, 296)
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
text = "THE NETWORK SECURITY OF A NATION DEPENDS ON THE TRUST THAT PEOPLE PLACE IN THE SYSTEMS THEY USE EVERY DAY WHEN A STUDENT PAYS A FEE THROUGH A MOBILE WALLET OR READS AN EXAM RESULT ON A PORTAL THE MESSAGES MUST REACH THE RIGHT PERSON UNCHANGED AND UNREAD BY ANYONE ELSE ENCRYPTION GIVES THE SECRECY AND A HASH GIVES THE PROOF THAT NOTHING WAS ALTERED ON THE WAY BETWEEN THE TWO ENDS"
cnt = [text.count(c) for c in A]
n = sum(cnt)
top = max(range(26), key=lambda i: cnt[i])
assert A[top] == "E"
sh = [cnt[(i - 3) % 26] for i in range(26)]
def panel(y0, vals, title, col, hl):
    f.text(290, y0, title, size=10.5, color=NAVY, bold=True)
    for i, v in enumerate(vals):
        x = 22 + i * 21
        h = v * 1.8
        f.box(x, y0 + 100 - h, 17, h, "", fill="#fde68a" if i == hl else col, stroke=AMBER if i == hl else NAVY, r=1, sw=1)
        f.text(x + 8.5, y0 + 112, A[i], size=9.5, color=SLATE)
        if v >= 20:
            f.text(x + 8.5, y0 + 96 - h, str(v), size=9.5, color=RED, bold=True)
panel(14, cnt, "plaintext (%d letters): tallest bar E" % n, BLUE, top)
panel(150, sh, "after Caesar shift of 3: tallest bar H", MINT, (top + 3) % 26)
f.text(290, 284, "E = %d of %d letters = %.1f percent; the pattern only moves 3 places" % (cnt[top], n, 100 * cnt[top] / n), size=10, color=SLATE)
```

```svgfig label="7.4" caption="The key distribution problem and how public-key cryptography removes it. With symmetric keys every pair of users needs its own secret key, so n users need n(n - 1)/2 keys: 10 users need 45, 100 need 4 950 and 1 000 need 499 500. With public-key cryptography each user needs just one key pair, so n users need only 2n keys (20, 200 and 2 000), and the public halves can be published openly. The cost is speed: public-key operations are about a thousand times slower than AES, so real systems use them only to agree on a symmetric session key and to sign."
f = Fig(580, 270)
ax = Axes(f, 56, 20, 330, 206, (0, 100), (0, 5000))
ax.grid(20, 1000)
ax.axes("n users", "keys")
ax.curve(lambda n: n * (n - 1) / 2, 0, 100, color=RED, sw=2.4)
ax.curve(lambda n: 2 * n, 0, 100, color=TEAL, sw=2.4)
f.text(150, 62, "symmetric: n(n-1)/2", size=10.5, color=RED, bold=True)
f.text(300, 190, "public key: 2n", size=10.5, color=TEAL, bold=True)
f.text(410, 36, "n", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(446, 36, "n(n-1)/2", size=10.5, color=RED, bold=True, anchor="start")
f.text(528, 36, "2n", size=10.5, color=TEAL, bold=True, anchor="start")
for i, n in enumerate((10, 100, 1000)):
    f.text(410, 58 + 22 * i, str(n), size=10.5, color=NAVY, anchor="start")
    f.text(446, 58 + 22 * i, format(n * (n - 1) // 2, ","), size=10.5, color=RED, bold=True, anchor="start")
    f.text(528, 58 + 22 * i, format(2 * n, ","), size=10.5, color=TEAL, bold=True, anchor="start")
f.text(410, 140, "AES is about 1000 x faster:", size=10, color=SLATE, anchor="start")
f.text(410, 156, "use RSA or DH only to share", size=10, color=SLATE, anchor="start")
f.text(410, 172, "the session key and to sign", size=10, color=SLATE, anchor="start")
f.text(220, 262, "keys needed for n users", size=10, color=SLATE)
```

```svgfig label="7.5" caption="The textbook RSA example computed with Python's modular arithmetic. Choose primes p = 61 and q = 53, so n = 3233 and phi = 60 x 52 = 3120. Take e = 17; then d = 2753 because 17 x 2753 = 46 801 = 15 x 3120 + 1. Encrypting m = 65 gives c = 65^17 mod 3233 = 2790, and decrypting gives 2790^2753 mod 3233 = 65. A signature runs the keys the other way: signing 65 with the private key gives s = 65^2753 mod 3233 = 588, and anyone can verify it with the public key because 588^17 mod 3233 = 65. Real RSA uses primes of 1 024 bits or more and padding (OAEP, PSS); these numbers are only for understanding."
f = Fig(580, 290)
p, q, e = 61, 53, 17
n, phi = p * q, (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = 65
c = pow(m, e, n)
assert (n, phi, d, c, pow(c, d, n)) == (3233, 3120, 2753, 2790, 65)
s = pow(m, d, n)
v = pow(s, e, n)
assert v == m
steps = [("1  primes", "p = %d, q = %d" % (p, q)), ("2  modulus", "n = p q = %d" % n), ("3  totient", "phi = 60 x 52 = %d" % phi), ("4  public e", "e = %d  (coprime to phi)" % e), ("5  private d", "d = %d : e d = %d = 15 phi + 1" % (d, e * d))]
for i, (a, b) in enumerate(steps):
    y = 10 + i * 30
    f.box(8, y, 90, 24, a, fill=BLUE, stroke=NAVY, size=10, r=3, bold=True, color=NAVY)
    f.box(104, y, 220, 24, b, fill="#ffffff", stroke=NAVY, size=10, r=3, color=NAVY)
f.box(340, 10, 230, 64, "public key (e, n) = (%d, %d)\nprivate key (d, n) = (%d, %d)" % (e, n, d, n), fill=SAND, stroke=AMBER, size=10.5, r=6, bold=True, color=NAVY)
f.text(455, 92, "n is public; p, q, phi and d are secret", size=9.5, color=SLATE)
f.box(8, 176, 270, 50, "encrypt:  c = %d^%d mod %d = %d" % (m, e, n, c), fill=MINT, stroke=TEAL, size=11, r=6, bold=True, color=NAVY)
f.box(8, 232, 270, 50, "decrypt:  %d^%d mod %d = %d" % (c, d, n, pow(c, d, n)), fill=MINT, stroke=TEAL, size=11, r=6, bold=True, color=NAVY)
f.box(300, 176, 270, 50, "sign:  s = %d^%d mod %d = %d" % (m, d, n, s), fill="#fce7f3", stroke="#9d174d", size=11, r=6, bold=True, color=NAVY)
f.box(300, 232, 270, 50, "verify:  %d^%d mod %d = %d  matches" % (s, e, n, v), fill="#fce7f3", stroke="#9d174d", size=11, r=6, bold=True, color=NAVY)
f.arrow([(143, 226), (143, 232)], color=SLATE, sw=1.5)
f.arrow([(435, 226), (435, 232)], color=SLATE, sw=1.5)
f.text(143, 168, "public key encrypts, private key decrypts", size=10, color=NAVY, bold=True)
f.text(435, 168, "private key signs, public key verifies", size=10, color=NAVY, bold=True)
```

```svgfig label="7.6" caption="Diffie-Hellman key exchange with p = 23 and g = 5, computed. Alice picks the secret a = 6 and sends A = 5^6 mod 23 = 8; Bob picks b = 15 and sends B = 5^15 mod 23 = 19. Alice computes 19^6 mod 23 = 2 and Bob computes 8^15 mod 23 = 2, so both hold the same secret 2 although it never crossed the network. The eavesdropper sees only p, g, 8 and 19 and would have to solve a discrete logarithm, which is infeasible for primes of 2 048 bits. Without authentication a man-in-the-middle can run one exchange with each side, which is why TLS signs the key shares with a certificate."
f = Fig(580, 270)
p, g, a, b = 23, 5, 6, 15
A_, B_ = pow(g, a, p), pow(g, b, p)
sa, sb = pow(B_, a, p), pow(A_, b, p)
assert (A_, B_, sa, sb) == (8, 19, 2, 2)
f.box(10, 20, 150, 150, "", fill=BLUE, stroke=NAVY, r=8, sw=1.6)
f.text(85, 38, "Alice", size=12, color=NAVY, bold=True)
f.text(85, 62, "secret a = %d" % a, size=10.5, color=RED, bold=True)
f.text(85, 90, "A = %d^%d mod %d" % (g, a, p), size=10.5, color=SLATE)
f.text(85, 108, "= %d" % A_, size=11, color=NAVY, bold=True)
f.text(85, 140, "key = %d^%d mod %d" % (B_, a, p), size=10.5, color=SLATE)
f.text(85, 158, "= %d" % sa, size=12, color=TEAL, bold=True)
f.box(420, 20, 150, 150, "", fill=MINT, stroke=TEAL, r=8, sw=1.6)
f.text(495, 38, "Bob", size=12, color=TEAL, bold=True)
f.text(495, 62, "secret b = %d" % b, size=10.5, color=RED, bold=True)
f.text(495, 90, "B = %d^%d mod %d" % (g, b, p), size=10.5, color=SLATE)
f.text(495, 108, "= %d" % B_, size=11, color=NAVY, bold=True)
f.text(495, 140, "key = %d^%d mod %d" % (A_, b, p), size=10.5, color=SLATE)
f.text(495, 158, "= %d" % sb, size=12, color=TEAL, bold=True)
f.box(180, 20, 220, 150, "", fill="#fffbeb", stroke=AMBER, r=8, sw=1.4, dash=True)
f.text(290, 38, "public channel", size=11, color=AMBER, bold=True)
f.arrow([(160, 76), (420, 76)], color=NAVY, sw=2, label="A = %d" % A_, lpos=(290, 66), lsize=11)
f.arrow([(420, 116), (160, 116)], color=TEAL, sw=2, label="B = %d" % B_, lpos=(290, 134), lsize=11)
f.text(290, 156, "p = 23, g = 5 are public", size=10, color=SLATE)
f.box(130, 196, 320, 56, "eavesdropper sees p, g, %d and %d only\nshared secret = %d never travels" % (A_, B_, sa), fill="#fee2e2", stroke=RED, size=10.5, r=6, color=RED, bold=True)
```

```svgfig label="7.7" caption="The avalanche effect of a hash, computed with SHA-256. The digest of the text abc begins ba7816bf, and changing one letter to abd gives a completely different digest, a52d159f. Comparing the two 256-bit values bit by bit, 122 bits differ (about half, as expected from a good hash), and 58 of the 64 hexadecimal digits differ. The digest is always 256 bits (64 hex digits) however long the input is, it cannot be reversed, and two inputs with the same digest (a collision) cannot be found in practice. That is why a hash can prove that a file or a message was not altered and can store a password without keeping the password itself."
f = Fig(580, 270)
hl = __import__("hashlib")
h1 = hl.sha256(b"abc").hexdigest()
h2 = hl.sha256(b"abd").hexdigest()
bits = bin(int(h1, 16) ^ int(h2, 16)).count("1")
dig = sum(x != y for x, y in zip(h1, h2))
assert (bits, dig) == (122, 58)
f.text(145, 14, "input 'abc'", size=11, color=NAVY, bold=True, anchor="middle")
f.text(435, 14, "input 'abd' (one letter changed)", size=11, color=RED, bold=True, anchor="middle")
for r in range(4):
    for col in range(16):
        i = r * 16 + col
        x, y = 8 + col * 17.6, 28 + r * 30
        for h, off, base in ((h1, 0, BLUE), (h2, 290, BLUE)):
            diff = h1[i] != h2[i]
            f.box(x + off, y, 16.4, 24, h[i], fill="#fecaca" if (diff and off) else base, stroke=RED if (diff and off) else NAVY, size=10, r=2, sw=1, color=NAVY, bold=bool(diff and off))
f.text(290, 168, "highlighted: %d of 64 hex digits differ, %d of 256 bits differ (%.0f percent)" % (dig, bits, bits / 2.56), size=11, color=RED, bold=True)
props = [("fixed size", "256 bits for any input"), ("one-way", "digest cannot be reversed"), ("collision-resistant", "no two inputs share a digest"), ("avalanche", "1 bit change flips about half")]
for i, (a, b) in enumerate(props):
    f.box(8 + i * 143, 190, 136, 60, a + "\n" + b, fill=MINT, stroke=TEAL, size=9.5, r=5, color=NAVY, bold=True)
f.text(290, 264, "SHA-256 is used for integrity, signatures and password storage (with a salt and a slow function)", size=9.5, color=SLATE)
```

```svgfig label="7.8" caption="A digital signature and the certificate chain that makes its public key trustworthy. Top: the sender hashes the message, encrypts the digest with the sender's private key to make the signature, and sends message and signature. The receiver hashes the received message, decrypts the signature with the sender's public key and compares the two digests: equal digests prove that the message is unchanged (integrity), that it came from the holder of the private key (authentication) and that the sender cannot deny it (non-repudiation). Bottom: a certificate binds a name to a public key and is signed by a certificate authority; the browser trusts a root CA, which signs an intermediate CA, which signs the site's certificate."
f = Fig(580, 306)
f.text(290, 12, "Sign and verify", size=11, color=NAVY, bold=True)
f.box(6, 24, 76, 40, "message", fill=BLUE, stroke=NAVY, size=10, r=4, bold=True, color=NAVY)
f.arrow([(82, 44), (112, 44)], color=SLATE)
f.box(112, 24, 70, 40, "hash\nH", fill=SAND, stroke=AMBER, size=10, r=4, bold=True, color=NAVY)
f.arrow([(182, 44), (212, 44)], color=SLATE)
f.box(212, 24, 108, 40, "encrypt with\nPRIVATE key", fill="#fce7f3", stroke="#9d174d", size=10, r=4, bold=True, color=NAVY)
f.arrow([(320, 44), (350, 44)], color=SLATE)
f.box(350, 24, 90, 40, "signature", fill=MINT, stroke=TEAL, size=10, r=4, bold=True, color=NAVY)
f.text(510, 38, "send message +", size=10, color=SLATE)
f.text(510, 52, "signature", size=10, color=SLATE)
f.box(6, 90, 110, 40, "message received", fill=BLUE, stroke=NAVY, size=10, r=4, bold=True, color=NAVY)
f.arrow([(116, 110), (142, 110)], color=SLATE)
f.box(142, 90, 60, 40, "hash\nH1", fill=SAND, stroke=AMBER, size=10, r=4, bold=True, color=NAVY)
f.box(212, 150, 108, 40, "decrypt with\nPUBLIC key", fill="#fce7f3", stroke="#9d174d", size=10, r=4, bold=True, color=NAVY)
f.box(350, 150, 90, 40, "signature", fill=MINT, stroke=TEAL, size=10, r=4, bold=True, color=NAVY)
f.arrow([(350, 170), (320, 170)], color=SLATE)
f.arrow([(266, 150), (230, 112)], color=SLATE)
f.box(212, 90, 60, 40, "H2", fill=SAND, stroke=AMBER, size=10, r=4, bold=True, color=NAVY)
f.arrow([(202, 110), (212, 110)], color=SLATE)
f.box(300, 90, 140, 40, "H1 = H2 ?  accept\notherwise reject", fill="#ffffff", stroke=RED, size=10, r=4, bold=True, color=RED)
f.line(272, 110, 300, 110, color=SLATE, sw=1.4)
f.text(290, 214, "Certificate chain (X.509)", size=11, color=NAVY, bold=True)
chain = [("Root CA", "self-signed; stored in the browser", NAVY, "#dbeafe"), ("Intermediate CA", "signed by the root", TEAL, MINT), ("www.example.np", "name + public key,\nsigned by the intermediate", AMBER, SAND)]
for i, (a, b, st, fl) in enumerate(chain):
    x = 8 + i * 190
    f.box(x, 226, 176, 56, a + "\n" + b, fill=fl, stroke=st, size=9.5, r=5, bold=True, color=NAVY)
    if i < 2:
        f.arrow([(x + 176, 253), (x + 190, 253)], color=SLATE, sw=1.6)
f.text(290, 298, "the browser checks every signature up to a root it already trusts, and that the name matches", size=9.5, color=SLATE)
```

```svgfig label="7.9" caption="The TLS 1.3 handshake as a ladder, with the delay computed for a round-trip time of 50 ms. After the TCP handshake (1 RTT) the client sends a ClientHello with its Diffie-Hellman key share; the server answers with its key share, its certificate and a Finished message, and the client replies with its own Finished. Both sides now hold the same session keys and application data flows encrypted, so TLS 1.3 adds just 1 RTT. TLS 1.2 needed 2 RTT, so the first request leaves after 50 + 100 = 150 ms instead of 50 + 50 = 100 ms, and the page arrives after 200 ms instead of 150 ms. Because the key comes from Diffie-Hellman, stealing the server's long-term key later does not reveal old sessions (forward secrecy)."
f = Fig(580, 300)
rtt = 50
t13 = rtt + rtt
t12 = rtt + 2 * rtt
f.box(40, 8, 90, 26, "client", fill=BLUE, stroke=NAVY, size=11, bold=True, color=NAVY)
f.box(300, 8, 90, 26, "server", fill=MINT, stroke=TEAL, size=11, bold=True, color=NAVY)
f.line(85, 34, 85, 270, color="#94a3b8", sw=1.2, dash=True)
f.line(345, 34, 345, 270, color="#94a3b8", sw=1.2, dash=True)
msgs = [(54, 1, "SYN", NAVY), (76, -1, "SYN-ACK", TEAL), (98, 1, "ACK + ClientHello (key share)", NAVY), (124, -1, "ServerHello, key share, certificate, Finished", TEAL), (150, 1, "Finished", NAVY), (176, 1, "encrypted HTTP request", RED), (202, -1, "encrypted response", RED)]
for y, dr, t, col in msgs:
    if dr > 0:
        f.arrow([(85, y), (345, y)], color=col, sw=1.6)
    else:
        f.arrow([(345, y), (85, y)], color=col, sw=1.6)
    f.text(215, y - 5, t, size=9.5, color=col, bold=True)
f.line(75, 54, 75, 98, color=AMBER, sw=1.5)
f.text(10, 70, "TCP 1 RTT", size=9.5, color=AMBER, bold=True, anchor="start")
f.line(75, 98, 75, 150, color=RED, sw=1.5)
f.text(10, 126, "TLS 1 RTT", size=9.5, color=RED, bold=True, anchor="start")
f.box(420, 50, 150, 70, "TLS 1.3\nrequest leaves at\n%d + %d = %d ms" % (rtt, rtt, t13), fill=MINT, stroke=TEAL, size=10.5, r=6, bold=True, color=NAVY)
f.box(420, 130, 150, 70, "TLS 1.2\nrequest leaves at\n%d + %d = %d ms" % (rtt, 2 * rtt, t12), fill="#fee2e2", stroke=RED, size=10.5, r=6, bold=True, color=NAVY)
f.text(495, 224, "page arrives: %d ms vs %d ms" % (t13 + rtt, t12 + rtt), size=10.5, color=NAVY, bold=True)
f.text(290, 286, "after Finished both sides use AES-GCM or ChaCha20 with keys derived from the shared secret", size=9.5, color=SLATE)
```

```svgfig label="7.10" caption="IPsec in transport mode and tunnel mode. The original packet is an IP header, a TCP header and the data. In transport mode (host to host) the IP header is kept and the ESP header is inserted after it, so the TCP header and data are encrypted and authenticated, but the addresses stay visible. In tunnel mode (gateway to gateway, the basis of a site-to-site VPN) the whole original packet, including its inner IP header, is encrypted and wrapped in a new IP header addressed from gateway to gateway, so even the real source and destination are hidden. ESP adds a header, a trailer and an integrity check value; AH gives integrity only."
f = Fig(580, 270)
def row(y, title, parts):
    f.text(8, y - 6, title, size=10.5, color=NAVY, bold=True, anchor="start")
    x = 8
    for t, w, fl, st in parts:
        f.box(x, y, w, 30, t, fill=fl, stroke=st, size=9.5, r=2, color=NAVY, bold=True, sw=1.2)
        x += w
    return x
ip, tcp, dat, esp, tr, new = ("IP", 56, BLUE, NAVY), ("TCP", 56, SAND, AMBER), ("data", 150, ROSE, RED), ("ESP", 52, "#e0e7ff", NAVY), ("trailer + ICV", 96, "#e0e7ff", NAVY), ("new IP", 62, "#fde68a", AMBER)
row(30, "original packet", [ip, tcp, dat])
row(100, "transport mode", [ip, esp, tcp, dat, tr])
row(170, "tunnel mode", [new, esp, ("inner IP", 62, BLUE, NAVY), tcp, dat, tr])
f.line(8 + 56 + 52, 140, 8 + 56 + 52 + 56 + 150, 140, color=RED, sw=3)
f.text(8 + 56 + 52 + 103, 154, "encrypted", size=10, color=RED, bold=True)
f.line(8 + 62 + 52, 210, 8 + 62 + 52 + 62 + 56 + 150, 210, color=RED, sw=3)
f.text(8 + 62 + 52 + 134, 224, "encrypted", size=10, color=RED, bold=True)
f.text(8 + 62 + 52 + 134, 246, "real addresses hidden inside", size=10, color=SLATE)
f.text(150, 24, "addresses visible", size=9.5, color=SLATE, anchor="start")
f.text(150, 94, "host to host", size=9.5, color=SLATE, anchor="start")
f.text(150, 164, "gateway to gateway", size=9.5, color=SLATE, anchor="start")
```

```svgfig label="7.11" caption="A packet-filter firewall with a DMZ, and an access control list evaluated by the figure code. The firewall has three interfaces: the Internet, a DMZ holding the public web server 203.0.113.10, and the inside LAN 192.168.1.0/24. The rules are checked in order, the first match decides, and an implicit deny ends the list. Rule 1 permits web traffic (TCP 80) to the web server, rule 2 permits HTTPS (TCP 443) to it, rule 3 lets the LAN open outgoing HTTPS connections, and rule 4 denies everything else. Of the six test packets, two are permitted and four denied: SSH to the web server (no rule permits port 22), a host outside the LAN subnet, an unsolicited packet to a LAN host, and UDP to port 80 (rule 1 permits TCP only)."
f = Fig(580, 330)
ipa = __import__("ipaddress")
rules = [("permit", "tcp", "any", "203.0.113.10/32", 80), ("permit", "tcp", "any", "203.0.113.10/32", 443), ("permit", "tcp", "192.168.1.0/24", "any", 443), ("deny", "any", "any", "any", None)]
def match(pk, r):
    act, pr, s, d, port = r
    src, dst, ppr, pport = pk
    ok = pr in ("any", ppr)
    ok = ok and (s == "any" or ipa.ip_address(src) in ipa.ip_network(s))
    ok = ok and (d == "any" or ipa.ip_address(dst) in ipa.ip_network(d))
    return ok and (port is None or port == pport)
pkts = [("8.8.4.4", "203.0.113.10", "tcp", 443), ("8.8.4.4", "203.0.113.10", "tcp", 22), ("192.168.1.20", "93.184.216.34", "tcp", 443), ("192.168.2.5", "93.184.216.34", "tcp", 443), ("8.8.4.4", "192.168.1.20", "tcp", 80), ("8.8.4.4", "203.0.113.10", "udp", 80)]
res = []
for pk in pkts:
    for i, r in enumerate(rules):
        if match(pk, r):
            res.append((i + 1, r[0])); break
assert [a for _, a in res].count("permit") == 2
f.box(10, 30, 90, 46, "Internet", fill="#dbeafe", stroke=NAVY, size=11, bold=True, color=NAVY, r=23)
f.box(170, 20, 100, 66, "FIREWALL\nrules 1-4", fill="#fee2e2", stroke=RED, size=11, bold=True, color=RED, r=6, sw=2)
f.box(350, 8, 220, 40, "DMZ: web server 203.0.113.10", fill=SAND, stroke=AMBER, size=10.5, bold=True, color=NAVY)
f.box(350, 58, 220, 40, "LAN 192.168.1.0/24: staff, students", fill=MINT, stroke=TEAL, size=10.5, bold=True, color=NAVY)
f.arrow([(100, 53), (170, 53)], color=SLATE, sw=2, both=True)
f.arrow([(270, 36), (350, 30)], color=AMBER, sw=2, both=True)
f.arrow([(270, 70), (350, 78)], color=TEAL, sw=2, both=True)
cx = [6, 26, 84, 196, 316, 366]
for xx, hh in zip(cx, ["#", "action", "source", "destination", "proto", "port"]):
    f.text(xx, 124, hh, size=10, color=NAVY, bold=True, anchor="start")
for i, r in enumerate(rules):
    y = 138 + i * 15
    for xx, val in zip(cx, [str(i + 1), r[0], r[2], r[3], r[1], "any" if r[4] is None else str(r[4])]):
        f.text(xx, y, val, size=10, color=RED if r[0] == "deny" else TEAL, anchor="start", bold=True)
f.text(6, 214, "test packet", size=10, color=NAVY, bold=True, anchor="start")
f.text(396, 214, "rule", size=10, color=NAVY, bold=True, anchor="start")
f.text(450, 214, "result", size=10, color=NAVY, bold=True, anchor="start")
for i, (pk, (rn, act)) in enumerate(zip(pkts, res)):
    y = 230 + i * 15
    f.text(6, y, "%s -> %s  %s/%s" % (pk[0], pk[1], pk[2], pk[3]), size=10, color=SLATE, anchor="start")
    f.text(396, y, "rule %d" % rn, size=10, color=SLATE, anchor="start")
    f.text(450, y, act.upper(), size=10, color=TEAL if act == "permit" else RED, bold=True, anchor="start")
f.text(290, 322, "first matching rule wins; the last rule is the implicit deny all", size=10, color=NAVY, bold=True)
```

```svgfig label="7.12" caption="Two denial-of-service attacks with their numbers. Left: a SYN flood fills the server's backlog of 128 half-open connections. At 500 forged SYN segments per second the queue is full after 128 / 500 = 0.256 s, and honest clients are refused; SYN cookies avoid storing state until the final ACK arrives. Right: DNS amplification. The attacker sends a 64-byte query to an open resolver with the victim's address forged as the source; the 3 000-byte reply goes to the victim, an amplification of 3000 / 64 = 46.9 times (typical figures for a large record). A 1 Mbps stream from one attacker becomes 46.9 Mbps at the victim, and 100 such sources give 4.69 Gbps, enough to fill most links."
f = Fig(580, 280)
cap, rate = 128, 500
f.text(140, 14, "SYN flood: backlog of %d half-open slots" % cap, size=10.5, color=NAVY, bold=True)
for i in range(cap):
    r, c = divmod(i, 16)
    f.box(14 + c * 16.5, 28 + r * 16.5, 14, 14, "", fill="#fecaca", stroke=RED, r=2, sw=1)
f.text(140, 172, "full after %d / %d = %.3f s" % (cap, rate, cap / rate), size=11, color=RED, bold=True)
f.text(140, 192, "honest clients get no free slot", size=10, color=SLATE)
f.text(140, 212, "defence: SYN cookies, backlog limits", size=10, color=TEAL, bold=True)
f.box(300, 30, 70, 40, "attacker", fill="#fee2e2", stroke=RED, size=10, r=4, bold=True, color=RED)
f.box(410, 30, 80, 40, "open DNS\nresolver", fill=SAND, stroke=AMBER, size=10, r=4, bold=True, color=NAVY)
f.box(410, 150, 80, 40, "victim", fill=BLUE, stroke=NAVY, size=10.5, r=4, bold=True, color=NAVY)
q, rep = 64, 3000
f.arrow([(370, 50), (410, 50)], color=RED, sw=2, label="%d B" % q, lpos=(390, 40), lsize=9.5)
f.text(390, 86, "source address", size=9.5, color=SLATE)
f.text(390, 99, "forged = victim", size=9.5, color=SLATE)
f.arrow([(450, 70), (450, 150)], color=RED, sw=4, label="%d B" % rep, lpos=(500, 110), lsize=10.5)
f.text(440, 212, "amplification = %d / %d = %.1f x" % (rep, q, rep / q), size=10.5, color=RED, bold=True)
f.text(440, 232, "1 Mbps becomes %.1f Mbps" % (rep / q), size=10, color=SLATE)
f.text(440, 250, "100 sources: %.2f Gbps" % (100 * rep / q / 1000), size=10, color=SLATE)
```

```svgfig label="7.13" caption="Password strength, computed: the time to try every password at 10 billion guesses per second, which a fast hash such as unsalted SHA-256 allows on a graphics card. A 4-digit PIN (10^4) falls in a microsecond; 8 lowercase letters (26^8 = 2.1 x 10^11) in 21 s; 8 characters from all 95 printable (95^8 = 6.6 x 10^15) in 7.7 days; 10 letters and digits (62^10) in 2.7 years; and 12 mixed characters (95^12 = 5.4 x 10^23) in 1.7 million years. Length helps more than variety. A slow password hash such as bcrypt, scrypt or Argon2 at 10 000 guesses per second makes the 8-character case last about 21 000 years, which is why stored passwords need a salt and a slow function."
f = Fig(580, 300)
cm = __import__("math")
G = 1e10
cases = [("4-digit PIN", 10 ** 4), ("8 lowercase (26)", 26 ** 8), ("8 mixed (95)", 95 ** 8), ("10 letters + digits (62)", 62 ** 10), ("12 mixed (95)", 95 ** 12)]
def human(s):
    if s < 1e-3: return "%.0f microsecond" % (s * 1e6)
    if s < 1: return "%.0f ms" % (s * 1000)
    if s < 120: return "%.0f s" % s
    if s < 7200: return "%.0f min" % (s / 60)
    if s < 172800: return "%.0f hours" % (s / 3600)
    if s < 86400 * 365: return "%.1f days" % (s / 86400)
    y = s / (86400 * 365.25)
    return "%.1f years" % y if y < 1e5 else "%.1f million years" % (y / 1e6)
f.text(290, 14, "time to try all passwords at 10 billion guesses per second (log scale)", size=10.5, color=NAVY, bold=True)
for i, (nm, space) in enumerate(cases):
    s = space / G
    L = max(5, (cm.log10(s) + 6.5) * 13)
    y = 30 + i * 40
    f.text(8, y + 14, nm, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(8, y + 28, "%.1e passwords" % space, size=9.5, color=SLATE, anchor="start", vmid=True)
    f.box(160, y, L, 26, "", fill="#fecaca" if s < 3600 else (SAND if s < 86400 * 365 else MINT), stroke=RED if s < 3600 else (AMBER if s < 86400 * 365 else TEAL), r=3)
    f.text(160 + L + 6, y + 13, human(s), size=10.5, color=RED if s < 3600 else TEAL, bold=True, anchor="start", vmid=True)
slow = 95 ** 8 / 1e4 / (86400 * 365.25)
f.box(8, 238, 564, 52, "slow hash (bcrypt, 10 000 guesses per second): 8 mixed characters last %s years\nadd a per-user salt so one cracked hash does not crack another; add a second factor on top" % format(round(slow, -3), ",.0f"), fill=BLUE, stroke=NAVY, size=10.5, r=6, color=NAVY, bold=True)
```

### 7.6.1 Eight security practices that matter in Nepal

1. **Encrypted web and payments.** ConnectIPS, Fonepay, eSewa and mobile banking apps all run over TLS, so the handshake of Fig. 7.9 happens before any password or amount is sent. The padlock shows that the certificate matched the host name and was signed by a trusted authority (Fig. 7.8). It does not prove that the site is honest, so students should still check the address before typing a password.
2. **Strong, salted passwords.** Portals, e-mail and social accounts are protected first by passwords, and Fig. 7.13 shows that length matters most: twelve mixed characters last millions of years, an eight-letter lowercase word only seconds. A service should store only a salted, slow hash (Fig. 7.7) so a stolen database does not reveal passwords. A password manager lets each account have a different long password.
3. **Multi-factor authentication.** Banks send a one-time code to the registered phone, and a hardware key such as the one in Plate 7.3 is stronger still because its private key never leaves the device. Two different kinds of evidence (something you know and something you have) mean that a stolen password alone is useless. Turn it on for e-mail first, because e-mail can reset every other account.
4. **Safe Wi-Fi at home, hostel and campus.** Use WPA2 or WPA3 with a long passphrase, and enterprise 802.1X in a college so each student has a personal login. Hiding the network name and filtering MAC addresses give almost no protection. Public Wi-Fi without encryption lets anyone nearby sniff traffic, so use only HTTPS sites or a VPN there.
5. **VPNs for remote work.** Nepali software and outsourcing companies serve foreign clients and let staff work from home through VPN tunnels (Fig. 7.10). The tunnel hides the real addresses and encrypts everything between the laptop and the office gateway. This is the same mechanism that joins two branch offices of a bank across the public Internet.
6. **Firewalls and a DMZ.** A college or ISP puts public servers such as the website and mail gateway in a DMZ and the student records on the inside LAN, with rules like those in Fig. 7.11. The first matching rule decides and everything not permitted is denied. If the web server is hacked, the attacker still faces the firewall before reaching internal data.
7. **Digital signatures and certificates.** The Electronic Transactions Act and the Controller of Certification allow licensed authorities to issue digital signature certificates, which are used on electronic tenders and filings. A signature (Fig. 7.8) proves who signed and that the document was not changed, so it can replace a handwritten signature. The certificate chain tells the verifier that the public key really belongs to the named person.
8. **Defence against attacks and fraud.** A public portal on result day may face traffic floods, and SYN cookies and rate limits keep it alive (Fig. 7.12). Phishing messages that copy a bank or a telecom prize offer are the most common attack on ordinary users, so never type a password after clicking a link in a message. Regular offline backups are the best answer to ransomware, because the data can be restored without paying.

## Formula and fact sheet

- RSA: n = pq, φ = (p − 1)(q − 1), e d ≡ 1 (mod φ), c = mᵉ mod n, m = cᵈ mod n.
- Diffie–Hellman: shared = gᵃᵇ mod p. Symmetric keys for n people: n(n − 1)/2.
- AES block 128 bits, keys 128/192/256. SHA-256 digest 256 bits. TLS port 443, SSH 22, IPsec ESP protocol 50, AH 51.
- Firewall: ordered rules, first match, implicit deny. Stateful tracks connections.
- Signature = private-key operation on the hash; verification with the public key.

## Chapter summary

- Security aims at confidentiality, integrity, availability, authentication and non-repudiation; attacks are passive or active.
- Symmetric ciphers (AES) are fast but need key distribution; public-key systems (RSA, Diffie–Hellman) solve distribution and give signatures; hashes provide integrity.
- Certificates bind keys to names through CAs; TLS combines all of them to secure the web; IPsec and WPA2 do it at the IP and Wi-Fi layers.
- Firewalls filter by policy, IDS/IPS detect and block attacks, and good practice (patching, least privilege, segmentation, MFA) matters more than any single device.

## Practice

1. Explain confidentiality, integrity and availability with an example attack on each.
2. Differentiate symmetric and public-key cryptography. How many keys do 10 people need for symmetric secrecy?
3. In RSA, p = 61, q = 53, e = 17. Find n, φ, d, and encrypt 65.
4. Do a Diffie–Hellman exchange with p = 23, g = 5, a = 6, b = 15.
5. What is a hash function? List three uses.
6. How does a digital signature give non-repudiation?
7. Describe the main steps of the TLS handshake and what the padlock does and does not mean.
8. Compare packet-filter, stateful and proxy firewalls.
9. What is a DMZ?
10. Compare IDS and IPS and signature-based and anomaly-based detection.
11. Why are SYN floods a threat to availability and how can they be mitigated?

::: note Answers and worked solutions
**1.** Confidentiality: eavesdropping on unencrypted Wi-Fi. Integrity: a man-in-the-middle changing a bank transfer amount. Availability: a DDoS flood that takes a site down.
**2.** Symmetric: one shared secret key, fast, key distribution is hard. Public key: key pair, slow, solves distribution and enables signatures. 10 × 9 / 2 = 45 keys.
**3.** n = 3233, φ = 3120, d = 2753, c = 65¹⁷ mod 3233 = 2790.
**4.** A = 5⁶ mod 23 = 8, B = 5¹⁵ mod 23 = 19, shared = 19⁶ mod 23 = 2.
**5.** A function that maps data to a fixed-length digest, one-way and collision resistant. Uses: password storage (with salt), integrity checks of downloads, digital signatures, HMAC.
**6.** Only the holder of the private key can produce a signature that the public key verifies, so the signer cannot plausibly deny it (assuming the key was not stolen).
**7.** ClientHello, ServerHello with certificate and key share, key derivation, Finished, encrypted data. The padlock means the connection is encrypted and the certificate matches the domain; it does not prove the site is trustworthy or safe.
**8.** Packet filter: stateless rules on addresses and ports, fast. Stateful: tracks connections and allows replies. Proxy: terminates and inspects the application content, slowest but deepest.
**9.** A separate network segment for public servers, isolated from the internal network so a compromise stays contained.
**10.** IDS alerts only; IPS blocks in line. Signature-based finds known attacks quickly but misses new ones; anomaly-based finds unusual behaviour at the cost of false alarms.
**11.** They fill the server's half-open connection table so real clients cannot connect; mitigation: SYN cookies, shorter timeouts, rate limiting and upstream scrubbing.
:::

## Model answers for Unit 7

**Q1. Explain symmetric and public-key cryptography, with the RSA algorithm and a worked example. (10 marks)**

**Introduction.** Cryptography turns readable plaintext into unreadable ciphertext with an algorithm and a key; by Kerckhoffs' principle the algorithm is public and only the key is secret. The two families are symmetric-key and public-key cryptography, and real systems use both.

**Symmetric-key cryptography.** One shared secret key encrypts and decrypts. DES used a 56-bit key and was broken in 1998 by a machine built for the purpose (Plate 7.2); its successor AES uses 128-, 192- or 256-bit keys on 128-bit blocks with 10, 12 or 14 rounds, and a mode of operation (CBC, CTR or GCM) lets it encrypt long messages without leaking patterns. It is fast, but n users need n(n - 1)/2 keys, which is 45 for 10 users and 499 500 for 1 000 (Fig. 7.4), and the key must first be delivered secretly.

**Public-key cryptography.** Each user has a public key, which is published, and a private key, which is kept secret. What one key encrypts only the other can decrypt, so n users need only 2n keys and no secret has to be shared beforehand. It is about a thousand times slower than AES, so it is used to exchange a session key and to sign.

**RSA.** Choose primes p and q and compute n = p q and phi = (p - 1)(q - 1). Choose e coprime to phi and find d with e d = 1 (mod phi). The public key is (e, n) and the private key is (d, n). Encryption is c = m^e mod n and decryption is m = c^d mod n. Its security rests on the difficulty of factorising n.

**Example (Fig. 7.5).** With p = 61 and q = 53: n = 3233 and phi = 3120. Take e = 17; then d = 2753 because 17 x 2753 = 46 801 = 15 x 3120 + 1. For m = 65, c = 65^17 mod 3233 = 2790, and 2790^2753 mod 3233 = 65 again. Signing is the reverse: s = 65^2753 mod 3233 = 588, which anyone checks with e since 588^17 mod 3233 = 65.

| Feature | Symmetric (AES) | Public key (RSA) |
|---|---|---|
| Keys | one shared secret | public and private pair |
| Speed | very fast | about 1 000 times slower |
| Keys for n users | n(n - 1)/2 | 2n |
| Main use | bulk data encryption | key exchange, signatures |

**Conclusion.** Practical protocols such as TLS combine the two: public-key methods agree a session key and authenticate the server, and AES encrypts the data.

**Q2. Explain how HTTPS works: the TLS handshake, certificates and the guarantees it gives. (10 marks)**

**Introduction.** HTTPS is HTTP carried inside a Transport Layer Security (TLS) connection on TCP port 443. TLS sits between TCP and the application and gives encryption (confidentiality), integrity and authentication of the server, and optionally of the client.

**Handshake (TLS 1.3, Fig. 7.9).** After the TCP handshake the client sends a ClientHello listing the cipher suites it supports and a Diffie-Hellman key share. The server replies with the chosen suite, its own key share, its certificate and a signature proving it owns the private key, then a Finished message. Both sides derive the same session keys from the shared secret, the client sends Finished, and application data then flows encrypted with AES-GCM or ChaCha20. TLS 1.3 needs only one round trip; with RTT = 50 ms the first request leaves after 100 ms, whereas TLS 1.2 needed 150 ms.

**Certificates.** A certificate is an X.509 document that binds a name to a public key and is signed by a certificate authority (CA). The browser holds a list of trusted root CAs and checks the chain from the site's certificate through an intermediate CA to a root, as well as the validity dates and that the name matches (Fig. 7.8). This stops a man-in-the-middle from posing as the server.

**Guarantees.** Confidentiality: data is encrypted with the session key. Integrity: every record carries an authentication tag, so any change is detected. Authentication: the certificate and the signature prove the server's identity. Forward secrecy: because the key comes from Diffie-Hellman, stealing the server's long-term key later does not decrypt recorded sessions.

| Layer | Protocol | Port | Protects |
|---|---|---|---|
| Application | HTTP | 80 | nothing (plain text) |
| Application + TLS | HTTPS | 443 | confidentiality, integrity, server identity |

**Limits.** The padlock means only that the certificate matched the name and was signed by a trusted CA; a phishing site can have a valid certificate for its own name. Users must still check the address.

**Conclusion.** HTTPS combines public-key cryptography for the handshake, symmetric encryption for the data and certificates for trust, which is why ConnectIPS, Fonepay and internet banking rely on it.

**Q3. Describe the types of firewall, the DMZ and an access control list. (10 marks)**

**Introduction.** A firewall enforces a security policy between networks of different trust, usually the Internet and a private LAN. It may be a hardware appliance (Plate 7.3) or software on a router or host.

**Types.**

| Type | How it works | Strength | Weakness |
|---|---|---|---|
| Packet filter (stateless) | checks IP addresses, protocol and ports of each packet against an ordered rule list | fast and simple | cannot tell a reply from an attack; no content check |
| Stateful inspection | keeps a table of connections; replies to connections opened inside are allowed automatically | blocks unsolicited inbound traffic | does not read the application data |
| Application gateway (proxy) | ends the connection and inspects HTTP, SMTP and so on; can cache and filter URLs | deep content control | slower, one proxy per protocol |
| Next-generation firewall | adds application identification, user identity and intrusion prevention | richest policy | costly and complex |

**ACL.** An access control list is an ordered list of permit and deny rules. The first matching rule decides and an implicit deny ends the list. In Fig. 7.11, rule 1 permits TCP 80 to the web server 203.0.113.10, rule 2 permits TCP 443, rule 3 lets the LAN 192.168.1.0/24 open outgoing HTTPS, and rule 4 denies everything. Of six test packets, HTTPS to the web server and the LAN's own HTTPS are permitted, while SSH to the web server, a host outside the /24, an unsolicited packet to a LAN host and UDP to port 80 are all denied by the last rule. Rule order matters: a broad deny placed first would block everything.

**DMZ.** A demilitarised zone is a separate segment for public servers (web, mail, DNS). The firewall allows the Internet to reach the DMZ only on the needed ports and allows almost nothing from the DMZ to the LAN, so a hacked web server cannot reach student records.

**Related devices.** An intrusion detection system (IDS) watches traffic and raises alarms; an intrusion prevention system (IPS) also blocks. A VPN gateway often runs on the same appliance.

**Conclusion.** Layering a stateful firewall, a DMZ, an IDS or IPS and patched hosts gives defence in depth: no single failure exposes the internal network.

**Q4. Explain the CIA triad and the main network attacks with their defences. (5 marks)**

The three goals of security are **confidentiality** (only authorised parties can read the data), **integrity** (the data is not altered unnoticed) and **availability** (the service works when needed). Further goals are authentication (who are you?), authorisation (what may you do?) and non-repudiation (you cannot deny sending). Attacks are **passive** if they only observe, and **active** if they modify or inject traffic (Fig. 7.1).

| Attack | Goal attacked | Defence |
|---|---|---|
| Eavesdropping, sniffing | confidentiality | encryption (TLS, WPA2) |
| Spoofing | authentication | ingress filtering, authentication, SPF |
| Man-in-the-middle | confidentiality and integrity | TLS with certificate checks |
| Replay | integrity | nonces, timestamps, sequence numbers |
| DoS, DDoS, SYN flood | availability | rate limits, SYN cookies, scrubbing |
| Phishing | authentication | training, multi-factor authentication |

Passive attacks are hard to detect, so they are defeated by encryption; active attacks are detected by integrity checks such as hashes and MACs. For example, a DNS amplification attack turns a 64-byte query into a 3 000-byte reply sent to the victim, an amplification of 46.9 times (Fig. 7.12).

**Q5. Using p = 61, q = 53 and e = 17, find the RSA keys and encrypt the message 65. (5 marks)**

First n = p x q = 61 x 53 = 3233, and phi = (p - 1)(q - 1) = 60 x 52 = 3120. The public exponent e = 17 has no common factor with 3120, so it is valid. The private exponent d must satisfy e x d = 1 (mod 3120). Trying d = 2753 gives 17 x 2753 = 46 801, and 46 801 = 15 x 3120 + 1, so the remainder is 1 and d = 2753.

The public key is (e, n) = (17, 3233) and the private key is (d, n) = (2753, 3233).

Encryption of m = 65: c = 65^17 mod 3233. Working with repeated squaring and reducing at every step gives c = 2790. Decryption: m = 2790^2753 mod 3233 = 65, which is the original message (Fig. 7.5).

For a signature the keys are used the other way round: s = 65^2753 mod 3233 = 588. The receiver computes 588^17 mod 3233 = 65 and compares it with the message: they match, so the signature is genuine. These small primes are only for practice; real keys use primes of 1 024 bits or more, a 2 048-bit modulus and padding schemes such as OAEP and PSS, because "textbook" RSA without padding is not secure.

**Q6. Explain the Diffie-Hellman key exchange with an example. (5 marks)**

Diffie-Hellman lets two parties create a shared secret over a public channel without ever sending it. They first agree on a public prime p and a base g. Alice chooses a secret a and sends A = g^a mod p; Bob chooses a secret b and sends B = g^b mod p. Alice computes B^a mod p and Bob computes A^b mod p, and both equal g^(ab) mod p.

With p = 23 and g = 5 (Fig. 7.6): Alice picks a = 6 and sends A = 5^6 mod 23 = 8. Bob picks b = 15 and sends B = 5^15 mod 23 = 19. Alice computes 19^6 mod 23 = 2, and Bob computes 8^15 mod 23 = 2. The shared secret is 2 and it never crossed the network.

An eavesdropper sees p, g, 8 and 19. To find the secret she would have to solve the discrete logarithm problem, which is infeasible for primes of 2 048 bits. The weakness is that the exchange is not authenticated: a man-in-the-middle can perform one exchange with Alice and another with Bob and read everything. TLS therefore signs the key shares with the server's certificate. Because new random a and b are used for every session, the method also gives forward secrecy.

**Q7. What is a cryptographic hash? Explain digital signatures and certificates. (5 marks)**

A **cryptographic hash** maps any input to a fixed-size digest (SHA-256 gives 256 bits). It is one-way (the input cannot be recovered), collision-resistant (no two inputs with the same digest can be found) and shows the avalanche effect: changing abc to abd changes 122 of the 256 bits and 58 of the 64 hexadecimal digits (Fig. 7.7). Hashes check file integrity and store passwords, with a per-user salt and a slow function such as bcrypt or Argon2. MD5 and SHA-1 are broken and should not be used.

A **digital signature** is the hash of a message encrypted with the sender's private key. The receiver hashes the message, decrypts the signature with the sender's public key and compares the two digests (Fig. 7.8). A match proves integrity, authentication of the sender and non-repudiation.

A **certificate** answers the question of whose public key it is. An X.509 certificate binds a name to a public key and is signed by a certificate authority. The browser trusts a few root CAs, which sign intermediate CAs, which sign site certificates, and it verifies the whole chain. In Nepal the Controller of Certification licenses certifying authorities under the Electronic Transactions Act.

**Q8. Compare IPsec transport mode and tunnel mode and explain a VPN. (5 marks)**

IPsec secures traffic at the IP layer. Its **AH** header gives integrity and authentication only, while **ESP** gives encryption plus integrity. Keys are agreed by the IKE protocol.

In **transport mode** the original IP header is kept and the ESP header is inserted after it, so only the payload (the TCP segment and data) is protected. The addresses stay visible, and the mode is used between two hosts. In **tunnel mode** the whole original packet, including its IP header, is encrypted and wrapped in a new IP packet addressed from one gateway to the other, so the real source and destination are hidden (Fig. 7.10). It is the mode used by gateways.

| Feature | Transport mode | Tunnel mode |
|---|---|---|
| Protected part | payload only | whole original packet |
| IP header | original kept | new outer header added |
| Typical use | host to host | gateway to gateway (site-to-site VPN) |
| Overhead | smaller | larger |

A **VPN** (virtual private network) uses such a tunnel to give a remote user or a branch office a private, encrypted connection across the public Internet, as if it were on the office LAN. Remote-access VPNs may use IPsec, a TLS-based client or WireGuard.

**Q9. How are Wi-Fi networks and passwords protected? (5 marks)**

**Wireless security.** WEP used the RC4 cipher badly and is broken in minutes. WPA2 uses AES-CCMP; in personal mode all users share one passphrase, and in enterprise mode 802.1X and EAP give each user a login checked by a RADIUS server, so a leaver can be removed without changing everyone's key. WPA3 adds SAE, a password-based key exchange that resists offline guessing, and protected management frames. Hiding the SSID and filtering MAC addresses are not real security because both can be bypassed in seconds.

**Password defence.** At 10 billion guesses per second, a 4-digit PIN falls in a microsecond, 8 lowercase letters in 21 s, 8 characters from all 95 printable symbols in 7.7 days, and 12 mixed characters need 1.7 million years (Fig. 7.13). Length therefore matters more than variety. A service should store a salted hash made with a slow function, which turns the 8-character case into about 21 000 years at 10 000 guesses per second. Users should use a different long password for every account, a password manager, and multi-factor authentication such as a phone code or a hardware key.

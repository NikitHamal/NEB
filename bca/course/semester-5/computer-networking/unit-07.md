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

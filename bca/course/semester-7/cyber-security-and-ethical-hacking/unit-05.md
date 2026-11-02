---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 5
title: Network Defence Architecture, DNSSEC, Wi-Fi Keys, Rate Limiting and ACLs
hours: 6
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 5
---

Network defence is the art of making the paths that traffic may take as narrow as the business allows, and making the paths that remain verifiable. This unit covers four building blocks that every security engineer should understand mathematically as well as operationally: the integrity of the naming system (DNSSEC) and the birthday bound that decides how long a hash must be; the key hierarchy that protects a Wi-Fi network; the token bucket that limits request rates; and the ordered rule lists of firewalls.

::: key What this unit gives you
- Defence architecture: segmentation, DMZ, default deny and zero trust at the network layer.
- DNSSEC's chain of trust and the birthday bound for collisions.
- WPA2 and WPA3: PMK, PTK, handshakes and the roles of the derived keys.
- Token-bucket rate limiting and first-match ACL evaluation, including rule shadowing.
:::

## 5.1 Architecture of a defended network

A defended network is divided into **zones** by trust and function: an *external* zone (the internet), a **DMZ** (demilitarised zone) holding public-facing servers, an *internal* zone for users and an isolated *management* zone for administration; databases usually sit in a further restricted zone. Traffic between zones passes a **firewall** or equivalent control that applies the principle of **default deny**: anything not explicitly permitted is dropped. **Network segmentation** limits the blast radius of a compromise (a breached web server cannot talk straight to the finance database) and **microsegmentation** extends the same idea to individual workloads. Complementary controls are intrusion detection (Unit 6), centralised logging, secure remote access (VPN or zero-trust access proxy with MFA) and patching of every exposed system.

## 5.2 DNS and DNSSEC

The Domain Name System translates names to addresses but was designed without authentication: a resolver could not tell whether an answer was genuine. **DNSSEC** adds digital signatures to DNS data so that a validating resolver can verify *origin authenticity* and *integrity* of answers. It does **not** encrypt queries (that is DNS over TLS or HTTPS) and does not protect against a compromised authoritative server.

The mechanism is a **chain of trust**:

1. A zone signs each set of records with a **zone signing key (ZSK)**, publishing the signature as an **RRSIG** record and the public key as a **DNSKEY** record.
2. A **key signing key (KSK)** signs the DNSKEY set. A hash of the KSK is published in a **DS** (delegation signer) record in the *parent* zone, which is itself signed.
3. The resolver starts from a configured trust anchor (the root zone's key) and follows DS and DNSKEY records down the hierarchy to the name being queried. A failed check yields a validation failure instead of an answer.
4. **NSEC/NSEC3** records give authenticated proof that a name does *not* exist.

DNSSEC signatures rely on cryptographic hashes, so output length matters. The **birthday bound** says that in a space of *N* equally likely values, a collision among random samples becomes more likely than not after about √(2 ln 2 · N) ≈ 1.1774 √N samples, far fewer than N. For a hash with *b*-bit output, finding *some* collision therefore costs about 2^(b/2) work, not 2^b.

```python
import math
for b in (16, 24, 32):
    n = math.ceil(math.sqrt(2 * math.log(2) * 2 ** b))
    print(f"{b}-bit space: 50% collision after about {n} samples")
for name, bits in (("MD5", 128), ("SHA-1", 160), ("SHA-256", 256)):
    print(f"{name} ({bits}-bit digest): collision work about 2^{bits // 2}")
```
```output
16-bit space: 50% collision after about 302 samples
24-bit space: 50% collision after about 4823 samples
32-bit space: 50% collision after about 77163 samples
MD5 (128-bit digest): collision work about 2^64
SHA-1 (160-bit digest): collision work about 2^80
SHA-256 (256-bit digest): collision work about 2^128
```
With a 16-bit space, a collision is as likely as not after only 302 samples, and with 32 bits after 77163, which is why short identifiers must not be treated as unique and why small random fields (such as the 16-bit DNS query identifier) cannot be the only protection of a protocol. MD5 and SHA-1 have 2^64 and 2^80 generic collision work respectively, which, together with practical cryptanalytic attacks, is why they are retired for signatures. SHA-256's 2^128 is comfortably out of reach. The checker confirmed the closed form against an exact product computation for the 16-bit and 24-bit cases (within one sample).

## 5.3 Wi-Fi security: WPA2 and WPA3

Wireless networks broadcast, so link-layer encryption and authentication are essential. **WPA2-Personal** derives a **pairwise master key (PMK)** from the passphrase and the network name (SSID) with PBKDF2-HMAC-SHA1 using 4,096 iterations and a 256-bit output. In the **four-way handshake** the access point and the client exchange random nonces, each derive a **pairwise transient key (PTK)** from the PMK, both MAC addresses and both nonces, and prove they hold the same PMK with a message integrity code, without ever transmitting the key. For AES-CCMP the 384-bit PTK is split into three 128-bit keys:

- **KCK** (key confirmation key): authenticates the handshake messages;
- **KEK** (key encryption key): protects the group key delivered to the client;
- **TK** (temporal key): encrypts and authenticates the user's data frames.

A separate **group temporal key (GTK)** protects broadcast and multicast frames.

```python
import hashlib
pmk = hashlib.pbkdf2_hmac("sha1", b"password", b"IEEE", 4096, 32)
print(f"PMK (first 16 hex): {pmk.hex()[:16]}")
kck, kek, tk = 128, 128, 128
print(f"PTK (CCMP) = {kck + kek + tk} bits = KCK {kck} + KEK {kek} + TK {tk}")
```
```output
PMK (first 16 hex): f42c6fc52df0ebef
PTK (CCMP) = 384 bits = KCK 128 + KEK 128 + TK 128
```
The first line reproduces the published IEEE 802.11i test vector for the passphrase "password" and SSID "IEEE", which is how implementations are validated. Because the PMK depends only on the passphrase and SSID, a *weak passphrase* on WPA2-Personal weakens everything, and anyone who learns the passphrase can derive the keys of sessions that they have recorded. **WPA3-Personal** replaces this with **SAE** (Simultaneous Authentication of Equals, a password-authenticated key exchange): each session gets a fresh, independent PMK, so recorded traffic stays protected even if the passphrase later leaks (forward secrecy), and offline guessing from a captured handshake is no longer possible; protected management frames are mandatory. WPA2/WPA3-Enterprise instead uses 802.1X with an authentication server so that every user has individual credentials.

## 5.4 Rate limiting with a token bucket

Rate limiting protects availability (Unit 1's "D" in STRIDE) by capping how fast clients may use a service. The **token bucket** algorithm holds up to *B* tokens (the burst capacity) and adds tokens at *r* per second; each request spends one token and is refused if none remain. Over any interval of length *t*, at most **B + r·t** requests can be accepted: a bounded burst plus a bounded sustained rate. The implementation below uses integer *milli-tokens* and millisecond time to avoid floating-point error: capacity 10 tokens, refill 5 tokens per second.

## 5.5 First-match ACLs and shadowing

A **packet-filter ACL** is an ordered list of rules; the first rule that matches decides, and a final implicit (or explicit) deny catches the rest. Order therefore matters. A rule is **shadowed** when an *earlier* rule already matches every packet it would match, so it can never fire; shadowed rules are a common configuration error because they give the author a false sense that a restriction exists.

```python
CAP, RATE, COST = 10000, 5, 1000        # milli-tokens: bucket size, refill per ms (5 tokens/s), cost of a request

def run(arrivals):
    tokens, last, ok = CAP, 0, 0
    for t in arrivals:
        tokens = min(CAP, tokens + RATE * (t - last))
        last = t
        if tokens >= COST:
            tokens -= COST
            ok += 1
    return ok

burst = run([0] * 15)
print(f"burst of 15 at t=0: accepted {burst}, rejected {15 - burst}")
steady = run([i * 10 for i in range(1000)])
print(f"10 s of 100 req/s: accepted {steady} of 1000 (bound 60)")
```
```output
burst of 15 at t=0: accepted 10, rejected 5
10 s of 100 req/s: accepted 59 of 1000 (bound 60)
```
A burst of 15 simultaneous requests is cut to the bucket size of 10. Offered 100 requests per second for ten seconds, the limiter accepts only 59 of 1,000, just under the theoretical bound of 10 + 5 × 10 = 60 (the last arrival is at 9.99 s, so 49.95 tokens have been added, not 50). The checker verified this with an independent *arrival-curve* formulation: accept request *i* only if the cumulative accepted count would stay at or below B + r·tᵢ.

The next program evaluates four packets against a three-rule ACL (permit HTTPS to the web subnet, permit SSH to it from the management subnet, deny everything else) and then detects shadowed rules in a second list. Addresses from the documentation range 203.0.113.0/24 stand in for outside hosts.

```python
import ipaddress
rules = [("permit", "tcp", "any", "10.0.1.0/24", (443, 443)),
         ("permit", "tcp", "10.0.9.0/24", "10.0.1.0/24", (22, 22)),
         ("deny", "ip", "any", "any", (0, 65535))]

def net(x):
    return ipaddress.ip_network("0.0.0.0/0" if x == "any" else x)

def decide(proto, src, dst, port):
    for n, (act, p, s, d, (lo, hi)) in enumerate(rules, 1):
        if (p in ("ip", proto) and ipaddress.ip_address(src) in net(s)
                and ipaddress.ip_address(dst) in net(d) and lo <= port <= hi):
            return act, n
    return "deny", 0

packets = [("tcp", "203.0.113.5", "10.0.1.10", 443), ("tcp", "203.0.113.5", "10.0.1.10", 22),
           ("tcp", "10.0.9.4", "10.0.1.10", 22), ("udp", "10.0.9.4", "10.0.1.10", 53)]
for proto, src, dst, port in packets:
    act, n = decide(proto, src, dst, port)
    print(f"{proto} {src} -> {dst}:{port} = {act} (rule {n})")

def covers(a, b):
    return (a[1] in ("ip", b[1]) and net(b[2]).subnet_of(net(a[2])) and net(b[3]).subnet_of(net(a[3]))
            and a[4][0] <= b[4][0] and b[4][1] <= a[4][1])

rules2 = [("permit", "tcp", "any", "any", (22, 22)),
          ("deny", "tcp", "10.0.5.0/24", "any", (22, 22)),
          ("permit", "tcp", "any", "any", (80, 80))]
shadowed = [j for j in range(1, len(rules2) + 1) if any(covers(rules2[i], rules2[j - 1]) for i in range(j - 1))]
print(f"shadowed rules: {shadowed}")
```
```output
tcp 203.0.113.5 -> 10.0.1.10:443 = permit (rule 1)
tcp 203.0.113.5 -> 10.0.1.10:22 = deny (rule 3)
tcp 10.0.9.4 -> 10.0.1.10:22 = permit (rule 2)
udp 10.0.9.4 -> 10.0.1.10:53 = deny (rule 3)
shadowed rules: [2]
```
HTTPS from outside matches rule 1. SSH from the outside address matches nothing earlier and falls to the deny in rule 3. SSH from the management subnet matches rule 2, and DNS-style UDP traffic is denied by rule 3. In the second list, rule 2 intends to block one subnet from SSH but rule 1 already permits SSH from *anywhere*, so the intended block never takes effect: the audit reports rule 2 as shadowed. Rule 3 is not shadowed because rule 1 covers only port 22.

## 5.6 Operating the controls

Review firewall rules at least twice a year and remove unused ones; require a ticket and an owner for each rule; log denies and sample permits; test changes in a lab or with a "simulate" mode; and rate-limit at several layers (network edge, load balancer, application, per account). Authentication endpoints deserve their own limits (Unit 3).

## 5.7 Summary and exercises

Network defence uses zones, default deny and segmentation; DNSSEC provides signed answers through a chain of trust; the birthday bound sets hash lengths at twice the desired collision resistance; WPA2 derives PMK and PTK and WPA3 adds SAE with forward secrecy; token buckets bound bursts and sustained rates; and first-match ACLs need audit for shadowing.

1. Explain the chain of trust from the root to a domain's A record in DNSSEC, naming the record types involved.
2. How many samples give a 50% collision chance in a 20-bit space, by the closed form?
3. Why does WPA3's SAE give forward secrecy while WPA2-Personal does not?
4. For a bucket with B = 20 and r = 10 per second, what is the maximum number of requests accepted in 5 seconds?
5. Reorder the second ACL in this unit so that the deny for 10.0.5.0/24 takes effect. Verify it with the program.
6. Why is default deny a better foundation than a list of blocked items?

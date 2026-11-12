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

## 5.7 Seeing the ideas: network hardware, zones, the DNSSEC chain, Wi-Fi keys and the token bucket

Plate 5.1 shows the hardware that implements the zones of section 5.1: switches that carry traffic, a firewall that filters it and an access point that extends the network over radio.

```photogrid label="5.1" cols="3" ratio="1.1" caption="Hardware of a defended network. (a) Managed rack-mount Ethernet switches wired to patch panels: VLANs on such switches separate the zones. (b) A rack-mount firewall appliance, the policy enforcement point between zones. (c) A ceiling access point: a wireless entry point that must use WPA2 or WPA3 with strong keys."
@ photo id="bca401/switch" cap="Managed switches and patch panels"
fit 1.1
focus 0.5 0.5
@ photo id="bca401/pix" cap="Firewall appliance"
fit 1.1
focus 0.5 0.55
@ photo id="bca401/ap" cap="Wireless access point"
fit 1.1
focus 0.5 0.4
```

```svgfig label="5.1" caption="A defended network in zones. The firewall allows the internet to reach only the DMZ servers; the internal zone is never reachable directly from outside, and the database sits in its own zone that only the application servers may query."
f = Fig(580, 214)
f.box(6, 70, 90, 60, "Internet\n(untrusted)", fill=ROSE, stroke=RED, bold=True, size=10.5)
f.box(120, 82, 54, 36, "Edge\nfirewall", fill=SAND, stroke=AMBER, bold=True, size=9)
f.box(200, 14, 160, 80, "DMZ\nweb server, mail relay,\nDNS resolver", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(200, 116, 160, 80, "Internal zone\nstaff PCs, printers,\nWi-Fi (WPA3)", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(414, 70, 160, 60, "Data zone\ndatabase, backups,\nlogging server", fill="#e2e8f0", stroke=SLATE, size=10, bold=True)
f.arrow([(96, 100), (120, 100)], color=RED)
f.arrow([(174, 92), (200, 60)], color=NAVY, label="443 only", lpos=(150, 58))
f.arrow([(174, 108), (200, 150)], color=TEAL, dash=True)
f.arrow([(360, 60), (414, 90)], color=NAVY, label="DB port", lpos=(392, 66))
f.arrow([(360, 150), (414, 112)], color=TEAL, dash=True)
f.text(290, 208, "Default deny between zones; log every denied connection", size=10, color=NAVY, bold=True)
```

```svgfig label="5.2" caption="The DNSSEC chain of trust. Each parent zone signs a DS record that holds a hash of the child's key-signing key, so a resolver that trusts the root can verify the .np zone and then the zone of a domain below it."
f = Fig(580, 212)
for i, (t, s) in enumerate([("Root zone (.)", "trust anchor in the resolver\nDNSKEY signed by root KSK"), (".np zone", "DS record for .np in root\nRRSIGs by .np ZSK"), ("example.com.np", "DS record for the zone in .np\nA record + RRSIG")]):
    x = 8 + i * 192
    f.box(x, 14, 180, 34, t, fill=BLUE if i < 2 else MINT, stroke=NAVY if i < 2 else TEAL, bold=True, size=11)
    f.box(x, 54, 180, 56, s, fill="#f8fafc", stroke=SLATE, size=9.5)
    if i < 2:
        f.arrow([(x + 180, 76), (x + 192, 76)], color=RED)
f.box(8, 122, 564, 42, "Resolver check: RRSIG on the A record verifies with the zone ZSK > ZSK verified by the KSK\n> KSK hash matches the parent DS > ... and so on up to the trust anchor", fill=MINT, stroke=TEAL, size=9.5)
f.box(8, 170, 564, 40, "Any broken link (bad signature, missing DS, expired RRSIG) makes the answer BOGUS:\nthe resolver returns an error instead of a forged address", fill=ROSE, stroke=RED, size=9.5)
```

```svgfig label="5.3" caption="The WPA2-Personal key hierarchy. The passphrase and SSID are stretched into the 256-bit PMK by PBKDF2 (4,096 iterations). The four-way handshake mixes in two random nonces and both MAC addresses to produce a fresh PTK for each session, which splits into KCK, KEK and TK."
f = Fig(580, 214)
f.box(6, 10, 120, 46, "Passphrase\n+ SSID", fill=SAND, stroke=AMBER, bold=True, size=10.5)
f.box(150, 10, 150, 46, "PBKDF2-HMAC-SHA1\n4096 iterations", fill=BLUE, stroke=NAVY, bold=True, size=10)
f.box(324, 10, 110, 46, "PMK\n256 bits", fill=MINT, stroke=TEAL, bold=True, size=10.5)
f.arrow([(126, 33), (150, 33)]); f.arrow([(300, 33), (324, 33)])
f.box(6, 84, 190, 46, "Two nonces (ANonce, SNonce)\n+ two MAC addresses", fill=SAND, stroke=AMBER, size=10)
f.box(230, 84, 150, 46, "Four-way handshake\nPRF -> PTK (per session)", fill=BLUE, stroke=NAVY, bold=True, size=10)
f.arrow([(379, 56), (320, 84)]); f.arrow([(196, 107), (230, 107)])
for i, (t, s) in enumerate([("KCK", "authenticates\nhandshake"), ("KEK", "protects the\ngroup key"), ("TK", "encrypts your\ndata frames")]):
    f.box(60 + i * 160, 156, 140, 48, t + "\n" + s, fill=MINT, stroke=TEAL, size=10, bold=True)
    f.arrow([(305, 130), (130 + i * 160, 156)], color=TEAL)
f.box(450, 84, 124, 46, "Same passphrase,\ndifferent session\nkeys every time", fill=ROSE, stroke=RED, size=9)
```

```svgfig label="5.4" caption="A token bucket with capacity B = 10 and refill r = 5 tokens per second under a flood of 100 requests per second. The accepted total never exceeds B + r x t: 10 at once, then about 5 per second, at most 60 after 10 seconds (the run in section 5.4 accepted 59), so the server sees a bounded load."
f = Fig(580, 216)
X = lambda t: 60 + t * 30
Y = lambda v: 186 - v * 2.5
f.line(60, 186, 360, 186, color=SLATE); f.line(60, 186, 60, 30, color=SLATE)
for t in range(0, 11, 2):
    f.text(X(t), 200, str(t), size=9.5, color=SLATE)
for v in range(0, 61, 20):
    f.text(48, Y(v) + 3, str(v), size=9.5, color=SLATE, anchor="end")
f.text(210, 212, "time (seconds)", size=9.5, color=SLATE)
f.text(20, 100, "accepted", size=9.5, color=SLATE)
f.arrow([(60, 186), (60, 160), (X(10), Y(60))], color=TEAL, sw=2.4)
f.arrow([(60, 186), (70, 40)], color=RED, dash=True)
f.text(92, 38, "offered load: 1000 in 10 s", size=9.5, color=RED, bold=True, anchor="start")
f.box(396, 30, 178, 48, "Bound = B + r x t\n= 10 + 5 x 10 = 60", fill=MINT, stroke=TEAL, bold=True, size=11)
f.box(396, 92, 178, 62, "A burst of 15 at t = 0:\n10 accepted, 5 rejected\n(bucket empties at once)", fill=SAND, stroke=AMBER, size=10)
f.box(396, 166, 178, 36, "Legitimate users still get\nservice after the burst", fill=BLUE, stroke=NAVY, size=10)
```

### 5.7.1 Eight good practices for network defence

1. **Segment the network.** Put public servers, staff devices and databases in different zones with a firewall between them. If a web server is attacked, the database is still behind another wall. A college can separate the lab network from the administration network.
2. **Default deny.** Block everything and permit only listed services. Each rule should have an owner and a purpose. A short rule list is easier to review than a long one.
3. **Order rules carefully.** In a first-match ACL, an early broad rule can shadow a later specific one. Review the list for shadowed rules after every change. Test with sample packets before going live.
4. **Sign DNS and validate answers.** DNSSEC lets resolvers detect forged answers. Enable validation on your resolvers even if your own zone is not yet signed. This protects users from being sent to a fake bank site.
5. **Use WPA3 or WPA2 with a long passphrase.** A short, common Wi-Fi password can be guessed offline from a captured handshake. Use at least 16 random characters, and change it when staff leave. Guest Wi-Fi must be separated from the office network.
6. **Rate-limit public services.** A token bucket allows normal bursts but caps floods. Apply it to login, OTP and search endpoints. This protects availability and also slows password guessing.
7. **Log and monitor.** Collect firewall, DNS and authentication logs in one place and alert on unusual patterns. A sudden rise in denied connections is an early warning. Keep logs long enough to investigate, for example 90 days.
8. **Patch and back up network devices.** Firewalls and routers have vulnerabilities too. Apply vendor updates in a planned window and store configuration backups offline. After a failure, the network can be rebuilt quickly.

## 5.8 Summary and exercises

Network defence uses zones, default deny and segmentation; DNSSEC provides signed answers through a chain of trust; the birthday bound sets hash lengths at twice the desired collision resistance; WPA2 derives PMK and PTK and WPA3 adds SAE with forward secrecy; token buckets bound bursts and sustained rates; and first-match ACLs need audit for shadowing.

1. Explain the chain of trust from the root to a domain's A record in DNSSEC, naming the record types involved.
2. How many samples give a 50% collision chance in a 20-bit space, by the closed form?
3. Why does WPA3's SAE give forward secrecy while WPA2-Personal does not?
4. For a bucket with B = 20 and r = 10 per second, what is the maximum number of requests accepted in 5 seconds?
5. Reorder the second ACL in this unit so that the deny for 10.0.5.0/24 takes effect. Verify it with the program.
6. Why is default deny a better foundation than a list of blocked items?

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain how DNSSEC protects DNS answers using a chain of trust.**

*Introduction.* Plain DNS has no authentication, so a resolver cannot tell whether an answer is genuine and a forged answer could send users to a fake banking site. DNSSEC adds digital signatures to DNS data (section 5.2).

*Mechanism (Figure 5.2).*

1. A zone signs each set of records with its **zone signing key (ZSK)**. The signature is published as an **RRSIG** record and the public key as a **DNSKEY** record.
2. A **key signing key (KSK)** signs the DNSKEY set.
3. A hash of the KSK is published as a **DS** record in the parent zone, which is itself signed.
4. The chain continues up to the root, whose key is the **trust anchor** configured in the validating resolver.

*Validation.* The resolver checks the RRSIG on the answer with the ZSK, the ZSK with the KSK, the KSK against the DS hash in the parent, and so on to the root. If every link verifies, the answer is *secure*; if any link fails, it is *bogus* and the resolver returns an error.

| Record | Purpose |
|---|---|
| DNSKEY | Public key of the zone |
| RRSIG | Signature over a record set |
| DS | Hash of the child's KSK, held by the parent |

*Limits.* DNSSEC proves authenticity and integrity, not secrecy; queries stay readable unless DNS over HTTPS or TLS is also used.

**Q2 (5 marks). Explain the token bucket algorithm with the figures from a worked simulation.**

*Introduction.* Rate limiting protects availability by capping how fast clients may use a service. The token bucket is the most common algorithm because it allows short bursts but bounds the long-term rate (section 5.4).

*Algorithm.* A bucket holds at most B tokens and is refilled at r tokens per second. Each request spends one token; if the bucket is empty, the request is refused or delayed.

*Parameters used.* B = 10 and r = 5 tokens per second.

1. **Burst test.** 15 requests arrive at the same instant. The bucket starts full, so 10 are accepted and 5 are rejected.
2. **Flood test.** Requests arrive at 100 per second for 10 seconds, 1,000 in all. The simulation accepted 59 of them, just under the theoretical limit of B + r x t = 10 + 5 x 10 = 60 (Figure 5.4).

| Case | Offered | Accepted | Rejected |
|---|---|---|---|
| Burst at t = 0 | 15 | 10 | 5 |
| 10 s at 100 per second | 1,000 | 59 | 941 |

*Uses.* Login, OTP and search endpoints use token buckets so that a script cannot try thousands of passwords per minute while ordinary users still work.

*Conclusion.* The bucket size sets the allowed burst and the refill rate sets the sustained rate, so the server load is always bounded.

**Q3 (10 marks). Describe the architecture of a defended network. Explain zones, first-match ACLs with an example, and the security of Wi-Fi.**

*Introduction.* No single device protects a network, so a defended network is built from zones, filtering rules, monitored links and encrypted wireless access. The aim is to keep an attacker from moving from one weak point to the data (section 5.1 and Figure 5.1).

*1. Zones.* The network is divided by trust: the external zone (internet), a **DMZ** holding public servers, an internal zone for staff and a data zone for databases and backups. Firewalls between zones allow only listed services, so the internet reaches port 443 of the web server and nothing in the data zone.

*2. First-match ACLs.* A packet-filter ACL is an ordered list; the first matching rule decides, and a final deny catches the rest. Take the three-rule list: (1) permit TCP from any to 10.0.1.0/24 port 443; (2) permit TCP from 10.0.9.0/24 to 10.0.1.0/24 port 22; (3) deny everything else.

| Packet | Matching rule | Decision |
|---|---|---|
| TCP 203.0.113.5 to 10.0.1.10 port 443 | 1 | permit |
| TCP 203.0.113.5 to 10.0.1.10 port 22 | 3 | deny |
| TCP 10.0.9.4 to 10.0.1.10 port 22 | 2 | permit |
| UDP 10.0.9.4 to 10.0.1.10 port 53 | 3 | deny |

*3. Shadowed rules.* A rule is shadowed if an earlier rule already matches all its packets. If rule 1 permits SSH from anywhere, a later rule that denies SSH from one subnet never fires, so the intended block fails. Administrators audit ACLs for shadowing after each change.

*4. DNS and rate limits.* Resolvers validate DNSSEC to reject forged answers, and public endpoints use token buckets to bound floods (Figures 5.2 and 5.4).

*5. Wi-Fi security.* WPA2-Personal derives a 256-bit PMK from the passphrase and SSID with PBKDF2 (4,096 iterations). The four-way handshake mixes two nonces and both MAC addresses to create a new PTK of 384 bits per session, split into KCK, KEK and TK of 128 bits each (Figure 5.3). Because the PMK depends only on the passphrase and SSID, a short passphrase can be guessed offline from a captured handshake, so use a long random one or WPA3.

| Control | Protects | Failure if missing |
|---|---|---|
| Zoning | Lateral movement | One breach reaches the data |
| ACL default deny | Unwanted services | Accidental exposure |
| DNSSEC | Name resolution | Redirection to fake sites |
| Rate limiting | Availability | Flood or guessing succeeds |
| WPA3 or strong WPA2 | Wireless data | Eavesdropping, free riders |

*Conclusion.* Layers, default deny, careful rule order and monitoring together give a network where one mistake does not become a disaster.

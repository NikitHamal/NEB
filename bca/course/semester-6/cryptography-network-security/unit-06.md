---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 6
title: Authentication and Secure Network Protocols
hours: 8
area: BCA 353 · Cryptography and Network Security · Unit 6
---

The primitives of the earlier units become useful only when assembled into **protocols**: precise sequences of messages that two machines follow to authenticate each other, agree on keys and protect data. A small mistake in a protocol breaks a cipher that is perfectly secure on its own. This unit studies the protocols you meet daily: **Kerberos** (single sign-on inside an organisation), **TLS 1.3** (every HTTPS connection), **IPsec** (VPNs), **SSH** and **PGP/S-MIME** (secure remote access and email), with calculations of their cost: handshake delay and the byte overhead of IPsec.

::: key What this unit gives you
- Authentication methods and protocol attacks (replay, reflection, man-in-the-middle); nonces and timestamps.
- Kerberos: tickets, the three exchanges, and why it works.
- TLS 1.3 handshake and its latency; HTTPS, certificates and forward secrecy.
- IPsec: AH, ESP, transport and tunnel modes with an overhead calculation; PGP and SSH.
:::

## 6.1 Authentication and its attacks

**Authentication** proves identity with something you **know** (password, PIN), **have** (phone, token, smart card), **are** (fingerprint, face) or **where you are**; **multi-factor** combines two or more kinds. In a network the two ends must also authenticate *each other* (**mutual authentication**) over an insecure channel. Attacks on protocols: **replay** (record a valid message, send it again later); **man-in-the-middle** (sit between the parties); **reflection** (return the victim's own challenge); **impersonation** by stolen credentials. Defences: **nonces** (random numbers used once; a challenge–response proves freshness: the server sends a nonce, the client returns MAC(K, nonce)), **timestamps** (need loosely synchronised clocks) and **sequence numbers**; and binding messages to the session so they cannot be spliced. Passwords must never travel in the clear: challenge–response, or a password-authenticated key exchange, or TLS around the login, avoids it. One-time passwords come from **HOTP** (counter-based) and **TOTP** (time-based): TOTP = HMAC(K, ⌊time/30⌋) truncated to six digits, which is what authenticator apps compute.

## 6.2 Kerberos

**Kerberos** (MIT, Needham–Schroeder-based) lets a user log in once and then use many network services without sending the password again, using a trusted **Key Distribution Center (KDC)** made of an **Authentication Server (AS)** and a **Ticket-Granting Server (TGS)**. Each user and service shares a long-term secret key with the KDC (derived from the password for users). Three exchanges:

1. **AS exchange (login):** the client asks the AS for a **ticket-granting ticket (TGT)**. The AS replies with a TGT (encrypted under the TGS's key) and a **session key** for the TGS (encrypted under the user's key). Only the real user can decrypt the session key, so the password is never sent.
2. **TGS exchange (get a service ticket):** the client presents the TGT plus an **authenticator** (the client's name and a timestamp encrypted under the session key) and names the service; the TGS returns a **service ticket** (encrypted under the service's key) and a service session key.
3. **Client–server exchange:** the client sends the service ticket and a fresh authenticator; the service decrypts the ticket with its key, learns the session key and client name, checks the timestamp (replays are rejected within the clock-skew window, typically 5 minutes) and, if mutual authentication is requested, returns the timestamp encrypted under the session key.

Benefits: single sign-on, no passwords on the network, mutual authentication, and the KDC is the only place secrets are stored. Weaknesses: the KDC is a **single point of failure and attack** (replicate it); **clocks must be synchronised**; offline **password guessing** against captured AS replies if passwords are weak; tickets can be stolen from memory. It underlies **Microsoft Active Directory** logins.

## 6.3 TLS and HTTPS

**TLS (Transport Layer Security)** is the successor to SSL and protects HTTPS, email transport, and many other protocols above TCP. It gives **confidentiality** (symmetric encryption), **integrity** (authenticated encryption) and **server authentication** (a certificate, Unit 5), optionally client authentication. TLS has two parts: the **handshake**, which authenticates and agrees on keys, and the **record protocol**, which protects the data with AEAD (AES-GCM or ChaCha20-Poly1305).

**TLS 1.3** (RFC 8446, 2018) removed old weak options (RSA key transport, CBC, RC4, SHA-1, compression) and shortened the handshake to **one round trip**:

1. **ClientHello:** supported cipher suites, a random value, and a **key share** (the client's ephemeral Diffie–Hellman public value, usually X25519).
2. **ServerHello + key share:** the server chooses a suite and sends its key share. Both sides now compute the shared secret and derive keys with **HKDF**; everything after this is **encrypted**.
3. **Server Certificate, CertificateVerify** (a signature over the handshake transcript with the certificate's private key) and **Finished** (a MAC over the whole transcript).
4. **Client Finished.** Application data flows.

Because the DH values are **ephemeral**, TLS 1.3 always has **forward secrecy**. **Session resumption** with a pre-shared key allows **0-RTT** data (fast but replayable, so only for idempotent requests). Browsers show the padlock when the certificate chains to a trusted root, is valid and matches the host name.

The handshake cost is a latency cost. With a round-trip time of 80 ms, fetching a page requires one TCP round trip, the TLS handshake, and one for the request and first byte of the response. TLS 1.2 needs **2** round trips for the handshake, TLS 1.3 needs **1**, and resumed TLS 1.3 with 0-RTT needs **0**:

| Protocol | TCP | TLS handshake | Request/response | Time to first byte at RTT = 80 ms |
|---|---|---|---|---|
| TLS 1.2 | 1 RTT | 2 RTT | 1 RTT | 4 × 80 = **320 ms** |
| TLS 1.3 | 1 RTT | 1 RTT | 1 RTT | 3 × 80 = **240 ms** |
| TLS 1.3 resumed, 0-RTT | 1 RTT | 0 RTT | 1 RTT | 2 × 80 = **160 ms** |

On a 200 ms mobile link the saving of one round trip is **200 ms** per new connection, which is why HTTP/3 (QUIC, which integrates TLS 1.3 into UDP-based transport) goes further.

## 6.4 IPsec

**IPsec** secures traffic at the **network layer**, protecting any application without changes, and is the basis of many VPNs. It has two protocols: **AH (Authentication Header)** gives integrity and origin authentication (not confidentiality) and breaks under NAT, so it is rarely used; **ESP (Encapsulating Security Payload)** gives confidentiality, integrity and optional anti-replay, and is the standard. Two **modes**: **transport mode** protects the payload of the original IP packet (host to host); **tunnel mode** encrypts the *whole original packet* and wraps it in a new IP header (gateway to gateway, the site-to-site and remote-access VPN). A **security association (SA)** is the one-way agreement (algorithms, keys, SPI, sequence counter); **IKEv2** negotiates SAs and authenticates the peers with certificates or pre-shared keys, using Diffie–Hellman.

**ESP overhead in tunnel mode** (AES-CBC with HMAC-SHA1-96): new IP header 20 bytes, ESP header (SPI + sequence number) 8, IV 16, the original packet plus the 2-byte ESP trailer (pad length, next header) padded to a multiple of 16, and an ICV of 12 bytes. For an inner packet of 1400 bytes: 1400 + 2 = 1402 padded to 1408 (6 pad bytes), so the new packet is 20 + 8 + 16 + 1408 + 12 = **1464 bytes**, an overhead of 64 bytes (4.6%). Since a standard Ethernet MTU is 1500 bytes, the largest inner packet that avoids fragmentation is **1438 bytes**, which is why VPN links lower the MTU or clamp the TCP segment size.

## 6.5 PGP, S/MIME and SSH

**PGP** (Pretty Good Privacy; the standard is OpenPGP, with GnuPG as the free implementation) protects email and files. To send a signed and encrypted message: hash the message and sign the digest with the sender's private key; compress; encrypt with a random **session key** using a symmetric cipher; encrypt the session key with the recipient's public key; send both. PGP has no certificate authorities: trust comes from a **web of trust** in which users sign each other's keys. **S/MIME** uses the same ideas with X.509 certificates, which suits organisations. **SSH** secures remote login and file transfer: the server authenticates with a host key (the first connection asks you to verify its **fingerprint**; a changed fingerprint is a warning of a possible attack), the client authenticates with a password or, better, a **public key** (`ssh-keygen`, `authorized_keys`); a key exchange yields a session key that encrypts the channel and supports **port forwarding** (tunnels). Disable password logins and root login on servers.

## 6.6 Comparing the layers

| Protocol | Layer | Protects | Authentication | Typical use |
|---|---|---|---|---|
| IPsec | Network | All IP traffic | Peer certificates or PSK (IKEv2) | VPN |
| TLS | Transport/application | One connection | Server certificate (and optionally client) | HTTPS, email, APIs |
| SSH | Application | Login and tunnels | Host key and user key | Administration |
| PGP / S/MIME | Application (message) | Email content | Web of trust / X.509 | Email, files |
| Kerberos | Application | Authentication to services | Tickets from the KDC | Enterprise login |

## Chapter summary

- Authentication uses what you know, have or are; protocols need nonces or timestamps against replay and authenticated key exchange against man-in-the-middle; TOTP = HMAC over a time counter.
- Kerberos issues a TGT then service tickets; passwords never travel, but clocks and the KDC are critical.
- TLS 1.3 completes its handshake in one round trip with ephemeral DH (forward secrecy): time to first byte at 80 ms RTT is 240 ms against 320 ms for TLS 1.2.
- IPsec ESP in tunnel mode adds 64 bytes to a 1400-byte packet; AH is rarely used; IKEv2 sets up SAs.
- PGP uses a hybrid signed-and-encrypted design with a web of trust; SSH uses host and user keys.

## Practice

1. Describe a challenge–response authentication using a nonce and an HMAC.
2. Why do replay attacks fail against Kerberos authenticators?
3. List the three Kerberos exchanges and what each returns.
4. How many round trips does the TLS 1.3 handshake need and what feature allows zero?
5. Compute time to first byte for TLS 1.2 at RTT = 50 ms.
6. What provides forward secrecy in TLS 1.3?
7. Compare AH and ESP, and transport and tunnel modes.
8. Compute the ESP tunnel packet size for a 1000-byte inner packet (AES-CBC, HMAC-SHA1-96).
9. Describe the steps of sending a PGP signed and encrypted email.
10. What should you check when SSH warns that a host key has changed?

::: note Answers and worked solutions
**1.** The server sends a random nonce; the client returns HMAC(K, nonce); the server recomputes and compares. A fresh nonce prevents replay of an old response.
**2.** An authenticator contains a timestamp encrypted with the session key; the service accepts only fresh timestamps within the clock-skew window and remembers recent authenticators.
**3.** AS exchange: TGT and TGS session key. TGS exchange: service ticket and service session key. Client–server exchange: the service verifies the ticket and authenticator (and may reply for mutual authentication).
**4.** One round trip; resumption with a pre-shared key allows 0-RTT (early data).
**5.** (1 + 2 + 1) × 50 = **200 ms**.
**6.** The ephemeral Diffie–Hellman key shares generated fresh for each session.
**7.** AH: integrity and authentication only; ESP: encryption plus integrity. Transport mode protects the payload between hosts; tunnel mode encapsulates the whole packet in a new IP header (gateway VPNs).
**8.** 1000 + 2 = 1002, padded to 1008 (6 pad bytes); total = 20 + 8 + 16 + 1008 + 12 = **1064 bytes**.
**9.** Hash and sign the message; compress; encrypt with a random session key; encrypt that key with the recipient's public key; send both.
**10.** Whether the server was legitimately reinstalled or re-keyed (ask the administrator for the fingerprint out of band); otherwise it may be a man-in-the-middle, so do not continue.
:::

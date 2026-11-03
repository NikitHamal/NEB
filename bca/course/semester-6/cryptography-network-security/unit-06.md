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

## 6.7 Seeing the protocols: tickets, handshakes and tunnels

Protocols are conversations, so they are best learned as drawings of who says what to whom. The plate pairs a mythical guard, the author of PGP and a small VPN router with the three families in this unit. The figures show the Kerberos tickets, the TLS 1.3 handshake, the layout of an ESP packet, the protocol stack and a challenge-response exchange that stops replay.

```photogrid label="6.1" cols="3" ratio="1.0" caption="Names and objects behind the protocols. (a) Cerberus, the three-headed dog that guards the gate of the underworld and gave Kerberos its name: the three heads stand for the client, the server and the key distribution centre. (b) Phil Zimmermann, who released PGP in 1991 so that ordinary people could encrypt email. (c) A small-office router that supports IPsec VPN tunnels, the kind of box that joins a branch office to the head office over the public internet."
@ photo id="crypto353/cerberus" cap="Cerberus (Kerberos)"
fit 1.0
focus 0.5 0.6
@ photo id="crypto353/zimmermann" cap="Phil Zimmermann (PGP)"
fit 1.0
focus 0.5 0.62
@ photo id="crypto353/ipsecrouter" cap="IPsec VPN router"
fit 1.0
focus 0.5 0.55
call 0.5 0.9 0.5 0.6 "VPN tunnel endpoint"
```

```svgfig label="6.1" caption="Kerberos in six messages. (1, 2) The client asks the authentication server (AS) for a ticket-granting ticket (TGT); the reply is protected by a key made from the user's password, so only the real user can open it. (3, 4) To use a service, the client shows the TGT and an authenticator (a timestamp encrypted with the session key) to the ticket-granting server (TGS) and receives a service ticket. (5, 6) The client presents the service ticket to the server, which may reply with a timestamp to prove its own identity. The password never crosses the network and clocks must agree within about five minutes."
f = Fig(580, 270)
lanes = [("Client", 50), ("Authentication\nserver (AS)", 200), ("Ticket-granting\nserver (TGS)", 360), ("Service\nserver", 520)]
for nm, x in lanes:
    f.box(x - 52, 4, 104, 34, nm, fill=BLUE, stroke=NAVY, size=10.5, bold=True)
    f.line(x, 38, x, 262, color="#cbd5e1", sw=1.2, dash=True)
msgs = [(1, 50, 200, "1  request TGT (user ID, nonce)", 62), (2, 200, 50, "2  TGT + session key (password-protected)", 94), (3, 50, 360, "3  TGT + authenticator + service name", 126), (4, 360, 50, "4  service ticket + new session key", 158), (5, 50, 520, "5  service ticket + authenticator", 190), (6, 520, 50, "6  timestamp + 1 (proves the server)", 222)]
for n, a, b, lab, y in msgs:
    d = 1 if b > a else -1
    f.arrow([(a + 4 * d, y), (b - 4 * d, y)], color=(TEAL if n % 2 == 0 else NAVY), label=lab, lpos=((a + b) / 2, y - 7), lsize=9.5)
```

```svgfig label="6.2" caption="The TLS 1.3 handshake in one round trip. The client's first message already carries a key share (an elliptic-curve Diffie-Hellman value); the server answers with its own share, so both sides can derive the handshake keys at once. Everything after the server hello is encrypted, including the certificate. After the client's finished message, application data flow under keys that are fresh for this session only, which gives forward secrecy."
f = Fig(580, 270)
f.box(40, 4, 110, 30, "Client (browser)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(430, 4, 110, 30, "Server (bank)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.line(95, 34, 95, 262, color="#cbd5e1", sw=1.2, dash=True); f.line(485, 34, 485, 262, color="#cbd5e1", sw=1.2, dash=True)
f.arrow([(99, 62), (481, 62)], color=NAVY, label="ClientHello: versions, ciphers, key share, server name", lpos=(290, 54), lsize=10)
f.arrow([(481, 100), (99, 100)], color=TEAL, label="ServerHello: chosen cipher, key share", lpos=(290, 92), lsize=10)
f.box(150, 112, 280, 22, "both derive handshake keys; the rest is encrypted", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(481, 160), (99, 160)], color=TEAL, label="Certificate, CertificateVerify, Finished (encrypted)", lpos=(290, 152), lsize=10)
f.arrow([(99, 196), (481, 196)], color=NAVY, label="Finished (encrypted)", lpos=(290, 188), lsize=10)
f.arrow([(99, 236), (481, 236)], color=RED, both=True, label="application data (AEAD, session keys)", lpos=(290, 228), lsize=10)
```

```svgfig label="6.3" caption="An IPsec ESP packet in tunnel mode. The original IP packet (header, TCP segment and data) is placed inside a new packet. The ESP header carries the security parameter index (SPI, which names the agreement) and a sequence number against replay; the original packet and the ESP trailer (padding, pad length, next header) are encrypted; the authentication field at the end holds an integrity tag over everything from the ESP header onward. The new outer IP header is not protected and is used to route the packet between the two VPN gateways."
f = Fig(580, 150)
parts = [("New IP\nheader", 70, SAND, AMBER), ("ESP\nheader\nSPI, seq", 70, ROSE, RED), ("Original IP\nheader", 80, BLUE, NAVY), ("TCP\nheader", 60, BLUE, NAVY), ("Data", 100, BLUE, NAVY), ("ESP\ntrailer", 60, ROSE, RED), ("ESP\nauth tag", 70, MINT, TEAL)]
x = 8
for t, w, fl, c in parts:
    f.box(x, 30, w, 54, t, fill=fl, stroke=c, size=10, bold=True, r=3); x += w + 4
f.line(8 + 74 + 74, 100, 8 + 74 + 74 + 80 + 4 + 60 + 4 + 100 + 4 + 60, 100, color=RED, sw=2)
f.text(330, 118, "encrypted", size=10.5, color=RED, bold=True)
f.line(8 + 74, 126, 8 + 74 + 74 + 84 + 64 + 104 + 64 + 70, 126, color=TEAL, sw=2)
f.text(330, 144, "authenticated (integrity tag)", size=10.5, color=TEAL, bold=True)
f.text(43, 100, "routing only", size=9.5, color=AMBER, bold=True)
```

```svgfig label="6.4" caption="Where each protocol sits. PGP and S/MIME protect individual messages inside the application. SSH and TLS sit between the application and TCP and protect one connection. IPsec works at the network layer and protects all traffic between two hosts or two networks without any change to applications. Wi-Fi security (WPA2 and WPA3) protects only the wireless hop between a device and the access point. The lower the layer, the more traffic it covers, but the less it knows about the user or the application."
f = Fig(580, 210)
L = [("Application", "PGP, S/MIME (messages)", BLUE, NAVY), ("Between application and TCP", "TLS / HTTPS, SSH (connections)", MINT, TEAL), ("Network (IP)", "IPsec: AH, ESP, IKE (host or site tunnels)", SAND, AMBER), ("Link (wireless)", "WPA2 / WPA3 (one Wi-Fi hop)", ROSE, RED)]
for i, (a, b, fl, c) in enumerate(L):
    y = 8 + i * 46
    f.box(8, y, 190, 38, a, fill=fl, stroke=c, size=11, bold=True)
    f.box(204, y, 366, 38, b, fill="#ffffff", stroke=c, size=11.5, bold=True)
f.text(290, 202, "Lower layer = more traffic covered, less knowledge of the user.", size=10.5, color=SLATE)
```

```photogrid label="6.2" cols="2" ratio="1.1" caption="Authentication in practice. (a) The https prefix and padlock in a browser address bar show that TLS is active: the server has proved its identity with a certificate and the traffic is encrypted. (b) A challenge-response exchange: the server sends a fresh random challenge, the client returns a response computed from the challenge and a secret, and an eavesdropper who records the response cannot reuse it, because the next challenge will differ (this is how security tokens and many login systems stop replay)."
@ photo id="cs11/https-padlock" cap="Padlock in the address bar"
fit 1.1
focus 0.4 0.5
call 0.3 0.15 0.18 0.5 "TLS is active"
@ svg cap="Challenge-response against replay"
f = Fig(340, 300)
f.box(6, 8, 110, 44, "Client\nsecret K", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(224, 8, 110, 44, "Server\nsecret K", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.line(61, 52, 61, 250, color="#cbd5e1", sw=1.2, dash=True); f.line(279, 52, 279, 250, color="#cbd5e1", sw=1.2, dash=True)
f.arrow([(65, 80), (275, 80)], color=NAVY, label="login request", lpos=(170, 72), lsize=12)
f.arrow([(275, 128), (65, 128)], color=TEAL, label="challenge R = 8F3A91", lpos=(170, 120), lsize=12)
f.arrow([(65, 176), (275, 176)], color=NAVY, label="HMAC(K, R)", lpos=(170, 168), lsize=12)
f.text(170, 208, "Server recomputes and compares:", size=12, color=SLATE)
f.text(170, 228, "match = client knows K", size=12, color=TEAL, bold=True)
f.text(170, 262, "A recorded reply is useless:", size=12, color=RED, bold=True)
f.text(170, 282, "the next challenge differs.", size=12, color=RED, bold=True)
```

### 6.7.1 Eight reasons TLS 1.3 is better than TLS 1.2

1. **A faster handshake.** TLS 1.3 completes the handshake in one round trip, where TLS 1.2 needs two. On a mobile link in a hill district with 150 ms round-trip time, this saves about 150 ms for every new connection. Pages that open many connections therefore load noticeably sooner.
2. **Forward secrecy always.** TLS 1.3 allows only ephemeral Diffie-Hellman key exchange, so every session has fresh keys. If the server's private key is stolen next year, recorded old traffic still cannot be decrypted. TLS 1.2 allowed plain RSA key exchange, which gave no such protection.
3. **Weak algorithms removed.** RC4, 3DES, MD5, SHA-1 signatures, static RSA and CBC-mode ciphers are no longer in the standard. A misconfigured server cannot fall back to them. Removing bad options is often the cheapest way to improve security.
4. **Authenticated encryption only.** Every record uses an AEAD cipher such as AES-GCM or ChaCha20-Poly1305, which provides secrecy and integrity in one step. This closes padding-oracle attacks such as the ones that hurt CBC modes. The designers deliberately left no unauthenticated option.
5. **More of the handshake is encrypted.** After the server hello, the certificate and other messages are encrypted. An observer on the network learns far less about who the server is. Privacy features such as encrypted server names are built on this base.
6. **A much shorter list of cipher suites.** TLS 1.2 had hundreds of combinations, many of them unsafe. TLS 1.3 has five. Fewer choices mean fewer mistakes by administrators and fewer attacks that trick a server into a weak choice (downgrade attacks).
7. **Stronger protection of the handshake.** The final messages are signed over the whole transcript, so a changed message is detected. This stops an active attacker from silently altering the negotiation. TLS 1.3 also includes a downgrade signal in the server random value.
8. **Optional 0-RTT resumption.** A returning client can send data in its first flight, which is useful for fast repeated requests. The standard warns that such data can be replayed, so it should be used only for safe requests such as reading a page. The choice is explicit rather than hidden.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain how Kerberos authenticates a user to a network service. Why does the password never travel over the network?**

*Introduction.* Kerberos is a ticket-based authentication protocol (MIT, now an IETF standard) in which a trusted key distribution centre (KDC), made of an authentication server (AS) and a ticket-granting server (TGS), vouches for users to services (section 6.2, Figure 6.1).

1. **Login (AS exchange).** The client sends its user name to the AS. The AS replies with a ticket-granting ticket (TGT) and a session key, both encrypted with a key derived from the user's password. Only the real user can open the reply.
2. **Ticket request (TGS exchange).** To use a service, the client sends the TGT and an authenticator (timestamp encrypted with the session key) to the TGS and receives a service ticket for that service.
3. **Service request.** The client sends the service ticket and a new authenticator to the service, which opens the ticket with its own long-term key, trusts the session key inside and may return the timestamp plus one to prove its identity.
4. **Why the password stays local.** It is used only on the client machine to decrypt the AS reply. The network sees only encrypted tickets.
5. **Limits.** Clocks must agree (about 5 minutes), the KDC is a single point of failure and offline password guessing against the AS reply is possible if passwords are weak.

| Message | From to | Contains |
|---|---|---|
| 1 | Client to AS | User ID, nonce |
| 2 | AS to client | TGT, session key |
| 3 | Client to TGS | TGT, authenticator |
| 4 | TGS to client | Service ticket |
| 5 | Client to server | Ticket, authenticator |
| 6 | Server to client | Timestamp plus one |

**Q2 (5 marks). Describe the TLS 1.3 handshake and the security services that TLS provides.**

*Introduction.* Transport Layer Security (RFC 8446) protects a TCP connection and is the security layer of HTTPS (section 6.3, Figure 6.2).

1. **ClientHello.** The client sends supported versions and cipher suites, a random value and a Diffie-Hellman key share.
2. **ServerHello.** The server selects a suite and sends its own key share. Both sides now compute the shared secret and derive handshake keys.
3. **Server authentication.** In encrypted messages the server sends its certificate chain and a CertificateVerify signature over the handshake, followed by Finished.
4. **Client Finished.** The client checks the certificate chain and signature, then sends its Finished message. This completes the handshake in **one round trip**.
5. **Application data.** Data are protected by an AEAD cipher with fresh keys for this session.
6. **Services.** Confidentiality (encryption), integrity (authentication tag on every record), server authentication (certificate) and forward secrecy (ephemeral keys).

**Q3 (5 marks). Compare IPsec transport mode and tunnel mode, and AH and ESP.**

*Introduction.* IPsec secures traffic at the IP layer using two protocols and two modes, set up by IKE (section 6.4, Figure 6.3).

1. **AH (authentication header).** Gives integrity and authentication of the packet, including parts of the IP header, but no encryption. It breaks with NAT, so it is rarely used.
2. **ESP (encapsulating security payload).** Gives encryption, integrity and anti-replay. It is the common choice.
3. **Transport mode.** The original IP header is kept and only the payload is protected. Used between two hosts.
4. **Tunnel mode.** The whole original packet is encapsulated in a new packet with a new IP header. Used between two gateways to build a site-to-site VPN.
5. **IKE.** The Internet Key Exchange authenticates the peers, runs Diffie-Hellman and creates the security associations (identified by the SPI).

| Feature | AH | ESP |
|---|---|---|
| Encryption | No | Yes |
| Integrity | Yes (with header) | Yes (payload) |
| Works with NAT | No | Yes (with NAT traversal) |

**Q4 (10 marks). Compare TLS, IPsec, SSH and PGP: the layer at which each works, what it protects, how keys are established and typical uses.**

*Introduction.* Secure network protocols apply the tools of Units 3 to 5 (symmetric ciphers, key exchange, hashes and signatures) at different layers. Each layer protects a different amount of traffic and suits a different job (section 6.6, Figure 6.4).

1. **TLS.** Works above TCP. It protects one connection (a web or email session). A Diffie-Hellman exchange creates the session keys and a server certificate (and optionally a client certificate) authenticates the peers. Used by HTTPS, email, APIs.
2. **IPsec.** Works at the IP layer, below all applications. It protects all packets between two hosts or gateways, and IKE sets up keys with certificates or pre-shared keys. Used for site-to-site and remote-access VPNs.
3. **SSH.** Works above TCP like TLS but is built for remote login and tunnels. Host keys identify the server (checked against a known-hosts list) and users authenticate with passwords or public keys. Used for server administration and secure file copy.
4. **PGP / S/MIME.** Work in the application and protect a single message or file. The sender encrypts a random session key with the receiver's public key and signs with their own private key. PGP uses a web of trust; S/MIME uses certificates from authorities. Used for secure email and signed software.
5. **Key establishment.** TLS, IPsec and SSH run an authenticated Diffie-Hellman exchange; PGP encrypts a one-time symmetric key with the recipient's public key.
6. **Common pattern.** All four use public-key methods to authenticate and agree a key, then a fast symmetric cipher and a MAC or AEAD for the bulk data (hybrid encryption).
7. **Choice.** Use TLS for web services, IPsec to join networks, SSH for administration and PGP when the message must stay protected after delivery.

| Protocol | Layer | Protects | Authentication | Typical use |
|---|---|---|---|---|
| TLS | Above TCP | One connection | Certificates | HTTPS, email |
| IPsec | Network | All IP traffic of a tunnel | Certificates, pre-shared keys | VPNs |
| SSH | Above TCP | One login or tunnel | Host key, user key | Administration |
| PGP | Application | One message | Web of trust, keys | Secure email |

*Conclusion.* None of the protocols replaces the others. Real systems layer them, for example an HTTPS request inside an IPsec tunnel over a WPA3 Wi-Fi link, and security depends on correct key management and certificate checking at every layer.

---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 5
title: Hash Functions, MACs, Digital Signatures and PKI
hours: 7
area: BCA 353 · Cryptography and Network Security · Unit 5
---

Encryption keeps a message secret; it does not prove who sent it or that nobody changed it. A downloaded installer, a software update, a bank instruction and a government certificate all need *integrity and authenticity*. Three tools provide them: **hash functions** (a fingerprint of data), **message authentication codes** (a fingerprint that needs a secret key) and **digital signatures** (a fingerprint that only the owner of a private key can produce). **Public-key infrastructure (PKI)** and X.509 certificates then answer "whose public key is this?". The hash and MAC values below are executed and compared with published test vectors (the NIST SHA-256 value for "abc" and RFC 4231 for HMAC-SHA256); the birthday-attack numbers are computed exactly.

::: key What this unit gives you
- Hash properties, SHA-256 in outline, the avalanche effect; the birthday attack with numbers.
- HMAC construction (checked against the RFC vector and a manual implementation).
- Digital signatures with RSA, DSA/ECDSA; certificates, X.509 and chains of trust; revocation.
- Password hashing and the Nepali legal context of digital signatures.
:::

## 5.1 Cryptographic hash functions

A **hash function** H maps a message of any length to a fixed-length **digest**. A *cryptographic* hash must satisfy: **preimage resistance** (given h, it is infeasible to find m with H(m) = h), **second-preimage resistance** (given m₁, it is infeasible to find a different m₂ with the same hash) and **collision resistance** (it is infeasible to find *any* two messages with the same hash). Also, a small change in the message must change about half the digest bits (**avalanche**). Uses: file integrity, password storage, digital signatures, commit schemes, blockchains, deduplication.

| Hash | Digest | Status |
|---|---|---|
| MD5 | 128 bits | Broken (collisions in seconds); do not use for security |
| SHA-1 | 160 bits | Broken (practical collisions since 2017); being retired |
| **SHA-256 / SHA-512** (SHA-2) | 256 / 512 bits | Secure; the workhorses |
| **SHA-3** (Keccak) | 224–512 bits | Secure; a different design (sponge) |

**SHA-256 in outline** (a Merkle–Damgård construction): the message is padded (a 1 bit, zeros, then the 64-bit message length) to a multiple of 512 bits; each 512-bit block is expanded into a schedule of 64 words and processed by **64 rounds** that mix eight 32-bit working variables with bitwise functions (Ch, Maj, rotations Σ₀ and Σ₁) and 64 constants; the result is added to the previous 256-bit state, which starts from fixed initial values. Length-extension weaknesses of plain SHA-256 are why **HMAC** (below) is used instead of H(key ‖ message).

### The birthday attack

Why are collisions much easier than preimages? With N = 2ⁿ possible digests, the probability that k random messages contain *some* collision is 1 − ∏ᵢ₌₁ᵏ⁻¹ (1 − i/N), and it reaches 50% when k ≈ **1.1774·√N**. For the classic birthday problem (N = 365), 23 people already give a probability of **0.5073**. For a 64-bit digest, N = 2⁶⁴ and collisions appear after about 1.1774 × 2³² = **5,056,894,494** messages: feasible. This is why hashes need at least 256 bits for 2¹²⁸ collision resistance, and why a 64-bit block cipher such as 3DES in CBC mode leaks after about 2³² blocks (2³² × 8 bytes = **32 GiB**).

```python
import hashlib, hmac
h = hashlib.sha256(b"abc").hexdigest()
print("SHA-256('abc') =", h)
h2 = hashlib.sha256(b"abd").hexdigest()
print("avalanche:", bin(int(h, 16) ^ int(h2, 16)).count("1"), "of 256 bits differ")

key, data = b"Jefe", b"what do ya want for nothing?"
mac = hmac.new(key, data, hashlib.sha256).hexdigest()
print("HMAC-SHA256 =", mac)

def hmac_manual(key, msg):
    if len(key) > 64:
        key = hashlib.sha256(key).digest()
    key = key.ljust(64, b"\0")
    ipad = bytes(k ^ 0x36 for k in key)
    opad = bytes(k ^ 0x5C for k in key)
    return hashlib.sha256(opad + hashlib.sha256(ipad + msg).digest()).hexdigest()

print("manual HMAC matches:", hmac_manual(key, data) == mac)
```
```output
SHA-256('abc') = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
avalanche: 122 of 256 bits differ
HMAC-SHA256 = 5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843
manual HMAC matches: True
```
The digest of "abc" is the published NIST test value ba7816bf…15ad. Changing one letter (abc to abd) flips about half of the 256 bits (the printed count is close to 128), the avalanche effect.

## 5.2 Message authentication codes and HMAC

A hash alone cannot authenticate: an attacker who alters a message simply recomputes the hash. A **message authentication code (MAC)** adds a **secret key** shared by sender and receiver: tag = MAC(K, m). The receiver recomputes the tag and compares (in constant time); a forger without K cannot produce a valid tag. **HMAC** (RFC 2104) builds a MAC from a hash H: **HMAC(K, m) = H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m))**, where ipad is the byte 0x36 and opad the byte 0x5C repeated to the hash's block size (64 bytes for SHA-256). The program above shows HMAC-SHA256 with key "Jefe" over "what do ya want for nothing?" equal to the RFC 4231 test value 5bdcc146…3843, and that the manual formula agrees with the library. **CMAC** builds a MAC from AES; **GCM** and **Poly1305** combine encryption with authentication (Unit 3). MACs give integrity and authentication but **not non-repudiation** (both parties know the key), which signatures provide.

## 5.3 Digital signatures

A **digital signature** is created with the signer's **private key** over the hash of the message and verified by anyone with the **public key**. It provides **authentication**, **integrity** and **non-repudiation**.

1. **Sign:** compute h = H(m); the signer produces s = Sign(d, h). (For RSA: s = hᵈ mod n with PSS padding.)
2. **Verify:** compute h′ = H(m) from the received message and check Verify(e, s, h′).

**DSA/ECDSA** signatures work in a discrete-log group: the signer picks a *fresh random k* for every signature and outputs a pair (r, s); **reusing or leaking k reveals the private key** (this broke the PlayStation 3 and several cryptocurrency wallets). **EdDSA (Ed25519)** derives k deterministically from the key and message, avoiding the failure. A signature on a hash is also a commitment: signing the *digest* makes signing fast and fixed-size. Signing proves that the holder of the private key signed *something*, so the private key must be protected (smart card, hardware token, HSM).

## 5.4 Certificates and PKI

How do you know a public key really belongs to *www.bank.example* and not to an attacker? A **certificate authority (CA)** vouches for the binding. An **X.509 certificate** contains: the **subject** (name, domain), the subject's **public key**, the **issuer** (the CA), **validity** dates, a **serial number**, extensions (key usage, subject alternative names, basic constraints) and the CA's **signature** over all of this. Verifying a certificate means checking the CA's signature with the CA's public key, which is itself in a certificate signed by a higher CA, and so on up to a **root CA** whose certificate is already trusted (installed in the operating system or browser). This is the **chain of trust**: *leaf (server) → intermediate CA → root CA*. Checks: signatures valid up the chain, dates valid, the name matches the domain, the key usage allows it, and the certificate is **not revoked**.

**Revocation:** a **CRL** (certificate revocation list) is a signed list of revoked serial numbers; **OCSP** asks the CA online about one certificate (with **OCSP stapling** the server attaches a fresh signed answer); short-lived certificates (the free **Let's Encrypt** CA issues 90-day certificates through the ACME protocol) reduce the need for revocation. **Certificate transparency** logs publish every issued certificate so that mis-issuance can be detected. Failures in this system are failures of the *CA*: DigiNotar (2011) was compromised and issued fraudulent certificates for Google domains.

| Item | Purpose |
|---|---|
| CA | Issues certificates; its security is critical |
| RA | Verifies identity on behalf of the CA |
| Certificate | Binds identity to a public key, signed by the CA |
| CRL / OCSP | Revocation |
| Trust store | Root certificates trusted by a device |

**In Nepal.** The **Electronic Transactions Act, 2063** recognises digital signatures and creates the **Controller of Certification** (under the Ministry of Communication and Information Technology), who licenses and supervises Certifying Authorities and runs the national root. Government and banking uses include digital-signed tax and customs filings and e-procurement, where a signature certificate on a hardware token or file identifies a bidder (see *Society and Technology*).

## 5.5 Password hashing

Storing passwords as a plain hash is unsafe because hashes are fast: a GPU computes billions of SHA-256 hashes a second, so **dictionary and brute-force attacks** on a leaked table are quick, and identical passwords have identical hashes (revealing duplicates and allowing **rainbow tables**). Correct storage uses a **per-user random salt** and a deliberately **slow, memory-hard** function (**Argon2id**, **scrypt**, **bcrypt**, or PBKDF2 with many iterations), storing (salt, cost parameters, hash); login recomputes and compares in constant time. A **pepper** (a secret kept outside the database) adds defence in depth. Combine with multi-factor authentication and rate limiting (see *MIS and e-Business*, Unit 6).

## 5.7 Seeing hashes, signatures and certificates

A hash is a fingerprint, a MAC is a fingerprint that needs a key, a signature is a fingerprint that anyone can check, and a certificate is a signed statement that a public key belongs to a named owner. The plate shows hardware that computes hashes at enormous speed, a pioneer of the field and a token that guards a private key. The figures follow the avalanche effect, the HMAC construction, the signing and verification steps, the chain of trust and the work needed to find collisions.

```photogrid label="5.1" cols="3" ratio="1.0" caption="Hashing in the real world. (a) A Bitcoin ASIC miner: its chips do nothing except compute SHA-256 twice, billions of times per second, in a search for a hash below a target value. It shows how fast dedicated hardware can run a hash, which is why plain hashes are unsuitable for storing passwords. (b) Ronald Rivest, co-inventor of RSA and designer of the MD4 and MD5 hash functions. (c) A YubiKey security token beside a bunch of keys: the private key is generated inside the chip and never leaves it, and the token signs a challenge to prove the holder is present."
@ photo id="crypto353/asic" cap="ASIC SHA-256 miner"
fit 1.0
focus 0.5 0.5
call 0.45 0.9 0.5 0.5 "hash chips under fan"
@ photo id="crypto353/rivest" cap="Ronald Rivest"
fit 1.0
focus 0.5 0.6
@ photo id="bca401/yubikey" cap="Hardware token"
fit 1.0
focus 0.75 0.5
call 0.7 0.1 0.72 0.45 "private key inside"
```

```svgfig label="5.1" caption="The avalanche effect with real values. The SHA-256 digest of 'abc' begins ba7816bf and that of 'abd' (one letter changed) begins a52d159f. Counting the bits of the two 256-bit digests that differ gives 122, about 48 percent, close to the ideal 50 percent. A good hash changes about half of its output bits when a single input bit changes, so similar inputs give unrelated digests and nothing can be learned from closeness."
f = Fig(580, 200)
f.box(8, 14, 120, 34, "message: abc", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(8, 110, 120, 34, "message: abd", fill=ROSE, stroke=RED, size=12, bold=True)
f.box(160, 14, 110, 34, "SHA-256", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(160, 110, 110, 34, "SHA-256", fill=SAND, stroke=AMBER, size=12, bold=True)
f.arrow([(128, 31), (160, 31)], color=SLATE); f.arrow([(128, 127), (160, 127)], color=SLATE)
f.box(300, 14, 270, 34, "ba7816bf 8f01cfea 414140de 5dae2223 ...", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(300, 110, 270, 34, "a52d159f 262b2c6d db724a61 840befc3 ...", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(270, 31), (300, 31)], color=SLATE); f.arrow([(270, 127), (300, 127)], color=SLATE)
f.text(435, 80, "122 of 256 output bits differ (47.7 percent)", size=12, color=TEAL, bold=True)
f.text(290, 178, "One changed input letter, an unrelated digest: no way to steer the output.", size=11, color=SLATE)
```

```svgfig label="5.2" caption="HMAC (RFC 2104). The key is padded to the block size and XORed with two fixed constants, ipad (0x36 repeated) and opad (0x5C repeated). The message is hashed together with the inner key, and the result is hashed again with the outer key: HMAC(K, m) = H((K XOR opad) followed by H((K XOR ipad) followed by m)). Two nested hashes avoid the length-extension weakness of the naive construction H(K followed by m). RFC 4231 test case 2 gives HMAC-SHA256 with key 'Jefe' and message 'what do ya want for nothing?' as 5bdcc146 bf60754e ..."
f = Fig(580, 206)
f.box(8, 40, 100, 34, "key K\n(padded)", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(140, 8, 110, 28, "K XOR ipad", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(140, 100, 110, 28, "K XOR opad", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(108, 52), (140, 24)], color=SLATE); f.arrow([(108, 62), (140, 112)], color=SLATE)
f.box(280, 8, 120, 34, "inner hash H\n(K^ipad || m)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(250, 22), (280, 22)], color=SLATE)
f.box(280, 66, 120, 28, "message m", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(340, 66), (340, 42)], color=SLATE)
f.box(420, 100, 150, 40, "outer hash H\n(K^opad || inner)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(250, 114), (420, 120)], color=SLATE)
f.arrow([(400, 25), (495, 25), (495, 100)], color=SLATE)
f.box(420, 156, 150, 32, "tag = HMAC(K, m)", fill=BLUE, stroke=NAVY, size=11.5, bold=True)
f.arrow([(495, 140), (495, 156)], color=SLATE)
f.text(210, 176, "The receiver recomputes the tag and compares.", size=10.5, color=SLATE)
```

```svgfig label="5.3" caption="A digital signature step by step. The signer hashes the document and encrypts the digest with the private key; the signature travels with the document. The verifier hashes the received document again and decrypts the signature with the signer's public key; if the two digests are equal, the document is unchanged and was signed by the owner of the private key. Hashing first keeps the signature short and fast for any document size."
f = Fig(580, 210)
f.text(4, 14, "Signer", size=11, color=NAVY, bold=True, anchor="start")
f.box(4, 22, 90, 40, "Document", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(120, 22, 90, 40, "Hash\n(SHA-256)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(236, 22, 120, 40, "Sign with\nprivate key", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(382, 22, 90, 40, "Signature", fill=MINT, stroke=TEAL, size=11, bold=True)
for a, b in ((94, 120), (210, 236), (356, 382)): f.arrow([(a, 42), (b, 42)], color=SLATE)
f.text(4, 108, "Verifier", size=11, color=NAVY, bold=True, anchor="start")
f.box(4, 116, 90, 40, "Document\nreceived", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(120, 116, 90, 40, "Hash\n(SHA-256)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(236, 116, 120, 40, "Open signature\nwith public key", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(382, 116, 90, 40, "Equal?", fill=SAND, stroke=AMBER, size=12, bold=True)
f.arrow([(94, 136), (120, 136)], color=SLATE); f.arrow([(356, 136), (382, 136)], color=SLATE)
f.arrow([(210, 136), (236, 136)], color=SLATE) if False else None
f.arrow([(165, 156), (165, 176), (427, 176), (427, 156)], color=AMBER)
f.box(490, 116, 80, 40, "valid", fill=MINT, stroke=TEAL, size=12, bold=True)
f.arrow([(472, 136), (490, 136)], color=SLATE)
f.arrow([(427, 62), (427, 80), (296, 80), (296, 116)], color=SLATE, dash=True)
f.text(290, 198, "Equal digests: unchanged document, signed by the private-key owner.", size=10.5, color=SLATE)
```

```svgfig label="5.4" caption="A chain of trust. The root certificate authority (CA) signs the intermediate CA's certificate with the root private key, and the intermediate signs the website's certificate. Browsers ship with a small list of trusted root certificates, so the browser checks each signature up the chain with the public key of the next certificate, and also checks the validity dates, the name and that the certificate is not revoked. If any link fails, the padlock is replaced by a warning."
f = Fig(580, 244)
tiers = [("Root CA", "self-signed; stored in the\nbrowser or OS trust list", ROSE, RED), ("Intermediate CA", "certificate signed by\nthe root private key", SAND, AMBER), ("Website certificate", "subject: bank.example.com.np\nsigned by the intermediate", MINT, TEAL)]
for i, (t, d, fl, c) in enumerate(tiers):
    y = 8 + i * 74
    f.box(10, y, 150, 56, t, fill=fl, stroke=c, size=12, bold=True)
    f.text(200, y + 28, d, size=10.5, color=SLATE, anchor="start")
    if i < 2:
        f.arrow([(85, y + 56), (85, y + 74)], color=SLATE, label="signs", lpos=(112, y + 66), lsize=9.5)
f.box(400, 8, 170, 150, "", fill=BLUE, stroke=NAVY)
f.text(485, 26, "Inside a certificate", size=11, color=NAVY, bold=True)
for i, s in enumerate(["subject name", "subject public key", "issuer name", "valid from / to", "usage, extensions", "issuer's signature"]):
    f.text(412, 50 + i * 18, s, size=10.5, color=SLATE, anchor="start")
f.text(290, 232, "Browser: check signature, dates, name, revocation at every link.", size=10.5, color=NAVY, bold=True)
```

```svgfig label="5.5" caption="Work needed to find a hash collision. By the birthday bound a collision in an n-bit hash needs about 2 to the power n/2 tries, not 2 to the power n. For a 16-bit toy hash this is 301 messages for a 50 percent chance; for MD5 (128 bits) it is about 2 to the power 64, and chosen-prefix attacks have made MD5 collisions cheap in practice; for SHA-1 (160 bits) the 2017 SHAttered attack found a collision with about 2 to the power 63 operations; SHA-256 needs about 2 to the power 128, which is out of reach."
f = Fig(580, 180)
rows = [("16-bit toy hash", 8, "2^8 = 256 tries", ROSE, RED), ("MD5 (128 bits)", 64, "2^64 (broken in practice)", ROSE, RED), ("SHA-1 (160 bits)", 80, "2^80 (SHAttered 2017: about 2^63)", SAND, AMBER), ("SHA-256", 128, "2^128 (safe)", MINT, TEAL)]
for i, (nm, b, d, fl, c) in enumerate(rows):
    y = 14 + i * 40
    f.text(4, y + 11, nm, size=11, color=NAVY, bold=True, anchor="start")
    w = b / 128 * 280
    f.box(140, y, w, 22, "", fill=fl, stroke=c, sw=1, r=3)
    f.text(146 + w, y + 15, d, size=10.5, color=c, bold=True, anchor="start")
f.text(290, 176, "Collision cost grows as 2 to the power (bits / 2).", size=10.5, color=SLATE)
```

### 5.7.1 Eight uses of hashes, MACs and signatures in Nepal's digital services

1. **Password storage.** A website stores a salted, slow hash of each password and not the password itself. When you log in, the site hashes what you typed and compares. A stolen database then reveals hashes that are expensive to crack, not passwords.
2. **File integrity.** A published SHA-256 value lets you check that a downloaded installer or exam software has not been changed. If one bit differs, the digest differs completely. Campus IT staff use this when they copy a software image to many lab computers.
3. **API and payment requests.** A merchant and a payment gateway share a secret key and attach an HMAC tag to every request. The gateway recomputes the tag, so an amount changed on the way is rejected. This is the pattern used between merchant servers and wallet or bank gateways.
4. **Digital signatures on documents.** A signed PDF or tax return proves who signed it and that it has not changed since. The signature covers the hash of the whole file, so adding one space breaks it. Under the Electronic Transactions Act, a valid digital signature has legal effect.
5. **Website certificates.** The certificate for a bank website binds the domain name to a public key and is signed by a certificate authority. The browser checks the chain and shows a padlock. A forged site without a valid certificate triggers a warning.
6. **Software updates and app stores.** Updates are signed by the vendor, and the device checks the signature before installing. This prevents fake updates that carry malware. The same check protects the apps you install on your phone.
7. **Blockchain and audit logs.** Each block of a ledger contains the hash of the previous block, so changing an old record changes every later hash. The same idea protects tamper-evident logs of a bank or a land-records office. Any edit is easy to detect and hard to hide.
8. **Evidence and duplicates.** A hash of a disk image or a file proves in court that the copy examined is identical to the original. Investigators also use hashes to find duplicate files quickly without comparing contents byte by byte. A matching digest is, for practical purposes, proof of equality.

## Chapter summary

- A cryptographic hash is preimage-, second-preimage- and collision-resistant with avalanche; MD5 and SHA-1 are broken, SHA-256 and SHA-3 are secure.
- Birthday bound: collisions appear after about 1.1774·√N messages: 23 people give 0.5073 for N = 365; a 64-bit digest falls after about 5,056,894,494 messages.
- HMAC(K, m) = H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m)) authenticates with a shared key; checked here against RFC 4231.
- Digital signatures (RSA-PSS, ECDSA, Ed25519) give authenticity, integrity and non-repudiation; reusing the ECDSA nonce reveals the key.
- X.509 certificates, CAs and chains of trust bind keys to identities; revocation by CRL/OCSP; Nepal's CCA licenses CAs under the ETA 2063.
- Passwords need salts and slow hashes (Argon2id, bcrypt).

## Practice

1. List the three security properties of a cryptographic hash.
2. Why is a collision easier to find than a preimage?
3. Approximately how many random 32-bit digests are needed for a 50% chance of a collision?
4. Why is H(key ‖ message) a poor MAC and what replaces it?
5. Write the HMAC formula.
6. What does a digital signature give that a MAC does not?
7. Describe the verification of a digital signature step by step.
8. What does an X.509 certificate contain?
9. Explain the chain of trust and two ways certificates can be revoked.
10. Why must passwords be salted and hashed with a slow function?

::: note Answers and worked solutions
**1.** Preimage resistance, second-preimage resistance, collision resistance.
**2.** Birthday paradox: among k messages there are about k²/2 pairs, so collisions need only about √N messages instead of N.
**3.** 1.1774 × 2¹⁶ = 1.1774 × 65,536 ≈ **77,162** digests.
**4.** Plain hashes built with the Merkle–Damgård structure allow length-extension; HMAC (two nested keyed hashes) is secure.
**5.** HMAC(K, m) = H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m)).
**6.** Non-repudiation: only the private-key holder could sign, whereas a MAC key is known to both parties.
**7.** Hash the received message; use the signer's public key on the signature (or verify the padded signature) and compare it with the hash; if equal, the message is intact and was signed by the key's owner.
**8.** Subject name and public key, issuer, validity dates, serial number, extensions (key usage, alternative names) and the issuer's signature.
**9.** Leaf certificate signed by an intermediate CA, signed by a root CA already trusted by the device. Revocation: CRL (signed list of revoked serials) or OCSP (online status query, with stapling).
**10.** The salt makes equal passwords produce different hashes and defeats rainbow tables; a slow function makes each guess expensive for an attacker with a stolen database.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a cryptographic hash function? State its security properties and explain the avalanche effect with an example.**

*Introduction.* A hash function H maps a message of any length to a fixed-length digest, for example 256 bits for SHA-256 (section 5.1, Figure 5.1).

1. **Easy to compute.** The digest of any message is computed quickly.
2. **Pre-image resistance.** Given a digest h, it is infeasible to find any message m with H(m) = h (a one-way function).
3. **Second pre-image resistance.** Given m1, it is infeasible to find a different m2 with the same digest.
4. **Collision resistance.** It is infeasible to find any two different messages with the same digest. By the birthday bound this costs about 2 to the power n/2 tries for an n-bit hash, so a hash needs at least 256 bits for 128-bit security.
5. **Avalanche effect.** A small change in the input changes about half of the output bits. SHA-256('abc') starts ba7816bf and SHA-256('abd') starts a52d159f; 122 of the 256 bits differ.

| Hash | Digest bits | Status |
|---|---|---|
| MD5 | 128 | Broken |
| SHA-1 | 160 | Broken (2017) |
| SHA-256 | 256 | Secure |

**Q2 (5 marks). Explain HMAC. Why is HMAC preferred to the construction H(K || m)?**

*Introduction.* A message authentication code (MAC) is a tag computed from the message and a shared secret key; it gives integrity and authentication but not non-repudiation (section 5.2, Figure 5.2).

1. **Construction.** HMAC(K, m) = H((K XOR opad) || H((K XOR ipad) || m)), where ipad is the byte 0x36 repeated and opad is 0x5C repeated.
2. **Use.** The sender sends m and the tag; the receiver recomputes the tag with the shared key and compares. A mismatch means the message or the key is wrong.
3. **Why not H(K || m).** For Merkle-Damgard hashes such as SHA-256, an attacker who knows H(K || m) and the length of the message can compute H(K || m || padding || extra) without knowing K (a **length-extension attack**). The nested HMAC form blocks this.
4. **Test vector.** HMAC-SHA256 with key 'Jefe' and message 'what do ya want for nothing?' is 5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843 (RFC 4231, test case 2).
5. **Limit.** Both sides hold the same key, so a MAC cannot prove to a third party which of them created a message; a signature is needed for that.

**Q3 (5 marks). Distinguish between a MAC and a digital signature.**

*Introduction.* Both detect changes to a message, but they use different keys and give different guarantees (sections 5.2 and 5.3, Figure 5.3).

1. **Key.** A MAC uses one shared secret key. A signature uses a key pair: a private key to sign and a public key to verify.
2. **Who can create.** Anyone with the shared key can create a valid MAC tag. Only the private-key owner can create a valid signature.
3. **Who can verify.** Only holders of the shared key can verify a MAC; anyone can verify a signature.
4. **Non-repudiation.** A signature gives it; a MAC does not.
5. **Speed.** A MAC is hundreds of times faster; signatures are slower.

| Point | MAC (HMAC) | Digital signature (RSA, ECDSA) |
|---|---|---|
| Keys | One shared key | Private and public key |
| Integrity | Yes | Yes |
| Authentication | Yes (shared group) | Yes (single signer) |
| Non-repudiation | No | Yes |
| Speed | Very fast | Slower |
| Typical use | API requests, TLS records | Certificates, software updates |

**Q4 (10 marks). Explain digital certificates and public-key infrastructure. Describe the structure of a certificate, how a browser validates a certificate chain, and how revocation works.**

*Introduction.* A public key by itself says nothing about who owns it, so an attacker could substitute his own key. A **digital certificate** binds a public key to a named owner and is signed by a trusted **certificate authority (CA)**. **Public-key infrastructure (PKI)** is the set of CAs, certificates, policies and software that make this trust work (section 5.4, Figure 5.4).

1. **Certificate contents (X.509).** Version, serial number, issuer name, validity dates (not before, not after), subject name, subject public key, extensions (for example allowed uses and alternative domain names) and the issuer's digital signature over all of these.
2. **Issuing.** The site generates a key pair and sends a certificate signing request. The CA checks control of the domain (or the organisation), then signs the certificate with its private key.
3. **Chain of trust.** The website certificate is signed by an intermediate CA, whose certificate is signed by a root CA. Roots are self-signed and are installed in the operating system or browser trust store.
4. **Validation by a browser.** (a) Check the dates. (b) Check that the name matches the address typed. (c) Verify the signature of each certificate with the public key of the next one up. (d) Check that the chain ends at a trusted root. (e) Check revocation. Any failure produces a warning.
5. **Revocation.** If a private key is stolen, the CA must cancel the certificate. A **certificate revocation list (CRL)** is a signed list of cancelled serial numbers; **OCSP** lets the browser ask a server about one certificate (OCSP stapling lets the site attach a fresh signed answer).
| Point | Certificate | CRL | OCSP |
|---|---|---|---|
| Purpose | Bind key to owner | List cancelled certificates | Query one certificate's status |
| Signed by | CA | CA | CA (responder) |
| Weakness | CA mistakes | Large, delayed | Privacy, extra delay |

*Conclusion.* PKI turns a public key into a trusted identity; TLS, signed software and e-government portals depend on it, and a careless CA is its main risk.

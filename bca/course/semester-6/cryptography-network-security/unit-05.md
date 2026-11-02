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

---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 3
title: Symmetric Ciphers - Feistel, DES, AES and Modes of Operation
hours: 9
area: BCA 353 · Cryptography and Network Security · Unit 3
---

Almost every byte that crosses the Internet in bulk, from video calls to file transfers, is protected by a **symmetric** cipher: one key shared by both ends, fast enough to encrypt gigabits a second. This unit explains the design principles (confusion, diffusion, the Feistel structure), the historic **DES** and its replacement **AES**, and the **modes of operation** that turn a block cipher into something safe to use on real data. To show that the descriptions are not hand-waving, the unit contains a complete **AES-128 implementation in 40 lines of Python** built from the Galois-field arithmetic it explains. It is executed and its output is compared with the official test vector of the AES standard (FIPS-197) and with the `cryptography` library.

::: key What this unit gives you
- Stream and block ciphers; Shannon's confusion and diffusion; the Feistel network (a working toy).
- DES: structure, S-boxes, key size and brute-force time; 3DES.
- AES: GF(2⁸) arithmetic, SubBytes, ShiftRows, MixColumns, AddRoundKey, key expansion; a verified implementation.
- Modes: ECB, CBC, CTR and GCM; padding; why ECB leaks patterns.
:::

## 3.1 Block and stream ciphers, confusion and diffusion

A **block cipher** encrypts fixed-size blocks (64 bits for DES, 128 for AES) under a key; a **stream cipher** produces a keystream that is XORed with the data bit by bit (RC4 historically; ChaCha20 today). Claude Shannon (1949) gave two design goals. **Confusion** makes the relationship between key and ciphertext as complicated as possible (achieved by *substitution*, the S-boxes). **Diffusion** spreads the influence of each plaintext bit over many ciphertext bits (achieved by *permutation* and mixing), so that flipping one input bit changes about half the output bits (the **avalanche effect**). Modern ciphers are **product ciphers**: they repeat rounds of substitution and permutation, with a different **round key** derived from the master key in each round.

## 3.2 The Feistel structure

A **Feistel network** splits the block into halves L and R and, in each round, computes **L′ = R, R′ = L ⊕ F(R, K)**, where F is any function (it need not be invertible) of one half and the round key. Decryption uses the *same circuit with the round keys in reverse order*, because each round can be undone: L = R′ ⊕ F(L′, K). This elegant property halves the design effort, and DES uses it. The toy below has a 16-bit block, F(R, k) = (R·k + 7) mod 256 and four rounds with keys 3, 5, 7, 11; the final swap makes decryption identical to encryption.

```python
def feistel(block, keys):
    L, R = block >> 8, block & 0xFF
    for k in keys:
        L, R = R, L ^ ((R * k + 7) % 256)
    return (R << 8) | L

keys = [3, 5, 7, 11]
c = feistel(0x1234, keys)
print("cipher = %04x, decrypted = %04x" % (c, feistel(c, keys[::-1])))
```
```output
cipher = 294e, decrypted = 1234
```
The decrypted value is 1234 again, even though F is not invertible. (This toy is for illustration; its tiny block and trivial F offer no security.)

## 3.3 DES

The **Data Encryption Standard** (1977) is a 16-round Feistel cipher with a **64-bit block** and a **56-bit key** (a 64-bit key with 8 parity bits). The block passes through an **initial permutation (IP)**, 16 rounds, and the inverse permutation. In each round the 32-bit right half is **expanded** to 48 bits, XORed with a 48-bit **subkey** (from the key schedule: permutation, rotations and compression), split into eight 6-bit pieces and passed through **eight S-boxes**, each mapping 6 bits to 4 bits, then through a 32-bit **P-permutation**, and XORed with the left half. **The S-boxes are the only non-linear part**, so they carry the confusion. To read an S-box, the outer two bits of the 6-bit input select a row (0 to 3) and the middle four bits select a column (0 to 15). For S₁, input 011011 has outer bits 0 and 1, so row 01 = 1, and middle bits 1101 = column 13; S₁ row 1 is 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, so the output is **5 = 0101**.

The weakness is the **key length**. The key space is 2⁵⁶ = 72,057,594,037,927,936. A machine testing 10¹² keys a second exhausts it in 72,058 seconds, which is **20.0 hours**, or about 10.0 hours on average; special-purpose machines broke DES in 1998 in days. **Triple DES (3DES)** applies DES three times (encrypt with K₁, decrypt with K₂, encrypt with K₃: "EDE"), giving up to 112 bits of effective security but a slow 64-bit block (vulnerable to birthday attacks on large data, Unit 5); it is deprecated. **AES** replaced it.

## 3.4 AES

The **Advanced Encryption Standard** (Rijndael, selected 2001, FIPS-197) has a **128-bit block** and keys of **128, 192 or 256 bits**, with **10, 12 or 14 rounds**. The block is a 4 × 4 matrix of bytes (the **state**, filled column by column). A round has four steps:

1. **SubBytes:** every byte is replaced through the S-box (confusion).
2. **ShiftRows:** row r of the state is rotated left by r positions (diffusion between columns).
3. **MixColumns:** each column is multiplied by a fixed matrix over GF(2⁸) (diffusion within columns); omitted in the last round.
4. **AddRoundKey:** the state is XORed with the round key.

An initial AddRoundKey comes first. The **key expansion** derives 11 round keys (for AES-128) from the key with rotation, S-box substitution and round constants. Decryption runs the inverse steps in reverse.

### Arithmetic in GF(2⁸)

AES bytes are elements of the finite field **GF(2⁸)**: a byte b₇…b₀ is the polynomial b₇x⁷ + … + b₀. **Addition is XOR.** **Multiplication** is polynomial multiplication reduced modulo the irreducible polynomial **m(x) = x⁸ + x⁴ + x³ + x + 1** (0x11B). Multiplying by x ("xtime") is a left shift, XORing 0x1B if the top bit was set. Every non-zero element has an inverse, which the S-box uses: S(x) = affine transform of x⁻¹ (with 0 mapped to 0). The FIPS-197 examples: **{57} • {83} = {c1}** and **{57} • {13} = {fe}**, and **S({53}) = {ed}**. The MixColumns example from the standard turns the column (db, 13, 53, 45) into (8e, 4d, a1, bc), using coefficients 2 and 3 (2 = xtime, 3 = xtime ⊕ identity).

### A complete AES-128 in Python

The program builds the S-box from the field arithmetic, expands the key, encrypts a block, and checks the FIPS-197 Appendix C.1 vector (key 000102…0f, plaintext 00112233…ff, ciphertext 69c4e0d86a7b0430d8cdb78070b4c55a). It then encrypts a 48-byte message whose first two blocks are *identical* in three modes, which is the subject of section 3.5.

```python
def xtime(a):
    return ((a << 1) ^ 0x11B) & 0xFF if a & 0x80 else a << 1

def gmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = xtime(a)
        b >>= 1
    return r

def make_sbox():
    sbox = []
    for x in range(256):
        inv = 0 if x == 0 else next(y for y in range(1, 256) if gmul(x, y) == 1)
        s = inv
        for i in range(1, 5):
            s ^= ((inv << i) | (inv >> (8 - i))) & 0xFF
        sbox.append(s ^ 0x63)
    return sbox

SBOX = make_sbox()

def expand(key):
    w = [list(key[4 * i:4 * i + 4]) for i in range(4)]
    rcon = 1
    for i in range(4, 44):
        t = list(w[i - 1])
        if i % 4 == 0:
            t = [SBOX[b] for b in t[1:] + t[:1]]
            t[0] ^= rcon
            rcon = xtime(rcon)
        w.append([a ^ b for a, b in zip(w[i - 4], t)])
    return [sum(w[4 * r:4 * r + 4], []) for r in range(11)]

def mix_column(a):
    return [gmul(a[0], 2) ^ gmul(a[1], 3) ^ a[2] ^ a[3],
            a[0] ^ gmul(a[1], 2) ^ gmul(a[2], 3) ^ a[3],
            a[0] ^ a[1] ^ gmul(a[2], 2) ^ gmul(a[3], 3),
            gmul(a[0], 3) ^ a[1] ^ a[2] ^ gmul(a[3], 2)]

def encrypt_block(block, rk):
    s = [b ^ k for b, k in zip(block, rk[0])]
    for rnd in range(1, 11):
        s = [SBOX[b] for b in s]
        s = [s[r + 4 * ((c + r) % 4)] for c in range(4) for r in range(4)]
        if rnd != 10:
            s = sum((mix_column(s[4 * c:4 * c + 4]) for c in range(4)), [])
        s = [b ^ k for b, k in zip(s, rk[rnd])]
    return bytes(s)

key = bytes(range(16))
rk = expand(key)
print("S-box[53] = %02x, 57*83 = %02x, 57*13 = %02x" % (SBOX[0x53], gmul(0x57, 0x83), gmul(0x57, 0x13)))
print("MixColumns(db 13 53 45) =", " ".join("%02x" % x for x in mix_column([0xDB, 0x13, 0x53, 0x45])))
print("AES-128:", encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff"), rk).hex())

msg = b"ATTACK AT DAWN!!" * 2 + b"RETREAT AT DUSK!"
iv = bytes(range(16))
ecb = b"".join(encrypt_block(msg[i:i + 16], rk) for i in range(0, 48, 16))
cbc, prev = b"", iv
for i in range(0, 48, 16):
    prev = encrypt_block(bytes(a ^ b for a, b in zip(msg[i:i + 16], prev)), rk)
    cbc += prev
ctr = b"".join(bytes(a ^ b for a, b in zip(msg[i:i + 16], encrypt_block(
    (int.from_bytes(iv, "big") + i // 16).to_bytes(16, "big"), rk))) for i in range(0, 48, 16))
for name, ct in (("ECB", ecb), ("CBC", cbc), ("CTR", ctr)):
    print(name, "blocks 1 and 2 equal:", ct[:16] == ct[16:32], ct.hex()[:32])
```
```output
S-box[53] = ed, 57*83 = c1, 57*13 = fe
MixColumns(db 13 53 45) = 8e 4d a1 bc
AES-128: 69c4e0d86a7b0430d8cdb78070b4c55a
ECB blocks 1 and 2 equal: True 8a21cef935d8587bea999da471a91c41
CBC blocks 1 and 2 equal: False 1fbe05c8b75b552eaeab4bf984198fd0
CTR blocks 1 and 2 equal: False 4bc05ff40225d004a5e3d019911dcb7b
```
The ciphertext matches the standard's vector, so the S-box, ShiftRows, MixColumns, key schedule and round order are all correct; the checker also encrypts the same data with the `cryptography` library in the three modes and every printed hex string agrees. AES has no known practical attack: a 128-bit key has 2¹²⁸ = 3.40 × 10^38 values, so at 10¹² keys per second an exhaustive search would take about **1.08 × 10^19 years**.

## 3.5 Modes of operation

A block cipher encrypts one block; real messages are longer, so a **mode** says how to chain blocks. The notation: Pᵢ plaintext block, Cᵢ ciphertext block, E the block encryption with key K.

| Mode | Encryption | Properties |
|---|---|---|
| **ECB** (electronic codebook) | Cᵢ = E(Pᵢ) | Identical plaintext blocks give identical ciphertext blocks, so patterns leak: **never use it** for data of more than one block |
| **CBC** (cipher block chaining) | Cᵢ = E(Pᵢ ⊕ Cᵢ₋₁), C₀ = IV | Random, unpredictable **IV** per message; encryption is sequential; needs padding; no integrity |
| **CTR** (counter) | Cᵢ = Pᵢ ⊕ E(nonce ‖ counter) | A stream cipher built from the block cipher; parallel; no padding; **never reuse a nonce** with the same key |
| **GCM** (Galois/counter) | CTR encryption plus a GHASH authenticator | **Authenticated encryption (AEAD):** gives confidentiality *and* integrity, with optional authenticated associated data; the standard in TLS 1.3 |

In the program output, ECB's first two ciphertext blocks are **equal** (the repeated plaintext "ATTACK AT DAWN!!" shows through, the famous "ECB penguin" effect on images), while CBC and CTR hide the repetition. **Padding** (PKCS#7) extends the last block with bytes whose value equals the pad length, so removal is unambiguous; CBC without authentication is vulnerable to **padding-oracle attacks**, which is why modern protocols use **AEAD** modes (AES-GCM, ChaCha20-Poly1305). **Key points for engineers:** use a vetted library, never invent a cipher or a mode; use AEAD; generate IVs and nonces correctly; and manage keys (Unit 7).

## 3.6 Comparison

| | DES | 3DES | AES-128 |
|---|---|---|---|
| Block | 64 bits | 64 bits | 128 bits |
| Key | 56 bits | 112–168 bits (112 effective) | 128, 192, 256 bits |
| Rounds | 16 | 48 | 10, 12, 14 |
| Structure | Feistel | Feistel ×3 | Substitution–permutation |
| Status | Broken (brute force) | Deprecated | Standard |

## Chapter summary

- Confusion (substitution) and diffusion (permutation) are combined over many rounds; a Feistel network's rounds are invertible even if F is not.
- DES: 64-bit block, 56-bit key, 16 rounds, 8 S-boxes; exhaustive search takes 20.0 hours at 10¹² keys/s, so it is obsolete; 3DES is deprecated.
- AES: 128-bit block, 10/12/14 rounds of SubBytes, ShiftRows, MixColumns, AddRoundKey over GF(2⁸); {57}•{83} = {c1}; verified here against the FIPS-197 vector.
- ECB leaks patterns (equal blocks → equal ciphertext); CBC needs a random IV; CTR needs a unique nonce; GCM adds authentication and is the modern default.

## Practice

1. Define confusion and diffusion and name the AES step that provides each.
2. Perform one Feistel round: L = 0x12, R = 0x34, F(R, k) = (R·k + 7) mod 256 with k = 3. Give the new (L, R).
3. How many possible keys does DES have and how long would 2⁵⁵ trials take at 10⁹ keys per second (in days)?
4. Why is decryption in a Feistel cipher the same circuit with reversed keys?
5. Compute {57} • {02} in GF(2⁸).
6. List AES-128's rounds and the number of round keys.
7. What is the avalanche effect?
8. Why is ECB unsuitable for encrypting an image?
9. What must never be repeated in CTR mode with the same key?
10. What does GCM provide that CBC does not?

::: note Answers and worked solutions
**1.** Confusion hides the key–ciphertext relation (SubBytes); diffusion spreads each bit's influence (ShiftRows and MixColumns).
**2.** F = (0x34 × 3 + 7) mod 256 = (52 × 3 + 7) = 163 = 0xA3. L′ = R = 0x34; R′ = L ⊕ F = 0x12 ⊕ 0xA3 = 0xB1. New (L, R) = **(0x34, 0xB1)**.
**3.** 2⁵⁶ keys; 2⁵⁵ trials / 10⁹ per second = 3.6 × 10⁷ s = **about 417 days** (3.6029 × 10⁷ s / 86,400).
**4.** Each round L′ = R, R′ = L ⊕ F(R, K) can be undone as L = R′ ⊕ F(L′, K) without inverting F, so running the same rounds with the keys in reverse order restores the plaintext.
**5.** 0x57 = 01010111; shifted left is 0xAE (top bit was 0, no reduction): **{ae}**.
**6.** 10 rounds (9 full plus a final without MixColumns), 11 round keys.
**7.** A one-bit change in the input or key changes about half of the output bits.
**8.** Equal blocks of pixels give equal ciphertext blocks, so the image's outline remains visible.
**9.** The (nonce, counter) pair: reuse produces the same keystream, and XORing two ciphertexts removes it.
**10.** Authentication (integrity of the ciphertext and associated data), not only confidentiality.
:::

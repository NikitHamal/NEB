---
subject: Cryptography and Network Security
grade: BCA Semester 6
unit: 1
title: Security Goals and Classical Ciphers
hours: 6
area: BCA 353 · Cryptography and Network Security · Unit 1
---

When Julius Caesar shifted every letter of a message by three places he was practising **cryptography**: transforming a message so that only the intended reader can understand it. Two thousand years later the same two ideas, a *method* and a *secret*, protect every bank transfer and every chat message. This unit sets out what security is trying to achieve, the vocabulary of attacks, and then studies the **classical ciphers** (Caesar, Vigenère, Playfair, Hill and rail fence). They are no longer secure, but they teach the vocabulary, and each is broken by an instructive method. All the ciphertexts in this unit were produced by the programs shown, executed, and compared with independently known values (the textbook examples) and with a second implementation.

::: key What this unit gives you
- Security services and attack types; Kerckhoffs's principle; cryptanalysis models.
- Substitution and transposition ciphers: Caesar, affine, Vigenère, Playfair, Hill (with matrix inverse mod 26), rail fence.
- Frequency analysis and why the one-time pad is perfectly secret.
- Executed programs with checked outputs.
:::

## 1.1 Security goals and attacks

The classical **security services** (ITU X.800): **confidentiality** (only authorised parties can read data), **integrity** (data are not altered undetected), **authentication** (the sender and the data's origin are genuine), **non-repudiation** (the sender cannot deny sending) and **availability** (the service works when needed), plus **access control**. **Attacks** are classified as **passive** (eavesdropping, traffic analysis: the data are not changed, so they are hard to *detect*, easier to *prevent* by encryption) and **active** (masquerade, replay, modification of messages, denial of service: easier to detect, harder to prevent).

Terms: **plaintext** is the readable message; **ciphertext** the scrambled form; **encryption** converts plaintext to ciphertext and **decryption** reverses it using a **key**; the **algorithm** (cipher) is the method; **cryptanalysis** is breaking a cipher without the key; **cryptology** covers both. **Kerckhoffs's principle** says the security of a system must rest only on the secrecy of the *key*, not on keeping the algorithm secret, because algorithms leak and secrecy through obscurity fails: every cipher in this book is public. Attack models by the attacker's power: **ciphertext-only**, **known-plaintext**, **chosen-plaintext**, **chosen-ciphertext**. A cipher is **computationally secure** if breaking it needs more resources than the attacker has, and **unconditionally secure** only if no amount of computation can break it (the one-time pad, below).

Two families of classical technique: **substitution** replaces letters with other letters or symbols; **transposition** rearranges the positions of letters. Modern ciphers combine both, many times (Unit 3).

## 1.2 Caesar, affine and Vigenère ciphers

The **Caesar cipher** shifts each letter by k: C = (P + k) mod 26 (A = 0 … Z = 25); decryption is P = (C − k) mod 26. With k = 3, ATTACKATDAWN becomes DWWDFNDWGDZQ. It has only 25 useful keys, so an attacker simply tries all (**brute force**). The **affine cipher** is C = (aP + b) mod 26, where a must be coprime with 26 (a has an inverse mod 26, Unit 2): there are 12 × 26 = 312 keys, still tiny, and it falls to frequency analysis.

All single-alphabet substitutions keep the letter frequencies of the language: in English **E, T, A, O, N** are the most common letters, so the commonest ciphertext letter probably stands for E. The **Vigenère cipher** defeats this by using a keyword to apply a *different* Caesar shift to successive letters: with keyword LEMON (shifts 11, 4, 12, 14, 13) repeated along the message, the same plaintext letter encrypts differently at different positions. It resisted analysis for 300 years until Kasiski (1863) and Friedman showed that repeated ciphertext fragments reveal the **keyword length** and then each position is a Caesar cipher solved by frequency analysis.

**Rail fence** is a transposition: write the message in a zigzag across n rails and read the rails row by row. Its key is n only, so it is easily broken.

## 1.3 Playfair

The **Playfair cipher** (Wheatstone, 1854) encrypts *pairs* of letters using a 5 × 5 square built from a keyword (I and J share a cell). To encrypt a pair (a, b): (1) if the letters are in the **same row**, replace each by the letter to its right (wrapping around); (2) if in the **same column**, by the letter below; (3) otherwise form the rectangle and replace each by the letter in *its own row* and the *other's column*. Repeated letters in a pair are separated by a filler X, and an odd final letter is padded with X. Digram substitution flattens the single-letter frequencies, but 600 digrams still have a recognisable distribution, so Playfair falls to known-plaintext or statistical attacks on ciphertexts of a few hundred letters.

## 1.4 The Hill cipher

The **Hill cipher** (Hill, 1929) multiplies blocks of n letters by an n × n key matrix K mod 26: **C = K·P mod 26**, and decryption is **P = K⁻¹·C mod 26**, which exists only if **gcd(det K, 26) = 1**. It is a *linear* cipher, so a known-plaintext attack with n plaintext–ciphertext blocks reveals K by solving linear equations; it was the first cipher to use algebra and the ancestor of the diffusion step in modern ciphers.

## 1.5 The programs

The following program implements Caesar, Vigenère (encrypting and decrypting), rail fence and Playfair with the classic textbook keys, and the Hill cipher with a 3 × 3 key using sympy for the modular matrix inverse. The expected results for the first, second, fourth and Playfair lines are the well-known textbook values, and the checker also recomputes everything with independent code.

```python
import string
import sympy

A = string.ascii_uppercase

def caesar(t, k):
    return "".join(A[(A.index(c) + k) % 26] for c in t)

def vigenere(t, key, sign=1):
    return "".join(A[(A.index(c) + sign * A.index(key[i % len(key)])) % 26]
                   for i, c in enumerate(t))

def rail(t, n):
    rows = [""] * n
    r, d = 0, 1
    for c in t:
        rows[r] += c
        if r == 0:
            d = 1
        elif r == n - 1:
            d = -1
        r += d
    return "".join(rows)

def playfair(text, key):
    sq = []
    for c in (key + A).replace("J", "I"):
        if c not in sq:
            sq.append(c)
    pos = {c: divmod(i, 5) for i, c in enumerate(sq)}
    pairs, i = [], 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"
        if a == b:
            b = "X"
            i += 1
        else:
            i += 2
        pairs.append((a, b))
    out = ""
    for a, b in pairs:
        (r1, c1), (r2, c2) = pos[a], pos[b]
        if r1 == r2:
            out += sq[r1 * 5 + (c1 + 1) % 5] + sq[r2 * 5 + (c2 + 1) % 5]
        elif c1 == c2:
            out += sq[((r1 + 1) % 5) * 5 + c1] + sq[((r2 + 1) % 5) * 5 + c2]
        else:
            out += sq[r1 * 5 + c2] + sq[r2 * 5 + c1]
    return " ".join("".join(sq[i:i + 5]) for i in range(0, 25, 5)), out

print(caesar("ATTACKATDAWN", 3))
print(vigenere("ATTACKATDAWN", "LEMON"))
print(vigenere("LXFOPVEFRNHR", "LEMON", -1))
print(rail("WEAREDISCOVEREDFLEEATONCE", 3))
square, ct = playfair("HIDETHEGOLDINTHETREESTUMP", "PLAYFAIREXAMPLE")
print(square)
print(ct)

K = sympy.Matrix([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
Kinv = K.inv_mod(26)
c = (K * sympy.Matrix([0, 2, 19])).applyfunc(lambda x: x % 26)
print("det =", K.det(), "mod 26 =", K.det() % 26)
print("inverse mod 26 =", Kinv.tolist())
print("ACT ->", "".join(A[int(x)] for x in c))
print("K*Kinv mod 26 =", (K * Kinv).applyfunc(lambda x: x % 26).tolist())
```
```output
DWWDFNDWGDZQ
LXFOPVEFRNHR
ATTACKATDAWN
WECRLTEERDSOEEFEAOCAIVDEN
PLAYF IREXM BCDGH KNOQS TUVWZ
BMODZBXDNABEKUDMUIXMMOUVIF
det = 441 mod 26 = 25
inverse mod 26 = [[8, 5, 10], [21, 8, 21], [21, 12, 8]]
ACT -> POH
K*Kinv mod 26 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
```
Reading the output: the Vigenère line reproduces the textbook ciphertext LXFOPVEFRNHR and decrypts back; the rail-fence line is the textbook WECRLTEERDSOEEFEAOCAIVDEN for three rails; the Playfair square from the key PLAYFAIR EXAMPLE and the digram ciphertext match the classic example. For Hill, det K = 441 and 441 mod 26 = 25, which is coprime with 26 (the only common factors of 26 are 2 and 13), so K⁻¹ exists: it is printed, and multiplying back gives the identity matrix. The plaintext ACT is the vector (0, 2, 19); the ciphertext is POH.

## 1.6 Breaking classical ciphers

| Cipher | Key space | Weakness | Attack |
|---|---|---|---|
| Caesar | 25 | Tiny key space | Try all shifts |
| Affine | 312 | Small key space, keeps frequencies | Brute force or frequency analysis |
| Mono-alphabetic substitution | 26! ≈ 4 × 10²⁶ | Letter frequencies survive | Frequency analysis, common words |
| Vigenère | 26ᵐ for a keyword of length m | Periodic key | Kasiski/Friedman, then Caesar on each column |
| Playfair | 25! | Digram frequencies survive | Digram statistics, known plaintext |
| Hill (n × n) | Large | Linear | Known plaintext: solve for K |
| Rail fence / transposition | Few | Letter frequencies unchanged | Try rail counts; anagramming |

The brute-force numbers show *why* key size matters but also that a large key space alone is not enough: a mono-alphabetic substitution has more than 10²⁶ keys and still falls in minutes because the **structure** of the language leaks through.

## 1.7 The one-time pad

Using a random key as long as the message, used **once**, and XORing (or adding mod 26) gives the **one-time pad** (Vernam), which Shannon proved is **perfectly secret**: for every ciphertext, every plaintext of the same length is equally likely, so the ciphertext carries no information about the plaintext. It is impractical because the key must be as long as the data, truly random, shared securely and *never reused*: if two messages share a pad, XORing the two ciphertexts removes the pad and exposes the XOR of the plaintexts (the **two-time pad** mistake, behind several real breaks). Practical stream ciphers (Unit 3) imitate the pad with a short key and a pseudo-random generator, giving computational rather than perfect security.

## Chapter summary

- Security services are confidentiality, integrity, authentication, non-repudiation and availability; attacks are passive or active; security must rest on the key (Kerckhoffs).
- Substitution ciphers (Caesar, affine, Vigenère, Playfair, Hill) and transposition ciphers (rail fence) are all breakable by exploiting language structure or linearity.
- Hill encryption is C = K·P mod 26 and needs gcd(det K, 26) = 1; here det K = 441 ≡ 25 (mod 26), and ACT encrypts to POH.
- A one-time pad is perfectly secret but impractical; key reuse destroys it.

## Practice

1. List the five security services and give an attack against each.
2. Encrypt "NEPAL" with a Caesar shift of 5.
3. Why can a Caesar cipher be broken by hand in minutes?
4. For the affine cipher C = (5P + 8) mod 26, encrypt the letter D (P = 3).
5. How many keys does the affine cipher have, and why can a not be 13?
6. Explain how repeated letters in the plaintext affect Playfair pairs.
7. Encrypt "HELP" with the Hill key [[3, 3], [2, 5]] mod 26 (blocks HE and LP).
8. When is a Hill key matrix invalid?
9. Why is the one-time pad impractical, and what happens if the key is reused?
10. State Kerckhoffs's principle.

::: note Answers and worked solutions
**1.** Confidentiality (eavesdropping), integrity (message modification), authentication (masquerade), non-repudiation (denying a sent order), availability (denial of service).
**2.** N=13, E=4, P=15, A=0, L=11 plus 5: 18, 9, 20, 5, 16 → **SJUFQ**.
**3.** There are only 25 possible keys, so trying every shift (or finding the commonest letter) reveals the plaintext.
**4.** 5 × 3 + 8 = 23, so D becomes **X**.
**5.** φ(26) = 12 values of a coprime with 26 times 26 values of b = **312** keys; a = 13 shares a factor with 26, so it has no inverse and decryption would be ambiguous.
**6.** A double letter within a pair (LL) is split by inserting X (LX LO ...) so that a pair never contains the same letter twice.
**7.** HE = (7, 4): 3·7 + 3·4 = 33 mod 26 = 7 (H); 2·7 + 5·4 = 34 mod 26 = 8 (I): **HI**. LP = (11, 15): 3·11 + 3·15 = 78 mod 26 = 0 (A); 2·11 + 5·15 = 97 mod 26 = 19 (T): **AT**. Ciphertext **HIAT**.
**8.** When gcd(det K, 26) ≠ 1 (the determinant is even or a multiple of 13), because K then has no inverse mod 26.
**9.** The key must be as long as the message, truly random and shared in secret; reusing it lets an attacker XOR two ciphertexts and cancel the key, exposing the XOR of the plaintexts.
**10.** Security should depend only on the secrecy of the key, not of the algorithm.
:::

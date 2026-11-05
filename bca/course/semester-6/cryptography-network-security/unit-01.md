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

## 1.8 Seeing the ciphers: machines, frequencies and keyspaces

Classical ciphers look like word puzzles on paper, but they were once real devices, and the same few ideas (substitute, rearrange, hide the pattern, enlarge the key) explain all of them. The first plate shows four historical devices. The figures then show the attack model, the Caesar shift, the letter frequencies that break simple substitution, the rail-fence zigzag and the size of each cipher's key space.

```photogrid label="1.1" cols="4" ratio="1.0" caption="Ciphers as objects. (a) A scytale: a strip of leather or paper is wound around a rod, the message is written along the rod, and the unwound strip shows scrambled letters. Only a rod of the same width brings the text back. This is a transposition cipher. (b) The Alberti cipher disk of the 1460s: an inner ring of lower-case letters turns inside an outer ring of capitals, so every turn of the disk gives a new substitution alphabet. (c) A three-rotor Enigma machine: every key press moves the rotors and changes the substitution for the next letter. (d) The Lorenz SZ42 teleprinter cipher attachment (the German Tunny), whose twelve wheels produced a long stream of key bits that were combined with the message letter by letter."
@ photo id="crypto353/scytale" cap="Scytale (transposition)"
fit 1.0
focus 0.5 0.5
call 0.5 0.9 0.5 0.62 "wooden rod"
@ photo id="crypto353/alberti" cap="Alberti cipher disk"
fit 1.0
focus 0.5 0.5
call 0.5 0.9 0.5 0.8 "outer ring: plaintext"
@ photo id="bca401/enigma" cap="Enigma rotor machine"
fit 1.0
focus 0.5 0.5
@ photo id="crypto353/lorenz" cap="Lorenz SZ42 (Tunny)"
fit 1.0
focus 0.3 0.5
call 0.35 0.9 0.28 0.55 "key wheels"
```

```svgfig label="1.1" caption="The attack model. Alice sends a message to Bob over an open channel. Eve only listens (a passive attack on confidentiality). Mallory sits in the channel and can change, replay or block messages (active attacks on integrity, authentication and availability). Cryptography puts the cipher and the key at the two ends so that what travels on the channel is useless to Eve and any change by Mallory is detected."
f = Fig(580, 230)
f.box(10, 70, 110, 60, "Alice\nplaintext P", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(460, 70, 110, 60, "Bob\nplaintext P", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(140, 82, 90, 36, "Encrypt\nkey K", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(350, 82, 90, 36, "Decrypt\nkey K", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(120, 100), (140, 100)], color=SLATE); f.arrow([(230, 100), (350, 100)], color=SLATE, label="ciphertext C on an open channel", lpos=(290, 136))
f.arrow([(440, 100), (460, 100)], color=SLATE)
f.box(150, 172, 130, 44, "Eve: eavesdrops\n(passive)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(215, 172), (270, 104)], color=AMBER, dash=True)
f.box(320, 8, 150, 44, "Mallory: modifies, replays,\nblocks (active)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(395, 52), (380, 90)], color=RED, dash=True)
f.text(480, 190, "Services protected:", size=10.5, color=NAVY, bold=True)
f.text(480, 206, "confidentiality, integrity,", size=10, color=SLATE)
f.text(480, 220, "authentication, availability", size=10, color=SLATE)
```

```svgfig label="1.2" caption="A Caesar shift of 3 drawn as two sliding alphabets. The lower alphabet is the upper one moved three places to the left, so A is written as D, T as W, C as F and so on. ATTACKATDAWN becomes DWWDFNDWGDZQ, and decrypting is the same slide in the opposite direction. Because there are only 25 useful shifts, an attacker can try them all in a minute."
f = Fig(580, 150)
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
f.text(10, 16, "Plain", size=10, color=NAVY, bold=True, anchor="start"); f.text(10, 74, "Cipher", size=10, color=RED, bold=True, anchor="start")
for i, ch in enumerate(A):
    x = 52 + i * 20
    f.box(x, 24, 18, 22, ch, fill=BLUE, stroke=NAVY, size=10, bold=True, r=3, sw=1)
    f.box(x, 58, 18, 22, A[(i + 3) % 26], fill=ROSE, stroke=RED, size=10, bold=True, r=3, sw=1)
    f.line(x + 9, 46, x + 9, 58, color="#94a3b8", sw=0.8)
f.text(290, 108, "ATTACKATDAWN  with key 3  gives  DWWDFNDWGDZQ", size=12, color=NAVY, bold=True)
f.text(290, 128, "C = (P + 3) mod 26        P = (C - 3) mod 26        only 25 keys", size=10.5, color=SLATE)
```

```svgfig label="1.3" caption="Letter frequencies in English text (percent, from the standard published table). E is far ahead at 12.7, then T 9.1, A 8.2, O 7.5, I 7.0, N 6.7. A Caesar, affine or any single-alphabet substitution only renames the bars, so the tallest ciphertext bar probably stands for E. The Vigenere cipher flattens the picture by using several alphabets in turn. The sum of the squared frequencies is about 0.0655 for English and 1/26 = 0.0385 for random letters, which is the index of coincidence used to guess key length."
f = Fig(580, 200)
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
fr = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]
base = 168
for i, v in enumerate(fr):
    x = 12 + i * 21.8
    h = v * 10.5
    top = v > 6
    f.box(x, base - h, 17, h, "", fill=("#fde68a" if top else BLUE), stroke=(AMBER if top else NAVY), sw=1, r=2)
    f.text(x + 8.5, base + 14, A[i], size=10, color=NAVY, bold=True)
    if v > 6: f.text(x + 8.5, base - h - 5, f"{v:.1f}", size=8.5, color=AMBER, bold=True)
f.line(8, base, 576, base, color=SLATE, sw=1)
f.text(330, 40, "Six commonest letters (amber): E T A O I N", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(330, 58, "make about half of ordinary English text", size=10, color=SLATE, anchor="start")
```

```svgfig label="1.4" caption="Rail fence with three rails for WEAREDISCOVEREDFLEEATONCE. The letters are written in a zigzag down and up the rails (top rail W, E, C, R, L, T, E; middle rail E, R, D, S, O, E, E, F, E, A, O, C; bottom rail A, I, V, D, E, N). Reading the rails one after another gives WECRLTEERDSOEEFEAOCAIVDEN. Only the number of rails is secret, so an attacker tries 2, 3, 4 and so on."
f = Fig(580, 150)
msg = "WEAREDISCOVEREDFLEEATONCE"
n = 3
rail = [min(k % 4, 4 - k % 4) for k in range(len(msg))]
cols = ["#fde68a", BLUE, MINT]; sts = [AMBER, NAVY, TEAL]
pts = []
for i, ch in enumerate(msg):
    x = 14 + i * 22.4; y = 20 + rail[i] * 36
    pts.append((x + 9, y + 11))
for i in range(len(pts) - 1):
    f.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color="#cbd5e1", sw=1)
for i, ch in enumerate(msg):
    x = 14 + i * 22.4; y = 20 + rail[i] * 36
    f.box(x, y, 18, 22, ch, fill=cols[rail[i]], stroke=sts[rail[i]], size=10.5, bold=True, r=3, sw=1)
rows = ["".join(msg[i] for i in range(len(msg)) if rail[i] == r) for r in range(3)]
f.text(290, 136, "Read rail by rail:  " + "  ".join(rows), size=10.5, color=NAVY, bold=True)
```

```photogrid label="1.2" cols="2" ratio="1.25" caption="Breaking ciphers is a matter of counting. (a) A reconstructed Turing-Welchman Bombe at Bletchley Park: each drum bank tested one possible Enigma setting against a guessed piece of plaintext (a crib), so the machine searched a key space mechanically. (b) The key space of each cipher in bits (log base 2 of the number of keys): Caesar 4.6, affine 8.3, a five-letter Vigenere key 23.5, a general substitution table 88.4, AES-128 128. A search of 2 to the power 40 keys is easy today; 2 to the power 128 is impossible."
@ photo id="crypto353/bombe" cap="Bombe: a key-search machine"
fit 1.25
focus 0.5 0.55
call 0.5 0.9 0.5 0.62 "banks of rotating drums"
@ svg cap="Key space in bits"
f = Fig(340, 272)
rows = [("Caesar", 4.64, "25"), ("Affine", 8.29, "312"), ("Vigenere, 5 letters", 23.50, "26^5"), ("Vigenere, 10 letters", 47.00, "26^10"), ("Substitution table", 88.38, "26!"), ("AES-128", 128.0, "2^128")]
for i, (nm, b, k) in enumerate(rows):
    y = 14 + i * 40
    f.text(4, y + 5, nm, size=12, color=NAVY, bold=True, anchor="start")
    w = b / 128 * 330
    f.box(4, y + 12, max(w, 6), 14, "", fill=(MINT if b > 80 else SAND if b > 20 else ROSE), stroke=(TEAL if b > 80 else AMBER if b > 20 else RED), sw=1, r=3)
    f.text(10 + w if w < 250 else 330, y + 38 if w >= 250 else y + 24, f"{b:.1f} bits  ({k} keys)", size=12, color=SLATE, bold=True, anchor="start" if w < 250 else "end")
```

### 1.8.1 Eight places where cryptography protects daily life in Nepal

1. **Mobile and internet banking.** When a customer logs in to a bank app or pays through ConnectIPS, the data travel inside an encrypted TLS session. An eavesdropper on the same Wi-Fi sees only ciphertext. The lessons of this unit (key, cipher, attack) are the ancestors of that protection.
2. **QR and wallet payments.** Fonepay QR codes and wallet apps send a payment request that must not be altered on the way. The apps protect the request with encryption and with message checks, so that changing an amount from Rs 100 to Rs 1,000 is detected. This is integrity, one of the five services in section 1.1.
3. **Passwords and OTP codes.** A well-built system never stores your password in plain form. It stores a scrambled value, so that a stolen database does not reveal the password. One-time codes sent to your phone are a modern, short-lived cousin of the one-time pad idea.
4. **Government portals.** Services such as the Nagarik App, tax filing and the passport system carry citizens' personal records. Encryption keeps the records private on the network, and login checks prove that the user is who they claim to be (authentication).
5. **Exam and result systems.** A university must keep question papers secret until the exam hour and must stop anyone changing marks afterwards. Encryption protects files in storage and in transfer, and checks on the files detect tampering. This shows confidentiality and integrity working together.
6. **Messaging and email.** Chat apps use end-to-end encryption, so that even the company running the server cannot read the messages. This idea goes back to the simple wish of Caesar to keep a message from the messenger himself.
7. **Mobile SIM and phone locks.** The SIM card holds a secret key and proves to the network that the phone belongs to a real subscriber. Phone storage is also encrypted, so a lost phone does not give away its photos and chats.
8. **Wi-Fi at home and campus.** A WPA2 or WPA3 password does two jobs: it controls who may join (authentication) and it derives the keys that encrypt every packet. An open network without encryption allows any neighbour with a laptop to act as Eve.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the five security services and the main types of attack against them.**

*Introduction.* Information security aims to protect data in storage and in transit. The ITU X.800 standard groups the aims into five services, and attacks are grouped by what the attacker does to the message (section 1.1, Figure 1.1).

1. **Confidentiality** means only authorised parties can read the data. Eavesdropping on an open Wi-Fi network defeats it.
2. **Integrity** means data are not changed without detection. A modified payment amount is an attack on integrity.
3. **Authentication** proves who sent the data. Masquerade, where Mallory pretends to be the bank, defeats it.
4. **Non-repudiation** stops a sender from denying a message, as when a customer denies sending a transfer order.
5. **Availability** keeps the service usable. A denial-of-service flood breaks it.

Attacks are **passive** (release of message contents and traffic analysis, no change to the data, hard to detect, so we prevent them by encryption) or **active** (modification, replay, masquerade and denial of service, easier to detect, so we add checks). Following **Kerckhoffs's principle**, the security of a system must rest only on the secrecy of the key, never on the secrecy of the method.

| Service | Typical attack | Typical defence |
|---|---|---|
| Confidentiality | Eavesdropping | Encryption |
| Integrity | Modification, replay | MAC, hash, sequence numbers |
| Authentication | Masquerade | Passwords, certificates |
| Non-repudiation | Denial of an order | Digital signature |
| Availability | Flooding | Filtering, redundancy |

**Q2 (5 marks). Encrypt ATTACKATDAWN with the Vigenere key LEMON and explain how a Vigenere cipher is broken.**

*Introduction.* The Vigenere cipher uses the letters of a keyword as a series of Caesar shifts, so one plaintext letter can become different ciphertext letters (section 1.2).

1. **Rule.** Write the key under the message, repeating it, and add the numbers (A = 0 to Z = 25) modulo 26.
2. **Working.** A + L = L, T + E = X, T + M = F, A + O = O, C + N = P, K + L = V, A + E = E, T + M = F, D + O = R, A + N = N, W + L = H, N + E = R.
3. **Ciphertext.** LXFOPVEFRNHR. Note that the three Ts become X, F and F, so the frequencies are flattened.
4. **Decryption.** Subtract the same key letters, giving back ATTACKATDAWN.
5. **Breaking it.** First find the key length m by Kasiski examination (repeated groups of letters in the ciphertext lie at distances that are multiples of m) or by the index of coincidence (about 0.0655 for English, about 0.0385 for random letters). Then split the text into m groups. Each group is an ordinary Caesar cipher and falls to frequency analysis, where the most common letter stands for E.

Strength depends on the key length: a 5-letter key gives 26 to the power 5 = 11,881,376 keys, but the attack above never needs to try them all.

**Q3 (10 marks). Describe the classical substitution and transposition ciphers. Explain how each can be broken and why none is used today.**

*Introduction.* Before computers, messages were protected by hand ciphers that either **replace** letters (substitution) or **rearrange** them (transposition). They are the ancestors of modern block ciphers, which repeat both operations many times, and studying their weaknesses explains what a modern cipher must avoid (Figures 1.2 to 1.5, Plate 1.1).

1. **Caesar cipher.** C = (P + k) mod 26. With k = 3, ATTACKATDAWN becomes DWWDFNDWGDZQ. There are only 25 keys, so brute force finishes in seconds.
2. **Affine cipher.** C = (aP + b) mod 26 with gcd(a, 26) = 1. For a = 5 and b = 8, D (3) gives 23 = X. The key space is 12 times 26 = 312, still tiny. Decryption uses the inverse of a, here 21, because 5 times 21 = 105 = 1 mod 26.
3. **Vigenere cipher.** A keyword gives a different shift to each position. It hides single-letter frequencies but repeats every m letters, so Kasiski and the index of coincidence find m and then m Caesar problems remain.
4. **Playfair cipher.** Pairs of letters are replaced using a 5 by 5 key square, so there are 600 digraphs instead of 26 letters. Frequency analysis is harder, but digraph frequencies still leak (TH and HE are common), and a known-plaintext attack is practical.
5. **Hill cipher.** C = K times P mod 26 with a matrix key. It hides digraph and trigraph frequencies, but it is linear: n known plaintext blocks give the matrix by solving equations. The key needs gcd(det K, 26) = 1.
6. **Rail fence cipher.** A transposition: the message is written in a zigzag and read by rails. The letters keep their original frequencies, so the ciphertext still looks like language, and trying small numbers of rails breaks it.
7. **One-time pad.** A random key as long as the message, used once, gives perfect secrecy (Shannon). It fails only in practice, because distributing and never reusing such keys is costly.

| Cipher | Type | Key space | Weakness |
|---|---|---|---|
| Caesar | Substitution | 25 | Brute force |
| Affine | Substitution | 312 | Brute force, frequencies |
| General substitution | Substitution | 26! (88 bits) | Frequency analysis |
| Vigenere | Polyalphabetic | 26 to the power m | Kasiski, coincidence index |
| Playfair | Digraph | about 25! | Digraph statistics |
| Hill | Block, linear | depends on n | Known plaintext |
| Rail fence | Transposition | n rails | Trying every n |

*Conclusion.* All of them leave a structure of the language or a linear equation behind. Modern ciphers (Unit 3) aim for confusion and diffusion, large keys and a public algorithm, and are judged by published cryptanalysis, never by secrecy of design.

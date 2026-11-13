---
subject: Image Processing
grade: BCA Semester 8 (Elective IV)
unit: 4
title: Image Coding and Compression
hours: 9
area: BCA 454 · Image Processing · Unit 4
---

A single uncompressed 12-megapixel photograph occupies 36 MB; a minute of uncompressed Full HD video is more than 10 GB. Without compression, neither the phone gallery, nor video calls, nor streaming, nor a hospital archive of millions of scans would be practical. **Image compression** reduces the amount of data needed to represent an image, by removing redundancy (and, in lossy methods, information the viewer will not miss). This unit follows the outline: the need for compression, the three redundancies, pixel coding (run length, Huffman), information theory, error-free and lossy compression, the JPEG and MPEG standards, and wavelet-based compression.

::: key What this unit gives you
- The need for compression, the compression ratio, and the three kinds of redundancy (coding, interpixel, psychovisual), with a program that measures each.
- The block model of an image compressor and the fidelity criteria (MSE, PSNR).
- Elements of information theory: self-information, entropy, Shannon's limit, and the entropy of an image computed in code.
- Error-free compression: run-length coding, Huffman coding (worked by hand and in code), LZW, arithmetic coding and predictive coding.
- Lossy compression: quantization, transform coding with the DCT, and JPEG step by step on one 8 x 8 block.
- Standards: JPEG, JPEG 2000, and MPEG (I, P and B frames, motion compensation); wavelet compression with the Haar transform.
:::

## 4.1 Need for compression and redundancy

### 4.1.1 Why compress

The raw size of a digital image is $b=M\times N\times k$ bits (Section 1.1). Some typical figures show the need:

| Data | Size (uncompressed) | Remark |
|---|---|---|
| A4 page scanned at 300 dpi, 1 bit | about 1 MB | A fax or scanned document |
| 12 MP colour photograph, 24 bit | 36 MB | Phone camera |
| Chest X-ray, 2048 x 2048, 12 bit | about 6 MB | Thousands per day in one hospital |
| Full HD video, 30 fps, 24 bit | about 187 MB per second | Streaming needs about 5 Mbit/s |
| Satellite scene (11 bands, 7,000 x 7,000 pixels, 16 bit) | about 1 GB | Archives measured in petabytes |

Compression is measured by the **compression ratio** $C_R=n_1/n_2$ (the size before divided by the size after), the **relative data redundancy** $R_D=1-1/C_R$, and the **bit rate** in bits per pixel (bpp). A ratio of 10:1 means 90% of the data is redundant, $R_D=0.9$. Note that the ratio depends on the content: a flat, simple image compresses far better than a noisy one.

### 4.1.2 The three redundancies

Compression is possible because image data are redundant. The three kinds, named by Gonzalez and Woods, are:

1. **Coding redundancy.** Using the same number of bits for every grey level is wasteful when some levels are far more common than others. Giving **short codes to frequent values and long codes to rare ones** (variable-length coding: Huffman, arithmetic) reduces the average bits per pixel. The average length is $L_{avg}=\sum_{k}l(r_k)\,p(r_k)$.
2. **Interpixel (spatial and temporal) redundancy.** Neighbouring pixels are strongly correlated: the value of one pixel predicts its neighbours. In a video, successive frames are almost identical. This redundancy is removed by run-length coding, predictive coding, transforms, and motion compensation.
3. **Psychovisual redundancy.** The eye does not respond equally to all information. It cannot see tiny changes in colour, very fine detail or changes in busy areas, so the information that the eye ignores (high spatial frequencies, chroma detail) can be discarded. Removing it is **irreversible**, so it is lossy, and it is carried out by **quantization**.

::: example Coding redundancy by hand
A 4-level image has probabilities 0.5, 0.25, 0.125, 0.125. A fixed 2-bit code needs 2 bits per pixel. A variable-length code 0, 10, 110, 111 has an average length $0.5(1)+0.25(2)+0.125(3)+0.125(3)=1.75$ bits per pixel, so $C_R=2/1.75=1.14$ and $R_D=1-1/1.14=0.125$: 12.5% of the data was coding redundancy.
:::

### 4.1.3 Compression models and fidelity criteria

```svgfig label="4.1" caption="The image compression system. The encoder removes interpixel redundancy (mapper), psychovisual redundancy (quantizer, absent in lossless coding) and coding redundancy (symbol coder). The decoder reverses the symbol coder and the mapper; the quantizer cannot be reversed."
f = Fig(700, 210)
f.text(80, 20, "ENCODER", size=11, color=NAVY, bold=True, anchor="start")
f.box(10, 34, 70, 44, "Input\nimage f", fill=SAND, stroke=AMBER, size=10.5)
f.box(115, 34, 100, 44, "Mapper\n(reduces\ninterpixel\nredundancy)", size=9.5)
f.box(250, 34, 110, 44, "Quantizer\n(psychovisual;\nlossy only)", size=9.5)
f.box(395, 34, 110, 44, "Symbol coder\n(coding\nredundancy)", size=9.5)
f.box(540, 34, 90, 44, "Compressed\nbit stream", fill=MINT, stroke=TEAL, size=10)
f.arrow([(80, 56), (115, 56)]); f.arrow([(215, 56), (250, 56)])
f.arrow([(360, 56), (395, 56)]); f.arrow([(505, 56), (540, 56)])
f.text(80, 118, "DECODER", size=11, color=NAVY, bold=True, anchor="start")
f.box(540, 132, 90, 44, "Compressed\nbit stream", fill=MINT, stroke=TEAL, size=10)
f.box(395, 132, 110, 44, "Symbol\ndecoder", size=10)
f.box(250, 132, 110, 44, "Inverse\nmapper", size=10)
f.box(115, 132, 100, 44, "Output\nimage f-hat", fill=SAND, stroke=AMBER, size=10)
f.arrow([(540, 154), (505, 154)]); f.arrow([(395, 154), (360, 154)]); f.arrow([(250, 154), (215, 154)])
f.arrow([(585, 78), (585, 132)], dash=True)
```

The **fidelity** of a lossy result is judged **objectively** by the mean square error and the peak signal-to-noise ratio,

$$\mathrm{MSE}=\frac{1}{MN}\sum_{x,y}\big[\hat f(x,y)-f(x,y)\big]^{2},\qquad \mathrm{PSNR}=10\log_{10}\frac{(L-1)^{2}}{\mathrm{MSE}}\ \text{dB},$$

and **subjectively** by a panel of viewers rating the picture on a scale (excellent, fine, passable, marginal, inferior, unusable). For 8-bit photographs a PSNR above 40 dB is visually near-lossless, 30 to 40 dB is good, and below 25 dB shows obvious damage. PSNR is simple but does not always match what people see; measures such as SSIM do better.

## 4.2 Elements of information theory

How much compression is possible? Claude Shannon (1948) answered with **information theory**. A source emits symbols $a_j$ with probabilities $P(a_j)$. The **self-information** of one event is

$$I(a_j)=-\log_{2}P(a_j)\ \text{bits}.$$

A certain event ($P=1$) carries no information; the rarer the event, the more it tells you (a coin flip carries 1 bit, a one-in-1024 event 10 bits). The average information per symbol is the **entropy**

$$H=-\sum_{j}P(a_j)\log_{2}P(a_j)\ \text{bits per symbol}.$$

For an image the symbols are the grey levels and the probabilities come from the normalized histogram, $H=-\sum_k p(r_k)\log_2p(r_k)$. The entropy is the **lower bound** on the average number of bits per symbol of any lossless code that codes each pixel on its own (**Shannon's noiseless coding theorem**): $L_{avg}\ge H$, and with suitable (block) coding $L_{avg}$ can approach $H$. It is largest, $H=\log_2L$, when all levels are equally likely (a flat histogram, such as after equalization), and smallest (0) when one level has probability 1. The **coding efficiency** is $\eta=H/L_{avg}$ and the **redundancy** $L_{avg}-H$. A better estimate of what is possible uses the *first-order* entropy of the differences between neighbours, which is lower, because of interpixel redundancy.

```python
import numpy as np
def entropy(a):
    p = np.bincount(a.ravel(), minlength=256) / a.size
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())

# Self-information and the 4-level example of the text.
for P in (1.0, 0.5, 0.125, 1 / 1024):
    print("P = %-10g self-information = %5.2f bits" % (P, abs(np.log2(P))))
p = np.array([0.5, 0.25, 0.125, 0.125]); H = -(p * np.log2(p)).sum()
L = (p * np.array([1, 2, 3, 3])).sum()
print("example source: entropy %.3f bits, code 0/10/110/111 average %.3f bits, efficiency %.0f%%, C_R vs 2-bit = %.3f" % (H, L, 100 * H / L, 2 / L))

# Entropy of images: noise, a smooth ramp with light noise, and the same ramp after prediction.
rng = np.random.default_rng(6)
n = 128
noise = rng.integers(0, 256, (n, n)).astype(np.uint8)
x = np.arange(n)
ramp = np.clip(np.tile(30 + 180 * x / (n - 1), (n, 1)) + rng.normal(0, 2, (n, n)), 0, 255).astype(np.uint8)
print("entropy of uniform random noise  : %.3f bits/pixel (max 8)" % entropy(noise))
print("entropy of a noisy smooth ramp   : %.3f bits/pixel" % entropy(ramp))
diff = (ramp[:, 1:].astype(int) - ramp[:, :-1].astype(int)) + 255            # horizontal neighbour differences, shifted to be non-negative
d = np.bincount(diff.ravel(), minlength=511) / diff.size; d = d[d > 0]
print("entropy of the neighbour differences: %.3f bits/pixel  (interpixel redundancy removed)" % float(-(d * np.log2(d)).sum()))
print("an equalized histogram has the highest entropy:", entropy(np.repeat(np.arange(256), 64).astype(np.uint8)), "bits")
```
```output
P = 1          self-information =  0.00 bits
P = 0.5        self-information =  1.00 bits
P = 0.125      self-information =  3.00 bits
P = 0.000976562 self-information = 10.00 bits
example source: entropy 1.750 bits, code 0/10/110/111 average 1.750 bits, efficiency 100%, C_R vs 2-bit = 1.143
entropy of uniform random noise  : 7.990 bits/pixel (max 8)
entropy of a noisy smooth ramp   : 7.521 bits/pixel
entropy of the neighbour differences: 3.568 bits/pixel  (interpixel redundancy removed)
an equalized histogram has the highest entropy: 8.0 bits
```
## 4.3 Error-free (lossless) compression and pixel coding

**Error-free (lossless) compression** removes redundancy only: the decoded image is *identical* to the original. It is needed for medical images, scanned legal documents, technical drawings and any image to be edited again, and typically achieves only 2:1 to 3:1 on natural photographs (less on noisy ones, much more on graphics and text pages). It has two stages: a mapper (such as run-length or prediction) that reduces interpixel redundancy, followed by a variable-length symbol coder that removes coding redundancy.

### 4.3.1 Run-length coding

A **run** is a sequence of consecutive pixels with the same value. **Run-length coding (RLC, RLE)** replaces each run by a pair (value, length). It is very effective on binary images (scanned text, fax; each scan line is a series of alternating white and black runs, so only the lengths need be stored) and on graphics with large flat areas, and it is useless, even harmful, on a noisy photograph in which runs are of length 1. The two-dimensional versions in fax standards (CCITT Group 3 and 4) combine runs with Huffman codes for the run lengths. When judging the gain, count **bits**, not entries: a run stored as an 8-bit value and an 8-bit length costs 16 bits, so it only pays when the run is longer than two pixels.

::: example Run-length coding of a binary line
The line 0000 0011 1111 0000 0000 0001 1100 (28 pixels) has runs of 6 zeros, 6 ones, 11 zeros, 3 ones, 2 zeros. Coded as the value of the first pixel (0) followed by the lengths, 6, 6, 11, 3, 2, with 4 bits each, it needs $1+5\times4=21$ bits against 28: $C_R=1.33$. Longer runs compress better; with 4 bits per length the maximum run is 15, so longer runs are split.
:::

### 4.3.2 Huffman coding

**Huffman coding** (1952) gives the **smallest possible average code length** for a fixed set of symbol probabilities, among codes that assign a whole number of bits to each symbol. It is a **prefix code**: no codeword is the beginning of another, so the bit stream can be decoded without separators. The code is built from the bottom up:

1. List the symbols in decreasing order of probability.
2. **Source reduction**: combine the two least probable symbols into one with the sum of the probabilities; re-sort; repeat until only two remain.
3. **Code assignment**: give 0 and 1 to the last two; go backwards through the reductions, and wherever a symbol was formed by combining two, append 0 and 1 to its code to give the two parts.

::: example Huffman code for six grey levels
Probabilities: $a_1=0.4$, $a_2=0.3$, $a_3=0.1$, $a_4=0.1$, $a_5=0.06$, $a_6=0.04$.

Reduction 1: $0.06+0.04=0.10$ (new list 0.4, 0.3, 0.1, 0.1, 0.1). Reduction 2: $0.1+0.1=0.2$ (0.4, 0.3, 0.2, 0.1). Reduction 3: $0.2+0.1=0.3$ (0.4, 0.3, 0.3). Reduction 4: $0.3+0.3=0.6$ (0.6, 0.4). Assigning bits backwards gives the code

| Symbol | Probability | Code | Length |
|---|---|---|---|
| $a_1$ | 0.4 | 1 | 1 |
| $a_2$ | 0.3 | 00 | 2 |
| $a_3$ | 0.1 | 011 | 3 |
| $a_4$ | 0.1 | 0100 | 4 |
| $a_5$ | 0.06 | 01010 | 5 |
| $a_6$ | 0.04 | 01011 | 5 |

$L_{avg}=0.4(1)+0.3(2)+0.1(3)+0.1(4)+0.06(5)+0.04(5)=2.2$ bits, against 3 bits for a fixed code ($C_R=1.36$) and an entropy of $H=2.14$ bits, so the efficiency is 97%. Different tie-breaking gives different but equally good codes with the same $L_{avg}$; the program below, for example, finds the lengths 1, 2, 4, 4, 4, 4 and also gets 2.2 bits.
:::

The **decoding** is a walk down the binary tree, one bit at a time, from the root until a leaf is reached. Huffman coding needs the table (or the histogram) in the file, which costs a few hundred bytes; **truncated** and **modified Huffman** codes limit the table size, and **adaptive** versions learn the probabilities as they go. Its weakness is the whole-bit limit: a symbol with $P=0.99$ still costs 1 bit although its information is only 0.015 bits. **Arithmetic coding** removes this limit by coding a whole *message* as one number in the interval $[0,1)$: each symbol narrows the interval in proportion to its probability, and the final number is written in about $-\log_2P(\text{message})$ bits. It approaches the entropy more closely, is used in JPEG 2000 and in H.264/H.265 (CABAC), but is more complex.

### 4.3.3 LZW coding

**Lempel-Ziv-Welch (LZW)** removes redundancy by building a **dictionary of repeated pixel sequences** on the fly, without knowing the probabilities. It starts with a dictionary of all single grey levels, reads the input, finds the longest string already in the dictionary, outputs its index, and adds that string plus the next pixel as a new entry. The decoder rebuilds the same dictionary from the codes, so the dictionary is never sent. LZW is used in GIF and in TIFF (optionally); similar dictionary methods (deflate) are used in PNG and ZIP.

### 4.3.4 Predictive (differential) coding and bit-plane coding

**Lossless predictive coding** predicts each pixel from its previous neighbours, for instance $\hat f(x,y)=f(x,y-1)$ or $\tfrac12[f(x,y-1)+f(x-1,y)]$, and codes only the **prediction error** $e=f-\hat f$. Because neighbours are correlated, the errors cluster tightly around 0, their histogram is peaked, and their entropy is much lower than that of the pixels; a Huffman or arithmetic coder then does the rest. The decoder makes the same prediction and adds the error back, so reconstruction is exact. **Bit-plane coding** splits the 8-bit image into eight binary planes (Section 2.1.4), and codes each plane with run-length or arithmetic coding; the top planes have long runs and compress well. A **Gray code** is often used so that small changes in intensity do not flip many planes.

```python
import numpy as np, heapq, itertools
from collections import Counter

# ---------- Huffman coding ----------
def huffman(probs):
    cnt = itertools.count()
    heap = [(p, next(cnt), {s: ""}) for s, p in probs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        p1, _, c1 = heapq.heappop(heap); p2, _, c2 = heapq.heappop(heap)
        merged = {s: "0" + c for s, c in c1.items()}; merged.update({s: "1" + c for s, c in c2.items()})
        heapq.heappush(heap, (p1 + p2, next(cnt), merged))
    return heap[0][2]

probs = {"a1": 0.4, "a2": 0.3, "a3": 0.1, "a4": 0.1, "a5": 0.06, "a6": 0.04}
code = huffman(probs)
Lavg = sum(probs[s] * len(c) for s, c in code.items())
H = -sum(p * np.log2(p) for p in probs.values())
print("code lengths:", {s: len(c) for s, c in sorted(code.items())})
print("L_avg = %.2f bits, entropy = %.3f bits, efficiency = %.1f%%, C_R vs 3-bit = %.2f" % (Lavg, H, 100 * H / Lavg, 3 / Lavg))
is_prefix = not any(a != b and b.startswith(a) for a in code.values() for b in code.values())
print("prefix-free:", is_prefix)

# ---------- run-length coding of a binary line ----------
line = "0000001111110000000000011100"
runs = [(k, len(list(g))) for k, g in itertools.groupby(line)]
print("runs:", runs, "-> %d bits with 4-bit lengths + 1 bit start, vs %d bits raw" % (1 + 4 * len(runs), len(line)))

# ---------- LZW on a small pixel string ----------
def lzw(data):
    dic = {(i,): i for i in range(256)}; w = (); out = []
    for c in data:
        wc = w + (c,)
        if wc in dic: w = wc
        else:
            out.append(dic[w]); dic[wc] = len(dic); w = (c,)
    if w: out.append(dic[w])
    return out
pix = [39, 39, 126, 126] * 4                      # the classic 4 x 4 example, rows of 39 39 126 126
codes = lzw(pix)
print("LZW codes for 16 pixels:", codes, "->", len(codes), "codes (256+ needs 9 bits each: %d bits vs 128 raw)" % (9 * len(codes)))

# ---------- predictive coding on a smooth image ----------
rng = np.random.default_rng(9)
n = 128; xs = np.arange(n)
img = np.clip(np.add.outer(40 + 100 * np.sin(xs / 25), 50 * xs / n) + rng.normal(0, 1.5, (n, n)), 0, 255).astype(int)
def H_of(v):
    c = Counter(v.ravel().tolist()); p = np.array(list(c.values())) / v.size
    return float(-(p * np.log2(p)).sum())
err = img[:, 1:] - img[:, :-1]
print("entropy of pixels: %.2f bpp;  of prediction errors (previous-pixel predictor): %.2f bpp" % (H_of(img), H_of(err)))
print("lossless reconstruction exact:", np.array_equal(img[:, 0:1] + np.concatenate([np.zeros((n, 1), int), np.cumsum(err, axis=1)], axis=1), img))
```
```output
code lengths: {'a1': 1, 'a2': 2, 'a3': 4, 'a4': 4, 'a5': 4, 'a6': 4}
L_avg = 2.20 bits, entropy = 2.144 bits, efficiency = 97.4%, C_R vs 3-bit = 1.36
prefix-free: True
runs: [('0', 6), ('1', 6), ('0', 11), ('1', 3), ('0', 2)] -> 21 bits with 4-bit lengths + 1 bit start, vs 28 bits raw
LZW codes for 16 pixels: [39, 39, 126, 126, 256, 258, 260, 259, 257, 126] -> 10 codes (256+ needs 9 bits each: 90 bits vs 128 raw)
entropy of pixels: 6.42 bpp;  of prediction errors (previous-pixel predictor): 2.85 bpp
lossless reconstruction exact: True
```
## 4.4 Lossy compression

**Lossy compression** accepts an error in the reconstructed image in return for a much higher ratio, 10:1 to 50:1 or more with acceptable quality. The loss is introduced by exactly one step, the **quantizer**, which maps many input values to few output values and cannot be undone.

### 4.4.1 Quantization

A **scalar quantizer** divides the range of a value into intervals and sends only the index of the interval; the decoder reconstructs the value as the interval's representative. With a uniform step $\Delta$, $q=\mathrm{round}(c/\Delta)$ and $\hat c=q\Delta$, so the error is at most $\Delta/2$ and the mean square error is about $\Delta^{2}/12$. A bigger $\Delta$ gives fewer distinct values (a lower entropy, so a smaller file) and more error. **Vector quantization** quantizes blocks of pixels against a codebook. The art of lossy coding is to choose a transform in which the *large* quantization errors fall where the eye does not look.

### 4.4.2 Lossy predictive coding (DPCM)

In **differential pulse code modulation** the predictor works on the *reconstructed* previous pixels, so the encoder and decoder stay synchronized, and the prediction error is quantized before being coded: $\dot e=Q(e)$ and $\hat f=\dot e+\text{prediction}$. It is simple and fast, with low delay, but gives modest ratios (about 2:1 to 4:1) and visible granular noise or slope overload on steep edges.

### 4.4.3 Transform coding

**Transform coding** (Section 2.4) divides the image into small blocks (usually $8\times8$), transforms each block with an orthogonal transform (the DCT), quantizes the coefficients, and codes them. Because the DCT compacts the energy into a few low-frequency coefficients, most high-frequency coefficients become zero after quantization, and they are cheap to code with zig-zag scanning and run-length and Huffman coding. The reasons for blocks are cost (a transform of an 8 x 8 block is cheap) and the fact that images are only locally smooth; the price is the **blocking artefact** at high compression, visible 8 x 8 squares. Other transforms (Walsh-Hadamard, KLT, wavelets) are possible; the DCT is the best compromise between compaction and speed and has fast algorithms.

### 4.4.4 The JPEG baseline algorithm

JPEG (Joint Photographic Experts Group, standard ITU T.81 / ISO 10918-1, 1992) is the image format of the world's photographs. The baseline sequential process is:

1. **Colour transform** RGB to YCbCr (Section 1.5.5) and optional **chroma subsampling** to 4:2:0: the two chroma planes are reduced to half width and half height, cutting the data to half before anything else is done.
2. **Block splitting**: each plane is cut into $8\times8$ blocks (padded if necessary).
3. **Level shift**: subtract 128 so that values lie in $[-128,127]$.
4. **2-D DCT** of each block, giving one DC coefficient and 63 AC coefficients.
5. **Quantization**: divide each coefficient by the matching entry of a **quantization table** $Q(u,v)$ and round, $F_q(u,v)=\mathrm{round}[F(u,v)/Q(u,v)]$. The table has small entries in the top-left (low frequencies, the eye is sensitive) and large ones at the bottom-right (high frequencies). The "quality" setting scales the table. This is the only lossy step.
6. **Zig-zag scan**: read the 64 values along diagonals from the top-left, so that the zeros are grouped at the end.
7. **Entropy coding**: the DC values are coded as the **difference** from the previous block's DC (DPCM), the AC values as (run of zeros, size) symbols with Huffman codes, followed by an end-of-block (EOB) code.

Decoding reverses steps 7 to 3 (multiply by the table, inverse DCT, add 128), and the error that remains is the quantization error. **JPEG 2000** (2000) replaces the DCT by a **wavelet** transform on large tiles with arithmetic coding, gives about 20% smaller files at the same quality, no blocking artefacts (the loss shows as slight blur), lossless and lossy modes in one codestream, and progressive transmission by resolution and quality; it is used in digital cinema and medical imaging but not on the web. **JPEG XL, WebP and AVIF** are newer formats.

```python
import numpy as np
# --- one 8 x 8 block through baseline JPEG
Q50 = np.array([[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]], float)
def dct_mat(n=8):
    C = np.zeros((n, n))
    for k in range(n):
        for i in range(n):
            C[k, i] = np.sqrt((1 if k == 0 else 2) / n) * np.cos((2 * i + 1) * k * np.pi / (2 * n))
    return C
C = dct_mat()
rng = np.random.default_rng(12)
yy, xx = np.mgrid[0:8, 0:8]
block = np.clip(120 + 7 * xx + 4 * yy + 10 * np.sin(xx * 0.9) + rng.normal(0, 2, (8, 8)), 0, 255).round()
D = C @ (block - 128) @ C.T
def zigzag(m):
    idx = sorted(((i, j) for i in range(8) for j in range(8)), key=lambda p: (p[0] + p[1], p[1] if (p[0] + p[1]) % 2 == 0 else p[0]))
    return [m[i, j] for i, j in idx]
def scaled(Q, quality):
    s = 5000 / quality if quality < 50 else 200 - 2 * quality
    return np.clip(np.floor((Q * s + 50) / 100), 1, 255)
print("original block, first row:", block[0].astype(int).tolist())
print("DC coefficient %.1f, largest AC %.1f" % (D[0, 0], np.abs(D.ravel()[1:]).max()))
for quality in (90, 50, 10):
    Qm = scaled(Q50, quality)
    Fq = np.round(D / Qm)
    rec = C.T @ (Fq * Qm) @ C + 128
    rec = np.clip(np.round(rec), 0, 255)
    mse = np.mean((rec - block) ** 2)
    zz = np.array(zigzag(Fq)).astype(int)
    last = max(np.nonzero(zz)[0]) if zz.any() else 0
    print("quality %2d: non-zero coefficients %2d of 64, last non-zero at zig-zag position %2d, MSE %6.2f, PSNR %5.1f dB" %
          (quality, np.count_nonzero(Fq), last, mse, 10 * np.log10(255 ** 2 / max(mse, 1e-9))))
Fq = np.round(D / Q50)
print("quantized block at quality 50:\n", Fq.astype(int))
print("zig-zag order of it:", [int(v) for v in zigzag(Fq)][:14], "...")

# --- motion estimation by block matching (the heart of MPEG's P and B frames)
n = 48
f0 = np.zeros((n, n)); f0[12:28, 14:30] = 200; f0[30:40, 8:20] = 120
f0 += np.random.default_rng(3).normal(0, 3, f0.shape)
f1 = np.roll(f0, (3, 5), axis=(0, 1))                          # the scene moves down 3 and right 5
blk = f1[16:32, 18:34]                                           # a 16 x 16 macroblock of the new frame
best = min(((np.abs(f0[16 + dy:32 + dy, 18 + dx:34 + dx] - blk).sum(), dy, dx) for dy in range(-8, 9) for dx in range(-8, 9)))
print("best match in the previous frame: displacement (dy, dx) = (%d, %d), SAD = %.0f" % (best[1], best[2], best[0]))
resid = blk - f0[16 + best[1]:32 + best[1], 18 + best[2]:34 + best[2]]
print("residual energy with motion compensation %.0f against %.0f without" % ((resid ** 2).sum(), ((blk - f0[16:32, 18:34]) ** 2).sum()))
```
```output
original block, first row: [120, 137, 145, 147, 147, 143, 153, 167]
DC coefficient 246.4, largest AC 89.5
quality 90: non-zero coefficients 10 of 64, last non-zero at zig-zag position 15, MSE   2.91, PSNR  43.5 dB
quality 50: non-zero coefficients  5 of 64, last non-zero at zig-zag position  9, MSE   7.33, PSNR  39.5 dB
quality 10: non-zero coefficients  4 of 64, last non-zero at zig-zag position  6, MSE  27.98, PSNR  33.7 dB
quantized block at quality 50:
 [[15 -8  0 -3  0  0  0  0]
 [-6  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0]
 [-1  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0]
 [ 0  0  0  0  0  0  0  0]]
zig-zag order of it: [15, -8, -6, 0, 0, 0, -3, 0, 0, -1, 0, 0, 0, 0] ...
best match in the previous frame: displacement (dy, dx) = (-3, -5), SAD = 0
residual energy with motion compensation 0 against 4206144 without
```
## 4.5 Video compression: MPEG

A video is a sequence of frames, and consecutive frames are almost identical (temporal redundancy). **MPEG** (Moving Picture Experts Group; MPEG-1 1993, MPEG-2 1995 for DVD and digital TV, MPEG-4 and H.264/AVC 2003, H.265/HEVC 2013) combines JPEG-like intra-frame coding with **inter-frame prediction**:

- **I frames** (intra) are coded alone, like a JPEG picture. They are the entry points for random access and error recovery, and are the largest.
- **P frames** (predicted) are predicted from the previous I or P frame by **motion compensation**: for each $16\times16$ **macroblock** the encoder searches the reference frame for the best match, sends the **motion vector**, and codes only the DCT of the small **residual** (the difference). A moving object costs a vector, not a picture.
- **B frames** (bidirectional) are predicted from both the previous and the next reference frame, averaging the two, which handles uncovered background and noise; they are the smallest, but need the future frame and so add delay and require the frames to be sent out of order.
- A **group of pictures (GOP)**, for example I B B P B B P B B P B B, repeats; a longer GOP compresses better, a shorter one allows faster seeking.

```svgfig label="4.2" caption="A group of pictures in display order (top). Arrows show the prediction: P frames from the previous I or P frame, B frames from the nearest reference frames on both sides. The transmission order (bottom) sends each reference frame before the B frames that need it."
f = Fig(700, 230)
names = ["I", "B", "B", "P", "B", "B", "P", "B", "B", "I"]
cx = [50 + i * 66 for i in range(10)]
fills = {"I": (SAND, AMBER), "P": (MINT, TEAL), "B": (BLUE, NAVY)}
f.text(20, 18, "Display order", size=10.5, color=NAVY, bold=True, anchor="start")
for i, nme in enumerate(names):
    fl, st = fills[nme]
    f.box(cx[i] - 20, 40, 40, 34, nme, fill=fl, stroke=st, bold=True, size=12)
    f.text(cx[i], 90, str(i + 1), size=9.5, color=SLATE)
f.arrow([(cx[0] + 4, 38), (cx[0] + 4, 26), (cx[3] - 4, 26), (cx[3] - 4, 38)], color=TEAL)
f.arrow([(cx[3] + 4, 38), (cx[3] + 4, 26), (cx[6] - 4, 26), (cx[6] - 4, 38)], color=TEAL)
f.arrow([(cx[6] + 4, 38), (cx[6] + 4, 26), (cx[9] - 4, 26), (cx[9] - 4, 38)], color=TEAL)
f.text(20, 135, "Transmission order", size=10.5, color=NAVY, bold=True, anchor="start")
order = [(0, "I"), (3, "P"), (1, "B"), (2, "B"), (6, "P"), (4, "B"), (5, "B"), (9, "I"), (7, "B"), (8, "B")]
for k, (i, nme) in enumerate(order):
    fl, st = fills[nme]
    f.box(30 + k * 66, 150, 40, 34, nme, fill=fl, stroke=st, bold=True, size=12)
    f.text(50 + k * 66, 202, "frame " + str(i + 1), size=9, color=SLATE)
```

::: caution Why quality drops when you re-save a JPEG
Every save repeats the DCT and quantization. Rounding again on blocks that already carry quantization error, and shifting the block grid when the image is cropped, adds new errors: a file saved ten times at quality 75 is visibly worse than one saved once. Edit a lossless master and export to JPEG once.
:::

## 4.6 Wavelet-based image compression

The DCT looks at fixed 8 x 8 blocks and says what frequencies are present, but not where. **Wavelets** analyse the image at several **scales** and keep the position as well: a small wavelet picks up fine detail and edges, a stretched one the broad shapes. The result is a **multiresolution** representation, a pyramid from a coarse approximation to the full image, and a transform that works on the *whole image* without blocks.

### 4.6.1 The Haar wavelet transform

The simplest wavelet is the **Haar** wavelet. For a pair of neighbouring samples $x_0,x_1$ it computes an **approximation** (average) and a **detail** (difference):

$$a=\frac{x_0+x_1}{2},\qquad d=\frac{x_0-x_1}{2}\qquad\Longleftrightarrow\qquad x_0=a+d,\quad x_1=a-d .$$

Applied to a whole row it produces a half-length low-pass signal $a$ (a blurred, subsampled copy) and a half-length high-pass signal $d$ (the differences, mostly near zero in smooth regions). Repeating on $a$ gives a **multi-level** decomposition. For the row $(9,7,3,5)$: first level $a=(8,4)$, $d=(1,-1)$; second level on $(8,4)$: $a=6$, $d=2$. The transform $(6,\;2,\;1,\;-1)$ holds the same information in a form with a **mean (6)** and details; reversing gives back $8=6+2$, $4=6-2$, then $9,7,3,5$. (The orthonormal version uses $1/\sqrt2$ instead of $1/2$ so that energy is preserved.)

In two dimensions the transform is applied to the rows and then the columns, which splits the image into four **subbands** one-quarter the size:

| Subband | Row filter | Column filter | Content |
|---|---|---|---|
| **LL** | low | low | A half-size approximation of the image |
| **LH** | low | high | Horizontal edges (changes down the columns) |
| **HL** | high | low | Vertical edges |
| **HH** | high | high | Diagonal detail and noise |

The LL band is split again at each further level, giving the familiar nested layout of Figure 4.3. A 3-level transform has 10 subbands: one LL (coarse) and three each of LH, HL, HH.

```svgfig label="4.3" caption="Subbands of a 3-level 2-D wavelet decomposition. Each level splits the current LL band into LL, LH, HL and HH; the final LL3 holds the coarse image and the finer detail bands (large areas) are mostly near zero and compress very well."
f = Fig(560, 330)
S = 256; x0, y0 = 150, 30
f.box(x0, y0, S, S, "", fill="#ffffff", stroke=NAVY, r=0)
def level(x, y, s, lv):
    h = s / 2
    if lv == 0:
        f.box(x, y, s, s, "LL3", fill=SAND, stroke=AMBER, r=0, size=11, bold=True)
        return
    f.box(x + h, y, h, h, "HL%d" % lv, fill=BLUE, stroke=NAVY, r=0, size=10 + (2 - lv) * 0.5)
    f.box(x, y + h, h, h, "LH%d" % lv, fill=BLUE, stroke=NAVY, r=0, size=10 + (2 - lv) * 0.5)
    f.box(x + h, y + h, h, h, "HH%d" % lv, fill=MINT, stroke=TEAL, r=0, size=10 + (2 - lv) * 0.5)
    level(x, y, h, lv - 1)
level(x0, y0, S, 3)
f.text(75, 160, "Level 1:", size=10, color=SLATE, bold=True)
f.text(75, 176, "finest detail", size=10, color=SLATE)
f.text(75, 70, "Level 3:", size=10, color=SLATE, bold=True)
f.text(75, 86, "coarsest", size=10, color=SLATE)
f.text(x0 + S / 2, 318, "H = high-pass, L = low-pass; first letter = rows, second = columns", size=9.5, color=SLATE)
```

### 4.6.2 Compression with wavelets

The procedure mirrors transform coding:

1. Apply a multi-level wavelet transform to the whole image (biorthogonal 9/7 filters for lossy and 5/3 for lossless in JPEG 2000).
2. **Quantize** the coefficients, with a **dead-zone** quantizer that sets all small coefficients to zero (a threshold) and coarser steps for finer subbands, because the eye is less sensitive to fine detail.
3. **Entropy code** the result. Most of the coefficients in LH1, HL1 and HH1 are zero, so very long runs and highly skewed statistics result. JPEG 2000 uses **EBCOT** (embedded block coding with optimized truncation) with an arithmetic coder, and the earlier **EZW** (embedded zerotree wavelet) coder exploits the fact that if a coarse coefficient is insignificant, its descendants at finer scales usually are too.

The advantages over JPEG are no blocking artefacts (at high compression the picture just gets softer), **progressive** and **scalable** decoding (a thumbnail by reading the first bytes; resolution or quality can be chosen after encoding) and better quality at low bit rates (below about 0.5 bpp). The disadvantages are higher computation and memory and, so far, less support on the web. Wavelets are also used in denoising (shrink small detail coefficients), edge detection and in the FBI fingerprint standard.

```python
import numpy as np

def haar2(a):
    """One level of the orthonormal 2-D Haar transform: returns LL, LH, HL, HH."""
    s2 = np.sqrt(2)
    lo = (a[:, 0::2] + a[:, 1::2]) / s2; hi = (a[:, 0::2] - a[:, 1::2]) / s2
    LL = (lo[0::2] + lo[1::2]) / s2; LH = (lo[0::2] - lo[1::2]) / s2     # low across rows, high down columns
    HL = (hi[0::2] + hi[1::2]) / s2; HH = (hi[0::2] - hi[1::2]) / s2
    return LL, LH, HL, HH

def ihaar2(LL, LH, HL, HH):
    s2 = np.sqrt(2)
    lo = np.zeros((LL.shape[0] * 2, LL.shape[1])); hi = np.zeros_like(lo)
    lo[0::2] = (LL + LH) / s2; lo[1::2] = (LL - LH) / s2
    hi[0::2] = (HL + HH) / s2; hi[1::2] = (HL - HH) / s2
    out = np.zeros((lo.shape[0], lo.shape[1] * 2))
    out[:, 0::2] = (lo + hi) / s2; out[:, 1::2] = (lo - hi) / s2
    return out

# 1-D example of the text
x = np.array([9.0, 7.0, 3.0, 5.0])
a1 = (x[0::2] + x[1::2]) / 2; d1 = (x[0::2] - x[1::2]) / 2
a2 = (a1[0] + a1[1]) / 2; d2 = (a1[0] - a1[1]) / 2
print("1-D Haar of (9,7,3,5): level 1 a =", a1.tolist(), "d =", d1.tolist(), "; level 2 a =", a2, "d =", d2, "-> (6, 2, 1, -1)")

# 2-D, three levels on a 64 x 64 test image.
rng = np.random.default_rng(15)
n = 64; yy, xx = np.mgrid[0:n, 0:n]
img = 70 + 1.2 * xx + 0.8 * yy
img[(yy - 30) ** 2 + (xx - 36) ** 2 < 15 ** 2] += 70
img[10:22, 8:30] -= 40
img += rng.normal(0, 1.5, img.shape)
bands = []; cur = img.copy()
for lv in range(3):
    cur, LH, HL, HH = haar2(cur); bands.append((LH, HL, HH))
print("shapes: LL3 %s, level-3 bands %s, level-1 bands %s" % (cur.shape, bands[2][0].shape, bands[0][0].shape))
energy = lambda b: float((b ** 2).sum())
tot = energy(cur) + sum(energy(b) for lv in bands for b in lv)
print("energy preserved (orthonormal): %.6f" % (tot / (img ** 2).sum()))
print("energy in LL3: %.2f%%; in the 9 detail bands: %.2f%%" % (100 * energy(cur) / tot, 100 * (1 - energy(cur) / tot)))

# Compression: keep only the largest coefficients and reconstruct.
coef = np.concatenate([cur.ravel()] + [b.ravel() for lv in bands for b in lv])
for keep in (0.50, 0.10, 0.05):
    thr = np.sort(np.abs(coef))[::-1][int(keep * coef.size) - 1]
    c = cur * (np.abs(cur) >= thr)
    bs = [tuple(b * (np.abs(b) >= thr) for b in lv) for lv in bands]
    r = c
    for lv in (2, 1, 0): r = ihaar2(r, *bs[lv])
    mse = np.mean((r - img) ** 2)
    print("keep the largest %2d%% of coefficients: MSE %6.2f, PSNR %5.1f dB, compression about %2.0f:1 before entropy coding" %
          (100 * keep, mse, 10 * np.log10(255 ** 2 / mse), 1 / keep))
```
```output
1-D Haar of (9,7,3,5): level 1 a = [8.0, 4.0] d = [1.0, -1.0] ; level 2 a = 6.0 d = 2.0 -> (6, 2, 1, -1)
shapes: LL3 (8, 8), level-3 bands (8, 8), level-1 bands (32, 32)
energy preserved (orthonormal): 1.000000
energy in LL3: 99.10%; in the 9 detail bands: 0.90%
keep the largest 50% of coefficients: MSE   0.33, PSNR  52.9 dB, compression about  2:1 before entropy coding
keep the largest 10% of coefficients: MSE   3.58, PSNR  42.6 dB, compression about 10:1 before entropy coding
keep the largest  5% of coefficients: MSE  13.77, PSNR  36.7 dB, compression about 20:1 before entropy coding
```
## 4.7 Summary and exercises

Compression removes **coding**, **interpixel** and **psychovisual** redundancy and is measured by $C_R=n_1/n_2$, $R_D=1-1/C_R$, and (for lossy methods) MSE and PSNR. The **entropy** $H=-\sum p\log_2p$ is the lower bound for lossless symbol coding. Lossless methods: run-length (binary images, fax), **Huffman** (optimal prefix code from probabilities), arithmetic (fractional bits), LZW (dictionary; GIF) and predictive coding (code the error). Lossy methods add a **quantizer**: transform coding with the DCT on 8 x 8 blocks (JPEG: colour transform, subsampling, DCT, quantization table, zig-zag, run-length and Huffman), MPEG (I, P and B frames, motion-compensated prediction, GOP) and wavelet coding (multi-level subbands, dead-zone quantization, EBCOT in JPEG 2000).

1. Why is image compression necessary? Give three examples with their uncompressed sizes.
2. Define compression ratio and relative data redundancy. A 1 MB image is compressed to 100 KB. Find both.
3. Explain the three types of redundancy with one method that removes each.
4. Draw and explain the block diagram of an image compression system. Which block is irreversible?
5. Define MSE and PSNR. Find the PSNR of an 8-bit image with an MSE of 25.
6. Define self-information and entropy. What is the self-information of an event of probability 1/8? Find the entropy of a source with probabilities 0.5, 0.25, 0.125, 0.125.
7. State Shannon's noiseless coding theorem. When is the entropy of an image a maximum?
8. Run-length encode the line WWWWBBWWWWWWBBBW (W white, B black) and find the compression ratio if every run costs 1 bit for the colour change plus 4 bits for the length.
9. Construct a Huffman code for six symbols with probabilities 0.35, 0.25, 0.20, 0.10, 0.06, 0.04. Find the average length, the entropy and the efficiency.
10. Why is a Huffman code a prefix code? State two limitations of Huffman coding and how arithmetic coding overcomes one.
11. Explain how LZW builds its dictionary. Where is it used?
12. Explain lossless predictive coding. A row has the values 100, 102, 105, 105, 104; give the prediction errors for the previous-pixel predictor.
13. What is quantization? A DCT coefficient 87.3 is quantized with a step of 16: give the index, the reconstructed value and the error. What would a coefficient of $-9.4$ with a step of 24 become?
14. Explain the baseline JPEG algorithm step by step. Why is only one step lossy? Why does JPEG use YCbCr and 4:2:0 subsampling?
15. Why are the quantization table entries larger at the bottom right? What is the blocking artefact and when does it appear?
16. Explain the I, P and B frames of MPEG and the idea of motion compensation. A GOP of 12 frames has one I frame of 120 kbit, three P frames of 40 kbit and eight B frames of 15 kbit each. Find the average bit rate at 25 frames per second.
17. Explain the Haar wavelet transform on $(9,7,3,5)$ and reconstruct the sequence from the result.
18. Describe the subbands of a 3-level wavelet decomposition and how wavelet compression works. List the advantages of JPEG 2000 over JPEG.
19. A grey image uses 8 bits per pixel. Under what conditions is a 2:1 lossless ratio realistic for a photograph? Give one image for which 50:1 lossless is possible.
20. Compare lossless and lossy compression in a table with a use for each.

**Answers to the numerical items.** (2) $C_R=1000\text{ KB}/100\text{ KB}=\mathbf{10}$:1, $R_D=1-1/10=\mathbf{0.9}$ (90% redundant). (5) $10\log_{10}(255^{2}/25)=10\log_{10}2601=\mathbf{34.1\ dB}$. (6) $I=-\log_2(1/8)=\mathbf{3}$ bits; $H=0.5(1)+0.25(2)+0.125(3)+0.125(3)=\mathbf{1.75}$ bits. (8) Runs: 4 W, 2 B, 6 W, 3 B, 1 W: five runs, so $5\times5=25$ bits (colour bit and length), against 16 raw bits: the code is *longer* ($C_R=0.64$): run-length coding does not help when runs are this short and the cost per run is high. (9) Reductions: $0.06+0.04=0.10$; $0.10+0.10=0.20$; $0.20+0.20=0.40$; $0.35+0.25=0.60$; $0.60+0.40=1$. Lengths: 0.35 → 2, 0.25 → 2, 0.20 → 2, 0.10 → 3, 0.06 → 4, 0.04 → 4. $L_{avg}=0.70+0.50+0.40+0.30+0.24+0.16=\mathbf{2.30}$ bits; $H=0.530+0.5+0.464+0.332+0.244+0.186=\mathbf{2.256}$ bits; efficiency $=2.256/2.30=\mathbf{98.1\%}$. (12) The first value 100 is sent as it is; the errors are $+2,+3,0,-1$. (13) $87.3/16=5.46\to$ index **5**, reconstruction $5\times16=80$, error **7.3**; $-9.4/24=-0.39\to$ index **0**, so the coefficient is lost (the reconstruction is 0). (16) Total per GOP $=120+3\times40+8\times15=360$ kbit for 12 frames, 30 kbit per frame; at 25 frames per second this is $\mathbf{750}$ kbit/s. (17) $a_1=(8,4)$, $d_1=(1,-1)$; $a_2=6$, $d_2=2$; the result is $(6,2,1,-1)$; reconstruction $8=6+2$, $4=6-2$; $9=8+1$, $7=8-1$, $3=4-1$, $5=4+1$.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is Huffman coding? Give its steps.**

Huffman coding is a lossless variable-length prefix code that gives the shortest average code length for a given set of symbol probabilities when each symbol receives a whole number of bits. Steps: sort the symbols by probability; combine the two smallest probabilities into one symbol and re-sort; repeat until two remain; assign 0 and 1 to the last two and work backwards, appending 0 and 1 to the parts of every combined symbol. Frequent symbols receive short codes. The average length is $L_{avg}=\sum p_il_i$, and it lies within one bit of the entropy $H$. Illustrate with six probabilities as in the worked example.

**Q2 (5 marks). Explain the three types of redundancy in images.**

Coding redundancy: fixed-length codes ignore the histogram; variable-length codes (Huffman) shorten the average length. Interpixel redundancy: neighbouring pixels (and successive frames) are correlated; run-length coding, prediction, transforms and motion compensation exploit it. Psychovisual redundancy: the eye ignores some detail (high frequencies, fine colour detail); quantization removes it, irreversibly. The first two can be removed without loss; the third gives lossy compression.

**Q3 (10 marks). Describe the JPEG baseline compression algorithm.**

Draw the block diagram: RGB to YCbCr and 4:2:0 subsampling; split into 8 x 8 blocks; level shift by 128; 2-D DCT; quantization with a table scaled by the quality factor; zig-zag scan; DC differential coding and AC run-length coding of (zeros, size) with Huffman codes. Explain the reasoning of each step: the eye is less sensitive to colour detail; the DCT compacts the energy into a few low-frequency coefficients; the quantization table is coarser for high frequencies; the zig-zag groups zeros so that the end-of-block code replaces them. State that only the quantization (and subsampling) is lossy, and that the decoder reverses the steps. Add the worked 8 x 8 block of Section 4.4.4: at quality 50 only a few coefficients survive. Mention blocking artefacts and JPEG 2000.

**Q4 (10 marks). Explain video compression in MPEG with the roles of I, P and B frames.**

Video has strong temporal redundancy. MPEG codes I frames independently (like JPEG). P frames are predicted from the previous reference with motion compensation: for each 16 x 16 macroblock the encoder finds the best-matching block in the reference (block matching minimizing the sum of absolute differences), transmits the motion vector and the DCT-coded residual. B frames use both a past and a future reference, give the highest compression but need frame reordering and add delay. Draw the GOP of Figure 4.2 with the arrows and the transmission order. Discuss the trade-off of GOP length (compression against random access and error recovery) and give the example of Exercise 16 for the bit rate. Mention that H.264 and H.265 refine the same idea with variable block sizes and arithmetic coding.

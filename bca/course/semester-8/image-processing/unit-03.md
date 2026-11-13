---
subject: Image Processing
grade: BCA Semester 8 (Elective IV)
unit: 3
title: Image Restoration
hours: 9
area: BCA 454 · Image Processing · Unit 3
---

Enhancement (Unit 2) is subjective: we make an image *look* better. **Image restoration** is objective: we try to **recover the original image** from a degraded copy, using a model of how the degradation happened. A blurred photograph from a shaking camera, a satellite scene with sensor stripes, an X-ray with quantum noise and a scanned old document are all restoration problems. The method is always the same: model the degradation, estimate its parameters, and apply the inverse process. This unit covers the degradation model, noise models and noise-only filtering, blur removal by inverse and Wiener filtering, and the morphological operations of erosion and dilation named in the outline.

::: key What this unit gives you
- The degradation model $g=h\star f+\eta$ (and $G=HF+N$) and the difference between enhancement and restoration.
- Noise models (Gaussian, Rayleigh, gamma, exponential, uniform, impulse), periodic noise, and how to estimate the noise from a flat region.
- Spatial filters for noise-only degradation: arithmetic, geometric, harmonic and contraharmonic means; median, max, min, midpoint and alpha-trimmed filters; adaptive filters.
- Blur: the point-spread function, inverse filtering, the transfer function of uniform linear motion blur, and why inverse filtering fails with noise.
- The Wiener (minimum mean square error) filter, with a program comparing the two.
- Morphological operations: erosion, dilation, opening, closing, boundary extraction and hole filling.
:::

## 3.1 Image degradation model

The degradation is modelled as an operator $H$ (the **degradation function**) followed by additive noise $\eta(x,y)$:

$$g(x,y)=h(x,y)\star f(x,y)+\eta(x,y)\quad\Longleftrightarrow\quad G(u,v)=H(u,v)F(u,v)+N(u,v),$$

where $f$ is the original image, $g$ the degraded one, $h$ the **point-spread function (PSF)** (the response to a single bright point), $\star$ is convolution, and capital letters are Fourier transforms (the second form follows from the convolution theorem). Restoration finds an estimate $\hat f$ as close to $f$ as possible from $g$, knowing something about $H$ and $\eta$.

```svgfig label="3.1" caption="The image degradation and restoration model. The original f passes through the degradation function H and gets additive noise to give g; the restoration filter or filters produce the estimate f-hat."
f = Fig(700, 170)
f.box(10, 60, 80, 50, "Original\nf(x, y)", fill=SAND, stroke=AMBER, size=10.5)
f.box(130, 60, 100, 50, "Degradation\nfunction H", size=10.5)
f.circle(285, 85, 17, fill=BLUE, stroke=NAVY, label="+", size=15)
f.text(285, 40, "noise", size=10, color=SLATE)
f.text(285, 56, "eta(x, y)", size=10, color=SLATE)
f.box(345, 60, 80, 50, "Degraded\ng(x, y)", size=10.5)
f.box(465, 60, 110, 50, "Restoration\nfilter(s)", fill=MINT, stroke=TEAL, size=10.5)
f.box(610, 60, 80, 50, "Estimate\nf-hat(x, y)", fill=MINT, stroke=TEAL, size=10.5)
f.arrow([(90, 85), (130, 85)])
f.arrow([(230, 85), (268, 85)])
f.arrow([(302, 85), (345, 85)])
f.arrow([(425, 85), (465, 85)])
f.arrow([(575, 85), (610, 85)])
f.arrow([(285, 60), (285, 68)])
f.text(170, 135, "DEGRADATION", size=10, color=AMBER, bold=True)
f.text(530, 135, "RESTORATION", size=10, color=TEAL, bold=True)
```

::: key Restoration against enhancement
**Enhancement** is subjective, needs no model, and aims at a pleasing result (contrast stretching, sharpening). **Restoration** is objective, is based on a degradation model, and tries to reverse it (deblurring, denoising). A sharpening filter and a deblurring filter may look alike, but one is chosen by taste and the other derived from a physical model. The measures used to compare an estimate with the original are the MSE and the PSNR, $\mathrm{PSNR}=10\log_{10}(255^{2}/\mathrm{MSE})$ dB.
:::

## 3.2 Noise models

Noise comes from the acquisition (sensor temperature, low light, electronic amplifiers), from transmission (interference on a channel) and from quantization. Spatially, noise is assumed **independent of position** and uncorrelated with the image, and is described by the **probability density function (PDF)** of its grey-level values.

| Noise | PDF | Where it is met |
|---|---|---|
| **Gaussian** | $p(z)=\dfrac{1}{\sqrt{2\pi}\,\sigma}e^{-(z-\mu)^{2}/2\sigma^{2}}$ | Electronic circuit and sensor noise in poor light or at high temperature; the most common model |
| **Rayleigh** | $p(z)=\dfrac{2}{b}(z-a)e^{-(z-a)^{2}/b}$ for $z\ge a$ | Range imaging; skewed histograms |
| **Gamma (Erlang)** | $p(z)=\dfrac{a^{b}z^{b-1}}{(b-1)!}e^{-az}$ for $z\ge0$ | Laser imaging |
| **Exponential** | $p(z)=a\,e^{-az}$ for $z\ge0$ | Laser imaging (the special case $b=1$ of gamma) |
| **Uniform** | $p(z)=\dfrac{1}{b-a}$ for $a\le z\le b$ | A model for quantization noise; a base for random-number generators |
| **Impulse (salt-and-pepper)** | $P_a$ at $z=a$ (pepper), $P_b$ at $z=b$ (salt), 0 elsewhere | Faulty switching, dead sensor elements, transmission errors; bipolar if both $P_a$ and $P_b$ are non-zero |

The mean of a Gaussian shifts the whole image; the standard deviation sets how grainy it looks. Impulse noise is the only model with a visible "dots" look, and it drives the choice of the median filter. **Periodic noise** is different: it comes from electrical or electromechanical interference and shows as a repeating pattern (stripes) which appears as **concentrated bursts of energy** in the Fourier spectrum, at positions that depend on the frequency of the interference. It is removed by **notch** or band-reject filters (Section 2.5.3).

**Estimating noise.** The PDF parameters are usually estimated from a small patch of **constant grey level** (a clear sky, a uniform wall): the histogram of that patch has the shape of the noise PDF, and its mean and variance give the parameters, $\mu=\sum z_ip(z_i)$ and $\sigma^{2}=\sum(z_i-\mu)^{2}p(z_i)$.

## 3.3 Restoration when only noise is present

If $H$ is the identity, $g=f+\eta$ and the spatial filters of Section 2.3 are used, applied to a window $S_{xy}$ of size $m\times n$ around $(x,y)$.

**Mean filters**

| Filter | Formula | Best for |
|---|---|---|
| Arithmetic mean | $\hat f=\dfrac1{mn}\sum_{S_{xy}}g(s,t)$ | Gaussian, uniform noise (blurs) |
| Geometric mean | $\hat f=\Big[\prod_{S_{xy}}g(s,t)\Big]^{1/mn}$ | Gaussian noise; blurs less than the arithmetic mean |
| Harmonic mean | $\hat f=\dfrac{mn}{\sum 1/g(s,t)}$ | Salt noise and Gaussian; fails for pepper |
| Contraharmonic mean, order $Q$ | $\hat f=\dfrac{\sum g^{Q+1}}{\sum g^{Q}}$ | $Q>0$ removes pepper, $Q<0$ removes salt; $Q=0$ is the arithmetic mean, $Q=-1$ the harmonic mean |

The contraharmonic filter with the wrong sign of $Q$ is a disaster: positive $Q$ on salt noise makes the salt larger.

**Order-statistic filters** rank the window values: **median** (the middle value; the best all-rounder for salt-and-pepper), **max** (brightest value; removes pepper, enlarges bright spots), **min** (removes salt), **midpoint** $\tfrac12(\max+\min)$ (good for random noise such as Gaussian and uniform) and the **alpha-trimmed mean**, which drops the $d/2$ lowest and $d/2$ highest values and averages the remaining $mn-d$ ones: with $d=0$ it is the arithmetic mean, with $d=mn-1$ it is the median, so it is good when both Gaussian and impulse noise are present.

**Adaptive filters** change their behaviour with the local statistics. The **adaptive local noise reduction** filter uses the noise variance $\sigma_\eta^{2}$ and the local mean $m_L$ and variance $\sigma_L^{2}$: $\hat f=g-\dfrac{\sigma_\eta^{2}}{\sigma_L^{2}}(g-m_L)$. Where the local variance is no larger than the noise variance (flat area) the output is the local mean, and where it is much larger (an edge) the output stays near $g$. The **adaptive median filter** grows its window until the median is not an impulse, which preserves detail with high noise densities.

```python
import numpy as np
rng = np.random.default_rng(21)
n = 64
img = np.full((n, n), 90.0); img[16:48, 16:48] = 170.0; img[28:36, 28:36] = 120.0

def windows(a, k=3):
    r = k // 2; p = np.pad(a, r, mode="edge")
    return np.stack([p[i:i + a.shape[0], j:j + a.shape[1]] for i in range(k) for j in range(k)])

def psnr(a, b=img): return 10 * np.log10(255 ** 2 / np.mean((a - b) ** 2))

# --- Gaussian noise: compare the mean filters
gn = np.clip(img + rng.normal(0, 20, img.shape), 1, 255)
W = windows(gn)
print("Gaussian noise (sigma 20)   PSNR noisy %.2f dB" % psnr(gn))
print("  arithmetic mean 3x3         %.2f dB" % psnr(W.mean(0)))
print("  geometric mean 3x3          %.2f dB" % psnr(np.exp(np.log(W).mean(0))))
print("  median 3x3                  %.2f dB" % psnr(np.median(W, 0)))
print("  midpoint 3x3                %.2f dB" % psnr((W.max(0) + W.min(0)) / 2))

# --- Pepper only, then salt only: contraharmonic with Q = +1.5 and -1.5
for name, val in (("pepper", 0.0), ("salt", 255.0)):
    sp = img.copy(); sp[rng.random(img.shape) < 0.08] = val
    sp1 = np.clip(sp, 1, 255); W = windows(sp1)
    for Q in (1.5, -1.5):
        out = (W ** (Q + 1)).sum(0) / (W ** Q).sum(0)
        print("%-6s noise, contraharmonic Q = %+.1f : PSNR %.2f dB (noisy %.2f)" % (name, Q, psnr(out), psnr(sp)))

# --- Mixed impulse + Gaussian noise: alpha-trimmed mean (d = 6 of 9) against mean and median
mix = img + rng.normal(0, 10, img.shape)
m = rng.random(img.shape); mix[m < 0.06] = 0; mix[m > 0.94] = 255
W = windows(mix); Ws = np.sort(W, axis=0)
print("Mixed noise: noisy %.2f | mean %.2f | median %.2f | alpha-trimmed d=6 %.2f dB" %
      (psnr(mix), psnr(W.mean(0)), psnr(np.median(W, 0)), psnr(Ws[3:6].mean(0))))

# --- Adaptive local noise reduction, known sigma_eta^2 = 400
W5 = windows(gn, 5); mL = W5.mean(0); vL = W5.var(0)
ad = gn - np.minimum(1.0, 400 / np.maximum(vL, 1e-9)) * (gn - mL)
print("Adaptive local noise reduction: %.2f dB (arithmetic 3x3 %.2f dB)" % (psnr(ad), psnr(windows(gn).mean(0))))
```
```output
Gaussian noise (sigma 20)   PSNR noisy 22.25 dB
  arithmetic mean 3x3         28.45 dB
  geometric mean 3x3          28.00 dB
  median 3x3                  28.61 dB
  midpoint 3x3                26.07 dB
pepper noise, contraharmonic Q = +1.5 : PSNR 29.58 dB (noisy 17.98)
pepper noise, contraharmonic Q = -1.5 : PSNR 9.93 dB (noisy 17.98)
salt   noise, contraharmonic Q = +1.5 : PSNR 14.52 dB (noisy 15.79)
salt   noise, contraharmonic Q = -1.5 : PSNR 28.38 dB (noisy 15.79)
Mixed noise: noisy 14.41 | mean 22.87 | median 31.67 | alpha-trimmed d=6 30.85 dB
Adaptive local noise reduction: 30.22 dB (arithmetic 3x3 28.45 dB)
```
## 3.4 Blur and the degradation function

Blur is the result of convolving the image with a PSF $h$. Common physical causes and their models:

- **Linear motion** of the camera or the object during the exposure.
- **Out-of-focus** lens: the PSF is a disc (a "circle of confusion").
- **Atmospheric turbulence** (telescope, aerial images): $H(u,v)=e^{-k(u^{2}+v^{2})^{5/6}}$, close to a Gaussian, with $k$ depending on the severity.
- **Sensor and optics** limits: a Gaussian-like PSF.

### 3.4.1 Estimating the degradation function

$H$ is rarely known exactly. There are three ways to estimate it: by **observation** (take a small sub-image with strong signal, such as an edge or a point, and compare it with your guess of the unblurred version, $H_s(u,v)=G_s(u,v)/\hat F_s(u,v)$); by **experiment** (photograph a point source, a bright dot, with the same equipment and settings: its image *is* the PSF, $H(u,v)=G(u,v)/A$); and by **mathematical modelling** (using the physics, as in the turbulence formula above or the motion model below).

### 3.4.2 Uniform linear motion blur

Suppose an image $f(x,y)$ moves with $x_0(t)=at/T$ and $y_0(t)=bt/T$ during an exposure of length $T$, so that in total it moves by $a$ pixels horizontally and $b$ pixels vertically. The exposure integrates the shifted copies, and the transfer function is

$$H(u,v)=\frac{T}{\pi(ua+vb)}\sin[\pi(ua+vb)]\;e^{-j\pi(ua+vb)} .$$

For motion only in $x$ ($b=0$) the PSF is a one-pixel-high strip of $a$ equal weights and $H=\dfrac{T}{\pi ua}\sin(\pi ua)e^{-j\pi ua}$, a sinc that has **zeros** wherever $ua$ is a non-zero integer. Those zeros cause the major difficulty of deblurring.

## 3.5 Inverse filtering

If $H$ is known and noise is ignored, the obvious estimate divides the spectrum of the degraded image by $H$:

$$\hat F(u,v)=\frac{G(u,v)}{H(u,v)}=F(u,v)+\frac{N(u,v)}{H(u,v)} .$$

This is **inverse filtering**. Without noise it restores the image exactly. But there are two problems, both visible in the second form of the equation.

1. The noise term $N/H$ is unknown, so the original cannot be recovered exactly even if $H$ is known.
2. Where $H(u,v)$ is zero or very small (the zeros of the motion-blur sinc, or the high frequencies of any smooth blur) the division is undefined or enormous, so that the **noise is amplified without limit** and dominates the output.

A common cure is to **limit the division** to the frequencies near the origin (apply the inverse only where $D(u,v)<D_0$ or $|H|>\epsilon$, a *pseudo-inverse*), which removes the worst noise at the cost of some detail.

## 3.6 Wiener filtering (minimum mean square error filtering)

Norbert Wiener's approach treats the image and the noise as random processes and finds the estimate $\hat f$ that **minimizes the mean square error** $e^{2}=E\{(f-\hat f)^{2}\}$. The filter in the frequency domain is

$$\hat F(u,v)=\left[\frac{1}{H(u,v)}\cdot\frac{|H(u,v)|^{2}}{|H(u,v)|^{2}+S_\eta(u,v)/S_f(u,v)}\right]G(u,v),$$

where $S_\eta=|N|^{2}$ and $S_f=|F|^{2}$ are the power spectra of the noise and of the undegraded image. The ratio $S_\eta/S_f$ is the inverse of the signal-to-noise ratio at each frequency. Where the signal is strong the bracketed factor is close to 1 and the filter acts as the inverse filter; where the signal is weak, or $H$ is small, the factor is small and the filter **gives up** and suppresses the frequency instead of amplifying the noise. Since $S_f$ is usually unknown, a constant is used,

$$\hat F=\left[\frac{1}{H}\frac{|H|^{2}}{|H|^{2}+K}\right]G,$$

and $K$ is adjusted by trial: a larger $K$ means more smoothing and less ringing, a smaller one means a sharper but noisier result. If there is no noise ($S_\eta=0$) the Wiener filter reduces to the inverse filter. **Constrained least squares filtering** is a related method that needs only the noise mean and variance and uses a smoothness constraint (the Laplacian), and so does not need the power spectra.

| | Inverse filter | Wiener filter |
|---|---|---|
| Needs | $H$ | $H$, noise and image power spectra (or the constant $K$) |
| With noise | Fails: amplifies noise where $H\approx0$ | Trades deblurring against noise amplification |
| Without noise | Exact | Same as the inverse filter |
| Output | A pseudo-inverse with a cut-off is needed to survive | Stable for all $H$ |

```python
import numpy as np
rng = np.random.default_rng(8)
n = 64
img = np.full((n, n), 60.0)
img[10:30, 12:34] = 200.0; img[38:56, 30:58] = 140.0
yy, xx = np.mgrid[0:n, 0:n]; img[((yy - 46) ** 2 + (xx - 16) ** 2) < 64] = 230.0

psnr = lambda a: 10 * np.log10(255 ** 2 / np.mean((a - img) ** 2))

# Uniform horizontal motion blur of length a = 9 pixels (circular convolution through the DFT).
a = 9
h = np.zeros((n, n)); h[0, :a] = 1.0 / a
H = np.fft.fft2(h)
blurred = np.fft.ifft2(np.fft.fft2(img) * H).real
print("blurred only                      : PSNR %.2f dB" % psnr(blurred))
print("smallest |H|: %.4f (near-zeros of the sinc), largest %.2f" % (np.abs(H).min(), np.abs(H).max()))

# 1. Noise-free: the inverse filter restores the image exactly.
inv0 = np.fft.ifft2(np.fft.fft2(blurred) / H).real
print("inverse filter, no noise          : largest pixel error %.1e (exact, up to rounding)" % np.abs(inv0 - img).max())

# 2. With a little noise (sigma = 2): inverse filtering collapses.
noisy = blurred + rng.normal(0, 2.0, blurred.shape)
inv = np.fft.ifft2(np.fft.fft2(noisy) / H).real
print("blurred + noise (sigma 2)         : PSNR %.2f dB" % psnr(noisy))
print("inverse filter with noise         : PSNR %.2f dB (noise amplified)" % psnr(inv))

# 3. Pseudo-inverse: divide only where |H| exceeds a threshold.
for eps in (0.05, 0.2):
    Hp = np.where(np.abs(H) > eps, H, np.inf)
    out = np.fft.ifft2(np.fft.fft2(noisy) / Hp).real
    print("pseudo-inverse, |H| > %.2f         : PSNR %.2f dB" % (eps, psnr(out)))

# 4. Wiener filter with the constant K: sweep K.
for K in (0.0001, 0.001, 0.01, 0.1):
    W = np.conj(H) / (np.abs(H) ** 2 + K)
    out = np.fft.ifft2(np.fft.fft2(noisy) * W).real
    print("Wiener, K = %-7g                : PSNR %.2f dB" % (K, psnr(out)))
```
```output
blurred only                      : PSNR 17.57 dB
smallest |H|: 0.0162 (near-zeros of the sinc), largest 1.00
inverse filter, no noise          : largest pixel error 1.7e-12 (exact, up to rounding)
blurred + noise (sigma 2)         : PSNR 17.56 dB
inverse filter with noise         : PSNR 14.70 dB (noise amplified)
pseudo-inverse, |H| > 0.05         : PSNR 22.80 dB
pseudo-inverse, |H| > 0.20         : PSNR 24.24 dB
Wiener, K = 0.0001                 : PSNR 16.49 dB
Wiener, K = 0.001                  : PSNR 21.94 dB
Wiener, K = 0.01                   : PSNR 25.98 dB
Wiener, K = 0.1                    : PSNR 22.98 dB
```
::: caution Boundaries and wrap-around
The programs above use circular convolution, so the blur wraps around the image edge and the same wrap-around is undone exactly. A real photograph is blurred without wrap-around: restoration then leaves **ringing** bands near the borders, which is avoided by tapering the edges of the image before filtering or by padding it.
:::

## 3.7 Morphological image processing

**Mathematical morphology** processes images by their **shape** using set theory. A binary image is the set $A$ of the coordinates of its foreground (white, 1) pixels; a small shape, the **structuring element (SE)** $B$ (a 3 x 3 square, a cross, a disc), acts as a probe that is slid over the image. Morphological operations are used to remove noise, separate touching objects, join broken ones, find boundaries, fill holes, and extract skeletons: everything that is needed to clean a thresholded image before measuring it. Notation: $(B)_z$ is $B$ translated so that its origin is at $z$, and $\hat B$ is $B$ reflected about its origin (the same for a symmetric SE).

### 3.7.1 Dilation and erosion

**Dilation** grows objects: $A\oplus B=\{z\mid(\hat B)_z\cap A\neq\varnothing\}$. The output is the set of positions where the SE, centred at $z$, touches (overlaps) at least one foreground pixel. Effects: it enlarges objects, fills small holes and gaps, and joins nearby objects. Its main use is to **bridge gaps** in broken text or lines.

**Erosion** shrinks objects: $A\ominus B=\{z\mid(B)_z\subseteq A\}$. The output is the set of positions where the SE, centred at $z$, fits entirely inside $A$. Effects: it shrinks objects, removes specks and thin spurs smaller than the SE, and separates objects joined by a thin bridge.

Dilation and erosion are **duals**: $(A\ominus B)^{c}=A^{c}\oplus\hat B$, so eroding the objects is the same as dilating the background. Neither undoes the other: dilating an eroded shape does not give back the original, which is the idea behind opening.

```svgfig label="3.2" caption="Erosion and dilation of a binary image with a 3 x 3 square structuring element. Erosion keeps only pixels whose whole 3 x 3 neighbourhood is foreground and deletes the isolated noise pixel; dilation adds every pixel touched by the element."
A = ["..........",
     ".########.",
     ".########.",
     ".#########",
     ".########.",
     "..........",
     "....#.....",
     ".........."]
R, C = len(A), len(A[0])
def get(g, i, j):
    return 1 if 0 <= i < R and 0 <= j < C and g[i][j] == "#" else 0
ero = ["".join("#" if all(get(A, i + a, j + b) for a in (-1, 0, 1) for b in (-1, 0, 1)) else "." for j in range(C)) for i in range(R)]
dil = ["".join("#" if any(get(A, i + a, j + b) for a in (-1, 0, 1) for b in (-1, 0, 1)) else "." for j in range(C)) for i in range(R)]
f = Fig(690, 205)
cell = 19
for k, (g, title) in enumerate(((A, "A (original)"), (ero, "A eroded by B"), (dil, "A dilated by B"))):
    ox = 12 + k * 228
    f.text(ox + C * cell / 2, 14, title, size=11, color=NAVY, bold=True)
    for i in range(R):
        for j in range(C):
            on = g[i][j] == "#"
            f.box(ox + j * cell, 26 + i * cell, cell, cell, "", fill=NAVY if on else "#ffffff", stroke="#94a3b8", r=0, sw=0.8)
f.text(345, 198, "Foreground pixels are dark. Structuring element B: 3 x 3 square of ones.", size=9.5, color=SLATE)
```

### 3.7.2 Opening, closing and other operations

- **Opening**: $A\circ B=(A\ominus B)\oplus B$. Erode, then dilate. It smooths contours, breaks thin bridges, **removes small objects and spurs**, and keeps the size of the large ones; it is the union of all copies of $B$ that fit inside $A$.
- **Closing**: $A\bullet B=(A\oplus B)\ominus B$. Dilate, then erode. It **fills small holes and narrow gaps**, joins close objects and smooths contours from the outside.
- Both are **idempotent**: applying the same opening or closing a second time changes nothing.
- **Boundary extraction**: $\beta(A)=A-(A\ominus B)$, the pixels removed by one erosion, which leaves a boundary one pixel thick for a 3 x 3 SE.
- **Hole filling**: starting from a seed point $X_0$ inside each hole, iterate $X_k=(X_{k-1}\oplus B)\cap A^{c}$ until it stops changing; the union of $X_k$ and $A$ is the filled object. $B$ is the cross-shaped (4-connected) SE.
- **Hit-or-miss transform**: finds an exact pattern of foreground and background pixels (used for corner detection and thinning); the others are the **skeleton**, **thinning**, **thickening** and **convex hull**.
- **Grey-scale morphology**: erosion is the local **minimum** and dilation the local **maximum** of the pixels under the SE; opening removes bright spots smaller than the SE, closing removes dark ones; the **morphological gradient** (dilation minus erosion) outlines edges, and the **top-hat** transform (image minus its opening) extracts small bright objects on an uneven background.

```python
import numpy as np

def dilate(A, B):
    r = B.shape[0] // 2; p = np.pad(A, r)
    out = np.zeros_like(A)
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            if B[i, j]: out |= p[i:i + A.shape[0], j:j + A.shape[1]]
    return out

def erode(A, B):
    r = B.shape[0] // 2; p = np.pad(A, r)
    out = np.ones_like(A)
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            if B[i, j]: out &= p[i:i + A.shape[0], j:j + A.shape[1]]
    return out

B = np.ones((3, 3), bool)
A = np.zeros((16, 16), bool)
A[3:12, 3:12] = True            # a square (81 pixels)
A[7, 12:15] = True              # a thin spur 3 pixels long
A[14, 14] = True                # an isolated noise pixel
A[7, 7] = False                 # a one-pixel hole in the square
print("pixels in A:", A.sum())
print("erosion  :", erode(A, B).sum(), "pixels (spur, noise pixel and a ring round the hole are consumed)")
print("dilation :", dilate(A, B).sum(), "pixels")
op = dilate(erode(A, B), B)
cl = erode(dilate(A, B), B)
print("opening  :", op.sum(), "pixels; noise pixel removed:", not op[14, 14], "; spur removed:", not op[7, 13])
print("closing  :", cl.sum(), "pixels; hole filled:", bool(cl[7, 7]))
print("idempotent: opening twice equals once:", np.array_equal(dilate(erode(op, B), B), op))
sq = np.zeros((7, 7), bool); sq[1:6, 1:6] = True
bd = sq & ~erode(sq, B)
print("boundary of a solid 5 x 5 square: %d pixels (25 - 9)" % bd.sum())
# Duality: erosion of A equals the complement of the dilation of the complement.
print("duality (A eroded)^c = A^c dilated:", np.array_equal(~erode(A, B), dilate(~A, B)))
# Grey-scale: opening removes a bright 1-pixel spike; closing removes a dark one.
g = np.full((9, 9), 100.0); g[4, 4] = 255.0; g[2, 6] = 0.0
def gmin(a): p = np.pad(a, 1, mode="edge"); return np.min([p[i:i+9, j:j+9] for i in range(3) for j in range(3)], axis=0)
def gmax(a): p = np.pad(a, 1, mode="edge"); return np.max([p[i:i+9, j:j+9] for i in range(3) for j in range(3)], axis=0)
print("grey opening : spike 255 -> %.0f ; grey closing: dark 0 -> %.0f" % (gmax(gmin(g))[4, 4], gmin(gmax(g))[2, 6]))
print("morphological gradient at the spike: %.0f" % (gmax(g) - gmin(g))[4, 4])
```
```output
pixels in A: 84
erosion  : 40 pixels (spur, noise pixel and a ring round the hole are consumed)
dilation : 139 pixels
opening  : 80 pixels; noise pixel removed: True ; spur removed: True
closing  : 85 pixels; hole filled: True
idempotent: opening twice equals once: True
boundary of a solid 5 x 5 square: 16 pixels (25 - 9)
duality (A eroded)^c = A^c dilated: True
grey opening : spike 255 -> 100 ; grey closing: dark 0 -> 100
morphological gradient at the spike: 155
```
## 3.8 Summary and exercises

Restoration recovers an image by reversing a modelled degradation: $g=h\star f+\eta$, or $G=HF+N$ in the frequency domain. Noise is described by a PDF (Gaussian, Rayleigh, gamma, exponential, uniform, impulse), estimated from a flat patch; periodic noise appears as spikes in the spectrum and is removed by notch filters. For noise only, mean filters (arithmetic, geometric, harmonic, contraharmonic), order-statistic filters (median, max, min, midpoint, alpha-trimmed) and adaptive filters are used according to the noise type. Blur (motion, defocus, turbulence) has a transfer function $H$. Inverse filtering divides by $H$ and fails where $H$ is near zero because it amplifies noise; the Wiener filter minimizes the mean square error and stays stable by including the noise-to-signal ratio $K$. Morphology uses a structuring element: erosion shrinks, dilation grows, opening removes small objects and closing fills small holes.

1. Distinguish image enhancement from image restoration.
2. Draw the image degradation and restoration model and write it in the spatial and the frequency domain.
3. List the common noise models with their PDFs and a source of each. Which model gives the salt-and-pepper appearance?
4. How is the noise PDF estimated from an image? What is periodic noise and how is it removed?
5. The mean square error between an image and its restoration is 100. Find the PSNR for 8-bit images.
6. Compare the arithmetic, geometric, harmonic and contraharmonic mean filters. When does the contraharmonic filter with $Q>0$ fail?
7. For the window values 2, 4, 4 find the arithmetic, geometric, harmonic and contraharmonic ($Q=1$) means.
8. Explain the median, max, min, midpoint and alpha-trimmed mean filters, with the noise each suits.
9. For the 3 x 3 window with values 12, 15, 200, 14, 13, 0, 16, 15, 14, find the median and the alpha-trimmed mean for $d=4$.
10. Explain the adaptive local noise reduction filter and the adaptive median filter. Why are they better than a fixed mean filter?
11. Name four causes of blur, with the form of the degradation function. How can $H$ be estimated?
12. Write the transfer function of uniform linear motion blur. For a horizontal blur of 8 pixels in a 64-point DFT, at which frequency indices does $H$ vanish?
13. Explain inverse filtering. Why does it fail in the presence of noise? What is a pseudo-inverse?
14. Derive the form of the Wiener filter and explain each factor. What does it reduce to when there is no noise, and what happens when $H=0$?
15. For $H=0.5$ at some frequency, find the inverse filter gain and the Wiener gain for $K=0.25$ and $K=0.1$.
16. Compare inverse filtering and Wiener filtering in a table.
17. Define dilation and erosion with a structuring element, and show that they are duals.
18. With $A=\{2,3,4,5,8\}$ and the 1-D structuring element $B=\{-1,0,1\}$ find $A\ominus B$, $A\oplus B$, the opening and the closing.
19. Explain opening and closing and give a use of each. Why are they idempotent?
20. How are the boundary of an object and the holes in it found by morphology? How many boundary pixels does a solid 5 x 5 square have with a 3 x 3 square SE?

**Answers to the numerical items.** (5) $\mathrm{PSNR}=10\log_{10}(255^{2}/100)=10\log_{10}650.25=\mathbf{28.1\ dB}$. (7) Arithmetic $=10/3=\mathbf{3.33}$; geometric $=(2\cdot4\cdot4)^{1/3}=32^{1/3}=\mathbf{3.17}$; harmonic $=3/(1/2+1/4+1/4)=\mathbf{3}$; contraharmonic $(Q=1)=(4+16+16)/(2+4+4)=36/10=\mathbf{3.6}$. (9) Sorted: 0, 12, 13, 14, 14, 15, 15, 16, 200. The median is **14**. For $d=4$ drop the two lowest (0, 12) and two highest (16, 200); the mean of 13, 14, 14, 15, 15 is $71/5=\mathbf{14.2}$. The outliers 200 and 0 are ignored. (12) $H$ vanishes where $ua$ is a non-zero integer; with $u=k/64$ and $a=8$ this is $k=8m$: **8, 16, 24, 32** and so on, so the first zero is at $k=8$ (0.125 cycles per pixel). (15) Inverse gain $1/H=\mathbf{2}$. Wiener gain $=\dfrac1H\dfrac{|H|^{2}}{|H|^{2}+K}$: for $K=0.25$ it is $2\times0.25/0.5=\mathbf{1.0}$; for $K=0.1$ it is $2\times0.25/0.35=\mathbf{1.43}$, so the Wiener filter boosts this frequency less than the inverse filter does and so amplifies less noise. (18) Erosion: $z$ such that $\{z-1,z,z+1\}\subseteq A$, so $z=3$ and $z=4$: $\{3,4\}$. Dilation: the union of $\{z-1,z,z+1\}$ for $z\in A$ is $\{1,\dots,9\}$. Opening $=\{3,4\}\oplus B=\{2,3,4,5\}$ (the isolated point 8 is removed). Closing $=\{1..9\}\ominus B=\{2,\dots,8\}$ (the gap at 6 and 7 is filled; the point 8 is joined). (20) Boundary $=A-(A\ominus B)$: erosion of the 5 x 5 square leaves 3 x 3 = 9 pixels, so the boundary has $25-9=\mathbf{16}$ pixels.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Write a note on noise models in images.**

Noise is an unwanted random variation of pixel values, produced during acquisition (sensor heat, low light) or transmission. It is modelled by the PDF of its values and is assumed independent of position. Gaussian noise (the most common) has a bell-shaped PDF with mean $\mu$ and standard deviation $\sigma$; Rayleigh, gamma and exponential noise are skewed and appear in range and laser imaging; uniform noise models quantization; impulse noise (salt-and-pepper) has two spikes of probability at the minimum and maximum grey levels. Periodic noise shows as spikes in the spectrum. The parameters are estimated from the histogram of a flat patch.

**Q2 (5 marks). Why does inverse filtering fail for noisy images, and how does the Wiener filter overcome this?**

Inverse filtering computes $\hat F=G/H=F+N/H$. Where $H$ is zero or very small, which is true for the high frequencies of any smooth blur and for the zeros of motion blur, the term $N/H$ becomes very large, so the noise is amplified and swamps the image. The Wiener filter minimizes the mean square error and uses $\hat F=\frac1H\frac{|H|^{2}}{|H|^{2}+K}G$: where $H$ is small the factor goes to zero, so those frequencies are suppressed instead of amplified. Without noise it is the same as the inverse filter.

**Q3 (10 marks). Describe the spatial filters used to restore an image that contains only noise.**

Give the model $g=f+\eta$. Present the mean filters with formulae: arithmetic, geometric, harmonic and contraharmonic of order $Q$ (positive $Q$ removes pepper, negative removes salt). Present the order-statistic filters: median (salt-and-pepper), max (pepper), min (salt), midpoint (Gaussian, uniform) and alpha-trimmed (mixed noise). Present the adaptive filters with the local statistic formula $\hat f=g-\frac{\sigma_\eta^{2}}{\sigma_L^{2}}(g-m_L)$ and the growing window of the adaptive median filter. Finish with a table matching noise types to filters and a numerical example such as Exercise 7 or 9. Mention that all of them blur or remove some detail, and that periodic noise needs frequency-domain notch filters.

**Q4 (10 marks). Explain erosion, dilation, opening and closing with examples.**

Define the binary image as a set $A$ and the structuring element $B$. Give $A\oplus B$ (grows; fills gaps) and $A\ominus B$ (shrinks; removes specks) and their duality. Show Figure 3.2 or a 1-D example: with $A=\{2,3,4,5,8\}$ and $B=\{-1,0,1\}$ the erosion is $\{3,4\}$ and the dilation $\{1,\dots,9\}$. Define opening as erosion followed by dilation (removes small objects, thin spurs; keeps large shapes) and closing as dilation followed by erosion (fills small holes and gaps); both are idempotent. Add the uses: noise removal from a thresholded image, boundary extraction $\beta(A)=A-(A\ominus B)$, hole filling and skeletons; and mention the grey-scale versions (local min and max).

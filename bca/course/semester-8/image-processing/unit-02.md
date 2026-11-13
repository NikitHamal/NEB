---
subject: Image Processing
grade: BCA Semester 8 (Elective IV)
unit: 2
title: Image Enhancement
hours: 12
area: BCA 454 · Image Processing · Unit 2
---

**Image enhancement** processes an image so that the result is more suitable than the original for a specific application. There is no general theory: "better" depends on the task. A radiologist wants faint tissue boundaries visible, a mapmaker wants roads to stand out, a photographer wants a dull holiday picture to look vivid. Enhancement works in two domains. In the **spatial domain** we manipulate the pixels directly, $g(x,y)=T[f(x,y)]$, where $T$ acts on a single pixel (point processing), on its neighbourhood (spatial filtering), or on the histogram. In the **frequency domain** we first transform the image (Fourier, cosine), modify the transform and invert it. The unit follows the outline: point processing, histogram processing, spatial filtering, transforms, and frequency-domain filtering.

::: key What this unit gives you
- Point processing: negative, log, power-law, contrast stretching, clipping, thresholding, level slicing and bit-plane slicing, each with its formula, curve and a program.
- Histogram processing: the normalized histogram, equalization derived and computed by hand, and histogram specification.
- Spatial filtering by correlation and convolution: averaging, median, Gaussian, Laplacian, unsharp masking, high-boost, and low-, high- and band-pass spatial filters.
- Image transforms: the 2-D DFT and its properties, the FFT (cost counted), and the discrete cosine transform.
- Frequency-domain enhancement: ideal, Butterworth and Gaussian low- and high-pass filters, and the homomorphic filter.
:::

## 2.1 Spatial domain enhancement: point processing

In **point processing** the neighbourhood is $1\times1$, so the output at a pixel depends only on the input at that pixel: $s=T(r)$, where $r$ is the input grey level and $s$ the output. The function $T$ is plotted as a curve from $r$ (horizontal) to $s$ (vertical); the shape of the curve tells you the effect. Throughout, grey levels lie in $[0,L-1]$ with $L=256$.

### 2.1.1 Digital negative

For an image with levels $[0,L-1]$ the **negative** is $s=L-1-r$. Dark becomes light and light becomes dark. It is useful to bring out white or grey detail embedded in the dark regions of an image, especially when the dark area dominates: the classic example is a breast X-ray, in which the negative makes small tissue masses easier to see.

### 2.1.2 Logarithmic and power-law transformations

The **log transformation** $s=c\log(1+r)$ maps a narrow range of low (dark) input values to a wide range of output values and compresses the high values. Use it when the dynamic range is too large to display, for instance a Fourier spectrum whose values run from 0 to $10^{6}$: displayed linearly only a few bright dots show, after the log the structure becomes visible. The constant $c$ scales the result back into $[0,L-1]$: $c=255/\log(1+r_{max})$. The **inverse log** does the opposite.

The **power-law (gamma) transformation** is $s=c\,r^{\gamma}$ with $r$ normalized to $[0,1]$. For $\gamma<1$ it expands dark values (brightens the image, like the log); for $\gamma>1$ it expands bright values (darkens it); $\gamma=1$ is the identity. Many devices respond with a power law: a CRT monitor has $\gamma\approx2.2$, so an image must be **gamma corrected** with $s=r^{1/2.2}$ before display; this is why the sRGB standard stores a non-linear value.

### 2.1.3 Contrast stretching, clipping and thresholding

A low-contrast image, from poor lighting or a small sensor range, uses only a narrow band of grey levels. **Contrast stretching** is a piecewise-linear map that expands that band. With control points $(r_1,s_1)$ and $(r_2,s_2)$ and slopes $\alpha,\beta,\gamma$ on the three segments,

$$s=\begin{cases}\alpha r & 0\le r<r_1\\ \beta(r-r_1)+s_1 & r_1\le r<r_2\\ \gamma(r-r_2)+s_2 & r_2\le r\le L-1\end{cases}$$

If $r_1=s_1$ and $r_2=s_2$ the map is the identity. The most common stretch is **min-max (full-scale) stretching**: $s=(L-1)\dfrac{r-r_{min}}{r_{max}-r_{min}}$. **Clipping** is the special case $\alpha=\gamma=0$: everything below $r_1$ becomes 0 and everything above $r_2$ becomes $L-1$, used to remove noise outside a range. **Thresholding** is the extreme: $s=0$ for $r<T$ and $s=L-1$ for $r\ge T$ (a very steep stretch with $r_1=r_2=T$), giving a binary image used for segmentation (Unit 5).

### 2.1.4 Intensity-level slicing and bit-plane slicing

**Intensity-level (grey-level) slicing** highlights a band $[A,B]$ of grey levels, for instance to show a water body or a particular tissue. Two forms: one gives a high value to all levels in the band and a low value to the rest (a binary result), the other brightens the band and leaves the other levels unchanged. **Bit-plane slicing** treats an 8-bit pixel as eight planes, bit 0 (least significant) to bit 7 (most). The top planes carry most of the visually significant data and the lowest planes look like noise; this is the idea behind some compression and watermarking schemes (Unit 5).

```svgfig label="2.1" caption="Transfer curves s = T(r) of point operations on an 8-bit image: identity, negative, log, gamma 0.5 and 2.0, and a contrast stretch with control points (70, 20) and (180, 235)."
f = Fig(680, 330)
ax = Axes(f, 55, 20, 270, 270, (0, 255), (0, 255))
ax.grid(dx=64, dy=64)
ax.axes(xl="input r", yl="output s")
import math
ax.curve(lambda r: r, color=SLATE, sw=1.6, dash=True)
ax.curve(lambda r: 255 - r, color=RED, sw=2.2)
ax.curve(lambda r: 255 * math.log(1 + r) / math.log(256), color=TEAL, sw=2.2)
ax.curve(lambda r: 255 * (r / 255) ** 2.0, color=AMBER, sw=2.2)
f.text(130, 306, "negative (red), log (teal), gamma 2.0 (amber), identity (dashed)", size=9.5, color=SLATE, anchor="start")
bx = Axes(f, 385, 20, 270, 270, (0, 255), (0, 255))
bx.grid(dx=64, dy=64)
bx.axes(xl="input r", yl="output s")
def stretch(r):
    if r < 70: return r * 20 / 70
    if r < 180: return 20 + (r - 70) * 215 / 110
    return 235 + (r - 180) * 20 / 75
bx.curve(stretch, color=NAVY, sw=2.4, n=400)
bx.curve(lambda r: 255 * (r / 255) ** 0.5, color=TEAL, sw=2.0)
bx.pt(70, 20, "(70, 20)", dx=6, dy=-8)
bx.pt(180, 235, "(180, 235)", dx=-6, dy=14, anchor="end")
f.text(430, 306, "contrast stretch (navy), gamma 0.5 (teal)", size=9.5, color=SLATE, anchor="start")
```

```python
import numpy as np

# A dull test image: values squeezed into the band 80..140 (a low-contrast photograph).
rng = np.random.default_rng(7)
n = 64
yy, xx = np.mgrid[0:n, 0:n]
img = 80 + 60 * (xx / (n - 1)) + rng.normal(0, 3, (n, n))
img = np.clip(img, 0, 255).astype(np.uint8)
print("input        : min %3d  max %3d  mean %6.2f  std %5.2f" % (img.min(), img.max(), img.mean(), img.std()))

def show(name, a):
    print("%-13s: min %3d  max %3d  mean %6.2f  std %5.2f" % (name, a.min(), a.max(), a.mean(), a.std()))

L = 256
neg   = (L - 1 - img)
logt  = (255 / np.log(1 + img.max()) * np.log(1 + img.astype(float))).astype(np.uint8)
gam05 = (255 * (img / 255.0) ** 0.5).astype(np.uint8)
gam20 = (255 * (img / 255.0) ** 2.0).astype(np.uint8)
mm    = (255.0 * (img - img.min()) / (img.max() - img.min())).astype(np.uint8)
thr   = np.where(img >= 110, 255, 0).astype(np.uint8)
for name, a in (("negative", neg), ("log", logt), ("gamma 0.5", gam05), ("gamma 2.0", gam20), ("min-max", mm), ("threshold110", thr)):
    show(name, a)

# Piecewise-linear stretch with control points (r1,s1) = (90,20) and (r2,s2) = (130,235).
def stretch(r, r1=90, s1=20, r2=130, s2=235):
    r = r.astype(float)
    out = np.where(r < r1, r * s1 / r1,
          np.where(r < r2, s1 + (r - r1) * (s2 - s1) / (r2 - r1), s2 + (r - r2) * (255 - s2) / (255 - r2)))
    return np.clip(out, 0, 255).astype(np.uint8)
show("stretch", stretch(img))

# Intensity-level slicing of the band 100..120 and bit planes.
sl = np.where((img >= 100) & (img <= 120), 255, 0)
print("pixels inside the band 100..120:", int((sl == 255).sum()), "of", n * n)
for b in (7, 6, 4, 0):
    plane = (img >> b) & 1
    print("bit plane %d: %4d ones (%.1f%%)" % (b, plane.sum(), 100 * plane.mean()))
```
```output
input        : min  71  max 147  mean 109.44  std 17.84
negative     : min 108  max 184  mean 145.56  std 17.84
log          : min 218  max 255  mean 238.89  std  8.42
gamma 0.5    : min 134  max 193  mean 165.96  std 13.71
gamma 2.0    : min  19  max  84  mean  47.77  std 15.36
min-max      : min   0  max 255  mean 128.50  std 59.87
threshold110 : min   0  max 255  mean 126.82  std 127.50
stretch      : min  15  max 237  mean 124.93  std 81.16
pixels inside the band 100..120: 1399 of 4096
bit plane 7:  847 ones (20.7%)
bit plane 6: 3249 ones (79.3%)
bit plane 4: 2064 ones (50.4%)
bit plane 0: 2059 ones (50.3%)
```
::: caution Do not stretch noise
Stretching enlarges everything in the chosen band, including noise. If the input has a few extreme outliers, a min-max stretch is almost useless because $r_{min}$ and $r_{max}$ are set by those outliers; use percentiles (for example the 1st and 99th) as $r_1$ and $r_2$ and clip the rest.
:::

## 2.2 Histogram processing

### 2.2.1 The histogram

The **histogram** of a digital image with levels $0,\dots,L-1$ is the function $h(r_k)=n_k$, where $r_k$ is the $k$-th grey level and $n_k$ the number of pixels with that level. The **normalized histogram** is $p(r_k)=n_k/MN$, an estimate of the probability that a pixel has level $r_k$; the values sum to 1. The histogram has no spatial information, but it tells a lot about the image:

| Histogram shape | Image |
|---|---|
| Concentrated at the low end | Dark image |
| Concentrated at the high end | Bright (washed-out) image |
| Narrow, in the middle | Low contrast |
| Spread over the whole range, fairly even | High contrast, usually a good image |
| Two peaks (bimodal) | Object and background: easy to threshold |

### 2.2.2 Histogram equalization

Equalization is a point operation $s=T(r)$ chosen so that the output histogram is as flat (uniform) as possible, which spreads the grey levels across the full range and so raises contrast automatically. For a continuous variable $r\in[0,1]$ with density $p_r(r)$, the transformation that makes $p_s(s)$ uniform is the **cumulative distribution function**

$$s=T(r)=\int_{0}^{r}p_r(w)\,dw .$$

(Derivation: $T$ is monotonically increasing, so $p_s(s)=p_r(r)\,|dr/ds|$. From $ds/dr=p_r(r)$ we get $p_s(s)=p_r(r)/p_r(r)=1$.) For the digital image the integral becomes a sum:

$$s_k=T(r_k)=(L-1)\sum_{j=0}^{k}p_r(r_j)=\frac{L-1}{MN}\sum_{j=0}^{k}n_j,\qquad k=0,1,\dots,L-1,$$

and each $s_k$ is **rounded** to the nearest integer. Because of rounding the output histogram is only approximately flat, and equalization can merge levels (never split them), so it is not exactly reversible.

**Procedure.** (1) Count $n_k$. (2) Compute $p(r_k)=n_k/MN$. (3) Form the cumulative sum $\sum p$. (4) Multiply by $L-1$. (5) Round. (6) Map every pixel $r_k\to s_k$.

::: example Equalizing a 3-bit image
A 64 x 64 image ($MN=4096$) has $L=8$ levels with counts $n_k$ = 790, 1023, 850, 656, 329, 245, 122, 81 for $r_k=0,\dots,7$.

| $r_k$ | $n_k$ | $p=n_k/4096$ | cumulative | $7\times$cum. | $s_k$ (rounded) |
|---|---|---|---|---|---|
| 0 | 790 | 0.19 | 0.19 | 1.33 | 1 |
| 1 | 1023 | 0.25 | 0.44 | 3.08 | 3 |
| 2 | 850 | 0.21 | 0.65 | 4.55 | 5 |
| 3 | 656 | 0.16 | 0.81 | 5.67 | 6 |
| 4 | 329 | 0.08 | 0.89 | 6.23 | 6 |
| 5 | 245 | 0.06 | 0.95 | 6.65 | 7 |
| 6 | 122 | 0.03 | 0.98 | 6.86 | 7 |
| 7 | 81 | 0.02 | 1.00 | 7.00 | 7 |

The new histogram: level 1 gets 790, level 3 gets 1023, level 5 gets 850, level 6 gets $656+329=985$, level 7 gets $245+122+81=448$. Levels 0, 2 and 4 are empty: the output is spread over the range but is not perfectly flat, and four input levels were merged into two.
:::

Equalization is automatic (no parameters) but it is a **global** method: it can over-enhance, amplify noise in a nearly flat region, and wash out an image that was already good. **Adaptive histogram equalization (AHE)** applies the method in local tiles, and **CLAHE** (contrast-limited AHE) clips the histogram at a limit to keep noise under control; it is the default in medical and underwater imaging.

### 2.2.3 Histogram specification (matching)

Sometimes a flat histogram is not what we want. **Histogram specification** transforms an image so that its histogram matches a chosen shape $p_z(z)$. The method equalizes twice: find $s=T(r)$ that equalizes the input, find $G(z)$ that equalizes the *desired* histogram, and apply the inverse $z=G^{-1}(s)$. In the discrete case each $s_k$ is mapped to the level $z_q$ whose $G(z_q)$ is closest to $s_k$. Uses: making two photographs of the same scene (taken in different light) comparable, or matching a scan to a reference. The result depends on how well $G$ can be inverted, and a poorly chosen target gives artefacts.

```python
import numpy as np

def equalize(img, L=256):
    h = np.bincount(img.ravel(), minlength=L)
    cdf = np.cumsum(h) / img.size
    lut = np.round((L - 1) * cdf).astype(np.uint8)
    return lut[img], h, lut

# The textbook example: a 64 x 64 image with 8 levels and the counts used in the worked example.
counts = [790, 1023, 850, 656, 329, 245, 122, 81]
img3 = np.repeat(np.arange(8), counts).astype(np.uint8)
out3, h, lut3 = equalize(img3, L=8)
print("mapping r -> s :", dict(zip(range(8), lut3.tolist())))
print("new counts     :", np.bincount(out3, minlength=8).tolist())

# A dark, low-contrast 8-bit image.
rng = np.random.default_rng(11)
img = np.clip(rng.normal(60, 18, (128, 128)), 0, 255).astype(np.uint8)
eq, h, lut = equalize(img)
print("before: min %3d max %3d mean %6.2f std %5.2f  distinct levels %d" % (img.min(), img.max(), img.mean(), img.std(), len(np.unique(img))))
print("after : min %3d max %3d mean %6.2f std %5.2f  distinct levels %d" % (eq.min(), eq.max(), eq.mean(), eq.std(), len(np.unique(eq))))

# Equalizing twice changes almost nothing (the operation is nearly idempotent).
eq2, _, _ = equalize(eq)
print("second pass changes %.1f%% of the pixels" % (100 * np.mean(eq2 != eq)))

# Histogram specification: match the image to a target Gaussian-shaped histogram centred at 150.
def match(img, target_pdf):
    s = np.cumsum(np.bincount(img.ravel(), minlength=256)) / img.size
    G = np.cumsum(target_pdf) / target_pdf.sum()
    lut = np.searchsorted(G, s).clip(0, 255).astype(np.uint8)   # smallest z with G(z) >= s
    return lut[img]
z = np.arange(256)
target = np.exp(-0.5 * ((z - 150) / 30.0) ** 2)
m = match(img, target)
print("matched to N(150, 30): mean %.1f  std %.1f  (target mean 150, std 30)" % (m.mean(), m.std()))
```
```output
mapping r -> s : {0: 1, 1: 3, 2: 5, 3: 6, 4: 6, 5: 7, 6: 7, 7: 7}
new counts     : [0, 790, 0, 1023, 0, 850, 985, 448]
before: min   0 max 129 mean  59.61 std 18.01  distinct levels 127
after : min   0 max 255 mean 129.51 std 73.63  distinct levels 83
second pass changes 0.0% of the pixels
matched to N(150, 30): mean 150.8  std 30.0  (target mean 150, std 30)
```
::: tip Exam tip
When asked to equalize a small histogram, always present the table (level, count, probability, cumulative probability, $(L-1)\times$ cumulative, rounded level) and then the new histogram obtained by *adding the counts of levels that map to the same value*. Examiners award marks for each column.
:::

## 2.3 Spatial filtering

### 2.3.1 Correlation, convolution and masks

**Spatial filtering** replaces each pixel by a function of the pixels in a small neighbourhood. A **linear filter** uses a **mask** (kernel, template, window) $w$ of odd size $m\times n$ (3 x 3, 5 x 5). The response at $(x,y)$ is the sum of products of the mask coefficients and the pixels beneath them:

$$g(x,y)=\sum_{s=-a}^{a}\sum_{t=-b}^{b}w(s,t)\,f(x+s,\,y+t),\qquad a=\tfrac{m-1}{2},\; b=\tfrac{n-1}{2}.$$

This is **correlation**. **Convolution** is the same with the mask rotated by 180 degrees, $g=\sum w(s,t)f(x-s,y-t)$; for a symmetric mask (most smoothing masks) the two are identical. The procedure: slide the mask centre over every pixel, multiply, add, and store the sum at the centre pixel of the *output* (never overwrite the input in place, or later pixels would see modified neighbours). At the border the mask hangs outside the image, so one **pads** the image with zeros, replicates the edge or reflects it, or simply skips the border. A **non-linear filter** (median, min, max) ranks the neighbourhood instead of weighting it.

### 2.3.2 Smoothing (low-pass) filters

Smoothing blurs the image and reduces noise and small detail: it is a **low-pass** filter, because it passes slowly varying (low-frequency) content and weakens rapid changes. The **averaging (box) filter** is a mask of ones divided by their sum:

$$\frac19\begin{bmatrix}1&1&1\\1&1&1\\1&1&1\end{bmatrix}.$$

A **weighted average** gives more weight to the centre to blur less:

$$\frac1{16}\begin{bmatrix}1&2&1\\2&4&2\\1&2&1\end{bmatrix}$$

(a sampled Gaussian). Larger masks blur more: the 3 x 3 mask removes fine noise, a 15 x 15 mask removes everything except large blobs, which is sometimes used to find large objects of interest. Disadvantages: edges are blurred along with the noise.

The **median filter** is a non-linear **order-statistic** filter that replaces the pixel with the median of the neighbourhood. It is excellent for **salt-and-pepper (impulse) noise**: an extreme value is never the median, so it is removed instead of smeared, and edges stay sharp. Its drawbacks are the loss of thin lines and corners with a large window, and the cost of sorting. The **max** and **min** filters take the largest or smallest value (the max filter removes pepper noise, the min filter removes salt noise).

### 2.3.3 Sharpening (high-pass) filters

Sharpening highlights fine detail and edges. Because smoothing is averaging, which is like integration, sharpening is **differentiation**. A digital first derivative is a difference, $\partial f/\partial x=f(x+1)-f(x)$, and the second derivative is $\partial^{2}f/\partial x^{2}=f(x+1)+f(x-1)-2f(x)$. The second derivative is zero on flat areas and ramps, positive then negative at the two sides of an edge, a "double edge" response that enhances fine detail more than the first derivative. The isotropic **Laplacian**,

$$\nabla^{2}f=\frac{\partial^{2}f}{\partial x^{2}}+\frac{\partial^{2}f}{\partial y^{2}}=f(x+1,y)+f(x-1,y)+f(x,y+1)+f(x,y-1)-4f(x,y),$$

has masks

$$\begin{bmatrix}0&1&0\\1&-4&1\\0&1&0\end{bmatrix},\qquad\begin{bmatrix}1&1&1\\1&-8&1\\1&1&1\end{bmatrix}$$

(coefficients sum to zero, so flat areas give zero). To obtain the sharpened image the Laplacian is added back to the original: $g=f+c\,\nabla^{2}f$ with $c=-1$ when the centre coefficient is negative. With the centre-negative mask this is the single mask with centre 5 and four neighbours of $-1$ ($c=-1$): $\begin{bmatrix}0&-1&0\\-1&5&-1\\0&-1&0\end{bmatrix}$.

**Unsharp masking and high-boost filtering.** Printers have long sharpened images by subtracting a blurred copy from the original: the mask $g_{mask}=f-\bar f$ contains only the edges and detail, and

$$g=f+k\,g_{mask},\qquad k\ge0 .$$

With $k=1$ this is unsharp masking; with $k>1$ it is **high-boost filtering**, which emphasizes the high frequencies while keeping the low-frequency content (a plain high-pass filter would discard it and the result would look dark). **Gradient** methods (Sobel, Prewitt; first derivatives) use the magnitude $|\nabla f|\approx|G_x|+|G_y|$, they are used chiefly for edge detection and are treated in Unit 5.

### 2.3.4 Low-pass, high-pass and band-pass spatial filters

| Filter | Mask property | Effect |
|---|---|---|
| Low-pass | All coefficients positive, sum = 1 | Blurs, removes noise, keeps the background |
| High-pass | Positive centre, negative surround, sum = 0 | Keeps edges and detail, background goes to zero |
| Band-pass | Difference of two low-pass filters (a Difference of Gaussians, DoG) | Keeps one band of detail sizes, rejects the finest noise and the coarse background |

A high-pass image can be made as original minus low-pass: $f_{hp}=f-f_{lp}$. A band-pass response is $f_{lp,\sigma_1}-f_{lp,\sigma_2}$ with $\sigma_1<\sigma_2$.

```python
import numpy as np

def filt(img, w, pad="edge"):
    """Correlation of img with an odd-sized mask w, same-size output (float)."""
    m, n = w.shape; a, b = m // 2, n // 2
    p = np.pad(img.astype(float), ((a, a), (b, b)), mode=pad)
    out = np.zeros(img.shape)
    for s in range(m):
        for t in range(n):
            out += w[s, t] * p[s:s + img.shape[0], t:t + img.shape[1]]
    return out

def median3(img):
    p = np.pad(img, 1, mode="edge")
    stack = np.stack([p[i:i + img.shape[0], j:j + img.shape[1]] for i in range(3) for j in range(3)])
    return np.median(stack, axis=0)

# Test image: a bright square on a dark background.
n = 48
img = np.full((n, n), 60.0); img[12:36, 12:36] = 180.0
rng = np.random.default_rng(5)
noisy = img.copy()
mask = rng.random(img.shape)
noisy[mask < 0.05] = 0; noisy[mask > 0.95] = 255          # 10% salt-and-pepper noise
mse = lambda a: float(np.mean((a - img) ** 2))
box = np.ones((3, 3)) / 9
gau = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
print("noisy image        MSE = %7.1f" % mse(noisy))
print("3x3 box filter     MSE = %7.1f" % mse(filt(noisy, box)))
print("3x3 Gaussian       MSE = %7.1f" % mse(filt(noisy, gau)))
print("3x3 median filter  MSE = %7.1f" % mse(median3(noisy)))

# Sharpening the (clean) edge: Laplacian, and unsharp masking / high-boost.
blur = filt(img, gau)
lap = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)
L = filt(img, lap)
print("Laplacian response: min %.0f  max %.0f  sum %.0f (zero on flat areas)" % (L.min(), L.max(), L.sum()))
sharp = np.clip(img - L, 0, 255)
print("row 24 across the edge (original) :", img[24, 9:16].astype(int).tolist())
print("row 24 blurred                    :", np.round(blur[24, 9:16]).astype(int).tolist())
print("row 24 Laplacian-sharpened        :", sharp[24, 9:16].astype(int).tolist())
for k in (1, 2):
    hb = np.clip(img + k * (img - blur), 0, 255)
    print("high-boost k=%d, row 24             :" % k, np.round(hb[24, 9:16]).astype(int).tolist())

# Band-pass as a difference of two Gaussians (sigma 1 and sigma 3).
def gauss_kernel(sig, r=9):
    ax = np.arange(-r, r + 1); g = np.exp(-(ax ** 2) / (2 * sig ** 2)); k = np.outer(g, g); return k / k.sum()
dog = filt(img, gauss_kernel(1.0)) - filt(img, gauss_kernel(3.0))
print("DoG band-pass: flat interior %.2f, response at the edge %.2f" % (dog[24, 24], dog[24, 12]))
```
```output
noisy image        MSE =  2164.6
3x3 box filter     MSE =   430.3
3x3 Gaussian       MSE =   440.3
3x3 median filter  MSE =    37.5
Laplacian response: min -240  max 120  sum 0 (zero on flat areas)
row 24 across the edge (original) : [60, 60, 60, 180, 180, 180, 180]
row 24 blurred                    : [60, 60, 90, 150, 180, 180, 180]
row 24 Laplacian-sharpened        : [60, 60, 0, 255, 180, 180, 180]
high-boost k=1, row 24             : [60, 60, 30, 210, 180, 180, 180]
high-boost k=2, row 24             : [60, 60, 0, 240, 180, 180, 180]
DoG band-pass: flat interior -0.00, response at the edge 15.95
```
## 2.4 Image transforms

A **transform** re-expresses the image as a weighted sum of basis images. Working in the transform domain is useful for two reasons: some operations (filtering, convolution with a large mask) become simple multiplications, and some transforms concentrate the information in a few coefficients (compression, Unit 4). All the transforms here are **separable** (the 2-D transform is a 1-D transform of the rows followed by a 1-D transform of the columns) and invertible.

### 2.4.1 The Fourier transform and the DFT

Fourier showed that any signal can be written as a sum of sines and cosines of different frequencies. For an image, frequency means **rate of change of intensity over distance**: smooth regions are low frequency, edges, texture and noise are high frequency. The 1-D **discrete Fourier transform** of $N$ samples $f(x)$ is

$$F(u)=\sum_{x=0}^{N-1}f(x)\,e^{-j2\pi ux/N},\qquad f(x)=\frac1N\sum_{u=0}^{N-1}F(u)\,e^{\,j2\pi ux/N},$$

and the 2-D DFT of an $M\times N$ image is

$$F(u,v)=\sum_{x=0}^{M-1}\sum_{y=0}^{N-1}f(x,y)\,e^{-j2\pi(ux/M+vy/N)},\qquad f(x,y)=\frac1{MN}\sum_{u}\sum_{v}F(u,v)\,e^{\,j2\pi(ux/M+vy/N)}.$$

$F(u,v)$ is complex. Its **magnitude** $|F|=\sqrt{R^{2}+I^{2}}$ is the **Fourier spectrum**, the **phase** $\phi=\tan^{-1}(I/R)$ and the **power spectrum** $|F|^{2}$. $F(0,0)=\sum\sum f(x,y)$ is $MN$ times the average grey level (the **DC term**).

**Properties** that matter in practice:

- **Separability**: $F(u,v)$ can be computed as 1-D DFTs along rows then columns.
- **Translation**: moving the image changes only the phase, not the spectrum magnitude. Multiplying $f(x,y)$ by $(-1)^{x+y}$ **centres** the spectrum, moving $F(0,0)$ to the middle of the display with low frequencies near the centre.
- **Periodicity and symmetry**: $F$ is periodic with period $N$; for a real image $F(-u,-v)=F^{*}(u,v)$ (conjugate symmetry), so the spectrum is symmetric about the origin.
- **Rotation**: rotating $f$ by $\theta$ rotates $F$ by $\theta$.
- **Convolution theorem**: convolution in space equals multiplication in frequency, $f*h\;\Longleftrightarrow\;F\cdot H$, and the converse. This is why frequency-domain filters work.
- **Linearity** and **Parseval's theorem** (energy is preserved, up to the factor $MN$).

Reading a spectrum: bright spots near the centre mean slowly varying content; energy along a line at right angles to an edge in the image; a regular pattern of dots away from the centre is periodic noise or texture; the centre usually dominates, so spectra are displayed after $\log(1+|F|)$ (Section 2.1.2).

### 2.4.2 The fast Fourier transform

Computing the $N$ outputs of a 1-D DFT directly takes $N^{2}$ complex multiplications. The **fast Fourier transform (FFT)** of Cooley and Tukey (1965) uses the factorization $F(u)=F_{even}(u)+W_N^{u}F_{odd}(u)$ with $W_N=e^{-j2\pi/N}$: a DFT of size $N$ is built from two DFTs of size $N/2$ (the even- and odd-numbered samples), recursively, until size 1. The result needs about $\tfrac N2\log_{2}N$ multiplications, so for $N=1024$ the speed-up is about $1024^{2}/(512\times10)\approx205$ times. A 2-D transform of an $N\times N$ image needs $2N$ 1-D FFTs, $O(N^{2}\log N)$ instead of $O(N^{4})$ for a direct 2-D sum. The standard radix-2 version needs $N$ to be a power of 2 (pad with zeros otherwise).

### 2.4.3 The discrete cosine transform

The **DCT** expresses a signal using only cosines. For $N$ samples the 1-D DCT (type II) is

$$C(u)=\alpha(u)\sum_{x=0}^{N-1}f(x)\cos\!\left[\frac{(2x+1)u\pi}{2N}\right],\qquad \alpha(0)=\sqrt{\tfrac1N},\;\alpha(u>0)=\sqrt{\tfrac2N},$$

and the 2-D DCT is the product of two such sums, $C(u,v)=\alpha(u)\alpha(v)\sum\sum f(x,y)\cos[\cdot]\cos[\cdot]$. Compared with the DFT: the DCT is **real** (no phase to store), it implies a symmetric extension of the signal rather than a periodic one, so there are no jumps at the borders and far less leakage, and it has an excellent **energy compaction** property: for typical images almost all the energy lies in a few low-frequency coefficients near the top-left corner $(0,0)$. This is why JPEG uses an $8\times8$ DCT (Unit 4). The DCT is orthonormal, so the inverse is the transpose and energy is preserved.

```python
import numpy as np

# 1. DFT by the definition against the FFT, and the operation counts.
rng = np.random.default_rng(2)
x = rng.integers(0, 256, 64).astype(float)
N = len(x)
u = np.arange(N)
W = np.exp(-2j * np.pi * np.outer(u, u) / N)
F_def = W @ x
print("DFT by definition equals FFT:", np.allclose(F_def, np.fft.fft(x)))
for n in (64, 1024, 4096):
    print("N = %4d: direct %9d multiplications, FFT about %7d, speed-up %5.0fx" %
          (n, n * n, n // 2 * int(np.log2(n)), n * n / (n / 2 * np.log2(n))))

# 2. Properties of the 2-D DFT on a small image.
img = np.zeros((32, 32)); img[8:24, 12:20] = 200.0         # a bright bar
F = np.fft.fft2(img)
print("F(0,0) = %.0f,  MN x mean = %.0f" % (F[0, 0].real, img.size * img.mean()))
print("Parseval: sum |f|^2 = %.4g,  sum |F|^2 / MN = %.4g" % ((img ** 2).sum(), (np.abs(F) ** 2).sum() / img.size))
shifted = np.roll(img, (5, 3), axis=(0, 1))
print("magnitude unchanged by translation:", np.allclose(np.abs(np.fft.fft2(shifted)), np.abs(F)))
back = np.fft.ifft2(F).real
print("inverse transform recovers the image:", np.allclose(back, img))
print("conjugate symmetry F(-u,-v) = conj F(u,v):", np.allclose(F[(-3) % 32, (-5) % 32], np.conj(F[3, 5])))

# 3. Convolution theorem: circular convolution with a 3x3 mean equals multiplication of spectra.
h = np.zeros((32, 32)); h[:3, :3] = 1 / 9
conv = np.fft.ifft2(np.fft.fft2(img) * np.fft.fft2(h)).real
direct = sum(np.roll(img, (a, b), axis=(0, 1)) for a in range(3) for b in range(3)) / 9
print("spectral product equals spatial 3x3 averaging:", np.allclose(conv, direct))

# 4. DCT energy compaction on an 8 x 8 smooth block.
def dct_matrix(n):
    C = np.zeros((n, n))
    for k in range(n):
        for i in range(n):
            C[k, i] = np.sqrt((1 if k == 0 else 2) / n) * np.cos((2 * i + 1) * k * np.pi / (2 * n))
    return C
C8 = dct_matrix(8)
block = np.add.outer(np.arange(8) * 6.0, np.arange(8) * 3.0) + 100       # a smooth ramp
D = C8 @ block @ C8.T
energy = D ** 2
order = np.argsort(energy.ravel())[::-1]
cum = np.cumsum(energy.ravel()[order]) / energy.sum()
print("DCT of a smooth 8x8 block: %.2f%% of the energy in the largest 1 coefficient, %.2f%% in the largest 3" % (100 * cum[0], 100 * cum[2]))
print("top-left 3 x 3 coefficients:\n", np.round(D[:3, :3], 1))
print("orthonormal (inverse = transpose):", np.allclose(C8.T @ D @ C8, block))
```
```output
DFT by definition equals FFT: True
N =   64: direct      4096 multiplications, FFT about     192, speed-up    21x
N = 1024: direct   1048576 multiplications, FFT about    5120, speed-up   205x
N = 4096: direct  16777216 multiplications, FFT about   24576, speed-up   683x
F(0,0) = 25600,  MN x mean = 25600
Parseval: sum |f|^2 = 5.12e+06,  sum |F|^2 / MN = 5.12e+06
magnitude unchanged by translation: True
inverse transform recovers the image: True
conjugate symmetry F(-u,-v) = conj F(u,v): True
spectral product equals spatial 3x3 averaging: True
DCT of a smooth 8x8 block: 98.65% of the energy in the largest 1 coefficient, 99.98% in the largest 3
top-left 3 x 3 coefficients:
 [[1052.   -54.7   -0. ]
 [-109.3   -0.     0. ]
 [  -0.     0.    -0. ]]
orthonormal (inverse = transpose): True
```
## 2.5 Frequency-domain image enhancement

### 2.5.1 The method

By the convolution theorem, filtering in the frequency domain means multiplying the spectrum by a **transfer function** $H(u,v)$:

$$G(u,v)=H(u,v)\,F(u,v),\qquad g(x,y)=\mathrm{Re}\{\mathcal F^{-1}[G(u,v)]\}.$$

Steps: (1) multiply the image by $(-1)^{x+y}$ to centre the spectrum (or shift the result); (2) compute the DFT $F(u,v)$; (3) multiply by a symmetric filter $H(u,v)$; (4) compute the inverse DFT; (5) take the real part and multiply by $(-1)^{x+y}$ again. For images, to avoid **wrap-around error** (the DFT assumes a periodic image) the image and the filter are first padded with zeros to size $P\ge M+m-1$. The filters are given in terms of $D(u,v)$, the distance from the centre of the (centred) spectrum, $D(u,v)=\sqrt{(u-P/2)^{2}+(v-Q/2)^{2}}$, and a **cut-off frequency** $D_0$.

```svgfig label="2.2" caption="Radial profiles of low-pass transfer functions with cut-off D0 = 30 (left) and the high-pass filters obtained as 1 - H (right). The ideal filter drops straight from 1 to 0 and rings; the Butterworth filter (order 2) is smoother; the Gaussian filter has no ringing at all."
import math
f = Fig(680, 310)
ax = Axes(f, 55, 20, 260, 230, (0, 100), (0, 1.1))
ax.grid(dx=25, dy=0.5)
ax.axes(xl="D(u,v)", yl="H")
ax.curve(lambda d: 1.0 if d <= 30 else 0.0, color=RED, sw=2.2, n=600)
ax.curve(lambda d: 1 / (1 + (d / 30) ** 4), color=AMBER, sw=2.2)
ax.curve(lambda d: math.exp(-d * d / (2 * 30 * 30)), color=TEAL, sw=2.2)
bx = Axes(f, 395, 20, 260, 230, (0, 100), (0, 1.1))
bx.grid(dx=25, dy=0.5)
bx.axes(xl="D(u,v)", yl="H")
bx.curve(lambda d: 0.0 if d <= 30 else 1.0, color=RED, sw=2.2, n=600)
bx.curve(lambda d: 1 - 1 / (1 + (d / 30) ** 4), color=AMBER, sw=2.2)
bx.curve(lambda d: 1 - math.exp(-d * d / (2 * 30 * 30)), color=TEAL, sw=2.2)
f.text(185, 286, "Low-pass: ideal (red), Butterworth (amber), Gaussian (teal)", size=9.5, color=SLATE)
f.text(525, 286, "High-pass: the same three as 1 - H", size=9.5, color=SLATE)
```

### 2.5.2 Low-pass filters (smoothing)

Low-pass filters pass the frequencies inside the circle of radius $D_0$ and weaken the rest: blur and noise reduction.

| Filter | $H(u,v)$ | Behaviour |
|---|---|---|
| **Ideal** (ILPF) | $1$ if $D\le D_0$, else $0$ | Sharp cut-off; cannot be built with analogue parts; produces **ringing** (ripples round edges, since its spatial form is a sinc) |
| **Butterworth** (BLPF), order $n$ | $\dfrac{1}{1+[D/D_0]^{2n}}$ | Smooth transition; ringing is slight for $n=1$ or 2 and grows as $n$ increases (towards the ideal) |
| **Gaussian** (GLPF) | $e^{-D^{2}/2D_0^{2}}$ | No ringing at all; its inverse transform is also Gaussian; smoothest result |

At $D=D_0$ the ideal filter jumps, the Butterworth equals 0.5, and the Gaussian equals $e^{-1/2}\approx0.607$. A small $D_0$ removes most of the image's power and gives heavy blur; the **percentage of power** inside radius $D_0$, $\alpha=100\sum_{(u,v)\in D_0}P(u,v)/P_T$, is used to choose it (for example, $D_0$ enclosing 90% of the power).

### 2.5.3 High-pass filters (sharpening)

A high-pass filter is $H_{hp}=1-H_{lp}$: it kills the low frequencies (the smooth background, the DC term) and keeps edges and detail. The ideal (IHPF), Butterworth (BHPF) and Gaussian (GHPF) versions behave like their low-pass counterparts, with ringing in the ideal one. Since removing $F(0,0)$ makes the average zero and the image dark, one adds a constant to the filter, **high-frequency emphasis**: $H_{hfe}=a+b\,H_{hp}$ with $a\ge0$ and $b>a$ (typical $a=0.5$, $b=1.5$ to 2), which boosts the high frequencies while keeping the low ones, the frequency-domain twin of high-boost filtering. A **band-pass** filter is $H_{lp,D_2}-H_{lp,D_1}$, and a **notch** filter, which zeros small blobs at symmetric positions $(\pm u_0,\pm v_0)$, removes periodic noise such as the stripes of a scanned halftone or a power-line pattern.

### 2.5.4 Homomorphic filtering

An image formed as $f=i\cdot r$ (Section 1.4.1) has the slowly varying illumination $i$ in the low frequencies and the quickly varying reflectance $r$ (detail, edges) in the high frequencies, but the product cannot be separated by a linear filter. The **homomorphic filter** takes the logarithm first, which turns the product into a sum,

$$\ln f(x,y)=\ln i(x,y)+\ln r(x,y)\;\xrightarrow{\ \mathrm{DFT}\ }\;Z(u,v)=F_i(u,v)+F_r(u,v),$$

applies a filter $H(u,v)$ that *attenuates* the low frequencies ($\gamma_L<1$) and *amplifies* the high ones ($\gamma_H>1$), takes the inverse DFT, and finishes with the exponential:

$$g(x,y)=\exp\{\mathcal F^{-1}[H(u,v)\,Z(u,v)]\},\qquad H(u,v)=(\gamma_H-\gamma_L)\Big[1-e^{-c\,D^{2}/D_0^{2}}\Big]+\gamma_L .$$

The result simultaneously **compresses the dynamic range** (uneven lighting is flattened) and **improves contrast** (detail is boosted): it rescues a photograph in which an object in shadow is invisible, and is used on X-rays and on face images under uneven light. Typical values are $\gamma_L=0.5$, $\gamma_H=2$, $c=1$.

```python
import numpy as np

def make_D(P, Q):
    u = np.arange(P) - P // 2; v = np.arange(Q) - Q // 2
    return np.sqrt(np.add.outer(u ** 2, v ** 2))

def freq_filter(img, H):
    F = np.fft.fftshift(np.fft.fft2(img))
    return np.fft.ifft2(np.fft.ifftshift(F * H)).real

n = 64
img = np.full((n, n), 80.0); img[16:48, 16:48] = 180.0
rng = np.random.default_rng(4)
noisy = img + rng.normal(0, 25, img.shape)
D = make_D(n, n); D0 = 12
H_ideal = (D <= D0).astype(float)
H_but = 1 / (1 + (D / D0) ** 4)
H_gau = np.exp(-D ** 2 / (2 * D0 ** 2))
mse = lambda a, b=img: float(np.mean((a - b) ** 2))
print("noisy MSE vs clean: %.1f" % mse(noisy))
for name, H in (("ideal", H_ideal), ("Butterworth n=2", H_but), ("Gaussian", H_gau)):
    out = freq_filter(noisy, H)
    clean_out = freq_filter(img, H)
    print("%-16s LPF D0=%d: MSE %.1f, overshoot above 180 on the clean square: %.1f (ringing), undershoot below 80: %.1f" %
          (name, D0, mse(out), max(clean_out.max() - 180, 0), max(80 - clean_out.min(), 0)))
print("H at D = D0: ideal %.2f, Butterworth %.2f, Gaussian %.3f" % (1.0, 1 / (1 + 1), np.exp(-0.5)))

# Power inside radius D0 of the clean image spectrum.
P = np.abs(np.fft.fftshift(np.fft.fft2(img))) ** 2
print("share of the power within D <= %d: %.1f%%" % (D0, 100 * P[D <= D0].sum() / P.sum()))

# High-pass (1 - Gaussian low-pass) and high-frequency emphasis on the clean image.
Hhp = 1 - np.exp(-D ** 2 / (2 * 8.0 ** 2))
hp = freq_filter(img, Hhp)
hfe = freq_filter(img, 0.5 + 1.5 * Hhp)
print("high-pass: mean %.2f (background removed), max |response| %.1f" % (hp.mean(), np.abs(hp).max()))
print("high-frequency emphasis (a = 0.5, b = 1.5): mean %.1f = a x original mean %.1f, so the background survives at half level" % (hfe.mean(), img.mean()))

# Homomorphic filter: uneven illumination (a left-to-right ramp) times a reflectance pattern.
x = np.arange(n)
illum = np.tile(10 + 90 * x / (n - 1), (n, 1))                 # 10 .. 100: strong shading
refl = np.full((n, n), 0.7); refl[:, 8::16] = 0.2; refl[:, 9::16] = 0.2   # dark thin stripes
f = illum * refl
Hh = (2.0 - 0.5) * (1 - np.exp(-1.0 * D ** 2 / 6.0 ** 2)) + 0.5
g = np.exp(freq_filter(np.log(f), Hh))
print("left/right brightness ratio of the background  : before %.2f  after %.2f (1.0 = even)" % (f[:, 20:26].mean() / f[:, 50:56].mean(), g[:, 20:26].mean() / g[:, 50:56].mean()))
print("stripe / background brightness in the dim left (smaller = stronger stripes): before %.2f  after %.2f" % (f[:, 8].mean() / f[:, 4].mean(), g[:, 8].mean() / g[:, 4].mean()))
```
```output
noisy MSE vs clean: 619.9
ideal            LPF D0=12: MSE 138.0, overshoot above 180 on the clean square: 18.1 (ringing), undershoot below 80: 11.2
Butterworth n=2  LPF D0=12: MSE 108.0, overshoot above 180 on the clean square: 5.9 (ringing), undershoot below 80: 3.4
Gaussian         LPF D0=12: MSE 109.2, overshoot above 180 on the clean square: 0.1 (ringing), undershoot below 80: 0.1
H at D = D0: ideal 1.00, Butterworth 0.50, Gaussian 0.607
share of the power within D <= 12: 99.4%
high-pass: mean -0.00 (background removed), max |response| 56.9
high-frequency emphasis (a = 0.5, b = 1.5): mean 52.5 = a x original mean 105.0, so the background survives at half level
left/right brightness ratio of the background  : before 0.37  after 0.53 (1.0 = even)
stripe / background brightness in the dim left (smaller = stronger stripes): before 0.39  after 0.17
```
## 2.6 Summary and exercises

Enhancement works in the spatial domain ($g=T[f]$) or the frequency domain ($G=HF$). Point processing uses a curve $s=T(r)$: negative, log, power law, contrast stretching, clipping, thresholding and slicing. The histogram $p(r_k)=n_k/MN$ summarizes the grey-level distribution, and equalization uses the cumulative distribution, $s_k=(L-1)\sum p$, to flatten it; histogram specification matches a chosen shape. Spatial filters slide a mask over the image: averaging and Gaussian masks smooth, the median filter removes impulse noise, the Laplacian and unsharp masking sharpen, and low-, high- and band-pass masks pass a range of spatial frequencies. The DFT (computed by the FFT in $O(N\log N)$) represents the image by frequencies; the DCT is real and compacts energy. Frequency filters multiply the spectrum by an ideal, Butterworth or Gaussian transfer function; the ideal filter rings, and the homomorphic filter separates illumination from reflectance with a logarithm.

1. Define image enhancement. Distinguish the spatial and frequency domain approaches.
2. State the formulae, effect and one use of the negative, log and power-law transformations.
3. What is contrast stretching? Write the piecewise-linear form, and distinguish it from clipping and thresholding.
4. Explain intensity-level slicing and bit-plane slicing.
5. Define the histogram of an image. Sketch the histograms of a dark, a bright, a low-contrast and a high-contrast image.
6. Derive the histogram equalization transform. Why is the result of equalizing a digital image only approximately flat?
7. A 4 x 4 image with 3 bits per pixel has the counts of levels 0 to 7: 2, 3, 4, 3, 2, 1, 1, 0. Equalize it and give the new histogram.
8. In an 8-bit image find the negative of 200, the log transform ($s=c\ln(1+r)$, with $c$ chosen so that 255 maps to 255) of $r=15$, and the gamma transform ($\gamma=0.5$) of $r=64$.
9. The grey levels of an image lie between 80 and 140. Where does min-max stretching to 0 to 255 send the level 100?
10. What is histogram specification? Outline the procedure.
11. Compare correlation and convolution. How is the border handled?
12. For the window rows (10, 20, 30), (40, 250, 60), (70, 80, 90) find the 3 x 3 mean and median at the centre. Which one suits impulse noise and why?
13. Apply the 4-neighbour Laplacian mask to the window rows (10, 10, 10), (10, 50, 10), (10, 10, 10), and find the Laplacian-sharpened value $f-\nabla^{2}f$ at the centre.
14. Explain unsharp masking and high-boost filtering. A pixel has value 50 and its blurred value is 30. Find the high-boost output for $k=2$.
15. Compare low-pass, high-pass and band-pass spatial filters with a mask for each.
16. Write the 1-D DFT and compute it for $f=(1,2,3,4)$.
17. List five properties of the 2-D DFT. How is the spectrum displayed and why is the log used?
18. How does the FFT reduce the cost of the DFT? Compare the multiplication counts for $N=256$.
19. State the 1-D DCT. Why is the DCT preferred to the DFT for compression?
20. Describe the steps of frequency-domain filtering. Why is padding needed?
21. Compare ideal, Butterworth and Gaussian low-pass filters. What is ringing? Find $H$ at $D=2D_0$ for a Butterworth (order 2) and a Gaussian filter.
22. Explain homomorphic filtering with a block diagram and the transfer function. Find $H$ at $D=D_0$ for $\gamma_L=0.5$, $\gamma_H=2$, $c=1$.

**Answers to the numerical items.** (7) Cumulative counts 2, 5, 9, 12, 14, 15, 16, 16; multiplying by $7/16$ gives 0.875, 2.19, 3.94, 5.25, 6.13, 6.56, 7, 7, which round to 1, 2, 4, 5, 6, 7, 7, 7. New histogram: level 1 has 2, level 2 has 3, level 4 has 4, level 5 has 3, level 6 has 2 and level 7 has $1+1+0=2$ pixels (total 16). (8) Negative $=255-200=\mathbf{55}$. $c=255/\ln256=255/5.545=45.99$, so $s=45.99\ln16=45.99\times2.773=127.5\approx\mathbf{128}$. Gamma: $s=255(64/255)^{0.5}=255\times0.501=127.8\approx\mathbf{128}$. (9) $255\times(100-80)/(140-80)=255/3=\mathbf{85}$. (12) Mean $=650/9=\mathbf{72.2}$; sorted values 10, 20, 30, 40, 60, 70, 80, 90, 250 give median **60**. The median suits impulse noise: the outlier 250 pulls the mean to 72 but never becomes the median. (13) $\nabla^{2}f=10+10+10+10-4\times50=-160$; $g=50-(-160)=\mathbf{210}$ (clipped to 255 at most). (14) $g=50+2(50-30)=\mathbf{90}$. (16) $F(0)=10$; $F(1)=1+2(-j)+3(-1)+4(j)=\mathbf{-2+2j}$; $F(2)=1-2+3-4=\mathbf{-2}$; $F(3)=\mathbf{-2-2j}$. (18) Direct: $256^{2}=65{,}536$; FFT: $128\times8=1024$; about **64 times** fewer. (21) Butterworth: $1/(1+2^{4})=1/17=\mathbf{0.059}$; Gaussian: $e^{-4/2}=e^{-2}=\mathbf{0.135}$. (22) $H=(2-0.5)(1-e^{-1})+0.5=1.5\times0.632+0.5=\mathbf{1.45}$.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is histogram equalization? Give the steps.**

Histogram equalization is an automatic point operation that makes the histogram of the output image close to uniform, so that the grey levels use the whole range and contrast improves. The transformation is the cumulative distribution function of the input, $s_k=(L-1)\sum_{j\le k}n_j/MN$. Steps: compute the histogram $n_k$; the probabilities $p(r_k)=n_k/MN$; the cumulative sum; multiply by $L-1$; round to integers; replace each pixel $r_k$ by $s_k$. Because levels can only be merged, never split, the output is approximately and not exactly flat. It enhances well when the useful information is in a narrow band, but it is global, so it can over-enhance noise; CLAHE is used in that case.

**Q2 (5 marks). Distinguish smoothing and sharpening spatial filters.**

Smoothing (low-pass) filters average the neighbourhood: the mask has positive coefficients that sum to 1 (for example 1/9 times a 3 x 3 mask of ones). They reduce noise and fine detail but blur edges. The median filter is a non-linear smoothing filter, best for impulse noise. Sharpening (high-pass) filters differentiate: the mask has a positive centre and negative surroundings with coefficients that sum to 0 (the Laplacian with centre $-4$). They emphasize edges and fine detail but amplify noise. Sharpening is obtained by adding the filtered result to the image, $g=f-\nabla^{2}f$, or by high-boost filtering $g=f+k(f-\bar f)$.

**Q3 (10 marks). Explain frequency-domain filtering with ideal, Butterworth and Gaussian low-pass filters.**

State the principle: by the convolution theorem $G(u,v)=H(u,v)F(u,v)$. Give the five steps (centre, DFT, multiply, inverse DFT, real part and un-centre) and mention zero-padding to avoid wrap-around. Define $D(u,v)$ and the cut-off $D_0$. Give the three filters: ideal ($H=1$ for $D\le D_0$, else 0), Butterworth ($1/(1+[D/D_0]^{2n})$) and Gaussian ($e^{-D^{2}/2D_0^{2}}$); sketch the three profiles as in Figure 2.2. Compare: the ideal filter has a sharp cut-off and causes ringing because its inverse transform is a sinc; the Butterworth filter has a smooth transition and mild ringing for low order; the Gaussian filter has no ringing. Conclude with the effect (blur and noise reduction) and the high-pass counterpart $1-H$.

**Q4 (10 marks). Describe homomorphic filtering and say why it is used.**

An image is $f=i\cdot r$ with slowly varying illumination (low frequency) and rapidly varying reflectance (high frequency). Because the product cannot be separated linearly, take the logarithm, $\ln f=\ln i+\ln r$, transform it by the DFT, multiply by a high-frequency-emphasis filter $H(u,v)=(\gamma_H-\gamma_L)[1-e^{-cD^{2}/D_0^{2}}]+\gamma_L$ with $\gamma_L<1<\gamma_H$, apply the inverse DFT and take the exponential. Draw the block diagram: $f\to\ln\to$ DFT $\to H\to$ IDFT $\to\exp\to g$. The low frequencies (illumination) are attenuated, so uneven lighting is flattened, and the high frequencies (detail) are amplified, so contrast improves. It is used for images with shadows or non-uniform lighting, such as X-rays and face images.

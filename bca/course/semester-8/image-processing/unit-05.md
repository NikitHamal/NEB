---
subject: Image Processing
grade: BCA Semester 8 (Elective IV)
unit: 5
title: Image Segmentation and Feature Extraction
hours: 10
area: BCA 454 · Image Processing · Unit 5
---

Enhancement, restoration and compression take an image and give an image. This last unit moves up to **mid- and high-level processing**: finding *what is in the picture*. **Segmentation** divides an image into meaningful regions (the coin against the table, the tumour against the tissue, the road against the field); **feature extraction** describes each region by numbers (area, shape, texture, colour); and **classification** assigns each region to a class. Together they are the front end of every machine-vision system, from reading a number plate to counting cells. The unit also covers the case studies named in the outline: image security, steganography and digital watermarking, visual effects, medical imaging and remote sensing.

::: key What this unit gives you
- Segmentation by thresholding (global, Otsu's method, adaptive) and region-based methods (region growing, split and merge).
- Edges, lines and curves: the gradient, Roberts, Prewitt and Sobel operators, the Laplacian of Gaussian, the Canny detector, and the Hough transform.
- Image features: boundary and region descriptors, chain codes, moments, texture (statistical, GLCM), and feature reduction with PCA.
- Image classification (minimum-distance, k-nearest-neighbour) and clustering (k-means), each with a program.
- Case studies: image encryption, steganography, watermarking, visual effects, medical imaging, remote sensing.
- A laboratory project that ties the course together.
:::

## 5.1 Image segmentation by thresholding

**Segmentation** partitions an image $R$ into $n$ regions $R_1,\dots,R_n$ such that (a) their union is $R$; (b) each $R_i$ is a connected set; (c) they do not overlap; (d) a predicate $Q(R_i)$ (for example "all pixels have similar grey level") is true for each region; and (e) $Q(R_i\cup R_j)$ is false for adjacent regions. Algorithms follow two principles: **discontinuity** (find boundaries where intensity changes abruptly: edges, Section 5.3) and **similarity** (group pixels that are alike: thresholding and regions, here).

### 5.1.1 Global thresholding

If an object is brighter (or darker) than its background, its histogram has two peaks (a **bimodal** histogram) separated by a valley. Choosing a **threshold** $T$ in the valley splits the image: $g(x,y)=1$ if $f(x,y)>T$, else 0. A single $T$ for the whole image is **global thresholding**. The basic **iterative algorithm** finds $T$ automatically: (1) guess $T$ (the mean grey level); (2) split the pixels into $G_1$ ($>T$) and $G_2$ ($\le T$); (3) compute the means $m_1$ and $m_2$; (4) set $T=\tfrac12(m_1+m_2)$; (5) repeat until $T$ changes by less than a small $\Delta T$.

### 5.1.2 Otsu's method

When the peaks overlap, a better choice is **Otsu's method**, which picks the $T$ that **maximizes the between-class variance** (equivalently, minimizes the within-class variance). For a threshold $k$ let $P_1(k)=\sum_{i\le k}p_i$ and $P_2=1-P_1$ be the class probabilities, $m_1(k)$ and $m_2(k)$ the class means and $m_G$ the global mean. Then

$$\sigma_B^{2}(k)=P_1(m_1-m_G)^{2}+P_2(m_2-m_G)^{2}=P_1P_2\,(m_1-m_2)^{2},$$

and the threshold is

$$k^{*}=\arg\max_k\ \sigma_B^{2}(k).$$

It uses only the histogram, needs no parameters, and works well when the classes are of reasonable size; it fails when one class is tiny (the small peak is overwhelmed) or when the illumination is uneven.

```svgfig label="5.1" caption="A bimodal histogram: dark background pixels (left peak) and bright object pixels (right peak). The Otsu threshold T lies in the valley between the peaks and separates the two classes."
import math
f = Fig(640, 280)
ax = Axes(f, 60, 25, 540, 200, (0, 255), (0, 1.05))
ax.grid(dx=32, dy=0.5, labels=False)
ax.axes(xl="", yl="count")
g = lambda x, m, s, a: a * math.exp(-0.5 * ((x - m) / s) ** 2)
h = lambda x: g(x, 70, 22, 1.0) + g(x, 175, 28, 0.62)
ax.area(h, 0, 255, fill="#dbeafe", n=300)
ax.curve(h, color=NAVY, sw=2.2, n=300)
ax.vline(118, color=RED, dash=False, sw=2)
ax.tag(124, 0.93, "threshold T", size=10.5, color=RED, bold=True, anchor="start")
ax.tag(70, 0.55, "background", size=10.5, color=NAVY, bold=True)
ax.tag(190, 0.52, "object", size=10.5, color=NAVY, bold=True)
f.text(330, 246, "grey level", size=10, color=SLATE)
f.text(330, 266, "pixels below T are set to 0, pixels above T to 1", size=10, color=SLATE)
```

### 5.1.3 Variable and adaptive thresholding

With **uneven illumination** (a page photographed under a lamp, a shadow across a part) no single $T$ works. Remedies: **correct the shading** first (divide by a heavily blurred copy, or use the homomorphic filter), **partition** the image into blocks and threshold each by its own histogram, or use a **local (adaptive) threshold** from the neighbourhood of each pixel, $T(x,y)=m_{xy}-C$ or $T=m_{xy}\,(1+k(\sigma_{xy}/R-1))$ (Sauvola). **Multiple thresholds** split an image into three or more classes: $g=a$ if $f\le T_1$, $b$ if $T_1<f\le T_2$, $c$ if $f>T_2$. Smoothing the image before thresholding makes the valley deeper.

```python
import numpy as np
rng = np.random.default_rng(31)
n = 96; yy, xx = np.mgrid[0:n, 0:n]
truth = ((yy - 48) ** 2 + (xx - 40) ** 2 < 26 ** 2) | ((yy > 70) & (xx > 60) & (xx < 90))      # object mask
img = np.where(truth, 175.0, 70.0) + rng.normal(0, 18, (n, n))
img = np.clip(img, 0, 255).astype(np.uint8)

def iterative(img, dT=0.5):
    T = img.mean()
    while True:
        m1 = img[img > T].mean(); m2 = img[img <= T].mean(); Tn = 0.5 * (m1 + m2)
        if abs(Tn - T) < dT: return Tn
        T = Tn
def otsu(img):
    p = np.bincount(img.ravel(), minlength=256) / img.size
    P1 = np.cumsum(p); m = np.cumsum(p * np.arange(256)); mG = m[-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        sb = (mG * P1 - m) ** 2 / (P1 * (1 - P1))
    return int(np.nanargmax(sb)), float(np.nanmax(sb))
def accuracy(mask): return 100 * np.mean(mask == truth)

Ti = iterative(img); To, sb = otsu(img)
print("iterative threshold = %.1f, accuracy %.1f%%" % (Ti, accuracy(img > Ti)))
print("Otsu threshold      = %d,   accuracy %.1f%%  (between-class variance %.0f)" % (To, accuracy(img > To), sb))

# Uneven illumination: add a ramp so that a single global threshold fails.
shaded = np.clip(img + np.linspace(-60, 60, n)[None, :], 0, 255).astype(np.uint8)
print("shaded image: global Otsu accuracy %.1f%%" % accuracy(shaded > otsu(shaded)[0]))
# Shading correction: fit a plane to the background pixels, subtract it, then threshold (3 passes).
A = np.c_[np.ones(n * n), xx.ravel(), yy.ravel()]; z = shaded.ravel().astype(float); w = np.ones(n * n, bool)
for it in range(3):
    c = np.linalg.lstsq(A[w], z[w], rcond=None)[0]
    flat = z - A @ c
    t = otsu(np.clip(flat + 128, 0, 255).astype(np.uint8))[0] - 128
    w = flat <= t
    print("pass %d: fitted slope across the columns %.2f grey levels per pixel (true 1.26), accuracy %.1f%%" % (it + 1, c[1], accuracy((flat > t).reshape(n, n))))
```
```output
iterative threshold = 121.9, accuracy 99.8%
Otsu threshold      = 121,   accuracy 99.8%  (between-class variance 2359)
shaded image: global Otsu accuracy 83.2%
pass 1: fitted slope across the columns 1.30 grey levels per pixel (true 1.26), accuracy 99.0%
pass 2: fitted slope across the columns 1.24 grey levels per pixel (true 1.26), accuracy 99.8%
pass 3: fitted slope across the columns 1.24 grey levels per pixel (true 1.26), accuracy 99.8%
```
## 5.2 Region-based segmentation

Thresholding uses pixel values only. **Region-based** methods use also the **connectivity and similarity** of neighbours, so a region is guaranteed to be connected.

### 5.2.1 Region growing

Start from one or more **seed** points and grow each region by adding neighbouring pixels that satisfy a **similarity criterion** (the grey level differs from the region mean by less than a tolerance, or the local variance is small), stopping when no pixel qualifies. The choices to make are the seeds (chosen by the user, by the brightest pixels, or from a threshold), the criterion, the connectivity (4 or 8) and a stopping rule. It works well on noisy images (a threshold on the single pixel fails) and where edges are hard to detect, but depends on the seed and the order of visiting the pixels, and can leak through a weak boundary.

### 5.2.2 Region splitting and merging

The opposite approach starts with the **whole image** as one region. The **splitting** step divides every region that fails the predicate $Q$ (for example, its standard deviation is too high) into four quadrants, recursively, producing a **quadtree**. The **merging** step then joins adjacent regions $R_i$ and $R_j$ if $Q(R_i\cup R_j)$ is true. The result is a set of homogeneous regions of irregular shape built from square blocks. It needs no seed, but the blocky boundaries need a clean-up.

### 5.2.3 Other region methods

**Watershed segmentation** treats the grey-level image (usually the gradient magnitude) as a topographic surface: water poured into each local minimum floods basins which are separated by **watershed lines** where the floods meet; with **markers** to avoid over-segmentation it separates touching objects such as cells and coins. **K-means clustering** of pixel colours (Section 5.5) and **graph cuts** are also in common use, and **deep networks** (U-Net, Mask R-CNN) now give the best results for complex scenes when training data exist.

```python
import numpy as np
from collections import deque
rng = np.random.default_rng(41)
n = 64; yy, xx = np.mgrid[0:n, 0:n]
truth = ((yy - 30) ** 2 + (xx - 28) ** 2) < 18 ** 2
img = np.where(truth, 150.0, 90.0) + rng.normal(0, 10, (n, n))
img[(yy > 58) & (xx > 50)] = 150                                    # a distant bright patch, not connected to the object

def grow(img, seed, tol):
    seg = np.zeros(img.shape, bool); seg[seed] = True; total, cnt = float(img[seed]), 1
    dq = deque([seed])
    while dq:
        a, b = dq.popleft()
        for da, db in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            u, v = a + da, b + db
            if 0 <= u < n and 0 <= v < n and not seg[u, v] and abs(img[u, v] - total / cnt) < tol:
                seg[u, v] = True; total += img[u, v]; cnt += 1; dq.append((u, v))
    return seg
seg = grow(img, (30, 28), 30)
thr = img > 120
print("object pixels (truth): %d" % truth.sum())
print("global threshold at 120 : %d pixels, includes the unconnected patch: %s" % (thr.sum(), bool(thr[60, 55])))
print("region growing, tol 30  : %d pixels, includes the unconnected patch: %s" % (seg.sum(), bool(seg[60, 55])))
print("region growing accuracy on the object: %.1f%%" % (100 * np.mean(seg == truth)))

# Split and merge predicate: split a block while its standard deviation exceeds 20 (quadtree).
def split(a, r, c, s, out):
    blk = a[r:r + s, c:c + s]
    if s > 4 and blk.std() > 20:
        h = s // 2
        for dr in (0, h):
            for dc in (0, h): split(a, r + dr, c + dc, h, out)
    else: out.append((r, c, s, blk.mean()))
blocks = []; split(img, 0, 0, n, blocks)
print("quadtree: %d leaf blocks, sizes used: %s" % (len(blocks), sorted(set(b[2] for b in blocks), reverse=True)))
```
```output
object pixels (truth): 1005
global threshold at 120 : 1073 pixels, includes the unconnected patch: True
region growing, tol 30  : 1002 pixels, includes the unconnected patch: False
region growing accuracy on the object: 99.9%
quadtree: 70 leaf blocks, sizes used: [16, 8, 4]
```
## 5.3 Edges, lines and curves

An **edge** is a set of connected pixels on the boundary between two regions where the intensity changes rapidly. Edge detection is the commonest way to find boundaries; it is the discontinuity approach. Real edges are modelled as a **step** (an ideal jump), a **ramp** (a blurred step, the commonest), or a **roof** (a thin line). The first derivative of a ramp is a non-zero plateau along it, the second derivative is a **positive then negative** pair with a **zero crossing** at the centre of the edge. Hence: the magnitude of the first derivative detects the presence of an edge, and the sign change of the second derivative locates it. Both derivatives are strongly affected by noise, so the image should be smoothed first.

### 5.3.1 Gradient operators

The **gradient** of $f$ is the vector $\nabla f=[G_x,\,G_y]^{T}=[\partial f/\partial x,\ \partial f/\partial y]^{T}$. It points in the direction of the greatest rate of change; its **magnitude** and **direction** are

$$M(x,y)=\sqrt{G_x^{2}+G_y^{2}}\approx|G_x|+|G_y|,\qquad\alpha(x,y)=\tan^{-1}(G_y/G_x),$$

and the edge is at right angles to $\alpha$. The partial derivatives are approximated by small masks (the 3 x 3 masks show $G_x$; $G_y$ is the transpose, rotated):

| Operator | $G_x$ mask | Properties |
|---|---|---|
| **Roberts** (2 x 2, cross-gradient) | $\begin{bmatrix}-1&0\\0&1\end{bmatrix}$ | Simplest, fast; very sensitive to noise; edges are on the diagonals |
| **Prewitt** | $\begin{bmatrix}-1&0&1\\-1&0&1\\-1&0&1\end{bmatrix}$ | Averages three rows, so less noise sensitive |
| **Sobel** | $\begin{bmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{bmatrix}$ | Extra weight on the centre row: smoothing and differentiation; the most used |

The result is then **thresholded** to keep strong edges. Smoothing first reduces the noise but widens the edges; a higher threshold keeps fewer, cleaner edges and loses weak ones. **Compass operators** (Kirsch, Robinson) test eight directions with rotated masks and keep the maximum.

### 5.3.2 The Laplacian of Gaussian and zero crossings

The **Laplacian** $\nabla^{2}f$ (Section 2.3.3) is isotropic and responds to edges in all directions with a zero crossing at the edge, but it is very noisy and gives no direction. Marr and Hildreth combined it with Gaussian smoothing, giving the **Laplacian of Gaussian (LoG)**:

$$\nabla^{2}G(x,y)=\frac{x^{2}+y^{2}-2\sigma^{2}}{\sigma^{4}}\,e^{-\frac{x^{2}+y^{2}}{2\sigma^{2}}}.$$

The image is convolved with the LoG (the "Mexican hat" shape), and the edges are the **zero crossings** of the result. $\sigma$ sets the scale: large $\sigma$ finds only coarse edges. The zero-crossing contours are always closed, which is a convenience and also a nuisance. The **Difference of Gaussians** (Section 2.3.4) approximates the LoG.

### 5.3.3 The Canny edge detector

Canny (1986) designed an edge detector for **good detection** (few misses and false edges), **good localization** (the marked edge is near the true one) and **a single response per edge**. The steps:

1. **Smooth** the image with a Gaussian filter to suppress noise.
2. Compute the **gradient magnitude and direction** (Sobel).
3. **Non-maximum suppression**: keep a pixel only if its magnitude is the largest along the gradient direction, thinning the broad ridges to one pixel.
4. **Double (hysteresis) thresholding**: pixels above a high threshold $T_H$ are *strong* edges; those between $T_L$ and $T_H$ are *weak* and kept only if connected to a strong edge; the others are discarded. A typical ratio is $T_H:T_L=2:1$ or $3:1$.

Canny is the standard against which other detectors are compared. Edge detection gives **fragments**: gaps and spurious bits remain, so an **edge-linking** step connects them: *local processing* joins neighbouring edge pixels if their gradient magnitudes and directions are similar, and *global processing* uses the Hough transform.

### 5.3.4 Line and curve detection: the Hough transform

To find **straight lines** among edge pixels, the **Hough transform** lets every edge pixel *vote* for all lines that could pass through it. A line is written in the **normal form** $\rho=x\cos\theta+y\sin\theta$ (Figure 5.2), where $\rho$ is the perpendicular distance from the origin and $\theta$ its angle (the slope-intercept form $y=mx+c$ cannot describe vertical lines). Each edge pixel $(x_i,y_i)$ corresponds to a **sinusoid** in the $(\rho,\theta)$ plane; points on one line give sinusoids that **all cross at the same $(\rho,\theta)$**. The steps:

1. Quantize $\rho$ and $\theta$ into an **accumulator** array $A[\rho,\theta]$, initially 0.
2. For each edge pixel and each $\theta$, compute $\rho$ and increment the cell.
3. Local **peaks** in $A$ above a threshold are lines; the count in a cell is the number of pixels on the line. The lines can be broken into segments afterwards.

The accumulator tolerates gaps and noise, since a line only has to collect enough votes. The same idea finds **circles** with a three-parameter accumulator $(a,b,r)$ for $(x-a)^{2}+(y-b)^{2}=r^{2}$ (two parameters if the gradient direction is used), **ellipses**, and arbitrary shapes (**generalized Hough transform**). The cost grows with the number of parameters, which is why only simple curves are practical. Uses: lane detection, finding the horizon, the edge of a page in a scanner, coin detection.

```svgfig label="5.2" caption="The Hough transform. A line is described by its distance rho from the origin and the angle theta of its normal (left). Each point on the line becomes a sinusoid in the (theta, rho) plane (right); all the sinusoids of points on the same line cross at one point, which is the (rho, theta) of the line."
import math
f = Fig(700, 280)
f.line(50, 240, 300, 240, color=SLATE, sw=1.2)
f.line(50, 240, 50, 30, color=SLATE, sw=1.2)
f.text(305, 252, "x", size=11, color=SLATE); f.text(40, 28, "y", size=11, color=SLATE)
th = math.radians(55); rho = 150
c, sn = math.cos(th), math.sin(th)
def S(t):                                   # screen point of the line at parameter t (data y points up)
    return (50 + rho * c - t * sn, 240 - (rho * sn + t * c))
(x1, y1), (x2, y2) = S(-120), S(95)
f.line(x1, y1, x2, y2, color=RED, sw=2.4)
f.line(50, 240, 50 + rho * c, 240 - rho * sn, color=NAVY, sw=1.8, dash=True)
for t in (-90, -40, 20, 60):
    qx, qy = S(t)
    f.circle(qx, qy, 4.5, fill=AMBER, stroke=AMBER, label="")
f.text(50 + rho * c / 2 + 16, 240 - rho * sn / 2 + 10, "rho", size=11, color=NAVY, bold=True)
f.text(112, 226, "theta", size=10.5, color=NAVY, bold=True)
f.text(300, 36, "line: rho = x cos(theta) + y sin(theta)", size=10, color=SLATE, anchor="end")
ax = Axes(f, 390, 30, 280, 210, (0, 180), (-1.6, 1.6))
ax.grid(dx=45, dy=1)
ax.axes(xl="", yl="rho (scaled)")
f.text(530, 268, "theta (degrees)", size=10, color=SLATE)
pts = [(0.950, 0.311), (0.623, 0.540), (0.295, 0.770), (-0.032, 0.999)]
def L(x, y): return lambda t: x * math.cos(math.radians(t)) + y * math.sin(math.radians(t))
cols = (AMBER, TEAL, NAVY, SLATE)
for (x, y), c in zip(pts, cols):
    ax.curve(L(x, y), color=c, sw=1.8, n=200)
ax.pt(55, 0.8, "(55, rho)", dx=10, dy=-10, anchor="start")
```

```python
import numpy as np
rng = np.random.default_rng(51)
n = 80
img = np.zeros((n, n))
img[:, :40] = 80; img[:, 40:] = 180                       # a vertical step edge at column 40
yy, xx = np.mgrid[0:n, 0:n]
img[yy > 55] = np.where(xx[yy > 55] + (yy[yy > 55] - 55) > 60, 220, img[yy > 55])   # a diagonal edge in the lower part
img += rng.normal(0, 6, img.shape)

def conv(a, k):
    r = k.shape[0] // 2; p = np.pad(a, r, mode="edge"); out = np.zeros_like(a)
    for i in range(k.shape[0]):
        for j in range(k.shape[1]): out += k[i, j] * p[i:i + a.shape[0], j:j + a.shape[1]]
    return out
Sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float); Sy = Sx.T
Gx, Gy = conv(img, Sx), conv(img, Sy); M = np.hypot(Gx, Gy)
print("Sobel: gradient magnitude on the vertical edge (column 40): %.0f, in a flat area: %.1f" % (M[20, 40], M[20, 10]))
print("gradient direction at the vertical edge: %.0f degrees (the edge is at right angles to it)" % np.degrees(np.arctan2(Gy[20, 40], Gx[20, 40])))
edges = M > 0.5 * M.max()
print("edge pixels above 50%% of the maximum: %d; columns containing edges in row 20: %s" % (edges.sum(), np.nonzero(edges[20])[0].tolist()))
print("Roberts-like noise sensitivity: noise-only rows give mean |Sobel| = %.1f" % M[5:15, 2:30].mean())

# Hough transform for lines on the edge map of the vertical edge.
ys, xs = np.nonzero(edges[:50])
thetas = np.deg2rad(np.arange(0, 180)); diag = int(np.hypot(n, n))
acc = np.zeros((2 * diag + 1, len(thetas)), int)
for x, y in zip(xs, ys):
    rhos = np.round(x * np.cos(thetas) + y * np.sin(thetas)).astype(int) + diag
    acc[rhos, np.arange(len(thetas))] += 1
r, t = np.unravel_index(acc.argmax(), acc.shape)
print("Hough peak: rho = %d, theta = %d degrees with %d votes out of %d edge pixels" % (r - diag, t, acc.max(), len(xs)))
print("(rho, theta) and (-rho, theta + 180) describe the same line, so this is the vertical line x = 39; the other half of the votes went to the edge column 40")
```
```output
Sobel: gradient magnitude on the vertical edge (column 40): 403, in a flat area: 15.3
gradient direction at the vertical edge: -3 degrees (the edge is at right angles to it)
edge pixels above 50% of the maximum: 160; columns containing edges in row 20: [39, 40]
Roberts-like noise sensitivity: noise-only rows give mean |Sobel| = 27.4
Hough peak: rho = -39, theta = 179 degrees with 50 votes out of 100 edge pixels
(rho, theta) and (-rho, theta + 180) describe the same line, so this is the vertical line x = 39; the other half of the votes went to the edge column 40
```
## 5.4 Image features and feature extraction

After segmentation each region is only a set of pixels. **Feature extraction** reduces it to a short vector of numbers (the **feature vector**) that describes the properties relevant to the task and is the same for objects of the same class. Good features are **discriminating** (different for different classes), **reliable** (similar within a class), **invariant** (to translation, rotation and scale where the task needs it) and **few**.

### 5.4.1 Types of features

| Type | Examples | Notes |
|---|---|---|
| **Boundary (external) features** | Perimeter, chain code, signature, Fourier descriptors, curvature | Describe shape when the outline matters (a leaf, a letter) |
| **Region (internal) features** | Area, centroid, bounding box, compactness, eccentricity, moments, holes | Describe the whole object |
| **Intensity and colour features** | Mean, variance, colour histogram, dominant hue | Material and lighting dependent |
| **Texture features** | Statistics of the histogram, GLCM measures, Gabor and wavelet energies | Describe repeated patterns (fabric, grass, skin) |
| **Keypoint features** | Corners (Harris), SIFT, ORB descriptors | Matching, tracking, panoramas |

**Chain code.** The boundary is stored as a sequence of directions (0 to 3 for a 4-connected code, 0 to 7 for 8-connected) of steps from one boundary pixel to the next. It is compact and can be made independent of the starting point (by choosing the **minimum-magnitude** cyclic shift) and of rotation (by using the **first difference**, the number of direction changes counted anticlockwise between successive codes). **Shape numbers** are the minimum-magnitude first difference.

**Simple region descriptors.** The **area** $A$ is the pixel count; the **perimeter** $P$ the boundary length; **compactness** (or circularity) $P^{2}/A$ (minimum $4\pi\approx12.57$ for a circle, larger for a square: 16, and larger still for elongated or ragged shapes), the **aspect ratio** of the bounding box, the **centroid** $(\bar x,\bar y)=(m_{10}/m_{00},m_{01}/m_{00})$ from the **moments** $m_{pq}=\sum x^{p}y^{q}f(x,y)$, and the **central moments** $\mu_{pq}=\sum(x-\bar x)^{p}(y-\bar y)^{q}f(x,y)$, which are translation invariant. The seven **Hu invariant moments** are combinations of normalized central moments that are also invariant to scale and rotation.

### 5.4.2 Texture

**Texture** is the spatial arrangement of intensities: smooth, rough, regular, random. Three approaches: **statistical** (measures from the histogram or from co-occurrence), **structural** (a pattern of primitives with placement rules) and **spectral** (the Fourier spectrum or the energy of Gabor and wavelet bands). The histogram statistics are the mean, the **variance** $\sigma^{2}=\sum(z-m)^{2}p(z)$ (roughness), **skewness**, **uniformity** $\sum p^{2}$ and **entropy** $-\sum p\log_2p$; but they carry no information about position. The **grey-level co-occurrence matrix (GLCM)** $C_{d,\theta}(i,j)$ counts how often a pixel with level $i$ has a neighbour with level $j$ at displacement $d$ in direction $\theta$; normalized to probabilities $P(i,j)$, it yields the **Haralick features**:

$$\text{contrast}=\sum_{i,j}(i-j)^{2}P(i,j),\quad\text{energy}=\sum_{i,j}P(i,j)^{2},\quad\text{homogeneity}=\sum_{i,j}\frac{P(i,j)}{1+|i-j|},\quad\text{entropy}=-\sum P\log_2P .$$

Smooth texture has low contrast and high homogeneity; coarse random texture has high contrast and high entropy.

### 5.4.3 Feature reduction

A long feature vector costs memory and time, and with too many features and few training examples a classifier **overfits** (the "curse of dimensionality"). **Feature reduction** takes two forms: *feature selection* (choose a subset by testing which features separate the classes, with a filter or by forward and backward selection) and *feature extraction* (build a few new features from combinations of the old). The classic method is **principal component analysis (PCA)** (the Karhunen-Loeve transform):

1. Centre the data: subtract the mean vector $\mathbf m$ from each feature vector $\mathbf x$.
2. Compute the **covariance matrix** $C=\tfrac1{n}\sum(\mathbf x-\mathbf m)(\mathbf x-\mathbf m)^{T}$.
3. Find the **eigenvalues** $\lambda_1\ge\lambda_2\ge\dots$ and eigenvectors $\mathbf e_i$ of $C$.
4. Keep the $k$ eigenvectors with the largest eigenvalues (the **principal components**), enough to explain, say, 95% of the variance $\sum_{i\le k}\lambda_i/\sum\lambda_i$.
5. Project: $\mathbf y=A(\mathbf x-\mathbf m)$, where the rows of $A$ are the chosen eigenvectors.

The new features are uncorrelated, ordered by variance, and $\mathbf x$ can be approximately recovered with $\hat{\mathbf x}=A^{T}\mathbf y+\mathbf m$ with a mean square error equal to the sum of the discarded eigenvalues. PCA is also used for face recognition ("eigenfaces") and to reduce the bands of a multispectral image (Section 5.6.6). **Linear discriminant analysis (LDA)** is a supervised alternative that maximizes class separation.

```python
import numpy as np
n = 64; yy, xx = np.mgrid[0:n, 0:n]
shapes = {"disc": (yy - 32) ** 2 + (xx - 32) ** 2 < 20 ** 2,
          "square": (abs(yy - 32) < 18) & (abs(xx - 32) < 18),
          "bar": (abs(yy - 32) < 6) & (abs(xx - 32) < 28)}

def boundary(m):
    p = np.pad(m, 1); inner = p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return m & ~inner
def features(m):
    A = m.sum(); ys, xs = np.nonzero(m); cy, cx = ys.mean(), xs.mean()
    mu20 = ((xs - cx) ** 2).mean(); mu02 = ((ys - cy) ** 2).mean(); mu11 = ((xs - cx) * (ys - cy)).mean()
    common = np.sqrt(4 * mu11 ** 2 + (mu20 - mu02) ** 2); l1 = (mu20 + mu02 + common) / 2; l2 = (mu20 + mu02 - common) / 2
    P = boundary(m).sum()          # boundary pixel count approximates the perimeter
    return A, P, P ** 2 / A, (cy, cx), np.sqrt(1 - l2 / l1)
for k, m in shapes.items():
    A, P, comp, (cy, cx), ecc = features(m)
    print("%-6s area %4d  boundary pixels %3d  P^2/A %5.1f  centroid (%.1f, %.1f)  eccentricity %.2f" % (k, A, P, comp, cy, cx, ecc))
print("theoretical P^2/A: circle %.2f, square 16 (counting boundary pixels underestimates the length of a curved edge, so the digital values are lower)" % (4 * np.pi))

# GLCM (distance 1, horizontal) on a smooth and a random texture with 8 grey levels.
def glcm_feats(a, L=8):
    q = (a * L // 256).astype(int); C = np.zeros((L, L))
    for i, j in zip(q[:, :-1].ravel(), q[:, 1:].ravel()): C[i, j] += 1
    P = C / C.sum(); i, j = np.indices(P.shape); nz = P[P > 0]
    return (P * (i - j) ** 2).sum(), (P ** 2).sum(), (P / (1 + abs(i - j))).sum(), -(nz * np.log2(nz)).sum()
rng = np.random.default_rng(61)
smooth = np.clip(128 + 60 * np.sin(xx / 9.0) + rng.normal(0, 4, (n, n)), 0, 255)
rough = rng.integers(0, 256, (n, n)).astype(float)
for name, t in (("smooth", smooth), ("random", rough)):
    c, e, h, en = glcm_feats(t)
    print("%-6s texture: contrast %.2f, energy %.3f, homogeneity %.2f, entropy %.2f" % (name, c, e, h, en))

# PCA on 3 correlated features: most of the variance sits in one component.
X = rng.normal(0, 1, (200, 1)) @ np.array([[3.0, 2.0, 1.0]]) + rng.normal(0, 0.4, (200, 3))
Xc = X - X.mean(0); C = Xc.T @ Xc / len(X)
w, V = np.linalg.eigh(C); order = np.argsort(w)[::-1]; w, V = w[order], V[:, order]
print("eigenvalues:", np.round(w, 2).tolist(), "explained variance: %s" % np.round(100 * w / w.sum(), 1).tolist())
Y = Xc @ V[:, :1]; back = Y @ V[:, :1].T
print("keep 1 of 3 components: reconstruction MSE per feature %.3f, sum of discarded eigenvalues / 3 = %.3f" % (np.mean((Xc - back) ** 2), w[1:].sum() / 3))
```
```output
disc   area 1245  boundary pixels 112  P^2/A  10.1  centroid (32.0, 32.0)  eccentricity 0.00
square area 1225  boundary pixels 136  P^2/A  15.1  centroid (32.0, 32.0)  eccentricity 0.00
bar    area  605  boundary pixels 128  P^2/A  27.1  centroid (32.0, 32.0)  eccentricity 0.98
theoretical P^2/A: circle 12.57, square 16 (counting boundary pixels underestimates the length of a curved edge, so the digital values are lower)
smooth texture: contrast 0.17, energy 0.187, homogeneity 0.91, entropy 2.82
random texture: contrast 9.88, energy 0.016, homogeneity 0.40, entropy 5.99
eigenvalues: [16.17, 0.16, 0.14] explained variance: [98.1, 1.0, 0.9]
keep 1 of 3 components: reconstruction MSE per feature 0.102, sum of discarded eigenvalues / 3 = 0.102
```
## 5.5 Image classification and clustering

**Classification** assigns an object, described by its feature vector $\mathbf x=(x_1,\dots,x_d)^{T}$, to one of $K$ known classes. **Supervised** methods learn from labelled examples (the **training set**) and are judged on a separate **test set**; **unsupervised** methods (clustering) find the groups by themselves, without labels.

### 5.5.1 Supervised classification

- **Minimum-distance classifier.** Each class $\omega_j$ is represented by its mean vector $\mathbf m_j$; an unknown $\mathbf x$ goes to the class with the **smallest Euclidean distance** $D_j=\lVert\mathbf x-\mathbf m_j\rVert$. Equivalently it maximizes the decision function $d_j(\mathbf x)=\mathbf x^{T}\mathbf m_j-\tfrac12\mathbf m_j^{T}\mathbf m_j$. It is simple, fast and works when the classes are compact and well separated, and it gives linear decision boundaries (the perpendicular bisectors between class means).
- **Maximum-likelihood (Bayes) classifier.** With Gaussian classes of mean $\mathbf m_j$, covariance $C_j$ and prior $P(\omega_j)$, choose the class with the highest posterior probability; it takes the scatter of each class into account (the **Mahalanobis** distance) and is the standard in remote sensing. It minimizes the average error when the model is right, but needs enough training pixels to estimate $C_j$.
- **k-nearest neighbours (k-NN).** Find the $k$ training samples closest to $\mathbf x$ and assign the **majority class**. No training step and flexible boundaries, but slow on large sets, and sensitive to the scale of the features (**normalize** each feature) and to the choice of $k$ (small $k$ is noisy, large $k$ blurs the boundary).
- **Decision trees, support vector machines (SVM), neural networks.** Modern systems, particularly deep **convolutional neural networks (CNNs)**, learn the features themselves from the pixels and now give the best accuracy on large image sets (see the Machine Learning book).

**Evaluating a classifier.** The **confusion matrix** counts samples of each true class against the predicted class. The overall **accuracy** is the trace divided by the total; for each class, **precision** $=TP/(TP+FP)$ and **recall** $=TP/(TP+FN)$. Always test on data that was not used for training, otherwise the accuracy is too optimistic.

### 5.5.2 Clustering

**Clustering** groups unlabelled feature vectors so that vectors in a cluster are similar and vectors in different clusters are not. In images it is used to segment by colour and to build classes without ground truth (unsupervised classification of satellite scenes).

**k-means.** (1) Choose $k$ and place $k$ initial centres (random samples). (2) **Assign** each vector to the nearest centre. (3) **Update** each centre to the mean of its vectors. (4) Repeat 2 and 3 until the assignments stop changing. It minimizes the within-cluster sum of squares $J=\sum_j\sum_{\mathbf x\in S_j}\lVert\mathbf x-\mathbf c_j\rVert^{2}$, converges quickly, but only to a **local** minimum (run it several times), needs $k$ in advance, and prefers round clusters of similar size. **ISODATA** adds splitting and merging of clusters; **fuzzy c-means** gives each point a degree of membership of every cluster; **hierarchical clustering** builds a tree (dendrogram) of merges; **mean-shift** and **DBSCAN** find the number of clusters themselves.

```python
import numpy as np
rng = np.random.default_rng(71)
# Three classes of objects in a 2-D feature space (area-like and texture-like features).
means = np.array([[2.0, 2.0], [6.0, 3.0], [4.0, 7.0]])
Xtr = np.vstack([rng.normal(m, 0.9, (40, 2)) for m in means]); ytr = np.repeat([0, 1, 2], 40)
Xte = np.vstack([rng.normal(m, 0.9, (30, 2)) for m in means]); yte = np.repeat([0, 1, 2], 30)

def confusion(y, p, K=3):
    M = np.zeros((K, K), int)
    for a, b in zip(y, p): M[a, b] += 1
    return M
# Minimum-distance classifier
M = np.array([Xtr[ytr == k].mean(0) for k in range(3)])
pred_md = np.argmin(((Xte[:, None, :] - M[None]) ** 2).sum(2), axis=1)
print("class means estimated from training data:\n", np.round(M, 2))
cm = confusion(yte, pred_md)
print("minimum-distance confusion matrix (rows = true):\n", cm)
print("accuracy %.1f%%; recall per class %s; precision per class %s" %
      (100 * np.trace(cm) / cm.sum(), np.round(np.diag(cm) / cm.sum(1), 2).tolist(), np.round(np.diag(cm) / cm.sum(0), 2).tolist()))

# k-nearest neighbours
def knn(x, k):
    d = ((Xtr - x) ** 2).sum(1); idx = np.argsort(d)[:k]
    return np.bincount(ytr[idx], minlength=3).argmax()
for k in (1, 5, 15):
    p = np.array([knn(x, k) for x in Xte])
    print("k-NN with k = %2d: accuracy %.1f%%" % (k, 100 * np.mean(p == yte)))
print("an example point (3.4, 3.0): minimum-distance class %d, 5-NN class %d" % (np.argmin(((np.array([3.4, 3.0]) - M) ** 2).sum(1)), knn(np.array([3.4, 3.0]), 5)))

# k-means on the unlabelled training data
def kmeans(X, k, seed):
    r = np.random.default_rng(seed); c = X[r.choice(len(X), k, replace=False)]
    for it in range(100):
        lab = np.argmin(((X[:, None, :] - c[None]) ** 2).sum(2), axis=1)
        new = np.array([X[lab == j].mean(0) if (lab == j).any() else c[j] for j in range(k)])
        if np.allclose(new, c): break
        c = new
    return c, lab, ((X - c[lab]) ** 2).sum(), it + 1
best = min((kmeans(Xtr, 3, s) for s in range(5)), key=lambda t: t[2])
print("k-means (k = 3, best of 5 starts): %d iterations, J = %.1f" % (best[3], best[2]))
print("cluster centres (sorted):\n", np.round(best[0][np.argsort(best[0][:, 0])], 2))
for k in (1, 2, 3, 4, 6):
    print("k = %d: J = %7.1f" % (k, min(kmeans(Xtr, k, s)[2] for s in range(5))))

# Colour segmentation: k-means with k = 2 on the colours of a synthetic 'sky and field' image.
img = np.zeros((40, 40, 3)); img[:20] = (90, 140, 230); img[20:] = (60, 150, 70); img += rng.normal(0, 12, img.shape)
c, lab, J, it = kmeans(img.reshape(-1, 3), 2, 0)
print("colour k-means centres:", np.round(c[np.argsort(c[:, 0])]).astype(int).tolist(), "-> top half and bottom half separated:", bool(len(set(lab[:800])) == 1 and len(set(lab[800:])) == 1))
```
```output
class means estimated from training data:
 [[1.79 2.05]
 [6.04 2.83]
 [4.   6.94]]
minimum-distance confusion matrix (rows = true):
 [[29  1  0]
 [ 0 30  0]
 [ 0  0 30]]
accuracy 98.9%; recall per class [0.97, 1.0, 1.0]; precision per class [1.0, 0.97, 1.0]
k-NN with k =  1: accuracy 98.9%
k-NN with k =  5: accuracy 98.9%
k-NN with k = 15: accuracy 98.9%
an example point (3.4, 3.0): minimum-distance class 0, 5-NN class 0
k-means (k = 3, best of 5 starts): 4 iterations, J = 138.0
cluster centres (sorted):
 [[1.79 2.05]
 [4.   6.94]
 [6.04 2.83]]
k = 1: J =  1054.3
k = 2: J =   512.3
k = 3: J =   138.0
k = 4: J =   117.2
k = 6: J =    87.0
colour k-means centres: [[60, 150, 70], [90, 140, 230]] -> top half and bottom half separated: True
```
## 5.6 Case studies

### 5.6.1 Image security: encryption

Medical, military, banking and personal images must be protected. Ordinary text ciphers (AES) can be applied to the bytes of an image, but encrypting a file with a block cipher in ECB mode leaves the **outline of the picture visible**, because identical blocks give identical ciphertext. The classical image-specific scheme has two parts: **permutation (confusion)**, shuffling the pixel positions with a key-driven pseudo-random sequence, and **diffusion**, changing the pixel values, for example by XORing with a key stream or a chaotic sequence (logistic map). A good image cipher has a very large key space, a flat histogram of the cipher image (entropy near 8 bits), near-zero correlation between neighbouring pixels, and sensitivity to a one-bit change of the key. The standard tests are exactly these three: the histogram, the correlation coefficient of adjacent pixels and the entropy.

### 5.6.2 Steganography

**Steganography** hides *the existence* of a message in an innocent-looking **cover**; **cryptography** hides its *meaning*. The simplest method is **least-significant-bit (LSB) substitution**: replace the lowest bit of each pixel (or of each colour channel) by one bit of the message. Changing the LSB changes a pixel value by at most 1 of 255, which the eye cannot see, and a $512\times512$ greyscale cover holds 32 KB. The weaknesses: the LSB plane is **noise-like** after embedding and statistical tests (chi-square, RS analysis) detect it; it does not survive JPEG compression, resizing or filtering (so it needs a lossless format such as PNG); and an adversary who suspects it can overwrite all the LSBs. Better schemes embed in the **DCT or wavelet coefficients**, adaptively in busy areas, or with matrix coding (fewer changes per message bit). The usual quality measures are PSNR and the **capacity** in bits per pixel.

### 5.6.3 Digital watermarking

A **watermark** is a signal embedded in an image to prove **ownership**, **authenticity** or track copies, while *still allowing the image to be used*. It differs from steganography in aim (robustness against removal, not secrecy) and in what is hidden (a short code or logo). Watermarks are classified as **visible** (a logo on a stock photo) or **invisible**; **robust** (survive compression, cropping, noise) or **fragile** (broken by any change, to detect tampering); and **blind** (detected without the original) or non-blind. The requirements are **imperceptibility**, **robustness**, **capacity** and **security**; they conflict. A standard robust scheme is **spread-spectrum embedding in the transform domain**: add a pseudo-random $\pm1$ pattern $w$ of strength $\alpha$ to the mid-frequency DCT coefficients, $c'=c+\alpha w$, and detect by **correlating** the received coefficients with the pattern $w$ generated from the secret key; a high correlation means that the mark is present.

### 5.6.4 Visual effects

Visual effects (VFX) in film, advertising and phone apps are applications of the techniques already met: **colour grading** (curves on the channels, Section 2.1), **blur and bokeh** (low-pass filters; depth-dependent blur for portrait mode), **sharpening and HDR tone mapping** (unsharp masking, homomorphic filtering, local contrast), **sepia and stylization** (matrix transform of colour, edge-preserving smoothing plus edge overlay for "cartoon"), **chroma keying** (green screen: segment by hue and saturation in HSV, soften the matte edge, composite $C=\alpha F+(1-\alpha)B$), **morphing** and warping (geometric transforms with interpolation between corresponding points), **image inpainting** and object removal, **stitching** of panoramas (keypoints, homography, blending), and AI style transfer and generative models.

### 5.6.5 Medical imaging

Medical images come from X-ray radiography, **computed tomography (CT)**, **magnetic resonance imaging (MRI)**, ultrasound and nuclear medicine (PET, SPECT), and are stored and exchanged in the **DICOM** format. Typical processing: **windowing** (a CT value in **Hounsfield units** from about $-1000$ (air) through 0 (water) to $+1000$ or more (bone) is mapped to the display by a *window level* and *width*, a piecewise-linear contrast stretch: a lung window and a bone window show different organs from the same data); **noise reduction** (non-local means, wavelet shrinkage) for low-dose scans; **enhancement** with CLAHE; **segmentation** of organs and tumours (thresholding, region growing, level sets, and now U-Net deep networks); **registration** (aligning CT with MRI or with an earlier scan); **3-D reconstruction and volume rendering**; and **computer-aided diagnosis** (detecting lung nodules, diabetic retinopathy, fractures). Lossy compression is allowed only to a limit set by regulation, as the loss of detail may hide a lesion; privacy of the patient data in the DICOM header must be protected.

### 5.6.6 Remote sensing

Satellites (Landsat, Sentinel-2, MODIS), aircraft and drones record **multispectral** images with a band for each wavelength range, such as blue, green, red, near-infrared (NIR), short-wave infrared and thermal. Healthy vegetation reflects strongly in NIR and absorbs red, so the **Normalized Difference Vegetation Index** is $\mathrm{NDVI}=\dfrac{NIR-Red}{NIR+Red}\in[-1,1]$: values near 0.6 to 0.9 for dense healthy vegetation, 0.2 to 0.5 for sparse crops or grass, close to 0 for bare soil, and negative for water and snow. Other indices: NDWI for water, NDBI for built-up area. The usual steps are **radiometric and atmospheric correction**, **geometric correction** (georeferencing, Section 3 of the GIS book), **enhancement** (contrast stretching, false-colour composites, band ratios, PCA to compress the bands), **classification** (supervised: maximum likelihood, SVM, random forest; unsupervised: ISODATA, k-means), **change detection** (image differencing between two dates: deforestation, flood extent, urban growth) and **accuracy assessment** (confusion matrix, kappa coefficient). In Nepal these are used for land-cover maps, glacier-lake monitoring in the Himalaya, flood mapping on the Terai rivers and crop monitoring.

```python
import numpy as np
rng = np.random.default_rng(81)
# --- 1. LSB steganography: hide a text message in a cover, then recover it.
cover = rng.integers(0, 256, (32, 32)).astype(np.uint8)
msg = "NEBians"; bits = np.unpackbits(np.frombuffer(msg.encode(), dtype=np.uint8))
flat = cover.ravel().copy(); flat[:len(bits)] = (flat[:len(bits)] & 0xFE) | bits
stego = flat.reshape(cover.shape)
back = np.packbits(stego.ravel()[:len(bits)] & 1).tobytes().decode()
mse = np.mean((stego.astype(float) - cover) ** 2)
print("hidden %d bits; recovered message: %r; max pixel change %d; PSNR %.1f dB; capacity %d bytes" %
      (len(bits), back, np.abs(stego.astype(int) - cover).max(), 10 * np.log10(255 ** 2 / mse), cover.size // 8))

# --- 2. Image encryption: permutation + XOR keystream, check histogram entropy and neighbour correlation.
n = 64; yy, xx = np.mgrid[0:n, 0:n]
plain = np.clip(60 + 2 * xx + 40 * (((yy - 32) ** 2 + (xx - 32) ** 2) < 400), 0, 255).astype(np.uint8)
key = np.random.default_rng(1234)
perm = key.permutation(n * n); stream = key.integers(0, 256, n * n, dtype=np.uint8)
cipher = (plain.ravel()[perm] ^ stream).reshape(n, n)
dec = np.empty(n * n, np.uint8); dec[perm] = cipher.ravel() ^ stream
def H(a): p = np.bincount(a.ravel(), minlength=256) / a.size; p = p[p > 0]; return -(p * np.log2(p)).sum()
def corr(a): return np.corrcoef(a[:, :-1].ravel().astype(float), a[:, 1:].ravel().astype(float))[0, 1]
print("plain : entropy %.2f bits, adjacent-pixel correlation %.3f" % (H(plain), corr(plain)))
print("cipher: entropy %.2f bits, adjacent-pixel correlation %.3f" % (H(cipher), corr(cipher)))
print("decryption with the same key is exact:", np.array_equal(dec.reshape(n, n), plain))

# --- 3. Spread-spectrum watermark in DCT mid-frequency coefficients, detected by correlation.
def dctm(m=8):
    C = np.zeros((m, m))
    for k in range(m):
        for i in range(m): C[k, i] = np.sqrt((1 if k == 0 else 2) / m) * np.cos((2 * i + 1) * k * np.pi / (2 * m))
    return C
C8 = dctm(); N = 64
host = np.clip(100 + 80 * np.sin(xx / 7.0) * np.cos(yy / 9.0) + rng.normal(0, 4, (N, N)), 0, 255)
wm = np.random.default_rng(99).choice([-1.0, 1.0], size=(N // 8, N // 8, 4))      # a key-driven +/-1 pattern, 4 coefficients per block
pos = [(2, 3), (3, 2), (3, 3), (2, 4)]
marked = host.copy(); alpha = 6.0
for bi in range(N // 8):
    for bj in range(N // 8):
        blk = host[bi * 8:bi * 8 + 8, bj * 8:bj * 8 + 8]; D = C8 @ blk @ C8.T
        for t, (u, v) in enumerate(pos): D[u, v] += alpha * wm[bi, bj, t]
        marked[bi * 8:bi * 8 + 8, bj * 8:bj * 8 + 8] = C8.T @ D @ C8
def detect(img, w):
    s = []
    for bi in range(N // 8):
        for bj in range(N // 8):
            D = C8 @ img[bi * 8:bi * 8 + 8, bj * 8:bj * 8 + 8] @ C8.T
            s += [D[u, v] * w[bi, bj, t] for t, (u, v) in enumerate(pos)]
    return np.mean(s)
wrong = np.random.default_rng(5).choice([-1.0, 1.0], size=wm.shape)
print("PSNR of the marked image: %.1f dB" % (10 * np.log10(255 ** 2 / np.mean((marked - host) ** 2))))
print("detector response: marked image with the right key %.2f (alpha %.0f), unmarked image %.2f, wrong key %.2f" %
      (detect(marked, wm), alpha, detect(host, wm), detect(marked, wrong)))
noisy = marked + rng.normal(0, 8, marked.shape)
print("after adding noise (sigma 8) the right-key response is still %.2f" % detect(noisy, wm))

# --- 4. Medical windowing and 5. NDVI
hu = np.array([-1000, -500, 0, 40, 80, 400, 1000])
def window(v, level, width): return np.clip((v - (level - width / 2)) / width, 0, 1) * 255
print("HU values:", hu.tolist())
print("brain window (level 40, width 80)  :", window(hu, 40, 80).round().astype(int).tolist())
print("bone window (level 400, width 1800):", window(hu, 400, 1800).round().astype(int).tolist())
nir = np.array([0.50, 0.45, 0.30, 0.03, 0.05]); red = np.array([0.06, 0.10, 0.25, 0.07, 0.04])
for nme, a, b in zip(("dense forest", "healthy crop", "dry grass", "water", "shadow"), nir, red):
    print("%-16s NIR %.2f RED %.2f  NDVI %+.2f" % (nme, a, b, (a - b) / (a + b)))
```
```output
hidden 56 bits; recovered message: 'NEBians'; max pixel change 1; PSNR 63.3 dB; capacity 128 bytes
plain : entropy 6.00 bits, adjacent-pixel correlation 0.991
cipher: entropy 7.95 bits, adjacent-pixel correlation -0.016
decryption with the same key is exact: True
PSNR of the marked image: 44.6 dB
detector response: marked image with the right key 6.27 (alpha 6), unmarked image 0.27, wrong key -0.20
after adding noise (sigma 8) the right-key response is still 6.49
HU values: [-1000, -500, 0, 40, 80, 400, 1000]
brain window (level 40, width 80)  : [0, 0, 0, 128, 255, 255, 255]
bone window (level 400, width 1800): [0, 0, 71, 76, 82, 128, 212]
dense forest     NIR 0.50 RED 0.06  NDVI +0.79
healthy crop     NIR 0.45 RED 0.10  NDVI +0.64
dry grass        NIR 0.30 RED 0.25  NDVI +0.09
water            NIR 0.03 RED 0.07  NDVI -0.40
shadow           NIR 0.05 RED 0.04  NDVI +0.11
```
## 5.7 Laboratory work and the course project

The TU outline asks for laboratory work on every topic and a small project in MATLAB or Python. A suggested ten-lab plan (each lab 2 hours) that follows the units:

| Lab | Task | Unit |
|---|---|---|
| 1 | Read, display and write images; pixel arithmetic; colour conversions (RGB, grey, HSV) | 1 |
| 2 | Sampling and quantization: reduce resolution and bit depth and compare | 1 |
| 3 | Point operations: negative, log, gamma, contrast stretching, slicing | 2 |
| 4 | Histogram, equalization, and CLAHE; compare with the textbook result | 2 |
| 5 | Spatial filters: mean, median, Gaussian, Laplacian, unsharp masking | 2 |
| 6 | FFT spectrum, low-pass and high-pass filters, homomorphic filter | 2 |
| 7 | Add noise models and restore: median, adaptive, Wiener deblurring, morphology | 3 |
| 8 | Huffman and run-length coding; DCT block compression at several qualities | 4 |
| 9 | Thresholding (Otsu), edge detection (Sobel, Canny), Hough lines | 5 |
| 10 | Features and a classifier (minimum distance and k-NN) on a small data set | 5 |

**Project ideas.** (a) *Coin counter:* threshold, clean with opening, label components, and measure areas to separate coins by size. (b) *Document scanner:* detect the page edges (Canny, Hough), correct the perspective, and binarize with an adaptive threshold. (c) *Leaf or fruit classifier:* segment, extract shape and colour features, and classify. (d) *Number plate reader:* locate the plate with edges and morphology and read the characters. (e) *Hidden message app:* LSB steganography with a PSNR and capacity report. Whatever the project, the report should follow the pipeline of the book: acquisition, enhancement, restoration, segmentation, feature extraction, classification, with an evaluation (accuracy, confusion matrix, run time) and a discussion of failures.

## 5.8 Summary and exercises

**Segmentation** divides the image into regions by discontinuity or similarity. Thresholding uses the histogram (global, iterative, Otsu: maximize $\sigma_B^{2}$; adaptive for uneven light); region growing and split-and-merge enforce connectivity. Edges are found by the gradient (Roberts, Prewitt, Sobel: $M=\sqrt{G_x^{2}+G_y^{2}}$), the LoG zero crossings and the Canny detector (smooth, gradient, non-maximum suppression, hysteresis); the Hough transform finds lines through voting in the $(\rho,\theta)$ plane and also circles. Features describe regions: chain code, area, perimeter, compactness $P^{2}/A$, moments, texture (histogram statistics, GLCM) and are reduced by PCA. Classifiers: minimum-distance, maximum-likelihood, k-NN; k-means clusters without labels. Case studies: encryption (permutation and diffusion), LSB steganography, robust watermarks, visual effects, medical windowing and remote-sensing indices such as NDVI.

1. Define image segmentation and state the conditions that a segmentation must satisfy. Distinguish the discontinuity and similarity approaches.
2. Explain the iterative global thresholding algorithm and compute it for the pixel values 1, 2, 2, 3, 10, 11, 11, 12.
3. Explain Otsu's method. When does it fail, and what can be done for uneven illumination?
4. Explain region growing and split-and-merge. Compare them with thresholding.
5. What is an edge? Distinguish step, ramp and roof edges and explain how the first and second derivatives locate them.
6. Write the Sobel masks. Compute $G_x$, $G_y$, the magnitude and the direction for the window with rows (10, 10, 100), (10, 10, 100), (10, 10, 100).
7. Compute the Roberts cross-gradient for the 2 x 2 window with rows (10, 50) and (30, 20).
8. Compare Roberts, Prewitt and Sobel operators. Why must the image be smoothed before differentiating?
9. Explain the Laplacian of Gaussian and zero-crossing detection. What does $\sigma$ control?
10. Describe the four steps of the Canny edge detector. What do the two thresholds do?
11. Explain the Hough transform for lines in the $(\rho,\theta)$ form. Find $\rho$ and $\theta$ for the points (2, 2), (4, 4) and (6, 6). How are circles detected?
12. List the types of image features with an example of each. What makes a feature good?
13. Define the chain code. Write the 4-connected chain code and first difference of the boundary of a 4 x 3-pixel rectangle (right 3, down 2, left 3, up 2).
14. Compute the compactness $P^{2}/A$ for a square of side 10 and for a disc of radius 10. What does it say about shape?
15. Define texture. Name the GLCM features and say how they differ for a smooth and a random texture.
16. Explain PCA. If the covariance matrix of two features has eigenvalues 4 and 1, how much variance does the first component explain, and what is the reconstruction error if only it is kept?
17. Explain the minimum-distance classifier. With the class means (2, 2) and (6, 3), classify the point (4.5, 2.6).
18. Explain k-NN. The five nearest neighbours of a point are A (0.5), B (0.8), B (1.1), A (1.4), A (1.6) (distance in brackets). Give the class for $k=3$ and $k=5$.
19. Explain k-means. Perform one full iteration on the points 1, 2, 9, 10, 12 with the initial centres 2 and 9.
20. Define the confusion matrix, accuracy, precision and recall.
21. Distinguish steganography, cryptography and watermarking. How much can a 512 x 512 greyscale image hold in its LSB plane? What changes if the bit to be embedded in the pixel value 156 is 1?
22. Why does LSB embedding not survive JPEG compression? Suggest a more robust method.
23. What is windowing in CT? Compute the display value for 60 HU with level 40 and width 80.
24. Define NDVI. Compute it for NIR = 0.45 and Red = 0.09 and interpret the result.

**Answers to the numerical items.** (2) The mean is 52/8 = 6.5; the classes are (1, 2, 2, 3) with mean 2 and (10, 11, 11, 12) with mean 11; the new threshold is $(2+11)/2=6.5$, so the algorithm stops at **$T=6.5$**. (6) $G_x=(-10+100)+(-20+200)+(-10+100)=\mathbf{360}$; $G_y=0$ (every row of the window is identical, so there is no change down the columns); magnitude **360**, direction $0^{\circ}$: the gradient points to the right and the edge is vertical. (7) $G_x=z_{9}-z_{5}=20-10=10$ and $G_y=z_{8}-z_{6}=30-50=-20$ with the two cross masks, magnitude $\approx|10|+|-20|=\mathbf{30}$ (exactly $\sqrt{500}=22.4$). (11) All three points lie on $y=x$; the normal to this line has $\theta=135^{\circ}$ and $\rho=x\cos135^{\circ}+y\sin135^{\circ}=2(-0.707)+2(0.707)=\mathbf{0}$; the same for the other two points, so their sinusoids meet at $(\rho,\theta)=(0,135^{\circ})$. A circle needs a three-parameter accumulator $(a,b,r)$. (13) Directions 0 right, 1 up, 2 left, 3 down: **0 0 0 3 3 2 2 2 1 1**. First difference (anticlockwise turns, mod 4, circular): **0 0 3 0 3 0 0 3 0 3**: the four 3s are the four corners. (14) Square: perimeter 40, area 100, $P^{2}/A=\mathbf{16}$; disc: $P=62.8$, $A=314.2$, $P^{2}/A=\mathbf{12.57}=4\pi$, the minimum, so a disc is the most compact shape. (16) The first component explains $4/(4+1)=\mathbf{80\%}$ of the variance; the reconstruction mean square error (sum of the discarded eigenvalues) is **1**. (17) $D_1=\sqrt{2.5^{2}+0.6^{2}}=\sqrt{6.61}=2.57$; $D_2=\sqrt{1.5^{2}+0.4^{2}}=\sqrt{2.41}=1.55$; the point belongs to **class 2**. (18) $k=3$: A, B, B, so **B**; $k=5$: three A against two B, so **A**: the answer depends on $k$. (19) Assign 1, 2 to the centre 2 and 9, 10, 12 to the centre 9; new centres $1.5$ and $(9+10+12)/3=10.33$; assigning again gives the same clusters, so the algorithm has converged. (21) $512\times512=262{,}144$ bits $=32{,}768$ bytes **= 32 KB**. $156=10011100_2$ already ends in 0, so embedding 1 gives **157** and embedding 0 leaves it as 156. (23) The window is 0 to 80 HU, so $(60-0)/80\times255=\mathbf{191}$. (24) $(0.45-0.09)/(0.45+0.09)=0.36/0.54=\mathbf{0.67}$: dense, healthy vegetation.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain Otsu's thresholding.**

Otsu's method chooses the global threshold automatically from the histogram. For each candidate $k$ it splits the pixels into two classes, finds the class probabilities $P_1$, $P_2$ and means $m_1$, $m_2$, and computes the between-class variance $\sigma_B^{2}=P_1P_2(m_1-m_2)^{2}$. The best threshold $k^{*}$ is the one that maximizes $\sigma_B^{2}$ (equivalently, minimizes the within-class variance). It needs no parameters and works for a bimodal histogram. It fails when one class is very small or when the illumination is uneven; then adaptive (local) thresholding is used.

**Q2 (5 marks). Explain the Hough transform for line detection.**

Every line can be written as $\rho=x\cos\theta+y\sin\theta$. Each edge pixel votes for all $(\rho,\theta)$ cells whose lines pass through it, which draws a sinusoid in an accumulator array. The sinusoids of collinear points meet in one cell, so the peaks of the accumulator give the lines and the vote count gives the number of pixels on a line. The method tolerates gaps and noise. The same idea with an $(a,b,r)$ accumulator finds circles.

**Q3 (10 marks). Describe edge detection with gradient operators and the Canny method.**

Define an edge and give the models (step, ramp, roof) and the effect of the derivatives (first-derivative magnitude detects, second-derivative zero crossing locates). Give the gradient, its magnitude and direction. Write the Roberts, Prewitt and Sobel masks and compare them (noise sensitivity, smoothing). Add the LoG and zero crossings. Then give the Canny steps: Gaussian smoothing; gradient magnitude and direction; non-maximum suppression; hysteresis thresholding with $T_H$ and $T_L$; mention the criteria (detection, localization, single response). Finish with edge linking and the numerical Sobel example of Exercise 6.

**Q4 (10 marks). Write short notes on steganography, digital watermarking and image encryption.**

Give the aim of each: steganography hides the existence of a message (LSB substitution, capacity 1 bit per pixel, PSNR above 50 dB, but fragile and detectable), watermarking embeds an ownership code that must survive processing (visible and invisible, robust and fragile, spread-spectrum embedding in DCT coefficients and detection by correlation), encryption hides the content (permutation plus diffusion with a key, tested by the histogram, entropy near 8 bits and near-zero neighbour correlation). Compare the three in a table by aim, robustness, imperceptibility and typical use, and quote the numerical results of the programs of Section 5.6 where useful.

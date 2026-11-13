---
subject: Image Processing
grade: BCA Semester 8 (Elective IV)
unit: 1
title: Fundamentals of Image Processing
hours: 8
area: BCA 454 · Image Processing · Unit 1
---

A photograph on a phone, an X-ray in a hospital, a satellite scene of the Koshi floodplain and the face-unlock camera all start the same way: light is measured at a grid of points and stored as numbers. **Digital image processing (DIP)** is the study of changing those numbers on purpose, to make an image look better, to repair damage, to shrink it, or to let a program decide what is in it. This unit builds the vocabulary used in the rest of the book: how an image is represented, how humans see, how a continuous scene becomes a grid of integers, how colour is described and how images are stored.

::: key What this unit gives you
- Image representation, pixel neighbourhoods, adjacency and the three distance measures, with a short program.
- The elements of a DIP system and the three levels of processing (low, mid, high).
- Visual perception: the eye, brightness adaptation, simultaneous contrast and the Mach band effect.
- The simple image formation model $f(x,y)=i(x,y)\,r(x,y)$, sampling, quantization, and what too few samples or levels look like.
- Colour fundamentals and the RGB, CMY(K), HSI and YCbCr models, with conversions computed in code.
- File formats (BMP, PNG, JPEG, GIF, TIFF, DICOM) and basic image operations; brightness, contrast, hue and saturation.
:::

## 1.1 Image representation and pixel relationships

### 1.1.1 What a digital image is

A monochrome image is a function $f(x,y)$ of two spatial coordinates, where the value of $f$ at any point is the **intensity** (grey level) there. In a **digital image** the coordinates and the intensity are all discrete: $x$ takes $M$ values (rows), $y$ takes $N$ values (columns), and $f$ takes one of $L=2^{k}$ levels. The picture is therefore a matrix

$$f(x,y)=\begin{bmatrix} f(0,0) & f(0,1) & \cdots & f(0,N-1)\\ f(1,0) & f(1,1) & \cdots & f(1,N-1)\\ \vdots & \vdots & & \vdots\\ f(M-1,0) & f(M-1,1) & \cdots & f(M-1,N-1)\end{bmatrix}.$$

Each entry is a **pixel** (picture element). Following Gonzalez and Woods the origin is the top-left corner, $x$ runs **down** the rows and $y$ runs **across** the columns; this is the same order as `a[row][col]` in a program, and it is the opposite of the usual mathematical $(x,y)$ plot. A typical 8-bit greyscale image has $k=8$, so $L=256$ and intensities run from 0 (black) to 255 (white).

The storage needed is simple arithmetic: $b = M\times N\times k$ bits. A 1024 x 768 image with 8 bits per pixel needs $1024\times768\times8=6{,}291{,}456$ bits, which is 786,432 bytes (768 KB). A colour image of the same size with three 8-bit channels needs three times that, 2.25 MB, before any compression.

| Image type | Values per pixel | Example |
|---|---|---|
| Binary | 1 bit (0 or 1) | A scanned signature after thresholding; a fax |
| Greyscale | 1 channel, usually 8 bits | A chest X-ray, a scanned page |
| Colour (RGB) | 3 channels, 8 bits each (24 bits) | A phone photo |
| Multispectral | 4 to 20 bands | Landsat 8 has 11 bands (visible, near, short-wave and thermal infrared) |
| Indexed | An index into a colour palette | A GIF or an 8-bit PNG |

```python
import numpy as np
# A tiny 4 x 5 8-bit image: rows are x, columns are y, origin at the top-left.
f = np.array([[ 10,  10,  60,  60, 200],
              [ 10,  40,  60, 120, 200],
              [ 30,  40, 100, 120, 220],
              [ 30,  90, 100, 255, 255]], dtype=np.uint8)
M, N = f.shape
print("shape (M rows, N columns):", f.shape, " dtype:", f.dtype)
print("f(2,3) =", f[2, 3], " (row 2, column 3)")
print("bits for the image  :", M * N * 8, "bits =", M * N, "bytes")
print("size of 1024x768x8  :", 1024 * 768 * 8 // 8, "bytes")
print("size of 1024x768 RGB:", 1024 * 768 * 3, "bytes =", round(1024 * 768 * 3 / 2**20, 2), "MB")
print("min, max, mean      :", f.min(), f.max(), round(float(f.mean()), 2))
```
```output
shape (M rows, N columns): (4, 5)  dtype: uint8
f(2,3) = 120  (row 2, column 3)
bits for the image  : 160 bits = 20 bytes
size of 1024x768x8  : 786432 bytes
size of 1024x768 RGB: 2359296 bytes = 2.25 MB
min, max, mean      : 10 255 100.5
```
### 1.1.2 Neighbours, adjacency and connectivity

Almost every algorithm in this book looks at a pixel together with the pixels around it. For a pixel $p$ at $(x,y)$:

- the **4-neighbours** $N_4(p)$ are the two horizontal and two vertical neighbours $(x\pm1,y)$, $(x,y\pm1)$;
- the **diagonal neighbours** $N_D(p)$ are $(x\pm1,y\pm1)$;
- the **8-neighbours** $N_8(p)=N_4(p)\cup N_D(p)$. Pixels on the border have fewer neighbours.

Let $V$ be the set of intensity values that count as "connected" (for a binary image $V=\{1\}$). Two pixels with values in $V$ are

- **4-adjacent** if one is in the other's $N_4$;
- **8-adjacent** if one is in the other's $N_8$;
- **m-adjacent** (mixed) if they are 4-adjacent, or they are diagonal neighbours **and** the set $N_4(p)\cap N_4(q)$ contains no pixel with a value in $V$.

Mixed adjacency exists to remove the ambiguity of 8-adjacency, where two pixels can be joined by both a diagonal and a two-step 4-path. A **path** from $p$ to $q$ is a sequence of distinct pixels each adjacent to the next; a set of pixels in which every pair is joined by a path inside the set is a **connected component**. Counting components in a thresholded image is the first step in counting rice grains, cells or people.

::: caution 4-connected or 8-connected
The same binary image can have a different number of objects under the two rules. Two black pixels touching only at a corner are two objects under 4-connectivity and one under 8-connectivity. Always state which rule you used; a common convention is 8-connectivity for the objects and 4-connectivity for the background so that the two do not overlap.
:::

### 1.1.3 Distance measures

For pixels $p=(x,y)$ and $q=(s,t)$ a function $D$ is a **distance** (metric) if $D(p,q)\ge0$ with equality only when $p=q$, $D(p,q)=D(q,p)$, and $D(p,z)\le D(p,q)+D(q,z)$. Three are used in practice:

| Name | Formula | Shape of the set at distance $\le r$ |
|---|---|---|
| Euclidean $D_e$ | $\sqrt{(x-s)^2+(y-t)^2}$ | Disc |
| City-block $D_4$ | $\lvert x-s\rvert+\lvert y-t\rvert$ | Diamond |
| Chessboard $D_8$ | $\max(\lvert x-s\rvert,\lvert y-t\rvert)$ | Square |

The pixels with $D_4\le1$ from the centre are exactly the 4-neighbours plus the centre; those with $D_8\le1$ are the 8-neighbours plus the centre. $D_4$ and $D_8$ are the lengths of the shortest 4-path and 8-path.

```python
import numpy as np
from collections import deque

p, q = (2, 3), (7, 9)
de = ((p[0]-q[0])**2 + (p[1]-q[1])**2) ** 0.5
d4 = abs(p[0]-q[0]) + abs(p[1]-q[1])
d8 = max(abs(p[0]-q[0]), abs(p[1]-q[1]))
print("p =", p, " q =", q)
print("Euclidean %.3f   city-block D4 = %d   chessboard D8 = %d" % (de, d4, d8))

def components(img, conn):
    """Label connected components of the 1-pixels (conn = 4 or 8) by breadth-first search."""
    if conn == 4: nb = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:         nb = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
    lab = np.zeros(img.shape, int); n = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] == 1 and lab[i, j] == 0:
                n += 1; lab[i, j] = n; dq = deque([(i, j)])
                while dq:
                    a, b = dq.popleft()
                    for da, db in nb:
                        u, v = a + da, b + db
                        if 0 <= u < img.shape[0] and 0 <= v < img.shape[1] and img[u, v] == 1 and lab[u, v] == 0:
                            lab[u, v] = n; dq.append((u, v))
    return n, lab

b = np.array([[1, 1, 0, 0, 0, 0],
              [0, 1, 0, 0, 1, 1],
              [0, 0, 1, 0, 1, 1],
              [0, 0, 0, 1, 0, 0],
              [1, 0, 0, 0, 0, 1]])
for c in (4, 8):
    n, lab = components(b, c)
    print("%d-connectivity: %d objects" % (c, n))
print(components(b, 8)[1])
```
```output
p = (2, 3)  q = (7, 9)
Euclidean 7.810   city-block D4 = 11   chessboard D8 = 6
4-connectivity: 6 objects
8-connectivity: 3 objects
[[1 1 0 0 0 0]
 [0 1 0 0 1 1]
 [0 0 1 0 1 1]
 [0 0 0 1 0 0]
 [2 0 0 0 0 3]]
```
## 1.2 Elements of a digital image processing system

A DIP system is a chain from scene to decision. Gonzalez and Woods list the building blocks as follows.

```svgfig label="1.1" caption="Elements of a digital image processing system. An image sensor with a digitizer feeds a computer; the problem domain decides which processing, storage and display devices are needed."
f = Fig(700, 250)
f.box(10, 100, 100, 50, "Problem\ndomain\n(scene)", fill=SAND, stroke=AMBER, size=10.5)
f.box(150, 100, 110, 50, "Image sensor\n+ digitizer", size=10.5)
f.box(300, 100, 120, 50, "Specialised\nhardware", size=10.5)
f.box(460, 90, 120, 70, "Computer\n+ image\nprocessing\nsoftware", fill=MINT, stroke=TEAL, size=10.5)
f.box(620, 100, 70, 50, "Display", fill=BLUE, size=10.5)
f.box(460, 190, 120, 40, "Mass storage", size=10.5)
f.box(620, 190, 70, 40, "Hard\ncopy", size=10.5)
f.box(300, 10, 120, 40, "Network", size=10.5)
f.arrow([(110, 125), (150, 125)])
f.arrow([(260, 125), (300, 125)])
f.arrow([(420, 125), (460, 125)])
f.arrow([(580, 125), (620, 125)])
f.arrow([(520, 160), (520, 190)], both=True)
f.arrow([(580, 210), (620, 210)])
f.arrow([(420, 30), (520, 30), (520, 90)], both=True)
```

- **Image sensors** convert light to an electrical signal. Two physical devices are needed: a device sensitive to the energy band of interest (a CCD or CMOS array for visible light, a scintillator for X-rays) and a **digitizer** (analogue-to-digital converter) that samples and quantizes the signal.
- **Specialised image processing hardware** performs fast fixed operations (arithmetic, logic, noise reduction at video rate): today usually a GPU or a camera's image signal processor (ISP).
- **The computer** ranges from a phone to a supercomputer, depending on the task, and runs software built from library routines (MATLAB, Python with NumPy, OpenCV, scikit-image).
- **Mass storage** is needed because images are large: archives are measured in terabytes. Storage is short term (working memory), on-line (disk) or archival (tape, cloud).
- **Image displays** are mostly flat-panel monitors; **hard-copy** devices are laser printers, film recorders and plotters.
- **Networking** carries images; because of the volume, bandwidth is the key issue and is why compression (Unit 4) matters.

### 1.2.1 Fundamental steps and levels of processing

The fundamental steps of DIP are: image acquisition; enhancement; restoration; colour image processing; wavelets and multiresolution processing; compression; morphological processing; segmentation; representation and description; and recognition. The first group of steps takes an image as input and produces an image, and the later group produces *attributes* extracted from the image. The processes are usually grouped into three levels.

| Level | Input to output | Examples | Unit |
|---|---|---|---|
| Low-level | Image to image | Noise removal, contrast enhancement, sharpening | 2, 3 |
| Mid-level | Image to attributes | Segmentation, edge detection, feature extraction | 5 |
| High-level | Attributes to meaning | Recognising, classifying and interpreting objects | 5 |

::: key Image processing, computer vision and computer graphics
**Image processing**: image in, image out. **Computer vision**: image in, description out (what is in it). **Computer graphics**: description in, image out (rendering a model). The boundaries are blurred, because a vision system always uses processing steps, but the three directions are a good way to keep them apart in an exam answer.
:::

## 1.3 Elements of visual perception

Because the usual end user of an enhanced image is a person, the way the human eye and brain respond to intensity shapes the design of algorithms.

### 1.3.1 Structure of the eye

The eye is nearly spherical, about 20 mm across. Light enters through the **cornea**, passes the **iris** (the aperture, whose pupil varies from about 2 to 8 mm), is focused by the **lens** and falls on the **retina** at the back. The retina has two classes of light receptors.

| | Cones | Rods |
|---|---|---|
| Number | 6 to 7 million | 75 to 150 million |
| Location | Concentrated in the **fovea** (centre of vision) | Spread over the whole retina |
| Vision | **Photopic** (bright light), colour, fine detail | **Scotopic** (dim light), no colour, low detail |
| Link to the brain | Each cone has its own nerve end | Several rods share one nerve end |

The **blind spot** is where the optic nerve leaves the retina, with no receptors at all. The fovea is a square of about 1.5 mm x 1.5 mm with roughly 150,000 cones per square millimetre, which is why we have to turn the eye to look directly at a detail. Unlike a camera lens, the focal length of the eye is changed by the ciliary muscle reshaping the lens.

### 1.3.2 Brightness adaptation and discrimination

The eye adapts to an enormous range of intensity, about $10^{10}$ from the scotopic threshold to the glare limit, but it cannot cover that range at once. At any adaptation level $B_a$ it can discriminate only a short range of intensities, below a level $B_b$ everything looks black. This is **brightness adaptation**. The reverse side is **brightness discrimination**: the **Weber ratio** $\Delta I_c/I$, where $\Delta I_c$ is the increment of illumination that is noticed 50% of the time against a background $I$. A small Weber ratio means good discrimination. It is small (about 0.02) at moderate and high luminance, so the eye is good in bright light, and large at low light, where discrimination is poor.

Two consequences matter for imaging. First, **perceived brightness is not a simple function of intensity**: it is roughly logarithmic, which is why a display uses a gamma curve and why 256 levels are enough (steps of about 2% at the bright end are near the Weber limit). Second, two perceptual effects show that the brain adds its own processing:

- **Simultaneous contrast.** A grey square looks darker on a white background than on a black one although its intensity is identical.
- **Mach band effect.** Where a dark region meets a bright one, the eye sees an *undershoot* on the dark side and an *overshoot* on the bright side of the boundary, so the edge looks sharper than it is.

```svgfig label="1.2" caption="The Mach band effect. Five uniform grey strips (top) give a staircase of true intensity (dashed). The perceived brightness (solid) undershoots on the dark side and overshoots on the bright side of every step, so each strip appears to be darker at one edge and brighter at the other, though it is perfectly flat."
f = Fig(680, 270)
greys = ["#2a2a2a", "#555555", "#808080", "#aaaaaa", "#d5d5d5"]
x0, w = 60, 112
for i, g in enumerate(greys):
    f.box(x0 + i * w, 20, w, 70, "", fill=g, stroke=g, r=0)
f.line(60, 235, 620, 235, color=SLATE, sw=1)
f.line(60, 100, 60, 235, color=SLATE, sw=1)
f.text(34, 170, "Intensity", size=9.5, color=SLATE)
vals = [115, 140, 165, 190, 215]
pts = []
for i, v in enumerate(vals):
    pts.append((x0 + i * w, 330 - v)); pts.append((x0 + (i + 1) * w, 330 - v))
f.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 3"/>' % (" ".join("%s,%s" % p for p in pts), SLATE))
perc = [(x0, 330 - vals[0])]
for i, v in enumerate(vals):
    xa, xb = x0 + i * w, x0 + (i + 1) * w
    lo = v + (9 if i > 0 else 0)
    hi = v - (9 if i < 4 else 0)
    perc += [(xa + 10, 330 - lo), (xb - 10, 330 - hi)]
perc.append((x0 + 5 * w, 330 - vals[4]))
f.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (" ".join("%s,%s" % p for p in perc), RED))
f.text(340, 256, "position across the strips", size=9.5, color=SLATE)
f.text(120, 150, "true (dashed)", size=9.5, color=SLATE)
f.text(470, 245, "perceived: solid red", size=9.5, color=RED, bold=True)
```

The Mach band effect is the visual system's own edge enhancement (lateral inhibition between neighbouring receptors). It is the reason sharpening filters, which deliberately overshoot at edges (Unit 2), look natural.

## 1.4 Image formation, sampling and quantization

### 1.4.1 A simple image formation model

An image is formed by light reflected or transmitted by objects. Writing $f(x,y)$ as a product of two components,

$$f(x,y)=i(x,y)\,r(x,y),\qquad 0<i(x,y)<\infty,\qquad 0<r(x,y)<1,$$

where $i$ is the **illumination** (the amount of source light falling on the scene) and $r$ is the **reflectance** (the fraction reflected, 0 for total absorption and 1 for total reflection). Typical values: the sun on a clear day gives $i\approx90{,}000$ lm/m$^2$, a cloudy day 10,000, a full moon 0.1, an office 1,000. Typical reflectances: black velvet 0.01, stainless steel 0.65, white wall paint 0.80, silver-plated metal 0.90, snow 0.93. For a transmission image (X-ray) the reflectance is replaced by a transmissivity. Since $f$ is bounded between $L_{min}=i_{min}r_{min}$ and $L_{max}=i_{max}r_{max}$, the interval $[L_{min},L_{max}]$ is called the **grey scale** and is shifted to $[0,L-1]$ in practice. The product model matters in Unit 2: the homomorphic filter takes the logarithm so the product becomes a sum that can be filtered separately.

### 1.4.2 Sampling and quantization

The output of a sensor is a continuous voltage. To digitize it, two operations are needed:

- **Sampling** digitizes the coordinate values: the scene is measured at regular intervals along $x$ and $y$.
- **Quantization** digitizes the amplitude: each sample is rounded to one of $L=2^k$ levels.

The number of samples sets the **spatial resolution** (pixels per inch or per unit length); $k$ sets the **intensity resolution**. Too few samples gives a blocky image with **aliasing** and the checkerboard effect; too few levels gives **false contouring**, visible ridges in smooth areas such as the sky or a face (usually noticeable below about 5 or 6 bits for natural images). The **sampling theorem** says that to represent a signal faithfully the sampling frequency must be at least twice its highest frequency (the Nyquist rate), a point that returns in Unit 2.

An image of 1024 x 1024 pixels is a "large" image only relatively. Common reference sizes: VGA 640 x 480, HD 1280 x 720, Full HD 1920 x 1080 and 4K UHD 3840 x 2160. The last lines of the program print the uncompressed size of a Full HD frame at 1, 8 and 24 bits per pixel.

```python
import numpy as np
# Build a smooth test image (a diagonal ramp with a bright disc), then reduce levels and samples.
n = 128
y, x = np.mgrid[0:n, 0:n]
img = 255.0 * (x + y) / (2 * (n - 1))
img[((x - 80) ** 2 + (y - 48) ** 2) < 20 ** 2] = 235
img = img.astype(np.uint8)

def requantize(a, k):
    levels = 2 ** k
    step = 256 / levels
    return (np.floor(a / step) * step + step / 2).astype(np.uint8)

for k in (8, 6, 4, 2, 1):
    q = requantize(img, k)
    mse = float(np.mean((img.astype(float) - q.astype(float)) ** 2))
    print("k = %d bits (%3d levels): distinct values used = %3d, MSE = %7.2f, size = %6d bytes" %
          (k, 2 ** k, len(np.unique(q)), mse, n * n * k // 8))

# Reduce spatial resolution by keeping every s-th sample, then compare to the original.
for s in (1, 2, 4, 8):
    small = img[::s, ::s]
    back = np.kron(small, np.ones((s, s), dtype=np.uint8))   # pixel replication back to 128 x 128
    err = float(np.mean((img.astype(float) - back.astype(float)) ** 2))
    print("every %d-th sample: %3d x %3d pixels, MSE after replication = %7.2f" % (s, *small.shape, err))

# Full HD frame sizes
for k in (1, 8, 24):
    print("1920 x 1080 at %2d bits per pixel: %7.2f MB" % (k, 1920 * 1080 * k / 8 / 2**20))
```
```output
k = 8 bits (256 levels): distinct values used = 255, MSE =    0.00, size =  16384 bytes
k = 6 bits ( 64 levels): distinct values used =  64, MSE =    1.46, size =  12288 bytes
k = 4 bits ( 16 levels): distinct values used =  16, MSE =   20.61, size =   8192 bytes
k = 2 bits (  4 levels): distinct values used =   4, MSE =  315.84, size =   4096 bytes
k = 1 bits (  2 levels): distinct values used =   2, MSE = 1295.73, size =   2048 bytes
every 1-th sample: 128 x 128 pixels, MSE after replication =    0.00
every 2-th sample:  64 x  64 pixels, MSE after replication =   56.75
every 4-th sample:  32 x  32 pixels, MSE after replication =  184.19
every 8-th sample:  16 x  16 pixels, MSE after replication =  345.69
1920 x 1080 at  1 bits per pixel:    0.25 MB
1920 x 1080 at  8 bits per pixel:    1.98 MB
1920 x 1080 at 24 bits per pixel:    5.93 MB
```
## 1.5 Colour fundamentals and colour models

### 1.5.1 Fundamentals

In 1666 Newton passed sunlight through a prism and showed that white light is a continuous spectrum of colours from violet (about 400 nm) to red (about 700 nm). The colour a person perceives from an object is decided by the light it reflects: a green object reflects mostly 500 to 570 nm and absorbs the rest, an object that reflects all wavelengths equally looks white, and one that absorbs them all looks black. A **chromatic** light source is described by three quantities.

- **Radiance**: the total energy that leaves the source, in watts.
- **Luminance**: the amount of energy an observer *perceives*, in lumens. Far-infrared sources can have large radiance and zero luminance.
- **Brightness**: the subjective (and so unmeasurable) sensation of intensity, the same idea as in achromatic light.

The human eye has three kinds of cones: about 65% respond mainly to red, 33% to green and only 2% to blue (but the blue cones are the most sensitive). Because of this, all colours are seen as combinations of the three **primary colours** red, green and blue (**RGB**), with CIE standard wavelengths 700, 546.1 and 435.8 nm. The **secondary colours** are made by adding two primaries: magenta (red + blue), cyan (green + blue) and yellow (red + green). A primary of light added to its opposite secondary gives white. The characteristics used to tell one colour from another are **brightness** (intensity), **hue** (the dominant wavelength: red, orange, green) and **saturation** (purity, the amount of white mixed in). Hue and saturation together are called **chromaticity**. A pure spectrum colour is fully saturated; pink is red diluted with white, so it has the same hue but lower saturation.

### 1.5.2 The RGB model

In **RGB** each colour is a point in a unit cube whose three axes are the red, green and blue values, with black at the origin (0,0,0), white at (1,1,1), the primaries on the three axes and the secondaries at the other three corners; the diagonal from black to white holds the greys. A **24-bit** colour image has 8 bits per channel and therefore $(2^{8})^{3}=16{,}777{,}216$ colours. RGB is the model of cameras, scanners and displays (additive mixing on a screen) and the natural model for hardware.

### 1.5.3 CMY and CMYK

Printing works by absorption, so it uses the **secondaries** cyan, magenta and yellow (**CMY**), as subtractive primaries. With the values scaled to $[0,1]$,

$$\begin{bmatrix}C\\M\\Y\end{bmatrix}=\begin{bmatrix}1\\1\\1\end{bmatrix}-\begin{bmatrix}R\\G\\B\end{bmatrix}.$$

A cyan surface reflects no red light. Equal amounts of C, M, Y in theory give black, in practice a muddy dark brown, so printers add a real black ink (**K**) to give the four-colour **CMYK** model: it saves coloured ink, gives a true black and dries faster.

### 1.5.4 HSI (and HSV)

RGB and CMY are not how people describe colour: nobody says "a colour that is 60% red, 30% green and 10% blue". The **HSI** model separates the **intensity** (I) from the colour information carried by **hue** (H) and **saturation** (S), which makes it ideal for algorithms that should work on the brightness alone (histogram equalization of a colour photograph) or on colour alone (segmenting skin tone). With $R,G,B\in[0,1]$,

$$I=\frac{R+G+B}{3},\qquad S=1-\frac{3\,\min(R,G,B)}{R+G+B},\qquad H=\begin{cases}\theta & B\le G\\ 360^{\circ}-\theta & B>G\end{cases}$$

with $\theta=\cos^{-1}\!\left\{\dfrac{\tfrac12[(R-G)+(R-B)]}{\left[(R-G)^{2}+(R-B)(G-B)\right]^{1/2}}\right\}$. Hue is an angle (0 degrees red, 120 green, 240 blue), saturation runs from 0 (grey) to 1 and intensity is the average of the three channels. The related **HSV** model uses $V=\max(R,G,B)$ and is the one in most colour pickers.

### 1.5.5 YCbCr and other models

Video and JPEG use **YCbCr**: a **luma** $Y$ that carries the brightness and two **chroma** differences $C_b$ and $C_r$. Because the eye is much less sensitive to detail in colour than in brightness, the chroma planes can be stored at a lower resolution (4:2:0 sampling keeps one chroma sample per 2 x 2 block of pixels) with little visible loss, which is the first compression saving in JPEG and every video codec. For 8-bit full-range (JFIF) data,

$$Y=0.299R+0.587G+0.114B,\quad C_b=128-0.168736R-0.331264G+0.5B,\quad C_r=128+0.5R-0.418688G-0.081312B.$$

Other models you may meet are **YIQ** (the old NTSC television model, which uses the same luma), **CIE XYZ and Lab** (device independent, used for colour differences), and a **colour look-up table** (the palette of an indexed image).

```python
import numpy as np, colorsys

def rgb_to_cmy(r, g, b):  return 1 - r, 1 - g, 1 - b

def rgb_to_hsi(r, g, b):
    i = (r + g + b) / 3
    s = 0.0 if i == 0 else 1 - min(r, g, b) / i
    num = 0.5 * ((r - g) + (r - b))
    den = ((r - g) ** 2 + (r - b) * (g - b)) ** 0.5
    if den == 0:
        h = 0.0                                  # grey: hue undefined
    else:
        t = np.degrees(np.arccos(np.clip(num / den, -1, 1)))
        h = t if b <= g else 360 - t
    return h, s, i

def rgb_to_ycbcr(r, g, b):                      # r, g, b in 0..255
    y  = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b
    cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b
    return tuple(float(np.clip(v, 0, 255)) for v in (y, cb, cr))

colours = {"red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1), "yellow": (1, 1, 0),
           "pink": (1, 0.6, 0.7), "grey": (0.5, 0.5, 0.5), "orange": (1, 0.5, 0)}
print("%-7s %-17s %-23s %-18s %s" % ("colour", "CMY", "HSI (H deg, S, I)", "HSV (colorsys)", "YCbCr (0-255)"))
for name, (r, g, b) in colours.items():
    c = rgb_to_cmy(r, g, b); h, s, i = rgb_to_hsi(r, g, b)
    hv = colorsys.rgb_to_hsv(r, g, b)
    yy = rgb_to_ycbcr(255 * r, 255 * g, 255 * b)
    print("%-7s %-17s %6.1f %5.2f %5.2f        %5.1f %4.2f %4.2f   %5.1f %5.1f %5.1f" %
          (name, tuple(round(v, 2) for v in c), h, s, i, hv[0] * 360, hv[1], hv[2], *yy))
print("number of 24-bit colours:", 256 ** 3)
```
```output
colour  CMY               HSI (H deg, S, I)       HSV (colorsys)     YCbCr (0-255)
red     (0, 1, 1)            0.0  1.00  0.33          0.0 1.00 1.00    76.2  85.0 255.0
green   (1, 0, 1)          120.0  1.00  0.33        120.0 1.00 1.00   149.7  43.5  21.2
blue    (1, 1, 0)          240.0  1.00  0.33        240.0 1.00 1.00    29.1 255.0 107.3
yellow  (0, 0, 1)           60.0  1.00  0.67         60.0 1.00 1.00   225.9   0.5 148.7
pink    (0, 0.4, 0.3)      346.1  0.22  0.77        345.0 0.40 1.00   186.4 123.5 176.9
grey    (0.5, 0.5, 0.5)      0.0  0.00  0.50          0.0 0.00 0.50   127.5 128.0 128.0
orange  (0, 0.5, 1)         30.0  1.00  0.50         30.0 1.00 1.00   151.1  42.7 202.1
number of 24-bit colours: 16777216
```
::: example Colour to grey
A common greyscale conversion uses the luma weights, $g=0.299R+0.587G+0.114B$, not the plain average. For pure green (0,255,0) the luma gives $0.587\times255\approx150$, while the plain average gives 85. The weights reflect the eye's much higher sensitivity to green: a green and a blue square of equal RGB value look very different in brightness, and a conversion that ignores this makes a red flower disappear against green leaves.
:::

## 1.6 Image file formats

An image file holds a header (size, depth, colour model), optionally a palette and the pixel data, which may be stored **raw** or **compressed**. Compression is **lossless** (the decoded image is identical) or **lossy** (some information is discarded). Raster formats store a grid of pixels; **vector** formats (SVG, EPS) store shapes and are not covered in this course.

| Format | Compression | Colours and features | Typical use |
|---|---|---|---|
| **BMP** | None (or simple RLE) | 1 to 32 bits; palette optional | Windows bitmaps; simple, large |
| **GIF** | Lossless LZW | Up to 256 colours; animation; one transparent colour | Icons, simple animations |
| **PNG** | Lossless (deflate with predictive filters) | Greyscale, palette, 24-bit and 48-bit; alpha channel | Screenshots, logos, web graphics |
| **JPEG** | Lossy (DCT; Unit 4) | 24-bit; no alpha; a quality setting | Photographs |
| **TIFF** | None, LZW, or others | Many bit depths and bands; tags; multiple pages | Scanning, publishing, GIS (GeoTIFF) |
| **PGM / PPM / PBM** | None | The plain Netpbm text/binary formats | Teaching and research |
| **DICOM** | Optional | Image plus patient and scan metadata | Medical imaging (CT, MRI, X-ray) |
| **RAW** | Usually none | The unprocessed sensor data (e.g., Bayer pattern) | Professional photography |

::: tip Choosing a format
Use **PNG** for anything with sharp edges or text (it is lossless), **JPEG** for photographs where small size matters, **TIFF** or raw for archives and editing, and **DICOM** for medical images because it carries the patient data and the exact scan parameters. Saving a JPEG repeatedly adds loss each time, because the compression is applied again.
:::

```python
import numpy as np, struct, zlib

# Write and read back the simplest format, a plain PGM, then a minimal PNG by hand.
img = (np.arange(8 * 8).reshape(8, 8) * 4).astype(np.uint8)
pgm = b"P5\n8 8\n255\n" + img.tobytes()
print("PGM header + data:", pgm[:11], "... total", len(pgm), "bytes (raw = 64 bytes of pixels)")

def png_bytes(a):
    h, w = a.shape
    raw = b"".join(b"\x00" + a[r].tobytes() for r in range(h))      # filter type 0 per scan line
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

big = np.tile(img, (32, 32))                     # 256 x 256 repeating pattern
png = png_bytes(big)
print("PNG signature  :", png[:8])
print("256 x 256 raw  :", big.size, "bytes;  PNG:", len(png), "bytes;  ratio %.1f : 1" % (big.size / len(png)))
rnd = np.random.default_rng(1).integers(0, 256, (256, 256)).astype(np.uint8)
print("random noise   :", rnd.size, "bytes;  PNG:", len(png_bytes(rnd)), "bytes (noise does not compress)")
```
```output
PGM header + data: b'P5\n8 8\n255\n' ... total 75 bytes (raw = 64 bytes of pixels)
PNG signature  : b'\x89PNG\r\n\x1a\n'
256 x 256 raw  : 65536 bytes;  PNG: 579 bytes;  ratio 113.2 : 1
random noise   : 65536 bytes;  PNG: 65880 bytes (noise does not compress)
```
## 1.7 Image operations and basic attributes

### 1.7.1 Brightness, contrast, hue and saturation

- **Brightness** is the overall lightness of the image, close to its mean grey level. Adding a constant to every pixel raises it: $g=f+b$.
- **Contrast** is the difference between the lightest and darkest regions, close to the spread (standard deviation, or $f_{max}-f_{min}$) of the grey levels. Multiplying by a gain about the mean changes it: $g=a\,(f-\bar f)+\bar f+b$ with $a>1$ increasing contrast and $a<1$ lowering it.
- **Hue** is the colour name (the dominant wavelength) and **saturation** is its purity. They live in the H and S channels of HSI or HSV; changing S alone fades a photograph to grey without changing what colour it is, and rotating H shifts every colour round the wheel.

All four are applied by **point operations** that treat each pixel independently, $s=T(r)$; the values must be clipped to $[0,255]$ after the operation, otherwise 8-bit arithmetic wraps around (250 + 10 becomes 4 in `uint8`), producing black speckles in the brightest areas.

### 1.7.2 Classes of operation

| Class | Output pixel depends on | Examples |
|---|---|---|
| **Point** | The same pixel only | Brightness, contrast, negative, thresholding, colour conversion |
| **Local (neighbourhood)** | A small window around the pixel | Smoothing, sharpening, median filter, edge detection |
| **Global** | Every pixel of the image | Fourier transform, histogram equalization, compression |
| **Geometric** | The pixel at a different position | Translation, rotation, scaling, warping |

### 1.7.3 Arithmetic and logic operations

Arithmetic operations act pixel by pixel on two images (or an image and a constant): **addition** (averaging several noisy frames reduces noise; blending two images; brightness change), **subtraction** (detecting change between two frames, removing a background, the mask mode of angiography), **multiplication** (masking, shading correction, gain) and **division** (ratio images such as the vegetation indices in remote sensing). **Logic operations** (AND, OR, NOT, XOR) work on binary images and on bit planes: ANDing with a binary mask extracts a region of interest, and the NOT of a binary image is its negative. **Set operations** on grey images use min for intersection and max for union.

### 1.7.4 Geometric operations and interpolation

A geometric transform maps pixel coordinates by $(x',y')=A(x,y)$: translation, rotation by $\theta$, scaling by $s_x,s_y$ and shear are all captured by a $3\times3$ **affine matrix** in homogeneous coordinates. Implemented forward, the transform leaves holes in the output, so the standard method is **inverse mapping**: for each output pixel, find the source position and *interpolate* its value there.

| Interpolation | Idea | Result |
|---|---|---|
| Nearest neighbour | Copy the closest pixel | Fast; blocky, jagged edges |
| Bilinear | Weighted average of the 4 nearest, $f=(1-a)(1-b)f_{00}+a(1-b)f_{10}+(1-a)bf_{01}+abf_{11}$ | Smooth, slightly blurred |
| Bicubic | Cubic weights of the 16 nearest | Sharper, standard for photographs |

```python
import numpy as np
rng = np.random.default_rng(3)
img = np.clip(rng.normal(100, 30, (64, 64)), 0, 255).astype(np.uint8)

def adjust(f, gain=1.0, bias=0.0):
    m = f.mean()
    return np.clip(gain * (f.astype(float) - m) + m + bias, 0, 255).astype(np.uint8)

print("original         : mean %.1f  std (contrast) %.1f" % (img.mean(), img.std()))
for gain, bias in ((1.0, 40), (1.6, 0), (0.5, 0)):
    g = adjust(img, gain, bias)
    print("gain %.1f bias %+3d: mean %.1f  std %.1f" % (gain, bias, g.mean(), g.std()))

# Overflow demonstration: uint8 wraps, clipping saturates.
a = np.array([250, 100], dtype=np.uint8)
print("250 + 10 in uint8 wraps to", (a + np.uint8(10))[0], "; clipped result is", int(np.clip(int(a[0]) + 10, 0, 255)))

# Averaging K noisy frames of the same scene reduces the noise by about sqrt(K).
scene = np.tile(np.linspace(50, 200, 64), (64, 1))
for K in (1, 4, 16, 64):
    frames = [scene + rng.normal(0, 20, scene.shape) for _ in range(K)]
    avg = np.mean(frames, axis=0)
    print("average of %2d frames: noise std = %5.2f   (theory %5.2f)" % (K, (avg - scene).std(), 20 / K ** 0.5))

# Bilinear interpolation at a fractional position.
def bilinear(f, x, y):
    x0, y0 = int(np.floor(x)), int(np.floor(y)); a, b = x - x0, y - y0
    return ((1-a)*(1-b)*f[x0, y0] + a*(1-b)*f[x0+1, y0] + (1-a)*b*f[x0, y0+1] + a*b*f[x0+1, y0+1])
t = np.array([[10, 20], [30, 80]], dtype=float)
print("bilinear at (0.5, 0.5) of [[10,20],[30,80]] =", bilinear(t, 0.5, 0.5), "(mean of the four)")
print("bilinear at (0.25, 0.75) =", bilinear(t, 0.25, 0.75))
```
```output
original         : mean 99.7  std (contrast) 30.1
gain 1.0 bias +40: mean 139.7  std 30.1
gain 1.6 bias  +0: mean 99.6  std 47.2
gain 0.5 bias  +0: mean 99.1  std 15.0
250 + 10 in uint8 wraps to 4 ; clipped result is 255
average of  1 frames: noise std = 20.13   (theory 20.00)
average of  4 frames: noise std =  9.86   (theory 10.00)
average of 16 frames: noise std =  4.98   (theory  5.00)
average of 64 frames: noise std =  2.52   (theory  2.50)
bilinear at (0.5, 0.5) of [[10,20],[30,80]] = 35.0 (mean of the four)
bilinear at (0.25, 0.75) = 30.0
```
## 1.8 Summary and exercises

A digital image is a matrix of $M\times N$ pixels quantized to $L=2^{k}$ levels and needs $MNk$ bits. Pixels have 4-, diagonal and 8-neighbourhoods, three kinds of adjacency, and Euclidean, city-block and chessboard distances. A DIP system is sensor, digitizer, hardware, computer, storage, display and network; processing is low-level (image to image), mid-level (image to attributes) and high-level (meaning). The eye adapts to a huge intensity range, perceives brightness roughly logarithmically, and shows simultaneous contrast and the Mach band effect. Images are formed as $f=ir$, then sampled (spatial resolution) and quantized (intensity resolution). Colour is described by RGB (additive), CMY(K) (subtractive), HSI/HSV (perceptual) and YCbCr (video). Common formats are BMP, GIF, PNG, JPEG, TIFF and DICOM. Basic operations are point, local, global and geometric, with arithmetic, logic and interpolation tools.

1. Define a digital image. What do $M$, $N$ and $L$ mean, and how many bits are needed to store the image?
2. Distinguish 4-neighbours, diagonal neighbours and 8-neighbours. State the three kinds of adjacency and why m-adjacency was introduced.
3. How much memory does an uncompressed 2048 x 1536 24-bit colour image need? Give the answer in bytes and MB.
4. A 512 x 512 image has 256 grey levels. How much storage is needed, and how much if it is requantized to 16 levels?
5. For $p=(1,2)$ and $q=(4,6)$ find the Euclidean, city-block and chessboard distances.
6. How many bytes does five minutes of uncompressed 1920 x 1080, 24-bit video at 30 frames per second take?
7. Convert the RGB colour (0.2, 0.4, 0.6) to CMY and to HSI.
8. Convert the 8-bit RGB colour (200, 100, 50) to a grey level with the luma weights.
9. Draw the block diagram of a DIP system and state the purpose of each element.
10. Explain the three levels of image processing with an example of each. How do image processing, computer vision and computer graphics differ?
11. Compare rods and cones. What is the fovea and what is the blind spot?
12. Explain brightness adaptation, the Weber ratio, simultaneous contrast and the Mach band effect.
13. Explain the image formation model $f(x,y)=i(x,y)r(x,y)$ with typical values of $i$ and $r$.
14. Distinguish sampling and quantization. What are aliasing and false contouring?
15. Explain the RGB, CMY, HSI and YCbCr models and give one use of each.
16. Compare BMP, GIF, PNG, JPEG, TIFF and DICOM. Which would you choose for a screenshot, a holiday photograph and a CT scan, and why?
17. What are point, local, global and geometric operations? Why is inverse mapping used for geometric transforms?

**Answers to the numerical items.** (3) $2048\times1536=3{,}145{,}728$ pixels, times 3 bytes = **9,437,184 bytes = 9 MB** (binary megabytes). (4) $512\times512\times8=2{,}097{,}152$ bits = **256 KB**; at 16 levels ($k=4$) the size halves to **128 KB**. (5) $D_e=\sqrt{3^2+4^2}=\mathbf{5}$; $D_4=3+4=\mathbf{7}$; $D_8=\max(3,4)=\mathbf{4}$. (6) One frame is $1920\times1080\times3=6{,}220{,}800$ bytes; times 30 is 186,624,000 bytes per second; times 300 s is **55,987,200,000 bytes (about 56 GB)**, which is why video is always compressed. (7) CMY = (0.8, 0.6, 0.4). $I=(0.2+0.4+0.6)/3=0.4$; $S=1-0.2/0.4=0.5$; numerator $\tfrac12[(0.2-0.4)+(0.2-0.6)]=-0.3$, denominator $\sqrt{0.04+(-0.4)(-0.2)}=\sqrt{0.12}=0.3464$, ratio $-0.866$ so $\theta=150^{\circ}$, and since $B>G$, $H=360-150=\mathbf{210^{\circ}}$ (a blue-cyan). (8) $0.299\times200+0.587\times100+0.114\times50=59.8+58.7+5.7=124.2\approx\mathbf{124}$.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain sampling and quantization.**

A camera gives a continuous image. **Sampling** digitizes the coordinates: the image is measured at a regular grid of $M\times N$ points, which sets the spatial resolution. **Quantization** digitizes the amplitude: each sample is rounded to one of $L=2^{k}$ levels, which sets the intensity resolution. Too few samples cause blocky images and aliasing; the sampling theorem needs at least twice the highest spatial frequency. Too few levels cause false contours in smooth regions. Storage is $M\times N\times k$ bits, so a 512 x 512 image with 8 bits needs 256 KB.

**Q2 (5 marks). What is the Mach band effect?**

Where two regions of different uniform brightness meet, the eye perceives an undershoot on the darker side and an overshoot on the brighter side of the boundary, though the real intensity is a plain step. The effect is caused by lateral inhibition between neighbouring receptors in the retina. It shows that perceived brightness is not the same as measured intensity, and it makes edges look sharper. Sharpening filters, which add an overshoot at edges, exploit the same effect.

**Q3 (10 marks). Describe the elements of a digital image processing system and the fundamental steps of image processing.**

Begin with the block diagram: problem domain, image sensor with digitizer, specialised hardware, computer with software, mass storage, display, hard copy and network. Explain each element in one or two sentences (sensor senses the energy band and the digitizer samples and quantizes; specialised hardware does fast fixed operations; the computer runs the software; storage is short-term, on-line and archival; the network is limited by bandwidth). Then give the steps: acquisition, enhancement, restoration, colour processing, wavelets, compression, morphological processing, segmentation, representation and description, recognition. State that the early steps are image-to-image and the later ones image-to-attributes, and end with the three levels (low, mid, high) with one example each.

**Q4 (10 marks). Explain the RGB, CMY and HSI colour models. Why is HSI preferred for some algorithms?**

RGB is additive and is a unit cube with black at the origin and white at (1,1,1); a 24-bit image has about 16.7 million colours; cameras and displays use it. CMY is subtractive, $C=1-R$ and so on, used for printing, with black ink K added in CMYK because equal C, M and Y give a dirty brown. HSI separates intensity $I=(R+G+B)/3$ from hue (an angle) and saturation $S=1-3\min(R,G,B)/(R+G+B)$, the way people describe colour. HSI is preferred when the brightness and colour should be treated independently: equalizing only $I$ improves contrast without shifting the colours, and segmenting by hue is less affected by lighting. State the conversion formulae and illustrate with one numerical example from Exercise 7.

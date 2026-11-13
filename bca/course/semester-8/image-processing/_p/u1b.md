
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

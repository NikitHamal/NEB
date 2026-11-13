
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

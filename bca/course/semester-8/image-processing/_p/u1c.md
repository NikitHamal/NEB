
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
    return y, cb, cr

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

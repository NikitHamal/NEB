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

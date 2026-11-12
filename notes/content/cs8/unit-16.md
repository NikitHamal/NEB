---
subject: Computer Science
grade: 8
unit: 16
title: Computer Graphics
hours: 0
area: Number System, Graphics and Multimedia
---

Every picture you see on a screen is computer graphics: a photo on Facebook, a
Daraz sale banner, the icons on your phone, a cartoon on NTV, the map in a GPS
app and the diagrams in an E-Paath lesson. This lesson explains what computer
graphics are and where they are used, the two ways a computer can store a
picture (raster and vector), the programs used to make and edit pictures, the
main drawing and editing tools, and the image file formats you meet every day.
Grade 9 and 10 build on these words, so learn them exactly.

::: key What the examination asks from this lesson
In the 50-mark school paper this lesson usually gives **one or two objective
questions** (a full form such as JPEG, PNG, GIF or SVG; which program is a
vector editor; what a pixel is), **one or two short questions** (define pixel or
resolution; two uses of computer graphics; two differences between raster and
vector graphics; the use of a Paint tool) and sometimes **a long question**
(raster and vector graphics with examples and four differences; the five image
formats; or the steps to draw and save a picture in Paint). Write differences as
matched pairs, one point of raster against the same point of vector.
:::

## 16.1 Computer graphics: meaning and uses

::: definition Computer graphics
**Computer graphics** are pictures, drawings, charts, designs and animations
that are created, stored, edited and displayed with the help of a computer. The
word is also used for the branch of computer science that deals with making
them.
:::

A computer shows a picture by lighting up thousands of tiny dots on the screen,
or by printing tiny dots of ink on paper. Graphics can be grouped in three
ways.

| Grouped by | Kinds | Examples |
|---|---|---|
| Dimension | **2D** (two-dimensional): flat, with width and height only | photos, posters, icons, cartoons |
| | **3D** (three-dimensional): with width, height and depth; can be turned and seen from any side | game characters, a 3D model of a house, an animated film |
| Interaction | **Interactive**: the user controls what the picture does | video games, a GPS map you can zoom, a flight simulator |
| | **Non-interactive** (passive): the user only watches | a TV advertisement, a printed poster, a film |
| How it is stored | **Raster** and **vector** | explained in section 16.2 |

Computer graphics are used in almost every field.

| Field | How graphics are used | Example |
|---|---|---|
| Graphic design and printing | posters, banners, logos, greeting cards, books, magazines | a Dashain greeting card, the school notice-board poster |
| Advertising | product photos, banners, hoardings, social-media adverts | a Daraz festival-sale banner |
| Entertainment | cartoons, animated films, special effects, video games | mobile games, animated films |
| Education | diagrams, charts, animations and simulations | E-Paath lessons by OLE Nepal, science diagrams |
| Engineering and architecture | **CAD** (computer-aided design) drawings of buildings, roads, bridges and machines | the house plan a municipality approves before building |
| Maps and GIS | digital maps, weather maps, satellite images | Google Maps, a map of flood-hit districts |
| Medicine | X-ray, CT-scan, MRI and ultrasound images; 3D models of organs | a CT scan on a hospital screen |
| Business and science | graphs and charts of data | census charts, share-price graphs |
| Using a computer | icons, buttons and windows of the graphical user interface | the Start menu and app icons |

::: tip Write the field and an example
For "write any two uses of computer graphics", name the field **and** give a
real example: "Advertising: festival-sale banners on websites" earns the mark;
"for advertisement" alone may not.
:::

## 16.2 Raster and vector graphics

A computer can store a picture in two completely different ways: as a grid of
coloured dots, or as a list of shapes.

### Raster graphics

::: definition Raster graphics, pixel and resolution
A **raster graphic** (also called a **bitmap**) is a picture made of a grid of
tiny coloured squares called **pixels**. A **pixel** (short for *picture
element*) is the smallest unit of a digital picture; each pixel holds exactly
one colour. The **resolution** of a raster picture is its number of pixels,
written as width × height, for example 1920 × 1080.
:::

A photograph from a phone, a scanned certificate, a screenshot and a picture
painted in Paint are all raster graphics. A screen is itself a grid of pixels:
each one is made of three tiny lights, red, green and blue.

```photo id="cs8/gfx-subpixels" caption="A laptop screen photographed through a close-up lens. The magnified square in the middle shows the grid of pixels; each pixel is made of three thin red, green and blue sub-pixels whose light mixes into one colour." width="70"
```

**How a pixel stores its colour.** Every colour on a screen is a mix of red,
green and blue light (**RGB**). In ordinary pictures each of the three is a
number from 0 (off) to 255 (full brightness). (255, 0, 0) is pure red,
(255, 255, 255) is white and (0, 0, 0) is black. The crimson and deep blue of
the national flag can be shown with mixes such as (220, 20, 60) and
(0, 56, 147).

::: definition Colour depth
**Colour depth** (bit depth) is the number of bits used to store the colour of
one pixel. With $n$ bits a pixel can have $2^n$ different colours.
:::

```figure caption="Nine pixels, enlarged. Every pixel is stored as three numbers, the amounts of red, green and blue light from 0 to 255. The table shows how many colours each colour depth allows; 24-bit colour, 8 bits for each of R, G and B, is called true colour."
fig, ax = plt.subplots(figsize=(5.0, 2.9))
cols = [[(220, 20, 60), (255, 255, 255), (0, 56, 147)],
        [(255, 0, 0), (0, 128, 0), (0, 0, 255)],
        [(255, 255, 0), (128, 128, 128), (0, 0, 0)]]
names = [["crimson", "white", "deep blue"], ["red", "green", "blue"], ["yellow", "grey", "black"]]
s = 1.0
for r in range(3):
    for c in range(3):
        rgb = cols[r][c]
        x, y = c * s, (2 - r) * s
        ax.add_patch(Rectangle((x, y), s, s, fc=[v / 255 for v in rgb], ec="#9aa1ab", lw=0.8))
        lum = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        tc = INK if lum > 140 else "white"
        ax.text(x + s / 2, y + s * 0.80, names[r][c], ha="center", va="center", fontsize=7.0, color=tc)
        ax.text(x + s / 2, y + s * 0.38, f"R {rgb[0]}\nG {rgb[1]}\nB {rgb[2]}", ha="center", va="center",
                fontsize=7.0, color=tc, fontweight="bold", linespacing=1.15)
ax.text(1.5, 3.12, "nine pixels, enlarged", ha="center", va="bottom", fontsize=7.8, color=INK)
rows = [("Colour depth", "Colours possible", True), ("1 bit per pixel", "2 (black and white)", False),
        ("8 bits per pixel", "2⁸ = 256", False), ("16 bits per pixel", "2¹⁶ = 65,536", False),
        ("24 bits per pixel", "2²⁴ = 16,777,216", False)]
for k, (a, b, head) in enumerate(rows):
    yy = 2.80 - k * 0.56
    ax.text(3.45, yy, a, ha="left", va="center", fontsize=7.8, color=INK, fontweight="bold" if head else "normal")
    ax.text(5.20, yy, b, ha="left", va="center", fontsize=7.8, color=INK, fontweight="bold" if head else "normal")
    if k < len(rows) - 1:
        ax.plot([3.4, 7.05], [yy - 0.28, yy - 0.28], color=GRID if k else MUTED, lw=0.8)
ax.text(5.22, 0.05, "24-bit “true colour”: 8 bits each for R, G and B", ha="center", va="center",
        fontsize=7.2, color=MUTED)
ax.set_xlim(-0.05, 7.1); ax.set_ylim(-0.2, 3.4); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([]); ax.axis("off")
```

More pixels show more detail, but they also need more memory. The figure below
shows one small drawing stored at four resolutions.

```figure caption="The same drawing stored at four resolutions. With 48 pixels the mountain and the sun are only blocks; with 3,072 pixels they are clearly a triangle and a circle. Each time the width and height double, the number of pixels, and the memory needed, becomes four times as large."
from matplotlib.path import Path
fig, axs = plt.subplots(2, 2, figsize=(4.6, 3.7))
tri = [(0.0625, 0.0833), (0.5, 0.875), (0.9375, 0.0833)]
tpath = Path(tri + [tri[0]])
sun = (0.7875, 0.7833, 0.1063)
for ax, (W, H) in zip(axs.flat, [(8, 6), (16, 12), (32, 24), (64, 48)]):
    img = np.ones((H, W, 3))
    for j in range(H):
        for i in range(W):
            cx, cy = (i + 0.5) / W, (j + 0.5) / H
            if ((cx - sun[0]) * 4) ** 2 + ((cy - sun[1]) * 3) ** 2 <= (sun[2] * 4) ** 2:
                img[j, i] = [0.95, 0.66, 0.0]
            elif tpath.contains_point((cx, cy)):
                img[j, i] = [0.11, 0.44, 0.72]
    ax.imshow(img, origin="lower", extent=(0, 4, 0, 3), interpolation="nearest")
    ax.add_patch(Rectangle((0, 0), 4, 3, fill=False, ec="#aab0ba", lw=0.8))
    ax.set_title(f"{W} × {H} = {W * H:,} pixels", fontsize=8.2, color=INK)
    ax.set_xlim(-0.05, 4.05); ax.set_ylim(-0.05, 3.05); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([]); ax.axis("off")
fig.subplots_adjust(wspace=0.10, hspace=0.30)
```

The memory an uncompressed raster picture needs follows directly from its
pixels:

$$ \text{size in bytes} = \frac{\text{width} \times \text{height} \times \text{bits per pixel}}{8} $$

::: example Worked example 16.1 — pixels and memory
**Problem.** (a) A laptop screenshot is 1366 × 768 pixels in 24-bit colour. How
many pixels does it have, and how much memory does it need without
compression? (b) An old 640 × 480 picture uses 8-bit colour. How many colours
can it show, and how many KB does it need? (Take 1 KB = 1024 bytes and
1 MB = 1024 KB.)

**Solution.** (a) Pixels = 1366 × 768 = **1,049,088 pixels**. 24 bits = 3 bytes
per pixel, so size = 1,049,088 × 3 = **3,147,264 bytes**.
In KB: 3,147,264 ÷ 1024 = 3,073.5 KB; in MB: 3,073.5 ÷ 1024 ≈ **3.0 MB**.

(b) 8 bits give 2⁸ = **256 colours**. Pixels = 640 × 480 = 307,200; at 1 byte
per pixel the size is 307,200 bytes = 307,200 ÷ 1024 = **300 KB**.
:::

When a raster picture is enlarged too much, its pixels become visible as small
blocks and its edges look like steps. This is called **pixelation**.

### Vector graphics

::: definition Vector graphics
A **vector graphic** stores a picture as a list of shapes — points, straight
lines, curves, circles and filled areas — each described by numbers such as
coordinates, sizes and colours. The computer redraws the shapes at whatever
size is needed, so a vector picture stays smooth and sharp at any size.
:::

Logos, icons, fonts, maps, diagrams, cartoons and engineering drawings are
usually made as vector graphics. A school logo drawn as a vector looks equally
sharp on an ID card and on a 6-metre banner, because the computer redraws the
circle and the letters at the new size instead of stretching dots.

```figure caption="One picture stored both ways and enlarged. The raster version is a grid of 192 pixels, so its sloping edges become staircases. The vector version is just two shapes, a triangle given by its three corners and a circle given by its centre and radius, so it is redrawn smoothly at any size."
from matplotlib.path import Path
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 3.2))
W, H = 16, 12
tri = [(1.0, 1.0), (8.0, 10.5), (15.0, 1.0)]
sun = (12.8, 9.2, 2.1)
gold = (0.95, 0.66, 0.0)
tpath = Path(tri + [tri[0]])
img = np.ones((H, W, 3))
for j in range(H):
    for i in range(W):
        cx, cy = i + 0.5, j + 0.5
        if (cx - sun[0]) ** 2 + (cy - sun[1]) ** 2 <= sun[2] ** 2:
            img[j, i] = gold
        elif tpath.contains_point((cx, cy)):
            img[j, i] = [0.11, 0.44, 0.72]
a1.imshow(img, origin="lower", extent=(0, W, 0, H), interpolation="nearest")
for k in range(W + 1):
    a1.plot([k, k], [0, H], color="#c3c9d2", lw=0.5)
for k in range(H + 1):
    a1.plot([0, W], [k, k], color="#c3c9d2", lw=0.5)
a1.add_patch(Rectangle((3, 4), 1, 1, fill=False, ec=SERIES[1], lw=1.6, zorder=5))
a1.set_title("Raster: 16 × 12 = 192 pixels", fontsize=8.6, color=INK)
a1.text(W / 2, -0.9, "each square is one pixel\n(one is outlined in red);\nsloping edges become staircases",
        fontsize=7.2, color=MUTED, ha="center", va="top", linespacing=1.3)
a2.fill([p[0] for p in tri], [p[1] for p in tri], color=ACCENT, zorder=2)
t = np.linspace(0, 2 * np.pi, 300)
a2.fill(sun[0] + sun[2] * np.cos(t), sun[1] + sun[2] * np.sin(t), color=gold, zorder=2)
for (x, y) in tri:
    a2.plot(x, y, "s", ms=4.5, mfc="white", mec=INK, mew=0.9, zorder=4)
a2.plot(sun[0], sun[1], "o", ms=3.5, color=INK, zorder=4)
a2.plot([sun[0], sun[0] + sun[2]], [sun[1], sun[1]], color=INK, lw=0.9, zorder=4)
a2.set_title("Vector: the same picture as shapes", fontsize=8.6, color=INK)
a2.text(W / 2, -0.9, "stored as numbers:\ntriangle (1, 1) (8, 10.5) (15, 1)\ncircle, centre (12.8, 9.2), radius 2.1",
        fontsize=7.2, color=MUTED, ha="center", va="top", linespacing=1.3)
for a in (a1, a2):
    a.set_xlim(-0.2, W + 0.2); a.set_ylim(-0.2, H + 0.2); a.set_aspect("equal")
    a.set_xticks([]); a.set_yticks([]); a.axis("off")
fig.subplots_adjust(wspace=0.16)
```

| Point | Raster (bitmap) graphics | Vector graphics |
|---|---|---|
| Made of | a grid of pixels | shapes described by numbers: points, lines, curves |
| When enlarged | becomes blurred or pixelated | stays smooth and sharp at any size |
| File size | depends on the number of pixels; photos give large files | depends on the number of shapes; usually small |
| Best for | photographs and realistic pictures with many shades | logos, icons, fonts, maps, diagrams, cartoons |
| Editing | pixel by pixel, or by selecting areas | shape by shape: move, resize or recolour one object |
| Software | Paint, GIMP, Adobe Photoshop | Inkscape, Adobe Illustrator, CorelDRAW |
| File formats | BMP, JPEG, PNG, GIF | SVG, AI, EPS, CDR (and PDF) |

::: caution Enlarging a raster picture does not add detail
Students often think that making a small photo "bigger" in Paint makes it
clearer. It does not: the computer only spreads the same pixels over a larger
area, so the picture becomes blocky or blurred. Detail can only come from a
camera or scanner with more pixels. A vector picture is different, because its
shapes are redrawn sharp at every size.
:::

::: example Worked example 16.2 — raster or vector?
**Problem.** Say whether each should be made as a raster or a vector graphic,
with a reason: (a) a photo of Phewa Lake; (b) the school logo for ID cards and
a large banner; (c) a map of the seven provinces of Nepal that will be printed
in many sizes; (d) a scanned copy of a citizenship certificate; (e) a set of
app icons.

**Solution.** (a) **Raster** — a photograph has millions of slightly different
colours, which only pixels can record. (b) **Vector** — it must stay sharp from
small to very large sizes. (c) **Vector** — borders and labels are lines and
text that must stay sharp when enlarged. (d) **Raster** — a scanner records the
paper as pixels. (e) **Vector** — simple shapes that are shown at many sizes.
:::

```photogrid label="16.H" cols="3" ratio="1.3" caption="Pixels and the two kinds of graphics software. (a) A magnified screen: every picture is a grid of tiny red, green and blue dots; this is what a raster image is made of. (b) GIMP, a free raster editor, changes pixels: it is used to retouch photographs. (c) Inkscape, a free vector editor, stores shapes as lines and curves described by numbers, so a drawing can be enlarged without blur."
@ photo id="cs8/gfx-subpixels" cap="(a) Pixels on a screen, magnified"
@ photo id="cs8/gfx-gimp" cap="(b) GIMP: a raster editor"
@ photo id="cs8/gfx-inkscape" cap="(c) Inkscape: a vector editor"
```

## 16.3 Graphics software: Paint, GIMP, Inkscape and Canva

::: definition Graphics software
**Graphics software** is application software used to create, edit, view and
print pictures. **Painting and photo-editing programs** work on pixels (raster
graphics); **drawing or illustration programs** work on shapes (vector
graphics); **online design tools** give ready-made templates that anyone can
change.
:::

### Paint

**Microsoft Paint** is a simple raster program that has come with Windows since
1985, so it is on almost every school computer. It has tools for freehand
drawing, shapes, text, colours, selecting, cropping, resizing, rotating and
flipping (section 16.4 explains them). It opens and saves BMP, JPEG, PNG, GIF
and TIFF files; its usual choice is PNG. The Paint of Windows 11 can also work
with **layers**, keep **transparent** backgrounds and remove the background of
a photo with one click. Paint is ideal for beginners and quick jobs, but it has
no filters or advanced photo tools.

### GIMP

**GIMP** (**GNU Image Manipulation Program**) is a free and open-source raster
editor for Windows, macOS and Linux, and a free alternative to Adobe Photoshop.
It is used to retouch and correct photos, cut out objects, join pictures, add
text and apply filters such as blur and sharpen. Its work is organised in
**layers**. GIMP saves its own project format, **XCF**, which keeps the layers,
and exports finished pictures as JPEG, PNG, GIF, TIFF and other formats. GIMP
3.0 was released in March 2025.

```photo id="cs8/gfx-gimp" caption="GIMP 2.10 editing a photograph. The numbered parts are listed below the picture." width="94"
mark 0.035 0.80 "1"
mark 0.035 0.50 "2"
mark 0.47 0.47 "3"
mark 0.88 0.20 "4"
mark 0.285 0.958 "5"
key 1 Toolbox: selection, paint, text, crop and other tools
key 2 Tool options for the chosen tool (here the paintbrush: size, opacity)
key 3 Canvas: the picture being edited
key 4 Layers panel: the picture is built from six layers stacked on each other
key 5 Menu bar: File, Edit, Select, Image, Layer, Colors, Tools, Filters
```

### Inkscape

**Inkscape** is a free and open-source **vector** editor for Windows, macOS and
Linux, a free alternative to Adobe Illustrator and CorelDRAW. Its native format
is **SVG** (Scalable Vector Graphics). It has tools for rectangles, ellipses,
stars and polygons, a pen tool for curves, text, gradients, and a node tool for
moving the points of a shape. Finished work can be exported as PNG for the web
or PDF for printing. It is the right program for logos, posters, badges,
diagrams and maps.

```photo id="cs8/gfx-inkscape" caption="Inkscape 1.0 editing the GTK logo, a vector drawing made of a few filled shapes. Because the shapes are stored as numbers, the logo is shown at 630% zoom (bottom right) without any blurring." width="94"
mark 0.015 0.86 "1"
mark 0.36 0.47 "2"
mark 0.85 0.80 "3"
mark 0.30 0.075 "4"
mark 0.30 0.965 "5"
key 1 Toolbox: select, node, rectangle, ellipse, star, pen, text and other tools
key 2 Canvas with the vector drawing; each coloured face is a separate shape
key 3 Fill and Stroke dialog: colour of the inside (fill) and of the outline (stroke)
key 4 Colour palette
key 5 Menu bar and the tool controls bar
```

### Canva

**Canva** is an online design platform, used in a web browser or as a phone
app, made by an Australian company that started in 2013. It offers thousands of
ready-made **templates** for posters, greeting cards, certificates,
social-media posts and presentations. You pick a template, then drag and drop
your own photos, text, icons and shapes onto it. The basic plan is free and the
**Pro** plan adds more templates and tools for a fee. Canva needs an Internet
connection, and designs are kept online and downloaded as PNG, JPG, PDF or
MP4.

| Point | Paint | GIMP | Inkscape | Canva |
|---|---|---|---|---|
| Type | raster | raster | vector | online design tool (templates) |
| Cost | free with Windows | free and open source | free and open source | free plan; Pro plan paid |
| Needs Internet | no | no | no | yes |
| Layers | in Windows 11 Paint | yes | yes | yes (arranged objects) |
| Own file format | PNG by default | XCF | SVG | saved online |
| Best for | simple drawings, quick edits | photo editing, cut-outs, effects | logos, posters, diagrams, maps | quick posters, cards and posts from templates |
| Paid programs of the same kind | — | Adobe Photoshop | Adobe Illustrator, CorelDRAW | Adobe Express |

Other programs you may meet are **Pixlr** (an online photo editor), **Krita**
(free digital painting), **Blender** (free 3D modelling and animation) and
**AutoCAD** (paid CAD drawings for engineers).

::: tip Choosing the program
Ask what the picture is made of. A photograph to correct or crop: a raster
editor (GIMP, or Paint for simple jobs). A logo or poster that must stay sharp
at any size: a vector editor (Inkscape). A good-looking card in ten minutes with
an Internet connection: Canva.
:::

## 16.4 Drawing and editing a picture

Every Windows computer has Paint, so we learn the tools there; GIMP has the same
tools with more options. Open Paint from the **Start** menu (type "Paint"). The
window has a **title bar** with the file name, a **File** menu, a **toolbar**
(the Home tab of older versions) with groups of tools, the white **canvas** you
draw on, and a **status bar** at the bottom that shows the position of the
pointer and the size of the canvas in pixels.

| Group | Tool | What it does |
|---|---|---|
| Image | **Select** (rectangle or free-form) | marks a part of the picture to move, copy, cut or delete |
| | **Crop** (Ctrl+Shift+X) | keeps only the selected part and throws away the rest |
| | **Resize and skew** (Ctrl+W) | changes the size in per cent or pixels; skew slants the picture |
| | **Rotate / Flip** | turns the picture 90° or 180°, or makes a mirror image |
| Tools | **Pencil** | draws thin freehand lines, like a sharp pencil |
| | **Fill with colour** (bucket) | fills a closed area with the chosen colour |
| | **Text** (A) | adds words in a chosen font, size and colour |
| | **Eraser** | rubs out part of the picture |
| | **Colour picker** (dropper) | copies a colour from the picture so you can use it again |
| | **Magnifier** | zooms in for detail work and out again |
| Brushes | **Brushes** | freehand strokes in styles such as calligraphy, airbrush and oil |
| Shapes | **Shapes** | line, curve, oval, rectangle, rounded rectangle, polygon, triangle, arrows, star, callout; with **Outline** and **Fill** choices |
| Size | **Size** | thickness of lines, brushes and the eraser |
| Colours | **Colour 1 and Colour 2** | Colour 1 is used with the left mouse button, Colour 2 with the right |
| | **Edit colours** | mixes any colour by giving its red, green and blue numbers |

Three habits make drawing easier. Hold **Shift** while drawing an oval or a
rectangle to get a perfect circle or square, and while drawing a line to keep it
straight across, straight down or at 45°. Press **Ctrl+Z** to undo a mistake
and **Ctrl+Y** to redo it. Save often with **Ctrl+S**: **File → Save as**, choose
the format (PNG, JPEG, BMP or GIF), type a name and click **Save**.

::: caution Close the shape before you fill it
The Fill tool pours colour into the area under the pointer until it meets a
line. If the outline of a mountain or a house has even a one-pixel gap, the
colour "leaks" through it and floods the background. Use **Ctrl+Z**, zoom in
with the Magnifier, close the gap with the Pencil, then fill again.
:::

::: example Worked example 16.3 — a Dashain greeting card in Paint
**Problem.** List the steps and the tools used to make a card showing green
hills, a kite in the sky and the words "Happy Dashain", and save it as
`dashain.png`.

**Solution.**
1. Open Paint. Set the canvas to 1200 × 800 pixels with **Image properties**
   (Ctrl+E).
2. **Fill with colour** the canvas light blue for the sky.
3. Draw the hills with the **Curve** shape, from the left edge of the canvas to
   the right edge, so that the area below the curve is closed; **Fill** it with
   green.
4. Draw the kite with the **Diamond** shape, fill it red, and add its string
   with the **Curve** tool.
5. Choose the **Text** tool, click on the sky, pick a large font and colour and
   type "Happy Dashain".
6. Check the details with the **Magnifier**; correct mistakes with **Ctrl+Z**
   or the **Eraser**.
7. **File → Save as → PNG picture**, type `dashain`, click **Save**.
:::

### Editing a photograph

Editing usually means **cropping** away what is not needed, **resizing** for
the web or an e-mail, **rotating** a sideways photo, and correcting
**brightness and contrast**. Paint can crop, resize, rotate and flip; GIMP can
also correct colours (**Colors → Brightness-Contrast**), sharpen or blur
(**Filters**), and remove small spots with the healing tool.

::: definition Layer
A **layer** is like a clear plastic sheet laid over a picture. Each part of the
picture — the background photo, a cut-out, the text — can be put on its own
layer, so it can be moved, changed, hidden or deleted without disturbing the
others. GIMP, Inkscape and Windows 11 Paint all use layers.
:::

::: note Activity 16.1 — draw, save and compare
1. In Paint, draw the greeting card of Worked example 16.3.
2. Save it twice: as `card.png` and as `card.jpg`. Right-click each file in
   File Explorer, choose **Properties** and write down the two sizes.
3. Open a phone photograph in Paint and save it as PNG and as JPEG too. Compare
   the four sizes with the bar chart in section 16.5. Which format won for the
   drawing, and which for the photograph?
4. Zoom the photograph with the Magnifier to 800% until you see its pixels.
:::

## 16.5 Image file formats: BMP, JPEG, PNG, GIF and SVG

::: definition File format and compression
An **image file format** is the way the data of a picture is arranged inside a
file; the **extension** after the dot (.jpg, .png) shows it. **Compression**
makes a file smaller. **Lossless** compression keeps every pixel exactly;
**lossy** compression throws away small details that the eye hardly notices,
so the file becomes much smaller but can never be returned to the original.
:::

| Format | Full form | Type | Compression | Colours | Transparency | Animation | Best for |
|---|---|---|---|---|---|---|---|
| BMP | Bitmap (Windows bitmap) | raster | none: very large files | up to 16.7 million | no | no | simple Windows programs |
| JPEG (JPG) | Joint Photographic Experts Group | raster | lossy | 16.7 million | no | no | photographs |
| PNG | Portable Network Graphics | raster | lossless | 16.7 million | yes | no | logos, screenshots, diagrams, pictures with text |
| GIF | Graphics Interchange Format | raster | lossless, but only 256 colours | 256 | yes (on or off only) | yes | short animations, stickers, simple icons |
| SVG | Scalable Vector Graphics | vector | stored as text instructions, no pixels | any | yes | yes, on web pages | logos, icons, maps on websites |

**BMP** stores the colour of every pixel one after another, so a 24-bit
1200 × 800 picture needs 2,813 KB whatever it shows. **JPEG** is the format of almost every
camera and phone photo: it shrinks photographs ten to twenty times. **PNG** is
lossless, keeps sharp edges and text crisp, and can have a **transparent**
background, so a logo can sit on any colour. **GIF** (introduced in 1987) can
only hold 256 colours but can store several pictures in one file and play them
as an **animation**. **SVG** is a text file of shapes, an open
standard of the World Wide Web Consortium (W3C); web browsers draw it directly.

```figure caption="Measured file sizes when one 1200 × 800 picture was saved in each format (1 KB = 1024 bytes). For the photograph JPEG is 15 times smaller than BMP. For a poster with a few flat colours PNG and GIF are about 16 KB and the SVG version only 0.5 KB, while BMP is still 2,813 KB, so the thin bars on the right can hardly be seen."
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.1, 2.8))
fmts = ["BMP", "PNG", "GIF", "JPEG"]
photo = [2812.6, 1357.9, 530.1, 185.7]
poster = [2812.6, 16.0, 13.5, 38.9, 0.5]
cp = [MUTED, ACCENT, SERIES[3], SERIES[1]]
y = np.arange(4)[::-1]
a1.barh(y, photo, color=cp, height=0.6)
for yi, v in zip(y, photo):
    a1.text(v + 50, yi, f"{v:,.0f} KB", va="center", fontsize=7.3, color=INK)
a1.set_yticks(y); a1.set_yticklabels(fmts, fontsize=7.8)
a1.set_xlim(0, 3900); a1.set_title("a photograph", fontsize=8.4, color=INK)
y2 = np.arange(5)[::-1]
a2.barh(y2, poster, color=cp + [SERIES[2]], height=0.6)
for yi, v in zip(y2, poster):
    lab = f"{v:,.1f} KB" if v < 100 else f"{v:,.0f} KB"
    a2.text(v + 50, yi, lab, va="center", fontsize=7.3, color=INK)
a2.set_yticks(y2); a2.set_yticklabels(fmts + ["SVG"], fontsize=7.8)
a2.set_xlim(0, 3900); a2.set_title("a flat-colour poster", fontsize=8.4, color=INK)
for a in (a1, a2):
    a.spines[["top", "right"]].set_visible(False)
    a.grid(axis="x", color=GRID, lw=0.6); a.set_axisbelow(True)
    a.set_xticks([0, 1000, 2000, 3000]); a.tick_params(axis="x", labelsize=7.2)
    a.set_xlabel("file size (KB)", fontsize=7.6)
fig.subplots_adjust(wspace=0.38)
```

Other formats you will see: **WebP** (a modern web format, smaller than JPEG
and PNG), **TIFF** (high-quality scans and printing), **HEIC** (photos on
iPhones), **PDF** (documents and posters, may contain both pixels and shapes),
and the project formats **XCF** (GIMP), **PSD** (Photoshop) and **AI**
(Illustrator).

::: caution GIF is not lossy, and JPG is not a different format
GIF compression is **lossless**; a photo saved as GIF looks worse only because
its millions of colours are cut down to 256. And **JPG** and **JPEG** are the
same format: old versions of Windows allowed only three letters after the dot.
One real loss to remember: every time a JPEG is edited and saved again, it is
compressed again and loses a little more detail, so keep the original.
:::

::: example Worked example 16.4 — choosing the format
**Problem.** Choose a format for each job and give a reason: (a) photos of the
school sports day for the school's Facebook page; (b) the school logo with a
transparent background for the website; (c) a small moving "Happy Tihar"
sticker; (d) a logo that a printing press will enlarge for a banner; (e) a
screenshot of a program, with small text, for a lab manual.

**Solution.** (a) **JPEG** — photographs compress best with lossy compression
and load quickly. (b) **PNG** — lossless and supports transparency. (c) **GIF**
— it can store a short animation. (d) **SVG** — a vector stays sharp at any
size. (e) **PNG** — lossless, so the small letters stay crisp; JPEG would blur
them.
:::

::: tip Learn the five full forms with the type
Objective questions ask the full forms. Learn them with one more fact each:
BMP — Bitmap, uncompressed; JPEG — Joint Photographic Experts Group, lossy,
photos; PNG — Portable Network Graphics, lossless, transparency; GIF — Graphics
Interchange Format, 256 colours, animation; SVG — Scalable Vector Graphics,
vector.
:::

## Chapter summary

- **Computer graphics** are pictures, drawings, charts and animations made,
  stored, edited and shown by computer; they may be 2D or 3D, interactive or
  non-interactive. Uses: design, advertising, entertainment, education, CAD,
  maps, medicine, charts and the GUI.
- **Raster** (bitmap) graphics are grids of **pixels**; **resolution** is
  width × height in pixels; **colour depth** $n$ bits gives $2^n$ colours
  (24-bit = 16,777,216). Uncompressed size = width × height × bits ÷ 8 bytes.
- Each pixel's colour is a mix of **red, green and blue**, each 0–255.
- **Vector** graphics store shapes as numbers and stay sharp at any size;
  raster pictures **pixelate** when enlarged.
- **Paint** (raster, with Windows), **GIMP** (free raster editor, XCF, layers),
  **Inkscape** (free vector editor, SVG) and **Canva** (online templates, free
  and Pro plans).
- Paint tools: select, crop, resize and skew, rotate/flip, pencil, fill, text,
  eraser, colour picker, magnifier, brushes, shapes, size, Colour 1 and 2.
- **BMP** uncompressed; **JPEG** lossy, photos; **PNG** lossless,
  transparency; **GIF** 256 colours, animation; **SVG** vector.

## Practice questions

**Group A — Objective (1 mark each)**

1. The smallest unit of a raster picture is a <span class="marks">[1]</span>
   (a) bit (b) pixel (c) vector (d) layer
2. Which of these is a vector graphics program? <span class="marks">[1]</span>
   (a) Paint (b) GIMP (c) Inkscape (d) Pixlr
3. The full form of PNG is <span class="marks">[1]</span>
   (a) Portable Network Graphics (b) Picture Network Group (c) Portable New Graphics (d) Printed Network Graphics
4. Which format can store a short animation? <span class="marks">[1]</span>
   (a) BMP (b) JPEG (c) GIF (d) TIFF
5. A photograph from a phone camera is usually saved as <span class="marks">[1]</span>
   (a) SVG (b) JPEG (c) GIF (d) XCF
6. A picture that stays sharp however much it is enlarged is a <span class="marks">[1]</span>
   (a) raster graphic (b) bitmap (c) vector graphic (d) scanned image
7. With 24-bit colour a pixel can show <span class="marks">[1]</span>
   (a) 256 colours (b) 65,536 colours (c) 16,777,216 colours (d) 24 colours
8. In Paint, the tool that fills a closed area with colour is <span class="marks">[1]</span>
   (a) Pencil (b) Fill with colour (c) Colour picker (d) Magnifier
9. Which format normally stores a picture without any compression? <span class="marks">[1]</span>
   (a) BMP (b) JPEG (c) PNG (d) GIF
10. A resolution of 1920 × 1080 means <span class="marks">[1]</span>
    (a) 1920 colours (b) 1920 pixels across and 1080 pixels down (c) 1920 KB (d) 1080 dots per inch
11. JPEG makes photographs small by using <span class="marks">[1]</span>
    (a) lossless compression (b) lossy compression (c) vector shapes (d) only 256 colours
12. An online design tool with ready-made templates for posters and cards is <span class="marks">[1]</span>
    (a) Canva (b) Inkscape (c) BMP (d) Windows
13. Which is an example of interactive graphics? <span class="marks">[1]</span>
    (a) a printed poster (b) a video game (c) a TV advertisement (d) a newspaper photo

::: note Answers to Group A
**1.** (b) — a pixel (picture element) is the smallest unit of a digital picture.
**2.** (c) — Inkscape edits shapes; Paint, GIMP and Pixlr edit pixels.
**3.** (a) — Portable Network Graphics.
**4.** (c) — GIF can hold several frames and play them in turn.
**5.** (b) — JPEG's lossy compression suits photographs.
**6.** (c) — vector shapes are redrawn at every size.
**7.** (c) — $2^{24} = 16,777,216$.
**8.** (b) — the bucket fills the area under the pointer up to its outline.
**9.** (a) — BMP stores every pixel one after another.
**10.** (b) — resolution is width × height in pixels.
**11.** (b) — JPEG throws away detail the eye hardly notices.
**12.** (a) — Canva works online with templates.
**13.** (b) — the player controls what the picture does.
:::

**Group B — Short answer (2 marks each)**

1. Define computer graphics. Write any two of its uses. <span class="marks">[2]</span>
2. What is a pixel? What does a screen resolution of 1366 × 768 mean? <span class="marks">[2]</span>
3. Write any two differences between raster and vector graphics. <span class="marks">[2]</span>
4. Write the full forms of BMP, JPEG, GIF and SVG. <span class="marks">[2]</span>
5. Name two free graphics programs and say whether each one is a raster or a vector program. <span class="marks">[2]</span>
6. What are the uses of the Fill with colour tool and the Colour picker tool in Paint? <span class="marks">[2]</span>
7. Differentiate between lossy and lossless compression, with one format of each. <span class="marks">[2]</span>
8. Find the size in KB of an uncompressed 800 × 600 picture in 24-bit colour (1 KB = 1024 bytes). <span class="marks">[2]</span>
9. What is a layer in GIMP? Give one advantage of using layers. <span class="marks">[2]</span>
10. What is colour depth? How many colours can an 8-bit picture show? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Computer graphics are pictures, drawings, charts and animations created,
stored, edited and displayed with a computer. Uses (any two): advertising
banners; animated films and games; CAD drawings of buildings; digital maps;
X-ray and CT images in hospitals; diagrams in e-learning lessons.

**2.** A pixel (picture element) is the smallest unit of a digital picture,
holding one colour. A resolution of 1366 × 768 means the screen has 1366
pixels across and 768 pixels down, 1,049,088 pixels in all.

**3.** Raster graphics are made of pixels, while vector graphics are made of
shapes described by numbers. A raster picture blurs or pixelates when
enlarged, while a vector picture stays sharp at any size. (Also: raster suits
photographs, vector suits logos and diagrams.)

**4.** BMP — Bitmap; JPEG — Joint Photographic Experts Group; GIF — Graphics
Interchange Format; SVG — Scalable Vector Graphics.

**5.** GIMP — a raster (photo-editing) program; Inkscape — a vector (drawing)
program. (Paint, which comes free with Windows, is also raster.)

**6.** Fill with colour pours the chosen colour into a closed area, such as the
inside of a circle. The Colour picker copies a colour from the picture and makes
it the current colour, so the same shade can be used again.

**7.** Lossless compression makes a file smaller while keeping every pixel
exactly, e.g. PNG (or GIF). Lossy compression throws away small details to make
the file much smaller, and the original cannot be got back, e.g. JPEG.

**8.** Pixels = 800 × 600 = 480,000. 24 bits = 3 bytes, so size =
480,000 × 3 = 1,440,000 bytes = 1,440,000 ÷ 1024 = **1,406.25 KB** (about
1.37 MB).

**9.** A layer is like a transparent sheet laid over a picture; each part of the
picture can be on its own layer. Advantage: one part, such as the text, can be
moved, changed or hidden without disturbing the rest of the picture.

**10.** Colour depth is the number of bits used to store the colour of one
pixel. An 8-bit picture can show $2^8 = 256$ colours.
:::

**Group C — Long answer (4 marks each)**

1. What are raster and vector graphics? Explain each with two examples and write any four differences between them. <span class="marks">[4]</span>
2. Describe the image formats BMP, JPEG, PNG, GIF and SVG: give the type, the kind of compression and one use of each. <span class="marks">[4]</span>
3. Write the steps to draw a greeting card in Paint using shapes, colours and text, and to save it as a PNG file. Name the tools you use. <span class="marks">[4]</span>
4. Compare Paint, GIMP, Inkscape and Canva in a table: type, cost, need for the Internet and best use. <span class="marks">[4]</span>
5. A camera takes photos of 4000 × 3000 pixels in 24-bit colour. (a) How many pixels does a photo have? (b) What is its uncompressed size in MB? (c) Saved as JPEG it is 3.5 MB; how many times smaller is that? (d) How many such JPEG photos fit on a 16 GB memory card? (1 KB = 1024 bytes, 1 MB = 1024 KB, 1 GB = 1024 MB) <span class="marks">[1+1+1+1]</span>

::: note Answers to Group C
**1.** *Raster graphics* are pictures made of a grid of pixels, each holding one
colour; examples: a phone photograph, a scanned certificate. *Vector graphics*
store pictures as shapes — points, lines, curves and filled areas — described by
numbers; examples: a school logo, a map of Nepal's provinces. Differences
(any four): (1) raster is made of pixels, vector of shapes; (2) raster
pixelates when enlarged, vector stays sharp; (3) raster files of photos are
large, vector files are usually small; (4) raster suits photographs, vector
suits logos, icons and diagrams; (5) raster is edited in Paint or GIMP, vector
in Inkscape or Illustrator; (6) raster formats are BMP, JPEG, PNG, GIF, vector
formats SVG, AI, EPS.

**2.** *BMP* (Bitmap): raster, uncompressed, very large files; used by simple
Windows programs. *JPEG* (Joint Photographic Experts Group): raster, lossy
compression, 16.7 million colours, no transparency; used for photographs.
*PNG* (Portable Network Graphics): raster, lossless, supports transparency; used
for logos, screenshots and diagrams. *GIF* (Graphics Interchange Format):
raster, lossless but only 256 colours, supports animation; used for stickers and
short animations. *SVG* (Scalable Vector Graphics): vector, stored as text
instructions, sharp at any size; used for logos, icons and maps on websites.

**3.** (1) Open Paint from the Start menu and set the canvas size with Image
properties (Ctrl+E). (2) Fill the background with the **Fill with colour** tool. (3) Draw
hills, a kite or a house with the **Shapes** tools (curve, polygon, oval,
rectangle), choosing **Size** and **Colour 1**; hold Shift for a perfect circle
or square. (4) Fill each closed shape with colour. (5) Add the greeting with the
**Text** tool, choosing font, size and colour. (6) Correct mistakes with
**Ctrl+Z** or the **Eraser**, using the **Magnifier** for detail. (7) Save: File →
Save as → PNG picture → type the name → Save.

**4.**

| Point | Paint | GIMP | Inkscape | Canva |
|---|---|---|---|---|
| Type | raster | raster | vector | online templates |
| Cost | free with Windows | free, open source | free, open source | free plan, paid Pro |
| Internet | not needed | not needed | not needed | needed |
| Best use | simple drawings and quick edits | photo editing and effects | logos, posters, diagrams | quick cards, posters and posts |

**5.** (a) 4000 × 3000 = **12,000,000 pixels** (12 megapixels).
(b) 12,000,000 × 3 bytes = 36,000,000 bytes; ÷ 1024 ÷ 1024 ≈ **34.3 MB**.
(c) 34.3 ÷ 3.5 ≈ **9.8 times smaller** — the effect of lossy compression.
(d) 16 GB = 16 × 1024 = 16,384 MB; 16,384 ÷ 3.5 = 4,681.1, so **4,681 photos**.
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. What is computer graphics? Differentiate raster and vector graphics, with the file-size calculation of a raster image. <span class="marks">[10]</span>
2. Explain eight uses of computer graphics and the common image file formats. <span class="marks">[10]</span>

### Model answer D1: raster and vector graphics (10 marks)

**Introduction.** **Computer graphics** means making, editing and showing pictures with the help of a computer. A computer stores a picture in one of two ways, as **raster** (bitmap) or **vector** graphics (Plate 16.H).

**Raster graphics.** The picture is a grid of tiny squares called **pixels**, and each pixel has a colour. Photographs from a camera or a phone are raster images. Paint and GIMP work with them. When we enlarge a raster image the pixels become visible and the picture looks blurred or blocky. The quality depends on the **resolution**, the number of pixels in the picture.

**Vector graphics.** The picture is stored as shapes (lines, curves, circles, rectangles) described by mathematical formulas, with their colour and position. Inkscape, CorelDRAW and Adobe Illustrator work with them. A vector picture can be enlarged to any size without loss of quality, and the file is usually small. It is used for logos, maps and diagrams.

| Point | Raster (bitmap) | Vector |
|---|---|---|
| Made of | Pixels | Lines, curves and shapes (formulas) |
| Zoom in | Becomes blurred | Stays sharp |
| File size | Large for large pictures | Usually small |
| Best for | Photographs, realistic pictures | Logos, drawings, maps |
| Editing | Pixel by pixel | Edit each shape |
| Software | Paint, GIMP, Photoshop | Inkscape, CorelDRAW, Illustrator |
| File types | BMP, JPEG, PNG, GIF | SVG, AI, CDR |

**File-size calculation of a raster image.** The size = number of pixels × bits for each pixel.

- A picture of 800 × 600 pixels with 24-bit colour has 800 × 600 = 480,000 pixels. Size = 480,000 × 24 bits = 480,000 × 3 bytes = 1,440,000 bytes, which is about 1406 KB, or about 1.37 MB.
- The same picture in black and white (1 bit per pixel) needs 480,000 bits = 60,000 bytes, about 58.6 KB.

So more pixels and more colours mean a bigger file.

**Conclusion.** Use raster graphics for photographs and vector graphics when the picture must be resized often or must stay sharp.

### Model answer D2: uses of graphics and image file formats (10 marks)

**Introduction.** Graphics are everywhere on a screen. Eight of their main uses are given below.

1. **Education.** Diagrams, charts, maps and animation make lessons clear, as in the pictures of a science book.
2. **Art and design.** Artists and designers draw posters, logos and cards, with tools such as Canva and Inkscape.
3. **Entertainment.** Films, cartoons and video games are built from computer graphics.
4. **Business.** Charts and graphs show sales and profit, and advertisements are made with graphics.
5. **Medicine.** CT scans, MRI and X-ray images are shown and studied on screen.
6. **Engineering and architecture.** CAD drawings of buildings, bridges and machines are made before building them.
7. **Science and maps.** Weather maps, satellite pictures and GPS maps are all computer graphics.
8. **Publishing and photography.** Newspapers, books and photographs are edited and printed using graphics software.

**Common image file formats.**

| Format | Full form | Type | Features |
|---|---|---|---|
| BMP | Bitmap | Raster | Uncompressed, large file, high quality |
| JPEG (JPG) | Joint Photographic Experts Group | Raster | Compressed with some loss, small file, best for photographs |
| PNG | Portable Network Graphics | Raster | Compressed without loss, supports transparency, good for logos and screenshots |
| GIF | Graphics Interchange Format | Raster | Only 256 colours, supports simple animation |
| SVG | Scalable Vector Graphics | Vector | Sharp at any size, small file, used on web pages |

**Graphics software.** Paint (simple drawing), GIMP (photo editing, free), Inkscape (vector drawing, free), Canva (online design) and Photoshop (professional).

**Conclusion.** Graphics make information clear and attractive, and the right software and file format should be chosen for each purpose.

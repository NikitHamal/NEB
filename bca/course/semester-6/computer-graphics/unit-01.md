---
subject: Computer Graphics and Animation
grade: BCA Semester 6
unit: 1
title: Introduction and Graphics Hardware
hours: 5
area: BCA 351 · Computer Graphics and Animation · Unit 1
---

Every image on a screen, whether a game, a map, a Nepali newspaper page or the cursor you are watching, is a grid of coloured dots whose values were computed by a program. **Computer graphics** is the discipline of computing those values: starting from a *description* of a scene (shapes, positions, materials, lights) and producing an *image* (a block of numbers in memory that the display hardware turns into light). This unit introduces what graphics is used for, how displays and memory organise an image, and does the arithmetic that sizes a frame buffer. The remaining units then follow the **graphics pipeline**, from lines and circles to transformations, clipping, 3D viewing, shading, curves and animation.

::: key What this unit gives you
- Applications and the main areas of graphics: modelling, rendering, animation, image processing.
- Raster-scan and vector displays; pixels, resolution, aspect ratio, colour depth, look-up tables.
- Frame-buffer size, refresh bandwidth and timing calculations.
- The graphics pipeline and the roles of the GPU and of graphics software standards.
:::

## 1.1 Applications and areas

Graphics is everywhere: **user interfaces** (windows, icons, touch gestures), **computer-aided design (CAD)** of buildings, machines and circuits, **scientific and information visualisation** (weather maps, charts, medical scans), **games and entertainment** (film effects, real-time 3D), **simulation and training** (flight and driving simulators), **virtual and augmented reality**, **cartography and GIS** (a municipality's ward map), **education** and **art and typography** (rendering Devanagari fonts). The field divides into four closely related areas.

| Area | Question it answers | Example |
|---|---|---|
| **Modelling** | How do we describe shapes mathematically? | A mesh of triangles for a temple; a Bézier curve for a letter |
| **Rendering** | How do we turn a model into a 2D image? | Projection, hidden-surface removal, lighting |
| **Animation** | How do we make the image change over time? | Keyframes, interpolation, physics |
| **Image processing / computer vision** | How do we analyse or improve an existing image? | Blur, edge detection, face detection (the reverse of rendering) |

*Interactive* graphics (a game) must produce a new image 30 to 120 times a second; *offline* rendering (a film) may spend hours on a single frame. The same mathematics serves both.

## 1.2 Display devices

### Raster-scan displays

Most displays today are **raster** devices. The image is a rectangular array of picture elements, **pixels**, each holding a colour value. The hardware reads the array row by row (*scan lines*), top to bottom, and sends each value to the screen. The classic cathode-ray tube (CRT) swept an electron beam across the phosphor, with a **horizontal retrace** at the end of each line and a **vertical retrace** at the end of each frame; modern **LCD** and **OLED** panels address pixels electronically but the same scanning model and terminology survive. Rasters are good at *filled areas* and *continuous colour*, and are the basis of photographs, video and 3D rendering. The cost is the memory needed and the "jaggies": a line that is not horizontal or vertical must be approximated by pixels (the **staircase** or *aliasing* effect), which is why Unit 2 exists.

### Random-scan (vector) displays

A **vector display** (random-scan, calligraphic) draws only the lines of a picture, directing the beam from endpoint to endpoint according to a *display list* of drawing commands. It gives smooth, sharp lines with little memory, but cannot fill areas with arbitrary colour and flickers when the list is long. It survives as an idea in **plotters** and in vector formats such as **SVG**, where a drawing is a list of shapes that is *rasterised* only when displayed. The difference matters daily: a vector logo scales to any size without blur, a raster image does not.

| | Raster scan | Random scan (vector) |
|---|---|---|
| Stores | Colour of every pixel | List of lines and commands |
| Memory | Large (width × height × depth) | Small |
| Refresh | Fixed rate, independent of content | Depends on the number of lines |
| Filled areas, photos | Excellent | Poor |
| Lines | Aliased (staircase) | Smooth |
| Scaling | Blurry or blocky | Perfect |
| Typical use | Monitors, TV, phones | Plotters, laser light shows, SVG |

### Colour, resolution and aspect ratio

**Resolution** is the number of pixels horizontally × vertically (1920 × 1080); **pixel density** is pixels per inch. **Colour depth** (bits per pixel) determines how many colours can be shown: 1 bit gives 2 (black and white), 8 bits give 256, and **true colour** uses 24 bits (8 each for red, green and blue) giving 2²⁴ = **1,67,77,216** colours; a fourth 8-bit channel (alpha, for transparency) gives 32 bits. The **aspect ratio** is width : height; 1920 × 1080 reduces to **16:9** (widescreen), and a mismatch between image and screen aspect ratios causes stretching or black bars. Colour on displays is made by **additive mixing** of red, green and blue light (RGB), while printers use **subtractive** cyan, magenta, yellow and black (CMYK). The **HSV/HSL** models describe the same colours by hue, saturation and value, which is more intuitive for pickers.

## 1.3 The frame buffer and its arithmetic

The **frame buffer** (video memory) holds the colour of every pixel; the **video controller** reads it continuously and drives the display. Its size is

**size (bytes) = width × height × bits per pixel ÷ 8.**

::: example Frame-buffer sizes
- 640 × 480 at 8 bits: 640 × 480 = 3,07,200 pixels, so the buffer is **3,07,200 bytes**.
- 1920 × 1080 at 24 bits: 20,73,600 pixels × 3 bytes = **62,20,800 bytes** (5.93 MiB).
- 3840 × 2160 (4K) at 32 bits: **3,31,77,600 bytes** (31.64 MiB), four times the pixels of full HD.

**Refresh bandwidth.** To redraw 1920 × 1080 at 24 bits sixty times a second the controller must read 62,20,800 × 60 = **37,32,48,000 bytes per second** (373.2 MB/s), and, because the buffer is rewritten by the processor too, memory bandwidth is a real constraint. **Timing:** one frame lasts 1/60 s; with 1080 lines, one scan line takes about **15.43 µs**, and each pixel about **8.04 ns**, so the pixel clock exceeds 124 MHz (more once blanking intervals are added).
:::

**Look-up tables (colour palettes).** To save memory on old displays, each pixel stores an *index* (8 bits) into a **colour look-up table (LUT)** of 256 entries of 24-bit colours (256 × 24 = **6144 bits** of table). A 1024 × 768 image then needs 7,87,200 bytes (the indices plus the 768-byte table) instead of 23,59,296 bytes in true colour, a saving of **15,72,096 bytes**, at the cost of only 256 simultaneous colours. Palette tricks survive in GIF and PNG-8 images.

**Double buffering.** If the program draws into the buffer being displayed, the viewer sees half-drawn frames (flicker and tearing). *Double buffering* draws the next frame into a *back buffer* and swaps it with the *front buffer* during the vertical retrace, which is why graphics libraries have a "swap buffers" call. A **depth buffer** (Unit 6) adds a second per-pixel array of depth values.

## 1.4 The graphics pipeline and the GPU

A renderer for 3D scenes performs a sequence of stages, the **graphics pipeline**; the units of this book follow it.

1. **Modelling:** objects are defined in their own coordinates (Units 3, 5, 7).
2. **Modelling transformation:** place each object in the *world* (Unit 3, 5).
3. **Viewing transformation:** express the world relative to the camera (Unit 5).
4. **Projection:** reduce 3D to 2D (Unit 5).
5. **Clipping:** discard what lies outside the view (Unit 4).
6. **Viewport mapping:** scale to screen coordinates (Unit 3).
7. **Rasterisation (scan conversion):** turn lines and polygons into pixels (Unit 2).
8. **Visibility and shading:** decide which surface is seen and compute its colour (Unit 6).
9. **Display:** write to the frame buffer.

A **graphics processing unit (GPU)** is a processor with thousands of simple cores that run the *same* program on many vertices or pixels at once (data parallelism); programmable **vertex shaders** and **fragment (pixel) shaders** replaced the fixed-function pipeline. Programmers reach it through **APIs** such as **OpenGL**, **Vulkan**, **DirectX** and **Metal** (and WebGL in browsers); older textbooks use a simple library such as the *Graphics Library of the C language*. The principles are unchanged.

## Chapter summary

- Graphics covers modelling, rendering, animation and image processing; applications range from CAD to games to maps.
- Raster displays store every pixel and give filled colour images with aliasing; vector displays store lines and scale perfectly.
- Frame-buffer size = width × height × bits ÷ 8: 1920 × 1080 × 24 bits needs 62,20,800 bytes and about 373.2 MB/s at 60 Hz.
- A look-up table trades colour range for memory; double buffering prevents flicker.
- The pipeline runs from modelling through viewing, projection, clipping and rasterisation to display, and GPUs execute it in parallel.

## Practice

1. Name four applications of computer graphics and the area (modelling, rendering, animation, image processing) each emphasises.
2. Differentiate raster-scan and random-scan displays.
3. Compute the frame-buffer size for 1280 × 720 at 24 bits per pixel.
4. How many bytes does an 800 × 600 image with an 8-bit palette need, including a 256-entry 24-bit table?
5. How many colours can 15-bit colour (5 bits per channel) represent?
6. Reduce 1366 × 768 to its aspect ratio (approximately) and say whether it is wider or narrower than 4:3.
7. Explain how a colour look-up table saves memory.
8. Why is double buffering used?
9. List the stages of the graphics pipeline in order.
10. Why are vector formats such as SVG preferred for logos?

::: note Answers and worked solutions
**1.** CAD (modelling); film effects (rendering and animation); medical scans (visualisation/image processing); GIS maps (modelling and rendering).
**2.** Raster scan stores the colour of every pixel and refreshes at a fixed rate (good for filled areas, aliased lines); random scan draws only lines from a display list (smooth lines, little memory, poor fills).
**3.** 1280 × 720 × 3 = **27,64,800 bytes** (2.64 MiB).
**4.** 800 × 600 = 4,80,000 bytes of indices + 768 bytes of table = **4,80,768 bytes**.
**5.** 2¹⁵ = **32,768** colours.
**6.** 1366/768 = 1.779, close to 16:9 (1.778); wider than 4:3 (1.333).
**7.** Each pixel stores a short index (8 bits) instead of a full 24-bit colour; the full colours are stored once in the table.
**8.** To draw the next frame off-screen and swap during the vertical retrace so that half-drawn frames are never shown.
**9.** Modelling, modelling transform, viewing transform, projection, clipping, viewport mapping, rasterisation, visibility and shading, display.
**10.** Vector graphics are resolution-independent: they scale without blur and have small files.
:::

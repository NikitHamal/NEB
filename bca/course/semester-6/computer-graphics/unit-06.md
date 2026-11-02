---
subject: Computer Graphics and Animation
grade: BCA Semester 6
unit: 6
title: Visible Surfaces, Illumination and Shading
hours: 7
area: BCA 351 · Computer Graphics and Animation · Unit 6
---

Two questions turn a projected wireframe into a convincing picture. **Which surface is in front** at each pixel (hidden-surface removal)? And **what colour** is that surface, given the lights, its material and the viewing direction (illumination and shading)? This unit answers the first with the Z-buffer (traced on a small grid) and the painter's algorithm, and the second with the Phong illumination model, then compares flat, Gouraud and Phong shading on a case where Gouraud shading completely misses a highlight. The Z-buffer grid was recomputed against a direct minimum over polygons, and all vectors were normalised and dotted by numpy.

::: key What this unit gives you
- Hidden-surface methods: back-face, depth (Z) buffer, painter's algorithm, scan-line and area subdivision, ray casting.
- The Phong illumination model: ambient, diffuse (Lambert) and specular terms, with a worked intensity.
- Flat, Gouraud and Phong shading, and why highlights differ.
- Basic ideas of textures, shadows and ray tracing.
:::

## 6.1 Hidden-surface removal

The methods fall into two groups: **object-space** methods compare objects with each other (painter's algorithm, back-face detection), while **image-space** methods decide visibility pixel by pixel (Z-buffer, ray casting, scan-line).

### The depth buffer (Z-buffer)

Keep, beside the frame buffer, a **depth buffer** with one value per pixel, initialised to the far value (infinity). For every polygon, for every pixel (x, y) it covers, compute its depth z; if **z < depth[x, y]** (nearer than what is stored, with smaller z meaning nearer), store the polygon's colour in the frame buffer and z in the depth buffer; otherwise discard the pixel. Depth along a scan line is found incrementally from the plane equation Ax + By + Cz + D = 0: z = −(Ax + By + D)/C, so moving one pixel right changes z by −A/C.

```text
for each pixel (x, y): depth[x, y] = infinity; colour[x, y] = background
for each polygon P:
    for each pixel (x, y) covered by P:
        z = depth of P at (x, y)
        if z < depth[x, y]:
            depth[x, y] = z
            colour[x, y] = shade(P, x, y)
```

::: example A 4 × 4 buffer with two polygons
Polygon A is a 3 × 3 square at constant depth 5 covering pixels x, y ∈ {0, 1, 2}. Polygon B is a slanted 3 × 3 square covering x, y ∈ {1, 2, 3} whose depth is 3 at x = 1, 4 at x = 2 and 5 at x = 3 (depth = 2 + x). Rendering A then B gives the depth buffer

|  | x=0 | x=1 | x=2 | x=3 |
|---|---|---|---|---|
| y=0 | 5 | 5 | 5 | ∞ |
| y=1 | 5 | 3 | 4 | 5 |
| y=2 | 5 | 3 | 4 | 5 |
| y=3 | ∞ | 3 | 4 | 5 |

and the visible colours

|  | x=0 | x=1 | x=2 | x=3 |
|---|---|---|---|---|
| y=0 | A | A | A | . |
| y=1 | A | B | B | B |
| y=2 | A | B | B | B |
| y=3 | . | B | B | B |

The polygons overlap on 4 pixels (x, y ∈ {1, 2}); at all of them B is nearer (4 wins, 0 ties). The result is the same whichever polygon is drawn first, and a total of 18 pixel tests were made, one per covered pixel.
:::

**Properties.** The Z-buffer is simple, works for any surfaces that can supply a depth, needs no sorting and handles interpenetrating objects; it costs memory (a 1920 × 1080 depth buffer of 32 bits is 8 MB) and each pixel is tested once per overlapping polygon. Its precision is limited, so **z-fighting** occurs when two surfaces are nearly coplanar (the far plane should be as near as possible). The **A-buffer** extends it to transparency by keeping a list per pixel. Z-buffering is built into every GPU.

### Other methods

- **Painter's algorithm (depth sort):** sort polygons from far to near and paint them in that order so that nearer ones overwrite farther ones. It fails when polygons overlap cyclically or intersect, which must be solved by splitting polygons. **BSP trees** precompute a correct order for static scenes.
- **Scan-line method:** for each scan line, find the visible polygon in each span between edge crossings, using depth only where polygons overlap.
- **Area subdivision (Warnock):** recursively split the window until each piece contains at most one visible surface or is a single pixel.
- **Ray casting:** shoot a ray from the eye through each pixel and take the nearest intersection; this leads to ray tracing.
- **Back-face culling** (Unit 5) removes surfaces facing away; it is a first step before the methods above.

## 6.2 Illumination models

An **illumination model** computes the intensity of light leaving a surface point towards the viewer. The **Phong model** is the standard empirical model: the intensity is the sum of three terms for each colour channel:

**I = k_a·I_a + k_d·I_d·(N · L) + k_s·I_s·(R · V)ⁿ**

with unit vectors **N** (surface normal), **L** (towards the light), **V** (towards the viewer) and **R** (the reflection of L about N, R = 2(N · L)N − L); the dot products are clamped at 0.

- **Ambient** k_a·I_a: a constant term standing for light scattered everywhere, so that unlit faces are not pure black.
- **Diffuse (Lambertian)** k_d·I_d·(N · L): matte reflection, brightest when the surface faces the light (N · L = cos θ = 1) and zero when edge-on; it does not depend on the viewer.
- **Specular** k_s·I_s·(R · V)ⁿ: the shiny highlight, strongest when the reflected ray points at the viewer; the **shininess exponent n** controls its size (n = 1 is a broad glow, n = 200 a tiny sharp spot).

**Attenuation** divides the diffuse and specular terms of a point light by a factor such as 1/(c₁ + c₂d + c₃d²), where d is the distance, so that distant lights are dimmer. **Blinn–Phong** replaces R · V by N · H with the **halfway vector H = (L + V)/|L + V|**, which is cheaper and is the form used in most real-time systems. Several lights are summed. Colour is handled by evaluating the equation separately for red, green and blue with the material coefficients for each channel.

::: example Phong intensity for one point
Take N = (0, 0, 1), light direction L = (1, 1, 1)/√3 and viewer V = (0, 0, 1), with k_a = 0.2, k_d = 0.6, k_s = 0.5 and unit light intensities.

L = (0.5774, 0.5774, 0.5774), so N · L = **0.5774**. Reflection R = 2(N · L)N − L = (-0.5774, -0.5774, 0.5774), so R · V = **0.5774**. Ambient = **0.200**, diffuse = 0.6 × 0.5774 = **0.3464**. The specular term depends strongly on n:

| Shininess n | (R·V)ⁿ | Specular k_s·(R·V)ⁿ | Total I = ambient + diffuse + specular |
|---|---|---|---|
| 1 | 0.5774 | 0.2887 | 0.8351 |
| 10 | 0.0041 | 0.0021 | 0.5485 |
| 50 | 0.0000 | 0.0000 | 0.5464 |
| 200 | 0.0000 | 0.0000 | 0.5464 |

With n = 10 the total is **0.5485**. The viewer sits at an angle to the mirror direction (R · V = 0.5774, about 54.7°), so for large n the specular term vanishes and only the matte parts remain: highlights appear only near the mirror direction. In Blinn–Phong the halfway vector H = (0.3251, 0.3251, 0.8881) gives N · H = 0.8881, a different but related number (the exponents are chosen differently to give a similar highlight size).
:::

## 6.3 Surface shading methods

A polygon mesh approximates a smooth surface; the illumination model can be applied at different points.

- **Flat (constant) shading:** compute one intensity per polygon (using its normal) and fill the whole polygon with it. It is fastest but shows visible facets, and Mach-band effects exaggerate the edges.
- **Gouraud shading:** compute the intensity at each *vertex* using a **vertex normal** (the average of the normals of the polygons sharing the vertex), then **interpolate the intensity** linearly along edges and across the scan line. It removes facets cheaply but can miss highlights that fall *inside* a polygon and cause Mach bands.
- **Phong shading:** **interpolate the normal** across the polygon and evaluate the illumination model *at every pixel*. It gives accurate highlights and smooth specular reflection at a higher cost (Phong *shading* is the interpolation method; the Phong *model* is the lighting equation, and they are often confused).

::: example A highlight that Gouraud misses
An edge joins two vertices with normals N₁ = (-0.60, 0.00, 0.80) and N₂ = (0.60, 0, 0.80), the light and the viewer are both along +z (L = V = (0, 0, 1)), n = 50, and the coefficients are as before. At each vertex N · L = 0.8, but R · V = 2(0.8)² − 1 = 0.28, and 0.28⁵⁰ is practically zero, so the intensity at both ends is **0.6800** (ambient 0.2 + diffuse 0.48). Gouraud shading interpolates the intensities: the midpoint gets **0.6800**. Phong shading interpolates the normal first: the midpoint normal is (0.00, 0.00, 1.00), pointing straight at the viewer and the light, so N · L = 1, R · V = 1 and the intensity is 0.2 + 0.6 + 0.5 = **1.3000** (clamped to 1.0 on a display). Gouraud shading shows a flat, dim edge; Phong shading shows a bright specular highlight, because the highlight lies *between* the vertices where Gouraud never evaluates the lighting. The Gouraud value is 47.7% below the Phong value.
:::

| | Flat | Gouraud | Phong |
|---|---|---|---|
| Computed | Per polygon | Per vertex, intensity interpolated | Per pixel, normal interpolated |
| Cost | Lowest | Moderate | Highest |
| Facets visible | Yes | Reduced | No |
| Highlights | Poor | May be missed | Accurate |

## 6.4 Beyond local shading

**Texture mapping** wraps an image onto a surface using (u, v) coordinates stored at the vertices; **bump mapping** perturbs normals to imitate roughness; **environment maps** fake reflections. **Shadows** come from shadow maps (render depth from the light) or shadow volumes. **Transparency** blends colours with an alpha value: C = α·C_source + (1 − α)·C_background. **Ray tracing** follows rays from the eye through each pixel, finds the nearest hit and spawns **shadow**, **reflection** and **refraction** rays recursively, producing realistic mirrors and glass; **global illumination** (radiosity, path tracing) also accounts for light bouncing between surfaces. Real-time engines combine rasterisation with ray tracing hardware.

## Chapter summary

- The Z-buffer keeps the nearest depth per pixel and works for any surface; painter's algorithm sorts and overwrites; back-face culling removes rear faces.
- The Phong model is ambient + diffuse (N · L) + specular (R · V)ⁿ; Blinn–Phong uses N · H.
- Flat shading uses one intensity per polygon, Gouraud interpolates vertex intensities, Phong interpolates normals and lights every pixel.
- Gouraud shading can miss a highlight inside a polygon; Phong shading captures it.
- Textures, shadow maps, alpha blending and ray tracing add realism.

## Practice

1. Describe the Z-buffer algorithm and state its main memory cost for 1280 × 720 with 32-bit depth.
2. Why does the painter's algorithm fail for cyclically overlapping polygons?
3. Write the three terms of the Phong model and say what each represents.
4. Compute N · L for N = (0, 1, 0) and L = (0.6, 0.8, 0).
5. Compute the diffuse term for k_d = 0.5, I_d = 1 and N · L = 0.8.
6. What is the effect of increasing the shininess exponent n?
7. Differentiate Gouraud and Phong shading.
8. What is the halfway vector in Blinn–Phong?
9. Compute the colour blend with α = 0.25, source = 200 and background = 40.
10. How does ray tracing produce shadows?

::: note Answers and worked solutions
**1.** For each polygon pixel compare its depth with the stored depth and, if nearer, update colour and depth. Memory: 1280 × 720 × 4 bytes = **36,86,400 bytes** (3.5 MiB).
**2.** There is no consistent far-to-near order when polygons overlap in a cycle (A over B over C over A), so any painting order shows an error unless a polygon is split.
**3.** Ambient (constant background light), diffuse (matte reflection proportional to N · L), specular (shiny highlight proportional to (R · V)ⁿ).
**4.** 0 × 0.6 + 1 × 0.8 + 0 × 0 = **0.8**.
**5.** 0.5 × 1 × 0.8 = **0.40**.
**6.** The highlight becomes smaller and sharper (shinier surface).
**7.** Gouraud interpolates intensities computed at vertices; Phong interpolates normals and evaluates the lighting at each pixel.
**8.** H = (L + V)/|L + V|, the direction halfway between the light and the viewer; N · H replaces R · V.
**9.** 0.25 × 200 + 0.75 × 40 = 50 + 30 = **80**.
**10.** It casts a ray from the surface point towards the light; if the ray hits an object first, the point is in shadow and the light's contribution is omitted.
:::

# Computer Graphics and Animation — BCA 351 (Semester VI, 3 credits)

Display hardware and frame-buffer arithmetic, scan conversion (DDA, Bresenham, midpoint circle and ellipse, area filling), 2D homogeneous transformations and window-to-viewport mapping, line and polygon clipping (Cohen–Sutherland, Liang–Barsky, Sutherland–Hodgman), 3D transformations, projection and viewing, hidden-surface removal and Phong illumination and shading, Bézier and B-spline curves, surfaces and computer animation. 45 teaching hours (old TU CACS305 Computer Graphics and Animation has the same shape; the revised list numbers it BCA 351).

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction and Graphics Hardware | 5 |
| 2 | Scan Conversion: Lines, Circles, Ellipses and Area Filling | 8 |
| 3 | Two-Dimensional Transformations and Viewing | 7 |
| 4 | Clipping | 6 |
| 5 | Three-Dimensional Transformations, Projection and Viewing | 7 |
| 6 | Visible Surfaces, Illumination and Shading | 7 |
| 7 | Curves, Surfaces and Computer Animation | 5 |

## Verification

`bca/tools/check_graphics.py` implements each algorithm twice and asserts agreement: the incremental DDA pixels; Bresenham against the exact rounded line (all 11 pixels); the midpoint circle against the true radius (every pixel within 0.5) and its 56-pixel symmetric expansion; the midpoint ellipse against the ellipse equation; 2D and 3D matrices with numpy (pivot is a fixed point, rotations orthogonal with determinant 1, composite order effects); Cohen–Sutherland outcodes and clipped endpoints against Liang–Barsky on four lines; Sutherland–Hodgman area against a 0.05-grid integration; perspective points, homogeneous divide and back-face normals; the Z-buffer grid against a direct minimum; the Phong intensities and the Gouraud/Phong midpoint comparison; Bézier points by Bernstein and de Casteljau, end derivative by finite difference; the B-spline segment end values; easing, morphing and frame-size arithmetic; and the practice answers. The Bresenham and midpoint-circle programs in Unit 2 and the outcode program in Unit 4 are executed by `fill_script_outputs.py`; `--verify` demands that their printed pixel lists match the checker's independent lists (keys `out_*`).

## Source and honesty

No TU unit list for BCA 351 was retrieved in this session; the seven units follow the standard shape of an introductory graphics course (and the topics in the course brief) with a reconstructed 45-hour split. Algorithms follow Hearn and Baker, *Computer Graphics (C version)* and Foley et al.; prose is original. The Android/OpenGL API names are mentioned only in passing and no shader code is claimed as executed.

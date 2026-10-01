# Videos

Rendered explainer videos for the class 11 and 12 science stream.  Every one is
generated from code by the Manim pipeline in
[`tools/manim`](../../tools/manim/README.md) — the picture and the voice-over are
both cut from the same source, so nothing here is hand-edited.

| File | Subject | Length | Source chapter |
| --- | --- | --- | --- |
| `phy11-unit-01-physical-quantities.mp4` | Class 11 Physics · Unit 1 — Physical Quantities | 7:48 | [`notes/content/phy11/unit-01.md`](../../notes/content/phy11/unit-01.md) |

To rebuild any of them:

```sh
tools/manim/scripts/build.py tools/manim/videos/phy11_unit01.py PhysicalQuantities
```

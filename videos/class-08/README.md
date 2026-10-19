# Class 8 explainer videos

Every chapter of the Class 8 books, taught on screen: Manim draws every frame,
a Microsoft neural voice narrates, every sound and the music bed are synthesised
here (no licences, no attributions), and the real pixel Neby from the site and
the app guides the student.

Rendered at 1080p30, H.264, with a soft subtitle track in English.

| Book | Unit | Title | Length | Video |
|---|---|---|---|---|
| Science and Technology | 1 | Scientific Learning | 14:52 | [unit_01.mp4](sci8/unit_01.mp4) |

## Rebuilding one

```bash
cd tools/lessons
pip install "manim==0.19.2" "pillow<12" edge-tts scipy      # + ffmpeg, LaTeX, cairo/pango
bash ../../notes/pipeline/fonts/install.sh                   # Poppins, Inter, Noto
python3 build.py scripts/sci8/unit_01.py --preview           # 480p15, cheapest check
python3 build.py scripts/sci8/unit_01.py                     # 1080p30 master -> videos/
```

Each lesson script is the lesson plan as well as the film: narration lines are
the voice track, and everything inside `with self.say(...)` is padded to the
length of the spoken sentence, so picture and voice never drift.

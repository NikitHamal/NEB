# NEBians lesson videos

Explainer videos for every chapter of the NEBians books (classes 12, 11, 10 and 8),
built entirely in code: Manim draws every frame, Microsoft neural voices narrate,
every sound effect and the music bed are synthesised (no licences, no attributions),
and the real pixel Neby from the site and the app guides the student.

```
pip install "manim==0.19.2" "pillow<12" edge-tts scipy        # + ffmpeg, LaTeX, cairo/pango
bash ../../notes/pipeline/fonts/install.sh                     # Poppins, Inter, Noto; add Mukta for Nepali
python3 build.py scripts/phy12/unit_01.py --draft              # 720p24 preview
LESSON_ONLY=3,4 python3 build.py scripts/phy12/unit_01.py --draft   # only parts 3 and 4
python3 build.py scripts/phy12/unit_01.py                      # 1080p30 master -> videos/
python3 contact.py videos/class-12/phy12/unit_01.mp4 /tmp/sheet.png 24   # look at it
python3 frames.py scripts/phy12/unit_02.py 1,2                  # cheap check: parts 1-2 at 360p/3fps -> contact sheet
python3 prefetch.py scripts/phy12/unit_02.py                    # synthesise narration only
```

Narration is already synthesised and committed: `.cache/tts/<hash>.mp3` (+ `.json` duration and
subtitle cues, `.srt`). A render on a fresh machine needs no network for the voice; the trimmed
`.wav` files are rebuilt from the mp3s automatically (they are gitignored). Change a narration line
and only that line is re-synthesised.

## Layout

| Path | What |
|---|---|
| `kit/lesson.py` | `Lesson` base scene: narration-timed animation (`with self.say(...)`), title card, roadmap, section wipes, HUD + progress bar, callouts, exam tips, pause-and-think quiz with countdown, recap, outro, subtitle export |
| `kit/neby.py` | pixel Neby, played frame-accurately from `backend_python/web/static/web/img/neby/<look>/<state>.png` |
| `kit/voice.py` | Microsoft neural TTS (`en-US-AndrewMultilingualNeural`, `ne-NP-HemkalaNeural`), cached by text hash, with sentence timings for subtitles |
| `kit/sfx.py` | synthesised whoosh, pop, tick, bell, correct chime, riser, impact, shimmer, and the ambient music bed |
| `kit/text.py` | `T()` picks Mukta for Devanagari and Inter/Poppins for Latin; `para()` wraps; `M()` is MathTex; `ne_num()` gives Nepali digits |
| `build.py` | render -> duck music under voice -> loudness -I 16 LUFS -> mux soft subtitles -> `videos/class-NN/<book>/unit_NN.mp4` + `.srt` + `.jpg` + `videos/index.json` |
| `scripts/<book>/unit_NN.py` | one lesson per chapter, written against `notes/content/<book>/unit-NN.md` |

## Rules

- Every lesson follows its chapter's syllabus sections in order and its numbers come
  from the chapter's worked examples (recomputed).
- Nepali-medium subjects (`nep`, `soc`, `health`) are Nepali all the way through: narration,
  on-screen text, numerals, quiz letters (क ख ग घ). Neby wears the topi and greets with
  namaste (the `wave` strip has a Latin "hi" bubble, so it is never used there).
- Narration drives timing: animations inside `with self.say(text):` are padded to the
  length of the spoken line, so picture and voice never drift.

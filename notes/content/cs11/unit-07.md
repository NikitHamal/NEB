---
subject: Computer Science
grade: 11
unit: 7
title: Multimedia
hours: 6
---

A page of a printed book can only carry text and pictures. A computer can carry
text, pictures, recorded sound, moving video and animation **at the same time**,
and it can let you choose what to look at next. That combination is what we call
multimedia, and it is the reason a computer can teach, entertain, advertise and
diagnose in ways that no earlier medium could.

::: key What the examiner wants from this unit
This is a short, definition-heavy unit and the marks are easy to collect. Learn
the **definition of multimedia** and the **five components** in order, with two
or three file formats and one piece of software for each. Be ready to explain
**linear versus non-linear** multimedia, **raster versus vector** graphics, and
to list **applications** with one sentence of explanation each — a bare list
rarely earns full marks.
:::

## 7.1 Introduction to multimedia

::: definition Multimedia
**Multimedia** is the integrated use of more than one medium — text, graphics,
audio, video and animation — presented and controlled by a computer, usually
with some degree of **interactivity** for the user.
:::

The word itself gives the definition away: *multi* means many and *media* means
the means of communicating. The key words in the definition are **integrated**
(the media work together in one presentation, not side by side), **computer
controlled** and **interactive**.

A textbook with photographs is not multimedia — it has two media but no computer
and no interaction. A film is not multimedia either: it combines pictures and
sound, but you cannot change what happens next. A website with text, photographs,
a video and buttons that let you choose a topic **is** multimedia.

**Characteristics of multimedia:**

- It combines **two or more** media in one presentation.
- It is **digital** — every medium is stored as numbers, so all of them can be
  edited, copied and transmitted by the same machine.
- It is **integrated**: the media are synchronised, so narration matches the
  picture on screen.
- It is usually **interactive**: the user controls the pace and the path through
  the content.
- It needs **large storage** and a **fast processor**, because sound and video
  carry far more data than text.

::: definition Linear and non-linear multimedia
**Linear (non-interactive) multimedia** runs from beginning to end in a fixed
order, with no control by the user — a cinema film, a slideshow that plays
automatically, a television advertisement.

**Non-linear (interactive) multimedia** lets the user choose the order and the
pace by clicking menus, buttons or links — a website, a computer game, an
e-learning CD, an information kiosk.
:::

A related idea is **hypermedia**: non-linear multimedia in which the pieces are
joined by **hyperlinks**, so that clicking a word or a picture jumps to related
content. The World Wide Web is the largest hypermedia system ever built.

**What a multimedia computer needs.** On the hardware side: a fast processor,
plenty of RAM, a good graphics card (GPU), a sound card with speakers or
headphones, a high-resolution monitor, large secondary storage, and capture
devices such as a microphone, a scanner, a digital camera and a webcam. On the
software side: media players, an image editor, a sound editor, a video editor,
an animation tool and an authoring tool that ties them all together.

| Advantages | Disadvantages |
|---|---|
| Uses sight and sound together, so people understand and remember more | Needs expensive hardware and software |
| Makes abstract ideas visible — a beating heart, a running engine | Files are very large; sharing needs fast internet |
| The user controls the pace, so learning is self-directed | Producing good content takes skill, time and money |
| One copy serves any number of students, anywhere | Too much animation and sound distracts from the message |
| Attracts and holds attention in advertising and teaching | Can encourage passive watching instead of active thinking |

## 7.2 Components of multimedia

The five components are **text, graphics, audio, video and animation**. Learn
them in that order: it is the order the syllabus uses, and it runs from the
smallest files to the largest.

```figure caption="The five components of multimedia. The computer integrates them into one presentation, and interactivity — the user's control over what happens next — is what turns that presentation into multimedia rather than a film."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
fig, ax = plt.subplots(figsize=(4.9, 3.15))

cx, cy, R = 0.0, 0.0, 1.32
ax.add_patch(Circle((cx, cy), 0.80, fc="#eef4fa", ec=ACCENT, lw=1.4))
ax.text(cx, cy + 0.10, "MULTIMEDIA", ha="center", va="center", fontsize=8.0,
        color=INK, fontweight="bold")
ax.text(cx, cy - 0.20, "integrated by\nthe computer", ha="center", va="center",
        fontsize=6.4, color=MUTED)

items = [("TEXT", "letters, numbers,\nsymbols", 90, "#fdf6ea", "#c8862a"),
         ("GRAPHICS", "still pictures:\nraster and vector", 18, "#eaf3ee", "#2e8b57"),
         ("AUDIO", "speech, music,\nsound effects", -54, "#fdf1ef", "#A8271F"),
         ("VIDEO", "recorded moving\npictures with sound", -126, "#eef4fa", ACCENT),
         ("ANIMATION", "drawn images made\nto appear to move", 162, "#f3ecf7", "#6a4c93")]

for name, sub, ang, fc, ec in items:
    a = np.radians(ang)
    x, y = cx + R * np.cos(a) * 1.62, cy + R * np.sin(a) * 1.10
    ax.add_patch(FancyBboxPatch((x - 0.82, y - 0.30), 1.64, 0.60,
                 boxstyle="round,pad=0.03,rounding_size=0.08",
                 fc=fc, ec=ec, lw=1.15))
    ax.text(x, y + 0.13, name, ha="center", va="center", fontsize=7.2,
            color=ec, fontweight="bold")
    ax.text(x, y - 0.13, sub, ha="center", va="center", fontsize=5.7, color=INK)
    sx, sy = cx + 0.80 * np.cos(a), cy + 0.80 * np.sin(a)
    ex, ey = x - 0.80 * np.cos(a), y - 0.28 * np.sin(a)
    ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                arrowprops=dict(arrowstyle="-", color=ec, lw=1.0))

ax.set_xlim(-3.05, 3.05); ax.set_ylim(-1.95, 1.95)
ax.set_aspect("equal"); ax.axis("off")
```

### Text

Text is the oldest and **smallest** component — a page of plain text is a few
kilobytes. It carries precise meaning that a picture cannot: a name, a date, a
price, an instruction. In a multimedia product, text appears as headings, body
text, captions, menu labels and buttons.

- A **font** (typeface) is a complete set of characters in one design — Arial,
  Times New Roman, Preeti. Its **size** is measured in **points** (1 point = 1/72
  inch), and its **style** may be regular, bold, italic or underlined.
- **Static text** simply sits on the screen; **hypertext** is text that links to
  other content when clicked.
- Common formats: `.txt` (plain text, no formatting), `.rtf` (rich text),
  `.docx`, `.pdf`, `.html`.
- Software: Notepad, MS Word, LibreOffice Writer.

### Graphics

Graphics are **still pictures** — photographs, drawings, diagrams, logos, charts.
They are the fastest way to show what something *looks* like. There are two
fundamentally different ways a computer can store a picture, and the difference
is examined nearly every year.

::: definition Raster and vector graphics
A **raster (bitmap)** image is stored as a **grid of pixels**, each with its own
colour value. Enlarging it stretches the pixels, so the image becomes blurred or
blocky — it is **resolution dependent**.

A **vector** image is stored as **mathematical descriptions of shapes** — lines,
curves, circles with their coordinates, thicknesses and fills. The computer
redraws the shapes at whatever size is asked for, so the image stays perfectly
sharp — it is **resolution independent**.
:::

```figure caption="Raster against vector. The raster picture is a grid of coloured squares, so enlarging it enlarges the squares; the vector picture is a stored instruction — circle, centre, radius — so the computer simply redraws it larger."
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.1, 2.45))

def pixel_circle(ox, oy, n, size):
    step = size / n
    for i in range(n):
        for j in range(n):
            px = ox + (i + 0.5) * step
            py = oy + (j + 0.5) * step
            d = np.hypot(px - (ox + size / 2), py - (oy + size / 2))
            fc = ACCENT if d < size * 0.36 else "#ffffff"
            ax.add_patch(Rectangle((ox + i * step, oy + j * step), step, step,
                                   fc=fc, ec="#cfd6de", lw=0.35))

ax.text(0.90, 2.30, "RASTER  (pixels)", ha="center", fontsize=7.6,
        color=INK, fontweight="bold")
pixel_circle(0.30, 1.05, 10, 1.20)
ax.text(0.90, 0.88, "stored as 100 colour values", ha="center", va="top",
        fontsize=6.0, color=MUTED)
pixel_circle(2.05, 0.95, 10, 1.40)
ax.text(2.75, 0.78, "enlarged: the squares\nshow — it goes blocky",
        ha="center", va="top", fontsize=6.0, color="#A8271F")
ax.annotate("", xy=(2.00, 1.65), xytext=(1.62, 1.65),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0,
                            mutation_scale=9))

ax.text(5.55, 2.30, "VECTOR  (shapes)", ha="center", fontsize=7.6,
        color=INK, fontweight="bold")
ax.add_patch(Rectangle((4.35, 1.05), 1.20, 1.20, fc="#ffffff", ec="#cfd6de", lw=0.6))
ax.add_patch(Circle((4.95, 1.65), 0.43, fc=ACCENT, ec="none"))
ax.text(4.95, 0.88, 'circle(cx, cy, r=0.43)', ha="center", va="top",
        fontsize=5.8, color=MUTED, family="DejaVu Sans Mono")
ax.add_patch(Rectangle((6.10, 0.95), 1.40, 1.40, fc="#ffffff", ec="#cfd6de", lw=0.6))
ax.add_patch(Circle((6.80, 1.65), 0.50, fc=ACCENT, ec="none"))
ax.text(6.80, 0.78, "enlarged: redrawn,\nso the edge stays smooth",
        ha="center", va="top", fontsize=6.0, color="#2e8b57")
ax.annotate("", xy=(6.05, 1.65), xytext=(5.67, 1.65),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0,
                            mutation_scale=9))
ax.plot([3.80, 3.80], [0.30, 2.45], color=GRID, lw=0.9, ls=(0, (4, 3)))
ax.set_xlim(0.10, 7.70); ax.set_ylim(0.20, 2.55)
ax.set_aspect("equal"); ax.axis("off")
```

| | Raster | Vector |
|---|---|---|
| Made of | pixels | mathematical shapes |
| On enlarging | blurred, blocky | stays sharp |
| File size | large, grows with resolution | small, grows with complexity |
| Best for | photographs, scanned images | logos, icons, maps, technical drawings |
| Formats | JPEG, PNG, GIF, BMP, TIFF | SVG, AI, EPS, CDR |
| Software | Adobe Photoshop, GIMP, MS Paint | Adobe Illustrator, CorelDRAW, Inkscape |

Three ideas describe any raster image. **Resolution** is the number of pixels,
written as width × height (1920 × 1080). **Colour depth** (or bit depth) is the
number of bits used per pixel: 1 bit gives 2 colours, 8 bits give 256, and
**24-bit "true colour"** gives 2²⁴ ≈ 16.7 million. **Compression** shrinks the
file, and is either **lossy** (JPEG — throws away detail the eye is unlikely to
miss, so the file is small but quality falls each time it is re-saved) or
**lossless** (PNG, GIF — nothing is discarded and the original can be rebuilt
exactly).

::: example Worked example 7.1 — how big is an uncompressed image?
**Problem.** Find the uncompressed size of a 1024 × 768 photograph stored in
24-bit true colour, in megabytes.

**Solution.** Each pixel takes 24 bits = 3 bytes.

$$ \text{pixels} = 1024 \times 768 = 786{,}432 $$
$$ \text{bytes} = 786{,}432 \times 3 = 2{,}359{,}296 $$
$$ \text{MB} = \frac{2{,}359{,}296}{1024 \times 1024} = 2.25 $$

So **2.25 MB** for one picture. A JPEG of the same photograph is typically
200–400 KB, roughly a tenth of the size — which is exactly why lossy compression
exists, and why raw video is impossible to stream without it.
:::

### Audio

Audio is sound in digital form — narration, music, sound effects, warning beeps.
Sound reaches a microphone as a continuous (analogue) wave, and the computer
converts it into numbers by **sampling**: measuring the height of the wave many
thousands of times a second and storing each measurement.

- **Sampling rate** is how many measurements are taken per second, in hertz. CD
  quality is **44,100 Hz** (44.1 kHz).
- **Bit depth** is how precisely each measurement is stored — 16 bits for CD
  audio.
- **Channels**: **mono** is one channel, **stereo** is two, surround sound more.

Higher values in any of these give better sound and a bigger file.

```photo id="cs11/audacity" caption="A recorded voice open in Audacity, a free sound editor. The blue shape is the waveform: the horizontal axis is time and the vertical axis is the loudness of the sample at that instant, so silences show as a thin line and loud syllables as tall bursts. The track is labelled Mono, 44100 Hz, 32-bit float — the sampling rate and bit depth at which it was recorded." width="96"
crop 0.0 0.51 1.0 1.0
call 0.155 0.085 0.050 0.300 "track panel"
call 0.480 0.085 0.380 0.330 "waveform — loudness over time"
call 0.790 0.085 0.700 0.600 "timeline in seconds"
```

- Formats: **MP3** (lossy, small, universal), **WAV** (uncompressed, large, full
  quality), **AAC**, **OGG**, **WMA**, **MIDI** (not a recording at all — a list
  of instructions saying which note to play on which instrument, so the files are
  tiny).
- Software: Audacity, Adobe Audition, Sound Forge.

::: example Worked example 7.2 — the size of a recording
**Problem.** A song lasts 3 minutes and is recorded in **stereo** at 44,100 Hz
with a bit depth of 16 bits. Find its uncompressed size in megabytes, and say
roughly how large the MP3 would be.

**Solution.** Work out the bytes stored every second, then multiply by the
duration.

$$ \text{bytes per second} = 44{,}100 \times \frac{16}{8} \times 2 = 176{,}400 $$
$$ \text{seconds} = 3 \times 60 = 180 $$
$$ \text{bytes} = 176{,}400 \times 180 = 31{,}752{,}000 $$
$$ \text{MB} = \frac{31{,}752{,}000}{1024 \times 1024} = 30.3 $$

So about **30.3 MB** as a WAV file. The 2 in the first line is the number of
channels — halve the answer and you have the mono figure. An MP3 of the same song
at 128 kbps stores 128,000 ÷ 8 = 16,000 bytes per second, giving 2,880,000 bytes
≈ **2.75 MB**, about **one eleventh** of the size. That saving is why MP3
displaced the CD.
:::

### Video

Video is a **sequence of still images (frames) captured from the real world and
played back fast enough to look continuous**, almost always with a synchronised
sound track. The number of frames shown per second is the **frame rate**; 24
frames per second is the cinema standard, and 25 or 30 fps is normal for
television and the web.

Video is the **largest** of the five components. One second of uncompressed
1920 × 1080 true-colour video at 30 fps would be about 178 MB, so video is always
compressed, by codecs such as H.264 and H.265.

::: definition Codec
A **codec** (coder–decoder) is the software that compresses a video or audio
stream for storage and decompresses it for playback. The **container** format —
`.mp4`, `.avi`, `.mkv` — is the wrapper that holds the compressed video, the
audio and the subtitles together; it is not the same thing as the codec inside.
:::

```photo id="cs11/kdenlive" caption="The timeline of Kdenlive, a free video editor. Editing means cutting clips and arranging them along the timeline; the timecode ruler across the top counts hours, minutes, seconds and frames." width="98"
crop 0.0 0.095 1.0 0.373
mark 0.329 0.879 "1"
mark 0.620 0.820 "2"
mark 0.440 0.648 "3"
mark 0.440 0.417 "4"
mark 0.620 0.186 "5"
key 1 Playhead — the vertical line marking the frame currently shown in the preview window
key 2 V2, an empty second video track; tracks are stacked, and an upper track covers what is beneath it
key 3 V1, the video track holding the clips of the film, each clip a separate rectangle that can be trimmed or moved
key 4 A1, the matching audio track — the green blocks are the sound waveforms belonging to those clips
key 5 A2, a spare audio track, free for background music or a voice-over
```

- Formats: **MP4** (the default choice today), **AVI**, **MKV**, **MOV**,
  **WMV**, **FLV**, **WebM**.
- Software: Adobe Premiere Pro, Kdenlive, OpenShot, Windows Video Editor.

### Animation

::: definition Animation
**Animation** is the process of creating the illusion of movement by displaying a
rapid sequence of still images that differ slightly from one another. The images
are **drawn or generated**, not captured from the real world — that is what
separates animation from video.
:::

Animation works because of **persistence of vision**: the human eye retains an
image for about a sixteenth of a second after it disappears, so images shown
faster than about 16 per second blend into continuous motion.

```photo id="cs11/horse-in-motion" caption="Eadweard Muybridge's 'The Horse in Motion', 1878 — the mare Sallie Gardner photographed by a row of cameras on the Palo Alto track. The plate's own note records that the negatives were taken about a twenty-fifth of a second apart. Played in sequence the twelve frames show the horse galloping; shown one at a time they are twelve still pictures. This is the whole principle of both video and animation." width="92"
crop 0.0 0.21 1.0 1.0
```

Kinds of animation:

- **Cel or frame-by-frame animation** — every frame is drawn separately, the
  traditional cartoon method.
- **Tweening (in-betweening)** — the artist draws only the first and last frames
  (the **key frames**) and the software calculates all the frames between them.
- **Path animation** — an object is moved along a drawn path.
- **Morphing** — one image is gradually transformed into another.
- **2D animation** works in height and width only; **3D animation** builds
  objects in a three-dimensional space with depth, lighting and camera angles,
  and is what modern animated films use.

Formats: **GIF** (short looping animations, 256 colours), **SWF** (the old Flash
format, now obsolete), **SVG** with CSS or JavaScript, **MP4** for rendered 3D
work. Software: Adobe Animate, Blender, Synfig Studio, Autodesk Maya.

::: caution Video and animation are not the same thing
Both show a fast sequence of frames, and both may be stored in an MP4 file, so
students mix them up. The difference is **where the frames come from**: video
frames are **captured** from reality by a camera; animation frames are **created**
by an artist or computed by software. A recording of a football match is video;
a cartoon of a football match is animation.
:::

## 7.3 Applications of multimedia

**Education and training.** Computer-assisted learning packages, e-learning
websites, virtual laboratories and interactive encyclopedias. A simulated
chemistry experiment can be repeated without cost or danger, and a video of a
heart beating teaches anatomy better than a still diagram. Flight and driving
simulators train pilots and drivers without risking an aircraft.

**Entertainment.** Computer and mobile games, animated films, streaming services,
digital music. This is the industry that has driven most multimedia hardware
development, because games demand the fastest graphics processors.

**Business and advertising.** Multimedia presentations to clients, video
conferencing, animated television and web advertisements, product demonstrations
and virtual showrooms where a customer can rotate a product on screen.

**Public information and kiosks.** Touch-screen kiosks at airports, museums,
banks and hospitals; digital notice boards; government information portals.
Because they are interactive, a visitor finds just the item wanted instead of
reading a whole board.

**Medicine.** Scanned images from MRI and CT machines assembled into
three-dimensional views; surgical simulators on which surgeons practise; patient
education videos; telemedicine, in which a specialist in Kathmandu examines
images and video sent from a district hospital.

**Engineering and science.** Computer-aided design (CAD) of buildings and
machines, three-dimensional walk-throughs of a building before it is built,
scientific visualisation of weather and earthquake data.

**Journalism and publishing.** Online newspapers combining text, photographs,
video and interactive graphs; e-books with embedded audio; digital archives.

**Arts and entertainment production.** Digital photography and photo editing,
music production, film special effects and computer-generated imagery (CGI).

::: example Worked example 7.3 — choosing the right component
**Problem.** A school is making an interactive CD about Nepal's national parks.
For each requirement below, say which component of multimedia should be used and
in which file format, and give the reason.

(i) The scientific name of each animal. (ii) A map of the park that must stay
sharp when a visitor zooms in. (iii) The call of a bird. (iv) A ranger
explaining how the park is patrolled. (v) A diagram showing how a river changes
course over fifty years.

**Solution.**

(i) **Text**, stored in the page itself or as `.html` — a name must be exact and
readable, which only text guarantees, and it costs almost no storage.

(ii) **Vector graphics**, as **SVG** — a map is made of lines and areas, and a
vector map is redrawn at every zoom level, so it never goes blocky. A JPEG map
would blur as soon as it was enlarged.

(iii) **Audio**, as **MP3** — a real recorded sound, compressed so that a whole
library of calls fits on the disc. WAV would be truer but roughly ten times
larger.

(iv) **Video**, as **MP4** — a person speaking must be captured from reality,
and the picture must stay synchronised with the sound. H.264 in an MP4 container
is playable on every device.

(v) **Animation**, as an animated **GIF** or a short **MP4** — the fifty-year
change was never filmed, so the frames must be drawn or computed. Tweening
between a key frame for 1975 and one for 2025 produces the in-between years
automatically.
:::

## Chapter summary

- **Multimedia** is the computer-controlled, integrated use of more than one
  medium — text, graphics, audio, video and animation — usually with
  interactivity.
- **Linear** multimedia runs in a fixed order with no user control (a film);
  **non-linear** multimedia lets the user choose the path (a website, a game).
  **Hypermedia** is non-linear multimedia joined by hyperlinks.
- **Text** is the smallest component and carries exact meaning; fonts are
  measured in **points** (1 point = 1/72 inch); formats `.txt`, `.rtf`, `.docx`,
  `.pdf`, `.html`.
- **Graphics** are still pictures. **Raster** images are grids of pixels, are
  resolution dependent and go blocky when enlarged (JPEG, PNG, GIF, BMP);
  **vector** images store shapes as mathematics, are resolution independent and
  stay sharp (SVG, AI, EPS, CDR).
- Image size depends on **resolution** (pixels), **colour depth** (24-bit true
  colour = 16.7 million colours) and **compression** — **lossy** (JPEG) discards
  detail, **lossless** (PNG, GIF) does not.
- **Audio** is digitised by **sampling**: CD quality is 44,100 Hz at 16 bits.
  MP3 is lossy and small, WAV is uncompressed and large, MIDI stores instructions
  rather than sound.
- **Video** is captured frames plus synchronised sound, measured in **frames per
  second** (24 fps cinema, 25–30 fps television). A **codec** compresses it;
  a **container** (`.mp4`, `.avi`, `.mkv`) holds the parts together.
- **Animation** is drawn or computed frames, not captured ones, and works by
  **persistence of vision**. Methods: frame-by-frame, **tweening** between key
  frames, path animation and morphing; 2D against 3D.
- Applications: education and training, entertainment, business and advertising,
  public information kiosks, medicine, engineering, journalism and the arts.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which one is **not** a component of multimedia? <span class="marks">[1]</span>
   (a) Text (b) Animation (c) Compiler (d) Audio
2. A cinema film that cannot be controlled by the viewer is an example of <span class="marks">[1]</span>
   (a) linear multimedia (b) non-linear multimedia (c) hypermedia (d) interactive media
3. Which type of graphic stays sharp when it is enlarged? <span class="marks">[1]</span>
   (a) bitmap (b) raster (c) vector (d) JPEG
4. The standard sampling rate of CD-quality audio is <span class="marks">[1]</span>
   (a) 8,000 Hz (b) 22,050 Hz (c) 44,100 Hz (d) 96,000 Hz
5. The number of frames displayed per second in a video is called its <span class="marks">[1]</span>
   (a) resolution (b) frame rate (c) bit depth (d) sampling rate
6. Which file format uses **lossy** compression? <span class="marks">[1]</span>
   (a) PNG (b) BMP (c) JPEG (d) GIF
7. Creating the frames between two key frames automatically is called <span class="marks">[1]</span>
   (a) morphing (b) tweening (c) rendering (d) sampling
8. Animation is possible because of <span class="marks">[1]</span>
   (a) persistence of vision (b) refraction (c) sampling (d) compression
9. In 24-bit true colour, the number of colours available is about <span class="marks">[1]</span>
   (a) 256 (b) 65,536 (c) 16.7 million (d) 4.3 billion

::: note Answers to Group A
**1.** (c) — a compiler is a translator program, not a medium.
**2.** (a) — linear multimedia runs start to finish with no user control.
**3.** (c) — vector images are redrawn from stored shapes.
**4.** (c) — 44.1 kHz at 16 bits is CD quality.
**5.** (b) — frames per second.
**6.** (c) — JPEG discards detail the eye is unlikely to notice.
**7.** (b) — tweening, short for in-betweening.
**8.** (a) — the eye holds an image for about 1/16 of a second.
**9.** (c) — 2²⁴ ≈ 16.7 million.
:::

**Group B — Short answer (5 marks each)**

1. Define multimedia. Explain any four of its characteristics. <span class="marks">[5]</span>
2. Differentiate between linear and non-linear multimedia with two examples of each. <span class="marks">[5]</span>
3. Differentiate between raster and vector graphics with any five points. <span class="marks">[5]</span>
4. What is animation? Explain any four types of animation. <span class="marks">[5]</span>
5. Explain the audio and video components of multimedia, naming three file formats and one piece of software for each. <span class="marks">[5]</span>
6. Calculate the uncompressed size, in megabytes, of a 1600 × 1200 image stored in 24-bit colour. Explain why compression is necessary. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Multimedia is the integrated, computer-controlled use of more than one
medium — text, graphics, audio, video and animation — usually with
interactivity. Characteristics: it combines two or more media; everything is
digital; the media are integrated and synchronised; it is normally interactive,
with the user choosing the path and the pace; and it demands large storage and a
fast processor.

**2.** Linear multimedia plays from beginning to end in a fixed order with no
user control — examples: a cinema film, an automatically playing slideshow.
Non-linear multimedia lets the user choose what to see next through menus,
buttons and links — examples: a website, a computer game. Linear content is
easier and cheaper to produce; non-linear content holds attention longer and
suits self-paced learning.

**3.** See the comparison table in §7.2: made of pixels against mathematical
shapes; blurs when enlarged against stays sharp; large file size against small;
suits photographs against suits logos and maps; JPEG/PNG/GIF/BMP against
SVG/AI/EPS/CDR; Photoshop or GIMP against Illustrator or Inkscape.

**4.** Animation is the illusion of movement created by displaying a rapid
sequence of still images that differ slightly, the images being drawn or computed
rather than captured. Types: **frame-by-frame (cel)**, where every frame is drawn
separately; **tweening**, where only the key frames are drawn and the software
fills in the rest; **path animation**, where an object follows a drawn path; and
**morphing**, where one image is gradually transformed into another.

**5.** Audio is digitised sound — narration, music and effects — produced by
sampling an analogue wave, typically at 44,100 Hz and 16 bits. Formats: MP3
(lossy, small), WAV (uncompressed), MIDI (instructions, not a recording).
Software: Audacity. Video is a sequence of frames captured from the real world
with synchronised sound, measured in frames per second and always compressed by a
codec. Formats: MP4, AVI, MKV. Software: Adobe Premiere Pro (or Kdenlive).

**6.** 1600 × 1200 = 1,920,000 pixels. At 24 bits = 3 bytes per pixel, that is
5,760,000 bytes, and 5,760,000 ÷ (1024 × 1024) = **5.49 MB**. Compression is
necessary because uncompressed images and especially video are far too large to
store in quantity or send over a network — one second of uncompressed 1080p video
at 30 fps is about 178 MB, which no ordinary internet connection could stream.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define multimedia and explain the five components with one example of each.
   <span class="marks">[5]</span>
   (b) Explain any three hardware requirements and any three software
   requirements of a multimedia computer. <span class="marks">[3]</span>
2. (a) Explain any six applications of multimedia, with one sentence on how
   multimedia helps in each. <span class="marks">[6]</span>
   (b) State any two advantages and any two disadvantages of multimedia.
   <span class="marks">[2]</span>

::: note Answers to Group C
**1. (a)** The definition is in §7.1. **Text** — the caption naming a photograph;
smallest component, carries exact meaning. **Graphics** — a photograph of Mount
Everest or a vector map of a national park; still pictures, raster or vector.
**Audio** — a recorded narration or a bird call, digitised by sampling.
**Video** — a filmed interview; frames captured from reality with synchronised
sound. **Animation** — a cartoon showing how a river changed course; frames drawn
or computed rather than captured.

**1. (b)** Hardware: a fast processor to decode compressed video in real time; a
graphics card (GPU) to render images and 3D scenes; a sound card with speakers,
and large secondary storage because media files are huge; capture devices such as
a microphone, scanner, webcam or digital camera. Software: an image editor such
as GIMP; a sound editor such as Audacity; a video editor such as Kdenlive; media
players and an authoring tool to combine everything.

**2. (a)** *Education* — simulations and videos make dangerous or invisible
processes safe to watch and repeatable. *Entertainment* — games and animated
films are built entirely from multimedia. *Business and advertising* — animated
advertisements and virtual showrooms let a customer examine a product before
buying. *Public information kiosks* — a touch screen at an airport or museum lets
each visitor find only the item wanted. *Medicine* — MRI and CT slices are
assembled into 3D views, and surgeons rehearse on simulators. *Engineering* — CAD
models and 3D walk-throughs show a building before it is built. *Journalism* —
online news combines text, photographs, video and interactive graphs in one
story.

**2. (b)** Advantages: it uses sight and sound together, so people understand and
remember more; the user controls the pace, which suits self-directed learning.
Disadvantages: it needs expensive hardware, software and skill to produce; the
files are very large, so sharing them needs fast internet and plenty of storage.
:::

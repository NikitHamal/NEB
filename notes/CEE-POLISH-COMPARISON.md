# CEE figure & photograph polish — comparison

Record of the polish pass applied to the six CEE entrance books on 1 Nov 2026, and the evidence
behind it. Kept in the repo so the decision is reviewable later.

## The two candidates

Two agents were asked to do the same job.

| | `_work/` (first agent) | `public/cee/` (second agent) |
|---|---|---|
| Form | 3 Python scripts meant to run inside a `notes/` tree | a finished content package |
| `add_photos_cee.py` | asks for **91** photo ids, **79** registered — dies on line 1 | 84 chapters already carrying **119** photo blocks |
| `polish_figures_cee.py` | 3 targeted label fixes | 6 figures redrawn; superseded |
| `prepare.py` | packs books into a reader app | `manifest.json` already does this |
| Captions | borrowed from other books; **27 registered assets have none** | all 119 written, with overlay directives |
| Overlay keys | a handful | on every numbered diagram (`key`/`mark`/`crop`/`call`) |
| Images | none sourced for the 12 gaps | 20 new Commons images sourced and credited |

The first agent's script cannot run at all:

```
AssertionError: asset not registered: cee-zoo/digestive-en
```

**The decisive difference is the overlay keys.** Real anatomical diagrams arrive with numbers
printed on them — `bio12/alimentary` carries 1–30 — and dropping one into a textbook without a key
leaves a student staring at floating numerals. The second agent wrote `key 1 Mouth (oral cavity)`,
`key 2 Palate`… onto each one, so the numbers are explained in the book. The first agent's script
had no mechanism for that, which is also why substituting library images was rejected while
evaluating it: `bio12/eye` and `bio12/alimentary` are excellent diagrams whose numbers would have
been unkeyed.

## The six books, before and after

Baseline is the set built in `6eb95c17`.

| Book | Pages | Size | Photographs |
|---|---|---|---|
| Physics | 429 → **437** | 12.63 → 13.69 MB | 0 → **12** |
| Chemistry | 398 → **409** | 6.77 → 8.28 MB | 0 → **17** |
| Zoology | 291 → **317** | 3.77 → 8.21 MB | 1 → **46** |
| Botany | 286 → **312** | 4.51 → 10.20 MB | 4 → **44** |
| Mental Agility Test | 85 → 85 | 1.24 → 1.24 MB | 0 → 0 |
| Model Papers & Mock Tests | 127 → 127 | 1.29 → 1.29 MB | 0 → 0 |
| **Total** | **1616 → 1687** (+71) | **30.21 → 42.91 MB** (+12.7) | **5 → 119** (+114) |

Mental Agility and Model Papers are untouched by design — reasoning drills and exam papers have
nothing to photograph.

## Exactly what changed

**Nothing but figures and photographs.** Verified, not assumed.

- **0 prose changes.** The 37 chapters whose text differs do so only by blank-line separators
  inserted between blocks.
- **0 MCQ changes.** `notes/tools/mcqcheck.py`: 4,837 / 4,837 keyed, key spread a 1231 · b 1223 ·
  c 1218 · d 1165 — identical to the pre-polish baseline.
- **Figure blocks: 312 → 305.** 299 byte-identical, 6 redrawn, 7 deleted.

### Seven drawn figures deleted, replaced by real labelled images

| Chapter | Was (drawn) | Now (real) |
|---|---|---|
| `cee-bot/unit-02` | "Two classic viruses" — drawn T4 + TMV | `bio11/t4`, `bio11/tmv` micrographs |
| `cee-zoo/unit-05` | alimentary canal, numbers keyed on the right | `bio12/alimentary` + a `key 1…11` overlay |
| `cee-zoo/unit-06` | respiratory tract, drawn | `cee-zoo/respiratory-system` |
| `cee-zoo/unit-08` | urinary system, drawn | `bio12/urinary-system` |
| `cee-zoo/unit-08` | kidney longitudinal section, drawn | `bio12/kidney-gray` + `key 1…4` overlay |
| `cee-zoo/unit-08` | juxtamedullary nephron, drawn | `bio12/nephron-numbered` + `key 1…4` overlay |
| `cee-zoo/unit-09` | eye horizontal section, drawn | `bio12/eye` + `key 1…4` overlay |

In every case the replacement is a real, correctly licensed image *and* the numbers printed on it
are keyed in the book, so nothing is lost relative to the drawn original.

### Six drawn figures redrawn in place

`cee-bot/unit-07` prokaryotic cell · `cee-bot/unit-08` DNA ladder · `cee-bot/unit-08` replication
fork · `cee-bot/unit-11` cell in three baths (proper ψ symbols) · `cee-zoo/unit-02` coelom types ·
`cee-zoo/unit-08` counter-current multiplier.

### The 19 images that had to be sourced

The package's markdown and credits were complete, but the image **bytes** were not. All 19 were
fetched from Wikimedia Commons at 1800 px and verified readable:

| id | subject | licence |
|---|---|---|
| `cee-bot/azolla` | *Azolla caroliniana* | CC BY-SA 4.0 |
| `cee-bot/marchantia` | *Marchantia polymorpha* | CC BY 4.0 |
| `cee-bot/mucor` | *Mucor* sporangia | CC BY-SA 4.0 |
| `cee-bot/mustard` | *Brassica juncea* raceme | CC BY-SA 3.0 |
| `cee-bot/neem` | *Azadirachta indica* | CC BY-SA 3.0 |
| `cee-bot/pea-flower` | garden pea in flower | CC BY-SA 4.0 |
| `cee-bot/potato-flower` | *Solanum tuberosum* flowers | CC BY-SA 3.0 |
| `cee-bot/rauvolfia` | *Rauvolfia serpentina* | CC BY-SA 3.0 |
| `cee-bot/root-nodules` | clover root nodules | CC BY-SA 4.0 |
| `cee-bot/tissue-culture` | cucumber plantlets in vitro | CC BY 4.0 |
| `cee-chem/brown-ring` | brown-ring nitrate test | CC BY-SA 3.0 |
| `cee-chem/carbon-allotropes` | eight allotropes of carbon | CC BY-SA 3.0 |
| `cee-chem/fractional-distillation` | fractionating column | CC BY-SA 3.0 |
| `cee-phy/newtons-rings` | Newton's rings | CC0 |
| `cee-phy/prism-dispersion` | dispersion through a prism | CC0 |
| `cee-phy/ripple-interference` | ripple-tank interference | CC0 |
| `cee-zoo/plasmodium-schizont` | *P. vivax* schizont, thin smear | public domain |
| `cee-zoo/plasmodium-smear` | *Plasmodium vivax* blood film | CC BY-SA 4.0 |
| `cee-zoo/respiratory-system` | respiratory system, labelled | public domain |

## Quality gates (the repo's own, not new criteria)

- `notes/pipeline/check.py` — **84 / 84 chapters pass**: every maths expression, every figure, all
  119 photos render, no unpaired `$`, no over-wide display equation, no overprinted or sub-7 pt
  figure label.
- `notes/tools/mcqcheck.py` — **4,837 / 4,837 MCQs keyed**, 0 warnings, worst key letter 24.1 %.
- Build log — zero `[math] … fell back`, zero `[figures] … failed`, zero `[photos] … failed`
  across all six books.
- Placed-image count inside each PDF matches its photo-block count exactly, so no photograph
  silently dropped.
- Every installed chapter, PDF and asset re-verified byte-identical to the tree that passed.

## Known gaps

1. **Two images deliberately not placed**, because no checked overlay exists:
   `bio11/sycon-photo` (filed by its photographer as "Sycon sp. à confirmer" — the species is not
   established, and a CEE student is asked to name the specimen) and `chem12/titration` (a bare
   burette clamp).
2. **`cee-zoo/plasmodium-schizont` is only 300 × 300 px**, the largest Commons offers. It prints
   soft at 66 % column width; the overlay numerals stay crisp, the micrograph does not.
3. **Physics and MAT graphs and circuits stay as vector drawings** by design — they are
   constructions, not specimens, and a photograph of a ripple tank is no substitute for the
   derivation beside it.

## Building them again

The package's markdown alone cannot build: `build_pdf.py` resolves photo ids through
`assets/credits.json` and needs the whole asset library. From `notes/pipeline`:

```powershell
$env:PATH = "C:\Program Files\GTK3-Runtime Win64\bin;" + $env:PATH   # WeasyPrint 70 needs the newer Pango
python build_pdf.py cee-phy cee-chem cee-zoo cee-bot cee-mat cee-mock
```

PowerShell renders a child's stderr as a terminating `NativeCommandError` even on success — the
GLib-GIO warnings about UWP app verbs are noise. Check the artifact, not the exit code.

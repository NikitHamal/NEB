# Class 10 completion + Class 8 build — working handoff

Branch: `resources/class10-class8-dsh` (from `hoplite/gortyn-fcf4f1d3` @ `25e55a3e`).
Pushes go through the AgentSky GitHub connector (the platform injects OAuth);
the owner's private repo is not reachable by plain `git push` from the pod.

## Push rules learned the hard way

- `git clone` works with the short-lived `temp_clone_token` the repo API
  returns, but that token is **read-only** — `git push` always 403s.
- `actl connector call github --body '…'` passes the body as an argv, so the
  kernel's 2 MB `ARG_MAX` caps it. Fine for text, useless for a 25 MB PDF.
- The connector's own HTTP endpoint (`POST {ACTL_BASE_URL}/api/agent/connector`,
  bearer `ACTL_AUTH_TOKEN`) takes the same payload with no argv limit, and that
  is what `notes/tools/push_branch.py` uses: create blobs -> tree -> commit ->
  fast-forward the branch ref.
- Hard ceiling found by probing: a single blob body above ~27 MB is rejected
  with `413 Request Entity Too Large`. **Every committed file must stay under
  25 MB**, so oversized books get a lossless-ish image-downsample pass before
  they are pushed.

## Environment recipe (rebuilt from scratch each session)

```
apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
    libgobject-2.0-0 libcairo2 shared-mime-info fonts-dejavu-core fontconfig
pip install weasyprint numpy matplotlib pymupdf markdown pillow
bash notes/pipeline/fonts/install.sh        # 5 book fonts + Noto Devanagari
```

Then `cd notes/pipeline && python3 check.py ../content/<slug>/unit-NN.md` and
`python3 build_pdf.py <slug>` both work in-tree (the pipeline resolves
`theme.css` and `brand/` beside itself).

## Where class 10 stood at the start of this session

All 7 books were present, `check.py`-clean, and already had 2.5k–6.5k words per
chapter. The gap to the Grade 11/12 books was **density of information
graphics**, not prose:

| Book | chapters | figures | photos | worked examples |
|---|---|---|---|---|
| science 10 | 19 | 56 | 72 | 105 |
| social 10 | 10 | 46 | 59 | 18 |
| english 10 | 18 | 36 | 25 | 77 |
| math 10 | 18 | 62 | **0** | 324 |
| optional math 10 | 12 | 53 | **0** | 268 |
| nepali 10 | 17 | **8** | 18 | 47 |
| question bank 10 | 16 | **7** | **0** | 4 |

Also: `qbank10` stops at unit 16 while its spine lists 19 units; the
`hours:` frontmatter is `0` on several class-10 books so the book's own
"Organisation of the book" table prints em-dashes where 11/12 print hours; and
the web app's Interactive hub ships NEB practical labs for grades 11/12 only.

## Work queue

1. [ ] qbank10 units 17–19 (spine completion)
2. [ ] Class 10 information-graphics pass (figures, infographics, real images)
3. [ ] `hours:` frontmatter backfill for every class-10 chapter
4. [ ] Interactive layer for class 10 (NEB Science/Maths virtual labs)
5. [ ] Rebuild + size-normalise the class-10 books, push
6. [ ] Class 8: curriculum spines, then the full chapter sets + question bank

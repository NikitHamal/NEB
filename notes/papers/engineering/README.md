# Engineering past-paper research dump (branch `claude/engineering`)

Raw source dump for the NEB app's **engineering** past papers / question banks (Nepal). Session 1-2 = research + bulk download only;
the *work* (extract, normalise, author JSON for the app) is a LATER session. Do NOT re-research: read `../PAPERS_TRACKER.md` first.

## Layout (`notes/papers/engineering/`)
- `sources/<group>/<collection>/...` - downloaded files, untouched names (PDF/DOC/DOCX). Groups: `tu-ioe` (IOE past-questions + curriculum), `pokhara-university`,
  `purbanchal-university`, `kathmandu-university`, `ioe-entrance`, `nec-licence`, `ctevt`, `github` (cloned repos, `.git` stripped), `promod-blog`, `ndds-ioe-entrance`.
- `manifests/*.jsonl` - one line per attempted file: `url, dest(rel. to sources/), meta, status(ok|exists|http404|notfile|err), sha256, bytes, pages, title`.
  **sha256/bytes are of the ORIGINAL download**; large scanned PDFs were later recompressed in place (see below), so on-disk size/hash differ.
- `INVENTORY.md` - auto-generated per-collection counts (`python3 tools/inventory.py`).
- `tools/` - re-usable scripts (run from repo root; `pip install --break-system-packages requests beautifulsoup4 lxml pymupdf gdown`):
  `harvest.py` (regex raw-HTML harvester -> tasks, expands Drive folders), `jsonld_tasks.py` (schema.org ItemList pages), `crawl.py`/`build_tasks.py` (older bs4 crawler),
  `fetch.py` (parallel downloader+manifest), `filter_new.py` (drop already-have), `dedupe.py` (sha dedupe vs other manifests), `retry_gdown.py`, `wayback_fetch.py`,
  `compress.py`/`compress_batch.sh` (PyMuPDF image recompress 130 dpi q60, ~4x smaller), `blogger_dump.py`, `inventory.py`.

## Conventions / gotchas
- SharePoint share links (`...sharepoint.com/:b:/g/...`) download with `?download=1` (used for 65 bani.com.np papers).
- Drive `uc?export=download&id=` works for <25 MB; bigger files need `retry_gdown.py`.
- GitHub rejects >50 MB files: compress first (`compress_batch.sh DIR 3 30 140`, repeat; progress in /tmp/w/compressed.txt). Two pre-existing files are 45-80 MB (waraunika CE.pdf, promod env-eng) - already pushed by an earlier session.
- Wall-clock limit per tool call ~3 min: keep downloads <90 s, compression batches <=50 files, push after every batch (a 120 MB push takes ~20 s).
- Dead/blocked hosts seen: blog.promod.com.np (conn error, Wayback 429/no snapshot), ioenotes.edu.np Drive ids (404), entrance.ioe.edu.np, ravidhami.com, sudipkhadka.com.np (conn refused from sandbox). Studocu/Scribd/CourseHero are login-walled - not downloadable.
- Dedup: `dedupe.py` deleted files whose original sha256 already existed elsewhere (manifest rows kept; `dest` may be missing on disk = duplicate).

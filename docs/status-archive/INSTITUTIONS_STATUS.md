# Institutions, verification and result checker: status

Read before touching `schools`, institution verification or the result checker. One doc for this track; extend it, do not start another.

## Catalogue

- `backend_python/api/data/institutions.json.gz`: 24,665 institutions (23,504 schools, 933 colleges, 142 institutes, 86 universities) across all 78 district polygons. Built by `tools/institutions/build_catalog.py`.
- Sources: OpenStreetMap (`amenity=school|college|university` in Nepal, ODbL, attribution OpenStreetMap contributors), Wikidata (official website, inception year, CC0), `tools/institutions/curated.json` (hand checked sites), `api/data/institution_sites.json` (official websites verified live, matched by name and district).
- Seeding: migration `0166_seed_institutions` (only when the table is empty), `0168_institution_sites` (fills blank websites from the overlay, adds missing well known schools, removes one bad Wikidata link). `manage.py import_institutions` adds rows that are not there yet, never edits existing ones.
- Only about 280 rows have a website (256 in the base file plus the overlay). The overlay is the place to add more: append `{name, kind, district, website}` (https only), open the site first, rerun tests. The build reads the overlay too, so a rebuild keeps them.

## Behaviour

- `/app/schools/`: verified institutions (claimed and approved) are listed first in "On NEBians" with their student counts; every other institution is below, 30 per page, search by name, kind chips, district select.
- `/app/schools/<slug>/`: counts (on NEBians, students, teachers), people list with All / Students / Teachers chips, website button, "Claim this school" while unverified.
- Student profile school link: verified and claimed gives the institution's NEBians profile; otherwise the school's own website in a new tab (`rel=noopener nofollow`); otherwise the school page. `school_go` redirects the same way with `Referrer-Policy: no-referrer`.
- `/app/schools/verify/` (institution accounts only): name, kind, district, address, website, registration number, contact person, role, email, phone, message, and up to six documents with a type each. Rate limited, one open application at a time, reviewer note can ask for more (`needs_info`).
- Admin: `admin_panel/institution_verifications.html` list with tabs, detail page with documents, approve (sets `verified`, claims the institution, links people, notifies the applicant), reject, needs info, revoke.
- Profile picker (edit profile) searches the catalogue; choosing a school sets `school_slug`, which is what the counts read.

## Result checker (`/app/results/check/`)

- Revamped on m3x: `result_checker.html`, `css/pages/result-checker-page.css`, `js/pages/result-checker.js`. Sliding class switch (Class 12 / Class 10), chips for Regular / Re-exam and Single / Bulk, white fields with one stroke (`.md-input`, `.md-select`, `.md-textarea`), one filled submit button with the morphing loader, error alert in error-container, bulk progress bar and table, result card with a cookie-shaped GPA medallion (primary, tertiary or error by GPA), tonal grade labels, details as inset tiles, subjects table in a tonal panel.
- Share card canvas and the printable gradesheet are flat: no gradients, no shadow, the gradesheet logo is drawn with flat fills. The gradesheet keeps its document look (white paper, blue ink) in both themes.
- No inline `style=` attributes in the template; the script toggles `hidden`, `md-chip-active`, `data-i` and state classes only.
- Tests: `web/test_result_checker_m3x.py` (no gradient, shadow, emoji, no hover to square, no inline style, every script hook exists, page renders), `web/test_tools_copy.py`, `web/test_icon_font.py` (use only icons that are in the font subset; `ios_share` is not).

## Design doc

`docs/M3X_DESIGN_SYSTEM.md` is the paste-able master document (prompt, tokens, type, shape generator, springs, components, bans, checklist). Keep it in step with `m3x/tokens.css`.

## Tests

`cd backend_python && DEBUG=True DB_ENGINE=sqlite python3 manage.py test` (full run is about 40 s). Institutions: `web.test_institutions` (27), `web.test_institution_sites` (3).

## Open

- More official websites (most of the 23k schools only have a map point). Wikidata and the overlay are the sources; do not scrape search engines.
- Document files are stored through the normal upload path; there is no virus scan.
- Android parity for schools was not checked this session; the API is `/api/institutions/` and `/api/institutions/<slug>/` (`api/views_institutions.py`).
- Rotate any personal access token that was pasted into a chat; none is stored in the repo.

## Portfolio on web and Android (session 41)

- Web `/app/schools/<slug>/` prints the claimed portfolio through `folio_context` (`web/views_institutions_profile.py`); an institution with no portfolio data shows the old page.
- Android: `InstitutionScreen` (read) and `InstitutionManageScreen` (owner edit, any field, any time) use the same schema as the web. Profile concept for the overhaul: `NEBians-Profile.html`, published on GitHub Pages (`gh-pages`, `profile.html`).

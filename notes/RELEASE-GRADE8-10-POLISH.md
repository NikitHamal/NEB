# Class 8 and 10 books and syllabus release

Base: `resources/grade8-rebuild-grade10-books` (`b6d601e`).
Delivery branch: `resources/grade8-10-polish-syllabus-c`. Main was not modified.

## Books

Rebuilt and pushed 17 complete books: 250 chapters and 3,014 pages. This includes the six Class 8 subject books, eight Class 10 subject books, and three question-bank volumes. PDFs are under `notes/pdf/`; source chapters remain under `notes/content/`.

The editorial pass corrected first-aid instructions, blood-group notation, population terminology, misleading social-studies explanations, opportunity-cost wording and unsupported examination-weight claims. Class 10 social-studies question-bank material was rewritten in Nepali, including three complete 75-mark practice papers. These are practice materials, not examination predictions. Optional mathematics, accountancy and economics gained 99 reasoned retrieval checks and 33 investigations. Coverage charts now count the actual questions instead of inventing official weights.

Repaired 14 image-registry paths that prevented complete chapter rendering. Nepali-medium copy, furniture and image credits use Nepali script; original attribution and licence details remain available through source links. Missing chapters, failed equations, failed figures, missing photos and unpaired mathematical delimiters now prevent a successful PDF release. PDF replacement is atomic.

This is an editorial and production improvement to the existing books, not a claim that every passage was independently rewritten or certified by the curriculum authority. Teacher review remains appropriate before classroom assessment use. Some PDF viewers extract shaped Devanagari text imperfectly; editable UTF-8 chapter sources remain available.

## Syllabus study experience

The generated catalogue contains 28 subject books and 492 chapters across Classes 8, 10, 11 and 12. Run `python notes/tools/export_syllabus.py` after changing chapters or curriculum spines, and `--check` in validation. Each chapter records its source path, SHA-256, topics, summary, teaching hours where known and existing model answers. This catalogue is a study companion derived from the notes, not a newly issued official specification grid.

Managed grades use the packaged catalogue rather than the old database syllabus. Older database rows are preserved for rollback but no longer shown, including common old grade aliases. Web and Android share the same API catalogue.

Web features include responsive subject search, chapter search/navigation, a table of contents, previous/next controls, worked-answer disclosure and local revision progress. Icons are bundled locally. Android includes searchable chapter selection, previous/next controls, local revision progress and disk caching of previously fetched public syllabus content. No fabricated offline subjects are displayed. Revision progress is device-local, not account-synchronised.

## Verification

- All 250 Class 8/10 chapter files passed equation, figure, photo and delimiter rendering checks; the final social-studies correction was also checked separately.
- All 17 released PDFs open, have bookmarks and have no empty pages. The release audit records checksums, pages, links and chapter counts.
- Seven focused Django tests pass, covering source hashes, completeness, canonical navigation, old-grade replacement, Nepali headings, anchors and escaping.
- All 28 public syllabus subject endpoints return their expected 492 chapters with study checks.
- Desktop and mobile browser checks passed at 1440 and 390 pixels: no horizontal overflow or JavaScript errors; subject filtering, empty search, saved revision state and next-chapter navigation work.
- Both `compileModernDebugKotlin` and `compileLegacyDebugKotlin` pass. No physical-device or emulator UI test was performed.
- Launch-video drift check passes; the existing marketplace availability notice remains informational.

## Release steps

This branch has not been merged or deployed to production. Deploy the Django changes and packaged catalogue together. No syllabus database migration is required. Build and release a new Android version to expose native UI changes. Use the normal production settings and existing release-signing workflow; local debug configuration is not a deployment configuration.

No subagents were used. Each finished PDF was checkpointed to GitHub individually. Build details are in `task/book-builds.json` and the release audit.

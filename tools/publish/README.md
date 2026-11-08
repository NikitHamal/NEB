# Publishing the books to the library

`manifest.json` holds one listing per built PDF (92 books): title, description, level, program, tags, file, cover.
`build_manifest.py` writes it from the spines, the BCA registry and the built PDFs, so a rebuilt book refreshes its
own page count. `covers/` are 16:9 JPEGs (1280 x 720, drawn by `notes/pipeline/thumb.py`, not the portrait first page) and are sent as the resource thumbnail.

```bash
# 1. on the machine that has the repo and the PDFs
export NEB_EMAIL=...  NEB_PASSWORD=...          # or NEB_TOKEN=<authToken>; NEB_BASE_URL defaults to the live site
python tools/publish/publish_books.py --dry-run  # read every listing first
python tools/publish/publish_books.py --level 12 # try one level
python tools/publish/publish_books.py            # everything not yet published

# 2. on the server, once the upload is checked
python manage.py approve_book_uploads <username>         # lists the pending uploads
python manage.py approve_book_uploads <username> --yes   # publishes them
```

A run is resumable: `published.json` (slug to resource id) is written after every upload, and a book whose title the
account already has in the library is skipped. Uploads are throttled by the server; the script waits on a 429.
Delete a line of `published.json` to upload a book again after rebuilding it (delete the old resource first).

## Updating rebuilt PDFs and covers

```bash
python tools/publish/build_manifest.py                 # refresh listings (and covers/) from the rebuilt PDFs
python tools/publish/update_books.py --seed            # once, after the first publish run
python tools/publish/update_books.py --dry-run         # what changed since the last run
python tools/publish/update_books.py                   # PATCH only the changed files
python manage.py approve_book_uploads <username> --yes # on the server, the edit puts them back to pending
```

`update_books.py` compares each PDF and cover with `published_files.json` (the versions last uploaded) and sends
only what changed; listing text stays untouched. Re-run it after every batch of rebuilds.

Regenerate the manifest after any PDF rebuild: `python tools/publish/build_manifest.py` (needs `pypdf` and `pymupdf`).

Books already in the library keep the thumbnail they were uploaded with. To give them the 16:9 cover: `python tools/publish/update_covers.py --dry-run`, then without `--dry-run`
(same credentials; matches `published.json` or the exact title; changes only the thumbnail).

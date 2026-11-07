# Publishing the books to the library

`manifest.json` holds one listing per built PDF (92 books): title, description, level, program, tags, file, cover.
`build_manifest.py` writes it from the spines, the BCA registry and the built PDFs, so a rebuilt book refreshes its
own page count. `covers/` are the first pages as 420 px JPEGs, sent as the resource thumbnail.

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

Regenerate the manifest after any PDF rebuild: `python tools/publish/build_manifest.py` (needs `pypdf` and `pymupdf`).

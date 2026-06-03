#!/usr/bin/env python3
"""
Server-side PDF recompression using Ghostscript.
Same approach as ilovepdf: /ebook = 150 DPI images, font subsetting.
Run: python3 /tmp/gs_compress.py
"""
import os
import subprocess
import sys
import django
from pathlib import Path

# Django setup for DB updates
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from api.models import Resource

# Find media directory
candidates = [
    Path('/home/consicac/nebians_api/media/resources'),
    Path('/home/consicac/nebians_api/mediafiles/resources'),
    Path('/home/consicac/nebians_api/public/media/resources'),
]

media_dir = None
for c in candidates:
    if c.exists() and any(c.glob('*.pdf')):
        media_dir = c
        break

if media_dir is None:
    # Try from DB
    r = Resource.objects.filter(file__endswith='.pdf').first()
    if r:
        from django.conf import settings
        media_dir = Path(settings.MEDIA_ROOT) / 'resources'
        print(f"Using MEDIA_ROOT path: {media_dir}")
    else:
        print("No PDF resources found in DB either. Exiting.")
        sys.exit(0)

print(f"=== Ghostscript PDF Recompression ===")
print(f"Media dir: {media_dir}")
print(f"PDFs found: {len(list(media_dir.glob('*.pdf')))}")
print()

total_before = 0
total_after  = 0
compressed   = 0

for pdf_path in sorted(media_dir.glob('*.pdf')):
    before = pdf_path.stat().st_size
    total_before += before
    tmp_path = pdf_path.with_suffix('.gs_tmp.pdf')

    print(f"Processing: {pdf_path.name}  ({before/1024/1024:.2f} MB)")

    result = subprocess.run([
        'gs', '-q',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/ebook',
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        '-dDetectDuplicateImages=true',
        '-dCompressFonts=true',
        '-r150',
        f'-sOutputFile={tmp_path}',
        str(pdf_path),
    ], capture_output=True)

    if result.returncode != 0 or not tmp_path.exists():
        print(f"  ✗ Ghostscript failed: {result.stderr.decode()[:200]}")
        tmp_path.unlink(missing_ok=True)
        total_after += before
        continue

    after = tmp_path.stat().st_size
    savings = before - after
    pct = savings / before * 100

    if after < before:
        tmp_path.replace(pdf_path)
        print(f"  ✓ {before/1024/1024:.2f} MB → {after/1024/1024:.2f} MB  "
              f"(saved {savings/1024/1024:.2f} MB, {pct:.1f}%)")
        total_after += after
        compressed += 1
    else:
        tmp_path.unlink(missing_ok=True)
        print(f"  ~ No improvement ({before/1024/1024:.2f} MB), keeping original")
        total_after += before

print()
saved_total = total_before - total_after
print(f"=== Summary ===")
print(f"Compressed: {compressed} PDF(s)")
print(f"Before: {total_before/1024/1024:.2f} MB")
print(f"After:  {total_after/1024/1024:.2f} MB")
print(f"Saved:  {saved_total/1024/1024:.2f} MB  "
      f"({saved_total/total_before*100:.1f}% total)" if total_before else "")
print()

# Update file_size in DB
print("=== Updating DB file_size records ===")
updated = 0
for pdf_path in sorted(media_dir.glob('*.pdf')):
    rel = f"resources/{pdf_path.name}"
    new_size = pdf_path.stat().st_size
    qs = Resource.objects.filter(file=rel)
    if qs.exists():
        qs.update(file_size=new_size)
        updated += qs.count()
        print(f"  DB: {rel} → {new_size:,} bytes ({new_size/1024/1024:.2f} MB)")
print(f"Updated {updated} DB record(s)")

print()
print("=== Final listing ===")
for f in sorted(media_dir.glob('*.pdf')):
    print(f"  {f.name}: {f.stat().st_size/1024/1024:.2f} MB")

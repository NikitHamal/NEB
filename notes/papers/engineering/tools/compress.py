#!/usr/bin/env python3
"""Recompress scanned PDFs in place (images -> <=130 dpi JPEG q60, garbage-collect, deflate).
Usage: compress.py MIN_MB DIR_OR_FILES...   (only files larger than MIN_MB are touched)
Keeps the original text layer; skips files that would grow."""
import sys, os, glob, warnings
warnings.filterwarnings('ignore')
from multiprocessing import Pool
import pymupdf
def work(f):
    try:
        before = os.path.getsize(f); d = pymupdf.open(f)
        d.rewrite_images(dpi_threshold=160, dpi_target=130, quality=60)
        tmp = f + '.tmp'; d.save(tmp, garbage=4, deflate=True, clean=True); d.close()
        after = os.path.getsize(tmp)
        if after < before * 0.95: os.replace(tmp, f)
        else: os.remove(tmp); after = before
        return f, before, after
    except Exception as e:
        return f, -1, str(e)[:60]
if __name__ == '__main__':
    mn = float(sys.argv[1]) * 1e6; fs = []
    for a in sys.argv[2:]:
        fs += glob.glob(os.path.join(a, '**/*.pdf'), recursive=True) if os.path.isdir(a) else [a]
    fs = [f for f in fs if os.path.getsize(f) > mn]
    with Pool(4) as p: res = p.map(work, fs, chunksize=1)
    ok = [r for r in res if r[1] > 0]
    print(len(fs), 'files;', sum(r[1] for r in ok) // 10**6, 'MB ->', sum(r[2] for r in ok) // 10**6, 'MB; errors:', [r for r in res if r[1] < 0][:5])

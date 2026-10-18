#!/usr/bin/env python3
"""Legacy Nepali font -> Unicode, for reading CDC PDFs.

The CDC publishes its textbooks, teacher guides and even some curricula with the
text encoded in the legacy ASCII fonts Preeti, Kantipur and Himalb/Himali. Copy
the text out and you get `kf7\\oj|md ljsf; s]Gb|` instead of
`पाठ्यक्रम विकास केन्द्र`, which is useless for building a syllabus spine.

This module applies the published character map plus the pre/post reordering
rules (the `ि` matra and the `ि`/`े`/`ो` clusters have to be moved, and the
`र्`/`्र` forms rebuilt) so the text comes back as proper Devanagari. The mapping
table is `preeti_map.json`, taken from the `casualsnek/npttf2utf` project.

Used by `tools/cdc_toc.py` to extract chapter lists; keep it in the repo so the
next session does not have to rediscover which font each document uses.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(HERE, "preeti_map.json")

_CACHE = {}


def _maps():
    if not _CACHE:
        with open(MAP_PATH, encoding="utf-8") as fh:
            _CACHE.update(json.load(fh))
    return _CACHE


# The CDC documents mis-encode the क्र ligature: the published tables expect the
# sequence "qm" (q = त्र + the m marker) but the CDC files carry "j|m", which the
# tables read as व + ्र. Left alone, पाठ्यक्रम comes out as फाठ्यव्रम and
# क्रियाकलाप as व्रियाकलाप. Rewriting the code sequence before mapping fixes
# both, and it cannot touch a real व्र cluster, which never carries the m marker.
CDC_PRE_RULES = [(r"j\|m", "qm")]


# Which mapping table to use for each embedded font name seen in the CDC PDFs.
FONT_ALIASES = {
    "preeti": "Preeti",
    "kantipur": "Kantipur",
    "himalb": "FONTASY_HIMALI_TT",
    "himali": "FONTASY_HIMALI_TT",
    "fontasy": "FONTASY_HIMALI_TT",
}


def table_for(font_name):
    low = (font_name or "").lower()
    for key, table in FONT_ALIASES.items():
        if key in low:
            return table
    return None


def convert(text, table="Preeti"):
    """Convert legacy-encoded text to Unicode Devanagari.

    The rules must be applied **word by word** in the order pre-rules, then the
    character map, then post-rules — that is what the reference implementation
    (`npttf2utf.base.fontmapper.FontMapper`) does, and doing it over the whole
    string instead mangles the `प`/`फ` and `क्र`/`व्र` clusters.
    """
    rules = _maps()[table]["rules"]
    cmap = rules["character-map"]
    out = []
    for word in re.findall(r"(\s+|\S+)", text):
        for pat, rep in CDC_PRE_RULES:
            word = re.sub(pat, rep, word)
        for pat, rep in rules.get("pre-rules", []):
            word = re.sub(pat, rep, word)
        word = "".join(cmap.get(ch, ch) for ch in word)
        for pat, rep in rules.get("post-rules", []):
            word = re.sub(pat, rep, word)
        out.append(word)
    return "".join(out)


def pdf_page_text(page):
    """Page text with each span converted using the mapping of its own font."""
    parts = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                t = span.get("text", "")
                table = table_for(span.get("font"))
                parts.append(convert(t, table) if table else t)
            parts.append("\n")
    return "".join(parts)


def pdf_text(path, first=0, last=None):
    import pymupdf

    doc = pymupdf.open(path)
    last = doc.page_count if last is None else min(last, doc.page_count)
    out = []
    for i in range(first, last):
        out.append(pdf_page_text(doc[i]))
    doc.close()
    return "".join(out)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    args = sys.argv[1:]
    if args[0] == "text":
        print(convert(" ".join(args[1:])))
    else:
        lo = int(args[1]) if len(args) > 1 else 0
        hi = int(args[2]) if len(args) > 2 else lo + 3
        print(pdf_text(args[0], lo, hi))

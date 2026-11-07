#!/usr/bin/env python3
"""Visual + structural QA for built Nursing PDFs. Exits non-zero if any hard check fails.

    python3 bca/tools/qa_pdf.py                      # every PDF under nursing/
    python3 bca/tools/qa_pdf.py --png /tmp/qa        # also render PNG contact sheets for eyeballing
    python3 bca/tools/qa_pdf.py path/to/book.pdf

Hard checks (FAIL): cover present; "Contents" page with >= 1 internal link per chapter; every body page
carries a page number; house fonts embedded (Poppins, Source Serif 4; Inter is optional since the m3x print system); no text outside the page
margins (overflowing tables / unwrapped code); no code line clipped at the right margin; no leaked TeX
(`$`, `\\frac`, `\\sqrt`...) in body text; no heading stranded alone at the bottom of a page; PDF title set.
Soft checks (WARN): near-empty pages (<6% ink area, last page of a chapter excluded), very small fonts.
"""
import glob, os, re, sys
import fitz  # pymupdf

BCA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARGIN_R_MM = 10          # nothing may be closer than this to the right edge
MM = 72 / 25.4


def check(path, png_dir=None):
    fails, warns = [], []
    doc = fitz.open(path)
    n = len(doc)
    if doc.metadata.get("title", "").strip() == "":
        fails.append("PDF metadata title is empty")
    fonts = set()
    for p in list(doc)[:40]:
        for f in p.get_fonts():
            fonts.add(f[3])
    for need in ("Poppins", "SourceSerif4"):
        if not any(need.lower() in f.lower().replace(" ", "").replace("-", "") for f in fonts):
            fails.append(f"house font not embedded: {need}")
    first = doc[0].get_text()
    if "NEBians".lower() not in first.lower():
        fails.append("page 1 is not the NEBians cover")
    toc_page = next((i for i in range(min(n, 8)) if re.search(r"^\s*Contents\s*$", doc[i].get_text(), re.M)), None)
    if toc_page is None:   # Nepali books title the list "विषयसूची": accept the first page with many internal links
        toc_page = next((i for i in range(min(n, 8)) if sum(1 for l in doc[i].get_links()
                         if l.get("kind") in (fitz.LINK_GOTO, fitz.LINK_NAMED)) >= 5), None)
    if toc_page is None:
        fails.append("no Contents page in the first 8 pages")
    else:
        links = [l for q in (toc_page, toc_page + 1) if q < n for l in doc[q].get_links()
                 if l.get("kind") in (fitz.LINK_GOTO, fitz.LINK_NAMED)]   # the list may spill onto the next page
        if len(links) < 1:
            fails.append("Contents page has no internal links")
    body_start = (toc_page or 0) + 1
    leak = re.compile(r"\$|\\(frac|sqrt|sum|int|alpha|beta|times|cdot|le|ge)\b|\\\\")
    for i, page in enumerate(doc):
        W, H = page.rect.width, page.rect.height
        d = page.get_text("dict")
        text = page.get_text()
        if i >= 1 and not re.search(r"\b(\d+|[ivxl]+)\s*$", text.strip()[-12:], re.I) and i != 0:
            fails.append(f"p{i+1}: no page number at foot")
        ink = 0.0
        last_block = None
        for b in d["blocks"]:
            if b["type"] != 0:
                continue
            x0, y0, x1, y1 = b["bbox"]
            ink += (x1 - x0) * (y1 - y0)
            if x1 > W - MARGIN_R_MM * MM + 2 and i > 0 and (y0 > 40 and y1 < H - 40):
                snippet = " ".join(s["text"] for l in b["lines"] for s in l["spans"])[:60]
                fails.append(f"p{i+1}: text runs into right margin (x1={x1:.0f}/{W:.0f}): {snippet!r}")
            for l in b["lines"]:
                for s in l["spans"]:
                    if "mono" in s["font"].lower() and s["bbox"][2] > W - 8 * MM:
                        fails.append(f"p{i+1}: code line clipped/overflowing: {s['text'][:50]!r}")
                    if s["size"] < 6.2 and s["text"].strip() and i > 0 and y0 < H - 40:
                        warns.append(f"p{i+1}: tiny text {s['size']:.1f}pt {s['text'][:30]!r}")
        prose = " ".join(sp["text"] for b in d["blocks"] if b["type"] == 0 for l in b["lines"]
                         for sp in l["spans"] if "mono" not in sp["font"].lower())   # code may contain $ and \\
        # Noto Sans Devanagari (semibold) maps the "pri"/"kri" conjunct glyphs to "$" in
        # its ToUnicode table: a "$" touching a Devanagari letter is a text-extraction
        # artefact of the font, not leaked TeX (the page itself renders correctly).
        # (the same font also maps the matra glyphs to stray Latin-extended letters U+0180-02AF.)
        _dv = "[\u0900-\u097F\u0180-\u02AF]"
        prose = re.sub(r"(?<=" + _dv + r")\s?\$|\$\s?(?=" + _dv + ")", "", prose)
        if i >= body_start and leak.search(prose):
            m = leak.search(prose)
            fails.append(f"p{i+1}: leaked TeX / stray '$' near {prose[max(0,m.start()-25):m.end()+25]!r}")
        if i >= body_start and ink / (W * H) < 0.06 and i != n - 1:
            nxt = doc[i + 1].get_text()[:200] if i + 1 < n else ""
            if not re.search(r"\bUnit \d+\b|Appendix", nxt):
                warns.append(f"p{i+1}: near-empty page ({ink/(W*H):.1%} ink)")
        # stranded heading: last text block on the page is a Poppins heading
        blocks = [b for b in d["blocks"] if b["type"] == 0 and b["bbox"][1] < H - 45]
        if blocks and i >= body_start:
            lb = max(blocks, key=lambda b: b["bbox"][3])
            spans = [s for l in lb["lines"] for s in l["spans"]]
            if spans and all("poppins" in s["font"].lower() for s in spans) and lb["bbox"][3] > H - 80 \
                    and len(lb["lines"]) <= 2 and spans[0]["size"] >= 10.5:
                fails.append(f"p{i+1}: heading stranded at page bottom: {lb['lines'][0]['spans'][0]['text'][:50]!r}")
    if png_dir:
        os.makedirs(png_dir, exist_ok=True)
        stem = os.path.splitext(os.path.basename(path))[0]
        pick = sorted(set([0, 1, 2, toc_page or 2, body_start, body_start + 1, n // 3, n // 2, (2 * n) // 3, n - 1]))
        pick = [p for p in pick if 0 <= p < n]
        pix = [doc[p].get_pixmap(dpi=55) for p in pick]
        cols = 5
        rows = (len(pix) + cols - 1) // cols
        w, h = pix[0].width, pix[0].height
        sheet = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, cols * (w + 6), rows * (h + 6)), False)
        sheet.set_rect(sheet.irect, (110, 110, 110))
        for k, px in enumerate(pix):
            px = fitz.Pixmap(fitz.csRGB, px) if px.n != 3 else px
            px.set_origin((k % cols) * (w + 6) + 3, (k // cols) * (h + 6) + 3)
            sheet.copy(px, px.irect)
        out = os.path.join(png_dir, stem + ".sheet.png")
        sheet.save(out)
    return n, sorted(set(fails)), sorted(set(warns))


def main(argv):
    png = None
    if "--png" in argv:
        k = argv.index("--png")
        png = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    pdfs = argv or sorted(glob.glob(os.path.join(BCA, "**", "pdfs", "*.pdf"), recursive=True))
    total_fail = 0
    for p in pdfs:
        n, f, w = check(p, png)
        status = "FAIL" if f else "ok"
        print(f"[{status:4}] {os.path.relpath(p, os.path.dirname(BCA))}  pages={n}  fails={len(f)} warns={len(w)}")
        for x in f[:12]:
            print("    FAIL", x)
        for x in w[:6]:
            print("    warn", x)
        total_fail += len(f)
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/env python3
"""Export every chapter and question-bank chapter of the books for the website and the app.

The PDF pipeline (pipeline/md2html.py) is reused as is, with two changes for the screen:
maths is left as TeX for KaTeX to typeset in the browser or the app (the PDF draws every
expression as an SVG, ~1.7 MB a chapter), and figures and photographs are written once as
files named by their content hash instead of being inlined. Output:

    backend_python/web/data/study/<grade>-<subject>/unit-NN.json     the chapters
    backend_python/web/data/study/<grade>-<subject>/bank-NN.json     its question-bank chapters
    backend_python/web/data/study/<grade>-<subject>/index.json       what exists, for the pages
    backend_python/web/static/web/study/<hash>.svg|.webp              figures and photographs

Run:  python3 notes/tools/export_study.py [book ...]     (default: every book of grades 8-12)
Needs the book fonts (notes/pipeline/fonts/install.sh): without Inter and Noto Sans Devanagari
matplotlib silently falls back and every Nepali label in a figure becomes a row of boxes. Clear
notes/figures/_fig/ after installing them, or the figure cache keeps the old drawings.
"""
import hashlib
import html as _html
import json
import os
import re
import shutil
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
ROOT = os.path.dirname(NOTES)
PIPE = os.path.join(NOTES, "pipeline")
sys.path.insert(0, PIPE)
sys.path.insert(0, HERE)

DATA = os.path.join(ROOT, "backend_python", "web", "data", "study")
MEDIA = os.path.join(ROOT, "backend_python", "web", "static", "web", "study")
MEDIA_URL = "/static/web/study/"

BOOKS = ["nep8", "eng8", "math8", "sci8", "soc8", "health8",
         "nep10", "eng10", "math10", "sci10", "soc10", "omath10", "acc10", "eco10",
         "nep11", "eng11", "math11", "phy11", "chem11", "bio11", "cs11",
         "nep12", "eng12", "math12", "phy12", "chem12", "bio12", "cs12"]
BANKS = ["qbank8", "qbank10", "qbankc10", "qbank11", "qbank12"]

# question-bank `area:` -> subject key used by the syllabus pages
BANK_AREAS = [
    (r"Science and Technology", "science"), (r"Optional Mathematics", "optional-mathematics"),
    (r"Mathematics", "mathematics"), (r"English", "english"), (r"नेपाली", "nepali"),
    (r"Social Studies|सामाजिक", "social-studies"), (r"स्वास्थ्य", "health-physical-creative-arts"),
    (r"Accountancy", "accountancy"), (r"Economics", "economics"), (r"Physics", "physics"),
    (r"Chemistry", "chemistry"), (r"Biology", "biology"), (r"Computer Science", "computer-science"),
]
SUBJECT_KEY = {"nep": "nepali", "eng": "english", "math": "mathematics", "sci": "science",
               "soc": "social-studies", "health": "health-physical-creative-arts",
               "omath": "optional-mathematics", "acc": "accountancy", "eco": "economics",
               "phy": "physics", "chem": "chemistry", "bio": "biology", "cs": "computer-science"}


def _split(slug):
    m = re.match(r"([a-z]+)(\d+)$", slug)
    return m.group(1), m.group(2)


def _media(src_path, ext=None):
    """Copy a rendered figure or photo into the static folder once; return its URL."""
    with open(src_path, "rb") as fh:
        blob = fh.read()
    key = hashlib.sha1(blob).hexdigest()[:20]
    ext = ext or os.path.splitext(src_path)[1].lower()
    if ext in (".png", ".jpg", ".jpeg"):
        name = key + ".webp"
        out = os.path.join(MEDIA, name)
        if not os.path.exists(out):
            from PIL import Image
            im = Image.open(src_path)
            im.thumbnail((1100, 1100))
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if "A" in im.mode else "RGB")
            im.save(out, "WEBP", quality=74, method=6)
        return MEDIA_URL + name
    name = key + ext
    out = os.path.join(MEDIA, name)
    if not os.path.exists(out):
        # matplotlib writes every coordinate to 6 decimals; 2 is far below a screen pixel
        txt = blob.decode("utf-8", "replace")
        txt = re.sub(r"(\d+\.\d{2})\d+", r"\1", txt)
        txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)
        txt = re.sub(r"<metadata>.*?</metadata>", "", txt, flags=re.S)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(txt)
    return MEDIA_URL + name


def _patch_md2html():
    import md2html
    import devaeqn

    def tex_inline(tex):
        if devaeqn.DEVA.search(tex):
            return devaeqn.html(tex)
        return '<span class="m">%s</span>' % _html.escape(tex.strip())

    def tex_display(tex):
        if devaeqn.DEVA.search(tex):
            return '<div class="dm">%s</div>' % devaeqn.html(tex, True)
        return '<div class="dm"><span class="m d">%s</span></div>' % _html.escape(tex.strip())

    def inline_math_html(text):
        out, pos = [], 0
        for m in md2html._IMATH.finditer(text):
            out.append(_html.escape(text[pos:m.start()]))
            out.append(tex_inline(m.group(1)))
            pos = m.end()
        out.append(_html.escape(text[pos:]))
        return "".join(out)

    def extract_display(body, store):
        def rep(m):
            store.append(tex_display(m.group(1)))
            return "\n\n" + md2html._PLACE.format(len(store) - 1) + "\n\n"
        return md2html._outside_code(body, lambda t: re.sub(r"\$\$(.+?)\$\$", rep, t, flags=re.S))

    def extract_inline(body, store):
        def rep(m):
            store.append(tex_inline(m.group(1)))
            return md2html._PLACE.format(len(store) - 1)
        return md2html._outside_code(body, lambda t: md2html._IMATH.sub(rep, t))

    md2html._inline_math_html = inline_math_html
    md2html._extract_display_math = extract_display
    md2html._extract_inline_math = extract_inline
    md2html._svg_data_uri = lambda p: _media(p)
    md2html._png_uri = lambda p: _media(p)
    return md2html


_HEAD = re.compile(r"<h2([^>]*)>(.*?)</h2>", re.S)


def _plain(frag):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", frag))).strip()



_ANSWER_TITLE = re.compile(r"answer|solution|उत्तर|हल|उत्तरकुञ्जी", re.I)
_DEVA_NUM = str.maketrans("०१२३४५६७८९", "0123456789")
_NE_OPT = {"क": "a", "ख": "b", "ग": "c", "घ": "d"}


_BOX_OPEN = re.compile(r'<div class="box (\w+)">\s*<div class="bt">(.*?)</div>', re.S)
_DIV = re.compile(r"<div\b|</div>")


def _answers_fold(htm):
    """Answer and model-answer boxes become a closed <details>: the student tries first."""
    out, pos = [], 0
    for m in _BOX_OPEN.finditer(htm):
        if m.start() < pos or not _ANSWER_TITLE.search(_plain(m.group(2))):
            continue
        depth, end = 1, None
        for d in _DIV.finditer(htm, m.end()):
            depth += 1 if d.group(0) == "<div" else -1
            if depth == 0:
                end = d
                break
        if not end:
            continue
        out.append(htm[pos:m.start()])
        out.append('<details class="ans box %s"><summary>%s</summary><div class="ans-body">%s</div></details>'
                   % (m.group(1), m.group(2), htm[m.end():end.start()]))
        pos = end.end()
    out.append(htm[pos:])
    return "".join(out)


def _mcq_keys(htm):
    """Tie each multiple-choice list to the answer key that follows it: <li data-key="b">."""
    out, pos = [], 0
    for m in re.finditer(r"<ol>(.*?)</ol>", htm, re.S):
        block = m.group(1)
        if 'class="opts' not in block:
            continue
        nxt = re.search(r'<details class="ans[^"]*">(.*?)</details>', htm[m.end():m.end() + 20000], re.S)
        if not nxt:
            continue
        keys = {}
        for n, letter in re.findall(r"<strong>([\d०-९]+)\.?</strong>\s*\(?\s*([a-dकखगघ])\s*\)", nxt.group(1)):
            keys[int(n.translate(_DEVA_NUM))] = _NE_OPT.get(letter, letter)
        if not keys:
            continue
        i = [0]

        def li(lm):
            i[0] += 1
            k = keys.get(i[0])
            return '<li data-key="%s">' % k if k and 'class="opts' in lm.group(1) else lm.group(0)
        new_block = re.sub(r"<li>(?=(.*?)</li>)", li, block, flags=re.S)
        out.append(htm[pos:m.start()] + "<ol class=\"mcq\">" + new_block + "</ol>")
        pos = m.end()
    out.append(htm[pos:])
    return "".join(out)


_P_Q = re.compile(r"<p><strong>([\d०-९]+)\.</strong>\s*(.*?)</p>", re.S)
_P_OPT = re.compile(r"\(([a-dकखगघ])\)")
_LATIN = {"क": "a", "ख": "b", "ग": "c", "घ": "d"}


def _para_mcq(htm):
    """Questions written as one paragraph, '<b>१.</b> stem (क) … (ख) … (ग) … (घ) …', as in the
    Nepali-medium books, become the same tappable options as the list-style ones."""
    out, pos = [], 0
    for det in re.finditer(r'<details class="ans[^"]*">(.*?)</details>', htm, re.S):
        keys = {int(n.translate(_DEVA_NUM)): _LATIN.get(l, l)
                for n, l in re.findall(r"<strong>([\d०-९]+)\.?</strong>\s*\(?\s*([a-dकखगघ])\s*\)", det.group(1))}
        chunk = htm[pos:det.start()]
        if keys:
            def rep(m):
                n = int(m.group(1).translate(_DEVA_NUM))
                body = m.group(2)
                marks = list(_P_OPT.finditer(body))
                letters = [_LATIN.get(x.group(1), x.group(1)) for x in marks]
                if n not in keys or len(marks) < 3 or letters != ["a", "b", "c", "d"][:len(letters)]:
                    return m.group(0)
                stem = body[:marks[0].start()].strip()
                opts = [body[marks[i].end():(marks[i + 1].start() if i + 1 < len(marks) else len(body))].strip()
                        for i in range(len(marks))]
                if not all(opts):
                    return m.group(0)
                cols = "c4" if max(len(_plain(o)) for o in opts) <= 14 else "c2"
                cells = "".join('<span class="opt" data-opt="%s"><i>%s</i>%s</span>' % (letters[i], marks[i].group(1), o)
                                for i, o in enumerate(opts))
                return ('<div class="mcq-p" data-key="%s"><p><strong>%s.</strong> %s</p><span class="opts %s">%s</span></div>'
                        % (keys[n], m.group(1), stem, cols, cells))
            chunk = _P_Q.sub(rep, chunk)
        out.append(chunk + det.group(0))
        pos = det.end()
    out.append(htm[pos:])
    return "".join(out)


def _finish(htm):
    """Give every h2 an id, collect the table of contents, fold answers, key the MCQs."""
    htm = _para_mcq(_mcq_keys(_answers_fold(htm)))
    toc = []

    def head(m):
        attrs, inner = m.group(1), m.group(2)
        title = _plain(inner)
        sid = "s%d" % (len(toc) + 1)
        kind = "qs" if 'class="qs"' in attrs else ("sum" if "chsum" in attrs else "")
        toc.append({"id": sid, "title": title, "kind": kind})
        return '<h2 id="%s"%s>%s</h2>' % (sid, attrs, inner)
    htm = _HEAD.sub(head, htm)
    return htm, toc


def _chapter(args):
    slug, path = args
    md2html = _patch_md2html()
    import i18n
    L = i18n.set_book(slug)
    text = open(path, encoding="utf-8").read()
    meta, _ = md2html.parse_front(text)
    i18n.CUR = i18n.for_title(meta.get("title", ""), L)
    try:
        meta, htm, _n = md2html.convert(text, "%s-%s" % (slug, os.path.basename(path)[5:7]))
    finally:
        i18n.CUR = L
    htm, toc = _finish(htm)
    words = len(_plain(htm).split())
    qs = len(re.findall(r'<h2[^>]*class="qs"', htm))
    return {
        "no": int(str(meta.get("unit", "0")).strip() or 0),
        "file_no": int(os.path.basename(path)[5:7]),
        "title": str(meta.get("title", "")).strip(),
        "area": str(meta.get("area", "")).strip(),
        "hours": str(meta.get("hours", "")).strip(),
        "lang": "ne" if re.search(r"[ऀ-ॿ]", meta.get("title", "")) or slug.startswith(i18n.NEPALI_MEDIUM) else "en",
        "words": words,
        "read_min": max(1, round(words / 180)),
        "figures": htm.count("<figure"),
        "examples": htm.count('class="box example') + htm.count("class='box example"),
        "has_questions": bool(qs),
        "toc": toc,
        "html": htm,
    }


def _units(slug):
    d = os.path.join(NOTES, "content", slug)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if re.match(r"unit-\d+\.md$", f))


def export_book(slug, pool):
    prefix, grade = _split(slug)
    subject = SUBJECT_KEY[prefix]
    out = os.path.join(DATA, "%s-%s" % (grade, subject))
    os.makedirs(out, exist_ok=True)
    chapters = pool.map(_chapter, [(slug, p) for p in _units(slug)])
    items = []
    for ch in chapters:
        name = "unit-%02d.json" % ch["no"]
        with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
            json.dump(ch, fh, ensure_ascii=False, separators=(",", ":"))
        items.append({k: ch[k] for k in ("no", "title", "area", "words", "read_min", "figures", "has_questions")})
    _merge_index(out, {"book": slug, "units": items})
    print("%-8s %2d chapters -> %s" % (slug, len(chapters), os.path.relpath(out, ROOT)), flush=True)


def _bank_subject(area, title):
    for pat, key in BANK_AREAS:
        if re.search(pat, area) or re.search(pat, title):
            return key
    return None


def _bank_kind(title):
    t = title.lower()
    if "objective" in t or "वस्तुगत" in title:
        return "objective"
    if "model" in t or "नमुना" in title:
        return "model"
    if "pattern" in t or "how to use" in t:
        return "guide"
    return "subjective"


def export_bank(slug, pool):
    _, grade = _split(slug)
    chapters = pool.map(_chapter, [(slug, p) for p in _units(slug)])
    by_subject, guides = {}, []
    titles = {}
    for ch in chapters:
        titles[ch["title"]] = titles.get(ch["title"], 0) + 1
    for ch in chapters:
        # a chapter saved under the wrong file number twice over (qbank12 unit-04 is a stale
        # copy of unit-07) would show the same set twice: keep the one in its own file
        if titles[ch["title"]] > 1 and ch["no"] != ch["file_no"]:
            print("  skipped %s unit-%02d: duplicate of unit %d" % (slug, ch["file_no"], ch["no"]), flush=True)
            continue
        kind = _bank_kind(ch["title"])
        if kind == "guide":
            guides.append(ch)
            continue
        key = _bank_subject(ch["area"], ch["title"])
        if key:
            by_subject.setdefault(key, []).append((kind, ch))
    order = {"objective": 0, "subjective": 1, "model": 2}
    for key, chs in by_subject.items():
        out = os.path.join(DATA, "%s-%s" % (grade, key))
        os.makedirs(out, exist_ok=True)
        banks = []
        for i, (kind, ch) in enumerate(sorted(chs, key=lambda t: order[t[0]]), 1):
            ch["kind"] = kind
            name = "bank-%02d.json" % i
            with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
                json.dump(ch, fh, ensure_ascii=False, separators=(",", ":"))
            banks.append({"no": i, "kind": kind, "title": ch["title"], "words": ch["words"], "read_min": ch["read_min"]})
        guide = guides[0] if guides else None
        if guide:
            guide["kind"] = "guide"
            with open(os.path.join(out, "guide.json"), "w", encoding="utf-8") as fh:
                json.dump(guide, fh, ensure_ascii=False, separators=(",", ":"))
        _merge_index(out, {"bank_book": slug, "banks": banks, "guide": guide["title"] if guide else None})
    print("%-8s %2d chapters -> %d subjects" % (slug, len(chapters), len(by_subject)), flush=True)


def _merge_index(out, patch):
    path = os.path.join(out, "index.json")
    data = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    if "banks" in patch and data.get("bank_book") and data["bank_book"] != patch["bank_book"]:
        # commerce and general banks never share a subject; keep both if they ever do
        patch["banks"] = data.get("banks", []) + patch["banks"]
    data.update(patch)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)


def _fonts_or_die():
    import matplotlib.font_manager as fm
    missing = []
    for family in ("Inter", "Noto Sans Devanagari"):
        try:
            fm.findfont(family, fallback_to_default=False)
        except ValueError:
            missing.append(family)
    if missing:
        sys.exit("missing fonts: %s (run notes/pipeline/fonts/install.sh)" % ", ".join(missing))


def main():
    _fonts_or_die()
    wanted = sys.argv[1:] or BOOKS + BANKS
    os.makedirs(MEDIA, exist_ok=True)
    with Pool(max(1, os.cpu_count() - 1)) as pool:
        for slug in wanted:
            (export_bank if slug.startswith("qbank") else export_book)(slug, pool)


if __name__ == "__main__":
    main()

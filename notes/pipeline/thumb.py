#!/usr/bin/env python3
"""Library thumbnails: one 16:9 JPEG (1280 x 720) per book, same look as the printed cover.

The first page of a book is portrait (A4); the library and app cards are 16:9 with object-fit: cover,
so a page thumbnail was cropped to a slice of the title. This draws the cover again at card shape:
flat accent field, M3E shapes in tonal steps (m3x.thumb_art), grade chip, title, NEBians lockup.
Safe area: the card puts its PDF badge at the top-left and a price badge at the top-right, and
rounds the corners, so text sits in the lower-left, 80 px from the edges, and 110 px below the top.

    python thumb.py                 # every book -> tools/publish/covers/<slug>.jpg
    python thumb.py math11 cs8      # some books
    python thumb.py --out DIR       # another directory

Needs weasyprint, pymupdf, pillow and the fonts of fonts/install.sh. Pure function of the spine and
the BCA registry: it never opens a PDF, so it does not drift when a book is rebuilt.
"""
import html, json, os, re, sys
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import i18n, m3x, spine  # noqa: E402

W, H = 1280, 720
OUT = os.path.join(REPO, "tools", "publish", "covers")
COURSE_PREFIX = "bca-course-"
PAPER_OUT = os.path.join(REPO, "tools", "publish", "paper_covers")
ENG_CONTENT = os.path.join(REPO, "notes", "papers", "engineering", "content")
TEXT_W = 700            # title column; the art owns everything to the right of it
FONT_DIRS = [os.path.expanduser("~/.local/share/fonts"), "/usr/share/fonts", os.path.expanduser("~/.fonts")]


def esc(s):
    return html.escape(str(s))


# ------------------------------------------------------------------ metadata
def course_registry():
    reg = json.load(open(os.path.join(REPO, "bca", "course", "books.json"), encoding="utf-8"))
    return {COURSE_PREFIX + rel.replace("/", "-"): meta for rel, meta in reg.items() if not rel.startswith("_")}


def course_slugs():
    return list(course_registry())


_ENG_CACHE = {}
# Discipline to accent, using the same hexes spine.SUBJECTS gives the school books, so an engineering
# paper sits in the same colour family as the subject chip it belongs to everywhere else.
ENG_ACCENTS = (
    ("mathematics", "#8F5507"), ("physics", "#4A42D6"), ("chemistry", "#A8271F"),
    ("computer", "#2E4057"), ("programming", "#2E4057"), ("data", "#2E4057"),
    ("electronic", "#0F766E"), ("electrical", "#0F766E"), ("instrumentation", "#0F766E"),
    ("civil", "#2F6B3A"), ("building", "#2F6B3A"), ("survey", "#2F6B3A"), ("transportation", "#2F6B3A"),
    ("mechanical", "#475569"), ("workshop", "#475569"), ("thermodynamics", "#475569"),
    ("fluid", "#0F766E"), ("geology", "#475569"), ("engineering drawing", "#8F5507"),
    ("english", "#6B3FA0"), ("communication", "#6B3FA0"),
    ("management", "#C2410C"), ("economics", "#C2410C"), ("account", "#9D174D"),
)
GRADE_CHIP = {"8": "Class 8", "9": "Class 9", "10": "Class 10", "11": "Class 11", "12": "Class 12"}
ENG_FALLBACK = ("#4A42D6", "#0B6A62", "#8F5507", "#9D174D", "#2E4057", "#C2410C")
NEB_CONTENT = os.path.join(REPO, "notes", "papers", "content")
NEB_PREFIX = ""


def _front_matter(path):
    meta, inside = {}, False
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.rstrip("\n")
            if i == 0 and line.strip() == "---":
                inside = True
                continue
            if inside and line.strip() == "---":
                break
            if inside and ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta


def _slug_meta(directory):
    out = {}
    if not os.path.isdir(directory):
        return out
    for name in sorted(os.listdir(directory)):
        if name.endswith(".md"):
            meta = _front_matter(os.path.join(directory, name))
            meta["slug"] = name[:-3]
            out[name[:-3]] = meta
    return out


def _paper_accent(meta):
    sub = (meta.get("subject") or "").lower()
    for key, hexcode in ENG_ACCENTS:
        if key in sub:
            return hexcode
    return ENG_FALLBACK[int(hashlib.md5(meta.get("slug", "").encode()).hexdigest(), 16) % len(ENG_FALLBACK)]


def engineering_papers():
    """Every authored engineering paper: paper id -> front matter of its content file.

    The papers live in notes/papers/engineering/content as authored markdown (front matter plus the
    questions), so the thumbnail is a pure function of that file, never of the built PDF.
    """
    if not _ENG_CACHE:
        _ENG_CACHE.update(_slug_meta(ENG_CONTENT))
    return _ENG_CACHE


_NEB_CACHE = {}


def school_papers():
    """The NEB board papers the same way: id -> front matter of notes/papers/content/<id>.md."""
    if not _NEB_CACHE:
        _NEB_CACHE.update(_slug_meta(NEB_CONTENT))
    return _NEB_CACHE


def engineering_accent(meta):
    return _paper_accent(meta)


def all_slugs():
    return list(spine.ALL) + course_slugs()


def book_meta(slug):
    """dict(subject, accent, chips, nepali) for any slug (school, entrance, BCA course or paper)."""
    eng = engineering_papers()
    neb = school_papers()
    if slug in neb:
        m = neb[slug]
        grade = str(m.get("grade", "")).strip()
        label = GRADE_CHIP.get(grade, "Class " + grade if grade else "")
        chips = [label, m.get("year_bs", "")]
        return dict(subject=m.get("subject", slug), accent=_paper_accent(m),
                    chips=[c for c in chips if c][:2], nepali=False)
    if slug in eng:
        m = eng[slug]
        chips = [m.get("code", ""), m.get("year_bs", "")]
        return dict(subject=m.get("subject", slug), accent=engineering_accent(m),
                    chips=[c for c in chips if c][:2], nepali=False)
    if slug.startswith(COURSE_PREFIX):
        m = course_registry()[slug]
        return dict(subject=m["name"], accent=m["accent"], nepali=False,
                    chips=[f"Semester {m['semester']}", "BCA"])
    L = i18n.set_book(slug)
    subject, accent, grade = spine.meta_for(slug)
    track, _ = spine.track_of(slug)
    if track:
        second = "प्रवेश परीक्षा" if L["digits"] else "Entrance"
        chips = [str(grade), second]
    else:
        chips = [p.strip() for p in L["grade"].format(g=i18n.num(grade)).split(" · ")]
    return dict(subject=subject, accent=accent, chips=chips[:2], nepali=bool(L["digits"]))


# ------------------------------------------------------------------ text fitting
_fonts = {}


def _font_file(names):
    for d in FONT_DIRS:
        for root, _, files in os.walk(d):
            for f in files:
                if f in names:
                    return os.path.join(root, f)
    return None


def _measure(text, size, nepali):
    from PIL import ImageFont
    key = (nepali, size)
    if key not in _fonts:
        path = _font_file(["NotoSansDevanagari[wdth,wght].ttf", "NotoSansDevanagari-Bold.ttf"] if nepali
                          else ["Poppins-Bold.ttf"])
        _fonts[key] = ImageFont.truetype(path, size) if path else None
    f = _fonts[key]
    return (f.getlength(text) if f else len(text) * size * .62) * (1.04 if nepali else 1.0)


def _lines(text, size, nepali):
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if cur and _measure(t, size, nepali) > TEXT_W:
            out.append(cur)
            cur = w
        else:
            cur = t
    out.append(cur)
    return out


def tie(text):
    """Keep a short last word (II, IT, of) with the word before it: no orphan line."""
    return re.sub(r" (\S{1,3})$", "\u00a0\\1", text)


def fit_title(text, nepali):
    """Largest size whose wrapped title stays within 3 lines and 330 px, and no word is cut."""
    for size in (104, 96, 88, 80, 72, 66, 60, 54, 48):
        ln = _lines(text, size, nepali)
        longest = max(_measure(x, size, nepali) for x in ln)
        if len(ln) <= (2 if size >= 96 else 3) and longest <= TEXT_W and len(ln) * size * 1.1 <= 330:
            return size
    return 44


# ------------------------------------------------------------------ the page
def thumb_html(slug):
    m = book_meta(slug)
    m["subject"] = tie(m["subject"])
    t = m3x.tones(m["accent"])
    size = fit_title(m["subject"], m["nepali"])
    chips = "".join(f'<span class="chip{" solid" if i == 0 else ""}">{esc(c)}</span>' for i, c in enumerate(m["chips"]))
    brand = "नेबियन्स" if m["nepali"] else "NEBians"
    deva = ('.chip,h1,.lockup span{font-family:"Noto Sans Devanagari",Poppins,sans-serif!important;'
            'letter-spacing:normal!important;text-transform:none!important}') if m["nepali"] else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page{{size:{W}px {H}px;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
.t{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{t["cover"]};color:#fff;font-family:Poppins,sans-serif}}
.col{{position:absolute;left:80px;bottom:176px;width:{TEXT_W}px}}
.chips{{display:flex;gap:12px}}
.chip{{display:inline-block;font-weight:500;font-size:33px;line-height:1;padding:16px 30px;border-radius:999px;background:{t["cover_hi"]};color:#fff}}
.chip.solid{{background:#fff;color:{t["cover"]};font-weight:600}}
h1{{margin:30px 0 0;font-weight:700;font-size:{size}px;line-height:1.1;letter-spacing:-.02em;color:#fff}}
.lockup{{position:absolute;left:80px;bottom:72px;display:flex;align-items:center;background:#fff;color:{t["cover"]};border-radius:999px;padding:12px 30px 12px 20px;font-weight:700;font-size:25px;letter-spacing:.06em;text-transform:uppercase}}
.lockup svg{{margin-right:14px}}
{deva}
</style></head><body><div class="t">{m3x.thumb_art(slug, m["accent"], W, H)}
<div class="col"><div class="chips">{chips}</div><h1>{esc(m["subject"])}</h1>
</div>
<div class="lockup">{m3x.mark_svg(t["cover"], 10.4)}<span>{brand}</span></div></div></body></html>"""


def render(slug, out_dir=OUT, quality=88):
    import fitz
    from weasyprint import HTML
    os.makedirs(out_dir, exist_ok=True)
    pdf = HTML(string=thumb_html(slug), base_url=HERE).write_pdf()
    page = fitz.open(stream=pdf, filetype="pdf")[0]
    k = W / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)
    path = os.path.join(out_dir, slug + ".jpg")
    pix.save(path, jpg_quality=quality)
    return path, pix.width, pix.height


def main(argv):
    out = OUT
    if "--out" in argv:
        i = argv.index("--out")
        out = os.path.abspath(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if "--papers" in argv:
        argv = [a for a in argv if a != "--papers"]
        out = out if out != OUT else PAPER_OUT
        slugs = argv or list(school_papers())
    elif "--engineering" in argv:
        argv = [a for a in argv if a != "--engineering"]
        out = out if out != OUT else PAPER_OUT
        slugs = argv or list(engineering_papers())
    else:
        slugs = argv or all_slugs()
    missing = [s for s in slugs if s not in engineering_papers() and s not in school_papers()
               and s not in spine.ALL and s not in course_registry()]
    if missing:
        print("unknown slugs:", " ".join(missing[:5]), file=sys.stderr)
        return 1
    for s in slugs:
        path, w, h = render(s, out)
        print(f"{s:52s} {w}x{h} {os.path.getsize(path) // 1024} KB", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

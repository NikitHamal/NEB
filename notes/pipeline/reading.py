"""Reading payload: the book as structure, carried inside its own PDF.

The Android reader used to rebuild paragraphs, tables, choices and maths from the drawn PDF page
(guessing from glyph positions and outlines). Every guess failed somewhere. The pipeline already has
the real structure, so each built PDF now carries it as an attachment, `neb-reading.tgz`
(a solid gzip tar: formulas share most of their outlines, so it is half the size of a zip; the phone
unpacks it once into its cache and serves the files to the reader page):

    meta.json     {"v": 1, "title", "lang", "accent", "pages", "chapters": [{"id", "no", "title", "area", "page"}]}
    c/<n>.html    chapter n, as typeset
    r/<hash>.svg  pictures (formulas, figures) and r/<hash>.jpg (photos), shared by every chapter

Each chapter html is the chapter exactly as it was typeset (same classes: .box, .opts/.opt, .fxs, .dv, tables,
figures) with three changes for a phone:

* every block carries `data-pg`, the PDF page it landed on (found from WeasyPrint's anchors), so
  the reader can show "Page N of M", jump from the page slider and open the original page;
* a picture is `<img src="r/<hash>.svg" ...>` (the bytes live once in `r/`) with its size, so layout does not
  jump while it loads; a typeset formula is sized in `em` relative to the body text and keeps its
  TeX in `data-tex` (screen readers, copy, search);
* nothing else is rewritten. The reader (`app/src/main/assets/reader/`) styles those classes.

Flow in `build_pdf.build`: `anchor()` the chapter html before typesetting (ids only, no layout change),
render, read the page of each anchor, `chapter()` to produce the payload, `attach()` into the file.
"""
import base64
import tarfile
import hashlib
import html as _html
import io
import json
import os
import re
import struct
from html.parser import HTMLParser

BODY_PT = 10.7            # body size in the print theme; formulas are sized relative to it
PT_PER_MM = 72.0 / 25.4
NAME = "neb-reading.tgz"
VERSION = 1

TEX = {}                  # svg data uri -> the TeX it was typeset from (filled by md2html)

_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
         "track", "wbr"}
_ANCHOR_TAGS = {"p", "li", "figure", "table", "div", "ol", "ul", "h2", "h3", "h4", "h5", "pre",
                "section", "blockquote", "span"}
# depth 1 = a direct child of the chapter section; depth 2 only inside these containers
_DEEP_PARENTS = {"div", "section", "ol", "ul"}


def _attrs(attrs):
    return "".join(f' {k}' if v is None else f' {k}="{_html.escape(v, quote=True)}"'
                   for k, v in attrs)


class _Anchor(HTMLParser):
    """Adds an id and a `data-pg` placeholder to blocks (depth 1 and list items / cards)."""

    def __init__(self, prefix):
        super().__init__(convert_charrefs=False)
        self.out, self.stack, self.n, self.prefix, self.ids = [], [], 0, prefix, []

    def _start(self, tag, attrs, end):
        d = len(self.stack)                        # 0 = the chapter section itself
        a = list(attrs)
        names = {k for k, _ in a}
        parent = self.stack[-1] if self.stack else ""
        want = (d == 1 and tag in _ANCHOR_TAGS) or \
               (d == 2 and tag in {"li", "p", "figure", "table"} and parent in _DEEP_PARENTS)
        if want and "data-pg" not in names:
            ident = dict(a).get("id")
            if not ident:
                self.n += 1
                ident = f"{self.prefix}{self.n}"
                a.append(("id", ident))
            self.ids.append(ident)
            a.append(("data-pg", ident))
        self.out.append(f"<{tag}{_attrs(a)}{' /' if end else ''}>")
        if not end and tag not in _VOID:
            self.stack.append(tag)

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, True)

    def handle_endtag(self, tag):
        if tag in _VOID:
            return
        if self.stack and tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        self.out.append(data)

    def handle_entityref(self, name):
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        self.out.append(f"&#{name};")

    def handle_comment(self, data):
        pass


def anchor(html, prefix):
    """-> (html with block ids, [ids in order]). Layout of the PDF does not change."""
    p = _Anchor(prefix)
    p.feed(html)
    p.close()
    return "".join(p.out), p.ids


# ------------------------------------------------------------------ pictures

_IMG = re.compile(r"<img\b([^>]*?)/?>", re.S)
_ATTR = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
_SVGSIZE = re.compile(r'<svg\b[^>]*?\bwidth="([\d.]+)(pt|px)?"[^>]*?\bheight="([\d.]+)(pt|px)?"', re.S)
_VIEWBOX = re.compile(r'viewBox="[\d.\-]+[ ,]+[\d.\-]+[ ,]+([\d.]+)[ ,]+([\d.]+)"')


def _svg_size(svg):
    m = _SVGSIZE.search(svg)
    if m:
        return float(m.group(1)), float(m.group(3))
    m = _VIEWBOX.search(svg)
    return (float(m.group(1)), float(m.group(2))) if m else (0.0, 0.0)


def _raster(path):
    """A photo as a JPEG data URI no wider than 1100 px, and its size."""
    from PIL import Image
    im = Image.open(path)
    im.load()
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if im.width > 1100:
        im = im.resize((1100, round(im.height * 1100 / im.width)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)
    return buf.getvalue(), im.width, im.height


class Pictures:
    """Shared resource table: one entry per distinct picture."""

    def __init__(self):
        self.res, self.size, self._seen = {}, {}, {}      # res: file name -> bytes

    def put(self, src):
        """-> (resource id, width, height) or None when the source cannot be read."""
        if src in self._seen:
            return self._seen[src]
        got = None
        try:
            if src.startswith("data:image/svg+xml;base64,"):
                raw = base64.b64decode(src.split(",", 1)[1])
                w, h = _svg_size(raw.decode("utf-8", "replace"))
                got = (raw, "svg", w, h)
            elif src.startswith("file://") or os.path.exists(src):
                raw, w, h = _raster(src[7:] if src.startswith("file://") else src)
                got = (raw, "jpg", w, h)
        except Exception:
            got = None
        if not got:
            self._seen[src] = None
            return None
        data, ext, w, h = got
        rid = hashlib.sha1(data).hexdigest()[:12] + "." + ext
        self.res[rid] = data
        self.size[rid] = (w, h)
        self._seen[src] = (rid, w, h)
        return self._seen[src]


def _img(m, pics):
    a = dict(_ATTR.findall(m.group(1)))
    src = _html.unescape(a.get("src", ""))
    got = pics.put(src)
    if not got:
        return ""
    rid, w, h = got
    cls = a.get("class", "")
    tex = _html.escape(TEX.get(src, "") or _html.unescape(a.get("data-t", "")), quote=True)
    out = [f'<img src="r/{rid}"']
    if cls:
        out.append(f' class="{cls}"')
    if a.get("alt") == "math" or "data-w" in a:
        # typeset maths: size in em of the body text (print: 10.7 pt), baseline from the print style
        if w and h:
            wem, hem = w / BODY_PT, h / BODY_PT
        else:
            wem = float(a.get("data-w", "0") or 0) * PT_PER_MM / BODY_PT
            hem = 0.0
        va = re.search(r"vertical-align:\s*(-?[\d.]+)pt", a.get("style", ""))
        vem = (float(va.group(1)) / BODY_PT) if va else 0.0
        st = f"width:{wem:.3f}em;"
        if hem:
            st += f"aspect-ratio:{w:.2f}/{h:.2f};"
        if va:
            st += f"vertical-align:{vem:.3f}em;"
        out.append(f' style="{st}"')
        if tex:
            out.append(f' data-tex="{tex}" alt="{tex}"')
        else:
            out.append(' alt="formula"')
    else:
        st = a.get("style", "")
        if w and h:
            st += f";aspect-ratio:{w:.2f}/{h:.2f}"
        out.append(f' style="{st.strip(";")}"' if st.strip(";") else "")
        out.append(f' alt="{a.get("alt", "figure")}"')
    out.append(">")
    return "".join(out)


def chapter(html, pages, pics):
    """Anchored print html -> reading html. `pages` maps an anchor id to its 1-based page."""
    html = _IMG.sub(lambda m: _img(m, pics), html)
    html = re.sub(r'data-pg="([^"]+)"',
                  lambda m: f'data-pg="{pages.get(m.group(1), 0)}"', html)
    html = re.sub(r"\s+(?:style|class)=\"\"", "", html)
    return html


# ------------------------------------------------------------------ payload

def attach(pdf_path, title, lang, accent, page_count, chapters, pics):
    """Write the payload into the PDF as an embedded zip (no change to pages). -> bytes written."""
    from pypdf import PdfWriter
    meta = {"v": VERSION, "title": title, "lang": lang, "accent": accent, "pages": page_count,
            "chapters": [{k: c[k] for k in ("id", "no", "title", "area", "page")} for c in chapters]}
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz", format=tarfile.USTAR_FORMAT, compresslevel=9) as t:
        def add(name, data):
            ti = tarfile.TarInfo(name)
            ti.size, ti.mtime = len(data), 0
            t.addfile(ti, io.BytesIO(data))
        add("meta.json", json.dumps(meta, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        for i, c in enumerate(chapters):
            add(f"c/{i}.html", c["html"].encode("utf-8"))
        for name, data in pics.res.items():
            add(f"r/{name}", data)
    raw = buf.getvalue()
    w = PdfWriter(clone_from=pdf_path)
    w.add_attachment(NAME, raw)
    try:
        w.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    except Exception:
        pass
    tmp = pdf_path + ".tmp"
    with open(tmp, "wb") as f:
        w.write(f)
    os.replace(tmp, pdf_path)
    return len(raw)

import io
import re


class ToolError(Exception):
    pass


def _require_pdf_sources(sources, count=None):
    pdfs = [s for s in sources if s.get("kind") == "pdf"]
    if not pdfs:
        raise ToolError("Attach a PDF file first, then ask me again.")
    if count is not None and len(pdfs) < count:
        raise ToolError(f"This needs at least {count} PDF files attached.")
    return pdfs


PAGE_SPEC_RE = re.compile(r"(\d+)\s*(?:-|–|to)\s*(\d+)|(\d+)")


def parse_page_ranges(spec, total):
    spec = (spec or "").strip()
    if not spec:
        return list(range(total))
    idx = []
    for m in PAGE_SPEC_RE.finditer(spec):
        a, b, single = m.group(1), m.group(2), m.group(3)
        try:
            if a and b:
                lo, hi = int(a), int(b)
                if lo > hi:
                    lo, hi = hi, lo
            else:
                lo = hi = int(single)
        except Exception:
            continue
        lo = max(1, min(lo, total))
        hi = max(1, min(hi, total))
        idx.extend(range(lo - 1, hi))
    if not idx:
        raise ToolError("Couldn't understand that page range. Use forms like '3', '2-5' or '1-3,7'.")
    seen = []
    for i in idx:
        if i not in seen:
            seen.append(i)
    return sorted(seen)


def t_pdf_info(sources, params):
    from pypdf import PdfReader

    pdfs = _require_pdf_sources(sources)
    lines = []
    for s in pdfs:
        try:
            r = PdfReader(io.BytesIO(s["data"]))
            meta = r.metadata or {}
            enc = " · encrypted" if getattr(r, "is_encrypted", False) else ""
            lines.append(
                f"**{s['name']}** — {len(r.pages)} pages{enc}"
                f" · title: {meta.title or '—'}"
            )
        except Exception as exc:
            lines.append(f"**{s['name']}** — unreadable ({exc})")
    return {"text": "\n".join(lines)}


def t_pdf_merge(sources, params):
    from pypdf import PdfWriter

    pdfs = _require_pdf_sources(sources, count=2)
    writer = PdfWriter()
    try:
        for s in pdfs:
            writer.append(io.BytesIO(s["data"]))
        out = io.BytesIO()
        writer.write(out)
    except Exception:
        raise ToolError("Could not merge those PDFs — one may be corrupted or password protected.")
    return {
        "artifacts": [{"name": "merged.pdf", "mime": "application/pdf", "bytes": out.getvalue()}],
        "text": f"Merged **{len(pdfs)} PDFs** into one document.",
    }


def t_pdf_extract_pages(sources, params):
    from pypdf import PdfReader, PdfWriter

    src = _require_pdf_sources(sources)[0]
    spec = str(params.get("pages") or "")
    r = PdfReader(io.BytesIO(src["data"]))
    idx = parse_page_ranges(spec, len(r.pages))
    if len(idx) >= len(r.pages):
        raise ToolError("That range already covers every page — nothing to extract.")
    writer = PdfWriter()
    for i in idx:
        writer.add_page(r.pages[i])
    out = io.BytesIO()
    writer.write(out)
    label = ", ".join(str(i + 1) for i in idx[:8])
    if len(idx) > 8:
        label += f" (+{len(idx) - 8} more)"
    return {
        "artifacts": [{"name": f"{src['name']}_pages.pdf", "mime": "application/pdf", "bytes": out.getvalue()}],
        "text": f"Extracted **{len(idx)} pages** ({label}) into a new PDF.",
    }


def t_pdf_split(sources, params):
    from pypdf import PdfReader, PdfWriter

    src = _require_pdf_sources(sources)[0]
    try:
        every = max(1, int(params.get("every") or 0))
    except Exception:
        every = 0
    spec = str(params.get("ranges") or "").strip()
    r = PdfReader(io.BytesIO(src["data"]))
    total = len(r.pages)
    groups = []
    if spec:
        marks = parse_page_ranges(spec, total)
        prev = None
        start = None
        for i in marks:
            if prev is None or i != prev + 1:
                if start is not None:
                    groups.append((start, prev))
                start = i
            prev = i
        if start is not None:
            groups.append((start, prev))
    elif every:
        for st in range(0, total, every):
            groups.append((st, min(st + every, total) - 1))
    else:
        raise ToolError("Tell me how to split: pages per part (e.g. '5') or ranges like '1-10,11-20'.")
    artifacts = []
    base = re.sub(r"\.(pdf|PDF)$", "", src["name"]) or "document"
    for gi, (a, b) in enumerate(groups[:24], start=1):
        w = PdfWriter()
        for i in range(a, b + 1):
            w.add_page(r.pages[i])
        buf = io.BytesIO()
        w.write(buf)
        artifacts.append({
            "name": f"{base}_part{gi}_p{a + 1}-{b + 1}.pdf",
            "mime": "application/pdf",
            "bytes": buf.getvalue(),
        })
    note = f" (first 24 of {len(groups)} parts)" if len(groups) > 24 else ""
    return {"artifacts": artifacts, "text": f"Split into **{len(artifacts)} parts**{note}."}


def t_pdf_rotate(sources, params):
    from pypdf import PdfReader, PdfWriter

    src = _require_pdf_sources(sources)[0]
    digits = re.findall(r"(90|180|270)", str(params.get("angle") or "90"))
    angle = int(digits[0]) if digits else 90
    r = PdfReader(io.BytesIO(src["data"]))
    writer = PdfWriter()
    spec = str(params.get("pages") or "")
    targets = (
        set(parse_page_ranges(spec, len(r.pages)))
        if spec and spec.lower() not in ("all", "*")
        else None
    )
    for i, pg in enumerate(r.pages):
        if targets is None or i in targets:
            pg.rotate(angle)
        writer.add_page(pg)
    out = io.BytesIO()
    writer.write(out)
    scope = "all pages" if targets is None else f"{len(targets)} page(s)"
    return {
        "artifacts": [{"name": f"{src['name']}_rotated.pdf", "mime": "application/pdf", "bytes": out.getvalue()}],
        "text": f"Rotated {scope} by **{angle}°**.",
    }


def t_pdf_compress(sources, params):
    import pikepdf

    src = _require_pdf_sources(sources)[0]
    out = io.BytesIO()
    try:
        with pikepdf.open(io.BytesIO(src["data"])) as pdf:
            pdf.save(
                out,
                compress_streams=True,
                object_stream_mode=pikepdf.ObjectStreamMode.generate,
                recompress_flate=True,
            )
    except Exception:
        raise ToolError(f"Could not recompress {src['name']} — it may be corrupted.")
    data = out.getvalue()
    before = len(src["data"])
    pct = 100 - (len(data) * 100 // max(before, 1))
    return {
        "artifacts": [{"name": f"{src['name']}_compressed.pdf", "mime": "application/pdf", "bytes": data}],
        "text": f"Compressed from **{before // 1024} KB** to **{len(data) // 1024} KB** ({pct}% smaller).",
    }


def t_pdf_to_docx(sources, params):
    from .lazypdf import convert_pdf_to_docx

    src = _require_pdf_sources(sources)[0]
    res = convert_pdf_to_docx(src["data"], title=src["name"])
    st = res["stats"]
    bits = [f"**{st['source_pages']} pages** kept 1:1"]
    if st["images"]:
        bits.append(f"{st['images']} image(s) placed at their original positions")
    if st.get("skipped_rotated"):
        bits.append(f"{st['skipped_rotated']} rotated text run(s) skipped")
    if st.get("autofit_pages"):
        bits.append(f"{st['autofit_pages']} dense page(s) auto-fitted")
    base = re.sub(r"\.(pdf|PDF)$", "", src["name"]) or "document"
    name = f"{base}.docx"
    return {
        "artifacts": [{
            "name": name,
            "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "bytes": res["bytes"],
        }],
        "text": "Converted your PDF to an editable Word document with the original layout preserved: "
        + ", ".join(bits) + ". Fonts, colors and pagination match the source.",
    }


IMG_KINDS = ("png", "jpg", "jpeg", "gif", "webp")


def t_pdf_extract_images(sources, params):
    from pypdf import PdfReader

    src = _require_pdf_sources(sources)[0]
    r = PdfReader(io.BytesIO(src["data"]))
    arts = []
    total_bytes = 0
    base = re.sub(r"\.(pdf|PDF)$", "", src["name"]) or "document"
    for pi, page in enumerate(r.pages, start=1):
        if len(arts) >= 12 or total_bytes > 12 * 1024 * 1024:
            break
        try:
            ims = list(page.images)
        except Exception:
            continue
        for k, im in enumerate(ims, start=1):
            if len(arts) >= 12 or total_bytes > 12 * 1024 * 1024:
                break
            try:
                pil = im.image
                buf = io.BytesIO()
                pil.save(buf, format="PNG")
                data = buf.getvalue()
            except Exception:
                continue
            if len(data) < 4096:
                continue
            total_bytes += len(data)
            arts.append({"name": f"{base}_p{pi}_{k}.png", "mime": "image/png", "bytes": data})
    if not arts:
        raise ToolError("No extractable images found in that PDF.")
    return {"artifacts": arts, "text": f"Extracted **{len(arts)} image(s)** from {src['name']}."}


def t_images_to_pdf(sources, params):
    from PIL import Image as PilImage

    imgs = [s for s in sources if s.get("kind") in IMG_KINDS]
    if not imgs:
        raise ToolError("Attach some images (PNG/JPG) first.")
    size_mode = str(params.get("page") or "auto")
    pages_meta = []
    for s in imgs:
        try:
            im = PilImage.open(io.BytesIO(s["data"]))
            im.load()
        except Exception:
            continue
        w_pt = max(im.width * 72.0 / 96.0, 36)
        h_pt = max(im.height * 72.0 / 96.0, 36)
        if size_mode == "a4":
            pages_meta.append((im, 595.27, 841.89, True))
        else:
            pages_meta.append((im, w_pt, h_pt, False))
    if not pages_meta:
        raise ToolError("None of those files could be opened as images.")
    buf = io.BytesIO()
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas as rl_canvas

    c = rl_canvas.Canvas(buf)
    for i, (im, pw, ph, fit) in enumerate(pages_meta):
        if i > 0:
            c.showPage()
        c.setPageSize((pw, ph))
        if fit:
            margin = 24.0
            ratio = min(
                (pw - 2 * margin) / max(im.width, 1),
                (ph - 2 * margin) / max(im.height, 1),
            )
            dw, dh = im.width * ratio, im.height * ratio
            x, y = (pw - dw) / 2.0, (ph - dh) / 2.0
        else:
            x, y, dw, dh = 0, 0, pw, ph
        c.drawImage(ImageReader(im), x, y, width=dw, height=dh, mask="auto")
    c.showPage()
    c.save()
    return {
        "artifacts": [{"name": "images.pdf", "mime": "application/pdf", "bytes": buf.getvalue()}],
        "text": f"Built a **{len(pages_meta)}-page PDF** from your images.",
    }


def _plain_text_of(sources, params):
    txt = str(params.get("text") or "").strip()
    if txt:
        return txt, None
    from .lazy_io import extract_docx, extract_pdf_text

    kinds = ("txt", "docx", "pdf")
    src = next((s for s in sources if s.get("kind") in kinds), None)
    if src is None:
        return None, None
    kind = src["kind"]
    if kind == "docx":
        html, _t = extract_docx(src["data"])
        plain = re.sub(r"<[^>]+>", " ", html)
    elif kind == "pdf":
        plain, _t = extract_pdf_text(src["data"])
    else:
        plain = src["data"].decode("utf-8", errors="replace")
    return plain, src["name"]


def t_word_count(sources, params):
    plain, name = _plain_text_of(sources, params)
    if not plain or not plain.strip():
        raise ToolError("Attach a file to count words from.")
    words = len(plain.split())
    chars = len(plain)
    read_min = max(1, round(words / 200))
    label = f" for **{name}**" if name else ""
    return {"text": f"{label}: **{words:,}** words · {chars:,} characters · ~{read_min} min read."}


REGISTRY = [
    {
        "id": "pdf_to_docx",
        "label": "PDF → Word",
        "icon": "picture_as_pdf",
        "desc": "Pixel-faithful PDF to editable DOCX. Keeps pages, fonts, colors and images in place.",
        "inputs": {"kinds": ["pdf"], "min": 1, "max": 1},
        "params": [],
    },
    {
        "id": "pdf_merge",
        "label": "Merge PDFs",
        "icon": "merge_type",
        "desc": "Combine multiple PDFs into one file, in the order you attach them.",
        "inputs": {"kinds": ["pdf"], "min": 2, "max": 6},
        "params": [],
    },
    {
        "id": "pdf_extract_pages",
        "label": "Extract Pages",
        "icon": "content_cut",
        "desc": "Pull a range of pages out into a new PDF (e.g. 2-5,8).",
        "inputs": {"kinds": ["pdf"], "min": 1, "max": 1},
        "params": [{"key": "pages", "type": "text", "label": "Pages", "placeholder": "e.g. 2-5,8"}],
    },
    {
        "id": "pdf_split",
        "label": "Split PDF",
        "icon": "call_split",
        "desc": "Split into parts by page count or ranges.",
        "inputs": {"kinds": ["pdf"], "min": 1, "max": 1},
        "params": [
            {"key": "every", "type": "number", "label": "Pages per part", "placeholder": "e.g. 5"},
            {"key": "ranges", "type": "text", "label": "…or ranges", "placeholder": "e.g. 1-10,11-20"},
        ],
    },
    {
        "id": "pdf_rotate",
        "label": "Rotate PDF",
        "icon": "rotate_right",
        "desc": "Rotate all or some pages by 90/180/270 degrees.",
        "inputs": {"kinds": ["pdf"], "min": 1, "max": 1},
        "params": [
            {"key": "angle", "type": "select", "label": "Angle", "options": ["90", "180", "270"]},
            {"key": "pages", "type": "text", "label": "Pages (blank = all)", "placeholder": "e.g. 3-6"},
        ],
    },
    {
        "id": "pdf_compress",
        "label": "Compress PDF",
        "icon": "compress",
        "desc": "Rebuild the PDF with stream compression to shrink file size.",
        "inputs": {"kinds": ["pdf"], "min": 1, "max": 1},
        "params": [],
    },
    {
        "id": "pdf_info",
        "label": "PDF Info",
        "icon": "info",
        "desc": "Page count, title and producer metadata for attached PDFs.",
        "inputs": {"kinds": ["pdf"], "min": 1, "max": 4},
        "params": [],
    },
    {
        "id": "pdf_extract_images",
        "label": "Extract Images",
        "icon": "image_search",
        "desc": "Pull embedded pictures and diagrams out of a PDF as PNG files.",
        "inputs": {"kinds": ["pdf"], "min": 1, "max": 1},
        "params": [],
    },
    {
        "id": "images_to_pdf",
        "label": "Images → PDF",
        "icon": "photo_library",
        "desc": "Turn photos/scans into one PDF, one image per page.",
        "inputs": {"kinds": ["png", "jpg", "jpeg", "gif", "webp"], "min": 1, "max": 12},
        "params": [{"key": "page", "type": "select", "label": "Page size", "options": ["auto", "a4"]}],
    },
    {
        "id": "word_count",
        "label": "Word Count",
        "icon": "functions",
        "desc": "Words, characters and reading time for an attached PDF/DOCX/TXT.",
        "inputs": {"kinds": ["pdf", "docx", "txt"], "min": 0, "max": 1},
        "params": [{"key": "text", "type": "textarea", "label": "…or paste text", "placeholder": "Paste text here"}],
    },
]

_HANDLERS = {
    "pdf_info": t_pdf_info,
    "pdf_merge": t_pdf_merge,
    "pdf_extract_pages": t_pdf_extract_pages,
    "pdf_split": t_pdf_split,
    "pdf_rotate": t_pdf_rotate,
    "pdf_compress": t_pdf_compress,
    "pdf_to_docx": t_pdf_to_docx,
    "pdf_extract_images": t_pdf_extract_images,
    "images_to_pdf": t_images_to_pdf,
    "word_count": t_word_count,
}


def run_tool(tool_id, sources, params):
    handler = _HANDLERS.get((tool_id or "").strip().lower())
    if handler is None:
        raise ToolError(f"Unknown tool '{tool_id}'.")
    return handler(sources or [], params or {})
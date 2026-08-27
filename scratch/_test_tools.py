import io
import os
import sys

sys.path.insert(0, r"F:\NEB\backend_python")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "")
from django.conf import settings

settings.configure(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "uniq"}},
    SECRET_KEY="x",
    ADMIN_API_SALT="test-salt-1234567890",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "api",
        "web",
    ],
    ROOT_URLCONF="nebians.urls",
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
)

import django

django.setup()

from django.core.cache import cache
cache.clear()

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from PIL import Image as PilImage
import io

W, H = A4


def make_pdf(pages=4):
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)
    c.setTitle("Doc Tools Test")
    for p in range(pages):
        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(0, 0.3, 0.8)
        c.drawCentredString(W / 2, H - 60, f"Page {p + 1} Heading")
        c.setFont("Helvetica", 11)
        c.setFillColorRGB(0, 0, 0)
        for i in range(18):
            c.drawString(72, H - 110 - i * 15, f"Content line {i+1} on page {p+1} about displacement and velocity.")
        if p == 0:
            img = PilImage.new("RGB", (180, 110), (120, 40, 200))
            ibuf = io.BytesIO()
            img.save(ibuf, "PNG")
            ibuf.seek(0)
            from reportlab.lib.utils import ImageReader
            c.drawImage(ImageReader(ibuf), 140, 300, width=170, height=100)
        c.showPage()
    c.save()
    return buf.getvalue()


pdf = make_pdf(4)

from web import study_tools, toolstore

# 1. PDF -> DOCX pixel-faithful
r = study_tools.run_tool("pdf_to_docx", [{"name": "a.pdf", "kind": "pdf", "data": pdf}], {})
docx = r["artifacts"][0]["bytes"]
from docx import Document
d = Document(io.BytesIO(docx))
texts = [p.text for p in d.paragraphs]
joined = "\n".join(texts)
assert "Page 1 Heading" in joined, "p1 header"
assert "Page 4 Heading" in joined, "p4 header (pagination)"
assert d.sections[0].page_width / 36000 > 200, "A4 width"
img_rels = [1 for rid, p in d.part.rels.items() if p.reltype.endswith(("image", "image/")) or "image" in str(p.reltype)]
assert img_rels, "image embedded"
assert "<wp:anchor" in d.element.xml, "floating anchor"
print("PASS pdf_to_docx")

# 2. merge two PDFs
pdf2 = make_pdf(2)
r = study_tools.run_tool("pdf_merge", [
    {"name": "a.pdf", "kind": "pdf", "data": pdf},
    {"name": "b.pdf", "kind": "pdf", "data": pdf2},
], {})
from pypdf import PdfReader
mr = PdfReader(io.BytesIO(r["artifacts"][0]["bytes"]))
assert len(mr.pages) == 6, len(mr.pages)
print("PASS pdf_merge ->", len(mr.pages), "pages")

# 3. extract pages 2-3
r = study_tools.run_tool("pdf_extract_pages", [{"name": "a.pdf", "kind": "pdf", "data": pdf}], {"pages": "2-3"})
er = PdfReader(io.BytesIO(r["artifacts"][0]["bytes"]))
assert len(er.pages) == 2
print("PASS pdf_extract_pages")

# 4. split every 2
r = study_tools.run_tool("pdf_split", [{"name": "a.pdf", "kind": "pdf", "data": pdf}], {"every": 2})
assert len(r["artifacts"]) == 2, len(r["artifacts"])
print("PASS pdf_split ->", len(r["artifacts"]), "parts")

# 5. rotate 90
r = study_tools.run_tool("pdf_rotate", [{"name": "a.pdf", "kind": "pdf", "data": pdf}], {"angle": "90", "pages": ""})
rr = PdfReader(io.BytesIO(r["artifacts"][0]["bytes"]))
assert rr.pages[0].rotation == 90, rr.pages[0].rotation
print("PASS pdf_rotate")

# 6. compress
r = study_tools.run_tool("pdf_compress", [{"name": "a.pdf", "kind": "pdf", "data": pdf}], {})
assert r["artifacts"][0]["bytes"]
print("PASS pdf_compress")

# 7. images -> pdf
img = PilImage.new("RGB", (300, 200), (10, 200, 30))
ibuf = io.BytesIO(); img.save(ibuf, "PNG")
r = study_tools.run_tool("images_to_pdf", [{"name": "x.png", "kind": "png", "data": ibuf.getvalue()}], {})
ipdf = PdfReader(io.BytesIO(r["artifacts"][0]["bytes"]))
assert len(ipdf.pages) == 1
print("PASS images_to_pdf")

# 8. info
r = study_tools.run_tool("pdf_info", [{"name": "a.pdf", "kind": "pdf", "data": pdf}], {})
assert "4 pages" in r["text"], r["text"]
print("PASS pdf_info")

# 9. word count
r = study_tools.run_tool("word_count", [], {"text": "hello world this is a test sentence for counting words precisely today"})
assert "words" in r["text"]
print("PASS word_count:", r["text"][:40])

# 10. agent quick-intent router
import web.lazy_agent as la
assert la._quick_intent("convert this pdf to word", ["pdf"]) == ("pdf_to_docx", {})
assert la._quick_intent("convert to docx", ["pdf"])[0] == "pdf_to_docx"
assert la._quick_intent("merge these two pdfs", ["pdf", "pdf"])[0] == "pdf_merge"
assert la._quick_intent("split into 3 parts", ["pdf"])[0] == "pdf_split"
assert la._quick_intent("rotate 180", ["pdf"]) == ("pdf_rotate", {"angle": "180", "pages": ""})
assert la._quick_intent("turn my images into one pdf", ["png", "jpeg"])[0] == "images_to_pdf"
assert la._quick_intent("how many pages", ["pdf"])[0] == "pdf_info"
print("PASS agent quick-intent routing")

# 11. toolstore round-trip with owner check
src_id = toolstore.put_source("u1", "a.pdf", "pdf", pdf)
got = toolstore.get_source(src_id, "u1")
assert got and got["data"] == pdf and got["kind"] == "pdf"
assert toolstore.get_source(src_id, "u2") is None, "owner mismatch must fail"
tok = toolstore.put_artifact("u1", "out.docx", "application/xml", b"hi")
art = toolstore.get_artifact(tok)
assert art and art["data"] == b"hi" and art["owner"] == "u1"
print("PASS toolstore")

print("\nALL TOOL TESTS PASSED")
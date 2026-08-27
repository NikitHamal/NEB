import io
import json

from django.test import TestCase

from api.models import User
from api.utils import now_ms, uuid_str
from web import study_tools, toolstore


def _make_pdf(pages=3):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas as rl_canvas
    from PIL import Image as PilImage

    W, H = A4
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)
    for p in range(pages):
        c.setFont("Helvetica-Bold", 18)
        c.setFillColorRGB(0, 0.3, 0.8)
        c.drawCentredString(W / 2, H - 60, f"Sheet {p + 1}")
        c.setFont("Helvetica", 11)
        c.setFillColorRGB(0, 0, 0)
        for i in range(12):
            c.drawString(72, H - 110 - i * 15, f"Row {i + 1} of page {p + 1}.")
        if p == 0:
            img = PilImage.new("RGB", (160, 100), (90, 40, 190))
            ib = io.BytesIO()
            img.save(ib, "PNG")
            ib.seek(0)
            c.drawImage(ImageReader(ib), 140, 320, width=160, height=100)
        c.showPage()
    c.save()
    return buf.getvalue()


def _pdf(kind="pdf", pages=3):
    return {"name": "sample.pdf", "kind": kind, "data": _make_pdf(pages)}


class LazyToolUnitTests(TestCase):
    def test_pdf_to_docx_preserves_layout(self):
        out = study_tools.run_tool("pdf_to_docx", [_pdf()], {})
        self.assertEqual(len(out["artifacts"]), 1)
        from docx import Document

        d = Document(io.BytesIO(out["artifacts"][0]["bytes"]))
        texts = "\n".join(p.text for p in d.paragraphs)
        self.assertIn("Sheet 1", texts)
        self.assertIn("Sheet 3", texts)  # pagination preserved
        self.assertGreater(d.sections[0].page_width / 36000, 200)  # A4
        self.assertIn("<wp:anchor", d.element.xml)  # floating image

    def test_merge_split_extract_rotate(self):
        two = _make_pdf(2)
        merged = study_tools.run_tool("pdf_merge", [
            {"name": "a.pdf", "kind": "pdf", "data": _make_pdf(3)},
            {"name": "b.pdf", "kind": "pdf", "data": two},
        ], {})
        from pypdf import PdfReader

        self.assertEqual(len(PdfReader(io.BytesIO(merged["artifacts"][0]["bytes"])).pages), 5)

        parts = study_tools.run_tool("pdf_split", [_pdf(4)], {"every": 2})
        self.assertEqual(len(parts["artifacts"]), 2)

        ext = study_tools.run_tool("pdf_extract_pages", [_pdf(4)], {"pages": "2-3"})
        self.assertEqual(len(PdfReader(io.BytesIO(ext["artifacts"][0]["bytes"])).pages), 2)

        rot = study_tools.run_tool("pdf_rotate", [_pdf(4)], {"angle": "90", "pages": ""})
        self.assertEqual(PdfReader(io.BytesIO(rot["artifacts"][0]["bytes"])).pages[0].rotation, 90)

    def test_compress_and_other_tools(self):
        comp = study_tools.run_tool("pdf_compress", [_pdf(3)], {})
        self.assertTrue(comp["artifacts"][0]["bytes"])
        info = study_tools.run_tool("pdf_info", [_pdf(3)], {})
        self.assertIn("3 pages", info["text"])
        wc = study_tools.run_tool("word_count", [], {"text": "one two three four"})
        self.assertIn("4", wc["text"])

    def test_array_helpers(self):
        self.assertEqual(study_tools.parse_page_ranges("2-4", 6), [1, 2, 3])
        self.assertEqual(study_tools.parse_page_ranges("3,5", 6), [2, 4])
        self.assertEqual(study_tools.parse_page_ranges("", 6), [0, 1, 2, 3, 4, 5])

    def test_quick_intent(self):
        from web import lazy_agent

        self.assertEqual(lazy_agent._quick_intent("convert this pdf to word", ["pdf"]), ("pdf_to_docx", {}))
        self.assertEqual(lazy_agent._quick_intent("merge these pdfs", ["pdf", "pdf"]), ("pdf_merge", {}))
        self.assertEqual(lazy_agent._quick_intent("split into 3 parts", ["pdf"]), ("pdf_split", {"ranges": "3", "every": ""}))
        self.assertEqual(lazy_agent._quick_intent("rotate 180", ["pdf"]), ("pdf_rotate", {"angle": "180", "pages": ""}))
        self.assertEqual(lazy_agent._quick_intent("make one pdf from my images", ["png", "jpeg"])[0], "images_to_pdf")
        self.assertEqual(lazy_agent._quick_intent("how many pages", ["pdf"]), ("pdf_info", {}))

    def test_toolstore_ownership(self):
        src = toolstore.put_source("u1", "a.pdf", "pdf", b"\x25PDF-data")
        got = toolstore.get_source(src, "u1")
        self.assertEqual(got["data"], b"\x25PDF-data")
        self.assertIsNone(toolstore.get_source(src, "u2"))
        tok = toolstore.put_artifact("u1", "x.docx", "application/xml", b"abc")
        self.assertEqual(toolstore.get_artifact(tok)["data"], b"abc")
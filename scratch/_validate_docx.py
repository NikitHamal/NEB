import io
import sys
import zipfile

sys.path.insert(0, r"F:\NEB\backend_python")

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from PIL import Image as PilImage

W, H = A4


def make_pdf(pages=4):
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)
    for p in range(pages):
        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(0, 0.3, 0.8)
        c.drawCentredString(W / 2, H - 60, f"Sheet {p + 1}")
        c.setFont("Helvetica", 11)
        c.setFillColorRGB(0, 0, 0)
        for i in range(16):
            c.drawString(72, H - 110 - i * 15, f"Row {i + 1} on page {p + 1} about displacement and velocity.")
        if p == 0:
            img = PilImage.new("RGB", (180, 110), (120, 40, 200))
            ib = io.BytesIO(); img.save(ib, "PNG"); ib.seek(0)
            from reportlab.lib.utils import ImageReader
            c.drawImage(ImageReader(ib), 140, 300, width=170, height=100)
        c.showPage()
    c.save()
    return buf.getvalue()


pdf = make_pdf(4)
from web.lazypdf import convert_pdf_to_docx
res = convert_pdf_to_docx(pdf)
docx = res["bytes"]
print("convert stats:", res["stats"])

# 1. structural open
from docx import Document
d = Document(io.BytesIO(docx))
texts = "\n".join(p.text for p in d.paragraphs)
assert "Sheet 4" in texts, "pagination"
print("structural open OK")

# 2. zip + relationship + XML checks
zin = zipfile.ZipFile(io.BytesIO(docx))
names = zin.namelist()
assert "word/document.xml" in names
assert any("media/" in n for n in names), "media part present"
assert any("word/_rels" in n for n in names), "rels present"

dom = zin.read("word/document.xml").decode("utf-8")
print("anchor count:", dom.count("<wp:anchor"))
print("drawing count:", dom.count("<w:drawing"))

# 3. element ordering check inside first wp:anchor (coarse): posOffset before extent, wrapNone before docPr
import re
anchor = dom.split("<wp:anchor")[1] if "<wp:anchor" in dom else ""
anchor = "<wp:anchor" + anchor
if anchor:
    i_pos = anchor.find("<wp:posOffset")
    i_extent = anchor.find("<wp:extent")
    i_wrap = anchor.find("<wp:wrapNone")
    i_docpr = anchor.find("<wp:docPr")
    # positionH/V come before extent
    assert i_pos != -1 and i_extent != -1 and i_pos < i_extent, "posOffset before extent"
    # wrapNone before docPr
    assert i_wrap != -1 and i_docpr != -1 and i_wrap < i_docpr, "wrap before docPr"
    print("anchor child ordering OK")

# 4. r:embed id resolves to a real relationship target
rels = zin.read([n for n in names if n.endswith("word/_rels/document.xml.rels")][0]).decode("utf-8")
import re as _r
rids = _r.findall(r'r:embed="([^"]+)"', anchor)
for rid in rids:
    assert '<Relationship Id="%s"' % rid in rels, "rId exists in rels: %s" % rid
    m = _r.search(r'<Relationship Id="%s" Type="([^"]+)" Target="([^"]+)"' % rid, rels)
    assert m and "image" in m.group(1), "rels type is image"
    # target file must exist in zip
    target = m.group(2)
    if not target.startswith("http"):
        tpath = "word/" + target
        assert tpath in names, "media target exists: " + tpath
print("r:embed relationships OK")

print("\nDOCX VALIDATION PASSED")

"""Count pages with PyMuPDF, falling back to pure-Python pypdf."""
try:
    import fitz
except ImportError:  # allow lightweight build hosts without the PyMuPDF wheel
    fitz = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


def count(path):
    if fitz is not None:
        with fitz.open(path) as document:
            return document.page_count
    if PdfReader is not None:
        return len(PdfReader(path).pages)
    raise ImportError("Install PyMuPDF (fitz) or pypdf to count PDF pages")

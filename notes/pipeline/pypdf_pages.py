import fitz
def count(path):
    d = fitz.open(path); n = d.page_count; d.close(); return n

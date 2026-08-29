"""Format renderers. Each accepts a normalized spec and returns file bytes."""

from . import docx_renderer, html_preview, pdf_renderer, pptx_renderer, xlsx_renderer
from .docx_renderer import render as render_docx
from .html_preview import render as render_html
from .pdf_renderer import render as render_pdf
from .pptx_renderer import render as render_pptx
from .xlsx_renderer import render as render_xlsx

__all__ = [
    'docx_renderer', 'pptx_renderer', 'xlsx_renderer', 'pdf_renderer', 'html_preview',
    'render_docx', 'render_pptx', 'render_xlsx', 'render_pdf', 'render_html',
]

"""Integration check for figures flowing through every renderer."""

import os
import sys
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')

import django
django.setup()

from web.lazy import docspec, visuals
from web.lazy.renderers import render_docx, render_html, render_pdf

WORK = os.path.join(BASE, 'media', '_figcheck')
os.makedirs(WORK, exist_ok=True)

results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS ' if ok else 'FAIL ') + name + ((' | ' + str(detail)) if detail else ''))


spec_raw = {
    'title': 'Photosynthesis in Higher Plants',
    'doc_type': 'assignment',
    'author': 'Test Student',
    'institution': 'Test School',
    'sections': [
        {
            'heading': 'Introduction',
            'level': 1,
            'blocks': [{'type': 'paragraph', 'text': 'Photosynthesis converts light energy into chemical energy.'}],
        },
        {
            'heading': 'The Light Reactions',
            'level': 1,
            'blocks': [
                {'type': 'paragraph', 'text': 'Light-dependent reactions occur in the thylakoid membrane.'},
                {
                    'type': 'image',
                    'path': 'figures/figure_1_flow.svg',
                    'caption': 'Figure 1: Flow of energy through the light reactions',
                    'width': 85,
                },
            ],
        },
        {
            'heading': 'Observed Rates',
            'level': 1,
            'blocks': [
                {
                    'type': 'image',
                    'path': 'figures/figure_2_chart.png',
                    'caption': 'Figure 2: Oxygen evolution at three light intensities',
                    'width': 80,
                },
            ],
        },
    ],
    'references': [{'text': 'NEB Biology Grade 11, Chapter 13.'}],
}

svg = visuals.build_diagram({
    'kind': 'flow',
    'title': 'Light Reaction Flow',
    'nodes': [
        {'label': 'Photon absorption', 'sub': 'Photosystem II'},
        {'label': 'Water splitting', 'sub': 'O2 released'},
        {'label': 'Electron transport', 'sub': 'Cytochrome b6f'},
        {'label': 'NADPH formation', 'sub': 'Photosystem I'},
    ],
})
png = visuals.build_chart({
    'kind': 'bar',
    'title': 'Oxygen evolution by light intensity',
    'labels': ['Low', 'Medium', 'High'],
    'values': [12.4, 28.9, 41.2],
    'x_label': 'Light intensity',
    'y_label': 'O2 (mL/min)',
})

os.makedirs(os.path.join(WORK, 'figures'), exist_ok=True)
with open(os.path.join(WORK, 'figures', 'figure_1_flow.svg'), 'w', encoding='utf-8') as fh:
    fh.write(svg)
with open(os.path.join(WORK, 'figures', 'figure_2_chart.png'), 'wb') as fh:
    fh.write(png)

check('diagram builds', svg.startswith('<svg'), f'{len(svg)} bytes')
check('chart builds', len(png) > 8000, f'{len(png)} bytes')
check('diagram is valid xml', (lambda: (ET.fromstring(svg), True)[1])())

spec = docspec.normalize_spec(spec_raw)
images_found = sum(
    1 for s in spec['sections'] for b in s['blocks'] if b.get('type') == 'image'
)
check('image blocks survive normalization', images_found == 2, images_found)

html = render_html(spec, base_path=WORK)
check('html embeds image data', html.count('data:image/') == 2, html.count('data:image/'))
check('html has figure markup', html.count('lzdoc-figure') == 2, html.count('lzdoc-figure'))
check('html has captions', 'Figure 1:' in html and 'Figure 2:' in html)

docx = render_docx(spec, base_path=WORK)
check('docx produced', len(docx) > 25000, f'{len(docx)} bytes')
check('docx bigger than text-only', len(docx) > 38000, f'{len(docx)} bytes')

pdf = render_pdf(spec, base_path=WORK)
check('pdf produced', len(pdf) > 4000, f'{len(pdf)} bytes')
check('pdf bigger than text-only', len(pdf) > 15000, f'{len(pdf)} bytes')
check('pdf is a real pdf', pdf[:5] == b'%PDF-', pdf[:5])

with open(os.path.join(WORK, 'out.html'), 'w', encoding='utf-8') as fh:
    fh.write(html)
with open(os.path.join(WORK, 'out.docx'), 'wb') as fh:
    fh.write(docx)
with open(os.path.join(WORK, 'out.pdf'), 'wb') as fh:
    fh.write(pdf)

from web.lazy.renderers import images as imgmod
esc = imgmod.safe_abspath(WORK, '../../etc/passwd')
check('path escape blocked', esc is None, esc)

block = {'type': 'image', 'path': 'figures/figure_1_flow.svg'}
imgmod.block_bytes(block, WORK)
check('svg rasterizes to png', imgmod.rasterize(block) and block.get('mime') == 'image/png',
      block.get('mime'))
check('rasterized png has size', len(block.get('_bytes') or b'') > 5000,
      len(block.get('_bytes') or b''))

# A tall diagram scaled to the text column used to exceed the page frame, and
# ReportLab refuses to place such a flowable — which aborted the whole PDF and
# left the agent with no PDF at all, so it rebuilt the entire document.
TALL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 620" width="120" height="620">
<rect x="4" y="4" width="112" height="612" fill="#EEF3F8" stroke="#3A5A78"/>
<line x1="60" y1="20" x2="60" y2="600" stroke="#3A5A78" stroke-width="2"/>
<circle cx="60" cy="60" r="26" fill="#8FB8D8"/>
<circle cx="60" cy="200" r="26" fill="#8FB8D8"/>
<circle cx="60" cy="340" r="26" fill="#8FB8D8"/>
<circle cx="60" cy="480" r="26" fill="#8FB8D8"/>
<text x="60" y="592" font-size="12" text-anchor="middle" fill="#3A5A78">Stage 4</text>
</svg>"""
os.makedirs(os.path.join(WORK, 'figures'), exist_ok=True)
with open(os.path.join(WORK, 'figures', 'tall.svg'), 'w', encoding='utf-8') as fh:
    fh.write(TALL_SVG)

tall_spec = docspec.normalize_spec({
    'title': 'Tall Figure Fit',
    'doc_type': 'lab_report',
    'sections': [
        {'heading': 'Procedure', 'blocks': [
            {'type': 'paragraph', 'text': 'The apparatus is arranged as shown below.' * 6},
            {'type': 'image', 'path': 'figures/tall.svg', 'caption': 'Figure 1: Tall apparatus'},
        ]},
        {'heading': 'Result', 'blocks': [
            {'type': 'paragraph', 'text': 'The focal length was found to be 15.2 cm.' * 6},
        ]},
    ],
})
try:
    tall_pdf = render_pdf(tall_spec, base_path=WORK)
    check('a tall figure does not abort the pdf', len(tall_pdf) > 3000 and tall_pdf[:5] == b'%PDF-',
          f'{len(tall_pdf)} bytes')
except Exception as exc:
    check('a tall figure does not abort the pdf', False, f'{type(exc).__name__}: {exc}'[:200])

from web.lazy.renderers import pdf_renderer  # noqa: E402
check('figure height is capped to the frame',
      pdf_renderer.MAX_FIGURE_HEIGHT_MM < pdf_renderer.USABLE_HEIGHT_MM,
      f'{pdf_renderer.MAX_FIGURE_HEIGHT_MM} < {pdf_renderer.USABLE_HEIGHT_MM}')
check('usable height matches A4 minus margins',
      abs(pdf_renderer.USABLE_HEIGHT_MM - (297 - 22 - 22)) < 0.01,
      pdf_renderer.USABLE_HEIGHT_MM)

failed = [n for n, ok, _ in results if not ok]
print('\n%d/%d passed' % (len(results) - len(failed), len(results)))
if failed:
    print('FAILED:', ', '.join(failed))
    sys.exit(1)
print('workspace:', WORK)

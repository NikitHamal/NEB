"""Document, slide, spreadsheet and PDF tools.

This is the group the agent reaches for when the user asks for an assignment,
a report, a deck or a data sheet.
"""

import os
import re
from datetime import datetime

from . import docspec, engine, events, sandbox
from .engine_quality import _topic_overlap
from .registry import Param, READ_TOOLS, WRITE_TOOLS
from .renderers import render_docx, render_pdf, render_pptx, render_xlsx
from .tools_shared import _register_artifact, _safe, _save_artifact_bytes


# --------------------------------------------------------------------------
# Documents and presentations
# --------------------------------------------------------------------------

def _register_documents(reg):
    reg.tool(
        name='build_document',
        summary='Run the full document pipeline (research → outline → parallel drafting → critique → render) and return .docx, .pdf and HTML. Use this for any assignment, report, essay, CV or letter.',
        timeout=600,
        risk=WRITE_TOOLS,
        params=[
            Param('title', 'string', 'Document title (optional — derived from the goal if empty)'),
            Param('brief', 'string', 'A precise description of what the document should cover', required=True),
            Param('doc_type', 'string', 'lab_report|assignment|essay|research_paper|project_report|report|cv|letter|notes|thesis|business_report|case_study|article|speech'),
            Param('audience', 'string', 'Who will read this', default=''),
            Param('depth', 'string', 'short|standard|comprehensive|long', default='standard'),
            Param('template', 'string', 'neb_classic|modern|formal|minimal|corporate', default='neb_classic'),
            Param('research', 'boolean', 'Whether to fetch sources from the web', default=True),
            Param('formats', 'array', 'Formats to return. A real list, e.g. ["docx", "pdf"] — never a JSON string. Allowed: docx, pdf, html', default=['docx', 'pdf', 'html']),
            Param('figures', 'boolean', 'Let the pipeline draw and embed its own diagrams/charts', default=True),
        ],
    )(lambda ctx, args: _safe(_build_document, ctx, args))

    reg.tool(
        name='create_document',
        summary='Render a pre-built document spec to .docx. Use build_document unless you already have a full spec.',
        timeout=60,
        risk=WRITE_TOOLS,
        params=[
            Param('spec', 'object', 'A complete document spec (title, sections, blocks, etc.)', required=True),
        ],
    )(lambda ctx, args: _safe(_create_document, ctx, args))

    reg.tool(
        name='create_slides',
        summary='Build a .pptx presentation from a deck spec (title, slides, bullets, notes, tables).',
        timeout=60,
        risk=WRITE_TOOLS,
        params=[
            Param('spec', 'object', 'A deck spec (title, slides, theme, etc.)', required=True),
        ],
    )(lambda ctx, args: _safe(_create_slides, ctx, args))

    reg.tool(
        name='create_spreadsheet',
        summary='Build a styled .xlsx workbook with optional charts.',
        timeout=60,
        risk=WRITE_TOOLS,
        params=[
            Param('spec', 'object', 'A workbook spec (sheets, header, rows, chart)', required=True),
        ],
    )(lambda ctx, args: _safe(_create_spreadsheet, ctx, args))

    reg.tool(
        name='create_pdf',
        summary='Render a document spec to .pdf.',
        timeout=60,
        risk=WRITE_TOOLS,
        params=[
            Param('spec', 'object', 'A document spec', required=True),
        ],
    )(lambda ctx, args: _safe(_create_pdf, ctx, args))

    reg.tool(
        name='save_preview',
        summary='Save HTML to the run workspace as a previewable artifact (also updates the in-app document panel).',
        timeout=10,
        risk=WRITE_TOOLS,
        params=[
            Param('html', 'string', 'HTML content', required=True),
            Param('title', 'string', 'Title for the preview', required=True),
        ],
    )(lambda ctx, args: _safe(_save_preview, ctx, args))


def _already_built(ctx, title, brief):
    """Return the earlier build of this same document, if there is one.

    The agent reads a mediocre critique score as a reason to start over, and
    every rebuild costs a full pipeline while handing the user a *different*
    document. A prompt rule alone did not stop it, so it is enforced here:
    one topic, one build per run.
    """
    key = f'{title} {brief}'.strip()
    if not key:
        return None
    for prior in (ctx.get('_built_documents') or []):
        if _topic_overlap(key, prior.get('key') or '') >= 0.6:
            return prior
    return None


def _build_document(ctx, args):
    brief = args.get('brief') or args.get('description') or args.get('instruction') or ''
    if not brief.strip():
        return {'ok': False, 'error': 'brief is required'}

    title = args.get('title') or ''
    prior = _already_built(ctx, title, brief)
    if prior:
        names = ', '.join(str(a.get('name') or 'file') for a in (prior.get('artifacts') or [])[:4])
        return {
            'ok': True,
            'reused': True,
            'title': prior.get('title') or title,
            'artifacts': prior.get('artifacts') or [],
            'figures': prior.get('figures') or [],
            'wordCount': prior.get('wordCount'),
            'score': prior.get('score'),
            'summary': (
                f'Already built this exact document earlier in the run ({names}). '
                'Rebuilding costs a full pipeline and returns a different document, '
                'so nothing was regenerated — use the files above.'
            ),
        }

    formats_in = args.get('formats') or ['docx', 'pdf', 'html']
    if isinstance(formats_in, str):
        formats_in = [f.strip() for f in formats_in.split(',') if f.strip()]
    formats = [f for f in formats_in if f in ('docx', 'pdf', 'html')] or ['docx', 'pdf', 'html']

    steps_log = ctx.get('steps') or []
    def step(label, detail=''):
        steps_log.append({'label': label, 'detail': detail, 'at': datetime.utcnow().isoformat(timespec='seconds') + 'Z'})
        ctx['on_step'] and ctx['on_step'](label, detail)

    step('Target formats resolved', ', '.join(formats))

    result = engine.build_document(
        user=ctx['user'],
        ctx=ctx,
        title=args.get('title') or '',
        brief=brief,
        doc_type=args.get('doc_type') or '',
        audience=args.get('audience') or '',
        depth=args.get('depth') or 'standard',
        template=args.get('template') or 'neb_classic',
        research_mode=bool(args.get('research', True)),
        output_formats=formats,
        on_step=step,
        visuals_enabled=bool(args.get('figures', True)),
    )

    artifacts = []
    for art in result.get('artifacts') or []:
        full = sandbox.write_file(ctx['run_id'], f'outputs/{art["name"]}', art['bytes'] if isinstance(art['bytes'], (bytes, bytearray)) else (art['bytes'].encode('utf-8') if isinstance(art['bytes'], str) else b''))
        artifacts.append({
            'kind': art['kind'],
            'name': art['name'],
            'mime': art['mime'],
            'path': full['path'],
            'size': full['size'],
            'id': _register_artifact(ctx, full['path'], kind=art['kind'], mime=art['mime'], name=art['name'])['id'],
        })

    for fig in result.get('figures') or []:
        _register_artifact(ctx, fig['rel'], kind='image', mime=fig['mime'], name=fig['name'])

    ctx['doc_html'] = result.get('html') or ''
    if ctx['doc_html']:
        emit = ctx.get('emit')
        if callable(emit):
            try:
                emit(events.doc(result['spec']['title'], ctx['doc_html']))
            except Exception:
                pass

    render_errors = list(result.get('render_errors') or [])
    produced = {str(a.get('name') or '').rsplit('.', 1)[-1].lower() for a in artifacts}
    for fmt in formats:
        if fmt not in produced and not any(e.get('format') == fmt for e in render_errors):
            render_errors.append({'format': fmt, 'error': 'renderer returned nothing'})

    out = {
        'ok': True,
        'title': result['spec']['title'],
        'wordCount': result.get('word_count'),
        'score': result.get('score'),
        'issues': result.get('issues') or [],
        'artifacts': artifacts,
        'renderErrors': render_errors,
        'figures': [
            {'name': f['name'], 'path': f['rel'], 'title': f['title'], 'mime': f['mime']}
            for f in (result.get('figures') or [])
        ],
        'html': result.get('html'),
    }
    if render_errors:
        out['summary'] = 'built but ' + ', '.join(
            f'{e["format"]} failed ({e["error"]})' for e in render_errors
        )[:300]

    ctx.setdefault('_built_documents', []).append({
        'key': f'{title} {brief}'.strip(),
        'title': out['title'],
        'artifacts': artifacts,
        'figures': out['figures'],
        'wordCount': out['wordCount'],
        'score': out['score'],
    })
    return out


# Below this, a hand-written spec is a stub rather than a document. The agent
# cannot tell the difference from a success message alone — it renders a
# 232-word shell with no tables or figures, reads "wrote file", and moves on.
THIN_DOCUMENT_WORDS = 500


def _spec_shape(spec):
    """Measure a spec so the agent sees what it actually rendered."""
    tables = images = 0
    for section in spec.get('sections') or []:
        for block in section.get('blocks') or []:
            if block.get('type') == 'table':
                tables += 1
            elif block.get('type') == 'image':
                images += 1
    return {
        'sections': len(spec.get('sections') or []),
        'tables': tables,
        'figures': images,
        'references': len(spec.get('references') or []),
        'words': docspec.spec_word_count(spec),
    }


def _thin_document_warning(shape):
    """Tell the model when a hand-written spec falls short of the bar.

    Keyed on length alone. Structure is not a safe trigger by itself — a
    2000-word essay legitimately holds no tables, and warning there would
    push the agent into "fixing" a document that was already fine.
    """
    if shape['words'] >= THIN_DOCUMENT_WORDS:
        return ''
    gaps = [f"only {shape['words']} words"]
    if not shape['tables']:
        gaps.append('no data tables')
    if not shape['figures']:
        gaps.append('no figures')
    return ('BELOW STANDARD: ' + ', '.join(gaps)
            + '. If this is an assignment, report or project, use build_document '
              'instead — it researches, drafts, critiques and embeds tables and '
              'diagrams. Only keep a hand-written spec this short if the user '
              'genuinely asked for something brief.')


def _render_spec_artifact(ctx, spec, name, mime, kind, data):
    """Register a rendered spec and report the shape of what was produced."""
    out = _save_artifact_bytes(ctx, name, mime, kind, data)
    shape = _spec_shape(spec)
    out.update({
        'title': spec.get('title') or '',
        'wordCount': shape['words'],
        'sections': shape['sections'],
        'tables': shape['tables'],
        'figures': shape['figures'],
        'references': shape['references'],
    })
    warning = _thin_document_warning(shape)
    if warning:
        out['warning'] = warning
    return out


def _create_document(ctx, args):
    spec = docspec.normalize_spec(args.get('spec') or {})
    bytes_data = render_docx(spec, base_path=sandbox.workspace_path(ctx['run_id'], create=False))
    name = re.sub(r'[^A-Za-z0-9_.-]+', '_', spec['title'])[:60] + '.docx'
    return _render_spec_artifact(ctx, spec, name, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'doc', bytes_data)


def _create_pdf(ctx, args):
    spec = docspec.normalize_spec(args.get('spec') or {})
    bytes_data = render_pdf(spec, base_path=sandbox.workspace_path(ctx['run_id'], create=False))
    name = re.sub(r'[^A-Za-z0-9_.-]+', '_', spec['title'])[:60] + '.pdf'
    return _render_spec_artifact(ctx, spec, name, 'application/pdf', 'pdf', bytes_data)


def _create_slides(ctx, args):
    spec = args.get('spec') or {}
    bytes_data = render_pptx(spec)
    name = re.sub(r'[^A-Za-z0-9_.-]+', '_', str(spec.get('title') or 'presentation'))[:60] + '.pptx'
    return _save_artifact_bytes(ctx, name, 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'slides', bytes_data)


def _create_spreadsheet(ctx, args):
    spec = args.get('spec') or {}
    bytes_data = render_xlsx(spec)
    name = re.sub(r'[^A-Za-z0-9_.-]+', '_', str(spec.get('title') or 'workbook'))[:60] + '.xlsx'
    return _save_artifact_bytes(ctx, name, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'sheet', bytes_data)


def _save_preview(ctx, args):
    title = args.get('title') or 'Preview'
    html = args.get('html') or ''
    safe = re.sub(r'[^A-Za-z0-9_-]+', '_', title)[:40] or 'preview'
    full_path = sandbox.write_file(ctx['run_id'], f'previews/{safe}.html', html.encode('utf-8') if isinstance(html, str) else html)
    ctx['doc_html'] = html
    return {'ok': True, 'path': full_path['path']}


def _save_artifact_bytes(ctx, name, mime, kind, data):
    full = sandbox.write_file(ctx['run_id'], f'outputs/{name}', data)
    art = _register_artifact(ctx, full['path'], kind=kind, mime=mime, name=name)
    return {'ok': True, 'artifact': art, 'path': full['path'], 'size': full['size']}


# --------------------------------------------------------------------------
# Legacy PDF tools
# --------------------------------------------------------------------------

def _register_media(reg):
    reg.tool(
        name='pdf_tool',
        summary='Run a PDF utility on attached files. Useful for converting, merging, splitting, rotating, compressing or extracting text/images from PDFs.',
        timeout=120,
        risk=WRITE_TOOLS,
        params=[
            Param('id', 'string', 'pdf_to_docx|pdf_merge|pdf_extract_pages|pdf_split|pdf_rotate|pdf_compress|pdf_info|pdf_extract_images|images_to_pdf|word_count', required=True),
            Param('pages', 'string', 'Page specification, e.g. "2-5,8" or "1-3"', default=''),
            Param('angle', 'string', '90|180|270', default='90'),
            Param('every', 'integer', 'For pdf_split: split into chunks of N pages', default=0),
        ],
    )(lambda ctx, args: _safe(_pdf_tool, ctx, args))


def _pdf_tool(ctx, args):
    from . import study_tools
    sources = ctx.get('sources') or []
    if not sources:
        return {'ok': False, 'error': 'no attached files for this tool'}
    materialized = []
    for src in sources:
        if isinstance(src, dict) and src.get('path'):
            materialized.append(src)
    if not materialized:
        return {'ok': False, 'error': 'attached files are not on disk; upload via /lazy/upload first'}

    tool_id = str(args.get('id') or '').strip()
    valid = set((study_tools.REGISTRY or {}).keys()) if hasattr(study_tools, 'REGISTRY') else set()
    if tool_id not in valid:
        return {'ok': False, 'error': f'unknown tool {tool_id}'}
    params = {}
    for key in ('pages', 'angle', 'every', 'ranges'):
        if args.get(key) not in (None, ''):
            params[key] = args[key]
    if 'every' in params:
        try:
            params['every'] = int(params['every'])
        except Exception:
            pass
    try:
        result = study_tools.run_tool(tool_id, materialized, params)
    except Exception as exc:
        return {'ok': False, 'error': str(exc)[:240]}

    artifacts = []
    for art in result.get('artifacts') or []:
        data = art.get('bytes') or b''
        if isinstance(data, str):
            data = data.encode('utf-8')
        full = sandbox.write_file(ctx['run_id'], f'outputs/{art["name"]}', data)
        a = _register_artifact(ctx, full['path'], kind='pdf' if 'pdf' in (art.get('mime') or '').lower() else 'other', mime=art.get('mime', ''), name=art['name'])
        artifacts.append(a)
    return {
        'ok': True,
        'summary': result.get('text') or result.get('summary') or 'Done',
        'artifacts': artifacts,
    }


# --------------------------------------------------------------------------
# Ingestion — reading what the user actually gave us
# --------------------------------------------------------------------------

_TEXT_EXT = {'.txt', '.md', '.csv', '.json', '.py', '.js', '.html', '.htm', '.xml', '.log'}


def _register_ingest(reg):
    reg.tool(
        name='read_upload',
        summary='Extract readable text from a file in the workspace (.pdf, .docx, .txt, .md, .csv). '
                'Call this FIRST whenever the user attaches a file or asks about one — uploads are already in inputs/.',
        timeout=60,
        risk=READ_TOOLS,
        params=[
            Param('path', 'string', 'Workspace-relative path, usually inputs/<filename>', required=True),
            Param('max_chars', 'integer', 'Maximum characters to return', default=12000),
        ],
    )(lambda ctx, args: _safe(_read_upload, ctx, args))

    reg.tool(
        name='list_uploads',
        summary='List the files the user attached to this run (the inputs/ folder).',
        timeout=10,
        risk=READ_TOOLS,
    )(lambda ctx, args: _safe(_list_uploads, ctx, args))


def _read_upload(ctx, args):
    path = args.get('path') or ''
    if not path:
        return {'ok': False, 'error': 'path is required'}
    try:
        full = sandbox.resolve_path(ctx['run_id'], path, must_exist=True)
    except sandbox.SandboxError as exc:
        # Help the model recover instead of failing the whole turn.
        listing = _list_uploads(ctx, {})
        available = ', '.join(f['path'] for f in (listing.get('files') or [])[:10])
        return {'ok': False, 'error': f'{exc}. Available files: {available or "(none)"}'}

    max_chars = max(500, min(60000, int(args.get('max_chars') or 12000)))
    with open(full, 'rb') as handle:
        data = handle.read()
    ext = os.path.splitext(full)[1].lower()

    title = ''
    if ext == '.pdf':
        from ..lazy_io import extract_pdf_text
        text, title = extract_pdf_text(data)
    elif ext == '.docx':
        from ..lazy_io import extract_docx
        text, title = extract_docx(data)
    elif ext in _TEXT_EXT:
        text = data.decode('utf-8', errors='replace')
    else:
        return {'ok': False, 'error': f'unsupported file type {ext or "(none)"}'}

    text = (text or '').strip()
    if not text:
        return {'ok': False, 'error': f'no readable text found in {path}'}
    excerpt = text[:max_chars]
    return {
        'ok': True,
        'text': excerpt,
        'chars': len(text),
        'truncated': len(text) > max_chars,
        'kind': ext.lstrip('.'),
        'title': title or '',
        'summary': f'Read {len(text)} characters from {os.path.basename(path)}',
    }


def _list_uploads(ctx, args):
    base = sandbox.workspace_path(ctx['run_id'])
    target = os.path.join(base, 'inputs')
    files = []
    if os.path.isdir(target):
        for name in sorted(os.listdir(target)):
            full = os.path.join(target, name)
            if os.path.isfile(full):
                files.append({'path': f'inputs/{name}', 'name': name, 'size': os.path.getsize(full)})
    for src in ctx.get('sources') or []:
        if isinstance(src, dict) and src.get('path'):
            if not any(f['path'] == src['path'] for f in files):
                files.append({'path': src['path'], 'name': src.get('name') or '', 'size': src.get('size') or 0})
    return {'ok': True, 'files': files, 'summary': f'{len(files)} attached file(s)'}



def register_all(reg):
    _register_documents(reg)
    _register_media(reg)
    _register_ingest(reg)

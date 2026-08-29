"""Turn a tool result into the one thing the loop actually needs: a sentence.

Handlers return rich structured dicts (`{'files': [...], 'truncated': False}`),
but the agent only ever reads the `summary` string in the observation. When a
handler forgets to add one the model sees a blank result, assumes the tool did
nothing, and redoes the work. This module guarantees every result speaks.

It is deliberately shape-driven rather than per-tool: it recognises the handful
of result shapes the tools emit (files, artifacts, search hits, document builds)
and falls back to a compact key/value rendering for anything else.
"""

MAX_SUMMARY = 600


def _human_size(num):
    try:
        value = float(num or 0)
    except (TypeError, ValueError):
        return '0 B'
    for unit in ('B', 'KB', 'MB', 'GB'):
        if value < 1024 or unit == 'GB':
            return f'{value:.0f} {unit}' if unit == 'B' else f'{value:.1f} {unit}'
        value /= 1024
    return f'{value:.1f} GB'


def _clip(text, limit=160):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= limit else text[:limit - 1] + '…'


def _name_of(entry):
    if not isinstance(entry, dict):
        return str(entry)
    return (entry.get('name')
            or (entry.get('path') or '').rsplit('/', 1)[-1]
            or entry.get('title')
            or entry.get('url')
            or '?')


def _files_lines(entries, limit=12):
    lines = []
    for entry in entries[:limit]:
        if isinstance(entry, dict):
            lines.append(f'{entry.get("path") or entry.get("name")} ({_human_size(entry.get("size"))})')
        else:
            lines.append(str(entry))
    if len(entries) > limit:
        lines.append(f'…and {len(entries) - limit} more')
    return lines


def _describe_files(result):
    entries = result.get('files')
    if not isinstance(entries, list):
        return None
    if not entries:
        return 'the workspace is empty — no files yet'
    lines = _files_lines(entries)
    tail = ' (list truncated)' if result.get('truncated') else ''
    return f'{len(entries)} file(s){tail}: ' + '; '.join(lines)


def _describe_results(result):
    entries = result.get('results')
    if not isinstance(entries, list):
        return None
    if not entries:
        return 'no results found'
    lines = []
    for entry in entries[:6]:
        if isinstance(entry, dict):
            title = _clip(entry.get('title') or entry.get('url'), 90)
            host = (entry.get('url') or '').split('/')[2] if '://' in (entry.get('url') or '') else ''
            lines.append(f'{title}{" (" + host + ")" if host else ""}')
        else:
            lines.append(_clip(entry, 90))
    if len(entries) > 6:
        lines.append(f'…and {len(entries) - 6} more')
    return f'{len(entries)} result(s): ' + ' | '.join(lines)


def _describe_artifact(result):
    art = result.get('artifact')
    if not isinstance(art, dict):
        return None
    size = result.get('size') or art.get('size') or 0
    return f'wrote {art.get("name") or "file"} ({_human_size(size)}) to {result.get("path") or art.get("path") or "outputs/"}'


def _describe_artifacts_list(result):
    entries = result.get('artifacts')
    if not isinstance(entries, list) or not entries:
        return None
    parts = [f'{_name_of(a)} ({_human_size(a.get("size") if isinstance(a, dict) else 0)})'
             for a in entries[:6]]
    return f'{len(entries)} file(s) written: ' + ', '.join(parts)


def _describe_document_build(result):
    if 'wordCount' not in result and 'word_count' not in result:
        return None
    words = result.get('wordCount') or result.get('word_count') or 0
    parts = [f'document "{_clip(result.get("title"), 90)}" built']
    if words:
        parts.append(f'{words} words')
    score = result.get('score')
    if score:
        # Phrased so it cannot be read as "retry for a higher number": the
        # critique has already been applied as revisions inside the pipeline.
        parts.append(f'editor score {score}/100 (already revised — do NOT rebuild to raise it)')
    if isinstance(result.get('sections'), int):
        parts.append(f"{result['sections']} section(s)")
    if isinstance(result.get('tables'), int):
        parts.append(f"{result['tables']} table(s)")
    figures = result.get('figures') or []
    if figures:
        parts.append(f'{len(figures)} figure(s)')
    issues = result.get('issues') or []
    if issues:
        parts.append(f'{len(issues)} critique note(s)')
    files = result.get('artifacts') or []
    if files:
        names = ', '.join(f'{_name_of(a)} ({_human_size(a.get("size") if isinstance(a, dict) else 0)})'
                          for a in files[:4])
        parts.append('saved as ' + names)
    errors = result.get('renderErrors') or []
    if errors:
        parts.append('MISSING: ' + '; '.join(
            f'{e.get("format")} — {_clip(e.get("error"), 90)}' for e in errors[:3]
        ))
    # A thin hand-written spec used to return a plain success, so the agent
    # believed it had produced a real document. Say so loudly instead.
    warning = result.get('warning')
    if warning:
        parts.append(str(warning))
    return ' — '.join(parts)


def _describe_written(result):
    path = result.get('path')
    if not isinstance(path, str) or not path.strip():
        return None
    if not any(k in result for k in ('size', 'bytes', 'written')):
        return None
    size = result.get('size') or result.get('bytes') or 0
    verb = 'overwrote' if result.get('overwritten') else 'wrote'
    return f'{verb} {path} ({_human_size(size)})'


def _describe_text(result):
    for key in ('text', 'content', 'output', 'stdout', 'answer', 'result'):
        value = result.get(key)
        if isinstance(value, str) and value.strip():
            return _clip(value, 420)
    return None


def _describe_generic(result):
    parts = []
    for key, value in result.items():
        if key in ('ok', 'html', 'bytes', 'data'):
            continue
        if isinstance(value, bool):
            parts.append(f'{key}={str(value).lower()}')
        elif isinstance(value, (int, float)):
            parts.append(f'{key}={value}')
        elif isinstance(value, str):
            if value.strip():
                parts.append(f'{key}={_clip(value, 90)}')
        elif isinstance(value, dict):
            parts.append(f'{key}={{{_name_of(value)}}}')
        elif isinstance(value, list):
            parts.append(f'{key}=[{len(value)} item(s)]')
        if len(', '.join(parts)) > 300:
            break
    return ', '.join(parts) if parts else None


_DESCRIBERS = (
    _describe_document_build,
    _describe_artifacts_list,
    _describe_artifact,
    _describe_results,
    _describe_files,
    _describe_written,
    _describe_text,
    _describe_generic,
)


def describe(tool_name, result):
    """Render a tool result as the observation text the agent will read."""
    if not isinstance(result, dict):
        return _clip(result, MAX_SUMMARY)

    if result.get('ok') is False or result.get('error'):
        return f'FAILED: {_clip(result.get("error") or "unknown error", 260)}'

    for fn in _DESCRIBERS:
        try:
            text = fn(result)
        except Exception:
            text = None
        if text:
            return f'{tool_name}: {_clip(text, MAX_SUMMARY)}' if not text.startswith(tool_name) else _clip(text, MAX_SUMMARY)

    return f'{tool_name}: completed'

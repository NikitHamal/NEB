"""Figure generation shared by the agent tools and the document pipeline.

Kept separate from `tools.py` so the document engine can ask for a figure
without going through the tool-call round trip, and so the rendering code
lives in one place.
"""

import io
import re

from . import diagrams

CHART_KINDS = {'bar', 'line', 'pie', 'donut', 'scatter', 'hist', 'histogram'}
DIAGRAM_KINDS = set(diagrams.KINDS) if hasattr(diagrams, 'KINDS') else {
    'flow', 'cycle', 'mindmap', 'timeline', 'compare', 'hierarchy', 'pyramid',
}


def slugify(value, default='figure', limit=50):
    text = re.sub(r'[^A-Za-z0-9_-]+', '_', str(value or '')).strip('_')
    return (text[:limit] or default)


def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _coerce_series(spec):
    """Normalise the several shapes a chart spec may arrive in."""
    series = spec.get('series')
    if not isinstance(series, list) or not series:
        values = [float(v) for v in (spec.get('values') or []) if _is_number(v)]
        if not values:
            rows = spec.get('rows')
            if isinstance(rows, list) and rows and isinstance(rows[0], (list, tuple)):
                width = max(len(r) for r in rows if isinstance(r, (list, tuple)))
                for idx in range(1, width):
                    values = [float(r[idx]) for r in rows if len(r) > idx and _is_number(r[idx])]
                    if values:
                        series = [{'name': f'Series {idx}', 'values': values}]
                        break
            else:
                series = []
        if not series and values:
            series = [{'name': spec.get('series_name') or 'Value', 'values': values}]
    if isinstance(series, list):
        cleaned = []
        for entry in series[:6]:
            if not isinstance(entry, dict):
                continue
            values = [float(v) for v in (entry.get('values') or []) if _is_number(v)]
            if values:
                cleaned.append({'name': str(entry.get('name') or 'Series'), 'values': values})
        series = cleaned
    return series or []


def build_chart(spec):
    """Render a chart spec to PNG bytes. Raises RuntimeError for bad specs."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError('matplotlib is not installed on this server') from exc

    spec = spec if isinstance(spec, dict) else {}
    kind = str(spec.get('kind') or spec.get('type') or 'bar').strip().lower()
    title = str(spec.get('title') or 'Chart')[:160]
    labels = [str(v) for v in (spec.get('labels') or [])][:40]
    series = _coerce_series(spec)

    if not series and kind not in ('hist', 'histogram'):
        raise RuntimeError('no numeric data to plot (provide values or series)')

    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    try:
        palette = diagrams._palette(spec.get('palette'))

        if kind in ('pie', 'donut'):
            values = series[0]['values']
            _, _, autotexts = ax.pie(
                values, labels=labels[:len(values)] or None, autopct='%1.1f%%',
                startangle=90, colors=palette[:len(values)],
            )
            for text in autotexts:
                text.set_fontsize(9)
            ax.axis('equal')

        elif kind in ('hist', 'histogram'):
            values = series[0]['values'] if series else []
            if not values:
                raise RuntimeError('histogram needs values')
            ax.hist(values, bins=int(spec.get('bins') or 10), color='#2563eb', edgecolor='white')

        else:
            positions = list(range(len(labels))) if labels else None
            for entry in series:
                values = entry['values']
                xs = positions[:len(values)] if positions else list(range(len(values)))
                if kind == 'line':
                    ax.plot(xs, values, marker='o', linewidth=2, label=entry['name'])
                elif kind == 'scatter':
                    ax.scatter(xs, values, s=45, label=entry['name'])
                else:
                    ax.bar([float(v) for v in xs], values, label=entry['name'])
            if positions and labels:
                rotate = len(labels) > 5
                ax.set_xticks(positions)
                ax.set_xticklabels(
                    labels, rotation=25 if rotate else 0,
                    ha='right' if rotate else 'center', fontsize=9,
                )
            if len(series) > 1:
                ax.legend(fontsize=9)

        ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
        if spec.get('x_label'):
            ax.set_xlabel(str(spec['x_label'])[:80], fontsize=10)
        if spec.get('y_label'):
            ax.set_ylabel(str(spec['y_label'])[:80], fontsize=10)
        ax.grid(axis='y', alpha=0.25, linestyle='--')
        for spine in ('top', 'right'):
            ax.spines[spine].set_visible(False)
        fig.tight_layout()

        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        data = buffer.getvalue()
    finally:
        try:
            plt.close(fig)
        except Exception:
            pass

    return data


def build_diagram(spec):
    """Render a diagram spec to a sanitized SVG string."""
    spec = spec if isinstance(spec, dict) else {}
    svg = diagrams.build_diagram(spec)
    if not svg:
        raise RuntimeError(f'could not draw that diagram — check the spec shape for kind "{spec.get("kind")}"')
    return diagrams.sanitize_svg(svg)


def build_visual(kind, spec):
    """Return ``(extension, mime, bytes)`` for a chart or diagram request."""
    kind = str(kind or '').strip().lower()
    if kind in CHART_KINDS or (kind == 'chart' and isinstance(spec, dict)):
        if kind == 'chart':
            kind = str(spec.get('kind') or 'bar').strip().lower()
            spec = {**spec, 'kind': kind}
        return 'png', 'image/png', build_chart(spec)
    if kind in ('diagram', 'figure', '') or kind in DIAGRAM_KINDS:
        if kind in ('diagram', 'figure', ''):
            kind = str(spec.get('kind') or 'flow').strip().lower()
            spec = {**spec, 'kind': kind}
        return 'svg', 'image/svg+xml', build_diagram(spec).encode('utf-8')
    raise RuntimeError(f'unknown visual kind "{kind}"')

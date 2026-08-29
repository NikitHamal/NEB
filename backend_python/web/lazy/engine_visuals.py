"""Figure planning, drawing and injection."""

import os
import re

from . import diagrams, llm, sandbox, visuals


_VISUAL_SYSTEM = """You are the art director for a professional document.

You are given the outline of a document that has just been written. Decide which
figures would genuinely raise its quality. A figure that merely repeats the text
is worthless — only request one that carries information better in picture form.

Return ONLY this JSON:
{
  "visuals": [
    {
      "kind": "flow|cycle|mindmap|timeline|compare|hierarchy|pyramid|chart",
      "section": "exact heading of the section it belongs to",
      "title": "figure title, 3-8 words",
      "caption": "one-sentence caption in the style 'Figure 1: ...'",
      "spec": { ... }
    }
  ]
}

SPEC SHAPES
- flow:    {"kind":"flow","title":"...","nodes":[{"label":"...","sub":"..."}]}   (3-6 nodes)
- cycle:   {"kind":"cycle","title":"...","nodes":[{"label":"..."}]}              (3-6 nodes)
- mindmap: {"kind":"mindmap","center":"...","branches":[{"label":"...","children":["..."]}]}
- timeline:{"kind":"timeline","title":"...","events":[{"date":"...","label":"...","detail":"..."}]}
- compare: {"kind":"compare","title":"...","columns":[{"title":"...","items":["..."]}]}  (2-3 columns)
- hierarchy:{"kind":"hierarchy","root":{"label":"...","children":[{"label":"...","children":[]}]}}
- pyramid: {"kind":"pyramid","title":"...","levels":[{"label":"..."}]}           (3-5, top first)
- chart:   {"kind":"bar|line|pie|scatter","title":"...","labels":["..."],"values":[1,2],"x_label":"...","y_label":"..."}

HARD RULES
- 0 to 3 visuals. Prefer 1-2 for a standard document, 2-3 for a comprehensive one.
- For lab reports, practicals, technical and scientific documents, return at least ONE
  diagram: the apparatus setup, the ray/circuit/flow being described, or the procedure
  as a sequence. A reader of a practical file expects to see the arrangement, and a
  report with no figure at all looks unfinished. Use "flow" for a procedure and
  "compare"/"hierarchy" for an arrangement of parts.
- "section" MUST exactly match one of the given section headings, or the figure is dropped.
- NEVER invent numeric data for a chart. Only use a chart if real figures appeared in the
  outline key points or the research. Otherwise use a diagram.
- Labels must be short (under 40 characters) or the drawing will clip.
- Return {"visuals": []} if no figure would help. Output ONLY the JSON.
"""


def _plan_visuals(user, outline, sections):
    headings = [s.get('heading') or '' for s in sections]
    if not headings:
        return []
    body = []
    for sec in sections:
        bits = [f'SECTION: {sec.get("heading") or ""}']
        bits.append(f'  purpose: {sec.get("purpose") or ""}')
        for point in (sec.get('key_points') or [])[:5]:
            bits.append(f'  - {point}')
        for block in (sec.get('blocks') or [])[:6]:
            if block.get('type') == 'paragraph':
                bits.append(f'  text: {(block.get("text") or "")[:320]}')
        body.append('\n'.join(bits))

    prompt = (
        f'TITLE: {outline.get("title")}\nDOC TYPE: {outline.get("doc_type")}\n\n'
        + '\n\n'.join(body)
        + '\n\nWhich figures would materially improve this document?'
    )
    data, _ = llm.json_chat(
        user=user, system=_VISUAL_SYSTEM, prompt=prompt,
        max_tokens=1200, temperature=0.3, model_key='neby-fast', attempts=2,
    )
    if not data or not isinstance(data, dict):
        return []
    plans = data.get('visuals') or []
    if not isinstance(plans, list):
        return []
    known = {(h or '').strip().lower(): h for h in headings}
    cleaned = []
    for plan in plans[:3]:
        if not isinstance(plan, dict):
            continue
        heading = known.get(str(plan.get('section') or '').strip().lower())
        if not heading:
            continue
        spec = plan.get('spec')
        if not isinstance(spec, dict):
            continue
        cleaned.append({**plan, 'section': heading, 'spec': spec})
    return cleaned


def _inject_visuals(user, ctx, outline, sections, base_path, step):
    """Plan, draw and inline real figures. Returns the files it produced."""
    if not sections or not base_path:
        return []

    plans = _plan_visuals(user, outline, sections)
    if not plans:
        return []

    step(f'Drawing {len(plans)} figures', ', '.join(str(p.get('kind') or 'figure') for p in plans))

    by_heading = {}
    for sec in sections:
        by_heading.setdefault((sec.get('heading') or '').strip().lower(), []).append(sec)

    figures = []
    for index, plan in enumerate(plans, start=1):
        kind = str(plan.get('kind') or '').strip().lower()
        spec = dict(plan.get('spec') or {})
        spec.setdefault('kind', kind)
        title = str(plan.get('title') or f'Figure {index}')[:120]
        spec['title'] = title

        try:
            ext, mime, data = visuals.build_visual(kind, spec)
        except Exception as exc:
            step(f'Figure {index} skipped', str(exc)[:100])
            continue

        rel = f'figures/figure_{index}_{visuals.slugify(title, "figure", 40)}.{ext}'
        try:
            written = sandbox.write_file(ctx.get('run_id'), rel, data)
        except Exception as exc:
            step(f'Figure {index} not saved', str(exc)[:100])
            continue

        caption = str(plan.get('caption') or '').strip()
        if not caption:
            caption = f'Figure {index}: {title}'
        elif not caption.lower().startswith('figure'):
            caption = f'Figure {index}: {caption}'

        figures.append({
            'path': written.get('path') or rel,
            'rel': rel,
            'name': rel.rsplit('/', 1)[-1],
            'mime': mime,
            'kind': 'image',
            'size': written.get('size') or len(data),
            'title': title,
        })

        block = {
            'type': 'image',
            'path': rel,
            'caption': caption,
            'alt': title,
            'width': 82,
            'align': 'center',
        }
        for sec in by_heading.get(str(plan.get('section') or '').strip().lower(), []):
            sec.setdefault('blocks', []).append(dict(block))

    return figures

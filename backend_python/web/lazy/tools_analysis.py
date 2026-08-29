"""Data analysis, charting and diagram tools."""

import os
import re

from . import diagrams, llm, sandbox, visuals
from .registry import Param, READ_TOOLS, WRITE_TOOLS
from .tools_shared import _register_artifact, _safe


# --------------------------------------------------------------------------
# Data analysis
# --------------------------------------------------------------------------

_ANALYSIS_SYSTEM = """You are a precise data analyst. You are given a compact statistical
summary of a dataset and a question about it.

Return ONLY a JSON object:
{
  "answer": "direct answer to the question in 2-5 sentences",
  "findings": ["specific, quantified finding", "..."],
  "caveats": ["data limitation worth mentioning"]
}
Rules: quote real numbers from the summary. Never invent values. If the data cannot
answer the question, say so plainly in "answer". Output ONLY the JSON.
"""


def _register_analysis(reg):
    reg.tool(
        name='analyze_data',
        summary='Analyse a CSV or Excel file in the workspace: shape, columns, statistics, correlations, missing values, and an LLM interpretation of a question you ask about it.',
        timeout=90,
        risk=READ_TOOLS,
        params=[
            Param('path', 'string', 'Workspace-relative path to the .csv or .xlsx file', required=True),
            Param('question', 'string', 'What you want to know from the data', default='Summarise the key patterns in this dataset.'),
        ],
    )(lambda ctx, args: _safe(_analyze_data, ctx, args))


def _analyze_data(ctx, args):
    try:
        import pandas as pd
    except ImportError:
        return {'ok': False, 'error': 'pandas is not installed on this server'}

    path = args.get('path') or ''
    if not path:
        return {'ok': False, 'error': 'path is required'}
    try:
        full = sandbox.resolve_path(ctx['run_id'], path, must_exist=True)
    except sandbox.SandboxError as exc:
        return {'ok': False, 'error': str(exc)}

    ext = os.path.splitext(full)[1].lower()
    try:
        if ext in ('.xlsx', '.xls'):
            frame = pd.read_excel(full)
        else:
            frame = pd.read_csv(full)
    except Exception as exc:
        return {'ok': False, 'error': f'could not parse {ext}: {exc}'[:240]}

    if frame.empty:
        return {'ok': False, 'error': 'the file contains no rows'}

    lines = [f'SHAPE: {frame.shape[0]} rows x {frame.shape[1]} columns']
    lines.append('COLUMNS: ' + ', '.join(f'{c} ({frame[c].dtype})' for c in frame.columns[:30]))
    missing = frame.isna().sum()
    if int(missing.sum()):
        lines.append('MISSING: ' + ', '.join(f'{c}={int(missing[c])}' for c in missing[missing > 0].index[:15]))

    numeric = frame.select_dtypes(include='number')
    if not numeric.empty:
        try:
            desc = numeric.describe().round(3)
            lines.append('NUMERIC SUMMARY:\n' + desc.to_string())
        except Exception:
            pass
        if numeric.shape[1] >= 2:
            try:
                corr = numeric.corr(numeric_only=True).round(3)
                pairs = []
                cols = list(corr.columns)
                for i in range(len(cols)):
                    for j in range(i + 1, len(cols)):
                        value = corr.iloc[i, j]
                        if value == value and abs(value) >= 0.5:
                            pairs.append(f'{cols[i]} ~ {cols[j]} = {value}')
                if pairs:
                    lines.append('STRONG CORRELATIONS (|r|>=0.5): ' + '; '.join(pairs[:12]))
            except Exception:
                pass

    categorical = frame.select_dtypes(exclude='number')
    for col in list(categorical.columns)[:4]:
        try:
            counts = frame[col].value_counts().head(6)
            if len(counts):
                lines.append(f'TOP {col}: ' + ', '.join(f'{k} ({v})' for k, v in counts.items()))
        except Exception:
            pass

    try:
        lines.append('FIRST ROWS:\n' + frame.head(5).to_string())
    except Exception:
        pass

    summary_text = '\n'.join(lines)[:7000]
    question = args.get('question') or 'Summarise the key patterns in this dataset.'
    data, _ = llm.json_chat(
        user=ctx['user'], system=_ANALYSIS_SYSTEM,
        prompt=f'QUESTION: {question}\n\nDATA SUMMARY:\n{summary_text}',
        max_tokens=900, temperature=0.2, model_key='neby-pro', attempts=2,
    )

    answer = ''
    if isinstance(data, dict):
        answer = str(data.get('answer') or '')
        findings = [str(f) for f in (data.get('findings') or [])][:6]
        if findings:
            answer += '\nKey findings:\n' + '\n'.join(f'- {f}' for f in findings)
        caveats = [str(c) for c in (data.get('caveats') or [])][:3]
        if caveats:
            answer += '\nCaveats: ' + '; '.join(caveats)
    if not answer:
        answer = summary_text[:2500]

    return {
        'ok': True,
        'answer': answer,
        'rows': int(frame.shape[0]),
        'columns': int(frame.shape[1]),
        'summary': f'Analysed {frame.shape[0]} rows x {frame.shape[1]} columns',
    }


# --------------------------------------------------------------------------
# Visuals — charts and diagrams
# --------------------------------------------------------------------------

def _register_visuals(reg):
    reg.tool(
        name='create_diagram',
        summary='Draw a clean vector diagram as SVG: flow, cycle, mindmap, timeline, compare, hierarchy or pyramid. '
                'Use it whenever a document or slide would be clearer with a figure.',
        timeout=30,
        risk=WRITE_TOOLS,
        params=[
            Param('spec', 'object', 'Diagram spec. flow/cycle use {kind,title,nodes:[{label,sub}]}; '
                                     'mindmap uses {kind,center,branches:[{label,children:[]}]}; '
                                     'timeline uses {kind,title,events:[{date,label,detail}]}; '
                                     'compare uses {kind,title,columns:[{title,items:[]}]}; '
                                     'hierarchy uses {kind,root:{label,children:[]}}; '
                                     'pyramid uses {kind,title,levels:[{label}]}', required=True),
            Param('name', 'string', 'Output filename without extension', default='diagram'),
        ],
    )(lambda ctx, args: _safe(_create_diagram, ctx, args))

    reg.tool(
        name='create_chart',
        summary='Plot a chart as a PNG image: bar, line, pie, scatter or histogram. Use for real data.',
        timeout=60,
        risk=WRITE_TOOLS,
        params=[
            Param('spec', 'object', 'Chart spec: {kind, title, labels:[], values:[], series:[{name,values}], x_label, y_label}', required=True),
            Param('name', 'string', 'Output filename without extension', default='chart'),
        ],
    )(lambda ctx, args: _safe(_create_chart, ctx, args))


def _create_diagram(ctx, args):
    spec = args.get('spec')
    if not isinstance(spec, dict):
        return {'ok': False, 'error': 'spec must be an object'}
    svg = diagrams.build_diagram(spec)
    if not svg:
        return {'ok': False, 'error': 'could not draw that diagram — check the spec shape'}
    svg = diagrams.sanitize_svg(svg)
    name = re.sub(r'[^A-Za-z0-9_-]+', '_', str(args.get('name') or 'diagram'))[:50] or 'diagram'
    rel = f'figures/{name}.svg'
    sandbox.write_file(ctx['run_id'], rel, svg)
    art = _register_artifact(ctx, rel, kind='image', mime='image/svg+xml', name=f'{name}.svg')
    return {
        'ok': True,
        'artifact': art,
        'path': rel,
        'summary': f'Drew a {spec.get("kind") or "flow"} diagram ({len(svg)} bytes)',
    }


def _create_chart(ctx, args):
    spec = args.get('spec')
    if not isinstance(spec, dict):
        return {'ok': False, 'error': 'spec must be an object'}
    try:
        data = visuals.build_chart(spec)
    except Exception as exc:
        return {'ok': False, 'error': f'chart failed: {exc}'[:240]}

    kind = str(spec.get('kind') or spec.get('type') or 'bar').strip().lower()
    name = visuals.slugify(args.get('name'), 'chart')
    rel = f'figures/{name}.png'
    sandbox.write_file(ctx['run_id'], rel, data)
    art = _register_artifact(ctx, rel, kind='image', mime='image/png', name=f'{name}.png')
    return {'ok': True, 'artifact': art, 'path': rel, 'summary': f'Plotted a {kind} chart ({len(data)} bytes)'}



def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False



def register_all(reg):
    _register_analysis(reg)
    _register_visuals(reg)

"""Writing helpers and parallel research subagents."""

import concurrent.futures
import re

from . import llm
from .registry import Param, READ_TOOLS
from .tools_shared import _safe


# --------------------------------------------------------------------------
# Writing helpers and parallel research
# --------------------------------------------------------------------------

_HUMANIZE_SYSTEM = """You rewrite text so it reads like it was written by a thoughtful
human student or professional, not a language model.

Return ONLY a JSON object: {"text": "the rewritten text"}

Rules:
- Keep the meaning, facts, structure and approximate length identical.
- Vary sentence length and rhythm. Use natural transitions.
- Remove model-ese: "It is important to note that", "In conclusion, it can be said",
  "delve", "tapestry", "crucial to understand", "Furthermore,", "Moreover," used repeatedly,
  and any list-of-three cliches.
- Keep the requested register (formal academic / plain / professional).
- Do not add new facts. Do not add headings unless the input had them.
- Output ONLY the JSON.
"""

_TRANSLATE_SYSTEM = """You are a precise translator. Translate the supplied text into the
target language, preserving meaning, tone and formatting structure.

Return ONLY a JSON object: {"text": "the translated text"}
Do not transliterate proper nouns unnecessarily. Do not add commentary.
"""


def _register_writing(reg):
    reg.tool(
        name='humanize_text',
        summary='Rewrite text so it reads naturally and human, removing AI-tell phrasing while preserving meaning and length.',
        timeout=90,
        risk=READ_TOOLS,
        params=[
            Param('text', 'string', 'The text to rewrite', required=True),
            Param('style', 'string', 'formal|academic|plain|professional', default='academic'),
        ],
    )(lambda ctx, args: _safe(_humanize_text, ctx, args))

    reg.tool(
        name='translate_text',
        summary='Translate text into another language (e.g. Nepali, Hindi, English).',
        timeout=90,
        risk=READ_TOOLS,
        params=[
            Param('text', 'string', 'The text to translate', required=True),
            Param('language', 'string', 'Target language name', required=True),
        ],
    )(lambda ctx, args: _safe(_translate_text, ctx, args))

    reg.tool(
        name='spawn_subagents',
        summary='Run 2-5 focused research subtasks in parallel and return their combined findings. '
                'Use for deep or multi-angled topics instead of doing many sequential searches.',
        timeout=180,
        risk=READ_TOOLS,
        params=[
            Param('tasks', 'array', 'List of subtask descriptions (2-5)', required=True),
            Param('context', 'string', 'Shared context every subtask should know', default=''),
        ],
    )(lambda ctx, args: _safe(_spawn_subagents, ctx, args))


def _humanize_text(ctx, args):
    text = (args.get('text') or '').strip()
    if not text:
        return {'ok': False, 'error': 'text is required'}
    style = str(args.get('style') or 'academic')
    data, _ = llm.json_chat(
        user=ctx['user'], system=_HUMANIZE_SYSTEM,
        prompt=f'REGISTER: {style}\n\nTEXT:\n{text[:14000]}',
        max_tokens=min(4000, 400 + int(len(text.split()) * 1.8)),
        temperature=0.7, model_key='neby-pro', attempts=2,
    )
    out = (data or {}).get('text') if isinstance(data, dict) else ''
    if not out:
        return {'ok': False, 'error': 'rewrite failed — try again with a shorter passage'}
    return {'ok': True, 'text': out, 'summary': f'Rewrote {len(text.split())} words in a {style} register'}


def _translate_text(ctx, args):
    text = (args.get('text') or '').strip()
    language = (args.get('language') or '').strip()
    if not text or not language:
        return {'ok': False, 'error': 'text and language are required'}
    data, _ = llm.json_chat(
        user=ctx['user'], system=_TRANSLATE_SYSTEM,
        prompt=f'TARGET LANGUAGE: {language}\n\nTEXT:\n{text[:14000]}',
        max_tokens=min(4000, 400 + int(len(text.split()) * 2)),
        temperature=0.3, model_key='neby-pro', attempts=2,
    )
    out = (data or {}).get('text') if isinstance(data, dict) else ''
    if not out:
        return {'ok': False, 'error': 'translation failed — try a shorter passage'}
    return {'ok': True, 'text': out, 'summary': f'Translated {len(text.split())} words into {language}'}


_SUBAGENT_SYSTEM = """You are a focused research subagent. You are given ONE narrow subtask.
Answer it thoroughly and concretely with facts, figures, formulas or steps as appropriate.
Be specific. No preamble, no "I will now...", no closing summary of what you did.
If you cannot establish something, say "not established" rather than guessing.
"""


def _spawn_subagents(ctx, args):
    tasks = [str(t).strip() for t in (args.get('tasks') or []) if str(t).strip()][:5]
    if not tasks:
        return {'ok': False, 'error': 'tasks must be a non-empty list'}
    context = str(args.get('context') or '')[:1500]

    def one(task):
        try:
            return {'task': task, 'result': llm.text_chat(
                user=ctx['user'], system=_SUBAGENT_SYSTEM,
                prompt=f'SHARED CONTEXT:\n{context}\n\nSUBTASK:\n{task}',
                max_tokens=1500, temperature=0.35, model_key='neby-pro',
            )}
        except Exception as exc:
            return {'task': task, 'result': f'(subagent failed: {exc})'[:200]}

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(5, len(tasks))) as pool:
        for fut in concurrent.futures.as_completed([pool.submit(one, t) for t in tasks]):
            try:
                results.append(fut.result())
            except Exception:
                pass

    combined = '\n\n'.join(f'### {r["task"]}\n{r["result"]}' for r in results)
    return {
        'ok': True,
        'findings': combined[:14000],
        'count': len(results),
        'summary': f'{len(results)} subagents completed',
    }



def register_all(reg):
    _register_writing(reg)

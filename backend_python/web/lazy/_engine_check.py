"""Free end-to-end test of the document engine with the model stubbed out.

Written after a live run burned six build_document calls on
`NameError: _format_sources`. Splitting engine.py into four modules orphaned a
helper, and no free suite exercised the drafting path — only a live run could
find it, and a live run is the most expensive way there is to discover a
missing import.

This stubs `llm.json_chat` and drives the real pipeline: research outline,
parallel section drafting, critique, revision, figure planning, figure
injection and rendering. Any NameError, ImportError or TypeError in that chain
fails here in seconds and costs nothing.

Run directly with the venv interpreter.
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import django
django.setup()

from web.lazy import docspec, engine, llm, sandbox

RUN = '_enginecheck'
FAILURES = []
CALLS = []

SECTIONS = [
    'Objective', 'Theory', 'Apparatus Required', 'Procedure',
    'Observation', 'Calculation', 'Result', 'Conclusion',
]

OUTLINE = {
    'title': 'Determination of NaOH Concentration by Titration',
    'subtitle': 'Chemistry lab report',
    'doc_type': 'lab_report',
    'template': 'neb_classic',
    'sections': [
        {'heading': heading, 'level': 1, 'purpose': f'State the {heading.lower()}.',
         'key_points': ['be specific', 'use SI units'], 'blocks': []}
        for heading in SECTIONS
    ],
}

# The declared contract is a list of heading strings. A model that returns
# dicts instead must not take the pipeline down, so both shapes are covered.
CRITIQUE = {
    'score': 74,
    'issues': [{'section': 'Conclusion', 'kind': 'clarity',
                'fix': 'State the mean titre explicitly.'}],
    'sections_to_revise': ['Conclusion'],
    'global_fixes': ['SI units'],
}

CRITIQUE_LOOSE = dict(CRITIQUE, sections_to_revise=[
    {'heading': 'Conclusion', 'directive': 'Restate the titre value explicitly.'},
])

VISUALS = {
    'visuals': [
        {'section': 'Apparatus Required', 'kind': 'diagram',
         'title': 'Titration setup',
         'spec': {'kind': 'diagram', 'nodes': [
             {'label': 'Burette'}, {'label': 'Conical flask'}, {'label': 'NaOH'},
         ], 'edges': [[0, 1], [1, 2]]},
         'caption': 'Titration apparatus.'},
        {'section': 'Observation', 'kind': 'chart',
         'title': 'Titre values',
         'spec': {'kind': 'chart', 'chart_type': 'bar',
                  'labels': ['Rough', 'I', 'II', 'III'],
                  'series': [{'name': 'Volume (mL)', 'values': [10.4, 10.2, 10.2, 10.2]}]},
         'caption': 'Titre readings across runs.'},
    ],
}

BODY = (
    'Sodium hydroxide solution of unknown concentration was titrated against '
    'a standard solution of oxalic acid using phenolphthalein as the indicator. '
    'The mean titre volume was recorded as 10.2 mL and used to compute the '
    'molarity of the alkali from the known normality of the acid. All readings '
    'were taken at the lower meniscus with the burette vertical, and the '
    'titration was repeated until three concordant values were obtained.'
)


CRITIQUE_PAYLOAD = [CRITIQUE]


def fake_json_chat(user, system, prompt, **kwargs):
    """Route each pipeline call to a canned response by system prompt."""
    CALLS.append(system[:60].replace('\n', ' '))
    if 'senior editor' in system and 'plan' in system.lower():
        return OUTLINE, '{}'
    if system.startswith(_SECTION_MARK):
        heading = _heading_from(prompt)
        return _section_payload(heading), '{}'
    if 'reviewing a document for quality' in system.lower():
        return CRITIQUE_PAYLOAD[0], '{}'
    if 'art director' in system.lower():
        return VISUALS, '{}'
    return {}, '{}'


def _heading_from(prompt):
    for heading in SECTIONS:
        if heading.lower() in prompt.lower():
            return heading
    return SECTIONS[0]


def _section_payload(heading):
    blocks = [{'type': 'paragraph', 'text': BODY}]
    if heading == 'Observation':
        blocks.append({
            'type': 'table', 'caption': 'Titration readings',
            'header': ['Run', 'Initial (mL)', 'Final (mL)', 'Volume (mL)'],
            'rows': [['Rough', '0.0', '10.4', '10.4'],
                     ['I', '0.0', '10.2', '10.2'],
                     ['II', '0.0', '10.2', '10.2'],
                     ['III', '0.0', '10.2', '10.2']],
        })
    if heading == 'Conclusion':
        blocks.append({'type': 'bullets', 'items': [
            'Mean titre = 10.2 mL.', 'Molarity of NaOH = 0.098 M.',
        ]})
    return {'heading': heading, 'level': 1, 'blocks': blocks}


def check(label, ok, detail=''):
    print(f'  [{"PASS" if ok else "FAIL"}] {label}' + (f' — {detail}' if detail else ''))
    if not ok:
        FAILURES.append(label)


_SECTION_MARK = engine._SECTION_SYSTEM[:60]
llm.json_chat = fake_json_chat


def run_pipeline(critique, run_id):
    """Drive the whole pipeline, returning (result, error)."""
    CRITIQUE_PAYLOAD[0] = critique
    CALLS.clear()
    try:
        return engine.build_document(
            user=None,
            ctx={'run_id': run_id, 'artifacts': [], '_registered_paths': set()},
            title='Determination of NaOH Concentration by Titration',
            brief='A complete NEB Class 12 chemistry lab report with observations, '
                  'calculations and a labelled diagram.',
            doc_type='lab_report',
            audience='NEB Grade 12 student',
            depth='standard',
            template='neb_classic',
            research_mode=False,
            output_formats=['docx', 'pdf', 'html'],
            visuals_enabled=True,
        ), None
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return None, f'{type(exc).__name__}: {exc}'


print('Engine pipeline with the model stubbed')
print('--------------------------------------')

result, error = run_pipeline(CRITIQUE, RUN)
check('build_document completes without raising', error is None, error or '')
if error:
    print(f'\n{len(FAILURES)} FAILED')
    sys.exit(1)
check('every pipeline stage was reached', len(CALLS) >= 4, f'{len(CALLS)} model calls')

spec = result['spec']
check('the outline produced sections', len(spec.get('sections') or []) >= 6,
      f'{len(spec.get("sections") or [])} sections')

blocks = [b for s in (spec.get('sections') or []) for b in (s.get('blocks') or [])]
tables = [b for b in blocks if b.get('type') == 'table']
images = [b for b in blocks if b.get('type') == 'image']
paras = [b for b in blocks if b.get('type') == 'paragraph']

check('sections were drafted with prose', len(paras) >= 6, f'{len(paras)} paragraphs')
check('the observation table survived', len(tables) >= 1, f'{len(tables)} tables')
check('figures were planned and injected', len(images) >= 1, f'{len(images)} images')

# The bug that started all this: figure injection swallowed a NameError from a
# missing `sandbox` import, so figures silently never appeared.
check('injected figures exist on disk',
      bool(images) and all(
          os.path.isfile(os.path.join(sandbox.workspace_path(RUN, create=False),
                                      str(b.get('path') or '')))
          for b in images
      ),
      str([b.get('path') for b in images]))

words = docspec.spec_word_count(spec)
check('the document has real length', words > 600, f'{words} words')

artifacts = result.get('artifacts') or []
names = {str(a.get('name') or '') for a in artifacts}
check('docx was rendered', any(n.endswith('.docx') for n in names), str(sorted(names)))
check('pdf was rendered', any(n.endswith('.pdf') for n in names), str(sorted(names)))
check('no format failed to render', not result.get('render_errors'),
      str(result.get('render_errors')))

titles = [s.get('heading') for s in (spec.get('sections') or [])]
refs = [t for t in titles if str(t).strip().lower().startswith('reference')]
check('references appear exactly once', len(refs) <= 1, str(titles))

print('Loose argument shapes from the model')
print('------------------------------------')

# A model that returns [{"heading": ...}] where the contract says ["heading"]
# must still get a document, not an AttributeError halfway through.
_loose, loose_error = run_pipeline(CRITIQUE_LOOSE, RUN + '_loose')
check('a dict-shaped sections_to_revise does not crash the pipeline',
      loose_error is None, loose_error or '')

print()
if FAILURES:
    print(f'{len(FAILURES)} FAILED: {", ".join(FAILURES)}')
    sys.exit(1)
print('ENGINE PIPELINE OK')

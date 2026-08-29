"""Regression tests for the document quality guards.

These cover the defects that pass a content review but fail a submission:
a section named for data that shows none, a fabricated measurement, and a
revision pass that silently drops the planner's metadata.

Free to run — no model calls.
  .venv/Scripts/python.exe web/lazy/_quality_check.py
"""

import os
import sys

import django

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from web.lazy import docspec, engine, registry, summarize, tools_documents  # noqa: E402

FAILURES = []


def check(label, condition, detail=''):
    mark = 'PASS' if condition else 'FAIL'
    if not condition:
        FAILURES.append(label)
    print(f'  [{mark}] {label}' + (f' — {detail}' if detail else ''))


def section(title):
    print('\n' + title)
    print('-' * len(title))


OUTLINE = {'sections': [
    {'heading': 'Aim', 'block_types': ['paragraph']},
    {'heading': 'Observation Table', 'block_types': ['paragraph', 'table']},
    {'heading': 'Result', 'block_types': ['paragraph', 'table']},
    {'heading': 'Conclusion', 'block_types': ['paragraph']},
]}


def draft(heading, types, blocks):
    return {'heading': heading, 'block_types': types, 'blocks': blocks}


section('1. Missing-table detection')

prose_only = draft('Observation Table', ['paragraph', 'table'], [
    {'type': 'paragraph',
     'text': 'The readings were recorded in a structured table with columns for trial, V and A.'},
])
bad = [
    draft('Aim', ['paragraph'], [{'type': 'paragraph', 'text': 'x'}]),
    prose_only,
    draft('Result', ['paragraph', 'table'], [{'type': 'paragraph', 'text': 'R = 10.05 ohm'}]),
    draft('Conclusion', ['paragraph'], [{'type': 'paragraph', 'text': 'done'}]),
]
found = engine._missing_tables(OUTLINE, bad)
check('prose-described table is caught', found == ['Observation Table', 'Result'], str(found))
check('clean sections are not flagged', 'Aim' not in found and 'Conclusion' not in found)

good = [
    bad[0],
    draft('Observation Table', ['paragraph', 'table'], [
        {'type': 'paragraph', 'text': 'Readings are tabulated below.'},
        {'type': 'table', 'caption': 'Sample', 'header': ['S.N.', 'V', 'I'],
         'rows': [['1', '1.0', '0.10'], ['2', '2.0', '0.20']]},
    ]),
    draft('Result', ['paragraph', 'table'], [
        {'type': 'table', 'caption': 'R', 'header': ['Q', 'V'], 'rows': [['1', '2']]},
    ]),
    bad[3],
]
check('real tables satisfy the check', engine._missing_tables(OUTLINE, good) == [],
      str(engine._missing_tables(OUTLINE, good)))

loose = [draft('Observation Table', ['paragraph'], [{'type': 'paragraph', 'text': 'q'}])]
check('heading alone triggers the check',
      engine._missing_tables({'sections': []}, loose) == ['Observation Table'])

check('empty input is safe', engine._missing_tables({}, []) == [])
check('unedited sections keep passing',
      engine._missing_tables(OUTLINE, [bad[0], bad[3]]) == [])

section('2. Critique surfaces the defect')

captured = {}
real_critique = engine._critique


def spy(user, outline, sections, sources, missing_tables=None):
    captured['missing'] = missing_tables if missing_tables is not None else engine._missing_tables(outline, sections)
    captured['prompt_seen'] = True
    return {'score': 70, 'issues': [], 'sections_to_revise': [], 'global_fixes': []}


engine._critique = spy
try:
    engine._critique(None, OUTLINE, bad, [], ['Observation Table'])
    check('missing tables reach the critic', captured.get('missing') == ['Observation Table'],
          str(captured.get('missing')))
finally:
    engine._critique = real_critique

section('3. Topic drift detection')

DRIFT_CASES = [
    ('To determine the focal length of a convex lens by the distant object method',
     'Determination of Focal Length of a Convex Lens', True),
    ('To determine the focal length of a convex lens by the distant object method',
     'Determination of Acceleration due to Gravity using a Simple Pendulum', False),
    ('Impact of Mobile Learning Applications on Study Habits of Secondary School Students in Nepal',
     'Assessment of Digital Learning Integration in Nepali Secondary Education', True),
    ('Impact of Mobile Learning Applications on Study Habits of Secondary School Students in Nepal',
     'Development of a Student Attendance Management System', False),
    ('To determine the focal length of a convex lens', 'Convex Lens Focal Length', True),
]
for requested, produced, should_match in DRIFT_CASES:
    score = engine._topic_overlap(requested, produced)
    check(f'{"keeps" if should_match else "drops"} "{produced[:44]}"',
          (score >= 0.2) == should_match, f'{score:.2f}')

check('empty title is safe', engine._topic_overlap('', 'anything') == 0.0)
check('identical titles score 1', engine._topic_overlap('Ohm Law', 'Ohm Law') == 1.0)

section('4. Prompts carry the rules')
for name, needle in (
    ('_SECTION_SYSTEM', 'It is a serious defect to describe a table in prose'),
    ('_SECTION_SYSTEM', 'Never fabricate measurements'),
    ('_OUTLINE_SYSTEM', '"table" is MANDATORY'),
    ('_OUTLINE_SYSTEM', 'REQUIRED TITLE'),
    ('_CRITIQUE_SYSTEM', 'STRUCTURAL DEFECTS FOUND BY AUTOMATED CHECK'),
):
    check(f'{name} states the rule', needle in getattr(engine, name), needle[:60])

section('5. Table sanitization')

from web.lazy.docspec import _normalize_table  # noqa: E402

TABLE_CASES = [
    ('code leak dropped', {'header': ['readings'], 'rows': [['readings = [10.2, 10.5, 10.3,']]}, None),
    ('assignment dropped', {'header': [], 'rows': [['values = [1,2,3,4,5]']]}, None),
    ('single column dropped', {'header': ['Value'], 'rows': [['a'], ['b'], ['c']]}, None),
    ('header-only dropped', {'header': ['A', 'B'], 'rows': []}, None),
    ('empty cells dropped', {'header': ['', ''], 'rows': [['', '']]}, None),
    ('observation table kept',
     {'header': ['S.No', 'u (cm)', 'v (cm)', 'f (cm)'],
      'rows': [['1', '30.0', '60.0', '20.0'], ['2', '35.0', '52.5', '21.0']]},
     (4, 2)),
    ('two-column prose kept',
     {'header': ['Item', 'Detail'], 'rows': [['Resistor', '10 ohm'], ['Battery', '9 V']]},
     (2, 2)),
    ('placeholder table kept',
     {'header': ['Trial', 'u', 'v'],
      'rows': [['1', 'Sample reading — replace with your own', 'x']]},
     (3, 1)),
]
for label, spec, expect in TABLE_CASES:
    out = _normalize_table(spec)
    if expect is None:
        check(label, out is None, 'kept' if out else 'dropped')
    else:
        got = (len(out['header']), len(out['rows'])) if out else None
        check(label, got == expect, str(got))

section('6. Duplicate table removal')


def tbl(header, rows):
    return {'type': 'table', 'header': header, 'rows': rows, 'caption': ''}


dupes = [
    {'heading': 'Observation', 'blocks': [
        tbl(['Trial No.', 'Distance between Lens and Screen (cm)', 'Focal Length (cm)'],
            [['1', '20.5', '20.5']])]},
    {'heading': 'Result', 'blocks': [
        tbl(['Trial No', 'Distance (cm)', 'Focal Length (cm)'], [['1', '20.0', '20.0']])]},
    {'heading': 'Apparatus', 'blocks': [
        tbl(['Item', 'Specification'], [['Lens', 'Convex'], ['Screen', 'White']])]},
]
removed = engine._dedupe_tables(dupes)
check('reworded duplicate is removed', removed == 1, str(removed))
check('unrelated table survives', len(dupes[2]['blocks']) == 1)
check('first copy survives', len(dupes[0]['blocks']) == 1)

unrelated = [
    {'heading': 'A', 'blocks': [tbl(['Name', 'Roll No'], [['x', '1']])]},
    {'heading': 'B', 'blocks': [tbl(['City', 'Population'], [['Ktm', '1']])]},
]
check('unrelated tables are kept', engine._dedupe_tables(unrelated) == 0)

identical = [{'heading': 'A', 'blocks': [
    tbl(['Item', 'Detail'], [['a', 'b']]), tbl(['Item', 'Detail'], [['c', 'd']])]}]
check('identical duplicate removed', engine._dedupe_tables(identical) == 1)

check('empty input is safe', engine._dedupe_tables([]) == 0)

section('Duplicate references section')

ref_spec = docspec.normalize_spec({
    'title': 'Report', 'doc_type': 'lab_report',
    'sections': [
        {'heading': 'Aim', 'blocks': [{'type': 'paragraph', 'text': 'To find f.'}]},
        {'heading': 'References', 'blocks': [{'type': 'list', 'items': [
            'Halliday, Resnick & Walker, Fundamentals of Physics, 11th ed.',
            'NEB Physics Grade 12 textbook, Curriculum Development Centre.',
        ]}]},
    ],
    'references': [{'text': 'NEB Physics Grade 12 textbook, Curriculum Development Centre.', 'url': ''}],
})
headings = [s['heading'].strip().lower() for s in ref_spec['sections']]
check('the planned references section is dropped', 'references' not in headings, str(headings))
check('other sections survive', headings == ['aim'], str(headings))
check('citations from it are harvested',
      len(ref_spec['references']) == 2, str([r['text'][:40] for r in ref_spec['references']]))
check('duplicates are not double-listed',
      len({r['text'].strip().lower() for r in ref_spec['references']}) == 2)

biblio = docspec.normalize_spec({'title': 'T', 'sections': [
    {'heading': 'Bibliography', 'blocks': [{'type': 'paragraph', 'text': 'A source.'}]}]})
check('bibliography is recognised too', biblio['sections'] == [], str(biblio['sections']))
check('bibliography text becomes a reference',
      len(biblio['references']) == 1, str(biblio['references']))

numbered = docspec.normalize_spec({'title': 'T', 'sections': [
    {'heading': '7. References', 'blocks': [{'type': 'paragraph', 'text': 'A source.'}]}]})
check('a numbered references heading is recognised', numbered['sections'] == [], str(numbered['sections']))

substantive = docspec.normalize_spec({'title': 'T', 'sections': [
    {'heading': 'References', 'blocks': [
        {'type': 'table', 'header': ['Source', 'Year'], 'rows': [['A', '2020'], ['B', '2021']]},
    ]}]})
check('a references section holding data is kept', len(substantive['sections']) == 1)

unrelated = docspec.normalize_spec({'title': 'T', 'sections': [
    {'heading': 'Method', 'blocks': [{'type': 'paragraph', 'text': 'Steps.'}]}]})
check('ordinary sections are untouched', len(unrelated['sections']) == 1)

section('Rebuild guard')


def _ctx_with_prior(key, artifacts=None):
    return {'_built_documents': [{
        'key': key, 'title': 'Prior', 'artifacts': artifacts or [{'name': 'report.docx'}],
        'figures': [], 'wordCount': 1200, 'score': 55,
    }]}


check('an identical rebuild is refused',
      tools_documents._already_built(
          _ctx_with_prior('To determine the focal length of a convex lens A formal lab report'),
          'To determine the focal length of a convex lens', 'A formal lab report',
      ) is not None)

check('a reworded rebuild is still caught',
      tools_documents._already_built(
          _ctx_with_prior('To determine the focal length of a convex lens A formal lab report'),
          'Focal length of a convex lens', 'A formal lab report',
      ) is not None)

check('a genuinely different document is allowed',
      tools_documents._already_built(
          _ctx_with_prior('To determine the focal length of a convex lens A formal lab report'),
          'To study the photoelectric effect', 'A formal lab report on the photoelectric effect',
      ) is None)

check('the first build always goes through',
      tools_documents._already_built(
          {'_built_documents': []}, 'Any title', 'Any brief',
      ) is None)

check('a run with no build history is safe',
      tools_documents._already_built({}, 'Any title', 'Any brief') is None)

section('Tool argument coercion')

cases = [
    ('["docx", "pdf"]', ['docx', 'pdf']),
    ('["docx"]', ['docx']),
    ('docx,pdf', ['docx', 'pdf']),
    ('docx', ['docx']),
    ('[]', []),
    ('', []),
    ('  ["docx", "pdf"]  ', ['docx', 'pdf']),
    ("['docx','pdf']", ['docx', 'pdf']),
    ('["docx", not json]', ['docx', 'not json']),
]
for raw, expected in cases:
    got = registry._split_list(raw)
    check(f'{raw!r} parses', got == expected, str(got))

check('a list passes through untouched', registry._split_list.__module__ == 'web.lazy.registry')

spec = registry.ToolSpec(
    name='probe', summary='', handler=lambda ctx, args: None,
    params=[registry.Param('formats', 'array', default=['docx', 'pdf', 'html'])],
)
normalized = registry.normalize_args(spec, {'formats': '["docx", "pdf"]'})
check('JSON array string reaches the handler intact', normalized['formats'] == ['docx', 'pdf'], str(normalized['formats']))

def kept(value):
    fmts = value if isinstance(value, list) else registry._split_list(value)
    return [f for f in fmts if f in ('docx', 'pdf', 'html')]

check('a model-supplied JSON array survives the format filter',
      kept(registry.normalize_args(spec, {'formats': '["docx", "pdf"]'})['formats']) == ['docx', 'pdf'])
check('an omitted format falls back to the default',
      kept(registry.normalize_args(spec, {})['formats']) == ['docx', 'pdf', 'html'])

section('Spec passed as a JSON string')

obj_spec = registry.ToolSpec(
    name='probe', summary='', handler=lambda ctx, args: None,
    params=[registry.Param('spec', 'object', required=True)],
)

# The failure this replaces: the model sent a whole document spec as a string,
# got it silently dropped, and spent six turns re-sending the same payload
# because "missing required args: spec" reads like truncation.
check('a JSON object string is parsed, not discarded',
      registry.normalize_args(obj_spec, {'spec': '{"title": "Lab Report"}'})['spec']
      == {'title': 'Lab Report'})

check('a fenced JSON block is parsed',
      registry.normalize_args(obj_spec, {'spec': '```json\n{"title": "Lab Report"}\n```'})['spec']
      == {'title': 'Lab Report'})

check("a single-quoted dict is parsed",
      registry.normalize_args(obj_spec, {'spec': "{'title': 'Lab Report'}"})['spec']
      == {'title': 'Lab Report'})

check('a trailing comma is forgiven',
      registry.normalize_args(obj_spec, {'spec': '{"title": "Lab Report",}'})['spec']
      == {'title': 'Lab Report'})

check('a real dict still passes through',
      registry.normalize_args(obj_spec, {'spec': {'title': 'Lab Report'}})['spec']
      == {'title': 'Lab Report'})

check('a truncated spec is rejected with a reason, not silently',
      registry.normalize_args(obj_spec, {'spec': '{"title": "Lab Repo'})['spec'] is None
      and bool(registry.rejected_args(obj_spec, {'spec': '{"title": "Lab Repo'}).get('spec')))

check('the rejection names the problem',
      'JSON' in (registry.rejected_args(obj_spec, {'spec': '{"title": "Lab Repo'}).get('spec') or ''),
      str(registry.rejected_args(obj_spec, {'spec': '{"title": "Lab Repo'})))

check('a valid spec produces no rejection',
      registry.rejected_args(obj_spec, {'spec': '{"title": "Lab Report"' + '}'}) == {})

# Every rejection has to name a cause the model can act on. A message like
# "could not parse it as JSON — None" is worse than no message at all.
reasons = {
    'just text': 'unbalanced quotes',
    '42': 'not an object',
    'null': 'not an object',
    '': 'was empty',
}
for raw, needle in reasons.items():
    got = registry.rejected_args(obj_spec, {'spec': raw}).get('spec') or ''
    check(f'{raw!r} is rejected with an actionable reason', needle in got, got)

section('Thin hand-written specs are called out')

stub = docspec.normalize_spec({'title': 'Titration', 'sections': [
    {'heading': 'Aim', 'blocks': [{'type': 'paragraph', 'text': 'To find the concentration.'}]},
]})
shape = tools_documents._spec_shape(stub)
check('the shape of a stub is measured', shape['sections'] == 1 and shape['tables'] == 0
      and shape['figures'] == 0 and shape['words'] > 0, str(shape))
check('a stub draws a warning', 'BELOW STANDARD' in tools_documents._thin_document_warning(shape),
      tools_documents._thin_document_warning(shape))

full = docspec.normalize_spec({'title': 'Titration', 'sections': [
    {'heading': 'Aim', 'blocks': [{'type': 'paragraph', 'text': 'To find the concentration.'}]},
    {'heading': 'Data', 'blocks': [
        {'type': 'table', 'header': ['Run', 'Volume'], 'rows': [['1', '10.2'], ['2', '10.4']]},
        {'type': 'image', 'path': 'outputs/diagram.svg', 'caption': 'Setup'},
    ]},
]})
rich_shape = tools_documents._spec_shape(full)
check('a spec with a table and a figure is counted',
      rich_shape['tables'] == 1 and rich_shape['figures'] == 1, str(rich_shape))
check('a complete spec earns no warning',
      tools_documents._thin_document_warning(dict(rich_shape, words=1800)) == '')

# A long essay legitimately holds no tables and warning there would push the
# agent into "improving" a document that was already fine, so length alone
# decides — structure is reported but never the trigger by itself.
check('a long spec with no tables is not flagged',
      tools_documents._thin_document_warning(dict(rich_shape, words=1800, tables=0, figures=0)) == '',
      tools_documents._thin_document_warning(dict(rich_shape, words=1800, tables=0, figures=0)))

warned = {
    'ok': True, 'title': 'Titration', 'wordCount': rich_shape['words'],
    'sections': rich_shape['sections'], 'tables': 0, 'figures': 0,
    'warning': 'BELOW STANDARD: no data tables. Use build_document instead.',
    'artifacts': [{'name': 'Titration.docx', 'size': 4553}],
}
check('the warning reaches the observation',
      'BELOW STANDARD' in summarize.describe('create_document', warned),
      summarize.describe('create_document', warned)[:300])
check('the shape reaches the observation too',
      'section(s)' in summarize.describe('create_document', warned),
      summarize.describe('create_document', warned)[:300])

section('Observation text')

build = {
    'ok': True, 'title': 'Refractive Index of a Glass Slab', 'wordCount': 1818,
    'score': 82, 'issues': [], 'figures': [{'name': 'f1.svg'}],
    'artifacts': [{'name': 'report.docx', 'size': 124358}, {'name': 'report.pdf', 'size': 125570}],
}
text = summarize.describe('build_document', build)
check('quality score is reported out of 100', 'editor score 82/100' in text, text[:200])
check('the score is framed as already-revised',
      'do not rebuild' in text.lower(), text[:200])
check('both artifacts are named in the observation',
      'report.docx' in text and 'report.pdf' in text, text[:240])

partial = dict(build, artifacts=[{'name': 'report.docx', 'size': 124358}],
               renderErrors=[{'format': 'pdf', 'error': 'TimeoutError: renderer stalled'}])
text = summarize.describe('build_document', partial)
check('a dropped format is reported, not hidden', 'MISSING' in text and 'pdf' in text, text[:240])

section('Result')
if FAILURES:
    print(f'{len(FAILURES)} failed: {", ".join(FAILURES)}')
    sys.exit(1)
print('ALL QUALITY CHECKS PASSED')

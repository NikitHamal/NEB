"""Ad-hoc proof that a spec sent as a JSON string renders a real document.

Not part of the suite — run directly to confirm the coercion fix end to end.
"""

import json
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import django
django.setup()

from web.lazy import registry, sandbox, tools_documents

RUN = '_spec_e2e'
SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">'
       '<rect width="400" height="200" fill="#eef"/>'
       '<circle cx="200" cy="100" r="60" fill="#36c"/></svg>')

sandbox.write_file(RUN, 'outputs/fig.svg', SVG)

SPEC = {
    'title': 'Determination of NaOH Concentration',
    'subtitle': 'Chemistry lab report',
    'sections': [
        {'heading': 'Aim', 'blocks': [
            {'type': 'paragraph', 'text': 'To determine the concentration of the given sodium '
                                          'hydroxide solution by titrating it against a standard '
                                          'solution of oxalic acid using phenolphthalein indicator.'},
        ]},
        {'heading': 'Observations', 'blocks': [
            {'type': 'table', 'caption': 'Titration readings',
             'header': ['Run', 'Initial (mL)', 'Final (mL)', 'Volume (mL)'],
             'rows': [['1', '0.0', '10.2', '10.2'],
                      ['2', '0.0', '10.3', '10.3'],
                      ['3', '0.0', '10.2', '10.2']]},
        ]},
        {'heading': 'Apparatus', 'blocks': [
            {'type': 'image', 'path': 'outputs/fig.svg', 'caption': 'Titration setup'},
        ]},
    ],
    'references': [{'text': 'NEB Chemistry Grade 12, Chapter 6.', 'url': ''}],
}

ctx = {'run_id': RUN, 'artifacts': [], '_registered_paths': set()}

spec_obj = registry.ToolSpec(
    name='create_document', summary='', handler=lambda c, a: None,
    params=[registry.Param('spec', 'object', required=True)],
)

fails = []


def check(label, ok, detail=''):
    print(f'  [{"PASS" if ok else "FAIL"}] {label}' + (f' — {detail}' if detail else ''))
    if not ok:
        fails.append(label)


print('Spec arrives as a JSON string, exactly as the model sent it')
args = registry.normalize_args(spec_obj, {'spec': json.dumps(SPEC)})
check('the string becomes a real dict', args['spec'] == SPEC, str(type(args['spec'])))

result = tools_documents._create_document(ctx, args)
print(f'  result: {json.dumps({k: v for k, v in result.items() if k != "artifact"}, default=str)[:300]}')

path = sandbox.workspace_path(RUN, create=False) + '/' + result['path'].replace('\\', '/')
check('a docx was written', os.path.isfile(path), f'{result.get("size")} bytes')
check('it is a real docx, not a stub', result.get('size', 0) > 15000, f'{result.get("size")} bytes')
check('the table survived', result.get('tables') == 1, str(result.get('tables')))
check('the figure survived', result.get('figures') == 1, str(result.get('figures')))
# This fixture is deliberately short, so the guard is *supposed* to fire. That
# is the point: the same call that once returned a bare success now tells the
# agent the document is thin and to use build_document instead.
check('a thin spec is flagged rather than passed off as done',
      'BELOW STANDARD' in (result.get('warning') or '')
      and 'build_document' in (result.get('warning') or ''),
      str(result.get('warning'))[:120])

text = ''
try:
    from web.lazy_io import extract_docx
    with open(path, 'rb') as handle:
        text, _title = extract_docx(handle.read())
except Exception as exc:
    check('docx is readable', False, str(exc))

for needle in ('NaOH', 'Titration readings', '10.2', 'Titration setup', 'Apparatus'):
    check(f'docx contains {needle!r}', needle in text)

print('\nA truncated spec now says why instead of "missing required args"')
broken = registry.normalize_args(spec_obj, {'spec': '{"title": "NaOH", "sections": ['})
check('the broken spec is dropped', broken['spec'] is None)
check('a reason is attached',
      'JSON' in (registry.rejected_args(spec_obj, {'spec': '{"title": "NaOH", "sections": ['}).get('spec') or ''),
      str(registry.rejected_args(spec_obj, {'spec': '{"title": "NaOH", "sections": ['})))

print()
if fails:
    print(f'{len(fails)} FAILED: {", ".join(fails)}')
    sys.exit(1)
print('SPEC E2E OK')

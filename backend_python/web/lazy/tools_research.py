"""Web research, workspace files and sandboxed execution tools."""

import os

from . import research, sandbox
from .registry import Param, READ_TOOLS, WRITE_TOOLS
from .tools_shared import _register_artifact, _safe


# --------------------------------------------------------------------------
# Research
# --------------------------------------------------------------------------

def _register_research(reg):
    reg.tool(
        name='web_search',
        summary='Search the web for current information. Returns titles, URLs and snippets.',
        timeout=30,
        risk=READ_TOOLS,
        params=[
            Param('query', 'string', 'What to search for', required=True),
            Param('max_results', 'integer', 'How many results to return (1-10)', default=6),
        ],
    )(lambda ctx, args: research.web_search(args['query'], max_results=args.get('max_results') or 6))

    reg.tool(
        name='web_fetch',
        summary='Fetch a URL and return clean, readable text.',
        timeout=30,
        risk=READ_TOOLS,
        params=[
            Param('url', 'string', 'The URL to fetch', required=True),
            Param('max_chars', 'integer', 'Maximum characters to return', default=6000),
        ],
    )(lambda ctx, args: research.web_fetch(args['url'], max_chars=args.get('max_chars') or 6000))


# --------------------------------------------------------------------------
# Workspace files
# --------------------------------------------------------------------------

def _register_files(reg):
    reg.tool(
        name='write_file',
        summary='Write text to a file inside the run workspace. Overwrites if it exists.',
        timeout=20,
        risk=WRITE_TOOLS,
        params=[
            Param('path', 'string', 'Workspace-relative path (no leading slash, no ..)', required=True),
            Param('content', 'string', 'Full file content', required=True),
        ],
    )(lambda ctx, args: _safe(sandbox.write_file, ctx['run_id'], args.get('path'), args.get('content') or ''))

    reg.tool(
        name='read_file',
        summary='Read a text file from the run workspace.',
        timeout=10,
        risk=READ_TOOLS,
        params=[
            Param('path', 'string', 'Workspace-relative path', required=True),
        ],
    )(lambda ctx, args: _safe(sandbox.read_file, ctx['run_id'], args.get('path')))

    reg.tool(
        name='list_files',
        summary='List files in the run workspace (optionally under a subfolder).',
        timeout=10,
        risk=READ_TOOLS,
        params=[
            Param('path', 'string', 'Subfolder to list (default: whole workspace)', default=''),
        ],
    )(lambda ctx, args: _safe(sandbox.list_files, ctx['run_id'], args.get('path') or ''))

    reg.tool(
        name='delete_path',
        summary='Delete a file or directory from the run workspace.',
        timeout=10,
        risk=WRITE_TOOLS,
        params=[
            Param('path', 'string', 'Workspace-relative path to delete', required=True),
        ],
    )(lambda ctx, args: _safe(sandbox.delete_path, ctx['run_id'], args.get('path')))


# --------------------------------------------------------------------------
# Execution
# --------------------------------------------------------------------------

def _register_exec(reg):
    reg.tool(
        name='run_python',
        summary='Run Python code in a restricted workspace. Network and dangerous modules are blocked. Use it to verify code, do calculations, or build data.',
        timeout=60,
        risk=WRITE_TOOLS,
        params=[
            Param('code', 'string', 'Python source to execute', required=True),
            Param('timeout', 'integer', 'Wall-clock limit in seconds (1-120)', default=30),
        ],
    )(lambda ctx, args: _safe(_run_python, ctx, args))

    reg.tool(
        name='run_shell',
        summary='Run an allowlisted shell command (python, node, npm, pip) inside the workspace.',
        timeout=60,
        risk=WRITE_TOOLS,
        params=[
            Param('command', 'string', 'Command without shell metacharacters', required=True),
            Param('timeout', 'integer', 'Wall-clock limit in seconds', default=30),
        ],
    )(lambda ctx, args: _safe(sandbox.run_shell, ctx['run_id'], args.get('command'), args.get('timeout') or 30))

    reg.tool(
        name='export_bundle',
        summary='Zip a set of files (or the whole workspace) into a downloadable archive.',
        timeout=20,
        risk=WRITE_TOOLS,
        params=[
            Param('name', 'string', 'Archive name without extension', default='bundle'),
            Param('paths', 'array', 'Files to include (default: whole workspace)', default=None),
        ],
    )(lambda ctx, args: _safe(_export_bundle, ctx, args))


def _run_python(ctx, args):
    code = args.get('code') or ''
    if not code.strip():
        return {'ok': False, 'error': 'no code provided'}
    timeout = max(1, min(120, int(args.get('timeout') or 30)))
    memory_mb = int(ctx.get('memory_mb') or 512)
    result = sandbox.run_python(ctx['run_id'], code, timeout=timeout, memory_mb=memory_mb)
    if not result.get('ok'):
        return result
    artifacts = []
    produced = []
    work = sandbox.workspace_path(ctx['run_id'])
    for fname in sorted(os.listdir(work)):
        full = os.path.join(work, fname)
        if not os.path.isfile(full) or fname.startswith('_') or fname.startswith('.'):
            continue
        produced.append(fname)
        artifacts.append(_register_artifact(ctx, fname))
    result['produced'] = produced
    result['artifacts'] = artifacts
    return result


def _export_bundle(ctx, args):
    result = sandbox.export_bundle(
        ctx['run_id'],
        paths=args.get('paths') or None,
        name=args.get('name') or 'bundle',
    )
    full = os.path.join(sandbox.workspace_path(ctx['run_id']), result['path'])
    art = _register_artifact(ctx, result['path'], kind='archive', mime='application/zip')
    return {'ok': True, 'archive': result, 'artifacts': [art]}



def register_all(reg):
    _register_research(reg)
    _register_files(reg)
    _register_exec(reg)

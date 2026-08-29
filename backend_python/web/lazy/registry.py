"""Declarative tool registry for the Lazy agent runtime.

Tools declare a schema once; the registry renders it into the model prompt,
normalizes loosely-typed LLM arguments, and enforces per-tool timeouts and
risk classes (read-only tools may run concurrently, writers may not).
"""

import json
import re

WRITE_TOOLS = 'write'
READ_TOOLS = 'read'

_IDENT_RE = re.compile(r'[^a-z0-9_]+')


class Param:
    __slots__ = ('name', 'type', 'desc', 'required', 'default')

    def __init__(self, name, type='string', desc='', required=False, default=None):
        self.name = name
        self.type = type
        self.desc = desc
        self.required = required
        self.default = default


class ToolSpec:
    __slots__ = ('name', 'summary', 'params', 'handler', 'timeout', 'risk', 'returns')

    def __init__(self, name, summary, params, handler, timeout=60, risk=WRITE_TOOLS, returns=''):
        self.name = name
        self.summary = summary
        self.params = params
        self.handler = handler
        self.timeout = timeout
        self.risk = risk
        self.returns = returns

    @property
    def concurrent_safe(self):
        return self.risk == READ_TOOLS

    def prompt_line(self):
        names = ', '.join(
            f'{p.name}{"" if p.required else "?"}' for p in self.params
        ) or '(no arguments)'
        detail = '; '.join(
            f'{p.name}: {p.desc}' for p in self.params if p.desc
        )
        return f'- {self.name}({names}) — {self.summary}' + (f' [{detail}]' if detail else '')


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, spec):
        self._tools[spec.name] = spec
        return spec

    def tool(self, name, **kwargs):
        """Decorator style registration returning a ToolSpec."""
        def wrap(fn):
            params = kwargs.pop('params', [])
            spec = ToolSpec(name=name, handler=fn, params=params, **kwargs)
            self.register(spec)
            return fn
        return wrap

    def get(self, name):
        if not name:
            return None
        key = _IDENT_RE.sub('', str(name).strip().lower().replace('-', '_').replace(' ', '_'))
        if key in self._tools:
            return self._tools[key]
        # tolerate common model misspellings such as "websearch" or "web-search"
        squashed = key.replace('_', '')
        for tool_name, spec in self._tools.items():
            if tool_name.replace('_', '') == squashed:
                return spec
        return None

    def names(self):
        return sorted(self._tools)

    def prompt_block(self):
        return '\n'.join(self._tools[n].prompt_line() for n in sorted(self._tools))


# Argument normalization -------------------------------------------------------

_ARG_SYNONYMS = {
    'path': ('path', 'file', 'file_path', 'filepath', 'filename', 'name', 'target', 'rel_path'),
    'content': ('content', 'text', 'body', 'code', 'source', 'data', 'value'),
    'query': ('query', 'q', 'search', 'search_query', 'terms', 'keywords'),
    'url': ('url', 'link', 'href', 'uri'),
    'instruction': ('instruction', 'instructions', 'task', 'prompt', 'request'),
    'title': ('title', 'doc_title', 'heading', 'subject'),
    'brief': ('brief', 'description', 'details', 'summary', 'outline', 'spec'),
}


def _coerce(value, ptype):
    return _coerce_detail(value, ptype)[0]


def _coerce_detail(value, ptype):
    """Coerce a loosely-typed model argument, returning (value, rejection_reason).

    The reason matters as much as the value. A model that sends a whole
    document spec as a JSON *string* used to get it silently replaced by
    ``None``, then a bare "missing required args: spec" — which it read as
    "my spec was truncated" and spent six turns re-sending the same string.
    """
    if value is None:
        return None, None
    if ptype in ('integer', 'int', 'number'):
        try:
            return int(float(value)), None
        except (TypeError, ValueError):
            return None, f'expected a number but got {str(value)[:60]!r}'
    if ptype in ('boolean', 'bool'):
        if isinstance(value, bool):
            return value, None
        return str(value).strip().lower() in ('1', 'true', 'yes', 'y', 'on'), None
    if ptype in ('object', 'dict', 'json'):
        return _coerce_object(value)
    if ptype in ('array', 'list'):
        if isinstance(value, list):
            return value, None
        if isinstance(value, tuple):
            return list(value), None
        if isinstance(value, str):
            return _split_list(value), None
        return None, f'expected a list but got {type(value).__name__}'
    return value, None


def _coerce_object(value):
    """Accept an object param that arrives JSON-encoded inside a string.

    Models very often emit `{"title": ..., "sections": [...]}` as one big
    string. Rejecting it wholesale is the difference between a rendered
    document and an empty one, so parse it rather than drop it.
    """
    if isinstance(value, (dict, list)):
        return value, None
    if not isinstance(value, str):
        return None, f'expected an object but got {type(value).__name__}'
    parsed, error = _parse_json(value)
    if error:
        return None, f'could not parse it as JSON — {error}'
    if isinstance(parsed, (dict, list)):
        return parsed, None
    return None, f'it parsed to a {type(parsed).__name__}, not an object'


# Distinguishes "parsed successfully, and the answer was null" from "the parse
# failed" — `null` is a valid piece of JSON, and collapsing the two produced
# the nonsense message "could not parse it as JSON — None".
_MISSING = object()


def _parse_json(raw):
    """Parse model-supplied JSON, returning (value, error).

    Tries strict JSON first, then Python literals for single-quoted payloads.
    On failure the value is `None` and the error explains why; a payload that
    is genuinely JSON `null` returns `(None, None)`.
    """
    text = _json_text(raw)
    if not text:
        return _MISSING, 'the value was empty'
    for loader in (json.loads, _literal_json):
        try:
            return loader(text), None
        except Exception:
            continue
    return _MISSING, 'unbalanced quotes or a truncated string'


_CODE_FENCE_RE = re.compile(r'^\s*```[A-Za-z0-9]*\s*|\s*```\s*$')
_TRAILING_COMMA_RE = re.compile(r',(\s*[}\]])')


def _json_text(raw):
    """Strip the decorations models wrap JSON in before parsing it.

    Fenced blocks and trailing commas are the two most common reasons a
    hand-typed spec fails to parse, and both are trivially repairable —
    repairing them beats rejecting a call that was seconds from working.
    """
    text = (raw or '').strip()
    text = _CODE_FENCE_RE.sub('', text).strip()
    return _TRAILING_COMMA_RE.sub(r'\1', text)


def _literal_json(raw):
    """Python-literal fallback for single-quoted JSON such as {'a': 'b'}."""
    import ast
    return ast.literal_eval(raw)


def _split_list(text):
    """Parse a model-supplied list that may arrive JSON-encoded or comma-joined.

    Models frequently emit `["docx", "pdf"]` as a *string*, and splitting that
    on commas yields the garbage tokens `['["docx"', '"pdf"]']`, which then get
    filtered out downstream — silently dropping every requested format.
    """
    raw = (text or '').strip()
    if not raw:
        return []
    if raw[0] in '[{':
        parsed, _error = _parse_json(raw)
        if isinstance(parsed, list):
            return [str(v).strip() for v in parsed if str(v).strip()]
        if isinstance(parsed, str) and parsed.strip():
            return [parsed.strip()]
    # Unparseable bracketed text: drop the brackets and split anyway, so a
    # malformed `["docx", pdf]` still yields ['docx', 'pdf'] instead of
    # ['["docx', 'pdf"]'] which the format filter would then discard entirely.
    stripped = raw.strip('[]{}').strip()
    return [v.strip().strip('"\'') for v in stripped.split(',') if v.strip().strip('"\'')]


def normalize_args(spec, raw_args):
    """Map a loosely-typed LLM argument dict onto the tool's declared params.

    Models routinely emit `file_path` for `path`, or nest the whole payload
    under a single `args` key; folding those here keeps handlers honest.
    """
    raw = raw_args if isinstance(raw_args, dict) else {}
    if len(raw) == 1 and 'args' in raw and isinstance(raw['args'], dict):
        raw = raw['args']

    lowered = {}
    for key, value in raw.items():
        lowered[_IDENT_RE.sub('', str(key).strip().lower().replace('-', '_'))] = value

    out = {}
    for param in spec.params:
        value = lowered.get(param.name)
        if value is None:
            for synonym in _ARG_SYNONYMS.get(param.name, ()):
                if synonym in lowered:
                    value = lowered[synonym]
                    break
        value = _coerce(value, param.type)
        if value is None:
            value = param.default
        out[param.name] = value
    return out


def missing_required(spec, args):
    return [
        p.name for p in spec.params
        if p.required and (args.get(p.name) in (None, '', [], {}))
    ]


def rejected_args(spec, raw_args):
    """Return {name: reason} for arguments the model sent but we threw away.

    Paired with `missing_required` this turns "missing required args: spec"
    into "spec was rejected: it could not be parsed as JSON — ...", which is
    the difference between the model re-sending the same broken payload six
    times and repairing it on the very next turn.
    """
    raw = raw_args if isinstance(raw_args, dict) else {}
    if len(raw) == 1 and 'args' in raw and isinstance(raw['args'], dict):
        raw = raw['args']

    lowered = {}
    for key, value in raw.items():
        lowered[_IDENT_RE.sub('', str(key).strip().lower().replace('-', '_'))] = value

    rejected = {}
    for param in spec.params:
        value, source = lowered.get(param.name), param.name
        if value is None:
            for synonym in _ARG_SYNONYMS.get(param.name, ()):
                if synonym in lowered:
                    value, source = lowered[synonym], synonym
                    break
        if value is None:
            continue
        _value, reason = _coerce_detail(value, param.type)
        if reason:
            rejected[source] = reason
    return rejected

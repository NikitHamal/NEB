"""Static name resolution check for the lazy package.

Written after a live run burned six build_document calls on
`NameError: _format_sources`. Splitting engine.py into four modules moved
`_draft_section` out but left its helper behind; nothing in the free suites
exercised that path, so it only surfaced against the real model, where it
cost ten minutes and a much worse document.

This resolves every name load in every module of the package and reports the
two ways a name can fail to resolve:

  undefined          — bound nowhere in the package at all
  not imported       — defined in another module of the package that this
                       module does not import it from

Run directly with the venv interpreter. No Django, no model calls.
"""

import ast
import builtins
import os
import sys

PACKAGE = os.path.dirname(os.path.abspath(__file__))
SKIP_PREFIX = '_'          # test scripts, not runtime modules
BUILTINS = set(dir(builtins))


class Scope:
    def __init__(self, parent=None, name='<module>'):
        self.parent = parent
        self.name = name
        self.binds = set()

    def resolve(self, name):
        scope = self
        while scope is not None:
            if name in scope.binds:
                return True
            scope = scope.parent
        return False


def _bind_target(target, scope):
    """Record everything a statement assigns to."""
    if isinstance(target, ast.Name):
        scope.binds.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            _bind_target(element, scope)
    elif isinstance(target, ast.Starred):
        _bind_target(target.value, scope)


def _bind_import(node, scope):
    for alias in node.names:
        scope.binds.add((alias.asname or alias.name).split('.')[0])


def collect_bindings(node):
    """Every name a scope binds, in any order, before the walk begins.

    Without this pre-pass two legitimate patterns look unresolved: a call to a
    function defined further down the file, and — the subtle one — a nested
    function closing over a name its parent binds *after* the def. Python
    closures resolve late, so `command_holder = []` a few lines below is
    perfectly legal. Drowning the real findings in those makes this check
    useless, so bindings are collected up front.

    Only descends into control flow: a nested def or class binds its own
    locals, and pulling those upward would hide genuine mistakes.
    """
    names = set()

    def add_target(target):
        if isinstance(target, ast.Name):
            names.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for element in target.elts:
                add_target(element)
        elif isinstance(target, ast.Starred):
            add_target(target.value)

    def walk(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(child.name)
            elif isinstance(child, ast.Lambda):
                walk(child)
            elif isinstance(child, (ast.Import, ast.ImportFrom)):
                for alias in child.names:
                    names.add((alias.asname or alias.name).split('.')[0])
            elif isinstance(child, ast.Assign):
                for target in child.targets:
                    add_target(target)
            elif isinstance(child, ast.AnnAssign):
                add_target(child.target)
            elif isinstance(child, ast.AugAssign):
                add_target(child.target)
            elif isinstance(child, ast.NamedExpr):
                add_target(child.target)
            elif isinstance(child, (ast.For, ast.AsyncFor)):
                add_target(child.target)
                walk(child)
            elif isinstance(child, (ast.With, ast.AsyncWith)):
                for item in child.items:
                    if item.optional_vars is not None:
                        add_target(item.optional_vars)
                walk(child)
            elif isinstance(child, ast.ExceptHandler):
                if child.name:
                    names.add(child.name)
                walk(child)
            elif isinstance(child, ast.Global):
                names.update(child.names)
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in child.generators:
                    add_target(generator.target)
                walk(child)
            else:
                walk(child)

    walk(node)
    return names


class Resolver(ast.NodeVisitor):
    """Walk a module tracking scope, recording unresolved name loads."""

    def __init__(self):
        self.unresolved = []      # (name, lineno)
        self.module_binds = set()

    # --- scopes ---------------------------------------------------------

    def visit_Module(self, node):
        scope = Scope(name='<module>')
        scope.binds |= collect_bindings(node)
        for child in node.body:
            self._scan(child, scope)
        self.module_binds = scope.binds

    def _scan(self, node, scope):
        """Bind names in `node` where possible, then recurse."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            scope.binds.add(node.name)
            inner = Scope(scope, node.name)
            inner.binds |= collect_bindings(node)
            arguments = node.args
            for arg in (list(arguments.posonlyargs) + list(arguments.args)
                        + list(arguments.kwonlyargs)):
                inner.binds.add(arg.arg)
            if arguments.vararg:
                inner.binds.add(arguments.vararg.arg)
            if arguments.kwarg:
                inner.binds.add(arguments.kwarg.arg)
            for child in node.body:
                self._scan(child, inner)
            return

        if isinstance(node, ast.ClassDef):
            scope.binds.add(node.name)
            inner = Scope(scope, node.name)
            inner.binds |= collect_bindings(node)
            for child in node.body:
                self._scan(child, inner)
            return

        if isinstance(node, ast.Lambda):
            inner = Scope(scope, '<lambda>')
            inner.binds |= collect_bindings(node)
            arguments = node.args
            for arg in (list(arguments.posonlyargs) + list(arguments.args)
                        + list(arguments.kwonlyargs)):
                inner.binds.add(arg.arg)
            if arguments.vararg:
                inner.binds.add(arguments.vararg.arg)
            if arguments.kwarg:
                inner.binds.add(arguments.kwarg.arg)
            self._scan(node.body, inner)
            return

        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            inner = Scope(scope, '<comp>')
            for generator in node.generators:
                _bind_target(generator.target, inner)
            for child in ast.iter_child_nodes(node):
                self._scan(child, inner)
            return

        if isinstance(node, ast.Import):
            _bind_import(node, scope)
            return
        if isinstance(node, ast.ImportFrom):
            _bind_import(node, scope)
            return

        if isinstance(node, ast.Assign):
            for target in node.targets:
                _bind_target(target, scope)
            self._scan(node.value, scope)
            return

        if isinstance(node, ast.AnnAssign):
            if node.value is not None:
                _bind_target(node.target, scope)
                self._scan(node.value, scope)
            return

        if isinstance(node, ast.AugAssign):
            _bind_target(node.target, scope)
            self._scan(node.value, scope)
            return

        if isinstance(node, ast.For):
            _bind_target(node.target, scope)
            for child in ast.iter_child_nodes(node):
                self._scan(child, scope)
            return

        if isinstance(node, ast.comprehension):
            _bind_target(node.target, scope)
            for child in ast.iter_child_nodes(node):
                self._scan(child, scope)
            return

        if isinstance(node, ast.ExceptHandler):
            if node.name:
                scope.binds.add(node.name)
            for child in ast.iter_child_nodes(node):
                self._scan(child, scope)
            return

        if isinstance(node, ast.Global):
            for name in node.names:
                scope.binds.add(name)
            return

        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                if not scope.resolve(node.id) and node.id not in BUILTINS:
                    self.unresolved.append((node.id, node.lineno))
            else:
                scope.binds.add(node.id)
            return

        if isinstance(node, ast.Nonlocal):
            return

        for child in ast.iter_child_nodes(node):
            self._scan(child, scope)


def modules():
    found = []
    for root, _dirs, files in os.walk(PACKAGE):
        if '__pycache__' in root:
            continue
        for name in sorted(files):
            if not name.endswith('.py'):
                continue
            if name.startswith(SKIP_PREFIX):
                continue
            found.append(os.path.join(root, name))
    return sorted(found)


def main():
    paths = modules()
    resolvers = {}
    for path in paths:
        with open(path, 'r', encoding='utf-8') as handle:
            tree = ast.parse(handle.read(), filename=path)
        resolver = Resolver()
        resolver.visit(tree)
        resolvers[path] = resolver

    # Every module-level name the package defines, and where it lives.
    defined_in = {}
    for path, resolver in resolvers.items():
        for name in resolver.module_binds:
            defined_in.setdefault(name, []).append(path)

    problems = []
    for path, resolver in resolvers.items():
        with open(path, 'r', encoding='utf-8') as handle:
            source = handle.read()
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported.add(alias.asname or alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add((alias.asname or alias.name).split('.')[0])

        rel = os.path.relpath(path, PACKAGE).replace('\\', '/')
        seen = set()
        for name, lineno in resolver.unresolved:
            if name in seen:
                continue
            seen.add(name)
            if name in imported:
                continue
            owners = defined_in.get(name) or []
            owners = [o for o in owners if os.path.abspath(o) != os.path.abspath(path)]
            if owners:
                where = ', '.join(os.path.relpath(o, PACKAGE).replace('\\', '/')
                                  for o in owners[:3])
                problems.append(f'{rel}:{lineno}: {name} is defined in {where} '
                                f'but never imported here')
            else:
                problems.append(f'{rel}:{lineno}: {name} is not defined anywhere')

    print(f'Scanned {len(paths)} modules in web/lazy/\n')
    if problems:
        for problem in sorted(problems):
            print('  ' + problem)
        print(f'\n{len(problems)} unresolved name(s)')
        return 1
    print('  every name resolves')
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""Tool registry assembly for the Lazy agent.

Handlers live in the per-domain modules beside this one (research, documents,
analysis, writing) and share their plumbing through `tools_shared`. This file
only wires them into one registry.

Each handler is a `ctx -> args -> result` callable. `ctx` carries the run
identity, the user, the workspace path and a small artifact registry so a
successful operation can announce itself back to the agent loop (which in turn
emits the right SSE frame to the browser). Tools never raise to the caller;
they return ``{"ok": False, "error": "..."}`` instead.
"""

from .registry import ToolRegistry
from . import tools_analysis, tools_documents, tools_research, tools_writing


def build_registry():
    reg = ToolRegistry()

    tools_research.register_all(reg)
    tools_documents.register_all(reg)
    tools_analysis.register_all(reg)
    tools_writing.register_all(reg)
    return reg

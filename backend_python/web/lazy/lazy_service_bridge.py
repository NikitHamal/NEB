"""Thin shim so the agent package can depend on a stable name even as
`web/lazy_service.py` evolves. Today this is a single re-export.
"""

from ..lazy_service import llm_chat  # noqa: F401

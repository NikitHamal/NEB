"""The Lazy agent: autonomous document chat, coding, research and content creation."""

from . import docspec, engine, events, llm, research, sandbox
from .loop import run as run_agent
from .registry import ToolRegistry
from .tools import build_registry

DEFAULT_REGISTRY = build_registry()

__all__ = [
    'docspec', 'engine', 'events', 'llm', 'research', 'sandbox',
    'run_agent', 'ToolRegistry', 'DEFAULT_REGISTRY',
]

import os
from typing import Iterable
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document

COMMANDS = [
    ("/model", "Switch active LLM model & provider"),
    ("/provider", "Select from available LLM providers"),
    ("/think quick", "Set TryingOpen thinking to quick"),
    ("/think balanced", "Set TryingOpen thinking to balanced"),
    ("/think deep", "Set TryingOpen thinking to deep"),
    ("/paste-img", "Paste image from clipboard and attach to context"),
    ("/image", "Attach image file by path (/image <path>)"),
    ("/clear-img", "Clear all attached images from context"),
    ("/agents", "List available specialized subagent roles"),
    ("/diff", "View git diff of uncommitted workspace changes"),
    ("/files", "Explore files in the current repository"),
    ("/clear", "Reset conversation context"),
    ("/help", "Show keyboard shortcuts & command list"),
    ("/exit", "Exit Neby CLI"),
]


class NebyCompleter(Completer):
    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        text = document.text_before_cursor
        
        # 1. Slash commands auto-complete
        if text.startswith("/"):
            word = text.lower()
            for cmd, desc in COMMANDS:
                if cmd.lower().startswith(word):
                    yield Completion(
                        cmd,
                        start_position=-len(text),
                        display=cmd,
                        display_meta=desc,
                    )
            return

        # 2. File mention with @
        last_word = text.split()[-1] if text.split() else ""
        if last_word.startswith("@"):
            query = last_word[1:].lower()
            cwd = os.getcwd()
            try:
                for root, dirs, files in os.walk(cwd):
                    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".git")]
                    for f in files:
                        if not f.startswith("."):
                            rel_path = os.path.relpath(os.path.join(root, f), cwd)
                            if not query or query in rel_path.lower():
                                yield Completion(
                                    f"@{rel_path}",
                                    start_position=-len(last_word),
                                    display=f"@{rel_path}",
                                    display_meta=f"{os.path.getsize(os.path.join(root, f))} B",
                                )
            except Exception:
                pass

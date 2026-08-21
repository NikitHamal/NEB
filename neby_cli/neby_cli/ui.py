
"""
neby/ui.py - Next-level minimal CLI UI
Inspired by Codex CLI screenshot:
- Sticky bottom prompt bar with border (always visible, even during streaming)
- esc to stop only visible when AI is working
- Mode indicator, model + context %, command hints inside same box
"""

import os
import sys
from pathlib import Path
from typing import List, Callable, Optional, Dict, Any
from html import escape as html_escape

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console(force_terminal=True, legacy_windows=False)


def print_banner(version: str = "0.1.0"):
    cwd = os.path.basename(os.getcwd()) or os.getcwd()
    console.print(f"[bold white]Neby Agent[/bold white] [dim white]v{version}[/dim white]")
    console.print(f"[dim]~/{cwd}[/dim]\n")


def print_step_bullet(action: str, duration_sec: Optional[float] = None, details: str = ""):
    dur_str = f" [dim]{duration_sec:.1f}s[/dim]" if duration_sec is not None else ""
    det_str = f" [dim]· {details}[/dim]" if details else ""
    console.print(f" [bold white]⬡[/bold white] {action}{dur_str}{det_str}")


def print_tool_call(tool_name: str, args: dict):
    title = f"tool: {tool_name}"
    content = ""
    for k, v in args.items():
        if isinstance(v, str) and "\n" in v:
            content += f"[cyan]{k}:[/cyan]\n{v}\n"
        else:
            content += f"[cyan]{k}:[/cyan] {v}\n"
    panel = Panel(
        content.strip() or "[dim]no arguments[/dim]",
        title=title,
        title_align="left",
        border_style="dim cyan",
        padding=(0, 1),
    )
    console.print(panel)


def print_tool_result(result: str, success: bool = True):
    preview = result.strip()
    if len(preview) > 600:
        preview = preview[:600] + "\n... [truncated]"
    panel = Panel(
        preview,
        title="result",
        title_align="left",
        border_style="dim green" if success else "dim red",
        padding=(0, 1),
    )
    console.print(panel)


def print_markdown(content: str):
    md = Markdown(content)
    console.print(md)


def print_error(msg: str):
    console.print(f"[bold red]error:[/bold red] {msg}")


def print_info(msg: str):
    console.print(f"[dim cyan]{msg}[/dim cyan]")


def print_help():
    table = Table(title="Commands", border_style="dim white")
    table.add_column("Command", style="bold cyan")
    table.add_column("Description", style="white")
    table.add_row("/model", "Switch active provider/model with arrow keys")
    table.add_row("/provider", "Select provider")
    table.add_row("/think quick/balanced/deep", "Set TryingOpen thinking level (quick=fast, deep=thorough)")
    table.add_row("/paste-img", "Paste image from clipboard and attach to context")
    table.add_row("/image", "Attach image file by path (/image <path>)")
    table.add_row("/clear-img", "Clear attached images from context")
    table.add_row("/agents", "List available specialized subagent roles")
    table.add_row("/diff", "Show uncommitted git diff")
    table.add_row("/files", "List workspace files")
    table.add_row("/clear", "Clear conversation history")
    table.add_row("/help", "Show this help table")
    table.add_row("/exit, exit, quit", "Exit CLI")
    console.print(table)


from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window, VSplit, ConditionalContainer, Dimension, FloatContainer, Float
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.formatted_text import HTML, to_formatted_text
from prompt_toolkit.filters import Condition, has_focus
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame, Box
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.layout.menus import CompletionsMenu
import re
import threading


_RICH_FG = {
    "bold white": "#ffffff",
    "white": "#e6e6e6",
    "dim": "#5a5a5a",
    "dim white": "#9a9a9a",
    "dim cyan": "#4aa3a3",
    "dim green": "#7ec699",
    "red": "#e06c75",
    "bold red": "#ff5555",
    "cyan": "#56b6c2",
    "bold cyan": "#56b6c2",
    "green": "#98c379",
    "yellow": "#e5c07b",
    "magenta": "#c678dd",
    "blue": "#61afef",
    "italic": "#9a9a9a",
}

_RICH_TOKEN = re.compile(r'(\[/?[a-z]+(?: [a-z]+)*\])')


def _rich_to_html(text: str) -> str:
    parts = _RICH_TOKEN.split(text)
    out = []
    for part in parts:
        if not part:
            continue
        if part.startswith("["):
            tag = part[1:-1]
            if tag.startswith("/"):
                out.append("</style>")
            else:
                fg = _RICH_FG.get(tag)
                if fg:
                    out.append(f'<style fg="{fg}">')
        else:
            out.append(html_escape(part))
    return "".join(out)


SLASH_COMMANDS = [
    ("/model", "Switch active LLM model & provider"),
    ("/provider", "Select from available LLM providers"),
    ("/think quick", "Set TryingOpen thinking to quick (fast, minimal reasoning)"),
    ("/think balanced", "Set TryingOpen thinking to balanced (default)"),
    ("/think deep", "Set TryingOpen thinking to deep (long reasoning)"),
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
    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        if text.lstrip().startswith("/"):
            return

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


class SlashCommandOverlay:
    def __init__(self, commands: List[tuple], on_select: Callable[[str], None]):
        self.all_commands = [{"cmd": c, "desc": d} for c, d in commands]
        self.on_select = on_select
        self.visible = False
        self.filtered: List[Dict[str, str]] = list(self.all_commands)
        self.selected_idx = 0
        self.filter_text = ""
        self.control = FormattedTextControl(self._get_content, focusable=True)
        self.kb = KeyBindings()
        self._visible_filter = Condition(lambda: self.visible)

        @self.kb.add('up', filter=self._visible_filter)
        def _(event):
            if self.filtered:
                self.selected_idx = (self.selected_idx - 1) % len(self.filtered)
                event.app.invalidate()

        @self.kb.add('down', filter=self._visible_filter)
        def _(event):
            if self.filtered:
                self.selected_idx = (self.selected_idx + 1) % len(self.filtered)
                event.app.invalidate()

        @self.kb.add('escape', filter=self._visible_filter)
        def _(event):
            self.hide()
            event.app.invalidate()

        @self.kb.add('c-c', filter=self._visible_filter)
        def _(event):
            self.hide()
            event.app.invalidate()

    def _get_content(self):
        if not self.visible or not self.filtered:
            return to_formatted_text(HTML(""))
        lines = []
        lines.append(HTML('<style fg="#c678dd">╭─ Commands ─╮</style>'))
        visible_count = min(8, len(self.filtered))
        start_idx = max(0, min(self.selected_idx - 3, len(self.filtered) - visible_count))
        for i in range(start_idx, start_idx + visible_count):
            if i >= len(self.filtered):
                break
            item = self.filtered[i]
            is_selected = (i == self.selected_idx)
            prefix = "→ " if is_selected else "  "
            cmd = html_escape(item["cmd"])
            desc = html_escape(item["desc"])
            if is_selected:
                line = f'<style fg="#c678dd">{prefix}</style><style fg="#ffffff">{cmd}</style> <style fg="#c678dd">· {desc}</style>'
            else:
                line = f'<style fg="#6e6e6e">{prefix}{cmd}</style> <style fg="#4a4a4a">· {desc}</style>'
            lines.append(HTML(line))
        if len(self.filtered) > visible_count:
            lines.append(HTML(f'<style fg="#4a4a4a">  {start_idx + 1}-{start_idx + visible_count} of {len(self.filtered)}</style>'))
        lines.append(HTML('<style fg="#c678dd">╰──────────────╯</style>'))
        lines.append(HTML('<style fg="#5a5a5a">  ↑/↓ navigate · enter/tab select · esc cancel</style>'))
        result = []
        for line in lines:
            result.extend(to_formatted_text(line))
            result.append(("", "\n"))
        return result

    def update_filter(self, text: str):
        raw = text.lstrip()
        if not raw.startswith("/"):
            self.hide()
            return
        raw_low = raw.strip().lower()
        # Exact full command typed -> hide, except for commands that need args like /image
        needs_arg = {"/image"}
        exact_cmd = next((c["cmd"].lower() for c in self.all_commands if c["cmd"].lower() == raw_low), None)
        if exact_cmd:
            if exact_cmd in needs_arg and " " not in raw.strip():
                # "/image" without space -> keep showing to prompt completion to "/image "
                pass
            else:
                self.hide()
                return
        if " " in raw:
            first = raw.split()[0].lower() if raw.split() else ""
            has_sub = any(c["cmd"].lower().startswith(first + " ") for c in self.all_commands)
            if not has_sub:
                # Typing args like "/image path" — hide
                self.hide()
                return
            # Has subcommands (e.g. "/think ") — show those subcommands
            word = first
            self.filtered = [c for c in self.all_commands if c["cmd"].lower().startswith(word + " ")]
            # Further filter by what after space if user typed "/think q"
            rest = raw[len(first):].strip().lower()
            if rest:
                self.filtered = [c for c in self.filtered if rest in c["cmd"].lower()]
            self.selected_idx = 0
            self.filter_text = word
            if self.filtered:
                self.visible = True
            else:
                self.hide()
            return
        word = raw.split()[0].lower() if raw.split() else "/"
        if word == "/":
            self.filtered = list(self.all_commands)
        else:
            self.filtered = [c for c in self.all_commands if c["cmd"].lower().startswith(word) or c["cmd"].split()[0].lower() == word]
            if not self.filtered:
                q = word[1:]
                self.filtered = [c for c in self.all_commands if q in c["cmd"].lower() or q in c["desc"].lower()]
        self.selected_idx = 0
        self.filter_text = word
        if self.filtered and raw.startswith("/"):
            self.visible = True
        else:
            self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def is_visible(self):
        return self.visible


class ModelSelectorOverlay:
    def __init__(self, catalog: List[Dict], on_select: Callable[[str, str], None]):
        self.catalog = catalog
        self.on_select = on_select
        self.visible = False
        self.items: List[Dict[str, Any]] = []
        self.selected_idx = 0
        self.current_provider = ""
        self.current_model = ""
        
        self._build_items()
        
        self.control = FormattedTextControl(
            self._get_content,
            focusable=True,
        )
        
        self.kb = KeyBindings()
        self._visible_filter = Condition(lambda: self.visible)
        
        @self.kb.add('up', filter=self._visible_filter)
        def _(event):
            self.selected_idx = (self.selected_idx - 1) % len(self.items)
            event.app.invalidate()
        
        @self.kb.add('down', filter=self._visible_filter)
        def _(event):
            self.selected_idx = (self.selected_idx + 1) % len(self.items)
            event.app.invalidate()
        
        @self.kb.add('enter', filter=self._visible_filter)
        def _(event):
            if self.items:
                item = self.items[self.selected_idx]
                self.on_select(item['provider'], item['model_id'])
            self.hide()
            event.app.invalidate()
        
        @self.kb.add('escape', filter=self._visible_filter)
        def _(event):
            self.hide()
            event.app.invalidate()
        
        @self.kb.add('c-c', filter=self._visible_filter)
        def _(event):
            self.hide()
            event.app.invalidate()
    
    def _build_items(self):
        self.items = []
        for p in self.catalog:
            for m in p.get("models", []):
                self.items.append({
                    "provider": p["provider"],
                    "provider_label": p.get("label", p["provider"]),
                    "model_id": m["id"],
                    "model_name": m.get("name", m["id"]),
                    "desc": m.get("desc", ""),
                })
    
    def _find_current_idx(self):
        for i, item in enumerate(self.items):
            if (item["provider"].lower() == self.current_provider.lower() and 
                item["model_id"].lower() == self.current_model.lower()):
                return i
        return 0
    
    def _get_content(self):
        if not self.visible:
            return to_formatted_text(HTML(""))
        
        lines = []
        lines.append(HTML('<style fg="#36a3eb">╭─ Model Selection ─╮</style>'))
        
        visible_count = min(8, len(self.items))
        start_idx = max(0, min(self.selected_idx - 4, len(self.items) - visible_count))
        
        for i in range(start_idx, start_idx + visible_count):
            if i >= len(self.items):
                break
            item = self.items[i]
            is_selected = (i == self.selected_idx)
            is_current = (item["provider"].lower() == self.current_provider.lower() and 
                         item["model_id"].lower() == self.current_model.lower())
            
            prefix = "→ " if is_selected else "  "
            name = html_escape(item['model_name'])
            prov = html_escape(item['provider'])
            desc = html_escape(item['desc'])
            
            if is_selected:
                line = f'<style fg="#36a3eb">{prefix}</style><style fg="#ffffff">{name}</style> <style fg="#5a5a5a">({prov})</style>'
                if desc:
                    line += f' <style fg="#36a3eb">· {desc}</style>'
            elif is_current:
                line = f'<style fg="#36a3eb">{prefix}</style><style fg="#2ecc71">{name}</style> <style fg="#5a5a5a">({prov}) ✓</style>'
            else:
                line = f'<style fg="#6e6e6e">{prefix}{name} ({prov})</style>'
                if desc:
                    line += f' <style fg="#4a4a4a">· {desc}</style>'
            
            lines.append(HTML(line))
        
        if len(self.items) > visible_count:
            lines.append(HTML(f'<style fg="#4a4a4a">  {start_idx + 1}-{start_idx + visible_count} of {len(self.items)}</style>'))
        
        lines.append(HTML('<style fg="#36a3eb">╰────────────────────╯</style>'))
        lines.append(HTML('<style fg="#5a5a5a">  ↑/↓ navigate · enter select · esc cancel</style>'))
        
        result = []
        for line in lines:
            result.extend(to_formatted_text(line))
            result.append(("", "\n"))
        return result
    
    def show(self, current_provider: str, current_model: str):
        self.current_provider = current_provider
        self.current_model = current_model
        self.selected_idx = self._find_current_idx()
        self.visible = True
    
    def hide(self):
        self.visible = False
    
    def is_visible(self):
        return self.visible


class NebyTUI:
    """
    Sticky bottom prompt bar TUI.
    - Header: Neby Agent + cwd
    - Body: scrollable history
    - Footer: bordered box that ALWAYS stays at bottom, even while streaming
        ┌──────────────────────────────────────────┐
        │ → [input]                esc to stop*    │
        │ ◍ Plan (shift+tab to cycle)              │
        │ Model · 7% · 📷 N img                    │
        │ / commands · @ files · ! shell           │
        └──────────────────────────────────────────┘
    * esc hint only when is_working
    - Shift+Enter inserts newline (multiline), Enter submits
    - "/" triggers SlashCommandOverlay dropdown (like model selector)
    - Ctrl+V pastes image from clipboard directly
    """
    def __init__(self, session, version="0.1.0", catalog=None):
        self.session = session
        self.version = version
        self.is_working = False
        self.stop_requested = False
        self.history: List[str] = []
        self.stream_accum = ""
        self.app: Optional[Application] = None
        self.on_submit_cb: Optional[Callable[[str], None]] = None
        self.catalog = catalog or []

        self.completer = NebyCompleter()
        self.input_buffer = Buffer(
            multiline=True,
            completer=self.completer,
            complete_while_typing=True,
        )

        self.kb = KeyBindings()
        self._setup_keys()

        self.style = Style.from_dict({
            'frame.border': '#3a3a3a',
            'header.title': '#ffffff bold',
            'header.version': '#6e6e6e',
            'header.path': '#c678dd',
            'output.text': '#e6e6e6',
            'input.text': '#ffffff',
            'input.prompt': '#7a7a7a',
            'input.placeholder': '#555555',
            'esc.hint': '#9a9a9a',
            'mode.dot': '#2ecc71 bold',
            'mode.text': '#2ecc71 bold',
            'mode.hint': '#5a5a5a',
            'model.text': '#8a8a8a',
            'hint.text': '#6e6e6e',
            'border': '#2e2e2e',
            'streaming': '#e6e6e6',
            'completion-menu': 'bg:#1a1a1a',
            'completion-menu.completion': 'bg:#1a1a1a #e6e6e6',
            'completion-menu.completion.current': 'bg:#2a4a6a #ffffff bold',
            'completion-menu.meta': 'bg:#1a1a1a #6e6e6e',
            'completion-menu.meta.current': 'bg:#2a4a6a #8a8a8a',
        })

        self.header_control = FormattedTextControl(self._get_header)
        self.output_control = FormattedTextControl(self._get_output, focusable=False)
        self.mode_control = FormattedTextControl(self._get_mode_line)
        self.model_control = FormattedTextControl(self._get_model_line)
        self.hint_control = FormattedTextControl(self._get_hint_line)
        self.attachments_control = FormattedTextControl(self._get_attachments_line)
        self.prefix_control = FormattedTextControl(lambda: to_formatted_text(HTML('<style fg="#7a7a7a">→ </style>')))
        self.esc_control = FormattedTextControl(self._get_esc_text)

        self.model_selector = ModelSelectorOverlay(
            self.catalog,
            on_select=self._on_model_selected
        )
        self.slash_overlay = SlashCommandOverlay(
            SLASH_COMMANDS,
            on_select=self._on_slash_selected,
        )
        self.input_buffer.on_text_changed.add_handler(lambda buf: self._on_buffer_changed())

    def _on_model_selected(self, provider: str, model_id: str):
        self.session.provider = provider
        self.session.model = model_id
        self.append_history(f"[dim cyan]switched to {provider}:{model_id}[/dim cyan]")
        self.session.reset()

    def _on_slash_selected(self, cmd: str):
        cur = self.input_buffer.text
        stripped = cur.lstrip()
        if stripped.startswith("/"):
            first_token = stripped.split()[0] if stripped.split() else "/"
            prefix_ws = cur[:len(cur) - len(cur.lstrip())]
            remainder = stripped[len(first_token):]
            needs_space = not cmd.endswith(" ")
            new_text = prefix_ws + cmd + (" " if needs_space and not remainder.startswith(" ") else "") + remainder.lstrip()
            self.input_buffer.text = new_text
            self.input_buffer.cursor_position = len(new_text)
        else:
            self.input_buffer.text = cmd + " "
            self.input_buffer.cursor_position = len(self.input_buffer.text)
        if self.app:
            self.app.invalidate()

    def _on_buffer_changed(self):
        if self.model_selector.is_visible():
            return
        text = self.input_buffer.text
        if text.lstrip().startswith("/") and not self.is_working:
            self.slash_overlay.update_filter(text)
        else:
            if self.slash_overlay.is_visible():
                self.slash_overlay.hide()
        if self.app:
            self.app.invalidate()

    def _handle_paste_image(self) -> bool:
        from .images import grab_clipboard_image
        ok, msg, info = grab_clipboard_image()
        if ok and info:
            self.session.attach_image(info)
            if not self.session.is_vision_supported():
                self.append_history(f"[dim yellow]ℹ {self.session.get_model_display_name()} has limited vision — image sent as metadata + path. Switch to qwen/openai for full vision.[/dim yellow]")
            self.append_history(f"[bold green]✓ Pasted image:[/bold green] {info['filename']} ({info['width']}x{info['height']} px, {info['size_kb']} KB) [dim]· /clear-img to remove[/dim]")
            if self.app:
                self.app.invalidate()
            return True
        return False

    def _setup_keys(self):
        sel_hidden = Condition(lambda: not self.model_selector.is_visible())
        slash_hidden = Condition(lambda: not self.slash_overlay.is_visible())
        both_hidden = Condition(lambda: not self.model_selector.is_visible() and not self.slash_overlay.is_visible())

        @self.kb.add('c-c', filter=both_hidden)
        def _(event):
            if self.is_working:
                self.stop_requested = True
                self.is_working = False
            else:
                event.app.exit()

        @self.kb.add('escape', filter=both_hidden)
        def _(event):
            if self.is_working:
                self.stop_requested = True
                self.is_working = False
                self.history.append("[dim]■ stopped[/dim]")
            elif self.input_buffer.text:
                self.input_buffer.reset()
            else:
                self.input_buffer.reset()
            event.app.invalidate()

        @self.kb.add('escape', filter=Condition(lambda: self.slash_overlay.is_visible()))
        def _(event):
            self.slash_overlay.hide()
            event.app.invalidate()

        @self.kb.add('s-tab')
        def _(event):
            self.session.cycle_mode()
            event.app.invalidate()

        @self.kb.add('c-v', filter=sel_hidden)
        def _(event):
            if self.is_working:
                return
            if self._handle_paste_image():
                return
            try:
                import pyperclip
                text = pyperclip.paste()
                if text:
                    event.current_buffer.insert_text(text)
                    event.app.invalidate()
            except Exception:
                pass

        @self.kb.add('c-j', filter=both_hidden)
        def _(event):
            event.current_buffer.insert_text('\n')
            event.app.invalidate()

        @self.kb.add('escape', 'enter', filter=both_hidden)
        def _(event):
            event.current_buffer.insert_text('\n')
            event.app.invalidate()

        @self.kb.add('enter', filter=both_hidden)
        def _(event):
            if self.is_working:
                return
            buf = self.input_buffer
            if buf.complete_state and buf.complete_state.completions:
                try:
                    comp = buf.complete_state.current_completion or buf.complete_state.completions[0]
                    buf.apply_completion(comp)
                    event.app.invalidate()
                    return
                except Exception:
                    pass
            text = buf.text
            if not text.strip():
                return
            buf.reset()
            if self.slash_overlay.is_visible():
                self.slash_overlay.hide()
            display = text.strip().splitlines()[0][:120]
            self.history.append(f"[bold white]› {display}[/bold white]")
            if self.on_submit_cb:
                cb = self.on_submit_cb
                threading.Thread(target=cb, args=(text,), daemon=True).start()
            event.app.invalidate()

        @self.kb.add('enter', filter=Condition(lambda: self.slash_overlay.is_visible() and not self.model_selector.is_visible()))
        def _(event):
            if not self.slash_overlay.filtered:
                event.app.invalidate()
                return
            selected = self.slash_overlay.filtered[self.slash_overlay.selected_idx]["cmd"]
            cur = self.input_buffer.text.lstrip()
            cur_low = cur.lower().strip()
            sel_low = selected.lower().strip()
            no_submit_exact = {"/image"}
            if (cur_low == sel_low or cur_low.startswith(sel_low + " ")) and sel_low not in no_submit_exact:
                self.slash_overlay.hide()
                text = self.input_buffer.text
                if not text.strip():
                    event.app.invalidate()
                    return
                self.input_buffer.reset()
                display = text.strip().splitlines()[0][:120]
                self.history.append(f"[bold white]› {display}[/bold white]")
                if self.on_submit_cb:
                    cb = self.on_submit_cb
                    threading.Thread(target=cb, args=(text,), daemon=True).start()
                event.app.invalidate()
                return
            # Otherwise autocomplete
            self.slash_overlay.hide()
            self._on_slash_selected(selected)
            event.app.invalidate()

        @self.kb.add('tab', filter=Condition(lambda: self.slash_overlay.is_visible() and not self.model_selector.is_visible()))
        def _(event):
            if self.slash_overlay.filtered:
                cmd = self.slash_overlay.filtered[self.slash_overlay.selected_idx]["cmd"]
                self.slash_overlay.hide()
                self._on_slash_selected(cmd)
            event.app.invalidate()

    def _get_header(self):
        cwd = Path.cwd()
        try:
            home = Path.home()
            cwd_str = "~" + str(cwd)[len(str(home)):] if str(cwd).startswith(str(home)) else str(cwd)
        except:
            cwd_str = str(cwd)
        short = "/".join(cwd_str.replace("\\","/").split("/")[-2:]) if "/" in cwd_str else cwd_str
        return to_formatted_text(HTML(
            f'<style fg="#ffffff">Neby Agent</style> <style fg="#6e6e6e">{self.version}</style>\n'
            f'<style fg="#c678dd">{short}</style>'
        ))

    def _get_output(self):
        if not self.history and not self.stream_accum:
            return to_formatted_text(HTML('<style fg="#3a3a3a">No conversation yet. Start with a follow-up below.</style>'))
        lines = self.history[-400:]
        text = "\n".join(_rich_to_html(line) for line in lines)
        if self.stream_accum:
            text += ("\n" if text else "") + html_escape(self.stream_accum)
        return to_formatted_text(HTML(text))

    def _get_mode_line(self):
        mode = self.session.mode if hasattr(self.session, 'mode') else "Plan"
        dot = "◍" if not self.is_working else "◍"
        color = "#2ecc71" if mode == "Plan" else "#f1c40f" if mode == "Agent" else "#3498db"
        return to_formatted_text(HTML(
            f'<style fg="{color}">{dot} {mode}</style> <style fg="#5a5a5a">(shift+tab to cycle)</style>'
        ))

    def _get_model_line(self):
        try:
            model_name = self.session.get_model_display_name()
            pct = self.session.get_context_percent()
        except:
            model_name = "Meta AI (Instant)"
            pct = 1

        img_count = len(getattr(self.session, "attached_images", []))
        img_badge = f' · <style fg="#e5c07b">📷 {img_count} img</style>' if img_count > 0 else ""
        effort = ""
        effort_badge = f' · <style fg="#c678dd">🧠 {effort}</style>' if effort else ""
        return to_formatted_text(HTML(
            f'<style fg="#8a8a8a">{model_name} · {pct}%</style>{img_badge}{effort_badge}'
        ))

    def _get_hint_line(self):
        return to_formatted_text(HTML(
            '<style fg="#6e6e6e">/ commands  ·  @ files  ·  ! shell  ·  shift+enter newline  ·  ctrl+v image</style>'
        ))

    def _get_attachments_line(self):
        imgs = getattr(self.session, "attached_images", [])
        if not imgs:
            return to_formatted_text(HTML(""))
        parts = []
        for idx, img in enumerate(imgs, 1):
            fn = html_escape(img.get("filename", f"image{idx}"))
            w = img.get("width", 0)
            h = img.get("height", 0)
            parts.append(f'<style fg="#e5c07b">📷 [{idx}] {fn} {w}x{h}</style>')
        joined = '<style fg="#4a4a4a"> · </style>'.join(parts)
        suffix = '<style fg="#5a5a5a">  (/clear-img to remove)</style>' if len(imgs) > 0 else ""
        return to_formatted_text(HTML(joined + suffix))

    def _get_esc_text(self):
        if self.is_working:
            return to_formatted_text(HTML('<style fg="#9a9a9a">esc to stop</style>'))
        return to_formatted_text(HTML(''))

    def _build_layout(self):
        header_win = Window(
            content=self.header_control,
            height=Dimension.exact(2),
            dont_extend_height=True,
        )

        output_win = Window(
            content=self.output_control,
            wrap_lines=True,
            always_hide_cursor=True,
        )

        prefix_win = Window(
            content=self.prefix_control,
            width=Dimension.exact(2),
            dont_extend_width=True,
        )
        input_win = Window(
            content=BufferControl(buffer=self.input_buffer),
            style='class:input.text',
            wrap_lines=True,
            height=Dimension(min=1, max=3),
        )
        esc_win = Window(
            content=self.esc_control,
            width=Dimension.exact(12),
            dont_extend_width=True,
        )

        input_row = VSplit([prefix_win, input_win, esc_win], height=Dimension(min=1, max=3))

        mode_win = Window(content=self.mode_control, height=Dimension.exact(1), wrap_lines=False)
        model_win = Window(content=self.model_control, height=Dimension.exact(1), wrap_lines=False)
        attachments_win = ConditionalContainer(
            content=Window(content=self.attachments_control, height=Dimension.exact(1), wrap_lines=True),
            filter=Condition(lambda: len(getattr(self.session, "attached_images", [])) > 0),
        )
        hint_win = Window(content=self.hint_control, height=Dimension.exact(1), wrap_lines=True)

        inner = HSplit([input_row, attachments_win, mode_win, model_win, hint_win], padding=0)

        bottom_frame = Frame(
            body=inner,
            style='class:border',
        )

        root = HSplit([
            header_win,
            output_win,
            Window(height=Dimension.exact(1), dont_extend_height=True),
            bottom_frame,
        ])

        selector_win = Window(
            content=self.model_selector.control,
            height=Dimension(min=1, max=12),
            width=Dimension(min=30, max=64),
            dont_extend_width=True,
            style='bg:#0a0a0a',
        )
        selector_container = ConditionalContainer(
            content=Box(selector_win, padding=0, style='bg:#0a0a0a'),
            filter=Condition(lambda: self.model_selector.is_visible()),
        )
        slash_win = Window(
            content=self.slash_overlay.control,
            height=Dimension(min=1, max=12),
            width=Dimension(min=30, max=64),
            dont_extend_width=True,
            style='bg:#0a0a0a',
        )
        slash_container = ConditionalContainer(
            content=Box(slash_win, padding=0, style='bg:#0a0a0a'),
            filter=Condition(lambda: self.slash_overlay.is_visible()),
        )

        float_container = FloatContainer(
            content=root,
            floats=[
                Float(
                    left=2,
                    bottom=9,
                    content=selector_container,
                    z_index=2,
                ),
                Float(
                    left=2,
                    bottom=9,
                    content=slash_container,
                    z_index=2,
                ),
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=8),
                    z_index=3,
                ),
            ],
        )

        return Layout(float_container, focused_element=input_win)

    def create_app(self):
        layout = self._build_layout()
        combined_kb = KeyBindings()
        for binding in self.kb.bindings:
            combined_kb.bindings.append(binding)
        for binding in self.model_selector.kb.bindings:
            combined_kb.bindings.append(binding)
        for binding in self.slash_overlay.kb.bindings:
            combined_kb.bindings.append(binding)
        app = Application(
            layout=layout,
            key_bindings=combined_kb,
            style=self.style,
            full_screen=True,
            mouse_support=False,
        )
        self.app = app
        return app

    def append_history(self, text: str):
        self.history.append(text)
        if self.app:
            self.app.invalidate()

    def set_stream(self, text: str):
        self.stream_accum = text
        if self.app:
            self.app.invalidate()

    def clear_stream(self):
        self.stream_accum = ""
        if self.app:
            self.app.invalidate()

    def set_working(self, working: bool):
        self.is_working = working
        if not working:
            self.stop_requested = False
        if self.app:
            self.app.invalidate()

    def request_stop(self) -> bool:
        return self.stop_requested

    def show_model_selector(self):
        self.model_selector.show(self.session.provider, self.session.model)
        if self.app:
            self.app.invalidate()

    def run(self, on_submit: Callable[[str], None]):
        self.on_submit_cb = on_submit
        app = self.create_app()
        app.run()


class NebyUI(NebyTUI):
    pass



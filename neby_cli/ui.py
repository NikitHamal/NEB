import os
import sys
import time
from typing import Optional
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


def print_prompt_box(user_input: str):
    panel = Panel(
        f"[bold white]{user_input}[/bold white]",
        border_style="dim white",
        padding=(0, 1),
    )
    console.print(panel)


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
    table.add_row("/diff", "Show uncommitted git diff")
    table.add_row("/files", "List workspace files")
    table.add_row("/clear", "Clear conversation history")
    table.add_row("/help", "Show this help table")
    table.add_row("/exit, exit, quit", "Exit CLI")
    
    console.print(table)

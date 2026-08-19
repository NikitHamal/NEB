import sys
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console(force_terminal=True, legacy_windows=False)


def print_banner(version: str = "0.1.0"):
    banner_text = Text()
    banner_text.append("NEBY ", style="bold white")
    banner_text.append(f"v{version} ", style="dim white")
    banner_text.append("· Minimal Agentic Coding CLI\n", style="dim white")
    banner_text.append("Providers: Qwen · K2 Think · Poolside · Motif · Meta AI · API", style="dim cyan")
    
    panel = Panel(
        banner_text,
        border_style="dim white",
        padding=(0, 2),
    )
    console.print(panel)


def print_status(model: str, provider: str, cwd: str):
    info = Text()
    info.append("cwd: ", style="dim white")
    info.append(f"{cwd}", style="white")
    info.append(" | ", style="dim white")
    info.append("model: ", style="dim white")
    info.append(f"{provider}:{model}", style="cyan")
    console.print(info)
    console.print()


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
        border_style="cyan",
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
    
    table.add_row("/model", "Switch active provider/model")
    table.add_row("/provider", "Select provider")
    table.add_row("/diff", "Show git diff")
    table.add_row("/files", "List workspace files")
    table.add_row("/clear", "Clear conversation history")
    table.add_row("/help", "Show this help table")
    table.add_row("/exit, exit, quit", "Exit CLI")
    
    console.print(table)

import sys
import threading
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console(force_terminal=True, legacy_windows=False)


def ask_question_interactive(
    question: str,
    options: List[str],
    allow_custom: bool = True,
    is_multi_select: bool = False,
    ui: Any = None,
) -> str:
    question = (question or "Please choose an option:").strip()
    if not isinstance(options, list) or not options:
        options = ["Yes", "No"]

    cleaned_options = [str(opt).strip() for opt in options if str(opt).strip()]
    if not cleaned_options:
        cleaned_options = ["Yes", "No"]

    if ui and hasattr(ui, "ask_question_overlay"):
        try:
            return ui.ask_question_overlay(question, cleaned_options, allow_custom, is_multi_select)
        except Exception:
            pass

    return _console_ask_question(question, cleaned_options, allow_custom, is_multi_select)


def _console_ask_question(
    question: str,
    options: List[str],
    allow_custom: bool = True,
    is_multi_select: bool = False,
) -> str:
    lines = [f"[bold white]{question}[/bold white]\n"]

    for idx, opt in enumerate(options, start=1):
        lines.append(f"  [bold cyan][{idx}][/bold cyan] {opt}")

    if allow_custom:
        lines.append("  [bold yellow][0][/bold yellow] [dim]Write custom response[/dim]")

    if is_multi_select:
        lines.append("\n[dim]Enter choice number(s) separated by commas (e.g. 1, 2) or custom text:[/dim]")
    else:
        lines.append("\n[dim]Enter choice number or custom response:[/dim]")

    panel = Panel(
        "\n".join(lines),
        title="[bold yellow]❓ Neby Clarification[/bold yellow]",
        title_align="left",
        border_style="yellow",
        padding=(0, 1),
    )
    console.print(panel)

    while True:
        try:
            raw = Prompt.ask("[bold yellow]› Choice[/bold yellow]").strip()
        except (KeyboardInterrupt, EOFError):
            return "User cancelled the prompt."

        if not raw:
            continue

        if is_multi_select:
            parts = [p.strip() for p in raw.split(",") if p.strip()]
            selected = []
            valid = True
            for p in parts:
                if p.isdigit():
                    val = int(p)
                    if 1 <= val <= len(options):
                        selected.append(options[val - 1])
                    elif val == 0 and allow_custom:
                        custom_text = Prompt.ask("[bold yellow]› Enter your custom answer[/bold yellow]").strip()
                        if custom_text:
                            selected.append(custom_text)
                    else:
                        valid = False
                        break
                else:
                    selected.append(p)

            if valid and selected:
                result_str = ", ".join(selected)
                console.print(f"[dim green]✓ Selected: {result_str}[/dim green]\n")
                return f"User selected: {result_str}"
            else:
                console.print("[red]Invalid selection. Please choose valid option numbers.[/red]")
                continue

        if raw.isdigit():
            val = int(raw)
            if 1 <= val <= len(options):
                chosen = options[val - 1]
                console.print(f"[dim green]✓ Selected: {chosen}[/dim green]\n")
                return f"User selected: {chosen}"
            elif val == 0 and allow_custom:
                custom_text = Prompt.ask("[bold yellow]› Enter your custom answer[/bold yellow]").strip()
                if custom_text:
                    console.print(f"[dim green]✓ Custom response: {custom_text}[/dim green]\n")
                    return f"User provided custom answer: {custom_text}"
                continue
            else:
                console.print(f"[red]Please enter a number between 1 and {len(options)} (or 0 for custom).[/red]")
                continue

        console.print(f"[dim green]✓ Response: {raw}[/dim green]\n")
        return f"User response: {raw}"

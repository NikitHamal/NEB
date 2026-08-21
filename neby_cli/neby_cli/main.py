
import argparse
import logging
import os
import subprocess
import sys
import warnings
import threading

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.disable(logging.CRITICAL)

from .agent import run_agent_turn
from .completer import NebyCompleter
from .providers import CATALOG
from .selector import keyboard_select_model
from .session import Session
from .tools import git_diff, list_dir
from .ui import NebyTUI, console, print_help, print_info

from .ui import print_banner


def interactive_model_picker(session: Session, ui=None):
    if ui and hasattr(ui, 'show_model_selector'):
        ui.show_model_selector()
    else:
        selected = keyboard_select_model(CATALOG, session.provider, session.model)
        if selected:
            session.provider = selected["provider"]
            session.model = selected["model"]
            session.rebuild_system_prompt()
            print_info(f"switched to {session.provider}:{session.model}")
            session.reset()


def handle_slash_command(cmd: str, session: Session, ui=None) -> bool:
    cmd_raw = cmd.strip()
    cmd_lower = cmd_raw.lower()

    if cmd_lower in ("/exit", "exit", "quit", "/quit"):
        if ui and ui.app:
            ui.app.exit()
        else:
            console.print("[dim]exiting.[/dim]")
            sys.exit(0)
        return True
    elif cmd_lower in ("/help", "help"):
        if ui:
            ui.append_history("[dim]Commands: /model, /think, /paste-img, /image, /clear-img, /agents, /diff, /files, /clear, /help, /exit[/dim]")
        else:
            print_help()
        return True
    elif cmd_lower.startswith("/think") or cmd_lower.startswith("/effort") or cmd_lower in ("/thinking", "/reasoning"):
        parts = cmd_raw.split(maxsplit=1)
        if len(parts) == 2:
            val = parts[1].strip().lower()
            if val in ("quick", "q", "fast"):
                session.set_effort("quick")
            elif val in ("balanced", "b", "normal", "auto"):
                session.set_effort("balanced")
            elif val in ("deep", "d", "thinking", "high"):
                session.set_effort("deep")
            else:
                msg = f"Unknown effort '{val}'. Use: /think quick|balanced|deep"
                if ui:
                    ui.append_history(f"[dim yellow]{msg}[/dim yellow]")
                else:
                    console.print(f"[dim yellow]{msg}[/dim yellow]")
                return True
        else:
            # cycle
            new = session.cycle_effort()
            if ui:
                ui.append_history(f"[dim cyan]Thinking effort → {new}[/dim cyan] (quick=fast, balanced=default, deep=thorough)")
            else:
                console.print(f"[dim cyan]Thinking effort → {new}[/dim cyan]")
            return True
        eff = getattr(session, "thinking_effort", "balanced")
        if ui:
            ui.append_history(f"[dim cyan]TryingOpen effort set to {eff}[/dim cyan] (quick/balanced/deep)")
        else:
            console.print(f"[dim cyan]TryingOpen effort → {eff}[/dim cyan]")
        return True
    elif cmd_lower in ("/model", "/provider"):
        if ui and hasattr(ui, 'show_model_selector'):
            ui.show_model_selector()
        else:
            interactive_model_picker(session, ui=ui)
        return True
    elif cmd_lower in ("/paste-img", "/paste", "/clipboard"):
        from .images import grab_clipboard_image, render_ascii_preview, format_image_description
        ok, msg, info = grab_clipboard_image()
        if ok and info:
            session.attach_image(info)
            preview = render_ascii_preview(info["path"])
            desc = format_image_description(info)
            if ui:
                ui.append_history(f"[bold green]✓ Image attached from clipboard:[/bold green] {info['filename']}")
                ui.append_history(f"[dim]{desc}[/dim]")
            else:
                console.print(f"[bold green]✓ Image attached from clipboard:[/bold green] {info['filename']}")
                console.print(preview)
        else:
            if ui:
                ui.append_history(f"[bold red]Clipboard error:[/bold red] {msg}")
            else:
                console.print(f"[bold red]Clipboard error:[/bold red] {msg}")
        return True
    elif cmd_lower.startswith("/image"):
        from .images import load_image_from_path, render_ascii_preview, format_image_description
        parts = cmd_raw.split(maxsplit=1)
        if len(parts) < 2:
            msg = "Usage: /image <path/to/image.png>"
            if ui:
                ui.append_history(f"[dim yellow]{msg}[/dim yellow]")
            else:
                console.print(f"[dim yellow]{msg}[/dim yellow]")
            return True
        img_path = parts[1].strip().strip("'\"")
        ok, msg, info = load_image_from_path(img_path)
        if ok and info:
            session.attach_image(info)
            preview = render_ascii_preview(info["path"])
            desc = format_image_description(info)
            if ui:
                ui.append_history(f"[bold green]✓ Image attached:[/bold green] {info['filename']} ({info['width']}x{info['height']} px)")
                ui.append_history(f"[dim]{desc}[/dim]")
            else:
                console.print(f"[bold green]✓ Image attached:[/bold green] {info['filename']}")
                console.print(preview)
        else:
            if ui:
                ui.append_history(f"[bold red]Image error:[/bold red] {msg}")
            else:
                console.print(f"[bold red]Image error:[/bold red] {msg}")
        return True
    elif cmd_lower in ("/clear-img", "/clear-images"):
        session.clear_images()
        if ui:
            ui.append_history("[dim]Cleared attached images.[/dim]")
        else:
            console.print("[dim]Cleared attached images.[/dim]")
        return True
    elif cmd_lower in ("/agents", "/roles", "/subagents"):
        from .subagents import get_available_roles
        roles = get_available_roles()
        if ui:
            ui.append_history("[bold cyan]Available Subagent Roles:[/bold cyan]")
            for r in roles:
                ui.append_history(f" • [bold white]{r['role']:<12}[/bold white] - {r['description']}")
        else:
            console.print("\n[bold cyan]Available Subagent Roles:[/bold cyan]")
            for r in roles:
                console.print(f" • [bold white]{r['role']:<12}[/bold white] - {r['description']}")
            console.print()
        return True
    elif cmd_lower in ("/clear", "/reset"):
        session.reset()
        if ui:
            ui.history.clear()
            ui.clear_stream()
            ui.set_working(False)
        else:
            print_info("session reset.")
        return True
    elif cmd_lower in ("/diff", "diff"):
        diff = git_diff()
        out = diff or "no git changes."
        if ui:
            ui.append_history(f"[dim]{out[:2000]}[/dim]")
        else:
            console.print(diff or "[dim]no git changes.[/dim]")
        return True
    elif cmd_lower in ("/files", "files"):
        files = list_dir(session.cwd)
        if ui:
            ui.append_history(f"[dim]{files[:3000]}[/dim]")
        else:
            console.print(files)
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Neby Agent - Minimal Autonomous Coding CLI")
    parser.add_argument("prompt", nargs="*", help="Direct prompt instruction for single-shot execution")
    parser.add_argument("--provider", "-p", default="metaai", help="LLM Provider")
    parser.add_argument("--model", "-m", default=None, help="Model ID")
    parser.add_argument("--cwd", "-d", default=".", help="Working directory path")
    args = parser.parse_args()

    session = Session(provider=args.provider, model=args.model, cwd=args.cwd)

    if args.prompt:
        user_prompt = " ".join(args.prompt)
        print_banner(version="0.1.0")
        run_agent_turn(session, user_prompt)
        return

    ui = NebyTUI(session, version="v0.1.0", catalog=CATALOG)

    def on_submit(text: str):
        if text.startswith("!"):
            sh_cmd = text[1:].strip()
            if sh_cmd:
                ui.append_history(f"[dim]→ running shell: {sh_cmd}[/dim]")
                try:
                    res = subprocess.run(sh_cmd, shell=True, text=True, capture_output=True, timeout=30)
                    if res.stdout:
                        ui.append_history(f"[dim]{res.stdout.strip()[:4000]}[/dim]")
                    if res.stderr:
                        ui.append_history(f"[red]{res.stderr.strip()[:2000]}[/red]")
                except Exception as e:
                    ui.append_history(f"[red]shell error: {e}[/red]")
            return

        if text.startswith("/") or text in ("exit", "quit", "help", "diff", "files", "clear"):
            if handle_slash_command(text, session, ui=ui):
                return

        ui.set_working(True)
        ui.set_stream("")

        def on_chunk(delta: str):
            if ui.request_stop():
                return
            ui.stream_accum += delta
            ui.app.invalidate()

        def stop_checker():
            return ui.request_stop()

        try:
            run_agent_turn(session, text, on_chunk=on_chunk, stop_checker=stop_checker, ui=ui)
        except Exception as exc:
            ui.append_history(f"[bold red]error:[/bold red] {exc}")
        finally:
            if ui.stream_accum:
                ui.append_history(ui.stream_accum)
            ui.clear_stream()
            ui.set_working(False)

    try:
        ui.run(on_submit=on_submit)
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]exiting.[/dim]")


if __name__ == "__main__":
    main()


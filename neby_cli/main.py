import argparse
import logging
import os
import subprocess
import sys
import warnings

# Suppress all library warnings and internal logs
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.disable(logging.CRITICAL)

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

from .agent import run_agent_turn
from .completer import NebyCompleter
from .providers import CATALOG, get_default_provider, list_providers
from .selector import keyboard_select_model
from .session import Session
from .tools import git_diff, list_dir
from .ui import console, print_banner, print_help, print_info


def interactive_model_picker(session: Session):
    selected = keyboard_select_model(CATALOG, session.provider, session.model)
    if selected:
        session.provider = selected["provider"]
        session.model = selected["model"]
        print_info(f"switched to {session.provider}:{session.model}")
        session.reset()


def handle_slash_command(cmd: str, session: Session) -> bool:
    cmd_lower = cmd.strip().lower()
    if cmd_lower in ("/exit", "exit", "quit", "/quit"):
        console.print("[dim]exiting.[/dim]")
        sys.exit(0)
    elif cmd_lower in ("/help", "help"):
        print_help()
        return True
    elif cmd_lower in ("/model", "/provider"):
        interactive_model_picker(session)
        return True
    elif cmd_lower in ("/clear", "/reset"):
        session.reset()
        print_info("session reset.")
        return True
    elif cmd_lower in ("/diff", "diff"):
        diff = git_diff()
        console.print(diff or "[dim]no git changes.[/dim]")
        return True
    elif cmd_lower in ("/files", "files"):
        files = list_dir(session.cwd)
        console.print(files)
        return True
    return False


def get_bottom_toolbar(session: Session):
    pct = session.get_context_percent()
    model_name = session.get_model_display_name()
    mode_name = session.mode
    files_edited = session.files_edited_count
    
    stats = f"{model_name} · {pct}%"
    if files_edited > 0:
        stats += f" · {files_edited} files edited"
        
    return HTML(
        f"<ansigreen><b>◉ {mode_name} (shift+tab to cycle)</b></ansigreen>\n"
        f"<ansigray>{stats}</ansigray>\n"
        f"<ansigray>/ commands  ·  @ files  ·  ! shell</ansigray>"
    )


def main():
    parser = argparse.ArgumentParser(description="Neby Agent - Minimal Autonomous Coding CLI")
    parser.add_argument("prompt", nargs="*", help="Direct prompt instruction for single-shot execution")
    parser.add_argument("--provider", "-p", default="metaai", help="LLM Provider (metaai, k2think, qwen, poolside, motiftech, deepai)")
    parser.add_argument("--model", "-m", default=None, help="Model ID")
    parser.add_argument("--cwd", "-d", default=".", help="Working directory path")
    args = parser.parse_args()

    session = Session(provider=args.provider, model=args.model, cwd=args.cwd)

    # Single-shot command mode
    if args.prompt:
        user_prompt = " ".join(args.prompt)
        run_agent_turn(session, user_prompt)
        return

    # Interactive REPL mode
    print_banner()

    history_file = os.path.expanduser("~/.neby_history")
    completer = NebyCompleter()
    
    # Key bindings for Shift+Tab to cycle mode
    kb = KeyBindings()
    
    @kb.add("s-tab")
    def _cycle_mode(event):
        session.cycle_mode()
        event.app.invalidate()

    pt_session = PromptSession(
        history=FileHistory(history_file),
        completer=completer,
        complete_while_typing=True,
        key_bindings=kb,
    )

    while True:
        try:
            prompt_html = HTML("<ansigray><b>→</b></ansigray> ")
            rprompt_html = HTML("<ansigray>esc to stop</ansigray>")
            
            user_input = pt_session.prompt(
                prompt_html,
                rprompt=rprompt_html,
                placeholder=HTML("<ansigray>Add a follow-up</ansigray>"),
                bottom_toolbar=lambda: get_bottom_toolbar(session),
            ).strip()
            
            if not user_input:
                continue

            # Shell command shortcut with !
            if user_input.startswith("!"):
                sh_cmd = user_input[1:].strip()
                if sh_cmd:
                    console.print(f"[dim]running shell: {sh_cmd}[/dim]")
                    res = subprocess.run(sh_cmd, shell=True, text=True, capture_output=True)
                    if res.stdout:
                        console.print(res.stdout.strip())
                    if res.stderr:
                        console.print(f"[red]{res.stderr.strip()}[/red]")
                    continue

            if user_input.startswith("/") or user_input in ("exit", "quit", "help", "diff", "files"):
                if handle_slash_command(user_input, session):
                    continue

            run_agent_turn(session, user_input)
            console.print()

        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]exiting.[/dim]")
            break
        except Exception as exc:
            console.print(f"[bold red]error:[/bold red] {exc}")


if __name__ == "__main__":
    main()

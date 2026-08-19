import argparse
import logging
import os
import sys
import warnings

# Suppress all library warnings and internal logs
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.disable(logging.CRITICAL)

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory

from .agent import run_agent_turn
from .providers import CATALOG, get_default_provider, list_providers
from .session import Session
from .tools import git_diff, list_dir
from .ui import console, print_banner, print_help, print_info, print_status


def interactive_model_picker(session: Session):
    console.print("\n[bold]Select Provider & Model:[/bold]")
    providers = list_providers()
    for idx, p in enumerate(providers, 1):
        console.print(f"[bold cyan]{idx}.[/bold cyan] [bold white]{p['label']}[/bold white] ({p['provider']})")
        for m in p["models"]:
            console.print(f"    • [cyan]{m['id']}[/cyan] - [dim]{m['name']} ({m.get('desc', '')})[/dim]")
    
    choice = input("\nEnter provider number or name (or press Enter to cancel): ").strip()
    if not choice:
        return
    
    selected_p = None
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(providers):
            selected_p = providers[num - 1]
    else:
        for p in providers:
            if p["provider"].lower() == choice.lower():
                selected_p = p
                break
                
    if selected_p:
        session.provider = selected_p["provider"]
        session.model = selected_p["default_model"]
        print_info(f"switched to {selected_p['label']} ({session.model})")
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


def main():
    parser = argparse.ArgumentParser(description="Neby CLI - Minimal Autonomous Coding Agent")
    parser.add_argument("prompt", nargs="*", help="Direct prompt instruction for single-shot execution")
    parser.add_argument("--provider", "-p", default="k2think", help="LLM Provider (k2think, qwen, poolside, metaai, motiftech)")
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
    print_status(session.model, session.provider, session.cwd)

    history_file = os.path.expanduser("~/.neby_history")
    pt_session = PromptSession(history=FileHistory(history_file))

    while True:
        try:
            prompt_html = HTML(f"<ansicyan>neby</ansicyan> <ansigray>({session.provider})</ansigray> <b>&gt;</b> ")
            user_input = pt_session.prompt(prompt_html).strip()
            
            if not user_input:
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

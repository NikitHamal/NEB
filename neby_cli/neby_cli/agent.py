
import sys
import time
from typing import Callable, Optional

from .parser import parse_tool_calls
from .providers import stream_chat
from .session import Session
from .tools import execute_tool_call
from .ui import console, print_error, print_step_bullet


def run_agent_turn(
    session: Session,
    user_input: str,
    on_chunk: Optional[Callable[[str], None]] = None,
    stop_checker: Optional[Callable[[], bool]] = None,
    ui=None,
):
    """
    Run one agent turn.
    - If ui is provided, streaming goes to ui via on_chunk and bullets go to ui history
    - stop_checker() -> bool allows esc to stop
    - on_chunk(delta) called for each token, keeps bottom bar sticky
    """
    session.add_user_message(user_input)
    step = 0

    def should_stop():
        return stop_checker() if stop_checker else False

    def emit(text: str):
        if ui:
            # When in TUI, accumulate via on_chunk, but also allow direct history appends
            if on_chunk:
                # on_chunk already updates ui.stream_accum, we don't need extra
                pass
            else:
                ui.append_history(text)
        else:
            sys.stdout.write(text)
            sys.stdout.flush()

    while step < session.max_steps_per_turn:
        if should_stop():
            if ui:
                ui.append_history("[dim]■ stopped by user[/dim]")
            else:
                console.print("[dim]■ stopped[/dim]")
            break

        step += 1
        accumulated_text = ""
        start_time = time.time()

        try:
            msgs = session.get_vision_messages() if hasattr(session, "get_vision_messages") else session.get_trimmed_messages()
            imgs = getattr(session, "attached_images", None)
            effort = getattr(session, "thinking_effort", None)
            for chunk in stream_chat(msgs, provider=session.provider, model=session.model, images=imgs, effort=effort):
                if should_stop():
                    break
                if chunk.get("type") == "reasoning":
                    continue
                c_type = chunk.get("type")
                if c_type == "text":
                    delta = chunk.get("content", "")
                    accumulated_text += delta
                    if on_chunk:
                        on_chunk(delta)
                    elif ui:
                        ui.set_stream(accumulated_text)
                    else:
                        sys.stdout.write(delta)
                        sys.stdout.flush()
                elif c_type == "error":
                    if not accumulated_text.strip():
                        err = chunk.get("error", "Unknown provider error")
                        if ui:
                            ui.append_history(f"[bold red]error:[/bold red] {err}")
                        else:
                            print_error(err)
                        return
                    break
        except Exception as exc:
            if not accumulated_text.strip():
                if ui:
                    ui.append_history(f"[bold red]error:[/bold red] Failed: {exc}")
                else:
                    print_error(f"Failed to generate response: {exc}")
                return

        elapsed = time.time() - start_time

        if not ui:
            sys.stdout.write("\n")
            sys.stdout.flush()

        if not accumulated_text.strip():
            if ui:
                ui.append_history("[dim]No response generated.[/dim]")
            else:
                console.print("[dim]No response generated.[/dim]")
            return

        clean_text, tool_calls = parse_tool_calls(accumulated_text)
        session.add_assistant_message(accumulated_text)

        # If we were streaming into ui.stream_accum, move it to history and clear for tool bullets
        if ui and on_chunk:
            ui.append_history(accumulated_text)
            ui.clear_stream()

        if not tool_calls:
            msg = f" [bold white]⬡[/bold white] Completed [dim]{elapsed:.1f}s[/dim]"
            if ui:
                ui.append_history(msg)
            else:
                print_step_bullet("Completed", duration_sec=elapsed)
            break

        is_done = False
        for call in tool_calls:
            if should_stop():
                break
            t_start = time.time()
            result = execute_tool_call(call.name, call.args, session=session, ui=ui)
            t_dur = time.time() - t_start

            action_desc = f"Tool {call.name}"
            if call.name == "read_file":
                action_desc = f"Read {call.args.get('path', 'file')}"
            elif call.name == "write_file":
                action_desc = f"Wrote {call.args.get('path', 'file')}"
            elif call.name == "edit_file":
                action_desc = f"Edited {call.args.get('path', 'file')}"
            elif call.name == "list_dir":
                action_desc = f"Listed directory {call.args.get('path', '.')}"
            elif call.name == "grep_search":
                action_desc = f"Search '{call.args.get('query', '')}'"
            elif call.name == "find_files":
                action_desc = f"Find files '{call.args.get('pattern', '*')}'"
            elif call.name == "run_command":
                action_desc = f"Executed '{call.args.get('command', '')[:40]}'"
            elif call.name in ("ask_user", "ask_question"):
                action_desc = f"Asked user: '{call.args.get('question', '')[:35]}...'"
            elif call.name in ("spawn_subagent", "delegate_task"):
                action_desc = f"Subagent [{call.args.get('role', 'worker')}]: {call.args.get('task', '')[:30]}"
            elif call.name == "inspect_image":
                action_desc = f"Inspected image {call.args.get('path', '')}"
            elif call.name in ("get_clipboard_image", "paste_clipboard_image"):
                action_desc = "Pasted image from clipboard"
            elif call.name == "done":
                action_desc = "Task finished"
                is_done = True

            bullet = f" [bold white]⬡[/bold white] {action_desc} [dim]{t_dur:.1f}s[/dim]"
            if ui:
                ui.append_history(bullet)
            else:
                print_step_bullet(action_desc, duration_sec=t_dur)

            session.add_tool_result(call.name, result)

            if is_done:
                break

        if is_done or should_stop():
            break


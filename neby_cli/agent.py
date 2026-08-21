import sys
import time
from typing import Callable, Optional

from .parser import parse_tool_calls
from .providers import stream_chat
from .session import Session
from .tools import execute_tool_call
from .ui import console, print_error, print_step_bullet, print_tool_call, print_tool_result


def run_agent_turn(session: Session, user_input: str, on_chunk: Optional[Callable[[str], None]] = None):
    session.add_user_message(user_input)
    step = 0

    while step < session.max_steps_per_turn:
        step += 1
        accumulated_text = ""
        start_time = time.time()
        
        try:
            for chunk in stream_chat(session.messages, provider=session.provider, model=session.model):
                c_type = chunk.get("type")
                if c_type == "text":
                    delta = chunk.get("content", "")
                    accumulated_text += delta
                    if on_chunk:
                        on_chunk(delta)
                    else:
                        sys.stdout.write(delta)
                        sys.stdout.flush()
                elif c_type == "error":
                    if not accumulated_text.strip():
                        print_error(chunk.get("error", "Unknown provider error"))
                        return
                    break
        except Exception as exc:
            if not accumulated_text.strip():
                print_error(f"Failed to generate response: {exc}")
                return

        elapsed = time.time() - start_time
        sys.stdout.write("\n")
        sys.stdout.flush()

        if not accumulated_text.strip():
            console.print("[dim]No response generated.[/dim]")
            return

        clean_text, tool_calls = parse_tool_calls(accumulated_text)
        session.add_assistant_message(accumulated_text)

        if not tool_calls:
            print_step_bullet("Completed", duration_sec=elapsed)
            break

        is_done = False
        for call in tool_calls:
            t_start = time.time()
            result = execute_tool_call(call.name, call.args)
            t_dur = time.time() - t_start
            success = not result.startswith("Error")
            
            # Format bullet action
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
            elif call.name == "run_command":
                action_desc = f"Executed '{call.args.get('command', '')[:30]}'"
            elif call.name == "done":
                action_desc = "Task finished"
                is_done = True
                
            print_step_bullet(action_desc, duration_sec=t_dur)
            session.add_tool_result(call.name, result)

            if is_done:
                break

        if is_done:
            break

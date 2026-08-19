import sys
from typing import Callable, Optional

from .parser import parse_tool_calls
from .providers import stream_chat
from .session import Session
from .tools import execute_tool_call
from .ui import console, print_error, print_tool_call, print_tool_result


def run_agent_turn(session: Session, user_input: str, on_chunk: Optional[Callable[[str], None]] = None):
    session.add_user_message(user_input)
    step = 0

    while step < session.max_steps_per_turn:
        step += 1
        accumulated_text = ""
        
        console.print(f"[dim]thinking ({session.provider}:{session.model})...[/dim]")
        
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

        sys.stdout.write("\n")
        sys.stdout.flush()

        if not accumulated_text.strip():
            console.print("[dim]No response generated.[/dim]")
            return

        clean_text, tool_calls = parse_tool_calls(accumulated_text)
        session.add_assistant_message(accumulated_text)

        if not tool_calls:
            break

        is_done = False
        for call in tool_calls:
            print_tool_call(call.name, call.args)
            result = execute_tool_call(call.name, call.args)
            success = not result.startswith("Error")
            print_tool_result(result, success=success)
            session.add_tool_result(call.name, result)
            if call.name == "done":
                is_done = True
                break

        if is_done:
            break

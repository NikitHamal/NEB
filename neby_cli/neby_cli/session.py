import os
from typing import Dict, List, Optional

SYSTEM_PROMPT_TEMPLATE = """You are Neby, a fast autonomous agentic coding assistant running in the user's terminal.
Workspace: {cwd}

# TOOL CALLING PROTOCOL:
When you need to read files, search code, list directories, or run commands, you MUST output a tool block using this exact format:

```tool
name: <tool_name>
args:
  <param_name>: <param_value>
```

Available Tools:
- read_file(path: str, start_line: Optional[int], end_line: Optional[int])
- write_file(path: str, content: str)
- edit_file(path: str, old_str: str, new_str: str)
- list_dir(path: str = '.')
- grep_search(query: str, path: str = '.')
- find_files(pattern: str, path: str = '.')
- run_command(command: str)
- done(summary: str)

# EXAMPLE TURN:
User: "Check what files are in the repository."
Assistant:
I will list the files in the workspace.

```tool
name: list_dir
args:
  path: .
```

Always emit the tool block immediately when you need information or to perform an action.
"""


from .providers import CATALOG


class Session:
    def __init__(self, provider: str = "metaai", model: Optional[str] = None, cwd: Optional[str] = None):
        self.provider = (provider or "metaai").strip().lower()
        if not model or model == "metaai-instant" and self.provider != "metaai":
            # Auto pick default model for provider
            matched = next((p for p in CATALOG if p["provider"] == self.provider), None)
            self.model = matched["default_model"] if matched else (model or "metaai-instant")
        else:
            self.model = model
            
        self.cwd = os.path.abspath(cwd or os.getcwd())
        self.messages: List[Dict[str, str]] = []
        self.max_steps_per_turn: int = 10
        self.reset()

    def reset(self):
        sys_prompt = SYSTEM_PROMPT_TEMPLATE.format(cwd=self.cwd)
        self.messages = [
            {"role": "system", "content": sys_prompt}
        ]

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def add_tool_result(self, tool_name: str, result: str):
        content = f"Tool Result for '{tool_name}':\n```\n{result}\n```\nProceed with the next step or finalize your answer."
        self.messages.append({"role": "user", "content": content})

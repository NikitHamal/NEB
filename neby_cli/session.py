import os
from typing import Dict, List, Optional

SYSTEM_PROMPT_TEMPLATE = """You are Neby, a fast autonomous agentic coding assistant running in the user's terminal.
Workspace: {cwd}

# TOOL CALLING PROTOCOL:
You inspect files, search codebase, edit files, and execute commands to solve the user's request.
To use a tool, output a tool call block using this exact format:

```tool
name: <tool_name>
args:
  <param_name>: <param_value>
```

Available Tools:
1. read_file:
   path: path to file (relative to workspace)
   start_line: optional starting line number (1-based)
   end_line: optional ending line number
2. write_file:
   path: path to file
   content: full content to write
3. edit_file:
   path: path to file
   old_str: exact text to replace
   new_str: new replacement text
4. list_dir:
   path: directory path (default '.')
5. grep_search:
   query: string to search in code files
6. find_files:
   pattern: glob pattern (e.g. '*.py')
7. run_command:
   command: shell command to run (e.g. pytest, npm test, python script)
8. git_diff:
   Show git diff of uncommitted changes.
9. done:
   summary: brief explanation of completed work.

# AGENT WORKFLOW GUIDELINES:
1. ALWAYS inspect and read relevant files before attempting to edit them.
2. Make minimal, precise changes. After editing, verify your changes if needed.
3. Emit one or two tool calls per step, then wait for the tool result before taking the next step.
4. When finished, summarize your solution clearly.
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

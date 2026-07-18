"""Background coding agent — autonomous agent that works on GitHub repos in the background.

Inspired by Google Jules / Cursor Agent / Tembo AI: each session gets its own
branch in a cloned copy of the connected repo, then an AI loops over a task
planning -> tool execution loop until the goal is achieved, with stop/pause/
resume/interrupt from the admin page.
"""
default_app_config = 'api.coding_agent.apps.CodingAgentConfig'

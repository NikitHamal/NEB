"""Qwen-optimized coding-agent harness (Hermes tool protocol + ACI observations)."""

from api.background_agent.qwen_harness.catalog import READONLY_TOOLS, advertised_tools, is_readonly
from api.background_agent.qwen_harness.execute import run_action_batches
from api.background_agent.qwen_harness.observe import compact_tool_content, format_tool_turn
from api.background_agent.qwen_harness.prompt import (
    build_system_prompt,
    build_user_prompt,
    format_repair_prompt,
    json_repair_prompt,
    render_hermes_transcript,
)
from api.background_agent.qwen_harness.recover import (
    action_signature,
    heal_note,
    needs_format_repair,
    thought_signature,
)

__all__ = [
    'READONLY_TOOLS',
    'action_signature',
    'advertised_tools',
    'build_system_prompt',
    'build_user_prompt',
    'compact_tool_content',
    'format_repair_prompt',
    'format_tool_turn',
    'heal_note',
    'is_readonly',
    'json_repair_prompt',
    'needs_format_repair',
    'render_hermes_transcript',
    'run_action_batches',
    'thought_signature',
]

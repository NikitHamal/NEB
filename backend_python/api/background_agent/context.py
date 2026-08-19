"""Anchored context accounting and automatic compaction for coding sessions."""
from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings

import json

from api.background_agent.attachments import prompt_attachment_block
from api.background_agent.events import emit
from api.background_agent.qwen_harness.observe import compact_tool_content
from api.models import BackgroundAgentMessage, BackgroundAgentSession
from api.utils import now_ms

COMPACTION_SYSTEM_PROMPT = """You are an anchored context summarization assistant for coding sessions.

Summarize only the conversation history you are given. The newest turns may be kept verbatim outside your summary, so focus on the older context that still matters for continuing the work.

If the prompt includes a <previous-summary> block, treat it as the current anchored summary. Update it with the new history by preserving still-true details, removing stale details, and merging in new facts.

Always follow the exact output structure requested by the user prompt. Keep every section, preserve exact file paths and identifiers when known, and prefer terse bullets over paragraphs.

Do not answer the conversation itself. Do not mention that you are summarizing, compacting, or merging context. Respond in the same language as the conversation."""

SUMMARY_STRUCTURE = """# Goal
# Repository and branches
# User requirements and constraints
# Work completed
# Files changed or inspected
# Commands and validation
# Current state
# Remaining work
# Important identifiers and exact paths
# Latest decisions and user guidance"""


@dataclass
class ContextSnapshot:
    transcript: str
    estimated_tokens: int
    window_tokens: int
    threshold_tokens: int
    percent: int


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def context_window_tokens() -> int:
    return max(16000, int(getattr(settings, 'BACKGROUND_AGENT_CONTEXT_WINDOW_TOKENS', 131072)))


def context_threshold() -> float:
    value = float(getattr(settings, 'BACKGROUND_AGENT_CONTEXT_COMPACTION_THRESHOLD', 0.80))
    return min(0.95, max(0.50, value))


def _message_kind(message: BackgroundAgentMessage) -> str:
    try:
        return str(json.loads(message.metadata or '{}').get('kind') or '')
    except (TypeError, json.JSONDecodeError):
        return ''


def _format_message(message: BackgroundAgentMessage, per_message_chars: int = 40000) -> str:
    content = message.content or ''
    if (message.role or '') == 'tool':
        content = compact_tool_content(content, cap=min(per_message_chars, 8000))
    if len(content) > per_message_chars:
        content = content[:per_message_chars] + '\n[message truncated for context]'
    attachment_block = prompt_attachment_block(message)
    suffix = f'\n{attachment_block}' if attachment_block else ''
    return f'{message.role.upper()} [{message.id}]: {content}{suffix}'


def recent_rows(session: BackgroundAgentSession) -> list[BackgroundAgentMessage]:
    qs = session.messages.order_by('created_at', 'id')
    if session.context_compacted_at:
        qs = qs.filter(created_at__gt=session.context_compacted_at)
    rows = []
    for row in qs:
        if _message_kind(row) == 'model_prompt':
            continue
        rows.append(row)
    return rows


def build_snapshot(session: BackgroundAgentSession, fixed_prompt: str = '', format_message=None, rows_as_transcript: bool = False) -> ContextSnapshot:
    rows = recent_rows(session)
    if rows_as_transcript and format_message is not None:
        transcript = format_message(rows)
    elif format_message is not None:
        transcript = '\n\n'.join(format_message(row) for row in rows)
    else:
        transcript = '\n\n'.join(_format_message(row) for row in rows)
    if session.context_summary:
        transcript = f'<anchored-summary>\n{session.context_summary}\n</anchored-summary>\n\n{transcript}'
    window = max(16000, int(session.context_window_tokens or context_window_tokens()))
    tokens = estimate_tokens(fixed_prompt) + estimate_tokens(transcript)
    threshold = int(window * context_threshold())
    return ContextSnapshot(
        transcript=transcript,
        estimated_tokens=tokens,
        window_tokens=window,
        threshold_tokens=threshold,
        percent=min(100, round(tokens * 100 / window)),
    )


def _split_for_compaction(rows: list[BackgroundAgentMessage], keep_tokens: int) -> tuple[list[BackgroundAgentMessage], list[BackgroundAgentMessage]]:
    if len(rows) <= 6:
        return [], rows
    kept: list[BackgroundAgentMessage] = []
    used = 0
    for row in reversed(rows):
        row_tokens = estimate_tokens(_format_message(row, per_message_chars=24000))
        if len(kept) >= 6 and used + row_tokens > keep_tokens:
            break
        kept.append(row)
        used += row_tokens
    kept.reverse()
    split_index = max(0, len(rows) - len(kept))
    return rows[:split_index], rows[split_index:]


def _run_compaction(session: BackgroundAgentSession, fixed_prompt: str, compact_call, old_rows, *, manual: bool) -> bool:
    """Summarize old rows into the anchored summary. Returns True when it ran."""
    history = '\n\n'.join(_format_message(row, per_message_chars=30000) for row in old_rows)
    previous = session.context_summary or '(none)'
    prompt = f"""Update the anchored coding-session summary using the exact headings below.
Do not add headings, preambles, conclusions, or markdown fences outside this structure.

{SUMMARY_STRUCTURE}

<previous-summary>
{previous}
</previous-summary>

<conversation-history>
{history}
</conversation-history>
"""
    snapshot = build_snapshot(session, fixed_prompt)
    emit(session, 'context.compacting', 'Manual compaction requested (/compact)' if manual else 'Context reached the compaction threshold', {
        'estimatedTokens': snapshot.estimated_tokens,
        'windowTokens': snapshot.window_tokens,
        'thresholdPercent': round(context_threshold() * 100),
        'messages': len(old_rows),
        'manual': manual,
    })
    summary = (compact_call(COMPACTION_SYSTEM_PROMPT, prompt) or '').strip()
    if not summary:
        emit(session, 'context.compact_failed', 'The summarizer returned an empty response; context was left unchanged', {'manual': manual})
        return False
    session.context_summary = summary[:120000]
    session.context_compacted_at = old_rows[-1].created_at
    session.context_compactions += 1
    session.last_compaction_at = now_ms()
    session.save(update_fields=[
        'context_summary', 'context_compacted_at', 'context_compactions', 'last_compaction_at',
    ])
    emit(session, 'context.compacted', 'Older context was compacted into an anchored summary' + (' (manual)' if manual else ''), {
        'compactions': session.context_compactions,
        'compactedThrough': session.context_compacted_at,
        'manual': manual,
    })
    snapshot = build_snapshot(session, fixed_prompt)
    session.context_tokens_estimate = snapshot.estimated_tokens
    session.context_window_tokens = snapshot.window_tokens
    session.save(update_fields=['context_tokens_estimate', 'context_window_tokens'])
    return True


def compact_now(session: BackgroundAgentSession, fixed_prompt: str, compact_call, *, manual: bool = True) -> bool:
    """Force an anchored compaction right now (the /compact command), ignoring the threshold."""
    snapshot = build_snapshot(session, fixed_prompt)
    rows = recent_rows(session)
    old_rows, _ = _split_for_compaction(rows, max(6000, int(snapshot.window_tokens * 0.18)))
    if len(old_rows) < 2:
        emit(session, 'context.compact_skipped', 'Not enough accumulated history to compact yet', {'manual': manual, 'messages': len(rows)})
        return False
    return _run_compaction(session, fixed_prompt, compact_call, old_rows, manual=manual)


def compact_if_needed(session: BackgroundAgentSession, fixed_prompt: str, compact_call) -> ContextSnapshot:
    snapshot = build_snapshot(session, fixed_prompt)
    session.context_tokens_estimate = snapshot.estimated_tokens
    session.context_window_tokens = snapshot.window_tokens
    session.save(update_fields=['context_tokens_estimate', 'context_window_tokens'])
    if snapshot.estimated_tokens < snapshot.threshold_tokens:
        return snapshot

    rows = recent_rows(session)
    old_rows, _ = _split_for_compaction(rows, max(6000, int(snapshot.window_tokens * 0.18)))
    if not old_rows:
        return snapshot

    _run_compaction(session, fixed_prompt, compact_call, old_rows, manual=False)
    snapshot = build_snapshot(session, fixed_prompt)
    session.context_tokens_estimate = snapshot.estimated_tokens
    session.context_window_tokens = snapshot.window_tokens
    session.save(update_fields=['context_tokens_estimate', 'context_window_tokens'])
    return snapshot

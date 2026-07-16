"""AI provider adapter for the background coding agent.

Adapts the existing reverse-engineered AI providers (AI4Bharat, Qwen, DeepAI, etc.)
to work as a coding agent. Since these providers don't support native tool calling,
we use a structured prompt approach where the AI outputs tool calls in a JSON format.

The adapter sends the conversation (system prompt + history) and returns the
raw text response, which is then parsed by prompts.parse_ai_response().
"""
import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

MAX_CONTEXT_MESSAGES = 30
MAX_MESSAGE_CHARS = 4000
MAX_RESPONSE_CHARS = 8000


def _truncate_history(messages):
    """Keep only the most recent messages to fit context window limits."""
    if len(messages) <= MAX_CONTEXT_MESSAGES:
        return messages
    system_msgs = [m for m in messages if m.get('role') == 'system']
    other_msgs = [m for m in messages if m.get('role') != 'system']
    recent = other_msgs[-(MAX_CONTEXT_MESSAGES - len(system_msgs)):]
    return system_msgs + recent


def _truncate_content(content, max_chars=MAX_MESSAGE_CHARS):
    if len(content) <= max_chars:
        return content
    return content[:max_chars] + '\n... (truncated)'


def call_ai4bharat(messages, model_id=None):
    """Call AI4Bharat Arena provider with the full conversation.
    
    Uses simple_chat for single-turn or creates a session for multi-turn.
    Returns the raw text response.
    """
    from api.ai4bharat_proxy import (
        acquire_token, fetch_models_for_client, create_session,
        stream_chat, new_message_id, commit_token_use, ArenaError,
    )
    
    system_prompt = ''
    user_content_parts = []
    
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role == 'system':
            system_prompt = content
        elif role == 'user':
            user_content_parts.append(f'[User]\n{content}')
        elif role == 'assistant':
            user_content_parts.append(f'[Assistant]\n{content}')
        elif role == 'tool_result':
            user_content_parts.append(f'[Tool Results]\n{content}')
    
    combined_user = '\n\n'.join(user_content_parts)
    combined_user = _truncate_content(combined_user, 60000)
    
    full_content = combined_user
    if system_prompt:
        full_content = f"[System Instructions]\n{system_prompt}\n\n{combined_user}"
    
    entry = acquire_token(require_low_budget=False)
    models = fetch_models_for_client(entry['token'])
    
    if model_id:
        match = next((m for m in models if m['id'] == model_id and m['active']), None)
        if not match:
            fallback = next((m for m in models if m['active'] and not m['random_only']), None)
            if fallback:
                model_id = fallback['id']
            else:
                raise ArenaError('no active model available')
    else:
        pick = next((m for m in models if m['active'] and not m['random_only']), None)
        if not pick:
            raise ArenaError('no active LLM model available')
        model_id = pick['id']
    
    sess = create_session(entry['token'], model_id)
    u, a = new_message_id(), new_message_id()
    
    full = ''
    for chunk in stream_chat(
        token=entry['token'],
        session_id=sess['id'],
        user_content=full_content,
        model_id=model_id,
        user_message_id=u,
        assistant_message_id=a,
        parent_message_ids=[],
        timeout=120,
    ):
        if chunk['type'] == 'content':
            full += chunk['text']
        elif chunk['type'] == 'error':
            logger.error('ai4bharat coding agent: upstream error: %s', chunk.get('message'))
            return f'{{"thoughts": "AI provider error: {chunk.get("message", "unknown")}", "actions": [], "status": "error"}}'
    
    commit_token_use(entry['token'], message_used=True, session_opened=True)
    return (full or '').strip()[:MAX_RESPONSE_CHARS]


def call_qwen(messages, model_id=None):
    """Call Qwen provider with the full conversation."""
    try:
        from api.qwen_utils.client import QwenClient
        client = QwenClient()
        chat = client.create_chat(model or 'qwen-max')
        
        system_prompt = ''
        for msg in messages:
            if msg.get('role') == 'system':
                system_prompt = msg.get('content', '')
                break
        
        user_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                continue
            user_parts.append(content)
        
        combined = '\n\n'.join(user_parts)
        combined = _truncate_content(combined, 60000)
        if system_prompt:
            combined = f"{system_prompt}\n\n{combined}"
        
        result = client.send_message(chat, combined, system_prompt=system_prompt)
        return (result or '').strip()[:MAX_RESPONSE_CHARS]
    except Exception as e:
        logger.warning('Qwen provider failed, falling back to ai4bharat: %s', e)
        return call_ai4bharat(messages, model_id)


def call_deepai(messages, model_id=None):
    """Call DeepAI provider."""
    try:
        from api.deepai_proxy import DeepAIClient
        client = DeepAIClient()
        
        system_prompt = ''
        user_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                system_prompt = content
            else:
                user_parts.append(content)
        
        combined = '\n\n'.join(user_parts)
        combined = _truncate_content(combined, 60000)
        
        result = client.chat(combined, system_prompt=system_prompt)
        return (result or '').strip()[:MAX_RESPONSE_CHARS]
    except Exception as e:
        logger.warning('DeepAI provider failed, falling back to ai4bharat: %s', e)
        return call_ai4bharat(messages, model_id)


PROVIDERS = {
    'ai4bharat': call_ai4bharat,
    'qwen': call_qwen,
    'deepai': call_deepai,
    'egov': call_ai4bharat,
}


def call_provider(provider, messages, model_id=None):
    """Call the specified AI provider with conversation messages.
    
    Args:
        provider: 'ai4bharat', 'qwen', 'deepai', or 'egov'
        messages: list of {'role': ..., 'content': ...} dicts
        model_id: optional model ID for the provider
    
    Returns: raw text response from the AI
    """
    messages = _truncate_history(messages)
    
    func = PROVIDERS.get(provider, call_ai4bharat)
    
    for attempt in range(2):
        try:
            result = func(messages, model_id)
            if result:
                return result
            logger.warning('Provider %s returned empty (attempt %d)', provider, attempt + 1)
        except Exception as e:
            logger.warning('Provider %s failed (attempt %d): %s', provider, attempt + 1, e)
            if attempt == 0 and provider != 'ai4bharat':
                logger.info('Falling back to ai4bharat provider')
                return call_ai4bharat(messages, model_id)
    
    return '{"thoughts": "All AI providers failed. Unable to generate a response.", "actions": [], "status": "error"}'

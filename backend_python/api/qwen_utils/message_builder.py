"""
Qwen message builder — construct the chat completion payload for Qwen API,
including file attachments and feature configuration.

Ported from flashy/backend/providers/qwen_utils/message_builder.py but
simplified for the NEBians use case (no tools/pass-through).
"""
import uuid
from typing import Any, Dict, List, Optional


def build_feature_config(
    thinking_enabled: bool = False,
    thinking_mode: str = "Auto",
    chat_type: str = "t2t",
) -> Dict[str, Any]:
    if thinking_enabled:
        return {
            "auto_thinking": thinking_mode == "Auto",
            "thinking_mode": thinking_mode,
            "thinking_enabled": True,
            "output_schema": "phase",
            "research_mode": "normal" if chat_type != "deep_research" else "deep",
            "auto_search": chat_type in ("search", "deep_research"),
        }
    return {
        "thinking_enabled": False,
        "output_schema": "phase",
        "thinking_budget": 81920,
    }


def resolve_chat_mode(chat_type: str) -> str:
    if chat_type == "search":
        return "search"
    if chat_type == "deep_research":
        return "deep_research"
    if chat_type == "artifacts":
        return "artifacts"
    if chat_type == "web_dev":
        return "web_dev"
    return "normal"


def build_msg_payload(
    chat_id: str,
    model: str,
    full_prompt: str,
    parent_id: Optional[str],
    uploaded_files: List[dict],
    chat_type: str = "t2t",
    chat_mode: str = "normal",
    feature_config: Optional[Dict[str, Any]] = None,
    stream: bool = True,
) -> Dict[str, Any]:
    msg_id = str(uuid.uuid4())
    if feature_config is None:
        feature_config = build_feature_config(thinking_enabled=False)
    return {
        "stream": stream,
        "incremental_output": stream,
        "chat_id": chat_id,
        "chat_mode": chat_mode,
        "model": model,
        "parent_id": parent_id,
        "messages": [
            {
                "fid": msg_id,
                "parentId": parent_id,
                "childrenIds": [],
                "role": "user",
                "content": full_prompt,
                "user_action": "chat",
                "files": uploaded_files,
                "models": [model],
                "chat_type": chat_type,
                "feature_config": feature_config,
                "sub_chat_type": chat_type,
                "safety": {
                    "enabled": False,
                },
                "extra": {
                    "disable_recitation_policy": True,
                    "skip_safety_check": True,
                },
            }
        ],
    }
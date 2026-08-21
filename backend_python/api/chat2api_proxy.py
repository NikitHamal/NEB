import json
import logging
import os
from typing import Any, Dict, Generator, List, Optional
import requests

logger = logging.getLogger(__name__)

FLASHY_CONFIG_PATH = r"F:\flashy\config.json"


def load_flashy_config() -> Dict[str, Any]:
    if os.path.exists(FLASHY_CONFIG_PATH):
        try:
            with open(FLASHY_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def get_chat2api_settings() -> tuple[str, str]:
    config = load_flashy_config()
    base_url = os.getenv("CHAT2API_BASE_URL") or config.get("chat2api_base_url") or "http://127.0.0.1:8080"
    api_key = os.getenv("CHAT2API_API_KEY") or config.get("chat2api_api_key") or ""
    return base_url.rstrip("/"), api_key


def list_models() -> List[Dict[str, Any]]:
    base_url, api_key = get_chat2api_settings()
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        resp = requests.get(f"{base_url}/v1/models", headers=headers, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("data", [])
    except Exception:
        pass
    return [
        {"id": "deepseek-v4-flash", "name": "DeepSeek V4 Flash"},
        {"id": "deepseek-v4-pro", "name": "DeepSeek V4 Pro"},
        {"id": "deepseek-chat", "name": "DeepSeek Chat (V3.2)"},
        {"id": "deepseek-reasoner", "name": "DeepSeek Reasoner (R1)"},
        {"id": "kimi", "name": "Kimi Moonshot"},
        {"id": "glm-4", "name": "Zhipu GLM-4"},
        {"id": "minimax", "name": "MiniMax M2.5"},
    ]


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "deepseek-v4-flash",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.6,
) -> Generator[Dict[str, Any], None, None]:
    cfg_base_url, cfg_api_key = get_chat2api_settings()
    base_url = (base_url or cfg_base_url).rstrip("/")
    api_key = api_key or cfg_api_key

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
    }

    try:
        with requests.post(
            f"{base_url}/v1/chat/completions",
            json=payload,
            headers=headers,
            stream=True,
            timeout=(5, 60),
        ) as resp:
            if resp.status_code != 200:
                err_text = resp.text[:300]
                yield {"type": "error", "error": f"Chat2API returned HTTP {resp.status_code}: {err_text}"}
                return

            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        choices = chunk.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            content = delta.get("content") or delta.get("reasoning_content") or ""
                            if content:
                                yield {"type": "text", "content": content}
                    except Exception:
                        continue

            yield {"type": "done"}
    except requests.exceptions.ConnectionError:
        yield {
            "type": "error",
            "error": f"Could not connect to Chat2API server at {base_url}. Make sure Chat2API app or service is running.",
        }
    except Exception as exc:
        yield {"type": "error", "error": str(exc)}

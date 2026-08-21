import json
import logging
import os
from typing import Any, Dict, Generator, List, Optional
import requests

logger = logging.getLogger(__name__)

OFFICIAL_API_BASE = "https://api.deepseek.com"
CONFIG_PATH = os.path.expanduser("~/.neby_config.json")


def load_neby_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_neby_config(config: Dict[str, Any]):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass


def get_deepseek_credentials() -> tuple[str, str]:
    config = load_neby_config()
    api_key = os.getenv("DEEPSEEK_API_KEY") or config.get("deepseek_api_key") or ""
    base_url = os.getenv("DEEPSEEK_BASE_URL") or config.get("deepseek_base_url") or OFFICIAL_API_BASE
    return api_key, base_url.rstrip("/")


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "deepseek-v4-flash",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    temperature: float = 0.6,
) -> Generator[Dict[str, Any], None, None]:
    cfg_api_key, cfg_base_url = get_deepseek_credentials()
    api_key = api_key or cfg_api_key
    base_url = (base_url or cfg_base_url).rstrip("/")

    # Normalize model IDs
    if model in ("flash", "v4-flash", "fast"):
        model = "deepseek-v4-flash"
    elif model in ("pro", "v4-pro", "coder", "reasoner"):
        model = "deepseek-v4-pro"
    elif model in ("v4", "default"):
        model = "deepseek-v4"

    if not api_key:
        # Check if we have public fallback or prompt user to configure key
        yield {
            "type": "error",
            "error": "DeepSeek API key not found. Set DEEPSEEK_API_KEY env var or add 'deepseek_api_key' to ~/.neby_config.json",
        }
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
    }

    try:
        with requests.post(
            f"{base_url}/chat/completions",
            json=payload,
            headers=headers,
            stream=True,
            timeout=(5, 60),
        ) as resp:
            if resp.status_code != 200:
                err_text = resp.text[:300]
                yield {"type": "error", "error": f"DeepSeek API error HTTP {resp.status_code}: {err_text}"}
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
    except Exception as exc:
        yield {"type": "error", "error": str(exc)}

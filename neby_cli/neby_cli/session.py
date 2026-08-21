import os
from typing import Any, Dict, List, Optional
from .providers import CATALOG
from .harness import build_system_prompt, trim_messages_to_window



MODES = ["Agent", "Plan", "Ask"]


class Session:
    def __init__(self, provider: str = "metaai", model: Optional[str] = None, cwd: Optional[str] = None):
        self.provider = (provider or "metaai").strip().lower()
        if not model or model == "metaai-instant" and self.provider != "metaai":
            matched = next((p for p in CATALOG if p["provider"] == self.provider), None)
            self.model = matched["default_model"] if matched else (model or "metaai-instant")
        else:
            self.model = model
            
        self.cwd = os.path.abspath(cwd or os.getcwd())
        self.messages: List[Dict[str, str]] = []
        self.attached_images: List[Dict[str, Any]] = []
        self.max_steps_per_turn: int = 10
        self.mode_index: int = 0
        self.thinking_effort: str = "balanced"  # quick | balanced | deep
        self.files_edited_count: int = 0
        self.reset()

    @property
    def mode(self) -> str:
        return MODES[self.mode_index]

    def cycle_mode(self) -> str:
        self.mode_index = (self.mode_index + 1) % len(MODES)
        return self.mode

    def cycle_effort(self) -> str:
        order = ["quick", "balanced", "deep"]
        try:
            idx = order.index(self.thinking_effort)
        except ValueError:
            idx = 1
        self.thinking_effort = order[(idx + 1) % len(order)]
        return self.thinking_effort

    def set_effort(self, effort: str) -> str:
        e = (effort or "").strip().lower()
        if e in ("quick", "balanced", "deep"):
            self.thinking_effort = e
        return self.thinking_effort

    def reset(self):
        sys_prompt = build_system_prompt(
            provider=self.provider,
            model=self.model,
            cwd=self.cwd,
            mode=self.mode,
        )
        self.messages = [{"role": "system", "content": sys_prompt}]
        self.attached_images = []
        self.files_edited_count = 0

    def attach_image(self, img_info: Dict[str, Any]):
        if img_info and img_info not in self.attached_images:
            self.attached_images.append(img_info)

    def clear_images(self):
        self.attached_images = []

    def get_trimmed_messages(self) -> List[Dict[str, str]]:
        return trim_messages_to_window(self.messages, self.provider)

    def add_user_message(self, content: str):
        if self.attached_images:
            img_descriptions = []
            for img in self.attached_images:
                fn = img.get("filename", "image")
                p = img.get("path", "")
                w = img.get("width", 0)
                h = img.get("height", 0)
                img_descriptions.append(f"[Attached Image: {fn} ({w}x{h} px) at '{p}']")
            img_block = "\n".join(img_descriptions)
            content = f"{img_block}\n\n{content}"
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def add_tool_result(self, tool_name: str, result: str):
        if tool_name in ("write_file", "edit_file"):
            self.files_edited_count += 1
        content = f"Tool Result for '{tool_name}':\n```\n{result}\n```\nProceed with the next step or finalize your answer."
        self.messages.append({"role": "user", "content": content})

    def get_model_display_name(self) -> str:
        for p in CATALOG:
            if p["provider"].lower() == self.provider.lower():
                for m in p.get("models", []):
                    if m["id"].lower() == self.model.lower():
                        return m.get("name", self.model)
        return f"{self.provider}:{self.model}"

    def get_context_percent(self) -> int:
        total_chars = sum(len(m.get("content", "")) for m in self.messages)
        # Context window baseline: 128k tokens (~480k chars)
        window_chars = 480000.0
        pct = max(1, min(99, int((total_chars / window_chars) * 100) + 1))
        return pct

    def rebuild_system_prompt(self):
        if self.messages and self.messages[0].get("role") == "system":
            self.messages[0]["content"] = build_system_prompt(
                provider=self.provider,
                model=self.model,
                cwd=self.cwd,
                mode=self.mode,
            )

    def is_vision_supported(self) -> bool:
        p = self.provider.lower()
        m = (self.model or "").lower()
        if p in ("qwen", "openai", "gemini", "anthropic", "egov", "metaai", "deepai"):
            return True
        if "vl" in m or "vision" in m or "vision" in p or "4o" in m:
            return True
        return False

    def get_attached_image_paths(self) -> List[str]:
        return [img.get("path", "") for img in self.attached_images if img.get("path")]

    def get_vision_messages(self) -> List[Dict[str, Any]]:
        base = self.get_trimmed_messages()
        if not self.attached_images or not self.is_vision_supported():
            return base
        last_user_idx = None
        for i in range(len(base) - 1, -1, -1):
            if base[i].get("role") == "user":
                last_user_idx = i
                break
        if last_user_idx is None:
            return base
        content = base[last_user_idx].get("content", "")
        parts: List[Dict[str, Any]] = [{"type": "text", "text": content}] if isinstance(content, str) else []
        for img in self.attached_images:
            b64 = img.get("base64", "")
            mime = img.get("mime_type", "image/png")
            if b64:
                parts.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}})
            elif img.get("path"):
                parts.append({"type": "image_url", "image_url": {"url": img["path"]}})
        new_base = list(base)
        new_base[last_user_idx] = {"role": "user", "content": parts}
        return new_base


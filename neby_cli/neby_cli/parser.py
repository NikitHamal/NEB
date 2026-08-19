import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ToolCall:
    name: str
    args: Dict[str, Any] = field(default_factory=dict)
    raw: str = ""


_FENCE_RE = re.compile(r"```(?:tool|json|yaml)?\s*\n([\s\S]*?)\n```", re.IGNORECASE)
_XML_RE = re.compile(r"<tool_call>([\s\S]*?)</tool_call>", re.IGNORECASE)
_JSON_TOOL_RE = re.compile(r'\{[\s\r\n]*"(?:name|tool|function)"[\s\r\n]*:[\s\S]*?\}')


def _clean_json_str(s: str) -> str:
    s = s.strip()
    s = re.sub(r'"""+', '"', s)
    return s


def _parse_yaml_lines(text: str) -> Tuple[str, Dict[str, Any]]:
    lines = text.splitlines()
    name = ""
    args = {}
    in_args = False
    current_key = ""
    current_val_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        m_name = re.match(r'^(?:name|tool)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)["\']?', stripped, re.IGNORECASE)
        if m_name and not in_args:
            name = m_name.group(1).lower()
            continue
            
        if re.match(r'^(?:args|arguments|parameters)\s*[:=]', stripped, re.IGNORECASE):
            in_args = True
            continue
            
        m_kv = re.match(r'^([a-zA-Z0-9_\-]+)\s*[:=]\s*(.*)$', stripped)
        if m_kv:
            if current_key and current_val_lines:
                args[current_key] = "\n".join(current_val_lines).strip()
                current_val_lines = []
            
            k = m_kv.group(1)
            v = m_kv.group(2).strip().strip("'\"")
            current_key = k
            if v in ("|", "|2", ">"):
                current_val_lines = []
            else:
                args[k] = v
        elif current_key:
            current_val_lines.append(line.rstrip())
            
    if current_key and current_val_lines:
        args[current_key] = "\n".join(current_val_lines).strip()
        
    return name, args


def parse_tool_calls(text: str) -> Tuple[str, List[ToolCall]]:
    if not text:
        return "", []
    
    calls: List[ToolCall] = []
    clean_text = text
    
    for m in _XML_RE.finditer(text):
        raw = m.group(1).strip()
        clean_text = clean_text.replace(m.group(0), "")
        try:
            parsed = json.loads(_clean_json_str(raw))
            name = parsed.get("name") or parsed.get("tool") or ""
            args = parsed.get("arguments") or parsed.get("args") or parsed.get("parameters") or parsed
            if isinstance(args, dict) and "name" in args:
                del args["name"]
            if name:
                calls.append(ToolCall(name=name, args=args if isinstance(args, dict) else {}, raw=raw))
                continue
        except Exception:
            pass
        name_m = re.search(r"<name>([\s\S]*?)</name>", raw)
        args_m = re.search(r"<(?:arguments|args|parameters)>([\s\S]*?)</(?:arguments|args|parameters)>", raw)
        if name_m:
            name = name_m.group(1).strip()
            args_raw = args_m.group(1).strip() if args_m else "{}"
            try:
                args = json.loads(args_raw)
            except Exception:
                _, args = _parse_yaml_lines(args_raw)
            calls.append(ToolCall(name=name, args=args if isinstance(args, dict) else {}, raw=raw))

    for m in _FENCE_RE.finditer(text):
        raw = m.group(1).strip()
        clean_text = clean_text.replace(m.group(0), "")
        try:
            parsed = json.loads(_clean_json_str(raw))
            if isinstance(parsed, dict):
                name = parsed.get("name") or parsed.get("tool") or ""
                args = parsed.get("arguments") or parsed.get("args") or parsed.get("parameters") or parsed
                if isinstance(args, dict) and "name" in args:
                    del args["name"]
                if name:
                    calls.append(ToolCall(name=name, args=args if isinstance(args, dict) else {}, raw=raw))
                    continue
        except Exception:
            pass
        name, args = _parse_yaml_lines(raw)
        if name:
            calls.append(ToolCall(name=name, args=args, raw=raw))

    if not calls:
        for m in _JSON_TOOL_RE.finditer(text):
            raw = m.group(0).strip()
            try:
                parsed = json.loads(_clean_json_str(raw))
                if isinstance(parsed, dict):
                    name = parsed.get("name") or parsed.get("tool") or ""
                    args = parsed.get("arguments") or parsed.get("args") or parsed.get("parameters") or parsed
                    if isinstance(args, dict) and "name" in args:
                        del args["name"]
                    if name:
                        calls.append(ToolCall(name=name, args=args if isinstance(args, dict) else {}, raw=raw))
                        clean_text = clean_text.replace(raw, "")
            except Exception:
                pass

    return clean_text.strip(), calls

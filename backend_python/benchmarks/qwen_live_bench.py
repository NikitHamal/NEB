#!/usr/bin/env python3
"""Live Qwen3.8-Max harness bench against chat.qwen.ai.

Does not use the NEBians HTTP API. Talks to Qwen with the local reverse
proxy (api/qwen_proxy.py) and scores JSON vs Hermes protocols on real
model output.

    QWEN_DISABLE_POOL_REFILL=1 python benchmarks/qwen_live_bench.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("QWEN_DISABLE_POOL_REFILL", "1")

from api.background_agent.protocol import parse_model_response
from api.background_agent.qwen_harness.prompt import build_system_prompt
from api.qwen_proxy import call_qwen, probe_qwen

MODEL = os.environ.get("QWEN_LIVE_MODEL", "qwen3.8-max")
MAX_TURNS = int(os.environ.get("QWEN_LIVE_TURNS", "6"))

JSON_SYSTEM = """You are a coding agent. Respond with exactly one JSON object and nothing else:
{"thought":"...","actions":[{"tool":"TOOL","arguments":{...}}],"final":"","summary":"..."}
Tools: list_files(path), read_file(path), write_file(path, content), edit_file(path, old_text, new_text), done via non-empty final.
Inspect before editing. When finished set final and leave actions empty."""


def hermes_system():
    return build_system_prompt("Qwen 3.8 Max")


class MiniWorkspace:
    def __init__(self, root: Path):
        self.root = root
        (root / "README.md").write_text("tiny calc\n", encoding="utf-8")
        (root / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")

    def list_files(self, path="."):
        base = (self.root / path).resolve()
        rows = []
        for item in sorted(base.rglob("*")):
            if item.is_file():
                rows.append(item.relative_to(self.root).as_posix())
        return {"entries": rows}

    def read_file(self, path, start_line=1, end_line=200):
        text = (self.root / path).read_text(encoding="utf-8").splitlines()
        start = max(1, int(start_line))
        end = max(start, int(end_line))
        view = "\n".join(f"{i:>4}|{text[i-1]}" for i in range(start, min(end, len(text)) + 1))
        return {"path": path, "view": view, "totalLines": len(text)}

    def write_file(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(content), encoding="utf-8")
        return {"path": path, "bytes": len(str(content))}

    def edit_file(self, path, old_text, new_text, replace_all=False):
        text = (self.root / path).read_text(encoding="utf-8")
        if old_text not in text:
            return {"ok": False, "error": "old_text not found"}
        count = text.count(old_text)
        if count > 1 and not replace_all:
            return {"ok": False, "error": f"old_text matches {count} locations"}
        (self.root / path).write_text(text.replace(old_text, new_text), encoding="utf-8")
        return {"ok": True, "replacements": 1 if not replace_all else count}

    def execute(self, action):
        tool = action.get("tool")
        args = action.get("arguments") or {}
        handlers = {
            "list_files": self.list_files,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "edit_file": self.edit_file,
            "glob_files": lambda pattern="*", path=".": self.list_files(path),
            "search_text": lambda query, path=".", **kw: {
                "matches": [
                    f"{p}:{i}:{line}"
                    for p in self.list_files(path)["entries"]
                    for i, line in enumerate((self.root / p).read_text(encoding="utf-8").splitlines(), 1)
                    if query in line
                ]
            },
        }
        if tool not in handlers:
            return {"ok": False, "tool": tool, "error": f"unknown tool {tool}"}
        try:
            return {"ok": True, "tool": tool, "result": handlers[tool](**args)}
        except TypeError as exc:
            return {"ok": False, "tool": tool, "error": str(exc)}
        except Exception as exc:
            return {"ok": False, "tool": tool, "error": str(exc)}


def ask(system, user, thinking="fast"):
    t0 = time.monotonic()
    raw = call_qwen(
        system_prompt=system,
        user_message=user,
        model=MODEL,
        max_tokens=4000,
        thinking_mode=thinking,
    )
    ms = int((time.monotonic() - t0) * 1000)
    return raw, ms


def score_parse(raw, expect_tool=None):
    parsed = parse_model_response(raw or "")
    tools = [a["tool"] for a in parsed.actions]
    hit = True
    if expect_tool:
        hit = expect_tool in tools or (expect_tool == "done" and bool(parsed.final))
    return {
        "parse_ok": parsed.parse_ok,
        "protocol": parsed.protocol,
        "tools": tools,
        "final": bool(parsed.final),
        "hit": hit,
        "chars": len(raw or ""),
    }


def protocol_pings():
    rows = []
    cases = [
        (
            "json_list",
            JSON_SYSTEM,
            'Call list_files on path "." . Return only the JSON object.',
            "list_files",
            "json",
        ),
        (
            "hermes_list",
            hermes_system(),
            'Call list_files with path "." . Use a <tool_call> block and nothing else.',
            "list_files",
            "hermes",
        ),
        (
            "json_done",
            JSON_SYSTEM,
            "The task is already complete. Set final to 'complete' and use no actions.",
            "done",
            "json",
        ),
        (
            "hermes_done",
            hermes_system(),
            "The task is already complete. Call done with summary 'complete'.",
            "done",
            "hermes",
        ),
    ]
    for name, system, user, expect, _family in cases:
        raw, ms = ask(system, user, thinking="fast")
        scored = score_parse(raw, expect)
        scored.update({"name": name, "ms": ms, "empty": raw is None})
        rows.append(scored)
        print(
            f"PING {name:14} empty={scored['empty']} parse_ok={scored['parse_ok']} "
            f"proto={scored['protocol']:8} hit={scored['hit']} tools={scored['tools']} {ms}ms",
            flush=True,
        )
        if raw:
            print("  RAW", (raw[:240] + ("…" if len(raw) > 240 else "")).replace("\n", "\\n"), flush=True)
    return rows


def coding_loop(protocol):
    tmp = Path(tempfile.mkdtemp(prefix=f"qwen-live-{protocol}-"))
    ws = MiniWorkspace(tmp)
    system = hermes_system() if protocol == "hermes" else JSON_SYSTEM
    goal = (
        "Fix calc.py so add(a, b) returns a + b, not a - b. "
        "Read the file first, edit it, then finish."
    )
    transcript = [f"GOAL\n{goal}\n\nFILES\n{ws.list_files()['entries']}"]
    stats = {
        "protocol": protocol,
        "turns": 0,
        "parse_ok": 0,
        "tool_ok": 0,
        "tool_fail": 0,
        "empty": 0,
        "fixed": False,
        "done": False,
        "ms": 0,
    }
    try:
        for turn in range(1, MAX_TURNS + 1):
            stats["turns"] = turn
            raw, ms = ask(system, "\n\n".join(transcript), thinking="auto")
            stats["ms"] += ms
            if not raw:
                stats["empty"] += 1
                print(f"LOOP {protocol} turn {turn} EMPTY {ms}ms", flush=True)
                continue
            parsed = parse_model_response(raw)
            stats["parse_ok"] += int(parsed.parse_ok)
            print(
                f"LOOP {protocol} turn {turn} proto={parsed.protocol} "
                f"tools={[a['tool'] for a in parsed.actions]} final={bool(parsed.final)} {ms}ms",
                flush=True,
            )
            print("  RAW", (raw[:300] + ("…" if len(raw) > 300 else "")).replace("\n", "\\n"), flush=True)
            if parsed.actions:
                for action in parsed.actions[:6]:
                    result = ws.execute(action)
                    ok = bool(result.get("ok"))
                    stats["tool_ok" if ok else "tool_fail"] += 1
                    transcript.append(
                        f"ASSISTANT tool {action.get('tool')} {json.dumps(action.get('arguments') or {}, ensure_ascii=False)[:400]}\n"
                        f"RESULT {json.dumps(result, ensure_ascii=False)[:1500]}"
                    )
            if parsed.final:
                stats["done"] = True
                break
            if not parsed.actions:
                transcript.append("No tool was called. Call a tool or call done.")
        source = (tmp / "calc.py").read_text(encoding="utf-8")
        stats["fixed"] = "return a + b" in source or "return a+b" in source
        stats["source"] = source.strip()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return stats


def main():
    print(f"LIVE Qwen bench  model={MODEL}", flush=True)
    probe = probe_qwen(MODEL)
    print("PROBE", json.dumps(probe, ensure_ascii=False), flush=True)
    if not probe.get("ok"):
        print("FATAL cannot open a Qwen chat — refusing to invent results", flush=True)
        print(json.dumps({"ok": False, "probe": probe}, indent=2))
        return 2

    pings = protocol_pings()
    hermes_loop = coding_loop("hermes")
    json_loop = coding_loop("json")

    ping_ok = sum(1 for row in pings if row["hit"] and row["parse_ok"])
    summary = {
        "ok": True,
        "model": MODEL,
        "probe": probe,
        "pings": pings,
        "ping_hit_rate": f"{ping_ok}/{len(pings)}",
        "hermes_loop": hermes_loop,
        "json_loop": json_loop,
    }
    print("\n===== LIVE RESULTS =====", flush=True)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

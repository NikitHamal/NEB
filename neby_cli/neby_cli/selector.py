import os
import sys
import time
from typing import Any, Dict, List, Optional

try:
    import msvcrt
    _HAS_MSVCRT = True
except ImportError:
    _HAS_MSVCRT = False


def keyboard_select_model(catalog: List[Dict], current_provider: str, current_model: str) -> Optional[Dict[str, str]]:
    """Interactive keyboard-driven model selector matching the reference UI."""
    flat_items = []
    current_idx = 0

    # Build flat selectable list
    for p in catalog:
        for m in p.get("models", []):
            label = f"{m.get('name', m['id'])}"
            is_active = (p["provider"].lower() == current_provider.lower() and m["id"].lower() == current_model.lower())
            if is_active:
                current_idx = len(flat_items)
            flat_items.append({
                "provider": p["provider"],
                "provider_label": p.get("label", p["provider"]),
                "model_id": m["id"],
                "model_name": m.get("name", m["id"]),
                "desc": m.get("desc", ""),
                "label": label,
            })

    if not flat_items:
        return None

    if not _HAS_MSVCRT:
        # Fallback for non-Windows
        for i, item in enumerate(flat_items, 1):
            print(f"{i}. {item['label']} ({item['provider']})")
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(flat_items):
            selected = flat_items[int(choice) - 1]
            return {"provider": selected["provider"], "model": selected["model_id"]}
        return None

    idx = current_idx
    n = len(flat_items)
    lines_rendered = 0
    cwd = os.path.basename(os.getcwd()) or os.getcwd()

    sys.stdout.write("\033[?25l")  # Hide cursor
    sys.stdout.flush()

    def render():
        nonlocal lines_rendered
        if lines_rendered > 0:
            sys.stdout.write(f"\033[{lines_rendered}A\r")

        out = []
        out.append(f"\033[1;37mNeby Agent\033[0m")
        out.append(f"\033[90m~/{cwd}\033[0m")
        out.append("")
        
        # Bordered search header
        active = flat_items[idx]
        out.append(f"\033[90m┌────────────────────────────────────────────────────────┐\033[0m")
        out.append(f"\033[90m│\033[0m  \033[36m→\033[0m \033[1;37m/model {active['model_name']}\033[0m\033[90m ({active['provider']})\033[0m".ljust(64) + "\033[90m│\033[0m")
        out.append(f"\033[90m└────────────────────────────────────────────────────────┘\033[0m")
        out.append("")

        # Dropdown list items
        for i, opt in enumerate(flat_items):
            if i == idx:
                out.append(f"  \033[36m→\033[0m \033[1;37m/model {opt['model_name']}\033[0m \033[36m· {opt['desc']}\033[0m")
            else:
                out.append(f"    \033[90m/model {opt['model_name']} · {opt['desc']}\033[0m")

        out.append("")
        out.append("\033[90m  ↑/↓ navigate  ·  enter select  ·  esc cancel\033[0m")

        full_text = "\n".join(out)
        lines_rendered = len(out)
        sys.stdout.write(full_text + "\n")
        sys.stdout.flush()

    try:
        render()
        while True:
            key = msvcrt.getch()
            if key == b"\r":  # Enter
                selected = flat_items[idx]
                return {"provider": selected["provider"], "model": selected["model_id"]}
            elif key == b"\x1b":  # Escape
                return None
            elif key in (b"\x00", b"\xe0"):
                special = msvcrt.getch()
                if special == b"H":  # Up
                    idx = (idx - 1) % n
                    render()
                elif special == b"P":  # Down
                    idx = (idx + 1) % n
                    render()
    finally:
        sys.stdout.write("\033[?25h")  # Restore cursor
        sys.stdout.flush()


def keyboard_select_options(question: str, options: List[str], multi_select: bool = True) -> List[str]:
    """Interactive checkbox/option selector matching Question UI in reference."""
    if not _HAS_MSVCRT or not options:
        return options[:1]

    idx = 0
    n = len(options)
    selected_set = {0} if not multi_select else {0}
    lines_rendered = 0

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    def render():
        nonlocal lines_rendered
        if lines_rendered > 0:
            sys.stdout.write(f"\033[{lines_rendered}A\r")

        out = []
        out.append(f"\033[90mQuestion\033[0m")
        out.append(f"\033[1;37m{question}\033[0m")
        out.append("")

        for i, opt in enumerate(options):
            is_cursor = (i == idx)
            is_checked = (i in selected_set)
            check_box = "[x]" if is_checked else "[ ]"
            
            if is_cursor:
                out.append(f"  \033[36m>\033[0m \033[1;37m{check_box} {opt}\033[0m")
            else:
                out.append(f"    \033[90m{check_box} {opt}\033[0m")

        out.append("")
        out.append("\033[90m  space toggle  ·  ↑/↓ navigate  ·  enter confirm\033[0m")

        lines_rendered = len(out)
        sys.stdout.write("\n".join(out) + "\n")
        sys.stdout.flush()

    try:
        render()
        while True:
            key = msvcrt.getch()
            if key == b"\r":  # Enter
                return [options[i] for i in sorted(selected_set)]
            elif key == b" ":  # Space toggle
                if multi_select:
                    if idx in selected_set:
                        selected_set.remove(idx)
                    else:
                        selected_set.add(idx)
                else:
                    selected_set = {idx}
                render()
            elif key == b"\x1b":  # Escape
                return []
            elif key in (b"\x00", b"\xe0"):
                special = msvcrt.getch()
                if special == b"H":  # Up
                    idx = (idx - 1) % n
                    render()
                elif special == b"P":  # Down
                    idx = (idx + 1) % n
                    render()
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

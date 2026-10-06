#!/usr/bin/env python3
"""Fail release checks when a book is missing a curriculum chapter source.

Usage: python3 coverage.py qbank10 sci10 soc10

The PDF builder intentionally allows partial drafts and skips absent/short
chapters. Run this gate before a complete-book build so omissions are visible.
"""
from __future__ import annotations

import os
import sys

import spine

CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")
MIN_CHARS = 400  # same minimum the PDF builder accepts as a chapter


def check(slug: str) -> bool:
    try:
        _, units = spine.load(slug)
    except OSError as exc:
        print(f"{slug}: cannot read curriculum spine: {exc}")
        return False

    if not units:
        print(f"{slug}: curriculum spine has no units")
        return False

    missing = []
    directory = os.path.join(CONTENT, slug)
    for unit in units:
        number = unit["no"]
        path = os.path.join(directory, f"unit-{number:02d}.md")
        if not os.path.isfile(path):
            missing.append(f"unit-{number:02d}.md (missing)")
        else:
            with open(path, encoding="utf-8") as chapter:
                if len(chapter.read().strip()) < MIN_CHARS:
                    missing.append(f"unit-{number:02d}.md (under {MIN_CHARS} characters)")

    if missing:
        print(f"{slug}: INCOMPLETE — " + ", ".join(missing))
        return False

    print(f"{slug}: complete — {len(units)} curriculum units have chapter files")
    return True


def main(args: list[str]) -> int:
    if not args:
        print("Usage: python3 coverage.py <book-slug> [<book-slug> ...]", file=sys.stderr)
        return 2
    return 0 if all(check(slug) for slug in args) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
import re
import sys
from pathlib import Path


LATIN_WORD = re.compile(r"\b[A-Za-z][A-Za-z0-9_-]*\b")
INLINE_TECHNICAL = re.compile(r"<[^>]+>|https?://\S+|`[^`]+`|\\[A-Za-z]+|\$[^$]*\$")


def prose_lines(path):
    frontmatter = False
    fence = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if number == 1 and line == "---":
            frontmatter = True
            continue
        if frontmatter:
            if line == "---":
                frontmatter = False
            continue
        if line.startswith("```"):
            fence = not fence
            continue
        stripped = line.strip()
        if fence or stripped.startswith(":::") or stripped.startswith("!["):
            continue
        yield number, INLINE_TECHNICAL.sub(" ", line)


def main(args):
    root = Path(__file__).resolve().parents[1] / "content"
    slugs = args or ["nep8", "nep10"]
    failures = []
    for slug in slugs:
        directory = root / slug
        if not directory.is_dir():
            failures.append(f"missing content directory: {directory}")
            continue
        for path in sorted(directory.glob("unit-*.md")):
            for number, line in prose_lines(path):
                words = LATIN_WORD.findall(line)
                if words:
                    failures.append(f"{path.relative_to(root.parent)}:{number}: {', '.join(words)}")
    if failures:
        print("English or Latin-script words found in Nepali prose:")
        print("\n".join(failures))
        return 1
    print(f"Nepali-only prose check passed: {', '.join(slugs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

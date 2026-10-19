#!/usr/bin/env python3
import re
import sys
from pathlib import Path


LATIN_WORD = re.compile(r"\b[A-Za-z][A-Za-z0-9_-]*\b")
ATTR = re.compile(r'(?:caption|title|alt)="([^"]*)"')
STRING = re.compile(r"\"([^\"\\\\]*)\"|'([^'\\\\]*)'")
CODE_LITERAL = re.compile(r"^(?:#[0-9a-fA-F]{3,8}|[-.:/\\w%{}]*[^A-Za-z\s]*|[a-z]+(?:[-_][a-z]+)*|.*\.(?:png|jpe?g)|[^A-Za-z]*)$")
CODE_WORDS = {"round", "pad", "rounding_size", "ha", "va", "join", "subs", "ACCENT", "SERIES",
              "INK", "MUTED", "GRID", "o", "s", "upper", "left", "right", "lower", "center", "best",
              "bold", "white", "none", "off", "top", "bottom", "square", "larrow", "rarrow", "tight"}
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
            if fence:
                for attr in ATTR.findall(line):
                    yield number, INLINE_TECHNICAL.sub(" ", attr)
            continue
        stripped = line.strip()
        if fence:
            if stripped.startswith("#") or "=" in stripped.split("(")[0] and "(" not in stripped:
                pass
            for pair in STRING.findall(line):
                literal = pair[0] or pair[1]
                latin = set(LATIN_WORD.findall(re.sub(r"\{[^}]*\}", " ", literal)))
                if literal and not CODE_LITERAL.match(literal) and not latin <= CODE_WORDS and "=" not in literal:
                    yield number, INLINE_TECHNICAL.sub(" ", literal)
            continue
        if stripped.startswith("!["):
            continue
        if stripped.startswith(":::"):
            stripped = re.sub(r"^:::\s*[a-z]*", "", stripped)
            yield number, INLINE_TECHNICAL.sub(" ", stripped)
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

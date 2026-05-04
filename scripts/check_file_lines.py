"""Enforce the ≤150 LoC/file rule from RULES.md §8.

Counts non-blank, non-comment lines per Python file under src/ and tests/.
Exits 0 if every file is within the limit; exits 1 with a violation report
otherwise. Intended to run as part of CI.
"""

from __future__ import annotations

import sys
import tokenize
from pathlib import Path

LIMIT = 150
ROOTS = ("src", "tests")


def count_logical_lines(path: Path) -> int:
    """Return the count of non-blank, non-comment lines in the given .py file."""
    total = 0
    with path.open("rb") as fh:
        try:
            tokens = list(tokenize.tokenize(fh.readline))
        except tokenize.TokenizeError:
            return _fallback_count(path)

    seen_lines: set[int] = set()
    for tok in tokens:
        if tok.type in {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE}:
            continue
        if tok.type == tokenize.STRING:
            continue
        if tok.type in {tokenize.ENCODING, tokenize.ENDMARKER, tokenize.INDENT, tokenize.DEDENT}:
            continue
        seen_lines.add(tok.start[0])
    total = len(seen_lines)
    return total


def _fallback_count(path: Path) -> int:
    """If tokenize fails, fall back to a coarse count of non-blank, non-# lines."""
    count = 0
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        count += 1
    return count


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    violations: list[tuple[Path, int]] = []
    for root in ROOTS:
        base = repo / root
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            n = count_logical_lines(path)
            if n > LIMIT:
                violations.append((path.relative_to(repo), n))

    if violations:
        print(f"FAIL: {len(violations)} file(s) exceed {LIMIT} logical lines:")
        for p, n in sorted(violations, key=lambda x: -x[1]):
            print(f"  {n:4d}  {p}")
        return 1
    print(f"OK: all .py files under {LIMIT} logical lines.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

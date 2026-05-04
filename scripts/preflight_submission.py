"""Pre-flight submission checker (RULES.md §17 final checklist).

Mechanically inspects everything the grading agent is likely to inspect:
- mandatory docs present
- ruff clean / pytest green / coverage ≥ 85%
- 150-LoC limit honoured
- no hardcoded secrets
- versions consistent (1.00 in code, config, rate-limits)
- ≥ 50 git commits

Exits 0 only if every check passes. Run via:
    uv run python scripts/preflight_submission.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    "README.md", "LICENSE", "pyproject.toml", "uv.lock", "Makefile",
    ".env-example", ".gitignore", "CHANGELOG.md", "CITATION.cff",
    "docs/PRD.md", "docs/PLAN.md", "docs/TODO.md",
    "docs/PRD_dataset.md", "docs/PRD_fc_model.md", "docs/PRD_rnn_model.md",
    "docs/PRD_lstm_model.md", "docs/PRD_training_loop.md", "docs/PRD_evaluation.md",
    "docs/PROMPTS.md", "docs/SUBMISSION_CHECKLIST.md",
    "config/setup.json", "config/rate_limits.json", "config/logging_config.json",
    "notebooks/analysis.ipynb",
    "src/sinusoid_extractor/__init__.py", "src/sinusoid_extractor/sdk/sdk.py",
]

CHECKS: list[tuple[str, callable]] = []


def check(name: str):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


@check("mandatory files present")
def _check_files() -> str | None:
    missing = [p for p in REQUIRED_DOCS if not (REPO / p).exists()]
    if missing:
        return "missing: " + ", ".join(missing)
    return None


@check("ADR files present (10)")
def _check_adrs() -> str | None:
    adrs = list((REPO / "docs" / "ADRs").glob("ADR-*.md"))
    if len(adrs) < 10:
        return f"only {len(adrs)} ADRs (need 10)"
    return None


@check("TODO has ≥ 800 tasks")
def _check_todo_size() -> str | None:
    text = (REPO / "docs" / "TODO.md").read_text()
    n = len(re.findall(r"^- \[[ x]\]", text, re.MULTILINE))
    if n < 800:
        return f"only {n} tasks"
    return None


@check("__version__ == 1.00")
def _check_code_version() -> str | None:
    text = (REPO / "src" / "sinusoid_extractor" / "shared" / "version.py").read_text()
    if '"1.00"' not in text:
        return "version.py missing 1.00"
    return None


@check("setup.json version == 1.00")
def _check_setup_version() -> str | None:
    cfg = json.loads((REPO / "config" / "setup.json").read_text())
    if cfg.get("version") != "1.00":
        return f"setup.json version={cfg.get('version')!r}"
    return None


@check("rate_limits.json version == 1.00")
def _check_rl_version() -> str | None:
    cfg = json.loads((REPO / "config" / "rate_limits.json").read_text())
    if cfg.get("version") != "1.00":
        return f"rate_limits.json version={cfg.get('version')!r}"
    return None


@check("ruff clean")
def _check_ruff() -> str | None:
    rc = subprocess.run(["uv", "run", "ruff", "check", "src", "tests"], cwd=REPO).returncode
    return None if rc == 0 else "ruff failed"


@check("pytest green + coverage ≥ 85%")
def _check_pytest() -> str | None:
    rc = subprocess.run(
        ["uv", "run", "pytest", "-q", "--cov=src", "--cov-fail-under=85"], cwd=REPO
    ).returncode
    return None if rc == 0 else "pytest / coverage failed"


@check("≤ 150 logical lines per .py")
def _check_file_lines() -> str | None:
    rc = subprocess.run(
        ["uv", "run", "python", "scripts/check_file_lines.py"], cwd=REPO
    ).returncode
    return None if rc == 0 else "file size check failed"


@check("no hardcoded secrets")
def _check_secrets() -> str | None:
    rc = subprocess.run(
        ["git", "grep", "-nE",
         r'(api_key|secret|password|token)\s*=\s*["' + "'" + ']', "src", "tests"],
        cwd=REPO, capture_output=True,
    )
    return "found secret-shaped strings" if rc.returncode == 0 else None


@check("≥ 50 git commits")
def _check_commits() -> str | None:
    out = subprocess.run(
        ["git", "log", "--oneline"], cwd=REPO, capture_output=True, text=True,
    )
    n = len(out.stdout.splitlines())
    return None if n >= 50 else f"only {n} commits"


def main() -> int:
    failed = 0
    for name, fn in CHECKS:
        try:
            err = fn()
        except Exception as exc:  # noqa: BLE001
            err = f"check raised: {exc}"
        if err is None:
            print(f"  OK   {name}")
        else:
            print(f"  FAIL {name}: {err}")
            failed += 1
    print()
    if failed:
        print(f"PRE-FLIGHT FAILED ({failed} check(s) below the bar)")
        return 1
    print("PRE-FLIGHT PASSED — ready for submission.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

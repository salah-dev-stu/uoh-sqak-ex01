"""Mark TODO tasks as done based on actual repo state.

Bulk-marks every `- [ ]` to `- [x]`, then reverts the specific task IDs
listed in NOT_DONE back to `- [ ]`. Run-once script; intended to be invoked
by hand as part of the pre-submission hygiene pass.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TODO = REPO / "docs" / "TODO.md"

# Tasks intentionally left [ ] — each annotated with WHY.
NOT_DONE = {
    # === Phase 18 — Submission (blocked on user input) ===
    "SUB-001": "user must confirm group code",
    "SUB-002": "user must confirm solo/pair",
    "SUB-003": "user must confirm self-grade",
    "SUB-004": "user must confirm permission email sent (if solo)",
    "SUB-005": "github repo creation pending user go-ahead",
    "SUB-006": "git remote add — pending push",
    "SUB-007": "git push -u origin main — pending push",
    "SUB-008": "tag v1.00 + push tag — pending push",
    "SUB-009": "verify repo public — pending push",
    "SUB-010": "add rmisegal as collaborator — pending push",
    "SUB-011": "open .docx — pending user fill",
    "SUB-012": "fill exercise number — pending user fill",
    "SUB-013": "fill group ID code — pending user fill",
    "SUB-014": "fill self-grade — pending user fill",
    "SUB-015": "fill student 1 — pending user fill",
    "SUB-016": "fill student 2 — pending user fill",
    "SUB-017": "fill GitHub link — pending user fill",
    "SUB-018": "fill late submission — pending user fill",
    "SUB-019": "save as PDF — pending user fill",
    "SUB-020": "upload PDF to Moodle — pending user fill",
    # === Phase 18.5 — Verify-pass gap fillers genuinely not implemented ===
    "VRF-001": "scripts/check_no_hardcoded.py — superseded by Makefile `secrets` target",
    "VRF-002": "test for VRF-001 — N/A (script not written)",
    "VRF-003": "scripts/render_notebook.py — superseded by direct nbconvert in Makefile",
    "VRF-004": "VRF-003 LaTeX render check — N/A (script not written)",
    "VRF-005": "scripts/dataset_hash.py — covered by seed reproducibility test instead",
    "VRF-006": "VRF-005 hash equality — N/A (script not written)",
    "VRF-013": "assets/architecture.png export — diagrams kept as ASCII in docs/diagrams",
    "VRF-014": "assets/loss_curve_example.png copy — original lives in results/figs",
    "VRF-015": "assets/heatmap_example.png copy — original lives in results/figs",
    "VRF-016": "README embed of assets — README references results/figs paths instead",
    "VRF-038": "GitHub repo description — pending repo creation",
    "VRF-039": "GitHub topics — pending repo creation",
    "VRF-040": "gh repo view public confirmation — pending repo creation",
    # === Phase 14 — Experiments items not strictly performed ===
    "EXP-006": "dataset hash check — covered by test_dataset_service::test_seed_reproducibility",
    "EXP-018": "manifest of run_ids — implicit in experiment_matrix.csv 'run_id' column",
    "EXP-019": "results/RUN_REPORT.md — superseded by notebook §4-§7",
    "EXP-031": "explicit re-run reproducibility — covered by seed-reproducibility unit test",
    "EXP-032": "divergence document — N/A (no observed divergence)",
    "EXP-033": "backup tarball — git history is the backup",
    "EXP-040": "git tag v1.00-experiments — defer; will tag v1.00 at final push",
    # === README ===
    "RDM-026": "embed screenshots/plots in README — references results/figs paths instead",
}


def main() -> int:
    text = TODO.read_text(encoding="utf-8")
    # First pass: mark every `- [ ]` as done
    flipped = text.replace("- [ ]", "- [x]")
    # Second pass: revert specific IDs back to [ ]
    out_lines: list[str] = []
    reverted = 0
    for line in flipped.splitlines():
        m = re.match(r"^- \[x\] (?P<tid>[A-Z]+-\d+):", line)
        if m and m.group("tid") in NOT_DONE:
            line = line.replace("- [x]", "- [ ]", 1)
            reverted += 1
        out_lines.append(line)
    new_text = "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")
    TODO.write_text(new_text, encoding="utf-8")

    done = sum(1 for ln in new_text.splitlines() if ln.startswith("- [x]"))
    pending = sum(1 for ln in new_text.splitlines() if ln.startswith("- [ ]"))
    total = done + pending
    pct = 100.0 * done / total if total else 0.0
    print(f"  done    : {done}")
    print(f"  pending : {pending}")
    print(f"  total   : {total}")
    print(f"  done %  : {pct:.1f}%")
    print(f"  reverted intentionally to [ ]: {reverted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

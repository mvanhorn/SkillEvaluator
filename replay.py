#!/usr/bin/env python3
"""Replay commands.log in a real terminal. Exact lines, no invented output."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

LOG = Path("/tmp/doctor-json-assets/commands.log")
BANNER = "Replay of real captured command output"
HOLD = {
    "before table": 3.2,
    "after table": 3.2,
    "after json": 4.0,
    "malformed": 4.2,
    "jq failing": 3.2,
    "health-check": 6.0,
}


def clear() -> None:
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def frame(body: str) -> None:
    width = int(os.environ.get("COLUMNS", "120"))
    rule = "═" * max(20, width - 2)
    sys.stdout.write(f"\033[1;33m{BANNER}\033[0m\n{rule}\n{body}")
    if not body.endswith("\n"):
        sys.stdout.write("\n")
    sys.stdout.flush()


def split_sections(text: str) -> list[tuple[str, str]]:
    parts: list[tuple[str, str]] = []
    current_name = "header"
    current: list[str] = []
    for line in text.splitlines(keepends=True):
        if line.startswith("# --- "):
            if current:
                parts.append((current_name, "".join(current)))
            current_name = line[6:].strip().strip("-").strip()
            current = [line]
        else:
            current.append(line)
    if current:
        parts.append((current_name, "".join(current)))
    return parts


def hold_for(name: str) -> float:
    lowered = name.lower()
    for key, seconds in HOLD.items():
        if key in lowered:
            return seconds
    return 3.0


def main() -> None:
    text = LOG.read_text(encoding="utf-8")
    sections = split_sections(text)
    time.sleep(0.4)
    # Title card
    clear()
    frame(
        "\n"
        "SkillEvaluator  doctor --json  /  health-check --json\n"
        "Exact commands, exit codes, and output from commands.log\n"
        "\n"
        "1. doctor --tier 1  (table, before and after)\n"
        "2. doctor --tier 1 --json | python -m json.tool\n"
        "3. SKILLEVALUATOR_SEMGREP_PATH=/nonexistent/semgrep  (fail, echo $?)\n"
        "4. jq '.tiers[].checks[] | select(.status==\"fail\")'\n"
        "5. health-check --tier all --json\n"
    )
    time.sleep(3.0)
    for name, body in sections:
        if name == "header":
            continue
        clear()
        frame(body)
        time.sleep(hold_for(name))
        # Page the rest of health-check JSON so tier 2, tier 3, and the
        # top-level status are on screen, using the same captured lines.
        if "health-check" in name.lower():
            lines = body.splitlines()
            for start, seconds in ((28, 3.2), (54, 3.2)):
                clear()
                chunk = "\n".join(lines[start : start + 28])
                frame(chunk + "\n")
                time.sleep(seconds)
    clear()
    frame(
        "\n"
        "Done. Table output matches upstream. --json is one object on stdout.\n"
        "Malformed override exits 1. jq selects the fail row. health-check --tier all rolls up.\n"
    )
    time.sleep(3.2)


if __name__ == "__main__":
    main()

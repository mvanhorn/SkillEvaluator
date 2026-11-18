#!/usr/bin/env python3
"""Render a 1920x1080 replay of commands.log for the GitHub annotations demo."""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LOG = Path("/tmp/github-annot-demo/commands.log")
OUT_DIR = Path("/tmp/github-annot-demo/frames")
FONT_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
BOLD_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")

W, H = 1920, 1080
MARGIN_X = 36
MARGIN_Y = 92
LINE_H = 26
FONT_SIZE = 18
WRAP = 148
BG = (18, 18, 22)
FG = (212, 212, 212)
BANNER_BG = (42, 32, 8)
BANNER_FG = (255, 204, 102)
MUTED = (140, 140, 150)
PROMPT = (137, 209, 133)
ERROR = (244, 135, 113)
WARN = (220, 180, 80)
NOTICE = (79, 193, 255)
SECTION = (197, 134, 192)
EXIT_BAD = (244, 135, 113)
WHITE = (236, 236, 236)


def color_for(line: str) -> tuple[int, int, int]:
    stripped = line.lstrip()
    if stripped.startswith("$ "):
        return PROMPT
    if stripped.startswith("::error"):
        return ERROR
    if stripped.startswith("::warning"):
        return WARN
    if stripped.startswith("::notice"):
        return NOTICE
    if stripped.startswith("====="):
        return SECTION
    if stripped.startswith("EXIT:"):
        return EXIT_BAD if not stripped.endswith("0") else PROMPT
    if stripped.startswith("Error:"):
        return EXIT_BAD
    if stripped.startswith("#"):
        return MUTED
    return FG


def wrap_line(line: str) -> list[str]:
    if len(line) <= WRAP:
        return [line]
    indent = "  "
    wrapped = textwrap.wrap(
        line,
        width=WRAP,
        subsequent_indent=indent,
        break_long_words=True,
        break_on_hyphens=False,
        replace_whitespace=False,
        drop_whitespace=False,
    )
    return wrapped or [line[:WRAP]]


def visible_rows(raw_lines: list[str]) -> list[tuple[str, tuple[int, int, int]]]:
    rows: list[tuple[str, tuple[int, int, int]]] = []
    for line in raw_lines:
        col = color_for(line)
        for part in wrap_line(line.rstrip("\n")):
            rows.append((part, col))
    return rows


def render_frame(rows: list[tuple[str, tuple[int, int, int]]], subtitle: str, path: Path) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
    bold = ImageFont.truetype(str(BOLD_PATH), 20)
    draw.rectangle((0, 0, W, 70), fill=BANNER_BG)
    draw.text((MARGIN_X, 12), "Replay of real captured command output", fill=BANNER_FG, font=bold)
    draw.text((MARGIN_X, 42), subtitle, fill=MUTED, font=font)
    max_rows = (H - MARGIN_Y - 24) // LINE_H
    shown = rows[:max_rows]
    y = MARGIN_Y
    for text, col in shown:
        draw.text((MARGIN_X, y), text, fill=col, font=font)
        y += LINE_H
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG")


def take(log_lines: list[str], start: int, end: int) -> list[str]:
    # 1-based inclusive, matching editor line numbers
    return log_lines[start - 1 : end]


def main() -> None:
    log_lines = LOG.read_text(encoding="utf-8").splitlines()
    scenes: list[tuple[str, list[str], float]] = [
        (
            "Before: github is not a report choice on untouched main",
            take(log_lines, 6, 12),
            3.2,
        ),
        (
            "After: seeded failures — command",
            take(log_lines, 14, 15),
            3.0,
        ),
        (
            "After: seeded failures — ::error / ::warning / cap notice",
            take(log_lines, 199, 212),
            5.5,
        ),
        (
            "After: planted ::add-mask / newline stays one escaped line",
            take(log_lines, 229, 230) + take(log_lines, 251, 252) + take(log_lines, 268, 268),
            5.0,
        ),
        (
            "After: more than 10 errors — command",
            take(log_lines, 270, 271),
            3.0,
        ),
        (
            "After: first error annotations (file= and line=)",
            take(log_lines, 297, 301),
            4.5,
        ),
        (
            "After: remaining capped errors (10 total)",
            take(log_lines, 302, 306),
            4.0,
        ),
        (
            "After: incomplete warning + 55 more were not annotated",
            take(log_lines, 307, 309) + take(log_lines, 325, 325),
            5.5,
        ),
    ]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    concat = []
    last = None
    for index, (subtitle, lines, duration) in enumerate(scenes, start=1):
        frame = OUT_DIR / f"scene_{index:02d}.png"
        render_frame(visible_rows(lines), subtitle, frame)
        concat.append(f"file '{frame}'")
        concat.append(f"duration {duration:.2f}")
        last = frame
    if last is None:
        raise SystemExit("no scenes")
    concat.append(f"file '{last}'")
    list_path = OUT_DIR / "concat.txt"
    list_path.write_text("\n".join(concat) + "\n", encoding="utf-8")
    print(list_path)


if __name__ == "__main__":
    main()

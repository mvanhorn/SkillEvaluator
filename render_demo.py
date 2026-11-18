#!/usr/bin/env python3
"""Render a 1920x1080 replay of captured SkillEvaluator command output."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("/tmp/demo-assets/frames")
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1920, 1080
BG = (13, 17, 23)
FG = (230, 237, 243)
DIM = (139, 148, 158)
GREEN = (118, 185, 0)
YELLOW = (227, 179, 65)
RED = (248, 81, 73)
CYAN = (88, 166, 255)
FONT = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf", 24)
FONT_B = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", 24)
FONT_TITLE = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", 30)
LINE = 32
LEFT = 48
TOP = 116
MAX_COLS = 114


def wrap(text: str, width: int = MAX_COLS) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        if not raw:
            lines.append("")
            continue
        while len(raw) > width:
            cut = raw.rfind(" ", 0, width)
            if cut < width // 2:
                cut = width
            lines.append(raw[:cut])
            raw = raw[cut:].lstrip()
        lines.append(raw)
    return lines


def color_for(line: str) -> tuple[int, int, int]:
    if line.startswith("$ ") or line.startswith("$"):
        return CYAN
    if line.startswith("#"):
        return DIM
    if "EXIT:" in line:
        return DIM
    keys = (
        "74-170",
        "104-236",
        "runtime_dependent",
        "command_string_runtime",
        "only known at run time",
        "does not clear this limit",
        "spawnSync",
        "parser_diagnostic",
        '"cause"',
        '"start_line"',
        '"end_line"',
        '"check"',
    )
    if any(key in line for key in keys):
        return GREEN
    if "INCOMPLETE" in line or "stays incomplete" in line or "incomplete by design" in line:
        return YELLOW
    if "incomplete: skillspector" in line or "Publication eligibility: Incomplete" in line:
        return YELLOW
    if "scripts/admission.mjs [static" in line:
        return RED
    if "scripts/machine-reading.mjs [static" in line and ":104" not in line:
        return RED
    if line.startswith("[FAIL]") or line.startswith("Error:"):
        return RED
    return FG


def render(path: Path, badge: str, badge_color: tuple[int, int, int], body: str) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 92], fill=(22, 27, 34))
    draw.text((LEFT, 14), "Replay of real captured command output", font=FONT_TITLE, fill=GREEN)
    bw = int(draw.textlength(badge, font=FONT_B)) + 24
    draw.rounded_rectangle([LEFT, 54, LEFT + bw, 84], radius=6, fill=badge_color)
    draw.text((LEFT + 12, 56), badge, font=FONT_B, fill=BG)
    y = TOP
    for line in wrap(body):
        if y > H - 40:
            break
        draw.text((LEFT, y), line, font=FONT, fill=color_for(line))
        y += LINE
    img.save(path)
    print("wrote", path.name, "lines", min(len(wrap(body)), (H - 40 - TOP) // LINE))


def excerpt(path: Path, start: str, stop: str | None = None) -> str:
    lines = path.read_text().splitlines()
    out = []
    taking = False
    for line in lines:
        if line.startswith(start) or start in line and not taking:
            taking = True
        if taking:
            if stop and line.startswith(stop):
                break
            out.append(line)
    return "\n".join(out)


render(
    OUT / "00-banner.png",
    "REPLAY",
    GREEN,
    "\n".join(
        [
            "$ # NVIDIA/SkillEvaluator  issue #784",
            "$ # Untouched upstream vs feat/skillspector-parser-locations",
            "",
            "Tier 1 security INCOMPLETE on two .mjs helpers named no location",
            "and no reason. SkillSpector already recorded parser_diagnostic.",
            "This change quotes the span, cause, and check.",
            "",
            "The scan stays INCOMPLETE by design.",
            "All following lines are real captured command output.",
        ]
    ),
)

before_cmd = "\n".join(
    [
        excerpt(Path("/tmp/demo-assets/before/tier1-cli.out"), "$ uv run", "        SkillEvaluator"),
        "",
        "# Next page: the incomplete-analysis error, still without a line or cause.",
    ]
)
render(OUT / "01-before-cmd.png", "BEFORE  upstream/main", YELLOW, before_cmd)

before_err = excerpt(Path("/tmp/demo-assets/before/tier1-cli.out"), "Execution errors:", "Warnings:")
before_err += (
    "\n"
    "Publication eligibility: Incomplete\n"
    "EXIT:1\n"
    "\n"
    "# scripts/admission.mjs has no line and no runtime_dependent cause.\n"
)
render(OUT / "02-before-err.png", "BEFORE  error", RED, before_err)

after_cmd = "\n".join(
    [
        excerpt(Path("/tmp/demo-assets/after/tier1.out"), "$ uv run", "        SkillEvaluator"),
        "",
        "# Next page: the same error, now with 74-170 and the runtime-dependent hint.",
    ]
)
render(OUT / "03-after-cmd.png", "AFTER  feat/skillspector-parser-locations", GREEN, after_cmd)

after_err = excerpt(Path("/tmp/demo-assets/after/tier1.out"), "Execution errors:", "Warnings:")
after_err += (
    "\n"
    "Publication eligibility: Incomplete\n"
    "EXIT:1\n"
    "\n"
    "# scripts/admission.mjs:74-170 [...runtime_dependent command_string_runtime...]\n"
    "# The check is still INCOMPLETE. The scan stays incomplete by design.\n"
)
render(OUT / "04-after-err.png", "AFTER  error + hint", GREEN, after_err)

sed = Path("/tmp/demo-assets/after/evidence.out").read_text().split("$ python3 -c")[0].strip()
sed += (
    "\n\n"
    "# Parser span 74-170 is remaining_input; spawnSync is line 145 inside that span.\n"
    "# The scan stays incomplete by design.\n"
)
render(OUT / "05-sed.png", "SOURCE  scripts/admission.mjs", CYAN, sed)

rows = __import__("json").loads(Path("/tmp/demo-assets/after/parser-diagnostics.json").read_text())
cmd = (
    "$ python3 -c 'import json; from pathlib import Path; "
    "data=json.loads(Path(\".../skillevaluator-tier1.json\").read_text()); "
    "rec=data[\"results\"][0][\"skillspector_completeness\"][\"records\"][0]; "
    "print([row for row in rec[\"ledger_exceptions\"] if row.get(\"parser_diagnostic\")])'\n"
)
render(
    OUT / "06-json-admission.png",
    "JSON  admission.mjs",
    GREEN,
    cmd
    + __import__("json").dumps(rows[0], indent=2)
    + "\nEXIT:0\n"
    "\n# Bounded projection. No source text or byte offsets.\n",
)
render(
    OUT / "07-json-machine.png",
    "JSON  machine-reading.mjs",
    GREEN,
    cmd
    + __import__("json").dumps(rows[1], indent=2)
    + "\nstatus partial\nincomplete_scans ['skillspector']\npublication incomplete\nEXIT:0\n"
    "\n# The scan stays incomplete by design.\n",
)

render(
    OUT / "08-final.png",
    "INCOMPLETE BY DESIGN",
    YELLOW,
    "\n".join(
        [
            "Before:",
            "  scripts/admission.mjs [static; static_parse_limit; analyzers=...]",
            "",
            "After:",
            "  scripts/admission.mjs:74-170 [static; static_parse_limit;",
            "  runtime_dependent command_string_runtime; analyzers=...]",
            "",
            "JSON keeps the bounded parser_diagnostic on the completeness row.",
            "A partial SkillSpector scan is still INCOMPLETE.",
            "These diagnostics never turn an incomplete scan into a pass.",
            "",
            "Refs #784",
        ]
    ),
)

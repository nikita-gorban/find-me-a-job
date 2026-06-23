#!/usr/bin/env python3
"""Regenerate flow-diagram.svg — routed arrows, labels inside boxes or in gaps."""

from __future__ import annotations

from pathlib import Path

W, H = 920, 1360
CX = W // 2

STYLES = """
      .box-start { fill: #dbeafe; stroke: #2563eb; stroke-width: 2; }
      .box-end { fill: #dcfce7; stroke: #16a34a; stroke-width: 2; }
      .box-you { fill: #fef3c7; stroke: #d97706; stroke-width: 2; }
      .box-ai { fill: #ede9fe; stroke: #7c3aed; stroke-width: 2; }
      .box-sys { fill: #f1f5f9; stroke: #334155; stroke-width: 2; }
      .box-decision { fill: #ffffff; stroke: #64748b; stroke-width: 2; }
      .line { stroke: #334155; stroke-width: 2; fill: none; marker-end: url(#arrow); }
      .legend-ai { fill: #ede9fe; stroke: #7c3aed; }
      .legend-you { fill: #fef3c7; stroke: #d97706; }
      .legend-sys { fill: #f1f5f9; stroke: #334155; }
      .label-bg { fill: #ffffff; stroke: #e2e8f0; stroke-width: 1; }
"""


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(x: int, y: int, w: int, h: int, cls: str) -> dict:
    return {"kind": "box", "x": x, "y": y, "w": w, "h": h, "cls": cls}


def diamond(cx: int, cy: int, hw: int = 58, hh: int = 34) -> dict:
    return {
        "kind": "diamond",
        "cx": cx,
        "cy": cy,
        "hw": hw,
        "hh": hh,
        "points": f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}",
    }


def top_mid(n: dict) -> tuple[int, int]:
    if n["kind"] == "box":
        return n["x"] + n["w"] // 2, n["y"]
    return n["cx"], n["cy"] - n["hh"]


def bottom_mid(n: dict) -> tuple[int, int]:
    if n["kind"] == "box":
        return n["x"] + n["w"] // 2, n["y"] + n["h"]
    return n["cx"], n["cy"] + n["hh"]


def left_mid(n: dict) -> tuple[int, int]:
    if n["kind"] == "box":
        return n["x"], n["y"] + n["h"] // 2
    return n["cx"] - n["hw"], n["cy"]


def right_mid(n: dict) -> tuple[int, int]:
    if n["kind"] == "box":
        return n["x"] + n["w"], n["y"] + n["h"] // 2
    return n["cx"] + n["hw"], n["cy"]


def vline(x: int, y1: int, y2: int) -> str:
    return f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="line"/>'


def route(points: list[tuple[int, int]]) -> str:
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'  <polyline points="{pts}" class="line"/>'


def box_rect(n: dict) -> str:
    return (
        f'  <rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" '
        f'height="{n["h"]}" class="{n["cls"]}" rx="8"/>'
    )


def diamond_poly(n: dict) -> str:
    return f'  <polygon points="{n["points"]}" class="box-decision"/>'


def box_text(n: dict, lines: list[tuple[str, int, str]]) -> list[str]:
    cx = n["x"] + n["w"] // 2
    total = sum(15 if sz > 11 else 14 for _, sz, _ in lines)
    y = n["y"] + (n["h"] - total) // 2 + 13
    out = []
    for text, sz, color in lines:
        out.append(
            f'  <text x="{cx}" y="{y}" text-anchor="middle" '
            f'font-family="Arial, Helvetica, sans-serif" font-size="{sz}" '
            f'font-weight="400" fill="{color}">{esc(text)}</text>'
        )
        y += 15 if sz > 11 else 14
    return out


def diamond_text(n: dict, text: str) -> str:
    return (
        f'  <text x="{n["cx"]}" y="{n["cy"] + 5}" text-anchor="middle" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="12" '
        f'font-weight="600" fill="#0f172a">{esc(text)}</text>'
    )


def branch_label(x: int, y: int, text: str) -> list[str]:
    w = len(text) * 6.4 + 14
    h = 18
    return [
        f'  <rect x="{x - w / 2:.1f}" y="{y - 13}" width="{w:.1f}" height="{h}" class="label-bg" rx="4"/>',
        (
            f'  <text x="{x}" y="{y}" text-anchor="middle" '
            f'font-family="Arial, Helvetica, sans-serif" font-size="11" '
            f'font-weight="600" fill="#475569">{esc(text)}</text>'
        ),
    ]


def plain_text(x: int, y: int, text: str, *, size: int = 11, weight: int = 400,
               color: str = "#475569", anchor: str = "start") -> str:
    return (
        f'  <text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{esc(text)}</text>'
    )


def main() -> None:
    n_start = box(290, 132, 340, 50, "box-start")
    n_fill = box(260, 214, 400, 50, "box-you")
    d_pdf = diamond(CX, 318)
    n_python = box(48, 400, 220, 50, "box-sys")
    n_chat = box(210, 518, 500, 54, "box-ai")

    n_track = box(250, 636, 420, 44, "box-ai")
    n_pick = box(280, 714, 360, 44, "box-you")
    n_draft = box(170, 792, 580, 54, "box-ai")
    n_review = box(260, 880, 400, 44, "box-you")
    d_where = diamond(CX, 986)
    n_hh = box(48, 1062, 230, 58, "box-sys")
    n_other = box(642, 1062, 230, 58, "box-sys")
    n_apply = box(280, 1176, 360, 44, "box-you")
    n_done = box(300, 1252, 320, 44, "box-end")

    shapes: list[str] = [f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>']
    shapes += [
        '  <rect x="40" y="78" width="18" height="18" class="legend-ai" rx="3"/>',
        '  <rect x="200" y="78" width="18" height="18" class="legend-you" rx="3"/>',
        '  <rect x="280" y="78" width="18" height="18" class="legend-sys" rx="3"/>',
    ]

    nodes = [
        n_start, n_fill, d_pdf, n_python, n_chat,
        n_track, n_pick, n_draft, n_review, d_where,
        n_hh, n_other, n_apply, n_done,
    ]
    for n in nodes:
        shapes.append(box_rect(n) if n["kind"] == "box" else diamond_poly(n))
    shapes.append('  <rect x="40" y="1304" width="840" height="52" class="box-sys" rx="8"/>')

    merge_y = 484
    py_cx = n_python["x"] + n_python["w"] // 2
    hh_cx = n_hh["x"] + n_hh["w"] // 2
    other_cx = n_other["x"] + n_other["w"] // 2
    join_y = 1152

    lines = [
        vline(*bottom_mid(n_start), top_mid(n_fill)[1]),
        vline(*bottom_mid(n_fill), top_mid(d_pdf)[1]),
        # PDF yes → Python (drop below diamond, then across)
        route([
            left_mid(d_pdf),
            (left_mid(d_pdf)[0], 360),
            (py_cx, 360),
            (py_cx, n_python["y"]),
        ]),
        # PDF no → merge rail
        route([right_mid(d_pdf), (720, d_pdf["cy"]), (720, merge_y), (CX, merge_y)]),
        # Python → merge rail
        route([(py_cx, n_python["y"] + n_python["h"]), (py_cx, merge_y), (CX, merge_y)]),
        vline(CX, merge_y, top_mid(n_chat)[1]),
        vline(*bottom_mid(n_chat), top_mid(n_track)[1]),
        vline(*bottom_mid(n_track), top_mid(n_pick)[1]),
        vline(*bottom_mid(n_pick), top_mid(n_draft)[1]),
        vline(*bottom_mid(n_draft), top_mid(n_review)[1]),
        vline(*bottom_mid(n_review), top_mid(d_where)[1]),
        # Where hh (route below diamond)
        route([
            left_mid(d_where),
            (left_mid(d_where)[0], 1030),
            (hh_cx, 1030),
            (hh_cx, n_hh["y"]),
        ]),
        # Where other
        route([
            right_mid(d_where),
            (right_mid(d_where)[0], 1030),
            (other_cx, 1030),
            (other_cx, n_other["y"]),
        ]),
        # Merge branches → apply
        route([(hh_cx, n_hh["y"] + n_hh["h"]), (hh_cx, join_y), (CX, join_y)]),
        route([(other_cx, n_other["y"] + n_other["h"]), (other_cx, join_y), (CX, join_y)]),
        vline(CX, join_y, top_mid(n_apply)[1]),
        vline(*bottom_mid(n_apply), top_mid(n_done)[1]),
    ]
    shapes.extend(lines)

    texts: list[str] = [
        plain_text(CX, 36, "Job Finder Kit — how it works", size=22, weight=700,
                   color="#0f172a", anchor="middle"),
        plain_text(CX, 58, "Folder + Cursor + AI helper. You review and apply yourself.",
                   size=14, color="#64748b", anchor="middle"),
        plain_text(64, 91, "AI helper in Cursor"),
        plain_text(224, 91, "You"),
        plain_text(304, 91, "Files / scripts"),
        plain_text(40, 118, "A. First-time setup (once)", size=16, weight=700, color="#1e40af"),
        plain_text(40, 606, "B. Each day / each application", size=16, weight=700, color="#1e40af"),
    ]

    texts += box_text(n_start, [
        ("Unzip or clone, install Cursor", 13, "#0f172a"),
        ("File → Open Folder → this folder", 11, "#475569"),
    ])
    texts += box_text(n_fill, [("Fill AGENTS.md and cv-base (your resume)", 13, "#0f172a")])
    texts.append(diamond_text(d_pdf, "Need PDF?"))
    texts += branch_label(250, 292, "yes")
    texts += branch_label(670, 292, "no / hh only")
    texts += box_text(n_python, [("Python + ONBOARDING step 4", 13, "#0f172a")])
    texts += box_text(n_chat, [
        ("First chat: @AGENTS.md — add jobs to tracker", 13, "#0f172a"),
        ("Agent mode · Cmd+L / Ctrl+L", 11, "#475569"),
    ])
    texts += box_text(n_track, [("Vacancies in tracker.md (numbered table)", 13, "#0f172a")])
    texts += box_text(n_pick, [("You: I like #3 and #7", 13, "#0f172a")])
    texts += box_text(n_draft, [
        ("Helper: applications/company-role/", 13, "#0f172a"),
        ("vacancy.md · cover.md · cv.md (if not hh)", 11, "#475569"),
    ])
    texts += box_text(n_review, [("You read, edit, say OK", 13, "#0f172a")])
    texts.append(diamond_text(d_where, "Where to apply?"))
    texts += branch_label(195, 944, "hh.ru")
    texts += branch_label(725, 944, "other site")
    texts += box_text(n_hh, [
        ("cover.md + resume", 13, "#0f172a"),
        ("on hh (cv-base-ru)", 11, "#475569"),
    ])
    texts += box_text(n_other, [
        ("cv.md, PDF if needed", 13, "#0f172a"),
        ("(generate_cv_unified.py)", 11, "#475569"),
    ])
    texts += box_text(n_apply, [("You apply on the employer site", 13, "#0f172a")])
    texts += box_text(n_done, [("Set status applied in tracker", 13, "#0f172a")])

    texts += [
        plain_text(CX, 1328, "Key files: tracker.md · AGENTS.md · cv-base · applications/",
                   size=12, color="#0f172a", anchor="middle"),
        plain_text(CX, 1346, "Details: ONBOARDING.md, README.md", color="#64748b", anchor="middle"),
    ]

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#334155"/>
    </marker>
    <style type="text/css"><![CDATA[{STYLES}]]></style>
  </defs>

{chr(10).join(shapes)}

{chr(10).join(texts)}
</svg>
'''

    out = Path(__file__).parent / "flow-diagram.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

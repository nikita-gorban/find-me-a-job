#!/usr/bin/env python3
"""Validate one application package against tracker and file conventions."""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List

from generate_cv_unified import PDF_FILENAME

ROOT = Path(__file__).parent
TRACKER = ROOT / "tracker.md"
APPLICATIONS = ROOT / "applications"


def tracker_row(number: str) -> Dict[str, str]:
    for line in TRACKER.read_text(encoding="utf-8").splitlines():
        if not re.match(rf"^\|\s*{re.escape(number)}\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        status_match = re.search(
            r"`(new|prep|ready|applied|declined|closed|skip)`", cells[-1]
        )
        return {
            "company": cells[1],
            "role": cells[2],
            "url": cells[8],
            "status": status_match.group(1) if status_match else "",
        }
    raise ValueError(f"tracker row #{number} not found")


def application_folder(number: str) -> Path:
    matches = sorted(
        path
        for path in APPLICATIONS.glob(f"{number}-*")
        if path.is_dir() and not path.name.startswith("_")
    )
    if len(matches) != 1:
        raise ValueError(f"expected one applications/{number}-* folder, found {len(matches)}")
    return matches[0]


def nonempty_lines(path: Path) -> List[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def cover_sentence_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    body = text.split("---", 1)[-1]
    body = re.split(r"\n\*\*[^*\n]+\*\*", body, maxsplit=1)[0]
    body = re.sub(r"\[[^\]]+\]\([^)]+\)", "", body)
    return len(re.findall(r"[.!?](?:\s|$)", body.strip()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Tracker/application number, e.g. 5")
    args = parser.parse_args()
    number = str(int(args.number))

    errors: List[str] = []
    warnings: List[str] = []
    try:
        row = tracker_row(number)
        folder = application_folder(number)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    vacancy = folder / f"{number}-vacancy.md"
    cover = folder / f"{number}-cover.md"
    cv = folder / f"{number}-cv.md"
    pdf = folder / PDF_FILENAME
    is_hh = "hh.ru/" in row["url"]

    if not vacancy.exists():
        errors.append(f"missing {vacancy.name}")

    if row["status"] in {"prep", "ready"} and not cover.exists():
        errors.append(f"{row['status']} requires {cover.name}")

    if row["status"] == "ready" and not is_hh:
        for path in (cv, cover, pdf):
            if not path.exists():
                errors.append(f"external ready application requires {path.name}")

    if cv.exists():
        lines = nonempty_lines(cv)
        if len(lines) < 3:
            errors.append(f"{cv.name}: expected name, vacancy role, contacts in first 3 lines")
        else:
            role_line = lines[1].replace("**", "").strip()
            tracker_role = re.sub(r"\s*\([^)]*\)\s*", " ", row["role"]).strip()
            if role_line.casefold() != tracker_role.casefold():
                warnings.append(
                    f"CV role {role_line!r} differs from tracker role {row['role']!r}"
                )

    if cover.exists():
        sentences = cover_sentence_count(cover)
        if not 3 <= sentences <= 5:
            warnings.append(f"{cover.name}: {sentences} sentence(s), expected 3–5")

    if cv.exists() and pdf.exists():
        if pdf.stat().st_mtime_ns < cv.stat().st_mtime_ns:
            errors.append(f"{pdf.name} is older than {cv.name}; regenerate PDF")

    if row["status"] in {"applied", "declined"}:
        warnings.append(
            f"status is {row['status']}: CV, cover, and PDF are immutable without explicit request"
        )

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"\n#{number} {row['company']} ({row['status']}): "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

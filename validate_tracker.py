#!/usr/bin/env python3
"""Validate tracker rows against numbered application folders."""

import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).parent
TRACKER = ROOT / "tracker.md"
APPLICATIONS = ROOT / "applications"
ACTIVE_STATUSES = {"new", "prep", "ready", "applied"}
TERMINAL_STATUSES = {"declined", "closed", "skip"}


def tracker_rows() -> List[Dict[str, str]]:
    rows = []
    for line in TRACKER.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 11:
            continue
        status_match = re.search(
            r"`(new|prep|ready|applied|declined|closed|skip)`", cells[-1]
        )
        rows.append(
            {
                "number": cells[0],
                "company": cells[1],
                "role": cells[2],
                "url": cells[8],
                "date": cells[9],
                "status": status_match.group(1) if status_match else "",
            }
        )
    return rows


def numbered_folders() -> Dict[str, List[Path]]:
    result: Dict[str, List[Path]] = {}
    for child in APPLICATIONS.iterdir():
        if not child.is_dir() or child.name.startswith("_"):
            continue
        match = re.match(r"^(\d+)-", child.name)
        if match:
            result.setdefault(match.group(1), []).append(child)
    return result


def main() -> int:
    rows = tracker_rows()
    folders = numbered_folders()
    errors: List[str] = []
    warnings: List[str] = []

    duplicate_rows = sorted(
        number for number, count in Counter(row["number"] for row in rows).items() if count > 1
    )
    if duplicate_rows:
        errors.append(f"duplicate tracker numbers: {duplicate_rows}")

    duplicate_folders = sorted(number for number, paths in folders.items() if len(paths) > 1)
    if duplicate_folders:
        errors.append(f"duplicate application folder numbers: {duplicate_folders}")

    row_by_number = {row["number"]: row for row in rows}
    for number, row in row_by_number.items():
        matches = folders.get(number, [])
        if not matches:
            message = f"#{number} {row['status']}: no applications/{number}-* folder"
            if row["status"] in ACTIVE_STATUSES:
                errors.append(message)
            else:
                warnings.append(message)
            continue
        if len(matches) != 1:
            continue
        folder = matches[0]
        vacancy = folder / f"{number}-vacancy.md"
        if not vacancy.exists():
            message = f"#{number}: missing exact file {vacancy.relative_to(ROOT)}"
            if row["status"] in ACTIVE_STATUSES:
                errors.append(message)
            else:
                warnings.append(message)

    for number, paths in folders.items():
        if number not in row_by_number:
            errors.append(
                f"orphan numbered folder(s) without tracker row: "
                f"{[str(path.relative_to(ROOT)) for path in paths]}"
            )

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    print(
        f"\nChecked {len(rows)} tracker rows and "
        f"{sum(len(paths) for paths in folders.values())} numbered folders: "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

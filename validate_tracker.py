#!/usr/bin/env python3
"""
Tracker consistency check.

Usage (macOS / Linux):
    python3 validate_tracker.py

Usage (Windows):
    py -3 validate_tracker.py

Cross-checks tracker.md row numbers against applications/<#>-<slug>/ folders:
  - every tracker.md row number has a matching application folder
  - every application folder (excluding applications/_*) has a matching row
  - no duplicate numbers on either side
Exits non-zero and lists the problems found; exits 0 with a summary otherwise.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TRACKER = ROOT / "tracker.md"
APPLICATIONS = ROOT / "applications"


def tracker_numbers() -> list[int]:
    numbers = []
    if not TRACKER.exists():
        return numbers
    for line in TRACKER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or not cells[0].isdigit():
            continue
        numbers.append(int(cells[0]))
    return numbers


def folder_numbers() -> list[int]:
    numbers = []
    if not APPLICATIONS.is_dir():
        return numbers
    for child in APPLICATIONS.iterdir():
        if not child.is_dir() or child.name.startswith("_"):
            continue
        m = re.match(r"^(\d+)-", child.name)
        if m:
            numbers.append(int(m.group(1)))
    return numbers


def find_duplicates(nums: list[int]) -> list[int]:
    seen, dupes = set(), set()
    for n in nums:
        if n in seen:
            dupes.add(n)
        seen.add(n)
    return sorted(dupes)


def main():
    t_nums = tracker_numbers()
    f_nums = folder_numbers()
    t_set, f_set = set(t_nums), set(f_nums)

    problems = []

    t_dupes = find_duplicates(t_nums)
    if t_dupes:
        problems.append(f"Duplicate row numbers in tracker.md: {t_dupes}")

    f_dupes = find_duplicates(f_nums)
    if f_dupes:
        problems.append(f"Duplicate application folder numbers: {f_dupes}")

    missing_folders = sorted(t_set - f_set)
    if missing_folders:
        problems.append(
            f"tracker.md rows with no applications/<#>-<slug>/ folder: {missing_folders}"
        )

    orphan_folders = sorted(f_set - t_set)
    if orphan_folders:
        problems.append(
            f"applications/<#>-<slug>/ folders with no tracker.md row: {orphan_folders}"
        )

    if problems:
        print("Tracker/applications mismatch:\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    print(f"OK — {len(t_set)} vacancy row(s), all matched to application folders.")


if __name__ == "__main__":
    main()

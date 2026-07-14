# Automations

Optional procedural playbooks for local Cursor loops. Shared filters, statuses, and fact rules live only in root `AGENTS.md`.

## Playbooks

- [`vacancy-scan.md`](vacancy-scan.md) — daily search for up to 7 active full-remote vacancies; creates tracker row and `<#>-vacancy.md` only.
- [`applied-status-check.md`](applied-status-check.md) — review `applied` applications every 2 days; does not change files without user reply.
- [`search-sources.md`](search-sources.md) — platform and careers reference; does not duplicate core filters.

## Before running

1. Add `@AGENTS.md` and `@tracker.md` to context.
2. For vacancy scan, also add `@cv-base-en.md`.
3. Do not modify materials for `applied` / `declined` applications.
4. After batch tracker changes, run `python3 validate_tracker.py`.

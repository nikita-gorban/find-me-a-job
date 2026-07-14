# Contributing to Job Finder Kit

This repo is a **template**. Contributions here should improve the kit itself
(scripts, docs, workflow) — not add your personal job search. Your own CV,
tracker, and application drafts belong in a private copy or fork, never in a
PR to this repo.

## Setup

```bash
git clone https://github.com/nikita-gorban/find-me-a-job.git
cd find-me-a-job
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Before opening a PR

- Run the PDF generators against the bundled example and confirm they still
  produce a valid one-page PDF:
  ```bash
  python3 generate_cv_unified.py applications/_example-do-not-track
  python3 generate_cover_pdf.py applications/_example-do-not-track
  ```
- If you touched `tracker.md` parsing or the `applications/` folder
  convention, run `python3 validate_tracker.py`.
- Before marking an application `ready`, run `python3 validate_application.py <#>`.
- CI (`.github/workflows/smoke-test.yml`) runs the same checks on every PR.
- If you change user-facing workflow (`AGENTS.md`, `ONBOARDING.md`,
  `README.md`), update `README.ru.md` to match, or note in the PR that the
  translation needs a follow-up.

## Scope

- `cv-base-en.example.md` / `cv-base-ru.example.md` must stay generic
  placeholders — never replace them with a real resume in a PR. (The working
  `cv-base-en.md` / `cv-base-ru.md` you fill in locally are gitignored, so
  this only matters if you touch the `.example` files directly.)
- Keep `applications/_example-do-not-track/` as a structural example only;
  don't turn it into a real application.

## Reporting issues

Open a GitHub issue with steps to reproduce (which script, which OS, the
exact command and error). For font-related errors, include the output of
`python3 -c "import platform; print(platform.system())"` and whether
`JOB_FINDER_FONT_DIR` is set.

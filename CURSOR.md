# Cursor — quick start

**Start here:** [ONBOARDING.md](ONBOARDING.md) (15 min checklist).

1. **Install [Cursor](https://cursor.com)** and sign in.
2. **Open this folder as the project root:** File → Open Folder → the folder that contains `README.md` and `AGENTS.md` (after unzip or clone). You can rename the folder.
3. **Fill [AGENTS.md](AGENTS.md) → User preferences** and [generate_cv_unified.py](generate_cv_unified.py) (`PDF_FILENAME`, `URL_FRAGMENTS`).
4. **Fill [cv-base-en.md](cv-base-en.md)** (and [cv-base-ru.md](cv-base-ru.md) if you use hh.ru).
5. **Agent chat:** **Cmd+L** (macOS) or **Ctrl+L** (Windows/Linux). Use **Agent** mode, not Ask.
6. **Rules context:** Cursor may load `AGENTS.md` automatically, but this is unreliable — **include `@AGENTS.md` in your first message**.
7. **Do not search for vacancies** until User preferences and cv-base are filled (see ONBOARDING).

**First prompts:**

```
@AGENTS.md @cv-base-en.md Read the rules. I'm looking for [role], [remote/location]. Add 10 active vacancies to tracker.md with verified links.
```

```
@AGENTS.md Prepare cover for vacancy #1.
```

```
@AGENTS.md Generate PDF for applications/company-role
```
(after `cv.md` is approved; non-hh only)

**hh.ru example:**

```
@AGENTS.md Vacancy #3 is hh.ru — cover only, no cv.md or PDF.
```

**Windows:** Explorer unzip is fine; Python — `py -3`, venv — see ONBOARDING. WSL not required. Prefer a project path without non-Latin characters.

Keep Markdown in a private git backup; do not commit secrets.

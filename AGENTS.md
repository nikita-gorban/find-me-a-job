# Job Finder Kit — Agent Instructions

Scope: all work in this project folder.

## Default language and style
- Communicate in the user's **Chat language** from User preferences (ask once if still blank).
- Keep wording concise and practical.

## User preferences (customize before use)

Replace bracketed placeholders with your values:

- **Chat language:** `[Russian / English]`
- **Roles:** `[e.g. Project Manager, Coordinator, Implementation PM]`
- **Location / remote:** `[e.g. EU remote; exclude employers based in Russia; timezone CET±2]`
- **Language requirements for vacancies:** `[e.g. accept only postings that require EN, RU, and/or PT up to A2 — exclude mandatory DE, FR, UA native, etc.]`
- **Platforms:** `[hh.ru, Lever, Greenhouse, Djinni, email, …]`
- **Cover letter:** `[~3–5 sentences; tone: direct / formal; if Russian first person: gender he/she and name for verb agreement]`
- **PDF filename:** `[Must match PDF_FILENAME in generate_cv_unified.py, e.g. Your_Name_CV.pdf]`

## Core workflow
1. Collect relevant vacancies in batches and keep `tracker.md` updated.
2. User selects vacancy numbers.
3. For each selected vacancy, create/update at minimum `applications/<slug>/vacancy.md` and `applications/<slug>/cover.md`.
4. **hh.ru:** cover only (+ optional `vacancy.md`). Application uses the resume on the platform (`cv-base-ru.md`); do not create `cv.md` / PDF in the folder unless the user asks.
5. **Other platforms** (Lever, Greenhouse, email, etc.): add `cv.md` when needed; PDF only after user approves `cv.md`:
   - macOS/Linux: `python3 generate_cv_unified.py applications/<slug>`
   - Windows: `py -3 generate_cv_unified.py applications/<slug>`
6. Wait for user approval of `cover.md` (and `cv.md` if present).

## Non-negotiable content rules
- No fabrication or exaggeration.
- Shift emphasis only within real experience.
- If a requirement is missing, state it honestly and position transferable evidence.
- Cover length: about 3–5 sentences unless the user sets otherwise.
- **Cover language = language of the vacancy posting** (not the same as “required candidate languages”).
- Do not open with “I am applying for…” / «Откликаюсь на роль…» — start with experience or fit.

## Vacancy quality rules
- Prioritize active vacancies; verify links before adding to the tracker.
- Apply only the search filters defined in **User preferences** above.
- If **User preferences** are still placeholders, **ask the user** for filters before adding many vacancies.
- If the user explicitly provides a vacancy outside their filters, proceed and flag the risk.

## Tracker discipline
- Statuses: `new`, `cv_draft`, `cv_approved`, `cover_done`, `pdf_ready`, `applied`, `skip`.
- When a vacancy is confirmed closed/expired, **delete its row** from the table and remove the notes entry.
- `skip` is transient; delete the row after the user confirms they are not pursuing it.
- **Match** column: `High` / `Medium` / `Low` (optional stretch/risk note in Notes).
- **Notes** format: `### #N Company — short title` then bullets (link check, fit, gaps).
- Do not assign tracker numbers to folders under `applications/_*` (examples only).

## File conventions
- Base CV: `cv-base-en.md` (most external applications), `cv-base-ru.md` (hh.ru one-click apply).
- Per-vacancy files: `applications/<slug>/` with **forward slashes** in paths (including on Windows), e.g. `applications/acme-pm`.
- **Slug:** lowercase, hyphens, `company-short-role-short`.
- PDF output name: `PDF_FILENAME` in `generate_cv_unified.py`.

## Optional files
- `applications/<slug>/questionnaire.md` — answers to employer forms.
- `applications/<slug>/assets.md` — portfolio links or attachments list.

# Job Finder Kit — Agent Instructions

Scope: all work in this project folder.

## Default language and style
- Communicate in the user's **Chat language** from User preferences (ask once if still blank).
- Keep wording concise and practical.

## User preferences (customize before use)

Replace bracketed placeholders with your values:

- **Chat language:** `[English / Russian / …]`
- **Roles:** `[e.g. Project Manager, Coordinator, Implementation PM]`
- **Location / remote:** `[e.g. full remote worldwide; EU timezone; exclude hybrid with regular onsite]`
- **Language requirements for vacancies:** `[e.g. accept only postings that require EN, RU, and/or PT up to A2 — exclude mandatory DE, FR, UA native, etc.]`
- **Platforms:** `[hh.ru, Lever, Greenhouse, Djinni, email, …]`
- **Cover letter:** `[~3–5 sentences; tone: direct / formal; if Russian first person: gender he/she for verb agreement]`
- **PDF filename:** `[Must match PDF_FILENAME in generate_cv_unified.py, e.g. Your_Name_CV.pdf]`

## Core workflow
1. Collect relevant vacancies in batches and keep `tracker.md` updated.
2. User selects vacancy numbers.
3. For each selected vacancy, create/update at minimum `applications/<slug>/vacancy.md` and `applications/<slug>/cover.md`.
4. **hh.ru:** cover only (+ optional `vacancy.md` for notes). Application uses the resume on the platform (`cv-base-ru.md`); do not create `cv.md` / PDF in the folder unless the user asks.
5. **Other platforms** (Lever, Greenhouse, email, wantapply, etc.): add `cv.md` when needed; PDF only after user approves `cv.md`:
   - macOS/Linux: `python3 generate_cv_unified.py applications/<slug>`
   - Windows: `py -3 generate_cv_unified.py applications/<slug>`
6. Wait for user approval of `cover.md` (and `cv.md` if present).
7. **Default PDF is CV** (`generate_cv_unified.py`). Cover PDF (`generate_cover_pdf.py`) — only when the user explicitly asks.

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
- **Location:** vacancies from any country, **including Russia**. Restrict by work format, not employer legal entity or HQ country.
- **Remote (when user wants remote-only):** only **clearly fully remote** roles — full remote, “remote work” with no mandatory office. **Exclude:** hybrid with regular onsite, office-first, relocation, vague “remote-friendly” without explicit full remote.
- For Russia-based employers — in `vacancy.md` verify remote is stated explicitly; flag ⚠️ if unclear.
- **Language filter:** exclude vacancies that **require any language other than** English, Russian, or Portuguese (A2). EN-only, RU-only, EN+RU, or PT A2 are fine. Do not add roles that mandate e.g. Ukrainian, German, French, Czech, or Portuguese above A2 — unless the user overrides.
- If the user explicitly provides a vacancy outside their filters, proceed and flag the risk clearly.

## Tracker discipline
- **Table only** in `tracker.md` — no notes block below the table. Vacancy details → `applications/<slug>/vacancy.md`.
- Statuses: `new` · `prep` · `ready` · `applied`.
  - `new` — listed, no materials yet
  - `prep` — preparing cv/cover; PDF not ready or awaiting edits
  - `ready` — CV PDF ready (or hh: cover ready; apply with platform resume)
  - `applied` — application submitted
- When adding a vacancy, create `applications/<slug>/vacancy.md` immediately (URL, fit, gaps, how to apply).
- When a vacancy is confirmed closed/expired, **delete its row from the table entirely**.
- `skip` — transient only, before deleting the row.
- **Match** column: `High` / `Medium` / `Low` (stretch or risk notes go in `vacancy.md`, not under the table).
- Do not assign tracker numbers to folders under `applications/_*` (examples only).

## File conventions
- Base CV: `cv-base-en.md` (most external applications), `cv-base-ru.md` (hh.ru one-click apply).
- Per-vacancy files: `applications/<slug>/` with **forward slashes** in paths (including on Windows), e.g. `applications/acme-pm`.
- **Slug:** lowercase, hyphens, `company-short-role-short`.
- PDF output name: `PDF_FILENAME` in `generate_cv_unified.py`.

## Optional files
- `applications/<slug>/questionnaire.md` — answers to employer forms.
- `applications/<slug>/assets.md` — portfolio links or attachments list.

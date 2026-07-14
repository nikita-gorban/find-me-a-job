# Job Finder Kit — Agent Instructions

Scope: all work in this project folder.

> This file belongs to the reusable **template kit**. In a customized working
> repository, the root `AGENTS.md` is authoritative; do not use this template to
> override instance-specific rules.

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
3. For each selected vacancy, create/update at minimum `applications/<#>-<slug>/<#>-vacancy.md` and `applications/<#>-<slug>/<#>-cover.md`.
4. **hh.ru:** cover only (+ optional `<#>-vacancy.md` for notes). Application uses the resume on the platform (`cv-base-ru.md`); do not create `<#>-cv.md` / PDF in the folder unless the user asks.
5. **Other platforms** (Lever, Greenhouse, email, wantapply, etc.): add `<#>-cv.md` when needed; PDF only after user approves `<#>-cv.md`:
   - macOS/Linux: `python3 generate_cv_unified.py applications/<#>-<slug>`
   - Windows: `py -3 generate_cv_unified.py applications/<#>-<slug>`
6. Wait for user approval of `<#>-cover.md` (and `<#>-cv.md` if present).
7. **Default PDF is CV** (`generate_cv_unified.py`). Cover PDF (`generate_cover_pdf.py`) — only when the user explicitly asks.

## Sources of truth and fact safety
- **Facts about experience** come only from `cv-base-en.md`, `cv-base-ru.md`, and explicit user corrections in the current chat.
- **Do not** copy facts, wording, or experience structure from other `applications/*-cv.md`, `applications/*-cover.md`, or responses for other vacancies — unless the user explicitly asks to work on that application.
- Before creating or fully checking a tailored CV, re-read the appropriate canonical CV. After preparation, line-check dates, titles, companies, numbers, tools, and scope of every claim.
- Tailoring changes emphasis only. Any new claim not in the canonical CV must be confirmed with the user first.
- If the user clarifies a permanent fact (dates, language level, project count, tool), suggest syncing both canonical CVs; do not silently propagate the change to other materials.
- Do not infer current employment from year ranges. “Currently working at…” is allowed only after explicit user confirmation.

## Non-negotiable content rules
- No fabrication or exaggeration.
- Shift emphasis only within real experience.
- If a requirement is missing, state it honestly and position transferable evidence.
- Cover length: about 3–5 sentences unless the user sets otherwise.
- **Cover language = language of the vacancy posting** (not the same as “required candidate languages”).
- Do not open with “I am applying for…” / «Откликаюсь на роль…» — start with experience or fit.
- **Job title in `<#>-cv.md`** (line under the name) must match the vacancy role title, not a generic default like “Project Manager”. Use the exact or closest role name from the posting (without platform tags like “- Gaming”, “(Full Remote/Full Time)”).

## Vacancy quality rules
- Prioritize active vacancies; verify links before adding to the tracker.
- Apply only the search filters defined in **User preferences** above.
- If **User preferences** are still placeholders, **ask the user** for filters before adding many vacancies.
- **Location:** vacancies from any country, **including Russia**. Restrict by work format, not employer legal entity or HQ country.
- **Remote (when user wants remote-only):** only **clearly fully remote** roles — full remote, “remote work” with no mandatory office. **Exclude:** hybrid with regular onsite, office-first, relocation, vague “remote-friendly” without explicit full remote.
- For Russia-based employers — in `<#>-vacancy.md` verify remote is stated explicitly; flag ⚠️ if unclear.
- **Language filter:** exclude vacancies that **require any language other than** English, Russian, or Portuguese (A2). EN-only, RU-only, EN+RU, or PT A2 are fine. Do not add roles that mandate e.g. Ukrainian, German, French, Czech, or Portuguese above A2 — unless the user overrides.
- If the user explicitly provides a vacancy outside their filters, proceed and flag the risk clearly.

## Tracker discipline
- **Table only** in `tracker.md` — no notes block below the table. Vacancy details → `applications/<#>-<slug>/<#>-vacancy.md`.
- **Applied** column — application date (`YYYY-MM-DD`). When status becomes `applied`, set today unless the user gives another date. For `declined`, keep the application date; use `?` if unknown. For other statuses — `—`.
- Statuses: `new` · `prep` · `ready` · `applied` · `declined` · `closed` · `skip`.
  - `new` — listed, no materials yet
  - `prep` — preparing cv/cover; PDF not ready or awaiting edits
  - `ready` — CV PDF ready (or hh: cover ready; apply with platform resume)
  - `applied` — application submitted
  - `declined` — rejection (employer or yours, incl. ghost)
  - `closed` — vacancy closed/expired (no application or process ended because posting closed)
  - `skip` — deliberately not pursuing; keep the row as history
- **Never delete tracker rows** — including after rejection or vacancy closure; details and outcome → `applications/<#>-<slug>/<#>-vacancy.md`.
- **Vacancy scan (optional):** see `automations/vacancy-scan.md` — local loop once per day, up to 7 new vacancies, no cover/cv/PDF.
- **Applied review (optional):** see `automations/applied-status-check.md` — local loop every 2 days; ghost candidates after **14 days** without pipeline.
- When adding a vacancy, create `applications/<#>-<slug>/<#>-vacancy.md` immediately (URL, fit, gaps, how to apply).
- On rejection: status → `declined`, outcome and context in `applications/<#>-<slug>/<#>-vacancy.md`.
- On vacancy closure: status → `closed`, date and context in `applications/<#>-<slug>/<#>-vacancy.md`.
- **Status markers in `tracker.md`:** colored circles in the last column (Cursor/VS Code preview) — ⚪ `new` · 🟡 `prep` · 🔵 `ready` · 🟢 `applied` · 🔴 `declined` · ⚫ `closed` · 🟣 `skip`.
- **Match** column: `High` / `Medium` / `Low` (stretch or risk notes go in `<#>-vacancy.md`, not under the table).
- Do not assign tracker numbers to folders under `applications/_*` (examples only).
- After batch tracker/folder changes, run `python3 validate_tracker.py`.
- Before marking a vacancy `ready`, run `python3 validate_application.py <#>`.

### Status transitions and immutability
- Main path: `new → prep → ready → applied`.
- `new → prep`: cover/CV preparation started.
- `prep → ready`: user approved materials; for external platforms PDF built and verified; for hh.ru cover is ready.
- `ready → applied`: **only after explicit user message** that the application was submitted; then set the date.
- `declined`, `closed`, `skip` — terminal history states; do not delete rows.
- After `applied` or `declined`, do not change `<#>-cv.md`, `<#>-cover.md`, or PDF without an explicit user request for that application. Updating outcome/pipeline in `<#>-vacancy.md` and preparing interview materials is allowed.

### PDF gate
- Before generation, ask the user to save an open `<#>-cv.md` if they reported manual edits; the generator reads from **disk**, not unsaved editor buffers.
- Generate PDF only from the exact `applications/<#>-<slug>/<#>-cv.md`.
- After generation require: exit code 0, one page, correct fields and links, PDF newer than Markdown, extracted text contains key edits.
- If any check fails, do not set `ready` and do not report PDF as ready.

## File conventions
- **Vacancy folder:** `applications/<#>-<slug>/`, where `#` is the row number in `tracker.md`, `slug` is a short Latin name (`acme-pm-digital`).
- **Files in folder:** `<#>-<name>` — e.g. `5-vacancy.md`, `5-cover.md`, `5-cv.md`, `5-interview-prep.md`. PDF without prefix: `PDF_FILENAME` from `generate_cv_unified.py`.
- Folders **without a number** — service folders or vacancies outside the tracker (`hh-ru`, drafts).
- Base CV: `cv-base-en.md` (most external applications), `cv-base-ru.md` (hh.ru one-click apply).
- Per-vacancy paths: always `applications/<#>-<slug>/` with **forward slashes** (including on Windows).
- Optional files with the same numeric prefix: `<#>-form-answers.md`, `<#>-interview-prep.md`, `<#>-email.md`, `<#>-company-brief.md`, `<#>-test-assignment.md`, `<#>-assets.md`, `<#>-projects.md`, `<#>-questionnaire.md`.

## Optional automations

Playbooks in `automations/` are **optional** local Cursor loops. They reference filters and fact rules from this file — do not duplicate or override them. See [`automations/README.md`](automations/README.md).

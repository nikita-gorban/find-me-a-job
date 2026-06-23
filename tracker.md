# Job Application Tracker

## How to use / Как пользоваться

1. Mark vacancy numbers you want to pursue — the agent prepares materials.
2. After you approve `cover.md`, apply or continue. For **non-hh** platforms: also approve `cv.md`, then generate PDF.
3. See [AGENTS.md](AGENTS.md) for statuses and rules.

**Statuses:** `new` · `cv_draft` · `cv_approved` · `cover_done` · `pdf_ready` · `applied` · `skip` (transient)

| Platform | Files |
|----------|--------|
| **hh.ru** | `cover.md` (+ optional `vacancy.md`); resume on site from `cv-base-ru.md` |
| **Other** | + `cv.md` → approve → `python3` / `py -3 generate_cv_unified.py applications/<slug>` |

**Match:** `High` · `Medium` · `Low` — optional stretch or risk in Notes.

---

## Vacancies / Вакансии

| # | Company | Role | Industry | Country | Remote | Salary | Match | URL | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | `new` |

---

## Notes / Заметки

Format per vacancy:

```markdown
### #1 Company Name — Role short title
- Link check: active as of YYYY-MM-DD
- Fit: …
- Gaps: …
```

---

## Next step

Tell the agent which numbers to work on, e.g. *“Let's do #1, #2.”*

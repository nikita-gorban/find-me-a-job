# Vacancy Scan — Agent Instructions

> **Loop (local):** `@AGENTS.md` `@tracker.md` `@cv-base-en.md` `@automations/vacancy-scan.md` `@automations/search-sources.md`

---

## Loop mode (local `/loop`)

Works only while **Cursor is open** and the session is alive. Mac sleep / closed Cursor → ticks do not run.

### Start

```
/loop 1d @AGENTS.md @tracker.md @cv-base-en.md @automations/vacancy-scan.md @automations/search-sources.md Run vacancy scan per automations/vacancy-scan.md. Up to 7 new vacancies. Do not touch applied/declined/ready/prep rows or their files. Do not create cover/cv. Short report in User preferences chat language. If 0 new — do not change files.
```

### Stop

**"stop loop vacancy scan"**

---

## Goal

Once per day find up to **7** relevant active vacancies and update `tracker.md` + `applications/<#>-<slug>/<#>-vacancy.md`.

Quality, remote, language, and file-format filters — from `AGENTS.md` only.

---

## Target roles

Search first for roles defined in **User preferences**. Default examples:

- Project Manager, Delivery Manager, Technical Project Manager, PMO / Project Coordinator (junior+).
- Ops roles with delivery focus: AI / automation PM, implementation PM, program PM.

Domains to prioritize (adjust in User preferences): web/digital agency, SaaS / B2B, outsourcing / IT services, gamedev, AI / product operations.

Role exclusions (general remote/language filters — only in `AGENTS.md`):

- recruitment / HR coordinator;
- pure marketing PM without delivery / implementation / production ownership.

---

## Platforms

The list below is a required starting set, **not a ceiling**. Use any additional source with an active direct vacancy link.

Extended reference (MVEC, Notion company lists, localization vendors, gamedev careers): [`automations/search-sources.md`](search-sources.md).

Each run: at least **2 Tier A** platforms, **1 Tier B**, one Tier C open search, and **one direct-careers block** from `search-sources.md` (rotate).

### Tier A — primary

| Platform | Search for | Notes |
| --- | --- | --- |
| [wantapply.com](https://wantapply.com) | PM, delivery, technical PM, remote | Check archived / no longer active |
| [djinni.co](https://djinni.co) | project manager, delivery, remote | EN/RU; skip Ukrainian mandatory |
| [hh.ru](https://hh.ru) | «удалённо» + project manager / delivery | RU employer → verify explicit full remote |
| [vseti.app](https://www.vseti.app) | PM, coordinator, digital agency | RU-speaking agencies |
| Lever (`jobs.lever.co`, `jobs.eu.lever.co`) | project manager remote | site search or direct company URLs |
| Greenhouse (`job-boards.greenhouse.io`) | project manager remote | Agency, SaaS, product shops |
| [remote-job.ru](https://remote-job.ru) | project manager | RU remote IT |

### Tier B — secondary

| Platform | Focus |
| --- | --- |
| [remoteotter.com](https://remoteotter.com) | Remote PM, gamedev, SaaS |
| [ingamejob.com](https://ingamejob.com) | Gamedev PM |
| [itjobs.pt](https://www.itjobs.pt) | Portugal / EU remote |
| Target company careers | IT outsourcing, SaaS, gamedev, agency — see [`search-sources.md`](search-sources.md) |
| [DOU.ua](https://jobs.dou.ua) | Only if remote + no Ukrainian mandatory |
| Ashby / Comeet / BambooHR | By companies from tracker and similar employers |
| [getmatch.ru](https://getmatch.ru) | PM remote, RU/EN |
| [MVEC](https://mvec.com.ru/temp/findvacancy.php) | Gamedev PM/producer reposts; cross-check careers |
| [AgileFluent Notion ~600](https://agilefluent.notion.site/600-3594f367824780d7b613d292007e08e1) | Company list by industry → spot-check careers |

### Tier C — open search

- Web search: `remote project manager lever 2026`, `delivery manager remote greenhouse`, etc.
- Careers pages of companies with good historical fit from your tracker.
- Gamedev / localization sources from [`search-sources.md`](search-sources.md).
- LinkedIn — only if the posting opens without login; otherwise skip and note in the report.
- Any new aggregator or direct careers page with a verifiable active link.

### Source rotation

Rotate sources by day to avoid repeating the same query. Use `(today - anchor_date) % 5 + 1` where **anchor_date** is the date you first enabled the loop (or note it in User preferences).

| Cycle day | Sources |
| --- | --- |
| 1 | wantapply + djinni + Lever + MVEC + open search (digital agency / SaaS) |
| 2 | hh.ru + vseti.app + Greenhouse + localization vendors + RU/EN remote search |
| 3 | remoteotter + itjobs.pt + gamedev batch A + EU / Portugal remote search |
| 4 | ingamejob + DOU + gamedev batch B + gamedev / outsourcing search |
| 5 | getmatch + remote-job.ru + AgileFluent Notion (5–10 companies) + AI / automation PM search |

If a source fails or yields few results, swap for the nearest relevant alternative and note it in the report.

---

## Algorithm each tick

1. Read `AGENTS.md`, `tracker.md`, `cv-base-en.md`.
2. Build dedupe set from URLs and company+role pairs in `tracker.md`.
3. Pick sources by rotation and search. Platform list is not a ceiling.
4. For each candidate verify:
   - link active, not archived / expired / 404;
   - full remote stated explicitly;
   - languages match `AGENTS.md`;
   - role matches target profile;
   - not a duplicate URL / company+role;
   - fit can be explained honestly via `cv-base-en.md`.
5. Select up to **7** best vacancies. Priority: High fit, then Medium; Low only with a clear reason.
6. Do not change rows with status `applied`, `declined`, `ready`, `prep` or any files in those folders.
7. For each new vacancy:
   - take next `#`;
   - add row to `tracker.md` with ⚪ `new`;
   - create `applications/<#>-<slug>/<#>-vacancy.md` (URL, company, format, salary, level, date found, role, fit, gaps, how to apply).
8. Do not create cover, CV, PDF, or interview prep.
9. If **0 new** — do not change files; report only.
10. Optional: if an obvious closed ⚪ `new` vacancy is found, set `closed` and note context in its `vacancy.md` (max 2–3 checks per tick).

---

## Report format

Short report in **User preferences chat language**:

```
## Vacancy scan — YYYY-MM-DD

Added: N (#...)
Sources: ...
Skipped: archived/expired, hybrid, language, duplicate, low fit — briefly

Top picks:
- #... Company — why good fit
```

If none added:

```
## Vacancy scan — YYYY-MM-DD

No new vacancies. Files unchanged.
Checked: ...
Main skip reasons: ...
```

---

## Do not

- Commit.
- Create cover / CV / PDF.
- Fabricate experience or fit.
- Add vacancies without an active link.
- Add roles with vague remote-friendly when full remote is not explicit.
- Delete rows from `tracker.md`.

# Applied Status Check — Agent Instructions

> **Loop (local):** `@AGENTS.md` `@tracker.md` `@automations/applied-status-check.md`

---

## Loop mode (local `/loop`)

Works only while **Cursor is open** and the session is alive.

### Start

```
/loop 2d @AGENTS.md @tracker.md @automations/applied-status-check.md Review applied applications per automations/applied-status-check.md. Show review list, ask for updates. Do not change files without user reply.
```

Test first run: `/loop 30m` or `/loop 2h`, then restart with `2d`.

### Stop

**"stop loop applied check"**

### Constraints

- Mac sleep / closed Cursor → ticks do not run
- Without user reply — **do not change** `tracker.md` or `vacancy.md`

---

## Goal

Every 2 days remind about `applied` submissions so ghosted applications do not pile up. User replies **in batch** — agent updates files.

**Ghost threshold:** application older than **14 days** with no active pipeline.

---

## Algorithm each tick

1. Read `tracker.md`, select rows with status `applied`.
2. For each — **Applied** column (`YYYY-MM-DD` or `?`).
3. Compute **days since application** (today − date; for `?` mark "date unknown").
4. Detect **active pipeline** (do not suggest ghost):
   - in `applications/<#>-<slug>/<#>-vacancy.md` there is `pipeline:` / `Pipeline:` / active-process note;
   - or folder has `<#>-interview-prep.md`.
5. Split into groups and show a **compact table** (User preferences chat language):

### Group A — "Needs review" (priority)

`applied` + **≥ 14 days** + no active pipeline.

Format: `# · Company · role (short) · N days · slug`

### Group B — "Active process"

`applied` + pipeline / `interview-prep.md`.

Format: `# · Company · pipeline (if known from vacancy.md)`

### Group C — "Waiting, < 14 days"

One summary line: count and numbers, no detailed poll.

### Group D — "Date unknown" (`?`)

Ask for date or ghost/declined separately.

6. **Ask** for updates. Example reply format:

```
37,38,39 — ghost
70 — pipeline, stage 2
64 — applied 2026-06-20
rest unchanged
```

7. **Only after user reply** apply changes (see below).
8. If `applied` = 0 — short message and exit.

---

## Applying updates

| User reply | `tracker.md` | `applications/<#>-<slug>/<#>-vacancy.md` |
| --- | --- | --- |
| `ghost` / no response | `declined` | `## Outcome` → ghost, N days without reply, date |
| rejection from employer | `declined` | `## Outcome` → employer rejection, context |
| `pipeline` / interview / stage N | stays `applied` | update `pipeline: …` |
| new application date | **Applied** column | sync in vacancy if needed |
| `rest unchanged` | leave others | — |

**Ghost = `declined`** — no separate status.

On `declined` **do not delete the row** (`AGENTS.md`).

---

## Resolving # → folder

Do not maintain manual mappings — they go stale quickly.

1. Find exactly one folder matching `applications/<#>-*`.
2. Verify exact `<#>-vacancy.md` exists.
3. If 0 or 2+ folders — find URL from tracker content and report desync.
4. Before batch updates run `python3 validate_tracker.py`.
5. If an active/applied row has no folder — create minimal `<#>-vacancy.md` from tracker data without inventing details.

---

## Do not

- Change statuses `new` / `prep` / `ready`
- Touch `declined` without explicit request
- Create cover/cv
- Commit
- Auto-set `declined` by age alone — only on user reply

---

## Report

Short summary in User preferences chat language: counts in A/B/C/D, what changed after reply (or "waiting for reply").

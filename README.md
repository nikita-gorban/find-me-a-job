# Job Finder Kit — job search with an AI helper

*[Читать по-русски](README.ru.md)*

Think of this folder as a **notebook on your computer**: one table lists jobs, other pages hold draft cover letters and CVs. Next to you sits an **AI helper inside Cursor** (a chat app for work with files). It finds jobs and writes drafts; **you** read, fix, and click “apply” yourself. It must **not invent experience** — only your real facts.

You don’t need to be a programmer. You need Cursor, the internet, and time to fill in your details once.

**This kit is local-first** — see [Local use (important)](#local-use-important) below.

**Not on Cursor?** `AGENTS.md` is a shared convention read by several AI coding tools (Cursor, Claude Code, Windsurf, and others). Any of them works here — just swap the chat shortcut in [CURSOR.md](CURSOR.md) for your tool's equivalent.

---

## Get the kit

**Clone from GitHub:**

```bash
git clone https://github.com/nikita-gorban/find-me-a-job.git
cd find-me-a-job
```

**Or** on GitHub: **Code → Download ZIP** → unzip → open the folder in Cursor.

> **Not comfortable with git?** ZIP is enough. You only download the kit once; daily job search does **not** require GitHub, commits, or pushes.

Your real application folders under `applications/` are **gitignored** — drafts and PDFs stay on your machine and are **not** meant for the public repo.

---

## Local use (important)

This project is **optimized for local use on your computer**, not as a cloud app or a repo you update while applying.

| | Once (setup) | Every day (job search) |
|---|---|---|
| **What you do** | Download kit → open in Cursor → fill `AGENTS.md` and cv-base | Chat with the helper, edit `tracker.md` and files in `applications/` |
| **Git / GitHub** | Optional: `git clone` or ZIP | **Not required** — no need to commit or push |
| **Where data lives** | Same folder on your disk | Same folder; optionally iCloud / Dropbox / **private** git backup |

**Why:** cover letters, tailored CVs, and application history are personal. The public repo is a **template**; your hunt stays local by default (`applications/` is in `.gitignore`).

**Do not** push your application materials to [find-me-a-job](https://github.com/nikita-gorban/find-me-a-job) — fork only if you want to customize the kit itself, in a **separate** private copy.

---

## Where to start

**Open [ONBOARDING.md](ONBOARDING.md)** — step-by-step first setup (~15–30 minutes, breaks OK).

**Full flow:** [flow-diagram.svg](flow-diagram.svg) (image) · [FLOW.md](FLOW.md) (diagrams in Cursor)

Short version: install Cursor → open **this folder** → fill in your CV and rules → send the helper your first message.

More about chat and keys: [CURSOR.md](CURSOR.md).

---

## How it works (simple)

1. The **helper** finds jobs and writes them into [tracker.md](tracker.md) (numbered table).
2. **You** say: “I like #3 and #7.”
3. The **helper** creates drafts under `applications/<#>-<slug>/`: job notes, cover letter, sometimes a tailored CV.
4. **You** edit the text until it sounds like you, then say “OK” or “make it shorter.”
5. If you need a **PDF CV** (not for hh.ru) — one terminal command (explained in ONBOARDING).
6. **You** submit the application on the employer’s site.

The helper does **not** apply for you and does **not** promise an offer. It saves time on boring drafts.

---

## Two kinds of job sites

| Where you apply | What we prepare in the folder | Your CV at apply time |
|-----------------|------------------------------|------------------------|
| **hh.ru** | `<#>-cover.md` + notes | CV already on hh (from your `cv-base-ru.md`, see [cv-base-ru.example.md](cv-base-ru.example.md)) |
| **Others** (email, Lever, Greenhouse…) | `<#>-cover.md` + `<#>-cv.md` + PDF if needed | You attach files yourself |

---

## What’s in this folder

| File | In plain words |
|------|----------------|
| **[ONBOARDING.md](ONBOARDING.md)** | First-time setup — **start here** |
| **[AGENTS.md](AGENTS.md)** | Rules for the helper (what jobs to find, how to write). **Fill in for you** |
| **[CURSOR.md](CURSOR.md)** | How to open chat and which keys to press |
| **[FLOW.md](FLOW.md)** | Workflow diagrams |
| **[cv-base-en.example.md](cv-base-en.example.md)** | Template — copy to `cv-base-en.md` (gitignored) and fill in your real CV |
| **[cv-base-ru.example.md](cv-base-ru.example.md)** | Russian template for hh.ru — copy to `cv-base-ru.md` (gitignored); section headers stay in Russian |
| **tracker.md** | Your job list (table only) |
| **generate_cv_unified.py** | Text CV → one-page PDF |
| **generate_cover_pdf.py** | Cover letter PDF — only when you ask |
| **validate_tracker.py** | Checks tracker.md rows match `applications/<#>-<slug>/` folders (catches typos/duplicates) |
| **validate_application.py** | Checks one application folder before marking `ready` (files, cover length, PDF freshness) |
| **applications/** | One subfolder per job: `applications/<#>-<slug>/` |
| **applications/_example-do-not-track/** | Example only — don’t add to the tracker |

`.md` files are normal text — open and edit in Cursor like a notepad.

---

## Tracker status words

| Word | Means |
|------|--------|
| `new` | Found, not started yet |
| `prep` | Drafting cv/cover or waiting for your edits |
| `ready` | CV PDF ready (or hh: cover ready) |
| `applied` | You already applied |
| `declined` | Rejected or ghosted — row stays for history |
| `closed` | Vacancy closed/expired — row stays for history |
| `skip` | Deliberately skipped — row stays for history |

---

## Good to know

- **Local-first** — work in a folder on your machine; git is optional after download (see [Local use](#local-use-important)).
- The helper can be wrong — **always read** before you send anything.
- Start your first chat with **`@AGENTS.md`** so it reads your rules.
- Cover letters: **short**, about 3–5 sentences, in the **same language as the job ad**.
- Python and PDF are **optional** — mainly if you apply outside hh and need a PDF file. See ONBOARDING.

**Sharing this kit:** copy a short blurb from [SHARE.md](SHARE.md) (Russian + English).

Stuck on a step? Ask in chat: “I’m on step X in ONBOARDING and …”

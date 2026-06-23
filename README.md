# Job Finder Kit — job search with an AI helper

Think of this folder as a **notebook on your computer**: one table lists jobs, other pages hold draft cover letters and CVs. Next to you sits an **AI helper inside Cursor** (a chat app for work with files). It finds jobs and writes drafts; **you** read, fix, and click “apply” yourself. It must **not invent experience** — only your real facts.

You don’t need to be a programmer. You need Cursor, the internet, and time to fill in your details once.

---

## Get the kit

**Clone from GitHub:**

```bash
git clone https://github.com/nikita-gorban/find-me-a-job.git
cd find-me-a-job
```

**Or** on GitHub: **Code → Download ZIP** → unzip → open the folder in Cursor.

Your real application folders under `applications/` are **gitignored** — drafts and PDFs stay on your machine.

---

## Where to start

**Open [ONBOARDING.md](ONBOARDING.md)** — step-by-step first setup (~15–30 minutes, breaks OK).

Short version: install Cursor → open **this folder** → fill in your CV and rules → send the helper your first message.

More about chat and keys: [CURSOR.md](CURSOR.md).

→ **Russian:** [README.ru.md](README.ru.md)

---

## How it works (simple)

1. The **helper** finds jobs and writes them into [tracker.md](tracker.md) (numbered table).
2. **You** say: “I like #3 and #7.”
3. The **helper** creates drafts under `applications/`: job notes, cover letter, sometimes a tailored CV.
4. **You** edit the text until it sounds like you, then say “OK” or “make it shorter.”
5. If you need a **PDF CV** (not for hh.ru) — one terminal command (explained in ONBOARDING).
6. **You** submit the application on the employer’s site.

The helper does **not** apply for you and does **not** promise an offer. It saves time on boring drafts.

---

## Two kinds of job sites

| Where you apply | What we prepare in the folder | Your CV at apply time |
|-----------------|------------------------------|------------------------|
| **hh.ru** | Letter + notes | CV already on hh (from [cv-base-ru.md](cv-base-ru.md)) |
| **Others** (email, Lever, Greenhouse…) | Letter + CV file + PDF if needed | You attach files yourself |

---

## What’s in this folder

| File | In plain words |
|------|----------------|
| **[ONBOARDING.md](ONBOARDING.md)** | First-time setup — **start here** |
| **[AGENTS.md](AGENTS.md)** | Rules for the helper (what jobs to find, how to write). **Fill in for you** |
| **[CURSOR.md](CURSOR.md)** | How to open chat and which keys to press |
| **cv-base-en.md** | Your main CV (English) — source for everything |
| **cv-base-ru.md** | Same in Russian, including hh |
| **tracker.md** | Your job list |
| **generate_cv_unified.py** | Small program: text CV → one-page PDF |
| **applications/** | One subfolder per job |
| **applications/_example-do-not-track/** | Example only — don’t add to the tracker |

`.md` files are normal text — open and edit in Cursor like a notepad.

---

## If you got a zip file

1. Unzip it.
2. In Cursor: **File → Open Folder**.
3. Pick the folder where you **immediately see** `README.md` and `AGENTS.md`.  
   If you only see another folder inside, open that inner folder instead.

---

## Tracker status words

| Word | Means |
|------|--------|
| `new` | Found, not started yet |
| `cv_draft` | CV draft needs your review |
| `cv_approved` | CV OK |
| `cover_done` | Cover letter OK |
| `pdf_ready` | PDF built |
| `applied` | You already applied |
| `skip` | Not pursuing — remove the row later |

---

## Good to know

- The helper can be wrong — **always read** before you send anything.
- Start your first chat with **`@AGENTS.md`** so it reads your rules.
- Cover letters: **short**, about 3–5 sentences, in the **same language as the job ad**.
- Python and PDF are **optional** — mainly if you apply outside hh and need a PDF file. See ONBOARDING.

Stuck on a step? Ask in chat: “I’m on step X in ONBOARDING and …”

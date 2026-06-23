# First-time setup — step by step

This guide is for people who **have never used Cursor or a terminal**. Time: about **15–30 minutes**. You can pause between steps.

**This folder is the whole project.** No parent folder needed.

Quick reference: [README.md](README.md) · Cursor keys: [CURSOR.md](CURSOR.md)

---

## What you are setting up

| Step | In plain words |
|------|----------------|
| 1 | Open the folder in Cursor |
| 2 | Tell the helper **what job** you want |
| 3 | Paste **your real resume** instead of the template |
| 4 | (Optional) Install Python to build PDFs later |
| 5 | Send the helper your first chat message |

---

## Step 0. What is Cursor? (30 seconds)

**Cursor** is an editor with a chat panel. Files are on the left (same as this folder); on the right you talk to an **AI helper**. It can read and edit your files — **you can always undo** (Ctrl+Z / Cmd+Z).

Download: [cursor.com](https://cursor.com) → install → sign in.

---

## Step 1. Open this folder

- **From GitHub:** `git clone https://github.com/nikita-gorban/find-me-a-job.git` → enter the `find-me-a-job` folder.
- **Or ZIP:** download from GitHub (**Code → Download ZIP**). You can rename the folder (e.g. `my-job-search`).
- In Cursor: **File → Open Folder**.
- Pick the folder where you **immediately see** `README.md` and `AGENTS.md`.
- **Windows tip:** prefer a path without non-Latin characters, e.g. `C:\Users\You\job-search` instead of long paths with spaces.

Check: `tracker.md` and the `applications/` folder appear in the file list on the left.

---

## Step 2. Rules for the helper — `AGENTS.md`

1. Open [AGENTS.md](AGENTS.md) (click on the left).
2. Find the **User preferences** block.
3. Replace text in `[square brackets]` with **your** values, for example:
   - target role (PM, coordinator…);
   - remote / location filters;
   - which vacancy languages you accept;
   - platforms (hh.ru vs international);
   - cover letter tone.

This is the helper’s standing instructions — without it, results will be generic.

Also at the top of [generate_cv_unified.py](generate_cv_unified.py) (if you will build PDFs):

- `PDF_FILENAME` — output name, e.g. `Smith_CV.pdf`;
- `URL_FRAGMENTS` — fragments of your links (telegram, email) so PDF links stay clickable.

---

## Step 3. Your resume — replace the template

Open [cv-base-en.md](cv-base-en.md) — your **English** master resume.

- Remove placeholder examples.
- Write **only true facts**: name, experience, skills.
- Short experience is fine — honesty beats padding.

If you use **hh.ru**, do the same in [cv-base-ru.md](cv-base-ru.md) (Russian section headers stay Russian; paste the text into your hh profile).

Delete the one-line reminder at the top of `cv-base-ru.md` after you read it.

---

## Step 4. Python and PDF — do you need it?

**Skip step 4** if:

- you apply **only via hh.ru**, and nobody asks for a PDF file.

**Do step 4** if:

- you need a **PDF resume** (common on international job boards).

### What Python does here

**Python** is a free runtime. Our small script `generate_cv_unified.py` turns resume text into a one-page PDF. Install once, then one command per application.

### Install Python

- Site: [python.org/downloads](https://www.python.org/downloads/)
- **Windows:** check **“Add python.exe to PATH”** during install.
- Test: open a terminal in Cursor (**Terminal → New Terminal** at the bottom).

### Commands (copy one line at a time)

You are already in the project folder if you opened it via **Open Folder**.

**Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows** (terminal at the bottom of Cursor):

```bat
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

What this does:

- `.venv` — isolated library folder;
- `activate` — use that environment (you may see `(.venv)` in the prompt);
- `pip install` — installs PDF dependencies.

If you see “command not found”, Python is not on PATH — reinstall on Windows with the PATH checkbox, or ask in chat: “stuck on ONBOARDING step 4”.

### Test: did PDF generation work?

The folder [applications/_example-do-not-track/](applications/_example-do-not-track/) contains a sample `cv.md`.

**Mac / Linux:**

```bash
python3 generate_cv_unified.py applications/_example-do-not-track
```

**Windows:**

```bat
py -3 generate_cv_unified.py applications/_example-do-not-track
```

You should get `Your_Name_CV.pdf` (rename later in the script).

**Font error?** On Windows, standard fonts usually work. If not, in PowerShell:

```powershell
$env:JOB_FINDER_FONT_DIR = 'C:\Windows\Fonts'
```

Then run the command again.

---

## Step 5. First chat with the helper

### 5.1 Open chat

- Use **Agent** mode (not Ask) — Agent can edit files.
- **Mac:** Cmd+L · **Windows:** Ctrl+L

### 5.2 What is `@AGENTS.md`?

Type **`@`** and start typing `AGENTS` — Cursor attaches the file. That way the helper **definitely** reads your rules.

### 5.3 First message (copy and customize)

```
@AGENTS.md @cv-base-en.md
Read the rules and my resume.
I'm looking for [your role, e.g. Project Manager], [remote / location].
Add 10 matching active vacancies to tracker.md with working links.
```

Wait. The helper fills [tracker.md](tracker.md). Open it and review the table.

### 5.4 Second message

When you pick vacancy numbers:

```
@AGENTS.md
Prepare cover for vacancy #1.
```

Read `applications/.../cover.md`. Not happy? Say: “shorter”, “less formal”, “mention my Jira experience”.

### hh.ru vs other sites

| Site | What the helper creates |
|------|-------------------------|
| **hh.ru** | Letter (`cover.md`) + notes; resume stays on hh from `cv-base-ru` |
| **Other** | Letter + tailored `cv.md` → you review → PDF command |

The `_example-do-not-track` folder is a **toy example** — do not add it to the tracker.

---

## You are done when…

- [ ] Folder open in Cursor, files visible on the left
- [ ] User preferences filled in `AGENTS.md`
- [ ] `cv-base-en` (and `cv-base-ru` if needed) contain your text, not placeholders
- [ ] Helper added rows to `tracker.md`
- [ ] (If you need PDF) step 4 command created a `.pdf`

---

## Daily routine

1. Check [tracker.md](tracker.md).
2. Tell the helper vacancy numbers.
3. Edit drafts until they sound like you.
4. **You** click apply on the employer site.
5. Set status to `applied` after you submit.

Keep the folder in a **private** cloud backup or git; never store passwords in files.

**Stuck?** Ask in chat: `@AGENTS.md Help with ONBOARDING step … — here's what I see: …`

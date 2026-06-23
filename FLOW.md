# Job Finder Kit — workflow diagrams

Mermaid blocks render in Cursor and on GitHub.

**Image for screenshots / messengers:** open [flow-diagram.svg](flow-diagram.svg) in a browser (double-click). Regenerate: `python3 generate_flow_diagram.py`

---

## 1. First-time setup (once)

```mermaid
flowchart TD
  start([Get folder / clone / zip]) --> unzip[Unzip if needed]
  unzip --> cursor[Install Cursor · cursor.com]
  cursor --> open[File → Open Folder · this folder]
  open --> agents[Fill AGENTS.md · what you are looking for]
  agents --> cv[Fill cv-base-en / cv-base-ru]
  cv --> py{Need PDF?}
  py -->|Yes| python[Python + ONBOARDING step 4]
  py -->|No / hh only| chat
  python --> chat[First chat · @AGENTS.md]
  chat --> ready([Ready to search])
```

---

## 2. Each application (main loop)

```mermaid
flowchart TD
  a([Start]) --> find[Helper adds vacancies to tracker.md]
  find --> pick[You pick numbers · e.g. #3 #7]
  pick --> draft[Helper writes drafts in applications/]
  draft --> read[You read cover.md and cv.md if needed]
  read --> ok{Looks good?}
  ok -->|No| fix[Ask for edits in chat]
  fix --> read
  ok -->|Yes| platform{Where to apply?}
  platform -->|hh.ru| hh[Resume on hh · send with cover]
  platform -->|Other site| pdf{Need PDF?}
  pdf -->|Yes| gen[generate_cv_unified.py]
  pdf -->|No| apply[Apply on site / email]
  gen --> apply
  hh --> done[Status applied in tracker]
  apply --> done
  done --> a
```

---

## 3. Folder layout (non-hh)

```mermaid
flowchart LR
  subgraph tracker [tracker.md]
    T[Table #1 #2 …]
  end
  subgraph app [applications/company-role/]
    V[vacancy.md · notes]
    C[cover.md · letter]
    CV[cv.md · tailored resume]
    P[PDF · if generated]
  end
  T --> app
  CV --> P
```

---

## 4. hh.ru — shorter path

```mermaid
flowchart LR
  T[tracker] --> C[cover.md]
  B[cv-base-ru on hh site] --> H[Apply on hh.ru]
  C --> H
```

---

More detail: [ONBOARDING.md](ONBOARDING.md) · [README.md](README.md)

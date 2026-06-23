# Cursor — quick start / Быстрый старт

**Start here:** [ONBOARDING.md](ONBOARDING.md) (15 min checklist).

## English

1. **Install [Cursor](https://cursor.com)** and sign in.
2. **Open this folder as the project root:** File → Open Folder → the folder that contains `README.md` and `AGENTS.md` (after unzip if needed). You can rename the folder.
3. **Fill [AGENTS.md](AGENTS.md) → User preferences** and [generate_cv_unified.py](generate_cv_unified.py) (`PDF_FILENAME`, `URL_FRAGMENTS`).
4. **Fill [cv-base-en.md](cv-base-en.md)** (and [cv-base-ru.md](cv-base-ru.md) if you use hh.ru).
5. **Agent chat:** **Cmd+L** (macOS) or **Ctrl+L** (Windows/Linux). Use **Agent** mode, not Ask.
6. **Rules context:** Cursor may load `AGENTS.md` automatically, but this is unreliable — **include `@AGENTS.md` in your first message**.
7. **Do not search for vacancies** until User preferences and cv-base are filled (see ONBOARDING).

**First prompts:**

```
@AGENTS.md @cv-base-en.md Read the rules. I'm looking for [role], [remote/location]. Add 10 active vacancies to tracker.md with verified links.
```

```
@AGENTS.md Prepare cover for vacancy #1.
```

```
@AGENTS.md Generate PDF for applications/company-role
```
(after `cv.md` is approved; non-hh only)

**hh.ru example:**

```
@AGENTS.md Vacancy #3 is hh.ru — cover only, no cv.md or PDF.
```

Keep Markdown in a private git backup; do not commit secrets.

---

## Русский

1. **Установите [Cursor](https://cursor.com)** и войдите в аккаунт.
2. **Откройте эту папку как корень проекта:** File → Open Folder → папку, где лежат `README.md` и `AGENTS.md` (после распаковки архива — если был zip). Папку можно переименовать.
3. **Заполните [AGENTS.md](AGENTS.md) → User preferences** и [generate_cv_unified.py](generate_cv_unified.py).
4. **Заполните [cv-base-en.md](cv-base-en.md)** (и [cv-base-ru.md](cv-base-ru.md) для hh.ru).
5. **Чат с агентом:** **Cmd+L** (macOS) или **Ctrl+L** (Windows/Linux), режим **Agent**.
6. **Контекст правил:** надёжнее всего писать **`@AGENTS.md`** в первом сообщении (автозагрузка в Cursor бывает нестабильной).
7. К поиску вакансий — только после заполнения User preferences и cv-base ([ONBOARDING.md](ONBOARDING.md)).

**Примеры первых запросов:**

```
@AGENTS.md @cv-base-en.md Прочитай правила. Ищу [роль], [remote/локация]. Добавь 10 активных вакансий в tracker.md с проверенными ссылками.
```

```
@AGENTS.md Сделай cover для вакансии #1.
```

```
@AGENTS.md Сгенерируй PDF для applications/company-role
```
(после approve `cv.md`; не для hh.ru)

**Windows:** распаковка через Проводник нормальна; Python — `py -3`, venv — см. ONBOARDING. WSL не обязателен. По возможности без кириллицы в полном пути к папке проекта.

Храните файлы в приватном репозитории или бэкапе; секреты в репозиторий не кладите.

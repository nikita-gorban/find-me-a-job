# Схема работы Job Finder Kit

Ниже — блок-схемы на русском. В Cursor и на GitHub они рисуются автоматически из текста.

**Картинка для скрина / мессенджера:** откройте [flow-diagram.svg](flow-diagram.svg) в Safari или Chrome (двойной клик). В редакторе кириллица может выглядеть как `&#1082;` — в браузере отображается нормально. Пересобрать: `python3 generate_flow_diagram.py`

---

## 1. Первый запуск (один раз)

```mermaid
flowchart TD
  start([Получили папку / zip]) --> unzip[Распаковать]
  unzip --> cursor[Установить Cursor · cursor.com]
  cursor --> open[File → Open Folder · эта папка]
  open --> agents[Заполнить AGENTS.md · кого ищете]
  agents --> cv[Заполнить cv-base-en / cv-base-ru]
  cv --> py{Нужен PDF?}
  py -->|Да| python[Python + ONBOARDING шаг 4]
  py -->|Нет только hh| chat
  python --> chat[Первый чат · @AGENTS.md]
  chat --> ready([Можно искать вакансии])
```

---

## 2. Каждый отклик (основной цикл)

```mermaid
flowchart TD
  a([Начало]) --> find[Помощник добавляет вакансии в tracker.md]
  find --> pick[Вы выбираете номера · например #3 #7]
  pick --> draft[Помощник пишет черновики в applications/]
  draft --> read[Вы читаете cover.md и при необходимости cv.md]
  read --> ok{Всё верно?}
  ok -->|Нет| fix[Просите поправить в чате]
  fix --> read
  ok -->|Да| platform{Где отклик?}
  platform -->|hh.ru| hh[Копируете резюме на hh · отправляете с cover]
  platform -->|Другой сайт| pdf{Нужен PDF?}
  pdf -->|Да| gen[Команда generate_cv_unified.py]
  pdf -->|Нет| apply[Отклик на сайте / email]
  gen --> apply
  hh --> done[Статус applied в tracker]
  apply --> done
  done --> a
```

---

## 3. Что в какой папке (не hh)

```mermaid
flowchart LR
  subgraph tracker [tracker.md]
    T[Таблица вакансий №1 №2 …]
  end
  subgraph app [applications/компания-роль/]
    V[vacancy.md · заметки]
    C[cover.md · письмо]
    CV[cv.md · резюме под вакансию]
    P[PDF · если собрали]
  end
  T --> app
  CV --> P
```

---

## 4. hh.ru — короче

```mermaid
flowchart LR
  T[tracker] --> C[cover.md]
  B[cv-base-ru.md на сайте hh] --> H[Отклик на hh.ru]
  C --> H
```

---

Подробные шаги: [ONBOARDING.md](ONBOARDING.md) · [README.ru.md](README.ru.md)

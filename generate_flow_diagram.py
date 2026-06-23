#!/usr/bin/env python3
"""Regenerate flow-diagram.svg with safe XML entities for Cyrillic (Safari-compatible)."""

from pathlib import Path


def ent(s: str) -> str:
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)


def main() -> None:
    labels = [
        ("title", 460, 36, "title", "Job Finder Kit - как это работает"),
        ("subtitle", 460, 58, "subtitle", "Папка + Cursor + помощник (ИИ). Вы проверяете и сами откликаетесь."),
        ("text-sm", 64, 92, "text-sm", "Помощник в Cursor"),
        ("text-sm", 224, 92, "text-sm", "Вы"),
        ("text-sm", 304, 92, "text-sm", "Файлы / программа"),
        ("section", 40, 128, "section", "А. Первый запуск (один раз)"),
        ("text", 460, 162, "text", "Распаковать папку, установить Cursor"),
        ("text-sm", 460, 178, "text-sm", "File - Open Folder - эта папка"),
        ("text", 460, 240, "text", "Заполнить AGENTS.md и cv-base (ваше резюме)"),
        ("text", 460, 308, "text", "Нужен PDF?"),
        ("text-sm", 290, 300, "text-sm", "да"),
        ("text-sm", 140, 314, "text-sm", "Python, ONBOARDING шаг 4"),
        ("text-sm", 610, 300, "text-sm", "нет / только hh"),
        ("text", 460, 380, "text", "Первый чат: @AGENTS.md - добавить вакансии в tracker"),
        ("text-sm", 460, 396, "text-sm", "Режим Agent, Cmd+L / Ctrl+L"),
        ("section", 40, 448, "section", "Б. Каждый день / каждый отклик"),
        ("text", 460, 488, "text", "Вакансии в tracker.md (таблица с номерами)"),
        ("text", 460, 556, "text", "Вы: нравится номер 3 и 7"),
        ("text", 460, 620, "text", "Помощник: папка applications/компания-роль/"),
        ("text-sm", 460, 638, "text-sm", "vacancy.md, cover.md, cv.md (если не hh)"),
        ("text", 460, 704, "text", "Вы читаете, правите, говорите OK"),
        ("text", 460, 778, "text", "Где отклик?"),
        ("text-sm", 265, 770, "text-sm", "hh.ru"),
        ("text-sm", 140, 778, "text-sm", "cover.md + резюме"),
        ("text-sm", 140, 794, "text-sm", "на hh (cv-base-ru)"),
        ("text-sm", 655, 770, "text-sm", "другой сайт"),
        ("text-sm", 760, 772, "text-sm", "cv.md, при необходимости"),
        ("text-sm", 760, 788, "text-sm", "PDF (generate_cv_unified.py)"),
        ("text", 460, 900, "text", "Вы сами откликаетесь на сайте"),
        ("text", 460, 968, "text", "В tracker: статус applied"),
        ("text", 460, 1024, "text", "Главные файлы"),
        ("text-sm", 460, 1044, "text-sm", "tracker.md - список; AGENTS.md - правила; cv-base - резюме; applications/ - черновики"),
        ("text-sm", 460, 1062, "text-sm", "Подробно: ONBOARDING.md, README.ru.md"),
        ("subtitle", 460, 1148, "subtitle", "job-finder-kit / flow-diagram.svg"),
    ]

    text_els = []
    for _id, x, y, klass, s in labels:
        anchor = ' text-anchor="middle"' if x > 100 else ""
        fw = ' font-weight="bold"' if s == "Главные файлы" else ""
        text_els.append(f'  <text x="{x}" y="{y}"{anchor} class="{klass}"{fw}>{ent(s)}</text>')

    shapes = """
  <rect x="40" y="78" width="18" height="18" class="legend-ai" rx="3"/>
  <rect x="200" y="78" width="18" height="18" class="legend-you" rx="3"/>
  <rect x="280" y="78" width="18" height="18" class="legend-sys" rx="3"/>
  <rect x="300" y="142" width="320" height="44" class="box-start" rx="8"/>
  <line x1="460" y1="186" x2="460" y2="212" class="line"/>
  <rect x="260" y="214" width="400" height="40" class="box-you" rx="8"/>
  <line x1="460" y1="254" x2="460" y2="280" class="line"/>
  <polygon points="460,282 520,322 400,322" class="box-decision"/>
  <line x1="400" y1="308" x2="180" y2="308" class="line"/>
  <rect x="40" y="288" width="200" height="40" class="box-sys" rx="8"/>
  <line x1="520" y1="308" x2="700" y2="308" class="line"/>
  <line x1="460" y1="322" x2="460" y2="358" class="line"/>
  <rect x="220" y="360" width="480" height="44" class="box-ai" rx="8"/>
  <rect x="300" y="462" width="320" height="40" class="box-ai" rx="8"/>
  <line x1="460" y1="502" x2="460" y2="528" class="line"/>
  <rect x="280" y="530" width="360" height="40" class="box-you" rx="8"/>
  <line x1="460" y1="570" x2="460" y2="596" class="line"/>
  <rect x="200" y="598" width="520" height="52" class="box-ai" rx="8"/>
  <line x1="460" y1="650" x2="460" y2="676" class="line"/>
  <rect x="260" y="678" width="400" height="40" class="box-you" rx="8"/>
  <line x1="460" y1="718" x2="460" y2="744" class="line"/>
  <polygon points="460,746 530,796 390,796" class="box-decision"/>
  <line x1="390" y1="778" x2="140" y2="778" class="line"/>
  <rect x="40" y="756" width="200" height="56" class="box-sys" rx="8"/>
  <line x1="530" y1="778" x2="780" y2="778" class="line"/>
  <rect x="640" y="748" width="240" height="60" class="box-sys" rx="8"/>
  <line x1="140" y1="812" x2="140" y2="848" class="line"/>
  <line x1="760" y1="808" x2="760" y2="848" class="line"/>
  <line x1="140" y1="848" x2="760" y2="848" class="line"/>
  <line x1="460" y1="848" x2="460" y2="872" class="line"/>
  <rect x="280" y="874" width="360" height="40" class="box-you" rx="8"/>
  <line x1="460" y1="914" x2="460" y2="940" class="line"/>
  <rect x="300" y="942" width="320" height="40" class="box-end" rx="8"/>
  <rect x="40" y="1000" width="840" height="72" class="box-sys" rx="8"/>
"""

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 1180">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L9,3 L0,6 Z" fill="#334155"/>
    </marker>
    <style type="text/css"><![CDATA[
      .title {{ font: 700 22px -apple-system, BlinkMacSystemFont, Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 14px -apple-system, BlinkMacSystemFont, Arial, sans-serif; fill: #64748b; }}
      .section {{ font: 700 16px -apple-system, BlinkMacSystemFont, Arial, sans-serif; fill: #1e40af; }}
      .box-start {{ fill: #dbeafe; stroke: #2563eb; stroke-width: 2; }}
      .box-end {{ fill: #dcfce7; stroke: #16a34a; stroke-width: 2; }}
      .box-you {{ fill: #fef3c7; stroke: #d97706; stroke-width: 2; }}
      .box-ai {{ fill: #ede9fe; stroke: #7c3aed; stroke-width: 2; }}
      .box-sys {{ fill: #f8fafc; stroke: #334155; stroke-width: 2; }}
      .box-decision {{ fill: #ffffff; stroke: #64748b; stroke-width: 2; }}
      .text {{ font: 13px -apple-system, BlinkMacSystemFont, Arial, sans-serif; fill: #0f172a; }}
      .text-sm {{ font: 11px -apple-system, BlinkMacSystemFont, Arial, sans-serif; fill: #475569; }}
      .line {{ stroke: #334155; stroke-width: 2; fill: none; marker-end: url(#arrow); }}
      .legend-ai {{ fill: #ede9fe; stroke: #7c3aed; }}
      .legend-you {{ fill: #fef3c7; stroke: #d97706; }}
      .legend-sys {{ fill: #f8fafc; stroke: #334155; }}
    ]]></style>
  </defs>

{chr(10).join(text_els)}
{shapes}
</svg>
'''

    out = Path(__file__).parent / "flow-diagram.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

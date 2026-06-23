"""
Unified CV PDF generator.

Usage (macOS / Linux):
    python3 generate_cv_unified.py applications/company-role

Usage (Windows):
    py -3 generate_cv_unified.py applications/company-role

Reads:  <folder>/cv.md
Writes: <folder>/<PDF_FILENAME>  (see USER SETTINGS below)

Fonts (auto-detected): macOS Supplemental Arial; Windows %WINDIR%\\Fonts;
  Linux Liberation/DejaVu. Override: JOB_FINDER_FONT_DIR environment variable.

The script parses the structured cv.md format and renders a 1-page A4 PDF
with clickable links. Font size is auto-tuned to fit exactly one page.

cv.md expected structure
------------------------
Line 1:  Full name
Line 2:  Role / subtitle
Line 3:  Location · [Telegram](...) · [email](...) · [site](...)

## Summary
<paragraph>

## Experience

### <Role> — [Company](url)
<year range>

<tagline>

- bullet
- bullet

(repeat for each job)

## Skills
- **Category**: text

## Tools
<comma list>

## Languages
<lines>

## Education
<line>
"""

import io
import os
import platform
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

import fitz  # PyMuPDF

# ── User settings (edit before first PDF) ─────────────────────────────────────
PDF_FILENAME = "Your_Name_CV.pdf"
URL_FRAGMENTS = [
    "t.me/your_username",
    "mailto:",
    "example.com",
]

# ── Fonts (macOS / Linux / Windows) ───────────────────────────────────────────
def _build_font_candidates() -> list[tuple[Path, dict[str, str]]]:
    candidates: list[tuple[Path, dict[str, str]]] = []
    env_dir = os.environ.get("JOB_FINDER_FONT_DIR")
    if env_dir:
        custom = Path(env_dir)
        for file_map in (
            _MACOS_FONT_FILES,
            _WINDOWS_FONT_FILES,
            _LIBERATION_FONT_FILES,
            _DEJAVU_FONT_FILES,
        ):
            candidates.append((custom, file_map))

    system = platform.system()
    if system == "Darwin":
        candidates.append(
            (Path("/System/Library/Fonts/Supplemental"), _MACOS_FONT_FILES)
        )
    elif system == "Windows":
        windir = os.environ.get("WINDIR", r"C:\Windows")
        candidates.append((Path(windir) / "Fonts", _WINDOWS_FONT_FILES))
    else:
        candidates.extend(
            [
                (
                    Path("/usr/share/fonts/truetype/liberation"),
                    _LIBERATION_FONT_FILES,
                ),
                (
                    Path("/usr/share/fonts/truetype/dejavu"),
                    _DEJAVU_FONT_FILES,
                ),
            ]
        )
    return candidates


_MACOS_FONT_FILES = {
    "Arial": "Arial.ttf",
    "Arial-Bold": "Arial Bold.ttf",
    "Arial-Italic": "Arial Italic.ttf",
    "Arial-BoldItalic": "Arial Bold Italic.ttf",
}

_WINDOWS_FONT_FILES = {
    "Arial": "arial.ttf",
    "Arial-Bold": "arialbd.ttf",
    "Arial-Italic": "ariali.ttf",
    "Arial-BoldItalic": "arialbi.ttf",
}

_LIBERATION_FONT_FILES = {
    "Arial": "LiberationSans-Regular.ttf",
    "Arial-Bold": "LiberationSans-Bold.ttf",
    "Arial-Italic": "LiberationSans-Italic.ttf",
    "Arial-BoldItalic": "LiberationSans-BoldItalic.ttf",
}

_DEJAVU_FONT_FILES = {
    "Arial": "DejaVuSans.ttf",
    "Arial-Bold": "DejaVuSans-Bold.ttf",
    "Arial-Italic": "DejaVuSans-Oblique.ttf",
    "Arial-BoldItalic": "DejaVuSans-BoldOblique.ttf",
}


def _register_from_dir(font_dir: Path, files: dict[str, str]) -> bool:
    if not font_dir.is_dir():
        return False
    paths = {name: font_dir / fname for name, fname in files.items()}
    missing = [str(p) for p in paths.values() if not p.is_file()]
    if missing:
        return False
    for logical_name, path in paths.items():
        pdfmetrics.registerFont(TTFont(logical_name, str(path)))
    registerFontFamily(
        "Arial",
        normal="Arial",
        bold="Arial-Bold",
        italic="Arial-Italic",
        boldItalic="Arial-BoldItalic",
    )
    return True


def register_fonts() -> Path:
    """Register Arial (or equivalent) for PDF rendering. Exits on failure."""
    tried: list[str] = []
    for font_dir, file_map in _build_font_candidates():
        tried.append(str(font_dir))
        if _register_from_dir(font_dir, file_map):
            return font_dir
    system = platform.system()
    hint = (
        "Set JOB_FINDER_FONT_DIR to a folder containing Arial .ttf files.\n"
        "  macOS: /System/Library/Fonts/Supplemental\n"
        "  Windows: C:\\Windows\\Fonts (arial.ttf, arialbd.ttf, …)\n"
        "  Linux: /usr/share/fonts/truetype/liberation or dejavu\n"
        "  PowerShell: $env:JOB_FINDER_FONT_DIR = 'C:\\Windows\\Fonts'"
    )
    if system == "Windows":
        hint += "\n  Install Python from python.org with 'Add python.exe to PATH'."
    print("Error: could not load fonts. Tried:\n  " + "\n  ".join(tried), file=sys.stderr)
    print(hint, file=sys.stderr)
    sys.exit(1)


FONT_DIR = register_fonts()

LINK_COLOR = "#1155cc"
W, H = A4


# ── Markdown link → reportlab link ────────────────────────────────────────────
def md_links_to_rl(text: str) -> str:
    """Convert [label](url) to reportlab <link> tags."""
    def _replace(m):
        label, url = m.group(1), m.group(2)
        return f'<link href="{url}"><font color="{LINK_COLOR}">{label}</font></link>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', _replace, text)


def escape_xml(text: str) -> str:
    """Escape & < > but preserve already-converted <link> and <font> tags."""
    # We convert md links first, then escape bare & and < > that aren't tags
    text = text.replace("&", "&amp;")
    # Un-escape our already-inserted tags
    text = text.replace("&amp;lt;", "<").replace("&amp;gt;", ">")
    return text


def process_inline(text: str) -> str:
    """Convert markdown inline formatting to reportlab XML."""
    text = md_links_to_rl(text)
    # Bold: **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # Escape bare & that aren't already part of an entity
    text = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#)', '&amp;', text)
    return text


# ── cv.md parser ──────────────────────────────────────────────────────────────
def parse_cv(md_path: Path) -> dict:
    lines = md_path.read_text(encoding="utf-8").splitlines()

    cv = {
        "name": "",
        "role": "",
        "contacts": "",
        "summary": "",
        "experience": [],   # list of {title, url, years, tagline, bullets}
        "skills": [],       # list of raw strings
        "tools": "",
        "languages": [],
        "education": "",
        "lang": "en",       # "en" or "ru" — detected from section headers
    }

    i = 0
    total = len(lines)

    def peek(n=0):
        idx = i + n
        return lines[idx].strip() if idx < total else ""

    # Header: first 3 non-empty lines
    header_lines = []
    while i < total and len(header_lines) < 3:
        line = lines[i].strip()
        if line:
            header_lines.append(line)
        i += 1
    if len(header_lines) >= 1:
        cv["name"] = header_lines[0]
    if len(header_lines) >= 2:
        cv["role"] = header_lines[1]
    if len(header_lines) >= 3:
        cv["contacts"] = header_lines[2]

    current_section = None
    current_job = None
    in_job_bullets = False
    collecting_body = []

    while i < total:
        line = lines[i]
        stripped = line.strip()

        # Section headers (## )
        if stripped.startswith("## "):
            # flush previous body
            if current_section == "summary" and collecting_body:
                cv["summary"] = " ".join(collecting_body).strip()
                collecting_body = []
            elif current_section == "tools" and collecting_body:
                cv["tools"] = " ".join(collecting_body).strip()
                collecting_body = []
            elif current_section == "education" and collecting_body:
                cv["education"] = " ".join(collecting_body).strip()
                collecting_body = []

            if current_job:
                cv["experience"].append(current_job)
                current_job = None
                in_job_bullets = False

            section_name = stripped[3:].strip().lower()
            _ru_map = {
                "о себе": "summary", "обо мне": "summary",
                "опыт": "experience", "опыт работы": "experience",
                "навыки": "skills",
                "инструменты": "tools",
                "языки": "languages",
                "образование": "education",
            }
            if section_name in _ru_map:
                cv["lang"] = "ru"
            section_name = _ru_map.get(section_name, section_name)
            current_section = section_name
            i += 1
            continue

        # Job headers (### )
        if stripped.startswith("### ") and current_section == "experience":
            if current_job:
                cv["experience"].append(current_job)

            job_header = stripped[4:].strip()
            # Parse "Role — [Company](url)" or "Role — Company"
            url_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', job_header)
            company_url = url_match.group(2) if url_match else ""
            company_name = url_match.group(1) if url_match else ""
            # Role is everything before " — "
            em_dash_variants = [" — ", " -- ", " - "]
            role_part = job_header
            for sep in em_dash_variants:
                if sep in job_header:
                    role_part = job_header.split(sep)[0].strip()
                    break

            current_job = {
                "role": role_part,
                "company": company_name,
                "company_url": company_url,
                "years": "",
                "tagline": "",
                "bullets": [],
            }
            in_job_bullets = False
            i += 1
            continue

        # Inside a job block
        if current_job is not None:
            if stripped and not current_job["years"] and re.match(r'^\d{4}', stripped):
                current_job["years"] = stripped
                i += 1
                continue
            if stripped.startswith("- ") or stripped.startswith("* "):
                current_job["bullets"].append(stripped[2:].strip())
                in_job_bullets = True
                i += 1
                continue
            if stripped and not in_job_bullets and not current_job["tagline"]:
                current_job["tagline"] = stripped
                i += 1
                continue

        # Skills bullets
        if current_section == "skills":
            if stripped.startswith("- "):
                cv["skills"].append(stripped[2:].strip())
            i += 1
            continue

        # Languages
        if current_section == "languages":
            if stripped:
                cv["languages"].append(stripped)
            i += 1
            continue

        # Body sections (summary, tools, education)
        if current_section in ("summary", "tools", "education"):
            if stripped:
                collecting_body.append(stripped)
            i += 1
            continue

        i += 1

    # Flush last job
    if current_job:
        cv["experience"].append(current_job)

    # Flush last body section
    if current_section == "summary" and collecting_body:
        cv["summary"] = " ".join(collecting_body).strip()
    elif current_section == "tools" and collecting_body:
        cv["tools"] = " ".join(collecting_body).strip()
    elif current_section == "education" and collecting_body:
        cv["education"] = " ".join(collecting_body).strip()

    return cv


# ── Story builder ─────────────────────────────────────────────────────────────
def build_story(cv: dict, base: float, section_space: float, leading_ratio: float):
    ru = cv.get("lang") == "ru"
    _sec = {
        "summary":    "О себе"      if ru else "Summary",
        "experience": "Опыт работы" if ru else "Experience",
        "skills":     "Навыки"      if ru else "Skills",
        "tools":      "Инструменты" if ru else "Tools",
        "languages":  "Языки"       if ru else "Languages",
        "education":  "Образование" if ru else "Education",
    }
    def style(name, **kw):
        d = dict(
            fontName="Arial",
            fontSize=base,
            leading=base * leading_ratio,
            textColor=colors.HexColor("#333333"),
            alignment=TA_LEFT,
        )
        d.update(kw)
        return ParagraphStyle(name, **d)

    s_name     = style("Name",     fontName="Arial-Bold",   fontSize=base*1.75, leading=base*2.1,  spaceAfter=1)
    s_role     = style("Role",     fontSize=base*1.05,      leading=base*1.3,   spaceAfter=2,      textColor=colors.HexColor("#555555"))
    s_contacts = style("Contacts", fontSize=base*0.93,      leading=base*1.25,  spaceAfter=5)
    s_section  = style("Section",  fontName="Arial-Bold",   fontSize=base*1.02, leading=base*1.3,  spaceBefore=section_space, spaceAfter=2, textColor=colors.HexColor("#1a1a1a"))
    s_job      = style("Job",      fontName="Arial-Bold",   fontSize=base,      leading=base*1.3,  spaceBefore=4, spaceAfter=1)
    s_sub      = style("Sub",      fontName="Arial-Italic", fontSize=base*0.92, leading=base*1.2,  spaceAfter=2, textColor=colors.HexColor("#666666"))
    s_body     = style("Body",     fontSize=base,           leading=base*1.3,   spaceAfter=1)
    s_bullet   = style("Bullet",   fontSize=base,           leading=base*leading_ratio, spaceAfter=1, leftIndent=10)

    story = []

    # Header
    story.append(Paragraph(process_inline(cv["name"]), s_name))
    story.append(Paragraph(process_inline(cv["role"]), s_role))
    story.append(Paragraph(process_inline(cv["contacts"]), s_contacts))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#bbbbbb"), spaceBefore=0, spaceAfter=4))

    # Summary
    if cv["summary"]:
        story.append(Paragraph(_sec["summary"], s_section))
        story.append(Paragraph(process_inline(cv["summary"]), s_body))

    # Experience
    if cv["experience"]:
        story.append(Paragraph(_sec["experience"], s_section))
        for job in cv["experience"]:
            company_part = (
                f'<link href="{job["company_url"]}"><font color="{LINK_COLOR}">{job["company"]}</font></link>'
                if job["company_url"] else job["company"]
            )
            title_line = f'{job["role"]} — {company_part}  ·  {job["years"]}'
            story.append(Paragraph(title_line, s_job))
            if job["tagline"]:
                story.append(Paragraph(process_inline(job["tagline"]), s_sub))
            for b in job["bullets"]:
                story.append(Paragraph(f"• {process_inline(b)}", s_bullet))

    # Skills
    if cv["skills"]:
        story.append(Paragraph(_sec["skills"], s_section))
        for sk in cv["skills"]:
            story.append(Paragraph(f"• {process_inline(sk)}", s_bullet))

    # Tools
    if cv["tools"]:
        story.append(Paragraph(_sec["tools"], s_section))
        story.append(Paragraph(process_inline(cv["tools"]), s_body))

    # Languages
    if cv["languages"]:
        story.append(Paragraph(_sec["languages"], s_section))
        story.append(Paragraph("  ·  ".join(cv["languages"]), s_body))

    # Education
    if cv["education"]:
        story.append(Paragraph(_sec["education"], s_section))
        story.append(Paragraph(process_inline(cv["education"]), s_body))

    return story


# ── Build + verify ─────────────────────────────────────────────────────────────
def try_build(cv: dict, margin: float, base: float, sec_sp: float, lead_r: float) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=margin, rightMargin=margin,
                            topMargin=margin, bottomMargin=margin)
    doc.build(build_story(cv, base, sec_sp, lead_r))
    return buf.getvalue()


def check(pdf_bytes: bytes, margin: float, required_urls: list[str]) -> dict:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    r = {"pages": doc.page_count, "pages_ok": doc.page_count == 1}
    if doc.page_count >= 1:
        page = doc[0]
        pw, ph = page.rect.width, page.rect.height
        blocks = page.get_text("blocks")
        if blocks:
            xs = [b[0] for b in blocks] + [b[2] for b in blocks]
            ys = [b[1] for b in blocks] + [b[3] for b in blocks]
            r["left_margin"]   = round(min(xs))
            r["right_margin"]  = round(pw - max(xs))
            r["top_margin"]    = round(min(ys))
            r["bottom_margin"] = round(ph - max(ys))
            thr = margin * 0.6
            r["margins_ok"] = (min(xs) >= thr and max(xs) <= pw - thr
                               and min(ys) >= thr and max(ys) <= ph - thr)
        else:
            r["margins_ok"] = True
        links = page.get_links()
        uris = [lk.get("uri", "") for lk in links if lk.get("uri")]
        r["link_count"] = len(uris)
        r["links_ok"] = all(any(req in u for u in uris) for req in required_urls)
    doc.close()
    return r


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_cv_unified.py <application-folder>")
        print("       py -3 generate_cv_unified.py <application-folder>   (Windows)")
        print("  e.g. python3 generate_cv_unified.py applications/acme-pm")
        sys.exit(1)

    folder = Path(sys.argv[1])
    if not folder.is_absolute():
        # Resolve relative to this script's directory
        folder = Path(__file__).parent / folder

    cv_md = folder / "cv.md"
    if not cv_md.exists():
        print(f"Error: {cv_md} not found")
        sys.exit(1)

    output_pdf = folder / PDF_FILENAME

    print(f"Parsing: {cv_md}")
    cv = parse_cv(cv_md)

    # Collect URLs to verify from the cv
    url_fragments = list(URL_FRAGMENTS)
    for job in cv["experience"]:
        if job["company_url"]:
            # Use a short fragment of the URL
            domain = re.sub(r'https?://(www\.)?', '', job["company_url"]).rstrip('/').split('/')[0]
            if domain:
                url_fragments.append(domain)

    MARGIN = 40
    configs = [
        (9.0, 5, 1.20),
        (8.8, 4, 1.18),
        (8.5, 4, 1.18),
        (8.5, 3, 1.16),
        (8.2, 3, 1.16),
        (8.0, 3, 1.15),
        (7.8, 3, 1.15),
        (7.5, 2, 1.14),
    ]

    chosen = None
    for base, sec_sp, lead_r in configs:
        pdf_bytes = try_build(cv, MARGIN, base, sec_sp, lead_r)
        req = check(pdf_bytes, MARGIN, url_fragments)
        status = "✓" if req["pages_ok"] else f"✗ ({req['pages']}p)"
        print(
            f"  base={base:4.1f}pt  sec={sec_sp}pt  lead={lead_r}  →  "
            f"pages={status}  "
            f"L={req.get('left_margin','?')}  R={req.get('right_margin','?')}  "
            f"T={req.get('top_margin','?')}  B={req.get('bottom_margin','?')}  "
            f"links={req.get('link_count','?')}{'✓' if req.get('links_ok') else '✗'}"
        )
        if req.get("pages_ok") and req.get("margins_ok") and req.get("links_ok"):
            chosen = (base, sec_sp, lead_r, pdf_bytes, req)
            break

    if chosen is None:
        print("\n❌  No config fit — content may be too long for one page.")
        sys.exit(1)

    base, sec_sp, lead_r, pdf_bytes, req = chosen
    output_pdf.write_bytes(pdf_bytes)

    print(f"\n✅  Saved: {output_pdf}")
    print(f"   font={base}pt  section_space={sec_sp}pt  leading={lead_r}  margin={MARGIN}pt")
    print(f"   pages={req['pages']}  margins L/R/T/B: "
          f"{req['left_margin']}/{req['right_margin']}/{req['top_margin']}/{req['bottom_margin']}pt")
    print(f"   links: {req['link_count']} found  ok={req['links_ok']}")


if __name__ == "__main__":
    main()

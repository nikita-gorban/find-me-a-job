"""
Unified CV PDF generator.

Usage (macOS / Linux):
    python3 generate_cv_unified.py applications/5-acme-pm
    python3 generate_cv_unified.py --allow-terminal-status applications/5-acme-pm

Usage (Windows):
    py -3 generate_cv_unified.py applications/5-acme-pm

Reads:  <folder>/<num>-cv.md (strict for numbered application folders)
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

import argparse
import hashlib
import io
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

from pdf_common import LINK_COLOR, make_style, process_inline, resolve_app_md

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

# ── User settings (edit before first PDF) ─────────────────────────────────────
PDF_FILENAME = "Your_Name_CV.pdf"
URL_FRAGMENTS = [
    "t.me/your_username",
    "mailto:",
    "example.com",
]

W, H = A4


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
        d = dict(fontSize=base, leading=base * leading_ratio)
        d.update(kw)
        return make_style(name, **d)

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
        for raw in cv["languages"]:
            line = re.sub(r'^[-*]\s+', '', raw.strip())
            story.append(Paragraph(process_inline(line), s_body))

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
    """Verify page count, margins, and links. Requires PyMuPDF (fitz)."""
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


def _plain_text(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "").replace("__", "").replace("*", "")
    return re.sub(r"\s+", " ", value).strip()


def _normalise_text(value: str) -> str:
    value = _plain_text(value).replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", value).casefold()


def expected_fragments(cv: dict) -> list[str]:
    """Return source fragments that must survive PDF rendering."""
    fragments = [cv["name"], cv["role"], cv["summary"]]
    for job in cv["experience"]:
        fragments.extend([job["role"], job["company"], job["years"], job["tagline"]])
        fragments.extend(job["bullets"])
    fragments.extend(cv["skills"])
    fragments.extend(cv["languages"])
    fragments.append(cv["education"])
    return [fragment for fragment in fragments if _plain_text(fragment)]


def verify_text(pdf_bytes: bytes, cv: dict) -> tuple[bool, list[str]]:
    """Verify every meaningful Markdown fragment is present in extracted PDF text."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    extracted = "\n".join(page.get_text() for page in doc)
    doc.close()
    haystack = _normalise_text(extracted)
    missing = [
        _plain_text(fragment)
        for fragment in expected_fragments(cv)
        if _normalise_text(fragment) not in haystack
    ]
    return not missing, missing


def tracker_status(folder: Path) -> Optional[str]:
    match = re.match(r"^(\d+)-", folder.name)
    if not match:
        return None
    tracker = Path(__file__).parent / "tracker.md"
    if not tracker.exists():
        return None
    number = match.group(1)
    row_re = re.compile(rf"^\|\s*{re.escape(number)}\s*\|")
    status_re = re.compile(r"`(new|prep|ready|applied|declined|closed|skip)`")
    for line in tracker.read_text(encoding="utf-8").splitlines():
        if row_re.match(line):
            status_match = status_re.search(line)
            return status_match.group(1) if status_match else None
    return None


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate and verify a one-page CV PDF.")
    parser.add_argument("application_folder")
    parser.add_argument(
        "--allow-terminal-status",
        action="store_true",
        help="Allow regeneration for applied/declined applications after explicit user request.",
    )
    args = parser.parse_args()

    folder = Path(args.application_folder)
    if not folder.is_absolute():
        # Resolve relative to this script's directory
        folder = Path(__file__).parent / folder
    folder = folder.resolve()

    try:
        cv_md = resolve_app_md(folder, "cv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    output_pdf = folder / PDF_FILENAME

    status = tracker_status(folder)
    if status in {"applied", "declined"} and not args.allow_terminal_status:
        print(
            f"Error: tracker status is {status!r}; CV/PDF is immutable after submission. "
            "Use --allow-terminal-status only after an explicit user request."
        )
        sys.exit(1)

    source_bytes = cv_md.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    source_mtime_ns = cv_md.stat().st_mtime_ns
    source_mtime = datetime.fromtimestamp(source_mtime_ns / 1_000_000_000).isoformat(
        timespec="seconds"
    )
    print(f"Parsing: {cv_md}")
    print(f"Source: mtime={source_mtime} sha256={source_hash}")
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

    if not HAS_FITZ:
        print("Error: PyMuPDF is required for page, link, and text verification.")
        print("Install it with: python3 -m pip install pymupdf")
        sys.exit(1)

    chosen = None
    for base, sec_sp, lead_r in configs:
        pdf_bytes = try_build(cv, MARGIN, base, sec_sp, lead_r)
        req = check(pdf_bytes, MARGIN, url_fragments)
        text_ok, missing = verify_text(pdf_bytes, cv)
        page_status = "✓" if req["pages_ok"] else f"✗ ({req['pages']}p)"
        print(
            f"  base={base:4.1f}pt  sec={sec_sp}pt  lead={lead_r}  →  "
            f"pages={page_status}  "
            f"L={req.get('left_margin','?')}  R={req.get('right_margin','?')}  "
            f"T={req.get('top_margin','?')}  B={req.get('bottom_margin','?')}  "
            f"links={req.get('link_count','?')}{'✓' if req.get('links_ok') else '✗'}  "
            f"text={'✓' if text_ok else '✗'}"
        )
        if (
            req.get("pages_ok")
            and req.get("margins_ok")
            and req.get("links_ok")
            and text_ok
        ):
            chosen = (base, sec_sp, lead_r, pdf_bytes, req)
            break
        if missing:
            print(f"    missing text: {missing[0][:120]}")

    if chosen is None:
        print("\n❌  No config passed page, margin, link, and text verification.")
        sys.exit(1)

    base, sec_sp, lead_r, pdf_bytes, req = chosen
    if cv_md.stat().st_mtime_ns != source_mtime_ns or hashlib.sha256(cv_md.read_bytes()).hexdigest() != source_hash:
        print("Error: source Markdown changed during generation; save it and retry.")
        sys.exit(1)

    temp_pdf = output_pdf.with_name(f".{output_pdf.name}.tmp")
    try:
        temp_pdf.write_bytes(pdf_bytes)
        os.replace(temp_pdf, output_pdf)
    finally:
        if temp_pdf.exists():
            temp_pdf.unlink()

    if output_pdf.stat().st_mtime_ns < source_mtime_ns:
        print("Error: generated PDF is older than source Markdown.")
        sys.exit(1)

    print(f"\n✅  Saved: {output_pdf}")
    print(f"   font={base}pt  section_space={sec_sp}pt  leading={lead_r}  margin={MARGIN}pt")
    print(f"   pages={req['pages']}  margins L/R/T/B: "
          f"{req['left_margin']}/{req['right_margin']}/{req['top_margin']}/{req['bottom_margin']}pt")
    print(f"   links: {req['link_count']} found  ok={req['links_ok']}")
    print("   text: all source fragments found")
    print(f"   freshness: pdf_mtime >= source_mtime ({output_pdf.stat().st_mtime_ns >= source_mtime_ns})")


if __name__ == "__main__":
    main()

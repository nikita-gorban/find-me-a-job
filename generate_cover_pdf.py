#!/usr/bin/env python3
"""
Cover letter PDF generator.

Usage (macOS / Linux):
    python3 generate_cover_pdf.py applications/company-role

Usage (Windows):
    py -3 generate_cover_pdf.py applications/company-role

Reads:  <folder>/cover.md
Writes: <folder>/<PDF_COVER_FILENAME>  (see USER SETTINGS below)
"""

import io
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

import generate_cv_unified  # registers fonts
from generate_cv_unified import LINK_COLOR

# ── User settings (edit before first PDF) ─────────────────────────────────────
PDF_COVER_FILENAME = "Your_Name_Cover_Letter.pdf"

MARGIN = 50
BASE = 11.0


def md_links_to_rl(text: str) -> str:
    def _replace(m):
        label, url = m.group(1), m.group(2)
        return f'<link href="{url}"><font color="{LINK_COLOR}">{label}</font></link>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _replace, text)


def process_inline(text: str) -> str:
    text = md_links_to_rl(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)", "&amp;", text)
    return text


def parse_cover(md_path: Path) -> dict:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    title = ""
    body_lines = []
    signature_name = "Your Name"
    signature_contacts = "you@email.com"
    phase = "header"

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if stripped == "---":
            phase = "body"
            continue
        if phase == "body":
            if not stripped:
                continue
            if stripped.startswith("**") and stripped.endswith("**"):
                signature_name = stripped.strip("*").strip()
                continue
            if "@" in stripped or "t.me/" in stripped:
                signature_contacts = stripped
                continue
            body_lines.append(stripped)

    return {
        "title": title,
        "body": " ".join(body_lines).strip(),
        "signature_name": signature_name,
        "signature_contacts": signature_contacts,
    }


def build_story(cover: dict):
    def style(name, **kw):
        d = dict(
            fontName="Arial",
            fontSize=BASE,
            leading=BASE * 1.45,
            textColor=colors.HexColor("#333333"),
            alignment=TA_LEFT,
        )
        d.update(kw)
        return ParagraphStyle(name, **d)

    s_name = style(
        "Name",
        fontName="Arial-Bold",
        fontSize=BASE * 1.5,
        leading=BASE * 1.8,
        spaceAfter=2,
    )
    s_meta = style(
        "Meta",
        fontSize=BASE * 0.9,
        leading=BASE * 1.25,
        spaceAfter=8,
        textColor=colors.HexColor("#555555"),
    )
    s_re = style(
        "Re",
        fontName="Arial-Bold",
        fontSize=BASE,
        leading=BASE * 1.3,
        spaceAfter=14,
        textColor=colors.HexColor("#1a1a1a"),
    )
    s_body = style("Body", fontSize=BASE, leading=BASE * 1.5, spaceAfter=24)
    s_sig_name = style(
        "SigName",
        fontName="Arial-Bold",
        fontSize=BASE,
        leading=BASE * 1.3,
        spaceAfter=4,
    )
    s_sig_contacts = style(
        "SigContacts",
        fontSize=BASE * 0.92,
        leading=BASE * 1.3,
        textColor=colors.HexColor("#555555"),
    )

    re_line = cover["title"]
    if re_line.lower().startswith("cover letter"):
        re_line = re_line.split("—", 1)[-1].strip() if "—" in re_line else re_line

    story = [
        Paragraph(process_inline(cover["signature_name"]), s_name),
        Paragraph(process_inline(cover["signature_contacts"]), s_meta),
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor("#bbbbbb"),
            spaceBefore=0,
            spaceAfter=12,
        ),
        Paragraph(process_inline(f"Re: {re_line}"), s_re),
        Paragraph(process_inline(cover["body"]), s_body),
        Paragraph(process_inline(cover["signature_name"]), s_sig_name),
        Paragraph(process_inline(cover["signature_contacts"]), s_sig_contacts),
    ]
    return story


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_cover_pdf.py <application-folder>")
        sys.exit(1)

    folder = Path(sys.argv[1])
    if not folder.is_absolute():
        folder = Path(__file__).parent / folder

    cover_md = folder / "cover.md"
    if not cover_md.exists():
        print(f"Error: {cover_md} not found")
        sys.exit(1)

    output_pdf = folder / PDF_COVER_FILENAME
    cover = parse_cover(cover_md)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    doc.build(build_story(cover))
    output_pdf.write_bytes(buf.getvalue())

    print(f"Saved: {output_pdf}")


if __name__ == "__main__":
    main()

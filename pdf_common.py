"""
Shared PDF helpers for generate_cv_unified.py and generate_cover_pdf.py.

Fonts (auto-detected): macOS Supplemental Arial; Windows %WINDIR%\\Fonts;
  Linux Liberation/DejaVu. Override: JOB_FINDER_FONT_DIR environment variable.
"""

import os
import platform
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

LINK_COLOR = "#1155cc"

# ── Fonts (macOS / Linux / Windows) ───────────────────────────────────────────
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


# ── Markdown inline → reportlab XML ───────────────────────────────────────────
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


def make_style(name: str, **kw) -> ParagraphStyle:
    """ParagraphStyle with the kit's shared defaults (Arial, dark-gray body text)."""
    d = dict(
        fontName="Arial",
        textColor=colors.HexColor("#333333"),
        alignment=TA_LEFT,
    )
    d.update(kw)
    return ParagraphStyle(name, **d)


# ── Application-folder file resolution ────────────────────────────────────────
def resolve_app_md(folder: Path, kind: str) -> Path:
    """Resolve <num>-<kind>.md inside an application folder."""
    if m := re.match(r"^(\d+)-", folder.name):
        numbered = folder / f"{m.group(1)}-{kind}.md"
        if numbered.exists():
            return numbered
        raise FileNotFoundError(
            f"Expected exact source file {numbered}; legacy fallback is disabled "
            "for numbered application folders"
        )
    plain = folder / f"{kind}.md"
    if plain.exists():
        return plain
    hits = sorted(folder.glob(f"*-{kind}.md"))
    if len(hits) == 1:
        return hits[0]
    raise FileNotFoundError(f"No {kind}.md found in {folder}")

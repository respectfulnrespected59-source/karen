"""
Extractor — converts DOCX/PDF/Markdown manuscripts to plain markdown text.

Open-core version: text only. The paid release includes image extraction,
caption preservation, and figure-aware reflow.
"""

from __future__ import annotations

from pathlib import Path


def extract_to_markdown(input_path: Path) -> str:
    """Return manuscript contents as markdown text."""
    suffix = input_path.suffix.lower()
    if suffix == ".docx":
        return _extract_docx(input_path)
    if suffix == ".pdf":
        return _extract_pdf(input_path)
    if suffix in {".md", ".txt"}:
        return input_path.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"Unsupported file type: {suffix}")


def _extract_docx(path: Path) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise ImportError(
            "python-docx is required for .docx scanning. "
            "Install with: pip install python-docx"
        ) from exc

    doc = Document(str(path))
    parts: list[str] = []
    for para in doc.paragraphs:
        text = para.text
        style = (para.style.name or "").lower() if para.style else ""
        if style.startswith("heading"):
            level = "".join(ch for ch in style if ch.isdigit()) or "1"
            parts.append(f"{'#' * int(level)} {text}")
        elif text.strip():
            parts.append(text)
        else:
            parts.append("")
    return "\n".join(parts)


def _extract_pdf(path: Path) -> str:
    try:
        import pdfplumber
    except ImportError as exc:
        raise ImportError(
            "pdfplumber is required for .pdf scanning. "
            "Install with: pip install pdfplumber"
        ) from exc

    chunks: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            chunks.append(text)
    return "\n\n".join(chunks)

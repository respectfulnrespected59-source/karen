"""
KAREN — Killing All Rival Editing Now (open-core scanner).

Scans a manuscript (DOCX, PDF, MD) and reports structural typography damage.
This open-core release is READ-ONLY. The repair pipeline that actually fixes
the damage ships in the paid release:

    https://quantummelaninmedia.gumroad.com/l/sfvygj
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from karen.extractor import extract_to_markdown
from karen.scanner import Scanner

GUMROAD_URL = "https://quantummelaninmedia.gumroad.com/l/sfvygj"


def cmd_scan(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"error: file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        text = extract_to_markdown(input_path)
    except (ImportError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report = Scanner().scan(text)

    print(f"KAREN scan report — {input_path.name}")
    print("=" * 60)
    print(f"  total lines:               {report.total_lines:>8,}")
    print(f"  total words:               {report.total_words:>8,}")
    print("-" * 60)
    print(f"  orphan word fragments:     {report.orphan_word_fragments:>8,}")
    print(f"  heading merge bugs:        {report.heading_merge_bugs:>8,}")
    print(f"  false-bold body sentences: {report.false_bold_body_sentences:>8,}")
    print(f"  buried section headings:   {report.buried_section_headings:>8,}")
    print("-" * 60)
    print(f"  TOTAL DEFECTS:             {report.total_defects:>8,}")
    print("=" * 60)

    if report.total_defects > 0:
        print()
        print("KAREN found structural damage in this manuscript.")
        print("This open-core release detects defects but does not repair them.")
        print()
        print(f"  Repair pipeline: {GUMROAD_URL}")
        print()

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="karen",
        description="KAREN — manuscript structural typography scanner (open-core).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Scan a manuscript and report defects.")
    scan.add_argument("input", help="Path to .docx, .pdf, .md, or .txt file.")
    scan.set_defaults(func=cmd_scan)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

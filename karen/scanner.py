"""
Scanner — KAREN's diagnostic eye.

Counts the structural typography damage in a manuscript without modifying
anything. This is the open-core scanner. The repair pipeline that actually
fixes the damage is part of the paid KAREN release:
https://quantummelaninmedia.gumroad.com/l/sfvygj
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


CONNECTORS: frozenset[str] = frozenset({
    "of", "the", "a", "an", "and", "or", "in", "as", "to", "for", "on",
    "at", "by", "with", "from", "is", "are", "was", "were", "be", "been",
    "being", "their", "this", "that", "its", "our", "your", "these",
    "those", "has", "have", "had", "will", "would", "could", "should",
    "may", "might", "can", "all", "any", "some", "no", "not", "but",
    "if", "when", "while", "because", "so", "than", "then", "also",
    "only", "just", "very", "more", "most", "much",
})

RECURRING_SECTION_LABELS: tuple[str, ...] = (
    "Analysis Through the Melanin Framework",
    "The Mechanism",
    "Case Study",
    "Historical Evidence",
    "Scientific Validation",
)


@dataclass(frozen=True)
class ScanReport:
    """Counts of each kind of structural damage KAREN found."""

    orphan_word_fragments: int
    heading_merge_bugs: int
    false_bold_body_sentences: int
    buried_section_headings: int
    total_lines: int
    total_words: int

    @property
    def total_defects(self) -> int:
        return (
            self.orphan_word_fragments
            + self.heading_merge_bugs
            + self.false_bold_body_sentences
            + self.buried_section_headings
        )

    def as_dict(self) -> dict[str, int]:
        return {
            "orphan_word_fragments": self.orphan_word_fragments,
            "heading_merge_bugs": self.heading_merge_bugs,
            "false_bold_body_sentences": self.false_bold_body_sentences,
            "buried_section_headings": self.buried_section_headings,
            "total_lines": self.total_lines,
            "total_words": self.total_words,
            "total_defects": self.total_defects,
        }


class Scanner:
    """Detects structural defects in markdown manuscripts. Read-only."""

    def __init__(
        self,
        recurring_labels: Iterable[str] = RECURRING_SECTION_LABELS,
    ) -> None:
        self._recurring_labels = tuple(recurring_labels)

    def scan(self, text: str) -> ScanReport:
        lines = text.split("\n")
        orphans = self._count_orphans(lines)
        merge_bugs, false_bold = self._count_heading_issues(lines)
        buried = self._count_buried_headings(lines)
        return ScanReport(
            orphan_word_fragments=orphans,
            heading_merge_bugs=merge_bugs,
            false_bold_body_sentences=false_bold,
            buried_section_headings=buried,
            total_lines=len(lines),
            total_words=sum(len(line.split()) for line in lines),
        )

    @staticmethod
    def _count_orphans(lines: list[str]) -> int:
        skip_prefixes = ("#", "**", "-", "*", "✦", ">", "`", "![")
        count = 0
        for i in range(1, len(lines) - 1):
            cur = lines[i].strip()
            prev = lines[i - 1].strip()
            nxt = lines[i + 1].strip()
            if prev != "" or nxt != "":
                continue
            if not cur or cur.startswith(skip_prefixes):
                continue
            if len(cur.split()) > 4:
                continue
            if cur and not cur[0].isdigit():
                count += 1
        return count

    @staticmethod
    def _count_heading_issues(lines: list[str]) -> tuple[int, int]:
        bold_pattern = re.compile(r"^\*\*(.+?)\*\*$")
        merge_bugs = 0
        false_bold = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            match = bold_pattern.match(stripped)
            if not match:
                continue
            bold = match.group(1).strip()
            if bold.endswith((".", "?", "!")) or len(bold) < 15:
                continue
            if bold.startswith("Chapter "):
                continue
            last_word = bold.split()[-1].lower().rstrip(":-,;")
            ends_with_connector = last_word in CONNECTORS
            ends_with_hyphen = bold.endswith("-")
            if not (ends_with_connector or ends_with_hyphen):
                continue
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines):
                continue
            nxt = lines[j].strip()
            if nxt.startswith(("**", "#", "-", "*")):
                continue
            if len(nxt) < 20:
                continue
            next_word = nxt.split()[0] if nxt.split() else ""
            if next_word and next_word[0].islower():
                false_bold += 1
            else:
                merge_bugs += 1
        return merge_bugs, false_bold

    def _count_buried_headings(self, lines: list[str]) -> int:
        count = 0
        for label in self._recurring_labels:
            for line in lines:
                if label in line and not line.strip().startswith("**"):
                    if len(line) > 80:
                        count += 1
        return count

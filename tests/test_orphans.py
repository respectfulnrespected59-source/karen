"""The scanner must tell a deliberate one-line beat from real fragment damage."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from karen.scanner import Scanner  # noqa: E402


def orphans(text: str) -> int:
    return Scanner().scan(text).orphan_word_fragments


def test_intentional_beats_are_not_damage():
    text = ("I knew that collection. There were no sealed vault folders.\n\nAnd yet.\n\n"
            "Here was a request slip on AAMLO letterhead.\n\nAnd it was warm.\n\n"
            "The note read:\n\n*To the one who finds this — open it.*\n\nMy hands were shaking.\n\nI opened it.\n")
    assert orphans(text) == 0


def test_front_matter_epigraphs_and_contents_are_not_damage():
    text = ("Robert Hadden Jr.\n\nMahal Kita\n\nCopyright © 2026 Robert Hadden Jr. and Mahal Kita\n\n"
            "All rights reserved.\n\nquantummelaninmedia.com\n\nFirst Edition\n\n"
            "Chapter One · The Folder That Wasn't Supposed to Exist\n\nChapter Two · Three Folders\n\n"
            "— The Heike Monogatari, c. thirteenth century\n\nThe lake was still.\n\nNothing moved.\n")
    assert orphans(text) == 0


def test_shattered_sentences_are_still_damage():
    text = "The vault was cold.\n\nThe\n\nvault is always cold, because we keep\n\nit at sixty-five degrees\n\nyear-round.\n"
    assert orphans(text) >= 2


def test_split_dialogue_tag_is_damage():
    assert orphans("He waited.\n\n*Tonight,*\n\nhe said.\n\nShe nodded.\n") >= 1

# KAREN

**K**illing **A**ll **R**ival **E**diting **N**ow.

KAREN is a manuscript structural typography scanner. She reads your DOCX, PDF, or markdown manuscript and tells you exactly how many structural defects it contains — orphan word fragments, heading merge bugs, false-bold body sentences, buried section headings.

This repo is the **open-core scanner**. It is read-only. It diagnoses; it does not repair.

The full repair pipeline that fixes the damage automatically is the paid release:

**[Get KAREN (repair pipeline) on Gumroad →](https://quantummelaninmedia.gumroad.com/l/sfvygj)**

---

## What's in this repo

| Module | Purpose |
|---|---|
| `karen/scanner.py` | The diagnostic engine. Counts 4 classes of structural defect. |
| `karen/extractor.py` | DOCX / PDF / markdown → plain markdown text. |
| `karen.py` | CLI entrypoint. `python karen.py scan <file>` |

What's **not** in this repo (intentionally — paid release only):

- The repair pipeline (`pipeline.py`) — six-stage rewrite that *fixes* the damage
- Paragraph reflow stage
- List reflow stage
- Buried-heading lift stage
- False-bold repair stage
- Split-heading merge stage
- Image extraction & caption preservation
- DOCX/PDF round-trip output

## Quick start

```bash
pip install -r requirements.txt
python karen.py scan path/to/manuscript.docx
```

Sample output:

```
KAREN scan report — magnum_opus.docx
============================================================
  total lines:                  18,432
  total words:                 142,891
------------------------------------------------------------
  orphan word fragments:         1,847
  heading merge bugs:               41
  false-bold body sentences:       312
  buried section headings:         348
------------------------------------------------------------
  TOTAL DEFECTS:                 2,548
============================================================

KAREN found structural damage in this manuscript.
This open-core release detects defects but does not repair them.

  Repair pipeline: https://quantummelaninmedia.gumroad.com/l/sfvygj
```

## The four defect classes

| Defect | What it looks like |
|---|---|
| **Orphan word fragment** | A 1–4 word line floating between blank lines, not a heading, not a list item — the leftover tail of a paragraph that got chopped. |
| **Heading merge bug** | A bold line that ends mid-phrase (e.g. ends with `of`, `the`, `and`) with body text continuing on the next line — the heading and its first paragraph fused, then re-split in the wrong place. |
| **False-bold body sentence** | A bold line that's actually a body sentence the converter mis-styled. The next line continues with a lowercase word. |
| **Buried section heading** | A recurring section label (e.g. `The Mechanism`) trapped inside a long body paragraph instead of standing as its own heading. |

These are the structural artifacts you get when you round-trip a manuscript through DOCX → PDF → markdown → DOCX with a careless toolchain. KAREN was built because the QMM *Magnum Opus* book had **2,548** of them after one bad export.

## Why open-core

The scanner is the easy half — counting defects is mechanical. The repair pipeline is the hard half — fixing them without destroying authorial intent took six stages, dozens of regression manuscripts, and a year of tuning. The repair half pays the rent. The scanner half is yours, free, MIT.

If you want the scanner alone: clone this repo.
If you want the scanner *and* the repair: [grab the paid release](https://quantummelaninmedia.gumroad.com/l/sfvygj).

## License

MIT. See [LICENSE](LICENSE).

## Credits

Built by [Quantum Melanin Media](https://quantummelaninmedia.gumroad.com) — Afrofuturist publishing house. KAREN ships alongside the *Magnum Opus* book series and other QMM titles.

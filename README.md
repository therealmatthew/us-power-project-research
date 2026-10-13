# US power project research

Matthew Z. Marte's research work sample for a Cleanview Research Analyst application.
One detailed case: **Crete Cottage Grove Solar 1, Will County, Illinois**.

Start with [the report](research/crete-cottage-grove/report.md). The case separates proposal details, historical commercial reports, interconnection allegations and unknown current status. Review date: October 13, 2026 (Asia/Manila).

## Repository map

- `data/projects.json`: curated case data; JSON null means unverified, never false/zero.
- `data/evidence.csv`: claims, locators, source classes and evidence limitations.
- `sources/manifest.csv`: source URLs, access results and original-document custody.
- `sources/originals/`: original documents, ignored by default.
- `research/crete-cottage-grove/`: report, timeline and actual search log.
- `scripts/`: native extraction, selective OCR and review-candidate searching.
- `tests/`: page provenance, OCR selection, candidate isolation and case integrity.
- `work/`: ignored extraction and candidate outputs.

Empty CSV cells mean unavailable/not applicable; see the row's limitation. Source type describes provenance; verification status describes what this review actually accessed. Party pleadings are primary filings but their allegations are not commission findings. Indexed excerpts are explicitly labelled.

## Setup and use

Python 3.10+:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m scripts.extract_pdf sources/originals/06-26-2023-agenda.pdf --output work/agenda.jsonl
python -m scripts.search_identifiers work/agenda.jsonl --output work/agenda-candidates.csv
```

Native text is extracted on every page first. Pages with fewer than 40 alphanumeric characters are flagged; `--min-chars` adjusts the heuristic. For OCR, install local Tesseract with English language data and add its executable to PATH, then use `--ocr`. Only flagged pages are rendered at 300 DPI and OCR'd. Sparse title pages may be flagged unnecessarily, and mixed scanned/native content may need manual review. No documents are sent to an OCR service.

Outputs retain original filename, one-based physical PDF page, SHA-256 of original bytes and extraction method. Printed page labels and exhibit locators belong in manually reviewed citations and are not interchangeable with physical pages. Native text is retained even after OCR. OCR dependency/errors fail explicitly; they are not silently treated as native successes. Existing outputs are never overwritten; choose a new output name to rerun.

Candidate exports must be CSVs inside `work/`; regexes deliberately include neighboring projects and ambiguous docket/utility IDs. Each match retains its exact offsets, page context and unreviewed status. A human checks identity, provenance and claim scope before manually editing curated data. Scripts never promote candidates automatically.

## Evidence boundaries

See the report and manifest for source-specific access limits. An agenda does not prove a final vote; a planned purchaser does not prove a PPA; a permit extension does not prove operation. The August 12, 2026 reported extension end is historical as of this review. Current status, final BESS, COD, capacity credit and Digital Realty membership are unknown.

## Delivery

Git was initialized locally, then GitHub publication was explicitly authorized. The repository remote is `https://github.com/therealmatthew/us-power-project-research.git`. Originals and working output remain ignored. See `CHECKS.md` for executed checks and evidence limitations.

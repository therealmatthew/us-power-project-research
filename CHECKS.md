# Executed checks and access limits

Executed October 13, 2026 (Asia/Manila), using Python 3.14.6 and Git 2.53.0.windows.2.
Available libraries: pypdf 6.20.0, pypdfium2 5.14.0, Pillow 12.3.0.

## Working

- `python -m unittest discover -s tests -v`: all 8 tests pass from the repository root. Tests create a real three-page PDF with native text and a blank middle page.
- Verified physical-page numbering, original-byte SHA-256, JSONL round-trip, blank-page retention, native-first extraction, selective OCR routing, explicit OCR failure, candidate context and offsets, neighboring project ambiguity, missing-provenance rejection, CSV export, and no overwrite/promotion of curated data (including path traversal).
- Both script CLI help commands run. A synthetic PDF CLI extraction/search smoke check produces page records and unreviewed candidates.
- pypdfium2 rendering of the synthetic fixture works; this is rendering verification, not OCR accuracy validation.
- Curated JSON nulls and evidence/source joins pass integrity checks.
- Local Git initialization and ignored originals/work paths verified; no remote configured and no push performed.

## Blocked or unverified

- Native extraction of the cited originals is blocked by retrieval: Village of Crete HTTP 403; ICC connection timeout after network access was granted. No original document bytes held and no source document hashes invented.
- The web tool returned the official agenda's page-indexed text and ICC indexed text. These accesses are distinguished from original-file retrieval in the manifest and report.
- Yahoo returned HTTP 429; Will County Gazette returned HTTP 403. Their supplied facts remain labelled as not independently retrieved.
- Tesseract is not on PATH. OCR routing and failure handling pass tests with injected stubs; actual OCR recognition/accuracy was not run. Install Tesseract plus English language data to use `--ocr`.
- Official adopted votes, current permits, ownership, operation, COD, BESS configuration, purchase agreement, capacity credit and Digital Realty membership remain unverified.
- The initial test discovery command was accidentally run in the parent directory and loaded an unrelated installed test suite; the command was corrected to the repository root. Only the scoped repository result is reported above.

Dependency installation in a clean virtual environment was not performed; checks used the available matching versions. Regex candidates and sparse-text OCR heuristics require human review.

Git's sandbox ownership warning was handled with a command-scoped safe.directory for this repository only; global Git configuration was not changed. Repository-local ignore rules were verified despite an unreadable global ignore file. The initial local commit uses Codex <codex@localhost> as the automation identity; Matthew's authorship attribution is in the README.

# Research checks and access limits

Reviewed October 13, 2026 (Asia/Manila).

## Research-file checks

- The retained research-data integrity test passes using only the standard library. It checks nulls for unverified fields, project-to-evidence IDs, evidence-to-source links, nonempty claim locators and limitations, absence of invented quotations, and the unverified official extension decision flag.
- Project JSON, evidence CSV, source manifest, timeline and search log are unchanged from the previous local commit; their file hashes match the pre-edit snapshots.
- Case findings and citations are preserved. Only the report's closing methodology paragraph was updated to describe the remaining research records.
- The CSV files parse successfully. Timeline source IDs and search-log source IDs resolve to the source manifest, including rows with multiple sources; empty source IDs remain research leads.
- Local Markdown links resolve to retained research files. References to external sources and git-ignored originals are distinguished from files held in this checkout.
- The diff passes whitespace checks. Original documents and local working files remain excluded from Git. Checks were completed locally before publication.

## Access limits and unverified findings

- Original-document retrieval failed: Village of Crete returned HTTP 403; ICC timed out after network access was granted. No original document bytes are held and source document hashes remain empty.
- The web tool returned the official agenda's page-indexed text and ICC indexed text. These accesses are distinguished from original-file retrieval in the manifest and report.
- Yahoo returned HTTP 429; Will County Gazette returned HTTP 403. Their supplied facts remain labelled as not independently retrieved.
- Official adopted votes, current permits, ownership, operation, COD, BESS configuration, purchase agreement, capacity credit and Digital Realty membership remain unverified.

These are file-integrity and traceability checks, not independent confirmation of the underlying research claims. No sources were re-fetched during this revision.

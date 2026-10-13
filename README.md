# US Power Project Research

A public-record research case study by Matthew Z. Marte tracing
Crete Cottage Grove Solar 1 in Will County, Illinois across county
zoning records, company statements, and utility regulatory filings.

The research connects a consistent parcel identifier to the project's
2023 zoning application and ComEd interconnection identifier. It records
proposed capacity, reported ownership, and a subsequent permitting update,
while leaving unsupported conclusions unresolved.

**Start with [the case report](research/crete-cottage-grove/report.md).**

## Key findings

- Linked zoning case ZC-23-006 to parcel 23-15-15-400-010-0000
  and Crete Cottage Grove Solar 1, LLC.
- Identified proposed capacity of 3.42 MW and reported Soltage ownership.
- Located indexed ICC filing text linking the project to ComEd
  identifier 22-19568.
- Located a reported February 2026 permitting extension.
- Distinguished these findings from unverified current operating status,
  final BESS configuration, COD, capacity credit, and Digital Realty
  portfolio membership.

## Planned automation

A future extension will extract PDF text, apply local OCR to scanned
pages, and identify project references while preserving source and page
information. This automation has not yet been implemented.

**Review date:** October 13, 2026.

## Repository map

-  `data/projects.json`: curated case data; `null` means not established
  in this review, not false or zero.
- `data/evidence.csv`: claims, locators, source classes and evidence limitations.
- `sources/manifest.csv`: source URLs, access results and original-document custody.
- `sources/originals/`: original documents, ignored by default.
- `research/crete-cottage-grove/`: report, timeline and actual search log.

Empty CSV cells mean unavailable/not applicable; see the row's limitation. Source type describes provenance; verification status describes what this review actually accessed. Party pleadings are primary filings but their allegations are not commission findings. Indexed excerpts are explicitly labelled.

## Evidence boundaries

See the report and manifest for source-specific access limits. An agenda does not prove a final vote; a planned purchaser does not prove a PPA; a permit extension does not prove operation. The August 12, 2026 reported extension end is historical as of this review. Current status, final BESS, COD, capacity credit and Digital Realty membership are unknown.

## Repository

[View the repository](https://github.com/therealmatthew/us-power-project-research).

The case report, structured project record, evidence table, timeline,
and source manifest document the findings and research limitations.

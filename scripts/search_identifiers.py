"""Export matches as review candidates, never curated facts."""
import argparse
import csv
import json
import re
from pathlib import Path
PATTERNS = {
    'entity': r'\bCrete\s+Cottage\s+Grove\s+Solar\s+1(?:\s*,?\s*LLC)?\b',
    'pin': r'\b\d{2}-\d{2}-\d{2}-\d{3}-\d{3}-\d{4}\b',
    'zoning_case': r'\bZC-\d{2}-\d{3}\b',
    'permit_request': r'\bS-\d{2}-\d{3}\b',
    'utility_project_or_docket': r'\b\d{2}-\d{4,5}\b',
    'capacity_mw': r'\b\d+(?:\.\d+)?\s*MW\b',
    'line_or_feeder': r'\b[LF]\d{3,5}\b',
}
FIELDS = ['filename','page_number','document_sha256','extraction_method',
          'candidate_type','matched_text','start_offset','end_offset','context','review_status']
def candidates(pages):
    for page in pages:
        for field in ('filename','page_number','document_sha256','extraction_method','text'):
            if field not in page:
                raise ValueError(f'missing provenance field: {field}')
        if not isinstance(page['page_number'], int) or page['page_number'] < 1:
            raise ValueError('page_number must be a positive integer')
        if not re.fullmatch(r'[0-9a-f]{64}',page['document_sha256']):
            raise ValueError('document_sha256 must be a SHA-256 hex digest')
        text = page['text']
        for kind, pattern in PATTERNS.items():
            for match in re.finditer(pattern,text,re.IGNORECASE):
                yield {
                    **{key:page[key] for key in FIELDS[:4]},
                    'candidate_type':kind, 'matched_text':match.group(),
                    'start_offset':match.start(), 'end_offset':match.end(),
                    'context':text[max(0,match.start()-100):match.end()+100],
                    'review_status':'unreviewed',
                }

def export_candidates(pages, output):
    output = Path(output).resolve()
    # Keep all automated output outside curated data, research and sources.
    if output.suffix.lower() != '.csv' or 'work' not in output.parts:
        raise ValueError('candidate output must be a CSV within a work/ directory')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',newline='',encoding='utf-8') as stream:
        writer = csv.DictWriter(stream,fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(candidates(pages))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('jsonl',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args = parser.parse_args()
    with args.jsonl.open(encoding='utf-8') as stream:
        pages = [json.loads(line) for line in stream if line.strip()]
    export_candidates(pages,args.output)
if __name__ == '__main__':
    main()

"""Native text first, optional OCR only for pages flagged as sparse."""
import argparse
import hashlib
import json
from pathlib import Path

def needs_ocr(text, min_chars=40):
    return sum(c.isalnum() for c in text) < min_chars

def extract_pages(path, min_chars=40):
    from pypdf import PdfReader
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = []
    for number, page in enumerate(PdfReader(path).pages, 1):
        error = None
        try:
            text = page.extract_text() or ''
        except Exception as exc:
            text = ''
            error = f'{type(exc).__name__}: {exc}'
        result.append({
            'filename': path.name, 'page_number': number,
            'page_number_basis': 'one-based PDF physical page; not printed label',
            'document_sha256': digest, 'extraction_method': 'native',
            'native_text': text, 'text': text, 'native_extraction_error': error,
            'needs_ocr': needs_ocr(text, min_chars), 'ocr_status': 'not_attempted',
        })
    return result

def extract(path, min_chars=40, ocr=False, ocr_engine=None):
    pages = extract_pages(path, min_chars)
    if ocr:
        if ocr_engine is None:
            try:
                from .selective_ocr import ocr_page
            except ImportError:
                from selective_ocr import ocr_page
            ocr_engine = ocr_page
        for page in pages:
            if page['needs_ocr']:
                page['text'] = ocr_engine(Path(path), page['page_number'])
                page['extraction_method'] = 'ocr:tesseract'
                page['ocr_status'] = 'completed' if page['text'].strip() else 'empty'
    return pages

def write_jsonl(records, output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--ocr', action='store_true')
    parser.add_argument('--min-chars', type=int, default=40)
    args = parser.parse_args()
    if args.min_chars < 1:
        parser.error('--min-chars must be positive')
    if args.pdf.resolve() == args.output.resolve():
        parser.error('output cannot be the source PDF')
    write_jsonl(extract(args.pdf, args.min_chars, args.ocr), args.output)

if __name__ == '__main__':
    main()

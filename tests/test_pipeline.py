import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
from scripts.extract_pdf import extract, write_jsonl
from scripts.search_identifiers import candidates, export_candidates

ROOT = Path(__file__).resolve().parents[1]

def fixture(path):
    writer = PdfWriter()
    font = DictionaryObject({NameObject('/Type'):NameObject('/Font'),
        NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    font_ref = writer._add_object(font)
    texts = [
        'Crete Cottage Grove Solar 1, LLC PIN 23-15-15-400-010-0000 ZC-23-006 S-23-003 3.42 MW',
        None,
        'Neighbor Crete Goodenow Solar 1 22-19569; Cottage Grove 22-19568 line L12735 feeder F365',
    ]
    for text in texts:
        page = writer.add_blank_page(width=612,height=792)
        if text:
            page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):font_ref})})
            stream = DecodedStreamObject()
            stream.set_data(f'BT /F1 10 Tf 20 750 Td ({text}) Tj ET'.encode())
            page[NameObject('/Contents')] = writer._add_object(stream)
    with path.open('wb') as output:
        writer.write(output)

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pdf = Path(self.temp.name)/'original.pdf'
        fixture(self.pdf)

    def test_blank_pages_preserve_physical_numbers_and_hash(self):
        pages = extract(self.pdf)
        self.assertEqual([p['page_number'] for p in pages],[1,2,3])
        self.assertEqual(pages[1]['text'],'')
        digest = hashlib.sha256(self.pdf.read_bytes()).hexdigest()
        for p in pages:
            self.assertEqual(p['document_sha256'],digest)
            self.assertEqual(p['filename'],'original.pdf')
            self.assertEqual(p['extraction_method'],'native')
        self.assertEqual([p['needs_ocr'] for p in pages],[False,True,False])
        out = Path(self.temp.name)/'pages.jsonl'
        write_jsonl(pages,out)
        restored = [json.loads(s) for s in out.read_text().splitlines()]
        self.assertEqual(restored,pages)
        with self.assertRaises(FileExistsError): write_jsonl(pages,out)

    def test_ocr_only_calls_blank_page_and_retains_provenance(self):
        calls = []
        def engine(path,number):
            calls.append((path,number))
            return 'Scanned 22-19568 S-23-004'
        pages = extract(self.pdf,ocr=True,ocr_engine=engine)
        self.assertEqual(calls,[(self.pdf,2)])
        self.assertEqual(pages[1]['native_text'],'')
        self.assertEqual(pages[1]['extraction_method'],'ocr:tesseract')
        self.assertEqual(pages[0]['extraction_method'],'native')
        self.assertEqual(pages[1]['document_sha256'],pages[0]['document_sha256'])
        hit = next(c for c in candidates(pages) if c['matched_text']=='S-23-004')
        self.assertEqual(hit['page_number'],2)
        self.assertEqual(hit['extraction_method'],'ocr:tesseract')

    def test_ocr_errors_are_explicit(self):
        def broken(*args): raise RuntimeError('OCR unavailable')
        with self.assertRaisesRegex(RuntimeError,'OCR unavailable'):
            extract(self.pdf,ocr=True,ocr_engine=broken)
        from scripts.selective_ocr import ocr_page
        with patch('scripts.selective_ocr.shutil.which',return_value=None):
            with self.assertRaisesRegex(RuntimeError,'Tesseract'):
                ocr_page(self.pdf,2)

    def test_candidates_keep_page_context_offsets_and_neighbor_ambiguity(self):
        pages = extract(self.pdf)
        hits = list(candidates(pages))
        self.assertIn('Crete Cottage Grove Solar 1, LLC',[h['matched_text'] for h in hits])
        self.assertIn('23-15-15-400-010-0000',[h['matched_text'] for h in hits])
        self.assertIn('3.42 MW',[h['matched_text'] for h in hits])
        for value in ['22-19568','22-19569','L12735','F365']:
            hit = next(h for h in hits if h['matched_text']==value)
            self.assertEqual(hit['page_number'],3)
            self.assertEqual(hit['review_status'],'unreviewed')
            self.assertIn('Neighbor',hit['context'])
        for hit in hits:
            text = pages[hit['page_number']-1]['text']
            self.assertEqual(text[hit['start_offset']:hit['end_offset']],hit['matched_text'])

    def test_export_cannot_overwrite_or_promote_curated_data(self):
        before = (ROOT/'data/projects.json').read_bytes()
        out = Path(self.temp.name)/'work'/'candidates.csv'
        export_candidates(extract(self.pdf),out)
        with out.open(newline='',encoding='utf-8') as stream:
            rows = list(csv.DictReader(stream))
        self.assertTrue(rows)
        self.assertTrue(all(r['review_status']=='unreviewed' for r in rows))
        with self.assertRaises(FileExistsError): export_candidates(extract(self.pdf),out)
        with self.assertRaises(ValueError): export_candidates(extract(self.pdf),ROOT/'data/evidence.csv')
        with self.assertRaises(ValueError): export_candidates(extract(self.pdf),ROOT/'data/projects.json')
        with self.assertRaises(ValueError):
            export_candidates(extract(self.pdf),Path(self.temp.name)/'work'/'..'/'data'/'new.csv')
        self.assertEqual((ROOT/'data/projects.json').read_bytes(),before)

    def test_missing_provenance_rejected(self):
        with self.assertRaisesRegex(ValueError,'provenance'):
            list(candidates([{'text':'22-19568'}]))
        page = extract(self.pdf)[0]
        page['document_sha256'] = ''
        with self.assertRaisesRegex(ValueError,'SHA-256'): list(candidates([page]))

    def test_no_cross_page_join_and_boundaries(self):
        base = extract(self.pdf)[0]
        pages = [{**base,'text':'Crete Cottage Grove'},
                 {**base,'page_number':2,'text':'Solar 1, LLC XZC-23-006 22-195680 23-15-15-400-010-00001'}]
        self.assertEqual(list(candidates(pages)),[])

class CuratedDataTests(unittest.TestCase):
    def test_nulls_evidence_links_and_limits(self):
        project = json.loads((ROOT/'data/projects.json').read_text())[0]
        for field in ['capacity_basis','current_owner','executed_purchase_agreement',
                      'current_operation','current_permit_status','final_bess_configuration',
                      'commercial_operation_date','capacity_credit_mw','digital_realty_portfolio_membership']:
            self.assertIsNone(project[field],field)
        with (ROOT/'data/evidence.csv').open(newline='',encoding='utf-8') as f:
            evidence = list(csv.DictReader(f))
        with (ROOT/'sources/manifest.csv').open(newline='',encoding='utf-8') as f:
            sources = {r['source_id']:r for r in csv.DictReader(f)}
        self.assertEqual(set(project['evidence_ids']),{r['evidence_id'] for r in evidence})
        for row in evidence:
            self.assertIn(row['source_id'],sources)
            self.assertTrue(row['limitation'])
            self.assertTrue(row['locator'])
            self.assertEqual(row['quotation'],'')
        self.assertFalse(project['permit_extension_report']['official_decision_verified'])

if __name__ == '__main__': unittest.main()

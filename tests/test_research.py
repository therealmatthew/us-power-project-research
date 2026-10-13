import csv
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def csv_rows(relative_path):
    with (ROOT / relative_path).open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError('Missing or duplicate CSV headings')
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise ValueError('CSV row width does not match headings')
        return reader.fieldnames, rows


class ResearchRecordTests(unittest.TestCase):
    def test_nulls_and_evidence_references(self):
        project = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))[0]
        for field in ['capacity_basis', 'current_owner', 'executed_purchase_agreement',
                      'current_operation', 'current_permit_status', 'final_bess_configuration',
                      'commercial_operation_date', 'capacity_credit_mw',
                      'digital_realty_portfolio_membership']:
            self.assertIsNone(project[field], field)
        headings, evidence = csv_rows('data/evidence.csv')
        self.assertEqual(headings, ['Finding', 'Evidence', 'Source', 'Page or passage',
                                    'Evidence date', 'Remaining uncertainty'])
        findings = [row['Finding'] for row in evidence]
        self.assertEqual(len(findings), len(set(findings)))
        self.assertEqual(set(project['evidence_findings']), set(findings))
        _, manifest = csv_rows('sources/manifest.csv')
        sources = {row['source_id']: row for row in manifest}
        for row in evidence:
            source_id = row['Source'].split(':', 1)[0]
            self.assertIn(source_id, sources)
            self.assertTrue(row['Evidence'])
            self.assertTrue(row['Page or passage'])
            self.assertTrue(row['Remaining uncertainty'])
            self.assertEqual(row['Evidence date'], sources[source_id]['document_date'])
        self.assertFalse(project['permit_extension_report']['official_decision_verified'])
        self.assertFalse(project['digital_realty_discovery_lead']['project_membership_established'])

    def test_source_review_and_supporting_records(self):
        _, manifest = csv_rows('sources/manifest.csv')
        sources = {row['source_id']: row for row in manifest}
        self.assertEqual(sources['S2']['review_description'], 'Agenda reference; search excerpt reviewed')
        self.assertEqual(sources['S3']['review_description'], 'News report')
        self.assertEqual(sources['S4']['review_description'], 'Document excerpt reviewed')
        for source in manifest:
            self.assertTrue(source['url'].startswith('https://'))
            self.assertTrue(source['access_result'])
            self.assertTrue(source['limitations'])
            self.assertEqual(source['local_path'], '')
            self.assertEqual(source['document_sha256'], '')
        for name in ['research/crete-cottage-grove/timeline.csv',
                     'research/crete-cottage-grove/search-log.csv']:
            _, rows = csv_rows(name)
            for row in rows:
                for source_id in filter(None, row['source_id'].split(';')):
                    self.assertIn(source_id, sources)
        _, timeline = csv_rows('research/crete-cottage-grove/timeline.csv')
        project = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))[0]
        extension = project['permit_extension_report']
        dates = {row['date'] for row in timeline}
        for key in ['committee_date', 'reported_through']:
            self.assertIn(extension[key], dates)
        self.assertEqual(extension['publication_date'], sources['S5']['document_date'])

    def test_local_markdown_links(self):
        for document in [ROOT / 'README.md', ROOT / 'CHECKS.md',
                         ROOT / 'sources/README.md',
                         ROOT / 'research/crete-cottage-grove/report.md']:
            text = document.read_text(encoding='utf-8')
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if re.match(r'\w+://', target) or target.startswith('#'):
                    continue
                path = (document.parent / target.split('#')[0]).resolve()
                self.assertTrue(path.is_file(), f'{document.name}: {target}')


if __name__ == '__main__':
    unittest.main()

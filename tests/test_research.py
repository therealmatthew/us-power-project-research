import csv
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

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

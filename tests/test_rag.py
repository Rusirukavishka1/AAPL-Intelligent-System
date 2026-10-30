import unittest
import json
from pathlib import Path
from rag import ingest,retrieve
class EvidenceTests(unittest.TestCase):
    def test_cutoff_and_no_match(self):
        docs=ingest('report.txt',b'Apple revenue increased during the year.','2025-01-01')
        self.assertTrue(retrieve('Apple revenue',docs))
        self.assertFalse(retrieve('Apple revenue',docs,'2024-12-31'))
        self.assertFalse(retrieve('quantum telescope',docs))
        self.assertFalse(retrieve('Apple revenue',docs,scope='Research'))
    def test_explanation_reconstruction(self):
        data=json.loads((Path(__file__).parents[1]/'data/research.json').read_text())
        for seed,rows in data['rows'].items():
            ex=data['explanations'][seed]
            for i,row in enumerate(rows):
                self.assertAlmostEqual(row['Ridge'],ex['ridgeBase']+sum(ex['ridge'][i]),places=3)
                self.assertAlmostEqual(row['XGBoost'],ex['xgbBase'][i]+sum(ex['xgb'][i]),places=3)

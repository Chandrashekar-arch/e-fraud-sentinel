import unittest

from fraud_detector.sample_data import SAMPLE_TRANSACTIONS
from fraud_detector.scoring import compute_risk, evaluate_dataset, summarize_transactions


class FraudScoringTests(unittest.TestCase):
    def test_low_risk_sample_is_approved(self):
        result = compute_risk(SAMPLE_TRANSACTIONS[0])
        self.assertEqual(result.level, "Low")
        self.assertLess(result.score, 35)

    def test_obvious_fraud_sample_is_critical(self):
        result = compute_risk(SAMPLE_TRANSACTIONS[6])
        self.assertEqual(result.level, "Critical")
        self.assertGreaterEqual(result.score, 75)

    def test_dataset_evaluation_has_expected_shape(self):
        metrics = evaluate_dataset(SAMPLE_TRANSACTIONS)
        self.assertIn("accuracy", metrics)
        self.assertIn("precision", metrics)
        self.assertIn("recall", metrics)

    def test_summary_counts_all_transactions(self):
        summary = summarize_transactions(SAMPLE_TRANSACTIONS)
        self.assertEqual(summary["total"], len(SAMPLE_TRANSACTIONS))


if __name__ == "__main__":
    unittest.main()

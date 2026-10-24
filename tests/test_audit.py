import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _paths  # noqa: F401,E402
import audit  # noqa: E402


def write(path, rows, headers):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "posts.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def test_rates_median_and_pending(self):
        write(self.path, [
            {"date": "2026-10-01", "type": "proof", "impressions": "1000", "reactions": "40", "comments": "10", "reposts": "0", "chars": "900"},
            {"date": "2026-10-03", "type": "teach", "impressions": "1,000", "reactions": "10", "comments": "0", "reposts": "0", "chars": "1500"},
            {"date": "2026-10-05", "type": "teach", "impressions": "2000", "reactions": "40", "comments": "0", "reposts": "0", "chars": "300"},
            {"date": "2026-10-07", "type": "proof", "impressions": "", "reactions": "", "comments": "", "reposts": "", "chars": ""},
        ], ["date", "type", "impressions", "reactions", "comments", "reposts", "chars"])
        res = audit.analyse(audit.load(self.path))
        self.assertEqual(len(res["posts"]), 3)
        self.assertEqual(len(res["pending"]), 1)
        self.assertAlmostEqual(res["median_rate"], 0.02)
        top = res["posts"][0]
        self.assertEqual(top["type"], "proof")
        self.assertAlmostEqual(top["vs_median"], 2.5)
        self.assertEqual(res["groups"]["band"]["medium (600-1299)"]["posts"], 1)
        self.assertTrue(res["warnings"])  # small sample

    def test_no_numbers(self):
        write(self.path, [{"date": "2026-10-01", "impressions": ""}], ["date", "impressions"])
        res = audit.analyse(audit.load(self.path))
        self.assertIsNone(res["median_rate"])
        self.assertIn("no posts", audit.render(res))

    def test_aliases_and_since(self):
        write(self.path, [
            {"Date": "2026-09-01", "Views": "100", "Likes": "5", "Shares": "1"},
            {"Date": "2026-10-01", "Views": "100", "Likes": "1", "Shares": "0"},
        ], ["Date", "Views", "Likes", "Shares"])
        res = audit.analyse(audit.load(self.path), since="2026-09-15")
        self.assertEqual(len(res["posts"]), 1)
        self.assertAlmostEqual(res["posts"][0]["rate"], 0.01)

    def test_to_num(self):
        self.assertEqual(audit.to_num("1,200"), 1200)
        self.assertIsNone(audit.to_num("n/a"))
        self.assertIsNone(audit.to_num(""))

    def test_cli(self):
        write(self.path, [{"date": "2026-10-01", "impressions": "10", "reactions": "1"}], ["date", "impressions", "reactions"])
        self.assertEqual(audit.main([self.path]), 0)


if __name__ == "__main__":
    unittest.main()

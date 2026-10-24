import csv
import datetime as dt
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _paths  # noqa: F401,E402
import dmqueue  # noqa: E402

DAY = dt.date(2026, 10, 21)  # a Wednesday


def write_leads(path, rows, headers):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)


class DmQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.leads = os.path.join(self.tmp.name, "leads.csv")
        self.log = os.path.join(self.tmp.name, "out", "outreach.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def sample(self, n=5):
        rows = [{"business_slug": "lunch-lane", "name": "Person %d" % i, "company": "Co %d" % i,
                 "role": "Ops lead", "fit_score": str(i * 10), "fit_reason": "posted about lunch %d" % i,
                 "linkedin_url": "https://www.linkedin.com/in/person-%d" % i}
                for i in range(n)]
        write_leads(self.leads, rows, dmqueue.LEADS_COLUMNS)
        rows, headers = dmqueue.read_csv(self.leads)
        return dmqueue.normalise_leads(rows, headers)[0]

    def test_alias_columns_and_split_names(self):
        write_leads(self.leads, [{"First Name": "Dana", "Last Name": "Ruiz", "Organization": "Northwind",
                                  "Why": "hiring ops", "Profile": "https://www.linkedin.com/in/dana"}],
                    ["First Name", "Last Name", "Organization", "Why", "Profile"])
        rows, headers = dmqueue.read_csv(self.leads)
        leads, missing = dmqueue.normalise_leads(rows, headers)
        self.assertEqual(leads[0]["name"], "Dana Ruiz")
        self.assertEqual(leads[0]["company"], "Northwind")
        self.assertEqual(missing, [])

    def test_pick_respects_daily_limit_and_sorts_by_fit(self):
        leads = self.sample(5)
        chosen, waiting, skipped, *_ = dmqueue.pick(leads, [], DAY, 3)
        self.assertEqual([c["name"] for c in chosen], ["Person 4", "Person 3", "Person 2"])
        self.assertEqual(chosen[0]["fit"], 40)
        self.assertEqual(len(waiting), 2)

    def test_pick_counts_today_already_sent(self):
        leads = self.sample(5)
        dmqueue.mark(self.log, "Someone", "Else", "invite", DAY)
        dmqueue.mark(self.log, "Other", "Else", "invite", DAY)
        chosen, *_ = dmqueue.pick(leads, dmqueue.read_log(self.log), DAY, 3)
        self.assertEqual(len(chosen), 1)

    def test_weekly_ceiling(self):
        leads = self.sample(5)
        log = [{"date": (DAY - dt.timedelta(days=1)).isoformat(), "name": "x%d" % i, "company": "",
                "step": "invite"} for i in range(dmqueue.WEEKLY_CEILING)]
        chosen, *_ , room = dmqueue.pick(leads, log, DAY, 15)
        self.assertEqual(room, 0)
        self.assertEqual(chosen, [])

    def test_skips_already_contacted_no_reason_and_dnc(self):
        write_leads(self.leads, [
            {"name": "A", "company": "X", "reason": "r", "status": ""},
            {"name": "B", "company": "X", "reason": "", "status": ""},
            {"name": "C", "company": "X", "reason": "r", "status": "Do-not-contact"},
        ], ["name", "company", "reason", "status"])
        rows, headers = dmqueue.read_csv(self.leads)
        leads, _ = dmqueue.normalise_leads(rows, headers)
        log = [{"name": "A", "company": "X", "step": "invite", "date": "2026-10-01"}]
        chosen, waiting, skipped, *_ = dmqueue.pick(leads, log, DAY, 10)
        self.assertEqual(chosen, [])
        reasons = dict(skipped)
        self.assertIn("already", reasons["A"])
        self.assertIn("reason", reasons["B"])
        self.assertEqual(reasons["C"], "do-not-contact")

    def shared(self):
        rows = [
            {"business_slug": "lunch-lane", "name": "Dana Ruiz", "company": "Northwind", "fit_score": "90",
             "fit_reason": "posted about lunch", "status": "new",
             "linkedin_url": "https://www.linkedin.com/in/dana-ruiz"},
            {"business_slug": "lunch-lane", "name": "No Link", "company": "Pier", "fit_score": "99",
             "fit_reason": "asked about lunch", "status": "new", "linkedin_url": ""},
            {"business_slug": "frameleaf", "name": "Maria Gomez", "company": "School", "fit_score": "95",
             "fit_reason": "teacher post", "status": "new"},
            {"business_slug": "lunch-lane", "name": "Lee Chen", "company": "Harbor", "fit_score": "80",
             "fit_reason": "meetup", "status": "do-not-contact"},
            {"business_slug": "lunch-lane", "name": "Sam Ok", "company": "Bright", "fit_score": "70",
             "fit_reason": "hiring", "status": "replied"},
            {"business_slug": "", "name": "No Biz", "company": "Q", "fit_score": "99",
             "fit_reason": "x", "status": "new"},
        ]
        write_leads(self.leads, rows, dmqueue.LEADS_COLUMNS)
        rows, headers = dmqueue.read_csv(self.leads)
        return dmqueue.normalise_leads(rows, headers)

    def test_shared_layout_filters_by_business(self):
        leads, missing = self.shared()
        self.assertEqual(missing, [])
        chosen, waiting, skipped, *_ = dmqueue.pick(leads, [], DAY, 10, "lunch-lane")
        self.assertEqual([c["name"] for c in chosen], ["Dana Ruiz"])
        reasons = dict(skipped)
        self.assertNotIn("Maria Gomez", reasons)  # other business: silently left out
        self.assertEqual(reasons["Lee Chen"], "do-not-contact")
        self.assertIn("replied", reasons["Sam Ok"])
        self.assertIn("business_slug", reasons["No Biz"])
        self.assertIn("linkedin_url", reasons["No Link"])  # high fit, but no profile link

    def test_missing_linkedin_column_is_reported(self):
        write_leads(self.leads, [{"name": "A", "company": "X", "reason": "r"}], ["name", "company", "reason"])
        rows, headers = dmqueue.read_csv(self.leads)
        leads, missing = dmqueue.normalise_leads(rows, headers)
        self.assertEqual(missing, ["linkedin"])
        chosen, _, skipped, *_ = dmqueue.pick(leads, [], DAY, 10)
        self.assertEqual(chosen, [])
        self.assertIn("linkedin_url", dict(skipped)["A"])

    def test_dnc_skipped_even_without_business(self):
        leads, _ = self.shared()
        chosen, *_ = dmqueue.pick(leads, [], DAY, 10)
        self.assertNotIn("Lee Chen", [c["name"] for c in chosen])

    def test_update_lead_status_and_last_contact(self):
        self.shared()
        self.assertTrue(dmqueue.update_lead(self.leads, "Dana Ruiz", "Northwind", "contacted", DAY, "lunch-lane"))
        rows, headers = dmqueue.read_csv(self.leads)
        self.assertEqual(headers, dmqueue.LEADS_COLUMNS)  # column order kept
        dana = [r for r in rows if r["name"] == "Dana Ruiz"][0]
        self.assertEqual(dana["status"], "contacted")
        self.assertEqual(dana["last_contact"], "2026-10-21")
        maria = [r for r in rows if r["name"] == "Maria Gomez"][0]
        self.assertEqual(maria["status"], "new")
        self.assertFalse(dmqueue.update_lead(self.leads, "Nobody", "", "contacted", DAY))

    def test_cli_mark_updates_leads(self):
        self.shared()
        self.assertEqual(dmqueue.main(["mark", "--log", self.log, "--name", "Dana Ruiz", "--company",
                                       "Northwind", "--step", "invite", "--leads", self.leads,
                                       "--business", "lunch-lane", "--date", DAY.isoformat()]), 0)
        rows, _ = dmqueue.read_csv(self.leads)
        self.assertEqual([r for r in rows if r["name"] == "Dana Ruiz"][0]["status"], "contacted")

    def test_mark_sets_next_steps(self):
        r = dmqueue.mark(self.log, "Dana", "N", "accepted", DAY)
        self.assertEqual(r["next_step"], "message")
        self.assertEqual(r["next_date"], "2026-10-22")
        r = dmqueue.mark(self.log, "Dana", "N", "message", DAY)
        self.assertEqual(r["next_date"], "2026-10-25")
        r = dmqueue.mark(self.log, "Dana", "N", "follow-up-2", DAY)
        self.assertEqual(r["next_step"], "")

    def test_mark_rejects_unknown_step(self):
        with self.assertRaises(ValueError):
            dmqueue.mark(self.log, "a", "b", "pitch", DAY)

    def test_due_uses_latest_row(self):
        dmqueue.mark(self.log, "Dana", "N", "message", DAY - dt.timedelta(days=5))
        self.assertEqual(len(dmqueue.due(dmqueue.read_log(self.log), DAY)), 1)
        dmqueue.mark(self.log, "Dana", "N", "replied", DAY)
        self.assertEqual(dmqueue.due(dmqueue.read_log(self.log), DAY), [])

    def test_count(self):
        self.assertEqual(dmqueue.main(["count", "--text", "a" * 200]), 0)
        self.assertEqual(dmqueue.main(["count", "--text", "a" * 201]), 1)

    def test_cli_pick_missing_file(self):
        self.assertEqual(dmqueue.main(["pick", "--leads", os.path.join(self.tmp.name, "none.csv"),
                                       "--log", self.log]), 1)

    def test_cli_pick(self):
        self.sample(3)
        self.assertEqual(dmqueue.main(["pick", "--leads", self.leads, "--log", self.log,
                                       "--business", "lunch-lane", "--date", DAY.isoformat()]), 0)


if __name__ == "__main__":
    unittest.main()

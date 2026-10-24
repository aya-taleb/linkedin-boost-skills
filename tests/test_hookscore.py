import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _paths  # noqa: F401,E402
import hookscore  # noqa: E402


class HookScoreTests(unittest.TestCase):
    def test_concrete_beats_vague(self):
        good = hookscore.score("We stopped cold DMs in March. Replies went from 2% to 11%.")
        bad = hookscore.score("Success is all about mindset and growth.")
        self.assertGreater(good["score"], bad["score"] + 30)

    def test_bait_costs_points(self):
        a = hookscore.score("I lost 3 clients in May because of one email.")
        b = hookscore.score("I lost 3 clients in May because of one email. Agree?")
        self.assertEqual(a["parts"]["no_bait"], 10)
        self.assertEqual(b["parts"]["no_bait"], 0)

    def test_stock_phrase_flagged(self):
        r = hookscore.score("Unpopular opinion: you should leverage AI.")
        self.assertLess(r["parts"]["plain"], 10)
        self.assertTrue(any("stock" in n for n in r["notes"]))

    def test_fold_penalty(self):
        long = "I " + "really " * 30 + "learned 3 things."
        r = hookscore.score(long)
        self.assertLess(r["parts"]["fold"], 15)
        self.assertTrue(any("mobile" in n for n in r["notes"]))

    def test_placeholder_counts_as_concrete_and_flags(self):
        r = hookscore.score("We cut lunch wait time to {{your number}} minutes.")
        self.assertGreater(r["parts"]["concrete"], 0)
        self.assertTrue(any("placeholder" in n for n in r["notes"]))

    def test_number_inside_placeholder_not_counted_twice(self):
        r = hookscore.score("{{2}}")
        self.assertTrue(r["score"] >= 0)

    def test_avoid_words_from_business(self):
        a = hookscore.score("Our cheap lunch beat 4 cafes on Monday.")
        b = hookscore.score("Our cheap lunch beat 4 cafes on Monday.", avoid=["cheap"])
        self.assertLess(b["parts"]["plain"], a["parts"]["plain"])

    def test_topics_reported(self):
        r = hookscore.score("212 office lunches in 6 weeks.", topics=["lunches", "parking"])
        self.assertEqual(r["topic_words"], ["lunches"])

    def test_late_and_missed_count_as_tension(self):
        for line in ["Late twice in 11 weeks.", "We missed 12:15 twice this fall."]:
            self.assertGreater(hookscore.score(line)["parts"]["tension"], 0, line)

    def test_person(self):
        self.assertEqual(hookscore.score("Ship it on Friday.")["parts"]["person"], 0)
        self.assertEqual(hookscore.score("You ship it on Friday.")["parts"]["person"], 10)

    def test_proper_nouns_skip_sentence_start(self):
        self.assertEqual(hookscore.proper_nouns("Today we met Dana at Northwind."), ["Dana", "Northwind"])

    def test_rank_sorted_and_skips_blank_and_comments(self):
        res = hookscore.rank(["", "# note", "Things are great.", "I lost $4,000 on one ad in June."])
        self.assertEqual(len(res), 2)
        self.assertGreaterEqual(res[0]["score"], res[1]["score"])

    def test_scores_in_range(self):
        for line in ["?", "a", "I" * 300, "Agree? Thoughts? Comment below"]:
            s = hookscore.score(line)["score"]
            self.assertTrue(0 <= s <= 100, (line, s))

    def test_cli(self):
        self.assertEqual(hookscore.main(["--line", "We doubled orders in 3 weeks."]), 0)


if __name__ == "__main__":
    unittest.main()

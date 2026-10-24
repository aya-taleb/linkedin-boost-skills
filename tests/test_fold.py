import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _paths  # noqa: F401,E402
import fold  # noqa: E402


class FoldTests(unittest.TestCase):
    def test_short_post_shows_whole(self):
        r = fold.report("One short line.")
        self.assertFalse(r["views"]["mobile"]["cut"])
        self.assertFalse(r["views"]["desktop"]["cut"])

    def test_mobile_cuts_at_three_lines(self):
        text = "Line one.\n\nLine two.\n\nLine three."
        shown, cut = fold.visible(text, 3, 140, 48)
        self.assertTrue(cut)
        self.assertEqual(shown, "Line one.\n\nLine two.")

    def test_blank_lines_count(self):
        text = "A\n\n\n\nB"
        shown, cut = fold.visible(text, 3, 140, 48)
        self.assertTrue(cut)
        self.assertNotIn("B", shown)

    def test_character_cap_cuts_on_word(self):
        text = "word " * 60
        shown, cut = fold.visible(text, 5, 210, 80)
        self.assertTrue(cut)
        self.assertLessEqual(len(shown.replace("\n", " ")), 210)
        self.assertFalse(shown.endswith("wor"))

    def test_desktop_shows_more_than_mobile(self):
        text = "\n".join("Sentence number %d here." % i for i in range(10))
        r = fold.report(text)
        self.assertGreater(len(r["views"]["desktop"]["shown"]), len(r["views"]["mobile"]["shown"]))

    def test_media_view_only(self):
        r = fold.report("Hello\nthere", media=True)
        self.assertEqual(list(r["views"]), ["media"])

    def test_long_first_line_warns(self):
        r = fold.report("x " * 100)
        self.assertTrue(any("first line" in w for w in r["warnings"]))
        self.assertFalse(r["views"]["mobile"]["hook_whole"])

    def test_link_and_hashtags_warn(self):
        r = fold.report("Hook\n\nbody https://example.com\n\n#a #b #c #d")
        joined = " ".join(r["warnings"])
        self.assertIn("link", joined)
        self.assertIn("hashtags", joined)

    def test_over_limit_warns(self):
        r = fold.report("a" * 3001)
        self.assertTrue(any("3000" in w for w in r["warnings"]))

    def test_render_has_both_views(self):
        out = fold.render(fold.report("Hook line.\n\nMore."))
        self.assertIn("MOBILE", out)
        self.assertIn("DESKTOP", out)
        self.assertIn(fold.CHECKED, out)

    def test_wrap_long_word(self):
        self.assertEqual(fold.wrap("a" * 100, 48)[0], "a" * 48)


if __name__ == "__main__":
    unittest.main()

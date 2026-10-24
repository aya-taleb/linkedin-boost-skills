import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _paths  # noqa: F401,E402
import postlog  # noqa: E402


class PostLogTests(unittest.TestCase):
    def test_add_creates_header_and_rows(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "biz", "posts.csv")
            postlog.add_row(path, {"date": "2026-10-20", "topic": "lunch", "first_line": "Hi\nthere"})
            postlog.add_row(path, {"date": "2026-10-22", "topic": "offices"})
            rows = postlog.read_rows(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["first_line"], "Hi there")
            self.assertEqual(rows[1]["impressions"], "")
            with open(path, encoding="utf-8") as fh:
                self.assertTrue(fh.readline().startswith("date,type,topic"))

    def test_read_missing_file(self):
        self.assertEqual(postlog.read_rows("/nonexistent/posts.csv"), [])

    def test_cli_add_and_list(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "posts.csv")
            self.assertEqual(postlog.main(["add", "--log", path, "--date", "2026-10-23",
                                           "--topic", "t", "--first-line", "x"]), 0)
            self.assertEqual(postlog.main(["list", "--log", path]), 0)

    def test_save_draft_makes_folders_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "draft.md")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write("Line one\n")
            dest = os.path.join(d, "social", "biz", "drafts", "2026-10-23-x.md")
            self.assertEqual(postlog.main(["save", "--from", src, "--to", dest]), 0)
            with open(dest, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "Line one\n")
            self.assertEqual(postlog.main(["save", "--from", src, "--to", dest]), 1)
            self.assertEqual(postlog.main(["save", "--from", src, "--to", dest, "--force"]), 0)

    def test_save_to_founder_path_uses_founder_home(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {"FOUNDER_HOME": d}):
            src = os.path.join(d, "draft.md")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write("Line one\n")
            out = postlog.save_draft(src, "~/.founder/social/linkedin/biz/drafts/x.md")
            self.assertEqual(out, os.path.join(d, "social", "linkedin", "biz", "drafts", "x.md"))
            self.assertTrue(os.path.isfile(out))


if __name__ == "__main__":
    unittest.main()

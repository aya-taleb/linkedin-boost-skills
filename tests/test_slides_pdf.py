import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _paths  # noqa: F401,E402
import slides_pdf  # noqa: E402

SAMPLE = """# Cover line here
Swipe for the route.
> Lunch Lane
---
# Step 1
Pick one building.
---
# Step 2
Talk to the front desk (they know who orders lunch).
---
# Your turn
Save this for Monday.
"""


class SlidesTests(unittest.TestCase):
    def test_parse(self):
        s = slides_pdf.parse(SAMPLE)
        self.assertEqual(len(s), 4)
        self.assertEqual(s[0]["title"], "Cover line here")
        self.assertEqual(s[0]["foot"], "Lunch Lane")
        self.assertEqual(s[1]["body"], ["Pick one building."])

    def test_check_warnings(self):
        s = slides_pdf.parse("# a\n---\nno title {{x}}\n")
        w = " ".join(slides_pdf.check(s))
        self.assertIn("at least 3", w)
        self.assertIn("no '# ' title", w)
        self.assertIn("placeholder", w)
        many = slides_pdf.parse("# t\n" + "word " * 60)
        self.assertTrue(any("words" in x for x in slides_pdf.check(many)))

    def test_pdf_structure(self):
        data = slides_pdf.build_pdf(slides_pdf.parse(SAMPLE))
        self.assertTrue(data.startswith(b"%PDF-1.4"))
        self.assertTrue(data.rstrip().endswith(b"%%EOF"))
        self.assertEqual(data.count(b"/Type /Page "), 4)
        self.assertIn(b"/Count 4", data)
        # parentheses in text are escaped
        self.assertIn(b"\\(they know", data)
        # xref offsets point at objects
        xref = int(data.rsplit(b"startxref\n", 1)[1].split(b"\n")[0])
        self.assertTrue(data[xref:].startswith(b"xref"))
        table = data[xref:].split(b"\n")[3:]
        first = int(table[0][:10])
        self.assertTrue(data[first:].startswith(b"1 0 obj"))

    def test_bad_color(self):
        with self.assertRaises(ValueError):
            slides_pdf.hex_rgb("red")

    def test_cli_writes_file(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "slides.md")
            out = os.path.join(d, "c.pdf")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(SAMPLE)
            self.assertEqual(slides_pdf.main([src, "--out", out]), 0)
            self.assertGreater(os.path.getsize(out), 500)
            self.assertEqual(slides_pdf.main([src, "--check"]), 0)

    def test_wrap(self):
        lines = slides_pdf.wrap("one two three four five six seven eight nine ten", 72, 888)
        self.assertTrue(all(len(l) <= int(888 / (72 * slides_pdf.AVG_W)) for l in lines))


if __name__ == "__main__":
    unittest.main()

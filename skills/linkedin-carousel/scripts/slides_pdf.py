#!/usr/bin/env python3
"""Turn a slides.md file into a square PDF you can upload as a LinkedIn document post.

slides.md format: slides separated by a line with only '---'. In each slide, the first
line starting with '# ' is the big line, everything else is smaller body text.
Lines starting with '> ' become a small footer (a name or handle).

  # I sold 212 lunches to offices in 6 weeks
  Here is the route that worked.
  > Lunch Lane
  ---
  # Step 1: pick one building
  ...

Usage:
  python3 slides_pdf.py slides.md --out carousel.pdf
  python3 slides_pdf.py slides.md --out carousel.pdf --bg "#111111" --fg "#F5F0E6" --accent "#E4572E"
  python3 slides_pdf.py slides.md --check     # word counts and warnings only

The PDF uses the built-in Helvetica font, so plain Latin text only (accents in Latin-1 are
fine). For custom fonts or images, use the design brief in a design tool instead.
Standard library only. Nothing leaves your machine.
"""
import argparse
import re
import sys

SIZE = 1080  # points; square pages read well in the feed
MARGIN = 96
MAX_PAGES = 300  # LinkedIn document limit, checked 2026-10-23, see references/limits.md
MAX_MB = 100
TITLE_PT = 72
BODY_PT = 40
FOOT_PT = 26
# average Helvetica glyph width as a share of the font size, close enough for wrapping
AVG_W = 0.52
MAX_WORDS = 40


def parse(text):
    slides = []
    for block in re.split(r"(?m)^---\s*$", text):
        lines = [l.rstrip() for l in block.strip().splitlines()]
        if not any(lines):
            continue
        title, body, foot = "", [], ""
        for line in lines:
            if line.startswith("# ") and not title:
                title = line[2:].strip()
            elif line.startswith("> "):
                foot = line[2:].strip()
            else:
                body.append(line)
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        slides.append({"title": title, "body": body, "foot": foot})
    return slides


def check(slides):
    warnings = []
    if len(slides) > MAX_PAGES:
        warnings.append("%d slides; LinkedIn takes up to %d pages" % (len(slides), MAX_PAGES))
    if len(slides) < 3:
        warnings.append("only %d slides; a swipe needs at least 3" % len(slides))
    for i, s in enumerate(slides, 1):
        words = len((s["title"] + " " + " ".join(s["body"])).split())
        if words > MAX_WORDS:
            warnings.append("slide %d has %d words; aim for %d or fewer so it reads on a phone"
                            % (i, words, MAX_WORDS))
        if not s["title"]:
            warnings.append("slide %d has no '# ' title line" % i)
        if "{{" in s["title"] + " ".join(s["body"]):
            warnings.append("slide %d still has a {{placeholder}}; fill it before uploading" % i)
    return warnings


def hex_rgb(value):
    v = value.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", v):
        raise ValueError("colors look like #1A2B3C, got %r" % value)
    return tuple(int(v[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def wrap(text, pt, width):
    max_chars = max(8, int(width / (pt * AVG_W)))
    words, lines, cur = text.split(), [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(text):
    data = text.encode("latin-1", "replace").decode("latin-1")
    return data.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def page_stream(slide, n, total, bg, fg, accent):
    ops = ["%.3f %.3f %.3f rg 0 0 %d %d re f" % (bg + (SIZE, SIZE))]
    ops.append("%.3f %.3f %.3f rg %d %d 120 10 re f" % (accent + (MARGIN, SIZE - MARGIN)))
    y = SIZE - MARGIN - 40 - TITLE_PT
    width = SIZE - 2 * MARGIN
    ops.append("%.3f %.3f %.3f rg" % fg)
    for line in wrap(slide["title"], TITLE_PT, width):
        ops.append("BT /F2 %d Tf %d %d Td (%s) Tj ET" % (TITLE_PT, MARGIN, y, esc(line)))
        y -= int(TITLE_PT * 1.15)
    y -= 30
    for para in slide["body"]:
        if not para.strip():
            y -= int(BODY_PT * 0.6)
            continue
        for line in wrap(para, BODY_PT, width):
            ops.append("BT /F1 %d Tf %d %d Td (%s) Tj ET" % (BODY_PT, MARGIN, y, esc(line)))
            y -= int(BODY_PT * 1.35)
    foot = slide["foot"]
    ops.append("%.3f %.3f %.3f rg" % accent)
    if foot:
        ops.append("BT /F1 %d Tf %d %d Td (%s) Tj ET" % (FOOT_PT, MARGIN, MARGIN - 20, esc(foot)))
    ops.append("BT /F1 %d Tf %d %d Td (%d/%d) Tj ET" % (FOOT_PT, SIZE - MARGIN - 70, MARGIN - 20, n, total))
    return "\n".join(ops).encode("latin-1")


def build_pdf(slides, bg="#FFFFFF", fg="#111111", accent="#E4572E"):
    bg, fg, accent = hex_rgb(bg), hex_rgb(fg), hex_rgb(accent)
    objects = []

    def add(body):
        objects.append(body)
        return len(objects)

    catalog = add(None)
    pages = add(None)
    f1 = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    f2 = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    kids = []
    total = len(slides)
    for i, s in enumerate(slides, 1):
        stream = page_stream(s, i, total, bg, fg, accent)
        content = add(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
        page = add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %d %d] /Contents %d 0 R "
                    "/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> >>"
                    % (pages, SIZE, SIZE, content, f1, f2)).encode())
        kids.append(page)
    objects[catalog - 1] = ("<< /Type /Catalog /Pages %d 0 R >>" % pages).encode()
    objects[pages - 1] = ("<< /Type /Pages /Kids [%s] /Count %d >>"
                          % (" ".join("%d 0 R" % k for k in kids), len(kids))).encode()
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for n, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % n + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, catalog, xref)
    return bytes(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("slides")
    parser.add_argument("--out")
    parser.add_argument("--bg", default="#FFFFFF")
    parser.add_argument("--fg", default="#111111")
    parser.add_argument("--accent", default="#E4572E")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    with open(args.slides, encoding="utf-8") as fh:
        slides = parse(fh.read())
    warnings = check(slides)
    print("%d slides" % len(slides))
    for w in warnings:
        print("warning: " + w)
    if args.check:
        return 0
    if not args.out:
        parser.error("--out is needed unless you pass --check")
    data = build_pdf(slides, args.bg, args.fg, args.accent)
    if len(data) > MAX_MB * 1024 * 1024:
        print("warning: PDF is over %d MB" % MAX_MB)
    with open(args.out, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d KB)" % (args.out, max(1, len(data) // 1024)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

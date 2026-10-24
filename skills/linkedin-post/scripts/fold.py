#!/usr/bin/env python3
"""Show what a LinkedIn post shows before "see more", on mobile and on desktop.

LinkedIn does not publish its cutoff. These defaults are observed values, checked
2026-10-23 against public sources listed in references/feed-limits.md:
  mobile, text only    about 3 lines or about 140 characters, whichever comes first
  desktop, text only   about 5 lines or about 210 characters
  any post with an image, video or document: about 3 lines on both
A line break counts as a full line, and a blank line counts too.

Usage:
  python3 fold.py draft.txt
  python3 fold.py draft.txt --media          # post has an image, video or PDF
  python3 fold.py draft.txt --json
  cat draft.txt | python3 fold.py -

Standard library only. Nothing leaves your machine.
"""
import argparse
import json
import re
import sys

CHECKED = "2026-10-23"
POST_LIMIT = 3000

# name: (max visual lines, max characters, characters per wrapped line)
VIEWS = {
    "mobile": (3, 140, 48),
    "desktop": (5, 210, 80),
    "media": (3, 140, 48),
}

LINK = re.compile(r"(https?://|www\.)\S+", re.I)
HASHTAG = re.compile(r"(?<!\w)#\w+")


def wrap(line, width):
    """Split one paragraph line into visual lines of at most `width` characters."""
    if not line:
        return [""]
    words = line.split(" ")
    out, cur = [], ""
    for word in words:
        while len(word) > width:  # a very long word or URL
            if cur:
                out.append(cur)
                cur = ""
            out.append(word[:width])
            word = word[width:]
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= width:
            cur += " " + word
        else:
            out.append(cur)
            cur = word
    out.append(cur)
    return out


def visible(text, max_lines, max_chars, width):
    """Return the part of `text` shown before "see more" for one view."""
    text = text.replace("\r\n", "\n").strip("\n")
    shown, used_lines, used_chars = [], 0, 0
    for para in text.split("\n"):
        for vline in wrap(para, width):
            if used_lines >= max_lines:
                return "\n".join(shown).rstrip(), True
            room = max_chars - used_chars
            if len(vline) > room:
                cut = vline[:room]
                if " " in cut:
                    cut = cut[: cut.rfind(" ")]
                shown.append(cut)
                return "\n".join(shown).rstrip(), True
            shown.append(vline)
            used_lines += 1
            used_chars += len(vline) + (1 if vline else 0)
    return "\n".join(shown).rstrip(), False


def first_sentence_whole(shown, text):
    """True if the first sentence or first line of the post ends inside the shown part."""
    first_line = text.strip().split("\n", 1)[0].strip()
    if not first_line:
        return True
    flat = " ".join(shown.split())
    return " ".join(first_line.split()) in flat


def report(text, media=False):
    text = text.replace("\r\n", "\n")
    views = ["media"] if media else ["mobile", "desktop"]
    result = {"checked": CHECKED, "characters": len(text.strip()), "views": {}, "warnings": []}
    for name in views:
        lines, chars, width = VIEWS[name]
        shown, cut = visible(text, lines, chars, width)
        result["views"][name] = {
            "shown": shown,
            "cut": cut,
            "hook_whole": first_sentence_whole(shown, text),
        }
        if not result["views"][name]["hook_whole"]:
            result["warnings"].append("%s: the first line is cut off before it ends" % name)
    if result["characters"] > POST_LIMIT:
        result["warnings"].append("over the %d character post limit by %d"
                                  % (POST_LIMIT, result["characters"] - POST_LIMIT))
    if LINK.search(text):
        result["warnings"].append("link in the post body; most people put it in the first comment")
    tags = HASHTAG.findall(text)
    if len(tags) > 3:
        result["warnings"].append("%d hashtags; 3 or fewer reads cleaner" % len(tags))
    first = text.strip().split("\n", 1)[0]
    if len(first) > VIEWS["mobile"][1]:
        result["warnings"].append("first line is %d characters; mobile shows about %d"
                                  % (len(first), VIEWS["mobile"][1]))
    return result


def render(result):
    labels = {
        "mobile": "MOBILE (about 3 lines or 140 characters)",
        "desktop": "DESKTOP (about 5 lines or 210 characters)",
        "media": "WITH IMAGE, VIDEO OR DOCUMENT (about 3 lines)",
    }
    out = ["Before \"see more\" (observed cutoffs, checked %s)" % result["checked"], ""]
    for name, view in result["views"].items():
        out.append(labels[name])
        for line in view["shown"].split("\n"):
            out.append("  | " + line)
        out.append("  | ...see more" if view["cut"] else "  | (whole post shows)")
        out.append("")
    out.append("length: %d of %d characters" % (result["characters"], POST_LIMIT))
    for w in result["warnings"]:
        out.append("warning: " + w)
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", help="draft text file, or - for stdin")
    parser.add_argument("--media", action="store_true", help="post has an image, video or document")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.file == "-":
        text = sys.stdin.read()
    else:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    result = report(text, media=args.media)
    print(json.dumps(result, indent=2) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
